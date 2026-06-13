#!/usr/bin/env python3
"""Playwright: intercept all API calls on Capital PCF and Taiwan Index constituents."""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(r"d:\ETF\output\pcf_scrape")

jobs = [
    ("00919_cap", "https://www.capitalfund.com.tw/etf/pcf/00919", []),
    ("IX0170", "https://www.taiwanindex.com.tw/indexes/IX0170", ["text=成分股", "text=成分", "a:has-text('成分')"]),
    ("IX0179", "https://www.taiwanindex.com.tw/indexes/IX0179", ["text=成分股", "text=成分", "a:has-text('成分')"]),
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(ignore_https_errors=True)
    page = ctx.new_page()
    log = []

    def on_resp(resp):
        url = resp.url
        if not any(x in url for x in ("api", "CFWeb", "backend.taiwanindex", "cwapi")):
            return
        try:
            ct = resp.headers.get("content-type", "")
            if "json" in ct or "text" in ct:
                body = resp.text()
                if len(body) > 80:
                    log.append({"url": url, "status": resp.status, "body": body[:8000]})
        except Exception:
            pass

    page.on("response", on_resp)

    for name, url, clicks in jobs:
        log.clear()
        print(f"=== {name} ===")
        page.goto(url, wait_until="networkidle", timeout=90000)
        page.wait_for_timeout(3000)
        for sel in clicks:
            loc = page.locator(sel)
            if loc.count():
                try:
                    loc.first.click()
                    page.wait_for_timeout(4000)
                    print(f"  clicked {sel}")
                except Exception as e:
                    print(f"  click fail {sel}: {e}")
        # scroll to trigger lazy load
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(3000)

        out = OUT / f"{name}_network.json"
        out.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  captured {len(log)} responses -> {out.name}")
        for item in log:
            u = item["url"]
            if any(k in u.lower() for k in ("buyback", "stock", "weight", "constitu", "pcf", "hold", "index")):
                print(f"   * {u[:120]} len={len(item['body'])}")
                if "stocks" in item["body"] or "stockWeights" in item["body"] or "weight" in item["body"].lower():
                    (OUT / f"{name}_hit.json").write_text(item["body"], encoding="utf-8")

    browser.close()

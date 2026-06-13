#!/usr/bin/env python3
import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(r"d:\ETF\output\pcf_scrape")

for ticker in ("00919", "00929"):
    url = f"https://www.pocket.tw/etf/tw/{ticker}/fundholding"
    captured = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        def on_resp(resp):
            if "GetDtnoData" in resp.url:
                try:
                    captured.append({"url": resp.url, "body": resp.text()[:20000]})
                except Exception:
                    pass

        page.on("response", on_resp)
        page.goto(url, wait_until="networkidle", timeout=120000)
        page.wait_for_timeout(5000)
        html = page.content()
        (OUT / f"pocket_{ticker}_fundholding.html").write_text(html, encoding="utf-8")
        (OUT / f"pocket_{ticker}_fundholding_net.json").write_text(
            json.dumps(captured, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        rows = re.findall(r"(\d{4,5})[^0-9%]{0,40}(\d+\.\d+)\s*%", html)
        print(ticker, "fundholding captured", len(captured), "dom rows", len(rows), rows[:5])
        browser.close()

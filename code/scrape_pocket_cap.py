#!/usr/bin/env python3
import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(r"d:\ETF\output\pcf_scrape")

urls = [
    ("pocket_00919", "https://www.pocket.tw/etf/tw/00919"),
    ("pocket_00929", "https://www.pocket.tw/etf/tw/00929"),
    ("cap_pcf", "https://www.capitalfund.com.tw/etf/pcf/00919"),
    ("fh_pcf", "https://www.fhtrust.com.tw/ETF/trade_list"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    captured = []

    def on_resp(resp):
        url = resp.url
        if any(x in url for x in ("api", "buyback", "ETFPcf", "pocket", "hold", "constitu", "weight", "pcf")):
            try:
                body = resp.text()
                if len(body) > 80:
                    captured.append({"url": url, "body": body[:12000]})
            except Exception:
                pass

    page.on("response", on_resp)

    for name, url in urls:
        captured.clear()
        print(f"=== {name} ===")
        page.goto(url, wait_until="networkidle", timeout=120000)
        page.wait_for_timeout(8000)
        if name == "fh_pcf":
            # try select 00929
            for sel in ("select", "#fundID"):
                if page.locator(sel).count():
                    try:
                        page.locator(sel).first.select_option(label="00929")
                    except Exception:
                        try:
                            page.locator(sel).first.select_option(value="ETF21")
                        except Exception:
                            pass
            page.wait_for_timeout(5000)
        html = page.content()
        (OUT / f"{name}.html").write_text(html, encoding="utf-8")
        (OUT / f"{name}_net.json").write_text(json.dumps(captured, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  captured {len(captured)} api responses")
        for c in captured:
            print(" ", c["url"][:100])
            if any(k in c["body"].lower() for k in ("weight", "stocks", "constitu", "stockcode", "stocno")):
                (OUT / f"{name}_hit.json").write_text(c["body"], encoding="utf-8")
                print("   -> HIT saved")
        # DOM table parse
        rows = re.findall(r"(\d{4,5})[^0-9%]{0,60}(\d+\.\d+)\s*%", html)
        print(f"  dom rows {len(rows)} sample {rows[:3]}")

    browser.close()

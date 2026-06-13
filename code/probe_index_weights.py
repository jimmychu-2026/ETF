#!/usr/bin/env python3
import json
import ssl
import urllib.request

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

import sys
sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

# Taiwan Index SSR pages
for code in ("IX0170", "IX0179", "IX0179"):
    for path in (
        f"https://www.taiwanindex.com.tw/indexes/{code}/constituents",
        f"https://www.taiwanindex.com.tw/indexes/{code}",
        f"https://www.taiwanindex.com.tw/zh-tw/indexes/{code}/constituents",
    ):
        try:
            html = fetch_url(path)
            has_nuxt = "__NUXT__" in html
            has_weight = "weight" in html.lower() or "權重" in html
            print(path, "len", len(html), "nuxt", has_nuxt, "weight", has_weight)
            if has_nuxt:
                open(rf"d:\ETF\output\tip_{code}.html", "w", encoding="utf-8").write(html)
        except Exception as e:
            print(path, "ERR", e)

# pocket.tw ETF holdings
for ticker in ("00919", "00929", "00878"):
    for url in (
        f"https://pocket.tw/etf/{ticker}",
        f"https://pocket.tw/ETF/{ticker}",
        f"https://www.pocket.tw/etf/{ticker}/constituents",
    ):
        try:
            html = fetch_url(url)
            if len(html) > 500 and "404" not in html[:200]:
                print(url, "len", len(html), "weight", ("weight" in html.lower() or "權重" in html))
        except Exception as e:
            pass

# FinMind TaiwanStockETFHoldings if exists
url = "https://api.finmindtrade.com/api/v4/data?dataset=TaiwanStockETFHoldings&data_id=00919&start_date=2026-06-01"
try:
    body = fetch_url(url)
    print("FinMind ETFHoldings:", body[:500])
except Exception as e:
    print("FinMind ERR", e)

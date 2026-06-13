#!/usr/bin/env python3
import json
import ssl
import urllib.parse
import urllib.request

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

import sys
sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url, finmind_get

# FinMind dataset probe
for ds in (
    "TaiwanStockETFHoldings",
    "TaiwanStockETFPortfolio",
    "TaiwanStockETFConstituent",
    "TaiwanStockETF",
):
    try:
        rows = finmind_get(ds, data_id="00919", start_date="2026-06-01", end_date="2026-06-09")
        print(ds, "rows", len(rows), rows[:2] if rows else "")
    except Exception as e:
        print(ds, "ERR", e)

# Fuh Hwa endpoints
for ep in ("ETFindex", "ETFRTnav", "frontdetail", "fundList"):
    for q in ("fundID=ETF21", "etf002=00929", "fundID=00929"):
        try:
            body = fetch_url(f"https://www.fhtrust.com.tw/api/{ep}?{q}")
            if body.lstrip().startswith("{") and len(body) > 100:
                print(ep, q, body[:600])
        except Exception as e:
            pass

# TWSE ETF portfolio
for url in (
    "https://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL?response=json",
    "https://www.twse.com.tw/rwd/zh/ETF/report/etfPortfolio?response=json&date=20260606&stockNo=00919",
    "https://www.twse.com.tw/rwd/zh/ETF/report/etfPortfolio?response=json&date=20260609&stockNo=00919",
):
    try:
        body = fetch_url(url)
        print("TWSE", url.split("?")[0].split("/")[-1], len(body), body[:300].replace("\n", " "))
    except Exception as e:
        print("TWSE ERR", e)

# Taiwan Index - try with lang param
for code in ("IX0170", "IX0179"):
    for path in (
        f"indexes/{code}/constituent_weight_records?lang=tw",
        f"indexes/{code}/constituents?lang=tw",
        f"index_constituents/{code}",
        f"IndexConstituents/{code}",
    ):
        url = f"https://backend.taiwanindex.com.tw/api/{path}"
        try:
            body = fetch_url(url)
            if len(body) > 100 and body.lstrip().startswith("{"):
                print("TIP", path, body[:400])
        except Exception:
            pass

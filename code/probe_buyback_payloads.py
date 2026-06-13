#!/usr/bin/env python3
import json
import ssl
import urllib.request

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

url = "https://www.capitalfund.com.tw/CFWeb/api/etf/buyback"
payloads = [
    {"fundNo": "195       "},
    {"fundNo": "195", "tradeDate": "2026/06/09"},
    {"fundNo": "195", "tdate": "2026-06-09"},
    {"stocNo": "00919", "tradeDate": "2026/06/09"},
    {"fundNo": "195", "date": "20260609"},
    {"fundNo": "195", "pcfDate": "2026/06/09"},
    {"itemNo": "00919", "pcfDate": "2026/06/09"},
]

for pl in payloads:
    req = urllib.request.Request(
        url,
        data=json.dumps(pl).encode(),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Referer": "https://www.capitalfund.com.tw/etf/pcf/00919",
            "Origin": "https://www.capitalfund.com.tw",
            "User-Agent": "Mozilla/5.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            body = resp.read().decode()
            print("OK", pl, body[:2000])
            if "stocks" in body:
                open(r"d:\ETF\output\cap_buyback_hit.json", "w", encoding="utf-8").write(body)
    except Exception as e:
        print("ERR", pl, e)

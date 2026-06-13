#!/usr/bin/env python3
import re
import sys

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

js = fetch_url("https://www.cathaysite.com.tw/main.1047ac4f81a3da4e7643.js")
for needle in ("etfDetailHoldings", "ETF-Holdings", "getHoldings", "holdings/"):
    idx = 0
    while True:
        i = js.find(needle, idx)
        if i < 0:
            break
        print("---", needle, "---")
        print(js[max(0, i - 120) : i + 280])
        idx = i + len(needle)

cap = fetch_url("https://www.capitalfund.com.tw/main.bdc1e85b555aa797.js")
for needle in ("pcf", "PCF", "holdings", "Holdings", "constituent", "stockHold"):
    if needle.lower() not in cap.lower():
        continue
    for m in re.finditer(rf'.{{0,80}}{re.escape(needle)}.{{0,120}}', cap, re.I):
        s = m.group(0)
        if "facebook" in s:
            continue
        if "/api/" in s or "CFWeb" in s or "pcf" in s.lower():
            print("CAP", s[:200])

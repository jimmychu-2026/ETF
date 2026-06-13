#!/usr/bin/env python3
import json
import re
import sys

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

js = fetch_url("https://www.cathaysite.com.tw/main.1047ac4f81a3da4e7643.js")

# Find PCF / BuySale component
for needle in ("GetStocksList(", "stockWeights", "StocksList", "trade/pcf", "ETF-Purchase"):
    idx = 0
    n = 0
    while n < 10:
        i = js.find(needle, idx)
        if i < 0:
            break
        chunk = js[max(0, i - 400) : i + 600]
        if "GetPromise" not in chunk or needle != "GetStocksList(":
            print(f"\n--- {needle} ---")
            print(chunk[:900])
        idx = i + len(needle)
        n += 1

# ObjToParam - understand query param casing
m = re.search(r"ObjToParam\([a-zA-Z]\)\{.{0,600}?\}", js)
if m:
    print("\nObjToParam:", m.group(0)[:600])

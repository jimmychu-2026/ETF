#!/usr/bin/env python3
import re
import sys

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

js = fetch_url("https://www.cathaysite.com.tw/main.1047ac4f81a3da4e7643.js")

# GetPromise implementation
for needle in ("GetPromise(", "getPromise("):
    idx = 0
    while True:
        i = js.find(needle, idx)
        if i < 0:
            break
        print(f"=== {needle} at {i} ===")
        print(js[max(0, i - 100) : i + 800])
        idx = i + len(needle)
        if idx > i + 3000:
            break

# Find usages of GetIndexStockWeights(
for m in re.finditer(r"GetIndexStockWeights\(", js):
    start = m.start()
    print("\n=== usage ===")
    print(js[max(0, start - 300) : start + 500])

# Find pcf related in cathay
for needle in ("pcf", "PCF", "00878", "IndexStock", "stockWeight", "Weighting"):
    if needle == "Weighting":
        pass
    count = js.count(needle)
    if count and needle in ("GetIndexStockWeights", "pcf", "IndexStock"):
        print(f"count {needle}: {count}")

cap = fetch_url("https://www.capitalfund.com.tw/main.bdc1e85b555aa797.js")
for m in re.finditer(r"stocNo|weightRound|\.stocks", cap):
    s = cap[max(0, m.start() - 200) : m.start() + 300]
    if "http" in s or "api" in s or "subscribe" in s or "get" in s.lower():
        print("\nCAP:", s[:450])

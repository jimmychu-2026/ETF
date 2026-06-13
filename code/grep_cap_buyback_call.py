#!/usr/bin/env python3
import re
import sys

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

cap = fetch_url("https://www.capitalfund.com.tw/main.bdc1e85b555aa797.js")

for needle in ("getBuyback", "buyback(", ".buyback"):
    idx = 0
    n = 0
    while n < 15:
        i = cap.find(needle, idx)
        if i < 0:
            break
        print(f"\n--- {needle} ---")
        print(cap[max(0, i - 250) : i + 450])
        idx = i + len(needle)
        n += 1

# search pcf component
for needle in ("pcf/", "EtfPcf", "etf-pcf", "app-pcf"):
    i = cap.find(needle)
    if i >= 0:
        print(f"\n=== {needle} ===")
        print(cap[max(0, i - 200) : i + 600])

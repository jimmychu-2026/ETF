#!/usr/bin/env python3
import json
import re
import ssl
import urllib.request

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

import sys
sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

cap = fetch_url("https://www.capitalfund.com.tw/main.bdc1e85b555aa797.js")

# find pcf object structure
for needle in ("pcf.", "y.pcf", "this.pcf", "getPcf", "loadPcf", "etfPcf", "PCF"):
    idx = 0
    while True:
        i = cap.find(needle, idx)
        if i < 0:
            break
        print(f"--- {needle} ---")
        print(cap[max(0, i - 150) : i + 350])
        idx = i + len(needle)
        if idx > i + 5000:
            break

# search exportEtfPortfolio for field names
i = cap.find("exportEtfPortfolio")
print("\n=== exportEtfPortfolio ===")
print(cap[i : i + 3000])

# search for stockList, stockWeight, holdings in capital js
for pat in (r"stockList", r"stockWeight", r"holdings", r"constituent", r"portfolioList", r"pcfStock"):
    for m in re.finditer(pat, cap, re.I):
        s = cap[max(0, m.start() - 80) : m.start() + 200]
        if "api" in s.lower() or "http" in s.lower() or "stock" in s.lower():
            print(f"HIT {pat}: {s[:250]}")

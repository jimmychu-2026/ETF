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

# Find PCF component - search for exportEtfPortfolio callers or portfolioData
for needle in ("exportEtfPortfolio", "portfolioData", "etfPortfolio", "pcfData", "loadPortfolio"):
    for m in re.finditer(needle, cap, re.I):
        print(f"\n=== {needle} ===")
        print(cap[max(0, m.start()-300):m.start()+500][:800])

# Search buyback payload fields in minified code
for m in re.finditer(r"getBuyback\([^)]+\)", cap):
    print("call:", m.group(0))

# Maybe PCF uses navPart
for m in re.finditer(r"navPart|getNavPart|/api/etf/navPart", cap, re.I):
    s = cap[max(0, m.start()-200):m.start()+300]
    print("\nnavPart:", s[:500])

# grep all http.post in cap related to etf
posts = re.findall(r'this\.http\.post\("(/api/etf/[^"]+)"', cap)
print("\nall etf posts:", sorted(set(posts)))

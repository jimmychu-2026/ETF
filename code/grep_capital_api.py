#!/usr/bin/env python3
import re
import sys

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

cap = fetch_url("https://www.capitalfund.com.tw/main.bdc1e85b555aa797.js")
apis = sorted(set(re.findall(r"/api/etf/[a-zA-Z0-9_/${}]+", cap)))
for a in apis:
    print(a)

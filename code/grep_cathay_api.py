#!/usr/bin/env python3
import json
import re
import sys

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

cath = fetch_url("https://www.cathaysite.com.tw/main.js")
apis = sorted(set(re.findall(r"/api/[a-zA-Z0-9_/${}.\-]+", cath)))
for a in apis:
    if "etf" in a.lower() or "hold" in a.lower() or "pcf" in a.lower():
        print(a)

print("\n--- all api ---")
for a in apis[:80]:
    print(a)

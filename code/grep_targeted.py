#!/usr/bin/env python3
import re
import sys

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

js = fetch_url("https://www.cathaysite.com.tw/main.1047ac4f81a3da4e7643.js")

# GetPromise definition
m = re.search(r"GetPromise\s*\([^)]*\)\s*\{[^}]{0,1200}\}", js)
if m:
    print("GetPromise def:", m.group(0)[:1200])
else:
    # try arrow function
    i = js.find("GetPromise(e,t")
    print("GetPromise ctx:", js[i:i+1500])

# IndexStockWeights usage - find component that calls it
for m in re.finditer(r".{0,80}IndexStockWeights.{0,200}", js):
    s = m.group(0)
    if "GetPromise" not in s:
        print("USE:", s[:280])

cap = fetch_url("https://www.capitalfund.com.tw/main.bdc1e85b555aa797.js")
# find buyback API
for m in re.finditer(r"buyback|Buyback|getBuyback|loadPcf|getPortfolio|etfPortfolio", cap, re.I):
    s = cap[max(0, m.start()-150):m.start()+400]
    if "http" in s or "/api/" in s:
        print("\nCAP buyback:", s[:500])

# find where stocks array is assigned
for m in re.finditer(r"stocks\s*=\s*[^;]{0,200}", cap):
    s = m.group(0)
    if len(s) > 20:
        print("\nCAP stocks assign:", s[:250])

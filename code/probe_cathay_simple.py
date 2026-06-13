#!/usr/bin/env python3
import json
import ssl
import urllib.request

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

import sys
sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

tests = [
    "https://www.cathaysite.com.tw/api/ETF/GetETFDetailStockList?ETFCode=00878",
    "https://www.cathaysite.com.tw/api/ETF/GetETFDetailStockList?FundCode=00878",
    "https://www.cathaysite.com.tw/api/ETF/GetIndexStockWeights?ETFCode=00878",
    "https://www.cathaysite.com.tw/api/ETF/GetETFInfoMain?ETFCode=00878",
    "https://www.cathaysite.com.tw/api/BuySale/GetLastPCFForeignCurr?ETFCode=00878",
]

for url in tests:
    try:
        body = fetch_url(url)
        print("URL:", url)
        print("LEN:", len(body), "HEAD:", body[:200].replace("\n", " "))
        print()
    except Exception as e:
        print("ERR", url, e)
        print()

# POST tests
for path, pl in [
    ("ETF/GetETFDetailStockList", {"ETFCode": "00878"}),
    ("BuySale/GetLastPCFForeignCurr", {"ETFCode": "00878"}),
]:
    url = f"https://www.cathaysite.com.tw/api/{path}"
    req = urllib.request.Request(
        url,
        data=json.dumps(pl).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            body = resp.read().decode()
            print("POST", url, "LEN", len(body), body[:300])
    except Exception as e:
        print("POST ERR", url, e)

#!/usr/bin/env python3
import json
import ssl
import urllib.parse
import urllib.request

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

BASE = "https://cwapi.cathaysite.com.tw/api"

import sys
sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url


def get(path, params):
    q = urllib.parse.urlencode(params)
    return fetch_url(f"{BASE}/{path}?{q}")


def post(path, params):
    url = f"{BASE}/{path}"
    req = urllib.request.Request(
        url,
        data=json.dumps(params).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        method="POST",
    )
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")


# 00878 Cathay
params_list = [
    {"ETFCode": "00878"},
    {"FundCode": "00878"},
    {"Code": "00878"},
    {"ETFNo": "00878"},
    {"FundNo": "ECN"},
    {"IndexCode": "ECN"},
]

for path in (
    "ETF/GetIndexStockWeights",
    "ETF/GetETFDetailStockList",
    "BuySale/GetLastPCFForeignCurr",
    "ETF/GetETFInfoMain",
):
    for pl in params_list:
        try:
            body = get(path, pl)
            if len(body) > 100:
                print(f"GET {path} {pl} len={len(body)}")
                print(body[:1500])
                print("---")
                open(
                    rf"d:\ETF\output\cathay_{path.replace('/','_')}.json",
                    "w",
                    encoding="utf-8",
                ).write(body)
        except Exception as e:
            print(f"ERR GET {path} {pl}: {e}")

# BuySale PCF endpoints - search js
js = fetch_url("https://www.cathaysite.com.tw/main.1047ac4f81a3da4e7643.js")
import re
hits = sorted(set(re.findall(r"api/BuySale/[A-Za-z0-9]+", js)))
print("BuySale endpoints:", hits)

for ep in hits:
    if "PCF" in ep or "Buy" in ep or "Stock" in ep or "ETF" in ep:
        for pl in ({"ETFCode": "00878"}, {"FundCode": "00878"}):
            try:
                body = get(ep.replace("api/", ""), pl)
                if len(body) > 100:
                    print(f"BS {ep} {pl}: {body[:800]}")
            except Exception as e:
                pass

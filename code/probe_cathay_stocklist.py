#!/usr/bin/env python3
import json
import re
import ssl
import urllib.parse
import urllib.request

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

import sys
sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

BASE = "https://www.cathaysite.com.tw/api"
REF = "https://www.cathaysite.com.tw/ETF/trade/pcf/00878"


def get(path, params):
    q = urllib.parse.urlencode(params)
    url = f"{BASE}/{path}?{q}"
    body = fetch_url(url)
    return url, body


def post(path, params):
    url = f"{BASE}/{path}"
    req = urllib.request.Request(
        url,
        data=json.dumps(params).encode(),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Referer": REF,
        },
        method="POST",
    )
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        return url, resp.read().decode("utf-8", "replace")


endpoints = [
    ("ETF/GetETFDetailStockList", {"ETFCode": "00878"}),
    ("ETF/GetETFDetailStockList", {"FundCode": "00878"}),
    ("ETF/GetETFDetailStockList", {"Code": "00878"}),
    ("ETF/GetETFDetailStockList", {"ETFNo": "00878"}),
    ("ETF/GetETFDetailStockList", {"FundNo": "ECN"}),
    ("ETF/GetIndexStockWeights", {"ETFCode": "00878"}),
    ("ETF/GetIndexStockWeights", {"FundCode": "00878"}),
    ("ETF/GetIndexStockWeights", {"IndexCode": "ECN"}),
    ("ETF/GetETFInfoMain", {"ETFCode": "00878"}),
    ("ETF/GetETFCode", {}),
    ("BuySale/GetLastPCFForeignCurr", {"ETFCode": "00878"}),
    ("BuySale/GetLastPCFForeignCurr", {"FundCode": "00878"}),
]

out = []
for path, params in endpoints:
    for fn, call in (("GET", get), ("POST", post)):
        try:
            url, body = call(path, params)
            if len(body) > 80 and not body.lstrip().startswith("<!"):
                out.append(f"{fn} {path} {params}\n{body[:2500]}\n")
        except Exception as e:
            err = str(e)
            if "404" not in err:
                out.append(f"{fn} ERR {path} {params} {err[:100]}\n")

js = fetch_url("https://www.cathaysite.com.tw/main.1047ac4f81a3da4e7643.js")
for needle in ("GetETFDetailStockList", "GetLastPCF", "GetIndexStockWeights"):
    for m in re.finditer(rf".{{0,200}}{needle}.{{0,400}}", js):
        s = m.group(0)
        if "GetPromise" not in s:
            out.append(f"JS {needle}: {s[:500]}\n")

open(r"d:\ETF\output\probe_cathay_stocklist.txt", "w", encoding="utf-8").write("".join(out))
print("written", len(out))

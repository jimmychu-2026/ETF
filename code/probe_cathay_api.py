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

BASE = "https://www.cathaysite.com.tw/api/ETF"
REF = "https://www.cathaysite.com.tw/ETF/trade/pcf/00878"


def try_get(path, params):
    q = urllib.parse.urlencode(params)
    url = f"{BASE}/{path}?{q}"
    try:
        body = fetch_url(url)
        return url, body
    except Exception as e:
        return url, f"ERR: {e}"


def try_post(path, params):
    url = f"{BASE}/{path}"
    body = json.dumps(params).encode()
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json,*/*",
            "User-Agent": "Mozilla/5.0",
            "Referer": REF,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
            return url, resp.read().decode("utf-8", "replace")
    except Exception as e:
        return url, f"ERR: {e}"


params_list = [
    {"ETFCode": "00878"},
    {"etfCode": "00878"},
    {"FundCode": "00878"},
    {"fundCode": "00878"},
    {"StockCode": "00878"},
    {"stockCode": "00878"},
    {"Code": "00878"},
    {"code": "00878"},
    {"Symbol": "00878"},
    {"symbol": "00878"},
    {"ETFNo": "00878"},
    {"FundNo": "ECN"},
    {"IndexCode": "ECN"},
    {"indexCode": "ECN"},
    {"ETFCode": "00878", "Lang": "tw"},
    {"ETFCode": "00878", "lang": "tw"},
]

out = []
for pl in params_list:
    url, body = try_get("GetIndexStockWeights", pl)
    if not body.startswith("ERR") and len(body) > 80 and not body.lstrip().startswith("<!"):
        out.append(f"GET OK {pl}\n{body[:2000]}")
    url, body = try_post("GetIndexStockWeights", pl)
    if not body.startswith("ERR") and len(body) > 80 and not body.lstrip().startswith("<!"):
        out.append(f"POST OK {pl}\n{body[:2000]}")

# search js for GetIndexStockWeights call site
js = fetch_url("https://www.cathaysite.com.tw/main.1047ac4f81a3da4e7643.js")
for m in re.finditer(r"GetIndexStockWeights[^;]{0,400}", js):
    out.append("JS call: " + m.group(0)[:400])

# also try GetETFDetailBalList (holdings?)
for path in ("GetETFDetailBalList", "GetETFDetailBondList", "DownloadETFWeightExcel"):
    for pl in ({"ETFCode": "00878"}, {"etfCode": "00878"}, {"Code": "00878"}):
        url, body = try_post(path, pl)
        if not body.startswith("ERR") and len(body) > 80:
            out.append(f"{path} POST {pl}: {body[:1500]}")

open(r"d:\ETF\output\probe_cathay_api.txt", "w", encoding="utf-8").write("\n".join(out))
print("hits", len(out))

#!/usr/bin/env python3
import json
import re
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
    url = f"{BASE}/{path}?{q}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")


js = fetch_url("https://www.cathaysite.com.tw/main.1047ac4f81a3da4e7643.js")
for needle in ("GetStocksList", "GetBuySale", "GetIndexStockWeights", "DownloadETFWeightExcel"):
    for m in re.finditer(rf".{{0,250}}{needle}.{{0,500}}", js):
        s = m.group(0)
        if "GetPromise" not in s:
            print(f"\n=== {needle} usage ===")
            print(s[:700])

# try GetStocksList with date params
for pl in (
    {"FundCode": "CN"},
    {"FundCode": "CN", "Date": "2026/06/09"},
    {"FundCode": "CN", "date": "2026/06/09"},
    {"FundCode": "CN", "PCFDate": "2026/06/09"},
    {"FundCode": "CN", "TradeDate": "2026/06/09"},
    {"FundCode": "CN", "Lang": "tw"},
    {"fundCode": "CN", "date": "2026/06/09"},
):
    try:
        body = get("BuySale/GetStocksList", pl)
        j = json.loads(body)
        n = len(j.get("result") or [])
        print(f"GetStocksList {pl} -> n={n} success={j.get('success')}")
        if n:
            print(json.dumps(j, ensure_ascii=False)[:2000])
    except Exception as e:
        print(f"ERR {pl}: {e}")

for pl in (
    {"FundCode": "CN"},
    {"FundCode": "00878"},
    {"ETFCode": "00878"},
    {"IndexCode": "ECN"},
):
    try:
        body = get("ETF/GetETFDetailStockList", pl)
        j = json.loads(body)
        res = j.get("result")
        print(f"GetETFDetailStockList {pl} -> {type(res)} {str(res)[:500]}")
    except Exception as e:
        print(f"ETFDetail ERR {pl}: {e}")

# Download excel URL pattern from js: apiUrl + api/ETF/DownloadETFWeightExcel + ObjToParam
for pl in (
    {"FundCode": "CN"},
    {"ETFCode": "00878"},
    {"FundCode": "00878"},
):
    try:
        body = get("ETF/DownloadETFWeightExcel", pl)
        print(f"Download {pl} len={len(body)} head={body[:20]!r}")
        if body[:2] == "PK" or body.startswith("0x"):
            open(rf"d:\ETF\output\cathay_weights_{pl.get('FundCode', pl.get('ETFCode'))}.xlsx", "wb").write(
                body.encode("latin1") if isinstance(body, str) else body
            )
    except Exception as e:
        print(f"Download ERR {pl}: {e}")

# raw bytes download
for q in ("FundCode=CN", "ETFCode=00878", "FundCode=00878"):
    url = f"{BASE}/ETF/DownloadETFWeightExcel?{q}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
            raw = resp.read()
            print(f"RAW {q} len={len(raw)} magic={raw[:4]!r}")
            if raw[:2] == b"PK":
                open(rf"d:\ETF\output\cathay_{q.replace('=','_')}.xlsx", "wb").write(raw)
    except Exception as e:
        print(f"RAW ERR {q}: {e}")

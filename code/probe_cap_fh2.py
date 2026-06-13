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

# find getNavPart callers
for m in re.finditer(r"getNavPart\([^)]{0,120}\)", cap):
    start = m.start()
    print(cap[max(0, start-400):start+200])
    print("---")

# search for buyback subscribe pattern
for m in re.finditer(r"buyback[^;]{0,400}", cap, re.I):
    s = m.group(0)
    if "subscribe" in s or "getBuyback" in s or ".stocks" in s:
        print("BUYBACK:", s[:500])
        print("---")

# Fuh Hwa POST ETFPcf
import datetime
today = datetime.date(2026, 6, 6)  # last trading day from summary
for fmt in ("20260606", "2026-06-06", "2026/06/06"):
    url = "https://www.fhtrust.com.tw/api/ETFPcf"
    req = urllib.request.Request(
        url,
        data=json.dumps({"fundID": "ETF21", "pcfDate": fmt}).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            body = resp.read().decode()
            j = json.loads(body)
            inner = (j.get("result") or [{}])[0]
            holdings = inner.get("result") or []
            print(f"FH ETFPcf {fmt} holdings={len(holdings)}")
            if holdings:
                print(holdings[:3])
                open(r"d:\ETF\output\fh_pcf.json", "w", encoding="utf-8").write(body)
    except Exception as e:
        print(f"FH ERR {fmt}: {e}")

# stockhold POST
for pl in ({"fundID": "ETF21"}, {"fundID": "00929"}):
    url = "https://www.fhtrust.com.tw/api/stockhold"
    req = urllib.request.Request(
        url,
        data=json.dumps(pl).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            body = resp.read().decode()
            j = json.loads(body)
            sh = ((j.get("result") or [{}])[0].get("stockHold") or {}).get("stockhold") or []
            print(f"stockhold POST {pl} n={len(sh)} sum={((j.get('result') or [{}])[0].get('stockHold') or {}).get('ratioSum')}")
            if sh:
                print(sh[:3])
    except Exception as e:
        print(f"stockhold ERR {pl}: {e}")

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


def post(url, payload=None):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload or {}).encode(),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.capitalfund.com.tw/etf/pcf/00919",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        return json.loads(resp.read())


for fid in ("195", "00919"):
    url = f"https://www.capitalfund.com.tw/CFWeb/api/etf/reviewTimes/{fid}"
    try:
        data = post(url)
        open(rf"d:\ETF\output\cap_review_{fid}.json", "w", encoding="utf-8").write(
            json.dumps(data, ensure_ascii=False, indent=2)
        )
        print(fid, "keys", list(data.keys()))
        if isinstance(data.get("data"), dict):
            print(" data keys", list(data["data"].keys())[:30])
        elif isinstance(data.get("data"), list) and data["data"]:
            print(" data[0] keys", list(data["data"][0].keys())[:30])
    except Exception as e:
        print(fid, "ERR", e)

# also CFWeb without prefix
for base in (
    "https://www.capitalfund.com.tw/CFWeb/api/etf/reviewTimes/195",
    "https://www.capitalfund.com.tw/api/etf/reviewTimes/195",
):
    try:
        data = post(base)
        print("base ok", base, str(data)[:300])
    except Exception as e:
        print("base err", base.split('/')[-2:], e)

#!/usr/bin/env python3
import json
import ssl
import urllib.request

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

BASE = "https://www.capitalfund.com.tw/CFWeb/api/etf/buyback"
REF = "https://www.capitalfund.com.tw/etf/pcf/00919"


def post(payload):
    req = urllib.request.Request(
        BASE,
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Referer": REF,
        },
        method="POST",
    )
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        return json.loads(resp.read())


payloads = [
    {"fundNo": "195"},
    {"fundNo": 195},
    {"stocNo": "00919"},
    {"stockNo": "00919"},
    {"itemNo": "00919"},
    {"code": "00919"},
    {"etfCode": "00919"},
    {"fundNo": "195", "date": "2026-06-09"},
    {"fundNo": "195", "pcfDate": "2026-06-09"},
    {"fundNo": "195", "tradeDate": "2026-06-09"},
    {},
]

for pl in payloads:
    try:
        data = post(pl)
        keys = list(data.keys())
        d = data.get("data")
        print("===", pl, "code", data.get("code"), "keys", keys)
        if isinstance(d, dict):
            print(" data keys:", list(d.keys())[:40])
            if "stocks" in d:
                stocks = d["stocks"]
                print(" stocks len", len(stocks), "sample", stocks[:2])
            if "pcf" in d:
                print(" pcf keys", list(d["pcf"].keys()) if isinstance(d["pcf"], dict) else d["pcf"])
        elif isinstance(d, list) and d:
            print(" data[0] keys", list(d[0].keys())[:40])
    except Exception as e:
        print("ERR", pl, e)

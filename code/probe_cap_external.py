#!/usr/bin/env python3
import json
import ssl
import urllib.request

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

BASES = (
    "http://125.227.3.107/CapitalFundAPI",
    "http://125.227.3.107/CapitalFundEcAPI",
    "https://www.capitalfund.com.tw/CFWeb",
)

paths = [
    "/api/etf/buyback",
    "/api/etf/pcf",
    "/api/etf/navPart",
    "/api/etf/items",
]

payloads = [
    {"fundNo": "195"},
    {"stocNo": "00919"},
    {"fundNo": "195", "stocNo": "00919"},
]

for base in BASES:
    for path in paths:
        url = base + path
        for pl in payloads:
            req = urllib.request.Request(
                url,
                data=json.dumps(pl).encode(),
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0",
                    "Referer": "https://www.capitalfund.com.tw/etf/pcf/00919",
                },
                method="POST",
            )
            try:
                with urllib.request.urlopen(req, context=CTX, timeout=15) as resp:
                    body = resp.read().decode("utf-8", "replace")
                    if len(body) > 100 and "stocks" in body.lower():
                        print("HIT", url, pl, body[:2000])
                    elif len(body) > 100 and body.lstrip().startswith("{"):
                        print("OK", url.split("/")[-1], pl, body[:300])
            except Exception as e:
                err = str(e)
                if "404" not in err and "timed out" not in err:
                    print("ERR", base.split("/")[-1], path.split("/")[-1], pl, err[:60])

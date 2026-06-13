#!/usr/bin/env python3
import json
import ssl
import urllib.request

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

bases = (
    "https://www.capitalfund.com.tw/CapitalFundAPI",
    "https://www.capitalfund.com.tw/CapitalFundEcAPI",
    "https://www.capitalfund.com.tw/CFWeb",
)

paths = [
    "/api/etf/buyback",
    "/api/etf/pcf",
    "/api/etf/navPart",
    "/api/Etf/Pcf",
    "/api/etf/portfolio",
]

payloads = [
    {"fundNo": "195"},
    {"stocNo": "00919"},
    {"fundNo": "195", "stocNo": "00919"},
    {"FundNo": "195"},
]

for base in bases:
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
                    if len(body) > 100:
                        print("OK", url, pl, body[:500])
                        if "stocks" in body or "stocNo" in body:
                            open(r"d:\ETF\output\cap_pcf_hit.json", "w", encoding="utf-8").write(body)
            except Exception as e:
                err = str(e)
                if "404" not in err and "500" not in err and "405" not in err:
                    print("ERR", url.split(".tw")[-1], pl, err[:70])

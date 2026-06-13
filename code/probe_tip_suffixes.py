#!/usr/bin/env python3
import json
import ssl
import urllib.request

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
BASE = "https://backend.taiwanindex.com.tw/api/indexes"

suffixes = [
    "constituent_weights",
    "constituents/weights",
    "constituents_weight",
    "weight_records",
    "constituents",
    "components",
    "portfolio_weights",
    "latest_constituent_weights",
    "constituent_weight_records",
]

for code in ("IX0170", "IX0179"):
    for suf in suffixes:
        url = f"{BASE}/{code}/{suf}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, context=CTX, timeout=12) as resp:
                body = resp.read().decode("utf-8", "replace")
                if len(body) > 100:
                    print("OK", suf, code, len(body), body[:350].replace("\n", " "))
                    if "weight" in body.lower() or "stock" in body.lower():
                        open(rf"d:\ETF\output\tip_{code}_{suf}.json", "w", encoding="utf-8").write(body)
        except Exception as e:
            err = str(e)
            if "404" not in err and "500" not in err:
                print("ERR", code, suf, err[:50])

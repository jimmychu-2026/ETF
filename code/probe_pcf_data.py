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


# Find 00878 fundCode from fee list
body = get("BuySale/GetBuySaleFeeList", {"FundCode": "00878"})
data = json.loads(body)
for row in data.get("result") or []:
    if "00878" in str(row.get("stockCode", "")) or "00878" in str(row.get("name", "")):
        print("FOUND 00878:", row)
        fc = row.get("fundCode")
        break
else:
    # search all
    body2 = get("BuySale/GetBuySaleFeeList", {})
    data2 = json.loads(body2)
    for row in data2.get("result") or []:
        if row.get("stockCode") == "00878":
            print("FOUND:", row)
            fc = row.get("fundCode")
            break
    else:
        fc = None
        print("00878 not in fee list, searching ETF code list...")
        etf_codes = get("ETF/GetETFCode", {})
        open(r"d:\ETF\output\cathay_etf_codes.json", "w", encoding="utf-8").write(etf_codes)
        for row in json.loads(etf_codes).get("result") or []:
            if "00878" in json.dumps(row, ensure_ascii=False):
                print("ETF code row:", row)
                fc = row.get("fundCode") or row.get("FundCode")

print("fundCode for 00878:", fc)

if fc:
    for path in ("BuySale/GetBuySale", "BuySale/GetStocksList", "BuySale/GetLastPCFForeignCurr"):
        for pl in (
            {"FundCode": fc},
            {"fundCode": fc},
            {"ETFCode": "00878"},
            {"FundCode": "00878", "fundCode": fc},
        ):
            try:
                body = get(path, pl)
                j = json.loads(body)
                if j.get("success") or j.get("result"):
                    print(f"\nOK {path} {pl}")
                    print(json.dumps(j, ensure_ascii=False)[:3000])
                    open(
                        rf"d:\ETF\output\cathay_{path.split('/')[-1]}_{fc}.json",
                        "w",
                        encoding="utf-8",
                    ).write(json.dumps(j, ensure_ascii=False, indent=2))
            except Exception as e:
                print(f"ERR {path} {pl}: {e}")

# Capital navPart
print("\n=== Capital navPart ===")
for pl in (
    {"fundNo": "195"},
    {"stocNo": "00919"},
    {"fundNo": "195", "date": "2026-06-09"},
    {"fundNo": "195", "pcfDate": "2026/06/09"},
    {"fundNo": "195", "tradeDate": "2026-06-09"},
    {"itemNo": "00919"},
):
    url = "https://www.capitalfund.com.tw/CFWeb/api/etf/navPart"
    req = urllib.request.Request(
        url,
        data=json.dumps(pl).encode(),
        headers={
            "Content-Type": "application/json",
            "Referer": "https://www.capitalfund.com.tw/etf/pcf/00919",
            "User-Agent": "Mozilla/5.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            body = resp.read().decode()
            if len(body) > 100:
                print(f"navPart {pl}: {body[:2000]}")
    except Exception as e:
        print(f"navPart ERR {pl}: {e}")

# Fuh Hwa GetBuySale style - try assets endpoint
print("\n=== Fuh Hwa assets ===")
for q in ("fundID=ETF21", "fundID=00929"):
    try:
        body = fetch_url(f"https://www.fhtrust.com.tw/api/assets?{q}")
        print(q, body[:1500])
    except Exception as e:
        print(q, e)

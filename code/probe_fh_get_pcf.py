#!/usr/bin/env python3
import json
import datetime
import ssl
import urllib.request

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

import sys
sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

# Fuh Hwa getETFPcf uses query string param
for delta in range(0, 30):
    d = datetime.date.today() - datetime.timedelta(days=delta)
    for fmt in (d.strftime("%Y%m%d"), d.strftime("%Y/%m/%d")):
        url = f"https://www.fhtrust.com.tw/api/ETFPcf?fundID=ETF21&pcfDate={fmt}"
        try:
            body = fetch_url(url)
            j = json.loads(body)
            inner = (j.get("result") or [{}])
            if not inner:
                continue
            r0 = inner[0] if isinstance(inner[0], dict) else {}
            holdings = r0.get("result") or []
            if holdings:
                print(f"OK {fmt} n={len(holdings)} sample={holdings[:2]}")
                open(r"d:\ETF\output\fh_etfpcf.json", "w", encoding="utf-8").write(body)
                raise SystemExit(0)
        except SystemExit:
            raise
        except Exception:
            pass
print("No FH holdings in 30 days")

# Capital buyback - try form-encoded and various field names from minified export
BASE = "https://www.capitalfund.com.tw/CFWeb/api/etf/buyback"
payloads = [
    {"fundNo": "195", "stocNo": "00919"},
    {"FundNo": "195"},
    {"FundNo": 195},
    {"StocNo": "00919"},
    {"ItemNo": "00919"},
    {"fundNo": "195", "lang": "tw"},
]
for pl in payloads:
    req = urllib.request.Request(
        BASE,
        data=json.dumps(pl).encode(),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Referer": "https://www.capitalfund.com.tw/etf/pcf/00919",
            "Origin": "https://www.capitalfund.com.tw",
            "User-Agent": "Mozilla/5.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            body = resp.read().decode()
            print(f"buyback {pl}: {body[:1500]}")
            if "stocks" in body:
                open(r"d:\ETF\output\cap_buyback.json", "w", encoding="utf-8").write(body)
    except Exception as e:
        print(f"buyback ERR {pl}: {e}")

# Cathay GetIndexStockWeights FundCode CN
for q in ("FundCode=CN", "FundCode=00878", "IndexCode=ECN", "ETFCode=00878"):
    url = f"https://cwapi.cathaysite.com.tw/api/ETF/GetIndexStockWeights?{q}"
    try:
        body = fetch_url(url)
        j = json.loads(body)
        sw = (j.get("result") or {}).get("stockWeights") or []
        print(f"IndexWeights {q} n={len(sw)} success={j.get('success')}")
        if sw:
            print(sw[:3])
            open(r"d:\ETF\output\cathay_index_weights.json", "w", encoding="utf-8").write(body)
    except Exception as e:
        print(f"IW ERR {q}: {e}")

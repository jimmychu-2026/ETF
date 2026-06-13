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


def fetch_scripts_from_page(url: str) -> list[str]:
    html = fetch_url(url)
    scripts = re.findall(r'src="([^"]+\.js)"', html)
    out = []
    for s in scripts:
        if s.startswith("/"):
            s = "https://www.capitalfund.com.tw" + s
        elif not s.startswith("http"):
            s = "https://www.capitalfund.com.tw/" + s.lstrip("/")
        try:
            out.append(fetch_url(s))
        except Exception:
            pass
    return out


# Capital PCF page chunks
print("=== Capital PCF page scripts ===")
for js in fetch_scripts_from_page("https://www.capitalfund.com.tw/etf/pcf/00919"):
    if "getBuyback" in js or "buyback" in js.lower():
        for m in re.finditer(r".{0,120}buyback.{0,200}", js, re.I):
            s = m.group(0)
            if "export" not in s.lower() or "getBuyback" in s:
                print("HIT:", s[:350])

# Cathay PCF page
print("\n=== Cathay PCF page scripts ===")
html = fetch_url("https://www.cathaysite.com.tw/ETF/trade/pcf/00878")
scripts = re.findall(r'src="([^"]+\.js)"', html)
print("scripts", scripts[:10])
for s in scripts:
    if s.startswith("/"):
        s = "https://www.cathaysite.com.tw" + s
    try:
        js = fetch_url(s)
        if "IndexStockWeights" in js or "GetIndexStockWeights" in js:
            for m in re.finditer(r".{0,150}IndexStockWeights.{0,300}", js):
                print("CY:", m.group(0)[:450])
    except Exception as e:
        print("err", s, e)

# Cathay - find PostPromise / GetPromise method body in main js
js = fetch_url("https://www.cathaysite.com.tw/main.1047ac4f81a3da4e7643.js")
for pat in (r"PostPromise\s*\([^)]*\)\s*\{[^}]{0,800}\}", r"GetPromise\s*\([^)]*\)\s*\{[^}]{0,800}\}"):
    m = re.search(pat, js)
    if m:
        print("\nPromise method:", m.group(0)[:800])

# try cathay with query string style (GetPromise likely uses GET with query params)
BASE = "https://www.cathaysite.com.tw/api/ETF/GetIndexStockWeights"
for q in (
    "ETFCode=00878",
    "FundCode=00878",
    "Code=00878",
    "etfCode=00878",
    "Symbol=00878",
    "StockCode=00878",
    "ETFNo=00878",
    "FundNo=ECN",
    "IndexCode=ECN",
    "ETFCode=ECN",
    "FundCode=ECN",
):
    try:
        body = fetch_url(f"{BASE}?{q}")
        if len(body) > 80 and not body.lstrip().startswith("<!"):
            print(f"CY GET ?{q} -> {body[:500]}")
    except Exception as e:
        pass

# Old capital API
for url in (
    "http://125.227.3.107/CapitalFundAPI/api/etf/pcf?fundId=00919",
    "http://125.227.3.107/CapitalFundAPI/api/etf/pcf?fundNo=195",
    "http://125.227.3.107/CapitalFundAPI/api/etf/buyback",
):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=CTX, timeout=15) as resp:
            body = resp.read().decode("utf-8", "replace")
            print(f"OLD {url}: {body[:400]}")
    except Exception as e:
        print(f"OLD ERR {url}: {e}")

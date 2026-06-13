#!/usr/bin/env python3
import json
import sys

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

for ep in ("assets", "EI_PortfolioData", "frontdetail", "ETFindex"):
    url = f"https://www.fhtrust.com.tw/api/{ep}?fundID=ETF21"
    try:
        body = fetch_url(url)
        j = json.loads(body)
        blob = json.dumps(j, ensure_ascii=False)
        print(ep, "len", len(blob))
        if isinstance(j.get("result"), list) and j["result"]:
            r0 = j["result"][0]
            if isinstance(r0, dict):
                for k, v in r0.items():
                    if isinstance(v, list):
                        print(" ", k, "list len", len(v))
                    elif isinstance(v, dict):
                        print(" ", k, "dict keys", list(v.keys())[:8])
        if "stockhold" in blob.lower():
            print("  contains stockhold")
    except Exception as e:
        print(ep, "ERR", str(e)[:60])

# MOPS style endpoints
mops_urls = [
    "https://mops.twse.com.tw/mops/api/json/t05sb08?encodeURIComponent=1&step=1&firstin=1&TYPEK=all&code=00929&keyword=",
    "https://mops.twse.com.tw/mops/api/json/t05st43?encodeURIComponent=1&step=1&firstin=1&TYPEK=all&code=00929",
    "https://mops.twse.com.tw/mops/api/json/t05st43_ifrs?encodeURIComponent=1&step=1&firstin=1&TYPEK=otc&code=00929",
]
for url in mops_urls:
    try:
        body = fetch_url(url)
        print("MOPS", url.split("/")[-1][:30], body[:200])
    except Exception as e:
        print("MOPS ERR", str(e)[:60])

import json
import sys
import urllib.parse

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

base = "https://www.fhtrust.com.tw/api/ETFPcf"
params_list = [
    {"fundID": "00929", "pcfDate": "2026-06-06"},
    {"fundID": "00929", "pcfDate": "2026/06/06"},
    {"fundId": "00929", "pcfDate": "2026-06-06"},
    {"fundID": "00929"},
    {"fundId": "00929"},
]
for p in params_list:
    url = base + "?" + urllib.parse.urlencode(p)
    try:
        body = fetch_url(url)
        print("OK", p, body[:300])
    except Exception as e:
        err = str(e)
        print("ERR", p, err[:80])

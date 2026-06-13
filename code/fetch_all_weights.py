#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url
from parse_taiwanindex_nuxt import parse_taiwanindex_constituents, hhi_from_rows

OUT = Path(r"d:\ETF\output")

for code in ("IX0170", "IX0179"):
    url = f"https://www.taiwanindex.com.tw/indexes/{code}"
    html = fetch_url(url)
    path = OUT / f"idx_{code}.html"
    path.write_text(html, encoding="utf-8")
    rows = parse_taiwanindex_constituents(html)
    stats = hhi_from_rows(rows)
    print(code, "rows", len(rows), stats)
    if rows:
        print(" top3", rows[:3])

# Cathay 00878
import json
import ssl
import urllib.parse
import urllib.request

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

url = "https://cwapi.cathaysite.com.tw/api/ETF/GetIndexStockWeights?FundCode=CN"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
    j = json.loads(resp.read())
sw = j["result"]["stockWeights"]
rows = [(r["stockCode"], float(r["weights"]), r.get("stockName", r["stockCode"])) for r in sw]
stats = hhi_from_rows(rows)
print("00878 CN", "rows", len(rows), stats)
OUT.joinpath("cathay_00878_weights.json").write_text(
    json.dumps(j, ensure_ascii=False, indent=2), encoding="utf-8"
)

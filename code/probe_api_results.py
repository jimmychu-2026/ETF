#!/usr/bin/env python3
import json
import sys

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

tests = [
    ("cap_detail_195", "https://www.capitalfund.com.tw/CFWeb/api/etf/detail/195"),
    ("cap_basic_195", "https://www.capitalfund.com.tw/CFWeb/api/etf/basic/195"),
    ("cap_delivery_195", "https://www.capitalfund.com.tw/CFWeb/api/etf/delivery?fundNo=195"),
    ("cap_items", "https://www.capitalfund.com.tw/CFWeb/api/etf/items"),
    ("fh_pcf", "https://www.fhtrust.com.tw/ETF/ETFPcf?fundID=ETF21&pcfDate=20260608"),
    ("fh_stockhold", "https://www.fhtrust.com.tw/ETF/stockhold?fundID=ETF21"),
]

out = []
for name, url in tests:
    try:
        raw = fetch_url(url)
        try:
            data = json.loads(raw)
            out.append(f"=== {name} ===\n{json.dumps(data, ensure_ascii=False, indent=2)[:8000]}")
        except json.JSONDecodeError:
            out.append(f"=== {name} (not json) ===\n{raw[:2000]}")
    except Exception as e:
        out.append(f"=== {name} ERROR ===\n{e}")

with open(r"d:\ETF\output\probe_api_results.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(out))
print("written", len(out))

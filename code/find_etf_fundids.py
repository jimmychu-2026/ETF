import json
import sys

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

targets = {"0050", "0056", "006208", "00878", "00919", "00929"}
data = json.loads(fetch_url("https://www.fhtrust.com.tw/api/FundList?ec001=3"))
for item in data.get("result", []):
    code = str(item.get("etf002", ""))
    if code in targets:
        print(code, item.get("fundID"), item.get("etf005"), item.get("twNameFull", "")[:30])

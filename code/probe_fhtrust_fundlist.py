import json
import sys

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

data = json.loads(fetch_url("https://www.fhtrust.com.tw/api/FundList?ec001=3"))
for item in data.get("result", []):
    fid = str(item.get("fundID", ""))
    name = item.get("twNameFull", "")
    if "00929" in fid or "00929" in name or "科技優息" in name:
        print(item)

#!/usr/bin/env python3
import re
import sys

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

cap = fetch_url("https://www.capitalfund.com.tw/main.bdc1e85b555aa797.js")

for pat in (r"getBuyback\(", r"\.buyback\(", r"stocks\s*=", r"stocNo", r"weightRound", r"pcfDate", r"fundNo"):
    matches = list(re.finditer(pat, cap))
    print(f"\n=== {pat} count {len(matches)} ===")
    for m in matches[:8]:
        print(cap[max(0, m.start()-150):m.start()+350][:500])

# search for pcf route component
i = cap.find("pcf/00919")
print("\npcf route hits", cap.count("/etf/pcf"))
for m in re.finditer(r"/etf/pcf[^\"']{0,40}", cap):
    print(m.group(0))

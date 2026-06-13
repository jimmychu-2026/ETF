#!/usr/bin/env python3
import re
import sys

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

html = fetch_url("https://www.capitalfund.com.tw/etf/pcf/00919")
scripts = re.findall(r'src="([^"]+\.js)"', html)
print("scripts", len(scripts))
for s in scripts:
    print(s)

# runtime chunk map
for name in scripts:
    if "runtime" in name or "main" in name:
        url = name if name.startswith("http") else "https://www.capitalfund.com.tw/" + name.lstrip("/")
        js = fetch_url(url)
        chunks = re.findall(r'"(\d+)":"([^"]+\.js)"', js)
        if chunks:
            print(f"\nchunks from {name}:", len(chunks))
            for cid, fname in chunks[:30]:
                print(cid, fname)

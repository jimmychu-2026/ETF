#!/usr/bin/env python3
import re
from pathlib import Path

html = Path(r"d:\ETF\output\idx_IX0170.html").read_text(encoding="utf-8")
start = html.find("window.__NUXT__=")
blob = html[start : start + 2000000]

patterns = [
    r'stock_id:"(\d{4,5})"',
    r'stock_code:"(\d{4,5})"',
    r'code:"(\d{4,5})"',
    r'weights?:([0-9.]+)',
    r'weight:([0-9.]+)',
    r'weight_per:([0-9.]+)',
    r'constituent',
    r'component',
]
for pat in patterns:
    hits = re.findall(pat, blob)
    print(pat, "count", len(hits), "sample", hits[:5])

# look for 4-digit codes near weight numbers
pairs = re.findall(r'(\d{4})[^0-9]{1,80}?([0-9]+\.[0-9]+)', blob[:500000])
print("pairs sample", pairs[:10])

# search backend API from nuxt
apis = sorted(set(re.findall(r"backend\.taiwanindex\.com\.tw[^\"']+", blob)))
print("apis", apis[:20])
for a in sorted(set(re.findall(r"/api/[A-Za-z/{}$]+", blob)))[:30]:
    print("api path", a)

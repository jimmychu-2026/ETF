#!/usr/bin/env python3
import re
import sys

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

js = fetch_url("https://www.cathaysite.com.tw/main.1047ac4f81a3da4e7643.js")

for needle in ("baseUrl", "BaseUrl", "apiUrl", "API_URL", "environment", "cathaysite", "PostPromise", "GetPromise"):
    idx = 0
    n = 0
    while n < 5:
        i = js.find(needle, idx)
        if i < 0:
            break
        print(f"\n--- {needle} ---")
        print(js[max(0, i - 80) : i + 400])
        idx = i + len(needle)
        n += 1

# find PostPromise function body
m = re.search(r"PostPromise\([a-zA-Z,\s=!.]+\)\{.{0,1500}?\}", js)
if m:
    print("\nPostPromise:", m.group(0)[:1500])

# URLs containing api
urls = sorted(set(re.findall(r"https?://[a-zA-Z0-9._/-]+api[a-zA-Z0-9._/-]*", js)))
for u in urls[:30]:
    print("URL", u)

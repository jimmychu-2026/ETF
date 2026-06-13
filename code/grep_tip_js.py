#!/usr/bin/env python3
import re
import sys

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

html = fetch_url("https://www.taiwanindex.com.tw/indexes/IX0170")
scripts = re.findall(r'src="(/_nuxt/[^"]+\.js)"', html)
print("scripts", len(scripts))
for s in scripts[:15]:
    url = "https://www.taiwanindex.com.tw" + s
    try:
        js = fetch_url(url)
        if "constituent" in js.lower() or "weight" in js.lower():
            apis = sorted(set(re.findall(r"/api/[A-Za-z/{}/$._-]+", js)))
            for a in apis:
                if any(x in a.lower() for x in ("constitu", "weight", "index", "stock")):
                    print(s.split("/")[-1], a)
            for m in re.finditer(r".{0,80}constituent.{0,150}", js, re.I):
                print("CTX:", m.group(0)[:220])
    except Exception as e:
        print("err", s, e)

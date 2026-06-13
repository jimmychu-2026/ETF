#!/usr/bin/env python3
"""Download Taiwan Index files and probe pocket.tw ETF API."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

OUT = Path(r"d:\ETF\output\tip_downloads")
OUT.mkdir(parents=True, exist_ok=True)

# From index page download links (IX0179 -> 634)
INDEX_FILES = {
    "IX0179": 634,  # 00929
    "IX0208": 754,  # from idx_IX0208.html grep earlier
}

for code, fid in INDEX_FILES.items():
    url = f"https://backend.taiwanindex.com.tw/api/downloadFile/IndexFiles/{fid}/tw"
    data = fetch_url(url).encode("latin1", "replace")  # binary-safe
    path = OUT / f"{code}_{fid}.bin"
    path.write_bytes(data if isinstance(data, bytes) else data.encode("latin1"))
    print(code, "saved", path, "size", path.stat().st_size, "head", path.read_bytes()[:8])

# pocket.tw - fetch page and look for __NEXT_DATA__ or API
for ticker in ("00878", "00919", "00929"):
    html = fetch_url(f"https://www.pocket.tw/etf/tw/{ticker}")
    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.+?)</script>', html)
    if m:
        j = json.loads(m.group(1))
        out = OUT / f"pocket_{ticker}.json"
        out.write_text(json.dumps(j, ensure_ascii=False, indent=2), encoding="utf-8")
        print(ticker, "NEXT_DATA saved", out)
        # dig for holdings
        blob = json.dumps(j, ensure_ascii=False)
        if "weight" in blob.lower() or "constitu" in blob.lower():
            print("  has weight/constituent keys")
    else:
        print(ticker, "no NEXT_DATA", len(html))
        apis = re.findall(r"https?://[^\"']+api[^\"']+", html)
        print("  apis", apis[:5])

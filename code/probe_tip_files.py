#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

for fid in (786, 797, 634, 754):
    url = f"https://backend.taiwanindex.com.tw/api/downloadFile/IndexFiles/{fid}/tw"
    req_raw = __import__("urllib.request").request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    import ssl
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with __import__("urllib.request").request.urlopen(req_raw, context=ctx, timeout=30) as resp:
        data = resp.read()
    path = Path(rf"d:\ETF\output\tip_downloads\file_{fid}.bin")
    path.write_bytes(data)
    print(fid, "size", len(data), "head", data[:20])

import json
import sys

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

indices = ["IX0179", "IX0205", "IX0208", "TWDIV", "TW50"]
paths = [
    "api/Index/{idx}/Constituents",
    "api/IndexConstituents/{idx}",
    "api/Index/{idx}/Portfolio",
    "api/IndexPortfolio/{idx}",
    "api/IndexWeight/{idx}",
    "api/Index/{idx}/Weight",
    "api/IndexData/{idx}",
]
for idx in indices:
    for p in paths:
        url = f"https://backend.taiwanindex.com.tw/{p.format(idx=idx)}"
        try:
            body = fetch_url(url)
            if body.strip().startswith("{") or body.strip().startswith("["):
                print("JSON", url, body[:200])
            elif len(body) < 500:
                print("SHORT", url, body[:100])
        except Exception:
            pass

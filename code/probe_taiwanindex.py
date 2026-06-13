import json
import sys

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

candidates = [
    "https://backend.taiwanindex.com.tw/api/IndexConstituent/IX0179",
    "https://backend.taiwanindex.com.tw/api/IndexConstituents/IX0179",
    "https://backend.taiwanindex.com.tw/api/IndexPortfolio/IX0179",
    "https://backend.taiwanindex.com.tw/api/IndexWeight/IX0179",
    "https://backend.taiwanindex.com.tw/api/Index/IX0179/constituents",
    "https://backend.taiwanindex.com.tw/api/downloadFile/IndexFiles/634/tw",
    "https://backend.taiwanindex.com.tw/api/downloadFile/IndexConstituent/IX0179/tw",
]
for url in candidates:
    try:
        body = fetch_url(url)
        print("OK", url.split("/")[-3:], "len", len(body), body[:150].replace("\n", " "))
    except Exception as e:
        print("ERR", url, str(e)[:70])

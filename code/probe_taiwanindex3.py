import sys

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

urls = [
    "https://backend.taiwanindex.com.tw/api/Home/IndexConstituent?indexCode=IX0179",
    "https://backend.taiwanindex.com.tw/api/Home/IndexConstituent?indexId=IX0179",
    "https://backend.taiwanindex.com.tw/api/IndexConstituent/IX0179",
    "https://backend.taiwanindex.com.tw/api/IndexConstituent?indexCode=IX0179",
    "https://www.taiwanindex.com.tw/Handler/IndexConstituent.ashx?indexNo=IX0179",
    "https://www.taiwanindex.com.tw/api/IndexConstituent/IX0179",
    "https://backend.taiwanindex.com.tw/api/Index/IX0179/ConstituentWeight",
]
for url in urls:
    try:
        body = fetch_url(url)
        print("OK", url.split("/")[-1][:50], len(body), body[:150].replace("\n", " "))
    except Exception as e:
        print("ERR", url.split("/")[-1][:50], str(e)[:60])

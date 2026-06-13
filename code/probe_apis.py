import re
import sys

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

candidates = [
    "https://www.fhtrust.com.tw/api/ETFPcf?fundID=00929&pcfDate=2026-06-06",
    "https://www.fhtrust.com.tw/api/etfpcf?fundID=00929&pcfDate=2026-06-06",
    "https://www.fhtrust.com.tw/Api/ETFPcf?fundID=00929&pcfDate=2026-06-06",
    "https://www.fhtrust.com.tw/api/Fund/ETFPcf?fundID=00929&pcfDate=2026-06-06",
    "https://www.cathaysite.com.tw/api/ETF/Pcf/00878",
    "https://www.cathaysite.com.tw/ETF/api/Pcf?fundId=00878",
    "https://www.capitalfund.com.tw/api/Pcf?fundId=00919",
    "https://capitalfund.tw/api/Pcf?fundId=00919",
]

for url in candidates:
    try:
        body = fetch_url(url)
        print("OK", url, len(body), body[:120].replace("\n", " "))
    except Exception as e:
        print("ERR", url.split("?")[0], str(e)[:60])

html = fetch_url("https://www.fhtrust.com.tw/ETF/trade_list")
scripts = re.findall(r'src="([^"]+\.js)"', html)
print("scripts", scripts)

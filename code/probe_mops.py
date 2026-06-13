import sys

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

urls = [
    "https://mops.twse.com.tw/mops/web/ajax_t51sb02?step=1&firstin=1&TYPEK=sii&code=00878",
    "https://mops.twse.com.tw/mops/web/t51sb02?step=1&TYPEK=sii&code=00878",
    "https://mops.twse.com.tw/mops/web/ajax_t05st43_ifrs?step=1&firstin=1&TYPEK=sii&code=00878",
]
for url in urls:
    try:
        body = fetch_url(url)
        print("OK", url[-40:], len(body), "持股" in body, "比例" in body)
        if "持股" in body or "比例" in body:
            open(r"d:\ETF\output\mops_00878.html", "w", encoding="utf-8").write(body)
    except Exception as e:
        print("ERR", str(e)[:70])

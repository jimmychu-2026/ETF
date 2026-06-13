#!/usr/bin/env python3
import json
import ssl
import urllib.parse
import urllib.request

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

BASE = "https://www.pocket.tw/api/cm/MobileService/ashx/GetDtnoData.ashx"


def fetch_holdings(ticker: str):
    param = (
        f"AssignID={ticker};MTPeriod=0;DTMode=0;DTRange=159;DTOrder=1;MajorTable=M061;"
    )
    q = urllib.parse.urlencode(
        {
            "action": "getdtnodata",
            "DtNo": "50828186",
            "ParamStr": param,
            "FilterNo": "0",
        }
    )
    url = f"{BASE}?{q}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Referer": f"https://www.pocket.tw/etf/tw/{ticker}"})
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        return json.loads(resp.read())


for ticker in ("00919", "00929", "00878"):
    try:
        data = fetch_holdings(ticker)
        open(rf"d:\ETF\output\pocket_holdings_{ticker}.json", "w", encoding="utf-8").write(
            json.dumps(data, ensure_ascii=False, indent=2)
        )
        rows = data.get("Data") or []
        print(ticker, "rows", len(rows))
        if rows:
            print(" sample keys", list(rows[0].keys())[:15])
            print(" first row", rows[0])
    except Exception as e:
        print(ticker, "ERR", e)

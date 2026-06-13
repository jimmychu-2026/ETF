#!/usr/bin/env python3
import json
import ssl
import urllib.parse
import urllib.request

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

BASE = "https://www.pocket.tw/api/cm/MobileService/ashx/GetDtnoData.ashx"


def get(dtn, param, ticker="00919"):
    q = urllib.parse.urlencode(
        {"action": "getdtnodata", "DtNo": dtn, "ParamStr": param, "FilterNo": "0"}
    )
    url = f"{BASE}?{q}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0", "Referer": f"https://www.pocket.tw/etf/tw/{ticker}"},
    )
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        return json.loads(resp.read())


tests = [
    ("60465380", "AssignID=00919;DTRange=1", "00919"),
    ("60465380", "AssignID=00929;DTRange=1", "00929"),
    ("61324146", "AssignID=0;DTRange=1500;", "00919"),
    ("50669373", "AssignID=00919;MTPeriod=0;DTMode=0;DTRange=1;DTOrder=1;MajorTable=M002;", "00919"),
    ("50669373", "AssignID=00919;MTPeriod=0;DTMode=0;DTRange=1;DTOrder=1;MajorTable=M003;", "00919"),
    ("50669373", "AssignID=00919;MTPeriod=0;DTMode=0;DTRange=1;DTOrder=1;MajorTable=M004;", "00919"),
    ("50669373", "AssignID=00919;MTPeriod=0;DTMode=0;DTRange=60;DTOrder=1;MajorTable=M005;", "00919"),
]

for dtn, param, ticker in tests:
    try:
        data = get(dtn, param, ticker)
        title = data.get("Title")
        rows = data.get("Data") or []
        print(f"\n=== DtNo={dtn} ticker={ticker} ===")
        print("Title:", title)
        print("n_rows:", len(rows), "sample:", rows[:3])
        if title and any("權" in str(t) or "股" in str(t) or "成分" in str(t) for t in title):
            open(rf"d:\ETF\output\pocket_{ticker}_{dtn}.json", "w", encoding="utf-8").write(
                json.dumps(data, ensure_ascii=False, indent=2)
            )
    except Exception as e:
        print("ERR", dtn, e)

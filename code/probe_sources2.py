#!/usr/bin/env python3
import json
import re
import ssl
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def probe_tip_constituents() -> None:
    print("=== TIP constituent SSR pages ===")
    for code in ("IX0179", "IX0205", "IX0209", "IX0210", "IX0208"):
        for path in (
            f"/indexes/{code}/constituents",
            f"/indexes/{code}/constituent",
        ):
            url = "https://www.taiwanindex.com.tw" + path
            try:
                html = fetch_url(url)
            except Exception:
                continue
            start = html.find("window.__NUXT__=")
            if start < 0:
                continue
            blob = html[start : start + 800000]
            rows = re.findall(
                r'stock_id:"(\d{4,5})"[^}]{0,400}?weight:([0-9.]+)', blob
            )
            if not rows:
                rows = re.findall(
                    r'code:"(\d{4,5})"[^}]{0,400}?weight_per:([0-9.]+)', blob
                )
            if rows:
                wsum = sum(float(w) for _, w in rows)
                print(code, path, "rows", len(rows), "wsum", wsum, "top", max(rows, key=lambda r: float(r[1])))


def probe_capital_main() -> None:
    print("\n=== Capital main.js API paths ===")
    js = fetch_url("https://www.capitalfund.com.tw/main.bdc1e85b555aa797.js")
    for m in sorted(set(re.findall(r"/api/[a-zA-Z0-9_/]+", js))):
        low = m.lower()
        if any(x in low for x in ("pcf", "hold", "item", "port", "weight", "stock", "constitu", "delivery")):
            print(m)


def post_capital(path: str, payload: dict) -> None:
    url = "https://www.capitalfund.com.tw" + path
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 ETF-HHI/1.0",
            "Origin": "https://www.capitalfund.com.tw",
            "Referer": "https://www.capitalfund.com.tw/etf/pcf/00919",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")


def probe_capital_post() -> None:
    print("\n=== Capital POST probes ===")
    tests = [
        ("/api/etf/items", {"etfCode": "00919"}),
        ("/api/etf/items", {"code": "00919"}),
        ("/api/etf/delivery", {"etfCode": "00919"}),
        ("/api/etf/index", {"etfCode": "00919"}),
        ("/api/etf/navPart", {"etfCode": "00919"}),
        ("/CFWeb/api/etf/nav", {"etfId": "00919"}),
    ]
    for path, payload in tests:
        try:
            body = post_capital(path, payload)
            if body.lstrip().startswith(("{", "[")):
                print("OK", path, payload, body[:250].replace("\n", " "))
        except Exception as e:
            print("ERR", path, str(e)[:70])


if __name__ == "__main__":
    probe_tip_constituents()
    probe_capital_main()
    probe_capital_post()

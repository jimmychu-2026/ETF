#!/usr/bin/env python3
import json
import re
import ssl
import urllib.request

import sys

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def post_json(url: str, payload: dict, referer: str = "") -> str:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 ETF-HHI/1.0",
    }
    if referer:
        headers["Referer"] = referer
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")


def probe_fhtrust_api_js() -> None:
    print("=== Fuh Hwa api.js ===")
    html = fetch_url("https://www.fhtrust.com.tw/ETF/trade_list")
    scripts = re.findall(r'src="([^"]+\.js)"', html)
    for s in scripts:
        if s.startswith("/"):
            s = "https://www.fhtrust.com.tw" + s
        try:
            js = fetch_url(s)
        except Exception:
            continue
        if "getETFPcf" in js or "ETFPcf" in js:
            print("file", s.split("/")[-1], "len", len(js))
            for m in re.findall(r'["\'](/api/[^"\']+)["\']', js):
                print(" ", m)
            idx = js.find("getETFPcf")
            print(js[max(0, idx - 200) : idx + 400])


def probe_cfweb() -> None:
    print("\n=== Capital CFWeb ===")
    base = "https://www.capitalfund.com.tw/CFWeb/api/etf"
    paths = [
        "holdings",
        "holding",
        "portfolio",
        "pcf",
        "constituent",
        "stock",
        "items",
        "delivery",
        "indexweight",
    ]
    payloads = [
        {"stocNo": "00919"},
        {"etfCode": "00919"},
        {"fundId": "195"},
        {"code": "00919"},
    ]
    for p in paths:
        for pl in payloads:
            url = f"{base}/{p}"
            try:
                body = post_json(url, pl, "https://www.capitalfund.com.tw/etf/pcf/00919")
                if body.lstrip().startswith(("{", "[")) and len(body) > 80:
                    print("OK", p, pl, body[:220].replace("\n", " "))
            except Exception as e:
                err = str(e)
                if "404" not in err and "405" not in err:
                    print("ERR", p, pl, err[:60])


def probe_cathay_detail() -> None:
    print("\n=== Cathay detail ECN ===")
    html = fetch_url("https://www.cathaysite.com.tw/ETF/detail/ECN")
    for pat in (
        r"holdings[^\"']{0,80}",
        r"etfDetailHoldings[^\"']{0,80}",
        r"/api/[^\"']+",
    ):
        hits = re.findall(pat, html, re.I)
        for h in hits[:15]:
            print(h[:120])
    # holdings sub-route
    for path in (
        "/ETF/detail/ECN/holdings",
        "/ETF/detail/00878/holdings",
        "/ETF/holdings/00878",
        "/ETF/holdings/ECN",
    ):
        try:
            body = fetch_url("https://www.cathaysite.com.tw" + path)
            if "weight" in body.lower() or "持股" in body:
                print("path", path, "hits", "weight" in body.lower())
                start = body.find("window.__NUXT__=")
                if start >= 0:
                    blob = body[start : start + 400000]
                    rows = re.findall(
                        r'code:"(\d{4,5})"[^}]{0,300}?weight:([0-9.]+)', blob
                    )
                    print(" rows", len(rows))
        except Exception as e:
            print("ERR", path, str(e)[:50])


if __name__ == "__main__":
    probe_fhtrust_api_js()
    probe_cfweb()
    probe_cathay_detail()

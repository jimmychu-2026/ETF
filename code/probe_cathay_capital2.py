#!/usr/bin/env python3
import json
import re
import ssl
import urllib.parse
import urllib.request

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

import sys
sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url


def post_form(url, data: dict, referer=""):
    body = urllib.parse.urlencode(data).encode()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json,text/plain,*/*",
        "User-Agent": "Mozilla/5.0",
    }
    if referer:
        headers["Referer"] = referer
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        return resp.read()


def post_json(url, payload, referer=""):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json,*/*",
        "User-Agent": "Mozilla/5.0",
    }
    if referer:
        headers["Referer"] = referer
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(), headers=headers, method="POST"
    )
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        return resp.read()


out = []

# Cathay GetIndexStockWeights
ref = "https://www.cathaysite.com.tw/ETF/trade/pcf/00878"
base = "https://www.cathaysite.com.tw/ETF"
for path in ("GetIndexStockWeights", "DownloadETFWeightExcel"):
    for method in ("GET", "POST"):
        for params in (
            {"etfCode": "00878"},
            {"fundCode": "00878"},
            {"code": "00878"},
            {"stockCode": "00878"},
            {"ETFCode": "00878"},
            {"symbol": "00878"},
            {"id": "00878"},
            {"etfId": "00878"},
            {"indexCode": "ECN"},
        ):
            url = f"{base}/{path}"
            try:
                if method == "GET":
                    q = urllib.parse.urlencode(params)
                    raw = fetch_url(f"{url}?{q}")
                else:
                    try:
                        raw = post_json(url, params, ref).decode("utf-8", "replace")
                    except Exception:
                        raw = post_form(url, params, ref).decode("utf-8", "replace")
                if len(raw) > 50:
                    head = raw[:300].replace("\n", " ")
                    if not raw.lstrip().startswith("<!DOCTYPE"):
                        out.append(f"CY {path} {method} {params} -> {head}")
                    elif "xlsx" in raw[:20].lower() or raw[:2] == "PK":
                        out.append(f"CY {path} {method} {params} -> binary len={len(raw)}")
            except Exception as e:
                err = str(e)
                if "404" not in err:
                    out.append(f"CY ERR {path} {method} {params} {err[:80]}")

# grep cathay js around GetIndexStockWeights
js = fetch_url("https://www.cathaysite.com.tw/main.1047ac4f81a3da4e7643.js")
for needle in ("GetIndexStockWeights", "DownloadETFWeightExcel", "IndexStockWeight"):
    i = js.find(needle)
    if i >= 0:
        out.append(f"JS ctx {needle}: {js[max(0,i-200):i+500]}")

# Capital - grep all .post(` patterns
cap = fetch_url("https://www.capitalfund.com.tw/main.bdc1e85b555aa797.js")
posts = sorted(set(re.findall(r"\.post\(`([^`]+)`", cap)))
gets = sorted(set(re.findall(r"\.get\(`([^`]+)`", cap)))
out.append("CAP posts: " + ", ".join(posts))
out.append("CAP gets: " + ", ".join(gets))

# try capital buyback endpoint (might have pcf)
for ep in posts + gets:
    if "pcf" in ep.lower() or "port" in ep.lower() or "hold" in ep.lower() or "stock" in ep.lower():
        url = "https://www.capitalfund.com.tw" + ep.replace("${y}", "195").replace("${C}", "195")
        if "${" in url:
            continue
        try:
            raw = post_json(url, {"fundNo": "195"}, "https://www.capitalfund.com.tw/etf/pcf/00919").decode()
            out.append(f"CAP try {ep} -> {raw[:400]}")
        except Exception as e:
            out.append(f"CAP try ERR {ep} {str(e)[:60]}")

open(r"d:\ETF\output\probe_cathay_capital2.txt", "w", encoding="utf-8").write("\n".join(out))
print("done", len(out))

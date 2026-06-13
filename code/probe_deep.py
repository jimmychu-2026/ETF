#!/usr/bin/env python3
import json
import re
import ssl
import urllib.request

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

import sys
sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url


def post_json(url: str, payload=None, referer: str = ""):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 ETF-HHI/1.0",
    }
    if referer:
        headers["Referer"] = referer
    data = json.dumps(payload or {}).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")


def probe_capital_pcf():
    base = "https://www.capitalfund.com.tw/CFWeb/api/etf"
    ref = "https://www.capitalfund.com.tw/etf/pcf/00919"
    paths = [
        "pcf", "portfolio", "holdings", "holding", "constituent", "indexweight",
        "reviewTimes", "navPart", "indexdetail", "benchmark", "interests",
    ]
    payloads = [
        {},
        {"fundNo": "195"},
        {"fundId": "195"},
        {"stocNo": "00919"},
        {"stockNo": "00919"},
        {"etfCode": "00919"},
        {"code": "00919"},
        {"fundNo": 195},
    ]
    out = []
    for p in paths:
        for pl in payloads:
            url = f"{base}/{p}" if "{" not in p else None
            if p == "reviewTimes":
                for fid in ("195", "00919"):
                    url = f"{base}/reviewTimes/{fid}"
                    try:
                        body = post_json(url, {}, ref)
                        if len(body) > 80:
                            out.append(f"OK {url} -> {body[:400]}")
                    except Exception as e:
                        pass
                continue
            if p in ("indexdetail", "benchmark", "basic", "detail"):
                for fid in ("195", "00919"):
                    url = f"{base}/{p}/{fid}"
                    try:
                        body = fetch_url(url)
                        if len(body) > 80:
                            out.append(f"GET {url} -> {body[:400]}")
                    except Exception:
                        pass
                continue
            try:
                body = post_json(f"{base}/{p}", pl, ref)
                if body.lstrip().startswith("{") and len(body) > 100:
                    low = body.lower()
                    if any(k in low for k in ("weight", "stock", "hold", "pcf", "nav", "constitu")):
                        out.append(f"OK POST {p} {pl} -> {body[:600]}")
            except Exception as e:
                err = str(e)
                if "404" not in err and "405" not in err:
                    out.append(f"ERR {p} {pl} {err[:80]}")

    # grep capital js for pcf-related strings
    cap = fetch_url("https://www.capitalfund.com.tw/main.bdc1e85b555aa797.js")
    for m in re.finditer(r'.{0,60}(?:pcf|PCF|portfolio|Portfolio|holdings|Holdings).{0,120}', cap):
        s = m.group(0)
        if "/api/" in s or "CFWeb" in s or ".pcf" in s or "exportEtf" in s:
            out.append("JS: " + s[:220])

    return out


def probe_fh():
    out = []
    # stockhold
    for q in ("fundID=ETF21", "fundID=00929", "etf002=00929"):
        try:
            body = fetch_url(f"https://www.fhtrust.com.tw/api/stockhold?{q}")
            out.append(f"stockhold {q}: {body[:800]}")
        except Exception as e:
            out.append(f"stockhold ERR {q}: {e}")

    # EI_PortfolioData
    for pl in (
        {"fundID": "ETF21"},
        {"fundId": "ETF21"},
        {"etf002": "00929"},
        {"fundID": "00929"},
    ):
        try:
            body = post_json("https://www.fhtrust.com.tw/api/EI_PortfolioData", pl)
            out.append(f"EI_PortfolioData {pl}: {body[:800]}")
        except Exception as e:
            out.append(f"EI_Portfolio ERR {pl}: {e}")

    # ETFPcf POST with various dates
    import datetime
    today = datetime.date.today()
    for delta in range(0, 10):
        d = today - datetime.timedelta(days=delta)
        for fmt in (d.strftime("%Y%m%d"), d.strftime("%Y-%m-%d"), d.strftime("%Y/%m/%d")):
            try:
                body = post_json("https://www.fhtrust.com.tw/api/ETFPcf", {"fundID": "ETF21", "pcfDate": fmt})
                j = json.loads(body)
                inner = (j.get("result") or [{}])
                if inner:
                    r0 = inner[0]
                    holdings = (r0.get("result") or []) if isinstance(r0, dict) else []
                    if holdings:
                        out.append(f"ETFPcf {fmt} holdings={len(holdings)} sample={holdings[:2]}")
                        return out
            except Exception:
                pass
    out.append("ETFPcf: no holdings in last 10 days")
    return out


def probe_cathay():
    out = []
    js = fetch_url("https://www.cathaysite.com.tw/main.1047ac4f81a3da4e7643.js")
    for pat in (
        r'https?://[^"\']+',
        r'/ETF/[^"\']+',
        r'/api/[^"\']+',
        r'get[A-Z][a-zA-Z]+\([^)]*\)',
    ):
        hits = set(re.findall(pat, js))
        for h in hits:
            hl = h.lower()
            if any(x in hl for x in ("pcf", "hold", "weight", "constitu", "portfolio", "trade")):
                if "facebook" not in hl and "holdings.com" not in hl:
                    out.append("CY hit: " + h[:150])

    # try common cathay backend patterns
    bases = [
        "https://www.cathaysite.com.tw",
        "https://api.cathaysite.com.tw",
        "https://www.cathaysite.com.tw/api",
    ]
    paths = [
        "/ETF/api/Pcf/00878",
        "/ETF/api/pcf/00878",
        "/api/ETF/Pcf/00878",
        "/api/etf/pcf/00878",
        "/api/ETF/Holdings/00878",
        "/api/ETF/holdings/00878",
        "/ETF/trade/pcfData/00878",
    ]
    for b in bases:
        for p in paths:
            url = b + p.replace("/ETF/api", "/api/ETF") if b.endswith("/api") else b + p
            try:
                body = fetch_url(url)
                if body.lstrip().startswith("{") and len(body) > 80:
                    out.append(f"CY OK {url}: {body[:400]}")
            except Exception:
                pass

    # search for http.post patterns in cathay js
    for m in re.finditer(r'\.post\(`([^`]+)`', js):
        out.append("CY post: " + m.group(1)[:120])
    for m in re.finditer(r'\.get\(`([^`]+)`', js):
        out.append("CY get: " + m.group(1)[:120])

    return out


if __name__ == "__main__":
    lines = []
    lines.append("=== CAPITAL ===")
    lines.extend(probe_capital_pcf())
    lines.append("\n=== FUH HWA ===")
    lines.extend(probe_fh())
    lines.append("\n=== CATHAY ===")
    lines.extend(probe_cathay())
    text = "\n".join(lines)
    open(r"d:\ETF\output\probe_deep_out.txt", "w", encoding="utf-8").write(text)
    print("lines", len(lines))

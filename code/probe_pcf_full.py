#!/usr/bin/env python3
"""Probe PCF APIs for 00878, 00919, 00929."""
from __future__ import annotations

import json
import re
import ssl
import urllib.parse
import urllib.request

import sys

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def post_json(url: str, data: dict) -> str:
    body = json.dumps(data).encode()
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 ETF-HHI/1.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")


def probe_fhtrust() -> None:
    print("=== Fuh Hwa 00929 ===")
    for fund in ("ETF21", "00929"):
        for d in ("2026-06-06", "2026-06-08", "20260606"):
            url = f"https://www.fhtrust.com.tw/api/ETFPcf?fundID={fund}&pcfDate={d}"
            try:
                body = fetch_url(url)
                print("GET", fund, d, body[:180].replace("\n", " "))
            except Exception as e:
                print("GET ERR", fund, d, str(e)[:70])
        try:
            body = post_json(
                "https://www.fhtrust.com.tw/api/ETFPcf",
                {"fundID": fund, "pcfDate": "2026-06-06"},
            )
            j = json.loads(body)
            print("POST", fund, "top keys:", list(j.keys()))
            res = j.get("result")
            if isinstance(res, dict):
                for k, v in res.items():
                    if isinstance(v, list):
                        print(f"  result.{k} len={len(v)} sample={v[:2]}")
                    else:
                        print(f"  result.{k} = {str(v)[:100]}")
            else:
                print("  result type:", type(res), str(res)[:200])
        except Exception as e:
            print("POST ERR", fund, str(e)[:100])


def probe_taiwanindex() -> None:
    print("\n=== Taiwan Index backend ===")
    paths = []
    for code in ("IX0179", "IX0205", "IX0208", "IX0209"):
        paths.extend(
            [
                f"https://backend.taiwanindex.com.tw/api/Home/IndexConstituent?indexCode={code}",
                f"https://backend.taiwanindex.com.tw/api/IndexConstituent/{code}",
                f"https://backend.taiwanindex.com.tw/api/Index/{code}/ConstituentWeight",
                f"https://backend.taiwanindex.com.tw/api/IndexConstituentWeight?indexCode={code}",
                f"https://backend.taiwanindex.com.tw/api/IndexConstituentWeight/{code}",
            ]
        )
    for url in paths:
        try:
            body = fetch_url(url)
            if body.lstrip().startswith(("{", "[")):
                print("OK", url, len(body), body[:150].replace("\n", " "))
        except Exception:
            pass


def probe_cathay() -> None:
    print("\n=== Cathay 00878 ===")
    html = fetch_url("https://www.cathaysite.com.tw/ETF/trade/pcf/00878")
    for pat in (
        r"https?://[^\s\"']+",
        r"/ETF/[^\s\"']+",
        r"/api/[^\s\"']+",
    ):
        hits = re.findall(pat, html)
        for h in hits:
            if any(x in h.lower() for x in ("pcf", "api", "weight", "constitu")):
                print("hit:", h[:120])
    scripts = re.findall(r'src="([^"]+\.js)"', html)
    print("scripts:", scripts[:8])
    for s in scripts[:3]:
        if s.startswith("/"):
            s = "https://www.cathaysite.com.tw" + s
        try:
            js = fetch_url(s)
            for m in re.findall(r"['\"](/[^'\"]*(?:api|pcf|PCF)[^'\"]*)['\"]", js):
                print("js api:", m[:100])
            for m in re.findall(r"https?://[^'\"\\s]+(?:api|pcf)[^'\"\\s]*", js, re.I):
                print("js url:", m[:120])
        except Exception as e:
            print("js err", s[:60], str(e)[:50])


def probe_capital() -> None:
    print("\n=== Capital 00919 ===")
    html = fetch_url("https://www.capitalfund.com.tw/etf/pcf/00919")
    for pat in (
        r"https?://[^\s\"']+",
        r"/etf/[^\s\"']+",
        r"/api/[^\s\"']+",
    ):
        hits = re.findall(pat, html)
        for h in hits:
            if any(x in h.lower() for x in ("pcf", "api", "weight", "constitu")):
                print("hit:", h[:120])
    scripts = re.findall(r'src="([^"]+\.js)"', html)
    print("scripts:", scripts[:8])
    for s in scripts[:5]:
        if s.startswith("/"):
            s = "https://www.capitalfund.com.tw" + s
        elif not s.startswith("http"):
            s = "https://www.capitalfund.com.tw/" + s.lstrip("/")
        try:
            js = fetch_url(s)
            for m in re.findall(r"['\"](/[^'\"]*(?:api|pcf|PCF)[^'\"]*)['\"]", js):
                print("js api:", m[:100])
            for m in re.findall(r"https?://[^'\"\\s]+(?:api|pcf)[^'\"\\s]*", js, re.I):
                print("js url:", m[:120])
        except Exception as e:
            print("js err", s[:60], str(e)[:50])


def probe_fhtrust_detail() -> None:
    print("\n=== Fuh Hwa detail endpoints ===")
    for d in ("20260608", "20260606", "20260605"):
        body = fetch_url(
            f"https://www.fhtrust.com.tw/api/ETFPcf?fundID=ETF21&pcfDate={d}"
        )
        j = json.loads(body)
        inner = (j.get("result") or [{}])[0].get("result") or []
        print("FH compact date", d, "holdings len", len(inner))
        if inner:
            print(" sample", inner[:2])

    for ep in (
        "ETFPcfDetail",
        "ETFPcfStock",
        "ETFStock",
        "ETFPcfList",
        "ETFPortfolio",
        "ETFHoldings",
        "ETFPcfItem",
    ):
        for q in ("fundID=ETF21&pcfDate=20260608", "fundID=ETF21", "etf002=00929"):
            url = f"https://www.fhtrust.com.tw/api/{ep}?{q}"
            try:
                body = fetch_url(url)
                if body.lstrip().startswith("{"):
                    print("OK", ep, q, body[:220].replace("\n", " "))
            except Exception:
                pass


def probe_capital_api() -> None:
    print("\n=== Capital API ===")
    for ep in ("items", "index", "delivery", "nav", "list"):
        for q in (
            "etfId=00919",
            "fundId=00919",
            "code=00919",
            "etfCode=00919",
            "id=00919",
        ):
            url = f"https://www.capitalfund.com.tw/api/etf/{ep}?{q}"
            try:
                body = fetch_url(url)
                if len(body) > 80 and not body.lstrip().startswith("<!"):
                    print("CAP", ep, q, body[:220].replace("\n", " "))
            except Exception:
                pass
    for url in (
        "https://www.capitalfund.com.tw/CFWeb/api/etf/nav?etfId=00919",
        "https://www.capitalfund.com.tw/api/etf/items?etfCode=00919",
        "http://125.227.3.107/CapitalFundAPI/api/etf/pcf?fundId=00919",
    ):
        try:
            body = fetch_url(url)
            print("CAP url", url, body[:220].replace("\n", " "))
        except Exception as e:
            print("CAP ERR", url, str(e)[:60])


def probe_cathay_js() -> None:
    print("\n=== Cathay main.js ===")
    js = fetch_url("https://www.cathaysite.com.tw/main.1047ac4f81a3da4e7643.js")
    hits = sorted(
        set(
            re.findall(
                r'["\'](/[^"\']*(?:pcf|PCF|api|Api|trade)[^"\']*)["\']',
                js,
            )
        )
    )
    for h in hits[:40]:
        print("CY", h[:120])
    for h in hits:
        if "pcf" in h.lower() or "constitu" in h.lower():
            url = "https://www.cathaysite.com.tw" + h if h.startswith("/") else h
            try:
                body = fetch_url(url)
                print("CY fetch", url, body[:180].replace("\n", " "))
            except Exception as e:
                print("CY ERR", url, str(e)[:50])


if __name__ == "__main__":
    probe_fhtrust()
    probe_fhtrust_detail()
    probe_taiwanindex()
    probe_cathay()
    probe_cathay_js()
    probe_capital()
    probe_capital_api()

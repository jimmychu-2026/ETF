#!/usr/bin/env python3
import json
import re
import sys

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url
from parse_nuxt_weights import hhi_from_weight_pcts

FH_ENDPOINTS = [
    "stockhold",
    "assets",
    "ETFindex",
    "frontdetail",
    "EI_PortfolioData",
]

CFWEB = [
    "holdings",
    "holding",
    "portfolio",
    "pcf",
    "constituent",
    "stock",
    "stockhold",
    "indexweight",
    "weights",
    "hold",
]


def parse_cathay_holdings_html(html: str) -> list[tuple[str, float, str]]:
    """Extract (code, weight_pct, name) from Cathay holdings page."""
    # Angular embedded JSON patterns
    for pat in (
        r'"stockCode"\s*:\s*"(\d{4,5})"[^}]{0,300}?"weight"\s*:\s*([0-9.]+)',
        r'"code"\s*:\s*"(\d{4,5})"[^}]{0,300}?"weighting"\s*:\s*([0-9.]+)',
        r'"stockNo"\s*:\s*"(\d{4,5})"[^}]{0,300}?"ratio"\s*:\s*([0-9.]+)',
        r'stockCode:"(\d{4,5})"[^}]{0,300}?weight:([0-9.]+)',
    ):
        rows = re.findall(pat, html)
        if len(rows) >= 5:
            return [(c, float(w), c) for c, w in rows]

    # table rows: 2330 台積電 12.34%
    rows = re.findall(
        r"(\d{4,5})\s*</[^>]+>\s*<[^>]+>\s*([^<]{2,20})\s*</[^>]+>\s*<[^>]+>\s*([0-9.]+)\s*%",
        html,
    )
    if len(rows) >= 5:
        return [(c, float(w), n.strip()) for c, n, w in rows]
    return []


def probe_fh() -> None:
    print("=== Fuh Hwa extra APIs ===")
    for ep in FH_ENDPOINTS:
        for q in (
            "fundID=ETF21",
            "fundID=ETF21&pcfDate=20260608",
            "etf002=00929",
            "fundId=ETF21",
        ):
            url = f"https://www.fhtrust.com.tw/api/{ep}?{q}"
            try:
                body = fetch_url(url)
                if body.lstrip().startswith("{"):
                    j = json.loads(body)
                    blob = json.dumps(j, ensure_ascii=False)
                    if "weight" in blob.lower() or "stock" in blob.lower():
                        print("OK", ep, q, blob[:300])
                        for k, v in (j.get("result") or j).items() if isinstance(j.get("result"), dict) else []:
                            if isinstance(v, list) and v:
                                print("  list", k, len(v), str(v[0])[:120])
            except Exception as e:
                pass


def probe_cfweb_holdings() -> None:
    print("\n=== Capital CFWeb extended ===")
    base = "https://www.capitalfund.com.tw/CFWeb/api/etf"
    pls = [{"stocNo": "00919"}, {"fundNo": "195"}, {"fundId": "195"}]
    for p in CFWEB:
        for pl in pls:
            url = f"{base}/{p}"
            try:
                from probe_sources3 import post_json

                body = post_json(url, pl, "https://www.capitalfund.com.tw/etf/product/detail/195")
                if body.lstrip().startswith("{") and "weight" in body.lower():
                    print("OK", p, pl, body[:350].replace("\n", " "))
            except Exception:
                pass


def probe_cathay() -> None:
    print("\n=== Cathay holdings pages ===")
    for path in (
        "/ETF/detail/ECN/holdings",
        "/ETF/holdings/00878",
    ):
        html = fetch_url("https://www.cathaysite.com.tw" + path)
        rows = parse_cathay_holdings_html(html)
        print(path, "parsed rows", len(rows))
        if rows:
            stats = hhi_from_weight_pcts(rows)
            print("  stats", stats)
            print("  sample", rows[:3])


if __name__ == "__main__":
    probe_fh()
    probe_cfweb_holdings()
    probe_cathay()

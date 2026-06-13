#!/usr/bin/env python3
import json
import re
import sys

sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

BASE = "https://backend.taiwanindex.com.tw/api"


def try_urls(codes):
    templates = [
        "{base}/IndexConstituent/{code}",
        "{base}/IndexConstituent?indexCode={code}",
        "{base}/Home/IndexConstituent?indexCode={code}",
        "{base}/Index/{code}/Constituent",
        "{base}/Index/{code}/ConstituentWeight",
        "{base}/IndexConstituentWeight?indexCode={code}",
        "{base}/IndexConstituentWeight/{code}",
        "{base}/IndexConstituent/Weight?indexCode={code}",
        "{base}/IndexConstituent/Weight/{code}",
        "{base}/IndexConstituent/Get?indexCode={code}",
        "{base}/IndexConstituent/Get/{code}",
        "{base}/IndexConstituent/GetWeight?indexCode={code}",
        "{base}/IndexConstituent/GetWeight/{code}",
        "{base}/IndexConstituent/GetLatest?indexCode={code}",
        "{base}/IndexConstituent/GetLatest/{code}",
        "{base}/IndexConstituent/GetLatestWeight?indexCode={code}",
        "{base}/IndexConstituent/GetLatestWeight/{code}",
        "{base}/IndexConstituent/GetLatestWeightList?indexCode={code}",
        "{base}/IndexConstituent/GetLatestWeightList/{code}",
        "{base}/IndexConstituent/GetLatestWeightList?indexNo={code}",
        "{base}/IndexConstituent/GetLatestWeightList?indexId={code}",
        "{base}/IndexConstituent/GetLatestWeightList?index={code}",
        "{base}/IndexConstituent/GetLatestWeightList?code={code}",
        "{base}/IndexConstituent/GetLatestWeightList?indexCode={code}&lang=tw",
        "{base}/IndexConstituent/GetLatestWeightList?indexCode={code}&language=tw",
        "{base}/IndexConstituent/GetLatestWeightList?indexCode={code}&lang=zh",
        "{base}/IndexConstituent/GetLatestWeightList?indexCode={code}&lang=zh-TW",
        "{base}/IndexConstituent/GetLatestWeightList?indexCode={code}&lang=zh_TW",
        "{base}/IndexConstituent/GetLatestWeightList?indexCode={code}&lang=zh-tw",
        "{base}/IndexConstituent/GetLatestWeightList?indexCode={code}&lang=zh_tw",
    ]
    for code in codes:
        for t in templates:
            url = t.format(base=BASE, code=code)
            try:
                body = fetch_url(url)
                if body.lstrip().startswith(("{", "[")) and len(body) > 100:
                    print("OK", url, body[:200].replace("\n", " "))
            except Exception:
                pass


def parse_nuxt_from_page(code: str) -> None:
    url = f"https://www.taiwanindex.com.tw/indexes/{code}"
    html = fetch_url(url)
    start = html.find("window.__NUXT__=")
    if start < 0:
        print(code, "no nuxt")
        return
    blob = html[start : start + 1200000]
    patterns = [
        r'stock_id:"(\d{4,5})"[^}]{0,300}?weight:([0-9.]+)',
        r'stockCode:"(\d{4,5})"[^}]{0,300}?weight:([0-9.]+)',
        r'code:"(\d{4,5})"[^}]{0,300}?weight_per:([0-9.]+)',
        r'securitiesCode:"(\d{4,5})"[^}]{0,300}?weight:([0-9.]+)',
    ]
    for pat in patterns:
        rows = re.findall(pat, blob)
        if len(rows) >= 5:
            print(code, pat[:30], "rows", len(rows), "sample", rows[:3])
            wsum = sum(float(w) for _, w in rows)
            print("  wsum", wsum)
            return
    # search for constituent keyword chunks
    for kw in ("constituent", "Constituent", "weightList", "indexConstituent"):
        if kw in blob:
            print(code, "has keyword", kw)
    print(code, "nuxt len", len(blob), "no weight rows")


if __name__ == "__main__":
    codes = ("IX0179", "IX0205", "IX0208", "IX0209", "IX0210")
    try_urls(codes)
    for c in codes:
        parse_nuxt_from_page(c)

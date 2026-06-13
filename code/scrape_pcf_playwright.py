#!/usr/bin/env python3
"""Scrape full PCF holdings via Playwright network interception."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(r"d:\ETF\output\pcf_scrape")
OUT.mkdir(parents=True, exist_ok=True)

TARGETS = [
    {
        "ticker": "00878",
        "url": "https://www.cathaysite.com.tw/ETF/trade/pcf/00878",
        "api_hint": "cwapi.cathaysite.com.tw",
    },
    {
        "ticker": "00919",
        "url": "https://www.capitalfund.com.tw/etf/pcf/00919",
        "api_hint": "buyback",
    },
    {
        "ticker": "00929",
        "url": "https://www.fhtrust.com.tw/ETF/trade_list",
        "api_hint": "ETFPcf",
    },
]


def extract_weights_from_json(obj, path="") -> list[dict]:
    hits: list[dict] = []
    if isinstance(obj, dict):
        keys = {k.lower() for k in obj.keys()}
        if {"stockcode", "weights"}.issubset(keys) or {"stocno", "weight"}.issubset(keys):
            hits.append(obj)
        if "stockWeights" in obj and isinstance(obj["stockWeights"], list):
            hits.extend(obj["stockWeights"])
        if "stocks" in obj and isinstance(obj["stocks"], list) and obj["stocks"]:
            hits.extend(obj["stocks"])
        if "result" in obj and isinstance(obj["result"], list):
            for item in obj["result"]:
                if isinstance(item, dict) and any(k in item for k in ("stockCode", "stocNo", "ratio", "weight")):
                    hits.append(item)
        for k, v in obj.items():
            hits.extend(extract_weights_from_json(v, f"{path}.{k}"))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits.extend(extract_weights_from_json(v, f"{path}[{i}]"))
    return hits


def normalize_row(row: dict) -> tuple[str, float, str] | None:
    code = (
        row.get("stockCode")
        or row.get("stocNo")
        or row.get("stockNo")
        or row.get("code")
        or row.get("itemNo")
    )
    wt = row.get("weights") or row.get("weight") or row.get("weightRound") or row.get("ratio")
    name = row.get("stockName") or row.get("stocName") or row.get("itemName") or code
    if not code or wt is None:
        return None
    if isinstance(wt, str):
        wt = wt.replace("%", "").replace(",", "").strip()
    try:
        w = float(wt)
    except ValueError:
        return None
    code = str(code).strip()
    if w <= 1.5 and "ratio" not in row:  # fraction not pct
        w *= 100
    return code, w, str(name)


def scrape_one(page, target: dict) -> dict:
    captured: list[tuple[str, str]] = []

    def on_response(resp):
        url = resp.url
        hint = target["api_hint"]
        if hint not in url:
            return
        try:
            if "json" in (resp.headers.get("content-type") or "").lower() or url.endswith((".json",)):
                body = resp.text()
            else:
                body = resp.text()
            if len(body) > 50:
                captured.append((url, body))
        except Exception:
            pass

    page.on("response", on_response)
    page.goto(target["url"], wait_until="networkidle", timeout=90000)

    if target["ticker"] == "00929":
        # Select 00929 in trade list and search PCF
        page.select_option('select[name="fundID"]', "ETF21") if page.locator('select[name="fundID"]').count() else None
        for sel in ("#fundID", "select.fundID", "select"):
            loc = page.locator(sel)
            if loc.count():
                try:
                    loc.first.select_option(value="ETF21")
                    break
                except Exception:
                    pass
        for btn in ("button:has-text('查詢')", "input[type=submit]", ".search-btn", "#searchBtn"):
            if page.locator(btn).count():
                page.locator(btn).first.click()
                page.wait_for_timeout(3000)
                break

    page.wait_for_timeout(5000)
    html = page.content()
    (OUT / f"{target['ticker']}_page.html").write_text(html, encoding="utf-8")

    rows: list[tuple[str, float, str]] = []
    for url, body in captured:
        (OUT / f"{target['ticker']}_api.json").write_text(body, encoding="utf-8")
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            continue
        for hit in extract_weights_from_json(data):
            norm = normalize_row(hit)
            if norm:
                rows.append(norm)

    # DOM fallback: table rows with stock code + weight
    if not rows:
        text = html
        for m in re.finditer(r"(\d{4,5})[^%]{0,40}?(\d+\.\d+)\s*%", text):
            rows.append((m.group(1), float(m.group(2)), m.group(1)))

    # dedupe by code keeping max weight
    dedup: dict[str, tuple[str, float, str]] = {}
    for code, w, name in rows:
        if code not in dedup or w > dedup[code][1]:
            dedup[code] = (code, w, name)

    final = list(dedup.values())
    return {
        "ticker": target["ticker"],
        "captured_urls": [u for u, _ in captured],
        "n_rows": len(final),
        "rows": final,
        "weight_sum": sum(r[1] for r in final),
    }


def main():
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
            ignore_https_errors=True,
        )
        page = context.new_page()
        for t in TARGETS:
            print(f"Scraping {t['ticker']}...")
            try:
                r = scrape_one(page, t)
                print(f"  rows={r['n_rows']} wsum={r['weight_sum']:.1f} urls={r['captured_urls'][:2]}")
                results.append(r)
            except Exception as e:
                print(f"  ERR: {e}")
                results.append({"ticker": t["ticker"], "error": str(e)})
        browser.close()

    out_path = OUT / "scrape_results.json"
    out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()

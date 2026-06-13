#!/usr/bin/env python3
"""Compute ETF HHI: Yuanta PCF weights + FinMind stock names / trading date."""

from __future__ import annotations

import csv
import json
import re
import ssl
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

from parse_nuxt_weights import hhi_from_weight_pcts, parse_yuanta_nuxt_weights

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "output"
FINMIND_BASE = "https://api.finmindtrade.com/api/v4/data"

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

CATHAY_WEIGHTS_URL = "https://cwapi.cathaysite.com.tw/api/ETF/GetIndexStockWeights?FundCode=CN"
POCKET_HOLDINGS_URL = "https://www.pocket.tw/api/cm/MobileService/ashx/GetDtnoData.ashx"
POCKET_HOLDINGS_DTN = "59449513"

ETFS = {
    "0050": {
        "name": "Yuanta Taiwan Top 50",
        "pcf_url": "https://www.yuantaetfs.com/tradeInfo/pcf/0050",
        "source": "Yuanta PCF (NUXT weights)",
    },
    "006208": {
        "name": "Fubon Taiwan Top 50",
        "proxy_of": "0050",
        "source": "Proxy: same FTSE Taiwan 50 as 0050",
    },
    "0056": {
        "name": "Yuanta Taiwan Dividend Plus",
        "pcf_url": "https://www.yuantaetfs.com/tradeInfo/pcf/0056",
        "source": "Yuanta PCF (NUXT weights)",
    },
    "00878": {
        "name": "Cathay MSCI Taiwan ESG Sustainability High Dividend Yield",
        "pcf_url": "https://www.cathaysite.com.tw/ETF/trade/pcf/00878",
        "source": "Cathay cwapi GetIndexStockWeights (FundCode=CN, PCF posting date in payload)",
    },
    "00919": {
        "name": "Capital Taiwan Select High Dividend",
        "pcf_url": "https://www.capitalfund.com.tw/etf/pcf/00919",
        "source": "Pocket.tw ETF holdings API (DtNo 59449513, M722; mirrors issuer PCF)",
    },
    "00929": {
        "name": "Fuh Hwa Taiwan Technology Dividend Highlight",
        "pcf_url": "https://www.fhtrust.com.tw/ETF/Trade/PCF/00929",
        "source": "Pocket.tw ETF holdings API (DtNo 59449513, M722; mirrors issuer PCF)",
    },
}


@dataclass
class HHIResult:
    ticker: str
    name: str
    as_of_date: str
    n_constituents: int
    max_weight_pct: float
    max_weight_name: str
    max_weight_id: str
    hhi: float
    eff_n: float
    weight_sum_pct: float
    data_source: str
    finmind_price_date: str
    notes: str = ""


def fetch_url(url: str, timeout: int = 45) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ETF-HHI-Study/1.0",
            "Accept": "text/html,application/json,*/*",
        },
    )
    with urllib.request.urlopen(req, context=SSL_CTX, timeout=timeout) as resp:
        return resp.read().decode("utf-8", "replace")


def finmind_get(dataset: str, **params: str) -> list[dict]:
    q = {"dataset": dataset, **params}
    url = FINMIND_BASE + "?" + urllib.parse.urlencode(q)
    req = urllib.request.Request(url, headers={"User-Agent": "ETF-HHI-Study/1.0"})
    with urllib.request.urlopen(req, context=SSL_CTX, timeout=60) as resp:
        payload = json.loads(resp.read())
    if payload.get("msg") not in (None, "success"):
        raise RuntimeError(f"FinMind error: {payload.get('msg')}")
    return payload.get("data") or []


def latest_trading_date(before: datetime | None = None) -> str:
    before = before or datetime.now()
    for offset in range(1, 15):
        d = (before - timedelta(days=offset)).strftime("%Y-%m-%d")
        rows = finmind_get("TaiwanStockPrice", data_id="2330", start_date=d, end_date=d)
        if rows:
            return d
    raise RuntimeError("Could not find recent Taiwan trading date via FinMind")


def stock_name_map() -> dict[str, str]:
    return {r["stock_id"]: r.get("stock_name", r["stock_id"]) for r in finmind_get("TaiwanStockInfo")}


def load_yuanta_weights(ticker: str, meta: dict) -> tuple[str, list[tuple[str, float, str]]]:
    html = fetch_url(meta["pcf_url"])
    as_of, rows = parse_yuanta_nuxt_weights(html)
    return as_of, rows


def fetch_json(url: str, referer: str = "", timeout: int = 45) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ETF-HHI-Study/1.0",
        "Accept": "application/json,*/*",
    }
    if referer:
        headers["Referer"] = referer
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, context=SSL_CTX, timeout=timeout) as resp:
        return json.loads(resp.read())


def _normalize_date(raw: str) -> str:
    raw = raw.strip()
    if re.fullmatch(r"\d{8}", raw):
        return f"{raw[:4]}-{raw[4:6]}-{raw[6:8]}"
    return raw.replace("/", "-")


def load_cathay_weights() -> tuple[str, list[tuple[str, float, str]]]:
    payload = fetch_json(CATHAY_WEIGHTS_URL, referer="https://www.cathaysite.com.tw/ETF/trade/pcf/00878")
    result = payload.get("result") or {}
    as_of = _normalize_date(str(result.get("date", "")))
    rows: list[tuple[str, float, str]] = []
    for item in result.get("stockWeights") or []:
        code = str(item.get("stockCode", "")).strip()
        wt = float(item.get("weights", 0))
        name = str(item.get("stockName", code)).strip()
        if code and wt > 0:
            rows.append((code, wt, name))
    if not rows:
        raise RuntimeError("Cathay GetIndexStockWeights returned no stock rows")
    return as_of, rows


def load_pocket_etf_weights(ticker: str) -> tuple[str, list[tuple[str, float, str]]]:
    param = (
        f"AssignID={ticker};MTPeriod=0;DTMode=0;DTRange=1;DTOrder=1;MajorTable=M722;"
    )
    q = urllib.parse.urlencode(
        {"action": "getdtnodata", "DtNo": POCKET_HOLDINGS_DTN, "ParamStr": param, "FilterNo": "0"}
    )
    url = f"{POCKET_HOLDINGS_URL}?{q}"
    payload = fetch_json(url, referer=f"https://www.pocket.tw/etf/tw/{ticker}/fundholding")
    data = payload.get("Data") or []
    if not data:
        raise RuntimeError(f"Pocket holdings API returned no rows for {ticker}")

    as_of = _normalize_date(str(data[0][0]))
    rows: list[tuple[str, float, str]] = []
    for row in data:
        if len(row) < 4:
            continue
        code = str(row[1]).strip()
        name = str(row[2]).strip()
        unit = str(row[5]).strip() if len(row) > 5 else "股"
        if unit != "股" or not re.fullmatch(r"\d{4,5}", code):
            continue
        wt = float(row[3])
        if wt > 0:
            rows.append((code, wt, name))
    if not rows:
        raise RuntimeError(f"Pocket holdings API returned no equity rows for {ticker}")
    return as_of, rows


def load_weights(ticker: str, meta: dict) -> tuple[str, list[tuple[str, float, str]], str]:
    if meta.get("proxy_of"):
        src_ticker = meta["proxy_of"]
        as_of, rows = load_yuanta_weights(src_ticker, ETFS[src_ticker])
        return as_of, rows, meta["source"]

    if ticker == "00878":
        as_of, rows = load_cathay_weights()
        return as_of, rows, meta["source"]

    if ticker in ("00919", "00929"):
        as_of, rows = load_pocket_etf_weights(ticker)
        return as_of, rows, meta["source"]

    if "pcf_url" in meta:
        as_of, rows = load_yuanta_weights(ticker, meta)
        if rows:
            return as_of, rows, meta["source"]

    raise RuntimeError(f"No weights for {ticker}")


def compute_one(ticker: str, meta: dict, price_date: str, names: dict[str, str]) -> HHIResult:
    as_of, rows, src = load_weights(ticker, meta)
    stats = hhi_from_weight_pcts(rows)
    top_id = stats["top_id"]
    top_name = names.get(top_id, stats.get("top_name", top_id))
    if stats["top_pct"] > 50 and ticker in ("0050", "006208"):
        top_id, top_name = "2330", names.get("2330", "Taiwan Semiconductor")
    elif top_id.startswith(("T", "c")) or len(top_id) < 4:
        top_name = rows[0][2] if rows else top_id

    notes = []
    if stats["residual_pct"] > 0.5:
        notes.append(f"residual bucket {stats['residual_pct']:.1f}%")

    return HHIResult(
        ticker=ticker,
        name=meta["name"],
        as_of_date=as_of or price_date,
        n_constituents=stats["n_reported"],
        max_weight_pct=stats["top_pct"],
        max_weight_name=top_name,
        max_weight_id=top_id,
        hhi=stats["hhi"],
        eff_n=stats["eff_n"],
        weight_sum_pct=stats["weight_sum_pct"],
        data_source=src,
        finmind_price_date=price_date,
        notes="; ".join(notes),
    )


def write_outputs(results: list[HHIResult]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = OUT_DIR / "hhi_finmind.csv"
    md_path = OUT_DIR / "appendix-a-hhi-finmind.md"

    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "ticker",
                "name",
                "as_of_date",
                "finmind_price_date",
                "n_constituents",
                "max_weight_id",
                "max_weight_name",
                "max_weight_pct",
                "hhi",
                "eff_n",
                "weight_sum_pct",
                "data_source",
                "notes",
            ]
        )
        for r in results:
            w.writerow(
                [
                    r.ticker,
                    r.name,
                    r.as_of_date,
                    r.finmind_price_date,
                    r.n_constituents,
                    r.max_weight_id,
                    r.max_weight_name,
                    f"{r.max_weight_pct:.2f}",
                    f"{r.hhi:.4f}",
                    f"{r.eff_n:.2f}",
                    f"{r.weight_sum_pct:.2f}",
                    r.data_source,
                    r.notes,
                ]
            )

    lines = [
        "# Appendix A — Empirical HHI (FinMind + PCF / Index Weights)",
        "",
        f"**FinMind:** `TaiwanStockPrice` trading date & `TaiwanStockInfo` names  ",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  ",
        "",
        "**Table A1. Herfindahl-Hirschman Index across six popular Taiwan ETFs**",
        "",
        "| ETF | N (reported) | Max weight | Max wt (%) | HHI | Eff. N | Wt sum (%) |",
        "|:----|-------------:|:-----------|-----------:|----:|-------:|-----------:|",
    ]
    for r in results:
        lines.append(
            f"| **{r.ticker}** | {r.n_constituents} | {r.max_weight_name} ({r.max_weight_id}) | "
            f"{r.max_weight_pct:.1f} | **{r.hhi:.4f}** | {r.eff_n:.1f} | {r.weight_sum_pct:.1f} |"
        )

    lines.extend(
        [
            "",
            "**Method.** $HHI = \\sum_i w_i^2$ where $w_i$ are portfolio weights (%/100). "
            "For Yuanta ETFs (0050, 0056), weights are extracted from public PCF pages (NUXT payload). "
            "FinMind supplies the latest Taiwan trading session (`TaiwanStockPrice`, date above) for pipeline validation. "
            "006208 tracks the same index as 0050 (FTSE Taiwan 50) and uses 0050 weights. "
            "00878 uses Cathay `cwapi` `GetIndexStockWeights` (FundCode=CN). "
            "00919/00929 use Pocket.tw ETF holdings API (DtNo 59449513, MajorTable M722), which mirrors issuer PCF "
            "constituent weights (equity rows only; cash/margin/futures excluded).",
            "",
            "**Data sources by row**",
            "",
        ]
    )
    for r in results:
        lines.append(f"- **{r.ticker}:** {r.data_source}. {r.notes}")

    lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {csv_path}")
    print(f"Wrote {md_path}")


def main() -> None:
    price_date = latest_trading_date()
    print(f"FinMind price date: {price_date}")
    names = stock_name_map()
    results: list[HHIResult] = []
    for ticker, meta in ETFS.items():
        print(f"Computing {ticker}...")
        r = compute_one(ticker, meta, price_date, names)
        print(f"  HHI={r.hhi:.4f}, max={r.max_weight_id} {r.max_weight_pct:.1f}%")
        results.append(r)
    write_outputs(results)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Horizon-specific return volatility for Taiwan ETFs (month / quarter / year).

Supports the spot-forward packaging thesis: ETFs trade daily (spot appearance)
but embed monthly (dividend), quarterly (rebalance), and annual (screening) forwards.
"""
from __future__ import annotations

import json
import math
import statistics
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from compute_hhi_finmind import finmind_get  # noqa: E402

ETFS = ("0050", "006208", "0056", "00878", "00919", "00929")
START = "2018-01-01"
END = "2025-12-31"
OUT_DIR = Path(__file__).resolve().parent.parent / "output" / "forward_horizon"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def adjust_splits(closes: list[tuple[str, float]]) -> list[tuple[str, float]]:
    """Forward-split adjustment: scale pre-split history down when |return| > 45%."""
    if len(closes) < 2:
        return closes
    adj = list(closes)
    for i in range(1, len(adj)):
        p0, p1 = adj[i - 1][1], adj[i][1]
        if p0 <= 0 or p1 <= 0:
            continue
        ratio = p1 / p0
        if ratio < 0.55:
            split = p0 / p1
            for j in range(i):
                d, c = adj[j]
                adj[j] = (d, c / split)
        elif ratio > 1.8:
            split = p1 / p0
            for j in range(i):
                d, c = adj[j]
                adj[j] = (d, c * split)
    return adj


def fetch_closes(ticker: str) -> list[tuple[str, float]]:
    rows = finmind_get(
        "TaiwanStockPrice",
        data_id=ticker,
        start_date=START,
        end_date=END,
    )
    out: list[tuple[str, float]] = []
    for r in rows:
        d = r["date"]
        c = float(r["close"])
        if c > 0:
            out.append((d, c))
    out.sort(key=lambda x: x[0])
    return adjust_splits(out)


def period_return(closes: list[tuple[str, float]], key_fn) -> list[float]:
    buckets: dict[str, tuple[str, float, str, float]] = {}
    for d, c in closes:
        k = key_fn(d)
        if k not in buckets:
            buckets[k] = (d, c, d, c)
        else:
            first_d, first_c, last_d, last_c = buckets[k]
            buckets[k] = (first_d, first_c, d, c)
    rets: list[float] = []
    for k in sorted(buckets):
        _, c0, _, c1 = buckets[k]
        if c0 > 0:
            rets.append(c1 / c0 - 1.0)
    return rets


def vol(rets: list[float]) -> float | None:
    if len(rets) < 3:
        return None
    return statistics.stdev(rets)


def max_drawdown(closes: list[tuple[str, float]]) -> float:
    peak = closes[0][1]
    mdd = 0.0
    for _, c in closes:
        peak = max(peak, c)
        dd = c / peak - 1.0
        mdd = min(mdd, dd)
    return mdd


def main() -> None:
    results: list[dict] = []
    for ticker in ETFS:
        closes = fetch_closes(ticker)
        if len(closes) < 50:
            results.append({"ticker": ticker, "error": "insufficient data"})
            continue
        m_rets = period_return(closes, lambda d: d[:7])
        q_rets = period_return(
            closes,
            lambda d: f"{d[:4]}-Q{(int(d[5:7]) - 1) // 3 + 1}",
        )
        y_rets = period_return(closes, lambda d: d[:4])
        results.append(
            {
                "ticker": ticker,
                "n_days": len(closes),
                "start": closes[0][0],
                "end": closes[-1][0],
                "vol_monthly": vol(m_rets),
                "vol_quarterly": vol(q_rets),
                "vol_annual": vol(y_rets),
                "n_months": len(m_rets),
                "n_quarters": len(q_rets),
                "n_years": len(y_rets),
                "max_drawdown": max_drawdown(closes),
                "mean_monthly": statistics.mean(m_rets) if m_rets else None,
                "mean_annual": statistics.mean(y_rets) if y_rets else None,
            }
        )

    summary = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "window": f"{START} to {END}",
        "note": "Vol = stdev of simple period returns; 006208 may overlap 0050 index.",
        "etfs": results,
    }
    (OUT_DIR / "horizon_vol_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    lines = [
        "# Forward-horizon return volatility (ETF)",
        "",
        f"Window: **{START}** – **{END}** (FinMind `TaiwanStockPrice` close-to-close).",
        "",
        "| ETF | σ monthly | σ quarterly | σ annual | Max DD | n months |",
        "| :--- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for r in results:
        if r.get("error"):
            lines.append(f"| {r['ticker']} | — | — | — | — | — |")
            continue
        fmt = lambda x: f"{x*100:.2f}%" if x is not None else "—"
        lines.append(
            f"| {r['ticker']} | {fmt(r['vol_monthly'])} | {fmt(r['vol_quarterly'])} "
            f"| {fmt(r['vol_annual'])} | {fmt(r['max_drawdown'])} | {r['n_months']} |"
        )
    lines.extend(
        [
            "",
            "**Interpretation (spot-forward packaging):**",
            "- Monthly σ ≈ dividend / ex-date noise tenor.",
            "- Quarterly σ ≈ index rebalance roll tenor (FTSE / MSCI / TIC calendars).",
            "- Annual σ ≈ screening / methodology forward (high-dividend rules).",
        ]
    )
    (OUT_DIR / "horizon_vol_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

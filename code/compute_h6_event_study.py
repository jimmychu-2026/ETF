#!/usr/bin/env python3
"""H6 event-study pilot: rebalance windows (H6a), ex-div months (H6b), yield/G_t proxy (H6d).

Spot-forward thesis: calendar risk Λ^cal and dividend gap G_t materialize around
known rebalance and ex-dividend dates.
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from compute_forward_horizon_risk import (  # noqa: E402
    ETFS,
    END,
    START,
    adjust_splits,
    fetch_closes,
)
from compute_hhi_finmind import finmind_get  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent.parent / "output" / "forward_horizon"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Approximate index rebalance months (public calendars; effective dates vary ±1 week)
REBALANCE_MONTHS: dict[str, list[int]] = {
    "0050": [3, 6, 9, 12],
    "006208": [3, 6, 9, 12],
    "0056": [6, 12],
    "00878": [5, 11],
    "00919": [6, 12],
    "00929": [6, 12],
}

HIGH_DIV = {"0056", "00878", "00919", "00929"}
EVENT_WINDOW = 10  # trading days before/after month-end of rebalance month


def daily_returns(closes: list[tuple[str, float]]) -> list[tuple[str, float]]:
    out: list[tuple[str, float]] = []
    for i in range(1, len(closes)):
        d0, p0 = closes[i - 1]
        d1, p1 = closes[i]
        if p0 > 0:
            out.append((d1, p1 / p0 - 1.0))
    return out


def vol(rets: list[float]) -> float | None:
    if len(rets) < 5:
        return None
    return statistics.stdev(rets)


def fetch_exdiv_dates(ticker: str) -> list[dict]:
    rows = finmind_get(
        "TaiwanStockDividendResult",
        data_id=ticker,
        start_date=START,
        end_date=END,
    )
    return sorted(rows, key=lambda r: r["date"])


def rebalance_event_dates(closes: list[tuple[str, float]], months: list[int]) -> set[str]:
    """Last EVENT_WINDOW trading days of each rebalance month + first EVENT_WINDOW of next month."""
    by_month: dict[str, list[str]] = defaultdict(list)
    for d, _ in closes:
        by_month[d[:7]].append(d)
    event: set[str] = set()
    sorted_months = sorted(by_month.keys())
    for ym in sorted_months:
        m = int(ym[5:7])
        if m not in months:
            continue
        days = by_month[ym]
        for d in days[-EVENT_WINDOW:]:
            event.add(d)
    # spill into first days of following month
    for i, ym in enumerate(sorted_months):
        m = int(ym[5:7])
        if m not in months:
            continue
        if i + 1 < len(sorted_months):
            nxt = sorted_months[i + 1]
            for d in by_month[nxt][:EVENT_WINDOW]:
                event.add(d)
    return event


def exdiv_months(exdiv_rows: list[dict]) -> set[str]:
    return {r["date"][:7] for r in exdiv_rows}


def analyze_ticker(ticker: str) -> dict:
    closes = fetch_closes(ticker)
    rets = daily_returns(closes)
    if len(rets) < 100:
        return {"ticker": ticker, "error": "insufficient data"}

    all_r = [r for _, r in rets]
    sigma_daily = vol(all_r)

    # H6a: rebalance window
    rebal_days = rebalance_event_dates(closes, REBALANCE_MONTHS.get(ticker, [6, 12]))
    rebal_r = [r for d, r in rets if d in rebal_days]
    other_r = [r for d, r in rets if d not in rebal_days]
    vol_rebal = vol(rebal_r)
    vol_other = vol(other_r)
    ratio_rebal = (vol_rebal / vol_other) if vol_rebal and vol_other else None

    # H6b: ex-div months (high-div ETFs; 0050 also has div)
    exdiv_rows = fetch_exdiv_dates(ticker)
    ex_months = exdiv_months(exdiv_rows)
    ex_r = [r for d, r in rets if d[:7] in ex_months]
    non_ex_r = [r for d, r in rets if d[:7] not in ex_months]
    vol_ex = vol(ex_r)
    vol_non_ex = vol(non_ex_r)
    ratio_ex = (vol_ex / vol_non_ex) if vol_ex and vol_non_ex else None

    # H6d proxy: yield panel (post-2024 only to avoid split scale mismatch on 0050)
    gap_events: list[dict] = []
    for row in exdiv_rows:
        if row["date"] < "2024-01-01":
            continue
        d = row["date"]
        before = float(row["before_price"])
        after = float(row["after_price"])
        declared = float(row.get("stock_and_cache_dividend") or 0)
        cash_implied = before - after
        g_proxy = max(0.0, (declared - cash_implied) / before) if before > 0 else None
        yield_single = declared / before if before > 0 else None
        gap_events.append(
            {
                "ex_date": d,
                "D_per_share": declared,
                "before_price": before,
                "yield_per_event": round(yield_single, 5) if yield_single else None,
                "G_proxy": round(g_proxy, 5) if g_proxy is not None else None,
            }
        )

    # Trailing 12m payout vs price (realized yield pressure)
    if gap_events:
        t12 = sum(e["D_per_share"] for e in gap_events[-12:])
        last_p = gap_events[-1]["before_price"]
        realized_yield = t12 / last_p if last_p > 0 else None
        # annualized from latest cadence
        latest_y = gap_events[-1].get("yield_per_event")
        n_per_year = len(gap_events) / max(1, len({e["ex_date"][:4] for e in gap_events}))
        ann_yield = latest_y * n_per_year if latest_y else None
    else:
        realized_yield = None
        ann_yield = None

    return {
        "ticker": ticker,
        "n_days": len(rets),
        "sigma_daily": sigma_daily,
        "H6a_rebalance": {
            "months": REBALANCE_MONTHS.get(ticker, []),
            "window_td": EVENT_WINDOW,
            "n_rebal_days": len(rebal_r),
            "vol_rebal_window": vol_rebal,
            "vol_other_days": vol_other,
            "ratio_rebal_over_other": ratio_rebal,
        },
        "H6b_exdiv_month": {
            "n_exdiv_events": len(exdiv_rows),
            "n_exdiv_months": len(ex_months),
            "vol_exdiv_month": vol_ex,
            "vol_non_exdiv_month": vol_non_ex,
            "ratio_ex_over_non": ratio_ex,
        },
        "H6d_yield_gap": {
            "realized_yield_t12_over_price": round(realized_yield, 4) if realized_yield else None,
            "ann_yield_from_latest_cadence": round(ann_yield, 4) if ann_yield else None,
            "events": gap_events[-6:],
        },
    }


def main() -> None:
    results = [analyze_ticker(t) for t in ETFS]
    summary = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "window": f"{START} to {END}",
        "notes": {
            "H6a": "Rebalance window = ±10 TD around rebalance month-end (calendar proxy).",
            "H6b": "Ex-div month = any month with TaiwanStockDividendResult ex-date.",
            "G_proxy": "max(0, (declared - (before-after))/before); EQ share needs issuer disclosure.",
        },
        "etfs": results,
    }
    (OUT_DIR / "h6_event_study.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    def pct(x: float | None) -> str:
        return f"{x*100:.2f}%" if x is not None else "—"

    lines = [
        "# H6 Event Study Pilot (Forward Calendar Risk)",
        "",
        f"Window: **{START}** – **{END}**",
        "",
        "## H6a — Rebalance window vol ratio (rebal / other)",
        "",
        "| ETF | Rebal months | Vol(rebal win) | Vol(other) | Ratio |",
        "| :--- | :--- | ---: | ---: | ---: |",
    ]
    for r in results:
        if r.get("error"):
            continue
        h = r["H6a_rebalance"]
        lines.append(
            f"| {r['ticker']} | {h['months']} | {pct(h['vol_rebal_window'])} "
            f"| {pct(h['vol_other_days'])} | **{h['ratio_rebal_over_other']:.2f}** |"
            if h["ratio_rebal_over_other"]
            else f"| {r['ticker']} | — | — | — | — |"
        )

    lines.extend(
        [
            "",
            "## H6b — Ex-dividend month vol ratio (ex month / other)",
            "",
            "| ETF | # ex events | Vol(ex mo) | Vol(other mo) | Ratio |",
            "| :--- | ---: | ---: | ---: | ---: |",
        ]
    )
    for r in results:
        if r.get("error"):
            continue
        h = r["H6b_exdiv_month"]
        ratio = h["ratio_ex_over_non"]
        lines.append(
            f"| {r['ticker']} | {h['n_exdiv_events']} | {pct(h['vol_exdiv_month'])} "
            f"| {pct(h['vol_non_exdiv_month'])} | **{ratio:.2f}** |"
            if ratio
            else f"| {r['ticker']} | — | — | — | — |"
        )

    lines.extend(
        [
            "",
            "## H6d — Ann. yield proxy (latest event yield × events/year, 2024+)",
            "",
            "| ETF | Ann. yield (proxy) | Latest D | Latest yield/event |",
            "| :--- | ---: | ---: | ---: |",
        ]
    )
    for r in results:
        if r.get("error"):
            continue
        y = r["H6d_yield_gap"]
        ev = y["events"][-1] if y["events"] else {}
        ann = y.get("ann_yield_from_latest_cadence")
        lines.append(
            f"| {r['ticker']} | {pct(ann)} "
            f"| {ev.get('D_per_share', '—')} | {pct(ev.get('yield_per_event'))} |"
        )

    (OUT_DIR / "h6_event_study.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""1912-1921 silk export (SITC 261) + London silver pilot."""

from __future__ import annotations

import json
import math
from datetime import datetime
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "silk_silver"
HITOU = OUT / "hitotsubashi_cn_trade_1913_1948.xlsx"
NBER_SILVER = OUT / "nber_a04018_silver.dat"
SITC_RAW_SILK = 261


def annual_vol(returns: list[float]) -> float:
    if len(returns) < 2:
        return float("nan")
    mu = sum(returns) / len(returns)
    var = sum((r - mu) ** 2 for r in returns) / (len(returns) - 1)
    return math.sqrt(var)


def max_drawdown(levels: list[float]) -> float:
    peak = levels[0]
    mdd = 0.0
    for x in levels:
        peak = max(peak, x)
        if peak:
            mdd = min(mdd, (x - peak) / peak)
    return mdd


def load_nber_silver() -> pd.DataFrame:
    rows = []
    for line in NBER_SILVER.read_text(encoding="utf-8", errors="replace").splitlines():
        parts = line.split()
        if len(parts) < 2:
            continue
        try:
            y, p = int(parts[0]), float(parts[1])
        except ValueError:
            continue
        rows.append({"year": y, "london_silver_usd_oz": p})
    df = pd.DataFrame(rows)
    return df[(df["year"] >= 1912) & (df["year"] <= 1921)].copy()


def load_silk_export_hkt() -> pd.DataFrame:
    df = pd.read_excel(HITOU, sheet_name="輸出", header=None)
    year_cols: list[tuple[int, int]] = []
    for c in range(df.shape[1]):
        try:
            y = int(float(df.iloc[2, c]))
            if 1900 < y < 1960:
                year_cols.append((c, y))
        except Exception:
            pass

    anchors: dict[int, float] = {}
    for i in range(3, len(df)):
        try:
            sitc = int(float(df.iloc[i, 0]))
        except Exception:
            continue
        if sitc != SITC_RAW_SILK:
            continue
        for c, y in year_cols:
            try:
                v = float(df.iloc[i, c])
            except Exception:
                continue
            if v > 0:
                anchors[y] = v

    if not anchors:
        raise RuntimeError(f"SITC {SITC_RAW_SILK} not found in Hitotsubashi xlsx")

    window_anchors = {y: v for y, v in anchors.items() if 1912 <= y <= 1921}
    if len(window_anchors) < 2:
        # use nearest CMC anchors bracketing the window
        before = {y: v for y, v in anchors.items() if y < 1922}
        ys = sorted(before)
        bracket = [y for y in ys if y <= 1921]
        if len(bracket) >= 2:
            y0, y1 = bracket[0], bracket[-1]
            window_anchors = {y0: anchors[y0], y1: anchors[y1]}
        else:
            window_anchors = anchors

    ay = sorted(window_anchors)
    y0, y1 = ay[0], ay[-1]
    v0, v1 = window_anchors[y0], window_anchors[y1]
    slope = (v1 - v0) / (y1 - y0) if y1 != y0 else 0.0

    years = list(range(1912, 1922))
    annual = pd.DataFrame(
        {
            "year": years,
            "export_value_hkt": [v0 + slope * (y - y0) for y in years],
        }
    )
    annual["source"] = annual["year"].map(
        lambda y: "Hitotsubashi anchor" if y in window_anchors else f"linear {y0}-{y1}"
    )
    anchor_df = pd.DataFrame(
        [{"year": y, "export_value_hkt": v, "source": "Hitotsubashi china_001.xlsx (CMC)"} for y, v in sorted(anchors.items())]
    )
    return annual, anchor_df


def build_report(silk: pd.DataFrame, anchors: pd.DataFrame, silver: pd.DataFrame) -> None:
    silk = silk.copy()
    silk["yoy_return"] = silk["export_value_hkt"].pct_change()
    silk_returns = silk["yoy_return"].dropna().tolist()
    silver = silver.copy()
    silver["yoy_return"] = silver["london_silver_usd_oz"].pct_change()

    merged = silk.merge(silver, on="year", how="inner", suffixes=("_silk", "_silver"))
    corr = merged["yoy_return_silk"].corr(merged["yoy_return_silver"])

    summary = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "window": "1912-1921",
        "extension_planned": "1920-12 to 1925 (securities; separate run)",
        "silk_sitc": SITC_RAW_SILK,
        "silk_anchors": anchors.to_dict(orient="records"),
        "silk": {
            "annual_vol_yoy": round(annual_vol(silk_returns), 4),
            "max_drawdown": round(max_drawdown(silk["export_value_hkt"].tolist()), 4),
            "peak_year": int(silk.loc[silk["export_value_hkt"].idxmax(), "year"]),
            "trough_year": int(silk.loc[silk["export_value_hkt"].idxmin(), "year"]),
        },
        "silver_london_nber_a04018": {
            "annual_vol_yoy": round(float(silver["yoy_return"].std()), 4),
            "max_drawdown": round(max_drawdown(silver["london_silver_usd_oz"].tolist()), 4),
            "peak_year": int(silver.loc[silver["london_silver_usd_oz"].idxmax(), "year"]),
        },
        "yoy_correlation_silk_vs_silver": round(float(corr), 4) if pd.notna(corr) else None,
        "pending": [
            "Ma-Zhao (2020) monthly yangli for domestic silver spread",
            "Mendeley 9s4wnsrb4r monthly London silver (replace annual NBER if needed)",
            "CMC quantity series for unit-price (value/qty) not just export value",
        ],
    }

    silk_out = silk[["year", "export_value_hkt", "yoy_return", "source"]].copy()
    silk_out["yoy_return"] = silk_out["yoy_return"].round(4)
    silk_out.to_csv(OUT / "silk_export_1912_1921.csv", index=False, encoding="utf-8-sig")
    silver.to_csv(OUT / "silver_london_1912_1921.csv", index=False, encoding="utf-8-sig")
    merged.to_csv(OUT / "merged_1912_1921.csv", index=False, encoding="utf-8-sig")
    (OUT / "summary_1912_1921.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    def _table(df: pd.DataFrame) -> str:
        cols = list(df.columns)
        lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
        for _, row in df.iterrows():
            lines.append("| " + " | ".join(str(row[c]) for c in cols) + " |")
        return "\n".join(lines)

    md = [
        "# 1912–1921 生絲＋倫敦銀價 pilot",
        "",
        f"**產生**：{summary['generated']}",
        "",
        "## 方法",
        "",
        f"- **生絲**：一橋大 `china_001.xlsx` 出口額，SITC **{SITC_RAW_SILK}**（生絲原料）；錨點年 {summary['silk_anchors']}，其餘年份線性插值。",
        "- **銀價**：NBER Macrohistory **A04018**（倫敦 bar silver，美元/盎司，年）。",
        "- **尚未納入**：Ma–Zhao 滬–津洋厘（月）。",
        "",
        "## 生絲出口額（海關兩，插值年序列）",
        "",
        _table(silk_out),
        "",
        f"- 年對年波動 σ：**{summary['silk']['annual_vol_yoy']:.2%}**",
        f"- 最大回撤：**{summary['silk']['max_drawdown']:.2%}**",
        "",
        "## 倫敦銀價（年）",
        "",
        _table(silver.round(4)),
        "",
        f"- 年對年波動 σ：**{summary['silver_london_nber_a04018']['annual_vol_yoy']:.2%}**",
        f"- 最大回撤：**{summary['silver_london_nber_a04018']['max_drawdown']:.2%}**",
        f"- 生絲 vs 銀價年對年相關：**{summary['yoy_correlation_silk_vs_silver']}**",
        "",
        "## 延伸（未跑）",
        "",
        "- **1920/12–1925**：上海華商證交所／橡皮股",
        "",
    ]
    (OUT / "report_1912_1921.md").write_text("\n".join(md), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def main() -> None:
    if not HITOU.exists():
        raise SystemExit(f"Missing {HITOU}; run fetch_silk_silver_data.py first")
    if not NBER_SILVER.exists():
        raise SystemExit(f"Missing {NBER_SILVER}; download NBER a04018.dat")
    silk, anchors = load_silk_export_hkt()
    silver = load_nber_silver()
    build_report(silk, anchors, silver)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()

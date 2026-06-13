import pandas as pd
from pathlib import Path

x = pd.ExcelFile(Path(r"d:\ETF\output\silk_silver\hitotsubashi_cn_trade_1913_1948.xlsx"))
out = Path(r"d:\ETF\output\silk_silver\xlsx_probe.txt")
lines = [f"sheets: {x.sheet_names}"]
for sh in x.sheet_names:
    df = pd.read_excel(x, sheet_name=sh)
    lines.append(f"\n=== {sh} shape {df.shape} ===")
    lines.append("columns: " + str(df.columns.tolist()[:8]))
    # find silk rows
    col0 = df.columns[0]
    mask = df[col0].astype(str).str.contains("silk|Silk|絲|丝", case=False, na=False)
    sub = df[mask]
    lines.append(f"silk rows: {len(sub)}")
    if len(sub):
        lines.append(sub.head(10).to_string())
    lines.append("\nfirst 15 rows:")
    lines.append(df.head(15).to_string())
out.write_text("\n".join(lines), encoding="utf-8")
print("wrote", out)

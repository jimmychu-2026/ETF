import pandas as pd
from pathlib import Path

path = Path(r"d:\ETF\output\silk_silver\hitotsubashi_cn_trade_1913_1948.xlsx")
df = pd.read_excel(path, sheet_name="輸出", header=None)
year_cols = []
for c in range(df.shape[1]):
    v = df.iloc[2, c]
    try:
        y = int(float(v))
        if 1900 < y < 1960:
            year_cols.append((c, y))
    except Exception:
        pass

rows = []
for i in range(3, len(df)):
    try:
        sitc = int(float(df.iloc[i, 0]))
    except Exception:
        continue
    for c, y in year_cols:
        val = df.iloc[i, c]
        try:
            v = float(val)
        except Exception:
            continue
        if v > 0:
            rows.append({"sitc": sitc, "year": y, "export_hkt": v})

out = pd.DataFrame(rows)
p = out.pivot(index="sitc", columns="year", values="export_hkt").fillna(0)
# top by 1913+1918 sum in range
sub = p[[c for c in p.columns if 1912 <= c <= 1921]]
sub["sum"] = sub.sum(axis=1)
top = sub.sort_values("sum", ascending=False).head(15)
Path(r"d:\ETF\output\silk_silver\sitc_pivot.txt").write_text(
    f"year_cols: {year_cols}\n\n{top.to_string()}\n\nall cols: {list(p.columns)}",
    encoding="utf-8",
)

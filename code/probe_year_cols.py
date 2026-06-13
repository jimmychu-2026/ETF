import pandas as pd
from pathlib import Path

df = pd.read_excel(
    Path(r"d:\ETF\output\silk_silver\hitotsubashi_cn_trade_1913_1948.xlsx"),
    sheet_name="輸出",
    header=None,
)
lines = []
lines.append("row1: " + str(df.iloc[1].tolist()[:30]))
lines.append("row2: " + str(df.iloc[2].tolist()[:30]))
# years every 4 cols from col 2?
for c in range(df.shape[1]):
    v = df.iloc[1, c]
    if pd.notna(v):
        try:
            y = int(float(v))
            if 1900 < y < 1960:
                lines.append(f"year col {c}: {y}")
        except Exception:
            pass
Path(r"d:\ETF\output\silk_silver\year_cols.txt").write_text("\n".join(lines), encoding="utf-8")

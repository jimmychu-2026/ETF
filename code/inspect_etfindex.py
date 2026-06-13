import json
from pathlib import Path

d = json.loads(Path(r"d:\ETF\output\etfindex_ix0179.json").read_text(encoding="utf-8"))
for k in ["result01", "result02", "result03"]:
    v = d.get(k)
    print(k, type(v).__name__, len(v) if hasattr(v, "__len__") else "")
    if isinstance(v, list) and v:
        print(json.dumps(v[0], ensure_ascii=False, indent=2)[:800])

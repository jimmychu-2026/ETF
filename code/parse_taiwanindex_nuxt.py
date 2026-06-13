import re
from pathlib import Path


def parse_taiwanindex_constituents(html: str) -> list[tuple[str, float, str]]:
    """Parse Taiwan Index NUXT payload for (stock_id, weight_pct, name)."""
    start = html.find("window.__NUXT__=")
    if start < 0:
        return []
    blob = html[start : start + 800000]

    # Modern NUXT JSON-like: stock_id:"2330", weight:1.23 or similar
    rows = re.findall(
        r'stock_id:"(\d{4,5})"[^}]{0,200}?weight:([0-9.]+)',
        blob,
    )
    if rows:
        return [(sid, float(wt), sid) for sid, wt in rows]

    rows = re.findall(
        r'stock_code:"(\d{4,5})"[^}]{0,200}?weight:([0-9.]+)',
        blob,
    )
    if rows:
        return [(sid, float(wt), sid) for sid, wt in rows]

    # Alternate: code + weight_per
    rows = re.findall(
        r'code:"(\d{4,5})"[^}]{0,300}?weight_per:([0-9.]+)',
        blob,
    )
    return [(sid, float(wt), sid) for sid, wt in rows]


def hhi_from_rows(rows: list[tuple[str, float, str]]) -> dict:
    if not rows:
        return {}
    wsum = sum(w for _, w, _ in rows)
    residual = max(0.0, 100.0 - wsum)
    weights = [w / 100 for w, _, _ in [(r[1], r[0], r[2]) for r in rows]]
    if residual > 0.01:
        weights.append(residual / 100)
    hhi = sum(x * x for x in weights)
    top = max(rows, key=lambda r: r[1])
    return {
        "n": len(rows),
        "wsum": wsum,
        "residual": residual,
        "hhi": hhi,
        "eff_n": 1 / hhi,
        "top_id": top[0],
        "top_pct": top[1],
    }


if __name__ == "__main__":
    for f in Path(r"d:\ETF\output").glob("idx_*.html"):
        html = f.read_text(encoding="utf-8")
        rows = parse_taiwanindex_constituents(html)
        stats = hhi_from_rows(rows)
        print(f.name, "rows", len(rows), stats)

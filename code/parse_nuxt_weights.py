import re
from pathlib import Path

DEBUG_NAMES = False

def _clean_name(name: str, stock_id: str = "") -> str:
    """Normalize noisy Yuanta NUXT name tokens into readable stock names.

    The PCF payload sometimes exposes placeholder-like tokens or short aliases
    (e.g. `ku (kE)`, `kp (kt)`) instead of the human-readable company name. We
    keep the original token when it already looks like a real name, but for
    suspicious short/garbled tokens we fall back to the stock id so downstream
    outputs stay interpretable.
    """
    name = name.strip().strip('"')
    if not name:
        return stock_id or name
    if re.search(r"[\u4e00-\u9fff]", name) or len(name) >= 6:
        return name
    if re.fullmatch(r"[A-Za-z0-9&\-\.\s]{1,5}", name):
        return stock_id or name
    return stock_id or name

    # If the token looks like a normal Chinese or alphanumeric company name,
    # keep it as-is.
    if re.search(r"[\u4e00-\u9fff]", name) or len(name) >= 6:
        return name

    # Yuanta payload can occasionally emit short alias tokens like `ku (kE)`.
    # Treat them as noise unless they clearly resemble a true listed name.
    if re.fullmatch(r"[A-Za-z0-9&\-\.\s]{1,5}", name):
        return stock_id or name

    return stock_id or name


def _debug_name_choice(stock_id: str, raw_name: str, cleaned_name: str, weight: float) -> None:
    if not DEBUG_NAMES:
        return
    if raw_name != cleaned_name:
        print(
            f"[YUANTA-NAME] id={stock_id} raw={raw_name!r} clean={cleaned_name!r} wt={weight:.2f}"
        )


def parse_yuanta_nuxt_weights(html: str) -> tuple[str, list[tuple[str, float, str]]]:
    """Return (posting_date, [(stock_id, weight_pct, stock_name_var)]) from Yuanta NUXT."""
    start = html.find("window.__NUXT__=")
    if start < 0:
        return "", []
    start += len("window.__NUXT__=")
    end = html.find(");</script>", start)
    nuxt = html[start:end] if end > start else html[start:]

    date_m = re.search(r"Posting Date[：:]\s*(\d{4}-\d{2}-\d{2})", html)
    as_of = date_m.group(1) if date_m else ""

    blocks = re.findall(
        r"\{code:([a-zA-Z0-9_$]+),ym:([a-zA-Z0-9_$]+),name:([a-zA-Z0-9_$]+),ename:([a-zA-Z0-9_$]+),weights:([0-9.]+),qty:([0-9]+)\}",
        nuxt,
    )
    if not blocks:
        return as_of, []

    # Resolve variable names via NUXT argument list
    func_m = re.match(r"\(function\(([^)]*)\)", nuxt)
    params = [p.strip() for p in func_m.group(1).split(",")] if func_m else []
    idx = nuxt.rfind("}(")
    args_str = nuxt[idx + 2 :].rstrip(")") if idx >= 0 else ""
    args = _split_js_args(args_str)
    mapping = dict(zip(params, args))

    rows: list[tuple[str, float, str]] = []
    for code_v, _ym, name_v, _en, wt, _qty in blocks:
        code = mapping.get(code_v, code_v).strip().strip('"')
        raw_name = mapping.get(name_v, name_v).strip().strip('"')
        name = _clean_name(raw_name, code)
        _debug_name_choice(code, raw_name, name, float(wt))
        rows.append((code, float(wt), name))
    return as_of, rows


def _split_js_args(s: str) -> list[str]:
    args: list[str] = []
    cur: list[str] = []
    in_str = False
    esc = False
    depth = 0
    for ch in s:
        if in_str:
            cur.append(ch)
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
            cur.append(ch)
            continue
        if ch in "{[(":
            depth += 1
        elif ch in "}])":
            depth = max(0, depth - 1)
        if ch == "," and depth == 0:
            token = "".join(cur).strip()
            if token:
                args.append(token)
            cur = []
        else:
            cur.append(ch)
    if cur:
        token = "".join(cur).strip()
        if token:
            args.append(token)
    return args


def hhi_from_weight_pcts(rows: list[tuple[str, float, str]]) -> dict:
    wsum = sum(w for _, w, _ in rows)
    residual = max(0.0, 100.0 - wsum)
    weights = [w / 100 for w, _, _ in [(r[1], r[0], r[2]) for r in rows]]
    if residual > 0.01:
        weights.append(residual / 100)
    hhi = sum(x * x for x in weights)
    top = max(rows, key=lambda r: r[1])
    return {
        "n_reported": len(rows),
        "weight_sum_pct": wsum,
        "residual_pct": residual,
        "hhi": hhi,
        "eff_n": 1 / hhi if hhi else float("nan"),
        "top_id": top[0],
        "top_name": top[2],
        "top_pct": top[1],
    }


if __name__ == "__main__":
    for f in ["pcf_0050.html", "pcf_0056.html"]:
        p = Path(r"d:\ETF\output") / f
        if not p.exists():
            continue
        html = p.read_text(encoding="utf-8")
        as_of, rows = parse_yuanta_nuxt_weights(html)
        stats = hhi_from_weight_pcts(rows)
        print(f, as_of, stats)

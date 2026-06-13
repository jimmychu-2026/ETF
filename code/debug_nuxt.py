import re

html = open(r"d:\ETF\output\pcf_0050.html", encoding="utf-8").read()
start = html.find("window.__NUXT__=") + len("window.__NUXT__=")
end = html.find("));</script>", start)
nuxt = html[start:end]
open_paren = nuxt.rfind("(")
args_str = nuxt[open_paren + 1 :]
print("nuxt len", len(nuxt), "args_str len", len(args_str))
print("args len", len(args_str))
codes = re.findall(r'"(\d{4})"', args_str)
print("quoted codes count", len(codes), codes[:20])
blob = nuxt[:500000]
blocks = re.findall(
    r"\{code:([a-zA-Z0-9_$]+),ym:([a-zA-Z0-9_$]+),name:([a-zA-Z0-9_$]+),ename:([a-zA-Z0-9_$]+),weights:([0-9.]+),qty:([0-9]+)\}",
    blob,
)
print("blocks", len(blocks))
print("top5", sorted([(float(b[4]), b[0]) for b in blocks], reverse=True)[:5])

# Build var->value map from args (positional params a,b,c,... at function start)
func_m = re.search(r"function\(([^)]*)\)", nuxt[:200])
params = [p.strip() for p in func_m.group(1).split(",")]
print("num params", len(params))

# Split args with a small state machine (respect strings)
args = []
cur = []
in_str = False
esc = False
depth = 0
for ch in args_str:
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
    elif ch in "}] )":
        if ch in "})" and depth == 0:
            token = "".join(cur).strip()
            if token:
                args.append(token)
            cur = []
            continue
        if ch in "}]":
            depth -= 1
    if ch == "," and depth == 0:
        token = "".join(cur).strip()
        if token:
            args.append(token)
        cur = []
    else:
        cur.append(ch)
if cur:
    args.append("".join(cur).strip())

print("parsed args", len(args), "params", len(params))
mapping = dict(zip(params, args))
for b in blocks[:3]:
    code_var = b[0]
    print("block", code_var, "->", mapping.get(code_var, "?"), "wt", b[4])

# resolve all blocks
resolved = []
for b in blocks:
    code = mapping.get(b[0], b[0]).strip('"')
    wt = float(b[4]) / 100.0
    resolved.append((code, wt))
print("resolved", len(resolved))
hhi = sum(w * w for _, w in resolved)
print("hhi from pcf weights", hhi)
print("sum w", sum(w for _, w in resolved))

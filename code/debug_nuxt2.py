import re

html = open(r"d:\ETF\output\pcf_0050.html", encoding="utf-8").read()
start = html.find("window.__NUXT__=") + len("window.__NUXT__=")
end = html.find("));</script>", start)
nuxt = html[start:end]

blocks = re.findall(
    r"\{code:([a-zA-Z0-9_$]+),ym:([a-zA-Z0-9_$]+),name:([a-zA-Z0-9_$]+),ename:([a-zA-Z0-9_$]+),weights:([0-9.]+),qty:([0-9]+)\}",
    nuxt,
)
print("standard blocks", len(blocks))
weights = [float(b[4]) for b in blocks]
print("sum weights", sum(weights))
hhi = sum((w / 100) ** 2 for w in weights)
print("hhi partial", hhi)

# other weight patterns
all_w = re.findall(r"weights:([0-9.]+)", nuxt)
print("all weights tags", len(all_w), "sum", sum(float(x) for x in all_w))

# find func params
func_m = re.match(r"\(function\(([^)]*)\)", nuxt)
params = func_m.group(1).split(",") if func_m else []
print("params", len(params))

# args: after final }(  pattern - nuxt ends with )) so find }( before last ))
idx = nuxt.rfind("}(")
print("idx", idx, "snippet", nuxt[idx : idx + 80])

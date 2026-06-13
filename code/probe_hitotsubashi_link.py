import re
import ssl
import urllib.request

url = "https://d-infra.ier.hit-u.ac.jp/Japanese/ltes/a000-asia-long-cn-trade.html"
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
html = urllib.request.urlopen(
    urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
    context=ctx,
    timeout=60,
).read().decode("utf-8", "replace")
for m in re.findall(r'href="([^"]+)"', html):
    if "xlsx" in m.lower():
        print(m)

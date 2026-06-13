import json
import ssl
import urllib.request

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.fhtrust.com.tw/api/ETFPcf"
payloads = [
    {"fundID": "00929", "pcfDate": "2026-06-06"},
    {"fundID": "00929", "pcfDate": "2026/06/06"},
]
for data in payloads:
    for as_json in [True, False]:
        if as_json:
            body = json.dumps(data).encode()
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0",
            }
        else:
            from urllib.parse import urlencode

            body = urlencode(data).encode()
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0",
            }
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
                out = resp.read()[:500]
                print("OK", as_json, data, out[:200])
        except Exception as e:
            print("ERR", as_json, data, str(e)[:80])

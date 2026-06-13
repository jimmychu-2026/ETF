#!/usr/bin/env python3
import json
import ssl
import urllib.request

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

BASE = "https://backend.taiwanindex.com.tw/api"

POSTS = [
    ("/IndexConstituent/GetLatestWeightList", {"indexCode": "IX0179", "lang": "tw"}),
    ("/IndexConstituent/GetLatestWeightList", {"indexNo": "IX0179"}),
    ("/IndexConstituent/GetLatestWeightList", {"indexId": "IX0179"}),
    ("/IndexConstituent/GetLatestWeightList", {"code": "IX0179"}),
    ("/IndexConstituent/GetLatestWeightList", {"indexCode": "IX0209"}),
    ("/IndexConstituent/GetLatestWeightList", {"indexCode": "IX0210"}),
    ("/IndexConstituent/GetLatestWeightList", {"indexCode": "IX0205"}),
    ("/IndexConstituent/GetWeightList", {"indexCode": "IX0179", "lang": "tw"}),
    ("/IndexConstituent/GetConstituentWeight", {"indexCode": "IX0179"}),
    ("/IndexConstituent/GetConstituent", {"indexCode": "IX0179"}),
    ("/Home/IndexConstituent", {"indexCode": "IX0179"}),
    ("/Home/GetIndexConstituent", {"indexCode": "IX0179"}),
]

GETS = [
    f"{BASE}/IndexConstituent/GetLatestWeightList?indexCode=IX0179",
    f"{BASE}/IndexConstituent/GetLatestWeightList?indexNo=IX0179",
    f"{BASE}/downloadFile/IndexConstituent/IX0179/tw",
    f"{BASE}/downloadFile/IndexConstituentWeight/IX0179/tw",
]

for path, payload in POSTS:
    url = BASE + path
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", "Accept": "application/json", "User-Agent": "Mozilla/5.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            out = resp.read().decode("utf-8", "replace")
            if out.lstrip().startswith(("{", "[")) and len(out) > 50:
                print("POST OK", path, payload, out[:250].replace("\n", " "))
    except Exception as e:
        err = str(e)
        if "404" not in err and "500" not in err:
            print("POST ERR", path, payload, err[:60])

for url in GETS:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            out = resp.read()
            if out[:4] == b"%PDF":
                print("GET PDF", url, len(out))
            else:
                text = out.decode("utf-8", "replace")
                if text.lstrip().startswith(("{", "[")) and len(text) > 50:
                    print("GET OK", url, text[:250].replace("\n", " "))
    except Exception as e:
        print("GET ERR", url.split("/")[-1], str(e)[:50])

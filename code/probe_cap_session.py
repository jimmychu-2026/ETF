#!/usr/bin/env python3
import http.cookiejar
import json
import re
import ssl
import urllib.request

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(cj),
    urllib.request.HTTPSHandler(context=CTX),
)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
    "Accept": "text/html,application/json,*/*",
}


def get(url):
    req = urllib.request.Request(url, headers=headers)
    with opener.open(req, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")


def post_json(url, payload):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={
            **headers,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Referer": "https://www.capitalfund.com.tw/etf/pcf/00919",
            "Origin": "https://www.capitalfund.com.tw",
        },
        method="POST",
    )
    with opener.open(req, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")


# Session: visit PCF page first
html = get("https://www.capitalfund.com.tw/etf/pcf/00919")
print("PCF page len", len(html))
print("cookies", [(c.name, c.value[:20]) for c in cj])

for pl in (
    {"fundNo": "195"},
    {"stocNo": "00919"},
    {"fundNo": "195", "stocNo": "00919"},
    {"fundNo": "195", "tradeDate": "2026/06/09"},
):
    try:
        body = post_json("https://www.capitalfund.com.tw/CFWeb/api/etf/buyback", pl)
        print(f"\nbuyback {pl}:")
        print(body[:2500])
        if "stocks" in body:
            open(r"d:\ETF\output\cap_buyback_session.json", "w", encoding="utf-8").write(body)
    except Exception as e:
        print(f"buyback ERR {pl}: {e}")

# Search capital js for external API base URLs
import sys
sys.path.insert(0, r"d:\ETF\code")
from compute_hhi_finmind import fetch_url

cap = fetch_url("https://www.capitalfund.com.tw/main.bdc1e85b555aa797.js")
urls = sorted(set(re.findall(r"https?://[a-zA-Z0-9._/-]+", cap)))
for u in urls:
    if "capital" in u.lower() or "125." in u or "api" in u.lower():
        print("URL", u)

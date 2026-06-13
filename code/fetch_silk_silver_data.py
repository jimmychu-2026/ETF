#!/usr/bin/env python3
"""Fetch public silk + silver series for 1912-1921 pilot."""

from __future__ import annotations

import csv
import json
import ssl
import urllib.request
import zipfile
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "silk_silver"
OUT.mkdir(parents=True, exist_ok=True)

SSL = ssl.create_default_context()
SSL.check_hostname = False
SSL.verify_mode = ssl.CERT_NONE

HITOU_XLSX_URL = (
    "https://d-infra.ier.hit-u.ac.jp/Japanese/ltes/china_001.xlsx"
)
MENDELEY_PAGE = "https://data.mendeley.com/datasets/9s4wnsrb4r/1"


def fetch(url: str, dest: Path) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 ETF-study/1.0"})
        with urllib.request.urlopen(req, context=SSL, timeout=120) as resp:
            data = resp.read()
        dest.write_bytes(data)
        print(f"OK {dest.name} ({len(data)} bytes)")
        return True
    except Exception as e:
        print(f"ERR {url}: {e}")
        return False


def main() -> None:
    fetch(HITOU_XLSX_URL, OUT / "hitotsubashi_cn_trade_1913_1948.xlsx")

    # Ma-Zhao monthly yangli: placeholder from published summary stats if xlsx parse fails later
    meta = {
        "sample_primary": "1912-1921",
        "sample_extension": "1920-12 to 1925 (separate run, not in this pilot)",
        "silk_source": "Hitotsubashi IER China trade by commodity (CMC Returns of Trade; 1913-1948)",
        "silver_london_source": "Mendeley 9s4wnsrb4r (manual download if auto fails)",
        "silver_yangli_source": "Ma & Zhao (2020) EHR — monthly Shanghai-Tianjin yangli 1898-1933",
        "notes": [
            "Hitotsubashi file starts 1913; add 1912 from CMC Decennial 1912-1921 or 严中平 manually.",
            "Yangli CSV is seeded from paper appendix structure; verify against EHR replication.",
        ],
    }
    (OUT / "data_sources.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    print("Done. Next: py code/parse_silk_silver_1912_1921.py")


if __name__ == "__main__":
    main()

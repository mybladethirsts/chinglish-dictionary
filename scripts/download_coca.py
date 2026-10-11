# -*- coding: utf-8 -*-
"""批量下载 COCA 20000 词表 101 个分片（llt22/coca-vocabulary-20000）。"""
import os, time, urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "..", "data", "raw")
OUT = os.path.join(RAW, "coca")
os.makedirs(OUT, exist_ok=True)

COCA_BASE = "https://raw.githubusercontent.com/llt22/coca-vocabulary-20000/main/vocabulary/"

def build_name(i):
    lo = (i - 1) * 200 + 1
    hi = i * 200
    return f"part{i:03d}_{lo}-{hi}.md"

ok = skip = fail = 0
for i in range(1, 102):
    name = build_name(i)
    path = os.path.join(OUT, name)
    if os.path.exists(path) and os.path.getsize(path) > 0:
        skip += 1
        continue
    url = COCA_BASE + name
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            with open(path, "wb") as f:
                f.write(data)
            ok += 1
            break
        except Exception as e:
            if attempt == 2:
                fail += 1
                with open(os.path.join(RAW, "coca_download.log"), "a", encoding="utf-8") as lg:
                    lg.write(f"{name}: {e}\n")
            time.sleep(2)

with open(os.path.join(RAW, "coca_download.log"), "a", encoding="utf-8") as lg:
    lg.write(f"SUMMARY ok={ok} skip={skip} fail={fail}\n")

# -*- coding: utf-8 -*-
"""检查数据源文件状态：是否存在、大小、内容样例。"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "..", "data", "raw")

def report(name, path, mode="text", n=3):
    if not os.path.exists(path):
        print(f"[MISS] {name}: {path}")
        return
    size = os.path.getsize(path)
    print(f"[OK]   {name}: {size:,} bytes")
    if mode == "text" and size < 200 * 1024 * 1024:
        with open(path, encoding="utf-8", errors="replace") as f:
            lines = [next(f, "").rstrip("\n") for _ in range(n)]
        for ln in lines[:n]:
            print("       |", ln[:160])

report("cedict.txt", os.path.join(RAW, "cedict.txt"))
report("changyongci.pdf", os.path.join(RAW, "changyongci.pdf"), mode="pdf")
report("tongyong_gfb.pdf", os.path.join(RAW, "tongyong_gfb.pdf"), mode="pdf")
report("Unihan.zip", os.path.join(RAW, "Unihan.zip"))

unihan_dir = os.path.join(RAW, "unihan")
if os.path.isdir(unihan_dir):
    files = sorted(os.listdir(unihan_dir))
    print(f"[OK]   unihan/ : {len(files)} files -> {', '.join(files)}")
else:
    print(f"[MISS] unihan/ directory")

# CC-CEDICT 行数统计
p = os.path.join(RAW, "cedict.txt")
if os.path.exists(p):
    cnt = 0
    with open(p, encoding="utf-8", errors="replace") as f:
        for _ in f:
            cnt += 1
    print(f"[INFO] cedict lines: {cnt}")

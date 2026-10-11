# -*- coding: utf-8 -*-
"""解压 CC-CEDICT 并检查两个 PDF 的文本层结构。结果写入日志文件。"""
import gzip, os, sys, traceback

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "..", "data", "raw")
LOG = os.path.join(BASE, "unpack_log.txt")

log_lines = []
def log(msg):
    log_lines.append(str(msg))
    print(msg)

try:
    # 1) 解压 CC-CEDICT
    gz = os.path.join(RAW, "cedict.txt.gz")
    out = os.path.join(RAW, "cedict.txt")
    if not os.path.exists(out):
        with gzip.open(gz, "rb") as f, open(out, "wb") as o:
            o.write(f.read())
        log(f"decompressed: {out} {os.path.getsize(out)} bytes")
    else:
        log(f"cedict.txt exists: {os.path.getsize(out)} bytes")

    # 2) 检查常用词表 PDF
    import pdfplumber
    p = pdfplumber.open(os.path.join(RAW, "changyongci.pdf"))
    log(f"changyongci pages: {len(p.pages)}")
    t = p.pages[0].extract_text()
    log(f"page0 text: {repr(t[:300]) if t else 'NO TEXT LAYER'}")
    p.close()

    # 3) 检查通用规范汉字表 PDF（大文件）
    p2 = pdfplumber.open(os.path.join(RAW, "tongyong_gfb.pdf"))
    log(f"tongyong_gfb pages: {len(p2.pages)}")
    t2 = p2.pages[0].extract_text()
    log(f"page0 text: {repr(t2[:300]) if t2 else 'NO TEXT LAYER'}")
    p2.close()
except Exception as e:
    log("ERROR: " + repr(e))
    log(traceback.format_exc())

with open(LOG, "w", encoding="utf-8") as f:
    f.write("\n".join(log_lines))

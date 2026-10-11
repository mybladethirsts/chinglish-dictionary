# -*- coding: utf-8 -*-
"""
英语补齐层：解析 COCA 20000 词表分片（llt22 仓库 md），
与中文侧（字层英文释义 + 词层英文释义）比对，输出未被覆盖的常用英语词 → 英→中反查条目。
"""
import csv, json, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "..", "data", "raw")
OUT = os.path.join(BASE, "..", "data", "out")
COCA_DIR = os.path.join(RAW, "coca")

log = []
def L(msg): log.append(str(msg))

# ---------- 1) 解析 COCA md 分片 ----------
entries = []
files = sorted(f for f in os.listdir(COCA_DIR) if f.startswith("part") and f.endswith(".md"))
for fn in files:
    with open(os.path.join(COCA_DIR, fn), encoding="utf-8") as f:
        lines = [ln.rstrip("\n") for ln in f]
    i = 0
    n = len(lines)
    while i < n:
        ln = lines[i].strip()
        m = re.match(r"^(\d+)[\s]+(\S+)\s*$", ln)
        if m:
            rank = int(m.group(1))
            word = m.group(2)
            definition = ""
            j = i + 1
            while j < n and lines[j].strip():
                line = lines[j].strip()
                if (line.startswith("- ") and ('"' in line) and "http" not in line
                        and "人人词典" not in line and "柯林斯" not in line and "朗文" not in line):
                    definition = line[2:].strip()
                j += 1
            entries.append({"rank": rank, "word": word, "chinese": definition})
            i = j
        else:
            i += 1
L(f"[1] COCA 解析: {len(entries)} 词 (范围 rank {entries[0]['rank']}-{entries[-1]['rank']})")

# ---------- 2) 中文侧英文释义 → 已覆盖英文词集合 ----------
master = json.load(open(os.path.join(OUT, "master_core.json"), encoding="utf-8"))
texts = []
for w in master["words"]:
    texts.append(w["english"])
for c in master["chars"]:
    texts.append(c["english"])
texts = " ".join(texts).lower()
covered = set(re.findall(r"[a-z][a-z'\-]*", texts))
L(f"[2] 中文侧释义词汇: {len(covered)} 个不同英文词")

# ---------- 3) 未覆盖的 COCA 常用词 → 英语补齐层 ----------
missing = []
for e in entries:
    if e["word"].lower() not in covered and e["chinese"].strip():
        missing.append({
            "word": e["word"],
            "rank": e["rank"],
            "chinese": e["chinese"],
            "source": "coca",
        })
L(f"[3] 未覆盖常用英语词: {len(missing)} (已覆盖 {len(entries)-len(missing)}/{len(entries)})")

# ---------- 4) 输出 ----------
with open(os.path.join(OUT, "english_layer.json"), "w", encoding="utf-8") as f:
    json.dump({"meta": {"name": "中式英语词典-英语补齐层", "version": "0.1",
                        "total_coca": len(entries), "covered": len(entries) - len(missing),
                        "missing": len(missing)},
               "words": missing}, f, ensure_ascii=False, indent=1)
L(f"[4] english_layer.json: {os.path.getsize(os.path.join(OUT,'english_layer.json')):,} bytes")

with open(os.path.join(OUT, "english_layer.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["word", "rank", "chinese", "source"])
    w.writeheader()
    w.writerows(missing)
L(f"[4] english_layer.csv: {os.path.getsize(os.path.join(OUT,'english_layer.csv')):,} bytes")

with open(os.path.join(OUT, "english_build_log.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(log))
print("\n".join(log))

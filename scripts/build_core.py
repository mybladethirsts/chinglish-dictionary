# -*- coding: utf-8 -*-
"""
核心层构建：汉字层（通用规范汉字表一二级 6500 字 + Unihan 释义/拼音）
+ 词层（CC-CEDICT 简体词条 + jieba 词频分层）。
输出统一 JSON/CSV 到 data/out/。
"""
import csv, json, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "..", "data", "raw")
OUT = os.path.join(BASE, "..", "data", "out")
os.makedirs(OUT, exist_ok=True)

log = []
def L(msg):
    log.append(str(msg))

# ---------- 1) 通用规范汉字表：8105 字，前3500一级 / 3501-6500二级 / 6501+三级 ----------
chars = []
with open(os.path.join(RAW, "tongyong-guifan-han.txt"), encoding="utf-8") as f:
    lines = [ln.strip() for ln in f if ln.strip()]
# 仅保留单字行（滤掉 YAML 头与说明行），再按顺序编号
single_chars = [ln for ln in lines if len(ln) == 1]
for i, ch in enumerate(single_chars, start=1):
    level = 1 if i <= 3500 else (2 if i <= 6500 else 3)
    chars.append({"char": ch, "level": level, "rank": i})
L(f"[1] 字表解析: {len(chars)} 字 (一级{sum(1 for c in chars if c['level']==1)}, 二级{sum(1 for c in chars if c['level']==2)}, 三级{sum(1 for c in chars if c['level']==3)})")

# ---------- 2) Unihan：kMandarin/kHanyuPinlu(拼音) + kDefinition(英文释义) ----------
def load_unihan(filename, field):
    """返回 {char: value}"""
    d = {}
    p = os.path.join(RAW, "unihan", filename)
    with open(p, encoding="utf-8") as f:
        for ln in f:
            if not ln.startswith("U+"):
                continue
            parts = ln.rstrip("\n").split("\t")
            if len(parts) >= 3 and parts[1] == field:
                try:
                    ch = chr(int(parts[0][2:], 16))
                except ValueError:
                    continue
                d[ch] = parts[2]
    return d

kdef = load_unihan("Unihan_Readings.txt", "kDefinition")
kmand = load_unihan("Unihan_Readings.txt", "kMandarin")
kpinlu = load_unihan("Unihan_Readings.txt", "kHanyuPinlu")
L(f"[2] Unihan: kDefinition {len(kdef)}, kMandarin {len(kmand)}, kHanyuPinlu {len(kpinlu)}")

def pinyin_for(ch):
    if ch in kmand:
        # kMandarin 如 "yī" 或 "yī, qí" —— 取全
        return kmand[ch]
    return ""

def freq_for(ch):
    # kHanyuPinlu 如 "yi1(99999) ji4(123)" —— 取最大频次
    v = kpinlu.get(ch, "")
    if not v:
        return 0
    m = re.findall(r"\((\d+)\)", v)
    return max((int(x) for x in m), default=0)

# ---------- 3) CC-CEDICT 词层 ----------
words = []
cedict_re = re.compile(r"^(\S+) (\S+) \[([^\]]+)\] /(.+)/$")
with open(os.path.join(RAW, "cedict.txt"), encoding="utf-8") as f:
    for ln in f:
        if ln.startswith("#"):
            continue
        m = cedict_re.match(ln.strip())
        if not m:
            continue
        trad, simp, pinyin, defs = m.groups()
        words.append({"word": simp, "trad": trad, "pinyin": pinyin, "english": defs})
L(f"[3] CC-CEDICT: {len(words)} 词条")

# ---------- 4) jieba 词频 ----------
freq_map = {}
with open(os.path.join(RAW, "jieba_dict.txt"), encoding="utf-8") as f:
    for ln in f:
        parts = ln.strip().split()
        if len(parts) >= 2:
            freq_map[parts[0]] = int(parts[1])
L(f"[4] jieba 词频: {len(freq_map)} 词")

# ---------- 5) 组装输出 ----------
# 字层：一二级 6500 字
char_rows = []
for c in chars:
    if c["level"] > 2:
        continue
    ch = c["char"]
    char_rows.append({
        "char": ch,
        "pinyin": pinyin_for(ch),
        "english": kdef.get(ch, ""),
        "level": c["level"],
        "rank": c["rank"],
        "freq": freq_for(ch),
        "source": "unihan",
    })
L(f"[5] 字层(一二级): {len(char_rows)} 字, 有释义 {sum(1 for r in char_rows if r['english'])}")

# 词层：CC-CEDICT 全部简体词条 + jieba 词频
word_rows = []
for w in words:
    word_rows.append({
        "word": w["word"],
        "trad": w["trad"],
        "pinyin": w["pinyin"],
        "english": w["english"],
        "freq": freq_map.get(w["word"], 0),
        "source": "cc-cedict",
    })
L(f"[5] 词层: {len(word_rows)} 词条, 有词频 {sum(1 for r in word_rows if r['freq']>0)}")

# ---------- 6) 写出 JSON + CSV ----------
def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    L(f"[6] {os.path.basename(path)}: {len(data)} 条, {os.path.getsize(path):,} bytes")

def write_csv(path, rows, cols):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    L(f"[6] {os.path.basename(path)}: {len(rows)} 条, {os.path.getsize(path):,} bytes")

write_json(os.path.join(OUT, "char_layer.json"), char_rows)
write_csv(os.path.join(OUT, "char_layer.csv"), char_rows,
          ["char", "pinyin", "english", "level", "rank", "freq", "source"])
write_json(os.path.join(OUT, "word_layer.json"), word_rows)
write_csv(os.path.join(OUT, "word_layer.csv"), word_rows,
          ["word", "trad", "pinyin", "english", "freq", "source"])

# 合并主文件（核心层）
master = {"meta": {"name": "中式英语词典-核心层", "version": "0.1",
                   "char_count": len(char_rows), "word_count": len(word_rows)},
          "chars": char_rows, "words": word_rows}
with open(os.path.join(OUT, "master_core.json"), "w", encoding="utf-8") as f:
    json.dump(master, f, ensure_ascii=False, indent=1)
L(f"[6] master_core.json: {os.path.getsize(os.path.join(OUT,'master_core.json')):,} bytes")

with open(os.path.join(OUT, "build_log.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(log))
print("\n".join(log))

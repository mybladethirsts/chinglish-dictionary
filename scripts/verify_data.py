# -*- coding: utf-8 -*-
"""验证：数据质量抽查 + data.js 有效性。"""
import json, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "..", "data", "out")
WEB = os.path.join(BASE, "..", "web")

def L(msg): print(msg)

# 1) 字层抽查
chars = json.load(open(os.path.join(OUT, "char_layer.json"), encoding="utf-8"))
cmap = {c["char"]: c for c in chars}
L("== 字层抽查 ==")
for ch in ["我", "你", "好", "打", "说", "的", "一"]:
    c = cmap.get(ch)
    if c:
        L(f"  {ch} [{c['pinyin']}] {c['english'][:80]} (级{c['level']})")
    else:
        L(f"  {ch} 缺失!")

# 2) 词层抽查
words = json.load(open(os.path.join(OUT, "word_layer.json"), encoding="utf-8"))
wmap = {w["word"]: w for w in words}
L("== 词层抽查 ==")
for w in ["加油", "中国", "时间", "吃饭", "厉害", "人山人海"]:
    e = wmap.get(w)
    if e:
        L(f"  {w} [{e['pinyin']}] freq={e['freq']} :: {e['english'][:80]}")
    else:
        L(f"  {w} 未在词层 (可能不在 CC-CEDICT)")

# 3) 特色层抽查
ce = json.load(open(os.path.join(OUT, "chinglish_layer.json"), encoding="utf-8"))["entries"]
L(f"== 特色层 = {len(ce)} 条 ==")
for e in ce[:6]:
    L(f"  {e['chinglish']} | {e['chinese']} | {e['status']} | {e['origin'][:40]}")

# 4) 英语层抽查
en = json.load(open(os.path.join(OUT, "english_layer.json"), encoding="utf-8"))["words"]
L(f"== 英语补齐层 = {len(en)} 词 ==")
for e in en[:5]:
    L(f"  #{e['rank']} {e['word']} :: {e['chinese'][:60]}")

# 5) data.js JSON 有效性
src = open(os.path.join(WEB, "data.js"), encoding="utf-8").read()
m = re.search(r"window\.DICT_DATA = (\{.*\});\s*$", src, re.S)
if m:
    d = json.loads(m.group(1))
    L(f"== data.js OK = chars {d['meta']['char_count']}, words {d['meta']['word_count']}, chinglish {d['meta']['chinglish_count']}, english {d['meta']['english_count']} ==")
else:
    L("data.js 格式错误!")

# 6) 总条目
L(f"== 总计 = 字 {len(chars)} + 词 {len(words)} + 特色 {len(ce)} + 英语 {len(en)} = {len(chars)+len(words)+len(ce)+len(en)} ==")

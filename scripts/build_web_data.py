# -*- coding: utf-8 -*-
"""
网页数据打包：从各层 JSON 生成 web/data.js（供本地 HTML 直接引用，file:// 可用）。
词层按 jieba 词频截取高频常用子集，控制体积。
"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "..", "data", "out")
WEB = os.path.join(BASE, "..", "web")
os.makedirs(WEB, exist_ok=True)

# 1) 字层（全量 6500）
chars = json.load(open(os.path.join(OUT, "char_layer.json"), encoding="utf-8"))

# 2) 词层：按 freq 降序截取 top 30000（freq>0 优先，其余按拼音序补足）
words = json.load(open(os.path.join(OUT, "word_layer.json"), encoding="utf-8"))
words_sorted = sorted(words, key=lambda w: -w["freq"])
top_words = words_sorted[:30000]
print("word layer: total", len(words), "-> web subset", len(top_words))

# 3) 特色层
chinglish = json.load(open(os.path.join(OUT, "chinglish_layer.json"), encoding="utf-8"))["entries"]

# 4) 英语补齐层
english = json.load(open(os.path.join(OUT, "english_layer.json"), encoding="utf-8"))["words"]
print("english layer:", len(english))

# 5) 句型层（中文语序 ↔ 标准英语）
sent = json.load(open(os.path.join(OUT, "sentence_layer.json"), encoding="utf-8"))
sentences = sent["entries"]
patterns = sent["patterns"]
print("sentence layer:", len(sentences), "entries /", len(patterns), "patterns")

# 6) 组装 data.js
meta = {
    "name": "中式英语词典（Chinglish Dictionary）",
    "version": "0.3",
    "char_count": len(chars),
    "word_count": len(top_words),
    "chinglish_count": len(chinglish),
    "english_count": len(english),
    "sentence_count": len(sentences),
    "built": "2026-10-13",
}
data = {"meta": meta, "chars": chars, "words": top_words,
        "chinglish": chinglish, "english": english,
        "patterns": patterns, "sentences": sentences}

js = "/* 中式英语词典 web 数据（由 build_web_data.py 生成） */\n"
js += "window.DICT_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n"

with open(os.path.join(WEB, "data.js"), "w", encoding="utf-8") as f:
    f.write(js)
print("data.js:", os.path.getsize(os.path.join(WEB, "data.js")), "bytes")

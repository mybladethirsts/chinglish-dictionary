# -*- coding: utf-8 -*-
"""
句型层构建：读 data/sentences.json（中文语序 ↔ 标准英语句型对），
输出 data/out/sentence_layer.json / .csv。
"""
import csv, json, os

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "..", "data", "sentences.json")
OUT = os.path.join(BASE, "..", "data", "out")

with open(SRC, encoding="utf-8") as f:
    src = json.load(f)

entries = src["entries"]
patterns = src["patterns"]
meta = {
    "name": src["meta"]["name"],
    "version": src["meta"]["version"],
    "entry_count": len(entries),
    "pattern_count": len(patterns),
}

out_data = {"meta": meta, "patterns": patterns, "entries": entries}

with open(os.path.join(OUT, "sentence_layer.json"), "w", encoding="utf-8") as f:
    json.dump(out_data, f, ensure_ascii=False, indent=1)

with open(os.path.join(OUT, "sentence_layer.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["id", "zh", "chinglish", "standard", "pattern", "notes"])
    w.writeheader()
    w.writerows(entries)

print("sentence_layer:", len(entries), "entries /", len(patterns), "patterns ->",
      os.path.getsize(os.path.join(OUT, "sentence_layer.json")), "bytes")

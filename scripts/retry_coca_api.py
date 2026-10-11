# -*- coding: utf-8 -*-
"""用 GitHub Contents API 下载缺失的 COCA 分片（base64 解码）。"""
import base64, json, os, time, urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "..", "data", "raw")
COCA_DIR = os.path.join(RAW, "coca")
MISSING = [
    "part012_2201-2400.md", "part018_3401-3600.md", "part045_8801-9000.md",
    "part063_12401-12600.md", "part072_14201-14400.md", "part076_15001-15200.md",
    "part077_15201-15400.md", "part079_15601-15800.md", "part084_16601-16800.md",
    "part087_17201-17400.md", "part090_17801-18000.md", "part092_18201-18400.md",
    "part098_19401-19600.md",
]
log = []
ok = fail = 0
for name in MISSING:
    path = os.path.join(COCA_DIR, name)
    if os.path.exists(path) and os.path.getsize(path) > 100:
        log.append(f"skip {name}")
        continue
    url = f"https://api.github.com/repos/llt22/coca-vocabulary-20000/contents/vocabulary/{name}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github+json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            j = json.load(r)
        if j.get("encoding") == "base64":
            data = base64.b64decode(j["content"])
            with open(path, "wb") as f:
                f.write(data)
            ok += 1
            log.append(f"OK {name} {len(data)} bytes")
        else:
            # 超过大小限制返回 download_url
            dl = j.get("download_url")
            if dl:
                with urllib.request.urlopen(urllib.request.Request(dl, headers={"User-Agent": "Mozilla/5.0"}), timeout=60) as r:
                    data = r.read()
                with open(path, "wb") as f:
                    f.write(data)
                ok += 1
                log.append(f"OK(dl) {name} {len(data)} bytes")
            else:
                fail += 1
                log.append(f"FAIL {name}: no content")
    except Exception as e:
        fail += 1
        log.append(f"FAIL {name}: {e}")
    time.sleep(1.2)

with open(os.path.join(RAW, "coca_api_download.log"), "w", encoding="utf-8") as f:
    f.write("\n".join(log) + f"\nSUMMARY ok={ok} fail={fail}\n")

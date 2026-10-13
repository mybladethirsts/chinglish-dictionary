# 中式英语词典 · Chinglish Dictionary

> 记录中式英语，而不是消灭它。
> **Record Chinglish, don't "fix" it.**

双语对照词典数据 + 离线查询工具：常用汉字、常用汉语词、中式英语特色词条、常用英语词、**句型对照（中文语序 ↔ 标准英语）**，支持中英双向查询。

灵感来自网络爆文「英国项目经理发现中式英语完胜标准英语」：中式英语剥去语法装饰后表意直白高效（如 *"Yesterday we discuss already, today we just confirm."*）。本仓库把它做成结构化、可查询、可持续扩充的语言观察数据。

## Who is this for?（这个仓库给谁看）

**Two audiences, one dataset:**

| 受众 | 场景 | 在仓库里看什么 |
|---|---|---|
| **English speakers**（优先） | 想知道「同一句英文，中文语序怎么说」 | 句型层 180 条对照：标准英语句 → 中文语序直译 → 中文原文 + 15 类语序模式说明（时间前置 / 时态由时间词表达 / 系词省略 / 话题置顶 / 量词 / no+动词否定 / 因为…所以… 等） |
| **Chinese speakers**（中文母语者） | 想按中文语序把英文说出来 | 字层 6500 汉字 + 词层 12.5 万常用词的中英释义；先按中文语序直译开口，再对照标准表达 |
| **语言研究者 / 内容创作者** | 引用、对比、扩展数据 | 开源数据底座（各层 JSON/CSV）+ 特色词条 38 条，可持续扩充 |

## Scale（总计约 13.4 万条目 + 180 句型）

| 层 | 内容 | 数量 | 数据源 | 授权 |
|---|---|---|---|---|
| 汉字层 | 一二级 6500 字：拼音 + 英文释义 + 级别 + 频次 | 6,500 | 《通用规范汉字表》+ Unihan kDefinition/kMandarin/kHanyuPinlu | 字表政府公开；Unihan 宽松许可 |
| 词层 | 常用汉语词：拼音 + 词性 + 英文释义 + 词频 | 125,262（全量）/ 网页工具含高频 3 万 | CC-CEDICT 12.5 万词条 + jieba 词频 | CC BY-SA 4.0（衍生须开源共享） |
| 特色层 | 中式英语词条：中 → 字面直译 → 规范译 → 出处/状态 | 38（首批） | 人工整理（皮钦英语、中文借词、网络梗、标语误译） | 本项目原创 |
| 英语层 | COCA 前 20200 中未被中文侧覆盖的常用词（英→中反查） | 2,006 | COCA 20000 开源整理版（llt22/coca-vocabulary-20000） | 开源整理数据 |
| **句型层** | **标准英语句 ↔ 中文语序直译 ↔ 中文原文 + 语序模式说明** | **180（15 类模式）** | 人工整理（基于常见中介语特征与高频表达） | 本项目原创 |

覆盖情况：COCA 前 20200 常用英语词中，18,022 个（约 89%）已被中文侧释义覆盖，2,006 个未覆盖词收入英语补齐层。

## Sentence layer（句型层，本仓库核心新资产）

For English speakers: **how would the same English sentence be said if you kept the Chinese word order?** Each entry has three lines:

```
中文：  昨天我们讨论过了，今天只是确认一下。
中文语序：Yesterday we discuss already, today we just confirm.
标准英语：We already discussed it yesterday; today we're just confirming.
```

15 类中文语序模式（每类 12 条）：时间状语前置、时态由时间词表达、系动词省略、话题置顶、连动结构、量词直译、介词直译/省略、no+动词否定、副词位置、因为…所以…双关联词、名词不标复数、冠词省略、完成靠 already/done、情态直译、语气词直译。

## 定位（为什么值得做）

公开领域没有直接对标项目（GitHub 上 62 个 chinglish 相关仓库无一为词典）。现有类似物分五类：

- 标准中英词典（CC-CEDICT 全家桶、WantWords、Syng 等）：无中式英语特色词条，更无「中文语序 ↔ 标准英语」句型对照
- 搞笑标语汇编（Radtke《Chinglish: Found in Translation》等）：非结构化数据
- 学术语料库（CCAE、CCE、iWrite 等）：研究用途，非词典
- 「消灭中式英语」工具（改写匠、Ries.AI、WordsTalk 等）：方向与本项目相反
- 谐音/生成器娱乐 App（拆个梨洗等）：非词典

本项目的交集「记录 + 数据化 + 词典 + 句型对照」目前无人占位；方法论先例是 Singlish 词典（1783 条，LLM 起草 + 人工校审，CC-BY-SA 开源）。

## 目录结构

```
chinglish-dictionary/
├── web/                 # 网页查询工具（双击 index.html 即可用）
│   ├── index.html       # 双向搜索（查中文 / 查英文）+ 句型对照库 + 特色词条
│   └── data.js          # 打包数据（高频 3 万词 + 6500 字 + 特色 + 英语层 + 180 句型）
├── data/
│   ├── sentences.json   # 句型层源数据（180 条，可直接编辑扩展）
│   └── out/             # 产物（raw 原始数据不上传，重建命令见下）
│       ├── char_layer.json / .csv        # 字层
│       ├── word_layer.json / .csv        # 词层（全量 12.5 万）
│       ├── chinglish_layer.json / .csv   # 特色层
│       ├── english_layer.json / .csv     # 英语层
│       ├── sentence_layer.json / .csv    # 句型层（180 条 / 15 模式）
│       └── master_core.json              # 字层+词层合并主数据
├── scripts/             # 构建脚本（Python，标准库即可）
│   ├── build_core.py        # 字层+词层构建
│   ├── build_english.py     # 英语补齐层构建
│   ├── build_chinglish.py   # 特色层构建（扩展特色词条改这里）
│   ├── build_sentences.py   # 句型层构建（读 data/sentences.json）
│   ├── build_web_data.py    # 网页数据打包
│   ├── download_coca.py / retry_coca_api.py  # COCA 下载
│   ├── unpack_sources.py / check_sources.py  # 数据源检查
│   └── verify_data.py       # 数据验证
├── LICENSE               # 代码 MIT
├── LICENSE-DATA.txt      # 数据 CC BY-SA 4.0
└── README.md
```

## 使用方式

1. **网页工具**：浏览器打开 `web/index.html`（与 `web/data.js` 同目录），离线可用。
   - 查中文：输入汉字/词语/中文句子片段 → 命中字、词、特色词条、**句型中文原文**
   - 查英文：输入英文单词/句子 → 命中词层释义、英语层、特色词条、**句型标准句**（并展示其中文语序直译版）
   - 句型对照库：按 15 类中文语序模式分组浏览 180 条「中文原文 → 中文语序直译 → 标准英语」
2. **数据文件**：`data/out/` 下各层 JSON/CSV；句型层源数据直接编辑 `data/sentences.json` 后运行 `build_sentences.py` 重建。

### 统一字段

| 字段 | 说明 |
|---|---|
| char / word / chinglish / word(en) | 词条主词 |
| pinyin | 拼音（字/词层） |
| english | 英文释义（字/词层） |
| chinese | 中文释义（英语层/特色层） |
| literal / standard | 字面直译 / 规范译法（特色层） |
| status | adopted=已入英语, calque=直译借入, net=网络流行, sign=标语误译（特色层） |
| origin / example | 出处说明 / 例句（特色层） |
| level / rank | 字表级别（1/2/3）/ 字表序位 |
| freq | 频次（字层=Unihan 拼音频次；词层=jieba 词频） |
| source | 数据源 |
| zh / chinglish / standard / pattern / notes | 句型层：中文原文 / 中文语序直译 / 标准英语 / 模式 ID / 说明 |

## 授权

- **代码与网页工具**：MIT（见 LICENSE）
- **数据**：CC BY-SA 4.0（见 LICENSE-DATA.txt）。因含 CC-CEDICT 衍生数据，公开分享须保持同授；特色层、句型层为本项目原创整理，一并按 CC BY-SA 4.0 开放
- **数据源**：Unihan（Unicode License 宽松）；CC-CEDICT（CC BY-SA 4.0）；COCA 开源整理版 llt22/coca-vocabulary-20000；jieba 词频（MIT）；《通用规范汉字表》政府公开

## 已知限制与后续

- 官方《现代汉语常用词表（草案）》（56008 词）PDF 为图片型无文本层，无法机器解析；词层改用 CC-CEDICT 全量（覆盖所有常用词并自带英文释义）+ jieba 词频分层
- COCA 20200 词中 5 个因分片格式变体未解析（影响极小）；个别特殊词形（缩略/拟声）释义为空已过滤
- 字层 6500 字中 15 个字 Unihan 无英文释义（生僻二级字），已标「释义待补」
- 特色层首批 38 条、句型层首批 180 条，按 Singlish 词典模式持续扩充（网络收集 + LLM 起草 + 人工校审）
- 后续可加：HSK 3.0 分级标记、例句库、繁体字关联、小程序接入（数据底座即 `data/out/`）

## 重建

原始数据（Unihan、CC-CEDICT、字表、COCA 分片）从各自上游下载到 `data/raw/` 后：

```powershell
python scripts\build_core.py        # 字层+词层
python scripts\build_english.py     # 英语层（需 raw/coca 分片齐全）
python scripts\build_chinglish.py   # 特色层
python scripts\build_sentences.py   # 句型层
python scripts\build_web_data.py    # 打包 web/data.js
python scripts\verify_data.py       # 数据验证
```

依赖：核心构建仅用 Python 标准库（pdfplumber、pandas 仅数据源检查时可选）。

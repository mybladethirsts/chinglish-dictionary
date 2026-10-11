# 中式英语词典（Chinglish Dictionary）

> 记录中式英语，而不是消灭它。
> 把「汉字 ↔ 英文」与「中式英语特色词条」做成一套开源数据 + 离线查询工具。

双语对照词典数据 + 本地离线查询工具。覆盖：常用汉字、常用汉语词、中式英语特色词条、常用英语词，支持中英双向查询。灵感来自「英国项目经理发现中式英语完胜标准英语」的网络爆文——它指出中式英语剥去语法装饰后表意直白高效。本仓库把它做成结构化、可查询、可持续扩充的语言观察数据。

## 规模（总计约 13.4 万条目）

| 层 | 内容 | 数量 | 数据源 | 授权 |
|---|---|---|---|---|
| 汉字层 | 一二级 6500 字：拼音 + 英文释义 + 级别 + 频次 | 6,500 | 《通用规范汉字表》+ Unihan kDefinition/kMandarin/kHanyuPinlu | 字表政府公开；Unihan 宽松许可 |
| 词层 | 常用汉语词：拼音 + 词性 + 英文释义 + 词频 | 125,262（全量）/ 网页工具含高频 3 万 | CC-CEDICT 12.5 万词条 + jieba 词频 | CC BY-SA 4.0（衍生须开源共享） |
| 特色层 | 中式英语词条：中 → 字面直译 → 规范译 → 出处/状态 | 38（首批） | 人工整理（皮钦英语、中文借词、网络梗、标语误译） | 本项目原创 |
| 英语层 | COCA 前 20200 中未被中文侧覆盖的常用词（英→中反查） | 2,006 | COCA 20000 开源整理版（llt22/coca-vocabulary-20000） | 开源整理数据 |

覆盖情况：COCA 前 20200 常用英语词中，18,022 个（约 89%）已被中文侧释义覆盖，2,006 个未覆盖词收入英语补齐层。

## 定位（为什么值得做）

公开领域没有直接对标项目（GitHub 上 62 个 chinglish 相关仓库无一为词典）。现有类似物分五类：

- 标准中英词典（CC-CEDICT 全家桶、WantWords、Syng 等）：无中式英语特色词条
- 搞笑标语汇编（Radtke《Chinglish: Found in Translation》等）：非结构化数据
- 学术语料库（CCAE、CCE、iWrite 等）：研究用途，非词典
- 「消灭中式英语」工具（改写匠、Ries.AI、WordsTalk 等）：方向与本项目相反
- 谐音/生成器娱乐 App（拆个梨洗等）：非词典

本项目的交集「记录 + 数据化 + 词典」目前无人占位；方法论先例是 Singlish 词典（1783 条，LLM 起草 + 人工校审，CC-BY-SA 开源）。

## 目录结构

```
chinglish-dictionary/
├── web/                 # 网页查询工具（双击 index.html 即可用）
│   ├── index.html       # 双向搜索界面（查中文 / 查英文 / 特色词条）
│   └── data.js          # 打包数据（高频 3 万词 + 6500 字 + 特色 + 英语层）
├── data/
│   └── out/             # 产物（raw 原始数据不上传，重建命令见下）
│       ├── char_layer.json / .csv        # 字层
│       ├── word_layer.json / .csv        # 词层（全量 12.5 万）
│       ├── chinglish_layer.json / .csv   # 特色层
│       ├── english_layer.json / .csv     # 英语层
│       └── master_core.json              # 字层+词层合并主数据
├── scripts/             # 构建脚本（Python）
│   ├── build_core.py        # 字层+词层构建
│   ├── build_english.py     # 英语补齐层构建
│   ├── build_chinglish.py   # 特色层构建
│   ├── build_web_data.py    # 网页数据打包
│   ├── download_coca.py / retry_coca_api.py  # COCA 下载
│   ├── unpack_sources.py / check_sources.py  # 数据源检查
│   └── verify_data.py       # 数据验证
├── LICENSE               # 代码 MIT
├── LICENSE-DATA.txt      # 数据 CC BY-SA 4.0
└── README.md
```

## 使用方式

1. **网页工具**：用浏览器打开 `web/index.html`（需与 `web/data.js` 同目录），离线可用。
   - 查中文：输入汉字或词语（精确匹配字/词 + 特色词条中文包含）
   - 查英文：输入英文单词（词层英文释义包含匹配 + 英语层精确匹配 + 特色词条）
2. **数据文件**：`data/out/` 下各层 JSON/CSV，字段见下。

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

## 授权

- **代码与网页工具**：MIT（见 LICENSE）
- **数据**：CC BY-SA 4.0（见 LICENSE-DATA.txt）。因含 CC-CEDICT 衍生数据，公开分享须保持同授；特色层为本项目原创整理，一并按 CC BY-SA 4.0 开放
- **数据源**：Unihan（Unicode License 宽松）；CC-CEDICT（CC BY-SA 4.0）；COCA 开源整理版 llt22/coca-vocabulary-20000；jieba 词频（MIT）；《通用规范汉字表》政府公开

## 已知限制与后续

- 官方《现代汉语常用词表（草案）》（56008 词）PDF 为图片型无文本层，无法机器解析；词层改用 CC-CEDICT 全量（覆盖所有常用词并自带英文释义）+ jieba 词频分层，规模与覆盖均超出原词表
- COCA 20200 词中 5 个因分片格式变体未解析（影响极小）；个别特殊词形（缩略/拟声）释义为空已过滤
- 字层 6500 字中 15 个字 Unihan 无英文释义（生僻二级字），已标「释义待补」
- 特色层首批 38 条，按 Singlish 词典模式持续扩充（网络收集 + LLM 起草 + 人工校审）
- 后续可加：HSK 3.0 分级标记、例句库、繁体字关联、小程序接入（数据底座即 `data/out/`）

## 重建

原始数据（Unihan、CC-CEDICT、字表、COCA 分片）从各自上游下载到 `data/raw/` 后：

```powershell
python scripts\build_core.py        # 字层+词层
python scripts\build_english.py     # 英语层（需 raw/coca 分片齐全）
python scripts\build_chinglish.py   # 特色层
python scripts\build_web_data.py    # 打包 web/data.js
python scripts\verify_data.py       # 数据验证
```

依赖：pdfplumber（仅数据源检查用）、pandas（可选）。核心构建仅用标准库。
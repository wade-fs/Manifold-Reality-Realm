# 《多重實相界》專案總覽 (manifest.md)

## 基本資訊
- **書名**：多重實相界（Manifold Reality Realm）
- **類型**：哲學神話 / 沉浸式新神話小說
- **核心主題**：理解即是創造，觀測即是改變
- **主角**：陳進
- **預計總章節**：1000+ 章
- **風格定位**：神話氣韻 + 深刻哲學 + 沉浸式遊記

---

## 專案目錄結構
```
多重實相界/
├── novel_write.py                  # 寫作助手腳本
├── VISION.md                       # 創作核心理念
├── core/                           # 核心概念草稿
│   ├── 01.md
│   └── 02.md
├── docs/
│   ├── manifest.md                 # 本檔案（總覽）
│   ├── volume_plan.md              # 各卷神話規劃
│   ├── vol1.md                     # 第一卷章節綱要
│   ├── vol2.md                     # 第二卷章節綱要
│   ├── canon/                      # 世界觀核心設定
│   ├── characters/                 # 人物設定與弧線
│   └── rules/                      # 寫作規範
└── chapter/                        # 生成的正文章節
    └── 01/                         # 第一卷（自動建立）
```


---

## 主要檔案說明

### docs/canon/ （世界觀聖經）
- `novel_bible.md` → 核心世界觀（神話版）
- `timeline.md` → 神話紀年
- `factions.md` → 門派法門
- `historical_events.md` → 重大事件
- `memory_system.md` → 記憶系統
- `footprint_system.md` → 踏印系統
- `settlement_and_population_system.md` → 聚落與生民
- `profession_system.md` → 職業系統

### docs/characters/
- `main_characters.md` → 主角與重要配角
- `character_arcs.md` → 主線人物成長弧

### docs/rules/
- `writing_style.md` → 寫作風格（神話版）
- `continuity.md` → 連續性規範
- `chapter_template.md` → 章節寫作模板

---

## 使用 novel_write.py 流程

1. 修改 `BIBLE_FILES` 列表（加入所有 canon 與 characters 檔案）
2. 執行 `python novel_write.py cache-create` 建立快取
3. 在 `docs/vol1.md`、`docs/vol2.md` 等綱要中用 `#### 第N章 【標題】` 格式規劃章節
4. 使用 `write` 或 `batch` 指令生成章節

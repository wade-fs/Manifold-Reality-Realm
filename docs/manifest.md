# 《修仙志怪錄》專案總覽 (manifest.md)

## 基本資訊
- **書名**：修仙志怪錄（Tales of Immortal Cultivation）
- **類型**：古典志怪 / 章回 / 修仙 / 懸疑 小說
- **核心主題**：世界是一個巨大的謎團。主角不是來尋找答案，而是來經歷未知與荒誕。
- **主角**：陳進
- **預計總章節**：600 章
- **風格定位**：東方克蘇魯氣韻 + 山海經地理 + 沉浸式懸疑志怪

---

## 專案目錄結構
```
修仙志怪錄/
├── novel_write.py                  # 寫作助手腳本
├── docs/
│   ├── manifest.md                 # 本檔案（總覽）
│   ├── volume_plan.md              # 各卷神話規劃
│   ├── vol1.md                     # 第一卷章節綱要
│   ├── vol2.md                     # 第二卷章節綱要
│   ├── vol3.md                     # 第三卷章節綱要
│   ├── vol4.md                     # 第四卷章節綱要
│   ├── vol5.md                     # 第五卷章節綱要
│   ├── canon/                      # 世界觀核心設定
│   ├── characters/                 # 人物設定與弧線
│   └── rules/                      # 寫作規範
└── chapter/                        # 生成的正文章節
    └── 01/                         # 第一卷（自動建立）
```

---

## 主要檔案說明

### docs/canon/ （世界觀聖經）
- `atom.md` → 世界公理
- `novel_bible.md` → 核心世界觀（懸疑志怪版）
- `creative-outline.md` → 創作綱領
- `religion.md`  → 教門派別

### docs/characters/
- `main_character.md` → 主角介紹

### docs/rules/
- `writing_style.md` → 寫作風格（不給答案、名詞延遲命名）
- `continuity.md` → 連續性規範
- `chapter_template.md` → 章節寫作模板

---

## 使用 novel_write.py 流程

1. 修改 `BIBLE_FILES` 列表（加入所有 canon 與 characters 檔案）
2. 執行 `python novel_write.py cache-create` 建立快取
3. 在 `docs/vol1.md` 等綱要中用 `#### 第N章 【標題】` 格式規劃章節
4. 使用 `write` 或 `batch` 指令生成章節

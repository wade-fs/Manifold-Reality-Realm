# 修仙志怪錄

這是《修仙志怪錄》小說寫作專案。

使用 `novel_write.py` 進行章節生成。

## 使用方式

```bash
# 1. 建立快取（強烈建議先執行）
./novel_write.py cache-create

# 2. 批次生成章節
./novel_write.py batch --start 1 --end 10

# 3. 單章生成
./novel_write.py write --chapter 1

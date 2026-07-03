#!/usr/bin/env python3
"""
count_zh.py - 計算 Markdown 檔案中純中文字數
用法:
  python count_zh.py file.md
  python count_zh.py dir/
  python count_zh.py dir/ --recursive
  python count_zh.py a.md b.md dir/
"""

import re
import sys
import shutil
import argparse
from pathlib import Path


def is_chinese(ch: str) -> bool:
    """判斷單一字元是否為中文字（CJK 統一表意文字範圍）"""
    cp = ord(ch)
    return (
        0x4E00 <= cp <= 0x9FFF   # CJK Unified Ideographs
        or 0x3400 <= cp <= 0x4DBF  # CJK Extension A
        or 0x20000 <= cp <= 0x2A6DF  # CJK Extension B
        or 0x2A700 <= cp <= 0x2CEAF  # CJK Extension C/D/E
        or 0xF900 <= cp <= 0xFAFF   # CJK Compatibility Ideographs
    )


def strip_markdown(text: str) -> str:
    """移除 Markdown 語法，只留純文字內容"""
    # 移除 code block（```...```）
    text = re.sub(r'```[\s\S]*?```', '', text)
    # 移除行內 code（`...`）
    text = re.sub(r'`[^`]*`', '', text)
    # 移除 HTML 標籤
    text = re.sub(r'<[^>]+>', '', text)
    # 移除圖片與連結語法，但保留顯示文字
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'\[([^\]]*)\]\([^\)]*\)', r'\1', text)
    # 移除 heading 符號 (#)
    text = re.sub(r'^#{1,6}\s*', '', text, flags=re.MULTILINE)
    # 移除 blockquote 符號 (>)
    text = re.sub(r'^\s*>\s?', '', text, flags=re.MULTILINE)
    # 移除水平線
    text = re.sub(r'^[-*_]{3,}\s*$', '', text, flags=re.MULTILINE)
    return text


def count_chinese_in_file(path: Path) -> int:
    """計算單一檔案的中文字數"""
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        print(f"  [錯誤] 無法讀取 {path}: {e}", file=sys.stderr)
        return 0
    text = strip_markdown(text)
    return sum(1 for ch in text if is_chinese(ch))


def collect_md_files(target: Path, recursive: bool) -> list[Path]:
    """收集目錄下（或單一）.md 檔案"""
    if target.is_file():
        return [target] if target.suffix.lower() == '.md' else []
    if target.is_dir():
        pattern = '**/*.md' if recursive else '*.md'
        return sorted(target.glob(pattern))
    return []


def fmt(n: int) -> str:
    return f"{n:>5,}"


def display_width(s: str) -> int:
    """計算字串的實際終端顯示寬度（全形字算 2，半形算 1）"""
    w = 0
    for ch in s:
        cp = ord(ch)
        # 全形範圍：CJK、全形標點、部分符號
        if (
            0x1100 <= cp <= 0x115F   # Hangul Jamo
            or 0x2E80 <= cp <= 0x303E  # CJK Radicals / Kangxi
            or 0x3040 <= cp <= 0x33FF  # Hiragana … CJK Compatibility
            or 0x3400 <= cp <= 0x4DBF  # CJK Ext-A
            or 0x4E00 <= cp <= 0xA4CF  # CJK Unified
            or 0xA960 <= cp <= 0xA97F  # Hangul Jamo Extended-A
            or 0xAC00 <= cp <= 0xD7FF  # Hangul Syllables
            or 0xF900 <= cp <= 0xFAFF  # CJK Compatibility Ideographs
            or 0xFE10 <= cp <= 0xFE1F  # Vertical Forms
            or 0xFE30 <= cp <= 0xFE4F  # CJK Compatibility Forms
            or 0xFF00 <= cp <= 0xFF60  # Fullwidth Latin / Katakana
            or 0xFFE0 <= cp <= 0xFFE6  # Fullwidth Signs
            or 0x1B000 <= cp <= 0x1B0FF # Kana Supplement
            or 0x1F004 <= cp <= 0x1F0CF # Playing Cards
            or 0x1F200 <= cp <= 0x1F2FF # Enclosed Ideographic
            or 0x20000 <= cp <= 0x2FFFD # CJK Ext-B … F
            or 0x30000 <= cp <= 0x3FFFD # CJK Ext-G …
        ):
            w += 2
        else:
            w += 1
    return w


def ljust_w(s: str, width: int) -> str:
    """以顯示寬度為基準的左對齊（補空格）"""
    pad = width - display_width(s)
    return s + ' ' * max(pad, 0)


def rjust_w(s: str, width: int) -> str:
    """以顯示寬度為基準的右對齊（補空格）"""
    pad = width - display_width(s)
    return ' ' * max(pad, 0) + s


def main():
    parser = argparse.ArgumentParser(
        description='計算 Markdown 檔案中的純中文字數'
    )
    parser.add_argument(
        'targets', nargs='+',
        help='檔案或目錄路徑（可多個）'
    )
    parser.add_argument(
        '-r', '--recursive', action='store_true',
        help='遞迴搜尋子目錄（目錄模式下有效）'
    )
    parser.add_argument(
        '--no-strip', action='store_true',
        help='不過濾 Markdown 語法，直接計算原始內容'
    )
    args = parser.parse_args()

    global strip_markdown
    if args.no_strip:
        strip_markdown = lambda t: t  # noqa: E731

    grand_total = 0
    multi = len(args.targets) > 1

    for raw in args.targets:
        target = Path(raw)
        if not target.exists():
            print(f"[警告] 找不到路徑: {target}", file=sys.stderr)
            continue

        files = collect_md_files(target, args.recursive)

        if not files:
            print(f"[警告] {target} 底下沒有找到 .md 檔案", file=sys.stderr)
            continue

        dir_total = 0

        if target.is_dir():
            # ── 收集所有結果 ──────────────────────────────
            rows: list[tuple[int, str]] = []
            for f in files:
                count = count_chinese_in_file(f)
                dir_total += count
                try:
                    rel = str(f.relative_to(target))
                except ValueError:
                    rel = str(f)
                rows.append((count, rel))

            # ── 計算多欄佈局 ──────────────────────────────
            import math
            term_w = shutil.get_terminal_size(fallback=(120, 24)).columns
            max_name_w = max(display_width(r[1]) for r in rows) if rows else 10
            # 每個欄組的實際顯示寬度：
            # "| 2,709 | 601.md " = "| "(2) + NUM_W(5) + " | "(3) + name_w + " "(1)
            # 整行末尾還有一個 "|"，當固定開銷 (-1)
            NUM_W  = 4
            cell_w = 2 + NUM_W + 3 + max_name_w + 1   # = max_name_w + 10
            ncols  = max(1, (term_w - 1) // cell_w)

            # ── 印出標題 ──────────────────────────────────
            print(f"\n📁  {target}{'  (遞迴)' if args.recursive else ''}")

            # GFM 表頭：每「欄組」重複 "| 字數 | 檔案 "
            # 數字欄固定 4 位（字數不破萬，無千分位）
            NUM_W = 4

            def md_header_row(n: int, name_w: int) -> str:
                cell = f"|{'字數':>4}|  {'檔案':<4}"
                return cell * n + "|"

            def md_sep_row(n: int, name_w: int) -> str:
                cell = f"|{'-' * NUM_W}: | {'-' * name_w} "
                return cell * n + "|"

            def md_data_row(cells: list, name_w: int) -> str:
                parts = []
                for cell in cells:
                    if cell is None:
                        parts.append(f"| {'':{NUM_W}} | {'':<{name_w}} ")
                    else:
                        cnt, name = cell
                        pad = name_w - display_width(name)
                        parts.append(f"| {cnt:>{NUM_W}} | {name}{' ' * max(pad,0)} ")
                return "".join(parts) + "|"

            print(md_header_row(ncols, max_name_w))
            print(md_sep_row(ncols, max_name_w))

            # ── 印出資料列（直向填欄：由上到下，再換下一欄）──
            nrows  = math.ceil(len(rows) / ncols)
            padded = rows + [None] * (nrows * ncols - len(rows))
            grid   = [[padded[c * nrows + r] for c in range(ncols)] for r in range(nrows)]
            for grid_row in grid:
                print(md_data_row(grid_row, max_name_w))

            # ── 小計 ──────────────────────────────────────
            if len(files) > 1:
                print(f"\n> **小計**：{dir_total} 字（共 {len(files)} 個檔案）")

        else:
            # 單檔模式：維持原行為
            for f in files:
                count = count_chinese_in_file(f)
                dir_total += count
                print(f"{fmt(count)}  {f}")

        grand_total += dir_total


    if multi:
        print(f"\n{'='*20}")
        print(f"{fmt(grand_total)}  總計")
    elif grand_total and not any(Path(t).is_dir() for t in args.targets):
        pass  # 單檔已印出，不重複
    else:
        pass


if __name__ == '__main__':
    main()

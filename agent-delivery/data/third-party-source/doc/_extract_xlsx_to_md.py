# -*- coding: utf-8 -*-
"""用 officecli 将 doc/*.xlsx 的「*要素库」Sheet 提取为 Markdown。

单元格值：officecli view text（完整，不截断）
样式/合并：officecli dump JSON（附存；注意 dump 的 import 文本对大表可能截断，故不以之为值真源）
"""
from __future__ import annotations

import csv
import json
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

DOC_DIR = Path(__file__).resolve().parent
OUT_DIR = DOC_DIR / "md-extract"
DUMP_DIR = OUT_DIR / "_officecli-dumps"
CSV_DIR = OUT_DIR / "_csv"
TEXT_DIR = OUT_DIR / "_officecli-text"
SHEET_SUFFIX = "要素库"
OFFICECLI: Path | None = None


def resolve_officecli() -> Path:
    """Prefer PATH; fall back to known WinGet / legacy install locations."""
    which = shutil.which("officecli") or shutil.which("officecli.exe")
    if which:
        return Path(which)
    candidates = [
        Path.home() / "AppData" / "Local" / "Microsoft" / "WinGet" / "Links" / "officecli.exe",
        Path.home() / "AppData" / "Local" / "OfficeCLI" / "officecli.exe",
    ]
    for p in candidates:
        if p.is_file():
            return p
    raise FileNotFoundError("officecli not found on PATH or known install paths")


def officecli_bin() -> Path:
    global OFFICECLI
    if OFFICECLI is None:
        OFFICECLI = resolve_officecli()
    return OFFICECLI

CELL_RE = re.compile(r"([A-Z]+)(\d+)=(.*?)(?=\t[A-Z]+\d+=|$)", re.DOTALL)
COL_RE = re.compile(r"([A-Z]+)")


def col_to_idx(col: str) -> int:
    n = 0
    for ch in col:
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def idx_to_col(i: int) -> str:
    i += 1
    s = ""
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def run_officecli(args: list[str], timeout: int = 900) -> bytes:
    cmd = [str(officecli_bin()), *args]
    p = subprocess.run(cmd, capture_output=True, timeout=timeout, check=False)
    if p.returncode != 0:
        err = p.stderr.decode("utf-8", errors="replace")
        out = p.stdout.decode("utf-8", errors="replace")
        raise RuntimeError(f"officecli failed ({p.returncode}): {' '.join(args)}\n{err}\n{out[:2000]}")
    return p.stdout


def run_officecli_text(args: list[str], timeout: int = 900) -> str:
    raw = run_officecli(args, timeout=timeout)
    for enc in ("utf-8", "utf-8-sig", "gbk", "cp936"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def sheet_outline(xlsx: Path) -> list[tuple[str, int, int]]:
    """Return list of (name, rows, cols) from outline."""
    text = run_officecli_text(["view", str(xlsx), "outline"])
    items: list[tuple[str, int, int]] = []
    for line in text.splitlines():
        m = re.search(r'├──\s*"([^"]+)"\s*\((\d+)\s*rows?\s*[×x]\s*(\d+)\s*cols?', line)
        if m:
            items.append((m.group(1), int(m.group(2)), int(m.group(3))))
    if not items:
        raise RuntimeError(f"no sheets in outline: {xlsx.name}\n{text[:1000]}")
    return items


def safe_name(s: str) -> str:
    s = re.sub(r'[<>:"/\\|?*]', "_", s).strip().rstrip(".")
    return s[:120]


def escape_md_cell(v: str) -> str:
    s = str(v).replace("\r\n", "\n").replace("\r", "\n")
    s = s.replace("|", "\\|").replace("\n", "<br>")
    return s


def parse_view_text(text: str) -> list[list[str]]:
    """Parse officecli view text sparse cells into dense grid (1-based rows)."""
    cells: dict[tuple[int, int], str] = {}
    max_r, max_c = 0, 0
    for line in text.splitlines():
        if "]=" not in line and not re.search(r"[A-Z]+\d+=", line):
            continue
        # strip row prefix [/Sheet/row[N]]
        payload = line
        if "] " in line:
            payload = line.split("] ", 1)[1]
        for m in CELL_RE.finditer(payload):
            col, row_s, val = m.group(1), m.group(2), m.group(3)
            r, c = int(row_s), col_to_idx(col)
            cells[(r, c)] = val
            max_r = max(max_r, r)
            max_c = max(max_c, c)
    if max_r == 0:
        return []
    grid = [["" for _ in range(max_c + 1)] for _ in range(max_r)]
    for (r, c), v in cells.items():
        grid[r - 1][c] = v
    # drop fully empty rows (outline 可能含空洞/尾部空行；值信息保留在非空行)
    grid = [row for row in grid if any((x or "").strip() for x in row)]
    # trim trailing empty cols
    while grid and grid[0] and all(not (row[-1] or "").strip() for row in grid):
        for row in grid:
            row.pop()
    return grid


def rows_to_md_table(rows: list[list[str]]) -> str:
    if not rows:
        return "_（空表）_\n"
    width = max(len(r) for r in rows)
    grid = [r + [""] * (width - len(r)) for r in rows]
    header = [escape_md_cell(c) if str(c).strip() else f"_col{i+1}_" for i, c in enumerate(grid[0])]
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(["---"] * width) + " |",
    ]
    for r in grid[1:]:
        lines.append("| " + " | ".join(escape_md_cell(c) for c in r) + " |")
    return "\n".join(lines) + "\n"


def write_csv(path: Path, rows: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerows(rows)


def collect_dump_meta(dump: list[dict]) -> dict:
    merges, formulas = [], []
    fills: dict[str, int] = defaultdict(int)
    fonts: dict[str, int] = defaultdict(int)
    for item in dump:
        props = item.get("props") or {}
        path = item.get("path") or ""
        if "merge" in props:
            merges.append(f"{path} merge={props.get('merge')}")
        if props.get("formula"):
            formulas.append(f"{path} formula={props.get('formula')}")
        if "fill" in props:
            fills[str(props["fill"])] += 1
        if "font.name" in props:
            fonts[str(props["font.name"])] += 1
    return {"merges": merges, "formulas": formulas, "fills": dict(fills), "fonts": dict(fonts), "commands": len(dump)}


def extract_sheet(xlsx: Path, sheet: str, rows: int, cols: int) -> str:
    # pad range beyond outline to be safe
    end_col = idx_to_col(max(cols + 5, 30) - 1)
    end_row = max(rows + 5, 50)
    rng = f"{sheet}!A1:{end_col}{end_row}"

    text_raw = run_officecli(["view", str(xlsx), "text", "--range", rng], timeout=900)
    # persist raw bytes as utf-8 text best-effort
    text_path = TEXT_DIR / f"{safe_name(xlsx.stem)}__{safe_name(sheet)}.txt"
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    try:
        text = text_raw.decode("utf-8")
    except UnicodeDecodeError:
        text = text_raw.decode("utf-8", errors="replace")
    text_path.write_bytes(text.encode("utf-8"))

    grid = parse_view_text(text)
    nonempty = sum(1 for r in grid if any((c or "").strip() for c in r))

    # dump for style meta (optional; may be large)
    dump_path = DUMP_DIR / f"{safe_name(xlsx.stem)}__{safe_name(sheet)}.json"
    dump_meta = {}
    try:
        run_officecli(["dump", str(xlsx), f"/{sheet}", "-o", str(dump_path), "--json"], timeout=900)
        dump = json.loads(dump_path.read_text(encoding="utf-8"))
        if isinstance(dump, list):
            dump_meta = collect_dump_meta(dump)
    except Exception as e:
        dump_meta = {"error": str(e)}

    csv_path = CSV_DIR / f"{safe_name(xlsx.stem)}__{safe_name(sheet)}.csv"
    write_csv(csv_path, grid)

    parts: list[str] = []
    parts.append(f'<a id="sheet-{safe_name(sheet)}"></a>\n\n')
    parts.append(f"## Sheet: {sheet}\n\n")
    parts.append(f"- outline: {rows} rows × {cols} cols\n")
    parts.append(f"- extracted nonempty rows: {nonempty}\n")
    parts.append(f"- extracted grid: {len(grid)} rows × {(len(grid[0]) if grid else 0)} cols\n")
    parts.append(f"- officecli view text: `{text_path.relative_to(DOC_DIR).as_posix()}`\n")
    parts.append(f"- CSV: `{csv_path.relative_to(DOC_DIR).as_posix()}`\n")
    if dump_path.is_file():
        parts.append(f"- officecli dump: `{dump_path.relative_to(DOC_DIR).as_posix()}`\n")
    parts.append("\n### 单元格数据（完整）\n\n")
    parts.append(rows_to_md_table(grid))

    parts.append("\n### 样式 / 合并 / 公式元数据（officecli dump）\n\n")
    if dump_meta.get("error"):
        parts.append(f"- dump 失败: {dump_meta['error']}\n")
    else:
        parts.append(f"- dump commands: {dump_meta.get('commands', 0)}\n")
        merges = dump_meta.get("merges") or []
        formulas = dump_meta.get("formulas") or []
        if merges:
            parts.append(f"- merge 条数: {len(merges)}\n")
            parts.append("<details><summary>merge 明细</summary>\n\n```\n")
            parts.append("\n".join(merges))
            parts.append("\n```\n</details>\n")
        else:
            parts.append("- merge: 无或未在 dump set 中标注\n")
        if formulas:
            parts.append(f"- formula 条数: {len(formulas)}\n")
            parts.append("<details><summary>formula 明细</summary>\n\n```\n")
            parts.append("\n".join(formulas))
            parts.append("\n```\n</details>\n")
        else:
            parts.append("- formula: 无（值可能已算入单元格）\n")
        fills = dump_meta.get("fills") or {}
        if fills:
            top = sorted(fills.items(), key=lambda x: -x[1])[:15]
            parts.append("- fill: " + ", ".join(f"`{k}`×{v}" for k, v in top) + "\n")
        fonts = dump_meta.get("fonts") or {}
        if fonts:
            parts.append("- font.name: " + ", ".join(f"`{k}`×{v}" for k, v in sorted(fonts.items(), key=lambda x: -x[1])) + "\n")

    parts.append("\n---\n\n")
    print(f"    rows={len(grid)} nonempty={nonempty}", flush=True)
    return "".join(parts)


def is_factor_sheet(name: str) -> bool:
    return name.strip().endswith(SHEET_SUFFIX)


def prune_non_factor_artifacts(keep_stems: set[str]) -> list[str]:
    """Remove csv/text/dump not belonging to the current *要素库 extract set."""
    removed: list[str] = []
    for d, suffix in ((CSV_DIR, ".csv"), (TEXT_DIR, ".txt"), (DUMP_DIR, ".json")):
        if not d.is_dir():
            continue
        for path in d.iterdir():
            if not path.is_file() or path.suffix.lower() != suffix:
                continue
            if path.stem in keep_stems:
                continue
            path.unlink()
            removed.append(str(path.relative_to(DOC_DIR).as_posix()))
    return removed


def main() -> int:
    try:
        officecli_bin()
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        return 1

    for d in (OUT_DIR, DUMP_DIR, CSV_DIR, TEXT_DIR):
        d.mkdir(parents=True, exist_ok=True)

    xlsx_files = sorted(DOC_DIR.glob("*.xlsx"))
    ver = run_officecli_text(["--version"]).strip()
    index = [
        "# 三方承诺数据源表 — doc 目录 Markdown 要素库提取\n\n",
        f"> 提取时间: {datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')}\n",
        f"> 工具: officecli `{ver}`\n",
        f"> 范围: **仅 Sheet 名以「{SHEET_SUFFIX}」结尾**｜值真源: `view text`｜样式: `dump` JSON｜CSV: `_csv/`\n\n",
        "## 工作簿索引\n\n",
        "| # | 源文件 | Markdown | 要素库 Sheets |\n|---|--------|----------|---------------|\n",
    ]

    keep_stems: set[str] = set()

    for i, xlsx in enumerate(xlsx_files, 1):
        print(f"[{i}/{len(xlsx_files)}] {xlsx.name}", flush=True)
        all_sheets = sheet_outline(xlsx)
        sheets = [(n, r, c) for n, r, c in all_sheets if is_factor_sheet(n)]
        skipped = [n for n, _, _ in all_sheets if not is_factor_sheet(n)]
        if skipped:
            print(f"  skip: {', '.join(skipped)}", flush=True)
        if not sheets:
            print(f"  WARN: no *{SHEET_SUFFIX} sheets in {xlsx.name}", flush=True)
            continue

        stats = run_officecli_text(["view", str(xlsx), "stats", "--json"])
        md_path = OUT_DIR / f"{safe_name(xlsx.stem)}.md"
        body = [
            f"# {xlsx.name}\n\n",
            f"- 源文件: `{xlsx.name}`\n",
            f"- 工作簿 Sheet 数: {len(all_sheets)}（本次提取要素库: {len(sheets)}）\n",
            f"- 提取范围: Sheet 名以「{SHEET_SUFFIX}」结尾\n",
            "- 提取: officecli view text（单元格）+ dump（样式）\n\n",
            "## workbook stats\n\n```json\n",
            stats.strip(),
            "\n```\n\n## Sheet 目录（仅要素库）\n\n",
        ]
        for name, r, c in sheets:
            body.append(f"- [{name}](#sheet-{safe_name(name)}) ({r}×{c})\n")
        if skipped:
            body.append("\n> 已跳过非要素库: " + ", ".join(f"`{n}`" for n in skipped) + "\n")
        body.append("\n")

        for name, r, c in sheets:
            print(f"  - {name} ({r}x{c})", flush=True)
            keep_stems.add(f"{safe_name(xlsx.stem)}__{safe_name(name)}")
            body.append(extract_sheet(xlsx, name, r, c))

        md_path.write_text("".join(body), encoding="utf-8")
        names = ", ".join(n for n, _, _ in sheets)
        index.append(f"| {i} | `{xlsx.name}` | [{md_path.name}]({md_path.name}) | {len(sheets)}: {names} |\n")
        print(f"  -> {md_path}", flush=True)

    removed = prune_non_factor_artifacts(keep_stems)
    if removed:
        print(f"pruned {len(removed)} non-factor artifacts", flush=True)
        for rel in removed:
            print(f"  - {rel}", flush=True)

    index.append(
        "\n## 目录\n\n"
        "```\n"
        "md-extract/\n"
        "  README.md\n"
        "  *.md                 ← 仅 *要素库 sheets\n"
        "  _csv/\n"
        "  _officecli-text/     ← view text 原文\n"
        "  _officecli-dumps/    ← dump JSON（样式）\n"
        "```\n"
    )
    (OUT_DIR / "README.md").write_text("".join(index), encoding="utf-8")
    print("DONE", OUT_DIR)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

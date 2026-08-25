# -*- coding: utf-8 -*-
"""Merge KJZTFWALGO work/L01–L60.md into FUNC Excel v1.

Does not trim. Does not write test steps.
Work unit is Lxx (one 六级 per file): 需规 sits above the 4-column table.
"""
from __future__ import annotations

import re
import shutil
from copy import copy
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "qa/total-set/KJZTFWALGO/fp-split-run"
DIR = ROOT / "qa/total-set/KJZTFWALGO"
OUT = DIR / "6.国际科技信息中心项目_科技专题服务算法库_功能点拆分_v1.xlsx"
ID_PREFIX = "ZNFWJQ-KJZTFWALGO-v1.0-FUNC-"
TITLE = "智能服务集群-科技专题服务算法库功能点拆分"
MAX_ID = 60
NCOLS = 20


def find_template() -> Path:
    topic = ROOT / "qa/total-set/KJZTFWXT"
    files = [f for f in topic.glob("*功能点拆分_v8.xlsx") if not f.name.startswith("~$")]
    if not files:
        raise SystemExit(f"template not found under {topic}")
    return files[0]


def extract_spec(text: str) -> str:
    m = re.search(r"## 需规原文\s*\n(.*?)(?=\n\| 子功能项)", text, re.S)
    return m.group(1).strip() if m else ""


def parse_work(path: Path) -> tuple[str, str, str, str, int, str, list[list[str]]]:
    text = path.read_text(encoding="utf-8")
    l3 = re.search(r"- 三级：(.+)", text)
    l4 = re.search(r"- 四级：(.+)", text)
    l5 = re.search(r"- 五级：(.+)", text)
    l6 = re.search(r"- 六级：(.+)", text)
    n = re.search(r"- 条数：(\d+)", text)
    l3s = l3.group(1).strip() if l3 else ""
    l4s = l4.group(1).strip() if l4 else ""
    l5s = l5.group(1).strip() if l5 else ""
    l6s = l6.group(1).strip() if l6 else ""
    declared = int(n.group(1)) if n else 0
    spec = extract_spec(text)
    rows: list[list[str]] = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 4:
            continue
        if cells[0] in ("子功能项", "---") or set(cells[0]) <= {"-", ":"}:
            continue
        rows.append(cells[:4])
    return l3s, l4s, l5s, l6s, declared, spec, rows


def collect() -> tuple[list[list[str]], list[str]]:
    out: list[list[str]] = []
    mismatches: list[str] = []
    seq = 1
    for i in range(1, MAX_ID + 1):
        lid = f"L{i:02d}"
        path = RUN / "work" / f"{lid}.md"
        if not path.exists():
            mismatches.append(f"{lid}: missing work")
            continue
        l3, l4, l5, l6, declared, spec, rows = parse_work(path)
        if not spec:
            mismatches.append(f"{lid}: empty 需规")
        if len(rows) != declared:
            mismatches.append(f"{lid}: header={declared} table={len(rows)}")
        for cells in rows:
            out.append(
                [
                    f"{ID_PREFIX}{seq:05d}",
                    l3,
                    l4,
                    l5,
                    cells[0] or l6,
                    l5,
                    cells[1],
                    cells[2],
                    cells[3],
                    spec,
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                ]
            )
            seq += 1
    return out, mismatches


def snapshot_row_styles(ws, row: int) -> list[dict]:
    out = []
    for c in range(1, NCOLS + 1):
        src = ws.cell(row, c)
        out.append(
            {
                "font": copy(src.font),
                "border": copy(src.border),
                "fill": copy(src.fill),
                "nf": src.number_format,
                "align": copy(src.alignment),
                "prot": copy(src.protection),
            }
        )
    return out


def apply_style(cell, style: dict) -> None:
    cell.font = style["font"]
    cell.border = style["border"]
    cell.fill = style["fill"]
    cell.number_format = style["nf"]
    cell.alignment = style["align"]
    cell.protection = style["prot"]


def main() -> None:
    rows, mismatches = collect()
    if mismatches:
        print("MISMATCH", "; ".join(mismatches))
        raise SystemExit(1)
    src = find_template()
    if OUT.exists():
        try:
            OUT.unlink()
        except PermissionError:
            raise SystemExit(f"Permission denied writing {OUT.name}; close Excel and retry")
    shutil.copyfile(src, OUT)
    wb = load_workbook(OUT)
    ws = wb["功能测试用例"]
    ws["A1"] = TITLE
    styles = snapshot_row_styles(ws, 3)
    if ws.max_row > 2:
        ws.delete_rows(3, ws.max_row - 2)
    for r_i, values in enumerate(rows, 3):
        for c_i, val in enumerate(values, 1):
            cell = ws.cell(r_i, c_i, val)
            apply_style(cell, styles[c_i - 1])
    wb.save(OUT)
    wb.close()
    print(f"rows={len(rows)} out={OUT.name} a1={TITLE}")


if __name__ == "__main__":
    main()

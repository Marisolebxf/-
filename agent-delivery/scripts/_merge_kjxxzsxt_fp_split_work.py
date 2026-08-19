# -*- coding: utf-8 -*-
"""Merge KJXXZSXT work/T01–T140.md into FUNC Excel. Does not trim. Does not write test steps."""
from __future__ import annotations

import re
import shutil
from copy import copy
from pathlib import Path

from openpyxl import load_workbook

RUN = Path(
    r"d:\work\gkx-lumen\gkx-orchestration\agent-delivery\qa\total-set\KJXXZSXT\fp-split-run"
)
DIR = Path(r"d:\work\gkx-lumen\gkx-orchestration\agent-delivery\qa\total-set\KJXXZSXT")
OUT = DIR / "6.国际科技信息中心项目_科技信息展示系统_功能点拆分_v1.xlsx"
ID_PREFIX = "ZNFWJQ-KJXXZSXT-v1.0-FUNC-"
TEMPLATE = Path(
    r"d:\work\gkx-lumen\gkx-orchestration\agent-delivery\qa\total-set\KJZTFWXT"
) / "6.国际科技信息中心项目_科技专题服务系统_功能点拆分_v8.xlsx"
MAX_ID = 140


def parse_work(path: Path) -> tuple[str, str, str, int, list[list[str]]]:
    text = path.read_text(encoding="utf-8")
    l3 = re.search(r"- 三级：(.+)", text)
    l4 = re.search(r"- 四级：(.+)", text)
    l5 = re.search(r"- 五级：(.+)", text)
    n = re.search(r"- 条数：(\d+)", text)
    l3s = l3.group(1).strip() if l3 else ""
    l4s = l4.group(1).strip() if l4 else ""
    l5s = l5.group(1).strip() if l5 else ""
    declared = int(n.group(1)) if n else 0
    rows: list[list[str]] = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 5:
            continue
        if cells[0] in ("子功能项", "---") or set(cells[0]) <= {"-", ":"}:
            continue
        rows.append(cells[:5])
    return l3s, l4s, l5s, declared, rows


def collect() -> tuple[list[list[str]], list[str]]:
    out: list[list[str]] = []
    mismatches: list[str] = []
    seq = 1
    for i in range(1, MAX_ID + 1):
        tid = f"T{i:02d}"
        path = RUN / "work" / f"{tid}.md"
        if not path.exists():
            mismatches.append(f"{tid}: missing work")
            continue
        l3, l4, l5, declared, rows = parse_work(path)
        if len(rows) != declared:
            mismatches.append(f"{tid}: header={declared} table={len(rows)}")
        for cells in rows:
            out.append(
                [
                    f"{ID_PREFIX}{seq:05d}",
                    l3,
                    l4,
                    l5,
                    cells[0],
                    l5,
                    cells[1],
                    cells[2],
                    cells[3],
                    cells[4],
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
    for c in range(1, 21):
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
    if not TEMPLATE.exists():
        raise SystemExit(f"template not found: {TEMPLATE}")
    shutil.copyfile(TEMPLATE, OUT)
    wb = load_workbook(OUT)
    ws = wb["功能测试用例"]
    ws["A1"] = "智能服务集群-科技信息展示系统功能点拆分"
    styles = snapshot_row_styles(ws, 3)
    # clear old topic rows beyond header (row 1-2) / sample row 3 overwritten
    if ws.max_row > 2:
        ws.delete_rows(3, ws.max_row - 2)
    for r_i, values in enumerate(rows, 3):
        for c_i, val in enumerate(values, 1):
            cell = ws.cell(r_i, c_i, val)
            apply_style(cell, styles[c_i - 1])
    wb.save(OUT)
    wb.close()
    print(f"rows={len(rows)} out={OUT.name}")
    if mismatches:
        print("MISMATCH", "; ".join(mismatches))


if __name__ == "__main__":
    main()

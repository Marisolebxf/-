#!/usr/bin/env python3
"""Rebuild the KJZTFWXT 功能测试用例 sheet from current B-line case books.

One live main-table row becomes one sheet row. 功能点 is filled from
coverage-fp 已覆盖/部分覆盖; 无对应功能点 stays empty. 是否通过 stays empty.
Other sheets are left as they are. Does not run the A∪B one-point-per-row merge.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

QA = Path(__file__).resolve().parents[2]
TC = QA / "test-cases" / "KJZTFWXT"
OUT = QA / "delivery" / "KJZTFWXT" / "6.国际科技信息中心项目_科技专题服务系统_测试用例.xlsx"
GROUPS = ["enterprise-企业分析", "industry-center-产业链分析", "service-产业服务链分析"]
ROW_RE = re.compile(r"^\| ZNFWJQ-KJZTFWXT-v1\.0-FUNC-(\d{5}) \|")


def split_row(line: str) -> list[str]:
    protected = line.replace("\\|", "\x00")
    return [c.strip().replace("\x00", "|") for c in protected.strip().strip("|").split("|")]


def fp_names(cov_text: str) -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    for line in cov_text.splitlines():
        if not line.startswith("|"):
            continue
        cells = split_row(line)
        if not cells or all(set(c) <= set("-: ") for c in cells):
            continue
        st_i = next((i for i, c in enumerate(cells) if c in ("已覆盖", "部分覆盖")), None)
        if st_i is None or st_i < 1:
            continue
        key_i = next((i for i, c in enumerate(cells) if "|" in c or c.startswith("T") or c.startswith("US-")), None)
        if key_i is None:
            continue
        parts = [p.strip() for p in cells[key_i].split("|") if p.strip()]
        name = "、".join(parts[2:]) if len(parts) >= 3 else (parts[-1] if parts else "")
        if not name:
            continue
        for fid in re.findall(r"\d{5}", cells[st_i - 1]):
            found.setdefault(fid, [])
            if name not in found[fid]:
                found[fid].append(name)
    return found


def books() -> list[Path]:
    found: list[tuple[int, Path]] = []
    for grp in GROUPS:
        base = TC / grp
        if not base.is_dir():
            continue
        for book in base.iterdir():
            mds = list(book.glob("FUNC-*-用例.md"))
            if book.is_dir() and len(mds) == 1:
                ids = [int(m.group(1)) for line in mds[0].read_text(encoding="utf-8").splitlines() if (m := ROW_RE.match(line))]
                if ids:
                    found.append((min(ids), book))
    return [b for _, b in sorted(found)]


def collect() -> list[list[str]]:
    rows: list[list[str]] = []
    seen: dict[str, str] = {}
    for book in books():
        md = next(book.glob("FUNC-*-用例.md"))
        cov = (book / "coverage-fp.md").read_text(encoding="utf-8")
        names = fp_names(cov)
        for line in md.read_text(encoding="utf-8").splitlines():
            m = ROW_RE.match(line)
            if not m:
                continue
            cells = split_row(line)
            if len(cells) < 17:
                raise SystemExit(f"{md.name} 列数 {len(cells)} < 17：{m.group(1)}")
            fid = m.group(1)
            prev = seen.get(fid)
            if prev:
                raise SystemExit(f"FUNC-{fid} 同时在 {prev} 和 {book.name}")
            seen[fid] = book.name
            row = cells[:17]
            row[6] = "、".join(names.get(fid, []))
            row[12] = ""
            rows.append(row)
    return rows


def main() -> None:
    dry = "--dry-run" in sys.argv
    rows = collect()
    filled = sum(1 for r in rows if r[6])
    print(f"条数 {len(rows)}  功能点已填 {filled}  功能点留空 {len(rows) - filled}")
    if dry:
        return
    if not OUT.is_file():
        raise SystemExit(f"找不到交付簿 {OUT}")
    try:
        import openpyxl
        from openpyxl.styles import Alignment
    except ImportError:
        raise SystemExit("当前解释器没有 openpyxl。改用 gkx-lumen/.venv/bin/python，不要 pip install。")
    wb = openpyxl.load_workbook(OUT)
    ws = wb["功能测试用例"]
    if ws.max_row >= 3:
        ws.delete_rows(3, ws.max_row - 2)
    ws.cell(1, 1).value = "智能服务集群-科技专题服务系统测试用例"
    align = Alignment(vertical="center", wrap_text=True)
    for i, row in enumerate(rows, start=3):
        for c in range(1, 18):
            cell = ws.cell(i, c)
            cell.value = row[c - 1] or None
            cell.alignment = align
    wb.save(OUT)
    print(f"已写入 {OUT}")


if __name__ == "__main__":
    main()

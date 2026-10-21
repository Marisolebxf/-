#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SDWJSF/KJZTFWSFK 第三轮 FUNC 册 → 客户 17 列 Excel（工作区合表 + delivery）。

真源：test-cases/SDWJSF-KJZTFWSFK/**/FUNC-*.md 主表前 17 列。
模板：delivery 目录现有 xlsx（保留兼容/集成/性能/规则 sheet，仅重写功能测试用例数据区）。
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment

ROOT = Path(__file__).resolve().parents[1]  # agent-delivery/
TC_ROOT = ROOT / "qa" / "test-cases" / "SDWJSF-KJZTFWSFK"
TPL = (
    ROOT
    / "qa"
    / "delivery"
    / "SDWJSF-KJZTFWSFK"
    / "6.国际科技信息中心项目_科技专题服务算法库_测试用例.xlsx"
)
OUT_WS = TC_ROOT / "科技专题服务算法库-FUNC测试用例.xlsx"
OUT_DELIVERY = TPL  # 就地覆盖 delivery 交付件

ROW_RE = re.compile(
    r"^\|\s*ZNFWJQ-SDWJSF/KJZTFWSFK-v1\.0-FUNC-(\d{5})\s*\|"
)
ID_RE = re.compile(
    r"^ZNFWJQ-SDWJSF/KJZTFWSFK-v1\.0-FUNC-(\d{5})$"
)


def parse_booklet(md: Path) -> list[list[str]]:
    rows: list[tuple[int, list[str]]] = []
    for line in md.read_text(encoding="utf-8").splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        seq = int(m.group(1))
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 17:
            raise AssertionError(f"{md}: 主表列数 {len(cells)} < 17")
        row = cells[:17]
        for i in range(12, 17):
            row[i] = ""
        rows.append((seq, row))
    return [r for _, r in sorted(rows, key=lambda t: t[0])]


def collect_all_rows() -> list[list[str]]:
    by_id: dict[str, list[str]] = {}
    for md in sorted(TC_ROOT.rglob("FUNC-*.md")):
        for row in parse_booklet(md):
            cid = row[0]
            if cid in by_id:
                raise AssertionError(f"重复编号 {cid}: {md}")
            by_id[cid] = row
    ordered = sorted(by_id.items(), key=lambda kv: int(ID_RE.match(kv[0]).group(1)))
    return [r for _, r in ordered]


def write_workbook(dst: Path, all_rows: list[list[str]]) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.resolve() != TPL.resolve():
        shutil.copy2(TPL, dst)
    wb = openpyxl.load_workbook(dst)
    ws = wb["功能测试用例"]
    if ws.max_row >= 3:
        ws.delete_rows(3, ws.max_row - 2)
    ws.cell(1, 1).value = "智能服务集群-科技专题服务算法库测试用例"
    align = Alignment(vertical="center", wrap_text=True)
    for i, row in enumerate(all_rows, start=3):
        for c in range(1, 18):
            cell = ws.cell(i, c)
            cell.value = row[c - 1] if row[c - 1] else None
            cell.alignment = align
    wb.save(dst)


def main() -> None:
    assert TPL.is_file(), f"模板缺失: {TPL}"
    all_rows = collect_all_rows()
    ids = [r[0] for r in all_rows]
    assert ids, "未解析到任何 FUNC 行"
    bad = [i for i in ids if not ID_RE.match(i)]
    assert not bad, f"编号格式异常: {bad[:5]}"
    seqs = [int(ID_RE.match(i).group(1)) for i in ids]
    assert seqs == list(range(seqs[0], seqs[-1] + 1)), (
        f"编号不连续: 共 {len(seqs)} 条, min={seqs[0]:05d} max={seqs[-1]:05d}"
    )
    write_workbook(OUT_DELIVERY, all_rows)
    write_workbook(OUT_WS, all_rows)
    print(f"OK {len(all_rows)} 条 FUNC-{seqs[0]:05d}～FUNC-{seqs[-1]:05d}")
    print(f"  delivery → {OUT_DELIVERY}")
    print(f"  workspace → {OUT_WS}")


if __name__ == "__main__":
    main()

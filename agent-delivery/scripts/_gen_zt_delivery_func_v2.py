#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""B线 KJZTFWXT 交付 Excel 功能测试用例 sheet 重出（v2.0 用例库 → 模板列）。

- 真源：agent-delivery/qa/test-cases/KJZTFWXT/**/FUNC-*.md 主表前 17 列（=交付模板列）
- 模板：参考文档/测试模板-v2/6.国际科技信息中心项目_xx_测试用例.xlsx（5 sheet 原样保留）
- 仅重写「功能测试用例」sheet 数据区；其他 sheet 不动（样例行清检留待放行前处理）
- 用例簿口径：是否通过列留空；不带 GKX 扩展列
"""
from __future__ import annotations

import copy
import re
from pathlib import Path

import openpyxl

ORCH = Path("/Users/roy/data/projects/zhipu/gkx/gkx-lumen/gkx-orchestration")
TC_ROOT = ORCH / "agent-delivery" / "qa" / "test-cases" / "KJZTFWXT"
TPL = Path("/Users/roy/data/projects/zhipu/gkx/参考文档/测试模板-v2/6.国际科技信息中心项目_xx_测试用例.xlsx")
OUT = ORCH / "agent-delivery" / "qa" / "delivery" / "KJZTFWXT" / "6.国际科技信息中心项目_科技专题服务系统_测试用例.xlsx"

ROW_RE = re.compile(r"^\|\s*ZNFWJQ-KJZTFWXT-v1\.0-FUNC-\d{5}\s*\|")


def parse_md(booklet_dir: Path) -> list[list[str]]:
    """解析一册 FUNC-*.md 主表行，返回 17 列交付数据。"""
    md_files = sorted(booklet_dir.glob("FUNC-*.md"))
    assert len(md_files) == 1, f"{booklet_dir}: 期望 1 个 FUNC md，实得 {len(md_files)}"
    rows = []
    for line in open(md_files[0], encoding="utf-8"):
        if not ROW_RE.match(line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        assert len(cells) >= 17, f"{md_files[0].name}: 主表列数 {len(cells)} < 17"
        rows.append(cells[:17])
    return rows


def min_id(rows: list[list[str]]) -> int:
    return min(int(r[0].rsplit("-", 1)[1]) for r in rows)


def main() -> None:
    # 1) 收集三目录全部册（组目录/册目录 两级）
    grp_order = ["enterprise-企业分析", "industry-center-产业链分析", "service-产业服务链分析"]
    booklets: dict[str, list[tuple[int, list[list[str]]]]] = {g: [] for g in grp_order}
    global_rows: list[list[str]] = []  # 功能模块=全局功能 的册（如对比篮）置底
    for grp in TC_ROOT.iterdir():
        if not grp.is_dir() or grp.name not in grp_order:
            continue
        for b in grp.iterdir():
            if b.is_dir() and any(b.glob("FUNC-*.md")):
                rows = parse_md(b)
                if all(r[1] == "全局功能" for r in rows):
                    global_rows.extend(rows)
                else:
                    booklets[grp.name].append((min_id(rows), rows))
    all_rows: list[list[str]] = []
    for g in grp_order:
        for _, rows in sorted(booklets[g], key=lambda t: t[0]):
            all_rows.extend(rows)
    all_rows.extend(global_rows)

    # 2) 唯一性 + 抽查
    ids = [r[0] for r in all_rows]
    assert len(ids) == len(set(ids)), "用例编号有重复"
    bad = [i for i in ids if not re.match(r"^ZNFWJQ-KJZTFWXT-v1\.0-FUNC-\d{5}$", i)]
    assert not bad, f"编号格式异常: {bad[:5]}"
    empty_content = [r[0] for r in all_rows if not r[7] or not r[10]]
    assert not empty_content, f"测试内容/预期为空: {empty_content[:5]}"

    # 3) 以模板为底，清掉「功能测试用例」数据区（R3 起），写入新行
    wb = openpyxl.load_workbook(TPL)
    ws = wb["功能测试用例"]
    if ws.max_row >= 3:
        ws.delete_rows(3, ws.max_row - 2)
    # 标题行对齐系统名（模板 R1 为门户系统标题，保留模板样式只换文字）
    ws.cell(1, 1).value = "智能服务集群-科技专题服务系统测试用例"
    # 样式参照 R2 表头行/模板示例行的对齐（垂直居中+自动换行），逐行套用
    for i, row in enumerate(all_rows, start=3):
        for c in range(1, 18):
            cell = ws.cell(i, c)
            cell.value = row[c - 1] if row[c - 1] else None
            cell.alignment = openpyxl.styles.Alignment(
                vertical="center", wrap_text=True
            )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)

    # 4) 汇总
    mods: dict[str, int] = {}
    for r in all_rows:
        mods[r[1]] = mods.get(r[1], 0) + 1
    print(f"OK 写入 {len(all_rows)} 条 → {OUT}")
    for m in sorted(mods):
        print(f"  {m}: {mods[m]}")
    gold = sum(1 for r in all_rows if "金样" in (r[16] or ""))
    print(f"  金样(备注含「金样」): {gold}")


if __name__ == "__main__":
    main()

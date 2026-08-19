# -*- coding: utf-8 -*-
"""Inventory 科技信息展示系统 L3–L6 from 功能清单. Read-only."""
from __future__ import annotations

import json
import re
from collections import OrderedDict, Counter
from pathlib import Path

import openpyxl

SRC = Path(r"d:\work\gkx-lumen\原始文档") / (
    "国际科技信息中心项目_需求规格说明书功能清单-智慧服务门户系统、科技信息展示系统、"
    "新型高端智库系统、科技专题服务系统、深度挖掘算法（科技专题服务算法库、语义计算工具库）、"
    "超大规模智算引擎、亿级科技知识图谱引擎、科技情报挖掘与知识服务_v1.2(1).xlsx"
)
OUT = Path(
    r"d:\work\gkx-lumen\gkx-orchestration\agent-delivery\qa\total-set\KJXXZSXT\fp-split-run"
)
EXCLUDE_L3 = "科技信息展示系统数据需求"
EXCLUDE_L4 = "科技抗疫主题报告（核减需求）"


def norm(s) -> str:
    return re.sub(r"\s+", "", str(s or "").strip())


def main() -> None:
    wb = openpyxl.load_workbook(SRC, data_only=True, read_only=True)
    print("sheets", wb.sheetnames)
    name = "科技信息展示系统"
    if name not in wb.sheetnames:
        raise SystemExit(f"missing sheet {name}")
    ws = wb[name]
    rows = list(ws.iter_rows(values_only=True))
    header_idx = 0
    for i, row in enumerate(rows[:8]):
        joined = "".join(str(x or "") for x in row[:20])
        print(f"ROW{i}", [str(x)[:40] if x else "" for x in (list(row)[:15])])
        if "需规功能描述" in joined or "三级功能" in joined:
            header_idx = i
    print("header_idx", header_idx)
    hdr = list(rows[header_idx])
    print("HDR_LEN", len(hdr))
    for j, c in enumerate(hdr):
        if c:
            print(f"  col {j} {openpyxl.utils.get_column_letter(j+1)} = {c}")

    cur = [""] * 6
    excluded_l3 = 0
    excluded_l4 = 0
    kept = []
    l3_set = OrderedDict()
    l4_by_l3 = OrderedDict()
    l5_items = OrderedDict()  # (l3,l4,l5) -> list of (l6, desc)
    skipped_samples = []

    for row in rows[header_idx + 1 :]:
        vals = list(row) + [None] * 20
        # G-L = 6..11 like topic; user said I=L3 J=L4 => I=8 J=9, so G=L1
        levels = [norm(vals[idx]) if vals[idx] else "" for idx in (6, 7, 8, 9, 10, 11)]
        for j, v in enumerate(levels):
            if v:
                cur[j] = v
                for k in range(j + 1, 6):
                    cur[k] = ""
        desc = str(vals[12]).strip() if vals[12] else ""
        if not any(cur) and not desc:
            continue
        l3, l4, l5, l6 = cur[2], cur[3], cur[4], cur[5]
        if EXCLUDE_L3 in l3 or l3 == EXCLUDE_L3:
            excluded_l3 += 1
            if len(skipped_samples) < 8:
                skipped_samples.append(("L3", l3, l4, l5, l6))
            continue
        if EXCLUDE_L4 in l4 or l4 == EXCLUDE_L4:
            excluded_l4 += 1
            if len(skipped_samples) < 8:
                skipped_samples.append(("L4", l3, l4, l5, l6))
            continue
        if not (l5 or l6 or desc):
            continue
        kept.append((l3, l4, l5, l6, desc))
        l3_set[l3] = l3_set.get(l3, 0) + 1
        l4_by_l3.setdefault(l3, OrderedDict())
        l4_by_l3[l3][l4] = l4_by_l3[l3].get(l4, 0) + 1
        l5_items.setdefault((l3, l4, l5), []).append((l6, desc))

    wb.close()

    print("\nKEEP_ROWS", len(kept))
    print("EXCL_L3_ROWS", excluded_l3, "EXCL_L4_ROWS", excluded_l4)
    print("L3_COUNT", len(l3_set))
    for k, n in l3_set.items():
        print(f"  L3 {k} rows={n}")
    print("L4_COUNT", sum(len(v) for v in l4_by_l3.values()))
    for l3, d in l4_by_l3.items():
        print(f"  -- {l3}")
        for l4, n in d.items():
            print(f"     L4 {l4} rows={n}")

    print("L5_COUNT", len(l5_items))
    l6_total = 0
    empty_l6 = 0
    empty_desc = 0
    for (l3, l4, l5), items in l5_items.items():
        n6 = len([x for x in items if x[0]])
        l6_total += len(items)
        if not any(x[0] for x in items):
            empty_l6 += 1
        if not any(x[1] for x in items):
            empty_desc += 1
    print("L6_LEAF_ROWS", l6_total, "L5_without_L6_name", empty_l6, "L5_without_desc", empty_desc)
    print("SKIP_SAMPLES", skipped_samples)

    OUT.mkdir(parents=True, exist_ok=True)
    inv = {
        "keep_rows": len(kept),
        "excl_l3_rows": excluded_l3,
        "excl_l4_rows": excluded_l4,
        "l3": list(l3_set.keys()),
        "l5_count": len(l5_items),
        "l6_leaf_rows": l6_total,
        "tasks": [],
    }
    for i, ((l3, l4, l5), items) in enumerate(l5_items.items(), 1):
        l6s = [x[0] for x in items]
        inv["tasks"].append(
            {
                "id": f"T{i:02d}",
                "l3": l3,
                "l4": l4,
                "l5": l5,
                "l6_count": len(items),
                "l6": l6s,
            }
        )
    (OUT / "_inventory.json").write_text(
        json.dumps(inv, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("wrote", OUT / "_inventory.json")


if __name__ == "__main__":
    main()

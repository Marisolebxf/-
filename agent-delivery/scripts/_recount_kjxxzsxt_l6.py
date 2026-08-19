# -*- coding: utf-8 -*-
"""Recount 科技信息展示系统 leaves after two exclusions."""
from __future__ import annotations

import re
from collections import Counter, OrderedDict
from pathlib import Path

import openpyxl

SRC = Path(r"d:\work\gkx-lumen\原始文档") / (
    "国际科技信息中心项目_需求规格说明书功能清单-智慧服务门户系统、科技信息展示系统、"
    "新型高端智库系统、科技专题服务系统、深度挖掘算法（科技专题服务算法库、语义计算工具库）、"
    "超大规模智算引擎、亿级科技知识图谱引擎、科技情报挖掘与知识服务_v1.2(1).xlsx"
)
EXCLUDE_L3 = "科技信息展示系统数据需求"
EXCLUDE_L4 = "科技抗疫主题报告（核减需求）"


def norm(s) -> str:
    return re.sub(r"\s+", "", str(s or "").strip())


def main() -> None:
    wb = openpyxl.load_workbook(SRC, data_only=True, read_only=True)
    ws = wb["科技信息展示系统"]
    rows = list(ws.iter_rows(values_only=True))
    header_idx = 2
    total = 0
    l3_data = 0
    l4_anti = 0
    l4_anti_inside_l3 = 0
    remain = []
    l3_cnt = Counter()
    l6_name_cnt = Counter()
    slash_l6 = 0
    empty_l6_cell = 0
    has_desc = 0
    seq_blank = 0

    cur = [""] * 6
    for row in rows[header_idx + 1 :]:
        vals = list(row) + [None] * 20
        seq = vals[0]
        levels_raw = [vals[idx] for idx in (6, 7, 8, 9, 10, 11)]
        desc = str(vals[12]).strip() if vals[12] else ""
        if seq is None and not any(levels_raw) and not desc:
            seq_blank += 1
            continue
        total += 1
        levels = [norm(x) if x else "" for x in levels_raw]
        for j, v in enumerate(levels):
            if v:
                cur[j] = v
                for k in range(j + 1, 6):
                    cur[k] = ""
        l3, l4, l5, l6 = cur[2], cur[3], cur[4], cur[5]
        if l3 == EXCLUDE_L3 or EXCLUDE_L3 in l3:
            l3_data += 1
            if l4 == EXCLUDE_L4 or EXCLUDE_L4 in l4:
                l4_anti_inside_l3 += 1
            continue
        if l4 == EXCLUDE_L4 or EXCLUDE_L4 in l4:
            l4_anti += 1
            continue
        remain.append((l3, l4, l5, l6, bool(desc), bool(levels[5]), l6 == "/"))
        l3_cnt[l3] += 1
        l6_name_cnt[l6] += 1
        if l6 == "/":
            slash_l6 += 1
        if not levels[5]:
            empty_l6_cell += 1
        if desc:
            has_desc += 1

    wb.close()
    print("data_rows_with_seq_or_content", total)
    print("blank_skipped", seq_blank)
    print("excl_L3", l3_data)
    print("excl_L4_after_L3", l4_anti)
    print("L4_anti_inside_L3", l4_anti_inside_l3)
    print("remain", len(remain), "expect 606?", len(remain) == 606)
    print("after_L3_before_L4", total - l3_data)
    print("remain_has_desc", has_desc, "slash_l6", slash_l6, "empty_l6_cell_this_row", empty_l6_cell)
    print("unique_l6_names", len(l6_name_cnt))
    print("--- L3 remain ---")
    for k, n in l3_cnt.most_common():
        print(f"  {n:4d}  {k}")

    core = [
        "科技发展态势",
        "科技政策跟踪",
        "科技人才态势",
        "科技数据资源",
        "科技知识图谱",
        "科技成果展示",
        "科技服务全景",
    ]
    zeng_policy = "政策对比功能升级（核增需求）"
    n_core = sum(l3_cnt[k] for k in core)
    n_pol = l3_cnt[zeng_policy]
    n_learn = len(remain) - n_core - n_pol
    print("core", n_core, "policy_zeng", n_pol, "other_zeng", n_learn)
    print("core+policy", n_core + n_pol)


if __name__ == "__main__":
    main()

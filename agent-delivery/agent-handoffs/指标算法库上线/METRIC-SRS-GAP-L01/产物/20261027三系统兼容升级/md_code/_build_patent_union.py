#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""E3 专利去重件数缓存（链×城，申请年≤2024，双角色并集）。

为什么要复用同族快照而不是本批重扫：
  gkx.dwd_patent 是 2,939,895 行的**宽表**（含 content/abstract 等多个大字段），
  名称列无索引，远程实例上按 dwd_id 分片 GROUP BY 实测 10 万行/100 秒量级，
  全表重扫约 40 分钟，且供应商实例有并发限流。因此本批不重扫，改用同族
  M_CHAIN_REG_COMMERCIALIZATION 构建的 `reg5_patent_20261021.json`：
  该快照统计的正是「第一申请人 ∪ 当前专利权人」双角色并集、申请年≤2024，
  其 n_patent_rows = 2,939,895 与 gkx 现表库存行数逐位一致（换库不换数）。

本文件只做两件事：校验行数一致 → 把 union_le2024 层拍平成本指标要用的
`{chain|city: 件数}` 缓存。若日后 gkx 专利表行数变化，此处会直接报错，避免
沿用过期快照。
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SNAP_SRC = ROOT.parent / "20261020_指标整体开发进度调研" / "code" / "_snapshots" / "reg5_patent_20261021.json"
INVENTORY = ROOT / "_work_gkx21" / "GKX_INVENTORY.json"
TAG = "region_index_patent_union.json"


def main():
    inv = json.load(open(INVENTORY, encoding="utf-8"))
    gkx_rows = int(inv["dwd_patent"]["rows"])
    snap = json.load(open(SNAP_SRC, encoding="utf-8"))
    assert int(snap["n_patent_rows"]) == gkx_rows, (
        "专利表行数已变（gkx %d vs 快照 %d），不可沿用快照" % (gkx_rows, snap["n_patent_rows"]))
    flat = {}
    for ch, cells in snap["cells"]["union_le2024"].items():
        for city, n in cells.items():
            flat["%s|%s" % (ch, city)] = int(n)
    out = HERE / "_snapshots21" / TAG
    out.write_text(json.dumps(flat, ensure_ascii=False), encoding="utf-8")
    print("wrote", out, "cells", len(flat), "gkx_rows", gkx_rows)


if __name__ == "__main__":
    sys.exit(main())

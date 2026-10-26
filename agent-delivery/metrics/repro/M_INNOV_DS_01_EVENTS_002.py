#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_DS_01_EVENTS_002 · 创新事件影响力（20261021 改源：三方库 gkx）。

改源要点
--------
1. 唯一数据源 `gkx.dwd_policy_base`（20,000 行），删除 `_devdb` 与 demo 库引用。
2. `rank` 为 JSON 数组字符串，按 国家级4 > 省级3 > 市级2 > 区县级/园区级1 > 其他0 取 max；
   实测 10,602 行为国家级（`["国家级"]`），与开发库一致，非换库缺口。
3. 地理覆盖 geo = 省 + 市 + 区县 三级中「有效非占位」的级数（0~3）。
4. 影响力 = 100 × (层级标准化 + 地理覆盖标准化 + 主题有无标准化) / 3，等权，与旧版一致。
5. 事件单元仍为政策 id；同题多行（53 组 / 55 行）不并，`dedup_audit` 披露。
"""
from __future__ import annotations

import json
import statistics
from pathlib import Path

import _innov_events_21 as E

HERE = Path(__file__).resolve().parent
MID = "M_INNOV_DS_01_EVENTS_002"

rows = E.load_policy()
scored = E.score_influence(rows)
n = len(scored)
by_s = [x["influence_score"] for x in scored]
dist = E.level_dist(rows)

res = {
    "metric_id": MID,
    "data_source": "gkx.dwd_policy_base",
    "n_events": n,
    "n_scored": n,
    "coverage": round(n / n, 4),
    "stats": {
        "score_min": min(by_s), "score_max": max(by_s),
        "score_avg": round(sum(by_s) / n, 2),
        "score_median": round(sorted(by_s)[n // 2], 2),
        "score_std": round(statistics.pstdev(by_s), 2),
        "n_score_ge_60": sum(1 for x in by_s if x >= 60),
        "n_score_ge_80": sum(1 for x in by_s if x >= 80),
    },
    "level_dist": dist,
    "dims": {
        "national": dist["国家级"],
        "provincial": dist["省级"],
        "city": dist["市级"],
        "geo0": sum(1 for r in rows if r["geo"] == 0),
        "geo3": sum(1 for r in rows if r["geo"] == 3),
        "theme_valid": sum(r["theme"] for r in rows),
    },
    "top10": scored[:10],
    "dedup_audit": E.dedup_audit(rows),
    "notes": [
        "层级字段是 JSON 数组，一个事件可同时挂多级，取 max 后国家级占比 53.0%（10,602/20,000）。",
        "theme 全库仅 2 条有效、quote_policy 仅 2 条，故 theme 维度对本指标几乎无区分度；"
        "改源前后取值相同，属 gkx 镜像一致，不是换库损失。",
    ],
}

out = HERE / f"{MID}_out.json"
out.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[{MID}] n={n} avg={res['stats']['score_avg']} max={res['stats']['score_max']} "
      f"国家级={dist['国家级']} -> {out.name}")

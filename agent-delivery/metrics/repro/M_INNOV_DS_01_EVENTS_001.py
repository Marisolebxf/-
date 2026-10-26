#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_DS_01_EVENTS_001 · 创新事件关注度（20261021 改源：三方库 gkx）。

改源要点
--------
1. 唯一数据源 `gkx.dwd_policy_base`（20,000 行），删除 `_devdb` 与 demo 库引用。
2. 正文长度先剔占位符 `'NULL'`（content 797 行 / abstract 7,841 行为字面量 NULL）。
3. 事件单元仍为政策文件 id；`dedup_audit` 披露同题多行（53 组 / 55 行），
   不按 title 去重（通用题名会错并），详见共用算路说明。
4. 公式与旧版一致：关注度 = 100 × (正文标准化 + 主题有无 + 引用有无) / 3，等权。
"""
from __future__ import annotations

import json
import statistics
from pathlib import Path

import _innov_events_21 as E

HERE = Path(__file__).resolve().parent
MID = "M_INNOV_DS_01_EVENTS_001"

rows = E.load_policy()
scored = E.score_attention(rows)
n = len(scored)

by_s = [x["attention_score"] for x in scored]
body = E.body_stats(rows)

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
        "n_score_eq_50": sum(1 for x in by_s if x == 50.0),
    },
    "body_len": body,
    "dims": {
        "theme_valid": sum(r["theme"] for r in rows),
        "quote_valid": sum(r["quote"] for r in rows),
    },
    "top10": scored[:10],
    "dedup_audit": E.dedup_audit(rows),
    "notes": [
        "score=50.0 的点是三维全部缺失的退化解（正文=0、theme=0、quote=0），非真实中位。",
        "gkx 未提供阅读/转载/搜索指数，关注度只能由正文规模+主题+引用三项代理，与旧版同口径。",
    ],
}

out = HERE / f"{MID}_out.json"
out.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[{MID}] n={n} avg={res['stats']['score_avg']} max={res['stats']['score_max']} -> {out.name}")

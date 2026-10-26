#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""当前分析机构数（M_SVC_ORG_SELECTED_COUNT）—— 已废止，gkx 口径无源。

本 ID 不是统计指标：页面「当前分析 N 家」= 前端会话勾选集合的 length，
既无总体、也无参考期、也无跨用户可比性。2026-10-13 徐滕强拍板废止。

本脚本不计算任何数，只把「不可算/不应算」的结构事实落盘：
    - gkx 无 svc_* 表，无机构池/结果面可承载会话态；
    - 本件人口池 44,153（与同域各件同池）只能作「存量替代」的候选，
      而存量替代与 selection.length 的相关性应为 0，不能冒充本指标。
产出：code/M_SVC_ORG_SELECTED_COUNT_out.json（覆盖写）
运行：cd code && python3 M_SVC_ORG_SELECTED_COUNT.py
"""
from __future__ import annotations

import json
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
OUT = os.path.join(HERE, "M_SVC_ORG_SELECTED_COUNT_out.json")


def main() -> None:
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    n = len(f["pool"])

    out = {
        "metric_id": "M_SVC_ORG_SELECTED_COUNT",
        "metric_name": "当前分析机构数",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "完全不支持",
        "judgment_reason": (
            "不适用（已废止）：页面 N = 前端会话 selection.length，不是统计指标；"
            "gkx 无 svc_* 表，无会话态承载，也不应为它灌数。"
            "存量替代（44,153）与 selection.length 的相关性按定义为 0，不能冒充"),
        "status": "retired",
        "retired_at": "2026-10-13",
        "retired_by": "徐滕强",
        "retired_reason": "前端会话勾选计数非指标；无总体、无参考期、无跨用户可比性",
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "（无承载表；gkx 无 svc_* 表族）", "rows": 0,
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "不适用：会话语义无参考期。若改为「机构关注度」类产品行为指标，"
            "须另立条目并重新定义总体/参考期/去重规则，不能沿用本 ID"),
        "metric_identity": {
            "has_population": False,
            "has_reference_period": False,
            "has_dedup_rule": False,
            "persistent": False,
            "cross_user_comparable": False,
            "source": "前端内存 selection 数组",
        },
        "counterfactual_candidates": [
            {"option": "存量机构总数", "value": n,
             "what_it_measures": "在册服务机构总家数",
             "why_not": "恒定值，与用户勾选无关，方差=0"},
            {"option": "深圳子池", "value": sum(1 for v in f["pool"].values() if v.get("city") == "深圳市"),
             "what_it_measures": "深圳在池机构数",
             "why_not": "同上，只是换分母"},
            {"option": "埋点日均勾选", "value": None,
             "what_it_measures": "用户交互强度",
             "why_not": "需前端埋点，属产品行为指标，非产业统计"},
        ],
        "evidence": {
            "gkx_svc_tables": 0,
            "result_rows_for_this_id": 0,
            "note": ("gkx 280 表中无 svc_* 表族；本 ID 在旧库结果面按 metric_id 过滤恒 0 行，"
                     "且 0 行是设计态、不是数据缺失"),
        },
        "gaps": {
            "object": "指标对象不合法（会话集合不是统计总体）",
            "repair": "无需补数；若甲方要「机构关注度」，另立埋点类产品指标",
        },
        "compute": {"status": "retired", "elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("retired; pool=%d; no computable value -> %s" % (n, OUT))


if __name__ == "__main__":
    main()

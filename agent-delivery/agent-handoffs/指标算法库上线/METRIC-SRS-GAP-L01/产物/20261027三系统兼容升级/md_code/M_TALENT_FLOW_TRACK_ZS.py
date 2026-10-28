#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TALENT_FLOW_TRACK_ZS 人才流动追踪（展示侧拆分件） —— 20261027 D2 拆分新件（数据结构契约件）

【适用系统】科技信息展示系统（本件只服务本系统；同名原 ID 归科技专题服务算法库）
【维护者】唐绍祖
【同名指标族·互见】
  - M_TALENT_FLOW_TRACK（原 ID·算法库计算模型）: ../第三方库指标计算过程/M_TALENT_FLOW_TRACK.md ｜ code/M_TALENT_FLOW_TRACK.py
  - M_TALENT_FLOW_TRACK_ZS（本件·科技信息展示系统）     : 本文件
  - M_TALENT_FLOW_TRACK_ZT（科技专题系统）   : ../第三方库指标计算过程/M_TALENT_FLOW_TRACK_ZT.md
【拆分判定】D2 不可兼容 → 拆分。理由：算法库需自建完整流动口径（人×次×期）vs 系统侧只要轨迹聚合视图（净流入数/迁徙可视化），粒度无法同一接口表达
  判定依据与全族映射表：../过程文件/02_D2兼容判定与拆分_总结.md

三系统调用注意（后端必读）
--------------------------
1. 科技信息展示系统后端：只接本件；不要调原 ID M_TALENT_FLOW_TRACK（口径/形态不同，见 md「拆分判定」）。
2. 科技信息展示系统后端：消费 detail/display 段做页面渲染；数值引擎按契约回填后经本接口读取。不要把本件当计算接口串进算法链路。
3. 缺参走缺省行为，assumptions 会声明；产物只由本脚本产出（B7）。

本件口径（数据结构契约件）
--------------------
展示侧轨迹聚合视图契约：净流入数+迁徙路径（Sankey/地图）
"""
from __future__ import annotations

import json
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "M_TALENT_FLOW_TRACK_ZS_out.json"
ORIG_OUT = HERE / "M_TALENT_FLOW_TRACK_out.json"

APPLICABLE = ['科技信息展示系统']

# 缺省参数（md「入参兼容策略」表与此一一对应）
DEFAULTS = {
    "q": None,               # 查询关键词/筛选条件（企业/产业/期间）；None → 全量结构返回
    "period": None,          # 报告期/时间窗（引擎件用）；None → 最近披露期
    "limit": 50,             # 列表条数上限（展示页分页用）
    "with_orig_probe": False,  # 调试：附原 ID 探针结论对照（正式调用不要开）
}


def compute(params: dict | None = None) -> dict:
    """科技信息展示系统统一入口（数据结构契约件）。参数语义见模块 docstring；缺参行为在 assumptions 声明。"""
    p_in = dict(params or {})
    p = {**DEFAULTS, **{k: v for k, v in p_in.items() if v is not None}}
    assumptions = ["本件为 D2 拆分新件（数据结构契约件），口径=系统侧需求原文，与原 ID M_TALENT_FLOW_TRACK 独立验收",
                   "数值不预置：结构/契约件；引擎件数值按运行时参数由后端计算回填后经本接口读取"]

    orig_summary = None
    if ORIG_OUT.exists():
        try:
            od = json.loads(ORIG_OUT.read_text(encoding="utf-8"))
            orig_summary = {"metric_id": od.get("metric_id"),
                             "support_judgment": str(od.get("support_judgment"))[:80]}
        except Exception:
            orig_summary = None
    if p["with_orig_probe"] and orig_summary:
        assumptions.append("with_orig_probe=True 仅调试对照用，不要在生产链路开启")

    t0 = time.time()
    result = {
        "metric_id": "M_TALENT_FLOW_TRACK_ZS",
        "metric_name": "人才流动追踪（展示侧拆分件）",
        "applicable_systems": APPLICABLE,
        "split_family": {"origin_id": "M_TALENT_FLOW_TRACK", "origin_path": "code/M_TALENT_FLOW_TRACK.py",
                          "this_path": "code/M_TALENT_FLOW_TRACK_ZS.py",
                          "sibling": "M_TALENT_FLOW_TRACK_ZT",
                          "md_origin": "第三方库指标计算过程/M_TALENT_FLOW_TRACK.md",
                          "md_this": "第三方库指标计算过程/M_TALENT_FLOW_TRACK_ZS.md"},
        "params_effective": p,
        "assumptions": assumptions,
        "value": None,
        "detail": {
            "contract": "展示侧轨迹聚合：净流入数+迁徙路径",
            "fields": ["区域对(源→目的)", "净流入", "路径权重", "期间"],
            "note": "字段契约在此固定；后端按契约落库/回填，本件不自动计算",
        },
        "display": {
            "view": {"cols": ["源区域", "目的区域", "净流入"], "rows": []},
            "consumer": "展示系统迁徙轨迹图",
        },
        "origin_baseline": orig_summary,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "elapsed_sec": round(time.time() - t0, 3),
    }
    return result


def main():
    r = compute()
    OUT.write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    print("[ok] M_TALENT_FLOW_TRACK_ZS value =", r["value"], "wrote", OUT.name)


if __name__ == "__main__":
    main()

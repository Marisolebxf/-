#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_REVENUE_LATEST_ZS 最新营收（展示侧拆分件） —— 20261027 D2 拆分新件（系统侧口径引擎件）

【适用系统】科技信息展示系统（本件只服务本系统；同名原 ID 归科技专题服务算法库）
【维护者】唐绍祖
【同名指标族·互见】
  - M_ENT_REVENUE_LATEST（原 ID·算法库计算模型）: ../第三方库指标计算过程/M_ENT_REVENUE_LATEST.md ｜ code/M_ENT_REVENUE_LATEST.py
  - M_ENT_REVENUE_LATEST_ZS（本件·科技信息展示系统）     : 本文件
  - M_ENT_REVENUE_LATEST_ZT（科技专题系统）   : ../第三方库指标计算过程/M_ENT_REVENUE_LATEST_ZT.md
【拆分判定】D2 不可兼容 → 拆分。理由：「哪一期算最新」的权威选择权冲突：算法库固定最新报告期规则 vs 系统侧用户可切换报告期口径
  判定依据与全族映射表：../过程文件/02_D2兼容判定与拆分_总结.md

三系统调用注意（后端必读）
--------------------------
1. 科技信息展示系统后端：只接本件；不要调原 ID M_ENT_REVENUE_LATEST（口径/形态不同，见 md「拆分判定」）。
2. 科技信息展示系统后端：消费 detail/display 段做页面渲染；数值引擎按契约回填后经本接口读取。不要把本件当计算接口串进算法链路。
3. 缺参走缺省行为，assumptions 会声明；产物只由本脚本产出（B7）。

本件口径（系统侧口径引擎件）
--------------------
同 _ZT（展示侧共用报告期切换契约）
"""
from __future__ import annotations

import json
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "M_ENT_REVENUE_LATEST_ZS_out.json"
ORIG_OUT = HERE / "M_ENT_REVENUE_LATEST_out.json"

APPLICABLE = ['科技信息展示系统']

# 缺省参数（md「入参兼容策略」表与此一一对应）
DEFAULTS = {
    "q": None,               # 查询关键词/筛选条件（企业/产业/期间）；None → 全量结构返回
    "period": None,          # 报告期/时间窗（引擎件用）；None → 最近披露期
    "limit": 50,             # 列表条数上限（展示页分页用）
    "with_orig_probe": False,  # 调试：附原 ID 探针结论对照（正式调用不要开）
}


def compute(params: dict | None = None) -> dict:
    """科技信息展示系统统一入口（系统侧口径引擎件）。参数语义见模块 docstring；缺参行为在 assumptions 声明。"""
    p_in = dict(params or {})
    p = {**DEFAULTS, **{k: v for k, v in p_in.items() if v is not None}}
    assumptions = ["本件为 D2 拆分新件（系统侧口径引擎件），口径=系统侧需求原文，与原 ID M_ENT_REVENUE_LATEST 独立验收",
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
        "metric_id": "M_ENT_REVENUE_LATEST_ZS",
        "metric_name": "最新营收（展示侧拆分件）",
        "applicable_systems": APPLICABLE,
        "split_family": {"origin_id": "M_ENT_REVENUE_LATEST", "origin_path": "code/M_ENT_REVENUE_LATEST.py",
                          "this_path": "code/M_ENT_REVENUE_LATEST_ZS.py",
                          "sibling": "M_ENT_REVENUE_LATEST_ZT",
                          "md_origin": "第三方库指标计算过程/M_ENT_REVENUE_LATEST.md",
                          "md_this": "第三方库指标计算过程/M_ENT_REVENUE_LATEST_ZS.md"},
        "params_effective": p,
        "assumptions": assumptions,
        "value": None,
        "detail": {
            "contract": "报告期切换查询：企业→期→值（年报/季报/最近披露三口径，用户可选）",
            "fields": ["企业", "报告期口径", "期间", "营收值", "单位"],
            "note": "字段契约在此固定；后端按契约落库/回填，本件不自动计算",
        },
        "display": {
            "view": {"cols": ["企业", "营收", "期", "单位自适应"], "rows": []},
            "consumer": "展示系统营收展示卡",
        },
        "origin_baseline": orig_summary,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "elapsed_sec": round(time.time() - t0, 3),
    }
    return result


def main():
    r = compute()
    OUT.write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    print("[ok] M_ENT_REVENUE_LATEST_ZS value =", r["value"], "wrote", OUT.name)


if __name__ == "__main__":
    main()

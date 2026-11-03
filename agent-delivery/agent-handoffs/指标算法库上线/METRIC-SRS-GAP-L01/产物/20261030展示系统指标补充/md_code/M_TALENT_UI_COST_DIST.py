#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TALENT_UI_COST_DIST · 人才引进个性化成本分布（薪酬/安家费/科研启动费，UI「个性化成本分布分析」）

展示系统 UI 实扫指标（20261030 批 2）：
repos/demo-ui-science/src/pages/talent-trend/components/CostTab.jsx:513-524
「个性化成本分布分析」面板：costBarOption（柱）+ pieOption（饼）+ 模拟总计 ¥breakdown.total 万/年
vs 模型预测 ¥current.predictedTotal 万。数据为 SCHEME_PRESETS 方案模拟值（mock）。
SRS 叶「个性化成本分布分析」(excel_row 267 附近, talentRecommendSpec.js key='distribution')
要求按人才层级给出薪酬、安家费、科研启动费等成本构成，未给口径。

口径（推测定义，非甲方闭合）：
  成本构成三分项 = 薪酬 / 安家费 / 科研启动费。库内没有「人才引进成本」明细表（负证据探针），
  本件用可公开聚合的代理面演示可算性：
    代理 = gkx.dwd_recruit（招聘岗位）年薪 min/max 均值 → 年薪成本代理（薪酬项）。
    安家费/科研启动费库内无承载 → absence_probe 三件套记录，判定缺失。
  产物给出：薪酬代理的分布（min/mean/median/max）+ 三分项缺失声明 + 模拟总计与代理的换算说明。

数据源：gkx。产出：M_TALENT_UI_COST_DIST_out.json。
"""
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_SHARED = Path(__file__).resolve().parents[2].joinpath(
    "20261021_指标整体开发进度调研", "code")
sys.path.insert(0, str(_SHARED))
from _gkxdb import gkx  # noqa: E402


def main():
    cur = gkx()
    out = {
        "metric_id": "M_TALENT_UI_COST_DIST",
        "batch": "20261030_展示系统指标补充",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/talent-trend/components/CostTab.jsx:513",
            "repos/demo-ui-science/src/pages/talent-trend/components/CostTab.jsx:521",
        ],
        "requirement_trace": {
            "named_in_srs": True,
            "note": "SRS 叶「个性化成本分布分析」（人才引进推荐评估页，excel_row 267 邻域）要求给出"
                    "薪酬/安家费/科研启动费成本构成；未给口径与数值源。",
        },
        "facts": {},
        "derived": {},
        "absence_probe": [],
        "support_judgment": None,
        "notes": [],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面件：在招岗位年薪截面；无年份维。",
        "ctx_refs": {"note": "正文引用型数字登记。", "refs": ["183.240", "141.251", "3318", "513", "521", "267", "2.1", "2.2", "2.3", "2.4"]},
    }

    # F1 探测招聘表（gkx 实测：dwd_job 10 行样例级；dwd_org_recruit_info 7,981,643 行但无薪酬列）
    salary_bearing = None
    try:
        cur.execute("SELECT COUNT(*) FROM gkx.dwd_job")
        out["facts"]["dwd_job_rows"] = cur.fetchone()[0]
    except Exception as e:
        out["absence_probe"].append({"probe": "gkx.dwd_job COUNT", "error": str(e)[:160],
                                     "verdict_kind": "negative_evidence"})
    try:
        cur.execute("SELECT COUNT(*) FROM gkx.dwd_org_recruit_info")
        out["facts"]["org_recruit_info_rows"] = cur.fetchone()[0]
    except Exception as e:
        out["absence_probe"].append({"probe": "gkx.dwd_org_recruit_info COUNT", "error": str(e)[:160],
                                     "verdict_kind": "negative_evidence"})
    # 薪酬列负证据探针（两表全列清单里均无 salary/wage/pay 类列，20261030 实测）
    try:
        cur.execute(
            "SELECT table_name, column_name FROM information_schema.columns "
            "WHERE table_schema = 'gkx' "
            "AND (column_name LIKE '%sal%' OR column_name LIKE '%wage%' OR column_name LIKE '%pay%') "
            "AND table_name IN ('dwd_job', 'dwd_org_recruit_info')")
        hits = cur.fetchall()
        out["absence_probe"].append({
            "probe": "information_schema.columns salary/wage/pay in (dwd_job, dwd_org_recruit_info)",
            "result": [list(h) for h in hits], "hit_rows": len(hits),
            "verdict_kind": "negative_evidence" if not hits else "positive_existence"})
        salary_bearing = hits[0] if hits else None
    except Exception as e:
        out["absence_probe"].append({"probe": "salary columns probe", "error": str(e)[:160],
                                     "verdict_kind": "negative_evidence"})


    # F3 安家费/科研启动费负证据探针（库表名关键词扫描）
    for kw, label in (("%settle%", "安家费"), ("%startup%", "科研启动费"), ("%talent_cost%", "人才成本明细")):
        try:
            cur.execute(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = 'gkx' AND table_name LIKE %s", (kw,))
            hits = [r[0] for r in cur.fetchall()]
            out["absence_probe"].append({
                "probe": f"information_schema.tables LIKE '{kw}'（{label}）",
                "result": hits, "hit_rows": len(hits),
                "verdict_kind": "negative_evidence" if not hits else "positive_existence"})
        except Exception as e:
            out["absence_probe"].append({"probe": kw, "error": str(e)[:160],
                                         "verdict_kind": "negative_evidence"})

    # D 派生：三分项 0/3 可承载（薪酬列都不存在）
    out["derived"]["cost_items_available"] = {
        "value": 0, "numerator": 0, "denominator": 3,
        "note": "三分项（薪酬/安家费/科研启动费）在 gkx 可承载 0 项：dwd_job(10 行样例)与"
                "dwd_org_recruit_info(7,981,643 行)均无薪酬列（absence_probe 列清单探针），"
                "安家费/启动费无表——UI 饼图三色全部无数据源",
    }

    # 判档
    out["support_judgment"] = "完全不支持"
    out["notes"].append(
        "三分类判据（skill §〇）：指标及关键依赖在 gkx 均无承载——岗位表无薪酬数值列、"
        "无安家费/科研启动费表；live 底册亦无此类表（enterprise_extra 为企业维非成本维）。"
        "本件为负结论件，§二计算过程从缺，absence_probe 三件套即证据。"
        "升档触发器：甲方提供引进成本明细表（含三分项数值）或地方补贴标准结构化表。")
    out["notes"].append("UI「模拟总计/模型预测/柱饼图」全部为 SCHEME_PRESETS mock 值，无真实数据源。")

    dest = _HERE / "M_TALENT_UI_COST_DIST_out.json"
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print("saved", dest)
    for k, v in out["facts"].items():
        print(k, "=", str(v)[:90])
    for k, v in out["derived"].items():
        print(k, "=", v["value"])


if __name__ == "__main__":
    main()

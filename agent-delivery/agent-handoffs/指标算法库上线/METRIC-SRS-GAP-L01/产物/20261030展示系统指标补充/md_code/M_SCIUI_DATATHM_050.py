#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_050 需求方月活跃天数占比（活跃天数/30 天）——产物生成（S3-05 L1）。

双挂载：ApplicationWindow.jsx:235（活跃度 Progress，Math.round(activeDays/30*100)）
+ global-innovation/tabs/InnovationRealtime.jsx:67（impactBreakdown 活跃度因子——
创新实时地图影响度分解的「活跃度」子项，0.45 权重——语义远亲，挂靠披露）。
049 已做全部原料探针（调用日志三源排除+sys_log 语义双排除+admin 9 天观察）。
本件零新探针（049 全复用），增量=mock 折算核验（activeDays/30 四舍五入 vs Progress 值）
与 InnovationRealtime:67 的 0.45/0.28/0.18 权重披露。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_050_out.json")

d049 = json.load(open(os.path.join(BASE, "M_SCIUI_DATATHM_049_out.json"), encoding="utf-8"))

# —— mock 折算核验（B1/B3：分子 activeDays / 分母 30 常量，四舍五入对照 Progress 渲染值）——
mock_rows = d049["facts"]["ui_mock_demander_active_days"]  # [name, activeDays, avgDaily]
MONTH_BASE = 30
mock_pct = [[name, days, round(days / MONTH_BASE * 100)] for name, days, _ in mock_rows]  # (B5 按 activeDays 降序继承 049)
mock_pct_range = [mock_pct[-1][2], mock_pct[0][2]]  # min/max（升序）

# —— InnovationRealtime.jsx:67 权重披露（实抄 :63-70 impactBreakdown）——
innov_weights = [["活跃度", 0.45], ["关联强度", 0.28], ["领域权重", 0.18]]  # 合计 0.91（非 1.0——披露）

facts = {
    "dev_call_tables_reused_041": d049["facts"]["dev_call_tables_reused_041"],
    "gkx_table_count": d049["facts"]["gkx_table_count"],
    "jiuxin_table_count_live": d049["facts"]["jiuxin_table_count_live"],
    "dev_sys_log_rows_reused_041": d049["facts"]["dev_sys_log_rows_reused_041"],
    "dev_sys_log_user_days_oct_reused_049": d049["facts"]["dev_sys_log_user_days_oct"],
    "ui_mock_active_days_reused_049": mock_rows,
    "ui_month_base_const": MONTH_BASE,
    "ui_mock_active_pct_calc": mock_pct,
    "ui_mock_active_pct_min": mock_pct_range[0],
    "ui_mock_active_pct_max": mock_pct_range[1],
    "ui_innov_impact_weights": innov_weights,
    "ui_innov_weights_sum": round(sum(w for _, w in innov_weights), 2),
    "admin_oct_days_reused_049": d049["derived"][1]["value"],
}

derived = [
    {
        "key": "demander_monthly_active_days_ratio",
        "value": None,
        "numerator": None, "denominator": None,
        "note": "『需求方月活跃天数占比』正式口径（月活跃天数÷月天数）分子依赖调用日志（三源零承载，049 复用）；分母月天数（30/31/当月实际天数）无裁定——UI 硬编码 30 是前端常量非口径；按 B10 不写伪指标值"
    },
    {
        "key": "admin_active_days_ratio_observed_oct",
        "value": round(d049["derived"][1]["value"] / 31 * 100, 1),
        "numerator": d049["derived"][1]["value"],
        "denominator": 31,
        "note": "附带交付（非需求方占比，语义双排除同 049）：admin 2026-10 窗 9 天 ÷ 10 月实际 31 天 = 29.0%——分母用实际天数 31（与 UI 的 30 常量分叉披露，B9）；管理 OAuth 面参考位",
    },
]

absence_probe = [
    {
        "probe": "分子原料（月活跃天数）——调用日志三源",
        "source": "dev/gkx/jiuxin",
        "sql": "049 全套复用（call 词族 0 张×3 + sys_log 语义双排除）",
        "hits": 0,
        "hit_detail": "分子零承载（049 同锚：调用族五件统一根因）；sys_log admin 9 天语义双排除（OAuth 99.4%+系统账号）——分子既无正式源亦无合规代理"
    },
    {
        "probe": "分母口径（月天数 30 vs 31）——需求与前端常量",
        "source": "doc/ui",
        "sql": "rg 检索三份需求真源 + ApplicationWindow.jsx:235 实读",
        "hits": 0,
        "hit_detail": "需求无月天数口径；UI 硬编码 30（Math.round(r.activeDays/30*100)）——2026-10 实际 31 天，mock 语境「5月」31 天：30 常量在两种月长下都偏差（31 天月低估 3.2%）；分母未裁定"
    },
    {
        "probe": "第二挂载 InnovationRealtime.jsx:67 语义核对",
        "source": "ui",
        "sql": "sed 实读 :55-80（impactBreakdown 构造）",
        "hits": 1,
        "hit_detail": "创新实时地图影响度分解 impactBreakdown=[活跃度 0.45/关联强度 0.28/领域权重 0.18]——是影响度合成因子的子项（baseValue*0.45 派生），与「需求方月活跃天数占比」语义远亲（不同域不同义）；权重合计 0.91≠1（未归一，披露）；挂靠登记不作依赖"
    },
]

doc = {
    "metric_id": "M_SCIUI_DATATHM_050",
    "batch": "S3-05",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:235",
        "repos/demo-ui-science/src/pages/global-innovation/tabs/InnovationRealtime.jsx:67",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:978",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "指标名级 0 命中；主挂载「活跃度」Progress 列（ApplicationWindow demanderColumns 尾列）为 049 活跃天数的派生展示（/30 折算）；第二挂载 InnovationRealtime:67 为创新地图影响度因子——语义远亲仅登记；seq 393/394 挂靠同 049"
    },
    "base_years_used": [],
    "base_years_missing": ["完全不支持：三源零承载，无库内年份基期"],
    "base_years_note": "完全不支持：无基期；mock 演示值不构成基期证据",
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": "完全不支持",
    "notes": [
        "判档：分子（活跃天数）三源零承载（049 全复用）——比值在分子断时整体断；分母（月天数）未裁定是次生缺口",
        "B11 对账：全套原料键=049 同键同值（零新探针）；admin 9 天=049 derived[1]",
        "B9 双分母披露：UI 30 常量 vs 实际 31 天（10 月）——附带键分母取 31 并标注；mock 折算值全按 30 列示（与前端渲染一致）",
        "InnovationRealtime:67 权重披露：0.45/0.28/0.18 合计 0.91 非归一——影响度合成分自身的未闭合，另证展示层演示值不成体系",
    ],
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
print("mock pct range:", mock_pct_range, "| admin ratio:", derived[1]["value"])
print("support:", doc["support_judgment"])

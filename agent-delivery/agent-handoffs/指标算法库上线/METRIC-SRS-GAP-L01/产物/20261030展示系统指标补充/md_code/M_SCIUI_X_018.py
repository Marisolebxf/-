#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_X_018 主体产值增长率（年）—— 三源探针 + 复现脚本（批 S3-02，Lane 2）。

UI 挂载（实查）：
  repos/demo-ui-science/src/pages/tech-innovation-evaluation/TechInnovationEvaluationPage.tsx:321
    industryWeights [{ key: 'output', label: '产值增长', weight: 20 }] —— 产业发展潜力
    权重组第 3 维（20%）；评估流程加权计算入口 weightedScore()
  （471 导出 l3「产值增长」，cat 无业务逻辑数值类，mean：某指标随时间上升/下降，
    和上年同期比还是和上一期比见指标名称——本件名明「（年）」=同比口径）

三源产值面（与 X_027 共用探针，本件聚焦增长率可算性）：
  ① 开发库：enterprise_finance_history 972 机构中 971 家有 ≥2 年营收（YoY 可算）——主承载
  ② gkx：dwd_org_annual_financial_info 451 家 ≥2 年营收（对照面）
  ③ 久新：无企业营收面（X_027 absence 同证）

复现口径（B10 双口径）：
  口径 A（机构级同比·主口径）：org×year 去重（同对多行取均值）后 YoY 分布
  口径 B（聚合面同比·对照）：年营收和的 YoY（X_027 口径 A 延伸，机构构成变动的混合效应披露）
"""
import json
import os
import sys

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           connect_timeout=20, read_timeout=180)

facts = {}
absence_probe = []


def q1(cur, sql):
    cur.execute(sql)
    r = cur.fetchone()
    return int(r[0]) if r else 0


dev = pymysql.connect(**DEV)
dc = dev.cursor()

facts["dev_finance_history_rows"] = 40239  # X_027 同源 assert（B11 零漂移）
assert q1(dc, "SELECT COUNT(*) FROM gkxlumenx_dwd.enterprise_finance_history") == \
    facts["dev_finance_history_rows"]
facts["dev_finance_orgs_multiyear_rev"] = q1(
    dc, "SELECT COUNT(*) FROM (SELECT org_id FROM gkxlumenx_dwd.enterprise_finance_history "
        "WHERE revenue IS NOT NULL AND revenue>0 GROUP BY org_id "
        "HAVING COUNT(DISTINCT data_year)>=2) t")

# ---- 口径 A：机构级同比 ----
# org×year 去重（同对多行取均值，对冲 dup=4 多报表源），Python 侧算 YoY（B5 确定性排序）
dc.execute(
    "SELECT org_id, data_year, AVG(revenue) avg_rev FROM gkxlumenx_dwd.enterprise_finance_history "
    "WHERE revenue IS NOT NULL AND revenue>0 AND data_year BETWEEN 2019 AND 2025 "
    "GROUP BY org_id, data_year ORDER BY org_id, data_year")
by_org = {}
for org_id, yr, rev in dc.fetchall():
    by_org.setdefault(org_id, {})[int(yr)] = float(rev)

yoy_pairs = []  # (org, prev_y, cur_y, growth)
for org_id, ym in by_org.items():
    years = sorted(ym)
    for prev_y, cur_y in zip(years, years[1:]):
        prev, cur = ym[prev_y], ym[cur_y]
        if prev > 0:
            yoy_pairs.append((org_id, prev_y, cur_y, (cur - prev) / prev * 100))

facts["dev_yoy_pairs_total"] = len(yoy_pairs)
facts["dev_yoy_orgs"] = len(by_org)

# 年度同比分布（相邻年对）
pair_dist = {}
for _, py, cy, g in yoy_pairs:
    pair_dist.setdefault(cy, []).append(g)
yearly_stats = []
for cy in sorted(pair_dist):
    gs = sorted(pair_dist[cy])
    n = len(gs)
    yearly_stats.append({
        "year": cy, "n_orgs": n,
        "median_pct": round(gs[n // 2], 2),
        "mean_pct": round(sum(gs) / n, 2),
        "p90_pct": round(gs[int(n * 0.9)], 2),
        "p10_pct": round(gs[int(n * 0.1)], 2)})
facts["dev_yoy_yearly_stats"] = yearly_stats

# 2024 vs 2023 主读数（UI 评估年相邻对）
g24 = sorted(g for _, py, cy, g in yoy_pairs if cy == 2024)
facts["dev_yoy_2024_median_pct"] = round(g24[len(g24) // 2], 2) if g24 else None
facts["dev_yoy_2024_mean_pct"] = round(sum(g24) / len(g24), 2) if g24 else None
facts["dev_yoy_2024_n_orgs"] = len(g24)
facts["dev_yoy_2024_negative_share_pct"] = round(
    sum(1 for g in g24 if g < 0) / len(g24) * 100, 2) if g24 else None

# Top5 增长/下滑样本（极端值披露）
g24_all = sorted([(g, o) for o, py, cy, g in yoy_pairs if cy == 2024], key=lambda x: -x[0])
facts["dev_yoy_2024_top5_growth"] = [{"org_id": o[:12], "growth_pct": round(g, 2)}
                                     for g, o in g24_all[:5]]
facts["dev_yoy_2024_bottom5_decline"] = [{"org_id": o[:12], "growth_pct": round(g, 2)}
                                         for g, o in g24_all[-5:]]

# ---- 口径 B：聚合面同比（X_027 延伸） ----
dc.execute(
    "SELECT data_year, SUM(revenue) FROM gkxlumenx_dwd.enterprise_finance_history "
    "WHERE revenue IS NOT NULL AND revenue>0 AND data_year BETWEEN 2019 AND 2025 "
    "GROUP BY data_year ORDER BY data_year")
agg = {int(r[0]): float(r[1]) for r in dc.fetchall()}
agg_yoy = [{"year": cy, "aggregate_yoy_pct": round((agg[cy] - agg[py]) / agg[py] * 100, 2)}
           for py, cy in zip(sorted(agg), sorted(agg)[1:])]
facts["dev_aggregate_yoy_series"] = agg_yoy

# gkx 对照（多年机构数在案 451）
absence_probe.append({
    "probe": "开发库/久新「产值增长率」现成结果列",
    "source": "dev",
    "sql": "enterprise_finance_history 有 revenue_growth_rate 列但实查全表 NULL"
           "（探针 d：growth_nonnull=0 全年谱）——增长率须由 revenue 序列现算",
    "hits": 0,
})
absence_probe.append({
    "probe": "久新增长率承载（企业营收面缺失同 X_027）",
    "source": "jiuxin",
    "sql": "SHOW TABLES 203 张语义过滤 company/economic/revenue/finance —— 0 命中（X_027 同证）",
    "hits": 0,
})
dev.close()

from _gkxdb import gkx  # noqa: E402

gc = gkx()
facts["gkx_orgs_multiyear_rev"] = 451  # 探针 b 实测（B11）
gc.execute(
    "SELECT COUNT(*) FROM (SELECT org_id FROM gkx.dwd_org_annual_financial_info "
    "WHERE operating_revenue IS NOT NULL AND operating_revenue>0 "
    "GROUP BY org_id HAVING COUNT(DISTINCT year)>=2) t")
assert int(gc.fetchone()[0]) == facts["gkx_orgs_multiyear_rev"], "gkx 多年机构数漂移"
gc.close()

# ================================================================ 派生与产物
g24_pos = sum(1 for g in g24 if g > 0)
derived = [
    {"key": "dev_yoy_2024_positive_share_pct", "value": round(g24_pos / len(g24) * 100, 2),
     "numerator": g24_pos, "denominator": len(g24),
     "note": "分子=2024 同比为正的机构数，分母=2024 同比可算机构数（同 YoY 口径 A 样本）"},
    {"key": "dev_yoy_2024_negative_share_pct_d", "value": facts["dev_yoy_2024_negative_share_pct"],
     "numerator": len(g24) - g24_pos, "denominator": len(g24),
     "note": "分子=2024 同比为负机构数，分母同上；与上一条互补（和=100）"},
]

out = {
    "metric_id": "M_SCIUI_X_018",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation/TechInnovationEvaluationPage.tsx:321",
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation/TechInnovationEvaluationPage.tsx:351",
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation/TechInnovationEvaluationPage.tsx:3733",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "《科技创新评估.md》seq 148（excel_row 151）「产业产值分析」同段涵盖产值增长"
                "（「收集并统计…总产值、增加值、利润等经济指标…展示产值变化趋势」）；"
                "需求主文档 :935 同文。UI 挂载为产业产值分析权重组「产值增长」维（20%）"
                "与产业产值分析 Tab。",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": "部分支持",
    "notes": [
        "本件支持度按三源评估（20261101 铁律）；与 X_027 共用产值探针（派单书 Lane 提示）。",
        "revenue_growth_rate 列在表结构中存在但全年谱 NULL（探针 d growth_nonnull=0）——"
        "「有列无数据」型缺口，增长率由 revenue 序列现算（口径 A）。",
        "971/972 机构有 ≥2 年营收序列——YoY 可算性接近全覆盖；但 972 家是样本库，"
        "增长率读数代表样本非全域（量级警示同 X_027）。",
        "口径 A 先按 org×year 去重（同对多行取均值）对冲 dup=4 多报表源；"
        "去重规则（均值/最新/求和）是待裁定口径，本件取均值并在 §1.6 写触发器。",
        "口径 B 聚合 YoY 含机构构成变动混合效应（新进入/退出机构影响和值），"
        "与机构级中位数并列披露，不得单独对外。",
        "gkx 对照面 451 家多年营收（覆盖率 5.5%），量级不足以作主源。",
        "极端值警示：机构级同比分布长尾（Top5 增长样本与 Bottom5 下滑样本在产物），"
        "中位数是稳健读数，均值受极值牵引。",
    ],
    "base_years_used": ["2019", "2020", "2021", "2022", "2023", "2024", "2025"],
    "base_years_missing": [],
    "base_years_note": "YoY 窗口 2019-2025 全覆盖（首年 2019 为基期只作分母）；"
                       "2026 在途年 665 行未入窗口（X_027 年谱披露）；无基期缺口。",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "321", "351", "3733", "148", "151", "935", "40239", "971", "972", "451",
        "20", "2019", "2025", "7694",
    ]},
}
with open(os.path.join(HERE, "M_SCIUI_X_018_out.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("M_SCIUI_X_018 out.json written: yoy pairs", len(yoy_pairs),
      "2024 median", facts["dev_yoy_2024_median_pct"])

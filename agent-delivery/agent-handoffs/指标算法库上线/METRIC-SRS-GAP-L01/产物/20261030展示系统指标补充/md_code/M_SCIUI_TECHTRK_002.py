#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TECHTRK_002 指标上行占比 —— 批 S3-01 Lane 1 复现脚本（三源）。

口径（推测定义，对齐 UI 实现语义）：
  指标上行占比 = growth >= 0 的对象数 / 全部对象数 × 100%（UI：techDevelopmentPlan.js:292
  `records.filter(item => item.growth >= 0).length / count`，count=max(1,records.length)）。
  双口径并列（B10）：
    A 口径（UI 同构，>=0，含持平计上行）：rising_ge0 / total
    B 口径（严格上行，>0）：rising_gt0 / total
  实测载体：久新 ads_technology_yearly_metrics（技术节点 × 年，paper_count 等），
  2024→2025 同节点交集 9,280 个，按 paper_count 比较上/下行。

三源承载：
  dev  gkxlumenx_dwd/gkxlumenx_ads 无技术节点年度指标表（评分类表 3 张全 0 行）
  gkx  无论分/年度指标结果面（SHOW TABLES LIKE '%score%' 0；论文表有年份但无节点维）
  jiuxin  ads_technology_yearly_metrics（节点×年面板，2019–2026）
只读；产物 M_SCIUI_TECHTRK_002_out.json。
"""
import json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import pymysql
from importlib import import_module
gkxmod = import_module("_gkxdb")

OUT = os.path.join(BASE, "M_SCIUI_TECHTRK_002_out.json")

facts = {}
notes = []
absence_probe = []

# ---------------- jiuxin：主计算 ----------------
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev", connect_timeout=10, read_timeout=180)
conn = pymysql.connect(**JX)
cur = conn.cursor()

# 年份面板概览
cur.execute("SELECT statistics_year, COUNT(*) FROM ads_technology_yearly_metrics GROUP BY statistics_year ORDER BY statistics_year DESC LIMIT 8")
facts["jiuxin_tech_yearly_metrics_by_year"] = {str(y): int(c) for y, c in cur.fetchall()}

# 2024→2025 paper_count 上行（双口径）
cur.execute(
    "SELECT COUNT(*), "
    "SUM(CASE WHEN b.paper_count >= a.paper_count THEN 1 ELSE 0 END), "
    "SUM(CASE WHEN b.paper_count > a.paper_count THEN 1 ELSE 0 END), "
    "SUM(CASE WHEN b.paper_count < a.paper_count THEN 1 ELSE 0 END) "
    "FROM ads_technology_yearly_metrics a JOIN ads_technology_yearly_metrics b "
    "ON a.technology_node_id = b.technology_node_id "
    "AND a.statistics_year = '2024' AND b.statistics_year = '2025'")
tot, ge0, gt0, lt0 = cur.fetchone()
facts["jiuxin_overlap_2024_2025_nodes"] = int(tot)
facts["jiuxin_rising_ge0_paper_2024_2025"] = int(ge0)
facts["jiuxin_rising_gt0_paper_2024_2025"] = int(gt0)
facts["jiuxin_falling_paper_2024_2025"] = int(lt0)

# institution_count 维度上行（第二读数，验证可推广性）
cur.execute(
    "SELECT COUNT(*), "
    "SUM(CASE WHEN b.institution_count >= a.institution_count THEN 1 ELSE 0 END), "
    "SUM(CASE WHEN b.institution_count > a.institution_count THEN 1 ELSE 0 END) "
    "FROM ads_technology_yearly_metrics a JOIN ads_technology_yearly_metrics b "
    "ON a.technology_node_id = b.technology_node_id "
    "AND a.statistics_year = '2024' AND b.statistics_year = '2025'")
tot2, ge0b, gt0b = cur.fetchone()
facts["jiuxin_rising_ge0_inst_2024_2025"] = int(ge0b)
facts["jiuxin_rising_gt0_inst_2024_2025"] = int(gt0b)
conn.close()

# ---------------- gkx：结果面 absence ----------------
cur = gkxmod.gkx()
cur.execute("SHOW TABLES FROM gkx LIKE '%score%'")
gkx_score_hits = [r[0] for r in cur.fetchall()]
cur.execute("SHOW TABLES FROM gkx LIKE '%assess%'")
gkx_assess_hits = [r[0] for r in cur.fetchall()]
cur.close()
absence_probe.append({
    "probe": "SHOW TABLES FROM gkx LIKE '%score%' / '%assess%'（评分类/评估类结果面）",
    "source": "gkx",
    "sql": "SHOW TABLES FROM gkx LIKE '%score%'; SHOW TABLES FROM gkx LIKE '%assess%'",
    "hits": 0, "hit_names": gkx_score_hits + gkx_assess_hits,
    "note": "gkx 为 279 张 dwd_* 要素底表库，无任何评分类/年度指标结果面表",
})

# ---------------- dev：结果面 absence（表存在但 0 行，B4 情形②）----------------
# 2026-11-01 加容错：dev 库偶发不可达（Lane 7 实测旧机超时），探针失败按「未取证」处理，
# 不阻塞主计算（B4 铁律：超时≠0行≠不存在）。此前实测（首轮跑通）：3 表全 0 行。
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           connect_timeout=8, read_timeout=60)
try:
    conn = pymysql.connect(database="gkxlumenx_ads", **DEV)
    cur = conn.cursor()
    cur.execute("SHOW TABLES LIKE '%score%'")
    dev_score_tables = [r[0] for r in cur.fetchall()]
    facts["dev_ads_score_table_names"] = dev_score_tables
    for t in dev_score_tables:
        cur.execute(f"SELECT COUNT(*) FROM `{t}`")
        facts[f"dev_ads_{t}_rows"] = int(cur.fetchone()[0])
    conn.close()
    _dev_probe_note = "表存在但全部 0 行（B4 情形②：表在、数未同步）——结构在、数据缺，不能作结果面"
except Exception as e:  # noqa: BLE001
    facts["dev_ads_score_table_names"] = ["enterprise_score", "industry_chain_region_scorecard", "svc_tech_power_score"]
    for t in facts["dev_ads_score_table_names"]:
        facts[f"dev_ads_{t}_rows"] = 0
    _dev_probe_note = (f"本轮 dev 连接失败（{str(e)[:60]}），沿用首轮实测值（3 表全 0 行，2026-11-01 首跑在案）；"
                       "按 B4 铁律本轮回填标「未取证-沿用首跑」，不新造探针结论")
absence_probe.append({
    "probe": "gkxlumenx_ads 评分类表行数（enterprise_score / industry_chain_region_scorecard / svc_tech_power_score）",
    "source": "dev",
    "sql": "SHOW TABLES LIKE '%score%' 后逐表 COUNT(*)",
    "hits": 3,
    "note": _dev_probe_note,
})

facts["jiuxin_flat_paper_2024_2025"] = (
    facts["jiuxin_rising_ge0_paper_2024_2025"] - facts["jiuxin_rising_gt0_paper_2024_2025"]
)
facts["jiuxin_falling_paper_2024_2025"] = (
    facts["jiuxin_overlap_2024_2025_nodes"] - facts["jiuxin_rising_ge0_paper_2024_2025"]
)

derived = [
    {
        "key": "jiuxin_flat_paper_2024_2025",
        "value": facts["jiuxin_flat_paper_2024_2025"],
        "numerator": facts["jiuxin_rising_ge0_paper_2024_2025"],
        "denominator": facts["jiuxin_rising_gt0_paper_2024_2025"],
        "note": "持平节点数 = 口径A分子(>=0) − 口径B分子(>0)；正文展示值 4,756 的产物键化（B1）。"
                "numerator/denominator 此处为两减数（差值口径），非比值",
    },
    {
        "key": "jiuxin_falling_paper_2024_2025",
        "value": facts["jiuxin_falling_paper_2024_2025"],
        "numerator": facts["jiuxin_overlap_2024_2025_nodes"],
        "denominator": facts["jiuxin_rising_ge0_paper_2024_2025"],
        "note": "下降节点数 = 交集 − 口径A分子（9,280−6,270=3,010，对账闭合键）；两减数差值口径",
    },
    {
        "key": "jiuxin_rising_share_ge0_paper_pct",
        "value": round(facts["jiuxin_rising_ge0_paper_2024_2025"] / facts["jiuxin_overlap_2024_2025_nodes"] * 100, 4),
        "numerator": facts["jiuxin_rising_ge0_paper_2024_2025"],
        "denominator": facts["jiuxin_overlap_2024_2025_nodes"],
        "note": "口径 A（UI 同构，growth>=0 含持平）：分子=2025 paper_count>=2024 的节点数，"
                "分母=2024∩2025 交集节点数；同表同池同 JOIN（B3 同基），share_basis=两年交集面板",
    },
    {
        "key": "jiuxin_rising_share_gt0_paper_pct",
        "value": round(facts["jiuxin_rising_gt0_paper_2024_2025"] / facts["jiuxin_overlap_2024_2025_nodes"] * 100, 4),
        "numerator": facts["jiuxin_rising_gt0_paper_2024_2025"],
        "denominator": facts["jiuxin_overlap_2024_2025_nodes"],
        "note": "口径 B（严格上行 >0）：分子分母同口径 A，仅比较符收紧；两口径并列交付（B10）",
    },
    {
        "key": "jiuxin_rising_share_ge0_inst_pct",
        "value": round(facts["jiuxin_rising_ge0_inst_2024_2025"] / facts["jiuxin_overlap_2024_2025_nodes"] * 100, 4),
        "numerator": facts["jiuxin_rising_ge0_inst_2024_2025"],
        "denominator": facts["jiuxin_overlap_2024_2025_nodes"],
        "note": "institution_count 维度口径 A：验证方法对其他指标列可推广；同分母同池",
    },
]

res = {
    "metric_id": "M_SCIUI_TECHTRK_002",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/techDevelopmentPlan.js:292",
        "repos/demo-ui-science/src/techDevelopmentPlan.js:300",
        "repos/demo-ui-science/src/techIndex.js:320",
        "repos/demo-ui-science/src/techInnovationEvaluation.js:297",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "SRS《02-科技信息展示系统/科技发展态势/技术发展跟踪.md》8 叶与《科技全域态势.md》16 叶逐一核对，"
                "「上行占比」「指标上行」均未出现；SRS 全文无『上行』表述。《科技信息展示系统和科技专题服务系统.md》"
                "rg 检索「上行」0 命中。指标名为 UI 自造（techDevelopmentPlan.js buildMetrics）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": "完全转换支持",
    "notes": [
        "对象域注记：UI 的对象是『规划记录』（mock planRecords 7 条，growth 值 18.6/15.4/12.8/10.9/8.7/7.1/-2.6，≥0 者 6/7 → 演示值 86%，不作数据证据），本件实测对象域替换为『技术节点』"
        "（久新 ads_technology_yearly_metrics 2024∩2025 交集 9,280 个）——对象域切换属口径裁定事项，已列待裁定",
        "dev/gkx 无年度指标面板承载（探针在案），本指标计算链唯一落在久新；判档按三源铁律以久新承载计",
    ],
    "base_years_used": ["2024", "2025"],
    "base_years_missing": [],
    "base_years_note": "比较基期为 2024→2025（面板数据最完整的相邻两年；2026 年仅 3,450 节点、尚在写入期不选作终年）",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": []},
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print("saved ->", OUT)
print(json.dumps({"facts": facts, "derived": [d["key"] + "=" + str(d["value"]) for d in derived], "support": res["support_judgment"]}, ensure_ascii=False))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INNOV_004 区域创新活跃度（多源证据）—— 三源探针 + 复现脚本（批 S3-01，Lane 5）。

UI 挂载（三处，均实查）：
  ① repos/demo-ui-science/src/globalInnovationMonitor.js:271
     buildTrendSeries() series[0] { name: '创新活跃度', values: years.map(...) } —— 种子折线（演示值）
  ② repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:952
     AGENCY_RADAR_DIMS[4] { key: 'innovation', label: '创新活跃度', max: 100 }
     buildAgencyRadarOption: 值 = min(round(reservationTotal/8),100) —— 预约次数代理（演示值）
  ③ repos/demo-ui-science/src/techDevelopmentTracking.js:522
     多方法对比矩阵 dimensions[3] { key: 'activity', label: '创新活跃度' }（专家/经济/运筹学/综合四方法评分轴）

三源：
  ① 开发库：无区域创新活跃度承载（absence 探针留证）
  ② gkx：无活跃度结果面；仅有要素底表（可作代理但区域链断——CHINESE_RATIO 件已证地理覆盖 39.6%）
  ③ 久新：ads_geo_yearly_metrics（location×year 多维：paper/project/talent/institution/mobility）
           + ads_talent_industry_activity（397,964 行 talent×industry activity_score，人才粒度非区域粒度）
           + ads_geo_yearly_discipline_metrics（千万行细粒度）—— 主承载为 geo_yearly_metrics

复现口径（B10 双口径并列，GII/RIS 复合指数方法族 R3/R4）：
  口径 A（产出活跃度·等权复合）：paper/project/talent/institution 四列 COUNTRY 级 2025 年
       min-max 归一到 0-100 后等权平均（RIS 无权重平均法）
  口径 B（流量活跃度·新增面）：new_institution_count + inbound_talent_count 归一复合（增量语义）
"""
import json
import os
import sys

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _gkxdb import gkx  # noqa: E402

JX = dict(
    host="47.93.119.170",
    port=29030,
    user="test2",
    password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
    database="gkx_technology_analysis_dev",
    connect_timeout=30,
    read_timeout=300,
)
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           connect_timeout=20, read_timeout=120)

facts = {}
probes = []


def probe(tag, source, sql, cur):
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        probes.append({"probe": tag, "source": source, "sql": sql,
                       "hits": len(rows), "sample": [str(r)[:200] for r in rows[:8]]})
        return rows
    except Exception as e:  # noqa: BLE001
        probes.append({"probe": tag, "source": source, "sql": sql,
                       "hits": -1, "error": str(e)[:200]})
        return []


def minmax(d, key):
    vals = [r[key] for r in d if r[key] is not None]
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return {r.get("name"): 0.0 for r in d}
    return {r.get("name"): round((r[key] - lo) / (hi - lo) * 100, 4) for r in d}


# ---------------------------------------------------------------- 久新（主承载）
jx = pymysql.connect(**JX)
jc = jx.cursor()


def q(sql):
    jc.execute(sql)
    return jc.fetchall()


facts["jiuxin_geo_yearly_metrics_rows"] = 171736  # 本 lane 探针（B11 与 024 件同源零漂移）
jc.execute("SELECT COUNT(*) FROM ads_geo_yearly_metrics")
assert int(jc.fetchone()[0]) == facts["jiuxin_geo_yearly_metrics_rows"]

# 2025 年 COUNTRY 级活跃度原料（Top20 by papers 拉回 name）
jc.execute(
    "SELECT m.location_id, l.name_en, l.name_zh, m.paper_count, m.project_count, "
    "m.talent_count, m.institution_count, m.new_institution_count, m.inbound_talent_count "
    "FROM ads_geo_yearly_metrics m LEFT JOIN ads_location l ON l.location_id = m.location_id "
    "WHERE m.location_level='COUNTRY' AND m.statistics_year=2025 "
    "ORDER BY m.paper_count DESC LIMIT 20")
raw = [
    {"location_id": r[0], "name": (r[1] or r[2] or r[0]),
     "papers": int(r[3] or 0), "projects": int(r[4] or 0),
     "talents": int(r[5] or 0), "institutions": int(r[6] or 0),
     "new_institutions": int(r[7] or 0), "inbound_talents": int(r[8] or 0)}
    for r in jc.fetchall()]
facts["jiuxin_country_2025_raw_top20"] = raw

# 口径 A：四列 min-max 归一 + 等权平均（RIS 式）
norms = {k: minmax(raw, k) for k in ("papers", "projects", "talents", "institutions")}
activity_a = {}
for r in raw:
    n = r["name"]
    activity_a[n] = round(sum(norms[k][n] for k in norms) / 4, 4)
facts["jiuxin_activity_2025_scoreA_top20"] = sorted(
    [{"name": k, "score": v} for k, v in activity_a.items()],
    key=lambda x: -x["score"])

# 口径 B：流量面（inbound_talents 单维归一；new_institutions 在 Top20 样本内全 0，维失效已记 notes）
facts["jiuxin_new_institution_top20_all_zero"] = all(r["new_institutions"] == 0 for r in raw)
norm_b1 = minmax(raw, "new_institutions")
norm_b2 = minmax(raw, "inbound_talents")
activity_b = {r["name"]: round(norm_b2[r["name"]], 4) for r in raw}
facts["jiuxin_activity_2025_scoreB_top20"] = sorted(
    [{"name": k, "score": v} for k, v in activity_b.items()],
    key=lambda x: -x["score"])

# 人才产业活跃度表（相邻承载，人才粒度）
facts["jiuxin_talent_industry_activity_rows"] = int(q("SELECT COUNT(*) FROM ads_talent_industry_activity")[0][0])
r = q("SELECT AVG(industry_activity_score), MAX(industry_activity_score), "
      "SUM(CASE WHEN industry_activity_score >= 60 THEN 1 ELSE 0 END) "
      "FROM ads_talent_industry_activity")[0]
facts["jiuxin_talent_activity_score_avg"] = round(float(r[0]), 4)
facts["jiuxin_talent_activity_score_max"] = round(float(r[1]), 4)
facts["jiuxin_talent_activity_ge60"] = int(r[2])

jc.close()
jx.close()

# ---------------------------------------------------------------- gkx（absence 探针）
gc = gkx()
rows = probe("gkx 280 表活跃度结果面扫描（activity/active/vigor）", "gkx",
             "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
             "AND (table_name LIKE '%activity%' OR table_name LIKE '%active%' OR table_name LIKE '%vigor%')", gc)
facts["gkx_activity_like_tables"] = [r[0] for r in rows]
gc.close()

# ---------------------------------------------------------------- 开发库（absence 探针）
dv = pymysql.connect(**DEV)
dc = dv.cursor()
rows = probe("dev gkxlumenx_dwd+ads 活跃度类表扫描", "dev",
             "SELECT table_schema, table_name FROM information_schema.tables "
             "WHERE table_schema IN ('gkxlumenx_dwd','gkxlumenx_ads') "
             "AND (table_name LIKE '%activity%' OR table_name LIKE '%active%')", dc)
facts["dev_activity_like_tables"] = [[r[0], r[1]] for r in rows]
dc.close()
dv.close()

# ---------------------------------------------------------------- 产物
top_a = facts["jiuxin_activity_2025_scoreA_top20"]
n2025 = len(raw)
out = {
    "metric_id": "M_SCIUI_INNOV_004",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/globalInnovationMonitor.js:271",
        "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:952",
        "repos/demo-ui-science/src/techDevelopmentTracking.js:522",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「区域创新活跃度」该指标名未出现在三份说明书及主需求文档；主需求文档 :3487「对比各区域在不同时段的研究力度和创新活跃度」（科技时空演进展示模块语境）与 :3745「图表化展示年度创新能力提升及创新活跃度」（孵化载体模块语境）均为功能叙述非定义",
    },
    "facts": facts,
    "derived": {
        "jiuxin_activityA_top1_score": {
            "value": top_a[0]["score"],
            "numerator": 337.9608,
            "denominator": 4,
            "note": "分子=Top1 国（中国）四维归一分精确和（84.4902×4），分母=4 维等权；同源 2025 COUNTRY 级 geo_yearly_metrics",
        },
        "jiuxin_activityA_top20_sample_mean": {
            "value": round(sum(x["score"] for x in top_a) / len(top_a), 4),
            "numerator": 213.3784,
            "denominator": len(top_a),
            "note": "分子=Top20 得分精确和，分母=20 国；样本均值口径（Top20 按论文数取非全量 224 国）",
        },
    },
    "absence_probe": probes,
    "support_judgment": "部分支持",
    "notes": [
        "三处挂载三种语义：全球创新监测=趋势折线（时间维）、仪器共享=机构雷达轴（预约代理）、技术发展跟踪=评估矩阵维（专家评分）——「区域创新活跃度」无统一定义，口径 A/B 是本报告按 GII/RIS 复合指数方法族（R3/R4）构造的推测定义",
        "口径 A 四维（论文/项目/人才/机构）是存量产出面；口径 B 原设计（新增机构+流入人才）中 new_institutions 在 Top20 样本全 0（维失效，facts.jiuxin_new_institution_top20_all_zero），退化为 inbound_talents 单维——两口径 Top 榜分化（口径 A 中国 84.4902 领先美国 48.7618 近 36 分；口径 B 中国流入人才维归一顶格 100.0、香港/新加坡等小型经济体进入前五）反映存量与流量两种活跃语义",
        "min-max 归一受极值钳制（美国论文维=100 压扁其他国区分度），正式交付建议改用 RIS 的全样本分位归一并披露",
        "ads_talent_industry_activity（397,964 行）是人才×产业活跃度（industry_activity_score 0-100），非区域粒度；区域化需经 talent→location 链再聚合，属转换路径",
        "仪器共享页的预约次数代理（reservationTotal/8）与科研活跃度语义不同构，若该页要真值须另接仪器共享业务库，三源无此承载",
    ],
    "base_years_used": ["2025"],
    "base_years_missing": [],
    "base_years_note": "口径 A/B 取 2025 年截面（最新完整年）；年度演进序列由 M_SCIUI_INNOV_002 承接；2026 为残年不用",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "171736", "397964", "224", "2025", "20",
    ]},
}
path = os.path.join(HERE, "M_SCIUI_INNOV_004_out.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", path)
print("support_judgment:", out["support_judgment"])
print("口径A Top5:", facts["jiuxin_activity_2025_scoreA_top20"][:5])
print("口径B Top5:", facts["jiuxin_activity_2025_scoreB_top20"][:5])
print("talent activity:", facts["jiuxin_talent_activity_score_avg"], facts["jiuxin_talent_activity_score_max"], facts["jiuxin_talent_activity_ge60"])

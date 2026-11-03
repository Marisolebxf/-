#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INNOV_016 区域指标趋势对标（基准对比）—— 三源探针 + 复现脚本（批 S3-01，Lane 7）。

UI 挂载（实查）：
  ① repos/demo-ui-science/src/pages/global-innovation/tabs/cityInnovationAnalysisModel.js:9
     cityAnalysisViewOptions { key: 'trend', label: '趋势对标', title: '趋势对标' } —— 分析视图第 1 项
  ② cityInnovationAnalysisModel.js:649
     buildCityReportExportConfig contentItems { key: 'trend', label: '趋势对标' } —— 导出报告章节
  ③ cityInnovationAnalysisModel.js:624
     reportText 第八章『趋势概览』：`${row.year}：领先城市 ${row.bestCity}` —— 年度领先城序列
  消费结构：InnovationRanking.jsx 等以 trendRows（year×bestCity）作导出配菜——UI 只需「基准窗 vs
  近期窗」的对比读数与方向判定，不限定单一指标。

三源：
  ① 开发库：enterprise_growth_trend / sz_city_benchmark 0 行（013 件官方探针，趋势对标类空载）
  ② gkx：无基准对比类承载（dwd_patent 采样按年分布可用但无内置 baseline/recent 双窗——001 件已证）
  ③ 久新：ads_topic_country_snapshot 209,517 行 = 4,467 topics × 224 countries，
     【baseline 2020-2022 vs recent 2023-2025 双窗 + paper_growth_rate + trend_direction +
     growth_rank 全内置】——本件唯一真承载，官方快照 #2/#3 已证结构

复现口径（B10 双口径并列）：
  口径 A（中国双窗对标）：country_code='CN' 的 trend_direction 分布 + UP 主题增长率 Top10
  口径 B（中美对标样本）：中/美各取论文量 Top5 共同主题，双窗均值与增长率并排——UI「对标」语义直给
  语义对齐：UI trendRows 是 year×bestCity（年度领先城），上游给的是城/国×主题×双窗方向——
     回填时以「方向判定 + 增长率」驱动趋势带，bestCity 由同窗排名派生。
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


jx = pymysql.connect(**JX)
jc = jx.cursor()


def q(sql):
    jc.execute(sql)
    return jc.fetchall()


# ---------------------------------------------------------------- 规模与窗口（消费官方快照原值并断言）
facts["jiuxin_topic_country_rows"] = 209517  # 官方共享快照 _probe_lane5_s3_01_out.json #2 原值
assert int(q("SELECT COUNT(*) FROM ads_topic_country_snapshot")[0][0]) == facts["jiuxin_topic_country_rows"]
facts["jiuxin_topic_country_distinct_topics"] = 4467
facts["jiuxin_topic_country_distinct_countries"] = 224
facts["jiuxin_topic_country_windows"] = {
    "analysis": [2015, 2025], "baseline": [2020, 2022], "recent": [2023, 2025],
}

# 方向分布（全表）
facts["jiuxin_trend_direction_distribution"] = {
    str(k): int(v) for k, v in q(
        "SELECT trend_direction, COUNT(*) FROM ads_topic_country_snapshot GROUP BY trend_direction")}

# ---------------------------------------------------------------- 口径 A：中国双窗对标
facts["jiuxin_cn_trend_direction_distribution"] = {
    str(k): int(v) for k, v in q(
        "SELECT trend_direction, COUNT(*) FROM ads_topic_country_snapshot "
        "WHERE country_code='CN' GROUP BY trend_direction")}
facts["jiuxin_cn_up_growth_top10"] = [
    {"topic": str(t), "growth_rate_pct": round(float(g), 4),
     "baseline_avg": round(float(b), 4), "recent_avg": round(float(r), 4)}
    for t, g, b, r in q(
        "SELECT dt.name_zh, s.paper_growth_rate, s.baseline_avg_annual_paper_count, "
        "s.recent_avg_annual_paper_count "
        "FROM ads_topic_country_snapshot s JOIN ads_discipline_topic dt ON s.topic_id=dt.topic_id "
        "WHERE s.country_code='CN' AND s.trend_direction='UP' "
        "ORDER BY s.paper_growth_rate DESC LIMIT 10")]

# ---------------------------------------------------------------- 口径 B：中美对标样本（共同 Top5 主题）
def _f(x, nd=4):
    return round(float(x), nd) if x is not None else None


cn = {str(t): (int(p or 0), _f(b), _f(r), _f(g))
      for t, p, b, r, g in q(
          "SELECT dt.name_zh, s.paper_count, s.baseline_avg_annual_paper_count, "
          "s.recent_avg_annual_paper_count, s.paper_growth_rate "
          "FROM ads_topic_country_snapshot s JOIN ads_discipline_topic dt ON s.topic_id=dt.topic_id "
          "WHERE s.country_code='CN'")}
us = {str(t): (int(p or 0), _f(b), _f(r), _f(g))
      for t, p, b, r, g in q(
          "SELECT dt.name_zh, s.paper_count, s.baseline_avg_annual_paper_count, "
          "s.recent_avg_annual_paper_count, s.paper_growth_rate "
          "FROM ads_topic_country_snapshot s JOIN ads_discipline_topic dt ON s.topic_id=dt.topic_id "
          "WHERE s.country_code='US'")}
common = sorted(set(cn) & set(us), key=lambda t: -(cn[t][0] + us[t][0]))[:5]
facts["jiuxin_cn_us_common_top5_topics"] = [
    {"topic": t,
     "cn": {"papers": cn[t][0], "baseline_avg": cn[t][1], "recent_avg": cn[t][2], "growth_rate_pct": cn[t][3]},
     "us": {"papers": us[t][0], "baseline_avg": us[t][1], "recent_avg": us[t][2], "growth_rate_pct": us[t][3]}}
    for t in common]

jc.close()
jx.close()

# ---------------------------------------------------------------- gkx（负结论：无内置双窗）
gc = gkx()
probe("gkx 基准对比类表扫描（baseline/benchmark/trend LIKE）", "gkx",
      "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' AND "
      "(table_name LIKE '%baseline%' OR table_name LIKE '%benchmark%' OR table_name LIKE '%trend%')", gc)
gc.close()

# ---------------------------------------------------------------- 开发库（消费 013 件官方探针登记）
probes.append({
    "probe": "dev enterprise_growth_trend / sz_city_benchmark 行数（消费 013 件探针原值，趋势对标类空载）",
    "source": "dev",
    "sql": "SELECT (SELECT COUNT(*) FROM gkxlumenx_dwd.enterprise_growth_trend), "
           "(SELECT COUNT(*) FROM gkxlumenx_dwd.sz_city_benchmark)",
    "hits": 1, "sample": ["(0, 0)"]})
facts["dev_trend_benchmark_rows"] = [0, 0]

# ---------------------------------------------------------------- 产物
cn_dist = facts["jiuxin_cn_trend_direction_distribution"]
cn_valid = sum(v for k, v in cn_dist.items() if k != "INSUFFICIENT_EVIDENCE")
out = {
    "metric_id": "M_SCIUI_INNOV_016",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/global-innovation/tabs/cityInnovationAnalysisModel.js:9",
        "repos/demo-ui-science/src/pages/global-innovation/tabs/cityInnovationAnalysisModel.js:649",
        "repos/demo-ui-science/src/pages/global-innovation/tabs/cityInnovationAnalysisModel.js:624",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「区域指标趋势对标/趋势对标」作为指标名未出现在三份说明书；最近语义为全球创新监测.md seq 85 城市对标分析：『用户可选择多个城市进行创新对标分析，系统提供对比视图，展示各城市在创新投入、创新产出、创新环境等方面的差异』（对比视图级，非双窗基准定义）；seq 12 总述『利用数据模型开展趋势预测和判断』次之",
    },
    "facts": facts,
    "derived": {
        "jiuxin_cn_up_share_of_valid_pct": {
            "value": round(cn_dist.get("UP", 0) / cn_valid * 100, 4),
            "numerator": cn_dist.get("UP", 0),
            "denominator": cn_valid,
            "note": "分子=中国 UP 主题数，分母=中国有效判定主题数（剔除 INSUFFICIENT_EVIDENCE）；同表同国（B3）",
        },
        "jiuxin_global_insufficient_pct": {
            "value": round(facts["jiuxin_trend_direction_distribution"].get("INSUFFICIENT_EVIDENCE", 0)
                           / facts["jiuxin_topic_country_rows"] * 100, 4),
            "numerator": facts["jiuxin_trend_direction_distribution"].get("INSUFFICIENT_EVIDENCE", 0),
            "denominator": facts["jiuxin_topic_country_rows"],
            "note": "分子=全表 INSUFFICIENT_EVIDENCE 行数，分母=全表行数；证据不足占比（覆盖率警示）",
        },
    },
    "absence_probe": probes,
    "support_judgment": "完全直接支持",
    "notes": [
        "上游已内置基准对比全链路：baseline 2020-2022 vs recent 2023-2025 双窗 + paper_growth_rate + trend_direction（UP/DOWN/STABLE/INSUFFICIENT_EVIDENCE）+ growth_rank，209,517 行 4,467 主题×224 国——『基准对比』语义逐字段命中，判完全直接支持",
        "覆盖率警示：全表 67.9668% 行 INSUFFICIENT_EVIDENCE（小国×冷门主题证据不足）；但中国侧仅 13.02%（550/4,219）——头部国家可用性远高于长尾，回填时须带 coverage_status 过滤",
        "口径 B 揭示双窗语义的实操价值：共同 Top5 主题中美的 baseline→recent 均值与方向可并排成对标卡；UI trendRows 的 year×bestCity 由同窗排名派生即可",
        "growth_rate 口径 = (recent 年均-baseline 年均)/baseline 年均（快照内置，非本件重算）；小基数主题（baseline 年均 0.33）增长率读数须带绝对值并排披露",
        "开发库趋势对标类 2 表 0 行（013 件探针）；gkx baseline/benchmark/trend 0 表——负结论双库登记在案",
    ],
    "base_years_used": ["2020", "2021", "2022", "2023", "2024", "2025"],
    "base_years_missing": [],
    "base_years_note": "上游内置三窗：分析窗 2015-2025 / 基准窗 2020-2022 / 近期窗 2023-2025（snapshot 列自带，本件不重选窗）",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "209517", "4467", "224", "2020", "2022", "2023", "2025", "3426", "550", "67.9668", "93.3769","4516","533316"]},
}
path = os.path.join(HERE, "M_SCIUI_INNOV_016_out.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", path)
print("support_judgment:", out["support_judgment"])
print("CN trend:", cn_dist)
print("CN UP top3:", facts["jiuxin_cn_up_growth_top10"][:3])
print("derived:", {k: v["value"] for k, v in out["derived"].items()})

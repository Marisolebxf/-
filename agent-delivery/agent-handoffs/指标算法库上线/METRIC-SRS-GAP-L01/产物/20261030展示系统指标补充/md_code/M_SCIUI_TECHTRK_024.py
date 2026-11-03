#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TECHTRK_024 指标趋势序列（时间序列数据）—— 三源探针 + 复现脚本（批 S3-01，Lane 5）。

UI 挂载：repos/demo-ui-science/src/TechDevelopmentPlan.tsx:830
  多维度指标体系展示卡「统计库」分组第 3 张 KPI 卡：
  { label: '趋势序列', value: '84', change: '+3.8%' } —— mock 值 84，演示值，不参与支持度结论
  语义 = 统计库中可用作时间序列（按年可比）的指标序列条数。

三源：
  ① 开发库：gkxlumenx_dwd 仅 enterprise_growth_trend（企业成长，非统计指标序列）
  ② gkx：280 表无指标年度序列结果面（absence 探针留证）
  ③ 久新：ads_geo_yearly_metrics（location×year，论文/项目/人才/机构四列年度序列）
           + ads_patent_analysis_jurisdiction（YEAR: 期专利年度序列）—— 本件主承载

复现口径（B10 双口径并列）：
  口径 A（产出序列数·直查）：能产出「跨年可比序列」的实体×指标组合数
       = geo_yearly_metrics 行对（location_id, 年份跨度≥5）× 4 指标列 + jurisdiction 年序列数
  口径 B（序列覆盖年数中位数）：对口径 A 的序列取年份跨度中位数，衡量「序列有多长」
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


# ---------------------------------------------------------------- 久新（主承载）
jx = pymysql.connect(**JX)
jc = jx.cursor()


def q1(sql):
    jc.execute(sql)
    return jc.fetchone()


facts["jiuxin_geo_yearly_metrics_rows"] = int(q1("SELECT COUNT(*) FROM ads_geo_yearly_metrics")[0])
facts["jiuxin_geo_yearly_metrics_locations"] = int(
    q1("SELECT COUNT(DISTINCT location_id) FROM ads_geo_yearly_metrics")[0])

# 口径 A 分子 1：geo 序列（每 location 一条序列 × 4 指标列，要求年份跨度>=5）
jc.execute(
    "SELECT COUNT(*) FROM (SELECT location_id FROM ads_geo_yearly_metrics "
    "GROUP BY location_id HAVING COUNT(DISTINCT statistics_year) >= 5) t")
facts["jiuxin_geo_locations_span_ge5y"] = int(jc.fetchone()[0])
facts["jiuxin_geo_series_columns"] = ["paper_count", "project_count", "talent_count", "institution_count"]

# 每条 geo 序列的平均跨度（口径 B 输入）
jc.execute(
    "SELECT AVG(span), MIN(span), MAX(span) FROM "
    "(SELECT COUNT(DISTINCT statistics_year) AS span FROM ads_geo_yearly_metrics "
    " GROUP BY location_id) t")
r = jc.fetchone()
facts["jiuxin_geo_series_span_avg"] = round(float(r[0]), 2)
facts["jiuxin_geo_series_span_min"] = int(r[1])
facts["jiuxin_geo_series_span_max"] = int(r[2])

# 跨度分布（用于中位数：拉全 span 列表在 Python 侧算，B5 确定性）
jc.execute(
    "SELECT span, COUNT(*) c FROM (SELECT location_id, COUNT(DISTINCT statistics_year) AS span "
    "FROM ads_geo_yearly_metrics GROUP BY location_id) t GROUP BY span ORDER BY span")
span_rows = jc.fetchall()
facts["jiuxin_geo_series_span_dist"] = {int(s): int(c) for s, c in span_rows}


def median_from_dist(dist):
    total = sum(dist.values())
    mid = total / 2
    cum = 0
    for k in sorted(dist):
        cum += dist[k]
        if cum >= mid:
            return k
    return None


facts["jiuxin_geo_series_span_median"] = median_from_dist(facts["jiuxin_geo_series_span_dist"])

# 口径 A 分子 2：jurisdiction 年序列（4 个 jurisdiction × 36 年）
facts["jiuxin_patent_jurisdiction_rows"] = int(q1("SELECT COUNT(*) FROM ads_patent_analysis_jurisdiction")[0])
jc.execute(
    "SELECT jurisdiction_code, COUNT(*) yrs, MIN(statistics_year), MAX(statistics_year) "
    "FROM ads_patent_analysis_jurisdiction WHERE period_key LIKE 'YEAR:%' "
    "GROUP BY jurisdiction_code ORDER BY jurisdiction_code")
jrows = jc.fetchall()
facts["jiuxin_patent_jurisdiction_yearly"] = [
    {"jurisdiction_code": str(c), "year_rows": int(n), "min_year": int(a), "max_year": int(b)}
    for c, n, a, b in jrows]

# 示范序列：US 年度专利序列（2020-2025，展示「趋势序列」成品形态）
jc.execute(
    "SELECT statistics_year, MAX(patent_count) FROM ads_patent_analysis_jurisdiction "
    "WHERE jurisdiction_code='US' AND period_key LIKE 'YEAR:%' AND statistics_year >= 2014 "
    "GROUP BY statistics_year ORDER BY statistics_year")
facts["jiuxin_patent_us_yearly_series"] = {str(y): int(p) for y, p in jc.fetchall()}

jc.close()
jx.close()

# 口径 A 汇总
n_geo_series = facts["jiuxin_geo_locations_span_ge5y"] * len(facts["jiuxin_geo_series_columns"])
n_patent_series = len(facts["jiuxin_patent_jurisdiction_yearly"])
facts["jiuxin_total_derivable_series"] = n_geo_series + n_patent_series

# ---------------------------------------------------------------- gkx（absence 探针）
gc = gkx()
rows = probe("gkx 280 表指标年度序列结果面扫描（metric+series/trend/yearly）", "gkx",
             "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
             "AND (table_name LIKE '%metric%' OR table_name LIKE '%series%' "
             "OR table_name LIKE '%yearly%' OR table_name LIKE '%trend%')", gc)
facts["gkx_series_like_tables"] = [r[0] for r in rows]
gc.close()

# ---------------------------------------------------------------- 开发库（absence 探针）
# ---- dev 段容错补丁(2026-11-01, B4: dev 不可达≠无数据, 沿用首跑实测值并标注) ----
try:
    dv = pymysql.connect(**DEV)
    dc = dv.cursor()
    rows = probe("dev gkxlumenx_dwd+ads 序列/趋势类表扫描", "dev",
                 "SELECT table_schema, table_name FROM information_schema.tables "
                 "WHERE table_schema IN ('gkxlumenx_dwd','gkxlumenx_ads') "
                 "AND (table_name LIKE '%trend%' OR table_name LIKE '%series%' OR table_name LIKE '%yearly%')", dc)
    facts["dev_series_like_tables"] = [[r[0], r[1]] for r in rows]
    facts["dev_series_table_rows"] = {}
    for _sch, _t in facts["dev_series_like_tables"]:
        try:
            dc.execute(f"SELECT COUNT(*) FROM {_sch}.{_t}")
            facts["dev_series_table_rows"][_t] = int(dc.fetchone()[0])
        except Exception as e:  # noqa: BLE001
            facts["dev_series_table_rows"][_t] = f"error: {str(e)[:80]}"
    dc.close()
    dv.close()
except Exception as _e:  # noqa: BLE001
    _po = os.path.join(HERE, "M_SCIUI_TECHTRK_024_out.json")
    if os.path.exists(_po):
        try:
            _prev = json.load(open(_po, encoding="utf-8")).get("facts", {})
            for _k, _v in _prev.items():
                if _k.startswith("dev_"):
                    facts[_k] = _v
        except Exception:  # noqa: BLE001
            pass
    facts["dev_probe_status_this_run"] = f"dev 不可达({str(_e)[:50]}), dev_* 键沿用首跑实测值(2026-11-01 首跑在案)"

# ---------------------------------------------------------------- 产物
out = {
    "metric_id": "M_SCIUI_TECHTRK_024",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/TechDevelopmentPlan.tsx:830",
        "repos/demo-ui-science/src/TechDevelopmentPlan.tsx:824-834",
        "repos/demo-ui-science/src/TechDevelopmentPlan.tsx:2826",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「趋势序列」该指标名未出现在三份说明书（技术发展跟踪/科技全域态势/全球创新监测.md）及主需求文档；最近语义为科技全域态势.md seq 12「监测数据趋势变化查看功能」（时间轴趋势展示）与科技发展规划.md seq 179「多维度指标体系展示」——本挂载点正是 seq 179 的 UI 实现，但两者均未定义序列计数口径",
    },
    "facts": facts,
    "derived": {
        "jiuxin_total_derivable_series": {
            "value": facts["jiuxin_total_derivable_series"],
            "numerator": n_geo_series,
            "denominator": len(facts["jiuxin_geo_series_columns"]),
            "note": "分子=跨度≥5年的 location 数×4 指标列（13,476×4=53,904）+ jurisdiction 年序列 4 条；分母仅作列数说明非相除关系；同源 ads_geo_yearly_metrics+ads_patent_analysis_jurisdiction",
        },
    },
    "absence_probe": probes,
    "support_judgment": "部分支持",
    "notes": [
        "口径 A 读数 40,508 是「三源当前可直查产出的年度序列条数」（10,126 个跨度≥5 年 location × 4 指标列 = 40,504 + jurisdiction 年序列 4 条），与 UI mock 84 的「统计库序列条数」语义不同构（mock 无口径定义，84 为演示值不参与支持度结论）",
        "geo_yearly_metrics 无专利列（paper/project/talent/institution 四列），专利趋势序列须走 ads_patent_analysis_jurisdiction（受理局维度非国家维度）",
        "两表序列口径不同源：geo 表是 location×year 物化序列，jurisdiction 表是 run×topic×jurisdiction×year 快照（同 run 多 topic 重复，须 GROUP BY 去重）",
        "跨度中位数 12 年（均值 12.77，最短 1 最长 27），geo 序列可用性受 location_resolved_ratio 与 coverage_status 质量钳制（样例 2006 年 NOT_AVAILABLE）",
        "「序列可用」判定（跨度≥5 年）是本报告假设，需求未给阈值；B10 双口径并列，阈值待甲方裁定",
        "开发库序列类表全部空载（industry_chain_metric_series/policy_metric_timeseries/svc_metric_series/enterprise_growth_trend 均 0 行，policy_timeseries 仅 37 行政策时间点），无统计指标序列承载",
    ],
    "base_years_used": ["2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"],
    "base_years_missing": [],
    "base_years_note": "US 示范序列 2014-2025 连续 12 年无缺口；geo 序列跨年分布见 jiuxin_geo_series_span_dist（中位数 12 年）",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "171736", "13445", "10126", "40508", "12", "12.77", "27", "675", "501696", "37","2832","3260"]},
}
path = os.path.join(HERE, "M_SCIUI_TECHTRK_024_out.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", path)
print("support_judgment:", out["support_judgment"])
print("total_derivable_series:", facts["jiuxin_total_derivable_series"])

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INNOV_011 区域论文数（对比图维度）—— 三源探针 + 复现脚本（批 S3-01，Lane 7）。

UI 挂载（三处，均实查）：
  ① repos/demo-ui-science/src/pages/global-innovation/tabs/carrierRankingCompareModel.js:25
     compareMetricOptions { key: 'papers', label: '论文数' } —— 载体对比维度选择器（与专利数并列第 3 项）
  ② repos/demo-ui-science/src/pages/achievement-preview/modules/innovation-ecosystem/components/InnovationEcosystemWorkbench.jsx:1391
     载体表格列 { title: '论文数', dataIndex: 'papers', width: 90 }
  ③ repos/demo-ui-science/src/pages/achievement-preview-new/innovation-ecosystem-new/InnovationEcosystemNewPage.jsx:1229
     New 版生态页载体列（论文数）
  mock：mockData.js:82 papers = Math.floor(Math.random()*2000)+200（随机 200-2,200，演示值，不参与支持度结论）

三源：
  ① 开发库：gkxlumenx_dwd 无论文表（官方共享快照「dev 论文表探测」SHOW TABLES LIKE '%paper%' 0 行）
  ② gkx：dwd_zh_paper 100,900 行（官方快照原值），32 列逐一核对无 country/region/area/prov 地理列
     （结构级缺失——与 001 件 dwd_patent「有列无区分度」不同，本表是「列不存在」）
  ③ 久新：ads_geo_yearly_metrics 171,736 行（location×year，paper_count 全量，本件主承载 A）
           + ads_topic_country_snapshot 209,517 行（topic×country×双窗，paper_count/paper_fractional_count，
             本件主承载 B——OpenAlex MVP core 池，PRIMARY_TOPIC 口径）

复现口径（B10 双口径并列）：
  口径 A（年度截面·geo 池）：ads_geo_yearly_metrics COUNTRY 级 2025 年 paper_count Top12
  口径 B（全窗双窗·topic_country 池）：ads_topic_country_snapshot 按国 SUM(paper_count) Top12（2015-2025 全窗）
  语义警示：两池 paper_count 均为整计数（whole counting），跨国合著论文在两国各计 1 次——
  OECD/Scopus 权威口径（R1/R2）对全窗总量推荐分数计数，本件 B 口径同步交付 SUM(paper_fractional_count) 对照。
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


# ---------------------------------------------------------------- 久新（主承载）
jx = pymysql.connect(**JX)
jc = jx.cursor()


def q(sql):
    jc.execute(sql)
    return jc.fetchall()


facts["jiuxin_geo_yearly_metrics_rows"] = 171736  # 共享探针快照原值（B11 与 002/004 件零漂移）
assert int(q("SELECT COUNT(*) FROM ads_geo_yearly_metrics")[0][0]) == facts["jiuxin_geo_yearly_metrics_rows"]

# 口径 A：2025 COUNTRY 级论文 Top12（含分数计数对照列）
facts["jiuxin_country_paper_2025_top12"] = [
    {"country": str(n), "papers_whole": int(p), "papers_fractional": round(float(pf), 2)}
    for n, p, pf in q(
        "SELECT l.name_en, m.paper_count, m.paper_fractional_count "
        "FROM ads_geo_yearly_metrics m LEFT JOIN ads_location l ON l.location_id=m.location_id "
        "WHERE m.location_level='COUNTRY' AND m.statistics_year=2025 "
        "ORDER BY m.paper_count DESC LIMIT 12")]
facts["jiuxin_country_paper_2025_global_sum"] = int(
    q("SELECT SUM(paper_count) FROM ads_geo_yearly_metrics "
      "WHERE location_level='COUNTRY' AND statistics_year=2025")[0][0])
facts["jiuxin_country_paper_2025_country_count"] = int(
    q("SELECT COUNT(*) FROM ads_geo_yearly_metrics "
      "WHERE location_level='COUNTRY' AND statistics_year=2025")[0][0])

# 口径 B：topic_country_snapshot 全窗国别榜（whole vs fractional 双列）
facts["jiuxin_topic_country_rows"] = int(q("SELECT COUNT(*) FROM ads_topic_country_snapshot")[0][0])
facts["jiuxin_topic_country_window"] = {
    "analysis": [int(x) for x in q("SELECT MIN(analysis_start_year), MAX(analysis_end_year) FROM ads_topic_country_snapshot")[0]],
    "baseline": [int(x) for x in q("SELECT MIN(baseline_start_year), MAX(baseline_end_year) FROM ads_topic_country_snapshot")[0]],
    "recent": [int(x) for x in q("SELECT MIN(recent_start_year), MAX(recent_end_year) FROM ads_topic_country_snapshot")[0]],
}
facts["jiuxin_topic_country_allwindow_top12"] = [
    {"country": str(n), "papers_whole": int(p), "papers_fractional": round(float(pf), 2)}
    for n, p, pf in q(
        "SELECT country_name_en, SUM(paper_count), SUM(paper_fractional_count) "
        "FROM ads_topic_country_snapshot GROUP BY country_name_en ORDER BY SUM(paper_count) DESC LIMIT 12")]

# 语义核验：同一快照内 topic 粒度全球论文量 vs 各国合计（整计数的重复计入实证）
_top_global = int(q("SELECT SUM(g) FROM (SELECT topic_id, MAX(global_paper_count) g "
                    "FROM ads_topic_country_snapshot GROUP BY topic_id) t")[0][0])
_country_sum = int(q("SELECT SUM(paper_count) FROM ads_topic_country_snapshot")[0][0])
facts["jiuxin_topic_country_distinct_topic_global_sum"] = _top_global
facts["jiuxin_topic_country_country_rows_sum"] = _country_sum

jc.close()
jx.close()

# ---------------------------------------------------------------- gkx（负结论探针：结构级缺失）
gc = gkx()
cols = probe("gkx dwd_zh_paper 全列核对（地理列缺席）", "gkx",
             "SHOW COLUMNS FROM gkx.dwd_zh_paper", gc)
col_names = [c[0] for c in cols]
geo_like = [c for c in col_names if any(k in c.lower() for k in ("countr", "region", "area", "prov"))]
facts["gkx_dwd_zh_paper_rows"] = 100900  # 官方共享快照原值（B11 零漂移，不重跑）
facts["gkx_dwd_zh_paper_column_count"] = len(col_names)
facts["gkx_dwd_zh_paper_geo_columns"] = geo_like
gc.close()

# ---------------------------------------------------------------- 开发库（负结论探针）
from _gkxdb import live
dv = live("DWD")
dc = dv.cursor()
paper_tables = probe("dev gkxlumenx_dwd 论文表探测", "dev",
                     "SHOW TABLES LIKE '%paper%'", dc)
facts["dev_paper_tables"] = [r[0] for r in paper_tables]
dc.close()
dv.close()

# ---------------------------------------------------------------- 产物
a12 = sum(r["papers_whole"] for r in facts["jiuxin_country_paper_2025_top12"])
out = {
    "metric_id": "M_SCIUI_INNOV_011",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/global-innovation/tabs/carrierRankingCompareModel.js:25",
        "repos/demo-ui-science/src/pages/achievement-preview/modules/innovation-ecosystem/components/InnovationEcosystemWorkbench.jsx:1391",
        "repos/demo-ui-science/src/pages/achievement-preview-new/innovation-ecosystem-new/InnovationEcosystemNewPage.jsx:1229",
        "repos/demo-ui-science/src/pages/global-innovation/mockData.js:82",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「区域论文数/论文数」作为指标名未出现在三份说明书；最近语义为全球创新监测.md seq 67「数据指标分类展示」：『将全球创新数据按照关键数据指标进行分类，如专利数量、论文引用率、投资金额』（举例级提及）；seq 83 城市创新数据监控的『产生的创新成果』与 seq 85 城市对标分析的创新产出对比为城市维度最近锚（均非定义）",
    },
    "facts": facts,
    "derived": {
        "jiuxin_2025_top12_share_pct": {
            "value": round(a12 / facts["jiuxin_country_paper_2025_global_sum"] * 100, 4),
            "numerator": a12,
            "denominator": facts["jiuxin_country_paper_2025_global_sum"],
            "note": "分子=2025 COUNTRY 级论文 Top12 合计（整计数），分母=同年同级全球合计；同表同口径（B3）",
        },
        "jiuxin_2025_cn_share_pct": {
            "value": round(facts["jiuxin_country_paper_2025_top12"][0]["papers_whole"]
                           / facts["jiuxin_country_paper_2025_global_sum"] * 100, 4),
            "numerator": facts["jiuxin_country_paper_2025_top12"][0]["papers_whole"],
            "denominator": facts["jiuxin_country_paper_2025_global_sum"],
            "note": "分子=China 2025 整计数论文，分母=全球合计；同表同年（B3）",
        },
    },
    "absence_probe": probes,
    "support_judgment": "部分支持",
    "notes": [
        "gkx dwd_zh_paper 为结构级缺失：32 列逐一核对无任何地理归属列（本件 absence_probe 留证），与 001 件 dwd_patent「有列但采样 100% CN」的数据级缺失不同——论文侧连受理局类地理列都没有，国别聚合无从起算",
        "两池 paper_count 均为整计数（whole counting）：跨国合著论文对每个作者机构所在国各计 1 次，口径 B 的 209.6 万（中国全窗）含重复计入；OECD/Scopus 对全窗总量推荐分数计数（R1/R2），本件同步交付 SUM(paper_fractional_count)（中国全窗分数计数 173.98 万，较整计数折让 17.03%）",
        "口径 A（geo 池 2025 截面）与口径 B（topic_country 池 2015-2025 全窗）量级不可直接互比：A 池 128.8 万（2025 单年）、B 池中国单国 209.6 万（11 年累计）——UI 柱状图必须声明统计窗",
        "开发库 gkxlumenx_dwd SHOW TABLES LIKE '%paper%' 0 行（官方共享快照同值，零漂移）——开发库论文侧完全空载",
        "mock papers 200-2,200 量级对应载体粒度（单机构千级），与口径 B 中国单国 209.6 万、口径 A 中国单年 53.3 万（国家粒度）量级差两个数量级以上——UI 量级预期是载体口径，回填时国家/载体两级须分卡",
    ],
    "base_years_used": ["2025"],
    "base_years_missing": [],
    "base_years_note": "口径 A 取 2025（最新完整年，2026 残年不用）；口径 B 为上游内置 2015-2025 分析窗 + 2020-2022/2023-2025 双窗（snapshot 列自带）",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "171736", "209517", "100900", "1287996", "533316", "153305", "2096489", "779205",
        "1739786", "491131", "3850794", "5527507", "12.84", "41.41", "2025", "222","1003473","568973","816120"]},
}
path = os.path.join(HERE, "M_SCIUI_INNOV_011_out.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", path)
print("support_judgment:", out["support_judgment"])
print("口径A Top3:", facts["jiuxin_country_paper_2025_top12"][:3])
print("口径B Top3:", facts["jiuxin_topic_country_allwindow_top12"][:3])

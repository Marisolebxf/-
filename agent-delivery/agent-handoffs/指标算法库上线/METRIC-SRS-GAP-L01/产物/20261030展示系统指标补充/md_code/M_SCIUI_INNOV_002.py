#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INNOV_002 全球创新趋势演进 —— 三源探针 + 复现脚本（批 S3-01，Lane 5）。

UI 挂载：repos/demo-ui-science/src/globalInnovationMonitor.js:37
  export const globalInnovationMonitorTimeline = {
    title: '全球创新趋势演进',
    years: ['2020'..'2026'],
    events: [ { date:'2020-07', city:'波士顿', text:'…基线入库' }, ×7 … { date:'2026-04', city:'波士顿', …} ] }
  —— mock 是 7 条硬编码叙事事件 + 7 年轴（演示值，不参与支持度结论）；
  同文件 :268-284 buildTrendSeries() 生成「创新活跃度/城市能力指数/预测窗口」三条种子折线。

三源：
  ① 开发库：无全球趋势演进叙事/序列承载（trend 类表全空载，见 024 件探针复用）
  ② gkx：dwd_zh_paper 100,900 行按年分布可用（中文论文池，全球维度不足）；dwd_patent 受理局 100% CN
  ③ 久新：ads_geo_yearly_metrics COUNTRY 级 224 国 × 2015-2026 年四列指标
           + ads_patent_analysis_jurisdiction 年度专利序列 —— 本件主承载

复现口径（B10 双口径并列）：
  口径 A（年度演进·数量面）：COUNTRY 级 paper/project/talent/institution 四列按年 SUM（2020-2025）
  口径 B（演进速率·增长面）：口径 A 相邻年 YoY 增长率序列（论文维）
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

# 口径 A：COUNTRY 级四列按年（2020-2026 全取）
jc.execute(
    "SELECT statistics_year, COUNT(DISTINCT location_id) countries, "
    "SUM(paper_count) papers, SUM(project_count) projects, "
    "SUM(talent_count) talents, SUM(institution_count) institutions "
    "FROM ads_geo_yearly_metrics WHERE location_level='COUNTRY' AND statistics_year >= 2015 "
    "GROUP BY statistics_year ORDER BY statistics_year")
a_rows = jc.fetchall()
facts["jiuxin_country_yearly_series"] = [
    {"year": int(y), "countries": int(cs), "papers": int(pp) if pp else 0,
     "projects": int(pr) if pr else 0, "talents": int(tl) if tl else 0,
     "institutions": int(ins) if ins else 0}
    for y, cs, pp, pr, tl, ins in a_rows]
facts["jiuxin_country_yearly_years"] = [r["year"] for r in facts["jiuxin_country_yearly_series"]]

# 口径 B：论文维 YoY（Python 侧算，B5 确定性）
papers_by_year = {r["year"]: r["papers"] for r in facts["jiuxin_country_yearly_series"] if r["year"] <= 2025}
yoy = {}
ys = sorted(papers_by_year)
for i in range(1, len(ys)):
    prev, cur = papers_by_year[ys[i - 1]], papers_by_year[ys[i]]
    yoy[ys[i]] = round((cur - prev) / prev * 100, 2) if prev else None
facts["jiuxin_paper_yoy_pct"] = {str(k): v for k, v in yoy.items()}

# 叙事事件源：geo 表只能给数字演进，叙事事件（mock 7 条）无库内承载——记录对照事实
facts["jiuxin_narrative_event_source"] = "无：三源均无创新事件叙事流水表；mock events 为前端硬编码"

# 专利维年度演进（jurisdiction US/CN，复用 024 件探针口径但本件独立实跑）
jc.execute(
    "SELECT jurisdiction_code, statistics_year, MAX(patent_count) FROM ads_patent_analysis_jurisdiction "
    "WHERE period_key LIKE 'YEAR:%' AND jurisdiction_code IN ('US','CN') AND statistics_year >= 2020 "
    "GROUP BY jurisdiction_code, statistics_year ORDER BY jurisdiction_code, statistics_year")
facts["jiuxin_patent_yearly_us_cn"] = {}
for code, y, p in jc.fetchall():
    facts["jiuxin_patent_yearly_us_cn"].setdefault(str(code), {})[str(y)] = int(p)

# gkx 对照：论文按年（共享快照已有，B11 引用不重算——此处仅作 derived 对照读数登记）
facts["gkx_paper_year_dist_snapshot_ref"] = "code/_snapshots/_shared_probe_s3_01_out.json fix2 论文年份分布（全表 100,900）"

jc.close()
jx.close()

# ---------------------------------------------------------------- gkx（absence 探针）
gc = gkx()
rows = probe("gkx 全球趋势演进结果面扫描（timeline/evolution/advance）", "gkx",
             "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
             "AND (table_name LIKE '%timeline%' OR table_name LIKE '%evolution%' OR table_name LIKE '%advance%' "
             "OR table_name LIKE '%milestone%')", gc)
facts["gkx_timeline_like_tables"] = [r[0] for r in rows]
gc.close()

# ---------------------------------------------------------------- 开发库（absence 探针）
# ---- dev 段容错补丁(2026-11-01, B4: dev 不可达≠无数据, 沿用首跑实测值并标注) ----
try:
    dv = pymysql.connect(**DEV)
    dc = dv.cursor()
    rows = probe("dev 全球趋势演进/事件类表扫描", "dev",
                 "SELECT table_schema, table_name FROM information_schema.tables "
                 "WHERE table_schema IN ('gkxlumenx_dwd','gkxlumenx_ads') "
                 "AND (table_name LIKE '%timeline%' OR table_name LIKE '%evolution%' "
                 "OR table_name LIKE '%milestone%' OR table_name LIKE '%advance%')", dc)
    facts["dev_timeline_like_tables"] = [[r[0], r[1]] for r in rows]
    dc.close()
    dv.close()
except Exception as _e:  # noqa: BLE001
    _po = os.path.join(HERE, "M_SCIUI_INNOV_002_out.json")
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
papers_2025 = papers_by_year.get(2025)
papers_2020 = papers_by_year.get(2020)
out = {
    "metric_id": "M_SCIUI_INNOV_002",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/globalInnovationMonitor.js:37",
        "repos/demo-ui-science/src/globalInnovationMonitor.js:39-49",
        "repos/demo-ui-science/src/globalInnovationMonitor.js:268-284",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「全球创新趋势演进」该指标名未出现在三份说明书及主需求文档；最近语义为全球创新监测.md 头部 bid_desc『利用数据模型开展趋势预测和判断』与 seq 71 创新影响预测『用户可查看预测结果和趋势分析』、科技全域态势.md seq 12 时间轴趋势展示——均为功能描述非本指标定义",
    },
    "facts": facts,
    "derived": {
        "jiuxin_paper_growth_2020_2025_pct": {
            "value": round((papers_2025 - papers_2020) / papers_2020 * 100, 2),
            "numerator": papers_2025 - papers_2020,
            "denominator": papers_2020,
            "note": "分子=2025 与 2020 年 COUNTRY 级论文合计之差，分母=2020 年合计；同表同口径（ads_geo_yearly_metrics COUNTRY 级 SUM(paper_count)）",
        },
    },
    "absence_probe": probes,
    "support_judgment": "部分支持",
    "notes": [
        "mock 的 7 条叙事事件（波士顿基线入库/慕尼黑持续监测等）三源无承载：没有「创新事件叙事流水」表；本件以数字演进序列（四列指标按年）承接时间轴语义，叙事层需另立事件库",
        "2026 年是残年（论文 133,932 仅为部分年度快照），趋势解读须截至 2025；2025 论文 1,287,996 vs 2024 906,865 的跃升含采集口径因素，非纯增长",
        "project_count 2023 年 603,004 > 2025 年 392,032 呈下降态——项目维与论文维演进方向相反，多指标并读时不能单一叙事",
        "专利维年度序列（jurisdiction）是受理局维度（US/EP/CN/WO），与 COUNTRY 级地理维度不同源，并读需标注",
        "buildTrendSeries 的「预测窗口」线是种子生成（seed-8+index*6），预测语义由 M_SCIUI_INNOV_008 承接，本件只管历史演进段",
    ],
    "base_years_used": [str(y) for y in facts["jiuxin_country_yearly_years"] if y <= 2025],
    "base_years_missing": [],
    "base_years_note": "COUNTRY 级序列 2015-2026 连续；2026 为残年剔除出趋势解读（保留在产物）；专利维 2020-2025 连续",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "224", "1287996", "906865", "133932", "225.03", "42.03", "39.82", "603004", "392032", "100900","10126"]},
}
path = os.path.join(HERE, "M_SCIUI_INNOV_002_out.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", path)
print("support_judgment:", out["support_judgment"])
print("years:", facts["jiuxin_country_yearly_years"])
print("paper yoy:", facts["jiuxin_paper_yoy_pct"])
print("growth 2020-2025:", out["derived"]["jiuxin_paper_growth_2020_2025_pct"])

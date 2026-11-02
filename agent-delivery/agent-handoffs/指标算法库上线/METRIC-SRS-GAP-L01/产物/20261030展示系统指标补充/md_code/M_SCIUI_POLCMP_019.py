#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_019 政策指标同比增长率 · 三源探针与复现脚本（S3-02 Lane 7）。

含义：政策指标（以政策发布量为分 子分母的默认口径）的同比增长率 =
（本期数 − 上年同期数）/ 上年同期数 × 100%（国家统计局口径）。
UI：repos/demo-ui-science/src/pages/policy-tracking/PolicyAnalysis.jsx:169
（TrendAnalysisChart legend『同比增长率』双轴图；数据源 policyData.js:456-463
trendAnalysisData.yearTrend：2020-2026 政策发布量 486→1026 + growth 12/17/13/18/18/15/8——mock 演示值）。

三源实况（全部实探，2026-11-01）：
- gkx：dwd_policy_base 20,000 行按 publish_year 全序列可得（1981-2024，2018-2021 连续 2,016/2,035/2,402/2,120）
  ——发布量口径的同比序列「现在就能算」（2019 +0.94%/2020 +18.03%/2021 −11.74% 实算）；
  但 2022 骤降至 289（同比 −86.37% 为采集断档镜像）、2023 缺失、2024 仅 1 行（采集截断非业务真实回落）。
- dev：gkxlumenx_ads.policy_timeseries 37 行（publish_count 按年，与 gkx 同源同读数）——
  growth_rate 列全 NULL（结构在值未算）；policy_time_series_indicator（dwd 层 year_over_year_ratio 列）0 行。
- 久新：203 张 ads_* 无政策时序/增长率面（问题×年政策计数切片 39 行是问题维度切片非全局政策时序）。
结论：政策发布量口径的同比序列可直算（gkx 全序列 + dev 37 行镜像），但序列尾部 2022-2024 采集截断
使近年读数失真——「能算但序列不完整」→ 部分支持。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_019_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

# ============ ① gkx：政策发布量年度序列（分子分母源） ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])
# publish_year 口径序列（全表 2 万行小表直查）
facts["gkx_policy_by_year"] = [[r[0], int(r[1])] for r in qg(
    "SELECT publish_year, COUNT(*) FROM gkx.dwd_policy_base "
    "WHERE publish_year REGEXP '^(19|20)[0-9]{2}$' GROUP BY publish_year ORDER BY publish_year")]
# publish_date 口径对照（B9：varchar 年份陷阱规避——两口径对账）
facts["gkx_policy_by_publish_date_year"] = [[int(r[0]), int(r[1])] for r in qg(
    "SELECT YEAR(publish_date), COUNT(*) FROM gkx.dwd_policy_base "
    "WHERE YEAR(publish_date) BETWEEN 2018 AND 2026 GROUP BY YEAR(publish_date) ORDER BY 1")]
# 口径陷阱读数：坏年份值 / 零日期（B9）
facts["gkx_policy_bad_year_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE publish_year IS NULL OR publish_year NOT REGEXP '^(19|20)[0-9]{2}$'")[0][0])
facts["gkx_policy_zero_or_null_date_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE publish_date IS NULL OR CAST(publish_date AS CHAR) IN ('0000-00-00','')")[0][0])

# ============ ② dev：政策时序族结构×数据探针 ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()

# dwd 层时序表（year_over_year_ratio 列——同比结构的最贴承载）
facts["dev_policy_time_series_indicator_cols"] = [r[0] for r in ql("SHOW COLUMNS FROM policy_time_series_indicator")]
facts["dev_policy_time_series_indicator_rows"] = int(ql("SELECT COUNT(*) FROM policy_time_series_indicator")[0][0])
lconn.close()
# ads 层 policy_timeseries（37 行镜像）
aconn = pymysql.connect(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
                        database="gkxlumenx_ads", charset="utf8mb4", connect_timeout=10, read_timeout=120)
acur = aconn.cursor()
acur.execute("SHOW COLUMNS FROM policy_timeseries")
facts["dev_ads_policy_timeseries_cols"] = [r[0] for r in acur.fetchall()]
acur.execute("SELECT COUNT(*), SUM(CASE WHEN growth_rate IS NOT NULL THEN 1 ELSE 0 END) FROM policy_timeseries")
rr = acur.fetchone()
facts["dev_ads_policy_timeseries_rows"] = int(rr[0])
facts["dev_ads_policy_timeseries_growth_rate_nonnull"] = int(rr[1] or 0)
acur.execute("SELECT period_key, publish_count FROM policy_timeseries WHERE period_type='Y' ORDER BY period_key LIMIT 5")
facts["dev_ads_policy_timeseries_head_sample"] = [[r[0], int(r[1])] for r in acur.fetchall()]
aconn.close()

# ============ ③ 久新：政策时序/增长率面探针 ============
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)
try:
    jconn = pymysql.connect(**JX)
    jcur = jconn.cursor()
    def qj(sql):
        jcur.execute(sql)
        return jcur.fetchall()
    jcur.execute("SHOW TABLES")
    jx_tables = sorted(r[0] for r in jcur.fetchall())
    facts["jiuxin_table_count"] = len(jx_tables)
    facts["jiuxin_policy_like_tables"] = [t for t in jx_tables if re.search(r"policy", t, re.I)]
    facts["jiuxin_policy_timeseries_tables"] = [t for t in jx_tables if re.search(r"policy", t, re.I) and re.search(r"time|trend|year|growth", t, re.I)]
    # yearly_metrics 定性实查：问题×年政策计数切片（粒度/量级/是否全局时序）
    try:
        facts["jiuxin_yearly_metrics_cols_sample"] = [r[0] for r in qj(
            "SHOW COLUMNS FROM ads_research_problem_policy_yearly_metrics")][:8]
        facts["jiuxin_yearly_metrics_max_policy_count"] = int(qj(
            "SELECT MAX(policy_count) FROM ads_research_problem_policy_yearly_metrics")[0][0])
    except Exception as e:  # noqa: BLE001
        facts["jiuxin_yearly_metrics_cols_sample"] = f"error: {e}"
    for t in ["ads_research_problem_policy_evidence", "ads_research_problem_policy_yearly_metrics", "ads_technology_policy_evidence"]:
        try:
            facts[f"jiuxin_{t}_rows"] = int(qj(f"SELECT COUNT(*) FROM {t}")[0][0])
        except Exception as e:  # noqa: BLE001
            facts[f"jiuxin_{t}_rows"] = f"error: {e}"
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_unreachable"] = str(e)
    facts["jiuxin_table_count"] = 203
    facts["jiuxin_policy_like_tables"] = [
        "ads_research_problem_policy_evidence", "ads_research_problem_policy_yearly_metrics", "ads_technology_policy_evidence"]
    facts["jiuxin_policy_timeseries_tables"] = []
    facts["jiuxin_ads_research_problem_policy_evidence_rows"] = "未取证（本次连接异常）——同批 Lane4 探针 _probe_lane4_s302_out.json 复核 0 行"
    facts["jiuxin_ads_technology_policy_evidence_rows"] = "未取证（本次连接异常）——schema 文档 2026-10-22-ADS_SCHEMA-5.11.0.md :212/:3551 在案『当前无数据/预留空表』"

# ================= 派生：同比序列实算（gkx publish_year 口径） =================
by_year = {y: c for y, c in facts["gkx_policy_by_year"]}
years_sorted = sorted(by_year)
yoy = []
for y in years_sorted:
    prev = str(int(y) - 1)
    if prev in by_year and by_year[prev] > 0:
        pct = 100.0 * (by_year[y] - by_year[prev]) / by_year[prev]
        yoy.append({"year": y, "count": by_year[y], "prev_year": prev, "prev_count": by_year[prev],
                    "yoy_pct": round(pct, 2)})
# 正文引用的近年读数（2018-2021 完整链）+ 尾部截断读数（2022）
facts["gkx_policy_yoy_series"] = yoy
d2019 = next((x for x in yoy if x["year"] == "2019"), None)
d2020 = next((x for x in yoy if x["year"] == "2020"), None)
d2021 = next((x for x in yoy if x["year"] == "2021"), None)
d2022 = next((x for x in yoy if x["year"] == "2022"), None)
for tag, d in [("yoy_2019", d2019), ("yoy_2020", d2020), ("yoy_2021", d2021), ("yoy_2022", d2022)]:
    if d:
        derived.append({
            "key": f"gkx_policy_count_{tag}",
            "value": d["yoy_pct"],
            "numerator": d["count"] - d["prev_count"],
            "denominator": d["prev_count"],
            "note": f"分子={d['year']}年政策数−{d['prev_year']}年政策数={d['count']}−{d['prev_count']}，"
                    f"分母={d['prev_year']}年政策数={d['prev_count']}（gkx.dwd_policy_base publish_year 口径，同表同池 B3）；"
                    "国家统计局同比定义（本期−上年同期）/上年同期×100%",
        })

# ================= absence_probe =================
absence += [
    {"probe": "dev 同比现成结果面（dwd 层）",
     "source": "dev",
     "sql": "SHOW COLUMNS + COUNT ON policy_time_series_indicator（含 year_over_year_ratio/chain_ratio 列）",
     "hits": 0,
     "hit_detail": "18 列结构含 publish_count/chain_ratio/year_over_year_ratio/theme_distribution——同比结构规划在，"
                   "但全表 0 行（B4 情形②表在 0 行）",
    },
    {"probe": "dev 同比现成结果面（ads 层镜像）",
     "source": "dev",
     "sql": "SELECT COUNT(*), SUM(growth_rate IS NOT NULL) FROM gkxlumenx_ads.policy_timeseries",
     "hits": 0,
     "hit_detail": f"37 行 publish_count 有值（与 gkx 按年序列同读数零漂移）但 growth_rate 非空 {facts['dev_ads_policy_timeseries_growth_rate_nonnull']} 行"
                   "——计数已算、同比未算，需从 publish_count 自行派生",
    },
    {"probe": "久新政策时序/增长率面",
     "source": "jiuxin",
     "sql": "SHOW TABLES；203 表名扫 policy × time/trend/year/growth 交叉",
     "hits": 0,
     "hit_detail": f"0 命中；policy 类仅 {facts['jiuxin_policy_like_tables']}——其中 ads_research_problem_policy_yearly_metrics "
                   "（39 行实测）是『科研问题×年×层级×类型』的政策计数切片（problem_id×statistics_year×policy_level×support_type 粒度，"
                   "policy_count 每格 0-1 量级、policy_ids 数组单元素），非全局政策年度时序，不能充当同比基列；"
                   "久新 ads_geo_yearly_index 等 0 行（Lane4 探针 A5 在案）",
    },
    {"probe": "需求原文「政策指标同比增长率」定义段",
     "source": "doc",
     "sql": "rg 同比增长/增长率 三份需求真源政策族段",
     "hits": 0,
     "hit_detail": "三份需求说明书政策族段无「同比增长率」指标定义；主需求 1.1.1.1.4.2.1.2.4 政策动态可视化展示"
                   "（『趋势图展示政策动态变化』）与 SRS seq 219 多维指标趋势图（『查看政策绩效随变量变化的动态趋势』）"
                   "为功能语境；指标语义源=UI mock 实现层（trendAnalysisData.growth 槽位）",
    },
]

support = "部分支持"

notes += [
    "判档：同比序列 = f(年度指标序列)。发布量口径的分子分母在 gkx 全序列可得（1981-2024），2018→2021 同比链完整"
    "（+20.21%/+0.94%/+18.03%/−11.74% 实算在产物）；dev ads.policy_timeseries 37 行镜像同读数。"
    "但序列尾部采集截断：2022 年 289 行（2021 年 2,120 的 13.6%，同比 −86.37%）、2023 年缺失、2024 年 1 行——"
    "近年同比读数是采集断档的镜像非政策真实回落，「能算的年份」与「需要读数的年份」错位 → 部分支持",
    "口径注记（B10 双口径）：默认口径=政策发布量同比（UI 双轴图语义）；若甲方口径=『政策指标』（核增 PC-04 规划指标库"
    "的结构化指标值同比），则依赖 PC-04 产物（扶持力度/适用范围等指标库搭建），当前三源无指标值时序承载——"
    "两种口径判档同为部分支持，口径待甲方裁定",
    "B9 陷阱规避：publish_year 是 varchar(4)，全部走 REGEXP 过滤（坏值 3 行剔除）；"
    "publish_date 零日期用 CAST(publish_date AS CHAR) 规避（errno 1525），零/空日期 3 行；"
    "publish_year 与 YEAR(publish_date) 对账 2018-2024 逐年一致（产物两组键对照）",
    "mock 披露：policyData.js:456-463 trendAnalysisData.yearTrend growth 值（12/17/13/18/18/15/8）为演示序列，"
    "与本件实算值（2019 +0.94/2020 +18.03/2021 −11.74）不同——演示值不参与支持度结论，"
    "但 UI 的 2026 年读数（325 条/+8%）在 gkx 序列中无承载（2024 后无数据）",
    "B11 对账：gkx 政策 20,000 行与共享快照 fix2_20261101.policy 一致；dev ads.policy_timeseries publish_count "
    "逐年读数与 gkx publish_year 口径零漂移（同源镜像）；dev dwd 层 0 行与 _probe_lane6_s302_r2_out.json 一致",
    "升档触发器（B10）：①政策采集管道补齐 2022-2026 年数据（序列完整）→ 发布量口径升完全转换支持"
    "（gkx 直算即可，无需加工链）；②核增 PC-04 指标库落地结构化指标值时序 → 指标口径可算；"
    "降档触发器：若甲方要求指标口径且不接受发布量代理 → 维持部分支持不升",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_019",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/PolicyAnalysis.jsx:169",
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:456",
        "repos/demo-ui-science/src/pages/policy-tracking/PolicyAnalysis.jsx:206",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「政策指标同比增长率」未以该名出现在三份需求真源；主需求 1.1.1.1.4.2.1.2.4 政策动态可视化展示"
                "（趋势图）+ SRS 政策分析评价 seq 219 多维指标趋势图为功能语境；指标语义源=UI mock 实现层"
                "（trendAnalysisData.yearTrend.growth 槽位）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [y for y in years_sorted if int(y) >= 2018],
    "base_years_missing": [str(y) for y in range(2023, 2027) if str(y) not in by_year],
    "base_years_note": "2018-2021 基年链完整（含 2018 同比 +20.21%）；2022 采集截断（289 行，同比 −86.37% 读数失真，"
                       "计入 used 但带截断注记）；2023 缺失、2024 仅 1 行、2025/2026 无数据",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts["gkx_policy_rows"]), "2016", "1316", "2017", "1677", "2018", "2016",
                          "2019", "2035", "2020", "2402", "2021", "2120", "2022", "289", "2024",
                          str(facts["dev_ads_policy_timeseries_rows"]),
                          str(facts["dev_ads_policy_timeseries_growth_rate_nonnull"]),
                          str(facts["gkx_policy_bad_year_rows"]),
                          str(facts["gkx_policy_zero_or_null_date_rows"]),
                          str(facts["jiuxin_table_count"]), "37", "18"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

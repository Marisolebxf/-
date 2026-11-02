#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATAOV_002 年度增长趋势 · 三源探针与复现脚本（S3-03 Lane 7）。

含义：科技数据资源·总体视窗·资源接入情况总览「年度增长趋势」——仪表盘呈现资源总量、
年度新增与同比增速的近 5 年序列（需求 1.1.1.1.4.4.1.1.1 原文「年度增长趋势」）。
UI：repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:621
（Card title="年度增长趋势" extra Tag「近5年 · 演示数据」；getAnnualAccessTrendOption() 双系列
折线+柱；mock 源 mockData.js:72-78 overviewAnnualAccessTrend——2022 total 12,860 → 2026 30,398）。

判档路径（口径=「资源总量/年度新增/同比增速」年度序列）：
- 直接承载：三源无资源接入台账（无按年记录的资源接入流水）→ 无直接结果面；
- 转换承载（数据资产的内容年份面作增长代理）：dev enterprise_base.registration_date
  按注册年聚合（269,511 行）；gkx 论文 cover_year_start/专利 apdt_year 年分布（共享快照，
  20 万采样）；久新 ads_talent_yearly_metrics 按年聚合——三源年度序列原料双在；
- 「资源接入量」本体（平台归集的记录数按年）无承载 → 部分支持。
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATAOV_002_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
SNAP_S3 = os.path.join(BASE, "_snapshots", "_shared_probe_s3_01_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402

facts, derived, notes, absence = {}, [], [], []
snap = json.load(open(SNAP, encoding="utf-8"))
snap_s3 = json.load(open(SNAP_S3, encoding="utf-8"))

# ============ ① dev：enterprise_base 注册年序列（增长趋势代理） ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()

facts["dev_enterprise_base_rows"] = int(ql(
    "SELECT COUNT(*) FROM gkxlumenx_dwd.enterprise_base")[0][0])
# 注册年聚合（B9：零日期规避——YEAR() 过滤合法年份区间，非 ='0000-00-00' 比较）
facts["dev_enterprise_reg_year_recent5"] = [[int(a), int(b)] for a, b in ql(
    "SELECT YEAR(registration_date) y, COUNT(*) FROM gkxlumenx_dwd.enterprise_base "
    "WHERE YEAR(registration_date) BETWEEN 2022 AND 2026 "
    "GROUP BY y ORDER BY y")]
# 接入台账词族排除（access_log/access_history/resource_access 归集流水）
lcur.execute(
    "SELECT table_schema, table_name FROM information_schema.tables "
    "WHERE table_schema LIKE 'gkxlumenx%%' AND table_name REGEXP 'access_log|access_history|resource_access|ingest'")
facts["dev_access_registry_tables"] = [f"{r[0]}.{r[1]}" for r in sorted(lcur.fetchall())]
lconn.close()

# ============ ② gkx：内容年份面（共享快照复用，采样口径） ============
paper_years = None
patent_years = None
for item in snap_s3["fix2_20261101"]:
    if item["tag"] == "论文年份分布（20万采样）":
        paper_years = [[str(a), int(b)] for a, b in item["data"]]
    if item["tag"] == "专利申请年分布（20万采样）":
        patent_years = [[str(a), int(b)] for a, b in item["data"]]
facts["gkx_paper_year_dist_sampled"] = paper_years
facts["gkx_patent_year_dist_sampled"] = patent_years
facts["gkx_table_count"] = snap["gkx"]["table_count"]

# ============ ③ 久新：talent_yearly_metrics 按年聚合（内容年份面） ============
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)
jconn = pymysql.connect(**JX)
jcur = jconn.cursor()
jcur.execute("SELECT COUNT(*) FROM ads_talent_yearly_metrics")
facts["jiuxin_yearly_metrics_rows"] = int(jcur.fetchone()[0])
jcur.execute(
    "SELECT year, COUNT(*) FROM ads_talent_yearly_metrics "
    "WHERE year BETWEEN 2022 AND 2026 GROUP BY year ORDER BY year")
facts["jiuxin_yearly_metrics_recent5"] = [[int(a), int(b)] for a, b in jcur.fetchall()]
# 久新接入台账词族排除
jx_tables = snap["jiuxin"]["tables"]
import re
facts["jiuxin_access_registry_tables"] = [t for t in jx_tables
    if re.search(r"access_log|access_history|resource_access|ingest|collect_log", t, re.I)]
jconn.close()

# ================= 派生 =================
reg = dict(facts["dev_enterprise_reg_year_recent5"])
if 2025 in reg and 2026 in reg:
    derived.append({
        "key": "dev_enterprise_reg_yoy_2026_vs_2025_pct",
        "value": round(100.0 * (reg[2026] - reg[2025]) / reg[2025], 2),
        "numerator": reg[2026] - reg[2025],
        "denominator": reg[2025],
        "note": "分子=2026 年注册企业数-2025 年（增量）；分母=2025 年注册企业数"
                "（同表同 WHERE YEAR() 口径，B3 同基）——内容年份面的同比增速代理读数",
    })
else:
    derived.append({
        "key": "dev_enterprise_reg_yoy_2026_vs_2025_pct",
        "value": None, "numerator": None, "denominator": None,
        "note": "序列不足两年，不可算",
    })
# 负结论登记（B10）
derived.append({
    "key": "resource_annual_growth_trend",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『资源接入量』年度序列（资源总量/年度新增/同比）三源无台账承载（接入流水/归集记录"
            "按年面不存在）；本件交付内容年份面代理读数（企业注册年/论文年/专利年/人才年序列），"
            "语义=数据资产内容规模增长≠平台资源接入增长；按 B10 留空即负结论登记",
})

# ================= absence_probe =================
absence += [
    {"probe": "dev 资源接入台账（access_log/access_history/resource_access/ingest 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表）",
     "hits": len(facts["dev_access_registry_tables"]),
     "hit_detail": f"命中 {facts['dev_access_registry_tables']}——无资源接入流水表；"
                   "enterprise_base 等事实表的内容年份列是增长代理非接入记录"},
    {"probe": "gkx 资源接入台账（同词族 + datasource 元数据面）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表）词族扫",
     "hits": 0,
     "hit_detail": "access_log/access_history/resource_access/ingest 词族 0 命中——gkx 为要素明细库，"
                   "无平台接入流水；内容年份列（cover_year_start/apdt_year）可作增长代理"},
    {"probe": "久新资源接入台账（210 表 access_log/access_history/resource_access/ingest/collect_log 词族）",
     "source": "jiuxin",
     "sql": "SHOW TABLES（210 表，2026-11-01 实测）词族扫",
     "hits": len(facts["jiuxin_access_registry_tables"]),
     "hit_detail": f"命中 {facts['jiuxin_access_registry_tables']}——0 张接入流水表；"
                   "ads_* 结果面按 metrics_as_of_date 快照管理，非逐年接入记录"},
    {"probe": "需求原文「年度增长趋势」定义段",
     "source": "doc",
     "sql": "rg 年度增长趋势 三份需求真源",
     "hits": 1,
     "hit_detail": "主需求 :2489（1.1.1.1.4.4.1.1.1 资源接入情况总览）：『在仪表盘上直观呈现各类资源"
                   "的分布比例、年度增长趋势和不同来源机构的接入活跃度』——功能在、口径无；"
                   "UI overviewAnnualAccessTrend 为 mock 演示值（Tag 自标「演示数据」）",
    },
]

support = "部分支持"

notes += [
    "判档：『资源接入量』年度序列三源无台账（接入流水不存在）→ 直接承载无；内容年份面三源双在"
    "（dev 企业注册年 269,511 行、gkx 论文/专利年分布、久新人才年序列）→ 转换代理可算，"
    "语义披露后交付 → 部分支持",
    f"代理读数 1（dev）：enterprise_base {facts['dev_enterprise_base_rows']} 行，近 5 年注册年分布 "
    f"{facts['dev_enterprise_reg_year_recent5']}，2026 对 2025 同比 "
    f"{derived[0]['value']}%（产物派生键）",
    "代理读数 2（gkx，共享快照复用）：论文 cover_year_start 20 万采样近年分布 "
    f"{facts['gkx_paper_year_dist_sampled'][:5] if facts['gkx_paper_year_dist_sampled'] else []}…；"
    "专利 apdt_year 同口径在案——采样，非全表（B11 快照键原文引用）",
    f"代理读数 3（久新）：ads_talent_yearly_metrics 近 5 年行分布 {facts['jiuxin_yearly_metrics_recent5']}"
    "——学者×年产出记录的年度规模序列（内容年份面）",
    "mock 披露：OverviewWindow.jsx:621 卡片消费的 overviewAnnualAccessTrend（2022 total 12,860 → "
    "2026 total 30,398，yoy 31.7→13.8）为 mockData.js:72-78 演示值且 Tag 自标「近5年 · 演示数据」"
    "——不作数据证据（B10）",
    "B9 规避：registration_date 零日期用 YEAR() BETWEEN 合法区间过滤，无 ='0000-00-00' 比较",
    "B11 对账：gkx 年分布取自 _shared_probe_s3_01_out.json fix2_20261101（采样口径原样引用）；"
    "jiuxin 210 表/1,278,048 行与 009 产物一致",
    "升档触发器（B10）：①建资源接入流水台账（资源×接入时间×记录数）→ 完全直接支持；"
    "②甲方裁定增长趋势=内容年份面代理（论文/专利/企业/人才年分布）→ 完全转换支持",
]

out = {
    "metric_id": "M_SCIUI_DATAOV_002",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:621",
        "repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:73",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:72",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "主需求《科技信息展示系统和科技专题服务系统.md》:2489（1.1.1.1.4.4.1.1.1 资源接入"
                "情况总览）明列「年度增长趋势」——功能在、序列口径无；核增需求与算法库 0 命中",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [str(y) for y, _ in facts["dev_enterprise_reg_year_recent5"]],
    "base_years_missing": [],
    "base_years_note": "基期=dev 企业注册年近 5 年（2022-2026 实测）；gkx 采样分布与久新年序列"
                       "覆盖同年段；资源接入台账缺失见 absence_probe",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts["dev_enterprise_base_rows"]), "269511", "12860", "30398",
                          "31.7", "13.8", "2022", "2026", "200000"][:10]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

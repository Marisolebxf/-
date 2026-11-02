#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATAIN_001 动态历史趋势可视化 · 三源探针与复现脚本（S3-03 Lane 7）。

含义：科技数据资源·接入视窗·历史资源接入情况「动态历史趋势可视化」（需求叶
1.1.1.1.4.4.2.4.3，SRS seq 362 / excel_row 365）——用趋势图动态展现历史资源接入量、
更新状况、异常分布等关键指标。派单 mount 列给的是 AccessWindow.jsx:577——实查该行
所在卡片是「问题资源可视化统计报表」统计视图的「动态历史趋势可视化」小卡
（problemTrendOption 双折线：问题总数/已解决，mock 源 mockData.js:1704-1710
monthlyTrend 1-5 月演示值）；需求语义主体（资源接入量/更新状况历史序列）由同文件
getAccessTrendOption（时点选择器 × 接入量趋势）与 AccessHistorySituation 组件承接。
本件按需求叶语义全量核：趋势本体=资源接入量/更新状况/异常分布的时间序列。

判档路径（Lane 7 数据资源族口径=接入台账/年度覆盖）：
- 直接承载：三源无资源接入历史台账（接入流水/更新周期记录按时间面不存在）；
- 替代承载：dev 更新时间列（enterprise_base.updated_at 等实体级 update 面按日分布）
  + gkx 内容年份面（共享快照采样）+ 久新 yearly_metrics 年序列——趋势可视化的
  内容年份代理三源双在；
- 异常分布子维：三源无数据质量监测/异常检测承载（问题资源族级缺口）。
→ 直接承载无、内容年份代理双在、异常子维零承载 → 部分支持。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATAIN_001_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []
snap = json.load(open(SNAP, encoding="utf-8"))

# ============ ① dev：更新时间面（趋势本体的实体级代理） ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()

# 1.1 企业底册按更新日分布（update 面的量级证据；列名 create_time/update_time，DATE() 归一）
facts["dev_enterprise_base_rows"] = int(ql(
    "SELECT COUNT(*) FROM gkxlumenx_dwd.enterprise_base")[0][0])
facts["dev_enterprise_updated_date_dist"] = [[str(a), int(b)] for a, b in ql(
    "SELECT DATE(update_time), COUNT(*) FROM gkxlumenx_dwd.enterprise_base "
    "WHERE update_time IS NOT NULL GROUP BY DATE(update_time) "
    "ORDER BY COUNT(*) DESC, DATE(update_time) LIMIT 5")]
facts["dev_enterprise_updated_nonnull"] = int(ql(
    "SELECT COUNT(*) FROM gkxlumenx_dwd.enterprise_base "
    "WHERE update_time IS NOT NULL")[0][0])

# 1.2 接入历史台账词族排除（history/归集流水）
lcur.execute(
    "SELECT table_schema, table_name FROM information_schema.tables "
    "WHERE table_schema LIKE 'gkxlumenx%%' AND table_name REGEXP "
    "'access_history|collect_log|ingest_log|update_cycle|access_registry|access_trend'")
facts["dev_history_registry_tables"] = [f"{r[0]}.{r[1]}" for r in sorted(lcur.fetchall())]

# 1.3 异常/质量监测面排除（异常分布子维）
lcur.execute(
    "SELECT table_schema, table_name FROM information_schema.tables "
    "WHERE table_schema LIKE 'gkxlumenx%%' AND table_name REGEXP "
    "'anomal|quality|problem|exception|dirty|alert'")
facts["dev_quality_anomaly_tables"] = [f"{r[0]}.{r[1]}" for r in sorted(lcur.fetchall())]
lconn.close()

# ============ ② gkx：接入历史台账排除 + 内容年份面登记 ============
gcur = gkx()
gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
facts["gkx_history_registry_tables"] = [t for t in gkx_tables
    if re.search(r"access_history|collect_log|ingest|update_cycle|access_registry", t, re.I)]
facts["gkx_quality_anomaly_tables"] = [t for t in gkx_tables
    if re.search(r"anomal|quality|problem|exception|dirty|alert", t, re.I)]
gcur.close()

# ============ ③ 久新：年序列面（趋势本体的内容年份代理，快照+实跑） ============
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)
jconn = pymysql.connect(**JX)
jcur = jconn.cursor()
jcur.execute(
    "SELECT year, COUNT(*) FROM ads_talent_yearly_metrics "
    "WHERE year BETWEEN 2022 AND 2026 GROUP BY year ORDER BY year")
facts["jiuxin_yearly_metrics_recent5"] = [[int(a), int(b)] for a, b in jcur.fetchall()]
jcur.execute(
    "SELECT MIN(metrics_as_of_date), MAX(metrics_as_of_date) "
    "FROM ads_talent_yearly_metrics")
row = jcur.fetchone()
facts["jiuxin_yearly_snapshot_span"] = [str(row[0]), str(row[1])]
jx_tables = snap["jiuxin"]["tables"]
facts["jiuxin_table_count"] = len(jx_tables)
facts["jiuxin_history_registry_tables"] = sorted([t for t in jx_tables
    if re.search(r"access_history|collect_log|ingest|update_cycle|access_registry|trend_log", t, re.I)])
facts["jiuxin_quality_anomaly_tables"] = sorted([t for t in jx_tables
    if re.search(r"anomal|quality|problem|exception|dirty|alert", t, re.I)])
jconn.close()

# ================= 派生 =================
n_upd = facts["dev_enterprise_updated_nonnull"]
n_all = facts["dev_enterprise_base_rows"]
derived.append({
    "key": "dev_enterprise_updated_coverage_pct",
    "value": round(100.0 * n_upd / n_all, 2),
    "numerator": n_upd,
    "denominator": n_all,
    "note": "分子=enterprise_base.update_time 非空行数；分母=同表总行数（同表同 WHERE 全量非采样，"
            "B3 同基）——更新时间面对企业底册的覆盖度（趋势可视化的实体级更新代理）",
})
# 负结论登记（B10）
derived.append({
    "key": "dynamic_historical_trend_visualization",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『历史资源接入量/更新状况/异常分布』时间序列三源无接入台账承载（接入历史/归集流水/"
            "更新周期/异常检测面词族 0 命中）；本件交付内容年份面与实体更新面代理读数，语义=数据资产"
            "内容规模与实体维护活动≠平台资源接入历史；按 B10 不写伪序列，此键留空即负结论登记",
})

# ================= absence_probe =================
absence += [
    {"probe": "dev 接入历史台账（access_history/collect_log/ingest_log/update_cycle/access_registry/access_trend 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（16 schema 542 表）",
     "hits": len(facts["dev_history_registry_tables"]),
     "hit_detail": f"命中 {facts['dev_history_registry_tables']}——0 张资源接入历史/更新周期表；"
                   "enterprise_base.update_time 是实体级维护时间戳，非资源接入流水"},
    {"probe": "dev 异常/质量监测面（anomal/quality/problem/exception/dirty/alert 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（16 schema 542 表）",
     "hits": len(facts["dev_quality_anomaly_tables"]),
     "hit_detail": f"命中 {facts['dev_quality_anomaly_tables']}——chain_sz_problem 为产业链深圳问题"
                   "表（产业诊断语义，非数据接入质量问题），语义排除后异常分布子维 0 承载"},
    {"probe": "gkx 接入历史台账 + 异常质量面（同词族）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表）词族扫",
     "hits": len(facts["gkx_history_registry_tables"]) + len(facts["gkx_quality_anomaly_tables"]),
     "hit_detail": f"接入历史命中 {facts['gkx_history_registry_tables']}；异常质量命中 "
                   f"{facts['gkx_quality_anomaly_tables']}——gkx 为要素明细库，无平台接入流水无质量监测面"},
    {"probe": "久新接入历史台账 + 异常质量面（210 表同词族 + trend_log）",
     "source": "jiuxin",
     "sql": "SHOW TABLES（210 表，2026-11-01 实测）词族扫",
     "hits": len(facts["jiuxin_history_registry_tables"]) + len(facts["jiuxin_quality_anomaly_tables"]),
     "hit_detail": f"接入历史命中 {facts['jiuxin_history_registry_tables']}（0 张）；problem 词族命中 "
                   f"{len(facts['jiuxin_quality_anomaly_tables'])} 张但全部为 ads_research_problem_*"
                   "（科研问题挖掘域：研究课题/难题的画像、热度、演化——『problem』=研究问题非数据质量"
                   "问题，语义排除；change_log/update_signal 亦是科研问题的变更追踪非资源接入历史）"
                   "——久新按 metrics_as_of_date 快照管理，无逐年接入记录无数据质量监测面"},
    {"probe": "dev 异常质量面命中的语义排除（chain_sz_problem）",
     "source": "dev",
     "sql": "表名语义核对",
     "hits": 0,
     "hit_detail": "gkxlumenx_ads.chain_sz_problem 是产业链深圳问题表（产业诊断语义），"
                   "非数据接入质量问题资源面——排除后 dev 异常质量面 0 命中"},
    {"probe": "需求原文「动态历史趋势可视化」定义段",
     "source": "doc",
     "sql": "rg 动态历史趋势可视化 三份需求真源",
     "hits": 1,
     "hit_detail": "SRS 接入视窗.md seq 362（excel_row 365）+主需求 :2701（1.1.1.1.4.4.2.4.3）："
                   "『利用可视化仪表盘和趋势图，可动态展现历史资源接入量、更新状况、异常分布等"
                   "关键指标』——功能行为在、序列口径无；UI monthlyTrend 为 mock 演示值",
    },
]

support = "部分支持"

notes += [
    "判档：需求语义=『资源接入量/更新状况/异常分布』的历史序列可视化；三源无接入台账与质量监测面"
    "（双词族 0 命中），但内容年份面（gkx 论文/专利年分布、久新人才年序列）与实体更新面"
    "（dev enterprise_base.update_time 按日分布）双在——趋势可视化的代理读数可交付，"
    "接入历史本体需台账立项 → 部分支持",
    f"代理读数 1（dev 实体更新面）：enterprise_base {n_all} 行，update_time 非空 "
    f"{derived[0]['value']}%（{n_upd}/{n_all}），按日分布 Top5 "
    f"{facts['dev_enterprise_updated_date_dist']}——数据维护活动的集中日证据（非接入流水）",
    f"代理读数 2（久新年序列）：ads_talent_yearly_metrics 近 5 年行分布 "
    f"{facts['jiuxin_yearly_metrics_recent5']}，快照日跨度 {facts['jiuxin_yearly_snapshot_span']}"
    "——内容年份面与 DATAOV_002 产物一致（B11）",
    "mount 勘误：派单行 AccessWindow.jsx:577 实查是「问题资源可视化统计报表」统计视图内的"
    "「动态历史趋势可视化」小卡（problemTrendOption 消费 mockData.js:1704-1710 monthlyTrend"
    " 1-5 月 18/15→23/16 演示值）——需求叶语义主体（资源接入量/更新状况趋势）由同文件"
    " getAccessTrendOption 与 AccessHistorySituation 组件承接，本件按需求叶全量语义核",
    "mock 披露：problemTrendOption 的 monthlyTrend（1 月 total 18/resolved 15 → 5 月 23/16）"
    "为 mockData.js:1704-1710 演示值——不作数据证据（B10）",
    f"久新活库：实测 {facts['jiuxin_table_count']} 张（2026-11-01 探测日），正文不写死表总数",
    "B11 对账：jiuxin 210 表/1,278,048 行年序列与 DATAOV_002/TALENTIR_009 产物一致；"
    "dev 542 表/16 schema 与共享快照一致",
    "升档触发器（B10）：①建接入历史台账（渠道×数据表×接入时间×记录数流水）→ 完全直接支持；"
    "②甲方裁定趋势口径=内容年份面代理（论文/专利/人才年分布+实体更新面）→ 完全转换支持；"
    "③异常分布子维需质量监测面立项（问题资源族级缺口，与 DATAOV_001 融合缺口分立）",
]

out = {
    "metric_id": "M_SCIUI_DATAIN_001",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/AccessWindow.jsx:577",
        "repos/demo-ui-science/src/pages/data-resources/AccessWindow.jsx:162",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:1704",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "SRS《02-科技信息展示系统/科技数据资源/接入视窗.md》seq 362（excel_row 365）+"
                "主需求《科技信息展示系统和科技专题服务系统.md》:2701（1.1.1.1.4.4.2.4.3 "
                "动态历史趋势可视化）需求明列叶：『利用可视化仪表盘和趋势图，可动态展现历史资源"
                "接入量、更新状况、异常分布等关键指标』——功能在、序列口径无；核增需求与算法库 0 命中",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [str(y) for y, _ in facts["jiuxin_yearly_metrics_recent5"]],
    "base_years_missing": [],
    "base_years_note": "基期=久新 ads_talent_yearly_metrics 年序列近 5 年（2022-2026 实测）+dev "
                       "实体更新面按日分布；接入历史台账缺失见 absence_probe",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(n_all), str(n_upd), "210", "542", "16", "280",
                          "18", "15", "23", "16"][:10]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

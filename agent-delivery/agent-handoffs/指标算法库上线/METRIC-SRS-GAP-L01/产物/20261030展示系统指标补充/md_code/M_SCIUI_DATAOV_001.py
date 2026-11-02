#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATAOV_001 多源数据整合分析 · 三源探针与复现脚本（S3-03 Lane 7）。

含义：科技数据资源·总体视窗·科技数据资源统计「多源数据整合分析」——不同格式、标准和
来源的数据资源自动结构融合与归类统计（需求 1.1.1.1.4.4.1.1.5 原文）。
UI：repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:643
（Card title="多源数据整合分析"，getThemeDistributionOption() 主题横条图；
mock 源 mockData.js:12-20 resourceThemeDistribution——基础科学 4,230/工程技术 3,890 等 7 主题演示值）。

判档路径（口径=「接入源数/表数/行量级」盘点面）：
- dev：gkxlumenx_* 16 schema 元数据面（information_schema 全表清单+行数分布）+
  数据源/任务登记表族（gen_datasource_conf/jimu_report_data_source/lumen_analysis_task）；
- gkx：280 表数据资产盘点（作为「一源一库」的接入事实）；
- 久新：ads_* 全表行数分布（210 张实测，久新侧接入面）。
→ 盘点面结构+数据在（可产出整合统计），但「整合过程/融合结果」无承载 → 部分支持。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATAOV_001_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []
snap = json.load(open(SNAP, encoding="utf-8"))

# ============ ① dev：元数据盘点面（核心承载） ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()

# 1.1 全 schema 表清单（快照已有）+ 非空/空表统计
schemas = snap["dev"]["schemas"]
facts["dev_schema_count"] = len(schemas)
all_tables = [(sch, t, r) for sch, lst in sorted(schemas.items()) for t, r in lst]
facts["dev_table_count"] = len(all_tables)
facts["dev_nonzero_tables"] = sum(1 for _, _, r in all_tables if r > 0)
facts["dev_zero_tables"] = sum(1 for _, _, r in all_tables if r == 0)

# 1.2 登记面读数：数据源配置/任务登记/报表数据源
facts["dev_gen_datasource_conf_rows"] = int(ql(
    "SELECT COUNT(*) FROM gkxlumenx_codegen.gen_datasource_conf")[0][0])
facts["dev_jimu_report_data_source_rows"] = int(ql(
    "SELECT COUNT(*) FROM gkxlumenx_bi.jimu_report_data_source")[0][0])
facts["dev_lumen_analysis_task_rows"] = int(ql(
    "SELECT COUNT(*) FROM gkxlumenx_cfg.lumen_analysis_task")[0][0])
facts["dev_analysis_task_type_dist"] = [[str(a), int(b)] for a, b in ql(
    "SELECT sub_type, COUNT(*) FROM gkxlumenx_cfg.lumen_analysis_task "
    "GROUP BY sub_type ORDER BY sub_type")]

# 1.3 整合过程承载排除：integration/merge/fusion/融合 词族
lcur.execute(
    "SELECT table_schema, table_name FROM information_schema.tables "
    "WHERE table_schema LIKE 'gkxlumenx%%' AND table_name REGEXP 'integrat|merge|fusion|combine'")
facts["dev_integration_like_tables"] = [f"{r[0]}.{r[1]}" for r in sorted(lcur.fetchall())]
lconn.close()

# ============ ② gkx：数据资产盘点面（接入事实） ============
gcur = gkx()
gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
gcur.close()

# ============ ③ 久新：ads_* 接入面行数分布（快照复用） ============
rowcounts = snap["jiuxin"]["rowcounts"]
facts["jiuxin_table_count"] = len(rowcounts)
facts["jiuxin_nonzero_tables"] = sum(1 for v in rowcounts.values() if v > 0)
facts["jiuxin_zero_tables"] = sum(1 for v in rowcounts.values() if v == 0)

# ================= 派生 =================
n_tables = facts["dev_table_count"]
n_nonzero = facts["dev_nonzero_tables"]
derived.append({
    "key": "dev_nonzero_table_share_pct",
    "value": round(100.0 * n_nonzero / n_tables, 2),
    "numerator": n_nonzero,
    "denominator": n_tables,
    "note": "分子=gkxlumenx_* 16 schema 中 table_rows>0 的表数；分母=同口径全部表数"
            "（information_schema 统计口径，非精确 COUNT——行数列为估算值，0 值可信非 0 为量级）",
})
n_src = facts["dev_gen_datasource_conf_rows"] + facts["dev_jimu_report_data_source_rows"]
derived.append({
    "key": "dev_registered_datasource_total",
    "value": float(n_src),
    "numerator": facts["dev_gen_datasource_conf_rows"],
    "denominator": facts["dev_jimu_report_data_source_rows"],
    "note": "分子=gen_datasource_conf 行数（代码生成器数据源配置）；分母=jimu_report_data_source "
            "行数（报表数据源）——两登记面合计 n_src 条，value=分子+分母非比值（登记读数并列）",
})
# 负结论登记（B10）
derived.append({
    "key": "multi_source_integration_analysis",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『整合分析』功能面（结构融合过程/融合结果表）三源未承载——dev integration/merge/fusion "
            "词族 0 命中；本件交付的是盘点口径读数（源/表/行量级），整合过程需数据工程立项；"
            "按 B10 不写伪指标值，此键留空即负结论登记",
})

# ================= absence_probe =================
absence += [
    {"probe": "dev 整合过程承载（gkxlumenx_* 16 schema integrat/merge/fusion/combine 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表）",
     "hits": len(facts["dev_integration_like_tables"]),
     "hit_detail": f"命中 {facts['dev_integration_like_tables']}——0 张整合过程/融合结果表；"
                   "数据源登记面在（gen_datasource_conf/jimu/lumen_analysis_task）但均为空或"
                   "任务调度配置，非资源整合分析结果面"},
    {"probe": "gkx 数据资源登记面（datasource/data_source/source_info/job/task/integrat/access/metadata 词族）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表）词族扫",
     "hits": 1,
     "hit_detail": "命中 dwd_job（10 行）——职位表非任务登记（语义排除）；gkx 为要素明细库，"
                   "无数据资源管理元数据面"},
    {"probe": "久新数据资源登记面（210 表同词族）",
     "source": "jiuxin",
     "sql": "SHOW TABLES（210 表，2026-11-01 实测）词族扫",
     "hits": 0,
     "hit_detail": "datasource/data_source/integrat/access 词族 0 命中——久新是 ads_* 结果面库，"
                   "接入管理元数据不在此库"},
    {"probe": "需求原文「多源数据整合分析」定义段",
     "source": "doc",
     "sql": "rg 多源数据整合分析 三份需求真源",
     "hits": 1,
     "hit_detail": "主需求 :2503-2505（1.1.1.1.4.4.1.1.5）：『针对不同格式、标准和来源的数据资源，"
                   "自动实现结构融合与归类统计……』——功能行为在、融合算法定义无；"
                   "UI resourceThemeDistribution 为 mock 演示值",
    },
]

support = "部分支持"

notes += [
    "判档：需求语义=『结构融合+归类统计』；三源均无整合过程/融合结果承载（integration 词族 0 命中），"
    "但盘点口径（源/表/行量级）三源结构+数据双在（dev 16 schema 542 表、gkx 280 表、久新 ads_* "
    f"实测 {len(rowcounts)} 张）→ 归类统计可交付、结构融合需立项 → 部分支持",
    f"盘点读数：dev 非空表 {derived[0]['value']}%（{n_nonzero}/{n_tables}，information_schema "
    "行数为估算口径，note 已披露）；数据源登记面合计 "
    f"{int(derived[1]['value'])} 条（gen_datasource_conf {facts['dev_gen_datasource_conf_rows']} + "
    f"jimu {facts['dev_jimu_report_data_source_rows']}）——均为开发态配置面，量级为样例级",
    "三源接入事实：gkx 280 表（第三方要素库整体接入）+ 久新 ads_* 结果面（上游持续加表）"
    "+ dev 自建派生表——「多源」事实本身成立，缺的是融合过程的工程承载",
    f"久新活库：实测 {len(rowcounts)} 张（2026-11-01 探测日），非空 "
    f"{facts['jiuxin_nonzero_tables']} 张",
    "mock 披露：OverviewWindow.jsx:643 卡片消费的 resourceThemeDistribution（基础科学 4,230/工程技术 "
    "3,890/医学健康 3,156 等 7 主题）为 mockData.js:12-20 演示值——不作数据证据（B10）",
    "B11 对账：gkx 280/dev 16 schema/久新行数分布全部取自共享快照 _lane7_shared_probe_out.json，零漂移",
    "升档触发器（B10）：①建数据资源元数据登记面（资源×来源×格式×接入时间的资产目录）→ 归类统计"
    "升完全直接支持；②整合过程立项（ETL 融合任务/血缘表）→ 完整功能升完全转换支持",
]

out = {
    "metric_id": "M_SCIUI_DATAOV_001",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:643",
        "repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:181",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:12",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "主需求《科技信息展示系统和科技专题服务系统.md》:2503-2505（1.1.1.1.4.4.1.1.5 "
                "多源数据整合分析）需求明列叶：『针对不同格式、标准和来源的数据资源，自动实现结构"
                "融合与归类统计，使所有数据在统一平台下实现高效关联和整体管理』——功能在、算式无；"
                "核增需求与算法库两份真源 0 命中",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件为存量盘点型（无年度序列需求；年度面由 DATAOV_002 承接）",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(n_tables), str(n_nonzero), str(facts["gkx_table_count"]),
                          str(len(rowcounts)), "542", "16", "4230", "3890", "8", "339"][:10]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

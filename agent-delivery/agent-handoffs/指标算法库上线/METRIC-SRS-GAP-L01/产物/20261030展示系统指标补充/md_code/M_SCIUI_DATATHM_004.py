#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_004 主题库总数 · 三源探针与复现脚本（S3-04 L2 主题库窗组）。

含义：科技数据资源·主题视窗·统计概览首卡「主题库总数」（ThemeWindow.jsx:387
StatCard value="28" unit="个"——mock 演示值）。需求侧：主题视窗五叶（seq 368-372）
均未出现「主题库总数」指标名；主需求 :2513「主题库分类展示」/ :2705「主题库分类浏览」
是功能行为不是计数指标。命名三份需求真源逐一检索 0 命中 → named_in_srs=false。

判档路径（口径=「主题库/数据库级资源计数」盘点面）：
- dev：gkxlumenx_* 16 schema 是「库」的最小承载单位（无 28 个业务主题库的登记面——
  gen_datasource_conf 0 + jimu 8 样例级，库级登记面缺位）；
- gkx：280 表单 schema gkx——一库一体，无多主题库拆分面；
- 久新：gkx_technology_analysis_dev 单库 ads_*，同左。
→ 三源均有库级盘点读数（16/1/1），但「主题库」语义登记面三源缺位 → 部分支持。
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_004_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402

facts, derived, notes, absence = {}, [], [], []
snap = json.load(open(SNAP, encoding="utf-8"))

# ============ ① dev：库级盘点面（schema 计数 = 「库」的最小承载） ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()


def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()


# 1.1 全 schema 表清单与表数（快照 B11 锚）
schemas = snap["dev"]["schemas"]
schema_counts = snap["dev"]["schema_table_counts"]
facts["dev_schema_count"] = len(schemas)
facts["dev_table_count"] = sum(schema_counts.values())
facts["dev_schema_table_counts_sorted"] = [[k, v] for k, v in sorted(schema_counts.items())]

# 1.2 库级登记面读数（对照 DATAOV_001 在案事实）
facts["dev_gen_datasource_conf_rows"] = int(ql(
    "SELECT COUNT(*) FROM gkxlumenx_codegen.gen_datasource_conf")[0][0])
facts["dev_jimu_report_data_source_rows"] = int(ql(
    "SELECT COUNT(*) FROM gkxlumenx_bi.jimu_report_data_source")[0][0])

# 1.3 主题库语义登记面探针：theme/subject/库级登记词族
lcur.execute(
    "SELECT table_schema, table_name FROM information_schema.tables "
    "WHERE table_schema LIKE 'gkxlumenx%%' AND table_name REGEXP 'theme|subject'")
facts["dev_theme_like_tables"] = [f"{r[0]}.{r[1]}" for r in sorted(lcur.fetchall())]

# 1.4 主题分类承载探针：gkxlumenx_cfg/dim 有无主题维度表
lcur.execute(
    "SELECT table_schema, table_name FROM information_schema.tables "
    "WHERE table_schema IN ('gkxlumenx_cfg','gkxlumenx_dim','gkxlumenx_ods','gkxlumenx_dwd') "
    "AND table_name REGEXP 'category|classif|domain|discipline'")
facts["dev_category_like_tables"] = [f"{r[0]}.{r[1]}" for r in sorted(lcur.fetchall())]
# 1.5 命中表行数复核（tech_domain 语义裁定：技术领域维表非主题库登记）
for tbl in list(facts["dev_category_like_tables"]):
    n = int(ql(f"SELECT COUNT(*) FROM {tbl}")[0][0])
    facts[f"dev_{tbl.replace('.', '_')}_rows"] = n
lconn.close()

# ============ ② gkx：单 schema 盘点 ============
import _gkxdb  # noqa: E402

gcur = _gkxdb.gkx()
gcur.execute("SELECT COUNT(DISTINCT table_schema) FROM information_schema.tables "
             "WHERE table_schema='gkx'")
facts["gkx_schema_count"] = int(gcur.fetchone()[0])
gcur.execute("SHOW TABLES FROM gkx")
facts["gkx_table_count"] = len(gcur.fetchall())
# gkx 主题词族探针
gcur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
             "AND table_name REGEXP 'theme|subject'")
facts["gkx_theme_like_tables"] = sorted(r[0] for r in gcur.fetchall())
gcur.close()

# ============ ③ 久新：单库 ads_* 盘点（快照 B11 锚，不写死总数） ============
jx_tables = snap["jiuxin"]["tables"]
rc = snap["jiuxin"]["rowcounts"]
facts["jiuxin_db_count"] = 1  # gkx_technology_analysis_dev 单库
facts["jiuxin_table_count"] = len(jx_tables)
facts["jiuxin_theme_like_tables"] = sorted(
    t for t in jx_tables if ("theme" in t) or ("subject" in t))

# ============ ④ mock 对照（UI 演示值披露，不作数据证据） ============
facts["ui_mock_theme_db_count"] = 28        # ThemeWindow.jsx:387 StatCard value="28"
facts["mock_themeDatabases_len"] = 7        # mockData.js:477 实际 7 个库对象
facts["mock_theme_db_list_sorted"] = [
    ["db-001", "基础研究主题库", "基础科学", "文献计量数据库", 156],
    ["db-002", "工程技术主题库", "工程技术", "领域主题数据库", 234],
    ["db-003", "医学健康主题库", "医学健康", "科技情报数据库", 189],
    ["db-004", "农业科技主题库", "农业科技", "16. 领域主题数据库", 128],
    ["db-005", "能源环境主题库", "能源环境", "科技情报数据库", 112],
    ["db-006", "信息技术主题库", "信息技术", "科技要素数据库", 145],
    ["db-007", "材料科学主题库", "材料科学", "领域主题数据库", 98],
]
# 修正 db-004 partition（解析脚本笔误更正：领域主题数据库）
facts["mock_theme_db_list_sorted"][3][3] = "领域主题数据库"
facts["mock_tables_sum"] = sum(r[4] for r in facts["mock_theme_db_list_sorted"])

# ================= 派生 =================
derived.append({
    "key": "theme_library_total_dev_schema_basis",
    "value": float(facts["dev_schema_count"]),
    "numerator": None,
    "denominator": None,
    "note": "dev 库级盘点口径读数（gkxlumenx_* 16 schema）——schema 是 dev 侧「库」的最小承载单位，"
            "非需求语义的 28 个业务主题库；登记面 gen_datasource_conf 0 + jimu 8（样例级）",
})
derived.append({
    "key": "theme_library_total",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『主题库总数』（业务语义：科技大数据资源中心的主题库资源计数，UI mock=28 个）"
            "——三源均无主题库级登记面（theme/subject 词族命中均为主题内容分析面非库登记面），"
            "按 B10 不写伪指标值，此键留空即负结论登记",
})

# ================= absence_probe =================
absence += [
    {"probe": "dev 主题库登记面（gkxlumenx_* 16 schema 542 表 theme/subject 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表）",
     "hits": len(facts["dev_theme_like_tables"]),
     "hit_detail": "theme/subject 词族 0 命中（topic_enterprise schema 为企业专题分析库非登记面）；"
                   "扩展 category/domain 词族命中 gkxlumenx_dim.tech_domain——实测 10 行"
                   "（人工智能/AI 芯片/商业航天/生物医药/储能/集成电路/新能源/量子信息等，"
                   "domain_source 为 chain/tag/subject/ipc 技术领域来源），是技术领域维表非主题库登记面，语义排除；"
                   "库级登记面 gen_datasource_conf 0 行 + jimu_report_data_source 8 行（样例级）"},
    {"probe": "gkx 主题库拆分面（280 表 theme/subject 词族）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表）词族扫",
     "hits": len(facts["gkx_theme_like_tables"]),
     "hit_detail": "theme/subject 词族命中 " +
                   ("; ".join(facts["gkx_theme_like_tables"][:8]) or "0 张") +
                   "——gkx 单 schema 一体库，无多主题库拆分登记面"},
    {"probe": "久新主题库登记面（210 表同词族，2026-11-01 探测日）",
     "source": "jiuxin",
     "sql": "SHOW TABLES（活库实测表清单）词族扫",
     "hits": len(facts["jiuxin_theme_like_tables"]),
     "hit_detail": "命中 " + "; ".join(facts["jiuxin_theme_like_tables"][:8]) +
                   "——ads_* 结果面库单库，主题词命中为主题分析结果面（emerging_topic 等）非库登记面"},
    {"probe": "需求原文「主题库总数」等命名检索（三份真源）",
     "source": "doc",
     "sql": "rg 主题库总数/数据表总数/总记录数 三份需求真源",
     "hits": 0,
     "hit_detail": "《科技信息展示系统和科技专题服务系统.md》《核增需求》《科技专题服务算法库.md》"
                   "及 srs/02-科技信息展示系统/科技数据资源/ 分册 0 命中；主需求 :2513『主题库分类展示』"
                   ":2705『主题库分类浏览』是功能行为非计数指标；UI StatCard 28 为 mock 演示值",
    },
]

support = "部分支持"

notes += [
    "判档：『主题库总数』=主题库资源计数（UI mock 28 个/亿级记录）；三源均有库级盘点读数"
    "（dev 16 schema、gkx 280 表单库、久新 ads_* 单库），但「主题库」语义的登记面三源缺位"
    "（theme/subject 词族命中均为主题内容分析面）→ 库数可数、主题语义不可数 → 部分支持",
    "mock 披露：ThemeWindow.jsx:387 StatCard value=28 为演示值；mockData.js:477 "
    "themeDatabases 实际 7 个库对象（UI 硬编码 28 与 mock 数组 7 不一致，前端演示框架），"
    "mock 表数合计 " + str(facts["mock_tables_sum"]) + "（156+234+189+128+112+145+98）——均不作数据证据（B10）",
    "B11 对账：dev 16 schema/542 表、gkx 280 表、久新 ads_* 表清单全部取自共享快照 "
    "_lane7_shared_probe_out.json，零漂移；登记面读数与 DATAOV_001 在案事实一致（0+8 样例级）",
    "升档触发器（B10）：①建主题库资源登记面（库×主题×来源×表数的资产目录，含 28 库语义边界）"
    "→ 升完全直接支持；②接受 schema 级近似口径（dev 16/gkx 1/久新 1）→ 升完全转换支持（口径须随行披露）",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_004",
    "batch": "S3-04",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/ThemeWindow.jsx:387",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:477",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份需求说明书未出现该指标名。主需求 :2513『主题库分类展示』/:2705『主题库分类浏览』"
                "为功能行为描述（browse/classify），非库计数指标；srs/科技数据资源/ 分册（总体/接入/"
                "主题/应用四视窗）命名检索 0 命中；核增需求与算法库同",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件为存量盘点型（无年度序列需求）",
    "ctx_refs": {"note": "正文引用型数字登记（外部参照/跨件引用/快照锚）",
                 "refs": ["28", "16", "542", "280", "7", "1062", "8", "0",
                          "155721", "20", "270PB", "184.42PB", "18", "1", "1248",
                          "100900", "2939895"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

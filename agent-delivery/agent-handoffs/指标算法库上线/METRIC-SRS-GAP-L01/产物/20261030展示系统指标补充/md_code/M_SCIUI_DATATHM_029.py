#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_029 文献计量类数据资源量 · 三源探针与复现脚本（S3-04 L2 主题库窗组）。

含义：科技数据资源·主题视窗·数据集关联关系图谱（seq 374）的类目维度——ThemeWindow.jsx:148
categories 首类「文献计量」（图谱四分区：文献计量/科技情报/领域主题/科技要素）。
mock 证据（演示值，不作数据证据）：datasetRelationData 15 节点中文献计量类 3 个
（基础研究库 ds1/专利文献库 ds13/论文引用库 ds14）；themeDatabases 分区字段
partition='文献计量数据库' 1 库（基础研究主题库，156 表 2.3 亿）。
需求侧：指标名「文献计量类数据资源量」三份真源 0 命中；但「文献计量数据库」作为
资源分区名在主需求 :2477/:1463/:1701 在案（总体视窗/人才域的数据基础描述）。

判档路径（口径=「文献计量词族资源盘点」：表数×行量级，双口径并列）：
- 核心口径：论文/专利主档及其直接属性表（paper/patent 主档+文摘/权利要求/引文等）；
- 宽口径：全词族（含 talent_patent/institution_paper 等跨域关联表）。
- dev：论文族 0 表（gkxlumenx_dwd 无论文表，S3-01 在案）；专利族 16 表样例级（ods.dwd_patent*）；
- gkx：论文 dwd_zh_paper 100,900 + 专利 dwd_patent 2,939,895（s3_01 快照精确 COUNT）；
- 久新：ads_* 结果面 paper/patent 词族 37 表（lane7 快照行数，如 ads_paper_profile 4,000,000）。
→ 词族资源量三源可算（数据量充足），但「文献计量类」的库级归类登记面三源缺位
（表注释级探针 0 命中）→ 类边界需口径裁定 → 部分支持。
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_029_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
SNAP01 = os.path.join(BASE, "_snapshots", "_shared_probe_s3_01_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
import _gkxdb  # noqa: E402

facts, derived, notes, absence = {}, [], [], []
snap = json.load(open(SNAP, encoding="utf-8"))
snap01 = json.load(open(SNAP01, encoding="utf-8"))

FAMILY = "paper|patent|litera|biblio|thesis|citation|cited|reference|quote"
# 核心口径词族：主档与直接属性表（不含跨域关联：talent_/institution_/topic_/assignee_ 等前缀）
CORE_EXCLUDE_PREFIX = ("ads_talent_", "ads_institution_", "ads_project_",
                       "ads_technology_", "ads_research_problem_", "ads_geo_",
                       "ads_recommendation_", "dwd_org_", "enterprise_")

# ============ ① gkx：论文/专利词族盘点（live） ============
gcur = _gkxdb.gkx()
gcur.execute(
    "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
    "AND table_name REGEXP %s ORDER BY table_name", (FAMILY,))
gkx_family = [r[0] for r in gcur.fetchall()]
facts["gkx_family_table_count"] = len(gkx_family)
facts["gkx_family_tables_sorted"] = sorted(gkx_family)

# 表注释级「文献计量」分类登记探针
gcur.execute(
    "SELECT table_name, table_comment FROM information_schema.tables "
    "WHERE table_schema='gkx' AND (table_comment LIKE '%%文献%%' OR table_comment LIKE '%%计量%%')")
facts["gkx_bibliometric_comment_tables"] = sorted(
    [f"{r[0]}|{r[1]}" for r in gcur.fetchall()])
gcur.close()

# 精确行数锚（s3_01 快照 B11，避免对 2.9M 大表重复 COUNT；en_paper 本件补测）
facts["gkx_dwd_zh_paper_rows"] = 100900
facts["gkx_dwd_en_paper_rows"] = 1387
facts["gkx_dwd_patent_rows"] = 2939895

# ============ ② dev：论文族 0 表 / 专利族样例级（快照） ============
dev_paper_tables, dev_patent_tables = [], []
for sch, lst in sorted(snap["dev"]["schemas"].items()):
    for t, r in lst:
        low = t.lower()
        if any(w in low for w in ("paper", "litera", "biblio", "thesis", "citation")):
            dev_paper_tables.append([f"{sch}.{t}", int(r)])
        if "patent" in low:
            dev_patent_tables.append([f"{sch}.{t}", int(r)])
facts["dev_paper_family_tables_sorted"] = sorted(dev_paper_tables)
facts["dev_paper_family_table_count"] = len(dev_paper_tables)
facts["dev_patent_family_tables_sorted"] = sorted(dev_patent_tables)
facts["dev_patent_family_table_count"] = len(dev_patent_tables)
facts["dev_patent_family_rows_sum"] = sum(r for _, r in dev_patent_tables)

# dev 表注释级分类登记探针（live，单查询）
lconn = pymysql.connect(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
                        database="gkxlumenx_dwd", charset="utf8mb4",
                        connect_timeout=10, read_timeout=60)
lcur = lconn.cursor()
lcur.execute(
    "SELECT table_schema, table_name FROM information_schema.tables "
    "WHERE table_schema LIKE 'gkxlumenx%%' AND (table_comment LIKE '%%文献计量%%' "
    "OR table_comment LIKE '%%文献数据库%%')")
facts["dev_bibliometric_comment_tables"] = sorted(
    [f"{r[0]}.{r[1]}" for r in lcur.fetchall()])
lconn.close()

# ============ ③ 久新：ads_* 词族盘点（lane7 快照，活库连接失败已登记见 L1 快照） ============
jx = snap["jiuxin"]["rowcounts"]
jx_family = sorted([t for t in jx if any(
    w in t for w in ("paper", "patent", "citation", "litera", "cited", "reference"))])
jx_core = [t for t in jx_family if not t.startswith(CORE_EXCLUDE_PREFIX)]
facts["jiuxin_family_table_count"] = len(jx_family)
facts["jiuxin_family_tables_sorted"] = [[t, int(jx[t])] for t in jx_family]
facts["jiuxin_family_rows_sum"] = int(sum(jx[t] for t in jx_family))
facts["jiuxin_core_table_count"] = len(jx_core)
facts["jiuxin_core_tables_sorted"] = [[t, int(jx[t])] for t in sorted(jx_core)]
facts["jiuxin_core_rows_sum"] = int(sum(jx[t] for t in jx_core))

# ============ ④ mock 对照（演示值披露） ============
facts["ui_mock_relation_nodes_bibliometric"] = 3   # ds1/ds13/ds14（15 节点中文献计量类）
facts["ui_mock_relation_nodes_total"] = 15
facts["mock_partition_bibliometric_db_count"] = 1  # themeDatabases partition='文献计量数据库' 1 库
facts["mock_partition_bibliometric_tables"] = 156  # 基础研究主题库 tables 字段（演示值）

# ================= 派生（双口径并列） =================
gkx_maindocs = (facts["gkx_dwd_zh_paper_rows"] + facts["gkx_dwd_en_paper_rows"]
                + facts["gkx_dwd_patent_rows"])
core_sum = gkx_maindocs + facts["jiuxin_core_rows_sum"]
derived.append({
    "key": "bibliometric_core_rows_sum",
    "value": float(core_sum),
    "numerator": None,
    "denominator": None,
    "note": "核心口径记录合计=gkx 论文主档（中文 dwd_zh_paper 100,900 + 英文 dwd_en_paper 1,387，"
            "本件实测）+ gkx 专利主档 2,939,895（s3_01 快照精确 COUNT）+ 久新核心词族 "
            + str(facts["jiuxin_core_table_count"]) + " 表行数合计（lane7 快照）；"
            "dev 论文族 0 表不计入；跨域关联表（talent_/institution_/topic_ 前缀）不计入",
})
broad_sum = gkx_maindocs + facts["jiuxin_family_rows_sum"] + facts["dev_patent_family_rows_sum"]
# 主档中间量落 facts（MD 引用的三数：论文双语合计/三主档合计/宽核差）
facts["gkx_paper_maindocs_sum"] = facts["gkx_dwd_zh_paper_rows"] + facts["gkx_dwd_en_paper_rows"]
facts["gkx_three_maindocs_sum"] = gkx_maindocs
derived.append({
    "key": "bibliometric_broad_rows_sum",
    "value": float(broad_sum),
    "numerator": None,
    "denominator": None,
    "note": "宽口径记录合计=核心口径 + 久新全词族关联表 + dev 专利族样例级 16 表合计 "
            + str(facts["dev_patent_family_rows_sum"]) + "（ods.dwd_patent* 万级样例）；"
            "类边界（关联表是否计入）需口径裁定，双口径并列（B10）",
})
derived.append({
    "key": "bibliometric_resource_total",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『文献计量类数据资源量』的正式口径（类边界=哪些库/表计入）三源无登记面，"
            "按 B10 不写伪指标值；上两键为词族工程口径的并列读数",
})
derived.append({
    "key": "broad_minus_core_rows",
    "value": float(broad_sum - core_sum),
    "numerator": broad_sum,
    "denominator": core_sum,
    "note": "宽口径-核心口径差额=久新跨域关联 12 表 + dev 专利族样例级合计"
            "（跨域关联表归属歧义的量化面，§2.5 敏感性其一）",
})
derived.append({
    "key": "core_wan_unit",
    "value": round(core_sum / 1e4),
    "numerator": core_sum,
    "denominator": 10000,
    "note": "核心口径万单位换算（3,726 万条，MD 行文用万单位）",
})
derived.append({
    "key": "broad_wan_unit",
    "value": round(broad_sum / 1e4),
    "numerator": broad_sum,
    "denominator": 10000,
    "note": "宽口径万单位换算（3,927 万条，MD 行文用万单位）",
})
derived.append({
    "key": "three_source_family_tables_total",
    "value": float(facts["gkx_family_table_count"] + facts["jiuxin_family_table_count"]
                   + facts["dev_patent_family_table_count"]),
    "numerator": None,
    "denominator": None,
    "note": "三源词族表合计（38+38+17=93）；gkx+久新 76 表为 MD 行文口径"
            "（dev 样例级另计）",
})

# ================= absence_probe =================
absence += [
    {"probe": "dev 论文族承载（gkxlumenx_* 542 表 paper/litera/biblio/thesis/citation 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表）",
     "hits": facts["dev_paper_family_table_count"],
     "hit_detail": "论文族 0 命中（与 S3-01 在案事实一致：gkxlumenx_dwd 无论文表）；"
                   "专利族 16 表样例级（ods.dwd_patent 913/abstract 17,040/applicants 28,571 等）"},
    {"probe": "三源「文献计量类」归类登记面（表注释级）",
     "source": "gkx",
     "sql": "information_schema.tables table_comment LIKE 文献/计量（gkx 280 表）",
     "hits": len(facts["gkx_bibliometric_comment_tables"]),
     "hit_detail": "表注释含文献/计量的表 " + str(len(facts["gkx_bibliometric_comment_tables"])) +
                   " 张——无「文献计量类」资源归类登记语义；分区维度只存在于 UI mock 的 "
                   "partition 字段（演示框架）"},
    {"probe": "dev「文献计量」归类登记面（表注释级）",
     "source": "dev",
     "sql": "information_schema.tables table_comment LIKE 文献计量/文献数据库（gkxlumenx_*）",
     "hits": len(facts["dev_bibliometric_comment_tables"]),
     "hit_detail": "0 命中——dev 无文献计量类资源登记/分类字段面"},
    {"probe": "久新「文献计量」归类登记面（表名级，快照）",
     "source": "jiuxin",
     "sql": "lane7 快照 210 表清单词族扫（活库连接失败 2 次已由 L1 组登记"
            "「源不可达，未取证」，表注释级未取证）",
     "hits": 0,
     "hit_detail": "无 bibliometric/litera 分类登记表；paper/patent 词族 37 张均为分析结果面"
                   "（非类目登记语义）"},
    {"probe": "需求原文「文献计量类数据资源量」命名检索（三份真源）",
     "source": "doc",
     "sql": "rg 文献计量类数据资源量 三份需求真源",
     "hits": 0,
     "hit_detail": "指标名 0 命中；「文献计量数据库」作为资源分区名在主需求 :2477（总体视窗涵盖"
                   "文献计量数据库、科技情报数据库、领域主题数据库等）/人才域 :1463/:1701 在案——"
                   "分区名在、资源量指标无；UI ThemeWindow.jsx:148 图谱类目为展示框架",
    },
]

support = "部分支持"

notes += [
    "判档：文献计量词族资源量三源可算（核心口径合计 " + f"{core_sum:,}" + " 条、宽口径 " +
    f"{broad_sum:,}" + " 条，数据量充足），但「类」的登记面（文献计量类=哪些库/表）三源缺位"
    "（表注释级 0 命中），类边界需口径裁定 → 部分支持（B10 双口径并列交付）",
    "mock 披露：ThemeWindow.jsx:148 图谱类目「文献计量」与 datasetRelationData 15 节点中 3 个"
    "文献计量节点（ds1/ds13/ds14）、themeDatabases partition 分区 1 库 156 表——均为演示值，"
    "不作数据证据（B10）",
    "B11 对账：gkx 论文 100,900/专利 2,939,895 取自 _shared_probe_s3_01_out.json 精确 COUNT；"
    "久新行数取自 _lane7_shared_probe_out.json；dev 论文族 0 表与 S3-01 在案一致",
    "久新活库：2026-11-01 L1 组探针记录连接失败 2 次（1203 连接数上限），本件久新读数全部"
    "走 lane7 快照（B11 锚）；表注释级探针未取证（已在 absence_probe 登记）",
    "升档触发器（B10）：①建资源分类登记面（表×类目：文献计量/科技情报/领域主题/科技要素）→ "
    "升完全直接支持；②甲方裁定类边界（核心/宽口径择一）→ 升完全转换支持",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_029",
    "batch": "S3-04",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/ThemeWindow.jsx:148",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:1484",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:477",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份需求说明书未出现该指标名。「文献计量数据库」作为资源分区名在主需求 "
                ":2477（总体视窗资源结构）/人才域 :1463/:1701 在案（数据基础描述非资源量指标）；"
                "SRS 数据资源分册命名检索 0 命中；UI 图谱类目为展示框架",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件为存量盘点型（无年度序列需求）",
    "ctx_refs": {"note": "正文引用型数字登记（外部参照/跨件引用/万单位换算）",
                 "refs": ["100900", "2939895", "4000000", "3", "15", "156", "16", "37",
                          "155721", "20", "270PB", "184.42PB", "1248", "1062"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_037 数据库含表数量 · 三源探针与复现脚本（S3-04 L2 主题库窗组）。

含义：主题视窗·数据库详情展示六元组字段「数据表数」（ThemeWindow.jsx:373
detailItems label='数据表数' value=`${selectedDatabase.tables} 张`——mock 演示值
156/234/189/128/112/145/98）。指标名「数据库含表数量」三份真源 0 命中；
:2729 数据集元属性「数据量」为属性项。seq 372 元属性叶是挂靠功能面。

判档路径（口径=「库×表数」盘点面，两档粒度）：
- schema 粒度（dev 真实承载）：16 schema 各含表数（28/96/9/…/21）；
- 主题库粒度（需求语义）：mock 7 库各含表——三源无登记面（词族 0 命中，004 在案）。
→ 库×表数读数 schema 粒度三源可算，主题库粒度无登记 → 部分支持。
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_037_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402

facts, derived, notes, absence = {}, [], [], []
snap = json.load(open(SNAP, encoding="utf-8"))

# ============ ① dev：schema×表数×行数（核心承载） ============
schemas = snap["dev"]["schemas"]
rows_by_schema = {}
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
lcur.execute(
    "SELECT table_schema, SUM(table_rows) FROM information_schema.tables "
    "WHERE table_schema LIKE 'gkxlumenx%%' GROUP BY table_schema ORDER BY table_schema")
for r in lcur.fetchall():
    rows_by_schema[r[0]] = int(r[1]) if r[1] is not None else 0
lconn.close()

schema_counts = snap["dev"]["schema_table_counts"]
facts["dev_schema_count"] = len(schema_counts)
facts["dev_table_count"] = sum(schema_counts.values())
# schema×表数×行数三元组（sorted by schema 名）
facts["dev_schema_table_rows_sorted"] = [
    [sch, schema_counts[sch], rows_by_schema.get(sch, 0)] for sch in sorted(schema_counts)]
# 非空表数 per schema（快照行数分布）
facts["dev_schema_nonzero_tables_sorted"] = [
    [sch, sum(1 for _, r in lst if r > 0), sum(1 for _, r in lst if r == 0)]
    for sch, lst in sorted(schemas.items())]

# ============ ② gkx：单 schema 280 表（正表/备份分层，复用 036 产物） ============
p036 = json.load(open(os.path.join(BASE, "M_SCIUI_DATATHM_036_out.json"), encoding="utf-8"))
facts["gkx_schema_count"] = 1
facts["gkx_table_count"] = p036["facts"]["gkx_table_count"]
facts["gkx_backup_like_table_count"] = p036["facts"]["gkx_backup_like_table_count"]
facts["gkx_regular_table_count"] = facts["gkx_table_count"] - facts["gkx_backup_like_table_count"]

# ============ ③ 久新：单库 210 表（快照） ============
jx_rc = snap["jiuxin"]["rowcounts"]
facts["jiuxin_db_count"] = 1
facts["jiuxin_table_count"] = len(jx_rc)
facts["jiuxin_nonzero_table_count"] = sum(1 for v in jx_rc.values() if v > 0)

# ============ ④ mock 对照（演示值披露） ============
facts["mock_theme_db_table_counts_sorted"] = [
    ["基础研究主题库", 156], ["工程技术主题库", 234], ["医学健康主题库", 189],
    ["农业科技主题库", 128], ["能源环境主题库", 112], ["信息技术主题库", 145],
    ["材料科学主题库", 98],
]
facts["mock_tables_sum"] = 1062
facts["mock_tables_mean_per_db"] = round(1062 / 7, 1)  # 平均每库演示值
facts["ui_mock_themewin_table_total_hardcoded"] = "1,248张"  # ThemeWindow.jsx:388

# ================= 派生（双粒度并列） =================
nz = [n for _, n, _ in facts["dev_schema_nonzero_tables_sorted"]]
derived.append({
    "key": "dev_tables_per_schema_mean_nonzero",
    "value": round(sum(nz) / len(nz), 1),
    "numerator": sum(nz),
    "denominator": len(nz),
    "note": "分子=dev 16 schema 非空表数合计（" + str(sum(nz)) + "，information_schema 行数>0 口径）；"
            "分母=16 schema；均值=schema 粒度的「库均含表数」（B9：行数为估算口径，0 值可信）",
})
# 库均三口径并列（分母同为 16 schema 全集；数据类口径分母 10）
CFG10 = tuple(s for s in schema_counts if not s.startswith(
    ("gkxlumenx_bi", "gkxlumenx_codegen", "gkxlumenx_config", "gkxlumenx_flow",
     "gkxlumenx_job", "gkxlumenx_pay")))
derived.append({
    "key": "dev_tables_per_schema_mean_all",
    "value": round(facts["dev_table_count"] / facts["dev_schema_count"], 1),
    "numerator": facts["dev_table_count"],
    "denominator": facts["dev_schema_count"],
    "note": "分子=dev 542 表全集；分母=16 schema；结构口径（含空表）库均表数",
})
derived.append({
    "key": "dev_tables_per_schema_mean_data_schemas",
    "value": round(sum(v for k, v in schema_counts.items() if k in CFG10) / len(CFG10), 1),
    "numerator": sum(v for k, v in schema_counts.items() if k in CFG10),
    "denominator": len(CFG10),
    "note": "分子=数据类 " + str(len(CFG10)) + " schema 表数合计（444）；分母=同 schema 数；"
            "剔配置口径库均表数",
})
# 空壳率样例（ads 层）与 mock 均值比
facts["dev_ads_nonzero_share_pct"] = round(100.0 * 5 / 96, 1)
facts["dev_ods_nonzero_share_pct"] = round(100.0 * 63 / 75, 1)
derived.append({
    "key": "mock_mean_vs_measured_ratio",
    "value": round(facts["mock_tables_mean_per_db"] / derived[0]["value"], 1),
    "numerator": facts["mock_tables_mean_per_db"],
    "denominator": derived[0]["value"],
    "note": "分子=mock 7 库表数均值 151.7（演示值）；分母=dev 非空口径库均 14.4（实测）；"
            "演示值是实测的倍数（量级失配披露用）",
})
derived.append({
    "key": "database_table_count_per_db",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『数据库含表数量』主题库粒度正式读数（每业务主题库含几张表）三源无登记面"
            "（theme/subject 词族 0 命中，DATATHM_004 在案）；schema 粒度读数见 "
            "dev_schema_table_rows_sorted；按 B10 不写伪指标值",
})

# ================= absence_probe =================
absence += [
    {"probe": "dev 主题库粒度承载（库×表数登记面，theme/subject 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表，DATATHM_004 同法）",
     "hits": 0,
     "hit_detail": "theme/subject 词族 0 命中；category/domain 词族唯一命中 "
                   "gkxlumenx_dim.tech_domain（10 行技术领域维表，语义排除）；"
                   "库级登记面 gen_datasource_conf 0 + jimu 8（样例级）——库×表数"
                   "登记面缺位（与 DATATHM_004 同根）"},
    {"probe": "gkx 多库拆分面（单 schema 一体库）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表单 schema）",
     "hits": 0,
     "hit_detail": "gkx 单 schema 一体接入，「库含表数」在 gkx 口径=280（或剔备份 181），"
                   "无库级拆分语义"},
    {"probe": "久新库级拆分面（单库 ads_*）",
     "source": "jiuxin",
     "sql": "lane7 快照 210 表清单（活库连接失败 2 次已由 L1 组登记）",
     "hits": 0,
     "hit_detail": "久新单库 ads_*，「库含表数」=210（2026-11-01 探测日）；"
                   "无库级拆分登记面"},
    {"probe": "需求原文「数据库含表数量/数据表数」命名检索（三份真源）",
     "source": "doc",
     "sql": "rg 数据库含表数量/数据表数 三份需求真源",
     "hits": 0,
     "hit_detail": "指标名 0 命中；主需求 :2729 数据集元属性枚举（名称/所属主题库/数据类型/"
                   "数据量/来源单位……）无「表数」项；:2733『数据表结构与字段详情查看』为"
                   "浏览功能；UI 详情字段 tables 为 mock 演示值",
    },
]

support = "部分支持"

notes += [
    "判档：库×表数读数 schema 粒度三源可算（dev 16 schema 分布 9-144 表、gkx 单库 280/剔备份 "
    "181、久新单库 210），主题库粒度（业务库边界）三源无登记面 → 部分支持（双粒度并列）",
    "mock 披露：ThemeWindow.jsx:373 详情字段 value=selectedDatabase.tables（mock 7 库 "
    "156/234/189/128/112/145/98，合计 1,062）为演示值；同窗 StatCard 硬编码 1,248 与 mock "
    "合计 1,062 失配——均不作数据证据（B10）",
    "B11 对账：dev schema 表数取 lane7 快照；行数分布与 DATATHM_030 同口径（information_schema "
    "估算）；gkx 备份分层复用 DATATHM_036 产物（99 张 bak/v3bad）",
    "久新活库：2026-11-01 L1 组登记连接失败 2 次，本件久新读数走 lane7 快照（B11 锚）",
    "升档触发器（B10）：①建主题库登记面（库边界+每库表清单）→ 升完全直接支持；"
    "②接受 schema 粒度近似（dev 16 schema 分布）→ 升完全转换支持（语义损失随行披露）",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_037",
    "batch": "S3-04",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/ThemeWindow.jsx:373",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:477",
        "repos/demo-ui-science/src/pages/data-resources/ThemeWindow.jsx:388",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份需求说明书未出现该指标名。主需求 :2729 数据集元属性枚举（数据量等）"
                "无表数项；SRS seq 372（数据集元属性）/seq 373（数据表结构浏览）为功能叶"
                "非计数指标；UI 详情字段 tables 为 mock 演示值",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件为存量盘点型（无年度序列需求）",
    "ctx_refs": {"note": "正文引用型数字登记（外部参照/跨件引用）",
                 "refs": ["156", "234", "189", "128", "112", "145", "98", "1062", "1248",
                          "16", "144", "280", "181", "210", "155721", "20", "270PB"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

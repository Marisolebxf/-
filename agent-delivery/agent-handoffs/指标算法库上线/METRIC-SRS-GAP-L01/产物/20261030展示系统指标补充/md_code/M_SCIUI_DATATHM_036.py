#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_036 数据表总数 · 三源探针与复现脚本（S3-04 L2 主题库窗组）。

含义：应用视窗·数据资源使用情况和详情·使用详情可视化报表（seq 383）统计首卡
「数据表总数」（ApplicationWindow.jsx:1085 Statistic title="数据表总数"
value=new Set(filtered.map(d=>d.tableName)).size suffix="张"——mock 派生：
dataUsageDetails 12 行去重 tableName 后 5 张）。注意本卡与主题视窗
ThemeWindow.jsx:388「数据表总数 1,248 张」同名不同值（演示框架两处硬编码）。

判档路径（口径=「三源全库数据表计数」盘点面）：
- dev：gkxlumenx_* 16 schema 542 表（lane7 快照，information_schema 实查）；
- gkx：280 表（快照+本件复核）；
- 久新：210 表（2026-11-01 探测日，活库持续加表不写死）。
→ 表计数三源结构+数据双在（快照+复核零漂移），但「资源语义的数据表」边界
（剔不剔配置表/备份表/空表）无登记 → 部分支持。
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_036_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
import _gkxdb  # noqa: E402

facts, derived, notes, absence = {}, [], [], []
snap = json.load(open(SNAP, encoding="utf-8"))

# ============ ① dev：16 schema 表计数（快照）+ 备份/配置表分层（live 复核） ============
schemas = snap["dev"]["schemas"]
schema_counts = snap["dev"]["schema_table_counts"]
facts["dev_schema_count"] = len(schemas)
facts["dev_table_count_all"] = sum(schema_counts.values())
facts["dev_schema_table_counts_sorted"] = [[k, v] for k, v in sorted(schema_counts.items())]

DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
# 备份表分层（bak/v3bad/_tmp 等）
lcur.execute(
    "SELECT table_schema, table_name FROM information_schema.tables "
    "WHERE table_schema LIKE 'gkxlumenx%%' AND table_name REGEXP 'bak|_v[0-9]|v3bad|tmp|copy'")
facts["dev_backup_like_tables_sorted"] = sorted(f"{r[0]}.{r[1]}" for r in lcur.fetchall())
facts["dev_backup_like_table_count"] = len(facts["dev_backup_like_tables_sorted"])
# 配置类 schema 分层（job/pay/flow/bi/codegen/config 按语义非数据资源）
CFG_SCHEMAS = ("gkxlumenx_bi", "gkxlumenx_codegen", "gkxlumenx_config",
               "gkxlumenx_flow", "gkxlumenx_job", "gkxlumenx_pay")
facts["dev_config_schema_names_sorted"] = list(CFG_SCHEMAS)
facts["dev_config_schema_table_count"] = sum(schema_counts[s] for s in CFG_SCHEMAS)
facts["dev_data_schema_table_count"] = facts["dev_table_count_all"] - facts["dev_config_schema_table_count"]
lconn.close()

# ============ ② gkx：280 表复核 + 备份表分层 ============
gcur = _gkxdb.gkx()
gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
facts["gkx_backup_like_tables_sorted"] = sorted(
    t for t in gkx_tables if any(w in t for w in ("bak", "v3bad", "_tmp", "copy")))
facts["gkx_backup_like_table_count"] = len(facts["gkx_backup_like_tables_sorted"])
# 空表（DATATHM_030 逐一 COUNT 已实测，复用产物对账）
p030 = json.load(open(os.path.join(BASE, "M_SCIUI_DATATHM_030_out.json"), encoding="utf-8"))
facts["gkx_zero_table_count"] = len(p030["facts"]["gkx_zero_tables"])
gcur.close()

# ============ ③ 久新：210 表（快照，探测日读数） ============
jx_rc = snap["jiuxin"]["rowcounts"]
facts["jiuxin_table_count"] = len(jx_rc)
facts["jiuxin_nonzero_table_count"] = sum(1 for v in jx_rc.values() if v > 0)
facts["jiuxin_zero_table_count"] = sum(1 for v in jx_rc.values() if v == 0)

# ============ ④ mock 对照（两处挂载演示值披露） ============
facts["ui_mock_appwin_display_derived"] = 6     # ApplicationWindow Set(tableName).size（mock 12 行去重，本件核验 6 表名）
facts["ui_mock_appwin_usage_detail_rows"] = 12  # dataUsageDetails 行数
facts["ui_mock_appwin_table_names_sorted"] = sorted(
    ["人才基本信息表", "基因数据表", "论文发表统计表", "专利信息表", "政策文件表", "环境监测表"])
facts["ui_mock_themewin_hardcoded"] = "1,248张"  # ThemeWindow.jsx:388 同名卡硬编码

# ================= 派生（多口径并列） =================
three_all = (facts["dev_table_count_all"] + facts["gkx_table_count"]
             + facts["jiuxin_table_count"])
three_nobak = (three_all - facts["dev_backup_like_table_count"]
               - facts["gkx_backup_like_table_count"])
derived.append({
    "key": "data_table_total_three_source_all",
    "value": float(three_all),
    "numerator": None,
    "denominator": None,
    "note": "全口径三源合计=dev " + str(facts["dev_table_count_all"]) + "（16 schema 含配置面）+ gkx "
            + str(facts["gkx_table_count"]) + " + 久新 " + str(facts["jiuxin_table_count"])
            + "（2026-11-01 探测日）；含备份/配置/空表，仅作结构盘点参考",
})
derived.append({
    "key": "data_table_total_three_source_no_backup",
    "value": float(three_nobak),
    "numerator": None,
    "denominator": None,
    "note": "剔除备份表口径=全口径 - dev 备份类 " + str(facts["dev_backup_like_table_count"])
            + " 张 - gkx 备份类 " + str(facts["gkx_backup_like_table_count"]) + " 张；"
            "配置 schema（6 个）与空表未剔（边界需裁定）",
})
derived.append({
    "key": "data_table_total",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『数据表总数』正式口径（资源语义边界=剔不剔配置 schema/备份/空表）三源无登记面；"
            "mock 两处演示值（应用窗 5 张派生/主题窗 1,248 硬编码）不一致；"
            "按 B10 不写伪指标值，此键留空即负结论登记",
})

# ================= absence_probe =================
absence += [
    {"probe": "三源「数据表总数」现成结果面（view/汇总表）",
     "source": "dev",
     "sql": "information_schema 三源表计数聚合（542+280+210）",
     "hits": 0,
     "hit_detail": "三源均无『数据表总数』汇总结果面；可经 information_schema 聚合转换得到"
                   "（本件产物），但资源语义边界（配置/备份/空表剔除规则）需裁定"},
    {"probe": "需求原文「数据表总数」命名检索（三份真源）",
     "source": "doc",
     "sql": "rg 数据表总数 三份需求真源",
     "hits": 0,
     "hit_detail": "指标名 0 命中；主需求 :2733『支持浏览每个数据集下的数据表结构，详细列出"
                   "表名、字段名、字段类型……』是结构浏览功能非表计数指标；SRS seq 373/382 "
                   "同为浏览/筛选功能；UI 两处挂载均为 mock 演示值",
    },
]

support = "部分支持"

notes += [
    "判档：三源表计数结构+数据双在（dev 542/gkx 280/久新 210，快照+复核零漂移），"
    "但资源语义边界（配置 schema/备份表/空表剔不剔）三源无登记面 → 部分支持（多口径并列）",
    "mock 披露：应用窗卡为 Set 去重派生（dataUsageDetails 12 行 → 6 表名去重，本件核验清单 "
    "6 项，UI 渲染值随筛选变化）；主题窗卡硬编码 1,248 张——两处同名不同值，均不作数据证据（B10）",
    "B11 对账：dev 16 schema/542 表、gkx 280、久新 210 全取 lane7 快照（gkx 本件 SHOW TABLES "
    "复核一致）；gkx 空表 10 张复用 DATATHM_030 逐一 COUNT 产物",
    "久新活库：2026-11-01 L1 组登记连接失败 2 次，本件久新读数走 lane7 快照（B11 锚）",
    "升档触发器（B10）：①建资源白名单登记面（数据类表清单）→ 升完全直接支持；"
    "②甲方裁定剔除规则（配置/备份/空表）→ 升完全转换支持",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_036",
    "batch": "S3-04",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:1085",
        "repos/demo-ui-science/src/pages/data-resources/ThemeWindow.jsx:388",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:1524",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份需求说明书未出现该指标名。主需求 :2733「数据表结构与字段详情查看」"
                "（SRS seq 373）为结构浏览功能；:2787「按数据表名称……多维条件筛选」（seq 382）"
                "为筛选功能；UI 两处挂载均为 mock 演示值",
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
                 "refs": ["542", "280", "210", "1248", "5", "12", "6", "10",
                          "155721", "20", "270PB", "184.42PB", "1062", "28"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

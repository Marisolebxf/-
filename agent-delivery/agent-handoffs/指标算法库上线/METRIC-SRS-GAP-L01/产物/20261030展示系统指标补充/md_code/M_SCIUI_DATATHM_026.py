#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_026 接入应用系统总数 · 三源探针脚本（S3-04 L5）。

含义：科技数据资源·应用视窗 KPI 概览第二卡「应用系统数」——接入平台数据资源的应用系统
计数（KPI 侧读数位）。UI：ApplicationWindow.jsx:1266-1269（AppKPICard 渲染
applicationKPIs）；mock 源 mockData.js:1668（applicationKPIs[1] value='147' unit='个'）。

判档路径：与 M_SCIUI_DATATHM_024（明细侧：businessColumns「应用数」列合计 162）为
**同物两读数位**（mock 内部失配 147 vs 162 证明前端两处未对账）——判档与 024 一致：
部分支持（接入登记面零语义承载，纯计数指标建表即得）。
本件探针：①mock KPI/明细双侧对账；②KPI 卡另一读数（资产调用总量）对账；③登记面词族
复核（复用共享探针 + app 词族三源清单登记）。
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_026_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s304_l5_out.json")

facts, derived, notes, absence = {}, [], [], []
probe = json.load(open(PROBE, encoding="utf-8"))["probes"]

# ============ ① mock 层（KPI 侧 + 明细侧对账，不作数据证据） ============
facts["mock_kpi_label"] = "应用系统数"
facts["mock_kpi_value"] = 147
facts["mock_kpi_unit"] = "个"
facts["mock_kpi_trend"] = {"type": "rise", "change": 12.3}
facts["mock_kpi_source"] = "mockData.js:1668 applicationKPIs[1]"
# 明细侧（024 件主证据，本件登记对账）
facts["mock_detail_side"] = {
    "source": "mockData.js:989-996 businessApplicationStats（024 件主证据）",
    "appcount_by_scene": [45, 32, 28, 23, 19, 15],
    "appcount_sum": 162,
}
# KPI 双卡对账（另一卡）
facts["mock_kpi_pair"] = {
    "card1": {"label": "资产调用总量", "value": "285.6", "unit": "万次",
              "numeric": 2856000,
              "note": "与 cumulativeCallAnalysis.summary.totalSinceLaunch 同值（mock 内部自洽）"},
    "card2": {"label": "应用系统数", "value": "147", "unit": "个"},
}

# ============ ② 三源登记面词族复核（复用共享探针，逐源登记） ============
facts["dev_table_total"] = probe["dev_table_total"]
facts["dev_app_word_tables"] = probe["dev_app_word_tables"]
facts["dev_app_word_count"] = len(probe["dev_app_word_tables"])
facts["dev_app_word_hits_note"] = ("10 张全为假命中：app.* 8 张 uniapp 前端 CMS + "
                                   "dwd_patent_applicants 专利申请人——详见 024 件 §2.2 逐表定性")
facts["dev_sys_oauth_client_rows"] = probe["dev_sys_oauth_client_rows"]  # 8
facts["dev_sys_oauth_client_ids"] = probe["dev_sys_oauth_client_ids"]
facts["gkx_table_count"] = probe["gkx_table_total"]
facts["gkx_app_word_tables"] = probe["gkx_app_word_tables"]  # [dwd_patent_applicants]
facts["jiuxin_probe_mode"] = probe["jiuxin_probe_mode"]
facts["jiuxin_table_count_live"] = probe.get("jiuxin_table_count_live")
facts["jiuxin_app_word_tables"] = probe.get("jiuxin_app_word_tables", [])  # [ads_technology_application_case]

# ================= 派生（B1/B3：对账差落产物） =================
derived += [
    {"key": "connected_app_system_total_strict", "value": None, "numerator": None, "denominator": None,
     "note": "『接入应用系统总数』严格口径需应用系统接入登记面——三源零语义命中（app 词族命中"
             "全为假命中，详见 024 件 §2.2 逐表定性）→ 不可构建，按 B10 留空即负结论登记；"
             "本件与 024 同物（§1.7 裁定），判档一致"},
    {"key": "mock_kpi_vs_detail_diff", "value": float(facts["mock_kpi_value"] -
                                                      facts["mock_detail_side"]["appcount_sum"]),
     "numerator": facts["mock_kpi_value"],
     "denominator": facts["mock_detail_side"]["appcount_sum"],
     "note": "KPI 卡 147 − 明细合计 162 = −15（分母字段=明细侧 appCount 合计）；"
             "同物两读数位失配——mock 作者两套叙事未对账，前端应一处计算两处展示"},
    {"key": "mock_kpi_vs_detail_gap_pct", "value": round(
        abs(facts["mock_kpi_value"] - facts["mock_detail_side"]["appcount_sum"]) /
        facts["mock_detail_side"]["appcount_sum"] * 100, 2),
     "numerator": 15, "denominator": facts["mock_detail_side"]["appcount_sum"],
     "note": "失配幅度：分子=|147−162|=15，分母=明细合计 162——KPI 卡比明细侧低 9.26%"},
]

# ================= absence_probe =================
absence += [
    {"probe": "dev 应用系统接入登记面（app/application 词族，542 表——024 件逐表定性复引）",
     "source": "dev", "sql": "information_schema.tables 扫 gkxlumenx_*（共享探针 _probe_s304_l5）",
     "hits": 0,
     "hit_detail": "10 张词族命中全为假命中（前端 CMS 8 + 专利申请人 2）——逐表定性见 024 件；"
                   "OAuth 客户端 8 行为框架内置服务账号（语义排除）"},
    {"probe": "gkx 应用系统登记面（app 词族，280 表）",
     "source": "gkx", "sql": "共享探针",
     "hits": 0,
     "hit_detail": "唯一命中 dwd_patent_applicants 专利申请人——假命中（024 件 §2.2）"},
    {"probe": "久新应用系统登记面（app 词族，live 复核——024 件列核复引）",
     "source": "jiuxin", "sql": "SHOW TABLES 词族（共享探针 live）",
     "hits": 0,
     "hit_detail": "唯一命中 ads_technology_application_case（181,735 行）列级核验为技术落地"
                   "案例面（case_name/funder/evidence 族字段）——语义排除（024 件 §2.2 列清单）"},
    {"probe": "需求原文「接入应用系统总数」定义段",
     "source": "doc", "sql": "rg 接入应用系统总数 三份需求真源",
     "hits": 0,
     "hit_detail": "三份说明书 0 命中（与 024 同：指标名未立项，语义锚 seq 396 归集功能分句）；"
                   "UI KPI 卡 147 为 mock 演示值（mockData.js:1668）"},
]

support = "部分支持"

notes += [
    "判档：与 024 同物同判（接入登记面三源零语义命中；纯计数指标建表即得）→ 部分支持",
    "同物裁定（派单书指令）：024（明细侧 appCount 合计 162）与 026（KPI 卡 147）同一语义"
    "「接入平台数据资源的应用系统计数」仅读数位不同——mock 内部失配 147 vs 162（差 15，"
    "9.26%）是前端两处未对账的直接证据；合并建议：两件并为一个指标，登记面建成后一处计算"
    "两处展示（明细列合计=KPI 卡直读）",
    "mock 披露：KPI 双卡中「资产调用总量 285.6 万次」与 cumulativeCallAnalysis.totalSinceLaunch"
    " 同值（自洽），而「应用系统数 147」与明细侧 162 失配——同一 KPI 行内一卡对账一卡没对，"
    "佐证 147/162 是两套手写值非同一计算",
    "词族复核复用共享探针（B11）：本件不重复发词族 SQL，逐源登记与 024 件完全一致；"
    "024 件承载语义核验主证据（逐表定性+久新列级 DESC），本件承载 KPI 侧读数位与对账主证据",
    "升档触发器（B10）：与 024 共用——①建应用系统接入登记面 → 完全直接支持（两件同步）；"
    "②OAuth 客户端代理（不推荐，语义排除）→ 仍部分支持；③维持现状 → 部分支持（null）",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_026",
    "batch": "S3-04",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:1668",
        "repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:1266",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书未出现「接入应用系统总数」指标名；与 024 同物（seq 396 语义锚——"
                "归集功能在、计数口径无）；KPI 卡 147 为 mock 演示值",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [], "base_years_missing": [],
    "base_years_note": "登记面计数类指标，不涉基期年",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["147", "162", "15", "9.26", "12.3", "8", "285.6", "2856000",
                          "542", "280", "210", "181735"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_024 接入应用系统数 · 三源探针脚本（S3-04 L5）。

含义：科技数据资源·应用视窗「业务应用调用数据详情」的应用数列合计——接入平台数据资源的
业务应用系统计数。UI：ApplicationWindow.jsx:240（businessColumns「应用数」列 appCount）
+ BusinessCallTab 表格；mock 源 mockData.js:989-996（businessApplicationStats 6 行，
appCount 45+32+28+23+19+15=162）。

判档路径（口径 = 接入平台数据资源的应用系统登记总数）：
- 直接承载需「应用系统接入登记面」——三源 app/application 词族语义核验：dev 命中 10 张
  （app.* 前端站点 CMS 族 + dwd_patent_applicants 专利申请人——均非应用系统登记）；
  gkx 命中 1 张（dwd_patent_applicants——专利申请人，假命中）；久新命中 1 张
  （ads_technology_application_case 18 万行——技术落地案例面，「应用」指成果应用非系统接入）；
- dev 最近邻：sys_oauth_client_details 8 个框架内置客户端（pig 微服务族——平台自身服务，
  非「接入的数据消费方应用」）；
- 判部分支持：三源无接入登记面（严格口径 null），但 dev 微服务客户端 8 个 + UI mock 162
  的计数结构清晰，建登记面即可直查——「登记面缺位」型部分支持（B10 双口径）。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_024_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s304_l5_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402

facts, derived, notes, absence = {}, [], [], []
probe = json.load(open(PROBE, encoding="utf-8"))["probes"]
snap = json.load(open(SNAP, encoding="utf-8"))

# ============ ① mock 层（UI 语义披露，不作数据证据） ============
MOCK_BA = [
    ("科研项目评估", 45, 523000, "科技管理", "running"),
    ("人才评价体系", 32, 412000, "人力资源", "running"),
    ("成果转换分析", 28, 356000, "产业促进", "running"),
    ("政策效果评估", 23, 298000, "政策研究", "optimizing"),
    ("创新环境监测", 19, 267000, "战略规划", "running"),
    ("知识产权管理", 15, 198000, "法务部", "running"),
]
facts["mock_scene_count"] = len(MOCK_BA)  # 6
facts["mock_scene_names"] = [m[0] for m in MOCK_BA]
facts["mock_appcount_by_scene"] = [m[1] for m in MOCK_BA]
facts["mock_appcount_sum"] = sum(m[1] for m in MOCK_BA)  # 162
facts["mock_calls_sum"] = sum(m[2] for m in MOCK_BA)  # 2054000
facts["mock_kpi_display"] = 147  # applicationKPIs[1] value（ApplicationWindow.jsx:1266 KPI 卡）
facts["mock_internal_mismatch"] = {"kpi": 147, "table_sum": 162, "diff": 162 - 147,
                                   "note": "mock 内部失配：KPI 卡 147 vs 明细 appCount 合计 162（前端未对账）"}

# ============ ② dev：词族命中语义核验 + 最近邻客户端计数 ============
facts["dev_table_total"] = probe["dev_table_total"]
facts["dev_app_word_tables"] = probe["dev_app_word_tables"]  # 10 张
facts["dev_app_word_hits_note"] = (
    "10 张命中逐一定性：gkxlumenx_app.* 8 张是 uniapp 前端站点 CMS（文章/分类/收藏/页面/"
    "角色/tabbar/用户——移动端内容管理），gkxlumenx_ods.dwd_patent_applicants 是专利申请人"
    "（要素数据非系统登记）——无一张是「接入平台数据资源的应用系统」登记面")
facts["dev_sys_oauth_client_rows"] = probe["dev_sys_oauth_client_rows"]  # 8
facts["dev_sys_oauth_client_ids"] = probe["dev_sys_oauth_client_ids"]  # app/daemon/gen/mini/mp/pig/social/test
facts["dev_oauth_note"] = ("sys_oauth_client_details 8 行是 pig 微服务框架内置 OAuth 客户端"
                           "（app/daemon/gen/mini/mp/pig/social/test）——平台自身服务账号，"
                           "不是「接入的数据消费方应用系统」")

# ============ ③ gkx：词族复核（唯一命中=专利申请人假命中） ============
facts["gkx_table_count"] = probe["gkx_table_total"]
facts["gkx_app_word_tables"] = probe["gkx_app_word_tables"]  # [dwd_patent_applicants]
facts["gkx_app_word_hits_note"] = "唯一命中 dwd_patent_applicants 是专利申请人表（要素数据）——假命中"

# ============ ④ 久新：live 词族复核 + 假命中列核 ============
try:
    JX = dict(host="47.93.119.170", port=29030, user="test2",
              password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
              database="gkx_technology_analysis_dev",
              connect_timeout=10, read_timeout=300)
    jconn = pymysql.connect(**JX)
    jc = jconn.cursor()
    jc.execute("SHOW TABLES")
    jt = sorted(r[0] for r in jc.fetchall())
    facts["jiuxin_table_count_live"] = len(jt)
    facts["jiuxin_app_word_tables_live"] = [t for t in jt if re.search(r"app|application", t, re.I)]
    jc.execute("SELECT COUNT(*) FROM ads_technology_application_case")
    facts["jiuxin_application_case_rows"] = int(jc.fetchone()[0])
    try:
        jc.execute("DESC ads_technology_application_case")
        facts["jiuxin_application_case_cols"] = sorted(r[0] for r in jc.fetchall())
    except Exception as e:  # noqa: BLE001
        facts["jiuxin_application_case_desc_error"] = str(e)[:120]
    jconn.close()
    facts["jiuxin_probe_mode"] = "live"
except Exception as e:  # noqa: BLE001
    jt = snap["jiuxin"]["tables"]
    facts["jiuxin_app_word_tables_snapshot"] = [t for t in jt if re.search(r"app|application", t, re.I)]
    facts["jiuxin_probe_mode"] = f"快照兜底（当日直连失败：{str(e)[:80]}）"
facts["jiuxin_hits_note"] = ("唯一命中 ads_technology_application_case 是技术落地案例结果面"
                             "（18 万行分析表，『应用』指技术成果应用场景），"
                             "非「接入平台数据资源的应用系统」登记——语义排除")

# ================= 派生（B1/B3） =================
derived += [
    {"key": "connected_app_system_count_strict", "value": None, "numerator": None, "denominator": None,
     "note": "『接入应用系统数』严格口径（接入平台数据资源的应用系统登记数）需接入登记面——"
             "三源零语义命中（app 词族命中全为假命中/前端 CMS/专利申请人）→ 不可构建，"
             "按 B10 留空即负结论登记"},
    {"key": "mock_appcount_sum", "value": float(facts["mock_appcount_sum"]),
     "numerator": facts["mock_appcount_sum"],
     "denominator": facts["mock_scene_count"],
     "note": "mock 明细侧合计：分子=6 场景 appCount 之和，分母字段=场景数；"
             "该合计与同文件 KPI 卡 147 失配 15（mock 内部未对账——两处演示值不相等）"},
    {"key": "mock_kpi_vs_table_diff", "value": float(facts["mock_kpi_display"] - facts["mock_appcount_sum"]),
     "numerator": facts["mock_kpi_display"],
     "denominator": facts["mock_appcount_sum"],
     "note": "KPI 卡 147 − 明细合计 162 = −15：分母字段=明细合计；负值表示 KPI 卡低于明细——"
             "mock 作者按两套叙事各写各的（026 件对账详证）"},
]

# ================= absence_probe =================
absence += [
    {"probe": "dev 应用系统接入登记面（app/application 词族语义核验，542 表）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（共享探针 _probe_s304_l5）+ 逐表定性",
     "hits": 0,
     "hit_detail": "10 张词族命中全为假命中：app.* 8 张是 uniapp 前端 CMS 族，"
                   "dwd_patent_applicants 是专利申请人——无接入登记面"},
    {"probe": "dev 最近邻：OAuth 客户端（应用接入的技术形态）",
     "source": "dev", "sql": "SELECT * FROM gkxlumenx.sys_oauth_client_details",
     "hits": 8,
     "hit_detail": "8 行全为 pig 框架内置服务客户端（app/daemon/gen/mini/mp/pig/social/test）——"
                   "平台自身微服务，非数据消费方应用；无接入时间/归属部门/调用统计列"},
    {"probe": "gkx 应用系统登记面（app/application 词族，280 表）",
     "source": "gkx", "sql": "information_schema.tables 扫 gkx（共享探针）",
     "hits": 0,
     "hit_detail": "唯一命中 dwd_patent_applicants 是专利申请人表——假命中（词形同、语义异）"},
    {"probe": "久新应用系统登记面（同词族，live 复核 + 列核）",
     "source": "jiuxin", "sql": "SHOW TABLES 词族 + DESC ads_technology_application_case",
     "hits": 0,
     "hit_detail": "唯一命中 ads_technology_application_case（181,735 行，S3-01 快照同锚）是"
                   "技术落地案例面——『应用』指技术成果应用场景，列无系统接入语义——语义排除"},
    {"probe": "需求原文「接入应用系统数/应用数」定义段",
     "source": "doc", "sql": "rg 接入应用/应用数 三份需求真源",
     "hits": 2,
     "hit_detail": "SRS seq 396「自动识别和归集每次数据调用对应的应用系统名称及其业务来源部门」"
                   "（归集功能在）；主需求 :2553「应用系统运行情况」——「接入应用系统数」指标名"
                   "与计数口径（去重键/接入判定/在网状态）三份说明书均未出现"},
]

support = "部分支持"

notes += [
    "判档：接入登记面（应用系统×接入关系×归属部门）三源零语义命中（词族命中全为假命中）——"
    "严格口径不可构建；但该指标是纯登记面计数（无流水依赖），建表即直查，且 dev OAuth 客户端"
    "表（8 行）证明平台已有「应用客户端」技术形态可扩列 → 部分支持（登记面缺位型）",
    "与 026 同物裁定：024（业务应用 Tab 应用数列合计 162）与 026（KPI 卡「应用系统数」147）"
    "是同一语义的两个 UI 读数位——mock 内部失配 147 vs 162（差 15）证明前端两处未对账；"
    "两件应合并为一个指标（登记面计数），一处计算两处展示；本件为明细侧主件，026 为 KPI 侧"
    "同物件（互引见 026 MD §1.7）",
    "mock 披露：businessApplicationStats 6 行 appCount 45/32/28/23/19/15 合计 162"
    "（facts.mock_appcount_sum）；KPI 卡 applicationKPIs[1] value='147'（mockData.js:1668）——"
    "两处演示值不相等，不作数据证据（B10）",
    "语义排障：三源四个「app 词族命中」三种性质——前端 CMS（dev app.*）、要素数据（patent_"
    "applicants）、分析案例（jiuxin application_case）、平台服务账号（oauth_client）——"
    "无一是「数据消费方应用系统」；词形命中必须过列级语义关",
    "B11 对账：dev 542/gkx 280/久新 210 表数共享快照；application_case 181,735 行与 S3-01 "
    "共享快照同锚",
    "升档触发器（B10）：①建应用系统接入登记面（系统名×归属部门×接入时间×状态）→ 升完全直接"
    "支持（纯计数，建表即得）；②甲方接受 OAuth 客户端数 8 作技术形态代理 → 仍属部分支持"
    "（口径披露「平台服务客户端非消费方应用」）；③维持现状 → 部分支持（严格口径 null）",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_024",
    "batch": "S3-04",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:240",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:989",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书未出现「接入应用系统数」指标名；语义锚 SRS 应用视窗 seq 396"
                "「应用系统名称及其业务来源部门自动归集」（归集功能在、计数口径无）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [], "base_years_missing": [],
    "base_years_note": "登记面计数类指标，不涉基期年",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["6", "45", "32", "28", "23", "19", "15", "162", "147", "8", "2054000",
                          "542", "280", "210", "181735", "15"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

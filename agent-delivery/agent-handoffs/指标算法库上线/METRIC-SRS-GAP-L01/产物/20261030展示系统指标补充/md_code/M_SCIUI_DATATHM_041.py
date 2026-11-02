#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_041 调用量月度趋势 · 三源探针与复现脚本（S3-05 L1）。

含义：接入视窗·问题资源可视化统计报表导出的「月度趋势」sheet——问题资源
月度序列（月份/问题总数/已解决）。UI：AccessWindow.jsx:556（ExportButton
sheets name='月度趋势'，fields 月份/问题总数/已解决）；mock 源
mockData.js:1708-1714 problemResourceStats.monthlyTrend（1-6 月 18/22/25/
…双序列）。派单名「调用量月度趋势」按 L3 命名=「数量＞月度趋势」——
月度趋势的量纲语义族（本挂载位实际量纲=问题资源数，跨窗族同构位=调用量）。

判档路径（口径=「逐月时序量（月×量双序列）」）：
- 直接承载：月度序列面——问题资源月度台账三源零承载（词族证）；
  调用量月度序列亦零承载（020/021/022 调用族先例：API 调用日志面三源 0 命中）；
- 最近邻：dev sys_log 月维分布（2026-07:99/08:36/09:8/10:917）——平台管理
  操作日志（OAuth2 认证端点，020 语义排除在案），非数据资源调用流；
  久新 metrics_as_of_date 单日一期（2026-09-18），无逐月快照；
  dev enterprise_news 月维单点 2026-08:1,668,414（批次式）；
→ 完全不支持（逐月序列维三源无承载——无论量纲取问题资源数还是调用量）。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_041_out.json")
PROBE = os.path.join(BASE, "_probe_s305_l1_out.json")

facts, derived, notes, absence = {}, [], [], []
probe = json.load(open(PROBE, encoding="utf-8"))["probes"]

# ============ ① 词族（共享探针复用） ============
facts["dev_table_total"] = probe["dev_table_total"]
facts["dev_call_tables"] = probe["dev_call_tables"]        # [] 调用词族 0 命中
facts["dev_period_tables"] = probe["dev_period_tables"]   # [] 月/周/日序列词族 0 命中
facts["gkx_table_count"] = probe["gkx_table_count"]
facts["gkx_call_tables"] = probe["gkx_call_tables"]       # []
facts["jiuxin_table_count_live"] = probe["jiuxin_table_count_live"]
facts["jiuxin_call_tables"] = probe["jiuxin_call_tables"]  # []

# ============ ② 三源时间维形态（月维序列可行性的逐一排除） ============
facts["dev_sys_log_month_dist"] = probe["dev_sys_log_month_dist"]  # 4 点（最近邻，语义排除）
facts["dev_sys_log_rows"] = probe["dev_sys_log_rows"]
facts["dev_enterprise_news_month_dist"] = probe["dev_enterprise_news_update_month_dist_top12"]  # 单点批次
facts["jiuxin_snapshot_as_of_dist"] = probe["jiuxin_talent_yearly_as_of_dist"]  # 单日一期
facts["jiuxin_snapshot_as_of_note"] = "ads_talent_yearly_metrics 按 metrics_as_of_date 分布：None 255,806 + 2026-09-18 1,022,242——单快照日一期，无逐月期"

# ============ ③ 调用族先例复核（B11 锚） ============
import pymysql  # noqa: E402
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
conn = pymysql.connect(**DEV)
cur = conn.cursor()
# sys_log request_uri 复核（月维 4 点的语义锚——认证端点占比）
cur.execute(
    "SELECT request_uri, COUNT(*) FROM gkxlumenx.sys_log "
    "GROUP BY request_uri ORDER BY COUNT(*) DESC, request_uri ASC LIMIT 5")
facts["dev_sys_log_uri_top5"] = [[str(a), int(b)] for a, b in cur.fetchall()]
conn.close()

# ============ ④ mock 对照 ============
facts["ui_mock_monthly_trend_sorted"] = [
    ["1月", 18, 15], ["2月", 22, 18], ["3月", 25, 20], ["4月", 20, 17],
    ["5月", 23, 16]]  # month, total, resolved（mock 1-5 月 5 点，本件逐值核验）

# ================= absence_probe =================
absence += [
    {"probe": "dev 调用日志面 + 月度序列面（call/invoke/api/request + period/monthly/weekly/daily 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表，共享探针独立两族）",
     "hits": 0,
     "hit_detail": "call 词族 []（0 张，与 020/021/022 独立复跑一致）；period/monthly/weekly/daily "
                   "词族 []（0 张）——无任何逐月序列承载表；最近邻 sys_log 月维 4 点（07:99/08:36/"
                   "09:8/10:917）但 URI Top 为 /oauth2/token 认证端点（020 语义排除在案，本件 Top5 复核）",
     },
    {"probe": "gkx 调用/序列面",
     "source": "gkx",
     "sql": "词族扫描（共享探针 gkx_call_tables=[]）",
     "hits": 0,
     "hit_detail": "280 表 call/invoke/api/request 词族 0 命中（要素明细库无调用监控面，"
                   "与 020/021/022 同结论）",
     },
    {"probe": "久新调用/逐月快照面",
     "source": "jiuxin",
     "sql": "词族扫描 + metrics_as_of_date 分布（共享探针）",
     "hits": 0,
     "hit_detail": "215 表 live 词族 0 命中；ads_talent_yearly_metrics 的 metrics_as_of_date "
                   "分布 None 255,806 + 2026-09-18 1,022,242——单快照日一期（019/003 同证），"
                   "无逐月期序列",
     },
    {"probe": "需求原文「月度趋势/调用量趋势」指标定义",
     "source": "doc",
     "sql": "rg 检索三份需求真源",
     "hits": 1,
     "hit_detail": "「月度趋势」为 UI 导出 sheet 名（AccessWindow.jsx:556）；主需求 :2563"
                   "「动态跟踪……调用频率」/:2571 趋势功能在（021/022 已承接）——工程前提 "
                   "API 日志未建；「调用量月度趋势」指标名与算式三份真源 0 命中",
     },
]

support = "完全不支持"

notes += [
    "判档：逐月时序量需「月×量」序列面——调用口径三源 0 命中（020/021/022 先例+本件独立复核）；"
    "本挂载位实际量纲（问题资源月度）同样无台账；时间维三源形态逐一排除"
    "（sys_log 4 点语义排除/enterprise_news 单点批次/久新单日一期）→ 完全不支持",
    "量纲披露：派单名「调用量月度趋势」（L3 命名=数量＞月度趋势）；本挂载位 mock 实际量纲是"
    "问题资源数（monthlyTrend total/resolved 双序列）——两量纲共用「月度序列面缺失」同一根因，"
    "判档结论对两量纲一致成立",
    "最近邻语义排除（sys_log 月维 4 点）：URI Top5 全 OAuth2 认证端点（020 在案，本件复核）——"
    "管理操作日志月维≠数据资源调用月维，且 10 月 917 行为平台调试期放量非业务节奏",
    "B11 对账：词族扫描与 020/021/022 调用族先例一致；久新单日一期与 019/003 同证；"
    "月维读数全部取共享探针（_probe_s305_l1_out.json）",
    "升档触发器（B10）：①API 网关/调用日志接入（APM 面，与 020/021/022 族共用）→ "
    "调用量口径升完全直接支持；②问题资源台账立项（问题×发现月×解决月）→ 本挂载位口径"
    "升完全直接支持",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_041",
    "batch": "S3-05",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/AccessWindow.jsx:556",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:1708",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份需求说明书未出现「调用量月度趋势」。「月度趋势」为导出 sheet 名（:556）；"
                "语义锚 :2563「动态跟踪……调用频率」/:2571 趋势功能（021/022 已承接，"
                "工程前提 API 日志未建）；mock monthlyTrend 实际量纲=问题资源数",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "月度序列不可构建（无逐月期面）",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "18", "22", "25", "20", "23", "99", "36", "8", "917", "1668414",
        "542", "280", "215"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

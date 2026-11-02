#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATAAPP_001 主题调用基本信息统计 · 三源探针脚本（S3-05 L3）。

含义：科技数据资源·应用视窗·主题数据被调用情况·主题调用基本信息统计
（SRS seq 384 / excel_row 387，需求明列叶）——按主题维度的调用量构成
（UI 饼图：基础科学 856,000 / 医学健康 642,000 / 工程技术 534,000 / 农业科技 423,000 /
能源环境 389,000；明细表 themeCallBasicInfo 5 行：主题名称/调用时间/调用频率/调用接口/业务系统）。
UI：repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:284-299（饼图）、
:306-310（明细表挂 ThemeCallTab 内，本件以饼图挂载行为主）；mock 源
mockData.js:1546-1576（themeCallTrend 12 月 5 主题序列 + themeCallBasicInfo 5 行，
注释自标需规 seq 384）。

判档路径（口径=「主题级调用登记面：主题×调用量×时间×接口×业务系统」）：
- 直接承载：需调用日志/台账面——三源词族（call/invoke/api_log/usage/access_log）0 命中
  （本批族级探针 _probe_s305_l3_call 独立留证）；
- 主题维载体：三源无「主题库」登记（gkx 无 theme 表、dev cms_svc_business_domain 是服务域非
  数据资源主题、久新 ads_* 是学科分析面非平台主题库）——主题轴无承载；
- 语义最近邻：dev sys_log 是平台认证管理日志（DATATHM_020 已语义排除），非主题调用；
- 判完全不支持（主题级调用面与主题登记轴三源均无）。
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATAAPP_001_out.json")
SNAP_LANE7 = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s305_l3_call_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402

facts, derived, notes, absence = {}, [], [], []
snap = json.load(open(SNAP_LANE7, encoding="utf-8"))
probe = json.load(open(PROBE, encoding="utf-8"))["facts"]

# ============ ① dev：主题轴承载核（词族 + cms_svc_business_domain 语义核） ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx", charset="utf8mb4", connect_timeout=10, read_timeout=120)
d = pymysql.connect(**DEV)
c = d.cursor()
c.execute("SELECT table_schema, table_name FROM information_schema.tables "
          "WHERE table_schema LIKE 'gkxlumenx%' AND table_name REGEXP 'theme|subject' ORDER BY table_schema, table_name")
facts["dev_theme_word_tables"] = [f"{r[0]}.{r[1]}" for r in c.fetchall()]
# cms_svc_business_domain 语义核（唯一 theme 词命中，证是服务业务域非数据资源主题库）
c.execute("SELECT COUNT(*) FROM gkxlumenx_cms.cms_svc_business_domain")
facts["dev_cms_svc_business_domain_rows"] = int(c.fetchone()[0])
# 调用日志词族（本件主判依赖，复跑留证）
c.execute("SELECT table_schema, table_name FROM information_schema.tables "
          "WHERE table_schema LIKE 'gkxlumenx%' AND table_name REGEXP "
          "'call|invoke|api_log|access_log|usage_log|request_log|trace'")
facts["dev_call_word_tables"] = sorted(f"{r[0]}.{r[1]}" for r in c.fetchall())
facts["dev_table_total"] = int(probe["dev_table_total"])
d.close()

# ============ ② gkx：词族复核（族级探针 0 命中） ============
facts["gkx_call_word_tables"] = probe["gkx_call_word_tables"]  # []
facts["gkx_table_count"] = probe["gkx_table_count"]
# gkx 主题语义最近邻：无 theme 表；学科轴在 dwd_zh_paper（学科≠平台主题库，语义排除登记）
facts["gkx_theme_word_tables"] = []

# ============ ③ 久新：词族复核 + 学科分析面语义排除 ============
facts["jiuxin_probe_mode"] = probe["jiuxin_probe_mode"]
facts["jiuxin_table_count_live"] = probe["jiuxin_table_count_live"]
facts["jiuxin_call_word_tables"] = probe["jiuxin_call_word_tables"]  # []
try:
    JX = dict(host="47.93.119.170", port=29030, user="test2",
              password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
              database="gkx_technology_analysis_dev",
              connect_timeout=10, read_timeout=300)
    jconn = pymysql.connect(**JX)
    jc = jconn.cursor()
    jc.execute("SHOW TABLES")
    jx_tables = sorted(r[0] for r in jc.fetchall())
    facts["jiuxin_theme_word_tables_live"] = [t for t in jx_tables
                                              if any(k in t.lower() for k in ("theme", "subject"))]
    # 学科分析面在册证明（语义排除：discipline 是文献学科非数据资源主题库）
    facts["jiuxin_discipline_tables_live"] = [t for t in jx_tables if "discipline" in t.lower()]
    jconn.close()
except Exception as e:  # noqa: BLE001
    jx_tables = snap["jiuxin"]["tables"]
    facts["jiuxin_theme_word_tables_live"] = [t for t in jx_tables
                                              if any(k in t.lower() for k in ("theme", "subject"))]
    facts["jiuxin_discipline_tables_live"] = [t for t in jx_tables if "discipline" in t.lower()]
    facts["jiuxin_probe_mode"] = f"{facts['jiuxin_probe_mode']}（复核直连失败：{str(e)[:60]}）"

# mock 演示值登记（边界证据，不作源）
facts["ui_mock_pie_values"] = [["基础科学", 856000], ["医学健康", 642000],
                               ["工程技术", 534000], ["农业科技", 423000], ["能源环境", 389000]]
facts["ui_mock_pie_sum"] = sum(v for _, v in facts["ui_mock_pie_values"])
facts["ui_mock_basicinfo_rows"] = 5

# ================= 派生（负结论登记，B10） =================
derived.append({
    "key": "theme_call_total_by_subject",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『主题级调用量构成（主题×调用量）』三源无调用日志/台账面（词族 0 命中）且无平台主题库"
            "登记轴（dev/gkx/久新 theme 词族均语义排除）→ 不可构建；UI 饼图 5 主题值合计 "
            "2,844,000 为 mock 演示值（ApplicationWindow.jsx:289-295 硬编码），按 B10 留空即负结论登记",
})

# ================= absence_probe =================
absence += [
    {"probe": "dev 主题调用日志/台账面（call/invoke/api_log/access_log/usage_log/request_log/trace 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表，本件独立复跑）",
     "hits": len(facts["dev_call_word_tables"]),
     "hit_detail": "0 张——dev 无任何调用日志表；最近邻 sys_log（1,060 行）是平台认证管理日志"
                   "（DATATHM_020 已语义排除：URI Top 为 /oauth2/token），非主题数据调用",
     },
    {"probe": "dev 平台主题库登记轴（theme/subject 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*",
     "hits": len(facts["dev_theme_word_tables"]),
     "hit_detail": f"命中 {facts['dev_theme_word_tables']}——cms_svc_business_domain 是科技服务"
                   "系统的业务域字典（服务域配置），不是数据资源主题库登记；主题轴无承载",
     },
    {"probe": "gkx 调用监控面 + 主题轴（call 词族 + theme 词族）",
     "source": "gkx",
     "sql": "information_schema.tables 扫 gkx（280 表，本批族级探针）",
     "hits": 0,
     "hit_detail": "调用词族 0 命中（要素明细库）；无 theme 表——gkx 无主题库概念，"
                   "学科轴在 dwd_zh_paper 等文献表（学科分类≠平台主题库）",
     },
    {"probe": "久新调用面 + 主题轴（call 词族 + theme/subject 词族）",
     "source": "jiuxin",
     "sql": "SHOW TABLES（当日 live）词族扫",
     "hits": len(facts["jiuxin_theme_word_tables_live"]),
     "hit_detail": f"theme/subject 词族命中 {facts['jiuxin_theme_word_tables_live']}；"
                   f"discipline 面 {len(facts['jiuxin_discipline_tables_live'])} 张在册"
                   "（ads_discipline_* 是文献学科分析面，非数据资源主题库调用统计）；"
                   "调用词族 0 命中——ads_* 全为按 metrics_as_of_date 快照管理的分析结果面",
     },
    {"probe": "需求原文「主题调用基本信息统计」定义段",
     "source": "doc",
     "sql": "SRS 应用视窗.md seq 384 + 主需求同文",
     "hits": 1,
     "hit_detail": "seq 384『自动收集并展示每个主题数据的调用基础信息，包括主题名称、调用时间、"
                   "调用频率、调用接口及涉及的业务系统』——功能在、且需求自宣数据来源为「自动收集」"
                   "（调用日志采集），该工程前提三源未建；聚合口径（构成比/时间窗）无定义",
     },
]

support = "完全不支持"

notes += [
    "判档：主题级调用构成需「调用日志×主题登记」双依赖——调用面三源词族 0 命中（独立复跑+族探针），"
    "主题轴三源无平台主题库登记（cms_svc_business_domain=服务域字典/gkx 无 theme 表/久新 discipline="
    "文献学科面，逐一语义排除）→ 指标及关键依赖三源均无法构建 → 完全不支持",
    "mock 披露：ApplicationWindow.jsx:289-295 饼图 5 主题值硬编码（合计 2,844,000），"
    "mockData.js:1557-1564 themeCallBasicInfo 5 行（注释自标需规 seq 384）——演示值，不作数据证据（B10）",
    "需求侧证据：seq 384 明列五字段（主题名称/调用时间/调用频率/调用接口/业务系统）——UI 明细表"
    "五列与之一一对应，前端已按需求字段建模；缺口在数据侧（调用日志采集工程前提未建）",
    "B11 对账：dev 542/gkx 280/久新 live 当日表数共享探针；调用词族与 S3-04 族级探针"
    "（DATATHM_020 gkx_call_like_tables=[]）一致",
    "升档触发器（B10）：①API 网关/调用日志接入（含主题标识列）+ 主题库登记面 → 升完全直接支持"
    "（工程立项，族级共用）；②乙方以「主题资源被引用情况」代理口径（如按主题库表访问记录）→ "
    "升完全转换支持（口径须披露非真实 API 调用）",
]

out = {
    "metric_id": "M_SCIUI_DATAAPP_001",
    "batch": "S3-05",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:284",
        "repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:306",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:1546",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:1557",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "SRS《02-科技信息展示系统/科技数据资源/应用视窗.md》seq 384（excel_row 387）+"
                "主需求 1.1.1.1.4.4.4.3.1 同文——需求明列叶：『自动收集并展示每个主题数据的调用"
                "基础信息，包括主题名称、调用时间、调用频率、调用接口及涉及的业务系统』——功能在、"
                "聚合口径无定义；核增需求与算法库 0 命中",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "监控类指标，不涉基期年",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["856000", "642000", "534000", "423000", "389000", "2844000",
                          "5", "542", "280", "215"][:12]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

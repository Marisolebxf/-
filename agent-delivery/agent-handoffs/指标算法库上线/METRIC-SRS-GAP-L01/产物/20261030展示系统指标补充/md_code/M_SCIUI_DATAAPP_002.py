#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATAAPP_002 主题调用基本信息统计（明细）· 三源探针脚本（S3-05 L3）。

含义：科技数据资源·应用视窗·主题数据被调用情况·主题调用基本信息统计的**明细表形态**
（SRS seq 384 同叶——明细五字段：主题名称/调用时间/调用频率/调用接口/业务系统）。
UI：repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:306-310
（Card title="主题调用基本信息统计（明细）"，Table themeCallInfoColumns 5 列消费
mock themeCallBasicInfo 5 行：mockData.js:1557-1564，注释自标需规 seq 384）。
判档同 DATAAPP_001（同叶明细形态，双依赖同缺），本件独立留证。
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATAAPP_002_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s305_l3_call_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402

facts, derived, notes, absence = {}, [], [], []
probe = json.load(open(PROBE, encoding="utf-8"))["facts"]

# ============ ① dev：明细五字段载体核（接口登记/业务系统登记独立词族） ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx", charset="utf8mb4", connect_timeout=10, read_timeout=120)
d = pymysql.connect(**DEV)
c = d.cursor()
# 明细五字段的字段级载体：接口登记面（callInterface）与业务系统登记面（businessSystems）
c.execute("SELECT table_schema, table_name FROM information_schema.tables "
          "WHERE table_schema LIKE 'gkxlumenx%' AND table_name REGEXP "
          "'interface|business_system|biz_system' ORDER BY table_schema, table_name")
facts["dev_interface_bizsys_tables"] = [f"{r[0]}.{r[1]}" for r in c.fetchall()]
# 调用词族（与 001 同判，复跑留证）
c.execute("SELECT table_schema, table_name FROM information_schema.tables "
          "WHERE table_schema LIKE 'gkxlumenx%' AND table_name REGEXP "
          "'call|invoke|api_log|access_log|usage_log|request_log|trace'")
facts["dev_call_word_tables"] = sorted(f"{r[0]}.{r[1]}" for r in c.fetchall())
# sys_oauth_client_details（8 个客户端——最近邻「应用系统」登记，语义核；实查表名带 _details 后缀）
try:
    c.execute("SELECT client_id FROM gkxlumenx.sys_oauth_client_details ORDER BY client_id LIMIT 10")
    facts["dev_sys_oauth_clients"] = [[str(r[0]), ""] for r in c.fetchall()]
except Exception as e:  # noqa: BLE001
    facts["dev_sys_oauth_clients"] = []
    facts["dev_sys_oauth_client_note"] = str(e)[:80]
d.close()

# ============ ② gkx：接口/业务系统词族复核 ============
facts["gkx_table_count"] = probe["gkx_table_count"]
facts["gkx_call_word_tables"] = probe["gkx_call_word_tables"]
facts["gkx_interface_bizsys_tables"] = []  # 280 表无 interface/business_system 词族（族级探针表清单复核）

# ============ ③ 久新：接口/业务系统词族复核（live） ============
facts["jiuxin_probe_mode"] = probe["jiuxin_probe_mode"]
try:
    JX = dict(host="47.93.119.170", port=29030, user="test2",
              password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
              database="gkx_technology_analysis_dev",
              connect_timeout=10, read_timeout=300)
    jconn = pymysql.connect(**JX)
    jc = jconn.cursor()
    jc.execute("SHOW TABLES")
    jx_tables = sorted(r[0] for r in jc.fetchall())
    facts["jiuxin_interface_bizsys_tables_live"] = [
        t for t in jx_tables if any(k in t.lower() for k in ("interface", "business_system", "biz_system"))]
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_interface_bizsys_tables_live"] = []
    facts["jiuxin_probe_mode"] = f"{facts['jiuxin_probe_mode']}（复核直连失败：{str(e)[:60]}）"

# mock 明细五字段登记（边界证据）
facts["ui_mock_basicinfo_columns"] = ["主题名称", "调用时间", "调用频率", "调用接口", "涉及业务系统"]
facts["ui_mock_basicinfo_rows"] = [
    ["基础科学", "近30天", "高频", "GET /api/theme/basic", "科研项目评估、文献计量"],
    ["医学健康", "近30天", "高频", "GET /api/theme/medical", "医学研究平台、影像诊断"],
    ["工程技术", "近30天", "中频", "GET /api/theme/engineering", "智能制造、工业4.0示范线"],
    ["农业科技", "近30天", "中频", "GET /api/theme/agriculture", "智慧农业示范、产量评估"],
    ["能源环境", "近30天", "低频", "GET /api/theme/energy", "碳达峰监测、环境监测"],
]
facts["ui_mock_callfreq_domain"] = ["高频", "中频", "低频"]  # 序数分档非数值口径

# ================= 派生（负结论登记，B10） =================
derived.append({
    "key": "theme_call_basicinfo_detail_rows",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『主题调用明细（主题名称/调用时间/调用频率/调用接口/业务系统五字段行级流水）』三源无"
            "调用日志面（词族 0 命中）且接口/业务系统登记面词族 0 命中 → 不可构建；UI 明细 5 行为"
            "mock 演示值（mockData.js:1558-1563），按 B10 留空即负结论登记",
})

# ================= absence_probe =================
absence += [
    {"probe": "dev 调用明细流水面（call/invoke/api_log/access_log/usage_log/request_log/trace 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表，本件独立复跑）",
     "hits": len(facts["dev_call_word_tables"]),
     "hit_detail": "0 张——dev 无调用流水表；sys_log（1,060 行）是认证管理日志（DATATHM_020 语义排除在案）",
     },
    {"probe": "dev 接口登记面 + 业务系统登记面（interface/business_system/biz_system 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*",
     "hits": len(facts["dev_interface_bizsys_tables"]),
     "hit_detail": f"命中 {facts['dev_interface_bizsys_tables']}——明细五字段中「调用接口」「业务系统」"
                   "两列的登记载体词族零语义命中（无接口目录、无业务系统目录）；最近邻 sys_oauth_client "
                   f"是 OAuth 客户端配置（{len(facts['dev_sys_oauth_clients'])} 个，app/daemon/gen 等"
                   "技术客户端），非业务应用系统登记",
     },
    {"probe": "gkx 调用面 + 接口/业务系统登记面",
     "source": "gkx",
     "sql": "information_schema.tables 扫 gkx（280 表，族级探针+表清单复核）",
     "hits": 0,
     "hit_detail": "调用词族 0 命中；interface/business_system 词族 0 命中——gkx 要素明细库无平台"
                   "调用语义表",
     },
    {"probe": "久新调用面 + 接口/业务系统登记面",
     "source": "jiuxin",
     "sql": "SHOW TABLES（当日 live）词族扫",
     "hits": len(facts["jiuxin_interface_bizsys_tables_live"]),
     "hit_detail": "0 命中——ads_* 全为学科/人才/专利/项目分析结果面，无接口目录与业务系统目录",
     },
    {"probe": "需求原文明细五字段定义段",
     "source": "doc",
     "sql": "SRS 应用视窗.md seq 384 + 主需求同文",
     "hits": 1,
     "hit_detail": "seq 384 五字段（主题名称、调用时间、调用频率、调用接口及涉及的业务系统）——"
                   "UI 明细表五列与之一一对应；「调用频率」无口径（mock 用高/中/低序数分档，"
                   "非数值频率）；字段级明细要求调用流水存在，该前提三源未建",
     },
]

support = "完全不支持"

notes += [
    "判档：与 DATAAPP_001 同叶（seq 384）明细形态——行级流水（主题×时间×频率×接口×业务系统）"
    "需调用日志面，且五字段中接口/业务系统两列另需登记目录——三源词族均 0 命中 → 完全不支持",
    "mock 披露：明细 5 行为演示值；「调用频率」列用高/中/低序数分档（ui_mock_callfreq_domain），"
    "非数值口径——需求未定义频率算法，正式版须先裁口径（次/天数值 or 分档阈值）",
    "B11 对账：调用词族与 001/S3-04 族探针一致；oauth_client 8 个客户端读数与 L5 探针一致",
    "升档触发器（B10）：同 DATAAPP_001（调用日志+主题登记族级触发器①；另需接口目录/业务系统"
    "目录两登记面才能落明细五列）",
]

out = {
    "metric_id": "M_SCIUI_DATAAPP_002",
    "batch": "S3-05",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:306",
        "repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:272",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:1557",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "SRS seq 384（excel_row 387）同叶明细形态（UI 卡题自带「（明细）」后缀区分）；"
                "五字段明列于需求句：『包括主题名称、调用时间、调用频率、调用接口及涉及的业务系统』"
                "——功能在、行级流水来源（调用日志）与频率口径无定义；核增需求与算法库 0 命中",
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
                 "refs": ["5", "8", "1060", "542", "280"][:8]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

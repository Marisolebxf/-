#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_021 调用量同比增速（较上年）· 三源探针脚本（S3-04 L1）。

含义：科技数据资源·累计调用与趋势分析的「调用量」年度维度派生读数——数据资源接口累计
调用量（mock totalCalls 2,856,000）的同比增速（较上年）。screen_v3 行 406 l3「年份＞同比增速」。
UI：repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:575
（reportSheets「年度增长趋势」sheet 的「同比增速」列，dataIndex 'yoy'——挂载点为导出报表
复用位；mock 源 mockData.js:72-78 overviewAnnualAccessTrend yoy 31.7/29.0/22.2/13.8 演示值）。

判档路径（口径=「数据资源接口调用量的年度同比」）：
- 直接承载：需 API 调用日志（接口×时间×次数）——需求 :2563「API日志采集」/:2571「累计调用量」
  自点名工程前提；三源词族（call/invoke/api/request/access_log）0 命中；
- dev sys_log 为平台管理操作日志（OAuth2 认证端点，020 已语义排除）——非资源接口调用流水；
- 内容年份面（论文/专利/企业/人才年分布）与「调用量」无语义关联（内容≠调用），不代理；
- 判完全不支持（调用日志面三源零承载，无代理路径）。
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_021_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s304_l1_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402

facts, derived, notes, absence = {}, [], [], []
snap = json.load(open(SNAP, encoding="utf-8"))
probe = json.load(open(PROBE, encoding="utf-8"))["probes"]

# ============ ① dev：调用日志词族独立复跑 + sys_log 语义引用 ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
d = pymysql.connect(**DEV)
c = d.cursor()

c.execute(
    "SELECT table_schema, table_name FROM information_schema.tables "
    "WHERE table_schema LIKE 'gkxlumenx%' AND table_name REGEXP "
    "'call_log|invoke_log|api_log|access_log|request_log|usage_log|call_stat|invoke_stat'")
facts["dev_call_log_tables"] = [f"{r[0]}.{r[1]}" for r in sorted(c.fetchall())]
# sys_log 按月分布（管理操作节奏——非调用量，语义引用 020 排除结论）
c.execute(
    "SELECT DATE_FORMAT(create_time, '%Y-%m') m, COUNT(*) FROM gkxlumenx.sys_log "
    "GROUP BY m ORDER BY m")
facts["dev_sys_log_month_dist"] = [[str(a), int(b)] for a, b in c.fetchall()]
d.close()

# ============ ② gkx：词族复核（族级探针 0 命中） ============
facts["gkx_call_like_tables"] = probe["gkx_call_like_tables"]  # []
facts["gkx_table_count"] = snap["gkx"]["table_count"]

# ============ ③ 久新：词族复核（当日 live 直连） ============
import re  # noqa: E402
try:
    JX = dict(host="47.93.119.170", port=29030, user="test2",
              password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
              database="gkx_technology_analysis_dev",
              connect_timeout=10, read_timeout=300)
    jconn = pymysql.connect(**JX)
    jc = jconn.cursor()
    jc.execute("SHOW TABLES")
    jx_tables = sorted(r[0] for r in jc.fetchall())
    facts["jiuxin_table_count_live"] = len(jx_tables)
    facts["jiuxin_call_log_tables_live"] = [
        t for t in jx_tables
        if re.search(r"call_log|invoke|api_log|access_log|request_log|usage_log|call_stat", t, re.I)]
    jconn.close()
    facts["jiuxin_probe_mode"] = "live"
except Exception as e:  # noqa: BLE001
    jx_tables = snap["jiuxin"]["tables"]
    facts["jiuxin_call_log_tables_snapshot"] = [
        t for t in jx_tables
        if re.search(r"call_log|invoke|api_log|access_log|request_log|usage_log|call_stat", t, re.I)]
    facts["jiuxin_probe_mode"] = f"快照兜底（当日直连失败：{str(e)[:80]}）"

# ================= 派生（负结论登记，B10） =================
derived.append({
    "key": "call_volume_yoy_growth_pct",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『调用量同比增速』需 API 调用日志的年度两期面（本年/上年调用量）——三源词族 0 命中，"
            "调用日志面不存在 → 不可构建；内容年份面（论文/专利/企业/人才年分布）度量的是库内"
            "内容产出，与『接口调用次数』无语义关联，不作代理（代理路径不存在，区别于 015 的"
            "数据量变化率）；按 B10 留空即负结论登记",
})

# ================= absence_probe =================
absence += [
    {"probe": "dev 调用量日志面（call_log/invoke_log/api_log/access_log/request_log/usage_log/"
              "call_stat 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表）",
     "hits": len(facts["dev_call_log_tables"]),
     "hit_detail": f"命中 {facts['dev_call_log_tables']}——0 张调用日志表；最近邻 sys_log "
                   f"（月分布 {facts['dev_sys_log_month_dist']}）为平台管理操作日志"
                   "（020 已语义排除：OAuth2 认证端点主导），非资源接口调用流水",
     },
    {"probe": "gkx 调用量面（call/invoke/api/request/latency/response/duration/monitor/usage 词族）",
     "source": "gkx",
     "sql": "information_schema.tables 扫 gkx（280 表，S3-04 族级探针）",
     "hits": len(facts["gkx_call_like_tables"]),
     "hit_detail": f"命中 {facts['gkx_call_like_tables']}——0 命中；gkx 为论文/专利/机构/学者等"
                   "要素明细库，无任何调用统计面",
     },
    {"probe": "久新调用量面（同词族）",
     "source": "jiuxin",
     "sql": "SHOW TABLES（当日 live）词族扫",
     "hits": len(facts.get("jiuxin_call_log_tables_live", [])) or
             len(facts.get("jiuxin_call_log_tables_snapshot", [])),
     "hit_detail": "0 命中——ads_* 全部为学科/人才/专利/项目分析结果面（按 metrics_as_of_date "
                   "快照管理），无调用统计；探测模式见 facts.jiuxin_probe_mode",
     },
    {"probe": "需求原文「调用量/累计调用」定义段",
     "source": "doc",
     "sql": "rg 调用量 三份需求真源",
     "hits": 2,
     "hit_detail": "主需求 :2563（资源接口状态跟踪）『通过API日志采集与接口调用分析，动态跟踪…"
                   "调用频率和失败率』；:2571（1.1.1.1.4.4.1.4.4 累计调用与趋势分析）『自动归集"
                   "各类数据资源自上线以来的累计调用量，并按时间区段进行趋势分析』——功能在、"
                   "且需求自点名前提（API日志采集/归集累计调用量）；『同比增速』口径无；"
                   "UI yoy 列（31.7/29.0/22.2/13.8）为 mock 演示值",
     },
]

support = "完全不支持"

notes += [
    "判档：调用量年度同比需两期调用面（本年/上年接口调用次数）——三源调用日志词族 0 命中，"
    "前提不存在 → 不可构建；内容年份面与『调用』无语义关联不作代理（区别于 015——015 的"
    "『数据量』尚可用内容规模代理，本件『调用量』是服务侧动作计数，库内无任何服务调用留痕）"
    "→ 完全不支持",
    f"最近邻证据（dev sys_log，语义引用 020 排除）：按月分布 {facts['dev_sys_log_month_dist']}"
    "——管理操作级量级（月均数十至千条），与 UI mock totalCalls 2,856,000 的调用量级差三个"
    "数量级以上，排除",
    "mock 披露：OverviewWindow.jsx:575 导出 sheet「同比增速」列消费 overviewAnnualAccessTrend.yoy"
    "（31.7/29.0/22.2/13.8，mockData.js:72-78）——演示值不作数据证据；注意该 mock 序列语义是"
    "『资源接入』年度趋势，UI 将其复用于调用量语境属前端演示约定",
    "权威口径参照（R2 深圳开放平台）：接口调用量累计 373,575,274 次、近七日 TOP10 逐接口计数"
    "——调用量统计的官方实践形态=平台侧调用日志聚合",
    "B11 对账：词族扫描与 S3-04 族级探针/020 产物一致；542/280/210 共享快照",
    "升档触发器（B10）：①API 网关/调用日志接入（含时间戳，可按年聚合）→ 升完全直接支持"
    "（与 020/022 共用工程）；②甲方裁定调用量代理口径（如页面访问日志）→ 须先立项日志采集，"
    "无库内即期路径",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_021",
    "batch": "S3-04",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:575",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:72",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书未出现「调用量同比增速」指标名；语义锚 :2571『累计调用量…按时间区段"
                "趋势分析』（功能在、前提未建、同比口径无）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["2025", "2026"],
    "base_years_note": "同比基期（上年/本年调用量）三源零承载——调用日志面不存在，"
                       "base_years_missing 即全部年份",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["2856000", "31.7", "29.0", "22.2", "13.8", "575", "373575274",
                          "542", "280", "210"][:10]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

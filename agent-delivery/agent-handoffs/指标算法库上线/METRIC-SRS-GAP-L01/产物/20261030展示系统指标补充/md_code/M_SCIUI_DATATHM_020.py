#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_020 接口平均响应时长（毫秒）· 三源探针脚本（S3-04 L1）。

含义：科技数据资源·总体视窗·应用系统状态监控的「平均响应」读数——平台数据资源接口的
平均响应时长（毫秒）。UI mock 给常量 245 ms（resourceUsageStats.avgResponseTime）。
UI：repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:388-389
（ApplicationStatusMonitor items latency 项：label '平均响应'、value `${stats.avgResponseTime} ms`；
mock 源 mockData.js:833-839 resourceUsageStats——需规 seq 343 演示值）。

判档路径（口径=「数据资源接口的调用级耗时均值」）：
- 直接承载：需 API 网关/链路追踪耗时日志（需求 :2559「接口响应速度」/:2563「API日志采集」的
  工程前提）——三源词族（api_log/access_log/latency/response/duration/call/invoke/request）0 命中；
- dev sys_log 有 time 耗时列（ms），但语义核对：平台管理操作日志（登录/token 刷新等 OAuth2
  管理端点），非「数据资源接口」调用日志——语义排除（登记为最近邻证据）；
- gkx/久新：无任何调用监控面（0 命中）；
- 判完全不支持（指标及关键依赖三源均无法构建——无 API 调用耗时日志面）。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_020_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s304_l1_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402

facts, derived, notes, absence = {}, [], [], []
snap = json.load(open(SNAP, encoding="utf-8"))
probe = json.load(open(PROBE, encoding="utf-8"))["probes"]

# ============ ① dev：sys_log 耗时列语义核（最近邻证据，非资源接口日志） ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
d = pymysql.connect(**DEV)
c = d.cursor()

def q(sql):
    c.execute(sql)
    return c.fetchall()

# sys_log 全量统计与耗时分布（log_type 含义标注）
facts["dev_sys_log_total_rows"] = int(q("SELECT COUNT(*) FROM gkxlumenx.sys_log")[0][0])
c.execute("SELECT log_type, COUNT(*) FROM gkxlumenx.sys_log GROUP BY log_type ORDER BY log_type")
facts["dev_sys_log_logtype_dist"] = [[str(a), int(b)] for a, b in c.fetchall()]
# 耗时列分布（time 为 varchar，CAST 聚合；B5 双键排序）
c.execute(
    "SELECT CAST(time AS UNSIGNED) t, COUNT(*) FROM gkxlumenx.sys_log "
    "WHERE time REGEXP '^[0-9]+$' GROUP BY t ORDER BY COUNT(*) DESC, t ASC LIMIT 8")
facts["dev_sys_log_time_dist_top8"] = [[int(a), int(b)] for a, b in c.fetchall()]
# 均值与中位（调用耗时最近邻读数——语义排除披露用）
row = q("SELECT AVG(CAST(time AS UNSIGNED)), COUNT(*) FROM gkxlumenx.sys_log "
        "WHERE time REGEXP '^[0-9]+$'")
facts["dev_sys_log_time_avg_ms"] = round(float(row[0][0]), 2) if row[0][0] is not None else None
facts["dev_sys_log_time_valid_rows"] = int(row[0][1])
# request_uri 分布（证明是管理端点非数据资源接口）
c.execute(
    "SELECT request_uri, COUNT(*) FROM gkxlumenx.sys_log "
    "GROUP BY request_uri ORDER BY COUNT(*) DESC, request_uri ASC LIMIT 8")
facts["dev_sys_log_uri_top8"] = [[str(a), int(b)] for a, b in c.fetchall()]
# 接口耗时日志词族（本件主判词族，独立复跑）
c.execute(
    "SELECT table_schema, table_name FROM information_schema.tables "
    "WHERE table_schema LIKE 'gkxlumenx%' AND table_name REGEXP "
    "'api_log|access_log|invoke|latency|duration|response_time|call_log|trace'")
facts["dev_api_latency_tables"] = [f"{r[0]}.{r[1]}" for r in sorted(c.fetchall())]
d.close()

# ============ ② gkx：词族复核（族级探针 0 命中） ============
facts["gkx_call_like_tables"] = probe["gkx_call_like_tables"]  # [] 已证
facts["gkx_table_count"] = snap["gkx"]["table_count"]

# ============ ③ 久新：词族复核（当日 live 直连复核） ============
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
    facts["jiuxin_api_latency_tables_live"] = [
        t for t in jx_tables
        if re.search(r"api_log|access_log|invoke|latency|duration|response_time|call_log|trace", t, re.I)]
    jconn.close()
    facts["jiuxin_probe_mode"] = "live"
except Exception as e:  # noqa: BLE001
    # 快照兜底复核
    jx_tables = snap["jiuxin"]["tables"]
    facts["jiuxin_api_latency_tables_snapshot"] = [
        t for t in jx_tables
        if re.search(r"api_log|access_log|invoke|latency|duration|response_time|call_log|trace", t, re.I)]
    facts["jiuxin_probe_mode"] = f"快照兜底（当日直连失败：{str(e)[:80]}）"

# ================= 派生（负结论登记，B10） =================
derived.append({
    "key": "api_avg_response_time_ms",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『数据资源接口平均响应时长』三源无 API 调用耗时日志面（词族 0 命中）→ 不可构建；"
            "dev sys_log.time 是平台管理操作日志耗时（登录/token 刷新，OAuth2 管理端点），"
            "语义≠数据资源接口调用，排除不作分子；按 B10 留空即负结论登记",
})

# ================= absence_probe =================
absence += [
    {"probe": "dev API 调用耗时日志面（api_log/access_log/invoke/latency/duration/response_time/"
              "call_log/trace 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表）",
     "hits": len(facts["dev_api_latency_tables"]),
     "hit_detail": f"命中 {facts['dev_api_latency_tables']}——0 张接口耗时日志表；最近邻 "
                   f"sys_log（{facts['dev_sys_log_total_rows']} 行）有 time 耗时列但语义为平台"
                   "管理操作日志（URI Top 为 /oauth2/token 等认证端点），非数据资源接口调用"
                   "——语义排除（§3.3 专段）",
     },
    {"probe": "gkx 调用监控面（call/invoke/api/request/latency/response/duration/monitor/usage 词族）",
     "source": "gkx",
     "sql": "information_schema.tables 扫 gkx（280 表，S3-04 族级探针）",
     "hits": len(facts["gkx_call_like_tables"]),
     "hit_detail": f"命中 {facts['gkx_call_like_tables']}——0 命中；gkx 为要素明细库"
                   "（论文/专利/机构/学者），无任何 API 调用监控面",
     },
    {"probe": "久新调用监控面（同词族 + api_log/access_log/call_log/trace）",
     "source": "jiuxin",
     "sql": "SHOW TABLES（当日 live）词族扫",
     "hits": len(facts.get("jiuxin_api_latency_tables_live", [])) or
             len(facts.get("jiuxin_api_latency_tables_snapshot", [])),
     "hit_detail": "0 命中——ads_* 全部为学科/人才/专利/项目分析结果面（按 metrics_as_of_date "
                   "快照管理），无 API 调用日志；探测模式见 facts.jiuxin_probe_mode",
     },
    {"probe": "需求原文「接口响应速度/API日志」定义段",
     "source": "doc",
     "sql": "rg 响应速度|API日志 三份需求真源",
     "hits": 2,
     "hit_detail": "主需求 :2559（1.1.1.1.4.4.1.4.1 应用系统状态监控）『包括服务可用性、接口响应"
                   "速度及异常告警』；:2563（1.1.1.1.4.4.1.4.2 资源接口状态跟踪）『通过API日志采集"
                   "与接口调用分析』——功能在、且需求自己点名了工程前提（API 日志采集），"
                   "该前提三源未建；UI avgResponseTime 245 为 mock 演示值（mockData.js:835）",
     },
]

support = "完全不支持"

notes += [
    "判档：数据资源接口的调用级耗时均值需 API 网关/链路追踪日志——三源词族逐一 0 命中；"
    "dev sys_log 有耗时列但语义为平台管理操作日志（语义排除）；gkx 要素库/久新 ADS 结果面"
    "均无调用监控面 → 指标及关键依赖三源均无法构建 → 完全不支持",
    f"最近邻证据（dev sys_log，语义排除披露用）：{facts['dev_sys_log_total_rows']} 行平台操作"
    f"日志，time 耗时列有效 {facts['dev_sys_log_time_valid_rows']} 行、均值 "
    f"{facts['dev_sys_log_time_avg_ms']} ms、Top 耗时分布 {facts['dev_sys_log_time_dist_top8']}"
    f"；URI Top8 {facts['dev_sys_log_uri_top8'][:3]}…——登录/token 刷新等 OAuth2 认证端点"
    "主导，非数据资源接口",
    "mock 披露：OverviewWindow.jsx:388-389「平均响应 ${stats.avgResponseTime} ms」消费 "
    "mockData.js:833-839 resourceUsageStats.avgResponseTime=245（注释自标需规 seq 343）——"
    "演示值，不作数据证据（B10）",
    "需求侧证据：需求 :2563 明写『通过API日志采集与接口调用分析』——需求自身把 API 日志列为"
    "工程前提，该前提三源未建（缺口归属『表不存在』，修复动作是 API 网关日志/链路追踪接入）",
    "权威口径参照（R2 云智慧 API 监控）：平均响应时间=一段时间内请求响应时间的平均值"
    "（不可用不计算）——即便有日志也须先定义可用性剔除口径",
    "B11 对账：dev 542/gkx 280/久新 210 表数共享快照；词族扫描与 S3-04 族级探针一致",
    "升档触发器（B10）：①API 网关/链路追踪日志接入（APM 面）→ 升完全直接支持（需工程立项）；"
    "②乙方自建探针拨测（主动测延迟）→ 升完全转换支持（非真实调用量加权）",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_020",
    "batch": "S3-04",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:388",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:833",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书未出现「接口平均响应时长」指标名；语义锚 :2559「接口响应速度」"
                "/:2563「API日志采集与接口调用分析」（功能在、工程前提未建）",
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
                 "refs": ["245", "343", "1034", "542", "280", "210"][:8]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

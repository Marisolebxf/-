#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_043 同步异常数（期）· 三源探针与复现脚本（S3-05 L1）。

含义：接入视窗·历史资源接入情况·动态历史趋势可视化——「异常数」逐期折线
+「异常归档」汇总读数。UI：AccessHistorySituation.jsx:112（series name='异常数'
line）+ :305-309（Statistic 异常归档 anomalyCount=5 条）；mock 源
mockData.js:1434/1429（trend.anomalyCount 6 点 18-8 递减 + summary.anomalyCount 5）
+ :1437-1442 anomalyByType（同步延迟 2/接口错误 1/数据缺失 1/格式异常 1）。

判档路径（口径=「同步任务运行异常次数（期）」）：
- 状态承载（本件新探针）：dev es_sync_watermark 有 sync_status/error_msg/
  retry_count 三列（结构在）——15 模块实测 14 success + 1 failed
  （reg_info，RuntimeError 5 万 build/bulk 错误，retry 1；reg_info_demo 为
  demo 模块按纪律排除）→ 模块级「当前状态」可读；
- 但「期」口径不可构建：es_sync 每模块仅最后一笔状态（无逐次日志序列），
  xxl_job_log 0 行（调度日志空载体），月维全库无承载（041 同法）；
  「异常数（期）」= 期内异常次数——需逐次运行记录，单笔状态撑不起期计数；
→ 完全不支持（期计数的三源承载缺位：单笔状态非序列、xxl 空载体、无期维）。
  附带交付：模块级当前状态读数（14/15 success，1 failed 披露 demo 排除）。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_043_out.json")
PROBE = os.path.join(BASE, "_probe_s305_l1_out.json")

facts, derived, notes, absence = {}, [], [], []
probe = json.load(open(PROBE, encoding="utf-8"))["probes"]

# ============ ① 词族与空载体读数（共享探针复用） ============
facts["dev_table_total"] = probe["dev_table_total"]
facts["dev_xxl_job_log_rows"] = probe["dev_xxl_job_log_rows"]      # 0
facts["dev_xxl_job_info_rows"] = probe["dev_xxl_job_info_rows"]    # 0
facts["dev_xxl_job_group_rows"] = probe["dev_xxl_job_group_rows"]  # 0
facts["dev_es_sync_row_count"] = probe["dev_es_sync_row_count"]    # 15
facts["gkx_table_count"] = probe["gkx_table_count"]
facts["gkx_sync_tables"] = probe["gkx_sync_tables"]                # []
facts["jiuxin_table_count_live"] = probe["jiuxin_table_count_live"]
facts["jiuxin_sync_tables"] = probe["jiuxin_sync_tables"]          # [2 张 update_signal]

# ============ ② es_sync_watermark 状态三列实查（本件新探针） ============
import pymysql  # noqa: E402
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
conn = pymysql.connect(**DEV)
cur = conn.cursor()
cur.execute("SHOW COLUMNS FROM gkxlumenx_cfg.es_sync_watermark")
facts["dev_es_sync_cols"] = [r[0] for r in cur.fetchall()]
cur.execute("SHOW COLUMNS FROM gkxlumenx_job.xxl_job_log")
facts["dev_xxl_job_log_cols"] = [r[0] for r in cur.fetchall()]
# 状态分布（demo 模块分层披露）
cur.execute(
    "SELECT sync_status, COUNT(*) FROM gkxlumenx_cfg.es_sync_watermark "
    "GROUP BY sync_status ORDER BY sync_status")
facts["dev_es_sync_status_dist_all15"] = [[a, int(b)] for a, b in cur.fetchall()]
cur.execute(
    "SELECT sync_status, COUNT(*) FROM gkxlumenx_cfg.es_sync_watermark "
    "WHERE module_name NOT LIKE '%%demo%%' GROUP BY sync_status ORDER BY sync_status")
facts["dev_es_sync_status_dist_excl_demo"] = [[a, int(b)] for a, b in cur.fetchall()]
# failed 明细（错误信息与重试计数——排除 demo）
cur.execute(
    "SELECT module_name, sync_status, LEFT(error_msg, 120), retry_count "
    "FROM gkxlumenx_cfg.es_sync_watermark "
    "WHERE sync_status != 'success' AND module_name NOT LIKE '%%demo%%' ORDER BY module_name")
facts["dev_es_sync_failed_detail_excl_demo"] = [
    {"module": r[0], "status": r[1], "error_msg": r[2], "retry_count": int(r[3])}
    for r in cur.fetchall()]
# demo 模块清单（B10 披露：按纪律排除但行内带披露词）
cur.execute(
    "SELECT module_name, sync_status FROM gkxlumenx_cfg.es_sync_watermark "
    "WHERE module_name LIKE '%%demo%%' ORDER BY module_name")
facts["dev_es_sync_demo_modules_disclosed"] = [[a, b] for a, b in cur.fetchall()]
conn.close()

# ============ ③ mock 对照 ============
facts["ui_mock_anomaly_count_summary"] = 5  # summary.anomalyCount（异常归档）
facts["ui_mock_anomaly_trend"] = [18, 16, 14, 12, 10, 8]  # trend 6 点递减
facts["ui_mock_anomaly_by_type_sorted"] = [
    ["同步延迟", 2], ["数据缺失", 1], ["格式异常", 1], ["接口错误", 1]]  # 按类型名排序

# ================= 派生（模块级当前状态附带交付 + 期口径负结论） =================
dist = dict(facts["dev_es_sync_status_dist_excl_demo"])
total_nd = sum(dist.values())
failed_nd = dist.get("failed", 0)
derived.append({
    "key": "sync_failed_module_count_current_snapshot",
    "value": float(failed_nd),
    "numerator": failed_nd,
    "denominator": total_nd,
    "note": "模块级当前状态附带读数（非「期」口径）：es_sync_watermark 排除 demo 模块后 "
            + str(total_nd) + " 模块中 failed " + str(failed_nd) + " 个（reg_info，"
            "RuntimeError 5 万 build/bulk 错误，retry_count=1）——单笔状态快照，"
            "不等于期内异常次数（该模块历史上可能已失败多次，仅留最后一笔）",
})
derived.append({
    "key": "sync_anomaly_count_period",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『同步异常数（期）』正式口径（期内异常运行次数）三源无逐次运行日志"
            "（es_sync 单笔状态非序列、xxl_job_log 0 行、月维无承载）→ 不可构建；"
            "按 B10 留空即负结论登记",
})

# ================= absence_probe =================
absence += [
    {"probe": "dev 同步任务逐次运行日志（xxl_job_log 触发/状态/耗时序列）",
     "source": "dev",
     "sql": "SELECT COUNT(*) FROM gkxlumenx_job.xxl_job_log / xxl_job_info / xxl_job_group",
     "hits": 0,
     "hit_detail": f"xxl_job_log={facts['dev_xxl_job_log_rows']} 行、xxl_job_info="
                   f"{facts['dev_xxl_job_info_rows']} 行、xxl_job_group="
                   f"{facts['dev_xxl_job_group_rows']} 行——调度器全链空载体"
                   "（xxl_job_log 列族结构在、零数据）：逐次触发序列不存在，"
                   "「期」计数无从统计",
     },
    {"probe": "dev es_sync_watermark 状态序列能力（单笔 vs 逐次）",
     "source": "dev",
     "sql": "SHOW COLUMNS + sync_status/error_msg/retry_count 值域实查",
     "hits": 0,
     "hit_detail": "状态三列结构在（sync_status/error_msg/retry_count）且实测有真实 failed"
                   "（reg_info，RuntimeError），但每模块仅保留最后一笔状态（15 行=15 模块各 1 行）"
                   "——是状态快照非运行日志：无时间序列、无失败历史，撑不起「期」口径；"
                   "结构证据登记为依赖面（044 复用）",
     },
    {"probe": "gkx 同步/异常面（sync/cycle/frequen/watermark 词族）",
     "source": "gkx",
     "sql": "词族扫描（共享探针 gkx_sync_tables=[]）",
     "hits": 0,
     "hit_detail": "280 表 0 命中（要素明细库无运行日志面）",
     },
    {"probe": "久新同步面（sync/cycle/frequen/watermark/update 词族）",
     "source": "jiuxin",
     "sql": "词族扫描（共享探针 jiuxin_sync_tables）",
     "hits": 2,
     "hit_detail": "命中 ads_research_problem_update_signal / ads_scientific_update_signal——"
                   "科研问题/科学数据的更新信号面（研究对象=科研内容更新非平台同步任务），"
                   "语义排除",
     },
    {"probe": "需求原文「同步异常/异常数」指标定义",
     "source": "doc",
     "sql": "rg 检索三份需求真源",
     "hits": 0,
     "hit_detail": "「异常数」为 UI 图例（:112）/「异常归档」为 Statistic 题名（:305）；"
                   "seq 362 功能句「动态跟踪……异常情况的历史变化」在——异常判定标准"
                   "（何种状态算异常）、计数口径（次数/任务数/记录数）、期定义均无",
     },
]

support = "完全不支持"

notes += [
    "判档：「同步异常数（期）」= 期内异常运行次数——需逐次运行日志；dev xxl 三表全空载体、"
    "es_sync_watermark 是单笔状态快照非序列（无失败历史）、gkx 0 命中、久新 2 张语义排除、"
    "「期」维全库无承载（041 同法）→ 完全不支持",
    "本件新探针（状态三列实查）：es_sync_watermark 有 sync_status/error_msg/retry_count——"
    "排除 demo 模块后 14 模块 13 success + 1 failed（reg_info：RuntimeError: reg_info slice "
    "has 50000 build/bulk errors，retry 1；demo 模块 reg_info_demo=success 按纪律排除、"
    "行内披露）→ 模块级「当前异常状态」可读（附带交付键），但单笔状态≠期计数",
    "结构证据层级：xxl_job_log「表存在但数据为空」（列族在零行）；es_sync_watermark "
    "「表存在、状态列在、但序列语义不存在」（单笔快照）——两种缺形态分别登记",
    "mock 披露：trend.anomalyCount 6 点单调递减（18→8）+ summary 5 条 + byType 四类合计 5——"
    "三组演示值内部自洽（治理改善叙事）但库内无对应承载，不作数据证据（B10）",
    "B11 对账：xxl 三表 0 行与 019 实测一致；es_sync 15 行与 019/046 共证（状态三列为"
    "本批新读数，044 复用）",
    "升档触发器（B10）：①xxl 调度器实装留日志（handle_code≠200 计异常逐次累计）→ "
    "升完全直接支持；②es_sync 改逐次留痕表（模块×时间×状态序列）→ 升完全转换支持；"
    "③维持现状 → 完全不支持（UI 异常位建议暂无数据态；当前状态读数可作即期监控参考）",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_043",
    "batch": "S3-05",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/components/AccessHistorySituation.jsx:112",
        "repos/demo-ui-science/src/pages/data-resources/components/AccessHistorySituation.jsx:305",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:1437",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份需求说明书未出现「同步异常数」。「异常数」为 UI 图例（:112）/「异常归档」"
                "为 Statistic 题名（:305）；挂靠 seq 362 功能句「动态跟踪……异常情况的历史变化」"
                "——功能在、异常判定标准/计数口径/期定义无",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "期序列不可构建（无逐次运行日志面）",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "5", "18", "8", "0", "15", "14", "13", "1", "542", "280", "215"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

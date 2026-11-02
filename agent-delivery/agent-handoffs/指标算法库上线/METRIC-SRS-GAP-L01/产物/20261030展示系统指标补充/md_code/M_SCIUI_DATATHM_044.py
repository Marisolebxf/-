#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_044 数据更新成功率 · 三源探针与复现脚本（S3-05 L1）。

含义：接入视窗·历史资源接入情况——「更新成功率%」逐期折线+「历史成功率」
汇总读数+渠道级成功率（updateCycleStats.successRate）。UI：
- AccessHistorySituation.jsx:104（series name='更新成功率%' line）
- :296-301（Statistic 历史成功率 summary.successRate=75.0）
- :416-421（历史更新周期统计 Tab 成功率 Progress 列）
mock 源 mockData.js:1433/1428 + :1451-1456 updateCycleStats。

判档路径（口径=「数据更新（同步）运行成功次数/总运行次数」）：
- 分子分母原料=逐次运行日志（同 043）——xxl 三表 0 行、es_sync 单笔快照；
- es_sync 状态三列可算「模块级成功率快照」：13 success/14 模块=92.86%
  （排除 demo；043 状态分布复用）——但这是「模块当前状态成功率」非
  「运行次数成功率」（每模块只 1 笔）；
- mock 内部失配：summary.successRate=75.0（9/12 状态口径：success 7+partial 3
  +failed 2 的 updateStatus 饼图合计 12，7/12=58.3%、(7+3)/12=83.3% 均非 75）
  ——演示值内部不闭合；
→ 完全不支持（运行次数口径的分子分母三源无日志面）。
  附带交付：模块级状态成功率快照 92.86%（13/14，标签「非运行次数口径」）。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_044_out.json")
PROBE = os.path.join(BASE, "_probe_s305_l1_out.json")

facts, derived, notes, absence = {}, [], [], []
probe = json.load(open(PROBE, encoding="utf-8"))["probes"]

# ============ ① 空载体与词族（共享探针复用） ============
facts["dev_table_total"] = probe["dev_table_total"]
facts["dev_xxl_job_log_rows"] = probe["dev_xxl_job_log_rows"]      # 0
facts["dev_xxl_job_info_rows"] = probe["dev_xxl_job_info_rows"]    # 0
facts["dev_es_sync_row_count"] = probe["dev_es_sync_row_count"]    # 15
facts["gkx_table_count"] = probe["gkx_table_count"]
facts["gkx_sync_tables"] = probe["gkx_sync_tables"]                # []
facts["jiuxin_table_count_live"] = probe["jiuxin_table_count_live"]
facts["jiuxin_sync_tables"] = probe["jiuxin_sync_tables"]

# ============ ② es_sync 状态分布（复用 043 本批新探针产物，B11 锚） ============
p043 = json.load(open(os.path.join(BASE, "M_SCIUI_DATATHM_043_out.json"), encoding="utf-8"))
facts["dev_es_sync_status_dist_excl_demo"] = p043["facts"]["dev_es_sync_status_dist_excl_demo"]
facts["dev_es_sync_failed_detail_excl_demo"] = p043["facts"]["dev_es_sync_failed_detail_excl_demo"]
facts["dev_es_sync_demo_modules_disclosed"] = p043["facts"]["dev_es_sync_demo_modules_disclosed"]
dist = dict(facts["dev_es_sync_status_dist_excl_demo"])
success_nd = dist.get("success", 0)
failed_nd = dist.get("failed", 0)
total_nd = success_nd + failed_nd

# ============ ③ mock 对照（含内部失配核验） ============
facts["ui_mock_summary_success_rate"] = 75.0          # summary.successRate
facts["ui_mock_trend_success_rate"] = [94.2, 95.1, 95.8, 96.4, 97.0, 97.5]  # 6 点爬升
facts["ui_mock_update_status_pie"] = [["失败", 2], ["成功", 7], ["部分成功", 3]]  # updateStatus 饼图（名称排序）
_pie = dict(facts["ui_mock_update_status_pie"])
_pie_total = sum(_pie.values())
facts["ui_mock_pie_total"] = _pie_total  # 12
# 内部失配核验（脚本算出）：75.0 与饼图两口径均不闭合
facts["ui_mock_pie_success_only_share_pct"] = round(100.0 * _pie["成功"] / _pie_total, 1)        # 58.3
facts["ui_mock_pie_success_plus_partial_share_pct"] = round(100.0 * (_pie["成功"] + _pie["部分成功"]) / _pie_total, 1)  # 83.3
facts["ui_mock_cycle_success_rates_sorted"] = [
    ["API接口", 98.2], ["数据库同步", 97.8], ["文件传输", 95.6], ["物联网采集", 96.8],
    ["人工录入", 92.3]]  # updateCycleStats 按渠道名排序（本件核验）

# ================= 派生（模块级快照附带 + 运行次数口径负结论） =================
derived.append({
    "key": "sync_success_rate_module_snapshot_pct",
    "value": round(100.0 * success_nd / total_nd, 2),
    "numerator": success_nd,
    "denominator": total_nd,
    "note": "模块级状态快照附带读数（非运行次数口径）：es_sync_watermark 排除 demo 后 "
            + str(total_nd) + " 模块中 success " + str(success_nd) + " 个 = "
            + str(round(100.0 * success_nd / total_nd, 2)) + "%——每模块仅 1 笔当前状态，"
            "「成功率」语义是「当前正常模块占比」非「成功运行次数/总运行次数」",
})
derived.append({
    "key": "data_update_success_rate",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『数据更新成功率』正式口径（成功运行次数/总运行次数）需逐次运行日志"
            "（xxl_job_log 0 行、es_sync 单笔快照无序列）→ 分子分母均不可构建；"
            "按 B10 留空即负结论登记",
})

# ================= absence_probe =================
absence += [
    {"probe": "dev 逐次运行日志（成功/失败次数的分子分母源）",
     "source": "dev",
     "sql": "SELECT COUNT(*) FROM gkxlumenx_job.xxl_job_log（019/043 同锚）",
     "hits": 0,
     "hit_detail": f"xxl_job_log={facts['dev_xxl_job_log_rows']} 行（xxl_job_info 同 0）——"
                   "调度器空载体：成功次数与总次数两计数器均无原料；"
                   "es_sync_watermark 单笔状态（success 13/failed 1，排除 demo）撑不起次数口径",
     },
    {"probe": "gkx 运行成功率面",
     "source": "gkx",
     "sql": "词族扫描（共享探针 gkx_sync_tables=[]）",
     "hits": 0,
     "hit_detail": "280 表 0 命中（要素明细库无运行监控面）",
     },
    {"probe": "久新运行监控面",
     "source": "jiuxin",
     "sql": "词族扫描（共享探针）",
     "hits": 2,
     "hit_detail": "ads_research_problem_update_signal / ads_scientific_update_signal——"
                   "科研内容更新信号面，语义排除（043 同证）",
     },
    {"probe": "需求原文「更新成功率」指标定义",
     "source": "doc",
     "sql": "rg 检索三份需求真源",
     "hits": 1,
     "hit_detail": "「更新成功率」字面三份真源 0 命中（指标名级）；seq 362 功能句"
                   "「动态跟踪接入量、更新成功率与异常情况的历史变化」——「更新成功率」"
                   "功能词在：分子分母口径（运行次数/任务数/记录数）、partial 是否计入成功"
                   "均无定义；UI mock summary 75.0 与饼图（58.3%/83.3% 两口径）内部不闭合",
     },
]

support = "完全不支持"

notes += [
    "判档：成功率=成功运行次数/总运行次数——分子分母同源于逐次运行日志；xxl 三表 0 行"
    "（调度器空载体）、es_sync 单笔快照（无次数语义）、gkx 0 命中、久新 2 张语义排除"
    "→ 完全不支持",
    "附带交付：模块级状态快照成功率 92.86%（13 success/14 模块，排除 demo；043 状态分布"
    "复用）——语义=「当前正常模块占比」，不得标「数据更新成功率」对外",
    "mock 内部失配（本件核验）：summary.successRate=75.0 vs updateStatus 饼图两口径"
    "（7/12=58.3%、(7+3)/12=83.3%）均不闭合——演示值自身没对账；trend 6 点爬升"
    "（94.2→97.5）为治理改善叙事，不作数据证据（B10）",
    "口径缺口：partial（部分成功）是否计入成功——mock 袋 summary 75.0 无法从 12 条状态"
    "推出任何一种口径的整值，说明前端未定义；正式口径须先裁定（R1 质量评价框架先行）",
    "B11 对账：状态分布/failed 明细复用 043 本批产物（同源零漂移）；xxl=019；词族=共享探针",
    "升档触发器（B10）：①xxl 调度器实装留日志（成功次数=handle_code=200 计数）→ "
    "升完全直接支持；②es_sync 逐次留痕 → 升完全转换支持（模块级粒度+partial 口径先裁）；"
    "③维持现状 → 完全不支持（UI 成功率位建议暂无数据态）",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_044",
    "batch": "S3-05",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/components/AccessHistorySituation.jsx:104",
        "repos/demo-ui-science/src/pages/data-resources/components/AccessHistorySituation.jsx:296",
        "repos/demo-ui-science/src/pages/data-resources/components/AccessHistorySituation.jsx:416",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:1451",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "指标名级三份真源 0 命中；seq 362 功能句含「更新成功率」功能词（动态跟踪"
                "……更新成功率……历史变化）——分子分母口径与 partial 计入规则无定义",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "成功率序列不可构建（无运行日志面）",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "75", "58.3", "83.3", "94.2", "97.5", "13", "14", "92.86", "0",
        "542", "280", "215"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

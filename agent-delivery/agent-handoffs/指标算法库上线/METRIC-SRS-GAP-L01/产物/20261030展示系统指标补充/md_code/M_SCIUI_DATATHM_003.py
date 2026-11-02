#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_003 科研项目评估 · 三源探针脚本（S3-04 L6）。

含义：数据资源·应用视窗·业务应用调用数据详情的「科研项目评估」业务应用
——作为业务应用名出现在调用统计语境（mock 挂载 mockData.js:1594 businessCallTrend.datasets[0]：
六个月 72,000→102,000 调用序列；另见 :990 businessApplicationStats ba-001 calls 523,000、
:1010 调用日志、:1525 字段级使用明细、:899 资产业务模块）。
注意：本件名「科研项目评估」在 UI 全部出现点均为【调用统计语境下的业务应用名】，
非「科研项目绩效评估」指标本身——语义判定须先过这一关（本件实测确认）。

判档路径（口径分两层）：
- 层1（调用语境·业务应用调用量）：与 032/034/035 同根——资产/应用×调用量台账三源零承载 → 完全不支持；
- 层2（若甲方裁定为科研项目绩效评估面）：gkx 有真实项目表族（dwd_zh_project 58,453 条 NSFC
  + dwd_zh_project_output 20,133 条成果；久新 ads_project_profile 1,838,841 条海外画像）——
  项目存量面结构+数据双在，但「评估」（绩效评分/结题结论）维三源无承载（无评估结果面）→
  该层为部分支持（存量可数、评估缺位）。
主判定取层1（UI 挂载语境）：完全不支持；层2 作为口径裁定备选路径登记（B10 双口径并列）。
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_003_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_probe_s304_l6_heat_out.json")

facts, derived, notes, absence = {}, [], [], []
probe = json.load(open(SNAP, encoding="utf-8"))["probes"]

# ============ ① dev：调用词族复核（层1 判据，与族件同证） ============
facts["dev_call_rank_heat_tables"] = probe["dev_call_rank_heat_tables"]
facts["dev_call_rank_heat_table_rows"] = probe["dev_call_rank_heat_table_rows"]
facts["dev_table_total"] = probe["dev_table_total"]
facts["dev_project_tables"] = probe["dev_project_tables"]  # enterprise_fund_project/fund_project/pay_refund_order

# ============ ② gkx：项目表族真实承载（层2 判据） ============
facts["gkx_project_tables"] = probe["gkx_project_tables"]
facts["gkx_project_main_rows"] = probe["gkx_project_main_rows"]
facts["gkx_zh_project_approval_year_dist_top"] = probe["gkx_zh_project_approval_year_dist"][-6:]
facts["gkx_zh_project_source_top"] = probe["gkx_zh_project_source_top"]
facts["gkx_zh_project_output_positive_rows"] = probe["gkx_zh_project_output_positive_rows"]
facts["gkx_zh_project_output_join_sample"] = probe["gkx_zh_project_output_join_sample"]
facts["gkx_call_rank_heat_tables"] = probe["gkx_call_rank_heat_tables"]

# ============ ③ 久新：项目画像面（层2 判据）+ 调用词族（层1） ============
facts["jiuxin_probe_mode"] = probe["jiuxin_probe_mode"]
facts["jiuxin_table_count_live"] = probe["jiuxin_table_count_live"]
facts["jiuxin_project_table_rows"] = probe["jiuxin_project_table_rows"]
facts["jiuxin_ads_project_profile_rows"] = probe["jiuxin_ads_project_profile_rows"]
facts["jiuxin_ads_project_profile_name_nonnull"] = probe["jiuxin_ads_project_profile_name_nonnull"]
facts["jiuxin_ads_project_profile_name_zh_nonnull"] = probe["jiuxin_ads_project_profile_name_zh_nonnull"]
facts["jiuxin_ads_project_profile_start_year_nonnull"] = probe["jiuxin_ads_project_profile_start_year_nonnull"]
facts["jiuxin_ads_project_profile_amount_cny_nonnull"] = probe["jiuxin_ads_project_profile_amount_cny_nonnull"]
facts["jiuxin_ads_project_profile_funder_name_nonnull"] = probe["jiuxin_ads_project_profile_funder_name_nonnull"]
facts["jiuxin_ads_project_profile_start_year_dist_top12"] = probe[
    "jiuxin_ads_project_profile_start_year_dist"][:12]
facts["jiuxin_call_rank_heat_tables"] = probe["jiuxin_call_rank_heat_tables"]

# ================= 派生（B10 双口径登记） =================
# 层2 备选口径的可算派生：gkx NSFC 项目成果覆盖
derived.append({
    "key": "gkx_zh_project_output_coverage_pct",
    "value": round(probe["gkx_zh_project_output_positive_rows"]
                   / probe["gkx_project_main_rows"]["dwd_zh_project"] * 100, 2),
    "numerator": probe["gkx_zh_project_output_positive_rows"],
    "denominator": probe["gkx_project_main_rows"]["dwd_zh_project"],
    "note": "分子=gkx dwd_zh_project_output 中 total_outputs>0 行数（8,601）；分母=gkx dwd_zh_project"
            " 全表行数（58,453，NSFC 单一来源）；同源同库（gkx），语义=『有正向成果登记的项目占比』"
            "——层2 备选口径的成果维覆盖读数，非指标值本身",
})
derived.append({
    "key": "jiuxin_ads_project_profile_start_year_coverage_pct",
    "value": round(probe["jiuxin_ads_project_profile_start_year_nonnull"]
                   / probe["jiuxin_ads_project_profile_rows"] * 100, 2),
    "numerator": probe["jiuxin_ads_project_profile_start_year_nonnull"],
    "denominator": probe["jiuxin_ads_project_profile_rows"],
    "note": "分子=久新 ads_project_profile 中 start_year 非 NULL 行数（74,144）；分母=同表全表行数"
            "（1,838,841）；同源同表，语义=『项目画像年份维覆盖率』——层2 备选口径的时间维质量披露"
            "（4.03%，年份维高度稀疏）",
})
derived.append({
    "key": "scientific_project_evaluation_score",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "主口径（UI 挂载语境=业务应用调用量）：科研项目评估作为业务应用的调用量统计"
            "（mock 523,000/月序列 72,000→102,000）——三源调用台账零承载 → 不可构建，B10 留空；"
            "层2 备选口径（科研项目绩效评估）：评估结果面（评分/结题结论）三源亦无承载"
            "（gkx/久新只有项目存量与成果计数，无评估结论字段），评估维同样不可构建",
})

# ================= absence_probe =================
absence += [
    {"probe": "dev 业务应用调用台账（call/invoke/usage/rank/heat/hot/trend/ranking 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表）+ 命中表 COUNT 复核",
     "hits": 0,
     "hit_detail": "词族命中 5 张全部语义排除且 0 行（chain_hotspot/enterprise_ranking/"
                   "industry_chain_graph_snapshot/enterprise_growth_trend/policy_support_rank）"
                   "——无业务应用×调用量台账；dev 项目词族命中 enterprise_fund_project（0 行）/"
                   "fund_project（0 行）/pay_refund_order（支付退款，语义排除）——dev 侧项目面也是空壳",
     },
    {"probe": "gkx 业务应用调用台账 + 科研项目评估结果面",
     "source": "gkx",
     "sql": "information_schema.tables 扫 gkx（280 表）：call/rank 词族 + project 表族列结构核对",
     "hits": 0,
     "hit_detail": "调用词族 0 命中；项目表族（dwd_zh_project 58,453 NSFC/dwd_zh_project_output "
                   "20,133/dwd_en_project 20,000 等）列为 project_number/title/funded_institution/"
                   "funded_amount/discipline/approval_year 等登记字段——无评估结论字段"
                   "（评分/等级/结题意见），存量面在而评估面无",
     },
    {"probe": "久新业务应用调用台账 + 项目评估语义面",
     "source": "jiuxin",
     "sql": "SHOW TABLES（活库 212 表）词族扫 + ads_project_profile 字段有效率核对",
     "hits": 0,
     "hit_detail": "调用词族 14 张命中全语义排除（科研问题/技术热度）；项目画像 "
                   "ads_project_profile 1,838,841 行（OpenAlex 资助画像，funder_name 有效 "
                   "1,838,841）但 name_zh 0/start_year 74,144（4.03%）/amount_cny 160,822（8.75%）"
                   "——画像字段高度稀疏且无评估结论面；ads_research_problem_potential_assessment"
                   "（812 行）是『科研问题潜力评估』非『科研项目评估』，语义排除；探测模式 live",
     },
    {"probe": "需求原文「科研项目评估」立项检索",
     "source": "doc",
     "sql": "rg 科研项目评估 三份需求真源 + UI 全仓",
     "hits": 0,
     "hit_detail": "三份需求真源（主需求/SRS 四视窗/核增/算法库）均未出现「科研项目评估」指标名或"
                   "功能叶——UI 全部 9 处出现点均为 mock 调用统计语境的业务应用名/业务模块名"
                   "（mockData.js:1594 businessCallTrend/:990 businessApplicationStats/:1010 调用日志/"
                   ":1525 字段使用明细/:899 资产业务模块/:1000 部门归集），无独立需求叶",
     },
]

support = "完全不支持"

notes += [
    "判档（主口径=UI 挂载语境）：「科研项目评估」是业务应用调用统计语境下的应用名——mock "
    "businessCallTrend.datasets[0] 六个月 72,000→102,000 调用序列，其承载前提是业务应用×调用量"
    "台账，三源词族 0 命中 → 完全不支持（与 032/034/035 同根同判，独立留证）",
    "层2 备选口径披露（B10 双口径并列）：若甲方裁定本件为「科研项目绩效评估」面——gkx 有真实"
    "项目存量（dwd_zh_project 58,453 条 NSFC 全量+成果面 20,133），久新有海外项目画像"
    "（ads_project_profile 1,838,841）；但「评估」维（评分/结题结论/绩效等级）三源均无承载——"
    "该口径下为部分支持（存量可数、评估缺位）；权威评估框架（R1 科技部综合绩效评价：任务书"
    "目标/代表性成果/成果转化/人才培养四维）要求的任务书与评审材料面三源皆无",
    "gkx 项目存量质量：NSFC 单一来源（58,453/58,453=100%），approval_year 覆盖 1986-2023 连续；"
    "成果面 join 覆盖好（前 2 万抽样 19,989 命中）但 total_outputs>0 仅 8,601（"
    "gkx_zh_project_output_coverage_pct=14.71%）——成果维半稀疏",
    "久新项目画像质量：funder_name 100% 有效但 name_zh 0 行、start_year 仅 4.03%、amount_cny "
    "8.75%——OpenAlex 海外资助画像的中文侧与时间/金额维高度稀疏，作画像参考可、作评估底数不足",
    "mock 披露：mockData.js:1594（businessCallTrend 科研项目评估序列）/:990（businessApplicationStats "
    "calls 523,000）——演示值，不作数据证据（B10）；且 UI 注释自标需规 seq 397（业务应用调用"
    "数据详情）语境",
    "B11 对账：调用词族与 L5/L6 族探针一致；gkx 项目行数走 00:19 计数缓存+live 复核；"
    "久新 212 表 live 实测",
    "升档触发器（B10）：①调用台账接入 → 主口径升完全直接支持（族级共用）；②甲方裁定为绩效评估面"
    "+评估结果面立项（或采用成果代理口径）→ 层2 升部分支持→成果代理可转换；③维持现状 → 完全不支持",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_003",
    "batch": "S3-04",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:1594",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:990",
        "repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:853",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份需求真源均未出现「科研项目评估」指标名/功能叶；UI 9 处出现点均为 mock "
                "调用统计语境的业务应用名（seq 397 业务应用调用数据详情语境），无独立需求叶",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": ["1986-2023"],
    "base_years_missing": [],
    "base_years_note": "层2 备选口径 gkx NSFC approval_year 1986-2023 连续；久新 start_year 仅 4.03% 覆盖",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["58453", "20133", "8601", "1838841", "74144", "160822", "523000", "102000"][:8]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

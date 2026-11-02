#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INCUB_028 成果热度值（heat，成果被关注程度排序键）· 三源探针脚本（S3-07 L3）。

含义：①软科学成果展示「热门成果」栏的排序键「热度」（value 字符串「热度 9.4」，
parseHeatValue 提取数值降序）；②政策跟踪热点问题看板的热度条（hotIssuesData
heat 95/88…0-100 分）。三挂载点：SoftScienceResultsRail.jsx:72（排序 Tab heat）/
__tests__:141（排序测试）/ HotIssueDiagnosisBoard.jsx:39（热度条形图 value）。

判档路径（口径 = 成果被关注程度加权分，权威参照 Altmetric Attention Score
加权聚合法）：
- ①成果互动行为流（阅读/收藏/点赞）——dev：无成果互动面（app_article_collect 0 行
  小程序文章收藏；cms 无成果互动表；软科学课题成果主档本身无表，同 INCUB_022）；
- ②政策议题热度——dev：policy_intensity 0 行/policy_focus 0 行（政策强度/聚焦
  预留面空壳）；久新 ads_research_problem_heat_component（2,842 行）是「难题热度
  分量」最近邻——problem_id 维的 component_score/weighted_contribution 加权结构，
  语义为科研难题热度非政策议题/成果热度，语义排除但结构范式可引；
- gkx：heat/hot 词族 0 命中（280 表）；
- mock 侧「热度 9.4」为手写字符串常数（readCount 118/favoriteCount 13 并列展示
  但 parseHeatValue 只读 value 字段——无计算关系）；
- 判完全不支持（成果互动行为流与热度结果面三源均无法构建）。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_INCUB_028_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s307_l3_incub_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")

facts, derived, notes, absence = {}, [], [], []
probe = json.load(open(PROBE, encoding="utf-8"))
snap = json.load(open(SNAP, encoding="utf-8"))

# ============ ① mock 层（UI 语义披露，不作数据证据） ============
MOCK_HOT_RESULTS_HEAT = ["9.4", "8.9", "8.6", "8.1", "7.9", "7.8", "7.7", "7.6", "7.5"]
MOCK_POLICY_HEAT = [95, 88]  # hotIssuesData 前2（0-100 整数分）
facts["ui_mounts"] = [
    "SoftScienceResultsRail.jsx:72（RESULT_SORT_OPTIONS heat Tab「热度」默认排序）+ :79 parseHeatValue（从「热度 9.4」字符串提取数值）+ :100 sortHotResultsByMode 降序",
    "soft-science/components/__tests__/SoftScienceResultsRail.test.jsx:141（热度→影响力切换测试）",
    "policy-tracking/analysis/interpret/HotIssueDiagnosisBoard.jsx:39（issues.map i.heat 条形图 value，xAxis max=100 name=热度）",
]
facts["ui_mock_result_heat_values"] = MOCK_HOT_RESULTS_HEAT
facts["ui_mock_result_readcounts"] = [118, 104, 96, 87, 82, 79, 73, 70, 68]
facts["ui_mock_result_favoritecounts"] = [13, 12, 11, 9, 9, 8, 8, 7, 7]
facts["ui_mock_policy_heat_values_head"] = MOCK_POLICY_HEAT
facts["ui_mock_semantics_note"] = ("mock「热度 9.4」是 value 字符串手写常数（1-10 量表）；readCount/favoriteCount 并列展示但 parseHeatValue 只读 value——"
                                   "演示层热度与互动计数无计算关系；政策侧 heat 95/88 为 0-100 整数分（trendNote「近 4 周热度 +18%」亦手写）")

# ============ ② dev ============
dev = probe["dev"]
facts["dev_table_total"] = dev["table_total"]
facts["dev_heat_word_tables"] = dev["word_heat"]
facts["dev_heat_hits_note"] = "heat/hot 词族 2 命中：ads.chain_hotspot（0 行，产业链热点预留面）/ads.industry_chain_graph_snapshot（0 行）——均非成果热度"
snap_rows = {}
for sch in ["gkxlumenx_ads", "gkxlumenx_dwd"]:
    for t, n in snap["dev"]["schemas"][sch]:
        if t in ("policy_intensity", "policy_focus", "policy_public_opinion", "policy_favorite"):
            snap_rows[f"{sch}.{t}"] = n
facts["dev_policy_heat_candidate_rows"] = snap_rows
facts["dev_interaction_note"] = ("成果互动行为流无表：app.app_article_collect 0 行（小程序文章收藏，语义亦非课题成果）；"
                                 "cms 无成果互动表；软科学课题成果主档本身无表（INCUB_022 已证，本件独立留证）")

# ============ ③ gkx ============
facts["gkx_table_count"] = probe["gkx"]["table_count"]
facts["gkx_heat_word_tables"] = probe["gkx"]["word_hits"]["heat"]

# ============ ④ 久新 ============
jx = probe["jiuxin"]
facts["jiuxin_table_count_live"] = jx["table_count_live"]
facts["jiuxin_heat_word_tables_head"] = sorted(jx["word_hits"]["heat"])[:8]
facts["jiuxin_heat_component_cols"] = jx.get("ads_research_problem_heat_component_cols", [])
facts["jiuxin_heat_component_rows_snapshot"] = snap["jiuxin"]["rowcounts"].get("ads_research_problem_heat_component", 0)
facts["jiuxin_hotspot_yearly_cols_head"] = [c for c in jx.get("ads_technology_hotspot_yearly_cols", []) if c in ("hotspot_score", "hotspot_score_yoy_change", "paper_activity_score", "citation_attention_score")]
facts["jiuxin_semantics_note"] = ("久新热度族语义辨析：ads_research_problem_heat_component（2,842 行快照）=科研难题热度分量"
                                  "（problem_id×component_score×weighted_contribution 加权结构——本件结构范式可引）；"
                                  "ads_technology_hotspot_yearly=技术热点年度分（hotspot_score/citation_attention_score）——"
                                  "均为难题/技术维度，无成果互动热度与政策议题热度语义")

# ============ ⑤ 需求溯源 ============
facts["srs_anchor"] = ("成果侧：SRS 软科学成果展示.md「成果互动与传播中心·互动统计与传播分析」（互动行为、传播数据与影响评价相结合）+ 主需求 :3337 同文；"
                       "政策侧：SRS 科技政策跟踪·热点问题分析看板（Bid §4.2.2.2.1 / E4 规则 Mock 打标——组件注释自认）")
facts["named_in_srs"] = False
facts["named_note"] = "「热度值/热度」作为指标名在三份说明书与主需求未单独出现（「热度」14 处均为图表伴随词——技术热度分布图/热度指数等）；两挂载侧均为排序键/条形值语义"

# ============ ⑥ 权威口径 ============
facts["authoritative_reference"] = ("Altmetric Attention Score：自动化加权聚合（非原始提及计数）——按来源类型赋权"
                                    "（博客 8/政策文件 3/专利 3/维基 3/X 0.25/Facebook 0.25），每人每源只计一次，取整呈现；"
                                    "成果热度=关注度的加权近似，非质量度量——本件语义最近邻")

# ============ ⑦ absence_probe ============
absence = [
    {"probe": "dev 成果互动行为流（阅读/收藏/点赞，热度计算输入）",
     "source": "dev", "sql": "heat/hot 词族扫 542 表 + 互动面语义核",
     "hits": 2,
     "hit_detail": "chain_hotspot/industry_chain_graph_snapshot 均 0 行产业链预留面；互动面 app_article_collect 0 行且为小程序文章收藏语义；成果主档无表（INCUB_022 结论独立复核）——热度输入维缺失"},
    {"probe": "dev 政策议题热度面（policy_intensity/policy_focus/public_opinion）",
     "source": "dev", "sql": "SELECT COUNT(*) 快照复核",
     "hits": 0,
     "hit_detail": "policy_intensity 0 行/policy_focus 0 行/policy_public_opinion 0 行——政策热度预留面全空壳；HotIssueDiagnosisBoard 数据来自 policyData.js 手写 hotIssuesData（组件注释自认 Mock 打标）"},
    {"probe": "gkx 热度面（heat/hot/attention 词族，280 表）",
     "source": "gkx", "sql": "information_schema.tables 扫 gkx",
     "hits": 0, "hit_detail": "0 命中——gkx 为要素库，无互动/热度聚合面"},
    {"probe": "久新热度面（heat/hot 词族+语义核，live 218 表复核）",
     "source": "jiuxin", "sql": "SHOW TABLES 词族过滤 + heat_component 列实读",
     "hits": 12,
     "hit_detail": "热度族全为难题/技术/主题维度：heat_component（难题热度分量 2,842 行）、hotspot_snapshot/signal（技术热点）、emerging_topic_snapshot（新兴主题）——无成果互动热度与政策议题热度语义；结构范式（component_score×weight 加权）可引"},
    {"probe": "需求原文热度定义段",
     "source": "doc", "sql": "rg 热度 三份说明书+主需求",
     "hits": 14,
     "hit_detail": "主需求 14 处「热度」全为图表伴随词（技术热度分布图 :399/热度指数 :1103/人才分布热度 :1565 等），无热度值计算口径定义；成果互动侧仅「互动统计与传播分析」功能分句"},
]

# ============ ⑧ derived ============
derived = [
    {"key": "result_heat_score", "value": None, "numerator": None, "denominator": None,
     "note": "『成果热度值』=成果被关注程度加权分（Altmetric 式来源加权聚合）。需成果互动行为流——dev 互动面 0 行+成果主档无表；gkx 0 命中；久新热度族全为难题/技术维 → 不可构建，按 B10 留空即负结论登记"},
    {"key": "policy_issue_heat_score", "value": None, "numerator": None, "denominator": None,
     "note": "『政策议题热度』（第二挂载侧）需政策舆情/检索行为流——dev 政策热度预留面三表全 0 行；久新无政策议题维 → 不可构建（与成果侧同判）"},
]

notes = [
    "判档：热度双层输入（成果互动流/政策舆情流）三源均无法构建 → 完全不支持（两挂载侧同判）",
    "权威口径（R1 Altmetric）：注意力分=来源类型加权聚合（博客 8/政策 3/维基 3/X 0.25），每人每源一次、取整呈现；明确「是关注度近似非质量度量」——本件 1-10 量表与 0-100 分两 UI 形态均为平台自定",
    "mock 披露：成果侧「热度 9.4」字符串手写（readCount 118/favoriteCount 13 并列不联动——parseHeatValue 只读 value 字段）；政策侧 heat 95/88 整数分（组件注释自认 Bid §4.2.2.2.1 / E4 规则 Mock 打标）",
    "范式可引：久新 ads_research_problem_heat_component 的「component_score×component_weight→weighted_contribution」三层加权结构是本件热度模型的形态参照（语义为难题维度）；ads_talent_profile 的 paper_score/citation_score 归一化范式亦可引",
    "同族件关系：INCUB_022（成果总览报表）共享「软科学课题成果主档无表」上游结论；SOFTSCI 族（L2 批）共享软科学页语义；政策侧与 POLICY 族件（他批）共享 policy_intensity 空壳结论（本件独立留证）",
    "升档路径：成果互动行为流落库（阅读/收藏/点赞事件表）→ Altmetric 式加权热度 run → 完全转换支持；课题成果主档是上游前提",
]

out = {
    "metric_id": "M_SCIUI_INCUB_028",
    "batch": "S3-07",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/achievement-preview/modules/soft-science/components/SoftScienceResultsRail.jsx:72",
        "repos/demo-ui-science/src/pages/achievement-preview/modules/soft-science/components/__tests__/SoftScienceResultsRail.test.jsx:141",
        "repos/demo-ui-science/src/pages/policy-tracking/analysis/interpret/HotIssueDiagnosisBoard.jsx:39",
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:484",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「热度值」指标名三份说明书未出现；主需求「热度」14 处均为图表伴随词；语义锚①软科学·互动统计与传播分析（主需求 :3337）②政策跟踪·热点问题分析看板（组件注释自认 Mock 打标）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": "完全不支持",
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["无年度基期维（热度为滚动关注度截面，mock trendNote「近 4 周热度 +18%」为手写演示）"],
    "base_years_note": "热度是滚动窗口注意力量（Altmetric 无固定基期概念）；三源无承载无基期可言；非「缺年按 0 摊入」",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": ["9.4", "8.9", "8.6", "8.1", "7.9", "7.8", "7.7", "7.6", "7.5", "95", "88", "100", "118", "13", "2842", "0", "8", "3", "0.25", "14", "542", "280", "218"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", OUT)
print("support_judgment:", out["support_judgment"])

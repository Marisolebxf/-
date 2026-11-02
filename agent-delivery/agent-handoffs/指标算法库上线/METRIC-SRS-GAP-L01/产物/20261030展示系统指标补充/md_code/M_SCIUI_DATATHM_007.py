#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_007 可靠性上期占比（环比基期）· 三源探针脚本（S3-04 L7）。

含义：科技数据资源·总体视窗·资源来源分析（需规 seq 331）「结构组成环比对比」图的
『上期占比』条（getCompareOption series name='上期占比'，ResourceSourceAnalysisDetail.jsx:156-162）。
UI mock：structureCompare.previousPeriod='2026-04' 五来源类型 previous 值
（国内数据库 20.1% / 国外数据库 14.6% / 科研院所 28.5% / 企业 15.8% / 开源平台 16.2%）——演示值。
UI：repos/demo-ui-science/src/pages/data-resources/components/ResourceSourceAnalysisDetail.jsx:139
（getCompareOption 图例 legend ['当前占比','上期占比']）。

判档路径（口径=「数据源可靠性评估 ≥阈值 档资源数 ÷ 评估范围资源总数，按来源类型分列，取环比基期」）：
- 语义前提核：本组件族是「mock 演示面」——五来源类型/reliability 评分/环比 delta 全部硬编码于
  mockData.js overviewSourceAnalysis，无任何后端接口；但组件注释自标需规 seq 331（功能需求真源在）；
- 直接承载（来源可靠性评估面：来源类型×评分×期）：三源词族（reliability/credible/trust/quality_monitor/
  data_quality/dq_/quality_check/quality_score）——dev 0 张 / gkx 0 张 / 久新 0 张（L7 族探针在案）；
- 结构相近语义排除：gkx dwd_scholar 等要素表无来源可靠性评分列；久新 ads_* 无来源级评估面；
- 分母侧（来源结构登记）同缺：无来源类型轴、无评估范围登记（DATAIN_002/003 来源轴零承载族内同结论）；
- 期维（环比基期）：评估快照/分期管理面三源 0 命中——单期都没有，基期更无从取；
- 判完全不支持（评分面+分母登记+期维三依赖全缺，指标及关键依赖三源均无法构建）。

B11 锚：三源表数 542/280/210（_lane7_shared_probe_out.json）；
词族命中 = _probe_s304_l7_quality_out.json（本件消费 dev/gkx/jiuxin reliability 三组键）。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_007_out.json")
SNAP7 = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s304_l7_quality_out.json")

snap = json.load(open(SNAP7, encoding="utf-8"))
probe = json.load(open(PROBE, encoding="utf-8"))

facts = {
    # 三源表数（B11 锚：共享快照）
    "dev_table_count": snap["dev"]["schema_table_counts"] and sum(snap["dev"]["schema_table_counts"].values()),
    "gkx_table_count": snap["gkx"]["table_count"],
    "jiuxin_table_count_snapshot_20261101": len(snap["jiuxin"]["tables"]),
    # 可靠性词族命中（L7 族探针 2026-11-02 实跑）
    "dev_reliability_like_tables": probe["dev_reliability_like_tables"],       # []
    "gkx_reliability_like_tables": probe["gkx_reliability_like_tables"],       # []
    "jiuxin_reliability_like_tables": probe["jiuxin_reliability_like_tables"],  # []
    "jiuxin_probe_mode": probe["jiuxin_status"],  # live
    # UI mock 演示值（结构证据，不作数据源）
    "ui_mock_previous_period": "2026-04",
    "ui_mock_previous_shares_by_type": [
        ["国内数据库", 20.1], ["国外数据库", 14.6], ["科研院所", 28.5],
        ["企业", 15.8], ["开源平台", 16.2]],
    "ui_mock_source_types_defined": 5,
}

derived = [{
    "key": "reliability_high_share_prev_period_pct_by_type",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『上期』来源可靠性达标占比需三依赖：①来源可靠性评估面（评分×来源×期）三源 0 命中；"
            "②来源结构登记（分母）零承载；③评估期次管理（基期快照）零承载——单期读数都不可构建，"
            "基期读数更无从取；UI previous 值为 mock 演示常量（20.1/14.6/28.5/15.8/16.2），不作分子分母。"
            "按 B10 留空即负结论登记（与 DATATHM_008 共用三依赖缺口，族级并项）",
}]

absence_probe = [
    {"probe": "dev 来源可靠性评估面（reliability/credible/trust/quality_monitor/data_quality/dq_/quality_check/quality_score 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表，L7 族探针 2026-11-02 实跑）",
     "hits": 0,
     "hit_detail": "命中 []——0 张；dev 的质量侧承载只有平台操作日志 sys_log（管理日志非数据质量评估，DATATHM_020 已证语义排除），无来源级可靠性评分面"},
    {"probe": "gkx 来源可靠性评估面（同词族）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表）词族扫（经 _gkxdb.py）",
     "hits": 0,
     "hit_detail": "命中 []——gkx 为要素明细库（论文/专利/机构/学者），dwd_* 表无任何来源可靠性评分列；表级元数据 table_data_source 标签轴实测空载（DATAIN_003 已证三表值域）——来源轴本身无值，更无来源×可靠性评分面"},
    {"probe": "久新来源可靠性评估面（同词族）",
     "source": "jiuxin",
     "sql": "SHOW TABLES（2026-11-02 live，212 表）词族扫",
     "hits": 0,
     "hit_detail": "命中 []——ads_* 全部为学科/人才/专利/项目分析结果面（按 metrics_as_of_date 单日快照管理），无来源可靠性评估面；价值词族唯一命中 ads_technology_commercial_value_simulation 是技术商业化价值仿真（语义排除）"},
    {"probe": "评估期次/环比基期管理面（快照分期）",
     "source": "三源",
     "sql": "词族 + 久新 metrics_as_of_date 值域（DATAIN_003 实测单日一期）",
     "hits": 0,
     "hit_detail": "三源均无评估期次登记：久新快照管理形态为单日一期（DATAIN_003 键 jiuxin_talent_yearly_as_of_dist 在案），无逐期评估序列——『上期/基期』在库内无承载"},
    {"probe": "需求原文「来源可靠性」定义段",
     "source": "doc",
     "sql": "rg 可靠性 三份需求真源（主需求/SRS 总体视窗.md/核增）",
     "hits": 3,
     "hit_detail": "主需求 :2493 = SRS 总体视窗.md seq 331（excel_row 334）『详细分析资源来源的结构组成及变化，辅助判断数据质量和来源可靠性』——功能在、『可靠性』判定标准（阈值/维度/期次）无定义；『上期占比』指标名三源 0 命中（附录 A.2 检索记录）"},
]

notes = [
    "判档：来源可靠性『上期占比』需 评分面+来源登记分母+期次管理 三依赖，三源逐一 0 命中（词族探针在案）"
    "→ 指标及关键依赖三源均无法构建 → 完全不支持（与 DATATHM_008 同根，族级并项）",
    "UI 语义核（派单预警处置）：ResourceSourceAnalysisDetail 是总体视窗·资源来源分析区的**评估面组件**"
    "（结构占比饼/趋势/环比对比/质量与可靠性评估卡/智能归纳明细五段），非纯演示页——组件注释自标需规 seq 331，"
    "但当前全部数据来自 mockData.js overviewSourceAnalysis 硬编码（五来源类型/reliability 93-96/环比 delta），"
    "无后端接口——功能需求真源在、数据面是 mock 演示（两层分开表述）",
    "mock 披露：structureCompare.previousPeriod='2026-04'、五来源 previous 值 20.1/14.6/28.5/15.8/16.2"
    "（mockData.js:256-264）——演示常量，不作数据证据（B10）",
    "B11 对账：三源表数 542/280/210 共享快照；词族命中与 _probe_s304_l7_quality_out.json 逐键一致"
    "（jiuxin 2026-11-02 live 复核 212 张，较 2026-11-01 快照 210 张多 2 张新增表，活库增长非口径漂移，纪律『活库表数不写死』在案）",
    "升档触发器（B10）：①建来源可靠性评估面（来源×评分×期次流水）→ 本件与 008 一起升完全直接支持；"
    "②甲方裁定可靠性判定规则（如按来源类型的稽核通过率）且建来源登记分母 → 升完全转换支持（评分可由稽核流水聚合）",
    "权威口径参照（R1 GB/T 36344-2018）：数据质量六维评价（规范性/完整性/准确性/一致性/时效性/可访问性）"
    "均为『满足要求元素数÷被评价元素数』的结构——可靠性若落地也应先定六维稽核规则再算达标占比，阈值无登记则占比无定义",
]

support = "完全不支持"

out = {
    "metric_id": "M_SCIUI_DATATHM_007",
    "batch": "S3-04",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/components/ResourceSourceAnalysisDetail.jsx:139",
        "repos/demo-ui-science/src/pages/data-resources/components/ResourceSourceAnalysisDetail.jsx:156",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:256",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书未出现「可靠性上期占比」指标名；语义锚 seq 331（excel_row 334）"
                "『分析资源来源的结构组成及变化，辅助判断数据质量和来源可靠性』——功能在、定义无",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["环比基期（上期）整体缺承载", "mock 演示基期 2026-04 无库内对应"],
    "base_years_note": "期维三源零承载：无评估期次管理面，『上期/基期』无从取（探针第 4 件）；"
                       "mock 的 2026-04→2026-05 是前端演示约定，不构成库内期次证据",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["542", "280", "210", "212", "20.1", "14.6", "28.5", "15.8", "16.2",
                          "2026-04", "93", "96", "331", "334"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_008 可靠性当前占比（本期）· 三源探针脚本（S3-04 L7）。

含义：科技数据资源·总体视窗·资源来源分析（需规 seq 331）「结构组成环比对比」图的
『当前占比』条（getCompareOption series name='当前占比'，ResourceSourceAnalysisDetail.jsx:147-152）。
UI mock：structureCompare.currentPeriod='2026-05' 五来源类型 current 值
（国内数据库 22.4% / 国外数据库 15.0% / 科研院所 27.1% / 企业 17.2% / 开源平台 18.3%）——演示值。
UI：repos/demo-ui-science/src/pages/data-resources/components/ResourceSourceAnalysisDetail.jsx:139
（getCompareOption 图例 legend ['当前占比','上期占比']）。

判档路径（口径=「数据源可靠性评估 ≥阈值 档资源数 ÷ 评估范围资源总数，按来源类型分列，取当期」）：
与 DATATHM_007 同根（评分面/来源登记分母/期维三依赖三源零承载），差异仅期位：本件取当期
（有单期即可算），007 取基期（需两期序列）。本件探针复用 L7 族快照（词族逐键一致），独立留证：
- dev 542 表 reliability 词族 0 张；gkx 280 表 0 张（标签轴空载 DATAIN_003 在案）；
- 久新 2026-11-02 live 212 表 0 张（价值词族唯一命中 commercial_value_simulation 语义排除）；
- 判完全不支持（三依赖全缺——虽单期即可算，但单期评估面同样不存在）。

B11 锚：三源表数 542/280/210（_lane7_shared_probe_out.json）；
词族命中 = _probe_s304_l7_quality_out.json（与 007 逐键一致，族内零漂移）。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_008_out.json")
SNAP7 = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s304_l7_quality_out.json")
SIB = os.path.join(BASE, "M_SCIUI_DATATHM_007_out.json")  # 族内对账锚

snap = json.load(open(SNAP7, encoding="utf-8"))
probe = json.load(open(PROBE, encoding="utf-8"))
sib = json.load(open(SIB, encoding="utf-8"))

facts = {
    "dev_table_count": sum(snap["dev"]["schema_table_counts"].values()),
    "gkx_table_count": snap["gkx"]["table_count"],
    "jiuxin_table_count_snapshot_20261101": len(snap["jiuxin"]["tables"]),
    # 可靠性词族命中（L7 族探针 2026-11-02 实跑；与 007 同键同值——族内零漂移对账）
    "dev_reliability_like_tables": probe["dev_reliability_like_tables"],
    "gkx_reliability_like_tables": probe["gkx_reliability_like_tables"],
    "jiuxin_reliability_like_tables": probe["jiuxin_reliability_like_tables"],
    "jiuxin_probe_mode": probe["jiuxin_status"],
    # 族内对账（B11）：词族三组键与 007 产物逐一相等
    "cross_check_with_datathm007_identical": (
        probe["dev_reliability_like_tables"] == sib["facts"]["dev_reliability_like_tables"]
        and probe["gkx_reliability_like_tables"] == sib["facts"]["gkx_reliability_like_tables"]
        and probe["jiuxin_reliability_like_tables"] == sib["facts"]["jiuxin_reliability_like_tables"]),
    # UI mock 演示值（结构证据，不作数据源）
    "ui_mock_current_period": "2026-05",
    "ui_mock_current_shares_by_type": [
        ["国内数据库", 22.4], ["国外数据库", 15.0], ["科研院所", 27.1],
        ["企业", 17.2], ["开源平台", 18.3]],
    "ui_mock_source_types_defined": 5,
    # mock 内部一致性核：structureCompare.current 与 sourceTypes.share 同源同值（演示面自洽）
    "ui_mock_current_equals_source_types_share": [22.4, 15.0, 27.1, 17.2, 18.3],
}

derived = [{
    "key": "reliability_high_share_current_period_pct_by_type",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『当期』来源可靠性达标占比需三依赖：①来源可靠性评估面（评分×来源×期）三源 0 命中；"
            "②来源结构登记（分母）零承载（gkx 标签轴空载 DATAIN_003 在案）；③评估期次管理零承载"
            "——本件虽单期即可算，但单期评估面同样不存在；UI current 值为 mock 演示常量"
            "（22.4/15.0/27.1/17.2/18.3），不作分子分母。按 B10 留空即负结论登记"
            "（与 DATATHM_007 同根三依赖缺口，族级并项；本件是族内先升档件——评估面建成即有当期读数）",
}]

absence_probe = [
    {"probe": "dev 来源可靠性评估面（reliability/credible/trust/quality_monitor/data_quality/dq_/quality_check/quality_score 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表，L7 族探针 2026-11-02 实跑）",
     "hits": 0,
     "hit_detail": "命中 []——0 张（与 DATATHM_007 同键同值，族内零漂移）；dev 质量侧唯一相近承载 sys_log 为平台管理操作日志（DATATHM_020 语义排除先例）"},
    {"probe": "gkx 来源可靠性评估面（同词族）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表）词族扫（经 _gkxdb.py）",
     "hits": 0,
     "hit_detail": "命中 []——dwd_* 要素明细表无来源评分列；来源标签轴 table_data_source 实测空载（DATAIN_003 三表值域在案：dwd_scholar 单标签/dwd_zh_paper 100% 无效/dwd_patent 采样全 null）——来源轴无值，来源×可靠性交叉面更不存在"},
    {"probe": "久新来源可靠性评估面（同词族）",
     "source": "jiuxin",
     "sql": "SHOW TABLES（2026-11-02 live，212 表）词族扫",
     "hits": 0,
     "hit_detail": "命中 []——ads_* 全部分析结果面；价值词族唯一命中 ads_technology_commercial_value_simulation（技术商业化价值仿真）语义排除；可靠性评分类面 0 张"},
    {"probe": "评估期次/当期快照管理面",
     "source": "三源",
     "sql": "词族 + 久新 metrics_as_of_date 值域（DATAIN_003 实测单日一期）",
     "hits": 0,
     "hit_detail": "三源均无评估期次登记：久新 metrics_as_of_date 为全库统一快照日（单日一期、非评估期次语义）；dev/gkx 无分期面——『当前期』评估快照在库内无承载"},
    {"probe": "需求原文「来源可靠性」定义段",
     "source": "doc",
     "sql": "rg 可靠性 三份需求真源（主需求/SRS 总体视窗.md/核增）",
     "hits": 3,
     "hit_detail": "主需求 :2493 = SRS seq 331（excel_row 334）『辅助判断数据质量和来源可靠性』——功能在、判定标准（阈值/维度/期次）无定义；『可靠性当前占比』指标名三源 0 命中（附录 A.2 检索记录）"},
]

notes = [
    "判档：来源可靠性『当前占比』与 007 共用三依赖（评分面/来源登记/期维），三源逐一 0 命中"
    "→ 指标及关键依赖三源均无法构建 → 完全不支持；本件与 007 的判档差异在期位：本件单期即可算、"
    "007 需两期——但单期评估面同样不存在，两件同判；升档顺序上本件在先（评估面建成即有当期读数）",
    "UI 语义核：与 007 同一组件（ResourceSourceAnalysisDetail 环比对比卡）的另一条序列"
    "（当前占比 :147-152 蓝彩条 vs 上期占比 :156-162 灰条）；mock 的 current 值与结构组成段的"
    "sourceTypes.share 同源同值（22.4/15.0/27.1/17.2/18.3——演示面自洽，仍不作数据证据）",
    "mock 披露：structureCompare.currentPeriod='2026-05'、五来源 current 值（mockData.js:256-264）"
    "——演示常量（B10）",
    "B11 对账：词族三组键与 M_SCIUI_DATATHM_007_out.json 逐一相等（cross_check_with_datathm007_identical=true）；"
    "三源表数 542/280/210 共享快照；久新 live 212 张较快照多 2 张（活库增长披露，『活库表数不写死』）",
    "升档触发器（B10）：①建来源可靠性评估面（R1 六维规则+稽核流水+当期快照）→ 本件先升完全直接支持"
    "（007 待两期积累）；②甲方裁定判定规则+来源登记分母（人工评估登记）→ 升完全转换支持",
    "权威口径参照（R1 GB/T 36344-2018）：六维评价均按『满足要求元素数÷被评价元素数』——"
    "当期达标占比是国标原生形态，落地前置是规则库与阈值登记",
]

support = "完全不支持"

out = {
    "metric_id": "M_SCIUI_DATATHM_008",
    "batch": "S3-04",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/components/ResourceSourceAnalysisDetail.jsx:139",
        "repos/demo-ui-science/src/pages/data-resources/components/ResourceSourceAnalysisDetail.jsx:147",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:256",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书未出现「可靠性当前占比」指标名；语义锚 seq 331（excel_row 334）"
                "『分析资源来源的结构组成及变化，辅助判断数据质量和来源可靠性』——功能在、定义无",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["当期评估快照整体缺承载", "mock 演示当期 2026-05 无库内对应"],
    "base_years_note": "期维三源零承载（探针第 4 件）；mock 的 2026-05 是前端演示约定，"
                       "不构成库内期次证据；本件不依赖基期（单期即可算），期维缺口指『当期快照面』",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["542", "280", "210", "212", "22.4", "15.0", "27.1", "17.2", "18.3",
                          "2026-05", "331", "334"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

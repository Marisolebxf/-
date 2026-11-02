#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INCUB_015 供需匹配率（载体-企业→政策资源匹配率）· 三源探针脚本（S3-07 L3）。

含义：创新载体孵化载体页 KPI「政策匹配率」与匹配面板分——载体当前可匹配政策资源
的比率（%）。UI：IncubationCarrierPage.jsx:114（KPI averageMatch）/ :254（匹配对象
面板「匹配率」）/ :627（SoftMatchResultPanel score）。mock 源 incubationCarrierMock.js
carriers[].policyMatchRate（92/86/79/74，4 载体均值 82.75→KPI 显示 83%）。

判档路径（口径 = 载体画像标签 × 政策适配条件 的匹配命中面）：
- 计算前提是「政策资源库（适配条件结构化）+ 载体/企业画像（标签面）+ 匹配结果面」
  三层之一承载——三源探针：
  dev：词族命中 6 表全为产业链/政策推荐空壳（ads.policy_match 0 行：结构面齐
  match_score/rank_no/model_version 但无数据；dwd.policy_layout_recommend /
  policy_recommendation_report 均 0 行）；载体主档 dim.carrier 28 行（v1_approx
  近似源，无标签/需求维）；
  gkx：280 表 incub/match 词族 0 命中（要素库无载体/政策匹配面）；
  久新：218 表 live 复核 incub 0 命中；match 命中 15 表全为「技术/人才/难题推荐」
  （ads_recommendation_* 为论文-人才-技术方向推荐 run，语义为科技要素推荐非
  政策供需匹配）；
- 判完全不支持（政策匹配结果面与两层依赖三源均无法构建）。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_INCUB_015_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s307_l3_incub_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")

facts, derived, notes, absence = {}, [], [], []
probe = json.load(open(PROBE, encoding="utf-8"))
snap = json.load(open(SNAP, encoding="utf-8"))

# ============ ① mock 层（UI 语义披露，不作数据证据） ============
MOCK_POLICY_MATCH_RATES = [92, 86, 79, 74]
facts["ui_mount"] = "IncubationCarrierPage.jsx:114（KPI「政策匹配率」averageMatch）/ :254（匹配对象面板「匹配率」）/ :627（政策匹配 SoftMatchResultPanel score）"
facts["ui_mock_carrier_rates"] = MOCK_POLICY_MATCH_RATES
facts["ui_mock_carrier_names"] = ["南山智造中试平台", "宝安先进制造孵化器", "黄埔生物医药加速器", "中关村硬科技众创空间"]
facts["ui_mock_kpi_value"] = round(sum(MOCK_POLICY_MATCH_RATES) / len(MOCK_POLICY_MATCH_RATES))  # 83
facts["ui_mock_kpi_note"] = "mock 4 载体 policyMatchRate 均值 82.75 四舍五入 83%（演示值，不参与支持度结论）"
facts["ui_mock_panel_scores"] = ["92分", "88分", "84分"]  # policyMatches[].score

# ============ ② dev：匹配面词族探针复核 ============
dev = probe["dev"]
facts["dev_table_total"] = dev["table_total"]
facts["dev_match_word_tables"] = dev["word_match"]
facts["dev_policy_match_cols"] = [c["col"] for c in dev["gkxlumenx_ads.policy_match"]["columns"]]
facts["dev_policy_match_rows"] = dev["gkxlumenx_ads.policy_match"]["rows"]
pm = snap["dev"]["schemas"]
facts["dev_policy_layout_recommend_rows"] = dict(pm["gkxlumenx_dwd"])["policy_layout_recommend"] if isinstance(pm["gkxlumenx_dwd"], list) else None
facts["dev_policy_recommendation_report_rows"] = None
for t, n in pm["gkxlumenx_dwd"]:
    if t == "policy_recommendation_report":
        facts["dev_policy_recommendation_report_rows"] = n
for t, n in pm["gkxlumenx_dwd"]:
    if t == "policy_layout_recommend":
        facts["dev_policy_layout_recommend_rows"] = n
facts["dev_dim_carrier_rows"] = dev["gkxlumenx_dim.carrier"]["rows"]
facts["dev_dim_carrier_cols"] = [c["col"] for c in dev["gkxlumenx_dim.carrier"]["columns"]]
facts["dev_dim_carrier_source_note"] = "dim.carrier 28 行 source=v1_approx（名称/类型/坐标近似主档），无画像标签/需求标签维——匹配计算的前提维缺失"
facts["dev_carrier_rel_rows"] = dev["gkxlumenx_dim.carrier_org_rel"]["rows"]
facts["dev_carrier_index_rows"] = dev["gkxlumenx_ads.carrier_index"]["rows"]

# ============ ③ gkx ============
facts["gkx_table_count"] = probe["gkx"]["table_count"]
facts["gkx_incub_match_word_tables"] = probe["gkx"]["word_hits"]["incub"] + probe["gkx"]["word_hits"]["match"]

# ============ ④ 久新 ============
jx = probe["jiuxin"]
facts["jiuxin_table_count_live"] = jx["table_count_live"]
facts["jiuxin_incub_word_tables"] = jx["word_hits"]["incub"]
facts["jiuxin_match_word_tables"] = jx["word_hits"]["match"]
facts["jiuxin_match_hits_note"] = ("match 词族 15 表全为科技要素推荐（ads_recommendation_* 论文/人才/技术方向推荐 run 与证据链、"
                                   "ads_research_problem_* 难题协同推荐），语义为『论文-人才-技术』推荐非『政策-载体/企业』供需匹配——语义排除")
facts["jiuxin_recommendation_run_cols_sample"] = jx.get("ads_recommendation_run_cols", [])[:8]

# ============ ⑤ 需求溯源 ============
facts["srs_anchor"] = "SRS 创新载体孵化载体.md 序号 549「载体对接政策资源」（平台自动匹配可用政策资源与孵化载体，高亮可申领补贴/辅导/技术支持）+ 主需求 :3717 同文"
facts["named_in_srs"] = False
facts["named_note"] = "「匹配率/供需匹配率」指标名在三份说明书与主需求均未出现；语义锚为序号 549 功能分句（匹配行为有需求、匹配率%口径无定义）"

# ============ ⑥ absence_probe ============
absence = [
    {"probe": "dev 政策匹配结果面（match/recommend 词族，542 表）",
     "source": "dev", "sql": "information_schema.tables 扫 gkxlumenx_*（_probe_s307_l3_incub）",
     "hits": 6,
     "hit_detail": "ads.policy_match / chain_layout_recommend / svc_attraction_recommend / svc_cultivation_recommend / dwd.policy_layout_recommend / dwd.policy_recommendation_report——全部 0 行空壳（policy_match 结构面齐：subject_type/policy_id/match_score/rank_no/model_version，为预留 schema）"},
    {"probe": "dev 载体画像标签维（匹配前提侧）",
     "source": "dev", "sql": "SELECT * FROM gkxlumenx_dim.carrier LIMIT 5 + 列结构",
     "hits": 0,
     "hit_detail": "dim.carrier 28 行仅 name/carrier_type/carrier_level/lng/lat/source(v1_approx)——无行业/规模/资质/需求标签列，政策适配比对无从构建；carrier_org_rel 57 行为载体-机构归属（rel_type=self）"},
    {"probe": "gkx 载体/政策匹配面（incub/match 词族，280 表）",
     "source": "gkx", "sql": "information_schema.tables + columns 扫 gkx",
     "hits": 0,
     "hit_detail": "表名与列名（carrier/instrument 列探）双零命中——gkx 为论文/专利/机构/学者要素库"},
    {"probe": "久新政策供需匹配面（incub/match 词族，live 218 表复核）",
     "source": "jiuxin", "sql": "SHOW TABLES 词族过滤 + DESC 语义核",
     "hits": 15,
     "hit_detail": "incub 0 命中；match 15 表全为 ads_recommendation_*（科技要素推荐 run）与 ads_research_problem_*（难题协同推荐）——推荐对象是论文/人才/技术方向，无政策资源库与载体/企业画像面，语义排除"},
    {"probe": "需求原文「匹配率」定义段",
     "source": "doc", "sql": "rg 匹配率/供需匹配 三份说明书+主需求",
     "hits": 0,
     "hit_detail": "「匹配率」指标名 0 命中；序号 549「载体对接政策资源」与主需求 :3717 仅描述匹配行为（高亮可申领政策红利），比率口径（分子=命中政策数、分母=政策总数或应享政策数）无定义"},
]

# ============ ⑦ derived（负结论留空登记） ============
derived = [
    {"key": "carrier_policy_match_rate", "value": None, "numerator": None, "denominator": None,
     "note": "『供需匹配率（载体-政策）』需「政策资源库适配条件结构化 + 载体画像标签 + 匹配结果面」——dev 匹配面全为 0 行空壳（结构面齐但无数据）、载体主档无标签维；gkx 0 命中；久新 match 命中全为科技要素推荐（语义排除）→ 三源均无法构建，按 B10 留空即负结论登记"},
]

notes = [
    "判档：匹配率三层依赖（政策库结构化/画像标签/匹配结果面）三源均缺——dev ads.policy_match 是唯一结构承载（match_score/rank_no/model_version 列齐）但 0 行且载体侧无标签输入维 → 指标及关键依赖三源均无法构建 → 完全不支持",
    "权威口径参照（R1 科技部火炬中心《科技企业孵化器评价指标体系》2019）：孵化器评价无「政策匹配率」直接指标，服务能力维度考察投融资/导师/中介服务——该指标是 UI 派生读数非法定报表指标；政企匹配业界口径（R2 厦门/黑龙江惠企平台）：匹配率=企业画像标签×政策事项标签比对命中率，兑现率=已兑现/应兑现——需政策库颗粒化拆解+企业标签库两前提",
    "mock 披露：policyMatchRate=[92,86,79,74]（4 载体）KPI 均值 83%、面板 score=92/88/84 分——纯演示值，无算法源（SoftMatchResultPanel「重新匹配」按钮为 900ms setTimeout 假动画）",
    "升档路径：①政策库颗粒化拆解落 dwd.policy_base_info 适配条件列+载体标签面建设 → 匹配 run 落 ads.policy_match（结构已在，插数即活）→ 部分支持；②直接接入深圳市惠企政策「免申即享」平台匹配接口 → 完全直接支持",
]

out = {
    "metric_id": "M_SCIUI_INCUB_015",
    "batch": "S3-07",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/achievement-preview/modules/incubation-carrier/components/IncubationCarrierPage.jsx:114",
        "repos/demo-ui-science/src/pages/achievement-preview/modules/incubation-carrier/components/IncubationCarrierPage.jsx:254",
        "repos/demo-ui-science/src/pages/achievement-preview/modules/incubation-carrier/components/IncubationCarrierPage.jsx:627",
        "repos/demo-ui-science/src/pages/achievement-preview/modules/incubation-carrier/mock/incubationCarrierMock.js:144",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书未出现「供需匹配率/匹配率」指标名；语义锚 SRS 序号 549「载体对接政策资源」+主需求 :3717（自动匹配+高亮可申领政策红利，比率口径无定义）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": "完全不支持",
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["无年度基期维（匹配率为当期截面比率，mock 亦无历史序列）"],
    "base_years_note": "匹配率为当期截面量；三源无承载无基期可言；非「缺年按 0 摊入」",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": ["92", "86", "79", "74", "83", "28", "57", "0", "6", "15", "280", "542", "218", "549", "3717"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", OUT)
print("support_judgment:", out["support_judgment"])

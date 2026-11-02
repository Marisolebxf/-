#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INCUB_026 载体成长活跃度 · 三源探针脚本（S3-07 L3）。

含义：孵化载体页总览 KPI「成长活跃度」——当前筛选载体的成长指数均值（分）。
UI：IncubationCarrierPage.jsx:115（KPI averageGrowth）。mock 源
incubationCarrierMock.js carriers[].growthIndex（88/81/76/73，均值 79.5→KPI 80 分）。

判档路径（口径 = 载体成长性综合评分，权威参照火炬中心孵化器评价指标体系
「孵化绩效 55%」维度——在孵企业收入增长/融资/知识产权/毕业等加权）：
- 计算前提是「载体画像 + 在孵企业运营流水（收入/融资/知识产权/毕业）」——三源：
  dev：dim.carrier 28 行 v1_approx 无标签/绩效维；enterprise_innovation_carrier 0 行；
  ads.carrier_index 0 行（index_score/sub_scores/weight_version 结构齐但空壳——
  为载体指数 run 预留）；在孵企业运营流水（企业-载体关系+收入/融资序列）无表；
  gkx：incub 词族 0 命中；
  久新：incub 词族 218 表 live 复核 0 命中（ads_* 科技要素分析面）；
- 判完全不支持（综合评分的输入维：企业运营流水与绩效结果面三源均无法构建；
  dev carrier_index 是唯一结构承载但 0 行且输入侧无源）。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_INCUB_026_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s307_l3_incub_out.json")

facts, derived, notes, absence = {}, [], [], []
probe = json.load(open(PROBE, encoding="utf-8"))

# ============ ① mock 层（UI 语义披露，不作数据证据） ============
MOCK_GROWTH_INDEX = [88, 81, 76, 73]
facts["ui_mount"] = "IncubationCarrierPage.jsx:115（KPI「成长活跃度」averageGrowth，buildKpis L106-108 growthIndex 均值）"
facts["ui_mock_growth_index"] = MOCK_GROWTH_INDEX
facts["ui_mock_kpi_value"] = round(sum(MOCK_GROWTH_INDEX) / len(MOCK_GROWTH_INDEX))  # 80
facts["ui_mock_rank_usage"] = "growthIndex 同为成长排榜排序键（buildRankItems L121 降序）与详情进度条（:1265 detailCarrier.growthIndex）"
facts["ui_mock_kpi_note"] = "mock 4 载体 growthIndex 均值 79.5 四舍五入 80 分（演示值，不参与支持度结论）"

# ============ ② dev ============
dev = probe["dev"]
facts["dev_table_total"] = dev["table_total"]
facts["dev_dim_carrier_rows"] = dev["gkxlumenx_dim.carrier"]["rows"]
facts["dev_dim_carrier_note"] = "dim.carrier 28 行 v1_approx 近似主档（名称/类型/坐标），无绩效/活跃输入维"
facts["dev_carrier_index_rows"] = dev["gkxlumenx_ads.carrier_index"]["rows"]
facts["dev_carrier_index_cols"] = [c["col"] for c in dev["gkxlumenx_ads.carrier_index"]["columns"]]
facts["dev_carrier_index_note"] = ("carrier_index 9 列（carrier_id/stat_period/domain_id/index_score/rank_total/rank_domain/"
                                   "rank_region/sub_scores/weight_version）——为载体指数 run 预留的结构面，0 行空壳；sub_scores/weight_version"
                                   " 证明设计意图是加权复合分（与火炬孵化绩效加权式同构），但输入侧无源")
facts["dev_growth_word_tables"] = dev["word_growth"]
facts["dev_growth_hits_note"] = "growth 词族唯一命中 dwd.enterprise_growth_trend（区域新设企业月度，0 行）——非载体成长评分面"

# ============ ③ gkx / 久新 ============
facts["gkx_table_count"] = probe["gkx"]["table_count"]
facts["gkx_incub_word_tables"] = probe["gkx"]["word_hits"]["incub"]
facts["jiuxin_table_count_live"] = probe["jiuxin"]["table_count_live"]
facts["jiuxin_incub_word_tables"] = probe["jiuxin"]["word_hits"]["incub"]
facts["jiuxin_hits_note"] = "incub/growth 词族 218 表 live 复核：incub 0 命中；growth 1 命中 ads_geo_yearly_index（地理年度指数，0 行快照）——均非载体成长面"

# ============ ④ 需求溯源 ============
facts["srs_anchor"] = "SRS 创新载体孵化载体.md 序号 543「载体势能与成长路径可视化」（趋势图/能级分析动态展示载体成长潜力、创新产出、资源聚集效果）+ 序号 556「用户评价与满意度报告」语境；主需求 :3665/:3731 同文"
facts["named_in_srs"] = False
facts["named_note"] = "「成长活跃度」指标名在三份说明书与主需求均未出现；语义锚为序号 543 成长路径可视化功能分句（活跃度构成口径无定义）"

# ============ ⑤ 权威口径 ============
facts["authoritative_reference"] = ("火炬中心《科技企业孵化器评价指标体系》（国科火字〔2019〕239 号）：综合加权评分=服务能力 30%+孵化绩效 55%+可持续发展 15%——"
                                    "孵化绩效含在孵企业收入增长比例 6%/获投融资占比 6%/新增在孵占比 6%/新增毕业占比 6%/研发投入占比 8%/知识产权密度 8% 等 9 项；"
                                    "「成长活跃度」语义最近邻=孵化绩效维度（在孵企业成长性加权复合）")

# ============ ⑥ absence_probe ============
absence = [
    {"probe": "dev 载体成长评分结果面",
     "source": "dev", "sql": "SELECT columns+COUNT(*) FROM gkxlumenx_ads.carrier_index / gkxlumenx_dwd.enterprise_innovation_carrier",
     "hits": 0,
     "hit_detail": "carrier_index 结构面齐（index_score/sub_scores/rank/weight_version——加权复合分设计意图明确）但 0 行；enterprise_innovation_carrier 0 行——结果面空壳"},
    {"probe": "dev 在孵企业运营流水（评分输入维：收入/融资/知识产权/毕业序列）",
     "source": "dev", "sql": "词族+表清单语义扫（enterprise_* 35 表语义核）",
     "hits": 0,
     "hit_detail": "enterprise_* 均为企业静态画像/风险面（enterprise_finance_history 39,959/enterprise_financing 25,621 为全市企业通用面非在孵企业-载体关系流水）；无「企业-载体入驻关系+运营序列」表——评分输入维缺失"},
    {"probe": "gkx 载体成长面（incub/growth 词族，280 表）",
     "source": "gkx", "sql": "information_schema.tables 扫 gkx",
     "hits": 0, "hit_detail": "0 命中——gkx 为论文/专利/机构/学者要素库"},
    {"probe": "久新载体成长面（incub/growth 词族，live 218 表复核）",
     "source": "jiuxin", "sql": "SHOW TABLES 词族过滤",
     "hits": 1,
     "hit_detail": "incub 0 命中；growth 唯一命中 ads_geo_yearly_index（0 行，地理年度指数）——科技要素侧无载体/孵化语义"},
    {"probe": "需求原文「成长活跃度」定义段",
     "source": "doc", "sql": "rg 成长活跃度 三份说明书+主需求",
     "hits": 0,
     "hit_detail": "指标名 0 命中；序号 543「载体势能与成长路径可视化」给展示要求（趋势图/能级分析）未定义活跃度构成；主需求 :3731 运行绩效监控列「孵化企业数量、毕业率、融资金额、创新成果和专利产出等指标」为构成族参照"},
]

# ============ ⑦ derived ============
derived = [
    {"key": "carrier_growth_activity_score", "value": None, "numerator": None, "denominator": None,
     "note": "『载体成长活跃度』=载体孵化绩效加权复合分（火炬式：收入增长/融资/新增在孵/毕业/研发投入/知识产权等加权）。需载体画像+在孵企业运营流水——dev carrier_index 0 行且输入维无表；gkx/久新 0 命中 → 不可构建，按 B10 留空即负结论登记"},
    {"key": "ui_mock_mean_reference", "value": facts["ui_mock_kpi_value"], "numerator": sum(MOCK_GROWTH_INDEX), "denominator": len(MOCK_GROWTH_INDEX),
     "note": "mock 4 载体均值 80 分——演示量级参照（B10 披露，不作数据证据）"},
]

notes = [
    "判档：综合评分双层依赖（结果面+输入流水）三源均无法构建——dev carrier_index 结构齐 0 行、在孵企业-载体关系流水无表 → 完全不支持",
    "权威口径（R1 火炬中心 2019 体系）：孵化绩效 55% 维度 9 项加权（收入增长/融资/新增在孵/新增毕业/研发投入/知识产权/科技型中小企业占比/上市并购/就业）；R2 广西体系 42% 孵化绩效同构——「成长活跃度」是 UI 对孵化绩效复合分的口语化命名",
    "mock 披露：growthIndex=[88,81,76,73] KPI 均值 80 分；同字段复用于排榜（降序）与详情进度条——单一 mock 字段三用",
    "同族件关系：INCUB_011（在孵企业成长分，L2 批）为企业级成长分、本件为载体级聚合——两件共享「评分输入维无承载」结论（本件独立留证）；INCUB_027（成长评分趋势）为时序形态",
    "升档路径：在孵企业-载体入驻关系+运营序列落库 → 评分 run 灌 carrier_index（结构已在，插数即活）→ 完全转换支持",
]

out = {
    "metric_id": "M_SCIUI_INCUB_026",
    "batch": "S3-07",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/achievement-preview/modules/incubation-carrier/components/IncubationCarrierPage.jsx:115",
        "repos/demo-ui-science/src/pages/achievement-preview/modules/incubation-carrier/mock/incubationCarrierMock.js:145",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书未出现「成长活跃度」指标名；语义锚 SRS 序号 543 载体势能与成长路径可视化+主需求 :3731 运行绩效监控指标族",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": "完全不支持",
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["无年度基期维（活跃度为当期复合分，mock 亦无历史序列；carrier_index.stat_period 预留未灌）"],
    "base_years_note": "复合评分为当期截面量；三源无承载无基期可言；非「缺年按 0 摊入」",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": ["88", "81", "76", "73", "80", "79.5", "28", "0", "9", "55", "30", "15", "6", "8", "543", "3731", "542", "280", "218"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", OUT)
print("KPI mock:", facts["ui_mock_kpi_value"])
print("support_judgment:", out["support_judgment"])

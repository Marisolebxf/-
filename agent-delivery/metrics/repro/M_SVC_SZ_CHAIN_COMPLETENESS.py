#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_SVC_SZ_CHAIN_COMPLETENESS｜深圳服务链完整度（挂起件，只出代理与阻断证据）。

官方口径（calc-logic v0.2.0，2026-10-13 拍板）：
  服务链完整度 = 已覆盖的服务链关键环节数 ÷ 全部关键环节数 × 100%
  - 公式**未签**（Q-SVCCHAIN-04 / 唐绍祖）
  - 环节轴只能是 CT-SVC-PT-01 服务链六环节；**禁止**用产业链 industry_link_code、
    服务六类、国标 industry 冒充
  - 机构×服务链环节服务记录不存在（SVC-P0-3），因此禁止用「六站有机构占比」
    或「六类覆盖率」冒充完整度

本件因此不产出完整度值（value=null），只产出：
  1) 六站口径的供给面代理（明确标注代理、不进 ADS、不当验收值）；
  2) 代理为何不可用的量化证据（12 个产业恒为 5/6、无方差；城市级 6/6 恒满）；
  3) 两库否定性证据（gkx 0 张 svc_*；live 13 张 svc_* 表 0 行）。

数据面：gkx（183.240.141.251:3318，只读 gkx_reader_zp）；零 SQL 运行。
产出：code/M_SVC_SZ_CHAIN_COMPLETENESS_out.json
运行：cd code && python3 M_SVC_SZ_CHAIN_COMPLETENESS.py
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FAM = os.path.join(SNAP, "svcsz21_facts_20261023.json")
OUT = os.path.join(HERE, "M_SVC_SZ_CHAIN_COMPLETENESS_out.json")

STAGES = ["stage-research", "stage-ip", "stage-transfer",
          "stage-pilot", "stage-testing", "stage-market"]
STAGE_CN = {
    "stage-research": "研发与科研合作",
    "stage-ip": "知识产权与标准",
    "stage-transfer": "技术转移与孵化",
    "stage-pilot": "中试熟化",
    "stage-testing": "检验检测认证",
    "stage-market": "市场与金融咨询",
}
# calc-logic（王惠 V1）四环节 → gkx 六站的映射尝试。None 表示没有对应站。
FOUR_MAP = [
    {"four": "研发创新", "stations": ["stage-research"], "status": "可映射"},
    {"four": "成果转化", "stations": ["stage-transfer", "stage-testing"], "status": "映射不唯一（含两站，且「中试」在 calc-logic 里属成果转化）"},
    {"four": "企业孵化", "stations": [], "status": "无独立站（「孵化」关键词被并入 stage-transfer 词表）"},
    {"four": "产业加速", "stations": ["stage-market"], "status": "可映射，但「产业基金/上市辅导」无独立字段，只能由「科技金融/投融资服务」词命中"},
]
# 两库否定性证据（落盘清单，见 _work_gkx21/GKX_INVENTORY.json 与 LIVE_INVENTORY.json）
NEG = {
    "gkx_tables_total": 280,
    "gkx_svc_like_tables": 0,
    "gkx_patterns": ["%svc%", "%service%", "%stage%", "%circle%", "%card%"],
    "gkx_stage_column_hits": 6,
    "gkx_stage_column_scope": "仅 dwd_bid_base_out 及其两张备份表的 bidding_stage / bidding_stage_code，与服务机构无关",
    "live_svc_tables": 13,
    "live_svc_tables_nonempty": 0,
    "live_svc_table_rows": 0,
}


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def pct(a, b):
    return round(a / b * 100, 2) if b else None


def main():
    fam = load(FAM)
    total = fam["pool"]["shenzhen"]
    stage_rows = fam["stage"]["rows"]
    stage_c = {r[0]: r[1] for r in stage_rows}
    covered = [s for s in STAGES if stage_c.get(s, 0) > 0]

    by_industry = []
    for ind, v in fam["industry_stage"].items():
        by_industry.append({
            "industry": ind,
            "orgs": v["orgs"],
            "covered_stages": v["covered_stages"],
            "total_stages": len(STAGES),
            "ratio_pct": round(v["complete_ratio"] * 100, 2),
            "missing_stages": [s for s in STAGES if s not in v["covered_ids"]],
            "stage_rows": [{"stage": r[0], "name_cn": STAGE_CN[r[0]], "orgs": r[1],
                            "hit": r[1] > 0} for r in v["stage_rows"]],
        })
    cov_values = sorted({r["covered_stages"] for r in by_industry})

    proxy = {
        "purpose": "代理探针：证明「有代理」不等于「部分支持」，代理值零方差、无区分度",
        "city_level": {
            "covered": len(covered),
            "total": len(STAGES),
            "ratio_pct": pct(len(covered), len(STAGES)),
            "verdict": "恒满（100%），零信息量",
            "why": "「有 ≥1 家机构」这一判定在城市级必然为真：深圳 25,597 家里六站都有命中",
        },
        "industry_level": {
            "industries": len(by_industry),
            "covered_values": cov_values,
            "distinct_values": len(cov_values),
            "ratio_uniform_pct": round(cov_values[0] / len(STAGES) * 100, 2) if len(cov_values) == 1 else None,
            "verdict": "无方差（12 个产业全部 5/6）",
            "why": "唯一缺的恒为「中试熟化」；代理无法区分产业，等于把常数当指标",
        },
        "proxy_value": None,
        "proxy_disclaimer": (
            "六站供给面代理（经营范围词表命中）不是「机构在某环节提供过服务」的事实记录；"
            "calc-logic 明确禁止用它冒充完整度。本件只将其作为缺口证据与展示层参考，"
            "禁止写入 ADS 的 svc_metric_* 本 ID，禁止作为验收值。"
        ),
    }

    out = {
        "metric_id": "M_SVC_SZ_CHAIN_COMPLETENESS",
        "metric_name": "服务链完整度",
        "support_judgment": "完全不支持",
        "judgment_reason": (
            "完整度公式未签（Q-SVCCHAIN-04 / 唐绍祖），calc-logic 0.2.0 明确「本件不做真数、不写可执行公式」；"
            "计算所需的「机构×服务链六环节服务记录」（SVC-P0-3）在 gkx 与 live 均不存在"
            "（gkx 280 表 0 张 svc_*；live 13 张 svc_* 表 0 行）。分子（某机构在某环节提供过服务）与分母"
            "（关键环节全集）两端都无结构承载，属结构与数据双缺。经营范围词表派生的六站代理在城市级恒满 6/6、"
            "在 12 个产业上恒为 5/6（distinct=1、零方差），既无区分度，又被 calc-logic 明令禁止冒充完整度，"
            "不能把档位抬到部分支持。故判完全不支持，官方值置 null。"
        ),
        "verdict_kind": "negative_evidence",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "本件是截面（当期环节覆盖），无年度序列，不使用基期年份；"
            "future 若要出「完整度时间序列」，需要机构×环节成员表带生效期，当前两库均无此字段。"
        ),
        "sources": {
            "library": "gkx",
            "host": "183.240.141.251:3318",
            "user": "gkx_reader_zp",
            "mode": "read-only",
            "tables": [
                "gkx.dwd_org_org_product_info（main_activities 词表 → 六站代理）",
                "gkx.dwd_org_industry_tags（产业标签，经 pool_tags 快照）",
                "gkx.information_schema（表名/列名否定性证据）",
            ],
            "snapshots": [
                "code/_snapshots21/svcsz21_facts_20261023.json",
                "code/_snapshots21/svc21_facts_20261022.json",
                "code/_snapshots21/svc21_pt_axis_20261022.json",
            ],
            "inventory": [
                "_work_gkx21/GKX_INVENTORY.json",
                "_work_gkx21/LIVE_INVENTORY.json",
            ],
            "calc_logic": "gkx-orchestration/agent-delivery/metrics/calc-logic/SVC/M_SVC_SZ_CHAIN_COMPLETENESS.md",
        },
        "params": {
            "formula": "已覆盖的服务链关键环节数 ÷ 全部关键环节数 × 100%",
            "formula_status": "未签（Q-SVCCHAIN-04 / 唐绍祖）",
            "axis": "CT-SVC-PT-01 服务链六环节（research/ip/transfer/pilot/testing/market）",
            "forbidden_substitutes": ["产业链 industry_link_code", "服务六类", "国标 industry", "六站有机构占比", "六类覆盖率"],
            "sz_total": total,
            "stage_rule": "经营范围 main_activities 词表命中（_build_svc21_facts.py STAGES）",
        },
        "value": {
            "completeness": None,
            "completeness_4_stage": None,
            "completeness_6_stage_proxy": None,
            "reason": "官方公式未签 + 环节成员记录缺失；代理无区分度且被禁止冒充",
        },
        "stage_rows": [{"stage": r[0], "name_cn": STAGE_CN[r[0]], "orgs": r[1],
                        "share_pct": pct(r[1], total), "hit": r[1] > 0} for r in stage_rows],
        "stage_summary": {
            "hit_orgs": fam["stage"]["hit_orgs"],
            "hit_rate_pct": round(fam["stage"]["hit_rate"] * 100, 2),
            "hits_total": fam["stage"]["hits_total"],
            "orgs_by_stage_count": fam["stage"]["orgs_by_stage_count"],
            "covered_stations": len(covered),
        },
        "proxy": proxy,
        "negative_probe": {
            "probe_1_algorithm": {
                "question": "完整度的分子/分母定义是否已在项目内签定？",
                "method": "读 calc-logic 正本 M_SVC_SZ_CHAIN_COMPLETENESS.md（0.2.0，2026-10-13）",
                "result": "未签（Q-SVCCHAIN-04 / 唐绍祖）；原文「公式：未签」「本件不做真数」「不写可执行公式」",
                "conclusion": "算法层不可构建",
            },
            "probe_2_structure": {
                "question": "gkx 是否存在机构×服务链环节的成员表或等价结构？",
                "method": "grep 全库列字典 gkx_columns_20261023.json（280 表 / 6,312 列）+ information_schema 表名匹配",
                "result": "0 张 svc_* 表；%stage% 列仅命中 6 列，全部落在 dwd_bid_base_out 及两张备份表的 bidding_stage / bidding_stage_code（招投标阶段，与服务机构无关）",
                "conclusion": "结构层不可构建",
            },
            "probe_3_data": {
                "question": "live 库 13 张 svc_* 表是否有行？",
                "method": "LIVE_INVENTORY.json 逐表 COUNT",
                "result": "13 张全部 0 行；svc_metric_fact / svc_metric_series 亦 0 行",
                "conclusion": "数据层不可构建",
            },
            "probe_4_proxy_variance": {
                "question": "六站供给面代理能否充当「部分可算」的取值？",
                "method": "按 12 个产业分组算覆盖站数",
                "result": "城市级 6/6（恒满）；产业级 12 个全部 5/6（distinct=1，唯一缺项恒为 stage-pilot）",
                "conclusion": "代理为零方差常数，不构成可用取值",
            },
        },
        "by_industry": by_industry,
        "four_stage_mapping": FOUR_MAP,
        "negative_evidence": NEG,
        "gaps": [
            {
                "gap": "完整度公式未签",
                "detail": "Q-SVCCHAIN-04 / 唐绍祖；calc-logic 明写「不写可执行公式」",
                "impact": "分子分母定义未定，任何数值都不具备验收资格",
                "fix": "唐绍祖出完整度定义卡",
            },
            {
                "gap": "机构×服务链环节服务记录缺失",
                "detail": "SVC-P0-3 待供方交付；gkx 280 表 0 张 svc_*，live 13 张 svc_* 表 0 行",
                "impact": "「某机构在某环节提供过服务」不可知，只能用经营范围词表代理",
                "fix": "供方交付机构×六环节成员表（含生效期）",
            },
            {
                "gap": "代理无区分度",
                "detail": "城市级 6/6 恒满；12 个产业全部 5/6，唯一缺项恒为「中试熟化」",
                "impact": "代理值等于常数，不能用于排名、分档或对外披露",
                "fix": "无需修代理；等真成员表",
            },
            {
                "gap": "中试熟化仅 2 家",
                "detail": "stage-pilot 在深圳切片命中 2 家（全池 10 家），词表为「中试/概念验证/熟化/试制/小试」",
                "impact": "该站事实上是空白站；即便将来用代理，也会把 5/6 变成所有产业的共同值",
                "fix": "补中试平台/概念验证中心名录（科技部/工信部口径）",
            },
            {
                "gap": "四环节与六站不是一一映射",
                "detail": "「企业孵化」无独立站，「成果转化」横跨 transfer+testing+pilot",
                "impact": "按 calc-logic 的四环节算完整度会引入映射假设，本件不做",
                "fix": "定义卡明确四环节与六站的对应关系，或统一改用六站轴",
            },
        ],
        "cross_refs": {
            "M_SVC_SZ_TIER": {"completeness_dimension": "共享同一代理轴，Tier 亦置 null"},
            "M_SVC_PT_CHAIN_NODE_ORG": {"same_stage_axis": True,
                                        "note": "同族已交付件用同一六站词表，判部分支持"},
            "M_SVC_SZ_COMPARE_METRIC": {"completeness_excluded": True},
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written", OUT)
    print("stage:", [(r["stage"], r["orgs"]) for r in out["stage_rows"]])
    print("covered=%d/%d industries_distinct=%d" % (len(covered), len(STAGES), len(cov_values)))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SVC_SZ_TIER｜深圳梯队位置（三维独立分档）。

三个对比维度（calc-logic / 王惠 V1-20260826 同口径）：
  1) 服务机构数量：深圳产业相关「科学研究和技术服务业」法人单位数
  2) 技术力得分：研发投入强度 + 研发人才结构 + 创新产出 三子指标极值归一化后等权
  3) 服务链完整度：已覆盖服务链关键环节数 / 全部关键环节数
每个维度把参与对比的城市按值排序，前 30% / 中 40% / 后 30% 分三档。

本件只做「可算部分 + 逐维阻断说明」，不产出梯队名次（三维均无法在同一城市集合上闭合）。

数据面：gkx（183.240.141.251:3318，只读 gkx_reader_zp）；零 SQL 运行。
产出：code/M_SVC_SZ_TIER_out.json
运行：cd code && python3 M_SVC_SZ_TIER.py
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
FAM = os.path.join(SNAP, "svcsz21_facts_20261023.json")
STAR = os.path.join(SNAP, "star_applicant_agg_gkx.json")
OUT = os.path.join(HERE, "M_SVC_SZ_TIER_out.json")

SZ = "深圳市"
CITIES = ["深圳市", "广州市", "东莞市", "惠州市"]
STAGES = ["stage-research", "stage-ip", "stage-transfer",
          "stage-pilot", "stage-testing", "stage-market"]
STAGE_CN = {
    "stage-research": "研发与科研合作", "stage-ip": "知识产权与标准",
    "stage-transfer": "技术转移与孵化", "stage-pilot": "中试熟化",
    "stage-testing": "检验检测认证", "stage-market": "市场与金融咨询",
}
M_IND = "科学研究和技术服务业"


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def pct(a, b):
    return round(a / b * 100, 2) if b else None


def main():
    facts = load(FACTS)
    fam = load(FAM)
    agg = (load(STAR).get("agg") or {})
    pool = facts["pool"]
    bf = facts["base_fields"]
    pool_tags = load(os.path.join(SNAP, "svc21_pt_axis_20261022.json")).get("pool_tags") or {}
    total = len(pool)

    city_rows = []
    for city in CITIES:
        ids = [oid for oid, v in pool.items() if v.get("city") == city]
        ind_m = sum(1 for oid in ids
                    if (bf.get(oid) or {}).get("ind") == M_IND)
        large = sum(1 for oid in ids if (bf.get(oid) or {}).get("size") == "大型")
        staged = sum(1 for oid in ids if pool[oid].get("stages"))
        pat = 0
        apps = 0
        grants = 0
        for oid in ids:
            rec = agg.get(pool[oid].get("name"))
            if rec and isinstance(rec, list) and len(rec) >= 2:
                pat += 1
                apps += int(rec[0])
                grants += int(rec[1])
        city_rows.append({
            "city": city,
            "orgs": len(ids),
            "orgs_share_pct": pct(len(ids), total),
            "ind_m_orgs": ind_m,
            "ind_m_share_pct": pct(ind_m, len(ids)),
            "large_orgs": large,
            "large_share_pct": pct(large, len(ids)),
            "stage_hit_orgs": staged,
            "stage_hit_rate_pct": pct(staged, len(ids)),
            "patent_matched_orgs": pat,
            "patent_apps": apps,
            "patent_grants": grants,
            "patent_apps_per_matched": round(apps / pat, 2) if pat else None,
            "patent_apps_per_all_org": round(apps / len(ids), 2) if ids else None,
        })
    city_rows.sort(key=lambda r: -r["orgs"])
    for i, r in enumerate(city_rows, 1):
        r["rank_in_pool_cities"] = i

    sz = city_rows[0] if city_rows[0]["city"] == SZ else next(r for r in city_rows if r["city"] == SZ)
    gd_orgs = sum(r["orgs"] for r in city_rows)

    # ---- 维度 2：技术力三子指标 ----
    tech_sub = [
        {
            "sub": "研发投入强度",
            "formula": "研发经费内部支出 ÷ 营业收入 × 100%",
            "field": "dwd_org_annual_financial_info.arch_development_am / operating_revenue",
            "status": "不可算",
            "reason": (
                "arch_development_am 在 dwd_org_annual_financial_info 全表 90,926 行**整列为空**"
                "（0 行非空），分子恒缺；operating_revenue 仅 2,193 行有值（2.41%）。"
                "研发口径只能去 dwd_org_stock_finance_info（上市主体 876 家），"
                "而上市主体不是服务机构池的子集，不能代入城市对比。"
            ),
            "num": None,
            "den": None,
            "value": None,
        },
        {
            "sub": "研发人才结构",
            "formula": "研发人员数 ÷ 从业人员总数 × 100%",
            "field": "dwd_org_annual_financial_info.development_employee / employees_number",
            "status": "不可算",
            "reason": (
                "development_employee 全表 90,926 行整列为空（0 行非空）；"
                "employees_number 仅 3,170 行有值（3.49%）。分子恒缺，分母也只剩 3.49%。"
            ),
            "num": None,
            "den": None,
            "value": None,
        },
        {
            "sub": "创新产出",
            "formula": "有效发明专利（或专利授权）总数",
            "field": "dwd_patent（按申请人名对齐 star_applicant_agg_gkx.json）",
            "status": "代理可算",
            "reason": (
                "专利授权件数可按申请人名对齐（深圳 13,378/25,597 家有专利记录），"
                "但只有「件数/授权数」两个聚合值，没有 kind 过滤与法律状态，"
                "不能区分「有效发明专利」与其它类型；且名对齐不是信用码对齐。"
            ),
            "num": sz["patent_grants"],
            "den": sz["patent_matched_orgs"],
            "value": sz["patent_apps_per_matched"],
        },
    ]
    tech_computable = sum(1 for s in tech_sub if s["status"] == "代理可算")

    # ---- 维度 3：完整度 ----
    stage_c = {r[0]: r[1] for r in fam["stage"]["rows"]}
    covered = [s for s in STAGES if stage_c.get(s, 0) > 0]
    ind_cov = {ind: v["covered_stages"] for ind, v in fam["industry_stage"].items()}
    complete = {
        "formula": "已覆盖的服务链关键环节数 ÷ 全部关键环节数 × 100%",
        "axis_6": {"covered": len(covered), "total": len(STAGES),
                   "ratio_pct": pct(len(covered), len(STAGES))},
        "axis_4_calc_logic": {
            "covered": None, "total": 4, "ratio_pct": None,
            "reason": "calc-logic 的四环节（研发创新/成果转化/企业孵化/产业加速）与 gkx 六站不是一一映射，映射表见 §2.5，缺「企业孵化」独立轴",
        },
        "by_industry_covered_values": sorted(set(ind_cov.values())),
        "by_industry_distinct_count": len(set(ind_cov.values())),
        "status": "仅代理",
        "value": None,
    }

    out = {
        "metric_id": "M_SVC_SZ_TIER",
        "metric_name": "深圳梯队位置",
        "support_judgment": "部分支持",
        "judgment_reason": (
            "三个维度里只有「服务机构数量」在池内可算（深圳 25,597），但梯队分档要求与全国城市"
            "同口径排序，而 gkx 服务机构池 100% 落在广东省、池外城市 0 家，无法构成全国对比集合；"
            "「技术力」三子指标有两个的分子列整列为空（研发投入/研发人员），只有专利代理可算；"
            "「服务链完整度」公式未签且无机构×环节成员表，六站代理在 12 个产业上恒为 5/6、无区分度。"
            "三维均无法在同一城市集合上闭合，故判部分支持，不产出梯队名次。"
        ),
        "verdict_kind": "positive",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "本件是截面排序（当期三维取值），不使用基期年份；技术力三子指标本应取同一会计年，"
            "但研发两列的分子整列为空、营收/员工最新有值年集中在 2014—2016（见 annual_report），"
            "年份无法对齐，这也是该维不可算的原因之一。"
        ),
        "sources": {
            "library": "gkx",
            "host": "183.240.141.251:3318",
            "user": "gkx_reader_zp",
            "mode": "read-only",
            "tables": [
                "gkx.dwd_org_org_product_info（机构池）",
                "gkx.dwd_org_base_info（city / area / org_size / industry）",
                "gkx.dwd_org_industry_tags（产业标签，经 pool_tags 快照）",
                "gkx.dwd_org_annual_financial_info（研发/营收/员工，两列整列为空）",
                "gkx.dwd_patent（经 star_applicant_agg_gkx.json 聚合快照）",
            ],
            "snapshots": [
                "code/_snapshots21/svcsz21_facts_20261023.json",
                "code/_snapshots21/svc21_facts_20261022.json",
                "code/_snapshots21/svc21_pt_axis_20261022.json",
                "code/_snapshots21/star_applicant_agg_gkx.json",
            ],
            "calc_logic": "gkx-orchestration/agent-delivery/metrics/calc-logic/SVC/M_SVC_SZ_TIER.md",
            "wanghui": "local-workspace/docs/metrics/王惠阶段性成果/20260904_综合智能/指标计算逻辑/M_SVC_SZ_TIER.md",
        },
        "params": {
            "compare_cities_defined": ["深圳", "北京", "上海", "广州", "其他省会城市"],
            "compare_cities_available": CITIES,
            "compare_city_status": "仅广东省 4 市有池内机构；北京/上海/其他省会城市 0 家，不可比",
            "tier_cut": {"first": 0.30, "second": 0.40, "third": 0.30},
            "tier_method": "每维独立排序后按 30/40/30 分档",
        },
        "value": {
            "tier_overall": None,
            "tier_org_count": None,
            "tier_tech": None,
            "tier_completeness": None,
            "reason": "三维均缺同一城市集合上的可比取值，按规则不得产出名次（宁缺不猜）",
        },
        "dimensions": {
            "org_count": {
                "status": "池内可算 / 全国不可比",
                "sz_orgs": sz["orgs"],
                "sz_share_of_pool_pct": pct(sz["orgs"], total),
                "sz_share_of_pool_cities_pct": pct(sz["orgs"], gd_orgs),
                "sz_ind_m_orgs": sz["ind_m_orgs"],
                "sz_ind_m_share_pct": sz["ind_m_share_pct"],
                "city_rows": city_rows,
                "note": (
                    "calc-logic 的维度 1 定义是「门类 M 法人单位数」，本件只能给池内门类 M"
                    "（深圳 2,579 家）；全量底册 189,116 行的门类 M 分布需整表扫描，"
                    "本轮按共享资产纪律未重扫（dwd_org_base_info 的 industry 无索引）。"
                ),
            },
            "tech_score": {
                "status": "1/3 子指标代理可算，整维不可算",
                "computable_sub": tech_computable,
                "sub_indicators": tech_sub,
                "value": None,
            },
            "completeness": complete,
        },
        "stage_rows": [[s, stage_c.get(s, 0), STAGE_CN[s]] for s in STAGES],
        "industry_stage": fam["industry_stage"],
        "annual_report": {
            "orgs_with_rev": fam["finance"]["orgs_with_rev"],
            "rev_rate_pct": round(fam["finance"]["rev_rate"] * 100, 2),
            "orgs_with_emp": fam["finance"]["orgs_with_emp"],
            "emp_rate_pct": round(fam["finance"]["emp_rate"] * 100, 2),
            "rev_latest_year_rows": fam["finance"]["rev_latest_year_rows"],
        },
        "gaps": [
            {
                "gap": "全国对比城市集合缺失",
                "detail": "服务机构池 44,132 行回联底册后 100% 为广东省（深圳/广州/东莞/惠州），北京/上海/其他省会城市 0 家",
                "impact": "「前 30% / 中 40% / 后 30%」的分母只有 4 个城市，比例分档在 4 个样本上没有统计意义",
                "fix": "甲方指定城市基准源（Q-SVCCHAIN-04），或提供全国服务机构圈定池",
            },
            {
                "gap": "研发投入分子整列为空",
                "detail": "dwd_org_annual_financial_info.arch_development_am 90,926 行 0 行非空",
                "impact": "技术力三分之一的子指标不可算，整维无法合成",
                "fix": "接入研发费用加计扣除/统计年报口径，或用上市主体研发费用（仅 876 家，需注明非全量）",
            },
            {
                "gap": "研发人员分子整列为空",
                "detail": "dwd_org_annual_financial_info.development_employee 90,926 行 0 行非空",
                "impact": "同上；分母 employees_number 也只有 3.49%",
                "fix": "接入社保参保人数或规上企业年报",
            },
            {
                "gap": "服务链完整度公式未签 + 环节成员表缺失",
                "detail": "Q-SVCCHAIN-04 / 唐绍祖未签；SVC-P0-3 机构×六环节成员表在 gkx 与 live 均不存在",
                "impact": "该维只能用经营范围词表代理，且代理在 12 个产业上恒为 5/6，无区分度",
                "fix": "算法定义卡 + 供方交付成员表",
            },
            {
                "gap": "创新产出只有件数/授权数聚合",
                "detail": "无 kind 与法律状态，无法只取有效发明专利",
                "impact": "只能作技术力的代理子指标，不能替代「有效发明专利数」",
                "fix": "补 dwd_patent_legal 的授权有效口径（gkx 无该表）",
            },
        ],
        "cross_refs": {
            "M_SVC_PT_SZ_TOTAL": {"sz_orgs": sz["orgs"]},
            "M_SVC_SZ_COMPARE_METRIC": {"shared_grid": True,
                                        "note": "两件共用同一城市×小项面板，深圳格必须同数"},
            "M_SVC_SZ_CHAIN_COMPLETENESS": {"proxy_same_axis": True},
        },
    }
    # city_rows 里 sz 引用是同一 dict，排序后仍一致
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written", OUT)
    print("city_rows:", [(r["city"], r["orgs"], r["patent_apps"]) for r in city_rows])
    print("stage covered=%d/%d" % (len(covered), len(STAGES)))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""区域产业创新成果综合评价模型（M_SYNTH_183_1）—— 复现脚本。

正本（calc-logic/SYNTH/M_SYNTH_183_1.md）三维：产品服务创新 / 企业创新 / 服务机构创新。
本脚本只做「读族级面板 + 三维极值归一 + 维内等权 + 三维等权」，不新建叶子。

运行：
    cd code && python3 M_SYNTH_183_1.py
产物：
    code/M_SYNTH_183_1_out.json
所需：
    code/_snapshots21/vit_family_20261023.json   （由 _build_vit_family_panel.py 生成）
    code/_snapshots21/vit_absence_20261023.json  （否定性证据探针）
    code/M_SYNTH_182_1_out.json                  （2024 授权专利，只读）
    code/M_SYNTH_VIT_RANK_out.json               （高企数，只读）
"""
from __future__ import annotations

import json
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
PANEL = os.path.join(SNAP, "vit_family_20261023.json")
ABSENCE = os.path.join(SNAP, "vit_absence_20261023.json")
OUT = os.path.join(HERE, "M_SYNTH_183_1_out.json")

CITIES = ["深圳市", "广州市", "东莞市", "惠州市"]
TOL = 1e-9


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def mm(values: dict) -> dict:
    """四市盘内极值归一。缺测（None）不参与求极值，也不得被写成 0。"""
    vals = [v for v in values.values() if v is not None]
    if not vals:
        return {c: None for c in values}
    lo, hi = min(vals), max(vals)
    if abs(hi - lo) < TOL:
        # 常数不是「高」也不是「低」：整列无定义，记 null 而不是 50
        return {c: None for c in values}
    return {c: (None if v is None else round((v - lo) / (hi - lo) * 100.0, 4))
            for c, v in values.items()}


def mean_of_available(*dicts):
    """维内等权：只对「该城非空」的子项求均值；无任何非空子项记 null。

    这不是「重归一」——归一化会放大剩余子项的权重，而这里是把剩余子项
    按同一把尺子（0—100）等权平均，缺失子项不占权重也不补 0。
    """
    out = {}
    for c in CITIES:
        vals = [d[c] for d in dicts if d.get(c) is not None]
        out[c] = round(sum(vals) / len(vals), 4) if vals else None
    return out


def weighted(dims: dict, w: dict) -> dict:
    """按维权重合成；缺维的城不进加权、也不把剩余维重归一（v8 口径）。"""
    out = {}
    for c in CITIES:
        num = den = 0.0
        for k, wk in w.items():
            v = dims[k].get(c)
            if v is None:
                continue
            num += wk * v
            den += wk
        out[c] = round(num, 4) if den > 0 else None
    return out


def ranking(idx: dict) -> dict:
    order = sorted([c for c in CITIES if idx.get(c) is not None],
                   key=lambda c: (-idx[c], c))
    return {c: i + 1 for i, c in enumerate(order)}


def main():
    t0 = time.time()
    panel = load(PANEL)
    absence = load(ABSENCE)
    m182 = load(os.path.join(HERE, "M_SYNTH_182_1_out.json"))
    rank = load(os.path.join(HERE, "M_SYNTH_VIT_RANK_out.json"))

    prod = panel["products"]["by_city"]
    macro = panel["macro"]
    svc = panel["svc"]["by_city"]

    # ---------------------------------------------------------------- 原始读数
    # 1. 产品名称覆盖数（product_name 去重）
    raw_products = {c: prod[c]["products"] for c in CITIES}
    # 2. 企业数（产品标签侧，用于密度敏感性）
    raw_companies = {c: prod[c]["companies"] for c in CITIES}
    # 3. 第三产业增加值占比重（同 area_code + 同 occur_period + JDZ + DNLJ）
    raw_tertiary = {c: (macro["by_city"][c].get("latest_pair") or {}).get("tertiary_share_pct")
                    for c in CITIES}
    # 4. 高新技术企业数（只读 VIT_RANK 的 raw，不重查 tech_tag）
    raw_hightech = {c: rank["raw"]["hightech_enterprises"][c] for c in CITIES}
    # 5. 企业授权专利数（2024，只读 182 的 D2）
    raw_patents = {c: m182["dims"]["D2_applied_tech"]["grants_2024"][c] for c in CITIES}
    # 6. 创新服务机构绩效（固定词表 0—100，不再做批内极值）
    raw_svc = {c: svc[c]["mean"] for c in CITIES}

    # ---------------------------------------------------------------- 归一
    norm_products = mm(raw_products)
    norm_tertiary = mm(raw_tertiary)          # 四城有三个 None → 整列 null
    norm_hightech = mm(raw_hightech)
    norm_patents = mm(raw_patents)
    # 服务机构维：分母是固定词表（6 类型 × 6 环节），分数本身已是 0—100，
    # 再做批内极值会把 1.4 分的差放大成 100 对 92，故保留原标度。
    norm_svc = {c: raw_svc[c] for c in CITIES}

    # ---------------------------------------------------------------- 三维
    d1 = mean_of_available(norm_products, norm_tertiary)
    d2 = mean_of_available(norm_hightech, norm_patents)
    d3 = dict(norm_svc)
    dims = {"D1_产品服务创新": d1, "D2_企业创新": d2, "D3_服务机构创新": d3}

    w_main = {"D1_产品服务创新": 1 / 3, "D2_企业创新": 1 / 3, "D3_服务机构创新": 1 / 3}
    idx = weighted(dims, w_main)
    rk = ranking(idx)

    # ---------------------------------------------------------------- 敏感性
    # S1：服务机构维改用批内极值（把 1.4 分的差放大成 100 对 92 会怎样）
    d3_mm = mm(raw_svc)
    s1 = weighted({"D1_产品服务创新": d1, "D2_企业创新": d2, "D3_服务机构创新": d3_mm}, w_main)
    # S2：产品维改用密度口径（企均产品名），检验「规模 vs 密度」
    raw_density = {c: round(raw_products[c] / raw_companies[c], 4) for c in CITIES}
    d1_density = mm(raw_density)
    s2 = weighted({"D1_产品服务创新": d1_density, "D2_企业创新": d2,
                   "D3_服务机构创新": d3}, w_main)
    # S3：权重倾斜（产品服务 0.50 / 企业 0.30 / 服务机构 0.20）
    w_bias = {"D1_产品服务创新": 0.50, "D2_企业创新": 0.30, "D3_服务机构创新": 0.20}
    s3 = weighted(dims, w_bias)
    # S4：砍掉服务机构维（二维盘），看是否可以不用代理维
    w_two = {"D1_产品服务创新": 0.5, "D2_企业创新": 0.5, "D3_服务机构创新": 0.0}
    s4 = weighted(dims, w_two)

    # ---------------------------------------------------------------- 派生比值
    base_orgs = panel["base_orgs"]
    pmeta = panel["products"]
    matched = pmeta["rows_matched_base"]
    cc18 = pmeta["rows_with_18char_company_name"]
    rows_total = pmeta["rows_total"]
    products_total = pmeta["products_matched"]
    companies_total = pmeta["companies_matched"]
    derived = {
        "product_tag_rows_over_base_orgs_pct": {
            "value": round(100.0 * matched / base_orgs, 4),
            "numerator": matched, "denominator": base_orgs,
            "denominator_note": "分母 = 底册 189,116 家（四市存续企业全集）；"
                                "分子 = 产品标签表能按信用代码归到四市底册的行数",
        },
        "product_tag_18char_share_pct": {
            "value": round(100.0 * cc18 / rows_total, 4),
            "numerator": cc18, "denominator": rows_total,
            "denominator_note": "分母 = 产品标签表全表 80,258 行；分子 = company_name 为 18 位"
                                "信用代码形态的行（其余 1,420 行是机构名或空）",
        },
        "product_tag_match_rate_pct": {
            "value": round(100.0 * matched / cc18, 4),
            "numerator": matched, "denominator": cc18,
            "denominator_note": "分母 = 信用代码形态行 78,838；分子 = 能在四市底册对上的行。"
                                "对不上的多数是四市以外的企业（产品表是全国表）",
        },
        "product_names_sum_by_city": {
            "value": sum(raw_products.values()),
            "numerator": sum(raw_products.values()), "denominator": len(CITIES),
            "denominator_note": "分母 = 四城；分子 = 四城各自去重后相加（会重复计同名产品）",
        },
        "product_names_dedup_total": {
            "value": products_total,
            "numerator": products_total, "denominator": sum(raw_products.values()),
            "denominator_note": "分母 = 四城各自去重后相加；分子 = 跨城再去重后的产品名数，"
                                "差 2,570 个是为同名产品在多个城市出现",
        },
        "product_tag_unmatched_rows": {
            "value": cc18 - matched,
            "numerator": cc18 - matched, "denominator": cc18,
            "denominator_note": "分母 = 18 位代码形态行 78,838；分子 = 对不上四市底册的行 "
                                "(78,838 − 10,410)，多为四市以外企业",
        },
        "products_per_tagged_company_city": {
            "value": {c: round(raw_products[c] / raw_companies[c], 4) for c in CITIES},
            "numerator": raw_products, "denominator": raw_companies,
            "denominator_note": "分母 = 该市有产品标签的企业数；分子 = 该市产品名去重数",
        },
        "tertiary_share_pct_dongguan_2017H1": {
            "value": raw_tertiary["东莞市"],
            "numerator": macro["by_city"]["东莞市"]["latest_pair"]["tertiary"],
            "denominator": macro["by_city"]["东莞市"]["latest_pair"]["gdp"],
            "denominator_note": "东莞 201706 单点：第三产业增加值 186,591,270,000 元 ÷ GDP "
                                "352,538,800,000 元；四市中唯一一个同期间 JDZ 配对，"
                                "仅 1 城故不进极值归一",
        },
        "sub_indicator_filled_share": {
            "value": round(4 / 5, 4),
            "numerator": 4, "denominator": 5,
            "denominator_note": "分母 = 正本三维下的 5 个三级指标；分子 = 四城至少一城有值的 4 个",
        },
        "cities_with_macro_pair_share": {
            "value": round(macro["cities_with_pair_n"] / len(CITIES), 4),
            "numerator": macro["cities_with_pair_n"], "denominator": len(CITIES),
            "denominator_note": "分母 = 评估集 4 城；分子 = 存在同期间 JDZ 配对的城市数",
        },
        "shenzhen_gap_to_guangzhou": {
            "value": round(idx["深圳市"] - idx["广州市"], 4),
            "numerator": idx["深圳市"], "denominator": idx["广州市"],
            "denominator_note": "合成指数之差（深圳 − 广州），不是比值",
        },
        "huizhou_density_over_shenzhen": {
            "value": round(raw_density["惠州市"] / raw_density["深圳市"], 4),
            "numerator": raw_density["惠州市"], "denominator": raw_density["深圳市"],
            "denominator_note": "企均产品名：惠州 964/257 对深圳 19,714/6,047",
        },
    }

    # ---------------------------------------------------------------- 否定性证据
    absence_probe = [
        {
            "target": "第三产业增加值占比重（产品服务创新维第 2 子项）",
            "table": "gkx.dwd_macro_index_data",
            "condition": "area_code IN ('440300000000','440100000000','441900000000',"
                         "'441300000000') AND index_code IN ('gmjj_jjzl_01','gmjj_jjzl_01_03')",
            "rows": macro["rows_total"],
            "screen": "再过滤 dim_cal='JDZ' AND dim_dur='DNLJ'，按 occur_period 求两码交集",
            "hit": {"cities_with_pair": macro["cities_with_pair_n"],
                    "pairs": macro["by_city"]["东莞市"]["jdz_pairs"],
                    "note": "只有东莞市 201706 一对；深圳第三产业 JDZ+DNLJ 为 0 行，"
                            "广州两码期间不相交，惠州两码期间不相交"},
            "consequence": "四城中有值城市 1 < 2，无法在四市盘上做极值归一，故整列记 null，"
                           "不用 TB 同比顶替、不填 0",
        },
        {
            "target": "创新服务机构绩效的服务机构主表（svc_org_card）",
            "table": "information_schema.tables",
            "condition": "table_schema='gkx' AND (table_name LIKE '%svc%' OR "
                         "table_name LIKE '%service%')",
            "rows": len(absence["svc_tables_gkx"]),
            "hit": "0 张",
            "consequence": "gkx 无 svc_* 表；改用覆盖率族快照（dwd_org_org_product_info 重建的"
                           "服务广度/深度），语义从『服务机构经营绩效』降级为『服务能力覆盖』",
        },
    ]

    out = {
        "metric_id": "M_SYNTH_183_1",
        "metric_name": "区域产业创新成果综合评价模型",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "verdict_kind": "negative_evidence",
        "verdict_kind_note": "部分支持且产品服务创新维有一个三级指标四城全缺（5 个三级指标里 1 个整块缺），"
                             "故按 v8 §四留 absence_probe",
        "source": {
            "library": "gkx",
            "host": "183.240.141.251:3318",
            "user": "gkx_reader_zp",
            "mode": "read-only",
            "tables": ["gkx.dwd_org_industry_product_tags", "gkx.dwd_macro_index_data"],
        },
        "sources": [
            "code/_snapshots21/vit_family_20261023.json",
            "code/_snapshots21/vit_absence_20261023.json",
            "code/M_SYNTH_182_1_out.json",
            "code/M_SYNTH_VIT_RANK_out.json",
            "code/_snapshots21/base_20261021.json",
            "code/_snapshots21/svc21_facts_20261022.json",
        ],
        "reused_from": "code/M_SYNTH_182_1_out.json（2024 授权专利）, "
                       "code/M_SYNTH_VIT_RANK_out.json（高新技术企业数）",
        "scope": "深圳市 / 广州市 / 东莞市 / 惠州市",
        "evaluation_set": CITIES,
        "excluded_cities": [],
        "stat_year": 2024,
        "dims_definition": {
            "D1_产品服务创新": ["产品名称覆盖数", "第三产业增加值占比重"],
            "D2_企业创新": ["高新技术企业数", "企业授权专利数"],
            "D3_服务机构创新": ["创新服务机构绩效"],
        },
        "raw": {
            "产品名称覆盖数": raw_products,
            "第三产业增加值占比重": raw_tertiary,
            "高新技术企业数": raw_hightech,
            "企业授权专利数": raw_patents,
            "创新服务机构绩效": raw_svc,
            "产品标签企业数": raw_companies,
            "企均产品名": raw_density,
        },
        "norm_0_100": {
            "产品名称覆盖数": norm_products,
            "第三产业增加值占比重": norm_tertiary,
            "高新技术企业数": norm_hightech,
            "企业授权专利数": norm_patents,
            "创新服务机构绩效": norm_svc,
        },
        "norm_note": "D1/D2 的计数型子项做四市盘内极值归一；D3 保留固定词表 0—100 原标度，"
                     "因为其分母（6 类型 × 6 环节）是词表而不是本批城市集",
        "dim_detail": {
            "D1_产品服务创新": {"产品名称覆盖数": norm_products,
                                "第三产业增加值占比重": norm_tertiary},
            "D2_企业创新": {"高新技术企业数": norm_hightech,
                            "企业授权专利数": norm_patents},
            "D3_服务机构创新": {"创新服务机构绩效": norm_svc},
        },
        "dim_scores": dims,
        "n_dims_available": {c: sum(1 for k in dims if dims[k].get(c) is not None) for c in CITIES},
        "n_subs_available": {
            c: sum(1 for k in ("产品名称覆盖数", "第三产业增加值占比重", "高新技术企业数",
                               "企业授权专利数", "创新服务机构绩效")
                   if ({"产品名称覆盖数": norm_products,
                        "第三产业增加值占比重": norm_tertiary,
                        "高新技术企业数": norm_hightech,
                        "企业授权专利数": norm_patents,
                        "创新服务机构绩效": norm_svc}[k].get(c) is not None))
            for c in CITIES},
        "weights": {
            "main": w_main,
            "main_is_official": False,
            "rule": "三维等权（正本默认）；维内对非空子项等权，缺失子项不占权重、不补 0、不重归一",
        },
        "index_0_100": idx,
        "rank": rk,
        "coverage": {
            "sub_indicator_total": 5,
            "sub_indicator_filled": 4,
            "sub_indicator_filled_share_pct": round(100.0 * 4 / 5, 4),
            "product_tag_enterprise_share_pct": derived["product_tag_rows_over_base_orgs_pct"]["value"],
            "macro_pair_cities": macro["cities_with_pair_n"],
            "service_org_pool": panel["svc"]["pool"],
        },
        "derived": derived,
        "sensitivity": {
            "S0_main": {"index": idx, "rank": rk,
                        "note": "D3 用固定词表原标度；D1 用产品名总量"},
            "S1_service_minmax": {"index": s1, "rank": ranking(s1),
                                  "d3_normalized": d3_mm,
                                  "delta_vs_main": {c: round(s1[c] - idx[c], 4) for c in CITIES},
                                  "note": "D3 改批内极值：广州 34.25 被抬到 100、深圳 33.38 被压到 92.38"},
            "S2_product_density": {"index": s2, "rank": ranking(s2),
                                   "note": "D1 改企均产品名：惠州 3.7510 成为盘内最大，名次由第 4 升到第 2"},
            "S3_weight_bias": {"weights": w_bias, "index": s3, "rank": ranking(s3),
                               "note": "产品服务 0.50 / 企业 0.30 / 服务机构 0.20"},
            "S4_two_dim": {"weights": w_two, "index": s4, "rank": ranking(s4),
                           "note": "砍掉服务机构代理维后的二维盘"},
            "rank_stability": {
                "first_place_all_variants": all(
                    ranking(x)["深圳市"] == 1 for x in (idx, s1, s2, s3, s4)),
                "huizhou_rank_range": [min(ranking(x)["惠州市"] for x in (idx, s1, s2, s3, s4)),
                                       max(ranking(x)["惠州市"] for x in (idx, s1, s2, s3, s4))],
                "guangzhou_rank_range": [min(ranking(x)["广州市"] for x in (idx, s1, s2, s3, s4)),
                                         max(ranking(x)["广州市"] for x in (idx, s1, s2, s3, s4))],
            },
        },
        "absence_probe": absence_probe,
        "sub_unavailable": {
            "第三产业增加值占比重": "四市仅东莞 201706 存在同期间 JDZ 配对，其余三市两码期间不相交"
                                    "（深圳第三产业 JDZ+DNLJ 0 行）；1 城无法做四市极值归一，记 null",
        },
        "cross_sibling": {
            "M_SYNTH_VIT_INDEX": "该件产业维 12 分项里的『新产品销售收入占比』在本件不是子项"
                                 "（本件用第三产业占比重），两者不是同一把尺子",
            "M_SYNTH_VIT_DIM_SCORE": "该件产业维直接取本件综合分，逐城必须相同",
            "M_SYNTH_VIT_RANK": "该件产业维只用高企数（深圳 100、广州 44.31），本件是"
                                "高企 + 授权专利 + 产品 + 服务四路合成，故本件深圳 77.7925 低于 100",
        },
        "params": {
            "normalizer": "min-max（四市盘）",
            "agg_within_dim": "非空子项等权",
            "agg_across_dim": "三维等权",
            "missing_policy": "维内缺子项不补 0、不重归一；维级缺则整维 null 且不进加权",
        },
        "support_judgment": "部分支持",
        "support_reason": "三维里两维（企业创新、服务机构创新）有真值链且四城齐全；"
                          "产品服务创新维的『第三产业增加值占比重』四城只有 1 城有同期间事实，"
                          "整列记 null，实际退化成一个子项（产品名称覆盖数）单撑；"
                          "且产品标签只能覆盖底册 5.50% 的企业。按 §0.1 判部分支持。",
        "note": "产品标签表存在一列错位：company_name 存 18 位信用代码、credit_code 存产品名，"
                "按正本写法的 credit_code 关联会全部落空（本脚本按 company_name 关联）",
        "base_years_used": [2024],
        "base_years_missing": [],
        "base_years_note": "统计年 2024（授权专利完整年）；产品标签表无年份维度，取当前截面；"
                           "第三产业占比重唯一同期间对是东莞 2017 上半年，因只有 1 城未进任何归一，"
                           "不作为基期；研发投入列（arch_development_am）全表 0 非空，"
                           "故本件不含任何以研发投入为分母的比值",
        "elapsed_sec": round(time.time() - t0, 3),
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print("=== M_SYNTH_183_1 ===")
    for c in CITIES:
        print(f"{c}: D1={d1[c]} D2={d2[c]} D3={d3[c]} idx={idx[c]} rank={rk[c]}")
    print("S1", s1)
    print("S2", s2, ranking(s2))
    print(f"→ {OUT}")


if __name__ == "__main__":
    main()

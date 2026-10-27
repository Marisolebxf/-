#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""活力分项指标值与得分（M_SYNTH_VIT_INDICATOR）—— 复现脚本。

正本口径：展示活力四维背后的分项指标值与标准化得分，只汇总展示、不重算、不另选代表指标。
    科技 / 产业 / 人才 / 政策 的分项叶子分别见 M_SYNTH_182_1 / 183_1 / 184_1 / 185_1。

本件交付的是「正本 12 个分项 → 本库落地形态」这一张对照表：
每一行都写清原值、进维时实际用的标准化得分、以及该分项是直接可取 / 代理 / 有值但未进维 / 缺。
最后再用「12 分项重算」与四个子模型的综合分对一次账，用差额证明「只展示不重算」不是懒，
而是重算会给出另一个数。

运行：
    cd code && python3 M_SYNTH_VIT_INDICATOR.py
产物：
    code/M_SYNTH_VIT_INDICATOR_out.json
"""
from __future__ import annotations

import json
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
PANEL = os.path.join(SNAP, "vit_family_20261023.json")
ABSENCE = os.path.join(SNAP, "vit_absence_20261023.json")
OUT = os.path.join(HERE, "M_SYNTH_VIT_INDICATOR_out.json")

CITIES = ["深圳市", "广州市", "东莞市", "惠州市"]
TOL = 1e-9


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def mm(values: dict) -> dict:
    vals = [v for v in values.values() if v is not None]
    if not vals:
        return {c: None for c in values}
    lo, hi = min(vals), max(vals)
    if abs(hi - lo) < TOL:
        return {c: None for c in values}
    return {c: (None if v is None else round((v - lo) / (hi - lo) * 100.0, 4))
            for c, v in values.items()}


def main():
    t0 = time.time()
    panel = load(PANEL)
    absence = load(ABSENCE)
    m182 = load(os.path.join(HERE, "M_SYNTH_182_1_out.json"))
    m183 = load(os.path.join(HERE, "M_SYNTH_183_1_out.json"))
    m184 = load(os.path.join(HERE, "M_SYNTH_184_1_out.json"))
    m185 = load(os.path.join(HERE, "M_SYNTH_185_1_out.json"))
    dim = load(os.path.join(HERE, "M_SYNTH_VIT_DIM_SCORE_out.json"))
    rank = panel["submodels"]["rank_leaf_board"]["raw"]

    # ---------------------------------------------------------------- 12 分项
    # 原值一律取自「拥有该叶子的子模型产物」，不在本件重查库。
    g_grants = {c: m182["dims"]["D2_applied_tech"]["grants_2024"][c] for c in CITIES}
    g_hq = {c: rank["high_cited_papers"][c] for c in CITIES}
    g_transfer = {c: m182["dims"]["D2_applied_tech"]["transfers_2024"][c] for c in CITIES}
    g_hightech = {c: rank["hightech_enterprises"][c] for c in CITIES}
    g_svc = {c: m183["raw"]["创新服务机构绩效"][c] for c in CITIES}
    g_hiedu = {c: m184["raw"]["硕博学者占比"][c] for c in CITIES}
    g_output = {c: m184["raw"]["论文+H指数"][c] for c in CITIES}
    g_policy = {c: m185["raw"]["市级有效政策存量"][c] for c in CITIES}
    g_ptype = {c: m185["raw"]["文件体裁覆盖度"][c] for c in CITIES}

    s_grants = mm(g_grants)
    s_hq = mm(g_hq)
    s_transfer = mm(g_transfer)
    s_hightech = mm(g_hightech)
    # 服务机构：固定词表 0—100，保留原标度（与 183 一致）
    s_svc = {c: g_svc[c] for c in CITIES}
    # 人才成果产出：取 184 D4 内的标准化分（该维 4 个子项等权，取其中一项会失真，
    # 故本行只报「该子项在 184 D4 里的标准化分」，并在 note 里写明它不等于 D4）
    s_output = {c: m184["dim_detail_norm"]["D4_成果产出"][c]["论文+H指数"] for c in CITIES}
    # 政策数量与类型覆盖：取 185 维内标准化分 / 原标度
    s_policy = {c: m185["dim_detail_norm"]["D1_政策数量"][c]["市级有效政策存量"]
                for c in CITIES} if "dim_detail_norm" in m185 else mm(g_policy)
    s_ptype = {c: g_ptype[c] for c in CITIES}

    leaves = [
        {"dim": "科技", "name": "专利授权量", "raw": g_grants, "score": s_grants,
         "status": "直接", "enters_dim": True,
         "note": "2024 年授权专利去重数（182 D2 叶子）；四市齐全"},
        {"dim": "科技", "name": "高质量论文数量", "raw": g_hq, "score": s_hq,
         "status": "直接", "enters_dim": True,
         "note": "被引 ≥ 本批 P70（6 次）的论文去重数；182 D1 另用『高质量期刊』口径"
                 "（深圳 239 / 广州 493 / 东莞 16 / 惠州 9），两者不是同一列"},
        {"dim": "科技", "name": "技术转化成效", "raw": g_transfer, "score": s_transfer,
         "status": "代理", "enters_dim": True,
         "note": "正本是『专利转移去重数 ÷ 研发投入合计』；研发投入列 arch_development_am "
                 "全表 0 非空，分母不存在，故只用分子（转移件数）归一"},
        {"dim": "产业", "name": "高新技术企业数量", "raw": g_hightech, "score": s_hightech,
         "status": "直接", "enters_dim": True,
         "note": "国家级高企去重数（org_tag 含高新技术企业）；四市齐全"},
        {"dim": "产业", "name": "新产品销售收入占比", "raw": {c: None for c in CITIES},
         "score": {c: None for c in CITIES}, "status": "缺", "enters_dim": False,
         "note": "指标码 a77234 在 dwd_macro_index_data 为 0 行（a772* 家族只有 6 个别的码，各 1 行）；"
                 "且分母『企业主营业务收入合计』依赖 annual_fin，该表 90,926 行里 "
                 "main_business_revenue 仅 2,040 行非空"},
        {"dim": "产业", "name": "创新服务机构绩效", "raw": g_svc, "score": s_svc,
         "status": "直接", "enters_dim": True,
         "note": "沿用 M_SVC_ORG_COVERAGE_DEPTH；分母是固定词表 6 类型 × 6 环节，保留 0—100 原标度"},
        {"dim": "人才", "name": "研发人员数量", "raw": {c: None for c in CITIES},
         "score": {c: None for c in CITIES}, "status": "缺", "enters_dim": False,
         "note": "dwd_org_annual_financial_info.development_employee 90,926 行、非空 0 行（整列空）"},
        {"dim": "人才", "name": "高学历人才占比", "raw": g_hiedu,
         "score": {c: None for c in CITIES}, "status": "有值未进维", "enters_dim": False,
         "note": "四位城市里只有深圳 100.0、广州 97.4026 有值，两城相差 2.5974 个百分点；"
                 "184 判其饱和（四城盘上会被拉成 100 对 0），整维记 null 不进加权"},
        {"dim": "人才", "name": "人才成果产出", "raw": g_output, "score": s_output,
         "status": "直接", "enters_dim": True,
         "note": "论文数 + H 指数合计；正本的人均式（÷ 研发人员总数）因分母整列空不可算，"
                 "故用绝对量，184 D4 内再与授权专利/转移/院士等权"},
        {"dim": "政策", "name": "产业创新政策数量", "raw": g_policy, "score": s_policy,
         "status": "直接", "enters_dim": True,
         "note": "市级有效政策存量（185 D1）；四市齐全，惠州 0 条是实测而不是缺测"},
        {"dim": "政策", "name": "政策类型覆盖度", "raw": g_ptype, "score": s_ptype,
         "status": "直接", "enters_dim": True,
         "note": "按 13 类固定词表计覆盖（185 D2）；分母是词表，不做批内极值"},
        {"dim": "政策", "name": "政策实施效果指数", "raw": {c: None for c in CITIES},
         "score": {c: None for c in CITIES}, "status": "缺", "enters_dim": False,
         "note": "实施时效性与政策可见度两子项均不可用：implementation_date/expire_date "
                 "20,000 行全部 '0000-00-00'；link 列 100% 非空，归一后整列无定义"},
    ]

    # ---------------------------------------------------------------- 覆盖率
    n_total = len(leaves)
    n_scored = sum(1 for x in leaves if x["status"] in ("直接", "代理") and x["enters_dim"])
    n_has_value = sum(1 for x in leaves if any(v is not None for v in x["raw"].values()))
    n_missing = sum(1 for x in leaves if x["status"] == "缺")
    by_dim = {}
    for d in ["科技", "产业", "人才", "政策"]:
        rows = [x for x in leaves if x["dim"] == d]
        by_dim[d] = {
            "leaves": len(rows),
            "scored_entered": sum(1 for x in rows if x["enters_dim"]),
            "has_value": sum(1 for x in rows if any(v is not None for v in x["raw"].values())),
            "missing": sum(1 for x in rows if x["status"] == "缺"),
        }

    # ---------------------------------------------------------------- 重算对账
    # 用「12 分项等权」重算四维，与子模型综合分比。差额就是「不能重算」的证据。
    recompute = {}
    reconcile = {}
    for d in ["科技", "产业", "人才", "政策"]:
        rows = [x for x in leaves if x["dim"] == d and x["enters_dim"]]
        rec = {}
        for c in CITIES:
            vals = [x["score"][c] for x in rows if x["score"].get(c) is not None]
            rec[c] = round(sum(vals) / len(vals), 4) if vals else None
        recompute[d] = rec
        published = m183["index_0_100"] if d == "产业" else None
        published = {
            "科技": m182["index_0_100"], "产业": m183["index_0_100"],
            "人才": m184["index_0_100"], "政策": m185["index_0_100"],
        }[d]
        reconcile[d] = {
            "recompute_12leaf": rec,
            "sub_model_index": {c: published[c] for c in CITIES},
            "diff": {c: (None if (rec[c] is None or published[c] is None)
                         else round(rec[c] - published[c], 4))
                     for c in CITIES},
            "entered_leaves": [x["name"] for x in rows],
            "not_entered": [x["name"] for x in leaves if x["dim"] == d and not x["enters_dim"]],
        }
    max_abs_diff = max(abs(v) for d in reconcile for v in reconcile[d]["diff"].values()
                       if v is not None)

    derived = {
        "leaf_coverage_share": {
            "value": {"scored": round(n_scored / n_total, 4),
                      "has_value": round(n_has_value / n_total, 4),
                      "missing": round(n_missing / n_total, 4)},
            "numerator": {"scored": n_scored, "has_value": n_has_value, "missing": n_missing},
            "denominator": n_total,
            "denominator_note": "分母 = 正本 12 个分项；scored = 有标准化得分且进维，"
                                "has_value = 至少一城有原值，missing = 四城全缺",
        },
        "dim_leaf_coverage": {
            "value": {d: round(by_dim[d]["scored_entered"] / by_dim[d]["leaves"], 4)
                      for d in by_dim},
            "numerator": {d: by_dim[d]["scored_entered"] for d in by_dim},
            "denominator": {d: by_dim[d]["leaves"] for d in by_dim},
            "denominator_note": "分母 = 该维分项数（3/3/3/3）；分子 = 有得分并进维的分项数（3/2/1/2）",
        },
        "recompute_vs_submodel_max_abs_diff": {
            "value": round(max_abs_diff, 4),
            "numerator": round(max_abs_diff, 4), "denominator": 1,
            "denominator_note": "分母取 1（单位为分，不是比值）；分子 = 四城四维里"
                                "『12 分项重算』与『子模型综合分』绝对差的最大值",
        },
        "hiedu_gap_pp_sz_gz": {
            "value": round(g_hiedu["深圳市"] - g_hiedu["广州市"], 4),
            "numerator": g_hiedu["深圳市"], "denominator": g_hiedu["广州市"],
            "denominator_note": "硕博学者占比（%）：深圳 100.0 − 广州 97.4026，单位百分点；"
                                "两城相差 2.5974 个百分点却被四城盘拉到 100 对 0，故不进维",
        },
    }

    absence_probe = [
        {"target": "新产品销售收入占比（产业维）",
         "table": "gkx.dwd_macro_index_data", "condition": "index_code='a77234'",
         "rows": int(absence["a77234_n"][0][0]), "hit": "0 行",
         "consequence": "指标码不存在；a772* 家族只有 6 个别的码（各 1 行），"
                        "无法用别的码顶替，故该分项记 null"},
        {"target": "研发人员数量（人才维）",
         "table": "gkx.dwd_org_annual_financial_info",
         "condition": "COUNT(*), SUM(development_employee IS NOT NULL)",
         "rows": int(absence["fin_cols"][0][0]), "hit": "0 行非空",
         "consequence": "整列空；人才数量维只剩学者存量一个子项"},
        {"target": "政策实施效果指数（政策维）",
         "table": "gkx.dwd_policy_base",
         "condition": "SUM(CAST(implementation_date AS CHAR)='0000-00-00'), "
                      "SUM(CAST(expire_date AS CHAR)='0000-00-00'), SUM(link<>'')",
         "rows": int(absence["policy_date"][0][0]), "hit": "20,000 行零日期 / 20,000 行 link 非空",
         "consequence": "时效性与可见度两子项都退化为常数，政策效果维整维 null"},
    ]

    out = {
        "metric_id": "M_SYNTH_VIT_INDICATOR",
        "metric_name": "活力分项指标值与得分",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "verdict_kind": "negative_evidence",
        "verdict_kind_note": "判部分支持，且 12 个分项里 3 个四城全缺（25%），故按 v8 §四留 absence_probe",
        "source": {
            "library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
            "mode": "read-only", "touched": False,
            "note": "本件不新建查询：12 分项全部来自四个子模型产物与族级面板",
        },
        "sources": [
            "code/_snapshots21/vit_family_20261023.json",
            "code/_snapshots21/vit_absence_20261023.json",
            "code/M_SYNTH_182_1_out.json", "code/M_SYNTH_183_1_out.json",
            "code/M_SYNTH_184_1_out.json", "code/M_SYNTH_185_1_out.json",
        ],
        "reused_from": "code/M_SYNTH_182_1_out.json, code/M_SYNTH_183_1_out.json, "
                       "code/M_SYNTH_184_1_out.json, code/M_SYNTH_185_1_out.json",
        "scope": "深圳市 / 广州市 / 东莞市 / 惠州市",
        "evaluation_set": CITIES,
        "stat_year": 2024,
        "leaves": leaves,
        "leaf_coverage": {"total": n_total, "scored_entered": n_scored,
                          "has_value": n_has_value, "missing": n_missing,
                          "by_dim": by_dim},
        "dim_scores": dim["dim_scores"],
        "dim_rank": dim["dim_rank"],
        "recompute_check": reconcile,
        "derived": derived,
        "weights": {
            "main": None, "main_is_official": False,
            "rule": "本件不合成：只展示分项值与进维得分；四维分取 M_SYNTH_VIT_DIM_SCORE，"
                    "总指数见 186_1 / VIT_INDEX",
        },
        "absence_probe": absence_probe,
        "support_judgment": "部分支持",
        "support_reason": "12 个分项里 8 个有标准化得分并进维、1 个（高学历人才占比）有值但因饱和"
                          "未进维、3 个（新产品销售收入占比 / 研发人员数量 / 政策实施效果指数）"
                          "四城全缺；其中两个缺项是整列空（研发人员、政策日期），一个是指标码不存在"
                          "（a77234）。按 §0.1 判部分支持。",
        "note": "本件是唯一「只展示不重算」的件：12 分项等权重算出来的四维分与子模型综合分最大差 "
                f"{round(max_abs_diff, 4)} 分（政策维差 0.0077，产业维差 11.10 量级），"
                "说明分项集合本身与子模型的叶子集合不同，重算会造出第二套四维分",
        "base_years_used": [2024],
        "base_years_missing": [],
        "base_years_note": "统计年 2024；高质量论文为全历史累计的高被引池（阈值 6 次），"
                           "与 2024 年授权专利不同源，故四维不是同一时间窗；"
                           "政策存量是当前有效集而不是 2024 年出台量",
        "elapsed_sec": round(time.time() - t0, 3),
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print("=== M_SYNTH_VIT_INDICATOR ===")
    print(f"12 分项: 进维 {n_scored} / 有值 {n_has_value} / 缺 {n_missing}")
    for d in reconcile:
        print(d, "重算", reconcile[d]["recompute_12leaf"],
              "子模型", reconcile[d]["sub_model_index"], "差", reconcile[d]["diff"])
    print("最大绝对差", round(max_abs_diff, 4))
    print(f"→ {OUT}")


if __name__ == "__main__":
    main()

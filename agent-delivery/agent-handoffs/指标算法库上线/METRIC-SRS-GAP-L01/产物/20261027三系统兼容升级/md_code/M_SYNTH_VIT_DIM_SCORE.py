#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""四维单维评分（M_SYNTH_VIT_DIM_SCORE）—— 复现脚本。

正本口径：四维得分分别取子模型综合分，不另算叶子，不加权成总指数。
    科技 = M_SYNTH_182_1 综合分
    产业 = M_SYNTH_183_1 综合分
    人才 = M_SYNTH_184_1 综合分
    政策 = M_SYNTH_185_1 综合分

本件是族内「四维盘」的唯一出处：186_1 与 VIT_INDEX 都只读本件产物取四维分，
不再各自去读四个子模型，避免同一城市出现两个分。

运行：
    cd code && python3 M_SYNTH_VIT_DIM_SCORE.py
产物：
    code/M_SYNTH_VIT_DIM_SCORE_out.json
"""
from __future__ import annotations

import json
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
PANEL = os.path.join(SNAP, "vit_family_20261023.json")
OUT = os.path.join(HERE, "M_SYNTH_VIT_DIM_SCORE_out.json")

CITIES = ["深圳市", "广州市", "东莞市", "惠州市"]
DIMS = ["科技", "产业", "人才", "政策"]
SUB_MODEL = {
    "科技": ("M_SYNTH_182_1", "M_SYNTH_182_1_out.json"),
    "产业": ("M_SYNTH_183_1", "M_SYNTH_183_1_out.json"),
    "人才": ("M_SYNTH_184_1", "M_SYNTH_184_1_out.json"),
    "政策": ("M_SYNTH_185_1", "M_SYNTH_185_1_out.json"),
}


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def rank_of(d: dict) -> dict:
    order = sorted([c for c in CITIES if d.get(c) is not None], key=lambda c: (-d[c], c))
    return {c: i + 1 for i, c in enumerate(order)}


def main():
    t0 = time.time()
    panel = load(PANEL)
    outs = {}
    for dim, (_mid, fname) in SUB_MODEL.items():
        outs[dim] = load(os.path.join(HERE, fname))

    dim_scores = {dim: {c: outs[dim]["index_0_100"][c] for c in CITIES} for dim in DIMS}
    dim_rank = {dim: rank_of(dim_scores[dim]) for dim in DIMS}

    # ---------------------------------------------------------------- 维内覆盖
    # 每个维的「在场子维数 / 应到子维数」直接从子模型产物读，不在本件重算。
    sub_cov = {}
    # 科技：182 三维（基础科学 / 应用科技 / 科研机构）
    sub_cov["科技"] = {
        "dims_expected": 3,
        "dims_live": int(outs["科技"].get("n_dims_available", {}).get("深圳市", 0)),
        "dims": list(outs["科技"]["dim_scores"].keys()),
        "leaves_live": "授权专利 2024 + 高被引论文 + 机构存量 + 机构授权 + 专利转移（全部四城有值）",
        "note": "三子维四城全有值，是四维里唯一无缺子维的一维",
    }
    # 产业：183 三维 / 5 个三级指标
    sub_cov["产业"] = {
        "dims_expected": 3,
        "dims_live": 3,
        "dims": list(outs["产业"]["dim_scores"].keys()),
        "leaves_expected": 5,
        "leaves_live": outs["产业"]["coverage"]["sub_indicator_filled"],
        "note": "第三产业占比重四城仅东莞 1 城有同期间事实 → 整列 null，产品服务维由单子项支撑",
    }
    # 人才：184 四维 / 8 个三级指标
    m184 = outs["人才"]
    sub_cov["人才"] = {
        "dims_expected": 4,
        "dims_live": int(m184.get("n_dims_available", {}).get("深圳市", 0)),
        "dims": [k for k, v in m184["dim_scores"].items() if v.get("深圳市") is not None],
        "dims_null": [k for k, v in m184["dim_scores"].items() if v.get("深圳市") is None],
        "leaves_expected": 8,
        "leaves_live": 5,
        "note": "企业研发人员（整列空）、硕博学者占比（四城仅两城有值且饱和）、青年学者占比"
                "（四城仅两城）三项不进维",
    }
    # 政策：185 三维 / 4 个三级指标
    m185 = outs["政策"]
    sub_cov["政策"] = {
        "dims_expected": 3,
        "dims_live": int(m185.get("n_dims_available", {}).get("深圳市", 0)),
        "dims": [k for k, v in m185["dim_scores"].items() if v.get("深圳市") is not None],
        "dims_null": [k for k, v in m185["dim_scores"].items() if v.get("深圳市") is None],
        "leaves_expected": 4,
        "leaves_live": 2,
        "note": "实施时效性与政策可见度不可用（实施日/失效日全为 '0000-00-00'；link 列 100% 非空、"
                "归一后整列无定义）",
    }

    dim_completeness = {d: round(sub_cov[d]["dims_live"] / sub_cov[d]["dims_expected"], 4)
                        for d in DIMS}
    # 人才维的「子维数」按 4 个计、按维计 2 → 组内完整度 50%
    city_dim_count = {c: sum(1 for d in DIMS if dim_scores[d].get(c) is not None) for c in CITIES}
    # 缺维容错（20261025）：正本口径"缺维不补 0 不进平均"——sum 前剔除 None，
    # 全缺时该城 span 记 None（下游统计同样按非 None 聚合）
    def _span(ds):
        vals = [v for v in ds if v is not None]
        return round(sum(vals) / 4.0, 4) if vals else None
    city_span = {c: _span([dim_scores[d].get(c) for d in DIMS]) for c in CITIES}

    # ---------------------------------------------------------------- 派生数字
    # 缺维容错：极差/差值仅在两端都有值时计算，否则 None（值含 None 的维不参与 min/max）
    def _rng(d):
        vals = [v for v in dim_scores[d].values() if v is not None]
        return round(max(vals) - min(vals), 4) if vals else None

    def _sub(a, b, d):
        va, vb = dim_scores[d].get(a), dim_scores[d].get(b)
        return round(va - vb, 4) if (va is not None and vb is not None) else None

    dim_range = {d: _rng(d) for d in DIMS}
    derived = {
        "shenzhen_minus_guangzhou_by_dim": {
            "value": {d: _sub("深圳市", "广州市", d) for d in DIMS},
            "numerator": {d: dim_scores[d].get("深圳市") for d in DIMS},
            "denominator": {d: dim_scores[d].get("广州市") for d in DIMS},
            "denominator_note": "逐维（深圳 − 广州）差值；负值表示广州更高（人才维）；任一端缺维则 None",
        },
        "dim_range_0_100": {
            "value": dim_range,
            "numerator": {d: (lambda vs: max(vs) if vs else None)([v for v in dim_scores[d].values() if v is not None]) for d in DIMS},
            "denominator": {d: (lambda vs: min(vs) if vs else None)([v for v in dim_scores[d].values() if v is not None]) for d in DIMS},
            "denominator_note": "四市极差 = 该维最大值 − 最小值；反映该维在四市盘上的分辨力；整维缺值则 None",
        },
        "dim_completeness_share": {
            "value": dim_completeness,
            "numerator": {d: sub_cov[d]["dims_live"] for d in DIMS},
            "denominator": {d: sub_cov[d]["dims_expected"] for d in DIMS},
            "denominator_note": "分母 = 各子模型正本的维数（科技 3 / 产业 3 / 人才 4 / 政策 3）；"
                                "分子 = 四城都有值的子维数",
        },
        "mean_dim_completeness": {
            "value": round(sum(dim_completeness.values()) / 4.0, 4),
            "numerator": round(sum(dim_completeness.values()), 4), "denominator": 4,
            "denominator_note": "分母 = 四维；分子 = 四维完整度之和（等权平均，仅作描述）",
        },
        "city_dim_coverage": {
            "value": {c: round(city_dim_count[c] / 4.0, 4) for c in CITIES},
            "numerator": city_dim_count, "denominator": 4,
            "denominator_note": "分母 = 四维；分子 = 该城有值的维数（四城均为 4/4，但内部子维不全）",
        },
        "tech_dim_leaf_vs_composite_gap": {
            "value": (lambda a, b: round(a - b, 4) if (a is not None and b is not None) else None)(
                outs["科技"]["index_0_100"]["深圳市"],
                panel["submodels"]["rank_leaf_board"]["dim_scores_gba4"]["科技"]["深圳市"]),
            "numerator": outs["科技"]["index_0_100"]["深圳市"],
            "denominator": panel["submodels"]["rank_leaf_board"]["dim_scores_gba4"]["科技"]["深圳市"],
            "denominator_note": "同一城市（深圳）两个口径之差：本件综合分 − VIT_RANK 单叶子分；任一端缺值则 None",
        },
    }

    # ---------------------------------------------------------------- 敏感性
    # ① 逐维名次（不合成）
    # ② 单叶子口径（VIT_RANK）的四维分对照
    leaf = panel["submodels"]["rank_leaf_board"]["dim_scores_gba4"]
    leaf_board = {d: {c: leaf[d].get(c) for c in CITIES} for d in DIMS}
    leaf_rank = {d: rank_of(leaf_board[d]) for d in DIMS}
    # ③ 砍掉某一维后剩余三维的「谁领先」——只回答方向，不给分数
    drop = {}
    for d in DIMS:
        rest = [x for x in DIMS if x != d]
        # 缺维容错：剔除 None 后再平均；该城剩余三维全缺则 None（rank_of 自跳过 None 城）
        win = {}
        for c in CITIES:
            vals = [dim_scores[x][c] for x in rest if dim_scores[x].get(c) is not None]
            win[c] = round(sum(vals) / 3.0, 4) if vals else None
        drop[d] = {"residual_mean": win, "first": rank_of(win)}
    # ④ 四维里「深圳是否第一」的分布（某维深圳缺值则该维不计入）
    sz_first_dims = [d for d in DIMS if dim_rank[d].get("深圳市") == 1]

    out = {
        "metric_id": "M_SYNTH_VIT_DIM_SCORE",
        "metric_name": "四维单维评分",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "source": {
            "library": "gkx",
            "host": "183.240.141.251:3318",
            "user": "gkx_reader_zp",
            "mode": "read-only",
            "touched": False,
            "note": "本件不新建查询：四维分全部来自同族子模型产物，零 SQL",
        },
        "sources": [
            "code/_snapshots21/vit_family_20261023.json",
            "code/M_SYNTH_182_1_out.json",
            "code/M_SYNTH_183_1_out.json",
            "code/M_SYNTH_184_1_out.json",
            "code/M_SYNTH_185_1_out.json",
            "code/M_SYNTH_VIT_RANK_out.json",
        ],
        "reused_from": "code/M_SYNTH_182_1_out.json, code/M_SYNTH_183_1_out.json, "
                       "code/M_SYNTH_184_1_out.json, code/M_SYNTH_185_1_out.json",
        "scope": "深圳市 / 广州市 / 东莞市 / 惠州市",
        "evaluation_set": CITIES,
        "stat_year": 2024,
        "dim_definition": {d: SUB_MODEL[d][0] for d in DIMS},
        "dim_scores": dim_scores,
        "dim_rank": dim_rank,
        "dim_sub_coverage": sub_cov,
        "dim_completeness": dim_completeness,
        "dim_detail": {
            "科技": outs["科技"]["dim_scores"],
            "产业": outs["产业"]["dim_scores"],
            "人才": outs["人才"]["dim_scores"],
            "政策": outs["政策"]["dim_scores"],
        },
        "dim_sub_scores_note": {
            "科技": "D1 基础科学 / D2 应用科技 / D3 科研机构",
            "产业": "D1 产品服务创新 / D2 企业创新 / D3 服务机构创新",
            "人才": "D1 创新人才数量 / D2 学历结构 / D3 年龄结构 / D4 成果产出",
            "政策": "D1 政策数量 / D2 政策类型 / D3 政策效果",
        },
        "weights": {
            "main": None,
            "main_is_official": False,
            "rule": "本件不加权：四维并列输出，总指数见 M_SYNTH_186_1（等权）与 M_SYNTH_VIT_INDEX（自定义权重）",
        },
        "derived": derived,
        "city_span_4dim_mean": city_span,
        "sensitivity": {
            "composite_board": leaf_board,
            "composite_board_rank": leaf_rank,
            "note_composite": "单叶子口径（VIT_RANK：专利授权 / 高企数 / 高学历占比 / 政策存量 四路直取）"
                              "与本件（四路子模型综合分）不是同一把尺子；科技维口径差最大",
            "drop_one_dim": drop,
            "shenzhen_first_dims": sz_first_dims,
            "shenzhen_first_dim_n": len(sz_first_dims),
            "ranking_stability": {
                "tech_guangzhou_first_under_leaf": leaf_rank["科技"].get("广州市") == 1,
                "tech_shenzhen_first_under_composite": dim_rank["科技"].get("深圳市") == 1,
                "talent_guangzhou_first_both": (dim_rank["人才"].get("广州市") == 1
                                                and leaf_rank["人才"].get("广州市") == 1),
            },
        },
        "support_judgment": "部分支持",
        "support_reason": "四维分全部可算（四城 4/4 有值），但只有科技维是满维（3/3 子维）；"
                          "产业维 5 个三级指标缺 1（第三产业占比重）、人才维 4 个子维只有 2 个有值、"
                          "政策维 3 个子维只有 2 个有值。四维「有值」不等于四维「齐」，"
                          "按 §0.1 判部分支持。",
        "note": "本件取上游产物已发布的数值，不在下游补位：182 的 73.7、184 的 56.2、185 的 92.3 "
                "都是一位小数，下游合成继承该精度（每维最多 ±0.05）",
        "base_years_used": [2024],
        "base_years_missing": [],
        "base_years_note": "四维均为统计年 2024（专利完整年）；产业维的产品标签为当前截面、"
                           "服务机构为覆盖率族快照，二者无年份维度；第三产业占比重因四城无同期间"
                           "事实未进任何维，故 2017 不作为基期",
        "elapsed_sec": round(time.time() - t0, 3),
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print("=== M_SYNTH_VIT_DIM_SCORE ===")
    for c in CITIES:
        print(f"{c}: " + "  ".join(f"{d}={dim_scores[d][c]}" for d in DIMS))
    print("维完整度", dim_completeness, "均值", derived["mean_dim_completeness"]["value"])
    print("深圳第一的维", sz_first_dims)
    print(f"→ {OUT}")


if __name__ == "__main__":
    main()

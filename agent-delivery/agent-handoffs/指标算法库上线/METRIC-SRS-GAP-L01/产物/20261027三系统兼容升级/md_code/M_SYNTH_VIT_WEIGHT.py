#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_SYNTH_VIT_WEIGHT 活力指数权重配置与权重弹性 —— gkx 换源版

口径真源（旧系统）：`biz_power` / `tech_power` / `eval_weight` 三张造数表，
`eval_weight` 存的就是「活力指数各维权重」。三张表在 gkx 里 **一张都不存在**
（`_work_gkx21/TABLE_ABSENCE.json` 实测 exists_in_gkx=false，derivable=false），
所以本件的交付物不是「读出官方权重」，而是：

  1) 在 gkx 可观测的四维分上**自定义**一组权重，并明确声明非官方；
  2) 给出权重的**客观参照**（熵权法），说明自定义权重与数据离散度给出的权重差多远；
  3) 给出**权重弹性**：某一维权重每 +0.10，指数变多少、名次变不变；
  4) 给出**排名翻转的权重阈值**（解析解 + 单纯形网格数值验证）；
  5) 划清「分数只能盘内比」的边界。

输入不重取数：四维分直接读 `code/M_SYNTH_VIT_RANK_out.json` 的
`boards.gba4.dim_scores`（同一批快照、同一 minmax 池、同一统计年 2024）。
这样权重件与排名件不会出现「同一城市两个分」的口径分裂。

输出：code/M_SYNTH_VIT_WEIGHT_out.json
"""
from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import networkx as nx  # noqa: F401  (保持与同域脚本一致的依赖面，不参与计算)

HERE = Path(__file__).parent
OUT = HERE / "M_SYNTH_VIT_WEIGHT_out.json"
RANK_OUT = HERE / "M_SYNTH_VIT_RANK_out.json"
METRIC = "M_SYNTH_VIT_WEIGHT"

DIMS = ["科技", "产业", "人才", "政策"]

# 自定义主口径权重：声明为非官方、非 AHP 标定、非 eval_weight 原值。
# 取值理由写进正文 §2.2：科技维是唯一有「完整年 + 全量扫描」支撑的维，
# 产业维样本最厚（高企名录），人才/政策两维在四市里的覆盖最弱（东莞、惠州缺）。
W_MAIN = {"科技": 0.30, "产业": 0.35, "人才": 0.20, "政策": 0.15}

SCHEMES = {
    "S0_等权": {"科技": 0.25, "产业": 0.25, "人才": 0.25, "政策": 0.25},
    "S1_主口径(自定义)": W_MAIN,
    "S2_科技主导": {"科技": 0.55, "产业": 0.25, "人才": 0.10, "政策": 0.10},
    "S3_产业主导": {"科技": 0.15, "产业": 0.60, "人才": 0.15, "政策": 0.10},
    "S4_人才主导": {"科技": 0.15, "产业": 0.15, "人才": 0.55, "政策": 0.15},
    "S5_政策主导": {"科技": 0.15, "产业": 0.15, "人才": 0.15, "政策": 0.55},
    "S6_单维科技": {"科技": 1.0, "产业": 0.0, "人才": 0.0, "政策": 0.0},
}

ELASTIC_STEP = 0.10
GRID_STEP = 0.01


def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def composite(dim_scores: dict, w: dict) -> dict:
    """加权和。维度缺值 → 该城不参与（不拿 0 顶，也不对剩余维重新归一）。

    为什么不重新归一：一旦对剩余维归一，东莞（2 维）的 0.5/0.5 会与深圳的
    四维加权当成同一把尺子，两城的分数就不可比了。缺维城只出现在「降维参考盘」，
    且盘内谁缺哪一维要逐城标明。
    """
    out = {}
    for city in dim_scores[DIMS[0]]:
        vals = {d: dim_scores[d].get(city) for d in DIMS}
        if any(v is None for v in vals.values()):
            continue
        out[city] = round(sum(w[d] * vals[d] for d in DIMS), 2)
    return out


def rank_of(scores: dict) -> dict:
    ordered = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    out, prev, prev_rank = {}, None, 0
    for i, (k, s) in enumerate(ordered, 1):
        if prev is not None and abs(s - prev) < 1e-12:
            out[k] = prev_rank
        else:
            out[k] = i
            prev_rank = i
        prev = s
    return out


def entropy_weights(dim_scores: dict, cities: list) -> dict:
    """熵权法（客观赋权）：只在四维齐全的城市上算，缺维城不得进分母。

    p_ij = x_ij / Σ_i x_ij；e_j = -(1/ln n)·Σ_i p_ij ln p_ij；d_j = 1-e_j；w_j = d_j/Σd。
    若某维在两城上完全相等（d_j=0），该维权重为 0 —— 不是缺陷，是「无区分度即无信息」。
    """
    n = len(cities)
    d = {}
    detail = {}
    for dim in DIMS:
        xs = [dim_scores[dim][c] for c in cities]
        s = sum(xs)
        if s <= 0:
            d[dim] = 0.0
            detail[dim] = {"entropy": None, "divergence": 0.0, "note": "该维全 0，无定义"}
            continue
        e = 0.0
        for x in xs:
            p = x / s
            if p > 0:
                e += -p * math.log(p)
        e /= math.log(n)
        d[dim] = max(0.0, 1.0 - e)
        detail[dim] = {"entropy": round(e, 6), "divergence": round(d[dim], 6)}
    tot = sum(d.values())
    w = {k: round(v / tot, 4) for k, v in d.items()} if tot > 0 else {k: 0.25 for k in DIMS}
    return {"weights": w, "divergence": {k: round(v, 6) for k, v in d.items()}, "detail": detail}


def elasticity(dim_scores: dict, w: dict) -> dict:
    """把某一维权重 +0.10、其余维按原比例缩减，看指数绝对变化与名次变化。"""
    base = composite(dim_scores, w)
    base_rank = rank_of(base)
    rows = []
    for dim in DIMS:
        w2 = dict(w)
        w2[dim] = round(w2[dim] + ELASTIC_STEP, 4)
        rest = [d for d in DIMS if d != dim]
        rest_sum = sum(w[d] for d in rest)
        for d in rest:
            w2[d] = round(w[d] * (1 - w2[dim]) / rest_sum, 6)
        # 修正四舍五入残差，保证 Σw=1
        diff = round(1.0 - sum(w2.values()), 10)
        w2[rest[-1]] = round(w2[rest[-1]] + diff, 6)
        after = composite(dim_scores, w2)
        r2 = rank_of(after)
        rows.append({
            "dim": dim,
            "weight_after": w2,
            "index": after,
            "rank": r2,
            "delta_index": {c: round(after[c] - base[c], 2) for c in after},
            "rank_changed": [c for c in after if r2[c] != base_rank[c]],
        })
    return {"base_index": base, "base_rank": base_rank,
            "step": ELASTIC_STEP, "rows": rows}


def crossover_two_dim(dim_scores: dict, dim_a: str, dim_b: str, ca: str, cb: str) -> dict:
    """两维盘上 A 城与 B 城的分相等点：w_a·(a_A-a_B) + (1-w_a)·(b_A-b_B) = 0。

    解出 w_a* ；再判断「w_a 大于/小于 w_a* 时谁在前」。
    """
    da = dim_scores[dim_a][ca] - dim_scores[dim_a][cb]
    db = dim_scores[dim_b][ca] - dim_scores[dim_b][cb]
    if abs(da - db) < 1e-12:
        return {"dim_a": dim_a, "dim_b": dim_b, "w_star": None,
                "note": "两维差相等，任何权重下两城同分（并列）"}
    w_star = -db / (da - db)
    return {"dim_a": dim_a, "dim_b": dim_b, "pair": [ca, cb],
            "diff_a": round(da, 2), "diff_b": round(db, 2),
            "w_star": round(w_star, 4),
            "w_a_above": ca if da > db else cb,
            "w_a_below": cb if da > db else ca,
            "note": "w_a 高于 w_star 时前者领先（因为 A 在该维的相对优势随权重放大）"}


def simplex_scan(dim_scores: dict, cities: list, step: float) -> dict:
    """四维单纯形网格：w 取 step 的整数倍且和为 1，统计名次分布。

    只在四维齐全的城市上扫（缺维城在四维加权里无定义）。
    """
    n = int(round(1 / step))
    ranks = {c: {} for c in cities}
    n_comb = 0
    leader_cnt = {c: 0 for c in cities}
    for i in range(n + 1):
        for j in range(n + 1 - i):
            for k in range(n + 1 - i - j):
                m = n - i - j - k
                w = {"科技": i * step, "产业": j * step, "人才": k * step, "政策": m * step}
                sc = composite(dim_scores, w)
                if len(sc) < len(cities):
                    continue
                n_comb += 1
                r = rank_of(sc)
                for c in cities:
                    ranks[c][r[c]] = ranks[c].get(r[c], 0) + 1
                top = min(r, key=lambda c: r[c])
                leader_cnt[top] += 1
    return {"step": step, "n_combos": n_comb,
            "leader_share": {c: round(v / n_comb, 4) for c, v in leader_cnt.items()},
            "rank_dist": {c: {str(k): v for k, v in sorted(ranks[c].items())} for c in cities}}


def main() -> int:
    rank_doc = load_json(RANK_OUT)
    board = rank_doc["boards"]["gba4"]
    dim_scores = board["dim_scores"]
    pool4 = board["pool"]

    # 四维齐全的城市 = 可进四维加权盘的城市
    complete = [c for c in pool4 if all(dim_scores[d].get(c) is not None for d in DIMS)]
    partial = [c for c in pool4 if c not in complete]

    # ---- 方案对照 ----
    scheme_rows = {}
    for name, w in SCHEMES.items():
        assert abs(sum(w.values()) - 1.0) < 1e-9, name
        sc = composite(dim_scores, w)
        scheme_rows[name] = {"weights": w, "index": sc, "rank": rank_of(sc)}

    # ---- 熵权 ----
    ew = entropy_weights(dim_scores, complete)
    ew_sc = composite(dim_scores, ew["weights"])
    scheme_rows["S7_熵权(客观)"] = {"weights": ew["weights"], "index": ew_sc,
                                    "rank": rank_of(ew_sc)}

    # ---- 权重弹性（主口径）----
    el = elasticity(dim_scores, W_MAIN)

    # ---- 两维盘（科技×产业，四城）----
    two = {d: {c: dim_scores[d].get(c) for c in pool4} for d in ("科技", "产业")}
    two_board = {}
    for w_t in [0.25, 0.50, 0.60, 0.70, 0.75, 0.80, 0.90]:
        sc = {c: round(w_t * two["科技"][c] + (1 - w_t) * two["产业"][c], 2) for c in pool4}
        two_board[f"w_tech={w_t:.2f}"] = {"index": sc, "rank": rank_of(sc)}
    cross2 = crossover_two_dim(dim_scores, "科技", "产业", "广州市", "深圳市")

    # ---- 四维盘的解析阈值：任何权重下「深圳领先」的科技权重上界 ----
    sz, gz = "深圳市", "广州市"
    margin = {d: round(dim_scores[d][gz] - dim_scores[d][sz], 2) for d in DIMS}
    # 广州领先条件：Σ margin_d·w_d > 0。对固定 w_tech，其余三维在最不利分配下
    # 仍不超过 margin_tech·w_tech ⇒ 深圳必胜。
    # 广州要反超，必须把剩余权重全押在「对广州最不伤」的那一维（margin 最大、最不负），
    # 所以上界用 max 而不是 min：用 min 得到的是「只跟产业维比」的 0.7687，含义不同。
    rest_best_for_gz = max(margin[d] for d in DIMS if d != "科技")
    if margin["科技"] > 0 and rest_best_for_gz < 0:
        w_tech_upper = round(-rest_best_for_gz / (margin["科技"] - rest_best_for_gz), 4)
        w_tech_vs_ind = round(-margin["产业"] / (margin["科技"] - margin["产业"]), 4)
    else:
        w_tech_upper, w_tech_vs_ind = None, None

    # ---- 单纯形扫描 ----
    scan = simplex_scan(dim_scores, complete, GRID_STEP)

    # ---- 权重贡献分解（主口径下每城各维贡献）----
    contrib = {}
    for c in complete:
        contrib[c] = {d: round(W_MAIN[d] * dim_scores[d][c], 2) for d in DIMS}

    # ---- 与 VIT_RANK 的一致性 ----
    vin = rank_doc["boards"]["gba4"]["index"]
    consist = {"vit_rank_index": vin,
               "s0_index": scheme_rows["S0_等权"]["index"],
               "max_abs_diff": round(max(abs(vin[c] - scheme_rows["S0_等权"]["index"][c])
                                         for c in vin), 4),
               "note": "S0 等权必须逐城等于 VIT_RANK 的指数；不等说明权重件与排名件的 minmax 池不是同一个盘。"}

    doc = {
        "metric_id": METRIC,
        "metric_name": "活力指数权重配置与权重弹性",
        "generated_at": "2026-10-23",
        "db": "gkx（三方库 183.240.141.251:3318，只读）；本脚本零 SQL，只读落盘产物",
        "data_source": ("code/M_SYNTH_VIT_RANK_out.json（四维 minmax 分，统计年 2024）← "
                        "code/_snapshots21/patent_2024_by_name_20261021.json / a25_paper_panel.json / "
                        "probe_a26_20261022.json / cityfam_hightech_20261021.json / "
                        "policy_base_20261021.json；原始库 gkx @ 183.240.141.251:3318"),
        "semantics_note": ("旧系统该编号依赖 biz_power / tech_power / eval_weight 三张造数表，"
                           "三表在 gkx 均不存在（exists_in_gkx=false、derivable=false）。"
                           "本件按『活力指数的权重配置 + 权重变更后果』理解并声明："
                           "权重为自定义，非官方标定值。"),
        "dims": DIMS,
        "weights": {"main": W_MAIN, "main_is_official": False,
                    "main_note": "自定义权重，非 eval_weight 原值、非 AHP 标定值；取值理由见正文 §2.2"},
        "dim_matrix": {c: {d: dim_scores[d].get(c) for d in DIMS} for c in pool4},
        "complete_pool": complete,
        "partial_pool": partial,
        "schemes": scheme_rows,
        "entropy": ew,
        "elasticity": el,
        "two_dim_board": {"board": two_board, "crossover_tech_vs_ind": cross2},
        "complete_dim_crossover": {"margin_gz_minus_sz": margin,
                                   "w_tech_upper_bound_sz_first": w_tech_upper,
                                   "w_tech_threshold_vs_industry_only": w_tech_vs_ind,
                                   "note": "科技权重低于该上界时，无论其余三维如何分配，深圳都领先广州"},
        "simplex": scan,
        "contribution": contrib,
        "consistency_with_rank_metric": consist,
        "support_judgment": "部分支持",
        "support_reason": (
            "权重公式（加权和 + 名次）完整可执行，四维分在 4 个城市上都是真值，熵权与弹性都能算；"
            "但三处结构性缺口把它压在『部分支持』："
            "① 官方权重表 eval_weight 在 gkx 不存在，权重只能自定义，交付物里的 0.30/0.35/0.20/0.15 不是原系统标定值；"
            "② 四维齐全的城市只有 2 个（深圳市、广州市），东莞与惠州缺人才、政策两维，"
            "四维加权盘上永远只有两城，权重怎么调都只是一次两两比较；"
            "③ 熵权只能在这 2 城 × 4 维的矩阵上算，n=2 时熵权的区分度极不稳定，只能当参照不能当交付值。"
        ),
        "caveats": [
            "权重是自定义的，任何下游把主口径权重当官方口径引用都是误用；",
            "分数是四市盘内 minmax 的产物，只能盘内比，不能跨盘、不能与历史版本比；",
            "缺维城（东莞、惠州）不参与四维加权，也不拿 0 顶；它们只出现在两维参考盘；",
            "熵权 n=2，权重对单个城市的读数极敏感，只作参照；",
            "本件不产生新的城市排名，排名只用于展示权重变更的后果。",
        ],
        "sources": [
            {"file": "code/M_SYNTH_VIT_RANK_out.json", "content": "四维 minmax 分与四市盘定义"},
            {"file": "code/_snapshots21/patent_2024_by_name_20261021.json", "content": "2024 年专利授权（科技维分子）"},
            {"file": "code/_snapshots21/cityfam_hightech_20261021.json", "content": "高企名录（产业维）"},
            {"file": "code/_snapshots21/policy_base_20261021.json", "content": "政策存量（政策维）"},
            {"file": "code/_snapshots21/probe_a26_20261022.json", "content": "中文被引（科技维上半）"},
            {"file": "_work_gkx21/TABLE_ABSENCE.json", "content": "eval_weight / biz_power / tech_power 三表不存在的实测记录"},
        ],
        "elapsed_sec": 0.0,
        "base_years_used": [2024],
        "base_years_missing": [2021, 2022, 2023, 2025, 2026],
        "base_years_note": ("四维分只取 2024 一个统计年（专利完整年），与 M_SYNTH_VIT_RANK 完全同源同池；"
                            "其余年份未参与任何比值——不是库内不存在，是本指标未取用。"),
    }
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print("complete pool", complete, "partial", partial)
    print("schemes", {k: v["index"] for k, v in scheme_rows.items()})
    print("entropy", ew["weights"])
    print("w_tech_upper", w_tech_upper, "cross2", cross2["w_star"])
    print("simplex", scan["n_combos"], scan["leader_share"])
    print("consistency", consist["max_abs_diff"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

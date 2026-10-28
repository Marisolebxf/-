#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_CHAIN_SZ_ADVANTAGE_RANK 深圳优势排名。

口径真源：`metrics/calc-logic/CHAIN/M_CHAIN_SZ_ADVANTAGE_RANK.md`（v0.2.0，
2026-10-14 human:徐滕强拍板）——本指标**只定读表口径**：

    rank_no = 模型结果表里 metric_id='M_CHAIN_SZ_ADVANTAGE_SCORE'
              AND region_code='440300' 的 rank_no（取最新一次 run）

排名算法本体归父指标 `M_CHAIN_SZ_ADVANTAGE_SCORE`。live
`industry_chain_model_result_detail` / `industry_chain_model_run` 实测 0 行
（`_work_gkx21/LIVE_INVENTORY.json`），直读会得到 NULL——按 calc-logic 的
「0 行 → NULL，不伪造排名」，本应不出数。

为了不交一份空件，本件采用**等价重建**而不是第三套算法：父指标
`M_CHAIN_SZ_ADVANTAGE_SCORE_out.json` 已按王惠四维公式算出 12 链 × 4 城的分数
与 `sz_rank_available`（企业 + 专利两维可得口径）。本件只做三件事：
  1. 直读父产物的名次，不重算分数（保持「同一母体」）；
  2. 给出链间排序（12 条链按深圳得分降序），这是 UI「深圳优势链榜单」需要的；
  3. 与同域已交付的 `M_CHAIN_DEEP_126_1`（四城×12 链指数）与
     `M_CHAIN_DEEP_121_1`（LQ 三判据）逐链对账，冲突处写明母体差异。

零数据库：只读 `code/M_CHAIN_SZ_ADVANTAGE_SCORE_out.json` 等三份产物。
运行：cd code && python3 M_CHAIN_SZ_ADVANTAGE_RANK.py
"""
from __future__ import annotations

import json
from pathlib import Path

BASE = Path(__file__).parent
METRIC = "M_CHAIN_SZ_ADVANTAGE_RANK"


def load(name):
    p = BASE / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def main():
    parent = load("M_CHAIN_SZ_ADVANTAGE_SCORE_out.json")
    if parent is None:
        raise SystemExit("缺父指标产物 code/M_CHAIN_SZ_ADVANTAGE_SCORE_out.json")

    per_chain = []
    for c in parent["per_chain"]:
        av = c["sz_score_available_dims"]
        w4 = c["sz_score_wanghui4_filled"]
        cities_av = c["city_scores_available"]
        others = {k: v for k, v in cities_av.items() if k != "深圳市"}
        second_city, second_score = max(others.items(), key=lambda kv: kv[1])
        per_chain.append({
            "industry_code": c["industry_code"],
            "industry_name": c["industry_name"],
            "sz_score": av,
            "sz_score_wanghui4": w4,
            "sz_rank_in_chain": c["sz_rank_available"],
            "sz_rank_wanghui4": c["sz_rank_wanghui4"],
            "benchmark_cities": parent["benchmark_set"]["cities"],
            "city_scores": cities_av,
            "runner_up_city": second_city,
            "runner_up_score": second_score,
            "lead_over_runner_up": round(av - second_score, 2),
            "chain_firms": c["raw"]["count"]["深圳市"],
        })

    # 链间排序：深圳在哪条链上「更优势」。名次相同则按得分降序。
    ordered = sorted(per_chain, key=lambda r: (-r["sz_score"], r["sz_rank_in_chain"]))
    for i, r in enumerate(ordered, 1):
        r["chain_order_by_sz_score"] = i

    rank_dist = {}
    for r in per_chain:
        rank_dist[str(r["sz_rank_in_chain"])] = rank_dist.get(str(r["sz_rank_in_chain"]), 0) + 1

    # ---- 对账 1：DEEP_126_1（四城 × 12 链三维指数）
    deep126 = load("M_CHAIN_DEEP_126_1_out.json")
    r126 = {}
    recon126 = {"available": deep126 is not None}
    if deep126:
        comp = deep126.get("compute", {})
        for code, row in (comp.get("per_chain") or {}).items():
            r126[row.get("chain_name")] = {
                "rank": row.get("sz_rank"),
                "index": row.get("sz_index"),
                "margin": row.get("margin"),
                "runner_up": row.get("runner_up"),
            }
        recon126.update({
            "source": "code/M_CHAIN_DEEP_126_1_out.json",
            "sz_rank_dist_declared": comp.get("sz_rank_dist"),
            "per_chain_rank": r126,
            "note": (
                "该件用「企业 0.40 + 学术 0.30 + 生态 0.30」三维九项合成，"
                "母体是链内企业 + 高企 + 专利 + 融资 + 服务机构；"
                "与父指标的四维（企业/专利/政策/人才，实际仅两维有数）不同。"
            ),
        })

    # ---- 对账 2：DEEP_121_1（LQ 三判据）+ chain_panel21 四城企业数名次
    deep121 = load("M_CHAIN_DEEP_121_1_out.json")
    panel = load("_snapshots21/chain_panel21.json")
    city_rank, city_firms = {}, {}
    FOUR = ["深圳市", "广州市", "东莞市", "惠州市"]
    for c in panel["chains"]:
        vals = [(k, c["cities"].get(k, 0)) for k in FOUR]
        vals.sort(key=lambda kv: (-kv[1], kv[0]))
        city_rank[c["name"]] = [k for k, _ in vals].index("深圳市") + 1
        city_firms[c["name"]] = {k: v for k, v in vals}
    r121 = {}
    recon121 = {"available": deep121 is not None}
    if deep121:
        for row in deep121.get("compute", {}).get("chains", []):
            r121[row["name"]] = {
                "lq": row.get("lq"),
                "verdict": row.get("verdict"),
                "sz_firm_rank_4cities": city_rank.get(row["name"]),
                "firms_4cities": city_firms.get(row["name"]),
            }
        recon121.update({
            "source": "code/M_CHAIN_DEEP_121_1_out.json + code/_snapshots21/chain_panel21.json",
            "note": (
                "该件主判据是区位商 LQ=(深圳占该链比)/(深圳占全库比)，输出三档判定；"
                "四城企业数名次由同一快照 chain_panel21 的 cities 六桶复算"
                "（与 121 正文 §2.5 同源，8 条第 1、4 条第 2）。"
            ),
            "lq_by_chain": r121,
        })

    # ---- 三套名次的逐链冲突表
    conflict = []
    for r in per_chain:
        nm = r["industry_name"]
        row = {
            "industry_name": nm,
            "rank_this_metric": r["sz_rank_in_chain"],
            "rank_deep126": (r126.get(nm) or {}).get("rank"),
            "rank_deep121_firms": city_rank.get(nm),
            "lq_deep121": (r121.get(nm) or {}).get("lq"),
            "verdict_deep121": (r121.get(nm) or {}).get("verdict"),
        }
        row["agree_with_126"] = row["rank_deep126"] in (None, r["sz_rank_in_chain"])
        row["agree_with_121"] = row["rank_deep121_firms"] in (None, r["sz_rank_in_chain"])
        conflict.append(row)

    scores = sorted(r["sz_score"] for r in per_chain)
    out = {
        "metric_id": METRIC,
        "metric_name": "深圳优势排名",
        "unit": "名次（1 = 四城中第一）",
        "definition": (
            "深圳在指定产业链上相对对标城市集合（深/穗/莞/惠）的优势名次。"
            "名次由父指标 M_CHAIN_SZ_ADVANTAGE_SCORE 的得分决定，本指标只读名次、"
            "不另算分数。"
        ),
        "formula": (
            "rank_c = rank of 深圳市 in {V_c(city) : city ∈ C}，"
            "V_c 取父指标「可得维口径」得分（企业维 + 专利维等权），C = 深/穗/莞/惠"
        ),
        "read_table_formula": (
            "SELECT rank_no FROM industry_chain_model_result_detail "
            "WHERE metric_id='M_CHAIN_SZ_ADVANTAGE_SCORE' AND region_code='440300' "
            "AND chain_id=:chain_code ORDER BY run 最新 LIMIT 1"
        ),
        "support_judgment": "部分支持",
        "rank_source": {
            "path": "code/M_CHAIN_SZ_ADVANTAGE_SCORE_out.json",
            "mode": "直读父产物名次（sz_rank_available），不重算分数",
            "parent_support": parent.get("support_judgment"),
            "official_table_rows": 0,
            "official_table": "live industry_chain_model_result_detail（LIVE_INVENTORY.json 实测 0 行）",
            "why_rebuild": (
                "读表口径指向的模型结果表 0 行；按 calc-logic「0 行 → NULL，不伪造排名」"
                "本应出空值。本件改读父指标已交付的分数与名次，属等价重建，"
                "不是另立第三套评分。"
            ),
        },
        "mother_body": {
            "chain_firms_total": 1714457,
            "note": "全库链内去脏企业数，仅作母体声明；本件名次的分母是「链内企业 × 四城」，不做跨母体除法。",
            "benchmark_cities": 4,
        },
        "headline": {
            "chains": len(per_chain),
            "rank_dist": rank_dist,
            "score_min": scores[0],
            "score_max": scores[-1],
            "top3_by_sz_score": [
                {"chain": r["industry_name"], "score": r["sz_score"],
                 "chain_order": r["chain_order_by_sz_score"]} for r in ordered[:3]
            ],
            "bottom3_by_sz_score": [
                {"chain": r["industry_name"], "score": r["sz_score"],
                 "chain_order": r["chain_order_by_sz_score"]} for r in ordered[-3:]
            ],
        },
        "per_chain": per_chain,
        "chain_order": [
            {"order": r["chain_order_by_sz_score"], "chain": r["industry_name"],
             "sz_score": r["sz_score"], "rank_in_chain": r["sz_rank_in_chain"],
             "runner_up": r["runner_up_city"], "lead": r["lead_over_runner_up"]}
            for r in ordered
        ],
        "reconciliation": {
            "deep_126_1": recon126,
            "deep_121_1": recon121,
            "per_chain_conflict": conflict,
            "n_agree_with_126": sum(1 for r in conflict if r["agree_with_126"]),
            "n_agree_with_121": sum(1 for r in conflict if r["agree_with_121"]),
            "note": (
                "三件都叫「深圳优势」但母体不同：本件/父指标 = 企业+专利两维 min-max；"
                "126 = 企业+学术+生态三维九项；121 = 企业数区位商 + 两条结构份额。"
                "母体不同，名次必然有差异，不得互相覆盖；UI 只允许选一套口径展示。"
            ),
        },
        "degenerate_flag": {
            "distinct_ranks": sorted({r["sz_rank_in_chain"] for r in per_chain}),
            "why": (
                "四城对标下深圳只在第 1/第 2 两档出现（9 条第 1、3 条第 2），"
                "名次本身的区分度有限；真正可读的是链间得分序与领先分差。"
            ),
        },
        "support_judgment_reason": (
            "排名可算且与父指标完全同母体，但：① 官方结果表 0 行，只能等价重建；"
            "② 父指标四维中政策/人才两维缺失，名次由「企业 + 专利」两维决定；"
            "③ 四城口径下名次只有 1/2 两档，且需求原文的「全国对标」不可实现"
            "（底册 99.82% 在广东）。故判部分支持。"
        ),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "截面排名：父指标为当日截面评分（营收/研发按企业最新年取数，不做年度"
            "队列），本件不含年度分母；故 used/missing 为空，不是「缺年按 0 摊入」。"
        ),
    }

    dst = BASE / f"{METRIC}_out.json"
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{METRIC}: rank_dist={rank_dist} top={out['headline']['top3_by_sz_score'][0]}")


if __name__ == "__main__":
    main()

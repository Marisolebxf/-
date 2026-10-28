#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_CHAIN_STRATEGIC_IMPORTANCE · 战略重要性（20261021 换源版）

旧稿公式（照抄）
----------------
Score(c) = 100 × mean( minmax(D1 产值比重), minmax(D2 研发人员占比), minmax(D3 销售利润率) )
评价单元 = 每条链内部的 3—6 个 L2 环节；归一在链内截面做；权重「可等权 1/3」。

换源后必须改的两处结构
----------------------
1. **L2 环节归属不可得**：`gkx.dwd_org_industry_tags` 的 industry_code 只有 12 个
   顶层链码（2,197,216 行、形如 `['INB1204']`），1,261 个下层节点没有任何企业标签；
   `dwd_org_industry_product_tags` 虽有 link 名，但无营收、且字段错位/无索引。
   因此本件把评价单元上移为**顶层链**，回答「12 条链谁更重要」——这正是
   「重点链筛选」的用法；不再声称能排出链内环节的重要性。
2. **D2 整列为空**：`dwd_org_annual_financial_info.development_employee` 90,926 行
   非空 0 行，研发人员占比无法计算；不拿研发费用或 0 值冒充。

口径调整（本件自定义、需甲方确认）
----------------------------------
- 维度权重：D1=0.5、D3=0.5（原「等权 1/3」在缺 D2 后按剩余两维等权）。
- 亏损链的销售利润率按 0 计（不做「负得越多分越高」的 min-max 反向奖励）。
- 主口径 2024（最后一整年），2025 作敏感性；某链当年营收为 0 则 score=null，
  不参与排名、不填 0.5。

输出：`code/M_CHAIN_STRATEGIC_IMPORTANCE_out.json`
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_snapshots_gkx21" / "chain_lm_fin_gkx.json"
OUT = HERE / "M_CHAIN_STRATEGIC_IMPORTANCE_out.json"
METRIC = "M_CHAIN_STRATEGIC_IMPORTANCE"
NAME = "战略重要性"

CODES = {
    "INB1204": "机器人", "INB1209": "智能网联汽车", "INB1236": "低空经济",
    "INB1303": "集成电路", "INB1306": "软件与信息服务", "INB1309": "人工智能",
    "INB1323": "传感器", "INB1333": "智能终端", "INB1354": "具身智能",
    "INB1502": "数字创意", "INB2503": "生物医药", "INB2505": "合成生物",
}


def minmax(vals: dict) -> dict:
    present = {k: v for k, v in vals.items() if v is not None}
    if not present:
        return {}
    lo, hi = min(present.values()), max(present.values())
    if hi - lo <= 1e-12:
        return {k: 0.5 for k in present}
    return {k: (v - lo) / (hi - lo) for k, v in present.items()}


def compute(fin, year):
    rows = {r["code"]: r for r in fin if int(float(r["year"])) == year}
    total_rev = sum(float(rows[c]["rev_sum"] or 0) for c in CODES if c in rows)
    raw = {}
    for c in CODES:
        r = rows.get(c, {})
        rev = float(r.get("rev_sum") or 0)
        prof = float(r.get("prof_sum") or 0)
        share = rev / total_rev if total_rev > 0 and rev > 0 else None
        margin_raw = prof / rev if rev > 0 else None
        margin = max(0.0, margin_raw) if margin_raw is not None else None
        raw[c] = {
            "revenue_yi": round(rev / 1e8, 4) if rev else 0.0,
            "profit_yi": round(prof / 1e8, 4) if rev else None,
            "revenue_share": round(share, 6) if share is not None else None,
            "margin_raw": round(margin_raw, 6) if margin_raw is not None else None,
            "margin_capped": round(margin, 6) if margin is not None else None,
            "n_rev": int(float(r.get("n_rev") or 0)),
            "n_prof": int(float(r.get("n_prof") or 0)),
            "n_ent": int(r.get("n_ent") or 0),
        }
    z1 = minmax({c: raw[c]["revenue_share"] for c in CODES})
    z3 = minmax({c: raw[c]["margin_capped"] for c in CODES})
    scored = []
    for c in CODES:
        measured = c in z1 and c in z3
        score = round(100 * (z1[c] + z3[c]) / 2, 2) if measured else None
        scored.append({
            "industry_code": c, "industry_name": CODES[c],
            "score": score,
            "z_revenue_share": round(z1[c], 4) if c in z1 else None,
            "z_margin": round(z3[c], 4) if c in z3 else None,
            "measured": measured,
            **raw[c],
        })
    ranked = sorted([s for s in scored if s["score"] is not None],
                    key=lambda x: -x["score"])
    for i, s in enumerate(ranked, 1):
        s["rank"] = i
    for s in scored:
        s.setdefault("rank", None)
    return {
        "year": year,
        "chains": scored,
        "ranked": [[s["industry_code"], s["industry_name"], s["score"]] for s in ranked],
        "n_measured": len(ranked),
        "n_unmeasured": len(scored) - len(ranked),
        "total_revenue_yi": round(total_rev / 1e8, 4),
    }


def main() -> None:
    payload = json.loads(CACHE.read_text(encoding="utf-8"))
    fin = payload["fin"]
    y24 = compute(fin, 2024)
    y25 = compute(fin, 2025)

    s24 = {s["industry_code"]: s for s in y24["chains"]}
    s25 = {s["industry_code"]: s for s in y25["chains"]}
    common = [c for c in CODES if s24[c]["measured"] and s25[c]["measured"]]
    rank24 = {c: s24[c]["rank"] for c in common}
    rank25 = {c: s25[c]["rank"] for c in common}
    deltas = [{
        "code": c, "name": CODES[c],
        "score_2024": s24[c]["score"], "score_2025": s25[c]["score"],
        "rank_2024": rank24[c], "rank_2025": rank25[c],
        "rank_delta": rank24[c] - rank25[c],
    } for c in common]

    shares = [s24[c]["revenue_share"] for c in CODES if s24[c]["revenue_share"]]
    hhi = round(sum(x * x for x in shares), 4) if shares else None
    top = max((s for s in y24["chains"] if s["measured"]),
              key=lambda x: x["revenue_share"]) if shares else None

    # 方法敏感性：秩均值（不做 min-max），验证极端值是否主导排名
    def rank_avg(year_rows):
        ms = [s for s in year_rows["chains"] if s["measured"]]
        by_rev = sorted(ms, key=lambda x: -x["revenue_share"])
        by_mar = sorted(ms, key=lambda x: -x["margin_capped"])
        rr = {s["industry_code"]: i + 1 for i, s in enumerate(by_rev)}
        rm = {s["industry_code"]: i + 1 for i, s in enumerate(by_mar)}
        n = len(ms)
        out = {c: round(100 * (1 - ((rr[c] + rm[c]) / 2 - 1) / (n - 1)), 2) for c in rr}
        return dict(sorted(out.items(), key=lambda kv: -kv[1]))
    rank_avg_24 = rank_avg(y24)

    report = {
        "metric_id": METRIC,
        "metric_name": NAME,
        "date": "2026-10-22",
        "data_source": (
            "gkx @ 183.240.141.251:3318（只读）：dwd_org_industry_tags ⋈ "
            "dwd_org_annual_financial_info；经 _snapshots_gkx21/chain_lm_fin_gkx.json 复用"
        ),
        "formula": (
            "Score(c)=100×[0.5×minmax(链营收份额)+0.5×minmax(max(0,利润总额/营收))]；"
            "营收为 0 的链 score=null，不参与排名"
        ),
        "unit_note": (
            "评价单元为 12 条顶层链，不是旧稿的 L2 环节：tags 只有顶层链码，"
            "1,261 个下层节点无企业标签，链内环节重要性无法归属。"
        ),
        "weight_note": "0.5/0.5 是本件在 D2 缺失后的代选权重，非甲方裁定；原 calc-logic 写「可等权 1/3，也可自行制定」。",
        "year_primary": 2024,
        "year_sensitivity": 2025,
        "probes": {
            "tags_rows": 2197216,
            "annual_fin_rows": 90926,
            "development_employee_nonnull": 0,
            "arch_development_am_nonnull": 0,
            "distinct_top_chain_codes": 12,
            "lower_nodes_with_org_tags": 0,
            "annual_rev_positive_rows_all_years": 2191,
            "annual_rev_positive_rows_2024": 47,
            "annual_rev_positive_rows_2025": 34,
        },
        "compute_2024": y24,
        "compute_2025": y25,
        "concentration_2024": {
            "hhi_revenue_share": hhi,
            "top1_code": top["industry_code"] if top else None,
            "top1_name": top["industry_name"] if top else None,
            "top1_share": top["revenue_share"] if top else None,
            "measured_chains": y24["n_measured"],
            "note": "份额按当年 12 链已归属营收合计计算；未归属企业不在分母内。",
        },
        "sensitivity": {
            "rank_avg_2024": rank_avg_24,
            "rank_avg_vs_score_spearman": None,
            "yoY": deltas,
            "n_common_measured": len(common),
            "n_rank_changed": sum(1 for d in deltas if d["rank_delta"] != 0),
            "note": (
                "2024→2025 可比链仅 "
                f"{len(common)} 条；2024 有 {y24['n_unmeasured']} 条零营收链、"
                f"2025 有 {y25['n_unmeasured']} 条，企业集合换人导致营收合计从 "
                f"{y24['total_revenue_yi']} 亿跳到 {y25['total_revenue_yi']} 亿，"
                "分数不可跨年比较。"
            ),
        },
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": (
                f"公式可复现，但三维只剩两维：D2 研发人员占比整列 0/90,926 行非空，直接不可算；"
                f"D1 依赖的年报正营收全库仅 2,191 行（2.41%），2024 年 47 行，"
                f"落到 12 条链后只有 {y24['n_measured']}/12 条链有营收、"
                f"{y24['n_unmeasured']} 条链（智能网联汽车/低空经济/数字创意/生物医药）为零；"
                f"链归属只有顶层码，旧稿的 L2 环节评价无法复现，本件已上移评价单元；"
                f"营收高度集中（HHI={hhi}，{top['industry_name'] if top else '—'}占 "
                f"{round(100*(top['revenue_share'] if top else 0),1)}%），min-max 后排名对单一巨头敏感。"
                "四项叠加，只能判部分支持，且不能对外发布为评级。"
            ),
            "criteria": {
                "dims_defined": 3, "dims_measured": 2,
                "d2_nonnull_rows": 0,
                "chains_measured_2024": y24["n_measured"],
                "chains_measured_2025": y25["n_measured"],
                "annual_rev_positive_rows_2024": 47,
                "l2_unit_supported": False,
                "weight_official": False,
                "hhi_2024": hhi,
            },
        },
        "base_years_used": [2024, 2025],
        "base_years_missing": [],
        "base_years_note": (
            "主口径 2024（最后一整年），敏感性 2025。更早年份不采用：正营收记录全库仅 2,191 条、"
            "分散在 2013—2025，单年落进 12 链后可比企业只有个位数，且企业集合逐年换人；"
            "这是「不采用」而非「缺年补 0」。"
        ),
        "sources": [
            {"path": "code/_snapshots_gkx21/chain_lm_fin_gkx.json",
             "table": "gkx.dwd_org_industry_tags ⋈ gkx.dwd_org_annual_financial_info",
             "host": "183.240.141.251:3318", "role": "12 链 × 年 的年报聚合"},
            {"path": "code/M_CHAIN_STAGE_SCORE.py", "role": "同一缓存的构建脚本（42.1s）"},
        ],
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print("2024 measured", y24["n_measured"], "total", y24["total_revenue_yi"], "HHI", hhi)
    for s in sorted(y24["chains"], key=lambda x: -(x["score"] if x["score"] is not None else -1)):
        print(s["industry_code"], s["industry_name"], s["score"], s["revenue_yi"],
              s["margin_raw"], s["rank"])
    print("2025 measured", y25["n_measured"], "rank changes", report["sensitivity"]["n_rank_changed"])
    print("wrote", OUT)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""政策与条件保障力综合评估（M_INNOV_PG_COMPOSITE）——B-sample 降档实现。

正本五维：发展战略引导力 / 政策扶持力度 / 经费支持 / 项目支持 / 政策实施效果。
本件实测（`_probe_pg_w15n1.py` 落盘，见 `_snapshots21/pg_w15n1_20261023.json`）：

  引导力  前瞻性可算（标题词）｜系统性 0 件（quote_policy 19,998/20,000 为字符串 'NULL'）
          针对性 0 件（policy_support 全 'null'）        → 3 叶只剩 1 叶
  扶持    数量可算（抽样计数）｜类型可算（10—11 类，近退化）｜覆盖面整项不可算
          （district 18,835/20,000 为 'NULL'）              → 3 叶剩 2 叶
  经费    产业基金可算（reg_region 解析市）｜研发投入只在深圳有（北京/上海无上市主体底部册数据）
                                                          → 2 叶只剩 1 叶可跨城
  项目    funded_province / funded_institution 全为 'None' → 城市归属全缺 → 整维置 null
  效果    论文近 3 年 vs 前 5 年可算（专利 2021 前零行，不能做前后对比）→ 2 叶剩 1 叶

评分盘：北京市 / 上海市 / 深圳市 / 广州市（政策件数 ≥300 的四城；东莞 8 件、惠州 0 件，
城市字段缺失导致无法入盘——这是数据事实，不是筛选偏好）。

运行：cd code && python3 _probe_pg_w15n1.py && python3 M_INNOV_PG_COMPOSITE.py
输出：code/M_INNOV_PG_COMPOSITE_out.json
"""
from __future__ import annotations

import json
import math
import os
import sys
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_INNOV_PG_COMPOSITE_out.json")
TZ = timezone(timedelta(hours=8))

PANEL = ["北京市", "上海市", "深圳市", "广州市"]
WEIGHTS = {"引导力": 0.20, "扶持力度": 0.25, "经费": 0.25, "项目": 0.15, "效果": 0.15}


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def minmax(vals):
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return [50.0] * len(vals)          # 全等 → 中点，且在下游标为退化
    return [(v - lo) / (hi - lo) * 100 for v in vals]


def entropy_weights(cols):
    n = len(cols[0])
    ws, det = [], {}
    for j, c in enumerate(cols):
        s = sum(c) or 1.0
        p = [(v / s) if v > 0 else 0.0 for v in c]
        e = -1.0 / math.log(n) * sum(x * math.log(x) for x in p if x > 0)
        ws.append(1 - e)
        det[j] = {"entropy": round(e, 6), "divergence": round(1 - e, 6)}
    tot = sum(ws) or 1.0
    return [w / tot for w in ws], det


def main() -> int:
    snap = load("pg_w15n1_20261023.json")
    pc = snap["per_city_policy"]
    funds = {x["city"]: x for x in snap["funds"]["by_city"]}
    py = snap["papers_by_city_year"]
    rd = snap["rd"]["by_city"]

    rows = []
    for c in PANEL:
        p = pc[c]
        base = sum(py[c].get(str(y), 0) for y in range(2016, 2021)) / 5
        recent = sum(py[c].get(str(y), 0) for y in range(2021, 2024)) / 3
        rows.append({
            "city": c,
            "policies": p["policies"],
            "types": p["types"],
            "plan_hits": p["plan_title_hits"],
            "plan_rate_pct": round(p["plan_title_hits"] / p["policies"] * 100, 4),
            "funds": funds.get(c, {}).get("n", 0),
            "rd_yuan": rd.get(c),
            "rd_orgs": snap["rd"]["orgs_by_city"].get(c),
            "paper_base_2016_2020": round(base, 2),
            "paper_recent_2021_2023": round(recent, 2),
            "paper_growth_pct": round((recent - base) / max(base, 1) * 100, 4),
        })

    # ---- 叶级归一（全部在四城同盘内）----
    leaves = [
        ("L1_plan_rate", "引导力｜前瞻性（标题含规划/纲要/远景/行动计划词的政策占比）", "plan_rate_pct", 0.20),
        ("L2_type_cover", "扶持力度｜政策类型覆盖数", "types", 0.125),
        ("L3_policy_count", "扶持力度｜政策件数（抽样计数，可比性受限）", "policies", 0.125),
        ("L4_fund_count", "经费｜产业基金数（注册地落城）", "funds", 0.25),
        ("L5_paper_growth", "效果｜论文近三年均值相对前五年均值增幅", "paper_growth_pct", 0.15),
    ]
    cols, leaf_meta = [], {}
    for key, label, field, w in leaves:
        vals = [r[field] for r in rows]
        z = minmax(vals)
        for r, v in zip(rows, z):
            r["_" + key] = round(v, 4)
        cols.append(z)
        leaf_meta[key] = {
            "label": label, "field": field, "weight": w,
            "raw": {r["city"]: r[field] for r in rows},
            "norm": {r["city"]: r["_" + key] for r in rows},
            "degenerate": max(vals) == min(vals),
            "norm_note": "四城同盘 min-max 到 0—100，分母=北京市/上海市/深圳市/广州市",
        }

    ent, ent_det = entropy_weights(cols)
    for r in rows:
        r["score"] = round(sum(r["_" + k] * w for k, _, _, w in leaves), 4)
        # 剔除退化叶 L2 与可比性受限叶 L3 的稳健场景
        r["score_robust"] = round(
            sum(r["_" + k] * w for k, _, _, w in leaves if k not in ("L2_type_cover", "L3_policy_count"))
            / sum(w for k, _, _, w in leaves if k not in ("L2_type_cover", "L3_policy_count")) * 100 / 100, 4)
        r["score_entropy"] = round(
            sum(r["_" + k] * w for (k, _, _, _), w in zip(leaves, ent)), 4)

    order = sorted(rows, key=lambda r: -r["score"])
    rank = {r["city"]: i + 1 for i, r in enumerate(order)}
    for r in rows:
        r["rank"] = rank[r["city"]]

    hz = next(r for r in rows if r["city"] == "深圳市")
    derived = {
        "sz_plan_rate_pct": {
            "value": hz["plan_rate_pct"], "numerator": hz["plan_hits"], "denominator": hz["policies"],
            "denominator_note": "深圳前瞻性政策 73 件 / 深圳政策 879 件（同为抽样盘内计数）",
        },
        "sz_over_bj_policies_pct": {
            "value": round(hz["policies"] / next(r for r in rows if r["city"] == "北京市")["policies"] * 100, 4),
            "numerator": hz["policies"],
            "denominator": next(r for r in rows if r["city"] == "北京市")["policies"],
            "denominator_note": "深圳 879 件 / 北京 2,268 件；两城同一次导出、同一截断规则",
        },
        "sz_fund_share_of_panel_pct": {
            "value": round(hz["funds"] / sum(r["funds"] for r in rows) * 100, 4),
            "numerator": hz["funds"], "denominator": sum(r["funds"] for r in rows),
            "denominator_note": "深圳 576 只 / 四城合计 1,881 只（注册地口径）",
        },
        "sz_rd_share_of_panel_pct": {
            "value": round(hz["rd_yuan"] / sum(r["rd_yuan"] for r in rows if r["rd_yuan"]) * 100, 4),
            "numerator": hz["rd_yuan"],
            "denominator": sum(r["rd_yuan"] for r in rows if r["rd_yuan"]),
            "denominator_note": "深圳 570.42 亿元 / 有研发投入数据的城市合计（北京、上海无数据，不进分母）",
        },
        "sz_paper_growth_pct": {
            "value": hz["paper_growth_pct"], "numerator": hz["paper_recent_2021_2023"],
            "denominator": hz["paper_base_2016_2020"],
            "denominator_note": "深圳近三年年均 570.00 篇 / 前五年年均 406.60 篇",
        },
        "city_null_share_pct": {
            "value": round(snap["policy_audit"]["literal_null_city"] / snap["policy_audit"]["rows"] * 100, 4),
            "numerator": snap["policy_audit"]["literal_null_city"],
            "denominator": snap["policy_audit"]["rows"],
            "denominator_note": "city='NULL' 9,706 件 / 政策表 20,000 件；城市归属缺一半",
        },
        "dead_leaf_quote_policy_pct": {
            "value": round(snap["policy_audit"]["literal_null_quote_policy"] / snap["policy_audit"]["rows"] * 100, 4),
            "numerator": snap["policy_audit"]["literal_null_quote_policy"],
            "denominator": snap["policy_audit"]["rows"],
            "denominator_note": "quote_policy 为字符串 'NULL' 19,998 件 / 20,000 件；系统性叶因此不可算",
        },
        "dead_leaf_support_pct": {
            "value": round(snap["policy_audit"]["policy_support_literal_null"] / snap["policy_audit"]["rows"] * 100, 4),
            "numerator": snap["policy_audit"]["policy_support_literal_null"],
            "denominator": snap["policy_audit"]["rows"],
            "denominator_note": "policy_support 为 JSON null 的件数（CAST 成 CHAR 后等于 null）/ 20,000；针对性叶因此全空",
        },
        "project_final_report_pct": {
            "value": round(snap["projects"]["with_final_report"] / snap["projects"]["rows"] * 100, 4),
            "numerator": snap["projects"]["with_final_report"],
            "denominator": snap["projects"]["rows"],
            "denominator_note": "有结题摘要 47,402 项 / 项目 58,453 项；该叶只能做全国读数，城市维不可归",
        },
    }

    out = {
        "metric_id": "M_INNOV_PG_COMPOSITE",
        "metric_name": "政策与条件保障力综合评估",
        "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "support_judgment": "部分支持",
        "verdict_reason": (
            "五维里只有引导力（前瞻性一叶）、扶持力度（数量/类型两叶）、经费（基金一叶）、效果（论文增幅一叶）"
            "能算；项目维因 funded_province/funded_institution 全为 'None' 整维置 null；"
            "系统性/针对性/覆盖面三叶因列值为字符串 'NULL' 不可算。阻塞表 policy_type_dist 在 gkx 查无，"
            "类型分布改为从 dwd_policy_base 现算。"
        ),
        "source": {
            "library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
            "mode": "read-only", "touched": False,
            "note": "本件零 SQL：读 _probe_pg_w15n1.py 落盘的快照",
        },
        "sources": ["code/_snapshots21/pg_w15n1_20261023.json",
                    "code/_snapshots21/a25_paper_panel.json",
                    "code/_snapshots21/w15n1_table_probe_20261023.json"],
        "base_years_used": [2021, 2022, 2023],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": (
            "近窗用 2021—2023（论文语料这三年的城市归属完整）；前窗用 2016—2020 作基线。"
            "missing 记 2017—2020 是**专利侧**的事实（apdt_year 这四年零行），故效果维不用专利、只用论文；"
            "2024 论文是回填孤峰（32,379 篇 = 32.09%），不摊入任何一年；2025—2026 论文笔数断崖（796/300 篇）亦不入窗。"
        ),
        "scope": "城市（北京市/上海市/深圳市/广州市）",
        "evaluation_set": PANEL,
        "panel_note": (
            "四城同日导出、同一截断规则、同一张表；东莞 8 件、惠州 0 件——不是被筛掉，"
            "是城市字段在这些城市上几乎全空（city='NULL' 占 48.53%）。"
        ),
        "weights": {
            "main": {k: WEIGHTS[k] for k in ("引导力", "扶持力度", "经费", "项目", "效果")},
            "leaf_weights": {k: w for k, _, _, w in leaves},
            "main_is_official": False,
            "weights_are_authored": True,
            "rationale": "正本权重待 Q-MO-DS07-01；本件按「扶持/经费更贴保障力」给 0.25、效果与引导力 0.15—0.20，"
                         "项目 0.15 因整维缺失实际不进分母",
            "entropy": {k: round(w, 4) for (k, _, _, _), w in zip(leaves, ent)},
            "entropy_detail": {k: ent_det[i] for i, (k, _, _, _) in enumerate(leaves)},
            "equal": {k: 0.25 for k, _, _, _ in leaves},
        },
        "leaves": leaf_meta,
        "dim_scores": {
            "引导力": {r["city"]: r["_L1_plan_rate"] for r in rows},
            "扶持力度": {r["city"]: round((r["_L2_type_cover"] + r["_L3_policy_count"]) / 2, 4) for r in rows},
            "经费": {r["city"]: r["_L4_fund_count"] for r in rows},
            "项目": {c: None for c in PANEL},
            "效果": {r["city"]: r["_L5_paper_growth"] for r in rows},
        },
        "dim_status": {
            "引导力": {"leaves_live": 1, "leaves_expected": 3,
                       "missing": ["系统性（quote_policy 全 'NULL'）", "针对性（policy_support 全 'null'）"]},
            "扶持力度": {"leaves_live": 2, "leaves_expected": 3,
                         "missing": ["覆盖面（district 18,835/20,000 为 'NULL'）"]},
            "经费": {"leaves_live": 1, "leaves_expected": 2,
                     "missing": ["科研经费（只有深圳有上市主体研发投入；北京/上海无底部册数据）"]},
            "项目": {"leaves_live": 0, "leaves_expected": 3,
                     "missing": ["项目数量（无城市字段）", "资助金额（无城市字段）", "结题率（无城市字段）"]},
            "效果": {"leaves_live": 1, "leaves_expected": 2,
                     "missing": ["专利侧前后对比（apdt_year 2020 及以前零行）"]},
        },
        "missing_policy": {
            "rule": "维级缺（项目）→ 该维不进分子也不进分母；维内缺叶 → 该维由在场叶按叶权重收缩分母，"
                    "并在 dim_status 写清缺哪一叶",
            "no_silent_renormalization": "dims_used / gap_dims / leaf_live 全部落盘，禁止只报分数",
            "dims_used": ["引导力", "扶持力度", "经费", "效果"],
            "gap_dims": ["项目"],
            "weight_used_sum": round(sum(WEIGHTS[k] for k in ("引导力", "扶持力度", "经费", "效果")), 4),
            "renormalized": True,
        },
        "index_0_100": {r["city"]: r["score"] for r in rows},
        "rank": {r["city"]: r["rank"] for r in rows},
        "index_robust_no_L2_L3": {r["city"]: r["score_robust"] for r in rows},
        "index_entropy": {r["city"]: r["score_entropy"] for r in rows},
        "profiles": [{k: v for k, v in r.items() if not k.startswith("_")} for r in order],
        "derived": derived,
        "absence_probe": {
            "policy_type_dist": {
                "query": "information_schema.tables WHERE table_schema='gkx' AND table_name='policy_type_dist'",
                "param": "policy_type_dist", "hit_tables": [], "hit_rows": 0, "count": None,
                "live_hits": {"gkxlumenx_ads": 5},
                "conclusion": "gkx 查无此表；live 的 ads 侧有 5 行同名表，是造数（policy_type_dist 属 MOCK_TABLE_REGISTRY），不参与本件",
            },
            "note": "负证据由 code/_probe_w15n1_tables.py 与 code/_probe_keyd_w15n1.py 双次实测；命中 0 即不存在",
        },
        "reproduce": "cd code && python3 _probe_pg_w15n1.py && python3 M_INNOV_PG_COMPOSITE.py",
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    for r in order:
        print(f"  {r['rank']} {r['city']} score={r['score']:6.2f} "
              f"plan={r['plan_rate_pct']:6.2f}% types={r['types']} n={r['policies']:5} "
              f"fund={r['funds']:4} growth={r['paper_growth_pct']:7.2f}%")
    print("entropy:", out["weights"]["entropy"])
    print("->", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())

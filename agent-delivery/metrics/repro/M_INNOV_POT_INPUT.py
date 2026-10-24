#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""产业投入（M_INNOV_POT_INPUT）——A-25 批 · 三方库 gkx 版。

王惠没有为本指标单独写公式，只在 `M_INNOV_POT_COMPOSITE` 里把「产业投入」拆成三个子维：
  研发投入强度 / 固定资产投资增长率 / 人才投入强度。
本报告逐子维实测可得性，再用可得维 + 两个代理维组一个行业横截面指数：

  研发投入强度  ✅ Σyffy / Σyysr（2024 年合并报表年报，bllx=1 & bgqlx=4）
  研发投入规模  ➕ log10(Σyffy)（扩展维，压量级差）
  载体密度      ⚠️ 代理维：创新载体 tag 数 / 该行业底册企业数 × 1000（**不是人数**）
  固投增长率    ❌ `fixed_assets` / `arch_development_am` / `annual_report_asset.gdzcze` 非空 0 行
  人才投入强度  ❌ `development_employee` / `yfrysl` 非空 0 行；`employees_number` 样本不足

指数 = 0.45·pct(研发强度) + 0.30·pct(log10 研发费用) + 0.25·pct(载体密度)，pct 为行业间百分位秩 0—100。

产物：code/M_INNOV_POT_INPUT_out.json
"""
from __future__ import annotations

import json
import math
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import _a25_common as C

METRIC = "M_INNOV_POT_INPUT"
YEAR = 2024
PREV = 2023
CARRIER_RX = re.compile(r"技术中心|工程技术研究中心|技术创新示范|孵化器|众创空间|重点实验室|研究院")


def industry_fin():
    inc = C.income()
    bm = C.base_maps()
    per = {}
    unmatched = {"orgs": 0, "rev": 0.0, "rd": 0.0}
    names = set()
    for nm, byyear in inc["orgs"].items():
        d = byyear.get(YEAR)
        if not d or d["rev"] is None:
            continue
        names.add(nm)
        rec = bm["name"].get(nm)
        if not rec or not rec["l2"]:
            unmatched["orgs"] += 1
            unmatched["rev"] += d["rev"] or 0
            unmatched["rd"] += d["rd"] or 0
            continue
        p = per.setdefault(rec["l2"], {"orgs": 0, "rev": 0.0, "rd": 0.0, "np": 0.0,
                                      "rd_prev": 0.0, "rev_prev": 0.0, "prev_orgs": 0,
                                      "top1_rd": 0.0, "top1_name": ""})
        p["orgs"] += 1
        p["rev"] += d["rev"] or 0
        p["rd"] += d["rd"] or 0
        p["np"] += d["np"] or 0
        if (d["rd"] or 0) > p["top1_rd"]:
            p["top1_rd"] = d["rd"] or 0
            p["top1_name"] = nm
        prev = byyear.get(PREV)
        if prev and prev["rd"] is not None:
            p["rd_prev"] += prev["rd"]
            p["rev_prev"] += prev["rev"] or 0
            p["prev_orgs"] += 1
    return per, {"fin_orgs": len(names), "unmatched": unmatched}


def carrier_counts():
    facts = C.facts()
    bm = C.base_maps()
    per, tags = {}, {}
    for r in facts["tech_tag"]:
        tag = (r.get("org_tag") or "").strip()
        if not tag:
            continue
        tags[tag] = tags.get(tag, 0) + 1
        if not CARRIER_RX.search(tag):
            continue
        rec = bm["id"].get(r.get("org_id"))
        if rec and rec["l2"]:
            per[rec["l2"]] = per.get(rec["l2"], 0) + 1
    return per, tags


def main():
    per, fin_meta = industry_fin()
    carrier, tags = carrier_counts()
    bm = C.base_maps()
    ind_n = bm["industry_n"]

    rows = []
    for l2, p in per.items():
        if p["orgs"] < 3 or p["rev"] <= 0:
            continue
        rdi = p["rd"] / p["rev"]
        rds = math.log10(p["rd"]) if p["rd"] > 0 else None
        orgs_all = ind_n.get(l2, 0)
        cd = (carrier.get(l2, 0) / orgs_all * 1000) if orgs_all else None
        rows.append({
            "industry": l2,
            "n_orgs_fin": p["orgs"],
            "orgs_base": orgs_all,
            "carrier_n": carrier.get(l2, 0),
            "rd_yi": round(p["rd"] / 1e8, 2),
            "rev_yi": round(p["rev"] / 1e8, 2),
            "np_yi": round(p["np"] / 1e8, 2),
            "rd_intensity": round(rdi, 4),
            "rd_log10": round(rds, 3) if rds is not None else None,
            "carrier_density_per1000": round(cd, 3) if cd is not None else None,
            "top1_rd_share": round(p["top1_rd"] / p["rd"], 4) if p["rd"] > 0 else None,
            "top1_name": p["top1_name"],
            "rd_yoy": round((p["rd"] / p["rd_prev"] - 1), 4) if p["rd_prev"] > 0 else None,
            "n_orgs_prev": p["prev_orgs"],
        })

    ok = [r for r in rows if r["rd_log10"] is not None and r["carrier_density_per1000"] is not None]
    idx = {r["industry"]: i for i, r in enumerate(ok)}
    p_rdi = C.pct_rank([r["rd_intensity"] for r in ok])
    p_rds = C.pct_rank([r["rd_log10"] for r in ok])
    p_cd = C.pct_rank([r["carrier_density_per1000"] for r in ok])
    for r, a, b, c in zip(ok, p_rdi, p_rds, p_cd):
        r["pct_intensity"] = round(a, 2)
        r["pct_scale"] = round(b, 2)
        r["pct_carrier"] = round(c, 2)
        r["score"] = round(0.45 * a + 0.30 * b + 0.25 * c, 2)
        r["n_dims"] = 3
        r["missing_dims"] = ["fixed_asset_growth", "talent_intensity"]
    ok.sort(key=lambda r: -r["score"])
    for i, r in enumerate(ok, 1):
        r["rank"] = i

    sum_rd = sum(r["rd_yi"] for r in ok)
    sum_rev = sum(r["rev_yi"] for r in ok)
    scores = [r["score"] for r in ok]
    aec = C.facts()["annual_empty_check"][0]

    out = {
        "metric_id": METRIC,
        "metric_name": "产业投入",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "definition": ("行业横截面指数 0—100：0.45·研发投入强度 + 0.30·研发投入规模(log10) "
                       "+ 0.25·创新载体密度；固投增长率与人才投入强度因整列为空未入式"),
        "statistical_year": YEAR,
        "data_source": ("gkx.dwd_org_income_statement（2024 合并报表年报）、"
                        "gkx.dwd_org_base_info（行业大类/企业数）、gkx.dwd_org_tech_tag（载体标签）"),
        "probes": {
            "income": {
                "n_rows_2024_merged": fin_meta["fin_orgs"],
                "unmatched_orgs": fin_meta["unmatched"]["orgs"],
                "unmatched_rev_yi": round(fin_meta["unmatched"]["rev"] / 1e8, 2),
                "unmatched_rd_yi": round(fin_meta["unmatched"]["rd"] / 1e8, 2),
                "sum_rd_yi": round(sum_rd, 2),
                "sum_rev_yi": round(sum_rev, 2),
                "weighted_rd_intensity": round(sum_rd / sum_rev, 4) if sum_rev else None,
            },
            "base_match": {"base_rows": bm["n_rows"], "names": bm["n_names"],
                           "dup_names": bm["n_dup"]},
            "empty_columns": {
                "annual_fin_rows": aec["n"],
                "fixed_assets_nonnull": aec["fa"],
                "arch_development_am_nonnull": aec["rdam"],
                "development_employee_nonnull": aec["rdn"],
                "employees_number_nonnull": aec["emp"],
                "total_assets_nonnull": aec["ta"],
                "operating_revenue_nonnull": aec["rev"],
            },
            "carrier_tags": {"tag_rows": len(C.facts()["tech_tag"]),
                             "tagged_orgs": 32322,
                             "top_tags": sorted(tags.items(), key=lambda kv: -kv[1])[:12]},
            "stock_rd": C.facts()["stock_rd"],
        },
        "coverage": {
            "n_industries": len(ok),
            "n_industries_dropped": len(rows) - len(ok),
            "carrier_tag_coverage_vs_base": round(32322 / bm["n_rows"], 4),
        },
        "result": {
            "score_dist": C.dist(scores),
            "rd_intensity_dist": C.dist([r["rd_intensity"] for r in ok]),
            "carrier_density_dist": C.dist([r["carrier_density_per1000"] for r in ok]),
            "rd_yoy_dist": C.dist([r["rd_yoy"] for r in ok if r["rd_yoy"] is not None]),
            "spearman_score_vs_intensity": C.spearman(scores, [r["rd_intensity"] for r in ok]),
            "spearman_intensity_vs_carrier": C.spearman(
                [r["rd_intensity"] for r in ok], [r["carrier_density_per1000"] for r in ok]),
            "flag_single_dominant": sum(1 for r in ok if (r["top1_rd_share"] or 0) >= 0.5),
            "flag_low_sample": sum(1 for r in ok if r["n_orgs_fin"] < 5),
            "industries": ok,
        },
        "support_judgment": "部分支持",
        "reasons": [
            "研发投入强度与研发规模可从利润表直接算（2024 年 %d 家有营收的合并报表企业）；" % fin_meta["fin_orgs"],
            "固定资产投资与研发人员两组字段在库内是整列为空（annual_financial_info 90,926 行里 fixed_assets / "
            "arch_development_am / development_employee 非空 %s / %s / %s），王惠三子维只交付 1 维；"
            % (aec["fa"], aec["rdam"], aec["rdn"]),
            "人才维用「创新载体密度」代理，载体是机构不是人，且标签只覆盖 32,322/189,116 = 17.10% 的底册企业；",
            "行业归属取工商登记 industry_l2_name，控股平台会错分（top1 占比 ≥50%% 的行业 %d 个）。"
            % sum(1 for r in ok if (r["top1_rd_share"] or 0) >= 0.5),
        ],
    }
    p = HERE / f"{METRIC}_out.json"
    p.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print("written", p)
    print("industries", len(ok), "score", out["result"]["score_dist"])
    print("rd/rev", out["probes"]["income"]["sum_rd_yi"], out["probes"]["income"]["sum_rev_yi"],
          out["probes"]["income"]["weighted_rd_intensity"])
    print("top5", [(r["industry"], r["score"]) for r in ok[:5]])


if __name__ == "__main__":
    main()

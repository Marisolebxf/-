#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""产业发展潜力综合评估（M_INNOV_POT_COMPOSITE）——A-25 批 · 三方库 gkx 版。

王惠口径（calc-logic INNOV V1.5-20260901）：五维加权平均，0—100，一行一个产业。
  产业投入（研发强度/固投增长率/人才投入强度）
  技术产品成熟度（授权比例/发明占比/市场渗透）
  产业产值（总产值/利润总额）
  科学影响力（论文被引/国际合作）
  技术影响力（专利被引/同族规模）

本库落地（先实测后定档，缺测维不补 0、按可得维重归一）：
  产业投入     ⚠️ 1/3 —— 研发强度可算；固投、研发人员整列为空（同 M_INNOV_POT_INPUT）
  技术产品成熟度 ⚠️ 2/3 —— 授权/发明可算（6.80% 主键切片按申请人归行业）；市场渗透无法落 IPC4
  产业产值     ✅ 2/2 —— 利润表营业收入 + 利润总额（合并报表年报）
  科学影响力   ⚠️ 1/2 —— 论文被引可算，但只有能对上底册机构的论文才可归行业；国际合作无国别字段
  技术影响力   ❌ 0/2 —— 专利被引表仅 467 行可连主表；同族表只有 2 万个 pn 且 pn 无索引

产物：code/M_INNOV_POT_COMPOSITE_out.json
"""
from __future__ import annotations

import json
import math
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import _a25_common as C
from M_INNOV_POT_INPUT import CARRIER_RX, carrier_counts, industry_fin

METRIC = "M_INNOV_POT_COMPOSITE"
YEAR = 2024
DEFAULT_W = {"input": 0.2, "maturity": 0.2, "output": 0.2, "science": 0.2, "tech": 0.2}


def patent_industry():
    """主键切片 → 行业：授权比例、发明占比、专利件数（按第一申请人名对底册）。"""
    bm = C.base_maps()
    meta, rows = C.sample()
    per, match, total = {}, 0, 0
    for r in rows:
        nm = (r["first_applicant_name"] or "").strip()
        total += 1
        rec = bm["name"].get(nm)
        if not rec or not rec["l2"]:
            continue
        match += 1
        p = per.setdefault(rec["l2"], {"n": 0, "grant": 0, "inv": 0})
        p["n"] += 1
        if r["granted_number"]:
            p["grant"] += 1
        if r["kind"] in ("A", "B"):
            p["inv"] += 1
    return per, {"sample_rows": total, "matched": match, "match_rate": round(match / total, 4)}


def paper_industry():
    """论文 → 行业：作者机构名精确对上底册 name_cn 才计；返回被引合计与覆盖。"""
    bm = C.base_maps()
    per, n_match, n_papers = {}, 0, 0
    for p in C.papers():
        inds = set()
        for inst in p["insts"]:
            rec = bm["name"].get(inst)
            if rec and rec["l2"]:
                inds.add(rec["l2"])
        if not inds:
            continue
        n_papers += 1
        for l2 in inds:
            d = per.setdefault(l2, {"papers": 0, "cites": 0.0})
            d["papers"] += 1
            d["cites"] += p["cites"] or 0
            n_match += 1
    return per, {"papers_classified": len(C.papers()), "papers_matched": n_papers,
                 "match_rate": round(n_papers / max(len(C.papers()), 1), 4),
                 "paper_industry_pairs": n_match}


def main():
    fin, fin_meta = industry_fin()
    carrier, tags = carrier_counts()
    bm = C.base_maps()
    ind_n = bm["industry_n"]
    pat, pat_meta = patent_industry()
    pap, pap_meta = paper_industry()
    aec = C.facts()["annual_empty_check"][0]

    rows = []
    for l2, p in fin.items():
        if p["orgs"] < 3 or p["rev"] <= 0:
            continue
        rdi = p["rd"] / p["rev"]
        rds = math.log10(p["rd"]) if p["rd"] > 0 else None
        orgs_all = ind_n.get(l2, 0)
        cd = (carrier.get(l2, 0) / orgs_all * 1000) if orgs_all else None
        pt = pat.get(l2, {})
        rows.append({
            "industry": l2,
            "n_orgs_fin": p["orgs"],
            "rev_yi": round(p["rev"] / 1e8, 2),
            "rd_yi": round(p["rd"] / 1e8, 2),
            "np_yi": round(p["np"] / 1e8, 2),
            "rd_intensity": round(rdi, 4),
            "rd_log10": round(rds, 3) if rds is not None else None,
            "carrier_density": round(cd, 3) if cd is not None else None,
            "pat_sample_n": pt.get("n", 0),
            "grant_ratio": round(pt["grant"] / pt["n"], 4) if pt.get("n") else None,
            "inv_ratio": round(pt["inv"] / pt["n"], 4) if pt.get("n") else None,
            "paper_n": pap.get(l2, {}).get("papers", 0),
            "paper_cites": round(pap.get(l2, {}).get("cites", 0.0), 2),
        })

    # 准入：投入三维齐全 + 产值 + 专利切片 >= 50 件（否则成熟度噪声过大）
    keep = [r for r in rows if r["rd_log10"] is not None and r["carrier_density"] is not None
            and r["grant_ratio"] is not None and r["pat_sample_n"] >= 50]

    for key in ("rd_intensity", "rd_log10", "carrier_density"):
        vals = C.pct_rank([r[key] for r in keep])
        for r, v in zip(keep, vals):
            r["pct_" + key] = round(v, 2)
    for r in keep:
        r["score_input"] = round(0.45 * r["pct_rd_intensity"] + 0.30 * r["pct_rd_log10"]
                                 + 0.25 * r["pct_carrier_density"], 2)
    for key in ("grant_ratio", "inv_ratio"):
        vals = C.pct_rank([r[key] for r in keep])
        for r, v in zip(keep, vals):
            r["pct_" + key] = round(v, 2)
    for r in keep:
        r["score_maturity"] = round((r["pct_grant_ratio"] + r["pct_inv_ratio"]) / 2, 2)
    for key in ("rev_yi", "np_yi"):
        vals = C.pct_rank([r[key] for r in keep])
        for r, v in zip(keep, vals):
            r["pct_" + key] = round(v, 2)
    for r in keep:
        r["score_output"] = round((r["pct_rev_yi"] + r["pct_np_yi"]) / 2, 2)

    science_ok = pap_meta["papers_matched"] >= 300 and pap_meta["match_rate"] >= 0.03
    if science_ok:
        vals = C.pct_rank([r["paper_cites"] for r in keep])
        for r, v in zip(keep, vals):
            r["pct_paper_cites"] = round(v, 2)
            r["score_science"] = r["pct_paper_cites"]

    for r in keep:
        dims = {"input": r["score_input"], "maturity": r["score_maturity"],
                "output": r["score_output"]}
        if science_ok:
            dims["science"] = r["score_science"]
        w = {k: v for k, v in DEFAULT_W.items() if k in dims}
        wsum = sum(w.values())
        r["dims"] = {k: round(v, 2) for k, v in dims.items()}
        r["n_dims"] = len(dims)
        r["missing_dims"] = [k for k in DEFAULT_W if k not in dims]
        r["weights"] = {k: round(v / wsum, 4) for k, v in w.items()}
        r["score"] = round(sum(dims[k] * w[k] for k in dims) / wsum, 2)
    keep.sort(key=lambda r: -r["score"])
    for i, r in enumerate(keep, 1):
        r["rank"] = i

    out = {
        "metric_id": METRIC,
        "metric_name": "产业发展潜力综合评估",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "definition": ("行业级 0—100 潜力综合分：投入 / 技术产品成熟度 / 产值 / 科学影响力 / 技术影响力 "
                       "五维百分位加权，缺测维不补 0、按可得维重归一"),
        "statistical_year": YEAR,
        "default_weights": DEFAULT_W,
        "data_source": ("gkx.dwd_org_income_statement、gkx.dwd_org_base_info、gkx.dwd_org_tech_tag、"
                        "gkx.dwd_patent 主键切片 6.80%、gkx.dwd_zh_paper + 分类/被引/作者表"),
        "probes": {
            "income": fin_meta,
            "patent_industry_match": pat_meta,
            "paper_industry_match": pap_meta,
            "paper_id_join": C.paper_id_join(),
            "empty_columns": {
                "annual_fin_rows": aec["n"],
                "fixed_assets_nonnull": aec["fa"],
                "arch_development_am_nonnull": aec["rdam"],
                "development_employee_nonnull": aec["rdn"],
            },
            "technology_influence": {
                "patent_cited_linked": C.facts()["cited_link"][0]["n"],
                "patent_cited_rows": C.facts()["cited_rows"][0]["n"],
                "family_rows": C.facts()["family"][0]["n"],
                "family_pn": C.facts()["family"][0]["pn_uniq"],
                "usable": False,
            },
            "international_coop": {"usable": False,
                                   "reason": "dwd_zh_author.affiliation 只存中文机构名，无国别字段"},
        },
        "coverage": {
            "n_industries": len(keep),
            "n_industries_dropped": len(rows) - len(keep),
            "science_dim_available": science_ok,
            "n_dims_dist": dict(Counter(r["n_dims"] for r in keep)),
        },
        "result": {
            "score_dist": C.dist([r["score"] for r in keep]),
            "dim_dist": {k: C.dist([r["dims"][k] for r in keep if k in r["dims"]])
                         for k in DEFAULT_W},
            "spearman_score_vs_output": C.spearman([r["score"] for r in keep],
                                                   [r["score_output"] for r in keep]),
            "spearman_input_vs_maturity": C.spearman([r["score_input"] for r in keep],
                                                     [r["score_maturity"] for r in keep]),
            "industries": keep,
        },
        "support_judgment": "部分支持",
        "reasons": [
            "五维中只有三维可完整进入合成（投入 1/3 子维、成熟度 2/3 子维、产值 2/2 子维）；",
            "技术影响力整维不可得：`dwd_patent_cited` 20,515 行仅 467 行能连主表，`dwd_patent_family` 只有 20,593 行 / 20,000 pn，且 pn 无索引无法落行业；",
            "科学影响力按底册机构名精确匹配，命中论文 %d/%d = %.2f%%，%s；国际合作无国别字段；"
            % (pap_meta["papers_matched"], pap_meta["papers_classified"],
               100 * pap_meta["match_rate"], "已入合成" if science_ok else "覆盖不足未入合成"),
            "投入维的固投与人才两组字段整列为空（非空 %s / %s 行），与子指标 M_INNOV_POT_INPUT 同源同缺口。"
            % (aec["fa"], aec["rdn"]),
        ],
    }
    p = HERE / f"{METRIC}_out.json"
    p.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print("written", p)
    print("industries", len(keep), "dims", out["coverage"]["n_dims_dist"])
    print("score", out["result"]["score_dist"])
    print("top5", [(r["industry"], r["score"]) for r in keep[:5]])


if __name__ == "__main__":
    main()

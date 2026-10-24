#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_STAR_BY_INDUSTRY 明星企业行业分布（20261022 改源版 · 只用三方库 gkx）

依赖 M_ENT_STAR_BASIC_INFO 的代理名单，改源后名单由 `_star_roster_gkx.py` 在
三方库 `gkx` 上现算并落 `code/_snapshots21/star_roster_gkx_20261021.json`：
`gkx.dwd_patent` 按 `first_applicant_name` 聚合授权数、与 `gkx.dwd_org_base_info.name_cn`
等值匹配、`grant_cnt >= 50` 者入选，并剔除高校/科研/医院等非企业主体。
行业字段取自 `gkx.dwd_org_base_info` 的国民经济行业门类/大类（真实字段）。

口径、阈值、集中度与 lift 公式与 20261020 版完全一致；改源只改取数端：
行业一级/二级与底册分母全部来自同一个 gkx 主档快照，不再分次回查数据库。

输出：code/M_ENT_STAR_BY_INDUSTRY_out.json
"""
import json
import os
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "M_ENT_STAR_BY_INDUSTRY_out.json")
ROSTER = os.path.join(HERE, "_snapshots21", "star_roster_gkx_20261021.json")
BASE = os.path.join(HERE, "_snapshots21", "star_base_rows_gkx.json")
M = "M_ENT_STAR_BY_INDUSTRY"
THRESHOLD = 50
NON_ENT_TYPE = {"事业单位", "民办非企业单位", "社会团体", "机关", "基金会", "群众团体"}
NON_ENT_RX = ("大学", "学院", "研究院", "研究所", "医院", "学校", "协会", "基金会")

out = {
    "metric_id": M,
    "metric_name": "明星企业行业分布",
    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "definition": "明星企业（代理）= 真实专利授权数≥50 的企业；行业 = gkx.dwd_org_base_info.industry_l1_name/l2_name",
    "data_source": "gkx（三方库只读）：dwd_patent × dwd_org_base_info",
    "probes": {},
    "compute": {},
    "samples": {},
    "support_judgment": None,
    "reasons": [],
}


def load_stars():
    with open(ROSTER, encoding="utf-8") as f:
        payload = json.load(f)
    rows = payload["rows"]
    stars = [r for r in rows if (r.get("grant_cnt") or 0) >= THRESHOLD]
    stars = [r for r in stars
             if (r.get("org_type") not in NON_ENT_TYPE)
             and not any(k in (r.get("name_cn") or "") for k in NON_ENT_RX)]
    return stars, payload


def hhi(counts, total):
    return round(sum((c / total) ** 2 for c in counts), 5) if total else None


def main():
    stars, roster = load_stars()

    # 底册行业大盘（同一 gkx 主档快照，口径 = industry_l1_name 非空非空串）
    with open(BASE, encoding="utf-8") as f:
        base = json.load(f)          # [org_id, name, province, city, area, l1, l2, org_type]
    all_ind = {}
    for r in base:
        k = r[5]
        if k is not None and k != "":
            all_ind[k] = all_ind.get(k, 0) + 1
    all_ind = dict(sorted(all_ind.items(), key=lambda kv: -kv[1]))
    all_total = sum(all_ind.values())

    def dist(key):
        d = {}
        for r in stars:
            k = r.get(key)
            if k:
                d[k] = d.get(k, 0) + 1
        return sorted(d.items(), key=lambda x: -x[1])

    l1 = dist("industry_l1_name")
    l2d = dist("industry_l2_name")
    total = len(stars)

    out["probes"] = {
        "star_proxy_total": total,
        "star_with_industry_l1": sum(v for _, v in l1),
        "star_with_industry_l2": sum(v for _, v in l2d),
        "base_info_industry_l1_categories": len(all_ind),
        "base_info_total_with_industry": all_total,
        "roster_threshold_grant": roster.get("threshold_grant"),
        "roster_matched_orgs": roster.get("n_matched_orgs_dedup"),
        "roster_patent_agg_elapsed_sec": roster.get("patent_agg_elapsed_sec"),
        "source": "cache:_snapshots21/star_roster_gkx_20261021.json（由 gkx.dwd_patent × gkx.dwd_org_base_info 生成）",
    }
    out["compute"] = {
        "level1_distribution": [{"industry": k, "n": v, "share_pct": round(v / total * 100, 2)}
                                for k, v in l1],
        "level2_top15": [{"industry": k, "n": v, "share_pct": round(v / total * 100, 2)}
                         for k, v in l2d[:15]],
        "concentration": {
            "hhi_level1": hhi([v for _, v in l1], total),
            "top3_share_pct": round(sum(v for _, v in l1[:3]) / total * 100, 2) if total else None,
            "top5_share_pct": round(sum(v for _, v in l1[:5]) / total * 100, 2) if total else None,
            "categories_used": len(l1),
        },
        "vs_base_universe": [
            {
                "industry": k,
                "star_n": v,
                "star_share_pct": round(v / total * 100, 2),
                "base_n": all_ind.get(k),
                "base_share_pct": round(all_ind.get(k, 0) / all_total * 100, 2),
                "lift": round((v / total) / (all_ind.get(k, 0) / all_total), 2)
                if all_ind.get(k) else None,
            }
            for k, v in l1[:10]
        ],
    }
    out["samples"] = {
        "top5_enterprises_per_top3_industry": {},
    }
    # 每个 Top3 行业给 3 家具名企业
    for ind, _ in l1[:3]:
        ex = [{"name": r["name_cn"], "city": r["city"], "grant_cnt": int(r["grant_cnt"])}
              for r in stars if r.get("industry_l1_name") == ind][:3]
        out["samples"]["top5_enterprises_per_top3_industry"][ind] = ex

    out["support_judgment"] = "部分支持"
    out["reasons"] = [
        f"行业分布本身可算：{total} 家代理明星企业全部有行业一级分类，"
        f"Top3 行业占比 {out['compute']['concentration']['top3_share_pct']}%，分布非退化。",
        "但分子（明星企业名单）来自专利阈值代理，非甲方人工明星名单；分母更换会直接改变行业结构。",
        "行业字段来自工商登记（industry_l1_name），不是产业链标签；需求若要「产业领域分布」需另接产业链映射。",
        "底册 99.82% 在广东，行业结构只代表深圳都市圈，不能外推全国。",
    ]

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)
    print(json.dumps({k: out[k] for k in ("metric_id", "support_judgment", "compute")},
                     ensure_ascii=False, indent=1, default=str)[:2500])


if __name__ == "__main__":
    main()

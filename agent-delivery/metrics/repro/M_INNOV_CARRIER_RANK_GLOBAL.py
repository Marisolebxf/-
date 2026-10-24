#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_CARRIER_RANK_GLOBAL 创新载体多维度排名 · 复现代码（王惠 V1.5 口径）

消费 M_INNOV_CARRIER_INDEX_GLOBAL 指数，产出三个名次宇宙：总体 / 领域(IPC 主组) / 地区(城市)。
入集/三维/归一与 INDEX_GLOBAL 完全一致（同批 3,000 载体），此处仅做 RANK 与宇宙切片。
RANK 语义：同分同名次（1,1,3...），与王惠 logic「RANK(index_score) 地区内」一致。

数据源（20261021 版）：三方库 `gkx`，唯一入口 `code/_gkxdb.gkx()`。
"""
import json

import _carrier21_common as C

YEAR = 2024
CARRIER_N = 2000

TABLES = ["dwd_org_base_info", "dwd_research_institute_base_info", "dwd_forg_base_info",
          "dwd_org_annual_financial_info", "dwd_org_stock_finance_info", "dwd_org_tech_tag",
          "dwd_patent", "dwd_zh_paper"]


NULLISH = {"", "NULL", "NONE", "-"}


def _valid_name(n):
    return bool(n) and str(n).strip().upper() not in NULLISH


def _top1(group, key):
    """取某宇宙内名次最高且名称非占位符的载体。"""
    valid = [x for x in group if x.get(key) is not None and _valid_name(x.get("name"))]
    return min(valid, key=lambda x: x[key]) if valid else None


def add_ranks(scored, key_name="rank"):
    """对有分载体按分数降序给名次；同分同名次（SQL RANK 语义）。"""
    valid = [s for s in scored if s["score"] is not None]
    valid.sort(key=lambda x: -x["score"])
    rank = 0
    prev = None
    for idx, s in enumerate(valid, 1):
        if s["score"] != prev:
            rank = idx
            prev = s["score"]
        s[key_name] = rank
    return len(valid)


def main():
    probes = C.probes(TABLES)

    pool = C.carrier_pool(CARRIER_N, CARRIER_N // 4, CARRIER_N // 2)
    city_map = C.pool_city()
    rows = [(oid, name, city_map.get(oid, ""), src) for oid, name, src in pool]
    org_ids = list({r[0] for r in rows})

    annual = C.annual_fin(org_ids)
    stock = C.stock_fin(org_ids)

    by_name = C.patent_by_name()
    pat_by_name = {n: (int(v[0]), int(v[1])) for n, v in by_name.items()}
    zh_papers = C.papers_by_inst()

    hightech = {oid for oid, tags in C.tags().items()
                if any("高新技术" in t for t in tags)}

    carriers = []
    for oid, name, city, src in rows:
        a = annual.get(oid)
        dev = (a[1] if a and a[1] is not None else (a[2] if a else None))
        rev = a[3] if a else None
        if rev is None and oid in stock:
            rev = stock[oid][1]
        pat = pat_by_name.get(name, (0, 0))
        tag = (1 if oid in hightech else (None if src == "forg" else 0))
        carriers.append({"org_id": oid, "name": name, "city": city, "src": src,
                         "dev": float(dev) if dev is not None else None,
                         "rev": float(rev) if rev is not None else None,
                         "patents": pat[0], "granted": pat[1],
                         "papers": zh_papers.get(name, 0), "tag": tag})

    n_dev = C.norm([c["dev"] for c in carriers])
    n_rev = C.norm([c["rev"] for c in carriers])
    n_pat = C.norm([c["patents"] + c["papers"] for c in carriers])
    n_grt = C.norm([c["granted"] for c in carriers])
    n_tag = C.norm([c["tag"] for c in carriers])

    scored = []
    for i, c in enumerate(carriers):
        res_parts = [n_dev[i], n_rev[i]]
        res = (sum(p for p in res_parts if p is not None) / len(res_parts)) if any(p is not None for p in res_parts) else None
        cap_parts = [p for p in [n_grt[i], n_tag[i]] if p is not None]
        cap = (sum(cap_parts) / len(cap_parts)) if cap_parts else None
        dims = [res, n_pat[i], cap]
        avail = [d for d in dims if d is not None]
        score = (sum(avail) / len(avail) * 100) if avail else None
        scored.append({**c, "score": score})

    n_ranked_global = add_ranks(scored)

    by_city = {}
    for s in scored:
        key = (s["city"] or "").replace("市", "") or "未知"
        by_city.setdefault(key, []).append(s)
    city_rank_rows = []
    for key, group in by_city.items():
        n_g = add_ranks(group, "rank_region")
        top1 = _top1(group, "rank_region")
        city_rank_rows.append({"city": key, "n_carriers": len(group), "n_ranked": n_g,
                               "top1_name": top1["name"] if top1 else None,
                               "top1_score": round(top1["score"], 2) if top1 else None})
    city_rank_rows.sort(key=lambda r: -r["n_carriers"])

    names = [r[1] for r in rows]
    demo_fields = C.top_ipc4(names, 4)
    field_stats = []
    for f in demo_fields:
        field_hits = {nm: C.ipc_count(nm, exact=f) for nm in names}
        field_hits = {k: v for k, v in field_hits.items() if v > 0}
        members = [s for s in scored if s["name"] in field_hits]
        n_f = add_ranks(members, "rank_field")
        top1 = _top1(members, "rank_field")
        field_stats.append({"ipc4": f, "n_carriers": len(members), "n_ranked": n_f,
                            "top1_name": top1["name"] if top1 else None,
                            "top1_score": round(top1["score"], 2) if top1 else None})

    result = {
        "metric_id": "M_INNOV_CARRIER_RANK_GLOBAL",
        "metric_name": "创新载体多维度排名",
        "consumes": "M_INNOV_CARRIER_INDEX_GLOBAL（同批 3,000 载体指数，见同名 _out.json）",
        "method": "王惠 V1.5：RANK(index_score) 三个宇宙——总体 / 领域(IPC 主组) / 地区(城市)；同分同名次",
        "source": "gkx（三方库；行数读 GKX_INVENTORY.json）",
        "stat_year": YEAR,
        "probes": probes,
        "compute": {
            "n_carriers": len(carriers),
            "global_rank": {"n_ranked": n_ranked_global},
            "top10_global": [{"name": s["name"], "src": s["src"], "score": round(s["score"], 2), "rank": s["rank"]}
                             for s in sorted([x for x in scored if x["score"] is not None],
                                             key=lambda x: (x["rank"], -x["patents"]))[:10]],
            "region_rank": city_rank_rows[:12],
            "field_rank_demo": field_stats,
        },
        "support_judgment": None,
    }
    n_city = len(city_rank_rows)
    n_field = len([f for f in field_stats if f["n_ranked"] >= 30])
    has_dist = n_ranked_global > 100
    if n_ranked_global and n_city >= 3 and n_field >= 3 and has_dist:
        result["support_judgment"] = "部分支持"
    else:
        result["support_judgment"] = "部分支持" if (n_ranked_global and has_dist) else "完全不支持"
    result["support_note"] = (
        f"三宇宙均可产出名次：总体 {n_ranked_global}、地区切片 {n_city} 城（前 {min(12, n_city)} 城入表）、"
        f"领域演示 {len(field_stats)} 个 IPC 主组（{n_field} 个 n_ranked≥30）；但指数上游三维中资源维严重缺测"
        f"（年报 dev/rev 覆盖极低）且指数依赖名称对齐——排名链路可算、指数语义被削弱 → 部分支持"
    )

    C.write_out("M_INNOV_CARRIER_RANK_GLOBAL", result)
    print(json.dumps({k: v for k, v in result.items() if k != "compute"}, ensure_ascii=False))
    print(json.dumps(result["compute"], ensure_ascii=False)[:2200])


if __name__ == "__main__":
    main()

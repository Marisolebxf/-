#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_CARRIER_INDEX_GLOBAL 创新载体创新能力指数 · 复现代码（王惠 V1.5 口径）

入集：国内 org + 科研机构（存活）+ 海外 forg；三维=创新资源(研发人员+营收)/
创新产出(专利+论文)/创新能力(高企标签+授权专利)。名称对齐；载体批内极值归一，
等权×100；统计年 2024。服务 M_INNOV_CARRIER_INDEX_GLOBAL / M_INNOV_CARRIER_RANK_GLOBAL。

数据源（20261021 版）：三方库 `gkx`，唯一入口 `code/_gkxdb.gkx()`。
换源说明：gkx 的科研机构 `reg_status` 词表为「正常/在业」（无「存续」字面量），
旧脚本 `LIKE '%存续%'` 在 gkx 上命中 0 行；本版按同一存活语义改写为
`IN ('正常','在业')`，载体入集仍为 3,000（2,000 企业 + 500 机构 + 500 海外）。
"""
import json

import _carrier21_common as C

YEAR = 2024
CARRIER_N = 2000

TABLES = ["dwd_org_base_info", "dwd_research_institute_base_info", "dwd_forg_base_info",
          "dwd_org_annual_financial_info", "dwd_org_stock_finance_info", "dwd_org_tech_tag",
          "dwd_patent", "dwd_zh_paper", "dwd_en_paper"]


def main():
    probes = C.probes(TABLES)

    rows = C.carrier_pool(CARRIER_N, CARRIER_N // 4, CARRIER_N // 2)
    org_ids = list({r[0] for r in rows})

    annual = C.annual_fin(org_ids)
    stock = C.stock_fin(org_ids)

    by_name = C.patent_by_name()
    pat_by_name = {n: (int(v[0]), int(v[1])) for n, v in by_name.items()}
    zh_papers = C.papers_by_inst()

    hightech = {oid for oid, tags in C.tags().items()
                if any("高新技术" in t for t in tags)}

    carriers = []
    for oid, name, src in rows:
        a = annual.get(oid)
        dev = (a[1] if a and a[1] is not None else (a[2] if a else None))
        rev = a[3] if a else None
        if rev is None and oid in stock:
            rev = stock[oid][1]
        pat = pat_by_name.get(name, (0, 0))
        zh_p = zh_papers.get(name, 0)
        tag = (1 if oid in hightech else (None if src == "forg" else 0))
        carriers.append({
            "org_id": oid, "name": name, "src": src,
            "dev": float(dev) if dev is not None else None,
            "rev": float(rev) if rev is not None else None,
            "patents": int(pat[0] or 0), "granted": int(pat[1] or 0),
            "papers": int(zh_p), "tag": tag,
        })

    n_dev = C.norm([c["dev"] for c in carriers])
    n_rev = C.norm([c["rev"] for c in carriers])
    n_pat = C.norm([c["patents"] + c["papers"] for c in carriers])
    n_grt = C.norm([c["granted"] for c in carriers])
    n_tag = C.norm([c["tag"] for c in carriers])

    scored = []
    for i, c in enumerate(carriers):
        res_parts = [n_dev[i], n_rev[i]]
        res = (sum(p for p in res_parts if p is not None) / len(res_parts)) if any(p is not None for p in res_parts) else None
        out_v = n_pat[i]
        cap_parts = [p for p in [n_grt[i], n_tag[i]] if p is not None]
        cap = (sum(cap_parts) / len(cap_parts)) if cap_parts else None
        dims = [res, out_v, cap]
        avail = [d for d in dims if d is not None]
        score = (sum(avail) / len(avail) * 100) if avail else None
        scored.append({**c, "d_res": res, "d_out": out_v, "d_cap": cap, "score": score})

    scores = [s["score"] for s in scored if s["score"] is not None]
    stats = {}
    if scores:
        ss = sorted(scores)
        stats = dict(n=len(scores), positive=len([s for s in scores if s > 0]),
                     min=round(min(scores), 2), max=round(max(scores), 2),
                     mean=round(sum(scores) / len(scores), 2), median=round(ss[len(ss) // 2], 2))
    top = sorted([s for s in scored if s["score"] is not None], key=lambda x: -x["score"])[:10]

    result = {
        "metric_id": "M_INNOV_CARRIER_INDEX_GLOBAL",
        "metric_name": "创新载体创新能力指数",
        "also_serves": ["M_INNOV_CARRIER_RANK_GLOBAL"],
        "method": "王惠 V1.5：载体批内三维极值归一等权×100；缺测维重归一；名称对齐",
        "source": "gkx（三方库；行数读 GKX_INVENTORY.json）",
        "stat_year": YEAR,
        "probes": probes,
        "compute": {
            "n_carriers": len(carriers),
            "dim_coverage": {
                "annual_dev_or_emp": len([c for c in carriers if c["dev"] is not None]),
                "revenue": len([c for c in carriers if c["rev"] is not None]),
                "patents_or_papers": len([c for c in carriers if c["patents"] + c["papers"] > 0]),
                "granted": len([c for c in carriers if c["granted"] > 0]),
                "hightech_tag_cn": len([c for c in carriers if c["tag"] == 1]),
            },
            **({"stats": stats} if stats else {}),
            "top10": [{"name": t["name"], "src": t["src"], "patents": t["patents"], "papers": t["papers"],
                       "granted": t["granted"], "score": round(t["score"], 2)} for t in top],
        },
        "support_judgment": None,
    }
    cov = result["compute"]["dim_coverage"]
    dims_ok = (cov["patents_or_papers"] > 100 and cov["annual_dev_or_emp"] + cov["revenue"] > 50)
    has_dist = stats and stats["max"] > stats["min"]
    result["support_judgment"] = "完全转换支持" if (dims_ok and has_dist) else "部分支持"
    result["support_note"] = (
        f"载体入集 {len(carriers)}；产出维覆盖 {cov['patents_or_papers']}；资源维覆盖 dev {cov['annual_dev_or_emp']}/rev {cov['revenue']}；"
        f"分布 {'非退化' if has_dist else '退化'}"
    )

    C.write_out("M_INNOV_CARRIER_INDEX_GLOBAL", result)
    print({k: v for k, v in result.items() if k != "compute"})
    print(json.dumps(result["compute"], ensure_ascii=False)[:1800])


if __name__ == "__main__":
    main()

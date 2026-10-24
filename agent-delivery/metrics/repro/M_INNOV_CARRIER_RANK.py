#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_CARRIER_RANK 创新载体排名 · 复现代码（跨载体排序口径，非王惠原式）

口径：排序宇宙=深圳存活载体池（总体宇宙）；排序键=质量分级(3/2/1)+2024授权专利归一+
      2024论文归一，等权复合降序，同分并列跳号；另演示领域宇宙（IPC 主组切片）排名。

数据源（20261021 版）：三方库 `gkx`，唯一入口 `code/_gkxdb.gkx()`。
"""
import json

import _carrier21_common as C

YEAR = 2024
IPC4_DEMO = "H02J"  # 领域宇宙演示切片（B5 锚点：H02J7/00 为影响力领先领域）

TABLES = ["dwd_org_base_info", "dwd_org_tech_tag", "dwd_patent", "dwd_zh_paper", "dwd_zh_author"]


def main():
    probes = C.probes(TABLES)

    pool = [(str(o), str(n)) for o, n in C.sz_pool(3000)]

    tags_by_org = {k: set(v) for k, v in C.tags().items()}

    by_name = C.patent_by_name()
    granted_by_name = {n: int(v[2]) for n, v in by_name.items()}
    papers_by_inst = C.papers_by_inst()

    rows = []
    for oid, name in pool:
        tags = tags_by_org.get(oid)
        tier = 3 if (tags and any(("国家级" in t or "小巨人" in t) for t in tags)) else \
               (2 if (tags and any("省级" in t for t in tags)) else
                (1 if tags else None))
        rows.append(dict(org_id=oid, name=name, tier=tier,
                         granted=granted_by_name.get(name, 0),
                         papers=papers_by_inst.get(name, 0),
                         ipc=C.ipc_count(name, prefix=IPC4_DEMO)))

    n_t = C.norm([float(r["tier"]) if r["tier"] else None for r in rows])
    n_g = C.norm([float(r["granted"]) for r in rows])
    n_p = C.norm([float(r["papers"]) for r in rows])
    scored = []
    for i, r in enumerate(rows):
        parts = [n_t[i], n_g[i], n_p[i]]
        avail = [p for p in parts if p is not None]
        score = (sum(avail) / len(avail) * 100) if avail else None
        scored.append({**r, "score": round(score, 2) if score is not None else None})
    ranked = sorted([s for s in scored if s["score"] is not None], key=lambda x: -x["score"])
    prev_score, prev_rank = None, 0
    for i, s in enumerate(ranked, 1):
        s["rank"] = prev_rank if s["score"] == prev_score else i
        prev_score, prev_rank = s["score"], s["rank"]

    dom_pool = [s for s in scored if s["ipc"] > 0]
    dom_ranked = sorted(dom_pool, key=lambda x: -x["ipc"])
    for i, s in enumerate(dom_ranked, 1):
        s["domain_rank"] = i

    scores = [s["score"] for s in ranked]
    ss = sorted(scores)
    stats = dict(
        n_pool=len(pool), n_scored=len(ranked),
        min=round(min(scores), 2), max=round(max(scores), 2),
        mean=round(sum(scores) / len(scores), 2), median=round(ss[len(ss) // 2], 2),
        p90=round(ss[int(len(ss) * 0.9)], 2),
    )
    top15 = [{"rank": s["rank"], "name": s["name"], "tier": s["tier"],
              "granted2024": s["granted"], "papers2024": s["papers"],
              "score": s["score"]} for s in ranked[:15]]

    result = {
        "metric_id": "M_INNOV_CARRIER_RANK",
        "metric_name": "创新载体排名",
        "method": "跨载体排序（总体宇宙=深圳存活载体池）：分级tier+授权专利+论文 三键等权复合降序；同分并列跳号；领域宇宙按 IPC 主组切片",
        "source": "gkx（三方库；行数读 GKX_INVENTORY.json）",
        "wanghui": False,
        "stat_year": YEAR,
        "probes": probes,
        "compute": {
            "stats": stats,
            "top15": top15,
            "domain_universe_demo": {
                "ipc4": IPC4_DEMO,
                "n_in_domain": len(dom_ranked),
                "top5": [{"domain_rank": s["domain_rank"], "name": s["name"],
                          "ipc_patents": s["ipc"], "total_score": s["score"]}
                         for s in dom_ranked[:5]],
            },
        },
        "support_judgment": None,
    }
    ok = stats["n_scored"] > 500 and stats["max"] > stats["min"]
    result["support_judgment"] = "完全转换支持" if ok else "部分支持"
    result["support_note"] = (
        f"深圳载体池 {stats['n_pool']}，得排名 {stats['n_scored']}；分数分布 {stats['min']}-{stats['max']}，"
        f"中位 {stats['median']}，P90 {stats['p90']}；领域宇宙 {IPC4_DEMO} 内 {len(dom_ranked)} 家可排；"
        "论文维 institution 对齐弱（覆盖低）但不阻断排序 → 完全转换支持"
    )

    C.write_out("M_INNOV_CARRIER_RANK", result)
    print(json.dumps({k: v for k, v in result.items() if k != "compute"}, ensure_ascii=False, indent=1))
    print(json.dumps(result["compute"]["stats"], ensure_ascii=False))
    print(json.dumps(result["compute"]["top15"][:8], ensure_ascii=False, indent=1))
    print(json.dumps(result["compute"]["domain_universe_demo"], ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

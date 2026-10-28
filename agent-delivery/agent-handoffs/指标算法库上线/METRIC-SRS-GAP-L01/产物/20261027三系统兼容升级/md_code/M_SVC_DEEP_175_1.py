#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""知识产权服务机构技术力评价模型（M_SVC_DEEP_175_1）—— gkx 口径，自包含。

四维（需规 §1.1.1.1.1.1.1.9.4）：
    专业能力   —— dwd_patent.agency 与机构名对齐后的代理件数（样本扫描，见下）
    业务范围   —— 产业覆盖数：gkx 无 dwd_org_industry_tags（旧库该表仅 104 行且信用码失配）→ 无源
    成功案例数 —— 正式计数待建；现用资讯条数代理（弱）
    合作伙伴   —— 投资边 + 机构股东边的去重对端数

专业能力的取数：dwd_patent 共 294 万件、agency 为自由文本。为控成本，按 dwd_id 区间分页
扫描（每页 30 万 id），命中 IP 池机构名的行计入件数。快照
code/_snapshots21/svc21_agency_scan_frozen_20261022.json（扫描器 76 页时点的冻结副本）记录已扫页与命中，本脚本只读该快照，
不连库；扫描覆盖率写进产物（sample_share），不外推。

数据源：code/_snapshots21/svc21_facts_20261022.json + svc21_agency_scan_frozen_20261022.json
产出：code/M_SVC_DEEP_175_1_out.json
运行：cd code && python3 M_SVC_DEEP_175_1.py
"""
from __future__ import annotations

import json
import os
import statistics
import time
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
AGENCY = os.path.join(SNAP, "svc21_agency_scan_frozen_20261022.json")
# 冻结副本：扫描器仍在增量推进，本件用 cp 时点（76 页 / 1,678,411 件）的冻结快照，
# 保证文档、产物与快照三者可长期复现；增量页不进本件，等扫描全量完成后另起一版。
OUT = os.path.join(HERE, "M_SVC_DEEP_175_1_out.json")


def mm(vals: dict) -> dict:
    """min-max（内联复制自 M_SVC_DEEP_174_1.py，不 import 共享模块）"""
    xs = [v for v in vals.values() if v is not None]
    if not xs:
        return {}
    lo, hi = min(xs), max(xs)
    if hi - lo <= 1e-12:
        return {k: 0.5 for k in vals if vals[k] is not None}
    return {k: (v - lo) / (hi - lo) for k, v in vals.items() if v is not None}


def main():
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    ag = json.load(open(AGENCY, encoding="utf-8"))
    pool, news, tags = f["pool"], f["news"], f["tags"]

    ip_pool = [o for o, v in pool.items() if v.get("ptype2") == "IP"]
    n = len(ip_pool)

    # 合作伙伴
    adj = defaultdict(set)
    for a, b, _m in f["invest_edges"]:
        if a in pool and b in pool and a != b:
            adj[a].add(b); adj[b].add(a)
    for a, b in f["shareholder_edges"]:
        if b and a in pool and b in pool and a != b:
            adj[a].add(b); adj[b].add(a)

    # 专业能力：agency 命中
    pn = {}
    for name, rec in (ag.get("hits") or {}).items():
        o = rec.get("org_id")
        if o in ip_pool:
            pn[o] = int(rec.get("pn", 0))

    newsc = {o: int(news.get(o, 0)) for o in ip_pool}
    tagc = {o: int(tags.get(o, 0)) for o in ip_pool}
    deg = {o: len(adj.get(o, ())) for o in ip_pool}

    s_ability = mm({o: v for o, v in pn.items() if v > 0})
    s_case = mm({o: v for o, v in newsc.items() if v > 0})
    s_partner = mm({o: v for o, v in deg.items() if v > 0})

    dims = {"专业能力": s_ability, "业务范围": {}, "成功案例数": s_case, "合作伙伴": s_partner}
    w = {"专业能力": 0.25, "业务范围": 0.25, "成功案例数": 0.25, "合作伙伴": 0.25}

    idx, used = {}, {}
    for o in ip_pool:
        av = [(k, dims[k][o]) for k in dims if o in dims[k]]
        if len(av) < 2:
            continue
        ws = sum(w[k] for k, _ in av)
        idx[o] = 100.0 * sum(w[k] * v for k, v in av) / ws
        used[o] = [k for k, _ in av]

    vals = sorted(idx.values())
    ranked = sorted(idx.items(), key=lambda x: -x[1])
    top = [{"org_id": o, "name": pool[o]["name"], "city": pool[o]["city"],
            "index": round(v, 2), "agency_patents": pn.get(o, 0), "dims": used[o],
            "ability_scored": o in s_ability,
            "news": newsc[o], "partners": deg[o], "tags": tagc[o]} for o, v in ranked[:10]]

    scanned = int(ag.get("pn_scanned", 0))
    total_patents = 2942379
    hit_pn = sum(pn.values())
    hit_all = sum(int(r.get("pn", 0)) for r in (ag.get("hits") or {}).values())

    out = {
        "metric_id": "M_SVC_DEEP_175_1",
        "metric_name": "知识产权服务机构技术力评价模型",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": ("四维中专业能力（agency 代理件数）与合作伙伴（资本边）可现转，成功案例仅有资讯代理；"
                            "业务范围维在 gkx 无产业标签表（dwd_org_industry_tags 缺失）→ 结构性缺维，部分支持"),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_patent(agency) 样本扫描", "rows": scanned,
             "snapshot": "code/_snapshots21/svc21_agency_scan_frozen_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_invest_info / dwd_org_shareholder_info / dwd_org_important_news_info",
             "rows": f["invest_meta"]["rows_total"] + f["shareholder_meta"]["rows_total"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("专利件数按 agency 名称对齐取全样本，不再按年切分——dwd_patent.apdt_year 只有 "
                            "2021—2026（2017—2020 零行），做年度序列会把缺失年当 0 摊入；本件刻意不做年份维"),
        "population": {"orgs_ip_primary": n, "share_of_pool": round(n / len(pool), 6)},
        "agency_scan": {
            "pages_done": ag.get("done_pages"), "pages_total": ag.get("pages_total"),
            "pn_scanned": scanned, "with_agency": ag.get("with_agency"),
            "sample_share": round(scanned / total_patents, 4),
            "ip_pool_matched": len(pn), "ip_pool_hit_share": round(len(pn) / n, 6) if n else None,
            "hit_patents": hit_pn, "hit_patents_all_types": hit_all,
            "coverage_note": ("样本覆盖率为 %.1f%%（按 dwd_id 区间顺序扫描，非随机抽样）；"
                              "命中机构均为真实代理所，件数为样本内计数，未按覆盖率外推" % (100.0 * scanned / total_patents)),
        },
        "dimensions": {k: {"n": len(v), "share_of_pool": round(len(v) / n, 6) if n else None} for k, v in dims.items()},
        "index": {"n": len(idx), "mean": round(statistics.mean(vals), 2) if vals else None,
                  "median": round(statistics.median(vals), 2) if vals else None,
                  "max": round(vals[-1], 2) if vals else None},
        "top10": top,
        "index_coverage_note": ("指数只对 %d/%d 家（≥2 维非空）成立；专业能力维仅 %d 家命中，"
                                "故指数是「可命中子集内的相对排序」，不是 IP 机构全体的技术力排名"
                                % (len(idx), n, len(pn))),
        "scope_dim_gap": {"needed": "dwd_org_industry_tags（机构-产业多对多）或主营业务→产业映射表",
                          "existing": "gkx 无该表；旧库该表仅 104 行且 credit_code 与底册失配",
                          "impact": "业务范围维全空，四维实际只能按 3 维合成（等权分母 0.75）"},
        "case_proxy_gap": {"needed": "svc_success_case_count（代理/服务成功案例数）",
                           "existing": "资讯条数（dwd_org_important_news_info）",
                           "impact": "资讯量是曝光度，不等于成功案例；对 IP 机构尤其弱（池内仅 %d 家有资讯）"
                                     % len([o for o in ip_pool if newsc[o]])},
        "compute": {"elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("IP 池", n, "agency 命中", len(pn), "命中专利", hit_pn, "样本", scanned,
          "覆盖 %.1f%%" % (100.0 * scanned / total_patents))
    print("分维覆盖", {k: len(v) for k, v in dims.items()}, "指数覆盖", len(idx))
    print("top", [(t["name"], t["index"], t["agency_patents"]) for t in top[:3]])
    print("->", OUT)


if __name__ == "__main__":
    main()

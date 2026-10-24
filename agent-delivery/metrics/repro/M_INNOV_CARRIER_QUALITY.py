#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_CARRIER_QUALITY 创新载体质量 · 复现代码（分级加权口径）

口径：科技资质分级（国家级>省级>无标签）+ 加权质量分（分维覆盖）。
数据：gkx.dwd_org_tech_tag 全量 202,424 行（15+ 级标签）；2024 授权专利作产出旁证。
数据源（20261021 版）：三方库 `gkx`，唯一入口 `code/_gkxdb.gkx()`。
"""
import json

import _carrier21_common as C

TABLES = ["dwd_org_tech_tag", "dwd_org_base_info", "dwd_research_institute_base_info",
          "dwd_patent", "dwd_org_annual_financial_info"]


def main():
    probes = C.probes(TABLES)

    tags_by_org = {k: set(v) for k, v in C.tags().items()}

    NATIONAL_KW = ["国家级", "小巨人"]
    PROV_KW = ["省级"]
    national_set, prov_set, plain_set = set(), set(), set()
    for oid, tags in tags_by_org.items():
        if any(any(k in t for k in NATIONAL_KW) for t in tags):
            national_set.add(oid)
        elif any(any(k in t for k in PROV_KW) for t in tags):
            prov_set.add(oid)
        else:
            plain_set.add(oid)

    # 名册 + 深圳切片：一次读 gkx 主档缓存（189,116 行，字段同旧版）
    base = json.loads((C.CACHE / "base_20261021.json").read_text(encoding="utf-8"))
    oid2name = {str(r[0]): str(r[2]) for r in base}
    sz_orgs = {str(r[0]) for r in base if str(r[4] or "").startswith("深圳")}

    # 2024 授权专利（按第一申请人名去重 pn —— 与旧脚本 COUNT(DISTINCT pn) 同口径）
    by_name = C.patent_by_name()
    granted_by_name = {n: int(v[2]) for n, v in by_name.items()}

    scored = []
    for oid, name in oid2name.items():
        tags = tags_by_org.get(oid)
        tier = 3 if (tags and oid in national_set) else (2 if (tags and oid in prov_set) else (1 if tags else None))
        granted = granted_by_name.get(name, 0)
        scored.append(dict(org_id=oid, name=name, sz=(oid in sz_orgs), tier=tier, granted=granted))

    tiers = [s["tier"] for s in scored if s["tier"] is not None]
    gvals = [s["granted"] for s in scored if s["tier"] is not None]
    n_t = C.norm([float(t) for t in tiers])
    n_g = C.norm([float(g) for g in gvals])
    for i, s in enumerate([x for x in scored if x["tier"] is not None]):
        parts = [n_t[i], n_g[i]]
        s["quality"] = round(sum(parts) / 2 * 100, 2)
    scored_final = [s for s in scored if s["tier"] is not None]

    qvals = [s["quality"] for s in scored_final]
    qvals_sorted = sorted(qvals)
    stats = dict(
        n=len(qvals),
        national=len([s for s in scored_final if s["tier"] == 3]),
        provincial=len([s for s in scored_final if s["tier"] == 2]),
        plain=len([s for s in scored_final if s["tier"] == 1]),
        sz=len([s for s in scored_final if s["sz"]]),
        min=round(min(qvals), 2), max=round(max(qvals), 2),
        mean=round(sum(qvals) / len(qvals), 2),
        median=round(qvals_sorted[len(qvals_sorted) // 2], 2),
    )
    top = sorted(scored_final, key=lambda x: -x["quality"])[:12]

    sz_vs = [s["quality"] for s in scored_final if s["sz"]]
    result = {
        "metric_id": "M_INNOV_CARRIER_QUALITY",
        "metric_name": "创新载体质量",
        "method": "分级加权（国家级3/省级2/普通1）× 产出旁证（2024授权专利极值归一）等权×100；无标签载体不计分（缺测而非零分）",
        "source": "gkx（三方库；行数读 GKX_INVENTORY.json）",
        "probes": probes,
        "compute": {
            "stats": stats,
            "tag_coverage": {
                "tagged_orgs": len(tags_by_org),
                "national": len(national_set),
                "provincial": len(prov_set),
                "plain": len(plain_set),
            },
            "top12": [{"name": t["name"], "tier": t["tier"], "sz": t["sz"],
                       "granted2024": t["granted"], "quality": t["quality"]} for t in top],
            "sz_quality_stats": dict(
                n=len(sz_vs), mean=round(sum(sz_vs) / len(sz_vs), 2),
                median=round(sorted(sz_vs)[len(sz_vs) // 2], 2),
                national=len([s for s in scored_final if s["sz"] and s["tier"] == 3]),
            ),
        },
        "support_judgment": None,
    }

    ok = stats["n"] > 1000 and stats["max"] > stats["min"] and stats["national"] > 100
    result["support_judgment"] = "完全转换支持" if ok else "部分支持"
    result["support_note"] = (
        f"gkx.dwd_org_tech_tag 实测 {probes['gkx.dwd_org_tech_tag']} 行；有标签载体 {len(tags_by_org)} 家"
        f"（国家级 {len(national_set)} / 省级 {len(prov_set)} / 普通 {len(plain_set)}）；"
        f"质量分 n={stats['n']}，分布 {stats['min']}-{stats['max']} 非退化；"
        "依赖结构+数据量足且已现转出分 → 完全转换支持（无现成结果面）"
    )

    C.write_out("M_INNOV_CARRIER_QUALITY", result)
    print({k: v for k, v in result.items() if k != "compute"})
    print(json.dumps(result["compute"]["stats"], ensure_ascii=False))
    print(json.dumps(result["compute"]["tag_coverage"], ensure_ascii=False))
    print(json.dumps(result["compute"]["top12"][:6], ensure_ascii=False))
    print(json.dumps(result["compute"]["sz_quality_stats"], ensure_ascii=False))


if __name__ == "__main__":
    main()

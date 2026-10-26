#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_INNOVATIVE_COUNT 创新型企业数（梯度培育四类标签去重计数）。

口径：calc-logic V3-2026-08-09（企业分析 / 重点企业分析 / 类型与区域分析）
    org_tag ∈ {创新型中小企业, 专精特新中小企业, 专精特新小巨人, 制造业单项冠军}，按 org_id 去重。
取数：`code/_snapshots21/tech_tags_20261021.json`（`gkx.dwd_org_tech_tag` 202,424 行 / 32,322 家机构）
      × `code/_snapshots21/base_20261021.json`（189,116 行底册，取省/市），零 DB。
"""
from __future__ import annotations

import json
import time
from pathlib import Path

BASE = Path(__file__).parent
SNAP = BASE / "_snapshots21"
METRIC = "M_ENT_INNOVATIVE_COUNT"

# 梯度培育四类（工信部《优质中小企业梯度培育管理办法》口径）
FAMILIES = [
    ("创新型中小企业", "创新型中小企业"),
    ("专精特新中小企业", "专精特新中小企业"),
    ("专精特新小巨人", "专精特新小巨人"),
    ("制造业单项冠军", "单项冠军"),
]
CITY4 = ["深圳市", "广州市", "东莞市", "惠州市"]


def main():
    t0 = time.time()
    tt = json.loads((SNAP / "tech_tags_20261021.json").read_text(encoding="utf-8"))
    base = json.loads((SNAP / "base_20261021.json").read_text(encoding="utf-8"))
    bidx = {r[0]: r for r in base}

    per = {f[1]: set() for f in FAMILIES}
    union = set()
    tag_rows = 0
    variants = {f[1]: {} for f in FAMILIES}
    per_nonexpired = {f[1]: set() for f in FAMILIES}
    union_nonexpired = set()
    for oid, tags in tt.items():
        tag_rows += len(tags)
        for t in tags:
            for label, key in FAMILIES:
                if key in t:
                    per[key].add(oid)
                    union.add(oid)
                    variants[key][t] = variants[key].get(t, 0) + 1
                    if "过期待复核" not in t:
                        per_nonexpired[key].add(oid)
                        union_nonexpired.add(oid)

    # 一企多牌结构
    fam_per_org = {}
    for oid in union:
        k = sum(1 for _, key in FAMILIES if oid in per[key])
        fam_per_org[k] = fam_per_org.get(k, 0) + 1

    # 区域分布（org_id → 底册 city / province）
    city = {}
    prov = {}
    unmatched = 0
    for oid in union:
        b = bidx.get(oid)
        if not b:
            unmatched += 1
            continue
        city[b[4]] = city.get(b[4], 0) + 1
        prov[b[3]] = prov.get(b[3], 0) + 1

    per_family_city = {key: {} for _, key in FAMILIES}
    for _, key in FAMILIES:
        for oid in per[key]:
            b = bidx.get(oid)
            if b:
                per_family_city[key][b[4]] = per_family_city[key].get(b[4], 0) + 1

    fam_counts = {key: len(per[key]) for _, key in FAMILIES}
    city4_total = sum(city.get(c, 0) for c in CITY4)
    overlap_pairs = {}
    keys = [k for _, k in FAMILIES]
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            overlap_pairs[f"{keys[i]}×{keys[j]}"] = len(per[keys[i]] & per[keys[j]])

    payload = {
        "metric_id": METRIC,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_sec": round(time.time() - t0, 2),
        "support_judgment": "完全转换支持",
        "definition": {
            "unit": "家企业",
            "dedupe_key": "org_id",
            "families": [{"label": lb, "match": kw, "n_org": fam_counts[kw]} for lb, kw in FAMILIES],
            "rule": "四类标签任一命中即计入，一企多牌只计一次",
        },
        "result": {
            "innovative_count": len(union),
            "share_of_base_pct": round(100.0 * len(union) / len(base), 2),
            "share_of_tagged_pct": round(100.0 * len(union) / len(tt), 2),
            "city4_total": city4_total,
            "city4_share_pct": round(100.0 * city4_total / len(union), 2),
            "unmatched_base": unmatched,
        },
        "family_counts": fam_counts,
        "label_variants": {k: dict(sorted(v.items(), key=lambda kv: -kv[1]))
                           for k, v in variants.items()},
        "sensitivity_exclude_expired": {
            "rule": "剔除标签名含『过期待复核』的写法（341 家小巨人 + 72 家单项冠军标签）",
            "family_counts": {k: len(v) for k, v in per_nonexpired.items()},
            "dedup_total": len(union_nonexpired),
            "delta_vs_main": len(union_nonexpired) - len(union),
        },
        "family_city": per_family_city,
        "city_dist": dict(sorted(city.items(), key=lambda kv: -kv[1])),
        "prov_dist": dict(sorted(prov.items(), key=lambda kv: -kv[1])[:10]),
        "fam_per_org": dict(sorted(fam_per_org.items())),
        "overlap_pairs": dict(sorted(overlap_pairs.items(), key=lambda kv: -kv[1])),
        "coverage": {
            "tag_rows": 202424,
            "tagged_orgs": len(tt),
            "tags_in_cache": tag_rows,
            "base_rows": len(base),
            "join_rate_vs_base": round(100.0 * sum(1 for k in tt if k in bidx) / len(tt), 3),
            "base_coverage_pct": round(100.0 * len(tt) / len(base), 2),
        },
        "notes": [
            "标签源为 gkx.dwd_org_tech_tag（202,424 行 / 32,322 家），已剔除 is_deleted=1。",
            "底册 join 走 org_id 主键（非名称），32,321/32,322 = 99.997% 可落底册。",
            "省级/国家级同义标签（如「省级专精特新中小企业」「国家级专精特新小巨人企业」）按包含关系归入同一族，不重复计数。",
            "「单项冠军」族同时覆盖「制造业单项冠军企业」与「国家级/示范企业」写法。",
        ],
    }
    out = BASE / f"{METRIC}_out.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: payload[k] for k in ("support_judgment", "result", "family_counts",
                                              "fam_per_org", "city_dist", "coverage")},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

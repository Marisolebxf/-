#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全球服务机构分布（按国家计数）（M_SVC_ORG_CNT）—— gkx 口径，自包含。

数据源（只读落盘快照，零 SQL、零 demo）：
    code/_snapshots21/svc21_facts_20261022.json   pool 44,153 家
    code/_snapshots21/base_20261021.json          189,116 行（province / city）

口径：country(e) 由 base_info.province 归并（国内省→中国）；base 无 country 列，
      海外格留空不造数，country_covered 如实报 1。
产出：code/M_SVC_ORG_CNT_out.json（覆盖写）
运行：cd code && python3 M_SVC_ORG_CNT.py
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
BASE = os.path.join(SNAP, "base_20261021.json")
OUT = os.path.join(HERE, "M_SVC_ORG_CNT_out.json")


def main() -> None:
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    base = json.load(open(BASE, encoding="utf-8"))
    pool = f["pool"]
    bmap = {r[0]: r for r in base}
    ids = list(pool.keys())
    n = len(ids)

    prov = Counter()
    for o in ids:
        r = bmap.get(o)
        prov[(r[3] if r and r[3] else "（未回联底册）")] += 1

    # 省份 → 国家：gkx 底册 province 全部为中华人民共和国省级行政区
    country = Counter()
    for p, c in prov.items():
        country["中国" if p.endswith(("省", "市", "自治区", "特别行政区")) else "（未判定）"] += c

    city = Counter((bmap.get(o)[4] if bmap.get(o) and bmap.get(o)[4] else "（未回联底册）")
                   for o in ids)
    covered = [c for c, v in country.items() if v > 0 and c != "（未判定）"]
    stage_mult = sum(len(v["stages"]) for v in pool.values())
    stage_union = sum(1 for v in pool.values() if v["stages"])

    out = {
        "metric_id": "M_SVC_ORG_CNT",
        "metric_name": "全球服务机构分布（按国家计数）",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": (
            "国内格可完整闭合（44,132 家经 province→中国归并、省级 drill-down 可对账）；"
            "但 gkx 底册无 country 列、无与六类服务机构口径闭合的海外名录，"
            "国家轴海外格始终无源，按四档落部分支持"),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_org_product_info", "rows": f["population"]["product_info_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_base_info（province / city）",
             "rows": f["population"]["base_all"],
             "snapshot": "code/_snapshots21/base_20261021.json"},
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "截面分布指标：国家格与省级 drill-down 均为当前存量，无年度分母。"
            "趋势能力依赖成立年序列（见 M_SVC_NEW_CNT），本件不摊年。"),
        "population": {
            "distinct_org_id": n,
            "join_base_rows": sum(v for p, v in prov.items() if p != "（未回联底册）"),
            "join_base_rate": round((n - prov.get("（未回联底册）", 0)) / n, 6),
            "country_covered": len(covered),
            "country_rows": len([c for c, v in country.items() if v > 0]),
        },
        "country_dist": [[c, v] for c, v in country.most_common()],
        "province_dist": [[p, v] for p, v in prov.most_common()],
        "city_dist": [[c, v] for c, v in city.most_common(10)],
        "country_covered": len(covered),
        "overseas_source_probe": {
            "base_country_column": "不存在（dwd_org_base_info 无 country/nation 类列）",
            "gkx_forg_tables": "存在 dwd_forg_* 近源，但为英国偏企业名录/全球科研机构名录，与六类服务机构口径不闭合",
            "decision": "海外格留空、返回空集而非 0，避免把「无源」渲染成「该国无机构」",
        },
        "pool_reconciliation": {
            "org_pool": n,
            "stage_multiplicity_sum": stage_mult,
            "stage_union_orgs": stage_union,
            "note": ("与 M_SVC_CHAIN_SEGMENT_ORG_COUNT 同池：该件 population.distinct_org_id=44,153；"
                     "%d 是六环节多命中合计，%d 是命中至少一个环节的去重机构数。"
                     "本件 ORG_CNT 数的是机构池 44,153，不是环节去重 %d" % (stage_mult, stage_union, stage_union)),
            "delta_vs_stage_union": n - stage_union,
        },
        "difference_vs_old_draft": {
            "population": "旧稿 43,296（演示库 svc_org_circle）→ 本件 44,153（gkx 经营范围机构）",
            "province": "旧稿 粤 43,292 / 京 3 / 浙 1 → 本件 粤 44,132 + 未回联 21",
            "reason": "换源后池子只覆盖广东一省，旧稿的京/浙三两家在 gkx 口径下不存在",
        },
        "gaps": {
            "overseas": "无闭合海外名录；国家轴仅中国一格",
            "hk_mo_tw": "需求未裁决港澳台单列或并入中国，gkx 底册亦无对应字段",
            "trend": "跨国份额比较不可用，只能做国内省际比较",
        },
        "compute": {"status": "ok", "elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("pool=%d countries=%d prov=%s -> %s" % (n, len(covered), prov.most_common(3), OUT))


if __name__ == "__main__":
    main()

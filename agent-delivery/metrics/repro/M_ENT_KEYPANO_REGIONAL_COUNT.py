#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_KEYPANO_REGIONAL_COUNT —— 覆盖区域数 2026-10-23

口径真源：`gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_KEYPANO_REGIONAL_COUNT.md`

    COUNT(DISTINCT region_key)
    WHERE org_id ∈ 该链重点名单
      AND region_id 非空
      AND region_key ∈ {省} ∪ {市} ∪ {县区} ∪ {已点亮的复合区域}
    GROUP BY chain_code

细节（正本原文）：
  - 省 = admin: + 2 位、市 = admin: + 4 位、县区 = admin: + 6 位；
  - 复合区域 = scope:gba / yrd / jjj，`region_id` 前缀命中成员表才点亮；
  - 热门城市并入市，不另开 `scope:shenzhen`；national/global/国外城市不进集合；
  - 一个深圳南山企业 = 广东 + 深圳 + 南山区 + 大湾区 = 4 个键。

本脚本零 DB。区域键已由 `_enrich_keypano_base_20261023.py` 在快照里备好。
另读 `code/_snapshots21/chain_firm_index_20261023.json` 作**对照证据**：
全库链标签表本身覆盖 31—32 个省、250—339 个市，用来说明区域维退化不是表的问题。
"""
from __future__ import annotations

import json
from collections import Counter

import _keypano_common as K

OUT = K.HERE / "M_ENT_KEYPANO_REGIONAL_COUNT_out.json"
FULL = K.SNAP / "chain_firm_index_20261023.json"


def main() -> None:
    base = K.load_base()
    cn = K.chain_names()
    p, c, a = K.admin_names()
    st = base["stats"]
    firms = base["firms"]

    chain_firm = Counter(ch for f in firms for ch in (f.get("chains") or []))
    scope_all = K.SCOPE_CN

    per_chain = {}
    for ch in chain_firm:
        keys = set()
        for f in firms:
            if ch in (f.get("chains") or []):
                keys.update(f["region_keys"])
        per_chain[ch] = keys

    union = set()
    for keys in per_chain.values():
        union |= keys

    def breakdown(keys: set) -> dict:
        cnt = Counter(K.key_kind(k) for k in keys)
        return {"province_n": cnt.get("prov", 0), "city_n": cnt.get("city", 0),
                "area_n": cnt.get("area", 0), "scope_n": cnt.get("scope", 0),
                "total_n": len(keys)}

    full = json.loads(FULL.read_text(encoding="utf-8"))

    payload = {
        "metric_id": "M_ENT_KEYPANO_REGIONAL_COUNT",
        "metric_name": "覆盖区域数",
        "script": "M_ENT_KEYPANO_REGIONAL_COUNT.py",
        "data_source": "gkx",
        "grain": "chain_code → COUNT(DISTINCT region_key)",
        "shared_base": K.shared_base_block(base),
        "probes": {
            "roster_n": st["roster_n"],
            "in_chain_n": st["in_chain_n"],
            "chain_n": len(chain_firm),
            "region_key_any_n": st["region_key_any_n"],
            "province_missing_n": st["province_code_missing_n"],
            "city_missing_n": st["city_code_missing_n"],
            "area_blank_n": st["area_blank_n"],
            "area_code_missing_n": st["area_code_missing_n"],
            "union_cover_n": len(union),
            "union_breakdown": breakdown(union),
            "scope_lit": sorted(k.split(":", 1)[1] for k in union if k.startswith("scope:")),
            "scope_unlit": sorted(s for s in scope_all
                                  if f"scope:{s}" not in union),
            "scope_firm_n": {"gba": st["scope_gba_n"], "yrd": st["scope_yrd_n"],
                             "jjj": st["scope_jjj_n"]},
            "admin_universe": {"province_n": len(p), "city_n": len(c), "area_n": len(a),
                               "source": "code/_snapshots21/admin_area_20261022.json"},
            "cover_vs_universe_pct": {
                "province_pct": K.pct(breakdown(union)["province_n"], len(p)),
                "city_pct": K.pct(breakdown(union)["city_n"], len(c)),
                "area_pct": K.pct(breakdown(union)["area_n"], len(a)),
            },
            "roster_geo": {
                "province_n": len({f.get("province") for f in firms}),
                "city_n": len({f.get("city") for f in firms}),
                "province_list": sorted({f.get("province") for f in firms}),
                "city_list": sorted({f.get("city") for f in firms}),
            },
            "contrast_full_chain_table": {
                "source": "code/_snapshots21/chain_firm_index_20261023.json",
                "note": "全库 dwd_org_industry_tags 按省聚合的覆盖（含未匹配桶），"
                        "用来说明省/市维在库里有全国数据，退化只发生在代理名单侧。",
                "per_chain": {
                    ch: {"firm_n": sum(v for k, v in full["chain_prov"][ch].items()
                                       if k != "未匹配"),
                         "province_n": len([k for k in full["chain_prov"][ch] if k != "未匹配"]),
                         "city_n": len(full["chain_city"].get(ch, {}))}
                    for ch in full["chain_prov"]
                },
            },
        },
        "probes_negative": base["negative_evidence"],
        "result": {
            "per_chain": [
                {"chain_code": ch, "chain_name": cn.get(ch),
                 "chain_firm_n": chain_firm[ch],
                 "cover_count": len(per_chain[ch]),
                 **breakdown(per_chain[ch]),
                 "firm_per_region": round(chain_firm[ch] / len(per_chain[ch]), 4)
                 if per_chain[ch] else 0.0,
                 "region_keys": sorted(per_chain[ch])}
                for ch in sorted(chain_firm, key=lambda x: -len(per_chain[x]))
            ],
            "union": {
                "cover_count": len(union),
                "keys": sorted(union),
                "labels": sorted((K.key_label(k, p, c, a) for k in union)),
            },
            "cover_range": {
                "max": max(len(v) for v in per_chain.values()),
                "min": min(len(v) for v in per_chain.values()),
                "max_chain": max(per_chain, key=lambda x: len(per_chain[x])),
                "min_chain": min(per_chain, key=lambda x: len(per_chain[x])),
            },
        },
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": (
                "公式可完整执行，实出 12 条链的 cover_count（21—28 个键），"
                "并集 30 个键 = 1 省 + 4 市 + 23 区县 + 1 个复合区域（大湾区）。"
                "但有两条依赖缺口：①重点名单不存在，4,561 家是专利授权≥50 的代理名单，"
                "且这 4,561 家全部落在广东省 4 市（深圳 2,590、广州 1,020、东莞 775、惠州 176），"
                "区域维因此退化为单省切片——31 个省级行政区只点亮 1 个（3.2258%）、"
                "339 个市只点亮 4 个（1.1799%）、2,836 个区县只点亮 23 个（0.8110%）、"
                "3 个复合区域只点亮 1 个；②复合区域维表不存在——gkx 里 %scope% 表 0 张，"
                "scope 成员是按国务院三份规划纲要的行政范围自建的，不是 region_scope_member。"
                "对照证据表明这不是表结构的问题：同一张 dwd_org_industry_tags 全库聚合时"
                "每条链覆盖 31—32 个省、250—339 个市。所以判部分支持，不判完全不支持，"
                "也不抬成完全转换支持。"
            ),
            "criteria": {
                "formula_executable": True,
                "roster_table_exists": False,
                "roster_is_proxy": True,
                "roster_single_province": True,
                "region_id_column_exists": False,
                "scope_dim_exists": False,
                "scope_is_self_mapped": True,
                "full_table_national": True,
            },
        },
        **K.base_years_block(),
    }
    K.dump(OUT, payload)


if __name__ == "__main__":
    main()

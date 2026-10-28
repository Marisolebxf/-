#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_KEYPANO_QUAL_DISTRIBUTION —— 整链资质分布 2026-10-23

口径真源：`gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_KEYPANO_QUAL_DISTRIBUTION.md`

    COUNT(DISTINCT org_id)
    WHERE org_id ∈ 该链重点名单
      AND tag_code = :t
      AND 该企点亮 :region_key
    GROUP BY chain_code, tag_code, region_key

六类：foreign / high_tech / sme / listed / little_giant / little_giant_pro。
区域键：nation:CN + admin:省2 + admin:市4 + admin:县区6 + scope:gba|yrd|jjj。

三条不许忘的口径：
  1. 嵌套格子不可加（南山 ⊂ 深圳 ⊂ 广东 ⊂ 全国）；大湾区与广东可重叠，也不可加。
  2. 六类不可加总（一企可同时是高企与专精特新）。
  3. 区域份额的分母用**同母体**：单元格 / 该链该资质全国数；区县再给一个
     「占同城」分母（区县数 / 该链该资质同市数），不用全库 189,116。

本脚本零 DB。矩阵 1,560 格落旁挂快照，out.json 只放可审计的汇总与全国格。
"""
from __future__ import annotations

from collections import Counter, defaultdict

import _keypano_common as K

OUT = K.HERE / "M_ENT_KEYPANO_QUAL_DISTRIBUTION_out.json"
SIDE = K.SNAP / "keypano_qual_matrix_20261023.json"


def main() -> None:
    base = K.load_base()
    cn = K.chain_names()
    p, c, a = K.admin_names()
    st = base["stats"]
    firms = base["firms"]

    chain_firm = Counter(ch for f in firms for ch in (f.get("chains") or []))
    # 一企可多类，六类不可加 → 另算「至少一类」的并集，作为分母之外的口径参考
    union_by_chain = Counter()
    for f in firms:
        if any(K.tag_of(f, t) for t in K.QUAL_CODES):
            for ch in f.get("chains") or []:
                union_by_chain[ch] += 1

    cell: Counter = Counter()
    for f in firms:
        tags = [t for t in K.QUAL_CODES if K.tag_of(f, t)]
        if not tags:
            continue
        keys = set(f["region_keys"]) | {"nation:CN"}
        for ch in f.get("chains") or []:
            for t in tags:
                for k in keys:
                    cell[(ch, t, k)] += 1

    nation = {(ch, t): n for (ch, t, k), n in cell.items() if k == "nation:CN"}

    rows = []
    for (ch, t, k), n in sorted(cell.items()):
        kind = "nation" if k == "nation:CN" else K.key_kind(k)
        r = {
            "chain_code": ch,
            "chain_name": cn.get(ch),
            "tag_code": t,
            "tag_name": K.QUAL_CN[t],
            "region_key": k,
            "region_name": "全国" if kind == "nation" else K.key_label(k, p, c, a),
            "region_kind": kind,
            "ent_count": n,
            "share_in_chain_tag_pct": K.pct(n, nation.get((ch, t), 0)),
        }
        if kind == "area":
            parent = K.parent_key(k)
            r["parent_region_key"] = parent
            r["share_in_parent_pct"] = K.pct(n, cell.get((ch, t, parent), 0))
        rows.append(r)

    K.dump(SIDE, {
        "metric_id": "M_ENT_KEYPANO_QUAL_DISTRIBUTION",
        "grain": "chain_code + tag_code + region_key",
        "row_n": len(rows),
        "note": "只落非空格；空格按 0 处理，不落行。",
        "rows": rows,
    })

    # 交叉校验：同一 (chain,tag) 下省级格相加应正好等于全国格（每企 1 个省）
    prov_sum, city_sum, area_sum = Counter(), Counter(), Counter()
    for (ch, t, k), n in cell.items():
        if k == "nation:CN":
            continue
        kind = K.key_kind(k)
        if kind == "prov":
            prov_sum[(ch, t)] += n
        elif kind == "city":
            city_sum[(ch, t)] += n
        elif kind == "area":
            area_sum[(ch, t)] += n

    prov_ok = sum(1 for key, n in nation.items() if prov_sum.get(key, 0) == n)
    city_ok = sum(1 for key, n in nation.items() if city_sum.get(key, 0) == n)

    payload = {
        "metric_id": "M_ENT_KEYPANO_QUAL_DISTRIBUTION",
        "metric_name": "整链资质分布",
        "script": "M_ENT_KEYPANO_QUAL_DISTRIBUTION.py",
        "data_source": "gkx",
        "grain": "(chain_code, tag_code, region_key) → COUNT(DISTINCT org_id)",
        "shared_base": K.shared_base_block(base),
        "probes": {
            "roster_n": st["roster_n"],
            "in_chain_n": st["in_chain_n"],
            "cell_n": len(cell),
            "nation_cell_n": len(nation),
            "chain_n": len(chain_firm),
            "tag_n": len(K.QUAL_CODES),
            "tag_totals_roster": {
                t: {"code": t, "name": K.QUAL_CN[t],
                    "firm_n": sum(1 for f in firms if K.tag_of(f, t)),
                    "share_in_roster_pct": K.pct(sum(1 for f in firms if K.tag_of(f, t)),
                                                 st["roster_n"])}
                for t in K.QUAL_CODES
            },
            "tag_union_roster_n": sum(1 for f in firms
                                      if any(K.tag_of(f, t) for t in K.QUAL_CODES)),
            "tag_union_roster_pct": K.pct(
                sum(1 for f in firms if any(K.tag_of(f, t) for t in K.QUAL_CODES)),
                st["roster_n"]),
            "tag_sum_roster_n": sum(1 for f in firms for t in K.QUAL_CODES if K.tag_of(f, t)),
            "region_kind_cell_n": dict(Counter(r["region_kind"] for r in rows)),
            "checks": {
                "province_sum_equals_nation_n": prov_ok,
                "city_sum_equals_nation_n": city_ok,
                "pair_checked_n": len(nation),
                "area_sum_lt_nation_n": sum(1 for key, n in nation.items()
                                            if area_sum.get(key, 0) < n),
                "note": "省级格逐对相加 = 全国格（每企恰 1 个省）；市级同样成立；"
                        "县级之和小于全国，差额是区县名缺失/码未匹配的企业。",
            },
            "roster_geo": {
                "province_n": len({f.get("province") for f in firms}),
                "city_n": len({f.get("city") for f in firms}),
                "area_blank_n": st["area_blank_n"],
                "area_code_missing_n": st["area_code_missing_n"],
            },
            "field_basis": {
                "high_tech": "dwd_org_tech_tag 含「高新技术企业」且不含「曾获/过期」",
                "little_giant": "含「专精特新中小企业」且不含「小巨人」",
                "little_giant_pro": "含「专精特新小巨人企业」",
                "sme": "代理：含「科技型中小企业」（库内无「中小微」标签）",
                "foreign": "代理：org_type 含外商/外资/中外合资/中外合作/港澳台",
                "listed": "代理：有股票财务记录，或 org_type 含「上市」",
            },
        },
        "probes_negative": base["negative_evidence"],
        "result": {
            "nation_cells": sorted(
                [r for r in rows if r["region_kind"] == "nation"],
                key=lambda x: (x["chain_code"], -x["ent_count"])),
            "chain_tag_matrix": [
                {"chain_code": ch, "chain_name": cn.get(ch),
                 "chain_firm_n": chain_firm[ch],
                 "tag_union_firm_n": union_by_chain.get(ch, 0),
                 "tag_union_pct": K.pct(union_by_chain.get(ch, 0), chain_firm[ch]),
                 **{t: nation.get((ch, t), 0) for t in K.QUAL_CODES}}
                for ch in sorted(chain_firm)
            ],
            "top_region_cells": sorted(
                [r for r in rows if r["region_kind"] in ("city", "area")],
                key=lambda x: -x["ent_count"])[:12],
            "top_scope_cells": sorted(
                [r for r in rows if r["region_kind"] == "scope"],
                key=lambda x: -x["ent_count"])[:6],
        },
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": (
                "资质维与区域维都能落格：dwd_org_tech_tag 202,424 行、32,322 家、55 类，"
                "代理名单内 2,981 家有至少一类资质；区域由 dwd_dim_admin_area 换算，"
                "实出 1,560 个非空格、72 个全国格。但三处缺口使其不能判「完全转换支持」："
                "①六类里只有 3 类是直取（高企/专精特新/小巨人），sme 用「科技型中小企业」代理、"
                "foreign 与 listed 只能从 org_type 字样代理，库内无 tag_dict；"
                "②重点名单不存在（280 表零命中），2,981 家是专利阈值代理名单的子集；"
                "③区域维退化为单省切片——代理名单 4,561 家全在广东省 4 市，"
                "复合区域只能点亮大湾区，长三角与京津冀点亮 0 家。三条都不是公式问题，"
                "是依赖数据问题，按定义判部分支持。"
            ),
            "criteria": {
                "tag_table_ready": True,
                "six_tag_codes_in_db": False,
                "sme_is_proxy": True,
                "foreign_listed_are_proxy": True,
                "roster_table_exists": False,
                "region_id_column_exists": False,
                "scope_dim_exists": False,
                "region_coverage_single_province": True,
            },
        },
        **K.base_years_block(),
    }
    K.dump(OUT, payload)


if __name__ == "__main__":
    main()

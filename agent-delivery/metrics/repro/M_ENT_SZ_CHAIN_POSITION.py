#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M_ENT_SZ_CHAIN_POSITION｜链中角色（深圳企业上/中/下游）

零 DB：只读
  code/_snapshots21/keypano_base_20261023.json       企业级链/一级环节/分游（4,561 家名录）
  code/_snapshots21/chain_stage_leaf_20261021.json   链 × 城市 × 叶码 的企业计数（全量上链）
  code/_snapshots21/chain_firm_index_20261023.json   12 链目录与一级环节 → 链的归属
  code/_probe_blocked_f2_20261023.json               阻塞表负证据

口径（P17：链树一级环节 → 上/中/下游是自建映射，必须显式引用）：
  - 游 = `stage_map[一级环节码]`，一级环节 = 9 位 INB 码；映射 41 个一级环节 → up/mid/down。
  - 主口径（去重企业级）：名录 4,561 家中深圳 2,590 家，逐家按 `chain_stages` 取游集合；
    一家跨多游则各游都计（与 calc-logic「一企多个叶子、跨游：各游都计」一致）。
  - 旁证口径（全量上链、叶码计数）：深圳 12 个 chain × city 单元共 133,012 个「叶码—企业」计数，
    因同一企业在一链下可打多叶，计数相对企业数膨胀 1.4316 倍，只用于判断结构排序，
    不得当企业数引用。
  - 对不上一级环节的企业（深圳 104 家）进 `unlabeled`，不猜游。

复现：cd code && python3 M_ENT_SZ_CHAIN_POSITION.py
"""
from __future__ import annotations

import json
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_ENT_SZ_CHAIN_POSITION_out.json")
KP = os.path.join(SNAP, "keypano_base_20261023.json")
LEAF = os.path.join(SNAP, "chain_stage_leaf_20261021.json")
IDX = os.path.join(SNAP, "chain_firm_index_20261023.json")
PROBE = os.path.join(HERE, "_probe_blocked_f2_20261023.json")

ID = "M_ENT_SZ_CHAIN_POSITION"
CITIES = ("深圳市", "广州市", "东莞市", "惠州市")


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    kp = load(KP)
    leaf = load(LEAF)
    idx = load(IDX)
    stage_map = kp["stage_map"]
    chain_name = idx["chain_name"]
    l1_chain = idx["l1_chain"]
    l1_name = idx["l1_name"]

    firms = kp["firms"]

    # ---------- 映射完整性 ----------
    l1_all = sorted(l1_chain)
    mapped = [k for k in l1_all if k in stage_map]
    stage_of_l1 = {k: stage_map[k]["stage"] for k in mapped}
    stage_cnt = Counter(stage_of_l1.values())

    chain_stage_l1 = defaultdict(lambda: defaultdict(list))
    for k in mapped:
        chain_stage_l1[l1_chain[k]][stage_of_l1[k]].append(k)

    chains_no_down = sorted([c for c in chain_name if "down" not in chain_stage_l1[c]])
    chains_no_up = sorted([c for c in chain_name if "up" not in chain_stage_l1[c]])
    chains_no_mid = sorted([c for c in chain_name if "mid" not in chain_stage_l1[c]])

    # ---------- 主口径：名录企业级 ----------
    def stage_row(city):
        sub = [f for f in firms if f.get("city") == city]
        onchain = [f for f in sub if f.get("chains")]
        with_l1 = [f for f in onchain if f.get("l1s")]
        per = Counter()
        multi = 0
        pair_sum = 0
        for f in with_l1:
            st = set()
            for ch, ss in (f.get("chain_stages") or {}).items():
                for s in (ss if isinstance(ss, list) else [ss]):
                    st.add(s)
            if len(st) > 1:
                multi += 1
            for s in st:
                per[s] += 1
            pair_sum += sum(len(v) for v in (f.get("chain_stages") or {}).values())
        return {
            "city": city,
            "roster_n": len(sub),
            "on_chain_n": len(onchain),
            "with_l1_n": len(with_l1),
            "unlabeled_n": len(onchain) - len(with_l1),
            "not_on_chain_n": len(sub) - len(onchain),
            "upstream_n": per.get("up", 0),
            "midstream_n": per.get("mid", 0),
            "downstream_n": per.get("down", 0),
            "multi_stage_n": multi,
            "stage_assignment_sum": sum(per.values()),
            "firm_chain_pairs": pair_sum,
        }

    city_rows = [stage_row(c) for c in CITIES]
    sz = city_rows[0]

    # 分链 × 游（深圳）
    per_chain = {}
    for f in firms:
        if f.get("city") != "深圳市":
            continue
        for ch, ss in (f.get("chain_stages") or {}).items():
            d = per_chain.setdefault(ch, Counter())
            for s in (ss if isinstance(ss, list) else [ss]):
                d[s] += 1
    chain_rows = []
    for ch in sorted(per_chain, key=lambda c: -sum(per_chain[c].values())):
        c = per_chain[ch]
        chain_rows.append({
            "chain": ch,
            "chain_name": chain_name.get(ch),
            "upstream_n": c.get("up", 0),
            "midstream_n": c.get("mid", 0),
            "downstream_n": c.get("down", 0),
            "firm_chain_pairs": sum(c.values()),
            "catalog_has_down": "down" in chain_stage_l1[ch],
        })

    # ---------- 旁证口径：全量上链叶码计数 ----------
    cells = [k for k in leaf["cell_leaf_firm_counts"] if k.endswith("|深圳市")]
    tag_total = 0
    leaf_stage = Counter()
    leaf_chain_stage = defaultdict(Counter)
    unmapped_tag = Counter()
    cross_chain_tag = 0
    for cell in cells:
        ch = cell.split("|")[0]
        for lcode, n in leaf["cell_leaf_firm_counts"][cell].items():
            tag_total += n
            l1 = lcode[:9]
            st = stage_of_l1.get(l1)
            if st is None:
                unmapped_tag[l1] += n
                continue
            # 归链用「一级环节所属链」（与名录口径 chain_stages 一致），
            # 不用该行 industry_code 的链——叶码可挂在别的链的一级环节下。
            owner = l1_chain.get(l1) or ch
            if owner != ch:
                cross_chain_tag += n
            leaf_stage[st] += n
            leaf_chain_stage[owner][st] += n
    firm_total_cells = sum(leaf["cell_firm_counts"][k] for k in cells)

    # ---------- 负证据 ----------
    probe = load(PROBE)
    blocked = [
        {"table": r["table"],
         "gkx_exists": r["gkx_information_schema"]["exists"],
         "gkx_hits": r["gkx_information_schema"]["hits"],
         "live_shell_rows": r["live_where"].get("live_shell_rows"),
         "live_demo_row_class": ("全量装载" if (r["live_where"].get("rows") or 0) >= 10000 else "样例级"),
         "verdict": r["live_where"].get("verdict")}
        for r in probe.get("blocked", [])
        if r["table"] in ("enterprise_industry_chain", "industry_chain_node")
    ]

    out = {
        "metric": ID,
        "metric_name": "链中角色",
        "support_judgment": "部分支持",
        "verdict_kind": "partial_with_gaps",
        "generated_at": "2026-10-23T05:10:00+08:00",
        "sources": {
            "db": "gkx",
            "host": "183.240.141.251:3318",
            "user": "gkx_reader_zp",
            "mode": "read-only",
            "tables": [
                "gkx.dwd_org_industry_tags",
                "gkx.dwd_org_base_info",
            ],
            "snapshots": [
                "code/_snapshots21/keypano_base_20261023.json",
                "code/_snapshots21/chain_stage_leaf_20261021.json",
                "code/_snapshots21/chain_firm_index_20261023.json",
                "code/_probe_blocked_f2_20261023.json",
            ],
            "demo_used": False,
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面指标（链标签快照 2026-10-21/23），无年度基期；链标签表无打标时间列，不能按年切片。",
        "mapping": {
            "rule_ref": "PENDING_RULINGS_20261023.md P17：链树一级环节 → 上/中/下游由本工程拟定，需甲方确认",
            "l1_total": len(l1_all),
            "l1_mapped": len(mapped),
            "l1_unmapped": len(l1_all) - len(mapped),
            "stage_l1_count": dict(stage_cnt),
            "chains": len(chain_name),
            "chains_without_down": [chain_name[c] for c in chains_no_down],
            "chains_without_up": [chain_name[c] for c in chains_no_up],
            "chains_without_mid": [chain_name[c] for c in chains_no_mid],
            "down_l1_absent_n": 12 - stage_cnt.get("down", 0) and len(chains_no_down),
            "stage_map": {k: v["stage"] for k, v in stage_map.items()},
            "l1_name": {k: l1_name.get(k) for k in mapped},
        },
        "universe": {
            "roster_n": len(firms),
            "roster_source": "star_profile_20261022.json（授权≥50 专利阈值代理，P15）",
            "sz_roster_n": sz["roster_n"],
            "sz_on_chain_n": sz["on_chain_n"],
            "sz_with_l1_n": sz["with_l1_n"],
            "sz_unlabeled_n": sz["unlabeled_n"],
            "sz_not_on_chain_n": sz["not_on_chain_n"],
            "full_chain_sz_firms": 16875,
            "full_chain_sz_source": "chain_linked_type_20261023.json：dwd_org_industry_tags JOIN dwd_org_base_info，深圳 16,875 家上链企业（全量、去重）",
        },
        "city_slices": city_rows,
        "chain_rows_sz": chain_rows,
        "tag_level_sidecar": {
            "sz_cells": len(cells),
            "tag_hits_total": tag_total,
            "firm_count_cells_total": firm_total_cells,
            "inflation_ratio": round(tag_total / firm_total_cells, 4),
            "stage_tag_hits": {k: leaf_stage.get(k, 0) for k in ("up", "mid", "down")},
            "stage_tag_sum": sum(leaf_stage.get(k, 0) for k in ("up", "mid", "down")),
            "unmapped_tag_hits": sum(unmapped_tag.values()),
            "cross_chain_tag_hits": cross_chain_tag,
            "cross_chain_note": "cross_chain_tag_hits = 叶码所属一级环节不在该行 industry_code 链下、而挂在另一条链的一级环节上的计数；归链统一取一级环节所属链，与名录口径一致。",
            "per_chain": {chain_name[c]: dict(leaf_chain_stage[c]) for c in leaf_chain_stage},
            "note": "叶码级计数，一企多叶会重复计；只用于判断链内结构排序，不得当企业数。",
        },
        "derived": {
            "on_chain_share_pct": {
                "value": round(sz["on_chain_n"] / sz["roster_n"] * 100, 4),
                "numerator": sz["on_chain_n"],
                "denominator": sz["roster_n"],
                "denominator_note": "分子=深圳名录内上链企业数 universe.sz_on_chain_n，分母=深圳名录企业数 city_slices[深圳市].roster_n",
            },
            "with_l1_share_pct": {
                "value": round(sz["with_l1_n"] / sz["on_chain_n"] * 100, 4),
                "numerator": sz["with_l1_n"],
                "denominator": sz["on_chain_n"],
                "denominator_note": "分子=深圳上链且能对上一级环节的企业数 universe.sz_with_l1_n，分母=深圳上链企业数 universe.sz_on_chain_n",
            },
            "unlabeled_share_pct": {
                "value": round(sz["unlabeled_n"] / sz["on_chain_n"] * 100, 4),
                "numerator": sz["unlabeled_n"],
                "denominator": sz["on_chain_n"],
                "denominator_note": "分子=有链码但一级环节为空的企业数 universe.sz_unlabeled_n，分母=深圳上链企业数 universe.sz_on_chain_n",
            },
            "upstream_share_pct": {
                "value": round(sz["upstream_n"] / sz["with_l1_n"] * 100, 4),
                "numerator": sz["upstream_n"],
                "denominator": sz["with_l1_n"],
                "denominator_note": "分子=分到上游的深圳企业数 city_slices[深圳市].upstream_n，分母=可判游企业数 universe.sz_with_l1_n（一企跨游各游都计，三游之和大于分母）",
            },
            "midstream_share_pct": {
                "value": round(sz["midstream_n"] / sz["with_l1_n"] * 100, 4),
                "numerator": sz["midstream_n"],
                "denominator": sz["with_l1_n"],
                "denominator_note": "分子=分到中游的深圳企业数 city_slices[深圳市].midstream_n，分母=可判游企业数 universe.sz_with_l1_n",
            },
            "downstream_share_pct": {
                "value": round(sz["downstream_n"] / sz["with_l1_n"] * 100, 4),
                "numerator": sz["downstream_n"],
                "denominator": sz["with_l1_n"],
                "denominator_note": "分子=分到下游的深圳企业数 city_slices[深圳市].downstream_n，分母=可判游企业数 universe.sz_with_l1_n",
            },
            "multi_stage_share_pct": {
                "value": round(sz["multi_stage_n"] / sz["with_l1_n"] * 100, 4),
                "numerator": sz["multi_stage_n"],
                "denominator": sz["with_l1_n"],
                "denominator_note": "分子=跨 ≥2 个游的深圳企业数 city_slices[深圳市].multi_stage_n，分母=可判游企业数 universe.sz_with_l1_n",
            },
            "stage_assignment_per_firm": {
                "value": round(sz["stage_assignment_sum"] / sz["with_l1_n"], 4),
                "numerator": sz["stage_assignment_sum"],
                "denominator": sz["with_l1_n"],
                "denominator_note": "分子=游归属计数之和 city_slices[深圳市].stage_assignment_sum，分母=可判游企业数 universe.sz_with_l1_n（比值即每企平均落几个游）",
            },
            "sz_roster_cover_of_full_chain_pct": {
                "value": round(sz["roster_n"] / 16875 * 100, 4),
                "numerator": sz["roster_n"],
                "denominator": 16875,
                "denominator_note": "分子=深圳名录企业数 city_slices[深圳市].roster_n，分母=全量深圳上链企业数 universe.full_chain_sz_firms（16,875，chain_linked_type 快照）",
            },
            "sz_with_l1_cover_of_full_chain_pct": {
                "value": round(sz["with_l1_n"] / 16875 * 100, 4),
                "numerator": sz["with_l1_n"],
                "denominator": 16875,
                "denominator_note": "分子=可判游深圳企业数 universe.sz_with_l1_n，分母=全量深圳上链企业数 universe.full_chain_sz_firms",
            },
            "tag_inflation_ratio": {
                "value": round(tag_total / firm_total_cells, 4),
                "numerator": tag_total,
                "denominator": firm_total_cells,
                "denominator_note": "分子=深圳叶码级计数合计 tag_level_sidecar.tag_hits_total，分母=同一批单元的去重企业数合计 tag_level_sidecar.firm_count_cells_total",
            },
            "down_catalog_gap_share_pct": {
                "value": round(len(chains_no_down) / len(chain_name) * 100, 4),
                "numerator": len(chains_no_down),
                "denominator": len(chain_name),
                "denominator_note": "分子=缺下游一级环节的链数 mapping.chains_without_down 的条数，分母=链目录总数 mapping.chains（12）",
            },
            "cross_chain_tag_share_pct": {
                "value": round(cross_chain_tag / tag_total * 100, 4),
                "numerator": cross_chain_tag,
                "denominator": tag_total,
                "denominator_note": "分子=叶码所属一级环节挂在另一条链上的计数 tag_level_sidecar.cross_chain_tag_hits，分母=深圳叶码级计数合计 tag_level_sidecar.tag_hits_total",
            },
            "no_down_chain_pairs": {
                "value": sum(r["firm_chain_pairs"] for r in chain_rows if not r["catalog_has_down"]),
                "numerator": sum(r["firm_chain_pairs"] for r in chain_rows if not r["catalog_has_down"]),
                "denominator": None,
                "denominator_note": "无分母，为计数：mapping.chains_without_down 四条链在 chain_rows_sz 中 firm_chain_pairs 之和",
            },
            "no_down_chain_pairs_share_pct": {
                "value": round(sum(r["firm_chain_pairs"] for r in chain_rows if not r["catalog_has_down"])
                               / sum(r["firm_chain_pairs"] for r in chain_rows) * 100, 4),
                "numerator": sum(r["firm_chain_pairs"] for r in chain_rows if not r["catalog_has_down"]),
                "denominator": sum(r["firm_chain_pairs"] for r in chain_rows),
                "denominator_note": "分子=缺下游链的「企业—链」对数之和（chain_rows_sz 中 catalog_has_down=false 的行），分母=深圳全部「企业—链」对数之和",
            },
            "sz_chain_top1_share_pct": {
                "value": round(chain_rows[0]["firm_chain_pairs"]
                               / sum(r["firm_chain_pairs"] for r in chain_rows) * 100, 4),
                "numerator": chain_rows[0]["firm_chain_pairs"],
                "denominator": sum(r["firm_chain_pairs"] for r in chain_rows),
                "denominator_note": "分子=深圳最大链的「企业—链」对数 chain_rows_sz[0].firm_chain_pairs，分母=深圳全部「企业—链」对数之和",
            },
        },
        "absence_probe": {
            "file": "code/_probe_blocked_f2_20261023.json",
            "blocked": blocked,
        },
        "rejected_dimensions": [
            {
                "dimension": "链主识别",
                "reason": "calc-logic 明写「链主不进本 JSON」；gkx 无 enterprise_industry_chain（0 表），链主认定无字段承载；industry_chain_node 亦不存在",
                "alternative": "只出上/中/下游",
                "difference": "链中角色缺「链主 / 核心配套 / 一般参与」这一层，无法回答「谁在主导这条链」",
            },
            {
                "dimension": "官方 position 列直读",
                "reason": "project 侧 chain_node.position 只在项目 DWD（现网 8 链 CH001—CH008），与 gkx 的 12 链 INB 码目录对不上；gkx 侧 dwd_industry_chain_info 12 条 INB 记录无 position 列",
                "alternative": "本工程自建 41 个一级环节 → 上/中/下游映射（P17）",
                "difference": "自建映射不是官方认定；换一份映射，三游家数与占比同时变",
            },
            {
                "dimension": "全量深圳上链企业分游（去重企业级）",
                "reason": "全量 16,875 家只有叶码级计数（一企多叶膨胀 1.4316 倍），没有企业级去重游归属；企业级去重只在 4,561 家专利阈值名录里有",
                "alternative": "名录口径出企业级三游分布 + 叶码口径出结构排序",
                "difference": "企业级分布只覆盖深圳上链企业的少数（名录占全量 15.35%），不能代表全量；两套口径不可相加",
            },
        ],
        "gaps": [
            "企业级三游分布只建在 4,561 家专利阈值名录上（P15 代理），不是全量上链企业",
            "4 条链（集成电路、传感器、智能终端、生物医药）在链树里缺下游一级环节；这是目录缺口，不是企业缺口，补企业无用（P17）",
            "104 家深圳上链企业有一级环节为空，进 unlabeled，不猜游",
            "「一企跨游各游都计」使三游家数之和（2,488）大于可判游企业数（1,367），占比不能相加为 100%",
            "叶码口径相对企业数膨胀 1.4316 倍，只能比结构、不能报家数",
        ],
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"l1_mapped={len(mapped)}/{len(l1_all)} chains_no_down={len(chains_no_down)} "
          f"sz_roster={sz['roster_n']} on_chain={sz['on_chain_n']} with_l1={sz['with_l1_n']} "
          f"up/mid/down={sz['upstream_n']}/{sz['midstream_n']}/{sz['downstream_n']} "
          f"tag_inflation={tag_total / firm_total_cells:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_GBA_PATENT_GRANT · 专利授权量（湾区 11 城）

口径（registry xlsx 53）：期内授权专利件数，含发明/实用新型/外观，按专利号去重；
专利权人地址或第一专利权人在湾区 11 城；窗口自然年。

取数（**零专利 SQL**，全部读全量扫描缓存）
-------------------------------------------
- 2024 年申请人级：`_snapshots21/patent2024_scan_20261021.json.by_name`
  → `[2024 去重 pn, 授权行数, 授权去重 pn]`（2024 全表 85 块扫完，74,923 名申请人）。
- 全窗（2021–2026）申请人级：`_snapshots21/star_applicant_agg_gkx.json.agg`
  → `[件数, 授权数]`（169,226 名，件数合计 2,939,895 与表行数逐位相等）。
- 城市归属：企业底册缓存 `base_20261021.json` 的 `name → city`（本地字典 join）；
  47 个重名按 1/k 计权（DATA_FACTS §3.5）。
- 7 个无底册城只给「名称 token 下界」，单列且不参与排名。

为什么不是「城市 × 年 × 件型」四维表
------------------------------------
`dwd_patent` 无 `apdt_year` / `first_applicant_name` 索引，任何按年聚合都是全表扫，
服务端约 2,400 秒断连（已复现 6 次）。现有缓存里**没有**「城市 × 年 × 件型」这一维，
本脚本据实降级为「2024 单年精确 + 全窗合计」，并在 out.json 写明缺口。
补这一维需要一次新的全表分页扫描（30 万行/页，约 1,800–2,000 秒），已登记为缺口。

输出：code/M_INNOV_GBA_PATENT_GRANT_out.json
"""
from __future__ import annotations

import json
import sys
import time
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _gba_gkx_common as C  # noqa: E402

T0 = time.time()
MID = "M_INNOV_GBA_PATENT_GRANT"

base = C.load_base()
name_city, _org_city, dup = C.name_city_maps(base)
p24 = C.load_patent2024()
star = C.load_star_agg()
scan = C.load_patent_scan()


def weight(name: str, city: str) -> float:
    if name in dup:
        cnt = dup[name]
        tot = sum(cnt.values())
        return cnt.get(city, 0) / tot
    return 1.0


# ---- 2024 单年：申请人级 → 城市级 ----
agg24 = defaultdict(lambda: {"apply_pn": 0.0, "grant_pn": 0.0, "grant_rows": 0.0, "orgs": 0})
unmatched_2024 = 0
for nm, (pn24, grow, gded) in p24["by_name"].items():
    c = name_city.get(nm)
    if not c:
        unmatched_2024 += int(pn24)
        continue
    w = weight(nm, c)
    a = agg24[c]
    a["apply_pn"] += pn24 * w
    a["grant_pn"] += gded * w
    a["grant_rows"] += grow * w
    a["orgs"] += 1

# ---- 全窗（2021–2026）：申请人级 → 城市级 ----
agg_all = defaultdict(lambda: {"patents": 0.0, "grants": 0.0, "orgs": 0})
for nm, (tot, gr) in star.items():
    c = name_city.get(nm)
    if not c:
        continue
    w = weight(nm, c)
    a = agg_all[c]
    a["patents"] += tot * w
    a["grants"] += gr * w
    a["orgs"] += 1

# ---- 名称 token 下界（仅无底册 7 城）----
TOKENS = {"珠海市": ["珠海"], "佛山市": ["佛山"], "中山市": ["中山"],
          "江门市": ["江门"], "肇庆市": ["肇庆"],
          "香港特别行政区": ["香港"], "澳门特别行政区": ["澳门"]}
# 已知误命中：中山大学/中山医院在广州、香港中文大学(深圳)在深圳 —— 下界里点名剔除
EXCLUDE_SUB = {"中山市": ["中山大学", "中山医科大学", "中山市华侨中学"]}
token_lower = {}
for city in C.GBA11:
    if city in C.COVERED:
        continue
    toks = TOKENS.get(city, [])
    pat = gr = 0
    ex = EXCLUDE_SUB.get(city, [])
    for nm, (tot, g) in star.items():
        if any(e in nm for e in ex):
            continue
        if any(t in nm for t in toks):
            pat += tot
            gr += g
    token_lower[city] = {"patents_all_window": pat, "grants_all_window": gr,
                         "path": "name_token_lower_bound", "comparable": False}

# ---- 城市表 ----
rows = []
for city in C.GBA11:
    a24 = agg24.get(city)
    aa = agg_all.get(city)
    if city in C.COVERED:
        apply24 = int(round(a24["apply_pn"])) if a24 else 0
        grant24 = int(round(a24["grant_pn"])) if a24 else 0
        rows.append({
            "city": city,
            "comparable": True,
            "attribution_path": "exact_name",
            "orgs_matched": int(a24["orgs"]) if a24 else 0,
            "apply_2024": apply24,
            "grant_2024": grant24,
            "grant_rate_2024": C.pct(grant24, apply24),
            "grant_rows_2024": int(round(a24["grant_rows"])) if a24 else 0,
            "patents_all_window_2021_2026": int(round(aa["patents"])) if aa else 0,
            "grants_all_window_2021_2026": int(round(aa["grants"])) if aa else 0,
            "grant_share_all_window": C.pct(aa["grants"], aa["patents"]) if aa and aa["patents"] else None,
        })
    else:
        tl = token_lower.get(city, {})
        rows.append({
            "city": city,
            "comparable": False,
            "attribution_path": "token_fallback_lower_bound",
            "orgs_matched": 0,
            "apply_2024": None,
            "grant_2024": None,
            "grant_rate_2024": None,
            "patents_all_window_2021_2026": tl.get("patents_all_window"),
            "grants_all_window_2021_2026": tl.get("grants_all_window"),
            "grant_share_all_window": C.pct(tl.get("grants_all_window", 0),
                                            tl.get("patents_all_window", 0) or 0),
            "lower_bound_note": "名称 token 下界：会漏掉无地名前缀的巨头，也会误命中同名异地机构，"
                                "只作「非零」证明，不参与排名与合计。",
        })

covered = [r for r in rows if r["comparable"]]
tot_apply24 = sum(r["apply_2024"] for r in covered)
tot_grant24 = sum(r["grant_2024"] for r in covered)
for r in covered:
    r["grant_share_of_comparable_2024"] = C.pct(r["grant_2024"], tot_grant24)

corpus_total = sum(t for t, _g in star.values())
corpus_grant = sum(g for _t, g in star.values())
grant_2024_universe = sum(v[2] for v in p24["by_name"].values())
apply_2024_universe = sum(v[0] for v in p24["by_name"].values())

# 城市 × 年（全部件型）供交叉核对 —— 来自同一份全表扫描缓存
cy = C.patent_city_year(scan)
year_by_city = {c: {str(y): cy.get((c, y), 0) for y in range(2021, 2027)} for c in C.COVERED}

out = {
    "metric_id": MID,
    "metric_name": "专利授权量",
    "domain": "INNOV / 湾区创新监测（DS-05）",
    "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    "window": {
        "primary": "2024 单年（缓存中唯一能做「城 × 件型」的完整年）",
        "secondary": "2021–2026 全窗合计（授权列直接取申请人聚合的授权数）",
        "note": "gkx.dwd_patent 的 apdt_year 只覆盖 2021–2026（2017–2020 零行）；2026 为残年。",
    },
    "unit": "件",
    "formula": "grant(city,y) = Σ_applicant 授权去重 pn，applicant_city=city；城市由第一申请人名对齐企业底册",
    "definition_note": "含发明/实用新型/外观；按 pn 去重；A 类（发明申请公开）不计授权。"
                       "「同申请年内出现授权记录的比例」不等于授权率（授权通常滞后于申请年）。",
    "rows": rows,
    "totals": {
        "comparable_cities": len(covered),
        "gba11_cities": 11,
        "apply_2024_comparable": tot_apply24,
        "grant_2024_comparable": tot_grant24,
        "grant_rate_2024_comparable": C.pct(tot_grant24, tot_apply24),
        "apply_2024_universe": apply_2024_universe,
        "grant_2024_universe": grant_2024_universe,
        "city_match_share_2024": C.pct(tot_apply24, apply_2024_universe),
        "unmatched_2024_patents": unmatched_2024,
        "corpus_patents_all_window": corpus_total,
        "corpus_grants_all_window": corpus_grant,
        "corpus_grant_share": C.pct(corpus_grant, corpus_total),
        "covered_grant_share_of_corpus": C.pct(tot_grant24, grant_2024_universe),
    },
    "year_by_city_all_kinds": year_by_city,
    "token_lower_bounds": token_lower,
    "probes": {
        "patent_rows": scan["row_total"],
        "patent_scan_done": scan["done"],
        "patent_scan_elapsed_sec": scan["elapsed_sec"],
        "star_agg_names": len(star),
        "star_agg_table_rows": corpus_total,
        "patent2024_names": p24["meta"]["names"],
        "patent2024_complete": p24["meta"]["complete"],
        "base_rows": len(base),
        "dup_names": len(dup),
    },
    "known_traps": [
        "dwd_patent 无「专利权人地址」列（55 列已探），城市只能由第一申请人名对齐企业底册。",
        "底册 99.82% 是深圳都市圈四城：珠海/佛山/中山/江门/肇庆/港澳 org 数 0–1 家，7 城只能给 token 下界。",
        "token 路径会漏计无地名前缀巨头（华为/比亚迪/荣耀），也会误命中同名异地机构（中山大学在广州）。",
        "缓存中没有「城市 × 年 × 件型」四维交叉，本件据实降级为 2024 单年 + 全窗合计。",
        "2024 年 606,468 件中，能对齐底册的 529,394 件（87.3%），余 77,074 件城市未知，不摊分。",
    ],
    "support_judgment": {
        "data_support_level": "部分支持",
        "criteria": {
            "structure": "dwd_patent(pn, kind, apdt_year, first_applicant_name) + 底册(name, city)；结构齐全",
            "volume": f"2024 单年可算 {len(covered)} 城（{tot_grant24:,} 件授权）；7 城仅 token 下界",
            "reproducible": True,
            "discriminative": True,
        },
        "blocking_gaps": [
            "11 城中 7 城无企业底册入集，只能给 token 下界，跨城排名失真。",
            f"2024 年 {unmatched_2024:,} 件（{1 - tot_apply24 / apply_2024_universe:.1%}）第一申请人无法对齐底册。",
            "官方口径含「专利权人地址」，库内无地址列，只退化到第一申请人属地。",
            "缓存缺「城市 × 年 × 件型」四维交叉，年度授权序列只能给全窗合计 + 2024 单年。",
        ],
        "note": "核心读数（4 城 2024 授权 381,952 件）可复现且可官方对表；7 城与年度序列两处缺口使其不得升档。",
    },
    "runtime_sec": round(time.time() - T0, 2),
}

C.write_out(MID, out)
print(f"[{time.time() - T0:.1f}s] comparable={len(covered)} apply24={tot_apply24:,} "
      f"grant24={tot_grant24:,} rate={out['totals']['grant_rate_2024_comparable']}")
for r in covered:
    print(f"  {r['city']:<6} orgs={r['orgs_matched']:>6} apply24={r['apply_2024']:>9,} "
          f"grant24={r['grant_2024']:>9,} rate={r['grant_rate_2024']}")
print("  token lower bounds:", {c: v["grants_all_window"] for c, v in token_lower.items()})

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_KEYD_COMPETITIVENESS · 区域科技创新竞争力水平（0—100，gkx 口径重建件，零 SQL）

口径（原样沿用旧稿的三维等权 + 四城 min-max）：
  D1 创新产出 = 0.5·minmax(专利件数) + 0.5·minmax(论文篇数)
  D2 创新主体 = 0.4·minmax(企业底册家数) + 0.4·minmax(高新技术企业家数) + 0.2·minmax(科研机构家数)
  D3 政策供给 = minmax(市级政策件数)
  综合分 = 100 × (D1 + D2 + D3) / 3
  敏感性 = 去政策维重算、0.4/0.3/0.3 加权重算

「区域」= 深圳都市圈 4 市（深圳/广州/东莞/惠州）。底册 99.82% 在广东，省外样本 <0.2%，
故本指标只作省内/都市圈比较，不作全国名次解释。

【本件自定义、待甲方确认】
  三维等权、D2 内部的 0.4/0.4/0.2、min-max 归一化方式，需求均未给；属旧稿设定。
  min-max 在 4 个样本上会把「第一名=100、末名=0」，城市间的绝对差距被抹平，
  因此本件同时给出原始值和排名，不把 0/100 读成「没有能力 / 能力满分」。

与旧稿的差异（数据源换血，公式不动）：
  旧稿 import `_keyd_common.load_panel()`（ODS/DWD 白名单，实为演示库连接器）；
  本件零 SQL、零 helper，只读本目录 gkx 落盘快照。
  年份窗口从 2021—2025 收窄为 2021—2024：四城专利归城只到 2024（2025 未归城），
  论文 2024 年 32,379 篇是 2021—2023 均值的 4.9 倍（源侧批量导入痕迹），故论文维另给「剔除 2024」敏感性。

数据源：
  _snapshots21/gba_patent_20261021.json         四城×年 专利件数
  _snapshots21/papers_city_year_gkx21.json      100,900 篇论文，第一作者单位定主城
  _snapshots21/base_20261021.json               企业底册 189,116 行（城市在第 5 列）
  _snapshots21/gba_hitech_20261021.json         高企标签去重 27,634 家
  _snapshots21/org_family_panel_20261021.json   科研机构 2,074 家
  _snapshots21/gba_policy_20261021.json         政策 20,000 行，市级可归属 51.47%

运行：cd code && python3 M_INNOV_KEYD_COMPETITIVENESS.py
产物：code/M_INNOV_KEYD_COMPETITIVENESS_out.json
"""
from __future__ import annotations

import collections
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")

MID = "M_INNOV_KEYD_COMPETITIVENESS"
CITIES = ["深圳市", "广州市", "东莞市", "惠州市"]
SHORT = {"深圳市": "深圳", "广州市": "广州", "东莞市": "东莞", "惠州市": "惠州"}
YEARS = [2021, 2022, 2023, 2024]


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def minmax(vals):
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return [50.0 for _ in vals]
    return [round((v - lo) / (hi - lo) * 100, 2) for v in vals]


def main():
    pat_src = load("gba_patent_20261021.json")["city_year"]
    pap_src = load("papers_city_year_gkx21.json")["first_city_year"]
    base = load("base_20261021.json")
    hitech = load("gba_hitech_20261021.json")
    panel = load("org_family_panel_20261021.json")
    policy = load("gba_policy_20261021.json")
    policy_rows = load("policy_base_20261021.json")
    # 市级可归属 = city 既非 'NULL' 也非空（§3.7：'NULL' 是占位串，不是空值）
    city_attr_all = sum(1 for r in policy_rows
                        if (r.get("city") or "").strip() not in ("", "NULL"))
    rd = load("gba_rd_20261021.json")

    pat = {c: sum(int(pat_src.get(c, {}).get(str(y), 0)) for y in YEARS) for c in CITIES}
    pap = {c: sum(int(pap_src.get(f"{c}|{y}", 0)) for y in YEARS) for c in CITIES}
    pap_ex24 = {c: sum(int(pap_src.get(f"{c}|{y}", 0)) for y in (2021, 2022, 2023)) for c in CITIES}
    org = collections.Counter(r[4] for r in base)
    org = {c: org.get(c, 0) for c in CITIES}
    heis = {c: int(hitech["by_city"].get(c, 0)) for c in CITIES}
    inst = collections.Counter(i["city"] for i in panel["institutions"])
    inst = {c: inst.get(c, 0) for c in CITIES}
    pol = {c: int(policy["by_city"].get(c, 0)) for c in CITIES}

    def mm(d):
        return dict(zip(CITIES, minmax([d[c] for c in CITIES])))

    z_pat, z_pap, z_org, z_heis, z_inst, z_pol = mm(pat), mm(pap), mm(org), mm(heis), mm(inst), mm(pol)
    z_pap_ex = mm(pap_ex24)

    d1 = {c: round(0.5 * z_pat[c] + 0.5 * z_pap[c], 2) for c in CITIES}
    d2 = {c: round(0.4 * z_org[c] + 0.4 * z_heis[c] + 0.2 * z_inst[c], 2) for c in CITIES}
    d3 = {c: round(z_pol[c], 2) for c in CITIES}
    comp = {c: round((d1[c] + d2[c] + d3[c]) / 3, 2) for c in CITIES}
    comp_no_pol = {c: round((d1[c] + d2[c]) / 2, 2) for c in CITIES}
    comp_w = {c: round(0.4 * d1[c] + 0.3 * d2[c] + 0.3 * d3[c], 2) for c in CITIES}
    d1_ex24 = {c: round(0.5 * z_pat[c] + 0.5 * z_pap_ex[c], 2) for c in CITIES}
    comp_ex24 = {c: round((d1_ex24[c] + d2[c] + d3[c]) / 3, 2) for c in CITIES}

    rank = {SHORT[c]: i + 1 for i, c in enumerate(sorted(CITIES, key=lambda x: -comp[x]))}
    rank_no_pol = {SHORT[c]: i + 1 for i, c in enumerate(sorted(CITIES, key=lambda x: -comp_no_pol[x]))}
    rank_ex24 = {SHORT[c]: i + 1 for i, c in enumerate(sorted(CITIES, key=lambda x: -comp_ex24[x]))}

    pol_city_rows = sum(pol.values())
    paper_total = sum(pap.values())
    payload = {
        "metric_id": MID,
        "metric_name": "区域科技创新竞争力水平",
        "domain": "TOPIC-INNOV / 区域创新比较",
        "formula_owner": "仿王惠（旧稿口径）",
        "support_judgment": "部分支持",
        "support_reason": (
            f"D1/D2 在四城上可算：专利 {sum(pat.values()):,} 件（2021—2024 归城）、论文 {paper_total:,} 篇、"
            f"企业底册 189,116 家、高企 27,634 家、科研机构 2,074 家；"
            f"但 D3 政策维量不可用：全表市级可归属 {city_attr_all:,}/20,000（{city_attr_all/20000:.2%}），"
            f"落到四城的仅 {pol_city_rows:,} 条（{pol_city_rows/20000:.2%}），东莞 {pol['东莞市']} 件、"
            f"惠州 {pol['惠州市']} 件，是源侧覆盖不均而不是供给真实差异；"
            "论文语料 100,900 篇中广州占 60.3%、且 2024 年单年 32,379 篇是前三年的 4.9 倍（导入痕迹），"
            "论文维只能作语料内相对。三档里两档可算、一档结构可用量不可用，判部分支持。"
        ),
        "generated_at": "2026-10-22",
        "main_db": "gkx @ 183.240.141.251:3318（gkx_reader_zp，只读）",
        "sql_count": 0,
        "sources": [
            "code/_snapshots21/gba_patent_20261021.json（面板 2,939,895 行 × 底册归城）",
            "code/_snapshots21/papers_city_year_gkx21.json（dwd_zh_paper 100,900 行）",
            "code/_snapshots21/base_20261021.json（dwd_org_base_info 189,116 行）",
            "code/_snapshots21/gba_hitech_20261021.json（高企标签 202,424 行 → 27,634 家）",
            "code/_snapshots21/org_family_panel_20261021.json（2,074 家）",
            "code/_snapshots21/gba_policy_20261021.json（20,000 行）",
        ],
        "base_years_used": YEARS,
        "base_years_missing": [2017, 2018, 2019, 2020, 2025],
        "base_years_note": (
            "专利归城只到 2024（gba_patent.city_year 无 2025）；论文 2025 有 6,548 篇但 2026 仅 2,989 篇，"
            "为避免把「导入批次」当增长，窗口统一取 2021—2024；2017—2020 专利零行，未补 0、未外推。"
            "论文 2024 年异常单列敏感性（剔除后重算 D1/综合分与排名）。"
        ),
        "definition_note": (
            "本件自定义、待甲方确认：三维等权、D2 内部 0.4/0.4/0.2、min-max 归一，均无官方出处；"
            "4 个样本的 min-max 必然产生 0 与 100 两个端点，端点不代表「零能力/满分」。"
        ),
        "scope": {"regions": CITIES, "years": YEARS,
                  "caveat": "底册 99.82% 在广东，省外 342 家；本指标不作全国名次解释"},
        "inputs": {
            "patents_2021_2024": pat, "papers_2021_2024": pap,
            "papers_2021_2023_ex2024": pap_ex24,
            "orgs": org, "high_tech_orgs": heis, "research_institutes": inst,
            "city_policies": pol,
            "rd_expense_yi_2024": {SHORT[c]: rd["by_city_year_yi"].get(c, {}).get("2024") for c in CITIES},
        },
        "normalized": {"patent": z_pat, "paper": z_pap, "paper_ex2024": z_pap_ex, "org": z_org,
                       "heis": z_heis, "institute": z_inst, "policy": z_pol},
        "dims": {"D1_output": d1, "D2_actor": d2, "D3_policy": d3},
        "composite": {SHORT[c]: comp[c] for c in CITIES},
        "rank": rank,
        "sensitivity": {
            "composite_without_policy": {SHORT[c]: comp_no_pol[c] for c in CITIES},
            "rank_without_policy": rank_no_pol,
            "composite_weight_403030": {SHORT[c]: comp_w[c] for c in CITIES},
            "rank_changed_without_policy": rank != rank_no_pol,
            "composite_paper_ex2024": {SHORT[c]: comp_ex24[c] for c in CITIES},
            "rank_paper_ex2024": rank_ex24,
            "rank_changed_paper_ex2024": rank != rank_ex24,
        },
        "policy_coverage": {
            "policy_rows": policy["rows"],
            "city_attributed_rows_all": city_attr_all,
            "city_attributed_share_all": round(city_attr_all / policy["rows"], 4),
            "city_attributed_rows_four": pol_city_rows,
            "city_attributed_share_four": round(pol_city_rows / policy["rows"], 4),
            "city_top": dict(sorted(pol.items(), key=lambda kv: -kv[1])),
            "placeholder_rows": policy["placeholder_rows"],
            "note": "东莞 8 件、惠州 0 件是源侧属地缺失，不是真实供给量；政策维不可单独用于城际比较",
        },
        "probes": {
            "patent_rows": 2939895, "org_rows": len(base), "paper_rows": 100900,
            "paper_city_attributed": paper_total,
            "paper_city_fill_share": round(paper_total / 100900, 4),
            "hitech_orgs": hitech["orgs_total"], "institutes": len(panel["institutions"]),
            "rd_rows_cities": rd["orgs_by_city"],
        },
        "gaps": [
            f"政策维量不可用：全表市级可归属 {city_attr_all:,}/20,000，四城仅 {pol_city_rows:,} 条"
            f"（东莞 8、惠州 0），且 9,706 行 province/city 为占位 'NULL'；",
            "论文语料偏置：100,900 篇中广州占 60.28%、深圳 30.57%，与真实产出结构不符（语料以广东高校为主）；",
            "论文 2024 年 32,379 篇为 2021—2023 均值 6,580 篇的 4.92 倍，属导入批次痕迹，已单列敏感性；",
            "专利归城只到 2024，2025 无法进窗口；且语料可归城行 99.95% 是四城，不是全国；",
            "D2 的「企业底册家数」是登记存量，不是活跃企业数或研发主体数；高企标签与底册非同一主键，按名称对齐；",
            "四城 min-max 端点效应：第一名恒 100、末名恒 0，绝对差距被抹平，不宜读成能力刻度。",
        ],
    }

    out = os.path.join(HERE, f"{MID}_out.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)

    print("wrote", os.path.basename(out))
    for c in CITIES:
        print(f"{SHORT[c]} pat={pat[c]:>8,} pap={pap[c]:>6,} org={org[c]:>6,} "
              f"hitech={heis[c]:>6,} inst={inst[c]:>4} pol={pol[c]:>4} "
              f"| D1={d1[c]:>6} D2={d2[c]:>6} D3={d3[c]:>6} comp={comp[c]:>6}")
    print("rank", rank, "no_pol", rank_no_pol, "ex24", rank_ex24)
    print("policy fill", payload["policy_coverage"])


if __name__ == "__main__":
    main()

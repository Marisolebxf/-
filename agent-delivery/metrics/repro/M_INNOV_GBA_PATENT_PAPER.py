#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_GBA_PATENT_PAPER · 专利及论文数量（湾区 11 城）

口径（registry seq 106 相邻项 / DS-05 指标组）：COUNT(专利) + COUNT(论文)，
授权量单列不并入（授权走 M_INNOV_GBA_PATENT_GRANT）；对象 = 申请人 / 第一完成单位
在湾区 11 城；窗口 2021–2024 四个完整自然年。

取数（专利零 SQL、论文单次缓存）
--------------------------------
- 专利侧：`_snapshots21/patent_scan_20261021.pkl` 的 `row_city`（全表 2,939,895 行，
  城市由第一申请人名对齐底册）。全部 kind，**申请口径**。
- 论文侧：`_snapshots21/papers_city_year_gkx21.json`（`_build_papers_city_gkx21.py` 建，
  gkx.dwd_zh_paper 100,900 行一次流式；第一作者单位 → 城市，白名单优先于 token）。

必须披露的三件事
----------------
1. 专利侧 7 城为 0：底册只有深圳/广州/东莞/惠州四城有实体机构（99.82% 在广东）。
2. 论文侧第一作者可归属湾区的仅 24.6%，其余 71,696 篇无湾区城市键，不摊分、不估算。
3. 两语料不同源、不同量级（专利 200 万级 / 论文 2 万级），相加只是「目录口径的并列合计」，
   不可解释为「创新产出当量」；2024 年论文入库 3.2 万篇是批次断点。

输出：code/M_INNOV_GBA_PATENT_PAPER_out.json
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _gba_gkx_common as C  # noqa: E402

T0 = time.time()
MID = "M_INNOV_GBA_PATENT_PAPER"

scan = C.load_patent_scan()
papers = C.load_papers()
pc = C.patent_city_year(scan)
pp = C.paper_city_year(papers)

rows = []
for city in C.GBA11:
    pat = sum(pc.get((city, y), 0) for y in C.YEARS_FULL)
    pap = sum(pp.get((city, y), 0) for y in C.YEARS_FULL)
    rows.append({
        "city": city,
        "patent_cnt_2021_2024": pat,
        "paper_cnt_2021_2024": pap,
        "total_cnt": pat + pap,
        "patent_share_of_comparable": None,
        "paper_share": None,
        "patent_source": "exact_name" if city in C.COVERED else "no_org_in_roster_zero",
        "paper_source": "first_author_affiliation_rule",
        "comparable": city in C.COVERED,
    })

pat_tot = sum(r["patent_cnt_2021_2024"] for r in rows)
pap_tot = sum(r["paper_cnt_2021_2024"] for r in rows)
for r in rows:
    r["patent_share_of_comparable"] = C.pct(r["patent_cnt_2021_2024"], pat_tot)
    r["paper_share"] = C.pct(r["paper_cnt_2021_2024"], pap_tot)
    r["total_share"] = C.pct(r["total_cnt"], pat_tot + pap_tot)

paper_window = {c: sum(pp.get((c, y), 0) for y in (2021, 2022, 2023)) for c in C.GBA11}
year_all = papers["year_all"]
corpus = papers["rows_declared"]
first_mapped_total = sum(pp.values())

out = {
    "metric_id": MID,
    "metric_name": "专利及论文数量",
    "domain": "INNOV / 湾区创新监测（DS-05）",
    "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    "window": "2021–2024 四个完整自然年（gkx 专利表无 2017–2020 行，2025/2026 不完整）",
    "unit": "件 / 篇",
    "formula": "total(city) = COUNT(patent | applicant_city=city) + COUNT(paper | first_author_city=city)",
    "definition_note": "专利为申请口径（全部 kind），授权量不并入；论文按第一完成单位；两语料不同源，"
                       "合计仅作目录口径并列。",
    "rows": rows,
    "totals": {
        "patent_total_mapped": pat_tot,
        "paper_total_mapped_2021_2024": pap_tot,
        "total": pat_tot + pap_tot,
        "cities_with_patent": sum(1 for r in rows if r["patent_cnt_2021_2024"] > 0),
        "cities_with_paper": sum(1 for r in rows if r["paper_cnt_2021_2024"] > 0),
        "patent_2024_all_cities": sum(pc.get((c, 2024), 0) for c in C.GBA11),
        "patent_2024_universe": year_all.get("2024"),
        "patent_2024_match_share": C.pct(sum(pc.get((c, 2024), 0) for c in C.GBA11),
                                         year_all.get("2024")),
    },
    "paper_window_sensitivity": {
        "window": "2021–2023（剔除 2024 入库尖峰）",
        "by_city": paper_window,
        "total": sum(paper_window.values()),
        "corpus_by_year": {y: year_all.get(y) for y in ("2021", "2022", "2023", "2024", "2025")},
        "note": "全国论文量 2023 年 6,651 篇 → 2024 年 32,379 篇（4.87 倍），11 城同步跳增，"
                "属入库批次断点而非发表激增；主表仍按需求窗口 2021–2024 列示，敏感性表用于验证排序。",
    },
    "paper_coverage": {
        "corpus": corpus,
        "first_author_mapped": first_mapped_total,
        "first_author_mapped_share": C.pct(first_mapped_total, corpus),
        "papers_with_no_gba_city": papers["papers_with_no_gba_city"],
        "parse_errors": papers["parse_errors"],
        "top_unmapped_first_inst": papers["unmapped_first_inst_top"][:10],
        "note": "未归属部分不摊分、不估算；未归属首单位里「广东电网科学研究院」「广东科技学院」等"
                "虽明显在粤，但机构名不含城市 token，按规则一律不猜。",
    },
    "known_traps": [
        "论文无结构化城市/行政区划码；「中山大学」在广州市，token 直判会把 2 万余篇误计中山市。",
        "论文库 2024 年入库尖峰（广州 4,275 篇 vs 2023 年 954 篇），年度同比不可解释。",
        "专利侧 7 城无企业底册入集，专利数恒 0；只看 total 排名会退化为「深广莞惠」四城排序。",
        "专利与论文是两个不同语料宇宙，相加只作目录口径的并列合计，不可解释为「创新产出当量」。",
        "底册 99.82% 在广东，本表本质是深圳都市圈 + 少量港澳/珠西的论文命中，不是湾区全域普查。",
    ],
    "support_judgment": {
        "data_support_level": "部分支持",
        "criteria": {
            "structure": "dwd_patent(全表缓存) + dwd_zh_paper(author_info_list) + 底册(name/city)",
            "volume": f"专利 4 城可算（{pat_tot:,} 件）；论文 11 城均有命中（{pap_tot:,} 篇，"
                      f"可归属率 {C.pct(first_mapped_total, corpus):.1%}）",
            "reproducible": True,
            "discriminative": True,
        },
        "blocking_gaps": [
            "专利城市归属仅 4/11 城，7 城专利维恒 0。",
            f"论文第一单位可映射率仅 {C.pct(first_mapped_total, corpus):.1%}，其余无城市键。",
            "两语料口径不同源，合计值只能作展示口径。",
            "论文 2024 入库断点使年度同比不可解释。",
        ],
        "note": "专利维可算且量级可对表；论文维靠机构名规则、可归属率不足四分之一，故不得升到完全转换支持。",
    },
    "runtime_sec": round(time.time() - T0, 2),
}

C.write_out(MID, out)
print(f"[{time.time() - T0:.1f}s] patent={pat_tot:,} paper={pap_tot:,} total={pat_tot + pap_tot:,}")
for r in rows:
    print(f"  {r['city']:<6} patent={r['patent_cnt_2021_2024']:>9,} "
          f"paper={r['paper_cnt_2021_2024']:>6,} total={r['total_cnt']:>9,}")

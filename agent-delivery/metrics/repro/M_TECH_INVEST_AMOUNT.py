#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TECH_INVEST_AMOUNT —— 技术投入金额（深圳上市主体研发费用，按 IPC4 分摊）。

口径（单一，深圳金额）：
  - 金额源 = `dwd_org_stock_finance_info.research_development_amount`（上市公司年报研发费用），
    缓存 `pg_stock_rd_annual_20261021.json`，873 家上市主体（深圳/广州/东莞/惠州）；
  - 主体城市 = `dwd_org_base_info` 的 `city`（按 org_id join，873/873 命中）；
  - 分摊键 = 该主体在 `patent_ipc4_by_name_20261021.json` 中、落在 238 个合格 IPC4 域内的
    专利件数占比；不在合格域内的专利不参与分摊，留在「未分摊池」；
  - 分母 = 深圳上市主体当年研发费用合计（元），不掺全国、不掺非上市企业。

政府/产业基金（`dwd_industrial_fund_basic_info`）只有基金注册地与认缴/实缴资本，
没有投资项目级金额、也没有 IPC/技术域字段，因此**不摊进域级金额**，单列一张存量表。

零 SQL：只读 _snapshots21 授权缓存；全国金额上下文取自 `city_family_probe` 的实测探针。
"""
from __future__ import annotations

import collections
import re

import _tech21_scope as sc
from _tech21_common import IPC_LABEL

METRIC = "M_TECH_INVEST_AMOUNT"
YEARS = [2021, 2022, 2023, 2024]

# 全国上市主体研发费用（`city_family_probe_20261021.json` → stock_period 探针，单位元）
NAT_RD = {2021: 282350854708.13, 2022: 330036076514.63,
          2023: 380244103269.75, 2024: 454643143159.48}


def parse_cap(s):
    if not s:
        return None
    m = re.match(r"([\d.]+)\s*(万元|亿元|元)?", str(s))
    if not m:
        return None
    v = float(m.group(1))
    unit = m.group(2) or "元"
    return v * {"元": 1.0, "万元": 1e4, "亿元": 1e8}.get(unit, 1.0)


def main():
    base = sc._load(sc.SNAP / "base_20261021.json")
    city_of = {r[0]: r[4] for r in base}
    rd_rows = sc._load(sc.SNAP / "pg_stock_rd_annual_20261021.json")

    cell, _ = sc.load_sz_ipc()
    panel = {d: {y: int(cell.get((d, y), 0)) for y in YEARS} for d in {d for d, _ in cell}}
    qualified = sorted([d for d, v in panel.items() if v[2024] >= 100])
    qset = set(qualified)

    # 主体 → 合格域内专利结构
    ipc_name = sc.load_ipc_name()
    mix = collections.defaultdict(dict)
    for ipc4, nm, n in ipc_name:
        if ipc4 in qset:
            mix[nm][ipc4] = mix[nm].get(ipc4, 0) + int(n)

    # 主体 → 年 → 研发费用（只保留深圳）
    rd_sz = collections.defaultdict(lambda: collections.defaultdict(float))
    org_city = {}
    for r in rd_rows:
        city = city_of.get(r["org_id"])
        if not city:
            continue
        org_city[r["org_id"]] = city
        y = int(str(r["period"])[:4])
        if city == "深圳市" and y in YEARS and r.get("rd") is not None:
            rd_sz[y][r["name"]] += float(r["rd"])

    # 按主体专利结构分摊
    alloc = {y: collections.Counter() for y in YEARS}
    unalloc = {y: 0.0 for y in YEARS}
    contributors = collections.defaultdict(set)
    for y in YEARS:
        for nm, amount in rd_sz[y].items():
            m = mix.get(nm)
            if not m:
                unalloc[y] += amount
                continue
            tot = sum(m.values())
            for ipc4, c in m.items():
                alloc[y][ipc4] += amount * c / tot
                contributors[ipc4].add(nm)

    # 平衡样本的域级金额：只保留 2021 与 2024 都在报的深圳主体，
    # 用于把「真实增减」与「进出样本造成的构成漂移」分开（B23Q、H02K 是典型）。
    both = set(rd_sz[2021]) & set(rd_sz[2024])
    bal_alloc = {2021: collections.Counter(), 2024: collections.Counter()}
    for y in (2021, 2024):
        for nm in both:
            amount = rd_sz[y].get(nm, 0.0)
            m = mix.get(nm)
            if not m:
                continue
            tot = sum(m.values())
            for ipc4, c in m.items():
                bal_alloc[y][ipc4] += amount * c / tot

    rows = []
    for d in qualified:
        a21, a24 = alloc[2021].get(d, 0.0), alloc[2024].get(d, 0.0)
        total = sum(alloc[y].get(d, 0.0) for y in YEARS)
        # 单主体集中度：该域 2024 年金额里最大一家主体的占比
        by_org = []
        for nm, amount in rd_sz[2024].items():
            m = mix.get(nm)
            if not m:
                continue
            tot = sum(m.values())
            if m.get(d):
                by_org.append((amount * m[d] / tot, nm))
        by_org.sort(reverse=True)
        top1 = round(by_org[0][0] / a24, 4) if a24 and by_org else None
        rows.append({
            "ipc4": d, "label": IPC_LABEL.get(d, ""),
            "amount_yuan": [round(alloc[y].get(d, 0.0), 2) for y in YEARS],
            "amount_yi": [round(alloc[y].get(d, 0.0) / 1e8, 4) for y in YEARS],
            "total_4y_yi": round(total / 1e8, 4),
            "g_2021_2024": round((a24 - a21) / a21, 4) if a21 else None,
            "amount_yi_balanced": [round(bal_alloc[y].get(d, 0.0) / 1e8, 4) for y in (2021, 2024)],
            "g_balanced": (round((bal_alloc[2024].get(d, 0.0) - bal_alloc[2021].get(d, 0.0))
                                 / bal_alloc[2021][d], 4)
                           if bal_alloc[2021].get(d) else None),
            "composition_flag": (abs((a24 - a21) / a21 - (bal_alloc[2024].get(d, 0.0) - bal_alloc[2021].get(d, 0.0)) / bal_alloc[2021][d]) > 0.5
                                 if a21 and bal_alloc[2021].get(d) else None),
            "n2024": panel[d][2024],
            "intensity_yuan_per_patent": round(a24 / panel[d][2024], 2) if panel[d][2024] else None,
            "listed_contributors": len(contributors[d]),
            "top1_org_share_2024": top1,
            "top1_org": by_org[0][1] if by_org else None,
        })
    rows.sort(key=lambda r: -r["total_4y_yi"])

    # 城市级合计
    city_tot = {y: sum(rd_sz[y].values()) for y in YEARS}
    alloc_tot = {y: sum(alloc[y].values()) for y in YEARS}
    # 平衡面板：2021 与 2024 都有研发费用的主体（剔除进出样本的构成漂移）
    bal21 = sum(rd_sz[2021][n] for n in both)
    bal24 = sum(rd_sz[2024][n] for n in both)
    city_rows = []
    for y in YEARS:
        city_rows.append({
            "year": y, "sz_listed_rd_yi": round(city_tot[y] / 1e8, 2),
            "allocated_yi": round(alloc_tot[y] / 1e8, 2),
            "unallocated_yi": round(unalloc[y] / 1e8, 2),
            "allocated_share": round(alloc_tot[y] / city_tot[y], 4) if city_tot[y] else None,
            "n_orgs": len(rd_sz[y]),
            "nat_listed_rd_yi": round(NAT_RD[y] / 1e8, 2),
            "sz_share_of_nat": round(city_tot[y] / NAT_RD[y], 4),
        })

    # 基金（存量，不进域级合计）
    funds = sc._load(sc.SNAP / "pg_fund_rows_20261021.json")
    sz_funds = [f for f in funds if "深圳市" in str(f.get("reg_region", ""))]
    real = [parse_cap(f.get("real_capital")) for f in sz_funds]
    reg = [parse_cap(f.get("reg_capital")) for f in sz_funds]
    real_ok = [x for x in real if x]
    reg_ok = [x for x in reg if x]
    ftype = collections.Counter(f.get("fund_type") or "未披露" for f in sz_funds)
    fyear = collections.Counter(str(f.get("est_date"))[:4] for f in sz_funds)
    fund_block = {
        "sz_funds": len(sz_funds),
        "with_real_capital": len(real_ok),
        "real_capital_yi": round(sum(real_ok) / 1e8, 2),
        "with_reg_capital": len(reg_ok),
        "reg_capital_yi": round(sum(reg_ok) / 1e8, 2),
        "fund_type_top": ftype.most_common(6),
        "est_year_2021_2024": {y: fyear.get(str(y), 0) for y in YEARS},
        "note": "基金资本是存量（认缴/实缴），不是年度流量，且无 IPC 字段，不并入域级研发投入合计",
    }

    total_4y = sum(r["total_4y_yi"] for r in rows)
    payload = {
        "metric_id": METRIC,
        "generated_at": "2026-10-22",
        "scope": "深圳",
        "scope_statement": (
            "本件金额分母是「深圳上市主体当年研发费用合计」：2021—2024 分别为 "
            "784.24 / 906.56 / 1,034.58 / 1,545.04 亿元。域级金额是这笔钱的专利结构分摊，"
            "不含非上市企业、不含政府专项、不含基金资本；全国金额只在一张上下文表出现，"
            "不进入任何分母。同一张表内不混用深圳与全国金额。"
        ),
        "main_db": "gkx @ 183.240.141.251:3318 (gkx_reader_zp, read-only)",
        "sql_count": 0,
        "base_years_used": YEARS,
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": (
            "研发费用缓存覆盖 2007—2025，但专利面板只有 2021—2026（2017—2020 零行），"
            "为保证「金额年 × 专利结构年」同窗，只取 2021—2024；2025 有金额但无同窗专利，"
            "不进入增速与均值。缺失年不按 0 摊入。"
        ),
        "input": {
            "rd": "code/_snapshots21/pg_stock_rd_annual_20261021.json",
            "org_city": "code/_snapshots21/base_20261021.json",
            "ipc_by_name": "code/_snapshots21/patent_ipc4_by_name_20261021.json",
            "funds": "code/_snapshots21/pg_fund_rows_20261021.json",
            "nat_rd_probe": "code/_snapshots21/city_family_probe_20261021.json#stock_period",
        },
        "reused_from": "_tech21_scope.py（共用离线取数层，零 SQL）",
        "method": {
            "allocation": "域金额(y)=Σ_主体 研发费用(主体,y)×主体域内件数/主体合格域总件数",
            "assumption_1": "企业全部研发费用都投向其专利覆盖的技术域（研发费用不区分技术与非技术）",
            "assumption_2": "企业专利的域结构在四年内不变（用全期结构分摊各年金额）",
            "excluded": "非上市企业研发、政府科技专项、基金资本、技术交易额",
        },
        "city_totals": city_rows,
        "headline": {
            "sz_listed_rd_2024_yi": round(city_tot[2024] / 1e8, 2),
            "sz_listed_rd_2021_yi": round(city_tot[2021] / 1e8, 2),
            "growth_2021_2024": round((city_tot[2024] - city_tot[2021]) / city_tot[2021], 4),
            "allocated_2024_share": round(alloc_tot[2024] / city_tot[2024], 4),
            "unallocated_2024_yi": round(unalloc[2024] / 1e8, 2),
            "domains_with_amount": len([r for r in rows if r["total_4y_yi"] > 0]),
            "total_4y_yi": round(total_4y, 2),
            "top_domain_2024": max(rows, key=lambda r: r["amount_yi"][3])["ipc4"],
            "top_domain_amount_2024_yi": round(max(r["amount_yi"][3] for r in rows), 2),
            "top_domain_share_2024": round(max(r["amount_yi"][3] for r in rows) / (alloc_tot[2024] / 1e8), 4),
            "balanced_orgs": len(both),
            "composition_sensitive_domains": len([r for r in rows if r.get("composition_flag")]),
            "balanced_growth_2021_2024": round((bal24 - bal21) / bal21, 4) if bal21 else None,
            "balanced_rd_2021_yi": round(bal21 / 1e8, 2),
            "balanced_rd_2024_yi": round(bal24 / 1e8, 2),
            "orgs_2021": len(rd_sz[2021]), "orgs_2024": len(rd_sz[2024]),
        },
        "top20": rows[:20],
        "bottom10": rows[-10:],
        "fund_pool": fund_block,
        "domains": rows,
        "support_judgment": {
            "data_support_level": "部分支持",
            "structure_support": "部分",
            "data_support": "部分",
            "reason": (
                "金额侧只有上市主体年报研发费用（深圳 412 家、1,545.04 亿元），非上市企业、"
                "政府专项、基金投资项目金额三项缺源：`dwd_org_annual_financial_info` 的"
                "`arch_development_am` 整列为空（0/90,926），基金表只有基金级认缴/实缴、"
                "无项目级金额与 IPC 字段。故只能交付「上市主体研发费用域级分摊」，"
                "不能交付「政府专项+社会资本」全口径技术投入。"
            ),
        },
    }
    sc.write_out(METRIC, payload)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_KPI_BOARD｜全球创新实时看板指标（只读聚合板，零 SQL）。

本件不产生任何新口径、不连数据库。每个格子只做一件事：
从**正式区** `第三方库指标计算过程/<ID>.md` 对应的 `code/<ID>_out.json` 里
按写死的键路径读一个标量，并记录来源件 ID、文件、键路径、官方区状态。

  - 有来源件 → `value` = 原值（不做单位换算，只登记 unit）；
  - 无来源件 → `value = null`，`missing_reason` 写明缺哪件、为什么；
  - 来源件在 code/ 有 out.json、但正式区没有同名 md → 视为「未归档」，
    同样写 null，防止拿暂存区半成品冒充满足格子。

运行：`cd code && python3 M_INNOV_KPI_BOARD.py`
产物：`code/M_INNOV_KPI_BOARD_out.json`
"""
from __future__ import annotations

import json
import os
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OFFICIAL = os.path.join(ROOT, "第三方库指标计算过程")
OUT = os.path.join(HERE, "M_INNOV_KPI_BOARD_out.json")

# (cell_id, 标签, 类别, 来源件 ID, 键路径, 单位, 窗口)
CELLS = [
    ("patent_total", "专利公开总量", "专利", "M_TECH_PAPER_PATENT_CNT",
     ["counts", "patent_rows"], "件", "全库（2021—2026 申请年）"),
    # 2026-10-23 修：原来源是 M_TECH_PAPER_PATENT_CNT.patent_axis.total_2021_2024 = 2,009,365，
    # 那是 IPC 非空行（634 域口径）的四年合计，不是全表四年合计。它与 130/131/132/135
    # 四件共用的「基期专利总量」是同一常量，用来看领域结构没问题；但拿它当「全表近四年」
    # 再除以全表总量，就得到 68.35%——分子少算 41.5 万行 IPC 缺失件、分母没少，真实值 82.4752%。
    # 改取 M_INNOV_POT_OUTPUT 的全表口径（该件已归档，属正式区兄弟件）。
    ("patent_2021_2024", "专利 2021—2024 合计（全表口径）", "专利", "M_INNOV_POT_OUTPUT",
     ["total", "patent_2021_2024"], "件", "2021—2024"),
    ("sz_patent_2024", "深圳专利 2024", "专利", "M_TECH_HEAT_INDEX",
     ["coverage", "sz_by_year", "2024"], "件", "2024"),
    ("sz_qualified_domains", "深圳合格技术域数", "专利", "M_TECH_HEAT_INDEX",
     ["coverage", "qualified_domains"], "个 IPC4", "2024 年 ≥100 件"),
    ("tech_heat_median", "技术域热度中位数", "专利", "M_TECH_HEAT_INDEX",
     ["index_stats", "median"], "0—100", "2021—2024"),
    ("paper_total", "中文论文总量", "论文", "M_TECH_PAPER_PATENT_CNT",
     ["counts", "paper_rows"], "篇", "1980—2026 全库"),
    ("paper_2023", "中文论文 2023", "论文", "M_TECH_PAPER_PATENT_CNT",
     ["paper_axis", "year_counts_2015_2026", "2023"], "篇", "2023"),
    ("paper_cited_per_paper", "论文篇均被引", "论文", "M_INNOV_POT_SCI_INFL",
     ["paper_level", "cited_per_paper"], "次/篇", "有引文记录的 20,031 篇"),
    ("citation_join_rate", "引文记录覆盖率", "论文", "M_INNOV_POT_SCI_INFL",
     ["coverage", "citation_author_join_rate_vs_zh_paper"], "比率（0—1）", "20,031 / 100,900"),
    ("sz_rd_2024_yi", "深圳上市主体研发费用 2024", "投资/经费", "M_TECH_INVEST_AMOUNT",
     ["headline", "sz_listed_rd_2024_yi"], "亿元", "2024"),
    ("sz_rd_growth_2021_2024", "深圳上市主体研发费用增幅", "投资/经费", "M_TECH_INVEST_AMOUNT",
     ["headline", "growth_2021_2024"], "比率（0—1）", "2021→2024"),
    ("invest_cny_2024_wan", "投融资事件金额 2024（CNY）", "投资/经费", "M_CHAIN_INVEST_TOTAL",
     ["year_block_cny_mapped", "2024", "cny_wan"], "万元", "2024（仅已挂链、有金额）"),
    ("hightech_orgs", "高新技术企业数", "主体", "M_ENT_HIGH_TECH_COUNT",
     ["result", "high_tech_orgs_distinct"], "家", "标签表截面"),
    ("sz_fund_count", "深圳产业基金数", "主体", "M_INNOV_PG_COMPOSITE",
     ["leaves", "L4_fund_count", "raw", "深圳市"], "支", "注册地落城截面"),
    ("event_count", "事件条数", "事件", None, None, "条", "—"),
    ("event_attention", "事件关注度", "事件", None, None, "0—100", "—"),
]

# 2026-10-23 修：原理由写的是「`M_TNIE_EVENT_COUNT` 在本批暂存区（未归档）」——归档那一刻
# 这句话就变成假的（文件已进正式区）。缺格的理由必须**只依赖数据面事实**，不依赖归档进度：
# 事件面缺源是长期事实，代理读数不能填真计数格是口径决定。两者都不随归档动作改变。
NULL_REASON = {
    "event_count": ("事件面缺源：`innovation_event` / `dwd_innovation_event` 在 gkx 逐字 0，"
                    "`dwd_event` 仅 20 行且是单一展会系列（2026-05-13/14，国药励展），"
                    "不构成事件面。`M_TNIE_EVENT_COUNT` 交的是「活动型标题条数」代理读数"
                    "（18,884 / 1,668,414），本板格要的是事件发生数，故置 null 不填代理。"),
    "event_attention": ("事件面缺源，且 `M_INNOV_EVENT_ATTENTION` 判完全不支持、交的是负证据"
                        "（policy 文本 theme/quote_policy 各 19,998 行为字符串 'NULL'）。"
                        "负证据不是 0—100 分数，看板格不填。"),
}


def get_path(obj, path):
    cur = obj
    for k in path:
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        else:
            return None, False
    return cur, True


def main() -> None:
    cells = []
    sources = []
    for cid, label, cat, mid, path, unit, window in CELLS:
        rec = {
            "cell_id": cid, "label": label, "category": cat, "unit": unit,
            "window": window, "source_metric_id": mid,
            "source_key": ".".join(path) if path else None,
            "source_official_area": False, "source_out_json": None,
            "value": None, "status": "null", "missing_reason": None,
        }
        if mid is None:
            rec["missing_reason"] = NULL_REASON[cid]
            cells.append(rec)
            continue
        md = os.path.join(OFFICIAL, mid + ".md")
        oj = os.path.join(HERE, mid + "_out.json")
        rec["source_official_area"] = os.path.exists(md)
        rec["source_out_json"] = f"code/{mid}_out.json"
        if not os.path.exists(md):
            rec["missing_reason"] = f"正式区缺 `{mid}.md`（未归档），不采用暂存区读数"
            cells.append(rec)
            continue
        if not os.path.exists(oj):
            rec["missing_reason"] = f"正式区有 `{mid}.md`，但 `code/{mid}_out.json` 不存在"
            cells.append(rec)
            continue
        with open(oj, encoding="utf-8") as fh:
            src = json.load(fh)
        val, ok = get_path(src, path)
        if not ok or val is None:
            rec["missing_reason"] = f"来源件 `{mid}_out.json` 无键路径 {rec['source_key']}"
            cells.append(rec)
            continue
        rec["value"] = val
        rec["status"] = "ok"
        cells.append(rec)
        if mid not in {s["metric_id"] for s in sources}:
            sources.append({
                "metric_id": mid,
                "md": f"第三方库指标计算过程/{mid}.md",
                "out_json": f"code/{mid}_out.json",
            })

    ok_cells = [c for c in cells if c["status"] == "ok"]
    null_cells = [c for c in cells if c["status"] != "ok"]

    def cell(cid):
        return next(c for c in cells if c["cell_id"] == cid)["value"]

    def derive(value, num, den, note):
        return {"value": value, "numerator": num, "denominator": den,
                "denominator_note": note}

    patent_total = cell("patent_total")
    patent_4y = cell("patent_2021_2024")
    paper_total = cell("paper_total")
    paper_2023 = cell("paper_2023")
    cited_rate = cell("citation_join_rate")
    rd_growth = cell("sz_rd_growth_2021_2024")
    sz_patent = cell("sz_patent_2024")
    hitech = cell("hightech_orgs")
    fund_sz = cell("sz_fund_count")

    # 四城基金合计：只从同一来源件的四个城市键求和，跨池不相除
    with open(os.path.join(HERE, "M_INNOV_PG_COMPOSITE_out.json"), encoding="utf-8") as fh:
        pg = json.load(fh)
    fund_four = sum(int(v) for v in pg["leaves"]["L4_fund_count"]["raw"].values())

    # 派生用到的相邻量也从同一批来源件读，不在脚本里写死
    with open(os.path.join(HERE, "M_TECH_INVEST_AMOUNT_out.json"), encoding="utf-8") as fh:
        inv = json.load(fh)["headline"]
    with open(os.path.join(HERE, "M_TECH_HEAT_INDEX_out.json"), encoding="utf-8") as fh:
        heat = json.load(fh)["coverage"]
    with open(os.path.join(HERE, "M_INNOV_POT_SCI_INFL_out.json"), encoding="utf-8") as fh:
        sci = json.load(fh)["coverage"]

    derived = {
        # 2026-10-23 改：原 2,009,365 / 2,939,895 = 68.3482%，分子是 IPC 非空子集、分母是全表，
        # 两侧不同基。改为全表 / 全表 = 82.4752%；IPC 子集口径另立对照键。
        # 2026-10-23 改：原 2,009,365 / 2,939,895 = 68.3482%，分子是 IPC 非空子集、分母是全表，
        # 两侧不同基，读成「近四年占全库」会低报 14 个百分点。改为全表 / 全表 = 82.4752%；
        # IPC 子集口径另立对照键（与 130/131/132/135 的「基期专利总量」同源）。
        "patent_2021_2024_share_pct": derive(
            round(patent_4y / patent_total * 100, 4), patent_4y, patent_total,
            "分子 = 全表 2021—2024 合计 2,424,684 件（M_INNOV_POT_OUTPUT.total.patent_2021_2024）；"
            "分母 = 专利公开总量 2,939,895（M_TECH_PAPER_PATENT_CNT.counts.patent_rows），两侧同为全表口径。"
            "注意不要用 2,009,365（IPC 非空行四年合计）当分子：那是领域结构的基期常量，"
            "与全表分母不同基，会得 68.3482% 的假低值"),
        "patent_2021_2024_ipc_share_pct": derive(
            round(2009365 / patent_total * 100, 4), 2009365, patent_total,
            "对照键：分子 = IPC 非空的 2021—2024 合计 2,009,365（634 域口径，130/131/132/135 同常量）；"
            "分母同样取全表 2,939,895。此值只用于说明「分母未变、分子换成 IPC 子集」会把 82.4752% 压到 68.3482%，"
            "不作为近四年占比发布"),
        "paper_2023_share_pct": derive(
            round(paper_2023 / paper_total * 100, 4), paper_2023, paper_total,
            "分母 = 中文论文总量（M_TECH_PAPER_PATENT_CNT.counts.paper_rows）"),
        "citation_join_pct": derive(
            round(cited_rate * 100, 4), sci["papers_with_citation"], sci["zh_paper_total"],
            "分子/分母来自 M_INNOV_POT_SCI_INFL.coverage：有引文记录篇数 / 中文论文总篇数"),
        "rd_growth_pct": derive(
            round(rd_growth * 100, 4),
            round(inv["sz_listed_rd_2024_yi"] - inv["sz_listed_rd_2021_yi"], 4),
            inv["sz_listed_rd_2021_yi"],
            "分子 = 2024 减 2021 的研发费用增量（亿元），分母 = 2021 研发费用（亿元）；"
            "同一来源件 M_TECH_INVEST_AMOUNT.headline"),
        "sz_patent_share_of_nat_2024_pct": derive(
            round(sz_patent / heat["nat_by_year"]["2024"] * 100, 4),
            sz_patent, heat["nat_by_year"]["2024"],
            "分母 = 全国 2024 专利件数（M_TECH_HEAT_INDEX.coverage.nat_by_year.2024）"),
        "hightech_share_of_base_pct": derive(
            round(hitech / 189116 * 100, 4), hitech, 189116,
            "分母 = 企业底册 189,116 家（共享常量 SHARED_CONSTANTS.json）"),
        "sz_fund_share_four_cities_pct": derive(
            round(fund_sz / fund_four * 100, 4), fund_sz, fund_four,
            "分母 = 北京+上海+深圳+广州产业基金合计 1,881 支（同一来源件四城 raw 求和）"),
        "cells_with_source_pct": derive(
            round(len(ok_cells) / len(cells) * 100, 4), len(ok_cells), len(cells),
            "分母 = 看板格总数 16；分子 = 能从正式区兄弟件读到值的 14 格"),
    }

    out = {
        "metric_id": "M_INNOV_KPI_BOARD",
        "metric_name_zh": "全球创新实时看板指标",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "support_judgment": "部分支持",
        "verdict_kind": "aggregation_readonly",
        "judgment_reason": (
            "看板 16 格中 14 格能从正式区兄弟件读到已归档读数（专利/论文/经费/主体四类），"
            "2 格（事件条数、事件关注度）因事件面缺源置 null——不是缺件，是缺数据。"
            "本件不新造任何口径，也不把暂存区半成品当来源；因此整体判部分支持，而不是完全转换支持。"
        ),
        "sources": sources,
        "base_years_used": [2021, 2022, 2023, 2024],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": (
            "看板主窗取 2021—2024，与专利/研发四件同窗；2017—2020 专利表零行，不按 0 摊入。"
            "论文 2024 为入库批次峰（32,379 篇），本板只展示 2023 截面，不把 2024 当趋势。"
            "投资金额格取 2024 年；其余截面格（高企、基金、技术域）不参与年度序列。"
        ),
        "cells": cells,
        "summary": {
            "n_cells": len(cells),
            "n_with_value": len(ok_cells),
            "n_null": len(null_cells),
            "null_cells": [c["cell_id"] for c in null_cells],
            "category_count": {
                k: sum(1 for c in cells if c["category"] == k)
                for k in ("专利", "论文", "投资/经费", "主体", "事件")
            },
        },
        "derived": derived,
        "absence_probe": {
            "dwd_kpi": {
                "condition": "information_schema.tables WHERE table_schema='gkx' AND table_name='dwd_kpi'",
                "hits": 0,
            },
            "dwd_indicator": {
                "condition": "information_schema.tables WHERE table_schema='gkx' AND table_name='dwd_indicator'",
                "hits": 0,
            },
            # 2026-10-23 修：原为写死 hits=0，归档后立刻自打脸。改为现读文件是否存在，
            # 并显式说明「存在 ≠ 可填格」，避免读者把 hits=1 误读成该格已满足。
            "event_count_sibling": {
                "condition": "正式区 第三方库指标计算过程/M_TNIE_EVENT_COUNT.md 是否存在",
                "hits": int(os.path.exists(os.path.join(ROOT, "第三方库指标计算过程",
                                                        "M_TNIE_EVENT_COUNT.md"))),
                "note": "存在也只交代理读数（活动型标题），不是事件发生数，不填看板格",
            },
            "event_attention_sibling": {
                "condition": "正式区 第三方库指标计算过程/M_INNOV_EVENT_ATTENTION.md 是否存在",
                "hits": int(os.path.exists(os.path.join(ROOT, "第三方库指标计算过程",
                                                        "M_INNOV_EVENT_ATTENTION.md"))),
                "note": "存在也只交负证据（完全不支持），没有可填的分数",
            },
        },
        "rule": (
            "每格只读正式区兄弟件 `_out.json` 的一个标量，键路径写死在 CELLS；"
            "不做单位换算、不做加总、不跨池相除。来源件未归档或键路径缺失即置 null。"
        ),
        "reproduce": "cd code && python3 M_INNOV_KPI_BOARD.py",
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print(f"[ok] {OUT} cells={len(cells)} with_value={len(ok_cells)} null={len(null_cells)}")


if __name__ == "__main__":
    main()

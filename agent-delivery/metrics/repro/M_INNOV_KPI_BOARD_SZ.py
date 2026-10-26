#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_KPI_BOARD_SZ · 深圳科技发展指标看板（城市看板级聚合，20261021 换源版）

与全国版 M_INNOV_KPI_BOARD 的区别（§1.6 口径对照）：
  · 全国版回答「全球创新监测六大子功能各格能不能出数」；
  · 深圳版只回答「在深圳这一城市口径下，11 个科技维度各自有没有属地可归属的数据」。
  分母不同：全国版用全库总量，深圳版一律用深圳归属子集，并同时给出占比。

20261021 换源
-------------
- 专利不再查 `dwd_patent`：深圳专利与年度序列从
  `_snapshots21/patent_panel_innov_20261021.json` 的 `app_year` 离线派生（窗口 2021–2024）。
- 期刊 / 学者 / 机构 / 基金 / 政策 / 项目 / 主题全部走 `gkx` 三方库。
- 会议维度：`gkx` 元数据检索 conference/meeting 命中 0 张表。
- 载体维度：`gkx` 无载体表；`live.enterprise_innovation_carrier` 是单批模板数据，按质量规则排除，
  不给分子，也不把演示值写进看板。

输出：code/M_INNOV_KPI_BOARD_SZ_out.json
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _gkxdb  # noqa: E402

OUT = HERE / "M_INNOV_KPI_BOARD_SZ_out.json"
PANEL = HERE / "_snapshots21" / "patent_panel_innov_20261021.json"


def q(sql):
    cur = _gkxdb.gkx()
    try:
        cur.execute(sql)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    finally:
        cur.close()


def one(sql):
    r = q(sql)
    return r[0] if r else {}


def main():
    t0 = time.time()

    paper = one("""SELECT COUNT(*) AS n, SUM(author_info_list LIKE '%%深圳%%') AS sz
                   FROM gkx.dwd_zh_paper""")
    scholar = one("""SELECT COUNT(*) AS n, SUM(scholar_org_name_zh LIKE '%%深圳%%') AS sz
                     FROM gkx.dwd_scholar""")
    journal = one("""SELECT COUNT(*) AS n, SUM(cite_nums IS NOT NULL) AS cited
                     FROM gkx.dwd_zh_journal""")
    org = one("""SELECT COUNT(*) AS n, SUM(city LIKE '%%深圳%%') AS sz
                 FROM gkx.dwd_org_base_info""")
    inst = one("""SELECT COUNT(*) AS n, SUM(city LIKE '%%深圳%%') AS sz
                  FROM gkx.dwd_research_institute_base_info""")
    fund = one("""SELECT COUNT(*) AS n, SUM(reg_region LIKE '%%深圳%%') AS sz
                  FROM gkx.dwd_industrial_fund_basic_info""")
    policy = one("""SELECT COUNT(*) AS n, SUM(city LIKE '%%深圳%%') AS sz,
                           SUM(theme IS NULL OR theme='' OR theme='NULL') AS theme_null
                    FROM gkx.dwd_policy_base""")
    project = one("""SELECT COUNT(*) AS n,
                            SUM(funded_institution IS NULL OR funded_institution='') AS inst_null,
                            SUM(funded_province IS NULL OR funded_province='') AS prov_null
                     FROM gkx.dwd_zh_project""")
    topic = one("""SELECT COUNT(*) AS n, COUNT(DISTINCT topic_name) AS d
                   FROM gkx.dwd_industry_analysis_topics""")
    conf = q("""SELECT table_name AS tn FROM information_schema.tables
                WHERE table_schema='gkx' AND (table_name LIKE '%confer%'
                   OR table_name LIKE '%meeting%')""")

    # 专利只读面板：2021–2024 全量 2,424,684 行，按第一申请人名称含「深圳」落城
    p = json.loads(PANEL.read_text(encoding="utf-8"))
    sz_pat_year = {str(y): 0 for y in range(2021, 2025)}
    for key, n in p["app_year"].items():
        y, nm = key.split("|", 1)
        if y in sz_pat_year and "深圳" in nm:
            sz_pat_year[y] += int(n)
    pat_sz = sum(sz_pat_year.values())
    pat_total = sum(int(v) for v in p["year_all"].values())

    paper_year = {str(r["y"]): int(r["n"]) for r in q("""
        SELECT cover_year_start AS y, COUNT(*) AS n FROM gkx.dwd_zh_paper
        WHERE author_info_list LIKE '%深圳%'
          AND cover_year_start BETWEEN '2015' AND '2026'
        GROUP BY cover_year_start ORDER BY cover_year_start""")}
    policy_year = {str(r["y"]): int(r["n"]) for r in q("""
        SELECT publish_year AS y, COUNT(*) AS n FROM gkx.dwd_policy_base
        WHERE city LIKE '%深圳%' AND publish_year BETWEEN '2015' AND '2026'
        GROUP BY publish_year ORDER BY publish_year""")}

    sz = {
        "patent": pat_sz, "patent_total": pat_total,
        "paper": int(paper["sz"] or 0), "paper_total": int(paper["n"]),
        "scholar": int(scholar["sz"] or 0), "scholar_total": int(scholar["n"]),
        "org": int(org["sz"] or 0), "org_total": int(org["n"]),
        "inst": int(inst["sz"] or 0), "inst_total": int(inst["n"]),
        "fund": int(fund["sz"] or 0), "fund_total": int(fund["n"]),
        "policy": int(policy["sz"] or 0), "policy_total": int(policy["n"]),
    }

    board = [
        dict(id="SZ01", dim="专利", name="深圳专利（第一申请人名称含深圳）",
             value=sz["patent"], unit="件", total=sz["patent_total"],
             share=round(sz["patent"] / sz["patent_total"], 4),
             source="patent_panel_innov_20261021.app_year", status="可算",
             note="2021–2024 面板全量 2,424,684 行；深圳 914,253 件（31.0%），"
                  "年度 23.7/22.6/23.1/22.0 万件。2025–2026 只有全库年度合计，"
                  "无申请人分年明细，故本格窗口截至 2024。"),
        dict(id="SZ02", dim="论文", name="深圳论文（作者机构含深圳）",
             value=sz["paper"], unit="篇", total=sz["paper_total"],
             share=round(sz["paper"] / sz["paper_total"], 4),
             source="gkx.dwd_zh_paper.author_info_list", status="可算",
             note="2015–2026 年度 219→3,989→357 篇；2024 年 3,989 篇为批量补录尖峰，"
                  "是 2023 年 735 篇的 5.43 倍，趋势图须标注断点。"),
        dict(id="SZ03", dim="期刊", name="期刊数（无城市归属）",
             value=int(journal["n"]), unit="种", total=int(journal["n"]), share=None,
             source="gkx.dwd_zh_journal", status="部分",
             note="2,796 种期刊表内无 city/province 字段，无法出「深圳期刊数」；"
                  "且 paper_nums 为外部口径（单刊最高 650,715 篇），与本地论文表不符，"
                  "只能给全国期刊总量，不能进深圳看板分子。"),
        dict(id="SZ04", dim="学者", name="深圳学者（所属机构含深圳）",
             value=sz["scholar"], unit="人", total=sz["scholar_total"],
             share=round(sz["scholar"] / sz["scholar_total"], 4),
             source="gkx.dwd_scholar.scholar_org_name_zh", status="部分",
             note="2.13 万学者主档中仅 194 人机构名含深圳（0.91%）；学者主档与人才属性表"
                  "ID 交集仅 8.72%，不能把属性表 20,030 人当分母。"),
        dict(id="SZ05", dim="会议", name="学术会议数",
             value=None, unit="场", total=None, share=None,
             source="无承载表", status="不可算",
             note=f"gkx 元数据检索 conference/meeting 命中 {len(conf)} 张表，无会议表，"
                  "也无会议-城市字段，需求侧的「会议」维度整体缺承载。"),
        dict(id="SZ06", dim="机构", name="深圳创新机构",
             value=sz["org"], unit="家", total=sz["org_total"],
             share=round(sz["org"] / sz["org_total"], 4),
             source="gkx.dwd_org_base_info.city + dwd_research_institute_base_info.city",
             status="可算",
             note=f"企业底册 95,600 家；科研机构 1,014 家（底册仅 2,074 家且 100% 在广东，"
                  f"深圳占 {sz['inst'] / sz['inst_total']:.2%}）。"),
        dict(id="SZ07", dim="项目", name="深圳承担项目数",
             value=None, unit="项", total=int(project["n"]), share=None,
             source="gkx.dwd_zh_project", status="不可算",
             note=f"58,453 条项目 funded_institution 与 funded_province 均 100% 为空"
                  f"（{int(project['inst_null'])}/{int(project['n'])}），无法归属到深圳；"
                  "项目级别字段恒为「国家级」，也不能用级别替代属地。"),
        dict(id="SZ08", dim="主题", name="深圳技术主题数",
             value=None, unit="个", total=int(topic["n"]), share=None,
             source="gkx.dwd_industry_analysis_topics", status="不可算",
             note=f"表内 {int(topic['n'])} 行但 topic_name 只有 {int(topic['d'])} 个不同值，"
                  "是字典残片而非主题识别结果；无城市字段，无法出深圳主题。"),
        dict(id="SZ09", dim="基金", name="深圳产业基金数",
             value=sz["fund"], unit="支", total=sz["fund_total"],
             share=round(sz["fund"] / sz["fund_total"], 4),
             source="gkx.dwd_industrial_fund_basic_info.reg_region", status="可算",
             note="reg_region 为中国-广东省-深圳市-XX区；未披露区县 209 支，南山 181、福田 96。"),
        dict(id="SZ10", dim="政策", name="深圳政策数",
             value=sz["policy"], unit="条", total=sz["policy_total"],
             share=round(sz["policy"] / sz["policy_total"], 4),
             source="gkx.dwd_policy_base.city", status="可算",
             note="20,000 行采集上限；theme/keywords/quote_policy 三列 99.99% 为字面 'NULL'，"
                  "政策主题分析不可用，只能出条数与类型。"),
        dict(id="SZ11", dim="基础设施/载体", name="深圳创新载体数",
             value=None, unit="家", total=None, share=None,
             source="无可靠承载表", status="不可算",
             note="gkx 无载体表；live 侧 enterprise_innovation_carrier 47,620 行全部"
                  "create_time=2026-10-19 单批、名称仅 28,826 种，属模板数据，"
                  "按数据质量规则排除，不给分子。"),
    ]

    status_count = {}
    for b in board:
        status_count[b["status"]] = status_count.get(b["status"], 0) + 1

    out = {
        "metric_id": "M_INNOV_KPI_BOARD_SZ",
        "metric_name": "深圳科技发展指标看板",
        "formula_owner": "本批 agent 重建（看板类聚合，需求未给公式）",
        "run_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "nature": "看板 = 11 个科技维度的属地读面，不是单一公式；"
                  "与全国版 M_INNOV_KPI_BOARD 的分母、口径、用途均不同",
        "vs_national_board": {
            "national": "全库总量 + 全球监测六大子功能分格（20 格）",
            "shenzhen": "深圳属地子集 + 11 个科技维度（11 格）",
            "shared_tables": ["dwd_patent", "dwd_zh_paper", "dwd_policy_base",
                              "dwd_org_base_info", "dwd_zh_journal"],
            "do_not_mix": "全国版专利 2,939,895 件不能直接当深圳分母；"
                          "深圳版专利 914,253 件是 2021–2024 面板中 first_applicant_name 含「深圳」的子集，"
                          "两版数字不可比。",
        },
        "board": board,
        "summary": {
            "n_cells": len(board),
            "status_count": status_count,
            "computable": [b["id"] for b in board if b["status"] == "可算"],
            "partial": [b["id"] for b in board if b["status"] == "部分"],
            "not_computable": [b["id"] for b in board if b["status"] == "不可算"],
            "computable_share": round(status_count.get("可算", 0) / len(board), 4),
        },
        "time_series": {
            "patent_sz_year": sz_pat_year,
            "paper_sz_year": paper_year,
            "policy_sz_year": policy_year,
        },
        "probes": {
            "patent_rows": pat_total, "patent_value_notnull": None,
            "paper_rows": sz["paper_total"], "scholar_rows": sz["scholar_total"],
            "journal_rows": int(journal["n"]), "org_rows": sz["org_total"],
            "inst_rows": sz["inst_total"], "fund_rows": sz["fund_total"],
            "policy_rows": sz["policy_total"], "project_rows": int(project["n"]),
            "topic_rows": int(topic["n"]), "carrier_rows": None,
        },
        "support_judgment": {
            "data_support_level": "部分支持",
            "criteria": {
                "structure": "11 维中 5 维有真实属地字段（专利/论文/机构/基金/政策），"
                             "2 维只有全国面（期刊/学者），4 维无可靠承载（会议/项目/主题/载体）",
                "volume": f"深圳专利 {sz['patent']:,} 件、论文 {sz['paper']:,} 篇、"
                          f"政策 {sz['policy']} 条、基金 {sz['fund']} 支、"
                          f"企业 {sz['org']:,} 家",
                "reproducible": True,
                "discriminative": "专利年度 22-24 万件、论文 2024 年 3,989 篇尖峰，"
                                  "均有真实波动",
                "but": "会议维度无表；项目/主题无城市归属；期刊与学者属地覆盖 <1%；"
                       "载体无可靠承载，看板 11 格中 4 格不可算。",
            },
            "reason": "可算格均落在真实源表且有属地字段；不可算格是「字段/承载缺失」而非「算法难」，"
                      "故整体判部分支持，不能宣称深圳看板已可整体交付。",
        },
        "elapsed_sec": round(time.time() - t0, 1),
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str),
                   encoding="utf-8")
    print(json.dumps(out["summary"], ensure_ascii=False, indent=1))
    print(json.dumps(sz, ensure_ascii=False))
    print(json.dumps(out["time_series"], ensure_ascii=False))
    print("written", OUT.name, out["elapsed_sec"], "s")


if __name__ == "__main__":
    main()

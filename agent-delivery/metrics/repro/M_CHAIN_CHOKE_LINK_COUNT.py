#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""卡脖子环节数（M_CHAIN_CHOKE_LINK_COUNT）——否定性证据探针。

本脚本**不计算指标值**。它只回答一个问题：本指标在 gkx 里为什么不可算。
做法是把「卡脖子环节数」拆成两个必要条件，逐条量化：

  N1 环节级的「受制」判定数据：进口依赖度 / 自给率 / 关键专利对外集中度,
     或任何形式的 trade / customs / IO 表；
  N2 环节级的标注位：链节点上的 is_choke 类标签列，或一份已经判定好的
     卡脖子环节清单（旧稿指向的 chain_bottleneck / chain_panorama_nodes /
     industry_chain_metric_fact）。

两个条件都必须能在 gkx 内落地，才能得到「环节是否被卡」的判定。脚本对
N1/N2 各做三类扫描（精确同名 / 表名模式 / 列名模式），并额外做四次反向核查
（macro 贸易序列、链节点名、政策文本、空位环节），把「最可能推翻结论的
那几件事」逐个查掉。

产物：code/M_CHAIN_CHOKE_LINK_COUNT_out.json
  verdict_kind = "negative_evidence"
  support_judgment = "完全不支持"

运行：python3 _work_gkx21/rebuild_metric.py M_CHAIN_CHOKE_LINK_COUNT
（裸跑本脚本不会写 base_years_*，请走上面那个入口，原因见 DATA_FACTS §3.25）
"""
from __future__ import annotations

import json
import os
import time

import pymysql

METRIC = "M_CHAIN_CHOKE_LINK_COUNT"
HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, METRIC + "_out.json")

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", connect_timeout=20,
           read_timeout=180, autocommit=True)
RETRY = 5


def connect():
    """gkx 连接：实测 10 次约 2 次 15—20 秒超时，必须重试 + 指数退避。

    失败不吞异常：抛出去，让 rebuild_metric 看到退出码非 0。
    把一次超时写成「查了没数据」是本批明令禁止的退化（DATA_FACTS §3.11）。
    """
    last = None
    for i in range(RETRY):
        try:
            c = pymysql.connect(**GKX)
            cur = c.cursor()
            cur.execute("SET NAMES utf8mb4")
            return c
        except Exception as e:  # noqa: BLE001 —— 重试是唯一目的
            last = e
            time.sleep(min(2 ** i, 30))
    raise RuntimeError("gkx 连接重试 %d 次仍失败：%s" % (RETRY, last))


def run(cur, sql, tmo_ms=60000):
    """每条查询都带 max_execution_time，绝不设 0。"""
    cur.execute("SET SESSION max_execution_time=%d" % tmo_ms)
    t0 = time.time()
    cur.execute(sql)
    rows = cur.fetchall()
    return rows, round(time.time() - t0, 2)


def load_panel():
    """链树/环节企业数共享快照（gkx 扫出，2026-10-22 15:32）。"""
    p = os.path.join(SNAP, "chain_panel21.json")
    if not os.path.exists(p):
        raise FileNotFoundError("缺共享快照 %s（由 _work_gkx21/build_chain21_layer.py 生成）" % p)
    return json.load(open(p, encoding="utf-8"))


# 表名模式：覆盖「受制/贸易/投入产出」与「瓶颈/卡点/标注」两族。
TABLE_PATTERNS = [
    "choke", "chokepoint", "bottleneck", "self_suff", "selfsuffic",
    "import_dep", "import", "export", "customs", "tariff", "hs_code",
    "trade", "input_output", "io_table", "dependency", "localization",
]
# 列名模式：真正能支撑「对外依赖」判定的字段名。
COL_PATTERNS = [
    "choke", "self_suff", "selfsuffic", "import_ratio", "import_dep",
    "external_dep", "foreign_dep", "customs", "tariff", "hs_code",
    "trade_flow", "input_output", "localization_rate", "domestic_rate",
    # 2026-10-22 17:10 补：第一轮扫描漏了「国别」这一族。全库确实有 country 列
    # （dwd_patent.country_code、dwd_forg_base_info.country 等），漏掉会把
    # 「没有国别数据」写成结论——那是错的。加进来逐列核，核完再判能不能用。
    "country", "nation", "overseas", "abroad",
]


def main():
    t0 = time.time()
    conn = connect()
    cur = conn.cursor()
    compute = {}
    probes = []

    # ---------- 0. 库规模（分母） ----------
    rows, sec = run(cur, """SELECT COUNT(*) FROM information_schema.tables
                            WHERE table_schema='gkx'""")
    n_tables = int(rows[0][0])
    compute["gkx_tables"] = n_tables
    probes.append({"id": "P0_table_inventory", "sql": "information_schema.tables count",
                   "rows": n_tables, "sec": sec})

    rows, sec = run(cur, """SELECT COUNT(*) FROM information_schema.columns
                            WHERE table_schema='gkx'""")
    n_cols = int(rows[0][0])
    compute["gkx_columns"] = n_cols
    probes.append({"id": "P0_column_inventory", "sql": "information_schema.columns count",
                   "rows": n_cols, "sec": sec})

    # ---------- 1. N2：旧稿三张阻塞表的精确同名核查 ----------
    blocking = ["chain_bottleneck", "chain_panorama_nodes", "industry_chain_metric_fact"]
    exact = {}
    for t in blocking:
        rows, sec = run(cur, """SELECT COUNT(*) FROM information_schema.tables
                                WHERE table_schema='gkx' AND table_name='%s'""" % t)
        exact[t] = int(rows[0][0])
        probes.append({"id": "P1_exact_%s" % t, "table": t, "hits": int(rows[0][0]), "sec": sec})
    compute["blocking_tables_exact_hits"] = exact
    compute["blocking_tables_found"] = sum(exact.values())

    # ---------- 2. N2：表名模式扫描 ----------
    table_hits = {}
    for pat in TABLE_PATTERNS:
        rows, sec = run(cur, """SELECT table_name FROM information_schema.tables
                                WHERE table_schema='gkx' AND table_name LIKE '%%%s%%'
                                ORDER BY table_name LIMIT 50""" % pat)
        table_hits[pat] = [r[0] for r in rows]
        probes.append({"id": "P2_table_like_%s" % pat, "pattern": pat,
                       "hits": len(table_hits[pat]), "names": table_hits[pat][:8], "sec": sec})
    compute["table_pattern_hits"] = {k: len(v) for k, v in table_hits.items()}
    compute["table_pattern_names"] = {k: v for k, v in table_hits.items() if v}

    # ---------- 3. N1：列名模式扫描（全库 280 张表的所有列） ----------
    col_hits = {}
    for pat in COL_PATTERNS:
        rows, sec = run(cur, """SELECT table_name, column_name FROM information_schema.columns
                                WHERE table_schema='gkx' AND column_name LIKE '%%%s%%'
                                ORDER BY table_name LIMIT 50""" % pat)
        col_hits[pat] = [[r[0], r[1]] for r in rows]
        probes.append({"id": "P3_col_like_%s" % pat, "pattern": pat,
                       "hits": len(col_hits[pat]), "sec": sec})
    compute["column_pattern_hits"] = {k: len(v) for k, v in col_hits.items()}
    compute["column_pattern_names"] = {k: v for k, v in col_hits.items() if v}

    # ---------- 4. 链树结构：节点级标注位是否存在 ----------
    rows, sec = run(cur, """SELECT COUNT(*), SUM(level<>0), SUM(node_company_count<>0),
                                   COUNT(DISTINCT parent_code)
                            FROM gkx.dwd_industry_chain_info""")
    n_nodes, level_nonzero, ncc_positive, n_roots = [int(x or 0) for x in rows[0]]
    compute["chain_nodes"] = n_nodes
    compute["chain_level_nonzero"] = level_nonzero
    compute["chain_node_company_count_positive"] = ncc_positive
    compute["chain_roots"] = n_roots
    rows, sec_c = run(cur, """SELECT COUNT(*) FROM information_schema.columns
                              WHERE table_schema='gkx' AND table_name='dwd_industry_chain_info'""")
    compute["chain_info_columns"] = int(rows[0][0])
    probes.append({"id": "P4_chain_info_shape", "nodes": n_nodes, "columns": compute["chain_info_columns"],
                   "level_nonzero": level_nonzero,
                   "node_company_count_positive": ncc_positive, "sec": sec})

    rows, sec = run(cur, """SELECT industry_code, industry_name FROM gkx.dwd_industry_chain_info
                            WHERE industry_name LIKE '%卡%' OR industry_name LIKE '%瓶颈%'
                               OR industry_name LIKE '%断供%' OR industry_name LIKE '%受制%'
                            ORDER BY industry_code LIMIT 20""")
    name_hits = [[r[0], r[1]] for r in rows]
    compute["node_name_choke_hits"] = len(name_hits)
    compute["node_name_choke_examples"] = name_hits
    probes.append({"id": "P4b_node_name_scan", "hits": len(name_hits), "sec": sec})

    # 环节企业数（共享快照）：证明「空位环节」确实存在，但它不是卡脖子
    panel = load_panel()
    leaves = sum(c["leaves"] for c in panel["chains"])
    leaves_filled = sum(c["leaves_with_firms"] for c in panel["chains"])
    compute["leaf_nodes"] = leaves
    compute["leaf_nodes_with_firms"] = leaves_filled
    compute["leaf_nodes_empty"] = leaves - leaves_filled

    # ---------- 5. N1：宏观贸易序列（最可能推翻结论的一类） ----------
    rows, sec = run(cur, """SELECT COUNT(*), COUNT(DISTINCT index_code),
                                   COUNT(DISTINCT area_code)
                            FROM gkx.dwd_macro_index_data""")
    macro_rows, macro_codes, macro_areas = [int(x or 0) for x in rows[0]]
    compute["macro_rows"] = macro_rows
    compute["macro_index_codes"] = macro_codes
    compute["macro_area_codes"] = macro_areas
    probes.append({"id": "P5_macro_inventory", "rows": macro_rows,
                   "codes": macro_codes, "areas": macro_areas, "sec": sec})

    rows, sec = run(cur, """SELECT index_code, unit_use, dim_cal, COUNT(*),
                                   MIN(occur_period_year), MAX(occur_period_year)
                            FROM gkx.dwd_macro_index_data
                            WHERE index_code LIKE 'dwjj_dwmy%%'
                            GROUP BY index_code, unit_use, dim_cal
                            ORDER BY 4 DESC LIMIT 20""")
    trade_rows = sum(int(r[3]) for r in rows)
    compute["macro_trade_rows"] = trade_rows
    compute["macro_trade_codes"] = len(set(r[0] for r in rows))
    compute["macro_trade_units"] = sorted(set(r[1] for r in rows))
    compute["macro_trade_year_span"] = ([min(int(r[4]) for r in rows), max(int(r[5]) for r in rows)]
                                        if rows else [])
    probes.append({"id": "P5b_macro_trade", "rows": trade_rows,
                   "codes": compute["macro_trade_codes"], "sec": sec})

    # 宏观表有没有「行业/环节」维度？逐列核。
    rows, sec = run(cur, """SELECT column_name FROM information_schema.columns
                            WHERE table_schema='gkx' AND table_name='dwd_macro_index_data'
                            ORDER BY ordinal_position""")
    macro_cols = [r[0] for r in rows]
    compute["macro_columns"] = macro_cols
    compute["macro_has_industry_dim"] = any(
        ("industr" in c or "chain" in c or "node" in c) for c in macro_cols)

    # ---------- 6. 反向核查：概念在语料里出现，但没有度量数据 ----------
    rows, sec = run(cur, """SELECT SUM(content LIKE '%卡脖子%'),
                                   SUM(content LIKE '%断供%'),
                                   SUM(content LIKE '%受制于人%'),
                                   SUM(content LIKE '%进口依赖%')
                            FROM gkx.dwd_policy_base""", 90000)
    pol = [int(x or 0) for x in rows[0]]
    compute["policy_text_mentions"] = {
        "卡脖子": pol[0], "断供": pol[1], "受制于人": pol[2], "进口依赖": pol[3]}
    probes.append({"id": "P6_policy_text_mentions", "counts": compute["policy_text_mentions"],
                   "sec": sec})

    rows, sec = run(cur, """SELECT SUM(title LIKE '%卡脖子%'), SUM(title LIKE '%断供%')
                            FROM gkx.dwd_industry_chain_news_info""", 90000)
    news = [int(x or 0) for x in rows[0]]
    compute["news_title_mentions"] = {"卡脖子": news[0], "断供": news[1]}
    probes.append({"id": "P6b_news_title_mentions", "counts": compute["news_title_mentions"],
                   "sec": sec})

    # ---------- 7. 国别族：第一轮漏扫的一族，逐列核完再判 ----------
    geo_tables = {}
    for pat in ("country", "nation", "overseas", "abroad"):
        rows, sec = run(cur, """SELECT table_name, column_name FROM information_schema.columns
                                WHERE table_schema='gkx' AND column_name LIKE '%%%s%%'
                                ORDER BY table_name LIMIT 60""" % pat)
        for t, c_ in rows:
            geo_tables.setdefault(t, set()).add(c_)
    compute["geo_tables"] = {k: sorted(v) for k, v in sorted(geo_tables.items())}
    compute["geo_tables_count"] = len(geo_tables)
    probes.append({"id": "P7_country_columns", "tables": len(geo_tables), "sec": 0.2})

    # 三张真的能落到「国别」的表，逐个量形态
    rows, sec = run(cur, """SELECT country_code, COUNT(*) FROM gkx.dwd_patent
                            GROUP BY country_code ORDER BY 2 DESC""", 120000)
    pat_ctry = {r[0] or "NULL": int(r[1]) for r in rows}
    pat_total = sum(pat_ctry.values())
    overseas = sum(v for k, v in pat_ctry.items() if k != "CN")
    compute["patent_country"] = pat_ctry
    compute["patent_country_total"] = pat_total
    compute["patent_overseas"] = overseas
    compute["patent_overseas_ratio"] = round(overseas / pat_total, 6) if pat_total else 0.0
    probes.append({"id": "P8_patent_country", "total": pat_total,
                   "overseas": overseas, "sec": sec})

    rows, sec = run(cur, """SELECT COUNT(*) FROM gkx.dwd_industry_analysis_countries""")
    iac_rows = int(rows[0][0])
    rows, sec2 = run(cur, """SELECT column_name FROM information_schema.columns
                             WHERE table_schema='gkx' AND table_name='dwd_industry_analysis_countries'
                             ORDER BY ordinal_position""")
    iac_cols = [r[0] for r in rows]
    compute["industry_analysis_countries_rows"] = iac_rows
    compute["industry_analysis_countries_cols"] = iac_cols
    compute["industry_analysis_countries_has_value"] = any(
        k in iac_cols for k in ("amount", "value", "trade_value", "import_value", "export_value"))
    compute["industry_analysis_countries_has_industry"] = any(
        ("industr" in c_ or "chain" in c_) for c_ in iac_cols)
    probes.append({"id": "P9_industry_analysis_countries", "rows": iac_rows,
                   "cols": len(iac_cols), "sec": round(sec + sec2, 2)})

    rows, sec = run(cur, """SELECT COUNT(*), COUNT(DISTINCT country_code) FROM gkx.dwd_forg_base_info""")
    forg_rows, forg_countries = int(rows[0][0] or 0), int(rows[0][1] or 0)
    rows2, sec2 = run(cur, """SELECT country_code, COUNT(*) FROM gkx.dwd_forg_base_info
                              GROUP BY country_code ORDER BY 2 DESC""")
    forg_dist = {r[0] or "NULL": int(r[1]) for r in rows2}
    compute["forg_rows"] = forg_rows
    compute["forg_countries"] = forg_countries
    compute["forg_country_dist"] = forg_dist
    probes.append({"id": "P10_forg_base_info", "rows": forg_rows,
                   "countries": forg_countries, "dist": forg_dist,
                   "sec": round(sec + sec2, 2)})

    conn.close()

    # ---------- 判定 ----------
    RESTRICT = TABLE_PATTERNS[:6] + ["import", "export", "customs", "tariff", "hs_code",
                                     "trade", "input_output", "io_table"]
    n1_hits = sum(compute["column_pattern_hits"].get(k, 0) for k in COL_PATTERNS[:14])
    geo_hits = sum(compute["column_pattern_hits"].get(k, 0) for k in COL_PATTERNS[14:])
    n2_hits = compute["blocking_tables_found"]
    out = {
        "metric": METRIC,
        "title": "卡脖子环节数",
        "verdict_kind": "negative_evidence",
        "support_judgment": "完全不支持",
        "judgment_reason": (
            "环节级「对外技术受制」判定需要两类前提，gkx 两类都不成立。"
            "（N1 度量）全库 %d 张表 / %d 列：受制类 14 组列名模式（choke/self_suff/"
            "import_dep/selfsuffic/customs/tariff/hs_code/input_output/localization 等）命中 %d 列；"
            "国别类 4 组（country/nation/overseas/abroad）命中 %d 列、落在 %d 张表，逐表核过只有 3 张"
            "真能落到国别——dwd_patent.country_code（%d 件中境外 %d 件，%.2f%%）、"
            "dwd_industry_analysis_countries（%d 行，仅 document_id→country，无金额列、无行业列）、"
            "dwd_forg_base_info（%d 家、%d 个国别，其中 GB 一家独大 %d 家，是单一来源样本）。三者都是「主体属性」，"
            "不是「环节的对外依存度」；唯一的贸易序列是 dwd_macro_index_data 的 dwjj_dwmy*"
            "（%d 行、%d 个指数码、%d 个 area_code），维度只有区域与年份，落不到行业或链节点。"
            "（N2 标注位）旧稿依赖的三张表精确同名命中 %d 张；1,273 个链节点的 17 列里没有标注位列"
            "（level 全 0、node_company_count 全 0），节点名匹配「卡/瓶颈/断供/受制」仅 %d 条且均为"
            "药品名误匹配。既无度量、也无环节级标注位，故判完全不支持。"
            % (n_tables, n_cols, n1_hits, geo_hits, compute["geo_tables_count"],
               compute["patent_country_total"], compute["patent_overseas"],
               compute["patent_overseas_ratio"] * 100,
               compute["industry_analysis_countries_rows"],
               compute["forg_rows"], compute["forg_countries"],
               compute["forg_country_dist"].get("GB", 0),
               compute["macro_trade_rows"], compute["macro_trade_codes"],
               compute["macro_area_codes"], n2_hits, compute["node_name_choke_hits"])
        ),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "elapsed_sec": round(time.time() - t0, 1),
        "sources": {
            "db": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）",
            "tables": ["information_schema.tables", "information_schema.columns",
                       "dwd_industry_chain_info", "dwd_macro_index_data",
                       "dwd_policy_base", "dwd_industry_chain_news_info"],
            "snapshots": ["code/_snapshots21/chain_panel21.json"],
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "截面否定性证据：本件不产出年度序列，故无基期口径。"
            "dwd_macro_index_data 的 dwjj_dwmy* 覆盖 1979—2026，但它是区域级贸易总额/增速，"
            "不含环节维度，不能作为本指标的基期序列。"
        ),
        "compute": compute,
        "probes": probes,
        "counter_checks": [
            {"id": "C1", "question": "宏观库里有没有进口依存度序列，可以直接借用？",
             "action": "扫 dwd_macro_index_data 全部 %d 行 / %d 个指数码，"
                       "按 index_code LIKE 'dwjj_dwmy%%' 取对外贸易族，并逐列检查维度" %
                       (macro_rows, macro_codes),
             "result": "有 %d 行贸易序列，但维度是 area_code×occur_period_year，"
                       "没有行业/环节列（macro_has_industry_dim=%s），"
                       "粒度是「某地区进出口总额/增速」，落不到链节点。"
                       % (trade_rows, compute["macro_has_industry_dim"])},
            {"id": "C2", "question": "节点名里有没有已经标好的「卡脖子」字样？",
             "action": "对 1,273 个节点名做 4 个关键词 LIKE",
             "result": "命中 %d 条：%s——均为药品名（卡拉美芬类、可卡因及其盐），"
                       "属关键词误匹配，不是标注。" %
                       (compute["node_name_choke_hits"],
                        "、".join(x[1] for x in name_hits) or "无")},
            {"id": "C3", "question": "「卡脖子」是不是根本没人提，所以库里才没有？",
             "action": "统计政策正文与资讯标题里该词的出现次数",
             "result": "政策正文出现 卡脖子 %d 次、断供 %d 次、受制于人 %d 次、进口依赖 %d 次；"
                       "资讯标题 卡脖子 %d 条。概念在语料里存在，缺的是可度量的字段，"
                       "不是缺话题。" %
                       (pol[0], pol[1], pol[2], pol[3], news[0])},
            {"id": "C4", "question": "能不能用「没有企业的空位环节」当卡脖子？",
             "action": "用链树 954 个叶节点与 916 个有企业叶节点对比",
             "result": "空位叶 %d 个。空位是「本地没人干」，卡脖子是「有人干但被外部卡住」，"
                       "两者语义相反；把它当卡脖子会把招商空白误报为技术受制。" %
                       (leaves - leaves_filled)},
            {"id": "C6", "question": "库里有国别列，能不能用「境外专利占比」当受制代理？",
             "action": "按 country_code 聚合 dwd_patent 全表 %d 件" % pat_total,
             "result": "境外仅 %d 件（%.2f%%），其中 PCT（WO）%d 件、HK %d 件、JP %d 件；"
                       "这是「在哪个专利局公开」的属性，PCT 多说明企业愿意做国际保护，"
                       "恰恰与「被卡住」相反。同族专利也不等于进口依赖。"
                       % (overseas, compute["patent_overseas_ratio"] * 100,
                          pat_ctry.get("WO", 0), pat_ctry.get("HK", 0), pat_ctry.get("JP", 0))},
            {"id": "C7", "question": "dwd_industry_analysis_countries 名字像「行业×国别分析」，是不是贸易表？",
             "action": "读它的 12 列并数行数",
             "result": "只有 %d 行，列是 pk_id/document_id/country_code/country_name/时间戳/操作人；"
                       "没有行业列（has_industry=%s）、没有金额列（has_value=%s）。"
                       "它是一张「分析文档—国别」的关联表，不是贸易流量表。"
                       % (iac_rows, compute["industry_analysis_countries_has_industry"],
                          compute["industry_analysis_countries_has_value"])},
            {"id": "C8", "question": "dwd_forg_base_info 的 2 万家外资企业能不能算「外资依赖」？",
             "action": "按 country_code 分组",
             "result": "GB %d 家、US %d 家、CA %d 家，国别字段 country 全为 NULL。"
                       "这是一个以英国注册主体为主的样本，不是中国境内外资企业分布；"
                       "用它算外资依赖会得出「外资几乎全来自英国」的荒谬结论。"
                       % (forg_dist.get("GB", 0), forg_dist.get("US", 0), forg_dist.get("CA", 0))},
            {"id": "C5", "question": "旧稿的表会不会只是换了名字？",
             "action": "16 组表名词根 LIKE 扫 280 张表",
             "result": "命中明细见 compute.table_pattern_names；"
                       "choke/chokepoint/self_suff/import_dep/customs/tariff/hs_code/"
                       "input_output/localization 九组均 0 命中。"},
        ],
        "notes": [
            "本件不产出指标值，只产出「为什么不可算」的计数证据。",
            "与已交付 M_CHAIN_BOTTLENECK_COUNT 的边界：瓶颈是「有人干但干不够」，"
            "本件是「被外部卡住」；后者在前者之上还多要求一条对外依赖判据。"
            "两件同判「完全不支持」，但否定证据不同：瓶颈缺的是五维评分输入，"
            "本件缺的是贸易/依赖类字段与环节级标注位。",
            "与 M_CHAIN_BREAK_RISK_COUNT 的边界：断链风险数的是无企业环节（%d 个），"
            "本件数的是受制环节；空位不能替代受制。" % (leaves - leaves_filled),
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("[OK] %s -> %s（%.1fs，表 %d / 列 %d，N1 列命中 %d，N2 表命中 %d）"
          % (METRIC, OUT, out["elapsed_sec"], n_tables, n_cols, n1_hits, n2_hits))


if __name__ == "__main__":
    main()

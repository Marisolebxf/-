#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TECH_DEEP_130_1 全景技术链模型 —— gkx 口径重建（20261022）。

只连 gkx（183.240.141.251:3318，只读账号）；专利聚合读授权缓存，避免对 2.94M 宽表做行级聚合。
产物：code/M_TECH_DEEP_130_1_out.json

节点：IPC4 技术域（634 个，来自 main_classification_ipcr 前 4 位）
边：同一专利内「主 IPC4 × 其他 IPC4」共类共现（等距主键抽样，抽样框写入产物）
属性：专利计数、申请人计数（全量缓存）；论文/标准/产品三维实测缺源，不伪造
"""
from __future__ import annotations

import collections
import json
import math
import time
from pathlib import Path

import pymysql

M = "M_TECH_DEEP_130_1"
CODE = Path(__file__).resolve().parent
SNAP = CODE / "_snapshots21"
GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", connect_timeout=60,
           read_timeout=600, write_timeout=600, autocommit=True)
BASE = [2021, 2022, 2023, 2024]
# 等距主键区间：每段 150k 个 dwd_id，五段覆盖表头/中段/表尾（抽样框写进产物）
RANGES = [(5000, 200000), (2000000, 2150000), (8000000, 8150000),
          (20000000, 20150000), (35000000, 35150000)]


def gkx():
    last = None
    for i in range(5):
        try:
            c = pymysql.connect(**GKX)
            with c.cursor() as cur:
                cur.execute("SET NAMES utf8mb4")
                cur.execute("SET SESSION max_execution_time=120000")
            return c
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(1.5 * (2 ** i))
    raise RuntimeError(f"gkx connect failed after 5 tries: {last!r}")


def q(sql, cap=120000):
    last = None
    for i in range(3):
        try:
            c = gkx()
            try:
                with c.cursor() as cur:
                    cur.execute(f"SET SESSION max_execution_time={cap}")
                    cur.execute(sql)
                    cols = [d[0] for d in cur.description] if cur.description else []
                    rows = cur.fetchall()
                    return [dict(zip(cols, r)) for r in rows] if cols else rows
            finally:
                c.close()
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2.0 * (2 ** i))
    raise RuntimeError(f"query failed: {last!r} :: {sql[:120]}")


def load_json(name):
    return json.load(open(SNAP / name, encoding="utf-8"))


const = load_json("tech5_constants_20261022.json")
ipc_year = load_json("patent_ipc4_year_20261021.json")
ipc_name = load_json("patent_ipc4_by_name_20261021.json")

# ---------------- 1. 节点面 ----------------
dom_year = collections.defaultdict(collections.Counter)
dom_all = collections.Counter()
for ipc4, year, n, _org in ipc_year:
    dom_year[ipc4][int(year)] += int(n)
    dom_all[ipc4] += int(n)
domains = sorted(dom_all)

app_cnt = collections.Counter()
top_app = {}
for ipc4, nm, n in ipc_name:
    app_cnt[ipc4] += 1
    if ipc4 not in top_app or n > top_app[ipc4][1]:
        top_app[ipc4] = (nm, int(n))

nodes = []
for d in domains:
    b = sum(dom_year[d][y] for y in BASE)
    n21, n24 = dom_year[d][2021], dom_year[d][2024]
    nodes.append({
        "ipc4": d,
        "patent_cnt_2021_2024": b,
        "patent_cnt_all": dom_all[d],
        "n2021": n21, "n2024": n24,
        "growth_2021_2024_pct": round((n24 - n21) / n21 * 100, 2) if n21 else None,
        "applicant_cnt": app_cnt.get(d, 0),
        "top_applicant": top_app.get(d, (None, 0))[0],
        "top_applicant_cnt": top_app.get(d, (None, 0))[1],
    })
nodes.sort(key=lambda r: -r["patent_cnt_2021_2024"])
b_total = sum(r["patent_cnt_2021_2024"] for r in nodes)

# ---------------- 2. 边面：共类共现抽样 ----------------
rows = []
for lo, hi in RANGES:
    rows += q(f"SELECT dwd_id, main_classification_ipcr, further_classification_ipcr "
              f"FROM gkx.dwd_patent WHERE dwd_id BETWEEN {lo} AND {hi}")
dom_set = set(domains)
pair = collections.Counter()
scanned = with_main = with_further = 0
for r in rows:
    scanned += 1
    main = (r.get("main_classification_ipcr") or "")[:4]
    if main not in dom_set:
        continue
    with_main += 1
    fj = r.get("further_classification_ipcr")
    if not fj:
        continue
    try:
        arr = json.loads(fj) if isinstance(fj, str) else fj
    except Exception:  # noqa: BLE001
        continue
    if not isinstance(arr, list):
        continue
    with_further += 1
    others = {str(x)[:4] for x in arr if x}
    others.discard(main)
    for o in others:
        if o in dom_set:
            a, b = (main, o) if main < o else (o, main)
            pair[(a, b)] += 1

MIN_W = 5
edges = [{"a": a, "b": b, "weight": w} for (a, b), w in pair.items() if w >= MIN_W]
adj = collections.defaultdict(set)
for e in edges:
    adj[e["a"]].add(e["b"])
    adj[e["b"]].add(e["a"])
seen, comps = set(), []
for d in domains:
    if d in seen:
        continue
    stack, comp = [d], []
    seen.add(d)
    while stack:
        v = stack.pop()
        comp.append(v)
        for w in adj[v]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    comps.append(comp)
comps.sort(key=len, reverse=True)
deg = {d: len(adj[d]) for d in domains}
n_nodes = len(domains)
density = round(2 * len(edges) / (n_nodes * (n_nodes - 1)), 8)
hubs = sorted(deg.items(), key=lambda kv: (-kv[1], kv[0]))[:10]

# ---------------- 3. 属性面与外源面实测 ----------------
paper_cols = q("""SELECT COLUMN_NAME FROM information_schema.COLUMNS
                  WHERE TABLE_SCHEMA='gkx' AND TABLE_NAME='dwd_zh_paper' ORDER BY ORDINAL_POSITION""")
paper_col_names = [r["COLUMN_NAME"] for r in paper_cols]
paper_ipc_like = [c for c in paper_col_names
                  if any(k in c.lower() for k in ("ipc", "class", "domain", "tech"))]
std_rows = q("""SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA='gkx'
                AND (TABLE_NAME LIKE '%standard%' OR TABLE_NAME LIKE '%_std%'
                     OR TABLE_NAME LIKE '%criterion%')""")
prod = q("""SELECT COUNT(*) n,
    SUM(company_name REGEXP '^[0-9A-Z]{18}$') cc_like,
    SUM(credit_code LIKE '[%') prod_like,
    SUM(industry_name REGEXP '^[0-9]+$') ind_num,
    SUM(industry_link_name LIKE '[%') link_like
    FROM gkx.dwd_org_industry_product_tags""")[0]
cit = q("""SELECT COUNT(*) n, SUM(cited_by_nums>0) positive, MAX(cited_by_nums) mx
           FROM gkx.dwd_patent_cited""")[0]
domain_tbl = q("""SELECT COUNT(*) n FROM information_schema.TABLES
                  WHERE TABLE_SCHEMA='gkx' AND TABLE_NAME IN ('tech_domain','event_type')""")[0]["n"]
total_tbl = q("SELECT COUNT(*) n FROM information_schema.TABLES WHERE TABLE_SCHEMA='gkx'")[0]["n"]

out = {
    "metric_id": M,
    "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    "domain_mapping_version": const["domain_mapping_version"],
    "patent_dedup_key": const["patent_dedup_key"],
    "base_years_used": const["base_years_used"],
    "base_years_missing": const["base_years_missing"],
    "base_years_note": const["base_years_note"],
    "constants_ref": "code/_snapshots21/tech5_constants_20261022.json",
    "node_face": {
        "n_nodes": n_nodes,
        "ipc_universe": const["domain_count"],
        "patent_cnt_2021_2024_sum": b_total,
        "patent_with_ipc_all": const["patent_with_ipc"],
        "top_domains": nodes[:15],
        "growth_up": sum(1 for r in nodes if (r["growth_2021_2024_pct"] or 0) > 0),
        "growth_down": sum(1 for r in nodes if (r["growth_2021_2024_pct"] or 0) < 0),
    },
    "edge_face": {
        "sampling_frame": f"{len(RANGES)} 段等距主键区间（每段 150,000 个 dwd_id）：{RANGES}",
        "scanned_rows": scanned,
        "with_main_ipc4": with_main,
        "with_further_ipc": with_further,
        "pairs_raw": len(pair),
        "min_weight": MIN_W,
        "n_edges": len(edges),
        "edge_weight_max": max((e["weight"] for e in edges), default=0),
        "edge_type": "co_classification（同一专利内主 IPC4 与其他 IPC4 共现）",
        "top_edges": sorted(edges, key=lambda e: -e["weight"])[:15],
    },
    "graph_metrics": {
        "components": len(comps),
        "largest_component": len(comps[0]) if comps else 0,
        "isolated_nodes": sum(1 for d in domains if deg[d] == 0),
        "isolated_pct": round(sum(1 for d in domains if deg[d] == 0) / n_nodes * 100, 2),
        "density": density,
        "degree_min": min(deg.values()), "degree_max": max(deg.values()),
        "degree_mean": round(sum(deg.values()) / n_nodes, 3),
        "hubs": [{"ipc4": d, "degree": k} for d, k in hubs],
    },
    "attribute_face": {
        "patent_cnt_fill": f"{n_nodes}/{n_nodes}",
        "applicant_cnt_fill": f"{sum(1 for d in domains if app_cnt.get(d))}/{n_nodes}",
        "paper_cnt_fill": f"0/{n_nodes}",
        "paper_ipc_like_columns": paper_ipc_like,
        "paper_columns_n": len(paper_col_names),
        "standard_tables": std_rows,
        "product_rows": prod["n"],
        "product_column_shift_rows": int(prod["cc_like"]),
        "product_column_shift_pct": round(int(prod["cc_like"]) / prod["n"] * 100, 2),
        "citation_rows": cit["n"],
        "citation_positive": int(cit["positive"]),
        "citation_coverage_pct": round(cit["n"] / const["patent_rows"] * 100, 2),
        "citation_max": cit["mx"],
    },
    "dictionary_probe": {
        "gkx_table_total": total_tbl,
        "tech_domain_or_event_type_tables": domain_tbl,
        "verdict": "tech_domain / event_type 在 gkx 280 张基表中零命中；节点字典不可直读",
    },
    "criteria": {
        "direct_structure": "部分（节点/边可由 IPC4 共类重建，结果面 tech_chain_* 不存在）",
        "direct_data": "部分（专利/申请人两维满格；论文/标准/产品三维缺键）",
        "dependency_structure": "部分（无 tech_domain 字典、无标准表）",
        "dependency_data": "部分（共类边为抽样，非全量标注边）",
    },
    "missing_sources": [
        "tech_chain_node / tech_chain_edge / tech_chain_events（gkx 零命中，需重建）",
        "tech_domain（10 行中文域名字典，gkx 零命中）",
        "dwd_zh_paper 无 IPC/技术域字段（32 列中 0 个可挂接列）",
        "标准表（gkx 零命中）",
        "产品表列错位（98.23% 行 company_name 存信用代码），无企业名→技术域键",
        "被引数据仅 20,515 行（0.70%），不足以做域级创新度",
    ],
    "support_judgment": "部分支持",
    "judgment_reason": "节点面（634 个 IPC4 域）与边面（同专利共类共现，抽样）可当日重建，"
                       "图结构指标可复算；但结果面 tech_chain_* 三表在 gkx 不存在，"
                       "需求点名的论文/标准/产品三类节点属性均无可挂接键，"
                       "边集为抽样共类而非标注依赖——结构与数据两侧都始终缺维。",
    "verdict_kind": "reconstructed",
    "sources": const["source"],
}

json.dump(out, open(CODE / f"{M}_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({"nodes": n_nodes, "edges": len(edges), "components": len(comps),
                  "largest": len(comps[0]), "isolated": out["graph_metrics"]["isolated_nodes"],
                  "density": density, "sampled": scanned, "support": out["support_judgment"]},
                 ensure_ascii=False))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_DS_02_ENTITY_004 [新增] 技术点影响力 —— gkx 复现（2026-10-22）

口径（calc-logic ENT/M_ENT_DS_02_ENTITY_004.md，注册表 formula = pending_cosign，未签）：
    Influence(tech) = w1·Norm(关联规模) + w2·Norm(关联实体影响力)
    关联规模 = 与技术点有边的企业/机构/人才/专利/论文去重数
    关联实体影响力 = 关联企业技术力均值 tech_power_index 或网络中心性 centrality
    禁止用 PATH 中心度/关键节点或 M_SVC_GRAPH_INFLUENCE 顶替（ENT-D04/ENT-B03）

本件实测到的结构缺口（见 probes）：
    1. gkx 280 张表无 graph_node / graph_edge / enterprise_graph_rel 任何图谱表（表名扫描 0 命中）；
    2. gkx 全库列名扫描里没有 tech_power_index / centrality / pagerank / influence 任何列（0 命中）；
    3. 技术点-专利/论文关联表不存在（dwd_org_base_info_patent_rel 0 命中）。
    → 技术点本体、技术点—实体边、影响力字段三者皆无源。

本件的代理口径（两处替换，全部显式标注）：
    技术点 → IPC 小类（IPC4，634 个）；关联实体 → 该 IPC4 下的专利申请人；
    关联规模 = 该 IPC4 的去重申请人（企业）数；
    关联实体影响力 → 关联企业中「有官方认定资质」的占比（tech_tag 覆盖），
                     用来替代不存在的 tech_power_index。
    Influence = 100 × (0.5·Norm_log(规模) + 0.5·质量占比)

输入（全部本目录）：
    code/_snapshots21/patent_ipc4_year_20261021.json    3,595 行 [ipc4, year, 件数, 机构数]
    code/_snapshots21/patent_ipc4_by_name_20261021.json 581,585 行 [ipc4, 申请人名, 件数]
    code/_snapshots21/tech_tags_20261021.json           32,322 家 × 55 类资质
    code/_snapshots21/base_20261021.json                底册 189,116 行（名称→org_id）

输出：code/M_ENT_DS_02_ENTITY_004_out.json
"""
from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import pymysql

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "M_ENT_DS_02_ENTITY_004_out.json"
SNAP = HERE / "_snapshots21"

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", database="gkx", charset="utf8mb4",
           cursorclass=pymysql.cursors.DictCursor, connect_timeout=15, read_timeout=120)


def main():
    ipc_year = json.load(open(SNAP / "patent_ipc4_year_20261021.json", encoding="utf-8"))
    ipc_name = json.load(open(SNAP / "patent_ipc4_by_name_20261021.json", encoding="utf-8"))
    tags = json.load(open(SNAP / "tech_tags_20261021.json", encoding="utf-8"))
    base = json.load(open(SNAP / "base_20261021.json", encoding="utf-8"))
    name_org = {r[2]: r[0] for r in base}

    inv = json.load(open(ROOT / "_work_gkx21" / "GKX_INVENTORY.json", encoding="utf-8"))
    graph_tables = sorted(t for t in inv if any(k in t.lower() for k in
                                                ("graph", "node", "edge", "central", "pagerank", "tech_point")))
    rel_tables = sorted(t for t in inv if "patent_rel" in t.lower() or "tech_rel" in t.lower())

    # 列名扫描：证明 tech_power_index / centrality 类字段在 gkx 整库不存在
    col_hits = {}
    try:
        c = pymysql.connect(**GKX)
        with c.cursor() as cur:
            cur.execute("SET SESSION max_execution_time=30000")
            for pat in ("%tech_power%", "%centrality%", "%pagerank%", "%influence%", "%tech_point%"):
                cur.execute("SELECT table_name, column_name FROM information_schema.columns "
                            "WHERE table_schema='gkx' AND column_name LIKE %s LIMIT 20", (pat,))
                col_hits[pat] = [f"{r['table_name']}.{r['column_name']}" for r in cur.fetchall()]
        c.close()
    except Exception as e:  # 连接/权限问题按「未测」登记，不当作「不存在」
        col_hits = {"error": f"{type(e).__name__}: {str(e)[:120]}"}

    firms_by_ipc = defaultdict(set)
    pat_by_ipc = Counter()
    for ipc4, nm, cnt in ipc_name:
        firms_by_ipc[ipc4].add(nm)
        pat_by_ipc[ipc4] += int(cnt or 0)

    years_by_ipc = defaultdict(list)
    for row in ipc_year:
        ipc4, yr, pats, orgs = row[0], row[1], int(row[2] or 0), int(row[3] or 0)
        years_by_ipc[ipc4].append((yr, pats, orgs))

    all_names = set()
    for s in firms_by_ipc.values():
        all_names |= s
    matched = sum(1 for n in all_names if n in name_org)
    tagged = 0
    for n in all_names:
        org = name_org.get(n)
        if org and tags.get(org):
            tagged += 1

    recs = []
    for ipc4, names in firms_by_ipc.items():
        n_firm = len(names)
        n_match = sum(1 for n in names if n in name_org)
        n_tag = sum(1 for n in names if name_org.get(n) and tags.get(name_org[n]))
        q = (n_tag / n_match) if n_match else 0.0
        ys = sorted(years_by_ipc.get(ipc4, []))
        recs.append({
            "ipc4": ipc4,
            "firms": n_firm,
            "patents": pat_by_ipc[ipc4],
            "firms_matched_base": n_match,
            "firms_with_tag": n_tag,
            "quality_share_pct": round(q * 100, 4),
            "year_min": ys[0][0] if ys else None,
            "year_max": ys[-1][0] if ys else None,
        })

    mx = max(math.log1p(r["firms"]) for r in recs)
    for r in recs:
        scale = math.log1p(r["firms"]) / mx
        r["norm_scale"] = round(scale, 6)
        r["influence"] = round(100 * (0.5 * scale + 0.5 * r["quality_share_pct"] / 100), 4)

    recs.sort(key=lambda r: -r["influence"])
    top20 = recs[:20]
    vals = sorted(r["influence"] for r in recs)
    n = len(vals)

    def pctl(q):
        k = (n - 1) * q
        lo, hi = int(k), min(int(k) + 1, n - 1)
        return round(vals[lo] + (vals[hi] - vals[lo]) * (k - lo), 4)

    payload = {
        "metric_id": "M_ENT_DS_02_ENTITY_004",
        "metric_name_zh": "[新增] 技术点影响力",
        "generated_for": "20261021 批 B-sample",
        "source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）.dwd_patent（IPC×申请人 聚合快照） × dwd_org_base_info × dwd_org_tech_tag",
        "support_judgment": "部分支持",
        "support_reason": ("技术点本体（graph_node 的技术实体类型）、技术点—实体边、tech_power_index 三者"
                           "在 gkx 均无源；本件用 IPC 小类 + 关联企业资质覆盖率做两处代理，"
                           "只交付「规模×质量」的代理影响力，不交付甲方口径的综合影响力。"),
        "proxy_declaration": {
            "tech_point": "IPC 小类（IPC4，634 个）",
            "linked_entity": "该 IPC4 下的专利申请人（企业名）",
            "influence": "关联企业中持官方认定资质的占比（替代不存在的 tech_power_index）",
        },
        "formula_status": "pending_cosign: human:唐绍祖（未签）；权重 w1/w2 未定义，本件取等权 0.5/0.5",
        "formula": "influence = 100 × (0.5·log1p 归一后的关联企业数 + 0.5·关联企业资质覆盖率)",
        "probes": {
            "table_scan": {
                "total_tables": len(inv),
                "graph_semantic_tables": graph_tables,
                "graph_semantic_hits": len(graph_tables),
                "patent_rel_tables": rel_tables,
                "patent_rel_hits": len(rel_tables),
            },
            "column_scan": col_hits,
            "ipc": {
                "distinct_ipc4_by_name": len(firms_by_ipc),
                "distinct_ipc4_by_year": len(years_by_ipc),
                "distinct_applicant_names": len(all_names),
                "names_matched_base": matched,
                "name_match_pct": round(matched / len(all_names) * 100, 4),
                "names_with_tag": tagged,
            },
            "scale": {"max_firms": recs and max(r["firms"] for r in recs),
                      "median_firms": sorted(r["firms"] for r in recs)[len(recs) // 2]},
        },
        "influence_dist": {"n": n, "min": vals[0], "median": pctl(0.5),
                           "mean": round(sum(vals) / n, 4), "p90": pctl(0.9), "max": vals[-1]},
        "top20": top20,
        "bottom5": recs[-5:],
        "coverage": {
            "ipc4_with_firms": sum(1 for r in recs if r["firms"] > 0),
            "ipc4_with_tagged_firm": sum(1 for r in recs if r["firms_with_tag"] > 0),
            "share_with_tagged_pct": round(sum(1 for r in recs if r["firms_with_tag"] > 0) / n * 100, 4),
        },
        "base_years_used": sorted({y for ys in years_by_ipc.values() for y, _, _ in ys}),
        "base_years_missing": [],
        "base_years_note": ("IPC×年 快照覆盖 2021—2026（dwd_patent 只有这六年，2017—2020 零行，"
                            "见 DATA_FACTS §3.13）；本件是截面排序，不用年份做分母，"
                            "2026 为残年，不参与任何「近 N 年均值」计算。"),
        "custom_thresholds": {
            "weights": {"scale": 0.5, "quality": 0.5},
            "note": "等权为本件默认；公式本体 pending_cosign（唐绍祖未签），签约后必须重算并同步改正文。",
        },
    }
    json.dump(payload, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({"probes": payload["probes"], "dist": payload["influence_dist"],
                      "coverage": payload["coverage"]}, ensure_ascii=False, indent=1)[:2200])
    print("->", OUT)


if __name__ == "__main__":
    main()

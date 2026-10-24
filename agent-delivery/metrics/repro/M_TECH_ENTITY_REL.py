#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TECH_ENTITY_REL · 实体关联关系网（DS-02）

三类边（可现转）：
  1) 专利权转移   dwd_patent_transfer.transfer_before/after（有向，按 pn 聚合为多边）
  2) 共同申请     dwd_patent_applicants（同一 pn 多申请人 → 两两无向边）
  3) 论文机构合著 dwd_zh_paper.author_info_list（同篇多机构 → 两两无向边）
缺失：引用边（dwd_patent_cited 仅 0.70% 且 cited_by 多为 'null'）、许可/诉讼关系边。
输出：code/M_TECH_ENTITY_REL_out.json
"""
import json, re, statistics, sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots"
OUT = HERE / "M_TECH_ENTITY_REL_out.json"
SMALL = json.loads((SNAP / "tech_d_small_tables_20261021.json").read_text())

edges = Counter()
types_of = defaultdict(set)


def add_edge(a, b, typ, w=1):
    a, b = (a or "").strip(), (b or "").strip()
    if not a or not b or a == b or len(a) < 2 or len(b) < 2:
        return
    if a in ("null", "NULL") or b in ("null", "NULL"):
        return
    edges[(a, b, typ)] += w
    types_of[a].add(typ)
    types_of[b].add(typ)


def parse_names(s):
    if not s or s in ("null", "NULL"):
        return []
    try:
        arr = json.loads(s) if isinstance(s, str) else s
        if isinstance(arr, list):
            return [x.get("name") for x in arr if isinstance(x, dict) and x.get("name")]
    except Exception:
        pass
    return []


transfer_pairs = 0
for r in SMALL.get("transfer_rows") or []:
    if not isinstance(r, dict):
        continue
    before, after = parse_names(r.get("transfer_before")), parse_names(r.get("transfer_after"))
    if before and after:
        transfer_pairs += 1
        for a in before:
            for b in after:
                add_edge(a, b, "专利权转移")

by_pat = defaultdict(list)
for r in SMALL.get("applicants_rows") or []:
    if isinstance(r, dict):
        by_pat[r.get("patent_id")].append(r.get("name"))
coapp_pat = 0
for pid, names in by_pat.items():
    names = [x for x in dict.fromkeys(names) if x]
    if len(names) >= 2:
        coapp_pat += 1
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                add_edge(names[i], names[j], "共同申请")

papers_multi = 0
for r in SMALL.get("paper_rows") or []:
    if not isinstance(r, dict):
        continue
    try:
        arr = json.loads(r.get("author_info_list") or "[]")
    except Exception:
        continue
    insts = []
    for a in arr if isinstance(arr, list) else []:
        inst = (a.get("institution") or a.get("affiliation") or "").strip()
        if inst:
            insts.append(inst)
    insts = list(dict.fromkeys(insts))[:8]
    if len(insts) >= 2:
        papers_multi += 1
        for i in range(len(insts)):
            for j in range(i + 1, len(insts)):
                add_edge(insts[i], insts[j], "论文合著")

neigh = defaultdict(set)
for (a, b, t) in edges:
    neigh[a].add(b)
    neigh[b].add(a)
deg = {n: len(v) for n, v in neigh.items()}
deg_vals = sorted(deg.values())


def brand(n):
    n = re.sub(r"[（(].*?[)）]", "", n)
    n = re.sub(r"(股份)?有限公司$|集团$|公司$|厂$", "", n)
    return n


type_w, intra_w = Counter(), Counter()
for (a, b, t), w in edges.items():
    type_w[t] += w
    if brand(a) and brand(a) == brand(b):
        intra_w[t] += w

# 技术点切片：实体（该 IPC4 ≥2 件）诱导子图
ent_ipc = defaultdict(Counter)


def ipc4s(main, further):
    codes = []
    for s in [main] + (json.loads(further) if further and str(further) not in ("[]", "null", "NULL", "") else []):
        s = str(s or "").strip()
        if len(s) >= 4:
            codes.append(s[:4].upper())
    return list(dict.fromkeys(codes))


for line in (SNAP / "tech_d_patent_sample.jsonl").open(encoding="utf-8"):
    r = json.loads(line)
    nm = (r.get("first_applicant_name") or "").strip()
    if not nm or nm in ("NULL", "null", "无"):
        continue
    for c in ipc4s(r.get("main_classification_ipcr"), r.get("further_classification_ipcr")):
        ent_ipc[nm][c] += 1

scoped = {}
for tech in ("G06F", "G06N", "H01M", "H04W"):
    ent = {e for e, c in ent_ipc.items() if c.get(tech, 0) >= 2}
    sub = [(a, b, t, w) for (a, b, t), w in edges.items() if a in ent and b in ent]
    sub_nodes = {x for e in sub for x in (e[0], e[1])}
    scoped[tech] = {"entities_ge2": len(ent), "sub_nodes": len(sub_nodes), "sub_edges": len(sub),
                    "sub_types": dict(Counter(e[2] for e in sub)),
                    "density": round(len(sub) / max(1, len(sub_nodes) * (len(sub_nodes) - 1) / 2), 6)}

out = {
    "metric_id": "M_TECH_ENTITY_REL",
    "metric_name": "实体关联关系网",
    "domain": "DS-02",
    "formula_owner": "仿王惠 ai-1020（需求未给公式）",
    "source_used": "snapshot(gkx transfer 22,809 / applicants 28,964 / paper 20,000)",
    "generated_at": "2026-10-21",
    "network": {"n_nodes": len(deg), "n_edges_unique": len(edges), "n_edge_instances": sum(edges.values()),
                "n_types": len(type_w), "type_weight": dict(type_w),
                "type_unique": dict(Counter(k[2] for k in edges)),
                "intra_group_weight": dict(intra_w),
                "intra_group_share": {t: round(intra_w[t] / max(1, type_w[t]), 4) for t in type_w}},
    "degree": {"min": deg_vals[0], "p50": deg_vals[len(deg_vals) // 2], "p90": deg_vals[int(len(deg_vals) * 0.9)],
               "max": deg_vals[-1], "mean": round(statistics.mean(deg_vals), 3),
               "n_deg_ge5": sum(1 for d in deg_vals if d >= 5), "n_deg_ge20": sum(1 for d in deg_vals if d >= 20)},
    "scoped_subgraph": scoped,
    "top_edges": [{"a": a, "b": b, "type": t, "w": w}
                  for (a, b, t), w in sorted(edges.items(), key=lambda kv: -kv[1])[:25]],
    "top_nodes_by_neighbors": [{"entity": n, "neighbors": d, "types": sorted(types_of[n])}
                               for n, d in sorted(deg.items(), key=lambda kv: -kv[1])[:20]],
    "coverage": {"transfer_pairs": transfer_pairs, "coapp_patents": coapp_pat, "papers_multi_inst": papers_multi},
    "missing_edge_types": ["引用（cited 0.70%，cited_by 多为 'null'）", "许可（legal_events 2/2000）",
                           "诉讼（legal_events 0/2000）", "质押（10/2000）"],
    "support_judgment": {
        "data_support_level": "部分支持",
        "criteria": {"edge_types_present": 3, "edge_types_required": "需求含合作/引用/影响多类型",
                     "n_edges": len(edges), "n_nodes": len(deg),
                     "reproducible": True, "citation_edges": False, "license_edges": False},
        "note": "共同申请/专利转移/论文合著三类边可现转（3.9 万唯一边、6.6 万边实例、3.07 万节点），但引用/许可/诉讼边无数据，实体跨源同名未消歧、集团更名边占比偏高 → 部分支持",
    },
}
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str))
print(json.dumps({k: out[k] for k in ("network", "degree", "scoped_subgraph", "support_judgment")},
                 ensure_ascii=False, indent=1))
print("top edges:", [(e["a"], e["b"], e["type"], e["w"]) for e in out["top_edges"][:3]])
print("written:", OUT.name)

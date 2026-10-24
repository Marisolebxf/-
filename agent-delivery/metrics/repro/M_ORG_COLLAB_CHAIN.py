#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ORG_COLLAB_CHAIN · 科研合作关系链条

边源（本件与同域 M_ORG_DEEP_153_1 有意分工，见 out.json `vs_org_deep_153_1`）：
  E1 论文共同署名（机构-机构）：dwd_zh_paper.author_info_list 同一篇里出现 ≥2 家本底册机构
  E2 产学研共同署名（机构-企业）：同一篇里同时出现本底册机构与企业署名
本件**不用**学者级共著表（dwd_scholar_coauthor 1,187,606 条）——那是 153 件的底边来源。

链条（chain）定义：机构 E 企业 机构 的二跳路径，即「两家机构共同服务同一家企业」；
这是专利共申边缺失后唯一能支撑「链条」语义的结构（专利表 294 万行禁止聚合，见 §3.6）。

网络统计：节点数/边数/连通分量/密度/度与加权度/介数中心性（Brandes，图 <1,000 节点可精确算）。

零 SQL，只读面板。产物 `code/M_ORG_COLLAB_CHAIN_out.json`。
"""
from __future__ import annotations

import json
import os
import re
from collections import Counter, defaultdict, deque

import _org_family_common as C

MID = "M_ORG_COLLAB_CHAIN"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, f"{MID}_out.json")


def core_name(n):
    n = re.sub(r"\([^()]*\)", "", str(n or ""))
    n = re.sub(r"^(广东省|深圳市|广州市|东莞市|惠州市|中国|国家)", "", n)
    return re.sub(r"(有限责任公司|有限公司)$", "", n).strip()


def same_family(a, b):
    ca, cb = core_name(a), core_name(b)
    if not ca or not cb:
        return False
    if ca in b or cb in a:
        return True
    k = 0
    for x, y in zip(ca, cb):
        if x != y:
            break
        k += 1
    return k >= 6


def brandes(nodes, adj):
    """无权图的介数中心性（Brandes 2001），O(V·E)。"""
    bc = {v: 0.0 for v in nodes}
    for s in nodes:
        S, P, sigma = [], {v: [] for v in nodes}, {v: 0.0 for v in nodes}
        sigma[s] = 1.0
        d = {v: -1 for v in nodes}
        d[s] = 0
        Q = deque([s])
        while Q:
            v = Q.popleft()
            S.append(v)
            for w in adj.get(v, ()):
                if d[w] < 0:
                    d[w] = d[v] + 1
                    Q.append(w)
                if d[w] == d[v] + 1:
                    sigma[w] += sigma[v]
                    P[w].append(v)
        delta = {v: 0.0 for v in nodes}
        while S:
            w = S.pop()
            for v in P[w]:
                delta[v] += sigma[v] / sigma[w] * (1 + delta[w])
            if w != s:
                bc[w] += delta[w]
    return {k: round(v / 2.0, 3) for k, v in bc.items()}


def main():
    panel = C.load_panel()
    inst = panel["institutions"]
    cov = panel["coverage"]
    city_of = {i["name"]: i["city"] for i in inst}

    # ---------- 边 ----------
    raw = panel["pairs"]
    e1 = [e for e in raw if not same_family(e[0], e[1])]
    n_family = len(raw) - len(e1)
    e2 = panel["inst_company_pairs"]
    # 企业名做轻量归一，避免同一企业多种写法把链条打散
    comp_norm = {}
    for _, comp, _w in e2:
        comp_norm.setdefault(re.sub(r"\s+", "", comp), comp)

    adj = defaultdict(set)
    wdeg = Counter()
    for a, b, w in e1:
        adj[a].add(b)
        adj[b].add(a)
        wdeg[a] += w
        wdeg[b] += w
    org_company = defaultdict(Counter)   # 机构 → {企业: 篇次}
    company_org = defaultdict(Counter)   # 企业 → {机构: 篇次}
    comp_edges = 0
    for a, comp, w in e2:
        c = re.sub(r"\s+", "", comp)
        org_company[a][c] += w
        company_org[c][a] += w
        comp_edges += 1

    # ---------- 二跳链条（机构 E 企业 机构） ----------
    chains = []
    for c, orgs in company_org.items():
        if len(orgs) < 2:
            continue
        lst = sorted(orgs.items(), key=lambda x: -x[1])
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                a, wa = lst[i]
                b, wb = lst[j]
                if a == b or same_family(a, b):
                    continue
                chains.append({"org_a": a, "org_b": b, "company": comp_norm.get(c, c),
                               "w_a": wa, "w_b": wb, "w": wa + wb,
                               "cities": [city_of.get(a), city_of.get(b)]})
    chains.sort(key=lambda x: -x["w"])
    n_2hop = len(chains)

    # ---------- 图统计（机构子图） ----------
    e1_nodes = sorted({x for e in e1 for x in e[:2]})
    org_nodes = sorted(set(e1_nodes) | {a for a, _, _ in e2})
    comp_nodes = sorted(company_org)
    n_e1 = len(e1_nodes)
    n_org = len(org_nodes)
    # 密度只在「机构-机构」边上算，分母是 E1 端点集（产学研边是二部边，不进这个分母）
    density = round(len(e1) / (n_e1 * (n_e1 - 1) / 2), 6) if n_e1 > 1 else None
    bip_density = round(len(e2) / (n_org * len(comp_nodes)), 6) if comp_nodes else None

    # 连通分量（只含机构-机构边）
    seen, comps = set(), []
    for v in e1_nodes:
        if v in seen:
            continue
        q, blk = deque([v]), []
        seen.add(v)
        while q:
            x = q.popleft()
            blk.append(x)
            for y in adj.get(x, ()):
                if y not in seen:
                    seen.add(y)
                    q.append(y)
        comps.append(blk)
    comps.sort(key=len, reverse=True)

    bc = brandes(e1_nodes, adj)
    deg = {v: len(adj.get(v, ())) for v in org_nodes}
    top_deg = sorted(e1_nodes, key=lambda v: (-deg[v], -wdeg[v]))[:20]
    top_bc = sorted(e1_nodes, key=lambda v: -bc[v])[:15]

    # ---------- 城市结构 ----------
    sz_nodes = [v for v in org_nodes if city_of.get(v) == "深圳市"]
    inner = sum(1 for a, b, w in e1 if city_of.get(a) == "深圳市" and city_of.get(b) == "深圳市")
    cross = len(e1) - inner
    city_stat = []
    for c in C.CITY_ORDER:
        nodes = [v for v in org_nodes if city_of.get(v) == c]
        city_stat.append({
            "city": c, "nodes": len(nodes),
            "deg_sum": sum(deg[v] for v in nodes),
            "wdeg_sum": sum(wdeg[v] for v in nodes),
            "in_2hop_chains": sum(1 for x in chains
                                  if city_of.get(x["org_a"]) == c or city_of.get(x["org_b"]) == c),
        })

    # ---------- 跨领域 ----------
    dom = {}
    for i in inst:
        d = C.domain_of(i.get("discipline_top"))
        if not d:
            for kw in (i.get("kw_top") or []):
                d = C.domain_of(kw)
                if d:
                    break
        if d:
            dom[i["name"]] = d
    cross_dom = 0
    dom_edges = 0
    for a, b, w in e1:
        da, db = dom.get(a), dom.get(b)
        if da and db:
            dom_edges += 1
            if da != db:
                cross_dom += 1
    cross_share = round(cross_dom / dom_edges * 100, 2) if dom_edges else None

    # ---------- 权重敏感性：按篇次阈值切边 ----------
    sens = []
    for cut in (1, 2, 3, 5):
        keep = [(a, b) for a, b, w in e1 if w >= cut]
        nodes = {x for e in keep for x in e}
        dens = round(len(keep) / (len(nodes) * (len(nodes) - 1) / 2), 6) if len(nodes) > 1 else None
        sens.append({"min_weight": cut, "edges": len(keep), "nodes": len(nodes),
                     "density": dens})

    out = {
        "metric_id": MID,
        "metric_name": "科研合作关系链条",
        "support_judgment": "部分支持",
        "generated_from": "code/_snapshots21/org_family_panel_20261021.json",
        "panel_built_at": panel["built_at"],
        "unit": "gkx.dwd_research_institute_base_info 2,074 家 + 论文共同署名企业",
        "base_years_used": ["2014", "2015", "2016", "2017", "2018", "2019",
                            "2020", "2021", "2022", "2023", "2024", "2025", "2026"],
        "base_years_missing": [],
        "note_years": "论文共同署名未按年切片：匹配集按年只有 10–1,159 篇，切年后链条数不足以做趋势；"
                      "2024 为整批补录年，不宜作为链条增量年份",
        "coverage": cov,
        "edges": {"E1_org_org": len(e1), "E1_family_dropped": n_family,
                  "E2_org_company": comp_edges, "companies": len(comp_nodes)},
        "graph": {"all_org_nodes": n_org, "e1_nodes": n_e1,
                  "e1_edges": len(e1), "density_e1": density,
                  "company_nodes": len(comp_nodes), "e2_edges": len(e2),
                  "bipartite_density": bip_density,
                  "components": len(comps),
                  "largest_component": len(comps[0]) if comps else 0,
                  "singletons": sum(1 for c in comps if len(c) == 1)},
        "chains_2hop": {"count": n_2hop,
                        "orgs_involved": len({x["org_a"] for x in chains} | {x["org_b"] for x in chains})},
        "shenzhen": {"nodes": len(sz_nodes), "inner_edges": inner,
                     "cross_edges": cross},
        "city": city_stat,
        "core_nodes": [{"name": v, "city": city_of.get(v), "degree": deg[v],
                        "wdeg": wdeg[v], "betweenness": bc[v]} for v in top_deg],
        "bridges": [{"name": v, "city": city_of.get(v), "betweenness": bc[v],
                     "degree": deg[v]} for v in top_bc if bc[v] > 0],
        "top_chains": chains[:25],
        "cross_domain": {"edges_with_domain_data": dom_edges, "cross_domain_edges": cross_dom,
                         "share_pct": cross_share, "orgs_with_domain": len(dom)},
        "sensitivity": sens,
        "vs_org_deep_153_1": {
            "same": "同属科研机构合作网络，同一机构底册",
            "diff": "153 件以学者级共著（dwd_scholar_coauthor 1,187,606 条）为唯一底边、"
                    "建学者-机构二部图后上卷；本件以论文署名机构串 + 产学研共同署名为边源，"
                    "并显式建「机构—企业—机构」二跳链条",
            "cannot_mix": "两件节点集与边权不同（153 件 V=1,052/E=1,519），不可相加、不可互校密度",
        },
        "gaps": [
            "专利共同申请人边缺失：dwd_patent 2,939,895 行无 apdt_year/first_applicant_name 索引，"
            "按申请人名聚合一次即被服务端杀（§3.6），本件只能用论文署名串",
            "项目合作边断裂：dwd_zh_project.funded_institution 58,453 行全为空，"
            "participating_institution 是单值字段，一对多合作关系无法还原",
            "机构-机构边只有 90 条（踢 6 条同族伪边后），网络极度稀疏，密度指标的解释力有限",
            "跨领域特征只覆盖 50 家机构（论文关键词表 cls 仅 20,048/100,900 篇有值）",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)

    print(f"{MID}: 机构节点 {n_org}，E1 {len(e1)}（剔同族 {n_family}），E2 {comp_edges}")
    print(f"  二跳链条 {n_2hop} 条；连通分量 {len(comps)}，最大 {len(comps[0]) if comps else 0}")
    print(f"  深圳节点 {len(sz_nodes)}，内部边 {inner}，跨境边 {cross}")
    print(f"  密度 {density}；跨领域边占比 {cross_share}%")
    print(f"  -> {OUT}")


if __name__ == "__main__":
    main()

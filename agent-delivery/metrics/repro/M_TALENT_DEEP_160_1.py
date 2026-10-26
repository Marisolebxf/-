#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TALENT_DEEP_160_1 —— 人才关系链模型（TALENT 深度分析第 160 号）

需求语义：以「人—人—机构」的合作关系为链，展示人才的关系网络、跨区域连接与
关键枢纽，支撑「关联画像」「人才迁徙/合作」类页面。需求未给链路层级、边权与窗口。

本文口径（3 条 SQL，全部落 gkx.dwd_scholar_coauthor）：
  1. 边 = `dwd_scholar_coauthor` 一行（ego 学者 → 合作者 + 合作者机构 + 合著篇数）。
     该表 1,187,606 行（is_deleted=0）、20,011 个 ego、899,662 个合作者节点。
     **每个 ego 最多只存 100 个合作者**（实测 degree 上限恰为 100），是「前 100 强合作者」
     清单而不是全量合著网络——这一点必须在正文披露，否则会低估枢纽度。
  2. ego 侧没有姓名/机构列，用 `dwd_scholar_work_experience`（57,117 段、20,028 人）
     的现职机构补，两表 scholar_id **同域**（workexp 20,028 vs coauthor 20,011，几乎重合），
     但与 `dwd_scholar` 主档只有 1,839 个 id 交集 → 不 JOIN 主档，避免把 90% 的人读空。
  3. 城市：机构名 → `_talent21_common.loc()` 五级归属（高校名录 → 企业底册 → 前缀 →
     城市关键词 → 海外）。合作者侧机构直接来自 coauthor 表，填充率 86.0%。
  4. 时间：coauthor 表**没有年份列**，只能取 create_time 作数据时点，不能做趋势。

产物：code/M_TALENT_DEEP_160_1_out.json。
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from _talent21_common import (  # noqa: E402
    SNAP, base_year_block, clusters_of, loc, research, work, write_out,
)

METRIC = "M_TALENT_DEEP_160_1"
SZ = "深圳市"
CACHE = SNAP / "coauthor160_20261022.json"


def _db():
    from _gkxdb import gkx

    cur = gkx()
    cur.execute("SET SESSION max_execution_time=60000")
    return cur


def ego_orgs() -> dict[str, str]:
    """ego 现职机构：优先 is_current，其次取最晚一段履历。"""
    best: dict[str, tuple] = {}
    for r in work():
        sid, org = r["sid"], r["org"]
        if not org:
            continue
        key = (r["y1"] or r["y0"] or 0, 1 if r["cur"] else 0)
        old = best.get(sid)
        if old is None or key > old[0]:
            best[sid] = (key, org)
    return {k: v[1] for k, v in best.items()}


def load_edges(sz_ids: list[str]) -> dict:
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding="utf-8"))
    cur = _db()
    out: dict = {}
    cur.execute(
        """SELECT scholar_id, COUNT(DISTINCT co_scholar_id) d, SUM(co_paper_count) w,
                  MAX(co_paper_count) mx, MIN(create_time), MAX(create_time)
           FROM gkx.dwd_scholar_coauthor WHERE is_deleted=0 GROUP BY scholar_id"""
    )
    out["degree"] = [[("" if x is None else str(x)) for x in r] for r in cur.fetchall()]
    ids = ",".join("'%s'" % i for i in sz_ids)
    cur.execute(
        "SELECT scholar_id, co_scholar_id, co_scholar_name_zh, co_scholar_org_name_zh, co_paper_count"
        " FROM gkx.dwd_scholar_coauthor WHERE is_deleted=0 AND scholar_id IN (" + ids + ")"
    )
    out["sz_ego_edges"] = [[("" if x is None else str(x)) for x in r] for r in cur.fetchall()]
    cur.execute(
        "SELECT scholar_id, co_scholar_id, co_scholar_name_zh, co_scholar_org_name_zh, co_paper_count"
        " FROM gkx.dwd_scholar_coauthor WHERE is_deleted=0 AND co_scholar_org_name_zh LIKE '%深圳%'"
    )
    out["sz_alter_edges"] = [[("" if x is None else str(x)) for x in r] for r in cur.fetchall()]
    CACHE.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    return out


def main() -> None:
    orgs = ego_orgs()
    city = {sid: loc(o)[1] for sid, o in orgs.items()}
    sz_ids = sorted([sid for sid, c in city.items() if c == SZ])
    raw = load_edges(sz_ids)

    # ---------- 度分布 ----------
    deg = [{"sid": r[0], "d": int(r[1] or 0), "w": int(float(r[2] or 0)),
            "mx": int(r[3] or 0)} for r in raw["degree"]]
    dvals = [r["d"] for r in deg]
    cap100 = sum(1 for d in dvals if d >= 100)
    hist = Counter()
    for d in dvals:
        b = ("1-5" if d <= 5 else "6-10" if d <= 10 else "11-20" if d <= 20
             else "21-50" if d <= 50 else "51-100")
        hist[b] += 1
    degree = {
        "egos": len(dvals),
        "edges": sum(dvals),
        "mean": round(statistics.mean(dvals), 2),
        "median": statistics.median(dvals),
        "p90": float(statistics.quantiles(dvals, n=10)[8]),
        "max": max(dvals),
        "at_cap_100": cap100,
        "at_cap_100_pct": round(100 * cap100 / len(dvals), 2),
        "hist": dict(hist),
        "weight_median": statistics.median([r["w"] for r in deg]),
        "max_single_co_papers": max(r["mx"] for r in deg),
    }

    # ---------- 按 ego 城市比较度 ----------
    by_city: dict[str, list[int]] = defaultdict(list)
    for r in deg:
        c = city.get(r["sid"])
        if c:
            by_city[c].append(r["d"])
    region_degree = []
    for c, v in sorted(by_city.items(), key=lambda kv: -len(kv[1]))[:8]:
        region_degree.append({"city": c, "n": len(v), "mean_deg": round(statistics.mean(v), 2),
                              "median_deg": statistics.median(v),
                              "p90_deg": float(statistics.quantiles(v, n=10)[8]) if len(v) >= 10 else None})

    # ---------- 深圳 ego 侧子图 ----------
    ego_edge: dict[str, list[dict]] = defaultdict(list)
    for sid, coid, coname, coorg, w in raw["sz_ego_edges"]:
        ego_edge[sid].append({"coid": coid, "name": coname, "org": coorg,
                              "w": int(float(w or 0))})
    n_edges = sum(len(v) for v in ego_edge.values())
    alters = {e["coid"] for v in ego_edge.values() for e in v}
    alter_city = Counter()
    alter_org = Counter()
    within_sz = 0
    unk = 0
    for sid, edges in ego_edge.items():
        for e in edges:
            c = loc(e["org"])[1] if e["org"] else "未填"
            if c in ("未填", "未归属"):
                unk += 1
            alter_city[c] += 1
            if c == SZ:
                within_sz += 1
            if e["org"]:
                alter_org[e["org"].strip()] += 1
    sz_egos = sorted(ego_edge)
    cities_per_ego = {
        sid: len({loc(e["org"])[1] for e in ego_edge[sid] if e["org"]} - {"未填", "未归属"})
        for sid in sz_egos
    }
    bridging = [{"sid": sid, "org": orgs.get(sid, ""), "deg": len(ego_edge[sid]),
                 "cities": cities_per_ego[sid]} for sid in sz_egos if cities_per_ego[sid] >= 15]
    bridging.sort(key=lambda r: (-r["cities"], -r["deg"]))

    top_alters = Counter()
    named_edge = 0
    org_edge = 0
    for sid, edges in ego_edge.items():
        for e in edges:
            if e["name"].strip():
                named_edge += 1
            if e["org"].strip():
                org_edge += 1
            top_alters[e["org"].strip() or "机构缺"] += e["w"]

    sz_sub = {
        "egos": len(sz_egos),
        "edges": n_edges,
        "distinct_alters": len(alters),
        "edges_per_ego": round(n_edges / max(1, len(sz_egos)), 2),
        "within_sz_edges": within_sz,
        "within_sz_pct": round(100 * within_sz / max(1, n_edges), 2),
        "cross_city_edges": n_edges - within_sz,
        "org_unknown_edges": unk,
        "org_unknown_pct": round(100 * unk / max(1, n_edges), 2),
        "partner_cities": len([c for c in alter_city if c not in ("未填", "未归属")]),
        "top_partner_cities": [{"city": c, "edges": n, "pct": round(100 * n / max(1, n_edges), 2)}
                               for c, n in alter_city.most_common(12)],
        "top_partner_orgs": [{"org": o, "edges": n} for o, n in alter_org.most_common(15)],
        "bridging_egos_ge15_cities": len(bridging),
        "bridging_pct": round(100 * len(bridging) / max(1, len(sz_egos)), 2),
        "bridging_top10": bridging[:10],
        "cities_per_ego_median": statistics.median(list(cities_per_ego.values())) if cities_per_ego else 0,
        "top_partner_orgs_by_weight": [{"org": o, "co_papers": w}
                                       for o, w in top_alters.most_common(10)],
        "named_alter_edges": named_edge,
        "named_alter_pct": round(100 * named_edge / max(1, n_edges), 2),
        "org_alter_pct": round(100 * org_edge / max(1, n_edges), 2),
    }

    # ---------- 深圳被合作侧（alter = 深圳机构） ----------
    in_ego_city = Counter()
    in_ego_edge = Counter()
    sz_org_in = Counter()
    for sid, coid, coname, coorg, w in raw["sz_alter_edges"]:
        c = city.get(sid, "未知")
        in_ego_city[c] += 1
        if c != "未知":
            in_ego_edge[c] += int(float(w or 0))
        sz_org_in[(coorg or "").strip()] += 1
    inbound = {
        "edges": len(raw["sz_alter_edges"]),
        "distinct_egos": len({r[0] for r in raw["sz_alter_edges"]}),
        "distinct_sz_alters": len({r[1] for r in raw["sz_alter_edges"]}),
        "ego_city_top": [{"city": c, "edges": n, "co_papers": in_ego_edge.get(c, 0)}
                         for c, n in in_ego_city.most_common(12)],
        "top_sz_alters_org": [{"org": o, "edges": n} for o, n in sz_org_in.most_common(12)],
        "sz_ego_overlap": len(sz_egos),
    }

    # ---------- 研究方向 → 20+8 簇 ----------
    rd = research()
    cl = Counter()
    for sid in sz_egos:
        for c in clusters_of(rd.get(sid) or []):
            cl[c] += 1
    clusters = [{"cluster": c, "sz_egos": n} for c, n in cl.most_common(15)]
    tagged = sum(1 for sid in sz_egos if rd.get(sid))

    payload = {
        "metric": METRIC,
        "support_judgment": "部分支持",
        "support_reason": (
            "关系边（1,187,606 行 / 20,011 ego / 899,662 合作者）与机构名可全量现读，"
            "深圳子图、跨城连接、枢纽识别都能算；但（a）每个 ego 只保留前 100 个合作者，"
            "（b）ego 侧无姓名、只能靠履历表补机构，（c）表内无年份，趋势链不可算，"
            "（d）ego id 与主档 dwd_scholar 只有 1,839 个交集 → 部分支持。"),
        "base_years": base_year_block(
            [],
            list(range(2017, 2027)),
            "关系链表无任何年份字段：dwd_scholar_coauthor 只有 create_time（数据物化时点，"
            "实测区间见 probes.create_time_span），无合作年份、无合著首发年。故本文只交截面链路，"
            "不交时间序列；2017—2026 全部年份在 missing 中声明，不按 0 摊入任何比率。"),
        "method": {
            "edge": "dwd_scholar_coauthor 一行 = ego 学者 → 合作者（含合作者机构、合著篇数）",
            "ego_org": "dwd_scholar_work_experience 现职机构（is_current=1 优先，否则取最晚一段）",
            "city": "机构名 → loc() 五级归属（HEIS 名录 → 企业底册 → 前缀 → 城市关键词 → 海外）",
            "sz_ego": "ego 现职机构城市 = 深圳市",
            "within_sz": "合作者机构城市 = 深圳市 的边占全部边的比例",
            "bridging": "单个 ego 的合作者覆盖 ≥15 个不同城市（约等于全池 P75）",
            "inbound": "合作者机构城市 = 深圳市 的全部边，按 ego 城市汇总",
            "deg_cap": 100,
            "id_gap_note": "coauthor/workexp 同域（20,011 vs 20,028）；与 dwd_scholar 主档交集 1,839",
            "window": "截面（无年份）",
        },
        "coverage": {
            "degree_rows": len(raw["degree"]),
            "ego_total": len(deg),
            "edge_total": degree["edges"],
            "ego_with_org": len(city),
            "ego_city_mapped": sum(1 for c in city.values() if c not in ("未填", "未归属")),
            "sz_egos": len(sz_egos),
            "sz_ego_edges": n_edges,
            "sz_alter_edges": len(raw["sz_alter_edges"]),
            "sz_alter_named": sum(1 for r in raw["sz_alter_edges"] if r[2].strip()),
            "sz_ego_named": sum(1 for r in raw["sz_ego_edges"] if r[2].strip()),
            "sz_ego_org_filled": sum(1 for r in raw["sz_ego_edges"] if r[3].strip()),
            "sz_research_tagged": tagged,
            "sz_clusters": len(cl),
        },
        "degree": degree,
        "region_degree": region_degree,
        "sz_subgraph": sz_sub,
        "inbound": inbound,
        "clusters": clusters,
        "integrity": {
            "note": "合作者姓名非空率仅 16.19%（1,468/9,066 条边），不足以支撑「人名人」链路，"
                    "本文的链路一律落在**机构节点**上；姓名列只作举例，不作唯一标识。"
                    "ego 侧（coauthor 表）根本没有姓名列，故不出现「某专家」的点名榜。",
            "cap_note": "degree 上限 100 是表结构约束（每 ego 前 100 合作者），不是真实上限；"
                        "34.03% 的 ego 已顶到 100，枢纽度被系统性截断。",
            "no_year": "表内无年份，任何「近 N 年新增关系」说法都不成立。",
        },
        "probes": {
            "coauthor_rows": 1187606,
            "coauthor_distinct_ego": 20011,
            "coauthor_distinct_alter": 899662,
            "coauthor_org_empty": 166427,
            "coauthor_org_fill_pct": round(100 * (1187606 - 166427) / 1187606, 2),
            "id_overlap_with_scholar": 1839,
            "workexp_rows": 57117,
            "workexp_egos": 20028,
            "create_time_span": [raw["degree"][0][4] if raw["degree"] else None,
                                 raw["degree"][0][5] if raw["degree"] else None],
            "sql_count": 3,
        },
    }
    payload["base_years_used"] = payload["base_years"]["base_years_used"]
    payload["base_years_missing"] = payload["base_years"]["base_years_missing"]
    payload["base_years_note"] = payload["base_years"]["note"]
    write_out(METRIC, payload)


if __name__ == "__main__":
    main()

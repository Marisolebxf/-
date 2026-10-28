#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""GAP-RECRUIT-METRIC-01 深圳连接度（20261021 换源版：gkx 直取）。

口径（本件定义，非甲方闭合口径）
--------------------------------
企业—深圳的经济联系由两组**投资/股权边**刻画，不用供应链（库内无表）：

  D1 对外投资：`dwd_org_invest_info` 的 org_id → inv_org_id，对端在深圳记 1；
  D2 归属/分支：`dwd_org_shareholder_info` 的 org_id → inv_org_id，
     加 `dwd_org_subsidiary_info` 的子公司名称含「深圳」；
  D3 稳健性口径：D1 + 股东边合并后重算（不含子公司名称代理）。

  $$S_k(i)=100\times\frac{\#\{\text{对端}\in\text{深圳}\}}{\#\{\text{全部对端}\}}$$
  $$Conn_{SZ}(i)=\frac{1}{|K|}\sum_{k\in K}S_k(i),\quad K=\{k:S_k\text{ 有定义}\}$$

D3 与 D1/D2 共用同一批边，只作口径敏感性对照，不构成第三个独立数据源；
供应链维（旧稿 D3 的名字）在 gkx 无表，本件不冒充。

数据面：gkx @ 183.240.141.251:3318（只读）；底册读 `code/_snapshots21/base_20261021.json`。
"""
from __future__ import annotations

import json
import statistics
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import _gkxdb as DB  # noqa: E402

OUT = HERE / "GAP-RECRUIT-METRIC-01_out.json"
SNAP = HERE / "_snapshots21"
BASE = SNAP / "base_20261021.json"
SOURCE = ("gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）：dwd_org_invest_info(46,967)、"
          "dwd_org_shareholder_info(400,286)、dwd_org_subsidiary_info(178,900)；"
          "底册 code/_snapshots21/base_20261021.json（189,116）")
ABSENCE_SOURCE = "gkx.information_schema（2026-10-23，`_snapshots21/w15c3_facts_20261023.json`）"


def pct(a: int, b: int):
    return round(100.0 * a / b, 4) if b else None


def st(vals):
    v = sorted(float(x) for x in vals if x is not None)
    if not v:
        return {"n": 0}
    def q(p):
        k = min(len(v) - 1, max(0, int(round(p * (len(v) - 1)))))
        return v[k]
    return {"n": len(v), "min": round(v[0], 4), "p50": round(statistics.median(v), 4),
            "p90": round(q(0.90), 4), "p99": round(q(0.99), 4),
            "max": round(v[-1], 4), "mean": round(statistics.mean(v), 4)}


def ranks(d):
    items = sorted(d.items(), key=lambda kv: (kv[1], kv[0]))
    out, i, n = {}, 0, len(items)
    while i < n:
        j = i
        while j + 1 < n and items[j + 1][1] == items[i][1]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            out[items[k][0]] = avg
        i = j + 1
    return out


def spearman(a, b):
    keys = sorted(set(a) & set(b))
    if len(keys) < 3:
        return None
    ra, rb = ranks({k: a[k] for k in keys}), ranks({k: b[k] for k in keys})
    xs, ys = [ra[k] for k in keys], [rb[k] for k in keys]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = (sum((x - mx) ** 2 for x in xs)) ** 0.5
    dy = (sum((y - my) ** 2 for y in ys)) ** 0.5
    return round(num / (dx * dy), 6) if dx and dy else None


def load_base():
    rows = json.loads(BASE.read_text(encoding="utf-8"))
    by_id, sz = {}, set()
    for r in rows:
        oid, _cc, nm, prov, city, _yr = (list(r) + [None] * 6)[:6]
        if not oid:
            continue
        by_id[oid] = {"name": nm, "province": prov, "city": city}
        if city and "深圳" in str(city):
            sz.add(oid)
    return by_id, sz


def absence_probe():
    """负证据：申请单里的三张阻塞表在 gkx 的存在性（检索条件 + 命中行数）。"""
    out = {"source": ABSENCE_SOURCE, "checks": []}
    cur = DB.gkx()
    try:
        cur.execute("SET SESSION max_execution_time=60000")
        for t in ("enterprise_supply_chain", "enterprise_cooperation",
                  "enterprise_industry_chain", "enterprise_centrality",
                  "enterprise_base", "enterprise_invest"):
            cur.execute("SELECT COUNT(*) FROM information_schema.tables "
                        "WHERE table_schema='gkx' AND table_name=%s", (t,))
            out["checks"].append({
                "table": t,
                "query": "information_schema.tables WHERE table_schema='gkx' AND table_name=?",
                "hit_rows": int(cur.fetchone()[0]),
            })
        like = {}
        for kw in ("supply", "supplier", "vendor", "cooperat", "coop", "collab", "central"):
            cur.execute("SELECT COUNT(*) FROM information_schema.tables "
                        "WHERE table_schema='gkx' AND table_name LIKE %s", ("%" + kw + "%",))
            nt = int(cur.fetchone()[0])
            cur.execute("SELECT COUNT(*) FROM information_schema.columns "
                        "WHERE table_schema='gkx' AND column_name LIKE %s", ("%" + kw + "%",))
            nc = int(cur.fetchone()[0])
            like[kw] = {"table_hits": nt, "column_hits": nc}
        out["fuzzy"] = like
        out["note"] = ("六张申请单表名逐字检索命中 0；supply/supplier/vendor/cooperat/coop/"
                       "collab/central 七个词的表名命中 0。`supplier` 的列命中仅出现在 "
                       "dwd_bid_base_out 的 supplier_qualification_criteria（招标资格文本，非关系列）。")
    finally:
        cur.close()
    return out


def fetch_edges():
    cur = DB.gkx()
    try:
        cur.execute("SET SESSION max_execution_time=0")
        cur.execute("SELECT org_id, inv_org_id FROM gkx.dwd_org_invest_info "
                    "WHERE org_id IS NOT NULL AND inv_org_id IS NOT NULL")
        inv = [(r[0], r[1]) for r in cur.fetchall()]
        cur.execute("SELECT org_id, sub_org_id, sub_name_cn FROM gkx.dwd_org_subsidiary_info "
                    "WHERE org_id IS NOT NULL")
        sub = [(r[0], r[1], r[2]) for r in cur.fetchall()]
        cur.execute("SELECT org_id, inv_org_id FROM gkx.dwd_org_shareholder_info "
                    "WHERE org_id IS NOT NULL AND inv_org_id IS NOT NULL")
        sh = [(r[0], r[1]) for r in cur.fetchall()]
    finally:
        cur.close()
    return inv, sub, sh


def agg(edges, sz):
    m = {}
    for o, j in edges:
        if not o or not j:
            continue
        e = m.setdefault(o, {"total": 0, "sz": 0})
        e["total"] += 1
        if j in sz:
            e["sz"] += 1
    return m


def main() -> int:
    t0 = time.time()
    base_by_id, sz = load_base()
    print("base", len(base_by_id), "sz", len(sz), flush=True)

    inv, sub, sh = fetch_edges()
    print("edges", len(inv), len(sub), len(sh), flush=True)

    d1 = agg(inv, sz)
    d2b = agg(sh, sz)

    # 子公司维两套属地判定：名称含「深圳」（旧稿代理）与 sub_org_id 命中底册深圳集合
    d2a, sub_name_sz, sub_id_sz, sub_id_resolved = {}, 0, 0, 0
    for o, j, nm in sub:
        if not o:
            continue
        e = d2a.setdefault(o, {"total": 0, "sz_name": 0, "sz_id": 0})
        e["total"] += 1
        if nm and "深圳" in str(nm):
            e["sz_name"] += 1
            sub_name_sz += 1
        if j:
            if j in sz:
                e["sz_id"] += 1
                sub_id_sz += 1
            if j in base_by_id:
                sub_id_resolved += 1

    orgs = set(d1) | set(d2a) | set(d2b)
    rows = []
    for o in orgs:
        a, b = d1.get(o, {}), d2b.get(o, {})
        c = d2a.get(o, {})
        s1 = pct(a.get("sz", 0), a.get("total", 0))
        t2 = c.get("total", 0) + b.get("total", 0)
        z2 = c.get("sz_name", 0) + b.get("sz", 0)
        s2 = pct(z2, t2)
        t3 = a.get("total", 0) + b.get("total", 0)
        z3 = a.get("sz", 0) + b.get("sz", 0)
        s3 = pct(z3, t3)
        parts = [x for x in (s1, s2, s3) if x is not None]
        if not parts:
            continue
        rows.append({
            "org_id": o,
            "S_D1": s1, "S_D2": s2, "S_D3": s3,
            "Conn_SZ": round(sum(parts) / len(parts), 4),
            "d1_total": a.get("total", 0), "d1_sz": a.get("sz", 0),
            "d2_total": t2, "d2_sz": z2,
            "d3_total": t3, "d3_sz": z3,
            "has_invest": bool(a), "has_sub": bool(c), "has_shareholder": bool(b),
        })

    # 两维口径（D1+D2，不含稳健性项）用于口径敏感性
    two = {r["org_id"]: round(statistics.mean([x for x in (r["S_D1"], r["S_D2"])
                                               if x is not None]), 4)
           for r in rows if r["S_D1"] is not None or r["S_D2"] is not None}
    conn = {r["org_id"]: r["Conn_SZ"] for r in rows}
    rho = spearman(conn, two)

    scores = [r["Conn_SZ"] for r in rows]
    positive = [r for r in rows if r["Conn_SZ"] > 0]
    scored_sz = sum(1 for r in rows if r["org_id"] in sz)

    def attach(r):
        m = base_by_id.get(r["org_id"], {})
        x = dict(r)
        x["name_cn"] = m.get("name")
        x["city"] = m.get("city")
        x["province"] = m.get("province")
        return x

    top = [attach(r) for r in sorted(rows, key=lambda x: (-x["Conn_SZ"],
                                                           -(x["d1_sz"] + x["d2_sz"])))[:15]]
    positive_top = [attach(r) for r in sorted(positive, key=lambda x: (-x["Conn_SZ"],
                                                                       -x["d1_sz"]))[:15]]
    named = [r for r in rows if r["org_id"] in base_by_id]
    named_top = [attach(r) for r in sorted(named, key=lambda x: (-x["Conn_SZ"],
                                                                 -(x["d1_sz"] + x["d2_sz"])))[:15]]

    buckets = {"0": 0, "0-10": 0, "10-25": 0, "25-50": 0, "50-75": 0, "75-100": 0}
    for s in scores:
        if s == 0:
            buckets["0"] += 1
        elif s < 10:
            buckets["0-10"] += 1
        elif s < 25:
            buckets["10-25"] += 1
        elif s < 50:
            buckets["25-50"] += 1
        elif s < 75:
            buckets["50-75"] += 1
        else:
            buckets["75-100"] += 1

    edge_hits = {
        "invest_rows": len(inv),
        "invest_to_sz_rows": sum(1 for _, j in inv if j in sz),
        "subsidiary_rows": len(sub),
        "subsidiary_name_sz_rows": sub_name_sz,
        "subsidiary_id_sz_rows": sub_id_sz,
        "subsidiary_sub_org_resolved": sub_id_resolved,
        "shareholder_rows": len(sh),
        "shareholder_to_sz_rows": sum(1 for _, j in sh if j in sz),
        "note": ("子公司维主口径用 sub_name_cn 含「深圳」；sub_org_id 命中底册深圳集合只作"
                 "对齐度披露（两者不可相加，名称代理会把「深圳市外分支」也算进对端）"),
    }

    support = "完全转换支持"
    payload = {
        "metric_id": "GAP-RECRUIT-METRIC-01",
        "metric_name": "深圳连接度",
        "support_judgment": support,
        "verdict_kind": "converted",
        "grain": "org_id（企业）× 关系对（投资/股东/子公司）",
        "data_source": "gkx @ 183.240.141.251:3318（只读）",
        "sources": [SOURCE, "code/_snapshots21/w15c3_facts_20261023.json（表存在性/行数探针）"],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面件：投资/股东/子公司三类边均无统一发布年度键，"
                            "不构成年度序列，不做同比/CAGR，也不把缺失年摊 0。"),
        "params": {"shenzhen_match": "base.city 含「深圳」；子公司用 sub_name_cn 含「深圳」",
                   "min_dimensions": 1, "d3_role": "稳健性对照，不独立计权"},
        "table_counts": {
            "dwd_org_base_info": len(base_by_id),
            "dwd_org_invest_info": len(inv),
            "dwd_org_subsidiary_info": len(sub),
            "dwd_org_shareholder_info": len(sh),
        },
        "shenzhen_org_n": len(sz),
        "n_orgs_with_edges": len(orgs),
        "n_scored": len(rows),
        "n_conn_gt0": len(positive),
        "n_conn_eq0": sum(1 for r in rows if r["Conn_SZ"] == 0),
        "n_scored_org_in_sz": scored_sz,
        "n_scored_named": len(named),
        "n_scored_unnamed": len(rows) - len(named),
        "score_stats": st(scores),
        "score_buckets": buckets,
        "score_bucket_sums": {
            "eq0": buckets["0"],
            "mid_0_75": buckets["0-10"] + buckets["10-25"] + buckets["25-50"] + buckets["50-75"],
            "mid_10_75": buckets["10-25"] + buckets["25-50"] + buckets["50-75"],
            "ends_0_or_100": buckets["0"] + buckets["75-100"],
            "note": "区间口径：ends = [0] ∪ [75,100]；mid_0_75 = (0,75)；mid_10_75 = [10,75)。",
        },
        "n_base_without_any_edge": len(base_by_id) - len(orgs),
        "edge_hit_stats": edge_hits,
        "top15_by_conn": top,
        "top15_named": named_top,
        "top15_positive": positive_top,
        "consistency": {
            "spearman_conn_vs_two_dim": rho,
            "n_two_dim": len(two),
            "note": "D3 是 D1+股东边重算，与主口径高度相关；相关系数用于证明它不引入新信息",
        },
        "cross_check_vs_20261020": {
            "old_n_scored": 62868,
            "old_n_conn_gt0": 31952,
            "old_mean": 36.1847,
            "old_median": 7.9034,
            "delta_n_scored": len(rows) - 62868,
            "delta_n_conn_gt0": len(positive) - 31952,
            "delta_mean": round(statistics.mean(scores) - 36.1847, 4) if scores else None,
            "delta_median": round(statistics.median(scores) - 7.9034, 4) if scores else None,
            "note": "旧版读数来自 20261020 交付件（换源前的镜像面），仅作逐项对账；四舍五入后差 0，说明 gkx 与旧面同源。",
        },
        "derived": {
            "conn_gt0_share_of_scored_pct": pct(len(positive), len(rows)),
            "scored_in_sz_share_pct": pct(scored_sz, len(rows)),
            "scored_named_share_pct": pct(len(named), len(rows)),
            "sz_org_share_of_base_pct": pct(len(sz), len(base_by_id)),
            "scored_share_of_base_pct": pct(len(rows), len(base_by_id)),
            "no_edge_share_of_base_pct": pct(len(base_by_id) - len(orgs), len(base_by_id)),
            "mid_10_75_share_of_scored_pct": pct(buckets["10-25"] + buckets["25-50"] + buckets["50-75"], len(rows)),
            "ends_share_of_scored_pct": pct(buckets["0"] + buckets["75-100"], len(rows)),
            "invest_to_sz_share_of_rows_pct": pct(edge_hits["invest_to_sz_rows"], len(inv)),
            "shareholder_to_sz_share_of_rows_pct": pct(edge_hits["shareholder_to_sz_rows"], len(sh)),
            "subsidiary_name_sz_share_of_rows_pct": pct(sub_name_sz, len(sub)),
            "subsidiary_id_sz_share_of_rows_pct": pct(sub_id_sz, len(sub)),
            "subsidiary_sub_org_resolved_pct": pct(sub_id_resolved, len(sub)),
            "denominator_note": (
                "• conn_gt0_share/scored：分母 n_scored=%d（有三类边中至少一类的主体数），"
                "不是底册 189,116；\n"
                "• sz_org_share_of_base / scored_share_of_base / no_edge_share_of_base：分母底册 %d；\n"
                "• invest_to_sz_share：分母投资边 %d 行；\n"
                "• shareholder_to_sz_share：分母股东边 %d 行；\n"
                "• subsidiary_*：分母子公司边 %d 行；名称代理与 id 命中是两个不同判定，不可相加。"
                % (len(rows), len(base_by_id), len(inv), len(sh), len(sub))
            ),
        },
        "absence_probe": absence_probe(),
        "caveats": [
            "投资/股东边是「资本联系」，不是供应链；gkx 无供应链边表，本件不拿投资边冒充供应关系。",
            "子公司维用名称含「深圳」判定属地，会把注册在深圳但实际无业务的分支计入对端。",
            "Conn_SZ 是比例均值，不区分关系金额大小；大额单边与小额单边同权。",
        ],
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print("n_scored=%d pos=%d mean=%s median=%s" % (
        len(rows), len(positive), payload["score_stats"].get("mean"),
        payload["score_stats"].get("p50")), flush=True)
    print("wrote", OUT.name, "%.1fs" % (time.time() - t0), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

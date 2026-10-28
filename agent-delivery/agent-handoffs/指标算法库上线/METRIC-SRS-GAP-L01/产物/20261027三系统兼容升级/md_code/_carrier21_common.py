#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""20261021 版 · 创新载体簇（CARRIER）共用算路：只读三方库 gkx，禁引 demo。

设计原则
--------
1. **唯一连库入口** `_gkxdb.gkx()`（该模块见 `demo_` 直接 raise）；所有 SQL 都写
   `gkx.<表名>`，不传 database / charset。
2. **重聚合一次落盘**：专利 2024 按申请人、论文 2024 按机构、标签全域、深圳池、
   存量/增量分布各扫一次，落 `code/_snapshots21/`，同簇 5 个指标共享。
3. **行数只读库存**：`_work_gkx21/GKX_INVENTORY.json` 已给逐表 COUNT(*)，
   本文件不重复摸 294 万行宽表（`dwd_patent` 全表 JOIN 会被服务端杀死）。
4. 缓存目录 `_snapshots21/` 与旧版 `_snapshots/` 物理隔离，避免旧快照被当新版证据。
"""
from __future__ import annotations

import json
from pathlib import Path

import _gkxdb

HERE = Path(__file__).parent
CACHE = HERE / "_snapshots21"
CACHE.mkdir(exist_ok=True)

INVENTORY = HERE.parent / "_work_gkx21" / "GKX_INVENTORY.json"

GKX = "gkx."
YEAR = 2024

ALIVE = ("存续（在营、开业、在册）", "在营（开业）企业", "正常", "存续", "在业")
ALIVE_SQL = ("reg_status IN ('存续（在营、开业、在册）','在营（开业）企业','正常','存续','在业')")


# ---------------------------------------------------------------- 连接与查询
def q(sql, args=None):
    cur = _gkxdb.gkx()
    try:
        cur.execute(sql, args) if args else cur.execute(sql)
        return cur.fetchall()
    finally:
        cur.close()


def qd(sql, args=None):
    cur = _gkxdb.gkx()
    try:
        cur.execute(sql, args) if args else cur.execute(sql)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    finally:
        cur.close()


# ---------------------------------------------------------------- 缓存与产物
def _load(name):
    p = CACHE / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def _save(name, obj):
    p = CACHE / name
    p.write_text(json.dumps(obj, ensure_ascii=False, default=str), encoding="utf-8")
    return p


def write_out(metric_id, payload):
    path = HERE / f"{metric_id}_out.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=1, default=str),
                    encoding="utf-8")
    return path


# ---------------------------------------------------------------- 行数（只读库存）
def inv_rows(table):
    inv = json.loads(INVENTORY.read_text(encoding="utf-8"))
    rec = inv.get(table)
    return int(rec["rows"]) if rec else None


def probes(tables):
    """源表行数探针：一律读 GKX_INVENTORY.json，不重复 COUNT(*) 大表。"""
    return {f"gkx.{t}": inv_rows(t) for t in tables}


# ---------------------------------------------------------------- 企业底册分布
def org_geo_scan(force=False):
    """企业底册一次分组扫：reg_status × city × incorporation_year。

    189,116 行、无覆盖索引，`COUNT(*)` 实测 87.7 秒；六条分散查询会把这笔成本
    重复六次。此处一次 GROUP BY 拿全，再在 Python 侧派生存量/城市/年度增量/深圳增量。
    """
    d = None if force else _load("org_geo_20261021.json")
    if d is None:
        d = qd("SELECT reg_status, city, incorporation_year y, COUNT(*) n "
               "FROM " + GKX + "dwd_org_base_info "
               "GROUP BY reg_status, city, incorporation_year")
        _save("org_geo_20261021.json", d)
    return d


def org_stock():
    """企业底册存量：reg_status 分档 + 总量（派生自一次分组扫）。"""
    rows = org_geo_scan()
    by = {}
    for r in rows:
        st = r["reg_status"]
        by[st] = by.get(st, 0) + int(r["n"])
    by_status = [{"reg_status": k, "n": v} for k, v in
                 sorted(by.items(), key=lambda x: -x[1])]
    return {"by_status": by_status, "total": sum(by.values()),
            "alive": sum(v for k, v in by.items() if k in ALIVE)}


def org_by_city(limit=8):
    """企业底册城市切片（总数 / 存活），派生自一次分组扫。"""
    agg = {}
    for r in org_geo_scan():
        c = r["city"]
        rec = agg.setdefault(c, {"city": c, "total": 0, "alive": 0})
        rec["total"] += int(r["n"])
        if r["reg_status"] in ALIVE:
            rec["alive"] += int(r["n"])
    rows = sorted(agg.values(), key=lambda x: -x["alive"])
    return rows[:limit]


def org_by_year(lo=2019, hi=2026):
    """企业底册年度增量（全库），派生自一次分组扫。"""
    agg = {}
    for r in org_geo_scan():
        y = r["y"]
        if y is None or not (lo <= int(y) <= hi):
            continue
        rec = agg.setdefault(int(y), {"y": int(y), "total": 0, "alive": 0})
        rec["total"] += int(r["n"])
        if r["reg_status"] in ALIVE:
            rec["alive"] += int(r["n"])
    return [agg[k] for k in sorted(agg)]


def sz_by_year(lo=2019, hi=2026):
    """深圳企业年度增量（旧版 city LIKE '深圳%'，不区分存活），同一次分组扫派生。"""
    agg = {}
    for r in org_geo_scan():
        y = r["y"]
        c = r["city"] or ""
        if not c.startswith("深圳"):
            continue
        if y is None or not (lo <= int(y) <= hi):
            continue
        agg[int(y)] = agg.get(int(y), 0) + int(r["n"])
    return [{"y": k, "n": agg[k]} for k in sorted(agg)]


def inst_by_city(limit=5):
    d = _load("inst_city_20261021.json")
    if d is None:
        rows = qd("SELECT city, COUNT(*) n FROM " + GKX + "dwd_research_institute_base_info "
                  "GROUP BY city ORDER BY n DESC")
        d = rows
        _save("inst_city_20261021.json", d)
    return d[:limit]


# ---------------------------------------------------------------- 标签
def tags():
    """org_id -> [org_tag...]（202,424 行全域一次拉取后本地分组）。"""
    d = _load("tech_tags_20261021.json")
    if d is None:
        rows = q("SELECT org_id, org_tag FROM " + GKX + "dwd_org_tech_tag")
        out = {}
        for oid, tag in rows:
            if tag is None or str(tag).strip() == "":
                continue
            out.setdefault(str(oid), []).append(str(tag))
        d = out
        _save("tech_tags_20261021.json", d)
    return d


# ---------------------------------------------------------------- 专利（按申请人名）
# 重要：gkx.dwd_patent 的 `apdt_year` / `first_applicant_name` **均无索引**，
# 一条 `WHERE apdt_year=2024 GROUP BY first_applicant_name` 在服务端跑满 600 秒
# 被读超时杀掉（本批实测复现）。`first_applicant_name IN (800 名)` 反而更慢：
# 无索引列的 IN 是 2.9M × 800 次比较。唯一可行路径与 DATA_FACTS §3.6 一致：
# **按 dwd_id 主键分块（50 万 id 一页）流式扫，块内聚合、块间按 pn 去重**，可断点续跑。
PATENT_BLOCK = 500_000
PATENT_BLOCKS = CACHE / "_patent_blocks"
PATENT_BLOCKS.mkdir(exist_ok=True)


_FINAL_CACHE = None


def patent_scan(force=False, worker=0, workers=1, merge=True, reverse=False):
    """分块扫 `dwd_patent`，只保留 2024 行；返回 (by_name, ipc_by_name, meta)。

    by_name: name -> [2024 去重 pn 数, 授权公告号非空行数, 授权去重 pn 数]
    ipc_by_name: name -> {ipc 主组: [pn...]}（仅深圳池 + 入集池名字，控制体积）
    """
    global _FINAL_CACHE
    if _FINAL_CACHE is not None and not force:
        return _FINAL_CACHE
    final = _load("patent2024_scan_20261021.json")
    if final is not None and not force:
        _FINAL_CACHE = (final["by_name"], final["ipc"], final["meta"])
        return _FINAL_CACHE

    interest = set()
    for oid, nm in sz_pool():
        interest.add(nm)
    for oid, nm, src in carrier_pool():
        interest.add(nm)

    cur = _gkxdb.gkx()
    try:
        cur.execute("SELECT MIN(dwd_id), MAX(dwd_id) FROM " + GKX + "dwd_patent")
        lo, hi = cur.fetchone()
    finally:
        cur.close()
    lo, hi = int(lo), int(hi)
    meta = {"min_id": lo, "max_id": hi, "block": PATENT_BLOCK,
            "blocks_total": (hi - lo) // PATENT_BLOCK + 1}

    start = (lo // PATENT_BLOCK) * PATENT_BLOCK
    idxs = list(range(start, hi + PATENT_BLOCK, PATENT_BLOCK))
    if reverse:
        idxs = idxs[::-1]
    for idx, a in enumerate(idxs):
        if workers > 1 and idx % workers != worker:
            continue
        b = a + PATENT_BLOCK
        bf = PATENT_BLOCKS / f"{a}_{b}.json"
        if bf.exists():
            continue
        rows = qd("SELECT first_applicant_name nm, pn, granted_number g, "
                  "SUBSTRING_INDEX(main_classification_ipcr,'/',1) ipc4 "
                  "FROM " + GKX + "dwd_patent "
                  f"WHERE dwd_id > {a} AND dwd_id <= {b} AND apdt_year = {YEAR}")
        agg, ipc = {}, {}
        for r in rows:
            nm = r["nm"]
            if not nm:
                continue
            nm = str(nm)
            rec = agg.setdefault(nm, [[], 0, []])
            if r["pn"] is not None and r["pn"] != "":
                rec[0].append(str(r["pn"]))
            if r["g"] is not None and r["g"] != "":
                rec[1] += 1
                rec[2].append(str(r["pn"]))
            if nm in interest:
                ip = r["ipc4"] or ""
                if ip:
                    ipc.setdefault(nm, {}).setdefault(str(ip), []).append(str(r["pn"]))
        bf.write_text(json.dumps({"lo": a, "hi": b, "rows": len(rows), "agg": agg,
                                  "ipc": ipc}, ensure_ascii=False), encoding="utf-8")
        print(f"[patent block {worker}/{workers}] {a}-{b} rows={len(rows)}", flush=True)

    blocks_done = len(list(PATENT_BLOCKS.glob("*_*.json")))
    print(f"[patent scan {worker}/{workers}] blocks {blocks_done}/{meta['blocks_total']}", flush=True)
    if not merge or blocks_done < meta["blocks_total"]:
        return None, None, {**meta, "blocks_done": blocks_done, "complete": False}

    by_name, ipc_by_name = {}, {}
    for bf in sorted(PATENT_BLOCKS.glob("*_*.json")):
        blk = json.loads(bf.read_text(encoding="utf-8"))
        for nm, (pns, g, gpns) in blk["agg"].items():
            by_name.setdefault(nm, [set(), 0, set()])
            by_name[nm][0].update(pns)
            by_name[nm][1] += int(g)
            by_name[nm][2].update(gpns)
        for nm, d in blk["ipc"].items():
            tgt = ipc_by_name.setdefault(nm, {})
            for ip, pns in d.items():
                tgt.setdefault(ip, set()).update(pns)

    # [2024 去重 pn 数, 授权公告号非空行数, 授权去重 pn 数]
    by_name = {k: [len(v[0]), v[1], len(v[2])] for k, v in by_name.items()}
    # ipc_by_name[name][ipc] = pn 列表（保留集合语义，供前缀口径再聚合）
    ipc_by_name = {k: {ip: sorted(v) for ip, v in d.items()} for k, d in ipc_by_name.items()}
    meta["names"] = len(by_name)
    meta["names_with_ipc"] = len(ipc_by_name)
    meta["blocks_done"] = blocks_done
    meta["complete"] = True
    _save("patent2024_scan_20261021.json",
          {"by_name": by_name, "ipc": ipc_by_name, "meta": meta})
    _FINAL_CACHE = (by_name, ipc_by_name, meta)
    return _FINAL_CACHE


def patent_by_name():
    return patent_scan()[0]


def patent_ipc_by_name():
    return patent_scan()[1]


def ipc_count(name, prefix=None, exact=None):
    """某载体 2024 专利在 IPC 主组上的去重 pn 数。

    `exact` 给定时按主组全等（旧版 SUBSTRING_INDEX(...,'/') 粒度，如 B23K26）；
    `prefix` 给定时按前缀合并后再按 pn 去重（旧版 `LIKE 'H02J%'` 口径）。
    """
    d = patent_ipc_by_name().get(name, {})
    if exact is not None:
        return len(set(d.get(exact, [])))
    if prefix is not None:
        pns = set()
        for k, v in d.items():
            if k.startswith(prefix):
                pns.update(v)
        return len(pns)
    return len({p for v in d.values() for p in v})


def top_ipc4(names, limit=4):
    """入集载体的 2024 专利 IPC 主组分布 TopN（领域宇宙动态选取）。"""
    ipc = patent_ipc_by_name()
    names = set(n for n in names if n)
    tot = {}
    for nm in names:
        for ip, pns in ipc.get(nm, {}).items():
            tot.setdefault(ip, set()).update(pns)
    return [k for k, _ in sorted(tot.items(), key=lambda x: -len(x[1]))[:limit]]


# ---------------------------------------------------------------- 论文（按机构名）
def papers_by_inst():
    """2024 年中文论文按作者机构去重篇数。"""
    d = _load("papers2024_by_inst_20261021.json")
    if d is None:
        rows = q("SELECT a.institution inst, COUNT(DISTINCT p.id) c "
                 "FROM " + GKX + "dwd_zh_paper p JOIN " + GKX + "dwd_zh_author a "
                 "ON p.id = a.paper_id WHERE p.cover_year_start = %s "
                 "GROUP BY a.institution", (YEAR,))
        d = {str(k): int(v or 0) for k, v in rows if k}
        _save("papers2024_by_inst_20261021.json", d)
    return d


# ---------------------------------------------------------------- 入集池
def sz_pool(limit=3000):
    """深圳存活载体池（旧版同一条 SQL：城市 LIKE + 存续，LIMIT 控制）。"""
    d = _load(f"sz_pool_{limit}_20261021.json")
    if d is None:
        rows = q("SELECT org_id, name_cn FROM " + GKX + "dwd_org_base_info "
                 "WHERE city LIKE '深圳%%' AND " + ALIVE_SQL + f" LIMIT {int(limit)}")
        d = [[str(o), str(n)] for o, n in rows]
        _save(f"sz_pool_{limit}_20261021.json", d)
    return d


def carrier_pool(n_cn=2000, n_inst=500, n_forg=500):
    """王惠入集三源（国内企业 / 科研机构 / 海外），各按旧版 LIMIT 截取。"""
    d = _load("carrier_pool_20261021.json")
    if d is None:
        rows = q("SELECT org_id, name_cn FROM " + GKX + "dwd_org_base_info "
                 f"WHERE reg_status LIKE '%%存续%%' LIMIT {int(n_cn)}")
        rows = [[str(o), str(n), "cn"] for o, n in rows]
        rows += [[str(o), str(n), "inst"] for o, n in
                 q("SELECT org_id, name_cn FROM " + GKX + "dwd_research_institute_base_info "
                   f"WHERE reg_status IN ('正常','在业') LIMIT {int(n_inst)}")]
        rows += [[str(o), str(n), "forg"] for o, n in
                 q("SELECT org_id, name_en FROM " + GKX + "dwd_forg_base_info "
                   f"LIMIT {int(n_forg)}")]
        d = rows
        _save("carrier_pool_20261021.json", d)
    return d


def pool_city():
    """入集池（三源）org_id -> city，供地区宇宙切片。"""
    d = _load("carrier_pool_city_20261021.json")
    if d is None:
        out = {}
        for oid, city in q("SELECT org_id, city FROM " + GKX + "dwd_org_base_info "
                           "WHERE reg_status LIKE '%%存续%%' LIMIT 2000"):
            out[str(oid)] = "" if city is None else str(city)
        for oid, city in q("SELECT org_id, city FROM " + GKX +
                           "dwd_research_institute_base_info "
                           "WHERE reg_status IN ('正常','在业') LIMIT 500"):
            out[str(oid)] = "" if city is None else str(city)
        for oid, city in q("SELECT org_id, city FROM " + GKX + "dwd_forg_base_info LIMIT 500"):
            out[str(oid)] = "" if city is None else str(city)
        d = out
        _save("carrier_pool_city_20261021.json", d)
    return d


def annual_fin(org_ids):
    """最近年年报：org_id -> (year, development_employee, employees_number, revenue)。"""
    d = _load("annual_fin_pool_20261021.json")
    if d is None:
        ids = tuple(dict.fromkeys(org_ids))
        out = {}
        step = 5000
        for i in range(0, len(ids), step):
            chunk = ids[i:i + step]
            ph = ",".join(["%s"] * len(chunk))
            rows = q("SELECT org_id, year, development_employee, employees_number, "
                     "operating_revenue FROM " + GKX + "dwd_org_annual_financial_info "
                     "WHERE org_id IN (" + ph + ")", chunk)
            for oid, yr, dev, emp, rev in rows:
                rec = out.get(str(oid))
                if rec is None or (yr or 0) > rec[0]:
                    out[str(oid)] = [yr, dev, emp, rev]
        d = out
        _save("annual_fin_pool_20261021.json", d)
    return d


def stock_fin(org_ids):
    """上市财报最近期：org_id -> (occur_period, revenue)。"""
    d = _load("stock_fin_pool_20261021.json")
    if d is None:
        ids = tuple(dict.fromkeys(org_ids))
        out = {}
        step = 5000
        for i in range(0, len(ids), step):
            chunk = ids[i:i + step]
            ph = ",".join(["%s"] * len(chunk))
            rows = q("SELECT org_id, occur_period, operating_revenue FROM " + GKX +
                     "dwd_org_stock_finance_info WHERE operating_revenue IS NOT NULL "
                     "AND org_id IN (" + ph + ")", chunk)
            for oid, per, rev in rows:
                rec = out.get(str(oid))
                if rec is None or (per or "") > rec[0]:
                    out[str(oid)] = [per, rev]
        d = out
        _save("stock_fin_pool_20261021.json", d)
    return d


# ---------------------------------------------------------------- 统计工具
def norm(xs):
    xs2 = [x for x in xs if x is not None]
    if not xs2:
        return [None] * len(xs)
    lo, hi = min(xs2), max(xs2)
    if hi == lo:
        return [0.5 if x is not None else None for x in xs]
    return [((x - lo) / (hi - lo)) if x is not None else None for x in xs]


def num(v, default=0.0):
    if v is None or v == "":
        return default
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


if __name__ == "__main__":
    print("inventory:", probes(["dwd_org_base_info", "dwd_patent", "dwd_org_tech_tag"]))
    print("tags orgs:", len(tags()))
    print("patent names:", len(patent_by_name()))
    print("papers insts:", len(papers_by_inst()))

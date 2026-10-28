#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""20261021 版 · 产业链簇（CHAIN）共用算路：只读三方库 gkx，禁引 demo。

设计原则
--------
1. **唯一连库入口** `_gkxdb.gkx()`（该模块见 `demo_` 直接 raise）；本文件所有 SQL 都写
   `gkx.<表名>`，不传 database / charset。
2. **重聚合一次落盘**：`tags × base` 的链×城/链×省聚合、`tags` 链宇宙行数、主档全量
   （189,116 行）三项各扫一次，落 `code/_snapshots21/*.json`，同簇 5 个指标共享。
   三方库 `dwd_org_industry_tags` 的 `credit_code` **无索引**（SHOW INDEX 实测只有主键与
   updated_time 组合索引），普通 JOIN 会退化成嵌套循环；必须 `tags STRAIGHT_JOIN base`
   让标签表作驱动表、主档走哈希，否则单条链的 JOIN 5 分钟不返回。
3. **行数只读库存**：`GKX_INVENTORY.json` 已给逐表 COUNT(*)，本文件不重复摸大表。
4. 缓存目录 `_snapshots21/` 与旧版 `_snapshots/` 物理隔离，避免把旧快照当成新版证据。
"""
from __future__ import annotations

import json
import statistics
from pathlib import Path

import _gkxdb

CACHE = Path(__file__).parent / "_snapshots21"
CACHE.mkdir(exist_ok=True)

GKX = "gkx."
ROOTS = ["INB1204", "INB1209", "INB1236", "INB1303", "INB1306", "INB1309",
         "INB1323", "INB1333", "INB1354", "INB1502", "INB2503", "INB2505"]
CITY4 = ["深圳市", "广州市", "东莞市", "惠州市"]
STAT_YEAR = 2025
PAT_CUTOFF = 2024


# ---------------------------------------------------------------- 连接与查询
def q(sql, args=None):
    cur = _gkxdb.gkx()
    try:
        cur.execute(sql, args) if args else cur.execute(sql)
        return cur.fetchall()
    finally:
        cur.close()


def q1(sql, args=None):
    rows = q(sql, args)
    return rows[0] if rows else None


def qd(sql, args=None):
    """字典行（列名做 key），便于写探针。"""
    cur = _gkxdb.gkx()
    try:
        cur.execute(sql, args) if args else cur.execute(sql)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    finally:
        cur.close()


# ---------------------------------------------------------------- 缓存
def cache_path(name):
    return CACHE / name


def load_cache(name):
    p = cache_path(name)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def save_cache(name, obj):
    p = cache_path(name)
    p.write_text(json.dumps(obj, ensure_ascii=False, default=str), encoding="utf-8")
    return p


def write_out(metric_id, payload):
    path = Path(__file__).parent / f"{metric_id}_out.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return path


# ---------------------------------------------------------------- 链树
def tree():
    """1,273 节点链树（gkx.dwd_industry_chain_info，含 parent_code）。"""
    d = load_cache("chain_tree_20261021.json")
    if d is None:
        d = qd("SELECT industry_code, industry_name, parent_code, level FROM " + GKX +
               "dwd_industry_chain_info WHERE is_deleted=0 ORDER BY industry_code")
        save_cache("chain_tree_20261021.json", d)
    return d


def chain_names():
    return {r["industry_code"]: r["industry_name"] for r in tree() if len(r["industry_code"]) == 7}


def chain_name_map():
    return {r["industry_code"]: r["industry_name"] for r in tree()}


def chain_l1():
    """顶层链 → 直属 L1 环节（9 位码）。

    gkx 的 `dwd_industry_chain_info.parent_code` 存的是**父节点中文名**（顶层节点存自身名），
    无法直接当编码用；但 industry_code 本身是前缀分层（7→9→11→…），故 L1 直接按
    「长度 9 且前 7 位等于顶层链码」取。实测 12 链共 41 个 L1，与旧版 policy 指标一致。
    """
    t = tree()
    return {c: sorted(r["industry_code"] for r in t
                      if len(r["industry_code"]) == 9 and r["industry_code"].startswith(c))
            for c in ROOTS}


# ---------------------------------------------------------------- 主档（企业底册）
def base_rows():
    """189,116 行主档（is_deleted=0），一次拉全量落缓存。

    字段：org_id, external_id, name_cn, province, city, incorporation_year
    """
    d = load_cache("base_20261021.json")
    if d is None:
        rows = q("SELECT org_id, external_id, name_cn, province, city, incorporation_year "
                 "FROM " + GKX + "dwd_org_base_info WHERE is_deleted=0")
        d = [list(r) for r in rows]
        save_cache("base_20261021.json", d)
    return d


def org_index():
    """org_id -> [org_id, credit, name, province, city]"""
    return {r[0]: r for r in base_rows()}


def credit_city():
    """credit_code -> city"""
    return {r[1]: r[4] for r in base_rows() if r[1]}


def base_province_dist():
    prov, city = {}, {}
    for r in base_rows():
        prov[r[3]] = prov.get(r[3], 0) + 1
        city[r[4]] = city.get(r[4], 0) + 1
    return prov, city


# ---------------------------------------------------------------- 链 × 城 / 链 × 省
def bridge(force=False):
    """企业—链桥：链上有属地标签的 35,046 家企业（52,906 条可联标签行）。

    返回 list[{nm, cc, p, c, n_row, chains:[...]}]；一次扫描 tags×base，
    `tags STRAIGHT_JOIN base` 让标签表作驱动表（`tags.credit_code` 无索引，
    反序会退化 4×10^11 次比较）。
    """
    d = None if force else load_cache("bridge_20261021.json")
    if d is not None:
        return d
    # 标签表 industry_code 是「字符串化的列表」（如 "['INB1306']" / "['INB1309','INB1306']"），
    # 且存在 credit_code 为时间戳的脏行。只取 18 位统一社会信用代码的行 + 原始 (cc, ic) 对，
    # 链归属在 Python 侧用正则解析——避免 12 个 LIKE 的整表条件聚合计入。
    import re
    pairs = q("SELECT credit_code, industry_code FROM " + GKX + "dwd_org_industry_tags "
              "WHERE is_deleted=0 AND CHAR_LENGTH(credit_code)=18")
    agg = {}
    pat = re.compile(r"INB\d{4}")
    for cc, ic in pairs:
        for ch in pat.findall(ic or ""):
            if ch in ROOTS:
                d = agg.setdefault(cc, {})
                d[ch] = d.get(ch, 0) + 1
    bidx = {r[1]: r for r in base_rows()}
    out = []
    for cc, tags in agg.items():
        b = bidx.get(cc)
        if not b:
            continue
        chains = [c for c in ROOTS if tags.get(c)]
        out.append({"nm": b[2], "cc": cc, "p": b[3], "c": b[4],
                    "n_row": sum(tags.values()), "chains": chains,
                    "tags": {c: tags[c] for c in chains}})
    save_cache("bridge_20261021.json", out)
    return out


def chain_city_from_bridge(br=None):
    br = br if br is not None else bridge()
    cc = {r: {} for r in ROOTS}
    cp = {r: {} for r in ROOTS}
    for b in br:
        for ch in b["chains"]:
            cc[ch][b["c"]] = cc[ch].get(b["c"], 0) + b["tags"][ch]
            cp[ch][b["p"]] = cp[ch].get(b["p"], 0) + b["tags"][ch]
    return {"chain_city": cc, "chain_prov": cp,
            "tag_rows_joinable": sum(b["n_row"] for b in br)}


def name_chain(br=None):
    """企业名 -> [[chain, city], ...]（与旧版 panel.name_chain 同构）"""
    br = br if br is not None else bridge()
    out = {}
    for b in br:
        out.setdefault(b["nm"], []).extend([[ch, b["c"]] for ch in b["chains"]])
    return out


def ent_chain_map(br=None):
    """credit_code -> [root chain...]"""
    br = br if br is not None else bridge()
    return {b["cc"]: b["chains"] for b in br if b["cc"]}


def chain_city_prov(force=False):
    """一次扫描 tags×base，同时得到链×城 与 链×省 的标签行计数。

    返回 {"rows": [{province, city, c<INBxxxx>...}], "chain_city": {chain:{city:n}},
          "chain_prov": {chain:{prov:n}}, "tag_rows_joinable": n}
    口径：与旧版 panel.chain_city 一致——**标签行计数**（非 credit_code 去重），
    多链企业的同一行标签按链各计一次。
    """
    d = None if force else load_cache("chain_city_prov_20261021.json")
    if d is not None:
        return d
    flags = ", ".join(f"SUM(t.industry_code LIKE '%%{r}%%') AS c_{r}" for r in ROOTS)
    sql = (f"SELECT b.province p, b.city c, COUNT(*) AS n_rows, {flags} FROM " + GKX + "dwd_org_industry_tags t "
           "STRAIGHT_JOIN " + GKX + "dwd_org_base_info b "
           "ON b.external_id = t.credit_code COLLATE utf8mb4_0900_ai_ci "
           "WHERE t.is_deleted=0 AND b.is_deleted=0 GROUP BY 1,2")
    rows = qd(sql)
    cc = {r: {} for r in ROOTS}
    cp = {r: {} for r in ROOTS}
    for row in rows:
        for r in ROOTS:
            n = int(row["c_" + r] or 0)
            if not n:
                continue
            cc[r][row["c"]] = cc[r].get(row["c"], 0) + n
            cp[r][row["p"]] = cp[r].get(row["p"], 0) + n
    d = {"rows": rows, "chain_city": cc, "chain_prov": cp,
         "tag_rows_joinable": sum(int(row["n_rows"] or 0) for row in rows)}
    save_cache("chain_city_prov_20261021.json", d)
    return d


def chain_tag_universe():
    """链宇宙标签行数（2,283,762 行，逐链 SUM，不 JOIN 主档）。"""
    d = load_cache("chain_tag_universe_20261021.json")
    if d is None:
        sel = ", ".join(f"SUM(industry_code LIKE '%%{r}%%') AS c_{r}" for r in ROOTS)
        row = qd(f"SELECT COUNT(*) n_all, COUNT(DISTINCT credit_code) n_cc, {sel} "
                 f"FROM " + GKX + "dwd_org_industry_tags WHERE is_deleted=0")[0]
        d = {"n_all": int(row["n_all"]), "n_cc": int(row["n_cc"]),
             "counts": {r: int(row["c_" + r] or 0) for r in ROOTS}}
        save_cache("chain_tag_universe_20261021.json", d)
    return d


def ent_chain_for(codes, tag="subset"):
    """给定 credit_code 子集，返回 {credit: [root chain...]}。

    反向取数：只用 IN 列表过滤标签表（一次全表扫），不 JOIN 主档——因为主档侧
    credit_code 的排序规则不同，且 tags.credit_code 无索引，JOIN 会退化成嵌套循环。
    """
    codes = [c for c in dict.fromkeys(codes) if c]
    d = load_cache(f"ent_chain_{tag}_20261021.json")
    if d is not None:
        return d
    out = {}
    step = 8000
    for i in range(0, len(codes), step):
        chunk = codes[i:i + step]
        ph = ",".join(["%s"] * len(chunk))
        rows = q("SELECT credit_code, industry_code FROM " + GKX +
                 "dwd_org_industry_tags WHERE is_deleted=0 AND credit_code IN (" + ph + ")", chunk)
        for cc, ic in rows:
            if not cc or not ic:
                continue
            got = out.setdefault(cc, set())
            for code in _codes(ic):
                got.add(code[:7])
    out = {k: sorted(v) for k, v in out.items()}
    save_cache(f"ent_chain_{tag}_20261021.json", out)
    return out


def _codes(s):
    """解析 industry_code 的列表字面量（"['INB1306','INB1209']"）。"""
    if not s:
        return []
    txt = str(s)
    return [t.strip(" '\"") for t in txt.strip("[]").split(",") if t.strip(" '\"")]


# ---------------------------------------------------------------- 统计工具
def num(v, default=0.0):
    if v is None or v == "":
        return default
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def minmax(vals):
    lo, hi = min(vals), max(vals)
    if hi - lo <= 1e-12:
        return [0.5 for _ in vals]
    return [(v - lo) / (hi - lo) for v in vals]


def stats(vals, nd=4):
    vals = [v for v in vals if v is not None]
    if not vals:
        return {"n": 0}
    s = sorted(vals)
    n = len(s)
    return {"n": n, "min": round(s[0], nd), "max": round(s[-1], nd),
            "mean": round(sum(s) / n, nd), "median": round(statistics.median(s), nd),
            "p90": round(s[int(0.9 * (n - 1))], nd),
            "n_zero": sum(1 for x in s if x == 0),
            "n_distinct": len({round(x, 6) for x in s})}


def jstats(vals, nd=4):
    return stats(vals, nd)


def spearman(xs, ys):
    def rank(a):
        order = sorted(range(len(a)), key=lambda i: a[i])
        r = [0.0] * len(a)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and a[order[j + 1]] == a[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    rx, ry = rank(xs), rank(ys)
    n = len(xs)
    mx, my = sum(rx) / n, sum(ry) / n
    num_ = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return round(num_ / den, 4) if den else None


if __name__ == "__main__":
    print("tree", len(tree()), "roots", len(chain_names()))
    print("base", len(base_rows()))
    print("tag universe", chain_tag_universe())
    d = chain_city_prov()
    print("joinable tag rows", d["tag_rows_joinable"])
    print("chain_city INB1306", d["chain_city"]["INB1306"])
    print("chain_prov INB1306", d["chain_prov"]["INB1306"])

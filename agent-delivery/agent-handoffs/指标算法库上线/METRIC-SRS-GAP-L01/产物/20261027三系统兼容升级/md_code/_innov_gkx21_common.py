#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""20261021 版 · INNOV 簇（A-10 批）自包含工具：只读三方库 gkx，禁引 demo。

为什么另起一个模块：`_innov_w6_common.py` 通过 `_innov_common.py` 间接依赖旧版
`_devdb`（其 schema 全部指向 demo），20261021 版铁律禁止该路径。本模块只依赖
`_gkxdb.gkx()`（该模块见 demo 直接 raise），不 import 任何旧版连接助手。

口径与旧版逐字一致：`norm01` / `holt_fit` / `iter_papers` 的字段契约与
`_innov_w6_common.py` 相同，保证「换源不换算法」时读数可比。
"""
from __future__ import annotations

import json
import math
import re
import statistics
from pathlib import Path

import _gkxdb

HERE = Path(__file__).parent
CACHE = HERE / "_snapshots21"
CACHE.mkdir(exist_ok=True)

GKX = "gkx."

# 机构性质判定：先产业后学术的判定顺序由调用方保证（006 §2.1）
ACA_RX = re.compile(
    r"大学|学院|研究院|研究所|科学院|实验室|学校|研究中心|医院|学会|中心|委员会|"
    r"University|Universit|Institute|College|School|Hospital|Academy|Laborator|"
    r"Istituto|Instituto|Consiglio|Ricerche|Fundaci",
    re.I,
)
IND_RX = re.compile(
    r"公司|集团|有限|股份|控股|实业|工厂|企业|厂$|"
    r"Inc\.?|Ltd\.?|LLC|Corp\.?|Co\.,|Company|Group|GmbH"
)
MED_RX = re.compile(r"医院|医科|中医|药|护理|临床|肿瘤|口腔|疾控|卫生|医学|Medical|Hospital|Clinic")


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
    """字典行（列名做 key）。"""
    cur = _gkxdb.gkx()
    try:
        cur.execute(sql, args) if args else cur.execute(sql)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    finally:
        cur.close()


def count(table):
    """行数只读库存 json（GKX_INVENTORY.json），不重复 COUNT(*) 大表。"""
    inv = json.loads((HERE.parent / "_work_gkx21" / "GKX_INVENTORY.json").read_text(encoding="utf-8"))
    rec = inv.get(table)
    return int(rec["rows"]) if rec else None


# ---------------------------------------------------------------- 缓存与产物
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
    path = HERE / f"{metric_id}_out.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return path


# ---------------------------------------------------------------- 数值工具
def f(x):
    """Decimal → float，None 保留 None。"""
    if x is None:
        return None
    try:
        return float(x)
    except (TypeError, ValueError):
        return x


def num(v, default=0.0):
    if v is None or v == "":
        return default
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def norm01(xs) -> list:
    """min-max 归一到 [0,1]；常数序列返回 0.5（无信息，不制造 0/1 极值）。"""
    xs = [f(x) for x in xs]
    if not xs:
        return []
    lo, hi = min(xs), max(xs)
    if hi - lo == 0:
        return [0.5 for _ in xs]
    return [(x - lo) / (hi - lo) for x in xs]


minmax = norm01


def pct(xs, p):
    xs = sorted(f(x) for x in xs if x is not None)
    if not xs:
        return None
    k = (len(xs) - 1) * p
    lo, hi = math.floor(k), math.ceil(k)
    return round(xs[lo] + (xs[hi] - xs[lo]) * (k - lo), 4)


def dist(xs):
    """与旧版 `_innov_common.dist` 同构的摘要量。"""
    xs = [f(x) for x in xs if x is not None]
    if not xs:
        return {"n": 0}
    return {
        "n": len(xs),
        "min": round(min(xs), 4),
        "max": round(max(xs), 4),
        "mean": round(statistics.mean(xs), 4),
        "median": round(statistics.median(xs), 4),
        "p10": pct(xs, 0.10),
        "p90": pct(xs, 0.90),
        "n_pos": sum(1 for x in xs if x > 0),
        "n_distinct": len(set(xs)),
    }


stats = dist


def holt_fit(series, h: int = 2, level: float = 0.80) -> dict:
    """Holt 线性趋势指数平滑 + 解析预测区间（与 004 §2.6.1 公式一致）。

    (alpha, beta) 在 {0.1..0.9} 上按一步残差 SSE 网格搜索。
    80% 区间：point ± 1.2816 * sigma * sqrt(1 + 0.15*k)，k 从 0 起。
    """
    ys = [f(x) for x in series]
    n = len(ys)
    if n < 4:
        return None

    best = None
    for ai in range(1, 10):
        for bi in range(1, 10):
            a, b = ai / 10, bi / 10
            lvl, tr = ys[0], ys[1] - ys[0]
            sse = 0.0
            steps = 0
            for t in range(1, n):
                pred = lvl + tr
                e = ys[t] - pred
                sse += e * e
                steps += 1
                prev = lvl
                lvl = a * ys[t] + (1 - a) * (lvl + tr)
                tr = b * (lvl - prev) + (1 - b) * tr
            if best is None or sse < best["sse"] - 1e-12:
                best = {"sse": sse, "alpha": a, "beta": b, "level": lvl, "trend": tr, "n": steps}

    sd = (best["sse"] / max(best["n"] - 2, 1)) ** 0.5
    z = 1.2816 if abs(level - 0.80) < 1e-9 else 1.96
    point = [best["level"] + (k + 1) * best["trend"] for k in range(h)]
    lo = [point[k] - z * sd * (1 + 0.15 * k) ** 0.5 for k in range(h)]
    hi = [point[k] + z * sd * (1 + 0.15 * k) ** 0.5 for k in range(h)]
    return {"point": [round(x, 2) for x in point],
            "lo80": [round(x, 2) for x in lo],
            "hi80": [round(x, 2) for x in hi],
            "resid_sd": round(sd, 3),
            "alpha": best["alpha"], "beta": best["beta"]}


def sql_list(xs) -> str:
    """把 Python 列表渲染成 SQL 的逗号分隔字面量（仅用于受控常量，不做转义防护）。"""
    out = []
    for x in xs:
        if isinstance(x, (int, float)):
            out.append(str(x))
        else:
            out.append("'" + str(x).replace("'", "''") + "'")
    return ",".join(out)


def parse_kw(raw) -> list:
    """解析 keywords 字段：优先 JSON 数组，退化按中英文分隔符切分。"""
    if raw is None:
        return []
    s = str(raw).strip()
    if not s:
        return []
    try:
        v = json.loads(s)
        if isinstance(v, list):
            return [str(t).strip() for t in v if str(t).strip()]
        if isinstance(v, str):
            return [t.strip() for t in re.split(r"[;,；，、|]", v) if t.strip()]
    except Exception:
        pass
    return [t.strip() for t in re.split(r"[;,；，、|]", s) if t.strip()]


# ---------------------------------------------------------------- 论文逐篇
def _iter_paper_rows(size: int = 8000):
    off = 0
    while True:
        rows = q(
            "SELECT id, zh_name, en_name, cover_year_start AS y, author_info_list AS ai "
            "FROM " + GKX + "dwd_zh_paper ORDER BY id LIMIT %s OFFSET %s",
            (size, off),
        )
        if not rows:
            return
        for r in rows:
            yield r
        if len(rows) < size:
            return
        off += size


def iter_papers(bag: dict):
    """逐篇产出 {id, year, title, insts, authors:[(name, [parts])], bad}。

    与旧版 `_innov_common.iter_papers` 的字段契约保持一致：
    - insts：篇内去重机构名集合（>=4 字）
    - authors：[(作者名, [机构片段...])]，无名作者跳过
    - bad_json 计入 bag，不静默吞掉
    """
    for r in _iter_paper_rows():
        # 列序固定为 (id, zh_name, en_name, y, ai)；_gkxdb.gkx() 返回的是元组行
        rid, zh_name, en_name, yr, ai = r
        insts = set()
        authors = []
        bad = False
        if ai:
            try:
                arr = json.loads(ai)
            except Exception:
                bag["bad_json"] = bag.get("bad_json", 0) + 1
                arr = []
                bad = True
            if isinstance(arr, list):
                for a in arr:
                    if not isinstance(a, dict):
                        continue
                    nm = (a.get("zh_name") or a.get("en_name") or "").strip()
                    aff = (a.get("institution") or a.get("affiliation") or "").strip()
                    parts = [p.strip() for p in re.split(r"[;；]", aff) if len(p.strip()) >= 4]
                    insts.update(parts)
                    if nm:
                        authors.append((nm, parts))
        yield {
            "id": rid,
            "year": yr,
            "title": (zh_name or en_name or ""),
            "insts": insts,
            "authors": authors,
            "bad": bad,
        }


def org_name_city():
    """机构名 → 城市，**按 name_cn 去重**（189,116 行只有 189,069 个不同名称）。

    gkx.dwd_org_base_info 有 47 个重名（DATA_FACTS §3.5），直接按名称 JOIN 会让
    这些企业的专利被重复计数。去重规则：同名多行取「城市出现次数最多」的那个，
    次数相同时取字典序最小，保证结果可复现；冲突明细随返回值一并披露。
    """
    d = load_cache("org_name_city_20261021.json")
    if d is None:
        rows = q("SELECT name_cn, city, COUNT(*) n FROM " + GKX +
                 "dwd_org_base_info GROUP BY name_cn, city")
        byname = {}
        for name, city, n in rows:
            if not name:
                continue
            byname.setdefault(name, []).append([city or "", int(n or 0)])
        pick, conflicts = {}, []
        city_totals = {}
        for name, cand in byname.items():
            if len(cand) == 1:
                pick[name] = cand[0][0]
            else:
                cand.sort(key=lambda x: (-x[1], x[0]))
                pick[name] = cand[0][0]
                if len({c[0] for c in cand}) > 1:
                    conflicts.append({"name": name, "candidates": cand, "picked": cand[0][0]})
        for cand in byname.values():
            for city, n in cand:
                city_totals[city] = city_totals.get(city, 0) + n
        d = {"map": pick, "dup_name_conflicts": conflicts, "city_totals": city_totals,
             "n_rows": sum(x[1] for cand in byname.values() for x in cand),
             "n_names": len(pick)}
        save_cache("org_name_city_20261021.json", d)
    return d


if __name__ == "__main__":
    print("gkx tables:", q1("SELECT COUNT(*) FROM information_schema.tables "
                            "WHERE table_schema='gkx'"))
    print("inventory dwd_zh_paper:", count("dwd_zh_paper"))
    nm = org_name_city()
    print("name map rows/names:", nm["n_rows"], nm["n_names"], "conflicts:", len(nm["dup_name_conflicts"]))

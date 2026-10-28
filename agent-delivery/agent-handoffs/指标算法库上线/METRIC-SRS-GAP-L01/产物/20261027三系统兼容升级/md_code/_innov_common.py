#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A-12 批（空间 / 孵化 / 因子混簇）共用算路：只读三方库 gkx，禁引 demo。

设计原则
--------
1. 唯一连库入口 `_gkxdb.gkx()`（该模块对演示/造数 schema 直接 raise）；本文件所有 SQL 写全
   `gkx.<表名>`，不传 database / charset。
2. `dwd_org_base_info`（189,116 行）与 `dwd_patent` 聚合面板各扫一次落缓存，
   本簇 5 个指标共享；专利面板由 `_build_patent_panel_innov.py` 流式生成。
3. 行政区名统一在 Python 侧归一（trim + 占位符 + 市级别名 + 区县误落检测），
   并用 `gkx.dwd_dim_admin_area` 做一次规范名核对，归一前后逐项计数写进 out.json。
4. 行数只读 `_work_gkx21/GKX_INVENTORY.json`，本文件不重复摸大表。

缓存目录 `_snapshots21/`（与旧版 `_snapshots/` 物理隔离）。
"""
from __future__ import annotations

import json
import statistics
from pathlib import Path

import _gkxdb

CACHE = Path(__file__).parent / "_snapshots21"
CACHE.mkdir(exist_ok=True)
GKX = "gkx."

# 缺失占位符：gkx 同一张表内 'NULL' / 'null' 混用，必须大小写不敏感
PLACEHOLDERS = ("NULL", "", "NONE", "-")
CITY_SUFFIX = ("市", "地区", "州", "盟")
CITY_ALIAS = {
    "深圳": "深圳市", "广州": "广州市", "东莞": "东莞市", "惠州": "惠州市",
    "北京": "北京市", "上海": "上海市", "天津": "天津市", "重庆": "重庆市",
    "杭州": "杭州市", "南京": "南京市", "武汉": "武汉市", "成都": "成都市",
    "西安": "西安市", "长沙": "长沙市", "郑州": "郑州市", "济南": "济南市",
    "合肥": "合肥市", "福州": "福州市", "厦门": "厦门市", "苏州": "苏州市",
}


# ---------------------------------------------------------------- 连接与查询
def q(sql, args=None):
    cur = _gkxdb.gkx()
    try:
        cur.execute(sql, args) if args else cur.execute(sql)
        return cur.fetchall()
    finally:
        cur.close()


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
def load_cache(name):
    p = CACHE / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def save_cache(name, obj):
    p = CACHE / name
    p.write_text(json.dumps(obj, ensure_ascii=False, default=str), encoding="utf-8")
    return p


def write_out(metric_id, payload):
    path = Path(__file__).parent / f"{metric_id}_out.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return path


# ---------------------------------------------------------------- 主档
def base():
    """189,116 行主档，字段：org_id, name_cn, city, province, area, org_type, reg_status。

    不写 `is_deleted=0`：该表 is_deleted 全为 0（`_work_gkx21/DATA_FACTS_gkx21.md` §3.2），
    加了只增成本；行数与库存 189,116 对齐作为完整性断言。
    """
    d = load_cache("innov_base_20261021.json")
    if d is None:
        rows = qd("SELECT org_id, name_cn, city, province, area, org_type, reg_status "
                  "FROM " + GKX + "dwd_org_base_info")
        d = rows
        save_cache("innov_base_20261021.json", d)
    return d


def admin_dim():
    """行政区维（6 级，20,000 行）的四市 canonical (city_name, area_name) 集合。"""
    d = load_cache("innov_admin_dim_20261021.json")
    if d is None:
        rows = qd("SELECT DISTINCT city_name, area_name FROM " + GKX + "dwd_dim_admin_area "
                  "WHERE city_name IN ('深圳市','广州市','东莞市','惠州市')")
        d = [[r["city_name"], r["area_name"]] for r in rows]
        save_cache("innov_admin_dim_20261021.json", d)
    return d


def panel():
    """专利共享面板（年份 / IPC 小类 / 申请人），由 _build_patent_panel_innov.py 生成。"""
    d = load_cache("patent_panel_innov_20261021.json")
    if d is None:
        raise RuntimeError("缺专利面板缓存：先跑 code/_build_patent_panel_innov.py")
    return d


# ---------------------------------------------------------------- 行政区名归一
def clean(v):
    s = "" if v is None else str(v).strip()
    return "" if s.upper() in PLACEHOLDERS else s


def norm_city(v):
    """城市名归一：别名补「市」；区县名误落到 city 的返回空串（交由 area 处置）。"""
    s = clean(v)
    if not s:
        return ""
    if s in CITY_ALIAS:
        return CITY_ALIAS[s]
    # 「南山区 / 宝安县」这类区县级字面落在 city 列：person 不猜城市，直接置空，
    # 由 city_norm_probe 计数披露（宁可少一个区县，不可把区县当城市）。
    if s.endswith(("区", "县", "旗")) and not s.endswith("地区"):
        return ""
    if not s.endswith(CITY_SUFFIX) and len(s) <= 6:
        # 无后缀的短名（如「深圳」）补「市」，其余保持原样
        if s in CITY_ALIAS:
            return CITY_ALIAS[s]
    return s


def norm_area(v, city=""):
    """区县名归一：清除占位符；把「市辖区 / 整市名」视为无区县。"""
    s = clean(v)
    if not s:
        return ""
    if s in ("市辖区", "市本级", "县"):
        return ""
    if s == city or (s.endswith("市") and s == norm_city(city)):
        return ""
    return s


def city_norm_probe(rows, dim=None):
    """归一前后计数：字面 'NULL'、空值、别名修正、区县误落 city、dim 命中率。"""
    raw_city, raw_area = {}, {}
    literal_null_city = literal_null_area = 0
    fixed_alias = dropped_area_as_city = dropped_city_as_area = 0
    for r in rows:
        c_raw, a_raw = r.get("city"), r.get("area")
        if c_raw is not None and str(c_raw).strip().upper() == "NULL":
            literal_null_city += 1
        if a_raw is not None and str(a_raw).strip().upper() == "NULL":
            literal_null_area += 1
        raw_city[str(c_raw)] = raw_city.get(str(c_raw), 0) + 1
        raw_area[str(a_raw)] = raw_area.get(str(a_raw), 0) + 1
        c, a = clean(c_raw), clean(a_raw)
        nc = norm_city(c_raw)
        if c and nc and nc != c:
            fixed_alias += 1
        if c and not nc:
            dropped_city_as_area += 1
        if a and not norm_area(a_raw, nc):
            dropped_area_as_city += 1
    regions = {(norm_city(r.get("city")), norm_area(r.get("area"), norm_city(r.get("city"))))
               for r in rows}
    regions = {x for x in regions if x[0] and x[1]}
    dim = dim if dim is not None else admin_dim()
    dim_set = {(d[0], d[1]) for d in dim}
    hit = len(regions & dim_set)
    return {
        "city_distinct_raw": len(raw_city),
        "area_distinct_raw": len(raw_area),
        "city_literal_NULL_rows": literal_null_city,
        "area_literal_NULL_rows": literal_null_area,
        "city_empty_rows": raw_city.get("None", 0) + raw_city.get("", 0),
        "city_alias_fixed_rows": fixed_alias,
        "city_value_is_district_rows": dropped_city_as_area,
        "area_value_is_city_rows": dropped_area_as_city,
        "regions_after_norm": len(regions),
        "regions_in_admin_dim": hit,
        "regions_not_in_admin_dim": len(regions) - hit,
        "admin_dim_note": "gkx.dwd_dim_admin_area 仅 20,000 行（6 级抽样），未全量覆盖全国区县；"
                          "dim 未命中不等于区县名错误。",
    }


# ---------------------------------------------------------------- 统计工具
def minmax(vals: dict):
    if not vals:
        return {}
    lo, hi = min(vals.values()), max(vals.values())
    if hi == lo:
        return {k: 50.0 for k in vals}
    return {k: (v - lo) / (hi - lo) * 100 for k, v in vals.items()}


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


def pct(vals, p):
    if not vals:
        return 0
    k = int(len(vals) * p)
    return vals[min(k, len(vals) - 1)]

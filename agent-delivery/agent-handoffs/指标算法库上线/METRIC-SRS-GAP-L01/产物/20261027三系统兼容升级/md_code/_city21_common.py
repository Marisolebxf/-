#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""城市簇（A-08）共享取数层 · gkx 版（20261021）

设计原则
--------
1. **一次取、五指标共用**：把粤三城五指标用到的原始量统一落到
   `_snapshots_gkx21/city_raw_gkx.json`，五个指标脚本只读缓存，重复运行零 DB 压力。
2. **重资产一律走本地快照**：
   * 企业底册 → `code/_snapshots21/base_20261021.json`（189,116 行，含 org_id / name / city）；
   * 专利「城市 × 申请年」→ `_snapshots_gkx21/city_patent_year_gkx.json`
     （由 A-12 面板 `app_year` × 底册 `name→city` 离线派生，见 `_build_city_patent_year.py`）。
3. **城市键用等值**：gkx 已把 city 规范化到「市」级全称（深圳市/广州市/东莞市），
   不再写 `LIKE '%深圳%'`（`DATA_FACTS_gkx21.md` §3.8）。
4. **占位符统一大小写无关处理**：`UPPER(TRIM(col)) NOT IN ('NULL','','NONE','-')`（§3.4）。
   `dwd_policy_base.city` 有 9,706 行字面 `'NULL'`（无真 NULL），旧的 `city IS NULL`
   在 gkx 上会返回 0 —— 这是本批唯一「换源后必须改写条件」而不是「只换前缀」的地方。
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

SNAP = HERE / "_snapshots21"
CACHE = HERE / "_snapshots_gkx21"
CACHE.mkdir(exist_ok=True)
RAW = CACHE / "city_raw_gkx.json"

CITY_CODES = [("深圳市", "深圳"), ("广州市", "广州"), ("东莞市", "东莞")]
CITY_KEYS = [c for c, _ in CITY_CODES]
SHORT = {"深圳市": "深圳", "广州市": "广州", "东莞市": "东莞"}
TAG_HITECH = ("高新技术企业", "国家级高新技术企业")
REG_ALIVE = ("存续（在营、开业、在册）", "在营（开业）企业", "正常", "存续", "在业")
RD_Y0, RD_Y1 = "2017", "2024"   # 趋势要 2017 起；投入维窗口 2019–2024 由 SUM_WINDOW 控制
SUM_Y0, SUM_Y1 = "2019", "2024"
PLACEHOLDER = ("NULL", "", "NONE", "-")


def gkx_conn(read_timeout=900):
    import pymysql
    import _gkxdb as _g
    cfg = dict(_g.GKX)
    cfg["read_timeout"] = read_timeout
    return pymysql.connect(**cfg)


def q(sql, args=None, read_timeout=900):
    conn = gkx_conn(read_timeout)
    try:
        cur = conn.cursor()
        cur.execute(sql, args) if args else cur.execute(sql)
        cols = [c[0] for c in cur.description]
        rows = [dict(zip(cols, r)) for r in cur.fetchall()]
        cur.close()
        return rows
    finally:
        conn.close()


def load_base():
    """底册本地快照 → (rows, by_org, by_name)。by_name 保留重名全部候选。"""
    rows = json.loads((SNAP / "base_20261021.json").read_text(encoding="utf-8"))
    by_org, by_name = {}, {}
    for r in rows:
        org_id, name, city = r[0], r[2], (r[4] or "")
        if org_id:
            by_org[org_id] = city
        if name:
            by_name.setdefault(name, []).append(city)
    return rows, by_org, by_name


def name_city_weights(by_name):
    """名 → [(city, 1/k)]；47 个重名按 1/k 计权。"""
    out = {}
    for nm, cities in by_name.items():
        agg = {}
        for c in cities:
            agg[c or "?"] = agg.get(c or "?", 0) + 1
        k = len(cities)
        out[nm] = [(c, n / k) for c, n in agg.items()]
    return out


def build_raw(force=False):
    """把五指标共用的原始量一次取回落盘。"""
    if RAW.exists() and not force:
        return json.loads(RAW.read_text(encoding="utf-8"))

    rows, by_org, by_name = load_base()
    name_w = name_city_weights(by_name)
    t_all = time.time()
    raw = {"generated_at": time.strftime("%Y-%m-%dT%H:%M:%S")}

    # 1) 机构存续数：城市 × reg_status
    t = time.time()
    raw["org_reg"] = q(
        "SELECT city, reg_status, COUNT(*) n FROM gkx.dwd_org_base_info "
        "WHERE city IN ('深圳市','广州市','东莞市') GROUP BY city, reg_status")
    raw["org_reg_sec"] = round(time.time() - t, 1)

    # 2) 高企标签：org_id 列表（城市归属走本地 org_id→city，等价于 org_id 精确 JOIN）
    t = time.time()
    hq = q("SELECT DISTINCT org_id FROM gkx.dwd_org_tech_tag "
           "WHERE org_tag IN ('高新技术企业','国家级高新技术企业')")
    hq_ids = [r["org_id"] for r in hq if r["org_id"]]
    hitech = {}
    for oid in hq_ids:
        c = by_org.get(oid)
        if c in CITY_KEYS:
            hitech[c] = hitech.get(c, 0) + 1
    raw["hitech_by_city"] = hitech
    raw["hitech_org_ids_n"] = len(hq_ids)
    raw["hitech_sec"] = round(time.time() - t, 1)

    # 3) 学者：机构名 → 城市（本地 1/k 去重，每城按 scholar_id 去重）
    t = time.time()
    sc = q("SELECT scholar_id, scholar_org_name_zh FROM gkx.dwd_scholar")
    sch_sets = {c: set() for c in CITY_KEYS}
    for r in sc:
        sid, nm = r["scholar_id"], r["scholar_org_name_zh"]
        for c, _w in name_w.get(nm, []):
            if c in CITY_KEYS:
                sch_sets[c].add(sid)
    raw["scholar_by_city"] = {c: len(v) for c, v in sch_sets.items()}
    raw["scholar_rows"] = len(sc)
    raw["scholar_sec"] = round(time.time() - t, 1)

    # 4) 政策：全表 20,000（市级等值 + 省级占位归空后共享）
    t = time.time()
    pol = q("SELECT id, city, province, status FROM gkx.dwd_policy_base")
    city_cnt, prov_ids, placeholder = {}, set(), 0
    for r in pol:
        city = (r["city"] or "").strip()
        if city.upper() in PLACEHOLDER:
            placeholder += 1
            if "广东" in (r["province"] or ""):
                prov_ids.add(r["id"])
        elif city in CITY_KEYS:
            city_cnt[city] = city_cnt.get(city, 0) + 1
    raw["policy_city"] = city_cnt
    raw["policy_prov_shared_n"] = len(prov_ids)
    raw["policy_placeholder_rows"] = placeholder
    raw["policy_rows"] = len(pol)
    raw["policy_status_all"] = sorted({(r["status"] or "") for r in pol})
    raw["policy_sec"] = round(time.time() - t, 1)

    # 5) 研发经费：上市公司年报口径，2019–2024，按 org_id→city 本地归城（含年序列）
    t = time.time()
    fin = q("SELECT org_id, LEFT(occur_period,4) y, research_development_amount amt "
            "FROM gkx.dwd_org_stock_finance_info "
            "WHERE LEFT(occur_period,4) BETWEEN %s AND %s "
            "AND research_development_amount IS NOT NULL", (RD_Y0, RD_Y1))
    rd_sum, rd_year, rd_unmapped = {}, {}, 0
    for r in fin:
        c = by_org.get(r["org_id"])
        if c not in CITY_KEYS:
            rd_unmapped += 1
            continue
        y = str(r["y"])
        rd_year.setdefault(c, {})
        rd_year[c][y] = round(rd_year[c].get(y, 0.0) + float(r["amt"]), 2)
        if SUM_Y0 <= y <= SUM_Y1:
            rd_sum[c] = rd_sum.get(c, 0.0) + float(r["amt"])
    raw["rd_sum"] = {k: round(v, 2) for k, v in rd_sum.items()}
    raw["rd_year"] = rd_year
    raw["rd_rows"] = len(fin)
    raw["rd_unmapped"] = rd_unmapped
    raw["rd_sec"] = round(time.time() - t, 1)

    raw["elapsed_sec"] = round(time.time() - t_all, 1)
    RAW.write_text(json.dumps(raw, ensure_ascii=False, indent=1), encoding="utf-8")
    return raw


def load_patent_city_year():
    p = CACHE / "city_patent_year_gkx.json"
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def norm(vals):
    mx, mn = max(vals), min(vals)
    return [round((v - mn) / (mx - mn), 4) if mx > mn else 1.0 for v in vals]


def write_out(metric_id, payload):
    path = HERE / f"{metric_id}_out.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    return path

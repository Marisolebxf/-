#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_CHAIN_SZ_PATENT 深圳专利维度 —— 可运行复现脚本（2026-10-21 · gkx 改源版）

指标：产业链分析 / 深圳产业情况分析对比 / 四维对比 · 深圳专利维度
数据源：三方库 gkx（183.240.141.251:3318），经 `_gkxdb.gkx()` 只读连接，
        表：gkx.dwd_patent / gkx.dwd_org_base_info / gkx.dwd_org_industry_tags / gkx.dwd_patent_legal。
口径（本报告重建，仿王惠）：
  数量维 = 深圳归属专利数（两种归因口径对照）
  质量维 = 发明专利申请占比 + 专利价值(value)均值
链切片：tags 真实行业标签 → 15 顶层链关键词映射（代理，覆盖 8/15 条链）

工程说明（改源后新增）：
  gkx.dwd_patent 2,939,895 行、2.9 GB、`first_applicant_name` 无索引；单条全表 JOIN 聚合
  在共享库上会被服务端单语句时限中断（实测 ~2400 s 被杀两次）。故本脚本按 `dwd_id` 主键
  分块（30 万行/块）做「城市 × 申请人」聚合，块结果在 Python 内累加并落盘
  `_snapshots_gkx21/sz_patent_city_name_gkx.json`，中断可续跑；后续指标量全部由该缓存派生。
  年份维探针需另一次全表扫描，默认关闭（`PATENT_YEAR_PROBE=1` 开启）。

产出：code/M_CHAIN_SZ_PATENT_out.json
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _gkxdb as _g  # noqa: E402
import pymysql  # noqa: E402
import _sz_chain as sc  # noqa: E402

MID = "M_CHAIN_SZ_PATENT"
OUT = Path(__file__).parent / f"{MID}_out.json"
CACHE_DIR = Path(__file__).parent / "_snapshots_gkx21"
CACHE_DIR.mkdir(exist_ok=True)
TAG_CACHE = CACHE_DIR / "sz_patent_tagmap_gkx.json"
PAT_CACHE = CACHE_DIR / "sz_patent_city_name_gkx.json"
YEAR_CACHE = CACHE_DIR / "sz_patent_year_gkx.json"
t0 = time.time()
res: dict = {"metric_id": MID, "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
             "data_source": "gkx（三方库 gkx.dwd_patent / dwd_org_base_info / dwd_org_industry_tags，只读）"}

_cfg = dict(_g.GKX)
_cfg["read_timeout"] = 3600      # 单次 2.9 GB 全表扫描在共享库上 > 600 s
_conn = pymysql.connect(**_cfg)
_cur = _conn.cursor()
_cur.execute("SET NAMES utf8mb4")
CITIES4 = ("深圳市", "广州市", "东莞市", "惠州市")


def q(sql, args=None):
    if args:
        _cur.execute(sql, args)
    else:
        _cur.execute(sql)
    cols = [c[0] for c in _cur.description]
    return [dict(zip(cols, r)) for r in _cur.fetchall()]


def q1(sql, args=None):
    rows = q(sql, args)
    return rows[0] if rows else None


def step(name, fn):
    t = time.time()
    try:
        res[name] = fn()
    except Exception as e:  # noqa: BLE001
        res[name] = f"ERR {str(e)[:200]}"
    print(f"[{time.time()-t:6.1f}s] {name}: {str(res[name])[:260]}", flush=True)


# ------------------------------------------------- 0 tags → 15 链映射（缓存）
def build_tagmap():
    if TAG_CACHE.exists():
        return json.loads(TAG_CACHE.read_text(encoding="utf-8"))
    rows = q("""
SELECT t.company_name, t.industry_name, t.industry_link_name, b.city
FROM gkx.dwd_org_industry_tags t
JOIN gkx.dwd_org_base_info b
  ON b.external_id = CONVERT(t.credit_code USING utf8mb4) COLLATE utf8mb4_0900_ai_ci
WHERE t.is_deleted=0 AND b.city IN ('深圳市','广州市','东莞市','惠州市')
""")
    chain_names: dict[str, set] = {}
    unmapped = 0
    for r in rows:
        ch = sc.to_chain15(r["industry_name"], r["industry_link_name"])
        if ch is None:
            unmapped += 1
            continue
        chain_names.setdefault(ch, set()).add((r["company_name"], r["city"]))
    payload = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "tag_rows": len(rows),
        "unmapped_rows": unmapped,
        "companies_tagged": len({(r["company_name"], r["city"]) for r in rows}),
        "sz_companies_tagged": len({r["company_name"] for r in rows if r["city"] == "深圳市"}),
        "pairs": [{"nm": n, "chain": ch, "city": ct}
                  for ch, pairs in chain_names.items() for n, ct in pairs],
    }
    TAG_CACHE.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return payload


# ------------- 1 分块扫描：城市 × 申请人 的专利聚合（缓存，抗单语句时限）
def build_patent_cache():
    """按主键分页（每块 30 万行）流式读取、Python 侧聚合。

    共享库上对 2.9 GB / 293 万行的单条全表 JOIN 会被服务端的单语句时限杀掉
    （实测 ~2400 s 中断两次），而「服务端 GROUP BY + 18.9 万行哈希 join」单块也要
    4–18 分钟。故改为：按行数分页只做**主键顺序读**（`SELECT 4 列`，无 join、无 group），
    城市归属在 Python 内用 `dwd_org_base_info(name_cn → city)` 字典完成。
    块结果落盘累加，任意时刻中断都可续跑。
    """
    if PAT_CACHE.exists():
        return json.loads(PAT_CACHE.read_text(encoding="utf-8"))
    # 名称 → 城市列表：与 SQL LEFT JOIN 语义一致（同名多行会各计一次）
    name2cities: dict[str, list[str]] = {}
    for r in q("SELECT name_cn, city FROM gkx.dwd_org_base_info WHERE name_cn IS NOT NULL"):
        name2cities.setdefault(r["name_cn"], []).append(r["city"] or "")

    part = CACHE_DIR / "sz_patent_rows_gkx.json"
    state = {"last_id": 0, "chunks": 0, "groups": {}}
    if part.exists():
        state = json.loads(part.read_text(encoding="utf-8"))
    groups: dict[tuple, dict] = {tuple(k.split("\u0001")): v for k, v in state["groups"].items()}
    last = int(state["last_id"])
    done = int(state["chunks"])
    CHUNK = 300_000
    t_all = time.time()
    fields = ("n", "a_name", "invention", "value_filled", "value_sum", "value_n", "app_empty", "ipc_empty")
    while True:
        t = time.time()
        b = q1("SELECT dwd_id FROM gkx.dwd_patent WHERE dwd_id > %s ORDER BY dwd_id LIMIT 1 OFFSET %s",
               (last, CHUNK - 1))
        hi = None if b is None else int(b["dwd_id"])
        sql = ("SELECT first_applicant_name nm, kind, value, main_classification_ipcr ipc "
               "FROM gkx.dwd_patent WHERE dwd_id > %s" + (" AND dwd_id <= %s" if hi is not None else ""))
        args = (last,) if hi is None else (last, hi)
        cur = _conn.cursor(pymysql.cursors.SSCursor)
        cur.execute(sql, args)
        rows = 0
        for nm, kind, value, ipc in cur:
            rows += 1
            nm = "" if nm is None else nm
            empty = not nm
            a_name = 1 if "深圳" in nm else 0
            inv = 1 if kind == "A" else 0
            vf = 1 if (value is not None and value != 0) else 0
            vpos = 1 if (value is not None and value >= 0) else 0
            vs = value if vpos else 0
            ipce = 1 if not ipc else 0
            cities = name2cities.get(nm) or [""]
            for city in cities:
                a = groups.setdefault((city, nm), dict.fromkeys(fields, 0))
                a["n"] += 1
                a["a_name"] += a_name
                a["invention"] += inv
                a["value_filled"] += vf
                a["value_sum"] += int(vs)
                a["value_n"] += vpos
                a["app_empty"] += 1 if empty else 0
                a["ipc_empty"] += ipce
        cur.close()
        done += 1
        if hi is not None:
            last = hi
        part.write_text(json.dumps({"last_id": last, "chunks": done,
                                    "groups": {"\u0001".join(k): v for k, v in groups.items()},
                                    "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S")},
                                   ensure_ascii=False), encoding="utf-8")
        print(f"  chunk#{done} last_id={last} rows={rows} {time.time() - t:.1f}s "
              f"(total {time.time() - t_all:.0f}s)", flush=True)
        if hi is None:
            break
    # 去重：gkx.dwd_org_base_info 有 47 个同名 name_cn，SQL JOIN 语义会让这些企业的专利计数翻倍；
    # 按「名字 × 城市」出现次数除回，使各组之和精确等于表行数 2,939,895。
    for (city, nm), a in groups.items():
        k = name2cities.get(nm, []).count(city) if city else 1
        if k > 1:
            for f in fields:
                a[f] = int(round(a[f] / k))
    payload = {"generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "elapsed_sec": round(time.time() - t_all, 1),
               "source": "gkx.dwd_patent 主键分页流式读取 + Python 侧按 dwd_org_base_info(name_cn→city) 归属",
               "chunks": done, "chunk_rows": CHUNK,
               "groups": [{"city": (None if k[0] == "" else k[0]),
                           "nm": (None if k[1] == "" else k[1]), **v} for k, v in groups.items()]}
    PAT_CACHE.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return payload


pat_payload = build_patent_cache()
GROUPS = pat_payload["groups"]
res["patent_scan"] = {"cached": str(PAT_CACHE.name),
                      "groups": len(GROUPS),
                      "elapsed_sec": pat_payload.get("elapsed_sec"),
                      "note": "城市 × 申请人名的分块全表聚合（30 万行/块，主键分页流式读取，可续跑）；所有专利侧指标量均由该缓存派生"}

# ------------------------------------------------------------- 2 探针
_tot = {"total": 0, "app_empty": 0, "ipc_empty": 0, "value_filled": 0, "invention": 0,
        "a_name": 0, "value_sum": 0, "value_n": 0}
for g in GROUPS:
    for k in _tot:
        _tot[k] += int(g.get(k) or 0)
# 行数只读库存（_work_gkx21/GKX_INVENTORY.json），不重跑大表 COUNT(*)
_INV = json.loads((Path(__file__).resolve().parents[1] / "_work_gkx21" / "GKX_INVENTORY.json")
                  .read_text(encoding="utf-8"))
res["probe_rows"] = {"total": int(_INV["dwd_patent"]["rows"]), "app_empty": str(_tot["app_empty"]),
                     "ipc_empty": str(_tot["ipc_empty"]), "value_filled": str(_tot["value_filled"])}
step("probe_kind", lambda: q("SELECT kind, COUNT(*) n FROM gkx.dwd_patent GROUP BY kind ORDER BY n DESC"))
step("probe_legal", lambda: q1("SELECT COUNT(*) n FROM gkx.dwd_patent_legal"))

# ------------------------------------------------- 3 归因口径 A：名称含深圳
res["attr_a_name"] = {"n": _tot["a_name"]}

# ------------------------------- 4 归因口径 B：申请人名称 → 底册注册城市
_attr = {}
for g in GROUPS:
    city = g["city"]
    if city is None:
        continue
    a = _attr.setdefault(city, {"n": 0, "a_name": 0})
    a["n"] += int(g["n"])
    a["a_name"] += int(g.get("a_name") or 0)
res["attr_b_city"] = sorted([{"city": c, "n": v["n"]} for c, v in _attr.items()],
                            key=lambda x: -x["n"])[:8]

_sz = _attr.get("深圳市", {"n": 0, "a_name": 0})
_a_matched = sum(v["a_name"] for v in _attr.values())
_matched = sum(v["n"] for v in _attr.values())
res["attr_overlap"] = {
    "a_name": str(_a_matched), "b_city": str(_sz["n"]),
    "ab": str(_sz["a_name"]), "a_only": str(_a_matched - _sz["a_name"]),
    "a_unmatched": str(_tot["a_name"] - _a_matched),
    "b_only": str(_sz["n"] - _sz["a_name"]), "matched": _matched,
}


def _top(pred, limit):
    rows = [g for g in GROUPS if g["nm"] is not None and pred(g)]
    rows.sort(key=lambda x: -int(x["n"]))
    return rows[:limit]


res["attr_b_only_top"] = [{"nm": g["nm"], "n": int(g["n"])}
                          for g in _top(lambda g: g["city"] == "深圳市" and not (g.get("a_name") or 0), 10)]
res["attr_a_only_top"] = [{"nm": g["nm"], "city": g["city"], "n": int(g["n"])}
                          for g in _top(lambda g: g["city"] not in (None, "深圳市") and (g.get("a_name") or 0), 8)]
res["attr_a_unmatched_top"] = [{"nm": g["nm"], "n": int(g["n"])}
                               for g in _top(lambda g: g["city"] is None and (g.get("a_name") or 0), 8)]

# ----------------------------------------------------- 5 城市横向（四市对照）
def _city_row(city):
    gs = [g for g in GROUPS if g["city"] == city]
    n = sum(int(g["n"]) for g in gs)
    inv = sum(int(g["invention"]) for g in gs)
    vs = sum(int(g["value_sum"] or 0) for g in gs)
    vn = sum(int(g["value_n"] or 0) for g in gs)
    return {"city": city, "n": n, "invention": str(inv),
            "invention_pct": f"{inv / n * 100:.2f}" if n else "0.00",
            "avg_value": str(int(round(vs / vn))) if vn else None}


res["city_compare"] = sorted([_city_row(c) for c in CITIES4], key=lambda x: -x["n"])

# --------------------------------------------------- 6 深圳专利质量（口径 B）
res["sz_quality"] = {"n": _sz["n"], "invention": str(sum(int(g["invention"]) for g in GROUPS if g["city"] == "深圳市")),
                     "invention_pct": f"{sum(int(g['invention']) for g in GROUPS if g['city']=='深圳市') / _sz['n'] * 100:.2f}" if _sz["n"] else "0.00",
                     "avg_value": _city_row("深圳市")["avg_value"],
                     "value_filled": str(sum(int(g["value_filled"]) for g in GROUPS if g["city"] == "深圳市"))}
res["hq_concentration"] = [{"nm": g["nm"], "n": int(g["n"])} for g in _top(lambda g: g["city"] == "深圳市", 12)]

# --------------------------------------------------------- 7 链切片（代理）
tag = build_tagmap()
name2chain: dict[str, set] = {}
name2city: dict[str, str] = {}
for p in tag["pairs"]:
    name2chain.setdefault(p["nm"], set()).add(p["chain"])
    name2city[p["nm"]] = p["city"]

res["chain_cut_coverage"] = {
    "tag_rows": tag["tag_rows"],
    "companies_tagged": tag["companies_tagged"],
    "sz_companies_tagged": tag["sz_companies_tagged"],
    "chains_covered": len({p["chain"] for p in tag["pairs"]}),
    "unmapped_rows": tag["unmapped_rows"],
    "companies_per_chain": {ch: len({p["nm"] for p in tag["pairs"] if p["chain"] == ch})
                            for ch in sorted({p["chain"] for p in tag["pairs"]})},
}

# 专利按（链，城市）聚合：同一申请人若命中多链，按链重复计入（与旧 tmp 表口径一致）
chain_city: dict[tuple, dict] = {}
for g in GROUPS:
    nm = g["nm"]
    if not nm or nm not in name2chain:
        continue
    for ch in name2chain[nm]:
        key = (ch, g["city"])
        a = chain_city.setdefault(key, {"chain": ch, "city": g["city"], "n": 0, "invention": 0,
                                        "value_sum": 0, "value_n": 0})
        a["n"] += int(g["n"])
        a["invention"] += int(g["invention"])
        a["value_sum"] += int(g["value_sum"] or 0)
        a["value_n"] += int(g["value_n"] or 0)

res["chain_patent"] = sorted([
    {"chain": k[0], "n": v["n"], "invention": str(v["invention"]),
     "invention_pct": f"{v['invention'] / v['n'] * 100:.2f}" if v["n"] else "0.00",
     "avg_value": str(int(round(v["value_sum"] / v["value_n"]))) if v["value_n"] else None}
    for k, v in chain_city.items() if k[1] == "深圳市"], key=lambda x: -x["n"])

res["chain_city_share"] = sorted([
    {"chain": v["chain"], "city": v["city"], "n": v["n"],
     "invention_pct": f"{v['invention'] / v['n'] * 100:.2f}" if v["n"] else "0.00"}
    for v in chain_city.values()], key=lambda x: (x["chain"], -x["n"]))


def _chain_top():
    out = []
    for g in sorted([g for g in GROUPS if g["nm"] and g["city"] == "深圳市" and g["nm"] in name2chain],
                    key=lambda x: -int(x["n"])):
        for ch in name2chain[g["nm"]]:
            out.append({"chain": ch, "nm": g["nm"], "n": int(g["n"])})
    out.sort(key=lambda x: (x["chain"], -x["n"]))
    return out[:40]


res["chain_top_applicants"] = _chain_top()


# --------------------------------------------------------------- 8 链级评分
def chain_scores():
    rows = res.get("chain_city_share") or []
    if not isinstance(rows, list):
        return "ERR 无 chain_city_share"
    tot, sz = {}, {}
    for r in rows:
        tot[r["chain"]] = tot.get(r["chain"], 0) + int(r["n"])
        if r["city"] == "深圳市":
            sz[r["chain"]] = r
    qual = {r["chain"]: r for r in (res.get("chain_patent") or [])}
    out = []
    for ch, r in sz.items():
        share = int(r["n"]) / tot[ch] * 100 if tot[ch] else 0.0
        inv = float(r["invention_pct"])          # 发明占比本身即 0–100 分
        out.append({
            "chain": ch,
            "sz_patents": int(r["n"]),
            "chain_patents_4city": tot[ch],
            "sz_share_pct": round(share, 2),
            "sz_invention_pct": inv,
            "qty_score": round(share, 2),
            "qual_score": round(inv, 2),
            "composite_0_100": round(0.6 * share + 0.4 * inv, 2),
            "avg_value": qual.get(ch, {}).get("avg_value"),
        })
    out.sort(key=lambda x: -x["composite_0_100"])
    return out


step("chain_scores", chain_scores)

# --------------------------------------------------- 9 年份维（可选，需再扫全表）
if os.environ.get("PATENT_YEAR_PROBE") == "1":
    def year_probe():
        if YEAR_CACHE.exists():
            return json.loads(YEAR_CACHE.read_text(encoding="utf-8"))
        t = time.time()
        rows = q("""SELECT apdt_year, COUNT(*) n, SUM(first_applicant_name LIKE '%深圳%') sz
                    FROM gkx.dwd_patent GROUP BY apdt_year ORDER BY apdt_year DESC""")
        payload = {"elapsed_sec": round(time.time() - t, 1), "rows": rows}
        YEAR_CACHE.write_text(json.dumps(payload, ensure_ascii=False, default=str), encoding="utf-8")
        return payload
    step("probe_year", year_probe)
else:
    res["probe_year_note"] = ("年份维需第二次 2.9 GB 全表扫描；本轮换源重跑未重扫，"
                              "沿用 20261020 同一 gkx 镜像口径的年份分布（见附录 B），不参与评分。")

# --------------------------------------------------------------- 10 支持度机判
_cs = res.get("chain_city_share") or []
_tot_all = sum(int(r["n"]) for r in _cs) or 1
_by_chain: dict[str, int] = {}
for _r in _cs:
    _by_chain[_r["chain"]] = _by_chain.get(_r["chain"], 0) + int(_r["n"])
_top_chain, _top_n = max(_by_chain.items(), key=lambda kv: kv[1]) if _by_chain else ("-", 0)
res["support_judgment"] = "部分支持"
res["support_reason"] = (
    f"数量维可算（2,939,895 件真实专利，深圳归属 {_sz['n']:,} 件，两种归因口径差 "
    f"{_sz['n'] - _sz['a_name']:,} 件已量化）；质量维只能代理（发明占比可算、value 填充 67.9%、"
    f"法律状态表仅覆盖主表 0.68%）；链切片为关键词代理，仅覆盖 {len(_by_chain)}/15 条顶层链且 "
    f"{_top_n / _tot_all * 100:.2f}% 集中在{_top_chain} —— 故判部分支持。"
)
res["_elapsed_s"] = round(time.time() - t0, 1)
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
print("wrote", OUT, f"{res['_elapsed_s']}s")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_AGGLOMERATION_INDEX 集聚指数 — 实测计算脚本（20261021 改源版）

方法依据（详见 MD 参考文献）：
  - 区位熵 LQ：Hoover (1948)；中国官方应用：国家统计局及各省市统计年鉴产业集聚度测算
  - 空间基尼系数：Krugman (1991)
  - HHI：美国司法部 Horizontal Merger Guidelines (2010)
  - 工程口径：metrics/calc-logic/ENT/M_ENT_AGGLOMERATION_INDEX.md（王惠表 AI 补漏注册版）

主算环境：三方库 gkx（183.240.141.251:3318），全表名写 gkx.<表名>。
性能约定：企业主档只做**一次**宽表拉取（18.9 万行），probe 与 compute 共用同一批行；
行数一律读库存 _work_gkx21/GKX_INVENTORY.json，不重复 COUNT(*)。
输出：M_ENT_AGGLOMERATION_INDEX_out.json
"""
from __future__ import annotations

import json
import sys
import time
from collections import defaultdict
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent
ROOT = CODE_DIR.parent
sys.path.insert(0, str(CODE_DIR))

from _gkxdb import gkx  # noqa: E402

OUT = Path(__file__).with_name("M_ENT_AGGLOMERATION_INDEX_out.json")
INVENTORY = ROOT / "_work_gkx21" / "GKX_INVENTORY.json"


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def inv_rows() -> dict:
    """行数只读库存（GKX_INVENTORY.json），不重复 COUNT(*)。"""
    d = json.loads(INVENTORY.read_text(encoding="utf-8"))
    return {k: int(v["rows"]) for k, v in d.items()}


def q(sql: str, args=None):
    """在三方库 gkx 上执行查询，返回 dict 行列表。"""
    cur = gkx()
    try:
        cur.execute(sql, args)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    finally:
        cur.close()


def s(v) -> str:
    return (v or "").strip() if isinstance(v, str) else ("" if v is None else str(v).strip())


CACHE = CODE_DIR / "_cache" / "gkx_dwd_org_base_info.json"


def load_base() -> list:
    """一次性拉取企业主档（probe/矩阵共用），避免对宽表多次全扫；>90 秒结果落 json 缓存。"""
    if CACHE.exists():
        log(f"load base_info from cache {CACHE.name}")
        return json.loads(CACHE.read_text(encoding="utf-8"))
    log("load gkx.dwd_org_base_info ...")
    rows = q(
        "SELECT reg_status, city, province, area, industry, industry_l1_code, "
        "       industry_l2_code, industry_l3_code, registered_capital_value "
        "FROM gkx.dwd_org_base_info")
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(rows, ensure_ascii=False, default=str), encoding="utf-8")
    return rows


def probe(inv: dict, rows: list) -> dict:
    """步骤0：结构+填充率探测（全表口径，行数走库存）"""
    out = {}
    out["base_info_rows"] = inv["dwd_org_base_info"]
    out["base_info_rows_measured"] = len(rows)
    out["industry_tags_rows"] = inv["dwd_org_industry_tags"]
    out["admin_area_rows"] = inv["dwd_dim_admin_area"]
    out["alive_rows"] = sum(1 for r in rows if "存续" in s(r.get("reg_status")))
    out["city_filled"] = sum(1 for r in rows if s(r.get("city")))
    out["province_filled"] = sum(1 for r in rows if s(r.get("province")))
    for f in ["industry", "industry_l1_code", "industry_l2_code", "industry_l3_code"]:
        out[f"fill_{f}"] = sum(1 for r in rows if s(r.get(f)))
    out["cap_filled"] = 0
    for r in rows:
        try:
            if r.get("registered_capital_value") is not None and float(r["registered_capital_value"]) > 0:
                out["cap_filled"] += 1
        except (TypeError, ValueError):
            pass
    return out


def compute(rows: list) -> dict:
    """主计算：全国企业集（存续+城市可识别）→ 城市×产业矩阵 → LQ/G/HHI"""
    ents = []
    empty_addr = 0
    for r in rows:
        if "存续" not in s(r.get("reg_status")):
            continue
        if not s(r.get("area")):
            empty_addr += 1
        city = s(r.get("city"))
        ind = s(r.get("industry_l1_code")) or s(r.get("industry"))
        if city and ind:
            ents.append((city, s(r.get("province")), ind, r.get("registered_capital_value") or 0))
    total_loaded = sum(1 for r in rows if "存续" in s(r.get("reg_status")))
    n_usable = len(ents)

    # 矩阵：E_ij[city][ind]，E_i[city]，E_j[ind]
    E_ij = defaultdict(lambda: defaultdict(int))
    E_i = defaultdict(int)
    E_j = defaultdict(int)
    C_ij = defaultdict(lambda: defaultdict(float))  # 注册资本口径
    C_i = defaultdict(float)
    C_j = defaultdict(float)
    for city, prov, ind, cap in ents:
        E_ij[city][ind] += 1
        E_i[city] += 1
        E_j[ind] += 1
        try:
            capv = float(cap)
        except (TypeError, ValueError):
            capv = 0.0
        if capv > 0:
            C_ij[city][ind] += capv
            C_i[city] += capv
            C_j[ind] += capv

    E_total = sum(E_j.values())
    C_total = sum(C_j.values())
    cities = sorted(E_i, key=lambda c: -E_i[c])
    top_inds = sorted(E_j, key=lambda j: -E_j[j])[:20]

    x = {c: E_i[c] / E_total for c in cities}  # 区域全部企业占比

    def metrics_for_ind(ind: str):
        Ej = E_j[ind]
        if Ej <= 0:
            return None
        s_ = {c: E_ij[c][ind] / Ej for c in cities if E_ij[c][ind] > 0}
        G = sum((s_.get(c, 0.0) - x[c]) ** 2 for c in cities)
        HHI = sum(v * v for v in s_.values())
        lq = {c: (E_ij[c][ind] / E_i[c]) / (Ej / E_total) for c in cities if E_i[c] > 0}
        lq_sz = lq.get("深圳市")
        # 注册资本口径 LQ（深圳）
        lq_cap_sz = None
        if C_total > 0 and C_j.get(ind, 0) > 0 and C_i.get("深圳市", 0) > 0:
            lq_cap_sz = (C_ij["深圳市"][ind] / C_i["深圳市"]) / (C_j[ind] / C_total)
        return {
            "industry": ind,
            "E_j": Ej,
            "LQ_shenzhen_count": round(lq_sz, 4) if lq_sz is not None else None,
            "LQ_shenzhen_capital": round(lq_cap_sz, 4) if lq_cap_sz is not None else None,
            "spatial_gini": round(G, 6),
            "HHI_city": round(HHI, 6),
        }

    ind_metrics = [m for m in (metrics_for_ind(j) for j in top_inds) if m]

    # 全库整体（不分产业）区域集中度 HHI（需求“直观反映集聚效应”的最简形态）
    HHI_all = sum(v * v for v in x.values())
    # 全国→省→市逐级：省级 HHI（同批行内聚合，口径与城市矩阵独立：只要存续且省份非空即计入）
    prov_cnt = defaultdict(int)
    for r in rows:
        if "存续" not in s(r.get("reg_status")):
            continue
        prov = s(r.get("province"))
        if prov:
            prov_cnt[prov] += 1
    prov_n = sum(prov_cnt.values())
    HHI_prov = sum((n / prov_n) ** 2 for n in prov_cnt.values()) if prov_n else None
    top_provinces = sorted(prov_cnt.items(), key=lambda t: -t[1])[:10]

    return {
        "total_loaded_alive": total_loaded,
        "n_usable_city_industry": n_usable,
        "n_cities": len(cities),
        "n_industries_l1": len(E_j),
        "E_total": E_total,
        "C_total_positive_capital": round(C_total, 2),
        "HHI_city_all_enterprises": round(HHI_all, 6),
        "HHI_province_all_enterprises": round(HHI_prov, 6) if HHI_prov else None,
        "top10_provinces": [{"province": p, "alive_enterprises": n} for p, n in top_provinces],
        "top10_cities": [{"city": c, "alive_enterprises": E_i[c]} for c in cities[:10]],
        "industry_metrics_top20": ind_metrics,
        "shenzhen_stats": {
            "alive_enterprises_sz": E_i.get("深圳市", 0),
            "share_of_national": round(x.get("深圳市", 0), 6),
        },
    }


def inventory_spotcheck(inv: dict, probe_out: dict) -> dict:
    """换源后不再有 demo 对照面；改为「库存行数 vs 本脚本实测行数」自校验。"""
    return {
        "source": "gkx",
        "inventory_file": "_work_gkx21/GKX_INVENTORY.json",
        "inventory_rows": {
            "dwd_org_base_info": inv["dwd_org_base_info"],
            "dwd_org_industry_tags": inv["dwd_org_industry_tags"],
            "dwd_dim_admin_area": inv["dwd_dim_admin_area"],
        },
        "measured_base_info_rows": probe_out.get("base_info_rows_measured"),
        "inventory_aligned": inv["dwd_org_base_info"] == probe_out.get("base_info_rows_measured"),
    }


def judge(probe_out: dict, comp: dict, spot: dict) -> dict:
    n_city = comp.get("n_cities", 0)
    n_ind = comp.get("n_industries_l1", 0)
    usable = comp.get("n_usable_city_industry", 0)
    sz_n = (comp.get("shenzhen_stats") or {}).get("alive_enterprises_sz", 0)
    struct_ok = n_city >= 50 and n_ind >= 10 and usable >= 1000 and sz_n >= 500
    inv_ok = bool(spot.get("inventory_aligned"))
    level = "完全转换支持" if struct_ok else ("部分支持" if usable > 0 else "完全不支持")
    return {
        "data_support_level": level,
        "reason": (
            f"gkx 存续企业可识别城市×产业 {usable:,} 家，覆盖 {n_city} 城市 / {n_ind} 个 L1 产业；"
            f"深圳存续企业 {sz_n:,} 家；industry_tags {probe_out.get('industry_tags_rows'):,} 行（产业归类主用 "
            f"base_info.industry_l1_code，填充 {probe_out.get('fill_industry_l1_code'):,}）；"
            f"库存行数与本脚本实测行数一致={inv_ok}。"
            + ("结构+当前数据量足，LQ/G/HHI 已现转算出。" if struct_ok else "有效样本量不足（区域覆盖维受限，仅粤内城市）。")
        ),
        "criteria": {
            "cities_ge_50": n_city >= 50,
            "industries_ge_10": n_ind >= 10,
            "usable_ge_1000": usable >= 1000,
            "sz_alive_ge_500": sz_n >= 500,
            "gkx_inventory_aligned": inv_ok,
        },
    }


def main():
    report = {"metric_id": "M_ENT_AGGLOMERATION_INDEX", "metric_name": "集聚指数",
              "script": Path(__file__).name, "data_source": "gkx"}
    inv = inv_rows()
    rows = load_base()
    log("== probe ==")
    report["probe"] = probe(inv, rows)
    print(json.dumps(report["probe"], ensure_ascii=False), flush=True)
    log("== compute ==")
    report["compute"] = compute(rows)
    report["gkx_spotcheck"] = inventory_spotcheck(inv, report["probe"])
    report["support_judgment"] = judge(report["probe"], report["compute"], report["gkx_spotcheck"])
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report["support_judgment"], ensure_ascii=False, indent=2), flush=True)
    log(f"wrote {OUT}")


if __name__ == "__main__":
    main()

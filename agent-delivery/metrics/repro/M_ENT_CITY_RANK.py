#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_CITY_RANK 多城市对标排名 —— gkx 口径复现（2026-10-22）

口径（王惠 20260816 底稿 / calc-logic ENT / M_ENT_CITY_RANK）：
  在预设对标城市集合中，以选定未来产业为筛选条件，从「企业规模（平均营业收入）40%
  + 企业密度（每百平方公里企业数）30% + 产业链完整度 30%」三维极值归一化加权，
  得到城市综合得分并降序排名。

本件只连 gkx（183.240.141.251:3318，只读 gkx_reader_zp）。三维逐一实测：
  * 规模维：营收原料在 gkx.dwd_org_annual_financial_info（90,926 行，营收>0 2,191 行），
    可算城市均值的企业只覆盖 4 个广东城市、且各市覆盖率 0.3%—0.8%；
  * 密度维：分母城市土地面积在 gkx 不存在（见 M_ENT_CITY_DENSITY 的探针），Δ 维不可算；
  * 完整度维：gkx.dwd_org_industry_tags 2,283,762 行 + 链目录 1,273 码，全国 k/K=940/954，
    深圳探针 712/954（74.63%）——三维中唯一可算的一维（同口径见
    code/M_ENT_CHAIN_COMPLETENESS_out.json）。
  * 评分类子维：全库 `%score%` / `%rank%` / `%evaluat%` / `%rating%` 表名扫描命中 0 张。

三维里一维可算、一维部分可算、一维恒缺，综合得分无法合成，故本件**不出名次**，
只出维度可得性矩阵与单维示意（规模维、市内相对值），并在 §四 写清补齐路径。

权重 40/30/30 来自王惠底稿，Q014 未甲方闭合——本件只登记不自造。

输出：code/M_ENT_CITY_RANK_out.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import pymysql

HERE = Path(__file__).resolve().parent
OUT = HERE / "M_ENT_CITY_RANK_out.json"
SNAP = HERE / "_snapshots21"
GEO = SNAP / "ent_base_geo_20261022.json"
CAP = SNAP / "ent_city_capital_20261022.json"
PANEL = SNAP / "ent_margin_panel_20261022.json"
SIB = HERE / "M_ENT_CHAIN_COMPLETENESS_out.json"

GKX = dict(
    host="183.240.141.251", port=3318, user="gkx_reader_zp",
    password="Zp_Use_Gkx_db@123456",
    connect_timeout=60, read_timeout=900, write_timeout=900, autocommit=True,
)
# 固定探测日：产物必须可重跑一致（时间戳进产物会让每次 --check 判「内容有变」）
PULLED = "2026-10-22"
MAIN4 = ["深圳市", "广州市", "东莞市", "惠州市"]
WEIGHTS = {"scale": 0.4, "density": 0.3, "completeness": 0.3}

SCORE_SCAN = (
    "SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA='gkx' "
    "AND (TABLE_NAME LIKE '%score%' OR TABLE_NAME LIKE '%rank%' "
    "OR TABLE_NAME LIKE '%evaluat%' OR TABLE_NAME LIKE '%rating%')"
)


def connect(retries: int = 5):
    last = None
    for i in range(retries):
        try:
            return pymysql.connect(**GKX)
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(3 * (2 ** i))
    raise last


def q(sql: str, args=None):
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute("SET NAMES utf8mb4")
        cur.execute("SET SESSION max_execution_time=600000")
        cur.execute(sql, args)
        return cur.fetchall()
    finally:
        conn.close()


def load_capital() -> dict:
    if CAP.exists():
        return json.loads(CAP.read_text(encoding="utf-8"))
    rows = q(
        "SELECT city, COUNT(*) n, SUM(registered_capital_value > 0) cap_pos, "
        "AVG(CASE WHEN registered_capital_value > 0 THEN registered_capital_value END) cap_avg "
        "FROM gkx.dwd_org_base_info WHERE city IS NOT NULL AND city <> '' GROUP BY city"
    )
    d = {"source": {"db": "gkx", "host": "183.240.141.251:3318",
                    "table": "gkx.dwd_org_base_info", "pulled_at": PULLED},
         "rows": [{"city": r[0], "n": int(r[1]), "cap_pos": int(r[2] or 0),
                   "cap_avg": round(float(r[3]), 2) if r[3] is not None else None}
                  for r in rows]}
    SNAP.mkdir(parents=True, exist_ok=True)
    CAP.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return d


def main() -> None:
    geo = json.loads(GEO.read_text(encoding="utf-8"))["groups"]
    total = sum(g["n"] for g in geo)
    city = {}
    for g in geo:
        city[g["city"]] = city.get(g["city"], 0) + g["n"]

    cap = {r["city"]: r for r in load_capital()["rows"]}
    panel = json.loads(PANEL.read_text(encoding="utf-8")) if PANEL.exists() else {"fin": []}
    rev_by_city, rev_orgs_city = {}, {}
    for r in panel.get("fin", []):
        c = r.get("city") or ""
        if not c:
            continue
        rev_by_city[c] = rev_by_city.get(c, 0.0) + float(r["rev"])
        rev_orgs_city.setdefault(c, set()).add(r["org_id"])

    score_tables = [r[0] for r in q(SCORE_SCAN)]
    sib = json.loads(SIB.read_text(encoding="utf-8")) if SIB.exists() else {}

    rows = []
    for c, n in sorted(city.items(), key=lambda x: -x[1]):
        k = cap.get(c, {})
        orgs = len(rev_orgs_city.get(c, ()))
        rows.append({
            "city": c,
            "orgs": n,
            "share": round(n / total * 100, 4),
            "cap_nonzero": k.get("cap_pos", 0),
            "cap_fill_pct": round(k.get("cap_pos", 0) / n * 100, 4) if n else None,
            "cap_avg_yuan": k.get("cap_avg"),
            "rev_orgs": orgs,
            "rev_fill_pct": round(orgs / n * 100, 4) if n else None,
            "rev_avg_yuan": round(rev_by_city[c] / orgs, 2) if orgs else None,
            "density_per_100km2": None,
            "completeness_pct": None,
        })

    main4 = [r for r in rows if r["city"] in MAIN4]
    small = [r for r in rows if r["orgs"] < 1000]

    # 单维示意：仅规模维（注册资本均值，按 4 城）——不是本件口径，仅证明原料可算
    demo = sorted([r for r in main4 if r["cap_avg_yuan"]], key=lambda r: -r["cap_avg_yuan"])
    for i, r in enumerate(demo, 1):
        r["scale_only_rank"] = i

    out = {
        "metric_id": "M_ENT_CITY_RANK",
        "metric_name": "多城市对标排名",
        "probe_date": "2026-10-22",
        "db": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）",
        "source": {"db": "gkx", "host": "183.240.141.251:3318",
                   "tables": ["gkx.dwd_org_base_info",
                              "gkx.dwd_org_annual_financial_info",
                              "gkx.dwd_org_industry_tags",
                              "gkx.dwd_industry_chain_info"],
                   "pulled_at": PULLED},
        "calc_logic_ref": "gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_CITY_RANK.md",
        "formula": ("score_c = 0.4*s_scale,c + 0.3*s_density,c + 0.3*s_complete,c（极值归一化后），"
                    "rank_c = RANK(score_c desc)；权重来自王惠底稿，Q014 未闭合"),
        "weights": WEIGHTS,
        "weights_status": "王惠 20260816 底稿值（40/30/30），Q014 未甲方闭合；本件不自造权重",
        "probes": {
            "base_rows": total,
            "n_city": len(city),
            "main4_orgs": sum(r["orgs"] for r in main4),
            "main4_share": round(sum(r["orgs"] for r in main4) / total * 100, 4),
            "cities_lt_1000_orgs": len(small),
            "score_tables_hit": len(score_tables),
            "score_tables": score_tables,
            "chain_tags_rows": (sib.get("compute", {}) or {}).get("tags_total"),
            "chain_catalog_rows": (sib.get("compute", {}) or {}).get("chain_catalog_rows"),
            "chain_leaves_K": (sib.get("compute", {}) or {}).get("leaves_K"),
            "chain_national_pct": ((sib.get("compute", {}) or {}).get("national") or {}).get("completeness"),
            "chain_sz_probe_pct": ((sib.get("compute", {}) or {}).get("shenzhen_join_probe") or {}).get("completeness"),
            "fin_rows": 90926,
            "fin_rev_pos": 2191,
        },
        "dimensions": [
            {"code": "D1", "name": "企业规模（平均营业收入）", "weight": 0.4,
             "status": "partial",
             "evidence": "营收>0 行 2,191 / 90,926（2.41%）；能出城市均值的企业只覆盖 4 个广东城市",
             "computable": True},
            {"code": "D2", "name": "企业密度（每百km²）", "weight": 0.3,
             "status": "absent",
             "evidence": "城市土地面积在 gkx 无数值载体（面积类数值列扫描 0 命中；"
                         "人口密度指标 a77361 仅 30 行 / 14 国 / 止于 2021）",
             "computable": False},
            {"code": "D3", "name": "产业链完整度", "weight": 0.3,
             "status": "partial",
             "evidence": "tags 2,283,762 行；全国 k/K=940/954（98.53%），深圳探针 712/954（74.63%）；"
                         "城市级需按城市×链矩阵重算",
             "computable": True},
            {"code": "D4", "name": "评分类子维（技术/商业评分）", "weight": 0.0,
             "status": "absent",
             "evidence": "score/rank/evaluat/rating 表名扫描 0 命中",
             "computable": False},
        ],
        "cities": rows,
        "main4": main4,
        "composite_rank": {
            "computed": False,
            "reason": "D2 恒缺、D4 恒缺，三维加权无法合成；合成值会由「有值的那一维」单独决定，"
                      "等于用完整度维冒充综合排名",
            "rows": 0,
        },
        "scale_only_demo": {
            "note": "仅规模维（注册资本均值）的市内示意，不是本件排名口径，不得对外称「城市排名」",
            "rows": demo,
        },
        "support_judgment": "部分支持",
        "judgment_reason": (
            "三维中 D1 部分可算（营收>0 2,191/90,926，城市均值只覆盖 4 个广东城市）、"
            "D3 可算（tags 228 万行、全国 98.53%、深圳 74.63%）、D2 恒缺（无城市面积载体）、"
            "D4 恒缺（0 张评分表）；权重 40/30/30 亦未甲方闭合（Q014）。"
            "综合得分无法在分母缺失下合成，名次不可交付，故判部分支持而非完全转换支持。"
        ),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面排名：按最新可得年数据合成；因名次未出，不涉及基期序列。",
        "proxy_deviation": {
            "proxy": "city 为登记住所所在市（非经营地）；规模维以「有营收披露的企业均值」代理全市企业均值",
            "coverage_pct": 0.65,
            "deviation_note": "营收披露企业 1,257 家 / 189,116（0.66%），且集中在广深莞惠；"
                              "以此均值代表全市企业规模，方向偏「上市与规上主体」，量级不可外推。"
                              "密度分母缺失，未使用任何代理（不用人口密度反解，理由见 §四）。",
        },
        "derived_from": "同口径完整度维取自 code/M_ENT_CHAIN_COMPLETENESS_out.json",
        "verdict_kind": "computed",
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"probes": out["probes"],
                      "main4": [{k: r[k] for k in ("city", "orgs", "cap_fill_pct",
                                                   "rev_fill_pct", "rev_avg_yuan")}
                                for r in main4]},
                     ensure_ascii=False, indent=1))
    print("support:", out["support_judgment"], "| wrote", OUT.name)


if __name__ == "__main__":
    main()

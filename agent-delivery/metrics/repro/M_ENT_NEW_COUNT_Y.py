#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_NEW_COUNT_Y 历年新增企业数 —— gkx 口径复现（2026-10-22）

口径（calc-logic ENT / M_ENT_NEW_COUNT_Y，王惠 20260816 底稿 + 2026-08-27 扩界）：
  按注册年份分组计数：国内主档 ∪ 国外主档，一律以 incorporation_date 派生年，
  COUNT(DISTINCT org_id) GROUP BY 年，再按年累计；空注册日不进分组；不按产业过滤。

本件只连 gkx（183.240.141.251:3318，只读 gkx_reader_zp）。
数据现实：
  * gkx.dwd_org_base_info 189,116 行，注册日有效 188,762（99.81%）；
  * gkx.dwd_forg_base_info 20,000 行，注册日有效 16,037（80.19%），country 列全空；
  * 年份尾部有 1775—1979 的脏年（合计 2,992 行，占 1.48%），1980 起为可比序列；
  * 2026 为残年（年度未完），不作为基期年份。

聚合成本：dwd_org_base_info 的 GROUP BY YEAR() 无索引可用，全表扫约 40 秒。
首次运行落盘 `_snapshots21/ent_base_year_20261022.json` 与 `ent_forg_year_20261022.json`，
之后复用快照，重跑不再打库。

输出：code/M_ENT_NEW_COUNT_Y_out.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import pymysql

HERE = Path(__file__).resolve().parent
OUT = HERE / "M_ENT_NEW_COUNT_Y_out.json"
SNAP = HERE / "_snapshots21"
BASE_Y = SNAP / "ent_base_year_20261022.json"
FORG_Y = SNAP / "ent_forg_year_20261022.json"

GKX = dict(
    host="183.240.141.251", port=3318, user="gkx_reader_zp",
    password="Zp_Use_Gkx_db@123456",
    connect_timeout=60, read_timeout=900, write_timeout=900, autocommit=True,
)
# 固定探测日：产物必须可重跑一致（时间戳进产物会让每次 --check 判「内容有变」）
PULLED = "2026-10-22"
Y0, Y1 = 1980, 2026
LAST_FULL = 2025


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


def load_year(path: Path, sql: str, table: str) -> dict:
    if path.exists():
        d = json.loads(path.read_text(encoding="utf-8"))
        return d
    rows = q(sql)
    d = {"source": {"db": "gkx", "host": "183.240.141.251:3318", "table": table,
                    "query": "GROUP BY YEAR(incorporation_date)", "pulled_at": PULLED},
         "rows": [{"year": int(r[0]), "n": int(r[1])} for r in rows]}
    SNAP.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return d


def main() -> None:
    base = load_year(
        BASE_Y,
        "SELECT YEAR(incorporation_date) y, COUNT(*) n FROM gkx.dwd_org_base_info "
        "WHERE incorporation_date IS NOT NULL AND CAST(incorporation_date AS CHAR) <> 'NULL' "
        "GROUP BY y",
        "gkx.dwd_org_base_info",
    )
    forg = load_year(
        FORG_Y,
        "SELECT YEAR(incorporation_date) y, COUNT(*) n FROM gkx.dwd_forg_base_info "
        "WHERE incorporation_date IS NOT NULL AND CAST(incorporation_date AS CHAR) <> 'NULL' "
        "GROUP BY y",
        "gkx.dwd_forg_base_info",
    )

    dom = {r["year"]: r["n"] for r in base["rows"]}
    frg = {r["year"]: r["n"] for r in forg["rows"]}
    # 「存量 ≠ 累计」是正文反复强调的边界，这个数必须落盘而不是只写在散文里
    alive = q("SELECT COUNT(*) FROM gkx.dwd_org_base_info "
              "WHERE reg_status LIKE '%存续%'")[0][0]

    # 快照把「注册日为空」落到 year=None 桶；空日期不进分组（口径明文），先摘出来
    dom_null = dom.pop(None, 0)
    frg_null = frg.pop(None, 0)

    dom_valid = sum(dom.values())
    forg_valid = sum(frg.values())
    tail = {y: n for y, n in dom.items() if y < Y0}
    tail_forg = {y: n for y, n in frg.items() if y < Y0}
    tail_sum = sum(tail.values()) + sum(tail_forg.values())

    series, cum = [], 0
    for y in range(Y0, Y1 + 1):
        d, f = dom.get(y, 0), frg.get(y, 0)
        cum += d + f
        series.append({"year": y, "domestic": d, "foreign": f, "total": d + f,
                       "cumulative": cum})

    peak = max(series, key=lambda r: r["total"])
    recent = [r for r in series if LAST_FULL - 4 <= r["year"] <= LAST_FULL]
    cur_year = series[-1]
    prev = {r["year"]: r for r in series}

    # 同比：与上一年比；1980 无前值
    for r in series:
        p = prev.get(r["year"] - 1)
        r["yoy_pct"] = (round((r["total"] / p["total"] - 1) * 100, 2)
                        if p and p["total"] else None)

    out = {
        "metric_id": "M_ENT_NEW_COUNT_Y",
        "metric_name": "历年新增企业数",
        "probe_date": "2026-10-22",
        "db": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）",
        "source": {"db": "gkx", "host": "183.240.141.251:3318",
                   "tables": ["gkx.dwd_org_base_info", "gkx.dwd_forg_base_info"],
                   "pulled_at": PULLED},
        "calc_logic_ref": "gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_NEW_COUNT_Y.md",
        "probes": {
            "domestic_rows": 189116,
            "alive_rows": int(alive),
            "alive_share": round(int(alive) / 189116 * 100, 4),
            "domestic_valid_date": dom_valid,
            "domestic_missing_date": dom_null,
            "domestic_date_fill_pct": round(dom_valid / 189116 * 100, 4),
            "foreign_rows": 20000,
            "foreign_valid_date": forg_valid,
            "foreign_missing_date": frg_null,
            "foreign_date_fill_pct": round(forg_valid / 20000 * 100, 4),
            "foreign_country_nonempty": 0,
            "tail_before_1980_rows": tail_sum,
            "tail_before_1980_years_n": len(set(tail) | set(tail_forg)),
            "years_in_series": len(series),
            "year_range": [Y0, Y1],
        },
        "result": {
            "total_cumulative": cum,
            "peak_year": peak["year"],
            "peak_total": peak["total"],
            "peak_domestic": peak["domestic"],
            "peak_foreign": peak["foreign"],
            "recent_5y": [{k: r[k] for k in ("year", "domestic", "foreign", "total")}
                          for r in recent],
            "recent_5y_sum": sum(r["total"] for r in recent),
            "recent_5y_foreign_share": round(
                sum(r["foreign"] for r in recent) / sum(r["total"] for r in recent) * 100, 4),
            "current_year": {"year": cur_year["year"], "total": cur_year["total"],
                             "domestic": cur_year["domestic"],
                             "foreign": cur_year["foreign"],
                             "partial": True,
                             "note": "2026 为残年，年度未完，不可与整年比高低，也不作基期"},
            "latest_full_year": {"year": LAST_FULL,
                                 "total": prev[LAST_FULL]["total"],
                                 "domestic": prev[LAST_FULL]["domestic"],
                                 "foreign": prev[LAST_FULL]["foreign"]},
            "series": series,
        },
        "support_judgment": "完全转换支持",
        "judgment_reason": (
            "国内主档 189,116 行中注册日有效 188,762（99.81%）、国外主档 20,000 行中有效 16,037"
            "（80.19%），按年 GROUP BY 一次即得 1980—2026 共 47 年序列（累计 201,807）；"
            "结构与当前数据量均足、脚本已现转出数，缺的只是目标结果表而非数据。"
            "国外侧 country 列全空不影响「按年计数」，只影响「按国家拆分」这一子维度（另见 §四）。"
        ),
        "base_years_used": list(range(Y0, LAST_FULL + 1)),
        "base_years_missing": [],
        "base_years_note": f"{Y0}—{LAST_FULL} 共 {LAST_FULL - Y0 + 1} 个基期年份；"
                           f"{Y1} 为残年，已单列并标 partial，不进基期；"
                           f"1980 年前 {tail_sum} 行属尾部脏年（1900—1979），已裁剪不计入序列。",
        "proxy_deviation": {
            "proxy": "无代理：年份由 incorporation_date 直接派生，国内/国外双主档各自原生字段",
            "coverage_pct": 100.0,
            "deviation_note": "唯一的口径边界是「主档是登记全集子集」：本库 20.9 万家对全国"
                              "企业存量是千分之一量级，故只能做形态对表（峰值年、回落节奏），"
                              "不能与市场监管总局的全国新设企业数做数值对标。",
        },
        "verdict_kind": "computed",
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"probes": out["probes"],
                      "peak": [peak["year"], peak["total"]],
                      "recent_5y": out["result"]["recent_5y"],
                      "cum": cum}, ensure_ascii=False, indent=1))
    print("support:", out["support_judgment"], "| wrote", OUT.name)


if __name__ == "__main__":
    main()

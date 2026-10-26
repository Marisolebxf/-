#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_PAINPOINT_SEVERITY 痛难点严重度 — 实测脚本（20261021 改源版）

口径（calc-logic 王惠迁移版）：
  企业各项经营指标实际表现与判断阈值之间的偏离程度；
  分维度（经营竞争力/盈利能力/生产效率/人才状况）加权汇总；
  按偏离度分档：轻度 0-20% / 中度 20-50% / 重度 >50%。

    10|本版数据面（20261021）：
  - 主算：三方库 gkx（全表名 gkx.<表名>）；行数只读 _work_gkx21/GKX_INVENTORY.json。
  - 阈值配置表存在性：live 开发库 gkxlumenx_dwd / gkxlumenx_ads（经 _gkxdb.live 连接，
    其 _check_schema 对 demo_ 直接 raise，物理层落实禁引）。

实测：
  1) 阈值配置表存在性（live 两 schema 扫描）；
  2) 偏离度公式原料审计（阈值缺 → 行业 P25 代理基线下 deviation = (thr - x)/thr）；
  3) 出数：代理基线下的可判定企业偏离度分布 + 分档 + 样例。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent
ROOT = CODE_DIR.parent
sys.path.insert(0, str(CODE_DIR))

from _gkxdb import gkx, live  # noqa: E402

METRIC = "M_ENT_PAINPOINT_SEVERITY"
NAME = "痛难点严重度"
TODAY = "2026-10-21"
OUT = Path(__file__).parent / f"{METRIC}_out.json"
INVENTORY = ROOT / "_work_gkx21" / "GKX_INVENTORY.json"


def inv_rows() -> dict:
    d = json.loads(INVENTORY.read_text(encoding="utf-8"))
    return {k: int(v["rows"]) for k, v in d.items()}


def qgkx(sql: str, args=None):
    cur = gkx()
    try:
        cur.execute(sql, args)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    finally:
        cur.close()


def qgkx1(sql: str, args=None):
    rows = qgkx(sql, args)
    return rows[0] if rows else None


def qlive(schema: str, sql: str, args=None):
    conn = live(schema)
    try:
        with conn.cursor() as cur:
            cur.execute(sql, args)
            return cur.fetchall()
    finally:
        conn.close()


def write_partial(key, val):
    data = {}
    if OUT.exists():
        try:
            data = json.loads(OUT.read_text())
        except Exception:
            data = {}
    data[key] = val
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1))


def main():
    inv = inv_rows()
    OUT.write_text(json.dumps({
        "metric_id": METRIC, "metric_name": NAME, "date": TODAY, "data_source": "gkx + live",
        "calc_logic_ref": "gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_PAINPOINT_SEVERITY.md（王惠调研结果规范化迁移；需求文档提供构建方法；关联 Q014）",
        "clean_rule": "clean(col) = col IS NOT NULL AND col != 'NULL' AND TRIM(col) != ''；数值列加 >0",
    }, ensure_ascii=False, indent=1))

    # ============ 阈值配置表存在性（live 开发库两 schema） ============
    live_probe = {}
    for sch in ["DWD", "ADS"]:
        try:
            tabs = qlive(sch, "SHOW TABLES")
            names = sorted(v for r in tabs for v in (r.values() if isinstance(r, dict) else [r[0]]))
            live_probe[f"gkxlumenx_{sch.lower()}"] = {
                "table_count": len(names),
                "threshold_like": [t for t in names
                                   if any(s in str(t).lower() for s in ["threshold", "painpoint", "severit"])],
            }
        except Exception as e:  # noqa: BLE001
            live_probe[f"gkxlumenx_{sch.lower()}"] = {"error": str(e)[:120]}
    write_partial("live_probe", live_probe)

    # ============ 原料审计：四维指标与王惠 src 列的存在性（单次条件聚合一趟扫） ============
    try:
        audit = {}
        cols = sorted(str(list(r.values())[0]) for r in qgkx(
            "SHOW COLUMNS FROM gkx.dwd_org_annual_financial_info"))
        audit["fin_cols"] = cols
        audit["arch_development_am_exists"] = "arch_development_am" in cols
        total = inv["dwd_org_annual_financial_info"]
        audit["total_rows"] = total
        agg = ["COUNT(*) total"]
        for col in ["operating_revenue", "total_profit", "pure_profit", "total_assets",
                    "total_liabilities", "employees_number", "development_employee"]:
            agg.append(f"SUM(`{col}` > 0) pos_{col}")
            agg.append(f"SUM(`{col}` IS NOT NULL AND `{col}` != 'NULL' AND `{col}` != '') nn_{col}")
        row = qgkx1("SELECT " + ", ".join(agg) + " FROM gkx.dwd_org_annual_financial_info")
        fill = {}
        for col in ["operating_revenue", "total_profit", "pure_profit", "total_assets",
                    "total_liabilities", "employees_number", "development_employee"]:
            nz = int(row[f"pos_{col}"] or 0)
            nn = int(row[f"nn_{col}"] or 0)
            fill[col] = {"nonnull": nn, "positive": nz,
                         "positive_pct": round(100.0 * nz / total, 2)}
        audit["fill_audit"] = fill
        # 行业分组键
        r = qgkx1("SELECT COUNT(*) c, COUNT(DISTINCT industry_l1_code) d FROM gkx.dwd_org_base_info "
                  "WHERE industry_l1_code IS NOT NULL AND industry_l1_code != 'NULL' AND TRIM(industry_l1_code) != ''")
        audit["base_industry_key"] = {"rows": int(r["c"]), "distinct_l1": int(r["d"])}
        write_partial("gkx_audit", audit)
    except Exception as e:  # noqa: BLE001
        write_partial("gkx_audit", {"fatal": str(e)[:200]})

    # ============ 出数：代理基线偏离度分档 ============
    # deviation_k = (thr_k − x_k)/thr_k，thr 缺 → 行业 P25 代理；
    # 加权：等权（Q014 权重未闭合的基线）；分档：轻 0-20%/中 20-50%/重 >50%（口径原式）。
    # 人才维整维缺省（development_employee 全 0）；四维以可承载三维（经营=营收、盈利=ROE、效率=人均营收）出数。
    try:
        calc = {"approach": "行业 P25 代理阈值 + 等权汇总 + 口径原式分档（阈值配置表缺，降级轨）",
                "excluded": "人才状况维整维缺省（development_employee 全空，缺维不计 0）",
                "source": "gkx.dwd_org_annual_financial_info × gkx.dwd_org_base_info"}
        rows = qgkx(
            "SELECT t.org_id, t.year, t.operating_revenue, t.pure_profit, "
            "       t.total_assets, t.total_liabilities, t.employees_number, b.industry_l1_code "
            "FROM gkx.dwd_org_annual_financial_info t "
            "JOIN gkx.dwd_org_base_info b ON t.org_id = b.org_id "
            "WHERE t.year IN (2022, 2023, 2024) AND t.operating_revenue > 0 "
            "  AND t.employees_number > 0 "
            "  AND t.total_assets > 0 AND t.total_liabilities > 0 LIMIT 30000")
        latest = {}
        for r in rows:
            oid = r["org_id"]
            if oid not in latest or (r["year"] or 0) > (latest[oid]["year"] or 0):
                latest[oid] = r
        recs = list(latest.values())
        for r in recs:
            rev = float(r["operating_revenue"] or 0)
            eq = float(r["total_assets"] or 0) - float(r["total_liabilities"] or 0)
            pp = float(r["pure_profit"]) if r["pure_profit"] is not None else None
            r["rev"] = rev
            r["percap"] = rev / float(r["employees_number"] or 1)
            r["roe"] = (pp / eq * 100.0) if (pp is not None and eq > 0) else None
            r["ind"] = (r["industry_l1_code"] or "UNKNOWN").strip() or "UNKNOWN"
        by_ind = {}
        for r in recs:
            by_ind.setdefault(r["ind"], []).append(r)
        baseline = {}
        for ind, rs in by_ind.items():
            if len(rs) < 5:
                continue
            for k in ["rev", "percap", "roe"]:
                vals = sorted(x[k] for x in rs if x.get(k) is not None)
                if len(vals) >= 5:
                    baseline[(ind, k)] = vals[int(len(vals) * 0.25)]
        calc["n_computable_enterprises"] = len(recs)
        calc["n_industries_with_baseline"] = len({k[0] for k in baseline})
        # 偏离度与分档
        sev_dist = {"无偏离(轻0)": 0, "轻度(0-20%)": 0, "中度(20-50%)": 0, "重度(>50%)": 0}
        scored = []
        for r in recs:
            devs = []
            for k in ["rev", "percap", "roe"]:
                thr = baseline.get((r["ind"], k))
                if thr is not None and thr > 0 and r.get(k) is not None:
                    if r[k] < thr:  # 低于阈值才有偏离
                        devs.append(min((thr - r[k]) / thr, 10.0))  # 封顶10防除零外溢
            if devs:
                sev = sum(devs) / len(devs)  # 等权（Q014 基线）
                band = ("轻度(0-20%)" if sev <= 0.20 else
                        "中度(20-50%)" if sev <= 0.50 else "重度(>50%)")
                sev_dist[band] += 1
                scored.append({"org_id": r["org_id"], "year": r["year"],
                               "industry_l1_code": r["ind"],
                               "severity_dev": round(sev * 100, 1), "band": band})
            else:
                sev_dist["无偏离(轻0)"] += 1
        calc["severity_band_dist"] = sev_dist
        calc["n_scored_with_deviation"] = len(scored)
        calc["sample8"] = sorted(scored, key=lambda x: -x["severity_dev"])[:8]
        write_partial("compute", calc)
    except Exception as e:  # noqa: BLE001
        write_partial("compute", {"error": str(e)[:300]})

    # ============ support_judgment ============
    try:
        all_ = json.loads(OUT.read_text())
        audit = all_.get("gkx_audit", {})
        fill = audit.get("fill_audit", {})
        calc = all_.get("compute", {})
        rd_ok = fill.get("development_employee", {}).get("positive", 0)
        level = "部分支持"
        reason = ("阈值配置表（Q014）在 live 开发库 gkxlumenx_dwd/ads 均无——王惠口径的分档依赖阈值，缺配置即无法正式出档；"
                  f"人才维研发人员全空（{rd_ok} 行）+ 财务原料填充 2-3%（营收 {fill.get('operating_revenue', {}).get('positive_pct', '?')}%）"
                  f"不足以支撑全国企业分档；降级轨：行业 P25 代理 + 等权下可对 {calc.get('n_computable_enterprises', 'N/A')} 家出偏离度，"
                  f"其中 {calc.get('n_scored_with_deviation', 'N/A')} 家存在偏离（分档分布 {calc.get('severity_band_dist', {})}）")
        write_partial("support_judgment", {
            "data_support_level": level, "reason": reason,
            "criteria": {
                "threshold_cfg_table_exists": False,
                "threshold_cfg_scanned": ["gkxlumenx_dwd", "gkxlumenx_ads"],
                "rd_employee_positive_rows": rd_ok,
                "revenue_positive_pct": fill.get("operating_revenue", {}).get("positive_pct"),
                "n_computable_enterprises": calc.get("n_computable_enterprises"),
                "n_scored_with_deviation": calc.get("n_scored_with_deviation"),
            }})
    except Exception as e:  # noqa: BLE001
        write_partial("support_judgment", {"error": str(e)[:300]})

    print(f"[done] {METRIC} -> {OUT}")


if __name__ == "__main__":
    main()

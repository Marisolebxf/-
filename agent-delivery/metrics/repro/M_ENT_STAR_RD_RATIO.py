#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_STAR_RD_RATIO · 明星企业研发投入占比（gkx 口径）

口径（calc-logic/ENT/M_ENT_STAR_RD_RATIO.md，Q-E34）：
    选定范围内，明星企业研发投入 / 营业收入 × 100%。
    SUM(研发投入) / SUM(营收)；每企取最新一期。
    源表：dwd_org_annual_financial_info（年报研发投入优先）、
         dwd_org_stock_finance_info（上市企业营收兜底）。

gkx 实测：
    年报口径 arch_development_am 整列为空（0/90,926），工商年报 yftrje 也整列为空（0/527,034），
    研发投入只剩「上市/发债主体财报」一条腿；明星名单用 code/_snapshots21 的
    star_roster_gkx_20261021.json（dwd_patent 申请人授权≥50 聚合，4,561 家）。

只连 gkx（183.240.141.251:3318，只读 gkx_reader_zp）+ 读本目录已验证快照。
产物：code/M_ENT_STAR_RD_RATIO_out.json
"""
from __future__ import annotations

import json
import statistics
import time
from collections import Counter
from decimal import Decimal
from pathlib import Path

import pymysql

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
ROSTER = SNAP / "star_roster_gkx_20261021.json"
OUT = HERE / "M_ENT_STAR_RD_RATIO_out.json"
METRIC_ID = "M_ENT_STAR_RD_RATIO"

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", connect_timeout=60,
           read_timeout=1800, write_timeout=1800, autocommit=True)

SQL_STOCK = (
    "SELECT org_id, name_cn, occur_period, research_development_amount, operating_revenue "
    "FROM (SELECT org_id, name_cn, occur_period, research_development_amount, operating_revenue, "
    "ROW_NUMBER() OVER (PARTITION BY org_id ORDER BY occur_period DESC) rn "
    "FROM gkx.dwd_org_stock_finance_info "
    "WHERE research_development_amount>0 AND operating_revenue>0) t WHERE rn=1"
)
SQL_INCOME = (
    "SELECT jgid, jgmc, hjnd, jzrq, yffy, yysr "
    "FROM (SELECT jgid, jgmc, hjnd, jzrq, yffy, yysr, "
    "ROW_NUMBER() OVER (PARTITION BY jgid ORDER BY jzrq DESC, hjnd DESC) rn "
    "FROM gkx.dwd_org_income_statement WHERE yffy>0 AND yysr>0) t WHERE rn=1"
)
SQL_ARCH_RD = (
    "SELECT COUNT(*) n, SUM(arch_development_am IS NOT NULL) nn, "
    "SUM(arch_development_am>0) pos FROM gkx.dwd_org_annual_financial_info"
)
SQL_REPORT_RD = (
    "SELECT COUNT(*) n, SUM(yftrje IS NOT NULL AND TRIM(yftrje)<>'') ok "
    "FROM gkx.dwd_org_annual_report_asset"
)
SQL_FOREIGN_RD = (
    "SELECT COUNT(*) n, SUM(rd_staff IS NOT NULL) staff_nn, "
    "SUM(research_development_amount IS NOT NULL) am_nn "
    "FROM gkx.dwd_foreign_org_annual_financial_info"
)


def j(v):
    if isinstance(v, (bytes, bytearray)):
        return v.decode("utf-8", "replace")
    if isinstance(v, Decimal):
        return float(v)
    if hasattr(v, "isoformat"):
        try:
            return v.isoformat()
        except TypeError:
            return str(v)
    return v


def connect():
    last = None
    for i in range(5):
        try:
            return pymysql.connect(**GKX)
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 ** i)
    raise RuntimeError(f"gkx 连不上（5 次重试）：{last}")


def q(cur, sql, ms=900000):
    cur.execute(f"SET SESSION max_execution_time={ms}")
    cur.execute(sql)
    return [list(map(j, r)) for r in cur.fetchall()]


def pct(xs, p):
    xs = sorted(xs)
    if not xs:
        return None
    k = (len(xs) - 1) * p
    f = int(k)
    c = min(f + 1, len(xs) - 1)
    return round(xs[f] + (xs[c] - xs[f]) * (k - f), 4)


def main() -> None:
    t0 = time.time()
    roster = json.loads(ROSTER.read_text(encoding="utf-8"))
    rows = roster["rows"]
    rids = {r["org_id"] for r in rows}
    rname = {r["org_id"]: r["name_cn"] for r in rows}
    rind = {r["org_id"]: r.get("industry_l1_name") for r in rows}

    conn = connect()
    cur = conn.cursor()
    stock_rows = q(cur, SQL_STOCK, 900000)
    income_rows = q(cur, SQL_INCOME, 900000)
    arch = q(cur, SQL_ARCH_RD, 300000)[0]
    rep = q(cur, SQL_REPORT_RD, 600000)[0]
    fore = q(cur, SQL_FOREIGN_RD, 300000)[0]
    conn.close()

    # org_id -> (rd, rev, period)
    stock = {r[0]: (float(r[3]), float(r[4]), str(r[2])) for r in stock_rows}
    income = {r[0]: (float(r[4]), float(r[5]), str(r[2])) for r in income_rows}

    def stat(ids, src):
        ok = [i for i in ids if src[i][1] > 0 and src[i][0] > 0 and src[i][0] / src[i][1] <= 1]
        vals = sorted(src[i][0] / src[i][1] for i in ok)
        rd_sum = sum(src[i][0] for i in ok)
        rev_sum = sum(src[i][1] for i in ok)
        return {
            "orgs_with_data": len(ids),
            "orgs_valid": len(ok),
            "median_pct": round(statistics.median(vals) * 100, 4) if vals else None,
            "p25_pct": round(pct(vals, 0.25) * 100, 4) if vals else None,
            "p75_pct": round(pct(vals, 0.75) * 100, 4) if vals else None,
            "aggregate_pct": round(rd_sum / rev_sum * 100, 4) if rev_sum else None,
            "rd_sum": round(rd_sum, 2),
            "rev_sum": round(rev_sum, 2),
        }

    star_income = [i for i in rids if i in income]
    star_stock = [i for i in rids if i in stock]
    all_income = list(income)
    all_stock = list(stock)

    valid = [i for i in star_income
             if income[i][1] > 0 and income[i][0] > 0 and income[i][0] / income[i][1] <= 1]
    excluded = [{"org_id": i, "name": rname.get(i), "rd": income[i][0], "rev": income[i][1],
                 "ratio_pct": round(income[i][0] / income[i][1] * 100, 4), "period": income[i][2]}
                for i in star_income
                if income[i][1] > 0 and income[i][0] > 0 and income[i][0] / income[i][1] > 1]
    # 稳定排序：DB 返回顺序不保证，同值并列时逐次重跑会换序，
    # 让 rebuild_metric 的语义比对误判「内容有变」。按比值降序 + org_id 兜底。
    excluded.sort(key=lambda r: (-r["ratio_pct"], r["org_id"]))

    buckets = Counter()
    for i in valid:
        r = income[i][0] / income[i][1]
        k = ("0-1%" if r < 0.01 else "1-3%" if r < 0.03 else "3-5%" if r < 0.05
             else "5-10%" if r < 0.10 else "10-20%" if r < 0.20 else "20%+")
        buckets[k] += 1

    top = sorted(valid, key=lambda i: -income[i][0])[:12]
    d25 = {i: v for i, v in income.items() if str(v[2]) == "2025"}
    star25 = [i for i in star_income if i in d25]

    def rate(a, b):
        return round(a / b * 100, 4) if b else None

    payload = {
        "metric_id": METRIC_ID,
        "metric_name": "明星企业研发投入占比",
        "support_judgment": "部分支持",
        "verdict_kind": "positive",
        "judgment_reason": (
            "研发投入只剩「上市/发债主体财报」一条腿：calc-logic 首选年报口径 "
            f"arch_development_am 在 {int(arch[0]):,} 行中非空 {int(arch[1] or 0)} 行，"
            f"工商年报 yftrje 在 {int(rep[0]):,} 行中非空 {int(rep[1] or 0)} 行，均整列为空；"
            f"可用的是 dwd_org_income_statement.yffy 与 dwd_org_stock_finance_info，"
            f"覆盖 4,561 家明星企业中的 {len(star_income)} 家（{rate(len(star_income), len(rids))}%）。"
            "有真数、可算比值，但八成以上明星企业（多为非上市）无研发投入披露，故判部分支持。"
        ),
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "sources": {
            "primary": "gkx @ 183.240.141.251:3318 (readonly gkx_reader_zp)",
            "star_roster": "code/_snapshots21/star_roster_gkx_20261021.json",
            "tables": ["gkx.dwd_org_income_statement", "gkx.dwd_org_stock_finance_info",
                       "gkx.dwd_org_annual_financial_info", "gkx.dwd_org_annual_report_asset",
                       "gkx.dwd_patent", "gkx.dwd_org_base_info"],
            "sql": [SQL_STOCK, SQL_INCOME, SQL_ARCH_RD, SQL_REPORT_RD, SQL_FOREIGN_RD],
            "calc_logic": "gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_STAR_RD_RATIO.md",
        },
        "compute": {
            "formula": "SUM(研发投入) / SUM(营业收入) × 100%",
            "star_roster": {
                "n_star": len(rids),
                "threshold_grant": roster.get("threshold_grant"),
                "n_candidates_ge50": roster.get("n_candidates_ge50"),
                "n_excluded_non_enterprise": roster.get("n_excluded_non_enterprise"),
                "grant_sum": sum(int(r.get("grant_cnt") or 0) for r in rows),
                "source": roster.get("source"),
                "industry_top": Counter(rind.values()).most_common(6),
                "city_top": Counter(r.get("city") for r in rows).most_common(6),
            },
            "coverage": {
                "with_income_statement": len(star_income),
                "with_stock_finance": len(star_stock),
                "with_either": len(set(star_income) | set(star_stock)),
                "coverage_rate_pct": rate(len(set(star_income) | set(star_stock)), len(rids)),
                "no_rd_data": len(rids) - len(set(star_income) | set(star_stock)),
            },
            "primary": stat(star_income, income),
            "annual_2025": {"orgs_with_data": len(star25), **{k: v for k, v in stat(star25, income).items() if k != "orgs_with_data"}},
            "benchmark_stock_only": stat(star_stock, stock),
            "benchmark_all_income": stat(all_income, income),
            "benchmark_all_stock": stat(all_stock, stock),
            "ratio_distribution": dict(buckets),
            "excluded_ratio_gt_100pct": {"n": len(excluded), "rows": excluded[:10]},
            "top_by_rd_amount": [
                {"name": rname.get(i), "industry": rind.get(i),
                 "rd": round(income[i][0], 2), "revenue": round(income[i][1], 2),
                 "ratio_pct": round(income[i][0] / income[i][1] * 100, 4),
                 "year": income[i][2]}
                for i in top
            ],
        },
        "probes": {
            "empty_columns": {
                "dwd_org_annual_financial_info.arch_development_am":
                    {"rows": int(arch[0]), "non_null": int(arch[1] or 0), "positive": int(arch[2] or 0)},
                "dwd_org_annual_report_asset.yftrje":
                    {"rows": int(rep[0]), "non_empty": int(rep[1] or 0)},
                "dwd_foreign_org_annual_financial_info":
                    {"rows": int(fore[0]), "rd_staff_non_null": int(fore[1] or 0),
                     "rd_amount_non_null": int(fore[2] or 0)},
            },
            "period_mix": dict(Counter(v[2] for v in income.values()).most_common(6)),
            "max_execution_time_ms": 900000,
            "retry_policy": "5 次指数退避",
        },
        "proxy_deviation": (
            "① 明星企业用「专利授权≥50 且剔除非企业主体」代理，名单来自 dwd_patent 申请人聚合，"
            "偏专利密集型（制造业 1,995 家），服务业明星会漏；"
            "② 每企取最新一期，最新期含季报（income_statement 2026 年 734 家、stock 202603 期 615 家），"
            "季报营收未年化，与年报口径不可直接比；年度敏感性见 annual_2025；"
            "③ 研发投入取利润表「研发费用」，不含资本化开发支出，较「研发投入合计」系统性偏低；"
            "④ 未上市公司无公开财报，占比读数只代表 590 家有财报的明星企业，不能外推到 4,561 家。"
        ),
        "base_years_used": ["2025"],
        "base_years_missing": [],
        "base_years_note": (
            "主口径是「每企最新一期」截面（期别分布见 probes.period_mix，最新期多为 2026Q1/2025 年报），"
            "不构成统一基期；为可比性另给 annual_2025 子集（120 家有效）。"
            "income_statement 的 hjnd 覆盖 38 个年度，但 2017 年前研发费用行基本缺失，故不做跨年序列。"
        ),
        "notes": [
            "比值>100% 的 7 家已剔除：多为季报营收与累计研发费用错位，或研发型生物医药早期营收极低。",
            "中位数与合计口径必须并列：前者回答「典型企业强度」，后者回答「整体投入比重」，两者被巨头拉开的差距很大。",
            "研发人员占比不在本件范围（见 M_ENT_RESEARCHER_COUNT，判完全不支持）。",
        ],
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    p = payload["compute"]["primary"]
    print(f"[{METRIC_ID}] 名单={len(rids)} 有数={len(star_income)} 有效={p['orgs_valid']} "
          f"中位={p['median_pct']}% 合计={p['aggregate_pct']}%")


if __name__ == "__main__":
    main()

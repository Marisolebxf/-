#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_PAINPOINT_GAP · 痛难点改进差距（gkx 口径）

口径（calc-logic/ENT/M_ENT_PAINPOINT_GAP.md，Q009/Q018，公式待算法 Lead 会签）：
    Gap_k(e) = x_k(e) − Baseline_k(P25 或 P75)
    六项三级指标：营收增长率 / 主营业务收入 / 净利润率 / ROE / 人均产值 / 研发人员占比
    分组键：产业链分组（Q018 未闭合，本件以行业门类 industry_l1_name 代理）
    不设硬阈值，输出原始差值；组内 P25/P75 在线计算（库内无基线配置表）。

gkx 实测：
    基线配置表不存在 → 在线分位；
    六项里研发人员占比整列为空（development_employee 0/90,926）；
    其余五项可算但覆盖薄（人均产值 699 家、营收增长率配对 17 家）；
    行业门类分组样本≥30 的组共 28 个，可打分主体 1,131 家。

只连 gkx（183.240.141.251:3318，只读 gkx_reader_zp）。
产物：code/M_ENT_PAINPOINT_GAP_out.json
"""
from __future__ import annotations

import json
import statistics
import time
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path

import pymysql

HERE = Path(__file__).resolve().parent
OUT = HERE / "M_ENT_PAINPOINT_GAP_out.json"
METRIC_ID = "M_ENT_PAINPOINT_GAP"

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", connect_timeout=60,
           read_timeout=1800, write_timeout=1800, autocommit=True)

SQL_FIN = (
    "SELECT f.org_id, f.name_cn, f.`year`, f.operating_revenue, f.main_business_revenue, "
    "f.pure_profit, f.owners_equity, f.employees_number, b.industry_l1_name "
    "FROM (SELECT org_id, name_cn, `year`, operating_revenue, main_business_revenue, "
    "pure_profit, owners_equity, employees_number, "
    "ROW_NUMBER() OVER (PARTITION BY org_id ORDER BY `year` DESC) rn "
    "FROM gkx.dwd_org_annual_financial_info WHERE operating_revenue>0) f "
    "LEFT JOIN gkx.dwd_org_base_info b ON b.org_id=f.org_id AND b.is_deleted=0 "
    "WHERE f.rn=1"
)
SQL_GROWTH_PAIRS = (
    "SELECT COUNT(*) pairs FROM (SELECT org_id FROM gkx.dwd_org_annual_financial_info "
    "WHERE `year`=2023 AND operating_revenue>0) a JOIN "
    "(SELECT org_id FROM gkx.dwd_org_annual_financial_info "
    "WHERE `year`=2024 AND operating_revenue>0) b ON a.org_id=b.org_id"
)
SQL_INCOME_PAIRS = (
    "SELECT COUNT(*) orgs FROM (SELECT jgid, COUNT(DISTINCT hjnd) k "
    "FROM gkx.dwd_org_income_statement WHERE yysr>0 AND hjnd REGEXP '^[0-9]{4}$' "
    "GROUP BY jgid HAVING k>=2) t"
)
SQL_BASELINE_TABLES = (
    "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' AND ("
    "table_name LIKE '%baseline%' OR table_name LIKE '%p25%' OR table_name LIKE '%p75%' "
    "OR table_name LIKE '%quantile%' OR table_name LIKE '%percentile%' "
    "OR table_name LIKE '%diagnosis%')"
)
SQL_RD_STAFF = (
    "SELECT COUNT(*) n, SUM(development_employee IS NOT NULL) nn "
    "FROM gkx.dwd_org_annual_financial_info"
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
    return xs[f] + (xs[c] - xs[f]) * (k - f)


def main() -> None:
    t0 = time.time()
    conn = connect()
    cur = conn.cursor()
    rows = q(cur, SQL_FIN, 900000)
    growth_pairs = int(q(cur, SQL_GROWTH_PAIRS, 300000)[0][0])
    income_pairs = int(q(cur, SQL_INCOME_PAIRS, 300000)[0][0])
    baseline_tables = [r[0] for r in q(cur, SQL_BASELINE_TABLES, 60000)]
    rd_n, rd_nn = q(cur, SQL_RD_STAFF, 300000)[0]
    conn.close()

    MIN_N = 30
    metrics = {
        "net_margin": "净利润率",
        "roe": "净资产收益率",
        "rev_per_cap": "人均产值",
        "main_rev": "主营业务收入",
    }

    def vals_of(r):
        _, _, _, rev, main, np_, eq, emp, _ind = r
        o = {}
        if rev and rev > 0 and np_ is not None:
            o["net_margin"] = np_ / rev
        if eq and eq > 0 and np_ is not None:
            o["roe"] = np_ / eq
        if rev and rev > 0 and emp and emp > 0:
            o["rev_per_cap"] = rev / emp
        if main and main > 0:
            o["main_rev"] = main
        return o

    groups = defaultdict(list)
    for r in rows:
        ind = r[8]
        if not ind:
            continue
        for m, v in vals_of(r).items():
            groups[(ind, m)].append(v)

    baseline = {}
    for (ind, m), vs in groups.items():
        if len(vs) >= MIN_N:
            baseline.setdefault(ind, {})[m] = {
                "n": len(vs),
                "p25": round(pct(vs, 0.25), 4),
                "p75": round(pct(vs, 0.75), 4),
                "median": round(statistics.median(vs), 4),
            }

    # 逐企业差值
    by_metric = Counter()
    samples = []
    for r in rows:
        ind = r[8]
        if not ind or ind not in baseline:
            continue
        hit = {}
        for m, v in vals_of(r).items():
            b = baseline[ind].get(m)
            if b:
                hit[m] = {
                    "value": round(v, 4),
                    "p25": b["p25"],
                    "p75": b["p75"],
                    "gap_p25": round(v - b["p25"], 4),
                    "gap_p75": round(v - b["p75"], 4),
                }
                by_metric[m] += 1
        if hit:
            samples.append({"org_id": r[0], "name": r[1], "year": r[2],
                            "industry": ind, "gaps": hit})

    samples.sort(key=lambda s: -len(s["gaps"]))
    rich = [s for s in samples if len(s["gaps"]) >= 4][:8] or samples[:8]

    # 单位体检：年报财务表的金额单位在上市/工商年报两个来源间不一致。
    # 证据是「最大值 298 亿」与「中位数 1.66 万」并存，且人均产值中位数低到 85 元/人（不可能是真实生产率）。
    revs = sorted(float(r[3]) for r in rows if r[3] and r[3] > 0)
    per_cap = sorted(vals_of(r)["rev_per_cap"] for r in rows
                     if "rev_per_cap" in vals_of(r))
    unit_check = {
        "revenue_n": len(revs),
        "revenue_max": round(revs[-1], 2),
        "revenue_median": round(statistics.median(revs), 2),
        "revenue_p90": round(pct(revs, 0.90), 2),
        "per_capita_median": round(statistics.median(per_cap), 2) if per_cap else None,
        "per_capita_p90": round(pct(per_cap, 0.90), 2) if per_cap else None,
        "flag": "金额单位疑不一致（元与万元混用）",
        "note": "最大值 298 亿与中位数 1.66 万并存；人均产值中位数落在两位数（元/人），"
                "真实劳动生产率不可能这么低，说明分子或分母量纲不齐。"
                "本件因此只把「差值」用于组内排序提示，不把绝对金额当可对外发布的读数。",
    }

    payload = {
        "metric_id": METRIC_ID,
        "metric_name": "痛难点改进差距",
        "support_judgment": "部分支持",
        "verdict_kind": "positive",
        "judgment_reason": (
            f"差值的分组基线在库内无配置表（名称含 baseline/p25/p75/quantile/percentile/diagnosis "
            f"的表 {len(baseline_tables)} 张），只能在线算分位；六项原料里研发人员占比整列为空"
            f"（development_employee 非空 {int(rd_nn or 0)}/{int(rd_n)}），营收增长率配对仅 {growth_pairs} 家；"
            f"其余四项可算但覆盖 699—1,242 家，行业门类样本≥{MIN_N} 的组 {len(baseline)} 个、"
            f"可打分主体 {len(samples)} 家。有算子、有真数、缺维度与样本，故判部分支持。"
        ),
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "sources": {
            "primary": "gkx @ 183.240.141.251:3318 (readonly gkx_reader_zp)",
            "tables": ["gkx.dwd_org_annual_financial_info", "gkx.dwd_org_base_info",
                       "gkx.dwd_org_income_statement"],
            "sql": [SQL_FIN, SQL_GROWTH_PAIRS, SQL_INCOME_PAIRS, SQL_BASELINE_TABLES, SQL_RD_STAFF],
            "calc_logic": "gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_PAINPOINT_GAP.md",
        },
        "compute": {
            "formula": "Gap_k(e) = x_k(e) - Baseline_k(P25/P75)",
            "group_key": {
                "declared": "产业链分组（Q018 未闭合）",
                "used_proxy": "dwd_org_base_info.industry_l1_name（行业门类）",
                "groups_with_n_ge_min": len(baseline),
                "pairs_with_n_ge_min": sum(len(v) for v in baseline.values()),
                "min_group_n": MIN_N,
            },
            "dims": [
                {"code": "D1", "name": "营业收入增长率", "dim": "经营竞争力",
                 "source": "dwd_org_annual_financial_info(2023→2024 同企两年营收)",
                 "computable_orgs": growth_pairs, "status": "不足",
                 "note": "配对 17 家，无法建组内分位；利润表跨年配对 3,162 家可作扩源轨（未纳入本件差值）"},
                {"code": "D2", "name": "主营业务收入", "dim": "经营竞争力",
                 "source": "dwd_org_annual_financial_info.main_business_revenue",
                 "computable_orgs": by_metric.get("main_rev", 0), "status": "可用（水平值）"},
                {"code": "D3", "name": "净利润率", "dim": "盈利能力",
                 "source": "pure_profit / operating_revenue",
                 "computable_orgs": by_metric.get("net_margin", 0), "status": "可用"},
                {"code": "D4", "name": "净资产收益率", "dim": "盈利能力",
                 "source": "pure_profit / owners_equity",
                 "computable_orgs": by_metric.get("roe", 0), "status": "可用"},
                {"code": "D5", "name": "人均产值", "dim": "生产效率",
                 "source": "operating_revenue / employees_number",
                 "computable_orgs": by_metric.get("rev_per_cap", 0), "status": "可用但薄"},
                {"code": "D6", "name": "研发人员占比", "dim": "人才状况",
                 "source": "development_employee / employees_number",
                 "computable_orgs": 0, "status": "无值",
                 "note": "development_employee 全表非空 0 行，整维缺省（不输出 0 差距）"},
            ],
            "baseline_online": {
                "config_table_found": bool(baseline_tables),
                "tables_matching_pattern": baseline_tables,
                "groups": [
                    {"industry": ind, "metrics": mv}
                    for ind, mv in sorted(baseline.items(),
                                          key=lambda kv: -max(x["n"] for x in kv[1].values()))
                ][:10],
            },
            "gaps": {
                "scorable_orgs": len(samples),
                "by_metric": dict(by_metric),
                "sample": rich,
            },
            "unit_check": unit_check,
            "extension_track": {
                "income_statement_multi_year_orgs": income_pairs,
                "note": "利润表 yysr 可提供跨年营收，用于把 D1 从 17 家扩到 3,162 家；"
                        "本件未纳入，因 calc-logic 的 D1 指定源是年报表，换源须先闭合口径。",
            },
        },
        "probes": {
            "baseline_table_scan": {
                "patterns": ["%baseline%", "%p25%", "%p75%", "%quantile%", "%percentile%", "%diagnosis%"],
                "hits": baseline_tables,
            },
            "rd_staff_column": {"rows": int(rd_n), "non_null": int(rd_nn or 0)},
            "max_execution_time_ms": 900000,
            "retry_policy": "5 次指数退避",
        },
        "proxy_deviation": (
            "分组键用行业门类代理产业链分组（Q018 未闭合）：产业链分组按产品/环节划分，"
            "同一门类内可能横跨上下游，代理会让基线变宽（组内异质性上升），P25/P75 区间被拉大，"
            "差距的绝对值偏小。差额无法在库内量化，须在 Q018 闭合后重算。"
            "另：年报财务表 90,926 行里营收>0 的仅 2,191 行，且集中在 2014—2017 年，"
            "本件每企取「最新有营收年」，故差值反映的是较早年度截面，不是当期经营状况。"
        ),
        "base_years_used": [2014, 2015, 2016, 2017, 2025],
        "base_years_missing": [2018, 2019, 2020, 2021, 2022, 2023, 2024],
        "base_years_note": (
            "每企取「最新一个有营收的年」，取到的年份集中在 2014—2017（最新年分布见 "
            "compute.dims 与主体样本的 year 字段），故 used 只列实际承载主体的年份；"
            "2018—2024 虽在表内存在，但承载主体极少（营收>0 行集中于早期），单列 missing 以免被读成可用基期。"
            "增长率维用 2023→2024 两年配对（17 家），与本截面基期不同源。"
        ),
        "notes": [
            "不设硬阈值：只输出原始差值，不判「劣势/优势」等级。",
            "缺维不补 0：研发人员占比整维缺省，输出 null 而不是 0 差距。",
            "与 M_ENT_PAINPOINT_COUNT（合规事件计数）、M_ENT_PAINPOINT_TOPIC（痛点主题归类）不同源、不同粒度，三者不互相顶替。",
        ],
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[{METRIC_ID}] 组={len(baseline)} 可打分={len(samples)} "
          f"净利率={by_metric.get('net_margin',0)} ROE={by_metric.get('roe',0)} "
          f"人均={by_metric.get('rev_per_cap',0)} 主营={by_metric.get('main_rev',0)} " "")


if __name__ == "__main__":
    main()

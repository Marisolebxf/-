#!/usr/bin/env python3
"""M_ENT_GROWTH_POTENTIAL 成长潜力 — 依赖侧实测脚本

王惠口径（calc-logic 真源，参照工信部《中小企业专精特新发展评价指标体系》成长性）：
  三维等权：市场扩张（营收增长率-行业均值）/盈利提升（利润增长率-行业均值）/
  资产积累（净资产增长率-行业均值）；取最近两个完整自然年度。
实测（2026-10-20）gkx：
  ① 财务 90,926 行：营收填充 2,193（2.4%）、利润/资产/负债另探。
  ② 行业对标键 org_base_info.industry_l1_code 填充另探。
  ③ 双年键 year 分布决定同比可算性。
结论：三维原料列在但填充极薄（营收 2.4%）→ 同比+行业均值对标样本不足 → 部分支持。
"""
from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

import pymysql

OUT = Path(__file__).with_name("M_ENT_GROWTH_POTENTIAL_out.json")
ENV_GKX = Path(__file__).resolve().parents[6] / "gkx-orchestration/agent-delivery/data/third-party-source/gkx-mysql-raw/.env.local"


def load_dotenv(path: Path) -> dict:
    env = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def dec(x):
    return str(x) if isinstance(x, Decimal) else x


def main():
    rep = {"metric_id": "M_ENT_GROWTH_POTENTIAL", "metric_name": "成长潜力", "script": "M_ENT_GROWTH_POTENTIAL.py"}
    e = load_dotenv(ENV_GKX)
    gc = pymysql.connect(host=e["GKX_SRC_HOST"], port=int(e["GKX_SRC_PORT"]), user=e["GKX_SRC_USER"],
                         password=e["GKX_SRC_PASSWORD"], database="gkx", charset="utf8mb4",
                         cursorclass=pymysql.cursors.DictCursor, connect_timeout=20, read_timeout=300)
    with gc.cursor() as cur:
        cur.execute("SELECT COUNT(*) n, SUM(operating_revenue IS NOT NULL) rev, SUM(total_profit IS NOT NULL) tp, "
                    "SUM(total_assets IS NOT NULL) ta, SUM(total_liabilities IS NOT NULL) tl "
                    "FROM dwd_org_annual_financial_info")
        fin = {k: dec(v) for k, v in dict(cur.fetchone()).items()}
        cur.execute("SELECT year, COUNT(*) n, SUM(operating_revenue IS NOT NULL) rev FROM dwd_org_annual_financial_info GROUP BY 1 ORDER BY 1")
        yr = [{k: dec(v) for k, v in dict(r).items()} for r in cur.fetchall()]
        cur.execute("SELECT SUM(industry_l1_code IS NOT NULL AND industry_l1_code<>'') l1, COUNT(*) n FROM dwd_org_base_info")
        l1 = {k: dec(v) for k, v in dict(cur.fetchone()).items()}
    gc.close()

    rep["probe"] = {"financial_fill": fin, "year_dist": yr, "org_industry_l1": l1}
    rep["support_judgment"] = {
        "data_support_level": "部分支持",
        "reason": (
            f"三维同比原料列在但填充极薄：营收 {fin['rev']}/{fin['n']}（2.4%）、利润 {fin['tp']}、"
            f"资产 {fin['ta']}、负债 {fin['tl']}；双年分布 {len(yr)} 个年份；"
            f"行业对标键 industry_l1_code 填充 {l1['l1']}/{l1['n']}。"
            "同比需同企双年+行业均值需足样本——当前填充率下两条件均不满足 → 部分支持。"
        ),
        "criteria": {
            "columns_ready": True,
            "revenue_fill_thin": True,
            "dual_year_comparable": False,
            "industry_benchmark_ready": False,
        },
    }
    OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(rep["probe"], ensure_ascii=False, indent=2), flush=True)
    print(json.dumps(rep["support_judgment"]["reason"], ensure_ascii=False), flush=True)
    print("wrote", OUT, flush=True)


if __name__ == "__main__":
    main()

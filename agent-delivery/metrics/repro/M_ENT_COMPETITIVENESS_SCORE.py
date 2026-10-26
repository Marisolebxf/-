#!/usr/bin/env python3
"""M_ENT_COMPETITIVENESS_SCORE 综合竞争力分 — 依赖侧实测脚本

王惠口径（calc-logic 真源，王惠调研规范化迁移）：
  四维（企业规模/财务状况/人力资源/市场表现）九三级指标，极值归一化 0-100，
  维内加权 → 一级权重（Q014 或熵值法）加权 → 综合竞争力得分。
实测（2026-10-20）gkx dwd_org_annual_financial_info 90,926 行填充率：
  资产总额>0 2,628（2.9%）；员工数>0 3,170（3.5%）；营收>0 2,191（2.4%）；
  利润非空 2,354；负债>0 2,408；研发人员 development_employee 全空（None）；
  财务三要素齐 2,102。年份 2021–2025 分布均衡（各约 7-8 千行）。
  本科及以上学历人数：现库无字段（待建）。
结论：九个三级指标中六个原料 2-4% 填充、一个全空、一个无字段——量级不足以支撑全国归一化 → 部分支持。
"""
from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

import pymysql

OUT = Path(__file__).with_name("M_ENT_COMPETITIVENESS_SCORE_out.json")
ENV_GKX = Path(__file__).resolve().parents[6] / "gkx-orchestration/agent-delivery/data/third-party-source/gkx-mysql-raw/.env.local"


def load_dotenv(path: Path) -> dict:
    env = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def main():
    rep = {"metric_id": "M_ENT_COMPETITIVENESS_SCORE", "metric_name": "综合竞争力分", "script": Path(__file__).name}
    e = load_dotenv(ENV_GKX)
    gc = pymysql.connect(host=e["GKX_SRC_HOST"], port=int(e["GKX_SRC_PORT"]), user=e["GKX_SRC_USER"],
                         password=e["GKX_SRC_PASSWORD"], database="gkx", charset="utf8mb4",
                         cursorclass=pymysql.cursors.DictCursor, connect_timeout=20, read_timeout=300)
    with gc.cursor() as cur:
        cur.execute("""SELECT COUNT(*) n,
            SUM(total_assets>0) assets, SUM(employees_number>0) emp,
            SUM(operating_revenue>0) rev, SUM(total_profit IS NOT NULL) profit,
            SUM(total_liabilities>0) liab, SUM(development_employee>0) rd_emp,
            SUM(operating_revenue>0 AND total_assets>0 AND total_liabilities>0) fin3
            FROM dwd_org_annual_financial_info""")
        fin = {k: (str(v) if isinstance(v, Decimal) else v) for k, v in dict(cur.fetchone()).items()}
        cur.execute("SELECT year, COUNT(*) n FROM dwd_org_annual_financial_info GROUP BY year ORDER BY year DESC LIMIT 5")
        years = [dict(r) for r in cur.fetchall()]
    gc.close()
    n = int(fin["n"])

    def pct(x):
        return round(int(x or 0) / n * 100, 1)

    probe = {
        "gkx_financial_fill": fin,
        "fill_pct": {k: f"{pct(v)}%" for k, v in fin.items() if k != "n"},
        "years": years,
        "bachelor_field_exists": False,
    }
    rep["probe"] = probe
    rep["support_judgment"] = {
        "data_support_level": "部分支持",
        "reason": (
            f"四维九三级指标原料：gkx 财务表 {n} 行中资产>0 {pct(fin['assets'])}%、员工>0 {pct(fin['emp'])}%、"
            f"营收>0 {pct(fin['rev'])}%、利润非空 {pct(fin['profit'])}%、负债>0 {pct(fin['liab'])}%、"
            f"财务三要素齐 fin3 {pct(fin['fin3'])}%；研发人员 development_employee 全空；本科及以上学历人数无字段（待建）；"
            "市场占有率需行业营收汇总（同样依赖低填充营收）。极值归一化对填充量敏感——2-4% 覆盖撑不起全国可比 min/max，"
            "人力资源维两指标一空一无 → 部分支持（表结构在、原料结构性薄，非无法构建）。"
        ),
        "criteria": {
            "financial_table_exists": True,
            "fill_rate_revenue_pct": pct(fin["rev"]),
            "rd_employee_any": fin["rd_emp"] not in (None, "0"),
            "bachelor_field_exists": False,
        },
    }
    OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(rep["support_judgment"], ensure_ascii=False, indent=2), flush=True)
    print("wrote", OUT, flush=True)


if __name__ == "__main__":
    main()

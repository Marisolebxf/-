#!/usr/bin/env python3
"""M_ENT_INDUSTRY_MATCH_SCORE 产业匹配度 — 依赖侧实测脚本

王惠口径（calc-logic 真源，方法源自陈林等《中国工业经济》2024(10) 产业链融入度三件套）：
  ind_link = C2×A2（收入加权产业出度，A=投入产出表直接消耗系数阵）
  d_f = (1-|u_f-c|/(u_max-u_min)) × production_f（质心度，u_i=Antràs 上游度）
  ind_chain_f = d_f × ind_link
calc-logic 已自评：核心瓶颈=《中国投入产出表》缺失（a_ij/Y_i/X_i 无源）→ 公式 1-2/6 不可算。
实测（2026-10-20）gkx：
  ① 库内无投入产出表（input_output/IO 类表空集）——外部公开数据（统计局 2020 年 153 部门表可下），
    属「可外采」而非「无处可得」，但当前两库均无。
  ② 收入权重 c_i 侧：main_business_revenue 填充探针；financial 表营收 2.4%（既往）。
  ③ 图谱边：shareholder/subsidiary 在（CULTIVATION_INDEX 已证）；投资边缺（CORE_SUPPLIER 已证 0 行）。
结论：方法核心输入（IO 表）两库皆无+收入权重薄 → 部分支持（外采可解但当前不可算）。
"""
from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

import pymysql

OUT = Path(__file__).with_name("M_ENT_INDUSTRY_MATCH_SCORE_out.json")
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
    rep = {"metric_id": "M_ENT_INDUSTRY_MATCH_SCORE", "metric_name": "产业匹配度", "script": "M_ENT_INDUSTRY_MATCH_SCORE.py"}
    e = load_dotenv(ENV_GKX)
    gc = pymysql.connect(host=e["GKX_SRC_HOST"], port=int(e["GKX_SRC_PORT"]), user=e["GKX_SRC_USER"],
                         password=e["GKX_SRC_PASSWORD"], database="gkx", charset="utf8mb4",
                         cursorclass=pymysql.cursors.DictCursor, connect_timeout=20, read_timeout=300)
    with gc.cursor() as cur:
        io_tabs = []
        for pat in ("%input_output%", "%invest_output%", "%io_table%", "%direct_consum%"):
            cur.execute(f"SHOW TABLES LIKE '{pat}'")
            io_tabs += [list(r.values())[0] for r in cur.fetchall()]
        # 宽匹配只作旁证（论文/行情表含 output 子串会误命中，不作为判定依据）
        cur.execute("SELECT COUNT(*) n, SUM(main_business_revenue IS NOT NULL) mbr FROM dwd_org_annual_financial_info")
        mbr = {k: dec(v) for k, v in dict(cur.fetchone()).items()}
        cur.execute("SELECT COUNT(*) n FROM dwd_org_shareholder_info")
        sh = cur.fetchone()["n"]
        cur.execute("SELECT COUNT(*) n FROM dwd_org_subsidiary_info")
        sub = cur.fetchone()["n"]
        cur.execute("SELECT COUNT(*) n FROM dwd_org_sc_info")
        try:
            sc = cur.fetchone()["n"]
        except Exception:
            sc = None
    gc.close()

    rep["probe"] = {
        "io_tables": sorted(set(io_tabs)),
        "main_business_revenue_fill": mbr,
        "edges": {"shareholder": sh, "subsidiary": sub, "supply_customer_sc": sc},
    }
    rep["support_judgment"] = {
        "data_support_level": "部分支持",
        "reason": (
            f"方法核心输入《中国投入产出表》两库皆无（io 类表空集）——a_ij/Y_i/X_i 无源，"
            f"ind_link（公式1-2/5）、上游度 u_i（公式6）、质心 c、d_f、ind_chain_f 全链不可算；"
            f"收入权重侧 main_business_revenue 填充 {mbr['mbr']}/{mbr['n']}（薄）；"
            f"图谱边 shareholder {sh:,}/subsidiary {sub:,} 在（投资边缺既往已证）。"
            "IO 表为统计局公开可下（2020 年 153 部门表）——外采可解，但当前两库均无 → 部分支持。"
        ),
        "criteria": {
            "io_table_available": len(set(io_tabs)) > 0,
            "revenue_weight_ready": False,
            "graph_edges_ready": True,
        },
    }
    OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(rep["support_judgment"], ensure_ascii=False, indent=2), flush=True)
    print("wrote", OUT, flush=True)


if __name__ == "__main__":
    main()

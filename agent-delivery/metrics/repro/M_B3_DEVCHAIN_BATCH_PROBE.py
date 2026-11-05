#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批3（8件）三源探针：
seq38 深圳企业规模分析 | seq39 选中产业历年企业数量趋势 | seq40 重点企业规模统计 | seq41 重点企业领域统计
seq42 关键驱动因素 | seq43 决策摘要·投资节奏 | seq44 决策摘要·政策窗口期 | seq45 潜在拐点
出参：repro/out/M_B3_DEVCHAIN_BATCH_PROBE_out.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx, live  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "out", "M_B3_DEVCHAIN_BATCH_PROBE_out.json")
out = {
    "metric_id": "M_B3_DEVCHAIN_BATCH_PROBE",
    "batch": "TOPIC-UI-GAP-L01 批3",
    "probe_date": "2026-11-04",
    "purpose": "批3（企业发展页续4件+产业周期分析4件）三源探针",
    "ui_evidence": [
        "live 30892 企业分析>企业发展>ShenzhenEnterprisesPanel（深圳企业规模分析 seq38）",
        "live 30892 企业分析>企业发展>DevelopmentOverviewPanel（选中产业历年企业数量趋势 seq39）",
        "live 30892 企业分析>企业发展>KeyEnterprisesPanel L437/L448（重点企业规模/领域统计 seq40/41）",
        "live 30892 产业链分析>产业周期分析>分析结果（关键驱动/投资节奏/政策窗口/潜在拐点 seq42-45）",
    ],
    "facts": {},
    "derived": {},
    "notes": [],
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "趋势/节奏件依赖年份面；周期件依赖时序驱动候选面。",
}


def num(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return 0


def main():
    # ---------- live：org_size 面（规模统计候选承载） ----------
    try:
        conn = live("DWD")
        with conn.cursor() as c:
            c.execute("SELECT org_size, COUNT(*) AS n FROM enterprise_base "
                      "WHERE org_size IS NOT NULL AND org_size <> '' GROUP BY org_size ORDER BY n DESC LIMIT 8")
            out["facts"]["live_org_size_dist"] = [{"k": str(r["org_size"])[:16], "n": num(r["n"])}
                                                   for r in c.fetchall()]
            c.execute("""SELECT is_high_tech, COUNT(*) AS n FROM enterprise_base
                         GROUP BY is_high_tech""")
            out["facts"]["live_high_tech_dist"] = {str(r["is_high_tech"]): num(r["n"]) for r in c.fetchall()}
        conn.close()
    except Exception as e:  # noqa: BLE001
        out["facts"]["live_org_size_dist"] = f"ERR:{type(e).__name__}: {e}"

    # ---------- gkx：规模列 / 重点企业规模领域 / 区域×年趋势 / 投融资节奏 / 政策面 ----------
    try:
        cur = gkx()
        cur.execute("""SELECT column_name FROM information_schema.columns
                       WHERE table_schema='gkx' AND table_name='dwd_org_base_info'
                       AND (column_name LIKE '%size%' OR column_name LIKE '%staff%'
                       OR column_name LIKE '%employee%' OR column_name LIKE '%scale%'
                       OR column_name LIKE '%capital%')""")
        out["facts"]["gkx_orgbase_size_cols"] = [r[0] for r in cur.fetchall()]
        # 重点企业（上市）规模/领域分布
        cur.execute("""SELECT SUBSTRING(CAST(registered_capital_value AS CHAR),1,2) AS cap_band, COUNT(*) AS n
                       FROM gkx.dwd_org_base_info
                       WHERE listing_status IS NOT NULL AND listing_status <> ''
                       AND registered_capital_value IS NOT NULL
                       GROUP BY cap_band ORDER BY n DESC LIMIT 8""")
        out["facts"]["listed_cap_band_top8"] = [{"band": r[0], "n": num(r[1])} for r in cur.fetchall()]
        cur.execute("""SELECT industry_l1_name, COUNT(*) AS n FROM gkx.dwd_org_base_info
                       WHERE listing_status IS NOT NULL AND listing_status <> ''
                       AND industry_l1_name IS NOT NULL AND industry_l1_name <> ''
                       GROUP BY industry_l1_name ORDER BY n DESC LIMIT 8""")
        out["facts"]["listed_l1_top8"] = [{"k": r[0], "n": num(r[1])} for r in cur.fetchall()]
        # 区域×年（seq39 区域参数化趋势原料）
        cur.execute("""SELECT city, incorporation_year, COUNT(*) AS n FROM gkx.dwd_org_base_info
                       WHERE incorporation_year BETWEEN 2018 AND 2024
                       AND city IN ('深圳市', '广州市', '东莞市', '惠州市', '北京市', '上海市')
                       GROUP BY city, incorporation_year ORDER BY city, incorporation_year""")
        rows = cur.fetchall()
        by_city = {}
        for r in rows:
            by_city.setdefault(r[0], []).append({"y": int(r[1]), "n": num(r[2])})
        out["facts"]["region_year_trend_2018_2024"] = by_city
        # 投融资节奏（seq43 候选承载：融资事件按 completion_date 逐年）
        cur.execute("""SELECT SUBSTRING(CAST(completion_date AS CHAR),1,4) AS y, COUNT(*) AS n
                       FROM gkx.dwd_org_financing_info
                       WHERE completion_date IS NOT NULL AND year(completion_date) > 2000
                       GROUP BY y ORDER BY y""")
        out["facts"]["financing_yearly"] = [{"y": int(r[0]), "n": num(r[1])} for r in cur.fetchall()]
        cur.execute("SHOW COLUMNS FROM gkx.dwd_org_financing_info")
        fin_cols = [r[0] for r in cur.fetchall()]
        out["facts"]["financing_cols"] = fin_cols[:20]
        # 政策面（seq44 候选承载：政策表族）
        cur.execute("""SELECT table_name FROM information_schema.tables
                       WHERE table_schema='gkx' AND (table_name LIKE '%%policy%%'
                       OR table_name LIKE '%%news%%') ORDER BY table_name""")
        pol_tabs = [r[0] for r in cur.fetchall()]
        out["facts"]["policy_news_tables"] = {}
        for t in pol_tabs[:14]:
            cur.execute(f"SELECT COUNT(*) FROM gkx.{t}")
            out["facts"]["policy_news_tables"][t] = num(cur.fetchone()[0])
        # 政策主表列名（时序/层级候选）
        cur.execute("SHOW COLUMNS FROM gkx.dwd_policy_base")
        out["facts"]["policy_base_cols"] = [r[0] for r in cur.fetchall()][:20]
        try:
            cur.execute("""SELECT SUBSTRING(CAST publish_date AS CHAR,1,4) FROM gkx.dwd_policy_base LIMIT 1""")
        except Exception:  # noqa: BLE001
            pass
        # 周期驱动候选（seq42/45：专利按申请年时序）
        cur.execute("""SELECT apdt_year, COUNT(*) AS n FROM gkx.dwd_patent
                       WHERE apdt_year IS NOT NULL AND apdt_year > 2000
                       GROUP BY apdt_year ORDER BY apdt_year""")
        out["facts"]["patent_yearly"] = [{"y": int(r[0]), "n": num(r[1])} for r in cur.fetchall()]
        # 政策逐年（seq44 时序候选）
        pb_date = next((c for c in out["facts"]["policy_base_cols"] if "date" in c or "year" in c), None)
        out["facts"]["policy_date_col"] = pb_date
        if pb_date:
            cur.execute(f"""SELECT SUBSTRING(CAST({pb_date} AS CHAR),1,4) AS y, COUNT(*) AS n
                            FROM gkx.dwd_policy_base
                            WHERE {pb_date} IS NOT NULL
                            GROUP BY y ORDER BY y""")
            out["facts"]["policy_yearly"] = [{"y": str(r[0]), "n": num(r[1])} for r in cur.fetchall()]
        cur.close()
    except Exception as e:  # noqa: BLE001
        out["notes"].append(f"gkx 探针异常（{type(e).__name__}: {e}）。")

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("saved", OUT_PATH)
    print("size_cols =", out["facts"].get("gkx_orgbase_size_cols"),
          "| policy_tables =", list(out["facts"].get("policy_tables", {}).items())[:4])


if __name__ == "__main__":
    main()

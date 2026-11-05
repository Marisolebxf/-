#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批2·组2（7件）三源探针：
seq24/25 数据覆盖与可信度(商业力/竞争力) | seq26 数据与权限预检 | seq34 产业链重点企业工作台
seq35 产业集群企业数量排名 | seq36 企业分布情况 | seq37 所选产业历年深圳企业数量趋势
出参：repro/out/M_ENT_UI_DEVCLUSTER_BATCH_PROBE_out.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx, live, gkx_count, live_count  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "out", "M_ENT_UI_DEVCLUSTER_BATCH_PROBE_out.json")
out = {
    "metric_id": "M_ENT_UI_DEVCLUSTER_BATCH_PROBE",
    "batch": "TOPIC-UI-GAP-L01",
    "probe_date": "2026-11-04",
    "purpose": "批2·组2（发展概览簇+评估面板依赖件）三源探针",
    "ui_evidence": [
        "live 30892 企业分析>企业发展>DevelopmentOverviewPanel（产业集群企业数量排名/企业分布情况）",
        "live 30892 企业分析>企业发展>ShenzhenEnterprisesPanel（所选产业历年深圳企业数量趋势）",
        "live 30892 企业分析>企业发展>KeyEnterprisesPanel（产业链重点企业工作台）",
        "live 30892 企业分析>企业商业力评估对比分析/企业竞争力分析>数据覆盖与可信度（评估面板）",
        "live 30892 企业分析>企业供应链关系分析>数据与权限预检",
    ],
    "facts": {},
    "derived": {},
    "notes": [],
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "截面件为主；趋势件依赖 enterprise_base 注册年份面。",
}


def num(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return 0


def main():
    import pymysql

    # ---------- live：企业底册（分布/趋势/排名基座） ----------
    try:
        conn = live("DWD")
        with conn.cursor() as c:
            c.execute("SELECT COUNT(*) AS n FROM enterprise_base")
            out["facts"]["live_eb_rows"] = num(c.fetchone()["n"])
            c.execute("SHOW COLUMNS FROM enterprise_base")
            cols = [r["Field"] for r in c.fetchall()]
            out["facts"]["live_eb_region_like_cols"] = [x for x in cols if any(
                k in x for k in ("region", "district", "addr", "industry", "chain", "reg_", "est"))][:24]
            c.execute("""SELECT industry_category, COUNT(*) AS n FROM enterprise_base
                         WHERE industry_category IS NOT NULL AND industry_category <> ''
                         GROUP BY industry_category ORDER BY n DESC LIMIT 8""")
            out["facts"]["live_industry_dist_top8"] = [{"k": r["industry_category"], "n": num(r["n"])}
                                                       for r in c.fetchall()]
            c.execute("""SELECT SUBSTRING(CAST(registration_date AS CHAR),1,4) AS y, COUNT(*) AS n
                         FROM enterprise_base
                         WHERE registration_date IS NOT NULL AND year(registration_date) > 1900
                         GROUP BY y ORDER BY y""")
            rows = c.fetchall()
            out["facts"]["live_reg_year_span"] = [rows[0]["y"], rows[-1]["y"]] if rows else []
            out["facts"]["live_reg_year_buckets"] = len(rows)
            c.execute("""SELECT COUNT(DISTINCT industry_category) AS n FROM enterprise_base
                         WHERE industry_category IS NOT NULL AND industry_category <> ''""")
            out["facts"]["live_industry_distinct"] = num(c.fetchone()["n"])
        conn.close()
        out["notes"].append("live 企业底册可达：分布/趋势/排名候选基座成立。")
    except Exception as e:  # noqa: BLE001
        out["facts"]["live_eb_rows"] = None
        out["notes"].append(f"live 连接失败（{type(e).__name__}: {e}）；分布/趋势/排名候选基座降级由 gkx 承载。")

    # ---------- gkx：产业链树 / 集群 / 企业底册 / 映射 / 供应链面 ----------
    try:
        cur = gkx()

        def cnt(t):
            cur.execute("SELECT COUNT(*) FROM gkx." + t)
            return num(cur.fetchone()[0])

        cur.execute("""SELECT table_name FROM information_schema.tables
                       WHERE table_schema='gkx' AND (table_name LIKE '%%chain%%'
                       OR table_name LIKE '%%node%%') ORDER BY table_name""")
        out["facts"]["gkx_chain_node_tables"] = {t: cnt(t) for t in [r[0] for r in cur.fetchall()][:24]}
        cur.execute("""SELECT table_name FROM information_schema.tables
                       WHERE table_schema='gkx' AND table_name LIKE '%%cluster%%' ORDER BY table_name""")
        out["facts"]["gkx_cluster_tables"] = {t: cnt(t) for t in [r[0] for r in cur.fetchall()][:12]}
        cur.execute("""SELECT table_name FROM information_schema.tables
                       WHERE table_schema='gkx' AND (table_name LIKE '%%org_base%%'
                       OR table_name LIKE '%%company%%') ORDER BY table_name""")
        out["facts"]["gkx_org_base_rows"] = {t: cnt(t) for t in [r[0] for r in cur.fetchall()][:14]}
        cur.execute("""SELECT table_name FROM information_schema.tables
                       WHERE table_schema='gkx' AND table_name LIKE '%%industry%%map%%'""")
        out["facts"]["gkx_industry_map_rows"] = {t: cnt(t) for t in [r[0] for r in cur.fetchall()][:12]}
        cur.execute("""SELECT table_name FROM information_schema.tables
                       WHERE table_schema='gkx' AND (table_name LIKE '%%supply%%'
                       OR table_name LIKE '%%relation%%' OR table_name LIKE '%%graph%%') ORDER BY table_name""")
        out["facts"]["gkx_supply_graph_tables"] = {t: cnt(t) for t in [r[0] for r in cur.fetchall()][:24]}
        # 产业链 12 链口径抽验（INB12xx-25xx）
        cur.execute("""SELECT COUNT(*) FROM information_schema.tables
                       WHERE table_schema='gkx' AND table_name LIKE 'dwd_chain_node_%'""")
        out["facts"]["gkx_chain_node_table_count"] = num(cur.fetchone()[0])
        cur.close()
        out["notes"].append("gkx 产业链树/集群/企业底册/映射/供应链面探针完成。")
    except Exception as e:  # noqa: BLE001
        out["notes"].append(f"gkx 连接失败（{type(e).__name__}: {e}）。")

    # ---------- 久新：生态/图谱/企业/链类承载（单连接、限次查询防连接上限） ----------
    jx = None
    try:
        jx = pymysql.connect(host="47.93.119.170", port=29030, user="test2",
                             password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
                             database="gkx_technology_analysis_dev", connect_timeout=20, read_timeout=120,
                             autocommit=True)
        jc = jx.cursor()
        jc.execute("SET NAMES utf8mb4")
        jc.execute("SHOW TABLES")
        jt = [r[0] for r in jc.fetchall()]
        out["facts"]["jiuxin_table_total"] = len(jt)
        eco = [t for t in jt if any(k in t for k in ("eco", "graph", "chain", "enterprise"))]
        out["facts"]["jiuxin_eco_like_tables"] = eco[:20]
        for t in eco[:6]:
            jc.execute(f"SELECT COUNT(*) FROM {t}")
            out["facts"].setdefault("jiuxin_eco_rows", {})[t] = num(jc.fetchone()[0])
        out["notes"].append("久新生态/图谱/链/企业类承载探针完成（单连接）。")
    except Exception as e:  # noqa: BLE001
        out["facts"]["jiuxin_error"] = f"ERR:{type(e).__name__}: {e}"
        out["notes"].append("久新连接失败；按批1探针结论（242 张 ads_* 无生态图谱类）留证。")
    finally:
        if jx:
            jx.close()

    # ---------- 补充：live 集群映射 / gkx 企业底册日期区域列 / 链树结构 ----------
    try:
        conn = live("DIM")
        with conn.cursor() as c:
            c.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='gkxlumenx_dim'")
            dimtabs = [list(r.values())[0] for r in c.fetchall()]
            out["facts"]["live_dim_all_tables"] = dimtabs[:24]
            c.execute("SELECT COUNT(*) AS n FROM information_schema.tables WHERE table_schema='gkxlumenx_dim'")
            out["facts"]["live_dim_table_total"] = num(c.fetchone()["n"])
        conn.close()
    except Exception as e:  # noqa: BLE001
        out["facts"]["live_dim_error"] = f"ERR:{type(e).__name__}: {e}"
    try:
        cur = gkx()
        cur.execute("""SELECT column_name FROM information_schema.columns
                       WHERE table_schema='gkx' AND table_name='dwd_org_base_info'""")
        ob_cols = [r[0] for r in cur.fetchall()]
        out["facts"]["gkx_orgbase_cols_sample"] = [x for x in ob_cols if any(
            k in x for k in ("date", "year", "region", "district", "city", "industry", "status", "capital"))][:24]
        dtcol = next((x for x in ob_cols if x in ("incorporation_date", "reg_date", "register_date",
                                                  "est_date", "establish_date")), None)
        out["facts"]["gkx_orgbase_date_col"] = dtcol
        out["facts"]["gkx_orgbase_has_year_col"] = "incorporation_year" in ob_cols
        # 企业分布（深圳/城市维）与历年趋势实测
        cur.execute("""SELECT city, COUNT(*) AS n FROM gkx.dwd_org_base_info
                       WHERE city IS NOT NULL AND city <> ''
                       GROUP BY city ORDER BY n DESC LIMIT 6""")
        out["facts"]["gkx_orgbase_city_top6"] = [{"city": r[0], "n": num(r[1])} for r in cur.fetchall()]
        cur.execute("""SELECT COUNT(*) AS n FROM gkx.dwd_org_base_info
                       WHERE city LIKE %s""", ("%深圳%",))
        out["facts"]["gkx_orgbase_sz_rows"] = num(cur.fetchone()[0])
        cur.execute("""SELECT incorporation_year, COUNT(*) AS n FROM gkx.dwd_org_base_info
                       WHERE incorporation_year BETWEEN 2015 AND 2024
                       GROUP BY incorporation_year ORDER BY incorporation_year""")
        out["facts"]["gkx_orgbase_trend_2015_2024"] = [{"y": int(r[0]), "n": num(r[1])} for r in cur.fetchall()]
        cur.execute("""SELECT industry_category, COUNT(*) AS n FROM gkx.dwd_org_base_info
                       WHERE industry_category IS NOT NULL AND industry_category <> ''
                       GROUP BY industry_category ORDER BY n DESC LIMIT 6""")
        out["facts"]["gkx_orgbase_industry_top6"] = [{"k": r[0], "n": num(r[1])} for r in cur.fetchall()]
        if dtcol:
            cur.execute(f"""SELECT SUBSTRING(CAST({dtcol} AS CHAR),1,4) AS y, COUNT(*) AS n
                            FROM gkx.dwd_org_base_info
                            WHERE {dtcol} IS NOT NULL AND year({dtcol}) > 1900
                            GROUP BY y ORDER BY y""")
            rows = cur.fetchall()
            out["facts"]["gkx_orgbase_year_span"] = [rows[0][0], rows[-1][0]] if rows else []
            out["facts"]["gkx_orgbase_year_buckets"] = len(rows)
        cur.execute("SHOW COLUMNS FROM gkx.dwd_industry_chain_info")
        chain_cols = [r[0] for r in cur.fetchall()]
        out["facts"]["gkx_chain_info_cols"] = chain_cols[:20]
        if "industry_code" in chain_cols:
            cur.execute("""SELECT COUNT(DISTINCT industry_code) AS n FROM gkx.dwd_industry_chain_info""")
            out["facts"]["gkx_chain_info_distinct_chains"] = num(cur.fetchone()[0])
            cur.execute("""SELECT level, COUNT(*) AS n FROM gkx.dwd_industry_chain_info
                           GROUP BY level ORDER BY level""")
            out["facts"]["gkx_chain_info_level_dist"] = [{"level": r[0], "n": num(r[1])} for r in cur.fetchall()]
            cur.execute("""SELECT COUNT(*) AS n FROM gkx.dwd_industry_chain_info
                           WHERE node_company_count > 0""")
            out["facts"]["gkx_chain_info_nodes_with_companies"] = num(cur.fetchone()[0])
        cur.close()
    except Exception as e:  # noqa: BLE001
        out["facts"]["gkx_supp_error"] = f"ERR:{type(e).__name__}: {e}"

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("saved", OUT_PATH)
    print("live_eb_rows =", out["facts"].get("live_eb_rows"),
          "| gkx chain/node tables =", len(out["facts"].get("gkx_chain_node_tables", {})),
          "| cluster tables =", len(out["facts"].get("gkx_cluster_tables", {})))


if __name__ == "__main__":
    main()

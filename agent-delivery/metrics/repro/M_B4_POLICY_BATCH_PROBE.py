#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批4（政策分析块 21 件）三源探针：
seq54 外商投资目录 | seq55 权威渠道 | seq56 对比区域 | seq57 评价维度
seq58-60/62-63/70-73 政策新闻可视化（全国/省/市 发布密度+数量连续性+链节点覆盖）
seq61/74 政策新闻内容管理（力度评估/统计与区域） | seq64-69 政策扶持（产业覆盖/力度排名/自动关联/数量对比/时序模型/标准化对比）
出参：repro/out/M_B4_POLICY_BATCH_PROBE_out.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx, live  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "out", "M_B4_POLICY_BATCH_PROBE_out.json")
out = {
    "metric_id": "M_B4_POLICY_BATCH_PROBE",
    "batch": "TOPIC-UI-GAP-L01 批4",
    "probe_date": "2026-11-05",
    "purpose": "批4（政策分析块 21 件）三源探针",
    "ui_evidence": [
        "live 30892 政策分析>政策查询/时序分析/区域对比/政策新闻可视化/政策扶持（seq54-74）",
        "页面证据 views/policy/policyNewsDisplayModel.ts、policyPortalTabs.ts、PolicyPortalStatsPanel.vue、PolicyNewsCmsPage.vue",
    ],
    "facts": {},
    "derived": {},
    "notes": [],
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "政策时序件依赖 publish_date 面（2022 后断更如实披露）。",
}


def num(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return 0


def main():
    cur = gkx()
    # 政策主表全列（层级/区域/产业/渠道/力度候选列）
    cur.execute("SHOW COLUMNS FROM gkx.dwd_policy_base")
    pcols = [r[0] for r in cur.fetchall()]
    out["facts"]["policy_base_cols_full"] = pcols
    # 政策层级分布（省/市/区 渠道候选列值域）
    for cand in ("policy_level", "level", "publish_org_level", "org_level", "region_level"):
        if cand in pcols:
            cur.execute(f"""SELECT {cand}, COUNT(*) AS n FROM gkx.dwd_policy_base
                            WHERE {cand} IS NOT NULL AND {cand} <> ''
                            GROUP BY {cand} ORDER BY n DESC LIMIT 10""")
            out["facts"][f"policy_{cand}_dist"] = [{"k": str(r[0])[:20], "n": int(r[1])} for r in cur.fetchall()]
    # 发布机构（权威渠道候选）
    org_col = next((c for c in pcols if "org" in c and ("publish" in c or "issue" in c or c == "publish_org"
                                                       or "agency" in c)), None)
    if not org_col:
        org_col = next((c for c in pcols if "org" in c or "agency" in c or "department" in c), None)
    out["facts"]["policy_org_col"] = org_col
    if org_col:
        cur.execute(f"""SELECT {org_col}, COUNT(*) AS n FROM gkx.dwd_policy_base
                        WHERE {org_col} IS NOT NULL AND {org_col} <> ''
                        GROUP BY {org_col} ORDER BY n DESC LIMIT 12""")
        out["facts"]["policy_org_top12"] = [{"k": str(r[0])[:24], "n": int(r[1])} for r in cur.fetchall()]
    # 区域列（对比区域候选）
    region_col = next((c for c in pcols if any(k in c for k in ("region", "province", "city", "district", "area"))), None)
    out["facts"]["policy_region_col"] = region_col
    if region_col:
        cur.execute(f"""SELECT {region_col}, COUNT(*) AS n FROM gkx.dwd_policy_base
                        WHERE {region_col} IS NOT NULL AND {region_col} <> ''
                        GROUP BY {region_col} ORDER BY n DESC LIMIT 12""")
        out["facts"]["policy_region_top12"] = [{"k": str(r[0])[:20], "n": int(r[1])} for r in cur.fetchall()]
    # 行业/产业列（产业覆盖候选）
    ind_col = next((c for c in pcols if any(k in c for k in ("industry", "field", "domain", "chain"))), None)
    out["facts"]["policy_industry_col"] = ind_col
    if ind_col:
        cur.execute(f"""SELECT {ind_col}, COUNT(*) AS n FROM gkx.dwd_policy_base
                        WHERE {ind_col} IS NOT NULL AND {ind_col} <> ''
                        GROUP BY {ind_col} ORDER BY n DESC LIMIT 10""")
        out["facts"]["policy_industry_top10"] = [{"k": str(r[0])[:22], "n": int(r[1])} for r in cur.fetchall()]
    # 年度×层级透视原料（发布密度/连续性）
    cur.execute("""SELECT SUBSTRING(CAST(publish_date AS CHAR),1,4) AS y, COUNT(*) AS n
                   FROM gkx.dwd_policy_base
                   WHERE publish_date IS NOT NULL AND year(publish_date) >= 2010
                   GROUP BY y ORDER BY y""")
    out["facts"]["policy_yearly_2010"] = [{"y": int(r[0]), "n": int(r[1])} for r in cur.fetchall()]
    # 全局政策表对照
    cur.execute("SHOW COLUMNS FROM gkx.dwd_global_policy_base")
    out["facts"]["global_policy_cols"] = [r[0] for r in cur.fetchall()][:22]
    cur.execute("""SELECT SUBSTRING(CAST(publish_date AS CHAR),1,4) AS y, COUNT(*) AS n
                   FROM gkx.dwd_global_policy_base
                   WHERE publish_date IS NOT NULL AND year(publish_date) >= 2010
                   GROUP BY y ORDER BY y""")
    out["facts"]["global_policy_yearly"] = [{"y": int(r[0]), "n": int(r[1])} for r in cur.fetchall()]
    # 外商投资目录候选（seq54：政策标题检索）
    cur.execute("""SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE title LIKE %s""", ("%外商%",))
    out["facts"]["policy_title_foreign_hits"] = int(cur.fetchone()[0])
    cur.execute("""SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE title LIKE %s""", ("%外商投资%",))
    out["facts"]["policy_title_fdi_hits"] = int(cur.fetchone()[0])
    cur.close()
    # live 政策面（政策查询页候选承载）
    try:
        conn = live("DWD")
        with conn.cursor() as c:
            c.execute("""SELECT table_name FROM information_schema.tables
                         WHERE table_schema='gkxlumenx_dwd' AND (table_name LIKE '%%policy%%'
                         OR table_name LIKE '%%news%%')""")
            tabs = [list(r.values())[0] for r in c.fetchall()]
            out["facts"]["live_policy_tables"] = tabs[:12]
            for t in tabs[:4]:
                c.execute(f"SELECT COUNT(*) AS n FROM `{t}`")
                out["facts"].setdefault("live_policy_rows", {})[t] = num(c.fetchone()["n"])
        conn.close()
    except Exception as e:  # noqa: BLE001
        out["facts"]["live_policy_tables"] = f"ERR:{type(e).__name__}: {e}"

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("saved", OUT_PATH)
    print("org_col =", out["facts"].get("policy_org_col"),
          "| region_col =", out["facts"].get("policy_region_col"),
          "| industry_col =", out["facts"].get("policy_industry_col"))


if __name__ == "__main__":
    main()

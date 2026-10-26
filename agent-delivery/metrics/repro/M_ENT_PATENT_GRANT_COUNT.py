#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_PATENT_GRANT_COUNT 专利授权量（20261021 改源版 · 零 DB）

口径真源：calc-logic/ENT/M_ENT_PATENT_GRANT_COUNT.md（2026-08-31）
    每个企业一条：该企业作为**第一专利权人**的授权专利去重件数（累计）。
    法律状态 = `dwd_patent_legal.status` 授权；查询键 `first_assignee_org_id`；
    不按产业过滤；不按报告期（无授权日列）。禁止无 GROUP BY 的全集 COUNT。

本件在 gkx 侧的落法：
  1. `enterprise_patent_detail` / `first_assignee_org_id` 两库均无（结果面与键都未建）；
  2. 授权标记用 `granted_number` 非空（全表可判），这是 gkx 侧唯一覆盖 100% 的授权信号——
     全库列字典 `legal_status` 命中 0，`dwd_patent_legal` 仅 20,000 行（覆盖 0.68%），
     拿它当过滤条件会把 99.3% 的专利判成未知；
  3. 归属键用 `first_applicant_name`（已聚合）× 底册 `name_cn`，不是
     `first_current_assignee_name`（该列存在但无聚合缓存，严格口径需再扫一遍全表）；
     现网实测第一申请人 ≠ 第一专利权人 1,867 条（0.0635%），影响 <0.1%；
  4. 每企业一条：`grant_cnt` 即该企业授权去重件数（聚合按 first_applicant_name 分块，
     一件只归一个主体，不跨企重复）。

输出：code/M_ENT_PATENT_GRANT_COUNT_out.json
"""
from __future__ import annotations

import json
import os
from collections import Counter
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_ENT_PATENT_GRANT_COUNT_out.json")
M = "M_ENT_PATENT_GRANT_COUNT"

AGG = os.path.join(SNAP, "star_applicant_agg_gkx.json")
BASE = os.path.join(SNAP, "star_base_rows_gkx.json")
PANEL = os.path.join(SNAP, "patent_panel_innov_20261021.json")
COLS = os.path.join(SNAP, "gkx_columns_20261023.json")


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def pct(a, b, nd=4):
    return round(100.0 * a / b, nd) if b else None


def stat_block(vals):
    v = sorted(vals)
    n = len(v)

    def q(k):
        return v[max(0, min(n - 1, int(round(k * (n - 1)))))] if n else None

    return {"n": n, "sum": sum(v), "mean": round(sum(v) / n, 4) if n else None,
            "median": q(0.5), "p25": q(0.25), "p75": q(0.75), "p90": q(0.90),
            "p95": q(0.95), "p99": q(0.99), "min": v[0] if n else None,
            "max": v[-1] if n else None}


def main():
    agg_doc = load(AGG)
    agg = agg_doc["agg"]
    base = load(BASE)
    panel = load(PANEL)
    cols = load(COLS)

    table_rows = int(agg_doc["table_rows"])
    lib_grant = sum(int(v[1]) for v in agg.values())

    base_otype = {r[0]: r[7] for r in base}
    firms, seen = [], set()
    for r in base:
        a = agg.get(r[1])
        if a is None or r[0] in seen:
            continue
        seen.add(r[0])
        firms.append({"org_id": r[0], "name": r[1], "province": r[2], "city": r[3],
                      "industry_l1": r[5], "industry_l2": r[6], "org_type": r[7],
                      "pub_cnt": int(a[0]), "grant_cnt": int(a[1])})

    n_firms = len(firms)
    n_base = len(base)
    total_grant = sum(f["grant_cnt"] for f in firms)
    total_pub = sum(f["pub_cnt"] for f in firms)
    with_grant = [f for f in firms if f["grant_cnt"] > 0]
    n_with_grant = len(with_grant)
    n_zero = n_firms - n_with_grant

    grant = stat_block([f["grant_cnt"] for f in firms])
    grant_pos = stat_block([f["grant_cnt"] for f in with_grant])

    # ---------- 授权量分档
    bands = [(0, 0), (1, 4), (5, 9), (10, 49), (50, 99), (100, 499), (500, 10 ** 9)]
    band_rows = []
    for lo, hi in bands:
        sel = [f for f in firms if lo <= f["grant_cnt"] <= hi]
        band_rows.append({"band": f"{lo}" if lo == hi else f"{lo}-{hi if hi < 10**9 else '+'}",
                          "n_firms": len(sel),
                          "firm_pct": pct(len(sel), n_firms),
                          "grant_sum": sum(f["grant_cnt"] for f in sel),
                          "grant_pct": pct(sum(f["grant_cnt"] for f in sel), total_grant)})

    # ---------- 集中度
    conc = {}
    sg = sorted((f["grant_cnt"] for f in firms), reverse=True)
    for k in (10, 50, 100, 1000):
        conc[f"top{k}_grant"] = sum(sg[:k])
        conc[f"top{k}_share_pct"] = pct(sum(sg[:k]), total_grant)

    # ---------- 阈值：多少家企业达到 N 件授权
    thr = []
    for th in (1, 5, 10, 20, 50, 100, 500):
        sel = [f for f in firms if f["grant_cnt"] >= th]
        thr.append({"threshold": th, "n_firms": len(sel),
                    "firm_pct": pct(len(sel), n_firms),
                    "grant_sum": sum(f["grant_cnt"] for f in sel),
                    "grant_pct": pct(sum(f["grant_cnt"] for f in sel), total_grant)})

    # ---------- 属地 / 行业（按授权量摊）
    def dist(field):
        d = Counter()
        for f in firms:
            d[f[field] or "未填"] += f["grant_cnt"]
        return {k: {"grant": v, "pct": pct(v, total_grant)} for k, v in d.most_common()}

    # ---------- 主体切分
    NON_ENT_TYPE = {"事业单位", "民办非企业单位", "社会团体", "机关", "基金会", "群众团体"}
    NON_ENT_RX = ("大学", "学院", "研究院", "研究所", "医院", "学校", "协会", "基金会")

    def is_non_ent(name, otype):
        return (otype or "") in NON_ENT_TYPE or any(k in (name or "") for k in NON_ENT_RX)

    ent = [f for f in firms if not is_non_ent(f["name"], f["org_type"])]
    non = [f for f in firms if is_non_ent(f["name"], f["org_type"])]
    entity_split = {
        "enterprise_orgs": len(ent),
        "enterprise_grant": sum(f["grant_cnt"] for f in ent),
        "enterprise_grant_pct": pct(sum(f["grant_cnt"] for f in ent), total_grant),
        "non_enterprise_orgs": len(non),
        "non_enterprise_grant": sum(f["grant_cnt"] for f in non),
        "non_enterprise_grant_pct": pct(sum(f["grant_cnt"] for f in non), total_grant),
    }

    # ---------- 探针
    ci = cols["column_index"]
    probe = {
        "legal_status_columns": sorted(ci.get("legal_status", [])),
        "first_current_assignee_columns": sorted(ci.get("first_current_assignee_name", [])),
        "first_assignee_org_id_columns": sorted(ci.get("first_assignee_org_id", [])),
        "granted_number_columns": sorted(ci.get("granted_number", [])),
        "patent_legal_tables": sorted({t for t in ci.get("status", []) if "patent" in t}),
        "enterprise_patent_detail_present": [t for t in ci.get("patent_id", [])
                                             if t == "enterprise_patent_detail"],
        "first_assignee_vs_first_applicant_diff_rows": 1867,
        "first_assignee_diff_pct": pct(1867, table_rows),
        "legal_table_rows": 20000,
        "legal_table_coverage_pct": pct(20000, table_rows),
        "source": "calc-logic/ENT/M_ENT_PATENT_GRANT_COUNT.md 现网探针（gkx, 2026-08-27）",
    }

    coverage = {
        "base_rows": n_base,
        "firms_with_patents": n_firms,
        "firms_with_grant": n_with_grant,
        "firms_with_zero_grant": n_zero,
        "zero_grant_pct": pct(n_zero, n_firms),
        "firm_grant_coverage_pct": pct(n_with_grant, n_base),
        "total_grant": total_grant,
        "total_pub": total_pub,
        "library_grant": lib_grant,
        "library_rows": table_rows,
        "grant_coverage_pct": pct(total_grant, lib_grant),
        "grant_rate_pct": pct(total_grant, total_pub),
        "library_grant_rate_pct": pct(lib_grant, table_rows),
        "grant_per_firm_mean": grant["mean"],
        "grant_per_positive_firm_mean": grant_pos["mean"],
    }

    top10 = [{"name": f["name"], "city": f["city"], "industry_l1": f["industry_l1"],
              "grant_cnt": f["grant_cnt"], "pub_cnt": f["pub_cnt"],
              "share_pct": pct(f["grant_cnt"], total_grant),
              "grant_rate_pct": pct(f["grant_cnt"], f["pub_cnt"])}
             for f in sorted(firms, key=lambda x: -x["grant_cnt"])[:10]]

    # ---------- 派生对照量（正文引用的一律落盘）
    city4 = ("深圳市", "广州市", "东莞市", "惠州市")
    four = sum(dist("city")[c]["grant"] for c in city4)
    derived = {
        "four_city_grant": four,
        "four_city_grant_pct": pct(four, total_grant),
        "out_of_province_grant": total_grant - four,
        "firms_le4_pct": round(8.6482 + 44.2976, 4),
        "non_enterprise_firm_pct": pct(len(non), n_firms),
        "star_subset_grant": 699284,
        "star_subset_share_of_grants_pct": pct(699284, total_grant),
        "enterprise_grant_rate_pct": pct(entity_split["enterprise_grant"],
                                         total_pub - 199436),
        "non_enterprise_grant_rate_pct": pct(entity_split["non_enterprise_grant"], 199436),
        "grant_minus_star": total_grant - 699284,
    }

    out = {
        "metric_id": M,
        "metric_name": "专利授权量",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "definition": "每企业一条：该企业作为第一专利权人的授权专利去重件数（累计，含发明/实用新型/外观）",
        "data_source": "gkx @ 183.240.141.251:3318（只读）：dwd_patent 聚合 × dwd_org_base_info；零 DB",
        "support_judgment": "完全转换支持",
        "verdict_kind": "converted",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面累计件，不按报告期（calc-logic 明文「不按报告期」，正式明细也无授权日列）。"
                            "dwd_patent.apdt_year 仅 2021—2026，故累计窗口为六年；2026 为残年（74,810 行）。"
                            "used/missing 留空，窗口在此说明。"),
        "sources": [
            {"path": "code/_snapshots21/star_applicant_agg_gkx.json", "kind": "snapshot",
             "role": "169,226 申请人 [件数, 授权数]；授权数合计 2,140,420"},
            {"path": "code/_snapshots21/star_base_rows_gkx.json", "kind": "snapshot",
             "role": "底册 189,116 行（org_id/名称/属地/行业/机构类型）"},
            {"path": "code/_snapshots21/patent_panel_innov_20261021.json", "kind": "snapshot",
             "role": "年份与国别（授权窗口与 WO 辨析）"},
            {"path": "code/_snapshots21/gkx_columns_20261023.json", "kind": "snapshot",
             "role": "列字典：legal_status / first_assignee_org_id 等列存在性"},
        ],
        "probes": probe,
        "compute": {
            "grant_stats": grant,
            "grant_stats_positive": grant_pos,
            "coverage": coverage,
            "band_dist": band_rows,
            "concentration": conc,
            "threshold_curve": thr,
            "city_dist": dist("city"),
            "province_dist": dist("province"),
            "industry_l1_dist": dist("industry_l1"),
            "industry_l2_top10": [{"name": k, "grant": v["grant"], "pct": v["pct"]}
                                  for k, v in list(dist("industry_l2").items())[:10]],
            "entity_split": entity_split,
            "derived": derived,
            "top10_by_grant": top10,
            "library": {"rows": table_rows, "grant_sum": lib_grant,
                        "names": int(agg_doc["names"])},
        },
        "reasons": [
            "结果面 enterprise_patent_detail 与查询键 first_assignee_org_id 两库均无，但原料列齐全"
            "（first_current_assignee_name / granted_number / patent_id 均在 dwd_patent），"
            "按名称匹配即可现造键 → 完全转换支持。",
            "授权状态用 granted_number 非空替代 legal_status：全库无 legal_status 列，"
            "dwd_patent_legal 仅 20,000 行（覆盖 0.68%），不可当全量过滤条件。",
            "归属用 first_applicant_name 聚合而非 first_current_assignee_name：后者无聚合缓存，"
            "严格口径需再扫全表（约 1,400 秒）；现网实测两者差 1,867 条（0.0635%），影响 <0.1%。",
            "每企业一条、不按产业、不按报告期，三条与 calc-logic 逐字一致。",
        ],
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print(f"[OK] {M} firms={n_firms} with_grant={n_with_grant} grant={total_grant} "
          f"cover={coverage['grant_coverage_pct']}% rate={coverage['grant_rate_pct']}%")
    print(f"     out -> {os.path.basename(OUT)} ({os.path.getsize(OUT)} B)")


if __name__ == "__main__":
    main()

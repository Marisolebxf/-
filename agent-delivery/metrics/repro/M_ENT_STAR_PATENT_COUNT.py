#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_STAR_PATENT_COUNT 明星企业专利数（20261021 改源版 · 零 DB）

口径真源（王惠 20260816 底稿 → calc-logic 2026-08-31）：
    「选定未来产业范围内，明星企业累计专利件数（授权口径），按企业唯一标识去重聚合。
      明星企业由后台 CMS 定义。」
    calc-logic 的计算说明： CMS 名单 → dwd_patent 按 assignees 匹配企业名 → COUNT 专利件数。

本件在 gkx 侧的落法：
  1. 明星名单不可得（CMS 无表），沿用 STAR 簇共用代理名单
     `star_roster_gkx_20261021.json`（4,561 家，授权>=50 且剔除非企业主体）；
  2. 专利件数不重扫 `dwd_patent`（2,939,895 行、无索引，全表 GROUP BY 会被服务端杀），
     直接读全量聚合 `star_applicant_agg_gkx.json`：agg[name] = [件数, 授权数]，
     两分量合计分别 2,939,895 / 2,140,420，与表行数逐位相等（PATENT_SCAN_LEDGER §二）；
  3. 主口径按王惠「授权口径」= agg[name][1]；calc-logic 未写法律状态过滤，
     故同时交「累计公开件数」= agg[name][0] 作为对照口径，并在正文说明两者差 37.0%；
  4. 「未来产业范围内」不可得：gkx 280 表无 `future_industry_code` / `cluster_id` 列
     （列字典 column_index 命中 0），本件只能交全量，不能交产业切片。

输出：code/M_ENT_STAR_PATENT_COUNT_out.json
"""
from __future__ import annotations

import json
import os
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_ENT_STAR_PATENT_COUNT_out.json")
M = "M_ENT_STAR_PATENT_COUNT"

ROSTER = os.path.join(SNAP, "star_roster_gkx_20261021.json")
AGG = os.path.join(SNAP, "star_applicant_agg_gkx.json")
BASE = os.path.join(SNAP, "star_base_rows_gkx.json")
COLS = os.path.join(SNAP, "gkx_columns_20261023.json")
PANEL = os.path.join(SNAP, "patent_panel_innov_20261021.json")


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def pct(a, b, nd=4):
    return round(100.0 * a / b, nd) if b else None


def stat_block(vals):
    """分位与均值（最近秩法，不插值，保证每个数都能在名单里找到原值）。"""
    v = sorted(vals)
    n = len(v)

    def q(k):
        if not n:
            return None
        i = max(0, min(n - 1, int(round(k * (n - 1)))))
        return v[i]

    return {
        "n": n,
        "sum": sum(v),
        "mean": round(sum(v) / n, 4) if n else None,
        "median": q(0.5),
        "p25": q(0.25),
        "p75": q(0.75),
        "p90": q(0.90),
        "p95": q(0.95),
        "p99": q(0.99),
        "min": v[0] if n else None,
        "max": v[-1] if n else None,
    }


def main():
    roster = load(ROSTER)
    agg_doc = load(AGG)
    agg = agg_doc["agg"]
    base = load(BASE)
    cols = load(COLS)
    panel = load(PANEL)

    rows = roster["rows"]
    n_star = len(rows)
    table_rows = int(agg_doc["table_rows"])
    lib_pub = sum(int(v[0]) for v in agg.values())
    lib_grant = sum(int(v[1]) for v in agg.values())

    # ---------- 1 名单内专利量（两个口径）
    pub_vals = [int(r["pub_cnt"]) for r in rows]
    grant_vals = [int(r["grant_cnt"]) for r in rows]
    pub = stat_block(pub_vals)
    grant = stat_block(grant_vals)

    # ---------- 2 集中度：前 N 家占比
    cum = {}
    sp = sorted(pub_vals, reverse=True)
    for k in (10, 50, 100, 500):
        cum[f"top{k}_share_pct"] = pct(sum(sp[:k]), pub["sum"])
        cum[f"top{k}_patents"] = sum(sp[:k])

    # ---------- 3 属地 × 行业（按名单企业把专利量摊到属地/行业）
    city, prov, ind1, ind2 = {}, {}, {}, {}
    for r in rows:
        p = int(r["pub_cnt"])
        city[r.get("city") or "未填"] = city.get(r.get("city") or "未填", 0) + p
        prov[r.get("province") or "未填"] = prov.get(r.get("province") or "未填", 0) + p
        ind1[r.get("industry_l1_name") or "未填"] = ind1.get(r.get("industry_l1_name") or "未填", 0) + p
        ind2[r.get("industry_l2_name") or "未填"] = ind2.get(r.get("industry_l2_name") or "未填", 0) + p

    def dist(d):
        return {k: {"patents": v, "pct": pct(v, pub["sum"])}
                for k, v in sorted(d.items(), key=lambda x: -x[1])}

    # ---------- 4 名单阈值敏感性：阈值一改，专利总量跟着改
    curve = []
    NON_ENT_TYPE = {"事业单位", "民办非企业单位", "社会团体", "机关", "基金会", "群众团体"}
    NON_ENT_RX = ("大学", "学院", "研究院", "研究所", "医院", "学校", "协会", "基金会")

    def is_non_ent(name, otype):
        return (otype or "") in NON_ENT_TYPE or any(k in (name or "") for k in NON_ENT_RX)

    for th in (20, 30, 50, 80, 100, 200, 500):
        # 与 M_ENT_STAR_ENTERPRISE_COUNT 的阈值曲线同规则：底册逐行 × agg 授权数 × 剔非企业主体，
        # 唯一变量是阈值。这样两件的曲线逐点可比（同一母体、同一剔除规则）。
        sel = [r for r in base
               if r[1] in agg and int(agg[r[1]][1]) >= th and not is_non_ent(r[1], r[7])]
        s_pub = sum(int(agg[r[1]][0]) for r in sel)
        s_grant = sum(int(agg[r[1]][1]) for r in sel)
        curve.append({"threshold_grant": th, "n_firms": len(sel), "pub_sum": s_pub,
                      "grant_sum": s_grant,
                      "pub_share_of_library_pct": pct(s_pub, lib_pub),
                      "grant_share_of_library_pct": pct(s_grant, lib_grant),
                      "method": "base_rows_x_agg_minus_non_enterprise"})

    # ---------- 5 探针：未来产业 / 法律状态 / assignees 多值
    # 列字典 column_index = {列名: [表名...]}（280 表 / 6,312 列）
    ci = cols["column_index"]
    key_hits = {kw: sorted(ci.get(kw, [])) for kw in
                ("future_industry_code", "future_industry_name", "cluster_id",
                 "legal_status", "first_current_assignee_name", "granted_number",
                 "assignee_name")}
    # 近似列名也查一遍，防止列名带前后缀（结果另存 fuzzy，不当否定证据）
    fuzzy = {kw: sorted(k for k in ci if kw in k and k != kw) for kw in key_hits}

    multi = {
        "note": "受让人多值会重复计件；本件按 first_applicant_name 聚合，一件只归第一申请人，故不重复但会漏计非第一受让人",
        "first_assignee_vs_first_applicant_diff_rows": 1867,
        "source": "calc-logic/ENT/M_ENT_PATENT_GRANT_COUNT.md 现网探针（gkx, 2026-08-27）",
    }

    # ---------- 6 覆盖率：名单占全库专利的比例
    # 名单企业数分布（与 M_ENT_STAR_BY_REGION 同源，供正文对照用）
    from collections import Counter
    city_firm = Counter((r.get("city") or "未填") for r in rows)
    city_firm_dist = {k: {"firms": v, "pct": pct(v, n_star)}
                      for k, v in city_firm.most_common()}

    coverage = {
        "n_star": n_star,
        "star_pub_sum": pub["sum"],
        "star_grant_sum": grant["sum"],
        "library_pub_sum": lib_pub,
        "library_grant_sum": lib_grant,
        "star_share_of_library_pub_pct": pct(pub["sum"], lib_pub),
        "star_share_of_library_grant_pct": pct(grant["sum"], lib_grant),
        "star_grant_rate_pct": pct(grant["sum"], pub["sum"]),
        "library_grant_rate_pct": pct(lib_grant, lib_pub),
        "star_share_of_firms_pct": pct(n_star, len(base)),
        "base_rows": len(base),
        "patents_per_star_mean_pub": round(pub["sum"] / n_star, 4),
        "patents_per_star_mean_grant": round(grant["sum"] / n_star, 4),
    }

    # ---------- 7 口径差：授权 vs 累计
    delta = pub["sum"] - grant["sum"]
    diff = {
        "pub_minus_grant": delta,
        "pub_minus_grant_pct_of_pub": pct(delta, pub["sum"]),
        "wanghui_definition": "累计专利件数（授权口径）→ 用 grant_sum",
        "calc_logic_definition": "COUNT 专利件数（未写法律状态）→ 用 pub_sum",
        "chosen": "grant_sum",
        "reason": "王惠正本逐字写「授权口径」，calc-logic 的 SQL 未写 WHERE；两者冲突时以正本为准，另一口径并列交付",
    }

    # ---------- 8 top10
    top10 = [{"name": r["name_cn"], "city": r.get("city"), "industry_l1": r.get("industry_l1_name"),
              "pub_cnt": int(r["pub_cnt"]), "grant_cnt": int(r["grant_cnt"]),
              "share_of_star_pub_pct": pct(int(r["pub_cnt"]), pub["sum"])}
             for r in sorted(rows, key=lambda x: -int(x["pub_cnt"]))[:10]]

    out = {
        "metric_id": M,
        "metric_name": "明星企业专利数",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "definition": "明星企业（CMS 名单，本件以代理名单替代）名下累计专利件数（授权口径）",
        "data_source": "gkx @ 183.240.141.251:3318（只读）：dwd_patent 全量聚合 × dwd_org_base_info；本脚本零 DB，只读快照",
        "support_judgment": "部分支持",
        "verdict_kind": "proxy_roster",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面累计件，无报告期。专利侧 dwd_patent 的 apdt_year 只覆盖 2021—2026"
                            "（2017—2020 零行，DATA_FACTS §3.13），故「累计」实为 2021—2026 六年累计；"
                            "2026 为残年（74,810 行）。名单无年度字段，不构成年度序列，故 used/missing 均为空。"),
        "sources": [
            {"path": "code/_snapshots21/star_roster_gkx_20261021.json", "kind": "snapshot",
             "role": "代理名单 4,561 家（grant_cnt>=50，剔除非企业主体）"},
            {"path": "code/_snapshots21/star_applicant_agg_gkx.json", "kind": "snapshot",
             "role": "169,226 申请人 [件数, 授权数]，全量 2,939,895 行聚合"},
            {"path": "code/_snapshots21/star_base_rows_gkx.json", "kind": "snapshot",
             "role": "底册 189,116 行（名称/省/市/行业）"},
            {"path": "code/_snapshots21/patent_panel_innov_20261021.json", "kind": "snapshot",
             "role": "专利面板：年/国别/件型，用于年份窗口与件型结构"},
            {"path": "code/_snapshots21/gkx_columns_20261023.json", "kind": "snapshot",
             "role": "全库列字典 280 表 / 6,312 列，用于「未来产业/法律状态列是否存在」探针"},
        ],
        "probes": {
            "future_industry_columns": key_hits.get("future_industry_code", []),
            "cluster_columns": key_hits.get("cluster_id", []),
            "legal_status_columns": key_hits.get("legal_status", []),
            "first_current_assignee_columns": key_hits.get("first_current_assignee_name", []),
            "granted_number_columns": key_hits.get("granted_number", []),
            "assignee_name_columns": key_hits.get("assignee_name", []),
            "fuzzy_column_names": fuzzy,
            "panel_country": panel.get("country"),
            "panel_year_all": panel.get("year_all"),
            "panel_rows": panel.get("rows"),
        },
        "compute": {
            "roster_threshold_grant": int(roster["threshold_grant"]),
            "n_star": n_star,
            "pub_stats": pub,
            "grant_stats": grant,
            "coverage": coverage,
            "concentration": cum,
            "city_dist_pub": dist(city),
            "city_firm_dist": city_firm_dist,
            "value_field": {"nonnull": 1994812, "mean": 17760.56,
                            "fill_pct": pct(1994812, table_rows),
                            "note": "dwd_patent.value：无单位，仅作旁证，不进公式"},
            "province_dist_pub": dist(prov),
            "industry_l1_dist_pub": dist(ind1),
            "industry_l2_top10_pub": [{"name": k, "patents": v["patents"], "pct": v["pct"]}
                                      for k, v in list(dist(ind2).items())[:10]],
            "threshold_curve": curve,
            "definition_conflict": diff,
            "multi_assignee": multi,
            "top10_by_pub": top10,
            "library": {"table_rows": table_rows, "names": int(agg_doc["names"]),
                        "pub_sum": lib_pub, "grant_sum": lib_grant},
        },
        "reasons": [
            "CMS 明星名单两库均无（gkx 280 表 star/roster/cms 命中 0），名单维度只能用代理（授权>=50），"
            "故本件数的是「代理名单的专利量」，不是「CMS 明星的专利量」。",
            "「选定未来产业范围内」不可得：gkx 无 future_industry_code / cluster_id 列（列字典命中 0），"
            "无法把专利量切到未来产业子集。",
            "口径冲突：王惠正本写「授权口径」，calc-logic 的 SQL 无法律状态过滤；本件以正本为主口径（699,284），"
            "并列交付累计公开口径（1,069,438），差额 370,154（34.61%）。",
            "专利只按第一申请人归属：first_applicant_name 聚合无法覆盖「非第一受让人」的共有专利，"
            "且第一申请人≠第一专利权人（现网差 1,867 条）。",
        ],
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print(f"[OK] {M} n_star={n_star} pub={pub['sum']} grant={grant['sum']} "
          f"share_grant={coverage['star_share_of_library_grant_pct']}%")
    print(f"     out -> {os.path.basename(OUT)} ({os.path.getsize(OUT)} B)")
    print("     probes:", {k: len(v) for k, v in key_hits.items()})


if __name__ == "__main__":
    main()

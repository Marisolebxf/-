#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_PATENT_TOTAL 专利总量（20261021 改源版 · 零 DB）

口径真源：calc-logic/ENT/M_ENT_PATENT_TOTAL.md（2026-08-27 COVER-STAT-L01）
    「企业作为专利权人（受让人映射到 org_id）的专利去重件数。授权 / 公开 / 审查中均计入，
      不过滤 legal_status。COUNT(DISTINCT patent_id) FROM enterprise_patent_detail。」
    关键约束：不按产业过滤；无独立国外专利表；名称对不上的权利人 drop。

本件在 gkx 侧的落法：
  1. `enterprise_patent_detail` 两库均无结果面（gkx 280 表命中 0，live 开发库为空壳），
     但原料表齐全：`dwd_patent`（2,939,895 行 / 55 列）+ `dwd_org_base_info`（189,116 行）；
  2. 不重扫 `dwd_patent`（无索引，全表 GROUP BY 会被服务端 600 秒时限杀掉），
     读全量聚合 `star_applicant_agg_gkx.json`：agg[name] = [件数, 授权数]，件数合计逐位等于表行数；
  3. `org_id` 由「底册 name_cn 精确等值 agg 键」产生（calc-logic 的 ETL 同名匹配口径），
     同名多企各匹配一次但按 org_id 去重；匹配不上的权利人 drop（calc-logic 明文要求）；
  4. 「去重」在本库里只能做到 `patent_id` 级：`dwd_patent` 一个 patent_id 一行，
     聚合按 first_applicant_name 分块求和，一件专利只归第一申请人，故不会跨企重复计；
     代价是非第一受让人的共有专利会被漏掉（无 assignees 多值列）。

输出：code/M_ENT_PATENT_TOTAL_out.json
"""
from __future__ import annotations

import json
import os
from collections import Counter
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_ENT_PATENT_TOTAL_out.json")
M = "M_ENT_PATENT_TOTAL"

AGG = os.path.join(SNAP, "star_applicant_agg_gkx.json")
BASE = os.path.join(SNAP, "star_base_rows_gkx.json")
PANEL = os.path.join(SNAP, "patent_panel_innov_20261021.json")
SAMPLE = os.path.join(SNAP, "a25_patent_sample.json")
VALUE = os.path.join(SNAP, "patent_value_agg_gkx.json")
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
        if not n:
            return None
        return v[max(0, min(n - 1, int(round(k * (n - 1)))) )]

    return {"n": n, "sum": sum(v), "mean": round(sum(v) / n, 4) if n else None,
            "median": q(0.5), "p25": q(0.25), "p75": q(0.75), "p90": q(0.90),
            "p95": q(0.95), "p99": q(0.99), "min": v[0] if n else None,
            "max": v[-1] if n else None}


def main():
    agg_doc = load(AGG)
    agg = agg_doc["agg"]
    base = load(BASE)
    panel = load(PANEL)
    value = load(VALUE)
    cols = load(COLS)

    table_rows = int(agg_doc["table_rows"])
    lib_grant = sum(int(v[1]) for v in agg.values())

    # ---------- 1 org 级归属：底册 name_cn == agg 键
    firms = []
    base_otype = {r[0]: r[7] for r in base}
    seen = set()
    for r in base:                       # [org_id, name_cn, province, city, area, l1, l2, type]
        nm = r[1]
        a = agg.get(nm)
        if a is None:
            continue
        if r[0] in seen:
            continue
        seen.add(r[0])
        firms.append({"org_id": r[0], "name": nm, "province": r[2], "city": r[3],
                      "area": r[4], "industry_l1": r[5], "industry_l2": r[6],
                      "pub_cnt": int(a[0]), "grant_cnt": int(a[1])})

    n_firms = len(firms)
    total_pub = sum(f["pub_cnt"] for f in firms)
    total_grant = sum(f["grant_cnt"] for f in firms)
    unmatched_rows = table_rows - total_pub
    base_names = {r[1] for r in base}
    matched_names = len([k for k in agg if k in base_names])

    pub = stat_block([f["pub_cnt"] for f in firms])
    grant = stat_block([f["grant_cnt"] for f in firms])
    only_grant_zero = sum(1 for f in firms if f["grant_cnt"] == 0)

    # ---------- 2 集中度
    conc = {}
    sp = sorted((f["pub_cnt"] for f in firms), reverse=True)
    for k in (10, 50, 100, 1000):
        conc[f"top{k}_patents"] = sum(sp[:k])
        conc[f"top{k}_share_pct"] = pct(sum(sp[:k]), total_pub)

    # ---------- 3 属地 / 行业（件数摊到企业属性）
    def dist(field):
        d = Counter()
        for f in firms:
            d[f[field] or "未填"] += f["pub_cnt"]
        return {k: {"patents": v, "pct": pct(v, total_pub)} for k, v in d.most_common()}

    def dist_n(field):
        d = Counter(f[field] or "未填" for f in firms)
        return {k: {"firms": v, "pct": pct(v, n_firms)} for k, v in d.most_common()}

    city = dist("city")
    province = dist("province")
    ind1 = dist("industry_l1")
    ind2 = dist("industry_l2")
    city_firms = dist_n("city")

    # ---------- 4 件型（抽样 6.8%，全表扫描不可行）
    sample = load(SAMPLE)
    srows = sample["rows"]
    kind = Counter(r.get("kind") for r in srows)
    sampled = len(srows)
    kind_dist = {k: {"rows": v, "pct": pct(v, sampled)} for k, v in kind.most_common()}

    # ---------- 5 探针
    ci = cols["column_index"]
    probe = {
        "enterprise_patent_detail_present": sorted(ci.get("patent_id", [])) and
        [t for t in ci.get("patent_id", []) if t == "enterprise_patent_detail"],
        "patent_tables_in_gkx": sorted({t for t in ci.get("patent_id", [])}),
        "industry_columns": sorted(k for k in ci if "industry" in k)[:12],
        "future_industry_columns": sorted(ci.get("future_industry_code", [])),
        "assignee_columns": sorted(k for k in ci if "assignee" in k),
        "legal_status_columns": sorted(ci.get("legal_status", [])),
    }

    # ---------- 6 覆盖
    coverage = {
        "base_rows": len(base),
        "firms_with_patents": n_firms,
        "firms_without_patents": len(base) - n_firms,
        "firm_coverage_pct": pct(n_firms, len(base)),
        "total_pub": total_pub,
        "total_grant": total_grant,
        "library_rows": table_rows,
        "library_grant": lib_grant,
        "pub_coverage_pct": pct(total_pub, table_rows),
        "grant_coverage_pct": pct(total_grant, lib_grant),
        "unmatched_rows": unmatched_rows,
        "unmatched_rows_pct": pct(unmatched_rows, table_rows),
        "name_match_pct": pct(matched_names, int(agg_doc["names"])),
        "matched_names": matched_names,
        "agg_names": int(agg_doc["names"]),
        "firms_with_zero_grant": only_grant_zero,
        "grant_rate_pct": pct(total_grant, total_pub),
        "library_grant_rate_pct": pct(lib_grant, table_rows),
        "value_fill_pct": pct(int(value["n_nonnull"]), table_rows),
        "value_mean": value.get("mean"),
    }

    # ---------- 6b 主体切分：主档里含高校/院所/医院，calc-logic 语义是「企业」
    NON_ENT_TYPE = {"事业单位", "民办非企业单位", "社会团体", "机关", "基金会", "群众团体"}
    NON_ENT_RX = ("大学", "学院", "研究院", "研究所", "医院", "学校", "协会", "基金会")

    def is_non_ent(name, otype):
        return (otype or "") in NON_ENT_TYPE or any(k in (name or "") for k in NON_ENT_RX)

    non_ent = [f for f in firms if is_non_ent(f["name"], base_otype.get(f["org_id"]))]
    ent = [f for f in firms if not is_non_ent(f["name"], base_otype.get(f["org_id"]))]
    entity_split = {
        "non_enterprise_orgs": len(non_ent),
        "non_enterprise_pub": sum(f["pub_cnt"] for f in non_ent),
        "non_enterprise_pub_pct": pct(sum(f["pub_cnt"] for f in non_ent), total_pub),
        "enterprise_orgs": len(ent),
        "enterprise_pub": sum(f["pub_cnt"] for f in ent),
        "enterprise_pub_pct": pct(sum(f["pub_cnt"] for f in ent), total_pub),
        "enterprise_grant": sum(f["grant_cnt"] for f in ent),
        "enterprise_grant_pct": pct(sum(f["grant_cnt"] for f in ent), total_grant),
        "top_non_enterprise": sorted(
            [{"name": f["name"], "pub_cnt": f["pub_cnt"], "grant_cnt": f["grant_cnt"]}
             for f in non_ent], key=lambda x: -x["pub_cnt"])[:5],
    }

    top10 = [{"name": f["name"], "city": f["city"], "industry_l1": f["industry_l1"],
              "pub_cnt": f["pub_cnt"], "grant_cnt": f["grant_cnt"],
              "share_pct": pct(f["pub_cnt"], total_pub)}
             for f in sorted(firms, key=lambda x: -x["pub_cnt"])[:10]]

    # ---------- 6c 派生对照量（正文引用的一律落盘，避免"正文有、产物无"）
    city4 = ("深圳市", "广州市", "东莞市", "惠州市")
    top5_ne = sum(x["pub_cnt"] for x in entity_split["top_non_enterprise"])
    derived = {
        "non_enterprise_grant": total_grant - entity_split["enterprise_grant"],
        "non_enterprise_grant_pct": pct(total_grant - entity_split["enterprise_grant"], total_grant),
        "firms_with_zero_grant_pct": pct(only_grant_zero, n_firms),
        "top5_non_enterprise_pub": top5_ne,
        "top5_non_enterprise_share_pct": pct(top5_ne, entity_split["non_enterprise_pub"]),
        "four_city_pub": sum(city[c]["patents"] for c in city4),
        "four_city_pub_pct": pct(sum(city[c]["patents"] for c in city4), total_pub),
        "out_of_province_pub": total_pub - province["广东省"]["patents"],
        "pub_minus_grant": total_pub - total_grant,
        "pub_minus_grant_pct_of_pub": pct(total_pub - total_grant, total_pub),
        "star_subset_pub": 1069438,
        "star_subset_share_of_matched_pct": pct(1069438, total_pub),
        "top1pct_firms": max(1, n_firms // 100),
        "unmatched_names": int(agg_doc["names"]) - matched_names,
        "firms_without_patents_pct": pct(len(base) - n_firms, len(base)),
        "kind_ab_pct": round(kind_dist.get("A", {}).get("pct", 0) + kind_dist.get("B", {}).get("pct", 0), 4),
        "country_china_pct": pct(panel["country"]["China"], table_rows),
        "country_wo_pct": pct(panel["country"]["WO"], table_rows),
    }

    out = {
        "metric_id": M,
        "metric_name": "专利总量",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "definition": "企业作为专利权人（受让人映射到 org_id）的专利去重件数；不过滤法律状态，不按产业过滤",
        "data_source": "gkx @ 183.240.141.251:3318（只读）：dwd_patent 全量聚合 × dwd_org_base_info；本脚本零 DB",
        "support_judgment": "完全转换支持",
        "verdict_kind": "converted",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面累计件，无报告期。dwd_patent.apdt_year 仅 2021—2026（2017—2020 零行），"
                            "故「总量」实为六年窗口累计；2026 为残年（74,810 行）。本指标不按年报期，"
                            "因此 used/missing 留空，年份窗口在此说明。"),
        "sources": [
            {"path": "code/_snapshots21/star_applicant_agg_gkx.json", "kind": "snapshot",
             "role": "169,226 申请人 [件数, 授权数]，件数合计 = 表行数 2,939,895"},
            {"path": "code/_snapshots21/star_base_rows_gkx.json", "kind": "snapshot",
             "role": "底册 189,116 行（org_id/名称/省/市/区/行业/机构类型）"},
            {"path": "code/_snapshots21/patent_panel_innov_20261021.json", "kind": "snapshot",
             "role": "全量面板：年 / 国别 / IPC（10 块，2,939,895 行）"},
            {"path": "code/_snapshots21/a25_patent_sample.json", "kind": "snapshot",
             "role": "20 万行连续切片（6.8%），用于件型分布"},
            {"path": "code/_snapshots21/patent_value_agg_gkx.json", "kind": "snapshot",
             "role": "value 字段填充率与均值（旁证，不进公式）"},
            {"path": "code/_snapshots21/gkx_columns_20261023.json", "kind": "snapshot",
             "role": "全库列字典，用于「结果表/产业列/受让人列是否存在」探针"},
        ],
        "probes": probe,
        "compute": {
            "pub_stats": pub,
            "grant_stats": grant,
            "coverage": coverage,
            "concentration": conc,
            "city_dist": city,
            "city_firm_dist": city_firms,
            "province_dist": province,
            "industry_l1_dist": ind1,
            "industry_l2_top10": [{"name": k, "patents": v["patents"], "pct": v["pct"]}
                                  for k, v in list(ind2.items())[:10]],
            "kind_dist_sample": kind_dist,
            "kind_sample_share_pct": pct(sampled, table_rows),
            "year_dist": panel.get("year_all"),
            "country_dist": panel.get("country"),
            "top10_by_pub": top10,
            "entity_split": entity_split,
            "derived": derived,
            "library": {"table_rows": table_rows, "names": int(agg_doc["names"]),
                        "grant_sum": lib_grant},
        },
        "reasons": [
            "结果面 enterprise_patent_detail 两库均无（gkx 280 表无此表，live 为空壳），但原料侧 dwd_patent "
            "2,939,895 行 + 底册 189,116 行齐全，件数可现算 → 完全转换支持。",
            "名称等值匹配覆盖 157,363/189,116 家企业（83.2% 的企业有专利），匹配不上的权利人按 calc-logic 要求 drop。",
            "专利件数只归第一申请人：无 assignees 多值列，非第一受让人的共有专利会漏计（方向明确，幅度不可量化）。",
            "不按产业过滤是 calc-logic 明文要求；gkx 也没有 future_industry_code 列，这一点与口径要求恰好一致。",
        ],
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print(f"[OK] {M} firms={n_firms} base={len(base)} pub={total_pub} grant={total_grant} "
          f"cover={coverage['pub_coverage_pct']}%")
    print(f"     out -> {os.path.basename(OUT)} ({os.path.getsize(OUT)} B)")


if __name__ == "__main__":
    main()

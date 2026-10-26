#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全球服务机构产业布局（M_SVC_INDUSTRY_LAYOUT）—— gkx 口径，自包含。

分析单元 = 服务机构（池 44,153 家）× 三维交叉：
    地理维  prov → city(4 市) → area(区/县，26 个)
    产业维  ind（国民经济行业门类 20 类，来自 dwd_org_base_info.ind）
    服务维  ptype2（主服务类型 7 类）+ stages（服务环节标签 6 类）

指标：格子机构数、行/列占比、城市内产业 HHI、产业内城市 HHI、CR3、
      服务类型香农熵（多样化度）、服务环节渗透率。

口径声明（重要，决定判档）：
    池内 prov 非空 44,132 家全部为「广东省」，无境外机构、无 country 字段，
    因此「全球」维在本库**无法实现**，退化为广东省内 4 市 + 26 区；产业维只有
    门类级（无中类/小类），故判「部分支持」而非完全转换支持。

数据源：code/_snapshots21/svc21_facts_20261022.json
产出：code/M_SVC_INDUSTRY_LAYOUT_out.json
运行：cd code && python3 M_SVC_INDUSTRY_LAYOUT.py
"""
from __future__ import annotations

import collections
import json
import math
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
FACTS = os.path.join(HERE, "_snapshots21", "svc21_facts_20261022.json")
OUT = os.path.join(HERE, "M_SVC_INDUSTRY_LAYOUT_out.json")

CITY_ORDER = ["深圳市", "广州市", "东莞市", "惠州市"]
STAGES = ["stage-research", "stage-ip", "stage-transfer", "stage-pilot", "stage-testing", "stage-market"]
STAGE_CN = {"stage-research": "研发", "stage-ip": "知识产权", "stage-transfer": "技术转移",
            "stage-pilot": "中试", "stage-testing": "检测检验", "stage-market": "市场化"}


def hhi(counter, total=None):
    t = total or sum(counter.values())
    if not t:
        return 0.0
    return sum((v / t) ** 2 for v in counter.values())


def entropy(counter):
    t = sum(counter.values())
    if not t:
        return 0.0
    return -sum((v / t) * math.log(v / t) for v in counter.values() if v)


def share(counter, total):
    return {k: round(v / total * 100, 2) for k, v in counter.items()} if total else {}


def main():
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    pool = f["pool"]
    bf = f["base_fields"]
    meta = f.get("base_fields_meta") or {}
    N = len(pool)

    recs = []
    for oid, v in pool.items():
        b = bf.get(oid) or {}
        recs.append({
            "id": oid, "city": v.get("city") or "(空)",
            "prov": v.get("prov") or "(空)",
            "area": b.get("area") or "(空)",
            "ind": b.get("ind") or "(空)",
            "type": v.get("ptype2") or "UNCLASSIFIED",
            "stages": v.get("stages") or [],
            "len": v.get("len") or 0,
        })

    n_ind = sum(1 for r in recs if r["ind"] != "(空)")
    n_area = sum(1 for r in recs if r["area"] != "(空)")
    n_city = sum(1 for r in recs if r["city"] != "(空)")

    # ---- 1. 地理分布 --------------------------------------------------------
    city_c = collections.Counter(r["city"] for r in recs)
    prov_c = collections.Counter(r["prov"] for r in recs)
    area_c = collections.Counter(r["area"] for r in recs if r["area"] != "(空)")
    city_sorted = sorted(city_c.items(), key=lambda x: -x[1])
    cr3 = round(sum(v for _, v in city_sorted[:3]) / N * 100, 2)

    # ---- 2. 城市 × 产业 -----------------------------------------------------
    ind_c = collections.Counter(r["ind"] for r in recs)
    city_ind = collections.defaultdict(collections.Counter)
    for r in recs:
        city_ind[r["city"]][r["ind"]] += 1

    # ---- 3. 服务类型 × 产业 ------------------------------------------------
    type_c = collections.Counter(r["type"] for r in recs)
    type_ind = collections.defaultdict(collections.Counter)
    for r in recs:
        type_ind[r["type"]][r["ind"]] += 1

    # ---- 4. 城市 × 服务类型 ------------------------------------------------
    city_type = collections.defaultdict(collections.Counter)
    for r in recs:
        city_type[r["city"]][r["type"]] += 1

    # ---- 5. 服务环节渗透 ----------------------------------------------------
    stage_city = {st: collections.Counter() for st in STAGES}
    stage_all = collections.Counter()
    for r in recs:
        for s in r["stages"]:
            stage_all[s] += 1
            stage_city.setdefault(s, collections.Counter())[r["city"]] += 1

    # ---- 6. 布局格子（city × ind，取量级 top） ------------------------------
    cells = []
    for c, cc in city_ind.items():
        tot = sum(cc.values())
        for i, v in cc.items():
            if v >= 30:
                cells.append({"city": c, "ind": i, "n": v,
                              "share_in_city_pct": round(v / tot * 100, 2),
                              "share_in_ind_pct": round(v / ind_c[i] * 100, 2)})
    cells.sort(key=lambda x: -x["n"])

    # ---- 7. 区级 top --------------------------------------------------------
    area_top = [{"area": a, "n": v, "pct": round(v / N * 100, 2)}
                for a, v in area_c.most_common(10)]

    # ---- 8. 聚集度 ----------------------------------------------------------
    city_hhi = {c: round(hhi(cc), 4) for c, cc in city_ind.items()}
    ind_hhi = {}
    for i in ind_c:
        cc = collections.Counter()
        for c, d in city_ind.items():
            if d.get(i):
                cc[c] = d[i]
        ind_hhi[i] = round(hhi(cc), 4)

    city_entropy = {c: round(entropy(cc), 3) for c, cc in city_ind.items()}
    type_entropy = {c: round(entropy(cc), 3) for c, cc in city_type.items()}

    top_ind = [{"ind": i, "n": v, "pct": round(v / N * 100, 2),
                "city_hhi": ind_hhi.get(i)}
               for i, v in ind_c.most_common(10)]

    type_rows = []
    for t, v in type_c.most_common():
        d = type_ind[t]
        top3 = d.most_common(3)
        type_rows.append({
            "type": t, "n": v, "pct": round(v / N * 100, 2),
            "ind_hhi": round(hhi(d), 4), "ind_entropy": round(entropy(d), 3),
            "top_ind": [{"ind": k, "n": n, "pct_in_type": round(n / v * 100, 2)} for k, n in top3],
            "city_mix": {c: round(n / v * 100, 2) for c, n in
                         sorted(collections.Counter(r["city"] for r in recs if r["type"] == t).items(),
                                key=lambda x: -x[1]) if n},
        })

    # ---- 9. 服务环节 --------------------------------------------------------
    stage_rows = []
    for st in STAGES:
        c = stage_all.get(st, 0)
        cc = stage_city.get(st, collections.Counter())
        stage_rows.append({
            "stage": st, "stage_cn": STAGE_CN[st], "n": c,
            "pct_of_pool": round(c / N * 100, 2),
            "city_mix": {k: round(v / c * 100, 2) for k, v in cc.most_common() if c},
        })

    reason = ("地理维（省→市→区）、产业维（国民经济行业门类 20 类，覆盖 99.88%）、"
              "服务维（主服务类型 7 类 + 服务环节 6 类）三轴交叉全部在库内实测可算，"
              "格子数、HHI、CR3、香农熵、环节渗透率均已落盘；但「全球」轴实现不了——"
              "池内 44,132 家有省份的机构 100% 是广东省，库内无 country/境外机构字段，"
              "布局只能做到省域内 4 市 26 区，且产业维只到门类不到中类小类，故判部分支持。")
    gap = ("『全球』轴缺失：无境外机构表、无 country 字段，池覆盖仅广东 4 市；"
           "产业维仅门类级（20 类），无中类/小类；服务环节 stage-pilot 全库仅 10 家，"
           "该环节的布局结论不可用（已单列标注）。")

    out = {
        "metric_id": "M_SVC_INDUSTRY_LAYOUT",
        "metric_name": "全球服务机构产业布局",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": reason,
        "main_gap": gap,
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_org_product_info", "field": "main_activities",
             "rows": (f.get("population") or {}).get("product_info_all"),
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_base_info", "field": "ind / area / city / prov",
             "rows": (f.get("population") or {}).get("base_all"),
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
        ],
        "base_years_used": [2026],
        "base_years_missing": [],
        "base_years_note": ("布局是存量截面（工商登记在营状态），不对年度序列做拆分；"
                            "inc_year 只用于结构描述，不作为基期。占比分母统一用池 44,153，"
                            "不用「有该字段的机构数」，避免缺字段处被悄悄抬升。"),
        "population": {"N": N, "city_nonnull": n_city, "area_nonnull": n_area, "ind_nonnull": n_ind,
                       "coverage": {"city_pct": round(n_city / N * 100, 2),
                                    "area_pct": round(n_area / N * 100, 2),
                                    "ind_pct": round(n_ind / N * 100, 2)}},
        "geo": {
            "prov": share(prov_c, N),
            "city": [{"city": c, "n": v, "pct": round(v / N * 100, 2)} for c, v in city_sorted],
            "city_cr3_pct": cr3,
            "city_hhi": round(hhi(city_c), 4),
            "area_top10": area_top,
            "area_count": len(area_c),
        },
        "industry": {"n_categories": len([k for k in ind_c if k != "(空)"]),
                     "pool_ind_hhi": round(hhi(ind_c), 4),
                     "pool_ind_entropy": round(entropy(ind_c), 3),
                     "top10": top_ind,
                     "ind_hhi_by_city_spread": ind_hhi},
        "layout_cells": {"n_cells_ge30": len(cells), "top20": cells[:20]},
        "service_type": type_rows,
        "service_stage": stage_rows,
        "concentration": {"city_hhi_over_ind": city_hhi,
                          "city_ind_entropy": city_entropy,
                          "city_type_entropy": type_entropy},
        "known_limits": [
            "「全球」不可算：prov 非空 44,132 家全为广东省，库内无境外机构/国家字段",
            "产业维仅门类级（20 类），dwd_org_base_info 无中类(div)/小类(group)列",
            "stage-pilot 全库 10 家（占 0.02%），该环节布局统计无解释力",
            "区域口径为工商注册区，不等于实际经营地；跨市分支未并入（subsidiary_edges 目标端多不在池）",
        ],
        "sql_count": 0,
        "elapsed_sec": round(time.time() - t0, 3),
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print("N=%d 城市覆盖 %.2f%% 区 %.2f%% 产业 %.2f%%" %
          (N, out["population"]["coverage"]["city_pct"], out["population"]["coverage"]["area_pct"],
           out["population"]["coverage"]["ind_pct"]))
    print("city:", [(x["city"], x["n"], x["pct"]) for x in out["geo"]["city"]], "CR3", cr3)
    print("ind HHI", out["industry"]["pool_ind_hhi"], "entropy", out["industry"]["pool_ind_entropy"])
    print("top cell", cells[0] if cells else None)
    print("->", OUT)


if __name__ == "__main__":
    main()

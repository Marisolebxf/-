#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""服务机构实体识别构建（M_SVC_GRAPH_112_1）—— gkx 口径，自包含。

口径（旧稿公式照抄，数据源整体换到 gkx）：
    实体域   = gkx.dwd_org_org_product_info 中「经营范围命中服务业态词表」的机构，
               按 org_id 去重；
    类型轴   = 六类候选（INNOV/FINANCE/CONSULT/MKT/HR/IP）+ UNCLASSIFIED；
    属性面   = 名称/类型/地理位置/规模/注册资本/行业门类/人数 七项覆盖率；
    节点标识 = node_id = "SVC-" + sha1(org_id)[:16]（确定性映射，可重算、可去重）。

与旧稿的差异（重要）：
    旧稿的实体识别产物是一张物化表（demo 侧 43,296 行的圈定池 + 43,296 行的图谱挂载表）。
    gkx 没有 `svc_*` 表，本件把「圈定 + 打标 + 发节点号」三步全部重算：
    池由 `dwd_org_org_product_info.main_activities`（45,011 行）按词表判态生成，
    节点号由 org_id 确定性派生（不落库，随时可重算），因此没有「挂载表」这一层物化，
    这一点在 §三 作为缺口写明。

数据源：code/_snapshots21/svc21_facts_20261022.json（gkx 只读快照）
产出：code/M_SVC_GRAPH_112_1_out.json
运行：cd code && python3 M_SVC_GRAPH_112_1.py
"""
from __future__ import annotations

import hashlib
import json
import os
import statistics
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
OUT = os.path.join(HERE, "M_SVC_GRAPH_112_1_out.json")

TYPE_ORDER = ["INNOV", "FINANCE", "CONSULT", "MKT", "HR", "IP", "UNCLASSIFIED"]
TYPE_CN = {"INNOV": "科技创新服务", "FINANCE": "金融服务", "CONSULT": "咨询服务",
           "MKT": "市场营销服务", "HR": "人力资源服务", "IP": "知识产权服务",
           "UNCLASSIFIED": "未分类"}


def node_id(org_id: str) -> str:
    """图谱节点标识：确定性派生，同一 org_id 永远得到同一 node_id（可重算、无库依赖）。"""
    return "SVC-" + hashlib.sha1(org_id.encode("utf-8")).hexdigest()[:16]


def pct(a, b):
    return round(100.0 * a / b, 2) if b else None


def main():
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    pool = f["pool"]
    bf = f.get("base_fields") or {}
    fin = f.get("finance") or {}
    pop = f["population"]
    tags = f.get("tags") or {}
    news = f.get("news") or {}
    recruit_meta = f.get("recruit_meta") or {}
    n = len(pool)

    # ---- 步骤 1：实体域与类型轴 -------------------------------------------------
    type_cnt = Counter(v.get("ptype2") or "UNCLASSIFIED" for v in pool.values())
    type_cnt.pop("", None)
    multi = Counter(len(v.get("types") or []) for v in pool.values())
    stage_cnt = Counter()
    for v in pool.values():
        for s in v.get("stages") or []:
            stage_cnt[s] += 1

    # ---- 步骤 2：主档对齐与去重 -------------------------------------------------
    base = json.load(open(os.path.join(SNAP, "base_20261021.json"), encoding="utf-8"))
    base_ids = {r[0] for r in base}
    aligned = sum(1 for o in pool if o in base_ids)
    names = [v.get("name") or "" for v in pool.values()]
    name_set = {x for x in names if x}
    empty_name = sum(1 for x in names if not x)
    # 全库重名披露（DATA_FACTS §3.5）：底册 189,116 行只有 189,069 个不同 name_cn
    base_names = Counter(r[2] for r in base if r[2])
    dup_groups = sum(1 for c in base_names.values() if c > 1)
    dup_rows = sum(c for c in base_names.values() if c > 1)

    # ---- 步骤 3：属性面覆盖率 ---------------------------------------------------
    def nz(key):
        return sum(1 for o in pool if (bf.get(o) or {}).get(key) not in (None, "", "NULL"))

    emp_ok = 0
    for o in pool:
        rows = fin.get(o) or {}
        if any((r or {}).get("emp") not in (None, 0) for r in rows.values()):
            emp_ok += 1
    attr = {
        "name": {"nonnull": n - empty_name, "rate_pct": pct(n - empty_name, n),
                 "source": "dwd_org_org_product_info.name_cn / dwd_org_base_info.name_cn"},
        "service_type": {"nonnull": n - type_cnt.get("UNCLASSIFIED", 0),
                         "rate_pct": pct(n - type_cnt.get("UNCLASSIFIED", 0), n),
                         "source": "main_activities 词表判态（本件自算）"},
        "geo_city": {"nonnull": nz("city"), "rate_pct": pct(nz("city"), n),
                     "source": "dwd_org_base_info.city"},
        "geo_area": {"nonnull": nz("area"), "rate_pct": pct(nz("area"), n),
                     "source": "dwd_org_base_info.area（区县）"},
        "org_size": {"nonnull": nz("size"), "rate_pct": pct(nz("size"), n),
                     "source": "dwd_org_base_info.org_size"},
        "reg_capital": {"nonnull": nz("cap"), "rate_pct": pct(nz("cap"), n),
                        "source": "dwd_org_base_info.reg_capital"},
        "industry": {"nonnull": nz("ind"), "rate_pct": pct(nz("ind"), n),
                     "source": "dwd_org_base_info.industry_category"},
        "employees": {"nonnull": emp_ok, "rate_pct": pct(emp_ok, n),
                      "source": "dwd_org_annual_financial_info.employees_number"},
    }

    # ---- 步骤 4：节点标识与去重 -------------------------------------------------
    nid = {o: node_id(o) for o in pool}
    uniq_nid = len(set(nid.values()))
    sample_nid = [{"org_id": o, "node_id": nid[o], "name": pool[o]["name"]}
                  for o in list(pool)[:5]]

    # ---- 步骤 5：周边属性（不作识别属性，只作识别后验证材料） ---------------------
    verify = {
        "tech_tag": {"orgs": len([o for o in pool if tags.get(o)]),
                     "rate_pct": pct(len([o for o in pool if tags.get(o)]), n)},
        "news": {"orgs": len([o for o in pool if news.get(o)]),
                 "rate_pct": pct(len([o for o in pool if news.get(o)]), n)},
        "recruit": {"orgs": recruit_meta.get("orgs_with_jobs"),
                    "scope": "HR 子池（type_primary=HR）分块查询口径，非全池"},
    }

    city_cnt = Counter(v.get("city") or "未标注" for v in pool.values())
    size_cnt = Counter((bf.get(o) or {}).get("size") or "未知" for o in pool)
    ind_cnt = Counter((bf.get(o) or {}).get("ind") or "未标注" for o in pool)

    # ---- 支持度机判 --------------------------------------------------------------
    # 五个原文点名属性里，名称/类型/地理/规模四项可用，人数仅 emp_ok 家（见 attr），
    # 且无物化挂载表；按「不许抬档」纪律，落部分支持。
    reason = ("实体域 %d 家（主档对齐 %d，%.2f%%）与七类类型轴、四项主档属性可现转；"
              "但原文点名的「人数」属性仅 %d 家（%.2f%%）有观测——年报人数字段在池内覆盖率过低，"
              "且 gkx 无图谱挂载表（节点号只能确定性派生、无物化），"
              "故落部分支持，不抬到完全转换。"
              % (n, aligned, 100.0 * aligned / n, emp_ok, 100.0 * emp_ok / n))

    out = {
        "metric_id": "M_SVC_GRAPH_112_1",
        "metric_name": "服务机构实体识别构建",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": reason,
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_org_product_info", "rows": pop["product_info_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_base_info", "rows": 189116,
             "snapshot": "code/_snapshots21/base_20261021.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_annual_financial_info", "rows": 90926,
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
        ],
        "base_years_used": [2026],
        "base_years_missing": [],
        "base_years_note": ("实体识别是截面件（以采集时点 2026-10 的池为口径），"
                            "不涉及跨年比较；人数属性取各机构最近一个有值的财务年份，"
                            "未把缺年按 0 摊入。"),
        "population": {
            "base_all": pop["base_all"],
            "product_info_all": pop["product_info_all"],
            "service_any_hit": pop["service_any_hit"],
            "pool_orgs": n,
            "aligned_to_base": aligned,
            "align_rate_pct": pct(aligned, n),
            "pool_distinct_names": len(name_set),
            "base_dup_name_groups": dup_groups,
            "base_dup_name_rows": dup_rows,
        },
        "type_axis": {
            "dist": [{"type": t, "name_cn": TYPE_CN.get(t, t), "orgs": type_cnt.get(t, 0),
                      "share_pct": pct(type_cnt.get(t, 0), n)} for t in TYPE_ORDER],
            "multi_hit_dist": {str(k): v for k, v in sorted(multi.items())},
        },
        "stage_axis": {"dist": {k: v for k, v in stage_cnt.most_common()}},
        "attribute_coverage": attr,
        "nodes": {"assigned": len(nid), "distinct_node_id": uniq_nid,
                  "rule": "node_id = 'SVC-' + sha1(org_id)[:16]（确定性、无物化表）",
                  "sample": sample_nid},
        "verify_channels": verify,
        "city_dist": city_cnt.most_common(8),
        "size_dist": size_cnt.most_common(),
        "industry_dist": ind_cnt.most_common(14),
        "compute": {"elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print("实体域 %d 家；主档对齐 %d（%.2f%%）" % (n, aligned, 100.0 * aligned / n))
    print("类型轴", {t: type_cnt.get(t, 0) for t in TYPE_ORDER})
    print("属性覆盖", {k: v["nonnull"] for k, v in attr.items()})
    print("node_id 去重 =", uniq_nid)
    print("->", OUT)


if __name__ == "__main__":
    main()

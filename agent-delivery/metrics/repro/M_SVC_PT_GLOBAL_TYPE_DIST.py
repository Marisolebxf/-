#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全球服务机构类型分布（M_SVC_PT_GLOBAL_TYPE_DIST）—— gkx 口径，自包含。

两根类型轴：
  主轴（钉版三分类，机构本体）：企业 / 高校 / 科研院所
      来自 svc21_pt_axis_20261022.json 的 org_kind：
        科研院所 = 池内 org_id ∈ gkx.dwd_research_institute_base_info（2,074 行）或用名称精确相等
        高校     = 名称含 大学/学院/高等专科/职业技术学院/学校
        企业     = 其余（三类互斥，合计 = 池）
  辅轴（服务类型六分类，经营范围词表）：INNOV/IP/FINANCE/HR/MKT/CONSULT，一家可多命中

数据源（只读快照，零 SQL）：
    code/_snapshots21/svc21_facts_20261022.json       pool + 六类词表命中
    code/_snapshots21/svc21_pt_axis_20261022.json     org_kind + 科研院所名单

产出：code/M_SVC_PT_GLOBAL_TYPE_DIST_out.json
运行：cd code && python3 M_SVC_PT_GLOBAL_TYPE_DIST.py
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
AXIS = os.path.join(SNAP, "svc21_pt_axis_20261022.json")
OUT = os.path.join(HERE, "M_SVC_PT_GLOBAL_TYPE_DIST_out.json")

ORDER = ["企业", "高校", "科研院所"]
TYPE_NAME = {"INNOV": "创新/技术服务", "IP": "知识产权服务", "FINANCE": "金融服务",
             "HR": "人力资源服务", "MKT": "市场营销服务", "CONSULT": "咨询服务"}


def main():
    t0 = time.time()
    fact = json.load(open(FACTS, encoding="utf-8"))
    ax = json.load(open(AXIS, encoding="utf-8"))
    pool = fact["pool"]
    kind = ax["org_kind"]
    n = len(pool)

    # ---------------- 主轴：机构本体三分类
    cnt = Counter(kind.get(o, "企业") for o in pool)
    rows = []
    for k in ORDER:
        rows.append({"org_kind": k, "org_count": cnt.get(k, 0),
                     "share_of_pool": round(cnt.get(k, 0) / n, 6)})

    samples = {}
    for k in ("高校", "科研院所"):
        ids = [o for o in pool if kind.get(o) == k]
        samples[k] = [{"name": pool[o]["name"], "city": pool[o].get("city", "")} for o in ids[:8]]

    # ---------------- 辅轴：六类服务词表（多命中 + 主类）
    multi = Counter()
    for v in pool.values():
        for t in v.get("types") or []:
            multi[t] += 1
    primary = Counter(v.get("ptype") for v in pool.values())
    svc_rows = []
    for t in ["INNOV", "IP", "FINANCE", "HR", "MKT", "CONSULT"]:
        svc_rows.append({"type": t, "type_name": TYPE_NAME[t],
                         "multi_hit": multi.get(t, 0),
                         "primary": primary.get(t, 0),
                         "share_multi": round(multi.get(t, 0) / n, 6)})

    sz_kind = Counter(kind.get(o, "企业") for o, v in pool.items() if v.get("city") == "深圳市")

    out = {
        "metric_id": "M_SVC_PT_GLOBAL_TYPE_DIST",
        "metric_name": "全球服务机构类型分布",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": (
            "机构本体三分类在 gkx 可实算且闭合（企业 44,095＋高校 37＋科研院所 21＝44,153），"
            "六类服务词表亦可现转；但「全球」轴的境外机构在 gkx 无源"
            "（dwd_forg_base_info 仅 GB/US/CA 三值且非服务名录），类型分布在境外面不可得 → 部分支持"),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_org_product_info(main_activities 词表分类)",
             "rows": fact["population"]["product_info_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_research_institute_base_info", "rows": ax["research"]["rows_total"],
             "snapshot": "code/_snapshots21/svc21_pt_axis_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_base_info（名称，用于高校判定）",
             "rows": fact["population"]["base_all"],
             "snapshot": "code/_snapshots21/base_20261021.json"},
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面指标：类型分布是当前时点存量的横截面，不含年度分母；"
                            "池内成立年序列由 M_SVC_PT_GLOBAL_TOTAL 承担，本件不重复计入。"),
        "population": {
            "distinct_org_id": n,
            "join_base_rows": fact["population"]["product_info_join_base"],
            "join_base_rate": round(fact["population"]["product_info_join_base"] / n, 6),
        },
        "kind_axis": {
            "order": ORDER,
            "rows": rows,
            "sum": sum(r["org_count"] for r in rows),
            "sum_equals_pool": sum(r["org_count"] for r in rows) == n,
            "rule": ax["org_kind_meta"]["rule"],
            "research_source_rows": ax["research"]["rows_total"],
            "research_matched": len(ax["research"]["matched"]),
            "samples": samples,
            "shenzhen": [{"org_kind": k, "org_count": sz_kind.get(k, 0)} for k in ORDER],
        },
        "service_axis": {
            "rows": svc_rows,
            "multi_hit_sum": sum(r["multi_hit"] for r in svc_rows),
            "classified_orgs": n - primary.get("UNCLASSIFIED", 0),
            "innov_absorbed": multi.get("INNOV", 0) - primary.get("INNOV", 0),
            "multiplicity": dict(sorted(Counter(len(v.get("types") or []) for v in pool.values()).items())),
            "unclassified_primary": primary.get("UNCLASSIFIED", 0),
            "note": ("六类是经营范围词表代理，一家机构可命中多类；主类按 "
                     "IP > FINANCE > HR > MKT > CONSULT > INNOV 归并（专精类优先、泛化类兜底，"
                     "故 INNOV 主类只剩未命中其余五类者；ptype_rule 见快照）。"),
        },
        "difference_vs_old_draft": {
            "population": "旧稿 43,296（演示库圈定池，企业侧为主）→ 本件 44,153（gkx 经营范围实体）",
            "kind_dist": "旧稿 企业 43,296 / 高校 0 / 科研院所 0 → 本件 企业 44,095 / 高校 37 / 科研院所 21",
            "reason": ("旧稿两桶为 0 是「池由企业底册构成」的口径性结论；换源后池来自经营范围，"
                       "gkx 另有 dwd_research_institute_base_info（2,074 行，池内命中 21）与名称含"
                       "「大学/学院」的 37 家，两桶由 0 变为可实测的非零小类"),
        },
        "compute": {"status": "ok", "elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("kind", [(r["org_kind"], r["org_count"]) for r in rows], "sum", sum(r["org_count"] for r in rows))
    print("svc", [(r["type"], r["multi_hit"], r["primary"]) for r in svc_rows])
    print("->", OUT)


if __name__ == "__main__":
    main()

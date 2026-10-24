#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全球服务机构规模分布（M_SVC_PT_GLOBAL_SCALE_DIST）—— gkx 口径，自包含。

两条度量链（沿用 calc-logic 0.2.0「员工数优先 / 注册资本兜底」的设计）：
  主链  员工数：gkx.dwd_org_annual_financial_info.employees_number
        按机构取「最近一个有值年」的人数值，按 <50 / [50,200) / [200,500) / ≥500 分桶
  兜底链 注册资本：gkx.dwd_org_base_info.registered_capital_value（**单位：元**）+ capital_currency
        先按币种分：非人民币 → foreign；人民币单币种再按万元阈值分桶（<50/50–200/200–500/≥500 万元）
        币种为空或金额为空 → unknown

口径要点：
  - 员工数主链在池内只有 1,582 家（3.58%）有值 → 不足以承担主链，正式结果走兜底链，正文披露；
  - 注册资本原值以「元」存储（中位 12,000,000 元 = 1,200 万元），阈值必须先 /10000 折算，
    否则会出现「≥500 万桶占 99.9%」的假分布（旧稿演示库即此形态，已在 §四 对照说明）；
  - 六桶合计必须等于池 44,153（foreign/unknown 单列，不外推、不丢弃）。

数据源（只读快照，零 SQL）：
    code/_snapshots21/svc21_facts_20261022.json      base_fields(cap) + finance(employees)
    code/_snapshots21/svc21_pt_axis_20261022.json    base_extra(capital_currency)

产出：code/M_SVC_PT_GLOBAL_SCALE_DIST_out.json
运行：cd code && python3 M_SVC_PT_GLOBAL_SCALE_DIST.py
"""
from __future__ import annotations

import json
import os
import statistics
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
AXIS = os.path.join(SNAP, "svc21_pt_axis_20261022.json")
OUT = os.path.join(HERE, "M_SVC_PT_GLOBAL_SCALE_DIST_out.json")

BUCKETS = ["lt50", "50to200", "200to500", "ge500", "foreign", "unknown"]
LABEL = {"lt50": "<50 万元", "50to200": "[50,200) 万元", "200to500": "[200,500) 万元",
         "ge500": "≥500 万元", "foreign": "外币注册", "unknown": "币种/金额缺失"}


def emp_bucket(e):
    if e is None:
        return None
    e = float(e)
    if e < 50:
        return "lt50"
    if e < 200:
        return "50to200"
    if e < 500:
        return "200to500"
    return "ge500"


def cap_bucket(cap, ccy):
    """cap 单位：元。返回六桶之一。"""
    if not ccy:
        return "unknown"
    if ccy != "人民币":
        return "foreign"
    if cap is None:
        return "unknown"
    wan = float(cap) / 10000.0
    if wan <= 0:
        return "unknown"
    if wan < 50:
        return "lt50"
    if wan < 200:
        return "50to200"
    if wan < 500:
        return "200to500"
    return "ge500"


def latest_fin(rec):
    """取最近一个有值年的人数值（不补 0；缺值年跳过）。"""
    ys = [y for y in rec if y.isdigit()]
    for y in sorted(ys, reverse=True):
        e = rec[y].get("emp")
        if e not in (None, 0):
            return y, e
    return None, None


def main():
    t0 = time.time()
    fact = json.load(open(FACTS, encoding="utf-8"))
    ax = json.load(open(AXIS, encoding="utf-8"))
    pool, bf, fin = fact["pool"], fact["base_fields"], fact["finance"]
    extra = ax["base_extra"]
    n = len(pool)

    # ---------------- 主链：员工数
    emp = {}
    for o, rec in fin.items():
        if o not in pool:
            continue
        y, e = latest_fin(rec)
        if e is not None:
            emp[o] = (y, e)
    emp_cnt = Counter(emp_bucket(e) for _y, e in emp.values())

    # ---------------- 兜底链：注册资本 + 币种
    cap_cnt = Counter()
    ccy_cnt = Counter()
    cap_vals = []
    for o in pool:
        b = bf.get(o) or {}
        ex = extra.get(o) or ["", ""]
        cap, ccy = b.get("cap"), ex[1]
        ccy_cnt[ccy or "（空）"] += 1
        if cap:
            cap_vals.append(float(cap))
        cap_cnt[cap_bucket(cap, ccy)] += 1

    rows = []
    for k in BUCKETS:
        rows.append({"bucket": k, "label": LABEL[k], "org_count": cap_cnt.get(k, 0),
                     "share_of_pool": round(cap_cnt.get(k, 0) / n, 6)})
    total_cap = sum(r["org_count"] for r in rows)

    # ---------------- 官方规模档（平行视角，来自底册 org_size）
    size_cnt = Counter((bf.get(o) or {}).get("size") or "未知" for o in pool)

    # ---------------- 深圳切片
    sz_rows = []
    for k in BUCKETS:
        c = sum(1 for o, v in pool.items()
                if v.get("city") == "深圳市"
                and cap_bucket((bf.get(o) or {}).get("cap"), (extra.get(o) or ["", ""])[1]) == k)
        sz_rows.append({"bucket": k, "org_count": c})

    out = {
        "metric_id": "M_SVC_PT_GLOBAL_SCALE_DIST",
        "metric_name": "全球服务机构规模分布",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": (
            "注册资本兜底链覆盖 99.84%（44,032/44,153 入桶，含 foreign/unknown 单列），"
            "六桶合计与池全对账；但员工数主链只有 1,582 家（3.58%）有值，规模刻画的"
            "第一指标不可用，且「全球」轴境外机构无源 → 部分支持"),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_base_info(registered_capital_value, capital_currency, org_size)",
             "rows": fact["population"]["base_all"],
             "snapshot": "code/_snapshots21/svc21_pt_axis_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_annual_financial_info(employees_number)",
             "rows": fact["finance_meta"]["rows_total"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_org_product_info（池驱动）",
             "rows": fact["population"]["product_info_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面指标：规模分布取「最近一个有值年」的员工数/当前注册资本，"
                            "不做跨年比较；年报年份在产物 latest_emp_year_dist 中披露，"
                            "缺失年不补 0、不参与分母。"),
        "population": {
            "distinct_org_id": n,
            "capital_nonnull": sum(1 for o in pool if (bf.get(o) or {}).get("cap")),
            "capital_coverage": round(sum(1 for o in pool if (bf.get(o) or {}).get("cap")) / n, 6),
            "currency_dist": [[k, v] for k, v in ccy_cnt.most_common()],
        },
        "bucket_rows": rows,
        "bucket_sum": total_cap,
        "bucket_sum_equals_pool": total_cap == n,
        "capital_unit": {
            "raw_unit": "元",
            "threshold_unit": "万元",
            "conversion": "raw / 10000",
            "median_raw": statistics.median(cap_vals) if cap_vals else None,
            "median_wan": round(statistics.median(cap_vals) / 10000.0, 2) if cap_vals else None,
        },
        "employee_chain": {
            "orgs_with_value": len(emp),
            "coverage": round(len(emp) / n, 6),
            "bucket_rows": [{"bucket": k, "org_count": emp_cnt.get(k, 0)}
                            for k in BUCKETS[:4]],
            "latest_emp_year_dist": [[y, c] for y, c in
                                     Counter(y for y, _e in emp.values()).most_common(8)],
            "note": ("员工数只在年报表有值，池内 1,582 家；按最近有值年取数，"
                     "不同机构的「最近年」不同，故只用于分桶画像，不做年度比较。"),
        },
        "org_size_axis": {
            "rows": [[k, c] for k, c in size_cnt.most_common()],
            "sum": sum(size_cnt.values()),
            "note": "底册 org_size 为官方划型档（大/中/小/微/未知），与资本六桶并行披露，不互相替代。",
        },
        "shenzhen_slice": {"orgs": sum(r["org_count"] for r in sz_rows), "rows": sz_rows},
        "difference_vs_old_draft": {
            "population": "旧稿 43,296（演示库圈定池）→ 本件 44,153（gkx 经营范围实体）",
            "bucket_dist": ("旧稿 ge500 桶 98.9%（演示库资本普遍取百万级）→ 本件 ge500 桶 {n} 家（{p}），"
                            "分布重新成形").format(n=cap_cnt.get("ge500", 0),
                                                   p="%.1f%%" % (100.0 * cap_cnt.get("ge500", 0) / n)),
            "unit_trap": ("旧稿按「万元」阈值直接比原值；gkx 原值以「元」存储，"
                          "不折算会把 99.9% 的机构塞进 ≥500 万桶"),
            "employee_chain": "旧稿 167 家（0.39%，卡面字段）→ 本件 1,582 家（3.58%，年报字段）",
        },
        "compute": {"status": "ok", "elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("cap", [(r["bucket"], r["org_count"]) for r in rows], "sum", total_cap)
    print("emp coverage", len(emp), "size", size_cnt.most_common(3))
    print("->", OUT)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""人力资源服务机构技术力评价模型（M_SVC_DEEP_176_1）—— gkx 口径，自包含。

三维（需规 §1.1.1.1.1.1.1.9.5）：
    人才资源   —— 从业人数（dwd_org_annual_financial_info.employees_number 最近一年）
                  + 招聘岗位数（dwd_org_recruit_info 按 HR 子池聚合，见 recruit_cover）
    服务标准化 —— 资质/荣誉标签数代理（dwd_org_tech_tag），正式流程规范分待建
    客户满意度 —— 无评价类承载表（待建 svc_csat_score）→ 无源

引才活跃度用资讯条数作旁证（不进三维）。

数据源：code/_snapshots21/svc21_facts_20261022.json（gkx 只读快照）
产出：code/M_SVC_DEEP_176_1_out.json
运行：cd code && python3 M_SVC_DEEP_176_1.py
"""
from __future__ import annotations

import json
import os
import statistics
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
OUT = os.path.join(HERE, "M_SVC_DEEP_176_1_out.json")


def mm(vals: dict) -> dict:
    """min-max（内联复制自 M_SVC_DEEP_174_1.py，不 import 共享模块）"""
    xs = [v for v in vals.values() if v is not None]
    if not xs:
        return {}
    lo, hi = min(xs), max(xs)
    if hi - lo <= 1e-12:
        return {k: 0.5 for k in vals if vals[k] is not None}
    return {k: (v - lo) / (hi - lo) for k, v in vals.items() if v is not None}


def latest_emp(fin: dict):
    for y in sorted(fin, reverse=True):
        row = fin[y] or {}
        if row.get("emp") is not None:
            return int(y), float(row["emp"])
    return None, None


def main():
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    pool, fin, tags, news = f["pool"], f["finance"], f["tags"], f["news"]
    hr_pool = [o for o, v in pool.items() if v.get("ptype2") == "HR"]
    n = len(hr_pool)

    emp, years = {}, {}
    for o in hr_pool:
        y, v = latest_emp(fin.get(o) or {})
        if v:
            emp[o] = v
            years[y] = years.get(y, 0) + 1
    rec = f.get("recruit_hr") or {}
    jobs = {o: int(rec[o]) for o in hr_pool if o in rec}
    tagc = {o: int(tags.get(o, 0)) for o in hr_pool}
    newsc = {o: int(news.get(o, 0)) for o in hr_pool}

    # 人才资源 = 从业人数 + 招聘岗位数（两子项先各自 min-max，再对非空子项等权）
    emp_n = mm({o: v for o, v in emp.items() if v > 0})
    job_n = mm({o: v for o, v in jobs.items() if v > 0})
    s_talent = {}
    for o in hr_pool:
        parts = [x for x in (emp_n.get(o), job_n.get(o)) if x is not None]
        if parts:
            s_talent[o] = sum(parts) / len(parts)
    s_std = mm({o: v for o, v in tagc.items() if v > 0})

    dims = {"人才资源": s_talent, "服务标准化": s_std, "客户满意度": {}}
    w = {"人才资源": 1 / 3, "服务标准化": 1 / 3, "客户满意度": 1 / 3}
    idx, used = {}, {}
    for o in hr_pool:
        av = [(k, dims[k][o]) for k in dims if o in dims[k]]
        if len(av) < 2:
            continue
        ws = sum(w[k] for k, _ in av)
        idx[o] = 100.0 * sum(w[k] * v for k, v in av) / ws
        used[o] = [k for k, _ in av]

    vals = sorted(idx.values())
    ranked = sorted(idx.items(), key=lambda x: -x[1])
    top = [{"org_id": o, "name": pool[o]["name"], "city": pool[o]["city"], "index": round(v, 2),
            "employees": emp.get(o), "jobs": jobs.get(o), "tags": tagc[o],
            "news": newsc[o], "dims": used[o]}
           for o, v in ranked[:10]]
    band = {"强(>=70)": 0, "中(50-70)": 0, "弱(<50)": 0}
    for v in vals:
        band["强(>=70)" if v >= 70 else ("中(50-70)" if v >= 50 else "弱(<50)")] += 1

    out = {
        "metric_id": "M_SVC_DEEP_176_1",
        "metric_name": "人力资源服务机构技术力评价模型",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": ("三维中人才资源（从业人数）与服务标准化（资质标签代理）可现转，"
                            "客户满意度维无任何评价类承载表、招聘侧数据未并入快照 → 部分支持"),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_annual_financial_info(employees_number)", "rows": f["finance_meta"]["rows_total"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318", "table": "gkx.dwd_org_tech_tag",
             "rows": 202424, "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318", "table": "gkx.dwd_org_recruit_info",
             "rows": 7981643, "snapshot": "code/_snapshots21/svc21_facts_20261022.json(recruit_hr)"},
        ],
        "base_years_used": list(range(2007, 2026)),
        "base_years_missing": [2026],
        "base_years_note": ("财务表覆盖 2007—2025，used 记整段；从业人数取每机构最近一个有值年份，"
                            "不按缺失年补 0；2026 无行，missing 记 2026。招聘侧只有岗位数、无年度序列，故不做同比"),
        "population": {"orgs_hr_primary": n, "share_of_pool": round(n / len(pool), 6)},
        "dimensions": {k: {"n": len(v), "share_of_pool": round(len(v) / n, 6)} for k, v in dims.items()},
        "index": {"n": len(idx), "mean": round(statistics.mean(vals), 2) if vals else None,
                  "median": round(statistics.median(vals), 2) if vals else None,
                  "max": round(vals[-1], 2) if vals else None},
        "bands": band,
        "top10": top,
        "gaps": {
            "csat": "客户满意度：gkx 无评分/评价/投诉闭环表（待建 svc_csat_score）",
            "recruit": ("招聘侧：dwd_org_recruit_info 已按 HR 子池聚合岗位数（%d 家覆盖），"
                        "但 hiring_number 未参与聚合，故岗位人数无法求和；"
                        "全池口径（非 HR 子池）未扫" % len(jobs)),
            "std": "服务标准化：无流程规范/认证表，仅资质类标签计数代理",
        },
        "emp_year_dist": {str(k): v for k, v in sorted(years.items(), reverse=True)[:6]},
        "recruit_cover": {"orgs_with_jobs": len(jobs), "jobs_total": sum(jobs.values()),
                          "share_of_pool": round(len(jobs) / n, 6) if n else None,
                          "source": "gkx.dwd_org_recruit_info 按 HR 子池 GROUP BY org_id COUNT(*)"},
        "compute": {"elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("HR 池", n, "人数非空", len(emp), "标签非空", len([o for o in hr_pool if tagc[o]]),
          "资讯非空", len([o for o in hr_pool if newsc[o]]), "指数", len(idx))
    print("均/中位", out["index"]["mean"], out["index"]["median"], band)
    print("top", [(t["name"], t["index"], t["employees"]) for t in top[:3]])
    print("->", OUT)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""专家H指数排行（M_INNOV_EXPERT_HINDEX）——A-16 批实现。

口径（registry/cfg_metric-INNOV-seed.yaml）：
  「柱/雷达展示专家 H 指数排行；可按学科/机构/地域筛选。对象=专家，不是 RANK 科技成果榜。
    实现类 third_party，禁止伪展开 Hirsch 公式。」
  → 本脚本**不自算 H 指数**，直接读 `gkx.dwd_scholar.h_index`（外采只读字段）；
    只做排行、分档、机构聚合，不重造 Hirsch 公式。

三个附属维的实测结论（决定了判档）：
  学科：`dwd_scholar_research_direction.fields` 是英文关键词串（不是学科分类体系），
        只能做关键词粗筛，不能当中文学科维度；
  机构：`dwd_scholar.scholar_org_name_zh` 覆盖 97.66%，可用；
  地域：`scholar_org_id` 全表 0 个非空，机构名与底册名称的交集只有 1,057/20,829 = 5.07%，
        且交集全部落在广东高校——地域筛选不是「不全」，而是「系统性偏向深圳都市圈」。

产物：code/M_INNOV_EXPERT_HINDEX_out.json
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import _gkxdb
from _innov_gkx21_common import load_cache, pct, write_out

METRIC = "M_INNOV_EXPERT_HINDEX"


def q(sql):
    cur = _gkxdb.gkx()
    try:
        cur.execute("SET SESSION max_execution_time=120000")
        cur.execute(sql)
        return cur.fetchall()
    finally:
        cur.close()


def load_scholars():
    """拉全量学者（21,316 行，小表）。方向与院士标记用字典本地 join，避免 JOIN 排序压力。"""
    rows = q(
        "SELECT scholar_id, name_zh, name_en, scholar_org_name_zh, h_index, paper_nums, "
        "citation_nums, reference_nums, status FROM gkx.dwd_scholar"
    )
    scholars = []
    for r in rows:
        sid, zh, en, org, h, pn, cn, rn, st = r
        scholars.append({
            "scholar_id": sid,
            "name": (zh or en or "").strip(),
            "name_en": (en or "").strip(),
            "org": (org or "").strip(),
            "h": int(h) if h is not None else None,
            "papers": int(pn) if pn is not None else None,
            "citations": int(cn) if cn is not None else None,
            "refs": int(rn) if rn is not None else None,
            "status": int(st) if st is not None else None,
        })

    dirs = q("SELECT scholar_id, fields FROM gkx.dwd_scholar_research_direction")
    dmap = {}
    for sid, fields in dirs:
        kws = [x.strip() for x in (fields or "").split(";") if x.strip()]
        if kws:
            dmap[sid] = kws
    flags = q("SELECT scholar_id, academician FROM gkx.dwd_scholar_talent_flag")
    amap = {}
    for sid, ac in flags:
        try:
            amap[sid] = int(ac or 0)
        except (TypeError, ValueError):
            amap[sid] = 0
    for s in scholars:
        s["keywords"] = dmap.get(s["scholar_id"], [])
        s["academician"] = amap.get(s["scholar_id"], 0)
    return scholars


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx == 0 or syy == 0:
        return None
    return round(sxy / (sxx * syy) ** 0.5, 4)


def main():
    scholars = load_scholars()
    scored = [s for s in scholars if s["h"] is not None]
    scored.sort(key=lambda s: (-s["h"], -(s["citations"] or 0), s["name"]))
    hs = [s["h"] for s in scored]

    # ---------- 完整性自检：h-index 不能超过发文量 ----------
    viol = [s for s in scored if s["papers"] is not None and s["h"] > s["papers"]]
    papers_known = [s for s in scored if s["papers"]]
    r_h_cit = pearson([s["h"] for s in scored if s["citations"] is not None],
                      [s["citations"] for s in scored if s["citations"] is not None])
    r_h_pap = pearson([s["h"] for s in papers_known], [s["papers"] for s in papers_known])

    buckets = [("0", 0, 0), ("1-4", 1, 4), ("5-9", 5, 9), ("10-19", 10, 19),
               ("20-49", 20, 49), ("50-99", 50, 99), ("100+", 100, 10 ** 9)]
    bucket_rows = []
    for label, lo, hi in buckets:
        n = sum(1 for h in hs if lo <= h <= hi)
        bucket_rows.append({"bucket": label, "n": n,
                            "share": round(n / len(hs), 4) if hs else None})

    # ---------- 机构维：学者数 ≥10 的机构 ----------
    by_org = {}
    for s in scored:
        if not s["org"]:
            continue
        by_org.setdefault(s["org"], []).append(s)
    org_rows = []
    for org, arr in by_org.items():
        oh = [x["h"] for x in arr]
        org_rows.append({
            "org": org,
            "n_scholars": len(arr),
            "avg_h": round(statistics.mean(oh), 3),
            "median_h": statistics.median(oh),
            "max_h": max(oh),
            "top_scholar": max(arr, key=lambda x: (x["h"], x["citations"] or 0))["name"],
        })
    big_orgs = sorted([o for o in org_rows if o["n_scholars"] >= 10],
                      key=lambda o: (-o["avg_h"], -o["n_scholars"]))
    count_orgs = sorted(org_rows, key=lambda o: -o["n_scholars"])[:20]

    # ---------- 学科维：关键词频次（不是学科分类） ----------
    kw_stats = {}
    for s in scored:
        for kw in s["keywords"]:
            kw_stats.setdefault(kw, []).append(s["h"])
    kw_rows = [{"keyword": k, "n": len(v),
                "avg_h": round(statistics.mean(v), 3),
                "max_h": max(v)}
               for k, v in kw_stats.items() if len(v) >= 30]
    kw_rows.sort(key=lambda x: -x["n"])
    n_with_kw = sum(1 for s in scored if s["keywords"])

    # ---------- 地域维：用底册名称→城市映射，如实披露命中率 ----------
    citymap = (load_cache("org_name_city_20261021.json") or {}).get("map", {})
    city_hit = {}
    matched_scholars = 0
    for s in scored:
        c = citymap.get(s["org"])
        if c:
            matched_scholars += 1
            city_hit.setdefault(c, []).append(s["h"])
    city_rows = [{"city": c, "n_scholars": len(v),
                  "avg_h": round(statistics.mean(v), 3),
                  "max_h": max(v)}
                 for c, v in sorted(city_hit.items(), key=lambda kv: -len(kv[1]))][:12]

    acad = [s for s in scored if s.get("academician") == 1]
    non_acad = [s for s in scored if s.get("academician") != 1]

    # ---------- 关键字段的主外键可连性（决定学科/院士维能不能用） ----------
    link = {
        "direction_join_scholar_id": int(q(
            "SELECT COUNT(*) FROM gkx.dwd_scholar_research_direction d "
            "JOIN gkx.dwd_scholar s ON s.scholar_id=d.scholar_id")[0][0]),
        "direction_join_id": int(q(
            "SELECT COUNT(*) FROM gkx.dwd_scholar_research_direction d "
            "JOIN gkx.dwd_scholar s ON s.id=d.scholar_id")[0][0]),
        "talent_flag_join_scholar_id": int(q(
            "SELECT COUNT(*) FROM gkx.dwd_scholar_talent_flag d "
            "JOIN gkx.dwd_scholar s ON s.scholar_id=d.scholar_id")[0][0]),
        "talent_flag_join_id": int(q(
            "SELECT COUNT(*) FROM gkx.dwd_scholar_talent_flag d "
            "JOIN gkx.dwd_scholar s ON s.id=d.scholar_id")[0][0]),
        "direction_rows": int(q(
            "SELECT COUNT(*) FROM gkx.dwd_scholar_research_direction")[0][0]),
        "talent_flag_rows": int(q(
            "SELECT COUNT(*) FROM gkx.dwd_scholar_talent_flag")[0][0]),
    }
    link["direction_join_rate"] = round(link["direction_join_scholar_id"] / link["direction_rows"], 4)
    link["talent_flag_join_rate"] = round(link["talent_flag_join_scholar_id"] / link["talent_flag_rows"], 4)
    link["note"] = ("dwd_scholar.scholar_id 与 dwd_scholar_research_direction / "
                    "dwd_scholar_talent_flag 的 scholar_id 不是同一套编码："
                    "按 scholar_id 只能连上约 9%，改按 dwd_scholar.id 更差；两表无法整表对齐。")

    payload = {
        "metric_id": METRIC,
        "metric_name": "专家H指数排行",

        # 基期披露（派单书铁律 5）：h 指数与发文量为库内累计值（学者全生涯截面），
        # 不按年度切分，故无基期分母。
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("h_index / paper_nums / citation_nums 均为库内累计值（学者全生涯截面），"
                            "不按年度切分，因此不构造基期；也无缺失年份可被摊入分母。"),
        "data_support_level": "部分支持",
        "run_at": "2026-10-22",
        "db": "gkx@183.240.141.251:3318",
        "tables": ["gkx.dwd_scholar", "gkx.dwd_scholar_research_direction",
                   "gkx.dwd_scholar_talent_flag"],
        "n_scholars_total": len(scholars),
        "n_scholars_scored": len(scored),
        "h_source": "gkx.dwd_scholar.h_index（外采只读字段，本脚本不重算 Hirsch 公式）",
        "h_stats": {
            "min": min(hs), "max": max(hs),
            "mean": round(statistics.mean(hs), 3),
            "median": statistics.median(hs),
            "p90": pct(hs, 0.90), "p95": pct(hs, 0.95), "p99": pct(hs, 0.99),
            "n_positive": sum(1 for h in hs if h > 0),
        },
        "h_buckets": bucket_rows,
        "integrity": {
            "h_gt_papers_rows": len(viol),
            "h_gt_papers_rate": round(len(viol) / len(scored), 4),
            "h_gt_papers_examples": [{"name": s["name"], "h": s["h"], "papers": s["papers"]}
                                     for s in viol[:5]],
            "pearson_h_citations": r_h_cit,
            "pearson_h_papers": r_h_pap,
            "note": "h_index 由外采方给出，本脚本不重算；但 h > 发文量的行在 Hirsch 定义下不可能，"
                    "属字段一致性缺陷，排行前列项须逐条复核。",
        },
        "key_linkage": link,
        "top50": [{"rank": i + 1, "name": s["name"], "name_en": s["name_en"],
                   "org": s["org"], "h": s["h"], "papers": s["papers"],
                   "citations": s["citations"], "academician": s["academician"],
                   "primary_keyword": (s["keywords"][0] if s["keywords"] else "")}
                  for i, s in enumerate(scored[:50])],
        "org_dim": {
            "n_orgs": len(org_rows),
            "n_orgs_ge10": len(big_orgs),
            "top_by_avg_h": big_orgs[:20],
            "top_by_size": count_orgs,
        },
        "discipline_dim": {
            "n_with_keywords": n_with_kw,
            "coverage": round(n_with_kw / len(scored), 4),
            "n_keywords_total": len(kw_stats),
            "top_keywords": kw_rows[:20],
            "note": "fields 为英文研究兴趣关键词，一篇多值（分号分隔），不是学科分类体系；"
                    "同一学者可命中多个关键词，故各关键词人数不可加总。",
        },
        "region_dim": {
            "n_matched": matched_scholars,
            "coverage": round(matched_scholars / len(scored), 4),
            "cities": city_rows,
            "note": "按机构名匹配底册名称→城市映射（189,068 个企业名称）。学者所在高校绝大多数不在企业底册，"
                    "命中者集中在广东高校，故本表只能作样本描述，不能作城市排名。",
        },
        "academician_dim": {
            "n_academician": len(acad),
            "joinable_rows": link["talent_flag_join_scholar_id"],
            "flag_table_academicians": 112,
            "avg_h_academician": round(statistics.mean([s["h"] for s in acad]), 3) if acad else None,
            "avg_h_other": round(statistics.mean([s["h"] for s in non_acad]), 3) if non_acad else None,
            "max_h_academician": max([s["h"] for s in acad]) if acad else None,
            "note": "院士标记表 20,030 行里 academician=1 共 112 行，但只有 1,858 行能与学者表连上，"
                    "故本维只能在 8.7% 的子集上描述，不能当全量院士口径。",
        },
        "gaps": [
            "地域维不可用：scholar_org_id 全表 0 个非空；按机构名匹配底册仅 4.97%，且集中广东。",
            "学科维不可用：fields 是英文研究兴趣关键词（非学科分类），且 scholar_id 编码对不上，只有 8.69% 能连。",
            "H 指数为外采字段，无法在库内复算；且有 719 行（3.37%）h > 发文量，违反 Hirsch 定义。",
            "dwd_scholar 是截面表，没有历史快照，无法做 H 指数的时间趋势或同比。",
        ],
    }
    write_out(METRIC, payload)
    print(json.dumps({k: payload[k] for k in ("n_scholars_scored", "h_stats", "integrity")},
                     ensure_ascii=False, indent=1))
    print("buckets:", [(b["bucket"], b["n"]) for b in bucket_rows])
    print("region coverage:", payload["region_dim"]["coverage"],
          "discipline coverage:", payload["discipline_dim"]["coverage"])


if __name__ == "__main__":
    main()

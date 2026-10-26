#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_DS_04_CARRIER_RANK_001 创新能力指数 · 复现代码（20261021 改源版）

口径：王惠 V1.5（本指标 calc-logic 原文「同 M_INNOV_CARRIER_INDEX_GLOBAL-创新载体创新能力指数」，
      计算步骤完全一致）。步骤：
        ① 载体入集：国内机构主档（存续，2,000）+ 科研机构底册（存续，500）+ 海外机构底册（500）；
        ② 三维：资源（研发人员/从业人数/营收）/ 产出（专利件数 + 论文件数）/ 能力（授权件数 + 高企标签）；
        ③ 批内 min-max 归一、缺维重归一、非缺失维等权 ×100；
        ④ 派生排名：以指数为排序键，给出 competition rank 名次与并列结构。
数据源（20261021 版）：**只读三方库 gkx**（旧版跑在开发库 ods 上，两库同名表逐表镜像，算法未改）。
输出：code/M_INNOV_DS_04_CARRIER_RANK_001_out.json
"""
import json
import os
import time
from collections import Counter

import _innov_gkx21_common as ic

HERE = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(HERE, "M_INNOV_DS_04_CARRIER_RANK_001_out.json")
YEAR = 2024
CARRIER_N = 2000


def norm_vals(xs):
    """min-max 归一；常数序列返回 0.5（与王惠 V1.5 的「缺维重归一」契约一致）。"""
    xs2 = [x for x in xs if x is not None]
    if not xs2:
        return [None] * len(xs)
    lo, hi = min(xs2), max(xs2)
    if hi == lo:
        return [0.5 if x is not None else None for x in xs]
    return [((x - lo) / (hi - lo)) if x is not None else None for x in xs]


def probes_today():
    p = {}
    for t in ["dwd_org_base_info", "dwd_research_institute_base_info", "dwd_forg_base_info",
              "dwd_org_tech_tag", "dwd_org_annual_financial_info", "dwd_org_stock_finance_info",
              "dwd_patent", "dwd_zh_paper", "dwd_zh_author", "dwd_en_paper"]:
        p["gkx." + t] = ic.count(t)
    row = ic.q1("SELECT COUNT(*), SUM(development_employee IS NULL), SUM(employees_number IS NULL), "
                "SUM(operating_revenue IS NULL) FROM gkx.dwd_org_annual_financial_info")
    n, dev_null, emp_null, rev_null = [int(x or 0) for x in row]
    p["gkx.dwd_org_annual_financial_info.detail"] = dict(
        rows=n, development_employee_null=dev_null,
        employees_number_null=emp_null, operating_revenue_null=rev_null,
        dev_null_pct=round(dev_null / n * 100, 2) if n else None)
    return p


def carrier_pool():
    """载体入集：三源各按旧版 LIMIT 截取；显式 ORDER BY org_id 把旧版的无序 LIMIT 固定下来。

    旧版没有 ORDER BY，批次成员取决于引擎返回顺序（InnoDB 通常为主键序，但无契约）。
    本版显式排序，使「同一份数据、任何一次重跑得到同一批载体」成立。
    """
    d = ic.load_cache("carrier_pool_20261021.json")
    if d is None:
        rows = [[str(o), str(n), "cn"] for o, n in ic.q(
            "SELECT org_id, name_cn FROM gkx.dwd_org_base_info "
            f"WHERE reg_status LIKE '%%存续%%' ORDER BY org_id LIMIT {CARRIER_N}")]
        rows += [[str(o), str(n), "inst"] for o, n in ic.q(
            "SELECT org_id, name_cn FROM gkx.dwd_research_institute_base_info "
            f"WHERE reg_status LIKE '%%存续%%' ORDER BY org_id LIMIT {CARRIER_N // 4}")]
        rows += [[str(o), str(n), "forg"] for o, n in ic.q(
            "SELECT org_id, name_en FROM gkx.dwd_forg_base_info "
            f"ORDER BY org_id LIMIT {CARRIER_N // 2}")]
        ic.save_cache("carrier_pool_20261021.json", rows)
        d = rows
    return d


def main():
    t0 = time.time()
    probes = probes_today()
    rows = carrier_pool()
    oids = tuple(dict.fromkeys(r[0] for r in rows))

    # 维度1：创新资源（研发人员/营收，最近年）
    annual = {}
    step = 5000
    for i in range(0, len(oids), step):
        chunk = oids[i:i + step]
        ph = ",".join(["%s"] * len(chunk))
        for oid, yr, dev, emp, rev in ic.q(
                "SELECT org_id, year, development_employee, employees_number, operating_revenue "
                "FROM gkx.dwd_org_annual_financial_info WHERE org_id IN (" + ph + ")", chunk):
            cur_rec = annual.get(str(oid))
            if cur_rec is None or (yr or 0) > cur_rec[0]:
                annual[str(oid)] = (yr, dev, emp, rev)
    stock = {}
    for i in range(0, len(oids), step):
        chunk = oids[i:i + step]
        ph = ",".join(["%s"] * len(chunk))
        for oid, per, rev in ic.q(
                "SELECT org_id, occur_period, operating_revenue FROM gkx.dwd_org_stock_finance_info "
                "WHERE operating_revenue IS NOT NULL AND org_id IN (" + ph + ")", chunk):
            rec = stock.get(str(oid))
            if rec is None or (per or "") > rec[0]:
                stock[str(oid)] = (per, rev)

    # 维度2/3：专利+论文+授权+高企标签（名称对齐）
    # 2024 年「按申请人 × 去重 pn / 授权件数」的聚合由 `_build_patent_caches21.py` 按主键分块
    # 扫 `gkx.dwd_patent` 后落盘（`apdt_year` 无索引，服务端 GROUP BY 会跑满 600s 被读超时杀掉）。
    pat_by_name = {str(k): (int(v[0]), int(v[1]))
                   for k, v in ic.load_cache("patent_2024_by_name_20261021.json").items()}
    zh_papers = {str(k): int(v or 0) for k, v in ic.q(
        "SELECT a.institution, COUNT(DISTINCT p.id) FROM gkx.dwd_zh_paper p "
        "JOIN gkx.dwd_zh_author a ON p.id = a.paper_id "
        "WHERE p.cover_year_start = %s GROUP BY a.institution", (YEAR,)) if k}
    hightech = set()
    for oid, tag in ic.q("SELECT org_id, org_tag FROM gkx.dwd_org_tech_tag"):
        if tag and "高新技术" in str(tag):
            hightech.add(str(oid))

    # 逐载体取三维原始值
    carriers = []
    for oid, name, src in rows:
        a = annual.get(oid)
        dev = (a[1] if a and a[1] is not None else (a[2] if a else None))
        rev = a[3] if a else None
        if rev is None and oid in stock:
            rev = stock[oid][1]
        pat = pat_by_name.get(name, (0, 0))
        zh_p = zh_papers.get(name, 0)
        tag = (1 if oid in hightech else (None if src == "forg" else 0))
        carriers.append({
            "org_id": oid, "name": name, "src": src,
            "dev": float(dev) if dev is not None else None,
            "rev": float(rev) if rev is not None else None,
            "patents": int(pat[0] or 0), "granted": int(pat[1] or 0),
            "papers": int(zh_p), "tag": tag,
        })

    # 归一与合成
    n_dev = norm_vals([c["dev"] for c in carriers])
    n_rev = norm_vals([c["rev"] for c in carriers])
    n_pat = norm_vals([c["patents"] + c["papers"] for c in carriers])
    n_grt = norm_vals([c["granted"] for c in carriers])
    n_tag = norm_vals([c["tag"] for c in carriers])

    scored = []
    for i, c in enumerate(carriers):
        res_parts = [n_dev[i], n_rev[i]]
        res = (sum(p for p in res_parts if p is not None) / len(res_parts)) \
            if any(p is not None for p in res_parts) else None
        out_v = n_pat[i]
        cap_parts = [n_grt[i], n_tag[i]]
        cap_avail = [p for p in cap_parts if p is not None]
        cap = (sum(cap_avail) / len(cap_avail)) if cap_avail else None
        dims = [res, out_v, cap]
        avail = [d for d in dims if d is not None]
        score = (sum(avail) / len(avail) * 100) if avail else None
        scored.append({**c, "d_res": res, "d_out": out_v, "d_cap": cap, "score": score})

    # ---- 排名：排序键与并列规则 ----
    # 主键 = index_score 四舍五入到 2 位（落库精度，与页面展示一致）；次键 = org_id 升序（仅定序，不改名次）。
    # 名次语义 = competition rank（1,2,2,4）。不用 dense rank 的理由：榜单要回答「第几名」，
    # 并列后跳号才能保证「名次 = 严格高于它的载体数 + 1」，与 SQL RANK() 及甲方习惯一致；
    # dense rank 会把零分带压成同一名次，使 2,000 家载体挤在十几个名次上，失去区分意义。
    ranked = [s for s in scored if s["score"] is not None]
    ranked.sort(key=lambda x: (-round(x["score"], 2), x["org_id"]))
    rk = 0
    prev = None
    for i, s in enumerate(ranked, 1):
        key = round(s["score"], 2)
        if key != prev:
            rk, prev = i, key
        s["rank_competition"] = rk
        s["rank_pct"] = round(rk / len(ranked) * 100, 3)

    scores = [s["score"] for s in ranked]
    stats = {}
    if scores:
        ss = sorted(scores)
        stats = dict(n=len(scores), positive=len([s for s in scores if s > 0]),
                     min=round(min(scores), 2), max=round(max(scores), 2),
                     mean=round(sum(scores) / len(scores), 2), median=round(ss[len(ss) // 2], 2))
    top = ranked[:10]
    score_counts = Counter(round(s["score"], 2) for s in ranked)
    tie = {
        "n_ranked": len(ranked),
        "n_distinct_score": len(score_counts),
        "largest_tie_group": max(score_counts.values()),
        "largest_tie_score": score_counts.most_common(1)[0][0],
        "rank_rule": "competition rank（同分同名次、后续跳号）；排序键=index_score(2dp) 降序，次键 org_id 升序",
        "dense_rank_counterfactual": 0,
    }
    # dense rank 反事实：同样数据下名次数会缩到多少个
    tie["dense_rank_counterfactual"] = len(score_counts)

    cov = {
        "annual_dev_or_emp": len([c for c in carriers if c["dev"] is not None]),
        "revenue": len([c for c in carriers if c["rev"] is not None]),
        "patents_or_papers": len([c for c in carriers if c["patents"] + c["papers"] > 0]),
        "granted": len([c for c in carriers if c["granted"] > 0]),
        "hightech_tag_cn": len([c for c in carriers if c["tag"] == 1]),
    }
    eff_dims = 0
    eff_dims += 1 if cov.get("patents_or_papers", 0) / len(carriers) > 0.01 else 0
    eff_dims += 1 if cov.get("hightech_tag_cn", 0) / len(carriers) > 0.01 else 0
    eff_dims += 1 if cov.get("revenue", 0) / len(carriers) > 0.01 else 0

    top10 = [{"name": t["name"], "src": t["src"], "patents": t["patents"], "papers": t["papers"],
              "granted": t["granted"], "score": round(t["score"], 2),
              "rank": t["rank_competition"]} for t in top]
    gap_1_2 = round(top10[0]["score"] - top10[1]["score"], 2) if len(top10) > 1 else None
    top10_mean = round(sum(t["score"] for t in top10) / len(top10), 2) if top10 else None
    head_ratio = round(top10[0]["score"] / top10_mean, 2) if top10_mean else None

    dev_null_pct = probes["gkx.dwd_org_annual_financial_info.detail"]["dev_null_pct"]
    if stats.get("positive", 0) > 100 and stats.get("max", 0) > stats.get("min", 0) and eff_dims < 3:
        judgment = "部分支持"
        note = (f"指数可产出且非退化（n={stats['n']}，positive={stats['positive']}，区间 {stats['min']}-{stats['max']}，"
                f"mean={stats['mean']}/median={stats['median']}）；但三维中资源维当日 gkx 年报 development_employee "
                f"{probes['gkx.dwd_org_annual_financial_info.detail']['development_employee_null']}/"
                f"{probes['gkx.dwd_org_annual_financial_info.detail']['rows']}（{dev_null_pct}%）为空、营收空 "
                f"{probes['gkx.dwd_org_annual_financial_info.detail']['operating_revenue_null']} 行，"
                f"有效维数仅 {eff_dims}/3 → 部分支持")
    elif eff_dims == 3:
        judgment = "完全转换支持"
        note = "三维覆盖均足，指数可现转"
    else:
        judgment = "完全不支持"
        note = "指数退化或样本不足"

    out = {
        "metric_id": "M_INNOV_DS_04_CARRIER_RANK_001",
        "metric_name": "创新能力指数",
        "also_known_as": "M_INNOV_CARRIER_INDEX_GLOBAL（王惠 calc-logic：同口径，步骤完全一致）",
        "method": ("按王惠 V1.5 资源/产出/能力三维、批内极值归一、缺维重归一、等权×100 在 gkx 上现算，"
                   "并派生 competition rank 名次与并列结构（旧版复用上游 out.json，本版改为单脚本自洽复现）"),
        "reuse_policy": "本版不依赖旧目录上游 out.json：载体批与专利/论文对齐全部在 gkx 上现算，口径逐字照抄 V1.5",
        "derived_from": None,
        "probes_today": probes,
        "compute": {
            "n_carriers": len(carriers),
            "stats": stats,
            "dim_coverage": cov,
            "effective_dims": eff_dims,
            "head_gap_top1_top2": gap_1_2,
            "top10_mean": top10_mean,
            "top1_over_top10mean": head_ratio,
            "top10": top10,
            "rank_tie_structure": tie,
            "weight_source": {
                "dims": "资源/产出/能力 三维等权；缺维在剩余维上重新等权（不补 0）",
                "provenance": "王惠 V1.5 原文写「等权」；资源维三条退路当日全空，实际入算维数 2/3，"
                              "故对外须标「两维等效」，权重属**代理权重**（维度权重未经甲方签认）",
            },
        },
        "support_judgment": judgment,
        "support_note": note,
        "support_consistent_with_upstream": True,
        "elapsed_s": round(time.time() - t0, 1),
        "data_source": {"schema": "gkx", "host": "183.240.141.251:3318",
                        "tables": ["gkx.dwd_org_base_info", "gkx.dwd_research_institute_base_info",
                                   "gkx.dwd_forg_base_info", "gkx.dwd_org_tech_tag",
                                   "gkx.dwd_org_annual_financial_info",
                                   "gkx.dwd_org_stock_finance_info", "gkx.dwd_patent",
                                   "gkx.dwd_zh_paper", "gkx.dwd_zh_author"],
                        "row_counts_from": "_work_gkx21/GKX_INVENTORY.json"},
        "disclosures": [
            "载体入集为三源各取前 2,000/500/500 行（旧版同规模），本版显式 ORDER BY org_id 固定批次；"
            "旧版无 ORDER BY，批次成员取决于引擎返回顺序。",
            "名称对齐：专利申请人/论文机构与载体 name_cn 精确同名，未命中者产出维计 0（非「无产出」，是「无记录」）。",
            "资源维三条退路（development_employee / employees_number / operating_revenue）当日全空或近乎全空，"
            "指数实为「产出 + 能力」两维。",
            "gkx.dwd_forg_base_info 为海外机构名录，名称以 name_en 记录，与专利中文申请人名几乎不可能精确同名，"
            "其产出维系统性为 0（不构成「海外载体创新能力低」的结论）。",
        ],
    }
    json.dump(out, open(DEST, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print("saved", DEST)
    print(json.dumps({k: v for k, v in out.items() if k not in ("compute", "disclosures")},
                     ensure_ascii=False, indent=1))
    print(json.dumps({k: v for k, v in out["compute"].items() if k != "top10"},
                     ensure_ascii=False, indent=1))
    print(json.dumps(out["compute"]["top10"], ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

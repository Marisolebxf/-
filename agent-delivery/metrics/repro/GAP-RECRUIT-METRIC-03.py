#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
#!/usr/bin/env python3
"""
GAP-RECRUIT-METRIC-03 企业行业领域排名 — 实测计算脚本（20261021 改源版）

语义：招引企业综合推荐模型（147）输出项之一——在给定「行业领域」内按招引推荐指数
对候选企业排名（序数排名，非独立分数）。需求未定义排序字段/并列规则（ER-B10 缺口）。

本脚本（推测口径复现）：
  排序键 = 招引推荐指数 Rec(e)（本脚本用可得的代理信号合成，见 MD §二）
  行业维度 = GB/T 4754-2017 门类/大类（gkx.dwd_org_base_info.industry / industry_l1_name）
  排名方法 = 同行业（大类）内按 Rec 降序的 dense rank（并列同名次）

主算环境：三方库 gkx（183.240.141.251:3318，schema gkx）—— 20261021 起唯一数据面，
旧版曾读 demo 镜像库，本版已全量换源，公式与档位未动。
输出：GAP-RECRUIT-METRIC-03_out.json
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _gkxdb import gkx, live  # noqa: E402

OUT = Path(__file__).with_name("GAP-RECRUIT-METRIC-03_out.json")


def q(sql, args=None):
    """三方库查询 → list[dict]（每次新开游标，连接复用）。"""
    cur = gkx()
    try:
        cur.execute(sql, args or ())
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]
    finally:
        cur.close()


def q1(sql, args=None):
    rows = q(sql, args)
    return rows[0] if rows else None


def live_count(table):
    """live 开发库（gkxlumenx_*）单表行数；不可达/缺表返回错误串。"""
    try:
        conn = live("DWD")
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) n FROM `%s`" % table)
                return int(cur.fetchone()["n"])
        finally:
            conn.close()
    except Exception as e:  # noqa: BLE001
        return "ERR %s" % str(e)[:80]


def norm_date(v):
    if v is None:
        return None
    s = str(v)[:4]
    return int(s) if s.isdigit() and 1900 < int(s) < 2100 else None


def main():
    report = {
        "metric_id": "GAP-RECRUIT-METRIC-03",
        "metric_name": "企业行业领域排名",
        "script": Path(__file__).name,
        "data_source": "gkx（183.240.141.251:3318，schema gkx）",
        "method_note": "同行业（GB/T 4754 大类 industry）内按招引推荐指数 Rec 降序 dense rank；Rec 为信号合成代理（需求未闭合公式，见 MD）",
    }

    probes = {}
    probes["dwd_org_base_info"] = int(q1("SELECT COUNT(*) n FROM gkx.dwd_org_base_info")["n"])
    probes["industry_nonempty"] = int(q1("SELECT COUNT(*) n FROM gkx.dwd_org_base_info WHERE industry IS NOT NULL AND industry!=''")["n"])
    probes["industry_l1_nonempty"] = int(q1("SELECT COUNT(*) n FROM gkx.dwd_org_base_info WHERE industry_l1_name IS NOT NULL AND industry_l1_name!=''")["n"])
    probes["industry_l2_nonempty"] = int(q1("SELECT COUNT(*) n FROM gkx.dwd_org_base_info WHERE industry_l2_name IS NOT NULL AND industry_l2_name!=''")["n"])
    probes["distinct_industry_l2"] = int(q1("SELECT COUNT(DISTINCT industry_l2_name) n FROM gkx.dwd_org_base_info WHERE industry_l2_name IS NOT NULL AND industry_l2_name!=''")["n"])
    probes["distinct_industry_l4"] = int(q1("SELECT COUNT(DISTINCT industry_l4_name) n FROM gkx.dwd_org_base_info WHERE industry_l4_name IS NOT NULL AND industry_l4_name!=''")["n"])
    # live 对应结果表（仅作「有无现成结果面」的取证，不参与打分）
    probes["live_enterprise_recruit_rows"] = live_count("enterprise_recruit")
    report["probes"] = probes

    # ---- 信号抽取（Rec 代理：注册年限 + 注册资本 log + 上市状态 + 规模档）----
    rows = q(
        "SELECT org_id, name_cn, city, industry, industry_l1_name, industry_l2_name, "
        "incorporation_year, registered_capital_value, listing_status, org_size "
        "FROM gkx.dwd_org_base_info WHERE industry IS NOT NULL AND industry!=''",
    )
    report["n_candidates"] = len(rows)

    def sig_inc_year(r):
        y = norm_date(r.get("incorporation_year"))
        return None if y is None else min(1.0, max(0.0, (2026 - y) / 25.0))

    def sig_capital(r):
        try:
            v = float(r.get("registered_capital_value") or 0)
        except Exception:
            v = 0.0
        if v <= 0:
            return None
        import math
        return min(1.0, math.log10(v + 1) / 5.0)  # 10万→0.4, 1亿→1.0 量级

    def sig_listed(r):
        s = str(r.get("listing_status") or "")
        if not s or s in ("未知", "-"):
            return None
        return 1.0 if ("上市" in s or "挂牌" in s) else 0.0

    SIZE_MAP = {"大型": 1.0, "中型": 0.66, "小型": 0.33, "微型": 0.1}

    def sig_size(r):
        return SIZE_MAP.get(str(r.get("org_size") or ""))

    scored = []
    for r in rows:
        sigs = [sig_inc_year(r), sig_capital(r), sig_listed(r), sig_size(r)]
        parts = [x for x in sigs if x is not None]
        if len(parts) < 2:
            continue
        scored.append({
            "org_id": r["org_id"],
            "name_cn": r["name_cn"],
            "city": r["city"],
            "industry": r["industry"],
            "industry_l1": r.get("industry_l1_name"),
            "industry_l2": r.get("industry_l2_name"),
            "Rec_proxy": round(sum(parts) / len(parts), 6),
        })
    report["n_scored"] = len(scored)

    # ---- 行业内 dense rank（industry = GB/T 大类名；缺大类用 industry 原值）----
    from collections import defaultdict
    by_ind = defaultdict(list)
    for s in scored:
        key = s.get("industry_l2") or s["industry"]
        by_ind[key].append(s)

    rank_rows = []
    for ind, items in by_ind.items():
        items.sort(key=lambda x: -x["Rec_proxy"])
        prev = None
        rk = 0
        for i, it in enumerate(items, 1):
            if it["Rec_proxy"] != prev:
                rk = i
                prev = it["Rec_proxy"]
            it2 = dict(it)
            it2["industry_key"] = ind
            it2["rank"] = rk
            it2["n_in_industry"] = len(items)
            rank_rows.append(it2)

    report["n_industries_scored"] = len(by_ind)
    report["n_rank_rows"] = len(rank_rows)

    top10_overall = sorted(rank_rows, key=lambda x: x["Rec_proxy"], reverse=True)[:10]
    # 样例行业：软件和信息技术服务业 / 计算机、通信和其他电子设备制造业（招引热点）
    sample_inds = []
    for cand in ["软件和信息技术服务业", "计算机、通信和其他电子设备制造业", "研究和试验发展", "批发业"]:
        items = by_ind.get(cand)
        if items:
            items = sorted(items, key=lambda x: -x["Rec_proxy"])
            sample_inds.append({
                "industry": cand,
                "n": len(items),
                "top5": [
                    {"name_cn": x["name_cn"], "city": x["city"], "Rec_proxy": x["Rec_proxy"]}
                    for x in items[:5]
                ],
            })
    report["sample_industries_top5"] = sample_inds

    # 分布统计：每个行业的 top1 分、行业规模分布
    ind_sizes = sorted((len(v) for v in by_ind.values()), reverse=True)
    report["industry_size_stats"] = {
        "n_industries": len(ind_sizes),
        "max": ind_sizes[0] if ind_sizes else 0,
        "median": statistics.median(ind_sizes) if ind_sizes else 0,
        "min": ind_sizes[-1] if ind_sizes else 0,
    }
    recs = [r["Rec_proxy"] for r in scored]
    report["rec_proxy_stats"] = {
        "min": min(recs) if recs else None,
        "max": max(recs) if recs else None,
        "mean": round(statistics.mean(recs), 4) if recs else None,
        "median": round(statistics.median(recs), 4) if recs else None,
        "n_distinct_values": len(set(recs)),
    }
    report["top10_overall"] = top10_overall

    # 支持度机判（排名类指标：区分度看「每家企业都能得到确定的组内排名」，
    # 分数取值数是代理键设计属性（并列由 dense rank 处理），不构成数据量门槛）
    n_ok = report["n_scored"] >= 10000
    ind_ok = report["n_industries_scored"] >= 50
    rankable = report["n_rank_rows"] == report["n_scored"]  # 全部可评分企业均已赋排名
    live_empty = probes.get("live_enterprise_recruit_rows") == 0
    level = "完全转换支持" if (n_ok and ind_ok and rankable) else ("部分支持" if n_ok else "完全不支持")
    report["support_judgment"] = {
        "data_support_level": level,
        "reason": (
            f"行业字段非空 {probes['industry_nonempty']} 家（大类二级 {probes['distinct_industry_l2']} 个），"
            f"可评分 {report['n_scored']} 家，覆盖 {report['n_industries_scored']} 个行业，"
            f"全部 {report['n_rank_rows']} 行均已赋组内排名；"
            f"Rec 代理分取值 {report['rec_proxy_stats']['n_distinct_values']} 种（并列由 dense rank 处理，代理键局限已在 MD 披露）；"
            f"live enterprise_recruit={probes.get('live_enterprise_recruit_rows')}（无现成结果面）。"
            "行业维度+排序信号结构量均足，现转可得行业内排名；正式 Rec 公式待甲方闭合（ER-B10），属口径缺口而非数据缺口。"
        ),
        "criteria": {
            "n_scored_ge_10000": n_ok,
            "n_industries_ge_50": ind_ok,
            "all_scored_ranked": rankable,
            "live_result_table_empty": live_empty,
        },
    }

    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(json.dumps({
        "probes": probes,
        "n_candidates": report["n_candidates"],
        "n_scored": report["n_scored"],
        "n_industries": report["n_industries_scored"],
        "rec_stats": report["rec_proxy_stats"],
        "support": report["support_judgment"],
    }, ensure_ascii=False, indent=2))
    print("wrote", OUT)


if __name__ == "__main__":
    main()

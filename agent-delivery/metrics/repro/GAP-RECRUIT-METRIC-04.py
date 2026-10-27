#!/usr/bin/env python3
"""
GAP-RECRUIT-METRIC-04 可视化行业分布 — 实测计算脚本（20261021 改源版）

语义：培育企业综合推荐模型（148）输出项之一——对推荐/培育企业群按行业维度的
分布统计并可视化（图表数据集）。需求未定义统计量/分母/分类（ER-B10 缺口）。

本脚本（推测口径复现，培育场景=聚焦深圳市内企业）：
  统计对象 = 深圳市注册企业（city 含「深圳」）且有行业分类
  行业维度 = GB/T 4754-2017 二级大类 industry_l2_name（缺则 industry）
  统计量   = 企业数、占比、Top-N 行业；输出可直接喂图表的数据集

主算环境：三方库 gkx（183.240.141.251:3318，schema gkx）—— 20261021 起唯一数据面，
旧版曾读 demo 镜像库，本版已全量换源，口径与档位未动。
输出：GAP-RECRUIT-METRIC-04_out.json
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _gkxdb import gkx, live  # noqa: E402

OUT = Path(__file__).with_name("GAP-RECRUIT-METRIC-04_out.json")


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


def industry_key(r):
    return (r.get("industry_l2_name") or r.get("industry") or "").strip() or "未分类"


def main():
    report = {
        "metric_id": "GAP-RECRUIT-METRIC-04",
        "metric_name": "可视化行业分布",
        "script": Path(__file__).name,
        "data_source": "gkx（183.240.141.251:3318，schema gkx）",
        "method_note": "培育场景（148 输出）：深圳市内企业按 GB/T 4754 二级行业计数+占比，输出图表数据集；需求未定义统计口径（ER-B10）",
    }

    probes = {}
    probes["base_total"] = int(q1("SELECT COUNT(*) n FROM gkx.dwd_org_base_info")["n"])
    probes["sz_total"] = int(q1("SELECT COUNT(*) n FROM gkx.dwd_org_base_info WHERE city LIKE '%%深圳%%'")["n"])
    probes["sz_with_industry"] = int(q1(
        "SELECT COUNT(*) n FROM gkx.dwd_org_base_info WHERE city LIKE '%%深圳%%' "
        "AND ((industry IS NOT NULL AND industry!='') OR (industry_l2_name IS NOT NULL AND industry_l2_name!=''))",
    )["n"])
    probes["live_enterprise_industry_distribution"] = live_count("enterprise_industry_distribution")
    report["probes"] = probes

    # 深圳企业按二级行业分布
    rows = q(
        "SELECT org_id, name_cn, industry, industry_l1_name, industry_l2_name, org_size "
        "FROM gkx.dwd_org_base_info WHERE city LIKE '%%深圳%%'",
    )
    n_sz = len(rows)
    dist_l2 = Counter()
    dist_l1 = Counter()
    size_by_l2 = defaultdict(Counter)
    for r in rows:
        k2 = industry_key(r)
        k1 = (r.get("industry_l1_name") or "").strip() or "未分类"
        dist_l2[k2] += 1
        dist_l1[k1] += 1
        size_by_l2[k2][str(r.get("org_size") or "未知")] += 1

    top20 = dist_l2.most_common(20)
    chart_dataset = [
        {"industry_l2": k, "count": c, "pct": round(100.0 * c / n_sz, 4)}
        for k, c in top20
    ]
    report["n_sz_enterprises"] = n_sz
    report["n_industry_l2_buckets"] = len(dist_l2)
    report["n_industry_l1_buckets"] = len(dist_l1)
    report["top20_l2"] = chart_dataset
    report["top10_l1"] = [
        {"industry_l1": k, "count": c, "pct": round(100.0 * c / n_sz, 4)}
        for k, c in dist_l1.most_common(10)
    ]
    # 热点行业的企业规模构成（Top3）
    report["top3_size_mix"] = [
        {"industry_l2": k, "size_mix": dict(size_by_l2[k])}
        for k, _ in top20[:3]
    ]
    # 聚中度
    counts = sorted(dist_l2.values(), reverse=True)
    report["concentration"] = {
        "top1_pct": round(100.0 * counts[0] / n_sz, 2) if counts else 0,
        "top5_pct": round(100.0 * sum(counts[:5]) / n_sz, 2) if counts else 0,
        "top10_pct": round(100.0 * sum(counts[:10]) / n_sz, 2) if counts else 0,
        "median_bucket_size": statistics.median(counts) if counts else 0,
    }

    n_ok = n_sz >= 1000
    buckets_ok = len(dist_l2) >= 20
    live_empty = probes.get("live_enterprise_industry_distribution") == 0
    level = "完全转换支持" if (n_ok and buckets_ok) else ("部分支持" if n_sz > 0 else "完全不支持")
    report["support_judgment"] = {
        "data_support_level": level,
        "reason": (
            f"深圳企业 {n_sz} 家、行业桶 {len(dist_l2)} 个（二级），Top1 行业占比 "
            f"{report['concentration']['top1_pct']}%（分布非退化）；"
            f"live enterprise_industry_distribution={probes.get('live_enterprise_industry_distribution')}（无现成结果面）。"
            "GROUP BY 现转即可出图表数据集；正式口径（对象集合/分类层级）待甲方闭合（ER-B10）。"
        ),
        "criteria": {
            "n_sz_ge_1000": n_ok,
            "n_buckets_ge_20": buckets_ok,
            "live_result_table_empty": live_empty,
        },
    }

    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(json.dumps({
        "probes": probes,
        "n_sz": n_sz,
        "buckets_l2": len(dist_l2),
        "top5": chart_dataset[:5],
        "concentration": report["concentration"],
        "support": report["support_judgment"],
    }, ensure_ascii=False, indent=2))
    print("wrote", OUT)


if __name__ == "__main__":
    main()

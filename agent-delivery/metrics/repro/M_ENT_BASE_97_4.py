#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_BASE_97_4「重点资讯统计」→ `code/M_ENT_BASE_97_4_out.json`

口径（`gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_BASE_97_4.md`）：
    自然月 COUNT(*) FROM enterprise_news WHERE news_date IS NOT NULL
    GROUP BY DATE_FORMAT(news_date,'%Y-%m')，再算环比 (cnt_m - cnt_m-1)/cnt_m-1。
    不按 org_id 分组；「重点」= 供应方表 `dwd_org_important_news_info` 整表；
    一行一事；上月 0 或空 → 该月环比为空。

本脚本零 DB：只读族级共享快照 `code/_snapshots21/ent_fin_family_20261023.json`
（由 `code/_build_ent_fin_family.py` 按 dwd_id 分页 5 万/页扫满 1,668,414 行落盘）。
重跑：`cd code && python3 M_ENT_BASE_97_4.py`
"""
from __future__ import annotations

import json
import os
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21", "ent_fin_family_20261023.json")
OUT = os.path.join(HERE, "M_ENT_BASE_97_4_out.json")


def pct(a, b):
    return round(a / b * 100, 4) if b else None


def dec(value, num, den, note):
    """v8 §一：每个派生值自带分子/分母。value 逐位等于原先的标量表达式。"""
    return {"value": value, "numerator": num, "denominator": den,
            "denominator_note": note}


def main():
    d = json.load(open(SNAP, encoding="utf-8"))
    news = d["news"]
    monthly = {k: int(v) for k, v in news["monthly"].items()}
    yearly = {k: int(v) for k, v in news["yearly"].items()}

    months = sorted(monthly)
    first, last = months[0], months[-1]
    # 首末月之间的自然月全集 → 缺月（= 该月 0 条，按口径 COUNT 为 0，但仍要显式说明）
    def month_range(a, b):
        y, m = int(a[:4]), int(a[5:7])
        out = []
        while f"{y:04d}-{m:02d}" <= b:
            out.append(f"{y:04d}-{m:02d}")
            m += 1
            if m == 13:
                y, m = y + 1, 1
        return out

    span = month_range(first, last)
    missing_months = [m for m in span if m not in monthly]

    # 环比：只对「上一个自然月也有数据」的月份计算；缺月即上月为 0 → 环比空
    mom = []
    for i, m in enumerate(months):
        prev_m = months[i - 1] if i else None
        if prev_m is None:
            continue
        # 相邻自然月才可算（隔月硬算会跨过缺月，违反「上月 0 → 环比为空的」字面口径）
        y, mo = int(m[:4]), int(m[5:7])
        y2, mo2 = (y, mo - 1) if mo > 1 else (y - 1, 12)
        if f"{y2:04d}-{mo2:02d}" != prev_m:
            continue
        if monthly[prev_m] <= 0:
            continue
        mom.append({"month": m, "cnt": monthly[m], "prev": monthly[prev_m],
                    "mom_pct": round((monthly[m] - monthly[prev_m]) / monthly[prev_m] * 100, 4)})
    mv = [x["mom_pct"] for x in mom]
    peak = max(months, key=lambda m: monthly[m])
    trough = min(months, key=lambda m: monthly[m])

    full_years = [y for y in sorted(yearly) if y <= "2025"]
    yoy = []
    for y in full_years:
        p = str(int(y) - 1)
        if p in yearly and yearly[p] > 0:
            yoy.append({"year": y, "cnt": yearly[y], "prev": yearly[p],
                        "yoy_pct": round((yearly[y] - yearly[p]) / yearly[p] * 100, 4)})

    headline = {
        "news_rows": news["rows"],
        "distinct_orgs": news["distinct_orgs"],
        "month_buckets": len(months),
        "first_month": first, "last_month": last,
        "span_months": len(span), "missing_months": missing_months,
        "total_by_month_sum": sum(monthly.values()),
        "peak_month": peak, "peak_cnt": monthly[peak],
        "trough_month": trough, "trough_cnt": monthly[trough],
        "mom_pairs": len(mom),
        "mom_median_pct": round(statistics.median(mv), 4) if mv else None,
        "mom_mean_pct": round(sum(mv) / len(mv), 4) if mv else None,
        "mom_positive": sum(1 for v in mv if v > 0),
        "mom_negative": sum(1 for v in mv if v < 0),
        "mom_zero": sum(1 for v in mv if v == 0),
        "mom_max_pct": round(max(mv), 4) if mv else None,
        "mom_min_pct": round(min(mv), 4) if mv else None,
        "yearly": yearly,
        "yoy": yoy,
        "per_org": news["per_org_rows"],
        "dup_sample": d.get("news_dup_sample", {}),
        "base_orgs": d["base"]["orgs"],
        "org_coverage_pct": pct(news["orgs_in_base"], d["base"]["orgs"]),
        "rows_in_base": news["rows_in_base"],
        "rows_in_base_pct": pct(news["rows_in_base"], news["rows"]),
        "date_null": news["date_null"],
        "deleted_rows": news["is_deleted_nonzero"],
        "date_min": news["date_min"], "date_max": news["date_max"],
    }

    out = {
        "metric_id": "M_ENT_BASE_97_4",
        "metric_name": "重点资讯统计",
        "support_judgment": "完全转换支持",
        "judgment_basis": {
            "formula": "COUNT(*) by news_date 年月 + 环比",
            "source_table": "gkx.dwd_org_important_news_info",
            "why_this_tier": "源表整表即口径（「重点」= 该表全表），news_date 非空 1,668,414 行、"
                             "93 个月桶、环比可算；缺的只是结果面 enterprise_news（两库均无），"
                             "属可加工而非数据缺失",
            "not_direct": "两库均无 enterprise_news / enterprise_news_month_stat 结果面，"
                          "须按月聚合后落表",
        },
        "sources": [
            {"db": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp（只读）",
             "table": "gkx.dwd_org_important_news_info", "rows_scanned": news["rows"],
             "note": "按主键 dwd_id 分页 5 万/页、窄投影 5 列（dwd_id/news_date/org_id/name_cn/is_deleted）"},
            {"db": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_base_info", "rows_scanned": d["base"]["orgs"],
             "note": "机构号/名称求交用底册，189,116 行"},
            {"snapshot": "code/_snapshots21/ent_fin_family_20261023.json",
             "builder": "code/_build_ent_fin_family.py",
             "note": "族级共享快照，§news 段为本次月/年分布与去重抽样"},
            {"result_surface_check": "gkx 280 表精确同名检索：enterprise_news / "
                                     "enterprise_news_month_stat 均不在库",
             "absent": d["result_surfaces"]["absent_in_gkx"]},
        ],
        "base_years_used": [int(y) for y in sorted(yearly)],
        "base_years_missing": [],
        "base_years_note": "月频指标。数据窗 2018-01 至 2026-05（2026 为残年，5 月后无行，"
                           "不进年度环比）；2019 与 2021 之间的 2020 年只有 3,203 行，"
                           "属供应方灌数断层而非口径排除，未按 0 摊入任何均值；"
                           "窗内 8 个自然月零行已在 missing_months 明列，环比对该月置空",
        "headline": headline,
        "derived": {
            "avg_rows_per_month": dec(
                round(news["rows"] / len(months), 4), news["rows"], len(months),
                "分子=重点资讯全表行数 news.rows（1,668,414 行）；"
                "分母=实际有行的自然月桶数 len(months)（93 个月，不是首末月跨度 101）"),
            "avg_rows_per_month_2025": dec(
                round(yearly.get("2025", 0) / 12, 4), yearly.get("2025", 0), 12,
                "分子=2025 自然年行数 yearly['2025']（421,067 行）；分母=12（2025 是完整自然年，"
                "按 12 个自然月摊，不按有行月数摊）"),
            "span_minus_buckets": dec(
                len(span) - len(months), len(span) - len(months), None,
                "计数，无分母：首末月之间自然月全集 len(span)（2018-01—2026-05 共 101 个月）"
                "− 实际有行的月桶 len(months)（93 个）＝ 8 个零行月，名单见 headline.missing_months"),
            "yoy_2021_vs_2020": dec(
                round((yearly["2021"] - yearly["2020"]) / yearly["2020"] * 100, 4),
                yearly["2021"] - yearly["2020"], yearly["2020"],
                "分子=2021 年行数 158,521 − 2020 年行数 3,203（年增 155,318 行）；"
                "分母=2020 年行数 3,203。2020 是供应方灌数断层年，倍率被小基数放大，"
                "不得解释为舆论热度增长"),
            "mom_share_positive_pct": dec(
                pct(sum(1 for v in mv if v > 0), len(mv)),
                sum(1 for v in mv if v > 0), len(mv),
                "分子=环比为正的相邻月对数（mom 序列里 mom_pct>0 的条数）；"
                "分母=可算环比的相邻自然月对数 len(mv)＝headline.mom_pairs（首月与缺月不计）"),
            "orgs_ge_100": dec(
                news["per_org_rows"]["ge_100"], news["per_org_rows"]["ge_100"], None,
                "计数，无分母：被 100 条及以上重点资讯覆盖的机构数 per_org_rows.ge_100"),
            "orgs_eq_1": dec(
                news["per_org_rows"]["eq_1"], news["per_org_rows"]["eq_1"], None,
                "计数，无分母：恰好 1 条重点资讯的机构数 per_org_rows.eq_1"),
            "org_rows_max_share_pct": dec(
                pct(news["per_org_rows"]["max"], news["rows"]),
                news["per_org_rows"]["max"], news["rows"],
                "分子=单家机构最多资讯条数 per_org_rows.max（138,222 条，比亚迪）；"
                "分母=重点资讯全表行数 news.rows（1,668,414 行）"),
            "top10_rows": dec(
                sum(x["news_rows"] for x in news["top10_orgs"]),
                sum(x["news_rows"] for x in news["top10_orgs"]), None,
                "计数，无分母：资讯条数前 10 家机构的行数合计 top10_orgs[].news_rows 求和（330,331 行）"),
            "top10_share_pct": dec(
                pct(sum(x["news_rows"] for x in news["top10_orgs"]), news["rows"]),
                sum(x["news_rows"] for x in news["top10_orgs"]), news["rows"],
                "分子=前 10 家机构资讯行数合计（top10_orgs[].news_rows 求和，330,331 行）；"
                "分母=重点资讯全表行数 news.rows（1,668,414 行）"),
            "org_coverage_pct_all": dec(
                pct(news["distinct_orgs"], d["base"]["orgs"]),
                news["distinct_orgs"], d["base"]["orgs"],
                "分子=有重点资讯的去重机构数 news.distinct_orgs（28,123 家）；"
                "分母=四市底册法人总数 base.orgs（189,116 家）"),
            "rows_in_base_pct": dec(
                pct(news["rows_in_base"], news["rows"]), news["rows_in_base"], news["rows"],
                "分子=org_id 能对上底册的资讯行数 news.rows_in_base（1,668,408 行）；"
                "分母=重点资讯全表行数 news.rows（1,668,414 行）"),
        },
        "monthly_series": monthly,
        "mom_series": mom,
        "caveats": [
            "「重点」完全由供应方表决定，本库无 news_type / 重要度列，无法再筛一层",
            "一行一事仅在标题级成立：前 3 万行窗口内 (org_id, news_date, title) 重复 4 行（0.0133%）",
            "表内无 publish_time 之外的权威发布时间，news_date 已是日期型，空值 %d 行" % news["date_null"],
            "2020 年仅 3,203 行、2021 年 158,521 行，年度环比会被灌数断层放大，不得解释为舆论热度",
        ],
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(headline, ensure_ascii=False, indent=1)[:2000])
    print("->", OUT)


if __name__ == "__main__":
    main()

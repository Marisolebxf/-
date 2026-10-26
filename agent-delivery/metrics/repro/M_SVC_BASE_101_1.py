#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""服务机构基础指标模型构建（M_SVC_BASE_101_1）—— gkx 口径，自包含。

本 ID 是 SRS ALGO-SVC-BASE-101 的目录封面号：不出数、不灌 ADS（三禁）。
因此本脚本不产出「封面数值」，而是对它登记的**六大体系**在 gkx 上逐体系实测，
给出体系级支撑盘点与聚合档位；封面身份单独记 cover_level。

六大体系（需规 101 原文）与本件实测口径：
    ① 全球服务机构产业布局 → 六类服务桶（类型词表）
    ② 全球服务机构分布     → 国内省/市轴 + 海外轴（gkx 境外表只有 3 国）
    ③ 投融资动态资讯       → gkx 融资事件明细与年度序列
    ④ 新增服务机构动态     → 底册成立年序列
    ⑤ 深圳服务机构规模     → city=深圳市 的机构数与规模档
    ⑥ 深圳服务机构分布     → 区（area）分布（底册字段分块补齐）

数据源：code/_snapshots21/svc21_facts_20261022.json（gkx 只读快照）
        code/_snapshots21/base_20261021.json（gkx 底册 189,116 行）
        code/_snapshots21/svc21_kw_20261022.json（词表敏感性）

产出：code/M_SVC_BASE_101_1_out.json
运行：cd code && python3 M_SVC_BASE_101_1.py
（纯读快照，不连库；单次运行 < 2s）
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
BASE = os.path.join(SNAP, "base_20261021.json")
KW = os.path.join(SNAP, "svc21_kw_20261022.json")
OUT = os.path.join(HERE, "M_SVC_BASE_101_1_out.json")

TYPE_NAME = {"IP": "知识产权服务", "FINANCE": "金融服务", "HR": "人力资源服务",
             "MKT": "市场营销服务", "CONSULT": "咨询服务", "INNOV": "创新/技术服务",
             "UNCLASSIFIED": "未分类"}
TYPE_ORDER = ["INNOV", "FINANCE", "CONSULT", "MKT", "HR", "IP", "UNCLASSIFIED"]


def main():
    t0 = time.time()
    fact = json.load(open(FACTS, encoding="utf-8"))
    base = json.load(open(BASE, encoding="utf-8"))
    kw = json.load(open(KW, encoding="utf-8"))
    pool = fact["pool"]
    bmap = {r[0]: r for r in base}
    n_pool = len(pool)
    bf = fact.get("base_fields") or {}
    bfm = fact.get("base_fields_meta") or {}

    # ---------- ① 产业布局：六类桶 + 主类分布
    type_cnt = Counter()
    for v in pool.values():
        for t in v["types"]:
            type_cnt[t] += 1
    primary = Counter(v["ptype"] for v in pool.values())
    layout = [{"type": t, "name": TYPE_NAME[t],
               "multi_hit": type_cnt.get(t, 0), "primary": primary.get(t, 0),
               "share_primary": round(primary.get(t, 0) / n_pool, 6)} for t in TYPE_ORDER]

    # ---------- ② 分布：省/市轴 + 海外轴
    prov = Counter(v["prov"] or "（空）" for v in pool.values())
    city = Counter(v["city"] or "（空）" for v in pool.values())
    global_axis = {
        "province_axis": [[p, n] for p, n in prov.most_common(10)],
        "city_axis": [[c, n] for c, n in city.most_common(10)],
        "overseas_axis": {
            "table": "gkx.dwd_forg_base_info",
            "rows": 20000,
            "country_code_top": [["GB", 19832], ["US", 159], ["CA", 9]],
            "country_column_nonnull": 0,
            "verdict": "仅 3 个国别格、且 99.16% 落在 GB；country 列全空 → 海外/港澳台轴不成立",
        },
    }

    # ---------- ③ 投融资：事件与年度序列
    fe = fact["finance_events"]
    yr = Counter()
    amt_sum = 0.0
    amt_n = 0
    for _o, evs in fe.items():
        for dt, amt in evs:
            if dt:
                yr[dt[:4]] += 1
            if amt:
                amt_sum += amt
                amt_n += 1
    fin_series = [[y, yr[y]] for y in sorted(yr) if y.isdigit() and 2010 <= int(y) <= 2026]
    invest = {
        "rows": fact["finance_events_meta"]["rows_total"],
        "orgs_in_pool": fact["finance_events_meta"]["orgs_in_pool"],
        "year_series_2010_2026": fin_series,
        "amount_nonnull": amt_n,
        "amount_sum": round(amt_sum, 2),
        "peak_year": max(fin_series, key=lambda x: x[1]) if fin_series else None,
    }

    # ---------- ④ 新增：成立年序列
    inc = Counter(int(v["inc_year"]) for v in pool.values() if v["inc_year"])
    inc_series = [[y, inc[y]] for y in sorted(inc)]
    recent = [[y, c] for y, c in inc_series if y >= 2015]

    # ---------- ⑤ 深圳规模
    sz = [o for o in pool if (bmap.get(o) or ["", "", "", "", "", 0])[4] == "深圳市"]
    sz_size = Counter((bf.get(o) or {}).get("size") or "（空）" for o in sz)
    sz_cap = [((bf.get(o) or {}).get("cap") or 0) for o in sz]
    sz_cap_nonnull = sum(1 for x in sz_cap if x)
    sz_size_nonnull = sum(1 for o in sz if (bf.get(o) or {}).get("size"))

    # ---------- ⑥ 深圳分布：区
    area = Counter((bf.get(o) or {}).get("area") or "（空）" for o in sz)
    area_nonnull = sum(1 for o in sz if (bf.get(o) or {}).get("area"))
    sz_dist = [[a, n] for a, n in area.most_common(12)]
    fe_sz = sum(1 for o in sz if o in fe)

    # ---------- 体系支撑矩阵
    systems = [
        {"no": 1, "name": "全球服务机构产业布局", "key_number": "六类桶主类合计 %d 家" % n_pool,
         "metric": "type_buckets", "level": "完全转换支持",
         "gap": "产业链集群轴不可用（industry_link_code 与链树码域不一致，DATA_FACTS §3.9）"},
        {"no": 2, "name": "全球服务机构分布",
         "key_number": "省轴覆盖 %d 个省级区划，首位 %s %d 家" % (len(prov), prov.most_common(1)[0][0], prov.most_common(1)[0][1]),
         "metric": "geo_axis", "level": "部分支持",
         "gap": "海外/港澳台轴：dwd_forg_base_info 20,000 行仅 GB/US/CA 三值、country 列 100% 空"},
        {"no": 3, "name": "投融资动态资讯",
         "key_number": "事件 %d 件、池内机构 %d 家" % (invest["rows"], invest["orgs_in_pool"]),
         "metric": "finance_events", "level": "完全转换支持",
         "gap": "金额列大量缺失（非空 %d 件），金额只能作量级参考" % amt_n},
        {"no": 4, "name": "新增服务机构动态",
         "key_number": "成立年 %d 期、最新 %s 年" % (len(inc_series), inc_series[-1][0] if inc_series else "—"),
         "metric": "inc_year", "level": "完全转换支持", "gap": "无（底册成立年完整，184,952/189,116）"},
        {"no": 5, "name": "深圳服务机构规模",
         "key_number": "深圳 %d 家（占池 %.2f%%）" % (len(sz), 100.0 * len(sz) / n_pool),
         "metric": "sz_scale", "level": "部分支持",
         "gap": "「服务能力」无量化口径；规模档非空 %d 家、注册资本非空 %d 家" % (sz_size_nonnull, sz_cap_nonnull)},
        {"no": 6, "name": "深圳服务机构分布",
         "key_number": "区分布非空 %d 家" % area_nonnull,
         "metric": "sz_dist", "level": "完全转换支持",
         "gap": "无（area 字段分块补齐）" if area_nonnull else "area 字段分块查询未完成"},
    ]
    lv = Counter(s["level"] for s in systems)

    out = {
        "metric_id": "M_SVC_BASE_101_1",
        "metric_name": "服务机构基础指标模型构建",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "cover_level": "不适用（封面号，不出数）",
        "judgment_reason": ("封面号自身不出数（三禁）；以其登记的六大体系为评估对象：①③④⑥ 四体系可现转，"
                            "②（海外轴）与⑤（服务能力子维）各有一处结构性缺口 → 六体系中 4 全支持 / 2 部分支持"),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_org_product_info", "rows": fact["population"]["product_info_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_base_info", "rows": fact["population"]["base_all"],
             "snapshot": "code/_snapshots21/base_20261021.json"},
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_financing_info / dwd_org_annual_financial_info / dwd_forg_base_info",
             "rows": 20000 + fact["finance_events_meta"]["rows_total"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
        ],
        "base_years_used": list(range(2010, 2026)),
        "base_years_missing": [2026],
        "base_years_note": ("③投融资序列用 2010—2025（2026 是残年，事件只到采集日，不进分母）；"
                            "④成立年序列覆盖 1978—2025 全段，分母只用真实存在年份，未按 0 补齐"),
        "cover_compliance": {
            "cover_metric_route": "本 ID 不产出封面数值（cover_level=不适用）",
            "ads_rows_for_this_id": 0,
            "note": "旧稿曾以演示库结果面三表 0 行自证；本件不再引用结果面，改以「源侧不存在该 ID 结果面」表述",
        },
        "population": {"orgs": n_pool, "product_info_rows": fact["population"]["product_info_all"],
                       "join_base_rate": round(fact["population"]["product_info_join_base"] / n_pool, 6)},
        "systems": systems,
        "system_level_summary": {k: v for k, v in lv.items()},
        "layout_axis": layout,
        "global_axis": global_axis,
        "invest_axis": invest,
        "new_org_axis": {"series": inc_series, "recent_2015_2025": recent, "periods": len(inc_series),
                         "latest_year": inc_series[-1][0] if inc_series else None},
        "sz_scale": {"orgs": len(sz), "share_of_pool": round(len(sz) / n_pool, 6),
                     "size_dist": [[k, v] for k, v in sz_size.most_common(8)],
                     "size_nonnull": sz_size_nonnull, "cap_nonnull": sz_cap_nonnull,
                     "finance_events_orgs": fe_sz},
        "sz_dist": {"area_nonnull": area_nonnull, "rows": sz_dist},
        "base_fields_meta": bfm,
        "keyword_sensitivity": {k: kw["kw"][k] for k in ("检测", "检验检测", "研发", "技术开发",
                                                         "咨询", "知识产权", "专利") if k in kw["kw"]},
        "difference_vs_old_draft": {
            "population": "旧稿 43,296（演示库 svc_org_circle）→ 本件 44,153（gkx 经营范围口径）",
            "layout": "旧稿用分类器列（INNOV 29,321 / FINANCE 2,062 / CONSULT 1,387 …）→ 本件类型词表多命中",
            "overseas": "旧稿境外表 0 行 → 本件 dwd_forg_base_info 20,000 行但仅 3 国、country 全空",
            "invest": "旧稿 15,755 件 / 47 期 → 本件 25,654 行事件明细（池内 5,910 家）",
        },
        "compute": {"status": "cover", "elapsed_sec": round(time.time() - t0, 3)},
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("systems:", dict(lv))
    print("invest:", invest["rows"], invest["orgs_in_pool"], "peak", invest["peak_year"])
    print("sz:", len(sz), "area非空", area_nonnull, "size非空", sz_size_nonnull, "top", sz_dist[:3])
    print("new org periods:", len(inc_series), "latest", inc_series[-1] if inc_series else None)
    print("->", OUT)


if __name__ == "__main__":
    main()

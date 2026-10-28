#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_STAR_BASIC_INFO 明星企业基础画像 —— gkx 复现（2026-10-22）

口径：
    名单 = 明星企业（门户 CMS 人工名单为唯一合法真源）。
    画像 = 名单内每家企业的属地 / 行业 / 规模 / 技术四组字段。
    本件在 gkx 无 CMS 名单表的前提下，用「专利授权数 ≥ 50 且能精确匹配到底册」造代理名单，
    全部输出标注 proxy_roster=true，不与 CMS 名单混称。

输入（全部本目录）：
    code/_snapshots21/star_roster_gkx_20261021.json   代理名单 4,561 家（专利授权≥50，已剔非企业 163）
    code/_snapshots21/star_profile_20261022.json      4,561 家的底册画像 + 财务 + 技术标签（按 org_id 分块拉取）
    _work_gkx21/GKX_INVENTORY.json                    280 张表名，用于证明无序表

输出：code/M_ENT_STAR_BASIC_INFO_out.json
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "M_ENT_STAR_BASIC_INFO_out.json"
SNAP = HERE / "_snapshots21"
BASE_TOTAL = 189116


def share(n, d):
    return round(n / d * 100, 4) if d else None


def main():
    roster = json.load(open(SNAP / "star_roster_gkx_20261021.json", encoding="utf-8"))
    prof = json.load(open(SNAP / "star_profile_20261022.json", encoding="utf-8"))
    rows = prof["rows"]
    n = len(rows)

    inv = json.load(open(ROOT / "_work_gkx21" / "GKX_INVENTORY.json", encoding="utf-8"))
    star_hits = sorted(t for t in inv if any(k in t.lower() for k in ("star", "honor", "award", "recogni")))

    prov = Counter(r["province"] for r in rows)
    city = Counter(r["city"] for r in rows)
    ind1 = Counter(r["industry_l1_name"] for r in rows)
    ind2 = Counter(r["industry_l2_name"] for r in rows)
    otype = Counter(r["org_type"] for r in rows)
    size = Counter(r["org_size"] for r in rows)

    def cap_ok(r):
        v = r.get("registered_capital_value")
        try:
            return v is not None and float(v) > 0
        except Exception:
            return False

    def rev_of(r):
        for k in ("stock_latest", "fin_latest"):
            d = r.get(k) or {}
            v = d.get("operating_revenue")
            if v is not None and float(v) > 0:
                return float(v), k
        return None, None

    def emp_of(r):
        for k in ("stock_latest", "fin_latest"):
            d = r.get(k) or {}
            v = d.get("employees_number")
            try:
                if v is not None and float(v) > 0:
                    return int(float(v))
            except Exception:
                pass
        return None

    rev_rows = [(r, *rev_of(r)) for r in rows]
    rev_pos = [x for x in rev_rows if x[1] is not None]
    emp_pos = [r for r in rows if emp_of(r) is not None]

    emp_any_n = sum(1 for r in rows if r.get("emp_any_year"))
    rev_any_n = sum(1 for r in rows if r.get("rev_any_year"))
    rd_any_n = sum(1 for r in rows if r.get("rd_any_year"))
    rd_pos = [r for r in rows if (r.get("stock_latest") or {}).get("research_development_amount")
              not in (None, "", "None") and float((r.get("stock_latest") or {}).get("research_development_amount") or 0) > 0]

    grants = sorted(r["grant_cnt"] for r in rows)
    gsum = sum(grants)

    fill = {
        "industry_l1_name": sum(1 for r in rows if r.get("industry_l1_name")),
        "industry_l2_name": sum(1 for r in rows if r.get("industry_l2_name")),
        "province": sum(1 for r in rows if r.get("province")),
        "city": sum(1 for r in rows if r.get("city") and r["city"] != "NULL"),
        "area": sum(1 for r in rows if r.get("area")),
        "incorporation_date": sum(1 for r in rows if r.get("incorporation_date")),
        "registered_capital_gt0": sum(1 for r in rows if cap_ok(r)),
        "org_size": sum(1 for r in rows if r.get("org_size")),
        "reg_status": sum(1 for r in rows if r.get("reg_status")),
        "operating_revenue_gt0": len(rev_pos),
        "employees_gt0": len(emp_pos),
        "rd_amount_gt0": len(rd_pos),
        "tech_tag_ge1": sum(1 for r in rows if r.get("tags")),
        "operating_revenue_any_year": rev_any_n,
        "employees_any_year": emp_any_n,
        "rd_amount_any_year": rd_any_n,
    }
    fill_pct = {k: share(v, n) for k, v in fill.items()}

    top10 = sorted(rows, key=lambda r: -r["grant_cnt"])[:10]

    payload = {
        "metric_id": "M_ENT_STAR_BASIC_INFO",
        "metric_name_zh": "明星企业基础画像",
        "generated_for": "20261021 批 B-sample",
        "source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）",
        "support_judgment": "部分支持",
        "support_reason": ("gkx 280 张表无任何 star/honor/award/recogni 语义表，明星名单只能用"
                           "「专利授权≥50」造代理；画像的属地/行业/成立年/规模字段近满覆盖，"
                           "但营收 11.66%、员工 6.64%，规模画像基本空白。"),
        "proxy_roster": True,
        "proxy_roster_rule": "专利授权数 >= 50 且 name_cn 精确匹配 dwd_org_base_info，剔除高校/科研院所 163 家",
        "probes": {
            "table_name_scan": {"total_tables": len(inv), "star_honor_award_hits": star_hits,
                                "hit_count": len(star_hits)},
            "roster": {
                "n_patent_names": roster["n_patent_names"],
                "n_candidates_ge50": roster["n_candidates_ge50"],
                "n_excluded_non_enterprise": roster["n_excluded_non_enterprise"],
                "n_star": roster["n_star"],
                "threshold_grant": roster["threshold_grant"],
                "share_of_base_pct": share(roster["n_star"], BASE_TOTAL),
            },
            "profile_fill": fill,
            "profile_fill_pct": fill_pct,
            "revenue_source_split": {
                "stock_only": sum(1 for r, v, k in rev_rows if k == "stock_latest"),
                "fin_only": sum(1 for r, v, k in rev_rows if k == "fin_latest"),
                "total": len(rev_pos),
            },
        },
        "roster_share_of_base_pct": share(n, BASE_TOTAL),
        "province_top": prov.most_common(6),
        "city_top": city.most_common(6),
        "city_covered_count": len(city),
        "dawan_qu_share_pct": share(sum(v for k, v in city.items() if k in ("深圳市", "广州市", "东莞市", "惠州市")), n),
        "industry_l1_top": ind1.most_common(10),
        "industry_l2_top": ind2.most_common(8),
        "org_type_top": otype.most_common(6),
        "org_size_dist": size.most_common(8),
        "grant_stats": {
            "min": grants[0], "median": grants[len(grants) // 2],
            "mean": round(gsum / n, 2), "max": grants[-1], "sum": gsum,
            "ge100": sum(1 for g in grants if g >= 100),
            "ge1000": sum(1 for g in grants if g >= 1000),
        },
        "top10_by_grant": [{"name": r["name_cn"], "city": r["city"], "grant_cnt": r["grant_cnt"],
                            "pub_cnt": r["pub_cnt"], "industry_l2": r["industry_l2_name"]} for r in top10],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面件：名单为当期专利聚合快照（2021—2026 申请年），画像字段取各企业"
                            "最新可得财务年，不做年度序列，故不设基期；"
                            "财务覆盖率低（营收 11.66%）本身就是结论，不用早期年份补零。"),
        "custom_thresholds": {
            "star_grant_threshold": 50,
            "note": "阈值 50 沿用 star_roster_gkx_20261021.json 的构建口径，非甲方 CMS 定义，待甲方确认。",
        },
    }
    json.dump(payload, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: payload[k] for k in ("roster_share_of_base_pct", "probes", "grant_stats")},
                     ensure_ascii=False, indent=1)[:2000])
    print("->", OUT)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_STAR_BY_REGION 明星企业区域分布（20261022 改源版 · 只用三方库 gkx）

依赖代理名单缓存 `code/_snapshots21/star_roster_gkx_20261021.json`（由
`_star_roster_gkx.py` 在三方库 `gkx` 上现算：`gkx.dwd_patent` 按
`first_applicant_name` 聚合授权数、与 `gkx.dwd_org_base_info.name_cn` 等值匹配，
`grant_cnt >= 50` 入选并剔除高校/科研/医院）。属地字段取自
`gkx.dwd_org_base_info` 的 province / city / area（真实工商登记地）。

口径、阈值、集中度与 lift 公式与 20261020 版完全一致；改源只改取数端：
区县与底册分母都来自同一份 gkx 主档快照，不再分次回查数据库。

输出：code/M_ENT_STAR_BY_REGION_out.json
"""
import json
import os
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "M_ENT_STAR_BY_REGION_out.json")
ROSTER = os.path.join(HERE, "_snapshots21", "star_roster_gkx_20261021.json")
BASE = os.path.join(HERE, "_snapshots21", "star_base_rows_gkx.json")
M = "M_ENT_STAR_BY_REGION"
THRESHOLD = 50
NON_ENT_TYPE = {"事业单位", "民办非企业单位", "社会团体", "机关", "基金会", "群众团体"}
NON_ENT_RX = ("大学", "学院", "研究院", "研究所", "医院", "学校", "协会", "基金会")

out = {
    "metric_id": M,
    "metric_name": "明星企业区域分布",
    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "definition": "明星企业（代理）= 真实专利授权数≥50 的企业；区域 = gkx.dwd_org_base_info.province/city",
    "data_source": "gkx（三方库只读）：dwd_patent × dwd_org_base_info",
    "probes": {},
    "compute": {},
    "samples": {},
    "support_judgment": None,
    "reasons": [],
}


def load_stars():
    with open(ROSTER, encoding="utf-8") as f:
        payload = json.load(f)
    rows = payload["rows"]
    stars = [r for r in rows if (r.get("grant_cnt") or 0) >= THRESHOLD]
    stars = [r for r in stars
             if (r.get("org_type") not in NON_ENT_TYPE)
             and not any(k in (r.get("name_cn") or "") for k in NON_ENT_RX)]
    return stars, payload


def hhi(counts, total):
    return round(sum((c / total) ** 2 for c in counts), 5) if total else None


def main():
    stars, roster = load_stars()
    total = len(stars)

    prov, city, dist_area = {}, {}, {}
    for r in stars:
        p = r.get("province")
        ct = r.get("city")
        if p:
            prov[p] = prov.get(p, 0) + 1
        if ct:
            city[ct] = city.get(ct, 0) + 1
        a = r.get("area")
        if a:
            dist_area[a] = dist_area.get(a, 0) + 1

    prov_d = sorted(prov.items(), key=lambda x: -x[1])
    city_d = sorted(city.items(), key=lambda x: -x[1])
    area_d = sorted(dist_area.items(), key=lambda x: -x[1])

    # 底册分母（同一 gkx 主档快照）
    with open(BASE, encoding="utf-8") as f:
        base = json.load(f)          # [org_id, name, province, city, area, l1, l2, org_type]
    base_total = len(base)
    base_prov_cnt = {}
    for r in base:
        p = r[2]
        if p is not None and p != "":
            base_prov_cnt[p] = base_prov_cnt.get(p, 0) + 1
    base_prov = sorted(base_prov_cnt.items(), key=lambda x: -x[1])[:8]

    out["probes"] = {
        "star_proxy_total": total,
        "star_with_province": sum(v for _, v in prov_d),
        "star_with_city": sum(v for _, v in city_d),
        "star_with_area": sum(v for _, v in area_d),
        "base_info_total": int(base_total),
        "roster_threshold_grant": roster.get("threshold_grant"),
        "roster_matched_orgs": roster.get("n_matched_orgs_dedup"),
        "roster_patent_agg_elapsed_sec": roster.get("patent_agg_elapsed_sec"),
        "source": "cache:_snapshots21/star_roster_gkx_20261021.json（由 gkx.dwd_patent × gkx.dwd_org_base_info 生成）",
        "coverage_disclosure": "底册 99.82% 在广东（深圳 50.55%/广州 26.23%/东莞 17.76%/惠州 5.28%），"
                               "省外样本不足 0.2%，全国名次不可解释，只可作省内/都市圈比较",
    }
    out["compute"] = {
        "province_distribution": [{"province": k, "n": v, "share_pct": round(v / total * 100, 2)}
                                  for k, v in prov_d],
        "city_top15": [{"city": k, "n": v, "share_pct": round(v / total * 100, 2)}
                       for k, v in city_d[:15]],
        "area_top10": [{"area": k, "n": v, "share_pct": round(v / total * 100, 2)}
                       for k, v in area_d[:10]],
        "concentration": {
            "hhi_city": hhi([v for _, v in city_d], total),
            "top1_city": city_d[0][0] if city_d else None,
            "top1_city_share_pct": round(city_d[0][1] / total * 100, 2) if city_d else None,
            "top3_city_share_pct": round(sum(v for _, v in city_d[:3]) / total * 100, 2) if total else None,
            "guangdong_share_pct": round(prov.get("广东省", 0) / total * 100, 2),
        },
        "vs_base_universe": [{
            "province": p,
            "base_n": int(n),
            "base_share_pct": round(int(n) / base_total * 100, 2),
            "star_n": prov.get(p, 0),
            "star_share_pct": round(prov.get(p, 0) / total * 100, 2),
        } for p, n in base_prov],
    }
    out["samples"] = {
        "top10_enterprises_shenzhen": [
            {"name": r["name_cn"], "city": r["city"], "industry_l1": r["industry_l1_name"],
             "grant_cnt": int(r["grant_cnt"])}
            for r in stars if r.get("city") == "深圳市"][:10],
        "top5_enterprises_other_cities": [
            {"name": r["name_cn"], "city": r["city"], "industry_l1": r["industry_l1_name"],
             "grant_cnt": int(r["grant_cnt"])}
            for r in stars if r.get("city") != "深圳市"][:5],
    }

    out["support_judgment"] = "部分支持"
    out["reasons"] = [
        f"区域分布可算：{total} 家代理明星企业，深圳占 {out['compute']['concentration']['top1_city_share_pct']}%，"
        f"Top3 城市占 {out['compute']['concentration']['top3_city_share_pct']}%，分布可解释。",
        "分子（明星名单）为专利阈值代理，与甲方 CMS 人工名单不等价，属地分布会随名单口径变化。",
        "底册 99.82% 在广东，省外不足 0.2%，「全国区域分布」不可解释，只能作深圳都市圈比较。",
        "工商注册地 ≠ 实际经营地（部分集团注册在深圳、生产在东莞/惠州），区域口径需甲方确认。",
    ]

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)
    print(json.dumps({k: out[k] for k in ("metric_id", "support_judgment", "compute")},
                     ensure_ascii=False, indent=1, default=str)[:2500])


if __name__ == "__main__":
    main()

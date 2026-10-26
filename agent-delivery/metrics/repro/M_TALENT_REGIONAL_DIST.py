#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TALENT_REGIONAL_DIST —— 重点人才区域分布（SRS 84/85）。

口径：区域不是库里的字段，而是机构名的文本推断（`_talent10_common.loc2`）。
五级顺序：高校名录精确 → 企业底册精确 → 高校名录前缀 → 企业底册前缀 → 城市名（取最右）；
分支校区（哈工大深圳、北大深圳医院）按最右城市名修正，中山大学回广州。
分母：有机构名且可定位的 18,069 人（20,829 − 2,760 未归属）。
领域对比：20+8 集群 × 城市，用区位商 LQ；门槛 n≥5。

零 SQL；产物 code/M_TALENT_REGIONAL_DIST_out.json。
"""
from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import _talent10_common as C  # noqa: E402

METRIC = "M_TALENT_REGIONAL_DIST"


def main() -> None:
    allrows = C.scholars_all()
    rows = [(r[0], (r[2] or "").strip()) for r in allrows if (r[2] or "").strip()]
    prov = Counter()
    city = Counter()
    how = Counter()
    for sid, org in rows:
        p, c, h = C.loc2(org)
        how[h] += 1
        prov[p] += 1
        city[c] += 1
    total = len(rows)
    unknown = prov.get("未归属", 0) + prov.get("未填", 0)
    locatable = total - unknown

    def dist(cnt, key, k=None, denom=total):
        items = cnt.most_common(k) if k else cnt.most_common()
        return [{key: a, "n": b, "share": C.share(b, denom)} for a, b in items]

    prov_list = dist(prov, "prov")
    city_list = dist(city, "city")
    city_counts = list(city.values())
    conc = {"cr3": C.cr(city_counts, 3), "cr10": C.cr(city_counts, 10),
            "hhi": C.hhi(city_counts), "gini": C.gini(city_counts),
            "units": len(city_counts), "prov_units": len(prov)}
    sz = {"n": city.get("深圳市", 0), "share": C.share(city.get("深圳市", 0), total),
          "share_locatable": C.share(city.get("深圳市", 0), locatable),
          "gd": prov.get("广东省", 0), "gd_share": C.share(prov.get("广东省", 0), total)}
    foreign = sum(n for p, n in prov.items() if p in ("海外",))

    # 领域 × 城市 LQ（只用有集群标签的面板行）
    panel = C.rows()
    cc = Counter((r["city"], c) for r in panel for c in r["cl"]
                 if r["city"] not in ("未归属", "未填"))
    ct = Counter()
    for (ci, cl), n in cc.items():
        ct[cl] += n
    ccity = Counter()
    for (ci, cl), n in cc.items():
        ccity[ci] += n
    top_cl = [k for k, _ in ct.most_common(10)]
    top_city = [k for k, _ in Counter(r["city"] for r in panel
                                      if r["city"] not in ("未归属", "未填")).most_common(10)]
    lq = []
    for ci in top_city:
        for cl in top_cl:
            n = cc.get((ci, cl), 0)
            if n < 5:
                continue
            s_c = n / ccity[ci] if ccity[ci] else 0
            s_a = ct[cl] / sum(ct.values()) if sum(ct.values()) else 0
            lq.append({"city": ci, "cluster": cl, "n": n,
                       "city_share": round(100 * s_c, 2),
                       "all_share": round(100 * s_a, 2),
                       "lq": round(s_c / s_a, 4) if s_a else None})
    lq.sort(key=lambda x: -x["lq"])

    payload = {
        "support_judgment": "部分支持",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面指标，无年度序列；机构属地由机构名推断，无「期初/期末」可比",
        "scope": {"universe": "dwd_scholar 全表 21,316 行", "denominator_global": total,
                  "denominator_locatable": locatable, "unit": "scholar_id 去重"},
        "coverage": {"org_filled": total, "locatable": locatable,
                     "locatable_share": C.share(locatable, total),
                     "unmatched": unknown, "unmatched_share": C.share(unknown, total),
                     "foreign": foreign, "method": dict(how)},
        "province": prov_list,
        "city": city_list,
        "concentration": conc,
        "shenzhen": sz,
        "city_cluster_lq": lq[:40],
        "data_quality": {
            "no_field": "dwd_scholar 27 列无 province / city / country，区域全部是机构名推断",
            "branch_fix": "分支校区按最右城市名修正；loc() 原逻辑会把哈工大（深圳）判回哈尔滨",
            "unmatched": f"{unknown:,} 人（{C.share(unknown, total)}%）机构名不含可识别地名，"
                         "且不在高校名录/企业底册，按不可定位处理，不摊入任何城市",
            "sample_skew": "可定位样本中深圳都市圈（深广莞惠）占绝对多数吗？见 §三 3.3；"
                           "本库是论文作者库，企业研发人员缺位",
            "district": "区县级粒度不可得（机构名不含区县的比例高），两跳停",
        },
        "diff_vs_old_draft": {
            "old": "旧稿 20,390/20,829=97.89% 可定位、深圳 194 人（0.91%）",
            "now": f"{locatable:,}/{total:,}={C.share(locatable, total)}% 可定位、深圳 {sz['n']} 人"
                   f"（{sz['share']}%）",
            "why": "旧稿用了 200+ 条机构白名单（把「中国科学院」直接判北京等），本件不维护白名单，"
                   "改用高校名录 3,501 行 + 最右城市名；可定位率因此下降，但每条归属可复核。"
                   "深圳人数上升是因为分支校区修正（哈工大深圳等 24 人）与南方科技大学等 55 人入深圳",
        },
        "findings": [
            f"可定位 {locatable:,} 人（{C.share(locatable, total)}%），未归属 {unknown:,} 人"
            f"（{C.share(unknown, total)}%）",
            f"城市 CR3={conc['cr3']}%、CR10={conc['cr10']}%、HHI={conc['hhi']}（170 个城市单元）",
            f"深圳 {sz['n']} 人（{sz['share']}%），广东 {sz['gd']} 人（{sz['gd_share']}%）",
        ],
    }
    C.write(METRIC, payload)
    print("coverage", payload["coverage"])
    print("prov top", prov_list[:8])
    print("city top", city_list[:10])
    print("conc", conc, "sz", sz)
    print("lq top", lq[:8])


if __name__ == "__main__":
    main()

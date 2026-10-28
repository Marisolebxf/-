#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_TALENT_ORG_DIST —— 重点人才机构分布（SRS 86/87）。

口径：机构 = `dwd_scholar.scholar_org_name_zh` 原串（不合并分校/别名），
人数 = 该串下的 scholar_id 去重计数，分母 = 有机构名的 20,829 人。
类型 = 高校名册（3,501 行）优先 + 名称规则五分类；属地 = `loc2`（分支校区修正）。
集中度用 CR5/CR10/CR50、HHI（份额平方和 ×10⁴）与 Gini。

零 SQL：只读 `probe_a26_20261022.json` / `heis21_20261022.json` / `talent22_panel`。
产物：code/M_TALENT_ORG_DIST_out.json
"""
from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import _talent10_common as C  # noqa: E402

METRIC = "M_TALENT_ORG_DIST"


def main() -> None:
    allrows = C.scholars_all()
    named = [r for r in allrows if (r[1] or "").strip()]
    org_rows = [(r[0], (r[1] or "").strip(), (r[2] or "").strip()) for r in allrows
                if (r[2] or "").strip()]
    total = len(org_rows)
    cnt = Counter(o for _, _, o in org_rows)
    meta = {o: (C.org_type(o), C.loc2(o)) for o in cnt}

    def bundle(items):
        return [{"org": o, "type": meta[o][0], "prov": meta[o][1][0], "city": meta[o][1][1],
                 "n": n, "share": C.share(n, total)} for o, n in items]

    top = bundle(cnt.most_common(30))
    by_type = Counter()
    type_orgs = defaultdict(list)
    for o, n in cnt.items():
        by_type[meta[o][0]] += n
        type_orgs[meta[o][0]].append((o, n))
    types = [{"type": t, "n": n, "share": C.share(n, total), "orgs": len(type_orgs[t])}
             for t, n in by_type.most_common()]
    type_top = {t: bundle(sorted(type_orgs[t], key=lambda x: -x[1])[:8])
                for t in type_orgs}

    vals = list(cnt.values())
    sing = sum(1 for v in vals if v == 1)
    conc = {"cr5": C.cr(vals, 5), "cr10": C.cr(vals, 10), "cr50": C.cr(vals, 50),
            "hhi": C.hhi(vals), "gini": C.gini(vals),
            "organizations": len(cnt), "singletons": sing,
            "singleton_share": C.share(sing, len(cnt)),
            "median_per_org": C.pctl(vals, 0.5), "max_per_org": max(vals)}

    # 深圳子集
    sz_orgs = [(o, n) for o, n in cnt.items() if C.is_sz_org(o)]
    sz_n = sum(n for _, n in sz_orgs)
    sz = {"orgs": len(sz_orgs), "scholars": sz_n, "share": C.share(sz_n, total),
          "top": bundle(sorted(sz_orgs, key=lambda x: -x[1])[:10])}

    # 院士子集（重点人才），只覆盖属性宇宙里能对齐的 80 人
    acad_ids = set(C.load("talent_flag_20261022.json")["scholar_ids"])
    acad_rows = [(r[0], (r[2] or "").strip(), (r[1] or "").strip()) for r in allrows
                 if r[0] in acad_ids and (r[2] or "").strip()]
    ac = Counter(o for _, o, _ in acad_rows)
    acad = {"n": len(acad_rows), "orgs": len(ac), "top": bundle(ac.most_common(10)),
            "note": "院士标识只在 dwd_scholar_talent_flag（20,030 行），与主档 21,316 的"
                    " scholar_id 交集使可定位者仅 80 人；这不是深圳院士数，是库内可对齐数"}

    # 与旧稿的差异（旧稿口径用演示库同结构表，数字按本件重算）
    old = {"scope": "旧稿 20,829 人有机构、2,084 个机构、CR10 18.07%、HHI 72.0",
           "now": "20,829 人有机构、2,108 个机构、CR10 18.07%、HHI 71.7",
           "why": "总人数一致，机构串去重数多 24 个（2,108 vs 2,084）——本件不做机构别名合并，"
                  "保留原串；HHI 差 0.3 由这 24 个单例机构摊薄"}

    payload = {
        "support_judgment": "完全转换支持",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面指标：dwd_scholar 为当前主档快照，无年度序列；"
                           "需求提到的「环比增长率」需第二期快照，本件不产出（见 §四 4.1）",
        "scope": {"universe": "dwd_scholar 全表 21,316 行", "unit": "scholar_id 去重",
                  "denominator": "有机构名的 20,829 人", "name_filled": len(named)},
        "coverage": {"scholar_rows": len(allrows), "org_filled": total,
                     "org_share": C.share(total, len(allrows)),
                     "distinct_org": len(cnt), "name_filled": len(named),
                     "org_id_filled": 0},
        "type_dist": types,
        "concentration": conc,
        "top_orgs": top,
        "type_top": type_top,
        "shenzhen": sz,
        "academicians": acad,
        "data_quality": {
            "org_id": "dwd_scholar.scholar_org_id 非空 0 行 —— 机构无主键，同名多校区不可分",
            "branch_campus": "哈工大（深圳）/北大深圳医院等 24 人按最右城市名修正为深圳市",
            "alias_merge": "未合并「中国科学院××研究所」到「中国科学院」；上卷会改变 CR10",
            "growth": "无历史快照，环比增长率不可算",
        },
        "diff_vs_old_draft": old,
        "findings": [
            f"高校占 {types[0]['share']}%（{types[0]['n']:,} 人），企业仅 "
            f"{next(t['n'] for t in types if t['type']=='企业'):,} 人——这是学术人才库，不是产业人才库",
            f"CR10={conc['cr10']}%、CR50={conc['cr50']}%、HHI={conc['hhi']}（低集中），"
            f"{sing:,} 个机构只有 1 人（{conc['singleton_share']}%）",
            f"深圳子集 {sz_n} 人 / {len(sz_orgs)} 个机构，占全库 {sz['share']}%",
        ],
    }
    C.write(METRIC, payload)
    print("type", types)
    print("conc", conc)
    print("sz", sz["orgs"], sz["scholars"], sz["share"])
    print("acad", acad["n"], acad["orgs"])
    print("top5", [(x["org"], x["n"]) for x in top[:5]])


if __name__ == "__main__":
    main()

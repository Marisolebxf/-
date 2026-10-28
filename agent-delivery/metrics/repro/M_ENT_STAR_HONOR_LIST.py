#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_STAR_HONOR_LIST 明星企业荣誉清单 —— gkx 复现（2026-10-22）

口径：
    清单对象 = 「明星企业 × 荣誉项」两级结构。
    明星企业：门户 CMS 人工名单为唯一合法真源；gkx 无该表，本件用专利授权≥50 的代理名单（4,561 家）。
    荣誉项：官方认定类资质（高企/科技型中小/创新型中小/专精特新/小巨人/单项冠军/独角兽瞪羚/
            知识产权优势示范/研发机构/创新平台），来源 gkx.dwd_org_tech_tag。

为什么只能叫「资质清单」而不是「荣誉清单」：
    gkx 280 张表里没有任何 star / honor / award / recogni 语义表（见 probes.table_name_scan），
    dwd_org_tech_tag 的 55 类标签全部是「认定/资质」，没有一类是获奖类（科技进步奖、专利奖等）。
    正文与产物都按「资质认定」表述，不把资质说成获奖。

输入：
    code/_snapshots21/tech_tags_20261021.json        32,322 家机构 × 55 类标签（202,424 行）
    code/_snapshots21/star_profile_20261022.json     4,561 家代理名单 + 技术标签

输出：code/M_ENT_STAR_HONOR_LIST_out.json
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "M_ENT_STAR_HONOR_LIST_out.json"
SNAP = HERE / "_snapshots21"
BASE_TOTAL = 189116

CATEGORY = [
    ("高企", ("高新技术企业",)),
    ("科技型中小企业", ("科技型中小企业",)),
    ("创新型中小企业", ("创新型中小企业",)),
    ("专精特新中小企业", ("专精特新中小企业",)),
    ("小巨人", ("小巨人",)),
    ("制造业单项冠军", ("单项冠军",)),
    ("独角兽/瞪羚/隐形冠军", ("独角兽", "瞪羚", "隐形冠军", "雏鹰")),
    ("知识产权优势/示范", ("知识产权",)),
    ("研发机构", ("工程技术研究中心", "企业技术中心")),
    ("创新平台/载体", ("孵化器", "众创空间")),
    ("其他示范类", ("技术先进型服务", "技术创新示范", "科改示范", "民营科技")),
]


def cat_of(tag: str) -> str:
    for name, keys in CATEGORY:
        if any(k in tag for k in keys):
            return name
    return "未归并"


def level_of(tag: str) -> str:
    if tag.startswith("国家级"):
        return "国家级"
    if tag.startswith("省级"):
        return "省级"
    if tag.startswith("曾获国家级"):
        return "国家级(曾获)"
    if tag.startswith("曾获省级"):
        return "省级(曾获)"
    return "未标级别"


def share(n, d):
    return round(n / d * 100, 4) if d else None


def main():
    tags_map = json.load(open(SNAP / "tech_tags_20261021.json", encoding="utf-8"))
    prof = json.load(open(SNAP / "star_profile_20261022.json", encoding="utf-8"))
    rows = prof["rows"]

    inv = json.load(open(ROOT / "_work_gkx21" / "GKX_INVENTORY.json", encoding="utf-8"))
    star_hits = sorted(t for t in inv if any(k in t.lower() for k in ("star", "honor", "award", "recogni")))

    all_rows = sum(len(v) for v in tags_map.values())
    all_tags = Counter(t for v in tags_map.values() for t in v)

    roster_tagged = [r for r in rows if r.get("tags")]
    n_roster = len(rows)
    roster_tags = Counter(t for r in roster_tagged for t in r["tags"])
    per_firm = sorted(len(r["tags"]) for r in roster_tagged)

    cat_all = Counter()
    for t, c in all_tags.items():
        cat_all[cat_of(t)] += c
    cat_roster = Counter()
    for t, c in roster_tags.items():
        cat_roster[cat_of(t)] += c

    lv_all = Counter()
    for t, c in all_tags.items():
        lv_all[level_of(t)] += c
    lv_roster = Counter()
    for t, c in roster_tags.items():
        lv_roster[level_of(t)] += c

    hist_all = sum(c for t, c in all_tags.items() if t.startswith("曾获"))
    hist_roster = sum(c for t, c in roster_tags.items() if t.startswith("曾获"))
    stale_all = sum(c for t, c in all_tags.items() if "过期待复核" in t)
    stale_roster = sum(c for t, c in roster_tags.items() if "过期待复核" in t)

    # 明星子集在各类资质上的「家数 / 全市-全库家数」
    tag_orgs_all = {t: c for t, c in all_tags.items()}

    top_roster = roster_tags.most_common(15)
    zero_examples = [r["name_cn"] for r in rows if not r.get("tags")][:8]

    payload = {
        "metric_id": "M_ENT_STAR_HONOR_LIST",
        "metric_name_zh": "明星企业荣誉清单",
        "generated_for": "20261021 批 B-sample",
        "source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）.dwd_org_tech_tag × dwd_org_base_info",
        "support_judgment": "部分支持",
        "support_reason": ("资质维真实且足量（202,424 行 / 55 类 / 32,322 家），但「明星企业」范围维"
                           "在 gkx 无表，只能用专利授权≥50 的代理名单；且 55 类标签全是认定资质、"
                           "无获奖类荣誉 → 内容侧可算、范围与语义侧有缺口。"),
        "proxy_roster": True,
        "honor_semantics": "qualification_only",
        "probes": {
            "table_name_scan": {"total_tables": len(inv), "star_honor_award_hits": star_hits,
                                "hit_count": len(star_hits)},
            "tech_tag_table": {
                "rows": all_rows,
                "orgs": len(tags_map),
                "distinct_tags": len(all_tags),
                "share_of_base_pct": share(len(tags_map), BASE_TOTAL),
            },
            "roster_join": {
                "roster_total": n_roster,
                "roster_with_tag": len(roster_tagged),
                "roster_without_tag": n_roster - len(roster_tagged),
                "join_rate_pct": share(len(roster_tagged), n_roster),
            },
            "per_firm": {
                "median": per_firm[len(per_firm) // 2] if per_firm else 0,
                "mean": round(sum(per_firm) / len(per_firm), 4) if per_firm else 0,
                "max": per_firm[-1] if per_firm else 0,
                "min": per_firm[0] if per_firm else 0,
            },
            "history_tags": {"all_rows": hist_all, "roster_rows": hist_roster},
            "stale_tags": {"all_rows": stale_all, "roster_rows": stale_roster},
        },
        "category_all_rows": dict(cat_all.most_common()),
        "category_roster_rows": dict(cat_roster.most_common()),
        "level_all_rows": dict(lv_all.most_common()),
        "level_roster_rows": dict(lv_roster.most_common()),
        "top_tags_roster": [{"tag": t, "orgs": c, "share_of_roster_pct": share(c, n_roster)}
                            for t, c in top_roster],
        "top_tags_all": [{"tag": t, "orgs": c, "share_of_all_tagged_pct": share(c, len(tags_map))}
                         for t, c in all_tags.most_common(15)],
        "tag_orgs_all": tag_orgs_all,
        "roster_without_tag_examples": zero_examples,
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面件：dwd_org_tech_tag 无年份列（只有 created_time/updated_time），"
                            "资质本身也不带年度窗口，故不设基期；不得用 updated_time 反推「当年新增」，"
                            "那是入库时间不是认定时间。"),
        "custom_thresholds": {
            "star_grant_threshold": 50,
            "note": "明星范围沿用专利授权≥50 的代理口径；若甲方坚持 CMS 名单为唯一范围口径，本件应降为完全不支持。",
        },
    }
    json.dump(payload, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({"probes": payload["probes"], "category_roster": payload["category_roster_rows"],
                      "level_roster": payload["level_roster_rows"]}, ensure_ascii=False, indent=1)[:2500])
    print("->", OUT)


if __name__ == "__main__":
    main()

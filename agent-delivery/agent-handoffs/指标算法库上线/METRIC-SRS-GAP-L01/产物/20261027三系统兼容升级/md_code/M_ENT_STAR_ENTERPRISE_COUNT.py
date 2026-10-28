#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_STAR_ENTERPRISE_COUNT · 明星企业数（gkx 口径，零 DB）

calc-logic（gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_STAR_ENTERPRISE_COUNT.md）：
    本条 = COUNT(DISTINCT enterprise_code) FROM star_roster_item WHERE 只收已发布
    名单真源在门户 CMS（久新只读契约），项目 DWD 无独立名单结果表。
    calc-logic 明文禁止：拿「专利≥50」/ `enterprise_tag.tag_code='star_enterprise'` /
    荣誉名含「明星」/ TopN 当作明星企业。

本脚本交付的是**代理名单计数**，不是 CMS 计数：
    口径 = gkx.dwd_patent 按 first_applicant_name 聚合出 grant_cnt（granted_number 非空），
    与 gkx.dwd_org_base_info.name_cn 等值匹配，剔除高校/科研/医院等非企业主体，
    取 grant_cnt >= 50。该口径与 STAR 簇已交付件（M_ENT_STAR_BY_REGION / M_ENT_STAR_RD_RATIO）
    共用同一份快照 code/_snapshots21/star_roster_gkx_20261021.json（4,561 家），保证跨件一致。

本脚本不连数据库：只读 code/_snapshots21/ 下的落盘快照，重跑 < 10 秒。
产物：code/M_ENT_STAR_ENTERPRISE_COUNT_out.json

运行：cd code && python3 M_ENT_STAR_ENTERPRISE_COUNT.py
"""
from __future__ import annotations

import json
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
ROOT = HERE.parent
OUT = HERE / "M_ENT_STAR_ENTERPRISE_COUNT_out.json"
METRIC_ID = "M_ENT_STAR_ENTERPRISE_COUNT"

ROSTER = SNAP / "star_roster_gkx_20261021.json"
BASE = SNAP / "base_20261021.json"
AGG = SNAP / "star_applicant_agg_gkx.json"
STAR_BASE = SNAP / "star_base_rows_gkx.json"
TECH_TAG = SNAP / "tech_tags_20261021.json"
INVENTORY = ROOT / "_work_gkx21" / "GKX_INVENTORY.json"

# calc-logic 指定的名单真源表（CMS 契约表），用于证明 gkx 侧无此表
CMS_TABLES = ["star_roster_item", "ent_star_roster_count", "enterprise_star"]
# 库内同义/易混表名，逐一核过才能写「两库均无」
SYNONYM_PATTERNS = ["star", "roster", "cms", "key_enterprise", "enterprise_tag", "honor"]

NON_ENT_TYPE = {"事业单位", "民办非企业单位", "社会团体", "机关", "基金会", "群众团体"}
NON_ENT_RX = ("大学", "学院", "研究院", "研究所", "医院", "学校", "协会", "基金会")


def pct(num: int, den: int) -> float:
    """比例一律落分子分母，正文只引用这里的值（v6 §三）。"""
    return round(num / den * 100, 4) if den else 0.0


def dist(values: list[str]) -> dict:
    c = Counter(values)
    total = sum(c.values())
    return {k: {"count": v, "pct": pct(v, total)} for k, v in c.most_common()}


def stat_block(values: list[int]) -> dict:
    v = sorted(values)
    n = len(v)

    def q(p: float) -> int:
        return v[min(n - 1, int(round(p * (n - 1))))]

    return {
        "n": n,
        "sum": sum(v),
        "mean": round(sum(v) / n, 4),
        "median": q(0.5),
        "p75": q(0.75),
        "p90": q(0.90),
        "p95": q(0.95),
        "p99": q(0.99),
        "min": v[0],
        "max": v[-1],
    }


def is_non_enterprise(name: str, org_type: str) -> bool:
    return (org_type or "") in NON_ENT_TYPE or any(x in name for x in NON_ENT_RX)


def main() -> None:
    roster = json.loads(ROSTER.read_text(encoding="utf-8"))
    rows = roster["rows"]
    base = json.loads(BASE.read_text(encoding="utf-8"))
    agg = json.loads(AGG.read_text(encoding="utf-8"))
    sb = json.loads(STAR_BASE.read_text(encoding="utf-8"))
    tags = json.loads(TECH_TAG.read_text(encoding="utf-8"))
    inv = json.loads(INVENTORY.read_text(encoding="utf-8"))

    n_star = len(rows)
    n_base = len(base)
    threshold = int(roster["threshold_grant"])
    n_candidates = int(roster["n_candidates_ge50"])
    n_excluded = int(roster["n_excluded_non_enterprise"])

    # ---- 名单主体分布（产品侧「共 N 家」的下钻维度）
    city = dist([r["city"] or "（空）" for r in rows])
    province = dist([r["province"] or "（空）" for r in rows])
    ind1 = dist([r["industry_l1_name"] or "（空）" for r in rows])
    ind2 = dist([r["industry_l2_name"] or "（空）" for r in rows])
    ind2_top = [{"name": k, "count": v["count"], "pct": v["pct"]}
                for k, v in list(ind2.items())[:10]]

    grant = stat_block([int(r["grant_cnt"]) for r in rows])
    pub = stat_block([int(r["pub_cnt"]) for r in rows])

    # ---- 阈值敏感性：名单口径唯一可变参数是 grant>=N，必须把曲线交出来
    agg_map = agg["agg"]
    curve = []
    for th in (20, 30, 50, 80, 100, 200, 500):
        sel = [r for r in sb if r[1] in agg_map and agg_map[r[1]][1] >= th
               and not is_non_enterprise(r[1], r[7])]
        curve.append({"threshold": th, "count": len(sel),
                      "pct_of_base": pct(len(sel), n_base),
                      "ratio_to_50": round(len(sel) / n_star, 4) if n_star else None})
    # 主口径阈值必须在曲线里逐字对上（防配置写死，§3.39）
    assert next(x for x in curve if x["threshold"] == threshold)["count"] == n_star

    # ---- 名单与快照的一致性对账（跨件一致性的硬证据）
    roster_ids = {r["org_id"] for r in rows}
    recomputed = {r[0] for r in sb if r[1] in agg_map and agg_map[r[1]][1] >= threshold
                  and not is_non_enterprise(r[1], r[7])}
    sym_left, sym_right = sorted(roster_ids - recomputed), sorted(recomputed - roster_ids)

    # ---- CMS 侧否定性证据：gkx 280 张表里没有任何名单表
    name_hits = {p: sorted(k for k in inv if p in k.lower()) for p in SYNONYM_PATTERNS}
    cms_present = [t for t in CMS_TABLES if t in inv]
    # 荣誉/资质标签侧：唯一接近的「明星」类标签是否存在
    star_tag_orgs = sum(1 for v in tags.values() if any("明星" in t for t in v))
    unicorn_orgs = sum(1 for v in tags.values() if any("独角兽" in t for t in v))
    hidden_champ_orgs = sum(1 for v in tags.values() if any("隐形冠军" in t for t in v))

    area_missing = sum(1 for r in rows if not r["area"])
    out = {
        "metric_id": METRIC_ID,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "support_judgment": "部分支持",
        "judgment_reason": (
            "名单真源在门户 CMS（star_roster_item / ads.ent_star_roster_count），"
            "gkx 280 张表与 live 开发库均无该结果面；本件交付的是以专利授权数≥50 构造的"
            "代理名单计数，语义与 CMS 已发布名单不等价（calc-logic 明禁以此当明星）。"
            "计数本身可复算，但名单维度始终无源，故判部分支持。"
        ),
        "verdict_kind": "proxy_constructed",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "截面件：名单无年度字段，口径是「当前名单里有谁算谁」，不含年度序列；"
            "因此不设基期。代理名单依赖的专利快照覆盖 apdt_year 2021—2026，"
            "但本指标不用年份切分，2017—2020 零行不影响本读数。"
        ),
        "sources": [
            {"file": "code/_snapshots21/star_roster_gkx_20261021.json",
             "source": roster.get("source"), "generated_at": roster.get("generated_at"),
             "role": "代理名单 4,561 家（授权≥50）"},
            {"file": "code/_snapshots21/star_base_rows_gkx.json",
             "source": "gkx.dwd_org_base_info 全量 189,116 行（含 org_type/industry）",
             "role": "阈值敏感性与非企业主体剔除"},
            {"file": "code/_snapshots21/star_applicant_agg_gkx.json",
             "source": agg.get("source"), "role": "申请人 → [件数, 授权数]"},
            {"file": "code/_snapshots21/tech_tags_20261021.json",
             "source": "gkx.dwd_org_tech_tag 32,322 家机构标签",
             "role": "「荣誉标签能否顶替名单」的否定性证据"},
            {"file": "_work_gkx21/GKX_INVENTORY.json",
             "source": "gkx 280 表逐表 COUNT(*)（2026-10-22）",
             "role": "名单表是否存在"},
        ],
        "compute": {
            "proxy_threshold_grant": threshold,
            "roster_count": n_star,
            "n_candidates_ge50": n_candidates,
            "n_excluded_non_enterprise": n_excluded,
            "excluded_share_pct": pct(n_excluded, n_candidates),
            "share_of_base_pct": pct(n_star, n_base),
            "share_of_applicants_pct": pct(n_star, int(agg["names"])),
            "n_applicant_names": int(agg["names"]),
            "patent_rows": int(agg["table_rows"]),
            "base_rows": n_base,
            "n_cities": len(city),
            "base_province_top": [
                {"province": k, "count": v, "pct": pct(v, n_base)}
                for k, v in Counter(r[3] for r in base).most_common(5)
            ],
            "city_dist": city,
            "province_dist": province,
            "industry_l1_dist": ind1,
            "industry_l2_top10": ind2_top,
            "n_industry_l2": len(ind2),
            "grant_stats": grant,
            "pub_stats": pub,
            "grant_rate_pct": pct(grant["sum"], pub["sum"]),
            "grant_rate_library_pct": pct(sum(v[1] for v in agg_map.values()),
                                          int(agg["table_rows"])),
            "library_grant_rows": sum(v[1] for v in agg_map.values()),
            "library_share_pub_pct": pct(pub["sum"], int(agg["table_rows"])),
            "library_share_grant_pct": pct(grant["sum"], sum(v[1] for v in agg_map.values())),
            "matched_names": int(roster["n_matched_base_rows"]),
            "unmatched_names": int(agg["names"]) - int(roster["n_matched_base_rows"]),
            "name_match_pct": pct(int(roster["n_matched_base_rows"]), int(agg["names"])),
            "top4_industry_sum_pct": round(
                sum(v["pct"] for k, v in list(ind1.items())[:4]), 4),
            "mfg_wholesale_pct": round(
                ind1["制造业"]["pct"] + ind1["批发和零售业"]["pct"], 4),
            "tail4_count": sum(v["count"] for k, v in list(ind1.items())[-4:]),
            "tail4_pct": round(sum(v["pct"] for k, v in list(ind1.items())[-4:]), 4),
            "threshold_curve": curve,
            "area_missing_count": area_missing,
            "area_missing_pct": pct(area_missing, n_star),
            "reconcile": {
                "roster_org_ids": len(roster_ids),
                "recomputed_org_ids": len(recomputed),
                "only_in_roster": len(sym_left),
                "only_in_recompute": len(sym_right),
            },
            "cms_probe": {
                "cms_tables_declared": CMS_TABLES,
                "cms_tables_present_in_gkx": cms_present,
                "gkx_table_name_hits": name_hits,
                "star_tag_orgs": star_tag_orgs,
                "unicorn_tag_orgs": unicorn_orgs,
                "hidden_champion_tag_orgs": hidden_champ_orgs,
                "tech_tag_orgs": len(tags),
                "live_devdb_note": "本机开发库 gkxlumenx_dwd/ods/ads 逐表实测非空 0 张（空壳）",
            },
            "top10_by_grant": [
                {"name": r["name_cn"], "city": r["city"], "grant_cnt": int(r["grant_cnt"]),
                 "pub_cnt": int(r["pub_cnt"])}
                for r in sorted(rows, key=lambda x: -int(x["grant_cnt"]))[:10]
            ],
        },
        "notes": [
            "代理名单 ≠ CMS 名单：本条 4,561 是「授权≥50」的构造值，不是门户已发布名单。",
            "阈值换成 30 立刻变成 9,813 家、换成 100 变成 1,630 家，说明「共 N 家」完全由阈值决定。",
            "名单里 4,561 家 100% 在广东，省外 0 家——底册本身 99.82% 偏粤，不能外推全国。",
            "calc-logic 明禁 enterprise_tag.tag_code='star_enterprise' 与荣誉名含「明星」；"
            "库内 tech_tag 的「明星」命中为 0，其它荣誉标签（独角兽/隐形冠军）也不得顶替。",
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[OK] {METRIC_ID} roster={n_star} base={n_base} "
          f"cities={len(city)} cand={n_candidates} excl={n_excluded}")
    print(f"     out -> {OUT.name} ({OUT.stat().st_size} B)")


if __name__ == "__main__":
    main()

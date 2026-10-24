#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TECH_DEEP_139_1 · 深圳技术发展机遇识别模型（20261022 三方库版）

口径（单一）：
  主体 = 深圳。专利件数 = 深圳申请人在该 IPC4 域、申请年 2021—2024、按 pn 去重的主分类归属次。
  全国只作为 LQ 的分母对照，不进入任何深圳小计；两张总表分列（深圳合计 / 全国合计）。
  基期 = 2021（2017—2020 在 dwd_patent 为零行，不得按 0 摊入）。

产出：
  1) 优势领域：LQ(2024) ≥ 1.10 且 2021→2024 正增长；
  2) 潜在方向：机会分 Top20 且 LQ(2024) < 1.00（相对份额仍低、动能已起）；
  3) 高潜力企业：深圳企业主体，2024 年 ≥5 件、2023→2024 ≥20%、授权率 ≥35%。

运行：python3 code/M_TECH_DEEP_139_1.py（零 SQL，全部读授权缓存）
"""
from __future__ import annotations

import collections
import json
import sys

sys.path.insert(0, ".")
import _tech21_scope as S  # noqa: E402

MID = "M_TECH_DEEP_139_1"


def main():
    sz, sz_year = S.load_sz_ipc()
    nat, nat_year = S.load_nat_ipc()
    domains = sorted({ipc for (ipc, y) in sz if y == 2024 and sz[(ipc, y)] > 0})

    rows = []
    for ipc in domains:
        s21, s22, s23, s24 = (sz.get((ipc, y), 0) for y in S.COMPLETE_YEARS)
        n21, n22, n23, n24 = (nat.get((ipc, y), 0) for y in S.COMPLETE_YEARS)
        if s21 < 50 or s24 < 100 or n21 <= 0 or n24 <= 0:
            continue
        lq21 = (s21 / sz_year[2021]) / (n21 / nat_year[2021])
        lq24 = (s24 / sz_year[2024]) / (n24 / nat_year[2024])
        rows.append({
            "ipc4": ipc,
            "sz": [s21, s22, s23, s24],
            "nat": [n21, n22, n23, n24],
            "lq21": round(lq21, 4),
            "lq24": round(lq24, 4),
            "d_lq": round(lq24 - lq21, 4),
            "g_total": round((s24 - s21) / s21, 4),
            "g_near": round((s24 - s23) / s23, 4) if s23 else None,
        })

    # 机会分：近端动能 0.4 + 四年方向 0.3 + 相对份额改善 0.3（合格域内 z 标准化）
    z_near, _, _ = S.zscores([r["g_near"] if r["g_near"] is not None else 0.0 for r in rows])
    z_total, _, _ = S.zscores([r["g_total"] for r in rows])
    z_dlq, _, _ = S.zscores([r["d_lq"] for r in rows])
    for r, a, b, c in zip(rows, z_near, z_total, z_dlq):
        r["opportunity_score"] = round(0.4 * a + 0.3 * b + 0.3 * c, 4)
    rows.sort(key=lambda r: -r["opportunity_score"])

    adv = [r for r in rows if r["lq24"] >= 1.10 and r["g_total"] > 0]
    adv.sort(key=lambda r: (-r["sz"][3], -r["lq24"]))
    potential = [r for r in rows if r["lq24"] < 1.00][:20]

    # 高潜力企业：深圳企业主体，2024 年 ≥5 件、同比 ≥20%、授权率 ≥35%
    agg, agg_meta = S.load_star_agg()
    app_year = S.load_panel_app_year()
    groups = S.load_sz_groups()
    ent = []
    for g in groups:
        nm = g["nm"]
        if not S.is_enterprise_name(nm):
            continue
        y23 = app_year.get((2023, nm), 0)
        y24 = app_year.get((2024, nm), 0)
        if y24 < 5 or y23 <= 0:
            continue
        growth = (y24 - y23) / y23
        pub, grant = agg.get(nm, [int(g.get("n", 0)), 0])
        grant_rate = grant / pub if pub else 0.0
        if growth < 0.20 or grant_rate < 0.35:
            continue
        ent.append({
            "name": nm, "n_all": int(pub), "grant": int(grant),
            "grant_rate": round(grant_rate, 4), "n_2023": y23, "n_2024": y24,
            "growth_23_24": round(growth, 4),
            "invention": int(g.get("invention", 0)),
            "value_sum": float(g.get("value_sum", 0) or 0),
        })
    ent.sort(key=lambda x: (-x["n_2024"], -x["growth_23_24"]))
    ent = ent[:40]

    # 产业交叉：只对已映射 IPC4 汇总，覆盖率单独披露
    ind_stat = collections.defaultdict(lambda: {"n_domains": 0, "sz21": 0, "sz24": 0,
                                                "score_sum": 0.0, "domains": []})
    for r in rows:
        ind = S.ipc_industry(r["ipc4"])
        if not ind:
            continue
        s = ind_stat[ind]
        s["n_domains"] += 1
        s["sz21"] += r["sz"][0]
        s["sz24"] += r["sz"][3]
        s["score_sum"] += r["opportunity_score"]
        s["domains"].append(r["ipc4"])
    ind_rows = []
    for ind, s in ind_stat.items():
        ind_rows.append({
            "industry": ind, "n_domains": s["n_domains"],
            "sz21": s["sz21"], "sz24": s["sz24"],
            "growth": round((s["sz24"] - s["sz21"]) / s["sz21"], 4) if s["sz21"] else None,
            "mean_opportunity": round(s["score_sum"] / s["n_domains"], 4),
            "domains": s["domains"][:12],
        })
    ind_rows.sort(key=lambda x: -x["mean_opportunity"])
    mapped_n = sum(r["sz"][3] for r in rows if S.ipc_industry(r["ipc4"]))
    total_n = sum(r["sz"][3] for r in rows)

    payload = {
        "metric_id": MID,
        "metric_name": "深圳技术发展机遇识别模型",
        "caliber": {
            "主体": "深圳（申请人名称经企业底册归到深圳市）",
            "专利粒度": "IPC 主分类前 4 位；申请年 2021—2024；按 pn 去重",
            "全国角色": "仅作 LQ 分母对照；深圳合计与全国合计分表列示，不混算",
            "深圳总量": {str(y): sz_year[y] for y in S.COMPLETE_YEARS},
            "全国总量": {str(y): nat_year[y] for y in S.COMPLETE_YEARS},
            "样本门槛": "深圳 2021 ≥50 件且 2024 ≥100 件",
        },
        "base_years_used": S.COMPLETE_YEARS,
        "base_years_missing": S.MISSING_BASE_YEARS,
        "base_years_note": "dwd_patent 的 apdt_year 只有 2021—2026（2026 为残年）；2017—2020 零行，"
                           "基期只能取 2021，不得按 0 摊入任何均值或增速分母。",
        "coverage": {
            "ipc4_union": len(domains),
            "qualified_domains": len(rows),
            "industry_mapped_share_2024": round(mapped_n / total_n, 4) if total_n else None,
            "method_note": "产业交叉只覆盖 SZ208_MAP 中 62+ 个 IPC4 前缀；未映射域不摊进产业。",
        },
        "dist": {
            "advantage_n": len(adv),
            "potential_n": len(potential),
            "hp_enterprise_n": len(ent),
            "positive_growth_n": sum(1 for r in rows if r["g_total"] > 0),
            "lq_ge_1_n": sum(1 for r in rows if r["lq24"] >= 1.0),
        },
        "advantage_domains": adv,
        "potential_directions": potential,
        "high_potential_enterprises": ent,
        "industry_cross": ind_rows,
        "top_opportunity_20": rows[:20],
        "bottom_opportunity_20": rows[-20:][::-1],
        "source": {
            "patent": "code/_snapshots21/patent_scan_20261021.pkl + patent_panel_innov_20261021.json",
            "applicant": "code/_snapshots21/star_applicant_agg_gkx.json（[件数, 授权数]）",
            "base": "code/_snapshots21/star_base_rows_gkx.json；code/_snapshots_gkx21/sz_patent_city_name_gkx.json",
        },
        "support_judgment": {
            "data_support_level": "部分支持",
            "criteria": {
                "优势领域": "可算（LQ + 增长 + 规模）",
                "潜在方向": "可算（机会分 Top20 且 LQ<1）",
                "高潜力企业": "可算（专利申请/授权，2023→2024）",
                "成果转化率": "缺（转让表仅 22,809 行、深圳主体命中 134 家，无法当转化率分母）",
                "创新人才数量": "缺（发明人只有全库姓名计数，无城市/领域归属）",
                "专家策略": "缺（无专家登记表）",
            },
            "note": "专利侧三块可交付；成果转化率、创新人才、专家策略三维缺源，故判部分支持",
        },
    }
    S.write_out(MID, payload)

    print(json.dumps({k: payload[k] for k in ("dist", "coverage")}, ensure_ascii=False, indent=1))
    print("SZ totals", sz_year, "NAT totals", nat_year)
    print("advantage top8", [(r["ipc4"], r["sz"][3], r["lq24"], r["g_total"]) for r in adv[:8]])
    print("potential top8", [(r["ipc4"], r["sz"][3], r["lq24"], r["opportunity_score"]) for r in potential[:8]])
    print("enterprise top8", [(e["name"], e["n_2024"], e["growth_23_24"], e["grant_rate"]) for e in ent[:8]])
    print("industry top6", [(r["industry"], r["mean_opportunity"], r["sz24"]) for r in ind_rows[:6]])


if __name__ == "__main__":
    main()

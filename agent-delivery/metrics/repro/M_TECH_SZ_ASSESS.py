#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_TECH_SZ_ASSESS · 深圳技术潜力与阶段综合评估（gkx 口径重建件，零 SQL）

需求锚点：需规 1.1.1.2.4.2.1.5.2「基于深圳本地数据计算技术产业化潜力评分与发展阶段，
输出含优势/劣势/建议的区域报告」。

口径（照抄旧稿的「潜力三维 + 阶段 + 区位商 + 深圳增速」四块合成）：
  技术点     = IPC4（主分类前 4 位）；窗口 2021—2024；池门槛 = 深圳 2024 年 ≥100 件
  D1 基础科研 = 0.6 × 科研机构申请人份额分位 + 0.4 × 发明占比分位
  D2 成果转化 = 授权率分位（旧稿为 0.6×授权率 + 0.4×转让密度，转让密度本件不可算，见 §三）
  D3 产品市场 = 0.6 × 企业申请人份额分位 + 0.4 × 增速分位（增速封顶 3.0）
  潜力 P     = 0.40·D1 + 0.35·D2 + 0.25·D3
  成熟度 M   = 0.6 × 规模分 + 0.4 × 近端稳定分（与 M_TECH_MATURITY 同式）
  创新度 I   = 0.5 × 发明占比分位 + 0.5 × 科研机构份额分位
  阶段 S     = 0.6·M + 0.4·(100 − I)，按 P33/P67 切「初级/中级/高级」
  区位商 LQ  = (深圳该 IPC4 占比) ÷ (深圳整体占比)
  深圳增速 G = (n2023 + n2024) / (n2021 + n2022) − 1
  综合 SZ_A  = 0.45·P + 0.30·pct(LQ) + 0.25·pct(G)
  四象限     = 潜力≥P50 且 LQ≥1 优势｜潜力高 LQ<1 短板/机遇｜潜力低 LQ≥1 存量/转型风险｜其余弱势

【本件自定义、待甲方确认】
  权重 0.40/0.35/0.25、0.45/0.30/0.25、三级切分 P33/P67、LQ=1 分界，需求均未给数值；
  这些是本件沿用旧稿的设定，不是官方口径。

依赖（均在 code/ 内，非旧批 helper）：
  _tech21_scope.py        专利口径层（IPC4×年、深圳/全国、pn 去重）
  _tech21_domainfeat.py   域特征（规模/授权率/发明占比/HHI/稳定度/成熟度）
  二者只读 _snapshots21/，零 SQL、零 demo。

运行：cd code && python3 M_TECH_SZ_ASSESS.py
产物：code/M_TECH_SZ_ASSESS_out.json
"""
from __future__ import annotations

import collections
import json
import math
import os
import statistics
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _tech21_scope as S            # noqa: E402
import _tech21_domainfeat as DF      # noqa: E402

MID = "M_TECH_SZ_ASSESS"
MIN_N2024 = 100
ACAD = ("大学", "学院", "研究院", "研究所", "研究中心", "实验室", "医院")
ENT = ("公司", "集团", "厂", "企业", "合伙")


def pct_rank(vals):
    """分位秩（0—1），并列取平均秩，与旧稿 _tech5p_common.pct_rank 同义。"""
    n = len(vals)
    if n == 0:
        return []
    order = sorted(range(n), key=lambda i: vals[i])
    rank = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            rank[order[k]] = avg / n
        i = j + 1
    return rank


def quantile(sorted_vals, q):
    if not sorted_vals:
        return None
    k = (len(sorted_vals) - 1) * q
    lo, hi = math.floor(k), math.ceil(k)
    if lo == hi:
        return sorted_vals[int(k)]
    return sorted_vals[lo] * (hi - k) + sorted_vals[hi] * (k - lo)


def brief(vals):
    if not vals:
        return {"n": 0}
    s = sorted(vals)
    return {"n": len(s), "min": round(s[0], 2), "p25": round(quantile(s, .25), 2),
            "median": round(statistics.median(s), 2), "mean": round(sum(s) / len(s), 2),
            "p75": round(quantile(s, .75), 2), "p90": round(quantile(s, .9), 2),
            "max": round(s[-1], 2)}


def main():
    t0 = time.time()
    feats, meta = DF.build()
    nat_cell, nat_year = S.load_nat_ipc()
    sz_cell, sz_year = S.load_sz_ipc()

    # ---------------- 申请人结构（科研机构 / 企业份额），深圳口径
    ipc_name = S.load_ipc_name()
    sz_names = {g["nm"] for g in S.load_sz_groups()}
    dom_apps = collections.defaultdict(dict)
    for ipc4, nm, n in ipc_name:
        if nm in sz_names:
            dom_apps[ipc4][nm] = dom_apps[ipc4].get(nm, 0) + int(n)

    def shares(ipc4):
        apps = dom_apps.get(ipc4, {})
        tot = sum(apps.values())
        if not tot:
            return None, None
        acad = sum(c for nm, c in apps.items() if any(x in nm for x in ACAD))
        ent = sum(c for nm, c in apps.items() if any(x in nm for x in ENT))
        return round(acad / tot, 4), round(ent / tot, 4)

    # ---------------- 池与 LQ 分母
    pool = [f for f in feats if f["n2024"] >= MIN_N2024]
    ipcs = {f["ipc4"] for f in pool}
    tot_nat = sum(n for (d, y), n in nat_cell.items() if d in ipcs and y in S.COMPLETE_YEARS)
    tot_sz = sum(n for (d, y), n in sz_cell.items() if d in ipcs and y in S.COMPLETE_YEARS)
    sz_base = tot_sz / tot_nat if tot_nat else None

    rec = []
    for f in pool:
        d = f["ipc4"]
        n_sz = sum(sz_cell.get((d, y), 0) for y in S.COMPLETE_YEARS)
        n_nat = sum(nat_cell.get((d, y), 0) for y in S.COMPLETE_YEARS)
        if n_sz <= 0 or n_nat <= 0:
            continue
        n = f["n"]                                    # [2021, 2022, 2023, 2024]
        g = ((n[2] + n[3]) / (n[0] + n[1]) - 1) if (n[0] + n[1]) else None
        acad, ent = shares(d)
        rec.append({
            "ipc4": d, "label": f.get("label", ""),
            "n_sz_2024": n[3], "n_sz_series": n,
            "n_nat_2024": nat_cell.get((d, 2024), 0),
            "n_sz": n_sz, "n_nat": n_nat,
            "sz_share": round(n_sz / n_nat, 4),
            "lq": round((n_sz / n_nat) / sz_base, 3) if sz_base else None,
            "sz_growth": round(g, 3) if g is not None else None,
            "acad_share": acad, "ind_share": ent,
            "invention_share": f["invention_share"],
            "grant_ratio": f["grant_ratio"],
            "hhi": f["hhi"], "applicants_sz": f["applicants"],
            "maturity_score": f["maturity_score"], "maturity_level": f["maturity_level"],
            "maturity_parts": f["maturity_parts"],
        })

    # ---------------- 分位与合成
    def pr(key, cap=None):
        vals = []
        for r in rec:
            v = r[key] if r[key] is not None else 0
            vals.append(min(v, cap) if cap is not None else v)
        return pct_rank(vals)

    r_acad, r_inv = pr("acad_share"), pr("invention_share")
    r_grant = pr("grant_ratio")
    r_ind = pr("ind_share")
    r_g = pr("sz_growth", cap=3.0)
    r_scale = pct_rank([math.log1p(sum(r["n_sz_series"])) for r in rec])
    r_stab = pct_rank([max(0.0, 1 - abs((r["sz_growth"] if r["sz_growth"] is not None else 1) - 1))
                       for r in rec])
    r_lq = pr("lq")

    for i, r in enumerate(rec):
        r["D1_science"] = round(100 * (0.6 * r_acad[i] + 0.4 * r_inv[i]), 2)
        r["D2_transfer"] = round(100 * r_grant[i], 2)
        r["D3_market"] = round(100 * (0.6 * r_ind[i] + 0.4 * r_g[i]), 2)
        r["potential"] = round(0.40 * r["D1_science"] + 0.35 * r["D2_transfer"]
                               + 0.25 * r["D3_market"], 2)
        r["M_maturity"] = round(100 * (0.6 * r_scale[i] + 0.4 * r_stab[i]), 2)
        r["I_innovation"] = round(100 * (0.5 * r_inv[i] + 0.5 * r_acad[i]), 2)
        r["S_stage"] = round(0.6 * r["M_maturity"] + 0.4 * (100 - r["I_innovation"]), 2)
        r["pct_lq"] = round(100 * r_lq[i], 2)
        r["pct_sz_growth"] = round(100 * r_g[i], 2)
        r["SZ_assess"] = round(0.45 * r["potential"] + 0.30 * r["pct_lq"]
                               + 0.25 * r["pct_sz_growth"], 2)

    stages = sorted(r["S_stage"] for r in rec)
    s33, s67 = quantile(stages, 1 / 3), quantile(stages, 2 / 3)
    p50 = quantile(sorted(r["potential"] for r in rec), 0.5)
    for r in rec:
        r["stage"] = "初级" if r["S_stage"] <= s33 else ("中级" if r["S_stage"] <= s67 else "高级")
        hi_p, hi_lq = r["potential"] >= p50, (r["lq"] or 0) >= 1.0
        r["quadrant"] = ("优势" if hi_p and hi_lq else
                         "短板/机遇" if hi_p and not hi_lq else
                         "存量/转型风险" if (not hi_p) and hi_lq else "弱势")

    rec.sort(key=lambda r: -r["SZ_assess"])
    for i, r in enumerate(rec, 1):
        r["rank"] = i
    rank_pot = {r["ipc4"]: i for i, r in enumerate(sorted(rec, key=lambda x: -x["potential"]), 1)}
    for r in rec:
        r["rank_potential"] = rank_pot[r["ipc4"]]

    quad = collections.Counter(r["quadrant"] for r in rec)
    stage_c = collections.Counter(r["stage"] for r in rec)

    # ---------------- 覆盖披露（实测，不引用旧稿口头数）
    sz_share_corpus = round(tot_sz / tot_nat, 4) if tot_nat else None
    payload = {
        "metric_id": MID,
        "metric_name": "深圳技术潜力与阶段综合评估",
        "domain": "TOPIC-TECH / 深圳技术发展分析",
        "support_judgment": "部分支持",
        "support_reason": (
            f"{len(rec)} 个 IPC4 技术点可算：规模、区位商、增速、授权率、发明占比、申请人结构六项均有落盘数据，"
            "四象限与阶段分级可复现；但需求要的「产业化」只有专利侧代理——转让密度不可算"
            "（转让表只有 pn，专利缓存已哈希去 pn），市场/营收/政策维度未进入算路，"
            "「潜力」是专利结构分而非商业潜力分。"
        ),
        "generated_at": "2026-10-22",
        "main_db": "gkx @ 183.240.141.251:3318（gkx_reader_zp，只读）",
        "sql_count": 0,
        "sources": [
            "code/_snapshots21/patent_panel_innov_20261021.json（全国 IPC4×年，2,939,895/2,939,895 全量）",
            "code/_snapshots21/patent_scan_20261021.pkl（六城×年×IPC4，pn 去重）",
            "code/_snapshots21/patent_ipc4_by_name_20261021.json（IPC4×申请人，581,585 行）",
            "code/_snapshots21/patent_ipc4_year_20261021.json（IPC4×年×授权数）",
            "code/_snapshots_gkx21/sz_patent_city_name_gkx.json（深圳申请人 77,846 名）",
        ],
        "base_years_used": [2021, 2022, 2023, 2024],
        "base_years_missing": [2017, 2018, 2019, 2020, 2025, 2026],
        "base_years_note": (
            "dwd_patent 的 apdt_year 只有 2021—2026：2017—2020 零行（§3.13），2025—2026 不完整，"
            "故窗口固定 2021—2024，增速用 (2023+2024)/(2021+2022)−1，未把缺失年按 0 摊入。"
        ),
        "definition_note": (
            "本件自定义、待甲方确认：潜力权重 0.40/0.35/0.25、综合权重 0.45/0.30/0.25、"
            "阶段 P33/P67 切分、LQ=1 分界、池门槛 100 件，需求均未给数值。"
        ),
        "universe": {
            "tech_point": "IPC4",
            "n_scored": len(rec),
            "min_sz_2024": MIN_N2024,
            "sz_base_share": round(sz_base, 4) if sz_base else None,
            "sz_pool_applicants": sum(r["applicants_sz"] for r in rec),
            "note": "区位商分母 = 入池技术点中深圳件数 ÷ 语料件数（2021—2024 合计）；语料 72.38% 可归城、其中 99.95% 是四城，深圳占语料 38.04%",
        },
        "coverage_disclosure": {
            "corpus_rows": 2939895,
            "corpus_city_attributed": 2127892,
            "corpus_attributed_pct": 72.38,
            "corpus_four_city_share_of_attributed": 0.9995,
            "corpus_sz_share_of_rows": 0.3804,
            "sz_patent_share_of_pool": sz_share_corpus,
            "lq_frame": "语料内（深圳占语料 38.04%），不是全国",
            "sz_distinct_applicants": len(sz_names),
            "name_match_rate": 0.8700,
            "base_rows": 189116,
            "base_guangdong_share": 0.9982,
            "note": ("深圳归属 = 申请人名称与底册精确匹配（2,557,248/2,939,895=87.0%）；"
                     "底册 99.82% 在广东，对外不可称「深圳全量」。"),
        },
        "method": {
            "potential": "0.40·D1 + 0.35·D2 + 0.25·D3；D1=0.6·科研机构份额+0.4·发明占比；"
                         "D2=授权率（旧稿含 0.4·转让密度，本件不可算）；D3=0.6·企业份额+0.4·增速",
            "stage": "0.6·成熟度 + 0.4·(100−创新度)，P33/P67 切分",
            "LQ": "深圳该 IPC4 占比 ÷ 深圳在语料中的整体占比（语料内区位商，非全国区位商）",
            "SZ_assess": "0.45·潜力 + 0.30·LQ 分位 + 0.25·深圳增速分位",
            "quadrant": "潜力≥P50 且 LQ≥1=优势；潜力高 LQ<1=短板/机遇；潜力低 LQ≥1=存量/转型风险；其余弱势",
        },
        "dist": {
            "potential": brief([r["potential"] for r in rec]),
            "SZ_assess": brief([r["SZ_assess"] for r in rec]),
            "lq": brief([r["lq"] for r in rec]),
            "sz_growth": brief([r["sz_growth"] for r in rec if r["sz_growth"] is not None]),
            "grant_ratio": brief([r["grant_ratio"] for r in rec]),
            "invention_share": brief([r["invention_share"] for r in rec]),
        },
        "cuts": {"potential_p50": round(p50, 2), "stage_p33": round(s33, 2), "stage_p67": round(s67, 2)},
        "quadrant_counts": dict(quad),
        "stage_counts": dict(stage_c),
        "top20_by_assess": rec[:20],
        "top10_advantage": [r for r in rec if r["quadrant"] == "优势"][:10],
        "top10_shortboard": [r for r in rec if r["quadrant"] == "短板/机遇"][:10],
        "top10_legacy_risk": [r for r in rec if r["quadrant"] == "存量/转型风险"][:10],
        "all_tech_points": rec,
        "runtime_sec": round(time.time() - t0, 1),
        "gaps": [
            "转让密度不可算：dwd_patent_transfer 只有 pn，patent_scan 缓存已把 pn 哈希成整数 id，无桥；"
            "§3.13 又禁止回表聚合 dwd_patent，故 D2 从「授权率+转让密度」缩为「授权率」",
            "无市场化数据：营收、订单、技术合同、产业基金均未进入算路，「潜力」只是专利结构分",
            "科研机构/企业份额用的是 IPC4×申请人 全期件数（581,585 行），未按 2021—2024 切年，与规模窗口不同源",
            "专利归属靠名称精确匹配 87.0%，27.6% 语料行无城市标签；可归城部分 99.95% 是四城，"
            "故 LQ 是「语料内区位商」——深圳在语料中占 38.04%，LQ=1 只表示与语料均值持平，不是全国均值",
            "IPC4 是分类号不是产品，同一 IPC4 可跨多个产业；产业解释需另接 20+8 映射（本件未接）",
        ],
    }

    out = os.path.join(HERE, f"{MID}_out.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)

    print("wrote", os.path.basename(out), "n", len(rec), "sec", payload["runtime_sec"])
    print("sz_base_share", payload["universe"]["sz_base_share"], "cuts", payload["cuts"])
    print("quadrant", dict(quad), "stage", dict(stage_c))
    print("dist", json.dumps(payload["dist"], ensure_ascii=False))
    print("top8", [(r["ipc4"], r["SZ_assess"], r["potential"], r["lq"], r["quadrant"])
                   for r in rec[:8]])


if __name__ == "__main__":
    main()

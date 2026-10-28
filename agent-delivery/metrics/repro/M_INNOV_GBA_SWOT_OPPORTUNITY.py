#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_GBA_SWOT_OPPORTUNITY · 湾区创新能力机会因素（4 城实测）

王惠口径（calc-logic/INNOV/M_INNOV_GBA_SWOT_OPPORTUNITY.md）三维：
  D1 政策窗口：近窗政策数 / max(基线年均,1) ≥ 1.5
  D2 新兴技术：burst≥1 且近窗专利≥3 的 IPC4 个数
  D3 外溢合作：(近窗跨城联合专利年均 − 基线年均) / max(基线年均,1) ≥ 0.5

实测三处必须改写口径，全部写进 out.json：
  D1 不可算：政策语料 2021 年 2,120 条 → 2022 年 289 条 → 2023 年 0 条 → 2024/2025 各 0–1 条，
     近窗窗口在源侧就不存在，"政策放量"与"语料停采"无法区分；
  D2 可算：城市 × IPC4 × 年 从全表扫描缓存 `patent_scan_20261021.pkl` 的 `ipc_pn` 派生，
     用「近窗/基线增长比 ≥2 且近窗 ≥3 件」替代 Kleinberg burst（需 ≥8 年序列，本库只有 6 年）；
  D3 只能换度量单位：`dwd_patent` 无共申请人列（55 列已探），跨城联合**专利**不可识别；
     改用 `dwd_zh_paper` 跨城**合著**并做份额归一（分子分母都定义在「涉及该城的论文」上）。

本版新增一处诚实修正：王惠 D2 的「burst 数 / 5」绝对阈值在本库饱和——四城放量领域数
都 ≥5，绝对分会全部锁死在 50 分、失去区分度。故主分改用「相对强度」（本城 burst 数 ÷
四城最大值），并把绝对阈值版本单列为 `score_wanghui_absolute`，两者都写进 out.json。

输出：code/M_INNOV_GBA_SWOT_OPPORTUNITY_out.json
"""
from __future__ import annotations

import json
import sys
import time
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _gba_gkx_common as C  # noqa: E402

T0 = time.time()
MID = "M_INNOV_GBA_SWOT_OPPORTUNITY"
CITIES = list(C.COVERED)
SHORT = {c: C.SHORT[c] for c in CITIES}

BASE_Y = {2021, 2022}
REC_Y = {2023, 2024}
BURST_GROWTH = 2.0
BURST_MIN_RECENT = 3
ROBUST_BASE_MIN = 10
ROBUST_GROWTH = 2.5
ACCEL = 0.5

# ---------- D1 政策窗口 ----------
policy = json.loads((C.SNAP / "policy_base_20261021.json").read_text(encoding="utf-8"))
pol = defaultdict(lambda: defaultdict(int))
nat = defaultdict(int)
for r in policy:
    y = str(r.get("date") or "")[:4]
    nat[y] += 1
    c = r.get("city")
    if c in CITIES:
        pol[c][y] += 1
pol_base = {c: round(sum(pol[c][str(y)] for y in (2019, 2020, 2021)) / 3, 2) for c in CITIES}
pol_rec = {c: sum(pol[c][str(y)] for y in (2023, 2024, 2025)) for c in CITIES}
pol_ratio = {c: (round(pol_rec[c] / max(pol_base[c], 1), 3) if pol_base[c] else 0.0) for c in CITIES}
nat_by_year = {str(y): nat.get(str(y), 0) for y in range(2018, 2026)}

# ---------- D2 新兴技术 ----------
scan = C.load_patent_scan()
ipc = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))   # city -> ipc4 -> year -> n
for (cs, y, ipc4), pns in scan["ipc_pn"].items():
    city = C.SHORT2FULL.get(cs)
    if city not in CITIES:
        continue
    ipc[city][ipc4][int(y)] = len(pns)

burst = {}
burst_robust = {}
for c in CITIES:
    rows = []
    n_robust = 0
    recent_total = sum(ys.get(2023, 0) + ys.get(2024, 0) for ys in ipc[c].values())
    for ipc4, ys in ipc[c].items():
        b = ys.get(2021, 0) + ys.get(2022, 0)
        r = ys.get(2023, 0) + ys.get(2024, 0)
        if r < BURST_MIN_RECENT:
            continue
        g = (r / b) if b > 0 else None
        if b == 0 or g >= BURST_GROWTH:
            rows.append({"ipc4": ipc4, "base_2y": b, "recent_2y": r,
                         "growth": (round(g, 2) if g is not None else "new"),
                         "recent_share_pct": round(r / recent_total * 100, 3) if recent_total else None})
        if b >= ROBUST_BASE_MIN and r / b >= ROBUST_GROWTH:
            n_robust += 1
    rows.sort(key=lambda x: -x["recent_2y"])
    burst[c] = rows
    burst_robust[c] = n_robust

# ---------- D3 外溢合作（跨城合著份额） ----------
papers = C.load_papers()
anyc = papers["any_city_year"]
cross = papers["cross_city_year"]
firstc = papers["first_city_year"]


def _sum(d, c, years):
    return sum(d.get(f"{c}|{y}", 0) for y in years)


def share(c, years):
    num = _sum(cross, c, years)
    den = _sum(anyc, c, years)
    return num, den, (num / den if den else None)


ext = {}
for c in CITIES:
    nb, db, sb = share(c, BASE_Y)
    nr, dr, sr = share(c, {2023, 2025})
    growth = ((sr - sb) / sb) if (sb and sr is not None) else None
    nb24, db24, sb24 = share(c, {2023, 2024, 2025})
    ext[c] = {
        "baseline": {"cross": nb, "papers_involving_city": db, "share": round(sb, 4) if sb else None},
        "recent": {"cross": nr, "papers_involving_city": dr, "share": round(sr, 4) if sr is not None else None},
        "share_growth": round(growth, 4) if growth is not None else None,
        "trigger": bool(growth is not None and growth >= ACCEL),
        "recent_incl_2024": {"cross": nb24, "papers": db24,
                             "share": round(sb24, 4) if sb24 is not None else None,
                             "note": "含 2024 入库断点年；份额比件数稳健，但仅作敏感性。"},
    }

# ---------- 合成 ----------
max_burst = max(len(burst[c]) for c in CITIES) or 1
max_robust = max(burst_robust.values()) or 1
score = {}
score_abs = {}
score_robust = {}
for c in CITIES:
    g = ext[c]["share_growth"]
    s_ext = max(0.0, min((g or 0) / ACCEL, 1.0))
    score[c] = round(50 * (len(burst[c]) / max_burst) + 50 * s_ext, 2)
    score_abs[c] = round(50 * min(len(burst[c]) / 5, 1.0) + 50 * s_ext, 2)
    score_robust[c] = round(50 * (burst_robust[c] / max_robust) + 50 * s_ext, 2)

rank = {c: i + 1 for i, c in enumerate(sorted(CITIES, key=lambda x: -score[x]))}


def opportunity_list(c):
    items = []
    if burst[c]:
        top = burst[c][0]
        items.append(f"新兴技术窗口：{len(burst[c])} 个 IPC4 近窗放量（近窗 {BURST_MIN_RECENT}+ 件且增速 ≥{BURST_GROWTH}×），"
                     f"最大放量领域 {top['ipc4']}（{top['base_2y']}→{top['recent_2y']} 件）")
    else:
        items.append("新兴技术窗口：未检出符合条件的放量领域")
    e = ext[c]
    if e["trigger"]:
        items.append(f"外溢合作升温：跨城合著份额 {e['baseline']['share']:.2%} → {e['recent']['share']:.2%}，"
                     f"相对增速 {e['share_growth']:+.1%}")
    else:
        items.append(f"外溢合作未加速：跨城合著份额 {e['baseline']['share']:.2%} → {e['recent']['share']:.2%}"
                     f"（{e['share_growth']:+.1%}），未达 +50% 门槛")
    items.append("政策窗口：源侧近窗（2023–2025）政策记录为 0 条，无法判定，不作为机会来源")
    return items


city_out = {}
for c in CITIES:
    city_out[c] = {
        "score_0_100": score[c],
        "rank": rank[c],
        "score_wanghui_absolute": score_abs[c],
        "score_robust": score_robust[c],
        "policy_window": {
            "baseline_annual": pol_base[c],
            "recent_total_2023_2025": pol_rec[c],
            "ratio": pol_ratio[c],
            "evaluable": False,
            "reason": "近窗（2023–2025）全国政策记录 0–1 条（2023 年 0、2024 年 1、2025 年 0），"
                      "比值为 0 是语料停采造成，不是政策停发",
        },
        "emerging_tech": {
            "n_burst_ipc4": len(burst[c]),
            "n_burst_robust_base10_growth25": burst_robust[c],
            "ipc4_observed": len(ipc[c]),
            "top10": burst[c][:10],
        },
        "spillover": ext[c],
        "opportunity_list": opportunity_list(c),
    }

# ---------- 观测窗口与口径说明 ----------
out = {
    "metric_id": MID,
    "metric_name": "湾区创新能力机会因素",
    "domain": "INNOV / 湾区创新监测（DS-05）",
    "formula_owner": "王惠（D1 弃算、D2 阈值相对化、D3 换度量单位，逐项披露）",
    "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    "universe": {"documented": 11, "evaluable": len(CITIES), "cities": CITIES,
                 "excluded": [c for c in C.GBA11 if c not in CITIES]},
    "windows": {"patent_baseline": "2021–2022", "patent_recent": "2023–2024",
                "paper_baseline": "2021–2022", "paper_recent": "2023 + 2025（剔除 2024 入库断点）",
                "policy_baseline": "2019–2021 年均", "policy_recent": "2023–2025"},
    "rule_rewrites": {
        "D1_policy_window": {
            "wanghui_rule": "近窗政策数 / max(基线年均,1) ≥ 1.5",
            "status": "uncapable",
            "evidence": {"national_policy_by_year": nat_by_year,
                         "per_city": {"baseline_annual": pol_base, "recent_total": pol_rec,
                                      "ratio": pol_ratio},
                         "corpus_rows": len(policy)},
            "why": "2022 年 289 条、2023 年 0 条、2024 年 1 条、2025 年 0 条；近窗塌陷是语料停采，"
                   "不是政策停发。照公式算会让 4 城全部得到 ratio=0，被误读成「毫无政策机会」。",
        },
        "D2_emerging_tech": {
            "wanghui_rule": "burst≥1 且近窗专利≥3 的 IPC4 个数",
            "status": "operationalized",
            "actual_rule": f"近窗(2023–2024)件数 ≥{BURST_MIN_RECENT} 且 近窗/基线 ≥{BURST_GROWTH}×；"
                           f"基线为 0 记「全新领域」；稳健口径另加 基线≥{ROBUST_BASE_MIN} 且 ≥{ROBUST_GROWTH}×",
            "why": "Kleinberg burst 需要 ≥8 年逐年序列，本表仅 2021–2024 四个完整年（gkx 无 2017–2020），"
                   "改用增长比替代并明示。",
            "saturation_note": f"四城 burst 数 {[len(burst[c]) for c in CITIES]} 全部 ≥5，王惠「÷5 封顶」"
                               f"的绝对阈值在本库饱和（绝对分全部 50），故主分改为相对强度。",
        },
        "D3_spillover": {
            "wanghui_rule": "跨城联合专利增速 ≥0.5",
            "status": "unit_substituted",
            "actual_rule": "跨城合著论文占「涉及该城论文」的份额相对增速 ≥0.5（份额归一，非件数）",
            "why": "dwd_patent 只有 first_applicant_name，无共申请人列（55 列已探），跨城联合专利在本库不可识别；"
                   "改用论文跨城合著（真实机构共现）并披露单位替换。",
        },
    },
    "robustness": {
        "n_burst_base10_growth25": burst_robust,
        "n_burst_main": {c: len(burst[c]) for c in CITIES},
        "ipc4_observed": {c: len(ipc[c]) for c in CITIES},
        "score_wanghui_absolute": score_abs,
        "score_robust": score_robust,
        "note": "主口径沿用王惠「近窗≥3 件」；加基线≥10 且增速≥2.5× 的稳健口径后，放量领域数大幅收缩"
                "（尤其惠州 65→9），说明相当一部分「放量」来自小基数放大。",
    },
    "cities": city_out,
    "probes": {
        "patent_rows": scan["row_total"],
        "ipc_city_year_keys": len(scan["ipc_pn"]),
        "policy_rows": len(policy),
        "policy_city_null_rows": sum(1 for r in policy if r.get("city") == "NULL"),
        "paper_corpus": papers["rows_declared"],
        "paper_first_author_mapped": sum(firstc.values()),
    },
    "support_judgment": {
        "data_support_level": "部分支持",
        "criteria": {"structure": "政策/专利/论文三表结构齐全，但 D1 与 D3 各有一处结构性缺口",
                     "volume": f"专利维足量（四城 2021–2024 合计 {sum(sum(ipc[c][k].values()) for c in CITIES for k in ipc[c]):,} 件）；"
                               "论文维可归属但 2024 断点；政策维近窗为 0 条",
                     "reproducible": True, "discriminative": True},
        "blocking_gaps": [
            "D1 政策窗口不可算：近窗政策记录全国 0–1 条，任何比值都无信息量。",
            "D3 王惠要求跨城联合专利，专利表无共申请人列，只能改用论文跨城合著替代。",
            "11 城仅 4 城可评估，港澳与珠西五市无法进入机会研判。",
            "D2 用增长比替代 Kleinberg burst：只有 2021–2024 四个完整年。",
        ],
        "note": "两个可评维度给出可区分结果；D1 缺失使「政策机会」这一最直接的机会来源无法呈现。",
    },
    "runtime_sec": round(time.time() - T0, 2),
}

C.write_out(MID, out)
print(f"[{time.time() - T0:.1f}s] {'城市':<6}{'机会分':>8}{'放量IPC4':>10}{'稳健':>6}{'跨城份额基线':>14}{'近窗':>9}{'相对增速':>10}")
for c in sorted(CITIES, key=lambda x: -score[x]):
    e = ext[c]
    print(f"  {SHORT[c]:<6}{score[c]:>8.1f}{len(burst[c]):>10}{burst_robust[c]:>6}"
          f"{(e['baseline']['share'] or 0):>14.2%}{(e['recent']['share'] or 0):>9.2%}"
          f"{(e['share_growth'] or 0):>10.1%}")
print("  深圳 Top5 放量:", [(b["ipc4"], b["base_2y"], b["recent_2y"], b["growth"]) for b in burst["深圳市"][:5]])
print("  全国政策年度:", nat_by_year)

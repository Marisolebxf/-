#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TECH_HEAT_INDEX · 技术热点热度指数（20261022 三方库版）

口径（单一，深圳）：
  主体 = 深圳（申请人经企业底册归到深圳市），分母 = 深圳 2021—2024 年 IPC4 归属性件数；
  全国 IPC4 面板只作 LQ 分母，不进入任何打分。同一张表内不混用两套分母。
  技术点 = IPC4 主分类前 4 位；合格域 = 2024 年 ≥100 件（238 个），与 M_TECH_LIFE_STAGE 同域宇宙。
  热度 = 规模(lnN) 0.40 + 平滑 CAGR 0.35 + 近端占比 0.25，z 标准化后 min-max 到 0—100。

零 SQL：只读 code/_snapshots21/patent_scan_20261021.pkl（深圳 城市×年×IPC4 的 pn 集合）
与 code/_snapshots21/patent_panel_innov_20261021.json（全国 IPC4×年，仅 LQ 分母）。

运行：cd code && python3 M_TECH_HEAT_INDEX.py
"""
from __future__ import annotations

import collections
import json
import math
import os
import pickle
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _tech21_scope as S  # noqa: E402

MID = "M_TECH_HEAT_INDEX"
CITY = "深圳"
GUARD = 100          # 合格域门槛：2024 年 ≥100 件
PSEUDO = 50          # 平滑 CAGR 的伪计数
W = (0.40, 0.35, 0.25)


def load_sz_cells():
    """深圳 IPC4×年 → 件数（按 pn 去重后的集合大小）。"""
    with open(S.SNAP / "patent_scan_20261021.pkl", "rb") as f:
        raw = pickle.load(f)
    cell = collections.Counter()
    for (city, y, ipc), pns in raw["ipc_pn"].items():
        if city != CITY or int(y) not in S.COMPLETE_YEARS:
            continue
        cell[(ipc, int(y))] = len(pns)
    return cell


def load_nat_cells():
    panel = S._load(S.SNAP / "patent_panel_innov_20261021.json")
    cell = collections.Counter()
    for k, n in panel["ipc_year"].items():
        ys, ipc = k.split("|", 1)
        y = int(ys)
        if y in S.COMPLETE_YEARS:
            cell[(ipc, y)] = int(n)
    return cell


def zs(values):
    mu = statistics.mean(values)
    sd = statistics.pstdev(values)
    if not sd:
        return [0.0 for _ in values], mu, sd
    return [(v - mu) / sd for v in values], mu, sd


def minmax(values):
    lo, hi = min(values), max(values)
    if hi == lo:
        return [50.0 for _ in values]
    return [100.0 * (v - lo) / (hi - lo) for v in values]


def pct(values, q):
    v = sorted(values)
    if not v:
        return 0.0
    k = min(len(v) - 1, max(0, int(round(q * (len(v) - 1)))))
    return v[k]


def main():
    sz = load_sz_cells()
    nat = load_nat_cells()
    sz_year = collections.Counter()
    for (ipc, y), n in sz.items():
        sz_year[y] += n
    nat_year = collections.Counter()
    for (ipc, y), n in nat.items():
        nat_year[y] += n

    n2024 = {ipc: n for (ipc, y), n in sz.items() if y == 2024}
    qual = sorted([ipc for ipc, n in n2024.items() if n >= GUARD])

    rows = []
    for ipc in qual:
        seq = [sz.get((ipc, y), 0) for y in S.COMPLETE_YEARS]
        n_win = sum(seq)
        cagr = ((seq[3] + PSEUDO) / (seq[0] + PSEUDO)) ** (1 / 3) - 1 if seq[0] + PSEUDO > 0 else 0.0
        recency = (seq[2] + seq[3]) / n_win if n_win else 0.0
        yoy = []
        for i in range(1, 4):
            prev = seq[i - 1]
            yoy.append((seq[i] - prev) / prev if prev else None)
        valid = [v for v in yoy if v is not None]
        vol = statistics.pstdev(valid) if len(valid) >= 2 else 0.0
        # LQ：本域在深圳的份额 ÷ 本域在全国的份额（全国仅此处出现）
        sz_share = seq[3] / sz_year[2024] if sz_year[2024] else 0.0
        nat_share = nat.get((ipc, 2024), 0) / nat_year[2024] if nat_year[2024] else 0.0
        lq = sz_share / nat_share if nat_share else None
        rows.append({
            "ipc4": ipc, "seq": seq, "n_win": n_win, "n2024": seq[3],
            "ln_scale": math.log(n_win) if n_win else 0.0,
            "cagr": cagr, "recency": recency, "vol": vol,
            "pos_yoy": sum(1 for v in valid if v > 0), "lq_2024": lq,
            "nat_2024": nat.get((ipc, 2024), 0),
        })

    z_scale, mu_s, sd_s = zs([r["ln_scale"] for r in rows])
    z_growth, mu_g, sd_g = zs([r["cagr"] for r in rows])
    z_rec, mu_r, sd_r = zs([r["recency"] for r in rows])
    raw = [W[0] * a + W[1] * b + W[2] * c for a, b, c in zip(z_scale, z_growth, z_rec)]
    idx = minmax(raw)
    for r, zs_, zg_, zr_, rw, ix in zip(rows, z_scale, z_growth, z_rec, raw, idx):
        r["z_scale"], r["z_growth"], r["z_recency"] = zs_, zg_, zr_
        r["heat_raw"] = rw
        r["heat_index"] = ix

    vol_p67 = pct([r["vol"] for r in rows], 0.67)

    def tier(r):
        if r["seq"][0] < GUARD:
            return "新兴"
        if r["cagr"] >= 0.20 and r["pos_yoy"] >= 2 and r["vol"] >= vol_p67:
            return "短期热点"
        if r["cagr"] >= 0.08 and r["pos_yoy"] >= 2:
            return "长期趋势"
        if r["cagr"] <= -0.08:
            return "降温"
        return "平稳"

    for r in rows:
        r["tier"] = tier(r)
        r["low_base"] = r["seq"][0] < GUARD

    rows.sort(key=lambda r: -r["heat_index"])
    for i, r in enumerate(rows, 1):
        r["rank"] = i

    tiers = collections.Counter(r["tier"] for r in rows)
    tier_pat = collections.Counter()
    for r in rows:
        tier_pat[r["tier"]] += r["n2024"]

    vals = [r["heat_index"] for r in rows]
    index_stats = {
        "n": len(rows), "min": round(min(vals), 4), "median": round(pct(vals, 0.5), 4),
        "mean": round(statistics.mean(vals), 4), "p90": round(pct(vals, 0.9), 4),
        "max": round(max(vals), 4),
        "ge60": sum(1 for v in vals if v >= 60), "eq100": sum(1 for v in vals if v >= 99.999),
    }

    lq_rows = sorted([r for r in rows if r["lq_2024"]], key=lambda r: -r["lq_2024"])
    lq_top = [{"ipc4": r["ipc4"], "lq_2024": round(r["lq_2024"], 4),
               "sz_2024": r["n2024"], "nat_2024": r["nat_2024"]} for r in lq_rows[:10]]
    lq_bottom = [{"ipc4": r["ipc4"], "lq_2024": round(r["lq_2024"], 4),
                  "sz_2024": r["n2024"], "nat_2024": r["nat_2024"]} for r in lq_rows[-10:]]

    top20 = [{"rank": r["rank"], "ipc4": r["ipc4"], "n_win": r["n_win"], "n2024": r["n2024"],
              "cagr": round(r["cagr"], 6), "recency": round(r["recency"], 4),
              "z_scale": round(r["z_scale"], 4), "z_growth": round(r["z_growth"], 4),
              "z_recency": round(r["z_recency"], 4), "heat_index": round(r["heat_index"], 2),
              "tier": r["tier"], "lq_2024": round(r["lq_2024"], 4) if r["lq_2024"] else None}
             for r in rows[:20]]
    bottom10 = [{"rank": r["rank"], "ipc4": r["ipc4"], "n_win": r["n_win"],
                 "cagr": round(r["cagr"], 6), "recency": round(r["recency"], 4),
                 "heat_index": round(r["heat_index"], 2), "tier": r["tier"]}
                for r in rows[-10:]]

    tier_top = {}
    for t in ("新兴", "短期热点", "长期趋势", "平稳", "降温"):
        sub = [r for r in rows if r["tier"] == t][:10]
        tier_top[t] = [{"ipc4": r["ipc4"], "heat_index": round(r["heat_index"], 2),
                        "cagr": round(r["cagr"], 6), "n2024": r["n2024"],
                        "vol": round(r["vol"], 4)} for r in sub]

    # 小基数外溢：2021 年不足 50 件的域，增长分母太小，z_growth 会被放大到 4—5 个标准差。
    # 本件不把它们剔除（2024 年绝对规模已不小），但给出「稳健基期（2021≥50）内」的次排名，
    # 供读者分辨「真热」与「小基数冲高」。
    stable = [r for r in rows if r["seq"][0] >= 50]
    stable_sorted = sorted(stable, key=lambda r: -r["heat_index"])
    rank_stable = {r["ipc4"]: i + 1 for i, r in enumerate(stable_sorted)}
    low_base_rows = [{"ipc4": r["ipc4"], "n2021": r["seq"][0], "n2024": r["n2024"],
                      "cagr": round(r["cagr"], 6), "heat_index": round(r["heat_index"], 2),
                      "rank_all": r["rank"]} for r in rows if r["seq"][0] < 50]

    payload = {
        "metric_id": MID,
        "generated_at": "2026-10-22",
        "main_db": "gkx @ 183.240.141.251:3318 (gkx_reader_zp, read-only)",
        "sql_count": 0,
        "caliber": {
            "subject": "深圳（申请人名称经企业底册归到深圳市）",
            "denominator": "深圳 2021—2024 年 IPC4 主分类归属性件数",
            "national_role": "仅作 LQ 分母（同一张表不混用两套分母）",
            "domain": "IPC4 = 主分类前 4 位",
            "window": "2021—2024（4 个完整年）",
            "guard": f"2024 年 ≥{GUARD} 件",
            "weights": {"scale": W[0], "growth": W[1], "recency": W[2]},
            "pseudo_count": PSEUDO,
        },
        "base_years_used": list(S.COMPLETE_YEARS),
        "base_years_missing": list(S.MISSING_BASE_YEARS),
        "base_years_note": (
            "基期与末期为库内真实存在的 2021 与 2024；CAGR 分母只用 2021（真实件数），"
            "2017—2020 在 dwd_patent 零行，不按 0 摊入、不做外推；2025/2026 属采集残年"
            "（全国 2025 覆盖 72.63%、2026 仅 12.33%），不进入窗口。"),
        "inputs": [
            {"path": "code/_snapshots21/patent_scan_20261021.pkl",
             "what": "深圳×年×IPC4 的去重 pn 集合",
             "source": "gkx.dwd_patent @ 183.240.141.251:3318，dwd_id 分页流式扫描，2026-10-21 21:30–23:50 产出"},
            {"path": "code/_snapshots21/patent_panel_innov_20261021.json",
             "what": "全国 IPC4×年（仅 LQ 分母）",
             "source": "gkx.dwd_patent @ 183.240.141.251:3318，2,939,895/2,939,895 全量，2026-10-22 08:23 产出"},
        ],
        "coverage": {
            "sz_by_year": {str(y): sz_year[y] for y in S.COMPLETE_YEARS},
            "nat_by_year": {str(y): nat_year[y] for y in S.COMPLETE_YEARS},
            "sz_share_of_nat_2024": round(sz_year[2024] / nat_year[2024], 4),
            "sz_domains_union": len({ipc for (ipc, y) in sz}),
            "sz_domains_2024": len(n2024),
            "qualified_domains": len(qual),
            "qualified_n2024": sum(r["n2024"] for r in rows),
            "qualified_share_2024": round(sum(r["n2024"] for r in rows) / sz_year[2024], 4),
        },
        "components_stats": {
            "ln_scale": {"mean": round(mu_s, 4), "sd": round(sd_s, 4)},
            "cagr": {"mean": round(mu_g, 6), "sd": round(sd_g, 6)},
            "recency": {"mean": round(mu_r, 4), "sd": round(sd_r, 4)},
            "vol_p67": round(vol_p67, 4),
        },
        "index_stats": index_stats,
        "tiers": {k: tiers[k] for k in ("新兴", "短期热点", "长期趋势", "平稳", "降温")},
        "tier_patent_2024": {k: tier_pat[k] for k in ("新兴", "短期热点", "长期趋势", "平稳", "降温")},
        "tier_top": tier_top,
        "lq_top10": lq_top,
        "lq_bottom10": lq_bottom,
        "top20": top20,
        "bottom10": bottom10,
        "stable_base": {
            "guard": "2021 年 ≥50 件（与 M_TECH_DEEP_139_1 的 50/100 双门槛一致）",
            "n": len(stable),
            "top10": [{"ipc4": r["ipc4"], "heat_index": round(r["heat_index"], 2),
                       "n2024": r["n2024"], "cagr": round(r["cagr"], 6),
                       "rank_all": r["rank"]} for r in stable_sorted[:10]],
            "low_base_excluded": len(low_base_rows),
            "low_base_rows": sorted(low_base_rows, key=lambda r: r["rank_all"]),
        },
        "new_code_domains": sorted([r["ipc4"] for r in rows if r["ipc4"].startswith(("H10B", "H10D", "H10F", "H10H", "H10K", "H10W", "H10N", "H10P"))]),
        "all_domains": [{"rank": r["rank"], "ipc4": r["ipc4"], "seq": r["seq"], "n_win": r["n_win"],
                         "cagr": round(r["cagr"], 6), "recency": round(r["recency"], 4),
                         "vol": round(r["vol"], 4), "lq_2024": round(r["lq_2024"], 4) if r["lq_2024"] else None,
                         "heat_index": round(r["heat_index"], 2), "tier": r["tier"],
                         "rank_stable": rank_stable.get(r["ipc4"])}
                        for r in rows],
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": ("专利单源的规模/增长/近端三维齐备，238 个域全部可算、指数非退化；"
                       "需求点名的多源输入（学术论文、新闻与技术博客、行业资讯、专家活动）"
                       "四项在库内均无「技术点」回连字段，无法合成，故落部分支持。"),
        },
    }
    S.write_out(MID, payload)
    print(json.dumps({"domains": len(rows), "tiers": payload["tiers"],
                      "index": index_stats, "qualified_share": payload["coverage"]["qualified_share_2024"]},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()

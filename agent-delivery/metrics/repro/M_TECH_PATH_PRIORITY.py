#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_TECH_PATH_PRIORITY —— 深圳技术点布局优先级（卡位 × 势头 × 体量）。

口径：深圳单口径（238 个 IPC4，与 M_TECH_HEAT_INDEX / M_TECH_PATH_KEYNODE 同域宇宙）。
三要素均为 238 点内百分位：卡位 P（桥接+跨部+强度）、势头 S（平滑 CAGR 与 2024 同比）、
体量 V（窗口件数 ln）。四套权重情景做稳定性检验，权重不敏感才允许发布排序。

零 SQL；直接跑：cd code && python3 M_TECH_PATH_PRIORITY.py
"""
from __future__ import annotations

import json
import math
from datetime import datetime

import _path_graph21 as P

METRIC_ID = "M_TECH_PATH_PRIORITY"
OUT = P.CODE / f"{METRIC_ID}_out.json"

PSEUDO = 50      # 平滑 CAGR 伪计数（与 M_TECH_HEAT_INDEX 同）
T1_CUT = 0.75
T2_CUT = 0.55
SCEN = {
    "S1 均衡": {"P": 0.40, "S": 0.35, "V": 0.25},
    "S2 卡位优先": {"P": 0.60, "S": 0.25, "V": 0.15},
    "S3 成长优先": {"P": 0.25, "S": 0.55, "V": 0.20},
    "S4 体量优先": {"P": 0.25, "S": 0.25, "V": 0.50},
}
WEIGHTS = SCEN["S1 均衡"]


def main():
    nodes, seq, cell = P.node_universe()
    g = P.build(nodes)
    adj = g["adj"]
    C = P.all_centralities(g)

    def pct_rank(vals):
        o = sorted(nodes, key=lambda x: vals[x])
        return {x: i / (len(o) - 1) for i, x in enumerate(o)}

    # ---- 卡位 P：与 KEYNODE 同一公式 ----
    cross = {x: sum(w for u, w in adj[x].items() if u[0] != x[0]) for x in nodes}
    p_bridge, p_cross, p_w = pct_rank(C["betweenness"]), pct_rank(cross), pct_rank(C["wdegree"])
    Pk = {x: 0.40 * p_bridge[x] + 0.35 * p_cross[x] + 0.25 * p_w[x] for x in nodes}

    # ---- 势头 S / 体量 V ----
    rows0 = []
    for x in nodes:
        s = seq[x]
        cagr = ((s[3] + PSEUDO) / (s[0] + PSEUDO)) ** (1 / 3) - 1
        yoy24 = (s[3] - s[2]) / s[2] if s[2] else None
        rows0.append({"ipc4": x, "seq": s, "n_win": sum(s), "n2024": s[3],
                      "cagr": cagr, "yoy24": yoy24, "ln_win": math.log(sum(s)) if sum(s) else 0.0})
    p_cagr = pct_rank({r["ipc4"]: r["cagr"] for r in rows0})
    p_yoy = pct_rank({r["ipc4"]: (r["yoy24"] if r["yoy24"] is not None else -1.0) for r in rows0})
    p_win = pct_rank({r["ipc4"]: r["ln_win"] for r in rows0})
    S_ = {r["ipc4"]: 0.60 * p_cagr[r["ipc4"]] + 0.40 * p_yoy[r["ipc4"]] for r in rows0}
    V_ = {x: p_win[x] for x in nodes}

    # ---- 热度复算：与 M_TECH_HEAT_INDEX 完全同式（规模 0.40 / 平滑 CAGR 0.35 / 近端 0.25）----
    def zvals(vals):
        mu = sum(vals) / len(vals)
        sd = (sum((v - mu) ** 2 for v in vals) / len(vals)) ** 0.5
        return [(v - mu) / sd if sd else 0.0 for v in vals], mu, sd

    ln_w = [r["ln_win"] for r in rows0]
    cg = [r["cagr"] for r in rows0]
    rc = [(r["seq"][2] + r["seq"][3]) / r["n_win"] if r["n_win"] else 0.0 for r in rows0]
    z_ln, _, _ = zvals(ln_w)
    z_cg, _, _ = zvals(cg)
    z_rc, _, _ = zvals(rc)
    raw = [0.40 * a + 0.35 * b + 0.25 * c for a, b, c in zip(z_ln, z_cg, z_rc)]
    lo, hi = min(raw), max(raw)
    heat = {r["ipc4"]: (100.0 * (v - lo) / (hi - lo) if hi > lo else 50.0) for r, v in zip(rows0, raw)}

    def blend(w):
        return {x: w["P"] * Pk[x] + w["S"] * S_[x] + w["V"] * V_[x] for x in nodes}

    sc = {k: blend(w) for k, w in SCEN.items()}
    base = sc["S1 均衡"]

    def topn(d, n=20):
        return {x for x in sorted(nodes, key=lambda z: -d[z])[:n]}

    stab = []
    for k in SCEN:
        if k == "S1 均衡":
            continue
        stab.append({"scenario": k, "weights": SCEN[k],
                     "tau_vs_base": round(P.spearman([base[x] for x in nodes], [sc[k][x] for x in nodes]), 4),
                     "top20_overlap": len(topn(base) & topn(sc[k]))})
    tau_min = min(s["tau_vs_base"] for s in stab)
    ov_min = min(s["top20_overlap"] for s in stab)

    if tau_min >= 0.90 and ov_min >= 18:
        support = "完全转换支持"
    elif tau_min >= 0.75 and ov_min >= 14:
        support = "部分支持"
    else:
        support = "不支持"

    def tier(x):
        if base[x] >= T1_CUT:
            return "T1 优先布局"
        if base[x] >= T2_CUT:
            return "T2 重点跟进"
        return "T3 观察"

    # 交叉验证：与 M_TECH_HEAT_INDEX 的逐点一致性（可选，文件存在才校验）
    crosschk = {"status": "skipped"}
    hp = P.CODE / "M_TECH_HEAT_INDEX_out.json"
    if hp.exists():
        try:
            hd = json.loads(hp.read_text(encoding="utf-8"))
            hmap = {r["ipc4"]: r["heat_index"] for r in hd["all_domains"]}
            diff = max(abs(hmap[x] - heat[x]) for x in nodes if x in hmap)
            crosschk = {"status": "ok", "n": len([x for x in nodes if x in hmap]),
                        "max_abs_diff": round(diff, 6)}
        except Exception as e:  # 兄弟件缺失/格式变更不影响本件成文
            crosschk = {"status": "error", "detail": str(e)[:80]}

    rows = []
    for r in rows0:
        x = r["ipc4"]
        rows.append({
            "ipc4": x, "seq": r["seq"], "n_win": r["n_win"], "n2024": r["n2024"],
            "cagr": round(r["cagr"], 6), "yoy24": round(r["yoy24"], 4) if r["yoy24"] is not None else None,
            "P": round(Pk[x], 4), "S": round(S_[x], 4), "V": round(V_[x], 4),
            "pct_bridge": round(p_bridge[x], 3), "pct_cross": round(p_cross[x], 3),
            "pct_strength": round(p_w[x], 3), "degree": C["degree"][x],
            "priority": round(base[x], 4), "tier": tier(x),
            "priority_S2": round(sc["S2 卡位优先"][x], 4),
            "priority_S3": round(sc["S3 成长优先"][x], 4),
            "priority_S4": round(sc["S4 体量优先"][x], 4),
        })
    rows.sort(key=lambda r: -r["priority"])
    for i, r in enumerate(rows, 1):
        r["rank"] = i

    tiers = {t: sum(1 for r in rows if r["tier"] == t) for t in ("T1 优先布局", "T2 重点跟进", "T3 观察")}
    tier_pat = {t: sum(r["n2024"] for r in rows if r["tier"] == t) for t in tiers}
    n2024_total = sum(r["n2024"] for r in rows)

    tiersheets = {}
    for t in tiers:
        sub = [r for r in rows if r["tier"] == t][:12]
        tiersheets[t] = [{"rank": r["rank"], "ipc4": r["ipc4"], "priority": r["priority"],
                          "P": r["P"], "S": r["S"], "V": r["V"], "cagr": r["cagr"],
                          "n2024": r["n2024"]} for r in sub]

    # 与热度榜、卡位榜的重合（说明三件不是同一张榜换个马甲）
    heat_top = set()
    if hp.exists():
        try:
            hd = json.loads(hp.read_text(encoding="utf-8"))
            heat_top = {r["ipc4"] for r in hd["top20"]}
        except Exception:
            heat_top = set()
    kp = P.CODE / "M_TECH_PATH_KEYNODE_out.json"
    key_top = set()
    if kp.exists():
        try:
            key_top = {r["ipc4"] for r in json.loads(kp.read_text(encoding="utf-8"))["t1"]}
        except Exception:
            key_top = set()

    out = {
        "metric_id": METRIC_ID,
        "metric_name": "技术路径优先级（卡位 × 势头 × 体量）",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": P.SOURCE,
        "caliber": "深圳单口径；全国不参与，无 LQ 分母",
        "support_level": support,
        "support_judgment": support,
        "support_note": f"四情景两两 Spearman 最低 {tau_min}，top20 最小保留 {ov_min} 个 → 权重不敏感度{'达标' if support=='完全转换支持' else '仅部分达标'}",
        "weights": WEIGHTS,
        "scenarios": SCEN,
        "rules": {"t1_cut": T1_CUT, "t2_cut": T2_CUT, "pseudo": PSEUDO},
        "universe": {"n_nodes": len(nodes), "n_edges": len(g["edges"]),
                     "n2024_total": n2024_total},
        "stability": stab,
        "crosscheck_heat": crosschk,
        "overlap_heat_top20": len(topn(base) & heat_top) if heat_top else None,
        "overlap_keynode_t1": len(topn(base, 30) & key_top) if key_top else None,
        "tiers": tiers, "tier_patent_share": {k: round(v / n2024_total, 4) for k, v in tier_pat.items()},
        "tier_sheets": tiersheets,
        "score_stats": P.stats([base[x] for x in nodes]),
        "nodes": rows,
        "base_years_used": [2021, 2022, 2023, 2024],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": "势头用 2021→2024 平滑 CAGR 与 2024 同比；2025/2026 不入算（2026 残年）；库内 2017—2020 无专利行，不补零",
        "key_numbers": {
            "t1_n": tiers["T1 优先布局"], "t1_top": rows[0]["ipc4"], "t1_top_score": rows[0]["priority"],
            "t1_cover": round(tier_pat["T1 优先布局"] / n2024_total, 4),
            "tau_min": tau_min, "top20_ov_min": ov_min,
            "overlap_heat20": len(topn(base) & heat_top) if heat_top else None,
        },
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("done ->", OUT)
    print(json.dumps({"support": support, "tau_min": tau_min, "ov_min": ov_min,
                      "tiers": tiers, "crosscheck": crosschk,
                      "top10": [(r["ipc4"], r["priority"], r["tier"]) for r in rows[:10]]},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()

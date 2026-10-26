#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_POLICY_DEEP_170_1｜政策机遇识别模型（王惠四步口径，零 SQL 复现）

四步：
  1) 五子指标截面极值归一到 0—100；
  2) 关注度 = 主题密度 + 关键词聚合强度 等权；影响力 = 部门覆盖 + 政策引用 等权；
     稳定性 = 发文持续性；
  3) 三维等权合成（缺维不进平均）；
  4) 综合分 ≥60 计为机遇政策，机遇计数 = 通过条数。

数据：只读 code/_snapshots21 下四份快照，不连数据库。
  policy_base_20261021.json        20,000 行（id/title/theme 标志）
  pg_policy_rows_20261021.json     20,000 行（title/ministry/publish_year）
  policy_aux_20261022.json         theme/quote_policy 真实值 2 行（gkx 补探）
  M_POLICY_DEEP_170_1_out.json     由本脚本覆盖写出

注意：theme 全表真实值只有 2 行、keywords 0 行、quote_policy 2 行。王惠五子指标中
关键词聚合强度整维不可算，主题/部门/引用/持续四个子指标只在 2 条政策上有值。
min-max 归一在 n=2 时必然产出 0 与 100，这个「区分度」是归一化假象，不是政策差异，
故主口径仍按王惠「主题字符串」分组（两条政策各成一组），并单列方向展开敏感性。
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_POLICY_DEEP_170_1_out.json")

PLACEHOLDER = {"", "NULL", "NULL", "NONE", "-", "[]"}


def nn(v):
    if v is None:
        return ""
    s = str(v).strip()
    return "" if s.upper() in PLACEHOLDER or s == "null" else s


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def runlen(years):
    if not years:
        return 0
    ys = sorted(set(years))
    best = cur = 1
    for i in range(1, len(ys)):
        cur = cur + 1 if ys[i] == ys[i - 1] + 1 else 1
        best = max(best, cur)
    return best


def norm(vals):
    vals = [v for v in vals if v is not None]
    if not vals:
        return None, None
    lo, hi = min(vals), max(vals)
    return lo, hi


def main():
    base = load("policy_base_20261021.json")
    rows = load("pg_policy_rows_20261021.json")
    aux = load("policy_aux_20261022.json")
    n = len(rows)

    theme_rows = {r["id"]: r for r in aux["probes"].get("theme_quote_rows", [])}
    theme_fields = {r["id"]: r for r in aux["probes"].get("theme_row_fields", [])}

    pol = []
    for r in rows:
        tid = r["id"]
        theme_raw = nn(theme_rows.get(tid, {}).get("theme"))
        quote_raw = nn(theme_rows.get(tid, {}).get("quote_policy"))
        year = None
        y = nn(r.get("publish_year"))
        if y.isdigit():
            year = int(y)
        pol.append(dict(id=tid, title=nn(r.get("title"))[:80], theme=theme_raw,
                        ministry=nn(r.get("ministry")), quote=quote_raw, year=year))

    # ---- 主题分组（主口径：theme 原字符串为一组；空不进） ----
    groups = {}
    for p in pol:
        if p["theme"]:
            groups.setdefault(p["theme"], []).append(p)

    theme_stats = []
    for t, ps in groups.items():
        years = [p["year"] for p in ps if p["year"]]
        ministries = {p["ministry"] for p in ps if p["ministry"]}
        theme_stats.append({
            "theme": t,
            "n_policies": len(ps),
            "n_ministries": len(ministries),
            "years": sorted(set(years)),
            "max_run_years": runlen(years),
            "n_quotes": sum(1 for p in ps if p["quote"]),
        })

    # ---- 五子指标原始值 ----
    subs = []
    for p in pol:
        t = p["theme"]
        grp = groups.get(t, [])
        subs.append({
            "theme_den": len(grp) if t else None,
            "dens": None,                       # keywords 整列为空 → 不可算
            "mcnt": len({x["ministry"] for x in grp if x["ministry"]}) if t else None,
            "qp": (1 if p["quote"] else None) if t else None,
            "cont": runlen([x["year"] for x in grp if x["year"]]) if t else None,
        })

    # ---- 极值归一（缺值不参与；同值取 50） ----
    lo_hi = {k: norm([s[k] for s in subs]) for k in ("theme_den", "dens", "mcnt", "qp", "cont")}
    z = {}
    for k, (lo, hi) in lo_hi.items():
        idx = {}
        for i, s in enumerate(subs):
            if s[k] is None:
                continue
            idx[i] = 50.0 if (lo is None or hi == lo) else (s[k] - lo) / (hi - lo) * 100
        z[k] = idx

    att, infl, stab = [], [], []
    for i in range(n):
        pa = [z[k][i] for k in ("theme_den", "dens") if i in z[k]]
        pi = [z[k][i] for k in ("mcnt", "qp") if i in z[k]]
        att.append(sum(pa) / len(pa) if pa else None)
        infl.append(sum(pi) / len(pi) if pi else None)
        stab.append(z["cont"].get(i))

    scores = []
    for i in range(n):
        vs = [v for v in (att[i], infl[i], stab[i]) if v is not None]
        scores.append(sum(vs) / len(vs) if vs else None)

    scored = [s for s in scores if s is not None]
    n_opp = sum(1 for s in scored if s >= 60)
    scored_sorted = sorted(scored)

    # ---- 方向展开敏感性（按 theme 数组逐条展开，仅 2 条政策） ----
    direction_stats = {}
    for r in aux["probes"].get("theme_quote_rows", []):
        f = theme_fields.get(r["id"], {})
        raw = nn(r["theme"])
        items = []
        if raw.startswith("["):
            try:
                items = [str(x).strip() for x in json.loads(raw) if str(x).strip()]
            except Exception:
                items = [x.strip(" \"'") for x in raw.strip("[]").split(",") if x.strip(" \"'")]
        for t in items:
            d = direction_stats.setdefault(t, {"theme": t, "n_policies": 0, "years": set(),
                                               "n_quotes": 0, "n_ministries": set()})
            d["n_policies"] += 1
            if f.get("content_len"):
                pass
            if r.get("quote_policy"):
                d["n_quotes"] += 1
            # 该政策年份从主表补
            y = next((p["year"] for p in pol if p["id"] == r["id"]), None)
            if y:
                d["years"].add(y)
            m = next((p["ministry"] for p in pol if p["id"] == r["id"]), "")
            if m:
                d["n_ministries"].add(m)

    dir_rows = []
    for t, d in sorted(direction_stats.items(), key=lambda kv: (-kv[1]["n_policies"], kv[0])):
        dir_rows.append({"theme": t, "n_policies": d["n_policies"],
                         "n_ministries": len(d["n_ministries"]),
                         "years": sorted(d["years"]),
                         "n_quotes": d["n_quotes"]})

    # 方向展开后，对每条政策取所辖方向的平均密度，再做 n=2 的 min-max
    per_policy_dir = {}
    for r in aux["probes"].get("theme_quote_rows", []):
        raw = nn(r["theme"])
        try:
            items = [str(x).strip() for x in json.loads(raw)] if raw.startswith("[") else []
        except Exception:
            items = []
        vals = [direction_stats[t]["n_policies"] for t in items if t in direction_stats]
        per_policy_dir[r["id"]] = sum(vals) / len(vals) if vals else None
    vals = [v for v in per_policy_dir.values() if v is not None]
    sens_scores = []
    if len(vals) == 2 and max(vals) > min(vals):
        for v in vals:
            dens_z = (v - min(vals)) / (max(vals) - min(vals)) * 100
            sens_scores.append(round((dens_z + 50.0 + 50.0) / 3.0, 2))

    out = {
        "metric_id": "M_POLICY_DEEP_170_1",
        "title": "政策机遇识别模型",
        "probe_date": "2026-10-22",
        "data_support_level": "部分支持",
        "support_judgment": "部分支持",
        "support_reason": ("王惠五子指标中关键词聚合强度整列无值（keywords 0/20,000）；"
                           "主题密度、部门覆盖、政策引用、发文持续性四个子指标只对 2 条政策有值，"
                           "20,000 条里 19,998 条因 theme 缺失无法分组 → 有必需子指标始终无法取值，判部分支持。"),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("本指标为截面评分，不设跨年基期，故 used/missing 均为空。"
                            "publish_year 仅用于「发文持续性」的连续年计数（两条 theme 政策分别为 2015、2010 年），"
                            "不进入任何增长率分母。政策表 2022 年后为采集残片（2023 年 0 行），"
                            "任何年度趋势都不做外推。"),
        "sources": {
            "policy_base": "code/_snapshots21/policy_base_20261021.json（20,000 行 theme 标志）",
            "pg_policy_rows": "code/_snapshots21/pg_policy_rows_20261021.json（title/ministry/publish_year）",
            "policy_aux": "code/_snapshots21/policy_aux_20261022.json（source=gkx@183.240.141.251:3318，theme/quote_policy 真实值 2 行）",
            "db": "gkx @ 183.240.141.251:3318（只读；本脚本零 SQL）",
        },
        "population": {
            "rows": n,
            "rows_with_theme": sum(1 for p in pol if p["theme"]),
            "theme_fill_pct": round(100.0 * sum(1 for p in pol if p["theme"]) / n, 4),
            "rows_with_quote": sum(1 for p in pol if p["quote"]),
            "keywords_fill": 0,
            "n_directions": len(direction_stats),
        },
        "subindicator_availability": {
            "theme_density": {"available": True, "n_scored": sum(1 for s in subs if s["theme_den"] is not None)},
            "keyword_density": {"available": False, "n_scored": 0,
                                "note": "keywords 全表 0 条非占位符，关键词聚合强度整维不可算"},
            "ministry_cover": {"available": True, "n_scored": sum(1 for s in subs if s["mcnt"] is not None)},
            "policy_quote": {"available": True, "n_scored": sum(1 for s in subs if s["qp"] is not None)},
            "continuity": {"available": True, "n_scored": sum(1 for s in subs if s["cont"] is not None)},
        },
        "theme_groups": theme_stats,
        "direction_rows": dir_rows,
        "scores": {
            "n_policies_scored": len(scored),
            "n_opportunity_ge60": n_opp,
            "score_min": round(scored_sorted[0], 2) if scored_sorted else None,
            "score_max": round(scored_sorted[-1], 2) if scored_sorted else None,
            "score_p50": round(scored_sorted[len(scored_sorted) // 2], 2) if scored_sorted else None,
            "threshold": 60,
        },
        "sensitivity_direction_expansion": {
            "n_policies_scored": len(sens_scores),
            "scores": sens_scores,
            "n_opportunity_ge60": sum(1 for s in sens_scores if s >= 60),
            "note": ("把 theme 数组按方向展开后，2 条政策的主题密度均值分别为 "
                     f"{sorted(round(v, 2) for v in vals)}；n=2 的 min-max 必然把两者压成 0 与 100，"
                     "于是较密的一条会被推到 66.67 分「过线」。这是归一化假象，不能读成「发现 1 条政策机遇」；"
                     "主口径不采用该展开，只作为脆弱性披露。"),
        },
        "verdict": ("机遇计数 = 0（王惠口径）。0 不是「政策体系没有机遇」的证据，"
                    "而是 theme/keywords/quote 三列近全空导致 19,998 条政策无法进入评分；"
                    "该结论只能作「不可判」使用，不得对外发布为机遇为零。"),
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print(json.dumps({k: out[k] for k in ("metric_id", "support_judgment", "population",
                                          "scores", "verdict")}, ensure_ascii=False, indent=1))
    print("theme_groups:", json.dumps(theme_stats, ensure_ascii=False))
    print("directions:", json.dumps(dir_rows, ensure_ascii=False))
    print("->", OUT)


if __name__ == "__main__":
    main()

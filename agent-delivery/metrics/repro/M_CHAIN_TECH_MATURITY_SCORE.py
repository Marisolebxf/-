#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_TECH_MATURITY_SCORE 技术成熟度评分（链级，0—100）。

口径：与注册表 `cfg_metric-CHAIN-seed.yaml` 及 calc-logic
`metrics/calc-logic/CHAIN/M_CHAIN_TECH_MATURITY_SCORE.md` 逐条一致——
以链上企业专利按公开年汇总的近 k 年复合增速判定生命周期位置：

    g_t = (P_t / P_{t-k})^(1/k) - 1,        k = 3
    无公开 0 ｜ 萌芽 25 ｜ 成长 50 ｜ 趋于成熟 70 ｜ 成熟 90 ｜ 衰退 90·P_t/P_{t-k}

与区域件 `M_CHAIN_REG_TECH_MATURITY`（链 × 城）的区别只有聚合层级：那件按
城切开，本件把四城与省外合并成链级。两者共用同一份面板、同一套阈值，
因此同向性可以在脚本里直接对账（`reconciliation`）。

三处受限期（与区域件一致，MD §三/§四 披露）：
  1. 面板只有申请年窗口 2021—2024（`app_year` 2,424,684 行，占全表 2,939,895
     的 82.48%），无 `pbdt_year` 缓存 → 用申请年代理公开年；
  2. 2017—2020 在 `dwd_patent` 零行 → 上期增速只能用 k=2（2021→2023）回算；
  3. 2025/2026 是采集残年（2026 仅 74,810 件）→ 统计年固定 2024，不往前后外推。

零数据库：只读 `code/_snapshots21/` 下三份快照。
运行：cd code && python3 M_CHAIN_TECH_MATURITY_SCORE.py
"""
from __future__ import annotations

import json
from pathlib import Path

BASE = Path(__file__).parent
SNAP = BASE / "_snapshots21"
METRIC = "M_CHAIN_TECH_MATURITY_SCORE"

ROOTS = ["INB1204", "INB1209", "INB1236", "INB1303", "INB1306", "INB1309",
         "INB1323", "INB1333", "INB1354", "INB1502", "INB2503", "INB2505"]
THETA = 0.05
STAT_YEAR = 2024
K = 3
YEARS = [2021, 2022, 2023, 2024]


def load(name):
    return json.loads((SNAP / name).read_text(encoding="utf-8"))


def cagr(p0, p1, k):
    if p0 is None or p1 is None or p0 <= 0:
        return None
    return (p1 / p0) ** (1.0 / k) - 1.0


def score_chain(p):
    """注册表映射原文实现；返回 (stage, score, g, g_prev)。"""
    g = cagr(p.get(STAT_YEAR - K), p.get(STAT_YEAR), K)
    g_prev = cagr(p.get(2021), p.get(2023), 2)
    if p.get(STAT_YEAR, 0) <= 0 and p.get(STAT_YEAR - K, 0) <= 0:
        return "无公开", 0.0, g, g_prev
    if p.get(STAT_YEAR - K, 0) <= 0 and p.get(STAT_YEAR, 0) > 0:
        return "萌芽", 25.0, g, g_prev
    if g is not None and g > THETA:
        if g_prev is not None and g < g_prev:
            return "趋于成熟", 70.0, g, g_prev
        return "成长", 50.0, g, g_prev
    if g is not None and abs(g) <= THETA:
        return "成熟", 90.0, g, g_prev
    if g is not None and g < -THETA:
        s = round(min(90.0, max(0.0, 90.0 * p[STAT_YEAR] / p[STAT_YEAR - K])), 2)
        return "衰退", s, g, g_prev
    return "无公开", 0.0, g, g_prev


def spearman(a, b):
    def rank(xs):
        order = sorted(range(len(xs)), key=lambda i: xs[i])
        r = [0.0] * len(xs)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1
            for t in range(i, j + 1):
                r[order[t]] = avg
            i = j + 1
        return r

    ra, rb = rank(a), rank(b)
    n = len(a)
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    da = sum((x - ma) ** 2 for x in ra) ** 0.5
    db = sum((y - mb) ** 2 for y in rb) ** 0.5
    return round(num / (da * db), 4) if da and db else None


def main():
    panel = load("patent_panel_innov_20261021.json")
    idx = load("chain_firm_index_20261023.json")
    tree = load("chain_tree_20261021.json")
    chain_name = {r["industry_code"]: r["industry_name"] for r in tree if len(r["industry_code"]) == 7}
    name_chain = idx["name_chain"]

    # ---- 链 × 年 件数：专利一经第一申请人归链（申请人名 → 链的唯一映射）
    cells = {c: {} for c in ROOTS}
    matched_patents = 0
    matched_names = set()
    for key, n in panel["app_year"].items():
        y, _, nm = key.partition("|")
        ch = name_chain.get(nm)
        if not ch:
            continue
        matched_patents += n
        matched_names.add(nm)
        cells.setdefault(ch, {})
        cells[ch][y] = cells[ch].get(y, 0) + n

    per_chain = []
    for ch in ROOTS:
        p = {y: int(round(cells.get(ch, {}).get(str(y), 0))) for y in YEARS}
        stage, score, g, g_prev = score_chain(p)
        per_chain.append({
            "industry_code": ch,
            "industry_name": chain_name[ch],
            "chain_firms": idx["chain_firms"].get(ch),
            "patents_by_year": p,
            "p_sum_2021_2024": sum(p.values()),
            "g_2021_2024": None if g is None else round(g, 6),
            "g_prev_2021_2023_k2": None if g_prev is None else round(g_prev, 6),
            "stage": stage,
            "score": score,
            "patent_per_firm": round(sum(p.values()) / idx["chain_firms"][ch], 6)
            if idx["chain_firms"].get(ch) else None,
        })

    # ---- 对账 1：与区域件（链 × 城）同向
    recon = {"available": False}
    reg_path = BASE / "M_CHAIN_REG_TECH_MATURITY_out.json"
    if reg_path.exists():
        reg = json.loads(reg_path.read_text(encoding="utf-8"))
        reg_by_chain = {}
        for city, rows in reg.get("by_city_score", {}).items():
            for r in rows:
                reg_by_chain.setdefault(r["chain"], []).append(r["score"])
        mine = {p["industry_name"]: p["score"] for p in per_chain}
        pairs = [(c, sum(v) / len(v), mine[c]) for c, v in reg_by_chain.items() if c in mine]
        reg_stage = {}
        for city, rows in reg.get("by_city_score", {}).items():
            for r in rows:
                reg_stage.setdefault(r["chain"], []).append(r["stage"])
        my_stage = {p["industry_name"]: p["stage"] for p in per_chain}
        same_stage = sum(
            1 for c in reg_stage
            if c in my_stage and max(set(reg_stage[c]), key=reg_stage[c].count) == my_stage[c]
        )
        recon = {
            "available": True,
            "source": "code/M_CHAIN_REG_TECH_MATURITY_out.json",
            "note": "区域件是链 × 城 48 格；本件把 4 城合并成链级，两者同一面板、同一阈值。",
            "spearman_chain_score_vs_city_mean": spearman([p[1] for p in pairs], [p[2] for p in pairs]),
            "n_pairs": len(pairs),
            "same_stage_chains": same_stage,
            "stage_diff_chains": [
                {"chain": c,
                 "city_stages": {s: reg_stage[c].count(s) for s in set(reg_stage[c])},
                 "chain_stage": my_stage.get(c)}
                for c in reg_stage if c in my_stage
                and max(set(reg_stage[c]), key=reg_stage[c].count) != my_stage[c]
            ],
        }

    # ---- 对账 2：与 M_TECH_MATURITY_LEVEL（IPC4 域级）方向一致性
    lvl_path = BASE / "M_TECH_MATURITY_LEVEL_out.json"
    lvl = {"available": False}
    if lvl_path.exists():
        d = json.loads(lvl_path.read_text(encoding="utf-8"))
        dist = d.get("level_distribution", {})
        lvl = {
            "available": True,
            "source": "code/M_TECH_MATURITY_LEVEL_out.json",
            "scope": d.get("scope_statement", "")[:120],
            "level_domains": {k: v.get("domains") for k, v in dist.items()},
            "note": (
                "该件是深圳 IPC4 域级五因子等级（L1—L5），与链级增速分不是同一算法，"
                "只做方向对账：域级高成熟占比越高，链级应有更多「成熟/趋于成熟」，"
                "不做数值互换。"
            ),
        }

    scores = sorted(p["score"] for p in per_chain)
    stage_dist = {}
    for p in per_chain:
        stage_dist[p["stage"]] = stage_dist.get(p["stage"], 0) + 1

    out = {
        "metric_id": METRIC,
        "metric_name": "技术成熟度评分",
        "unit": "分（0—100）",
        "definition": (
            "指定产业链上，以链上企业专利按公开年汇总的近 3 年复合增速判定技术"
            "所处生命周期位置，输出 0—100 分；分值越高表示公开量增速越趋缓、"
            "技术越接近成熟。"
        ),
        "formula": (
            "g_t=(P_t/P_{t-k})^(1/k)-1；P 连续为 0 评 0；上期 0 且本期有量评 25；"
            "g>5% 且（加速或缺上期）评 50；g>5% 且减速评 70；|g|<=5% 评 90；"
            "g<-5% 评 90×P_t/P_{t-k} 并截断到 [0,90)"
        ),
        "support_judgment": "部分支持",
        "params": {
            "theta": THETA,
            "stat_year": STAT_YEAR,
            "k": K,
            "time_axis": "apdt_year（申请年，代公开年）",
            "window": [YEARS[0], YEARS[-1]],
        },
        "data_sources": {
            "panel": "code/_snapshots21/patent_panel_innov_20261021.json",
            "chain_index": "code/_snapshots21/chain_firm_index_20261023.json",
            "tree": "code/_snapshots21/chain_tree_20261021.json",
        },
        "coverage": {
            "panel_rows": panel.get("rows"),
            "panel_total_rows": 2939895,
            "panel_share": round(panel.get("rows", 0) / 2939895, 6),
            "app_year_rows": sum(panel["app_year"].values()),
            "applicant_names_total": len(panel.get("app_total", {})),
            "chain_matched_names": len(name_chain),
            "names_used": len(matched_names),
            "patents_matched": matched_patents,
            "patents_matched_share": round(matched_patents / panel.get("rows", 1), 6),
            "scanned_years": YEARS,
            "years_not_in_panel": [2025, 2026],
            "chain_firms_total": 1714457,
        },
        "headline": {
            "chains": len(per_chain),
            "score_min": scores[0],
            "score_max": scores[-1],
            "stage_dist": stage_dist,
            "patents_2021_2024": sum(p["p_sum_2021_2024"] for p in per_chain),
        },
        "per_chain": per_chain,
        "reconciliation": {"reg_tech_maturity": recon, "tech_maturity_level": lvl},
        "why_partial": (
            "三个必需条件都只能降级满足：① 时间轴用申请年代理公开年；② 只有 "
            "2021—2024 四年可用，2017—2020 零行使上期增速降为 k=2；③ 专利按"
            "申请人名匹配链上企业，匹配到的件数只占全表 30.05%，且匹配偏向"
            "有专利的大企业。方法与映射完全可执行，故不是「完全不支持」；"
            "但任一条件都不足以支撑「技术成熟度」的严格语义，故判部分支持。"
        ),
        "base_years_used": YEARS,
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": (
            "统计年 2024，主窗口 k=3（2021→2024），上期增速用 2021→2023 的 k=2 年化值。"
            "2017—2020 在 dwd_patent 零行，未按 0 摊入任何分母或均值；2025/2026 为"
            "采集残年（2026 仅 74,810 件）且不在面板 app_year 窗口内，主动排除，"
            "不参与涨跌判定。"
        ),
    }

    dst = BASE / f"{METRIC}_out.json"
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{METRIC}: scores {scores[0]}..{scores[-1]} stage={stage_dist} "
          f"matched={matched_patents}")
    for p in per_chain:
        print(" ", p["industry_name"], p["patents_by_year"], p["stage"], p["score"])


if __name__ == "__main__":
    main()

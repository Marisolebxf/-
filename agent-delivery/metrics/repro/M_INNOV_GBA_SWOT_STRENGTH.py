#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_GBA_SWOT_STRENGTH · 湾区创新能力优势因素（20261021 换源版）

旧稿公式（照抄）
----------------
优势 = 城市在 12 个分项上面向 11 城的降序排名 ≤3 的分项；
每条给「具体表现」（原值）与「影响程度」（0—1 归一）。

换源后的硬事实
--------------
1. 面板只有 4 城可算（其余 7 城实体基数近零），排名 ≤3 在 4 城上等价于
   **「不是最后一名」**：设计入选率 3/11=27.3%，实际 3/4=75%。本件保留原规则，
   同时单列 `strong_advantage`（rank≤2 且 norm≥0.5）作为可区分替代，并标「需甲方确认」。
2. 12 分项里「政策覆盖」缺 theme 不可算，实际 11 项；「载体产出」与资源维重复计位，
   在汇总里标 `duplicate_with`，不重复计入强优势条数。
3. 归一采用四城 min-max，仅用于「影响程度」，不改变排名。

输出：`code/M_INNOV_GBA_SWOT_STRENGTH_out.json`
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
FACT = SNAP / "gba_factors_20261021.json"
RD = SNAP / "gba_rd_20261021.json"
PAPER = SNAP / "papers_city_year_gkx21.json"
OUT = HERE / "M_INNOV_GBA_SWOT_STRENGTH_out.json"
METRIC = "M_INNOV_GBA_SWOT_STRENGTH"
NAME = "湾区创新能力优势因素"

CITY_SHORT = {"深圳": "深圳市", "广州": "广州市", "东莞": "东莞市", "惠州": "惠州市"}
CITIES = ["深圳", "广州", "东莞", "惠州"]
LABEL = {
    "专利资源": "专利授权/申请存量（2021—2024）",
    "论文资源": "第一作者城市论文数（2021—2023）",
    "研发投入": "上市主体研发费用合计（2019—2024，亿元）",
    "载体数量": "企业法人 + 科研院所数",
    "载体产出": "专利数 + 论文数（与资源维重复计位）",
    "科技型机构": "高企 + 科研院所数",
    "联合专利": "多申请人专利数（20,000 pn 样本）",
    "合作项目": "多机构参与项目数（2021—2023）",
    "成果转化": "专利转移件数 / 专利数 ×10000",
    "政策供给": "政策条数（存量）",
    "政策覆盖": "政策主题覆盖率（缺 theme，不可算）",
    "高企密度": "高企数 / 企业法人数 ×100",
}
DUPLICATE = {"载体产出": "与「专利资源」「论文资源」同源"}


def minmax(d):
    vals = [v for v in d.values() if v is not None]
    if not vals:
        return {}
    lo, hi = min(vals), max(vals)
    if hi - lo <= 1e-12:
        return {k: 0.5 for k in d if d[k] is not None}
    return {k: (v - lo) / (hi - lo) for k, v in d.items() if v is not None}


def main() -> None:
    fact = json.loads(FACT.read_text(encoding="utf-8"))
    rd = json.loads(RD.read_text(encoding="utf-8"))
    paper = json.loads(PAPER.read_text(encoding="utf-8"))["first_city_year"]

    paper3 = {c: 0 for c in CITIES}
    for k, v in paper.items():
        city, y = k.rsplit("|", 1)
        short = city.replace("市", "").replace("特别行政区", "")
        if short in paper3 and y in ("2021", "2022", "2023"):
            paper3[short] += int(v)

    inst = {"深圳": 1014, "广州": 822, "东莞": 127, "惠州": 111}
    org = {c: fact["org"][c] for c in CITIES}
    ht = {c: fact["hightech"][c] for c in CITIES}
    patent = {c: fact["patent"][c] for c in CITIES}
    raw = {
        "专利资源": patent,
        "论文资源": paper3,
        "研发投入": {c: rd["by_city_sum_yi"][CITY_SHORT[c]] for c in CITIES},
        "载体数量": {c: org[c] + inst[c] for c in CITIES},
        "载体产出": {c: patent[c] + paper3[c] for c in CITIES},
        "科技型机构": {c: ht[c] + inst[c] for c in CITIES},
        "联合专利": {c: fact["joint"][c] for c in CITIES},
        "合作项目": {c: fact["project"][c] for c in CITIES},
        "成果转化": {c: round(10000.0 * fact["transfer"][c] / patent[c], 4) if patent[c] else None for c in CITIES},
        "政策供给": {c: fact["policy"][c] for c in CITIES},
        "政策覆盖": None,
        "高企密度": {c: round(100.0 * ht[c] / org[c], 4) if org[c] else None for c in CITIES},
    }
    norm = {k: (minmax(v) if isinstance(v, dict) else {}) for k, v in raw.items()}

    rank = {}
    for i, d in raw.items():
        if not isinstance(d, dict):
            continue
        order = sorted([c for c in CITIES if d.get(c) is not None], key=lambda c: -d[c])
        rank[i] = {c: order.index(c) + 1 for c in order}

    strengths = {c: [] for c in CITIES}
    strong = {c: [] for c in CITIES}
    for i, rk in rank.items():
        for c, r in rk.items():
            if r <= 3:
                rec = {"factor": i, "label": LABEL[i], "rank": r, "of": len(rk),
                       "raw": raw[i][c], "impact_norm": round(norm[i].get(c, 0), 4)}
                if i in DUPLICATE:
                    rec["duplicate_with"] = DUPLICATE[i]
                strengths[c].append(rec)
                if r <= 2 and norm[i].get(c, 0) >= 0.5 and i not in DUPLICATE:
                    strong[c].append(rec)

    counts = {c: len(strengths[c]) for c in CITIES}
    strong_counts = {c: len(strong[c]) for c in CITIES}
    avg_impact = {c: round(sum(x["impact_norm"] for x in strengths[c]) / len(strengths[c]), 4)
                  if strengths[c] else None for c in CITIES}

    report = {
        "metric_id": METRIC,
        "metric_name": NAME,
        "date": "2026-10-22",
        "data_source": (
            "gkx @ 183.240.141.251:3318（只读）：dwd_patent / dwd_zh_paper / "
            "dwd_org_stock_finance_info / dwd_org_base_info / dwd_org_tech_tag / "
            "dwd_zh_project / dwd_patent_transfer / dwd_policy_base；经 _snapshots21 复用"
        ),
        "formula": "advantage = 分项在 4 城降序排名 ≤3；impact = 四城 min-max 归一；strong = rank≤2 ∧ norm≥0.5 ∧ 非重复计位",
        "rule_contract": {
            "designed_cities": 11,
            "designed_cutoff": 3,
            "designed_selection_rate": round(3 / 11, 4),
            "actual_cities": 4,
            "actual_cutoff": 3,
            "actual_selection_rate": round(3 / 4, 4),
            "degenerate": True,
            "note": "4 城上 rank≤3 = 不是最后一名；75% 入选率是设计值的 2.75 倍，必须甲方确认替代规则。",
        },
        "items": {i: {"label": LABEL[i], "raw": raw[i], "rank": rank.get(i),
                      "norm": {c: round(norm[i].get(c, 0), 4) for c in CITIES} if i in norm else None,
                      "missing": i not in norm,
                      **({"duplicate_with": DUPLICATE[i]} if i in DUPLICATE else {})}
                  for i in LABEL},
        "strengths": strengths,
        "strong_advantage": strong,
        "counts": counts,
        "strong_counts": strong_counts,
        "avg_impact": avg_impact,
        "summary": {
            "cities": CITIES,
            "items_available": sum(1 for v in norm.values() if v),
            "items_total": 12,
            "missing": ["政策覆盖"],
            "rank1_counts": {c: sum(1 for x in strengths[c] if x["rank"] == 1) for c in CITIES},
        },
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": (
                f"11/12 分项可算、4 城清单全部可出；但面板只有 4/11 城，"
                "原规则「11 城 rank≤3」在 4 城上退化为「不是最后一名」，"
                f"实际入选率 75%（设计 27.3%），{min(counts.values())}–{max(counts.values())} 项/城，"
                "区分度低；政策覆盖缺失；载体产出与资源维重复计位；"
                "联合专利仅 20,000 pn 样本、研发投入仅上市主体。"
                "故判部分支持；`strong_advantage` 是可区分替代，但属本件自定义、需甲方确认。"
            ),
            "criteria": {
                "items_available": sum(1 for v in norm.values() if v),
                "cities": 4,
                "selection_rate_actual": 0.75,
                "selection_rate_designed": round(3 / 11, 4),
                "strong_rule_official": False,
                "duplicate_item": True,
            },
        },
        "base_years_used": [2019, 2020, 2021, 2022, 2023, 2024],
        "base_years_missing": [],
        "base_years_note": (
            "分项窗口不同：专利 2021—2024；论文 2021—2023（2024 年论文量属批次断层，排除）；"
            "研发投入 2019—2024（上市主体）；项目 2021—2023；转移 2021—2026；政策存量无年度窗口。"
            "used 为并集，未把缺年补 0。"
        ),
        "sources": [
            {"path": "code/_snapshots21/gba_factors_20261021.json", "role": "专利/项目/转移/联合/高企/机构/政策"},
            {"path": "code/_snapshots21/gba_rd_20261021.json", "role": "上市主体研发费用"},
            {"path": "code/_snapshots21/papers_city_year_gkx21.json", "role": "论文第一作者城"},
        ],
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print("counts", counts, "strong", strong_counts, "avg", avg_impact)
    for c in CITIES:
        print(c, [(x["factor"], x["rank"], x["impact_norm"]) for x in strengths[c]])
    print("wrote", OUT)


if __name__ == "__main__":
    main()

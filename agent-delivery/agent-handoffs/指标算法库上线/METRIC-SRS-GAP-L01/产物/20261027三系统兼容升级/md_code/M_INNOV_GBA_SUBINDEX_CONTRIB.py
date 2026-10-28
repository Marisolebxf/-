#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_GBA_SUBINDEX_CONTRIB · 湾区子指数贡献度（20261021 换源版）

旧稿公式（照抄）
----------------
四子指数（资源 / 载体 / 机制 / 环境）各由若干分项等权合成；
某城某子指数贡献 = 该城子指数得分 / 四城合计 ×100%；
分项先做四城 min-max 归一，缺失分项不补 0、其权重按可用分项均摊。

换源后的面板（4 城，11/12 分项可算）
------------------------------------
  资源：专利（2021—2024）、论文（2021—2023 第一作者城）、研发投入（2019—2024 上市主体）
  载体：机构数、载体产出（专利+论文）、科技型机构（高企+科研院所）
  机制：联合专利（20,000 pn 样本）、合作项目（2021—2023）、成果转化率（转移/专利）
  环境：政策供给（存量）、高企密度；**政策覆盖缺失**（theme 全空）
  —— 缺 1 项，环境维只剩 2 项；其余三维各 3 项。

权重声明
--------
子指数等权 0.25、子指数内分项等权，是**本件自定义、需甲方确认**；
calc-logic 只给四维框架，没有给分项权重。

输出：`code/M_INNOV_GBA_SUBINDEX_CONTRIB_out.json`
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
FACT = SNAP / "gba_factors_20261021.json"
PAT = SNAP / "gba_patent_20261021.json"
RD = SNAP / "gba_rd_20261021.json"
PAPER = SNAP / "papers_city_year_gkx21.json"
OUT = HERE / "M_INNOV_GBA_SUBINDEX_CONTRIB_out.json"
METRIC = "M_INNOV_GBA_SUBINDEX_CONTRIB"
NAME = "湾区子指数贡献度"

CITY_SHORT = {"深圳": "深圳市", "广州": "广州市", "东莞": "东莞市", "惠州": "惠州市"}
CITIES = ["深圳", "广州", "东莞", "惠州"]
SUB = {
    "资源": ["专利资源", "论文资源", "研发投入"],
    "载体": ["载体数量", "载体产出", "科技型机构"],
    "机制": ["联合专利", "合作项目", "成果转化"],
    "环境": ["政策供给", "政策覆盖", "高企密度"],
}
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
    pat = json.loads(PAT.read_text(encoding="utf-8"))
    rd = json.loads(RD.read_text(encoding="utf-8"))
    paper = json.loads(PAPER.read_text(encoding="utf-8"))["first_city_year"]

    paper3 = {c: 0 for c in CITIES}
    for k, v in paper.items():
        city, y = k.rsplit("|", 1)
        short = city.replace("市", "").replace("特别行政区", "")
        if short in paper3 and y in ("2021", "2022", "2023"):
            paper3[short] += int(v)

    # 科研院所数：city_family 的 inst 口径
    inst = {"深圳": 1014, "广州": 822, "东莞": 127, "惠州": 111}
    org = {c: fact["org"][c] for c in CITIES}
    ht = {c: fact["hightech"][c] for c in CITIES}
    patent = {c: fact["patent"][c] for c in CITIES}
    rd_yi = {c: rd["by_city_sum_yi"][CITY_SHORT[c]] for c in CITIES}
    transfer = {c: fact["transfer"][c] for c in CITIES}
    joint = {c: fact["joint"][c] for c in CITIES}
    project = {c: fact["project"][c] for c in CITIES}
    policy = {c: fact["policy"][c] for c in CITIES}

    raw = {
        "专利资源": patent,
        "论文资源": paper3,
        "研发投入": rd_yi,
        "载体数量": {c: org[c] + inst[c] for c in CITIES},
        "载体产出": {c: patent[c] + paper3[c] for c in CITIES},
        "科技型机构": {c: ht[c] + inst[c] for c in CITIES},
        "联合专利": joint,
        "合作项目": project,
        "成果转化": {c: round(10000.0 * transfer[c] / patent[c], 4) if patent[c] else None for c in CITIES},
        "政策供给": policy,
        "政策覆盖": None,
        "高企密度": {c: round(100.0 * ht[c] / org[c], 4) if org[c] else None for c in CITIES},
    }
    norm = {k: (minmax(v) if isinstance(v, dict) else {}) for k, v in raw.items()}

    item_weight = {}
    for s, items in SUB.items():
        avail = [i for i in items if norm.get(i)]
        for i in avail:
            item_weight[i] = round(0.25 / len(avail), 6)

    city = {}
    for c in CITIES:
        s_scores = {}
        for s, items in SUB.items():
            avail = [i for i in items if norm.get(i)]
            s_scores[s] = round(sum(norm[i].get(c, 0) for i in avail) / len(avail), 4) if avail else None
        overall = round(sum(norm[i].get(c, 0) * w for i, w in item_weight.items()), 6)
        city[c] = {"subindex": s_scores, "overall": overall}
    total_overall = sum(v["overall"] for v in city.values())

    item_contrib = {}
    for i, w in item_weight.items():
        item_contrib[i] = {}
        for c in CITIES:
            item_contrib[i][c] = round(100.0 * norm[i].get(c, 0) * w / total_overall, 2) if total_overall else None

    sub_share = {}
    for s in SUB:
        tot = sum(city[c]["subindex"][s] or 0 for c in CITIES)
        sub_share[s] = {c: (round(100.0 * (city[c]["subindex"][s] or 0) / tot, 2) if tot else None)
                        for c in CITIES}

    rank = {}
    for i, d in raw.items():
        if not isinstance(d, dict):
            continue
        order = sorted([c for c in CITIES if d.get(c) is not None], key=lambda c: -d[c])
        rank[i] = {c: order.index(c) + 1 for c in order}

    report = {
        "metric_id": METRIC,
        "metric_name": NAME,
        "date": "2026-10-22",
        "data_source": (
            "gkx @ 183.240.141.251:3318（只读）：dwd_patent / dwd_zh_paper / "
            "dwd_org_stock_finance_info / dwd_org_base_info / dwd_org_tech_tag / "
            "dwd_zh_project / dwd_patent_transfer / dwd_policy_base；经 _snapshots21 复用"
        ),
        "formula": (
            "子指数=可用分项 min-max 后等权平均；城贡献=城子指数/四城合计×100%；"
            "分项总贡献=norm×权重/Σ(norm×权重)×100%"
        ),
        "panel_scope": {
            "cities": CITIES,
            "cities_designed": 11,
            "why_4": "其余 7 城 org/hightech/policy 近零或为 0，11 城面板会出现大量 0 值假排名；旧稿同为 4 城。",
            "items_total": 12,
            "items_available": sum(1 for v in norm.values() if v),
            "items_missing": ["政策覆盖"],
            "subindex_items": {s: len([i for i in items if norm.get(i)]) for s, items in SUB.items()},
        },
        "weight_note": (
            "子指数 0.25 等权、子指数内分项等权，均为**本件自定义、需甲方确认**；"
            "calc-logic 未给分项权重。环境维缺政策覆盖，只剩 2 项，仍占 0.25 总权重。"
        ),
        "raw": raw,
        "normalized": {k: {c: round(v.get(c, 0), 4) for c in CITIES} for k, v in norm.items() if v},
        "rank": rank,
        "item_weight": item_weight,
        "item_contrib_pct": item_contrib,
        "subindex": {c: {**city[c]["subindex"], "overall": city[c]["overall"]} for c in CITIES},
        "subindex_share_pct": sub_share,
        "overall_share_pct": {c: round(100.0 * city[c]["overall"] / total_overall, 2) if total_overall else None
                              for c in CITIES},
        "overall_rank": {c: i + 1 for i, c in enumerate(
            sorted(CITIES, key=lambda x: -city[x]["overall"]))},
        "probes": {
            "patent_window": pat.get("window"),
            "patent_city_total": {c: pat["city_total"].get(CITY_SHORT[c], 0) for c in CITIES},
            "paper_years": "2021-2023（2024 为批次断层，排除）",
            "paper_2024_excluded": {c: paper.get(f"{CITY_SHORT[c]}|2024") for c in CITIES},
            "rd_window": rd.get("window"),
            "rd_orgs": {c: rd["orgs_by_city"].get(CITY_SHORT[c]) for c in CITIES},
            "joint_meta": fact.get("joint_meta"),
            "policy_total_nonnull": fact.get("policy_total_nonnull"),
            "contamination": fact.get("contamination"),
        },
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": (
                f"12 分项中 {sum(1 for v in norm.values() if v)} 项可算，4 城四子指数与贡献份额全部落盘；"
                "但政策覆盖因 theme 全空不可算，环境维只剩 2 项；"
                "面板只有 4/11 城（其余 7 城实体基数近零），不是完整湾区；"
                "联合专利只覆盖 20,000 pn（0.68%）、研发投入只覆盖上市主体（856 家）、"
                "载体产出与资源维重复计位；权重为自定义。"
                "故判部分支持，贡献份额只能作内部结构参考。"
            ),
            "criteria": {
                "items_available": sum(1 for v in norm.values() if v),
                "items_missing": 1,
                "cities": 4,
                "cities_designed": 11,
                "weights_official": False,
                "joint_sample_pn": 20000,
                "rd_listed_orgs": rd.get("orgs_total"),
            },
        },
        "base_years_used": [2019, 2020, 2021, 2022, 2023, 2024],
        "base_years_missing": [],
        "base_years_note": (
            "分项窗口不同：专利 2021—2024；论文 2021—2023（2024 年论文量 32,379 是 2023 年的 4.87 倍，"
            "属批次断层，排除）；研发投入 2019—2024（上市主体年报）；项目 2021—2023；"
            "转移 2021—2026；政策为存量（无年度窗口）。used 列出并集，未把任何缺年补 0。"
        ),
        "sources": [
            {"path": "code/_snapshots21/gba_factors_20261021.json", "role": "专利/项目/转移/联合/高企/机构/政策"},
            {"path": "code/_snapshots21/gba_patent_20261021.json", "role": "专利面板 2,939,895 行"},
            {"path": "code/_snapshots21/gba_rd_20261021.json", "role": "上市主体研发费用 856 家"},
            {"path": "code/_snapshots21/papers_city_year_gkx21.json", "role": "论文第一作者城 100,900 行"},
        ],
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print("items", report["panel_scope"]["items_available"], "overall", report["overall_share_pct"])
    for c in CITIES:
        print(c, report["subindex"][c], report["overall_rank"][c])
    print("wrote", OUT)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TECH_TOPIC_HEAT｜技术话题热度（专利 IPC + 论文中图分类 + 产业链新闻）。

零 SQL，只读三份已落盘快照：
  - `patent_ipc4_year_20261021.json`：dwd_patent IPC4 × 年 × 件数（2021—2026）
  - `f3_facts_20261023.json`：论文中图分类前缀、产业链字典、链新闻年度总量、负证据
  - `chain_news_year_20261023.json`：dwd_industry_chain_news_info 的
    `industry_code` JSON 数组 × 年 × 条数（108,052 行新闻的链级展开底表）

「技术词→主题」**没有官方映射**：
  - `dwd_tech_topic` 在 gkx 逐字命中 0 张表；
  - `dwd_industry_analysis_topics` 1,052 行只有 3 个不同 topic_name
    （Industry 1,000 / Company 49 / Industry overview 3），是字典残片；
  - IPC（专利）与中图分类（论文）两套分类没有官方对照表。
因此本件的主题字典是**自建映射**（`mapping_is_official=false`），规则逐条写在
`mapping_rule` 与 `topics[].ipc_prefixes/clc_prefixes` 里，任何下游引用都必须带这句声明。

运行：`cd code && python3 M_TECH_TOPIC_HEAT.py`
产物：`code/M_TECH_TOPIC_HEAT_out.json`
"""
from __future__ import annotations

import json
import math
import os
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_TECH_TOPIC_HEAT_out.json")

# 自建主题字典：顺序即优先级，一个 IPC4 只归一个主题。
# industry_kw 用于把 1,273 个产业链节点名映射到主题；一条新闻可命中多主题。
TOPICS = [
    {
        "topic": "人工智能与数字技术",
        "ipc_prefixes": ["G06N", "G06T", "G06V", "G06F", "G06Q", "G10L", "G06K", "H04N"],
        "clc_prefixes": ["TP"],
        "industry_kw": ["人工智能", "智能终端", "软件与信息服务", "数字创意"],
    },
    {
        "topic": "通信与网络",
        "ipc_prefixes": ["H04L", "H04W", "H04B", "H04J", "H04Q", "H04M"],
        "clc_prefixes": ["TN"],
        "industry_kw": ["通信", "网络"],
    },
    {
        "topic": "集成电路与电子元件",
        "ipc_prefixes": ["H10", "H01L", "H01R", "H01G", "H01C", "H03", "H05K", "H05F"],
        "clc_prefixes": ["TM"],
        "industry_kw": ["集成电路", "半导体", "传感器", "电子"],
    },
    {
        "topic": "电池储能与新能源",
        "ipc_prefixes": ["H01M", "H02J", "B60L", "H02S", "F03D", "H02K", "H02P", "H02N"],
        "clc_prefixes": ["TK", "TV"],
        "industry_kw": ["新能源", "储能", "电池", "光伏", "风电"],
    },
    {
        "topic": "生物医药与医疗器械",
        "ipc_prefixes": ["A61K", "A61P", "A61B", "A61M", "A61F", "A61H", "A61N",
                         "A61J", "A61L", "C07K", "C12N", "C12Q", "C07D"],
        "clc_prefixes": ["R"],
        "industry_kw": ["生物医药", "合成生物", "医药"],
    },
    {
        "topic": "机器人与智能制造",
        "ipc_prefixes": ["B25J", "B23K", "B23P", "B23Q", "G05B", "B65G", "B21D"],
        "clc_prefixes": ["TH"],
        "industry_kw": ["机器人", "具身智能", "智能制造", "自动化"],
    },
    {
        "topic": "低空经济与航空航天",
        "ipc_prefixes": ["B64U", "B64C", "B64D", "B64G", "G05D", "F02K"],
        "clc_prefixes": ["V"],
        "industry_kw": ["低空", "无人机", "航空", "通用航空"],
    },
    {
        "topic": "新材料与化工",
        "ipc_prefixes": ["C08L", "C08K", "C09D", "C01B", "C04B", "B32B", "C22C",
                         "C03B", "C21D"],
        "clc_prefixes": ["TQ", "TB", "TG"],
        "industry_kw": ["新材料", "材料", "化工"],
    },
    {
        "topic": "环境与节能",
        "ipc_prefixes": ["B01D", "C02F", "F23G", "B09B", "C10L"],
        "clc_prefixes": ["X"],
        "industry_kw": ["环保", "环境", "节能"],
    },
    {
        "topic": "测量与检测",
        "ipc_prefixes": ["G01N", "G01R", "G01M", "G01S", "G01B", "G01C", "G01D"],
        "clc_prefixes": [],
        "industry_kw": ["检测", "测量", "仪器"],
    },
]

WEIGHTS = {"patent_scale": 0.35, "patent_growth": 0.35,
           "paper_rows": 0.15, "media_rows": 0.15}


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as fh:
        return json.load(fh)


def ipc_topic(ipc: str):
    for t in TOPICS:
        for p in t["ipc_prefixes"]:
            if ipc.startswith(p):
                return t["topic"]
    return None


def clc_topic(code: str):
    code = code.replace("[", "").replace("]", "").strip()
    for t in TOPICS:
        if code in t["clc_prefixes"]:
            return t["topic"]
    return None


def minmax(vals: dict, low=0.0, high=100.0):
    vs = [v for v in vals.values() if v is not None]
    lo, hi = min(vs), max(vs)
    if hi == lo:
        return {k: 50.0 for k in vals}
    return {k: low + (v - lo) / (hi - lo) * (high - low) for k, v in vals.items()}


def pct(num, den, note, digits=4):
    return {
        "value": round(num / den * 100, digits) if den else None,
        "numerator": num,
        "denominator": den,
        "denominator_note": note,
    }


def main() -> None:
    pat_rows = load("patent_ipc4_year_20261021.json")
    f3 = load("f3_facts_20261023.json")
    news = load("chain_news_year_20261023.json")

    # ---- 专利：IPC4 × 年 → 主题 ----
    pat = {t["topic"]: {str(y): 0 for y in range(2021, 2027)} for t in TOPICS}
    pat_unmapped = {str(y): 0 for y in range(2021, 2027)}
    for ipc, year, cnt, _orgs in pat_rows:
        yy = str(int(year))
        if yy not in pat_unmapped:
            continue
        topic = ipc_topic(str(ipc))
        if topic is None:
            pat_unmapped[yy] += int(cnt)
        else:
            pat[topic][yy] += int(cnt)
    pat_total_2124 = sum(sum(pat[t["topic"]][str(y)] for y in (2021, 2022, 2023, 2024))
                         for t in TOPICS)

    # ---- 论文：中图分类前缀 → 主题（截面，无年份）----
    paper_nat = {t["topic"]: 0 for t in TOPICS}
    paper_mapped = 0
    for rec in f3["dwd_zh_paper_classification"]["scope_prefix3_top"]:
        n = int(rec["rows"])
        topic = clc_topic(rec["prefix"])
        if topic:
            paper_nat[topic] += n
            paper_mapped += n
    paper_all = int(f3["dwd_zh_paper_classification"]["rows"])

    # ---- 媒体：产业链节点名 → 主题；一条新闻可命中多主题，按 cell 去重 ----
    node_name = {n["industry_code"]: n["industry_name"]
                 for n in f3["dwd_industry_chain_info"]["nodes"]}
    media = {t["topic"]: 0 for t in TOPICS}
    media_cells_mapped = 0
    media_total_rows = 0
    for codes, year, n in news["cells"]:
        media_total_rows += int(n)
        topics_hit = set()
        try:
            code_list = json.loads(codes)
        except Exception:
            code_list = []
        for code in code_list:
            nm = node_name.get(code)
            if not nm:
                continue
            for t in TOPICS:
                if any(k in nm for k in t["industry_kw"]):
                    topics_hit.add(t["topic"])
        if topics_hit:
            media_cells_mapped += int(n)
            for tp in topics_hit:
                media[tp] += int(n)

    # ---- 各主题读数 ----
    topics = []
    for t in TOPICS:
        tp = t["topic"]
        n21, n24 = pat[tp]["2021"], pat[tp]["2024"]
        growth = (n24 - n21) / n21 * 100 if n21 else None
        topics.append({
            "topic": tp,
            "ipc_prefixes": t["ipc_prefixes"],
            "clc_prefixes": t["clc_prefixes"],
            "patent_2021": n21,
            "patent_2024": n24,
            "patent_growth_pct": round(growth, 4) if growth is not None else None,
            "paper_rows": paper_nat[tp],
            "media_rows": media[tp],
        })
    pat24_total = sum(x["patent_2024"] for x in topics)
    media_sum = sum(x["media_rows"] for x in topics)
    for x in topics:
        x["patent_share_2024_pct"] = round(x["patent_2024"] / pat24_total * 100, 4)
        x["paper_share_pct"] = round(x["paper_rows"] / paper_mapped * 100, 4) if paper_mapped else None
        x["media_share_pct"] = round(x["media_rows"] / media_total_rows * 100, 4)

    scale_score = minmax({x["topic"]: math.log1p(x["patent_2024"]) for x in topics})
    growth_score = minmax({x["topic"]: x["patent_growth_pct"] for x in topics}, 0, 100)
    paper_score = minmax({x["topic"]: float(x["paper_rows"]) for x in topics}, 0, 100)
    media_score = minmax({x["topic"]: float(x["media_rows"]) for x in topics}, 0, 100)
    for x in topics:
        tp = x["topic"]
        x["scores"] = {
            "patent_scale": round(scale_score[tp], 4),
            "patent_growth": round(growth_score[tp], 4),
            "paper_rows": round(paper_score[tp], 4),
            "media_rows": round(media_score[tp], 4),
        }
        x["heat_score"] = round(
            WEIGHTS["patent_scale"] * scale_score[tp]
            + WEIGHTS["patent_growth"] * growth_score[tp]
            + WEIGHTS["paper_rows"] * paper_score[tp]
            + WEIGHTS["media_rows"] * media_score[tp], 4)
    topics.sort(key=lambda x: -x["heat_score"])
    for i, x in enumerate(topics, 1):
        x["rank"] = i

    pat_mapped_2124 = sum(sum(pat[t["topic"]][str(y)] for y in (2021, 2022, 2023, 2024))
                          for t in TOPICS)
    pat_2124_total = pat_mapped_2124 + sum(pat_unmapped[str(y)] for y in (2021, 2022, 2023, 2024))

    derived = {
        "patent_mapped_share_pct": pct(
            pat_mapped_2124, pat_2124_total,
            "分母 = 2021—2024 有 IPC 的专利件数合计（含未映射 IPC）；分子 = 命中自建主题字典的件数"),
        "paper_mapped_share_pct": pct(
            paper_mapped, paper_all,
            "分母 = dwd_zh_paper_classification 20,048 行；分子 = 中图分类命中主题的行数（见 coverage.paper_mapped_rows）"),
        "paper_class_coverage_pct": pct(
            paper_all, 100900,
            "分母 = 中文论文全库 100,900 篇；分子 = 有中图分类的 20,048 篇"),
        "media_mapped_share_pct": pct(
            media_cells_mapped, media_total_rows,
            "分母 = 链新闻总条数 108,052；分子 = 至少命中一个主题的新闻条数（按 cell 去重）"),
        "patent_2024_share_of_2124_pct": pct(
            sum(x["patent_2024"] for x in topics),
            pat_2124_total,
            "分母 = 2021—2024 有 IPC 的专利合计；分子 = 2024 命中主题件数"),
    }

    out = {
        "metric_id": "M_TECH_TOPIC_HEAT",
        "metric_name_zh": "技术话题热度",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "support_judgment": "部分支持",
        "verdict_kind": "partial_selfbuilt_mapping",
        "judgment_reason": (
            "专利 IPC、论文中图分类、产业链新闻三侧都有真实数据可算，但「技术词→主题」"
            "没有官方映射：`dwd_tech_topic` 0 张表，`dwd_industry_analysis_topics` 只有 3 个"
            "不同主题名（字典残片），IPC 与中图分类也无官方对照表。主题字典为自建，"
            "且论文分类只覆盖 20,048/100,900（19.87%），有整维口径缺口，故判部分支持。"
        ),
        "mapping_is_official": False,
        "mapping_rule": (
            "自建 10 主题字典：每个 IPC4 按 TOPICS 顺序做前缀匹配，只归一个主题；"
            "每个中图分类号只归一个主题；产业链节点名按 industry_kw 命中，一条新闻可命中多主题。"
            "主题名、前缀集合与权重全部写在本脚本 TOPICS/WEIGHTS 中，无外部标准可引。"
        ),
        "weights": {**WEIGHTS, "main_is_official": False,
                    "note": "四分量等权思路自定：规模 0.35、增速 0.35、论文 0.15、媒体 0.15；不是甲方签发权重。"},
        "sources": [
            {"path": "code/_snapshots21/patent_ipc4_year_20261021.json",
             "what": "dwd_patent 全量扫描的 IPC4×年×件数（2021—2026）"},
            {"path": "code/_snapshots21/f3_facts_20261023.json",
             "what": "论文中图分类前缀、产业链字典、链新闻年度量、负证据"},
            {"path": "code/_snapshots21/chain_news_year_20261023.json",
             "what": "dwd_industry_chain_news_info 108,052 行的 industry_code 数组×年×条数"},
        ],
        "base_years_used": [2021, 2022, 2023, 2024],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": (
            "专利侧 2017—2020 零行，不按 0 摊入；2025/2026 为采集残年，不进增速。"
            "论文分类表没有日期列，只能给截面，不能给年度趋势；"
            "链新闻覆盖 2025-02-01—2026-07-27，媒体分量是 2025—2026 单窗。"
        ),
        "topics": topics,
        "coverage": {
            "patent_total_2124": pat_2124_total,
            "patent_mapped_2124": pat_mapped_2124,
            "patent_unmapped_2124": sum(pat_unmapped[str(y)] for y in (2021, 2022, 2023, 2024)),
            "patent_2024_mapped": pat24_total,
            "paper_rows_total": paper_all,
            "paper_mapped_rows": paper_mapped,
            "paper_zh_total": 100900,
            "media_total_rows": media_total_rows,
            "media_cells_mapped_rows": media_cells_mapped,
            "media_topic_sum_rows": media_sum,
        },
        "derived": derived,
        "absence_probe": {
            "dwd_tech_topic": f3["absence_probe"]["dwd_tech_topic"],
            "dwd_industry_analysis_topics": {
                "condition": "gkx.dwd_industry_analysis_topics 按 topic_code/topic_name 分组",
                "hits": 1,
                "rows": f3["dwd_industry_analysis"]["topics_rows"],
                "distinct_topic_name": 3,
                "top_names": [t["topic_name"] for t in f3["dwd_industry_analysis"]["topics"][:3]],
                "verdict": "字典残片，不能当官方主题表",
            },
            "dwd_tech_topic_at_all": {
                "condition": ("information_schema.tables WHERE table_schema='gkx' "
                              "AND table_name='dwd_tech_topic'"),
                "hits": f3["absence_probe"]["dwd_tech_topic"]["hits"],
                "verdict": "官方技术主题表不存在，映射只能自建",
            },
        },
        "reproduce": "cd code && python3 M_TECH_TOPIC_HEAT.py",
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print(f"[ok] {OUT} topics={len(topics)} "
          f"patent_mapped={pat_mapped_2124}/{pat_2124_total} "
          f"paper={paper_mapped}/{paper_all} media={media_cells_mapped}/{media_total_rows}")
    for x in topics:
        print(f"  {x['rank']:2d} {x['topic']:14s} heat={x['heat_score']:7.4f} "
              f"p21={x['patent_2021']:7d} p24={x['patent_2024']:7d} "
              f"g={x['patent_growth_pct']} paper={x['paper_rows']:5d} media={x['media_rows']:6d}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_RES_OVERLAP · 研究领域重叠度（0—1，企业对）

口径（calc-logic 真源）
----------------------
三维 Jaccard：专利 IPC4 重叠 / 关键词重叠 / 学者重叠；对象＝企业对企业。
需求原文（研究领域分析 §9.3.1）：基于企业－专家－学术文献－研究关键词知识图谱，
分析两家企业在研究领域上的重叠度，提供重叠度计算结果和可视化展示。

可算边界（本批实测）
------------------
* IPC 维：`patent_ipc4_by_name` 581,585 个组合，12 家企业各 33—319 个 IPC4 → **可用**；
* 学者维：`dwd_scholar` 21,316 人仅 2,108 个机构名，12 家里只有华为有 6 人，其余为 0
  → 大多数企业对的学者 Jaccard 恒为 0（无交集不是「不重叠」，是**没人**）；
* 关键词维：专利 `keywords` 需按申请人聚合 294 万行主表（禁止）；论文关键词表
  `dwd_zh_paper_classification` 仅 20,048 行且无机构字段 → **不可用**；
* 作者维（敏感性对照）：`author_info_list` 解析缓存，25 家机构有值（华为 125、中兴 292、
  深圳供电局 522、比亚迪 17）→ 只作旁证，不替代学者实体。

合成：对每对企业只在可用维上等权平均（缺维不补 0），并输出 n_dims 供甲方核对。

运行：python3 code/M_INNOV_RES_OVERLAP.py（零新增 SQL）
"""
from __future__ import annotations

import json
import os
import statistics
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _a26_common as C

MID = "M_INNOV_RES_OVERLAP"


def main() -> None:
    B = C.overlap_bundle(12)
    rows = B["pairs"]
    comps = [r["composite"] for r in rows if r["composite"] is not None]
    ipcs = [r["ipc_jaccard"] for r in rows if r["ipc_jaccard"] is not None]
    schs = [r["scholar_jaccard"] for r in rows if r["scholar_jaccard"] is not None]
    auths = [r["author_jaccard"] for r in rows if r["author_jaccard"] is not None]

    rows_sorted = sorted(rows, key=lambda r: -(r["composite"] or 0))
    n_pairs = len(rows)
    n_scholar_signal = sum(1 for r in rows if (r["scholar_jaccard"] or 0) > 0)
    n_author_signal = sum(1 for r in rows if (r["author_jaccard"] or 0) > 0)
    n_ipc_signal = sum(1 for r in rows if (r["ipc_jaccard"] or 0) > 0)

    scholar_zero_ents = [n for n in B["names"] if not B["scholar_sets"][n]]

    # 可视化数据：前 30 对（热力/条形），以及每家企业的 top 对手
    top_pairs = [{"a": r["a"], "b": r["b"], "composite": r["composite"],
                  "ipc_jaccard": r["ipc_jaccard"], "author_jaccard": r["author_jaccard"],
                  "scholar_jaccard": r["scholar_jaccard"],
                  "ipc_inter": r["ipc_inter"], "ipc_union": r["ipc_union"]} for r in rows_sorted[:30]]

    # 敏感性：只用 IPC 单维 vs 合成，排序是否一致
    ipc_only = [r["ipc_jaccard"] for r in sorted(rows, key=lambda x: x["a"] + x["b"])]
    three = [r["composite"] for r in sorted(rows, key=lambda x: x["a"] + x["b"])]
    rho = C.spearman([x or 0 for x in three], [x or 0 for x in ipc_only])

    res = {
        "metric_id": MID,
        "metric_name": "研究领域重叠度",
        "support_judgment": "部分支持",
        "object": "企业对企业（明星企业池 Top 12，按专利件数）",
        "generated_from": "_snapshots21/patent_ipc4_by_name（IPC4）+ probe_a26 scholar dump（学者）+ "
                          "research_paper_authors（作者名）+ probe_a26_ent_papers（论文规模）",
        "sql_count": 0,
        "method": {
            "formula": "overlap_ab = mean(available_dims)，dim ∈ {Jaccard(IPC4_a,IPC4_b), "
                       "Jaccard(scholar_a,scholar_b)}；作者名 Jaccard 只作敏感性对照，不进合成",
            "weights": "可用维等权；缺维不补 0，n_dims 逐对输出",
            "keyword_dim": "不可用（专利 keywords 需全表聚合，论文关键词表无机构字段）",
        },
        "universe": {
            "n_enterprises": len(B["names"]),
            "names": B["names"],
            "selection": "star_roster_gkx_20261021（授权≥50、已剔除非企业主体）按 pub_cnt 降序 Top 12",
            "patent_counts": {e["name_cn"]: e["pub_cnt"] for e in B["enterprises"]},
            "grant_counts": {e["name_cn"]: e["grant_cnt"] for e in B["enterprises"]},
            "paper_counts": B["papers"],
            "ipc_set_sizes": {n: len(v) for n, v in B["ipc_sets"].items()},
            "scholar_set_sizes": {n: len(v) for n, v in B["scholar_sets"].items()},
            "author_set_sizes": {n: len(v) for n, v in B["author_sets"].items()},
        },
        "coverage": {
            "n_pairs": n_pairs,
            "pairs_with_ipc_signal": n_ipc_signal,
            "pairs_with_scholar_signal": n_scholar_signal,
            "pairs_with_author_signal": n_author_signal,
            "enterprises_without_scholar_set": scholar_zero_ents,
            "ipc_dim_usable": True,
            "scholar_dim_usable": n_scholar_signal > 0,
            "keyword_dim_usable": False,
        },
        "distribution": {
            "composite": C.st([x for x in comps]),
            "ipc_jaccard": C.st([x for x in ipcs]),
            "scholar_jaccard": C.st([x for x in schs]),
            "author_jaccard": C.st([x for x in auths]),
        },
        "per_enterprise": B["per_enterprise"],
        "matrix": {"labels": B["names"], "values": B["matrix"],
                   "note": "对角固定 100（自重叠），非对角为 composite×100；None 表示该对无可用维"},
        "top_pairs": top_pairs,
        "sensitivity": {"ipc_only_vs_composite_spearman": rho,
                        "note": "IPC 单维与合成（IPC+学者）的排序相关；等于 1 时说明学者维未参与任何一对，"
                                "重叠度实际退化为 IPC 单维"},
        "base_year_block": C.base_year_block(
            [], [], "重叠度为截面集合运算，不涉及年度分母；IPC 集合取全历史（2021—2026 库内区间）"),
        "gaps": [
            "学者维：dwd_scholar 只有 21,316 人、2,108 个机构名，12 家企业中 11 家学者集合为空",
            "关键词维：dwd_patent.keywords 无法在不扫 294 万行的前提下按申请聚合；"
            "dwd_zh_paper_classification 无机构字段",
            "IPC 集合是全历史并集，未做时间窗（库内 apdt_year 只覆盖 2021—2026）",
            "作者名同名不同人无法消歧，作者维只能当敏感性对照",
        ],
    }
    C.write_out(MID, res)
    print(json.dumps({k: res[k] for k in ("support_judgment", "coverage", "distribution")},
                     ensure_ascii=False, indent=1))
    print("top pairs:", json.dumps(top_pairs[:6], ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

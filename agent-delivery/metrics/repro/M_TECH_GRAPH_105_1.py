#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_TECH_GRAPH_105_1 · 技术实体关系抽取（20261022 三方库版）

口径（单一）：
  节点 = IPC4 技术域（全期（2021—2026）件数前 200，覆盖 91.47% 的有 IPC 专利）；
  关系的抽取单位 = 申请人/机构（不是论文共词、不是 NLP 句法）。
  七类关系中，三类有数据键可抽（技术-技术、技术-企业、技术-机构），
  技术-产业为规则映射，技术-政策为产业代理，技术-人才、技术-服务两维无键。

技术-技术边的定义：同一申请人同时出现在两个 IPC4 域 → 记一次共现；
  骨干边要求 共现次数 ≥20 且 Jaccard ≥0.05（原始共现图接近完全图，必须稀疏化，见 §四）。

运行：python3 code/M_TECH_GRAPH_105_1.py（零 SQL）
"""
from __future__ import annotations

import collections
import itertools
import json
import sys

sys.path.insert(0, ".")
import _tech21_scope as S  # noqa: E402

MID = "M_TECH_GRAPH_105_1"
TOP_N = 200
MIN_CO = 20
MIN_JACCARD = 0.05


def main():
    panel = json.load(open(S.SNAP / "patent_panel_innov_20261021.json", encoding="utf-8"))
    top = sorted(panel["ipc_all"].items(), key=lambda kv: -kv[1])[:TOP_N]
    topset = {k for k, _ in top}
    top_patents = sum(v for _, v in top)
    all_patents = sum(panel["ipc_all"].values())

    # 申请人 → 域集合；域 → 申请人数
    by_name = collections.defaultdict(set)
    deg = collections.Counter()
    for ipc, nm, n in S.load_ipc_name():
        if ipc in topset:
            by_name[nm].add(ipc)
            deg[ipc] += 1

    co = collections.Counter()
    for ds in by_name.values():
        if len(ds) < 2:
            continue
        for a, b in itertools.combinations(sorted(ds), 2):
            co[(a, b)] += 1

    backbone = []
    for (a, b), c in co.items():
        j = c / (deg[a] + deg[b] - c)
        if c >= MIN_CO and j >= MIN_JACCARD:
            backbone.append({"a": a, "b": b, "co": c, "jaccard": round(j, 4)})
    backbone.sort(key=lambda e: (-e["co"], -e["jaccard"]))

    # 技术-企业：深圳企业实体 × 域
    groups = S.load_sz_groups()
    sz_names = {g["nm"] for g in groups}
    ent_names = {nm for nm in sz_names if S.is_enterprise_name(nm)}
    inst_names = {nm for nm in sz_names
                  if any(x in nm for x in ("大学", "学院", "研究院", "研究所", "实验室", "医院", "科学院"))}
    ent_dom = collections.defaultdict(set)
    inst_dom = collections.defaultdict(set)
    for ipc, nm, n in S.load_ipc_name():
        if ipc not in topset:
            continue
        if nm in ent_names:
            ent_dom[nm].add(ipc)
        elif nm in inst_names:
            inst_dom[nm].add(ipc)
    ent_edges = sum(len(v) for v in ent_dom.values())
    inst_edges = sum(len(v) for v in inst_dom.values())
    ent_hubs = sorted(((nm, len(ds)) for nm, ds in ent_dom.items()), key=lambda x: -x[1])[:15]
    inst_hubs = sorted(((nm, len(ds)) for nm, ds in inst_dom.items()), key=lambda x: -x[1])[:10]

    # 技术-产业：规则映射（一个 IPC4 只进一个产业）
    ind_edges = []
    for ind, prefixes in S.SZ208_MAP.items():
        got = [p for p in prefixes if S.ipc_industry(p) == ind and p in topset]
        if got:
            ind_edges.append({"industry": ind, "n_ipc4": len(got), "ipc4": got})

    # 技术-政策：产业层代理（不是域级命中）
    pol_cnt, pol_total = S.industry_policy_counts()
    pol_edges = [{"industry": k, "policy_hits": v} for k, v in
                 sorted(pol_cnt.items(), key=lambda kv: -kv[1]) if v > 0]

    relation_types = [
        {"relation": "技术-技术", "source": "patent_ipc4_by_name（同申请人共现）", "edges": len(backbone),
         "status": "可抽", "note": f"原始共现 {len(co)} 对，骨干阈 co≥{MIN_CO}、Jaccard≥{MIN_JACCARD}"},
        {"relation": "技术-企业", "source": "patent_ipc4_by_name × 深圳企业名单", "edges": ent_edges,
         "status": "可抽", "note": f"深圳企业 {len(ent_dom)} 家、二部图边 {ent_edges} 条"},
        {"relation": "技术-机构", "source": "patent_ipc4_by_name × 深圳高校/科研/医疗名单", "edges": inst_edges,
         "status": "可抽", "note": f"深圳机构 {len(inst_dom)} 家"},
        {"relation": "技术-产业", "source": "SZ208_MAP 规则映射", "edges": len(ind_edges),
         "status": "规则映射", "note": "不是从文本抽取，是 IPC4→产业的字典关系"},
        {"relation": "技术-政策", "source": "深圳市政策关键词 → 产业 → IPC4", "edges": len(pol_edges),
         "status": "产业代理", "note": f"{pol_total} 条深圳政策，只能落到产业层，落不到 IPC4"},
        {"relation": "技术-人才", "source": "无域级键", "edges": 0, "status": "缺",
         "note": "发明人只有全库姓名计数（403,743 人），无 IPC/城市归属，不能建人才-技术边"},
        {"relation": "技术-服务机构", "source": "无表", "edges": 0, "status": "缺",
         "note": "技术服务机构底册不在本库；无主体、无技术域标签"},
    ]

    payload = {
        "metric_id": MID,
        "metric_name": "技术实体关系抽取",
        "caliber": {
            "节点": f"IPC4 技术域，全期（2021—2026）件数前 {TOP_N}",
            "边": "同一申请人/机构同时出现在两个域 → 共现；骨干阈 co≥20 且 Jaccard≥0.05",
            "主体": "关系抽取对象含全国申请人（技术-技术）与深圳主体（技术-企业/机构）",
            "口径声明": "本件技术-技术边是「申请人共现」代理，不是专利同族/引文/NLP 句法关系",
        },
        "base_years_used": [],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": "节点筛选为全期（2021—2026）聚合截面，不做跨年比较，故不设基期；2017—2020 在 dwd_patent 为零行。",
        "coverage": {
            "top_n": TOP_N,
            "top_patents": top_patents,
            "all_ipc_patents": all_patents,
            "top_share": round(top_patents / all_patents, 4),
            "applicants_with_ipc": len(by_name),
            "raw_pairs": len(co),
            "backbone_edges": len(backbone),
        },
        "relation_types": relation_types,
        "tech_tech_top": backbone[:25],
        "tech_enterprise_hubs": [{"name": n, "n_domains": d} for n, d in ent_hubs],
        "tech_institution_hubs": [{"name": n, "n_domains": d} for n, d in inst_hubs],
        "tech_industry_edges": ind_edges,
        "tech_policy_edges": pol_edges,
        "degree_top": [{"ipc4": k, "n_applicants": v} for k, v in deg.most_common(20)],
        "support_judgment": {
            "data_support_level": "部分支持",
            "criteria": {
                "技术-技术": "可抽（申请人共现骨干）",
                "技术-企业": "可抽（深圳企业二部图）",
                "技术-机构": "可抽（深圳高校/科研/医疗）",
                "技术-产业": "仅规则映射（无链码对齐，INB13xx 与 INB12xx 不同码域，§3.9）",
                "技术-政策": "仅产业代理（政策无 IPC 标签）",
                "技术-人才": "缺（发明人无域级键）",
                "技术-服务机构": "缺（无服务机构底册）",
            },
            "note": "七类关系中三类可抽、两类只能做规则/产业代理、两类缺键，判部分支持",
        },
    }
    S.write_out(MID, payload)

    print(json.dumps(payload["coverage"], ensure_ascii=False, indent=1))
    print("relations", [(r["relation"], r["edges"], r["status"]) for r in relation_types])
    print("top edges", backbone[:5])
    print("ent hubs", ent_hubs[:5], "inst hubs", inst_hubs[:5])


if __name__ == "__main__":
    main()

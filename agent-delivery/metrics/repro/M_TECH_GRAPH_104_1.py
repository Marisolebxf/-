#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TECH_GRAPH_104_1 · 技术实体识别构建（20261022 三方库版）

口径（单一）：
  实体 = 深圳专利申请人（名称经企业底册归到深圳市），一个名称一个实体；
  属性 = 名称/类型/行业归属/区县/专利件数/授权件数/主 IPC4/技术标签/论文数/技术交易记录。
  专利件数为全期（2021—2026，dwd_patent 全部年份），不是单年截面；
  论文与技术交易只做「属性可得性」核验，不作为实体打分。

识别方法：规则（名称后缀）+ 词典（企业底册 189,069 个名称、32,322 个技术标签机构）。
本件不训练 NER 模型，也不冒充 NER 结果；缺口在 §三/§四 逐项披露。

运行：python3 code/M_TECH_GRAPH_104_1.py（零 SQL）
"""
from __future__ import annotations

import collections
import json
import re
import sys

sys.path.insert(0, ".")
import _tech21_scope as S  # noqa: E402

MID = "M_TECH_GRAPH_104_1"


def entity_type(name: str) -> str:
    if any(x in name for x in ("大学", "学院", "学校")):
        return "高校"
    if any(x in name for x in ("研究院", "研究所", "研究中心", "实验室", "科学院")):
        return "科研机构"
    if any(x in name for x in ("医院", "疾病预防控制中心")):
        return "医疗机构"
    if S.is_enterprise_name(name):
        return "企业"
    return "其他主体"


def main():
    groups = S.load_sz_groups()
    base = S.load_base_rows()
    agg, agg_meta = S.load_star_agg()
    tags = S.load_tech_tags()
    papers = json.load(open(S.SNAP / "org_paper_counts_20261021.json", encoding="utf-8"))["counts"]
    transfer = json.load(open(S.SNAP / "probe_tinn21_20261022.json", encoding="utf-8"))["transfer_rows"]["rows"]

    # 主 IPC4：深圳实体在 IPC4×申请人聚合中出现最多的域
    sz_names = {g["nm"] for g in groups}
    dom_cnt = collections.defaultdict(collections.Counter)
    n_with_ipc = set()
    for ipc, nm, n in S.load_ipc_name():
        if nm in sz_names:
            dom_cnt[nm][ipc] += int(n)
            n_with_ipc.add(nm)

    # 技术交易：只统计「买方/卖方名称命中」，不冒充交易额（表内无金额列）
    tr_cnt = collections.Counter()
    for pn, d, before, after in transfer:
        for blob in (before, after):
            for m in re.finditer(r'"name"\s*:\s*"([^"]+)"', blob or ""):
                if m.group(1) in sz_names:
                    tr_cnt[m.group(1)] += 1

    records = []
    type_cnt = collections.Counter()
    type_pat = collections.Counter()
    fill = collections.Counter()
    for g in groups:
        nm = g["nm"]
        b = base.get(nm, {})
        et = entity_type(nm)
        pub, grant = agg.get(nm, [int(g.get("n", 0)), 0])
        top_ipc = dom_cnt[nm].most_common(1)[0][0] if dom_cnt[nm] else None
        rec = {
            "name": nm,
            "entity_type": et,
            "org_type": b.get("org_type"),
            "industry_l2": b.get("industry_l2"),
            "area": b.get("area"),
            "n_patent": int(pub),
            "n_grant": int(grant),
            "grant_rate": round(grant / pub, 4) if pub else None,
            "invention": int(g.get("invention", 0)),
            "top_ipc4": top_ipc,
            "n_ipc4": len(dom_cnt[nm]),
            "tech_tags": len(tags.get(b.get("org_id"), [])),
            "n_paper": int(papers.get(nm, 0)),
            "n_transfer": int(tr_cnt.get(nm, 0)),
        }
        records.append(rec)
        type_cnt[et] += 1
        type_pat[et] += rec["n_patent"]
        fill["base_matched"] += int(bool(b))
        fill["industry"] += int(bool(rec["industry_l2"]) and str(rec["industry_l2"]).upper() != "NULL")
        fill["area"] += int(bool(rec["area"]) and str(rec["area"]).upper() != "NULL")
        fill["grant"] += int(rec["n_patent"] > 0)
        fill["ipc4"] += int(top_ipc is not None)
        fill["tech_tag"] += int(rec["tech_tags"] > 0)
        fill["paper"] += int(rec["n_paper"] > 0)
        fill["transfer"] += int(rec["n_transfer"] > 0)

    n = len(records)
    records.sort(key=lambda r: (-r["n_patent"], r["name"]))
    top = records[:30]

    payload = {
        "metric_id": MID,
        "metric_name": "技术实体识别构建",
        "caliber": {
            "实体": "深圳专利申请人名称（一名称一实体，未做同名合并以外的消歧）",
            "城市归属": "企业底册 name_cn → city；只取 city='深圳市'",
            "专利件数": "全期 2021—2026，dwd_patent 按 first_applicant_name 聚合（[件数,授权数] 缓存）",
            "识别方法": "规则（名称后缀）+ 词典（底册 189,069 名称、32,322 家技术标签机构）；无 NER 模型",
        },
        "base_years_used": [],
        "base_years_missing": [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026],
        "base_years_note": "本件是截面实体表（全期聚合），不设年度基期；base_years_used=[] 表示不做跨年比较。",
        "entity_total": n,
        "patent_total": int(sum(r["n_patent"] for r in records)),
        "type_dist": {k: {"entities": v, "patents": int(type_pat[k]),
                          "patent_share": round(type_pat[k] / max(1, sum(type_pat.values())), 4)}
                      for k, v in type_cnt.most_common()},
        "attribute_fill": {k: {"n": v, "rate": round(v / n, 4)} for k, v in fill.items()},
        "attribute_definition": {
            "名称": "实体主键（申请人名称原文，未归一）",
            "类型": "规则判定：企业/高校/科研机构/医疗机构/其他主体",
            "行业归属": "底册 industry_l2（GB/T 4754 二级行业）",
            "区县": "底册 area",
            "专利件数": "star_applicant_agg_gkx.agg[nm][0]",
            "授权件数": "star_applicant_agg_gkx.agg[nm][1]（不是 WO/PCT 件数，§3.17）",
            "主 IPC4": "patent_ipc4_by_name 中最多的 IPC4",
            "技术标签": "tech_tags_20261021[org_id] 的标签个数",
            "论文数": "org_paper_counts_20261021[名称]（只覆盖 2,070 家科研机构）",
            "技术交易": "dwd_patent_transfer 买方/卖方名称命中条数（表内无金额列）",
        },
        "top_entities": top,
        "gaps": {
            "论文属性": "深圳申请人命中 0 家：论文计数缓存只覆盖科研机构 2,070 家（其中非零 181 家），"
                        "高校/企业不在其中；论文侧无 IPC/产业标签，也不能反推实体技术领域。",
            "技术交易额": "dwd_patent_transfer 只有 pn/日期/买卖方，没有金额列；只能给「交易记录条数」，"
                          "不能给「技术交易额」。深圳实体命中 134 家（0.17%）。",
            "技术标签": "32,322 家机构有标签，深圳实体 12,628 家命中（16.22%）；其余实体无标签。",
            "同名": "底册 189,116 行只有 189,069 个不同 name_cn（47 个重名，§3.5）；本件按名称保留，"
                    "重名会合并为同一实体，属已知偏差。",
            "NER": "未训练命名实体识别；技术报告、论文正文、交易文本均未进入识别语料。",
        },
        "source": {
            "entity": "code/_snapshots_gkx21/sz_patent_city_name_gkx.json（168,827 名，深圳 77,846 名）",
            "base": "code/_snapshots21/star_base_rows_gkx.json（189,116 行，含 industry_l2/area/org_type）",
            "patent": "code/_snapshots21/star_applicant_agg_gkx.json + patent_ipc4_by_name_20261021.json",
            "tag": "code/_snapshots21/tech_tags_20261021.json",
            "paper": "code/_snapshots21/org_paper_counts_20261021.json",
            "transfer": "code/_snapshots21/probe_tinn21_20261022.json#transfer_rows",
        },
        "support_judgment": {
            "data_support_level": "部分支持",
            "criteria": {
                "名称/类型/行业/区域": "可算（底册 100% 命中）",
                "专利数量/授权数量": "可算（全量聚合）",
                "主 IPC4/技术标签": "可算（标签覆盖 16.22%）",
                "论文数量": "缺（深圳实体 0 命中）",
                "技术交易额": "缺（无金额列，只有 22,809 条记录）",
                "文本 NER": "缺（无技术报告/论文正文语料）",
            },
            "note": "实体表与四项属性可交付；论文、技术交易额、文本 NER 三项缺源，判部分支持",
        },
    }
    S.write_out(MID, payload)

    print("entities", n, "patents", payload["patent_total"])
    print("types", json.dumps(payload["type_dist"], ensure_ascii=False))
    print("fill", json.dumps(payload["attribute_fill"], ensure_ascii=False))
    print("top5", [(r["name"], r["entity_type"], r["n_patent"], r["n_grant"], r["industry_l2"]) for r in top[:5]])


if __name__ == "__main__":
    main()

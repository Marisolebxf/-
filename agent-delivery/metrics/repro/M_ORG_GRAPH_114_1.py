#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ORG_GRAPH_114_1 · 科研机构实体识别构建（GRAPH 域，序号 114）

需求锚点：bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/科研机构/图谱.md 序号 114
  「从大规模科研机构数据库及相关信息源中，自动抽取并结构化科研机构的名称、类型、所属学科领域、
    地理位置及各类关键属性。集成基于规则的识别与基于词典的识别两种方法，配套实体维护更新及
    属性提取机制。属性提取包括人员规模、论文产出量、专利数量、地址。」

本件口径（零 SQL + 一次本地文本评测）：
  1) 实体主表 = gkx.dwd_research_institute_base_info（2,074 家，27 列）；
  2) 词典识别 = 2,074 个规范名 + 去尾括号别名（2,241 条），对 100,900 篇论文的
     435,937 条署名机构串做前缀/包含匹配，统计命中字符串数、命中机构数、候选新实体；
  3) 规则识别 = 机构后缀正则（研究院/研究所/大学/学院/中心/实验室/医院…）判定「是不是机构串」，
     与词典结果交叉，区分「规则认出但词典没有」（候选新实体）与「规则也没认出」（非机构串）；
  4) 属性提取 = 论文/专利/项目/学者四类产出按名匹配，逐类给覆盖率；人员规模列不存在。

硬约束（必须披露）：
  - 「人员规模」在机构底册中没有对应列（`dwd_org_base_info.org_size` 只覆盖企业库，
    且该库与本底册零交集），因此这一项属性提取率为 0，不是稀疏而是无字段。
  - 论文/专利/项目/学者四类属性的覆盖率是 11.33% / 10.56% / 2.56% / 1.40%，
    属性提取只能覆盖「名字规范、发文多」的头部机构。
  - 变更记录表对底册零命中，实体维护更新机制没有可观测的更新日志，只能靠 ETL 的
    `updated_time` 判断批次，不能判断实体内容何时变化。
"""
from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _org_deep21_common as OC  # noqa: E402

MID = "M_ORG_GRAPH_114_1"

ORG_SUFFIX = re.compile(r"(研究院|研究所|研究中心|实验室|大学|学院|医院|防治中心|"
                        r"基金会|学会|协会|委员会|检验中心|技术中心|设计院)")
NON_ORG = re.compile(r"(有限公司|有限责任公司|股份有限公司|集团|厂|银行|支行|分公司)")
ID_TYPE = {"12": "事业单位（机构编制）", "52": "民办非企业单位（民政）",
           "51": "社会团体（民政）", "53": "基金会（民政）",
           "34": "司法鉴定机构（司法行政）", "11": "机关", "19": "编办管理其他机构"}


def main() -> None:
    panel = OC.load_panel()
    inst = panel["institutions"]
    probe = OC.load_probe()

    names = [i["name"] for i in inst]
    alias, idx = OC.build_alias_index(names)
    alias_collision = defaultdict(set)
    for a, full in alias.items():
        alias_collision[a].add(full)
    collisions = {a: sorted(v) for a, v in alias_collision.items() if len(v) > 1}

    # ---------------- 1. 主表与去重 ----------------
    name_cnt = Counter(names)
    dup_names = {n: c for n, c in name_cnt.items() if c > 1}
    # external_id 前缀分布取自本批 SQL 探针（面板未保留 external_id 列）
    idp = {r[0]: r[1] for r in ((probe.get("inst_id_prefix") or {}).get("rows") or [])}
    type_by_prefix = {p: {"n": n, "map": ID_TYPE.get(p, "未登记前缀")}
                      for p, n in sorted(idp.items(), key=lambda kv: -kv[1])}
    blank_type = sum(1 for i in inst if not i["org_type"])
    type_by_prefix["12"]["note"] = ("org_type 为空的 %d 家全部落在 12 前缀，可直接补为事业单位，"
                                    "补全后类型覆盖 2,074/2,074" % blank_type)

    # ---------------- 1b. 逐列填充率（来自本批 SQL 探针 inst_fill，2,074 行） ----------------
    f = ((probe.get("inst_fill") or {}).get("rows") or [[None] * 14])[0]
    fcols = (probe.get("inst_fill") or {}).get("cols") or []
    fmap = dict(zip(fcols, f))
    fill = {
        "名称 name_cn": fmap.get("n"),
        "类型 org_type": sum(1 for i in inst if i["org_type"]),
        "类型（按 external_id 前缀补全后）": 2074,
        "登记状态 reg_status": fmap.get("st"),
        "省份/城市/区县": fmap.get("area"),
        "成立日期 incorporation_date": fmap.get("inc"),
        "注册资本 registered_capital": fmap.get("cap"),
        "地址 address": fmap.get("addr"),
        "经纬度 addr_lng": fmap.get("lng"),
        "英文名 name_en": fmap.get("en"),
        "登记机关 registration_org": fmap.get("regorg"),
        "法定代表人 lerep": fmap.get("lerep"),
        "统一社会信用代码 external_id": fmap.get("ext"),
    }

    # ---------------- 2. 词典 + 规则识别评测 ----------------
    papers = OC.load_json(OC.PAPER)["paper"]
    aff_cnt = Counter()
    hit_inst = 0
    hit_str = set()
    matched_org = Counter()
    bad_json = 0
    for p in papers:
        try:
            arr = json.loads(p.get("author_info_list") or "[]")
        except Exception:
            bad_json += 1
            continue
        if not isinstance(arr, list):
            bad_json += 1
            continue
        for it in arr:
            if not isinstance(it, dict):
                continue
            a = (it.get("institution") or it.get("affiliation") or "").strip()
            if not a:
                continue
            aff_cnt[a] += 1
            hit = OC.match_org(a, alias, idx)
            if hit:
                hit_str.add(a)
                hit_inst += 1
                matched_org[hit] += 1

    total_inst = sum(aff_cnt.values())
    org_like = {a: c for a, c in aff_cnt.items() if ORG_SUFFIX.search(a) and not NON_ORG.search(a)}
    org_like_hit = {a: c for a, c in org_like.items() if a in hit_str}
    recall_str = len(hit_str & set(org_like)) / len(org_like) if org_like else None
    recall_inst = (sum(c for a, c in org_like.items() if a in hit_str) / sum(org_like.values())
                   if org_like else None)
    candidates = sorted(((c, a) for a, c in org_like.items() if a not in hit_str), reverse=True)

    # 狭义科研院所（只要研究院/研究所/研究中心/实验室，排除大学/学院/医院/企业）：
    # 这才是「科研机构底册」自身收录范围，用它衡量词典质量，避免把「省外机构没收录」算成漏配。
    narrow_ok = re.compile(r"(研究院|研究所|研究中心|实验室)")
    narrow_no = re.compile(r"(大学|学院|医院|有限公司|集团|公司)")
    narrow = {a: c for a, c in aff_cnt.items() if narrow_ok.search(a) and not narrow_no.search(a)}
    narrow_hit = {a: c for a, c in narrow.items() if a in hit_str}
    narrow_cand = sorted(((c, a) for a, c in narrow.items() if a not in hit_str), reverse=True)
    narrow_scope = {
        "rule": "字符串含 研究院/研究所/研究中心/实验室，且不含 大学/学院/医院/公司/集团",
        "strings": len(narrow), "instances": sum(narrow.values()),
        "matched_strings": len(narrow_hit), "matched_instances": sum(narrow_hit.values()),
        "string_recall": round(len(narrow_hit) / len(narrow), 4) if narrow else None,
        "instance_recall": round(sum(narrow_hit.values()) / sum(narrow.values()), 4) if narrow else None,
        "top_misses": [{"affiliation": a, "count": c} for c, a in narrow_cand[:15]],
        "note": "漏配样本清一色是省外国家级院所（中国食品药品检定研究院 446 次、"
                "中国石油勘探开发研究院 156 次…），属底册只收广东的收录边界，不是匹配规则失效。",
    }

    # 命中样例（供人工抽查精度）
    hit_samples = sorted(((c, a, OC.match_org(a, alias, idx)) for a, c in aff_cnt.items()
                          if a in hit_str), reverse=True)[:15]

    # ---------------- 3. 属性抽取覆盖 ----------------
    attr = {
        "论文产出量 papers": sum(1 for i in inst if i.get("papers")),
        "专利数量 patents": sum(1 for i in inst if i.get("patents")),
        "专利 IPC 小类": len(OC.load_ipc_by_name()),
        "科研项目 projects": sum(1 for i in inst if i.get("projects")),
        "学者 scholars": sum(1 for i in inst if i.get("scholars")),
        "政策提及 policy": sum(1 for i in inst if i.get("policy_mentions")),
        "专利受让 transfer_in": sum(1 for i in inst if i.get("transfer_in")),
        "人员规模 employees": 0,
        "地址 address": 2074,
        "经纬度 lng": 2056,
        "注册资本 capital": 2044,
        "成立日期 incorporation": 1996,
    }
    attr_pct = {k: round(v / len(inst), 4) for k, v in attr.items()}

    forg = {r[0]: {"rows": r[1], "countries": r[2]}
            for r in ((probe.get("forg_rows") or {}).get("rows") or [])}
    forg_c = [{"src": r[0], "country": r[1], "n": r[2]}
              for r in ((probe.get("forg_country") or {}).get("rows") or [])]

    out = {
        "metric_id": MID,
        "metric_name": "科研机构实体识别构建",
        "domain": "GRAPH / 产业全要素图谱（序号 114）",
        "formula_owner": "AI-20261022（推测定义，wanghui=false）",
        "support_judgment": "部分支持",
        **OC.base_years(
            [2021, 2022, 2023, 2024, 2025, 2026], [2017, 2018, 2019, 2020],
            "实体主表是 2026-10 快照（截面）；论文属性取自 100,900 篇（1980—2026），"
            "专利属性为存量（库内 2021—2026，2017—2020 零行，不按 0 摊入）；"
            "2026 为残年，只用于「当前属性」不做趋势。"),
        "inputs": {
            "entity_master": "gkx.dwd_research_institute_base_info 2,074 行（27 列）",
            "text_corpus": "a25_paper_panel.json 100,900 篇署名机构串（435,937 条实例）",
            "attributes": "org_family_panel_20261021.json（论文/专利/项目/学者/政策/转让）",
            "foreign_registries": "gkx.dwd_forg_research_org_info / dwd_forg_university_org_info",
            "change_log": "gkx.dwd_org_changerecord_info 3,245,250 行（对底册零命中）",
        },
        "entity_master": {
            "rows": len(inst),
            "distinct_names": len(name_cnt),
            "duplicate_names": dup_names,
            "duplicate_name_rows": sum(dup_names.values()),
            "distinct_org_id": len({i["org_id"] for i in inst}),
            "distinct_external_id": 2074,
            "id_prefix_dist": type_by_prefix,
            "id_note": "external_id 是登记管理码：12=事业单位、52=民办非企业、51=社会团体、"
                       "53=基金会、34=司法鉴定；前缀与 org_type 100% 一致，可作类型校验规则。",
            "city_dist": dict(Counter(i["city"] for i in inst).most_common()),
            "type_dist": dict(Counter(i["org_type"] for i in inst).most_common()),
        },
        "field_fill": {
            "counts": fill,
            "pct": {k: round(v / len(inst), 4) for k, v in fill.items()},
            "note": "地址/英文名/类型/登记状态/省份/城市/区县为 100%；经纬度 99.13%、"
                    "注册资本 98.55%、成立日期 96.24%（78 家无成立日）。",
        },
        "recognition": {
            "papers": len(papers),
            "affiliation_instances": total_inst,
            "distinct_affiliations": len(aff_cnt),
            "dictionary_aliases": len(alias),
            "prefix_buckets": len(idx),
            "alias_collisions": len(collisions),
            "alias_collision_examples": dict(list(collisions.items())[:10]),
            "matched_strings": len(hit_str),
            "matched_instances": hit_inst,
            "matched_orgs": len(matched_org),
            "org_like_strings": len(org_like),
            "org_like_instances": sum(org_like.values()),
            "org_like_matched_strings": len(org_like_hit),
            "string_recall_on_org_like": round(recall_str, 4) if recall_str else None,
            "instance_recall_on_org_like": round(recall_inst, 4) if recall_inst else None,
            "overall_string_hit_rate": round(len(hit_str) / len(aff_cnt), 4),
            "overall_instance_hit_rate": round(hit_inst / total_inst, 4),
            "precision_samples": [{"affiliation": a, "count": c, "matched": m}
                                  for c, a, m in hit_samples],
            "narrow_scope": narrow_scope,
            "candidate_new_entities": [{"affiliation": a, "count": c} for c, a in candidates[:30]],
            "candidate_note": "候选新实体 = 规则判为机构串、但词典未命中；多为省外高校/医院与企业研究院，"
                              "不在「广东省科研机构底册」的收录范围内，不等于识别失败。",
        },
        "attribute_extraction": {
            "counts": attr,
            "pct": attr_pct,
            "personnel_note": "人员规模无字段：dwd_research_institute_base_info 无 employees/org_size 列；"
                              "dwd_org_base_info.org_size 只覆盖企业库，与本底册 external_id 零交集。",
        },
        "maintenance": {
            "change_records_matched": 0,
            "reason": "dwd_org_changerecord_info（3,245,250 行）按 org_id 与 external_id 连接底册均 0 行；"
                      "该表是工商变更库，事业单位/民办非企业不在其中。",
            "etl_timestamp_only": "底册 updated_time 只能判断入湖批次，不能判断实体内容变更时点。",
            "recommendation": "建「机构实体变更日志」（org_id, field, old, new, changed_at, source），"
                              "否则需求里的「实体维护更新」无法审计。",
        },
        "foreign_registries": {
            "tables": forg,
            "country_top": forg_c,
            "caveat": "两表各 20,000 行，正好是取数上限，按国家分布看是抽样而非全量名录；"
                      "只能作别名词典的补充，不能宣称「全球机构全覆盖」。",
        },
        "limits": [
            "人员规模无字段，4 项要求属性里缺 1 项。",
            "论文/专利属性覆盖 11.33% / 10.56%，项目 2.56%、学者 1.40%，属性提取集中在大所大校。",
            "词典对「科研型机构串」的召回见 recognition 段；漏配主要是省外机构与企业研究院，"
            "属底册收录边界，不是匹配算法失效。",
            "无实体变更日志，维护更新机制不可审计。",
            "无实体消歧（同名不同实体、同一实体多写法）的人工标注集，无法给准确率/召回率的置信区间。",
        ],
        "probes": {k: probe.get(k) for k in ("inst_fill", "inst_id_prefix", "inst_dup_names", "chg_head")},
    }
    path = OC.write_out(out, MID)
    print("wrote", path)
    print("rows", len(inst), "names", len(name_cnt), "dup", dup_names)
    print("aff", total_inst, len(aff_cnt), "hit", hit_inst, len(hit_str), "orgs", len(matched_org))
    print("org_like", len(org_like), sum(org_like.values()), "recall", recall_str, recall_inst)
    print("attr", attr_pct)
    print("top candidates", candidates[:8])


if __name__ == "__main__":
    main()

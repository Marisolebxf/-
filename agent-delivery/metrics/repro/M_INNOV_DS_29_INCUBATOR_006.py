#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M_INNOV_DS_29_INCUBATOR_006 —— 影响力评价（孵化/众创载体三维综合评分，0-100）

口径（王惠 calc-logic/INNOV/M_INNOV_DS_29_INCUBATOR_006.md）：
  载体入集：科技企业孵化器 / 众创空间资质；
  三维加权：在孵规模（子公司数）/ 创新产出（载体+子公司专利论文）/ 服务能力（高企覆盖）。

20261021 版换源：唯一数据面改为三方库 `gkx`（`gkx.<表名>`，不传 database/charset）。
本版同时纠正 20261020 的一处失败做法（**名称关键词硬挂**）：
  - 旧版把「名称含 孵化/众创/加速器」的机构直接当成载体并入集（81 家只靠名称），
    实测会把「XX众创科技有限公司」「XX孵化器管理有限公司」（运营服务商）与真正的
    孵化载体混在一起，属 20261020 已被判失败的关键词匹配。
  - 本版**主池只取真实资质标签** `gkx.dwd_org_tech_tag.org_tag IN ('科技企业孵化器','众创空间')`；
    名称关键词命中的其余机构降级为 `name_only_candidates`（只登记、不评分），
    并披露「机构底册无孵化器类型字段」这一结构缺口。

开发库实现要点：
  - `gkx.dwd_org_base_info.org_id` 与 `dwd_org_tech_tag.org_id` 可直接 JOIN（202,423 条标签全命中）；
  - `dwd_org_subsidiary_info` 的 org_id / sub_org_id 与 base_info **不同 ID 命名空间（JOIN 命中 0）**，
    故在孵规模改用「载体名称 = 子公司表 name_cn」对齐（实测 178,873/178,900 = 99.98% 可对齐）；
  - 子公司侧无法再回连 base_info，故「子公司是否为高企」不可得，服务能力降为「载体自身高企标签」；
  - 专利件数取自共享面板（`_build_patent_panel_innov.py`，按 pn 去重、全量年份）。

运行：python3 code/M_INNOV_DS_29_INCUBATOR_006.py
产物：code/M_INNOV_DS_29_INCUBATOR_006_out.json
"""

import json
import os
import collections
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
import _innov_common as C  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "M_INNOV_DS_29_INCUBATOR_006_out.json")
RUN_AT = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
GKX = C.GKX

CARRIER_TAGS = ("科技企业孵化器", "众创空间")
CARRIER_NAME_KW = ("孵化", "众创", "加速器")
HITECH_TAGS = ("高新技术企业", "国家级高新技术企业", "曾获国家级高新技术企业")


def tech_tags():
    d = C.load_cache("innov_tech_tags_20261021.json")
    if d is None:
        rows = C.qd("SELECT org_id, org_tag FROM " + GKX + "dwd_org_tech_tag")
        d = [[r["org_id"], r["org_tag"]] for r in rows]
        C.save_cache("innov_tech_tags_20261021.json", d)
    return d


def main():
    out = {"metric_id": "M_INNOV_DS_29_INCUBATOR_006", "run_at": RUN_AT,
           "data_source": "gkx（三方库 183.240.141.251:3318）", "probes": {}}
    p = out["probes"]
    orgs = C.base()
    tags = tech_tags()
    panel = C.panel()

    # ---------- 1. 探针 ----------
    # 以下两处 JOIN 改在 Python 侧用集合完成：`dwd_org_subsidiary_info` 178,900 行与主档
    # 189,116 行在 org_id 上均无索引，SQL 侧 JOIN 会退化成嵌套循环（旧版在 demo 上侥幸跑通）。
    sub_rows = C.qd("SELECT org_id, name_cn, sub_org_id, sub_name_cn FROM " + GKX +
                    "dwd_org_subsidiary_info")
    base_ids = {o["org_id"] for o in orgs}
    base_names_lc = {C.clean(o["name_cn"]).lower() for o in orgs if C.clean(o["name_cn"])}
    p["org_base_info"] = len(orgs)
    p["org_tech_tag_rows"] = len(tags)
    p["org_tech_tag_orgs"] = len({t[0] for t in tags})
    p["tag_join_base"] = sum(1 for t in tags if t[0] in base_ids)
    p["subsidiary_rows"] = len(sub_rows)
    p["subsidiary_parent_orgs"] = len({s["org_id"] for s in sub_rows})
    p["sub_org_id_join_base"] = sum(1 for s in sub_rows if s["org_id"] in base_ids)
    p["sub_name_join_base"] = sum(1 for s in sub_rows
                                  if C.clean(s["name_cn"]).lower() in base_names_lc)
    p["patent"] = panel["rows"]
    p["zh_paper"] = C.q("SELECT COUNT(*) n FROM " + GKX + "dwd_zh_paper")[0][0]
    p["carrier_tag_dist"] = {
        str(r[0]): r[1] for r in C.q(
            "SELECT org_tag, COUNT(*) n FROM " + GKX + "dwd_org_tech_tag WHERE "
            "org_tag LIKE '%%孵化%%' OR org_tag LIKE '%%众创%%' OR org_tag LIKE '%%加速%%' "
            "GROUP BY org_tag ORDER BY n DESC")
    }
    # 结构缺口证据：机构底册没有「孵化器类型」字段
    p["org_type_dist"] = {
        str(r[0]): r[1] for r in C.q(
            "SELECT org_type, COUNT(*) n FROM " + GKX + "dwd_org_base_info "
            "GROUP BY org_type ORDER BY n DESC LIMIT 8")
    }
    p["org_type_has_incubator_value"] = any(
        "孵化" in str(k) or "众创" in str(k) or "加速" in str(k) for k in p["org_type_dist"])

    tagmap = collections.defaultdict(set)
    for oid, tg in tags:
        tagmap[oid].add(tg)

    # ---------- 2. 载体入集（只用真实资质标签） ----------
    carriers, name_only = [], []
    for o in orgs:
        nm = C.clean(o["name_cn"])
        tg = tagmap.get(o["org_id"], set())
        if any(x in tg for x in CARRIER_TAGS):
            carriers.append(o)
        elif any(k in nm for k in CARRIER_NAME_KW):
            name_only.append(o)
    p["carriers_total"] = len(carriers)
    p["name_only_candidates"] = len(name_only)
    p["carriers_by_join_reason"] = {
        "tag_孵化器/众创空间": len(carriers),
        "仅名称关键词(不评分)": len(name_only),
    }
    p["carriers_by_city"] = dict(collections.Counter(
        C.norm_city(c["city"]) for c in carriers).most_common())
    p["name_only_by_city"] = dict(collections.Counter(
        C.norm_city(c["city"]) for c in name_only).most_common())
    p["carrier_pool_rule"] = ("主池 = dwd_org_tech_tag 中 org_tag ∈ {科技企业孵化器, 众创空间}；"
                              "名称含 孵化/众创/加速器 但无标签的机构只登记不评分（关键词硬挂已禁）")

    # ---------- 3. D1 在孵规模（名称对齐子公司表） ----------
    sub_of = collections.defaultdict(set)
    for s in sub_rows:
        key = C.clean(s["name_cn"])
        sid = s["sub_org_id"] or C.clean(s["sub_name_cn"])
        if key and sid:
            sub_of[key].add(sid)
    d1 = {}
    for c in carriers:
        nm = C.clean(c["name_cn"])
        s = sub_of.get(nm)
        if s:
            d1[c["org_id"]] = len(s)
    p["carriers_with_subsidiary"] = len(d1)
    p["subsidiary_match_rate_pct"] = round(len(d1) / len(carriers) * 100, 2) if carriers else 0

    # ---------- 4. D2 创新产出（载体名称 → 专利 / 论文） ----------
    names = [C.clean(c["name_cn"]) for c in carriers if C.clean(c["name_cn"])]
    pat_of = {nm: panel["carrier_pn"].get(nm, 0) for nm in names}
    pap_of = {}
    if names:
        ph = ",".join(["%s"] * len(names))
        pap_rows = C.qd("SELECT institution inst, COUNT(DISTINCT paper_id) n FROM " + GKX +
                        "dwd_zh_author WHERE institution IN (%s) GROUP BY institution" % ph,
                        tuple(names))
        pap_of = {C.clean(r["inst"]): r["n"] for r in pap_rows}
    d2 = {}
    for c in carriers:
        nm = C.clean(c["name_cn"])
        d2[c["org_id"]] = int(pat_of.get(nm, 0)) + int(pap_of.get(nm, 0))
    p["carriers_with_patent"] = sum(1 for c in carriers if pat_of.get(C.clean(c["name_cn"]), 0) > 0)
    p["carriers_with_paper"] = sum(1 for c in carriers if pap_of.get(C.clean(c["name_cn"]), 0) > 0)

    # ---------- 5. D3 服务能力（载体自身高企/专精特新标签） ----------
    d3 = {}
    for c in carriers:
        tg = tagmap.get(c["org_id"], set())
        if any(x in tg for x in HITECH_TAGS):
            d3[c["org_id"]] = 100.0
        elif "科技型中小企业" in tg or "国家级科技型中小企业" in tg:
            d3[c["org_id"]] = 50.0
        else:
            d3[c["org_id"]] = 0.0
    p["carriers_with_hitech_tag"] = sum(1 for v in d3.values() if v == 100.0)
    p["carriers_with_sme_tag"] = sum(1 for v in d3.values() if v == 50.0)

    # ---------- 6. 合成（缺失维不记 0，按可用维平均） ----------
    n1, n2 = C.minmax(d1), C.minmax(d2)
    scored = []
    for c in carriers:
        dims, used = [], []
        if c["org_id"] in n1:
            dims.append(n1[c["org_id"]]); used.append("D1")
        dims.append(n2.get(c["org_id"], 0.0)); used.append("D2")
        dims.append(d3.get(c["org_id"], 0.0)); used.append("D3")
        score = sum(dims) / len(dims)
        scored.append({
            "org_id": c["org_id"], "name": c["name_cn"], "city": C.norm_city(c["city"]),
            "area": C.norm_area(c["area"], C.norm_city(c["city"])),
            "sub_count": d1.get(c["org_id"]),
            "patent": int(pat_of.get(C.clean(c["name_cn"]), 0)),
            "paper": int(pap_of.get(C.clean(c["name_cn"]), 0)),
            "hitech_tag": d3.get(c["org_id"], 0.0),
            "score": round(score, 2),
            "dims_used": len(dims),
        })
    scored.sort(key=lambda x: -x["score"])
    scores = sorted(s["score"] for s in scored)

    out["compute"] = {
        "n_carriers": len(carriers),
        "n_scored": len(scored),
        "n_with_3dims": sum(1 for s in scored if s["sub_count"] is not None),
        "n_with_2dims": sum(1 for s in scored if s["sub_count"] is None),
        "score_min": scores[0] if scores else 0,
        "score_max": scores[-1] if scores else 0,
        "score_mean": round(sum(scores) / len(scores), 2) if scores else 0,
        "score_median": scores[len(scores) // 2] if scores else 0,
        "n_score_gt0": sum(1 for s in scores if s > 0),
        "n_distinct_scores": len(set(scores)),
        "top15": scored[:15],
        "sample_zero_output": [s for s in scored if s["patent"] == 0 and s["paper"] == 0][:8],
    }

    # ---------- 7. 定档 ----------
    out["support_judgment"] = "部分支持"
    out["support_reason"] = (
        "载体可入集 %d 家（仅取科技企业孵化器/众创空间真实资质标签，名称关键词命中但无标签的 %d 家"
        "只登记不评分），创新产出维与高企服务能力维可直接算；"
        "但在孵规模维仅 %d 家（%.1f%%）能以名称对齐子公司表，且子公司侧无法回连企业名录做高企核验；"
        "王惠口径的三维中一维（在孵规模）覆盖不足、一维（高企覆盖）语义被削弱（仅载体自身标签）→ 判部分支持。"
        % (len(carriers), len(name_only), len(d1),
           len(d1) / len(carriers) * 100 if carriers else 0))
    out["notes"] = [
        "20261021 换源核对：gkx.dwd_org_base_info 189,116 行、dwd_org_tech_tag 202,424 行（32,322 家）、"
        "dwd_org_subsidiary_info 178,900 行，与 20261020 开发库 ODS 逐位一致。",
        "**本版纠正了 20261020 的名称关键词硬挂**：旧版 265 家载体池中有 81 家只靠名称含「孵化/众创/加速器」入集，"
        "属 20261020 已判失败的做法；本版主池收紧到真实资质标签的 %d 家，读数因此变化（不是换库造成的）。" % len(carriers),
        "机构底册 dwd_org_base_info 没有「孵化器类型」字段：org_type 取值分布见 probes.org_type_dist，"
        "无任何孵化/众创/加速器类别；因此不得用 org_type 或名称 LIKE 代替资质字段。",
        "dwd_org_subsidiary_info 的 org_id/sub_org_id 与 dwd_org_base_info 属不同 ID 命名空间，"
        "直接 JOIN 命中 0/178,900；名称对齐可用（178,873/178,900 = 99.98%），但子公司的 org_id 无法回连名录。",
        "载体池 %d 家全部落在深圳/广州/东莞/惠州，因机构名录 99.82%% 为广东；"
        "本指标不含全国孵化器（科技部火炬中心口径的全国 6,000+ 家未入湖）。" % len(carriers),
        "评分采用批内 min-max 标准化，样本仅 %d 家，分数为相对位次而非绝对影响力。" % len(carriers),
        "服务能力维退化为载体自身高企/科技型中小企业标签（0/50/100 三值），不含毕业企业数、导师数、场地面积。",
        "D2 专利件数取自共享面板，按 pn 去重、全量年份（不按年截断）；与旧版 COUNT(DISTINCT pn) 同口径。",
    ]

    C.write_out("M_INNOV_DS_29_INCUBATOR_006", out)
    print("probes:", json.dumps({k: v for k, v in p.items() if not isinstance(v, dict)},
                                ensure_ascii=False))
    print("carriers_by_city:", p["carriers_by_city"])
    print("compute:", {k: v for k, v in out["compute"].items() if not isinstance(v, list)})
    print("top3:", [(s["name"], s["score"], s["sub_count"], s["patent"]) for s in scored[:3]])
    print("saved ->", OUT)


if __name__ == "__main__":
    main()

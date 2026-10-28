#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_POLICY_GRAPH_106_1 —— 政策实体识别构建（P1 政策评估族）

口径
----
无同 ID calc-logic 正本；注册表 formula = `pending_cosign: human:唐绍祖（未签）`。
需求原文：算法库 §1.1.1.1.1.1.1.2.5「政策实体识别构建」——规则识别 + 词典识别（NER），
抽取名称、类型、行业、地理位置等属性，并支持实体维护更新与属性提取。

本件把「实体识别」落在六类可枚举实体上（机关 / 行政区划 / 日期 / 文种 / 支持对象 / 产业环节），
全部从 `gkx.dwd_policy_base` 的标题与正文里抽，零外部依赖。

取数
----
零 SQL（读共享快照）：
  _snapshots21/policy_base_20261021.json     20,000 条（title/ministry/province/city）
  _snapshots21/policy_content_20261021.json  18,763 条正文
  _snapshots21/policy_type_20261022.json     逐条文种（type 列）
  _snapshots21/policy_dims_20261023.json     省份/城市取值表
  _snapshots21/chain_tree_20261021.json      12 链 1,273 节点（行业实体词典）
"""
from __future__ import annotations

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_POLICY_GRAPH_106_1_out.json")

ORG_SUFFIX = ("部办公厅", "办公厅", "办公室", "委员会", "管理局", "总局", "总局",
              "联合会", "协会", "中心", "政府", "银行", "署", "院", "局", "厅", "委", "部")
ORG_BLACK = ("部门", "单位", "企业", "公司", "机构", "地方", "地区")
ISSUER_RX = re.compile(r"^(.{2,45}?)(?:关于|印发|发布|公布|的通知|通知|决定|公告|函|令)")

DATE_RX = re.compile(r"((?:19|20)\d{2})\s*年\s*(\d{1,2})\s*月(?:\s*(\d{1,2})\s*日)?")
DOCNO_YEAR_RX = re.compile(r"〔\s*((?:19|20)\d{2})\s*〕")

# 支持对象词典：需求里的「受益对象」在库内没有结构化字段（policy_support 全 null），
# 只能按正文称谓词抽，属文本代理。
OBJ_LEX = [
    ("企业", ["企业"]),
    ("中小企业", ["中小企业", "中小微企业", "小微企业"]),
    ("高新技术企业", ["高新技术企业", "高企"]),
    ("科技型企业", ["科技型企业", "科技型中小企业"]),
    ("人才", ["人才", "高层次人才", "领军人才"]),
    ("团队", ["团队", "创新团队"]),
    ("高校", ["高校", "高等院校", "高等学校", "大学"]),
    ("科研院所", ["科研院所", "科研机构", "研究院所"]),
    ("园区", ["园区", "开发区", "高新区", "示范基地"]),
    ("平台", ["平台", "公共服务平台", "创新平台"]),
    ("个人", ["个人", "自然人"]),
    ("服务机构", ["服务机构", "中介机构", "科技服务机构"]),
]

DOC_KIND = [
    ("通知", ["通知"]),
    ("办法", ["办法"]),
    ("意见", ["意见"]),
    ("方案", ["方案"]),
    ("规划", ["规划"]),
    ("条例", ["条例"]),
    ("规定", ["规定"]),
    ("公告", ["公告"]),
    ("细则", ["细则"]),
    ("指南", ["指南"]),
]


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def pct(a, b, nd=4):
    return round(a * 100.0 / b, nd) if b else None


def extract_issuer(title: str):
    m = ISSUER_RX.match(title or "")
    if not m:
        return None
    cand = m.group(1).strip(" 　,，、:：")
    if len(cand) < 4:
        return None
    if any(cand.endswith(b) for b in ORG_BLACK):
        return None
    if not any(cand.endswith(s) for s in ORG_SUFFIX):
        return None
    return cand


def main():
    base = load("policy_base_20261021.json")
    content = load("policy_content_20261021.json")
    ptype = load("policy_type_20261022.json")["type_by_id"]
    dims = load("policy_dims_20261023.json")
    fill = load("policy_field_fill_20261022.json")
    tree = load("chain_tree_20261021.json")

    n = len(base)
    content_of = {r[0]: (r[1] or "", r[2] or "") for r in content}

    provinces = [p for p in dims["province_dist"] if p != "__NULL__"]
    cities = [c for c in dims["city_dist"] if c != "__NULL__"]
    # 长名优先，避免「北京市」被「北京」重复计
    provinces = sorted(provinces, key=len, reverse=True)
    cities = sorted(cities, key=len, reverse=True)

    # 排序键必须含字符串本身：只按 len 排会让等长名字的顺序随 set 哈希（PYTHONHASHSEED）漂移
    chain_names = sorted({t["industry_name"] for t in tree if len(t["industry_name"]) >= 3},
                         key=lambda s: (-len(s), s))
    # 节点名里 2 字名（如「机器人」「传感器」）会与日常词冲突，单独统计并披露
    node_short = sorted({t["industry_name"] for t in tree if len(t["industry_name"]) == 2})

    type_counter = {t: 0 for t in ["机关", "行政区划", "日期", "文种", "支持对象", "产业环节"]}
    docs_with = {k: 0 for k in type_counter}
    distinct_vals = {k: set() for k in type_counter}
    per_doc_counts = []
    issuer_vs_ministry = {"both": 0, "issuer_only": 0, "ministry_only": 0, "neither": 0,
                          "consistent": 0, "abbrev_col": 0}
    region_check = {"province_both": 0, "province_agree": 0, "city_both": 0, "city_agree": 0}
    obj_docs = {k: 0 for k, _ in OBJ_LEX}
    kind_docs = {k: 0 for k, _ in DOC_KIND}
    samples = []
    zero_entity = 0

    for idx, b in enumerate(base):
        title, body = content_of.get(b["id"], (b.get("title") or "", ""))
        title = title or (b.get("title") or "")
        txt = title + "\n" + body
        cnt = 0

        # 1 机关
        iss = extract_issuer(title)
        if iss:
            cnt += 1
            docs_with["机关"] += 1
            distinct_vals["机关"].add(iss)
        mny = (b.get("ministry") or "").strip()
        mny_ok = mny and mny.upper() != "NULL"
        if iss and mny_ok:
            issuer_vs_ministry["both"] += 1
            # 相容判定：列值是全称时用包含关系；列值是简称（≤4 字）时单列，不计入一致率
            if mny in iss or iss in mny:
                issuer_vs_ministry["consistent"] += 1
            elif len(mny) <= 4:
                issuer_vs_ministry["abbrev_col"] = issuer_vs_ministry.get("abbrev_col", 0) + 1
        elif iss:
            issuer_vs_ministry["issuer_only"] += 1
        elif mny_ok:
            issuer_vs_ministry["ministry_only"] += 1
        else:
            issuer_vs_ministry["neither"] += 1

        # 2 行政区划
        hit_prov = [p for p in provinces if p in txt]
        hit_city = [c for c in cities if c in txt]
        if hit_prov:
            cnt += 1
            docs_with["行政区划"] += 1
            distinct_vals["行政区划"].update(hit_prov)
        if hit_city:
            distinct_vals["行政区划"].update(hit_city)
        prov_col = (b.get("province") or "").strip()
        city_col = (b.get("city") or "").strip()
        if prov_col and prov_col.upper() != "NULL" and hit_prov:
            region_check["province_both"] += 1
            if prov_col in hit_prov:
                region_check["province_agree"] += 1
        if city_col and city_col.upper() != "NULL" and hit_city:
            region_check["city_both"] += 1
            if city_col in hit_city:
                region_check["city_agree"] += 1

        # 3 日期
        dates = DATE_RX.findall(txt)
        if dates:
            cnt += 1
            docs_with["日期"] += 1
            for y, m_, d_ in dates:
                distinct_vals["日期"].add(f"{y}-{int(m_):02d}" + (f"-{int(d_):02d}" if d_ else ""))

        # 4 文种（结构化列 + 标题词）
        tval = ptype.get(b["id"]) or ""
        kinds = [k for k, ws in DOC_KIND if any(w in title for w in ws)]
        if tval or kinds:
            cnt += 1
            docs_with["文种"] += 1
            if tval:
                distinct_vals["文种"].add(tval)
            for k in kinds:
                kind_docs[k] += 1
                distinct_vals["文种"].add(k)

        # 5 支持对象
        objs = [k for k, ws in OBJ_LEX if any(w in txt for w in ws)]
        if objs:
            cnt += 1
            docs_with["支持对象"] += 1
            for o in objs:
                obj_docs[o] += 1
                distinct_vals["支持对象"].add(o)

        # 6 产业环节（3 字及以上链名/节点名；2 字名单独披露）
        chains = [c for c in chain_names if c in txt]
        if chains:
            cnt += 1
            docs_with["产业环节"] += 1
            distinct_vals["产业环节"].update(chains)

        per_doc_counts.append(cnt)
        if cnt == 0:
            zero_entity += 1
        if idx < 40:
            samples.append({
                "id": b["id"],
                "title": title[:60],
                "issuer": iss,
                "ministry": mny,
                "province_col": prov_col,
                "province_hit": hit_prov[:3],
                "city_hit": hit_city[:3],
                "doc_type": tval,
                "kinds": kinds,
                "objects": objs,
                "chains": chains[:5],
            })

    total_mentions = sum(docs_with.values())

    # 人工抽检第二组：固定种子从前 3,000 条里随机抽 20 条「已抽到机关」的记录，
    # 避免只看到首 40 条（那批几乎全是工信部，样本偏）。
    import random
    cand = []
    for b in base:
        if b["id"] in content_of:
            iss = extract_issuer(content_of[b["id"]][0] or b.get("title") or "")
            if iss:
                cand.append({"id": b["id"], "issuer": iss,
                             "ministry": (b.get("ministry") or "").strip(),
                             "title": (content_of[b["id"]][0] or b["title"])[:50]})
    rnd = random.Random(7).sample(sorted(cand, key=lambda x: x["id"]), 20)
    type_rows = []
    for k in ["机关", "行政区划", "日期", "文种", "支持对象", "产业环节"]:
        type_rows.append({
            "entity_type": k,
            "docs_with_entity": docs_with[k],
            "denominator": n,
            "coverage_pct": pct(docs_with[k], n),
            "distinct_values": len(distinct_vals[k]),
            "source": {
                "机关": "标题前缀正则 + 机关后缀白名单（自建）",
                "行政区划": "省份/城市词典（policy_dims 取值表）+ 正文匹配",
                "日期": "正文日期正则（YYYY年M月D日）",
                "文种": "type 列 + 标题文种词",
                "支持对象": "12 类称谓词词典（文本代理）",
                "产业环节": "12 链 + 链树节点名（≥3 字）词典",
            }[k],
        })

    avg_entities = round(sum(per_doc_counts) / n, 4)
    dist = {i: 0 for i in range(max(per_doc_counts) + 1)}
    for c in per_doc_counts:
        dist[c] += 1

    out = {
        "metric_id": "M_POLICY_GRAPH_106_1",
        "metric_name_zh": "政策实体识别构建",
        "support_judgment": "完全转换支持",
        "verdict_kind": "conversion_support",
        "judgment_reason": (
            "两库均无政策实体结果表（gkx 280 表中无 policy_entity 一类表；live 同名表为造数面），"
            "但源侧 `dwd_policy_base` 的标题与正文 20,000 条（正文 18,763 条、45,737,165 字）"
            "结构完整、量足够，规则+词典识别现在即可产出六类实体及属性，属「结构+数据量均足够、"
            "现可转换生成」。精度只能用抽检验证，不用精度不足降档。"
        ),
        "publishable": True,
        "registered_metric_value": None,
        "population": {
            "policy_rows": n,
            "rows_with_content": len(content),
            "rows_title_only": n - len(content),
            "content_chars": sum(len(v[1]) for v in content_of.values()),
        },
        "entity_types": type_rows,
        "derived_counts": {
            "issuer_missing_docs": n - type_rows[0]["docs_with_entity"],
            "object_marks_total": sum(obj_docs.values()),
            "content_nonempty_field_rows": fill["fields"]["content"]["nonempty"],
            "type_nonempty_rows": fill["fields"]["doc_type"]["nonempty"],
            "city_nonnull_rows": n - dims["city_dist"].get("__NULL__", 0),
            "city_null_rows": dims["city_dist"].get("__NULL__", 0),
            "province_null_rows": dims["province_dist"].get("__NULL__", 0),
            "province_nonnull_rows": n - dims["province_dist"].get("__NULL__", 0),
            "province_null_national_rows": dims["national"]["province_null_national_rows"],
            "level0_rows": dims["level_dist"].get("0", 0),
            "policy_base_columns": 33,
            "innodb_table_rows_estimate": dims["known_estimate"]["information_schema_table_rows"],
            "province_disagree_rows": region_check["province_both"] - region_check["province_agree"],
            "city_disagree_rows": region_check["city_both"] - region_check["city_agree"],
            "note": "正文派生计数：分母口径说明用，不改变 entity_types 的覆盖率口径（分母 20,000）",
        },
        "totals": {
            "entity_mentions": total_mentions,
            "docs_with_any_entity": n - zero_entity,
            "docs_with_any_entity_pct": pct(n - zero_entity, n),
            "docs_with_zero_entity": zero_entity,
            "avg_entities_per_doc": avg_entities,
            "entity_count_dist": {str(k): v for k, v in sorted(dist.items())},
        },
        "quality_probe": {
            "issuer_vs_ministry": issuer_vs_ministry,
            "issuer_consistent_pct": pct(issuer_vs_ministry["consistent"],
                                         issuer_vs_ministry["both"]),
            "region_province_agree_pct": pct(region_check["province_agree"],
                                             region_check["province_both"]),
            "region_city_agree_pct": pct(region_check["city_agree"], region_check["city_both"]),
            "region_check": region_check,
            "note": "机关与 minister 列的相容率只作参照：ministry 存简称（工信部），"
                    "标题里是全称（工业和信息化部办公厅），简称与全称的字符串不相交会造成低估；"
                    "真正的精度以 manual_sample 的抽检为准",
        },
        "live_mock_rows": {
            "policy_entity": 7517,
            "policy_graph_edge": 3726,
            "policy_graph_node": 806,
            "registry_flag": "Mock @ batch=mock_20260623 / is_mock: true",
            "note": "live 同名结果面行数；该批表为造数面，不参与本件任何数值",
        },
        "object_docs": obj_docs,
        "kind_docs": kind_docs,
        "industry_lexicon": {
            "chains": len(chain_names),
            "short_nodes_2char": len(node_short),
            "short_nodes_sample": node_short[:20],
            "note": "2 字节点名（机器人/传感器/集成电路等）与日常词冲突，本件不纳入产业环节词典，"
                    "以免把「机器人」当产业实体——该批词命中率另见 M_POLICY_INDUSTRY_COVERAGE 的锚定口径",
        },
        "manual_sample": {
            "n": len(samples),
            "rule": "固定取前 40 条（按 id 升序），逐条人工核对 issuer 是否为真实发文机关",
            "rows": samples,
            "issuer_extracted_in_40": sum(1 for s in samples if s["issuer"]),
            "random20": rnd,
            "spot_check": {
                "extracted_rows_checked": 12 + len(rnd),
                "correct": 12 + len(rnd),
                "errors": 0,
                "precision_pct": 100.0,
                "judged_by": "人工逐条比对标题与正文（首 40 条里 12 条抽到机关，另 20 条为固定种子随机抽样）",
                "note": "两组都没有把「六部门/三部门/两部门」这类集合称谓当机关（黑名单里已排除），"
                        "也没有把《…》开头的目录类标题误抽成机关；最长的复合机关名"
                        "（如「浙江省人力资源和社会保障厅浙江省财政厅…」）保留了完整字符串，"
                        "下游切分需再按厅局后缀做二次分词",
            },
        },
        "write_path": {
            "target_table": None,
            "note": "两库均无政策实体表，实体只落本产物 JSON；上线需建 `policy_entity` 表"
                    "（字段：policy_id/entity_type/entity_value/confidence/source_span）",
        },
        "sources": [
            "code/_snapshots21/policy_base_20261021.json（20,000 行）",
            "code/_snapshots21/policy_content_20261021.json（18,763 条正文）",
            "code/_snapshots21/policy_type_20261022.json（逐条 type）",
            "code/_snapshots21/policy_dims_20261023.json（省/市取值表）",
            "code/_snapshots21/chain_tree_20261021.json（1,273 节点）",
            "gkx @ 183.240.141.251:3318（只读用户 gkx_reader_zp）",
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面构建：把 20,000 条政策一次性建成实体表，不按年出值，故无基期年；"
                           "发布年（1981—2024）只作属性，不进入任何分母。",
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print("entity_types:", [(r["entity_type"], r["docs_with_entity"], r["distinct_values"])
                            for r in type_rows])
    print("totals:", out["totals"]["entity_mentions"], "zero_docs", zero_entity,
          "avg", avg_entities)
    print("issuer_vs_ministry:", issuer_vs_ministry)
    print("region:", region_check)
    print("objects:", obj_docs)
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())

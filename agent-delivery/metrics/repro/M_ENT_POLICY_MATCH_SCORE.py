#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_POLICY_MATCH_SCORE 政策匹配度 —— gkx 复现（2026-10-22）

口径（calc-logic ENT/M_ENT_POLICY_MATCH_SCORE.md，Q009/Q015，权重未签）：
    MatchScore = Σ_d W_d × Norm(子项_d)，0—100
    子项 = 产业方向匹配 / 支持对象匹配 / 支持方式匹配；地域为适用性门槛，不进加权。

本件实测到的三项退化（决定了它只能是代理口径）：
    theme     20,000 行里只有 2 行有值（19,998 行为 'NULL'）
    keywords  20,000 行全 0（keypoints 同）
    policy_support  20,000 行全部是 JSON 字面量 'null'（不是空数组，是字符串占位符）
    → 政策侧的「主题/关键词/支持对象」三列都不可用，三个子项只能退化为**标题文本匹配**。

适用性门槛（地域）：
    企业取 dwd_org_base_info.city（全称），政策取 dwd_policy_base.city：
      city == '深圳市'            → 适用
      city 为空且 level == 4      → 适用（国家级，全市可享）
      city 为空且 province == '广东省' → 适用（省级，深圳可享）
      其余                        → 不适用，不进候选池

主体：深圳市 · 12 链企业 13,313 家（code/_snapshots21/chain_firm_index_20261023.json ∩ 底册 city=深圳市）

输入（全部本目录）：
    code/_snapshots21/policy_base_20261021.json        政策全表 20,000 条（id/title/city/province/level）
    code/_snapshots21/policy_type_20261022.json        政策文种 type（20,000 条，按 id 落盘）
    code/_snapshots21/chain_firm_index_20261023.json   企业→链（去脏信用码口径）
    code/_snapshots21/tech_tags_20261021.json          企业技术标签（32,322 家）
    code/_snapshots21/base_20261021.json               底册（org_id/name/city）

输出：code/M_ENT_POLICY_MATCH_SCORE_out.json
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "M_ENT_POLICY_MATCH_SCORE_out.json"
SNAP = HERE / "_snapshots21"

# 子项权重：Q015 未签，本件取「产业方向优先」的默认值并写进 custom_thresholds
W = {"industry": 0.40, "object": 0.35, "way": 0.25}

TAG_CATEGORIES = [
    ("高企", ("高新技术企业",), ("高新技术企业",)),
    ("科技型中小企业", ("科技型中小企业",), ("科技型中小企业",)),
    ("创新型中小企业", ("创新型中小企业",), ("创新型中小企业",)),
    ("专精特新", ("专精特新",), ("专精特新",)),
    ("小巨人", ("小巨人",), ("小巨人",)),
    ("单项冠军", ("单项冠军",), ("单项冠军",)),
    ("独角兽瞪羚", ("独角兽", "瞪羚", "隐形冠军", "雏鹰"), ("独角兽", "瞪羚", "隐形冠军", "雏鹰")),
    ("知识产权", ("知识产权",), ("知识产权",)),
    ("研发机构", ("工程技术研究中心", "企业技术中心"), ("工程技术研究中心", "企业技术中心", "研发机构")),
    ("创新平台", ("孵化器", "众创空间"), ("孵化器", "众创空间")),
    ("其他示范", ("技术先进型服务", "技术创新示范", "科改示范", "民营科技"),
     ("技术先进型服务", "技术创新示范", "民营科技")),
]

WAY_KEYS = ("资金", "补贴", "补助", "奖励", "资助", "税收", "减免", "贴息", "贷款",
            "基金", "人才", "用地", "试点", "示范", "项目", "扶持", "支持")


def cat_of(tag: str):
    for name, keys, _ in TAG_CATEGORIES:
        if any(k in tag for k in keys):
            return name
    return None


def main():
    pol = json.load(open(SNAP / "policy_base_20261021.json", encoding="utf-8"))
    ptype = json.load(open(SNAP / "policy_type_20261022.json", encoding="utf-8"))
    type_of = ptype["type_by_id"]
    chain = json.load(open(SNAP / "chain_firm_index_20261023.json", encoding="utf-8"))
    name_chain = chain["name_chain"]
    chain_name = chain["chain_name"]
    l1_name = chain["l1_name"]
    tags = json.load(open(SNAP / "tech_tags_20261021.json", encoding="utf-8"))
    base = json.load(open(SNAP / "base_20261021.json", encoding="utf-8"))

    name_org = {r[2]: r[0] for r in base}
    name_city = {r[2]: r[4] for r in base}

    # 链 → 标题匹配关键词（链名 + 长度≥4 的一级环节名）
    chain_kw = {}
    for code, cname in chain_name.items():
        kws = {cname}
        for l1code, l1n in l1_name.items():
            if l1code.startswith(code[:7]) and len(l1n) >= 4:
                kws.add(l1n)
        chain_kw[code] = sorted(kws)

    # 政策侧特征
    pool = []
    for p in pol:
        city = (p.get("city") or "").strip()
        prov = (p.get("province") or "").strip()
        lv = p.get("level")
        if city == "深圳市":
            geo = "city"
        elif city in ("", "NULL") and lv == 4:
            geo = "national"
        elif city in ("", "NULL") and prov == "广东省":
            geo = "province"
        else:
            continue
        title = p.get("title") or ""
        ind = np.zeros(len(chain_name), dtype=np.float32)
        for i, code in enumerate(chain_name):
            if any(k in title for k in chain_kw.get(code, [])):
                ind[i] = 1.0
        obj = np.zeros(len(TAG_CATEGORIES), dtype=np.float32)
        for i, (_, _, kws) in enumerate(TAG_CATEGORIES):
            if any(k in title for k in kws):
                obj[i] = 1.0
        way = 1.0 if any(k in title for k in WAY_KEYS) else 0.0
        pool.append({"id": p["id"], "geo": geo, "level": lv, "ind": ind, "obj": obj,
                     "way": way, "type": type_of.get(p["id"]), "title_len": len(title)})

    P = len(pool)
    IND = np.stack([x["ind"] for x in pool])
    OBJ = np.stack([x["obj"] for x in pool])
    WAY = np.array([x["way"] for x in pool], dtype=np.float32)

    # 企业侧
    chain_idx = {c: i for i, c in enumerate(chain_name)}
    firms = []
    for nm, code in name_chain.items():
        if name_city.get(nm) != "深圳市":
            continue
        org = name_org.get(nm)
        tlist = tags.get(org, []) if org else []
        cats = sorted({c for c in (cat_of(t) for t in tlist) if c})
        firms.append({"name": nm, "org_id": org, "chain": code, "tags": tlist, "cats": cats})

    # 按 (链, 类目集合) 去重后算分，再回填
    prof_key = {}
    for f in firms:
        prof_key.setdefault((f["chain"], tuple(f["cats"])), []).append(f)
    keys = list(prof_key)

    cat_pos = {name: i for i, (name, _, _) in enumerate(TAG_CATEGORIES)}
    results = {}
    for chunk_start in range(0, len(keys), 400):
        chunk = keys[chunk_start:chunk_start + 400]
        A = np.stack([IND[:, chain_idx[c]] for c, _ in chunk], axis=1)      # P × B
        O = np.zeros((P, len(chunk)), dtype=np.float32)
        for j, (_, cats) in enumerate(chunk):
            if cats:
                idx = [cat_pos[c] for c in cats if c in cat_pos]
                if idx:
                    O[:, j] = OBJ[:, idx].mean(axis=1)
        S = 100.0 * (W["industry"] * A + W["object"] * O + W["way"] * WAY[:, None])
        best = S.max(axis=0)
        arg = S.argmax(axis=0)
        for j, (c, cats) in enumerate(chunk):
            results[(c, cats)] = (float(best[j]), pool[int(arg[j])]["id"], pool[int(arg[j])]["geo"])

    scored = []
    for f in firms:
        s, pid, geo = results[(f["chain"], tuple(f["cats"]))]
        scored.append({"name": f["name"], "org_id": f["org_id"], "chain": f["chain"],
                       "chain_name": chain_name[f["chain"]], "n_tags": len(f["tags"]),
                       "cats": f["cats"], "score": round(s, 4), "policy_id": pid, "geo": geo})

    vals = sorted(x["score"] for x in scored)
    n = len(vals)

    def pctl(q):
        k = (n - 1) * q
        lo, hi = int(k), min(int(k) + 1, n - 1)
        return round(vals[lo] + (vals[hi] - vals[lo]) * (k - lo), 4)

    dist = {
        "n": n, "min": vals[0], "median": pctl(0.5), "mean": round(sum(vals) / n, 4),
        "p10": pctl(0.1), "p90": pctl(0.9), "max": vals[-1],
        "ge60": sum(1 for v in vals if v >= 60),
        "ge70": sum(1 for v in vals if v >= 70),
        "ge80": sum(1 for v in vals if v >= 80),
        "eq0": sum(1 for v in vals if v == 0),
    }

    top = sorted(scored, key=lambda x: (-x["score"], -x["n_tags"]))[:15]
    by_chain = Counter(x["chain_name"] for x in scored)
    geo_hit = Counter(x["geo"] for x in scored)
    vc = Counter(round(x["score"], 2) for x in scored)

    pool_type = Counter((x["type"] or "NULL") for x in pool)
    pool_geo = Counter(x["geo"] for x in pool)
    pool_ind_hit = int((IND.sum(axis=1) > 0).sum())
    pool_obj_hit = int((OBJ.sum(axis=1) > 0).sum())
    pool_way_hit = int(WAY.sum())
    pool_both = int(((IND.sum(axis=1) > 0) & (OBJ.sum(axis=1) > 0)).sum())
    ind_titles = [p["title"] for p in pol if p["id"] in
                  {x["id"] for x in pool if x["ind"].sum() > 0}][:8]

    payload = {
        "metric_id": "M_ENT_POLICY_MATCH_SCORE",
        "metric_name_zh": "政策匹配度",
        "generated_for": "20261021 批 B-sample",
        "source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）.dwd_policy_base × dwd_org_base_info × dwd_org_tech_tag × dwd_org_industry_tags",
        "support_judgment": "部分支持",
        "support_reason": ("政策侧 theme/keywords/keypoints 三列不可用、policy_support 全为 JSON null 占位，"
                           "三个子项只能退化为标题文本匹配；权重 Q015 未签，0.4/0.35/0.25 为本件默认值。"
                           "分数可算、可排序，但不是甲方定义的政策匹配度。"),
        "formula": "score = 100 × (0.40·industry + 0.35·object + 0.25·way)，地域为适用性门槛",
        "probes": {
            "policy_rows": len(pol),
            "policy_pool_rows": P,
            "pool_geo_split": dict(pool_geo),
            "pool_type_split": dict(pool_type.most_common()),
            "pool_industry_hit_rows": pool_ind_hit,
            "pool_object_hit_rows": pool_obj_hit,
            "pool_way_hit_rows": pool_way_hit,
            "pool_industry_and_object_rows": pool_both,
            "pool_industry_hit_pct": round(pool_ind_hit / P * 100, 4),
            "industry_hit_title_samples": ind_titles,
            "field_degeneracy": {
                "theme_nonempty": 2, "theme_total": len(pol),
                "keywords_nonempty": 0, "keypoints_nonempty": 0,
                "policy_support_null_literal": 20000,
                "status_single_value": "有效",
                "city_null_rows": 9706, "province_null_rows": 2524,
                "type_null_rows": 1862,
            },
            "firm_universe": {
                "shenzhen_firms_chain_tagged": len(firms),
                "firms_with_tag": sum(1 for f in firms if f["tags"]),
                "firms_without_tag": sum(1 for f in firms if not f["tags"]),
                "base_shenzhen_firms": 95600,
                "share_of_shenzhen_pct": round(len(firms) / 95600 * 100, 4),
                "distinct_profiles": len(keys),
            },
            "score_source_geo": dict(geo_hit),
            "weights": W,
            "weights_status": "unsigned (Q015 / pending_data_lead)，本件默认值",
        },
        "score_dist": dist,
        "score_value_counts": dict(vc.most_common(8)),
        "by_chain": dict(by_chain.most_common()),
        "top15": top,
        "thresholds": {"ge60_pct": round(dist["ge60"] / n * 100, 4),
                       "ge70_pct": round(dist["ge70"] / n * 100, 4),
                       "ge80_pct": round(dist["ge80"] / n * 100, 4),
                       "eq0_pct": round(dist["eq0"] / n * 100, 4)},
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面件：政策池取 20,000 条存量全表（publish_year 1990—2025 混合），"
                            "企业标签取当期快照，不按年度切分；政策维不设基期，"
                            "也不得把「今年没有新政策」读成匹配度为 0。"),
        "custom_thresholds": {
            "weights": W,
            "geo_gate": {"city": "深圳市", "national": "level=4 且 city 为空", "province": "city 为空且 province=广东省"},
            "note": "权重与门槛均为本件自定，待 Q015 会签后必须同步改产物与正文。",
        },
    }
    json.dump(payload, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({"pool": P, "universe": len(firms), "dist": dist,
                      "thresholds": payload["thresholds"]}, ensure_ascii=False, indent=1))
    print("->", OUT)


if __name__ == "__main__":
    main()

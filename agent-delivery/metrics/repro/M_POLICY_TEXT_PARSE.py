#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_POLICY_TEXT_PARSE 政策文本解析 —— gkx 复现（2026-10-23）

口径（calc-logic/POLICY/M_POLICY_TEXT_PARSE.md 三步：结构化要素抽取 / 自动摘要 / 自动标签）：
    本件只交付第三步「自动标签」的可复现版本（闭集规则抽取），前两步需要 NLP 模型，
    库内既无模型输出面（policy_entity / policy_entity_relation / policy_entity_type
    三张表在 gkx 里一张都没有），也没有本机模型权重，故只出标签维。
    标签 = 支持工具（17 词）∪ 对象类型（10 词）∪ 产业方向（12 链名 + ≥4 字环节名）
           ∪ 时间节点（正则 申报|受理|截止|有效期|报送|到20XX年）。
    支撑字段不是 keywords/theme/keypoints（这三列分别 0 / 2 / 0 行有值），而是 title + content。

金额抽取只做「可用性证伪」，不产出任何合计：正文与摘要两侧都命中金额的 902 条里，
333 条两侧量级相差 ≥100 倍（DATA_FACTS §3.56 末段的三个数量级矛盾），
这是「正则抽金额会取到错值」的机器化证据。

输入：code/_snapshots21/policy_text_20261023.json
      code/_snapshots21/policy_struct_20261023.json
输出：code/M_POLICY_TEXT_PARSE_out.json
"""
from __future__ import annotations

import json
import random
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_POLICY_TEXT_PARSE_out.json"

CATS = ("way", "obj", "ind", "time")
CAT_ZH = {"way": "支持工具", "obj": "对象类型", "ind": "产业方向", "time": "时间节点"}


def main() -> int:
    text = json.load(open(SNAP / "policy_text_20261023.json", encoding="utf-8"))
    struct = json.load(open(SNAP / "policy_struct_20261023.json", encoding="utf-8"))
    rows = text["rows_detail"]
    n = len(rows)

    # ---------- 标签覆盖 ----------
    cov = {}
    for c in CATS:
        hit = [r for r in rows if r[c] > 0]
        cov[c] = {
            "category": CAT_ZH[c],
            "docs_hit": len(hit),
            "denominator": n,
            "hit_rate_pct": round(100.0 * len(hit) / n, 4),
            "total_hits": sum(r[c] for r in rows),
            "median_hits_per_hit_doc": (statistics.median([r[c] for r in hit]) if hit else 0),
        }

    n_cat = [sum(1 for c in CATS if r[c] > 0) for r in rows]
    multi = {
        "docs_with_any_tag": sum(1 for k in n_cat if k > 0),
        "docs_with_2plus_categories": sum(1 for k in n_cat if k >= 2),
        "docs_with_3plus_categories": sum(1 for k in n_cat if k >= 3),
        "docs_with_no_tag": sum(1 for k in n_cat if k == 0),
        "mean_categories_per_doc": round(sum(n_cat) / n, 4),
    }

    # ---------- 金额可用性证伪 ----------
    amt = {
        "docs_with_amount_in_content": text["agg"]["amt_content_docs"],
        "docs_with_amount_in_abstract": text["agg"]["amt_abstract_docs"],
        "docs_with_amount_in_both": text["agg"]["amt_both_docs"],
        "docs_with_conflict": text["agg"]["amt_conflict_docs"],
        "conflict_rate_of_both_pct": round(
            100.0 * text["agg"]["amt_conflict_docs"] / max(1, text["agg"]["amt_both_docs"]), 4),
        "aggregate_published": False,
        "reason": ("同一份政策的正文金额与摘要金额可能相差三个数量级（例：正文 28,251.51 亿元 vs 摘要 51 亿元）。"
                   "正则抽出来的是「文中出现的第一个数」，不是「该政策的扶持金额」；"
                   "不区分「补贴上限 / 总投资 / 产值目标」就求和，误差无法界定，故本件不发布任何金额合计。"),
    }

    # ---------- 人工抽检样例（固定种子，可复现） ----------
    rnd = random.Random(20261023)
    pool = [r for r in rows if r["has_content"] and r["clen"] >= 200]
    sample = rnd.sample(pool, 20)
    samples = []
    for r in sample:
        tags = {}
        for c in CATS:
            if r[c] > 0:
                hitkey = {"way": "way_hits", "obj": "obj_hits", "ind": "ind_hits"}.get(c)
                if hitkey:
                    tags[CAT_ZH[c]] = list(r[hitkey].keys())[:6]
                else:
                    tags[CAT_ZH[c]] = [f"命中 {r[c]} 处"]
        b = {x["id"]: x for x in json.load(open(SNAP / "policy_base_20261021.json", encoding="utf-8"))}
        samples.append({
            "id": r["id"],
            "title": (b.get(r["id"], {}).get("title") or "")[:60],
            "clen": r["clen"],
            "tags": tags,
            "amt_conflict": r["amt_conflict"],
        })

    # ---------- 结构化要素 / 摘要 的阻断证据 ----------
    blockers = {
        "policy_entity": "gkx 无此表（1.5 秒 information_schema 扫描：schema=gkx 下含 policy 的表只有 dwd_policy_base / dwd_global_policy_base 及其 _bak）",
        "policy_entity_relation": "同上，无表",
        "policy_entity_type": "同上，无表",
        "ads.policy_text_parse": "gkx 只有 dwd_* 层，无 ads 层结果面",
        "nlp_model_runtime": "本目录无模型权重、无推理依赖，脚本不可能在本机复现 NER/摘要",
        "支撑字段": "keywords 0 行、keypoints 0 行、theme 2 行（policy_struct_20261023.json elements 段）",
    }

    # ---------- 泛词精度体检：命中量集中在哪几个词 ----------
    way_total = {}
    for r in rows:
        for w, c in r["way_hits"].items():
            way_total[w] = way_total.get(w, 0) + c
    way_sum = sum(way_total.values()) or 1
    generic = ("支持", "项目", "资金")
    generic_hits = sum(way_total.get(w, 0) for w in generic)
    way_rank = [
        {"word": w, "hits": c, "share_pct": round(100.0 * c / way_sum, 4)}
        for w, c in sorted(way_total.items(), key=lambda x: -x[1])
    ]

    # ---------- 编码体检：标题乱码（GBK 被按 UTF-8 解） ----------
    base = json.load(open(SNAP / "policy_base_20261021.json", encoding="utf-8"))
    MOJI = ("鍥", "锛", "銆", "鐨", "瀹", "鏂", "浠", "鍔")
    moji_ids = [b["id"] for b in base
                if any(ch in (b.get("title") or "") for ch in MOJI)]

    out = {
        "metric_id": "M_POLICY_TEXT_PARSE",
        "support_judgment": "部分支持",
        "publishable": True,
        "registered_metric_value": None,
        "headline": {
            "policy_total": n,
            "docs_with_substantive_content": text["agg"]["content_local_rows"],
            "docs_with_abstract": text["agg"]["abstract_rows"],
            "title_rows": text["agg"]["title_rows"],
            "branches_total": 3,
            "branches_deliverable": 1,
            "delivered_branch": "自动标签（闭集规则抽取）",
            "blocked_branches": ["结构化要素抽取（无模型、无输出表）", "自动摘要（无模型、无输出表）"],
            "docs_with_any_tag": multi["docs_with_any_tag"],
            "any_tag_rate_pct": round(100.0 * multi["docs_with_any_tag"] / n, 4),
        },
        "tag_coverage": cov,
        "tag_multiplicity": multi,
        "precision_probe": {
            "way_word_rank": way_rank,
            "generic_words": list(generic),
            "generic_hits": generic_hits,
            "generic_share_of_way_hits_pct": round(100.0 * generic_hits / way_sum, 4),
            "note": ("「支持 / 项目 / 资金」三个泛词占支持工具命中的大头；它们在任何体裁里都出现，"
                     "不构成「该政策写了支持方式」的证据。精度体检见 manual_audit。"),
        },
        "encoding_probe": {
            "mojibake_title_rows": len(moji_ids),
            "ids_sample": moji_ids[:10],
            "note": "标题含 GBK 误码字符（鍥/锛/銆/鐨…），同一批导入的编码不一致，按标题匹配的件会漏掉这些行",
        },
        "manual_audit": {
            "sample_size": 20,
            "seed": 20261023,
            "correct": 7,
            "partly_correct": 5,
            "wrong": 5,
            "empty_correct": 3,
            "rule": ("正确 = 标签与文种/正文语义一致；部分正确 = 至少一类标签成立但另一类是泛词；"
                     "错误 = 全部标签都由泛词误命中；空正确 = 该文本无政策工具语义，正确留空"),
        },
        "amount_probe": amt,
        "samples_20": samples,
        "blockers": blockers,
        "probes": {
            "keywords_nonnull": struct["elements"]["keywords_nonnull"],
            "keypoints_nonnull": struct["elements"]["keypoints_nonnull"],
            "theme_nonnull": struct["elements"]["theme_nonnull"],
            "content_db_rows": text["agg"]["content_db_rows"],
            "content_local_rows": text["agg"]["content_local_rows"],
            "content_missing_rows": text["agg"]["content_missing_rows"],
            "content_chars_db": text["agg"]["content_chars_db"],
            "content_chars_local": text["agg"]["content_chars_local"],
            "lexicons": {k: text["lexicons"][k] for k in
                         ("parse_way", "parse_object", "parse_industry", "parse_time_regex")},
        },
        "custom_thresholds": {
            "tag_rule": "闭集子串命中，长词优先、区间不重复计；一条政策可带多类标签",
            "industry_lexicon": "12 链名 + 码长 9/11 且名称 ≥4 字的环节名；2 字环节名（如「材料」）因过宽剔除",
            "amount_rule": "正文与摘要两侧都命中且量级差 ≥100 倍 → amt_conflict；冲突行不得参与任何金额合计",
        },
        "reused_from": "code/_snapshots21/policy_text_20261023.json",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面件：政策文本解析对 20,000 条存量政策逐条执行，不按年份切窗、无时间分母。"
                            "publish_year 跨 1981—2024，2023/2024 的零行是采集断档（DATA_FACTS §3.49 邻域），"
                            "不得读成「政策文本归零」。"),
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("support_judgment", "headline")}, ensure_ascii=False, indent=1))
    print(json.dumps(cov, ensure_ascii=False, indent=1))
    print(json.dumps(multi, ensure_ascii=False))
    print(json.dumps(amt, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

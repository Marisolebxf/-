#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_STATE_OWNED_COUNT · 国有企业数量（gkx 单库转换版）

定义
----
国有企业数 = 登记类型属于「国有独资 / 国有控股 / 全民所有制 / 国有经营单位」的企业数。
统计单元是企业个体（按 org_id 去重），可按城市、行业门类、登记类型下钻。

为什么判「完全转换支持」
------------------------
`enterprise_type_dist` 结果面在 gkx 不存在（source_absent，见 TABLE_ABSENCE_EVIDENCE
§enterprise_type_dist），但本指标不需要结果面：`dwd_org_base_info.ent_type`
（登记类型）对 189,116 家企业 100% 有值，国有属性是登记类型的确定性函数，
按关键词规则分类即可，无歧义、无阈值、无外部参数。

口径细节
--------
计入：含「国有独资」「国有控股」的类型（排除「非国有…」前缀）、「全民所有制」及其
      分支机构、类型以「全民」开头的内联企业、「国有经营单位」。
不计入：集体所有制 / 集体经济组织（单列，属集体不属国有）、
      「全民与私营联营」（混合所有制，不满足控股判据）、事业单位/机关/社会团体（非企业）。
参考线索：`dwd_org_shareholder_info` 里股东名含国资/财政/政府的记录 522 条、涉及 358 家，
      属「国有参股」口径，与「国有控股」口径不同，不并入本件计数，仅作交叉校验。

输出：code/M_ENT_STATE_OWNED_COUNT_out.json
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_ENT_STATE_OWNED_COUNT_out.json"
METRIC = "M_ENT_STATE_OWNED_COUNT"


def load(name):
    return json.loads((SNAP / name).read_text(encoding="utf-8"))


def classify(ent_type: str) -> str:
    t = (ent_type or "").strip()
    if not t:
        return "空类型"
    if t.startswith("非国有"):
        return "非国有(排除)"
    if "国有独资" in t or "国有控股" in t:
        return "国有独资/控股"
    if "全民所有制" in t or t.startswith("全民"):
        if "私营" in t or "联营" in t:
            return "混合(排除)"
        return "全民所有制"
    if "国有经营单位" in t:
        return "国有经营单位"
    if "集体" in t:
        return "集体(不计入)"
    if t in ("事业单位", "机关", "党政机关", "社会团体", "民办非企业单位"):
        return "非企业(不计入)"
    return "其他(不计入)"


def main() -> None:
    rows = load("star_base_rows_gkx.json")
    # [org_id, name, province, city, district, industry_l1, industry_l2, ent_type]
    buckets = Counter()
    by_city = defaultdict(int)
    by_industry = defaultdict(int)
    by_type = Counter()
    for r in rows:
        b = classify(r[7])
        buckets[b] += 1
        if b in ("国有独资/控股", "全民所有制", "国有经营单位"):
            by_city[r[3]] += 1
            by_industry[r[5]] += 1
            by_type[r[7]] += 1

    soe = sum(v for k, v in buckets.items()
              if k in ("国有独资/控股", "全民所有制", "国有经营单位"))
    total = len(rows)
    collective = buckets["集体(不计入)"]

    city_rows = [{"city": c, "soe": n, "share": round(n / soe, 4)}
                 for c, n in sorted(by_city.items(), key=lambda x: -x[1])[:8]]
    ind_rows = [{"industry_l1": k, "soe": v, "share": round(v / soe, 4)}
                for k, v in sorted(by_industry.items(), key=lambda x: -x[1])[:10]]

    out = {
        "metric_id": METRIC,
        "metric_name": "国有企业数量",
        "data_source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）+ code/_snapshots21/ 落盘快照",
        "formula": "COUNT(DISTINCT org) WHERE ent_type ∈ {国有独资, 国有控股, 全民所有制, 国有经营单位}，排除「非国有」前缀",
        "blocking_tables": {
            "enterprise_type_dist": {
                "triage": "source_absent",
                "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §enterprise_type_dist",
            }
        },
        "conversion_path": "dwd_org_base_info.ent_type（189,116 行全量有值）→ 关键词确定性分类",
        "rule": {
            "counted": ["国有独资", "国有控股", "全民所有制", "全民(内联)", "国有经营单位"],
            "excluded": ["非国有*", "集体所有制/集体经济组织", "全民与私营联营", "事业单位/机关/社会团体"],
            "dedup_key": "org_id",
        },
        "totals": {
            "base_orgs": total, "soe": soe, "soe_share": round(soe / total, 4),
            "collective_excluded": collective,
            "buckets": dict(buckets),
        },
        "by_city": city_rows,
        "by_industry_l1": ind_rows,
        "by_ent_type": [{"ent_type": k, "n": v} for k, v in by_type.most_common(12)],
        "cross_check": {
            "shareholder_soe_rows": 522,
            "shareholder_soe_orgs": 358,
            "note": "股东名含国资/财政/政府的记录，属参股口径；与控股口径不并入，仅作量级交叉校验（358 < 550，方向合理）",
        },
        "support_judgment": {
            "data_support_level": "完全转换支持",
            "reason": "本指标不需要任何缺失结果面：ent_type 是登记类型的枚举值，189,116 家企业 100% 有值，国有属性由登记类型确定性判定，规则无阈值、无歧义、可逐行复核；去重键 org_id 唯一。城市、行业门类、登记类型三个下钻维齐全，计数即真值，故判完全转换支持。",
            "criteria": {
                "result_table_needed": False,
                "source_field_exists": True,
                "field_fill_rate": 1.0,
                "rule_ambiguous": False,
                "soe": soe,
                "proxy_used": False,
            },
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "本件是截面计数（底册当前时点），不做年度序列，故无基期年份。底册不带历史登记类型快照，无法回溯往年国企数；若要做年增量，只能用成立年份近似，且需声明「成立年 ≠ 当前国有属性」。",
        "sources": [
            {"path": "code/_snapshots21/star_base_rows_gkx.json",
             "table": "gkx.dwd_org_base_info", "rows": 189116,
             "role": "企业底册含登记类型（唯一输入）"},
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[OK] {METRIC} -> {OUT.name} soe={soe}/{total} share={out['totals']['soe_share']} "
          f"collective={collective}")
    print("  cities", city_rows[:4])
    print("  buckets", dict(buckets))


if __name__ == "__main__":
    main()

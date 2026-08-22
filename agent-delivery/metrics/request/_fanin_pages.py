# -*- coding: utf-8 -*-
"""Merge TOPIC-ALGO-GAP-L01 page yamls into 15-col items + csv."""
from __future__ import annotations

import csv
import os
from collections import Counter, defaultdict

import yaml

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGE_DIR = os.path.join(ROOT, "专题系统", "pages")
OUT_DIR = os.path.join(ROOT, "专题系统")

PAGE_ORDER = [
    "CHAIN-TOPIC-PANORAMA",
    "CHAIN-TOPIC-DIAGNOSIS",
    "CHAIN-TOPIC-REGIONAL",
    "CHAIN-TOPIC-SHENZHEN",
    "SVCCHAIN-ORG-ANALYSIS",
    "SVCCHAIN-ECOSYSTEM",
    "SVCCHAIN-RECOMMEND",
    "SVCCHAIN-PORTAL",
    "E7-POLICY",
    "SYNTH-REGION",
    "SYNTH-VITALITY",
    "SYNTH-ELEMENT",
    "SYNTH-COLLAB",
    "TOPIC-ENT-05",
    "TOPIC-TECH-05",
    "TOPIC-ORG-05",
    "TOPIC-TALENT-05",
    "TOPIC-QUERY",
    "TOPIC-OPS",
    "TOPIC-DATAREQ",
]

MODULE_BY_PAGE = {
    "CHAIN-TOPIC-PANORAMA": ("产业链分析", "产业链全景图谱"),
    "CHAIN-TOPIC-DIAGNOSIS": ("产业链分析", "产业运行诊断"),
    "CHAIN-TOPIC-REGIONAL": ("产业链分析", "区域产业评价"),
    "CHAIN-TOPIC-SHENZHEN": ("产业链分析", "深圳产业决策"),
    "SVCCHAIN-ORG-ANALYSIS": ("产业服务链分析", "服务机构分析"),
    "SVCCHAIN-ECOSYSTEM": ("产业服务链分析", "服务链生态"),
    "SVCCHAIN-RECOMMEND": ("产业服务链分析", "机构招引培育"),
    "SVCCHAIN-PORTAL": ("产业服务链分析", "专题服务门户"),
    "E7-POLICY": ("政策分析", "政策分析"),
    "SYNTH-REGION": ("综合智能分析", "区域创新分析"),
    "SYNTH-VITALITY": ("综合智能分析", "区域创新活力分析"),
    "SYNTH-ELEMENT": ("综合智能分析", "区域创新要素分析"),
    "SYNTH-COLLAB": ("综合智能分析", "区域创新协同分析"),
    "TOPIC-ENT-05": ("企业分析", "专题企业分析"),
    "TOPIC-TECH-05": ("技术链分析", "专题技术链分析"),
    "TOPIC-ORG-05": ("科研机构分析", "专题科研机构分析"),
    "TOPIC-TALENT-05": ("人才分析", "专题人才分析"),
    "TOPIC-QUERY": ("科技专题数据查询", "科技专题数据查询"),
    "TOPIC-OPS": ("运营管理", "运营四级汇总"),
    "TOPIC-DATAREQ": ("数据需求", "数据需求"),
}

COLS = [
    "模块",
    "页面",
    "主项",
    "子项",
    "指标含义",
    "建议取值/取值口径",
    "取值依据类型",
    "调用系统",
    "调用模块",
    "取数依据",
    "差集判定",
    "A1需规ID",
    "A1指标叶ID",
    "metric_id",
    "缺口说明",
]


def _s(v):
    if v is None:
        return None
    if isinstance(v, str):
        t = v.strip()
        return t if t else None
    return v


def demand_to_item(page_id, dem, idx):
    mod, page = MODULE_BY_PAGE[page_id]
    name = dem.get("metric_name_zh") or dem.get("主项") or dem.get("demand_id")
    gap = dem.get("缺口说明")
    verdict = dem.get("差集判定")
    call_sys = "科技专题服务系统"
    if verdict == "mapped":
        call_sys = "深度挖掘算法"
    elif verdict == "third_party":
        call_sys = "深度挖掘算法"
    elif verdict == "other_system":
        call_sys = "基础数据"
    elif verdict == "n/a_ops":
        call_sys = "科技专题服务系统"
    return {
        "row_id": dem.get("demand_id") or f"{page_id}-{idx:03d}",
        "page_id": page_id,
        "模块": mod,
        "页面": page,
        "主项": name,
        "子项": None,
        "指标含义": name,
        "建议取值/取值口径": _s(gap) or verdict,
        "取值依据类型": "根据原文归纳",
        "调用系统": call_sys,
        "调用模块": None,
        "取数依据": _s(gap),
        "差集判定": verdict,
        "A1需规ID": dem.get("A1需规ID"),
        "A1指标叶ID": dem.get("A1指标叶ID"),
        "metric_id": dem.get("metric_id"),
        "缺口说明": _s(gap),
    }


def normalize_item(page_id, raw, idx):
    mod, page = MODULE_BY_PAGE[page_id]
    item = {k: raw.get(k) for k in COLS}
    item["row_id"] = raw.get("row_id") or raw.get("demand_id") or f"{page_id}-{idx:03d}"
    item["page_id"] = page_id
    item["模块"] = item["模块"] or mod
    item["页面"] = item["页面"] or page
    return item


def main():
    all_items = []
    page_stats = []
    debt_n = 0
    for pid in PAGE_ORDER:
        path = os.path.join(PAGE_DIR, pid + ".yaml")
        with open(path, encoding="utf-8") as f:
            doc = yaml.safe_load(f)
        items = [x for x in (doc.get("items") or []) if isinstance(x, dict)]
        demands = [x for x in (doc.get("demands") or []) if isinstance(x, dict)]
        debts = doc.get("semantic_debt") or []
        debt_n += len(debts)
        src = items if items else [demand_to_item(pid, d, i + 1) for i, d in enumerate(demands)]
        norm = [normalize_item(pid, x, i + 1) for i, x in enumerate(src)]
        vc = Counter(x.get("差集判定") for x in norm)
        page_stats.append(
            {
                "page_id": pid,
                "wave": doc.get("wave"),
                "n": len(norm),
                "verdicts": dict(vc),
                "semantic_debt": len(debts),
            }
        )
        all_items.extend(norm)

    vc_all = Counter(x.get("差集判定") for x in all_items)
    missing = [x for x in all_items if x.get("差集判定") == "missing"]

    out_yaml = {
        "version": 1,
        "task": "TOPIC-ALGO-GAP-L01",
        "system": "topic",
        "updated": "2026-08-22",
        "source_excel_ref": None,
        "page_count": len(PAGE_ORDER),
        "item_count": len(all_items),
        "verdicts": dict(vc_all),
        "missing_count": len(missing),
        "semantic_debt_count": debt_n,
        "a1_tables_ready": False,
        "pages": page_stats,
        "missing": [
            {
                "row_id": x["row_id"],
                "page_id": x["page_id"],
                "模块": x["模块"],
                "页面": x["页面"],
                "主项": x["主项"],
                "metric_id": x.get("metric_id"),
                "缺口说明": x.get("缺口说明"),
            }
            for x in missing
        ],
        "items": all_items,
    }
    ypath = os.path.join(OUT_DIR, "TOPIC-ALGO-GAP-L01.yaml")
    with open(ypath, "w", encoding="utf-8") as f:
        yaml.safe_dump(out_yaml, f, allow_unicode=True, sort_keys=False, width=120)
    csv_path = os.path.join(OUT_DIR, "_fanin.csv")
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["row_id", "page_id"] + COLS, extrasaction="ignore")
        w.writeheader()
        for row in all_items:
            w.writerow({k: ("" if row.get(k) is None else row.get(k)) for k in ["row_id", "page_id"] + COLS})
    miss_csv = os.path.join(OUT_DIR, "_fanin_missing.csv")
    with open(miss_csv, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["row_id", "page_id"] + COLS, extrasaction="ignore")
        w.writeheader()
        for row in missing:
            w.writerow({k: ("" if row.get(k) is None else row.get(k)) for k in ["row_id", "page_id"] + COLS})
    print("items", len(all_items))
    print("verdicts", dict(vc_all))
    print("missing", len(missing))
    print("debt", debt_n)
    for m in missing:
        print("MISSING", m["page_id"], m.get("metric_id"), m["主项"])


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 2-概要设计/2-1需求分析 功能点 CSV 生成 acceptance-catalog YAML。
验收真源：需求分析目录，不读取招标 PDF。

用法:
  python extract_feature_catalog.py
"""
from __future__ import annotations

import csv
import sys
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

SCRIPT_DIR = Path(__file__).resolve().parent
AGENT_DELIVERY = SCRIPT_DIR.parent
CODE_ROOT = AGENT_DELIVERY.parent

REQ_CSV_DIR = Path(
    r"e:/实施/2025/智谱-深圳国科信/2-概要设计/2-1需求分析/需求调研和澄清/csv"
)
OUT_DIR = AGENT_DELIVERY / "acceptance-catalog"

# 展示系统 7 模块（主验收清单）
DISPLAY_CSV = "08-功能点台账-展示系统7模块.csv"
DISPLAY_JUDGE_CSV = "10-功能点台账-展示系统7模块-要求分析与判断.csv"

# 四要素 / 专题（扩展验收）
TOPIC_CSVS = [
    ("catalog-topic-industry.yaml", "11-功能点台账-产业链相关-要求分析与判断.csv", "IND"),
    ("catalog-topic-enterprise.yaml", "12-功能点台账-企业相关-要求分析与判断.csv", "ENT"),
    ("catalog-topic-org.yaml", "13-功能点台账-科研机构相关-要求分析与判断.csv", "ORG"),
    ("catalog-topic-policy.yaml", "14-功能点台账-政策相关-要求分析与判断.csv", "POL"),
]


def load_judgments(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    out: dict[str, dict] = {}
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            fid = (row.get("条目ID") or "").strip()
            if fid:
                out[fid] = {
                    "judgment": (row.get("要求判断") or "").strip(),
                    "analysis": (row.get("要求分析") or row.get("功能描述摘要") or "").strip(),
                }
    return out


def read_csv_rows(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def default_tier(module: str, judgment: str) -> str:
    j = judgment or ""
    if j in ("删除", "REMOVED"):
        return "DEMO"
    if "人才" in module or "成果" in module or "服务全景" in module or "数据资源" in module:
        return "INTEG"
    return "TBD"


def build_display_catalog() -> dict:
    base = REQ_CSV_DIR / DISPLAY_CSV
    judge = load_judgments(REQ_CSV_DIR / DISPLAY_JUDGE_CSV)
    rows = read_csv_rows(base)
    entries = []
    for r in rows:
        fid = (r.get("条目ID") or "").strip()
        if not fid:
            continue
        module = (r.get("展示系统模块") or "").strip()
        sub = (r.get("子功能/专题") or "").strip()
        scope = (r.get("功能范围（招标技术要求/文档描述摘要）") or r.get("功能描述摘要") or "").strip()
        deps = (r.get("主要依赖维度（数据要素）") or "").strip()
        j = judge.get(fid, {})
        entries.append({
            "id": fid,
            "source": "req-analysis-display",
            "module": module,
            "title": sub,
            "scope_summary": scope,
            "dependencies": deps,
            "judgment": j.get("judgment") or None,
            "analysis": j.get("analysis") or None,
            "tier": default_tier(module, j.get("judgment", "")),
            "route": None,
            "task_id": None,
            "demo_id": None,
        })
    leaves = len(entries)
    return {
        "version": 1,
        "source": "req-analysis-display",
        "authority": "2-概要设计/2-1需求分析/需求调研和澄清/csv/08-功能点台账-展示系统7模块.csv",
        "supplement": "2-概要设计/2-1需求分析/需求调研和澄清/csv/10-功能点台账-展示系统7模块-要求分析与判断.csv",
        "extracted_at": str(date.today()),
        "stats": {"entries_total": len(entries), "leaf_total": leaves},
        "entries": entries,
    }


def build_topic_catalog(filename: str, csv_name: str, prefix: str) -> dict:
    path = REQ_CSV_DIR / csv_name
    rows = read_csv_rows(path)
    entries = []
    for r in rows:
        fid = (r.get("条目ID") or "").strip()
        if not fid:
            continue
        # 不同 CSV 列名略有差异
        title = (
            r.get("子功能/专题")
            or r.get("功能点/专题")
            or r.get("功能点")
            or r.get("专题/功能")
            or ""
        ).strip()
        module = (r.get("所属模块") or r.get("专题模块") or r.get("要素") or prefix).strip()
        scope = (
            r.get("功能描述摘要")
            or r.get("功能范围")
            or r.get("功能描述")
            or ""
        ).strip()
        judgment = (r.get("要求判断") or "").strip()
        entries.append({
            "id": fid,
            "source": f"req-analysis-{prefix.lower()}",
            "module": module,
            "title": title,
            "scope_summary": scope,
            "judgment": judgment or None,
            "tier": default_tier(module, judgment),
            "route": None,
            "task_id": None,
            "demo_id": None,
        })
    return {
        "version": 1,
        "source": f"req-analysis-{prefix.lower()}",
        "authority": f"2-概要设计/2-1需求分析/需求调研和澄清/csv/{csv_name}",
        "extracted_at": str(date.today()),
        "stats": {"entries_total": len(entries), "leaf_total": len(entries)},
        "entries": entries,
    }


def write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if yaml:
        with path.open("w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
    else:
        import json
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def main() -> int:
    if not REQ_CSV_DIR.exists():
        print(f"CSV 目录不存在: {REQ_CSV_DIR}", file=sys.stderr)
        return 1

    results = []

    display = build_display_catalog()
    out_display = OUT_DIR / "catalog-display-7modules.yaml"
    write_yaml(out_display, display)
    results.append({"source": "req-analysis-display", "entries": display["stats"]["entries_total"], "out": str(out_display)})
    print(f"OK display: {display['stats']['entries_total']} entries -> {out_display}")

    topic_total = 0
    for out_name, csv_name, prefix in TOPIC_CSVS:
        cat = build_topic_catalog(out_name, csv_name, prefix)
        out_path = OUT_DIR / out_name
        write_yaml(out_path, cat)
        n = cat["stats"]["entries_total"]
        topic_total += n
        results.append({"source": cat["source"], "entries": n, "out": str(out_path)})
        print(f"OK {prefix}: {n} entries -> {out_path}")

    index = {
        "version": 2,
        "authority": "2-概要设计/2-1需求分析",
        "policy": "agent-delivery/acceptance-compliance-policy.md",
        "extract_script": "agent-delivery/scripts/extract_feature_catalog.py",
        "deprecated": ["scripts/extract_acceptance_catalog.py", "catalog-service-cluster.yaml", "catalog-cognitive-brain.yaml"],
        "sources": results,
        "totals": {
            "display_entries": display["stats"]["entries_total"],
            "topic_entries": topic_total,
            "all_entries": display["stats"]["entries_total"] + topic_total,
        },
        "coverage": {
            "rule": "每个功能点条目须有 tier!=TBD 且 route 非空（验收前）",
            "current_tier_assigned": sum(1 for e in display["entries"] if e["tier"] != "TBD"),
            "current_route_assigned": 0,
        },
    }
    index_path = OUT_DIR / "catalog-index.yaml"
    write_yaml(index_path, index)
    print(f"Index -> {index_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

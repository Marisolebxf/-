#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【已废弃】从招标 PDF 提取目录 — 验收已改为 2-1需求分析 CSV。
请使用 extract_feature_catalog.py。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    print("需要 pypdf: pip install pypdf", file=sys.stderr)
    sys.exit(1)

try:
    import yaml
except ImportError:
    yaml = None

# 项目根：agent-delivery/scripts -> agent-delivery -> gkx_src (code_root)
# 招标 PDF 在 docs_root（paths.yaml）
SCRIPT_DIR = Path(__file__).resolve().parent
AGENT_DELIVERY = SCRIPT_DIR.parent
CODE_ROOT = AGENT_DELIVERY.parent

def _load_paths() -> dict:
    paths_file = AGENT_DELIVERY / "paths.yaml"
    if paths_file.exists() and yaml:
        with paths_file.open(encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        docs = Path(data.get("docs_root", CODE_ROOT.parent))
        return {"docs_root": docs, "code_root": Path(data.get("code_root", CODE_ROOT))}
    return {"docs_root": Path(r"e:\实施\2025\智谱-深圳国科信"), "code_root": CODE_ROOT}

_PATHS = _load_paths()
PROJECT_ROOT = _PATHS["docs_root"]

DEFAULT_PDFS = [
    {
        "id": "bid-service-cluster",
        "title": "五、实施方案-智能服务集群",
        "path": PROJECT_ROOT / "1-招投标需求" / "五、实施方案-智能服务集群-ZP-2025-11-18.pdf",
        "out": AGENT_DELIVERY / "acceptance-catalog" / "catalog-service-cluster.yaml",
        "prefix": "SC",
    },
    {
        "id": "bid-cognitive-brain",
        "title": "五、实施方案-智慧认知大脑",
        "path": PROJECT_ROOT / "1-招投标需求" / "五、实施方案-智慧认知大脑-ZP-2025-11-18.pdf",
        "out": AGENT_DELIVERY / "acceptance-catalog" / "catalog-cognitive-brain.yaml",
        "prefix": "CB",
    },
]

# 编号 + 标题（至少 2 级编号，标题 2~120 字）
HEADING_RE = re.compile(
    r"^(\d+(?:\.\d+){1,})\s+(.{2,120}?)\s*$"
)

# 过滤明显非菜单的噪声行
NOISE_KEYWORDS = (
    "图 ", "表 ", "单位：", "备注：", "说明：", "如下", "截图", "采购人",
    "最终界面", "页码", ".....",
)


def is_noise(title: str) -> bool:
    t = title.strip()
    if len(t) < 2:
        return True
    if any(k in t for k in NOISE_KEYWORDS):
        return True
    # 纯数字或纯标点
    if re.fullmatch(r"[\d\.\s\-—]+", t):
        return True
    return False


def depth(number: str) -> int:
    return number.count(".") + 1


def is_leaf(number: str, all_numbers: set[str]) -> bool:
    """叶子：不存在以 number. 开头的更长编号"""
    prefix = number + "."
    return not any(n.startswith(prefix) for n in all_numbers if n != number)


def extract_headings(pdf_path: Path) -> list[dict]:
    reader = PdfReader(str(pdf_path))
    seen: set[tuple[str, str]] = set()
    rows: list[dict] = []

    for page_idx, page in enumerate(reader.pages):
        try:
            text = page.extract_text() or ""
        except Exception:
            continue
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            m = HEADING_RE.match(line)
            if not m:
                continue
            num, title = m.group(1), m.group(2).strip()
            # 去掉标题尾页码等
            title = re.sub(r"\s+\d+\s*$", "", title).strip()
            if is_noise(title):
                continue
            key = (num, title)
            if key in seen:
                continue
            seen.add(key)
            rows.append({
                "number": num,
                "title": title,
                "page": page_idx + 1,
                "depth": depth(num),
            })

    rows.sort(key=lambda r: [int(x) for x in r["number"].split(".")])
    all_nums = {r["number"] for r in rows}
    for r in rows:
        r["is_leaf"] = is_leaf(r["number"], all_nums)
    return rows


def build_catalog_entries(rows: list[dict], source_id: str, prefix: str) -> list[dict]:
    entries = []
    for i, r in enumerate(rows):
        eid = f"{prefix}-{r['number'].replace('.', '-')}"
        entry = {
            "id": eid,
            "pdf_source": source_id,
            "number": r["number"],
            "title": r["title"],
            "page": r["page"],
            "depth": r["depth"],
            "is_leaf": r["is_leaf"],
            "tier": "TBD",  # FULL | INTEG | DEMO — 人工/Coordinator 标注
            "route": None,
            "task_id": None,
            "demo_id": None,
        }
        entries.append(entry)
    return entries


def write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if yaml:
        with path.open("w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
    else:
        # 最小 YAML 手写（仅 index）
        import json
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def process_one(spec: dict) -> dict:
    pdf_path = Path(spec["path"])
    if not pdf_path.exists():
        raise FileNotFoundError(pdf_path)

    rows = extract_headings(pdf_path)
    entries = build_catalog_entries(rows, spec["id"], spec["prefix"])
    leaves = [e for e in entries if e["is_leaf"]]

    catalog = {
        "version": 1,
        "pdf_source": spec["id"],
        "pdf_title": spec["title"],
        "pdf_path": str(pdf_path).replace("\\", "/"),
        "extracted_at": "2026-06-16",
        "stats": {
            "headings_total": len(entries),
            "leaf_total": len(leaves),
            "max_depth": max((e["depth"] for e in entries), default=0),
        },
        "entries": entries,
    }

    out_path = Path(spec["out"])
    write_yaml(out_path, catalog)
    print(f"OK {spec['id']}: headings={len(entries)} leaves={len(leaves)} -> {out_path}")
    return {
        "source": spec["id"],
        "headings": len(entries),
        "leaves": len(leaves),
        "out": str(out_path),
    }


def write_index(results: list[dict]) -> None:
    index_path = AGENT_DELIVERY / "acceptance-catalog" / "catalog-index.yaml"
    index = {
        "version": 1,
        "policy": "agent-delivery/acceptance-compliance-policy.md",
        "demo_registry": "agent-delivery/demo-fallback-registry.yaml",
        "extract_script": "agent-delivery/scripts/extract_acceptance_catalog.py",
        "sources": results,
        "totals": {
            "headings": sum(r["headings"] for r in results),
            "leaves": sum(r["leaves"] for r in results),
        },
        "coverage": {
            "rule": "每个 is_leaf=true 的条目须有 tier!=TBD 且 route 非空（验收前）",
            "current_tier_assigned": 0,
            "current_route_assigned": 0,
        },
    }
    write_yaml(index_path, index)
    print(f"Index -> {index_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", type=Path, help="单个 PDF")
    parser.add_argument("--source-id", default="custom")
    parser.add_argument("--out", type=Path, help="输出 yaml")
    parser.add_argument("--prefix", default="X")
    args = parser.parse_args()

    if args.pdf:
        spec = {
            "id": args.source_id,
            "title": args.source_id,
            "path": args.pdf,
            "out": args.out or AGENT_DELIVERY / "acceptance-catalog" / "catalog-custom.yaml",
            "prefix": args.prefix,
        }
        write_index([process_one(spec)])
    else:
        results = [process_one(s) for s in DEFAULT_PDFS]
        write_index(results)


if __name__ == "__main__":
    main()

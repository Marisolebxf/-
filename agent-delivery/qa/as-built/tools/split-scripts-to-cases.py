#!/usr/bin/env python3
"""将功能目录 gold.yaml + scripts.yaml 拆成 index.yaml + cases/{id}.yaml，并删除旧双文件。

用法：
  python3 split-scripts-to-cases.py <功能目录> [<功能目录>...]
  python3 split-scripts-to-cases.py --all   # 扫 KJZTFWXT 下全部 scripts.yaml

2026-10-14 已对 KJZTFWXT 25 入口全量执行；runner 仅认 cases-v1。本工具保留供漏网/回滚重拆。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

# 长 assert 用字面块，便于单文件 diff
class LiteralStr(str):
    pass


def _literal_representer(dumper, data):
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")


yaml.add_representer(LiteralStr, _literal_representer)


def _walk_literal(obj):
    if isinstance(obj, dict):
        return {k: _walk_literal(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_walk_literal(v) for v in obj]
    if isinstance(obj, str) and ("\n" in obj or len(obj) > 120):
        return LiteralStr(obj)
    return obj


def natural_key(s: str):
    return [int(x) if x.isdigit() else x.lower() for x in re.split(r"(\d+)", s)]


def load_merged(feat: Path):
    gold_path = feat / "gold.yaml"
    scripts_path = feat / "scripts.yaml"
    if not scripts_path.exists():
        raise FileNotFoundError(f"无 scripts.yaml: {feat}")
    gold_ids = []
    merged = []
    if gold_path.exists():
        gdoc = yaml.safe_load(gold_path.read_text(encoding="utf-8")) or {}
        gscripts = gdoc.get("scripts") or []
        gold_ids = [s["id"] for s in gscripts if s and s.get("id")]
        merged.extend(gscripts)
    sdoc = yaml.safe_load(scripts_path.read_text(encoding="utf-8")) or {}
    for inc in sdoc.get("includes") or []:
        # 已从 gold 展开则跳过重复 include
        if Path(inc).name == "gold.yaml" and gold_ids:
            continue
        p = feat / inc
        if not p.exists():
            raise FileNotFoundError(f"include 不存在: {p}")
        idoc = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        merged.extend(idoc.get("scripts") or [])
    merged.extend(sdoc.get("scripts") or [])
    seen = set()
    out = []
    for s in merged:
        if not s or not s.get("id"):
            continue
        if s["id"] in seen:
            continue
        seen.add(s["id"])
        out.append(s)
    if not gold_ids:
        # 无独立 gold 时：取前 5 条或带 tier A/gold 的
        gold_ids = [
            s["id"]
            for s in out
            if str(s.get("tier", "")).upper() in ("A", "GOLD")
        ][:5]
        if not gold_ids:
            gold_ids = [s["id"] for s in out[:5]]
    return gold_ids, out


def split_one(feat: Path, *, dry_run: bool = False) -> tuple[int, list[str]]:
    gold_ids, scripts = load_merged(feat)
    cases_dir = feat / "cases"
    if not dry_run:
        cases_dir.mkdir(exist_ok=True)
    for s in scripts:
        sid = s["id"]
        # 金样标 tier A，其余若无 tier 标 B
        if sid in gold_ids and not s.get("tier"):
            s = {**s, "tier": "A"}
        elif not s.get("tier"):
            s = {**s, "tier": "B"}
        body = _walk_literal(s)
        text = yaml.dump(
            body,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            width=120,
        )
        if not dry_run:
            (cases_dir / f"{sid}.yaml").write_text(text, encoding="utf-8")
    # 全量顺序：金样在前，其余自然序
    rest = sorted((s["id"] for s in scripts if s["id"] not in gold_ids), key=natural_key)
    all_ids = list(gold_ids) + rest
    index = {
        "layout": "cases-v1",
        "gold": gold_ids,
        "all": all_ids,
    }
    index_text = (
        "# as-built 索引 · 一用例一文件（cases-v1）\n"
        "# gold = A 档机跑顺序；all = 全量顺序（金样在前）\n"
        + yaml.dump(index, allow_unicode=True, default_flow_style=False, sort_keys=False)
    )
    if not dry_run:
        (feat / "index.yaml").write_text(index_text, encoding="utf-8")
        for name in ("gold.yaml", "scripts.yaml"):
            p = feat / name
            if p.exists():
                p.unlink()
    return len(scripts), gold_ids


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dirs", nargs="*", type=Path)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[1] / "scripts" / "KJZTFWXT"
    feats = list(args.dirs)
    if args.all:
        feats = sorted({p.parent for p in root.rglob("scripts.yaml")})
    if not feats:
        ap.error("给出功能目录或 --all")
    total = 0
    for feat in feats:
        feat = feat.resolve()
        n, gold = split_one(feat, dry_run=args.dry_run)
        total += n
        print(f"{'[dry] ' if args.dry_run else ''}OK {feat.relative_to(root.parent) if root.parent in feat.parents else feat}  cases={n} gold={gold}")
    print(f"done modules={len(feats)} cases={total}")


if __name__ == "__main__":
    main()

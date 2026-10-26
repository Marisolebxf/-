#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""merge_calc_logic_source.py —— 把 local-workspace 正本 MD 全文并入 calc-logic MD（GitLab 自包含化）。

背景（2026-10-24 淮政玮反馈）：calc-logic MD 只含结构化摘要，详细计算过程以
`local-workspace/...` 路径指针存在，而 local-workspace 不同步 GitLab，验收方看不到。

本脚本对每份 calc-logic/{域}/{ID}.md：
  1. 找到 local-workspace/.../第三方库指标计算过程/{ID}.md 正本；
  2. 正本全文（去 H1 标题）作为 `# 详细计算过程（正本全文并入）` 节插入 calc-logic MD；
  3. 头部指针行追加「正本全文已并入本件；local-workspace 路径仅为本地备份（GitLab 不可见）」。

幂等：已含「正本全文并入」标记的文件跳过（--force 可重并）。
用法：python3 scripts/merge_calc_logic_source.py [--only ID] [--dry-run] [--force]
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ORCH_ROOT = Path(__file__).resolve().parent.parent
CALC_DIR = ORCH_ROOT / "agent-delivery" / "metrics" / "calc-logic"
SRC_DIR = (
    ORCH_ROOT.parent
    / "local-workspace"
    / "docs"
    / "tasks"
    / "investiage"
    / "20261021_指标整体开发进度调研"
    / "第三方库指标计算过程"
)
MARK = "正本全文并入"
HEADER_NOTE = "（**正本全文已并入本件下方「详细计算过程」节**；`local-workspace/` 路径仅为本地备份指针，GitLab 不可见）"


def find_source(md_id: str) -> Path | None:
    p = SRC_DIR / f"{md_id}.md"
    return p if p.is_file() else None


def strip_h1(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    # 去掉开头连续空行
    while lines and not lines[0].strip():
        lines = lines[1:]
    return "\n".join(lines).rstrip() + "\n"


def merge_file(cl_path: Path, src_path: Path, force: bool, dry: bool) -> str:
    text = cl_path.read_text(encoding="utf-8")
    if MARK in text and not force:
        return "skip"
    src_body = strip_h1(src_path.read_text(encoding="utf-8"))
    section = f"\n---\n\n# 详细计算过程（{MARK} · 2026-10-24，源：local-workspace 20261021 调研正本）\n\n{src_body}"

    # 1) 头部指针行补自包含说明（只改首处引用正本路径的 blockquote/正文行）
    if MARK not in text:
        m = re.search(r"^(>?.*学术级调研正本.*local-workspace.*\S.*)$", text, re.M)
        if not m:
            m = re.search(r"^(\| 正本 MD \|.*)$", text, re.M)
        if m:
            line = m.group(1)
            text = text.replace(line, line + HEADER_NOTE, 1)

    # 2) 插入详细计算过程节：优先放在「## 更新记录」之前，否则追加文末
    ins = f"\n{section}\n"
    m_rec = re.search(r"^## 更新记录\s*$", text, re.M)
    if m_rec:
        text = text[: m_rec.start()] + section.lstrip("\n") + "\n\n" + text[m_rec.start():]
    else:
        text = text.rstrip() + ins

    if not dry:
        cl_path.write_text(text, encoding="utf-8")
    return "merged"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="仅处理指定指标 ID")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    targets = sorted(CALC_DIR.rglob("*.md"))
    stats = {"merged": 0, "skip": 0, "no_source": 0}
    missing = []
    for cl in targets:
        md_id = cl.stem
        if md_id == "README" or (args.only and md_id != args.only):
            continue
        src = find_source(md_id)
        if src is None:
            stats["no_source"] += 1
            missing.append(md_id)
            continue
        stats[merge_file(cl, src, args.force, args.dry_run)] += 1

    print(f"merged={stats['merged']} skip={stats['skip']} no_source={stats['no_source']}")
    if missing:
        print("no_source IDs:", ", ".join(missing[:20]), "..." if len(missing) > 20 else "")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Health-scan as-built cases/*.yaml for half-written / broken scripts.

Complements gap-func-vs-scripts.py (which only finds missing func_id).

Usage (gkx-orchestration root):
  python3 agent-delivery/qa/as-built/tools/health-cases.py --system KJZTFWXT --write
"""
from __future__ import annotations

import argparse
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
QA = ROOT / "qa"
AS_BUILT = QA / "as-built"
SCRIPTS = AS_BUILT / "scripts"

# reuse map from gap tool
from importlib.util import module_from_spec, spec_from_file_location

_gap_path = Path(__file__).with_name("gap-func-vs-scripts.py")
_spec = spec_from_file_location("gap_func_vs_scripts", _gap_path)
_gap = module_from_spec(_spec)
assert _spec.loader
_spec.loader.exec_module(_gap)

FUNC_ID_LINE = re.compile(r"^func_id:\s*(\S+)", re.M)
ID_LINE = re.compile(r"^id:\s*(\S+)", re.M)
TIER_LINE = re.compile(r"^tier:\s*(\S+)", re.M)
ALLOW_SKIP = re.compile(r"^allow_skip:\s*true\b", re.M | re.I)
# top-level WIP only (avoid assert 文案里的「未完成」)
WIP_TOP = re.compile(
    r"^(?:#\s*)?(?:WIP|FIXME|TODO|incomplete|draft)\b|^(?:incomplete|wip):\s*true\b",
    re.M | re.I,
)


def parse_index_list(text: str, key: str) -> list[str]:
    m = re.search(rf"^{key}:\s*\n", text, re.M)
    if not m:
        return []
    items: list[str] = []
    for line in text[m.end() :].splitlines():
        if re.match(r"^[a-zA-Z_][\w-]*:", line):
            break
        if re.match(r"^[ \t]*#", line) or not line.strip():
            continue
        mm = re.match(r"^[ \t]*-[ \t]+(\S+)", line)
        if mm:
            items.append(mm.group(1))
        elif not line.startswith((" ", "\t")):
            break
    return items


def check_case_file(path: Path) -> list[str]:
    reasons: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        return [f"READ_FAIL:{e}"]

    if len(text.strip()) < 120:
        reasons.append("TOO_SHORT")
    if not ID_LINE.search(text):
        reasons.append("NO_ID")
    if not FUNC_ID_LINE.search(text):
        reasons.append("NO_FUNC_ID")
    if not re.search(r"^expect:\s*$", text, re.M) and not re.search(
        r"^expect:\s*\[", text, re.M
    ):
        reasons.append("NO_EXPECT")
    else:
        # 截取 expect 块（到下一个顶层键）；兼容 0 缩进与 2 空格 list
        em = re.search(
            r"^expect:\s*\n([\s\S]*?)(?=^[a-zA-Z_#]|\Z)", text, re.M
        )
        block = em.group(1) if em else ""
        if re.search(r"^expect:\s*\[\s*\]\s*$", text, re.M) or (
            block.strip() == "" or block.strip() == "[]"
        ):
            reasons.append("EXPECT_EMPTY")
        else:
            has_note = bool(re.search(r"^[ \t]*-\s+note:\s*\S", block, re.M))
            has_assert = bool(re.search(r"^[ \t]*assert:\s*\S", block, re.M))
            # 存量裸字符串：仅 list 项为引号串、无 note/assert 键
            bare_only = bool(
                re.search(r"^[ \t]*-\s+[\"']", block, re.M)
            ) and not has_note
            if not has_note and not bare_only:
                reasons.append("EXPECT_NO_NOTE")
            elif has_note and not has_assert:
                reasons.append("EXPECT_NOTE_NO_ASSERT")
            # bare_only = 存量白名单，不进 REWORK（改动该文件时再转双层）
    if re.search(r"^[ \t]*assert:\s*[\"']?\s*[\"']?\s*$", text, re.M):
        reasons.append("EMPTY_ASSERT")
    if ALLOW_SKIP.search(text):
        tm = TIER_LINE.search(text)
        if tm and tm.group(1).upper() == "A":
            reasons.append("A_SKIP")
    if WIP_TOP.search(text):
        reasons.append("WIP_MARK")
    # truncated quote at EOF (common interrupt artifact)
    stripped = text.rstrip()
    if stripped.endswith(("assert: \"", "assert: '", 'assert: "await', "note: \"")):
        reasons.append("TRUNCATED_EOF")
    # unclosed triple / odd count of \" at end of last non-empty line
    last = stripped.splitlines()[-1] if stripped else ""
    if last.count('"') % 2 == 1 and ("assert:" in last or last.strip().startswith('"')):
        reasons.append("ODD_QUOTE_LAST_LINE")
    return reasons


def scan_entry(system: str, entry_id: str, script_rel: str) -> list[dict]:
    root = SCRIPTS / system / script_rel
    cases_dir = root / "cases"
    idx_path = root / "index.yaml"
    findings: list[dict] = []

    index_all: list[str] = []
    index_gold: list[str] = []
    if idx_path.exists():
        idx_text = idx_path.read_text(encoding="utf-8", errors="replace")
        index_all = parse_index_list(idx_text, "all")
        index_gold = parse_index_list(idx_text, "gold")

    on_disk = (
        {p.stem: p for p in cases_dir.glob("*.yaml")} if cases_dir.is_dir() else {}
    )

    for stem in index_all:
        if stem not in on_disk:
            findings.append(
                {
                    "entry_id": entry_id,
                    "script_rel": script_rel,
                    "case_id": stem,
                    "func_id": "",
                    "reasons": ["INDEX_ALL_MISSING_FILE"],
                    "path": f"scripts/{system}/{script_rel}/cases/{stem}.yaml",
                }
            )
    for stem in index_gold:
        if stem not in on_disk:
            findings.append(
                {
                    "entry_id": entry_id,
                    "script_rel": script_rel,
                    "case_id": stem,
                    "func_id": "",
                    "reasons": ["INDEX_GOLD_MISSING_FILE"],
                    "path": f"scripts/{system}/{script_rel}/cases/{stem}.yaml",
                }
            )
    for stem, path in sorted(on_disk.items()):
        if index_all and stem not in index_all:
            # extra on disk — still health-check content; also flag drift
            extra_reason = ["DISK_NOT_IN_INDEX_ALL"]
        else:
            extra_reason = []
        reasons = check_case_file(path) + extra_reason
        if not reasons:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        fm = FUNC_ID_LINE.search(text)
        findings.append(
            {
                "entry_id": entry_id,
                "script_rel": script_rel,
                "case_id": stem,
                "func_id": fm.group(1) if fm else "",
                "reasons": reasons,
                "path": str(path.relative_to(AS_BUILT)),
            }
        )
    return findings


def build_report(system: str) -> tuple[str, list[dict]]:
    mapping = _gap.MAPS.get(system)
    if not mapping:
        raise SystemExit(f"unsupported system {system}")

    findings: list[dict] = []
    for entry_id, _book, script_rel in mapping:
        findings.extend(scan_entry(system, entry_id, script_rel))

    now = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M %Z")
    reason_c = Counter()
    for f in findings:
        for r in f["reasons"]:
            reason_c[r] += 1

    lines = [
        f"# 脚本健康扫描 · {system}",
        "",
        f"> 由 `tools/health-cases.py` 生成 · {now}",
        f"> 与 gap 互补：有文件但半成品/坏结构也会检出。编排见 `script-backfill-playbook.md` §4.1。",
        "",
        "| 指标 | 值 |",
        "|------|----|",
        f"| 需回炉条数 | **{len(findings)}** |",
        f"| 涉及入口 | {len({f['entry_id'] for f in findings})} |",
        "",
        "## 原因分布",
        "",
        "| reason | count |",
        "|--------|------:|",
    ]
    for r, n in reason_c.most_common():
        lines.append(f"| `{r}` | {n} |")

    lines.extend(["", "## 回炉明细（供派单 · 优先于 gap 新写）", ""])
    if not findings:
        lines.append("_无异常。_")
    else:
        lines.append("| entry_id | CASE_ID | FUNC_ID | reasons | path |")
        lines.append("|----------|---------|---------|---------|------|")
        for f in sorted(
            findings, key=lambda x: (x["entry_id"], x["case_id"])
        ):
            lines.append(
                f"| `{f['entry_id']}` | `{f['case_id']}` | `{f['func_id'] or '—'}` | "
                f"{', '.join(f'`{r}`' for r in f['reasons'])} | `{f['path']}` |"
            )
    lines.append("")
    return "\n".join(lines) + "\n", findings


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--system", default="KJZTFWXT")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    text, findings = build_report(args.system)
    print(f"{args.system}: health rework={len(findings)}")
    for f in findings[:30]:
        print(
            f"  {f['entry_id']:24} {f['case_id']:8} {','.join(f['reasons'])}"
        )
    if len(findings) > 30:
        print(f"  … +{len(findings) - 30} more")
    if args.write:
        out = AS_BUILT / f"script-backfill-health-{args.system}.md"
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")


if __name__ == "__main__":
    main()

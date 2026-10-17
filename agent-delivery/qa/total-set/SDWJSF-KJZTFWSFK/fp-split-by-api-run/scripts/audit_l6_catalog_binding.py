#!/usr/bin/env python3
"""Parent QA audit: 3c, 7b, Lxx↔catalog pages, meta row counts, review stale phrases."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "work"
REVIEW = ROOT / "review"
MAP = ROOT / "_l6-to-catalog-map.yaml"
_CANDIDATES = [
    Path(__file__).resolve().parents[7] / "repos/lumen-ui-algo-apiview/src/catalog",
    Path(__file__).resolve().parents[6] / "repos/lumen-ui-algo-apiview/src/catalog",
]
CATALOG_DIR = next((p for p in _CANDIDATES if p.is_dir()), _CANDIDATES[0])

VALID_STATUS = {"live", "unavailable", "req_only"}
L13_ALLOWED_PREFIX = "comp.graph."


def load_endpoint_page_map() -> dict[str, str]:
    m: dict[str, str] = {}
    for jf in CATALOG_DIR.glob("*.json"):
        pages = json.loads(jf.read_text(encoding="utf-8"))
        if not isinstance(pages, list):
            continue
        for page in pages:
            pid = page.get("id", "")
            for ep in page.get("endpoints") or []:
                m[ep["id"]] = pid
    return m


def load_l6_pages() -> dict[str, list[str]]:
    text = MAP.read_text(encoding="utf-8")
    out: dict[str, list[str]] = {}
    for m in re.finditer(
        r"^\s+(L\d+):\s*\{\s*v:\s*\w+,\s*pages:\s*\[([^\]]+)\]",
        text,
        re.M,
    ):
        lid = m.group(1)
        pages = [x.strip() for x in m.group(2).split(",")]
        out[lid] = pages
    return out


def parse_work_rows(path: Path) -> tuple[int | None, list[dict]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    declared: int | None = None
    for line in lines:
        if "表行数" in line:
            dm = re.search(r"\*\*(\d+)\*\*", line)
            if dm:
                declared = int(dm.group(1))
    rows: list[dict] = []
    for line in lines:
        if not line.startswith("|") or "---" in line or "子功能项" in line:
            continue
        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) != 11:
            rows.append({"_bad_cols": len(parts), "_line": line[:120]})
            continue
        rows.append(
            {
                "six": parts[0],
                "endpoint_id": parts[6],
                "method": parts[7],
                "path": parts[8],
                "field_key": parts[9],
                "catalog_status": parts[10],
            }
        )
    return declared, rows


def main() -> int:
    ep_page = load_endpoint_page_map()
    l6_pages = load_l6_pages()
    issues: list[str] = []
    warn: list[str] = []

    keys: list[tuple[str, str]] = []
    key_l6: dict[tuple[str, str], list[str]] = defaultdict(list)
    by_l6_eids: dict[str, set[str]] = defaultdict(set)

    for wf in sorted(WORK.glob("L*.md")):
        lid = wf.stem
        if lid not in l6_pages:
            issues.append(f"{lid}: missing in _l6-to-catalog-map.yaml")
            continue
        allowed_pages = set(l6_pages[lid])
        declared, rows = parse_work_rows(wf)
        data_rows = [r for r in rows if "_bad_cols" not in r]
        bad_parse = [r for r in rows if "_bad_cols" in r]
        if bad_parse:
            issues.append(f"{lid}: {len(bad_parse)} table row(s) with column count != 11")
        if declared is not None and declared != len(data_rows):
            issues.append(
                f"{lid}: meta 表行数 {declared} != actual data rows {len(data_rows)}"
            )

        for r in data_rows:
            st = r["catalog_status"]
            if st not in VALID_STATUS:
                issues.append(f"{lid}: invalid catalog_status `{st}` on {r.get('field_key')}")
            eid = r["endpoint_id"]
            if not eid:
                continue
            by_l6_eids[lid].add(eid)
            if eid not in ep_page:
                issues.append(f"{lid}: unknown endpoint_id `{eid}` (not in catalog JSON)")
                continue
            pg = ep_page[eid]
            if pg not in allowed_pages:
                issues.append(
                    f"{lid}: endpoint `{eid}` belongs to page `{pg}`, "
                    f"not in allowed {sorted(allowed_pages)}"
                )
            k = (eid, r["field_key"])
            keys.append(k)
            key_l6[k].append(lid)

        # L13 hard rule
        if lid == "L13":
            for eid in by_l6_eids[lid]:
                if not eid.startswith(L13_ALLOWED_PREFIX):
                    issues.append(f"L13: forbidden endpoint `{eid}` (must be comp.graph.*)")

        # L05-L12 must not hang comp.graph
        if lid in {f"L{n:02d}" for n in range(5, 13)}:
            for eid in by_l6_eids[lid]:
                if eid.startswith("comp.graph."):
                    issues.append(f"{lid}: must not hang comp.graph endpoint `{eid}`")

    dups = {k: v for k, v in Counter(keys).items() if v > 1}
    for k, n in sorted(dups.items(), key=lambda x: -x[1]):
        issues.append(f"3c: duplicate ({k[0]}, {k[1]}) in {key_l6[k]} (x{n})")

    # Review stale 4A phrase
    for rf in sorted(REVIEW.glob("L*.md")):
        lid = rf.stem
        t = rf.read_text(encoding="utf-8")
        if lid in {f"L{n:02d}" for n in range(5, 13)} and "契约见 L13" in t:
            warn.append(f"{lid} review: still contains「契约见 L13」（构建 API 不应再指 L13）")

    missing_work = [f"L{n:02d}" for n in range(1, 61) if not (WORK / f"L{n:02d}.md").exists()]
    missing_review = [
        f"L{n:02d}" for n in range(1, 61) if not (REVIEW / f"L{n:02d}.md").exists()
    ]
    if missing_work:
        issues.append(f"missing work: {missing_work}")
    if missing_review:
        issues.append(f"missing review: {missing_review}")

    # Semantic heuristics P0
    api_dev = {"L13"}
    for lid in api_dev:
        for eid in by_l6_eids.get(lid, set()):
            if ".graph.ops" in eid or eid.endswith(".ops"):
                issues.append(f"{lid}: API服务六级挂入了 ops 写入 endpoint `{eid}`")

    report_path = ROOT / "memo" / "audit-parent-run-20261017.md"
    lines = [
        "# 父控全库复核报告（不进 F4）",
        "",
        f"- 时间：2026-10-17",
        f"- catalog：`{CATALOG_DIR}`（endpoint 数 {len(ep_page)}）",
        f"- work 文件：{60 - len(missing_work)}/60",
        "",
        "## 结论",
        "",
    ]
    if not issues:
        lines.append("- **硬门禁**：未发现 blocking issue（3c / 页归属 / L13 规则 / 7b / 表列解析）")
    else:
        lines.append(f"- **硬门禁**：**未通过**（{len(issues)} 项）")
    lines.append(f"- **提醒**：{len(warn)} 项 review 文案/抽检建议")
    lines.append("")
    lines.append("## Blocking issues")
    lines.append("")
    if issues:
        for i in issues:
            lines.append(f"- {i}")
    else:
        lines.append("- （无）")
    lines.append("")
    lines.append("## Warnings")
    lines.append("")
    if warn:
        for w in warn:
            lines.append(f"- {w}")
    else:
        lines.append("- （无）")
    lines.append("")
    lines.append("## 抽检：各六级 endpoint 页归属（摘要）")
    lines.append("")
    lines.append("| Lxx | #endpoint_id | pages (from catalog) |")
    lines.append("|---|---:|---|")
    for n in range(1, 61):
        lid = f"L{n:02d}"
        eids = sorted(by_l6_eids.get(lid, set()))
        pages = sorted({ep_page.get(e, "?") for e in eids})
        lines.append(f"| {lid} | {len(eids)} | {', '.join(pages) if pages else '—'} |")

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(report_path)
    print("BLOCKING", len(issues), "WARN", len(warn))
    for i in issues[:30]:
        print("!", i)
    if len(issues) > 30:
        print(f"... and {len(issues)-30} more")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""A16 ingest: officecli view chunks of <=15 rows, write SRS leaves."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

XLSX = r"D:\深圳市国际科技信息中心\20、原型评审\国际科技信息中心项目_需求规格说明书功能清单(各子系统).xlsx"
SHEET = "超大规模智算引擎"
SRS_ROOT = Path(r"e:\gkx-lumen\gkx-orchestration\agent-delivery\bid-reference\srs\06-超大规模智算引擎")
TMP = Path(r"e:\gkx-lumen\gkx-orchestration\agent-delivery\bid-reference\_ingest-loop\_tmp-a16")
ALLOW_J = {"教育领域智能体", "大模型算法服务", "超大规模预训练模型"}
ILLEGAL = re.compile(r'[\\/:*?"<>|]')
ROW_SPLIT = re.compile(r"\[/超大规模智算引擎/row\[(\d+)\]\]\s*")

RANGES = [
    (147, 161),
    (162, 176),
    (177, 182),
    (183, 197),
    (198, 212),
    (213, 226),
    (357, 371),
    (372, 386),
    (387, 401),
    (402, 416),
    (417, 422),
]


def officecli_bin() -> str:
    r = subprocess.run(
        ["powershell", "-NoProfile", "-Command", "(Get-Command officecli).Source"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    p = (r.stdout or "").strip()
    if not p:
        return "officecli"
    return p


OC = officecli_bin()


def view_range(start: int, end: int) -> str:
    if end - start + 1 > 15:
        raise SystemExit(f"chunk too large: {start}-{end}")
    rng = f"{SHEET}!A{start}:N{end}"
    r = subprocess.run(
        [OC, "view", XLSX, "text", "--range", rng],
        capture_output=True,
    )
    if r.returncode != 0:
        err = r.stderr.decode("utf-8", errors="replace")
        raise SystemExit(f"officecli failed {rng}: {err}")
    for enc in ("utf-8", "gbk", "utf-16"):
        try:
            return r.stdout.decode(enc)
        except UnicodeDecodeError:
            continue
    return r.stdout.decode("utf-8", errors="replace")


def parse_cells(body: str, rownum: int) -> dict[str, str]:
    marker = re.compile(rf"(?:(?<=^)|(?<=\t))([A-N]){rownum}=")
    matches = list(marker.finditer(body))
    cells: dict[str, str] = {}
    for i, m in enumerate(matches):
        col = m.group(1)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        raw = body[start:end]
        if i + 1 < len(matches) and raw.endswith("\t"):
            raw = raw[:-1]
        if i == len(matches) - 1:
            raw = raw.rstrip("\n")
        cells[col] = raw
    return cells


def parse_text(text: str) -> list[tuple[int, dict[str, str]]]:
    parts = ROW_SPLIT.split(text)
    rows: list[tuple[int, dict[str, str]]] = []
    i = 1
    while i + 1 < len(parts):
        rownum = int(parts[i])
        body = parts[i + 1]
        rows.append((rownum, parse_cells(body, rownum)))
        i += 2
    return rows


def empty_title(val: str) -> str:
    return val if val.strip() else "（空）"


def filename_for_k(k: str) -> str:
    name = empty_title(k)
    name = ILLEGAL.sub("_", name)
    return f"{name}.md"


def md_escape_none(s: str) -> str:
    return s if s else ""


def leaf_md(rec: dict) -> str:
    title = empty_title(rec["L6"])
    notes = rec["notes"] if rec["notes"] else "（空）"
    bid = rec["bid_desc"]
    lines = [
        f"### {title} · 序号 {rec['seq']}",
        "",
        f"- excel_sheet: {SHEET}",
        f"- excel_row: {rec['excel_row']}",
        f"- seq: {rec['seq']}",
        f"- path: {rec['path']}",
        f"- level5: {empty_title(rec['L5'])}",
        f"- bid_desc: {bid}",
        f"- bid_desc_inherited: {'true' if rec['inherited'] else 'false'}",
    ]
    if rec["inherited"]:
        lines.append(f"- bid_desc_from_excel_row: {rec['inherit_from']}")
    lines += [
        f"- notes: {notes}",
        "",
        "#### 需规功能描述",
        "",
        rec["desc"] if rec["desc"] else "（空）",
        "",
    ]
    return "\n".join(lines)


def file_header(j: str, k: str, recs: list[dict]) -> str:
    rows = [r["excel_row"] for r in recs]
    path0 = recs[0]["path_prefix"]
    return "\n".join(
        [
            f"# {empty_title(k)}",
            "",
            f"- system: {SHEET}",
            f"- level3: {SHEET}",
            f"- level4_J: {j}",
            f"- source_sheet: {SHEET}",
            f"- excel_rows: {min(rows)}-{max(rows)}",
            f"- leaf_count: {len(recs)}",
            "",
            "## 检索",
            "",
            f"`{path0}`",
            "",
            "---",
            "",
        ]
    )


def write_k_file(j: str, k: str, recs: list[dict]) -> Path:
    recs = sorted(recs, key=lambda r: r["excel_row"])
    d = SRS_ROOT / j
    d.mkdir(parents=True, exist_ok=True)
    p = d / filename_for_k(k)
    body = file_header(j, k, recs) + "\n".join(leaf_md(r) for r in recs)
    p.write_text(body, encoding="utf-8")
    return p


def write_module_readme(j: str, by_k: dict[str, list[dict]]) -> Path:
    all_recs = [r for recs in by_k.values() for r in recs]
    rows = [r["excel_row"] for r in all_recs]
    lines = [
        f"# {j}",
        "",
        f"- system: {SHEET}",
        f"- source_sheet: {SHEET}",
        f"- filter_J: {j}",
        f"- excel_rows: {min(rows)}-{max(rows)}",
        f"- leaf_count: {len(all_recs)}",
        "",
        "| 四级文件 | 叶子数 | excel_rows |",
        "|----------|--------|------------|",
    ]
    for k in sorted(by_k.keys(), key=lambda x: min(r["excel_row"] for r in by_k[x])):
        recs = sorted(by_k[k], key=lambda r: r["excel_row"])
        rs = [r["excel_row"] for r in recs]
        # collapse to closed intervals
        intervals = []
        a = b = rs[0]
        for n in rs[1:]:
            if n == b + 1:
                b = n
            else:
                intervals.append(f"{a}–{b}" if a != b else str(a))
                a = b = n
        intervals.append(f"{a}–{b}" if a != b else str(a))
        lines.append(f"| `{filename_for_k(k)}` | {len(recs)} | {', '.join(intervals)} |")
    lines.append("")
    p = SRS_ROOT / j / "README.md"
    p.write_text("\n".join(lines), encoding="utf-8")
    return p


def main() -> None:
    leaves: dict[tuple[str, str], list[dict]] = defaultdict(list)
    last_g_row: int | None = None
    gaps: list[str] = []
    written_rows: list[int] = []

    for start, end in RANGES:
        text = view_range(start, end)
        (TMP / f"chunk-{start}-{end}.txt").write_text(text, encoding="utf-8")
        parsed = parse_text(text)
        got = {r for r, _ in parsed}
        expect = set(range(start, end + 1))
        if got != expect:
            gaps.append(f"officecli parse row mismatch {start}-{end}: got {sorted(got)}")
        for rownum, cells in parsed:
            j = cells.get("J", "")
            if j not in ALLOW_J:
                gaps.append(f"row {rownum} J={j!r} out of A16 filter (skipped)")
                continue
            g = cells.get("G", "")
            inherited = False
            inherit_from = None
            if not g.strip():
                inherited = True
                inherit_from = last_g_row
                bid_desc = "（本行空）"
            else:
                bid_desc = g
                last_g_row = rownum
            h = cells.get("H", "")
            i = cells.get("I", "")
            k = cells.get("K", "")
            l5 = cells.get("L", "")
            l6 = cells.get("M", "")
            desc = cells.get("N", "")
            seq = cells.get("A", "")
            notes = cells.get("notes", "")  # this sheet has no notes col; N is desc
            # detect missing columns
            for col in "AHIJKLMN":
                if col not in cells:
                    gaps.append(f"row {rownum} missing col {col}")
            if not desc.strip():
                gaps.append(f"row {rownum} empty 需规功能描述 (N)")
            rec = {
                "excel_row": rownum,
                "seq": seq if seq else "（空）",
                "J": j,
                "K": k,
                "L5": l5,
                "L6": l6,
                "path": "/".join(
                    [
                        empty_title(h),
                        empty_title(i),
                        empty_title(j),
                        empty_title(k),
                        empty_title(l5),
                        empty_title(l6),
                    ]
                ),
                "path_prefix": " / ".join(
                    [empty_title(h), empty_title(i), empty_title(j), empty_title(k)]
                ),
                "bid_desc": bid_desc,
                "inherited": inherited,
                "inherit_from": inherit_from,
                "notes": "",
                "desc": desc,
            }
            leaves[(j, k)].append(rec)
            written_rows.append(rownum)

        # write after each chunk
        by_j: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
        for (j, k), recs in leaves.items():
            by_j[j][k] = recs
        for j, by_k in by_j.items():
            for k, recs in by_k.items():
                write_k_file(j, k, recs)
            write_module_readme(j, by_k)

        print(f"chunk {start}-{end}: parsed={len(parsed)} cumulative={len(written_rows)}", flush=True)

    # final rewrite
    by_j = defaultdict(lambda: defaultdict(list))
    for (j, k), recs in leaves.items():
        by_j[j][k] = recs
    files = []
    for j in sorted(by_j.keys()):
        by_k = by_j[j]
        for k, recs in by_k.items():
            p = write_k_file(j, k, recs)
            files.append(p)
        rp = write_module_readme(j, by_k)
        files.append(rp)

    summary = {
        "written_leaves": len(written_rows),
        "rows": written_rows,
        "by_j": {j: sum(len(v) for v in by_k.values()) for j, by_k in by_j.items()},
        "files": [str(p.relative_to(SRS_ROOT.parent)) for p in files],
        "gaps": gaps,
    }
    (TMP / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("DONE", json.dumps({k: summary[k] for k in ("written_leaves", "by_j", "gaps")}, ensure_ascii=False))


if __name__ == "__main__":
    main()

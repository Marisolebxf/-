# -*- coding: utf-8 -*-
"""A11 SRS ingest: officecli JSON chunks -> markdown leaves."""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

CHUNK_DIR = Path(__file__).resolve().parent
SRS_ROOT = Path(
    r"e:\gkx-lumen\gkx-orchestration\agent-delivery\bid-reference\srs\04-科技专题服务系统"
)
SHEET = "科技专题服务系统"
ALLOWED_I = {
    "科技专题内容运营中心",
    "科技专题项目管理",
    "科技专题系统管理中心",
    "科技专题信息发布管理",
}
ILLEGAL = re.compile(r'[\\/:*?"<>|]')
EXPECTED = 239


def cell(cells: dict, col: str, row: int) -> str:
    v = cells.get(f"{col}{row}", "")
    if v is None:
        return ""
    return str(v)


def sanitize_filename(name: str) -> str:
    name = (name or "").strip()
    if not name:
        return "（空）"
    return ILLEGAL.sub("_", name)


def disp(name: str) -> str:
    name = (name or "").strip()
    return name if name else "（空）"


def load_rows() -> list[dict]:
    rows = []
    files = sorted(CHUNK_DIR.glob("chunk-*.json"))
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        for sheet in data["data"]["sheets"]:
            rows.extend(sheet["rows"])
    rows.sort(key=lambda r: r["row"])
    return rows


def leaf_md(rec: dict) -> str:
    lines = []
    lines.append(f"### {disp(rec['L'])} · 序号 {disp(rec['A'])}")
    lines.append("")
    lines.append(f"- excel_sheet: {SHEET}")
    lines.append(f"- excel_row: {rec['row']}")
    lines.append(f"- seq: {disp(rec['A'])}")
    path = "/".join(disp(rec[k]) for k in "GHIJKL")
    lines.append(f"- path: {path}")
    lines.append(f"- level5: {disp(rec['K'])}")
    if rec["F"].strip():
        lines.append(f"- bid_desc: {rec['F']}")
        lines.append("- bid_desc_inherited: false")
    else:
        lines.append("- bid_desc: （本行空）")
        if rec["inherit_from"]:
            lines.append("- bid_desc_inherited: true")
            lines.append(f"- bid_desc_prev_nonempty_row: {rec['inherit_from']}")
        else:
            lines.append("- bid_desc_inherited: false")
    notes = rec["N"].strip() if rec["N"].strip() else "（空）"
    lines.append(f"- notes: {notes}")
    lines.append("")
    lines.append("#### 需规功能描述")
    lines.append("")
    body = rec["M"] if rec["M"].strip() else "（空）"
    lines.append(body)
    lines.append("")
    return "\n".join(lines)


def file_header(j: str, i: str, recs: list[dict]) -> str:
    rows = [r["row"] for r in recs]
    lines = [
        f"# {disp(j)}",
        "",
        f"- system: {SHEET}",
        f"- level3: {i}",
        f"- source_sheet: {SHEET}",
        f"- excel_rows: {min(rows)}-{max(rows)}",
        f"- leaf_count: {len(recs)}",
        "",
        "## 检索",
        "",
        f"`{disp(recs[0]['G'])} / {disp(recs[0]['H'])} / {disp(i)} / {disp(j)}`",
        "",
        "---",
        "",
    ]
    return "\n".join(lines)


def module_readme(i: str, files: dict[str, list[dict]]) -> str:
    all_rows = [r["row"] for recs in files.values() for r in recs]
    lines = [
        f"# {i}",
        "",
        f"- system: {SHEET}",
        f"- level3: {i}",
        f"- source_sheet: {SHEET}",
        f"- excel_rows: {min(all_rows)}-{max(all_rows)}",
        f"- leaf_count: {sum(len(v) for v in files.values())}",
        "",
        "| 四级功能文件 | 叶子数 | excel_rows |",
        "|--------------|--------|------------|",
    ]
    for j in sorted(files, key=lambda x: min(r["row"] for r in files[x])):
        recs = files[j]
        rows = [r["row"] for r in recs]
        fn = sanitize_filename(j) + ".md"
        lines.append(f"| `{fn}` | {len(recs)} | {min(rows)}-{max(rows)} |")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    raw = load_rows()
    gaps: list[str] = []
    last_f_row = None
    recs: list[dict] = []

    seen_rows = set()
    for r in raw:
        n = r["row"]
        if n in seen_rows:
            gaps.append(f"duplicate excel_row {n}")
            continue
        seen_rows.add(n)
        cells = r["cells"]
        rec = {col: cell(cells, col, n) for col in "ABCDEFGHIJKLMN"}
        rec["row"] = n
        if rec["I"].strip() not in ALLOWED_I:
            gaps.append(f"row {n} I={rec['I']!r} out of filter (skipped)")
            continue
        if rec["F"].strip():
            last_f_row = n
            rec["inherit_from"] = None
        else:
            rec["inherit_from"] = last_f_row
        recs.append(rec)
        for col in "JKLM":
            if not rec[col].strip():
                gaps.append(f"empty {col} at excel_row {n}")
        if rec["M"] and rec["M"].endswith("…"):
            gaps.append(f"possible truncation M excel_row {n}")

    if len(recs) != EXPECTED:
        raise SystemExit(f"written would be {len(recs)} != {EXPECTED}")

    grouped: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for rec in recs:
        grouped[rec["I"]][rec["J"]].append(rec)

    written = 0
    file_list = []
    for i, jmap in grouped.items():
        idir = SRS_ROOT / i
        idir.mkdir(parents=True, exist_ok=True)
        for j, jrecs in jmap.items():
            jrecs.sort(key=lambda x: x["row"])
            fn = sanitize_filename(j) + ".md"
            body = file_header(j, i, jrecs) + "\n".join(leaf_md(r) for r in jrecs)
            path = idir / fn
            path.write_text(body, encoding="utf-8", newline="\n")
            written += len(jrecs)
            rel = f"04-科技专题服务系统/{i}/{fn}"
            file_list.append((rel, len(jrecs), min(r["row"] for r in jrecs), max(r["row"] for r in jrecs)))
        (idir / "README.md").write_text(module_readme(i, jmap), encoding="utf-8", newline="\n")
        file_list.append((f"04-科技专题服务系统/{i}/README.md", 0, 0, 0))

    by_i = {i: sum(len(v) for v in jmap.values()) for i, jmap in grouped.items()}
    summary = {
        "written_leaves": written,
        "by_i": by_i,
        "files": file_list,
        "excel_rows": f"{min(r['row'] for r in recs)}-{max(r['row'] for r in recs)}",
        "gaps": gaps,
        "empty_F": sum(1 for r in recs if not r["F"].strip()),
        "raw_chunk_rows": len(raw),
    }
    (CHUNK_DIR / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"written_leaves={written}")
    print("by_i=" + json.dumps(by_i, ensure_ascii=False))
    print(f"md_files={len([f for f in file_list if f[0].endswith('.md') and not f[0].endswith('README.md')])}")
    print(f"gaps={len(gaps)}")


if __name__ == "__main__":
    main()

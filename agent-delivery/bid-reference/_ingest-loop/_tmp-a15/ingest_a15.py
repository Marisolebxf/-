# -*- coding: utf-8 -*-
"""A15 ingest: officecli view 15-row chunks -> srs leaves. Do not mutate xlsx."""
from __future__ import annotations

import os
import re
import shutil
import subprocess
from collections import OrderedDict
from pathlib import Path

XLSX = r"D:\深圳市国际科技信息中心\20、原型评审\国际科技信息中心项目_需求规格说明书功能清单(各子系统).xlsx"
SHEET = "超大规模智算引擎"
FILTER_J = "智能体开发应用平台"
OUT_DIR = Path(r"e:\gkx-lumen\gkx-orchestration\agent-delivery\bid-reference\srs\06-超大规模智算引擎\智能体开发应用平台")
TMP = Path(r"e:\gkx-lumen\gkx-orchestration\agent-delivery\bid-reference\_ingest-loop\_tmp-a15")
DONE = Path(r"e:\gkx-lumen\gkx-orchestration\agent-delivery\bid-reference\_ingest-loop\DONE-A15.md")
EXPECTED = 130
CHUNKS = [
    (227, 241),
    (242, 256),
    (257, 271),
    (272, 286),
    (287, 301),
    (302, 316),
    (317, 331),
    (332, 346),
    (347, 356),
]
ILLEGAL = str.maketrans({c: "_" for c in '\\/:*?"<>|'})
CELL_RE = re.compile(r"(?:(?<=\t)|(?<=\] ))([A-N])(\d+)=(.*?)(?=\t[A-N]\d+=|$)")
ROW_START = re.compile(r"^\[/.*/row\[(\d+)\]\]\s*")


def officecli_bin() -> str:
    p = shutil.which("officecli")
    if not p:
        raise SystemExit("officecli not on PATH")
    return p


def view_chunk(oc: str, start: int, end: int) -> str:
    rng = f"{SHEET}!A{start}:N{end}"
    if end - start + 1 > 15:
        raise SystemExit(f"chunk too large: {start}-{end}")
    r = subprocess.run(
        [oc, "view", XLSX, "text", "--range", rng],
        capture_output=True,
        check=False,
    )
    raw = r.stdout
    for enc in ("utf-8-sig", "utf-8", "gbk"):
        try:
            text = raw.decode(enc)
            if "智能体开发应用平台" in text or "超大规模智算引擎" in text or "=== Sheet:" in text:
                if enc != "utf-8" and "智能体" not in text:
                    continue
                decoded = text
                break
        except UnicodeDecodeError:
            continue
    else:
        decoded = raw.decode("utf-8", errors="replace")
    dest = TMP / f"chunk-{start}-{end}.utf8.txt"
    dest.write_text(decoded, encoding="utf-8")
    if r.returncode != 0:
        raise SystemExit(f"officecli failed {rng}: {r.stderr.decode('utf-8', errors='replace')}")
    return decoded


def parse_rows(text: str) -> list[dict]:
    rows: list[dict] = []
    current_no = None
    buf: list[str] = []

    def flush():
        nonlocal current_no, buf
        if current_no is None:
            return
        blob = "\n".join(buf)
        m = ROW_START.match(blob)
        rest = blob[m.end() :] if m else blob
        cells: dict[str, str] = {}
        for cm in re.finditer(
            r"([A-N])(\d+)=", rest
        ):
            pass
        # split by tab+ColRow=
        parts = re.split(r"\t(?=[A-N]\d+=)", rest)
        for i, part in enumerate(parts):
            part = part.strip("\r")
            if i == 0:
                part = part.lstrip()
            m2 = re.match(r"([A-N])(\d+)=(.*)$", part, re.S)
            if not m2:
                continue
            col, rno, val = m2.group(1), int(m2.group(2)), m2.group(3)
            if val.endswith("\n") and "\n" not in val[:-1]:
                val = val.rstrip("\r\n")
            else:
                val = val.rstrip("\r")
                if val.endswith("\n") and not val[:-1].endswith("\n"):
                    # single trailing newline from dump line
                    val = val[:-1]
            cells[col] = val
        rec = {"excel_row": current_no, **{k: cells.get(k, "") for k in "ABCDEFGHIJKLMN"}}
        rows.append(rec)
        current_no = None
        buf = []

    for line in text.splitlines():
        if line.startswith("==="):
            continue
        ms = ROW_START.match(line)
        if ms:
            flush()
            current_no = int(ms.group(1))
            buf = [line]
        elif current_no is not None:
            buf.append(line)
    flush()
    return rows


def safe_name(s: str) -> str:
    s = (s or "").strip() or "（空）"
    return s.translate(ILLEGAL)


def md_escape_none(s: str) -> str:
    return s.replace("\r\n", "\n").replace("\r", "\n")


def render_leaf(rec: dict, inherited: bool, inherit_from: int | None) -> str:
    seq = rec["A"].strip()
    l6 = rec["M"].strip() or "（空）"
    path_parts = []
    for col in "HIJKLM":
        v = rec[col].strip()
        path_parts.append(v if v else "（空）")
    path = "/".join(path_parts)
    g = rec["G"].strip()
    if g:
        bid = g
    else:
        bid = "（本行空）"
    notes = ""
    lines = [
        f"### {l6} · 序号 {seq}",
        "",
        f"- excel_sheet: {SHEET}",
        f"- excel_row: {rec['excel_row']}",
        f"- seq: {seq}",
        f"- path: {path}",
        f"- bid_desc: {bid}",
    ]
    if inherited:
        lines.append("- bid_desc_inherited: true")
        if inherit_from:
            lines.append(f"- inherit_from_excel_row: {inherit_from}")
    lines.append(f"- notes: {notes}")
    lines.append("")
    lines.append("#### 需规功能描述")
    lines.append("")
    desc = md_escape_none(rec["N"])
    if not desc.strip():
        desc = "（本行空）"
    lines.append(desc)
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    oc = officecli_bin()
    all_rows: list[dict] = []
    gaps: list[str] = []
    for start, end in CHUNKS:
        text = view_chunk(oc, start, end)
        parsed = parse_rows(text)
        got_rows = {r["excel_row"] for r in parsed}
        missing = [i for i in range(start, end + 1) if i not in got_rows]
        if missing:
            gaps.append(f"officecli parse miss rows {missing} in {start}-{end}")
        all_rows.extend(parsed)

    filtered = [r for r in all_rows if r["J"].strip() == FILTER_J]
    extra = [r["excel_row"] for r in all_rows if r["J"].strip() != FILTER_J]
    if extra:
        gaps.append(f"rows in dump with J!={FILTER_J}: {extra}")

    last_bid_row = None
    files: OrderedDict[str, list[tuple[dict, bool, int | None]]] = OrderedDict()
    for rec in filtered:
        g = rec["G"].strip()
        if g:
            last_bid_row = rec["excel_row"]
            inherited, inherit_from = False, None
        else:
            inherited, inherit_from = True, last_bid_row
        k = rec["K"].strip() or "（空）"
        files.setdefault(k, []).append((rec, inherited, inherit_from))
        for col, label in (("N", "需规功能描述"), ("M", "六级功能")):
            if not rec[col].strip():
                gaps.append(f"empty {label} excel_row={rec['excel_row']}")
        if rec["N"].endswith("…") or rec["N"].endswith("..."):
            gaps.append(f"possible truncation excel_row={rec['excel_row']} N ends with ellipsis")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # clear prior md except we may overwrite
    written_leaves = 0
    file_rows = []
    rel_files = []
    for k, items in files.items():
        fname = safe_name(k) + ".md"
        excel_rows = [t[0]["excel_row"] for t in items]
        lo, hi = min(excel_rows), max(excel_rows)
        body = [f"# {k}", "", f"> 需规四级 K = {k} · excel_rows {lo}–{hi} · leaf_count {len(items)}", ""]
        for rec, inherited, inherit_from in items:
            body.append(render_leaf(rec, inherited, inherit_from))
            written_leaves += 1
        path = OUT_DIR / fname
        path.write_text("\n".join(body).rstrip() + "\n", encoding="utf-8")
        rel = f"06-超大规模智算引擎/智能体开发应用平台/{fname}"
        rel_files.append(rel)
        file_rows.append((fname, len(items), lo, hi))

    readme_lines = [
        "# 智能体开发应用平台",
        "",
        f"- Excel 表：{SHEET}",
        f"- 过滤：需规 J = {FILTER_J}",
        "- loop：A15",
        f"- expected_data_rows：{EXPECTED}",
        f"- written_leaves：{written_leaves}",
        "- excel_rows：227–356",
        "",
        "| 四级文件 | leaf_count | excel_rows |",
        "|----------|------------|------------|",
    ]
    for fname, n, lo, hi in file_rows:
        readme_lines.append(f"| `{fname}` | {n} | {lo}–{hi} |")
    (OUT_DIR / "README.md").write_text("\n".join(readme_lines) + "\n", encoding="utf-8")
    rel_files.insert(0, "06-超大规模智算引擎/智能体开发应用平台/README.md")

    excel_rows_list = [r["excel_row"] for r in filtered]
    done = [
        "# DONE-A15",
        "",
        "| 项 | 值 |",
        "|----|----|",
        f"| sheet | {SHEET} |",
        f"| filter | J={FILTER_J} |",
        f"| excel_rows | {min(excel_rows_list)}–{max(excel_rows_list)} |" if excel_rows_list else "| excel_rows | |",
        f"| expected_data_rows | {EXPECTED} |",
        f"| written_leaves | {written_leaves} |",
        "| files | " + "<br>".join(f"`{p}`" for p in rel_files) + " |",
        "| gaps | " + ("无" if not gaps else "<br>".join(gaps)) + " |",
        "",
    ]
    DONE.write_text("\n".join(done), encoding="utf-8")
    summary = {
        "parsed": len(all_rows),
        "filtered": len(filtered),
        "written_leaves": written_leaves,
        "files": len(file_rows),
        "ks": list(files.keys()),
        "gaps": gaps,
        "extra_j": extra,
    }
    (TMP / "summary.txt").write_text(repr(summary) + "\n", encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    main()

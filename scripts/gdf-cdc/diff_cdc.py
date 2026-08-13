#!/usr/bin/env python3
"""Compare two CDC workbooks cell-by-cell (values only)."""
from __future__ import annotations

import argparse
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter


def norm(v) -> str:
    if v is None or v == "":
        return ""
    if isinstance(v, float) and v == int(v):
        return str(int(v))
    if isinstance(v, bool):
        return "TRUE" if v else "FALSE"
    return str(v).replace("\r\n", "\n")


def used_dim(ws) -> tuple[int, int]:
    max_r = max_c = 1
    for row in ws.iter_rows():
        for c in row:
            if c.value not in (None, ""):
                if c.row > max_r:
                    max_r = c.row
                if c.column > max_c:
                    max_c = c.column
    return max_r, max_c


def diff_books(left: Path, right: Path, limit: int = 80) -> dict:
    wb_l = load_workbook(left, data_only=False)
    wb_r = load_workbook(right, data_only=False)
    names_l = list(wb_l.sheetnames)
    names_r = list(wb_r.sheetnames)
    diffs: list[str] = []
    n = 0
    if names_l != names_r:
        diffs.append(f"SHEETS gold={names_l} gen={names_r}")
        n += 1
    for name in names_l:
        if name not in wb_r.sheetnames:
            diffs.append(f"MISSING_SHEET {name}")
            n += 1
            continue
        ws_l, ws_r = wb_l[name], wb_r[name]
        mr = max(used_dim(ws_l)[0], used_dim(ws_r)[0])
        mc = max(used_dim(ws_l)[1], used_dim(ws_r)[1])
        for r in range(1, mr + 1):
            for c in range(1, mc + 1):
                a = norm(ws_l.cell(r, c).value)
                b = norm(ws_r.cell(r, c).value)
                if a != b:
                    n += 1
                    if len(diffs) < limit:
                        coord = f"{get_column_letter(c)}{r}"
                        diffs.append(f"{name}!{coord} gold={a!r} gen={b!r}")
    extra = [s for s in names_r if s not in names_l]
    for name in extra:
        n += 1
        if len(diffs) < limit:
            diffs.append(f"EXTRA_SHEET {name}")
    return {"diff_count": n, "shown": diffs, "gold_sheets": names_l, "gen_sheets": names_r}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", required=True)
    ap.add_argument("--gen", required=True)
    ap.add_argument("-o", "--out", default="-")
    ap.add_argument("--limit", type=int, default=80)
    args = ap.parse_args()
    gold, gen = Path(args.gold), Path(args.gen)
    if gold.is_dir() and gen.is_dir():
        reports = []
        total = 0
        for fn in ("1、贴源_模板.xlsx", "2、明细数据_模板.xlsx"):
            r = diff_books(gold / fn, gen / fn, args.limit)
            r["file"] = fn
            reports.append(r)
            total += r["diff_count"]
        lines = [f"# CDC diff  gold={gold}  gen={gen}", f"total_diffs={total}", ""]
        for r in reports:
            lines.append(f"## {r['file']}  diffs={r['diff_count']}")
            lines.extend(r["shown"])
            if r["diff_count"] > len(r["shown"]):
                lines.append(f"... {r['diff_count'] - len(r['shown'])} more")
            lines.append("")
        text = "\n".join(lines)
        print(f"total_diffs={total}")
    else:
        r = diff_books(gold, gen, args.limit)
        lines = [f"# CDC diff", f"diffs={r['diff_count']}", ""] + r["shown"]
        text = "\n".join(lines)
        print(f"diffs={r['diff_count']}")
    if args.out == "-":
        print(text)
    else:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()

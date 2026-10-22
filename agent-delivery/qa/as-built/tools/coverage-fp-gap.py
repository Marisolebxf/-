#!/usr/bin/env python3
"""List KJZTFWXT case books whose coverage-fp.md is behind the live case table.

A book is listed when a live main-table FUNC id is absent from coverage-fp.md,
or a voided id still sits on an 已覆盖 / 部分覆盖 row.
Remarks that merely say 接作废 do not void a live row.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "test-cases" / "KJZTFWXT"
LIVE_RE = re.compile(r"^\| ZNFWJQ-KJZTFWXT-v1\.0-FUNC-(\d{5}) \|", re.M)
RANGE_RE = re.compile(r"(\d{5})\s*[~～\-—]+\s*(\d{5})")


def split_row(line: str) -> list[str]:
    protected = line.replace("\\|", "\x00")
    return [c.strip().replace("\x00", "|") for c in protected.strip().strip("|").split("|")]


def void_ids(text: str, live: set[str]) -> set[str]:
    void: set[str] = set()
    head = text.split("##", 1)[0]
    for line in head.splitlines():
        if not any(w in line for w in ("作废", "删除", "废弃", "不复用")):
            continue
        for a, b in RANGE_RE.findall(line):
            void.update(f"{i:05d}" for i in range(int(a), int(b) + 1))
        void.update(re.findall(r"\d{5}", line))
    for line in text.splitlines():
        if not line.startswith("|") or "ZNFWJQ" in line or "作废" not in line:
            continue
        cells = split_row(line)
        if cells and re.fullmatch(r"\d{5}", cells[0]):
            void.add(cells[0])
    return void - live


def covered_ids(cov: str) -> tuple[set[str], set[str]]:
    """Return (ids on 已覆盖/部分覆盖 rows, ids mentioned in any table cell)."""
    covered: set[str] = set()
    mentioned: set[str] = set()
    for line in cov.splitlines():
        if not line.startswith("|"):
            continue
        cells = split_row(line)
        if not cells or all(set(c) <= set("-: ") for c in cells):
            continue
        if "功能点键" in cells[0] or "对应用例" in "".join(cells[:4]):
            continue
        ids = []
        for c in cells:
            ids.extend(re.findall(r"\d{5}", c))
        mentioned.update(ids)
        if any(c in ("已覆盖", "部分覆盖") for c in cells):
            covered.update(ids)
    return covered, mentioned


def gaps(book: Path) -> list[str]:
    cases = list(book.glob("FUNC-*-用例.md"))
    cov_path = book / "coverage-fp.md"
    if len(cases) != 1 or not cov_path.is_file():
        return ["缺用例册或 coverage-fp.md"]
    text = cases[0].read_text(encoding="utf-8")
    cov = cov_path.read_text(encoding="utf-8")
    live = set(LIVE_RE.findall(text))
    void = void_ids(text, live)
    covered, mentioned = covered_ids(cov)
    missing = sorted(live - mentioned)
    stale = sorted((void & covered) - live)
    out = []
    if missing:
        out.append(f"有效号未挂{len(missing)}:{','.join(missing[:8])}")
    if stale:
        out.append(f"作废号仍在已覆盖{len(stale)}:{','.join(stale[:8])}")
    return out


def main() -> None:
    only = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else None
    books = [only] if only else sorted(p.parent for p in ROOT.rglob("coverage-fp.md"))
    n = 0
    for book in books:
        bad = gaps(book)
        if not bad:
            continue
        n += 1
        rel = book.relative_to(ROOT.parent.parent) if book.is_relative_to(ROOT.parent.parent) else book
        # print path relative to qa/
        try:
            rel = book.relative_to(ROOT.parents[1])
        except ValueError:
            rel = book
        print(f"{rel}\t{'；'.join(bad)}")
    if not only:
        print(f"# 待改 {n}", file=sys.stderr)


if __name__ == "__main__":
    main()

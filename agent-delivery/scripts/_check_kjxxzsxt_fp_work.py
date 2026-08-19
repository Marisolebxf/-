# -*- coding: utf-8 -*-
"""Check KJXXZSXT work/Txx.md row counts vs header dim/source stats."""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

RUN = Path(
    r"d:\work\gkx-lumen\gkx-orchestration\agent-delivery\qa\total-set\KJXXZSXT\fp-split-run"
)


def parse(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    n_m = re.search(r"^- 条数：(\d+)\s*$", text, re.M)
    dim_m = re.search(r"^- 拆分维度：(.+)$", text, re.M)
    src_m = re.search(r"^- 规则来源：(.+)$", text, re.M)
    declared = int(n_m.group(1)) if n_m else None
    rows = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5:
            continue
        if cells[0] in ("子功能项", "---") or set(cells[0]) <= set("-:"):
            continue
        rows.append(cells)
    dims = Counter(r[2] for r in rows)
    srcs = Counter(r[3] for r in rows)

    def parse_stat(s: str | None) -> dict[str, int]:
        if not s:
            return {}
        out = {}
        for part in s.split("、"):
            part = part.strip()
            m = re.match(r"(.+?)\s+(\d+)$", part)
            if m:
                out[m.group(1).strip()] = int(m.group(2))
        return out

    return {
        "declared": declared,
        "rows": len(rows),
        "dims": dims,
        "srcs": srcs,
        "head_dims": parse_stat(dim_m.group(1) if dim_m else None),
        "head_srcs": parse_stat(src_m.group(1) if src_m else None),
        "review": (RUN / "review" / path.name).exists(),
    }


def main() -> None:
    work = RUN / "work"
    files = sorted(work.glob("T*.md"), key=lambda p: int(p.stem[1:]))
    total = 0
    bad = []
    for f in files:
        d = parse(f)
        total += d["rows"]
        issues = []
        if d["declared"] != d["rows"]:
            issues.append(f"header={d['declared']} table={d['rows']}")
        if sum(d["dims"].values()) != d["rows"]:
            issues.append("dim rows mismatch")
        if dict(d["dims"]) != d["head_dims"]:
            issues.append(f"dim head {d['head_dims']} vs {dict(d['dims'])}")
        if dict(d["srcs"]) != d["head_srcs"]:
            issues.append(f"src head {d['head_srcs']} vs {dict(d['srcs'])}")
        if not d["review"]:
            issues.append("missing review")
        if issues:
            bad.append(f"{f.stem}: " + "; ".join(issues))
        print(f"{f.stem}\t{d['rows']}\t{'OK' if not issues else 'FAIL'}")
    print("FILES", len(files), "TOTAL", total)
    if bad:
        print("ISSUES")
        print("\n".join(bad))


if __name__ == "__main__":
    main()

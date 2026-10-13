# -*- coding: utf-8 -*-
"""Check 算法库（旧记 KJZTFWALGO）work/Lxx.md header counts vs table rows."""
from pathlib import Path
import re
import sys

RUN = Path(__file__).resolve().parents[1] / "qa/total-set/SDWJSF-KJZTFWSFK/fp-split-run"
ids = sys.argv[1:] or [p.stem for p in sorted((RUN / "work").glob("L*.md"))]
fail = 0
for lid in ids:
    p = RUN / "work" / f"{lid}.md"
    r = RUN / "review" / f"{lid}.md"
    if not p.exists():
        print("MISSING_WORK", lid)
        fail += 1
        continue
    text = p.read_text(encoding="utf-8")
    m = re.search(r"^- 条数：(\d+)", text, re.M)
    if not m:
        print("NO_COUNT", lid)
        fail += 1
        continue
    n = int(m.group(1))
    rows = [ln for ln in text.splitlines() if re.match(r"^\| [^|]+ \| [^|]+ \| [^|]+ \| [^|]+ \|$", ln)]
    rows = [ln for ln in rows if not ln.startswith("| 子功能项") and "---" not in ln]
    dim_h = re.search(r"^- 拆分维度：(.+)$", text, re.M)
    src_h = re.search(r"^- 规则来源：(.+)$", text, re.M)
    from collections import Counter

    dim_c = Counter()
    src_c = Counter()
    for ln in rows:
        parts = [x.strip() for x in ln.strip("|").split("|")]
        if len(parts) != 4:
            print("BAD_ROW", lid, ln[:80])
            fail += 1
            break
        dim_c[parts[2]] += 1
        src_c[parts[3]] += 1
    ok = True
    if len(rows) != n:
        print("COUNT", lid, "header", n, "rows", len(rows))
        ok = False
    if "需规原文" not in text:
        print("NO_SPEC", lid)
        ok = False
    if "| 需规描述 |" in text:
        print("SPEC_IN_TABLE", lid)
        ok = False
    if dim_h:
        declared = {}
        for part in dim_h.group(1).split("、"):
            mm = re.match(r"(\S+)\s+(\d+)$", part.strip())
            if mm:
                declared[mm.group(1)] = int(mm.group(2))
        if declared != dict(dim_c):
            print("DIM", lid, "header", declared, "rows", dict(dim_c))
            ok = False
        if sum(declared.values()) != n:
            print("DIM_SUM", lid)
            ok = False
    if src_h:
        declared = {}
        for part in src_h.group(1).split("、"):
            mm = re.match(r"(\S+)\s+(\d+)$", part.strip())
            if mm:
                declared[mm.group(1)] = int(mm.group(2))
        if declared != dict(src_c):
            print("SRC", lid, "header", declared, "rows", dict(src_c))
            ok = False
        if sum(declared.values()) != n:
            print("SRC_SUM", lid)
            ok = False
    if not r.exists():
        print("MISSING_REVIEW", lid)
        ok = False
    else:
        rt = r.read_text(encoding="utf-8")
        if "需返工" in rt and "通过" not in rt:
            print("REVIEW_FAIL", lid)
            ok = False
        if "误用" in rt and ("是" in rt.split("误用")[-1][:40] and "否" not in rt.split("误用")[-1][:80]):
            pass
        if "是否误用" in rt and "否" not in rt:
            print("REVIEW_PROTO", lid)
            ok = False
    status = "OK" if ok else "FAIL"
    if not ok:
        fail += 1
    print(status, lid, "n=", n)
print("fail", fail)
raise SystemExit(1 if fail else 0)

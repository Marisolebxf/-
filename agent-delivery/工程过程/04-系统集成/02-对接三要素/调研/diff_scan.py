# -*- coding: utf-8 -*-
"""Diff the fresh scan (_raw_schema.json) against HEAD's snapshot in git.

Usage: python diff_scan.py [repo_root]
Prints added/removed tables, row changes, column changes.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE
GIT_PATH = "agent-delivery/工程过程/04-系统集成/02-对接三要素/调研/_raw_schema.json"


def main():
    blob = subprocess.run(
        ["git", "-C", str(REPO), "show", f"HEAD:{GIT_PATH}"],
        capture_output=True, check=True,
    ).stdout
    old = json.loads(blob.decode("utf-8"))
    new = json.loads((HERE / "_raw_schema.json").read_text(encoding="utf-8"))
    ot = {t["table"]: t for t in old["tables"]}
    nt = {t["table"]: t for t in new["tables"]}
    added = sorted(set(nt) - set(ot))
    removed = sorted(set(ot) - set(nt))
    print("old", len(ot), "tables,", len(old["columns"]), "cols,",
          sum(t["table_rows"] or 0 for t in old["tables"]), "rows")
    print("new", len(nt), "tables,", len(new["columns"]), "cols,",
          sum(t["table_rows"] or 0 for t in new["tables"]), "rows")
    print("added", len(added))
    for t in added:
        print(" +", t, nt[t]["table_rows"])
    print("removed", len(removed))
    for t in removed:
        print(" -", t, ot[t]["table_rows"])
    chg = [(t, ot[t]["table_rows"] or 0, nt[t]["table_rows"] or 0)
           for t in nt if t in ot and (ot[t]["table_rows"] or 0) != (nt[t]["table_rows"] or 0)]
    print("row-changed", len(chg))
    for t, a, b in sorted(chg, key=lambda r: -(r[2] - r[1]))[:30]:
        print(" ~", t, a, "->", b)
    oc = {}
    for c in old["columns"]:
        oc.setdefault(c["table"], set()).add(c["column"])
    nc = {}
    for c in new["columns"]:
        nc.setdefault(c["table"], set()).add(c["column"])
    coldiff = [(t, sorted(nc[t] - oc.get(t, set())), sorted(oc.get(t, set()) - nc[t]))
               for t in nt if t in oc and nc[t] != oc.get(t, set())]
    print("col-changed", len(coldiff))
    for t, addc, delc in coldiff:
        print(" *", t, "+", addc, "-", delc)
    return 0


if __name__ == "__main__":
    sys.exit(main())

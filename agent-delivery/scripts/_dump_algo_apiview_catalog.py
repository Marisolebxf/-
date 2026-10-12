# -*- coding: utf-8 -*-
"""Dump lumen-ui-algo-apiview catalog pages for by-api prep. Read-only."""
from __future__ import annotations

import json
import subprocess
from collections import Counter
from pathlib import Path

CAT = Path(r"d:/work/gkx-lumen/repos/lumen-ui-algo-apiview/src/catalog")
REPO = CAT.parents[1]
OUT = Path(__file__).resolve().parents[1] / "qa/total-set/KJZTFWALGO/fp-split-by-api-run/_catalog-snapshot.md"


def git_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True
        ).strip()
    except Exception:
        return "UNKNOWN"


def main() -> None:
    sha = git_sha()
    lines = [
        "# 联调台 catalog 快照（by-api 接口真源）",
        "",
        f"- git SHA：`{sha}`",
        "- 仓：`repos/lumen-ui-algo-apiview`",
        "- 路径：`src/catalog/{entan,chain,policy,svc,comp,innov}.json`",
        "- 本文件由 `scripts/_dump_algo_apiview_catalog.py` 生成；拆点前再跑一次，SHA 变了要更新原则稿冻结值",
        "",
    ]
    st = Counter()
    rt = Counter()
    n_ep = 0
    n_page = 0
    unique_path: set[str] = set()
    for name in ("entan", "chain", "policy", "svc", "comp", "innov"):
        pages = json.loads((CAT / f"{name}.json").read_text(encoding="utf-8"))
        n_page += len(pages)
        lines.append(f"## {name}（{len(pages)} 页）")
        lines.append("")
        lines.append("| id | title | menuPath | endpoints | running | unavailable | local_mock |")
        lines.append("|---|---|---|---:|---:|---:|---:|")
        for p in pages:
            eps = p.get("endpoints") or []
            n_ep += len(eps)
            run = unavail = mock = 0
            paths = []
            for e in eps:
                st[e.get("status") or ""] += 1
                rt[e.get("runtime") or ""] += 1
                if e.get("status") == "running":
                    run += 1
                if e.get("status") == "unavailable":
                    unavail += 1
                if e.get("runtime") == "local_mock":
                    mock += 1
                key = f"{e.get('method', 'GET')} {e.get('path') or ''}"
                unique_path.add(key)
                paths.append(key)
            lines.append(
                f"| `{p.get('id')}` | {p.get('title') or ''} | `{p.get('menuPath')}` | "
                f"{len(eps)} | {run} | {unavail} | {mock} |"
            )
            for x in paths:
                lines.append(f"| | `{x}` | | | | | |")
        lines.append("")
    lines.append("## 合计")
    lines.append("")
    lines.append(f"- 页：{n_page}")
    lines.append(f"- endpoint 声明：{n_ep}")
    lines.append(f"- 唯一 METHOD+path：{len(unique_path)}")
    lines.append(f"- status：{dict(st)}")
    lines.append(f"- runtime：{dict(rt)}")
    lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} pages={n_page} eps={n_ep} unique={len(unique_path)}")


if __name__ == "__main__":
    main()

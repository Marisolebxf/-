#!/usr/bin/env python3
"""Compare FUNC case-book rows vs as-built cases/*.yaml (KJZTFWXT default).

Usage (from gkx-orchestration root):
  python3 agent-delivery/qa/as-built/tools/gap-func-vs-scripts.py --system KJZTFWXT --write
  # --write 默认附带健康扫描 + 派单队列（缺口∪回炉）；只要缺口加 --no-health
"""
from __future__ import annotations

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # agent-delivery/
QA = ROOT / "qa"
AS_BUILT = QA / "as-built"
SCRIPTS = AS_BUILT / "scripts"
CASES = QA / "test-cases"

# entry_id -> (func book relative under test-cases/{system}, scripts relative under scripts/{system})
KJZTFWXT_MAP: list[tuple[str, str, str]] = [
    ("ent-search", "enterprise-企业分析/SEARCH-企业查询", "enterprise/search"),
    ("ent-key-type", "enterprise-企业分析/KEYENT-重点企业类型分析", "enterprise/key-type"),
    ("ent-key-domain", "enterprise-企业分析/KEYDOM-重点企业领域分析", "enterprise/key-domain"),
    ("ent-eval-tech", "enterprise-企业分析/EVALTECH-企业技术力评估对比分析", "enterprise/eval-tech"),
    ("ent-eval-business", "enterprise-企业分析/EVALBIZ-企业商业力评估对比分析", "enterprise/eval-business"),
    ("ent-eval-compete", "enterprise-企业分析/EVALCOMP-企业综合竞争力评估", "enterprise/eval-compete"),
    ("ent-sz-status", "enterprise-企业分析/SZSTATUS-深圳企业现状分析", "enterprise/sz-status"),
    ("ent-attract", "enterprise-企业分析/ATTRACT-招引企业推荐分析", "enterprise/attract"),
    ("ent-cultivate", "enterprise-企业分析/CULTIVATE-培育企业推荐分析", "enterprise/cultivate"),
    ("ent-supply", "enterprise-企业分析/SUPPLY-企业供应链关系分析", "enterprise/supply"),
    ("ent-pain", "enterprise-企业分析/PAIN-企业发展痛难点分析", "enterprise/pain"),
    ("shell-compare-basket", "enterprise-企业分析/COMPARE-对比篮", "shell/compare-basket"),
    ("chain-overview", "industry-center-产业链分析/OVERVIEW-专题全景", "industry-center/overview"),
    ("chain-search", "industry-center-产业链分析/CHAINSEARCH-产业查询", "industry-center/search"),
    ("chain-panorama", "industry-center-产业链分析/PANORAMA-产业链全景图谱", "industry-center/panorama"),
    ("chain-cycle", "industry-center-产业链分析/CYCLE-产业周期分析", "industry-center/cycle"),
    ("chain-regional-index", "industry-center-产业链分析/REGIDX-区域产业指数评价", "industry-center/regional-index"),
    ("chain-key-link", "industry-center-产业链分析/KEYLINK-产业关键环节识别", "industry-center/key-link"),
    ("chain-bottleneck", "industry-center-产业链分析/BOTTLENECK-产业瓶颈堵点识别", "industry-center/bottleneck"),
    ("chain-sz-compare", "industry-center-产业链分析/SZCMP-深圳产业情况分析对比", "industry-center/sz-compare"),
    ("chain-sz-dev", "industry-center-产业链分析/SZDEV-深圳产业发展分析", "industry-center/sz-dev"),
    ("chain-regional-compete", "industry-center-产业链分析/REGCOMP-区域产业竞争力评价", "industry-center/regional-compete"),
    ("chain-maintenance", "industry-center-产业链分析/CHAINMAINT-维护管理", "industry-center/maintenance"),
    ("svc-portal", "service-产业服务链分析/SVCPORTAL-专题服务门户", "service/portal"),
    ("svc-search", "service-产业服务链分析/SVCSEARCH-服务机构查询", "service/search"),
    ("svc-org-field", "service-产业服务链分析/SVCFIELD-服务机构产业领域分析", "service/org-field"),
    ("svc-org-trend", "service-产业服务链分析/SVCTREND-服务机构新增趋势分析", "service/org-trend"),
    ("svc-org-capability", "service-产业服务链分析/SVCCAP-服务机构技术力评估分析", "service/org-capability"),
    ("svc-chain-shortboard", "service-产业服务链分析/SVCSHORT-服务链短板分析", "service/chain-shortboard"),
    ("svc-chain-graph", "service-产业服务链分析/SVCGRAPH-服务链图谱分析", "service/chain-graph"),
    ("svc-rec-attract", "service-产业服务链分析/SVCATTR-引入服务机构推荐分析", "service/rec-attract"),
    ("svc-rec-cultivate", "service-产业服务链分析/SVCCULT-培育服务机构推荐分析", "service/rec-cultivate"),
    ("svc-sz", "service-产业服务链分析/SVCSZ-深圳服务链现状分析", "service/sz"),
    ("svc-maintenance", "service-产业服务链分析/SVCMAINT-维护管理", "service/maintenance"),
    ("ent-detail", "enterprise-企业分析/DETAIL-企业详情", "enterprise/detail"),
    ("chain-result-deep", "industry-center-产业链分析/RESULTDEEP-产业链分析结果深链", "industry-center/result-deep"),
    ("chain-report-deep", "industry-center-产业链分析/REPORTDEEP-产业链分析报告深链", "industry-center/report-deep"),
    ("svc-portal-industry", "service-产业服务链分析/SVCINDDIST-服务机构产业分布", "service/portal-industry"),
    ("svc-portal-region", "service-产业服务链分析/SVCREGION-服务机构区域分布", "service/portal-region"),
    ("svc-portal-capability", "service-产业服务链分析/SVCCAPRANK-服务机构技术能力", "service/portal-capability"),
    ("svc-portal-shenzhen", "service-产业服务链分析/SVCSZINTRO-深圳产业服务介绍", "service/portal-shenzhen"),
]

MAPS = {"KJZTFWXT": KJZTFWXT_MAP}
FUNC_RE = re.compile(r"^ZNFWJQ-[A-Z0-9/-]+-FUNC-\d{5}\b")
FUNC_ID_LINE = re.compile(r"^func_id:\s*(\S+)", re.M)


def find_func_md(system: str, book_rel: str) -> Path | None:
    d = CASES / system / book_rel
    if not d.is_dir():
        return None
    mds = sorted(d.glob("FUNC-*.md"))
    return mds[0] if mds else None


def parse_func_ids(md: Path) -> list[str]:
    ids: list[str] = []
    for line in md.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip().startswith("|"):
            continue
        if re.match(r"^\|\s*[-:]+", line):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells:
            continue
        first = cells[0]
        if FUNC_RE.match(first) or first.startswith("ZNFWJQ-"):
            ids.append(first.split()[0])
    return ids


def parse_script_func_ids(cases_dir: Path) -> dict[str, str]:
    """func_id -> case file stem."""
    out: dict[str, str] = {}
    if not cases_dir.is_dir():
        return out
    for f in cases_dir.glob("*.yaml"):
        text = f.read_text(encoding="utf-8", errors="replace")
        m = FUNC_ID_LINE.search(text)
        if m:
            out[m.group(1)] = f.stem
        else:
            # fallback: unmatched file still counts as a script slot
            out[f"__no_func_id__:{f.stem}"] = f.stem
    return out


def next_case_ids(existing: set[str], n: int, prefix: str = "P0") -> list[str]:
    used = set()
    for stem in existing:
        m = re.match(r"^(P[01])-(\d+)$", stem)
        if m:
            used.add((m.group(1), int(m.group(2))))
    out = []
    num = 1
    while len(out) < n:
        cand = f"{prefix}-{num:02d}"
        key = (prefix, num)
        if cand not in existing and key not in used:
            out.append(cand)
            used.add(key)
        num += 1
        if num > 500:
            break
    return out


def build_report(system: str) -> tuple[str, list[dict]]:
    mapping = MAPS.get(system)
    if not mapping:
        raise SystemExit(f"unsupported system {system}; known: {list(MAPS)}")

    rows: list[dict] = []
    for entry_id, book_rel, script_rel in mapping:
        md = find_func_md(system, book_rel)
        func_ids = parse_func_ids(md) if md else []
        cases_dir = SCRIPTS / system / script_rel / "cases"
        script_map = parse_script_func_ids(cases_dir)
        covered = {fid for fid in func_ids if fid in script_map}
        missing = [fid for fid in func_ids if fid not in script_map]
        existing_stems = set(script_map.values())
        suggested = next_case_ids(existing_stems, len(missing))
        rows.append(
            {
                "entry_id": entry_id,
                "book": book_rel,
                "script_rel": script_rel,
                "func_md": str(md.relative_to(QA)) if md else "",
                "func_n": len(func_ids),
                "script_n": len(list(cases_dir.glob("*.yaml"))) if cases_dir.is_dir() else 0,
                "covered": len(covered),
                "gap": len(missing),
                "missing": missing,
                "suggested": suggested,
            }
        )

    total_f = sum(r["func_n"] for r in rows)
    total_s = sum(r["script_n"] for r in rows)
    total_g = sum(r["gap"] for r in rows)
    now = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M %Z")

    lines = [
        f"# 脚本缺口快照 · {system}",
        "",
        f"> 由 `tools/gap-func-vs-scripts.py` 生成 · {now}",
        f"> 勿手改正文；重跑工具覆写。编排见 `script-backfill-playbook.md`。",
        "",
        f"| 指标 | 值 |",
        f"|------|----|",
        f"| FUNC 行合计 | {total_f} |",
        f"| 脚本文件合计 | {total_s} |",
        f"| 缺口（无 func_id 命中） | **{total_g}** |",
        f"| 有缺口入口 | {sum(1 for r in rows if r['gap'])} / {len(rows)} |",
        "",
        "## 按入口",
        "",
        "| entry_id | FUNC | scripts | gap | 脚本目录 |",
        "|----------|------|---------|-----|----------|",
    ]
    for r in sorted(rows, key=lambda x: (-x["gap"], x["entry_id"])):
        lines.append(
            f"| `{r['entry_id']}` | {r['func_n']} | {r['script_n']} | {r['gap']} | `{r['script_rel']}` |"
        )

    lines.extend(["", "## 缺口明细（供派单）", ""])
    for r in sorted(rows, key=lambda x: -x["gap"]):
        if not r["gap"]:
            continue
        lines.append(f"### `{r['entry_id']}` · 缺 {r['gap']}")
        lines.append("")
        lines.append(f"- 用例册：`{r['func_md']}`")
        lines.append(f"- 脚本目录：`scripts/{system}/{r['script_rel']}/`")
        lines.append("")
        lines.append("| FUNC_ID | 建议 scripts id |")
        lines.append("|---------|-----------------|")
        for fid, sid in zip(r["missing"], r["suggested"]):
            lines.append(f"| `{fid}` | `{sid}` |")
        lines.append("")

    lines.extend(
        [
            "## 已对齐入口",
            "",
            ", ".join(f"`{r['entry_id']}`" for r in rows if r["gap"] == 0) or "_无_",
            "",
        ]
    )
    return "\n".join(lines) + "\n", rows


def _run_health(system: str) -> list[dict]:
    """Invoke sibling health-cases.py and return findings (also writes health md)."""
    health_py = Path(__file__).with_name("health-cases.py")
    # import in-process to avoid double YAML path issues
    from importlib.util import module_from_spec, spec_from_file_location

    spec = spec_from_file_location("health_cases", health_py)
    mod = module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    _text, findings = mod.build_report(system)
    out = AS_BUILT / f"script-backfill-health-{system}.md"
    out.write_text(_text, encoding="utf-8")
    print(f"wrote {out}")
    return findings


def build_queue(system: str, gap_rows: list[dict], health: list[dict]) -> str:
    """合并：回炉优先，再缺口新写；同一 CASE_ID 只出现一次。"""
    now = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M %Z")
    lines = [
        f"# 脚本补齐派单队列 · {system}",
        "",
        f"> 由 `gap-func-vs-scripts.py --write` 生成 · {now}",
        f"> **回炉优先于新写**；同一 CASE_ID 去重。父按本表「一行一派」。",
        "",
        "| # | kind | entry_id | CASE_ID | FUNC_ID | note |",
        "|---|------|----------|---------|---------|------|",
    ]
    seen_case: set[tuple[str, str]] = set()
    n = 0
    # 1) rework
    for f in sorted(health, key=lambda x: (x["entry_id"], x["case_id"])):
        key = (f["entry_id"], f["case_id"])
        if key in seen_case:
            continue
        seen_case.add(key)
        n += 1
        lines.append(
            f"| {n} | `REWORK` | `{f['entry_id']}` | `{f['case_id']}` | "
            f"`{f['func_id'] or '—'}` | {', '.join(f['reasons'])} |"
        )
    # 2) gap
    for r in sorted(gap_rows, key=lambda x: -x["gap"]):
        for fid, sid in zip(r["missing"], r["suggested"]):
            key = (r["entry_id"], sid)
            if key in seen_case:
                continue
            seen_case.add(key)
            n += 1
            lines.append(
                f"| {n} | `GAP` | `{r['entry_id']}` | `{sid}` | `{fid}` | 缺脚本 |"
            )
    lines.extend(
        [
            "",
            f"**队列长度**：{n}（REWORK={len(health)} 原始命中；GAP 行见 gap 快照）",
            "",
            "## 父派单用法",
            "",
            "2026-10-19 起专题脚本重写**不按本队列派单**。派单真源是 `script-rewrite-ledger-KJZTFWXT.csv`，见 `script-backfill-playbook.md` 文首「重写波」。",
            "本文件只作缺口快照。旧 `cases/P0-*.yaml` 即使 `func_id` 对上，也不算重写完成。",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--system", default="KJZTFWXT")
    ap.add_argument(
        "--write",
        action="store_true",
        help="write gap + health + queue markdown under as-built/",
    )
    ap.add_argument(
        "--no-health",
        action="store_true",
        help="with --write, skip health scan / queue merge",
    )
    args = ap.parse_args()
    text, rows = build_report(args.system)
    total_g = sum(r["gap"] for r in rows)
    print(
        f"{args.system}: FUNC={sum(r['func_n'] for r in rows)} "
        f"scripts={sum(r['script_n'] for r in rows)} gap={total_g}"
    )
    for r in sorted(rows, key=lambda x: -x["gap"]):
        if r["gap"]:
            print(
                f"  {r['entry_id']:28} gap={r['gap']:3}  "
                f"func={r['func_n']:3} scripts={r['script_n']:3}"
            )
    if args.write:
        out = AS_BUILT / f"script-backfill-gap-{args.system}.md"
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
        if not args.no_health:
            health = _run_health(args.system)
            print(f"{args.system}: health rework={len(health)}")
            qpath = AS_BUILT / f"script-backfill-queue-{args.system}.md"
            qpath.write_text(build_queue(args.system, rows, health), encoding="utf-8")
            print(f"wrote {qpath}")


if __name__ == "__main__":
    main()

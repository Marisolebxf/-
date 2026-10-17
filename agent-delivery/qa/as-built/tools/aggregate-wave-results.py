#!/usr/bin/env python3
"""Aggregate a wave run directory into results.xlsx (+ optional JSON).

Usage (from gkx-orchestration root or any cwd):
  python3 agent-delivery/qa/as-built/tools/aggregate-wave-results.py \\
    --wave agent-delivery/qa/as-built/runs/20261015-50892-smoke-r1 --write
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

SEVERITY = {
    "C1": "高",
    "C2": "中",
    "C3": "—",
    "C4": "中",
    "C5": "阻塞",
    "C6": "高",
}

# script-batch-run-playbook.md §6.2；Excel「失败分类」列输出为「编号-名称」
FAIL_CLASS_LABEL = {
    "C1": "产品/代码缺陷",
    "C2": "发布/环境",
    "C3": "白名单空态",
    "C4": "用例/脚本错",
    "C5": "结构/库闸",
    "C6": "未知/待分诊",
}

# qa-test-case-spec.md §5.1 交付 17 列（与 _gen_zt_delivery_func_v2.py 一致）
DELIVERY_COLS = [
    "用例编号",
    "功能模块",
    "子功能模块",
    "功能项",
    "子功能项",
    "页面",
    "功能点",
    "测试内容",
    "前置条件",
    "测试步骤",
    "预期结果",
    "优先级",
    "是否通过",
    "测试工程师",
    "测试时间",
    "审核员",
    "测试截图",
]

EXEC_JOIN_COLS = [
    "脚本ID",
    "功能入口",
    "通过情况",
    "失败原因",
    "失败分类",
    "严重程度",
    "BUG编号",
    "证据路径",
    "traceId",
]

CASEBOOK_ROW_RE = re.compile(r"^\|\s*ZNFWJQ-KJZTFWXT-v1\.0-FUNC-\d{5}\s*\|")
CASEBOOK_GRP_ORDER = [
    "enterprise-企业分析",
    "industry-center-产业链分析",
    "service-产业服务链分析",
]


def format_fail_class(code: str) -> str:
    c = normalize_fail_class(code)
    if not c:
        return ""
    label = FAIL_CLASS_LABEL.get(c)
    return f"{c}-{label}" if label else c


def normalize_fail_class(raw: str) -> str:
    if not raw:
        return ""
    s = str(raw).strip().upper()
    m = re.match(r"^(C[1-6])\b", s)
    if m:
        return m.group(1)
    if s in FAIL_CLASS_LABEL:
        return s
    return ""


def evidence_path_from_runs(wave: Path, case_dir: Path) -> str:
    rel = case_dir.relative_to(wave)
    return f"runs/{wave.name}/{rel.as_posix()}"


def load_feature_titles(catalog_path: Path) -> dict[str, str]:
    """Map catalog scripts rel path (enterprise/search) → 中文 title."""
    if not catalog_path.is_file() or not yaml:
        return {}
    data = yaml.safe_load(catalog_path.read_text(encoding="utf-8")) or {}
    out: dict[str, str] = {}
    for entry in data.get("entries") or []:
        if not isinstance(entry, dict):
            continue
        scripts = str(entry.get("scripts") or "")
        m = re.search(r"scripts/KJZTFWXT/(.+?)/?\s*$", scripts)
        if not m:
            continue
        rel = m.group(1).strip("/")
        title = entry.get("title") or entry.get("id") or rel
        out[rel] = str(title)
    return out


def resolve_entry_title(feat_dir: Path, feat_label: str, feature_titles: dict[str, str]) -> str:
    meta = feat_dir / "meta.yaml"
    if meta.is_file():
        doc = load_yaml(meta) or {}
        feature = str(doc.get("feature") or "").strip("/")
        if feature and feature in feature_titles:
            return feature_titles[feature]
    # run-dir 名 enterprise-search → enterprise/search
    guess = feat_label.replace("-", "/", 1) if "-" in feat_label else feat_label
    if guess in feature_titles:
        return feature_titles[guess]
    return feat_label


def load_yaml(path: Path):
    text = path.read_text(encoding="utf-8", errors="replace")
    if yaml:
        try:
            return yaml.safe_load(text)
        except Exception:
            pass
    # minimal fallback for result.yaml key: value
    out = {}
    for line in text.splitlines():
        m = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)
        if not m:
            continue
        k, v = m.group(1), m.group(2).strip()
        if v.startswith('"') and v.endswith('"'):
            v = v[1:-1]
        out[k] = v
    return out


def map_pass(verdict: str, actual: str) -> str:
    v = (verdict or "").lower()
    if v == "pass":
        if "待人工" in (actual or "") or "pending_manual" in (actual or "").lower():
            return "待人工"
        return "通过"
    if v == "fail":
        return "不通过"
    if v in ("n/a", "na"):
        return "跳过"
    if v == "blocked":
        return "阻塞"
    return verdict or "未知"


def guess_class(doc: dict) -> str:
    fc = doc.get("fail_class") or doc.get("failClass") or ""
    if fc:
        return str(fc).upper()
    actual = str(doc.get("actual") or "")
    for c in ("C1", "C2", "C3", "C4", "C5", "C6"):
        if c in actual:
            return c
    if (doc.get("verdict") or "").lower() == "fail":
        return "C6"
    return ""


def _collect_feat(
    wave: Path,
    feat_dir: Path,
    feat_label: str,
    feature_titles: dict[str, str],
) -> list[dict]:
    entry_title = resolve_entry_title(feat_dir, feat_label, feature_titles)
    rows: list[dict] = []
    scripts_root = feat_dir / "scripts"
    if not scripts_root.is_dir():
        return rows
    for case_dir in sorted(scripts_root.iterdir()):
        if not case_dir.is_dir():
            continue
        result = case_dir / "result.yaml"
        if not result.exists():
            rows.append(
                {
                    "用例编号": "",
                    "用例描述": "",
                    "脚本ID": case_dir.name,
                    "功能入口": entry_title,
                    "通过情况": "阻塞",
                    "失败原因": "缺少 result.yaml",
                    "失败分类": format_fail_class("C6"),
                    "严重程度": "高",
                    "BUG编号": "",
                    "证据路径": evidence_path_from_runs(wave, case_dir),
                    "traceId": "",
                }
            )
            continue
        doc = load_yaml(result) or {}
        func_id = doc.get("func_id") or ""
        title = doc.get("title") or ""
        case_id = doc.get("case_id") or doc.get("id") or case_dir.name
        verdict = str(doc.get("verdict") or "")
        actual = str(doc.get("actual") or "")
        if not title:
            summary = feat_dir / "SUMMARY.md"
            if summary.exists():
                for line in summary.read_text(encoding="utf-8", errors="replace").splitlines():
                    if not line.startswith("|"):
                        continue
                    cells = [c.strip() for c in line.strip("|").split("|")]
                    if cells and cells[0] == str(case_id) and len(cells) >= 3:
                        title = cells[2]
                        break
        fc_code = guess_class(doc)
        status = map_pass(verdict, actual)
        rows.append(
            {
                "用例编号": func_id,
                "用例描述": title,
                "脚本ID": case_id,
                "功能入口": entry_title,
                "通过情况": status,
                "失败原因": actual if status in ("不通过", "阻塞", "跳过", "待人工") else "",
                "失败分类": format_fail_class(fc_code) if status in ("不通过", "阻塞") else "",
                "严重程度": SEVERITY.get(fc_code, "") if status in ("不通过", "阻塞") else "",
                "BUG编号": doc.get("bug_id") or "",
                "证据路径": evidence_path_from_runs(wave, case_dir),
                "traceId": doc.get("trace_id") or doc.get("traceId") or "",
            }
        )
    return rows


def collect_wave(wave: Path, feature_titles: dict[str, str]) -> list[dict]:
    # 新布局：WAVE/<feat>/scripts/；旧平铺：WAVE/scripts/
    if (wave / "scripts").is_dir():
        return _collect_feat(wave, wave, wave.name, feature_titles)
    rows: list[dict] = []
    for feat_dir in sorted(p for p in wave.iterdir() if p.is_dir()):
        if feat_dir.name in ("scripts",):
            continue
        rows.extend(_collect_feat(wave, feat_dir, feat_dir.name, feature_titles))
    return rows


def parse_func_md_booklet(booklet_dir: Path) -> list[dict]:
    """一册 FUNC-*.md → 行 dict（17 列 + 自动化用例ID 若有）。"""
    md_files = sorted(booklet_dir.glob("FUNC-*.md"))
    if len(md_files) != 1:
        return []
    out: list[dict] = []
    for line in md_files[0].read_text(encoding="utf-8").splitlines():
        if not CASEBOOK_ROW_RE.match(line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 17:
            continue
        row = {DELIVERY_COLS[i]: cells[i] for i in range(17)}
        if len(cells) >= 28:
            row["自动化用例ID"] = cells[27]
        else:
            row["自动化用例ID"] = ""
        out.append(row)
    return out


def load_bline_casebook(tc_root: Path) -> list[dict]:
    """B 线 KJZTFWXT 全库用例（与交付 v2 行序一致）。"""
    if not tc_root.is_dir():
        return []
    booklets: dict[str, list[tuple[int, list[dict]]]] = {g: [] for g in CASEBOOK_GRP_ORDER}
    global_rows: list[dict] = []
    for grp in tc_root.iterdir():
        if not grp.is_dir() or grp.name not in CASEBOOK_GRP_ORDER:
            continue
        for b in grp.iterdir():
            if not b.is_dir():
                continue
            rows = parse_func_md_booklet(b)
            if not rows:
                continue
            min_id = min(int(r["用例编号"].rsplit("-", 1)[1]) for r in rows)
            if all(r["功能模块"] == "全局功能" for r in rows):
                global_rows.extend(rows)
            else:
                booklets[grp.name].append((min_id, rows))
    ordered: list[dict] = []
    for g in CASEBOOK_GRP_ORDER:
        for _, rows in sorted(booklets[g], key=lambda t: t[0]):
            ordered.extend(rows)
    ordered.extend(global_rows)
    return ordered


def _exec_slice(row: dict) -> dict:
    return {c: row.get(c, "") for c in EXEC_JOIN_COLS}


def _unscripted(auto_id: str) -> bool:
    s = (auto_id or "").strip()
    return s in ("", "—", "-", "—")


def merge_casebook_exec(casebook: list[dict], exec_rows: list[dict]) -> list[dict]:
    """B 线用例左连接执行结果（func_id）；无执行时标未脚本化/未执行。"""
    by_func: dict[str, list[dict]] = {}
    for r in exec_rows:
        fid = str(r.get("用例编号") or "").strip()
        if not fid:
            continue
        by_func.setdefault(fid, []).append(r)

    merged: list[dict] = []
    seen_exec_keys: set[tuple[str, str]] = set()

    for case in casebook:
        fid = case["用例编号"]
        execs = by_func.get(fid, [])
        if not execs:
            ex = {c: "" for c in EXEC_JOIN_COLS}
            if _unscripted(case.get("自动化用例ID", "")):
                ex["通过情况"] = "未脚本化"
            else:
                ex["通过情况"] = "未执行"
            merged.append({**case, **ex})
            continue
        for ex_row in execs:
            seen_exec_keys.add((fid, str(ex_row.get("脚本ID") or "")))
            merged.append({**case, **_exec_slice(ex_row)})

    for r in exec_rows:
        fid = str(r.get("用例编号") or "").strip()
        key = (fid, str(r.get("脚本ID") or ""))
        if fid and key not in seen_exec_keys:
            blank = {c: "" for c in DELIVERY_COLS}
            blank["用例编号"] = fid
            merged.append({**blank, **_exec_slice(r)})

    return merged


def enrich_from_scripts(rows: list[dict], scripts_root: Path | None) -> None:
    """Fill empty func_id/title from as-built cases if --scripts-root given."""
    if not scripts_root or not scripts_root.is_dir():
        return
    # build map: (feat_basename or path end) — weak match by walking all cases
    by_id: dict[str, tuple[str, str]] = {}
    for f in scripts_root.rglob("cases/*.yaml"):
        text = f.read_text(encoding="utf-8", errors="replace")
        mid = re.search(r"^id:\s*(\S+)", text, re.M)
        mfunc = re.search(r"^func_id:\s*(\S+)", text, re.M)
        mtitle = re.search(r"^title:\s*[\"']?(.*)[\"']?\s*$", text, re.M)
        if mid:
            by_id[mid.group(1)] = (
                mfunc.group(1) if mfunc else "",
                (mtitle.group(1).strip().strip('"').strip("'") if mtitle else ""),
            )
    for r in rows:
        if r["用例编号"] and r["用例描述"]:
            continue
        meta = by_id.get(str(r["脚本ID"]))
        if not meta:
            continue
        if not r["用例编号"]:
            r["用例编号"] = meta[0]
        if not r["用例描述"]:
            r["用例描述"] = meta[1]


def write_xlsx(
    rows: list[dict],
    path: Path,
    casebook_merged: list[dict] | None = None,
) -> None:
    from openpyxl import Workbook

    cols = [
        "用例编号",
        "用例描述",
        "脚本ID",
        "功能入口",
        "通过情况",
        "失败原因",
        "失败分类",
        "严重程度",
        "BUG编号",
        "证据路径",
        "traceId",
    ]
    wb = Workbook()
    ws = wb.active
    ws.title = "执行清单"
    ws.append(cols)
    for r in rows:
        ws.append([r.get(c, "") for c in cols])

    if casebook_merged:
        ws_cb = wb.create_sheet("B线用例+执行")
        cb_cols = DELIVERY_COLS + EXEC_JOIN_COLS
        ws_cb.append(cb_cols)
        for r in casebook_merged:
            ws_cb.append([r.get(c, "") for c in cb_cols])
        ws_cb2 = wb.create_sheet("B线汇总")
        cb_counts: dict[str, int] = {}
        for r in casebook_merged:
            st = r.get("通过情况") or "未知"
            cb_counts[st] = cb_counts.get(st, 0) + 1
        ws_cb2.append(["通过情况", "条数"])
        for k, v in sorted(cb_counts.items()):
            ws_cb2.append([k, v])
        ws_cb2.append([])
        ws_cb2.append(["总行数", len(casebook_merged)])

    # summary sheet（执行清单粒度）
    ws2 = wb.create_sheet("汇总")
    counts: dict[str, int] = {}
    for r in rows:
        counts[r["通过情况"]] = counts.get(r["通过情况"], 0) + 1
    ws2.append(["通过情况", "条数"])
    for k, v in sorted(counts.items()):
        ws2.append([k, v])
    ws2.append([])
    ws2.append(["总行数", len(rows)])
    wb.save(path)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--wave", required=True, help="wave run directory")
    ap.add_argument("--write", action="store_true", help="write results.xlsx + aggregate-raw.json")
    ap.add_argument(
        "--scripts-root",
        default="",
        help="optional as-built/scripts/{SYSTEM} to fill func_id/title",
    )
    ap.add_argument(
        "--casebook-scope",
        choices=("off", "bline-only"),
        default="off",
        help="off=仅执行清单；bline-only=追加 sheet「B线用例+执行」（17 列+执行列）",
    )
    args = ap.parse_args()
    wave = Path(args.wave).resolve()
    if not wave.is_dir():
        raise SystemExit(f"wave not found: {wave}")

    as_built = wave.parents[1]
    catalog_path = as_built / "catalog" / "KJZTFWXT.yaml"
    feature_titles = load_feature_titles(catalog_path)

    rows = collect_wave(wave, feature_titles)
    scripts_root = Path(args.scripts_root).resolve() if args.scripts_root else None
    if not scripts_root:
        # heuristic: …/as-built/runs/WAVE → …/as-built/scripts/KJZTFWXT
        cand = as_built / "scripts" / "KJZTFWXT"
        if cand.is_dir():
            scripts_root = cand
    enrich_from_scripts(rows, scripts_root)

    counts: dict[str, int] = {}
    for r in rows:
        counts[r["通过情况"]] = counts.get(r["通过情况"], 0) + 1
    print(f"wave={wave.name} rows={len(rows)} {counts}")

    casebook_merged: list[dict] | None = None
    if args.casebook_scope == "bline-only":
        qa_root = as_built.parent
        tc_root = qa_root / "test-cases" / "KJZTFWXT"
        casebook = load_bline_casebook(tc_root)
        if not casebook:
            raise SystemExit(f"casebook empty: {tc_root}")
        casebook_merged = merge_casebook_exec(casebook, rows)
        cb_counts: dict[str, int] = {}
        for r in casebook_merged:
            st = r.get("通过情况") or "未知"
            cb_counts[st] = cb_counts.get(st, 0) + 1
        print(f"casebook rows={len(casebook)} merged={len(casebook_merged)} {cb_counts}")

    if args.write:
        raw = wave / "aggregate-raw.json"
        raw.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
        xlsx = wave / "results.xlsx"
        write_xlsx(rows, xlsx, casebook_merged=casebook_merged)
        print(f"wrote {xlsx}")
        print(f"wrote {raw}")
        if casebook_merged is not None:
            side = wave / "results-casebook-merged.json"
            side.write_text(json.dumps(casebook_merged, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"wrote {side}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""导出「指标需求来源」完整 Excel（注册表全量 + srs_refs）。

不改飞书进度表列。不写 seed / 矩阵 / metric-srs-map.yaml。
空来源 = 尚未从 A1/A2 回填，不是「无需求」。seq 只在分册内唯一。

用法（仓根）：
  python agent-delivery/metrics/registry/export/export_metric_srs_board.py
  python agent-delivery/metrics/registry/export/export_metric_srs_board.py --json
MCP：metric-registry → metric-srs-export
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import date, datetime
from pathlib import Path

import yaml
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

EXPORT_DIR = Path(__file__).resolve().parent
REGISTRY_DIR = EXPORT_DIR.parent
OUT_XLSX = EXPORT_DIR / "指标需求来源.xlsx"

BOOK_ZH = {"02": "02 展示需规", "04": "04 专题需规", "05": "05 算法库需规"}
ROLE_ZH = {"algo_leaf": "算法库叶", "page_use": "页面使用"}
DEF_ZH = {"aligned": "已对齐", "draft": "草案", "missing": "未登记", "unassessed": "待评估"}
INGEST_ZH = {"mock": "Mock", "ingesting": "接入中", "live": "已接真", "n/a": "不适用"}

CATALOG_HEADERS = [
    "指标ID",
    "指标名",
    "模块",
    "算法类型",
    "D1定义",
    "D4接入",
    "需求来源条数",
    "需求回填",
    "主来源分册",
    "主来源序号",
    "主来源名称",
    "主来源简述",
    "主来源需规ID",
    "全部来源",
    "口径摘要",
    "更新日期",
]
DETAIL_HEADERS = [
    "指标ID",
    "指标名",
    "模块",
    "分册",
    "分册名称",
    "序号",
    "需规名称",
    "简要描述",
    "需规ID",
    "角色",
    "页面",
    "需规文件",
    "回填状态",
]
SUMMARY_HEADERS = ["项", "值"]

CATALOG_WIDTH = {
    "指标ID": 28,
    "指标名": 22,
    "模块": 12,
    "算法类型": 12,
    "D1定义": 10,
    "D4接入": 10,
    "需求来源条数": 14,
    "需求回填": 10,
    "主来源分册": 14,
    "主来源序号": 12,
    "主来源名称": 28,
    "主来源简述": 42,
    "主来源需规ID": 22,
    "全部来源": 48,
    "口径摘要": 42,
    "更新日期": 12,
}
DETAIL_WIDTH = {
    "指标ID": 28,
    "指标名": 22,
    "模块": 12,
    "分册": 8,
    "分册名称": 16,
    "序号": 10,
    "需规名称": 28,
    "简要描述": 42,
    "需规ID": 22,
    "角色": 12,
    "页面": 28,
    "需规文件": 48,
    "回填状态": 10,
}
WRAP = {"主来源简述", "全部来源", "口径摘要", "简要描述", "需规文件", "值"}


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def nz(v) -> str:
    if v is None:
        return ""
    return str(v).strip()


def book_of(v) -> str:
    s = nz(v)
    return s.zfill(2) if s.isdigit() else s


def clip(s: str, n: int) -> str:
    t = " ".join((s or "").split())
    return t if len(t) <= n else t[:n] + "…"


def domain_from_seed_name(name: str) -> str:
    m = re.match(r"cfg_metric-(.+)-seed\.yaml$", name)
    return m.group(1) if m else ""


def domain_from_matrix_name(name: str) -> str:
    m = re.match(r"metric-readiness-matrix-(.+)\.yaml$", name)
    return m.group(1) if m else ""


def parse_catalog() -> dict[str, dict]:
    by_id: dict[str, dict] = {}

    def ensure(mid: str) -> dict:
        if mid not in by_id:
            by_id[mid] = {
                "metric_id": mid,
                "name": "",
                "domain": "",
                "algorithm_type": "UNKNOWN",
                "definition": "",
                "d1": "",
                "d4": "",
                "srs_refs": [],
            }
        return by_id[mid]

    for path in sorted(REGISTRY_DIR.glob("cfg_metric-*-seed.yaml")):
        domain = domain_from_seed_name(path.name)
        doc = load_yaml(path)
        for row in doc.get("metrics") or []:
            mid = nz(row.get("metric_id"))
            if not mid:
                continue
            rec = ensure(mid)
            rec["name"] = nz(row.get("metric_name_zh")) or rec["name"]
            rec["domain"] = domain or rec["domain"]
            algo = nz(row.get("algorithm_type")).upper() or "UNKNOWN"
            rec["algorithm_type"] = algo
            rec["definition"] = nz(row.get("definition")) or rec["definition"]

    for path in sorted(REGISTRY_DIR.glob("metric-readiness-matrix-*.yaml")):
        domain = domain_from_matrix_name(path.name)
        doc = load_yaml(path)
        file_module = nz(doc.get("module")) or domain
        for row in doc.get("metrics") or []:
            mid = nz(row.get("metric_id"))
            if not mid:
                continue
            rec = ensure(mid)
            rec["name"] = nz(row.get("metric_name_zh")) or rec["name"]
            rec["domain"] = nz(row.get("module")) or file_module or rec["domain"]
            rec["d1"] = nz(row.get("d1_def_status")) or rec["d1"]
            rec["d4"] = nz(row.get("d4_ingestion_status")) or rec["d4"]

    srs_path = REGISTRY_DIR / "metric-srs-map.yaml"
    if srs_path.exists():
        doc = load_yaml(srs_path)
        for row in doc.get("metrics") or []:
            mid = nz(row.get("metric_id"))
            if mid not in by_id:
                continue
            refs = row.get("srs_refs") or []
            if isinstance(refs, list):
                by_id[mid]["srs_refs"] = refs
    return by_id


def primary_ref(refs: list) -> dict:
    if not refs:
        return {}
    for r in refs:
        if isinstance(r, dict) and nz(r.get("role")) == "algo_leaf":
            return r
    return refs[0] if isinstance(refs[0], dict) else {}


def book_zh(book: str) -> str:
    return BOOK_ZH.get(str(book), str(book or ""))


def fmt_all(refs: list) -> str:
    parts = []
    for r in refs:
        if not isinstance(r, dict):
            continue
        book = book_of(r.get("book"))
        seq = nz(r.get("seq"))
        name = nz(r.get("name"))
        token = f"{book}·{seq}" if book or seq else ""
        parts.append(" ".join(x for x in (token, name) if x))
    return " | ".join(parts)


def pages_of(ref: dict) -> str:
    ids = ref.get("page_ids") or ref.get("pages") or []
    if isinstance(ids, list):
        return ", ".join(nz(x) for x in ids if nz(x))
    return nz(ids)


def build_tables(by_id: dict[str, dict]) -> tuple[list[dict], list[dict]]:
    today = date.today().isoformat()
    catalog = []
    detail = []
    for mid in sorted(by_id):
        rec = by_id[mid]
        refs = [r for r in (rec.get("srs_refs") or []) if isinstance(r, dict)]
        pri = primary_ref(refs)
        filled = "已回填" if refs else "未回填"
        catalog.append(
            {
                "指标ID": mid,
                "指标名": rec["name"] or mid,
                "模块": rec["domain"],
                "算法类型": rec["algorithm_type"] or "UNKNOWN",
                "D1定义": DEF_ZH.get(rec["d1"], rec["d1"] or "—"),
                "D4接入": INGEST_ZH.get(rec["d4"], rec["d4"] or "—"),
                "需求来源条数": len(refs),
                "需求回填": filled,
                "主来源分册": book_zh(book_of(pri.get("book"))) if pri else "",
                "主来源序号": pri.get("seq") if pri else "",
                "主来源名称": nz(pri.get("name")),
                "主来源简述": clip(nz(pri.get("brief")), 160),
                "主来源需规ID": nz(pri.get("requirement_id")),
                "全部来源": fmt_all(refs),
                "口径摘要": clip(rec["definition"], 120),
                "更新日期": today,
            }
        )
        if not refs:
            detail.append(
                {
                    "指标ID": mid,
                    "指标名": rec["name"] or mid,
                    "模块": rec["domain"],
                    "分册": "",
                    "分册名称": "",
                    "序号": "",
                    "需规名称": "",
                    "简要描述": "",
                    "需规ID": "",
                    "角色": "",
                    "页面": "",
                    "需规文件": "",
                    "回填状态": "未回填",
                }
            )
            continue
        for r in refs:
            book = book_of(r.get("book"))
            detail.append(
                {
                    "指标ID": mid,
                    "指标名": rec["name"] or mid,
                    "模块": rec["domain"],
                    "分册": book,
                    "分册名称": book_zh(book),
                    "序号": r.get("seq", ""),
                    "需规名称": nz(r.get("name")),
                    "简要描述": clip(nz(r.get("brief")), 200),
                    "需规ID": nz(r.get("requirement_id")),
                    "角色": ROLE_ZH.get(nz(r.get("role")), nz(r.get("role"))),
                    "页面": pages_of(r),
                    "需规文件": nz(r.get("file")),
                    "回填状态": "已回填",
                }
            )
    return catalog, detail


def style_header(ws, headers, widths):
    fill = PatternFill("solid", fgColor="165DFF")
    font = Font(name="Calibri", color="FFFFFF", bold=True, size=11)
    wrap = Alignment(wrap_text=True, vertical="center")
    top = Alignment(vertical="center")
    body = Font(name="Calibri", size=11)
    for cell in ws[1]:
        cell.fill = fill
        cell.font = font
        cell.alignment = wrap
    if ws.max_row >= 2:
        for r in ws.iter_rows(min_row=2, max_row=ws.max_row, max_col=len(headers)):
            for cell in r:
                cell.font = body
                header = headers[cell.column - 1]
                cell.alignment = wrap if header in WRAP else top
    for i, name in enumerate(headers, 1):
        ws.column_dimensions[get_column_letter(i)].width = widths.get(name, 14)
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{max(ws.max_row, 1)}"
    ws.freeze_panes = "A2"
    ws.row_dimensions[1].height = 22


def add_table(ws, name, headers):
    if ws.max_row < 2:
        return
    ref = f"A1:{get_column_letter(len(headers))}{ws.max_row}"
    table = Table(displayName=name, ref=ref)
    table.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
    ws.add_table(table)


def write_xlsx(catalog: list[dict], detail: list[dict]) -> Path:
    wb = Workbook()
    ws0 = wb.active
    ws0.title = "汇总"
    with_refs = sum(1 for r in catalog if r["需求回填"] == "已回填")
    without = len(catalog) - with_refs
    book_c = Counter(nz(r["分册"]) for r in detail if r["回填状态"] == "已回填" and nz(r["分册"]))
    summary_rows = [
        ("目录行数（注册表）", len(catalog)),
        ("已回填需求来源", with_refs),
        ("未回填", without),
        ("明细行数", len(detail)),
        ("02 展示叶条数", book_c.get("02", 0)),
        ("04 专题叶条数", book_c.get("04", 0)),
        ("05 算法库叶条数", book_c.get("05", 0)),
        ("生成日期", date.today().isoformat()),
        ("说明", "空=尚未从 A1/A2 回填，不是「无需求」。序号只在分册内唯一（02 的 97 ≠ 05 的 97）。"),
        ("刷新命令", "python agent-delivery/metrics/registry/export/export_metric_srs_board.py"),
        ("MCP", "metric-registry → metric-srs-export"),
    ]
    ws0.append(SUMMARY_HEADERS)
    for k, v in summary_rows:
        ws0.append([k, v])
    style_header(ws0, SUMMARY_HEADERS, {"项": 24, "值": 88})
    add_table(ws0, "SrsSummary", SUMMARY_HEADERS)

    ws1 = wb.create_sheet("指标目录")
    ws1.append(CATALOG_HEADERS)
    for row in catalog:
        ws1.append([row.get(h, "") for h in CATALOG_HEADERS])
    style_header(ws1, CATALOG_HEADERS, CATALOG_WIDTH)
    add_table(ws1, "SrsCatalog", CATALOG_HEADERS)

    ws2 = wb.create_sheet("需求来源明细")
    ws2.append(DETAIL_HEADERS)
    for row in detail:
        ws2.append([row.get(h, "") for h in DETAIL_HEADERS])
    style_header(ws2, DETAIL_HEADERS, DETAIL_WIDTH)
    add_table(ws2, "SrsDetail", DETAIL_HEADERS)

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    try:
        wb.save(OUT_XLSX)
        return OUT_XLSX
    except PermissionError:
        stamped = EXPORT_DIR / f"指标需求来源-{datetime.now().strftime('%Y%m%d-%H%M%S')}.xlsx"
        wb.save(stamped)
        return stamped


def summarize(catalog: list[dict], detail: list[dict], xlsx: Path) -> dict:
    with_refs = sum(1 for r in catalog if r["需求回填"] == "已回填")
    return {
        "ok": True,
        "xlsx": str(xlsx),
        "xlsx_canonical": str(OUT_XLSX),
        "xlsx_locked": str(xlsx) != str(OUT_XLSX),
        "sheets": ["汇总", "指标目录", "需求来源明细"],
        "catalog_rows": len(catalog),
        "detail_rows": len(detail),
        "with_refs": with_refs,
        "without_refs": len(catalog) - with_refs,
        "by_book": dict(
            Counter(nz(r["分册"]) for r in detail if r["回填状态"] == "已回填" and nz(r["分册"]))
        ),
    }


def main() -> None:
    json_mode = "--json" in sys.argv
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    by_id = parse_catalog()
    catalog, detail = build_tables(by_id)
    assert catalog, "未解析到任何指标"
    xlsx = write_xlsx(catalog, detail)
    payload = summarize(catalog, detail, xlsx)
    if json_mode:
        print(json.dumps(payload, ensure_ascii=False))
        return
    print(
        f"[source] 注册表 {payload['catalog_rows']} 条；已回填 {payload['with_refs']}；未回填 {payload['without_refs']}"
    )
    print(f"[detail] {payload['detail_rows']} 行  by_book={payload['by_book']}")
    print(f"[out] {xlsx}")
    if payload["xlsx_locked"]:
        print("[warn] 原文件被占用，已写时间戳副本；请关闭 Excel 后再跑一次以覆盖主文件")


if __name__ == "__main__":
    main()

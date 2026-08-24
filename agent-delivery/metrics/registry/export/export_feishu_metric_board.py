# -*- coding: utf-8 -*-
"""离线导出飞书「指标与数据开发进度」同列 Excel。

真源与 scripts/sync-feishu-metric-board.mjs 相同：
  metrics/registry seed + 就绪度矩阵
  + agent-handoffs/**/*data-gap-catalog.yaml
  + metrics/request/{专题系统,展示系统}/pages/*.yaml（合同集合）
飞书配额不够时用本表；禁止把本表回写进 registry YAML。

用法（仓根）：
  python agent-delivery/metrics/registry/export/export_feishu_metric_board.py
  python agent-delivery/metrics/registry/export/export_feishu_metric_board.py --json
MCP：metric-registry → metric-progress-export。依赖：PyYAML + openpyxl（仓内已有）。
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
ORCH_ROOT = EXPORT_DIR.parents[3]
HANDOFFS_DIR = ORCH_ROOT / "agent-delivery" / "agent-handoffs"
REQUEST_DIR = ORCH_ROOT / "agent-delivery" / "metrics" / "request"
OUT_XLSX = EXPORT_DIR / "指标与数据开发进度.xlsx"

SHEET_NAME = "指标与数据开发进度"

# 列序 = feishu-metric-board.yaml#field_names（禁止改中文名）
HEADERS = [
    "指标ID",
    "指标名",
    "模块",
    "专题维度Owner",
    "算法类型",
    "合同集合",
    "填齐阶段",
    "验收单元",
    "四维评估",
    "定义状态",
    "开放项",
    "结构支撑",
    "结构缺口",
    "结构判定",
    "源映射",
    "源缺口",
    "接入状态",
    "接入阶段",
    "综合就绪",
    "卡点责任方",
    "更新频率",
    "口径摘要",
    "缺口说明",
    "更新日期",
]

ALGO_TYPES = ("STAT", "COMPUTE", "MODEL", "GRAPH", "API", "MIXED", "UNKNOWN")
MODEL_TYPES = {"MODEL", "GRAPH", "COMPUTE", "MIXED"}

DEF_ZH = {"aligned": "已对齐", "draft": "草案", "missing": "未登记", "unassessed": "待评估"}
SCHEMA_ZH = {
    "ready": "就绪",
    "partial": "部分",
    "missing": "缺失",
    "pending": "待首评",
    "n/a": "不适用",
    "unassessed": "待评估",
}
ASSESSED_ZH = {"provisional": "初判", "verified": "已核验", "none": "—"}
SOURCE_ZH = {
    "full": "齐备",
    "partial": "部分缺口",
    "none": "无源",
    "pending_ods": "待ODS",
    "n/a": "不适用",
    "unassessed": "待评估",
}
INGEST_ZH = {"mock": "Mock", "ingesting": "接入中", "live": "已接真", "n/a": "不适用"}
OVERALL_ZH = {
    "unregistered": "未登记",
    "no_source": "无数据源",
    "pending_definition": "待口径确认",
    "pending_algorithm": "待算法实现",
    "pending_schema": "待结构设计",
    "pending_source": "待数据源",
    "mock_waiting": "待接入（Mock）",
    "ingesting": "接入中",
    "live": "可上线",
}
OWNER_ZH = {
    "unregistered": "口径（淮政玮）",
    "no_source": "甲方/数据采购（PM 跟踪）",
    "pending_definition": "口径（淮政玮）+ 甲方决策清单",
    "pending_algorithm": "算法（唐绍祖）",
    "pending_schema": "架构（徐滕强/李伟）",
    "pending_source": "GDF（辜少彬）/ 甲方源侧",
    "mock_waiting": "数据工厂（GDF 接入排期）",
    "ingesting": "数据工厂（GDF）",
    "live": "—",
}
LIFE_ZH = {
    "pre_register": "盘点未注册",
    "identified": "已点名",
    "open": "定义中",
    "formula_signed": "公式已签",
    "source_mapped": "源已对",
    "kit_complete": "8件套齐",
    "retired": "废止",
    "unspecified": "未标",
}
CONTRACT_ZH = {"both": "F∩L", "func_only": "F−L", "lib_only": "L−F", "unsorted": "未分拣"}
STAGE_LABEL = {
    "ods_synced": "源同步",
    "dwd_loaded": "DWD",
    "es_indexed": "ES",
    "graph_loaded": "图谱",
    "verified": "核验",
}
STAGE_ZH = {"done": "✔", "in_progress": "进行中", "todo": "未开始", "n/a": "不适用"}

COL_WIDTH = {
    "指标ID": 32,
    "指标名": 22,
    "模块": 22,
    "专题维度Owner": 14,
    "算法类型": 12,
    "合同集合": 10,
    "填齐阶段": 12,
    "验收单元": 12,
    "四维评估": 10,
    "定义状态": 10,
    "开放项": 14,
    "结构支撑": 10,
    "结构缺口": 36,
    "结构判定": 10,
    "源映射": 12,
    "源缺口": 36,
    "接入状态": 10,
    "接入阶段": 42,
    "综合就绪": 16,
    "卡点责任方": 28,
    "更新频率": 16,
    "口径摘要": 42,
    "缺口说明": 42,
    "更新日期": 12,
}
WRAP_COLS = {"结构缺口", "源缺口", "接入阶段", "卡点责任方", "口径摘要", "缺口说明"}


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def nz(v) -> str:
    if v is None:
        return ""
    return str(v).strip()


def clip(s: str, n: int) -> str:
    t = " ".join((s or "").split())
    return t if len(t) <= n else t[:n] + "…"


def parse_seeds() -> dict[str, dict]:
    seeds = {}
    for path in sorted(REGISTRY_DIR.glob("cfg_metric-*-seed.yaml")):
        doc = load_yaml(path)
        for row in doc.get("metrics") or []:
            mid = nz(row.get("metric_id"))
            if not mid:
                continue
            algo = nz(row.get("algorithm_type")).upper() or "UNKNOWN"
            seeds[mid] = {
                "name": nz(row.get("metric_name_zh")),
                "definition": nz(row.get("definition")),
                "update_freq": nz(row.get("update_freq")),
                "mapping_status": nz(row.get("mapping_status")),
                "pending_ref": nz(row.get("pending_ref")),
                "acceptance_unit": nz(row.get("acceptance_unit_id")),
                "algorithm_type": algo if algo in ALGO_TYPES else "UNKNOWN",
            }
    return seeds


def schema_gap_of(row: dict) -> str:
    detail = row.get("d2_schema_detail")
    if isinstance(detail, dict) and detail.get("gap"):
        return nz(detail.get("gap"))
    return nz(row.get("d2_gap") or row.get("gap"))


def parse_matrices() -> tuple[dict[str, dict], dict[str, str]]:
    readiness = {}
    header_module = {}
    for path in sorted(REGISTRY_DIR.glob("metric-readiness-matrix-*.yaml")):
        doc = load_yaml(path)
        file_module = nz(doc.get("module"))
        for row in doc.get("metrics") or []:
            mid = nz(row.get("metric_id"))
            if not mid:
                continue
            life = nz(row.get("lifecycle_stage")) or "unspecified"
            if life not in LIFE_ZH:
                life = "unspecified"
            stages = row.get("d4_ingestion_stages")
            if not isinstance(stages, dict):
                stages = {}
            readiness[mid] = {
                "module": nz(row.get("module")) or file_module,
                "name": nz(row.get("metric_name_zh")),
                "acceptance_unit": nz(row.get("acceptance_unit_id")),
                "def_status": nz(row.get("d1_def_status")),
                "pending_ref": nz(row.get("d1_pending_ref")),
                "def_note": nz(row.get("d1_note")),
                "schema_status": nz(row.get("d2_schema_status")),
                "schema_assessed": nz(row.get("d2_assessed")) or "provisional",
                "schema_gap": schema_gap_of(row),
                "source_status": nz(row.get("d3_source_mapping_status")),
                "source_gap": nz(row.get("d3_gap")),
                "ingestion_status": nz(row.get("d4_ingestion_status")),
                "stages": {nz(k): nz(v) for k, v in stages.items()},
                "lifecycle_stage": life,
            }
            header_module[mid] = file_module
    return readiness, header_module


def _yaml_scalar(raw: str) -> str:
    v = (raw or "").strip()
    if not v or v in ("null", "~", "undefined"):
        return ""
    if len(v) > 1 and ((v[0] == v[-1] == '"') or (v[0] == v[-1] == "'")):
        return v[1:-1].replace('\\"', '"')
    if v[0] in "\"'":
        return v[1:]
    hash_at = v.find(" #")
    if hash_at >= 0:
        v = v[:hash_at].strip()
    return v


def _field_of(block: str, key: str) -> str:
    m = re.search(rf"^\s+{re.escape(key)}:\s*(.+)$", block, re.M)
    if not m:
        return ""
    v = m.group(1).strip()
    if v in ("|", ">", "|-", ">"):
        return ""
    return _yaml_scalar(v)


def _split_metric_blocks(raw: str) -> list[str]:
    blocks: list[list[str]] = []
    current: list[str] | None = None
    for line in raw.splitlines():
        if re.match(r"^ {2}- metric_id:", line):
            if current:
                blocks.append(current)
            current = [line]
        elif current is not None:
            if re.match(r"^ {2}- ", line) or (line.strip() and not line.startswith(" ")):
                blocks.append(current)
                current = None
            else:
                current.append(line)
    if current:
        blocks.append(current)
    return ["\n".join(b) for b in blocks]


def parse_gap_hints() -> dict[str, str]:
    """缺口 catalog 常有未加引号冒号，不能整文件 yaml.safe_load；与飞书脚本同用块解析。"""
    hints = {}
    for path in HANDOFFS_DIR.rglob("*data-gap-catalog.yaml"):
        raw = path.read_text(encoding="utf-8")
        for block in _split_metric_blocks(raw):
            mid = _field_of(block, "- metric_id") or _field_of(block, "metric_id")
            hint = _field_of(block, "pending_hint")
            if mid and hint:
                hints[mid] = hint
    return hints


def parse_a2_verdicts() -> dict[str, set[str]]:
    verdicts: dict[str, set[str]] = {}
    for folder in ("专题系统", "展示系统"):
        pages = REQUEST_DIR / folder / "pages"
        if not pages.is_dir():
            continue
        for path in pages.glob("*.yaml"):
            doc = load_yaml(path)
            for item in doc.get("items") or []:
                if not isinstance(item, dict):
                    continue
                mid = nz(item.get("metric_id"))
                verdict = nz(item.get("差集判定"))
                if not mid or not verdict:
                    continue
                verdicts.setdefault(mid, set()).add(verdict)
    return verdicts


def rollup_assessed(r: dict) -> str:
    if r.get("def_status") == "missing":
        return "unregistered"
    if r.get("source_status") == "none":
        return "no_source"
    if r.get("def_status") == "draft":
        return "pending_definition"
    if r.get("schema_status") not in ("ready", "n/a"):
        return "pending_schema"
    if r.get("source_status") in ("partial", "pending_ods"):
        return "pending_source"
    if r.get("ingestion_status") == "ingesting":
        return "ingesting"
    if r.get("ingestion_status") == "live":
        return "live"
    return "mock_waiting"


def rollup_legacy(seed: dict | None) -> str:
    t = (seed or {}).get("algorithm_type") or "UNKNOWN"
    mapping = (seed or {}).get("mapping_status") or ""
    if mapping == "❌":
        return "no_source"
    if mapping == "⚠️" or (seed or {}).get("pending_ref"):
        return "pending_definition"
    if mapping == "🔧":
        if t in MODEL_TYPES:
            return "pending_algorithm"
        if t == "UNKNOWN":
            return "pending_definition"
        return "pending_schema"
    return "mock_waiting"


def topic_owner_of(mid: str) -> str:
    if mid.startswith("M_ENT_") or mid.startswith("M_SYNTH_"):
        return "徐滕强"
    if mid.startswith("M_CHAIN_"):
        return "李伟"
    if mid.startswith("M_SVC_"):
        return "侯佳伟"
    if mid.startswith("M_POLICY_"):
        return "淮政玮"
    return "—"


def contract_of(mid: str, verdicts: dict[str, set[str]]) -> str:
    s = verdicts.get(mid)
    if not s:
        return "unsorted"
    if "missing" in s:
        return "func_only"
    if "mapped" in s:
        return "both"
    return "unsorted"


def blocker_owner(overall_key: str, algo_type: str, topic_owner: str) -> str:
    if algo_type == "STAT" and overall_key in ("pending_schema", "pending_algorithm"):
        who = topic_owner if topic_owner != "—" else "模块负责人"
        return f"STAT Java（{who}）+ GDF ADS"
    return OWNER_ZH.get(overall_key, "—")


def module_display(mid: str, r: dict | None) -> str:
    mod = (r or {}).get("module") or ""
    if mod:
        if mod.startswith("ENT-"):
            return f"E1 企业 · {mod[4:]}"
        return mod
    if mid.startswith("M_ENT_"):
        return "E1 企业（待四维评估）"
    if mid.startswith("M_CHAIN_"):
        return "E2 产业链（待四维评估）"
    if mid.startswith("M_SVC_"):
        return "产业服务（待四维评估）"
    if mid.startswith("M_POLICY_"):
        return "E7 政策（待四维评估）"
    if mid.startswith("M_SYNTH_"):
        return "综合（待四维评估）"
    if mid.startswith("M_TNIE_"):
        return "科技动态（待四维评估）"
    return "其他"


def stages_text(stages: dict) -> str:
    parts = []
    for key, label in STAGE_LABEL.items():
        if stages.get(key):
            parts.append(f"{label}:{STAGE_ZH.get(stages[key], stages[key])}")
    return " | ".join(parts)


def build_rows() -> list[dict]:
    seeds = parse_seeds()
    readiness, _ = parse_matrices()
    hints = parse_gap_hints()
    verdicts = parse_a2_verdicts()
    today = date.today().isoformat()
    rows = []
    for mid in set(seeds) | set(readiness):
        seed = seeds.get(mid)
        r = readiness.get(mid)
        assessed = r is not None
        algo = (seed or {}).get("algorithm_type") or "UNKNOWN"
        overall_key = rollup_assessed(r) if assessed else rollup_legacy(seed)
        def_status = r["def_status"] if assessed else ("draft" if seed and seed.get("pending_ref") else "aligned")
        if not seed:
            legacy_source = "unassessed"
        elif seed["mapping_status"] == "❌":
            legacy_source = "none"
        elif seed["mapping_status"] == "✅":
            legacy_source = "full"
        else:
            legacy_source = "unassessed"
        definition = (seed or {}).get("definition") or (r or {}).get("def_note") or ""
        topic_owner = topic_owner_of(mid)
        rows.append(
            {
                "指标ID": mid,
                "指标名": (seed or {}).get("name") or (r or {}).get("name") or mid,
                "模块": module_display(mid, r),
                "专题维度Owner": topic_owner,
                "算法类型": algo,
                "合同集合": CONTRACT_ZH[contract_of(mid, verdicts)],
                "填齐阶段": LIFE_ZH[r["lifecycle_stage"] if assessed else "unspecified"],
                "验收单元": (seed or {}).get("acceptance_unit") or (r or {}).get("acceptance_unit") or "—",
                "四维评估": "已评估" if assessed else "待评估",
                "定义状态": DEF_ZH.get(def_status, "待评估"),
                "开放项": (r.get("pending_ref") if assessed else (seed or {}).get("pending_ref")) or "",
                "结构支撑": SCHEMA_ZH.get(r["schema_status"] if assessed else "unassessed", "待评估"),
                "结构缺口": r["schema_gap"] if assessed else "",
                "结构判定": ASSESSED_ZH.get(r["schema_assessed"], "初判") if assessed else "—",
                "源映射": SOURCE_ZH.get(r["source_status"] if assessed else legacy_source, "待评估"),
                "源缺口": (r.get("source_gap") if assessed else "") or "",
                "接入状态": INGEST_ZH.get(r["ingestion_status"] if assessed else "mock", "Mock"),
                "接入阶段": stages_text(r["stages"]) if assessed else "",
                "综合就绪": OVERALL_ZH[overall_key],
                "卡点责任方": blocker_owner(overall_key, algo, topic_owner),
                "更新频率": (seed or {}).get("update_freq") or "",
                "口径摘要": clip(definition, 120),
                "缺口说明": hints.get(mid, ""),
                "更新日期": today,
            }
        )
    rows.sort(key=lambda x: (x["模块"], x["指标ID"]))
    return rows


def write_xlsx(rows: list[dict]) -> Path:
    wb = Workbook()
    ws = wb.active
    ws.title = SHEET_NAME
    header_fill = PatternFill("solid", fgColor="165DFF")
    header_font = Font(name="Calibri", color="FFFFFF", bold=True, size=11)
    body_font = Font(name="Calibri", size=11)
    wrap = Alignment(wrap_text=True, vertical="center")
    top = Alignment(vertical="center")

    ws.append(HEADERS)
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = wrap

    for row in rows:
        ws.append([row.get(h, "") for h in HEADERS])

    for r in ws.iter_rows(min_row=2, max_row=ws.max_row, max_col=len(HEADERS)):
        for cell in r:
            cell.font = body_font
            header = HEADERS[cell.column - 1]
            cell.alignment = wrap if header in WRAP_COLS else top

    for i, name in enumerate(HEADERS, 1):
        ws.column_dimensions[get_column_letter(i)].width = COL_WIDTH.get(name, 16)

    ws.auto_filter.ref = f"A1:{get_column_letter(len(HEADERS))}{ws.max_row}"
    ws.freeze_panes = "A2"
    ws.row_dimensions[1].height = 22
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_title_rows = "1:1"

    if rows:
        ref = f"A1:{get_column_letter(len(HEADERS))}{ws.max_row}"
        table = Table(displayName="MetricBoard", ref=ref)
        table.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
        ws.add_table(table)

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    try:
        wb.save(OUT_XLSX)
        return OUT_XLSX
    except PermissionError:
        stamped = EXPORT_DIR / f"指标与数据开发进度-{datetime.now().strftime('%Y%m%d-%H%M%S')}.xlsx"
        wb.save(stamped)
        return stamped


def selfcheck(rows: list[dict]) -> None:
    assert rows, "未解析到任何指标"
    bad = [r["指标ID"] for r in rows if r["算法类型"] == "STAT" and r["综合就绪"] == "待算法实现"]
    assert not bad, f"STAT 误入待算法实现: {bad}"
    assert all(h in rows[0] for h in HEADERS)


def summarize(rows: list[dict], xlsx: Path) -> dict:
    assessed = sum(1 for r in rows if r["四维评估"] == "已评估")
    return {
        "ok": True,
        "xlsx": str(xlsx),
        "xlsx_canonical": str(OUT_XLSX),
        "xlsx_locked": str(xlsx) != str(OUT_XLSX),
        "sheet": SHEET_NAME,
        "rows": len(rows),
        "assessed": assessed,
        "overall": dict(Counter(r["综合就绪"] for r in rows)),
        "algorithm_type": dict(Counter(r["算法类型"] for r in rows)),
        "contract_set": dict(Counter(r["合同集合"] for r in rows)),
        "columns": HEADERS,
    }


def main() -> None:
    json_mode = "--json" in sys.argv
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    rows = build_rows()
    selfcheck(rows)
    xlsx = write_xlsx(rows)
    payload = summarize(rows, xlsx)
    if json_mode:
        print(json.dumps(payload, ensure_ascii=False))
        return
    print(f"[source] 指标 {payload['rows']} 条（四维已评估 {payload['assessed']} 条）")
    print(f"[out] {xlsx}")
    if payload["xlsx_locked"]:
        print("[warn] 原文件被占用，已写时间戳副本；请关闭 Excel 后再跑一次以覆盖主文件")
    print(f"[rollup] overall={payload['overall']}")
    print(f"[rollup] algorithm_type={payload['algorithm_type']}")
    print(f"[rollup] contract_set={payload['contract_set']}")


if __name__ == "__main__":
    main()

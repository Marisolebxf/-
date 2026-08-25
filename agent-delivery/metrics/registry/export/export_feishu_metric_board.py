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
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

EXPORT_DIR = Path(__file__).resolve().parent
REGISTRY_DIR = EXPORT_DIR.parent
ORCH_ROOT = EXPORT_DIR.parents[3]
HANDOFFS_DIR = ORCH_ROOT / "agent-delivery" / "agent-handoffs"
REQUEST_DIR = ORCH_ROOT / "agent-delivery" / "metrics" / "request"
OUT_XLSX = EXPORT_DIR / "指标与数据开发进度.xlsx"
DOMAIN_ZH = json.loads(
    (ORCH_ROOT / "scripts" / "lib" / "metric-domain-enum.json").read_text(encoding="utf-8")
)
MODULE_ZH = json.loads(
    (ORCH_ROOT / "scripts" / "lib" / "metric-module-enum.json").read_text(encoding="utf-8")
)

SHEET_NAME = "指标与数据开发进度"

# 列序 ≈ feishu-metric-board.yaml#field_names。
# 离线表在「模块」后多「模块说明」；lifecycle_stage 离线列名「语义层开发阶段」（飞书仍叫「填齐阶段」）。
# 「差集判定」仅离线表：A2 原文分档按 metric_id 聚合。飞书进度表不加该列（页级差集另表「页面指标差集」）。
HEADERS = [
    "指标ID",
    "指标名",
    "域",
    "模块",
    "模块说明",
    "专题维度Owner",
    "算法类型",
    "合同集合",
    "差集判定",
    "语义层开发阶段",
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

ALGO_TYPES = ("STAT", "COMPUTE", "MODEL", "GRAPH", "API", "third_party", "MIXED", "LITERATURE", "UNKNOWN")
MODEL_TYPES = {"MODEL", "GRAPH", "COMPUTE", "MIXED"}
# 轴 A 绿框：这段计算谁写 = 唐绍祖。可上线除外。
# third_party → PM（郭万迎）；STAT / COMPUTE → 专题维度Owner 人名。
TANG_BLOCKER_TYPES = {"MODEL", "GRAPH", "MIXED", "LITERATURE", "UNKNOWN"}
THIRD_PARTY_BLOCKER = "PM（郭万迎）"
TOPIC_OWNER_UNNAMED = "专题维度Owner（未点名）"


def normalize_algo_type(raw: str) -> str:
    """seed 写 third_party；API 同义。禁止 .upper() 把 third_party 打成 THIRD_PARTY 再掉进 UNKNOWN。"""
    t = nz(raw).strip()
    if not t:
        return "UNKNOWN"
    if t.lower() in ("api", "third_party"):
        return "third_party"
    u = t.upper()
    return u if u in ALGO_TYPES else "UNKNOWN"


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
VERDICT_ORDER = ("missing", "mapped", "other_system", "third_party", "n/a_ops", "semantic_debt")
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
    "域": 10,
    "模块": 22,
    "模块说明": 28,
    "专题维度Owner": 14,
    "算法类型": 12,
    "合同集合": 10,
    "差集判定": 22,
    "语义层开发阶段": 16,
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
WRAP_COLS = {"结构缺口", "源缺口", "接入阶段", "卡点责任方", "口径摘要", "缺口说明", "模块说明", "差集判定"}

# 表头批注（Excel 批注/Note）。飞书已有列中文名不改；离线表本处可与飞书列名不同。
HEADER_NOTES = {
    "指标ID": "指标主键 metric_id。8 件套第 1 项。",
    "指标名": "中文名称。8 件套第 2 项。",
    "域": "注册表分类字段，中文枚举：企业 / 产业链 / 产业服务 / 政策 / 综合 / 创新 / 技术 / 机构 / 人才 / 通用 / 科技动态。由 seed 文件名推导。不是 8 件套。",
    "模块": "矩阵 module 代码（DS-07 / ENT-EVAL / TOPIC-TALENT…）。列名不改。中文见「模块说明」。",
    "模块说明": "模块代码的中文：展示 DS-xx = 三级/四级页名；专题 TOPIC-* / ENT-* / CHAIN-* 为页面中文。枚举 scripts/lib/metric-module-enum.json。不是 8 件套。",
    "专题维度Owner": "该指标所属专题维度的负责人。",
    "算法类型": "8 件套第 5 项。STAT / COMPUTE / MODEL / GRAPH / third_party（与 API 同义）/ MIXED / UNKNOWN。UNKNOWN 禁止派实现单。",
    "合同集合": (
        "功能清单 F 与算法库 L 的交并。A2 mapped→F∩L；A2 missing（有正式号）→F−L；注册表有、A2 未挂→L−F；"
        "other_system / n/a_ops / third_party→未分拣。细档看「差集判定」。"
    ),
    "差集判定": (
        "A2 页面差集（不是 8 件套，也不是合同集合）。按 metric_id 把各页 差集判定 去重并列；多档用「 / 」。\n"
        "mapped：本页对上某 05 叶，算覆盖。\n"
        "missing：招标要了、库和页都对不上 → 缺口。\n"
        "other_system：能力在别的页/别的系统已覆盖，本页只展示；禁止当本页缺口，也禁止再 mapped 一次。\n"
        "n/a_ops：壳（Tab、筛选、分页、空态），不进算法差集。\n"
        "另有 third_party（三方）/ semantic_debt（语义欠账，不上差集看板）。\n"
        "未挂页：注册表有、A2 未写这个 ID（合同集合 = L−F）。\n"
        "页级一行一条见飞书「页面指标差集」。"
    ),
    "语义层开发阶段": (
        "lifecycle_stage：这条指标在填齐流水线上走到哪一关（policy §2.1.1），与 D1–D4 正交，不是 8 件套。\n"
        "取值：盘点未注册 → 已点名 → 定义中 → 公式已签 → 源已对 → 8件套齐（还有废止 / 未标）。\n"
        "它回答的是：过程走到哪了。"
    ),
    "验收单元": "对应验收目录单元 ID。",
    "四维评估": (
        "本列取值：已评估 = 已入就绪度矩阵；待评估 = 仅有 8 件套、四维未评。\n"
        "四维（D1–D4，不是 8 件套）：\n"
        "D1 定义 — 库里有没有、口径齐不齐（「定义状态」）\n"
        "D2 结构 — 项目自己的表/ES/图算不算得出（「结构支撑」）\n"
        "D3 源映射 — 三方源喂不喂得饱（「源映射」）\n"
        "D4 接入 — 线上是 Mock 还是真数（「接入状态」）"
    ),
    "定义状态": (
        "定义状态是四维里的 D1：这条指标在库里的口径对象齐不齐。不是 8 件套本身。\n"
        "取值只有三档——已对齐 / 草案 / 未登记。\n"
        "终态「已对齐」= 8 件套（9 项）都合格，algorithm_type 不能是 UNKNOWN。\n"
        "它回答的是：身份证算不算写完了。"
    ),
    "开放项": "未闭合口径或缺口编号（pending_ref）。",
    "结构支撑": "D2 结构：项目自己的表/ES/图算不算得出。就绪 / 部分 / 缺失 / 待首评 / 不适用。",
    "结构缺口": "D2 缺口说明。",
    "结构判定": "D2 判定可信度：初判 / 已核验。",
    "源映射": "D3 源映射：三方源喂不喂得饱。齐备 / 部分缺口 / 无源 / 待ODS / 不适用。",
    "源缺口": "D3 缺口说明。",
    "接入状态": "D4 接入：线上是 Mock 还是真数。Mock / 接入中 / 已接真。",
    "接入阶段": "D4 分阶段清单（源同步 / DWD / ES / 图谱 / 核验）。只记事实状态，不用百分比。",
    "综合就绪": "由四维 rollup 的会议主状态。",
    "卡点责任方": (
        "现在卡在谁手里。不是 8 件套。按 algorithm_type 优先：\n"
        "third_party（与 API 同义）→ PM（郭万迎）。\n"
        "STAT / COMPUTE → 专题维度Owner 人名（企业/综合=徐滕强，产业链=李伟，产业服务=侯佳伟，政策=淮政玮；未点名为「专题维度Owner（未点名）」）。\n"
        "MODEL / GRAPH / MIXED / LITERATURE / UNKNOWN（轴 A 绿框）→ 算法（唐绍祖）；可上线仍为 —。\n"
        "其余按综合就绪：口径淮政玮 / 架构 / GDF / 甲方源。"
    ),
    "更新频率": "8 件套：指标更新频率。",
    "口径摘要": "定义 / 口径截断摘要（完整口径在 seed）。",
    "缺口说明": "数据缺口长文案（gap catalog）。",
    "更新日期": "本表导出日期，不是指标业务更新日。",
}


def attach_header_notes(ws) -> None:
    for cell in ws[1]:
        text = HEADER_NOTES.get(str(cell.value or ""))
        if not text:
            continue
        note = Comment(text, "指标注册表")
        note.width = 320
        lines = text.count("\n") + 1
        if lines >= 6:
            note.height = 240
        elif lines >= 4 or "\n" in text or len(text) > 80:
            note.height = 200 if lines >= 4 else 168
        else:
            note.height = 96
        cell.comment = note


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


def domain_code_of_seed(name: str) -> str:
    m = re.match(r"cfg_metric-(.+)-seed\.yaml$", name)
    return m.group(1) if m else ""


def domain_code_of_matrix(name: str) -> str:
    m = re.match(r"metric-readiness-matrix-(.+)\.yaml$", name)
    return m.group(1) if m else ""


def domain_zh(code: str) -> str:
    c = (code or "").strip()
    return DOMAIN_ZH.get(c) or DOMAIN_ZH.get(c.upper()) or c


def parse_seeds() -> dict[str, dict]:
    seeds = {}
    for path in sorted(REGISTRY_DIR.glob("cfg_metric-*-seed.yaml")):
        doc = load_yaml(path)
        code = domain_code_of_seed(path.name)
        for row in doc.get("metrics") or []:
            mid = nz(row.get("metric_id"))
            if not mid:
                continue
            algo = normalize_algo_type(row.get("algorithm_type"))
            seeds[mid] = {
                "name": nz(row.get("metric_name_zh")),
                "definition": nz(row.get("definition")),
                "update_freq": nz(row.get("update_freq")),
                "mapping_status": nz(row.get("mapping_status")),
                "pending_ref": nz(row.get("pending_ref")),
                "acceptance_unit": nz(row.get("acceptance_unit_id")),
                "algorithm_type": algo,
                "domain_code": code,
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
        file_domain = domain_code_of_matrix(path.name)
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
                "domain_code": file_domain,
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
            rows = []
            for key in ("items", "demands"):
                rows.extend(x for x in (doc.get(key) or []) if isinstance(x, dict))
            for item in rows:
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
        return "lib_only"
    if "missing" in s:
        return "func_only"
    if "mapped" in s:
        return "both"
    return "unsorted"


def verdict_of(mid: str, verdicts: dict[str, set[str]]) -> str:
    s = verdicts.get(mid)
    if not s:
        return "未挂页"
    ordered = [v for v in VERDICT_ORDER if v in s]
    rest = sorted(x for x in s if x not in VERDICT_ORDER)
    return " / ".join(ordered + rest)


def topic_blocker(topic_owner: str) -> str:
    if topic_owner and topic_owner not in ("—", "未点名"):
        return topic_owner
    return TOPIC_OWNER_UNNAMED


def blocker_owner(overall_key: str, algo_type: str, topic_owner: str) -> str:
    t = "third_party" if algo_type == "API" else (algo_type or "UNKNOWN")
    if t == "third_party":
        return THIRD_PARTY_BLOCKER
    if t in ("STAT", "COMPUTE"):
        return topic_blocker(topic_owner)
    if t in TANG_BLOCKER_TYPES and overall_key != "live":
        return "算法（唐绍祖）"
    return OWNER_ZH.get(overall_key, "—")


def module_zh_of(mid: str, r: dict | None) -> str:
    code = nz((r or {}).get("module"))
    if code in MODULE_ZH:
        return MODULE_ZH[code]
    ds = re.match(r"^(DS-\d{2})", code)
    if ds and ds.group(1) in MODULE_ZH:
        return MODULE_ZH[ds.group(1)]
    if code.startswith("ENT-"):
        return f"企业展示 / {code[4:]}"
    if code.startswith("CHAIN-"):
        return f"产业链分析 / {code[6:]}"
    if code.startswith("TOPIC-"):
        return f"专题 / {code[6:]}"
    if code.startswith("SYNTH-"):
        return f"综合智能分析 / {code[6:]}"
    if code.startswith("SVC-"):
        return f"产业服务 / {code[4:]}"
    if code:
        return DOMAIN_ZH.get(code) or DOMAIN_ZH.get(code.upper()) or code
    if mid.startswith("M_ENT_"):
        return MODULE_ZH["ENT"]
    if mid.startswith("M_CHAIN_"):
        return MODULE_ZH["CHAIN"]
    if mid.startswith("M_SVC_"):
        return MODULE_ZH["SVC"]
    if mid.startswith("M_POLICY_"):
        return MODULE_ZH["POLICY"]
    if mid.startswith("M_SYNTH_"):
        return MODULE_ZH["SYNTH"]
    if mid.startswith("M_TNIE_"):
        return MODULE_ZH["TNIE"]
    if mid.startswith("M_INNOV_"):
        return MODULE_ZH["INNOV"]
    if mid.startswith("M_TECH_"):
        return MODULE_ZH["TECH"]
    if mid.startswith("M_ORG_"):
        return MODULE_ZH["ORG"]
    if mid.startswith("M_TALENT_"):
        return MODULE_ZH["TALENT"]
    return "其他"


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
                "域": domain_zh((seed or {}).get("domain_code") or (r or {}).get("domain_code") or ""),
                "模块": module_display(mid, r),
                "模块说明": module_zh_of(mid, r),
                "专题维度Owner": topic_owner,
                "算法类型": algo,
                "合同集合": CONTRACT_ZH[contract_of(mid, verdicts)],
                "差集判定": verdict_of(mid, verdicts),
                "语义层开发阶段": LIFE_ZH[r["lifecycle_stage"] if assessed else "unspecified"],
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
    rows.sort(key=lambda x: (x["域"], x["模块"], x["指标ID"]))
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
    attach_header_notes(ws)

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
    assert HEADERS[HEADERS.index("模块") + 1] == "模块说明"
    assert "语义层开发阶段" in HEADERS and "填齐阶段" not in HEADERS
    assert HEADERS[HEADERS.index("合同集合") + 1] == "差集判定"
    keypano = next((r for r in rows if r["指标ID"] == "M_ENT_KEYPANO_DOMAIN_SUMMARY"), None)
    assert keypano and "other_system" in keypano["差集判定"], "E-33 KEYPANO 领域摘要应为 other_system"
    tang_miss = [
        r["指标ID"]
        for r in rows
        if r["算法类型"] in TANG_BLOCKER_TYPES and r["综合就绪"] != "可上线" and r["卡点责任方"] != "算法（唐绍祖）"
    ]
    assert not tang_miss, f"轴 A 绿框未归集唐绍祖: {tang_miss[:8]}"
    tp_miss = [
        r["指标ID"]
        for r in rows
        if r["算法类型"] == "third_party" and r["卡点责任方"] != THIRD_PARTY_BLOCKER
    ]
    assert not tp_miss, f"third_party 未归集郭万迎: {tp_miss[:8]}"
    owner_miss = [
        r["指标ID"]
        for r in rows
        if r["算法类型"] in ("STAT", "COMPUTE") and r["卡点责任方"] != topic_blocker(topic_owner_of(r["指标ID"]))
    ]
    assert not owner_miss, f"STAT/COMPUTE 未归集专题维度Owner: {owner_miss[:8]}"
    stat_tang = [
        r["指标ID"]
        for r in rows
        if r["算法类型"] in ("STAT", "COMPUTE", "third_party") and r["卡点责任方"] == "算法（唐绍祖）"
    ]
    assert not stat_tang, f"STAT/COMPUTE/third_party 误归唐绍祖: {stat_tang[:8]}"
    blank_zh = [r["指标ID"] for r in rows if not r.get("模块说明")]
    assert not blank_zh, f"模块说明空: {blank_zh[:8]}"
    unsorted = sum(1 for r in rows if r["合同集合"] == "未分拣")
    lib_only = sum(1 for r in rows if r["合同集合"] == "L−F")
    assert lib_only > 0, "合同集合应有 L−F（注册表有、A2 未挂）"
    assert unsorted < lib_only, f"未分拣({unsorted}) 仍多于 L−F({lib_only})，推断可能没吃 T0X"
    missing_notes = [h for h in HEADERS if h not in HEADER_NOTES]
    assert not missing_notes, f"表头缺批注: {missing_notes}"


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
        "domain": dict(Counter(r["域"] for r in rows)),
        "contract_set": dict(Counter(r["合同集合"] for r in rows)),
        "a2_verdict": dict(Counter(r["差集判定"] for r in rows)),
        "blocker_owner": dict(Counter(r["卡点责任方"] for r in rows)),
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
    print(f"[rollup] a2_verdict={payload['a2_verdict']}")
    print(f"[rollup] blocker_owner={payload['blocker_owner']}")


if __name__ == "__main__":
    main()

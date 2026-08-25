# -*- coding: utf-8 -*-
"""解析客户决策清单跟踪表.md，按 metric_id 归集决策编号。

规则对齐 scripts/sync-feishu-decision-board.mjs#parseDecisionItems：
只收 §2 注册表（首列 = ID）的 Q 项，跳过占位行。
挂到指标：影响列里的 M_*（含前缀通配）∪ 该指标 pending_ref 中确在清单上的编号。
GAP-* / 叶级 Q-MO-* 不进本列。
"""
from __future__ import annotations

import re
from pathlib import Path

EXPORT_DIR = Path(__file__).resolve().parent
ORCH_ROOT = EXPORT_DIR.parents[3]
DECISION_MD = ORCH_ROOT / "agent-delivery" / "客户决策清单跟踪表.md"
COL_NAME = "决策清单中的编号"

STATUS_MAP = {"🔴": "阻塞", "🟡": "临时默认", "🟢": "已确认", "⚪": "已撤销"}
QID_RE = re.compile(r"Q[\w-]*\d+")
METRIC_TOKEN_RE = re.compile(r"M_[A-Z][A-Z0-9_]*(?:\*)?")


def strip_md(text: str) -> str:
    t = text or ""
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    t = re.sub(r"`([^`]+)`", r"\1", t)
    t = re.sub(r"(^|\s)_([^_]+)_(?=\s|$)", r"\1\2", t)
    return t.strip()


def extract_decision_id(raw: str) -> str:
    text = strip_md(raw or "")
    m = re.match(r"^(Q[\w-]*\d+)", text)
    return m.group(1) if m else ""


def split_table_row(line: str) -> list[str]:
    cells = [c.strip() for c in line.split("|")]
    return cells[1:-1]


def classify_header(name: str) -> str | None:
    n = name.strip()
    if n == "ID":
        return "decision_id"
    if "标题" in n:
        return "title"
    if "来源" in n:
        return "source"
    if "影响" in n:
        return "impact"
    if "临时默认" in n:
        return "team_default"
    if "状态" in n:
        return "status"
    if "deadline" in n.lower():
        return "deadline"
    if "甲方决策" in n:
        return "decision"
    if "PDR" in n:
        return "pdr_delta"
    if "落地" in n:
        return "landing"
    return None


def parse_decision_items(path: Path | None = None) -> list[dict]:
    raw = (path or DECISION_MD).read_text(encoding="utf-8")
    items: list[dict] = []
    batch = ""
    header_keys: list[str | None] | None = None
    for line in raw.splitlines():
        h = re.match(r"^###\s+(2\.\w+)\s+(.+)$", line)
        if h:
            batch = f"{h.group(1)} {strip_md(h.group(2))}"
            header_keys = None
            continue
        if not line.strip().startswith("|"):
            header_keys = None
            continue
        cells = split_table_row(line)
        if not cells:
            continue
        if re.match(r"^:?-{3,}", cells[0]):
            continue
        if cells[0] == "ID":
            header_keys = [classify_header(c) for c in cells]
            continue
        if not header_keys:
            continue
        decision_id = extract_decision_id(cells[0])
        if not decision_id:
            continue
        item: dict = {"batch": batch}
        for key, cell in zip(header_keys, cells):
            if key and cell is not None:
                item[key] = strip_md(cell)
        item["decision_id"] = decision_id
        title = item.get("title") or ""
        if not title or title == "—":
            continue
        item["status"] = next((zh for sym, zh in STATUS_MAP.items() if sym in (item.get("status") or "")), "未标注")
        items.append(item)
    return items


def qids_in(text: str) -> list[str]:
    return QID_RE.findall(text or "")


def metric_tokens(text: str) -> list[str]:
    return METRIC_TOKEN_RE.findall(text or "")


def build_index(items: list[dict] | None = None) -> dict:
    rows = items if items is not None else parse_decision_items()
    ids = {it["decision_id"] for it in rows}
    exact: dict[str, set[str]] = {}
    prefixes: list[tuple[str, str]] = []
    for it in rows:
        qid = it["decision_id"]
        for token in metric_tokens(it.get("impact") or ""):
            if token.endswith("*"):
                prefixes.append((token[:-1], qid))
            else:
                exact.setdefault(token, set()).add(qid)
    return {"ids": ids, "exact": exact, "prefixes": prefixes, "count": len(rows)}


def format_decision_ids(metric_id: str, pending_ref: str = "", index: dict | None = None) -> str:
    idx = index if index is not None else build_index()
    found: set[str] = set()
    found.update(idx["exact"].get(metric_id) or ())
    for prefix, qid in idx["prefixes"]:
        if metric_id.startswith(prefix):
            found.add(qid)
    for qid in qids_in(pending_ref):
        if qid in idx["ids"]:
            found.add(qid)
    return " / ".join(sorted(found))


def selfcheck() -> None:
    items = parse_decision_items()
    assert len(items) >= 50, f"决策项过少: {len(items)}"
    ids = {it["decision_id"] for it in items}
    for qid in ("Q001", "Q010", "Q019", "QC06", "QPOL-01", "Q-SYNTH-E-02"):
        assert qid in ids, f"清单缺 {qid}"
    idx = build_index(items)
    type_ids = format_decision_ids("M_ENT_TYPE_COUNT", "Q010", idx)
    assert "Q010" in type_ids, type_ids
    market = format_decision_ids("M_ENT_MARKET_SHARE", "Q019", idx)
    assert "Q019" in market, market
    chain = format_decision_ids("M_CHAIN_MARKET_SIZE", "", idx)
    assert "QC06" in chain, chain
    gap_only = format_decision_ids("M_FAKE_NONE", "GAP-METRIC-BID-01", idx)
    assert gap_only == "", gap_only
    leaf = format_decision_ids("M_FAKE_NONE", "Q-MO-ENT-01", idx)
    assert leaf == "", leaf


if __name__ == "__main__":
    selfcheck()
    items = parse_decision_items()
    print(f"ok decision_items={len(items)}")

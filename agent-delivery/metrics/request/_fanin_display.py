# -*- coding: utf-8 -*-
"""Merge DS-ALGO-GAP-L01 page yamls into 15-col items + xlsx."""
from __future__ import annotations

import csv
import os
from collections import Counter

import yaml
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGE_DIR = os.path.join(ROOT, "展示系统", "pages")
OUT_DIR = os.path.join(ROOT, "展示系统")
CATALOG = os.path.join(ROOT, "展示系统", "A2-GAP-page-catalog.yaml")
TOPIC_YAML = os.path.join(ROOT, "专题系统", "TOPIC-ALGO-GAP-L01.yaml")

B_PREFIXES = ("M_CHAIN_", "M_SVC_")

COLS = [
    "模块",
    "页面",
    "主项",
    "子项",
    "指标含义",
    "建议取值/取值口径",
    "取值依据类型",
    "调用系统",
    "调用模块",
    "取数依据",
    "差集判定",
    "A1需规ID",
    "A1指标叶ID",
    "metric_id",
    "缺口说明",
]


def _s(v):
    if v is None:
        return None
    if isinstance(v, str):
        t = v.strip()
        return t if t else None
    return v


def load_page_order():
    with open(CATALOG, encoding="utf-8") as f:
        cat = yaml.safe_load(f)
    order = []
    titles = {}
    for wave in cat.get("waves") or []:
        for p in wave.get("pages") or []:
            pid = p.get("page_id")
            if pid:
                order.append(pid)
                titles[pid] = p.get("title")
    return order, titles, cat.get("skipped") or []


def load_topic_missing():
    path = TOPIC_YAML
    if not os.path.isfile(path):
        return set(), set()
    with open(path, encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    mids, names = set(), set()
    for x in doc.get("missing") or []:
        mid = _s(x.get("metric_id"))
        name = _s(x.get("主项"))
        if mid:
            mids.add(mid)
        if name:
            names.add(name)
    return mids, names


def is_b_track(mid):
    if not isinstance(mid, str):
        return False
    return mid.startswith(B_PREFIXES)


def demand_to_item(page_id, title, dem, idx, level3, level4, level5):
    name = dem.get("metric_name_zh") or dem.get("主项") or dem.get("demand_id")
    gap = dem.get("缺口说明")
    verdict = dem.get("差集判定")
    page = level5 or level4 or title
    call_sys = "科技信息展示系统"
    if verdict == "mapped":
        call_sys = "深度挖掘算法"
    elif verdict == "third_party":
        call_sys = "第三方数据"
    elif verdict == "other_system":
        call_sys = "基础数据"
    elif verdict == "n/a_ops":
        call_sys = "科技信息展示系统"
    return {
        "row_id": dem.get("demand_id") or f"{page_id}-{idx:03d}",
        "page_id": page_id,
        "模块": level3 or "展示系统",
        "页面": page,
        "主项": name,
        "子项": None,
        "指标含义": name,
        "建议取值/取值口径": _s(gap) or verdict,
        "取值依据类型": "根据原文归纳",
        "调用系统": call_sys,
        "调用模块": None,
        "取数依据": _s(gap),
        "差集判定": verdict,
        "A1需规ID": dem.get("A1需规ID"),
        "A1指标叶ID": dem.get("A1指标叶ID"),
        "metric_id": dem.get("metric_id"),
        "缺口说明": _s(gap),
    }


def normalize_item(page_id, title, raw, idx, level3, level4, level5):
    item = {k: raw.get(k) for k in COLS}
    item["row_id"] = raw.get("row_id") or raw.get("demand_id") or f"{page_id}-{idx:03d}"
    item["page_id"] = page_id
    item["模块"] = item["模块"] or level3 or "展示系统"
    item["页面"] = item["页面"] or level5 or level4 or title
    return item


def datareq_row():
    return {
        "row_id": "DS-DATAREQ-FANIN-001",
        "page_id": "DS-DATAREQ",
        "模块": "数据资源",
        "页面": "数据需求清单",
        "主项": "展示数据需求清单",
        "子项": None,
        "指标含义": "展示侧数据需求清单本身；运营取数已由 DS-17～20 视窗覆盖",
        "建议取值/取值口径": "不进算法库差集",
        "取值依据类型": "根据原文归纳",
        "调用系统": "基础数据",
        "调用模块": None,
        "取数依据": "catalog skip reason=other_system",
        "差集判定": "other_system",
        "A1需规ID": None,
        "A1指标叶ID": None,
        "metric_id": None,
        "缺口说明": "catalog 指定 FANIN 一行汇总；不扫全图、不 missing。",
    }


def is_topic_repeat(item, topic_mids, topic_names):
    mid = _s(item.get("metric_id"))
    name = _s(item.get("主项"))
    note = item.get("缺口说明") or ""
    if mid and mid in topic_mids:
        return True
    if (not mid) and name and name in topic_names:
        return True
    if "also_in:" in str(note) and any(
        k in str(note)
        for k in (
            "E7-POLICY",
            "CHAIN-TOPIC",
            "SYNTH-",
            "TOPIC-",
            "SVCCHAIN-",
        )
    ):
        return True
    return False


def write_xlsx(path, rows):
    wb = Workbook()
    ws = wb.active
    ws.title = "页面指标差集"
    headers = ["row_id", "page_id"] + COLS
    fill = PatternFill("solid", fgColor="1D4ED8")
    font = Font(color="FFFFFF", bold=True, name="Microsoft YaHei", size=10)
    thin = Border(
        left=Side(style="thin", color="D0D5DD"),
        right=Side(style="thin", color="D0D5DD"),
        top=Side(style="thin", color="D0D5DD"),
        bottom=Side(style="thin", color="D0D5DD"),
    )
    wrap = Alignment(wrap_text=True, vertical="top")
    for col, h in enumerate(headers, 1):
        cell = ws.cell(1, col, h)
        cell.fill = fill
        cell.font = font
        cell.alignment = Alignment(wrap_text=True, vertical="center")
        cell.border = thin
    miss_fill = PatternFill("solid", fgColor="FEE4E2")
    for r_i, row in enumerate(rows, 2):
        for c_i, h in enumerate(headers, 1):
            val = row.get(h)
            cell = ws.cell(r_i, c_i, "" if val is None else val)
            cell.alignment = wrap
            cell.border = thin
            cell.font = Font(name="Microsoft YaHei", size=9)
            if row.get("差集判定") == "missing":
                cell.fill = miss_fill
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{max(1, len(rows) + 1)}"
    widths = {
        "A": 22,
        "B": 22,
        "C": 16,
        "D": 18,
        "E": 22,
        "F": 12,
        "G": 28,
        "H": 28,
        "I": 14,
        "J": 16,
        "K": 16,
        "L": 22,
        "M": 12,
        "N": 14,
        "O": 14,
        "P": 22,
        "Q": 40,
    }
    for col, w in widths.items():
        ws.column_dimensions[col].width = w
    ws.row_dimensions[1].height = 22
    wb.save(path)


def main():
    order, titles, skipped = load_page_order()
    topic_mids, topic_names = load_topic_missing()
    all_items = []
    page_stats = []
    debt_n = 0
    b_track_missing = []
    missing_files = []
    for pid in order:
        path = os.path.join(PAGE_DIR, pid + ".yaml")
        if not os.path.isfile(path):
            missing_files.append(pid)
            continue
        with open(path, encoding="utf-8") as f:
            doc = yaml.safe_load(f)
        items = [x for x in (doc.get("items") or []) if isinstance(x, dict)]
        demands = [x for x in (doc.get("demands") or []) if isinstance(x, dict)]
        debts = doc.get("semantic_debt") or []
        debt_n += len(debts)
        level3 = doc.get("level3")
        level4 = doc.get("level4")
        level5 = doc.get("level5")
        title = titles.get(pid)
        src = items if items else [demand_to_item(pid, title, d, i + 1, level3, level4, level5) for i, d in enumerate(demands)]
        norm = [normalize_item(pid, title, x, i + 1, level3, level4, level5) for i, x in enumerate(src)]
        for x in norm:
            if x.get("差集判定") == "missing" and is_b_track(x.get("metric_id")):
                b_track_missing.append((pid, x.get("metric_id"), x.get("主项")))
        vc = Counter(x.get("差集判定") for x in norm)
        page_stats.append(
            {
                "page_id": pid,
                "wave": doc.get("wave"),
                "n": len(norm),
                "verdicts": dict(vc),
                "semantic_debt": len(debts),
                "a_class": vc.get("missing", 0),
            }
        )
        all_items.extend(norm)

    all_items.append(datareq_row())
    page_stats.append(
        {
            "page_id": "DS-DATAREQ",
            "wave": "FANIN",
            "n": 1,
            "verdicts": {"other_system": 1},
            "semantic_debt": 0,
            "a_class": 0,
            "note": "catalog skip; one-line FANIN",
        }
    )

    vc_all = Counter(x.get("差集判定") for x in all_items)
    missing_raw = [x for x in all_items if x.get("差集判定") == "missing"]
    missing = [x for x in missing_raw if not is_topic_repeat(x, topic_mids, topic_names)]
    dropped = [x for x in missing_raw if is_topic_repeat(x, topic_mids, topic_names)]

    out_yaml = {
        "version": 1,
        "task": "DS-ALGO-GAP-L01",
        "system": "display",
        "updated": "2026-08-22",
        "source_excel_ref": "metrics/request/展示系统页面指标释义清单.xlsx",
        "page_count": len(order),
        "item_count": len(all_items),
        "verdicts": dict(vc_all),
        "missing_count": len(missing),
        "missing_dropped_topic_repeat": [
            {"page_id": x["page_id"], "metric_id": x.get("metric_id"), "主项": x.get("主项")}
            for x in dropped
        ],
        "semantic_debt_count": debt_n,
        "a1_tables_ready": False,
        "skipped": skipped,
        "b_track_missing_violations": [
            {"page_id": a, "metric_id": b, "主项": c} for a, b, c in b_track_missing
        ],
        "pages": page_stats,
        "missing": [
            {
                "row_id": x["row_id"],
                "page_id": x["page_id"],
                "模块": x["模块"],
                "页面": x["页面"],
                "主项": x["主项"],
                "metric_id": x.get("metric_id"),
                "缺口说明": x.get("缺口说明"),
            }
            for x in missing
        ],
        "items": all_items,
    }
    ypath = os.path.join(OUT_DIR, "DS-ALGO-GAP-L01.yaml")
    with open(ypath, "w", encoding="utf-8") as f:
        yaml.safe_dump(out_yaml, f, allow_unicode=True, sort_keys=False, width=120)

    csv_path = os.path.join(OUT_DIR, "_fanin.csv")
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["row_id", "page_id"] + COLS, extrasaction="ignore")
        w.writeheader()
        for row in all_items:
            w.writerow({k: ("" if row.get(k) is None else row.get(k)) for k in ["row_id", "page_id"] + COLS})

    miss_csv = os.path.join(OUT_DIR, "_fanin_missing.csv")
    with open(miss_csv, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["row_id", "page_id"] + COLS, extrasaction="ignore")
        w.writeheader()
        for row in missing:
            w.writerow({k: ("" if row.get(k) is None else row.get(k)) for k in ["row_id", "page_id"] + COLS})

    xlsx_path = os.path.join(OUT_DIR, "DS-ALGO-GAP-L01.xlsx")
    write_xlsx(xlsx_path, all_items)

    print("missing_files", missing_files)
    print("items", len(all_items))
    print("verdicts", dict(vc_all))
    print("missing_raw", len(missing_raw))
    print("missing_master", len(missing))
    print("dropped_topic_repeat", len(dropped))
    print("debt", debt_n)
    print("b_track_missing", b_track_missing)
    for m in missing:
        print("MISSING", m["page_id"], m.get("metric_id"), m["主项"])
    for d in dropped:
        print("DROPPED", d["page_id"], d.get("metric_id"), d["主项"])


if __name__ == "__main__":
    main()

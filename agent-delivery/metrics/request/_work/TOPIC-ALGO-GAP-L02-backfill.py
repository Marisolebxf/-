# TOPIC-ALGO-GAP-L02: fill A1 IDs from ALGO-LIB-METRIC-DEPS-L01 tables.
# ponytail: off — definition backfill; do not invent M_*.
from __future__ import annotations

import copy
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
REQ_PATH = ROOT / "metrics/algo-results/ALGO-LIB-METRIC-DEPS-L01-requirements.yaml"
MET_PATH = ROOT / "metrics/algo-results/ALGO-LIB-METRIC-DEPS-L01-metrics.yaml"
L01_PATH = ROOT / "metrics/request/专题系统/TOPIC-ALGO-GAP-L01.yaml"
PAGES_DIR = ROOT / "metrics/request/专题系统/pages"
OUT_DIR = ROOT / "metrics/request/专题系统"
WORK = ROOT / "metrics/request/_work"

ALIAS_TITLE = {
    "深圳产业要素": "产业链基础指标模型构建",
    "深圳产业分布": "产业链基础指标模型构建",
}

# 页面未挂 algo_lib_leaf、但 L01 已 mapped（B 轨覆盖）的深圳四维对比 → A1 深圳产业链模型叶
ROW_A1_OVERRIDE = {
    "TOPIC-SZ-011": "ALGO-CHAIN-DEEP-118",
    "TOPIC-SZ-012": "ALGO-CHAIN-DEEP-118",
    "TOPIC-SZ-013": "ALGO-CHAIN-DEEP-118",
    "TOPIC-SZ-014": "ALGO-CHAIN-DEEP-118",
}

MODULE_DIM = {
    "产业链分析": "产业链",
    "产业服务链分析": "产业服务",
    "政策分析": "政策",
    "综合智能分析": "综合",
    "企业分析": "企业",
    "技术链分析": "技术链",
    "科研机构分析": "科研机构",
    "人才分析": "人才",
}

ENT_BASE_HINTS = [
    ("重点企业", "M_ENT_KEY_TOTAL"),
    ("类型", "M_ENT_TYPE_COUNT"),
    ("领域", "M_ENT_DOMAIN_COVERAGE_COUNT"),
    ("资讯", "TEMP_ALGO_ALGO-ENT-BASE-97_4"),
    ("新增", "M_ENT_NEW_COUNT_Y"),
]

ITEM_KEYS = [
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
    "row_id",
    "page_id",
]


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def leaf_title(algo_lib_leaf):
    if not algo_lib_leaf:
        return None
    s = str(algo_lib_leaf).strip().strip('"').strip("'")
    if "#" in s:
        return s.split("#", 1)[1].strip()
    return s.strip() or None


def token_overlap(a: str, b: str) -> int:
    if not a or not b:
        return 0
    stop = set("的与及和或及模型构建分析评价识别综合")
    def toks(s):
        parts = re.findall(r"[\u4e00-\u9fff]{2,}|[A-Za-z0-9_]+", s)
        return [p for p in parts if p not in stop]
    ta, tb = set(toks(a)), set(toks(b))
    return len(ta & tb)


def pick_metric_ids(req, name_zh: str):
    mets = req.get("metrics") or []
    if not mets:
        return []
    ids = [m["metric_id"] for m in mets]
    if len(ids) == 1:
        return ids
    name = name_zh or ""
    if req["requirement_id"] == "ALGO-ENT-BASE-97":
        hit = [mid for hint, mid in ENT_BASE_HINTS if hint in name and mid in ids]
        if hit:
            return hit
    scored = []
    for m in mets:
        scored.append((token_overlap(name, m.get("metric_name_zh") or ""), m["metric_id"]))
    scored.sort(key=lambda x: x[0], reverse=True)
    if scored[0][0] > 0:
        best = scored[0][0]
        return [mid for s, mid in scored if s == best]
    return [ids[0]]


def parse_seq_05(text: str):
    if not text:
        return []
    seqs = [int(x) for x in re.findall(r"05\s*seq\s*(\d+)", text, flags=re.I)]
    seqs += [int(x) for x in re.findall(r"srs/05[^。；\n]{0,40}seq\s*(\d+)", text, flags=re.I)]
    seqs += [int(x) for x in re.findall(r"算法库\s*seq\s*(\d+)", text)]
    return seqs


def parse_titles_in_text(text: str):
    if not text:
        return []
    titles = []
    for m in re.findall(r"#([\u4e00-\u9fffA-Za-z0-9·\-]+)", text):
        titles.append(m)
    for m in re.findall(r"「([^」]+)」", text):
        titles.append(m)
    return titles


def main():
    req_doc = load_yaml(REQ_PATH)
    met_doc = load_yaml(MET_PATH)
    l01 = load_yaml(L01_PATH)

    reqs = req_doc["requirements"]
    assert len(reqs) == 97, len(reqs)
    by_title = {}
    by_seq = {}
    by_rid = {}
    for r in reqs:
        by_title[r["requirement_title"]] = r
        by_seq[int(r["seq"])] = r
        by_rid[r["requirement_id"]] = r

    a1_metric_ids = {m["metric_id"] for m in met_doc["metrics"]}
    assert len(a1_metric_ids) == 101, len(a1_metric_ids)
    formal_m = sorted(x for x in a1_metric_ids if x.startswith("M_"))
    temp_m = sorted(x for x in a1_metric_ids if x.startswith("TEMP_ALGO_"))
    assert len(formal_m) == 11 and len(temp_m) == 90, (len(formal_m), len(temp_m))

    demands = []
    for p in sorted(PAGES_DIR.glob("*.yaml")):
        if p.name.startswith("_"):
            continue
        doc = load_yaml(p)
        page_id = doc.get("page_id")
        for d in doc.get("demands") or []:
            d = dict(d)
            d["_page_id"] = page_id
            demands.append(d)

    demands_by_page = defaultdict(list)
    demand_by_id = {}
    for d in demands:
        demands_by_page[d["_page_id"]].append(d)
        demand_by_id[d["demand_id"]] = d

    items = l01["items"]
    assert len(items) == 250, len(items)

    def resolve_req(title, item):
        if not title:
            return None
        title = ALIAS_TITLE.get(title, title)
        if title in by_title:
            return by_title[title]
        # unique substring
        hits = [r for t, r in by_title.items() if title in t or t in title]
        if len(hits) == 1:
            return hits[0]
        dim = MODULE_DIM.get(item.get("模块"))
        if dim:
            hits = [r for r in hits if r.get("dimension") == dim]
            if len(hits) == 1:
                return hits[0]
        return None

    def find_demand(item):
        page_id = item.get("page_id")
        page_demands = demands_by_page.get(page_id) or []
        mid = item.get("metric_id")
        name = item.get("主项") or ""
        if mid:
            hits = [d for d in page_demands if d.get("metric_id") == mid]
            if len(hits) == 1:
                return hits[0]
            if len(hits) > 1:
                hits2 = [d for d in hits if (d.get("metric_name_zh") == name) or (d.get("差集判定") == item.get("差集判定"))]
                return (hits2 or hits)[0]
        hits = [d for d in page_demands if d.get("metric_name_zh") == name]
        if len(hits) == 1:
            return hits[0]
        if len(hits) > 1:
            hits2 = [d for d in hits if d.get("差集判定") == item.get("差集判定")]
            return (hits2 or hits)[0]
        # startswith / contain
        hits = [d for d in page_demands if name and d.get("metric_name_zh") and (name in d["metric_name_zh"] or d["metric_name_zh"] in name)]
        if hits:
            hits2 = [d for d in hits if d.get("差集判定") == item.get("差集判定")]
            return (hits2 or hits)[0]
        return None

    MISSING_KEEP = {
        "TOPIC-PAN-006",
        "TOPIC-PAN-007",
        "TOPIC-DIAG-018",
        "TOPIC-SZ-016",
        "TOPIC-POL-005",
        "TOPIC-ELEM-009",
        "TOPIC-COL-006",
    }

    # Re-check missing against A1 titles: only flip if a dedicated leaf exists.
    missing_titles_forbidden_as_cover = {
        "TOPIC-PAN-006": ("产品计数", "关联产品"),
        "TOPIC-PAN-007": ("专利计数", "关联专利"),
        "TOPIC-DIAG-018": ("环节健康",),
        "TOPIC-SZ-016": ("成功案例",),
        "TOPIC-POL-005": ("产业适配",),
        "TOPIC-ELEM-009": ("贡献度", "影响路径"),
        "TOPIC-COL-006": ("产出关联", "相关系数"),
    }
    a1_title_blob = " ".join(r["requirement_title"] for r in reqs)
    a1_metric_blob = " ".join((m.get("metric_name_zh") or "") + " " + (m.get("definition") or "") for m in met_doc["metrics"])
    missing_flip = []
    for row_id, keys in missing_titles_forbidden_as_cover.items():
        if any(k in a1_title_blob for k in keys) or any(k in a1_metric_blob for k in keys):
            missing_flip.append({"row_id": row_id, "keys": keys})

    fill_log = []
    unmatched_mapped = []
    verdict_changes = []

    for item in items:
        row_id = item["row_id"]
        verdict = item.get("差集判定")
        demand = find_demand(item)
        req = None
        how = None
        title = leaf_title(demand.get("algo_lib_leaf") if demand else None)
        if title:
            req = resolve_req(title, item)
            if req:
                how = "algo_lib_leaf"
        if req is None:
            blob = " ".join(
                str(x or "")
                for x in [
                    item.get("取数依据"),
                    item.get("缺口说明"),
                    (demand or {}).get("缺口说明"),
                    (demand or {}).get("note"),
                    (demand or {}).get("algo_lib_leaf"),
                ]
            )
            for t in parse_titles_in_text(blob):
                req = resolve_req(t, item)
                if req:
                    how = "text_title"
                    break
            if req is None:
                seqs = [s for s in parse_seq_05(blob) if s in by_seq]
                if seqs:
                    req = by_seq[seqs[0]]
                    how = "05_seq"
        if req is None and item.get("row_id") in ROW_A1_OVERRIDE:
            req = by_rid[ROW_A1_OVERRIDE[item["row_id"]]]
            how = "row_override"
        if req is None and verdict in ("mapped", "third_party"):
            # last resort: unique title overlap with 主项 within dimension
            dim = MODULE_DIM.get(item.get("模块"))
            name = item.get("主项") or ""
            cands = [r for r in reqs if (dim is None or r["dimension"] == dim) and token_overlap(name, r["requirement_title"]) >= 2]
            if len(cands) == 1:
                req = cands[0]
                how = "title_overlap"

        a1_rid = None
        a1_leaf = None
        if req and verdict in ("mapped", "third_party"):
            name = (demand.get("metric_name_zh") if demand else None) or item.get("主项") or ""
            a1_rid = req["requirement_id"]
            a1_leaf = ",".join(pick_metric_ids(req, name))
            item["A1需规ID"] = a1_rid
            item["A1指标叶ID"] = a1_leaf
        elif verdict == "missing":
            # keep missing; do not invent coverage
            item["A1需规ID"] = None
            item["A1指标叶ID"] = None
            if row_id not in MISSING_KEEP:
                unmatched_mapped.append({"row_id": row_id, "reason": "unexpected_missing"})
        else:
            item["A1需规ID"] = None
            item["A1指标叶ID"] = None

        # never put TEMP into metric_id; never invent M_*
        mid = item.get("metric_id")
        if isinstance(mid, str) and mid.startswith("TEMP_ALGO_"):
            raise SystemExit(f"TEMP in metric_id col14: {row_id} {mid}")
        if isinstance(mid, str) and mid.startswith("M_") and mid not in a1_metric_ids:
            pass  # B-track / semantic layer ID — keep
        if isinstance(item.get("A1指标叶ID"), str):
            for part in item["A1指标叶ID"].split(","):
                if part and part not in a1_metric_ids:
                    raise SystemExit(f"invented A1 leaf id: {row_id} {part}")

        if verdict in ("mapped", "third_party") and item.get("A1需规ID"):
            fill_log.append(
                {
                    "row_id": row_id,
                    "page_id": item.get("page_id"),
                    "主项": item.get("主项"),
                    "差集判定": verdict,
                    "metric_id": item.get("metric_id"),
                    "A1需规ID": item.get("A1需规ID"),
                    "A1指标叶ID": item.get("A1指标叶ID"),
                    "how": how,
                    "demand_id": demand.get("demand_id") if demand else None,
                }
            )
        elif verdict == "mapped" and not item.get("A1需规ID"):
            unmatched_mapped.append(
                {
                    "row_id": row_id,
                    "page_id": item.get("page_id"),
                    "主项": item.get("主项"),
                    "差集判定": verdict,
                    "metric_id": item.get("metric_id"),
                    "demand_id": demand.get("demand_id") if demand else None,
                    "algo_lib_leaf": demand.get("algo_lib_leaf") if demand else None,
                    "取数依据": item.get("取数依据"),
                }
            )

    # same metric_id already filled on another page (门户复用分析侧)
    filled_by_mid = {}
    for it in items:
        if it.get("差集判定") == "mapped" and it.get("metric_id") and it.get("A1需规ID"):
            filled_by_mid.setdefault(it["metric_id"], it)
    still = []
    for u in unmatched_mapped:
        it = next(x for x in items if x["row_id"] == u["row_id"])
        src = filled_by_mid.get(it.get("metric_id"))
        if src:
            it["A1需规ID"] = src["A1需规ID"]
            it["A1指标叶ID"] = src["A1指标叶ID"]
            fill_log.append(
                {
                    "row_id": it["row_id"],
                    "page_id": it.get("page_id"),
                    "主项": it.get("主项"),
                    "差集判定": "mapped",
                    "metric_id": it.get("metric_id"),
                    "A1需规ID": it["A1需规ID"],
                    "A1指标叶ID": it["A1指标叶ID"],
                    "how": "reuse_same_metric_id",
                    "demand_id": None,
                }
            )
        else:
            still.append(u)
    unmatched_mapped = still

    third_party_unfilled = [
        {
            "row_id": it["row_id"],
            "主项": it.get("主项"),
            "page_id": it.get("page_id"),
            "缺口说明": it.get("缺口说明"),
        }
        for it in items
        if it.get("差集判定") == "third_party" and not it.get("A1需规ID")
    ]

    # demand-level fill map
    by_row = {x["row_id"]: x for x in fill_log}
    item_by_row = {it["row_id"]: it for it in items}
    by_demand = {}
    for d in demands:
        # attach from matching item
        rec = None
        for it in items:
            if it.get("page_id") != d.get("_page_id"):
                continue
            if d.get("metric_id") and it.get("metric_id") == d.get("metric_id"):
                rec = it
                break
            if it.get("主项") == d.get("metric_name_zh"):
                rec = it
                break
        if rec and rec.get("A1需规ID"):
            by_demand[d["demand_id"]] = {
                "A1需规ID": rec["A1需规ID"],
                "A1指标叶ID": rec["A1指标叶ID"],
            }
        elif d.get("差集判定") in ("mapped", "third_party"):
            title = leaf_title(d.get("algo_lib_leaf"))
            dummy = {"模块": None, "主项": d.get("metric_name_zh")}
            # infer module from page later; try title only
            req = resolve_req(title, dummy) if title else None
            if req:
                by_demand[d["demand_id"]] = {
                    "A1需规ID": req["requirement_id"],
                    "A1指标叶ID": ",".join(pick_metric_ids(req, d.get("metric_name_zh") or "")),
                }

    report = {
        "a1_req": 97,
        "a1_metrics": 101,
        "a1_formal_M": formal_m,
        "item_count": len(items),
        "verdicts": dict(Counter(it.get("差集判定") for it in items)),
        "missing_flip_candidates": missing_flip,
        "missing_keep": sorted(MISSING_KEEP),
        "filled": len(fill_log),
        "unmatched_mapped": unmatched_mapped,
        "third_party_unfilled": third_party_unfilled,
        "verdict_changes": verdict_changes,
        "filled_by_how": dict(Counter(x["how"] for x in fill_log)),
        "filled_mapped": sum(1 for x in fill_log if x["差集判定"] == "mapped"),
        "filled_third_party": sum(1 for x in fill_log if x["差集判定"] == "third_party"),
    }
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / "TOPIC-ALGO-GAP-L02-match-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    with (WORK / "TOPIC-ALGO-GAP-L02-fill-log.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["row_id", "page_id", "主项", "差集判定", "metric_id", "A1需规ID", "A1指标叶ID", "how", "demand_id"],
        )
        w.writeheader()
        w.writerows(fill_log)

    if unmatched_mapped:
        print("UNMATCHED", json.dumps(unmatched_mapped, ensure_ascii=False, indent=2))
        raise SystemExit(f"unmatched mapped/third_party: {len(unmatched_mapped)}")
    if missing_flip:
        print("MISSING_FLIP_CANDIDATES (kept missing unless dedicated leaf):", missing_flip)

    # ----- write L02 yaml -----
    out = copy.deepcopy(l01)
    out["task"] = "TOPIC-ALGO-GAP-L02"
    out["updated"] = "2026-08-24"
    out["round"] = "L02-A1-backfill"
    out["a1_tables_ready"] = True
    out["a1_source"] = {
        "table1": "metrics/algo-results/ALGO-LIB-METRIC-DEPS-L01-requirements.yaml",
        "table2": "metrics/algo-results/ALGO-LIB-METRIC-DEPS-L01-metrics.yaml",
    }
    out["library_missing_unchanged"] = 7
    out["l02_note"] = (
        "对照 A1 表1/表2 回填 mapped（及 third_party）的 A1需规ID / A1指标叶ID。"
        "列 14 metric_id 保留语义层/B 轨已有 ID，不把 TEMP_ALGO_* 写入 metric_id，不编造 M_*。"
        "Round 17 OPEN 指针不回滚。库 missing 7→7：A1 97 叶仍无产品计数/链级专利计数/环节健康度/"
        "全球成功案例/产业适配性/要素贡献路径/协同—产出相关专叶。"
    )
    out["items"] = items
    out["missing_count"] = 7
    out["verdicts"]["missing"] = 7
    l02_yaml = OUT_DIR / "TOPIC-ALGO-GAP-L02.yaml"
    with l02_yaml.open("w", encoding="utf-8") as f:
        yaml.safe_dump(out, f, allow_unicode=True, sort_keys=False, width=120)
    print("wrote", l02_yaml)

    # ----- xlsx -----
    write_xlsx(items, fill_log)

    # ----- pages additive fill -----
    fill_pages(by_demand, item_by_row)

    print("filled", len(fill_log), "unmatched", len(unmatched_mapped))


def write_xlsx(items, fill_log):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.table import Table, TableStyleInfo

    headers = [
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
        "row_id",
        "page_id",
    ]
    wb = Workbook()
    ws = wb.active
    ws.title = "清单"
    header_font = Font(name="Calibri", bold=True, color="FFFFFF")
    header_fill = PatternFill("solid", fgColor="165DFF")
    thin = Border(
        left=Side(style="thin", color="D0D5DD"),
        right=Side(style="thin", color="D0D5DD"),
        top=Side(style="thin", color="D0D5DD"),
        bottom=Side(style="thin", color="D0D5DD"),
    )
    wrap = Alignment(wrapText=True, vertical="top")
    for col, h in enumerate(headers, 1):
        cell = ws.cell(1, col, h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(wrapText=True, vertical="center")
        cell.border = thin
    miss_fill = PatternFill("solid", fgColor="FDECEC")
    map_fill = PatternFill("solid", fgColor="E8F3FF")
    for i, it in enumerate(items, 2):
        for col, h in enumerate(headers, 1):
            val = it.get(h)
            if val is None:
                val = ""
            cell = ws.cell(i, col, val)
            cell.font = Font(name="Calibri", size=11)
            cell.alignment = wrap
            cell.border = thin
            if it.get("差集判定") == "missing":
                cell.fill = miss_fill
            elif it.get("差集判定") == "mapped" and h in ("A1需规ID", "A1指标叶ID"):
                cell.fill = map_fill
    ws.auto_filter.ref = f"A1:Q{len(items)+1}"
    ws.freeze_panes = "A2"
    widths = {
        "A": 16, "B": 20, "C": 28, "D": 14, "E": 36, "F": 36, "G": 16, "H": 18, "I": 18,
        "J": 40, "K": 14, "L": 28, "M": 36, "N": 28, "O": 44, "P": 18, "Q": 22,
    }
    for col, w in widths.items():
        ws.column_dimensions[col].width = w
    ws.row_dimensions[1].height = 22
    for r in range(2, len(items) + 2):
        ws.row_dimensions[r].height = 36
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.print_title_rows = "1:1"

    sc = wb.create_sheet("计数")
    sc["A1"] = "TOPIC-ALGO-GAP-L02 计数"
    sc["A1"].font = Font(name="Calibri", bold=True, size=14, color="165DFF")
    sc.merge_cells("A1:C1")
    labels = [
        (3, "清单行", f"=COUNTA(清单!P2:P{len(items)+1})"),
        (4, "missing", '=COUNTIF(清单!K:K,"missing")'),
        (5, "mapped", '=COUNTIF(清单!K:K,"mapped")'),
        (6, "third_party", '=COUNTIF(清单!K:K,"third_party")'),
        (7, "other_system", '=COUNTIF(清单!K:K,"other_system")'),
        (8, "n/a_ops", '=COUNTIF(清单!K:K,"n/a_ops")'),
        (9, "mapped 已回填 A1需规ID", '=COUNTIFS(清单!K:K,"mapped",清单!L:L,"<>")'),
        (10, "missing 旧", 7),
        (11, "missing 新", '=B4'),
        (12, "改判定行数", 0),
    ]
    sc["A3"] = "口径"
    sc["B3"] = "值"
    sc["A3"].font = header_font
    sc["B3"].font = header_font
    sc["A3"].fill = header_fill
    sc["B3"].fill = header_fill
    # rewrite cleanly
    sc["A3"] = "口径"
    sc["B3"] = "值"
    rows = [
        ("清单行", f"=COUNTA(清单!P2:P{1+len(items)})"),
        ("missing", '=COUNTIF(清单!K:K,"missing")'),
        ("mapped", '=COUNTIF(清单!K:K,"mapped")'),
        ("third_party", '=COUNTIF(清单!K:K,"third_party")'),
        ("other_system", '=COUNTIF(清单!K:K,"other_system")'),
        ("n/a_ops", '=COUNTIF(清单!K:K,"n/a_ops")'),
        ("mapped 已填 A1需规ID", f'=COUNTIFS(清单!K2:K{1+len(items)},"mapped",清单!L2:L{1+len(items)},"<>")'),
        ("missing 旧", 7),
        ("missing 新", "=B4"),
        ("改判定行数", 0),
    ]
    for idx, (lab, val) in enumerate(rows, 4):
        sc.cell(idx, 1, lab).font = Font(name="Calibri", size=11)
        cell = sc.cell(idx, 2, val)
        cell.font = Font(name="Calibri", size=11)
        if lab == "missing":
            cell.fill = miss_fill
    sc.column_dimensions["A"].width = 28
    sc.column_dimensions["B"].width = 18
    sc["A16"] = "missing 7 条维持（A1 97 叶无专叶）。禁止把 TEMP_ALGO_* 当作已入 seed。"
    sc["A16"].font = Font(name="Calibri", size=11)
    sc.merge_cells("A16:F16")
    sc.page_setup.orientation = "landscape"
    sc.page_setup.fitToPage = True
    sc.page_setup.fitToWidth = 1
    sc.page_setup.fitToHeight = 1

    sh = wb.create_sheet("回填清单")
    fh = ["row_id", "page_id", "主项", "差集判定", "metric_id", "A1需规ID", "A1指标叶ID", "how"]
    for col, h in enumerate(fh, 1):
        cell = sh.cell(1, col, h)
        cell.font = header_font
        cell.fill = header_fill
        cell.border = thin
    for i, row in enumerate(fill_log, 2):
        for col, h in enumerate(fh, 1):
            cell = sh.cell(i, col, row.get(h) or "")
            cell.font = Font(name="Calibri", size=11)
            cell.alignment = wrap
            cell.border = thin
    sh.freeze_panes = "A2"
    sh.auto_filter.ref = f"A1:H{len(fill_log)+1}"
    for col, w in enumerate([18, 22, 28, 14, 28, 28, 40, 16], 1):
        sh.column_dimensions[get_column_letter(col)].width = w
    sh.page_setup.orientation = "landscape"
    sh.page_setup.fitToWidth = 1
    sh.page_setup.fitToHeight = 0

    path = OUT_DIR / "TOPIC-ALGO-GAP-L02.xlsx"
    wb.save(path)
    print("wrote", path)


def fill_pages(by_demand, item_by_row):
    demand_re = re.compile(r"^(\s*)-\s*demand_id:\s*(\S+)")
    row_re = re.compile(r"^(\s*)-\s*row_id:\s*(\S+)")
    a1_re = re.compile(r"^(\s*)A1需规ID:\s*")
    for p in sorted(PAGES_DIR.glob("*.yaml")):
        if p.name.startswith("_"):
            continue
        lines = p.read_text(encoding="utf-8").splitlines(keepends=True)
        current_demand = None
        current_row = None
        out = []
        i = 0
        changed = False
        while i < len(lines):
            line = lines[i]
            md = demand_re.match(line)
            if md:
                current_demand = md.group(2).strip()
                current_row = None
            mr = row_re.match(line)
            if mr:
                current_row = mr.group(2).strip()
                current_demand = None
            am = a1_re.match(line)
            rec = None
            if am:
                if current_demand and current_demand in by_demand:
                    rec = by_demand[current_demand]
                elif current_row and current_row in item_by_row:
                    it = item_by_row[current_row]
                    if it.get("A1需规ID"):
                        rec = {"A1需规ID": it["A1需规ID"], "A1指标叶ID": it.get("A1指标叶ID")}
            if rec:
                indent = am.group(1)
                rid = rec["A1需规ID"]
                leaf = rec.get("A1指标叶ID") or "null"
                out.append(f"{indent}A1需规ID: {rid}\n")
                changed = True
                nxt = lines[i + 1] if i + 1 < len(lines) else ""
                if re.match(r"^\s*A1指标叶ID:", nxt):
                    i += 1
                    out.append(f"{indent}A1指标叶ID: {leaf}\n")
                else:
                    out.append(f"{indent}A1指标叶ID: {leaf}\n")
                i += 1
                continue
            out.append(line)
            i += 1
        text = "".join(out)
        # stamp updated date only if file still says 2026-08-22 A1 未交 — keep OPEN fields
        if "A1 双表未交" in text:
            text = text.replace("A1 双表未交（A2-GAP-algo-catalog.a1_tables_ready=false）→ A1需规ID 一律空。",
                                "A1 已交（TOPIC-ALGO-GAP-L02）：mapped 回填 A1需规ID / A1指标叶ID；不回滚 OPEN 指针。")
            text = text.replace("A1 表未交 → A1需规ID 一律 null",
                                "A1 已交 → mapped 回填 A1需规ID / A1指标叶ID")
            text = text.replace("# A1 双表未交（A2-GAP-algo-catalog.a1_tables_ready=false）→ A1需规ID 一律空。",
                                "# A1 已交（TOPIC-ALGO-GAP-L02）回填 A1 ID；不回滚 OPEN。")
        if "updated: \"2026-08-22\"" in text:
            text = text.replace("updated: \"2026-08-22\"", "updated: \"2026-08-24\"", 1)
        if "updated: '2026-08-22'" in text:
            text = text.replace("updated: '2026-08-22'", "updated: '2026-08-24'", 1)
        # never touch metric_open_status
        p.write_text(text, encoding="utf-8")
        print("updated page", p.name, "changed_a1", changed)


if __name__ == "__main__":
    main()

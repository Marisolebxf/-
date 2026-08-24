# -*- coding: utf-8 -*-
"""对照分析清单 vs metrics/registry（走 metric-registry-lib，不整文件读 seed）。"""
from __future__ import annotations

import json
import subprocess
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
REQ = ROOT / "metrics" / "request"
ALGO = ROOT / "metrics" / "algo-results"
OUT = REQ / "_work" / "ALGO-LIB-T0X-L01-registry-coverage.json"
ORCH = Path(__file__).resolve().parents[4]


def load(p: Path):
    with p.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def ids_from_items(items: list, verdicts: set[str]) -> tuple[list[str], int, list[str]]:
    """return (unique M_* in order, null_count, row_ids_without_id)"""
    seen: list[str] = []
    seen_set: set[str] = set()
    null_n = 0
    no_id_rows: list[str] = []
    for it in items:
        if it.get("差集判定") not in verdicts:
            continue
        mid = it.get("metric_id")
        rid = it.get("row_id") or ""
        if not mid or str(mid).strip() in ("", "None", "null"):
            null_n += 1
            no_id_rows.append(rid)
            continue
        s = str(mid).strip()
        if s not in seen_set:
            seen_set.add(s)
            seen.append(s)
    return seen, null_n, no_id_rows


def a1_ids(doc: dict) -> tuple[list[str], list[str]]:
    formal, temp = [], []
    for m in doc.get("metrics") or []:
        mid = str(m.get("metric_id") or "").strip()
        if not mid:
            continue
        if mid.startswith("TEMP_"):
            temp.append(mid)
        else:
            formal.append(mid)
    return formal, temp


def lookup(ids: list[str]) -> dict:
    ids_path = REQ / "_work" / "ALGO-LIB-T0X-L01-registry-ids.json"
    ids_path.write_text(json.dumps(ids, ensure_ascii=False), encoding="utf-8")
    lookup_js = Path(__file__).with_name("ALGO-LIB-T0X-L01-registry-lookup.mjs")
    proc = subprocess.run(
        ["node", str(lookup_js), str(ids_path)],
        cwd=str(ORCH),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if proc.returncode != 0:
        raise SystemExit(proc.stderr or proc.stdout)
    return json.loads(proc.stdout)


def tally(rows: list[dict]) -> dict:
    c = Counter()
    missing = []
    for r in rows:
        if r.get("missing") or not r.get("seed"):
            c["not_in_seed"] += 1
            missing.append(r["metric_id"])
        else:
            c["in_seed"] += 1
    return {"in_seed": c["in_seed"], "not_in_seed": c["not_in_seed"], "not_in_seed_ids": missing}


def main() -> None:
    topic = load(REQ / "专题系统" / "TOPIC-ALGO-GAP-L02.yaml")
    display = load(REQ / "展示系统" / "DS-ALGO-GAP-L02.yaml")
    a1 = load(ALGO / "ALGO-LIB-METRIC-DEPS-L01-metrics.yaml")
    t0x = load(REQ / "T0X" / "ALGO-LIB-T0X-L01-pre-meeting.yaml")

    mapped_t, null_mt, _ = ids_from_items(topic["items"], {"mapped"})
    mapped_d, null_md, _ = ids_from_items(display["items"], {"mapped"})
    miss_t, null_xt, rows_xt = ids_from_items(topic["items"], {"missing"})
    miss_d, null_xd, rows_xd = ids_from_items(display["items"], {"missing"})

    # T0X 77 主清单
    fl_ids, fl_null, fl_no = [], 0, []
    seen = set()
    for it in t0x["f_minus_l"]:
        mid = it.get("metric_id")
        rid = it.get("row_id") or ""
        if not mid:
            fl_null += 1
            fl_no.append(rid)
        else:
            s = str(mid).strip()
            if s not in seen:
                seen.add(s)
                fl_ids.append(s)

    a1_formal, a1_temp = a1_ids(a1)
    all_lookup = list(dict.fromkeys(mapped_t + mapped_d + miss_t + miss_d + fl_ids + a1_formal))
    raw = lookup(all_lookup)
    by_id = {r["metric_id"]: r for r in raw["rows"]}

    def pack(ids: list[str], null_n: int, no_rows: list[str] | None = None) -> dict:
        rows = [by_id[i] for i in ids if i in by_id]
        t = tally(rows)
        return {
            "unique_M_star": len(ids),
            "rows_without_metric_id": null_n,
            "no_id_row_ids": no_rows or [],
            **t,
        }

    out = {
        "registry_summary": raw["summary"],
        "F交L_专题_mapped": pack(mapped_t, null_mt),
        "F交L_展示_mapped": pack(mapped_d, null_md),
        "F减L_专题_missing": pack(miss_t, null_xt, rows_xt),
        "F减L_展示_missing": pack(miss_d, null_xd, rows_xd),
        "F减L_T0X_77": pack(fl_ids, fl_null, fl_no),
        "A1_表2_正式M": pack(a1_formal, 0),
        "A1_表2_TEMP_ALGO": {"count": len(a1_temp), "in_seed": 0, "note": "TEMP_ALGO_* 按 SEED-TYPE 不入 seed"},
        "F减L_有号但未入seed": [i for i in fl_ids if not by_id.get(i, {}).get("seed")],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k != "registry_summary"}, ensure_ascii=False, indent=2))
    print("--- registry_summary ---")
    print(json.dumps(out["registry_summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

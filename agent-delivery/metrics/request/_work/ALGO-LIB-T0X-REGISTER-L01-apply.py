# -*- coding: utf-8 -*-
"""ALGO-LIB-T0X-REGISTER-L01 — register analysis-list identities into metrics/registry.

D1=draft, algorithm_type=UNKNOWN. Append-only. Does not rewrite existing bodies.
Does not copy A1 algorithm.type. Does not write TEMP_* as seed metric_id.
"""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

import yaml

ROOT = Path(__file__).resolve().parents[4]
REQ = ROOT / "agent-delivery" / "metrics" / "request"
ALGO = ROOT / "agent-delivery" / "metrics" / "algo-results"
REG = ROOT / "agent-delivery" / "metrics" / "registry"
WORK = Path(__file__).resolve().parent

TODAY = "2026-08-24"
TASK = "ALGO-LIB-T0X-REGISTER-L01"
GAP = "GAP-ALGO-TYPE-UNSIGNED"
FL_REUSE = {
    "M_CHAIN_PRODUCT_COUNT",
    "M_CHAIN_PATENT_COUNT",
    "M_POLICY_INDUSTRY_FIT",
    "M_SYNTH_ELEM_CONTRIB",
    "M_SYNTH_COLLAB_OUTPUT_CORR",
}
FL_SPECIAL = {
    "TOPIC-DIAG-018": "M_CHAIN_LINK_HEALTH",
    "TOPIC-SZ-016": "M_CHAIN_GLOBAL_CASE_MATCH",
}
SEED_MARKER = {
    "ENT": "# 状态分布汇总",
    "CHAIN": "# 状态分布汇总",
    "POLICY": "# 状态分布汇总",
}
MAT_MARKER = {
    "ENT": "# 汇总",
}
POLICY_MATRIX_HEADER = """\
# metric-readiness-matrix —— 政策域（POLICY）四维就绪度
# ============================================================================
# 生成任务：ALGO-LIB-T0X-REGISTER-L01 · 2026-08-24 · 监管 human:淮政玮
# 模型：data-lineage-policy.md §2.3
# D1=draft；D2=pending；D3=pending_ods；D4=mock。禁止改绿。
# lifecycle_stage=open。本文件为 POLICY 矩阵首份（存量 19 条 POLICY seed 不在此重复登记）。
# ============================================================================

version: 1
module: POLICY
model_ref: data-lineage-policy.md#2.3
model_status: provisional
updated: "2026-08-24"
as_of: "2026-08-24"
d2_verifier: lineage-subcoord
d4_batch: t0x_register_20260824
register_task: ALGO-LIB-T0X-REGISTER-L01
coverage_notes:
  - "T0-X 分析清单身份注册；D1=draft，公式/类型未签。"
  - "不改 A2 库 missing 为 mapped。"
  - "D2/D3/D4 本批不改绿。"

metrics:
"""


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def dump_catalog():
    js = WORK / "ALGO-LIB-T0X-REGISTER-L01-dump-catalog.mjs"
    proc = subprocess.run(
        ["node", str(js)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if proc.returncode != 0:
        raise SystemExit(proc.stderr or proc.stdout or "catalog dump failed")
    return json.loads(proc.stdout)


def domain_of(metric_id: str) -> str:
    m = re.match(r"^M_([A-Z]+)_", metric_id)
    if not m:
        raise ValueError(f"not M_*: {metric_id}")
    return m.group(1)


def sanitize(s: str) -> str:
    t = re.sub(r"[^A-Za-z0-9]+", "_", s or "").strip("_").upper()
    return re.sub(r"_+", "_", t)


def page_domain(page_id, module) -> str:
    blob = f"{page_id or ''} {module or ''}"
    if any(k in blob for k in ("TALENT", "人才")):
        return "TALENT"
    if any(k in blob for k in ("POLICY", "政策")):
        return "POLICY"
    if any(k in blob for k in ("GRAPH", "图谱", "SYNTH", "综合")):
        return "SYNTH"
    if any(k in blob for k in ("CHAIN", "产业链", "TOPIC-DIAG", "TOPIC-SZ", "TOPIC-PAN")):
        return "CHAIN"
    if any(k in blob for k in ("ORG", "机构")):
        return "ORG"
    if any(k in blob for k in ("TECH", "技术")):
        return "TECH"
    if "企业" in blob or ("ENT" in blob and "EVENT" not in blob):
        return "ENT"
    if any(k in blob for k in ("SVC", "服务")):
        return "SVC"
    return "INNOV"


def formal_from_temp(temp_id: str) -> str:
    m = re.match(r"^TEMP_ALGO_ALGO-([A-Z]+)-([A-Z0-9]+)-(\d+)_(\d+)$", temp_id)
    if not m:
        raise ValueError(f"unexpected TEMP id: {temp_id}")
    dom, kind, num, seq = m.group(1), m.group(2), m.group(3), m.group(4)
    if kind == "SYNTH" and dom == "SYNTH":
        return f"M_SYNTH_{num}_{seq}"
    return f"M_{dom}_{kind}_{num}_{seq}"


def ensure_len(text: str) -> str:
    d = re.sub(r"\s+", " ", (text or "").strip())
    if len(d) < 50:
        d += " 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。"
    return d


def dq(s: str) -> str:
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def emit_seed_item(m: dict) -> str:
    k, b = "    ", "      "
    return "\n".join(
        [
            f"  - metric_id: {m['metric_id']}",
            f"{k}metric_name_zh: {dq(m['metric_name_zh'])}",
            f"{k}definition: >",
            f"{b}{m['definition']}",
            f"{k}formula: {dq(m['formula'])}",
            f"{k}algorithm_type: UNKNOWN",
            f"{k}source_tables: [pending_ods]",
            f"{k}source_systems: [pending_ods]",
            f"{k}update_freq: pending",
            f'{k}version: "0.1.0"',
            f"{k}is_mock: true",
            f'{k}mapping_status: "⏳"',
            f"{k}pending_ref: {dq(m['pending_ref'])}",
            f"{k}acceptance_unit_id: {dq(m['acceptance_unit_id'])}",
            f"{k}owner_agent: data-agent",
            f"{k}owner_human: human:淮政玮",
            f"{k}register_task: {TASK}",
            f"{k}open_task: {dq(m.get('open_task') or TASK)}",
            "",
        ]
    )


def emit_matrix_item(m: dict) -> str:
    k = "    "
    stages = "{ ods_synced: todo, dwd_loaded: todo, es_indexed: n/a, graph_loaded: n/a, verified: todo }"
    return "\n".join(
        [
            f"  - metric_id: {m['metric_id']}",
            f"{k}metric_name_zh: {dq(m['metric_name_zh'])}",
            f"{k}acceptance_unit_id: {dq(m['acceptance_unit_id'])}",
            f"{k}module: {m['module']}",
            f"{k}d1_def_status: draft",
            f"{k}d1_pending_ref: {dq(m['pending_ref'])}",
            f'{k}d1_note: "T0-X 分析清单身份注册；formula / algorithm_type 未签；禁止把 A1 表2 type 当已签"',
            f"{k}d2_schema_status: pending",
            f"{k}d2_assessed: provisional",
            f"{k}d3_source_mapping_status: pending_ods",
            f'{k}d3_gap: "身份已入 seed；三方 ODS 字段尚未核验。未核 ≠ 已确认缺口，禁止写成 none/full。"',
            f"{k}d4_ingestion_status: mock",
            f"{k}d4_ingestion_stages: {stages}",
            f"{k}lifecycle_stage: open",
            f'{k}legacy_mapping_status: "⏳"',
            "",
        ]
    )


def insert_before_or_append(path: Path, marker: str | None, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    if marker:
        idx = text.find(marker)
        if idx >= 0:
            path.write_text(text[:idx] + block + text[idx:], encoding="utf-8")
            return
    path.write_text(text.rstrip() + "\n" + block, encoding="utf-8")


def bump_total(path: Path, added: int) -> None:
    text = path.read_text(encoding="utf-8")
    for key in ("total_metrics", "total_metrics"):
        m = re.search(rf"^{key}:\s*(\d+)\s*$", text, re.M)
        if m:
            old = int(m.group(1))
            text = text[: m.start()] + f"{key}: {old + added}" + text[m.end() :]
            break
    text, _n = re.subn(r'^updated:\s*".*"', f'updated: "{TODAY}"', text, count=1, flags=re.M)
    path.write_text(text, encoding="utf-8")


def hash_metrics(path: Path, keep_ids: set[str]) -> dict[str, str]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    out = {}
    for m in data.get("metrics") or []:
        mid = m.get("metric_id")
        if mid in keep_ids:
            out[mid] = hashlib.sha256(repr(m).encode("utf-8")).hexdigest()
    return out


def first_token_id(raw) -> str | None:
    if raw is None:
        return None
    s = str(raw).strip()
    if s in ("", "None", "null"):
        return None
    for part in re.split(r"[,;|/]+", s):
        p = part.strip()
        if p.startswith("M_") or p.startswith("TEMP_ALGO_"):
            return p
    return None


def mid_of(it: dict) -> str | None:
    return first_token_id(it.get("metric_id"))


def unique_id(candidate: str, used: set[str]) -> str:
    if candidate not in used:
        used.add(candidate)
        return candidate
    i = 2
    while f"{candidate}_{i}" in used:
        i += 1
    mid = f"{candidate}_{i}"
    used.add(mid)
    return mid


def name_from(it: dict, a1_map: dict, fallback: str) -> tuple[str, str]:
    name = (it.get("主项") or "").strip()
    meaning = (it.get("指标含义") or it.get("缺口说明") or "").strip()
    leaf = first_token_id(it.get("A1指标叶ID"))
    if leaf and str(leaf) in a1_map:
        a = a1_map[str(leaf)]
        if not name:
            name = (a.get("metric_name_zh") or "").strip()
        if not meaning:
            meaning = (a.get("definition") or "").strip()
    if not name:
        name = fallback
    return name, meaning


def add_reg(register, seed_ids, skip_reuse, mid, name, meaning, acc, batch, pending=GAP, extra=None):
    if mid in seed_ids:
        skip_reuse.append({"metric_id": mid, "batch": batch, "reason": "already_in_seed"})
        return "reuse"
    if mid in register:
        return "queued"
    register[mid] = {
        "metric_id": mid,
        "metric_name_zh": name,
        "definition": ensure_len(meaning or name),
        "formula": "pending_cosign: human:唐绍祖（未签）",
        "pending_ref": pending,
        "acceptance_unit_id": acc,
        "module": domain_of(mid),
        "batch": batch,
        "open_task": TASK,
        **(extra or {}),
    }
    return "new"


def build_plan(catalog, topic, display, t0x, a1_map):
    seed_ids = {r["metric_id"] for r in catalog if r["seed"]}
    matrix_ids = {r["metric_id"] for r in catalog if r["matrix"]}
    used = set(seed_ids) | set(matrix_ids)
    temp_to_formal = {}
    register = {}
    skip_reuse = []
    rows_fl = []
    map_c = []

    for temp_id, rec in a1_map.items():
        if not str(temp_id).startswith("TEMP_ALGO_"):
            continue
        formal = unique_id(formal_from_temp(temp_id), used)
        temp_to_formal[temp_id] = formal
        add_reg(
            register,
            seed_ids,
            skip_reuse,
            formal,
            rec.get("metric_name_zh") or temp_id,
            rec.get("definition") or "",
            (rec.get("requirement_refs") or [temp_id])[0],
            "D_TEMP",
            extra={"temp_id": temp_id},
        )

    for it in t0x.get("f_minus_l") or []:
        rid = it.get("row_id") or ""
        mid = mid_of(it)
        if mid:
            action = "reuse" if mid in seed_ids else "register_existing"
            rows_fl.append({"row_id": rid, "metric_id": mid, "action": action})
            if mid not in seed_ids:
                name, meaning = name_from(it, a1_map, mid)
                add_reg(register, seed_ids, skip_reuse, mid, name, meaning, rid, "A_FL_existing")
            else:
                skip_reuse.append({"metric_id": mid, "batch": "A_FL", "reason": "F-L already in seed"})
            continue
        if rid in FL_SPECIAL:
            new_id = unique_id(FL_SPECIAL[rid], used)
        else:
            dom = page_domain(it.get("page_id"), it.get("模块"))
            new_id = unique_id(f"M_{dom}_{sanitize(rid)}", used)
        name, meaning = name_from(it, a1_map, rid)
        add_reg(register, seed_ids, skip_reuse, new_id, name, meaning, rid, "A_FL_new")
        rows_fl.append({"row_id": rid, "metric_id": new_id, "action": "new", "name": name})

    for src, batch in ((topic, "B_TOPIC_MAPPED"), (display, "B_DS_MAPPED")):
        for it in src.get("items") or []:
            if it.get("差集判定") != "mapped":
                continue
            mid = mid_of(it)
            if not mid or not mid.startswith("M_"):
                continue
            if mid in seed_ids:
                continue
            name, meaning = name_from(it, a1_map, mid)
            pending = "Q038" if mid == "M_ENT_KEY_TOTAL" else GAP
            add_reg(register, seed_ids, skip_reuse, mid, name, meaning, it.get("row_id") or mid, batch, pending=pending)

    if "M_ENT_KEY_TOTAL" in a1_map and "M_ENT_KEY_TOTAL" not in seed_ids:
        rec = a1_map["M_ENT_KEY_TOTAL"]
        add_reg(
            register,
            seed_ids,
            skip_reuse,
            "M_ENT_KEY_TOTAL",
            rec.get("metric_name_zh") or "重点企业总数",
            rec.get("definition") or "",
            "Q038",
            "B_A1_KEY_TOTAL",
            pending="Q038",
        )

    for src, batch in ((topic, "C_TOPIC_NOID"), (display, "C_DS_NOID")):
        for it in src.get("items") or []:
            if it.get("差集判定") != "mapped":
                continue
            if mid_of(it):
                continue
            rid = it.get("row_id") or ""
            leaf_s = first_token_id(it.get("A1指标叶ID")) or ""
            if leaf_s.startswith("TEMP_ALGO_"):
                mid = temp_to_formal.get(leaf_s) or unique_id(formal_from_temp(leaf_s), used)
                temp_to_formal[leaf_s] = mid
            elif leaf_s.startswith("M_"):
                mid = leaf_s
            else:
                dom = page_domain(it.get("page_id"), it.get("模块"))
                mid = unique_id(f"M_{dom}_{sanitize(rid)}", used)
            name, meaning = name_from(it, a1_map, rid)
            pending = "Q038" if mid == "M_ENT_KEY_TOTAL" else GAP
            add_reg(register, seed_ids, skip_reuse, mid, name, meaning, rid, batch, pending=pending)
            map_c.append({"row_id": rid, "metric_id": mid, "a1_leaf": leaf_s, "batch": batch})

    for mid, rec in register.items():
        rec["in_matrix"] = mid in matrix_ids
    return register, skip_reuse, rows_fl, map_c, temp_to_formal, seed_ids, matrix_ids


def write_docs(register, skip_reuse, rows_fl, map_c, temp_to_formal):
    by_batch = defaultdict(list)
    for m in register.values():
        by_batch[m["batch"]].append(m)
    lines = [
        f"# {TASK} 赋号+注册清单",
        "",
        f"日期：{TODAY}。algorithm_type=UNKNOWN，D1=draft。禁止把 A1 表2 type / 赋号建议当已签。",
        "",
        f"- 新注册（去重后）：**{len(register)}**",
        f"- reuse 跳过（已在 seed）：**{len(skip_reuse)}**",
        "",
    ]
    for batch in sorted(by_batch):
        items = sorted(by_batch[batch], key=lambda x: x["metric_id"])
        lines += [
            f"## {batch}（{len(items)}）",
            "",
            "| metric_id | 中文名 | pending_ref | 备注 |",
            "|-----------|--------|-------------|------|",
        ]
        for m in items:
            note = m.get("temp_id") or m.get("acceptance_unit_id")
            lines.append(f"| `{m['metric_id']}` | {m['metric_name_zh']} | {m['pending_ref']} | {note} |")
        lines.append("")
    lines += ["## TEMP_ALGO → 正式号", "", "| TEMP | M_* |", "|------|-----|"]
    for t, f in sorted(temp_to_formal.items()):
        lines.append(f"| `{t}` | `{f}` |")
    lines += ["", "## reuse / 跳过", ""]
    for s in skip_reuse:
        lines.append(f"- `{s['metric_id']}` · {s['batch']} · {s['reason']}")
    (WORK / "ALGO-LIB-T0X-REGISTER-L01-new-ids.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    gl = [
        f"# T0-X 会前闸门 · F−L 77 行 found.seed=true",
        "",
        f"任务：`{TASK}` · {TODAY}",
        "",
        "| row_id | metric_id | 动作 |",
        "|--------|-----------|------|",
    ]
    for r in rows_fl:
        gl.append(f"| `{r['row_id']}` | `{r['metric_id']}` | {r['action']} |")
    gl += ["", "机器复核：`node ALGO-LIB-T0X-REGISTER-L01-verify.mjs`。", ""]
    (WORK / "ALGO-LIB-T0X-REGISTER-L01-t0x-gate.md").write_text("\n".join(gl) + "\n", encoding="utf-8")
    (WORK / "ALGO-LIB-T0X-REGISTER-L01-plan.json").write_text(
        json.dumps(
            {
                "register_count": len(register),
                "register_ids": sorted(register),
                "fl_rows": rows_fl,
                "c_rows": map_c,
                "temp_map": temp_to_formal,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def apply_yaml(register, matrix_ids):
    by_dom = defaultdict(list)
    for mid, it in sorted(register.items()):
        by_dom[domain_of(mid)].append(it)
    written = []
    for dom, items in sorted(by_dom.items()):
        seed_path = REG / f"cfg_metric-{dom}-seed.yaml"
        mat_path = REG / f"metric-readiness-matrix-{dom}.yaml"
        seed_block = f"\n  # --- {TASK} T0-X 分析清单身份（D1=draft, type=UNKNOWN） ---\n"
        seed_block += "".join(emit_seed_item(it) for it in items)
        seed_block += "\n"
        if not seed_path.exists():
            raise SystemExit(f"missing seed: {seed_path}")
        insert_before_or_append(seed_path, SEED_MARKER.get(dom), seed_block)
        bump_total(seed_path, len(items))
        written.append(str(seed_path))

        mat_items = [it for it in items if it["metric_id"] not in matrix_ids]
        if not mat_items:
            continue
        mblock = f"\n  # --- {TASK} T0-X 分析清单身份 ---\n"
        mblock += "".join(emit_matrix_item(it) for it in mat_items)
        mblock += "\n"
        if not mat_path.exists():
            if dom != "POLICY":
                raise SystemExit(f"missing matrix: {mat_path}")
            mat_path.write_text(
                POLICY_MATRIX_HEADER + "".join(emit_matrix_item(it) for it in mat_items),
                encoding="utf-8",
            )
        else:
            insert_before_or_append(mat_path, MAT_MARKER.get(dom), mblock)
            bump_total(mat_path, len(mat_items))
        written.append(str(mat_path))
    return written


def main() -> int:
    dry = "--dry-run" in sys.argv
    catalog = dump_catalog()
    topic = load_yaml(REQ / "专题系统" / "TOPIC-ALGO-GAP-L02.yaml")
    display = load_yaml(REQ / "展示系统" / "DS-ALGO-GAP-L02.yaml")
    t0x = load_yaml(REQ / "T0X" / "ALGO-LIB-T0X-L01-pre-meeting.yaml")
    a1 = load_yaml(ALGO / "ALGO-LIB-METRIC-DEPS-L01-metrics.yaml")
    a1_map = {}
    for m in a1.get("metrics") or []:
        mid = str(m.get("metric_id") or "").strip()
        if mid:
            a1_map[mid] = m

    register, skip_reuse, rows_fl, map_c, temp_map, seed_ids, matrix_ids = build_plan(
        catalog, topic, display, t0x, a1_map
    )
    write_docs(register, skip_reuse, rows_fl, map_c, temp_map)
    summary = {
        "register": len(register),
        "by_domain": {
            d: sum(1 for m in register if domain_of(m) == d) for d in sorted({domain_of(m) for m in register})
        },
        "fl_rows": len(rows_fl),
        "fl_new": sum(1 for r in rows_fl if r["action"] == "new"),
        "temp": len(temp_map),
        "c_rows": len(map_c),
        "skip_reuse": len(skip_reuse),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if dry:
        print("dry-run: yaml not written")
        return 0

    keep = {}
    for name in (
        "cfg_metric-ENT-seed.yaml",
        "cfg_metric-CHAIN-seed.yaml",
        "cfg_metric-POLICY-seed.yaml",
        "cfg_metric-SYNTH-seed.yaml",
        "cfg_metric-SVC-seed.yaml",
    ):
        p = REG / name
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        ids = {m["metric_id"] for m in data.get("metrics") or []}
        keep[str(p)] = hash_metrics(p, ids)

    written = apply_yaml(register, matrix_ids)
    for path, before in keep.items():
        after = hash_metrics(Path(path), set(before))
        for mid, digest in before.items():
            if after.get(mid) != digest:
                raise SystemExit(f"existing metric mutated: {path} {mid}")
    print("written", len(written))
    for w in written:
        print(" ", w)
    return 0


if __name__ == "__main__":
    sys.exit(main())

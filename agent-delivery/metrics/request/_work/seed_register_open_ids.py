# One-shot: register OPEN new M_* into metrics/registry (METRIC-SEED-REGISTER-L01).
# D1=draft, algorithm_type=UNKNOWN. Does not rewrite existing ENT/CHAIN/… metric bodies.
from __future__ import annotations

from collections import defaultdict
from datetime import date
from pathlib import Path
import hashlib
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[4]  # gkx-orchestration
ASSIGN = ROOT / "agent-delivery" / "metrics" / "request" / "_work" / "id-assign"
REG = ROOT / "agent-delivery" / "metrics" / "registry"
TODAY = "2026-08-22"
TASK = "METRIC-SEED-REGISTER-L01"
GAP_UNSIGNED = "GAP-ALGO-TYPE-UNSIGNED"

STAGES = {
    "ods_synced": "todo",
    "dwd_loaded": "todo",
    "es_indexed": "n/a",
    "graph_loaded": "n/a",
    "verified": "todo",
}


def domain_of(metric_id: str) -> str:
    m = re.match(r"^M_([A-Z]+)_", metric_id)
    if not m:
        raise ValueError(f"not M_* : {metric_id}")
    return m.group(1)


def load_seed_ids() -> dict[str, str]:
    out = {}
    for p in sorted(REG.glob("cfg_metric-*-seed.yaml")):
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        for m in data.get("metrics") or []:
            out[m["metric_id"]] = p.name
    return out


def collect_register_items(seed_ids: dict[str, str]):
    new_by_id: dict[str, dict] = {}
    reuse_in_seed = []
    skip_zhiku = []
    skip_red = []
    reuse_miss = []

    for p in sorted(ASSIGN.glob("*-METRIC-OPEN-L01.yaml")):
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        for it in data.get("items") or []:
            it = dict(it)
            it["_task"] = data["task_id"]
            mid = it["metric_id"]
            if it.get("demo_lock") or it.get("promote") == "forbidden":
                skip_red.append(it)
                continue
            if str(mid).startswith("ZHIKU-"):
                skip_zhiku.append(it)
                continue
            if it.get("reuse_of"):
                if it["reuse_of"] in seed_ids or mid in seed_ids:
                    reuse_in_seed.append(it)
                else:
                    reuse_miss.append(it)
                    if mid not in new_by_id:
                        new_by_id[mid] = it
                continue
            if mid in seed_ids:
                reuse_in_seed.append(it)
                continue
            if mid not in new_by_id or new_by_id[mid].get("reuse_of"):
                new_by_id[mid] = it
    return new_by_id, reuse_in_seed, skip_zhiku, skip_red, reuse_miss


def pending_ref(it: dict) -> str:
    ref = it.get("pending_ref")
    if ref in (None, "", "null"):
        return GAP_UNSIGNED
    return str(ref)


def definition(it: dict) -> str:
    d = (it.get("definition_draft") or "").strip()
    d = re.sub(r"[ \t]+\n", "\n", d)
    d = re.sub(r"\n{3,}", "\n\n", d)
    if len(d) < 50:
        d = d + " 统计窗口与对象范围见 OPEN 赋号卡内部默认；公式与 algorithm_type 未签。"
    return d


def seed_entry(it: dict) -> dict:
    pages = it.get("page_ids") or []
    acc = pages[0] if pages else it["_task"]
    return {
        "metric_id": it["metric_id"],
        "metric_name_zh": it["metric_name_zh"],
        "definition": definition(it),
        "formula": "pending_cosign: human:唐绍祖（未签）",
        "algorithm_type": "UNKNOWN",
        "source_tables": ["pending_ods"],
        "source_systems": ["pending_ods"],
        "update_freq": "pending",
        "version": "0.1.0",
        "is_mock": True,
        "mapping_status": "⏳",
        "pending_ref": pending_ref(it),
        "acceptance_unit_id": acc,
        "owner_agent": "data-agent",
        "owner_human": "human:淮政玮",
        "register_task": TASK,
        "open_task": it["_task"],
    }


def matrix_entry(it: dict) -> dict:
    pages = it.get("page_ids") or []
    acc = pages[0] if pages else it["_task"]
    return {
        "metric_id": it["metric_id"],
        "metric_name_zh": it["metric_name_zh"],
        "acceptance_unit_id": acc,
        "module": it["_task"].replace("-METRIC-OPEN-L01", ""),
        "d1_def_status": "draft",
        "d1_pending_ref": pending_ref(it),
        "d1_note": "OPEN 身份注册；formula / algorithm_type 未签；禁止把赋号建议类型当已签",
        "d2_schema_status": "pending",
        "d2_assessed": "provisional",
        "d3_source_mapping_status": "pending_ods",
        "d3_gap": "身份已入 seed；三方 ODS 字段尚未核验。未核 ≠ 已确认缺口，禁止写成 none/full。",
        "d4_ingestion_status": "mock",
        "d4_ingestion_stages": dict(STAGES),
        "lifecycle_stage": "open",
        "legacy_mapping_status": "⏳",
    }


def dump_yaml(obj) -> str:
    return yaml.safe_dump(
        obj,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=88,
    )


def dq(s: str) -> str:
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def emit_seed_item(m: dict, item_indent: int = 2) -> str:
    """Subset YAML that scripts/lib/metric-registry-lib.mjs can parse (dash indented, flow lists, > blocks)."""
    sp = " " * item_indent
    k = " " * (item_indent + 2)
    b = " " * (item_indent + 4)  # definition > content; mapIndent+2
    lines = [
        f"{sp}- metric_id: {m['metric_id']}",
        f"{k}metric_name_zh: {dq(m['metric_name_zh'])}",
        f"{k}definition: >",
        f"{b}{definition_oneline(m['definition'])}",
        f"{k}formula: {dq(m['formula'])}",
        f"{k}algorithm_type: UNKNOWN",
        f"{k}source_tables: [pending_ods]",
        f"{k}source_systems: [pending_ods]",
        f"{k}update_freq: pending",
        f"{k}version: {dq(m['version'])}",
        f"{k}is_mock: true",
        f"{k}mapping_status: {dq(m['mapping_status'])}",
        f"{k}pending_ref: {dq(m['pending_ref'])}",
        f"{k}acceptance_unit_id: {dq(m['acceptance_unit_id'])}",
        f"{k}owner_agent: data-agent",
        f"{k}owner_human: human:淮政玮",
        f"{k}register_task: {TASK}",
        f"{k}open_task: {m['open_task']}",
        "",
    ]
    return "\n".join(lines)


def definition_oneline(d: str) -> str:
    return re.sub(r"\s+", " ", d.strip())


def emit_matrix_item(m: dict, item_indent: int = 2) -> str:
    sp = " " * item_indent
    k = " " * (item_indent + 2)
    stages = "{ ods_synced: todo, dwd_loaded: todo, es_indexed: n/a, graph_loaded: n/a, verified: todo }"
    lines = [
        f"{sp}- metric_id: {m['metric_id']}",
        f"{k}metric_name_zh: {dq(m['metric_name_zh'])}",
        f"{k}acceptance_unit_id: {dq(m['acceptance_unit_id'])}",
        f"{k}module: {m['module']}",
        f"{k}d1_def_status: draft",
        f"{k}d1_pending_ref: {dq(m['d1_pending_ref'])}",
        f"{k}d1_note: {dq(m['d1_note'])}",
        f"{k}d2_schema_status: pending",
        f"{k}d2_assessed: provisional",
        f"{k}d3_source_mapping_status: pending_ods",
        f"{k}d3_gap: {dq(m['d3_gap'])}",
        f"{k}d4_ingestion_status: mock",
        f"{k}d4_ingestion_stages: {stages}",
        f"{k}lifecycle_stage: open",
        f"{k}legacy_mapping_status: {dq(m['legacy_mapping_status'])}",
        "",
    ]
    return "\n".join(lines)


def emit_seed_file(dom: str, items: list[dict]) -> str:
    n = len(items)
    head = SEED_HEADER.format(zh=ZH[dom], dom=dom, today=TODAY)
    body = "\n".join(
        [
            "version: 1",
            f'updated: "{TODAY}"',
            f"domain: {dom}",
            'seed_version: "0.1.0"',
            "batch: open_draft_20260822",
            f"total_metrics: {n}",
            "",
            "defaults:",
            "  source_systems: [pending_ods]",
            "  is_mock: true",
            "  owner_agent: data-agent",
            '  version: "0.1.0"',
            "  algorithm_type: UNKNOWN",
            "",
            "metrics:",
        ]
    )
    return head + body + "\n" + "".join(emit_seed_item(seed_entry(it)) for it in items)


def emit_matrix_file(dom: str, items: list[dict]) -> str:
    head = MATRIX_HEADER.format(zh=ZH[dom], dom=dom, today=TODAY)
    body = "\n".join(
        [
            "version: 1",
            f"module: {dom}",
            "model_ref: data-lineage-policy.md#2.3",
            "model_status: provisional",
            f'updated: "{TODAY}"',
            f'as_of: "{TODAY}"',
            "d2_verifier: lineage-subcoord",
            "d4_batch: open_draft_20260822",
            f"register_task: {TASK}",
            "coverage_notes:",
            '  - "OPEN 新号身份注册；D1=draft，公式/类型未签。"',
            '  - "不改 A2 库 missing 为 mapped。"',
            '  - "D2/D3/D4 本批不改绿。"',
            "",
            "metrics:",
        ]
    )
    return head + body + "\n" + "".join(emit_matrix_item(matrix_entry(it)) for it in items)


SEED_HEADER = """\
# cfg_metric 种子 —— {zh}（{dom}）M_{dom}_* 指标 8 件套
# ============================================================================
# 作用：METRIC-SEED-REGISTER-L01 把 OPEN 新号身份写入 seed（D1=draft）。
# 维护：data-agent  ·  监管：human:淮政玮  ·  创建：{today}
# 8 件套（v1.5 共 9 项）：metric_id / metric_name_zh / definition / formula /
#         algorithm_type / source_tables / source_systems / update_freq / version
# algorithm_type 本批一律 UNKNOWN（未签）。禁止把赋号卡 suggested_unsigned 当已签。
# 禁止 D1=aligned。存量口径/公式/源表不在本文件改（本文件为该域首份 seed）。
# ============================================================================

"""

MATRIX_HEADER = """\
# metric-readiness-matrix —— {zh}（{dom}）四维就绪度
# ============================================================================
# 生成任务：METRIC-SEED-REGISTER-L01 · {today} · 监管 human:淮政玮
# 模型：data-lineage-policy.md §2.3
# D1=draft；D2=pending；D3=pending_ods；D4=mock。禁止改绿。
# lifecycle_stage=open（已过 METRIC-OPEN 身份点名，公式未签）。
# ============================================================================

"""

ZH = {
    "ENT": "企业域",
    "INNOV": "科技发展态势 / 创新监测域",
    "TECH": "技术链域",
    "ORG": "科研机构域",
    "TALENT": "人才域",
    "SVC": "产业服务域",
    "COMMON": "跨要素 / 查询聚合域",
}


def write_new_seed(dom: str, items: list[dict]) -> Path:
    path = REG / f"cfg_metric-{dom}-seed.yaml"
    path.write_text(emit_seed_file(dom, items), encoding="utf-8")
    return path


def write_new_matrix(dom: str, items: list[dict]) -> Path:
    path = REG / f"metric-readiness-matrix-{dom}.yaml"
    path.write_text(emit_matrix_file(dom, items), encoding="utf-8")
    return path


def append_yaml_list(path: Path, marker: str, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    idx = text.find(marker)
    if idx < 0:
        raise SystemExit(f"marker not found in {path.name}: {marker!r}")
    path.write_text(text[:idx] + block + text[idx:], encoding="utf-8")


def bump_total_metrics(path: Path, added: int) -> None:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^total_metrics:\s*(\d+)\s*$", text, re.M)
    if not m:
        raise SystemExit(f"total_metrics not found in {path.name}")
    old = int(m.group(1))
    text = text[: m.start()] + f"total_metrics: {old + added}" + text[m.end() :]
    text = re.sub(r'^updated:\s*".*"', f'updated: "{TODAY}"', text, count=1, flags=re.M)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    seed_ids = load_seed_ids()
    new_by_id, reuse_in_seed, skip_zhiku, skip_red, reuse_miss = collect_register_items(seed_ids)

    # snapshot ENT bodies we must not touch
    ent_path = REG / "cfg_metric-ENT-seed.yaml"
    ent_before = ent_path.read_text(encoding="utf-8")
    ent_data = yaml.safe_load(ent_before)
    keep_ids = {m["metric_id"]: hashlib.sha256(repr(m).encode("utf-8")).hexdigest() for m in ent_data["metrics"]}

    by_dom: dict[str, list] = defaultdict(list)
    for mid, it in sorted(new_by_id.items()):
        by_dom[domain_of(mid)].append(it)

    written = []
    # new domain seeds + matrices
    for dom in ("INNOV", "TECH", "ORG", "TALENT", "COMMON"):
        if not by_dom.get(dom):
            continue
        written.append(str(write_new_seed(dom, by_dom[dom])))
        written.append(str(write_new_matrix(dom, by_dom[dom])))

    # ENT: append 7, do not rewrite existing metrics
    if by_dom.get("ENT"):
        block = "\n  # --- METRIC-SEED-REGISTER-L01 OPEN 新号（D1=draft, type=UNKNOWN） ---\n"
        block += "".join(emit_seed_item(seed_entry(it)) for it in by_dom["ENT"])
        block += "\n"
        append_yaml_list(ent_path, "# 状态分布汇总", block)
        bump_total_metrics(ent_path, len(by_dom["ENT"]))
        written.append(str(ent_path))

        ent_mat = REG / "metric-readiness-matrix-ENT.yaml"
        mblock = "\n  # --- METRIC-SEED-REGISTER-L01 OPEN 新号 ---\n"
        mblock += "".join(emit_matrix_item(matrix_entry(it)) for it in by_dom["ENT"])
        mblock += "\n"
        append_yaml_list(ent_mat, "# ============================================================================\n# 汇总", mblock)
        written.append(str(ent_mat))

    # SVC: OPEN 身份 seed（允许覆盖本 generator 上一轮写出的文件）
    if by_dom.get("SVC"):
        written.append(str(write_new_seed("SVC", by_dom["SVC"])))
        svc_mat = REG / "metric-readiness-matrix-SVC.yaml"
        sblock = "\n  # --- METRIC-SEED-REGISTER-L01 OPEN 新号 / 未入 seed 的 reuse ---\n"
        sblock += "".join(emit_matrix_item(matrix_entry(it)) for it in by_dom["SVC"])
        svc_text = svc_mat.read_text(encoding="utf-8")
        svc_mat.write_text(svc_text.rstrip() + "\n" + sblock, encoding="utf-8")
        written.append(str(svc_mat))

    # --- checks ---
    ent_after = yaml.safe_load(ent_path.read_text(encoding="utf-8"))
    after_map = {m["metric_id"]: m for m in ent_after["metrics"]}
    for mid, digest in keep_ids.items():
        now = hashlib.sha256(repr(after_map[mid]).encode("utf-8")).hexdigest()
        if now != digest:
            raise SystemExit(f"ENT existing metric mutated: {mid}")

    all_seed = load_seed_ids()
    for mid in new_by_id:
        if mid not in all_seed:
            raise SystemExit(f"missing from seed after write: {mid}")
        # load algorithm_type
    bad_type = []
    suggested_leak = []
    for p in REG.glob("cfg_metric-*-seed.yaml"):
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        for m in data.get("metrics") or []:
            if m["metric_id"] not in new_by_id:
                continue
            if m.get("algorithm_type") != "UNKNOWN":
                bad_type.append(m["metric_id"])
            if "suggested" in str(m.get("algorithm_type", "")).lower():
                suggested_leak.append(m["metric_id"])
    if bad_type or suggested_leak:
        raise SystemExit(f"type errors {bad_type} leak {suggested_leak}")

    for it in skip_zhiku + skip_red:
        if it["metric_id"] in all_seed:
            raise SystemExit(f"ZHIKU/red leaked into seed: {it['metric_id']}")

    # matrix D1 draft + no green
    for p in REG.glob("metric-readiness-matrix-*.yaml"):
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        for m in data.get("metrics") or []:
            if m["metric_id"] not in new_by_id:
                continue
            if m.get("d1_def_status") != "draft":
                raise SystemExit(f"D1 not draft: {m['metric_id']}")
            if m.get("d1_def_status") == "aligned":
                raise SystemExit("aligned leak")
            if m.get("d2_schema_status") in ("ready",):
                raise SystemExit(f"D2 greened {m['metric_id']}")
            if m.get("d3_source_mapping_status") in ("full",):
                raise SystemExit(f"D3 greened {m['metric_id']}")
            if m.get("d4_ingestion_status") in ("live",):
                raise SystemExit(f"D4 greened {m['metric_id']}")
            if m.get("lifecycle_stage") not in ("open", "identified"):
                raise SystemExit(f"bad lifecycle {m['metric_id']}")

    summary = {
        "new_registered": len(new_by_id),
        "by_domain": {k: len(v) for k, v in sorted(by_dom.items())},
        "reuse_skip_already_in_seed": sorted({i["metric_id"] for i in reuse_in_seed}),
        "reuse_miss_now_registered": [i["metric_id"] for i in reuse_miss],
        "zhiku_skip": len(skip_zhiku),
        "red_skip": [i["metric_id"] for i in skip_red],
        "files": written,
    }
    outp = ASSIGN.parent / "METRIC-SEED-REGISTER-L01-summary.yaml"
    outp.write_text(dump_yaml(summary), encoding="utf-8")
    print(dump_yaml(summary))
    print("OK", len(new_by_id), "registered")
    return 0


if __name__ == "__main__":
    sys.exit(main())

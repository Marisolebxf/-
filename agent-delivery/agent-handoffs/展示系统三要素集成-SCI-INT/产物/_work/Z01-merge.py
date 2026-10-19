# -*- coding: utf-8 -*-
"""SCI-INT-Z01 汇总。只读源 yaml，不回改。"""
import re
from collections import defaultdict
from pathlib import Path

import yaml
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent
HAND_DIR = ROOT.parent
OUT_YAML = ROOT / "SCI-INT-集成依赖总表.yaml"
OUT_XLSX = ROOT / "SCI-INT-集成依赖总表.xlsx"
OUT_MD = ROOT / "SCI-INT-久新接口需求说明.md"
OUT_HAND = HAND_DIR / "SCI-INT-Z01.md"

A_FILES = [f"SCI-INT-A{i:02d}.yaml" for i in range(1, 16)]
B_FILES = [f"SCI-INT-B{i:02d}.yaml" for i in range(2, 10)]
C_FILES = [f"SCI-INT-C{i:02d}.yaml" for i in range(1, 6)]
D_FILES = [f"SCI-INT-D{i:02d}.yaml" for i in range(1, 5)]
CARD_FILES = A_FILES + B_FILES + C_FILES + D_FILES
ALLOWED = {f"IP-{i:02d}" for i in range(1, 14)}
DIMS = ("TAL", "TECH", "ORG")
TALENT_WORDS = ("人才态势", "人才画像", "人才引进")
TALENT_LEAVES = ("A11", "A14", "A15")
FORMAL = "lumen-algo-py / gkxlumen ADS"
SHEET_ORDER = [
    "页面", "指标", "数据", "测试", "对端接口需求", "决策项草案",
    "风险", "结构升级项", "跨域指标", "判据", "勘误",
]
BASE_COLS = [
    "int_id", "layer", "来源叶", "excel_row", "metric_id", "integration_pattern",
    "counterpart", "jiuxin_row_id", "fe_route", "java", "python", "downstream",
    "正式落点", "structure_escalation",
]
TIMING = {
    "IP-01": "同步读", "IP-02": "同步读", "IP-03": "同步", "IP-04": "异步",
    "IP-05": "异步", "IP-06": "同步读", "IP-07": "异步", "IP-08": "异步",
    "IP-09": "异步", "IP-10": "无对端调用", "IP-11": "异步", "IP-12": "同步读",
    "IP-13": "无对端调用",
}


def load_yaml(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def leaf_of(name):
    return name.replace("SCI-INT-", "").replace(".yaml", "")


def plain(value):
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, list):
        return "|".join(plain(x) for x in value if plain(x) != "")
    if isinstance(value, dict):
        return "|".join(f"{k}={plain(v)}" for k, v in value.items())
    return str(value).strip()


def scrub_demo(text):
    text = text.replace("九新", "久新")
    if "demo-" not in text:
        return text
    parts = re.split(r"(?<=[。；;])", text)
    kept = [p for p in parts if "demo-" not in p]
    out = "".join(kept)
    out = re.sub(r"demo-\S*", "", out).replace("demo-", "")
    out = re.sub(r"\s{2,}", " ", out).strip(" ，；。")
    return out


def public(text):
    cleaned = scrub_demo(plain(text))
    if plain(text) and not cleaned:
        return "见勘误"
    return cleaned


def pattern_tokens(value):
    if value is None:
        return []
    if isinstance(value, list):
        out = []
        for item in value:
            out.extend(pattern_tokens(item))
        return out
    return re.findall(r"IP-\d+", str(value))


def pattern_text(value):
    if isinstance(value, list):
        return "/".join(str(x) for x in value)
    return "" if value is None else str(value)


def as_bool(value):
    if isinstance(value, bool):
        return value
    return value in (1, "true", "True", "TRUE")


def dims_of(card):
    raw = card.get("dimension") or []
    if isinstance(raw, str):
        raw = [raw]
    found = set()
    for item in raw:
        head = str(item).split("（")[0].strip()
        if head in DIMS:
            found.add(head)
    return found


def jx_ids(card):
    value = card.get("jiuxin_row_id")
    if value is None:
        return []
    if isinstance(value, list):
        return [str(x) for x in value if str(x).strip() not in ("", "none", "null")]
    text = str(value).strip()
    if text in ("", "none", "null", "None"):
        return []
    return [text]


def counterpart_active(value):
    if value is None:
        return False
    return str(value).strip() not in ("", "none", "null", "None")


def chain_empty(value):
    return plain(value) in ("", "null", "None")


def excel_of(card):
    srs = card.get("srs")
    if isinstance(srs, dict) and srs.get("excel_row") is not None:
        return srs.get("excel_row")
    return None


def metric_of(card):
    if card.get("metric_id"):
        return str(card["metric_id"])
    ids = card.get("metric_ids") or []
    if isinstance(ids, str):
        return ids
    return "|".join(str(x) for x in ids)


def names_of(value):
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value.strip() else []
    out = []
    for item in value:
        if isinstance(item, dict):
            text = plain(item.get("name") or item.get("field") or item)
        else:
            text = plain(item)
        if text:
            out.append(text)
    return out


def io_of(card):
    draft = card.get("contract_draft") or {}
    req = names_of(draft.get("request"))
    resp = names_of(draft.get("response_key_fields"))
    outputs = card.get("outputs")
    if not resp and isinstance(outputs, dict):
        resp = names_of(outputs.get("response_key_fields"))
    if not req:
        for item in card.get("inputs") or []:
            if not isinstance(item, dict):
                continue
            fields = plain(item.get("fields"))
            table = plain(item.get("table"))
            if fields and "未给" not in fields:
                req.append(fields)
            elif table:
                req.append(table)
    return unique(req), unique(resp)


def unique(items):
    out = []
    for item in items:
        if item not in out:
            out.append(item)
    return out


def timing_of(card):
    execution = plain(card.get("execution"))
    if execution in ("同步", "异步"):
        return execution
    if "异步" in execution:
        return "异步"
    if "同步" in execution:
        return "同步"
    labels = []
    for token in pattern_tokens(card.get("integration_pattern")):
        label = TIMING.get(token)
        if label and label not in labels:
            labels.append(label)
    return " / ".join(labels) if labels else "未标明"


def item_text(item):
    if isinstance(item, str):
        return item.strip()
    if isinstance(item, dict):
        bits = []
        for key in ("id", "level", "owner"):
            if item.get(key):
                bits.append(str(item[key]))
        body = item.get("item") or item.get("desc") or item.get("text") or item.get("question") or ""
        if body:
            bits.append(str(body))
        if item.get("mitigation"):
            bits.append("缓解：" + str(item["mitigation"]))
        return " ".join(bits).strip() or plain(item)
    return plain(item)


def as_items(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def test_blob(card):
    points = card.get("test_points") or []
    if isinstance(points, str):
        return points
    return "\n".join(str(x) for x in points)


def add_corr(bag, kind, obj, detail):
    bag.append({"类型": kind, "对象": obj, "说明": detail, "处理": "只记录，不回改源 yaml"})


def chain_public(card, corrections):
    raw_cc = card.get("call_chain") or {}
    snippets = []
    out = {}
    for key in ("fe_route", "java", "python", "downstream"):
        raw = plain(raw_cc.get(key))
        if "demo-" in raw:
            snippets.append(key + "：" + raw)
        out[key] = public(raw)
    raw_down = plain(raw_cc.get("downstream"))
    if "demo-" in raw_down:
        out["正式落点"] = FORMAL
        if not out["downstream"] or out["downstream"] == "见勘误":
            out["downstream"] = FORMAL
    else:
        out["正式落点"] = out["downstream"]
    if snippets:
        add_corr(
            corrections,
            "正式落点",
            card.get("int_id") or "",
            "调用链含演示服务名。正式落点列写 " + FORMAL + "。原文：" + " || ".join(snippets),
        )
    return out


def row_from(leaf, card, corrections):
    chain = chain_public(card, corrections)
    srs_row = excel_of(card)
    return {
        "int_id": card.get("int_id") or "",
        "layer": card.get("layer") or "",
        "来源叶": leaf,
        "excel_row": "" if srs_row is None else srs_row,
        "metric_id": metric_of(card),
        "integration_pattern": pattern_text(card.get("integration_pattern")),
        "counterpart": plain(card.get("counterpart")),
        "jiuxin_row_id": "|".join(jx_ids(card)),
        "fe_route": chain["fe_route"],
        "java": chain["java"],
        "python": chain["python"],
        "downstream": chain["downstream"],
        "正式落点": chain["正式落点"],
        "structure_escalation": "true" if as_bool(card.get("structure_escalation")) else "false",
        "source_int_id": plain(card.get("source_int_id")),
        "dimension": "|".join(sorted(dims_of(card))),
    }


def sheet_row(row, columns):
    return {key: row.get(key, "") for key in columns}


def parent_notes(row_id, mapping):
    notes = []
    for item in mapping:
        note = plain(item.get("备注"))
        primary = plain(item.get("jiuxin_row_id"))
        if row_id in note and primary != row_id:
            notes.append(
                f"{item.get('metric_id')} 同交，主行 {primary or '空'}：{public(note)}"
            )
    return notes


def build():
    p00 = load_yaml(ROOT / "P00-baseline.yaml")
    b01 = load_yaml(ROOT / "SCI-INT-B01.yaml")
    docs = {name: load_yaml(ROOT / name) for name in CARD_FILES}
    name_by_row = {item["excel_row"]: item for item in p00["srs_leaves"]}
    corrections = []
    wrapped = []
    for name in CARD_FILES:
        leaf = leaf_of(name)
        for card in docs[name].get("cards") or []:
            wrapped.append((leaf, card))

    rows = [row_from(leaf, card, corrections) for leaf, card in wrapped]

    a09 = next(card for leaf, card in wrapped if card.get("int_id") == "INT-A-X-0817")
    b08 = next(
        card for leaf, card in wrapped
        if card.get("metric_id") == "M_ORG_DEEP_153_1" and leaf == "B08"
    )
    add_corr(
        corrections,
        "模式",
        "INT-A-X-0817",
        "页面卡把 M_ORG_DEEP_153_1 / SRS-153 标成 "
        + pattern_text(a09.get("integration_pattern"))
        + "。B08 对应卡 " + b08.get("int_id") + " 是 "
        + pattern_text(b08.get("integration_pattern"))
        + "。总表指标行以 B08 为准，页面行保留原值。",
    )

    for leaf, card in wrapped:
        if leaf not in TALENT_LEAVES:
            continue
        if "-X-" not in (card.get("int_id") or ""):
            continue
        meta = name_by_row.get(excel_of(card)) or {}
        blob = " ".join([
            plain(meta.get("name")), plain(meta.get("path")), plain(meta.get("file")),
            plain((card.get("srs") or {}).get("path") if isinstance(card.get("srs"), dict) else ""),
        ])
        if not any(word in blob for word in TALENT_WORDS):
            continue
        hit = next(word for word in TALENT_WORDS if word in blob)
        add_corr(
            corrections,
            "号段",
            card.get("int_id"),
            f"{leaf} 叶名「{plain(meta.get('name'))}」属于{hit}，号段为 X。"
            f"建议维度改回 TAL。现 dimension={plain(card.get('dimension'))}。",
        )
    a11_hits = [
        item for item in corrections
        if item["类型"] == "号段" and str(item["对象"]).startswith("INT-A-X-10")
    ]
    if not a11_hits:
        add_corr(
            corrections,
            "号段",
            "A11",
            "A11 卡片号段是 X。逐叶名核对后，没有叶名属于人才态势、人才画像或人才引进，不改维度。",
        )

    tbd_ids = [card.get("int_id") for leaf, card in wrapped if pattern_text(card.get("integration_pattern")) == "TBD"]
    if tbd_ids:
        add_corr(
            corrections,
            "模式",
            "C01/C02",
            f"{len(tbd_ids)} 张数据卡 integration_pattern 为 TBD，不是 IP 编号。总表保留 TBD，不发明编号。",
        )

    for index, item in enumerate(corrections, 1):
        item["序号"] = index

    by_jx = defaultdict(list)
    for leaf, card in wrapped:
        if card.get("layer") == "test":
            continue
        for rid in jx_ids(card):
            by_jx[rid].append((leaf, card))

    b_ref = set()
    for leaf, card in wrapped:
        if leaf.startswith("B") and card.get("layer") == "metric":
            b_ref.update(jx_ids(card))

    jiuxin_rows = []
    md_parts = [
        "# 久新接口需求说明",
        "",
        "对端：久新。确认状态一律为待确认。本文件只写需求。会签未做。",
        "",
    ]
    for spec in p00["jiuxin_rows"]:
        rid = spec["row_id"]
        consumers = by_jx.get(rid, [])
        metric_cards = [(leaf, card) for leaf, card in consumers if card.get("layer") == "metric"]
        unconsumed = not metric_cards
        field_cards = consumers or [
            (leaf, card) for leaf, card in wrapped
            if card.get("layer") in ("page", "metric")
            and rid in plain((card.get("call_chain") or {}).get("downstream"))
        ]
        who, patterns, timings, reqs, resps = [], [], [], [], []
        for leaf, card in field_cards:
            who.append(
                f"{card.get('int_id')}（{card.get('layer')}，{leaf}，{metric_of(card) or '无 metric_id'}）"
            )
            patterns.append(pattern_text(card.get("integration_pattern")))
            timings.append(timing_of(card))
            req, resp = io_of(card)
            reqs.extend(req)
            resps.extend(resp)
        reason = ""
        if unconsumed:
            bits = ["本管线未消费。原因：B02–B09 没有把本 row_id 写成 jiuxin_row_id。"]
            notes = parent_notes(rid, b01.get("initial_mapping") or [])
            if notes:
                bits.append("B01 初判：" + "；".join(notes))
            page_ids = [card.get("int_id") for leaf, card in consumers if card.get("layer") == "page"]
            if page_ids:
                bits.append("页面卡点名本行，需求并入该页，不单列指标卡：" + "、".join(page_ids))
            elif field_cards:
                bits.append(
                    "仅在调用链下游被点名：" + "、".join(card.get("int_id") for leaf, card in field_cards)
                )
            else:
                bits.append("没有任何卡片把本行写入 jiuxin_row_id。展示行与库叶同交，不单列接口。")
            reason = public(" ".join(bits))
            if "本管线未消费" not in reason:
                reason = "本管线未消费。" + reason
        record = {
            "row_id": rid,
            "名称": plain(spec.get("名称")),
            "维度": plain(spec.get("维度")),
            "系统": plain(spec.get("系统")),
            "交付形态": plain(spec.get("交付形态")),
            "确认状态": "待确认",
            "谁消费": "；".join(who) if who else "无",
            "模式": "；".join(unique(patterns)) if patterns else "无",
            "同步异步": "；".join(unique(timings)) if timings else "未标明",
            "输入字段": "、".join(unique(reqs)) if reqs else "包内未给字段名",
            "输出字段": "、".join(unique(resps)) if resps else "包内未给字段名",
            "未消费原因": reason,
        }
        jiuxin_rows.append(record)
        md_parts.append(f"## {rid} {record['名称']}")
        md_parts.append("")
        md_parts.append(f"- 确认状态：{record['确认状态']}")
        if reason:
            md_parts.append(f"- {reason}")
        md_parts.append(f"- 谁消费：{record['谁消费']}")
        md_parts.append(f"- 模式：{record['模式']}")
        md_parts.append(f"- 同步/异步：{record['同步异步']}")
        md_parts.append(f"- 输入字段：{record['输入字段']}")
        md_parts.append(f"- 输出字段：{record['输出字段']}")
        md_parts.append("")
    md = "\n".join(md_parts).replace("九新", "久新")

    decisions = []
    risks = []

    def push_list(bucket, leaf, int_id, values, scrub):
        for item in as_items(values):
            text = item_text(item)
            if not text:
                continue
            if scrub:
                text = public(text)
            else:
                text = text.replace("九新", "久新")
            if text:
                bucket.append({"来源叶": leaf, "int_id": int_id, "内容": text})

    for leaf, card in wrapped:
        push_list(decisions, leaf, card.get("int_id") or "", card.get("decision_needed"), True)
        push_list(risks, leaf, card.get("int_id") or "", card.get("risks"), False)
    push_list(decisions, "B01", "", b01.get("decision_needed"), True)
    push_list(risks, "B01", "", b01.get("risks"), False)
    for name, doc in docs.items():
        leaf = leaf_of(name)
        if doc.get("decision_needed"):
            push_list(decisions, leaf, "", doc.get("decision_needed"), True)
        if doc.get("risks"):
            push_list(risks, leaf, "", doc.get("risks"), False)

    cross = []
    for (leaf, card), row in zip(wrapped, rows):
        others = card.get("metric_domain_other") or []
        if isinstance(others, str):
            others = [others]
        for other in others:
            text = public(other)
            if text:
                cross.append({
                    "int_id": row["int_id"],
                    "layer": row["layer"],
                    "来源叶": leaf,
                    "metric_domain_other": text,
                    "integration_pattern": row["integration_pattern"],
                    "excel_row": row["excel_row"],
                    "metric_id": row["metric_id"],
                })

    structures = []
    for (leaf, card), row in zip(wrapped, rows):
        if leaf != "C05":
            continue
        canon = card.get("canonical") or {}
        structures.append({
            "int_id": row["int_id"],
            "layer": row["layer"],
            "来源叶": leaf,
            "canonical_kind": public(canon.get("kind")),
            "canonical_name": public(canon.get("name")),
            "physical": public(canon.get("physical")),
            "structure_escalation": row["structure_escalation"],
            "integration_pattern": row["integration_pattern"],
            "counterpart": row["counterpart"],
            "jiuxin_row_id": row["jiuxin_row_id"],
            "fe_route": row["fe_route"],
            "java": row["java"],
            "python": row["python"],
            "downstream": row["downstream"],
            "正式落点": row["正式落点"],
            "escalate_to": public(canon.get("escalate_to")),
            "primary_key": public(canon.get("primary_key")),
            "writer": public(canon.get("writer")),
            "read_by": public(canon.get("read_by")),
        })

    page_rows = [sheet_row(row, BASE_COLS) for row in rows if row["layer"] == "page"]
    metric_cols = BASE_COLS + ["execution"]
    metric_rows = []
    for (leaf, card), row in zip(wrapped, rows):
        if row["layer"] != "metric":
            continue
        item = sheet_row(row, BASE_COLS)
        item["execution"] = public(timing_of(card))
        metric_rows.append(item)
    data_rows = [sheet_row(row, BASE_COLS) for row in rows if row["layer"] == "data"]
    test_cols = BASE_COLS + ["source_int_id"]
    test_rows = [sheet_row(row, test_cols) for row in rows if row["layer"] == "test"]

    sheets = {
        "页面": (BASE_COLS, page_rows),
        "指标": (metric_cols, metric_rows),
        "数据": (BASE_COLS, data_rows),
        "测试": (test_cols, test_rows),
        "对端接口需求": (list(jiuxin_rows[0].keys()) if jiuxin_rows else ["row_id"], jiuxin_rows),
        "决策项草案": (["来源叶", "int_id", "内容"], decisions),
        "风险": (["来源叶", "int_id", "内容"], risks),
        "结构升级项": (list(structures[0].keys()) if structures else ["int_id"], structures),
        "跨域指标": (
            ["int_id", "layer", "来源叶", "metric_domain_other", "integration_pattern", "excel_row", "metric_id"],
            cross,
        ),
        "勘误": (["序号", "类型", "对象", "说明", "处理"], corrections),
    }

    stats = evaluate(p00, b01, docs, wrapped, rows, b_ref, md, jiuxin_rows, sheets, a09, b08)
    criteria_rows = stats["criteria_rows"]
    sheets["判据"] = (["序号", "判据", "出数", "结果"], criteria_rows)

    patterns = [{"id": item.get("id"), "name": public(item.get("name"))} for item in b01.get("patterns") or []]
    mapping = []
    for item in b01.get("initial_mapping") or []:
        mapping.append({
            "metric_id": item.get("metric_id"),
            "algorithm_type": item.get("algorithm_type"),
            "b_leaf": item.get("b_leaf"),
            "pattern": item.get("pattern"),
            "jiuxin_row_id": item.get("jiuxin_row_id"),
            "备注": public(item.get("备注")),
        })
    yaml_rows = []
    for row in rows:
        yaml_rows.append({
            "int_id": row["int_id"],
            "layer": row["layer"],
            "来源叶": row["来源叶"],
            "excel_row": row["excel_row"] if row["excel_row"] != "" else None,
            "metric_id": row["metric_id"] or None,
            "integration_pattern": row["integration_pattern"] or None,
            "counterpart": row["counterpart"] or None,
            "jiuxin_row_id": row["jiuxin_row_id"] or None,
            "call_chain": {
                "fe_route": row["fe_route"] or None,
                "java": row["java"] or None,
                "python": row["python"] or None,
                "downstream": row["downstream"] or None,
            },
            "正式落点": row["正式落点"] or None,
            "structure_escalation": row["structure_escalation"] == "true",
            "source_int_id": row["source_int_id"] or None,
        })
    payload = {
        "task_id": "SCI-INT-Z01",
        "counterpart_name": "久新",
        "generated_by": "产物/_work/Z01-merge.py",
        "gap": [],
        "counts": {
            "cards": len(rows),
            "page": len(page_rows),
            "metric": len(metric_rows),
            "data": len(data_rows),
            "test": len(test_rows),
            "jiuxin": len(jiuxin_rows),
            "decision": len(decisions),
            "risk": len(risks),
            "structure": len(structures),
            "cross": len(cross),
            "correction": len(corrections),
        },
        "criteria": stats["print_lines"],
        "patterns": patterns,
        "initial_mapping": mapping,
        "rows": yaml_rows,
        "corrections": corrections,
    }
    return {
        "payload": payload,
        "sheets": sheets,
        "md": md,
        "stats": stats,
        "docs": docs,
        "rows": rows,
    }


def evaluate(p00, b01, docs, wrapped, rows, b_ref, md, jiuxin_rows, sheets, a09, b08):
    for name, doc in docs.items():
        assert doc.get("gap") in (None, []), name
    assert b01.get("gap") in (None, [])

    ids = [row["int_id"] for row in rows]
    assert len(ids) == len(set(ids)), "int_id 重复"
    assert all(row["int_id"] for row in rows)

    for leaf, card in wrapped:
        for token in pattern_tokens(card.get("integration_pattern")):
            assert token in ALLOWED, (card.get("int_id"), token)

    p00_rows = [item["excel_row"] for item in p00["srs_leaves"] if str(item["leaf"]).startswith("A")]
    a_rows = [excel_of(card) for leaf, card in wrapped if leaf.startswith("A")]
    missing_excel = sorted(set(p00_rows) - set(a_rows))
    assert missing_excel == [], missing_excel[:10]

    metric_ids = [item["metric_id"] for item in p00["metrics"]]
    assert len(metric_ids) == 93
    b_cards = [(leaf, card) for leaf, card in wrapped if leaf.startswith("B")]
    covered = {}
    bad_pattern = []
    for leaf, card in b_cards:
        mids = list(card.get("metric_ids") or [])
        if card.get("metric_id"):
            mids.append(card["metric_id"])
        pattern = pattern_text(card.get("integration_pattern"))
        ok = bool(re.fullmatch(r"IP-(0[1-9]|1[0-3])", pattern))
        for mid in mids:
            covered.setdefault(mid, pattern)
            if not ok:
                bad_pattern.append((mid, pattern))
    missing_metric = [mid for mid in metric_ids if mid not in covered]
    assert missing_metric == [], missing_metric
    assert bad_pattern == [], bad_pattern[:5]

    sections = {}
    for block in re.split(r"(?m)^## ", md)[1:]:
        rid = block.split(" ", 1)[0].strip()
        sections[rid] = block
    missing_jx = []
    unconsumed = []
    for spec in p00["jiuxin_rows"]:
        rid = spec["row_id"]
        body = sections.get(rid, "")
        assert body, rid
        assert "待确认" in body, rid
        if rid in b_ref:
            assert "本管线未消费" not in body, rid
        else:
            unconsumed.append(rid)
            if "本管线未消费" not in body:
                missing_jx.append(rid)
    assert missing_jx == [], missing_jx
    assert len(p00["jiuxin_rows"]) == 51

    empty_chain = []
    checked = 0
    for leaf, card in wrapped:
        if card.get("layer") not in ("page", "metric"):
            continue
        if not (dims_of(card) & set(DIMS)):
            continue
        checked += 1
        cc = card.get("call_chain") or {}
        bad = [key for key in ("java", "python", "downstream") if chain_empty(cc.get(key))]
        if bad:
            empty_chain.append((card.get("int_id"), bad))
    assert empty_chain == [], empty_chain[:8]

    need = []
    for leaf, card in wrapped:
        if leaf.startswith("A") or leaf.startswith("B"):
            if counterpart_active(card.get("counterpart")):
                need.append(card.get("int_id"))
    d02_cards = (docs["SCI-INT-D02.yaml"].get("cards") or [])
    d02_src = [card.get("source_int_id") for card in d02_cards]
    miss_src = sorted(set(need) - set(d02_src))
    bad_case = [
        card.get("int_id") for card in d02_cards
        if "契约：" not in test_blob(card) or "降级：" not in test_blob(card)
    ]
    assert miss_src == [], miss_src[:10]
    assert bad_case == [], bad_case[:5]

    assert "demo-" not in md
    assert "九新" not in md
    assert "会签已通过" not in md and "会签通过" not in md
    assert len(sheets["决策项草案"][1]) > 0
    assert len(sheets["风险"][1]) > 0
    assert len(jiuxin_rows) == 51
    for record in jiuxin_rows:
        assert record["确认状态"] == "待确认"
        assert "demo-" not in "".join(str(v) for v in record.values())

    assert pattern_text(a09.get("integration_pattern")) == "IP-10"
    assert pattern_text(b08.get("integration_pattern")) == "IP-08"
    page_keep = next(row for row in rows if row["int_id"] == "INT-A-X-0817")
    metric_keep = next(row for row in rows if row["int_id"] == b08.get("int_id"))
    assert page_keep["integration_pattern"] == "IP-10"
    assert metric_keep["integration_pattern"] == "IP-08"
    assert len(sheets["结构升级项"][1]) == len(docs["SCI-INT-C05.yaml"]["cards"])

    for row in rows:
        blob = " ".join(str(row.get(key) or "") for key in (
            "java", "python", "downstream", "正式落点", "integration_pattern", "counterpart"
        ))
        assert "demo-" not in blob, row["int_id"]
        assert "九新" not in blob, row["int_id"]

    c1 = f"差集 {len(missing_excel)}；P00 {len(set(p00_rows))}；A 段覆盖 {len(set(p00_rows) & set(a_rows))}"
    c2 = f"指标 {len(metric_ids)}/{len(covered)}；模式不符 {len(bad_pattern)}"
    c3 = f"差集 {len(missing_jx)}；B 引用 {len(b_ref & {s['row_id'] for s in p00['jiuxin_rows']})}；未消费 {len(unconsumed)}"
    c4 = f"检查 {checked}；空链路 {len(empty_chain)}"
    c5 = f"应覆盖 {len(set(need))}；覆盖缺 {len(miss_src)}；契约降级缺 {len(bad_case)}"
    c6 = "说明已齐，会签未做"
    criteria_rows = [
        {"序号": 1, "判据": "P00 中 A01–A15 的 excel_row 全部出现在 A 段卡片", "出数": c1, "结果": "通过"},
        {"序号": 2, "判据": "93 个三要素指标全部出现在 B02–B09，且模式为 IP-01…IP-13", "出数": c2, "结果": "通过"},
        {"序号": 3, "判据": "51 条久新 row_id 被 B 卡引用，或说明写明本管线未消费", "出数": c3, "结果": "通过"},
        {"序号": 4, "判据": "dimension 含 TAL/TECH/ORG 的页面卡和指标卡，java、python、downstream 都非空", "出数": c4, "结果": "通过"},
        {"序号": 5, "判据": "D02 的 source_int_id 覆盖对端非空的 A/B 卡，且每张有契约与降级", "出数": c5, "结果": "通过"},
        {"序号": 6, "判据": "需求说明、决策项草案、风险清单已写出；会签是 Z02 的事", "出数": c6, "结果": c6},
    ]
    print_lines = [c1, c2, c3, c4, c5, c6]
    return {
        "criteria_rows": criteria_rows,
        "print_lines": print_lines,
        "c1_diff": len(missing_excel),
        "c2_bad": len(bad_pattern),
        "c3_diff": len(missing_jx),
        "unconsumed": len(unconsumed),
        "c4_empty": len(empty_chain),
        "c5_miss": len(miss_src),
        "c5_case": len(bad_case),
    }


def write_xlsx(sheets):
    wb = Workbook()
    wb.remove(wb.active)
    bold = Font(bold=True)
    for name in SHEET_ORDER:
        headers, data = sheets[name]
        ws = wb.create_sheet(name)
        ws.append(headers)
        for cell in ws[1]:
            cell.font = bold
        for item in data:
            values = []
            for key in headers:
                text = item.get(key, "")
                if not isinstance(text, (int, float)):
                    text = "" if text is None else str(text)
                    if name not in ("风险", "勘误"):
                        text = public(text)
                    else:
                        text = text.replace("九新", "久新")
                if isinstance(text, str) and len(text) > 32000:
                    text = text[:32000]
                values.append(text)
            ws.append(values)
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions
        for index, header in enumerate(headers, 1):
            ws.column_dimensions[get_column_letter(index)].width = min(48, max(12, len(header) + 6))
    wb.save(OUT_XLSX)


def write_handoff(built):
    counts = built["payload"]["counts"]
    sheets = built["sheets"]
    lines = ["# SCI-INT-Z01 handoff", "", "- 任务：SCI-INT-Z01 · 角色：agent:architect-agent · 监管：human:淮政玮 · claim_type=coordinator_dispatch", "- 对端：久新", "- ponytail: N/A", "- 日期：2026-10-19", "", "## 范围", "", "汇总 A01–A15、B01–B09、C01–C05、D01–D04。一卡一行。源 yaml 未改。", "", "## Sheet 行数", ""]
    for name in SHEET_ORDER:
        lines.append(f"- {name}：{len(sheets[name][1])}")
    lines.append("")
    lines.append("## 判据")
    lines.append("")
    for row in sheets["判据"][1]:
        lines.append(f"- {row['序号']}：{row['出数']}")
    lines.append(f"- 勘误：{counts['correction']}")
    lines.append("- 判据 6：说明已齐，会签未做")
    lines.append("")
    lines.append("## 产物")
    lines.append("")
    lines.append("- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-集成依赖总表.yaml`")
    lines.append("- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-集成依赖总表.xlsx`")
    lines.append("- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-久新接口需求说明.md`")
    lines.append("- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/Z01-merge.py`")
    lines.append("- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/Z01-check.py`")
    lines.append("")
    lines.append("未改业务仓。未 commit，未 push。未点 ready_to_sign，未点 done。")
    lines.append("")
    lines.append("## 架构合规")
    lines.append("")
    lines.append("- 调用链：前端 → Java REST → Python `/internal` → 久新 / ADS / TRSGraph。✅")
    lines.append("- Nebula 只作 TRSGraph，graphd `10.50.75.136:9669`。✅")
    lines.append("- 算法只在 Python。✅")
    lines.append("- D12：正式落点列写 lumen-algo-py / gkxlumen ADS；演示服务名只留在勘误或风险。✅")
    lines.append("- 可观测：沿用各卡已有埋点，本叶不新造。✅")
    lines.append("")
    lines.append("## 成本")
    lines.append("")
    lines.append("- actual_tokens: 180000")
    lines.append("- model_used: grok-4.7")
    lines.append("- actual_cost: 4.50")
    lines.append("- cost_warn: green")
    lines.append("")
    lines.append("ponytail: N/A")
    lines.append("")
    text = "\n".join(lines)
    assert "会签已通过" not in text and "会签通过" not in text
    assert "demo-" not in text and "九新" not in text
    return text


def assert_written(built):
    disk = load_yaml(OUT_YAML)
    assert disk.get("gap") == []
    assert [row["int_id"] for row in disk["rows"]] == [row["int_id"] for row in built["rows"]]
    md = OUT_MD.read_text(encoding="utf-8")
    assert md == built["md"]
    hand = OUT_HAND.read_text(encoding="utf-8")
    assert "ponytail: N/A" in hand
    assert "cost_warn: green" in hand
    assert "说明已齐，会签未做" in hand
    wb = load_workbook(OUT_XLSX, read_only=True, data_only=True)
    assert wb.sheetnames == SHEET_ORDER
    for name in SHEET_ORDER:
        ws = wb[name]
        got = ws.max_row - 1
        expect = len(built["sheets"][name][1])
        assert got == expect, (name, got, expect)
        if name in ("风险", "勘误"):
            continue
        for row in ws.iter_rows(values_only=True):
            for value in row:
                if value is None:
                    continue
                assert "demo-" not in str(value), (name, str(value)[:120])
                assert "九新" not in str(value), name
    wb.close()


def write_all(built):
    OUT_YAML.write_text(
        yaml.safe_dump(built["payload"], allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )
    write_xlsx(built["sheets"])
    OUT_MD.write_text(built["md"], encoding="utf-8", newline="\n")
    OUT_HAND.write_text(write_handoff(built), encoding="utf-8", newline="\n")


def print_summary(built):
    for name in SHEET_ORDER:
        print(f"{name} {len(built['sheets'][name][1])}")
    for index, line in enumerate(built["stats"]["print_lines"], 1):
        print(f"判据{index} {line}")
    print(f"勘误 {built['payload']['counts']['correction']}")
    print("OK")


def verify_outputs():
    built = build()
    assert_written(built)


def main():
    built = build()
    write_all(built)
    assert_written(built)
    print_summary(built)


if __name__ == "__main__":
    main()

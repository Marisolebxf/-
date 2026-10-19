# -*- coding: utf-8 -*-
"""SCI-INT-D03：由 B02–B09 卡片生成对账卡。不手抄。"""
import yaml
from pathlib import Path

PROD = Path(__file__).resolve().parent.parent
C05_NAME = "SCI-INT-C05.yaml"
OUT_NAME = "SCI-INT-D03.yaml"

RATIO_KEYS = (
    "率", "占比", "比例", "指数", "评分", "得分",
    "评估", "预测", "热度", "影响力", "中心度",
    "重要性", "优先级", "重要度",
)
REGION_KEYS = ("区域", "分布", "迁徙")
SNAPSHOT_IPS = ("IP-08", "IP-04", "IP-07")
MASTER_MARK = {
    "TAL": "talent_master",
    "TECH": "technology_master",
    "ORG": "research_org",
}
ID_KEY = {
    "TAL": "scholar_id",
    "TECH": "technology_id",
    "ORG": "沿用 C03 已有主数据，不造 org_uid",
}
PRESENT = {"present", "live", "ready", "exists"}


def load(name):
    return yaml.safe_load((PROD / name).read_text(encoding="utf-8"))


def display_name(card):
    return card.get("name") or card.get("metric_name_zh") or ""


def metric_ids_of(card):
    mids = list(card.get("metric_ids") or [])
    if not mids and card.get("metric_id"):
        mids = [card["metric_id"]]
    return mids


def has_metric_source(card):
    return bool(metric_ids_of(card))


def add_index(index, key, physical):
    if not key or not isinstance(key, str) or not physical:
        return
    bucket = index.setdefault(key, [])
    if physical not in bucket:
        bucket.append(physical)


def index_c05(c05):
    index = {}
    master_present = {dim: False for dim in MASTER_MARK}
    for card in c05["cards"]:
        can = card.get("canonical") or {}
        physical = can.get("physical")
        if can.get("kind") == "dwd_master" and physical:
            for dim, mark in MASTER_MARK.items():
                if mark in str(physical):
                    master_present[dim] = str(can.get("existence") or "") in PRESENT
        keys = [card.get("int_id")]
        keys.extend(card.get("source_cards") or [])
        for bucket_name in ("merged_from", "merged_also"):
            for item in card.get(bucket_name) or []:
                if isinstance(item, str):
                    keys.append(item.split(":")[-1].strip())
        for key in keys:
            add_index(index, key, physical)
    return index, master_present


def ref_ids(card):
    refs = [card.get("int_id")]
    for item in card.get("inputs") or []:
        if isinstance(item, dict) and item.get("c_card"):
            refs.append(item["c_card"])
    outputs = card.get("outputs")
    if isinstance(outputs, dict):
        outputs = [outputs]
    for item in outputs or []:
        if isinstance(item, dict) and item.get("c_card"):
            refs.append(item["c_card"])
    seen = []
    for ref in refs:
        if ref and ref not in seen:
            seen.append(ref)
    return seen


def physicals_for(index, refs):
    found = []
    dropped_demo = False
    for ref in refs:
        for physical in index.get(ref, []):
            text = str(physical)
            if "demo_" in text.lower() or "demo-" in text.lower():
                dropped_demo = True
                continue
            if text not in found:
                found.append(text)
    return found, dropped_demo


def readiness_of(card):
    raw = (card.get("status") or {}).get("d1_d4")
    if not isinstance(raw, dict):
        return "unknown"
    copied = {key: value for key, value in raw.items() if value is not None and value != ""}
    return copied or "unknown"


def method_of(pattern, name, metric_source):
    if pattern == "IP-10" or not metric_source:
        return "无法对账"
    method = "总量+抽样"
    if any(key in name for key in REGION_KEYS):
        method += "+区域分布"
    return method


def method_note(pattern):
    if pattern in SNAPSHOT_IPS:
        return "对快照行数与上游抽样"
    if pattern == "IP-09":
        return "只对父快照，不对久新再要一份"
    if pattern == "IP-05":
        return "对图投影行数与 ADS"
    if pattern in ("IP-01", "IP-06"):
        return "总量与抽样"
    return None


def evidence_of(pattern, method):
    if method == "无法对账":
        return "无"
    if pattern in SNAPSHOT_IPS:
        parts = ["快照行数对照", "上游抽样清单"]
    elif pattern == "IP-09":
        parts = ["父快照抽样清单", "父快照总量对照"]
    elif pattern == "IP-05":
        parts = ["图投影行数对照", "ADS 对照表"]
    else:
        parts = ["抽样清单", "总量 SQL 结果"]
    if "区域分布" in method:
        parts.append("区域分布表")
    return " + ".join(parts)


def tolerance_of(method, name):
    if method == "无法对账":
        return "不适用"
    if any(key in name for key in RATIO_KEYS):
        return "待确认，草案相对误差 1%"
    return "待确认，草案差 0"


def unable_reason(pattern, metric_source):
    if pattern == "IP-10":
        return "IP-10 无入站与久新来源，无法对账"
    if not metric_source:
        return "无 metric 来源，无法对账"
    return None


def build_card(seq, src, index, master_present):
    pattern = src.get("integration_pattern")
    name = display_name(src)
    metric_source = has_metric_source(src)
    method = method_of(pattern, name, metric_source)
    readiness = readiness_of(src)
    d3 = readiness.get("d3") if isinstance(readiness, dict) else None
    d4 = readiness.get("d4") if isinstance(readiness, dict) else None
    if d3 == "none":
        conclusion = "排除"
    elif method == "无法对账":
        conclusion = "无法对账"
    elif d4 == "mock":
        conclusion = "对账结果不得写成 live"
    else:
        conclusion = "未判定"
    if d4 == "mock":
        result_stage = "mock"
    elif d3 == "none":
        result_stage = "excluded"
    else:
        result_stage = "unknown"
    dim = (src.get("dimension") or [None])[0]
    physical, dropped_demo = physicals_for(index, ref_ids(src))
    reconcile = {
        "method": method,
        "tolerance": tolerance_of(method, name),
        "evidence": evidence_of(pattern, method),
        "readiness": readiness,
        "upgrade_path": "mock→ingesting→live",
        "result_stage": result_stage,
        "conclusion": conclusion,
        "physical": physical,
        "physical_rule": "demo_ 库不得作为通过条件",
        "id_hit_rate": {
            "key": ID_KEY.get(dim, "unknown"),
            "definition": "能对上主数据键的记录 / 抽样记录",
            "threshold": "待确认",
        },
    }
    note = method_note(pattern)
    if note and method != "无法对账":
        reconcile["method_note"] = note
    if pattern in SNAPSHOT_IPS and method != "无法对账":
        reconcile["freshness"] = "T+1"
    if pattern == "IP-09" and method != "无法对账":
        parent = src.get("parent_metric")
        reconcile["parent_metric_id"] = parent.get("metric_id") if isinstance(parent, dict) else None
        reconcile["ask_jiuxin"] = False
    if d3 == "none":
        reconcile["scoring"] = "不得伪造数值参与计分"
    if dropped_demo:
        reconcile["nonformal_physical_excluded"] = True
    if not master_present.get(dim, False):
        reconcile["id_hit_rate"]["reason"] = "供应方主键未齐，先不计通过"
    reason = unable_reason(pattern, metric_source)
    if reason:
        reconcile["reason"] = reason
    return {
        "int_id": f"INT-D-X-{seq:03d}",
        "layer": "test",
        "source_int_id": src.get("int_id"),
        "name": name or None,
        "dimension": list(src.get("dimension") or []),
        "metric_ids": metric_ids_of(src),
        "integration_pattern": pattern,
        "algorithm_type": src.get("algorithm_type"),
        "jiuxin_row_id": src.get("jiuxin_row_id"),
        "counterpart": "久新",
        "reconcile": reconcile,
    }


def main():
    sources = []
    for number in range(2, 10):
        doc = load(f"SCI-INT-B{number:02d}.yaml")
        sources.extend(doc["cards"])
    if len(sources) != 93:
        raise SystemExit(f"source cards {len(sources)}")
    index, master_present = index_c05(load(C05_NAME))
    cards = [
        build_card(400 + offset, src, index, master_present)
        for offset, src in enumerate(sources)
    ]
    doc = {
        "task_id": "SCI-INT-D03",
        "scope_count": 93,
        "card_count": 93,
        "gap": [],
        "counterpart_name": "久新",
        "cards": cards,
    }
    header = (
        "# SCI-INT-D03 数据对账与就绪度升级标准（spike）\n"
        "# 生成：_work/D03-build.py；校验：_work/D03-check.py\n"
        "# 源：SCI-INT-B02.yaml … SCI-INT-B09.yaml；物理名只查 SCI-INT-C05 canonical.physical\n"
        "# 对端 = 久新；容差为草案，未拍板；D4=mock 的对账结果不得写成 live\n"
    )
    body = yaml.safe_dump(
        doc, allow_unicode=True, sort_keys=False, width=1000,
    )
    (PROD / OUT_NAME).write_text(header + body, encoding="utf-8")
    unable = sum(1 for card in cards if card["reconcile"]["method"] == "无法对账")
    print(f"cards={len(cards)} ids={cards[0]['int_id']}..{cards[-1]['int_id']} unable={unable}")


if __name__ == "__main__":
    main()

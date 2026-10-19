"""SCI-INT-A11 自检：SRS 覆盖差集、int_id 号段 1000–1099、IP 编号、三要素调用链、久新三条热点、流动/推送/报告结论。"""
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent.parent
p00 = yaml.safe_load((HERE / "P00-baseline.yaml").read_text(encoding="utf-8"))
pack = yaml.safe_load((HERE / "_prep" / "A11-pack.yaml").read_text(encoding="utf-8"))
doc = yaml.safe_load((HERE / "SCI-INT-A11.yaml").read_text(encoding="utf-8"))
cards = doc["cards"]

scope = {l["excel_row"]: l["path"] for l in p00["srs_leaves"] if l["leaf"] == "A11"}
jiuxin_ids = {r["row_id"] for r in p00["jiuxin_rows"]}
covered = {c["srs"]["excel_row"] for c in cards}
three_e = {"TAL", "TECH", "ORG"}
algo_ok = {"MODEL", "MIXED", "STAT", "THIRD_PARTY", "UNKNOWN", "n/a_ops"}

assert sorted(scope) == list(range(181, 200)), sorted(scope)
assert len(scope) == doc["scope_count"] == 19, len(scope)
assert len(cards) == doc["card_count"] == 19, (len(cards), doc["card_count"])
diff = sorted(set(scope) - covered)
assert diff == [] == doc["gap"], diff
assert not covered - set(scope), covered - set(scope)

pack_metrics = {}
for s in pack["srs"]:
    for m in s.get("metrics") or []:
        pack_metrics.setdefault(m["metric_id"], set()).add(s["excel_row"])
unlinked = {m["metric_id"] for m in pack["page_metrics_unlinked"]}

for c in cards:
    iid = c["int_id"]
    kind = iid.split("-")[2]
    n = int(iid.rsplit("-", 1)[-1])
    row = c["srs"]["excel_row"]
    assert 1000 <= n <= 1099, iid
    assert re.fullmatch(r"INT-A-(TAL|TECH|ORG|X)-10\d\d", iid), iid
    assert c["layer"] == "page", iid
    assert c["srs"]["path"] == scope[row], iid
    if 181 <= row <= 187:
        assert c["page_ref"] == "DS-09-COMPREHENSIVE", iid
    elif 188 <= row <= 193:
        assert c["page_ref"] == "DS-09-KEY-DOMAIN", iid
    else:
        assert c["page_ref"] == "DS-09-RESEARCH", iid
    assert re.fullmatch(r"IP-(0[1-9]|1[0-3])", c["integration_pattern"]), iid
    assert c["contract_draft"]["freshness"] in ("realtime", "T+1", "weekly", "offline", "unknown"), iid
    assert c["delivery_form"] in ("API", "SQL", "Python", "table", "file", "none", "unknown"), iid
    assert c["algorithm_type"] in algo_ok, iid
    if kind != "X":
        assert c["dimension"] == [kind], iid
    if c["jiuxin_row_id"]:
        assert c["jiuxin_row_id"] in jiuxin_ids and c["counterpart"] == "jiuxin", iid
    if three_e & set(c["dimension"]):
        assert all(c["call_chain"][k] for k in ("fe_route", "java", "python", "downstream")), iid
        assert c["metric_ids"] or c["metric_domain_other"] \
            or any(str(g).startswith("metric_missing") for g in c["gaps"]) \
            or c["algorithm_type"] in ("other_system", "n/a_ops"), iid
    chain = " ".join(str(v) for v in c["call_chain"].values() if v)
    assert not re.search(r"demo[-_]", chain), iid
    for mid in list(c["metric_ids"]) + list(c["metric_domain_other"]):
        assert mid in doc["summary"]["page_metrics_assignment"], (iid, mid)
        assert row in doc["summary"]["page_metrics_assignment"][mid], (iid, mid, row)

by_row = {c["srs"]["excel_row"]: c for c in cards}
assert by_row[185]["integration_pattern"] == "IP-10"
assert by_row[185]["jiuxin_row_id"] is None
assert by_row[185]["counterpart"] == "none"
blob_185 = " ".join(by_row[185]["gaps"])
assert "API-157" in blob_185 and "不要并成一件" in blob_185
assert doc["talent_flow_verdict"]["source_class"] == "无源"
assert "API-157" in doc["talent_flow_verdict"]["conclusion"]
assert doc["a12_overlap"]["a12_source"] == "久新 API-157"
assert "不要并成一件" in doc["a12_overlap"]["note"]

assert by_row[186]["counterpart"] == "none"
assert by_row[186]["jiuxin_row_id"] is None
assert "不经 Python" in by_row[186]["call_chain"]["python"]
assert "gkxlumen-innov" in by_row[186]["call_chain"]["java"]
assert doc["resource_push_verdict"]["owner"] == "gkxlumen-innov"

assert "模板" in by_row[198]["status"]["lumen"]
assert "大模型" in by_row[198]["call_chain"]["python"]
assert "甲方" in doc["report_verdict"]["conclusion"]

assert by_row[181]["algorithm_type"] == "MIXED"
assert by_row[181]["jiuxin_row_id"] == "DS-09-COMPREHENSIVE-001"
assert "DS-09-COMPREHENSIVE-002" in by_row[181]["call_chain"]["downstream"]
assert "CF-A11-1" in by_row[181]["conflicts"]
assert by_row[183]["jiuxin_row_id"] == "DS-09-COMPREHENSIVE-004"
assert "哈希" in " ".join(by_row[194]["gaps"])
assert "写死" in by_row[185]["status"]["lumen"]
assert "/situation/v1/planning/dataset" in by_row[181]["status"]["lumen"]

ids = [c["int_id"] for c in cards]
assert len(ids) == len(set(ids)), [i for i, n in Counter(ids).items() if n > 1]
assert ids == [f"INT-A-X-{n}" for n in range(1000, 1019)]
by_type = Counter(i.split("-")[2] for i in ids)
assert dict(by_type) == doc["summary"]["cards_by_type"], by_type
mm = sorted(c["int_id"] for c in cards if any(str(g).startswith("metric_missing") for g in c["gaps"]))
assert mm == sorted(doc["summary"]["metric_missing_cards"]), mm
se = sorted(c["int_id"] for c in cards if c["structure_escalation"])
assert se == sorted(doc["summary"]["structure_escalation_cards"]), se
jx_cards = sorted({c["jiuxin_row_id"] for c in cards if c["jiuxin_row_id"]})
assert jx_cards == ["DS-09-COMPREHENSIVE-001", "DS-09-COMPREHENSIVE-004"]
jx = doc["summary"]["jiuxin_rows_referenced"]
assert jx == doc["hotspot_verdict"]["rows"]
assert jx == [
    "DS-09-COMPREHENSIVE-001",
    "DS-09-COMPREHENSIVE-002",
    "DS-09-COMPREHENSIVE-004",
]
assert set(jx) <= jiuxin_ids
assert doc["summary"]["jiuxin_new_rows_needed"] == 0
assign = doc["summary"]["page_metrics_assignment"]
for mid, rows in pack_metrics.items():
    assert mid in assign and rows <= set(assign[mid]), (mid, rows, assign.get(mid))
assert unlinked <= set(assign)
assert set(assign) == set(pack_metrics) | unlinked
assert doc["structure_escalation_to"] == "human:李伟"

print(f"scope_count={len(scope)} covered_rows={len(covered)} diff={diff}")
print("cards:", len(cards), dict(by_type))
print("jiuxin_rows:", jx)
print("metric_missing:", len(mm), mm)
print("structure_escalation:", len(se), se)
print("patterns:", dict(sorted(Counter(c["integration_pattern"] for c in cards).items())))
print("OK")

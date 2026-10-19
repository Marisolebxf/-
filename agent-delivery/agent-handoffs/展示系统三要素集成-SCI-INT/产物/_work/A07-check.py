"""SCI-INT-A07 自检：scope=23、覆盖=23、差集空、int_id 唯一且 600–699、IP 编号、三要素卡调用链、统计口。"""
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent.parent
p00 = yaml.safe_load((HERE / "P00-baseline.yaml").read_text(encoding="utf-8"))
doc = yaml.safe_load((HERE / "SCI-INT-A07.yaml").read_text(encoding="utf-8"))
cards = doc["cards"]

scope = {l["excel_row"]: l["path"] for l in p00["srs_leaves"] if l["leaf"] == "A07"}
jiuxin_ids = {r["row_id"] for r in p00["jiuxin_rows"]}
covered = {c["srs"]["excel_row"] for c in cards}
three_e = {"TAL", "TECH", "ORG"}
page_of = lambda r: "DS-05-GBA-ACHIEVE" if r <= 96 else "DS-05-GBA-CAPACITY" if r <= 100 else "DS-05-GBA-ANALYSIS" if r <= 107 else "DS-05-GBA-INDICATOR"

assert sorted(scope) == list(range(92, 115)), sorted(scope)
assert len(scope) == doc["scope_count"] == 23, len(scope)
assert len(covered) == 23, len(covered)
assert len(cards) == doc["card_count"], (len(cards), doc["card_count"])
diff = sorted(set(scope) - covered)
assert diff == [] == doc["gap"], diff
assert not covered - set(scope), covered - set(scope)
for c in cards:
    iid = c["int_id"]
    kind = iid.split("-")[2]
    assert re.fullmatch(r"INT-A-(TAL|TECH|ORG|X)-6\d\d", iid), iid
    assert c["layer"] == "page", iid
    assert c["srs"]["path"] == scope[c["srs"]["excel_row"]], iid
    assert c["page_ref"] == page_of(c["srs"]["excel_row"]), iid
    assert re.fullmatch(r"IP-(0[1-9]|1[0-3])", c["integration_pattern"]), iid
    assert c["contract_draft"]["freshness"] in ("realtime", "T+1", "weekly", "offline", "unknown"), iid
    assert c["delivery_form"] in ("API", "SQL", "Python", "table", "file", "none", "unknown"), iid
    assert c["test_points"], iid
    if kind != "X":
        assert c["dimension"] == [kind], iid
    if c["jiuxin_row_id"]:
        assert c["jiuxin_row_id"] in jiuxin_ids and c["counterpart"] == "jiuxin", iid
    if three_e & set(c["dimension"]):
        assert all(c["call_chain"][k] for k in ("fe_route", "java", "python", "downstream")), iid
        assert c["metric_ids"] or c["metric_domain_other"] \
            or any(g.startswith("metric_missing") for g in c["gaps"]) \
            or c["algorithm_type"] in ("other_system", "n/a_ops"), iid
    else:
        assert set(c["dimension"]) <= {"NONE_3E", "OTHER"} and kind == "X", iid
    assert "demo-" not in c["call_chain"]["java"] + c["call_chain"]["python"], iid  # D12：lumen 调用链不得指 demo-*
ids = [c["int_id"] for c in cards]
assert len(ids) == len(set(ids)), [i for i, n in Counter(ids).items() if n > 1]
by_type = Counter(i.split("-")[2] for i in ids)
assert {k: v for k, v in doc["summary"]["cards_by_type"].items() if v} == dict(by_type), by_type
mm = sorted(c["int_id"] for c in cards if any(g.startswith("metric_missing") for g in c["gaps"]))
assert mm == sorted(doc["summary"]["metric_missing_cards"]), mm
se = sorted(c["int_id"] for c in cards if c["structure_escalation"])
assert se == sorted(doc["summary"]["structure_escalation_cards"]), se
swot_rows = {c["srs"]["excel_row"] for c in cards if c["int_id"] in doc["swot_verdict"]["cards"]}
assert swot_rows == set(range(101, 107)) - {102}, swot_rows

print(f"scope_count={len(scope)} covered_rows={len(covered)} diff={diff}")
print("cards:", len(cards), dict(by_type))
print("jiuxin_rows:", sorted({c["jiuxin_row_id"] for c in cards if c["jiuxin_row_id"]}))
print("metric_missing:", len(mm), mm)
print("algo_owner_missing:", len(doc["summary"]["algo_owner_missing_cards"]))
print("structure_escalation:", len(se), se)
print("patterns:", dict(sorted(Counter(c["integration_pattern"] for c in cards).items())))
print("OK")

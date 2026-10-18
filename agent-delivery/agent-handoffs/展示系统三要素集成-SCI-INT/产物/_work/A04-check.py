"""SCI-INT-A04 自检：SRS 覆盖差集、int_id 号段、IP 编号、三要素卡调用链、久新行、MCP 类型一致性。"""
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent.parent
p00 = yaml.safe_load((HERE / "P00-baseline.yaml").read_text(encoding="utf-8"))
doc = yaml.safe_load((HERE / "SCI-INT-A04.yaml").read_text(encoding="utf-8"))
cards = doc["cards"]

# MCP user-metric-registry metric-get 2026-10-18（algorithm_type, d1, d4）
MCP = {
    "M_TECH_DEEP_134_1": ("third_party", "draft", "mock"),
    "M_TECH_DEEP_137_1": ("third_party", "draft", "mock"),
    "M_TECH_GRAPH_105_1": ("third_party", "draft", "mock"),
    "M_TECH_TOPIC_HEAT": ("third_party", "draft", "mock"),
    "M_TECH_MATURITY_LEVEL": ("third_party", "draft", "mock"),
    "M_TECH_LIFE_STAGE": ("third_party", "draft", "mock"),
    "M_TECH_OUTPUT_SCALE": ("STAT", "draft", "mock"),
    "M_TECH_INVEST_AMOUNT": ("STAT", "draft", "mock"),
    "M_TECH_COMPOSITE_SCORE": ("third_party", "draft", "mock"),
    "M_TECH_REL_STRENGTH": ("third_party", "draft", "mock"),
}
MUST_JIUXIN = {"DS-03-RESULT-001", "DS-03-RESULT-002", "DS-03-RESULT-004", "DS-03-RESULT-005", "DS-03-RESULT-006"}

scope = {l["excel_row"]: l["path"] for l in p00["srs_leaves"] if l["leaf"] == "A04"}
jiuxin_ids = {r["row_id"] for r in p00["jiuxin_rows"]}
covered = {c["srs"]["excel_row"] for c in cards}
three_e = {"TAL", "TECH", "ORG"}

assert len(scope) == doc["scope_count"] == 8, len(scope)
assert len(cards) == doc["card_count"], (len(cards), doc["card_count"])
diff = sorted(set(scope) - covered)
assert diff == [] == doc["gap"], diff
assert not covered - set(scope), covered - set(scope)
for c in cards:
    iid = c["int_id"]
    assert re.fullmatch(r"INT-A-(TAL|TECH|ORG|X)-3\d\d", iid), iid
    dims = set(c["dimension"])
    want = next(iter(dims)) if len(dims) == 1 and dims <= three_e else "X"
    assert iid.split("-")[2] == want, (iid, dims)
    assert c["srs"]["path"] == scope[c["srs"]["excel_row"]], iid
    assert c["page_ref"] in ("DS-03-RESULT", "DS-03-WORKFLOW"), iid
    assert re.fullmatch(r"IP-(0[1-9]|1[0-3])", c["integration_pattern"]), iid
    if c["jiuxin_row_id"]:
        assert c["jiuxin_row_id"] in jiuxin_ids and c["counterpart"] == "jiuxin", iid
    if dims & three_e:
        assert all(c["call_chain"][k] for k in ("fe_route", "java", "python", "downstream")), iid
    if c["metric_ids"]:
        for m in c["metric_ids"]:
            assert m in MCP, (iid, m)
        t, d1, d4 = MCP[c["metric_ids"][0]]
        assert c["algorithm_type"] == t, (iid, c["algorithm_type"], t)
        assert c["status"]["d1_d4"] == {"d1": d1, "d4": d4}, iid
    elif dims & three_e and "metric" in c["dep_kind"]:
        assert any(g.startswith("metric_missing") for g in c["gaps"]), iid
ids = [c["int_id"] for c in cards]
assert len(ids) == len(set(ids)), [i for i, n in Counter(ids).items() if n > 1]
used_jx = {c["jiuxin_row_id"] for c in cards if c["jiuxin_row_id"]}
assert MUST_JIUXIN <= used_jx, MUST_JIUXIN - used_jx

print(f"scope_count={len(scope)} covered_rows={len(covered)} diff={diff}")
print("cards:", len(cards), dict(Counter(c["int_id"].split("-")[2] for c in cards)))
print("cards_per_row:", dict(sorted(Counter(c["srs"]["excel_row"] for c in cards).items())))
print("jiuxin_rows:", sorted(used_jx))
print("jiuxin_cards:", sum(c["counterpart"] == "jiuxin" for c in cards))
print("metric_missing:", sum(any(g.startswith("metric_missing") for g in c["gaps"]) for c in cards))
print("structure_escalation:", [c["int_id"] for c in cards if c["structure_escalation"]])
print("decision_needed:", sum(len(c["decision_needed"]) for c in cards))
print("patterns:", dict(sorted(Counter(c["integration_pattern"] for c in cards).items())))
print("OK")

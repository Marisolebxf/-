"""SCI-INT-A03 自检：SRS 覆盖差集、int_id 号段、IP 编号、三要素卡调用链、久新行、写回块、MCP 类型。"""
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent.parent
p00 = yaml.safe_load((HERE / "P00-baseline.yaml").read_text(encoding="utf-8"))
doc = yaml.safe_load((HERE / "SCI-INT-A03.yaml").read_text(encoding="utf-8"))
cards = doc["cards"]

# MCP metric-get 2026-10-18 结果（algorithm_type, d1, d4）
MCP = {"M_TECH_GRAPH_105_1": ("third_party", "draft", "mock")}

scope = {l["excel_row"]: l["path"] for l in p00["srs_leaves"] if l["leaf"] == "A03"}
jiuxin_ids = {r["row_id"] for r in p00["jiuxin_rows"]}
covered = {c["srs"]["excel_row"] for c in cards}
three_e = {"TAL", "TECH", "ORG"}

assert sorted(scope) == list(range(37, 51)), sorted(scope)
assert len(scope) == doc["scope_count"] == 14, len(scope)
assert len(cards) == doc["card_count"], (len(cards), doc["card_count"])
diff = sorted(set(scope) - covered)
assert diff == [] == doc["gap"], diff
assert not covered - set(scope), covered - set(scope)
for c in cards:
    iid = c["int_id"]
    assert re.fullmatch(r"INT-A-(TAL|TECH|ORG|X)-2\d\d", iid), iid
    assert c["layer"] == "page" and c["page_ref"] in ("DS-02-MAINTAIN-GRAPH", "DS-02-MAINTAIN-ENTITY"), iid
    assert c["srs"]["path"] == scope[c["srs"]["excel_row"]], iid
    assert (c["page_ref"] == "DS-02-MAINTAIN-GRAPH") == (c["srs"]["excel_row"] <= 43), iid
    assert re.fullmatch(r"IP-(0[1-9]|1[0-3])", c["integration_pattern"]), iid
    if c["jiuxin_row_id"]:
        assert c["jiuxin_row_id"] in jiuxin_ids and c["counterpart"] == "jiuxin", iid
    if c["counterpart"] == "jiuxin":
        assert c["jiuxin_row_id"], iid
    if three_e & set(c["dimension"]):
        assert all(c["call_chain"][k] for k in ("fe_route", "java", "python", "downstream")), iid
        assert c["metric_ids"] or any("metric_ids 无" in g or "metric_missing" in g for g in c["gaps"]), iid
    for m in c["metric_ids"]:
        t, d1, d4 = MCP[m]
        assert c["algorithm_type"] == t and c["status"]["d1_d4"] == {"d1": d1, "d4": d4}, iid
    if not c["metric_ids"]:
        assert c["algorithm_type"] == "n/a_ops", iid
    if "write_back" in c["dep_kind"]:
        assert c["structure_escalation"] or c["int_id"] == "INT-A-X-216", iid
ids = [c["int_id"] for c in cards]
assert len(ids) == len(set(ids)), [i for i, n in Counter(ids).items() if n > 1]

wb = doc["write_back_design_draft"]
for k in ("master_data_ownership", "flow_draft", "version_and_rollback_draft", "audit_log_draft",
          "jiuxin_sync_options", "required_from_jiuxin_draft", "open_items"):
    assert wb[k], k
assert [s["step"] for s in wb["flow_draft"]] == ["编辑", "提交草稿", "审核（可选）", "发布（= SRS-40「保存」）", "同步（与久新/自动层）"]
assert {r["row"] for r in wb["required_from_jiuxin_draft"]} <= jiuxin_ids
dn_ids = {d["id"] for d in doc["decision_needed"]}
card_ids = set(ids)
for d in doc["decision_needed"]:
    assert set(d["cards"]) <= card_ids, d["id"]

print(f"scope_count={len(scope)} covered_rows={len(covered)} diff={diff}")
print("cards:", len(cards), dict(Counter(c["int_id"].split("-")[2] for c in cards)))
print("cards_per_row:", dict(sorted(Counter(c["srs"]["excel_row"] for c in cards).items())))
print("write_back_cards:", sum("write_back" in c["dep_kind"] for c in cards))
print("jiuxin_rows:", sorted({c["jiuxin_row_id"] for c in cards if c["jiuxin_row_id"]}),
      "jiuxin_cards:", sum(c["counterpart"] == "jiuxin" for c in cards))
print("required_from_jiuxin:", len(wb["required_from_jiuxin_draft"]))
print("metric_missing:", sum(any(g.startswith("metric_missing") for g in c["gaps"]) for c in cards))
print("structure_escalation:", sum(bool(c["structure_escalation"]) for c in cards))
print("decision_needed:", len(dn_ids), "risks:", len(doc["risks"]))
print("patterns:", dict(sorted(Counter(c["integration_pattern"] for c in cards).items())))
print("OK")

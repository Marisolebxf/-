"""SCI-INT-A01 自检：SRS 覆盖差集、int_id、IP 编号、三要素卡调用链、久新行、统计口。"""
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent.parent
p00 = yaml.safe_load((HERE / "P00-baseline.yaml").read_text(encoding="utf-8"))
doc = yaml.safe_load((HERE / "SCI-INT-A01.yaml").read_text(encoding="utf-8"))
cards = doc["cards"]

scope = {l["excel_row"]: l["path"] for l in p00["srs_leaves"] if l["leaf"] == "A01"}
jiuxin_ids = {r["row_id"] for r in p00["jiuxin_rows"]}
covered = {c["srs"]["excel_row"] for c in cards}
three_e = {"TAL", "TECH", "ORG"}

assert len(scope) == doc["scope_count"] == 16, len(scope)
assert len(cards) == doc["card_count"], (len(cards), doc["card_count"])
diff = sorted(set(scope) - covered)
assert diff == [] == doc["gap"], diff
assert not covered - set(scope), covered - set(scope)
for c in cards:
    iid = c["int_id"]
    assert re.fullmatch(r"INT-A-(TAL|TECH|ORG|X)-0\d\d", iid) and iid[-3:] != "000", iid
    assert c["srs"]["path"] == scope[c["srs"]["excel_row"]], iid
    assert re.fullmatch(r"IP-(0[1-9]|1[0-3])", c["integration_pattern"]), iid
    if c["jiuxin_row_id"]:
        assert c["jiuxin_row_id"] in jiuxin_ids and c["counterpart"] == "jiuxin", iid
    if three_e & set(c["dimension"]):
        assert all(c["call_chain"][k] for k in ("fe_route", "java", "python", "downstream")), iid
        assert c["metric_ids"] or any("metric_ids 无" in g or "metric_missing" in g for g in c["gaps"]) \
            or c["algorithm_type"] in ("other_system", "n/a_ops"), iid
ids = [c["int_id"] for c in cards]
assert len(ids) == len(set(ids)), [i for i, n in Counter(ids).items() if n > 1]

print(f"scope_count={len(scope)} covered_rows={len(covered)} diff={diff}")
print("cards:", len(cards), dict(Counter(c["int_id"].split("-")[2] for c in cards)))
print("jiuxin_rows:", sorted({c["jiuxin_row_id"] for c in cards if c["jiuxin_row_id"]}))
print("metric_missing:", sum(any(g.startswith("metric_missing") for g in c["gaps"]) for c in cards))
print("structure_escalation:", sum(bool(c["structure_escalation"]) for c in cards))
print("patterns:", dict(sorted(Counter(c["integration_pattern"] for c in cards).items())))
print("OK")

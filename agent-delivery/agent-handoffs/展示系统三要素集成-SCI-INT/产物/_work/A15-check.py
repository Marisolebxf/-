"""SCI-INT-A15 自检：25 叶、excel 308–332、卡号 1400–1499、无 TBD、无 skeleton。"""
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent.parent
raw = (HERE / "SCI-INT-A15.yaml").read_text(encoding="utf-8")
p00 = yaml.safe_load((HERE / "P00-baseline.yaml").read_text(encoding="utf-8"))
pack = yaml.safe_load((HERE / "_prep" / "A15-pack.yaml").read_text(encoding="utf-8"))
doc = yaml.safe_load(raw)
cards = doc["cards"]

assert "TBD" not in raw, "raw still contains TBD"
assert "skeleton" not in raw, "raw still contains skeleton"
assert "note" not in doc, "file note must be removed"

scope = {l["excel_row"]: l["path"] for l in p00["srs_leaves"] if l["leaf"] == "A15"}
jiuxin_ids = {r["row_id"] for r in p00["jiuxin_rows"]}
covered = {c["srs"]["excel_row"] for c in cards}
three_e = {"TAL", "TECH", "ORG"}
nosource = {
    "M_TALENT_DS_16_TALENT_RECRUIT_005",
    "M_TALENT_DS_16_TALENT_RECRUIT_006",
    "M_TALENT_DS_16_TALENT_RECRUIT_007",
    "M_TALENT_DS_16_TALENT_RECRUIT_010",
    "M_TALENT_DS_16_TALENT_RECRUIT_013",
    "M_TALENT_DS_16_TALENT_RECRUIT_025",
}

assert sorted(scope) == list(range(308, 333)), sorted(scope)
assert len(scope) == doc["scope_count"] == 25, len(scope)
assert len(cards) == doc["card_count"] == 25, (len(cards), doc["card_count"])
diff = sorted(set(scope) - covered)
assert diff == [] == doc["gap"], diff
assert not covered - set(scope), covered - set(scope)

pack_metrics = {}
for s in pack["srs"]:
    for m in s.get("metrics") or []:
        pack_metrics.setdefault(m["metric_id"], set()).add(s["excel_row"])

for c in cards:
    iid = c["int_id"]
    kind = iid.split("-")[2]
    n = int(iid.rsplit("-", 1)[-1])
    assert 1400 <= n <= 1499, iid
    assert re.fullmatch(r"INT-A-(TAL|TECH|ORG|X)-14\d\d", iid), iid
    assert "skeleton" not in c, iid
    assert c["layer"] == "page", iid
    assert c["srs"]["path"] == scope[c["srs"]["excel_row"]], iid
    assert c["page_ref"] == "DS-16-TALENT-RECRUIT", iid
    assert re.fullmatch(r"IP-(0[1-9]|1[0-3])", c["integration_pattern"]), iid
    assert c["contract_draft"]["freshness"] in ("realtime", "T+1", "weekly", "offline", "unknown"), iid
    assert c["delivery_form"] in ("API", "SQL", "Python", "table", "file", "none", "unknown"), iid
    assert c["algorithm_type"] in ("third_party", "UNKNOWN", "n/a_ops", "STAT"), iid
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
    blob = yaml.safe_dump(c, allow_unicode=True)
    assert "TBD" not in blob and "skeleton" not in blob, iid

by_row = {c["srs"]["excel_row"]: c for c in cards}
for mid, rows in pack_metrics.items():
    for row in rows:
        assert mid in by_row[row]["metric_ids"], (row, mid)
mapped = {m["metric_id"]: m for m in pack["b01_mapping"]}
for mid in nosource:
    assert mapped[mid]["pattern"] == "IP-10" and mapped[mid]["jiuxin_row_id"] is None
for c in cards:
    mids = set(c["metric_ids"])
    if mids & nosource:
        assert c["integration_pattern"] == "IP-10", c["int_id"]
        assert c["jiuxin_row_id"] is None and c["counterpart"] == "none", c["int_id"]
        text = " ".join(str(x) for x in c["gaps"]) + " " + " ".join(c["decision_needed"])
        assert "待定" in text, c["int_id"]

assert by_row[319]["integration_pattern"] == "IP-10"
assert by_row[319]["jiuxin_row_id"] is None
assert doc["cost_collection_verdict"]["source_class"] == "无源"
assert doc["cost_collection_verdict"]["pattern"] == "IP-10"
assert "DN-A15-COST" in doc["cost_collection_verdict"]["conclusion"] or any(
    d["id"] == "DN-A15-COST" for d in doc["decision_needed"]
)
assert "P0-1" in doc["talent_key_verdict"]["ref"]
assert doc["ds16_nosource_verdict"]["owner"] == "待定"
assert doc["ds16_nosource_verdict"]["pattern"] == "IP-10"
assert set(doc["ds16_nosource_verdict"]["metrics"]) == nosource
assert doc["summary"]["lumen_page"] == "无"
assert doc["summary"]["jiuxin_new_rows_needed"] == 0
assert doc["summary"]["structure_escalation_cards"] == []

ids = [c["int_id"] for c in cards]
assert len(ids) == len(set(ids)), [i for i, n in Counter(ids).items() if n > 1]
assert ids == [f"INT-A-X-{n}" for n in range(1400, 1425)]
by_type = Counter(i.split("-")[2] for i in ids)
assert dict(by_type) == doc["summary"]["cards_by_type"], by_type
mm = sorted(c["int_id"] for c in cards if any(str(g).startswith("metric_missing") for g in c["gaps"]))
assert mm == sorted(doc["summary"]["metric_missing_cards"]), mm
se = sorted(c["int_id"] for c in cards if c["structure_escalation"])
assert se == sorted(doc["summary"]["structure_escalation_cards"]), se
jx = sorted({c["jiuxin_row_id"] for c in cards if c["jiuxin_row_id"]})
assert jx == sorted(doc["summary"]["jiuxin_rows_referenced"]), jx
assert jx == ["SRS-110", "SRS-160", "SRS-164"]
assign = doc["summary"]["page_metrics_assignment"]
for mid, rows in pack_metrics.items():
    assert mid in assign and rows <= set(assign[mid]), (mid, rows, assign.get(mid))
assert set(assign) == set(pack_metrics)

print(f"scope_count={len(scope)} covered_rows={len(covered)} diff={diff}")
print("cards:", len(cards), dict(by_type))
print("jiuxin_rows:", jx)
print("metric_missing:", len(mm), mm)
print("structure_escalation:", len(se), se)
print("patterns:", dict(sorted(Counter(c["integration_pattern"] for c in cards).items())))
print("OK")

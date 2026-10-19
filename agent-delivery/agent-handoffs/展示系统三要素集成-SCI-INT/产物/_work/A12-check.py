"""SCI-INT-A12 自检：SRS 覆盖差集、int_id 号段 1100–1122、IP 编号、三要素调用链、久新行、华人占比/迁徙结论。"""
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent.parent
p00 = yaml.safe_load((HERE / "P00-baseline.yaml").read_text(encoding="utf-8"))
pack = yaml.safe_load((HERE / "_prep" / "A12-pack.yaml").read_text(encoding="utf-8"))
doc = yaml.safe_load((HERE / "SCI-INT-A12.yaml").read_text(encoding="utf-8"))
cards = doc["cards"]

scope = {l["excel_row"]: l["path"] for l in p00["srs_leaves"] if l["leaf"] == "A12"}
jiuxin_ids = {r["row_id"] for r in p00["jiuxin_rows"]}
covered = {c["srs"]["excel_row"] for c in cards}
three_e = {"TAL", "TECH", "ORG"}

assert sorted(scope) == list(range(246, 269)), sorted(scope)
assert len(scope) == doc["scope_count"] == 23, len(scope)
assert len(cards) == doc["card_count"] == 23, (len(cards), doc["card_count"])
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
    assert 1100 <= n <= 1199, iid
    assert re.fullmatch(r"INT-A-(TAL|TECH|ORG|X)-11\d\d", iid), iid
    assert c["layer"] == "page", iid
    assert c["srs"]["path"] == scope[c["srs"]["excel_row"]], iid
    assert c["page_ref"] == "DS-13-TALENT-GLOBAL", iid
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
            or any(g.startswith("metric_missing") for g in c["gaps"]) \
            or c["algorithm_type"] in ("other_system", "n/a_ops"), iid
    chain = " ".join(str(v) for v in c["call_chain"].values() if v)
    assert not re.search(r"demo[-_]", chain), iid

by_row = {c["srs"]["excel_row"]: c for c in cards}
assert by_row[251]["integration_pattern"] == "IP-10"
assert by_row[251]["jiuxin_row_id"] is None
assert doc["chinese_share_verdict"]["source_class"] == "无源"
assert "IP-10" in doc["chinese_share_verdict"]["conclusion"]
assert by_row[249]["integration_pattern"] == "IP-08"
assert by_row[249]["jiuxin_row_id"] == "SRS-157"
assert by_row[255]["jiuxin_row_id"] == "SRS-157"
assert doc["migration_verdict"]["source_class"] == "久新"
assert "API-157" in doc["migration_verdict"]["conclusion"]
assert doc["a11_overlap"]["excel_row"] == 185
assert doc["a11_overlap"]["a11_yaml"] == "无"
assert doc["summary"]["lumen_page"] == "无"

ids = [c["int_id"] for c in cards]
assert len(ids) == len(set(ids)), [i for i, n in Counter(ids).items() if n > 1]
assert ids == [f"INT-A-TAL-{n}" for n in range(1100, 1123)]
by_type = Counter(i.split("-")[2] for i in ids)
assert dict(by_type) == doc["summary"]["cards_by_type"], by_type
mm = sorted(c["int_id"] for c in cards if any(g.startswith("metric_missing") for g in c["gaps"]))
assert mm == sorted(doc["summary"]["metric_missing_cards"]), mm
se = sorted(c["int_id"] for c in cards if c["structure_escalation"])
assert se == sorted(doc["summary"]["structure_escalation_cards"]), se
jx = sorted({c["jiuxin_row_id"] for c in cards if c["jiuxin_row_id"]})
assert jx == sorted(doc["summary"]["jiuxin_rows_referenced"]), jx
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

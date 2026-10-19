"""SCI-INT-A13 自检：scope=11、excel 269–279 全覆盖、卡号 1200–1299、无 TBD、无 skeleton。"""
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent.parent
raw = (HERE / "SCI-INT-A13.yaml").read_text(encoding="utf-8")
p00 = yaml.safe_load((HERE / "P00-baseline.yaml").read_text(encoding="utf-8"))
pack = yaml.safe_load((HERE / "_prep" / "A13-pack.yaml").read_text(encoding="utf-8"))
doc = yaml.safe_load(raw)
cards = doc["cards"]

assert "TBD" not in raw, "raw still contains TBD"
assert "skeleton" not in raw.lower(), "raw still contains skeleton"
assert "未实现（草案）" not in raw, "placeholder skeleton text remains"

scope = {l["excel_row"]: l["path"] for l in p00["srs_leaves"] if l["leaf"] == "A13"}
jiuxin_ids = {r["row_id"] for r in p00["jiuxin_rows"]}
covered = {c["srs"]["excel_row"] for c in cards}
three_e = {"TAL", "TECH", "ORG"}

assert sorted(scope) == list(range(269, 280)), sorted(scope)
assert len(scope) == doc["scope_count"] == 11, len(scope)
assert len(cards) == doc["card_count"] == 11, (len(cards), doc["card_count"])
diff = sorted(set(scope) - covered)
assert diff == [] == doc["gap"], diff
assert not covered - set(scope), covered - set(scope)

pack_metrics = {}
for s in pack["srs"]:
    for m in s.get("metrics") or []:
        pack_metrics.setdefault(m["metric_id"], set()).add(s["excel_row"])
mapped = {m["metric_id"]: m for m in pack["b01_mapping"]}

for c in cards:
    iid = c["int_id"]
    kind = iid.split("-")[2]
    n = int(iid.rsplit("-", 1)[-1])
    assert 1200 <= n <= 1299, iid
    assert re.fullmatch(r"INT-A-(TAL|TECH|ORG|X)-12\d\d", iid), iid
    assert "skeleton" not in c, iid
    assert c["layer"] == "page", iid
    assert c["srs"]["path"] == scope[c["srs"]["excel_row"]], iid
    assert c["page_ref"] == "DS-14-TALENT-REGION", iid
    assert re.fullmatch(r"IP-(0[1-9]|1[0-3])", c["integration_pattern"]), iid
    assert c["contract_draft"]["freshness"] in ("realtime", "T+1", "weekly", "offline", "unknown"), iid
    assert c["delivery_form"] in ("API", "SQL", "Python", "table", "file", "none", "unknown"), iid
    assert c["algorithm_type"] in ("third_party", "UNKNOWN", "n/a_ops", "STAT"), iid
    assert c["contract_draft"]["request"], iid
    assert c["contract_draft"]["response_key_fields"], iid
    if kind != "X":
        assert c["dimension"] == [kind], iid
    if c["jiuxin_row_id"]:
        assert c["jiuxin_row_id"] in jiuxin_ids and c["counterpart"] == "jiuxin", iid
    if c["metric_ids"]:
        assert c["algorithm_type"] == "third_party", iid
    if three_e & set(c["dimension"]):
        assert all(c["call_chain"][k] for k in ("java", "python", "downstream")), iid
        assert c["metric_ids"] or c["metric_domain_other"] \
            or any(str(g).startswith("metric_missing") for g in c["gaps"]) \
            or c["algorithm_type"] in ("other_system", "n/a_ops"), iid
    else:
        assert c["metric_ids"] or any(str(g).startswith("metric_missing") for g in c["gaps"]) \
            or c["algorithm_type"] == "n/a_ops", iid
    chain = " ".join(str(v) for v in c["call_chain"].values() if v)
    assert not re.search(r"demo[-_]", chain), iid
    blob = yaml.safe_dump(c, allow_unicode=True)
    assert "TBD" not in blob and "skeleton" not in blob.lower(), iid
    assert "未实现（草案）" not in blob, iid

by_row = {c["srs"]["excel_row"]: c for c in cards}
for mid, rows in pack_metrics.items():
    meta = mapped[mid]
    for row in rows:
        c = by_row[row]
        assert mid in c["metric_ids"], (row, mid)
        assert c["integration_pattern"] == meta["pattern"], (c["int_id"], mid)
        assert c["jiuxin_row_id"] == meta["jiuxin_row_id"], (c["int_id"], mid)

cn = doc["china_map_verdict"]
assert cn["excel_row"] == 269 and cn["int_id"] == "INT-A-X-1200"
assert cn["basemap"] == "未核实"
assert "SQL-98" in cn["conclusion"]
assert by_row[269]["metric_ids"] == ["M_TALENT_BASE_98_1"]
assert by_row[269]["integration_pattern"] == "IP-06"
assert by_row[269]["jiuxin_row_id"] == "SRS-98"
assert by_row[269]["call_chain"]["fe_route"] is None
assert any(str(g).startswith("metric_missing") for g in by_row[269]["gaps"])

sz = doc["shenzhen_map_verdict"]
assert sz["excel_row"] == 274 and sz["int_id"] == "INT-A-X-1205"
assert sz["basemap"] == "未核实"
assert sz["structure_escalation"] == "INT-A-X-1205"
assert "未核实" in sz["conclusion"]
assert by_row[274]["structure_escalation"] is True
assert by_row[274]["integration_pattern"] == "IP-06"
assert by_row[274]["jiuxin_row_id"] == "SRS-98"

ex = doc["report_export_verdict"]
assert ex["excel_row"] == 279 and ex["int_id"] == "INT-A-X-1210"
assert ex["jiuxin_new_row"] is False
assert ex["pattern"] == "IP-10"
assert "未核实" in ex["conclusion"]
assert by_row[279]["integration_pattern"] == "IP-10"
assert by_row[279]["jiuxin_row_id"] is None
assert "export" in by_row[279]["dep_kind"]
assert any(str(g).startswith("metric_missing") for g in by_row[279]["gaps"])

assert by_row[270]["integration_pattern"] == "IP-08"
assert by_row[270]["jiuxin_row_id"] == "SRS-157"
assert by_row[270]["metric_ids"] == ["M_TALENT_DEEP_157_1"]

ids = [c["int_id"] for c in cards]
assert len(ids) == len(set(ids)), [i for i, n in Counter(ids).items() if n > 1]
assert ids == [f"INT-A-X-{n}" for n in range(1200, 1211)]
by_type = Counter(i.split("-")[2] for i in ids)
assert dict(by_type) == doc["summary"]["cards_by_type"], by_type
mm = sorted(c["int_id"] for c in cards if any(str(g).startswith("metric_missing") for g in c["gaps"]))
assert mm == [
    "INT-A-X-1200",
    "INT-A-X-1202",
    "INT-A-X-1204",
    "INT-A-X-1206",
    "INT-A-X-1209",
    "INT-A-X-1210",
], mm
assert mm == sorted(doc["summary"]["metric_missing_cards"]), mm
se = sorted(c["int_id"] for c in cards if c["structure_escalation"])
assert se == ["INT-A-X-1205"], se
assert se == sorted(doc["summary"]["structure_escalation_cards"]), se
jx = sorted({c["jiuxin_row_id"] for c in cards if c["jiuxin_row_id"]})
assert jx == ["SRS-157", "SRS-98"], jx
assert jx == sorted(doc["summary"]["jiuxin_rows_referenced"]), jx
assert doc["summary"]["jiuxin_new_rows_needed"] == 0
assert doc["summary"]["lumen_page"] == "未核实"
assert doc["summary"]["demo_page"] == "未核实"
assign = doc["summary"]["page_metrics_assignment"]
for mid, rows in pack_metrics.items():
    assert mid in assign and rows <= set(assign[mid]), (mid, rows, assign.get(mid))
assert set(assign) == set(pack_metrics) | {"M_TALENT_BASE_98_1"}

print(f"scope_count={len(scope)} covered_rows={len(covered)} diff={diff}")
print("cards:", len(cards), dict(by_type))
print("jiuxin_rows:", jx)
print("metric_missing:", len(mm), mm)
print("structure_escalation:", len(se), se)
print("patterns:", dict(sorted(Counter(c["integration_pattern"] for c in cards).items())))
print("OK")

"""SCI-INT-A14 自检：28 叶、excel 280–307、卡号 1300–1399、无 TBD、无 skeleton。"""
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent.parent
raw = (HERE / "SCI-INT-A14.yaml").read_text(encoding="utf-8")
p00 = yaml.safe_load((HERE / "P00-baseline.yaml").read_text(encoding="utf-8"))
pack = yaml.safe_load((HERE / "_prep" / "A14-pack.yaml").read_text(encoding="utf-8"))
cindex = (HERE / "_prep" / "C-index.yaml").read_text(encoding="utf-8")
doc = yaml.safe_load(raw)
cards = doc["cards"]

assert "TBD" not in raw, "raw still contains TBD"
assert "skeleton" not in raw, "raw still contains skeleton"
assert "note" not in doc, "file note must be removed"

scope = {l["excel_row"]: l["path"] for l in p00["srs_leaves"] if l["leaf"] == "A14"}
jiuxin_ids = {r["row_id"] for r in p00["jiuxin_rows"]}
covered = {c["srs"]["excel_row"] for c in cards}
three_e = {"TAL", "TECH", "ORG"}

assert sorted(scope) == list(range(280, 308)), sorted(scope)
assert len(scope) == doc["scope_count"] == 28, len(scope)
assert len(cards) == doc["card_count"] == 28, (len(cards), doc["card_count"])
diff = sorted(set(scope) - covered)
assert diff == [] == doc["gap"], diff
assert not covered - set(scope), covered - set(scope)

assert "talent_coop" not in cindex, "C-index unexpectedly names talent_coop"
assert not re.search(r"(?m)^\s*name:\s*talent\s*$", cindex), "C-index has a tag named talent"

pack_metrics = {}
for s in pack["srs"]:
    for m in s.get("metrics") or []:
        pack_metrics.setdefault(m["metric_id"], set()).add(s["excel_row"])

for c in cards:
    iid = c["int_id"]
    kind = iid.split("-")[2]
    n = int(iid.rsplit("-", 1)[-1])
    assert 1300 <= n <= 1399, iid
    assert re.fullmatch(r"INT-A-(TAL|TECH|ORG|X)-13\d\d", iid), iid
    assert "skeleton" not in c, iid
    assert c["layer"] == "page", iid
    assert c["srs"]["path"] == scope[c["srs"]["excel_row"]], iid
    assert c["page_ref"] == "DS-15-TALENT-PROFILE", iid
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
    assert "nGQL" not in str(c["call_chain"]["java"]) or "不写 nGQL" in str(c["call_chain"]["java"]), iid
    blob = yaml.safe_dump(c, allow_unicode=True)
    assert "TBD" not in blob and "skeleton" not in blob, iid
    assert "C01-P0-1" in c["decision_needed"], iid

by_row = {c["srs"]["excel_row"]: c for c in cards}
for mid, rows in pack_metrics.items():
    for row in rows:
        assert mid in by_row[row]["metric_ids"], (row, mid)
mapped = {m["metric_id"]: m for m in pack["b01_mapping"]}
for mid, meta in mapped.items():
    for c in cards:
        if mid in c["metric_ids"]:
            assert c["integration_pattern"] == meta["pattern"], (c["int_id"], mid)
            assert c["jiuxin_row_id"] == meta["jiuxin_row_id"], (c["int_id"], mid)

assert by_row[280]["integration_pattern"] == "IP-10"
assert by_row[280]["metric_ids"] == []
assert "人才主键未定（C01）" in doc["talent_key_verdict"]["conclusion"]
assert "P0-1" in doc["talent_key_verdict"]["ref"]
assert doc["privacy_verdict"]["status"] == "decision_needed"
assert doc["privacy_verdict"]["id"] == "DN-A14-PRIVACY"
assert "不替甲方" in doc["privacy_verdict"]["conclusion"]
assert "写回走 ADS 人工层再投影，不直接写 Nebula（A03/C04）" in doc["writeback_verdict"]["conclusion"]
assert doc["writeback_verdict"]["escalation"] == "human:李伟"
assert by_row[282]["structure_escalation"] is True
assert "不直接写 Nebula" in by_row[282]["call_chain"]["downstream"]
assert "DS-08-VIZ-001" in doc["hindex_verdict"]["conclusion"]
assert "DS-08-VIZ-004" in doc["hindex_verdict"]["conclusion"]
assert "只引用" in doc["hindex_verdict"]["conclusion"]
for c in cards:
    assert "M_INNOV_EXPERT_HINDEX" not in c["metric_ids"], c["int_id"]
    assert "M_INNOV_EXPERT_ACTIVITY" not in c["metric_ids"], c["int_id"]
assert doc["hindex_verdict"]["jiuxin_row_id"] == ["DS-08-VIZ-001", "DS-08-VIZ-004"]
assert doc["graph_verdict"]["c_index_hit"]["talent_coop"] is False
assert doc["graph_verdict"]["escalation"] == "human:李伟"
assert set(doc["graph_verdict"]["names"]) == {"talent", "talent_coop"}
for iid in doc["summary"]["structure_escalation_cards"]:
    if iid == "INT-A-X-1302":
        continue
    text = yaml.safe_dump(by_row[int(iid.rsplit("-", 1)[-1]) - 1300 + 280], allow_unicode=True)
    assert "talent" in text, iid
assert doc["summary"]["lumen_page"] == "无"
assert doc["summary"]["jiuxin_new_rows_needed"] == 0
assert "DN-A14-PRIVACY" in {d["id"] for d in doc["decision_needed"]}

ids = [c["int_id"] for c in cards]
assert len(ids) == len(set(ids)), [i for i, n in Counter(ids).items() if n > 1]
assert ids == [f"INT-A-X-{n}" for n in range(1300, 1328)]
by_type = Counter(i.split("-")[2] for i in ids)
assert dict(by_type) == doc["summary"]["cards_by_type"], by_type
mm = sorted(c["int_id"] for c in cards if any(str(g).startswith("metric_missing") for g in c["gaps"]))
assert mm == sorted(doc["summary"]["metric_missing_cards"]), mm
se = sorted(c["int_id"] for c in cards if c["structure_escalation"])
assert se == sorted(doc["summary"]["structure_escalation_cards"]), se
jx = sorted({c["jiuxin_row_id"] for c in cards if c["jiuxin_row_id"]})
assert jx == sorted(doc["summary"]["jiuxin_rows_referenced"]), jx
assert jx == ["SRS-110", "SRS-160", "SRS-162"]
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

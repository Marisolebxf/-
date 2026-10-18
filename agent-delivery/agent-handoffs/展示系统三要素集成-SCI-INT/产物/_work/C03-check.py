# -*- coding: utf-8 -*-
"""SCI-INT-C03 自检：对照 P00-baseline 校验 ORG 指标覆盖差集、源卡编号、久新科研机构行挂接。
运行：python 产物/_work/C03-check.py
"""
import pathlib
import re
import yaml

BASE = pathlib.Path(__file__).resolve().parent.parent
doc = yaml.safe_load((BASE / "SCI-INT-C03.yaml").read_text(encoding="utf-8"))
p00 = yaml.safe_load((BASE / "P00-baseline.yaml").read_text(encoding="utf-8"))

org = {m["metric_id"] for m in p00["metrics"] if m["domain"] == "ORG"}
assert len(org) == 22, len(org)
jx_org = {r["row_id"] for r in p00["jiuxin_rows"] if r["维度"] == "科研机构"}

cards = doc["cards"]
ids = [c["int_id"] for c in cards]
assert len(ids) == len(set(ids)), "int_id 重复"
for i in ids:
    m = re.fullmatch(r"INT-C-ORG-(\d{3})", i)
    assert m and 200 <= int(m.group(1)) <= 299, i
assert doc["scope_count"] == doc["card_count"] == len(cards), "scope/card 计数不一致"
assert doc["gap"] == [], doc["gap"]
for c in cards:
    assert c["layer"] == "data", c["int_id"]
    ds = c["data_source"]
    for k in ("source_system", "table", "key_fields", "primary_key", "entity_align_key", "coverage", "update_freq", "rows"):
        assert ds.get(k) not in (None, "", []), (c["int_id"], k)
    assert ds["rows"]["ref"], c["int_id"]
    assert c["metric_ids"], f"{c['int_id']} 未挂任何指标"

items = doc["metric_coverage"]["items"]
cov = {it["metric_id"]: it for it in items}
assert len(cov) == len(items), "metric_coverage 重复"
diff_missing, diff_extra = org - set(cov), set(cov) - org
assert not diff_missing and not diff_extra, (diff_missing, diff_extra)
assert doc["metric_coverage"]["diff"] == []
id_set = set(ids)
no_source = []
for m, it in cov.items():
    if it["source_cards"] == "no_source":
        assert it["binding"] == "no_source" and it["note"], m
        no_source.append(m)
    else:
        assert it["source_cards"] and set(it["source_cards"]) <= id_set, (m, set(it["source_cards"]) - id_set)
for c in cards:
    for m in c["metric_ids"]:
        assert m in org and c["int_id"] in cov[m]["source_cards"], (c["int_id"], m)
assert doc["metric_coverage"]["no_source"] == len(no_source)

linked_jx = {r for c in cards for r in (c["jiuxin_row_id"] or [])}
assert jx_org == linked_jx, (jx_org ^ linked_jx)
for c in cards:
    if c["counterpart"] == "jiuxin":
        assert any("待确认" in g for g in c["gaps"]), c["int_id"]
    if c["counterpart"] == "none":
        assert c["structure_escalation"], c["int_id"]

for k in ("conclusion", "status", "carrier_vs_org"):
    assert doc["master_data_conclusion"].get(k), k
assert doc["id_alignment_draft"]["org_uid"]["grid_ror"].startswith("unknown")

esc = sum(1 for c in cards if c["structure_escalation"])
by_cp = {}
for c in cards:
    by_cp[c["counterpart"]] = by_cp.get(c["counterpart"], 0) + 1
print(f"OK cards={len(cards)} gap=0 by_counterpart={by_cp}")
print(f"OK ORG metrics scope=22 covered={22 - len(no_source)} no_source={len(no_source)} {no_source} diff=0")
print(f"OK jiuxin 科研机构行={len(jx_org)} 全部挂卡 diff=0 · structure_escalation={esc} · open_items={len(doc['open_items'])}")

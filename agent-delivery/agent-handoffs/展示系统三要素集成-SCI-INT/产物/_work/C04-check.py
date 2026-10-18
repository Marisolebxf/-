# -*- coding: utf-8 -*-
"""SCI-INT-C04 自检：卡数/ID 区间、图指标覆盖差集（集合由 B01 initial_mapping 规则现算）、源卡/页面卡挂接、结构升级。
运行：python 产物/_work/C04-check.py
"""
import pathlib
import re
import sys

import yaml

sys.stdout.reconfigure(encoding="utf-8")
BASE = pathlib.Path(__file__).resolve().parent.parent


def load(name):
    return yaml.safe_load((BASE / name).read_text(encoding="utf-8"))


doc = load("SCI-INT-C04.yaml")
b01 = load("SCI-INT-B01.yaml")
p00 = load("P00-baseline.yaml")

GRAPH_ROWS = {f"SRS-{i}" for i in (104, 105, 110, 111, 114, 115, 130, 131, 153, 157, 160)}
graph_metrics = {m["metric_id"] for m in b01["initial_mapping"]
                 if m["pattern"] == "IP-05" or m["jiuxin_row_id"] in GRAPH_ROWS}

cards = doc["cards"]
ids = [c["int_id"] for c in cards]
id_set = set(ids)
assert len(ids) == len(id_set), "int_id 重复"
for i in ids:
    m = re.fullmatch(r"INT-C-(TAL|TECH|ORG|X)-(\d{3})", i)
    assert m and 300 <= int(m.group(2)) <= 399, i
assert doc["scope_count"] == doc["card_count"] == len(cards), "scope/card 计数不一致"
assert doc["gap"] == [], doc["gap"]

src_ids = {c["int_id"] for leaf in ("SCI-INT-C01.yaml", "SCI-INT-C02.yaml", "SCI-INT-C03.yaml") for c in load(leaf)["cards"]}
page_ids = {c["int_id"] for leaf in ("SCI-INT-A01.yaml", "SCI-INT-A02.yaml") for c in load(leaf)["cards"]}
jx_ids = {r["row_id"] for r in p00["jiuxin_rows"]}
ev_keys = set(doc["evidence_index"])
STATUSES = {"existing", "existing_alter", "planned_not_built", "missing"}
VID_PREFIX = re.compile(r"(tech|talent|inst|ent):")

for c in cards:
    g = c["graph"]
    assert c["layer"] == "data" and g["kind"] in ("TAG", "EDGE") and g["name"], c["int_id"]
    for k in ("props_draft", "vid_rule", "vid_align"):
        assert g.get(k), (c["int_id"], k)
    assert VID_PREFIX.search(g["vid_rule"]), (c["int_id"], g["vid_rule"])
    assert "{名称}" not in g["vid_rule"] and "name}" not in g["vid_rule"], c["int_id"]
    ex = c["existence"]
    assert ex["status"] in STATUSES and ex["note"], c["int_id"]
    assert ex["evidence"] and set(ex["evidence"]) <= ev_keys, (c["int_id"], set(ex["evidence"]) - ev_keys)
    assert c["structure_escalation"] == (ex["status"] != "existing"), c["int_id"]
    ds = c["data_source"]
    assert set(ds["source_cards"]) <= src_ids, (c["int_id"], set(ds["source_cards"]) - src_ids)
    assert ds["source_cards"] or ds.get("source_note"), c["int_id"]
    assert set(ds["jiuxin_rows"]) <= jx_ids, (c["int_id"], set(ds["jiuxin_rows"]) - jx_ids)
    if ds["jiuxin_rows"]:
        assert any("待确认" in x for x in c["gaps"]), f"{c['int_id']} 久新行未标待确认"
    for k in ("who", "freq", "mode"):
        assert c["writer"].get(k), (c["int_id"], k)
    cons = c["consumers"]
    assert set(cons["page_cards"]) <= page_ids, (c["int_id"], set(cons["page_cards"]) - page_ids)
    assert cons["page_cards"] or cons["page_cards_unknown"], c["int_id"]

items = doc["graph_metric_coverage"]["items"]
cov = {it["metric_id"]: it for it in items}
assert len(cov) == len(items), "coverage 重复"
missing, extra = graph_metrics - set(cov), set(cov) - graph_metrics
assert not missing and not extra, (missing, extra)
assert doc["graph_metric_coverage"]["diff"] == []
assert doc["graph_metric_coverage"]["scope"] == doc["graph_metric_coverage"]["covered"] == len(graph_metrics)
for m, it in cov.items():
    assert it["cards"] and set(it["cards"]) <= id_set, (m, set(it["cards"]) - id_set)
for c in cards:
    derived = sorted(m for m, it in cov.items() if c["int_id"] in it["cards"])
    assert sorted(c["metric_ids"]) == derived, (c["int_id"], set(c["metric_ids"]) ^ set(derived))

wb_ids = {w["id"] for w in doc["write_back_conflicts"]["items"]}
cf_ids = {x["id"] for x in doc["conflicts"]}
for w in doc["write_back_conflicts"]["items"]:
    assert set(w["cards"]) <= id_set and w["decision_needed"], w["id"]
for c in cards:
    assert set(c["conflicts"]) <= wb_ids | cf_ids, (c["int_id"], set(c["conflicts"]) - wb_ids - cf_ids)

sp = doc["space_plan"]
assert sp["demo_space"] == "demo_gkx_chain" and sp["structure_escalation"] is True
assert {"entan", "demo_entan"} <= set(sp["forbidden_spaces"])
assert doc["structure_escalation"] == sum(c["structure_escalation"] for c in cards)

by_status, by_kind = {}, {}
for c in cards:
    by_status[c["existence"]["status"]] = by_status.get(c["existence"]["status"], 0) + 1
    by_kind[c["graph"]["kind"]] = by_kind.get(c["graph"]["kind"], 0) + 1
print(f"OK cards={len(cards)} gap=0 by_kind={by_kind} by_status={by_status}")
print(f"OK graph metrics (B01 rule) scope={len(graph_metrics)} covered={len(cov)} diff=0")
print(f"OK structure_escalation={doc['structure_escalation']} write_back_conflicts={len(wb_ids)} conflicts={len(cf_ids)} open_items={len(doc['open_items'])}")

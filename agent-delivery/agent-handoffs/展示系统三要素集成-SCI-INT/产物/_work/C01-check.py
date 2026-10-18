# -*- coding: utf-8 -*-
"""SCI-INT-C01 自检：对照 P00-baseline 校验 TALENT 指标覆盖差集、源卡编号、久新人才行挂接。
运行：python 产物/_work/C01-check.py
"""
import pathlib
import re
import yaml

BASE = pathlib.Path(__file__).resolve().parent.parent
doc = yaml.safe_load((BASE / "SCI-INT-C01.yaml").read_text(encoding="utf-8"))
p00 = yaml.safe_load((BASE / "P00-baseline.yaml").read_text(encoding="utf-8"))

tal = {m["metric_id"] for m in p00["metrics"] if m["domain"] == "TALENT"}
assert len(tal) == 32, len(tal)
jx_tal = {r["row_id"] for r in p00["jiuxin_rows"] if r["维度"] == "人才"}

cards = doc["cards"]
ids = [c["int_id"] for c in cards]
assert len(ids) == len(set(ids)), "int_id 重复"
for i in ids:
    m = re.fullmatch(r"INT-C-TAL-(\d{3})", i)
    assert m and 1 <= int(m.group(1)) <= 99, i
assert doc["scope_count"] == doc["card_count"] == len(cards), "scope/card 计数不一致"
assert doc["gap"] == [], doc["gap"]
for k in ("master_data_conclusion", "id_alignment_draft", "metric_coverage", "open_items"):
    assert doc.get(k), k
for c in cards:
    assert c["layer"] == "data", c["int_id"]
    ds = c["data_source"]
    for k in ("source_system", "table", "key_fields", "primary_key", "entity_align_key", "coverage", "update_freq", "rows"):
        assert ds.get(k) not in (None, "", []), (c["int_id"], k)
    assert ds["rows"]["ref"], c["int_id"]

items = doc["metric_coverage"]["items"]
cov = {it["metric_id"]: it for it in items}
assert len(cov) == len(items), "metric_coverage 重复"
diff_missing, diff_extra = tal - set(cov), set(cov) - tal
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
        assert m in tal and c["int_id"] in cov[m]["source_cards"], (c["int_id"], m)
assert doc["metric_coverage"]["no_source"] == len(no_source)
assert doc["metric_coverage"]["covered"] + len(no_source) == 32

linked_jx = {r for c in cards for r in (c["jiuxin_row_id"] or [])}
assert jx_tal <= linked_jx, jx_tal - linked_jx
assert linked_jx <= jx_tal, linked_jx - jx_tal
for c in cards:
    if c["counterpart"] == "jiuxin":
        assert any("待确认" in g for g in c["gaps"]), c["int_id"]
        assert not any("已确认" in str(v) for v in c.values()), c["int_id"]

esc = sum(1 for c in cards if c["structure_escalation"])
by_cp = {}
for c in cards:
    by_cp[c["counterpart"]] = by_cp.get(c["counterpart"], 0) + 1
print(f"OK cards={len(cards)} gap=0 by_counterpart={by_cp}")
print(f"OK TALENT metrics scope=32 covered={32 - len(no_source)} no_source={len(no_source)} {sorted(no_source)} diff=0")
print(f"OK jiuxin 人才行={len(jx_tal)} 全部挂卡 diff=0 · structure_escalation={esc} · open_items={len(doc['open_items'])}")

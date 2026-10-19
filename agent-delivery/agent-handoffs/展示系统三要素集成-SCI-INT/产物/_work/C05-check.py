# -*- coding: utf-8 -*-
"""SCI-INT-C05 自检：yaml 可解析、ID 区间/唯一、dedup 差集 0（对 C05-collect 现采集）、结构升级、源卡/消费卡/冲突引用存在。
运行：python 产物/_work/C05-check.py
"""
import importlib.util
import pathlib
import re
import sys

import yaml

WORK = pathlib.Path(__file__).resolve().parent
BASE = WORK.parent
spec = importlib.util.spec_from_file_location("collect", WORK / "C05-collect.py")
col = importlib.util.module_from_spec(spec)
sys.argv = [sys.argv[0]]
spec.loader.exec_module(col)
raw_ids = {r["raw_id"] for r in col.collect()}


def load(name):
    return yaml.safe_load((BASE / name).read_text(encoding="utf-8"))


doc = load("SCI-INT-C05.yaml")
cards = doc["cards"]
ids = [c["int_id"] for c in cards]
id_set = set(ids)
assert len(ids) == len(id_set), "int_id 重复"
for i in ids:
    m = re.fullmatch(r"INT-C-(TAL|TECH|ORG|X)-(\d{3})", i)
    assert m and 400 <= int(m.group(2)) <= 499, i
assert doc["card_count"] == len(cards) and doc["gap"] == []

# dedup：每条原始提法恰好一条映射，目标卡存在；差集 0
dm = doc["dedup_map"]
mapped = [d["raw_id"] for d in dm]
assert len(mapped) == len(set(mapped)), "dedup_map 重复 raw_id"
missing, extra = raw_ids - set(mapped), set(mapped) - raw_ids
assert not missing and not extra, (missing, extra)
assert doc["scope_count"] == len(raw_ids)
for d in dm:
    assert d["to"] in id_set and set(d["also"]) <= id_set, d
# 卡上 merged_from 与 dedup_map 互逆
for c in cards:
    assert sorted(c["merged_from"]) == sorted(d["raw_id"] for d in dm if d["to"] == c["int_id"]), c["int_id"]
    assert sorted(c["merged_also"]) == sorted(d["raw_id"] for d in dm if c["int_id"] in d["also"]), c["int_id"]

# 源卡 / 消费卡引用存在
all_ids = {}
for t in col.SRC:
    for c in load(f"{t}.yaml").get("cards", []) or []:
        all_ids[c["int_id"]] = t
pages = set()
for t in col.SRC:
    for c in load(f"{t}.yaml").get("cards", []) or []:
        pr = c.get("page_ref")
        pages |= {pr} if isinstance(pr, str) else set(pr or [])
for c in cards:
    assert c["layer"] == "data", c["int_id"]
    assert set(c["source_cards"]) <= set(all_ids), (c["int_id"], set(c["source_cards"]) - set(all_ids))
    for x in c["consumer_cards"]:
        assert x in all_ids or re.fullmatch(r"DS-\d{2}-[A-Z-]+", x), (c["int_id"], x)
    can = c["canonical"]
    for k in ("kind", "name", "physical", "existence", "fields_draft", "primary_key", "refresh", "writer"):
        assert can.get(k), (c["int_id"], k)
    # 新结构一律升级；存量不改可不升级
    assert c["structure_escalation"] == (can["existence"] != "existing"), c["int_id"]
    if c["structure_escalation"]:
        assert can["escalate_to"] == "human:李伟", c["int_id"]
    # 久新行全部待确认
    if c["counterpart"] == "jiuxin" or c["jiuxin_row_id"]:
        assert any("待确认" in g for g in c["gaps"]), c["int_id"]
    # 低置信预判卡
    if can.get("predicted_for"):
        assert c["confidence"] == "low", c["int_id"]
    # D12：物理位置不得落 demo_*（规范卡只描述正式库）
    assert "demo_" not in can["physical"] or c["int_id"] == "INT-C-X-490", (c["int_id"], can["physical"])

cf_ids = {x["id"] for x in doc["conflicts"]}
for c in cards:
    assert set(c["conflicts"]) <= cf_ids, (c["int_id"], set(c["conflicts"]) - cf_ids)
for x in doc["conflicts"]:
    assert set(x["cards"]) <= id_set and x["suggestion"], x["id"]
for need in ("CF-C05-01", "CF-C05-02", "CF-C05-03"):
    assert need in cf_ids
assert all(x.get("d12") for x in doc["conflicts"] if x["id"] in ("CF-C05-02", "CF-C05-03", "CF-C05-04"))
assert any("Z01" in o["item"] for o in doc["open_items"])
for blk in ("geo_dim_plan", "domain_dim_plan", "jiuxin_result_backflow"):
    assert doc[blk]["structure_escalation"] is True, blk
assert {f["form"] for f in doc["jiuxin_result_backflow"]["by_form"]} == {"SQL", "Python", "API"}
assert all(f["status"] == "待确认" for f in doc["jiuxin_result_backflow"]["by_form"])
assert doc["structure_escalation"] == sum(c["structure_escalation"] for c in cards)

by_kind = {}
for c in cards:
    by_kind[c["canonical"]["kind"]] = by_kind.get(c["canonical"]["kind"], 0) + 1
low = sum(c["confidence"] == "low" for c in cards)
print(f"OK yaml.safe_load; cards={len(cards)} (INT-C-*-400..499 唯一)")
print(f"OK raw mentions={len(raw_ids)} -> canonical={len(cards)}; dedup missing=0 extra=0")
print(f"OK by_kind={by_kind}")
print(f"OK structure_escalation={doc['structure_escalation']} conflicts={len(cf_ids)} risks={len(doc['risks'])} open_items={len(doc['open_items'])} low_conf={low}")

# 供 Z01：本次范围外、已出现的后续叶产物中的 structure_escalation 提法数（信息性，不计入差集）
later = sorted(p.stem for p in BASE.glob("SCI-INT-*.yaml") if p.stem not in col.SRC and p.stem != "SCI-INT-C05")
cnt = {}
for t in later:
    d = load(f"{t}.yaml")
    n = sum(1 for c in d.get("cards", []) or [] if c.get("structure_escalation") is True)
    top = []
    col.walk({k: v for k, v in d.items() if k != "cards"}, "", top)
    cnt[t] = n + len(top)
print(f"INFO 待 Z01 补归并（范围外已出现产物）: {cnt}")

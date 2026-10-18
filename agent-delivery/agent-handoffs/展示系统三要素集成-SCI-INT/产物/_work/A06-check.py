"""SCI-INT-A06 自检：SRS 覆盖差集、int_id 号段、IP 编号、三要素卡调用链、久新行、MCP 类型一致性、D12。"""
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent.parent
p00 = yaml.safe_load((HERE / "P00-baseline.yaml").read_text(encoding="utf-8"))
doc = yaml.safe_load((HERE / "SCI-INT-A06.yaml").read_text(encoding="utf-8"))
cards = doc["cards"]

# MCP user-metric-registry metric-get 2026-10-18（algorithm_type, d1, d4）
MCP = {
    "M_INNOV_DS_04_CARRIER_RANK_001": ("MODEL", "draft", "mock"),
    "M_INNOV_CARRIER_INDEX_GLOBAL": ("MODEL", "draft", "mock"),
    "M_INNOV_DS_04_CARRIER_RANK_002": ("MIXED", "draft", "mock"),
    "M_INNOV_CARRIER_RANK_GLOBAL": ("MIXED", "draft", "mock"),
    "M_INNOV_DS_04_MONITOR_001": ("MODEL", "draft", "mock"),
    "M_INNOV_POINT_DISCOVERY": ("MODEL", "draft", "mock"),
    "M_INNOV_DS_04_MONITOR_002": ("MODEL", "draft", "mock"),
    "M_INNOV_POINT_VALUE": ("MODEL", "draft", "mock"),
    "M_INNOV_CITY_MONITOR_GLOBAL": ("STAT", "draft", "mock"),
    "M_INNOV_CITY_RANK_GLOBAL": ("MIXED", "draft", "mock"),
    "M_INNOV_CITY_BENCHMARK_GLOBAL": ("MIXED", "draft", "mock"),
    "M_INNOV_CITY_FACTOR_GLOBAL": ("MIXED", "draft", "mock"),
    "M_INNOV_CITY_TALENT_INDEX_GLOBAL": ("third_party", "draft", "mock"),
    "M_SYNTH_186_1": ("MIXED", "draft", "mock"),
    "M_SYNTH_187_1": ("MIXED", "draft", "mock"),
}
NO_METRIC_TYPES = {"n/a_ops", "other_system", "UNKNOWN"}
PAGE_OF = {**{r: "DS-04-CARRIER-RANK" for r in range(76, 80)},
           **{r: "DS-04-MONITOR" for r in range(80, 86)},
           **{r: "DS-04-CITY" for r in range(86, 92)}}

scope = {l["excel_row"]: l["path"] for l in p00["srs_leaves"] if l["leaf"] == "A06"}
covered = {c["srs"]["excel_row"] for c in cards}
three_e = {"TAL", "TECH", "ORG"}

assert sorted(scope) == list(range(76, 92)), sorted(scope)
assert len(scope) == doc["scope_count"] == 16, len(scope)
assert len(cards) == doc["card_count"], (len(cards), doc["card_count"])
diff = sorted(set(scope) - covered)
assert diff == [] == doc["gap"], diff
assert not covered - set(scope), covered - set(scope)
for c in cards:
    iid = c["int_id"]
    assert re.fullmatch(r"INT-A-(TAL|TECH|ORG|X)-5\d\d", iid), iid
    dims = set(c["dimension"])
    want = next(iter(dims)) if len(dims) == 1 and dims <= three_e else "X"
    assert iid.split("-")[2] == want, (iid, dims)
    row = c["srs"]["excel_row"]
    assert c["srs"]["path"] == scope[row], iid
    assert c["page_ref"] == PAGE_OF[row], (iid, c["page_ref"])
    assert re.fullmatch(r"IP-(0[1-9]|1[0-3])", c["integration_pattern"]), iid
    assert c["jiuxin_row_id"] is None and c["counterpart"] != "jiuxin", iid  # 页面映射禁挂 99/149/153
    if dims & three_e:
        assert all(c["call_chain"][k] for k in ("fe_route", "java", "python", "downstream")), iid
    assert "demo-" not in c["call_chain"]["java"] + c["call_chain"]["python"], iid  # D12
    if c["metric_ids"]:
        for m in c["metric_ids"]:
            assert m in MCP, (iid, m)
        t, d1, d4 = MCP[c["metric_ids"][0]]
        assert c["algorithm_type"] == t, (iid, c["algorithm_type"], t)
        assert c["status"]["d1_d4"] == {"d1": d1, "d4": d4}, iid
        assert c["metric_domain_other"], iid
    else:
        assert c["algorithm_type"] in NO_METRIC_TYPES, iid
        assert c["status"]["d1_d4"] == {"d1": "n/a", "d4": "n/a"}, iid
        if dims & three_e and "metric" in c["dep_kind"]:
            assert any(g.startswith("metric_missing") for g in c["gaps"]), iid
ids = [c["int_id"] for c in cards]
assert len(ids) == len(set(ids)), [i for i, n in Counter(ids).items() if n > 1]

print(f"scope_count={len(scope)} covered_rows={len(covered)} diff={diff}")
print("cards:", len(cards), dict(Counter(c["int_id"].split("-")[2] for c in cards)))
print("cards_per_row:", dict(sorted(Counter(c["srs"]["excel_row"] for c in cards).items())))
print("jiuxin_cards:", sum(c["counterpart"] == "jiuxin" for c in cards))
print("metric_missing:", sum(any(g.startswith("metric_missing") for g in c["gaps"]) for c in cards))
print("structure_escalation:", [c["int_id"] for c in cards if c["structure_escalation"]])
print("decision_needed:", sum(len(c["decision_needed"]) for c in cards), "open_items:", len(doc["open_items"]))
print("patterns:", dict(sorted(Counter(c["integration_pattern"] for c in cards).items())))
print("OK")

# SCI-INT-B06：总派单 12 个 metric_id 全覆盖、差集 0、卡号 500–599、无 TBD
# 运行：python 产物/_work/B06-check.py（任意 cwd）
import re
from pathlib import Path

import yaml

OUT = Path(__file__).resolve().parent.parent
pack = yaml.safe_load((OUT / "_prep" / "B06-pack.yaml").read_text(encoding="utf-8"))
raw = (OUT / "SCI-INT-B06.yaml").read_text(encoding="utf-8")
doc = yaml.safe_load(raw)

expect = [m["metric_id"] for m in pack["metrics"]]
by_id = {m["metric_id"]: m for m in pack["metrics"]}
cards = doc["cards"]
got = [c["metric_id"] for c in cards]
gap = sorted(set(expect).symmetric_difference(got))

PATH = [
    "M_TECH_PATH_CENTRALITY",
    "M_TECH_PATH_KEYNODE",
    "M_TECH_PATH_PRIORITY",
]
PHRASE = "建议改由我方 Python 与 Nebula 计算"
PARENT_SEQ = {
    "M_TECH_EDGE_STRENGTH": 105,
    "M_TECH_ENTITY_REL": 105,
    "M_TECH_ENTITY_TOP5": 105,
    "M_TECH_GRAPH_STRUCT": 104,
    "M_TECH_REL_STRENGTH": 105,
}


def pages_of(metric_id):
    src = by_id[metric_id]
    pages = []
    for row in src.get("srs_refs_02") or []:
        if row["page"] not in pages:
            pages.append(row["page"])
    for a in pack["a_cards"]:
        if metric_id in (a.get("metric_ids") or []) and a.get("page_ref") not in pages:
            pages.append(a["page_ref"])
    return pages


nums = []
for c in cards:
    m = re.fullmatch(r"INT-B-TECH-(\d+)", c["int_id"])
    if not m:
        raise SystemExit(f"卡号非法: {c['int_id']}")
    n = int(m.group(1))
    if not 500 <= n <= 599:
        raise SystemExit(f"卡号越界: {c['int_id']}")
    nums.append(n)
    src = by_id[c["metric_id"]]
    if c["layer"] != "metric":
        raise SystemExit(f"layer 不是 metric: {c['int_id']}")
    if c["integration_pattern"] != src["b01"]["pattern"]:
        raise SystemExit(f"模式与包不一致: {c['metric_id']}")
    if c["algorithm_type"] != src["b01"]["algorithm_type"]:
        raise SystemExit(f"algorithm_type 被改: {c['metric_id']}")
    if c["jiuxin_row_id"] != src["b01"]["jiuxin_row_id"]:
        raise SystemExit(f"久新行被改: {c['metric_id']}")
    if c["jiuxin_row_id"] and c["integration_pattern"] == "IP-10":
        raise SystemExit(f"有久新行却标了 IP-10: {c['metric_id']}")
    if not c.get("inputs") or not c.get("outputs"):
        raise SystemExit(f"缺输入或输出: {c['metric_id']}")
    if c["execution"] not in ("同步", "异步"):
        raise SystemExit(f"执行方式未写明: {c['metric_id']}")
    if "D12" not in " ".join(c.get("risks") or []):
        raise SystemExit(f"未记 D12: {c['metric_id']}")
    pat = c["integration_pattern"]
    expect_pages = pages_of(c["metric_id"])
    got_pages = c["used_by"]["pages"]
    if not expect_pages:
        if got_pages != "未挂页":
            raise SystemExit(f"未挂页未写明: {c['metric_id']}")
    elif sorted(got_pages) != sorted(expect_pages):
        raise SystemExit(f"页面与包不一致: {c['metric_id']} {got_pages} != {expect_pages}")
    if pat == "IP-09":
        parent = c.get("parent_metric") or {}
        if parent.get("seq") != PARENT_SEQ[c["metric_id"]] or not parent.get("fields"):
            raise SystemExit(f"派生卡缺母指标 seq 或字段: {c['metric_id']}")
        if c["execution"] != "同步":
            raise SystemExit(f"IP-09 应按同步读计: {c['metric_id']}")
    elif pat == "IP-07":
        if c["parent_metric"] is not None:
            raise SystemExit(f"图谱库叶不应写母指标: {c['metric_id']}")
        if c["execution"] != "异步":
            raise SystemExit(f"IP-07 应按异步 Job 计: {c['metric_id']}")
    elif pat == "IP-06":
        if c["parent_metric"] is not None:
            raise SystemExit("基础库叶不应写母指标")
        if c["execution"] != "同步":
            raise SystemExit("IP-06 应按同步读计")
    elif pat == "IP-05":
        if c["parent_metric"] is not None or c["jiuxin_row_id"] is not None:
            raise SystemExit(f"IP-05 不应有久新行或母指标: {c['metric_id']}")
        if c["execution"] != "异步":
            raise SystemExit(f"IP-05 应按批 Job 计异步: {c['metric_id']}")
        if c["integration_pattern"] == "IP-10":
            raise SystemExit(f"图自建被标成无源: {c['metric_id']}")
    else:
        raise SystemExit(f"未预期模式: {pat}")
    if c["metric_id"] in PATH:
        blob = " ".join(c["conflicts"])
        if PHRASE not in blob or "third_party" not in blob:
            raise SystemExit(f"中心度三条缺少建议或改了注册值: {c['metric_id']}")
        if "DN-02" not in " ".join(c["decision_needed"]) or "唐绍祖" not in " ".join(c["decision_needed"]):
            raise SystemExit(f"未登记 DN-02: {c['metric_id']}")
        if "SE-B06-01" not in c["structure_escalation_id"]:
            raise SystemExit(f"中心度卡未挂 SE-B06-01: {c['metric_id']}")

banned = "TB" + "D"
if banned in raw:
    raise SystemExit("yaml 含禁用占位")
for banned_table in ("dwd_technology_master", "ads_technology_master", "dwd_tech_point"):
    if banned_table in raw:
        raise SystemExit(f"另造了技术点主表: {banned_table}")
if "INT-C-TECH-180" not in raw or "不另造" not in raw:
    raise SystemExit("未引用 C02 技术点主数据或不另造声明缺失")

sync = sum(1 for c in cards if c["execution"] == "同步")
async_n = sum(1 for c in cards if c["execution"] == "异步")
assert doc["scope_count"] == doc["card_count"] == len(cards) == len(expect) == 12
assert doc["gap"] == [] and gap == []
assert len(set(got)) == 12 and got == expect
assert nums == list(range(500, 512))
assert doc["execution_count"] == {"sync": sync, "async": async_n} == {"sync": 6, "async": 6}
assert doc["jiuxin_rows"] == ["SRS-96", "SRS-104", "SRS-105"]
assert [e["id"] for e in doc["structure_escalations"]] == ["SE-B06-01"]
assert doc["structure_escalations"][0]["owner"] == "human:李伟"
assert [e["id"] for e in doc["structure_escalation_refs"]][0] == "INT-C-TECH-180"
assert doc["recommendation"]["advice"] == PHRASE
assert doc["recommendation"]["registry_algorithm_type"] == "third_party"

print(f"cards={len(cards)} expect={len(expect)} gap={gap}")
print(f"int_ids={min(nums)}-{max(nums)} unique={len(set(nums))}")
print(f"sync={sync} async={async_n}")
print("jiuxin_rows:", doc["jiuxin_rows"])
print("structure_escalation:", [e["id"] for e in doc["structure_escalations"]])
print("structure_escalation_refs:", [e["id"] for e in doc["structure_escalation_refs"]])
print("OK")

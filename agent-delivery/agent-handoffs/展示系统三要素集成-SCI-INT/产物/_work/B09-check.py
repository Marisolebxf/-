# SCI-INT-B09：总派单 15 个 metric_id 全覆盖、差集 0、卡号 800–899、无 TBD
# 运行：python 产物/_work/B09-check.py（任意 cwd）
import re
from pathlib import Path

import yaml

OUT = Path(__file__).resolve().parent.parent
pack = yaml.safe_load((OUT / "_prep" / "B09-pack.yaml").read_text(encoding="utf-8"))
raw = (OUT / "SCI-INT-B09.yaml").read_text(encoding="utf-8")
doc = yaml.safe_load(raw)

expect = [m["metric_id"] for m in pack["metrics"]]
by_id = {m["metric_id"]: m for m in pack["metrics"]}
cards = doc["cards"]
got = [c["metric_id"] for c in cards]
gap = sorted(set(expect).symmetric_difference(got))

DEEP = [
    "M_ORG_DEEP_149_1",
    "M_ORG_DEEP_150_1",
    "M_ORG_DEEP_151_1",
    "M_ORG_DEEP_152_1",
    "M_ORG_DEEP_153_1",
    "M_ORG_DEEP_154_1",
    "M_ORG_DEEP_155_1",
]
PARENT = {
    "M_ORG_ATTENTION_TREND": ("M_ORG_BASE_99_1", 99),
    "M_ORG_ATTRACT_SCORE": ("M_ORG_DEEP_154_1", 154),
    "M_ORG_COLLAB_CHAIN": ("M_ORG_DEEP_153_1", 153),
    "M_ORG_CULTIVATE_SCORE": ("M_ORG_DEEP_155_1", 155),
    "M_ORG_INDUSTRY_COVER": ("M_ORG_BASE_99_1", 99),
    "M_ORG_NEW_TREND": ("M_ORG_BASE_99_1", 99),
    "M_ORG_SZ_ADVANTAGE": ("M_ORG_DEEP_151_1", 151),
    "M_ORG_SZ_PAINPOINT": ("M_ORG_DEEP_152_1", 152),
    "M_ORG_SZ_STATUS": ("M_ORG_BASE_99_1", 99),
    "M_ORG_TECH_LAYOUT": ("M_ORG_DEEP_149_1", 149),
}
JIUXIN = [
    "SRS-99",
    "SRS-114",
    "SRS-115",
    "SRS-154",
    "SRS-153",
    "SRS-155",
    "SRS-151",
    "SRS-152",
    "SRS-149",
    "TOPIC-RORG-012",
]


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
    m = re.fullmatch(r"INT-B-ORG-(\d+)", c["int_id"])
    if not m:
        raise SystemExit(f"卡号非法: {c['int_id']}")
    n = int(m.group(1))
    if not 800 <= n <= 899:
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
        want_id, want_seq = PARENT[c["metric_id"]]
        if parent.get("metric_id") != want_id or parent.get("seq") != want_seq or not parent.get("fields"):
            raise SystemExit(f"派生卡缺母指标: {c['metric_id']}")
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
    elif pat == "IP-08":
        if c["metric_id"] != "M_ORG_TECH_SCORE":
            raise SystemExit(f"IP-08 只应是技术力: {c['metric_id']}")
        if c["parent_metric"] is not None or c["jiuxin_row_id"] != "TOPIC-RORG-012":
            raise SystemExit("技术力未对上 TOPIC-RORG-012")
        if c["execution"] != "异步":
            raise SystemExit("IP-08 应按页面读快照计异步")
        blob = " ".join(c["conflicts"])
        if "M_SVC_ORG_TECH_SCORE" not in blob or "TOPIC-RORG-012" not in blob:
            raise SystemExit("技术力 conflicts 未写替身或无专叶挂接")
    elif pat == "IP-01":
        if c["metric_id"] != "M_ORG_PERF_QUERY" or c["algorithm_type"] != "STAT":
            raise SystemExit("绩效查询未保持 STAT")
        if c["jiuxin_row_id"] is not None or c["parent_metric"] is not None:
            raise SystemExit("绩效查询不应有久新行或母指标")
        if c["integration_pattern"] == "IP-10" or c["execution"] != "同步":
            raise SystemExit("绩效查询不应标 IP-10，且应按同步读计")
        if "SE-B09-01" not in c["structure_escalation_id"]:
            raise SystemExit("绩效查询未挂 SE-B09-01")
    else:
        raise SystemExit(f"未预期模式: {pat}")

if any(c["metric_id"] in DEEP for c in cards):
    raise SystemExit("重写了 B08 深度模型卡")

banned = "TB" + "D"
if banned in raw:
    raise SystemExit("yaml 含禁用占位")
for banned_table in ("dwd_org_master", "ads_org_master", "dim_org_uid"):
    if banned_table in raw:
        raise SystemExit(f"另造了机构主表: {banned_table}")
if "INT-C-ORG-240" not in raw or "不另造" not in raw or "没有 org_uid" not in raw:
    raise SystemExit("未引用 C03 机构主数据或未声明没有 org_uid")
if "M_SVC_ORG_TECH_SCORE" not in raw:
    raise SystemExit("未登记技术力替身")

sync = sum(1 for c in cards if c["execution"] == "同步")
async_n = sum(1 for c in cards if c["execution"] == "异步")
assert doc["scope_count"] == doc["card_count"] == len(cards) == len(expect) == 15
assert doc["gap"] == [] and gap == []
assert len(set(got)) == 15 and got == expect
assert nums == list(range(800, 815))
assert doc["execution_count"] == {"sync": sync, "async": async_n} == {"sync": 12, "async": 3}
assert doc["jiuxin_rows"] == JIUXIN
assert [e["id"] for e in doc["structure_escalations"]] == ["SE-B09-01"]
assert doc["structure_escalations"][0]["owner"] == "human:李伟"
assert doc["structure_escalation_refs"][0]["id"] == "INT-C-ORG-240"
assert doc["tech_score"]["jiuxin_row_id"] == "TOPIC-RORG-012"
assert doc["tech_score"]["substitute_forbidden"] == "M_SVC_ORG_TECH_SCORE"
assert doc["deep_models_149_155"]["rewrite"] is False
assert doc["org_key"]["new_master_table"] is False

print(f"cards={len(cards)} expect={len(expect)} gap={gap}")
print(f"int_ids={min(nums)}-{max(nums)} unique={len(set(nums))}")
print(f"sync={sync} async={async_n}")
print("jiuxin_rows:", doc["jiuxin_rows"])
print("structure_escalation:", [e["id"] for e in doc["structure_escalations"]])
print("structure_escalation_refs:", [e["id"] for e in doc["structure_escalation_refs"]])
print("OK")

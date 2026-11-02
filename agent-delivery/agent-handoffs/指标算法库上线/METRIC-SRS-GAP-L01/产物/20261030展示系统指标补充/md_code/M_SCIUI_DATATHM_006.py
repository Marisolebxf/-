#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M_SCIUI_DATATHM_006 高价值数据资源占比 — 证据采集脚本（S3-04 L7）
挂载点：repos/demo-ui-science/src/pages/data-resources/components/ResourceAppSubjectList.jsx:93
  （实查：:92-95 价值占比列 valueShare，`${v}%`；mock 源 mockData.js:849-860 resourceAppSubjects 10 行）

口径（派单预警核后）：seq 345 主体清单语境——「价值占比」为主体维价值分摊列（各应用主体占全部
资源价值/调用的份额），派单名「高价值数据资源占比」= 该列在重点用户（isKeyUser=true）主体上的
聚合读数：ΣvalueShare(isKeyUser)。三源无资产价值分级登记面、无主体×资源价值分摊面 → 完全不支持。

证据源（复用共享快照，B8 幂等）：
- code/_snapshots/_lane7_shared_probe_out.json（三库表数 B11 锚：dev 542 / gkx 280 / jiuxin live 212）
- code/_snapshots/_probe_s304_l7_quality_out.json（L7 族探针：value/asset 词族三源命中）
- 本脚本补：valueShare 演示值求和（主体侧聚合核）；dev value 命中 degrade_switch 语义排除登记。
"""
import json, re, os, sys, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_006_out.json")
SNAP_SHARED = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
SNAP_L7 = os.path.join(BASE, "_snapshots", "_probe_s304_l7_quality_out.json")
UI_MOCK = "/Users/samuel_tang/my_project/gkx-lumen/repos/demo-ui-science/src/pages/data-resources/mockData.js"

facts = {"generated": datetime.date.today().strftime("%Y%m%d")}

# ---------- 1) 共享快照复用（B8：不重跑族探针） ----------
shared = json.load(open(SNAP_SHARED))
l7 = json.load(open(SNAP_L7))
facts["snapshot_reuse"] = ["_lane7_shared_probe_out.json", "_probe_s304_l7_quality_out.json"]
facts["dev_table_count"] = shared.get("dev_table_count") or l7.get("dev_table_count")
facts["gkx_table_count"] = shared.get("gkx_table_count") or l7.get("gkx_table_count")
# 久新：活库表数不写死（教训 6）——读 live 复核值并披露快照日
facts["jiuxin_table_count_live"] = l7.get("jiuxin_table_count_live")
facts["jiuxin_status"] = l7.get("jiuxin_status")

# ---------- 2) value 词族命中（快照直引，B5 sorted 已保证） ----------
facts["dev_value_like_tables"] = sorted(l7.get("dev_value_like_tables") or [])
facts["gkx_value_like_tables"] = sorted(l7.get("gkx_value_like_tables") or [])
facts["jiuxin_value_like_tables"] = sorted(l7.get("jiuxin_value_like_tables") or [])

# dev 唯一命中 degrade_switch：降级开关配置表（cfg 库运维开关），语义≠数据资源价值分级 → 语义排除
facts["dev_degrade_switch_semantic"] = (
    "gkxlumenx_cfg.degrade_switch 为服务降级开关配置表（运维开关面），"
    "列结构为开关状态维护，无资源价值/分级字段，语义排除"
)
# 久新唯一命中 value 表：技术商业化价值仿真面（tech_transfer/commercial 域），非数据资源价值分级
facts["jiuxin_value_table_semantic"] = (
    "ads_technology_commercial_value_simulation 为技术成果商业化价值仿真面"
    "（成果转化域，模拟估值），语义≠数据资源资产价值分级，排除"
)

# ---------- 3) UI mock 价值占比演示值（主体侧聚合核） ----------
src = open(UI_MOCK, encoding="utf-8").read()
m = re.search(r"export const resourceAppSubjects = \[(.*?)\];", src, re.S)
rows = []
if m:
    for line in m.group(1).strip().splitlines():
        kv = dict(re.findall(r"(\w+): ('[^']*'|[\d.]+|true|false)", line))
        if kv.get("id"):
            rows.append({
                "id": kv["id"].strip("'"),
                "name": kv.get("name", "").strip("'"),
                "subject_type": kv.get("subjectType", "").strip("'"),
                "value_share": float(kv["valueShare"]) if "valueShare" in kv else None,
                "is_key_user": kv.get("isKeyUser") == "true",
                "call_count": int(kv["callCount"]) if "callCount" in kv else None,
            })
rows = sorted(rows, key=lambda r: r["id"])  # B5
facts["ui_mock_subject_rows"] = len(rows)
facts["ui_mock_value_share_sum_all"] = round(sum(r["value_share"] for r in rows if r["value_share"] is not None), 2)
key_rows = [r for r in rows if r["is_key_user"]]
facts["ui_mock_value_share_sum_key_users"] = round(sum(r["value_share"] for r in key_rows if r["value_share"] is not None), 2)
facts["ui_mock_key_user_count"] = len(key_rows)
facts["ui_mock_value_share_top1"] = {
    "id": rows[0]["id"], "name": rows[0]["name"], "value_share": rows[0]["value_share"]
} if rows else None
# mock 不自洽披露：10 主体份额合计 58.7% ≠ 100%（长尾未列）——演示值特征
facts["ui_mock_disclosure"] = (
    "10 主体 valueShare 合计 58.7%（≠100%，长尾主体未列全）——mock 按头部主体叙事截断，"
    "非全量分摊；『高价值占比』口径在 mock 中即未闭合"
)

# ---------- 4) absence_probe（四件：dev/gkx/jiuxin/doc） ----------
absence_probe = [
    {
        "db": "dev",
        "what": "542 表扫 value/worth/asset_value/high_value 词族",
        "hit": facts["dev_value_like_tables"],
        "verdict": "唯一命中 degrade_switch 为运维降级开关配置面，语义排除；无数据资源价值分级登记表",
    },
    {
        "db": "gkx",
        "what": "280 表扫同词族",
        "hit": [],
        "verdict": "零命中——要素明细库无资产价值面",
    },
    {
        "db": "jiuxin",
        "what": f"live {facts['jiuxin_table_count_live']} 表扫同词族",
        "hit": facts["jiuxin_value_like_tables"],
        "verdict": "唯一命中 commercial_value_simulation 为成果转化仿真面，语义排除",
    },
    {
        "db": "doc",
        "what": "三份需求真源检索『高价值数据资源占比/价值占比/高价值』",
        "hit": [],
        "verdict": "字面零命中；seq 345 原文仅『识别资源价值分布及重点用户』（价值分布=管理意图，无分级口径）；cfg_metric 无条目",
    },
]
facts["absence_probe"] = absence_probe

# ---------- 5) 判档与派生 ----------
derived = [{
    "key": "high_value_data_resource_share",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": (
        "『高价值数据资源占比』需资产价值分级登记面（资源×价值等级×评估依据）+ 主体×资源价值分摊面——"
        "三源零承载：dev value 词族唯一命中 degrade_switch（运维开关，语义排除）、gkx 零命中、"
        "久新唯一命中成果转化仿真面（语义排除）；UI valueShare 为 mock 演示值（10 主体合计 58.7%，"
        "非全量分摊）。指标值 null（B10：口径无定义且零承载，不产出伪值）"
    ),
}]

out = {
    "metric_id": "M_SCIUI_DATATHM_006",
    "metric_name": "高价值数据资源占比",
    "mount": "repos/demo-ui-science/src/pages/data-resources/components/ResourceAppSubjectList.jsx:93（价值占比列 valueShare）",
    "category": "无业务逻辑数值类",
    "srs_seq": "345（总体视窗/资源应用状态/资源应用主体详细列表，excel_row 348）",
    "support_judgment": "完全不支持",
    "base_years_used": [],
    "base_years_missing": ["价值分级登记面与主体×资源价值分摊面三源零承载，无任何年份基期可言"],
    "base_years_note": "完全不支持档：无库内基期；mock valueShare（10 主体合计 58.7%≠100%）为演示值，不构成基期证据",
    "facts": facts,
    "derived": derived,
    "notes": sorted([
        "口径核：派单名『高价值数据资源占比』落位 seq 345 主体清单 valueShare 列——主体维价值分摊，非资产分级统计",
        "语义排除两处：degrade_switch（运维开关）/ commercial_value_simulation（成果转化仿真）——字面 value 命中过列结构语义关后排除",
        "mock 不自洽：10 主体份额合计 58.7%≠100%（长尾截断），演示值不作源",
        "同族先例：M_SCIUI_DATATHM_023（应用主体总数）同表列族零承载在案，本件共用其 mock 画像披露",
    ]),
}
json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("done ->", OUT)

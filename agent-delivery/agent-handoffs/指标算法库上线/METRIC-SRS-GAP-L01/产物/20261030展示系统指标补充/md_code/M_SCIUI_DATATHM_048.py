#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_048 来源机构接入活跃度——三源探针+产物生成（S3-05 L1）。

挂载 OverviewWindow.jsx:626（「来源机构接入活跃度」卡，getSourceActivityOption :128 横条图）。
mock overviewSourceActivity（mockData.js:81-87）：五机构 activity 96/88/76/58/36 + accessCount 1286/1048/836/432/186。
活跃度是「分」制合成评分（0-100）——需要评分模型定义；accessCount 近12个月接入次数——需要台账。
三源：台账词族已排除（042 复用）；本件新探针=dev org/机构维度表的来源标签分布
（gkx 来源标签分布已在 _probe_lane3_s304c 快照——dwd_org_base_info 等 org 来源面复用）。
"""
import json
import os

import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_048_out.json")

d042 = json.load(open(os.path.join(BASE, "M_SCIUI_DATATHM_042_out.json"), encoding="utf-8"))
# 复用 lane3 快照（gkx org 来源标签分布）
snap = json.load(open(os.path.join(BASE, "_snapshots/_probe_lane3_s304c_out.json"), encoding="utf-8"))

conn = pymysql.connect(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
                       charset="utf8mb4", autocommit=True,
                       cursorclass=pymysql.cursors.DictCursor)
org_tables = []
org_type_dist = None
try:
    with conn.cursor() as cur:
        # 本件新探针①：dev org/机构维度面（org/inst 词族，排除 demo）
        cur.execute(
            "SELECT table_schema, table_name FROM information_schema.tables "
            "WHERE table_schema LIKE 'gkxlumenx%%' AND table_schema NOT LIKE '%%demo%%' "
            "AND (table_name LIKE '%%org%%' OR table_name LIKE '%%institution%%') "
            "ORDER BY table_schema, table_name")
        org_tables = [list(r.values()) for r in cur.fetchall()]
        # 本件新探针②：org 主表机构类型分布（dwd_org_base_info 在 gkx；dev 侧查 contact 维度）
        cur.execute(
            "SELECT COUNT(*) c FROM gkxlumenx_dwd.enterprise_base")
        ent_rows = cur.fetchone()["c"]
finally:
    conn.close()

# gkx 来源标签分布（快照复用，B8/B11）：dwd_scholar 全量 gkx_ods 单源；patent/zh_paper 来源列 NULL——
# 供应商库自身无「来源机构」多源标签（与 040 来源结构探针同族结论）
gkx_src_dist = snap["facts"]["gkx"]
snap_keys = sorted(gkx_src_dist.keys())

ui_mock_activity = [
    ["科研机构", 1286, 96, "活跃"],
    ["高等院校", 1048, 88, "活跃"],
    ["企业单位", 836, 76, "活跃"],
    ["政府部门", 432, 58, "一般"],
    ["国际组织", 186, 36, "较低"],
]  # mockData.js:81-87 实抄（B5：按 activity 降序=mock 原序）

facts = {
    "dev_table_total": d042["facts"]["dev_table_total"],
    "gkx_table_count": d042["facts"]["gkx_table_count"],
    "jiuxin_table_count_live": d042["facts"]["jiuxin_table_count_live"],
    "dev_org_inst_table_scan": org_tables,
    "dev_org_table_count": len(org_tables),
    "gkx_snapshot_keys": snap_keys,
    "gkx_source_label_dist_reused_lane3": gkx_src_dist,
    "dev_enterprise_base_rows_reused": ent_rows,
    "ui_mock_source_activity": ui_mock_activity,
    "ui_mock_activity_max": 96,
    "ui_mock_activity_min": 36,
    "ui_mock_access_count_total": sum(r[1] for r in ui_mock_activity),
}

derived = [
    {
        "key": "source_org_access_activity",
        "value": None,
        "numerator": None, "denominator": None,
        "note": "『来源机构接入活跃度』正式口径（活跃度=评分模型输出，mock 为 0-100 分制合成分）需两依赖：评分模型定义+近12个月接入台账——前者需求无定义、后者三源零承载（042 词族排除复用）；按 B10 不写伪指标值"
    },
    {
        "key": "source_org_presence_observed_gkx_org_base",
        "value": 189116,
        "numerator": None, "denominator": None,
        "note": "附带交付（非活跃度）：gkx dwd_org_base_info 189,116 行机构存量面（042 计数复用）——机构维度「存在性」可支撑（可列机构清单/类型分布），但无接入动作维度（活跃度分子）。存量≠活跃：静态名单非动态评分"
    },
]

absence_probe = [
    {
        "probe": "dev 机构维度表 + 接入动作交叉面（org/institution 词族×access 词族）",
        "source": "dev",
        "sql": "information_schema.tables 扫 gkxlumenx_* 非 demo（org/institution 词族，本件新探针）+ 台账词族（042 复用）交叉",
        "hits": len(org_tables),
        "hit_detail": f"org 词族命中 {len(org_tables)} 张（机构维度面存在——dwd 侧 org 表/enterprise 派生），但台账词族 0 张（042 复用）：有「机构是谁」无「机构何时接入多少」——活跃度所需的动作×时间×机构三元组缺两元（动作/时间）",
    },
    {
        "probe": "gkx 来源标签分布 + 接入台账",
        "source": "gkx",
        "sql": "_probe_lane3_s304c 快照复用（dwd_scholar/patent/zh_paper 来源列分布）+ 词族扫描（042 复用）",
        "hits": 0,
        "hit_detail": "来源标签面缺席：dwd_scholar 来源列全量单值 gkx_ods（21,316 行）、dwd_patent 采样 14,371 行来源全 NULL、dwd_zh_paper 63,656 NULL+37,244 空——供应商库自身无『来源机构』多源标签（040 来源结构探针同族）；org 存量 189,116 行在（维度可支撑）但接入台账 0 命中：维度有、动作无、标签也无",
    },
    {
        "probe": "久新机构×接入动作面",
        "source": "jiuxin",
        "sql": "词族扫描（042 复用 jiuxin_access_tables=[]，215 表 live）",
        "hits": 0,
        "hit_detail": "ads_* 全部分析结果面（快照单期），无接入动作流水——机构活跃度不可构建",
    },
    {
        "probe": "需求原文「来源机构接入活跃度」指标定义（含评分模型）",
        "source": "doc",
        "sql": "rg 检索三份需求真源",
        "hits": 1,
        "hit_detail": "SRS 总体视窗.md seq（总览功能句）：「直观呈现各类资源的分布比例、年度增长趋势和不同来源机构的接入活跃度」——功能词在；「活跃度」评分模型（分制/因子/权重）与「接入」计数口径无定义。指标名级 0 命中",
    },
]

doc = {
    "metric_id": "M_SCIUI_DATATHM_048",
    "batch": "S3-05",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:626",
        "repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:128",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:81",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份需求真源指标名级 0 命中；总体视窗总览功能句含「不同来源机构的接入活跃度」功能词（seq 见 SRS 总体视窗.md:14）——评分模型（mock 为 0-100 分制合成分）与接入计数口径无定义"
    },
    "base_years_used": [],
    "base_years_missing": ["完全不支持：三源零承载，无库内年份基期"],
    "base_years_note": "完全不支持：无基期；mock 演示值不构成基期证据",
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": "完全不支持",
    "notes": [
        "判档：活跃度=评分模型×接入台账双缺——评分模型需求无定义（mock 五档 96/88/76/58/36 无因子可考），接入台账三源零承载（042 复用）；机构维度存量面（dev org 表族+gkx 189,116 行）只解决「机构是谁」不解决「多活跃」",
        "B11 对账：台账词族=042；org 存量=042 gkx_main_table_rows.dwd_org_base_info=189,116 同值；lane3 快照复用不重跑",
        "量纲披露（B9）：mock activity 是「分」（0-100 合成评分）非「次」——tooltip 双读数（accessCount 次+activity 分）两量纲并列，正式口径须先定评分制",
        "mock 活跃度阈值分色（>=70 蓝/>=50 橙/灰）与 status 三档（活跃/一般/较低）是前端自定阈值——不作口径证据",
    ],
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
print("org tables:", len(org_tables), "| support:", doc["support_judgment"])

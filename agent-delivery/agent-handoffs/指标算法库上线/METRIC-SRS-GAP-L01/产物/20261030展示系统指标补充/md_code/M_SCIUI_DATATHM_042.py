#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_042 历史累计接入量 · 三源探针与复现脚本（S3-05 L1）。

含义：接入视窗·历史资源接入情况·动态历史趋势可视化——「历史接入量」
逐期柱序列（trend.accessVolume）与「归档记录」累计读数（summary.archiveCount）。
UI：AccessHistorySituation.jsx:97（series name='历史接入量' bar）+ :288
（Statistic 归档记录 archiveCount=12 条）；mock 源 mockData.js:1423-1436
historyAccessDashboard（trend.accessVolume 6 点 1,860-3,360 + summary.archiveCount 12）。

判档路径（口径=「累计接入量（存量口径可代理）」）：
- 逐期序列（accessVolume）：台账缺位（L4 族证+040/041 同法）——不撑；
- 累计读数（archiveCount）：存量口径三源可数（DATAIN_002 产物：
  dev 269,511 / gkx 11 表 / 久新 210 表合计 182,707,016）；
  「归档记录条数」口径最近邻=接入台账行数——台账缺位；
→ 部分支持（累计存量读数三源双在可代理交付；逐期接入序列与
  「归档记录」台账口径缺位——与 DATAIN_002 同构）。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_042_out.json")
PROBE = os.path.join(BASE, "_probe_s305_l1_out.json")

facts, derived, notes, absence = {}, [], [], []
probe = json.load(open(PROBE, encoding="utf-8"))["probes"]

# ============ ① 词族（共享探针复用） ============
facts["dev_table_total"] = probe["dev_table_total"]
facts["dev_access_registry_tables"] = probe["dev_access_registry_tables"]  # [app_article_collect] 语义排除
facts["gkx_table_count"] = probe["gkx_table_count"]
facts["gkx_access_tables"] = probe["gkx_access_tables"]  # []
facts["jiuxin_table_count_live"] = probe["jiuxin_table_count_live"]
facts["jiuxin_access_tables"] = probe["jiuxin_access_tables"]  # []

# ============ ② 存量读数（复用族产物，B11 锚——与 DATAIN_002/027 同构） ============
p002 = json.load(open(os.path.join(BASE, "M_SCIUI_DATAIN_002_out.json"), encoding="utf-8"))
facts["dev_enterprise_base_rows"] = p002["facts"]["dev_enterprise_base_rows"]
facts["dev_enterprise_update_month_dist"] = p002["facts"]["dev_enterprise_update_month_dist"]
facts["gkx_main_table_rows"] = p002["facts"]["gkx_main_table_rows"]
facts["jiuxin_all_ads_rows_sum_210tables"] = p002["derived"][0]["value"]
facts["jiuxin_main_table_rows"] = p002["facts"]["jiuxin_main_table_rows"]

# ============ ③ mock 对照 ============
facts["ui_mock_archive_count"] = 12        # summary.archiveCount（归档记录）
facts["ui_mock_trend_access_volume"] = [1860, 2100, 2350, 2680, 3010, 3360]  # 6 点逐期（12月-5月）
facts["ui_mock_trend_labels"] = ["12月", "1月", "2月", "3月", "4月", "5月"]
facts["ui_mock_volume_cumsum"] = [sum(facts["ui_mock_trend_access_volume"][:i+1])
                                  for i in range(6)]  # 演示口径的累计形态（脚本算出）

# ================= 派生（多口径并列） =================
three_sum = (facts["dev_enterprise_base_rows"]
             + sum(facts["gkx_main_table_rows"].values())
             + facts["jiuxin_all_ads_rows_sum_210tables"])
derived.append({
    "key": "historical_cumulative_access_volume_proxy_three_source",
    "value": float(three_sum),
    "numerator": None,
    "denominator": None,
    "note": "存量代理口径三源合计=dev enterprise_base " + str(facts["dev_enterprise_base_rows"])
            + " + gkx 11 表 " + str(sum(facts["gkx_main_table_rows"].values()))
            + " + 久新 210 表 " + str(int(facts["jiuxin_all_ads_rows_sum_210tables"]))
            + "（DATAIN_002 同构口径，跨源不去重；语义=库内数据资产存量非接入动作累计）",
})
derived.append({
    "key": "historical_cumulative_access_volume",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『历史累计接入量』正式口径（接入台账逐笔累计/归档记录条数）三源无台账面"
            "（词族语义排除在案）；存量代理见并列键；按 B10 不写伪指标值",
})

# ================= absence_probe =================
absence += [
    {"probe": "dev 接入流水台账（access_log/access_history/resource_access/ingest/collect 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表，共享探针）",
     "hits": 1,
     "hit_detail": "命中 gkxlumenx_app.app_article_collect（文章收藏-用户行为表）——语义排除"
                   "（与 DATAOV_002/DATAIN_001/002 族内同结论，独立留证）；0 张接入流水表",
     },
    {"probe": "gkx 接入台账（access/ingest/collect 词族）",
     "source": "gkx",
     "sql": "词族扫描（共享探针 gkx_access_tables=[]）",
     "hits": 0,
     "hit_detail": "280 表 0 命中（L4 族探针同结论：仅 dwd_org_changerecord_info 企业变更流水"
                   "名近义异，语义排除）",
     },
    {"probe": "久新接入台账（access/ingest/collect 词族）",
     "source": "jiuxin",
     "sql": "词族扫描（共享探针 jiuxin_access_tables=[]，215 表 live）",
     "hits": 0,
     "hit_detail": "0 命中——ads_* 全部分析结果面，快照管理无逐笔接入记录",
     },
    {"probe": "需求原文「历史接入量/归档记录」指标定义",
     "source": "doc",
     "sql": "rg 检索三份需求真源",
     "hits": 0,
     "hit_detail": "「历史接入量」为 UI 图例名（AccessHistorySituation.jsx:97）；「归档记录」为 "
                   "Statistic 题名（:288）；seq 362 历史资源接入情况总览功能在"
                   "（AccessHistorySituation 组件注释自标 seq 360/362/363），累计口径与"
                   "「归档」登记语义无定义",
     },
]

support = "部分支持"

notes += [
    "判档：逐期接入序列（trend.accessVolume）台账缺位（040/041 同法）；累计读数可用存量口径"
    "三源代理（dev 269,511 + gkx 11 表 + 久新 210 表合计，DATAIN_002 同构并列）→ 部分支持",
    "口径披露：mock summary.archiveCount=12 是「归档记录条数」（台账行数语义），mock "
    "trend.accessVolume 是逐期接入量——两读数在 mock 内也未闭合（6 点合计 15,360 ≠ 12）；"
    "本件代理口径语义=「库内数据资产存量」非「接入动作累计」，补录/回溯灌库时脱钩"
    "（DATAIN_002 §2.5 同披露）",
    "B11 对账：存量三读数与月维两点全部复用 DATAIN_002 产物（零漂移）；词族与 L4 族探针一致",
    "升档触发器（B10）：①接入台账立项（资源×量×时间流水，族级）→ 升完全直接支持；"
    "②甲方裁「台账口径=归档记录条数」→ 归档口径同升；③接受存量代理 → 完全转换支持"
    "（语义降维随行披露）",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_042",
    "batch": "S3-05",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/components/AccessHistorySituation.jsx:97",
        "repos/demo-ui-science/src/pages/data-resources/components/AccessHistorySituation.jsx:288",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:1423",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份需求说明书未出现「历史累计接入量」。「历史接入量」为 UI 图例（:97）；"
                "「归档记录」为 Statistic 题名（:288）；挂靠 seq 362 历史资源接入情况总览"
                "（组件注释自标 seq 360/362/363）——功能在、累计与归档口径无定义",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "累计口径无基年概念（存量盘点型）",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "12", "1860", "3360", "15360", "269511", "2939895", "182707016",
        "269163", "348", "542", "280", "215"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

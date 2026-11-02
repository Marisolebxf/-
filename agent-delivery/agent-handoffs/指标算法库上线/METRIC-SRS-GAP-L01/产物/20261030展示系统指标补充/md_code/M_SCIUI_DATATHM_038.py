#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M_SCIUI_DATATHM_038 数据资产数量 — 证据采集脚本（S3-04 L7）
挂载点：repos/demo-ui-science/src/pages/data-resources/components/AssetApplicationBasicSummary.jsx:63
  （实查：:60-66 数据资产列 name；组件注释 seq 378-379；mock 源 mockData.js:898-905 assetRanking 7 行）

口径（同族先例 DATATHM_036/037 在案）：「数据资产数量」在 UI 无独立 StatCard，派单值取
assetRanking 行数（filtered.length 命中计数）。三源无逻辑资产目录（数据集登记面）→ 存量口径
可按库表/schema 计数交付（部分支持），资产语义边界无登记（同 036 判档根因）。

证据源（复用共享快照，B8 幂等）：
- code/M_SCIUI_DATATHM_036_out.json（表计数先例：dev 542=444 数据+98 配置 / gkx 280=181 正+99 备份
  / 久新 210=206 非空+4 空；全口径 1,032 / 剔备份 930）
- code/_snapshots/_probe_s304_l7_quality_out.json（L7 族探针：asset 词族三源命中）
- 本脚本补：assetRanking 演示行数核 + asset 词族语义排除登记。
"""
import json, re, os, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_038_out.json")
M036 = os.path.join(BASE, "M_SCIUI_DATATHM_036_out.json")
SNAP_L7 = os.path.join(BASE, "_snapshots", "_probe_s304_l7_quality_out.json")
UI_MOCK = "/Users/samuel_tang/my_project/gkx-lumen/repos/demo-ui-science/src/pages/data-resources/mockData.js"

facts = {"generated": datetime.date.today().strftime("%Y%m%d")}

# ---------- 1) 036 件计数先例复用（B8：不重跑库表计数） ----------
m036 = json.load(open(M036))["facts"]
l7 = json.load(open(SNAP_L7))
facts["precedent_reuse"] = ["M_SCIUI_DATATHM_036_out.json", "_probe_s304_l7_quality_out.json"]
facts["dev_table_count_all"] = m036["dev_table_count_all"]                # 542
facts["dev_data_schema_table_count"] = m036["dev_data_schema_table_count"]  # 444
facts["dev_config_schema_table_count"] = m036["dev_config_schema_table_count"]  # 98
facts["gkx_table_count"] = m036["gkx_table_count"]                        # 280
facts["gkx_backup_like_table_count"] = m036["gkx_backup_like_table_count"]  # 99
facts["gkx_regular_table_count"] = m036["gkx_table_count"] - m036["gkx_backup_like_table_count"]  # 181
facts["jiuxin_table_count"] = m036["jiuxin_table_count"]                  # 210（快照日 2026-11-01）
facts["jiuxin_nonzero_table_count"] = m036["jiuxin_nonzero_table_count"]  # 206
facts["jiuxin_table_count_live"] = l7.get("jiuxin_table_count_live")      # 212（live 复核，活库增长披露）
# 久新活库表数不写死（教训 6）：非空口径按快照 206 登记，live 212 增长披露另列

# ---------- 2) asset 词族命中（快照直引）+ 语义排除 ----------
facts["dev_asset_like_tables"] = sorted(l7.get("dev_asset_like_tables") or [])
facts["gkx_asset_like_tables"] = sorted(l7.get("gkx_asset_like_tables") or [])
facts["jiuxin_asset_like_tables"] = sorted(l7.get("jiuxin_asset_like_tables") or [])
facts["dev_asset_hits_semantic"] = (
    "dev 命中 2 组：gkxlumenx_bi.onl_drag_dataset_*（3 张 BI 拖拽报表配置面，"
    "语义=报表配置非数据资产目录）+ gkxlumenx_ods.dwd_org_annual_report_asset"
    "（企业年报资产明细——财务资产科目，语义≠数据资产），均语义排除"
)
facts["gkx_asset_hits_semantic"] = (
    "gkx 命中 dwd_org_annual_report_asset(_bak_zczeconv)——同企业年报财务资产，语义排除"
)

# ---------- 3) UI mock 资产清单演示值 ----------
src = open(UI_MOCK, encoding="utf-8").read()
m = re.search(r"export const assetRanking = \[(.*?)\];", src, re.S)
rows = []
if m:
    for line in m.group(1).strip().splitlines():
        kv = dict(re.findall(r"(\w+): ('[^']*'|[\d.\-]+|true|false|\[[^\]]*\])", line))
        if kv.get("id"):
            rows.append({
                "id": kv["id"].strip("'"),
                "name": kv.get("name", "").strip("'"),
                "data_type": kv.get("dataType", "").strip("'"),
                "business_type": kv.get("businessType", "").strip("'"),
                "deploy_location": kv.get("deployLocation", "").strip("'"),
            })
rows = sorted(rows, key=lambda r: r["id"])  # B5
facts["ui_mock_asset_rows"] = len(rows)
facts["ui_mock_asset_names_sorted"] = [r["name"] for r in rows]
facts["ui_mock_data_type_distribution"] = {
    t: sum(1 for r in rows if r["data_type"] == t)
    for t in sorted({r["data_type"] for r in rows})
}
# mock 披露：7 资产为叙事截断（基础研究主题库/医学影像/工程设计规范…），对应需求 seq 378 六字段画像
facts["ui_mock_disclosure"] = (
    "assetRanking 7 行为叙事截断演示清单（每行含 seq 378 六字段画像：数据类型/应用主体/部署位置/"
    "使用周期/业务模块/使用单位），非全量资产登记；『命中 N 条』随筛选联动"
)

# ---------- 4) absence_probe（四件：dev/gkx/jiuxin/doc） ----------
absence_probe = [
    {
        "db": "dev",
        "what": "542 表扫 asset/资产 词族 + 数据资产目录存在性",
        "hit": facts["dev_asset_like_tables"],
        "verdict": "命中均语义排除（BI 报表配置面/企业年报财务资产）；无逻辑数据资产目录（数据集登记面）",
    },
    {
        "db": "gkx",
        "what": "280 表扫同词族",
        "hit": facts["gkx_asset_like_tables"],
        "verdict": "命中为企业年报财务资产（语义排除）；无数据资产目录",
    },
    {
        "db": "jiuxin",
        "what": f"live {facts['jiuxin_table_count_live']} 表扫同词族",
        "hit": facts["jiuxin_asset_like_tables"],
        "verdict": "零命中——ads_* 分析面无资产目录",
    },
    {
        "db": "doc",
        "what": "三份需求真源检索『数据资产数量/资产数量』",
        "hit": [],
        "verdict": "字面零命中；seq 378 原文『为每项被应用的数据资产整理基础信息』——资产是列举对象非计数指标；cfg_metric 无条目",
    },
]
facts["absence_probe"] = absence_probe

# ---------- 5) 判档与派生（部分支持：存量库表计数可交付 + 逻辑资产口径缺） ----------
derived = [
    {
        "key": "data_asset_count_logical_catalog",
        "value": None,
        "numerator": None,
        "denominator": None,
        "note": "逻辑资产口径（数据集登记目录）三源零承载——无资产目录面，逻辑资产数量不可得",
    },
    {
        "key": "data_asset_count_physical_three_source_all",
        "value": float(m036["dev_table_count_all"] + m036["gkx_table_count"] + m036["jiuxin_table_count"]),
        "numerator": None,
        "denominator": None,
        "note": "物理存量口径全口径=036 件同源复用（542+280+210=1,032；含 99 备份+98 配置 schema）",
    },
    {
        "key": "data_asset_count_physical_no_backup",
        "value": float((m036["dev_table_count_all"] - m036["dev_backup_like_table_count"]) +
                       (m036["gkx_table_count"] - m036["gkx_backup_like_table_count"]) +
                       m036["jiuxin_nonzero_table_count"]),
        "numerator": None,
        "denominator": None,
        "note": "物理存量口径剔备份剔空=539+181+206=926（036 件剔备份口径 930 的空表收紧变体：久新取非空 206）",
    },
    {
        "key": "data_asset_count",
        "value": None,
        "numerator": None,
        "denominator": None,
        "note": "B10：资产语义边界（物理表 vs 逻辑数据集）未裁，主读数 null；多口径并列交付（B10 多口径并列）",
    },
]

out = {
    "metric_id": "M_SCIUI_DATATHM_038",
    "metric_name": "数据资产数量",
    "mount": "repos/demo-ui-science/src/pages/data-resources/components/AssetApplicationBasicSummary.jsx:63（数据资产列 name；命中计数 filtered.length :178）",
    "category": "无业务逻辑数值类",
    "srs_seq": "378-379（应用视窗/资产应用总览/应用基本情况汇总+多维筛选，excel_row 381-382）",
    "support_judgment": "部分支持",
    "base_years_used": [],
    "base_years_missing": ["逻辑资产目录面三源零承载，无登记年份维", "物理存量口径为快照计数，无年度基期"],
    "base_years_note": "部分支持档：物理口径基期=探针快照日（dev 2026-11-01 / 久新 210 表快照+212 live 复核），非年度基期；逻辑资产口径无基期",
    "facts": facts,
    "derived": derived,
    "notes": sorted([
        "口径核：UI 无独立资产数 StatCard，派单值=assetRanking 行数（mock 7）；seq 378 资产是列举对象非计数指标",
        "同族先例：DATATHM_036（表总数 部分支持：多口径 1,032/930）/037（库均表数）——本件共享其计数底账与判档根因",
        "语义排除三处：BI 拖拽配置面/企业年报财务资产（dev+gkx）——『asset』字面≠数据资产",
        "逻辑资产目录（数据集登记面）三源零承载——006 件价值分级共享同一基建缺口",
        "久新活库 212 live 复核 vs 快照 210：活库增长披露（教训 6 不写死）",
    ]),
}
json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("done ->", OUT)

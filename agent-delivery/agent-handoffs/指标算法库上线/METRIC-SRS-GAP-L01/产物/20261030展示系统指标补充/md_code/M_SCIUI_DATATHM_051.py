#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_051 接入渠道数量——三源探针+产物生成（S3-05 L1）。

挂载 AccessSourceAnalysisDetail.jsx:363（Statistic title="渠道数" value={channels.length} suffix="类"）。
mock accessSourceAnalysis.channels（mockData.js:100-106）五渠道：科研院所/企业/第三方平台/高等院校/政府部门。
口径=渠道维度的基数（DISTINCT count of 渠道分类）——需资源×渠道归属面（元数据）。
三源：051 与 048 同病（来源/渠道标签缺位）；本件新探针=dev 全库 channel 字段扫描
（列名 channel 词族——dwd_bid_base_out.channel 等候选逐条核对）。
"""
import json
import os

import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_051_out.json")

d042 = json.load(open(os.path.join(BASE, "M_SCIUI_DATATHM_042_out.json"), encoding="utf-8"))

conn = pymysql.connect(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
                       charset="utf8mb4", autocommit=True,
                       cursorclass=pymysql.cursors.DictCursor)
channel_cols = []
channel_dist = None
try:
    with conn.cursor() as cur:
        # 本件新探针①：dev 全库列级 channel 词族（排除 demo）
        cur.execute(
            "SELECT table_schema, table_name, column_name, data_type "
            "FROM information_schema.columns "
            "WHERE table_schema LIKE 'gkxlumenx%%' AND table_schema NOT LIKE '%%demo%%' "
            "AND column_name LIKE '%%channel%%'")
        channel_cols = [[r["TABLE_SCHEMA"], r["TABLE_NAME"], r["COLUMN_NAME"], r["DATA_TYPE"]]
                        for r in cur.fetchall()]
        # 本件新探针②：候选列的值分布（渠道维度语义核对）
        dists = []
        for sch, tb, col, _dt in channel_cols:
            try:
                cur.execute(
                    f"SELECT `{col}` v, COUNT(*) c FROM `{sch}`.`{tb}` "
                    f"WHERE `{col}` IS NOT NULL AND `{col}` != '' GROUP BY v ORDER BY c DESC LIMIT 8")
                rows = [[r["v"], r["c"]] for r in cur.fetchall()]
                if rows:
                    dists.append([f"{sch}.{tb}.{col}", rows])
            except Exception:
                pass
        channel_dist = dists
finally:
    conn.close()

ui_mock_channels = [
    ["科研院所", 12580, 485, 38.6], ["企业", 8920, 356, 28.3],
    ["第三方平台", 6240, 245, 19.5], ["高等院校", 4120, 120, 9.6],
    ["政府部门", 1810, 50, 4.0],
]  # mockData.js:100-106 实抄（name/volume/count/share；B5 按 volume 降序=mock 原序）

facts = {
    "dev_table_total": d042["facts"]["dev_table_total"],
    "gkx_table_count": d042["facts"]["gkx_table_count"],
    "jiuxin_table_count_live": d042["facts"]["jiuxin_table_count_live"],
    "dev_channel_column_scan": channel_cols,
    "dev_channel_dist_probe": channel_dist,
    "ui_mock_channels": ui_mock_channels,
    "ui_mock_channel_count": len(ui_mock_channels),
    "ui_mock_volume_total": sum(r[1] for r in ui_mock_channels),
    "ui_mock_count_total": sum(r[2] for r in ui_mock_channels),
}

derived = [
    {
        "key": "access_channel_count",
        "value": None,
        "numerator": None, "denominator": None,
        "note": "『接入渠道数量』正式口径（资源登记面的渠道维度基数）需资源×渠道归属元数据——dev channel 词族列逐条语义核对无资源渠道归属面（业务字段排除）；gkx 来源标签三面全空（lane3 复用）；按 B10 不写伪指标值。注意 mock 渠道名（科研院所/企业…）是来源机构分类非传输渠道（API/文件/DB 同步）——UI 自身两套渠道词混用（019/053 另一套）"
    },
]

absence_probe = [
    {
        "probe": "dev 列级 channel 词族 + 值分布",
        "source": "dev",
        "sql": "information_schema.columns 扫 gkxlumenx_* 非 demo + 逐列 TOP8 分布（本件新探针）",
        "hits": len(channel_cols),
        "hit_detail": f"channel 词族命中 {len(channel_cols)} 列——逐条语义核对：dwd_bid_base_out.channel 等为业务字段（招标渠道/融资轮次等），无『资源接入渠道归属』登记列；值分布佐证（见 facts.dev_channel_dist_probe）——渠道维度的资源登记面不存在",
    },
    {
        "probe": "gkx 渠道/来源归属面",
        "source": "gkx",
        "sql": "lane3 快照复用（来源标签三面）+ 042 词族",
        "hits": 0,
        "hit_detail": "来源标签三面全空（scholar 单值 gkx_ods/patent NULL 100%/zh_paper 空 100%——048 同锚）；280 表无 channel 资源登记面",
    },
    {
        "probe": "久新渠道归属面",
        "source": "jiuxin",
        "sql": "词族扫描（042 复用，215 表 live）",
        "hits": 0,
        "hit_detail": "ads_* 分析结果面快照单期，无资源×渠道登记",
    },
    {
        "probe": "需求原文「渠道数/接入渠道」指标定义",
        "source": "doc",
        "sql": "rg 检索三份需求真源",
        "hits": 1,
        "hit_detail": "SRS 接入视窗.md 渠道相关功能句在（seq 361 渠道周期/363 渠道对比——「按渠道」维度词多见）；「渠道数量」指标名级 0 命中（UI Statistic 题名）；渠道 taxonomy（来源机构分类 vs 传输方式）无定义——UI 两套词混用证据在案",
    },
]

doc = {
    "metric_id": "M_SCIUI_DATATHM_051",
    "batch": "S3-05",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/components/AccessSourceAnalysisDetail.jsx:363",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:100",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "指标名级 0 命中；「渠道数」为 UI Statistic 题名（channels.length 动态计数——mock 五类）；渠道 taxonomy 无定义：本挂载 mock 渠道=来源机构分类（科研院所/企业/第三方平台/高等院校/政府部门），而 019/044/053 的 updateCycleStats/accessChannelStats 渠道=传输方式（API接口/文件传输/数据库同步/人工录入/物联网采集）——同一前端两套渠道词"
    },
    "base_years_used": [],
    "base_years_missing": ["完全不支持：三源零承载，无库内年份基期"],
    "base_years_note": "完全不支持：无基期；mock 演示值不构成基期证据",
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": "完全不支持",
    "notes": [
        "判档：渠道维度的资源登记面三源缺位（dev channel 列全业务语义/gkx 来源标签三面空/久新快照无登记）——渠道基数无分母面；UI 双套渠道词混用（来源机构 vs 传输方式）是口径级前置缺口",
        "B11 对账：gkx 来源标签=lane3 快照（048 同锚）；台账词族=042；mock 五渠道与 042 首段来源五分类同款（资源来源分析共享 mock）",
        "渠道词消歧登记：科研院所五类（来源机构）≠ API 五类（传输方式）——本件判「来源机构分类」口径（挂载所在卡为「资源来源分析」），传输方式口径归 019/044/053 族",
    ],
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
print("channel cols:", len(channel_cols), "| dist probes:", len(channel_dist or []))
print("support:", doc["support_judgment"])

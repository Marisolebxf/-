#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_035 数据应用排行榜 · 三源探针脚本（S3-04 L6）。

含义：科技数据资源·应用视窗·资产应用总览「数据应用排行榜」卡的榜单本体
——数据资产×调用量×用户数×环比增长的多字段排行列表（034 是位次端，本件是本体端）。
UI：repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:1294
（Card title="数据应用排行榜"，:1295 getAssetRankingOption 条形图 + :1300-1312 表格
assetColumns：排名/资产名称/类别/调用次数/部门/环比；mock 源 mockData.js:898-905
assetRanking 7 条，每条含 calls/users/growth/category/department/dataType/appSubject/
deployLocation/usageCycle/businessModules/businessType/usageUnit/lastActiveDate）。

判档路径（口径=「数据资产多字段调用排行列表」）：
- 直接承载：需资产×调用量台账（+用户/环比扩展维）——三源词族 0 命中；
- 扩展维：用户数（distinct 调用用户）、环比增长（上期调用量）均依赖同一台账的时间/主体明细，
  台账缺位则全链缺位；
- 判完全不支持（与 034 同根：排序对象与排序依据双缺）。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_035_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_probe_s304_l6_heat_out.json")
L5SNAP = os.path.join(BASE, "_snapshots", "_probe_s304_l5_out.json")

facts, derived, notes, absence = {}, [], [], []
probe = json.load(open(SNAP, encoding="utf-8"))["probes"]
l5 = json.load(open(L5SNAP, encoding="utf-8"))["probes"]

# ============ ① dev：词族命中 + 行数复核 + 用户面最近邻 ============
facts["dev_call_rank_heat_tables"] = probe["dev_call_rank_heat_tables"]
facts["dev_call_rank_heat_table_rows"] = probe["dev_call_rank_heat_table_rows"]
facts["dev_table_total"] = probe["dev_table_total"]
# 用户维最近邻（assetRanking.users 字段的承载探针）：L5 族已证 sys_user 仅 3 行平台账号
facts["dev_sys_user_rows"] = l5["dev_sys_user_rows"]
facts["dev_sys_user_usernames"] = l5["dev_sys_user_usernames"]

# ============ ② gkx：词族复核（0 命中） ============
facts["gkx_call_rank_heat_tables"] = probe["gkx_call_rank_heat_tables"]

# ============ ③ 久新：词族 live 复核 ============
facts["jiuxin_probe_mode"] = probe["jiuxin_probe_mode"]
facts["jiuxin_table_count_live"] = probe["jiuxin_table_count_live"]
facts["jiuxin_call_rank_heat_tables"] = probe["jiuxin_call_rank_heat_tables"]

# ================= 派生（负结论登记，B10） =================
derived.append({
    "key": "asset_application_ranking_list",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『数据应用排行榜（榜单本体：资产×调用量×用户数×环比）』需资产×调用量台账"
            "（含用户与时间明细以支撑扩展维）——三源词族 0 命中（dev 5 张命中全 0 行语义排除；"
            "gkx 0 命中；久新 14 张命中全为科研问题/技术热度语义排除）且资产登记轴三源未建"
            "（DATAOV_001 同根）→ 主维与扩展维全链缺位，按 B10 留空即负结论登记",
})

# ================= absence_probe =================
absence += [
    {"probe": "dev 资产调用台账面（call/invoke/usage/rank/heat/hot/trend/ranking/leaderboard 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表）+ 命中表 COUNT 复核",
     "hits": 0,
     "hit_detail": "词族命中 5 张全部语义排除且 0 行（chain_hotspot/enterprise_ranking/"
                   "industry_chain_graph_snapshot/enterprise_growth_trend/policy_support_rank）"
                   "——无一含资产×调用量×用户×时间明细",
     },
    {"probe": "gkx 调用/榜单词族（call/invoke/usage/rank/heat/hot/trend/leaderboard/popular）",
     "source": "gkx",
     "sql": "information_schema.tables 扫 gkx（280 表，经 _gkxdb.py）",
     "hits": 0,
     "hit_detail": "命中 []——要素明细库无调用监控面；mock users 字段（1,234/987/756…）"
                   "所要求的 distinct 调用用户维在 gkx 无任何承载表",
     },
    {"probe": "久新调用/榜单词族（同词族 live 复核）",
     "source": "jiuxin",
     "sql": "SHOW TABLES（活库 212 表）词族扫 + 语义核对",
     "hits": 0,
     "hit_detail": "命中 14 张全部语义排除（科研问题/技术热度面，与 034 件同一批排除证据）；"
                   "ads_* 无资产级调用统计面；探测模式 live",
     },
    {"probe": "用户维最近邻（assetRanking.users 承载探针）",
     "source": "dev",
     "sql": "SELECT COUNT(*), username FROM gkxlumenx.sys_user（L5 族探针）",
     "hits": 3,
     "hit_detail": "dev sys_user 仅 3 行平台管理账号（admin 等）——是平台运维账号面非"
                   "『数据资产调用用户』注册面；mock users 1,234/987/756…量级的用户基础"
                   "三源皆无（用户注册/行为面未建），扩展维独立缺位",
     },
    {"probe": "需求原文「数据应用排行榜」定义段",
     "source": "doc",
      "sql": "rg 数据应用排行榜 三份需求真源",
     "hits": 1,
     "hit_detail": "SRS 应用视窗.md seq 376（excel_row 379）『自动统计并展示各数据资源被调用"
                   "和使用的排行情况，支持按时间、应用主体或业务领域进行排序…』——与 034 同源"
                   "需求句；本件承接榜单本体（多字段列表+条形图），034 承接位次端；"
                   "mock assetRanking 13 字段为演示值",
     },
]

support = "完全不支持"

notes += [
    "判档：数据应用排行榜（本体）=资产×调用量×用户×环比多字段列表——主维（资产调用台账）"
    "与扩展维（用户数/环比增长）全链依赖同一台账，三源词族逐一 0 命中 → 指标及关键依赖"
    "三源均无法构建 → 完全不支持（与 034 同根同判，独立留证）",
    "mock 披露：ApplicationWindow.jsx:1294 Card 消费 mockData.js:898-905 assetRanking 7 条 13 字段"
    "（calls 856,000 领衔/users 1,234/growth 15.2%/usageCycle/lastActiveDate 等）——演示值，"
    "不作数据证据（B10）",
    "用户维独立缺位披露：dev sys_user 仅 3 行平台管理账号（L5 族探针同读数，B11），"
    "mock 千级用户量的基础三源皆无（用户注册/行为面未建）——即便台账建成，users 字段仍需"
    "用户体系补齐",
    "环比维同根披露：growth（环比）需上期调用量——时间明细缺位下环比无从算起（032 件同根）",
    "B11 对账：词族扫描与 L5/L6 族探针一致；sys_user 3 行与 L5 族（DATATHM_016 平台月活跃件）"
    "同读数零漂移",
    "升档触发器（B10）：①调用台账+资产登记面+用户体系 → 升完全直接支持（三件套并项）；"
    "②第三方监测+白名单 → 升完全转换支持（users/growth 字段降维披露）；③维持现状 → 完全不支持",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_035",
    "batch": "S3-04",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:1294",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:898",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "SRS 应用视窗.md seq 376「数据应用排行榜」（excel_row 379）需求明列叶；"
                "本件承接榜单本体端（多字段列表），与 034（位次端）同源同叶拆件",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "榜单本体类读数，不涉基期年",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["376", "542", "280", "212", "856000", "1234", "15.2", "3"][:8]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

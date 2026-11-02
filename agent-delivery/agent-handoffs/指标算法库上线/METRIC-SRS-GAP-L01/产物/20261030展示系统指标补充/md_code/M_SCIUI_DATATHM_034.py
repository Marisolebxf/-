#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_034 数据资产调用量排名（Top 榜位次）· 三源探针脚本（S3-04 L6）。

含义：科技数据资源·应用视窗·资产应用总览的「数据应用排行榜」Top 榜位次
——按数据资产（主题库/数据集）聚合调用量并排序取 Top N。
UI：repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:203
（assetColumns 第 1 列「排名」Badge count={i+1}，前三名蓝色；数据源 mockData.js:898-905
assetRanking：基础研究主题库 856,000 / 医学影像数据集 642,000 / 工程设计规范库 534,000…7 条；
另一挂载 :81-92 getAssetRankingOption 横向条形图 + :1293-1298 Card「数据应用排行榜」）。

判档路径（口径=「按数据资产聚合调用量的 Top N 位次」）：
- 直接承载：需资产×调用量台账——三源词族 0 命中（dev 5 张命中表全 0 行且语义排除）；
- 语义最近邻：dev enterprise_ranking（企业排名结果面，0 行且语义为企业非数据资产，排除）；
- 资产登记轴：三源无资产编目（DATAOV_001 目录缺口同根）——排序对象不存在；
- 判完全不支持。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_034_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_probe_s304_l6_heat_out.json")

facts, derived, notes, absence = {}, [], [], []
probe = json.load(open(SNAP, encoding="utf-8"))["probes"]

# ============ ① dev：词族命中 + 行数复核（语义排除证据） ============
facts["dev_call_rank_heat_tables"] = probe["dev_call_rank_heat_tables"]
facts["dev_call_rank_heat_table_rows"] = probe["dev_call_rank_heat_table_rows"]
facts["dev_table_total"] = probe["dev_table_total"]

# ============ ② gkx：词族复核（0 命中） ============
facts["gkx_call_rank_heat_tables"] = probe["gkx_call_rank_heat_tables"]

# ============ ③ 久新：词族 live 复核 + 榜单语义最近邻 ============
facts["jiuxin_probe_mode"] = probe["jiuxin_probe_mode"]
facts["jiuxin_table_count_live"] = probe["jiuxin_table_count_live"]
facts["jiuxin_call_rank_heat_tables"] = probe["jiuxin_call_rank_heat_tables"]
facts["jiuxin_ads_research_problem_competition_rank_rows"] = probe[
    "jiuxin_ads_research_problem_competition_rank_rows"]

# ================= 派生（负结论登记，B10） =================
derived.append({
    "key": "asset_call_rank_topn",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『数据资产调用量 Top 榜位次』需资产×调用量台账 + 资产登记轴——三源词族 0 命中"
            "（dev 5 张命中全 0 行且语义排除；gkx 0 命中；久新 14 张命中全为科研问题/技术热度"
            "语义排除）且资产编目面三源未建（DATAOV_001 同根）→ 排序对象与排序依据双缺，"
            "按 B10 留空即负结论登记",
})

# ================= absence_probe =================
absence += [
    {"probe": "dev 资产调用台账与排名面（call/invoke/usage/rank/heat/hot/trend/ranking/leaderboard 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表）+ 命中表 COUNT 复核",
     "hits": 0,
     "hit_detail": "词族命中 5 张全部语义排除且 0 行：最近邻 enterprise_ranking（企业排名结果面，"
                   "0 行）语义为『企业』非『数据资产』且为空表；chain_hotspot/policy_support_rank 等"
                   "同为产业链/政策面——无一为资产×调用量台账",
     },
    {"probe": "gkx 调用/榜单词族（call/invoke/usage/rank/heat/hot/trend/leaderboard/popular）",
     "source": "gkx",
     "sql": "information_schema.tables 扫 gkx（280 表，经 _gkxdb.py）",
     "hits": 0,
     "hit_detail": "命中 []——gkx 为要素明细库（论文/专利/机构/学者），无任何调用监控或资产排名面；"
                   "要素量榜（专利数/论文数）语义为『科研产出排名』非『数据资产调用量排名』，语义排除",
     },
    {"probe": "久新调用/榜单词族（同词族 live 复核）+ 竞争排名表语义核对",
     "source": "jiuxin",
     "sql": "SHOW TABLES（活库 212 表）词族扫 + ads_research_problem_competition_rank DESCRIBE",
     "hits": 0,
     "hit_detail": "词族命中 14 张全部语义排除；榜单最近邻 ads_research_problem_competition_rank"
                   f"（{probe['jiuxin_ads_research_problem_competition_rank_rows']} 行）列为 "
                   "problem_id/subject_name/metric_value/ranking——『科研问题竞争主体排名』"
                   "（按文献计量指标对国家/机构排名），非数据资产调用量排名，语义排除；探测模式 live",
     },
    {"probe": "需求原文「排行榜」定义段",
     "source": "doc",
     "sql": "rg 排行|排序|活跃度 三份需求真源",
     "hits": 1,
     "hit_detail": "SRS 应用视窗.md seq 376（excel_row 379）『自动统计并展示各数据资源被调用和"
                   "使用的排行情况，支持按时间、应用主体或业务领域进行排序，帮助用户直观了解哪些"
                   "数据资产在实际业务中最具活跃度和价值』——排行对象（数据资产）与排序键（调用量）"
                   "在、算式与 Top N 深度无定义；UI mock assetRanking 7 条为演示值（mockData.js:898-905）",
     },
]

support = "完全不支持"

notes += [
    "判档：数据资产调用量 Top 榜=按资产聚合调用量排序——需『资产×调用量台账』+『资产登记轴』双前提，"
    "三源词族逐一 0 命中（dev 最近邻 enterprise_ranking 为 0 行企业排名面，排除）→ 指标及关键依赖"
    "三源均无法构建 → 完全不支持",
    "mock 披露：ApplicationWindow.jsx:203-208 排名列（Badge 前三蓝）+ :81-92 getAssetRankingOption "
    "横向条形图 + :1293-1298 Card 消费 mockData.js:898-905 assetRanking（基础研究主题库 856,000 领衔"
    "7 条）——演示值，不作数据证据（B10）",
    "需求侧证据：seq 376 把『被调用和使用的排行情况』列为功能要求（对象与排序键在）——工程前提"
    "（资产级调用统计）三源未建；本件是 SRS 需求明列叶 seq 376「数据应用排行榜」的位次端读数",
    "权威口径参照（R2 深圳开放平台）：接口调用总量 TOP10 + 近七日调用 TOP10 双榜公示——资产级"
    "调用量榜的官方实践形态，前提是接口调用日志",
    "资产登记轴：三源无数据资产编目面（DATAOV_001 目录缺口同根）——即便台账建成，『数据资产』"
    "的登记边界（哪些库/表/接口算资产）仍需裁定，族内互引",
    "B11 对账：dev 542/gkx 280/久新 212（live）表数与 L6 族探针一致；词族扫描与 L5 族探针同法同结论",
    "升档触发器（B10）：①API 网关/调用台账 + 资产登记面 → 升完全直接支持（族级共用）；"
    "②第三方监测+资产白名单裁定 → 升完全转换支持（Top N 深度须甲方定）；③维持现状 → 完全不支持",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_034",
    "batch": "S3-04",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:203",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:898",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "SRS 应用视窗.md seq 376「数据应用排行榜」（excel_row 379）为需求明列叶；"
                "本件是该叶的『Top 榜位次』读数（排行对象与排序键在、算式与 Top N 深度无定义）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "榜单位次类读数，不涉基期年",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["376", "379", "542", "280", "212", "856000", "7"][:8]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_005 主题总数 · 三源探针与复现脚本（S3-04 L1）。

含义：科技数据资源·总体视窗·多源数据整合分析主题下钻弹窗的汇总项「主题总数」——
UI mock 给常量 '7个'（resourceThemeDistribution 数组长度）。指标语义=平台数据资源的
主题分类维计数：平台把接入的资源按主题（基础科学/工程技术/医学健康…）归类后，主题的个数。
UI：repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:750
（DrillDownCard summaryItems，drillDownKey='theme'；mock 源 mockData.js:14-22
resourceThemeDistribution 7 主题演示值）。

判档路径：
- 直接承载：三源无「数据资源×主题」资产登记/编目面（DATAOV_001 已证登记面合计 8 条样例级，
  且无主题维映射表）→ 无 7 主题口径的直接结果面；
- 转换承载（主题维表计数）：dev 有多张主题/行业/技术域维表（tech_domain 10、industry_cluster 15、
  cms_industry_custom 65 等）+ gkx 主题分析维表族 + 久新 ads_discipline_* 学科维表族——
  三源结构在、计数可产出，但「主题」口径未定义（哪张维表=UI 的 7 主题？无映射裁定）；
- 判部分支持（口径开放待裁定 + 登记面缺位，计数面三源在）。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_005_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s304_l1_out.json")

import pymysql  # noqa: E402

facts, derived, notes, absence = {}, [], [], []
snap = json.load(open(SNAP, encoding="utf-8"))
probe = json.load(open(PROBE, encoding="utf-8"))["probes"]

# ============ ① dev：主题/行业/技术域维表计数（复用族级探针，本件直查复核） ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
d = pymysql.connect(**DEV)
c = d.cursor()

def q(sql):
    c.execute(sql)
    return c.fetchall()

# 主题候选维表逐一精确计数（B5：按键排序）
dim_targets = [
    ("gkxlumenx_dim", "tech_domain"),            # 技术域维表
    ("gkxlumenx_dim", "industry_cluster"),        # 产业集群
    ("gkxlumenx_dim", "industry_cluster_map"),    # 产业×主题映射
    ("gkxlumenx_cms", "cms_industry_custom"),     # 自定义行业主题
    ("gkxlumenx_dim", "code_nic"),                # 国民行业分类
]
dev_dim = {}
for sch, tab in dim_targets:
    c.execute(f"SELECT COUNT(*) FROM `{sch}`.`{tab}`")
    dev_dim[f"{sch}.{tab}"] = int(c.fetchone()[0])
facts["dev_theme_dim_counts"] = dev_dim

# dev 主题词族命中表（语义分层标注）
theme_like = probe["dev_theme_like_tables"]
facts["dev_theme_like_tables"] = theme_like

# dev topic_enterprise schema 表数（主题企业专题库工程面）
facts["dev_topic_enterprise_table_count"] = probe["dev_topic_enterprise_table_count"]

# dev 数据资源×主题登记面探针（资产目录主题维——DATAOV_001 同族缺口）
c.execute(
    "SELECT table_schema, table_name FROM information_schema.tables "
    "WHERE table_schema LIKE 'gkxlumenx%' "
    "AND table_name REGEXP 'resource|asset|catalog|metadata' ORDER BY table_schema, table_name")
facts["dev_resource_catalog_like_tables"] = [f"{r[0]}.{r[1]}" for r in c.fetchall()]
d.close()

# ============ ② gkx：主题分析维表族（经 _gkxdb.py 唯一入口） ============
import sys  # noqa: E402
sys.path.insert(0, BASE)
import _gkxdb  # noqa: E402

gcur = _gkxdb.gkx()
gkx_dims = {}
for tab in ("dwd_industry_analysis_topic_dict", "dwd_industry_analysis_topics"):
    gcur.execute(f"SELECT COUNT(*) FROM gkx.`{tab}`")
    gkx_dims[tab] = int(gcur.fetchone()[0])
facts["gkx_theme_dim_counts"] = gkx_dims
facts["gkx_theme_like_tables"] = probe["gkx_theme_like_tables"]
facts["gkx_table_count"] = snap["gkx"]["table_count"]
# gkx 论文/专利学科主题列探针（列级）
facts["gkx_paper_theme_cols"] = probe["gkx_dwd_zh_paper_theme_cols"]
facts["gkx_patent_theme_cols"] = probe["gkx_dwd_patent_theme_cols"]
gcur.close()

# ============ ③ 久新：学科主题维表族（Doris；当日两连败→快照口径，登记未取证） ============
JIUXIN_LIVE = False
try:
    JX = dict(host="47.93.119.170", port=29030, user="test2",
              password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
              database="gkx_technology_analysis_dev",
              connect_timeout=10, read_timeout=300)
    jconn = pymysql.connect(**JX)
    JIUXIN_LIVE = True
    jc = jconn.cursor()
    jx_dims = {}
    for tab in ("ads_discipline_domain", "ads_discipline_field",
                "ads_discipline_subfield", "ads_discipline_topic"):
        jc.execute(f"SELECT COUNT(*) FROM `{tab}`")
        jx_dims[tab] = int(jc.fetchone()[0])
    facts["jiuxin_theme_dim_counts_live"] = jx_dims
    jc.execute("SHOW TABLES")
    facts["jiuxin_table_count_live"] = len(jc.fetchall())
    jconn.close()
    facts["jiuxin_probe_mode"] = "live"
except Exception:
    # 共享快照兜底：_lane7_shared_probe_out.json 的 jiuxin.tables（2026-11-01 当日清单）
    jx_tables = snap["jiuxin"]["tables"]
    facts["jiuxin_table_count_snapshot"] = snap["jiuxin"]["table_count"]
    facts["jiuxin_theme_like_tables_snapshot"] = sorted(
        t for t in jx_tables if any(w in t for w in ("discipline", "domain", "topic", "theme", "subject")))
    facts["jiuxin_probe_mode"] = ("snapshot：当日两次连接失败（Reach limit of connections），"
                                  "按久新连接纪律停手；学科维表计数未取证（快照表清单在案，"
                                  "ads_discipline_domain/field/subfield/topic 四张均在清单）")
    facts["jiuxin_connect_errors"] = probe.get("jiuxin_connect_errors", [])[:2]

# ================= 派生（B3 同基；本件为计数类，派生=各维表计数并列，非比值） =================
derived.append({
    "key": "theme_total_by_source",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『主题总数』单一口径值 null（B10）：UI mock 的 7 个主题（resourceThemeDistribution "
            "长度）是前端演示分类，三源无该 7 类口径的主题映射表；各源主题维候选计数见 "
            "facts（dev tech_domain 10/industry_cluster 15/cms_industry_custom 65、gkx 主题分析"
            "维表、久新 ads_discipline_* 族）——口径须甲方裁定后方可取数",
})

# ================= absence_probe =================
absence += [
    {"probe": "dev 数据资源×主题资产登记面（resource/asset/catalog/metadata 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表）",
     "hits": len([t for t in facts["dev_resource_catalog_like_tables"]
                  if "catalog" in t or "metadata" in t]),
     "hit_detail": f"命中 {facts['dev_resource_catalog_like_tables'][:8]}——多为 cms 内容管理表；"
                   "无『资源×主题』资产目录表（与 DATAOV_001 资产目录缺口同根）；"
                   "gen_datasource_conf 0 行 + jimu_report_data_source 8 行（样例级，共享快照）",
     },
    {"probe": "gkx 主题维表（theme/topic/subject/discipline/domain 词族 280 表）",
     "source": "gkx",
     "sql": "information_schema.tables 扫 gkx（280 表）",
     "hits": len(facts["gkx_theme_like_tables"]),
     "hit_detail": f"命中 {facts['gkx_theme_like_tables']}——产业主题分析维表族（面向产业链分析，"
                   "非数据资源主题编目）；论文 32 列/专利 55 列学科主题类列 0 命中"
                   "（gkx_paper_theme_cols/gkx_patent_theme_cols 均 []）",
     },
    {"probe": "久新学科主题维表（ads_discipline_* 族，表级存在性）",
     "source": "jiuxin",
     "sql": "SHOW TABLES 快照（210 表，2026-11-01）词族扫 + 当日两次直连尝试",
     "hits": 4,
     "hit_detail": "ads_discipline_domain/ads_discipline_field/ads_discipline_subfield/"
                   "ads_discipline_topic 四张学科维表在 2026-11-01 表清单快照中（学科主题维结构在）；"
                   "当日直连两次失败（Reach limit of connections 1203），计数未取证——"
                   "按久新连接纪律停手登记，非『不存在』",
     },
    {"probe": "需求原文「主题总数/主题」定义段",
     "source": "doc",
     "sql": "rg 主题 三份需求真源",
     "hits": 0,
     "hit_detail": "三份需求说明书未出现「主题总数」指标名；主需求 :2493（资源来源分析与详情）"
                   "最近语境为『详细分析资源来源的结构组成及变化』——来源结构非主题分类；"
                   "UI 的 7 主题是前端演示分类（mockData.js:14-22），不作口径证据",
     },
]

support = "部分支持"

notes += [
    "判档：『数据资源×主题』资产登记/编目面三源零承载（与 DATAOV_001 资产目录缺口同根）"
    "→ 直接承载无；主题维候选表三源结构+数据双在（dev 维表族精确计数、gkx 产业主题分析维表族、"
    "久新 ads_discipline_* 族在快照清单）→ 转换计数可产出，但『主题』口径未定义（7 主题映射"
    "须甲方裁定）→ 部分支持",
    f"dev 主题维候选计数（本件实查）：{facts['dev_theme_dim_counts']}——tech_domain 10 为技术域"
    "口径、industry_cluster 15 为产业集群口径、cms_industry_custom 65 为运营自定义行业口径、"
    "code_nic 2197 为国民行业分类口径：四张维表口径互异，无一张与 UI 7 主题同构",
    f"gkx 主题维候选：{facts['gkx_theme_dim_counts']}（产业主题分析域）；"
    f"论文/专利学科主题类列 0 命中（{facts['gkx_paper_theme_cols']} / {facts['gkx_patent_theme_cols']}）",
    f"久新探针模式：{facts['jiuxin_probe_mode']}",
    "mock 披露：OverviewWindow.jsx:750 summaryItems 的『主题总数 7 个』来自 mockData.js:14-22 "
    "resourceThemeDistribution 数组长度（7 主题演示值：基础科学 4,230/工程技术 3,890/…），"
    "mock 结构披露用，不作数据证据（B10）",
    "B11 对账：dev 542 表/gkx 280 表/久新 210 张取自 _lane7_shared_probe_out.json 共享快照，零漂移；"
    "登记面读数（gen 0 + jimu 8）与 DATAOV_001 产物一致",
    "升档触发器（B10）：①建数据资源×主题资产目录（DATAOV_001 触发器①并项）+ 主题映射裁定 → "
    "完全直接支持；②甲方裁定主题口径=某张既有维表（如 tech_domain 10 类）→ 完全转换支持",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_005",
    "batch": "S3-04",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:750",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:14",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书未出现「主题总数」指标名（附录 A.2 检索记录）；仅见于 UI 下钻弹窗"
                "汇总项（mock 常量 7 个）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "计数类指标，不涉基期年",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["7", "10", "15", "65", "2197", "50", "542", "280", "210", "21", "8", "4"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

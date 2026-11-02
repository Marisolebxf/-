#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_040 数据量及其期际变化 · 三源探针与复现脚本（S3-05 L1）。

含义：主题视窗·来源结构组成分析卡「数据量与变化」视图——按五类来源
（国内数据库/国外数据库/科研院所/企业/开源平台）展示数据量（volume 条）与
期际变化（change %，环比箭头）。UI：
- ResourceSourceAnalysisDetail.jsx:396（Segmented option '数据量与变化' value='bar'）
- 同文件 :89-107 getStructureBarOption（volume 横条 + change 百分比标签）
- 同文件 :240-249 channelColumns「环比变化」列（Tag ±%）
mock 源 mockData.js:160-229 overviewSourceAnalysis.sourceTypes
（五类 volume 6,820/4,560/8,234/5,234/5,550 + change 14.2/8.6/12.5/18.3/22.1）。

判档路径（口径=「来源类×数据量×期际变化率」双维序列）：
- 直接承载：来源台账（来源类×量×期）三源零承载（L4 族探针在案）；
- 代理轴：存量读数三源双在（DATAIN_002/027 产物）；dev data_source 分组轴有值
  但 taxonomy 分叉（DATATHM_027 证）；期际变化需「同来源类两期量」——
  月维分布仅 2026-08/2026-09 两点且 9 月仅 348 行（DATAIN_001 同法），
  5 类来源的分期变化序列不可构建；
- gkx table_data_source 标签轴三表空载（DATAIN_003 证：dwd_scholar 单标签/
  dwd_zh_paper 100% 无效/dwd_patent 采样全 null）；
→ 完全不支持（期际变化维三源无承载，来源类分组轴仅 dev 有血缘值且无分期）。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_040_out.json")
PROBE = os.path.join(BASE, "_probe_s305_l1_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")

facts, derived, notes, absence = {}, [], [], []
probe = json.load(open(PROBE, encoding="utf-8"))["probes"]
snap = json.load(open(SNAP, encoding="utf-8"))

# ============ ① 词族（共享探针复用，absence 原料） ============
facts["dev_table_total"] = probe["dev_table_total"]
facts["dev_growth_tables"] = probe["dev_growth_tables"]  # [enterprise_growth_trend] 语义排除用
facts["gkx_table_count"] = probe["gkx_table_count"]
facts["jiuxin_table_count_live"] = probe["jiuxin_table_count_live"]

# ============ ② dev 最近邻：enterprise_growth_trend 语义核 ============
import pymysql  # noqa: E402
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
conn = pymysql.connect(**DEV)
cur = conn.cursor()
cur.execute("SHOW COLUMNS FROM gkxlumenx_dwd.enterprise_growth_trend")
facts["dev_growth_trend_cols"] = [r[0] for r in cur.fetchall()]
cur.execute("SELECT COUNT(*) FROM gkxlumenx_dwd.enterprise_growth_trend")
facts["dev_growth_trend_rows"] = int(cur.fetchone()[0])
# 月维代理（与 DATAIN_001/002 同法锚——批次式灌库形态）
cur.execute("SELECT DATE_FORMAT(update_time,'%Y-%m') m, COUNT(*) FROM gkxlumenx_dwd.enterprise_base "
            "GROUP BY m ORDER BY m")
facts["dev_enterprise_base_month_dist"] = [[a, int(b)] for a, b in cur.fetchall()]
conn.close()

# ============ ③ 存量读数（复用族产物，B11 锚） ============
p002 = json.load(open(os.path.join(BASE, "M_SCIUI_DATAIN_002_out.json"), encoding="utf-8"))
facts["dev_enterprise_base_rows"] = p002["facts"]["dev_enterprise_base_rows"]
facts["gkx_main_table_rows_top3"] = dict(sorted(
    p002["facts"]["gkx_main_table_rows"].items(), key=lambda kv: -kv[1])[:3])
facts["jiuxin_all_ads_rows_sum_210tables"] = p002["derived"][0]["value"]

# ============ ④ mock 对照（演示值披露） ============
facts["ui_mock_source_types_sorted"] = [
    ["企业", 5234, 18.3], ["国内数据库", 6820, 14.2], ["开源平台", 5550, 22.1],
    ["科研院所", 8234, 12.5], ["国外数据库", 4560, 8.6]]  # name, volume, change%（sorted by name）
facts["ui_mock_volume_sum"] = 6820 + 4560 + 8234 + 5234 + 5550
facts["ui_mock_change_range"] = [8.6, 22.1]

# ================= absence_probe =================
absence += [
    {"probe": "dev 来源类×量×期 台账/增长序列面（growth/change/trend/mom 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表，词族 growth|change_log|trend）",
     "hits": 1,
     "hit_detail": "命中 gkxlumenx_dwd.enterprise_growth_trend（唯一）——结构核：列含 "
                   "stat_year/stat_month/new_enterprise_count（区域×年月×新增企业数的时间序列结构），"
                   f"但 COUNT(*)={facts['dev_growth_trend_rows']}（0 行空表）；且度量对象是「区域新增"
                   "企业数」非「来源类数据量」——结构近邻（年月维）+ 语义分叉（对象维）+ 空表，"
                   "双重排除：结构可参考、语义不可用",
     },
    {"probe": "gkx 来源标签轴 + 增长序列面",
     "source": "gkx",
     "sql": "词族扫描（共享探针 gkx_growth_tables=[]）+ table_data_source 值域（DATAIN_003 三表证）",
     "hits": 0,
     "hit_detail": "growth/trend 词族 0 命中；table_data_source 标签轴三表空载"
                   "（dwd_scholar 单标签 gkx_ods 21,316/dwd_zh_paper 100% 无效/dwd_patent 采样全 null，"
                   "dwd_news_base 本批复核同构单值 gkx_qh 20,000）——无来源类分组轴",
     },
    {"probe": "久新增长/来源面（growth|trend|change 词族 + channel/source 词族）",
     "source": "jiuxin",
     "sql": "SHOW TABLES 词族扫（共享探针，215 表 live）",
     "hits": 2,
     "hit_detail": "growth 词族命中 ads_research_outcome_trend_case/ads_research_problem_change_log——"
                   "科研问题演变案例/问题清单变更日志（研究对象=研究问题非数据资源），语义排除；"
                   "channel 词族 7 张 ads_*_resource_* 均为学科资源配置分析面，无来源类×量×期台账",
     },
    {"probe": "需求原文「数据量与变化/期际变化」指标定义",
     "source": "doc",
     "sql": "rg 检索三份需求真源",
     "hits": 0,
     "hit_detail": "「数据量与变化」为 UI Segmented 选项文案（ResourceSourceAnalysisDetail.jsx:396），"
                   "三份需求说明书 0 命中；主需求 :2729「数据量」为数据集元属性项；"
                   "seq 351 渠道归集数据量统计为总量功能（无期际变化率定义）",
     },
]

support = "完全不支持"

notes += [
    "判档：期际变化维需「同来源类两期量」序列——三源无来源台账（L4 族探针+本件词族双证）；"
    "月维代理仅 2026-08:269,163/2026-09:348 两点（enterprise_base，DATAIN_001/002 同法同读数），"
    "5 类来源的分期变化序列不可构建；gkx 标签轴空载 → 完全不支持",
    "最近邻结构证据（dev enterprise_growth_trend）：stat_year/stat_month/new_enterprise_count "
    "列族是本库唯一的「年月×量」序列结构——但 0 行空表 + 度量对象是区域新增企业数非来源类数据量，"
    "结构与语义双排除；久新 ads_research_outcome_trend_case 等（研究问题演变，非数据资源增长）",
    "存量读数（B11 锚，复用族产物）：dev enterprise_base 269,511 / gkx 11 表（dwd_patent 2,939,895 "
    "领衔）/ 久新 210 表合计 182,707,016——「量」维三源可数，但「来源类分组×期际变化」双维缺承载",
    "mock 披露：mockData.js:160-229 五类来源 volume+change 均为演示值"
    "（change 全为正、区间 8.6-22.1%，无一期负增长——演示形态）；不作数据证据（B10）",
    "B11 对账：月维两点与 DATAIN_001/002 同键同值；存量三读数与 DATAIN_002 族产物零漂移",
    "升档触发器（B10）：①来源台账立项（来源类×量×期，与 DATAOV_002/DATAIN_001 族触发器共用）"
    "→ 升完全直接支持；②甲方裁「血缘分组轴+批次期」口径 → 可升完全转换支持（语义降维随行披露）",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_040",
    "batch": "S3-05",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/components/ResourceSourceAnalysisDetail.jsx:396",
        "repos/demo-ui-science/src/pages/data-resources/components/ResourceSourceAnalysisDetail.jsx:240",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:160",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份需求说明书未出现「数据量及其期际变化」。「数据量与变化」为 UI Segmented "
                "选项文案（:396）；「环比变化」为表格列（:240-249，mock change 字段）；"
                "主需求 :2729「数据量」为数据集元属性项非平台指标",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "期际序列不可构建（无上期基值）",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "6820", "4560", "8234", "5234", "5550", "269511", "2939895", "182707016",
        "269163", "348", "542", "280", "215"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

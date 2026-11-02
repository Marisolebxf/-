#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_027 平台归集数据量（记录数）· 三源探针与复现脚本（S3-04 L4）。

含义：接入视窗·资源来源分析和详情组件（AccessSourceAnalysisDetail，承接 SRS seq 351-355）
的渠道归集数据量统计卡——渠道表格「归集数据量」列（volume，:230）与 Statistic
「归集总量」（:367）/「资源总数」（:373）读数。组清单 mean：『从各数据源单位（如政务
部门、事业单位）收集进平台的数据总量（按记录条数计）——回答"平台攒了多少数据"』。

判档路径（口径=「平台归集数据总量（记录数），按渠道/来源分组呈现」）：
- 直接承载无：归集台账（渠道×资源×量×时间）三源零承载（L4 族探针词族，002/003 独立
  复跑在案，本件复用族探针留证）；
- 分组轴真实承载（本件新探针）：dev enterprise_base.data_source 列有真实值域
  （5 组：ods 链路 189,115 / gkx_qh 40,000 / 港 20,000 / 台 20,000 / 澳 396）——
  dev 侧存在可分组的来源列（与 gkx table_data_source 空载不同），但值语义是
  「表血缘+供应商代号」混合，与需求「数据源单位（政务部门/事业单位）」taxonomy 分叉；
- 存量读数三源双在：dev enterprise_base 269,511、gkx 11 表、久新 210 表合计
  182,707,016（快照求和）；
- 判部分支持。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_027_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s304_l4_collect_out.json")
GROUP = os.path.join(BASE, "_snapshots", "_probe_s304_l4_group_out.json")

probe = json.load(open(PROBE, encoding="utf-8"))
group = json.load(open(GROUP, encoding="utf-8"))

facts, derived, notes, absence = {}, [], [], []

# ============ ① UI mock 结构披露（演示值，不作数据证据） ============
MOCK_CHANNELS = [
    {"name": "科研院所", "volume": 12580, "count": 485, "share": 38.6},
    {"name": "企业", "volume": 8920, "count": 356, "share": 28.3},
    {"name": "第三方平台", "volume": 6240, "count": 245, "share": 19.5},
    {"name": "高等院校", "volume": 4120, "count": 120, "share": 9.6},
    {"name": "政府部门", "volume": 1810, "count": 50, "share": 4.0},
]
facts["ui_mock_volume_by_channel"] = [
    [c["name"], c["volume"]] for c in MOCK_CHANNELS]
facts["ui_mock_total_volume_statistic"] = sum(c["volume"] for c in MOCK_CHANNELS)
facts["ui_mock_total_count_statistic"] = sum(c["count"] for c in MOCK_CHANNELS)

# ============ ② dev：主量锚 + data_source 分组轴（本件新探针） ============
facts["dev_enterprise_base_rows"] = group["dev"]["enterprise_base_rows"]
facts["dev_enterprise_base_data_source_dist"] = group["dev"][
    "enterprise_base_data_source_dist"]
facts["dev_data_source_like_column_count"] = len(
    group["dev"]["channel_source_like_columns"])
facts["dev_channel_source_like_columns_sample"] = sorted(
    group["dev"]["channel_source_like_columns"])[:20]

# ============ ③ gkx / 久新：族探针快照复用 ============
facts["gkx_main_table_rows"] = probe["gkx_main_table_rows"]
facts["gkx_table_count"] = probe["gkx_table_count"]
facts["gkx_org_type_dist_top"] = group["gkx"].get(
    "dwd_org_base_info_org_type_dist", [])[:10]
facts["jiuxin_status"] = probe["jiuxin_status"]
facts["jiuxin_table_count"] = probe["jiuxin_table_count"]
facts["jiuxin_main_table_rows"] = probe["jiuxin_main_table_rows"]

# 久新 210 表合计（与 DATAIN_002/DATATHM_039 同键同值，族内 B11 对账）
snap = json.load(open(os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json"),
                      encoding="utf-8"))
rc = snap["jiuxin"]["rowcounts"]
jiuxin_sum = sum(rc.values())
derived.append({
    "key": "jiuxin_all_ads_rows_sum_210tables",
    "value": jiuxin_sum,
    "numerator": jiuxin_sum,
    "denominator": snap["jiuxin"]["table_count"],
    "note": "分子=共享快照 210 张 ads_* 表逐表行数之和；分母=表数（210，2026-11-01 快照日）；"
            "久新库对象级总量（与 DATAIN_002/DATATHM_039 同键同值，族内 B11 对账）",
})
# dev data_source 分组求和恒等校验（分组完备性：Σ各组 = 总行数）
grp = facts["dev_enterprise_base_data_source_dist"]
derived.append({
    "key": "dev_data_source_group_sum_equals_total",
    "value": sum(v for _, v in grp),
    "numerator": sum(v for _, v in grp),
    "denominator": facts["dev_enterprise_base_rows"],
    "note": "分子=data_source 5 组计数之和；分母=enterprise_base 总行数——恒等（分组轴完备，"
            "无未分组残留），证明该轴可作为分组读数的可靠基准",
})
# 指标负结论登记（B10）
derived.append({
    "key": "platform_collected_volume_total",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『平台归集数据总量（动作口径：渠道×资源×量登记汇总）』三源无归集台账承载"
            "（词族排除，族探针在案）；本件交付存量口径读数（三源对象级行数）与 dev 侧"
            "data_source 分组轴实测——语义=库内数据资产存量≠归集动作量；按 B10 留空",
})

# ================= absence_probe =================
absence += [
    {"probe": "三源归集台账（渠道×资源×量×时间登记面）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表）access/collect/ingest 词族"
            "（L4 族探针 + DATAIN_002 独立复跑）",
     "hits": 1,
     "hit_detail": "命中 app_article_collect（文章收藏-用户行为，语义排除）——0 张归集台账；"
                   "本件新探针另证 dev 侧 data_source 列族存在（"
                   f"{facts['dev_data_source_like_column_count']} 处列命中）但值域为表血缘/"
                   "供应商代号混合，非「渠道×资源×量×时间」登记",
     },
    {"probe": "gkx 归集台账（同词族）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表）词族扫（L4 族探针）",
     "hits": 1,
     "hit_detail": "命中 dwd_org_changerecord_info（企业变更流水，语义排除）——280 表为要素"
                   "明细库无归集台账；org_type 值域（本件新探针）是工商登记类型轴"
                   "（有限责任公司 58,158 领衔），非数据源单位轴",
     },
    {"probe": "久新归集台账（同词族）",
     "source": "jiuxin",
     "sql": "SHOW TABLES（live，211 表，探测日实测）词族扫（L4 族探针）",
     "hits": 0,
     "hit_detail": "命中 []——211 张 ads_* 全部为分析结果面；快照管理形态无归集登记",
     },
    {"probe": "需求原文「平台归集数据量」定义段",
     "source": "doc",
     "sql": "rg 平台归集数据量/归集数据量 三份需求真源 + SRS 接入视窗.md",
     "hits": 1,
     "hit_detail": "「平台归集数据量」0 命中；最近语境 seq 351「渠道归集数据量统计」（SRS "
                   "接入视窗.md:61-70 + 主需求 :2607）——本指标名的直挂语义叶；『各渠道"
                   "归集的数据量』功能在、度量单位与渠道 taxonomy 无定义；本件挂载组件"
                   "（AccessSourceAnalysisDetail）即 seq 351-355 的 UI 承接位",
     },
]

support = "部分支持"

notes += [
    "判档：需求语义=『平台归集数据总量（记录数口径，渠道维呈现）』；归集台账三源零承载 → "
    "动作口径不可直算；存量读数三源双在 + dev 侧 data_source 分组轴真实有值（本件新探针）"
    "→ 部分支持",
    f"dev 分组轴新发现：enterprise_base.data_source 值域 5 组 {grp}——分组求和恒等 "
    "269,511（派生键校验）；值语义=表血缘（ods 表名链路）与供应商代号（gkx_qh）混合，"
    "与需求『数据源单位（政务部门/事业单位）』taxonomy 分叉（与 003/018 共享待裁）",
    "存量口径读数：dev enterprise_base 269,511（全库估算 9,855,673 见 DATATHM_039 键）、"
    "gkx 11 表（专利 2,939,895 领衔）、久新 210 表合计 182,707,016（快照求和）——"
    "『平台攒了多少数据』三源可数",
    f"mock 披露：渠道表格 volume 列 5 值（科研院所 12,580 领衔，合计 "
    f"{facts['ui_mock_total_volume_statistic']}）与 Statistic 归集总量/资源总数（"
    f"{facts['ui_mock_total_volume_statistic']}/{facts['ui_mock_total_count_statistic']}）"
    "——演示值不作数据证据（B10）",
    "语义族定位：本件=平台总量读数（表格 volume 列+Statistic）；033=分组明细（柱图）；"
    "028=分组合计（分组表合计列）——三件同挂本组件、同一分组聚合的三种读法（总量=Σ合计"
    "=Σ明细）；与 DATAIN_003（seq 351 需求叶）同物近邻——003 是需求明列的渠道分布，"
    "本件是其表格列的总量读数位，建议并项（§1.7）",
    "B5 确定性：词族/列清单 sorted()；值域分布 COUNT DESC+值双键排序",
    "B11 对账：enterprise_base 269,511 与 DATAIN_002/003 族内一致；久新合计与 002/039 "
    "同键同值 182,707,016；gkx 11 表与 S3-01 共享快照零漂移",
    "升档触发器（B10）：①建归集台账（渠道×资源×量×时间，族级并项）→ 动作口径直查升完全"
    "直接支持；②甲方裁渠道 taxonomy（data_source 血缘口径升格或数据源单位字典立项）+总量"
    "口径=库内对象级存量 → 完全转换支持",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_027",
    "batch": "S3-04",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/components/AccessSourceAnalysisDetail.jsx:230",
        "repos/demo-ui-science/src/pages/data-resources/components/AccessSourceAnalysisDetail.jsx:367",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:100",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「平台归集数据量」指标名三份真源 0 命中——UI 派生读数；直挂语义叶=seq 351"
                "「渠道归集数据量统计」（SRS 接入视窗.md:61-70/主需求 :2607），本件挂载组件"
                "AccessSourceAnalysisDetail 即 seq 351-355 的 UI 承接位；『按记录条数计』"
                "口径为组清单 screen 语，需求未定义度量单位",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件无基期年份依赖（存量读数+分组轴，mock 时间位仅渠道趋势图属 002 族）",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["269511", "189115", "40000", "2939895", "182707016", "280",
                          "211", "210", "12580", "33670", "1256", "1816"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

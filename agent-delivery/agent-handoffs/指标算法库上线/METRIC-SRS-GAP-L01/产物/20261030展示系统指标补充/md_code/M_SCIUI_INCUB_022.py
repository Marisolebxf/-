#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INCUB_022 载体成果总览报表（汇总表）· 三源探针脚本（S3-07 L3）。

含义：软科学成果展示系统全局头的「成果总览报表」——报表模块配置清单中的第一项
（label 常量，非数值读数）。UI：ScienceGlobalHeader.jsx:7（REPORT_MODULE_OPTIONS
首项）。派单书 cat=无业务逻辑数值类。

判档路径（口径 = 成果总览报表的数据面：成果主档+统计聚合+报表配置三层）：
- dev：report 词族命中 22 表全为框架面（jimu_report 报表设计器 15 表/
  xxl_job_log_report 任务日志/policy_*_report 政策报告 0 行/ads.report 0 行）——
  无「成果统计报表」数据面；成果主档本身（软科学课题成果库）三源无承载
  （软科学成果是课题制报送面，dev/gkx/久新均无课题成果表）；
- gkx：report 词族命中 14 表全为 dwd_en_report（英文科技报告文献）——文献语义
  非成果报表语义，语义排除；
- 久新：report 词族 1 命中 ads_talent_media_report（人才媒体报道，语义排除）；
  ads_research_outcome_* 族（成果评价面 342 行）是「科研成果评价」语义最近邻，
  但其成果=科研产出（论文/专利侧）非软科学课题成果，且无报表配置面；
- UI 侧：组件内写死常量（REPORT_MODULE_OPTIONS），配置弹窗保存也是演示态
  （message.success「报表配置已保存（演示）」）；
- 判完全不支持（成果统计主档与报表配置面三源均无法构建；UI 位为导航配置项非数值）。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_INCUB_022_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s307_l3_incub_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")

facts, derived, notes, absence = {}, [], [], []
probe = json.load(open(PROBE, encoding="utf-8"))
snap = json.load(open(SNAP, encoding="utf-8"))

# ============ ① UI 层（配置项语义披露） ============
facts["ui_mount"] = "ScienceGlobalHeader.jsx:7（REPORT_MODULE_OPTIONS 首项 {key:'overview', label:'成果总览报表'}）"
facts["ui_module_options_full"] = [
    {"key": "overview", "label": "成果总览报表"},
    {"key": "domain-dist", "label": "领域分布报表"},
    {"key": "org-compare", "label": "机构对比报表"},
    {"key": "year-trend", "label": "年度趋势报表"},
    {"key": "topic-progress", "label": "课题进展报表"},
    {"key": "transfer-perf", "label": "转化绩效报表"},
]
facts["ui_comment_read"] = "组件注释实读：「演示数据：可配置的报表模块清单，正式环境由角色权限接口下发」"
facts["ui_save_behavior"] = "handleSaveReportConfig 保存后 message.success('报表配置已保存（演示）…')——配置无持久化后端，纯前端 state"
facts["ui_nature_note"] = "该 UI 位是报表配置清单的导航项（label 常量），非数值读数位——派单书 cat=无业务逻辑数值类按清单录入，语义层为「报表模块存在性配置」"

# ============ ② dev ============
dev = probe["dev"]
facts["dev_table_total"] = dev["table_total"]
facts["dev_report_word_tables"] = dev["word_report"]
snap_report_rows = {}
for sch in ["gkxlumenx_ads", "gkxlumenx_dwd", "gkxlumenx_job"]:
    for t, n in snap["dev"]["schemas"][sch]:
        if t in ("report", "policy_analysis_report", "policy_interpretation_report",
                 "policy_recommendation_report", "xxl_job_log_report"):
            snap_report_rows[f"{sch}.{t}"] = n
facts["dev_report_rows_snapshot"] = snap_report_rows
facts["dev_report_hits_note"] = ("report 词族 22 命中分层：jimu_report* 15 表=报表设计器框架面（拖拽设计/数据源配置，无成果统计语义）；"
                                 "ads.report/policy_*_report 3 表均 0 行；xxl_job_log_report 任务日志；ods.dwd_org_annual_report_* 机构年报——无一张是「成果总览统计」数据面")

# ============ ③ gkx ============
facts["gkx_table_count"] = probe["gkx"]["table_count"]
facts["gkx_report_word_tables"] = probe["gkx"]["word_hits"]["report"]
facts["gkx_hits_note"] = "report 词族 14 命中全为 dwd_en_report*（英文科技报告文献表族）——文献载体语义，非成果统计报表语义，语义排除"

# ============ ④ 久新 ============
jx = probe["jiuxin"]
facts["jiuxin_table_count_live"] = jx["table_count_live"]
facts["jiuxin_report_word_tables"] = jx["word_hits"]["report"]
facts["jiuxin_outcome_family_note"] = ("ads_research_outcome_* 族 20 表是「科研成果评价」最近邻（快照 rowcounts：profile 342/dimension 1368/metric 3420/"
                                       "yearly_metric 9055/scope_yearly 41153 等）——其成果=科研产出评价面（论文/专利侧指标），非软科学课题成果总览；无报表配置面")

# ============ ⑤ 需求溯源 ============
facts["srs_anchor"] = "SRS 软科学成果展示.md 序号 462「高级排序与筛选历史」/ 序号 470 附近「数据导出与报告管理」（成果报表导出需求）；主需求 :3241 软科学七功能含「数据导出与报告管理」"
facts["named_in_srs"] = False
facts["named_note"] = "「成果总览报表」指标名在三份说明书与主需求均未出现；语义锚为数据导出与报告管理功能族（报表模块存在性需求在案，总览报表口径无定义）"

# ============ ⑥ absence_probe ============
absence = [
    {"probe": "dev 成果总览统计报表面（report 词族，542 表）",
     "source": "dev", "sql": "information_schema.tables 扫 gkxlumenx_* + 行数快照",
     "hits": 22,
     "hit_detail": "分层全排除：jimu_report* 15 表报表设计器框架、ads.report 0 行、dwd.policy_analysis_report/policy_interpretation_report/policy_recommendation_report 0 行、job.xx_log_report 任务日志、bi.tmp_report_data 临时表——无成果统计聚合面"},
    {"probe": "dev 软科学课题成果主档（成果报表的数据底座）",
     "source": "dev", "sql": "词族+表清单语义扫（achievement/outcome/project/课题）",
     "hits": 0,
     "hit_detail": "dev 无软科学课题成果表——成果主档缺失则总览报表无从聚合（achievement_year/ods 0 行，enterprise_* 均企业面非课题成果）"},
    {"probe": "gkx 成果报表面（report 词族，280 表）",
     "source": "gkx", "sql": "information_schema.tables 扫 gkx",
     "hits": 14,
     "hit_detail": "全为 dwd_en_report*（英文科技报告文献）——文献语义排除；无课题成果/统计报表面"},
    {"probe": "久新成果报表面（report/outcome 词族，live 218 表复核）",
     "source": "jiuxin", "sql": "SHOW TABLES 词族过滤 + rowcounts 快照",
     "hits": 21,
     "hit_detail": "report 词族 1 命中 ads_talent_media_report（人才媒体报道）排除；ads_research_outcome_* 20 表为科研产出评价面（论文/专利侧），非软科学课题成果——语义均排除，无报表配置面"},
    {"probe": "需求原文「成果总览报表」定义段",
     "source": "doc", "sql": "rg 成果总览报表 三份说明书+主需求",
     "hits": 0,
     "hit_detail": "指标名 0 命中；SRS 数据导出与报告管理族（定制数据导出与自定义报告生成 序号 468 附近）要求报表可自定义导出，未定义总览报表内容口径；UI 位为配置清单导航项"},
]

# ============ ⑦ derived ============
derived = [
    {"key": "carrier_achievement_overview_report", "value": None, "numerator": None, "denominator": None,
     "note": "『载体成果总览报表』需「成果主档+统计聚合+报表配置」三层——dev report 词族全为框架/0 行面且无课题成果主档；gkx/久新语义排除；UI 位本身是配置导航项非数值 → 不可构建，按 B10 留空即负结论登记"},
]

notes = [
    "判档：三层依赖（成果主档/统计聚合/报表配置）三源均无有效承载 + UI 位是 label 常量配置项非数值读数 → 完全不支持",
    "语义辨析：dev jimu_report 15 表是报表『设计器』（BI 工具框架面，56 个 jimu_report 模板在库）——有报表工具无成果数据源，二者不能互替；gkx dwd_en_report 是英文科技报告『文献』（与 dwd_zh_paper 同族），非报表语义",
    "久新 ads_research_outcome_* 是本件最近邻（成果评价面 20 表）——但其口径是科研产出评价（dimension/metric/yearly 指标面），非软科学课题成果总览，语义排除已留证",
    "mock/演示披露：REPORT_MODULE_OPTIONS 6 项是组件内写死常量（注释自认『演示数据…正式环境由角色权限接口下发』），保存按钮 message 带「（演示）」字样——无后端",
    "同族件关系：INCUB_031（数据社区条目数）同挂 scienceGlobalHeaderMock/App 层配置面；SOFTSCI_009（转化效率趋势）同属软科学 trendSeries 族——共享「软科学课题成果面三源无承载」结论（本件独立留证）",
    "升档路径：软科学课题成果主档立项落库（课题/承担单位/立项年度/成果类型）→ jimu 报表设计器接成果数据源出总览报表 → 部分支持",
]

out = {
    "metric_id": "M_SCIUI_INCUB_022",
    "batch": "S3-07",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/achievement-preview/modules/soft-science/components/ScienceGlobalHeader.jsx:7",
        "repos/demo-ui-science/src/pages/achievement-preview/AchievementPreviewApp.jsx:555",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书未出现「成果总览报表」指标名；语义锚 SRS 软科学成果展示·数据导出与报告管理功能族（定制导出/自定义报告）+主需求 :3241",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": "完全不支持",
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["无年度基期维（报表配置项为当期导航存在性，非时序数值）"],
    "base_years_note": "本 UI 位是配置清单导航项非数值读数，无基期语义；非「缺年按 0 摊入」",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": ["6", "22", "14", "1", "20", "15", "56", "0", "542", "280", "218", "3241"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", OUT)
print("support_judgment:", out["support_judgment"])

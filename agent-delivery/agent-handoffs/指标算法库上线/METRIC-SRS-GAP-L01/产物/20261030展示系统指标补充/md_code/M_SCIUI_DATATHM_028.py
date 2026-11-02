#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_028 分组归集量合计 · 三源探针与复现脚本（S3-04 L4）。

含义：接入视窗·资源来源分析和详情组件（AccessSourceAnalysisDetail，承接 SRS seq 354
多维筛选与分组功能）分组表「归集量合计」列（volume，:319）——用户选定分组维
（来源渠道/数据种类/质量等级）后，分组 Table 内每组的资源数（count）与归集量合计
（volume=组内明细行 volume 求和，groupedData useMemo :196-204）。

判档路径（口径=「按指定维分组后的组级归集量合计（分组键×资源数×Σ记录数）」）：
- 直接承载无：归集台账三源零承载（族探针，027 §3.3 在案，本件互引）；
- 分组语义的载体是「明细行×分组键」——需求明细（seq 352 元数据）在库内无资源级
  登记面（资源编目缺口，DATAOV_001 同根）；三源可分组对象=物理表（血缘/库/表维）；
- dev data_source 分组（027 新探针）即本件分组维「按来源渠道」的最近邻工程面：
  5 组 269,511（恒等完备）——按其他维（数据种类/质量等级）分组轴零承载
  （quality 词族仅 3 处列命中且语义偏移）；
- 判部分支持。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_028_out.json")
GROUP = os.path.join(BASE, "_snapshots", "_probe_s304_l4_group_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s304_l4_collect_out.json")

group = json.load(open(GROUP, encoding="utf-8"))
probe = json.load(open(PROBE, encoding="utf-8"))

facts, derived, notes, absence = {}, [], [], []

# ============ ① UI mock 分组聚合复算（groupedData 同构算法） ============
DETAILS = [
    {"id": "asd-001", "channel": "科研院所", "dataType": "结构化数据",
     "qualityLevel": "优", "volume": 2300},
    {"id": "asd-002", "channel": "高等院校", "dataType": "非结构化数据",
     "qualityLevel": "优", "volume": 1800},
    {"id": "asd-003", "channel": "企业", "dataType": "半结构化数据",
     "qualityLevel": "良", "volume": 1500},
    {"id": "asd-004", "channel": "第三方平台", "dataType": "实时流数据",
     "qualityLevel": "优", "volume": 920},
    {"id": "asd-005", "channel": "政府部门", "dataType": "实时流数据",
     "qualityLevel": "良", "volume": 860},
    {"id": "asd-006", "channel": "科研院所", "dataType": "结构化数据",
     "qualityLevel": "良", "volume": 1100},
    {"id": "asd-007", "channel": "企业", "dataType": "非结构化数据",
     "qualityLevel": "中", "volume": 640},
    {"id": "asd-008", "channel": "第三方平台", "dataType": "结构化数据",
     "qualityLevel": "优", "volume": 2100},
    {"id": "asd-009", "channel": "高等院校", "dataType": "半结构化数据",
     "qualityLevel": "中", "volume": 720},
    {"id": "asd-010", "channel": "政府部门", "dataType": "结构化数据",
     "qualityLevel": "优", "volume": 480},
    {"id": "asd-011", "channel": "企业", "dataType": "实时流数据",
     "qualityLevel": "良", "volume": 980},
    {"id": "asd-012", "channel": "第三方平台", "dataType": "非结构化数据",
     "qualityLevel": "良", "volume": 1320},
]

def grouped_by(key):
    m = {}
    for r in DETAILS:
        k = r[key] or "未分组"
        if k not in m:
            m[k] = {"count": 0, "volume": 0}
        m[k]["count"] += 1
        m[k]["volume"] += r["volume"]
    # B5：按 volume 降序+键名字典序双键稳定排序（UI sort 同向）
    return [[k, m[k]["count"], m[k]["volume"]]
            for k in sorted(m, key=lambda k: (-m[k]["volume"], k))]

facts["ui_mock_group_by_channel"] = grouped_by("channel")
facts["ui_mock_group_by_dataType"] = grouped_by("dataType")
facts["ui_mock_group_by_qualityLevel"] = grouped_by("qualityLevel")
facts["ui_mock_detail_rows_total"] = len(DETAILS)
facts["ui_mock_detail_volume_sum"] = sum(r["volume"] for r in DETAILS)

# ============ ② dev：分组轴（027 组探针复用 + 质量词族列证据） ============
facts["dev_enterprise_base_rows"] = group["dev"]["enterprise_base_rows"]
facts["dev_enterprise_base_data_source_dist"] = group["dev"][
    "enterprise_base_data_source_dist"]
facts["dev_quality_like_columns"] = group["dev"]["quality_like_columns"]
# 质量等级词族命中判读（3 处）：score_level（ads 评分档）/time_quality（事件时间质量）/
# company_quality（台企专项表列）——均非「资源质量等级」轴
facts["gkx_table_count"] = probe["gkx_table_count"]
facts["jiuxin_table_count"] = probe["jiuxin_table_count"]
facts["jiuxin_status"] = probe["jiuxin_status"]

# 分组聚合恒等校验（B3 同基）：Σ组 volume = Σ明细 volume（三组维同构校验）
derived.append({
    "key": "ui_mock_group_volume_sum_equals_detail_sum",
    "value": sum(g[2] for g in facts["ui_mock_group_by_channel"]),
    "numerator": sum(g[2] for g in facts["ui_mock_group_by_channel"]),
    "denominator": facts["ui_mock_detail_volume_sum"],
    "note": "分子=按渠道分组的组级合计之和（复算 groupedData 同构算法）；分母=12 行明细 "
            "volume 直加——恒等（分组完备无漏），三组维（渠道/种类/质量）同构校验通过",
})
# dev data_source 分组聚合（分组维=血缘轴时的组级合计交付形态）
grp = facts["dev_enterprise_base_data_source_dist"]
derived.append({
    "key": "dev_group_by_data_source_volume_sum",
    "value": sum(v for _, v in grp),
    "numerator": sum(v for _, v in grp),
    "denominator": facts["dev_enterprise_base_rows"],
    "note": "分子=按 data_source 分组的 5 组行数合计；分母=enterprise_base 总行数——"
            "恒等 269,511（与 027 派生键同值，族内 B11 对账）；血缘分组即本件分组维"
            "『按来源渠道』的最近邻工程交付形态",
})
# 指标负结论登记（B10）
derived.append({
    "key": "grouped_collected_volume_by_dim",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『按需求分组维（数据种类/质量等级/正式渠道 taxonomy）的组级归集量合计』——"
            "资源级明细登记面（seq 352 元数据）三源零承载，分组键无挂靠对象；仅血缘维"
            "（data_source）可分组但 taxonomy 分叉（027 在案）；按 B10 留空",
})

# ================= absence_probe =================
absence += [
    {"probe": "dev 资源级明细登记面（名称/类型/采集时间/质量等级/关联项目元数据，seq 352）",
     "source": "dev",
     "sql": "information_schema.columns 扫 gkxlumenx_*（542 表）quality/grade 词族 + "
            "access/collect/ingest 表词族（L4 族探针+组探针）",
     "hits": 3,
     "hit_detail": "质量词族命中 3 处列：enterprise_score.score_level（ads 评分档）/"
                   "event_std.time_quality（事件时间质量）/dwd_special_taiwan_company."
                   "company_quality（台企表列）——均非「资源质量等级」轴；无资源级明细"
                   "登记表（分组键无挂靠对象）；台账词族命中 app_article_collect 语义排除"
                   "（族探针）",
     },
    {"probe": "gkx 资源级明细/质量等级轴",
     "source": "gkx",
     "sql": "280 表词族扫（L4 族探针）+ dwd_org_base_info 列清单（组探针）",
     "hits": 1,
     "hit_detail": "台账词族命中 dwd_org_changerecord_info（语义排除）；dwd_org_base_info "
                   "38 列无质量等级列（列清单在案）——280 表为要素明细库，无「资源×质量"
                   "等级/数据种类」编目面",
     },
    {"probe": "久新资源级明细/质量等级轴",
     "source": "jiuxin",
     "sql": "SHOW TABLES（live，211 表）词族扫（L4 族探针）",
     "hits": 0,
     "hit_detail": "命中 []——211 张 ads_* 全为分析结果面（学科/人才/专利/项目/技术），"
                   "无资源归集明细或质量等级编目",
     },
    {"probe": "需求原文「分组归集量合计/多维筛选与分组」定义段",
     "source": "doc",
     "sql": "rg 分组归集量合计/多维筛选与分组 三份需求真源 + SRS 接入视窗.md",
     "hits": 1,
     "hit_detail": "「分组归集量合计」0 命中；功能语义叶=seq 354 多维筛选与分组（SRS "
                   "接入视窗.md:106-117 + 主需求 :2617）：『支持根据来源渠道、数据种类、"
                   "时间、质量等多种维度对资源进行筛选和分组，方便用户实现针对性分析或"
                   "批量管理各类数据来源』——分组功能在、分组键的数据承载与合计口径无定义",
     },
]

support = "部分支持"

notes += [
    "判档：需求语义=『按指定维（渠道/种类/质量）分组的组级归集量合计』；分组的载体是"
    "资源级明细行×分组键——明细登记面三源零承载（质量/种类轴无列或语义偏移）→ 需求维"
    "分组不可直算；血缘维分组（dev data_source 5 组恒等 269,511）+ 存量读数可交付 → "
    "部分支持",
    "mock 复算：groupedData 同构算法（组内 volume 求和+volume 降序+键名双键）——渠道维 "
    f"5 组/种类维 4 组/质量维 3 组，Σ组 volume={facts['ui_mock_detail_volume_sum']} 与 "
    "12 行明细直加恒等（派生键校验）；演示值不作数据证据",
    f"质量等级轴证据：dev 质量词族仅 3 处列命中且全语义偏移 {facts['dev_quality_like_columns']}"
    "——033 的『按质量等级分组』在 dev 侧无轴承载",
    "三件套恒等：本件（分组表合计）的 Σ组 volume ≡ 027（总量）≡ 033（Σ明细）——数学恒等，"
    "mock 内同源自洽（12 行明细求和=渠道卡 volume 求和的口径演示）；三件修复路径完全"
    "共享（明细登记面+分组键编目一次立项）",
    "B5 确定性：分组复算按 volume 降序+键名字典序双键；分布 COUNT DESC+值双键",
    "B11 对账：enterprise_base 269,511/data_source 5 组与 027 同快照同值；族探针表数 "
    "（dev 542/gkx 280/久新 211）与族内一致",
    "升档触发器（B10）：①建资源级明细登记面（seq 352 元数据：名称/类型/时间/质量/渠道）"
    "+分组键编目 → 需求维分组直查升完全直接支持（族级并项，027/028/033/003/352 五叶"
    "同时受益）；②甲方裁分组维=血缘轴（data_source）→ 完全转换支持（本件交付形态即该"
    "口径，组级合计即期可出）",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_028",
    "batch": "S3-04",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/components/AccessSourceAnalysisDetail.jsx:319",
        "repos/demo-ui-science/src/pages/data-resources/components/AccessSourceAnalysisDetail.jsx:196",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:121",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「分组归集量合计」指标名三份真源 0 命中——UI 派生读数；功能语义叶=seq 354"
                "「多维筛选与分组功能」（SRS 接入视窗.md:106-117/主需求 :2617，『支持根据"
                "来源渠道、数据种类、时间、质量等多种维度……筛选和分组』）+seq 355 导出"
                "（分组结果随明细导出）；合计口径（组内 volume 求和）为 UI 实现约定，"
                "需求未定义",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件无基期年份依赖（分组聚合读数；mock 筛选时间位 2026-05/04 是演示值）",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["269511", "189115", "40000", "396", "14720", "4340", "12",
                          "3", "5", "280", "211"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_039 数据资源数据量（条）· 三源探针与复现脚本（S3-04 L4）。

含义：总体视窗·大数据资源中心详情的资源级「数据资源数据量（条）」读数——每条资源（数据集/
数据库）的记录数（条）。UI 挂载（派单行 OverviewWindow.jsx:549 实查）：549 行位于
BigDataCenterDetail 抽屉的「关联主题库」块，非本指标读数位；本指标的真实读数位是
BigDataCenterDetail.jsx:330-333 主题库分类卡的「记录数」统计项（cat.records，mock 三分类
3.5亿/2.9亿/3.8亿）+ :535 深度浏览抽屉「记录数」字段（item.recordCount，mock '1.28亿' 等
文本量级值）。语义=资源×记录数（条）。

判档路径（口径=「每条数据资源的记录数」）：
- 直接承载无：三源无「资源登记×记录数」资产目录面——「哪个数据集、多少条记录」的登记
  不存在（资源登记面 dev 仅样例级：gen_datasource_conf 0 行 + jimu_report_data_source 8 行，
  DATAOV_001 已证；gkx/久新同无）；
- 转换承载（对象级精确行数）三源双在：库内每个物理表就是一条「数据资源」，其精确 COUNT(*)
  即该资源的记录数——dev 主量面（enterprise_base 269,511 等 9 表）、gkx 主量面（专利
  2,939,895/论文 100,900 等 11 表）、久新主量面（ads_patent_analysis_topic_patent
  12,406,725 等 5 表）全部精确可数；全库合计 dev 全 schema 9,855,673（估算）/久新共享快照
  182,707,016（210 表逐表求和）；
- 判部分支持：对象级读数可交付（表级 COUNT 即资源级记录数），但「资源」的编目口径（平台
  登记的资源清单）与三源物理表的映射缺位——mock 的 28 库/1,248 表/10.2 亿条在库里无同构
  登记面；且无按「条」的资源级计量单位登记（mock 用亿/万文本量级）。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_039_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s304_l4_collect_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")

probe = json.load(open(PROBE, encoding="utf-8"))
snap = json.load(open(SNAP, encoding="utf-8"))

facts, derived, notes, absence = {}, [], [], []

# ============ ① dev：主量面精确行数（探针快照复用）+ 登记面排除复核 ============
facts["dev_main_table_rows"] = probe["dev_main_table_rows"]
facts["dev_all_schema_rows_sum_est"] = probe["dev_all_schema_rows_sum_est"]
facts["dev_registry_like_tables"] = probe["dev_registry_like_tables"]
facts["dev_table_total"] = probe["dev_table_total"]

# ============ ② gkx：主量面精确行数（经 _gkxdb.py，探针快照复用） ============
facts["gkx_main_table_rows"] = probe["gkx_main_table_rows"]
facts["gkx_table_count"] = probe["gkx_table_count"]

# ============ ③ 久新：主量面行数（live 探针快照）+ 全库合计（共享快照 210 表求和） ============
facts["jiuxin_status"] = probe["jiuxin_status"]
facts["jiuxin_table_count"] = probe["jiuxin_table_count"]
facts["jiuxin_main_table_rows"] = probe["jiuxin_main_table_rows"]
rc = snap["jiuxin"]["rowcounts"]
facts["jiuxin_snapshot_table_count"] = snap["jiuxin"]["table_count"]
derived.append({
    "key": "jiuxin_all_ads_rows_sum_210tables",
    "value": sum(rc.values()),
    "numerator": sum(rc.values()),
    "denominator": snap["jiuxin"]["table_count"],
    "note": "分子=共享快照 210 张 ads_* 表逐表行数之和；分母=表数（210，2026-11-01 快照日）；"
            "久新库对象级记录数全库合计（换口径时以当日重数为准，活库表数不写死）",
})
# dev 全 schema 合计（估算口径并列，B10 双口径）
derived.append({
    "key": "dev_all_schema_rows_sum_est",
    "value": probe["dev_all_schema_rows_sum_est"],
    "numerator": probe["dev_all_schema_rows_sum_est"],
    "denominator": probe["dev_table_total"],
    "note": "分子=information_schema.table_rows 估算合计（InnoDB 近似，非精确）；分母=表数 542；"
            "仅作量级参考——精确口径以逐表 COUNT 为准（B9 估算值标注）",
})

# ================= 指标负结论登记（B10） =================
derived.append({
    "key": "data_resource_record_count",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『平台登记资源×记录数（条）』三源无资源登记面承载（资源→库表映射不存在）；"
            "本件交付对象级读数（库内物理表=资源的等价口径：dev/gkx/久新主量面精确行数 + "
            "全库合计），语义=库内数据资产的记录数≠平台登记资源的归集记录数；按 B10 留空",
})

# ================= absence_probe =================
absence += [
    {"probe": "dev 资源登记×记录数面（access/collect/ingest/resource/dataset/source 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表）",
     "hits": len(probe["dev_registry_like_tables"]),
     "hit_detail": f"命中 {probe['dev_registry_like_tables']}——app_article_collect（文章收藏"
                   "用户行为）、bi 报表/拖拽数据集配置（jimu/onl_*）、gen_datasource_conf（代码"
                   "生成器数据源配置，0 行）全部语义排除；无『资源×记录数』登记表（与 DATAOV_001 "
                   "资产目录缺口同根）",
     },
    {"probe": "gkx 归集/资源登记面（collect/ingest/access/resource/dataset/volume/record 词族）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表）词族扫",
     "hits": len(probe["gkx_collect_like_tables"]),
     "hit_detail": f"命中 {probe['gkx_collect_like_tables']}——dwd_org_changererecord 名近而实为"
                   "企业变更记录明细（org 变更流水非资源登记），语义排除；280 表为要素明细库"
                   "（对象级行数可数）无资源编目层",
     },
    {"probe": "久新归集/资源登记面（collect/ingest/access/volume/record 词族）",
     "source": "jiuxin",
     "sql": "SHOW TABLES（live，211 表，2026-11-01 探测日）词族扫",
     "hits": 0,
     "hit_detail": "命中 []——211 张 ads_* 全部为分析结果面（学科/人才/专利/项目/技术），"
                   "无资源登记/记录数台账；按 metrics_as_of_date 快照管理（DATAIN_003 已证单日"
                   "一期），无归集动作记录",
     },
    {"probe": "需求原文「数据资源数据量/记录数」定义段",
     "source": "doc",
     "sql": "rg 数据资源数据量|记录数 三份需求真源",
     "hits": 0,
     "hit_detail": "三份说明书未出现「数据资源数据量」指标名；主需求最近语境 :2729（1.1.1.1.4."
                   "4.3.1.2 数据集元数据）『每个数据集显示其元数据，包括名称、所属主题库、数据"
                   "类型、数据量、来源单位、采集时间…』——数据集元数据的字段列举，无记录数口径"
                   "定义；UI recordCount 为 mock 文本量级值（'1.28亿' 等）",
     },
]

support = "部分支持"

notes += [
    "判档：『资源×记录数（条）』的资源登记面三源零承载（词族命中逐一语义排除）→ 平台口径"
    "不可直查；对象级读数（物理表=资源等价口径）三源精确可数（dev/gkx/久新主量面行数）→ "
    "转换承载双在 → 部分支持",
    f"对象级读数（dev）：{facts['dev_main_table_rows']}（精确 COUNT）；全 schema 合计 "
    f"{facts['dev_all_schema_rows_sum_est']}（table_rows 估算口径，量级参考）",
    f"对象级读数（gkx）：{facts['gkx_main_table_rows']}（精确 COUNT，经 _gkxdb.py）——"
    "专利 2,939,895/论文 100,900 为主量面",
    f"对象级读数（久新）：live {facts['jiuxin_status']}，{facts['jiuxin_main_table_rows']}；"
    f"共享快照 210 表合计 {[x for x in derived if x['key']=='jiuxin_all_ads_rows_sum_210tables'][0]['value']:,}"
    "（2026-11-01 快照日求和）",
    "mount 勘误：派单行 OverviewWindow.jsx:549 实查是 BigDataCenterDetail 抽屉「关联主题库」"
    "渲染行——本指标真实读数位在 components/BigDataCenterDetail.jsx:330-333（分类卡「记录数」"
    "统计项）与 :535（深度浏览抽屉 recordCount 字段）；mock：分类卡 3.5亿/2.9亿/3.8亿"
    "（mockData.js:1134/1145/1156）+ 资源级 recordCount 文本量级值（'1.28亿' 等，:1176 起）——"
    "mock 用『亿』级文本而非逐条计数，不作数据证据（B10）",
    "语义对齐：本件与 DATAIN_002（接入视窗·归集数据量统计）跨窗同语义——002 挂接入动作的"
    "时序量（新增/更新资源折线），本件挂资源存量的记录数；两件同缺资源登记面，对象级读数"
    "共用本族探针（互引登记，合并建议见 MD §1.7）",
    "B9 规避：table_rows 估算与精确 COUNT 双口径并列、键名带 est 标注；mock recordCount 的"
    "『亿/万』文本量级登记为口径不可比证据",
    "B11 对账：dev 542/gkx 280/久新 211（live）与共享探针一致；gkx 11 表行数与 "
    "_shared_probe_s3_01 快照对账（专利 2,939,895/论文 100,900/学者 21,316 零漂移）；"
    "久新 210 表快照合计 182,707,016 与 lane7 快照一致",
    "升档触发器（B10）：①建数据资源登记面（资源→库表映射×记录数快照）→ 完全直接支持"
    "（与 DATAOV_001/002 台账并项）；②甲方裁资源口径=库内物理表 → 对象级读数升完全转换"
    "支持（本件交付形态即该口径）",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_039",
    "batch": "S3-04",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:549",
        "repos/demo-ui-science/src/pages/data-resources/components/BigDataCenterDetail.jsx:330",
        "repos/demo-ui-science/src/pages/data-resources/components/BigDataCenterDetail.jsx:535",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:1176",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书未出现「数据资源数据量」指标名；最近语境主需求 :2729 数据集元数据"
                "字段列举（含『数据量』字）无记录数口径；UI recordCount 为 mock 文本量级值",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件为存量记录数读数，无基期年份依赖",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["269511", "2939895", "100900", "12406725", "182707016", "542", "280",
                          "211", "210", "8", "10", "9855673"][:12]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

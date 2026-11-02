#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_056 平台覆盖资源数 · 三源探针脚本（S3-05 L2 资源计数组）。

含义：应用视窗·累计调用与趋势分析·汇总卡「覆盖资源数」（resourceCovered 30,398 个）——
被调用行为覆盖到的资源去重计数（COUNT(DISTINCT resource) 调用流水口径）。
挂载：CumulativeCallTrendAnalysis.jsx:151（Statistic title="覆盖资源数" resourceCovered）。
mock 源：mockData.js:863-896 cumulativeCallAnalysis.summary.resourceCovered=30398
（与 overviewKPIs「资源总量 30,398 个」同值——mock 自证「覆盖资源数=资源总量」，口径混同披露）。
需规锚：组件注释自标「需规 seq 346」（归集上线以来累计调用量，按时间区段分析热度与生命周期）。

判档路径（口径=「存在调用记录的资源去重计数」——调用流水的聚合读数）：
- 调用流水面（谁在何时调用了什么资源）三源零承载（L4/L5 族先例：DATAOV_002/DATAIN 族已结论
  接入/调用流水台账三源未立项；L4 探针 registry/volume 词族命中均为 BI 报表配置/文章收藏，语义排除）；
- 降档不到底：调用流水缺位不阻断「资源总量」侧近似（036 件先例：三源表计数多口径
  542+280+210=1,032/剔备份 930——若甲方裁定「覆盖≈总量」可近似交付，但语义不等价：
  覆盖=被调用过的资源（流量语义），总量=登记在库的资源（存量语义）；
- mock 自证口径混同：resourceCovered 30398 = overviewKPIs 资源总量 30398——演示作者把
  流量读数直接抄了存量值，恰证明流水不存在时只能抄总量；
- 判部分支持（存量近似可交付、流量口径无承载——语义边界须裁定）。

B11 锚：三源表数 542/280/210；L4 探针 = _probe_s304_l4_collect_out.json；036 计数 = M_SCIUI_DATATHM_036_out.json。
"""
import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_056_out.json")
SNAP7 = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
L4 = os.path.join(BASE, "_snapshots", "_probe_s304_l4_collect_out.json")
M036 = os.path.join(BASE, "M_SCIUI_DATATHM_036_out.json")
MOCK = "/Users/samuel_tang/my_project/gkx-lumen/repos/demo-ui-science/src/pages/data-resources/mockData.js"

snap = json.load(open(SNAP7, encoding="utf-8"))
l4 = json.load(open(L4, encoding="utf-8"))
m036 = json.load(open(M036, encoding="utf-8"))
mock_src = open(MOCK, encoding="utf-8").read()

# mock 读数实算
cca = re.search(r"export const cumulativeCallAnalysis = \{(.*?)\n\};", mock_src, re.S).group(1)
resource_covered = int(re.search(r"resourceCovered: (\d+)", cca).group(1))  # 30398
total_since_launch = int(re.search(r"totalSinceLaunch: (\d+)", cca).group(1))  # 2856000
kpi = re.search(r"label: '资源总量', value: '([\d,]+)'", mock_src).group(1).replace(",", "")
overview_total = int(kpi)  # 30398 — mock 口径混同实证

# 036 件计数复用（B8 不复收）
f036 = m036["facts"]
dev_total = 542
gkx_total = f036["gkx_table_count"]                    # 280
gkx_backup = f036["gkx_backup_like_table_count"]       # 99
dev_backup = len(f036["dev_backup_like_tables_sorted"])  # 3
jiuxin_total = 210
all_count = dev_total + gkx_total + jiuxin_total        # 1032
dedup_backup = all_count - gkx_backup - dev_backup      # 930

facts = {
    # 三源表数（B11 锚 + 036 复用）
    "dev_table_count": dev_total,
    "gkx_table_count": gkx_total,
    "jiuxin_table_count": jiuxin_total,
    "gkx_backup_like_table_count": gkx_backup,
    "dev_backup_like_table_count": dev_backup,
    "three_source_table_all": all_count,          # 1032
    "three_source_table_dedup_backup": dedup_backup,  # 930
    "count_source": "M_SCIUI_DATATHM_036_out.json（B8 复用，非本件重跑）",
    # 调用流水承载（L4 探针复用——语义排除证据）
    "dev_registry_like_tables": l4["dev_registry_like_tables"],  # 6 张 BI/收藏配置面
    "dev_registry_semantic_note": "app_article_collect=文章收藏、jimu_report_data_source/onl_drag_dataset_*=BI 报表数据源配置、gen_datasource_conf=代码生成器数据源配置——均非调用流水，语义排除",
    "gkx_collect_like_tables": l4["gkx_collect_like_tables"],  # [dwd_org_changerecord_info]
    "gkx_collect_semantic_note": "dwd_org_changerecord_info=机构变更记录（要素明细），非调用流水——语义排除",
    "jiuxin_status": "调用流水词族三源 0 命中（L4/L5 族先例：DATAOV_002/DATAIN 族已结论流水台账未立项）",
    # UI 挂载证据
    "ui_mount_summary_card": "CumulativeCallTrendAnalysis.jsx:150-152 汇总卡（Statistic title=覆盖资源数 value=resourceCovered suffix=个）",
    "ui_mount_context": "同排四卡：上线以来累计调用 285.6 万次/覆盖资源数/日均调用 85,600 次/热度生命周期——seq 346 累计调用语境",
    "ui_mock_resource_covered": resource_covered,     # 30398
    "ui_mock_total_since_launch": total_since_launch,  # 2856000
    "ui_mock_overview_total": overview_total,          # 30398
    # 口径混同披露
    "ui_mock_conflation_note": "resourceCovered 30398 与 overviewKPIs 资源总量 30398 同值——mock 作者把流量读数直接抄了存量值，"
                               "自证调用流水不存在时只能抄总量（覆盖=被调用过的资源·流量语义 ≠ 总量=登记在库·存量语义）",
}

derived = [{
    "key": "platform_covered_resource_count",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『覆盖资源数』= 调用流水去重资源计数（COUNT(DISTINCT resource_id)）——调用流水面三源零承载"
            "（registry/collect 词族命中均为 BI 配置/收藏/要素明细，语义排除）。存量近似读数可交付"
            "（036 件三源表计数 1,032/剔备份 930）但语义不等价，须甲方裁定。按 B10 留空即负结论登记",
}]

absence_probe = [
    {"probe": "dev 调用流水/资源登记面（registry/collect/call/usage 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表，L4 探针 2026-11-01 实跑）",
     "hits": 0,
     "hit_detail": "registry 词族 6 张命中全为 BI 报表数据源配置（jimu_report_data_source 等）/文章收藏"
                   "（app_article_collect）/代码生成器配置（gen_datasource_conf）——语义排除后 0；无调用流水表"},
    {"probe": "gkx 调用流水面（collect/call/usage 词族）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表）词族扫（经 _gkxdb.py，L4 探针）",
     "hits": 0,
     "hit_detail": "collect 词族唯一命中 dwd_org_changerecord_info（机构变更记录——要素明细非流水），语义排除后 0"},
    {"probe": "久新调用流水面（同词族）",
     "source": "jiuxin",
     "sql": "SHOW TABLES（L4 探针 211 表/live 212 表）词族扫",
     "hits": 0,
     "hit_detail": "ads_* 无调用流水表（分析面按主题切分）；resource 词族 7 张命中均为科技资源配置/瓶颈语义"
                   "（subfield_resource/research_resource_shortage 等——科技资源≠数据资源调用），语义排除"},
    {"probe": "需求原文覆盖资源数定义段",
     "source": "doc",
     "sql": "rg 覆盖资源|资源覆盖 三份需求真源",
     "hits": 0,
     "hit_detail": "三份说明书未出现「覆盖资源数」字面；语义锚 seq 346「累计调用量，按时间区段分析热度与生命周期」"
                   "——覆盖资源数是累计调用语境的衍生卡，未单独立项；口径（覆盖判据=至少一次调用？）无定义"},
]

notes = [
    "判档：覆盖资源数是调用流水的去重计数读数——流水面三源零承载（流量口径无承载）；"
    "但存量侧资源计数可近似交付（036 件先例 1,032/剔备份 930）——流量缺位+存量近似 ⇒ 部分支持",
    "语义边界（本件核心口径发现）：覆盖=被调用过的资源（流量子集）≠ 总量=登记在库（存量全集）——"
    "mock 自证混同（resourceCovered 30398 直接抄 overviewKPIs 资源总量 30398），演示作者都只能在无流水时抄存量值",
    "UI 语义核：覆盖资源数卡在 seq 346 累计调用语境的四卡排（累计调用/覆盖资源/日均调用/热度生命周期）——"
    "四卡共享同一流水前提（缺流水则四卡连坐：本件+057 资源调用频率共缺）",
    "近似读数口径（若甲方裁定覆盖≈总量）：全口径 1,032 张表（542+280+210）/剔备份口径 930 张"
    "（036 件发现 gkx 99 张 bak/v3bad + dev 3 张 tmp/copy）——但表数≠资源数（一资源可多表），须再乘资源-表映射",
    "B11 对账：三源表数 542/280/210 与 lane7 快照/036 件逐键一致；L4 探针 registry/collect 词族与 DATAOV_002/DATAIN 族先例零漂移",
    "升档触发器（B10）：①调用流水台账立项（网关日志/调用登记）→ COUNT(DISTINCT resource_id) 直查"
    "→ 升完全直接支持；②甲方裁定「覆盖≈总量」+资源-表映射登记 → 存量近似转正 → 升完全转换支持"
    "（须登记映射规则）；③维持现状 → 部分支持（UI 建议改挂存量口径或「暂无数据」）",
    "权威口径参照（GB/T 33850-2017 信息技术服务 监控）：服务调用的覆盖面统计以调用记录为准——流量语义的国标锚",
]

support = "部分支持"

out = {
    "metric_id": "M_SCIUI_DATATHM_056",
    "batch": "S3-05",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/components/CumulativeCallTrendAnalysis.jsx:151",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:867",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书未出现「覆盖资源数」字面；语义锚 seq 346「累计调用量，按时间区段分析热度与生命周期」"
                "——覆盖资源数是累计调用语境的衍生卡；覆盖判据（至少一次调用？）无定义",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["调用流水时间序列整体缺承载（覆盖数无期次可算）"],
    "base_years_note": "覆盖数为流水快照的去重读数；月/季度期次序列（periods 维）无库内承载",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["542", "280", "210", "1032", "930", "99", "30398", "2856000", "151", "346"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

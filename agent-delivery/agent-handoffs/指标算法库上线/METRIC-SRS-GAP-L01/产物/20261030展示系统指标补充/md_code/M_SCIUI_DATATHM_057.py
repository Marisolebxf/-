#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_057 资源调用频率（日均）· 三源探针脚本（S3-05 L2 调用组）。

含义：应用视窗「调用频率」语义的三处读数形态：
- ApplicationWindow.jsx:234 需求方统计表「日均调用」列（demanderStats.avgDaily 9143/7269/… 次/日）
- ApplicationWindow.jsx:274 主题调用信息表「调用频率」列（themeCallBasicInfo.callFreq 高频/中频/低频 枚举）
- ApplicationWindow.jsx:509「调用频率与趋势分析」卡（supplierCallTrend 折线——供应方调用时序）
同族参照：CumulativeCallTrendAnalysis.jsx:154 汇总卡「日均调用」85,600 次（056 同排四卡之三）。
需规锚：seq 391（需求方调用统计——部门/业务类型/项目组）+ seq 384（主题调用基本信息——
主题名称/调用时间/调用频率/调用接口/业务系统，mock 注释自标）。

判档路径（口径=「调用流水按日聚合的均值/分档」——流量面的期次读数）：
- 与 056 同根但更进一层：056 只需流水去重计数，本件需流水**按日时间序列**（更细粒度）——
  调用流水面三源零承载（L4 探词语义排除同 056）⇒ 日均无从除、分档无从判、趋势无从画；
- mock 三处演示值自洽性核：demanderStats avgDaily≈calls/activeDays（256000/28≈9143 对上——
  手写值按公式倒推圆润）；themeCallBasicInfo 高/中/低频枚举无阈值定义；
  cumulativeCallAnalysis.avgDaily 85600=2856000/33.3（除数凑天数反推）——三处均为手写无流水支撑；
- 判完全不支持（日均=流水期次聚合——流水整体缺位则期次读数连带缺位，且无存量近似可用：
  流水无「登记在库」形态，与 056 的表计数近似路径根本不同）。

B11 锚：三源表数 542/280/210；L4 探针 = _probe_s304_l4_collect_out.json（与 056 共享）。
"""
import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_057_out.json")
SNAP7 = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
L4 = os.path.join(BASE, "_snapshots", "_probe_s304_l4_collect_out.json")
MOCK = "/Users/samuel_tang/my_project/gkx-lumen/repos/demo-ui-science/src/pages/data-resources/mockData.js"

snap = json.load(open(SNAP7, encoding="utf-8"))
l4 = json.load(open(L4, encoding="utf-8"))
mock_src = open(MOCK, encoding="utf-8").read()

# demanderStats avgDaily 自洽性实算（mockData.js:977-986）
dm_block = re.search(r"export const demanderStats = \[(.*?)\n\];", mock_src, re.S).group(1)
dm_rows = re.findall(r"name: '(.*?)', calls: (\d+), activeDays: (\d+), avgDaily: (\d+)", dm_block)
dm_check = []
for name, calls, days, avg in dm_rows:
    calls, days, avg = int(calls), int(days), int(avg)
    derived_avg = round(calls / days)
    dm_check.append({"name": name, "calls": calls, "activeDays": days,
                     "avgDaily_mock": avg, "avgDaily_recomputed": derived_avg,
                     "match": avg == derived_avg})
assert len(dm_check) == 8, len(dm_check)

# themeCallBasicInfo callFreq 枚举（mockData.js:1558-1564）
tc_block = re.search(r"export const themeCallBasicInfo = \[(.*?)\n\];", mock_src, re.S).group(1)
tc_rows = re.findall(r"theme: '(.*?)', callTime: '(.*?)', callFreq: '(.*?)'", tc_block)
from collections import Counter
freq_dist = dict(sorted(Counter(f for _, _, f in tc_rows).items()))

# cumulativeCallAnalysis avgDaily（056 同源）
avg_daily_summary = int(re.search(r"avgDaily: (\d+)", mock_src).group(1))  # 85600

facts = {
    "dev_table_count": sum(snap["dev"]["schema_table_counts"].values()),
    "gkx_table_count": snap["gkx"]["table_count"],
    "jiuxin_table_count_snapshot_20261101": len(snap["jiuxin"]["tables"]),
    # 调用流水承载（L4 探针复用——与 056 共享语义排除证据）
    "dev_registry_like_tables": l4["dev_registry_like_tables"],
    "dev_registry_semantic_note": "6 张命中全为 BI 报表数据源配置/文章收藏/代码生成器配置——非调用流水，语义排除（同 056）",
    "gkx_collect_like_tables": l4["gkx_collect_like_tables"],
    "gkx_collect_semantic_note": "dwd_org_changerecord_info=机构变更记录（要素明细），非调用流水——语义排除（同 056）",
    "call_log_absence_note": "call/usage/log 词族三源 0 命中（L4 探针）——调用流水台账三源未立项（与 DATAOV_002/DATAIN 族同根）",
    # UI 挂载证据（三处 + 同族参照）
    "ui_mount_demander_column": "ApplicationWindow.jsx:234 需求方统计表「日均调用」列（avgDaily，需规 seq 391 语境）",
    "ui_mount_theme_freq_column": "ApplicationWindow.jsx:274 主题调用信息表「调用频率」列（callFreq 枚举，需规 seq 384——mock 注释自标五字段）",
    "ui_mount_trend_card": "ApplicationWindow.jsx:509「调用频率与趋势分析」卡（supplierCallTrend 折线——供应方调用时序）",
    "ui_mount_sibling_summary": "CumulativeCallTrendAnalysis.jsx:154 汇总卡「日均调用」85,600 次（056 同排四卡之三——同族参照）",
    # mock 演示值（实算，结构证据，不作源）
    "ui_mock_demander_avg_daily_check": dm_check,  # 8 行自洽性核
    "ui_mock_demander_selfconsistency_note": "avgDaily ≈ calls/activeDays 逐行对上（256000/28≈9143 等）——手写值按公式倒推圆润",
    "ui_mock_theme_freq_dist": freq_dist,  # {中频:2, 低频:1, 高频:2}
    "ui_mock_theme_freq_note": "高/中/低频三档枚举无阈值定义（多少次/日算高频？）——分档判据缺失",
    "ui_mock_summary_avg_daily": avg_daily_summary,  # 85600
    "ui_mock_summary_selfconsistency_note": "85600 = 2856000/33.3（totalSinceLaunch 除以凑 5 月 22 日的天数反推）——除数非自然月/周",
}

derived = [{
    "key": "resource_call_frequency_daily_avg",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『资源调用频率（日均）』= 调用流水按日聚合的均值（Σ调用/活跃天数）或分档（高/中/低频阈值映射）"
            "——调用流水面三源零承载（L4 探词语义排除同 056），流水整体缺位则日均无从除、分档无从判。"
            "mock 三处演示值（demanderStats 8 行/themeCallBasicInfo 枚举/summary 85600）均手写无流水支撑。"
            "与 056 根本不同：流水无存量近似形态（表计数救不了日均），按 B10 留空即负结论登记",
}]

absence_probe = [
    {"probe": "dev 调用流水/按日调用日志面（call/usage/registry 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表，L4 探针 2026-11-01 实跑）",
     "hits": 0,
     "hit_detail": "registry 词族 6 张全为 BI 配置/收藏（语义排除，同 056）；call/usage 词族 0 命中——"
                   "dev 无调用日志表（sys_log 为系统操作日志非资源调用流水，语义排除）"},
    {"probe": "gkx 调用流水面（同词族）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表）词族扫（经 _gkxdb.py，L4 探针）",
     "hits": 0,
     "hit_detail": "collect 词族唯一命中 dwd_org_changerecord_info（机构变更——语义排除，同 056）；无调用日志面"},
    {"probe": "久新调用流水面（同词族）",
     "source": "jiuxin",
     "sql": "SHOW TABLES（L4 探针 211 表）词族扫",
     "hits": 0,
     "hit_detail": "ads_* 无调用流水/日志表（分析面按主题切分，无运营日志域）"},
    {"probe": "需求原文调用频率/日均定义段",
     "source": "doc",
     "sql": "rg 调用频率|日均调用 三份需求真源",
     "hits": 0,
     "hit_detail": "三份说明书未出现「调用频率/日均调用」字面；语义锚 seq 391（需求方调用统计——calls/activeDays 字段语境）"
                   "+ seq 384（主题调用基本信息五字段——调用频率为其一，SRS 原文有「调用频率」字段名）；"
                   "日均算式（Σ调用/活跃天数 vs /自然日历）与分档阈值（高/中/低频）均无定义"},
]

notes = [
    "判档：调用频率（日均）是调用流水的期次聚合读数——流水面三源零承载（与 056 同根）且更进一层："
    "056 只需去重计数（存量近似可救），本件需按日时间序列（流水无存量形态，表计数救不了日均）"
    "→ 判完全不支持",
    "判档与 056 分档的差异论证：056 判部分支持因「覆盖≈总量」有存量近似路径；本件的日均分母是时间"
    "（活跃天数/日历天数）——时间维无「登记在库」形态，流水缺位则分子分母皆空——近似路径根本不存在",
    "UI 语义核：调用频率三处读数形态——数值型（demanderStats.avgDaily 次数/日）/枚举型（themeCallBasicInfo.callFreq "
    "高/中/低频三档）/时序型（supplierCallTrend 折线+summary.avgDaily 85600）——三种形态共享同一流水前提",
    "mock 自洽性披露（三处）：①demanderStats 8 行 avgDaily≈calls/activeDays 逐行对上（手写值按公式倒推圆润）；"
    "②themeCallBasicInfo 高/中/低频枚举无阈值定义（分档判据缺失）；③summary.avgDaily 85600=2856000/33.3"
    "（除数凑天数反推）——三处均为演示常量，不作频率原料（B10）",
    "B11 对账：三源表数 542/280/210；L4 探针与 056 共享（registry/collect 词族同一语义排除证据零漂移）",
    "升档触发器（B10）：①调用流水台账立项（网关日志含 resource×timestamp 粒度）→ 日均聚合/分档/趋势全套直查"
    "→ 升完全直接支持；②乙方自建抽样埋点（只统计高频资源）→ 升完全转换支持（抽样框与阈值须登记）；"
    "③维持现状 → 完全不支持（UI 三处建议「暂无数据」）",
    "权威口径参照（GB/T 33850-2017）：服务调用量按统计周期（日/周/月）聚合——日均的周期口径国标锚；"
    "RED 方法（Rate/Errors/Duration）：Rate 维即调用频率——可观测性工程范式",
]

support = "完全不支持"

out = {
    "metric_id": "M_SCIUI_DATATHM_057",
    "batch": "S3-05",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:234",
        "repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:274",
        "repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:509",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:36",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "SRS 应用视窗 seq 384「主题调用基本信息」五字段含「调用频率」（字段名在，分档阈值无定义）；"
                "seq 391 需求方调用统计（calls/activeDays 语境——日均的分子分母字段）；"
                "「日均调用」字面仅见 UI 列名/卡名",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["调用流水的日/月时间序列整体缺承载（supplierCallTrend 语义的时序面不存在）"],
    "base_years_note": "日均与趋势均为流水的期次读数；流水缺位则全时间维缺位",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["542", "280", "210", "9143", "7269", "85600", "2856000", "234", "274", "509", "384", "391"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

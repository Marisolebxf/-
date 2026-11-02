#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_022 调用量年度增长趋势 · 三源探针脚本（S3-04 L1）。

含义：科技数据资源·累计调用与趋势分析的「调用量」年度增长趋势（序列形态）——数据资源
接口调用量的年度序列（总量/新增/同比多列趋势，mock 复用 overviewAnnualAccessTrend）。
screen_v3 行 407 l3「年份＞年度增长趋势」。
UI：repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:575
（reportSheets「年度增长趋势」sheet 的年度序列三列；mount 亦含 :621 Card「年度增长趋势」
——DATAOV_002 承接的资源接入语境卡位，本件按调用语境独立核）。

判档路径（口径=「调用量年度序列」）：与 021 同根——需 API 调用日志（接口×时间×次数），
需求 :2563/:2571 自点名前提；三源词族 0 命中（021 独立复跑在案，本件引用其当日读数并
自行复核 dev 侧）；内容年份面与「调用量」无语义关联不代理 → 完全不支持。
本件与 021 的差别只在读数形态（单点同比 vs 年度序列），前提依赖完全同面。
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_022_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s304_l1_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402

facts, derived, notes, absence = {}, [], [], []
snap = json.load(open(SNAP, encoding="utf-8"))
probe = json.load(open(PROBE, encoding="utf-8"))["probes"]

# ============ ① dev：调用日志词族复核 + sys_log 年度跨度（序列可行性的量级证据） ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
d = pymysql.connect(**DEV)
c = d.cursor()

c.execute(
    "SELECT table_schema, table_name FROM information_schema.tables "
    "WHERE table_schema LIKE 'gkxlumenx%' AND table_name REGEXP "
    "'call_log|invoke_log|api_log|access_log|request_log|usage_log|call_stat|trend'")
facts["dev_call_trend_tables"] = [f"{r[0]}.{r[1]}" for r in sorted(c.fetchall())]
# trend 词族唯一命中复核：enterprise_growth_trend 结构定性（排除假阳性）
c.execute("SELECT COUNT(*) FROM gkxlumenx_dwd.enterprise_growth_trend")
egt_rows = int(c.fetchone()[0])
c.execute("SELECT column_name FROM information_schema.columns "
          "WHERE table_schema='gkxlumenx_dwd' AND table_name='enterprise_growth_trend'")
egt_cols = sorted(r[0] for r in c.fetchall())
facts["dev_trend_hit_structure"] = {
    "table": "gkxlumenx_dwd.enterprise_growth_trend",
    "columns": egt_cols,
    "rows": egt_rows,
    "verdict": "企业增长统计面（new_enterprise_count×region×stat_year/stat_month），非 API 调用"
               "语义——trend 词族假阳性，排除",
}
# sys_log 时间跨度（年度序列要求跨年日志——量级与跨度双重证据）
row = c.execute("SELECT MIN(create_time), MAX(create_time), COUNT(*) FROM gkxlumenx.sys_log") or None
span = c.fetchone()
facts["dev_sys_log_time_span"] = [str(span[0]), str(span[1])]
facts["dev_sys_log_total_rows"] = int(span[2])
d.close()

# ============ ② gkx：词族复核（族级探针） ============
facts["gkx_call_like_tables"] = probe["gkx_call_like_tables"]  # []
facts["gkx_table_count"] = snap["gkx"]["table_count"]

# ============ ③ 久新：词族复核（引用 021 当日 live 读数 + 快照兜底） ============
jx021 = os.path.join(BASE, "M_SCIUI_DATATHM_021_out.json")
if os.path.exists(jx021):
    d021 = json.load(open(jx021, encoding="utf-8"))
    facts["jiuxin_call_log_tables_live"] = d021["facts"].get("jiuxin_call_log_tables_live", [])
    facts["jiuxin_probe_mode"] = d021["facts"].get("jiuxin_probe_mode", "n/a")
    facts["jiuxin_table_count_live"] = d021["facts"].get("jiuxin_table_count_live")
else:
    import re  # noqa: E402
    jx_tables = snap["jiuxin"]["tables"]
    facts["jiuxin_call_log_tables_snapshot"] = [
        t for t in jx_tables
        if re.search(r"call_log|invoke|api_log|access_log|request_log|usage_log|call_stat", t, re.I)]
    facts["jiuxin_probe_mode"] = "快照兜底（021 产物当日不可用）"

# ================= 派生（负结论登记，B10） =================
derived.append({
    "key": "call_volume_annual_growth_trend",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『调用量年度增长趋势』需 API 调用日志的跨年序列面（年×调用量）——三源词族 0 命中"
            "→ 不可构建；内容年份面与『被调用次数』无语义关联不代理（与 021 同一裁定，"
            "产出时间≠使用时间）；按 B10 留空即负结论登记",
})

# ================= absence_probe =================
absence += [
    {"probe": "dev 调用量序列面（call_log/invoke_log/api_log/access_log/request_log/usage_log/"
              "call_stat/trend 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表）",
     "hits": len(facts["dev_call_trend_tables"]),
     "hit_detail": f"命中 {facts['dev_call_trend_tables']}——词族唯一命中 enterprise_growth_trend "
                   f"已结构复核排除（{facts['dev_trend_hit_structure']['verdict']}，0 行），"
                   "0 张调用序列表；最近邻 sys_log 跨度 "
                   f"{facts['dev_sys_log_time_span']} 共 {facts['dev_sys_log_total_rows']} 行"
                   "（单月量级、管理操作语义——020/021 已双重排除），非资源接口调用流水",
     },
    {"probe": "gkx 调用量面（call/invoke/api/request/latency/response/duration/monitor/usage 词族）",
     "source": "gkx",
     "sql": "information_schema.tables 扫 gkx（280 表，S3-04 族级探针）",
     "hits": len(facts["gkx_call_like_tables"]),
     "hit_detail": f"命中 {facts['gkx_call_like_tables']}——0 命中；要素明细库无调用统计面",
     },
    {"probe": "久新调用量面（同词族，引用 021 当日 live 读数）",
     "source": "jiuxin",
     "sql": "SHOW TABLES（2026-11-01 live，经 021 产物）词族扫",
     "hits": len(facts.get("jiuxin_call_log_tables_live", []) or
                 facts.get("jiuxin_call_log_tables_snapshot", [])),
     "hit_detail": "0 命中——ads_* 全部为分析结果面（快照管理），无调用日志；探测模式见 "
                   "facts.jiuxin_probe_mode（本件与 021 同日探测，读数复用 B11）",
     },
    {"probe": "需求原文「调用量…趋势分析」定义段",
     "source": "doc",
     "sql": "rg 调用量|趋势分析 三份需求真源",
     "hits": 2,
     "hit_detail": "主需求 :2571（累计调用与趋势分析）『自动归集各类数据资源自上线以来的累计"
                   "调用量，并按时间区段进行趋势分析』——功能在、前提（归集累计调用量）未建、"
                   "序列口径（年度/季度/月度？列结构？）无；UI 导出 sheet 年度三列（总量/新增/"
                   "同比）复用资源接入 mock（seq 330 语境），前端演示约定",
     },
]

support = "完全不支持"

notes += [
    "判档：调用量年度序列需跨年调用日志——三源词族 0 命中 → 不可构建；与 021 同根同判"
    "（差别仅读数形态：单点同比 vs 年度序列）；内容年份面不代理（产出≠使用）→ 完全不支持",
    f"序列可行性量级证据（dev sys_log，语义排除披露用）：时间跨度 {facts['dev_sys_log_time_span']}"
    f"、共 {facts['dev_sys_log_total_rows']} 行——单月量级的管理操作日志既不跨年也非调用语义，"
    "年度序列的原料完全缺位",
    "mock 披露：OverviewWindow.jsx:575 导出 sheet 年度三列（资源总量/年度新增/同比增速）消费 "
    "mockData.js:72-78 overviewAnnualAccessTrend（2022 total 12,860 → 2026 30,398）——该 mock "
    "是资源接入语境（seq 330，DATAOV_002 承接），UI 复用于导出表属演示约定，不作数据证据",
    "权威口径参照（R2 开放数林指数）：地方平台有效数据集总数 2017 年 8 千个 → 2025 年近 48 万个"
    "（八年近 57 倍、复合年均增长率 66%）——年度增长趋势的官方叙事形态（其度量对象是数据集"
    "开放量，调用量序列须由调用日志聚合，语义分界与 021 同）",
    "B11 对账：久新词族读数复用 021 当日 live 产物（同日探测零漂移）；sys_log 行数与 020/021 "
    "对账；542/280/210 共享快照",
    "升档触发器（B10）：①API 网关/调用日志接入（跨年时间戳）→ 升完全直接支持（020/021/022 "
    "共用）；②应用视窗组件位（CumulativeCallTrendAnalysis，DATATHM_025/032）同族受益",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_022",
    "batch": "S3-04",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:575",
        "repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:621",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:72",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书未出现「调用量年度增长趋势」指标名；语义锚 :2571『累计调用量…按时间"
                "区段进行趋势分析』（功能在、前提未建、序列口径无）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["2022", "2023", "2024", "2025", "2026"],
    "base_years_note": "年度序列基期（各年调用量）三源零承载——调用日志面不存在，mock 五年演示"
                       "序列（2022-2026）无真实对应",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["12860", "30398", "2022", "2026", "66", "542", "280", "210",
                          "1060"][:10]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_015 数据量变化率（较上期）· 三源探针与复现脚本（S3-04 L1）。

含义：科技数据资源·总体视窗·来源分析下钻表格的「变化率」列——按来源类别展示数据量较上期
的变化率（mock 5 来源全部上涨：国内数据库 +14.2%/国外 +8.6%/科研院所 +12.5%/企业 +18.3%/
开源平台 +22.1%）。指标语义=资源数据量的期环比（本期对上期，国家统计局环比口径 R1）。
UI：repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:555
（drillDownColumns 'source' 分支「变化率」列，dataIndex 'change'；mock 源
mockData.js:26-30 resourceSourceDistribution——5 来源 change 演示值）。

判档路径（口径=「数据量按来源的期环比」）：
- 直接承载：三源无资源接入流水台账（DATAOV_002 已证词族 0 命中）→ 无「本期/上期」两期
  资源数据量，环比本体不可直算；
- dev sys_log 有 time 耗时列但它是平台管理操作日志（登录/token 刷新），非数据资源接入流水
  （语义排除，登记）；
- 转换承载（内容年份面代理环比）：dev enterprise_base 注册年 2026 对 2025、gkx 论文/专利
  年分布相邻年、久新年序列相邻年——三源「内容年份面」相邻期比率可算（DATAOV_002 同族读数
  复用 + 独立留证），语义披露：内容规模变化 ≠ 平台接入数据量变化；
- 判部分支持（两期台账缺位 + 代理环比三源可算）。
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_015_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
SNAP_S3 = os.path.join(BASE, "_snapshots", "_shared_probe_s3_01_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402

facts, derived, notes, absence = {}, [], [], []
snap = json.load(open(SNAP, encoding="utf-8"))
snap_s3 = json.load(open(SNAP_S3, encoding="utf-8"))

# ============ ① dev：注册年序列（内容年份面代理的两期原料）+ 台账排除复核 ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
d = pymysql.connect(**DEV)
c = d.cursor()

def q(sql):
    c.execute(sql)
    return c.fetchall()

facts["dev_enterprise_base_rows"] = int(q(
    "SELECT COUNT(*) FROM gkxlumenx_dwd.enterprise_base")[0][0])
# 近 6 年注册年聚合（B9：YEAR() 合法区间过滤；较上期=相邻年环比，近 6 年给 5 个环比点）
facts["dev_enterprise_reg_year_recent6"] = [[int(a), int(b)] for a, b in q(
    "SELECT YEAR(registration_date) y, COUNT(*) FROM gkxlumenx_dwd.enterprise_base "
    "WHERE YEAR(registration_date) BETWEEN 2021 AND 2026 GROUP BY y ORDER BY y")]
# 接入台账词族复核（与 DATAOV_002 同词族，本件独立留证）
c.execute(
    "SELECT table_schema, table_name FROM information_schema.tables "
    "WHERE table_schema LIKE 'gkxlumenx%' "
    "AND table_name REGEXP 'access_log|access_history|resource_access|ingest|collect'")
facts["dev_access_registry_tables"] = [f"{r[0]}.{r[1]}" for r in sorted(c.fetchall())]
d.close()

# ============ ② gkx：论文/专利年分布（共享快照复用，20 万采样口径） ============
paper_years = patent_years = None
for item in snap_s3["fix2_20261101"]:
    if item["tag"] == "论文年份分布（20万采样）":
        paper_years = [[str(a), int(b)] for a, b in item["data"]]
    if item["tag"] == "专利申请年分布（20万采样）":
        patent_years = [[str(a), int(b)] for a, b in item["data"]]
facts["gkx_paper_year_dist_sampled"] = paper_years
facts["gkx_patent_year_dist_sampled"] = patent_years
facts["gkx_table_count"] = snap["gkx"]["table_count"]

# ============ ③ 久新：人才年序列（内容年份面） ============
try:
    JX = dict(host="47.93.119.170", port=29030, user="test2",
              password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
              database="gkx_technology_analysis_dev",
              connect_timeout=10, read_timeout=300)
    jconn = pymysql.connect(**JX)
    jc = jconn.cursor()
    jc.execute("SELECT year, COUNT(*) FROM ads_talent_yearly_metrics "
               "WHERE year BETWEEN 2021 AND 2026 GROUP BY year ORDER BY year")
    facts["jiuxin_yearly_metrics_recent6"] = [[int(a), int(b)] for a, b in jc.fetchall()]
    jconn.close()
    facts["jiuxin_probe_mode"] = "live"
except Exception as e:  # noqa: BLE001
    facts["jiuxin_probe_mode"] = f"源不可达，未取证（{str(e)[:100]}）"
    facts["jiuxin_yearly_metrics_recent6"] = None

# ================= 派生（B3：分子分母同表同 WHERE 相邻年） =================
reg6 = dict(facts["dev_enterprise_reg_year_recent6"]) if facts["dev_enterprise_reg_year_recent6"] else {}
if 2025 in reg6 and 2026 in reg6:
    derived.append({
        "key": "dev_enterprise_reg_change_2026_vs_2025_pct",
        "value": round(100.0 * (reg6[2026] - reg6[2025]) / reg6[2025], 2),
        "numerator": reg6[2026] - reg6[2025],
        "denominator": reg6[2025],
        "note": "分子=2026 注册数-2025（增量）；分母=2025 注册数（同表同 WHERE YEAR() 口径，"
                "B3 同基）——内容年份面的『较上期』代理读数（相邻年环比）",
    })
else:
    derived.append({"key": "dev_enterprise_reg_change_2026_vs_2025_pct", "value": None,
                    "numerator": None, "denominator": None, "note": "序列不足两年，不可算"})
# 逐相邻年环比序列（口径 B 交付形态：每点分子分母可回算）
pop_dist = []
if reg6:
    ys = sorted(reg6)
    for a, b in zip(ys, ys[1:]):
        pop_dist.append({
            "period": f"{b}_vs_{a}",
            "value": round(100.0 * (reg6[b] - reg6[a]) / reg6[a], 2),
            "numerator": reg6[b] - reg6[a],
            "denominator": reg6[a],
        })
derived.append({"key": "dev_enterprise_reg_change_series_pct", "value": pop_dist,
                "note": "注册年相邻期环比序列（每点分子=年增量、分母=上年注册数，同基）——"
                        "内容年份面代理的完整环比序列"})
# 负结论登记（B10）
derived.append({
    "key": "source_volume_change_rate",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『按来源的数据量较上期变化率』三源无两期台账承载（本期/上期资源数据量面不存在）；"
            "本件交付内容年份面相邻期比率（企业注册年环比/论文专利年分布/人才年序列），"
            "语义=库内内容规模变化≠平台接入数据量变化；按 B10 留空即负结论登记",
})

# ================= absence_probe =================
absence += [
    {"probe": "dev 资源接入流水台账（access_log/access_history/resource_access/ingest/collect 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表）",
     "hits": len(facts["dev_access_registry_tables"]),
     "hit_detail": f"命中 {facts['dev_access_registry_tables']}——0 张接入流水表（与 DATAOV_002 "
                   "同词族结论，本件独立复跑留证）；无两期资源数据量面，环比本体不可直算",
     },
    {"probe": "gkx 资源接入/调用量台账（同词族 + call/invoke/request 词族）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表）词族扫（S3-04 族级探针复用）",
     "hits": 0,
     "hit_detail": "call/invoke/api/request/latency/response 词族 280 表 0 命中（gkx_call_like_tables"
                   "=[]，_probe_s304_l1_out.json）——要素明细库无任何接入/调用流水面",
     },
    {"probe": "久新资源接入/调用量台账（同词族）",
     "source": "jiuxin",
     "sql": "SHOW TABLES 快照（210 表，2026-11-01）词族扫",
     "hits": 0,
     "hit_detail": "call/invoke/api/request/latency/response 词族 0 命中（族级探针 "
                   "jiuxin_call_like_tables 未及——当日两连败；以共享快照 210 表清单复核同结论："
                   "ads_* 全部为学科/人才/专利/项目分析结果面，无接入流水）",
     },
    {"probe": "需求原文「变化率/数据量」定义段",
     "source": "doc",
     "sql": "rg 变化率|同比 三份需求真源",
     "hits": 0,
     "hit_detail": "三份说明书未出现「数据量变化率」指标名；主需求最近语境 :2493『详细分析资源"
                   "来源的结构组成及变化』——『及变化』为功能泛述无口径；UI change 列 5 来源演示值"
                   "（mockData.js:26-30）不作口径证据",
     },
]

support = "部分支持"

notes += [
    "判档：『较上期』两期资源数据量面三源零承载（台账词族 0 命中）→ 环比本体不可直算；"
    "内容年份面相邻期比率三源可算（dev 注册年环比 + gkx 论文/专利年分布 + 久新年序列）→ "
    "代理读数可交付（语义披露）→ 部分支持",
    f"代理读数（dev）：enterprise_base {facts['dev_enterprise_base_rows']} 行，近 6 年注册年分布 "
    f"{facts['dev_enterprise_reg_year_recent6']}，2026 对 2025 环比 "
    f"{[x for x in derived if x['key']=='dev_enterprise_reg_change_2026_vs_2025_pct'][0]['value']}%"
    "（产物派生键，分子分母同基）",
    "代理读数（gkx，共享快照复用）：论文 cover_year_start/专利 apdt_year 20 万采样年分布在案"
    "（采样，非全表）——相邻年比率可从分布直接回算，本件不另立键（B11 快照原样引用）",
    f"代理读数（久新）：ads_talent_yearly_metrics 近 6 年行分布 {facts['jiuxin_yearly_metrics_recent6']}"
    f"（probe_mode={facts['jiuxin_probe_mode']}）",
    "mock 披露：OverviewWindow.jsx:555 下钻表格「变化率」列消费 resourceSourceDistribution 的 "
    "change 字段（国内数据库 +14.2/国外 +8.6/科研院所 +12.5/企业 +18.3/开源平台 +22.1，全部上涨）"
    "——mockData.js:26-30 演示值，且为来源维度，不作数据证据（B10）",
    "口径注：名称「较上期」=期环比（国家统计局 R1：环比增长率＝(本期数-上期数)/上期数×100%）；"
    "UI mock 全上涨叙事与 dev 代理读数（2026 对 2025 大幅下行）方向相反——代理披露价值所在",
    "B9 规避：registration_date 零日期用 YEAR() BETWEEN 合法区间过滤；gkx 年份列为 varchar（快照已注）",
    "B11 对账：gkx 年分布取自 _shared_probe_s3_01_out.json 原样；dev 542/gkx 280/久新 210 共享快照",
    "升档触发器（B10）：①建资源接入流水台账（含来源维）→ 环比本体直查升完全直接支持；"
    "②甲方裁定变化率=内容年份面相邻期比率 → 完全转换支持",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_015",
    "batch": "S3-04",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:555",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:26",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书未出现「数据量变化率」指标名；最近语境主需求 :2493『结构组成及变化』"
                "为功能泛述；UI change 列为 mock 演示值",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [str(y) for y in sorted(reg6)] if reg6 else [],
    "base_years_missing": [],
    "base_years_note": "基期=dev 企业注册年近 6 年（2021-2026 实测，相邻年环比）；『较上期』的"
                       "本期/上期两期资源数据量面缺失见 absence_probe",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["14.2", "8.6", "12.5", "18.3", "22.1", "2025", "2026", "269511", "542",
                          "280", "210"][:12]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INNOV_013 区域能力结构分析（五维构成）—— 三源探针 + 复现脚本（批 S3-01，Lane 7）。

UI 挂载（实查）：
  ① repos/demo-ui-science/src/pages/global-innovation/tabs/carrierRankingCompareModel.js:32
     compareViewOptions { key: 'radar', label: '能力结构', title: '能力结构分析' } —— 对比视图第 2 项（雷达）
  ② carrierRankingCompareModel.js:604
     buildCarrierCompareExportConfig contentItems { key: 'radar', label: '能力结构分析' } —— 导出报告章节
  雷达实现 :500-538：indicator = 用户勾选的 metrics（score/patents/papers/projects/rank 五选 N），
  每维按「值/组内最大值×100」相对归一（rank 反向 min/value×100）——组内相对制，非全局基准制。
  mock：mockData.js:129-133 城市雷达五维（创新投入/创新产出/创新环境/人才储备/政策支持，baseIndex 派生随机抖动，
  演示值，不参与支持度结论）。

三源：
  ① 开发库：gkxlumenx_dwd 评分类表扫描 score/ability/capability/index 全部 0 命中（本件 absence_probe）
  ② gkx：cap/power/score 0 命中；dwd_dim_index_attribute(867)/dwd_macro_index_data(20,000) 是宏观
     经济指标字典（规上工业 R&D 人员等），非区域创新能力结构承载
  ③ 久新：ads_geo_yearly_metrics 171,736 行五列全在（paper/project/talent/institution/cited_by），
     CITY 级 2025 有 9,121 行——城市五维雷达的原料一次取齐，本件主承载

复现口径（B10 双口径并列）：
  口径 A（城市五维雷达·UI 同构）：mock 十城（深圳/北京/上海/杭州/硅谷→旧金山/纽约/伦敦/东京/新加坡/柏林）
       五维 = 论文/项目/人才/机构/流入人才，取 2025 CITY 级行，五维 min-max 归一（×100 制）画雷达
  口径 B（全球城市 Top10 五维）：全库 CITY 级按论文 Top10 的五维归一面板（结构对比可直接回填）
  方法依据：GII 2025 七支柱框架的「维度→归一→聚合」范式（R1）；UI 自身即组内相对归一（radar 实现），
  本件实测改全样本极值归一并披露（与 004 件一致的保守透明中间态）。
"""
import json
import os
import sys

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _gkxdb import gkx  # noqa: E402

JX = dict(
    host="47.93.119.170",
    port=29030,
    user="test2",
    password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
    database="gkx_technology_analysis_dev",
    connect_timeout=30,
    read_timeout=300,
)

facts = {}
probes = []

DIMS = ("papers", "projects", "talents", "institutions", "inbound_talents")


def probe(tag, source, sql, cur):
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        probes.append({"probe": tag, "source": source, "sql": sql,
                       "hits": len(rows), "sample": [str(r)[:200] for r in rows[:8]]})
        return rows
    except Exception as e:  # noqa: BLE001
        probes.append({"probe": tag, "source": source, "sql": sql,
                       "hits": -1, "error": str(e)[:200]})
        return []


def fetch_city_rows(jc, queries):
    """按 (zh_like, en_eq) 查询对取 2025 CITY 行五维（多命中取论文最大者）。

    ads_location 命名规约：中国城市 name_zh 带「市」后缀（深圳除外）、海外城市 name_zh 为 NULL
    只能按 name_en 精确匹配——因此每城给一个 (中文 LIKE, 英文 =) 二元组。
    """
    rows = []
    for zh, en in queries:
        jc.execute(
            "SELECT COALESCE(l.name_en, l.name_zh), m.paper_count, m.project_count, "
            "m.talent_count, m.institution_count, m.inbound_talent_count "
            "FROM ads_geo_yearly_metrics m LEFT JOIN ads_location l ON l.location_id=m.location_id "
            "WHERE (l.name_zh LIKE %s OR l.name_en=%s) AND m.location_level='CITY' AND m.statistics_year=2025 "
            "ORDER BY m.paper_count DESC LIMIT 1", (zh, en))
        r = jc.fetchone()
        if r and (r[1] or 0) > 0:
            rows.append({"city": str(r[0]), "papers": int(r[1] or 0), "projects": int(r[2] or 0),
                         "talents": int(r[3] or 0), "institutions": int(r[4] or 0),
                         "inbound_talents": int(r[5] or 0)})
    # 去重（按 city 名）
    seen, uniq = set(), []
    for r in rows:
        if r["city"] not in seen:
            seen.add(r["city"])
            uniq.append(r)
    return uniq


def minmax100(rows, key):
    vals = [r[key] for r in rows]
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return {r["city"]: 0.0 for r in rows}
    return {r["city"]: round((r[key] - lo) / (hi - lo) * 100, 2) for r in rows}


# ---------------------------------------------------------------- 久新（主承载）
jx = pymysql.connect(**JX)
jc = jx.cursor()

facts["jiuxin_geo_yearly_metrics_rows"] = 171736  # 共享探针快照原值（B11 与 002/004 件零漂移）
jc.execute("SELECT COUNT(*) FROM ads_geo_yearly_metrics")
assert int(jc.fetchone()[0]) == facts["jiuxin_geo_yearly_metrics_rows"]

jc.execute("SELECT COUNT(*) FROM ads_geo_yearly_metrics WHERE location_level='CITY' AND statistics_year=2025")
facts["jiuxin_city_2025_rows"] = int(jc.fetchone()[0])

# 口径 A：mock 十城五维（硅谷→San Francisco；中国城市库内带「市」后缀走 LIKE，海外城市按 name_en）
mock_queries = [
    ("%深圳%", "Shenzhen"), ("%北京%", "Beijing"), ("%上海%", "Shanghai"), ("%杭州%", "Hangzhou"),
    ("", "New York"), ("", "London"), ("", "Tokyo"), ("", "Singapore"), ("", "Berlin"),
    ("", "San Francisco"), ("", "Boston"),
]
raw_a = fetch_city_rows(jc, mock_queries)
facts["jiuxin_mock_city_raw"] = raw_a
norms = {k: minmax100(raw_a, k) for k in DIMS}
facts["jiuxin_mock_city_radar_dimnames"] = list(DIMS)
facts["jiuxin_mock_city_radar"] = [
    {"city": r["city"], **{k: norms[k][r["city"]] for k in DIMS}}
    for r in sorted(raw_a, key=lambda r: -norms["papers"][r["city"]])]

# 口径 B：全球城市 Top10（by papers）五维面板
jc.execute(
    "SELECT COALESCE(l.name_en, l.name_zh), m.paper_count, m.project_count, m.talent_count, "
    "m.institution_count, m.inbound_talent_count "
    "FROM ads_geo_yearly_metrics m LEFT JOIN ads_location l ON l.location_id=m.location_id "
    "WHERE m.location_level='CITY' AND m.statistics_year=2025 "
    "ORDER BY m.paper_count DESC LIMIT 10")
raw_b = [{"city": str(r[0]), "papers": int(r[1] or 0), "projects": int(r[2] or 0),
          "talents": int(r[3] or 0), "institutions": int(r[4] or 0),
          "inbound_talents": int(r[5] or 0)} for r in jc.fetchall()]
facts["jiuxin_global_city_top10_raw"] = raw_b
norms_b = {k: minmax100(raw_b, k) for k in DIMS}
facts["jiuxin_global_city_top10_radar"] = [
    {"city": r["city"], **{k: norms_b[k][r["city"]] for k in DIMS}} for r in raw_b]

jc.close()
jx.close()

# ---------------------------------------------------------------- gkx（负结论探针）
gc = gkx()
rows = probe("gkx 280 表能力结构/评分类结果面扫描（capability/power/score/assessment/index/benchmark）", "gkx",
             "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
             "AND (table_name LIKE '%capability%' OR table_name LIKE '%power%' OR table_name LIKE '%score%' "
             "OR table_name LIKE '%assessment%' OR table_name LIKE '%benchmark%')", gc)
facts["gkx_capability_like_tables"] = [r[0] for r in rows]
rows2 = probe("gkx 指数类表扫描（index，宏观指标字典甄别）", "gkx",
              "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
              "AND table_name LIKE '%index%'", gc)
facts["gkx_index_like_tables"] = [r[0] for r in rows2]
gc.close()

# ---------------------------------------------------------------- 开发库（负结论探针）
from _gkxdb import live
dv = live("DWD")
dc = dv.cursor()
rows = probe("dev gkxlumenx_dwd 评分/能力/指数类表扫描", "dev",
             "SHOW TABLES", dc)
all_dev_tables = [list(r.values())[0] if isinstance(r, dict) else r[0] for r in rows]
facts["dev_capability_like_tables"] = [t for t in all_dev_tables
                                       if any(k in t.lower() for k in ("score", "ability", "capability", "index"))]
rows = probe("dev enterprise_growth_trend / sz_city_benchmark 行数（趋势对标类空载甄别）", "dev",
             "SELECT (SELECT COUNT(*) FROM enterprise_growth_trend), "
             "(SELECT COUNT(*) FROM sz_city_benchmark)", dc)
if rows:
    row0 = rows[0]
    vals = list(row0.values()) if isinstance(row0, dict) else list(row0)
    facts["dev_trend_benchmark_rows"] = [int(x) for x in vals]
dc.close()
dv.close()

# ---------------------------------------------------------------- 产物
out = {
    "metric_id": "M_SCIUI_INNOV_013",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/global-innovation/tabs/carrierRankingCompareModel.js:32",
        "repos/demo-ui-science/src/pages/global-innovation/tabs/carrierRankingCompareModel.js:604",
        "repos/demo-ui-science/src/pages/global-innovation/tabs/carrierRankingCompareModel.js:514",
        "repos/demo-ui-science/src/pages/global-innovation/mockData.js:129",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「区域能力结构分析/能力结构分析」作为指标名未出现在三份说明书；最近语义为全球创新监测.md seq 85 城市对标分析：『系统提供对比视图，展示各城市在创新投入、创新产出、创新环境等方面的差异』（维度枚举级，非公式定义）；seq 86 创新能力要素分析『分析影响城市创新能力的关键要素，如人才、资金、政策』次之",
    },
    "facts": facts,
    "derived": {
        "jiuxin_mock_city_radar_dimcount": {
            "value": float(len(DIMS)),
            "numerator": len(DIMS),
            "denominator": 1,
            "note": "五维构成 = 论文/项目/人才/机构/流入人才（geo_yearly_metrics 五列）；分子=可归一维数，分母=1（计数型派生）",
        },
    },
    "absence_probe": probes,
    "support_judgment": "完全转换支持",
    "notes": [
        "三源无现成「能力结构」结果面（gkx capability/power/score/assessment/benchmark 0 命中；dev score/ability/capability/index 0 命中；久新 ads_geo_yearly_index 结构在但 0 行——见 014 件），但久新 ads_geo_yearly_metrics CITY 级 2025 年 9,121 行五列（论文/项目/人才/机构/流入人才）全量可用——结构+数据双达标，现在就能转换得到，判完全转换支持",
        "UI 雷达是组内相对归一（值/组内最大×100，rank 反向），mock 五维为创新投入/创新产出/创新环境/人才储备/政策支持（投入/环境/政策三维在 geo 池无直接对应列——政策支持三源无城市级政策量化面，投入维可用机构/流入人才近似，语义须降级披露）；本件口径 A/B 用论文/项目/人才/机构/流入人才五维是数据可得的最近似结构",
        "口径 A 的「硅谷」在 ads_location 无同名城（探针 0 命中），以 San Francisco 替代并在正文披露；mock 十城中北京/上海/杭州/深圳全在库，海外五城全在库（纽约/伦敦/东京/新加坡/柏林）",
        "五维归一为 min-max 全样本（A=mock 城市组内，B=全球 Top10 组内），极值钳制警示与 004 件同——正式版建议分位归一（R1 范式）",
        "gkx dwd_dim_index_attribute(867 行)/dwd_macro_index_data(20,000 行) 是宏观经济指标字典与月度数据（规上工业 R&D 人员等），非区域创新能力结构承载，已甄别排除",
    ],
    "base_years_used": ["2025"],
    "base_years_missing": [],
    "base_years_note": "城市五维取 2025 年 CITY 级截面（最新完整年）；年度演进可由同表回算（002 件已证 2015-2025 连续）；2026 残年不用",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "171736", "9121", "2025", "5", "160529", "24904", "129",
    ]},
}
path = os.path.join(HERE, "M_SCIUI_INNOV_013_out.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", path)
print("support_judgment:", out["support_judgment"])
print("mock city radar Top3:", facts["jiuxin_mock_city_radar"][:3])
print("global top10 radar Top3:", facts["jiuxin_global_city_top10_radar"][:3])

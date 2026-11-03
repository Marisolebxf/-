#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INNOV_014 区域能力评分（综合）—— 三源探针 + 复现脚本（批 S3-01，Lane 7）。

UI 挂载（实查，三页同构）：
  ① repos/demo-ui-science/src/globalInnovationMonitor.js:403
     metricCards { label: '能力评分', value: target.score ?? '-' } —— 详情卡第一张
  ② repos/demo-ui-science/src/bayAreaInnovationMonitor.js:386 同构
  ③ repos/demo-ui-science/src/shenzhenInnovationMonitor.js:461 同构（区级范围变体）
  mock：baseRecords score 94/91/86/89/82/87/84/79 手写演示值（0-100 制，不参与支持度结论）
  姊妹算法：carrierRankingCompareModel.js:96『创新力指数 = 专利×35% + 论文×25% + 项目×25% + 活跃×15%』
           （归一 0-100 加权汇总，UI 已内置公式模板但无真实数据源）

三源：
  ① 开发库：gkxlumenx_ads score 类 3 表（enterprise_score/industry_chain_region_scorecard/
     svc_tech_power_score，lane1 probe2 探针）——但 gkxlumenx_dwd 侧无能力评分承载（本件补行数探针）
  ② gkx：score/assess/power 0 命中（lane1 probe2 官方探针）
  ③ 久新：两候选——ads_geo_yearly_index（schema 在 0 行，1.6.0 预留）与
     ads_technology_region_assessment（2,708,162 行 19,027 节点×389 地名，但实测分值是
     节点内百分位制：每城 AVG≈50、城市间不可比——是陷阱面非结果面）

复现口径（B10 双口径并列）：
  口径 A（加权综合评分·UI 同构）：ads_geo_yearly_metrics 2025 COUNTRY 级五维
       （papers/projects/talents/institutions/inbound）→ min-max 归一 ×100 →
       权重 [25,25,25,15,10]（仿 UI 专利/论文/项目/活跃四维模板扩五维）
  口径 B（非加权参照）：等权 20%×5 对照——揭示权重敏感性
  方法依据：GII 2025 加权汇总范式（R1）；UI 自身 formula 模板（carrierRankingCompareModel.js:96）
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
W_A = (25, 25, 25, 15, 10)  # 口径 A 权重（UI 模板式加权）
W_B = (20, 20, 20, 20, 20)  # 口径 B 等权


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


jx = pymysql.connect(**JX)
jc = jx.cursor()


def q(sql):
    jc.execute(sql)
    return jc.fetchall()


# ---------------------------------------------------------------- 久新：陷阱面甄别（主降档证据）
facts["jiuxin_geo_yearly_index_rows"] = 0  # 官方共享快照 _probe_lane5_s3_01_out.json #10 原值
assert int(q("SELECT COUNT(*) FROM ads_geo_yearly_index")[0][0]) == 0

facts["jiuxin_region_assessment_rows"] = 2708162  # lane1 probe 官方探针原值（B11 零漂移）
assert int(q("SELECT COUNT(*) FROM ads_technology_region_assessment")[0][0]) == facts["jiuxin_region_assessment_rows"]
facts["jiuxin_region_assessment_named_locs"] = int(
    q("SELECT COUNT(DISTINCT location_name_zh) FROM ads_technology_region_assessment "
      "WHERE location_name_zh IS NOT NULL")[0][0])

# 陷阱面实证：节点内百分位制（北京 AVG vs 满分行）
facts["jiuxin_region_assessment_full_score_rows"] = 10928  # lane1 probe2 官方探针原值
_row = q("SELECT COUNT(*), ROUND(AVG(regional_potential_score),4) FROM ads_technology_region_assessment "
         "WHERE location_name_zh='北京市' AND model_version='technology_insight_mvp_v2_eto_cluster_technology'")[0]
facts["jiuxin_region_assessment_beijing_rows_v2"] = int(_row[0])
facts["jiuxin_region_assessment_beijing_avg_score"] = float(_row[1])

# ---------------------------------------------------------------- 口径 A/B：加权综合评分（geo 五维）
jc.execute(
    "SELECT COALESCE(l.name_en, l.name_zh), m.paper_count, m.project_count, m.talent_count, "
    "m.institution_count, m.inbound_talent_count "
    "FROM ads_geo_yearly_metrics m LEFT JOIN ads_location l ON l.location_id=m.location_id "
    "WHERE m.location_level='COUNTRY' AND m.statistics_year=2025")
raw = [(str(n), tuple(int(x or 0) for x in vals)) for n, *vals in jc.fetchall()]
raw = [(n, vals) for n, vals in raw if len(vals) == 5]  # 防御：列数不足行剔除
facts["jiuxin_country_2025_rows_for_score"] = len(raw)

extrema = {d: (min(r[1][i] for r in raw), max(r[1][i] for r in raw)) for i, d in enumerate(DIMS)}


def normalize(v, d):
    lo, hi = extrema[d]
    return 0.0 if hi == lo else (v - lo) / (hi - lo) * 100.0


scored = []
for name, vals in raw:
    ns = [normalize(vals[i], d) for i, d in enumerate(DIMS)]
    scored.append({
        "country": name,
        "weighted": round(sum(n * w for n, w in zip(ns, W_A)) / 100.0, 4),
        "equal": round(sum(n * w for n, w in zip(ns, W_B)) / 100.0, 4),
    })
scored.sort(key=lambda r: -r["weighted"])
facts["jiuxin_country_score_2025_top12_weighted"] = scored[:12]
facts["jiuxin_country_score_2025_global_mean_weighted"] = round(
    sum(r["weighted"] for r in scored) / len(scored), 4)

# 权重敏感性：Top3 排名在 A/B 两制式下是否一致
rank_a = [r["country"] for r in sorted(scored, key=lambda x: -x["weighted"])[:3]]
rank_b = [r["country"] for r in sorted(scored, key=lambda x: -x["equal"])[:3]]
facts["jiuxin_country_score_top3_weighted"] = rank_a
facts["jiuxin_country_score_top3_equal"] = rank_b

jc.close()
jx.close()

# ---------------------------------------------------------------- gkx（负结论，消费官方探针不重跑）
gc = gkx()
probe("gkx score/assess/power 表扫描（消费 lane1 probe2 官方探针，此处登记）", "gkx",
      "SHOW TABLES FROM gkx LIKE '%score%'", gc)
gc.close()

# ---------------------------------------------------------------- 开发库（行数补测，live 库经 _gkxdb）
try:
    from _gkxdb import live  # noqa: E402
    lconn = live("ADS")
    lcv = lconn.cursor()
    rows = probe("dev live gkxlumenx_ads 3 张 score 类表行数（空载甄别）", "dev",
                 "SELECT (SELECT COUNT(*) FROM enterprise_score) AS c1, "
                 "(SELECT COUNT(*) FROM industry_chain_region_scorecard) AS c2, "
                 "(SELECT COUNT(*) FROM svc_tech_power_score) AS c3", lcv)
    if rows:
        row = rows[0]
        vals = list(row.values()) if isinstance(row, dict) else list(row)
        facts["dev_ads_score_table_rows"] = [int(x) for x in vals]
    lcv.close()
    lconn.close()
except Exception as e:  # noqa: BLE001
    probes.append({"probe": "dev live gkxlumenx_ads 3 张 score 类表行数（连接失败登记）",
                   "source": "dev", "sql": "SELECT COUNT(*) FROM gkxlumenx_ads.enterprise_score ...",
                   "hits": -1, "error": str(e)[:200]})

# ---------------------------------------------------------------- 产物
out = {
    "metric_id": "M_SCIUI_INNOV_014",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/globalInnovationMonitor.js:403",
        "repos/demo-ui-science/src/bayAreaInnovationMonitor.js:386",
        "repos/demo-ui-science/src/shenzhenInnovationMonitor.js:461",
        "repos/demo-ui-science/src/pages/global-innovation/tabs/carrierRankingCompareModel.js:96",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「区域能力评分」作为指标名未出现在三份说明书；最近语义为全球创新监测.md seq 73 创新能力指数计算：『基于数据模型对各创新载体的创新成果数据进行计算，生成创新能力指数，用户可查看指数计算方法和权重设置』（载体级非区域级）；seq 84 创新能力排名计算『基于数据模型分析计算各大城市的创新能力排名』为城市级最近锚（两处均无公式定义，权重留白）",
    },
    "facts": facts,
    "derived": {
        "jiuxin_score_top1_gap_pts": {
            "value": round(scored[0]["weighted"] - scored[1]["weighted"], 4),
            "numerator": scored[0]["weighted"],
            "denominator": scored[1]["weighted"],
            "note": "分子=口径A Top1 加权分，分母=Top2 加权分（同表同截面 2025，B3）；差值即领先幅度（分）",
        },
        "jiuxin_region_assessment_named_pct": {
            "value": round(facts["jiuxin_region_assessment_named_locs"] and
                           facts["jiuxin_region_assessment_beijing_rows_v2"] /
                           facts["jiuxin_region_assessment_rows"] * 100, 6),
            "numerator": facts["jiuxin_region_assessment_beijing_rows_v2"],
            "denominator": facts["jiuxin_region_assessment_rows"],
            "note": "分子=北京市 v2 模型行数（单城体量参照），分母=全表行数——陷阱面体量对照",
        },
    },
    "absence_probe": probes,
    "support_judgment": "部分支持",
    "notes": [
        "三源无现成「区域能力评分」结果面：久新 ads_geo_yearly_index schema 在但 0 行（1.6.0 预留、公式未审定）；ads_technology_region_assessment 2,708,162 行是节点×地名粒度的陷阱面——分值为节点内百分位（每城 AVG≈50，北京 48.8899），城市间不可比，不能当城市评分直接回填",
        "gkx score/assess/power 0 命中；dev gkxlumenx_ads 3 张 score 表为企业/产业链粒度（若空载则双降），均非区域能力承载",
        "口径 A 为 UI 同构推测：仿 carrierRankingCompareModel 创新力指数模板（归一 0-100+加权）扩至五维，权重 [25,25,25,15,10] 为本件假设——SRS seq 73 明言权重须「用户可查看/设置」，正式版须甲方裁定权重后重算",
        "min-max 归一受极值钳制（中国论文维 100 压扁他国区分度），与 004 件同病——正式版建议 RIS 式分位归一（R2）",
        "UI mock score 94/91/86... 是城市/项目混合粒度手写值；回填时国家/城市两级须分卡",
    ],
    "base_years_used": ["2025"],
    "base_years_missing": [],
    "base_years_note": "评分取 2025 截面（最新完整年，2026 残年不用）；ads_geo_yearly_index 若上游填充后按年出值",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "0", "2708162", "389", "10928", "48.8899", "2025", "25", "15", "10","21918","47.0593","47.9260"]},
}
path = os.path.join(HERE, "M_SCIUI_INNOV_014_out.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", path)
print("support_judgment:", out["support_judgment"])
print("口径A Top5:", scored[:5])
print("Top3 A vs B:", rank_a, "|", rank_b)
print("beijing avg:", facts["jiuxin_region_assessment_beijing_avg_score"])

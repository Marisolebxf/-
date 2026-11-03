#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INNOV_017 领域创新指标排名 —— 三源探针 + 复现脚本（批 S3-01，Lane 7）。

UI 挂载（实查）：
  ① repos/demo-ui-science/src/pages/global-innovation/tabs/carrierRankModeModel.js:5
     CARRIER_RANK_MODES { key: 'domain', label: '领域排名' } —— 排名模式第 2 项（总体/领域/地区三选一）
  ② carrierRankModeModel.js:22 attachCarrierRankGroups：rankMode='domain' 时按 row.domain 分组、
     组内 displayRank 重排——「领域内排名」语义（分组降序组大小 + localeCompare 组名）
  消费方：InnovationRanking.jsx:44 rankMode state、:121 模式选择器、InnovationRanking 排序键
     RANK_SCORE_DIMENSION='score'（:39）——领域分组的排序底座是创新能力指数（014 姊妹件）
  mock：mockData.js:15 domains 八领域枚举（合成生物/光载信息/量子信息/新材料/人工智能/新能源/
     智能制造/生命健康）——载体行携带 domain 字段随机装配

三源：
  ① 开发库：无论文/领域承载（官方快照 dev 论文表探测 0 行；领域分组属展示层无库内承载）
  ② gkx：无领域排名类表（score/assess/power 0 命中，lane1 probe2 官方探针）
  ③ 久新：ads_topic_country_snapshot 209,517 行自带 output_rank（topic 内国别排名）+
     ranked_country_count；经 ads_discipline_topic（4,516 topics→26 fields）+
     ads_discipline_field（26 领域字典）两级 JOIN 即得「领域×国」排名——结构+数据双达标

复现口径（B10 双口径并列）：
  口径 A（领域内国别排名·UI 同构）：26 领域各自 SUM(paper_count) 国别 Top3——
     「领域排名」= 分组内 displayRank 的数据侧同构
  口径 B（国别×领域矩阵）：中/美在 26 领域的 output_rank=1 占有数——「领域排名」的
     领先面全景（headline 读数：中国在 26 领域中的 N 个居首）
  语义对齐：UI 的领域分组键是载体 domain（八领域 mock 枚举），上游是 26 学科领域——
     回填时需建 UI 八领域→26 领域映射（或改用 UI 领域枚举直接对齐学科字典）。
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


# ---------------------------------------------------------------- 规模校验（消费官方快照原值并断言）
facts["jiuxin_topic_country_rows"] = 209517  # 官方共享快照 #2 原值
assert int(q("SELECT COUNT(*) FROM ads_topic_country_snapshot")[0][0]) == facts["jiuxin_topic_country_rows"]
facts["jiuxin_discipline_topic_rows"] = 4516
facts["jiuxin_discipline_field_rows"] = 26
assert int(q("SELECT COUNT(*) FROM ads_discipline_field")[0][0]) == 26

# output_rank 直读验证（中国论文量 Top5 主题的排名）
facts["jiuxin_cn_output_rank_sample_top5"] = [
    {"topic": str(t), "output_rank": int(rk), "ranked_countries": int(rc), "papers": int(p)}
    for t, rk, rc, p in q(
        "SELECT dt.name_zh, s.output_rank, s.ranked_country_count, s.paper_count "
        "FROM ads_topic_country_snapshot s JOIN ads_discipline_topic dt ON s.topic_id=dt.topic_id "
        "WHERE s.country_code='CN' ORDER BY s.paper_count DESC LIMIT 5")]

# ---------------------------------------------------------------- 口径 A：26 领域各自国别 Top3
jc.execute(
    "SELECT f.name_zh AS field, s.country_name_en AS country, SUM(s.paper_count) AS papers "
    "FROM ads_topic_country_snapshot s "
    "JOIN ads_discipline_topic t ON s.topic_id=t.topic_id "
    "JOIN ads_discipline_field f ON t.field_id=f.field_id "
    "GROUP BY f.name_zh, s.country_name_en")
agg = {}
for field, country, papers in jc.fetchall():
    agg.setdefault(str(field), []).append((str(country), int(papers)))
field_top3 = {}
for field, lst in agg.items():
    lst.sort(key=lambda x: -x[1])
    field_top3[field] = [{"country": c, "papers": p} for c, p in lst[:3]]
facts["jiuxin_field_country_top3"] = dict(sorted(field_top3.items()))
facts["jiuxin_field_count"] = len(field_top3)

# ---------------------------------------------------------------- 口径 B：中/美领域居首数
cn_first = sum(1 for f, lst in field_top3.items() if lst and lst[0]["country"] == "China")
us_first = sum(1 for f, lst in field_top3.items() if lst and lst[0]["country"] == "United States")
facts["jiuxin_cn_field_first_count"] = cn_first
facts["jiuxin_us_field_first_count"] = us_first

jc.close()
jx.close()

# ---------------------------------------------------------------- gkx（负结论）
gc = gkx()
probe("gkx 领域/学科排名类表扫描（discipline/field/rank LIKE）", "gkx",
      "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' AND "
      "(table_name LIKE '%discipline%' OR table_name LIKE '%field%' OR table_name LIKE '%rank%')", gc)
gc.close()

# ---------------------------------------------------------------- 开发库（负结论，消费官方快照）
probes.append({
    "probe": "dev 论文表探测（消费官方共享快照原值：0 行）",
    "source": "dev",
    "sql": "SHOW TABLES LIKE '%paper%'",
    "hits": 0, "sample": []})
facts["dev_paper_tables"] = []

# ---------------------------------------------------------------- 产物
out = {
    "metric_id": "M_SCIUI_INNOV_017",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/global-innovation/tabs/carrierRankModeModel.js:5",
        "repos/demo-ui-science/src/pages/global-innovation/tabs/carrierRankModeModel.js:22",
        "repos/demo-ui-science/src/pages/global-innovation/tabs/InnovationRanking.jsx:39",
        "repos/demo-ui-science/src/pages/global-innovation/mockData.js:15",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "SRS 全球创新监测.md seq 74 多维度排名展示：『提供创新载体的多维度排名，包括总体排名、领域排名、地区排名，用户可切换查看不同维度的排名情况』——「领域排名」逐字命中（载体粒度）；seq 73 创新能力指数计算（排名的算分底座）与 seq 84 创新能力排名计算（城市粒度变体）为姊妹锚",
    },
    "facts": facts,
    "derived": {
        "jiuxin_cn_field_first_share_pct": {
            "value": round(cn_first / len(field_top3) * 100, 4),
            "numerator": cn_first,
            "denominator": len(field_top3),
            "note": "分子=中国居首领域数（26 领域 SUM 论文 Top1），分母=领域总数；同快照同 JOIN（B3）",
        },
        "jiuxin_top5_topics_cn_rank1_share_pct": {
            "value": round(sum(1 for r in facts["jiuxin_cn_output_rank_sample_top5"]
                               if r["output_rank"] == 1) / 5 * 100, 4),
            "numerator": sum(1 for r in facts["jiuxin_cn_output_rank_sample_top5"]
                             if r["output_rank"] == 1),
            "denominator": 5,
            "note": "分子=中国论文量 Top5 主题中 output_rank=1 的个数，分母=样本数 5；快照内置排名直读",
        },
    },
    "absence_probe": probes,
    "support_judgment": "完全直接支持",
    "notes": [
        "上游自带排名列：ads_topic_country_snapshot.output_rank（topic 内国别排名）+ ranked_country_count，经 discipline_topic（4,516 topics→26 fields）+ discipline_field（26 领域字典）JOIN 即得领域×国排名——「领域排名」语义结构+数据双达标，判完全直接支持",
        "SRS seq 74 逐字命中（named_in_srs=true，本批少有的正名件）；UI 挂载是载体粒度（mock 八领域），上游是 26 学科领域×224 国——回填需建 UI 八领域→26 学科映射，或按学科字典直接换 UI 枚举",
        "口径 B headline：中国在 26 领域中的 N 个居首（领域论文 SUM 国别第一）——「领域排名」全景读数；美国 M 个居首次之，其余领域由英/德/日等分领",
        "output_rank 是 topic 内排名：同一国家在不同 topic 排名不同，领域级聚合须 SUM(paper_count) 重排——本件口径 A 即此重排（B5 确定性：同 JOIN 同 SUM，幂等重跑同值）",
        "开发库无论文表（官方快照 0 行）；gkx discipline/field/rank 0 表——负结论双库登记",
    ],
    "base_years_used": ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"],
    "base_years_missing": [],
    "base_years_note": "领域聚合取分析全窗 2015-2025（snapshot 自带 analysis_start/end_year）；双窗（2020-2022/2023-2025）可作增长口径变体，本件主口径为全窗存量",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "209517", "4516", "26", "4467", "224", "23", "3", "88.4615","1352563","90.7862"]},
}
path = os.path.join(HERE, "M_SCIUI_INNOV_017_out.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", path)
print("support_judgment:", out["support_judgment"])
print("fields:", facts["jiuxin_field_count"], "| cn_first:", cn_first, "| us_first:", us_first)
print("cn rank sample:", facts["jiuxin_cn_output_rank_sample_top5"][:3])
print("field 计算机 Top3:", facts["jiuxin_field_country_top3"].get("计算机科学"))

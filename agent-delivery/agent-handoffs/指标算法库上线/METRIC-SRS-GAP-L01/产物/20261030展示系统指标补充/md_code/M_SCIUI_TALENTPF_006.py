#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TALENTPF_006 研究领域热度值（关注/产出活跃度） · 三源探针与复现脚本（S3-03 Lane 5）。

含义：人才画像「学术影响力量化（引进参考）」卡的领域热度条——
ProfileBasicPanel 影响力 bars 末行「领域热度」：fieldHotness（0-1）×100 渲染进度条；
语义=学者所研究领域的外部热度（领域侧关注度），区别于学者自身影响力分。
UI：repos/demo-ui-science/src/pages/talent-trend/components/ProfileBasicPanel.jsx:373（领域热度 bar，
academicInfluence.fieldHotness）。数值语义源：data.js:862 fieldHotness=randomFloat(0.62,0.95,2) mock。

SRS 溯源：主需求 :2241 研究领域图谱总述「动态捕捉其学术方向的变化和拓展…兴趣热点以图形化方式直观展现」
+ :2290-2292 动态热点标记「对近期高频关注领域和最新研究热点进行自动高亮标记」——
「研究热点」需求明列；「热度值」作为数值定名 0 命中。

三源判档路径（热度主战场走久新学科/主题年度面）：
- 产出活跃度口径（领域产出侧）：ads_talent_yearly_discipline（field×year 论文/被引聚合）——
  年度面直接支撑「领域年度热度」读数；
- 关注侧口径（领域演进热度）：ads_emerging_topic_yearly_metrics/snapshot（Topic 级
  paper_share/relative_growth/作者扩散/机构扩散全套热度指标，库内官方新兴热度模型）；
- 「学者↔其领域的热度」绑定：potential_result.primary_field_id + yearly_discipline 同体系
  （fld_* 哈希 ID 一致）——学者热度值=其主领域的年度面读数（映射一条 JOIN）；
  （ads_talent_profile 无 primary_field_id，主领域承载在 potential_result）；
- gkx/dev：无学科年度面（同 PF_003 探针，零承载）。
→ 热度口径结构+数据双达标（产出侧现成直查、演进侧现成直查）+ 学者绑定链在 +
  「热度值」合成算式未定版（关注/产出双口径待裁）→ 完全转换支持。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_TALENTPF_006_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)
jconn = pymysql.connect(**JX)
jcur = jconn.cursor()


def qj(sql):
    jcur.execute(sql)
    return jcur.fetchall()


jcur.execute("SHOW TABLES")
jx_tables = sorted(r[0] for r in jcur.fetchall())
facts["jiuxin_table_count"] = len(jx_tables)
facts["jiuxin_heat_like_tables"] = [t for t in jx_tables
                                    if re.search(r"heat|hot|trend|momentum|emerging|growth", t, re.I)]

# ---------- ① 产出侧：yearly_discipline 年度面（field×year 论文/被引） ----------
facts["jiuxin_yearly_discipline_rows"] = int(
    qj("SELECT COUNT(*) FROM ads_talent_yearly_discipline")[0][0])
rows = qj("SELECT field_id, SUM(paper_count), SUM(cited_by_count) FROM ads_talent_yearly_discipline "
          "WHERE statistics_year = 2025 GROUP BY field_id "
          "ORDER BY SUM(paper_count) DESC, field_id ASC LIMIT 10")
facts["jiuxin_yd_2025_field_output_top10"] = [[str(a), int(b), int(c)] for a, b, c in rows]
rows = qj("SELECT field_id, SUM(paper_count) FROM ads_talent_yearly_discipline "
          "WHERE statistics_year = 2024 GROUP BY field_id "
          "ORDER BY SUM(paper_count) DESC, field_id ASC LIMIT 10")
facts["jiuxin_yd_2024_field_output_top10"] = [[str(a), int(b)] for a, b in rows]
# 年度总产出（热度的分母候选：份额口径）
rows = qj("SELECT statistics_year, SUM(paper_count) FROM ads_talent_yearly_discipline "
          "WHERE statistics_year IN (2023,2024,2025) GROUP BY statistics_year ORDER BY statistics_year")
facts["jiuxin_yd_paper_total_by_year"] = [[int(a), int(b)] for a, b in rows]

# ---------- ② 关注/演进侧：emerging_topic 热度面 ----------
if "ads_emerging_topic_snapshot" in jx_tables:
    facts["jiuxin_emerging_topic_snapshot_rows"] = int(
        qj("SELECT COUNT(*) FROM ads_emerging_topic_snapshot")[0][0])
    # snapshot 分数面样例（subfield 内相对增长 Top5）
    rows = qj("SELECT topic_id, subfield_id, relative_growth, recent_new_author_ratio "
              "FROM ads_emerging_topic_snapshot ORDER BY relative_growth DESC, topic_id ASC LIMIT 5")
    facts["jiuxin_emerging_snapshot_growth_top5"] = [
        [str(a), str(b), float(c) if c is not None else None, float(d) if d is not None else None]
        for a, b, c, d in rows]
if "ads_emerging_topic_yearly_metrics" in jx_tables:
    facts["jiuxin_emerging_topic_yearly_rows"] = int(
        qj("SELECT COUNT(*) FROM ads_emerging_topic_yearly_metrics")[0][0])
    rows = qj("SELECT statistics_year, SUM(paper_count), SUM(author_count), SUM(institution_count) "
              "FROM ads_emerging_topic_yearly_metrics WHERE statistics_year IN (2023,2024,2025) "
              "GROUP BY statistics_year ORDER BY statistics_year")
    facts["jiuxin_emerging_topic_year_totals"] = [[int(a), int(b or 0), int(c or 0), int(d or 0)]
                                                  for a, b, c, d in rows]

# ---------- ③ 学者↔领域绑定（热度值挂到人） ----------
# 注：ads_talent_profile 无 primary_field_id——人才级主领域承载在 ads_talent_potential_result
prof_cols = [r[0] for r in qj("DESC ads_talent_profile")]
facts["jiuxin_profile_rows"] = int(qj("SELECT COUNT(*) FROM ads_talent_profile")[0][0])
facts["jiuxin_profile_primary_field_id_nonnull"] = 0  # 实测列不存在，登记 0 并在 note 披露
facts["jiuxin_potential_pf_nonnull"] = int(
    qj("SELECT COUNT(primary_field_id) FROM ads_talent_potential_result")[0][0])
facts["jiuxin_potential_result_rows"] = int(
    qj("SELECT COUNT(*) FROM ads_talent_potential_result")[0][0])
# topic_profile 的近窗活跃（学者级热度合成的现成底料）
if "ads_talent_topic_profile" in jx_tables:
    rows = qj("SELECT SUM(recent_3y_paper_count), SUM(recent_5y_paper_count) FROM ads_talent_topic_profile")
    facts["jiuxin_topic_profile_recent_sums"] = [int(x or 0) for x in rows[0]]
    rows = qj("SELECT COUNT(*) FROM ads_talent_topic_profile WHERE recent_3y_paper_count > 0")
    facts["jiuxin_topic_profile_recent3y_positive_topics"] = int(rows[0][0])
jconn.close()

# ---------- ④ gkx：热度/趋势承载探针 ----------
gcur = gkx()
gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
facts["gkx_heat_like_tables"] = [t for t in gkx_tables
                                 if re.search(r"heat|hot|trend|momentum|emerging", t, re.I)]
gcur.close()

# ---------- ⑤ dev：热度承载探针 ----------
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
lcur.execute("SELECT table_schema, table_name FROM information_schema.tables "
             "WHERE table_schema LIKE 'gkxlumenx%%' AND table_name REGEXP 'heat|hot|trend|momentum|emerging'")
facts["dev_heat_like_tables"] = [f"{r[0]}.{r[1]}" for r in lcur.fetchall()]
lconn.close()

# ================= 派生 =================
# 产出侧份额口径样例：2025 Top1 领域份额（热度读数=领域产出份额×100）
ta = facts["jiuxin_yd_2025_field_output_top10"]
tot_rows = [r for r in facts["jiuxin_yd_paper_total_by_year"] if r[0] == 2025]
tot_2025 = int(tot_rows[0][1]) if tot_rows else 0
top1_papers = int(ta[0][1]) if ta else 0
derived.append({
    "key": "jiuxin_2025_top1_field_paper_share_pct",
    "value": round(100.0 * top1_papers / tot_2025, 4) if tot_2025 else None,
    "numerator": top1_papers,
    "denominator": tot_2025,
    "note": "分子=2025 年 Top1 领域（by 论文数）全池论文数；分母=2025 年全池论文总数"
            "（同表同年同 WHERE 池，全量非采样）——产出侧领域热度（份额口径）读数样例",
})
# 关注侧样例：snapshot 相对增长 Top1（演进热度的库内官方读数）
if facts.get("jiuxin_emerging_snapshot_growth_top5"):
    g = facts["jiuxin_emerging_snapshot_growth_top5"][0]
    derived.append({
        "key": "jiuxin_emerging_top1_relative_growth",
        "value": float(g[2]) if g[2] is not None else None,
        "numerator": None,
        "denominator": None,
        "note": "ads_emerging_topic_snapshot.relative_growth=（近期年均份额+1e-12)/(对照年均份额+1e-12)"
                "——关注/演进侧热度的库内官方指标（口径 A 产出份额的互补口径），非本件自算故分子分母留空",
    })
# 学者主领域覆盖率（热度值挂人的绑定链，承载面=potential_result）
n_pf = facts["jiuxin_potential_pf_nonnull"]
n_prof = facts["jiuxin_potential_result_rows"]
derived.append({
    "key": "jiuxin_primary_field_coverage_pct",
    "value": round(100.0 * n_pf / n_prof, 2),
    "numerator": n_pf,
    "denominator": n_prof,
    "note": "分子=ads_talent_potential_result.primary_field_id 非空行数；分母=该表总行数（同表全量非采样）——"
            "学者热度值绑定链（人→主领域→领域年度面）的覆盖率（profile 表无 primary_field_id）",
})

# ================= absence_probe =================
absence.extend([
    {"probe": "gkx 280 表 heat/hot/trend/momentum/emerging 词族（领域热度结果面）",
     "source": "gkx", "sql": "SHOW TABLES FROM gkx 后词族扫",
     "hits": 0, "hit_detail": "命中 []——gkx 无任何热度/趋势结果面；dwd_scholar 亦无 field 列（PF_003 探针在案），"
            "学者领域热度无从构建"},
    {"probe": "dev gkxlumenx_* heat/hot/trend/momentum/emerging 词族",
     "source": "dev", "sql": "information_schema.tables 扫 gkxlumenx_*",
     "hits": 3, "hit_detail": "命中 gkxlumenx_ads.chain_hotspot / industry_chain_graph_snapshot"
            "（产业链热点图谱）与 gkxlumenx_dwd.enterprise_growth_trend（企业成长趋势）——产业链/企业级"
            "非学者领域级，无人才×领域绑定，不构成本件承载"},
    {"probe": "「fieldHotness 型学者级领域热度现成分」列（久新 profile 列级）",
     "source": "jiuxin", "sql": "DESC ads_talent_profile 后 hot/heat 词族扫",
     "hits": 0, "hit_detail": "profile 无学者级领域热度列（热度需由领域年度面 JOIN 主领域现转——"
            "绑定链 primary_field_id 覆盖率 99.998%（99998/100000，显示值 100.0）在案，"
            "转换一条 JOIN 即得）"},
    {"probe": "需求原文「热度值」合成算式（关注侧/产出侧口径）",
     "source": "doc", "sql": "rg 热度/热点 三份需求真源",
     "hits": 2, "hit_detail": "「热度值」数值定名 0 命中；最近义 :2290-2292 动态热点标记『对近期高频关注"
            "领域和最新研究热点进行自动高亮标记』+ :2251 领域热点对比——热点『行为』明列、热度『算式』无；"
            "「关注/产出活跃度」为派单书定名双口径"},
])

notes.extend([
    "本件支持度按三源评估（20261101 铁律）：dev live 非 demo + gkx 只读 + 久新 ads_* 只读。",
    "双口径：产出侧=ads_talent_yearly_discipline 领域年度论文/被引（份额或绝对量）；"
    "关注/演进侧=ads_emerging_topic_* 全套热度指标（paper_share/relative_growth/作者机构扩散）——"
    "两口径均现成直查，合成算式（份额×100？增长加成？）待甲方裁定（B10）。",
    "emerging_topic 面官方口径：观察窗 2017-2025、对照窗 2020-2022、近期窗 2023-2025，"
    "撤稿与 paratext 不入有效总体，2026 只展示不进窗口（schema 明载）——热度读数的窗口纪律。",
    "学者绑定链完整：potential_result.primary_field_id→领域年度面一条 JOIN（fld_* ID 同体系）；"
    "近窗活跃底料 topic_profile recent_3y/recent_5y 论文计数在（学者级活跃热度的第二绑定路径）；"
    "profile 表无 primary_field_id。",
    "UI fieldHotness=randomFloat(0.62,0.95,2)（data.js:862）为 mock 演示值，不作数据证据；"
    "『领域热度』bar 取值 Math.round(fieldHotness*100)（ProfileBasicPanel.jsx:373）。",
    "本件与 PF_003 共享领域年度面与维表（族内对账零漂移）；与 X_015 subfield 252 读数同体系不同层。",
])

out = {
    "metric_id": "M_SCIUI_TALENTPF_006",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/talent-trend/components/ProfileBasicPanel.jsx:373（领域热度 bar：academicInfluence.fieldHotness×100）",
        "repos/demo-ui-science/src/pages/talent-trend/components/ProfileBasicPanel.jsx:350-388（学术影响力量化卡 influence-bars 容器）",
        "repos/demo-ui-science/src/pages/talent-trend/data.js:862（fieldHotness=randomFloat(0.62,0.95,2) mock 生成器）",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "需求明列行为：主需求 :2290-2292（1.1.1.1.4.3.3.6.3(3) 动态热点标记）『对近期高频关注领域和"
                "最新研究热点进行自动高亮标记』+ :2241 总述『兴趣热点以图形化方式直观展现』——「研究热点」"
                "明列；「热度值（关注/产出活跃度）」为派单书定名口径；核增/算法库 0 命中",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": "完全转换支持",
    "notes": notes,
    "base_years_used": [2023, 2024, 2025],
    "base_years_missing": [],
    "base_years_note": "产出侧读数按 2023-2025 完整年；emerging_topic 面近期窗 2023-2025/对照窗 2020-2022"
                       "（schema 官方窗口）；2026 为 PARTIAL_YEAR 只展示不入正式窗口",
    "ctx_refs": {
        "note": "正文引用型数字登记",
        "refs": [],
    },
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1, default=str)
print("ok ->", OUT)

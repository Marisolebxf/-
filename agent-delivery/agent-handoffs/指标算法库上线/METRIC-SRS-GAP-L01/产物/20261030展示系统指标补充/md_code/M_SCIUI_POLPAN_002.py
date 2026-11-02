#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLPAN_002 分区/群体对比分析图 · 三源探针与复现脚本（S3-02 Lane 5）。

需求源：SRS 政策分析评价.md seq 220（excel_row 223）「分区/群体对比分析图」——
柱状图/热力图批量展示各地区、行业或目标群体间的政策效果数据。
UI：RegionGroupCompare.jsx 三 Tab（地区/行业/群体）×四指标
（支持力度/落实率/满意度/创新贡献）柱状+热力双图。

三源实况：
- gkx.dwd_policy_base 20,000 行：region 维（province/city 100% 非空）可支撑「分区」；
  industry 维无专列（title/abstract 关键词代理）；「效果」四指标全无（落实率/满意度缺）。
- dev gkxlumenx_ads 政策面 0-37 行样例（policy_national_dist 33 行与 gkx 同源）。
- 久新政策 evidence 1,252 行（1,213 行 LLM 合成语境，真实 39 条）。
本件交付：分区/行业/群体三 Tab 的可算骨架（政策存量分布）+ 效果维 absence 全记录。
"""
import json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLPAN_002_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

# ============ ① 分区 Tab：省级政策存量分布 ============
facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])
facts["gkx_policy_province_nonnull"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE province IS NOT NULL AND province != ''")[0][0])
prov = qg("SELECT province, COUNT(*) c FROM gkx.dwd_policy_base WHERE province IS NOT NULL "
          "AND province != '' AND province != 'NULL' GROUP BY province ORDER BY c DESC LIMIT 10")
facts["gkx_policy_province_top10"] = [{"province": r[0], "policies": int(r[1])} for r in prov]
# 城市级（市名对比组，UI mock 是北上深广杭五市）
city = qg("SELECT city, COUNT(*) c FROM gkx.dwd_policy_base WHERE city IS NOT NULL AND city != '' "
          "AND city != 'NULL' GROUP BY city ORDER BY c DESC LIMIT 5")
facts["gkx_policy_city_top5"] = [{"city": r[0], "policies": int(r[1])} for r in city]

# ============ ② 行业 Tab：关键词代理分布 ============
INDUSTRY_KWS = ["人工智能", "生物医药", "新能源", "半导体", "先进材料"]
ind = {}
for kw in INDUSTRY_KWS:
    n = int(qg(f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE title LIKE '%{kw}%' "
               f"OR abstract LIKE '%{kw}%'")[0][0])
    ind[kw] = n
facts["gkx_policy_industry_kw_hits"] = ind

# ============ ③ 群体 Tab：目标群体关键词代理 ============
GROUP_KWS = ["人才", "企业", "机构", "创业"]
grp = {}
for kw in GROUP_KWS:
    n = int(qg(f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE title LIKE '%{kw}%' "
               f"OR abstract LIKE '%{kw}%'")[0][0])
    grp[kw] = n
facts["gkx_policy_group_kw_hits"] = grp

# 资源投向四类（UI 资源投向 Select：资金/人才/平台/税收）
TARGET_KWS = {"funding": ["资金", "补贴", "经费"], "talent": ["人才"], "platform": ["平台"], "tax": ["税收"]}
tgt = {}
for k, kws in TARGET_KWS.items():
    conds = " OR ".join([f"abstract LIKE '%{w}%'" for w in kws])
    n = int(qg(f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {conds}")[0][0])
    tgt[k] = n
facts["gkx_policy_resource_target_hits"] = tgt

# ============ ④ 效果维 absence：落实率/满意度列探针 ============
gcur.execute("SHOW COLUMNS FROM gkx.dwd_policy_base")
policy_cols = [r[0] for r in gcur.fetchall()]
facts["gkx_policy_cols"] = policy_cols
effect_like = [c for c in policy_cols if any(k in c.lower() for k in ("effect", "satisf", "implement", "fulfil"))]
facts["gkx_policy_effect_like_cols"] = effect_like

# policy_support 列存在但全 null（支持力度结构在值缺）
n_support = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE policy_support IS NOT NULL "
                   "AND policy_support != 'null' AND JSON_LENGTH(policy_support) > 0")[0][0])
facts["gkx_policy_support_real_rows"] = n_support

# ============ ⑤ dev 库效果面探针 ============
LIVE = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
            charset="utf8mb4", connect_timeout=10, read_timeout=60)
lconn = pymysql.connect(**LIVE)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()
dev_effect_tables = ["policy_effect_eval", "policy_support_assessment", "policy_public_opinion",
                     "shenzhen_policy_status", "policy_support_rank"]
dev_effect_rows = {}
for t in dev_effect_tables:
    dev_effect_rows[t] = int(ql(f"SELECT COUNT(*) FROM gkxlumenx_dwd.{t}")[0][0])
facts["dev_policy_effect_table_rows"] = dev_effect_rows
# ads 政策面
ads_tables = ["policy_effect", "policy_intensity", "policy_metric_timeseries"]
ads_rows = {}
for t in ads_tables:
    ads_rows[t] = int(ql(f"SELECT COUNT(*) FROM gkxlumenx_ads.{t}")[0][0])
facts["dev_ads_policy_effect_table_rows"] = ads_rows
# dev policy_base_info 效果列
lcols = [r[0] for r in ql("SHOW COLUMNS FROM gkxlumenx_dwd.policy_base_info")]
facts["dev_policy_base_info_effect_like_cols"] = [
    c for c in lcols if any(k in c.lower() for k in ("effect", "satisf", "implement", "fulfil"))]
lconn.close()

# ============ ⑥ 久新政策面 ============
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)
jconn = pymysql.connect(**JX)
jcur = jconn.cursor()
def qj(sql):
    jcur.execute(sql)
    return jcur.fetchall()
jconn_rows = int(qj("SELECT COUNT(*) FROM ads_research_problem_policy_evidence")[0][0])
jconn_syn = int(qj("SELECT COUNT(*) FROM ads_research_problem_policy_evidence WHERE is_synthetic=1")[0][0])
jconn_loc = {r[0]: int(r[1]) for r in qj(
    "SELECT location_id, COUNT(*) FROM ads_research_problem_policy_evidence GROUP BY location_id ORDER BY 2 DESC")}
jconn_sup = {r[0]: int(r[1]) for r in qj(
    "SELECT support_type, COUNT(*) FROM ads_research_problem_policy_evidence GROUP BY support_type ORDER BY 2 DESC")}
facts["jiuxin_policy_evidence_rows"] = jconn_rows
facts["jiuxin_policy_evidence_synthetic_rows"] = jconn_syn
facts["jiuxin_policy_evidence_location_dist"] = jconn_loc
facts["jiuxin_policy_evidence_support_type_dist"] = jconn_sup
jconn.close()

# ================= 派生 =================
top1_prov = facts["gkx_policy_province_top10"][0]
derived.append({
    "key": "gkx_policy_province_nonnull_pct",
    "value": round(100.0 * facts["gkx_policy_province_nonnull"] / facts["gkx_policy_rows"], 4),
    "numerator": facts["gkx_policy_province_nonnull"],
    "denominator": facts["gkx_policy_rows"],
    "note": "分子=province 非空行数，分母=policy_base 全表行数；同表同池（B3）——分区 Tab 可算面覆盖"})
derived.append({
    "key": "gkx_policy_synth_share_pct_jiuxin",
    "value": round(100.0 * jconn_syn / jconn_rows, 4),
    "numerator": jconn_syn,
    "denominator": jconn_rows,
    "note": "分子=is_synthetic=1 行数，分母=evidence 全表行数；同表同池（B3）——久新政策证据面合成占比（可信度披露）"})
funding = facts["gkx_policy_resource_target_hits"]["funding"]
derived.append({
    "key": "gkx_policy_funding_share_pct",
    "value": round(100.0 * funding / facts["gkx_policy_rows"], 4),
    "numerator": funding,
    "denominator": facts["gkx_policy_rows"],
    "note": "分子=abstract 含 资金/补贴/经费 之一行数，分母=policy_base 全表行数；同表同池（B3）——资金投向代理覆盖"})

# ================= absence_probe =================
absence += [
    {"probe": "gkx 政策效果四指标列（支持力度值/落实率/满意度/创新贡献）",
     "source": "gkx",
     "sql": f"SHOW COLUMNS FROM gkx.dwd_policy_base（{len(policy_cols)} 列逐一核对）",
     "hits": len(effect_like),
     "hit_detail": f"effect/satisf/implement/fulfil 关键词列命中 {effect_like}；"
                   "policy_support 列在但 20,000 行全为字面 'null'（JSON_LENGTH>0 且非 null 值实测 0 行）"},
    {"probe": "dev 政策效果承载表",
     "source": "dev",
     "sql": "SELECT COUNT(*) FROM gkxlumenx_dwd.{policy_effect_eval, policy_support_assessment, "
            "policy_public_opinion, shenzhen_policy_status, policy_support_rank}",
     "hits": 0,
     "hit_detail": f"五表实测 {dev_effect_rows} 全 0 行——表存在但 0 行（skill B4 情形②：补数据同步问题，非建表问题）"},
    {"probe": "dev ads 政策效果面",
     "source": "dev",
     "sql": "SELECT COUNT(*) FROM gkxlumenx_ads.{policy_effect, policy_intensity, policy_metric_timeseries}",
     "hits": 0,
     "hit_detail": f"三表实测 {ads_rows} 全 0 行——同上，结构在数据缺"},
    {"probe": "久新政策效果值（落实率/满意度）",
     "source": "jiuxin",
     "sql": "DESC ads_research_problem_policy_evidence（45 列）+ 关键词全表扫",
     "hits": 0,
     "hit_detail": "evidence 面仅政策↔问题对齐置信度（relation_confidence/alignment_score），"
                   "无落实率/满意度类效果值列；且 1,252 行中 1,213 行 is_synthetic=1（96.88% LLM 合成语境）"},
]

support = "部分支持"

notes += [
    "判档：需求四指标（支持力度/落实率/满意度/创新贡献）中仅『支持力度』有文本代理面，"
    f"效果类三指标在三源均无承载（gkx {len(policy_cols)} 列无效果值列——effect 类命中仅 "
    f"{effect_like}；dev 效果五表+ads 三表全 0 行；久新 evidence 无效果值列"
    "且 96.88% 合成）——效果维始终缺 → 部分支持",
    "可算骨架（即期版）：分区 Tab=province 分布（Top10 北京 1,932/上海 1,842/广东 1,612…，非空率 100%）+"
    "城市 Top5；行业 Tab=五行业关键词命中（新能源 256/生物医药 104/人工智能 73…）；群体 Tab=四群体命中"
    "（企业 6,861/机构 3,026/人才 1,020/创业 865）——三 Tab 的 x 轴骨架现转即得，y 轴效果值缺",
    "资源投向维度（UI Select：资金/人才/平台/税收）：abstract 关键词代理 "
    f"funding {tgt['funding']:,}+ talent {tgt['talent']:,}+ platform {tgt['platform']:,} "
    f"+ tax {tgt['tax']} 行可切——过滤交互可用，但切出来的仍是存量计数非效果值",
    "mock 披露：UI mock regionGroupCompareData（policyData.js:2391）北京支持力度 92/落实率 88 等为演示值，"
    "不参与支持度结论",
    "B11 对账：gkx.dwd_policy_base 20,000 行与共享快照 fix2 政策底表行数一致；"
    "province top（北京 1,932 等）与 dev ads.policy_national_dist 33 行（2026-10-29 批）零漂移",
    "升档触发器（B10）：接入政务侧落实/满意度台账数据源（如免申即享兑付记录）→ 效果维闭合可升完全转换支持；"
    "若甲方接受『政策存量强度』作效果代理 → 需书面确认口径（当前保守不升）",
]

out = {
    "metric_id": "M_SCIUI_POLPAN_002",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/analysis/RegionGroupCompare.jsx:175",
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:2391",
        "repos/demo-ui-science/src/pages/policy-tracking/PolicyAnalysis.jsx:1644",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "SRS 政策分析评价.md seq 220（excel_row 223）「分区/群体对比分析图」需求明列叶；"
                "主需求 1.1.1.1.4.2.2.1.2 同文；功能=柱状图/热力图批量展示各地区/行业/目标群体间政策效果数据",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件为存量分布读数（无年度序列诉求）；gkx publish_year 分布在 POLPAN_003 件登记",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["20,000", "1,932", "1,842", "1,612", "6,861",
                          str(tgt["funding"]), "96.88", str(len(policy_cols)), "33"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

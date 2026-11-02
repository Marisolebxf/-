#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_041 政策惠及企业税收增长 · 三源探针与复现脚本（S3-03 Lane 1）。

含义：享受过某项科技政策（如补贴、税收优惠）的企业的税收较上期增长（仿真语境为
政策实施后受惠企业群的税收增长贡献，unit 亿元）。
= （本期受惠企业税收 − 上期受惠企业税收）/ 上期受惠企业税收。
UI：repos/demo-ui-science/src/pages/policy-tracking/policyData.js:1834
（policySimulationParams.indicators 第 5 项 { key: 'taxRevenue', label: '税收增长', unit: '亿元' }；
  消费方 simulation/estimate/EstimateWorkbench.jsx 效果预估 Tab）。

三源实况（全部实探，2026-11-01）：
- gkx：dwd_org_annual_financial_info.total_tax_paid 有真实年度税收面（90,926 行财务面中
  1,284 家有非零税收，452 家有 ≥2 年序列）——税收侧原料在；但「受惠企业」界定依赖
  政策×企业兑现台账，该台账 280 表零承载（POLCMP_002 同族缺口）——处理组不可界定。
- dev：enterprise_finance_history 40,239 行无税收列（revenue/rd_investment 在，tax 缺）；
  risk_tax_punish 528 行是税务处罚负面面；政策族兑现类全 0 行。
- 久新：203 张 ads_* 无企业税收面（tax 词根命中是 taxonomy 分类树误中）。
分子分母的「受惠企业群」三源不可界定 → 完全不支持（族级缺口，非税收原料缺口）。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_041_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

# ============ ① gkx：税收面与受惠企业界定探针 ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
# 税收语义表扫
tax_pat = re.compile(r"tax|revenue|invoice|duty", re.I)
facts["gkx_tax_like_tables"] = [t for t in gkx_tables if tax_pat.search(t)]
# 企业年度财务表：税收面原料盘点
facts["gkx_fin_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_org_annual_financial_info")[0][0])
facts["gkx_fin_tax_nonzero_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_org_annual_financial_info WHERE total_tax_paid IS NOT NULL AND total_tax_paid != 0")[0][0])
facts["gkx_orgs_with_tax_nonzero"] = int(qg(
    "SELECT COUNT(DISTINCT org_id) FROM gkx.dwd_org_annual_financial_info WHERE total_tax_paid IS NOT NULL AND total_tax_paid != 0")[0][0])
facts["gkx_orgs_with_2plus_tax_years"] = int(qg(
    "SELECT COUNT(*) FROM (SELECT org_id FROM gkx.dwd_org_annual_financial_info "
    "WHERE total_tax_paid IS NOT NULL AND total_tax_paid != 0 GROUP BY org_id "
    "HAVING COUNT(DISTINCT year)>=2) t")[0][0])
# 税收年度分布（原料面的时间结构）
tax_year = qg("SELECT year, COUNT(*), ROUND(SUM(total_tax_paid),2) FROM gkx.dwd_org_annual_financial_info "
              "WHERE total_tax_paid IS NOT NULL AND total_tax_paid != 0 GROUP BY year ORDER BY year DESC LIMIT 6")
facts["gkx_tax_by_year_top6"] = [[int(r[0]), int(r[1]), float(r[2])] for r in tax_year]
# 税务处罚面（负面旁证）
facts["gkx_tax_punish_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_org_risk_tax_punish")[0][0])
# 受惠企业界定：政策×企业享受台账（POLCMP_002 同法独立跑）
enjoy_pat = re.compile(r"enjoy|benefit|reward|subsid|grant", re.I)
facts["gkx_enjoy_like_tables"] = [t for t in gkx_tables if enjoy_pat.search(t)]
policy_cols = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_policy_base")]
facts["gkx_policy_col_count"] = len(policy_cols)
facts["gkx_policy_enjoy_like_cols"] = [c for c in policy_cols if re.search(r"enjoy|benefit|enterprise|org|company|subsid", c, re.I)]
# 政策文本税收/惠及词命中
facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])
for word, tag in [("税收", "shuishou"), ("惠及", "huiji"), ("减税", "jianshui")]:
    facts[f"gkx_policy_text_{tag}_rows"] = int(qg(
        f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,''),IFNULL(keypoints,'')) LIKE '%{word}%'")[0][0])

# ============ ② dev：税收面与兑现台账探针 ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()
# 税收类表名扫
lcur.execute("SELECT TABLE_NAME, TABLE_SCHEMA FROM information_schema.TABLES WHERE TABLE_SCHEMA IN "
             "('gkxlumenx_dwd','gkxlumenx_ods','gkxlumenx_ads','gkxlumenx_dim') AND TABLE_NAME REGEXP "
             "'tax|revenue|invoice|duty'")
facts["dev_tax_like_tables"] = sorted([[r[1], r[0]] for r in lcur.fetchall()])
# enterprise_finance_history 列盘点（税收列缺失证据）
fin_cols = [r[0] for r in ql("SHOW COLUMNS FROM enterprise_finance_history")]
facts["dev_finhist_rows"] = int(ql("SELECT COUNT(*) FROM enterprise_finance_history")[0][0])
facts["dev_finhist_cols"] = fin_cols
facts["dev_finhist_tax_cols"] = [c for c in fin_cols if re.search(r"tax", c, re.I)]
# risk_tax_punish（负面面）
facts["dev_risk_tax_punish_rows"] = int(ql("SELECT COUNT(*) FROM risk_tax_punish")[0][0])
# 政策族兑现类
dev_policy_rows = {}
for t in ["policy_base_info", "policy_effect_eval", "policy_simulation_result", "enterprise_fund_project"]:
    dev_policy_rows[t] = int(ql(f"SELECT COUNT(*) FROM `{t}`")[0][0])
facts["dev_policy_family_rows"] = dev_policy_rows
lconn.close()

# ============ ③ 久新：企业税收面探针 ============
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)
try:
    jconn = pymysql.connect(**JX)
    jcur = jconn.cursor()
    def qj(sql):
        jcur.execute(sql)
        return jcur.fetchall()
    jcur.execute("SHOW TABLES")
    jx_tables = sorted(r[0] for r in jcur.fetchall())
    facts["jiuxin_table_count"] = len(jx_tables)
    facts["jiuxin_tax_like_tables"] = [t for t in jx_tables if tax_pat.search(t)]
    # 税收/财务语义列扫（表名 taxonomy 误中已在 facts 注记，列扫定位真实财务列）
    target_cols = re.compile(r"tax|revenue|invoice|amount_yuan|turnover", re.I)
    col_hits = {}
    for t in jx_tables:
        try:
            cols = [r[0] for r in qj(f"DESC `{t}`")]
            m = [c for c in cols if target_cols.search(c)]
            if m:
                col_hits[t] = m
        except Exception:  # noqa: BLE001
            pass
    facts["jiuxin_tax_like_cols"] = col_hits
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_unreachable"] = str(e)
    notes.append("久新连接失败按未取证登记（B4：连接失败≠0 行），不参与判档数字")

# ================= 派生（骨架读数，非指标值） =================
# 税收原料面的整体同比（全库口径——证明原料可算但语义是全库非受惠群）
ty = {int(y): (c, s) for y, c, s in facts["gkx_tax_by_year_top6"]}
if 2024 in ty and 2023 in ty and ty[2023][1]:
    derived.append({
        "key": "gkx_tax_sum_2024_yoy_pct_allorgs",
        "value": round(100.0 * (ty[2024][1] - ty[2023][1]) / ty[2023][1], 4),
        "numerator": round(ty[2024][1] - ty[2023][1], 2),
        "denominator": round(ty[2023][1], 2),
        "note": "分子=2024−2023 全库 total_tax_paid 合计差（元），分母=2023 合计；同表同池全库口径（B3）；"
                "语义=全库企业税收面同比（覆盖 45/35 行极窄样本），不是「受惠企业群」税收增长——"
                "受惠群界定零承载，此键仅为证明税收原料的时间差分结构存在",
    })
derived.append({
    "key": "gkx_policy_text_shuishou_share_pct",
    "value": round(100.0 * facts["gkx_policy_text_shuishou_rows"] / facts["gkx_policy_rows"], 4),
    "numerator": facts["gkx_policy_text_shuishou_rows"],
    "denominator": facts["gkx_policy_rows"],
    "note": "分子=文本含「税收」的政策行数（title+content+keypoints 拼串 LIKE），分母=gkx.dwd_policy_base "
            "全表 20,000 行；同表同池（B3）；语义=税收类政策叙述覆盖面，不是受惠企业税收值",
})

# ================= absence_probe =================
absence += [
    {"probe": "gkx 政策×企业享受台账（受惠企业群界定）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx；280 表名扫 enjoy/benefit/reward/subsid/grant + dwd_policy_base 33 列扫",
     "hits": len(facts["gkx_enjoy_like_tables"]) + len(facts["gkx_policy_enjoy_like_cols"]),
     "hit_detail": "表列双扫 0 语义命中（enjoy 族空列表、政策表享受列空列表均在案）——"
                   "「哪些企业享受过哪项政策」关系零承载；税收原料（total_tax_paid）无法被限定到受惠子群"},
    {"probe": "dev 企业税收面",
     "source": "dev",
     "sql": "information_schema.TABLES 扫 tax/revenue/invoice/duty + enterprise_finance_history 列盘点",
     "hits": len(facts["dev_finhist_tax_cols"]),
     "hit_detail": "enterprise_finance_history（40,239 行）18 列无 tax 类列——revenue/main_business_revenue/"
                   "rd_investment 在，税额缺；risk_tax_punish（528 行）是税务违法处罚负面面非纳税额；"
                   "无企业纳税正面表"},
    {"probe": "久新企业税收面",
     "source": "jiuxin",
     "sql": "SHOW TABLES；203 表扫 tax/revenue/invoice/duty + 全表 DESC 列扫 tax/revenue/invoice/amount_yuan/turnover",
     "hits": len(facts.get("jiuxin_tax_like_cols", {})),
     "hit_detail": "表名命中 5 张全是 ads_talent_taxonomy* 分类树（taxonomy 词根误中）；"
                   "列扫命中见 facts.jiuxin_tax_like_cols（taxonomy_id 等分类键误中）——"
                   "无任何企业纳税额/税收贡献结果面"},
    {"probe": "需求原文「税收增长/惠及企业税收」定义段",
     "source": "doc",
     "sql": "rg 税收增长/惠及企业 三份需求真源",
     "hits": 0,
     "hit_detail": "三份需求真源均未出现「税收增长（亿元）」指标名；主需求 1.1.1.1.4.2.3.1 未出台政策仿真"
                   "「经济效益/社会影响/创新促进等方面」是其结果指标语境但无定义；"
                   "语义源=UI mock policySimulationParams.indicators 槽位"},
]

support = "完全不支持"

notes += [
    "判档：惠及企业税收增长 =（本期受惠企业税收−上期）/上期。税收原料在（gkx.dwd_org_annual_financial_info"
    ".total_tax_paid：90,926 行财务面中 1,284 家非零、452 家有 ≥2 年），但「受惠企业群」界定依赖政策×企业"
    "兑现台账——该台账三源零承载（与 POLCMP_002 惠及企业增长共享族级缺口，本件独立留证）。"
    "处理组不可界定 → 全库口径税收同比不等于本指标（混入非受惠企业），判完全不支持",
    "税收原料质量披露：total_tax_paid 年度覆盖极窄（2025:30 行/2024:35 行/2023:45 行…），"
    "且 gkx 财务表单位未标注（元/千元未知）——即使处理组可得，原料量级也需先完成单位裁定（B9 前置）",
    "mock 披露：policyData.js:1834 taxRevenue（税收增长 亿元）是 policySimulationParams 仿真结果指标槽位，"
    "与 POLCMP_002 企业增长/007 创新指数同组 mock——演示值不参与支持度结论",
    "B11 对账：gkx 政策 20,000 行/财务面 90,926 行与共享快照体系零漂移；dev 政策族与 Lane6 探针零漂移",
    "升档触发器（B10）：接入政务兑现台账（受惠企业名单闭合）+ 税务/财务税收面扩容（单位裁定）→ "
    "可升完全转换支持；若甲方接受「全库企业税收同比」代理 → 语义已换（全库≠受惠群），本件不接受",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_041",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:1834",
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:1829",
        "repos/demo-ui-science/src/pages/policy-tracking/simulation/estimate/EstimateWorkbench.jsx:42",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「税收增长」未出现在三份需求真源（政策仿真语境的「经济效益等方面」涵盖其语义但无定义）；"
                "语义源=UI mock policySimulationParams.indicators 第 5 槽位（unit 亿元）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": ["受惠企业各期税收计数/金额序列"],
    "base_years_note": "本件受惠群口径无可算序列（台账零承载）；全库税收面年度分布在 facts（原料证据非基期）",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts["gkx_fin_rows"]), str(facts["gkx_orgs_with_tax_nonzero"]),
                          str(facts["gkx_orgs_with_2plus_tax_years"]), str(facts["gkx_policy_rows"]),
                          str(facts["gkx_policy_text_shuishou_rows"]), str(facts["gkx_policy_text_huiji_rows"]),
                          str(facts["dev_finhist_rows"]), str(facts["gkx_tax_punish_rows"]), "280", "203"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)

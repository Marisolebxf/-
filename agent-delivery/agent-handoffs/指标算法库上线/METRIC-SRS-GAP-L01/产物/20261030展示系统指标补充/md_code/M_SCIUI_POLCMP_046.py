#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_046 综合力度指数 · 三源探针与登记脚本（S3-03 Lane 4）。

含义：科技政策跟踪·政策分析评价（DS-11 三画像）语境下，政策画像卡的 KPI——
「综合力度指数」（policyData.js:2178，演示值 86 分），画像 metrics 行另给
「发布密度 128 项/季」「平均资助强度 3200 万元」等构成暗示。
export 自认「各维度怎么构成、权重怎么定，需要立项调研后才能确定」（裁定 NEW：
政策力度组合口径未调查，无候选）。
语义源：《科技专题服务算法库.md》:1031-1039「政策力度评估模型」——效果/覆盖/成本
三维指标体系加权合成政策力度指数（招标算法库明列，但属服务系统算法非本指标闭合定义）。

三源实况（全部实探，2026-11-01）：
- gkx：dwd_policy_base 33 列无力度类结构化列（唯一扶持列 policy_support 占位全 'null'，
  与 POLCMP_009 共证）；文本面「力度」3,919 行是叙述面非量化面。
- dev：政策族 33+5 表中 **policy_intensity_eval 表结构在**（intensity_index/
  effect_score/coverage_score/cost_score/intensity_level——与算法库三维同构）但 0 行；
  policy_support_rank.intensity_index、policy_time_analysis.intensity_trend_series 同为 0 行。
- 久新：210 张 ads_* 扫 policy/metric/index/quant 命中面与 POLCMP_009 同（24 张类目，
  均为科技活动分析指标面，无政策力度评估面）。
判档：完全不支持（组合口径未立项 + 力度评估结果面三源 0 行——dev 结构同构表在但空，
模型从未跑过；文本叙述面不可替代量化合成）。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_046_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []


def _ser(v):
    from decimal import Decimal
    import datetime as _dt
    if isinstance(v, Decimal):
        return float(v)
    if isinstance(v, (_dt.date, _dt.datetime)):
        return str(v)
    return v


# ============ ① gkx：力度结构化列 + 文本叙述面 ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

policy_cols = [r[0] for r in qg("SHOW COLUMNS FROM gkx.dwd_policy_base")]
facts["gkx_policy_col_count"] = len(policy_cols)
facts["gkx_policy_intensity_cols"] = [c for c in policy_cols if re.search(
    r"intensity|strength|force|power|weight|score|index|rank|level", c, re.I)]
facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])
# 占位列共证（与 009 对账）
facts["gkx_policy_support_nonnull"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE policy_support IS NOT NULL "
    "AND policy_support != ''")[0][0])
facts["gkx_policy_support_distinct_sample"] = [_ser(r[0]) for r in qg(
    "SELECT DISTINCT policy_support FROM gkx.dwd_policy_base WHERE policy_support IS NOT NULL "
    "AND policy_support != '' LIMIT 5")]
# 叙述面（政策自述力度语言——非量化承载）
TF = ("CONCAT_WS(' ',IFNULL(title,''),IFNULL(theme,''),IFNULL(content,''),"
      "IFNULL(keywords,''),IFNULL(keypoints,''))")
facts["gkx_text_lidu_rows"] = int(qg(
    f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {TF} LIKE '%力度%'")[0][0])
facts["gkx_text_lidu_title_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE title LIKE '%力度%'")[0][0])
gcur.close()

# ============ ② dev：力度评估结果面（结构与行数） ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
dconn = pymysql.connect(**DEV)
dcur = dconn.cursor()
# 力度评估主表（算法库三维同构落位）
dcur.execute("SHOW COLUMNS FROM policy_intensity_eval")
facts["dev_policy_intensity_eval_cols"] = [r[0] for r in dcur.fetchall()]
dcur.execute("SELECT COUNT(*) FROM policy_intensity_eval")
facts["dev_policy_intensity_eval_rows"] = int(dcur.fetchone()[0])
# 力度类邻表
for t in ["policy_support_rank", "policy_time_analysis", "policy_support_assessment"]:
    dcur.execute(f"SHOW COLUMNS FROM `{t}`")
    cols = [r[0] for r in dcur.fetchall()]
    dcur.execute(f"SELECT COUNT(*) FROM `{t}`")
    n = int(dcur.fetchone()[0])
    hits = [c for c in cols if re.search(r"intensity|index|score|strength", c, re.I)]
    facts[f"dev_{t}_rows"] = n
    facts[f"dev_{t}_strength_cols"] = hits
dconn.close()

# ============ ③ 久新：政策力度评估面 ============
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)
try:
    jconn = pymysql.connect(**JX)
    jcur = jconn.cursor()
    jcur.execute("SHOW TABLES")
    jx_tables = sorted(r[0] for r in jcur.fetchall())
    facts["jiuxin_table_count"] = len(jx_tables)
    facts["jiuxin_policy_intensity_like_tables"] = [t for t in jx_tables if re.search(
        r"policy|intensity|strength|power", t, re.I)]
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_unreachable"] = str(e)[:120]

# ============ 派生与登记 ============
# 叙述面派生比（同基相除：分子=「力度」命中行，分母=gkx 政策全表）
derived.append({
    "key": "lidu_share_pct",
    "value": round(facts["gkx_text_lidu_rows"] / facts["gkx_policy_rows"] * 100, 3),
    "numerator": facts["gkx_text_lidu_rows"],
    "denominator": facts["gkx_policy_rows"],
    "note": "「力度」叙述面占 gkx 政策全表比（政策自述力度语言的工作量指示器，非量化指数）",
})
# 负结论登记键
derived.append({
    "key": "composite_policy_intensity_index",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "不可算——组合口径未立项（裁定 NEW）；力度评估结果面三源 0 行"
            "（dev policy_intensity_eval 结构在但空，模型从未跑过）",
})

absence = [
    {"probe": "gkx 力度结构化列",
     "source": "gkx",
     "sql": "SHOW COLUMNS FROM dwd_policy_base（33 列）扫 intensity/strength/force/power/"
            "weight/score/index/rank/level",
     "hits": 0,
     "hit_detail": "33 列无力度量化列；唯一扶持列 policy_support 占位全 'null'"
                   "（20,000/20,000，与 POLCMP_009 共证零漂移）"},
    {"probe": "dev 力度评估结果面",
     "source": "dev",
     "sql": "SHOW COLUMNS + COUNT：policy_intensity_eval / policy_support_rank / "
            "policy_time_analysis / policy_support_assessment",
     "hits": 0,
     "hit_detail": "policy_intensity_eval 五列结构与算法库三维同构（intensity_index/effect/"
                   "coverage/cost/intensity_level）但 0 行；邻表含力度列同样 0 行——"
                   "评估模型规划过、从未运行"},
    {"probe": "久新政策力度面",
     "source": "jiuxin",
     "sql": "SHOW TABLES（实测 210 张，探测日 2026-11-01）扫 policy/intensity/strength/power",
     "hits": 0,
     "hit_detail": "policy 词根命中仅 3 张（政策证据/yearly_metrics，语义为关联证据与年度"
                   "计数非力度评估）；intensity/strength/power 词根 0 命中——分析仓无政策"
                   "力度评估面"},
    {"probe": "需求文档定义",
     "source": "doc",
     "sql": "rg 综合力度/力度指数 主需求 + SRS 政策族四文件 + 核增 17 叶；算法库 :1031-1039",
     "hits": 1,
     "hit_detail": "「综合力度指数」指标名三源需求真源 0 命中；算法库 :1031-1039「政策力度"
                   "评估模型」给效果/覆盖/成本三维框架（语义源，非闭合定义——无权重无算式）；"
                   "export 自认需立项调研；父代理裁定 NEW（口径未调查，无候选）"},
]

support = "完全不支持"

notes = [
    "判档：组合口径未立项（裁定 NEW + export 自认）+ 力度结果面三源 0 行。最关键的证据是"
    "dev policy_intensity_eval：五列结构与算法库「政策力度评估模型」效果/覆盖/成本三维"
    "逐列同构（intensity_index/effect_score/coverage_score/cost_score/intensity_level）"
    "——开发库完整规划过该模型落位，但 0 行，模型从未运行。这是「结构在、数据空 + "
    "口径未立项」的双缺叠加形态",
    "语义源链：算法库 :1031-1039 政策力度评估模型（效果维/覆盖维/成本维三类指标+阈值+权重"
    "赋值与综合加权 → 政策力度指数，支持趋势跟踪与排行榜）是招标算法库明列算法——"
    "但它是科技专题服务系统侧算法，未给权重表与算式；UI 政策画像卡（policyData.js:2178 "
    "kpi 86 分 + metrics「发布密度 128 项/季/平均资助强度 3200 万元」）的演示值暗示组合"
    "维度但无权重。学术方法族（R2 四维框架：力度=颁布层级+协同度；R3 PMC 指数；熵权/AHP+"
    "TOPSIS）可补口径，但输入侧（资助金额结构化、层级评分）库内仍缺",
    "文本叙述面边界：「力度」3,919 行（title 层 23 行）是政策自述力度语言（「加大支持"
    "力度」类修辞），非量化承载；叙述面占比 19.595% 只说明力度是高频政策词汇，不可作为"
    "指数输入。gkx 33 列无力度列、policy_support 占位（与 POLCMP_009 探针零漂移）",
    "UI mock 披露：policyData.js:2178 政策画像卡 KPI「综合力度指数 86 分」与 metrics 四行"
    "（发布密度/平均资助强度/跨部门协同率/免申即享占比）是 DS-11 Wave0 扩展 mock 常量"
    "（演示值不参与支持度结论）——metrics 行恰与本批 053（跨部门协同率）交叉，"
    "mock 作者把两者设计为同一画像卡的组成读数",
    "升档触发器（B10）：①力度评估模型立项（算法库三维框架 + 学术赋权方法族定权重）+ "
    "输入侧结构化（资助金额抽取/层级评分回填）+ dev policy_intensity_eval 模型运行回填 "
    "→ 升完全转换支持；②若甲方接受「政策文本 PMC 指数类」纯文本评价口径 → 需 NLP 量化"
    "管线立项（与 POLCMP_009 抽取管线共享），单独一条转换路径",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_046",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:2178",
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:2183",
        "repos/demo-ui-science/src/pages/policy-tracking/analysis/PortraitTrio.jsx:40",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「综合力度指数」指标名三份需求真源 0 命中；语义源=算法库 :1031-1039 政策"
                "力度评估模型（效果/覆盖/成本三维，无权重无算式）；UI DS-11 政策画像卡"
                "（PortraitTrio 消费）是唯一实证；export 自认口径需立项调研",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "指数无年度序列（口径未闭合、结果面 0 行）",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts.get("gkx_text_lidu_rows", "")),
                          str(facts.get("gkx_text_lidu_title_rows", "")),
                          str(facts.get("gkx_policy_rows", "")),
                          str(facts.get("jiuxin_table_count", "")),
                          "86", "128", "3200"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", OUT)

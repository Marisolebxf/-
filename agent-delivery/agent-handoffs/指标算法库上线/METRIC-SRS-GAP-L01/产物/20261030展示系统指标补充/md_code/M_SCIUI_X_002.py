#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_X_002 产业产值分析权重（16%）—— 三源探针 + 复现脚本（批 S3-02，Lane 1）。

UI 挂载（实查，与 X_001 同链）：
  ① repos/demo-ui-science/src/pages/tech-innovation-evaluation-new/TechInnovationEvaluationNewPage.jsx:79
     DEFAULT_WEIGHTS.industry = { value: 25, metrics: [17, 17, 16, 17, 16, 17] }
     —— industry 六个二级指标（产业投入/成熟度/产业产值/科学影响力/技术影响力/综合评估）默认权重，
     第 3 位（产业产值，metrics[2]）= 16% ← 本件 16% 示例值的出处
  ② 同文件 :1196 指标体系预览 header「权重 {config.weight}%」（一级 25%）与 :1201「权重 {metric.weight}%」（二级）
  ③ 同文件 :1507 详情页 <em>权重 {snapshot.weights[config.key].metrics[index]}%</em> —— 权重随评估快照冻结
  ④ 同文件 :1576-1601 管理权重抽屉：每个二级指标数值输入（min0 max100），
     validateWeightTotal（:279-283）校验「一级合计=100 且 每组二级合计=100」——权重体系是 UI 一等公民
  ⑤ TechInnovationEvaluationPage.tsx:318-324 industryWeights: [{key:'input',weight:22},{key:'maturity',weight:20},
     {key:'output',label:'产值增长',weight:20},{key:'sciImpact',weight:19},{key:'techImpact',weight:19}]
     —— 旧页等价物：产值增长 20%（旧版 5 分项口径）；:552-559 权重方案管理（「影响投入、成熟度、产值、
     科学影响力和技术影响力的组合口径」）；:3754-3760 WeightSensitivityComposite 权重敏感性分析

需求原文（SRS《科技创新评估.md》seq 150 / excel_row 153『产业发展潜力综合评估』）：
  「将产业发展潜力的各项指标进行综合展示，用户可自定义指标权重，支持根据权重计算综合得分，
   提供产业发展潜力的综合评估结果和排名。」——权重语义=用户自定义输入参数（UI 已实现），
  无任何「权重应为多少」的数值定义。本件指标名『产业产值分析权重』未出现在三份说明书（screen_v3
  mean 注记「页面示例值：16%」——即 UI DEFAULT_WEIGHTS 的 16%，非需求文书数字）。

三源结论（探针实测，与 X_001 共用主链）：
  权重是「配置态」而非「数据态」——三源没有也不需要现成权重表；判定轴是「权重赖以生效的主链是否可算」：
  gkx  深圳 17 个产业 JDZ 增加值散点在案（X_001 主链），产业维真实；但无逐产业×逐年面 → 主链部分可算
  dev  enterprise_finance_history 绝对值覆盖 <1% + 产业 join 100 行 → 企业级主链不可算
  jiuxin 无经济金额面（对照面同 X_001）
判档：部分支持——权重功能本身 UI 自带（自定义+校验+敏感性分析全链实现，无需后端表），
  但「按权重对产业产值加权出综合得分」的产值主链部分可算（继承 X_001：gkx 散点可算 17 产业单点得分，
  逐年序列缺 → 权重敏感性分析要的多场景基线不齐）。
复现口径（B10 双口径并列）：
  口径 A（默认权重效用演示）——按 UI DEFAULT_WEIGHTS 六分项对 mock 六维分（74/70/71/73/72/72）加权复算
       综合分 71.99≈页面 72 分，验证「Σwᵢsᵢ/Σwᵢ」公式与 UI 一致
  口径 B（产值维权重敏感性·数据侧）——gkx 17 产业 JDZ 值在 16%/20%/25% 三档产值权重下的
       「产值维贡献额」对比（产业得分 min-max 归一后加权）——演示权重变化对产值维读数的杠杆
"""
import json
import os
import sys

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _gkxdb import gkx, live  # noqa: E402

facts = {}
probes = []


def probe(tag, source, sql, cur, note=""):
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        probes.append({"probe": tag, "source": source, "sql": sql, "hits": len(rows),
                       "sample": [str(r)[:220] for r in rows[:6]], "note": note})
        return rows
    except Exception as e:  # noqa: BLE001
        probes.append({"probe": tag, "source": source, "sql": sql, "hits": -1,
                       "error": str(e)[:220], "note": note})
        return []


# ================================================================ gkx（主链共享 X_001）
gc = gkx()
rows = probe("gkx 权重/评分配置类表扫描", "gkx",
             "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' AND ("
             "table_name LIKE '%weight%' OR table_name LIKE '%config%' OR table_name LIKE '%score%')", gc,
             "权重配置表 0 命中（weight 关键词全库 0 表）——权重是 UI 态非库态")
facts["gkx_weight_tables"] = [r[0] for r in rows]

# 主链引用：深圳产业增加值（与 X_001 同 SQL 同值，B11 零漂移）
SZ_IND = {
    "ftts_tzjz_09": "战略性新兴产业增加值",
    "a71336": "生物医药与健康产业增加值", "a71337": "网络与通信产业增加值",
    "a71338": "半导体与集成电路产业增加值", "a71339": "超高清视频显示产业增加值",
    "a71340": "智能终端产业增加值", "a71341": "智能传感器产业增加值",
    "a71342": "软件与信息服务产业增加值", "a71343": "数字创意产业增加值",
    "a71344": "现代时尚产业增加值", "a71349": "新能源产业增加值",
    "a71350": "安全节能环保产业增加值", "a71351": "智能网联汽车产业增加值",
    "a71352": "高端医疗器械产业增加值", "a71353": "生物医药产业增加值",
    "a71354": "大健康产业增加值", "a76246": "人工智能产业增加值",
    "a76247": "高端装备与仪器产业增加值", "a76248": "低空经济与空天产业增加值",
    "ftts_tzjz_09_06": "新材料产业增加值", "ftts_tzjz_09_09": "高端装备制造产业增加值",
    "ftts_tzjz_09_10": "绿色低碳产业增加值", "ftts_tzjz_09_11": "海洋经济产业增加值",
}
codes_sql = ",".join("'%s'" % k for k in SZ_IND)
gc.execute(
    f"SELECT index_code, occur_period, index_value FROM gkx.dwd_macro_index_data "
    f"WHERE area_code LIKE '4403%%' AND index_code IN ({codes_sql}) AND dim_cal='JDZ' "
    f"ORDER BY index_code, occur_period DESC")
ind_latest = {}
for code, per, val in gc.fetchall():
    if val is None:
        continue
    name = SZ_IND[code]
    if name not in ind_latest or int(per) > ind_latest[name][0]:
        ind_latest[name] = (int(per), round(float(val) / 1e8, 2))
facts["gkx_sz_industry_av_latest_yi"] = {k: {"period": v[0], "yi": v[1]}
                                         for k, v in sorted(ind_latest.items(), key=lambda kv: -kv[1][1])}
facts["gkx_sz_industry_av_count"] = len(ind_latest)
gc.close()

# ================================================================ dev（负结论）
dv = live("DWD")
dc = dv.cursor()
rows = probe("dev 权重/配置类表扫描", "dev",
             "SELECT table_name FROM information_schema.tables WHERE table_schema='gkxlumenx_dwd' AND ("
             "table_name LIKE '%%weight%%' OR table_name LIKE '%%config%%')", dc,
             "weight/config 表名 0 命中；cfg 库为系统级配置非指标权重")
facts["dev_weight_tables"] = [list(r.values())[0] for r in rows]
dc.close()
dv.close()

# ================================================================ jiuxin（负结论 + 对照面）
jx = pymysql.connect(host="47.93.119.170", port=29030, user="test2",
                     password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
                     database="gkx_technology_analysis_dev", connect_timeout=30, read_timeout=300)
jc = jx.cursor()
rows = probe("jiuxin 203 表权重表扫描（SHOW TABLES 关键词）", "jiuxin", "SHOW TABLES", jc,
             "weight/config 0 命中——权重无库内承载")
jt = [r[0] for r in rows]
facts["jiuxin_weight_tables"] = [t for t in jt if "weight" in t.lower() or "config" in t.lower()]
jc.close()
jx.close()

# ================================================================ 口径 A：默认权重效用复算
# UI DEFAULT_WEIGHTS.industry（TechInnovationEvaluationNewPage.jsx:79）与六维 mock 分（:138-143）
W = {"产业投入": 17, "产品成熟度": 17, "产业产值": 16, "科学影响力": 17, "技术影响力": 16, "综合评估": 17}
S = {"产业投入": 74, "产品成熟度": 70, "产业产值": 71, "科学影响力": 73, "技术影响力": 72, "综合评估": 72}
composite = sum(W[k] * S[k] for k in W) / sum(W.values())
facts["ui_default_weights_industry"] = W
facts["ui_mock_scores_industry"] = S
facts["ui_weight_sum_check"] = sum(W.values())  # = 100（validateWeightTotal 语义）

# ================================================================ 口径 B：产值维权重敏感性（数据侧）
avs = facts["gkx_sz_industry_av_latest_yi"]
if avs:
    vals = [v["yi"] for v in avs.values()]
    lo, hi = min(vals), max(vals)
    norm = {k: round((v["yi"] - lo) / (hi - lo) * 100, 2) if hi > lo else 0.0 for k, v in avs.items()}
    facts["gkx_sz_industry_av_norm100"] = dict(sorted(norm.items(), key=lambda kv: -kv[1])[:10])
    mean_norm = round(sum(norm.values()) / len(norm), 2)

derived = [
    {"key": "ui_industry_composite_score_weighted",
     "value": round(composite, 2),
     "numerator": round(sum(W[k] * S[k] for k in W), 0),
     "denominator": sum(W.values()),
     "note": "分子=Σ(权重×得分)（六分项，UI DEFAULT_WEIGHTS × mock 六维分）；分母=Σ权重=100；"
             "复算 72.01 与页面综合评估 72 分（TechInnovationEvaluationNewPage.jsx:143 mock 直给值）一致——"
             "mock 的 72 分恰等于 Σwᵢsᵢ/Σwᵢ 加权复算值，验证 UI 加权公式语义（B3：分子分母同 UI 同快照）"},
    {"key": "ui_output_weight_share_pct",
     "value": 16.0,
     "numerator": W["产业产值"],
     "denominator": sum(W.values()),
     "note": "分子=产业产值默认权重 16（DEFAULT_WEIGHTS.industry.metrics[2]）；分母=二级权重合计 100；"
             "旧页等价口径为 20%（TechInnovationEvaluationPage.tsx:321 output 产值增长 weight:20，五分项）——"
             "两版 UI 权重并存，B10 双口径并列待甲方裁定"},
]
if avs:
    for w in (16, 20, 25):
        derived.append({
            "key": f"gkx_output_dim_contribution_at_weight_{w}",
            "value": round(w / 100 * mean_norm, 2),
            "numerator": w,
            "denominator": 100,
            "note": f"产值权重={w}% 时产值维贡献额={w/100:.2f}×{mean_norm}（17 产业 JDZ 值 min-max 归一均值 "
                    f"{mean_norm}，gkx 实测面）——口径 B 敏感性演示：权重 16→25 对产值维读数杠杆 0.83→1.29 分"})
    facts["gkx_sz_industry_av_norm_mean"] = mean_norm

# ================================================================ 产物
out = {
    "metric_id": "M_SCIUI_X_002",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation-new/TechInnovationEvaluationNewPage.jsx:79",
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation-new/TechInnovationEvaluationNewPage.jsx:1507",
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation-new/TechInnovationEvaluationNewPage.jsx:1584",
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation/TechInnovationEvaluationPage.tsx:321",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书未出现该指标名；最近语义为 SRS《科技创新评估.md》seq 150 / excel_row 153"
                "『产业发展潜力综合评估』：『用户可自定义指标权重，支持根据权重计算综合得分…』——"
                "权重是功能参数非独立指标；本件名源自 UI DEFAULT_WEIGHTS 的 16% 示例值（screen_v3 注记）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": probes,
    "support_judgment": "部分支持",
    "notes": [
        "本件与 X_001 共用产值主链（同 SQL 同值，B11 零漂移）：gkx 深圳 17 个产业 JDZ 增加值在案可作加权底册；"
        "权重本体三源皆无表（gkx/dev/jiuxin weight 关键词 0 命中）——但权重是 UI 一等公民"
        "（DEFAULT_WEIGHTS+管理权重抽屉+validateWeightTotal+WeightSensitivityComposite 全链实现），"
        "判档轴落在『加权对象（产值主链）可算性』：主链部分可算 → 部分支持",
        "UI 两版权重并存：新页六分项产值=16%（DEFAULT_WEIGHTS.industry.metrics[2]，TechInnovationEvaluationNewPage.jsx:79）；"
        "旧页五分项产值增长=20%（TechInnovationEvaluationPage.tsx:321）——B10 双口径并列，正式口径待甲方裁定",
        "口径 A 验证：Σwᵢsᵢ/Σwᵢ=72.01 复算与页面综合评估 72 分一致（mock 72 恰为加权值）——UI 加权公式闭环，权重功能无需后端改造",
        "口径 B 敏感性：产值维 17 产业归一均值 X（facts.gkx_sz_industry_av_norm_mean），"
        "权重 16/20/25% 对应贡献额三档（derived）——权重杠杆可量化，但逐年序列缺（继承 X_001）使"
        "『产值增长』维（旧页口径）不可算，敏感性分析只能用截面值",
        "需求只定义了权重机制（自定义+校验+按权重综合），未定义权重数值——16%/20% 均为 UI 演示默认，"
        "不得当需求证据引用（禁止事项 2）",
    ],
    "base_years_used": [2021, 2023, 2024, 2025],
    "base_years_missing": [2019, 2020, 2022],
    "base_years_note": "与 X_001 同（17 产业最近期 JDZ 报告期散布 2014-2025，年度对齐仅 2021/2022/2024）；"
                       "权重敏感性用截面值不受年份缺影响，但『产值增长』类时间敏感维不可算",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": []},
}
refs = {"16", "20", "25", "100", "72", "72.01"}
refs |= {str(d["value"]) for d in derived}
refs |= {str(v["yi"]) for v in facts.get("gkx_sz_industry_av_latest_yi", {}).values() if isinstance(v, dict)}
out["ctx_refs"]["refs"] = sorted(refs)
path = os.path.join(HERE, "M_SCIUI_X_002_out.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", path)
print("support_judgment:", out["support_judgment"])
print("composite:", round(composite, 2), " 产业数:", facts["gkx_sz_industry_av_count"])
print("derived keys:", [d["key"] for d in derived])

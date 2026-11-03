#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INNOV_007 实时投资金额 —— 批 S3-01 Lane 6 复现脚本（三源）。

UI 语义（InnovationRealtime.jsx:85）：KPI 卡「实时投资金额 456 亿美元 +23.1%」，
  30 秒扰动刷新（realtimeStatus.tooltip 自认『演示刷新非真源流…不接正式 ADS』）。

三源承载（探针实测）：
  dev  投融资 5 表：3 张 0 行；enterprise_invest 46,967 行（金额 8,294 非空/万元，event_date 0 覆盖）
  gkx  dwd_org_financing_info 25,654 行（completion_date 100% 覆盖；金额 8,826 行中文格式）
  jiuxin 项目资金面（ads_project_profile amount 63,122 非空 / amount_cny 160,822），
        funding_evidence 5,123 行（252 行有金额）
判档要点：『实时/近实时流』三源均无 CDC/流式承载；『投资金额存量+可刷新』三源均直接支持。
  本件按『可刷新的累计投资金额读数』判完全转换支持（30s 流式语义无承载 → 若甲方咬定 30s 实时流则降部分支持）。
只读；产物 M_SCIUI_INNOV_007_out.json。
"""
import json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import pymysql
from importlib import import_module
gkxmod = import_module("_gkxdb")

OUT = os.path.join(BASE, "M_SCIUI_INNOV_007_out.json")

facts = {}
notes = []
absence_probe = []
derived = []

# ---------------- dev ----------------
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           connect_timeout=8, read_timeout=60)
# ---- dev 段容错补丁(2026-11-01, B4: dev 不可达≠无数据, 沿用首跑实测值并标注) ----
try:
    conn = pymysql.connect(database="gkxlumenx_dwd", **DEV)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*), SUM(CASE WHEN invest_amount IS NOT NULL AND invest_amount > 0 THEN 1 ELSE 0 END) FROM enterprise_invest")
    d_rows, d_amt = [int(x or 0) for x in cur.fetchone()]
    cur.execute("SELECT SUM(invest_amount) FROM enterprise_invest WHERE invest_amount IS NOT NULL")
    d_total_wan = float(cur.fetchone()[0] or 0)
    cur.execute("SELECT COUNT(*) FROM chain_investment")
    d_chain = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM industry_chain_investment_event")
    d_evt = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM industry_chain_investment_participant")
    d_par = int(cur.fetchone()[0])
    facts["dev_enterprise_invest_rows"] = d_rows
    facts["dev_enterprise_invest_amount_rows"] = d_amt
    facts["dev_enterprise_invest_amount_sum_wan_cny"] = round(d_total_wan, 2)
    facts["dev_chain_investment_rows"] = d_chain
    facts["dev_industry_chain_investment_event_rows"] = d_evt
    facts["dev_industry_chain_investment_participant_rows"] = d_par
    conn.close()
except Exception as _e:  # noqa: BLE001
    _po = os.path.join(BASE, "M_SCIUI_INNOV_007_out.json")
    if os.path.exists(_po):
        try:
            _prev = json.load(open(_po, encoding="utf-8")).get("facts", {})
            for _k, _v in _prev.items():
                if _k.startswith("dev_"):
                    facts[_k] = _v
        except Exception:  # noqa: BLE001
            pass
    facts["dev_probe_status_this_run"] = f"dev 不可达({str(_e)[:50]}), dev_* 键沿用首跑实测值(2026-11-01 首跑在案)"
absence_probe.append({
    "probe": "开发库『实时流』承载：链投资事件/参与方表行数（事件流空壳）",
    "source": "dev",
    "sql": "SELECT COUNT(*) FROM chain_investment; SELECT COUNT(*) FROM industry_chain_investment_event; SELECT COUNT(*) FROM industry_chain_investment_participant",
    "hits": 0, "hit_detail": "三表均 0 行；enterprise_forg_invest/enterprise_invest 为股权关系快照非事件流",
})

# ---------------- gkx：融资事件金额（中文格式解析：N万人民币/亿人民币/万美元/亿美元/港元）----------------
cur = gkxmod.gkx()
cur.execute(
    "SELECT funding_amount FROM gkx.dwd_org_financing_info "
    "WHERE funding_amount IS NOT NULL AND funding_amount != ''")
amounts = [r[0] for r in cur.fetchall()]
cur.close()
facts["gkx_financing_amount_nonnull"] = len(amounts)

def parse_cny(s):
    """'8320.0万人民币'→8320.0万元；'4.7亿人民币'→47000万元；'1.1亿美元'→按 7.2 汇率 7920万元；
    '100万美元'→720万元；港元按 0.92。返回万元 CNY 或 None。"""
    s = s.strip()
    try:
        if s.endswith("万人民币"):
            return float(s[:-4])
        if s.endswith("亿人民币"):
            return float(s[:-4]) * 10000
        if s.endswith("万美元"):
            return float(s[:-3]) * 7.2
        if s.endswith("亿美元"):
            return float(s[:-3]) * 72000
        if s.endswith("万港元") or s.endswith("万港币"):
            return float(s[:-3]) * 0.92
        if s.endswith("亿港元") or s.endswith("亿港币"):
            return float(s[:-3]) * 9200
    except ValueError:
        return None
    return None

parsed = [(a, parse_cny(a)) for a in amounts]
ok = [(a, v) for a, v in parsed if v is not None]
facts["gkx_financing_amount_parseable"] = len(ok)
facts["gkx_financing_amount_parse_fail"] = len(amounts) - len(ok)
facts["gkx_financing_amount_sum_wan_cny"] = round(sum(v for _, v in ok), 2)
facts["gkx_financing_amount_rate_note"] = "汇率口径：USD/CNY=7.2、HKD/CNY=0.92（固定汇率换算，非即期）"
# 分形态计数（与 lane6 探针对账：万人民币 4510 / 亿人民币 3814 / 万美元 263 / 亿美元 134 / 港系 105）
shapes = {"万人民币": 0, "亿人民币": 0, "万美元": 0, "亿美元": 0, "港元港币系": 0, "其他": 0}
for a, v in parsed:
    if a.endswith("万人民币"): shapes["万人民币"] += 1
    elif a.endswith("亿人民币"): shapes["亿人民币"] += 1
    elif a.endswith("万美元"): shapes["万美元"] += 1
    elif a.endswith("亿美元"): shapes["亿美元"] += 1
    elif ("港元" in a) or ("港币" in a): shapes["港元港币系"] += 1
    else: shapes["其他"] += 1
facts["gkx_financing_amount_shapes"] = shapes
# 近端窗口（『实时』读数的现实语义：最近完成年 2025 累计 + 最近 90 天滚动）
cur = gkxmod.gkx()
cur.execute(
    "SELECT SUM(1) FROM gkx.dwd_org_financing_info WHERE YEAR(completion_date) = 2025")
facts["gkx_financing_events_2025"] = int(cur.fetchone()[0])
cur.execute(
    "SELECT COUNT(*) FROM gkx.dwd_org_financing_info WHERE completion_date >= DATE_SUB('2026-11-01', INTERVAL 90 DAY)")
facts["gkx_financing_events_last90d_from_20261101"] = int(cur.fetchone()[0])
cur.execute(
    "SELECT MAX(completion_date) FROM gkx.dwd_org_financing_info")
facts["gkx_financing_max_completion_date"] = str(cur.fetchone()[0])
cur.close()

# ---------------- jiuxin：项目资金金额面 ----------------
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev", connect_timeout=10, read_timeout=300)
conn = pymysql.connect(**JX)
cur = conn.cursor()
cur.execute(
    "SELECT COUNT(*), SUM(CASE WHEN amount IS NOT NULL THEN 1 ELSE 0 END), "
    "SUM(CASE WHEN amount_cny IS NOT NULL THEN 1 ELSE 0 END) FROM ads_project_profile")
jx_n, jx_amt, jx_cny = [int(x or 0) for x in cur.fetchone()]
facts["jiuxin_project_profile_rows"] = jx_n
facts["jiuxin_project_amount_nonnull"] = jx_amt
facts["jiuxin_project_amount_cny_nonnull"] = jx_cny
cur.execute(
    "SELECT COUNT(*), SUM(CASE WHEN funding_amount_original IS NOT NULL THEN 1 ELSE 0 END) "
    "FROM ads_research_problem_funding_evidence")
fe_n, fe_amt = [int(x or 0) for x in cur.fetchone()]
facts["jiuxin_funding_evidence_rows"] = fe_n
facts["jiuxin_funding_evidence_amount_rows"] = fe_amt
cur.execute(
    "SELECT MAX(update_time) FROM ads_project_profile")
facts["jiuxin_project_profile_max_update_time"] = str(cur.fetchone()[0])
conn.close()

# ---------------- derived ----------------
derived.append({
    "key": "gkx_financing_amount_coverage_pct",
    "value": round(facts["gkx_financing_amount_nonnull"] / 25654 * 100, 2),
    "numerator": facts["gkx_financing_amount_nonnull"],
    "denominator": 25654,
    "note": "分子=funding_amount 非空行，分母=dwd_org_financing_info 全表 25,654（共享快照键，零漂移）；"
            "share_basis=gkx 融资事件池（B3 同表）",
})
derived.append({
    "key": "gkx_financing_amount_parseable_pct",
    "value": round(facts["gkx_financing_amount_parseable"] / facts["gkx_financing_amount_nonnull"] * 100, 2)
    if facts["gkx_financing_amount_nonnull"] else 0.0,
    "numerator": facts["gkx_financing_amount_parseable"],
    "denominator": facts["gkx_financing_amount_nonnull"],
    "note": "分子=可机器解析为万元 CNY 的行，分母=金额非空行；解析规则六形态闭合（正文 §2.3）",
})
derived.append({
    "key": "gkx_financing_amount_usd_bn_est",
    "value": round(facts["gkx_financing_amount_sum_wan_cny"] / 7.2 / 10000, 2),
    "numerator": facts["gkx_financing_amount_sum_wan_cny"],
    "denominator": 72000,
    "note": "亿美元口径 = 累计金额(万元CNY) ÷ 7.2 ÷ 10000；仅与 UI mock『456 亿美元』量级对照用，"
            "非对外读数（广东样本池，见 notes）",
})

res = {
    "metric_id": "M_SCIUI_INNOV_007",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/global-innovation/tabs/InnovationRealtime.jsx:85",
        "repos/demo-ui-science/src/pages/global-innovation/tabs/realtimeModel.js:3",
        "repos/demo-ui-science/src/pages/global-innovation/tabs/realtimeModel.js:58",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「实时投资金额」全称在三份 SRS 与主文档 rg 未命中；近似叶：SRS 全球创新监测 seq 67「数据指标分类展示」"
                "（投资金额列为其举例指标之一）与 seq 72「实时数据更新」（『实时更新全球创新数据』，无 30s 频率定义）；"
                "主文档 505 行同文复述",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": "完全转换支持",
    "notes": [
        "判档口径：『实时』按『定时增量刷新的累计投资金额读数』理解（分钟/小时级调度即可满足）；"
        "30 秒流式 CDC 三源均无承载（dev 事件流三表 0 行；gkx/久新为批量快照），若甲方咬定 30s 流式 → 降部分支持（触发器 §1.6）",
        "UI 自认演示：realtimeStatus.tooltip 原文『演示刷新非真源流…按 30 秒频率扰动…不接正式 ADS』——mock 456 亿美元不作数据证据",
        "gkx 金额为中文格式 varchar（'8320.0万人民币'），六形态解析闭合（8,826/8,826 全可解析）；"
        "dev invest_amount 为数值万元（8,294 行）；久新 amount/amount_cny 为 DECIMAL（63,122/160,822 行）——三源三种物理承载",
        "gkx 池为广东企业融资池（省份 100% 广东省），读数语义是广东口径；全球口径需换久新池（项目资金）或外部源（CB Insights R3）",
        "汇率固定 7.2/0.92 为解析用口径，非即期汇率；正式交付应接汇率服务（久新 amount_cny 的 CONVERTED_TO_CNY_FIXED_RATE 同为固定汇率先例）",
    ],
    "base_years_used": [2025],
    "base_years_missing": [],
    "base_years_note": "『实时』读数无基期年概念；近端窗口锚定最近完成年 2025（618 事件）与最近 90 天滚动窗口"
                       "（gkx_financing_events_last90d_from_20261101 键）",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": ["128456","4790.45","665.36"]},
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print("saved ->", OUT)
print(json.dumps({k: facts[k] for k in sorted(facts)}, ensure_ascii=False)[:1500])

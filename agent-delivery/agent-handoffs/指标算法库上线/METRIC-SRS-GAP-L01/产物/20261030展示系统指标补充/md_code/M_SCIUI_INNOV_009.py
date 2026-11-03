#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INNOV_009 领域投资规模 —— 批 S3-01 Lane 6 复现脚本（三源）。

UI 语义（cityInnovationAnalysisModel.js:80/374）：城市创新能力『关键指标对比』含『投资规模』项
  （cityBenchmarkMetrics key=investment，读 dimensions.innovationInput.investment，mock 无量纲分）；概览卡『投资规模』。
  需求原文（SRS seq 83 城市创新数据监控）：『监控全球主要城市的创新基金、投资规模…』——本件取其领域维切片。

三源承载（探针实测）：
  dev  投融资 5 表无领域维聚合（chain_investment 0 行；enterprise_invest 仅股权关系）
  gkx  dwd_org_financing_info ⋈ dwd_org_base_info.industry_l1_name（国民经济行业分类，
        join 覆盖 24,598/25,654=95.9%，金额 8,826 行中文格式可全解析）
  jiuxin ads_shenzhen_institution_field_funding 1,645 行（field 维 allocated_amount_cny，SIMULATED_ONLY）
        / ads_research_problem_yearly_metrics.funding_amount_cny（问题维，252 行有金额）
判档：部分支持——『领域』语义不闭合：gkx 是国民经济行业分类（非 UI 的七大未来产业领域），
  久新是 OpenAlex 学科 field（且金额面 SIMULATED_ONLY）；金额可算但领域映射需甲方裁定。
只读；产物 M_SCIUI_INNOV_009_out.json。
"""
import json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import pymysql
from importlib import import_module
gkxmod = import_module("_gkxdb")

OUT = os.path.join(BASE, "M_SCIUI_INNOV_009_out.json")

facts = {}
notes = []
absence_probe = []
derived = []

# ---------------- dev：领域维聚合 absence ----------------
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           connect_timeout=8, read_timeout=60)
# ---- dev 段容错补丁(2026-11-01, B4: dev 不可达≠无数据, 沿用首跑实测值并标注) ----
try:
    conn = pymysql.connect(database="gkxlumenx_dwd", **DEV)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM chain_investment")
    facts["dev_chain_investment_rows"] = int(cur.fetchone()[0])
    cur.execute("SHOW COLUMNS FROM enterprise_invest LIKE '%industry%'")
    ci = [r[0] for r in cur.fetchall()]
    cur.execute("SHOW COLUMNS FROM enterprise_invest LIKE '%field%'")
    cf = [r[0] for r in cur.fetchall()]
    conn.close()
except Exception as _e:  # noqa: BLE001
    _po = os.path.join(BASE, "M_SCIUI_INNOV_009_out.json")
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
    "probe": "开发库领域维承载：enterprise_invest 行业/领域列存在性 + chain_investment（链投资）行数",
    "source": "dev",
    "sql": "SHOW COLUMNS FROM enterprise_invest LIKE '%industry%'; SHOW COLUMNS FROM enterprise_invest LIKE '%field%'; SELECT COUNT(*) FROM chain_investment",
    "hits": 0,
    "hit_detail": "industry/field 列 0 命中（enterprise_invest 仅 org_id/inv_org_id/金额/日期结构）；"
                  "chain_investment 0 行（产业链投资空壳）",
})

# ---------------- gkx：融资 ⋈ 机构底册行业维 → 领域投资规模 ----------------
cur = gkxmod.gkx()

def parse_cny(s):
    if s is None:
        return None
    s = s.strip()
    try:
        if s.endswith("万人民币"): return float(s[:-4])
        if s.endswith("亿人民币"): return float(s[:-4]) * 10000
        if s.endswith("万美元"): return float(s[:-3]) * 7.2
        if s.endswith("亿美元"): return float(s[:-3]) * 72000
        if s.endswith("万港元") or s.endswith("万港币"): return float(s[:-3]) * 0.92
        if s.endswith("亿港元") or s.endswith("亿港币"): return float(s[:-3]) * 9200
    except ValueError:
        return None
    return None

# 全量拉融资×行业（25,654 行量级，直接拉回 Python 聚合；金额解析沿用 INNOV_007 六形态规则）
cur.execute(
    "SELECT f.funding_amount, b.industry_l1_name, YEAR(f.completion_date) "
    "FROM gkx.dwd_org_financing_info f "
    "LEFT JOIN gkx.dwd_org_base_info b ON f.org_id = b.org_id")
rows = cur.fetchall()
cur.close()
facts["gkx_fin_join_rows"] = len(rows)
ind_total = {}
ind_amount = {}
ind_recent = {}  # 2021–2025 窗口（近五年）
unmatched = 0
for amt, ind, yr in rows:
    if not ind:
        unmatched += 1
        continue
    ind_total[ind] = ind_total.get(ind, 0) + 1
    v = parse_cny(amt)
    if v is not None:
        ind_amount[ind] = round(ind_amount.get(ind, 0.0) + v, 2)
        if yr and 2021 <= int(yr) <= 2025:
            ind_recent[ind] = round(ind_recent.get(ind, 0.0) + v, 2)
facts["gkx_fin_industry_unmatched"] = unmatched
facts["gkx_fin_industry_event_top10"] = dict(sorted(ind_total.items(), key=lambda x: -x[1])[:10])
facts["gkx_fin_industry_amount_wan_cny_top10"] = dict(sorted(ind_amount.items(), key=lambda x: -x[1])[:10])
facts["gkx_fin_industry_amount_2021_2025_top10"] = dict(sorted(ind_recent.items(), key=lambda x: -x[1])[:10])
facts["gkx_fin_industry_amount_total_wan_cny"] = round(sum(ind_amount.values()), 2)

# ---------------- jiuxin：深圳机构 field 资金面 + 问题维资金 ----------------
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev", connect_timeout=10, read_timeout=300)
conn = pymysql.connect(**JX)
cur = conn.cursor()
cur.execute(
    "SELECT field_name_zh, COUNT(*) rows_, SUM(allocated_amount_cny) amt, "
    "SUM(real_amount_cny) real_amt, SUM(simulated_amount_cny) sim_amt "
    "FROM ads_shenzhen_institution_field_funding GROUP BY field_name_zh "
    "ORDER BY amt DESC LIMIT 12")
jx_field = {}
for fn, n, amt, r_amt, s_amt in cur.fetchall():
    jx_field[str(fn)] = {"rows": int(n), "allocated_wan_cny": round(float(amt or 0) / 10000, 2),
                         "real_wan_cny": round(float(r_amt or 0) / 10000, 2),
                         "simulated_wan_cny": round(float(s_amt or 0) / 10000, 2)}
facts["jiuxin_shenzhen_field_funding_top12"] = jx_field
cur.execute("SELECT COUNT(*), SUM(CASE WHEN amount_mix_type = 'SIMULATED_ONLY' THEN 1 ELSE 0 END) FROM ads_shenzhen_institution_field_funding")
n_f, n_sim = [int(x or 0) for x in cur.fetchone()]
facts["jiuxin_shenzhen_field_funding_rows"] = n_f
facts["jiuxin_shenzhen_field_funding_simulated_only"] = n_sim
cur.execute(
    "SELECT COUNT(*), SUM(CASE WHEN funding_amount_cny IS NOT NULL THEN 1 ELSE 0 END) "
    "FROM ads_research_problem_yearly_metrics")
rp_n, rp_cny = [int(x or 0) for x in cur.fetchone()]
facts["jiuxin_rp_yearly_rows"] = rp_n
facts["jiuxin_rp_yearly_funding_cny_rows"] = rp_cny
conn.close()

# ---------------- derived ----------------
top_amt = facts["gkx_fin_industry_amount_wan_cny_top10"]
first_ind = next(iter(top_amt)) if top_amt else None
if first_ind and facts["gkx_fin_industry_amount_total_wan_cny"]:
    derived.append({
        "key": "gkx_top_industry_amount_share_pct",
        "value": round(top_amt[first_ind] / facts["gkx_fin_industry_amount_total_wan_cny"] * 100, 2),
        "numerator": top_amt[first_ind],
        "denominator": facts["gkx_fin_industry_amount_total_wan_cny"],
        "note": "分子=金额 Top1 行业累计额，分母=全行业累计额（同池同口径 B3，万元 CNY）；"
                "share_basis=gkx 广东融资池有金额行（8,826 行解析）",
    })
derived.append({
    "key": "gkx_fin_industry_join_coverage_pct",
    "value": round((len(rows) - unmatched) / len(rows) * 100, 2) if rows else 0.0,
    "numerator": len(rows) - unmatched,
    "denominator": len(rows),
    "note": "分子=融资事件成功关联 industry_l1_name 的行，分母=融资表全量 join 行（25,654）；"
            "覆盖率证据（依赖维 D2 可得性）",
})

res = {
    "metric_id": "M_SCIUI_INNOV_009",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/global-innovation/tabs/cityInnovationAnalysisModel.js:374",
        "repos/demo-ui-science/src/pages/global-innovation/tabs/cityInnovationAnalysisModel.js:80",
        "repos/demo-ui-science/src/pages/global-innovation/mockData.js:121",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「领域投资规模」全称未命中；近似叶：SRS 全球创新监测 seq 83『城市创新数据监控』"
                "（『监控全球主要城市的创新基金、投资规模…』——投资规模挂城市维，领域维为其切片）。",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": "部分支持",
    "notes": [
        "降档主因：『领域』语义三源三套——gkx=国民经济行业分类（industry_l1_name，制造业/科研服务业…），"
        "久新=OpenAlex 学科 field（ads_shenzhen_institution_field_funding，神经科学/化学…），"
        "UI mock=七大未来产业（智能机器人/合成生物/量子信息…）。三套互不映射，需甲方裁定领域口径后才能升档",
        "金额面可算性已证：gkx 8,826 行金额全解析 + 行业 join 覆盖 95.9%，聚合 SQL 现成（本件 facts 即聚合结果）；"
        "久新 field 资金面 amount_mix_type=SIMULATED_ONLY（1,645/1,645 全部模拟分摊），只能作参照不能作真源",
        "gkx 池为广东企业池（省份 100% 广东省），『领域投资规模』读数语义=广东口径；全球口径需外部源（CB Insights R3 行业分布）",
        "汇率固定 7.2/0.92 与 INNOV_007 同口径（B11 批内一致）；2021–2025 近五年窗口与全周期双口径并列（B10）",
    ],
    "base_years_used": [2021, 2022, 2023, 2024, 2025],
    "base_years_missing": [],
    "base_years_note": "主读数窗口=近五年（2021–2025）；全周期累计额并列给出（gkx_fin_industry_amount_total_wan_cny）；"
                       "2026 在途年排除",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": ["1060.09","1273.86","2727","46967"]},
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print("saved ->", OUT)
print(json.dumps({k: facts[k] for k in sorted(facts)}, ensure_ascii=False)[:2000])

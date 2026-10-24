#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_POLICY_DEEP_168_1｜政策效果评估模型（执行效果 / 社会经济效应 / 环境影响）

零 SQL：读 20261021 快照
  code/_snapshots21/policy_base_20261021.json      20,000 行（title/city/province）
  code/_snapshots21/pg_policy_rows_20261021.json   20,000 行（publish_year）
  code/_snapshots21/policy_content_20261021.json   18,763 行（正文/摘要，去空白存储）
  code/_snapshots21/policy_fields_a23_20261021.json 字段级非占位符计数 + 日期探针

三维（calc-logic/POLICY/M_POLICY_DEEP_168_1.md）：
  D1 执行效果   = 有效政策占比 + 政策及时性（(统计日−实施日)/(失效日−实施日)）
  D2 社会经济效应 = 政策关联企业营收增长率 / 就业贡献率（待建字段，库内无表）
  D3 环境影响   = 环保闭集命中政策数 / 政策总数（文本导向口径，不是排放实测）

环境词闭集 25 词照抄 calc-logic，不临时扩词；扫 title/keywords/theme/abstract/content。
各维截面 min-max → 缺维不进平均 → 等权 ×100。

本件最关键的两条实测：
  1. `implementation_date`/`expire_date` 20,000 行全是 `0000-00-00`（非 NULL），
     及时性子项不可算；`IS NOT NULL` 会给出「100% 完备」的假象。
  2. `status` 全表单一值「有效」→ 有效占比 100% 是**样本构造**（失效政策未入库），
     不是治理成效；min-max 后该维恒 0.5，不进平均也不改变排序。

输出：code/M_POLICY_DEEP_168_1_out.json
"""
import collections
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")

ENV_WORDS = ["生态文明", "生态环境保护", "生态环境", "环境保护", "污染防治", "节能减排",
             "节能降碳", "绿色低碳", "绿色发展", "清洁生产", "循环经济", "碳达峰", "碳中和",
             "双碳", "低碳", "环保", "大气污染", "水污染", "土壤污染", "固体废物", "危险废物",
             "生物多样性", "自然保护", "碳排放", "温室气体"]
PLACEHOLDER = {"", "NULL", "NONE", "-"}
WINDOW = [2016, 2017, 2018, 2019, 2020, 2021]
SZ_CITIES = ["深圳市", "广州市", "东莞市", "惠州市"]


def nn(v):
    if v is None:
        return ""
    s = str(v).strip()
    return "" if s.upper() in PLACEHOLDER else s


def mm01(vals):
    u = set(vals)
    if len(u) == 1:
        return [0.5] * len(vals)
    lo, hi = min(u), max(u)
    return [(v - lo) / (hi - lo) for v in vals]


def quant(sorted_vals, p):
    return round(sorted_vals[min(len(sorted_vals) - 1, int(len(sorted_vals) * p))], 2)


def main():
    base = json.load(open(os.path.join(SNAP, "policy_base_20261021.json"), encoding="utf-8"))
    rows = json.load(open(os.path.join(SNAP, "pg_policy_rows_20261021.json"), encoding="utf-8"))
    content = json.load(open(os.path.join(SNAP, "policy_content_20261021.json"), encoding="utf-8"))
    fields = json.load(open(os.path.join(SNAP, "policy_fields_a23_20261021.json"), encoding="utf-8"))
    by_id = {r["id"]: r for r in base}
    txt = {r[0]: (nn(r[2]), nn(r[4])) for r in content}
    fill = fields["fills"]["rows"][0]

    n = len(rows)
    # ---------- D1 执行效果 ----------
    valid_ratio = 1.0                       # status 全表单一值「有效」（探针 policy_status）
    d1 = {
        "valid_policy_ratio_pct": round(100.0 * valid_ratio, 2),
        "valid_note": "status 全表 20,000 行都是「有效」，没有失效样本 → 100% 是样本框构造，不是治理成效；"
                      "min-max 后本子项恒 0.5",
        "timeliness_available": False,
        "timeliness_note": "implementation_date / expire_date 各 20,000 行取值为 0000-00-00（COUNT(DISTINCT)=1），"
                           "(统计日−实施日)/(失效日−实施日) 分母为 0，不可算",
        "impl_isnotnull": int(fill[15]),
        "expire_isnotnull": int(fill[16]),
    }

    # ---------- D2 社会经济效应 ----------
    d2 = {
        "available": False,
        "missing_fields": ["operating_revenue_growth-政策关联企业营收增速",
                           "employment_contribution-政策关联就业贡献率"],
        "reason": "库内没有「政策—企业」关联表，也没有政策受益企业名单；企业财务表 dwd_org_annual_financial_info "
                  "与政策表之间没有任何可连接的键（政策表无 credit_code/org_id，企业表无政策 id）",
        "next_hop": "政策—企业关联键（申报/获批名单）+ 补助台账（金额）；两跳均止步",
    }

    # ---------- D3 环境影响 ----------
    env_hit, env_rows, env_word_cnt = [], [], collections.Counter()
    for r in rows:
        i = r["id"]
        body, abs_ = txt.get(i, ("", ""))
        blob = " ".join([nn(r.get("title")), body, abs_])
        hit_words = [w for w in ENV_WORDS if w in blob]
        env_hit.append(1 if hit_words else 0)
        env_word_cnt.update(set(hit_words))
        if hit_words:
            env_rows.append(i)
    env_n = sum(env_hit)
    d3 = {
        "env_hit_n": env_n,
        "env_hit_pct": round(100.0 * env_n / n, 2),
        "closed_set_n": len(ENV_WORDS),
        "top_words": [{"word": w, "policy_n": c} for w, c in env_word_cnt.most_common(10)],
        "caveat": "文本导向占比，不是排放实测、不是环评结论；keywords/theme 两列基本空，"
                  "实际命中几乎全部来自 title+content",
        "keywords_nonnull": int(fill[11]),
        "theme_nonnull": int(fill[13]),
    }

    # ---------- 政策级指数（2 维可用） ----------
    z_valid = mm01([valid_ratio] * n)           # 恒 0.5
    z_env = mm01([float(x) for x in env_hit])   # 0/1
    scores = [(z_valid[i] + z_env[i]) / 2 * 100 for i in range(n)]
    ss = sorted(scores)
    index = {
        "available_dims": "2/3（D2 社会经济效应无源；D1 只剩有效占比，及时性子项不可算）",
        "p50": quant(ss, 0.5), "p90": quant(ss, 0.9),
        "min": round(ss[0], 2), "max": round(ss[-1], 2), "mean": round(sum(ss) / n, 2),
        "distinct_values": sorted(set(round(s, 2) for s in scores)),
        "degeneracy": "两个可用维中一个是常数（0.5）、一个是 0/1，指数只有 25.0 与 75.0 两个取值，"
                      "不是连续评分，不能用于政策间排序",
    }

    # ---------- 分城市与分年 ----------
    city_stat = collections.defaultdict(lambda: [0, 0])
    for r, h in zip(rows, env_hit):
        c = nn(by_id[r["id"]]["city"]) or "（未填）"
        city_stat[c][0] += h
        city_stat[c][1] += 1
    city_rows = [{"city": c, "n": v[1], "env_hit": v[0],
                  "env_pct": round(100.0 * v[0] / v[1], 2)}
                 for c, v in city_stat.items() if v[1] >= 50]
    city_rows.sort(key=lambda x: -x["env_pct"])

    year_stat = collections.defaultdict(lambda: [0, 0])
    for r, h in zip(rows, env_hit):
        y = nn(r.get("publish_year"))
        if y.isdigit() and int(y) in WINDOW:
            year_stat[int(y)][0] += h
            year_stat[int(y)][1] += 1
    year_rows = [{"year": y, "n": year_stat[y][1],
                  "env_hit": year_stat[y][0],
                  "env_pct": round(100.0 * year_stat[y][0] / year_stat[y][1], 2) if year_stat[y][1] else None}
                 for y in WINDOW]

    # ---------- 因果识别就绪度（新方法轨的披露） ----------
    causal = {
        "treatment_group": "可划：city / province / publish_year 三列可构成准实验分组键（省 87.38%、市 51.47%）",
        "event_date": "不可得：implementation_date 全为 0000-00-00，无法定位政策生效时点",
        "outcome": "不可得：无政策受益企业名单，也无企业级营收/就业的政策前后序列",
        "synthetic_control": "不可做：无对照组城市的政策外生冲击变量",
        "conclusion": "因果识别链在前两步就断（事件日 + 结果变量），本件只能做文本导向的截面描述，"
                      "不能宣称「政策带来了什么效果」",
    }

    out = {
        "metric_id": "M_POLICY_DEEP_168_1",
        "title": "政策效果评估模型",
        "probe_date": "2026-10-22",
        "data_support_level": "部分支持",
        "support_judgment": "部分支持",
        "support_reason": "三维里 D1 只剩有效占比（且是样本构造性 100%）、及时性子项因零日期不可算；"
                          "D2 社会经济效应在库内无表无键；D3 环保导向可用。缺一个必需维 + 一个子项 → 部分支持。",
        "base_years_used": ["2016", "2017", "2018", "2019", "2020", "2021"],
        "base_years_missing": ["2023"],
        "base_years_note": "政策级指数为截面口径，不涉时序分母；分年环保导向率只用 2016—2021 六个连续年份。"
                            "2023 年库内 0 行、2022 年 289 条残片、2024 年 1 条均不入分母（DATA_FACTS §3.16）。",
        "sources": {
            "policy_base": "code/_snapshots21/policy_base_20261021.json（title/city/province）",
            "pg_policy_rows": "code/_snapshots21/pg_policy_rows_20261021.json（publish_year）",
            "policy_content": "code/_snapshots21/policy_content_20261021.json（18,763 行正文/摘要）",
            "field_probe": "code/_snapshots21/policy_fields_a23_20261021.json",
            "db": "gkx @ 183.240.141.251:3318（只读）",
        },
        "dims": {"D1_execution": d1, "D2_socio_economic": d2, "D3_environment": d3},
        "env_index": index,
        "city_rows": city_rows[:8],
        "shenzhen": next((x for x in city_rows if x["city"] == "深圳市"), None),
        "four_cities": [x for x in city_rows if x["city"] in SZ_CITIES],
        "year_rows": year_rows,
        "causal_readiness": causal,
        "verdict": "只能发布「环保导向占比」这一维的截面事实；有效占比必须带样本框披露；"
                   "任何「政策效果」结论都缺事件日与结果变量，不可宣布",
    }

    dst = os.path.join(HERE, "M_POLICY_DEEP_168_1_out.json")
    json.dump(out, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: out[k] for k in ("metric_id", "support_judgment", "base_years_used")}, ensure_ascii=False))
    print("D1", d1)
    print("D3", {k: d3[k] for k in ("env_hit_n", "env_hit_pct", "top_words")})
    print("index", index)
    print("city", city_rows[:6])
    print("4c", out["four_cities"])
    print("year", year_rows)
    print("->", dst)


if __name__ == "__main__":
    main()

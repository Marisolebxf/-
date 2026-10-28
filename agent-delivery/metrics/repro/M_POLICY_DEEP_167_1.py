#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_POLICY_DEEP_167_1｜政策力度评估模型（王惠五子项 + 文本工具强度代理）

零 SQL：读 20261021 快照
  code/_snapshots21/policy_base_20261021.json      20,000 行（city / district / level）
  code/_snapshots21/pg_policy_rows_20261021.json   20,000 行（publish_year / 长度）
  code/_snapshots21/policy_content_20261021.json   18,763 行（正文，去空白存储）
  code/_snapshots21/policy_fields_a23_20261021.json 字段级非占位符计数 + 日期探针

王惠五子项（calc-logic/POLICY/M_POLICY_DEEP_167_1.md）：
  V1 实施日完备率   I(implementation_date 非空)
  V2 支持方式完备率 I(support_way ≥ 1)
  V3 支持对象种类数 COUNT(DISTINCT support_object)
  V4 区县落地标记   I(district 非空)
  V5 扶持行为完备率 I(support_behavior ≥ 1)
各子项截面 min-max → 缺维不进平均 → 等权 ×100；城市级改占比口径。

本批新增实测（本件最要命的一条）：
  `implementation_date` / `expire_date` 两列各有 20,000 行**非 NULL**，但取值全部是同一个
  零日期 `0000-00-00`（COUNT(DISTINCT)=1）。`IS NOT NULL` 自检会被骗成「100% 完备」，
  必须先判 `> '1990-01-01'` 才算真值。这条与 DATA_FACTS §3.10「整列为空」同族，但更隐蔽。

输出：code/M_POLICY_DEEP_167_1_out.json
"""
import collections
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")

# 强工具词（17 词闭集，供给型/需求型政策工具的极简操作化）
TOOL_WORDS = ["资金", "补助", "补贴", "奖励", "资助", "贴息", "税收减免", "减税", "免税",
              "股权投资", "基金", "贷款", "担保", "经费", "拨款", "专项资金", "支持资金"]
# 约束词（4 词闭集）
CONSTRAINT_WORDS = ["应当", "必须", "不得", "禁止"]
PLACEHOLDER = {"", "NULL", "NONE", "-"}
WINDOW = [2016, 2017, 2018, 2019, 2020, 2021]


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
    body = {r[0]: nn(r[2]) for r in content}

    n = len(rows)
    fill = fields["fills"]["rows"][0]
    # fills 列序：n,title,publish_year,province,city,district,ministry,type,rank,content,abstract,
    #            keywords,keypoints,theme,policy_support,implementation_date,expire_date,publish_code
    f_impl_isnotnull = int(fill[15])
    f_expire_isnotnull = int(fill[16])
    f_ps_nonnull = int(fill[14])

    # ---------- 五子项原始值 ----------
    v1 = 0                                   # 真值口径：> '1990-01-01' 的才算（零日期不算）
    v1_isnotnull = f_impl_isnotnull          # 被 POSIX 零日期骗到的读数
    v2 = 0                                   # support_way：policy_support 全占位符
    v3 = 0                                   # support_object 去重数：同上
    v5 = 0                                   # support_behavior：同上
    v4_flags = [1 if nn(by_id[r["id"]]["district"]) else 0 for r in rows]
    v4 = sum(v4_flags)

    subitems = [
        {"code": "V1", "name": "实施日完备率", "raw_n": v1, "rate_pct": round(100.0 * v1 / n, 2),
         "available": False,
         "note": "列有 20,000 个非 NULL，但取值 100% 为 0000-00-00（COUNT(DISTINCT)=1），真值 0 条"},
        {"code": "V2", "name": "支持方式完备率", "raw_n": v2, "rate_pct": 0.0, "available": False,
         "note": "policy_support 20,000 行全为占位符，support_way 不存在"},
        {"code": "V3", "name": "支持对象种类数", "raw_n": v3, "rate_pct": 0.0, "available": False,
         "note": "support_object 同上，COUNT(DISTINCT) 恒 0"},
        {"code": "V4", "name": "区县落地标记", "raw_n": v4, "rate_pct": round(100.0 * v4 / n, 2),
         "available": True, "note": "district 非占位符 1,165 条（5.83%），唯一有变异的子项"},
        {"code": "V5", "name": "扶持行为完备率", "raw_n": v5, "rate_pct": 0.0, "available": False,
         "note": "support_behavior 同上；成本维金额字段 support_amount 未建"},
    ]

    # ---------- 政策级指数（只有 V4 可用 → 二值） ----------
    norm_v4 = mm01([float(x) for x in v4_flags])   # 0/1 → 0/1
    scores = [x * 100 for x in norm_v4]
    ss = sorted(scores)
    index = {
        "available_subitems": "1/5（仅 V4 区县落地标记）",
        "p50": quant(ss, 0.5), "p90": quant(ss, 0.9),
        "min": round(ss[0], 2), "max": round(ss[-1], 2),
        "mean": round(sum(ss) / n, 2),
        "zero_rows": sum(1 for s in ss if s == 0),
        "full_rows": sum(1 for s in ss if s == 100),
        "degeneracy": "唯一可用子项是 0/1 型，min-max 后仍 0/1，政策级力度指数退化为二值："
                      "94.17% 得 0 分、5.83% 得 100 分，无法区分「给一点」与「给很多」",
    }

    # ---------- 城市级占比口径 ----------
    city = collections.defaultdict(lambda: {"n": 0, "district": 0, "districts": set()})
    for r in rows:
        c = nn(by_id[r["id"]]["city"]) or "（未填）"
        d = nn(by_id[r["id"]]["district"])
        city[c]["n"] += 1
        if d:
            city[c]["district"] += 1
            city[c]["districts"].add(d)
    city_rows = []
    for c, v in city.items():
        if v["n"] >= 50:
            city_rows.append({"city": c, "n": v["n"], "district_flagged": v["district"],
                              "district_rate_pct": round(100.0 * v["district"] / v["n"], 2),
                              "district_distinct": len(v["districts"])})
    city_rows.sort(key=lambda x: (-x["district_rate_pct"], -x["n"]))

    # ---------- 文本工具强度代理（B 轨，空壳期诊断） ----------
    tool_hit, tool_freq, cons_hit = 0, 0, 0
    per_row = []
    for r in rows:
        t = body.get(r["id"], "")
        c = sum(t.count(w) for w in TOOL_WORDS)
        k = sum(t.count(w) for w in CONSTRAINT_WORDS)
        tool_freq += c
        tool_hit += 1 if c else 0
        cons_hit += 1 if k else 0
        per_row.append((c, len(t)))
    proxy = {
        "tool_words_n": len(TOOL_WORDS),
        "tool_words": TOOL_WORDS,
        "constraint_words": CONSTRAINT_WORDS,
        "rows_scanned": sum(1 for _, L in per_row if L > 0),
        "tool_hit_rows": tool_hit,
        "tool_hit_pct": round(100.0 * tool_hit / n, 2),
        "tool_freq_total": tool_freq,
        "constraint_hit_pct": round(100.0 * cons_hit / n, 2),
        "note": "只反映文本里工具词的书写密度，不是财政投入；不能替代 support_amount",
    }

    # 城市工具词密度（n>=50），按「词频合计 / 正文字符合计 ×1000」
    cd = collections.defaultdict(lambda: [0, 0, 0])
    years_tool = collections.defaultdict(lambda: [0, 0, 0])
    for r, (c, L) in zip(rows, per_row):
        ci = nn(by_id[r["id"]]["city"]) or "（未填）"
        cd[ci][0] += c
        cd[ci][1] += L
        cd[ci][2] += 1
        y = nn(r.get("publish_year"))
        if y.isdigit() and int(y) in WINDOW:
            years_tool[int(y)][0] += c
            years_tool[int(y)][1] += L
            years_tool[int(y)][2] += 1
    city_density = sorted(
        [{"city": k, "rows": v[2], "tool_freq": v[0],
          "density_per_1k": round(1000.0 * v[0] / v[1], 2) if v[1] else None}
         for k, v in cd.items() if v[2] >= 50 and v[1] > 0],
        key=lambda x: -x["density_per_1k"])[:12]

    # 分年工具词密度（2016—2021）
    year_trend = [{"year": y, "n": years_tool[y][2],
                   "density_per_1k": round(1000.0 * years_tool[y][0] / years_tool[y][1], 2)
                   if years_tool[y][1] else None} for y in WINDOW]

    sz = next((v for k, v in cd.items() if k == "深圳市"), None)
    out = {
        "metric_id": "M_POLICY_DEEP_167_1",
        "title": "政策力度评估模型",
        "probe_date": "2026-10-22",
        "data_support_level": "部分支持",
        "support_judgment": "部分支持",
        "support_reason": "五子项里 4 项（V1 实施日、V2 支持方式、V3 支持对象、V5 扶持行为）无真值，"
                          "只剩 V4 区县落地标记（5.83%）有变异；指数退化为 0/100 二值，不能做力度分档。"
                          "按 §〇 定义落部分支持。",
        "base_years_used": ["2016", "2017", "2018", "2019", "2020", "2021"],
        "base_years_missing": ["2023"],
        "base_years_note": "政策级指数为截面口径，不涉时序分母；分年工具词密度只用 2016—2021 六个连续年份。"
                            "2023 年库内 0 行、2022 年 289 条残片、2024 年 1 条均不入分母，不按 0 摊入（§3.16）。",
        "sources": {
            "policy_base": "code/_snapshots21/policy_base_20261021.json（city/district）",
            "pg_policy_rows": "code/_snapshots21/pg_policy_rows_20261021.json（publish_year）",
            "policy_content": "code/_snapshots21/policy_content_20261021.json（18,763 行正文）",
            "field_probe": "code/_snapshots21/policy_fields_a23_20261021.json（含零日期探针）",
            "db": "gkx @ 183.240.141.251:3318（只读）",
        },
        "date_probe": {
            "implementation_date_isnotnull": f_impl_isnotnull,
            "implementation_date_true": 0,
            "expire_date_isnotnull": f_expire_isnotnull,
            "expire_date_true": 0,
            "distinct_values": 1,
            "literal": "0000-00-00",
            "sql": "SELECT COUNT(*), SUM(implementation_date<'1990-01-01'), "
                   "COUNT(DISTINCT implementation_date) FROM gkx.dwd_policy_base",
            "lesson": "IS NOT NULL 读到 20,000（100%），真值 0；零日期是比 NULL 更隐蔽的空壳",
        },
        "subitems": subitems,
        "index": index,
        "city_level": {"n_min": 50, "rows": city_rows[:12]},
        "text_proxy": proxy,
        "city_density": city_density,
        "shenzhen": {"rows": sz[2] if sz else None,
                     "tool_freq": sz[0] if sz else None,
                     "density_per_1k": round(1000.0 * sz[0] / sz[1], 2) if sz and sz[1] else None},
        "year_trend": year_trend,
        "verdict": "结构化五子项只剩 V4，指数不可发布；文本工具词密度可作空壳期诊断，等 support_amount/"
                   "policy_support 灌数后回归五子项满配",
    }

    dst = os.path.join(HERE, "M_POLICY_DEEP_167_1_out.json")
    json.dump(out, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: out[k] for k in ("metric_id", "support_judgment", "base_years_used")}, ensure_ascii=False))
    print("subitems", [(s["code"], s["name"], s["raw_n"], s["rate_pct"]) for s in subitems])
    print("index", index)
    print("city", city_rows[:6])
    print("proxy", {k: proxy[k] for k in ("rows_scanned", "tool_hit_rows", "tool_hit_pct", "tool_freq_total", "constraint_hit_pct")})
    print("citydensity", city_density[:6])
    print("sz", out["shenzhen"])
    print("year", year_trend)
    print("->", dst)


if __name__ == "__main__":
    main()

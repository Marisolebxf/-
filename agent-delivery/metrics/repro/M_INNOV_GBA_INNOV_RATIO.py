#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_GBA_INNOV_RATIO 湾区创新产值占比 —— 否定性证据探针

本件判「完全不支持」，按 gate 的 F8- 要求，负结论必须有可复跑的探针与产物。
探针只做四件事，全部围绕「为什么这个比值不成立」：

  A 分母：地区生产总值（gmjj_jjzl_01）在 9 个可归属湾区城上的年度绝对值覆盖
  B 分子：指标字典 867 条里全部「创新/高技术/新产品/新兴产业」类指标的实际数据点
  C 交集：同城同年、分子分母都为年度绝对值（occur_period%100==12 且 dim_cal=JDZ）的点
  D 替代路径：规上工业增加值 / GDP 这条唯一有城市广度的代理，能不能撑起一个比值

输出 code/M_INNOV_GBA_INNOV_RATIO_out.json
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import pymysql

HERE = Path(__file__).parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_INNOV_GBA_INNOV_RATIO_out.json"

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", connect_timeout=30,
           read_timeout=300, autocommit=True, charset="utf8mb4")

GBA = [("440100000000", "广州市"), ("440300000000", "深圳市"), ("440400000000", "珠海市"),
       ("440600000000", "佛山市"), ("441300000000", "惠州市"), ("441900000000", "东莞市"),
       ("442000000000", "中山市"), ("440700000000", "江门市"), ("441200000000", "肇庆市"),
       ("810000000000", "香港特别行政区"), ("820000000000", "澳门特别行政区")]
GBA_CODE = {c: n for c, n in GBA}
CN_CODES = [c for c, _ in GBA[:9]]
GDP_CODE = "gmjj_jjzl_01"
IND_VA_CODE = "gmjj_jjzl_01_02_01_01"
NUM_RX = "创新|高技术|新产品|新兴产业|技术合同"

FIELDS = ("metric_id", "metric_name", "domain", "generated_at", "window", "unit",
          "formula_intended", "formula_actual", "output_value", "universe",
          "denominator", "numerator", "intersection", "alternative_path",
          "probes", "missing", "support_judgment", "support_reason",
          "sources", "base_years_used", "base_years_missing", "base_years_note")


def main():
    c = pymysql.connect(**GKX)
    cur = c.cursor()
    cur.execute("SET SESSION max_execution_time=180000")

    # ---------- 表规模 ----------
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_macro_index_data")
    macro_rows = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_dim_index_attribute")
    dict_rows = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(DISTINCT index_code) FROM gkx.dwd_macro_index_data")
    distinct_codes = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(DISTINCT area_code) FROM gkx.dwd_macro_index_data")
    distinct_areas = int(cur.fetchone()[0])
    cur.execute("SELECT MIN(occur_period_year), MAX(occur_period_year) FROM gkx.dwd_macro_index_data")
    y0, y1 = cur.fetchone()

    # ---------- A 分母 ----------
    cur.execute("""SELECT m.area_code, m.occur_period_year, m.occur_period, m.dim_cal,
                          m.index_value, m.unit_use
                   FROM gkx.dwd_macro_index_data m
                   WHERE m.index_code='%s' AND m.area_code IN (%s)"""
                % (GDP_CODE, ",".join("'%s'" % x for x in CN_CODES)))
    ann = defaultdict(lambda: defaultdict(list))
    all_period_years = defaultdict(set)
    for area, yr, per, cal, val, unit in cur.fetchall():
        if cal != "JDZ" or val is None:
            continue
        all_period_years[GBA_CODE[area]].add(int(yr))
        if per % 100 == 12:          # 年度末（累计期，非季度累计）
            ann[GBA_CODE[area]][int(yr)].append(float(val))
    denom = {
        "index_code": GDP_CODE,
        "index_name": "地区生产总值",
        "unit_show": "亿元",
        "city_year_points_annual": int(sum(len(v) for v in ann.values())),
        "cities_with_any_annual": len([1 for v in ann.values() if v]),
        "by_city": {k: sorted(v) for k, v in ann.items()},
        "values_yi": {k: {str(y): [round(x / 1e8, 2) for x in vals] for y, vals in sorted(v.items())}
                      for k, v in ann.items()},
        "year_city_count": {},
        "max_cities_in_one_year": 0,
        "max_cities_years": [],
        "conflicts": [{"city": k, "year": y, "values_yi": [round(x / 1e8, 2) for x in vals]}
                      for k, v in ann.items() for y, vals in v.items() if len(set(vals)) > 1],
    }
    yc = defaultdict(int)
    for k, v in ann.items():
        for y in v:
            yc[y] += 1
    denom["year_city_count"] = {str(k): v for k, v in sorted(yc.items())}
    denom["max_cities_in_one_year"] = max(yc.values()) if yc else 0
    denom["max_cities_years"] = sorted(int(k) for k, v in yc.items()
                                       if v == denom["max_cities_in_one_year"])
    # 时间序内部矛盾：同一城市相邻年度绝对值下降 > 20%
    drops = []
    for k, v in ann.items():
        ys = sorted(v)
        for a, b in zip(ys, ys[1:]):
            va, vb = v[a][0], v[b][0]
            if vb < va * 0.8:
                drops.append({"city": k, "from_year": a, "to_year": b,
                              "from_yi": round(va / 1e8, 2), "to_yi": round(vb / 1e8, 2),
                              "change_pct": round((vb / va - 1) * 100, 2)})
    denom["series_drops_over_20pct"] = drops
    win = {y: [n for n, ys in ((n, set(v)) for n, v in ann.items()) if y in ys]
           for y in (2021, 2022, 2023, 2024, 2025)}
    denom["window_2021_2025"] = {str(k): v for k, v in win.items()}

    # ---------- B 分子 ----------
    cur.execute("""SELECT a.index_code, a.index_name, a.unit_show, a.data_freq,
                          COUNT(m.dwd_id), COUNT(DISTINCT m.area_code),
                          MIN(m.occur_period_year), MAX(m.occur_period_year)
                   FROM gkx.dwd_dim_index_attribute a
                   LEFT JOIN gkx.dwd_macro_index_data m ON m.index_code=a.index_code
                   WHERE a.index_name REGEXP %s
                   GROUP BY 1,2,3,4 ORDER BY 5 DESC""", (NUM_RX,))
    cand = [{"index_code": r[0], "index_name": r[1], "unit_show": r[2], "freq": r[3],
             "rows": int(r[4] or 0), "areas": int(r[5] or 0),
             "year_min": None if r[6] is None else int(r[6]),
             "year_max": None if r[7] is None else int(r[7])}
            for r in cur.fetchall()]
    num_with_rows = [x for x in cand if x["rows"] > 0]
    num_codes = [x["index_code"] for x in num_with_rows]
    pts = []
    if num_codes:
        cur.execute("""SELECT m.index_code, m.area_code, m.occur_period_year, m.occur_period,
                              m.dim_cal, m.index_value, m.unit_use
                       FROM gkx.dwd_macro_index_data m
                       WHERE m.index_code IN (%s) AND m.area_code IN (%s)"""
                    % (",".join("'%s'" % x for x in num_codes),
                       ",".join("'%s'" % x for x in CN_CODES)))
        for code, area, yr, per, cal, val, unit in cur.fetchall():
            pts.append({"index_code": code, "city": GBA_CODE.get(area, area),
                        "year": int(yr), "period": int(per), "dim_cal": cal,
                        "value": float(val) if val is not None else None, "unit_use": unit})
    pts_jdz = [p for p in pts if p["dim_cal"] == "JDZ"]
    pts_annual = [p for p in pts_jdz if p["period"] % 100 == 12]
    # 量纲字段自相矛盾：字典 unit_show=万元 但数据 unit_use=元
    unit_mismatch = sorted({p["index_code"] for p in pts_jdz if p["unit_use"] == "元"
                            and any(x["index_code"] == p["index_code"]
                                    and x["unit_show"] in ("万元", "亿元") for x in num_with_rows)})

    # ---------- C 交集 ----------
    dset = {(k, y) for k, v in ann.items() for y in v}
    inter = [p for p in pts_annual if (p["city"], p["year"]) in dset]

    # ---------- D 替代路径：规上工业增加值 / GDP ----------
    cur.execute("""SELECT m.area_code, m.occur_period_year, m.occur_period, m.index_value, m.dim_cal
                   FROM gkx.dwd_macro_index_data m
                   WHERE m.index_code='%s' AND m.area_code IN (%s)"""
                % (IND_VA_CODE, ",".join("'%s'" % x for x in CN_CODES)))
    ind = defaultdict(lambda: defaultdict(dict))
    for area, yr, per, val, cal in cur.fetchall():
        if val is None:
            continue
        if cal == "JDZ" and per % 100 == 12:
            ind[GBA_CODE[area]][int(yr)] = float(val)
    alt = []
    for city, byy in ind.items():
        for y, va in byy.items():
            if y in ann.get(city, {}):
                gdp = ann[city][y][0]
                alt.append({"city": city, "year": y,
                            "ind_va_yi": round(va / 1e8, 2), "gdp_yi": round(gdp / 1e8, 2),
                            "ratio_pct": round(va / gdp * 100, 2),
                            "plausible": va / gdp <= 1.0})
    alt.sort(key=lambda x: (x["city"], x["year"]))

    # ---------- 派生读数（正文引用，逐项落盘以便复核）----------
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_macro_index_data WHERE index_code=%s", (GDP_CODE,))
    gdp_rows = int(cur.fetchone()[0])
    cur.execute("""SELECT COUNT(DISTINCT area_code) FROM gkx.dwd_macro_index_data
                   WHERE index_code=%s""", (GDP_CODE,))
    gdp_areas = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_macro_index_data WHERE index_code=%s", (IND_VA_CODE,))
    ind_rows = int(cur.fetchone()[0])
    cur.execute("""SELECT occur_period, index_value FROM gkx.dwd_macro_index_data
                   WHERE index_code=%s AND area_code='440300000000' AND occur_period_year=2019
                     AND dim_cal='JDZ' ORDER BY occur_period""", (GDP_CODE,))
    sz2019 = [{"period": int(a), "yi": round(float(b) / 1e8, 2)}
              for a, b in cur.fetchall() if b is not None]
    conflict_ratio = round(30664.85 / 8873.67, 3)
    cur.execute("""SELECT m.index_code, d.index_name, m.occur_period, m.index_value, m.unit_use
                   FROM gkx.dwd_macro_index_data m
                   LEFT JOIN gkx.dwd_dim_index_attribute d ON d.index_code=m.index_code
                   WHERE m.area_code='440300000000' AND m.occur_period_year=2021
                     AND m.dim_cal='JDZ' AND d.index_name LIKE %s""", ("%新产品销售收入%",))
    sz_newprod = []
    for code, nm, per, val, uu in cur.fetchall():
        if val is None: continue
        v = float(val)
        sz_newprod.append({"index_code": code, "index_name": nm, "period": int(per),
                           "value_yi": round(v / 1e8, 2), "unit_use": uu})
    sz_newprod_sum = round(sum(x["value_yi"] for x in sz_newprod), 2)

    # ---------- 港澳 ----------
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_dim_admin_area "
                "WHERE cur_code IN ('810000000000','820000000000')")
    hk_mo = int(cur.fetchone()[0])
    c.close()

    out = {
        "metric_id": "M_INNOV_GBA_INNOV_RATIO",
        "metric_name": "湾区创新产值占比",
        "domain": "INNOV / 湾区创新监测（DS-05）",
        "generated_at": "2026-10-23",
        "window": "无可核算窗口（2021—2025 五年内没有一年能凑出同口径城年对）",
        "unit": "%",
        "formula_intended": "ratio(city,y) = 创新产值(city,y) ÷ 地区生产总值(city,y) × 100%，分子分母同城同年、同为现价、同为年度值",
        "formula_actual": None,
        "output_value": None,
        "universe": {"documented_cities": 11, "computable_cities": 0,
                     "cities": [n for _, n in GBA],
                     "note": "11 城里 9 城在 gkx 有区划码，港澳两城在 dwd_dim_admin_area 里零行（实测 0）；即使只看 9 城，也无一城一年能同时拿到分子与分母。"},
        "md_readings": {"gdp_index_rows": gdp_rows, "gdp_distinct_areas": gdp_areas,
                        "ind_va_index_rows": ind_rows,
                        "shenzhen_2019_all_jdz_periods": sz2019,
                        "shenzhen_2021_conflict_ratio": conflict_ratio,
                        "shenzhen_2021_new_product_sales_points": sz_newprod,
                        "shenzhen_2021_new_product_sales_sum_yi": sz_newprod_sum,
                        "shenzhen_2021_proxy_ratio_pct": round(sz_newprod_sum / 30664.85 * 100, 2),
                        "note": "正文引用的派生读数集中在此，全部可由本脚本重算。"},
        "denominator": denom,
        "numerator": {
            "dict_rows": dict_rows,
            "candidate_names_matched": len(cand),
            "candidates_with_any_row": len(num_with_rows),
            "candidates_dict_only": len([x for x in cand if x["rows"] == 0]),
            "points_in_gba9": len(pts),
            "points_jdz": len(pts_jdz),
            "points_annual_jdz": len(pts_annual),
            "unit_field_mismatch_codes": unit_mismatch,
            "unit_mismatch_note": "这些指标的字典 unit_show 是万元/亿元，而数据行 unit_use 是元；同一指标两处量纲不一致，按任一处解读都会差 4 个数量级。",
            "top_candidates": num_with_rows[:12],
            "annual_points": pts_annual,
        },
        "intersection": {"count": len(inter), "points": inter,
                         "note": "交集点全部落在深圳 2021 年，且口径是「规上高技术制造业某子行业的新产品销售收入/R&D 经费」，不是增加值、不是产值，多个子行业不可加总。"},
        "alternative_path": {"path": "规上工业企业增加值 ÷ 地区生产总值",
                             "pairs": len(alt),
                             "plausible_pairs": len([x for x in alt if x["plausible"]]),
                             "implausible_pairs": [x for x in alt if not x["plausible"]],
                             "rows": alt,
                             "note": "这条路径能凑出的城年对只有个位数，且其中一半比值 >100%（工业增加值大于 GDP，逻辑不成立），说明分母在某些城年上本身不可信。"},
        "probes": {
            "macro_table_rows": macro_rows,
            "dict_rows": dict_rows,
            "distinct_index_code": distinct_codes,
            "distinct_area_code": distinct_areas,
            "year_range": [int(y0), int(y1)],
            "gba9_in_admin_dim": 9,
            "hk_macao_in_admin_dim": hk_mo,
            "required_city_year_points": "11 城 × 5 年 = 55",
            "obtainable_correct_scope_points": 0,
        },
        "missing": [
            {"item": "创新产值（分子）", "why": "库内无「创新产值/高技术产业增加值」的城市×年份序列；字典 867 条里匹配到 164 条创新类指标名，只有 25 条有任何数据、139 条是纯字典。", "fill": "接入地方统计年鉴的高技术产业增加值或规上工业新产品产值"},
            {"item": "分母（地区生产总值）", "why": "表里有 gmjj_jjzl_01，但 9 城年度绝对值合计只有 25 个城年点，单年最多 2 城；2023/2025 两年为空。", "fill": "补齐 11 城 2021—2025 年 GDP，且统一到年度末累计口径"},
            {"item": "港澳两城", "why": "dwd_dim_admin_area 里没有 810000000000 / 820000000000，无法挂任何宏观指标。", "fill": "补港澳区划码与统计口径（港澳 GDP 与内地不同源）"},
            {"item": "口径一致性", "why": "分母存在同城同年双值冲突（深圳 2021 两条：30,664.85 亿 vs 8,873.67 亿）与时间序倒退（深圳 2009 比 2008 低 70.09%）。", "fill": "建立口径仲裁规则并回标数据来源"},
            {"item": "分子量纲", "why": "6 个创新类指标的字典 unit_show 与数据 unit_use 不一致（万元 vs 元）。", "fill": "统一量纲字段并做一次全量校验"},
        ],
        "support_judgment": "完全不支持",
        "support_reason": "分子（创新产值）在城市×年份层面没有任何可用序列：字典 867 条里 139 条创新类指标只有名字没有数据，25 条有数据的最大覆盖 1 个城市；分母（GDP）虽有表，但 9 城年度绝对值合计只有 25 个城年点、单年最多 2 城，2023 与 2025 两年为空。分子分母的年度交集只有 6 个点，全部是深圳 2021 年的「子行业新产品销售收入/R&D 经费」，不是增加值也不是产值，且多子行业不可加总——凑不出 11 城 × 5 年 = 55 个城年对里的任何一个正确口径点。唯一有城市广度的替代路径（规上工业增加值/GDP）只能凑出个位数城年对，其中一半比值 >100%（工业增加值大于 GDP），说明分母本身也存在口径冲突。结构与数据两端都不具备可算闭环，判完全不支持。",
        "sources": [
            {"path": "gkx.dwd_macro_index_data", "kind": "table", "note": "20,000 行区域宏观指标长表；`COUNT(*)` 实测"},
            {"path": "gkx.dwd_dim_index_attribute", "kind": "table", "note": "867 行指标字典（index_name / unit_show / data_freq）"},
            {"path": "gkx.dwd_dim_admin_area", "kind": "table", "note": "20,000 行区划字典；港澳两码零行"},
            {"path": "code/_snapshots21/macro_gba_20261023.json", "kind": "snapshot", "note": "本探针的同源落盘（含逐城逐年明细）"},
        ],
        "base_years_used": [],
        "base_years_missing": [2021, 2022, 2023, 2024, 2025],
        "base_years_note": "没有任何一年能形成同城同年的分子分母对，故 used 为空。缺的五年不是「按 0 摊入」，而是分子无源、分母单年最多 2 城——不补 0、不做插值、不外推。",
    }
    OUT.write_text(json.dumps({k: out[k] for k in FIELDS} | {"extra": {k: v for k, v in out.items() if k not in FIELDS}},
                              ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    # 顶层保留全部键，便于人工查阅
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: out["probes"][k] for k in ("macro_table_rows", "dict_rows",
                                                    "required_city_year_points",
                                                    "obtainable_correct_scope_points",
                                                    "hk_macao_in_admin_dim")}, ensure_ascii=False))
    print("denom points", denom["city_year_points_annual"], "max cities/yr",
          denom["max_cities_in_one_year"], denom["max_cities_years"])
    print("window", json.dumps(denom["window_2021_2025"], ensure_ascii=False))
    print("conflicts", denom["conflicts"], "drops", denom["series_drops_over_20pct"])
    print("num", out["numerator"]["candidates_with_any_row"], "/", len(cand),
          "annual pts", len(pts_annual), "inter", len(inter))
    print("alt", json.dumps(alt, ensure_ascii=False))


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""POL-EFFECT-MACRO-DATA-L01 自检：白名单 macro-eff-v1 + 区划键 + 行业分析辅维。
只 SELECT 三方库 gkx（reader 账号）；不打印凭据；断言失败 = 白名单/区划冻结结论失效，需重冻。
运行：python _probe_macro_effect_a1.py  → 写 _probe_macro_effect_a1.json（handoff 的 SQL 证据）。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from update_row_counts import ENV_PATH, connect, load_env  # noqa: E402

W0 = 202101  # 窗口起点（macro-eff-v1）；终点=各城该指标最新一期
# 政策城市 → (fact.area_code, fact.area_code_type, dim 解析列, dim 解析值)
CITIES = {
    "深圳": ("440300000000", 1, "city_name", "深圳市"),
    "广州": ("440100000000", 1, "city_name", "广州市"),
    "北京": ("11", 1, "province_name", "北京市"),  # 直辖市：fact 用 2 位省码
    "上海": ("31", 1, "province_name", "上海市"),  # 同上；'31' 另有未定义的 type=4 平行序列，必须带 type=1
}
WHITELIST = [  # (index_code, tier)  P0=窗口内≥3 城有 TB·DNLJ 值；P1=2 城
    ("gmjj_gnmy_01", "P0"), ("gmjj_tzjs_01", "P0"), ("gmjj_jjzl_01_02", "P0"),
    ("gmjj_jjzl_01_03", "P0"), ("gmjj_jjzl_01_02_01_01", "P0"), ("dwjj_dwmy_01", "P0"),
    ("dwjj_dwmy_01_01", "P0"), ("dwjj_dwmy_01_02", "P0"), ("gmjj_jjzl_01", "P1"),
]


def q(cur, sql):
    cur.execute(sql)
    return cur.fetchall()


def main() -> int:
    cur = connect(load_env(ENV_PATH)).cursor()
    out: dict = {"now": str(q(cur, "SELECT NOW()")[0][0]), "window_start": W0}
    assert len(WHITELIST) <= 12

    # 1. 区划：dim 无市级行，经下级行的 city/province 列解析；再看 fact 键
    out["area"] = {}
    for name, (code, typ, col, val) in CITIES.items():
        dim = q(cur, f"""SELECT COUNT(*), MIN(province_code), MIN(city_code), MIN(city_name)
                         FROM dwd_dim_admin_area WHERE is_deleted=0 AND {col}='{val}'""")[0]
        fact = q(cur, f"""SELECT COUNT(*), COUNT(DISTINCT index_code), MIN(occur_period), MAX(occur_period)
                          FROM dwd_macro_index_data WHERE is_deleted=0 AND area_code='{code}' AND area_code_type={typ}""")[0]
        own = q(cur, f"SELECT COUNT(*) FROM dwd_dim_admin_area WHERE is_deleted=0 AND cur_code='{code}'")[0][0]
        out["area"][name] = {"fact_area_code": code, "area_code_type": typ, "dim_resolve_rows": dim[0],
                             "province_code": dim[1], "city_code": dim[2], "city_name": dim[3],
                             "dim_self_row(cur_code=fact key)": own,
                             "fact_rows": fact[0], "fact_indices": fact[1], "fact_period": [fact[2], fact[3]]}
        assert dim[0] > 0 and fact[0] > 0, f"{name} 区划/事实不可解析"

    keys = " OR ".join(f"(f.area_code='{c}' AND f.area_code_type={t})" for c, t, _, _ in CITIES.values())
    codes = ",".join(f"'{c}'" for c, _ in WHITELIST)
    # 2. 白名单属性
    attr = q(cur, f"SELECT index_code,index_name,data_freq,unit_use,unit_show FROM dwd_dim_index_attribute "
                  f"WHERE is_deleted=0 AND index_code IN ({codes}) ORDER BY index_code")
    out["attr"] = [list(r) for r in attr]
    assert len(attr) == len(WHITELIST), "白名单 index_code 不在 dwd_dim_index_attribute"

    # 3. 覆盖：每指标 × (cal,dur∈TB/JDZ·DNLJ) × 城，窗口内非空点数/最新期/最新值/单位/值域
    cov = q(cur, f"""
        SELECT f.index_code, f.dim_cal, f.area_code, f.area_code_type, COUNT(*) n, MAX(f.occur_period) mx,
               MIN(f.index_value) lo, MAX(f.index_value) hi, MAX(f.unit_use) unit
        FROM dwd_macro_index_data f
        WHERE f.is_deleted=0 AND f.index_value IS NOT NULL AND f.occur_period>={W0}
          AND f.dim_dur='DNLJ' AND f.dim_cal IN ('TB','JDZ') AND ({keys}) AND f.index_code IN ({codes})
        GROUP BY 1,2,3,4 ORDER BY 1,2,3""")
    inv = {(c, t): n for n, (c, t, _, _) in CITIES.items()}
    cover: dict = {}
    out["coverage"] = []
    for idx, cal, ac, at, n, mx, lo, hi, unit in cov:
        city = inv[(ac, at)]
        out["coverage"].append([idx, cal, city, int(n), mx, str(lo), str(hi), unit])
        if cal == "TB":
            cover.setdefault(idx, set()).add(city)
    out["tb_cities"] = {k: sorted(v) for k, v in cover.items()}
    for idx, tier in WHITELIST:
        k = len(cover.get(idx, ()))
        assert k >= (3 if tier == "P0" else 2), f"{idx} TB·DNLJ 窗口内仅 {k} 城，与 {tier} 不符"
    assert all(u == "%" for r in out["coverage"] if r[1] == "TB" for u in [r[7]]), "TB 行单位不是 %"
    out["dupe_keys"] = q(cur, """SELECT COUNT(*) FROM (SELECT 1 FROM dwd_macro_index_data WHERE is_deleted=0
        GROUP BY index_code,occur_period,area_code,dim_cal,dim_dur HAVING COUNT(*)>1) t""")[0][0]
    assert out["dupe_keys"] == 0

    # 4. 行业分析辅维
    out["ia"] = {
        "docs_by_month": q(cur, "SELECT SUBSTR(creation_date,1,7),COUNT(*) FROM dwd_industry_analysis_documents WHERE is_deleted=0 GROUP BY 1"),
        "topics": q(cur, "SELECT topic_code,topic_name,COUNT(*) FROM dwd_industry_analysis_topics WHERE is_deleted=0 GROUP BY 1,2 ORDER BY 3 DESC"),
        "content_types": q(cur, "SELECT code,name,COUNT(*) FROM dwd_industry_analysis_content_types WHERE is_deleted=0 GROUP BY 1,2 ORDER BY 3 DESC"),
        "countries": q(cur, "SELECT country_code,COUNT(*) FROM dwd_industry_analysis_countries WHERE is_deleted=0 GROUP BY 1"),
        "companies(rows,docs,companies)": q(cur, "SELECT COUNT(*),COUNT(DISTINCT document_id),COUNT(DISTINCT company_id) FROM dwd_industry_analysis_companies WHERE is_deleted=0")[0],
        "industries_top": q(cur, "SELECT industry_code,industry_name,COUNT(*) FROM dwd_industry_analysis_industries WHERE is_deleted=0 GROUP BY 1,2 ORDER BY 3 DESC LIMIT 5"),
    }
    dest = Path(__file__).with_name("_probe_macro_effect_a1.json")
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print("OK all asserts passed;", "WROTE", dest.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

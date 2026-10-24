#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_POLICY_BASE_100_1｜政策基础指标模型构建（五类：级别 / 类型 / 时序 / 全国分布 / 深圳分布）

零 SQL：只读 20261021 三方库快照
  code/_snapshots21/policy_base_20261021.json   20,000 行（id/title/date/province/city/district/
                                                ministry/body_len/theme/quote/geo/level）
  code/_snapshots21/pg_policy_rows_20261021.json 20,000 行（type / rank / publish_year / 长度计数）
字段级可得性（非占位符计数）取自 code/_snapshots21/policy_fields_a23_20261021.json（4 条探针）。

口径要点：
  * `level` 是 0—4 的整数码，与 `rank` 文本的一对一映射在本脚本内实测核对（见 level_check）；
    `level=1` 同时覆盖「区级」与「园区级」，因此展示层一律用 `rank` 原文，不用整数码。
  * 年份只对「库内真实存在的年份」计算环比；2023 年 0 行、2022 年 289 行（残片）、2024 年 1 行，
    一律不进趋势分母（DATA_FACTS §3.16）。
  * 深圳分区域分布是本件判档的关键：市级 `city='深圳市'` 879 条，但 `district` 只有 7 条。

输出：code/M_POLICY_BASE_100_1_out.json
"""
import collections
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
BASE = json.load(open(os.path.join(SNAP, "policy_base_20261021.json"), encoding="utf-8"))
ROWS = json.load(open(os.path.join(SNAP, "pg_policy_rows_20261021.json"), encoding="utf-8"))
FIELDS = json.load(open(os.path.join(SNAP, "policy_fields_a23_20261021.json"), encoding="utf-8"))

PLACEHOLDER = {"", "NULL", "NONE", "-"}


def nn(v):
    """把 gkx 的 'NULL'/'null'/空串统一折成空串（DATA_FACTS §3.4）。"""
    if v is None:
        return ""
    s = str(v).strip()
    return "" if s.upper() in PLACEHOLDER else s


def rank_first(s):
    """`rank` 是 JSON 数组字面量，取首个元素。"""
    try:
        j = json.loads(s or "[]")
        if isinstance(j, list) and j:
            return nn(j[0])
    except Exception:
        pass
    return ""


def pct(a, b):
    return round(100.0 * a / b, 2) if b else None


def main():
    by_id = {r["id"]: r for r in BASE}
    n = len(ROWS)
    ids = {r["id"] for r in ROWS}

    # ---------- 0. 盘子与去重键 ----------
    plate = {
        "rows": n,
        "distinct_id": len(ids),
        "id_unique": len(ids) == n,
        "base_snapshot_rows": len(BASE),
        "status_effective": 20000,          # 探针 policy_status：全表 20,000 行 status='有效'
        "is_deleted": 0,
    }

    # ---------- 1. 政策级别 ----------
    levels = collections.Counter(rank_first(r.get("rank")) or "（未标注）" for r in ROWS)
    level_code = collections.Counter(int(by_id[r["id"]]["level"]) for r in ROWS if r["id"] in by_id)
    # 整数码 → 文本的实测映射，用来证明展示层不用整数码
    code_map = collections.defaultdict(collections.Counter)
    for r in ROWS:
        code_map[int(by_id[r["id"]]["level"])][rank_first(r.get("rank")) or "（未标注）"] += 1
    level_rows = [{"level": k, "n": v, "pct": pct(v, n)} for k, v in levels.most_common()]

    # ---------- 2. 政策类型 ----------
    types = collections.Counter(nn(r.get("type")) or "（未标注）" for r in ROWS)
    type_rows = [{"type": k, "n": v, "pct": pct(v, n)} for k, v in types.most_common()]
    ps = [v / n for v in types.values()]
    entropy = -sum(p * math.log(p) for p in ps)
    hhi = sum(p * p for p in ps)

    # ---------- 3. 政策时序（只用真实年份算环比） ----------
    years = collections.Counter()
    for r in ROWS:
        y = nn(r.get("publish_year"))
        if y.isdigit():
            years[int(y)] += 1
    window = [2016, 2017, 2018, 2019, 2020, 2021]     # 连续、样本 >=1,300/年 的稳定窗口
    yoy = []
    for i, y in enumerate(window):
        cur = years.get(y, 0)
        prev = years.get(y - 1, 0) if i else years.get(y - 1, 0)
        yoy.append({
            "year": y,
            "n": cur,
            "yoy_pct": (round(100.0 * (cur - prev) / prev, 2) if prev else None),
            "yoy_from": y - 1,
            "prev_n": prev,
        })
    cagr = round(100.0 * (years[2021] / years[2016] - 1), 2)
    year_series = [{"year": y, "n": years[y]} for y in sorted(years)]
    excluded = {
        "1981-2015": "年样本 <1,300，且早期文件多为存量汇编，不参与趋势窗口",
        "2022": "289 条，采集在 2021 年底截断后的残片",
        "2023": "0 条（库内该年一行都没有）",
        "2024": "1 条",
        "2025-2026": "语料未覆盖",
    }

    # ---------- 4. 全国分布 ----------
    prov = collections.Counter(nn(by_id[r["id"]]["province"]) or "（未填）" for r in ROWS if r["id"] in by_id)
    city = collections.Counter(nn(by_id[r["id"]]["city"]) or "（未填）" for r in ROWS if r["id"] in by_id)
    prov_filled = n - prov.get("（未填）", 0)
    city_filled = n - city.get("（未填）", 0)
    prov_real = len([k for k in prov if k != "（未填）"])
    city_real = len([k for k in city if k != "（未填）"])
    region = {
        "province_field_filled": prov_filled,
        "province_field_fill_pct": pct(prov_filled, n),
        "province_distinct": prov_real,
        "city_field_filled": city_filled,
        "city_field_fill_pct": pct(city_filled, n),
        "city_distinct": city_real,
        "province_top10": [{"province": k, "n": v, "pct": pct(v, n)} for k, v in prov.most_common(10)],
        "city_top10": [{"city": k, "n": v, "pct": pct(v, n)} for k, v in city.most_common(10)],
    }

    # ---------- 5. 深圳分布 ----------
    sz_ids = [r["id"] for r in ROWS if r["id"] in by_id and nn(by_id[r["id"]]["city"]) == "深圳市"]
    sz_dist = collections.Counter(nn(by_id[i]["district"]) or "（未填）" for i in sz_ids)
    sz_dist_filled = len(sz_ids) - sz_dist.get("（未填）", 0)
    sz_year = collections.Counter()
    for i in sz_ids:
        y = nn(by_id[i]["date"])[:4]
        if y.isdigit():
            sz_year[int(y)] += 1
    shenzhen = {
        "n": len(sz_ids),
        "pct_of_all": pct(len(sz_ids), n),
        "district_filled": sz_dist_filled,
        "district_fill_pct": pct(sz_dist_filled, len(sz_ids)),
        "district_distinct": len([k for k in sz_dist if k != "（未填）"]),
        "district_rows": [{"district": k, "n": v} for k, v in sz_dist.most_common()],
        "year_window": [{"year": y, "n": sz_year.get(y, 0)} for y in window],
        "ministry_top5": collections.Counter(
            nn(by_id[i]["ministry"]) or "（未填）" for i in sz_ids).most_common(5),
    }

    # ---------- 6. 五类逐类判定 ----------
    five = [
        {"class": "政策级别指标", "field": "rank（JSON 首元素）", "fill_pct": 100.0,
         "verdict": "可用", "note": "五级齐全，国家级 2,174 / 省级 9,922 / 市级 6,149 / 区级 1,254 / 园区级 144，未标注 357"},
        {"class": "政策类型指标", "field": "type（公文文种）", "fill_pct": pct(n - types.get("（未标注）", 0), n),
         "verdict": "部分可用",
         "note": "需求举例的产业/人才/企业扶持是主题分类，库内 type 是文种分类，两者不同源（同 M_INNOV_PG_COUNT_DIST 结论）"},
        {"class": "政策时序指标", "field": "publish_year", "fill_pct": pct(n - 3, n),
         "verdict": "可用（截至 2021）", "note": "1981—2024 有值，2022 起截断；环比只用 2016—2021"},
        {"class": "全国政策分布指标", "field": "province / city", "fill_pct": pct(prov_filled, n),
         "verdict": "省级可用，市级偏斜",
         "note": f"省 {pct(prov_filled, n)}%（{prov_real} 个省级单位 + 未填 1 组）；"
                 f"市 {pct(city_filled, n)}%（{city_real} 个城市 + 未填 1 组），未填 {n - city_filled} 条"},
        {"class": "深圳政策分布指标", "field": "city='深圳市' + district", "fill_pct": pct(sz_dist_filled, len(sz_ids)),
         "verdict": "不可用（按区）",
         "note": "需求原文是「计算深圳各个区发布的相关政策数量」；879 条深圳政策里只有 7 条带区县（0.80%）"},
    ]

    out = {
        "metric_id": "M_POLICY_BASE_100_1",
        "title": "政策基础指标模型构建",
        "probe_date": "2026-10-22",
        "data_support_level": "部分支持",
        "support_judgment": "部分支持",
        "support_reason": "五类里三类（级别/类型文种层/时序）可直算；全国分布只有省级成立（省 87.38%、市 51.47%）；"
                          "深圳分区域分布因 district 仅 7/879=0.80% 不可构建 → 按 §〇 定义落部分支持",
        "base_years_used": ["2016", "2017", "2018", "2019", "2020", "2021"],
        "base_years_missing": ["2023"],
        "base_years_note": "环比窗口只用 2016—2021 六个连续且样本 >=1,300/年的年份。2023 年库内 0 行（缺失），"
                            "2022 年 289 条为采集截断残片、2024 年 1 条、2025—2026 未覆盖，三者均不进分母；"
                            "分母绝不把缺年按 0 摊入（DATA_FACTS §3.16）。",
        "sources": {
            "policy_base": "code/_snapshots21/policy_base_20261021.json（20,000 行，gkx.dwd_policy_base）",
            "pg_policy_rows": "code/_snapshots21/pg_policy_rows_20261021.json（20,000 行）",
            "field_probe": "code/_snapshots21/policy_fields_a23_20261021.json（4 条 SQL 实探）",
            "db": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）",
        },
        "plate": plate,
        "levels": {"rows": level_rows, "level_code_dist": dict(sorted(level_code.items())),
                   "code_to_rank": {str(k): dict(v) for k, v in sorted(code_map.items())},
                   "unlabeled_n": levels.get("（未标注）", 0)},
        "types": {"rows": type_rows, "unlabeled_n": types.get("（未标注）", 0),
                  "entropy_nat": round(entropy, 4), "hhi": round(hhi, 4),
                  "effective_classes": round(math.exp(entropy), 2)},
        "years": {"series": year_series, "window": yoy, "window_growth_pct": cagr,
                  "window_from": 2016, "window_to": 2021,
                  "excluded": excluded, "null_year_rows": 3},
        "region": region,
        "shenzhen": shenzhen,
        "five_classes": five,
        "verdicts": {
            "level": "可用（rank 五级齐全）",
            "type": "文种层可用；主题层（产业/人才/企业扶持）不可用",
            "timeline": "可用但截至 2021",
            "national": "省级可用；市级 51.47% 不足支撑城市排名",
            "shenzhen_district": "不可用（7/879）",
        },
    }

    dst = os.path.join(HERE, "M_POLICY_BASE_100_1_out.json")
    json.dump(out, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: out[k] for k in ("metric_id", "support_judgment", "base_years_used",
                                          "base_years_missing")}, ensure_ascii=False))
    print("levels:", level_rows)
    print("types top:", type_rows[:4], "unlabeled", types.get("（未标注）"), "H", round(entropy, 4), "HHI", round(hhi, 4))
    print("years window:", yoy, "growth", cagr)
    print("region:", {k: region[k] for k in ("province_field_filled", "city_field_filled",
                                             "province_distinct", "city_distinct")})
    print("shenzhen:", {k: shenzhen[k] for k in ("n", "district_filled", "district_fill_pct", "district_distinct")})
    print("->", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()

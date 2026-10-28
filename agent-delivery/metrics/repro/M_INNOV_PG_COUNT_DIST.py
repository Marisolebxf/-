#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""政策数量分布（M_INNOV_PG_COUNT_DIST）——零 SQL 复算。

数据入口（均为本机快照，全部由 gkx 三方库导出）：
  code/_snapshots21/pg_policy_rows_20261021.json   政策全表 20,000 行（含 type/rank/年份/层级）
  code/_snapshots21/base_20261021.json             企业底册 189,116 行（城市口径对照）

口径：一条政策 = 一行 = 一个 id；按 年份 × 类型 × 层级 × 地域 四维统计，
并给出类型结构熵 / HHI 与城市分布合成分（后者只作展示，不作跨城评价，见 §三）。

运行：python3 code/M_INNOV_PG_COUNT_DIST.py
产物：code/M_INNOV_PG_COUNT_DIST_out.json
"""
from __future__ import annotations

import json
import math
import os
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_INNOV_PG_COUNT_DIST_out.json")
METRIC_ID = "M_INNOV_PG_COUNT_DIST"

PLACEHOLDER = {"NULL", "", "NONE", "-"}


def norm(v) -> str:
    """统一清洗占位符（DATA_FACTS §3.4：大小写两种 'null' 都要判）。"""
    s = "" if v is None else str(v).strip()
    return "" if s.upper() in PLACEHOLDER else s


def parse_rank(v) -> str:
    """rank 存的是 JSON 数组字面量，如 '["省级","市级"]'，取第一个为层级。"""
    s = norm(v)
    if not s:
        return ""
    if s.startswith("["):
        try:
            arr = json.loads(s)
            return norm(arr[0]) if arr else ""
        except Exception:
            return ""
    return s


def entropy(counts) -> float:
    n = sum(counts)
    if n <= 0:
        return 0.0
    return -sum((c / n) * math.log(c / n) for c in counts if c > 0)


def main() -> None:
    t0 = time.time()
    rows = json.load(open(os.path.join(SNAP, "pg_policy_rows_20261021.json"), encoding="utf-8"))
    base = json.load(open(os.path.join(SNAP, "base_20261021.json"), encoding="utf-8"))

    for r in rows:
        for k in ("province", "city", "district", "ministry", "type"):
            r[k] = norm(r.get(k))
        r["lvl"] = parse_rank(r.get("rank"))
        y = norm(r.get("publish_year"))
        r["yr"] = int(y) if y.isdigit() else None

    n_total = len(rows)
    ids = {r["id"] for r in rows}

    # ---------- 1. 年份 ----------
    yc = Counter(r["yr"] for r in rows if r["yr"])
    years_sorted = sorted(yc)
    # 2022 年 289 条为断崖残片、2024 年仅 1 条；可用年窗止于 >=100 条的最后一年
    usable_max = max(y for y in years_sorted if yc[y] >= 100)
    year_dist = [{"year": y, "n": yc[y]} for y in years_sorted]
    year_missing = [y for y in range(usable_max + 1, 2027) if yc.get(y, 0) == 0]

    # ---------- 2. 类型 ----------
    tc = Counter(r["type"] or "（未标注）" for r in rows)
    type_dist = [{"type": k, "n": v, "share": round(100 * v / n_total, 3)}
                 for k, v in tc.most_common()]
    type_counts = list(tc.values())
    H = entropy(type_counts)
    hhi = sum((v / n_total) ** 2 for v in type_counts)
    type_nonnull = sum(1 for r in rows if r["type"])

    # ---------- 3. 层级 ----------
    lc = Counter(r["lvl"] or "（未标注）" for r in rows)
    level_dist = [{"level": k, "n": v, "share": round(100 * v / n_total, 3)}
                  for k, v in lc.most_common()]

    # ---------- 4. 地域覆盖 ----------
    prov_fill = sum(1 for r in rows if r["province"])
    city_fill = sum(1 for r in rows if r["city"])
    dist_fill = sum(1 for r in rows if r["district"])
    pc = Counter(r["province"] for r in rows if r["province"])
    cc = Counter(r["city"] for r in rows if r["city"])
    dc = Counter(r["district"] for r in rows if r["district"])
    four = ["深圳市", "广州市", "东莞市", "惠州市"]
    firms = Counter(b[4] for b in base)
    four_city = []
    for c in four:
        sub = [r for r in rows if r["city"] == c]
        four_city.append({
            "city": c, "n": len(sub),
            "share_all": round(100 * len(sub) / n_total, 3),
            "types": len({r["type"] for r in sub if r["type"]}),
            "levels": len({r["lvl"] for r in sub if r["lvl"]}),
            "districts": len({r["district"] for r in sub if r["district"]}),
            "firms": firms.get(c, 0),
            "per_1000_firms": round(1000 * len(sub) / firms.get(c, 1), 3),
        })

    # ---------- 5. 发文机关 ----------
    mc = Counter(r["ministry"] for r in rows if r["ministry"])
    ministry_top = [{"ministry": k, "n": v} for k, v in mc.most_common(15)]

    # ---------- 6. 城市合成分（展示用，n>=100 的城市） ----------
    big = [c for c, n in cc.items() if n >= 100]
    comp = []
    for c in big:
        sub = [r for r in rows if r["city"] == c]
        comp.append({"city": c, "n": len(sub),
                     "types": len({r["type"] for r in sub if r["type"]}),
                     "levels": len({r["lvl"] for r in sub if r["lvl"]})})
    mx_n = max(x["n"] for x in comp)
    mx_t = max(x["types"] for x in comp)
    mx_l = max(x["levels"] for x in comp)
    for x in comp:
        x["composite"] = round(
            (x["n"] / mx_n * 100 + x["types"] / mx_t * 100 + x["levels"] / mx_l * 100) / 3, 2)
    comp.sort(key=lambda x: -x["composite"])

    result = {
        "metric_id": METRIC_ID,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "data_source": "gkx.dwd_policy_base @ 183.240.141.251:3318（快照 20,000 行，零 SQL 复算）",
        "support_judgment": "部分支持",
        "n_records": n_total,
        "n_distinct_id": len(ids),
        "year_coverage": {
            "min": min(years_sorted), "max": max(years_sorted),
            "usable_max": usable_max,
            "note": "2022 年 289 条、2023 年 0 条、2024 年 1 条为采集截断；2023—2026 不是『无政策』，是语料未覆盖",
            "years_missing_after_usable_max": year_missing,
        },
        "year_dist": year_dist,
        "type": {
            "n_classes_nonnull": len({r["type"] for r in rows if r["type"]}),
            "n_classes_incl_missing": len(tc),
            "nonnull_rows": type_nonnull,
            "nonnull_share": round(100 * type_nonnull / n_total, 3),
            "entropy_nats": round(H, 4),
            "effective_classes": round(math.exp(H), 3),
            "hhi": round(hhi, 4),
            "dist": type_dist,
        },
        "level": {"n_classes": len({r["lvl"] for r in rows if r["lvl"]}), "dist": level_dist},
        "geo": {
            "province_fill": prov_fill, "province_fill_rate": round(100 * prov_fill / n_total, 3),
            "city_fill": city_fill, "city_fill_rate": round(100 * city_fill / n_total, 3),
            "district_fill": dist_fill, "district_fill_rate": round(100 * dist_fill / n_total, 3),
            "n_provinces": len(pc), "n_cities": len(cc), "n_districts": len(dc),
            "province_top": [{"province": k, "n": v} for k, v in pc.most_common(10)],
            "city_top": [{"city": k, "n": v} for k, v in cc.most_common(10)],
            "four_city": four_city,
        },
        "ministry": {"n_distinct": len(mc), "top": ministry_top},
        "city_composite": comp[:20],
        "caveats": [
            "城市维覆盖率 51.47%，district 维 5.83%，且东莞 8 条 / 惠州 0 条，跨城比较不可作评价，只能作分布展示",
            "2022 年后语料截断，年度趋势只能宣称覆盖 1981—2021",
            "类型维 1,862 条未标注（9.31%），按『未标注』单列，不并入任何一类",
            "城市合成分是展示排序，不是评价分，禁止用于政策力度排名",
        ],
        "runtime_sec": None,
    }

    print(f"[{METRIC_ID}] n={n_total} ids={len(ids)}")
    print("年份: ", ", ".join(f"{x['year']}={x['n']}" for x in year_dist[-8:]))
    print(f"类型: {result['type']['n_classes_nonnull']} 类非空 / 熵 {H:.4f} / HHI {hhi:.4f} / 有效类 {math.exp(H):.2f}")
    print("层级: ", ", ".join(f"{x['level']}={x['n']}" for x in level_dist))
    print(f"地域填充: 省 {prov_fill} / 市 {city_fill} / 区县 {dist_fill}")
    print("四城: ", ", ".join(f"{x['city']}={x['n']}({x['types']}类,{x['levels']}级)" for x in four_city))
    print("合成分 top5: ", [(x["city"], x["composite"]) for x in comp[:5]])

    result["runtime_sec"] = round(time.time() - t0, 3)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print(f"saved {OUT} ({result['runtime_sec']}s)")


if __name__ == "__main__":
    main()

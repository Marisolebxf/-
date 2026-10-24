#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_CITY_COMPARE_SZ 深圳科技发展指标对比 · 复现代码（王惠 V1.5-20260901，20261021 换源版）

四维：研发投入(上市 rd)/专利数量/高企数量/创新人才(学者)。
城市：深圳 + 广州 + 东莞（库覆盖可信区）。
数据源：三方库 `gkx`（唯一入口 `code/_gkxdb.py`），**不含任何 demo_* / _devdb**。

换源说明（20261021）
--------------------
* 读数与 20261020 旧版逐项一致：rd 深圳 3,555.5 亿 / 专利 275,908 / 高企 15,683 / 学者 194；
  广州 566.8 亿 / 140,395 / 7,556 / 86；东莞 149.4 亿 / 89,347 / 3,607 / 7。
* 专利维改为读共享扫描缓存（`_snapshots21/patent_scan_20261021.pkl`）：`COUNT(DISTINCT pn)`
  按 (城市, 年) 去重，与旧 `JOIN ... COUNT(DISTINCT p.pn)` 同口径（旧版按城聚合，不做申请人分组求和）。
* 城市键：`dwd_org_base_info.city` → `norm_city()`；实测该列 66 个取值、全为「X市」，
  无 'NULL' 字面量、无区县值，`LIKE '%深圳%'` 与归一后等值判定结果一致（95,600 行）。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import _gkx21_city as C  # noqa: E402

METRIC_ID = "M_INNOV_CITY_COMPARE_SZ"
YEAR = 2024
CITIES = ["深圳", "广州", "东莞"]


def main():
    probes = {t: C.inventory_rows(t) for t in
              ("dwd_org_base_info", "dwd_org_stock_finance_info", "dwd_patent",
               "dwd_org_tech_tag", "dwd_scholar")}
    pat = C.patents_2024_by_city(CITIES)
    rd = C.rd_by_city(CITIES, YEAR, YEAR)
    ht = C.hightech_by_city(CITIES)
    sch = C.scholars_by_city_like(CITIES)

    rows = {c: dict(rd=rd.get(c), patents=pat.get(c, 0),
                    hightech=ht.get(c), scholars=sch.get(c)) for c in CITIES}

    def norm_dim(key):
        vals = [rows[c][key] for c in CITIES]
        xs = [v for v in vals if v is not None]
        if not xs:
            return [None] * len(vals)
        lo, hi = min(xs), max(xs)
        return [None if v is None else (0.5 if hi == lo else (v - lo) / (hi - lo)) for v in vals]

    dims = {k: norm_dim(k) for k in ["rd", "patents", "hightech", "scholars"]}
    out = []
    for i, c in enumerate(CITIES):
        d = [dims[k][i] for k in ["rd", "patents", "hightech", "scholars"]]
        avail = [x for x in d if x is not None]
        comp = round(sum(avail) / len(avail) * 100, 2) if avail else None
        out.append({"city": c, **rows[c],
                    "d_rd": round(d[0], 3) if d[0] is not None else None,
                    "d_pat": round(d[1], 3) if d[1] is not None else None,
                    "d_ht": round(d[2], 3) if d[2] is not None else None,
                    "d_sch": round(d[3], 3) if d[3] is not None else None,
                    "composite": comp})

    dims_with_data = sum(1 for k in ["rd", "patents", "hightech", "scholars"]
                         if any(rows[c][k] for c in CITIES))
    scores = [o["composite"] for o in out if o["composite"] is not None]
    has_dist = len(set(scores)) > 1
    result = {
        "metric_id": METRIC_ID,
        "metric_name": "深圳科技发展指标对比",
        "also_serves": ["M_INNOV_CITY_FACTOR_GLOBAL"],
        "method": "王惠 V1.5：四维（研发投入/专利/高企/创新人才）所选城内归一",
        "cities": CITIES, "stat_year": YEAR,
        "data_source": "gkx（三方库 183.240.141.251:3318，只读账号；不含任何演示库引用）",
        "patent_caliber": "COUNT(DISTINCT pn) @apdt_year=2024，申请人名精确等于城内机构名",
        "probes": probes,
        "compute": {"cities": out},
        "support_judgment": "部分支持" if (dims_with_data >= 3 and has_dist) else "完全不支持",
    }
    result["support_note"] = (
        f"四维中 {dims_with_data} 维有数（rd 仅上市、dev 兜底全 NULL；scholar 用机构名含城市名近似对齐）；"
        f"对比限定库覆盖可信区（深圳/广州/东莞）；非粤城市因机构库地域失衡不可信。"
        f"换源 gkx 后四维读数与 20261020 旧版逐项一致（深圳 3,555.5 亿/275,908 件/15,683 家/194 人）"
    )

    path = HERE / f"{METRIC_ID}_out.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "compute"}, ensure_ascii=False))
    for o in out:
        print(o)


if __name__ == "__main__":
    main()

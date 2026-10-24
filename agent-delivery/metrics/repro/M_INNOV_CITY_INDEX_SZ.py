#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_CITY_INDEX_SZ 深圳创新能力指数 · gkx 版（20261021 改源）

口径与 20261020 版 V1.6 完全一致，只把数据面换成 `gkx` 三方库：
三维 = 创新资源(Σ研发经费 2019–2024) / 创新主体(0.5×机构 + 0.5×高企) / 创新环境(有效政策)，
城内极值归一 + 等权 ×100。城市 = 深圳/广州/东莞（gkx 底册 99.82% 粤集中，可信区）。

改源要点（不是简单换前缀）
--------------------------
* 城市键：`city LIKE '%深圳%'` → `city = '深圳市'`（gkx 已把 city 规范化到市级全称，§3.8）；
* 存续机构：`COUNT(DISTINCT org_id)` 走本地底册 + `reg_status IN (REG_ALIVE)`，
  实测与库内聚合逐位一致（SZ 95,600 / GZ 49,604 / DG 33,590，广州有 1 行 `在营（开业）` 不属标准表述）；
* 高企：`dwd_org_tech_tag.org_id` 精确匹配底册 `org_id`（不用 `org_id` JOIN 两遍全表），
  实测 15,476 / 7,499 / 3,584 与原读数一致；
* 政策：`city` 市级等值 + 省级共享。**gkx 的省级政策 city 是字面 `'NULL'`（9,706 行，无真 NULL）**，
  旧的 `city IS NULL` 在 gkx 上返回 0 → 改写为 `UPPER(TRIM(city)) IN ('NULL','')`，否则省级 231 件会凭空消失；
* 研发经费：`dwd_org_stock_finance_info`（上市主体年报口径，2019–2024 窗），org_id→city 本地归城。
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _city21_common as C  # noqa: E402

CITIES = C.CITY_KEYS


def main():
    raw = C.build_raw()
    org_reg = raw["org_reg"]

    rows = []
    for city in CITIES:
        rd = float(raw["rd_sum"].get(city, 0.0))
        org_alive = sum(int(r["n"]) for r in org_reg
                        if r["city"] == city and (r["reg_status"] or "") in C.REG_ALIVE)
        org_total = sum(int(r["n"]) for r in org_reg if r["city"] == city)
        hq = int(raw["hitech_by_city"].get(city, 0))
        pol_city = int(raw["policy_city"].get(city, 0))
        pol_prov = int(raw["policy_prov_shared_n"])
        rows.append({
            "city": C.SHORT[city], "city_code": city,
            "rd_funding_sum": round(rd, 2),
            "org_alive_cnt": org_alive, "org_total_cnt": org_total,
            "hightech_cnt": hq,
            "policy_cnt": pol_city + pol_prov,
            "policy_city_cnt": pol_city, "policy_prov_shared": pol_prov,
        })

    nf = C.norm([r["rd_funding_sum"] for r in rows])
    no = C.norm([r["org_alive_cnt"] for r in rows])
    nh = C.norm([r["hightech_cnt"] for r in rows])
    npv = C.norm([r["policy_cnt"] for r in rows])
    for i, r in enumerate(rows):
        resource = nf[i]
        entity = 0.5 * no[i] + 0.5 * nh[i]
        env = npv[i]
        r["d_resource"], r["d_entity"], r["d_env"] = resource, round(entity, 4), env
        r["index_score"] = round(100 / 3 * (resource + entity + env), 1)

    result = {
        "metric_id": "M_INNOV_CITY_INDEX_SZ",
        "metric_name": "深圳创新能力指数",
        "method": "王惠 V1.6：创新资源/主体/环境三维，城内极值归一+等权×100",
        "source_db": "gkx（183.240.141.251:3318）",
        "cities": [C.SHORT[c] for c in CITIES],
        "probes": {
            "gkx.dwd_org_base_info": 189116,
            "gkx.dwd_org_stock_finance_info": 40239,
            "gkx.dwd_org_annual_financial_info": 90926,
            "gkx.dwd_org_tech_tag": 202424,
            "gkx.dwd_policy_base": 20000,
        },
        "compute": {"cities": rows},
        "support_judgment": "部分支持",
        "support_note": (
            f"资源维研发经费可用（上市主体年报口径，2019–2024 窗 {raw['rd_rows']:,} 行非空、其中 {raw['rd_unmapped']} 行无法归城；全表非空 {19587:,} 行）；"
            "人员口径 development_employee 100% NULL 不可作备选；主体维机构/高企标签齐全；"
            "环境维政策 city 有 9,706 行字面 'NULL'（占 48.5%）已归空并单列省级共享 231 件；"
            "机构底册 99.82% 粤集中 → 宇宙限粤三城 ⇒ 部分支持"
        ),
        "change_note": (
            "换源后资源/主体/环境三维读数与 20261020 版逐位一致（研发经费 SZ 1,366,367,257,075.05；"
            "高企 15,476/7,499/3,584；政策市级 879/325/8 + 省级共享 231）；"
            "唯一改写是省级政策判定（gkx 用字面 'NULL' 而非 SQL NULL），不改口径。"
        ),
    }
    p = C.write_out("M_INNOV_CITY_INDEX_SZ", result)
    print("wrote", p)
    for r in rows:
        print(r["city"], r["index_score"], r["d_resource"], r["d_entity"], r["d_env"],
              r["rd_funding_sum"], r["org_alive_cnt"], r["hightech_cnt"], r["policy_cnt"])


if __name__ == "__main__":
    main()

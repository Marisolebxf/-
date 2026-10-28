#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_GBA_ENV_INDEX · 湾区创新环境指数（INNOV / DS-05-GBA-ENV）。

王惠 V1.5 口径：政策供给 / 政策覆盖 / 高企密度 三维等权 × 100。

20261021 版实测口径（gkx + 授权缓存）：
- 11 城中仅 4 城有机构底册（深圳/广州/东莞/惠州）；港澳与珠三角其余 7 城机构数为 0；
- `dwd_policy_base.theme` 字面 'NULL' 19,998/20,000 → 政策覆盖维以政策 `type` 广度代理；
- 输出 `env_index`（三维等权）与二维敏感性（供给+密度，去掉代理维）。

零专利 SQL：本指标不使用专利表。

输出：code/M_INNOV_GBA_ENV_INDEX_out.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
FACTS = HERE / "_snapshots21" / "innov21_facts_20261021.json"
OUT = HERE / "M_INNOV_GBA_ENV_INDEX_out.json"
METRIC_ID = "M_INNOV_GBA_ENV_INDEX"
GBA11 = ["广州市", "深圳市", "珠海市", "佛山市", "惠州市", "东莞市",
         "中山市", "江门市", "肇庆市", "香港", "澳门"]


def minmax(vals):
    lo, hi = min(vals), max(vals)
    return [0.5] * len(vals) if hi == lo else [(v - lo) / (hi - lo) for v in vals]


def main():
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    orgs = f["base"]["gba_city_counts"]
    pol = f["policy_city"]
    breadth = f["policy_type_breadth"]
    hq = f["hightech_city"]["by_city"]
    inst = f["institute_city"]

    scope = [c for c in GBA11 if orgs.get(c, 0) >= 100]
    rows = []
    for c in scope:
        n_org = int(orgs.get(c, 0))
        rows.append({"city": c, "orgs": n_org,
                     "policy_cnt": int(pol.get(c, 0)),
                     "policy_type_breadth": int(breadth.get(c, 0)),
                     "hightech_cnt": int(hq.get(c, 0)),
                     "hightech_density": round(hq.get(c, 0) / n_org, 5) if n_org else 0.0,
                     "research_inst_cnt": int(inst.get(c, 0))})

    ns = minmax([r["policy_cnt"] for r in rows])
    nb = minmax([r["policy_type_breadth"] for r in rows])
    nd = minmax([r["hightech_density"] for r in rows])
    for i, r in enumerate(rows):
        r["n_supply"] = round(ns[i], 4)
        r["n_coverage_proxy"] = round(nb[i], 4)
        r["n_density"] = round(nd[i], 4)
        r["env_index"] = round(100 * (ns[i] + nb[i] + nd[i]) / 3, 1)
        r["env_index_2dim_sensitivity"] = round(100 * (ns[i] + nd[i]) / 2, 1)

    policy_only = []
    for c in GBA11:
        if c in scope:
            continue
        n = int(pol.get(c, 0))
        if n > 0:
            policy_only.append({"city": c, "policy_cnt": n, "orgs": int(orgs.get(c, 0)),
                                "policy_type_breadth": int(breadth.get(c, 0)),
                                "note": "有市级政策、机构底册 <100 家 → 高企密度维不可算，不入 env_index"})

    result = {
        "metric_id": METRIC_ID,
        "formula_owner": "王惠",
        "generated_at": time.strftime("%Y-%m-%d"),
        "source_db": "gkx",
        "source_detail": {
            "机构/高企": "base_20261021.json + cityfam_hightech_20261021.json",
            "政策": "gkx.dwd_policy_base（20,000 行小表，按 city/type 聚合）",
            "科研院所": "gkx.dwd_research_institute_base_info（2,074 行）",
        },
        "method": "三维等权×100：政策供给 min-max + 政策覆盖(type 广度代理) min-max + 高企密度 min-max",
        "asof": time.strftime("%Y-%m-%d"),
        "probes": {
            "org_base_info_total": f["table_counts"]["dwd_org_base_info"]["rows"],
            "policy_total": f["policy_total"],
            "policy_status": f["policy_status"],
            "policy_theme_null": f["policy_theme_null"],
            "policy_city_null_rows": int(pol.get("NULL", 0)),
            "forg_total": f["table_counts"]["dwd_forg_base_info"]["rows"],
            "patent_apdt_year_range": [min(int(k) for k in f["patent"]["year"]),
                                       max(int(k) for k in f["patent"]["year"])],
        },
        "gba_11_city_org_counts": orgs,
        "computable_cities": scope,
        "missing_cities": [c for c in GBA11 if c not in scope],
        "policy_only_cities": policy_only,
        "rows": rows,
        "support_judgment": "部分支持",
        "support_reason": (
            "11 城中仅 4 城有机构底册（深圳/广州/东莞/惠州，合计 188,774 家）；"
            "珠海 0 家、佛山 1 家、中山 1 家、江门/肇庆/香港/澳门 0 家，港澳 forg 有效命中 0；"
            "政策覆盖维 theme 字面 NULL 19,998/20,000，只能用 type 广度为代理 → 不得超过部分支持"
        ),
        "notes": [
            "政策供给按 city 命中且 status='有效'（全库 20,000 行 status 均为有效，故 status 过滤无区分度）；",
            "国家级政策 city 为 'NULL'（9,706 行）未按 11 城共享计入，避免把同一政策重复摊到各城；",
            "高企口径 = cityfam_hightech 名单（27,936 个 org_id），按 org_id 关联底册城市；",
            "政策 type 广度 = COUNT(DISTINCT type)，type 取值形如「政策文件-管理办法/实施方案」「申报通知」，"
            "不是产业主题；它只能代理「政策工具箱宽度」，不能代理「政策覆盖的产业范围」。",
        ],
        "elapsed_sec": round(time.time() - t0, 2),
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(json.dumps({"cities": {r["city"]: r["env_index"] for r in rows},
                      "two_dim": {r["city"]: r["env_index_2dim_sensitivity"] for r in rows},
                      "missing": result["missing_cities"],
                      "policy_only": policy_only,
                      "support": result["support_judgment"]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

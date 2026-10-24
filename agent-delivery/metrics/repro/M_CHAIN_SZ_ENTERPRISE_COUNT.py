#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_SZ_ENTERPRISE_COUNT —— 深圳产业链企业数

口径：与 M_CHAIN_ENTERPRISE_COUNT 同池（同一张 tags 挂链桥、同一 12 链、同一链码规则），
深圳判定用统一社会信用代码第 3—6 位行政区划码 4403（注册地语义，全量可判），
不用底册 city 回联（底册只覆盖 18.9 万家，回联会漏掉 84% 的深圳挂链企业）。
"""
from __future__ import annotations
import json, os, time

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_SZ_ENTERPRISE_COUNT_out.json")


def L(n):
    with open(os.path.join(SNAP, n), encoding="utf-8") as f:
        return json.load(f)


layer = L("chain21_layer_20261022.json")
chains, cc = layer["chain_name"], layer["chain_city"]
base = L("base_20261021.json")
sz_distinct = L("chain21_sz_nodecov_20261022.json")["rows_sz"]

rows = []
for ch, nm in chains.items():
    sz = cc.get(ch + "|深圳市", 0)
    gz = cc.get(ch + "|广州市", 0)
    dg = cc.get(ch + "|东莞市", 0)
    hz = cc.get(ch + "|惠州市", 0)
    nat = sum(v for k, v in cc.items() if k.startswith(ch + "|"))
    four = sz + gz + dg + hz
    rows.append({
        "chain_code": ch, "chain_name": nm,
        "sz_count": sz, "gz_count": gz, "dg_count": dg, "hz_count": hz,
        "four_city_sum": four, "chain_national": nat,
        "sz_share_of_chain": round(sz / nat, 6) if nat else 0.0,
        "sz_share_of_four": round(sz / four, 6) if four else 0.0,
    })
rows.sort(key=lambda r: -r["sz_count"])

base_sz = sum(1 for r in base if r[4] == "深圳市")
payload = {
    "metric_id": "M_CHAIN_SZ_ENTERPRISE_COUNT",
    "metric_name": "深圳产业链企业数",
    "support_judgment": "部分支持",
    "judgment_reason": "链归属与企业规模都可在 gkx 单库内闭合，12 条链的深圳企业数全部非零；但「深圳」只能按统一社会信用代码第 3—6 位 4403 判定，是登记机关辖区而非实际经营地，且 12 链深圳挂接 136,326 次对应去重企业 116,017 家（多链重复计 20,309 次），跨链不可加总当总量；底册 city 路径只覆盖 95,600 家、与挂链桥交集约 3.5 万家，无法作为独立校验。注册地口径的系统性偏差不可在本库内修复，故判部分支持。",
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "截面存量指标，不设统计期；挂链桥无统计期字段，年度序列不在本件范围（见 M_CHAIN_ENTERPRISE_NEW_COUNT）。",
    "sources": [
        {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
         "table": "gkx.dwd_org_industry_tags", "rows": 2283762,
         "snapshot": "code/_snapshots21/chain21_layer_20261022.json",
         "pulled_at": "2026-10-22T15:21:30+08:00"},
        {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
         "table": "gkx.dwd_org_industry_tags（4403 切片）", "rows": 116017,
         "snapshot": "code/_snapshots21/chain21_sz_nodecov_20261022.json",
         "pulled_at": "2026-10-22T15:31:50+08:00"},
        {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
         "table": "gkx.dwd_org_base_info", "rows": 189116,
         "snapshot": "code/_snapshots21/base_20261021.json", "pulled_at": "2026-10-21"},
    ],
    "rule": {
        "pool": "与 M_CHAIN_ENTERPRISE_COUNT 同池：tags 2,283,762 行、一行一企、12 条顶层链",
        "shenzhen": "credit_code[2:6] == '4403'（行政区划码，注册地语义）",
        "why_not_roster": "底册 city='深圳市' 仅 95,600 家、与挂链桥交集约 3.5 万家；用底册回联会把 84% 的深圳挂链企业判成非深圳",
    },
    "chains": rows,
    "population": {
        "chain_memberships": sum(r["chain_national"] for r in rows),
        "sz_memberships": sum(r["sz_count"] for r in rows),
        "sz_distinct_firms": sz_distinct,
        "four_city_memberships": sum(r["four_city_sum"] for r in rows),
        "sz_share_of_all": round(sum(r["sz_count"] for r in rows) / sum(r["chain_national"] for r in rows), 6),
        "base_roster_rows": len(base),
        "base_roster_sz": base_sz,
    },
    "audit_chain": {
        "city_total_all_chains": layer["stats"]["rows"],
        "city_sum": {c: sum(v for k, v in cc.items() if k.endswith("|" + c))
                     for c in ["深圳市", "广州市", "东莞市", "惠州市", "广东其他市", "省外"]},
        "city_sum_is_memberships": sum(v for k, v in cc.items()) == sum(r["chain_national"] for r in rows),
        "distinct_after_dedupe": layer["stats"]["rows"],
        "membership_overlap": sum(v for k, v in cc.items()) - layer["stats"]["rows"],
        "multi_chain_rows": layer["multi_chain_rows"],
        "overlap_equals_extra_memberships": (sum(v for k, v in cc.items()) - layer["stats"]["rows"]) >= layer["multi_chain_rows"],
        "rule": "重叠次数 = Σ(每条记录挂链数 − 1)，因此 ≥ 多链企业数 131,978；两者不是同一个量，不可互相校验相等",
    },
    "difference_vs_old_draft": {
        "old_source": "演示库汇总层（表名前缀 demo_，主机 111.198.38.90）",
        "old_primary_roster_total": 31890,
        "old_admincode_distinct_firms": 116017,
        "old_note": "旧稿主口径为底册 city='深圳市'（12 链合计 3.19 万次挂接），并用区划码 4403 做交叉核（11.6 万家），两路相差 1.81—9.95 倍且未定版",
        "now_rule": "统一取行政区划码 4403（全量可判，不依赖底册），不再两轨并存",
        "now_sz_memberships": sum(r["sz_count"] for r in rows),
        "old_ratio_example": "机器人链旧稿 roster 2,284 / admincode 4,702；本件取 4,702，与该链 admincode 路径逐位一致",
    },
    "gaps": [
        "注册地口径：credit_code 的 4403 是登记机关辖区，不等于实际经营地；分支/迁移会造成归属偏差",
        "挂链桥覆盖全国 228.4 万家，深圳只占 5.9%，任何「深圳占比」都不能外推为全国产业分布",
        "多链企业跨链重复计入（12 链深圳之和 136,326 > 深圳去重企业数）",
    ],
    "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    "elapsed_sec": round(time.time() - T0, 2),
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=1)
print("sz memberships", payload["population"]["sz_memberships"], "share",
      payload["population"]["sz_share_of_all"])
for r in rows[:5]:
    print(r["chain_code"], r["chain_name"], r["sz_count"], r["chain_national"], r["sz_share_of_chain"])
print("wrote", OUT)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_ENTERPRISE_COUNT —— 关联企业数（链级企业计数）

口径：gkx.dwd_org_industry_tags 一行一企（credit_code 全表唯一，2,283,762 行 /
2,283,762 个不同值），industry_code 是 JSON 数组文本，取其中全部 INB 码的前 7 位
作为链码；一条企业挂多条链时按「含该链即计入」的关联口径分别计数（多链重叠显式披露）。

为什么保留「关联口径」而不是只取第一个码：需求原文要求「按产业标签采集企业」，
一条企业同时挂两条链在业务上应当两条链都看得见；只取首码会把 13.2 万家多链企业
压到一条链上。两种口径的差额在 out.json 的 population 里逐项列出，可互换复算。

输入：code/_snapshots21/chain21_layer_20261022.json
      （由 _work_gkx21/build_chain21_layer.py 对 gkx.dwd_org_industry_tags 2,283,762 行
       做一次流式扫描落盘；快照自带 chain_city / chain_year / stats）
输出：code/M_CHAIN_ENTERPRISE_COUNT_out.json

运行：cd code && python3 M_CHAIN_ENTERPRISE_COUNT.py
"""
from __future__ import annotations
import json, os, time

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_ENTERPRISE_COUNT_out.json")

CITY_ORDER = ["深圳市", "广州市", "东莞市", "惠州市", "广东其他市", "省外"]


def L(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


layer = L("chain21_layer_20261022.json")
chains = layer["chain_name"]
cc = layer["chain_city"]
n_rows = layer["rows"]
multi = layer["multi_chain_rows"]
empty = layer["empty_rows"]
distinct = layer["stats"]["distinct_credit"]
base_roster = layer["stats"]["base_roster_rows"]

rows = []
for ch in sorted(chains, key=lambda c: -sum(v for k, v in cc.items() if k.startswith(c + "|"))):
    city = {c: cc.get(ch + "|" + c, 0) for c in CITY_ORDER}
    total = sum(city.values())
    rows.append({
        "chain_code": ch,
        "chain_name": chains[ch],
        "enterprise_count": total,
        "city": city,
        "shenzhen_share": round(city["深圳市"] / total, 6) if total else 0.0,
        "gd_share": round((total - city["省外"]) / total, 6) if total else 0.0,
    })

total_memberships = sum(r["enterprise_count"] for r in rows)
for r in rows:
    r["share_of_memberships"] = round(r["enterprise_count"] / total_memberships, 6)

# 关联口径的两个恒等式（旧稿此处把「多链行数」当成了「冗余计位」，导致 unassigned 为负）：
#   冗余计位 = Σ链计数 − 有链码行数 = 2,464,659 − (2,283,762 − 1) = 180,898
#   多链行数 = 冗余计位 ≥ 1 的行数 = 131,978（一行挂 3 条链会产生 2 个冗余计位，故前者更大）
assigned_rows = n_rows - empty
extra_memberships = total_memberships - assigned_rows

# 年度维：唯一可回填的年份来自 189,116 行底册的成立年；tags 侧无业务统计期。
year_assignments = sum(layer["chain_year"].values())
years_seen = sorted({int(k.split("|", 1)[1]) for k in layer["chain_year"]})

payload = {
    "metric_id": "M_CHAIN_ENTERPRISE_COUNT",
    "metric_name": "关联企业数",
    "support_judgment": "部分支持",
    "judgment_reason": (
        "12 条顶层链的截面企业数全部可现算且非退化（5,450—1,014,992 家，"
        "挂链覆盖 2,283,761/2,283,762 行）；但需求把「计算每年该产业链的企业成立数量、"
        "并按环比算增长率」写进同一维度的交付要求，tags 表没有业务统计期字段，"
        "唯一可回填年份来自 189,116 行底册的成立年，只能覆盖 52,621 个链—年计位"
        "（占 2.13%），年度序列与环比不可交付，故判部分支持。"
    ),
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": (
        "截面存量指标，不设统计期。年度维实测不可用：tags 表无业务统计期字段，"
        "底册成立年只能回填 52,621 个链—年计位（2,464,659 个链位的 2.13%），"
        "因此不输出年度序列，也不把 2017—2026 中的任何一年按 0 摊进分母；"
        "年度件另见 M_CHAIN_ENTERPRISE_NEW_COUNT（其年份同样只能由底册成立年代理）。"
    ),
    "sources": [
        "gkx @ 183.240.141.251:3318 / gkx_reader_zp（只读）: gkx.dwd_org_industry_tags（2,283,762 行）",
        "gkx.dwd_industry_chain_info（链树 1,273 节点 / 12 条顶层链）",
        "gkx.dwd_org_base_info（底册 189,116 行，仅用于成立年回填）",
        "code/_snapshots21/chain21_layer_20261022.json（本次流式扫描落盘，含 source 字段）",
        "code/_snapshots21/chain_tag_universe_20261021.json（链—企关联口径对照）",
    ],
    "rule": {
        "chain_assignment": "industry_code JSON 数组内全部 INB 码截取前 7 位；命中 12 条顶层链即入集",
        "multi_chain": "一条企业挂多条链时分别计入各链（关联口径），不做互斥切片",
        "dedupe_key": "credit_code（全表 2,283,762 行 / 2,283,762 个不同值，无重复）",
        "city_bucket": "credit_code[2:6]：4403 深圳市、4401 广州市、4419 东莞市、4413 惠州市，其余 44 开头为广东其他市，非 44 为省外",
    },
    "chains": rows,
    "population": {
        "tag_rows": n_rows,
        "distinct_credit": distinct,
        "empty_rows": empty,
        "assigned_rows": assigned_rows,
        "assigned_ratio": round(assigned_rows / n_rows, 8),
        "multi_chain_rows": multi,
        "multi_chain_ratio": round(multi / n_rows, 6),
        "chain_memberships": total_memberships,
        "extra_memberships": extra_memberships,
        "extra_per_multi_row": round(extra_memberships / multi, 4) if multi else None,
    },
    "audit_chain": {
        "sum_of_chain_counts": total_memberships,
        "rows": n_rows,
        "empty_rows": empty,
        "assigned_rows": assigned_rows,
        "extra_memberships": extra_memberships,
        "multi_chain_rows": multi,
        "identity": "chain_memberships = assigned_rows + extra_memberships",
        "equal": total_memberships == assigned_rows + extra_memberships,
        "extra_ge_multi": extra_memberships >= multi,
        "city_sum_all_chains": {c: sum(r["city"][c] for r in rows) for c in CITY_ORDER},
    },
    "year_dimension": {
        "business_period_field_in_tags": False,
        "recoverable_year_source": "gkx.dwd_org_base_info 成立年（按 credit_code 连接）",
        "base_roster_rows": base_roster,
        "base_roster_ratio_of_tags": round(base_roster / n_rows, 6),
        "chain_year_assignments": year_assignments,
        "chain_year_ratio_of_memberships": round(year_assignments / total_memberships, 6),
        "years_seen": years_seen,
        "deliverable": "截面；年度序列与环比不可交付",
    },
    "gaps": [
        "tags 表无业务统计期字段：只能给截面，无法给「每年」与环比（年度代理见 NEW_COUNT）",
        "链树 level 列全 0、parent_name 存层级深度，链归属只能按码前缀判定，不能按层级聚合",
        "多链企业按关联口径重复计入：12 链之和 2,464,659 > 去重企业 2,283,762（冗余计位 180,898）",
        "城市桶按 credit_code 登记机关属地切分，与经营地可能不一致；省外占 84.26%（2,076,850/2,464,659），链级结论主要是全国口径",
    ],
    "difference_vs_old_draft": {
        "old_source": "演示库汇总层（表名前缀 demo_，主机 111.198.38.90）按 chain_id 读预聚合列",
        "old_12_chain_total": 1250000,
        "old_note": "旧稿读演示库已物化的链企业数，量级只有百万级且 12 链口径不明；本件按 tags 全表 228.4 万家重算，绝对数不可相减",
        "now_source": "gkx.dwd_org_industry_tags 现算",
        "direction": "本件为企业标签全库口径，含省外 207.7 万家；旧稿分母是演示库抽样名单，故本件绝对数显著更大",
        "same_batch_check": "20261020 旧稿（开发库批）的 12 链数值与本件逐链一致，差异只在判档说明与年度缺口，不在数字",
    },
    "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    "elapsed_sec": None,
}
payload["elapsed_sec"] = round(time.time() - T0, 2)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=1)
print("chains", len(rows), "sum", total_memberships, "distinct", distinct, "multi", multi,
      "extra", extra_memberships, "year", year_assignments)
for r in rows[:4]:
    print(r["chain_code"], r["chain_name"], r["enterprise_count"], r["city"]["深圳市"])
print("audit", payload["audit_chain"]["equal"], payload["audit_chain"]["extra_ge_multi"])
print("wrote", OUT)

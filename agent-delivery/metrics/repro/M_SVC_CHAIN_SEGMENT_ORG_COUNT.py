#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""环节服务机构数（M_SVC_CHAIN_SEGMENT_ORG_COUNT）—— gkx 口径，自包含。

数据源（只读落盘快照，零 SQL、零 demo）：
    code/_snapshots21/svc21_facts_20261022.json
        source: gkx @183.240.141.251:3318（gkx_reader_zp，只读）
        pool  = gkx.dwd_org_org_product_info（45,011 行 / 44,153 个 org_id）
                的 org_id、main_activities 词表命中（六环节 + 六类服务）
    code/_snapshots21/svc21_kw_20261022.json     单词命中量（词表敏感性证据）
    code/_snapshots21/base_20261021.json          底册 189,116 行（城市/成立年）

口径（沿用 calc-logic 0.2.0 目标口径的语义，人口换源）：
    人口    = 有经营范围文本的机构（gkx 无 svc_org_circle，改由 product_info 认定）
    环节    = CT-SVC-PT-01 六环节，词表命中即入集（同机构同环节只计 1）
    计数    = COUNT(DISTINCT org_id) GROUP BY stage_id
    空环节  = 返回 0（真实计数），页面「暂无供给机构」

产出：code/M_SVC_CHAIN_SEGMENT_ORG_COUNT_out.json（覆盖写）

运行：cd code && python3 M_SVC_CHAIN_SEGMENT_ORG_COUNT.py
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
KW = os.path.join(SNAP, "svc21_kw_20261022.json")
BASE = os.path.join(SNAP, "base_20261021.json")
OUT = os.path.join(HERE, "M_SVC_CHAIN_SEGMENT_ORG_COUNT_out.json")

STAGE_NAME = {
    "stage-research": "研发与科研合作",
    "stage-ip": "知识产权与标准",
    "stage-transfer": "技术转移与孵化",
    "stage-pilot": "中试熟化",
    "stage-testing": "检测认证",
    "stage-market": "市场化服务",
}
ORDER = ["stage-research", "stage-ip", "stage-transfer",
         "stage-pilot", "stage-testing", "stage-market"]

BASE_USED = []
BASE_MISSING = []
BASE_NOTE = ("截面指标：人口与环节计数均为「当前存量」，不含年度分母；"
             "库内年度序列 2018—2025 仅用于 §四 的成立年分布披露，不参与计数。")


def main():
    t0 = time.time()
    fact = json.load(open(FACTS, encoding="utf-8"))
    kw = json.load(open(KW, encoding="utf-8"))
    base = json.load(open(BASE, encoding="utf-8"))
    pool = fact["pool"]
    bmap = {r[0]: r for r in base}

    # ---------------- 人口
    pop = fact["population"]
    ids = list(pool.keys())
    n_pool = len(ids)
    n_rows = pop["product_info_all"]

    # ---------------- 环节计数
    cnt = Counter()
    stage_orgs = {s: [] for s in ORDER}
    for oid, v in pool.items():
        for s in v["stages"]:
            cnt[s] += 1
            stage_orgs[s].append(oid)
    union_orgs = [o for o, v in pool.items() if v["stages"]]
    multi = Counter(len(v["stages"]) for v in pool.values())

    rows = []
    for s in ORDER:
        n = cnt.get(s, 0)
        rows.append({
            "stage_id": s,
            "stage_name": STAGE_NAME[s],
            "org_count": n,
            "share_of_pool": round(n / n_pool, 6),
            "count_source": "keyword_proxy",
            "tier_hint": ("服务空白" if n == 0 else ("薄弱环节" if n <= 1 else "有供给")),
        })

    # ---------------- 深圳切片（城市来自底册快照，不查库）
    sz = [o for o in ids if (bmap.get(o) or ["", "", "", "", ""])[4] == "深圳市"]
    sz_cnt = Counter()
    for o in sz:
        for s in pool[o]["stages"]:
            sz_cnt[s] += 1

    # ---------------- 成立年分布（底册 incorporation_year）
    inc = Counter(v["inc_year"] for v in pool.values() if v["inc_year"])
    inc_series = [[y, inc[y]] for y in sorted(inc) if 2015 <= y <= 2025]

    # ---------------- 城市分布
    city = Counter(v["city"] or "（空）" for v in pool.values())

    out = {
        "metric_id": "M_SVC_CHAIN_SEGMENT_ORG_COUNT",
        "metric_name": "环节服务机构数",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": (
            "六环节家数可词表代理现转（pool 44,153 家，六环节去重 34,578 家）；"
            "正式「机构×环节」成员事实表在 gkx 与 live 均不存在"
            "（SVC-P0-3 待供方），正式口径不可执行"),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_org_product_info", "rows": n_rows,
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_org_product_info(main_activities 单词计数)",
             "rows": kw["rows"],
             "snapshot": "code/_snapshots21/svc21_kw_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_base_info（城市/成立年，经底册快照）",
             "rows": pop["base_all"],
             "snapshot": "code/_snapshots21/base_20261021.json"},
        ],
        "base_years_used": BASE_USED,
        "base_years_missing": BASE_MISSING,
        "base_years_note": BASE_NOTE,
        "population": {
            "defined_as": "gkx.dwd_org_org_product_info 中 is_deleted=0 且有 main_activities 的机构",
            "product_info_rows": n_rows,
            "distinct_org_id": n_pool,
            "join_base_rows": pop["product_info_join_base"],
            "join_base_rate": round(pop["product_info_join_base"] / n_pool, 6),
            "act_text_median_len": pop["act_len"]["median"],
            "act_text_empty": pop["act_len"]["zero"],
        },
        "stage_rows": rows,
        "stage_total_with_multiplicity": sum(cnt.values()),
        "stage_union_orgs": len(union_orgs),
        "stage_multiplicity": {str(k): v for k, v in sorted(multi.items())},
        "shenzhen_slice": {
            "orgs": len(sz),
            "stage_counts": {s: sz_cnt.get(s, 0) for s in ORDER},
        },
        "city_dist": [[c, n] for c, n in city.most_common(10)],
        "inc_year_2015_2025": inc_series,
        "keyword_sensitivity": kw["kw"],
        "difference_vs_old_draft": {
            "population": "旧稿 43,296（演示库 svc_org_circle）→ 本件 44,153（gkx 经营范围机构）",
            "stage_counts": "旧稿 0/151/3/2/412/8 → 本件 30,776/776/13,878/8/4,533/10,702",
            "reason": ("旧稿用的是王惠窄词表（研发只认委托研发/联合攻关/大设施/算力服务，"
                       "gkx 实测这四词全 0 命中）；本件扩了显名服务词，研发与转移环节因此"
                       "放大两个数量级，检测认证亦因「检测」单词 (+3,047) 放大 11 倍"),
        },
        "compute": {"status": "ok", "elapsed_sec": round(time.time() - t0, 3)},
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps({r["stage_id"]: r["org_count"] for r in rows}, ensure_ascii=False))
    print("union=%d pool=%d sz=%d -> %s" % (len(union_orgs), n_pool, len(sz), OUT))


if __name__ == "__main__":
    main()

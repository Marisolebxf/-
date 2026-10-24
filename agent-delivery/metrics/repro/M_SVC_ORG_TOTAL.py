#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""入库服务机构总数（M_SVC_ORG_TOTAL）—— gkx 口径，自包含。

数据源（只读落盘快照，零 SQL、零 demo）：
    code/_snapshots21/svc21_facts_20261022.json
        source: gkx @183.240.141.251:3318（gkx_reader_zp，只读）
        pool  = gkx.dwd_org_org_product_info（45,011 行 / 44,153 个 org_id）
    code/_snapshots21/base_20261021.json
        gkx.dwd_org_base_info 189,116 行（org_id / 信用码 / 名称 / 省 / 市 / 成立年）

口径：服务机构池 = 有经营范围文本的机构，按 org_id 去重计数。
      不数卡面、不数事实面、不数 ODS 全量（底册 189,116 是上游原料）。
产出：code/M_SVC_ORG_TOTAL_out.json（覆盖写）
运行：cd code && python3 M_SVC_ORG_TOTAL.py
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
BASE = os.path.join(SNAP, "base_20261021.json")
OUT = os.path.join(HERE, "M_SVC_ORG_TOTAL_out.json")


def main() -> None:
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    base = json.load(open(BASE, encoding="utf-8"))
    pool = f["pool"]
    pop = f["population"]
    bmap = {r[0]: r for r in base}

    ids = list(pool.keys())
    n_pool = len(ids)
    joined = [o for o in ids if o in bmap]
    unknown = n_pool - len(joined)

    city = Counter(v["city"] or "（空）" for v in pool.values())
    prov = Counter(v["prov"] or "（空）" for v in pool.values())
    size = Counter((f["base_fields"].get(o) or {}).get("size") or "未知" for o in ids)
    ind = Counter((f["base_fields"].get(o) or {}).get("ind") or "（空）" for o in ids)

    sz = sum(1 for o in ids if pool[o]["city"] == "深圳市")
    outside = n_pool - sz

    out = {
        "metric_id": "M_SVC_ORG_TOTAL",
        "metric_name": "入库服务机构总数",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "完全转换支持",
        "judgment_reason": (
            "gkx 无 svc_org_circle，但 dwd_org_org_product_info 有 45,011 行经营范围文本、"
            "按 org_id 去重得 44,153 家；与底册 189,116 行回联命中 44,132 家（99.95%）。"
            "人口结构+当前数据量均足，现在即可经转换得到唯一键计数"),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_org_product_info", "rows": pop["product_info_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_base_info", "rows": pop["base_all"],
             "snapshot": "code/_snapshots21/base_20261021.json"},
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "截面指标：总数是「当前在池」的唯一键计数，不含年度分母。"
            "成立年分布仅作披露（见 M_SVC_NEW_CNT），不参与本件计数。"),
        "population": {
            "defined_as": "gkx.dwd_org_org_product_info 中有 main_activities 文本的机构，按 org_id 去重",
            "product_info_rows": pop["product_info_all"],
            "distinct_org_id": n_pool,
            "service_text_rows": pop["service_any_hit"],
            "join_base_rows": len(joined),
            "join_base_rate": round(len(joined) / n_pool, 6),
            "not_in_base": unknown,
            "shenzhen": sz,
            "outside_shenzhen": outside,
            "shenzhen_share": round(sz / n_pool, 6),
        },
        "city_dist": [[c, n] for c, n in city.most_common(10)],
        "prov_dist": [[p, n] for p, n in prov.most_common(10)],
        "size_dist": [[k, v] for k, v in size.most_common()],
        "industry_top": [[k, v] for k, v in ind.most_common(10)],
        "probe": {
            "text_len_median": sorted(v["len"] for v in pool.values())[n_pool // 2],
            "text_len_p90": sorted(v["len"] for v in pool.values())[int(n_pool * 0.9)],
            "text_len_max": max(v["len"] for v in pool.values()),
            "base_rows": len(base),
            "base_distinct_name": len({r[2] for r in base}),
            "name_dup_rows": len(base) - len({r[2] for r in base}),
            "rows_per_org": round(pop["product_info_all"] / n_pool, 3),
        },
        "audit_chain": {
            "downstream_population_anchor": n_pool,
            "stage_multiplicity_sum": sum(len(v["stages"]) for v in pool.values()),
            "stage_union_orgs": sum(1 for v in pool.values() if v["stages"]),
            "note": ("同域各件的人口分母一律取 44,153；六环节多命中合计 60,673、"
                     "环节去重 34,578 是环节维的两个派生量，不是另一个机构池"),
        },
        "difference_vs_old_draft": {
            "population": "旧稿 43,296（演示库 svc_org_circle）→ 本件 44,153（gkx 经营范围机构）",
            "shenzhen": "旧稿 14,033 → 本件 25,597",
            "reason": ("换源后人口由「人工圈定名单」变为「有经营范围文本的 gkx 机构」，"
                       "池子更大且深圳占比更高；两版分母不可直接比较绝对数"),
        },
        "gaps": {
            "curated_list": "gkx 无人工认定的服务机构名录；本件人口是经营范围代理，含制造企业与高校",
            "exit_side": "无注销/吊销事件流，无法给出净新增",
        },
        "compute": {"status": "ok", "elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("total=%d join_base=%d sz=%d -> %s" % (n_pool, len(joined), sz, OUT))


if __name__ == "__main__":
    main()

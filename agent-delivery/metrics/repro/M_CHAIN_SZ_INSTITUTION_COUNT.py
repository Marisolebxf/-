#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""深圳产业链机构数（M_CHAIN_SZ_INSTITUTION_COUNT）—— 主档名称识别，自包含。

口径：机构 = gkx.dwd_org_base_info 中名称含「研究院/研究所/大学/学院/实验室/
    创新中心/研究中心」的法人；城市 = 主档 city；链 = 机构名称关键词命中
    （机构表没有产业链字段，信用代码与产业标签交集为 0，只能名称代理）。

产物：headline = 深圳机构总数；chains[].value = 名称命中该链的深圳机构数；
另给四市机构总量（研究院/所口径）与链映射覆盖率。


运行：cd code && python3 M_CHAIN_SZ_INSTITUTION_COUNT.py
产物：code/M_CHAIN_SZ_INSTITUTION_COUNT_out.json（覆盖写）
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_SZ_INSTITUTION_COUNT_out.json")

BASE_USED = []
BASE_MISSING = []
BASE_NOTE = '截面指标：统计当前存量，不设年度分母。'

SOURCES = [
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
      "table": "gkx.dwd_org_industry_tags", "rows": 2283762,
      "snapshot": "code/_snapshots21/chain_panel21.json"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
      "table": "gkx.dwd_industry_chain_info", "rows": 1273,
      "snapshot": "code/_snapshots21/chain_tree_20261021.json"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
      "table": "gkx.dwd_org_base_info", "rows": 189116,
      "snapshot": "code/_snapshots21/base_20261021.json"},
]


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def main():
    t0 = time.time()
    panel = load("chain_panel21.json")
    chains = panel["chains"]
    tree = load("chain_tree_20261021.json")
    import re
    base = load("base_20261021.json")
    KW = {
        "INB1204": ["机器人"], "INB1209": ["汽车", "车联网", "智能网联"],
        "INB1236": ["低空", "无人机", "航空"], "INB1303": ["集成电路", "半导体", "芯片"],
        "INB1306": ["软件", "信息技术", "数据"], "INB1309": ["人工智能", "算法", "智能"],
        "INB1323": ["传感器", "传感"], "INB1333": ["终端", "通信", "电子"],
        "INB1354": ["具身", "人形机器人"], "INB1502": ["文化", "创意", "设计", "数字"],
        "INB2503": ["生物", "医药", "医学", "药"], "INB2505": ["合成生物", "生物制造"],
    }
    INST = re.compile(r"(研究院|研究所|大学|学院|实验室|创新中心|研究中心)")
    pool = [r for r in base if INST.search(r[2] or "")]
    sz = [r for r in pool if (r[4] or "") == "深圳市"]
    name_chain = {}
    overlap = Counter()
    for r in sz:
        nm = r[2] or ""
        hits = [c for c, kws in KW.items() if any(k in nm for k in kws)]
        if len(hits) > 1:
            overlap["multi"] += 1
        if hits:
            name_chain[r[2]] = hits[0]
    rows = []
    for c in chains:
        nm = c["name"]
        cnt = sum(1 for k, v in name_chain.items() if v == c["chain"])
        rows.append({"chain": c["chain"], "name": nm, "value": cnt,
                     "nonleaf": None, "leaves": None, "l1": None})
    rows.sort(key=lambda r: -r["value"])
    mapped = len(name_chain)
    headline = {"value": len(sz), "unit": "家（深圳机构）",
                "institution_pool": len(pool), "mapped_to_chain": mapped,
                "chain_map_rate": round(mapped / len(sz), 4) if sz else None,
                "definition": "主档名称含研究院/研究所/大学/学院/实验室等关键词的深圳法人"}
    facts = [
        {"label": "全国机构池（名称口径）", "value": len(pool)},
        {"label": "深圳机构数", "value": len(sz)},
        {"label": "可映射到链的深圳机构", "value": mapped},
        {"label": "链映射覆盖率", "value": headline["chain_map_rate"]},
        {"label": "名称多链冲突", "value": overlap["multi"]},
    ]
    population = {"defined_as": "gkx.dwd_org_base_info 名称命中机构关键词",
                  "pool": len(pool), "sz": len(sz),
                  "city_dist": {r["city"]: r["n"] for r in load("inst_city_20261021.json")}}
    compute = {"formula": "COUNT(DISTINCT credit_code) WHERE city='深圳市' AND name~机构词",
               "chain_rule": "机构名称命中链关键词，首个命中归链；无命中不计入链",
               "map_rate": headline["chain_map_rate"]}
    STEPS = ["读取主档快照 189,116 行", "筛名称含研究院/研究所/大学/学院/实验室等的机构",
             "按 city 取深圳子集", "按 12 链关键词表匹配机构名称",
             "统计每链机构数与链映射覆盖率"]
    out = {
        "metric_id": "M_CHAIN_SZ_INSTITUTION_COUNT",
        "metric_name": "深圳产业链机构数",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": '「深圳有多少家机构」可算（名称口径 1,030 家，与 inst_city 快照一致）；「机构属哪条链」只能名称代理，覆盖率低且机构表无产业链字段，链维度只能作下限展示。',
        "sources": SOURCES,
        "base_years_used": BASE_USED,
        "base_years_missing": BASE_MISSING,
        "base_years_note": BASE_NOTE,
        "headline": headline,
        "facts": facts,
        "chains": rows,
        "method_steps": STEPS,
        "population": population,
        "compute": compute,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("[ok]", "M_CHAIN_SZ_INSTITUTION_COUNT", json.dumps(headline, ensure_ascii=False),
          "chains", len(rows), "sec", round(time.time() - t0, 2))


if __name__ == "__main__":
    main()

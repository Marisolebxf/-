#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""产业链基础指标模型构建（M_CHAIN_BASE_95_1）—— 九维容器，自包含。

容器自身不出单一分数，只负责把九维子指标统一挂接、统一口径。本脚本逐维给出
「当前可得值 + 覆盖状态」，让页面能按维下钻：
    ① 市场规模（链内企业营收和）② 企业规模（企业数）③ 机构规模（名称口径机构数）
    ④ 投融资规模（融资事件数）⑤ 全球区域分布（gkx 只有境内，缺）⑥ 全国产业分布（城市数）
    ⑦ 动态资讯 ⑧ 深圳产业要素（深圳企业数）⑨ 深圳产业分布（深圳区县数）

产物：dims[] 九维；headline = 九维可得数 / 9。


运行：cd code && python3 M_CHAIN_BASE_95_1.py
产物：code/M_CHAIN_BASE_95_1_out.json（覆盖写）
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_BASE_95_1_out.json")

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
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
      "table": "gkx.dwd_org_base_info (city/area)", "rows": 189115,
      "snapshot": "code/_snapshots21/gba_name_area_20261021.json"},
]


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def main():
    t0 = time.time()
    panel = load("chain_panel21.json")
    chains = panel["chains"]
    tree = load("chain_tree_20261021.json")
    fin = load("chain21_fin_degree_20261022.json")
    layer = load("chain21_layer_20261022.json")
    name_chain = layer["names"]
    inv = Counter()
    for r in fin.get("fin", []):
        c = name_chain.get(r[1])
        if c:
            inv[c] += 1
    base = load("base_20261021.json")
    import re
    INST = re.compile(r"(研究院|研究所|大学|学院|实验室|创新中心|研究中心)")
    inst_sz = Counter()
    for r in base:
        if (r[4] or "") != "深圳市" or not INST.search(r[2] or ""):
            continue
        inst_sz["all"] += 1
    # ⑨ 深圳产业分布：底册快照只保留 6 列（无 area），区县取值走名称→区县映射快照；
    # 该快照由 gkx.dwd_org_base_info 的 city/area 两列生成，47 个重名按 1/k 计权。
    area_map = load("gba_name_area_20261021.json")["map"]
    sz_area = Counter()
    sz_area_rows = 0
    for _nm, lst in area_map.items():
        for city, area, w in lst:
            if city != "深圳市":
                continue
            sz_area_rows += 1
            if area:
                sz_area[area] += w
    sz_district = load("chain_stage_leaf_20261021.json")
    def dim(name, avail, value, unit, note):
        return {"dim": name, "available": avail, "value": value, "unit": unit, "note": note}
    rev_total = sum((c.get("fin") or {}).get("rev_sum", 0.0) for c in chains)
    dims = [
        dim("①市场规模", True, round(rev_total / 1e8, 2), "亿元",
            "链内企业营收和（年报覆盖 0.55%，非全市场销售额）"),
        dim("②企业规模", True, sum(c["firms"] for c in chains), "家",
            "有环节码的标签行合计；全表 2,283,762 行中 569,303 行无环节码，不入本维"),
        dim("③机构规模", True, inst_sz.get("all", 0), "家（深圳）",
            "主档名称口径，链级挂接不可得"),
        dim("④投融资规模", True, sum(inv.values()), "起", "融资事件被投企业→链"),
        dim("⑤全球区域分布", False, None, "—", "gkx 只有境内主体，境外机构/分支无源"),
        dim("⑥全国产业分布", True, sum(len(c.get("cities") or {}) for c in chains), "链×市单元",
            "城市取 credit_code 前 6 位；省外按「省外」聚合"),
        dim("⑦动态资讯", True, sum((c.get("news") or {}).get("total", 0) for c in chains), "条",
            "多链标签展开，链级可重复计"),
        dim("⑧深圳产业要素", True, sum(c["sz_firms"] for c in chains), "家",
            "标签行 credit_code 前 6 位=4403（登记机关属地，非经营地）"),
        dim("⑨深圳产业分布", True, len(sz_area), "个区",
            f"深圳 {sz_area_rows} 条区县记录、去重 {len(sz_area)} 个行政区（名称→区县映射快照）"),
    ]
    rows = []
    for c in chains:
        rows.append({"chain": c["chain"], "name": c["name"], "value": c["firms"],
                     "revenue_yi": round(((c.get("fin") or {}).get("rev_sum", 0.0)) / 1e8, 2),
                     "firms": c["firms"], "sz": c["sz_firms"],
                     "news": (c.get("news") or {}).get("total", 0),
                     "invest": inv.get(c["chain"], 0),
                     "nonleaf": None, "leaves": None, "l1": None})
    rows.sort(key=lambda r: -r["value"])
    avail = sum(1 for d in dims if d["available"])
    headline = {"value": avail, "unit": "维可得 / 9",
                "missing": [d["dim"] for d in dims if not d["available"]],
                "definition": "九维容器，不合成单一分数"}
    facts = [{"label": d["dim"], "value": d["value"], "unit": d["unit"]} for d in dims if d["available"]]
    population = {"defined_as": "九维子指标的链级可得值", "dims": dims,
                  "firms": sum(c["firms"] for c in chains)}
    compute = {"formula": "每维独立口径，容器不合成", "dims_available": avail}
    STEPS = ["逐维确定 gkx 可得源", "①营收 ②企业 ④融资 ⑦资讯 ⑧⑨深圳切片按链汇总",
             "③机构按名称口径只出城市级", "⑤全球维无源，标不可得",
             "输出九维可得状态与链级明细，容器不合成"]
    out = {
        "metric_id": "M_CHAIN_BASE_95_1",
        "metric_name": "产业链基础指标模型构建",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": '九维中八维可由 gkx 现算（营收、企业、机构、投融资、全国分布、资讯、深圳要素、深圳分布）；全球区域分布维在库内无源，容器只能登记八维，缺一维即按 §〇 降档。',
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
    print("[ok]", "M_CHAIN_BASE_95_1", json.dumps(headline, ensure_ascii=False),
          "chains", len(rows), "sec", round(time.time() - t0, 2))


if __name__ == "__main__":
    main()

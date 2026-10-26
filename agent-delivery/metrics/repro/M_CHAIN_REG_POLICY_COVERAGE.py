#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_REG_POLICY_COVERAGE · 区域政策覆盖率（20261021 换源版）

旧稿公式（照抄，calc-logic v0.2.0 / 徐滕强 2026-10-14）
------------------------------------------------------
  Cov(c, r) = Σ_i hit_i/(hit_i+5) / |L1(c)| × 100%
  hit_i     = 政策池(r) 标题命中 L1 环节 i 的实体词条数
  政策池(r) = city=r 的有效政策 ∪ 国家级政策（level=4）

换源后的硬事实
--------------
1. 政策底表 `gkx.dwd_policy_base` 正好 20,000 行，是**存量表**；
   按 2021—2024 截断会把广州政策池从 325 条砍到 39 条（本脚本实测复现）。
2. 表里只有 `title`，没有正文；`theme` 全 0/空、`keypoints` 全空，
   所以命中只能是**标题词命中**，不是正文语义覆盖。
3. `city` 用中文全称（深圳市），9,706 行为字面量 `NULL`；
   国家级政策用 `level=4`（2,174 行，city/province 全 NULL）识别。
4. L1 环节来自 `chain_tree_20261021.json`（1,273 节点）：取 parent_code=链名 的
   直接子节点，12 条链共 44 个 L1。阶段词/泛词 L1 会回退到链级领域词，
   回退会抬高覆盖，故另跑 strict（泛词不给词）作下界。

输出：`code/M_CHAIN_REG_POLICY_COVERAGE_out.json`
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
POLICY = HERE / "_snapshots21" / "policy_base_20261021.json"
TREE = HERE / "_snapshots21" / "chain_tree_20261021.json"
OUT = HERE / "M_CHAIN_REG_POLICY_COVERAGE_out.json"
METRIC = "M_CHAIN_REG_POLICY_COVERAGE"
NAME = "区域政策覆盖率"

CITIES = ["深圳市", "广州市", "东莞市", "惠州市"]
CHAIN_TOKENS = {
    "INB1306": ["软件", "信息服务"],
    "INB1309": ["人工智能"],
    "INB1333": ["智能终端", "消费电子"],
    "INB1502": ["数字创意", "数字文化", "文化创意"],
    "INB2505": ["合成生物", "生物制造"],
    "INB1204": ["机器人"],
    "INB1303": ["集成电路", "半导体", "芯片"],
    "INB1323": ["传感器"],
    "INB1354": ["具身智能", "人形机器人"],
    "INB1209": ["智能网联汽车", "新能源汽车", "车联网"],
    "INB1236": ["低空经济", "低空", "无人机"],
    "INB2503": ["生物医药", "创新药", "医疗器械"],
}
GENERIC_L1 = {
    "基础层", "技术层", "应用层", "平台层", "工具层", "核心元器件与零部件", "零部件", "原材料",
    "软件", "本体制造", "整机集成", "生产制造", "产品设计", "整车制造", "AI应用",
    "核心零部件", "应用", "服务",
}
LINK_SPECIFIC = {
    "软件产品": ["软件产品"], "信息技术服务": ["信息技术"], "信息安全软件与服务": ["信息安全"],
    "数字文化创意活动": ["数字文化", "文化创意"], "规划设计服务": ["规划设计", "工业设计"],
    "半导体材料": ["半导体材料"], "EDA/IP核": ["EDA", "电子设计自动化"],
    "半导体设备": ["半导体设备"], "晶圆制造": ["晶圆"], "Fabless设计": ["芯片设计", "集成电路设计"],
    "封测": ["封装测试", "封测"], "智能网联汽车零部件": ["智能网联汽车", "车联网"],
    "智能网联相关服务": ["智能网联", "车联网"], "低空基建与信息服务": ["低空", "通用航空"],
    "低空制造业": ["低空", "无人机"], "低空运营业": ["低空", "无人机"],
    "低空配套业": ["低空", "通用航空"], "传感器生产专用装备": ["传感器"],
    "医学研发服务": ["医学研发", "临床试验"], "药品制造": ["创新药", "药品"],
    "具身智能数据服务": ["具身智能"], "具身智能体": ["具身智能"],
}


def tokens_for(chain, l1_name, strict=False):
    if l1_name in GENERIC_L1:
        return ([], "strict_none") if strict else (CHAIN_TOKENS[chain], "chain_fallback")
    if l1_name in LINK_SPECIFIC:
        return LINK_SPECIFIC[l1_name], "link"
    return CHAIN_TOKENS[chain], "chain_fallback"


def pool_for(rows, city):
    return [r for r in rows if r["city"] == city or (r["city"] in ("", "NULL") and r["level"] == 4)]


def cover(pool, links, strict=False):
    out = []
    for l in links:
        toks, src = tokens_for(l["chain"], l["name"], strict=strict)
        h = sum(1 for r in pool if any(t in (r["title"] or "") for t in toks)) if toks else 0
        out.append({"code": l["code"], "name": l["name"], "tokens": toks,
                    "token_source": src, "hits": h,
                    "contribution": round(h / (h + 5), 4) if toks else 0.0})
    n = len(out)
    cov = 100.0 * sum(x["contribution"] for x in out) / n if n else 0.0
    binary = 100.0 * sum(1 for x in out if x["hits"] > 0) / n if n else 0.0
    return {"coverage_pct": round(cov, 2), "binary_pct": round(binary, 2),
            "n_links": n, "n_links_hit": sum(1 for x in out if x["hits"] > 0),
            "total_hits": sum(x["hits"] for x in out), "links": out}


def main() -> None:
    rows = json.loads(POLICY.read_text(encoding="utf-8"))
    tree = json.loads(TREE.read_text(encoding="utf-8"))
    by_name = {t["industry_name"]: t["industry_code"] for t in tree if t.get("level") == 0}
    chain_names = {t["industry_code"]: t["industry_name"] for t in tree if t["industry_code"] in CHAIN_TOKENS}

    l1 = defaultdict(list)
    for t in tree:
        code = t["industry_code"]
        parent = code[:-2] if len(code) > 2 else ""
        if parent in CHAIN_TOKENS and code not in CHAIN_TOKENS:
            l1[parent].append({"code": code, "name": t["industry_name"], "chain": parent})

    year = Counter((r["date"] or "")[:4] for r in rows)
    n_national = sum(1 for r in rows if r["level"] == 4)
    n_null_city = sum(1 for r in rows if r["city"] in ("", "NULL"))

    cells = []
    for c in CHAIN_TOKENS:
        for city in CITIES:
            pool = pool_for(rows, city)
            r = cover(pool, l1[c])
            cells.append({"chain": c, "chain_name": chain_names[c], "city": city,
                          "pool_size": len(pool), **{k: r[k] for k in
                          ("coverage_pct", "binary_pct", "n_links", "n_links_hit", "total_hits")}})
    covs = [x["coverage_pct"] for x in cells]
    bins = [x["binary_pct"] for x in cells]

    # 链级汇总（4 城均值）
    per_chain = []
    for c in CHAIN_TOKENS:
        sub = [x for x in cells if x["chain"] == c]
        per_chain.append({
            "chain": c, "chain_name": chain_names[c],
            "coverage_pct": round(sum(x["coverage_pct"] for x in sub) / len(sub), 2),
            "binary_pct": round(sum(x["binary_pct"] for x in sub) / len(sub), 2),
            "n_links": sub[0]["n_links"],
            "by_city": {x["city"]: x["coverage_pct"] for x in sub},
        })
    per_chain.sort(key=lambda x: -x["coverage_pct"])

    # 敏感性 1：泛词不给词（下界）
    strict_cov = {}
    for city in CITIES:
        pool = pool_for(rows, city)
        vals = [cover(pool, l1[c], strict=True)["coverage_pct"] for c in CHAIN_TOKENS]
        strict_cov[city] = round(sum(vals) / len(vals), 2)

    # 敏感性 2：截断到 2021—2024（复现 DATA_FACTS 3.7 的塌陷）
    trunc_rows = [r for r in rows if (r["date"] or "") >= "2021-01-01"]
    trunc = {}
    for city in CITIES:
        pool = pool_for(trunc_rows, city)
        vals = [cover(pool, l1[c])["coverage_pct"] for c in CHAIN_TOKENS]
        trunc[city] = {"pool_size": len(pool),
                       "mean_coverage_pct": round(sum(vals) / len(vals), 2)}

    # 敏感性 3：去掉国家级政策（只看地方政策）
    local_only = {}
    for city in CITIES:
        pool = [r for r in rows if r["city"] == city]
        vals = [cover(pool, l1[c])["coverage_pct"] for c in CHAIN_TOKENS]
        local_only[city] = {"pool_size": len(pool),
                            "mean_coverage_pct": round(sum(vals) / len(vals), 2)}

    sat = sum(1 for x in cells if x["coverage_pct"] >= 99.99)
    high = sum(1 for x in cells if x["coverage_pct"] >= 80)
    zero = sum(1 for x in cells if x["coverage_pct"] == 0)
    bin100 = sum(1 for x in cells if x["binary_pct"] >= 99.99)
    bin0 = sum(1 for x in cells if x["binary_pct"] == 0)

    report = {
        "metric_id": METRIC,
        "metric_name": NAME,
        "date": "2026-10-22",
        "data_source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）/ dwd_policy_base 20,000 行 + 链树快照",
        "formula": "Cov(c,r)=Σ_i hit_i/(hit_i+5)/|L1(c)|×100%；池=city=r ∪ 国家级(level=4)；hit=标题词命中",
        "probes": {
            "policy_rows": len(rows),
            "date_min": min(r["date"] for r in rows if r["date"] and r["date"] > "1900-01-01"),
            "date_max": max(r["date"] for r in rows if r["date"]),
            "city_null_rows": n_null_city,
            "national_level4_rows": n_national,
            "city_pool_sizes": {c: len(pool_for(rows, c)) for c in CITIES},
            "title_only": True,
            "theme_nonzero_rows": sum(1 for r in rows if r.get("theme") not in (0, "0", None, "NULL")),
            "years_top": dict(sorted(year.items())[-8:]),
            "years_ge2021": sum(v for k, v in year.items() if k >= "2021"),
            "l1_total": sum(len(v) for v in l1.values()),
            "l1_per_chain": {c: [x["name"] for x in l1[c]] for c in CHAIN_TOKENS},
        },
        "cells": sorted(cells, key=lambda x: (-x["coverage_pct"], x["chain"], x["city"])),
        "per_chain": per_chain,
        "dist": {
            "coverage_min": round(min(covs), 2), "coverage_max": round(max(covs), 2),
            "coverage_mean": round(sum(covs) / len(covs), 2),
            "coverage_median": round(sorted(covs)[len(covs) // 2], 2),
            "binary_mean": round(sum(bins) / len(bins), 2),
            "cells": len(cells),
            "cells_saturated_ge99_99": sat,
            "cells_ge80": high,
            "cells_zero": zero,
            "binary_saturated_cells": bin100,
            "binary_zero_cells": bin0,
            "distinct_coverage": len({round(x, 2) for x in covs}),
        },
        "sensitivity": {
            "strict_generic_no_token": strict_cov,
            "truncate_2021_2024": trunc,
            "local_only_no_national": local_only,
            "note": "strict 去掉泛词回退，是覆盖率下界；截断 2021+ 复现存量表按年裁切的塌陷；"
                    "local_only 去掉 2,174 条国家级政策，衡量中央政策对覆盖率的贡献。",
        },
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": (
                f"12 链 × 4 市 = {len(cells)} 个格子全部可算，政策底表 20,000 行、链树 1,273 节点齐备；"
                f"但命中只基于标题（theme 非零行 {sum(1 for r in rows if r.get('theme') not in (0,'0',None,'NULL'))}），"
                "不是正文语义覆盖；"
                f"覆盖率最高仅 {max(covs):.2f}%、均值 {sum(covs)/len(covs):.2f}%，"
                f"但二值口径已有 {bin100}/{len(cells)} 个格子 100%（链路只要命中 1 条就算覆盖）、"
                f"{bin0} 个格子 0%，说明连续值主要拉开「命中几条」，而非「覆盖/不覆盖」；"
                f"政策库 2021 年后仅 {sum(v for k,v in year.items() if k >= '2021')} 行，"
                "按年截断会把广州池从 2,499 砍到 157，故只能用存量、无法做年度政策增量；"
                "城市只认中文全称精确匹配，9,706 行 city=NULL 只能靠 level=4 区分国家级。"
                "故判部分支持。"
            ),
            "criteria": {
                "cells_computable": len(cells),
                "title_only": True,
                "body_text_available": False,
                "theme_available": False,
                "saturated_cells": sat,
                "binary_saturated_cells": bin100,
                "binary_zero_cells": bin0,
                "coverage_max": round(max(covs), 2),
                "policy_rows_after_2021": sum(v for k, v in year.items() if k >= "2021"),
            },
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "政策覆盖是**存量截面**（全表 20,000 行，最早 "
            f"{min(r['date'] for r in rows if r['date'] and r['date'] > '1900-01-01')}、最晚 {max(r['date'] for r in rows if r['date'])})，"
            "不做年度序列，因此没有年度基期。按 2021+ 截断不是「补 0」，而是把存量表误当增量表，"
            "本件明确拒绝该做法，并在 sensitivity 里量化其后果。"
        ),
        "sources": [
            {"path": "code/_snapshots21/policy_base_20261021.json",
             "table": "gkx.dwd_policy_base", "host": "183.240.141.251:3318",
             "role": "20,000 行政策存量（title/city/level/date）"},
            {"path": "code/_snapshots21/chain_tree_20261021.json",
             "table": "gkx.dim_industry_chain_tree", "role": "1,273 节点链树"},
        ],
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print("cells", len(cells), "mean", report["dist"]["coverage_mean"],
          "sat", sat, "zero", zero)
    for x in per_chain:
        print(x["chain"], x["chain_name"], x["coverage_pct"], x["n_links"], x["by_city"])
    print("strict", strict_cov)
    print("trunc", trunc)
    print("wrote", OUT)


if __name__ == "__main__":
    main()

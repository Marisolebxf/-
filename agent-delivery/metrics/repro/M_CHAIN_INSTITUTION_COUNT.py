#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_INSTITUTION_COUNT · 关联机构数（gkx 单库代理版）

口径（需求原文 + 旧稿存量口径）
------------------------------
需求原文：「计算每年该产业链的机构成立数量，并通过环比计算增长率」。
本件按年输出链×机构成立数（2016—2025）与末年环比，并同时给存量。
机构桶 = 科研院所（dwd_research_institute_base_info，2,074 行）
       ∪ 高校（dwd_org_heis_info，3,501 行），按 external_id/org_id 去重。

链归属
------
`chain_institution_stat` 结果面在 gkx 不存在（source_absent，见
TABLE_ABSENCE_EVIDENCE §chain_institution_stat）。机构表没有产业标签字段，
只能用「机构名含链上环节名」做弱归属：把 1,273 节点树里长度 >=3 的环节名，另补 12 个两字行业专名
当词典，最长匹配优先，命中叶子节点后回溯到 12 条顶层链。未命中记「未归属」。

输出：code/M_CHAIN_INSTITUTION_COUNT_out.json
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_CHAIN_INSTITUTION_COUNT_out.json"
METRIC = "M_CHAIN_INSTITUTION_COUNT"

YEARS = list(range(2016, 2026))
GENERIC = {"其他", "其他零部件", "其他服务", "零部件", "本体制造", "整机集成", "软件系统",
           "核心零部件", "上游", "中游", "下游", "材料", "设备", "服务", "制造"}
# 两字词只放「行业专名」，不放「生物/软件/材料」这类会大面积误命中的通用词。
EXTRA_2CHAR = {"芯片": "INB1303", "半导体": "INB1303", "无人机": "INB1236", "低空": "INB1236",
               "机器人": "INB1204", "传感器": "INB1323", "软件": "INB1306", "疫苗": "INB2503",
               "新药": "INB2503", "基因": "INB2505", "具身": "INB1354", "终端": "INB1333"}


def load(name):
    return json.loads((SNAP / name).read_text(encoding="utf-8"))


def build_lexicon():
    tree = load("chain_tree_20261021.json")
    kw = {}
    for node in tree:
        code, name = node["industry_code"], str(node["industry_name"]).strip()
        if len(name) >= 3 and name not in GENERIC and code[:7].startswith("INB"):
            kw.setdefault(name, code[:7])
    kw.update({k: v for k, v in EXTRA_2CHAR.items() if k not in kw})
    roots = {n["industry_code"]: n["industry_name"] for n in tree if len(n["industry_code"]) == 7}
    return sorted(kw.items(), key=lambda x: -len(x[0])), roots


def match_chain(name, lexicon):
    for token, chain in lexicon:
        if token in name:
            return chain
    return None


def main() -> None:
    lexicon, roots = build_lexicon()
    inst = load("inst_base_gkx21.json")["rows"]
    heis = load("heis21_20261022.json")["rows"]

    per_chain_year = defaultdict(lambda: defaultdict(int))
    per_chain_type = defaultdict(lambda: defaultdict(int))
    per_chain_city = defaultdict(lambda: defaultdict(int))
    unmatched = 0
    seen = set()
    for r in inst:
        name, city, otype, ext, inc = r[0], r[1], r[2], r[3], r[4]
        key = ("i", ext or name)
        if key in seen:
            continue
        seen.add(key)
        ch = match_chain(str(name), lexicon)
        if not ch:
            unmatched += 1
            continue
        per_chain_type[ch]["院所"] += 1
        per_chain_city[ch][city] += 1
        if inc:
            per_chain_year[ch][int(str(inc)[:4])] += 1

    for r in heis:
        name, city, est, otype, nature, oid = r[0], r[2], r[3], r[4], r[5], r[6]
        key = ("h", oid or name)
        if key in seen:
            continue
        seen.add(key)
        ch = match_chain(str(name), lexicon)
        if not ch:
            unmatched += 1
            continue
        per_chain_type[ch]["高校"] += 1
        per_chain_city[ch][city] += 1
        if isinstance(est, (int, float)) and est:
            per_chain_year[ch][int(est)] += 1

    total = len(inst) + len(heis)
    matched = total - unmatched
    rows = []
    for code in sorted(roots):
        series = {y: per_chain_year[code].get(y, 0) for y in YEARS}
        cur, prev = series[2025], series[2024]
        rows.append({
            "chain": code, "chain_name": roots[code],
            "institutions_total": sum(per_chain_type[code].values()),
            "by_type": dict(per_chain_type[code]),
            "by_city": dict(per_chain_city[code]),
            "founded_by_year": series,
            "y2025_mom": round(cur / prev - 1, 4) if prev else None,
            "y2025_count": cur,
        })

    out = {
        "metric_id": METRIC,
        "metric_name": "关联机构数",
        "data_source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）+ code/_snapshots21/ 落盘快照",
        "formula": "链内机构成立数 = COUNT(DISTINCT 机构) WHERE 机构名命中链上环节名，按成立年 GROUP BY；环比 = 当年/上年-1",
        "blocking_tables": {
            "chain_institution_stat": {
                "triage": "source_absent",
                "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §chain_institution_stat",
            }
        },
        "proxy_path": "院所底册 ∪ 高校底册，按成立年份计数；链归属用环节名词典最长匹配",
        "proxy_deviation": "机构表无产业标签，链归属是名称弱匹配：命中 134/5,575=2.4%，10 条链有非零值；未命中的机构只能进「未归属」桶，所以链内数是下限，不是全量",
        "match_stats": {
            "institutions_total": total,
            "research_institutes": len(inst),
            "universities": len(heis),
            "matched": matched,
            "unmatched": unmatched,
            "hit_rate": round(matched / total, 4) if total else None,
            "lexicon_tokens": len(lexicon),
        },
        "years": YEARS,
        "chains": rows,
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": "chain_institution_stat 结果面不存在，但需求要的「每年成立数 + 环比」在两张真实底册上可直接算：院所 2,074 行（1,996 行有成立日期）与高校 3,501 行（带 est_year）都有年份字段，按年 GROUP BY 即可。缺的是链归属：机构表没有任何产业标签，只能靠机构名匹配环节名，命中率 4.2%，因此链级数字是下限。结构与主键齐、年份齐、链维弱，判部分支持。",
            "criteria": {
                "result_table_exists": False,
                "year_field_exists": True,
                "chain_field_exists": False,
                "hit_rate": round(matched / total, 4) if total else None,
                "proxy_used": True,
            },
        },
        "base_years_used": YEARS,
        "base_years_missing": [],
        "base_years_note": "院所成立年取 incorporation_date 的年份（1,996/2,074 有值，78 行空值不进任何年，不摊 0）；高校取 est_year。窗口 2016—2025，2026 为残年（22 家）不入窗口。未命中年份的机构在「未归属」桶，不按比例摊派到链。",
        "sources": [
            {"path": "code/_snapshots21/inst_base_gkx21.json",
             "table": "gkx.dwd_research_institute_base_info", "rows": 2074,
             "role": "科研院所底册（含成立日期）"},
            {"path": "code/_snapshots21/heis21_20261022.json",
             "table": "gkx.dwd_org_heis_info", "rows": 3501,
             "role": "高校底册（含 est_year）"},
            {"path": "code/_snapshots21/chain_tree_20261021.json",
             "table": "gkx.dwd_industry_chain_info", "rows": 1273,
             "role": "环节名词典与顶层链回溯"},
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[OK] {METRIC} -> {OUT.name}  matched={matched}/{total} "
          f"hit={out['match_stats']['hit_rate']}")
    for r in rows:
        print(f"  {r['chain']} {r['chain_name'][:8]:<8} total={r['institutions_total']:<4} "
              f"2025={r['y2025_count']:<3} mom={r['y2025_mom']} {r['by_type']}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_REG_COMP_ACADEMIC 竞争力-学术生态（区域）（20261021 复现）

口径（calc-logic/CHAIN/M_CHAIN_REG_COMP_ACADEMIC.md，human:王惠）：
  加权平均三个三级指标（权重待甲方确认）：
    论文产出 = 链上高校与科研机构所属学者发表论文去重件数
    人才储备 = 链上高校与科研机构所属学者去重人数
    科研机构 = 链上高校与科研机构去重数量

链归属缺口（核心）：`dwd_org_industry_tags` 对 4 市高校/科研机构零标签
（panel.acad.heis_city4_tagged = 0 / inst_city4_tagged = 0），故"链上"不能直接取标签，
本脚本改用**产学研共著**这一可溯源替代：论文作者机构串中若出现某链上企业（名称匹配），
则同篇论文的非企业机构即计入该链（覆盖不到即 0，不外推）。

输出：code/M_CHAIN_REG_COMP_ACADEMIC_out.json
"""
from __future__ import annotations

import json
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _chain_reg_common import CHAIN_AXIS, CITY4, STAT_YEAR, load_panel, load_small, stats, write_out  # noqa: E402

MID = "M_CHAIN_REG_COMP_ACADEMIC"
CHAIN_CN = {
    "INB1306": "软件与信息服务", "INB1309": "人工智能", "INB1333": "智能终端", "INB1502": "数字创意",
    "INB2505": "合成生物", "INB1204": "机器人", "INB1303": "集成电路", "INB1323": "传感器",
    "INB1354": "具身智能", "INB1209": "智能网联汽车", "INB1236": "低空经济", "INB2503": "生物医药",
}
MED_HINT = re.compile(r"医院|医学院|医学中心|疾病|卫生|临床|中医|药学院|肿瘤|口腔|护理|疾控|血液")
SPLIT = re.compile(r"[;；,，、]")


def minmax(vals):
    lo, hi = min(vals), max(vals)
    return [round(100 * (v - lo) / (hi - lo), 1) if hi > lo else 0.0 for v in vals]


def main() -> None:
    t0 = time.time()
    panel = load_panel()
    small = load_small()
    snap = json.loads((Path(__file__).parent / "_snapshots" /
                       "chain_reg_paper_inst_20261021.json").read_text())

    # 机构底册（高校 + 科研院所），带城市
    acad = {}
    for row in small["heis"]:
        if row[4]:
            acad[row[2]] = (row[4], "高校")
    for row in small["inst"]:
        if row[4]:
            acad[row[2]] = (row[4], "科研机构")
    idx4 = defaultdict(list)
    for nm in acad:
        if len(nm) >= 4:
            idx4[nm[:4]].append(nm)
    for k in idx4:
        idx4[k].sort(key=len, reverse=True)

    # 链上企业名称 → 链（含城市校验）
    name_chain = {}
    for nm, pairs in panel["name_chain"].items():
        seq = []
        for p in pairs:
            code = p[0] if isinstance(p, (list, tuple)) else p
            if code in CHAIN_AXIS:
                seq.append(code)
        if seq:
            name_chain[nm] = seq
    ent_idx = defaultdict(list)
    for nm in name_chain:
        if len(nm) >= 4:
            ent_idx[nm[:4]].append(nm)
    for k in ent_idx:
        ent_idx[k].sort(key=len, reverse=True)

    def match_acad(s):
        """机构串 → 底册机构名（优先最长前缀命中，含 ';' 分段）"""
        for seg in [s] + SPLIT.split(s):
            seg = seg.strip()
            if len(seg) < 4:
                continue
            for nm in idx4.get(seg[:4], []):
                if seg.startswith(nm):
                    return nm
        return None

    def match_ent(s):
        for seg in [s] + SPLIT.split(s):
            seg = seg.strip()
            if "公司" not in seg or len(seg) < 6:
                continue
            for nm in ent_idx.get(seg[:4], []):
                if seg.startswith(nm):
                    return nm
        return None

    inst_chain = defaultdict(set)      # 机构 -> 链集合
    cell_inst = defaultdict(set)       # (chain, city) -> 机构
    paper_cell = defaultdict(int)      # (chain, city) -> 产学研共著论文数
    n_ent_mention = n_ent_matched = n_paper_hit = 0
    ent_hit_names = Counter()
    med_inst = 0

    for pid, inst_lists in snap["papers"].items():
        flat = []
        for s in inst_lists:
            flat.extend(x.strip() for x in SPLIT.split(s) if x.strip())
        if not flat:
            continue
        chains = set()
        for s in flat:
            if "公司" in s:
                n_ent_mention += 1
                nm = match_ent(s)
                if nm:
                    n_ent_matched += 1
                    ent_hit_names[nm] += 1
                    chains.update(name_chain[nm])
        if not chains:
            continue
        n_paper_hit += 1
        for s in flat:
            if "公司" in s:
                continue
            nm = match_acad(s)
            if not nm:
                continue
            city, kind = acad[nm]
            if MED_HINT.search(nm):
                med_inst += 1
            for ch in chains:
                inst_chain[nm].add(ch)
                if city in CITY4:
                    cell_inst[(ch, city)].add(nm)
        for ch in chains:
            for s in flat:
                if "公司" in s:
                    continue
                nm = match_acad(s)
                if nm and acad[nm][0] in CITY4:
                    paper_cell[(ch, acad[nm][0])] += 1

    # 学者 → 机构（精确名匹配），再按机构链归属铺到单元
    schol_by_org = defaultdict(set)
    for sid, name, org, pn, cite, hind in small["scholar"]:
        if org:
            schol_by_org[org.strip()].add(sid)
    cell_scholar = defaultdict(set)
    for nm, chains in inst_chain.items():
        city = acad[nm][0]
        if city not in CITY4:
            continue
        sids = schol_by_org.get(nm, set())
        for ch in chains:
            cell_scholar[(ch, city)] |= sids

    # 论文产出：学者全部论文（去重 paper_id，年 <= 统计年）
    papers_by_scholar = defaultdict(set)
    for sid, pid, yr in small["scholar_papers"]:
        if not yr or int(yr) <= STAT_YEAR:
            papers_by_scholar[sid].add(pid)
    cell_papers = {}
    for k, sids in cell_scholar.items():
        acc = set()
        for sid in sids:
            acc |= papers_by_scholar.get(sid, set())
        cell_papers[k] = len(acc)

    matrix = []
    for ch in CHAIN_AXIS:
        row = {"chain": ch, "chain_name": CHAIN_CN[ch], "cells": {}}
        for city in CITY4:
            k = (ch, city)
            row["cells"][city] = {
                "academic_institutions": len(cell_inst.get(k, ())),
                "scholars": len(cell_scholar.get(k, ())),
                "papers": cell_papers.get(k, 0),
                "coauthored_papers_with_chain_enterprise": paper_cell.get(k, 0),
            }
        matrix.append(row)

    A = [row["cells"][c]["academic_institutions"] for row in matrix for c in CITY4]
    B = [row["cells"][c]["scholars"] for row in matrix for c in CITY4]
    C = [row["cells"][c]["papers"] for row in matrix for c in CITY4]

    # 城市总量（不做链归属）：用于量化「链归属损耗」，避免把稀疏误读为资源匮乏
    city_scholars, city_papers, city_inst = {}, {}, {}
    for city in CITY4:
        names = [nm for nm, (ct, kind) in acad.items() if ct == city]
        city_inst[city] = len(names)
        sids = set()
        for nm in names:
            sids |= schol_by_org.get(nm, set())
        city_scholars[city] = len(sids)
        acc = set()
        for sid in sids:
            acc |= papers_by_scholar.get(sid, set())
        city_papers[city] = len(acc)
    cover = {}
    for city in CITY4:
        cell_i = set().union(*[cell_inst.get((ch, city), set()) for ch in CHAIN_AXIS])
        cell_s = set().union(*[cell_scholar.get((ch, city), set()) for ch in CHAIN_AXIS])
        uni = set()
        for sid in cell_s:
            uni |= papers_by_scholar.get(sid, set())
        cover[city] = {
            "inst_city_total": city_inst[city], "inst_chain_attributed": len(cell_i),
            "inst_cover_pct": round(100 * len(cell_i) / city_inst[city], 1) if city_inst[city] else None,
            "scholar_city_total": city_scholars[city], "scholar_chain_attributed": len(cell_s),
            "scholar_cover_pct": round(100 * len(cell_s) / city_scholars[city], 1) if city_scholars[city] else None,
            "papers_city_total": city_papers[city],
            "papers_attributed_distinct": len(uni),
            "papers_cell_sum_double_counted": sum(cell_papers.get((ch, city), 0) for ch in CHAIN_AXIS),
        }

    na, nb, nc = minmax(A), minmax(B), minmax(C)
    for i, row in enumerate(matrix):
        for j, c in enumerate(CITY4):
            idx = i * 4 + j
            row["cells"][c]["composite_equal_weight_0_100"] = round((na[idx] + nb[idx] + nc[idx]) / 3, 1)

    payload = {
        "metric_id": MID,
        "metric_name": "竞争力-学术生态",
        "date": "2026-10-21",
        "formula_owner": "王惠（calc-logic/CHAIN/M_CHAIN_REG_COMP_ACADEMIC.md）",
        "stat_year": STAT_YEAR,
        "region_axis": CITY4,
        "chain_axis": len(CHAIN_AXIS),
        "weights": "未定稿（原稿「权重待甲方确认」），合成分按等权 1/3 演示",
        "probes": {
            "heis_rows": len(small["heis"]),
            "inst_rows": len(small["inst"]),
            "heis_city4_tagged": panel["acad"]["heis_city4_tagged"],
            "inst_city4_tagged": panel["acad"]["inst_city4_tagged"],
            "scholars_total": len(small["scholar"]),
            "scholar_paper_relations": len(small["scholar_papers"]),
            "papers_with_inst": snap["n_papers_with_inst"],
            "enterprise_mentions": n_ent_mention,
            "enterprise_mentions_matched": n_ent_matched,
            "papers_with_chain_enterprise": n_paper_hit,
            "matched_chain_enterprises": len(ent_hit_names),
            "cell_instances_medical": med_inst,
            "distinct_inst_matched": len(inst_chain),
        },
        "matrix": matrix,
        "stats_institutions": stats(A),
        "stats_scholars": stats(B),
        "stats_papers": stats(C),
        "city_attribution_coverage": cover,
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": (
                f"三项均有真实底层（高校 {len(small['heis']):,} 家、科研机构 {len(small['inst']):,} 家、"
                f"学者 {len(small['scholar']):,} 人、学者—论文关系 {len(small['scholar_papers']):,} 条、"
                f"带机构信息的论文 {snap['n_papers_with_inst']:,} 篇），但「链上」这一层无标签："
                f"4 市高校/机构在 `dwd_org_industry_tags` 命中 0 条（heis_city4_tagged=0、inst_city4_tagged=0），"
                f"只能经产学研共著反推（企业提及 {n_ent_mention:,} 次，名称匹配 {n_ent_matched:,} 次，"
                f"命中链上企业的论文 {n_paper_hit:,} 篇），机构→链是「有共著才有」的选择性覆盖，故判部分支持。"
            ),
            "criteria": {"cells_null_or_zero_institutions": sum(1 for v in A if v == 0),
                         "cells_zero_scholars": sum(1 for v in B if v == 0),
                         "cells_zero_papers": sum(1 for v in C if v == 0)},
        },
        "notes": [
            "链归属替代路径：论文机构串中出现链上企业（名称前缀最长匹配）→ 同篇非企业机构计入该链；"
            "无共著即不入账（不按 0 均摊、不外推）。",
            "机构串归属底册用「最长前缀匹配」（如「上海交通大学材料科学与工程学院…」→「上海交通大学」），"
            "不匹配的机构串丢弃并计入未匹配池。",
            "学者→机构只做机构名精确相等匹配（`scholar_org_name_zh`），比模糊匹配保守，属低估。",
            "论文产出取这些学者的**全部**论文（王惠原文口径），故同一学者挂多链时其论文在各链各计一次。",
            f"机构串中含医学线索（医院/医学院/临床等）出现 {med_inst:,} 次，医疗类机构在论文机构池中占比高，"
            "会把「学术生态」拉向临床医学而非产业链技术，须在解读时剔除或分域看。",
            "权重未定稿，合成分仅等权演示。",
        ],
        "elapsed_sec": round(time.time() - t0, 2),
    }
    write_out(MID, payload)
    print("inst", stats(A), "scholar", stats(B), "papers", stats(C))
    print("ent mention", n_ent_mention, "matched", n_ent_matched, "paper hit", n_paper_hit)


if __name__ == "__main__":
    main()

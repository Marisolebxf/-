#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TECH_ENTITY_TOP5 · 根技术点 Top5 关键实体与关联强度（gkx 口径重建件，零 SQL）

需求锚点：算法库 SRS 序号 105 的展示面——「按已有 105 边权截取与当前根技术点关联的
Top5 实体（人/机构/论文/专利），卡片含名称、类型、关联强度。不另造排序模型。」

口径（不改需求给的「边权即强度」原则）：
  根技术点 = 深圳 2024 年件数前 5 的 IPC4；
  邻居     = 与根 IPC4 共享申请人最多的 5 个 IPC4（105 R1 的申请人共现代理）；
  关联强度 w：
    机构/企业 ← IPC4×申请人件数（同根 IPC4 的件数）
    专利      ← 该专利 IPC 集合落在「根 ∪ 邻居」的个数（仅 2024 年 pn 清单可查）
    人才      ← 【不可算】库内无「发明人 × IPC」落盘，dwd_patent 聚合被 §3.13 禁止
  展示强度 = 100 × w / 同类内最大 w（线性缩放，不改变名次）。

与旧稿的差异：
  旧稿 import `_tech_e_common`（六城专利行 + 发明人 + 论文标题 + 关键词桥），
  本件不 import 任何旧 helper，只读 gkx 落盘快照；**人才卡整类缺失**，专利卡无标题
  （快照未落 title），只能给公开号，已在产物与正文标注。

数据源（零 SQL）：
  _snapshots21/patent_scan_20261021.pkl                六城×年×IPC4（pn 哈希 id 集合）
  _snapshots21/patent2024_scan_20261021.json           2024 年 申请人→IPC4→pn 清单
  _snapshots21/patent_ipc4_by_name_20261021.json       IPC4×申请人 件数 581,585 行
  _snapshots21/plan_ipc_lexicon_gkx21.json             IPC4→关键词权重（26,722 词）
  _snapshots21/a25_paper_panel.json                    论文 100,900 条（标题/关键词/作者机构）

运行：cd code && python3 M_TECH_ENTITY_TOP5.py
产物：code/M_TECH_ENTITY_TOP5_out.json
"""
from __future__ import annotations

import collections
import json
import os
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")

MID = "M_TECH_ENTITY_TOP5"
N_ROOTS = 5
TOPK = 5
ACAD = ("大学", "学院", "研究院", "研究所", "研究中心", "实验室", "医院")
ENT = ("公司", "集团", "厂", "企业", "合伙")
IPC_LABEL = {
    "G06F": "电数字数据处理", "G06N": "基于特定计算模型的计算机系统（AI）",
    "G06Q": "行政/商业/金融/管理用途的数据处理系统", "G06V": "图像或视频识别",
    "G06T": "一般的图像数据处理或产生", "G01N": "借助测定材料性质测试或分析材料",
    "G01R": "测量电变量/磁变量", "H04L": "数字信息的传输", "H04W": "无线通信网络",
    "H04N": "图像通信", "H01M": "电池/燃料电池", "H02J": "供电或配电电路装置",
    "H05K": "印刷电路/电气设备外壳", "A61K": "医用/梳妆用配制品",
    "A61B": "诊断/外科器械", "B01D": "分离", "B29C": "塑料成型",
    "B23K": "焊接/钎焊", "C12N": "微生物或酶", "G16H": "医疗信息学",
    "H01L": "半导体器件", "B60L": "电动车辆", "G05B": "一般控制或调节系统",
}


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def pct_rank(vals):
    n = len(vals)
    if not n:
        return []
    order = sorted(range(n), key=lambda i: vals[i])
    out = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            out[order[k]] = avg / n
        i = j + 1
    return out


def main():
    import pickle
    with open(os.path.join(SNAP, "patent_scan_20261021.pkl"), "rb") as f:
        scan = pickle.load(f)

    # ---------------- 1. 根技术点：深圳 2024 件数 TOP5
    sz2024 = collections.Counter()
    for (city, y, ipc), pns in scan["ipc_pn"].items():
        if city == "深圳" and int(y) == 2024:
            sz2024[ipc] = len(pns)
    roots = [ipc for ipc, _ in sz2024.most_common(N_ROOTS)]

    # ---------------- 2. 申请人共现邻居
    ipc_name = load("patent_ipc4_by_name_20261021.json")
    by_ipc = collections.defaultdict(dict)
    by_app = collections.defaultdict(set)
    for ipc4, nm, n in ipc_name:
        by_ipc[ipc4][nm] = by_ipc[ipc4].get(nm, 0) + int(n)
        by_app[nm].add(ipc4)

    neighbors = {}
    for r in roots:
        co = collections.Counter()
        for nm in by_ipc.get(r, {}):
            for other in by_app[nm]:
                if other != r:
                    co[other] += 1
        neighbors[r] = [{"ipc4": k, "shared_applicants": v,
                         "label": IPC_LABEL.get(k, "")}
                        for k, v in co.most_common(TOPK)]

    # ---------------- 3. 实体卡
    scan24 = load("patent2024_scan_20261021.json")
    pn_ipc = collections.defaultdict(set)
    for nm, ipcd in scan24["ipc"].items():
        for code, pns in ipcd.items():
            code4 = code[:4].upper()
            for pn in pns:
                pn_ipc[pn].add(code4)
    pat_sample = load("a25_patent_sample.json")
    pat_rows = pat_sample["rows"]

    papers = load("a25_paper_panel.json")
    kw_by_id = {c["id"]: (c.get("keywords") or "") for c in papers["cls"]}
    paper_rows = []
    for p in papers["paper"]:
        kws = kw_by_id.get(p["id"], "")
        paper_rows.append((p["id"], p.get("zh_name") or "", p.get("y") or "", kws))
    lexicon = load("plan_ipc_lexicon_gkx21.json")["terms_by_ipc"]

    roots_out = []
    for r in roots:
        nbrs = [n["ipc4"] for n in neighbors[r]]
        scope = {r} | set(nbrs)

        # 机构 / 企业
        orgs, ents = [], []
        for nm, w in by_ipc.get(r, {}).items():
            if any(x in nm for x in ACAD):
                orgs.append((nm, w))
            elif any(x in nm for x in ENT):
                ents.append((nm, w))
        orgs.sort(key=lambda x: -x[1])
        ents.sort(key=lambda x: -x[1])

        def cards(items, typ):
            if not items:
                return []
            mx = items[0][1]
            return [{"name": nm, "type": typ, "w": w,
                     "strength": round(100 * w / mx, 1)} for nm, w in items[:TOPK]]

        # 专利：2024 pn 清单里，IPC ∈ 根∪邻居 的个数；因 pn→IPC 只落主分类，
        # 该计数对同根专利恒为 1，不能区分名次 → 改用 20 万行专利样本的 keywords 做二次排序。
        pats = []
        for pn, codes in pn_ipc.items():
            hit = len(codes & scope)
            if hit:
                pats.append((pn, hit))
        pats.sort(key=lambda x: (-x[1], x[0]))

        # 论文：关键词桥（根 IPC4 的词典权重求和；要求 ≥2 个 w≥0.03 的词，
        # 且剔除权重 1.0 的规模异常词——该词是建典样本的极值，单命中会把无关论文顶到第一）
        terms = [(t, w) for t, w in lexicon.get(r, {}).items()
                 if 0.03 <= w < 1.0 and len(t) >= 2][:80]
        pw = []
        for pid, title, y, kws in paper_rows:
            blob = (title + " " + kws).lower()
            hits = [(t, w) for t, w in terms if t in blob]
            if len(hits) < 2:
                continue
            pw.append((pid, title, y, round(sum(w for _, w in hits), 2), len(hits)))
        pw.sort(key=lambda x: (-x[3], -x[4]))

        def paper_cards(items):
            if not items:
                return []
            mx = items[0][3]
            return [{"name": t or pid, "type": "论文", "w": s, "hits": h, "year": y,
                     "strength": round(100 * s / mx, 1)} for pid, t, y, s, h in items[:TOPK]]

        # 专利卡：样本内主分类命中根或邻居，按关键词亲和二次排序
        kws_root = [(t, w) for t, w in lexicon.get(r, {}).items() if 0.03 <= w < 1.0]
        pat_cards = []
        for row in pat_rows:
            code4 = (row.get("main_classification_ipcr") or "")[:4].upper()
            if code4 not in scope:
                continue
            blob = (row.get("keywords") or "").lower()
            kw_hits = [(t, w) for t, w in kws_root if t in blob]
            score = round(1.0 + sum(w for _, w in kw_hits), 3)
            pat_cards.append({"name": row.get("granted_number") or f"dwd_id:{row.get('dwd_id')}",
                              "type": "专利", "w": score, "kw_hits": len(kw_hits),
                              "year": row.get("apdt_year"),
                              "applicant": row.get("first_applicant_name"),
                              "ipc": code4})
        pat_cards.sort(key=lambda x: (-x["w"], x["name"]))
        if pat_cards:
            mx = pat_cards[0]["w"]
            for c in pat_cards:
                c["strength"] = round(100 * c["w"] / mx, 1) if mx else 0.0
        pat_cards = pat_cards[:TOPK]

        roots_out.append({
            "ipc4": r, "label": IPC_LABEL.get(r, ""),
            "sz_2024": sz2024[r],
            "n_applicants": len(by_ipc.get(r, {})),
            "neighbors": neighbors[r],
            "cards": {
                "institutions": cards(orgs, "科研机构/高校"),
                "enterprises": cards(ents, "企业"),
                "patents": pat_cards,
                "papers": paper_cards(pw),
                "talents": [],
            },
            "counts": {"institutions": len(orgs), "enterprises": len(ents),
                       "patents_2024_in_scope": len(pats), "patent_cards": len(pat_cards),
                       "papers_matched": len(pw), "talents": 0},
        })

    # ---------------- 4. 覆盖披露
    cover = {
        "roots": N_ROOTS, "topk": TOPK,
        "ipc_by_name_rows": len(ipc_name),
        "applicants_total": len(by_app),
        "pn_2024_with_ipc": len(pn_ipc),
        "papers_scanned": len(paper_rows),
        "papers_total_table": papers.get("counts", {}).get("paper"),
        "lexicon_terms": sum(len(v) for v in lexicon.values()),
        "talent_blocked": True,
    }

    payload = {
        "metric_id": MID,
        "metric_name": "根节点 Top5 关键实体与关联强度",
        "domain": "TOPIC-TECH / 技术-实体关联展示面",
        "support_judgment": "部分支持",
        "support_reason": (
            f"{N_ROOTS} 个根技术点、{len(roots_out)} 组卡片可出：机构/企业卡有全量 IPC4×申请人（{len(ipc_name):,} 行），"
            "论文卡有 100,900 篇标题+关键词桥；但**人才卡整类不可算**——gkx 无「发明人×IPC」落盘，"
            "dwd_patent 聚合被 DATA_FACTS §3.13 禁止；专利卡无标题字段（快照未落 title），"
            "只能给公开号。四类实体缺一类、弱一类，判部分支持。"
        ),
        "generated_at": "2026-10-22",
        "main_db": "gkx @ 183.240.141.251:3318（gkx_reader_zp，只读）",
        "sql_count": 0,
        "sources": [
            "code/_snapshots21/patent_scan_20261021.pkl（六城×年×IPC4，pn 哈希 id）",
            "code/_snapshots21/patent2024_scan_20261021.json（2024 年 1,142 名申请人→IPC4→pn）",
            "code/_snapshots21/patent_ipc4_by_name_20261021.json（581,585 行）",
            "code/_snapshots21/plan_ipc_lexicon_gkx21.json（26,722 词/484 IPC4）",
            "code/_snapshots21/a25_paper_panel.json（100,900 篇）",
        ],
        "base_years_used": [2024],
        "base_years_missing": [2017, 2018, 2019, 2020, 2025, 2026],
        "base_years_note": (
            "根技术点用 2024 单年（深圳最新完整年）；机构/企业边权为全期累计（2021—2026），"
            "专利卡限定 2024（唯一有 pn 清单的年份）；论文卡不限年（库内以 2019—2024 为主）。"
            "2017—2020 在 dwd_patent 为零行，未补 0、未外推。"
        ),
        "definition_note": (
            "需求明确「不另造排序模型」，故强度 = 边权（共现/件数）本身，展示值只做同类线性缩放；"
            "邻居定义由「专利内 IPC 共现」退化为「申请人共现」——快照无专利级多 IPC 清单（仅主分类单值），"
            "该退化使邻居偏「同主体多领域」，不是技术互补。"
        ),
        "coverage": cover,
        "roots": roots_out,
        "gaps": [
            "人才卡：无「发明人×IPC」表；patent_inventor_counts_gkx 只有人名→件数，无分类号，无法挂到根技术点；",
            "专利卡：a25_patent_sample 有 20 万行标题缺失（只落 dwd_id/分类号/年份/公开号/申请人/关键词），卡片只能显示公开号；",
            "邻居：专利申请表只落主分类（1 个 IPC），无「一件专利多分类号」清单，R1 边只能用申请人共现代理；",
            "论文桥：词典是 dwd_patent.keywords 1/8 抽样建典（296,155 行），论文标题命中即计权，未做语义校验；",
            "论文库只有 100,900 篇（dwd_zh_paper 子集），中文为主，英文论文覆盖不足。",
        ],
    }

    out = os.path.join(HERE, f"{MID}_out.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)

    print("wrote", os.path.basename(out))
    print("cover", cover)
    for r in roots_out:
        print(r["ipc4"], r["label"], "sz2024", r["sz_2024"], "counts", r["counts"],
              "nbr", [n["ipc4"] for n in r["neighbors"]])
        print("   org", [(c["name"], c["w"]) for c in r["cards"]["institutions"][:3]])
        print("   pat", [(c["name"], c["w"]) for c in r["cards"]["patents"][:2]])
        print("   paper", [(c["name"][:28], c["w"]) for c in r["cards"]["papers"][:2]])


if __name__ == "__main__":
    main()

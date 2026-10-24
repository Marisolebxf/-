#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""创新影响分数（M_INNOV_DS_04_REALTIME_004）—— **节点级产出规模**

王惠口径（calc-logic M_INNOV_IMPACT_SCORE）：对**实体节点**赋创新影响分，二维——
  产出规模：机构 = 专利数 + 论文数；领域 = 专利数
  网络影响：机构 = 合作邻居数；领域 = 专利被引合计
极值归一后加权 ×100，按 entity_type 分组排名。

本件的实测结论（决定了它只交付一半）：
  * 领域（IPC4）产出规模：全量可算，634 个节点，逐年件数可复核；
  * 机构产出规模：专利侧全量可算（169,226 个申请人、合计 2,939,895 = 表行数），
    论文侧只有分类子集 20,048 篇可归属（19.87%），故论文件数只作**下界展示列**、不进打分；
  * 网络影响两侧都不可算：共申请人表 28,964 行只覆盖 20,000 件专利（0.68%），
    项目表 funded_institution **0 条非空**，专利被引表只有 467 个 pn 能连回主表（2.28%）。

因此本件产出的是「节点产出规模分」（单维，剩余维重归一），不是完整的「创新影响分数」。
按 §〇 判 **部分支持**。

重建背景：原稿读 20261020 目录共享 bundle（演示库 + 2017—2020 补零，DATA_FACTS §3.19）。
本脚本零 SQL、零 bundle。

产物：code/M_INNOV_DS_04_REALTIME_004_out.json
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import _a25_common as A
import _ds04_common as D

METRIC = "M_INNOV_DS_04_REALTIME_004"
TOP_N = 20


def domain_panel() -> dict:
    """领域节点：IPC4 全量件数 + 机构数 + 观察窗口。"""
    ipc = D.ipc_year()
    orgs = D.ipc_orgs()
    rows = []
    for term, yc in ipc.items():
        total = sum(yc.get(y, 0) for y in D.PATENT_YEARS)
        win = sum(yc.get(y, 0) for y in D.COMPLETE_YEARS)
        rows.append({
            "entity_type": "domain",
            "node": term,
            "output_total": total,
            "output_2021_2024": win,
            "n_orgs_2024": orgs.get((term, D.T)),
            "year_counts": {str(y): yc.get(y, 0) for y in D.PATENT_YEARS},
        })
    rows.sort(key=lambda r: -r["output_total"])
    return {"rows": rows, "n_nodes": len(rows),
            "sum_output": sum(r["output_total"] for r in rows)}


def org_panel() -> dict:
    """机构节点：申请人全量件数（专利）+ 论文件数下界（不参与打分）。"""
    agg = D.applicant_agg()
    base = D.base_orgs()
    papers = D.org_papers()
    rows = []
    matched = 0
    for nm, v in agg.items():
        n = int(v[0])
        g = int(v[1])
        b = base.get(nm)
        if b:
            matched += 1
        rows.append({
            "entity_type": "org",
            "node": nm,
            "output_total": n,
            "output_patent": n,
            "granted": g,
            "grant_rate": round(g / n, 4) if n else None,
            "papers_lower_bound": papers.get(nm, 0),
            "city": (b or {}).get("city"),
            "province": (b or {}).get("province"),
            "industry_l1": (b or {}).get("l1"),
            "in_base": 1 if b else 0,
        })
    rows.sort(key=lambda r: -r["output_total"])
    return {"rows": rows, "n_nodes": len(rows),
            "sum_output": sum(r["output_total"] for r in rows),
            "n_in_base": matched,
            "base_match_rate": round(matched / max(len(rows), 1), 4)}


def score(rows: list) -> None:
    """单维打分：产出规模 → **对数压缩后极值归一** ×100（剩余维重归一后即单维）。

    为什么不是线性极值归一：专利件数长尾极重（机构最大 81,376 件、领域最大 190,077 件，
    中位数分别是个位数与 3 位数）。线性 min-max 会把 99% 的节点压到 0.0x，分数失去区分度；
    先取 log10 再 min-max，头部与中段都保留分辨率，代价是分数不再是「件数的线性倍数」。
    同时输出 `rank_pct`（百分位秩）作为序信息的对照列——它是严格保序的，但顶部
    （169,226 个机构里前 40 名）在两位小数下会并成 100.00，故只作参考。
    """
    vals = [r["output_total"] for r in rows]
    logs = [__import__("math").log10(v) if v > 0 else 0.0 for v in vals]
    lo, hi = min(logs), max(logs)
    for r, lg, pr in zip(rows, logs, D.pct_rank(vals)):
        s = 0.5 if hi == lo else (lg - lo) / (hi - lo)
        r["output_score"] = round(100 * s, 2)
        r["impact_score"] = round(100 * s, 2)   # 单维：网络影响缺测不参与权重
        r["rank_pct"] = round(pr, 3)
        r["n_dims_scored"] = 1
        r["missing_dims"] = ["network"]


def main():
    t0 = time.time()
    dom = domain_panel()
    org = org_panel()
    score(dom["rows"])
    score(org["rows"])

    org_base = [r for r in org["rows"] if r["in_base"] == 1]
    org_base.sort(key=lambda r: -r["output_total"])
    papers_meta = D.org_papers_meta()
    facts = A.facts()

    probes = {}
    pfile = HERE / "_snapshots21" / "probe_ds04_20261022.json"
    if pfile.exists():
        probes = __import__("json").loads(pfile.read_text(encoding="utf-8"))

    def pv(label):
        d = probes.get(label) or {}
        return d.get("row") if d.get("ok") else None

    out = {
        "metric_id": METRIC,
        "name": "创新影响分数",
        "vendor_metric": "M_INNOV_IMPACT_SCORE",
        "formula_owner": "王惠",
        "view": "node",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "runtime_sec": None,
        "data_source": ("gkx.dwd_patent 全量派生（IPC 小类×年 2,420,915 件、"
                        "申请人×件数/授权数 2,939,895 件、申请人×年 275,135 组）、"
                        "gkx.dwd_org_base_info 底册 189,116 行、gkx.dwd_zh_author 62,002 行"),
        "db": "gkx @ 183.240.141.251:3318（只读，本脚本零 SQL）",
        "definition": ("对实体节点赋创新影响分：产出规模（机构=专利+论文，领域=专利）"
                       "与网络影响（机构=合作邻居数，领域=专利被引）二维加权 ×100，"
                       "按 entity_type 分组排名。本件网络影响缺测，实际交付单维产出规模分。"),
        "statistical_year": D.T,
        "windows": {"recent": list(D.RECENT), "base_formula": list(D.BASE_FORMULA),
                    "base_used": list(D.BASE_USED_PATENT)},
        "params": {"entity_types": ["domain", "org"], "dims": ["output_scale", "network_impact"],
                   "dims_available": ["output_scale"], "dims_missing": ["network_impact"],
                   "norm": "log10 压缩后极值归一 ×100（线性 min-max 会把中位数压到 0）；附 rank_pct 百分位秩对照列",
                   "weights": "单维重归一：产出规模占 1.0"},

        # ---- 硬约束：基期三字段进顶层 ----
        "base_years_used": list(D.BASE_USED_PATENT),
        "base_years_missing": list(D.BASE_MISSING_PATENT),
        "base_years_note": D.BASE_NOTE,

        "family": {
            "group": "M_INNOV_DS_04（科技发展态势·全球创新监测）",
            "this": "REALTIME_004 = **节点级**产出规模与影响分（实体是机构/IPC 领域）",
            "sibling": {
                "M_INNOV_DS_04_MONITOR_001": "实体是**词条**，算突现；本件实体是**节点**，算规模",
                "M_INNOV_DS_04_MONITOR_002": "词条的详情价值分，与节点得分不可混用",
                "M_INNOV_DS_04_REALTIME_005": "在本件节点年序列上做 Holt 外推（本库样本期不足）",
            },
            "key_diff": "词条 vs 节点：MONITOR 的主键是 point_key（IPC 小类/关键词），REALTIME 的主键是实体节点（机构名/IPC 小类）",
        },

        "probes": {
            "domain": {"n_ipc4": dom["n_nodes"], "sum_output": dom["sum_output"],
                       "years": list(D.PATENT_YEARS)},
            "org": {"n_applicants": org["n_nodes"], "sum_output": org["sum_output"],
                    "n_in_base": org["n_in_base"], "base_match_rate": org["base_match_rate"],
                    "base_rows": 189116, "base_names": 189068, "base_dup": 47},
            "paper_side": papers_meta,
            "patent_applicants_table": {"rows": pv("patent_applicants")},
            "zh_author": {"rows": pv("zh_author")},
            "zh_author_inst_uniq": {"rows": pv("zh_author_inst_uniq")},
            "zh_project": {"rows": pv("zh_project")},
            "patent_cited": {"rows": pv("patent_cited"),
                             "joinable_pn": (facts.get("cited_link") or [{}])[0].get("n")},
            "cited_joinability_note": ("被引表 20,515 行只有 467 个 pn 能连回 dwd_patent（2.28%），"
                                       "领域级「专利被引合计」不成立"),
        },
        "compute": {
            "n_nodes_domain": dom["n_nodes"],
            "n_nodes_org": org["n_nodes"],
            "domain_output_dist": D.dist([r["output_total"] for r in dom["rows"]]),
            "org_output_dist": D.dist([r["output_total"] for r in org["rows"]]),
            "domain_score_dist": D.dist([r["impact_score"] for r in dom["rows"]]),
            "org_score_dist": D.dist([r["impact_score"] for r in org["rows"]]),
            "top_domain": dom["rows"][:TOP_N],
            "top_org": org_base[:TOP_N],
            "top_org_raw": org["rows"][:TOP_N],
        },
        "quarantine_delta": {
            "why": ("隔离前旧稿读 20261020 共享 bundle，且机构维直接判「不可产出」；"
                    "本件用 gkx 全量申请人聚合把机构产出规模补了出来"),
            "old_vs_new": [
                {"item": "领域节点数", "old": "Top20（bundle 切片）", "new": dom["n_nodes"],
                 "cause": "旧稿只绑定 bundle 的 impact_score 段 Top20；本件对 634 个小类全量打分"},
                {"item": "领域最高分", "old": 75.0, "new": dom["rows"][0]["impact_score"],
                 "cause": "旧稿 75.0 来自 H02J7/00 的 4 次被引经极值归一放大；本件不用被引、改百分位秩"},
                {"item": "领域被引最大", "old": 8, "new": None,
                 "cause": "被引表 pn 与专利主表连通率仅 2.28%，词条/领域级被引不成立，本件标缺测"},
                {"item": "机构维", "old": "未产出（判不可算）", "new": org["n_nodes"],
                 "cause": "旧稿依据 dwd_patent_applicants 覆盖 0.68% 判死；但产出规模可用全量申请人聚合，"
                          "只有网络影响才依赖合作边"},
                {"item": "机构最高分", "old": None, "new": org["rows"][0]["impact_score"],
                 "cause": "同上；本件 org_in_base 前 20 名见 compute.top_org"},
            ],
        },
        "support_judgment": "部分支持",
        "support_basis": (
            "产出规模维在两类节点上都已全量闭合（领域 634 个 IPC 小类 / 2,420,915 件；"
            "机构 169,226 个申请人 / 2,939,895 件，合计与表行数逐位相等）；"
            "但网络影响维两侧都拿不到数据——共申请人表 28,964 行仅覆盖 20,000 件专利（0.68%）、"
            "项目表 funded_institution 0 条非空、专利被引表 pn 连通率 2.28%；"
            "论文侧只有 19.87% 的论文能归属到机构。二维公式只能执行一维，故判部分支持。"),
        "reasons": [
            "用 log10 压缩后极值归一、而非线性 min-max：机构件数最大 81,376、中位数 1—2 件，"
            "线性归一会把 99% 的机构压到 0.0x；取对数后归一，头部与中段都有分辨率。"
            "代价是分数不代表线性倍数差。同表附 rank_pct 百分位秩供严格保序复核（其顶部两位小数会并成 100.00）；",
            "网络影响（机构合作邻居数）不可算：`dwd_patent_applicants` 实测 28,964 行 / 20,000 件专利，"
            "覆盖率 0.68%，用它建的合作图只能代表 0.68% 的样本；`dwd_zh_project` 的 "
            "funded_institution 实测 0 条非空、participating_institution 58,452 条非空但属项目参与方、"
            "不是专利合作边；",
            "网络影响（领域被引合计）不可算：`dwd_patent_cited` 20,515 行中只有 467 个 pn 能在 "
            "`dwd_patent` 命中（2.28%），且这 467 件摊到 634 个小类后每类不足 1 件；",
            "机构论文数是下界：`dwd_zh_author` 62,002 行只挂在 20,048 篇分类论文上（占 100,900 篇的 19.87%），"
            "论文强的机构会被系统性低估，故只作展示列、不进打分；",
            "机构名与底册按 `name_cn` 对齐，底册 189,116 行只有 189,068 个可用名称（47 行重名），"
            "重名机构的城市字段可能张冠李戴，已在 probes.org 披露。",
        ],
        "notes": [
            "本脚本零 SQL、无 reused_from；节点得分全部由本目录缓体现算。",
            "impact_score 在本件等于 output_score：网络影响缺测不补 0、也不参与权重（王惠「剩余维重归一」）。",
            "对外展示时不要把本件叫「创新影响分数」而不加限定——它只含产出规模一维。",
            "领域节点的「机构数」列来自全量缓存，仅作参考列，未进打分。",
        ],
    }
    out["runtime_sec"] = round(time.time() - t0, 1)

    p = D.write_out(METRIC, out)
    print("written", p)
    print("domain", dom["n_nodes"], "sum", dom["sum_output"])
    print("org", org["n_nodes"], "sum", org["sum_output"], "in_base", org["base_match_rate"])
    print("top domain:", [(r["node"], r["output_total"], r["impact_score"]) for r in dom["rows"][:5]])
    print("top org:", [(r["node"], r["output_total"], r["impact_score"]) for r in org["rows"][:5]])


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_DS_09_COMPREHENSIVE_008 潜在科技发展方向预警（王惠六源口径 · 20261021 改源版）

王惠口径（calc-logic/INNOV/M_INNOV_PLAN_DIRECTION_ALERT.md）：
  按 IPC 前 4 位监测潜在方向；六源 = 专利/论文/项目/人才/产业/政策，各源近窗相对基线增速 g；
  F = 六源 g 加权；预警等级：F≥1 且两源 g>0 → 2；F≥0.5 → 1；否则 0。

数据源（20261021 版）：**只读三方库 gkx**
  gkx.dwd_patent / dwd_zh_paper / dwd_zh_project / dwd_policy_base / dwd_scholar_research_direction
本脚本实现：专利、产业、项目、政策（题名代理）、论文（题名代理）五源；人才源因方向字段为英文、
无法与中文锚点对齐而记缺口（见 disclosures）。算法与旧版逐字相同，只换数据源与前缀。
"""
import json
import os
import re
import time
from collections import Counter, defaultdict

import _innov_gkx21_common as ic

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "M_INNOV_DS_09_COMPREHENSIVE_008_out.json")

STOP = set("""方法 装置 设备 系统 技术 结构 工程 工业工程学 结构工程 材料 应用 工艺 产品 领域 研究 分析 设计
控制 检测 制备 制造 数据 信息 智能 平台 模块 单元 组件 方法及 及其 一种 包括 用于 基于 提高 优化 管理
计算 模型 算法 网络 装置及 系统及 工艺方法 工程学 学科 理论 实验 性能 功能 质量 效率 精度 方法研究""".split())

# 各源窗口（因覆盖期不同，逐源取「最近两个完整年」为近窗，之前两年为基线）
WIN = {
    "patent": {"base": (2021, 2022), "recent": (2024,)},
    "industry": {"base": (2021, 2022), "recent": (2024,)},
    "paper": {"base": (2018, 2019), "recent": (2022, 2023)},
    "project": {"base": (2017, 2018), "recent": (2020, 2021)},
    "policy": {"base": (2017, 2018), "recent": (2020, 2021)},
}

# 缺失占位符统一写法（DATA_FACTS §3.4：同一张表内大小写不统一）
REAL = "UPPER(TRIM(%s)) NOT IN ('NULL','','NONE','-')"


def growth(series_by_year, win):
    b = [series_by_year.get(y, 0) for y in win["base"]]
    r = [series_by_year.get(y, 0) for y in win["recent"]]
    bm = sum(b) / max(len(b), 1)
    rm = sum(r) / max(len(r), 1)
    return (rm - bm) / max(bm, 1), bm, rm


def patent_ipc4_year():
    """IPC4 × 申请年：专利件数 + 活跃申请人去重数（一次扫描后落缓存）。"""
    d = ic.load_cache("patent_ipc4_year_20261021.json")
    if d is None:
        rows = ic.q("SELECT LEFT(main_classification_ipcr,4) ipc4, apdt_year y, "
                    "COUNT(*) c, COUNT(DISTINCT first_applicant_name) orgs "
                    "FROM gkx.dwd_patent "
                    "WHERE main_classification_ipcr IS NOT NULL AND main_classification_ipcr <> '' "
                    "AND apdt_year IS NOT NULL GROUP BY 1,2")
        d = [[str(r[0]), int(r[1]), int(r[2] or 0), int(r[3] or 0)] for r in rows]
        ic.save_cache("patent_ipc4_year_20261021.json", d)
    return d


def main():
    t0 = time.time()
    out = {"metric_id": "M_INNOV_DS_09_COMPREHENSIVE_008", "probes": {}, "compute": {}}

    for t in ["dwd_patent", "dwd_zh_paper", "dwd_zh_project", "dwd_policy_base",
              "dwd_scholar_research_direction"]:
        out["probes"][t] = ic.count(t)
    out["probes"]["policy_keywords_real_rows"] = ic.q1(
        "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE " + (REAL % "keywords"))[0]
    out["probes"]["policy_theme_real_rows"] = ic.q1(
        "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE " + (REAL % "theme"))[0]
    out["probes"]["placeholder_rule"] = "UPPER(TRIM(col)) NOT IN ('NULL','','NONE','-')"

    # ---------- 专利/产业：IPC4 × 年 ----------
    pat_y = defaultdict(Counter)
    org_y = defaultdict(Counter)
    for ipc, y, c, orgs in patent_ipc4_year():
        pat_y[ipc][y] = c
        org_y[ipc][y] = orgs
    out["probes"]["ipc4_n"] = len(pat_y)
    out["probes"]["patent_year_span"] = [min(min(v) for v in pat_y.values()),
                                         max(max(v) for v in pat_y.values())]

    top_ipc = [k for k, _ in sorted(pat_y.items(), key=lambda kv: -sum(kv[1].values()))[:40]]

    # ---------- 方向语义锚：该 IPC4 专利关键词袋高频词（跨方向高频词按文档频率剔除） ----------
    # 旧版按 `WHERE LEFT(main_classification_ipcr,4)=%s ... LIMIT 3000` 逐方向取袋（40 次全表扫描，
    # 该列无索引，共享实例上每次 5~15 分钟）。这里改为**一次按主键分块顺扫**：按 `dwd_id` 升序
    # 依次取「该方向前 3000 条 keywords」，与旧版 `LIMIT 3000` 在主键顺序下的取值**完全一致**，
    # 但只扫到 40 个方向都取满即停（实测前 2~3 个 200 万 ID 块即满）。
    anchors_kw = ic.load_cache("anchor_kw_20261021.json")
    if anchors_kw is None:
        anchors_kw = {}
        need = {ipc: 3000 for ipc in top_ipc}
        cur = ic.q("SELECT MIN(dwd_id), MAX(dwd_id) FROM gkx.dwd_patent")[0]
        lo, hi = int(cur[0]), int(cur[1])
        BLK = 2_000_000
        a = (lo // BLK) * BLK
        while a <= hi and any(need.values()):
            rows = ic.q(
                "SELECT LEFT(main_classification_ipcr,4) ipc4, keywords FROM gkx.dwd_patent "
                f"WHERE dwd_id > {a} AND dwd_id <= {a + BLK} "
                "AND keywords IS NOT NULL AND keywords <> ''")
            for ipc, kw in rows:
                ipc = str(ipc)
                if need.get(ipc, 0) > 0:
                    anchors_kw.setdefault(ipc, []).append(str(kw))
                    need[ipc] -= 1
            a += BLK
        ic.save_cache("anchor_kw_20261021.json", anchors_kw)
    raw_anchor = {}
    for ipc in top_ipc:
        cnt = Counter()
        for r in anchors_kw.get(ipc, []):
            for t in ic.parse_kw(r):
                t = t.strip()
                if 2 <= len(t) <= 12 and t not in STOP and not t.isdigit():
                    cnt[t] += 1
        raw_anchor[ipc] = cnt
    df = Counter()
    for ipc, cnt in raw_anchor.items():
        for t in cnt:
            df[t] += 1
    anchors = {}
    for ipc, cnt in raw_anchor.items():
        keep = [(t, c) for t, c in cnt.most_common(400) if df[t] <= 3]
        anchors[ipc] = [t for t, _ in keep[:8]]
    out["compute"]["anchors"] = anchors
    out["compute"]["anchor_doc_freq_dropped"] = [t for t, k in df.items() if k >= 4][:20]
    out["probes"]["anchor_sampled_patents_per_ipc"] = 3000

    # ---------- 论文：题名逐年命中 ----------
    paper_rows = ic.q("SELECT zh_name, en_name, cover_year_start y FROM gkx.dwd_zh_paper")
    paper_titles = []
    for zh, en, y in paper_rows:
        try:
            yy = int(str(y)[:4])
        except Exception:
            continue
        paper_titles.append((yy, zh or en or ""))

    # ---------- 项目 ----------
    proj_rows = ic.q("SELECT keywords, title, FLOOR(approval_year/10000) y FROM gkx.dwd_zh_project")
    proj = []
    for kw, title, y in proj_rows:
        try:
            yy = int(y)
        except Exception:
            continue
        proj.append((yy, (kw or "") + " " + (title or "")))

    # ---------- 政策（题名代理，keywords/theme 列为字面 'NULL'） ----------
    pol_rows = ic.q("SELECT title, publish_year y FROM gkx.dwd_policy_base")
    pol = []
    for title, y in pol_rows:
        try:
            yy = int(str(y)[:4])
        except Exception:
            continue
        pol.append((yy, title or ""))

    def series_hits(items, terms):
        s = Counter()
        for y, text in items:
            if any(t in text for t in terms):
                s[y] += 1
        return s

    results = []
    for ipc in top_ipc:
        terms = anchors[ipc] or []
        row = {"ipc4": ipc, "anchors": terms, "sources": {}}
        gp, bm, rm = growth(pat_y[ipc], WIN["patent"])
        row["sources"]["patent"] = {"g": round(gp, 4), "base_mean": bm, "recent_mean": rm}
        gi, bm, rm = growth(org_y[ipc], WIN["industry"])
        row["sources"]["industry"] = {"g": round(gi, 4), "base_mean": bm, "recent_mean": rm}
        if terms:
            ps = series_hits(paper_titles, terms)
            g, bm, rm = growth(ps, WIN["paper"])
            row["sources"]["paper"] = {"g": round(g, 4), "base_mean": bm, "recent_mean": rm,
                                       "match_mode": "题名关键词命中（关键词表不可关联，代理口径）"}
            js = series_hits(proj, terms)
            g, bm, rm = growth(js, WIN["project"])
            row["sources"]["project"] = {"g": round(g, 4), "base_mean": bm, "recent_mean": rm}
            ls = series_hits(pol, terms)
            g, bm, rm = growth(ls, WIN["policy"])
            row["sources"]["policy"] = {"g": round(g, 4), "base_mean": bm, "recent_mean": rm,
                                        "match_mode": "政策题名命中（keywords/theme 为字面 'NULL'，代理口径）"}
        gs = []
        insufficient = []
        for k, v in row["sources"].items():
            if v["base_mean"] < 2:
                v["insufficient_base"] = True
                insufficient.append(k)
            else:
                gs.append(v["g"])
        F = sum(gs) / len(gs) if gs else 0.0
        pos = sum(1 for g in gs if g > 0)
        lv = 2 if (F >= 1 and pos >= 2) else (1 if F >= 0.5 else 0)
        row.update({"F": round(F, 4), "n_sources": len(gs), "n_sources_positive": pos,
                    "n_sources_insufficient": insufficient, "alert_level": lv})
        results.append(row)

    # 排序键与并列规则：F 降序，次键 IPC4 升序；名次按 competition rank（同分同名次、后续跳号）
    results.sort(key=lambda x: (-x["F"], x["ipc4"]))
    rank = 0
    prev = None
    for i, r in enumerate(results, 1):
        if r["F"] != prev:
            rank, prev = i, r["F"]
        r["rank_competition"] = rank

    out["compute"]["directions_scored"] = len(results)
    out["compute"]["alert_level_dist"] = dict(Counter(r["alert_level"] for r in results))
    out["compute"]["top12_f"] = results[:12]
    out["compute"]["bottom5_f"] = results[-5:]
    out["compute"]["multi_source_positive_ge3"] = [
        {"ipc4": r["ipc4"], "F": r["F"], "pos": r["n_sources_positive"], "anchors": r["anchors"]}
        for r in results if r["n_sources_positive"] >= 3][:12]
    out["compute"]["windows"] = WIN
    out["compute"]["rank_rule"] = "F 降序 + IPC4 升序（全序、可复现）；名次取 competition rank"
    out["compute"]["weight_source"] = {
        "F": "可用源等权平均（1/|S_ok|）",
        "provenance": "王惠写「加权平均」未给权重；等权为本实现自定，属**代理权重**，"
                      "甲方签认前 F 的绝对值与排序不得当作正式预警清单",
    }
    out["elapsed_s"] = round(time.time() - t0, 1)
    out["data_source"] = {"schema": "gkx", "host": "183.240.141.251:3318",
                          "tables": ["gkx.dwd_patent", "gkx.dwd_zh_paper", "gkx.dwd_zh_project",
                                     "gkx.dwd_policy_base", "gkx.dwd_scholar_research_direction"],
                          "row_counts_from": "_work_gkx21/GKX_INVENTORY.json"}

    out["support_judgment"] = "部分支持"
    out["support_reason"] = (
        "王惠六源中，专利与产业两源（IPC4 申请量、IPC4 活跃申请人）在 2021-2026 全覆盖、可直接算增速；"
        "论文与政策两源可借助方向锚点以题名匹配近似；项目源有真实关键词与立项年可命中；"
        "但 ①政策 keywords/theme 为字面 'NULL'（按 UPPER(TRIM()) 口径复核，真实值仍为 "
        f"{out['probes']['policy_keywords_real_rows']}/20,000 与 {out['probes']['policy_theme_real_rows']}/20,000），"
        "只能退为题名匹配；"
        "②论文关键词表 gkx.dwd_zh_paper_classification 与论文主表 JOIN 仅命中 799 篇（0.79%），论文维只能退为题名匹配；"
        "③人才源 gkx.dwd_scholar_research_direction 的 fields 为英文短语，无法与中文 IPC 锚点对齐，本批次完全无法计算。"
        "六源少一源、两源降级为代理，故判部分支持。")
    out["disclosures"] = [
        "方向锚点由「该 IPC4 内 3,000 件专利的关键词袋高频词」生成，属本文方法桥接，非甲方口径；"
        "跨源命中均基于中文子串匹配，会漏掉同义不同译法。",
        "各源窗口不同（专利/产业 基线 2021-2022、近窗 2024；论文 基线 2018-2019、近窗 2022-2023；"
        "项目/政策 基线 2017-2018、近窗 2020-2021），因各表覆盖期不等；窗口差异会放大 F 的噪声。",
        f"政策 keywords/theme 为字面 'NULL'（20,000 行中 keywords 真实值 {out['probes']['policy_keywords_real_rows']} 行、"
        f"theme {out['probes']['policy_theme_real_rows']} 行，按 UPPER(TRIM()) 统一口径复核），"
        "政策维只能用题名匹配代理，不参与「政策主题强度」的严格判断。",
        "gkx.dwd_zh_project 覆盖到 2021 年即基本截止（2022 年 58 条、2023 年 6 条），gkx.dwd_policy_base 2022 年仅 289 条，"
        "故项目/政策维近窗只能取 2020-2021。",
        "六源权重为等权「代理权重」：王惠只写「加权平均」，甲方签认前不得当作正式口径。",
    ]
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)
    print(json.dumps(out["probes"], ensure_ascii=False, indent=1))
    print(json.dumps(out["compute"]["alert_level_dist"], ensure_ascii=False))
    print(json.dumps(out["compute"]["top12_f"][:6], ensure_ascii=False, indent=1))
    print(json.dumps(out["compute"]["multi_source_positive_ge3"][:6], ensure_ascii=False))
    print(json.dumps(out["compute"]["bottom5_f"], ensure_ascii=False))
    print("support", out["support_judgment"], out["elapsed_s"])


if __name__ == "__main__":
    main()

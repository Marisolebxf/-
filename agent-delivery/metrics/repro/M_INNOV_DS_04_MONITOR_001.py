#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""创新点发现（M_INNOV_DS_04_MONITOR_001）—— 词条级突现监测 · **列表视角**

重建背景：原稿读的是 20261020 目录下的共享 bundle，而产出该 bundle 的脚本连的是
演示库、并用 `.get(y, 0)` 把 2017—2020 补成 0（DATA_FACTS §3.19）。本文的数字
全部本脚本现算，输入只有 `code/_snapshots21/` 下的 gkx 导出缓存，零 SQL、零 bundle。

口径（与 M_INNOV_POINT_DISCOVERY 同一套，不得另起）：
  词条 = IPC 小类（`main_classification_ipcr` 前 4 位）/ 专利关键词 / 中文论文关键词
  burst = (近窗年均 − 基窗年均) / max(基窗年均, 1)
  is_new = 首次出现年 ≥ T−2（T=2024）
  候选 = (burst ≥ 1 或 is_new) 且 近窗合计 ≥ 3
  基窗：公式要 2017—2021，库内只有 2021；缺失年不进分母（§3.16）

产物：code/M_INNOV_DS_04_MONITOR_001_out.json
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import _a25_common as A          # 关键词面板（6.80% 切片 / 论文分类子集）
import _ds04_common as D         # IPC 全量面板 + 口径常量 + 数值工具

METRIC = "M_INNOV_DS_04_MONITOR_001"
MIN_RECENT = 3
MIGRATION_PREFIX = ("H10", "B64U")


def score_terms(counts: dict, available, kind: str) -> dict:
    rows = []
    for term, yc in counts.items():
        st = D.window_stats(yc, D.BASE_FORMULA, D.RECENT, available)
        if st["recent_total"] < MIN_RECENT:
            continue
        st["is_new"] = 1 if (st["t0"] is not None and st["t0"] >= D.T - 2) else 0
        st["candidate"] = 1 if (st["burst"] >= 1 or st["is_new"]) else 0
        st["term"] = term
        st["point_type"] = kind
        st["year_counts"] = {str(y): yc[y] for y in sorted(yc)}
        rows.append(st)
    cand = [r for r in rows if r["candidate"]]
    cand.sort(key=lambda r: (-r["burst"], -r["recent_total"], r["term"]))
    return {
        "n_terms_scored": len(rows),
        "n_candidates": len(cand),
        "n_new": sum(1 for r in rows if r["is_new"]),
        "n_base_mean_zero": sum(1 for r in cand if r["b_mean"] <= 0),
        "n_genuine_burst": sum(1 for r in cand if r["b_mean"] > 0 and r["burst"] >= 1),
        "candidate_rate": round(len(cand) / max(len(rows), 1), 4),
        "burst_dist": D.dist([r["burst"] for r in rows]),
        "recent_total_dist": D.dist([r["recent_total"] for r in cand]),
        "rows": cand,
    }


def list_view(ipc_cand: list) -> dict:
    """列表视角：一行一个词条 + 展示层分层规则。

    前端只有一屏，33 个候选可以一次给全；分层是为了把「码迁移」「基窗退化」两类
    不可信候选压到二级页，而不是把阈值继续抬高（抬高会漏掉真实早期信号）。
    """
    out = []
    for i, r in enumerate(ipc_cand, 1):
        mig = r["term"].startswith(MIGRATION_PREFIX)
        degenerate = r["b_mean"] <= 0
        if mig:
            tier = "D_migration"
        elif degenerate:
            tier = "C_new_term"
        elif r["recent_total"] >= 30:
            tier = "A_solid"
        else:
            tier = "B_thin"
        out.append({
            "rank": i,
            "point_type": "ipc4",
            "point_key": r["term"],
            "burst": r["burst"],
            "is_new": r["is_new"],
            "first_year": r["t0"],
            "recent_total": r["recent_total"],
            "base_mean": r["b_mean"],
            "base_years_used": r["base_years_used"],
            "year_counts": r["year_counts"],
            "migration_flag": 1 if mig else 0,
            "degenerate_base_flag": 1 if degenerate else 0,
            "tier": tier,
        })
    tiers = {}
    for r in out:
        tiers[r["tier"]] = tiers.get(r["tier"], 0) + 1
    return {
        "page_size_suggest": 30,
        "n_rows": len(out),
        "tier_counts": tiers,
        "tier_rule": ("A_solid: 非迁移 & 基窗均值>0 & 近窗≥30；B_thin: 非迁移 & 基窗均值>0 & 近窗<30；"
                      "C_new_term: 基窗均值=0（burst 退化为近窗年均）；D_migration: H10x/B64U 码迁移"),
        "rows": out,
    }


def migration_audit(ipc_cand: list) -> dict:
    mig = [r for r in ipc_cand if r["term"].startswith(MIGRATION_PREFIX)]
    rest = [r for r in ipc_cand if not r["term"].startswith(MIGRATION_PREFIX)]
    return {
        "n_candidates": len(ipc_cand),
        "n_migration": len(mig),
        "migration_terms": [r["term"] for r in mig],
        "n_after_exclusion": len(rest),
        "top_after_exclusion": [(r["term"], r["burst"], r["recent_total"]) for r in rest[:10]],
        "note": ("2023.01 版 IPC 把半导体器件从 H01L 拆到 H10 族、把无人机从 B64C 拆到 B64U；"
                 "同期 H01L 6,789→4,097→1,004→0、B64C 569→180→146→30，属编码迁移不是技术突现"),
    }


def main():
    t_start = time.time()
    ipc = D.ipc_year()
    years_pat = sorted({y for yc in ipc.values() for y in yc})
    tp = A.term_panel()
    p_year_all = A.paper_year_all()
    years_paper = sorted(y for y in p_year_all if p_year_all[y] > 0)

    ipc_res = score_terms(ipc, years_pat, "ipc4")
    kwp_res = score_terms(tp["kwp"], years_pat, "keyword_patent")
    kwa_res = score_terms(tp["kwa"], years_paper, "keyword_paper")

    # 敏感性：T 推到 2025（近窗 2023—2025），检验 IPC4 排序是否由单年波动撑起
    def rank_for(recent):
        m = {}
        for term, yc in ipc.items():
            st = D.window_stats(yc, D.BASE_FORMULA, recent, years_pat)
            if st["recent_total"] >= MIN_RECENT:
                m[term] = st["burst"]
        return m

    a = rank_for(D.RECENT)
    b = rank_for((2023, 2024, 2025))
    common = [k for k in a if k in b]
    rho = D.spearman([a[k] for k in common], [b[k] for k in common]) if len(common) > 10 else None

    ss = A.sample_stats()
    out = {
        "metric_id": METRIC,
        "name": "创新点发现",
        "vendor_metric": "M_INNOV_POINT_DISCOVERY",
        "formula_owner": "王惠",
        "view": "list",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "runtime_sec": None,
        "data_source": ("gkx.dwd_patent（IPC 小类全量缓存 2,420,915 件 + 关键词主键切片 200,000 行）、"
                        "gkx.dwd_zh_paper_classification（20,048 篇）"),
        "db": "gkx @ 183.240.141.251:3318（只读，本脚本零 SQL，全部读 code/_snapshots21/ 缓存）",
        "definition": ("词条级突现检测：burst=(近窗年均−基窗年均)/max(基窗年均,1)，"
                       "is_new=首次出现年≥T−2，候选=(burst≥1 或 is_new)且近窗合计≥3；"
                       "输出是一行一个词条的清单，不是 0—100 分。"),
        "statistical_year": D.T,
        "windows": {"recent": list(D.RECENT), "base_formula": list(D.BASE_FORMULA),
                    "base_used": list(D.BASE_USED_PATENT)},
        "params": {"min_recent_count": MIN_RECENT, "burst_threshold": 1.0,
                   "migration_prefix": list(MIGRATION_PREFIX)},

        # ---- 硬约束：基期三字段进顶层 ----
        "base_years_used": list(D.BASE_USED_PATENT),
        "base_years_missing": list(D.BASE_MISSING_PATENT),
        "base_years_note": D.BASE_NOTE,

        "family": {
            "group": "M_INNOV_DS_04（科技发展态势·全球创新监测）",
            "this": "MONITOR_001 = 词条级突现监测的**列表视角**（一行一个候选词条）",
            "sibling": {
                "M_INNOV_DS_04_MONITOR_002": "同一批词条的**详情视角**（新颖性/影响潜力/成熟度三维价值分）",
                "M_INNOV_DS_04_REALTIME_004": "节点级（机构/IPC 领域）产出规模与影响分——实体是节点，不是词条",
                "M_INNOV_DS_04_REALTIME_005": "在上者年序列上的 Holt 外推——本库样本期不足，未发射预测",
            },
            "shared_key": "point_type + point_key（MONITOR_002 逐条消费本件候选）",
        },

        "probes": {
            "ipc_full": {"patents_with_ipc": sum(sum(v.values()) for v in ipc.values()),
                         "n_ipc4": len(ipc), "years": years_pat},
            "patent_sample": {"rows": ss["n"], "share": ss["meta"]["share"],
                              "kw_share": ss["kw_share"], "ipc_share": ss["ipc_share"],
                              "grant_rate": ss["grant_rate"]},
            "paper_keywords": {"papers_classified": len(A.papers()),
                               "papers_total": sum(p_year_all.values()),
                               "share": round(len(A.papers()) / max(sum(p_year_all.values()), 1), 4),
                               "year_counts": {str(y): p_year_all[y] for y in years_paper if y >= 2017}},
            "paper_id_join": A.paper_id_join(),
            "patent_year_total": {str(y): n for y, n in sorted(A.year_full().items())},
        },
        "probes_migration": None,
        "result": {
            "ipc4": {k: v for k, v in ipc_res.items() if k != "rows"},
            "keyword_patent": {k: v for k, v in kwp_res.items() if k != "rows"},
            "keyword_paper": {k: v for k, v in kwa_res.items() if k != "rows"},
        },
        "list_view": list_view(ipc_res["rows"]),
        "sensitivity": {
            "primary_window": {"recent": list(D.RECENT), "n": len(a)},
            "alt_window": {"recent": [2023, 2024, 2025], "n": len(b)},
            "n_common": len(common),
            "spearman_burst": rho,
            "note": ("2025 年入库 440,401 件（低于 2023/2024 的 60 万级，含公开滞后），"
                     "该窗口只作敏感性对照，不作主口径"),
        },

        "quarantine_delta": {
            "why": ("隔离前旧稿读 20261020 目录的共享 bundle，该 bundle 连演示库并用 .get(y,0) "
                    "把 2017—2020 补成 0，把 burst 抬了一个量级（DATA_FACTS §3.19）"),
            "old_vs_new": [
                {"item": "IPC4 词条数", "old": 42963, "new": len(ipc),
                 "cause": "旧稿把 IPC 大组（如 B08B1/12）当词条；本件按 IPC 小类前 4 位（B08B1）"},
                {"item": "突现候选数", "old": 24423, "new": ipc_res["n_candidates"],
                 "cause": "旧稿近窗/基窗都以补零序列计算，2021 年首现的码批量进「新主题」分支"},
                {"item": "burst 最大值", "old": 132.53, "new": ipc_res["burst_dist"]["max"],
                 "cause": "旧稿分母是 2017—2021 五年均值、其中四年是 0，分母被摊薄到 1/5"},
                {"item": "burst 最大者", "old": "B08B1/12", "new": ipc_res["rows"][0]["term"],
                 "cause": "同上；本件最大值是 H10F（半导体新码），且已被码迁移审计标记"},
                {"item": "Top 首现年分布", "old": "Top30 中 29 个为 2021", "new": "见 result.ipc4.n_new",
                 "cause": "本件把「2021 年有件数」与外推前的真实年份区分开，只有 2021 为 0 才是新"},
            ],
        },
        "support_judgment": "部分支持",
        "support_basis": (
            "IPC 小类词条为全量（2,420,915 件有 IPC、634 个小类），burst 与 is_new 可直接算；"
            "但（1）专利关键词只有主键切片 200,000 行（6.80%），件数是样本口径；"
            "（2）论文关键词只有分类子集 20,048 篇、其中 799 篇能拿到年份；"
            "（3）基窗公式要 2017—2021，库内只有 2021 一年，burst 分母退化为单年值；"
            "（4）33 个 IPC4 候选里 9 个是 2023 版 IPC 改版拆出的新码，属编码迁移。"),
        "reasons": [
            "IPC4 全量：634 个小类 / 2,420,915 件，无抽样，可逐词条复核逐年件数；",
            "专利关键词 6.80% 切片：全表 GROUP BY keywords 会跑满 600 秒断连（§3.6/§3.12），"
            "按铁律不扫，故关键词侧件数是样本计数，比值可用、绝对值不可外推；",
            "基窗 2017—2020 在 dwd_patent 零行：base_years_used=[2021]，"
            "凡 2021 年为 0 的词条 burst 退化为近窗年均（本件 %d 个候选属此）；"
            % ipc_res["n_base_mean_zero"],
            "论文分类表与论文主表 id 连通率 3.99%%（799/20,048），论文侧时间轴只剩 799 篇，"
            "最后只剩 %d 个候选，不足以成维；" % kwa_res["n_candidates"],
            "9 个候选命中 2023 版 IPC 码迁移（H10 族与 B64U），必须在列表页单列，不能计入技术突现。",
        ],
        "notes": [
            "本脚本零 SQL：IPC 面板、关键词切片、论文分类表全部读 code/_snapshots21/ 缓存。",
            "不引用任何共享结果文件（无 reused_from），四个 DS_04 件的 out.json 各由本目录 py 现算。",
            "2026 年（74,810 件）为残年，不进近窗；2025 年只用于敏感性对照。",
            "候选清单不是热度排行榜：burst 高值里混有码迁移与基窗退化两类伪信号，见 list_view.tier_rule。",
        ],
    }
    out["probes_migration"] = migration_audit(ipc_res["rows"])
    out["runtime_sec"] = round(time.time() - t_start, 1)

    p = D.write_out(METRIC, out)
    print("written", p)
    for k in ("ipc4", "keyword_patent", "keyword_paper"):
        r = out["result"][k]
        print(k, "scored", r["n_terms_scored"], "cand", r["n_candidates"],
              "new", r["n_new"], "burst_max", r["burst_dist"].get("max"),
              "median", r["burst_dist"].get("median"))
    print("migration", out["probes_migration"]["n_migration"],
          "after", out["probes_migration"]["n_after_exclusion"])
    print("spearman", rho, "n", len(common))
    print("tiers", out["list_view"]["tier_counts"])


if __name__ == "__main__":
    main()

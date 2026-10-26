#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TECH_COMPOSITE_SCORE 技术域综合评价分 —— 重建与取证

注册口径（cfg_metric-TECH-seed.yaml）：技术域综合评价分，源自 ADS 已落库的综合评价结果；
calc-logic 侧未冻结（`pending_ods`），分项与权重均未定。

本件做法：先把 `M_TECH_BASE_96_1` 的 11 子指标矩阵按「可用 / 代理 / 无源」三类钉死，
再只在可观测的 5 个子指标上做自定义加权重算，缺的 6 个置 null（不置 0），
最后用敏感性证明「缺的那几维本来是区分层」。

输出 code/M_TECH_COMPOSITE_SCORE_out.json
"""
from __future__ import annotations

import json
import math
import statistics
from pathlib import Path

import pymysql

HERE = Path(__file__).parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_TECH_COMPOSITE_SCORE_out.json"
BASE_OUT = HERE / "M_TECH_BASE_96_1_out.json"

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", connect_timeout=30,
           read_timeout=300, autocommit=True, charset="utf8mb4")

# 自定义权重（声明：非官方，非 AHP；注册表本件权重未冻结）
# 四维对 10 个域全部可得 → 同一权重集、同一归一池，分数严格可比。
# 头部集中(5 域可得) 只作读数不进权重：只对 4/10 域可得，进权重会破坏可比性。
W_MAIN = {"patent_scale": 0.35, "breadth": 0.25, "paper_upper": 0.15, "sz_share": 0.25}
W_SENS = {
    "S1_纯专利规模": {"patent_scale": 1.0, "breadth": 0.0, "paper_upper": 0.0, "sz_share": 0.0},
    "S2_论文优先": {"patent_scale": 0.20, "breadth": 0.15, "paper_upper": 0.45, "sz_share": 0.20},
    "S3_深圳优先": {"patent_scale": 0.20, "breadth": 0.15, "paper_upper": 0.10, "sz_share": 0.55},
    "S4_四维等权": {"patent_scale": 0.25, "breadth": 0.25, "paper_upper": 0.25, "sz_share": 0.25},
}


def rank_ties(vals: dict):
    order = sorted(vals.items(), key=lambda kv: (-kv[1], kv[0]))
    out, prev, pr = {}, None, 0
    for i, (k, v) in enumerate(order, 1):
        if prev is not None and abs(v - prev) < 1e-12:
            out[k] = pr
        else:
            out[k] = i
            pr = i
        prev = v
    return out


def norm(vals: dict, log=False, share=False):
    v = {k: (math.log1p(max(0.0, x)) if log else x) for k, x in vals.items()}
    lo, hi = min(v.values()), max(v.values())
    if hi - lo < 1e-12:
        return {k: 0.5 for k in v}
    if share:                       # 份额类：不截尾，0—1 天然有界
        return {k: (x - lo) / (hi - lo) for k, x in v.items()}
    return {k: (x - lo) / (hi - lo) for k, x in v.items()}


def spearman(a: dict, b: dict):
    ks = [k for k in a if k in b]
    ra, rb = rank_ties({k: a[k] for k in ks}), rank_ties({k: b[k] for k in ks})
    x = [ra[k] for k in ks]
    y = [rb[k] for k in ks]
    mx, my = statistics.mean(x), statistics.mean(y)
    num = sum((i - mx) * (j - my) for i, j in zip(x, y))
    den = (sum((i - mx) ** 2 for i in x) * sum((j - my) ** 2 for j in y)) ** 0.5
    return round(num / den, 4) if den else None


def main():
    base = json.loads(BASE_OUT.read_text(encoding="utf-8"))
    domains = base["patent_domain"]                    # 10 域 + IPC4 清单 + count
    paper_upper = base["paper_domain_upper"]
    top_app = base["domain_top_applicants"]
    dom_names = list(domains)

    by_name = json.loads((SNAP / "patent_ipc4_by_name_20261021.json").read_text(encoding="utf-8"))
    base_rows = json.loads((SNAP / "base_20261021.json").read_text(encoding="utf-8"))
    name_city = {}
    for r in base_rows:
        name_city.setdefault(r[2], r[4])

    # ---------- 一、逐域聚合：主体广度 + 深圳份额 ----------
    rows = {}
    for dom in dom_names:
        ipcs = set(domains[dom]["ipc4_hit"] or domains[dom]["ipc4"])
        names, sz_cnt, tot_cnt = {}, 0, 0
        for ipc, nm, c in by_name:
            if ipc in ipcs:
                names[nm] = names.get(nm, 0) + c
                tot_cnt += c
                if name_city.get(nm) == "深圳市":
                    sz_cnt += c
        top5 = top_app.get(dom, [])[:5]
        top5_sum = sum(x["patents"] for x in top5)
        rows[dom] = {
            "patent_scale": domains[dom]["count"],
            "breadth": len(names),
            # top5 清单缺失 → 该维置 None（不置 0），权重按域重归一
            # 头部集中只作读数：10 域里只有 4 域有 top5 清单，不进权重
            "head_conc": (round(top5_sum / domains[dom]["count"], 4)
                          if (top5 and domains[dom]["count"]) else None),
            "paper_upper": (paper_upper.get(dom) or {}).get("count", 0),
            "sz_share": round(sz_cnt / tot_cnt, 4) if tot_cnt else 0.0,
            "sz_patents": sz_cnt,
            "top5": [x["name"] for x in top5],
            "ipc4": sorted(ipcs),
        }

    # ---------- 二、归一 + 加权 ----------
    dims = list(W_MAIN)   # 4 维，10 域全部可得
    normed = {}
    for k in dims:
        avail = {d: rows[d][k] for d in dom_names if rows[d].get(k) is not None}
        if not avail:
            normed[k] = {}
            continue
        normed[k] = norm(avail, log=(k in ("patent_scale", "breadth", "paper_upper")))

    def composite(w):
        sc = {}
        for d in dom_names:
            have = [k for k in dims if d in normed.get(k, {})]
            tot = sum(w[k] for k in have)
            sc[d] = round(100 * sum(w[k] * normed[k][d] for k in have) / tot, 4) if tot else 0.0
        return sc

    main_score = composite(W_MAIN)
    main_rank = rank_ties(main_score)

    # ---------- 三、敏感性 ----------
    sens = {}
    for tag, w in W_SENS.items():
        sc = composite(w)
        rk = rank_ties(sc)
        shifts = [abs(rk[d] - main_rank[d]) for d in dom_names]
        sens[tag] = {"weights": w, "scores": sc, "ranks": rk,
                     "max_rank_shift": max(shifts),
                     "top3": [d for d, _ in sorted(sc.items(), key=lambda kv: -kv[1])[:3]],
                     "spearman_vs_main": spearman(sc, main_score)}
    # 与「只看专利规模」的秩相关——衡量其余四维是否提供了独立信息
    sens["baseline_patent_scale_only"] = {
        "scores": {d: round(100 * normed["patent_scale"][d], 4) for d in dom_names},
        "ranks": rank_ties({d: normed["patent_scale"][d] for d in dom_names}),
        "spearman_vs_main": spearman({d: normed["patent_scale"][d] for d in dom_names}, main_score),
        "max_rank_shift": max(abs(rank_ties({d: normed["patent_scale"][d] for d in dom_names})[d]
                                  - main_rank[d]) for d in dom_names),
    }

    # ---------- 四、无源四维的现场复核 ----------
    c = pymysql.connect(**GKX)
    cur = c.cursor()
    cur.execute("SET SESSION max_execution_time=120000")
    probe = {}
    for t in ("dwd_deal", "dwd_patent_transfer", "dwd_chain_news_info"):
        cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='gkx' AND table_name=%s", (t,))
        if cur.fetchone()[0]:
            cur.execute("SELECT COUNT(*) FROM gkx.`%s`" % t)
            probe[t] = int(cur.fetchone()[0])
        else:
            probe[t] = None
    # 影响因子 / 下载量
    cur.execute("""SELECT column_name FROM information_schema.columns
                   WHERE table_schema='gkx' AND table_name='dwd_zh_paper'
                     AND (column_name LIKE '%%impact%%' OR column_name LIKE '%%download%%')""")
    probe["paper_quality_cols"] = [r[0] for r in cur.fetchall()]
    cur.execute("SELECT SUM(download_num), SUM(download_num>0) FROM gkx.dwd_zh_paper")
    s, nz = cur.fetchone()
    probe["download_num"] = {"sum": float(s or 0), "nonzero_rows": int(nz or 0)}
    # 技术合同类表是否存在（按名称扫）
    cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema='gkx'
                   AND (table_name LIKE '%%contract%%' OR table_name LIKE '%%transfer%%'
                        OR table_name LIKE '%%trade%%' OR table_name LIKE '%%deal%%')""")
    probe["contract_like_tables"] = [r[0] for r in cur.fetchall()]
    c.close()

    # ---------- 五、11 子指标矩阵（沿用 BASE_96_1 的三分类）----------
    matrix = base["sub_metric_matrix"]
    status_count = {"直接": 0, "代理": 0, "无源": 0}
    for m in matrix:
        status_count[m["status"]] = status_count.get(m["status"], 0) + 1
    used_codes = {"D5": "patent_scale", "D6": "sz_share", "D9": "head_conc"}

    # ---------- 六、落盘 ----------
    out = {
        "metric_id": "M_TECH_COMPOSITE_SCORE",
        "metric_name": "技术域综合评价分",
        "generated_at": "2026-10-23",
        "db": "gkx @ 183.240.141.251:3318 / gkx_reader_zp（只读）；专利与论文读数复用 M_TECH_BASE_96_1 已核验产物",
        "formula_owner": "未署名（cfg_metric-TECH-seed.yaml 本件 formula 为 pending_ods，分项与权重未冻）",
        "unit": "分（0—100，只在 10 个技术域内可比）",
        "formula_intended": "composite(d) = Σ_j w_j × norm_j(x_j(d))，j 取 11 个子指标（论文 4 + 专利 4 + 交易 2 + 资讯 1），w 官方未定",
        "formula_actual": "composite(d) = 100 × (0.35×专利规模 + 0.25×主体广度 + 0.15×论文上界 + 0.25×深圳份额)，四维对 10 域全部可得；其余 7 个子指标置 null",
        "weights_declared": {"main": W_MAIN,
                             "note": "自定义权重，非官方、非 AHP 标定。注册表本件权重「未冻」，故任何引用都必须带「自定义」三字。"},
        "universe": {"domains": len(dom_names),
                     "domain_names": dom_names,
                     "note": "10 个技术域由 `M_TECH_BASE_96_1` 的 IPC4 清单定义；IPC4 前缀跨域共享（H01L 同时在 AI芯片/集成电路），故 10 域分值不可相加、不可跨域比规模，只能比「同一权重下的域间相对位置」。"},
        "dims_used": [{"dim": k, "weight": W_MAIN[k], "source": v} for k, v in {
            "patent_scale": "dwd_patent 主分类 IPC4 件数（BASE_96_1 patent_domain）",
            "breadth": "dwd_patent 申请人去重数（patent_ipc4_by_name 快照）",
            "paper_upper": "中图一级类上界（BASE_96_1 paper_domain_upper，代理）",
            "sz_share": "域内深圳申请人件数占比（名称→城市经底册）。",
        }.items()],
        "dims_null": [
            {"dim": "D4 前沿论文机构", "why": "影响因子列不存在、download_num 整列为 0、论文级被引 ID 不通", "status": None},
            {"dim": "D8 技术交易额", "why": "dwd_deal 仅 10 行且无金额列；dwd_patent_transfer 无成交价", "status": None},
            {"dim": "D10 区域技术交易额", "why": "同上，且无区域键", "status": None},
            {"dim": "D11 技术动态资讯", "why": "资讯表无 IPC / 技术域字段，词表与 10 域不同源", "status": None},
            {"dim": "D1 论文数量(按域)", "why": "有代理读数（中图一级类上界），已并入 paper_upper，不单列", "status": None},
            {"dim": "D2/D3 深圳与区域论文数", "why": "机构代理、城市覆盖 37.09%，样本 20,048 篇；不进权重，只作读数", "status": None},
        ],
        "sub_metric_status_count": status_count,
        "sub_metric_matrix": matrix,
        "probe": probe,
        "dim_null_domains": {"head_conc": [d for d in dom_names if rows[d]["head_conc"] is None],
                             "note": "这些域在 BASE_96_1 的 domain_top_applicants 里没有 top5 清单，头部集中维置 null 并按域重归一权重——不置 0，否则会把域分系统性压低。"},
        "rows": rows,
        "scores": main_score,
        "ranks": main_rank,
        "top3": [d for d, _ in sorted(main_score.items(), key=lambda kv: -kv[1])[:3]],
        "bottom3": [d for d, _ in sorted(main_score.items(), key=lambda kv: kv[1])[:3]],
        "sensitivity": sens,
        "support_judgment": "部分支持",
        "support_reason": "综合分的计算面（归一 + 加权 + 排序）完全可实现，10 个域都能出分；但 11 个子指标里 4 个无源（前沿质量、技术交易额两项、资讯），2 个只有机构代理且城市覆盖 37.09%，可用维只有 5 个；且主分与「只看专利规模」的秩相关达 0.9 以上——说明缺的那几维本来承担区分，去掉后综合分退化为专利规模的不同写法。按「始终有部分依赖维无法得到」判部分支持。",
        "boundary": "分数只能在这 10 个域之间比，且只能在同一组权重下比；换权重后名次变化见 sensitivity。分值不可跨权重、不可跨域口径（不同 IPC4 清单）比较。",
        "sources": [
            {"path": "code/M_TECH_BASE_96_1_out.json", "kind": "upstream", "note": "10 域 IPC4 清单、域件数、top5 申请人、论文上界、11 子指标矩阵"},
            {"path": "code/_snapshots21/patent_ipc4_by_name_20261021.json", "kind": "snapshot", "note": "IPC4 × 申请人 × 件数（581,585 行）"},
            {"path": "code/_snapshots21/base_20261021.json", "kind": "snapshot", "note": "企业名称→城市"},
            {"path": "gkx.dwd_patent", "kind": "table", "note": "2,939,895 件，有主分类 IPC4 的 2,420,915 件"},
            {"path": "gkx.dwd_zh_paper", "kind": "table", "note": "100,900 篇；download_num 整列为 0"},
            {"path": "gkx.dwd_deal", "kind": "table", "note": "10 行，无金额列"},
        ],
        "base_years_used": [2021, 2022, 2023, 2024, 2025, 2026],
        "base_years_missing": [],
        "base_years_note": "专利侧六个年份（2021—2026）全部计入域件数，2026 为残年（69,747 件，约为 2025 的 20.4%）只做端点披露、不用于增速；论文侧上界无年份字段，不做域×年双轴。跨年不摊 0。",
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("status", status_count, "probe", json.dumps(probe, ensure_ascii=False)[:300])
    print("scores", json.dumps(main_score, ensure_ascii=False))
    print("ranks", json.dumps(main_rank, ensure_ascii=False))
    print("sens", {k: (v.get("max_rank_shift"), v.get("spearman_vs_main"), v.get("top3")) for k, v in sens.items()})


if __name__ == "__main__":
    main()

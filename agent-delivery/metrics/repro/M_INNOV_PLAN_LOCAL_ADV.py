#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_PLAN_LOCAL_ADV —— 本地科技创新特色与优势（三方库 gkx 版，专利零 SQL）。

王惠三维区位商，对象 = IPC4，本地 = 深圳：
  LQ_patent    = (深圳该方向专利 / 深圳专利) / (全池该方向专利 / 全池专利)
  LQ_resource  = (深圳该方向活跃申请人 / 深圳申请人) / (全池该方向申请人 / 全池申请人)
  LQ_paper     = (深圳该方向论文 / 深圳论文) / (全池该方向论文 / 全池论文)
合成 = 可得维几何平均；归一 = 除以截面几何均值；LQ_norm>1 记优势。

数据：专利来自 `patent_scan_20261021.pkl`（城市×年×IPC4 pn 集合）与
`patent_ipc4_year_20261021.json`（全量）；申请人来自 `patent_ipc4_by_name_20261021.json`
× 底册名称→城市；论文 1 条 SQL（2021—2024，52,000 行级小表）。
"""
from __future__ import annotations

import math
import time

import _gkxdb as D
import _plan21_common as C

METRIC = "M_INNOV_PLAN_LOCAL_ADV"
CITY = "深圳"
YEARS = (2021, 2022, 2023, 2024)
MIN_POOL = 100  # 方向稳定性门槛：池内 2021—2024 专利 ≥100 件
MIN_APP = 20    # 资源维稳定性门槛：池内该方向申请人 ≥20 个
MIN_PAPER = 20  # 论文维稳定性门槛：池内该方向论文 ≥20 篇
T0 = time.time()


def q(sql: str) -> list[tuple]:
    cur = D.gkx()
    try:
        cur.execute("SET SESSION max_execution_time=60000")
        cur.execute(sql)
        return list(cur.fetchall())
    finally:
        cur.close()


def safe_div(a, b):
    return a / b if b else 0.0


def main() -> None:
    # ---------- 分母：全池（2021—2024，全部有 IPC 的专利） ----------
    d = C.ipc4_year()
    pool: dict[str, int] = {}
    for ipc, y in {(k[0], k[1]) for k in d}:
        if y in YEARS:
            pool[ipc] = pool.get(ipc, 0) + d.get((ipc, y), [0, 0])[0]
    dirs = sorted(i for i, v in pool.items() if v >= MIN_POOL)
    pool_total = sum(pool[i] for i in dirs)

    # ---------- 专利维：深圳 ----------
    cip = C.city_ipc_pn()
    sz: dict[str, int] = {}
    for (city, y, ipc), pns in cip.items():
        if city == CITY and y in YEARS:
            sz[ipc] = sz.get(ipc, 0) + len(pns)
    sz_total = sum(sz.get(i, 0) for i in dirs)

    # ---------- 资源维：活跃申请人（按名称去重） ----------
    nm2city, n_conflict = C.name_city()
    all_app: dict[str, set] = {i: set() for i in dirs}
    sz_app: dict[str, set] = {i: set() for i in dirs}
    matched_names = 0
    for ipc, nm, cnt in C.ipc4_by_name():
        if ipc not in all_app:
            continue
        all_app[ipc].add(nm)
        c = nm2city.get(nm)
        if c:
            matched_names += 1
            if c.startswith(CITY):  # 底册 city 为「深圳市」全称
                sz_app[ipc].add(nm)
    all_app_total = sum(len(v) for v in all_app.values())
    sz_app_total = sum(len(v) for v in sz_app.values())

    # ---------- 论文维：1 条 SQL ----------
    pap_rows = q("""SELECT zh_name, en_name, author_info_list FROM gkx.dwd_zh_paper
                    WHERE LEFT(CAST(cover_year_start AS CHAR),4) IN ('2021','2022','2023','2024')""")
    all_pap: dict[str, int] = {i: 0 for i in dirs}
    sz_pap: dict[str, int] = {i: 0 for i in dirs}
    pap_un = 0
    pap_sz = 0
    for r in pap_rows:
        top = C.assign_fast(((r[0] or "") + " " + (r[1] or "")).strip(), k=1)
        if not top:
            pap_un += 1
            continue
        ipc = top[0][0]
        if ipc not in all_pap:
            continue
        all_pap[ipc] += 1
        if CITY in str(r[2] or ""):
            sz_pap[ipc] += 1
            pap_sz += 1
    all_pap_total = sum(all_pap.values())
    sz_pap_total = sum(sz_pap.values())

    # ---------- 三维 LQ ----------
    rows = []
    for ipc in dirs:
        lq_p = safe_div(safe_div(sz.get(ipc, 0), sz_total), safe_div(pool[ipc], pool_total))
        lq_r = (safe_div(safe_div(len(sz_app[ipc]), sz_app_total), safe_div(len(all_app[ipc]), all_app_total))
                if len(all_app[ipc]) >= MIN_APP else None)
        lq_w = (safe_div(safe_div(sz_pap[ipc], sz_pap_total), safe_div(all_pap[ipc], all_pap_total))
                if all_pap[ipc] >= MIN_PAPER and sz_pap_total > 0 else None)
        dims = [x for x in (lq_p, lq_r, lq_w) if x and x > 0]
        comp = math.exp(sum(math.log(x) for x in dims) / len(dims)) if dims else None
        rows.append({
            "ipc4": ipc, "sz_patent": sz.get(ipc, 0), "pool_patent": pool[ipc],
            "sz_applicants": len(sz_app[ipc]), "pool_applicants": len(all_app[ipc]),
            "sz_papers": sz_pap[ipc], "pool_papers": all_pap[ipc],
            "lq_patent": round(lq_p, 4),
            "lq_resource": round(lq_r, 4) if lq_r else None,
            "lq_paper": round(lq_w, 4) if lq_w else None,
            "n_dims": len(dims), "lq_composite": round(comp, 4) if comp else None,
        })

    comps = [r["lq_composite"] for r in rows if r["lq_composite"]]
    geo_mean = math.exp(sum(math.log(x) for x in comps) / len(comps))
    for r in rows:
        r["lq_norm"] = round(r["lq_composite"] / geo_mean, 4) if r["lq_composite"] else None
    rows = [r for r in rows if r["lq_norm"] is not None]
    rows.sort(key=lambda r: -r["lq_norm"])
    vals = [r["lq_norm"] for r in rows]

    adv = [r for r in rows if r["lq_norm"] > 1]
    strong = [r for r in rows if r["lq_norm"] >= 1.5]
    # 劣势清单：体量足够（池内 ≥1000 件）以避免小样本噪声
    dis = sorted([r for r in rows if r["pool_patent"] >= 1000], key=lambda r: r["lq_norm"])[:10]
    pat_only_adv = sum(1 for r in rows if r["lq_patent"] > 1)

    out = {
        "metric_id": METRIC,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "db": {"host": "183.240.141.251:3318", "schema": "gkx",
               "tables": ["dwd_zh_paper"],
               "patent_source": "_snapshots21/patent_scan_20261021.pkl + patent_ipc4_year_20261021.json"
                                "（城市×年×IPC4 pn 集合，零专利 SQL）",
               "applicant_source": "_snapshots21/patent_ipc4_by_name_20261021.json × base_20261021.json"},
        "support_judgment": "部分支持",
        "judgment_reason": (
            "448 类方向可算出非退化 LQ（专利/申请人/论文三维），但需求要求的「与全球水平对比」在本库没有"
            "全球分母（现有分母是国内专利池，深圳占池 4 成以上是名称宇宙的结构性偏高）；"
            "创新资源维只能用活跃申请人代理，论文维依赖 Top-1 22.14% 的术语桥"
        ),
        "formula": {
            "lq": "LQ_d=(L_d/L_total)/(A_d/A_total)",
            "composite": "LQ_comp=几何平均(可得维)",
            "normalize": f"LQ_norm=LQ_comp/{round(geo_mean, 4)}（截面几何均值）",
            "threshold": "LQ_norm>1 优势；≥1.5 强优势；仅专利单维 LQ>1 作对照",
        },
        "base_years": C.base_year_block(
            used=list(YEARS), missing=[2017, 2018, 2019, 2020],
            note="专利/申请人/论文均取 2021—2024（dwd_patent 的 apdt_year 只有 2021—2026，"
                 "2017—2020 零行）；LQ 是同期份额比，不跨期，但不得把缺失年按 0 摊入任何趋势分母。"),
        "scope": {
            "city": CITY, "years": list(YEARS), "min_pool_patent": MIN_POOL,
            "n_directions": len(rows),
            "pool_patent_total": pool_total, "sz_patent_total": sz_total,
            "sz_share_of_pool": round(sz_total / pool_total, 4) if pool_total else None,
            "pool_applicant_total_distinct": all_app_total,
            "sz_applicant_total_distinct": sz_app_total,
            "sz_applicant_share": round(sz_app_total / all_app_total, 4) if all_app_total else None,
            "sz_applicant_name_matched": matched_names,
            "name_conflicts": n_conflict,
            "papers_rows": len(pap_rows), "papers_assigned": len(pap_rows) - pap_un,
            "papers_unassigned": pap_un,
            "papers_assigned_rate": round((len(pap_rows) - pap_un) / len(pap_rows), 4) if pap_rows else None,
            "sz_papers": pap_sz, "sz_paper_share": round(pap_sz / all_pap_total, 4) if all_pap_total else None,
            "disclosure": "深圳占池比例是「可回连底册的国内专利池」份额，不是全球份额；"
                          "底册 189,116 家中深圳 95,600 家（50.5%），分母本身结构性偏向本地。",
        },
        "result": {
            "distribution": C.st(vals),
            "geo_mean": round(geo_mean, 4),
            "n_advantage": len(adv), "n_strong": len(strong),
            "n_advantage_rate": round(len(adv) / len(rows), 4),
            "n_with_paper_dim": sum(1 for r in rows if r["lq_paper"]),
            "top20": rows[:20], "disadvantage_10": dis,
            "worst10_all": sorted(rows, key=lambda r: r["lq_norm"])[:10],
            "patent_only_advantage": pat_only_adv,
            "spearman_composite_vs_patent": C.spearman([r["lq_composite"] for r in rows],
                                                      [r["lq_patent"] for r in rows]),
            "top20_overlap_patent": len({r["ipc4"] for r in rows[:20]}
                                        & {r["ipc4"] for r in sorted(rows, key=lambda r: -r["lq_patent"])[:20]}),
            "all": rows,
        },
        "sql_count": 1,
        "elapsed_sec": None,
    }
    out["elapsed_sec"] = round(time.time() - T0, 1)
    C.write_out(METRIC, out)
    print(f"dirs={len(rows)} geo={geo_mean:.4f} adv={len(adv)} strong={len(strong)} "
          f"top1={rows[0]['ipc4']} {rows[0]['lq_norm']} sz_share={out['scope']['sz_share_of_pool']} "
          f"in {out['elapsed_sec']}s")


if __name__ == "__main__":
    main()

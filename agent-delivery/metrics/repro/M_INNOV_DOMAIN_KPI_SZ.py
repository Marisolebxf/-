#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_DOMAIN_KPI_SZ 深圳科技领域明细指标 · 20261021 改源版

口径（沿用 20261020 版，不重写公式）
------------------------------------
领域键 = 专利主分类 IPC4；对象 = 深圳机构（dwd_org_base_info.city 含「深圳」）。
四 KPI：企业数量（first_applicant_name 去重）、专利数量（pn 去重）、
研发投入（dwd_org_stock_finance_info.research_development_amount，无领域键）、
人才数量（dwd_scholar，无领域列）。后两列按深圳总量披露，领域内置 NULL。

本版只改数据源：旧演示库 → 三方库 gkx（演示库与 _devdb 一律禁引）。

工程约束（DATA_FACTS_gkx21 §3.6）
---------------------------------
gkx.dwd_patent 2,939,895 行、first_applicant_name 无索引；单条全表 JOIN 会被服务端
在约 2,400 秒杀死。故按 dwd_id 主键、30 万行一页流式读取（4 列、无 JOIN、无 GROUP BY），
城市归属与 IPC4 聚合全部在 Python 侧完成；每页落盘，可断点续跑。

运行：python3 code/M_INNOV_DOMAIN_KPI_SZ.py
"""
from __future__ import annotations

import json
import pickle
import pymysql
import time
from collections import defaultdict
from pathlib import Path

import _gkx21_common as C
import _gkxdb

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_snapshots21"
CACHE.mkdir(exist_ok=True)
STATE = CACHE / "domain_kpi_sz_patent_state.pkl"
META = CACHE / "domain_kpi_sz_patent_meta.json"

YEAR_LO, YEAR_HI = 2019, 2024
CHUNK = 300_000
TOP_N = 15
PLACEHOLDER = ("NULL", "", "NONE", "-")


def clean(v):
    """占位符统一清洗（DATA_FACTS §3.4）。"""
    if v is None:
        return ""
    s = str(v).strip()
    return "" if s.upper() in PLACEHOLDER else s


# ---------------------------------------------------------------- 深圳名册
def sz_names():
    """深圳机构名集合：直接从 gkx 主档缓存取（base_rows 已按 gkx 全量落盘）。"""
    base = C.base_rows()
    names = {clean(r[2]) for r in base if r[4] and "深圳" in str(r[4])}
    names.discard("")
    return names


# ---------------------------------------------------------------- 专利分页扫描
def build_patent_ipc4(force=False):
    """流式聚合「深圳第一申请人 × IPC4」。

    dwd_id 是 PRIMARY 但取值稀疏（1,524 ~ 41,406,094 撑 293.9 万行），
    按 id 区间或 OFFSET 分页都会退化成上万次探测，故改用**服务端流式游标**
    （SSCursor）+ 主键有序扫描：一次连接从头读到尾，fetchmany(50,000) 边读边算，
    每 50 万行落盘一次（记录 last_id 可断点续跑）。全程无 JOIN、无 GROUP BY。

    返回 {ipc4: {"pn": set, "nm": set}}；pn / nm 均为全局去重集合。
    """
    inv_rows = int(json.loads((HERE.parent / "_work_gkx21" / "GKX_INVENTORY.json")
                              .read_text(encoding="utf-8"))["dwd_patent"]["rows"])
    if STATE.exists() and not force:
        with STATE.open("rb") as f:
            st = pickle.load(f)
        if int(st.get("source_rows", -1)) == inv_rows and st.get("done"):
            return st["agg"], st
        print("[cache] 上次未读完，从 last_id=%s 续跑" % st.get("last_id"), flush=True)
        agg, last_id, rows0, kept0, chunks0 = st["agg"], st["last_id"], st["rows"], st["kept"], st["chunks"]
    else:
        agg = {}
        last_id, rows0, kept0, chunks0 = 0, 0, 0, 0

    names = sz_names()
    print("深圳机构名", len(names), flush=True)

    st = {"last_id": last_id, "chunks": chunks0, "rows": rows0, "kept": kept0,
          "source_rows": inv_rows, "agg": agg, "done": False,
          "started": time.strftime("%Y-%m-%dT%H:%M:%S")}

    def save():
        with STATE.open("wb") as f:
            pickle.dump(st, f, protocol=4)

    t_all = time.time()
    conn = pymysql.connect(cursorclass=pymysql.cursors.SSCursor, **{k: v for k, v in _gkxdb.GKX.items()
                                                                    if k != "cursorclass"})
    try:
        cur = conn.cursor()
        cur.execute("SET NAMES utf8mb4")
        cur.execute("SELECT dwd_id, pn, first_applicant_name, main_classification_ipcr "
                    "FROM gkx.dwd_patent WHERE dwd_id > %s AND apdt_year BETWEEN %s AND %s "
                    "ORDER BY dwd_id", (st["last_id"], YEAR_LO, YEAR_HI))
        while True:
            batch = cur.fetchmany(50_000)
            if not batch:
                break
            t = time.time()
            n_kept = 0
            for did, pn, nm, ipc in batch:
                st["rows"] += 1
                nm = clean(nm)
                if nm not in names:
                    continue
                ipc = clean(ipc)
                if len(ipc) < 4:
                    continue
                p = clean(pn)
                a = agg.setdefault(ipc[:4].upper(), {"pn": set(), "nm": set()})
                if p:
                    a["pn"].add(p)
                a["nm"].add(nm)
                n_kept += 1
            st["kept"] += n_kept
            st["last_id"] = int(batch[-1][0])
            st["chunks"] += 1
            if st["chunks"] % 1 == 0:
                save()
            print("  batch#%d last_id=%s rows=%d kept=%d %.1fs (total %.0fs)" %
                  (st["chunks"], st["last_id"], len(batch), n_kept,
                   time.time() - t, time.time() - t_all), flush=True)
        cur.close()
    finally:
        conn.close()

    st["done"] = True
    out = {k: {"pn": set(v["pn"]), "nm": set(v["nm"])} for k, v in agg.items()}
    st["agg"] = out
    save()
    META.write_text(json.dumps({"batches": st["chunks"], "rows": st["rows"], "kept": st["kept"],
                                "elapsed_sec": round(time.time() - t_all, 1)}, ensure_ascii=False),
                    encoding="utf-8")
    return out, st


# ---------------------------------------------------------------- 研发与人才
def rd_and_talent():
    """研发投入与人才：按深圳总量披露（两表均无领域键）。"""
    base = C.base_rows()
    sz_org = {r[0] for r in base if r[4] and "深圳" in str(r[4])}
    names = {clean(r[2]) for r in base if r[4] and "深圳" in str(r[4])}

    rows = C.qd("SELECT org_id, SUM(research_development_amount) s, COUNT(*) n "
                "FROM gkx.dwd_org_stock_finance_info "
                "WHERE LEFT(occur_period,4) BETWEEN %s AND %s "
                "  AND research_development_amount IS NOT NULL GROUP BY org_id",
                (str(YEAR_LO), str(YEAR_HI)))
    rd = 0.0
    rd_rows = rd_orgs = 0
    for r in rows:
        if r["org_id"] in sz_org:
            rd += float(r["s"] or 0)
            rd_rows += int(r["n"] or 0)
            rd_orgs += 1

    scholars = C.qd("SELECT scholar_id, scholar_org_name_zh nm FROM gkx.dwd_scholar")
    sids = {r["scholar_id"] for r in scholars if clean(r["nm"]) in names}
    return {"rd_total": round(rd, 2), "rd_rows": rd_rows, "rd_orgs": rd_orgs,
            "talent_total": len(sids), "scholar_rows": len(scholars)}


def main():
    t0 = time.time()
    inv = json.loads((HERE.parent / "_work_gkx21" / "GKX_INVENTORY.json").read_text(encoding="utf-8"))
    probes = {("gkx." + t): int(inv[t]["rows"]) for t in
              ("dwd_org_base_info", "dwd_patent", "dwd_org_stock_finance_info", "dwd_scholar")}

    base = C.base_rows()
    sz_n = sum(1 for r in base if r[4] and "深圳" in str(r[4]))
    agg, st = build_patent_ipc4()
    rt = rd_and_talent()

    top = sorted(((k, len(v["pn"]), len(v["nm"])) for k, v in agg.items()),
                 key=lambda x: (-x[1], x[0]))[:TOP_N]
    rows_out = [{"ipc4": k, "ent_cnt": ent, "patent_cnt": pat,
                 "rd_funding": None, "talent_cnt": None} for k, pat, ent in top]

    result = {
        "metric_id": "M_INNOV_DOMAIN_KPI_SZ",
        "metric_name": "深圳科技领域明细指标",
        "method": "bid 口径四 KPI（企业/专利/研发/人才）；领域键=IPC4；研发/人才无领域键→仅总量披露",
        "data_source": "gkx（三方库，只读）：dwd_patent / dwd_org_base_info / "
                       "dwd_org_stock_finance_info / dwd_scholar",
        "window": {"patent_apdt_year": [YEAR_LO, YEAR_HI],
                   "finance_occur_period_year": [YEAR_LO, YEAR_HI]},
        "probes": probes,
        "compute": {
            "top_ipc4": rows_out,
            "sz_total_rd_funding": rt["rd_total"],
            "sz_total_scholar": rt["talent_total"],
            "n_ipc4_covered": len(agg),
            "patent_scan": {"chunks": st["chunks"], "rows_scanned": st["rows"],
                            "rows_kept_sz": st["kept"],
                            "note": "按 dwd_id 主键 30 万行/页流式读取，Python 侧按 "
                                    "first_applicant_name∈深圳名册 + IPC4 聚合；无全表 JOIN"},
            "sz_entities": {"names": len({clean(r[2]) for r in base if r[4] and "深圳" in str(r[4])}),
                            "rows": sz_n, "org_ids": len({r[0] for r in base if r[4] and "深圳" in str(r[4])})},
            "rd_detail": {"rows": rt["rd_rows"], "orgs": rt["rd_orgs"]},
            "talent_detail": {"scholar_rows": rt["scholar_rows"], "matched_sz": rt["talent_total"]},
            "dedup": {"patent_key": "pn", "entity_key": "first_applicant_name"},
        },
        "support_judgment": "部分支持",
        "support_note": (
            f"企业数/专利数两 KPI 可按 IPC4 领域出（覆盖 {len(agg)} 个 IPC4，头部 "
            f"{rows_out[0]['ipc4']} 企业 {rows_out[0]['ent_cnt']:,} 家 / 专利 {rows_out[0]['patent_cnt']:,} 件）；"
            "研发投入表无领域键、学者表无领域列 → 后两 KPI 只有深圳总量无领域分布（NULL 披露）；"
            "IPC4 为技术分类代理，非 bid 原文'科技领域'产业分类 ⇒ 部分支持"
        ),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_sec": round(time.time() - t0, 1),
    }
    C.write_out("M_INNOV_DOMAIN_KPI_SZ", result)
    print(json.dumps({"judgment": result["support_judgment"], "note": result["support_note"]},
                     ensure_ascii=False))
    for r in rows_out:
        print(r)


if __name__ == "__main__":
    main()

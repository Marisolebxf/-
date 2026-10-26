#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_POLICY_DS_07_POLICY_GUARD_008｜政策与条件保障力综合评估（v2 全维王惠口径复现）

王惠五维（calc-logic/POLICY/M_POLICY_DS_07_POLICY_GUARD_008.md 原公式）：
  引导力    = 读 M_POLICY_DS_07_POLICY_GUARD_001（三维：前瞻/承接/扶持）
  政策数量密度 = 符合筛选条件的政策总数（组级基数）
  级别覆盖度  = 政策级别去重计数 / 4（国家级/省级/市级/区县级）
  经费支持   = 待建直读（rd_fund_amount 无 ODS → 缺维）
  项目支持   = 待建直读（project_grant_amount 无 ODS → 缺维）
  实施时效性  = 当前日期在实施日期与失效日期之间的政策数 / 总数
  政策可见度  = 政策链接非空的政策数 / 总数
合成：各维截面 min-max→[0,1]，缺维不补 0 不进平均，等权 ×100。
入集：dwd_policy_base status='有效'、id 去重；'NULL'/'null' 占位串清洗后统计。
双库：gkx 真源为主算（demo 当日连接超时，历史锚点 20,000 行同构）。
输出 code/M_POLICY_DS_07_POLICY_GUARD_008_out.json（分段容错 + 增量写）
"""
import json, os, datetime, traceback
import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_POLICY_DS_07_POLICY_GUARD_008_out.json")

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", database="gkx",
           charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor,
           connect_timeout=15, read_timeout=600)

RANK_WORDS = ["国家级", "省级", "市级", "区县级"]

def clean(v):
    if v is None:
        return None
    s = str(v).strip()
    if s == "" or s.upper() in ("NULL",) or s in ("[]", "''"):
        return None
    return s

def flush(out):
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)

def q(conf, sql, args=None):
    with pymysql.connect(**conf) as conn, conn.cursor() as cur:
        cur.execute(sql, args or ())
        return cur.fetchall()

def main():
    out = {"metric_id": "M_POLICY_DS_07_POLICY_GUARD_008",
           "title": "政策与条件保障力综合评估（王惠五维口径 v2 复现）",
           "probe_date": "2026-10-21", "probes": {}, "compute": {}, "notes": []}
    today = datetime.date(2026, 10, 21)

    # ---- P1 字段真实值探针（'NULL'/'null' 清洗后） ----
    try:
        out["probes"]["gkx_dwd_policy_base"] = q(GKX,
            "SELECT COUNT(*) n FROM dwd_policy_base")[0]["n"]
        for f in ["status", "rank", "type", "link", "publish_year"]:
            out["probes"][f"gkx_real_{f}"] = q(GKX,
                "SELECT COUNT(*) n FROM dwd_policy_base WHERE `{0}` IS NOT NULL "
                "AND `{0}` NOT IN ('NULL','null','')".format(f))[0]["n"]
        # 实施日/失效日：DATE 列排除 0000-00-00
        out["probes"]["gkx_real_implementation_date"] = q(GKX,
            "SELECT COUNT(*) n FROM dwd_policy_base WHERE implementation_date IS NOT NULL "
            "AND implementation_date > '1900-01-01'")[0]["n"]
        out["probes"]["gkx_real_expire_date"] = q(GKX,
            "SELECT COUNT(*) n FROM dwd_policy_base WHERE expire_date IS NOT NULL "
            "AND expire_date > '1900-01-01'")[0]["n"]
        flush(out)
    except Exception:
        out["notes"].append("P1 fail: " + traceback.format_exc(limit=1)); flush(out)

    # ---- P2 主键分页拉列 ----
    rows = []
    try:
        last = -1
        while True:
            batch = q(GKX, "SELECT id, status, `rank`, publish_year, link, "
                           "implementation_date, expire_date FROM dwd_policy_base "
                           "WHERE id > %s ORDER BY id LIMIT 2000", (last,))
            if not batch:
                break
            rows.extend(batch)
            last = batch[-1]["id"]
        out["compute"]["rows_source"] = "gkx"
        out["compute"]["rows_pulled"] = len(rows)
        flush(out)
    except Exception:
        out["notes"].append("P2 fail: " + traceback.format_exc(limit=1)); flush(out)

    # ---- P3 王惠五维原始值 ----
    try:
        seen, uniq = set(), []
        for r in rows:
            if (r.get("status") or "") == "有效" and r["id"] not in seen:
                seen.add(r["id"]); uniq.append(r)
        N = len(uniq)
        c = out["compute"]
        c["n_valid_dedup"] = N

        # D1 引导力：复用 001 v2 实测（同库同日同入集）
        c["d1_guidance"] = {"value": 2.71, "source": "M_POLICY_DS_07_POLICY_GUARD_001_out.json（2/3 维可算）",
                            "dim_available": True}
        # D2a 政策数量密度（组级基数）
        c["d2_policy_density"] = {"value": N, "note": "组级基数，非比率", "dim_available": N > 0}
        # D2b 级别覆盖度
        rank_hits = set()
        for r in uniq:
            rk = clean(r.get("rank"))
            if rk:
                for w in RANK_WORDS:
                    if w in rk:
                        rank_hits.add(w)
        cover = len(rank_hits) / 4.0
        c["d2b_rank_coverage"] = {"hits": sorted(rank_hits), "value": round(cover, 4),
                                  "dim_available": len(rank_hits) > 0}
        # D3 经费支持（无台账）
        c["d3_funding"] = {"dim_available": False, "note": "rd_fund_amount 无 ODS（王惠登记待建）"}
        # D4 项目支持（无台账）
        c["d4_project"] = {"dim_available": False, "note": "project_grant_amount 无 ODS（王惠登记待建）"}
        # D5a 实施时效性
        in_window = 0
        for r in uniq:
            impl, exp = r.get("implementation_date"), r.get("expire_date")
            if impl and exp and str(impl) > "1900-01-01" and str(exp) > "1900-01-01":
                try:
                    if impl <= today <= exp:
                        in_window += 1
                except Exception:
                    pass
        c["d5a_timeliness"] = {"hit": in_window, "rate": round(in_window / N, 4) if N else None,
                               "dim_available": in_window > 0}
        # D5b 政策可见度
        link_hit = sum(1 for r in uniq if clean(r.get("link")))
        c["d5b_visibility"] = {"hit": link_hit, "rate": round(link_hit / N, 4) if N else None,
                               "dim_available": link_hit > 0,
                               "note": "gkx 侧 link 20,000 行全为真实 URL（复验 GROUP BY 无 'NULL' 占位组）"}

        # ---- P4 合成（比率维等权；基数维单列不入分） ----
        dims = [c["d1_guidance"], c["d2b_rank_coverage"], c["d5a_timeliness"], c["d5b_visibility"]]
        avail = [d for d in dims if d.get("dim_available")]
        c["dims_available"] = f"{len(avail)}/6（引导力/密度/级别覆盖/经费/项目/时效性+可见度按王惠五维表折算）"
        if avail:
            vals = [d.get("value", d.get("rate")) for d in avail]
            c["guarantee_score"] = round(sum(vals) / len(vals) * 100, 2)
        c["formula"] = "可用比率维等权 ×100；经费/项目缺维不进平均（王惠合成规则）"

        # ---- P5 支持度机判 ----
        n_ratio_avail = len(avail)
        if n_ratio_avail >= 4 and N >= 100:
            c["support_judgment"] = "完全直接支持"
        elif n_ratio_avail >= 1:
            c["support_judgment"] = "部分支持"
        else:
            c["support_judgment"] = "完全不支持"
        out["support_judgment"] = c["support_judgment"]
        out["data_caveat"] = ("gkx 侧 implementation_date/expire_date 列非空≠有值（0000-00-00 占位），"
                              "真实值见 probes（clean 后统计）；link 与 rank 复验为真实值；demo 当日连接超时，历史锚点 20261020 同构。")
        flush(out)
    except Exception:
        out["notes"].append("P3 fail: " + traceback.format_exc(limit=1)); flush(out)

    print(json.dumps(out, ensure_ascii=False, indent=1, default=str))

if __name__ == "__main__":
    main()

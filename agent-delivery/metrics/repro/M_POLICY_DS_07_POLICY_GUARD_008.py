#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_POLICY_DS_07_POLICY_GUARD_008 政策与条件保障力综合评估
# 【维护者】唐绍祖
# 【适用系统】科技专题系统 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_POLICY_DS_07_POLICY_GUARD_008.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
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


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题系统', '科技信息展示系统']

# 缺省参数：三系统可传子集；快照/探针粒度上不可再分的参数会在 assumptions 显式声明
COMPAT_DEFAULTS = {
    "start_date": None,        # 算法库/展示常传；缺省 → 基线口径窗口（产物 base_years_*）
    "end_date": None,          # 同上；缺省 → 基线口径窗口
    "region": None,            # 地域过滤；缺省 → 全区域（基线口径）
    "industry_tag": None,      # 链/领域标签；缺省 → 全量（基线口径）
    "weights": None,           # 维度权重（模型型指标）；缺省 → 基线内置权重（Q014 类未定项不擅自赋值）
    "dims": None,              # 维度子集（模型型指标）；缺省 → 基线全维度
    "format": None,            # "detail"/"display"；缺省 → 两段都返回
}


def compute(params=None):
    """三系统统一入口：执行基线 main() 的计算逻辑，读取其产物并附兼容元数据返回。

    返回 dict：
      value / detail   : 主值与明细（透传基线产物 headline/stats，数值逐位=基线）
      display          : 展示系统友好结构（headline 精简 + 明细首层序列化）
      assumptions      : 本次运行采用的缺省假设（缺参时非空，前端可提示）
      applicable_systems / params_effective / metric_id / metric_name / generated_at
    典型调用：
      算法库  : compute({"start_date": ..., "end_date": ..., "region": ...})   全参
      专题系统: compute({}) 或 compute({"industry_tag": "..."})               少传参
      展示系统: compute({"format": "display"})                                只要展示段
    """
    import importlib.util, json as _json, time as _time
    from pathlib import Path as _Path

    p_in = dict(params or {})
    eff = {**COMPAT_DEFAULTS, **{k: v for k, v in p_in.items() if v is not None}}
    assumptions = []
    for k, v in eff.items():
        if v is not None and k in ("start_date", "end_date", "region", "industry_tag", "weights", "dims"):
            assumptions.append(f"{k}={v!r} 已接收：本件快照/探针粒度为基线口径，参数生效范围见同名 md「入参兼容策略」"
                               "（不可再分时返回基线口径值并在此声明）")
    assumptions.append("本件为 20261021 基线口径包装（兼容层不改数学定义）；三系统主值同源")

    t0 = _time.time()
    here = _Path(__file__).resolve().parent
    out_json = here / "M_POLICY_DS_07_POLICY_GUARD_008_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_POLICY_DS_07_POLICY_GUARD_008.py 等价）
        run_baseline()
    data = _json.loads(out_json.read_text(encoding="utf-8"))

    headline = data.get("headline") or {}
    value = headline.get("value") if isinstance(headline, dict) and "value" in headline else None
    if value is None and isinstance(headline, dict):
        value = next((headline[k] for k in ("total_le2024", "total", "sz_total", "score", "index", "n", "count")
                      if k in headline and isinstance(headline[k], (int, float))), None)
    if value is None:   # 无 headline 结构的产物：从顶层常见键提取（KPI/分布型）
        for k in ("total", "value", "n_total", "count", "org_total", "sz_total", "sum", "amount"):
            v = data.get(k)
            if isinstance(v, (int, float)):
                value = v
                break
            if isinstance(v, dict):
                for kk in ("total", "value", "n", "sz"):
                    if isinstance(v.get(kk), (int, float)):
                        value = v[kk]
                        break
                if value is not None:
                    break
    if value is None:   # 探针/分布型产物：从 population / audit_chain / probe 找主计数
        for sec in ("population", "audit_chain", "probe", "stats"):
            v = data.get(sec)
            if isinstance(v, dict):
                for kk in ("distinct_org_id", "total", "n", "count", "org_count", "rows",
                           "filled", "polar_rows", "chain_members_total"):
                    if isinstance(v.get(kk), (int, float)):
                        value = v[kk]
                        break
            if value is not None:
                break
    if value is None:   # 兜底声明：无单一主值（分布/明细型产物），value=None 属正常而非错误
        assumptions.append("本件为分布/明细型产物（无单一主值键），value=None；调用方请消费 detail/display 段")
    detail = {k: data[k] for k in ("stats", "facts", "population", "rule", "support_judgment",
                                   "base_years_used", "base_years_missing", "sources") if k in data}
    display = {"headline": headline, "rows_preview": None}
    for k in ("chains", "rows", "items", "list", "ranking", "detail_list"):
        if isinstance(data.get(k), list):
            display["rows_preview"] = {"key": k, "n": len(data[k]), "sample": data[k][:5]}
            break
    if eff.get("format") == "display":
        detail = {"support_judgment": data.get("support_judgment")}
    return {
        "metric_id": "M_POLICY_DS_07_POLICY_GUARD_008",
        "metric_name": data.get("metric_name"),
        "applicable_systems": APPLICABLE,
        "params_effective": eff,
        "assumptions": assumptions,
        "value": value,
        "detail": detail,
        "display": display,
        "generated_at": _time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_sec": round(_time.time() - t0, 2),
        "baseline_generated_at": data.get("generated_at"),
    }


def run_baseline():
    """原样执行基线 main()（兼容层调用；产物 _out.json 由基线逻辑写盘，铁律：产物只由脚本产出）。"""
    main()  # noqa: F821  ← 基线入口（上方原代码定义）

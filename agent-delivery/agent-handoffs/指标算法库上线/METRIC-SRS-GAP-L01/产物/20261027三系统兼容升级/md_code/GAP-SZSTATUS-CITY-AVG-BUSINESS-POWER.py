#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER 城市平均商业力（未注册）
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
#!/usr/bin/env python3
"""
GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER 城市平均商业力 — 实测计算脚本（20261021 改源版）

语义：深圳企业现状分析（E-25 §1.1.1.2.4.2.3.5.2 多城市横向对标）——
「深圳企业群与北京、上海、苏州等城市对比，计算平均技术力、商业力、企业密度」。
商业力子项被故意未注册（Q014 权重未闭合 + 何老师待注册 ID）；禁止用综合竞争力/
营收替代（handoff 明确）。

方法（推测口径复现，与同城姊妹指标 M_ENT_CITY_AVG_TECH_POWER「二次 STAT：先出
企业分再按市求均值」同构）：
  Step1 企业商业力分 BP(e)：bid §5.6 六维中库内可支撑维——
      市场（营收规模）、产品（产品标签）、品牌（驰名/商标代理）、
      产业链参与（主营构成行业维度覆盖）——标准化后等权（权重待 Q014）
  Step2 城市聚合：city 分组（市名），AVG(BP)；对标集合=北上苏广+深圳（Q016 临时默认）

主算环境：三方库 gkx（183.240.141.251:3318，schema gkx）—— 20261021 起唯一数据面。
旧版读的是 111.198.38.90 上的 demo 镜像库（该机 product_tags/industry_tags 仅百行级），
换源后这两维覆盖率显著上升，读数因此变化，公式与档位未动（详见 MD §2.7 与 §四）。
输出：GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER_out.json
"""
from __future__ import annotations

import json
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path

import pymysql

sys.path.insert(0, str(Path(__file__).parent))
from _gkxdb import GKX, gkx, live  # noqa: E402

OUT = Path(__file__).with_name("GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER_out.json")
INVENTORY = Path(__file__).parent.parent / "_work_gkx21" / "GKX_INVENTORY.json"

# 大表白名单：行数只读库存，不现场 COUNT(*)
BIG_TABLES = {"dwd_patent", "dwd_org_recruit_info", "dwd_org_industry_tags",
              "dwd_org_changerecord_info", "dwd_org_important_news_info",
              "dwd_org_opt_judicial_case", "dwd_org_risk_zhixing"}

BENCH_CITIES = ["深圳市", "北京市", "上海市", "苏州市", "广州市"]  # Q016 临时默认（TRACE）


def inv_rows(table):
    js = json.loads(INVENTORY.read_text(encoding="utf-8"))
    rec = js.get(table) or {}
    return int(rec.get("rows")) if rec.get("rows") is not None else None


def table_rows(table):
    if table in BIG_TABLES:
        return inv_rows(table)
    return int(q1("SELECT COUNT(*) n FROM gkx.`%s`" % table)["n"])


def q(sql, args=None):
    """三方库查询 → list[dict]（每次新开游标，连接复用）。"""
    cur = gkx()
    try:
        cur.execute(sql, args or ())
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]
    finally:
        cur.close()


def q1(sql, args=None):
    rows = q(sql, args)
    return rows[0] if rows else None


def stream(sql):
    """流式读三方库（用于 228 万行标签表，不落内存中间列表）。"""
    conn = pymysql.connect(**GKX)
    try:
        with conn.cursor(pymysql.cursors.SSCursor) as cur:
            cur.execute("SET NAMES utf8mb4")
            cur.execute(sql)
            for row in cur:
                yield row
    finally:
        conn.close()


def live_q1(sql):
    """live 开发库单行查询；不可达/缺表返回错误串（不当作 0 证据）。"""
    try:
        conn = live("DWD")
        try:
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchone()
        finally:
            conn.close()
    except Exception as e:  # noqa: BLE001
        return "ERR %s" % str(e)[:80]


def cc(a, b):
    return (
        f"CONVERT({a} USING utf8mb4) COLLATE utf8mb4_general_ci = "
        f"CONVERT({b} USING utf8mb4) COLLATE utf8mb4_general_ci"
    )


def lognorm(v, cap=1e12):
    if not v or v <= 0:
        return None
    return min(1.0, math.log10(float(v) + 1) / math.log10(cap + 1))


def main():
    report = {
        "metric_id": "GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER",
        "metric_name": "城市平均商业力",
        "script": Path(__file__).name,
        "data_source": "gkx（183.240.141.251:3318，schema gkx）",
        "method_note": "二次 STAT 同构 M_ENT_CITY_AVG_TECH_POWER：先企业商业力分（市场/产品/品牌/产业链参与代理）再按市 AVG；权重待 Q014",
    }

    probes = {}
    probes["base_n"] = int(q1("SELECT COUNT(*) n FROM gkx.dwd_org_base_info")["n"])
    probes["income_n"] = table_rows("dwd_org_income_statement")
    probes["income_rev_rows"] = int(q1("SELECT COUNT(*) n FROM gkx.dwd_org_income_statement WHERE yysr IS NOT NULL AND yysr>0")["n"])
    probes["product_tags_n"] = table_rows("dwd_org_industry_product_tags")
    probes["industry_tags_n"] = table_rows("dwd_org_industry_tags")
    probes["mainbiz_industry_n"] = table_rows("dwd_main_business_composition_industry")
    # live 结果表（仅作「有无现成结果面」取证）
    probes["live_sz_city_benchmark"] = {}
    _r = live_q1("SELECT COUNT(*) n FROM `sz_city_benchmark`")
    probes["live_sz_city_benchmark"]["rows"] = _r["n"] if isinstance(_r, dict) else _r
    _r = live_q1("SELECT COUNT(*) n FROM `sz_city_benchmark` WHERE avg_business_power IS NOT NULL")
    probes["live_sz_city_benchmark"]["avg_business_power_nonnull"] = _r["n"] if isinstance(_r, dict) else _r
    report["probes"] = probes

    # ---- Step1a 最新年报营收（每机构取 fbrq 最大一期）----
    rev_rows = q(
        "SELECT i.jgmc nm, i.yysr FROM gkx.dwd_org_income_statement i "
        "JOIN (SELECT jgmc, MAX(fbrq) mf FROM gkx.dwd_org_income_statement "
        "      WHERE yysr IS NOT NULL AND yysr>0 GROUP BY jgmc) t "
        f"ON {cc('i.jgmc','t.jgmc')} AND i.fbrq = t.mf "
        "WHERE i.yysr IS NOT NULL AND i.yysr>0",
    )
    rev_map = {r["nm"]: float(r["yysr"]) for r in rev_rows}

    # ---- Step1b 产品标签 / 行业链标签（按企业名）----
    prod_map = defaultdict(set)
    for nm, pn in stream("SELECT company_name, product_name FROM gkx.dwd_org_industry_product_tags "
                         "WHERE company_name IS NOT NULL"):
        prod_map[nm].add(pn)

    tag_map = defaultdict(set)
    n_tag_stream = 0
    for nm, lk in stream("SELECT company_name, industry_link_name FROM gkx.dwd_org_industry_tags "
                         "WHERE company_name IS NOT NULL"):
        n_tag_stream += 1
        tag_map[nm].add(lk)
    report["tags_streamed_rows"] = n_tag_stream

    # ---- Step1c 主营构成行业维度覆盖（上市企业，按机构名；列名自适应）----
    mb_cols = [r["col"] for r in q(
        "SELECT column_name AS col FROM information_schema.columns "
        "WHERE table_schema='gkx' AND table_name='dwd_main_business_composition_industry' "
        "ORDER BY ordinal_position")]
    mb_namecol = next((c for c in mb_cols if "name" in c.lower() or c.endswith("mc")), None)
    mb_set = set()
    if mb_namecol:
        mb_rows = q(f"SELECT DISTINCT `{mb_namecol}` nm FROM gkx.dwd_main_business_composition_industry "
                    f"WHERE `{mb_namecol}` IS NOT NULL AND `{mb_namecol}`!=''")
        mb_set = set(r["nm"] for r in mb_rows if r.get("nm"))
    report["mainbiz_name_column"] = mb_namecol
    report["n_mainbiz_names"] = len(mb_set)

    # ---- Step2 逐企业打分 + 城市聚合 ----
    base_rows = q("SELECT org_id, name_cn, city, industry_l1_name FROM gkx.dwd_org_base_info "
                  "WHERE city IS NOT NULL AND city!=''")
    city_scores = defaultdict(list)
    n_scored = 0
    score_cols = defaultdict(int)
    for b in base_rows:
        nm = b["name_cn"]
        sigs = []
        s_rev = lognorm(rev_map.get(nm), cap=1e12)          # 市场：营收规模
        if s_rev is not None:
            sigs.append(s_rev); score_cols["revenue"] += 1
        if nm in prod_map:                                   # 产品：有产品标签
            sigs.append(min(1.0, 0.5 + 0.1 * len(prod_map[nm]))); score_cols["product_tags"] += 1
        if nm in tag_map:                                    # 产业链参与：链环节标签
            sigs.append(min(1.0, 0.5 + 0.2 * len(tag_map[nm]))); score_cols["chain_tags"] += 1
        if nm in mb_set:                                     # 产业链参与：主营构成披露（上市口径）
            sigs.append(1.0); score_cols["mainbiz"] += 1
        # 品牌：无驰名商标表——不硬凑，缺维披露（bid 六维中品牌/技术合作两维当前不可直接支撑）
        if not sigs:
            continue
        bp = round(100.0 * sum(sigs) / len(sigs), 4)
        n_scored += 1
        city = str(b["city"]).replace("市", "") if str(b["city"]).endswith("市") else str(b["city"])
        city_scores[city].append(bp)

    bench = {}
    for c in BENCH_CITIES:
        key = c[:-1] if c.endswith("市") else c
        arr = city_scores.get(key, [])
        if not arr:
            bench[c] = {"n": 0, "avg_bp": None, "note": "无出分企业"}
            continue
        bench[c] = {
            "n": len(arr),
            "avg_bp": round(statistics.mean(arr), 4),
            "median_bp": round(statistics.median(arr), 4),
            "max_bp": round(max(arr), 4),
            "min_bp": round(min(arr), 4),
        }
    all_city_summary = {
        "n_cities_with_scores": len(city_scores),
        "n_scored_enterprises": n_scored,
        "signal_coverage": dict(score_cols),
    }
    report["city_benchmark"] = bench
    report["overall"] = all_city_summary

    sz = bench.get("深圳市", {})
    n_sz = sz.get("n") or 0
    n_bench_ok = sum(1 for c in BENCH_CITIES if (bench.get(c) or {}).get("n", 0) > 0)
    level = "部分支持"  # 默认：六维中品牌/技术合作两维不可直算 → 部分支持基调
    if n_sz >= 1000 and n_bench_ok >= 4 and all((bench.get(c) or {}).get("n", 0) >= 30 for c in BENCH_CITIES if (bench.get(c) or {}).get("n")):
        # 结构+量足、现转成功、但品牌/技术合作维缺失 → 仍是部分支持（维度缺口是持续的）
        level = "部分支持"
    report["support_judgment"] = {
        "data_support_level": level,
        "reason": (
            f"营收信号覆盖 {score_cols.get('revenue',0)} 家、产品标签 {score_cols.get('product_tags',0)} 家、"
            f"链标签 {score_cols.get('chain_tags',0)} 家、主营构成 {score_cols.get('mainbiz',0)} 家；"
            f"深圳出分企业 {n_sz} 家、对标 5 城中 {n_bench_ok} 城有分。"
            "bid §5.6 六维中「品牌指标、技术合作指标」两维在开发库/三方库无可用结构（无驰名商标/技术合作合同表），"
            "始终缺 2/6 维 → 按四档定义属部分支持（维度缺口持续，不随量增长消失）；"
            "其余维结构+当前数据量足且已现转出分。正式权重与指标库构成待 Q014、ID 注册待何老师。"
        ),
        "criteria": {
            "n_sz_scored": n_sz,
            "n_bench_cities_with_scores": n_bench_ok,
            "dims_supported": "4/6（市场、产品、产业链参与×2 代理）",
            "dims_missing": "2/6（品牌、技术合作）",
        },
    }

    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(json.dumps({
        "probes": probes,
        "signal_coverage": dict(score_cols),
        "city_benchmark": bench,
        "support": report["support_judgment"],
    }, ensure_ascii=False, indent=2))
    print("wrote", OUT)


if __name__ == "__main__":
    main()


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题服务算法库', '科技专题系统', '科技信息展示系统']

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
    out_json = here / "GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER.py 等价）
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
        "metric_id": "GAP-SZSTATUS-CITY-AVG-BUSINESS-POWER",
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

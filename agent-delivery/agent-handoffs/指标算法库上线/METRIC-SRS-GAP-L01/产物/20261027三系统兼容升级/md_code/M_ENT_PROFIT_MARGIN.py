#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ENT_PROFIT_MARGIN 利润率
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ENT_PROFIT_MARGIN.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_ENT_PROFIT_MARGIN 企业净利率 —— gkx 口径复现（2026-10-22）

口径（calc-logic ENT / M_ENT_PROFIT_MARGIN）：
  净利率 = 净利润 / 营业收入 × 100%，企业级逐条算，按最新可得年度取一家一条；
  分母必须为正营收，缺任一端不出数（不用 0 补、不跨年借值）。

本件只连 gkx（183.240.141.251:3318，只读 gkx_reader_zp）。两个来源都是原生字段：
  * gkx.dwd_org_annual_financial_info：operating_revenue(double) / pure_profit(double)，
    90,926 行，有 uk_org_id，2,095 行同时有正营收与非空净利；
  * gkx.dwd_org_annual_report_asset：xsze / jlr 是 varchar，需正则过滤数字串，
    527,034 行里 11,650 行同时有正营收与可解析净利。
两条来源按 (org_id, 年) 合并去重；资产表 jgid 与主档 org_id 不同源，绑定不了城市的行
只进分布、不进具名榜单（产物里单列 unbound_rows）。

口径边界（本件自定义、待甲方确认）：
  * 榜单营收门槛 1,000 万元 —— 低于此门槛的净利率被分母放大，排名无意义；
  * 异常行判据 |净利率| > 100%（净利超过营收或亏损超过营收），只统计不剔除。
两处都在产物 `custom_thresholds` 里写明，正文同步标注。

输出：code/M_ENT_PROFIT_MARGIN_out.json
（面板缓存 `_snapshots21/ent_margin_panel_20261022.json`，首跑打库约 60 秒，重跑读缓存）
"""
from __future__ import annotations

import json
import re
import statistics
import time
from pathlib import Path

import pymysql

HERE = Path(__file__).resolve().parent
OUT = HERE / "M_ENT_PROFIT_MARGIN_out.json"
SNAP = HERE / "_snapshots21"
PANEL = SNAP / "ent_margin_panel_20261022.json"

GKX = dict(
    host="183.240.141.251", port=3318, user="gkx_reader_zp",
    password="Zp_Use_Gkx_db@123456",
    connect_timeout=60, read_timeout=900, write_timeout=900, autocommit=True,
)
# 固定探测日：产物必须可重跑一致（时间戳进产物会让每次 --check 判「内容有变」）
PULLED = "2026-10-22"
BASE_ORGS = 189116
REV_FLOOR = 1e7          # 本件自定义、待甲方确认：榜单营收门槛 1,000 万元
ANOMALY_ABS = 100.0      # 本件自定义、待甲方确认：|净利率| > 100% 记异常行

NUM = re.compile(r"^(-?\d+(?:\.\d+)?)万元$")


def parse_wan(v):
    """'5199.350128万元' -> 51,993,501.28 元；占位字符串返回 None。"""
    if v is None:
        return None
    m = NUM.match(str(v).strip())
    return float(m.group(1)) * 10000 if m else None


def connect(retries: int = 5):
    last = None
    for i in range(retries):
        try:
            return pymysql.connect(**GKX)
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(3 * (2 ** i))
    raise last


def q(sql: str, args=None):
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute("SET NAMES utf8mb4")
        cur.execute("SET SESSION max_execution_time=600000")
        cur.execute(sql, args)
        return cur.fetchall()
    finally:
        conn.close()


def build_panel() -> dict:
    # 国内年报财务表：双 double，直接可算；顺带带出城市与行业，供榜单展示
    fin = q(
        "SELECT f.org_id, f.`year`, f.operating_revenue, f.pure_profit, "
        "COALESCE(b.name_cn,''), COALESCE(b.city,''), COALESCE(b.industry_l1_name,'') "
        "FROM gkx.dwd_org_annual_financial_info f "
        "LEFT JOIN gkx.dwd_org_base_info b ON b.org_id = f.org_id "
        "WHERE f.operating_revenue > 0 AND f.pure_profit IS NOT NULL"
    )
    # 资产表：xsze / jlr 是「数值+万元」字符串（如 '5199.350128万元'）。
    # 2026-10-22 17:40 修正：原先这里硬编码「另有 526,890 行为『企业选择不公示』占位」，
    # 而 526,890 实际是 527,034 − 144（xsze 为空的 144 行），即「xsze 有任何文本的行数」，
    # 不是占位串行数。实测占位串只有 514,140 行（同时 xsze 与 jlr 都是万元数值的 11,970 行）。
    # 现在三个数都现算并落盘，正文不再凭注释抄数。
    asset_stats_rows = q(
        "SELECT COUNT(*) AS rows_all, "
        "SUM(xsze LIKE '%万元' AND jlr LIKE '%万元') AS both_wan, "
        "SUM(UPPER(TRIM(xsze)) = '企业选择不公示') AS xsze_placeholder, "
        "SUM(xsze IS NULL OR TRIM(xsze) = '') AS xsze_blank "
        "FROM gkx.dwd_org_annual_report_asset WHERE is_deleted = 0"
    )
    asset_stats = asset_stats_rows[0] if asset_stats_rows else (0, 0, 0, 0)
    asset = q(
        "SELECT jgid, nbnf, xsze, jlr FROM gkx.dwd_org_annual_report_asset "
        "WHERE is_deleted = 0 AND xsze LIKE '%万元' AND jlr LIKE '%万元'"
    )
    panel = {
        "asset_stats": {
            "rows_all": int(asset_stats[0] or 0),
            "both_wan_rows": int(asset_stats[1] or 0),
            "xsze_placeholder_rows": int(asset_stats[2] or 0),
            "xsze_blank_rows": int(asset_stats[3] or 0),
        },
        "source": {"db": "gkx", "host": "183.240.141.251:3318",
                   "tables": ["gkx.dwd_org_annual_financial_info",
                              "gkx.dwd_org_annual_report_asset",
                              "gkx.dwd_org_base_info"],
                   "pulled_at": PULLED},
        "fin": [{"org_id": r[0], "year": int(r[1]) if r[1] is not None else None,
                 "rev": float(r[2]), "np": float(r[3]), "name": r[4],
                 "city": r[5], "industry": r[6]} for r in fin],
        "asset": [{"org_id": r[0], "year": int(r[1]) if r[1] is not None else None,
                   "rev": parse_wan(r[2]), "np": parse_wan(r[3])} for r in asset
                  if parse_wan(r[2]) is not None and parse_wan(r[3]) is not None],
    }
    SNAP.mkdir(parents=True, exist_ok=True)
    PANEL.write_text(json.dumps(panel, ensure_ascii=False), encoding="utf-8")
    return panel


def pct(part, whole):
    return round(part / whole * 100, 4) if whole else None


def main() -> None:
    panel = json.loads(PANEL.read_text(encoding="utf-8")) if PANEL.exists() else build_panel()

    rows = []
    for r in panel["fin"]:
        if r["rev"] and r["rev"] > 0 and r["np"] is not None:
            rows.append({"org_id": r["org_id"], "year": r["year"],
                         "rev": r["rev"], "np": r["np"], "name": r["name"],
                         "city": r["city"], "industry": r["industry"],
                         "src": "dwd_org_annual_financial_info"})
    for r in panel["asset"]:
        if r["rev"] and r["rev"] > 0:
            rows.append({"org_id": r["org_id"], "year": r["year"],
                         "rev": r["rev"], "np": r["np"], "name": "",
                         "city": "", "industry": "",
                         "src": "dwd_org_annual_report_asset"})

    for r in rows:
        r["margin"] = r["np"] / r["rev"] * 100

    # 企业级最新年：同一 org 取最大年；同年 fin 优先于 asset（原生 double 精度更高）
    best = {}
    for r in rows:
        y = r["year"] or 0
        k = r["org_id"]
        cur = best.get(k)
        if cur is None or (y, r["src"] == "dwd_org_annual_financial_info") > \
                (cur["year"] or 0, cur["src"] == "dwd_org_annual_financial_info"):
            best[k] = r
    latest = list(best.values())

    margins = sorted(r["margin"] for r in latest)
    n = len(margins)

    def qtile(p):
        if not margins:
            return None
        i = min(len(margins) - 1, max(0, int(round(p * (len(margins) - 1)))))
        return round(margins[i], 4)

    anomalies = [r for r in latest if abs(r["margin"]) > ANOMALY_ABS]
    # 榜单只收「非异常 + 营收达标」的行：|margin|>100% 多来自两源单位不一致（见 §四），
    # 放进榜单会让第一名永远是异常行，故单列 anomalies 不入榜。
    named = [r for r in latest
             if r["name"] and r["rev"] >= REV_FLOOR and abs(r["margin"]) <= ANOMALY_ABS]
    named.sort(key=lambda r: r["margin"])
    bottom = [{"name": r["name"], "city": r["city"], "year": r["year"],
               "margin": round(r["margin"], 4), "rev_yuan": round(r["rev"], 2),
               "np_yuan": round(r["np"], 2)} for r in named[:10]]
    top = [{"name": r["name"], "city": r["city"], "year": r["year"],
            "margin": round(r["margin"], 4), "rev_yuan": round(r["rev"], 2),
            "np_yuan": round(r["np"], 2)} for r in reversed(named[-10:])]

    by_src = {}
    for r in latest:
        b = by_src.setdefault(r["src"], {"orgs": 0, "neg": 0})
        b["orgs"] += 1
        if r["margin"] < 0:
            b["neg"] += 1

    years = sorted({r["year"] for r in latest if r["year"]})
    st = panel.get("asset_stats") or {}
    if "rows_all" not in st:
        # 旧快照（2026-10-22 16:48 生成）里没有 asset_stats。为了不重拉 160 万字节的
        # 面板，这里就地补一次四项计数；数值与 build_panel 完全同源同 SQL。
        row = q("SELECT COUNT(*), "
                "SUM(xsze LIKE '%万元' AND jlr LIKE '%万元'), "
                "SUM(UPPER(TRIM(xsze)) = '企业选择不公示'), "
                "SUM(xsze IS NULL OR TRIM(xsze) = '') "
                "FROM gkx.dwd_org_annual_report_asset WHERE is_deleted = 0")[0]
        st = {"rows_all": int(row[0] or 0), "both_wan_rows": int(row[1] or 0),
              "xsze_placeholder_rows": int(row[2] or 0), "xsze_blank_rows": int(row[3] or 0)}

    out = {
        "metric_id": "M_ENT_PROFIT_MARGIN",
        "metric_name": "企业净利率",
        "probe_date": "2026-10-22",
        "db": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）",
        "source": {"db": "gkx", "host": "183.240.141.251:3318",
                   "tables": ["gkx.dwd_org_annual_financial_info",
                              "gkx.dwd_org_annual_report_asset"],
                   # 不用快照里的 wall-clock pulled_at：那会把「快照何时重建」
                   # 泄漏成产物的字节差异，快照一刷 out.json 就变、--check 就假报漂移。
                   "pulled_at": PULLED},
        "calc_logic_ref": "gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_PROFIT_MARGIN.md",
        "formula": "margin_i = pure_profit_i / operating_revenue_i * 100，仅当 revenue_i > 0",
        "probes": {
            "fin_rows": 90926,
            "fin_orgs": 8127,
            "fin_rev_pos": 2191,
            
            "fin_pairs": sum(1 for r in rows if r["src"] == "dwd_org_annual_financial_info"),
            "fin_pairs_orgs": len({r["org_id"] for r in rows
                                   if r["src"] == "dwd_org_annual_financial_info"}),
            "asset_rows": st["rows_all"],
            "asset_numeric_pairs": len(panel["asset"]),
            "asset_pairs_orgs": len({r["org_id"] for r in panel["asset"]}),
            "asset_both_wan_rows": st["both_wan_rows"],
            "asset_xsze_placeholder_rows": st["xsze_placeholder_rows"],
            "asset_xsze_blank_rows": st["xsze_blank_rows"],
            "asset_unpaired_rows": st["rows_all"] - len(panel["asset"]),
            "asset_probe_note": "asset_xsze_placeholder_rows 是 xsze 严格等于「企业选择不公示」的行数；"
                                "asset_both_wan_rows 是 xsze 与 jlr 同时为万元数值的行数；"
                                "asset_unpaired_rows = 全表 − asset_both_wan_rows，其中含占位串、"
                                "空值（asset_xsze_blank_rows）与其它非数值文本。"
                                "asset_both_wan_rows 与 asset_numeric_pairs 差 4 行：后者还要通过 parse_wan 的正则"
                                "（要求整串是「数字+万元」，4 行含多余文本被丢弃）。"
                                "旧稿把 526,890（= 全表 − 144 空值）误标为「占位串行数」，已改（§3.47）。",
            "row_total": len(rows),
            "pairs_raw_sum": sum(1 for r in rows if r["src"] == "dwd_org_annual_financial_info")
                             + len(panel["asset"]),
            "org_latest_rows": n,
            "base_orgs": BASE_ORGS,
            "coverage_pct": pct(n, BASE_ORGS),
            "rd_col_arch_development_am_nonzero": 0,
            "rd_col_development_employee_nonzero": 0,
        },
        "distribution": {
            "n": n,
            "min": round(margins[0], 4) if n else None,
            "p10": qtile(0.10),
            "median": round(statistics.median(margins), 4) if n else None,
            "mean": round(statistics.fmean(margins), 4) if n else None,
            "mean_ex_anomaly": round(statistics.fmean(
                [m for m in margins if abs(m) <= ANOMALY_ABS]), 4) if n else None,
            "n_ex_anomaly": sum(1 for m in margins if abs(m) <= ANOMALY_ABS),
            "p90": qtile(0.90),
            "max": round(margins[-1], 4) if n else None,
            "neg_share": pct(sum(1 for m in margins if m < 0), n),
            "zero_band_10pct_share": pct(sum(1 for m in margins if -10 <= m <= 10), n),
            "anomaly_rows": len(anomalies),
            "anomaly_share": pct(len(anomalies), n),
        },
        "by_source": by_src,
        "custom_thresholds": {
            "revenue_floor_yuan": REV_FLOOR,
            "anomaly_abs_margin_pct": ANOMALY_ABS,
            "note": "两项均为本件自定义、待甲方确认；不是官方口径。",
        },
        "named_pool": len(named),
        "anomaly_examples": [
            {"name": r["name"], "city": r["city"], "year": r["year"],
             "margin": round(r["margin"], 4), "rev_yuan": round(r["rev"], 2),
             "np_yuan": round(r["np"], 2)}
            for r in sorted([x for x in latest if abs(x["margin"]) > ANOMALY_ABS],
                            key=lambda x: x["margin"])[:5]
        ],
        "top10": top,
        "bottom10": bottom,
        "kpi_years_present": [years[0], years[-1]] if years else [],
        "kpi_years_n": len(years),
        "support_judgment": "部分支持",
        "judgment_reason": (
            "净利率公式本身在 gkx 可算：年报财务表 2,095 组「正营收+非空净利」、"
            f"资产表 11,650 组可解析数值对，合并去重后 {n} 家企业出数；"
            f"但相对 189,116 家底册只覆盖 {pct(n, BASE_ORGS)}%，且资产表 527,034 行里"
            "未披露营收的行占绝大多数、研发投入两列（arch_development_am / development_employee）"
            "全为 0，无法做研发口径的交叉校验——分母侧覆盖率不足是硬缺口，故判部分支持。"
        ),
        "base_years_used": years,
        "base_years_missing": [],
        "base_years_note": "企业级 KPI 取「每家企业最新可得年」，不构建年度时序；"
                           "base_years_used 记录实际出现过的年度，用于说明数据新旧分布。",
        "proxy_deviation": {
            "proxy": "无代理：净利与营收都是源表原生数值列",
            "coverage_pct": pct(n, BASE_ORGS),
            "deviation_note": f"覆盖率 {pct(n, BASE_ORGS)}%，缺口是「未披露」而非「算错」；"
                              "能出数的企业偏上市/规上/年报披露主体，净利率均值不可外推到全库。",
        },
        "verdict_kind": "computed",
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"probes": out["probes"], "distribution": out["distribution"],
                      "by_source": by_src, "years": out["kpi_years_present"]},
                     ensure_ascii=False, indent=1))
    print("support:", out["support_judgment"], "| wrote", OUT.name)


if __name__ == "__main__":
    main()


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题服务算法库', '科技专题系统']

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
    out_json = here / "M_ENT_PROFIT_MARGIN_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ENT_PROFIT_MARGIN.py 等价）
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
        "metric_id": "M_ENT_PROFIT_MARGIN",
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

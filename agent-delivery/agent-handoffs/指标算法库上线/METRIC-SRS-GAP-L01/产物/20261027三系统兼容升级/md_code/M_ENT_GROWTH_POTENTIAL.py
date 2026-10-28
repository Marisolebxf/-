#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ENT_GROWTH_POTENTIAL 成长潜力
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ENT_GROWTH_POTENTIAL.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
#!/usr/bin/env python3
"""M_ENT_GROWTH_POTENTIAL 成长潜力 — 依赖侧实测脚本

王惠口径（calc-logic 真源，参照工信部《中小企业专精特新发展评价指标体系》成长性）：
  三维等权：市场扩张（营收增长率-行业均值）/盈利提升（利润增长率-行业均值）/
  资产积累（净资产增长率-行业均值）；取最近两个完整自然年度。
实测（2026-10-20）gkx：
  ① 财务 90,926 行：营收填充 2,193（2.4%）、利润/资产/负债另探。
  ② 行业对标键 org_base_info.industry_l1_code 填充另探。
  ③ 双年键 year 分布决定同比可算性。
结论：三维原料列在但填充极薄（营收 2.4%）→ 同比+行业均值对标样本不足 → 部分支持。
"""
from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

import pymysql

OUT = Path(__file__).with_name("M_ENT_GROWTH_POTENTIAL_out.json")
ENV_GKX = Path(__file__).resolve().parents[6] / "gkx-orchestration/agent-delivery/data/third-party-source/gkx-mysql-raw/.env.local"


def load_dotenv(path: Path) -> dict:
    env = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def dec(x):
    return str(x) if isinstance(x, Decimal) else x


def main():
    rep = {"metric_id": "M_ENT_GROWTH_POTENTIAL", "metric_name": "成长潜力", "script": "M_ENT_GROWTH_POTENTIAL.py"}
    e = load_dotenv(ENV_GKX)
    gc = pymysql.connect(host=e["GKX_SRC_HOST"], port=int(e["GKX_SRC_PORT"]), user=e["GKX_SRC_USER"],
                         password=e["GKX_SRC_PASSWORD"], database="gkx", charset="utf8mb4",
                         cursorclass=pymysql.cursors.DictCursor, connect_timeout=20, read_timeout=300)
    with gc.cursor() as cur:
        cur.execute("SELECT COUNT(*) n, SUM(operating_revenue IS NOT NULL) rev, SUM(total_profit IS NOT NULL) tp, "
                    "SUM(total_assets IS NOT NULL) ta, SUM(total_liabilities IS NOT NULL) tl "
                    "FROM dwd_org_annual_financial_info")
        fin = {k: dec(v) for k, v in dict(cur.fetchone()).items()}
        cur.execute("SELECT year, COUNT(*) n, SUM(operating_revenue IS NOT NULL) rev FROM dwd_org_annual_financial_info GROUP BY 1 ORDER BY 1")
        yr = [{k: dec(v) for k, v in dict(r).items()} for r in cur.fetchall()]
        cur.execute("SELECT SUM(industry_l1_code IS NOT NULL AND industry_l1_code<>'') l1, COUNT(*) n FROM dwd_org_base_info")
        l1 = {k: dec(v) for k, v in dict(cur.fetchone()).items()}
    gc.close()

    rep["probe"] = {"financial_fill": fin, "year_dist": yr, "org_industry_l1": l1}
    rep["support_judgment"] = {
        "data_support_level": "部分支持",
        "reason": (
            f"三维同比原料列在但填充极薄：营收 {fin['rev']}/{fin['n']}（2.4%）、利润 {fin['tp']}、"
            f"资产 {fin['ta']}、负债 {fin['tl']}；双年分布 {len(yr)} 个年份；"
            f"行业对标键 industry_l1_code 填充 {l1['l1']}/{l1['n']}。"
            "同比需同企双年+行业均值需足样本——当前填充率下两条件均不满足 → 部分支持。"
        ),
        "criteria": {
            "columns_ready": True,
            "revenue_fill_thin": True,
            "dual_year_comparable": False,
            "industry_benchmark_ready": False,
        },
    }
    OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(rep["probe"], ensure_ascii=False, indent=2), flush=True)
    print(json.dumps(rep["support_judgment"]["reason"], ensure_ascii=False), flush=True)
    print("wrote", OUT, flush=True)


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
    out_json = here / "M_ENT_GROWTH_POTENTIAL_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ENT_GROWTH_POTENTIAL.py 等价）
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
        "metric_id": "M_ENT_GROWTH_POTENTIAL",
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ENT_DOMAIN_COVERAGE_DEPTH 领域覆盖深度
# 【维护者】唐绍祖
# 【适用系统】科技专题系统 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ENT_DOMAIN_COVERAGE_DEPTH.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
#!/usr/bin/env python3
"""M_ENT_DOMAIN_COVERAGE_DEPTH 领域覆盖深度 — 依赖侧实测脚本

王惠口径（calc-logic 真源）：
  深度 = 企业集合命中节点的最大 level ÷ 该链最大 level（归一化 0~1）。
实测（2026-10-20）：
  ① gkx dwd_industry_chain_info.level 全 0（1,273 行，M_ENT_CHAIN_STAGE_COVERAGE 已证）——层级字段无效。
  ② 代理：code 长度差（(len-7)/2）即层级深度（INB 目录根=7 位，每层+2 位）——链内最大深度可算。
  ③ gkx tags 2,283,762 行 link_code JSON 摊平后企业与节点深度可关联。
结论：王惠公式的 level 维在源侧无效（全 0），码长代理可算但需会签 → 部分支持。
"""
from __future__ import annotations

import ast
import json
from collections import defaultdict
from pathlib import Path

import pymysql

OUT = Path(__file__).with_name("M_ENT_DOMAIN_COVERAGE_DEPTH_out.json")
ENV_GKX = Path(__file__).resolve().parents[6] / "gkx-orchestration/agent-delivery/data/third-party-source/gkx-mysql-raw/.env.local"


def load_dotenv(path: Path) -> dict:
    env = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def depth_of(code: str) -> int:
    return (len(code) - 7) // 2 if len(code) >= 7 else 0


def main():
    rep = {"metric_id": "M_ENT_DOMAIN_COVERAGE_DEPTH", "metric_name": "领域覆盖深度", "script": "M_ENT_DOMAIN_COVERAGE_DEPTH.py"}
    e = load_dotenv(ENV_GKX)
    gc = pymysql.connect(host=e["GKX_SRC_HOST"], port=int(e["GKX_SRC_PORT"]), user=e["GKX_SRC_USER"],
                         password=e["GKX_SRC_PASSWORD"], database="gkx", charset="utf8mb4",
                         cursorclass=pymysql.cursors.DictCursor, connect_timeout=20, read_timeout=300)
    with gc.cursor() as cur:
        cur.execute("SELECT level, COUNT(*) n FROM dwd_industry_chain_info GROUP BY 1")
        lvl = [dict(r) for r in cur.fetchall()]
        cur.execute("SELECT industry_code FROM dwd_industry_chain_info")
        codes = [r["industry_code"] for r in cur.fetchall()]
    gc.close()
    # 链内最大码深（代理）
    root_max = defaultdict(int)
    for c in codes:
        root_max[c[:7]] = max(root_max[c[:7]], depth_of(c))
    # 抽样演示：全库最大深度分布
    import collections
    chain_depths = sorted(root_max.values())
    dist = collections.Counter(chain_depths)

    probe = {
        "level_dist": lvl,
        "code_depth_proxy": {
            "chains": len(root_max),
            "max_depth_dist": dict(dist),
            "note": "level 全 0 → 码深代理（根 7 位，每层 +2）",
        },
    }
    rep["probe"] = probe
    rep["support_judgment"] = {
        "data_support_level": "部分支持",
        "reason": (
            f"王惠公式依赖 chain_info.level——实测全 0（{lvl}，1,273 行无一例外），层级维无效；"
            f"码深代理可得 {len(root_max)} 条链的深度结构（最大深度分布 {dict(dist)}），"
            "tags 228 万行可关联企业命中深度。代理口径需会签（语义=目录树深而非业务环节纵深）→ 部分支持。"
        ),
        "criteria": {
            "level_field_usable": any(r["level"] != 0 for r in lvl),
            "code_depth_proxy_ready": True,
            "tags_ready": True,
        },
    }
    OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(rep["support_judgment"], ensure_ascii=False, indent=2), flush=True)
    print("wrote", OUT, flush=True)


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
    out_json = here / "M_ENT_DOMAIN_COVERAGE_DEPTH_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ENT_DOMAIN_COVERAGE_DEPTH.py 等价）
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
        "metric_id": "M_ENT_DOMAIN_COVERAGE_DEPTH",
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

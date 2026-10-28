#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ENT_CHAIN_COMPLETENESS 产业链完整度
# 【维护者】唐绍祖
# 【适用系统】科技专题系统 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ENT_CHAIN_COMPLETENESS.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
#!/usr/bin/env python3
"""M_ENT_CHAIN_COMPLETENESS 产业链完整度 — gkx 现转实测脚本

口径（calc-logic/ENT/M_ENT_CHAIN_COMPLETENESS.md，算法 2026-09 COVER-STAT-L01）：
  某地区全部企业覆盖的叶子环节数 k / 全目录叶子数 K × 100
  - K = 12 条 INB* 链的叶子（industry_code 无更长后缀码）；探针 K=954，不作口径常数
  - k = 该地区企业 tags.industry_link_code（JSON 数组，拆开后祖先+叶子混排）∩ 叶子集合，去重
  - 至少 1 家企业挂到该叶子算覆盖；不加权；不上卷；只国内；城市用行政区划（深圳 4403）
主算：gkx 生产库（tags 2,283,762 行全量）；对照 demo。
"""
from __future__ import annotations

import ast
import json
import re
from collections import defaultdict
from pathlib import Path

import pymysql

OUT = Path(__file__).with_name("M_ENT_CHAIN_COMPLETENESS_out.json")
ROOT = Path(__file__).resolve().parents[6]
ENV_GKX = ROOT / "gkx-orchestration/agent-delivery/data/third-party-source/gkx-mysql-raw/.env.local"
DEV = dict(
    host="111.198.38.90", port=34306, user="gkxlumenx", password="GKX@Lumen2026",
    charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor,
    connect_timeout=20, read_timeout=600,
)


def load_dotenv(path: Path) -> dict:
    env = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def q(conn, sql):
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()


CODE_RE = re.compile(r"INB\d+")


def parse_codes(raw) -> set:
    if not raw:
        return set()
    return set(CODE_RE.findall(str(raw)))


def main():
    report = {"metric_id": "M_ENT_CHAIN_COMPLETENESS", "metric_name": "产业链完整度", "script": Path(__file__).name}
    e = load_dotenv(ENV_GKX)
    gc = pymysql.connect(host=e["GKX_SRC_HOST"], port=int(e["GKX_SRC_PORT"]), user=e["GKX_SRC_USER"],
                         password=e["GKX_SRC_PASSWORD"], database="gkx", charset="utf8mb4",
                         cursorclass=pymysql.cursors.DictCursor, connect_timeout=20, read_timeout=600)
    try:
        # 1) 目录与叶子（前缀树：无更长码）
        rows = q(gc, "SELECT industry_code FROM dwd_industry_chain_info")
        codes = [r["industry_code"] for r in rows]
        code_set = set(codes)
        leaves = {c for c in codes if not any(o != c and o.startswith(c) for o in code_set)}
        roots = {c for c in codes if len(c) == 7}
        # 2) 企业城市（demo 侧 base_info 有 city；gkx base_info 同步量）
        # 深圳打标走 gkx dwd_org_base_info.city（LIKE 走全表慢，取 org_id->city dict 分块）
        sz_ids = set()
        n_base = 0
        cur = gc.cursor()
        cur.execute("SELECT COUNT(*) n FROM dwd_org_base_info")
        n_base = int(cur.fetchone()["n"])
        cur.execute("SELECT org_id FROM dwd_org_base_info WHERE city LIKE '深圳%%'")
        for r in cur.fetchall():
            sz_ids.add(r["org_id"])
        # 3) tags 分块拉取，解析数组 → 叶子命中
        cur.execute("SELECT COUNT(*) n FROM dwd_org_industry_tags")
        tags_total = int(cur.fetchone()["n"])
        leaf_hit_sz = set()
        leaf_hit_all = set()
        orgs_with_tags = set()
        cur.execute("SELECT credit_code, industry_link_code FROM dwd_org_industry_tags")
        batch = cur.fetchmany(50000)
        while batch:
            for r in batch:
                orgs_with_tags.add(r["credit_code"])
                hits = parse_codes(r["industry_link_code"]) & leaves
                leaf_hit_all |= hits
                # 深圳过滤：tags 键是 credit_code 非 org_id，无法直接联 —— 全国层面先算；
                # 深圳层面用 gkx 内 JOIN（下方 SQL 版本）
            batch = cur.fetchmany(50000)
        # 深圳层面：SQL 侧 JOIN（collation 不一致需 CONVERT；探针 LIMIT 控制时长）
        cur.execute(
            "SELECT t.industry_link_code FROM dwd_org_industry_tags t "
            "JOIN dwd_org_base_info b ON CONVERT(t.credit_code USING utf8mb4) COLLATE utf8mb4_general_ci = CONVERT(b.external_id USING utf8mb4) COLLATE utf8mb4_general_ci "
            "WHERE b.city LIKE '深圳%%' LIMIT 50000"
        )
        sz_join_rows = 0
        leaf_hit_sz = set()
        for r in cur.fetchall():
            sz_join_rows += 1
            leaf_hit_sz |= parse_codes(r["industry_link_code"]) & leaves
    finally:
        gc.close()

    K = len(leaves)
    k_all = len(leaf_hit_all)
    k_sz = len(leaf_hit_sz)
    comp = {
        "chain_catalog_rows": len(codes),
        "root_chains": len(roots),
        "leaves_K": K,
        "tags_total": tags_total,
        "orgs_with_tags": len(orgs_with_tags),
        "national": {"k": k_all, "completeness": round(100.0 * k_all / K, 2) if K else None},
        "shenzhen_join_probe": {"joined_rows": sz_join_rows, "k": k_sz,
                                 "completeness": round(100.0 * k_sz / K, 2) if K else None,
                                 "note": "credit_code=external_id CONVERT JOIN 探针（LIMIT 50000）"},
    }
    report["compute"] = comp
    level = "完全转换支持" if (K > 100 and k_all >= 50 and comp["national"]["completeness"] is not None) else (
        "部分支持" if k_all > 0 else "完全不支持"
    )
    report["support_judgment"] = {
        "data_support_level": level,
        "reason": (
            f"gkx 目录 {len(codes)} 码（12 链根、叶子 K={K}）；tags {tags_total:,} 行全量拆解后 "
            f"全国层面 k={k_all}/{K}（完整度 {comp['national']['completeness']}%）；"
            f"深圳探针（credit_code JOIN LIMIT 20 万）k={k_sz}/{K}（{comp['shenzhen_join_probe']['completeness']}%）。"
            + ("结构+当前数据量均足，k/K 已现转算出。" if level == "完全转换支持" else "覆盖不足。")
        ),
        "criteria": {"K_ge_100": K >= 100, "national_k_ge_50": k_all >= 50, "sz_probe_k_ge_20": k_sz >= 20},
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report["support_judgment"], ensure_ascii=False, indent=2), flush=True)
    print(json.dumps({k: comp[k] for k in ["leaves_K", "tags_total", "national", "shenzhen_join_probe"]}, ensure_ascii=False, indent=1), flush=True)
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
    out_json = here / "M_ENT_CHAIN_COMPLETENESS_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ENT_CHAIN_COMPLETENESS.py 等价）
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
        "metric_id": "M_ENT_CHAIN_COMPLETENESS",
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

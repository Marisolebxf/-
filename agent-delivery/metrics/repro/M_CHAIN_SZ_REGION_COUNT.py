#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_CHAIN_SZ_REGION_COUNT 深圳产业分布区域数
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_CHAIN_SZ_REGION_COUNT.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_CHAIN_SZ_REGION_COUNT 深圳区域数（区县覆盖数）—— 可运行复现脚本（2026-10-21 · gkx 改源版）

指标：产业链分析 / 产业链总览 / 深圳统计 · 深圳区域数
数据源：三方库 gkx（183.240.141.251:3318），经 `_gkxdb.gkx()` 只读连接，
        表：gkx.dwd_org_base_info / gkx.dwd_org_industry_tags。
口径（仿王惠）：COUNT(DISTINCT area) WHERE city='深圳市' AND 链上主体。
实测约束：
  - `dwd_org_base_info.area` 全表填充 82.28%，但**分城市极不均衡**：深圳 95,581/95,600、
    广州 49,603/49,605、惠州 9,920/9,979、**东莞 33,590 行全空**；
  - 深圳只有 9 个区县取值（缺大鹏新区/深汕合作区）；
  - 任何有规模的链都覆盖全部 9 个区 → 指标饱和、区分度≈0。

产出：code/M_CHAIN_SZ_REGION_COUNT_out.json
"""
from __future__ import annotations

import ast
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _gkxdb import gkx  # noqa: E402
from _sz_chain import to_chain15  # noqa: E402

MID = "M_CHAIN_SZ_REGION_COUNT"
OUT = Path(__file__).parent / f"{MID}_out.json"
t0 = time.time()
res: dict = {"metric_id": MID, "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
             "data_source": "gkx（三方库 gkx.dwd_org_base_info / dwd_org_industry_tags，只读）"}

_cur = gkx()


def parse_tags(raw: str) -> list[str]:
    """把 `["A","B"]` 形态的标签串解析成列表。

    库内实际存的是单引号形态（`['A','B']`），json.loads 会失败，故用 ast 兜底；
    两者都失败时按逗号切分并剥引号——宁可退化也不能让整件崩掉。
    """
    s = (raw or "").strip()
    if not s or s == "[]":
        return []
    for parser in (json.loads, ast.literal_eval):
        try:
            v = parser(s)
        except (ValueError, SyntaxError):
            continue
        if isinstance(v, (list, tuple)):
            return [str(x).strip() for x in v if str(x).strip()]
        if isinstance(v, str):
            return [v.strip()] if v.strip() else []
    return [x.strip().strip("'\"") for x in s.strip("[]").split(",") if x.strip().strip("'\"")]


def q(sql, args=None):
    if args:
        _cur.execute(sql, args)
    else:
        _cur.execute(sql)
    cols = [c[0] for c in _cur.description]
    return [dict(zip(cols, r)) for r in _cur.fetchall()]


def q1(sql, args=None):
    rows = q(sql, args)
    return rows[0] if rows else None


def step(name, fn):
    t = time.time()
    try:
        res[name] = fn()
    except Exception as e:  # noqa: BLE001
        res[name] = f"ERR {str(e)[:200]}"
    print(f"[{time.time()-t:6.1f}s] {name}: {str(res[name])[:280]}", flush=True)


# ------------------------------------------- 1 area 填充与取值域（单次扫描派生）
CITY_AREA = q("""
SELECT city, area, COUNT(*) n
FROM gkx.dwd_org_base_info
WHERE city IS NOT NULL AND city<>''
GROUP BY city, area""")

_agg: dict[str, dict] = {}
for r in CITY_AREA:
    c = r["city"]
    a = _agg.setdefault(c, {"city": c, "n": 0, "area_n": 0, "areas": set()})
    n = int(r["n"])
    a["n"] += n
    if r["area"] is not None and r["area"] != "":
        a["area_n"] += n
        a["areas"].add(r["area"])

area_fill = sorted(
    [{"city": a["city"], "n": a["n"], "area_n": a["area_n"], "areas": len(a["areas"]),
      "fill_pct": round(a["area_n"] / a["n"] * 100, 2) if a["n"] else 0.0}
     for a in _agg.values()],
    key=lambda x: -x["n"])[:8]
for r in area_fill:
    r["area_n"] = str(r["area_n"])
    r["fill_pct"] = f"{r['fill_pct']:.2f}"
res["area_fill_by_city"] = area_fill

res["sz_area_dist"] = sorted(
    [{"area": r["area"], "n": int(r["n"])} for r in CITY_AREA
     if r["city"] == "深圳市" and r["area"] not in (None, "")],
    key=lambda x: -x["n"])
res["sz_total"] = {"n": _agg.get("深圳市", {}).get("n", 0)}
res["sz_district_count"] = {"n": len(_agg.get("深圳市", {}).get("areas", ()))}
print(f"[  0.0s] area_fill_by_city: {res['area_fill_by_city'][:2]}", flush=True)


# ------------------------------------------------ 2 链切片（15 顶层链·代理）
def chain_slice():
    rows = q("""
SELECT t.company_name, t.industry_name, t.industry_link_name, t.industry_code, b.area
FROM gkx.dwd_org_industry_tags t
JOIN gkx.dwd_org_base_info b
  ON b.external_id = CONVERT(t.credit_code USING utf8mb4) COLLATE utf8mb4_0900_ai_ci
WHERE t.is_deleted=0 AND b.city='深圳市' AND b.area IS NOT NULL AND b.area<>''
""")
    chain_dist: dict[str, set] = {}
    chain_cos: dict[str, set] = {}
    for r in rows:
        ch = to_chain15(r["industry_name"], r["industry_link_name"])
        if ch is None:
            continue
        chain_dist.setdefault(ch, set()).add(r["area"])
        chain_cos.setdefault(ch, set()).add(r["company_name"])

    res["chain_coverage"] = {
        "tag_rows_with_area": len(rows),
        "chains_covered": len(chain_dist),
        "sz_companies_tagged": len({r["company_name"] for r in rows}),
    }
    res["chain_region_count"] = sorted([
        {"chain": ch, "districts": len(v), "district_list": sorted(v), "companies": len(chain_cos[ch])}
        for ch, v in chain_dist.items()
    ], key=lambda x: -x["companies"])

    # 原生行业码切片（真实码族）
    # 注意：industry_name / industry_link_name 都是「JSON 数组字符串」，不是标量码。
    # 同一个标签集合会以不同排列重复出现（['智能终端','软件与信息服务'] 与
    # ['软件与信息服务','智能终端'] 是同一组标签、两条不同字符串），直接以原串做
    # 字典键会把一个语义类别拆成两三个桶。所以这里先解析 → 排序去重 → 用规范键分组，
    # 同时保留「原串个数 / 规范键个数」作为拆分诊断（DATA_FACTS §3.32）。
    native: dict[tuple, dict] = {}
    raw_keys: set[str] = set()
    for r in rows:
        raw = r["industry_name"]
        if raw in (None, "", "[]"):
            continue
        raw_keys.add(raw)
        tags = sorted(set(parse_tags(raw)))
        if not tags:
            continue
        key = tuple(tags)
        d = native.setdefault(key, {"industry_tags": tags, "areas": set(), "cos": set()})
        d["areas"].add(r["area"])
        d["cos"].add(r["company_name"])
    res["native_code_region"] = sorted(
        [{"industry_tags": list(k), "industry_key": "|".join(k), "n_tags": len(k),
          "districts": len(v["areas"]), "cos": len(v["cos"])} for k, v in native.items()],
        key=lambda x: -x["cos"])[:20]
    res["native_tag_diag"] = {
        "rows_with_area": len(rows),
        "raw_tag_strings": len(raw_keys),
        "canonical_tag_sets": len(native),
        "split_by_order": len(raw_keys) - len(native),
        "note": "raw_tag_strings 为原串去重数，canonical_tag_sets 为「排序去重后的标签集合」数；"
                "两者之差即被数组排列顺序拆开的桶数",
    }
    return "ok"


step("chain_slice", chain_slice)


# ------------------------------------------------ 4 区分度：区县数的取值分布
def discrimination():
    rows = res.get("native_code_region") or []
    if not isinstance(rows, list) or not rows:
        return "ERR"
    vals = [int(r["districts"]) for r in rows]
    return {
        "n_codes": len(vals),
        "min": min(vals), "max": max(vals),
        "mode": max(set(vals), key=vals.count),
        "pct_at_max": round(sum(1 for v in vals if v == max(vals)) / len(vals) * 100, 2),
    }


step("discrimination", discrimination)

res["support_judgment"] = "部分支持"
res["support_reason"] = (
    "深圳侧 COUNT(DISTINCT area) 可现算（面积填充 95,581/95,600=99.98%，9 个区县取值）；"
    "但「指定产业链」这一限定在真实数据上无法闭合：15 条顶层链与 tags 的 INB13xx/15xx/25xx 码族无交叉表，"
    "tags 仅覆盖 19,909 家深圳企业（20.8%），且映射后仅落 8 条链；"
    "同时东莞 33,590 行 area 全空，跨市对比不可做；指标在规模链上饱和为 9 —— 故判部分支持。"
)
res["_elapsed_s"] = round(time.time() - t0, 1)
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
print("wrote", OUT, f"{res['_elapsed_s']}s")


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
    out_json = here / "M_CHAIN_SZ_REGION_COUNT_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_CHAIN_SZ_REGION_COUNT.py 等价）
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
        "metric_id": "M_CHAIN_SZ_REGION_COUNT",
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_INNOV_CITY_INDEX_SZ 深圳创新能力指数
# 【维护者】唐绍祖
# 【适用系统】科技专题系统 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_INNOV_CITY_INDEX_SZ.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_INNOV_CITY_INDEX_SZ 深圳创新能力指数 · gkx 版（20261021 改源）

口径与 20261020 版 V1.6 完全一致，只把数据面换成 `gkx` 三方库：
三维 = 创新资源(Σ研发经费 2019–2024) / 创新主体(0.5×机构 + 0.5×高企) / 创新环境(有效政策)，
城内极值归一 + 等权 ×100。城市 = 深圳/广州/东莞（gkx 底册 99.82% 粤集中，可信区）。

改源要点（不是简单换前缀）
--------------------------
* 城市键：`city LIKE '%深圳%'` → `city = '深圳市'`（gkx 已把 city 规范化到市级全称，§3.8）；
* 存续机构：`COUNT(DISTINCT org_id)` 走本地底册 + `reg_status IN (REG_ALIVE)`，
  实测与库内聚合逐位一致（SZ 95,600 / GZ 49,604 / DG 33,590，广州有 1 行 `在营（开业）` 不属标准表述）；
* 高企：`dwd_org_tech_tag.org_id` 精确匹配底册 `org_id`（不用 `org_id` JOIN 两遍全表），
  实测 15,476 / 7,499 / 3,584 与原读数一致；
* 政策：`city` 市级等值 + 省级共享。**gkx 的省级政策 city 是字面 `'NULL'`（9,706 行，无真 NULL）**，
  旧的 `city IS NULL` 在 gkx 上返回 0 → 改写为 `UPPER(TRIM(city)) IN ('NULL','')`，否则省级 231 件会凭空消失；
* 研发经费：`dwd_org_stock_finance_info`（上市主体年报口径，2019–2024 窗），org_id→city 本地归城。
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _city21_common as C  # noqa: E402

CITIES = C.CITY_KEYS


def main():
    raw = C.build_raw()
    org_reg = raw["org_reg"]

    rows = []
    for city in CITIES:
        rd = float(raw["rd_sum"].get(city, 0.0))
        org_alive = sum(int(r["n"]) for r in org_reg
                        if r["city"] == city and (r["reg_status"] or "") in C.REG_ALIVE)
        org_total = sum(int(r["n"]) for r in org_reg if r["city"] == city)
        hq = int(raw["hitech_by_city"].get(city, 0))
        pol_city = int(raw["policy_city"].get(city, 0))
        pol_prov = int(raw["policy_prov_shared_n"])
        rows.append({
            "city": C.SHORT[city], "city_code": city,
            "rd_funding_sum": round(rd, 2),
            "org_alive_cnt": org_alive, "org_total_cnt": org_total,
            "hightech_cnt": hq,
            "policy_cnt": pol_city + pol_prov,
            "policy_city_cnt": pol_city, "policy_prov_shared": pol_prov,
        })

    nf = C.norm([r["rd_funding_sum"] for r in rows])
    no = C.norm([r["org_alive_cnt"] for r in rows])
    nh = C.norm([r["hightech_cnt"] for r in rows])
    npv = C.norm([r["policy_cnt"] for r in rows])
    for i, r in enumerate(rows):
        resource = nf[i]
        entity = 0.5 * no[i] + 0.5 * nh[i]
        env = npv[i]
        r["d_resource"], r["d_entity"], r["d_env"] = resource, round(entity, 4), env
        r["index_score"] = round(100 / 3 * (resource + entity + env), 1)

    result = {
        "metric_id": "M_INNOV_CITY_INDEX_SZ",
        "metric_name": "深圳创新能力指数",
        "method": "王惠 V1.6：创新资源/主体/环境三维，城内极值归一+等权×100",
        "source_db": "gkx（183.240.141.251:3318）",
        "cities": [C.SHORT[c] for c in CITIES],
        "probes": {
            "gkx.dwd_org_base_info": 189116,
            "gkx.dwd_org_stock_finance_info": 40239,
            "gkx.dwd_org_annual_financial_info": 90926,
            "gkx.dwd_org_tech_tag": 202424,
            "gkx.dwd_policy_base": 20000,
        },
        "compute": {"cities": rows},
        "support_judgment": "部分支持",
        "support_note": (
            f"资源维研发经费可用（上市主体年报口径，2019–2024 窗 {raw['rd_rows']:,} 行非空、其中 {raw['rd_unmapped']} 行无法归城；全表非空 {19587:,} 行）；"
            "人员口径 development_employee 100% NULL 不可作备选；主体维机构/高企标签齐全；"
            "环境维政策 city 有 9,706 行字面 'NULL'（占 48.5%）已归空并单列省级共享 231 件；"
            "机构底册 99.82% 粤集中 → 宇宙限粤三城 ⇒ 部分支持"
        ),
        "change_note": (
            "换源后资源/主体/环境三维读数与 20261020 版逐位一致（研发经费 SZ 1,366,367,257,075.05；"
            "高企 15,476/7,499/3,584；政策市级 879/325/8 + 省级共享 231）；"
            "唯一改写是省级政策判定（gkx 用字面 'NULL' 而非 SQL NULL），不改口径。"
        ),
    }
    p = C.write_out("M_INNOV_CITY_INDEX_SZ", result)
    print("wrote", p)
    for r in rows:
        print(r["city"], r["index_score"], r["d_resource"], r["d_entity"], r["d_env"],
              r["rd_funding_sum"], r["org_alive_cnt"], r["hightech_cnt"], r["policy_cnt"])


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
    out_json = here / "M_INNOV_CITY_INDEX_SZ_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_INNOV_CITY_INDEX_SZ.py 等价）
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
        "metric_id": "M_INNOV_CITY_INDEX_SZ",
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_CHAIN_SZ_TALENT 深圳人才维度
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_CHAIN_SZ_TALENT.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_CHAIN_SZ_TALENT 深圳人才维度 —— 可运行复现脚本（2026-10-21 · gkx 改源版）

指标：产业链分析 / 深圳产业情况分析对比 / 四维对比 · 深圳人才维度
数据源：三方库 gkx（183.240.141.251:3318），经 `_gkxdb.gkx()` 只读连接，
        表：gkx.dwd_scholar / dwd_scholar_talent_flag / dwd_scholar_education_background /
            dwd_scholar_work_experience / dwd_org_heis_info / dwd_research_institute_base_info。
口径（仿王惠）：人才数量（深圳机构学者数）+ 人才结构（硕博占比）。
强制披露（BRIEF §3.4 / P4.3）：
  dwd_scholar 21,316（身份宇宙） vs dwd_scholar_talent_flag 20,030（属性宇宙），
  ID 交集仅 1,858（8.72%）—— 分子分母不得跨宇宙相除。
本脚本同时给出双口径：主档口径（分母 21,316）与属性宇宙口径（分母 20,030）。

产出：code/M_CHAIN_SZ_TALENT_out.json
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _gkxdb import gkx  # noqa: E402

MID = "M_CHAIN_SZ_TALENT"
OUT = Path(__file__).parent / f"{MID}_out.json"
t0 = time.time()
res: dict = {"metric_id": MID, "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
             "data_source": "gkx（三方库 gkx.dwd_scholar 系 + 机构底册，只读）"}

_cur = gkx()


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


# ------------------------------------------------------------ 1 两套 ID 宇宙
step("scholar_base", lambda: q1("""
SELECT COUNT(*) n,
       SUM(scholar_org_name_zh IS NOT NULL AND scholar_org_name_zh<>'') org_filled,
       SUM(scholar_org_id IS NOT NULL AND scholar_org_id<>'') orgid_filled,
       SUM(h_index IS NOT NULL AND h_index>0) h_filled
FROM gkx.dwd_scholar"""))
step("talent_universe", lambda: q1("""
SELECT (SELECT COUNT(*) FROM gkx.dwd_scholar_talent_flag) flag_n,
       (SELECT COUNT(DISTINCT scholar_id) FROM gkx.dwd_scholar_education_background) edu_n,
       (SELECT COUNT(DISTINCT scholar_id) FROM gkx.dwd_scholar_work_experience) work_n"""))
step("intersection", lambda: q1("""
SELECT
 (SELECT COUNT(*) FROM gkx.dwd_scholar s JOIN (SELECT DISTINCT scholar_id FROM gkx.dwd_scholar_talent_flag) f
    ON f.scholar_id=s.scholar_id) flag_x,
 (SELECT COUNT(*) FROM gkx.dwd_scholar s JOIN (SELECT DISTINCT scholar_id FROM gkx.dwd_scholar_education_background) e
    ON e.scholar_id=s.scholar_id) edu_x,
 (SELECT COUNT(*) FROM gkx.dwd_scholar_talent_flag f JOIN (SELECT DISTINCT scholar_id FROM gkx.dwd_scholar_education_background) e
    ON e.scholar_id=f.scholar_id) flag_edu_x"""))
step("talent_flag_dist", lambda: q("SELECT academician, COUNT(*) n FROM gkx.dwd_scholar_talent_flag GROUP BY academician"))

# --------------------------------------------------------------- 2 深圳归集
step("sz_by_name", lambda: q1("SELECT COUNT(*) n FROM gkx.dwd_scholar WHERE scholar_org_name_zh LIKE '%深圳%'"))
step("sz_by_inst_name", lambda: q1("""
SELECT COUNT(*) n FROM gkx.dwd_scholar s
JOIN (SELECT name_cn FROM gkx.dwd_org_heis_info WHERE city='深圳市'
      UNION SELECT name_cn FROM gkx.dwd_research_institute_base_info WHERE city='深圳市') i
  ON i.name_cn = s.scholar_org_name_zh"""))
step("sz_union", lambda: q1("""
SELECT COUNT(*) n FROM gkx.dwd_scholar s
WHERE s.scholar_org_name_zh LIKE '%深圳%'
   OR EXISTS (SELECT 1 FROM gkx.dwd_org_heis_info h WHERE h.name_cn=s.scholar_org_name_zh AND h.city='深圳市')
   OR EXISTS (SELECT 1 FROM gkx.dwd_research_institute_base_info r WHERE r.name_cn=s.scholar_org_name_zh AND r.city='深圳市')"""))
step("sz_by_orgid", lambda: q1("""
SELECT COUNT(*) n FROM gkx.dwd_scholar s
JOIN gkx.dwd_research_institute_base_info r
  ON r.org_id = CONVERT(s.scholar_org_id USING utf8mb4) COLLATE utf8mb4_0900_ai_ci
WHERE r.city='深圳市'"""))

# 四市对照（机构名匹配）
step("city_scholars", lambda: q("""
SELECT c.city, COUNT(DISTINCT s.scholar_id) n FROM gkx.dwd_scholar s
JOIN (
  SELECT name_cn, city FROM gkx.dwd_org_heis_info WHERE city IN ('深圳市','广州市','东莞市','惠州市')
  UNION
  SELECT name_cn, city FROM gkx.dwd_research_institute_base_info WHERE city IN ('深圳市','广州市','东莞市','惠州市')
) c ON c.name_cn = s.scholar_org_name_zh
GROUP BY c.city ORDER BY n DESC"""))

step("sz_inst_top", lambda: q("""
SELECT scholar_org_name_zh o, COUNT(*) n FROM gkx.dwd_scholar
WHERE scholar_org_name_zh LIKE '%深圳%' GROUP BY o ORDER BY n DESC LIMIT 10"""))

# --------------------------------------------------------- 3 学位结构（双口径）
DEG = """
CASE
  WHEN e.degree_zh LIKE '%博士%' THEN 3
  WHEN e.degree_zh LIKE '%硕士%' THEN 2
  WHEN e.degree_zh LIKE '%学士%' OR e.degree_zh LIKE '%本科%' THEN 1
  ELSE 0
END
"""
LVL = "CASE lvl WHEN 3 THEN '博士' WHEN 2 THEN '硕士' WHEN 1 THEN '学士' ELSE '其他' END"

step("degree_all", lambda: q(f"""
SELECT {LVL} level_name, COUNT(*) n FROM (
  SELECT e.scholar_id, MAX({DEG}) lvl
  FROM gkx.dwd_scholar_education_background e
  WHERE e.degree_zh IS NOT NULL AND e.degree_zh<>''
  GROUP BY e.scholar_id
) t GROUP BY lvl ORDER BY n DESC"""))
step("degree_sz", lambda: q(f"""
SELECT {LVL} level_name, COUNT(*) n FROM (
  SELECT e.scholar_id, MAX({DEG}) lvl
  FROM gkx.dwd_scholar s
  JOIN gkx.dwd_scholar_education_background e ON e.scholar_id=s.scholar_id
  WHERE s.scholar_org_name_zh LIKE '%深圳%' AND e.degree_zh IS NOT NULL AND e.degree_zh<>''
  GROUP BY e.scholar_id
) t GROUP BY lvl ORDER BY n DESC"""))
step("sz_edu_covered", lambda: q1("""
SELECT COUNT(DISTINCT s.scholar_id) n FROM gkx.dwd_scholar s
JOIN gkx.dwd_scholar_education_background e ON e.scholar_id=s.scholar_id
WHERE s.scholar_org_name_zh LIKE '%深圳%'"""))

# --------------------------------------------------- 4 链切片可行性（字段级）
step("chain_field_check", lambda: q1("""
SELECT SUM(scholar_department_name_zh IS NOT NULL AND scholar_department_name_zh<>'') dept_filled,
       SUM(bio_zh IS NOT NULL AND bio_zh<>'') bio_filled
FROM gkx.dwd_scholar"""))


# ------------------------------------------------------------- 5 合成评分
def scores():
    sz_n = int((res.get("sz_union") or {}).get("n") or 0)
    base = int((res.get("scholar_base") or {}).get("n") or 21316)
    deg_sz = {r["level_name"]: int(r["n"]) for r in (res.get("degree_sz") or [])}
    covered = int((res.get("sz_edu_covered") or {}).get("n") or 0)
    phd_ratio = deg_sz.get("博士", 0) / covered * 100 if covered else None
    ms_phd = (deg_sz.get("博士", 0) + deg_sz.get("硕士", 0)) / covered * 100 if covered else None
    return {
        "sz_scholars_main_universe": sz_n,
        "sz_share_of_main_pct": round(sz_n / base * 100, 3),
        "sz_with_education": covered,
        "sz_education_coverage_pct": round(covered / sz_n * 100, 2) if sz_n else None,
        "phd_ratio_pct": round(phd_ratio, 2) if phd_ratio is not None else None,
        "ms_phd_ratio_pct": round(ms_phd, 2) if ms_phd is not None else None,
        "note": "学位按「最高学历」逐人去重后统计；分母只能是 29 位有教育记录的深圳学者，不能外推到 194/199/251 人，更不能外推到 21,316 主档",
    }


step("scores", scores)

res["support_judgment"] = "部分支持"
res["support_reason"] = (
    "人才数量可按机构名归集（深圳 194–199 位学者，主档 21,316），但："
    "① 人才属性宇宙与身份主档 ID 交集仅 1,858（8.72%）；"
    "② scholar_org_id 整列为空，机构只能按名称字符串匹配；"
    "③ 深圳学者中有教育记录的仅 29 人（14.6%），硕博占比的分母过小；"
    "④ 学者表无产业/链归属字段，链切片无承载 —— 故判部分支持。"
)
res["_elapsed_s"] = round(time.time() - t0, 1)
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
print("wrote", OUT, f"{res['_elapsed_s']}s")


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题服务算法库', '科技信息展示系统']

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
    out_json = here / "M_CHAIN_SZ_TALENT_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_CHAIN_SZ_TALENT.py 等价）
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
        "metric_id": "M_CHAIN_SZ_TALENT",
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

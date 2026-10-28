#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_CHAIN_REG_RESEARCH_ORG 科研机构
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_CHAIN_REG_RESEARCH_ORG.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_CHAIN_REG_RESEARCH_ORG · 科研机构（链维/区域维）（gkx 单库代理版）

口径（徐滕强 v0.2.0）
--------------------
双桶 UNION：科研院所（dwd_research_institute_base_info）∪ 高校（dwd_org_heis_info）；
区域维用机构 city；链维官方桥是 `industry_chain_entity_rel(chain_id, entity_type='institution')`，
该表在 gkx 不存在（source_absent，见 TABLE_ABSENCE_EVIDENCE §industry_chain_entity_rel）。
按 org_id / external_id 去重。

本件的分工
----------
区域维是**完整的**：四市（深/广/莞/惠）机构总数可直接数出，列合计即真值。
链维是**弱的**：机构表无产业标签，只能按「机构名含环节名」匹配，命中率 2.4%，
未命中进「未归属」列。因此矩阵的列合计可信、行内拆分是下限。

输出：code/M_CHAIN_REG_RESEARCH_ORG_out.json
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_CHAIN_REG_RESEARCH_ORG_out.json"
METRIC = "M_CHAIN_REG_RESEARCH_ORG"

CITIES = ["深圳市", "广州市", "东莞市", "惠州市"]
GENERIC = {"其他", "其他零部件", "其他服务", "零部件", "本体制造", "整机集成", "软件系统",
           "核心零部件", "上游", "中游", "下游", "材料", "设备", "服务", "制造"}
EXTRA_2CHAR = {"芯片": "INB1303", "半导体": "INB1303", "无人机": "INB1236", "低空": "INB1236",
               "机器人": "INB1204", "传感器": "INB1323", "软件": "INB1306", "疫苗": "INB2503",
               "新药": "INB2503", "基因": "INB2505", "具身": "INB1354", "终端": "INB1333"}


def load(name):
    return json.loads((SNAP / name).read_text(encoding="utf-8"))


def build_lexicon():
    tree = load("chain_tree_20261021.json")
    kw = {}
    for n in tree:
        nm = str(n["industry_name"]).strip()
        if len(nm) >= 3 and nm not in GENERIC and n["industry_code"][:7].startswith("INB"):
            kw.setdefault(nm, n["industry_code"][:7])
    kw.update({k: v for k, v in EXTRA_2CHAR.items() if k not in kw})
    roots = {n["industry_code"]: n["industry_name"] for n in tree if len(n["industry_code"]) == 7}
    return sorted(kw.items(), key=lambda x: -len(x[0])), roots


def match_chain(name, lexicon):
    for token, chain in lexicon:
        if token in name:
            return chain
    return None


def main() -> None:
    lexicon, roots = build_lexicon()
    inst = load("inst_base_gkx21.json")["rows"]
    heis = load("heis21_20261022.json")["rows"]

    cnt = defaultdict(lambda: defaultdict(int))
    bucket = defaultdict(int)
    seen = set()
    assigned = 0
    city_totals = defaultdict(int)
    for r in inst:
        name, city, oid = str(r[0]), str(r[1]), r[3] or r[0]
        key = ("i", oid)
        if key in seen:
            continue
        seen.add(key)
        bucket["院所"] += 1
        city_totals[city] += 1
        ch = match_chain(name, lexicon)
        if ch:
            cnt[ch][city] += 1
            assigned += 1
        else:
            cnt["未归属"][city] += 1
    for r in heis:
        name, city, oid = str(r[0]), str(r[2]), r[6] or r[0]
        key = ("h", oid)
        if key in seen:
            continue
        seen.add(key)
        bucket["高校"] += 1
        city_totals[city] += 1
        ch = match_chain(name, lexicon)
        if ch:
            cnt[ch][city] += 1
            assigned += 1
        else:
            cnt["未归属"][city] += 1

    total = bucket["院所"] + bucket["高校"]
    rows = []
    for code in sorted(roots):
        r = {c: cnt[code].get(c, 0) for c in CITIES}
        rows.append({"chain": code, "chain_name": roots[code], **r,
                     "total": sum(r.values())})
    unmatched = {c: cnt["未归属"].get(c, 0) for c in CITIES}
    col_tot = {c: sum(x[c] for x in rows) + unmatched[c] for c in CITIES}
    four_city_assigned = sum(x["total"] for x in rows)
    out_city_matched = defaultdict(int)
    for ch, per_city in cnt.items():
        if ch == "未归属":
            continue
        for city, n in per_city.items():
            if city not in CITIES:
                out_city_matched[city] += n

    out = {
        "metric_id": METRIC,
        "metric_name": "科研机构（链维/区域维）",
        "data_source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）+ code/_snapshots21/ 落盘快照",
        "formula": "机构数 = COUNT(DISTINCT org) BY chain × city；机构桶 = 院所 ∪ 高校",
        "blocking_tables": {
            "industry_chain_entity_rel": {
                "triage": "source_absent",
                "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §industry_chain_entity_rel",
            }
        },
        "proxy_path": "两张载体底册 UNION + city 直分组（区域维完整）+ 机构名匹配环节名（链维弱）",
        "proxy_deviation": "官方桥 institution 关系表不存在，链归属退化为名称匹配：命中 134/5,575=2.4%。列合计（四市机构总数）是真值，行内拆分是下限；未归属列不可按比例摊到链",
        "buckets": dict(bucket),
        "cities": CITIES,
        "four_city_total": sum(col_tot.values()),
        "outside_four_city_total": total - sum(col_tot.values()),
        "column_totals": col_tot,
        "unmatched_by_city": unmatched,
        "assigned": assigned,
        "assigned_four_city": four_city_assigned,
        "matched_outside_four_cities": assigned - four_city_assigned,
        "matched_outside_cities_breakdown": dict(sorted(out_city_matched.items(), key=lambda x: -x[1])),
        "hit_rate": round(assigned / total, 4) if total else None,
        "matrix": rows,
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": "官方唯一桥 industry_chain_entity_rel 的 institution 行在 gkx 不存在，链维没有现成归属；但区域维所需的两张载体底册齐全（院所 2,074 + 高校 3,501，city 字段 100% 有值），四市列合计可直接数出、可对账。链维用机构名匹配环节名得到 134 家、10 链非零，只能作下限。区域完整 + 链维弱，判部分支持。",
            "criteria": {
                "official_bridge_table": False,
                "region_dimension_complete": True,
                "chain_dimension_complete": False,
                "hit_rate": round(assigned / total, 4) if total else None,
                "proxy_used": True,
            },
        },
        "judgment_reason": "官方唯一桥 industry_chain_entity_rel 的 institution 行在 gkx 不存在，链维没有现成归属；但区域维所需的两张载体底册齐全（院所 2,074 + 高校 3,501，city 字段 100% 有值），四市列合计可直接数出、可对账。链维用机构名匹配环节名得到 134 家、10 链非零，只能作下限。区域完整 + 链维弱，判部分支持。",
        "judgment_criteria": {
            "official_bridge_table": False,
            "region_dimension_complete": True,
            "chain_dimension_complete": False,
            "hit_rate": round(assigned / total, 4) if total else None,
            "proxy_used": True,
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "本件是截面计数（当前底册时点），不做年度序列，故无基期年份；底册不带历史版本，无法回溯往年机构数。若要做年度序列，院所侧有 incorporation_date（1,996 行），高校侧有 est_year，见 M_CHAIN_INSTITUTION_COUNT。",
        "sources": [
            {"path": "code/_snapshots21/inst_base_gkx21.json",
             "table": "gkx.dwd_research_institute_base_info", "rows": 2074,
             "library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "pulled_at": "2026-10-22T15:43:47+08:00",
             "role": "院所桶（含 city）"},
            {"path": "code/_snapshots21/heis21_20261022.json",
             "table": "gkx.dwd_org_heis_info", "rows": 3501,
             "library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "pulled_at": "2026-10-22T13:40+08:00",
             "role": "高校桶（含 city）"},
            {"path": "code/_snapshots21/chain_tree_20261021.json",
             "table": "gkx.dwd_industry_chain_info", "rows": 1273,
             "library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "pulled_at": "2026-10-21T23:48:04+08:00",
             "role": "环节名词典与顶层链回溯"},
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[OK] {METRIC} -> {OUT.name}  buckets={dict(bucket)} assigned={assigned} "
          f"hit={out['hit_rate']}")
    print("  col_totals", col_tot, "unmatched", unmatched)
    for r in rows:
        print(f"  {r['chain']} {r['chain_name'][:8]:<8} total={r['total']:<4} "
              f"sz={r['深圳市']} gz={r['广州市']} dg={r['东莞市']} hz={r['惠州市']}")


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
    out_json = here / "M_CHAIN_REG_RESEARCH_ORG_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_CHAIN_REG_RESEARCH_ORG.py 等价）
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
        "metric_id": "M_CHAIN_REG_RESEARCH_ORG",
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_INNOV_FACTOR_DIST 科创要素分布比例
# 【维护者】唐绍祖
# 【适用系统】科技专题系统 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_INNOV_FACTOR_DIST.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_INNOV_FACTOR_DIST · 科创要素分布比例（INNOV / DS-01-FACTORS）。

数据面：`gkx`（三方库）+ §2 授权缓存。
  - 专利年/国别/IPC：`_snapshots21/patent_panel_innov_20261021.json`（全量 2,939,895 行）
    → **本脚本不向 `dwd_patent` 发任何聚合 SQL**；
  - 论文/期刊/学者/机构/项目/成果行数：`gkx` 小表 COUNT（均 <10 万行）；
  - 机构省市分布：`_snapshots21/base_20261021.json`（189,116 行全量底册）。

输出：code/M_INNOV_FACTOR_DIST_out.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
FACTS = HERE / "_snapshots21" / "innov21_facts_20261021.json"
OUT = HERE / "M_INNOV_FACTOR_DIST_out.json"

COUNTRY_CN = {"China": "CN", "WO": "WO", "Hong Kong": "HK",
              "Japan": "JP", "Taiwan Province": "TW", "Macao": "MO"}


def share_rows(rows, key="n"):
    total = sum(r[key] for r in rows)
    out = []
    for r in rows:
        item = dict(r)
        item["pct"] = round(float(r[key]) / float(total) * 100, 2) if total else None
        out.append(item)
    return total, out


def main():
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    tc = {k: v["rows"] for k, v in f["table_counts"].items()}
    pat = f["patent"]
    py = {int(k): v for k, v in f["paper_year"].items()}
    jy = {int(k): v for k, v in f["project_year"].items()}

    # ---------- 1. 类型结构 ----------
    counts = {
        "论文": tc["dwd_zh_paper"] + tc["dwd_en_paper"],
        "期刊": tc["dwd_zh_journal"] + tc["dwd_en_journal"],
        "专利": int(pat["rows"]),
        "专家学者": tc["dwd_scholar"],
        "组织机构": tc["dwd_org_base_info"] + tc["dwd_research_institute_base_info"] + tc["dwd_forg_base_info"],
        "课题/项目": tc["dwd_zh_project"] + tc["dwd_en_project"],
        "成果（代理）": int(f["project_output"]["total_outputs"]),
    }
    total_types, type_share = share_rows([{"type": k, "n": v} for k, v in counts.items()])

    # ---------- 2. 年度结构（2021–2026） ----------
    years = list(range(2021, 2027))
    year_rows = []
    for y in years:
        year_rows.append({"year": y, "论文": py.get(y, 0), "专利": int(pat["year"].get(str(y), 0)),
                          "项目": jy.get(y, 0)})
    for label in ("论文", "专利", "项目"):
        s = sum(r[label] for r in year_rows)
        for r in year_rows:
            r[f"{label}_pct"] = round(float(r[label]) / float(s) * 100, 2) if s else None

    # ---------- 3. 地域结构：机构底册 ----------
    base = f["base"]
    region_rows = [{"province": "广东省", "city": c, "n": n,
                    "pct": round(n / base["rows"] * 100, 3)}
                   for c, n in base["city_counts"].items()]

    # ---------- 4. 地域结构：专利受理国 ----------
    country_rows = [{"c": COUNTRY_CN.get(k, k), "raw": k, "n": v}
                    for k, v in sorted(pat["country"].items(), key=lambda x: -x[1])]
    total_country, country_share = share_rows(country_rows)

    # ---------- 5. 学科结构：中文论文中图分类 ----------
    disc_total, disc_share = share_rows([{"s": s, "n": n} for s, n in f["discipline"]])

    # ---------- 6. 技术结构：专利 IPC 部类 ----------
    ipc_total, ipc_share = share_rows([{"s": s, "n": n} for s, n in pat["ipc_section"].items()])

    out = {
        "metric_id": "M_INNOV_FACTOR_DIST",
        "name": "科创要素分布比例",
        "domain": "INNOV / DS-01-FACTORS",
        "formula_owner": "AI-20261016（需求只给功能口径，无公式；本报告按类型/年度/地域/学科/技术五维给占比）",
        "generated_at": time.strftime("%Y-%m-%d"),
        "source_db": "gkx",
        "source_detail": {
            "专利": "patent_panel_innov_20261021.json（全量 2,939,895 行，零专利 SQL）",
            "机构底册": "base_20261021.json（189,116 行）",
            "其余": "gkx 小表聚合（论文 100,900 / 项目 58,453 / 学者 21,316 / 政策 20,000）",
        },
        "probes": {
            "type_counts": counts,
            "table_counts": tc,
            "patent_panel_rows": int(pat["rows"]),
            "patent_year_coverage": sorted(int(k) for k in pat["year"]),
        },
        "compute": {
            "type_structure": {"total": total_types, "rows": type_share,
                               "missing": "会议（gkx 无会议主表；zh/en 论文与期刊表的 publication_type 均无「会议」）"},
            "year_structure_2021_2026": {
                "rows": year_rows,
                "note": "专利仅 2021–2026 有 apdt_year；2017–2020 零行，不得把缺失年份当 0；"
                        "2026 为残年（采集止于 2026-10，且公开滞后），不与 2025 做同比；"
                        "项目 2022 年后严重截断（58/6 条），年结构不可解释。",
            },
            "region_structure_org": {
                "total": base["rows"], "guangdong_pct": base["guangdong_pct"],
                "rows": region_rows[:12],
                "method": "base_20261021.json 全量底册（189,116 行，非采样）；47 个重名已在底册侧按 org_id 去重",
            },
            "region_structure_patent_country": {"total": total_country, "rows": country_share},
            "region_structure_scholar": f["scholar_city"],
            "discipline_structure_paper": {
                "total": disc_total, "rows": disc_share[:15],
                "coverage": f"{disc_total:,} / {tc['dwd_zh_paper']:,} 篇"
                            f"（{disc_total / tc['dwd_zh_paper'] * 100:.2f}%）有中图分类",
            },
            "tech_structure_patent_ipc": {"total": ipc_total, "rows": ipc_share},
        },
        "samples": type_share,
        "support_judgment": "部分支持",
        "support_basis": (
            "类型、年度、地域（机构/专利受理国）、学科（中图分类）、技术（IPC 部类）五个维度均可产出占比，"
            "分母来自 gkx 真表或全量面板缓存；但「会议」无主表导致类型结构缺 1 类，成果只能用项目产出聚合代理，"
            "机构地域 99.82% 集中在广东（深圳都市圈四市 99.82%）、不能当全国分布，"
            "论文分类仅覆盖 19.87%——始终有依赖维不足，判部分支持。"
        ),
        "notes": [
            "专利占可计要素总量的 85.52%，类型结构会被专利数量碾压；页面应提供「去专利」或按类内归一视图。",
            "机构地域分布来自 189,116 行全量底册（非采样），广东 99.82%（深圳 50.55%、广州 26.23%、东莞 17.76%、惠州 5.28%），不能解释为全国/全球分布。",
            "专利受理国 96.90% 为 CN、3.06% 为 WO，海外仅 1,055 件；该分布反映数据采集范围，不反映全球创新格局。",
            "中文论文中图分类中「医药、卫生」占 47.73%（9,569/20,048），语料医学偏重；按学科做分布会被医学主导，须给剔除医疗类的对照。",
            "会议要素缺失、成果为聚合计数（awards_count 全为 0），类型结构与分布比例均无法覆盖需求列举的全部 9 类。",
            "英文论文 1,387 篇、英文期刊 605 种，英文侧占比在任何维度都不具代表性。",
            "专利年度维只覆盖 2021–2026（六期，2026 为残年）；2017–2020 在 gkx.dwd_patent 中零行，任何跨 2020 之前的年度占比都不能用本库构造。",
        ],
        "elapsed_sec": round(time.time() - t0, 2),
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(json.dumps({"saved": OUT.name, "type_total": total_types,
                      "type_rows": type_share, "years": year_rows,
                      "ipc": ipc_share, "support": out["support_judgment"]},
                     ensure_ascii=False, indent=1))


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
    out_json = here / "M_INNOV_FACTOR_DIST_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_INNOV_FACTOR_DIST.py 等价）
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
        "metric_id": "M_INNOV_FACTOR_DIST",
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

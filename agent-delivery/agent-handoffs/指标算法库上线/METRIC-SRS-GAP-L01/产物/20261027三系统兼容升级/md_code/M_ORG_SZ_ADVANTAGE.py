#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ORG_SZ_ADVANTAGE 深圳科研机构优势
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ORG_SZ_ADVANTAGE.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_ORG_SZ_ADVANTAGE · 深圳科研机构优势（ORG 域）

需求锚点：算法库序号 151 ——「构建覆盖科研成果水平、科研经费投入、人才队伍素质的评价体系，
深圳与全国科研机构数据进行对标分析，量化识别优势与不足」；
展示系统 §1.1.1.2.4.2.4.9「深圳科研机构优势分析」。

本件先回答一个前置问题：**能不能对标全国？** 不能。三条实测证据：
  1. 机构底册 2,074 家 100% 在广东省（深圳 1,014 / 广州 822 / 东莞 127 / 惠州 111），
     省外机构 0 家；
  2. 专利的城市归属由「申请人名 → 企业底册城市」离线 join 得到，北京只命中 638 件、
     上海 4 件（`_snapshots_gkx21/city_patent_year_gkx.json` 的 city_totals），
     这不是北京/上海专利少，而是映射链只覆盖都市圈；
  3. 论文城市白名单只 11 城（深圳/广州/东莞/惠州/中山/佛山/香港/珠海…），北京上海不在其中。
所以本件把口径收缩为**深圳都市圈四市对标**（深/广/莞/惠），并在正文把「全国对标不可做」写死。

本件口径（零 SQL）：
  总量指数 = 5 维（机构数 / 专利 / 论文 / 项目 / 学者）各城 min-max 后等权平均 ×100
  强度指数 = 4 维人均当量（专利/机构、论文/机构、项目/机构、学者/机构）同法
  辅助列（不进指数）：专利授权率、项目经费/机构、政策提及/机构

硬边界：
  - 底册只收「登记为科研机构」的主体（研究院/研究生院/创新中心/民非），
    **不收高校本部**：深圳大学、南方科技大学本体不在底册，只有「深圳大学龙岗创新研究院」
    「南方科技大学坪山生物医药研究院」这类分支。这会系统性压低深圳的论文/项目/学者三项。
  - 「科研经费投入」维全缺（年报财务表对底册命中 0 行），只能用项目资助额代替。
"""
from __future__ import annotations

import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _org_m21_common as M  # noqa: E402

MID = "M_ORG_SZ_ADVANTAGE"
CITIES = ["深圳市", "广州市", "东莞市", "惠州市"]
CITY_SHORT = {"深圳市": "深圳", "广州市": "广州", "东莞市": "东莞", "惠州市": "惠州"}


def main() -> None:
    panel = M.load_panel()
    inst = panel["institutions"]
    paper_city = M.load_paper_city()
    city_patent = M.OC.load_json(os.path.join(HERE, "_snapshots_gkx21",
                                              "city_patent_year_gkx.json"))

    raw = {}
    for c in CITIES:
        sub = [x for x in inst if x["city"] == c]
        raw[c] = {
            "orgs": len(sub),
            "patents": sum(x["patents"] for x in sub),
            "patent_grant": sum(x["patent_grant"] for x in sub),
            "papers": sum(x["papers"] for x in sub),
            "projects": sum(x["projects"] for x in sub),
            "scholars": sum(x["scholars"] for x in sub),
            "fund_wan": round(sum(float(x.get("project_fund") or 0) for x in sub), 1),
            "policy_mentions": sum(x["policy_mentions"] for x in sub),
            "tech_tags": sum(1 for x in sub if x.get("tags")),
            "with_patents": sum(1 for x in sub if x["patents"]),
            "with_papers": sum(1 for x in sub if x["papers"]),
            "with_projects": sum(1 for x in sub if x["projects"]),
            "with_scholars": sum(1 for x in sub if x["scholars"]),
            "org_type": dict(Counter(x["org_type"] for x in sub).most_common()),
        }

    dims_total = ["orgs", "patents", "papers", "projects", "scholars"]
    idx_total = {c: {} for c in CITIES}
    for d in dims_total:
        vals = [raw[c][d] for c in CITIES]
        mm = M.minmax(vals)
        for c, v in zip(CITIES, mm):
            idx_total[c][d] = v
    for c in CITIES:
        idx_total[c]["index"] = round(sum(idx_total[c][d] for d in dims_total) / len(dims_total), 2)

    dims_int = ["patents_per_org", "papers_per_org", "projects_per_org", "scholars_per_org"]
    per_org = {c: {
        "patents_per_org": round(raw[c]["patents"] / raw[c]["orgs"], 3),
        "papers_per_org": round(raw[c]["papers"] / raw[c]["orgs"], 3),
        "projects_per_org": round(raw[c]["projects"] / raw[c]["orgs"], 3),
        "scholars_per_org": round(raw[c]["scholars"] / raw[c]["orgs"], 4),
    } for c in CITIES}
    idx_int = {c: {} for c in CITIES}
    for d in dims_int:
        mm = M.minmax([per_org[c][d] for c in CITIES])
        for c, v in zip(CITIES, mm):
            idx_int[c][d] = v
    for c in CITIES:
        idx_int[c]["index"] = round(sum(idx_int[c][d] for d in dims_int) / len(dims_int), 2)

    # 辅助列：授权率、经费/机构、政策/机构
    aux = {}
    for c in CITIES:
        r = raw[c]
        aux[c] = {
            "grant_rate": round(r["patent_grant"] / r["patents"], 4) if r["patents"] else None,
            "fund_per_org_wan": round(r["fund_wan"] / r["orgs"], 2),
            "policy_per_org": round(r["policy_mentions"] / r["orgs"], 4),
        }

    # 排名与强弱项
    ranks = {}
    for d in dims_total:
        order = sorted(CITIES, key=lambda c: -raw[c][d])
        for i, c in enumerate(order, 1):
            ranks.setdefault(c, {})[d] = i
    for c in CITIES:
        ranks[c]["index"] = sorted(CITIES, key=lambda x: -idx_total[x]["index"]).index(c) + 1
        ranks[c]["index_int"] = sorted(CITIES, key=lambda x: -idx_int[x]["index"]).index(c) + 1
    sz_rank = ranks["深圳市"]

    # ---- 全国对标不可做的三条证据 ----
    national = {
        "roster_province": {p: sum(1 for x in inst if x["province"] == p)
                            for p in {x["province"] for x in inst}},
        "roster_cities": dict(Counter(x["city"] for x in inst).most_common()),
        "patent_city_totals": {c: city_patent["city_totals"].get(c) for c in
                               ["深圳市", "广州市", "东莞市", "惠州市",
                                "北京市", "上海市", "杭州市", "成都市"]},
        "patent_city_note": ("city_totals 由「申请人名→企业底册城市」离线 join 得到，"
                             "底册 99.82% 是深圳都市圈，所以北京/上海读数是个位数到几百，"
                             "**不能读成专利量**，只能读成映射覆盖。"),
        "paper_city_whitelist_n": len({k.split("|")[0] for k in paper_city["first_city_year"]}),
        "paper_city_whitelist": sorted({k.split("|")[0] for k in paper_city["first_city_year"]}),
        "paper_city_note": ("作者单位串只解析出 11 个都市圈城市，北京/上海不在白名单；"
                            "全国论文维同样不可得。"),
        "university_note": ("底册只收登记为科研机构的主体，不收高校本部：深圳大学、南方科技大学"
                            "本体不在底册（仅有深圳大学龙岗创新研究院等分支），这会压低深圳的"
                            "论文/项目/学者三项，是结构性口径而不是深圳真实产出。"),
    }

    # 集中度：单城 top5 机构占该城产出比重
    conc = {}
    for c in CITIES:
        sub = [x for x in inst if x["city"] == c]
        for d in ("patents", "papers"):
            tot = raw[c][d]
            top = sorted((x[d] for x in sub), reverse=True)[:5]
            conc.setdefault(c, {})[d] = {
                "top5": sum(top), "total": tot,
                "share": round(sum(top) / tot, 4) if tot else None,
                "top1_name": max(sub, key=lambda x: x[d])["name"] if sub else None,
                "top1_val": max((x[d] for x in sub), default=0),
            }
    # 单家极值剔除：广州中医药大学（广州中医药研究院）以高校本体入册，1,265 篇
    GZ_EDGE = "广州中医药大学（广州中医药研究院）"
    excl = {c: dict(raw[c]) for c in CITIES}
    for x in inst:
        if x["name"] == GZ_EDGE:
            excl[x["city"]]["papers"] -= x["papers"]
    idx_excl = {c: {} for c in CITIES}
    for d in dims_total:
        mm = M.minmax([excl[c][d] for c in CITIES])
        for c, v in zip(CITIES, mm):
            idx_excl[c][d] = v
    for c in CITIES:
        idx_excl[c]["index"] = round(sum(idx_excl[c][d] for d in dims_total) / len(dims_total), 2)
    excl_note = {
        "excluded_entity": GZ_EDGE,
        "excluded_papers": next((x["papers"] for x in inst if x["name"] == GZ_EDGE), 0),
        "why": ("该主体是广州中医药大学校本部以「研究院」名义登记入册，1,265 篇占广州论文总量 50.3%；"
                "深圳的同类主体（深圳大学、南方科技大学）未入册。剔除后重算，用于判断广州论文领先"
                "有多少来自登记口径。"),
        "papers_after": {CITY_SHORT[c]: excl[c]["papers"] for c in CITIES},
        "index_after": {CITY_SHORT[c]: idx_excl[c]["index"] for c in CITIES},
    }

    # 机构类型结构（民非占比 → 新型研发机构特征）
    type_share = {}
    for c in CITIES:
        n = raw[c]["orgs"]
        type_share[CITY_SHORT[c]] = {
            "民办非企业单位": round(raw[c]["org_type"].get("民办非企业单位", 0) / n, 4),
            "事业单位": round(raw[c]["org_type"].get("事业单位", 0) / n, 4),
            "other": round(1 - (raw[c]["org_type"].get("民办非企业单位", 0)
                                + raw[c]["org_type"].get("事业单位", 0)) / n, 4),
        }

    # 权重敏感性（总量指数）
    schemes = [("等权 5 维", {d: .2 for d in dims_total}),
               ("规模优先（机构数 0.40）", {"orgs": .40, "patents": .20, "papers": .15,
                                        "projects": .15, "scholars": .10}),
               ("产出优先（专利+论文 0.70）", {"orgs": .10, "patents": .35, "papers": .35,
                                         "projects": .10, "scholars": .10}),
               ("人才优先（学者 0.40）", {"orgs": .10, "patents": .15, "papers": .20,
                                       "projects": .15, "scholars": .40})]
    sens = []
    for label, W in schemes:
        sc = {c: round(sum(W[d] * idx_total[c][d] for d in dims_total) / sum(W.values()), 2)
              for c in CITIES}
        order = sorted(CITIES, key=lambda c: -sc[c])
        sens.append({"weights": label, "order": [CITY_SHORT[c] for c in order],
                     "scores": {CITY_SHORT[c]: sc[c] for c in CITIES},
                     "sz_rank": order.index("深圳市") + 1})

    out = {
        "metric_id": MID,
        "metric_name": "深圳科研机构优势",
        "domain": "ORG / 深圳科研机构优势分析（算法库 151 / 展示系统 §1.1.1.2.4.2.4.9）",
        "formula_owner": "AI-20261022（推测定义，wanghui=false）",
        "support_judgment": "部分支持",
        **M.base_years(
            [2021, 2022, 2023, 2024, 2025, 2026], [2017, 2018, 2019, 2020],
            "专利为 2021—2026 存量（2017—2020 库内零行，不按 0 摊入；2026 残年）；"
            "论文 1980—2026、项目 1986—2022 为累计口径，城市间同口径可比。"
            "本件不做增速，故不需要同比基期；缺失年不进任何分母。"),
        "inputs": {
            "roster": "gkx.dwd_research_institute_base_info 2,074 家（100% 广东省）",
            "panel": "_snapshots21/org_family_panel_20261021.json",
            "city_patent": "_snapshots_gkx21/city_patent_year_gkx.json（申请人→底册城市）",
            "paper_city": "_snapshots21/papers_city_year_gkx21.json（11 城白名单）",
        },
        "scope": {
            "declared_by_requirement": "深圳 vs 全国",
            "actual": "深圳 vs 广州/东莞/惠州（都市圈四市）",
            "why": "省外机构 0 家；专利城市映射与论文城市白名单都只覆盖都市圈（见 national_check）",
        },
        "national_check": national,
        "dims": {
            "total_index": {"dims": dims_total, "weights": {d: .2 for d in dims_total},
                            "normalization": "四城截面 min-max → 等权平均 ×100"},
            "intensity_index": {"dims": dims_int,
                                "weights": {d: .25 for d in dims_int},
                                "normalization": "先除机构数（人均当量），再四城 min-max 等权"},
            "auxiliary_not_in_index": ["grant_rate", "fund_per_org_wan", "policy_per_org"],
            "why_two_indices": "总量指数受机构数量驱动；强度指数剥离规模。两者结论相反时，"
                               "说明优势来自「多」而不是「强」，必须分开呈现。",
        },
        "raw": raw,
        "per_org": per_org,
        "index_total": idx_total,
        "index_intensity": idx_int,
        "ranks": ranks,
        "aux": aux,
        "sz_strength_weakness": {
            "strength": [d for d in dims_total if sz_rank.get(d) == 1],
            "weakness": [d for d in dims_total if sz_rank.get(d) == 4],
            "middle": [d for d in dims_total if sz_rank.get(d) in (2, 3)],
            "note": "排名只在四市内；「弱」不等于低于全国均值，因为全国样本不存在。",
        },
        "sensitivity": sens,
        "concentration": conc,
        "sens_exclude_single_entity": excl_note,
        "org_type_share": type_share,
        "limits": [
            "全国对标不可做：底册 100% 广东省，省外机构 0 家；专利城市映射只覆盖都市圈；"
            "论文城市白名单 11 城不含北京/上海。",
            "「科研经费投入」维全缺：年报财务表对底册 2,074 家命中 0 行，只能用项目资助额代替，"
            "且项目经费是全周期累计、含 1986 年以来项目。",
            "高校本部不在底册（深圳大学、南方科技大学），深圳的论文/项目/学者被系统性低估；"
            "广州因中大、华工等高校的下属研究院在册，读数相对占优。",
            "学者库只命中 29 家 / 145 人，学者维几乎不具区分度，却仍占总量指数 1/5 权重。",
            "论文 2024 年是采集口径尖峰，累计口径受影响但方向不变。",
            "四城 min-max 使最小城市恒为 0、最大恒为 100，城市间差距被压缩成相对值，不能读成绝对差距倍数。",
        ],
    }
    path = M.write_out(out, MID)
    print("wrote", path)
    print("raw", {CITY_SHORT[c]: {k: raw[c][k] for k in dims_total} for c in CITIES})
    print("index_total", {CITY_SHORT[c]: idx_total[c]["index"] for c in CITIES})
    print("index_int", {CITY_SHORT[c]: idx_int[c]["index"] for c in CITIES})
    print("ranks SZ", sz_rank)
    print("sens", [(s["weights"], s["order"]) for s in sens])


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
    out_json = here / "M_ORG_SZ_ADVANTAGE_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ORG_SZ_ADVANTAGE.py 等价）
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
        "metric_id": "M_ORG_SZ_ADVANTAGE",
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

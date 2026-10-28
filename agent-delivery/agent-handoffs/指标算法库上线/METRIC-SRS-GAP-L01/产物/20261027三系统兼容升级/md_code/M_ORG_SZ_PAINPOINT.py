#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ORG_SZ_PAINPOINT 深圳科研机构痛难点
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统
# 【差异分级】D2 口径级分歧（本件复核为可兼容·配置型） ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ORG_SZ_PAINPOINT.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""
M_ORG_SZ_PAINPOINT｜深圳科研机构痛难点

零 DB：只读 code/_snapshots21/org_family_panel_20261021.json（gkx 侧
dwd_research_institute_base_info 2,074 行 + 专利/论文/项目/政策/转移的机构级聚合）
+ code/_probe_blocked_f2_20261023.json（合作关系表负证据）。

口径：
  - 母体 = 科研机构底册 2,074 家；深圳切片 1,014 家（city='深圳市'，A 口径=注册地，P13）。
  - 四条可算痛点维（每维都要求「有值 / 总量 / 集中度」三件套）：
      ① 项目获取：projects / project_fund
      ② 成果转化：transfer_in + transfer_out
      ③ 学术产出：papers / patents
      ④ 政策触达：policy_mentions
  - 拒拟维：合作关系（enterprise_cooperation 在 gkx 不存在，见 absence_probe）。
  - 四城对照用 min-max 归一后的「痛点分」= 100×(max−x)/(max−min)，只在四市之间可比，
    不外推全国。

复现：cd code && python3 M_ORG_SZ_PAINPOINT.py
"""
from __future__ import annotations

import json
import os
import statistics as st
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_ORG_SZ_PAINPOINT_out.json")
PANEL = os.path.join(SNAP, "org_family_panel_20261021.json")
PROBE = os.path.join(HERE, "_probe_blocked_f2_20261023.json")

ID = "M_ORG_SZ_PAINPOINT"
CITIES = ("深圳市", "广州市", "东莞市", "惠州市")


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def hhi(vals):
    s = sum(vals)
    if s <= 0:
        return None
    return round(sum((v / s) ** 2 for v in vals if v > 0), 6)


def top_share(vals, k=5):
    s = sum(vals)
    if s <= 0:
        return None
    return round(sum(sorted(vals, reverse=True)[:k]) / s * 100, 4)


def minmax_pain(values: dict) -> dict:
    lo, hi = min(values.values()), max(values.values())
    if hi <= lo:
        return {c: 50.0 for c in values}
    return {c: round(100 * (hi - v) / (hi - lo), 2) for c, v in values.items()}


def main() -> int:
    d = load(PANEL)
    inst = d["institutions"]
    sz = [i for i in inst if i["city"] == "深圳市"]

    # ---------- 四城基线 ----------
    city_base = {}
    for c in CITIES:
        a = [i for i in inst if i["city"] == c]
        n = len(a)
        city_base[c] = {
            "institutes": n,
            "with_projects": sum(1 for i in a if i["projects"] > 0),
            "projects": sum(i["projects"] for i in a),
            "project_fund_total": round(sum(i["project_fund"] for i in a), 2),
            "with_transfer": sum(1 for i in a if i["transfer_in"] + i["transfer_out"] > 0),
            "transfer_events": sum(i["transfer_in"] + i["transfer_out"] for i in a),
            "with_papers": sum(1 for i in a if i["papers"] > 0),
            "papers": sum(i["papers"] for i in a),
            "with_patents": sum(1 for i in a if i["patents"] > 0),
            "patents": sum(i["patents"] for i in a),
            "patent_grants": sum(i["patent_grant"] for i in a),
            "with_policy": sum(1 for i in a if i["policy_mentions"] > 0),
            "policy_mentions": sum(i["policy_mentions"] for i in a),
            "scholars": sum(i["scholars"] for i in a),
            "people": sum(i["people"] for i in a),
        }
        n_ = city_base[c]["institutes"]
        city_base[c]["per_100_projects"] = round(city_base[c]["projects"] / n_ * 100, 4)
        city_base[c]["per_100_transfer"] = round(city_base[c]["transfer_events"] / n_ * 100, 4)
        city_base[c]["per_100_papers"] = round(city_base[c]["papers"] / n_ * 100, 4)
        city_base[c]["per_100_patents"] = round(city_base[c]["patents"] / n_ * 100, 4)
        city_base[c]["per_100_policy"] = round(city_base[c]["policy_mentions"] / n_ * 100, 4)

    # ---------- 深圳四维 ----------
    sz_proj = [i["projects"] for i in sz]
    sz_fund = [i["project_fund"] for i in sz]
    sz_trans = [i["transfer_in"] + i["transfer_out"] for i in sz]
    sz_paper = [i["papers"] for i in sz]
    sz_patent = [i["patents"] for i in sz]
    sz_policy = [i["policy_mentions"] for i in sz]

    def dim_block(vals, fund=None):
        pos = [v for v in vals if v > 0]
        return {
            "with_value": len(pos),
            "total": round(sum(vals), 2),
            "median_of_positive": st.median(pos) if pos else None,
            "p90_of_positive": sorted(pos)[int(len(pos) * 0.9) - 1] if len(pos) >= 10 else None,
            "max": max(vals) if vals else None,
            "hhi": hhi(vals),
            "top5_share_pct": top_share(vals, 5),
            "zero_share_pct": round((len(vals) - len(pos)) / len(vals) * 100, 4),
            "fund_total": round(sum(fund), 2) if fund else None,
            "fund_top5_share_pct": top_share(fund, 5) if fund else None,
        }

    dims = {
        "project": dim_block(sz_proj, sz_fund),
        "transfer": dim_block(sz_trans),
        "paper": dim_block(sz_paper),
        "patent": dim_block(sz_patent),
        "policy": dim_block(sz_policy),
    }

    # ---------- 四城痛点分 ----------
    subs = {
        "project_per_100": minmax_pain({c: city_base[c]["per_100_projects"] for c in CITIES}),
        "transfer_per_100": minmax_pain({c: city_base[c]["per_100_transfer"] for c in CITIES}),
        "paper_per_100": minmax_pain({c: city_base[c]["per_100_papers"] for c in CITIES}),
        "patent_per_100": minmax_pain({c: city_base[c]["per_100_patents"] for c in CITIES}),
        "policy_per_100": minmax_pain({c: city_base[c]["per_100_policy"] for c in CITIES}),
    }

    # ---------- 机构级「多维薄弱」 ----------
    ident = [i for i in sz if (i["projects"] + i["transfer_in"] + i["transfer_out"]
                               + i["papers"] + i["patents"] + i["policy_mentions"]
                               + i["scholars"] + i["people"]) > 0]
    q = {}
    for k, getter in (("project", lambda i: i["projects"]),
                      ("transfer", lambda i: i["transfer_in"] + i["transfer_out"]),
                      ("paper", lambda i: i["papers"]),
                      ("patent", lambda i: i["patents"]),
                      ("policy", lambda i: i["policy_mentions"])):
        vals = sorted(getter(i) for i in ident if getter(i) > 0)
        q[k] = st.quantiles(vals, n=4)[0] if len(vals) >= 4 else (min(vals) if vals else 0)

    weak_dist = Counter()
    weak_rows = []
    for i in ident:
        v = {"project": i["projects"], "transfer": i["transfer_in"] + i["transfer_out"],
             "paper": i["papers"], "patent": i["patents"], "policy": i["policy_mentions"]}
        weak = [k for k, x in v.items() if x > 0 and x <= q[k]]
        avail = [k for k, x in v.items() if x > 0]
        weak_dist[len(weak)] += 1
        if len(weak) >= 2:
            weak_rows.append({"name": i["name"], "weak_dims": weak, "available_dims": len(avail)})
    weak_rows.sort(key=lambda r: (-len(r["weak_dims"]), r["name"]))

    # ---------- 头部集中 ----------
    top_proj = sorted(sz, key=lambda i: -i["projects"])[:5]
    top_paper = sorted(sz, key=lambda i: -i["papers"])[:5]
    top_patent = sorted(sz, key=lambda i: -i["patents"])[:5]

    pop_block = {
        "shenzhen": len(sz),
        "org_type_shenzhen": dict(Counter(i["org_type"] or "（空）" for i in sz)),
        "area_top": Counter(i["area"] or "（空）" for i in sz).most_common(10),
    }

    out = {
        "metric": ID,
        "metric_name": "深圳科研机构痛难点",
        "support_judgment": "部分支持",
        "verdict_kind": "partial_with_gaps",
        "generated_at": "2026-10-23T04:46:00+08:00",
        "sources": {
            "db": "gkx",
            "host": "183.240.141.251:3318",
            "user": "gkx_reader_zp",
            "mode": "read-only",
            "tables": [
                "gkx.dwd_research_institute_base_info",
                "gkx.dwd_patent_transfer",
                "gkx.dwd_zh_project",
                "gkx.dwd_zh_paper",
                "gkx.dwd_policy_base",
                "gkx.dwd_scholar",
            ],
            "snapshots": [
                "code/_snapshots21/org_family_panel_20261021.json",
                "code/_probe_blocked_f2_20261023.json",
            ],
            "demo_used": False,
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "机构级快照口径（2026-10-21 面板），无年度基期；论文年列受 §3.74 采集批次峰影响，本件只作存量总量，不画年度趋势。",
        "population": {
            "institutes_all": len(inst),
            "names_all": d["coverage"]["names"],
            "shenzhen": len(sz),
            "shenzhen_identified": len(ident),
            "shenzhen_unidentified": len(sz) - len(ident),
            "org_type_shenzhen": dict(Counter(i["org_type"] or "（空）" for i in sz)),
            "area_top": Counter(i["area"] or "（空）" for i in sz).most_common(10),
        },
        "dimensions": dims,
        "city_baseline": city_base,
        "city_pain_scores": subs,
        "shenzhen_composite_pain": {
            "weights_are_authored": True,
            "main_is_official": False,
            "weights": {"project_per_100": 0.30, "transfer_per_100": 0.25,
                        "paper_per_100": 0.20, "patent_per_100": 0.15, "policy_per_100": 0.10},
            "score": round(sum(
                {"project_per_100": 0.30, "transfer_per_100": 0.25, "paper_per_100": 0.20,
                 "patent_per_100": 0.15, "policy_per_100": 0.10}[k] * subs[k]["深圳市"]
                for k in subs), 2),
            "note": "权重为本工程自拟（按维度可算性分配），非官方权重表；四市 min-max 归一后加权，只在四市间可比。",
        },
        "weak_profile": {
            "quartile_thresholds": {k: round(v, 4) for k, v in q.items()},
            "identified_n": len(ident),
            "weak_dim_count_dist": {str(k): v for k, v in sorted(weak_dist.items())},
            "multi_weak_orgs": weak_rows[:20],
            "multi_weak_n": len(weak_rows),
        },
        "head_concentration": {
            "top5_projects": [{"name": i["name"], "value": i["projects"]} for i in top_proj],
            "top5_papers": [{"name": i["name"], "value": i["papers"]} for i in top_paper],
            "top5_patents": [{"name": i["name"], "value": i["patents"]} for i in top_patent],
        },
        "derived": {
            "sz_share_of_institutes_pct": {
                "value": round(len(sz) / len(inst) * 100, 4),
                "numerator": len(sz),
                "denominator": len(inst),
                "denominator_note": "分子=深圳科研机构数 population.shenzhen，分母=四市科研机构底册数 population.institutes_all（2,074）",
            },
            "sz_identified_share_pct": {
                "value": round(len(ident) / len(sz) * 100, 4),
                "numerator": len(ident),
                "denominator": len(sz),
                "denominator_note": "分子=深圳有任一分维非零的机构数 population.shenzhen_identified，分母=深圳机构数 population.shenzhen",
            },
            "sz_unidentified_share_pct": {
                "value": round(pop_block.get("shenzhen_unidentified", 0) / pop_block["shenzhen"] * 100, 4) if "shenzhen_unidentified" in pop_block else round((pop_block["shenzhen"] - len(set(i["org_id"] for i in sz if (i["projects"] + i["transfer_in"] + i["transfer_out"] + i["papers"] + i["patents"] + i["policy_mentions"] + i["scholars"] + i["people"]) > 0))) / pop_block["shenzhen"] * 100, 4),
                "numerator": pop_block["shenzhen"] - len(set(i["org_id"] for i in sz if (i["projects"] + i["transfer_in"] + i["transfer_out"] + i["papers"] + i["patents"] + i["policy_mentions"] + i["scholars"] + i["people"]) > 0)),
                "denominator": pop_block["shenzhen"],
                "denominator_note": "分子=深圳五路（含人才两路）全零机构数 population.shenzhen_unidentified，分母=深圳机构数 population.shenzhen",
            },
            "sz_project_with_value_pct": {
                "value": round(dims["project"]["with_value"] / len(sz) * 100, 4),
                "numerator": dims["project"]["with_value"],
                "denominator": len(sz),
                "denominator_note": "分子=深圳有纵向项目记录的机构数 dimensions.project.with_value，分母=深圳机构数 population.shenzhen",
            },
            "sz_transfer_with_value_pct": {
                "value": round(dims["transfer"]["with_value"] / len(sz) * 100, 4),
                "numerator": dims["transfer"]["with_value"],
                "denominator": len(sz),
                "denominator_note": "分子=深圳有专利转让记录（转入+转出）的机构数 dimensions.transfer.with_value，分母=深圳机构数 population.shenzhen",
            },
            "sz_paper_with_value_pct": {
                "value": round(dims["paper"]["with_value"] / len(sz) * 100, 4),
                "numerator": dims["paper"]["with_value"],
                "denominator": len(sz),
                "denominator_note": "分子=深圳有中文论文的机构数 dimensions.paper.with_value，分母=深圳机构数 population.shenzhen",
            },
            "sz_policy_with_value_pct": {
                "value": round(dims["policy"]["with_value"] / len(sz) * 100, 4),
                "numerator": dims["policy"]["with_value"],
                "denominator": len(sz),
                "denominator_note": "分子=深圳被政策文本提及的机构数 dimensions.policy.with_value，分母=深圳机构数 population.shenzhen",
            },
            "sz_paper_per_100_vs_gz_x": {
                "value": round(city_base["深圳市"]["per_100_papers"]
                               / city_base["广州市"]["per_100_papers"], 4),
                "numerator": city_base["深圳市"]["per_100_papers"],
                "denominator": city_base["广州市"]["per_100_papers"],
                "denominator_note": "分子=深圳每百家机构论文数 city_baseline.深圳市.per_100_papers，分母=广州同名指标（倍率）",
            },
            "sz_project_per_100_vs_gz_x": {
                "value": round(city_base["深圳市"]["per_100_projects"]
                               / city_base["广州市"]["per_100_projects"], 4),
                "numerator": city_base["深圳市"]["per_100_projects"],
                "denominator": city_base["广州市"]["per_100_projects"],
                "denominator_note": "分子=深圳每百家机构项目数 city_baseline.深圳市.per_100_projects，分母=广州同名指标（倍率）",
            },
            "sz_transfer_per_100_vs_gz_x": {
                "value": round(city_base["深圳市"]["per_100_transfer"]
                               / city_base["广州市"]["per_100_transfer"], 4),
                "numerator": city_base["深圳市"]["per_100_transfer"],
                "denominator": city_base["广州市"]["per_100_transfer"],
                "denominator_note": "分子=深圳每百家机构转让笔数 city_baseline.深圳市.per_100_transfer，分母=广州同名指标（倍率）",
            },
            "project_top5_share_pct": {
                "value": dims["project"]["top5_share_pct"],
                "numerator": None,
                "denominator": dims["project"]["total"],
                "denominator_note": "分子=深圳项目数前 5 家机构之和（head_concentration.top5_projects 前五项值相加），分母=深圳项目总数 dimensions.project.total",
            },
            "multi_weak_share_of_identified_pct": {
                "value": round(len(weak_rows) / len(ident) * 100, 4),
                "numerator": len(weak_rows),
                "denominator": len(ident),
                "denominator_note": "分子=在 ≥2 个分维上同时落到下四分位的机构数 weak_profile.multi_weak_n，分母=深圳有值机构数 population.shenzhen_identified",
            },
            "fund_top5_share_pct": {
                "value": dims["project"]["fund_top5_share_pct"],
                "numerator": None,
                "denominator": dims["project"]["fund_total"],
                "denominator_note": "分子=深圳项目经费前 5 家之和（project_fund 降序前五），分母=深圳项目经费总额 dimensions.project.fund_total",
            },
            "sz_shiye_share_pct": {
                "value": round(pop_block["org_type_shenzhen"].get("事业单位", 0) / pop_block["shenzhen"] * 100, 4),
                "numerator": pop_block["org_type_shenzhen"].get("事业单位", 0),
                "denominator": pop_block["shenzhen"],
                "denominator_note": "分子=深圳机构中登记类型为事业单位的家数 population.org_type_shenzhen.事业单位，分母=深圳机构数 population.shenzhen",
            },
            "sz_minban_share_pct": {
                "value": round(pop_block["org_type_shenzhen"].get("民办非企业单位", 0) / pop_block["shenzhen"] * 100, 4),
                "numerator": pop_block["org_type_shenzhen"].get("民办非企业单位", 0),
                "denominator": pop_block["shenzhen"],
                "denominator_note": "分子=深圳机构中登记类型为民办非企业单位的家数 population.org_type_shenzhen.民办非企业单位，分母=深圳机构数 population.shenzhen",
            },
            "sz_nanshan_share_pct": {
                "value": round(dict(pop_block["area_top"]).get("南山区", 0) / pop_block["shenzhen"] * 100, 4),
                "numerator": dict(pop_block["area_top"]).get("南山区", 0),
                "denominator": pop_block["shenzhen"],
                "denominator_note": "分子=深圳南山区机构数 population.area_top 中南山区一项，分母=深圳机构数 population.shenzhen",
            },
            "sz_patent_grant_share_pct": {
                "value": round(city_base["深圳市"]["patent_grants"] / city_base["深圳市"]["patents"] * 100, 4),
                "numerator": city_base["深圳市"]["patent_grants"],
                "denominator": city_base["深圳市"]["patents"],
                "denominator_note": "分子=深圳机构专利授权量 city_baseline.深圳市.patent_grants，分母=深圳机构专利总量 city_baseline.深圳市.patents",
            },
        },
        "absence_probe": {
            "file": "code/_probe_blocked_f2_20261023.json",
            "blocked": [
                {"table": r["table"],
                 "gkx_exists": r["gkx_information_schema"]["exists"],
                 "gkx_hits": r["gkx_information_schema"]["hits"],
                 "live_demo_row_class": ("全量装载" if (r["live_where"].get("rows") or 0) >= 10000 else "样例级"),
                 "verdict": r["live_where"].get("verdict")}
                for r in load(PROBE).get("blocked", [])
                if r["table"] == "enterprise_cooperation"
            ],
        },
        "rejected_dimensions": [
            {
                "dimension": "产学研合作痛点（机构—企业合作缺口）",
                "reason": "gkx 无 enterprise_cooperation；information_schema.TABLES WHERE TABLE_SCHEMA='gkx' 命中 0 行；演示库同名表为全量装载，铁律禁引，不构成支持",
                "alternative": "专利转让 × 纵向项目 × 论文三路独立刻画（本件主口径）",
                "difference": "三路只能反映机构自身的产出与流动，不能回答「想合作但找不到企业」这类关系型痛点；合作缺口只能由企业侧间接推断",
            },
            {
                "dimension": "经费强度（项目经费/机构规模）",
                "reason": "gkx 无机构人员数（employees_number 整列为空，§3.71）；project_fund 单位未在表结构中标注",
                "alternative": "项目经费绝对额与集中度",
                "difference": "无分母，只能比总额与集中度，不能比「人均经费」或「经费强度」",
            },
            {
                "dimension": "痛点年度演化",
                "reason": "论文年列受 §3.74 采集批次峰（2024 占 32.09%）污染；项目年列只有起始年、无结题年",
                "alternative": "快照截面",
                "difference": "不能画趋势，也不能判断痛点在改善还是恶化",
            },
        ],
        "gaps": [
            "1,014 家深圳机构中 886 家（87.38%）在项目/转让/论文/专利/人才/政策六路上全部为 0，无法识别其痛点（数据缺口，不是「无痛点」）",
            "合作/服务关系维整块缺失，产学研协同只能由转让与合著间接代理",
            "项目经费单位未标注，跨机构相加存在量纲风险，本件只用相对份额",
            "专利按申请人名称桥接，机构更名会导致漏计（面板 patent_matched_orgs 仅 219/2,074）",
        ],
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"sz={len(sz)} ident={len(ident)} proj={dims['project']['total']} "
          f"papers={dims['paper']['total']} patents={dims['patent']['total']} "
          f"multi_weak={len(weak_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


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
    out_json = here / "M_ORG_SZ_PAINPOINT_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ORG_SZ_PAINPOINT.py 等价）
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
        "metric_id": "M_ORG_SZ_PAINPOINT",
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

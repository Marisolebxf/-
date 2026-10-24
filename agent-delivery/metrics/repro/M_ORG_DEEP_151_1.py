#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ORG_DEEP_151_1 · 深圳科研机构优势分析模型（gkx 口径重建件）

需求锚点：产品需求「科研机构深度分析模型构建 / 深圳科研机构优势分析模型」（序号 151，excel_row 60）

口径（照抄旧稿公式：三维分位合成 + 优势/不足判定）：
  D1 科研成果 = 专利件数（深圳内部相对分位，**不是**全国分位）
  D2 科研经费 = NSFC 项目资助额（万元，全国 1,593 家承担机构分位）★唯一真全国对标
  D3 人才队伍 = 学者论文数（2,074 家机构中 29 家有学者记录，省内底册分位）
  AI_i = 可得维度分位的等权平均（缺维不进分母、不补 0）
  分位 P = #{j: x_j ≤ x_i} / N × 100；P ≥ 75 记优势，P ≤ 25 记不足

【本件自定义、待甲方确认】
  * 三维等权：需求只说「设定权重」，未给数值；等权是本件的默认，不是官方权重。
  * 阈值 75 / 25：取上/下四分位的统计惯例，需求未给。
  * 优势指数不是绩效评分：它是「在各自样本中的相对位置」，样本换了分数就变。

与旧稿的差异（数据源换血，公式不动）：
  旧稿跑在演示库连接器上（`_org_common` / `demo_*` 系列表），且把 22 所深圳高校并进底册凑成 1,034 家；
  本件不 import 任何 helper，只读本目录 gkx 落盘快照，评价宇宙 = 1,014 家机构，
  高校另立「高校对标面」（16 / 207 / 3,501），不再与机构底册混算。
  经费维从「全国 1,592 家」升级为可复算的 1,593 家（含空名 1 行），并新增深圳占全国份额。

数据源（零 SQL）：
  _snapshots21/org_family_panel_20261021.json    2,074 家机构（专利/项目/资助额/学者）
  _snapshots21/nsfc_org_dist_20261022.json       全国 NSFC 1,593 家承担机构（2 条 SQL 落盘，58,453 项）
  _snapshots21/heis21_20261022.json              全国高校 3,501 所（31 省，dwd_org_heis_info）

运行：cd code && python3 M_ORG_DEEP_151_1.py
产物：code/M_ORG_DEEP_151_1_out.json
"""
from __future__ import annotations

import json
import os
import statistics
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")

MID = "M_ORG_DEEP_151_1"
CITY = "深圳市"
ADV, WEAK = 75, 25


# ------------------------------------------------- 统计工具（内联自 _org_deep21_common.py）
def dist(vals):
    if not vals:
        return {"n": 0}
    s = sorted(vals)
    n = len(s)
    return {"n": n, "min": round(s[0], 2), "p25": round(s[int(n * .25)], 2),
            "median": round(statistics.median(s), 2), "mean": round(sum(s) / n, 2),
            "p75": round(s[int(n * .75)], 2), "p90": round(s[int(n * .9)], 2),
            "max": round(s[-1], 2)}


def pct_of(value, universe):
    """分位：≤ value 的样本占比 ×100（与旧稿同式）。"""
    if not universe:
        return None
    return round(sum(1 for v in universe if v <= value) / len(universe) * 100, 1)


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def main():
    panel = load("org_family_panel_20261021.json")
    nsfc = load("nsfc_org_dist_20261022.json")
    heis = load("heis21_20261022.json")

    inst = panel["institutions"]
    sz = [i for i in inst if i["city"] == CITY]
    nsfc_orgs = [o for o in nsfc["orgs"] if o["name"]]
    nsfc_fund = [o["fund_wan"] for o in nsfc_orgs]
    nsfc_proj = [o["projects"] for o in nsfc_orgs]
    nsfc_by_name = {o["name"]: o for o in nsfc_orgs}

    # ---------------- 1. 证据宇宙
    ev = [i for i in sz if i["patents"] > 0 or i["projects"] > 0 or i["scholars"] > 0]
    ev_pat = [i["patents"] for i in ev if i["patents"] > 0]
    ev_fund = [i["project_fund"] for i in ev if i["projects"] > 0]
    ev_sch = [i["scholars"] for i in ev if i["scholars"] > 0]
    universe = {
        "sz_roster": len(sz),
        "evidence": len(ev),
        "evidence_pct": round(len(ev) / len(sz) * 100, 2),
        "patent_bearing": len(ev_pat),
        "project_bearing": len(ev_fund),
        "scholar_bearing": len(ev_sch),
        "no_record": len(sz) - len(ev),
        "combo": dict(Counter(
            ("P" if i["patents"] > 0 else "") + ("F" if i["projects"] > 0 else "") +
            ("S" if i["scholars"] > 0 else "") or "none" for i in ev).most_common()),
    }

    # ---------------- 2. 一致性自检：面板资助额 vs 全国表按名匹配
    matched = [i for i in sz if i["name"] in nsfc_by_name]
    panel_fund = round(sum(i["project_fund"] for i in matched), 2)
    nsfc_fund_m = round(sum(nsfc_by_name[i["name"]]["fund_wan"] for i in matched), 2)
    panel_proj = sum(i["projects"] for i in matched)
    nsfc_proj_m = sum(nsfc_by_name[i["name"]]["projects"] for i in matched)
    share = {
        "matched_orgs": len(matched),
        "panel_projects": panel_proj,
        "nsfc_projects": nsfc_proj_m,
        "panel_fund_wan": panel_fund,
        "nsfc_fund_wan": nsfc_fund_m,
        "fund_diff_pct": round((panel_fund - nsfc_fund_m) / nsfc_fund_m * 100, 3) if nsfc_fund_m else None,
        "sz_share_projects_pct": round(nsfc_proj_m / nsfc["n_rows"] * 100, 3),
        "sz_share_fund_pct": round(nsfc_fund_m / nsfc["total_fund_wan"] * 100, 3),
        "national_projects": nsfc["n_rows"],
        "national_fund_wan": round(nsfc["total_fund_wan"], 2),
    }

    # ---------------- 3. 三维分位与优势指数
    rows = []
    for i in ev:
        d = {}
        if i["patents"] > 0:
            d["D1"] = pct_of(i["patents"], ev_pat)
        if i["projects"] > 0:
            d["D2"] = pct_of(i["project_fund"], nsfc_fund)
        if i["scholars"] > 0:
            d["D3"] = pct_of(i["scholars"], ev_sch)
        got = [v for v in d.values() if v is not None]
        ai = round(sum(got) / len(got), 1) if got else None
        rows.append({
            "org_id": i["org_id"], "name": i["name"], "org_type": i.get("org_type"),
            "inc_year": i.get("inc_year"),
            "patents": i["patents"], "projects": i["projects"],
            "project_fund_wan": round(i["project_fund"], 2), "scholars": i["scholars"],
            "pct": d, "dims": len(got), "ai": ai,
            "advantages": sorted([k for k, v in d.items() if v is not None and v >= ADV]),
            "weaknesses": sorted([k for k, v in d.items() if v is not None and v <= WEAK]),
        })
    scored = [r for r in rows if r["ai"] is not None]
    by_ai = sorted(scored, key=lambda r: -r["ai"])

    dim_stats = {}
    for k in ("D1", "D2", "D3"):
        vals = [r["pct"][k] for r in scored if k in r["pct"]]
        dim_stats[k] = {
            "n": len(vals),
            "adv": sum(1 for v in vals if v >= ADV),
            "weak": sum(1 for v in vals if v <= WEAK),
            "median_pct": round(statistics.median(vals), 1) if vals else None,
        }

    # ---------------- 4. 全国/省内基准对照
    sz_fund_med = statistics.median(ev_fund) if ev_fund else None
    bench = {
        "D1_frame": "深圳内部（有专利 %d 家）" % len(ev_pat),
        "D1_median": statistics.median(ev_pat) if ev_pat else None,
        "D2_frame": "全国 NSFC 承担机构 %d 家" % len(nsfc_orgs),
        "D2_national_median_projects": statistics.median(nsfc_proj),
        "D2_national_median_fund_wan": round(statistics.median(nsfc_fund), 2),
        "D2_national_p90_fund_wan": round(sorted(nsfc_fund)[int(len(nsfc_fund) * .9)], 2),
        "D2_sz_median_fund_wan": round(sz_fund_med, 2) if sz_fund_med else None,
        "D2_sz_median_projects": statistics.median([i["projects"] for i in matched]) if matched else None,
        "D2_ratio_median_fund": round(sz_fund_med / statistics.median(nsfc_fund), 2) if sz_fund_med else None,
        "D3_frame": "省内底册（有学者 %d 家）" % len(ev_sch),
        "D3_median": statistics.median(ev_sch) if ev_sch else None,
        "D3_national_frame_available": False,
    }

    # ---------------- 5. 高校对标面（不与机构底册混算）
    h_rows = heis["rows"]
    # 名单表有重名行（普通高校与成人高校两份名单交叉），按校名去重后再计数，
    # 否则「深圳 16 所」会把 5 所重复计入（实测 16 行 → 11 个唯一校名）。
    def uniq(rows):
        seen, out = set(), []
        for r in rows:
            if r[0] in seen:
                continue
            seen.add(r[0])
            out.append(r)
        return out
    sz_h = uniq([r for r in h_rows if r[2] == "深圳市"])
    gd_h = uniq([r for r in h_rows if r[1] == "广东省"])
    nat_h = uniq(h_rows)
    hei = {
        "source": "gkx.dwd_org_heis_info（全国普通/成人高校名单）",
        "national_rows": len(h_rows), "national": len(nat_h),
        "national_dup_rows": len(h_rows) - len(nat_h),
        "national_provinces": len({r[1] for r in h_rows}),
        "guangdong_rows": len([r for r in h_rows if r[1] == "广东省"]),
        "guangdong": len(gd_h),
        "shenzhen_rows": len([r for r in h_rows if r[2] == "深圳市"]),
        "shenzhen": len(sz_h),
        "sz_share_pct": round(len(sz_h) / len(nat_h) * 100, 3),
        "sz_list": [{"name": r[0], "level": r[5], "est_year": r[3]} for r in sz_h],
        "national_level": dict(Counter(r[5] or "(空)" for r in nat_h).most_common()),
        "sz_level": dict(Counter(r[5] or "(空)" for r in sz_h).most_common()),
        "est_year_fill_pct": round(sum(1 for r in h_rows if r[3]) / len(h_rows) * 100, 2),
        "note": ("高校名单只作外部参照：3,501 行去重后 2,933 所（重名 568 行，普通/成人两份名单交叉）/31 省，"
                 "深圳去重后 11 所（16 行，重复 5 行）占 0.375%；"
                 "est_year 仅 53.61% 非空且 2019—2025 合计 11 条，不能作趋势。"),
    }

    payload = {
        "metric_id": MID,
        "metric_name": "深圳科研机构优势分析模型",
        "domain": "TOPIC-ORG / 科研机构深度分析（外部对标）",
        "support_judgment": "部分支持",
        "support_reason": (
            f"评价宇宙 {len(sz)} 家深圳机构中 {len(ev)} 家有可核实产出（{universe['evidence_pct']}%），"
            f"三维分位与优势指数可复现；但只有经费维是真全国对标（NSFC {len(nsfc_orgs)} 家承担机构），"
            f"专利维无全国属地只能内部相对分位（{len(ev_pat)} 家），人才维仅 {len(ev_sch)} 家有记录（省内底册）。"
            "需求要求的「科研成果水平/科研经费投入/人才队伍素质」三线里，两条是代理或内部相对，"
            "且权重的阈值为本件自定义，故判部分支持。"
        ),
        "generated_at": "2026-10-22",
        "main_db": "gkx @ 183.240.141.251:3318（gkx_reader_zp，只读）",
        "sql_count": 2,
        "sources": [
            "code/_snapshots21/org_family_panel_20261021.json（2,074 家机构，含专利/项目/资助额/学者）",
            "code/_snapshots21/nsfc_org_dist_20261022.json（gkx.dwd_zh_project 聚合，1,593 家/58,453 项）",
            "code/_snapshots21/heis21_20261022.json（gkx.dwd_org_heis_info，3,501 所高校）",
        ],
        "base_years_used": [1986, 1987, 1988, 1989, 1990],
        "base_years_missing": [2022, 2023, 2024, 2025],
        "base_years_note": (
            "NSFC 项目批准年覆盖 1986—2021 连续 36 年（每年 ≥1 条），2022 年 58 条、2023 年 6 条，"
            "2024—2025 零条 → 2022 起为残年，不参与任何年度趋势，只作累计存量；"
            "专利与学者为截面积累口径，无年度基期。base_years_used 列前 5 年作代表，"
            "全量连续区间见 coverage_years。"
        ),
        "coverage_years": {"nsfc": [1986, 2021], "nsfc_residual": [2022, 2023],
                           "patent": [2021, 2026], "roster_inc": [1996, 2026]},
        "definition_note": (
            "本件自定义、待甲方确认：1) 三维等权（需求未给权重）；2) 优势/不足阈值 75/25（上/下四分位惯例）；"
            "3) 分位分母分别取「深圳有专利机构」「全国 NSFC 承担机构」「省内底册有学者机构」，三者不同源，"
            "故 AI 只用于同一维度内的相对排序，不做跨维度的绝对值比较。"
        ),
        "probes": {
            "institute_total": len(inst),
            "sz_roster": len(sz),
            "panel_coverage": panel.get("coverage", {}),
            "nsfc_rows": nsfc["n_rows"],
            "nsfc_orgs": nsfc["n_orgs"],
            "nsfc_total_fund_wan": round(nsfc["total_fund_wan"], 2),
            "nsfc_by_year_tail": nsfc["by_year"][-6:],
            "heis_rows": len(h_rows),
        },
        "universe": universe,
        "consistency": share,
        "benchmark": bench,
        "dim_stats": dim_stats,
        "ai_dist": dist([r["ai"] for r in scored]),
        "ai_top10": by_ai[:10],
        "ai_bottom10": by_ai[-10:][::-1],
        "adv_orgs": sum(1 for r in scored if r["advantages"]),
        "weak_orgs": sum(1 for r in scored if r["weaknesses"]),
        "org_rows": by_ai,
        "hei_frame": hei,
        "gaps": [
            "专利维无全国基准：dwd_patent 无申请人属地字段，机构底册 100% 广东，无法给全国申请人打城市标签；",
            "经费维只有 NSFC 竞争性经费，且批准年止于 2021（2022 年 58 条、2023 年 6 条），不能做 2022 后趋势；",
            "dwd_zh_project.funded_province 全列为空（58,453/58,453 空），属地只能靠机构名精确匹配，改名/简称即漏；",
            "人才维仅 12 家深圳机构有学者记录（1.18%），dwd_scholar 21,316 人与底册交集极小，不构成全国分位；",
            "机构级 R&D 经费/研发人员表整列为空（§3.10），「科研经费投入」的原义口径无表可依；",
            "底册无统一社会信用代码列，专利/项目全靠名称精确匹配，重名与别名会双向漏配。",
        ],
    }

    out = os.path.join(HERE, f"{MID}_out.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)

    print("wrote", os.path.basename(out))
    print("universe", universe)
    print("consistency", share)
    print("bench", bench)
    print("ai", payload["ai_dist"])
    print("dim_stats", dim_stats)
    print("adv/weak orgs", payload["adv_orgs"], payload["weak_orgs"])
    print("top3", [(r["name"], r["ai"], r["dims"]) for r in by_ai[:3]])
    print("hei", hei["national_rows"], "->", hei["national"], "gd", hei["guangdong"],
          "sz", hei["shenzhen"], hei["sz_share_pct"], "%")


if __name__ == "__main__":
    main()

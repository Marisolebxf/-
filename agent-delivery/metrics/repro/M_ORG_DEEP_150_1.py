#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ORG_DEEP_150_1 · 科研机构发展历程模型（ORG 域）

需求锚点：bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/科研机构/深度分析.md 序号 150
  「基于科研机构的基础指标和资讯指标，系统识别其发展过程中的重大事件，并构建重大事件时间线，
    分析机构的历史演变和关键发展阶段。定义重大事件指标 + 阈值，超过阈值即认定为重大事件，
    按时间顺序输出时间线。」输出：重大事件列表 / 时间线 / 发展历程可视化 / 趋势分析报告。

本件口径（零 SQL，只读面板）：
  事件源 = 6 类可观测信号，每条事件都带「年份 + 类型 + 强度 + 来源字段」：
    E1 成立          incorporation_date（底册，1,996 家有值）
    E2 首个项目立项   dwd_zh_project.approval_year（面板 projects_year，53 家）
    E3 项目密集年     projects_year[y] ≥ 3（阈值取 3，等于该分布的 P90 附近）
    E4 首篇论文       dwd_zh_paper.cover_year_start（面板 papers_year，236 家）
    E5 论文密集年     papers_year[y] ≥ max(5, 3×该机构非零年均值)
    E6 首次政策提及   dwd_policy_base 全文匹配（面板 policy_year，72 家）
    E7 政策密集年     policy_year[y] ≥ 2
    E8 首次专利受让   dwd_patent_transfer.transfer_after 命中（面板 transfer_in_year，10 家）
    E9 人才流入峰值   dwd_scholar_work_experience.start_time（面板 flow_year，15 家）

阈值全部是确定性规则，可逐条复核；不做「模型训练」（本库无事件标签，训练是伪监督）。

硬约束（必须披露）：
  - 变更记录表 3,245,250 行，与机构底册 org_id / external_id 零交集（工商库只覆盖企业），
    因此「注册资本变更 / 名称变更 / 法定代表人变更」这类最典型的发展事件一条都拿不到。
  - 新闻表 1,668,414 行，按名称精确匹配只命中 6 条 / 5 家，不能构成资讯时间线。
  - 专利只有存量合计（star agg），没有「申请人 × 申请年」表，专利里程碑只能用 2024 单年快照。
  - 学术会议无对应表。
"""
from __future__ import annotations

import os
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _org_deep21_common as OC  # noqa: E402

MID = "M_ORG_DEEP_150_1"
TYPES = ["成立", "首个项目立项", "项目密集年", "首篇论文", "论文密集年",
         "首次政策提及", "政策密集年", "首次专利受让", "人才流入峰值"]


def years_of(d):
    return sorted(int(y) for y in (d or {}) if str(y).isdigit())


def build_events(x):
    ev = []
    if x.get("inc_year") and str(x["inc_year"]).isdigit():
        ev.append({"year": int(x["inc_year"]), "type": "成立", "strength": 1,
                   "src": "incorporation_date"})
    py = {int(y): int(v) for y, v in (x.get("projects_year") or {}).items() if str(y).isdigit()}
    if py:
        y0 = min(py)
        ev.append({"year": y0, "type": "首个项目立项", "strength": py[y0],
                   "src": "dwd_zh_project.approval_year"})
        for y, v in py.items():
            if v >= 3 and y != y0:
                ev.append({"year": y, "type": "项目密集年", "strength": v,
                           "src": "dwd_zh_project.approval_year"})
    wy = {int(y): int(v) for y, v in (x.get("papers_year") or {}).items() if str(y).isdigit()}
    if wy:
        y0 = min(wy)
        ev.append({"year": y0, "type": "首篇论文", "strength": wy[y0],
                   "src": "dwd_zh_paper.cover_year_start"})
        nz = [v for v in wy.values() if v > 0]
        if nz:
            thr = max(5, 3 * (sum(nz) / len(nz)))
            for y, v in wy.items():
                if v >= thr and y != y0:
                    ev.append({"year": y, "type": "论文密集年", "strength": v,
                               "src": "dwd_zh_paper.cover_year_start"})
    oy = {int(y): int(v) for y, v in (x.get("policy_year") or {}).items() if str(y).isdigit()}
    if oy:
        y0 = min(oy)
        ev.append({"year": y0, "type": "首次政策提及", "strength": oy[y0],
                   "src": "dwd_policy_base(title+content)"})
        for y, v in oy.items():
            if v >= 2 and y != y0:
                ev.append({"year": y, "type": "政策密集年", "strength": v,
                           "src": "dwd_policy_base(title+content)"})
    ty = years_of(x.get("transfer_in_year"))
    if ty:
        s = (x.get("transfer_in_year") or {}).get(str(ty[0]))
        ev.append({"year": ty[0], "type": "首次专利受让", "strength": int(s or 1),
                   "src": "dwd_patent_transfer.transfer_after"})
    fy = {int(y): int(v) for y, v in (x.get("flow_year") or {}).items() if str(y).isdigit()}
    if fy:
        y, v = max(fy.items(), key=lambda t: t[1])
        ev.append({"year": y, "type": "人才流入峰值", "strength": v,
                   "src": "dwd_scholar_work_experience.start_time"})
    return sorted(ev, key=lambda e: (e["year"], e["type"]))


def main() -> None:
    panel = OC.load_panel()
    inst = panel["institutions"]
    probe = OC.load_probe()

    # 按行（org_id）存储，避免 4 组重名机构被 dict 折叠（2,074 行 / 2,070 个不同名）
    type_org, type_n, year_type = Counter(), Counter(), defaultdict(Counter)
    rows_ev = []
    for x in inst:
        ev = build_events(x)
        rows_ev.append((x, ev))
        for e in ev:
            type_n[e["type"]] += 1
            year_type[e["year"]][e["type"]] += 1
        for t in {e["type"] for e in ev}:
            type_org[t] += 1

    ev_dist = Counter(len(ev) for _, ev in rows_ev)
    yr_dist = Counter(len({e["year"] for e in ev}) for _, ev in rows_ev)

    # 只靠成立年、没有任何后续事件的机构
    only_founding = sum(1 for _, ev in rows_ev
                        if ev and all(e["type"] == "成立" for e in ev))
    no_event = sum(1 for _, ev in rows_ev if not ev)
    rich = sorted(((len(ev), len({e["year"] for e in ev}), x) for x, ev in rows_ev),
                  key=lambda t: (t[0], t[1], t[2]["name"]), reverse=True)

    # 近五年事件密度（2021—2025，2026 残年不计）
    recent = Counter()
    recent_orgs = defaultdict(set)
    for x, ev in rows_ev:
        for e in ev:
            if 2021 <= e["year"] <= 2025:
                recent[e["type"]] += 1
                recent_orgs[e["type"]].add(x["org_id"])

    # 登记日期与产出年的逻辑冲突：首个项目/论文/政策年早于「成立年」的机构
    contradict = []
    for x in inst:
        inc_y = x.get("inc_year")
        if not inc_y or not str(inc_y).isdigit():
            continue
        cand = []
        for f in ("projects_year", "papers_year", "policy_year"):
            ys = years_of(x.get(f))
            if ys:
                cand.append(min(ys))
        if cand and min(cand) < int(inc_y):
            contradict.append({"name": x["name"], "inc_year": int(inc_y),
                               "first_output_year": min(cand),
                               "gap_years": int(inc_y) - min(cand)})

    # 成立年分布（底册）
    inc = Counter(x["inc_year"] for x in inst if x.get("inc_year"))
    inc_dist = {y: inc[y] for y in sorted(inc)}

    # 论文年度的采集口径异常（2024 尖峰）——只用于披露，不参与事件阈值解释
    paper_year = Counter()
    for x in inst:
        for y, v in (x.get("papers_year") or {}).items():
            if str(y).isdigit():
                paper_year[int(y)] += int(v)
    py_recent = {y: paper_year.get(y, 0) for y in range(2018, 2027)}

    def card(x):
        ev = dict((id(y), e) for y, e in rows_ev)[id(x)]
        return {"name": x["name"], "city": x["city"], "org_type": x["org_type"],
                "events": len(ev), "years": len({e["year"] for e in ev}),
                "timeline": ev,
                "patents": x["patents"], "papers": x["papers"],
                "projects": x["projects"], "scholars": x["scholars"],
                "policy_mentions": x["policy_mentions"]}

    out = {
        "metric_id": MID,
        "metric_name": "科研机构发展历程模型",
        "domain": "ORG / 科研机构深度分析（序号 150）",
        "formula_owner": "AI-20261022（推测定义，wanghui=false）",
        "support_judgment": "部分支持",
        **OC.base_years(
            [2021, 2022, 2023, 2024, 2025], [2017, 2018, 2019, 2020],
            "近五年事件密度窗口取 2021—2025；专利侧库内 2017—2020 零行，窗口不向前延伸、"
            "缺失年不按 0 摊入；2026 为残年（采集至 2026-10）不计入。成立年事件不受窗口限制。"),
        "inputs": {
            "org_roster": "gkx.dwd_research_institute_base_info 2,074 家",
            "events": "org_family_panel_20261021.json 的 papers_year / projects_year / "
                      "policy_year / transfer_in_year / flow_year / news_year",
            "change_records": "gkx.dwd_org_changerecord_info 3,245,250 行（与底册零交集，见 limits）",
        },
        "coverage": {
            "institutes": len(inst),
            "with_founding_year": sum(1 for x in inst if x.get("inc_year")),
            "with_any_event": sum(1 for _, ev in rows_ev if ev),
            "with_two_plus_years": sum(1 for _, ev in rows_ev
                                       if len({e["year"] for e in ev}) >= 2),
            "with_three_plus_events": sum(1 for _, ev in rows_ev if len(ev) >= 3),
            "only_founding": only_founding,
            "with_nonfounding": sum(1 for _, ev in rows_ev
                                    if any(e["type"] != "成立" for e in ev)),
            "single_point_or_less": only_founding + no_event,
            "no_event": no_event,
            "event_count_dist": {str(k): v for k, v in sorted(ev_dist.items())},
            "year_count_dist": {str(k): v for k, v in sorted(yr_dist.items())},
        },
        "event_types": {
            "types": TYPES,
            "event_total": sum(type_n.values()),
            "orgs_by_type": {t: type_org.get(t, 0) for t in TYPES},
            "events_by_type": {t: type_n.get(t, 0) for t in TYPES},
            "inc_semantics": "「成立」事件取自 incorporation_date；对老机构该字段多为登记/换证日期，"
                             "与真实创院年不一致（见 incorporation_check）。",
            "thresholds": {
                "项目密集年": "同一年立项数 ≥ 3",
                "论文密集年": "同一年论文数 ≥ max(5, 3×该机构非零年度均值)",
                "政策密集年": "同一年政策提及 ≥ 2 次",
                "人才流入峰值": "该机构工作经历起始年计数最大的一年",
            },
        },
        "recent_5y": {
            "window": [2021, 2025],
            "total": sum(recent.values()),
            "events_by_type": {t: recent.get(t, 0) for t in TYPES},
            "orgs_by_type": {t: len(recent_orgs.get(t, ())) for t in TYPES},
        },
        "founding_year_dist": inc_dist,
        "incorporation_check": {
            "contradictions": len(contradict),
            "rule": "首个项目/论文/政策年份早于 incorporation_date 的年份，说明该字段记的是登记日期而非创院年。",
            "top_examples": sorted(contradict, key=lambda r: -r["gap_years"])[:15],
            "spike_years": {y: inc_dist.get(y) for y in ("2016", "2021")},
            "note": "2016 年 326 家、2021 年 266 家集中登记，是换证/补录批次，"
                    "不能读成「2016 与 2021 年是科研机构成立高峰」。",
        },
        "paper_year_recent": py_recent,
        "paper_year_note": "2024 年论文 32,379 篇、2023 年 6,651 篇、2025 年 6,548 篇——"
                           "2024 是期刊覆盖口径造成的尖峰，不能解释为「2024 年成果爆发」；"
                           "本件论文密集年阈值仍按机构自身均值算，不按全库年度比较。",
        "timeline_top": [card(n) for _, _, n in rich[:20]],
        "timeline_samples": [card(n) for _, _, n in rich[20:26]],
        "limits": [
            "变更记录 3,245,250 行与底册 2,074 家 org_id / external_id 零交集；"
            "strengthen/名称/法人/注册资本变更这类核心发展事件为 0 条。",
            "新闻表 1,668,414 行按名称精确匹配只命中 6 条 / 5 家，不能构成资讯时间线。",
            "专利只有存量合计，无「申请人 × 申请年」交叉表；专利里程碑只剩 2024 单年快照。",
            "项目批准年集中在 1986—2021（2022 年 58 项、2023 年 6 项），近三年项目事件近乎断流。",
            "无学术会议表，需求列的「学术会议记录」输入缺失。",
            "1,793 家（86.45%）除「成立」外七类信号全为 0：1,726 家只有成立年一条事件、"
            "67 家连成立年都没有（底册 78 家无成立日，其中 11 家有其他事件），无法生成多节点时间线。",
            "成立年字段 1,996/2,074 有值，但其中 118 家首个产出年早于该年（最大差 30 年），"
            "说明它记的是登记/换证日期；「成立高峰在 2016 与 2021」是登记批次的假象。",
        ],
        "probes": {k: probe.get(k) for k in ("chg_head", "chg_type", "chg_year", "inst_fill")},
    }
    path = OC.write_out(out, MID)
    print("wrote", path)
    print("any_event", out["coverage"]["with_any_event"], "2+ years", out["coverage"]["with_two_plus_years"])
    print("type orgs", out["event_types"]["orgs_by_type"])
    print("events", out["event_types"]["events_by_type"])
    print("recent", out["recent_5y"])
    print("top", [(c["name"], c["events"], c["years"]) for c in out["timeline_top"][:8]])


if __name__ == "__main__":
    main()

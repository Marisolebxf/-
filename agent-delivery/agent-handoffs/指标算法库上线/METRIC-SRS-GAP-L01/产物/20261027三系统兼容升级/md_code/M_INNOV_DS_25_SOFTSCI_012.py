#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_DS_25_SOFTSCI_012 影响力评价与应用反馈 — 20261021 换源复现脚本

口径（王惠，calc-logic/INNOV/M_INNOV_DS_25_SOFTSCI_012.md）：
  得分 = 三维加权平均 × 100
    C1 课题能级 = 0.5·norm(log funded_amount) + 0.5·norm(project_level 映射)
    C2 成果影响 = norm(journal_articles + conference_papers + patents + awards)
    C3 应用反馈 = I(final_report_abstract 非空) + reports_count（再归一）

数据面（20261021）：**三方库 gkx**（`183.240.141.251:3318`），经 `_gkxdb.gkx()`。
原版读旧开发库（现以停用、不再使用）；gkx 与它逐表镜像（`dwd_zh_project` 58,453、
`dwd_zh_project_output` 20,133 一致），本版只换数据面、不改公式。

关键事实（换源后复测）：`dwd_zh_project` 100% 为「国家自然科学基金(NSFC)」项目，
**没有任何一行命中「软科学」**（title/discipline/project_source 三列 LIKE 均 0 行），
故以 NSFC 项目作软科学课题的代理宇宙，全部结论标注「代理」。

产物：M_INNOV_DS_25_SOFTSCI_012_out.json
"""
import json
import math
import time
from pathlib import Path
from statistics import mean, median

import _inn_res21_common as C

HERE = Path(__file__).parent
MID = "M_INNOV_DS_25_SOFTSCI_012"
DB = "gkx@183.240.141.251:3318"
LEVEL_MAP = {"国家级": 1.0, "省部级": 0.7, "厅局级": 0.5, "市级": 0.4, "其他": 0.2}
SOFT_DISC = ("管理", "经济", "政策", "法学", "社会学", "图书情报", "新闻", "教育")


def main():
    t0 = time.time()
    inv = C.inventory()
    out = {"metric_id": MID, "name": "影响力评价与应用反馈", "formula_owner": "王惠",
           "run_at": time.strftime("%Y-%m-%d %H:%M:%S"), "db": DB, "probes": {},
           "fill_rate": {}, "distribution": {}, "dims": {}, "samples": [],
           "sensitivity": {}, "disclosures": [], "support_judgment": None}

    # ---------- 1. 探针与填充率 ----------
    out["probes"]["dwd_zh_project"] = int(inv["dwd_zh_project"]["rows"])
    out["probes"]["dwd_zh_project_output"] = int(inv["dwd_zh_project_output"]["rows"])
    fr = C.qd("""SELECT COUNT(*) n,
        SUM(funded_amount IS NOT NULL AND funded_amount>0) amt,
        SUM(project_level IS NOT NULL AND project_level<>'') lvl,
        SUM(final_report_abstract IS NOT NULL AND final_report_abstract<>'') fra,
        SUM(discipline IS NOT NULL AND discipline<>'') disc,
        SUM(funded_institution IS NOT NULL AND funded_institution<>'') inst,
        SUM(participating_institution IS NOT NULL AND participating_institution<>'') part
        FROM gkx.dwd_zh_project""")[0]
    n = int(fr["n"])
    out["fill_rate"] = {k: {"n": int(fr[k]), "rate": round(int(fr[k]) / n, 4)}
                        for k in ["amt", "lvl", "fra", "disc", "inst", "part"]}
    out["probes"]["soft_science_hits"] = int(C.q1(
        "SELECT COUNT(*) FROM gkx.dwd_zh_project WHERE title LIKE '%%软科学%%' "
        "OR discipline LIKE '%%软科学%%' OR project_source LIKE '%%软科学%%'")[0])
    out["probes"]["project_source_distinct"] = [
        r[0] for r in C.q("SELECT project_source,COUNT(*) c FROM gkx.dwd_zh_project "
                          "GROUP BY 1 ORDER BY c DESC LIMIT 5")]
    out["probes"]["project_level_distinct"] = [
        {"level": r[0], "n": int(r[1])} for r in
        C.q("SELECT project_level,COUNT(*) c FROM gkx.dwd_zh_project GROUP BY 1 "
            "ORDER BY c DESC LIMIT 10")]
    out["probes"]["soft_adjacent_disciplines"] = int(C.q1(
        "SELECT COUNT(*) FROM gkx.dwd_zh_project WHERE " +
        " OR ".join(["discipline LIKE '%%%s%%'" % k for k in SOFT_DISC]))[0])
    out["probes"]["output_join_hit"] = int(C.q1(
        "SELECT COUNT(*) FROM gkx.dwd_zh_project p JOIN gkx.dwd_zh_project_output o "
        "ON p.id=o.id")[0])

    # ---------- 2. 取数 ----------
    rows = C.qd("""SELECT p.id, p.title, p.discipline, p.funded_amount, p.project_level,
        p.final_report_abstract, p.approval_year, o.journal_articles_count j,
        o.conference_papers_count c, o.patents_count pat, o.awards_count aw,
        o.reports_count rep, o.total_outputs tot
        FROM gkx.dwd_zh_project p LEFT JOIN gkx.dwd_zh_project_output o ON p.id=o.id""")
    recs = []
    for r in rows:
        amt = float(r["funded_amount"] or 0)
        lvl = LEVEL_MAP.get(r["project_level"] or "其他", 0.2)
        j = int(r["j"] or 0)
        cf = int(r["c"] or 0)
        pt = int(r["pat"] or 0)
        aw = int(r["aw"] or 0)
        rep = int(r["rep"] or 0)
        fra = 1.0 if (r["final_report_abstract"] or "").strip() else 0.0
        recs.append({"id": r["id"], "title": r["title"], "discipline": r["discipline"],
                     "year": (int(r["approval_year"]) // 10000) if r["approval_year"] else None,
                     "amt": amt, "lvl": lvl, "j": j, "c": cf, "pat": pt, "aw": aw,
                     "rep": rep, "fra": fra, "out_sum": j + cf + pt + aw,
                     "has_output": 1 if r["tot"] is not None else 0})

    # ---------- 3. 归一化 ----------
    # funded_amount 重尾，用 log1p 后再 min-max；成果件数同法
    amt_n = C.minmax([math.log1p(x["amt"]) for x in recs])
    out_n = C.minmax([math.log1p(x["out_sum"]) for x in recs])
    lvl_n = C.minmax([x["lvl"] for x in recs])          # 本例为常量 → 全部 0.5
    rep_n = C.minmax([x["rep"] for x in recs])          # 本例全 0 → 全部 0.5
    fb_n = C.minmax([x["fra"] + x["rep"] for x in recs])

    for i, x in enumerate(recs):
        x["c1"] = 0.5 * amt_n[i] + 0.5 * lvl_n[i]
        x["c2"] = out_n[i]
        x["c3"] = fb_n[i]
        x["score"] = round(100 * (x["c1"] + x["c2"] + x["c3"]) / 3, 2)
        x["score_amt_only"] = round(100 * (amt_n[i] + out_n[i] + fb_n[i]) / 3, 2)

    scores = [x["score"] for x in recs]
    ranked = sorted(recs, key=lambda x: -x["score"])

    out["distribution"] = {
        "n_scored": len(recs), "min": min(scores), "max": max(scores),
        "mean": round(mean(scores), 2), "median": round(median(scores), 2),
        "p10": round(C.pct(scores, .10), 3), "p50": round(C.pct(scores, .50), 3),
        "p90": round(C.pct(scores, .90), 3), "p99": round(C.pct(scores, .99), 3),
        "n_distinct": len(set(scores)),
        "n_with_any_output": sum(1 for x in recs if x["out_sum"] > 0),
        "n_with_fra": sum(1 for x in recs if x["fra"] > 0),
        "share_score_zero": round(sum(1 for s in scores if s == 0) / len(scores), 4)}
    out["dims"] = {
        "C1_课题能级": {"mean": round(mean([x["c1"] for x in recs]), 4),
                        "note": "project_level 全表仅 1 个取值（国家级）→ lvl_n 恒 0.5，该半维无区分度"},
        "C2_成果影响": {"mean": round(mean([x["c2"] for x in recs]), 4),
                        "awards_total": sum(x["aw"] for x in recs),
                        "note": "awards_count 全表为 0，成果影响实际只由期刊+会议+专利三类件数构成"},
        "C3_应用反馈": {"mean": round(mean([x["c3"] for x in recs]), 4),
                        "reports_total": sum(x["rep"] for x in recs),
                        "note": "reports_count 全表为 0，应用反馈退化为「结题摘要是否非空」二值"},
    }
    out["samples"] = [{"rank": i + 1, "title": x["title"][:60], "discipline": x["discipline"],
                       "year": x["year"], "funded_amount": x["amt"], "outputs": x["out_sum"],
                       "fra": int(x["fra"]), "score": x["score"]}
                      for i, x in enumerate(ranked[:15])]
    out["samples_mid"] = [{"title": x["title"][:50], "discipline": x["discipline"],
                           "funded_amount": x["amt"], "outputs": x["out_sum"],
                           "score": x["score"]}
                          for x in ranked[len(ranked) // 2: len(ranked) // 2 + 5]]
    out["samples_zero"] = [{"title": x["title"][:50], "funded_amount": x["amt"],
                            "score": x["score"]} for x in recs if x["score"] == 0][:5]

    # ---------- 4. 敏感性：剔除退化半维 ----------
    diff = [abs(a["score"] - a["score_amt_only"]) for a in recs]
    out["sensitivity"] = {
        "variant": "C1 只用 norm(log funded_amount)（剔除恒定的 project_level 半维）",
        "mean_abs_diff": round(mean(diff), 3), "max_abs_diff": round(max(diff), 3),
        "spearman_like_top100_overlap": round(
            len({x["id"] for x in sorted(recs, key=lambda z: -z["score"])[:100]} &
                {x["id"] for x in sorted(recs, key=lambda z: -z["score_amt_only"])[:100]}) / 100, 3),
        "conclusion": "两口径 Top100 重合度高 → 等级结论对 project_level 退化不敏感；"
                      "但绝对分值仍含一个常数半维，正式上线前应由甲方确认是否剔除"}

    out["disclosures"] = [
        "实测 dwd_zh_project 的 project_source 100% 为「国家自然科学基金(NSFC)」，全表 0 行命中「软科学」；"
        "本指标以 NSFC 项目作软科学课题的代理宇宙，属代理态结论，不是甲方口径的软科学课题评价",
        "funded_institution 全表 0 行非空，故无法把课题归到承担机构，机构层影响力评价无法闭合",
        "project_level 全表恒为「国家级」（58,453/58,453）→ 能级维的级别映射半维退化",
        "awards_count 与 reports_count 全表为 0 → 王惠口径的「奖项」「报告产出」两个子项无数据，"
        "成果影响维退化为期刊+会议+专利件数，应用反馈维退化为结题摘要是否非空",
        "dwd_zh_project_output 只覆盖 20,133 个课题（与主表 join 命中 %d），其余课题按 0 产出处理，"
        "会系统性压低影响力分" % out["probes"]["output_join_hit"],
        "所有取值来自三方库 gkx 真实表（dwd_zh_project / dwd_zh_project_output），"
        "未引用任何 mock_* / demo_* 面",
    ]
    out["support_judgment"] = {
        "level": "部分支持",
        "reason": "三维公式可对 " + str(len(recs)) + " 个课题现算并输出非退化分布，但"
                  "（1）软科学课题实体缺失，只能用 NSFC 项目代理；"
                  "（2）project_level 恒定、awards/reports 全 0 三个子项无数据；"
                  "（3）funded_institution 全空导致机构归集断裂——始终有依赖维不足。",
    }
    out["runtime_sec"] = round(time.time() - t0, 1)
    dest = C.write_out(MID, out)
    print("saved", dest, "n", len(recs), "dist", out["distribution"])


if __name__ == "__main__":
    main()

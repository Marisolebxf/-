#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TALENT_SZ_SUPPLY_DEMAND —— 深圳人才供需匹配（SRS 90/91）。

需求侧：`dwd_org_recruit_info` 97 分位等距抽样 82,201 条（表内 6,702,453 条），
  work_place 含「深圳」= 18,075 条；岗位标题走 JOB2D 六域规则。
供给侧给两套口径：
  A 主口径：属性宇宙里最晚履历机构判深圳的学者（123 人），研究方向全量走十域规则；
  B 稳健性：面板中 is_sz_org 且至少 1 个 20+8 集群标签的学者（59 人），集群经 CL2D 映射，
    多标签按 1/k 分摊。A 的样本更大，B 更贴 20+8 政策口径，两者都报。
匹配度：相异指数 D = 0.5 × Σ|供给份额 − 需求份额|，0=完全匹配、1=完全不匹配；
  另给「研发口径」（剔除经管/人文社科与未归类后重新归一）作稳健性。
零 SQL；产物 code/M_TALENT_SZ_SUPPLY_DEMAND_out.json。
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import _talent10_common as C  # noqa: E402

METRIC = "M_TALENT_SZ_SUPPLY_DEMAND"
RND = ("生物医药/健康", "能源/材料与化工", "AI/软件与信息", "电子/芯片与通信",
       "装备/机器人与制造", "基础科学", "农业/食品/生态", "建筑/土木/交通")


def main() -> None:
    raw = C.load("recruit161_20261022.json")
    rows = raw["rows"]
    sz = [r for r in rows if "深圳" in (r[1] or "")]
    dem = Counter(C.job_domain(r[0]) for r in sz)
    # 需求侧三域口径与供给侧十域口径对齐：把三域拆细会失真，保留六域+其他
    titles = Counter((r[0] or "").strip() for r in sz)
    comps = Counter((r[3] or "").strip() for r in sz if (r[3] or "").strip())
    years = Counter((r[2] or "")[:4] for r in sz if r[2])

    p = C.rows()
    szs = [r for r in p if C.is_sz_org(r["org"] or "") and r["cl"]]
    sup = Counter()
    for r in szs:
        for c in r["cl"]:
            sup[C.CL2D.get(c, "其他/未归类")] += 1 / len(r["cl"])

    # A 口径：属性宇宙 + 最晚履历机构
    work = C.work()
    res = C.research()
    latest = {}
    for w in work:
        if not w["org"]:
            continue
        k = (w["y1"] or w["y0"] or 0, 1 if w["cur"] else 0)
        if w["sid"] not in latest or k > latest[w["sid"]][0]:
            latest[w["sid"]] = (k, w["org"])
    sz_dir = [sid for sid, (k, o) in latest.items() if C.is_sz_org(o)]
    sup_d = Counter(C.domain_of(" ".join(res[sid])) if res.get(sid) else "其他/未归类"
                    for sid in sz_dir)
    dem_tot = sum(dem.values())
    domains = [d for d in C.DOMAINS]
    sup_tot = sum(sup.values())
    sup_share = {d: (sup.get(d, 0) / sup_tot if sup_tot else 0) for d in domains}
    supd_share = {d: (sup_d.get(d, 0) / len(sz_dir) if sz_dir else 0) for d in domains}
    dem_share = {d: (dem.get(d, 0) / dem_tot if dem_tot else 0) for d in domains}
    d_all = 0.5 * sum(abs(sup_share[d] - dem_share[d]) for d in domains)
    d_dir = 0.5 * sum(abs(supd_share[d] - dem_share[d]) for d in domains)

    def rnd_norm(x, tot):
        t = sum(x.get(d, 0) for d in RND)
        return {d: (x.get(d, 0) / t if t else 0) for d in RND}
    s_r, d_r = rnd_norm(sup, sup_tot), rnd_norm(dem, dem_tot)
    sd_r = rnd_norm(sup_d, len(sz_dir))
    d_rnd = 0.5 * sum(abs(s_r[d] - d_r[d]) for d in RND)
    d_rnd_dir = 0.5 * sum(abs(sd_r[d] - d_r[d]) for d in RND)

    gap = []
    for d in domains:
        gap.append({"domain": d, "supply_share": round(100 * supd_share[d], 2),
                    "demand_share": round(100 * dem_share[d], 2),
                    "diff_pp": round(100 * (supd_share[d] - dem_share[d]), 2),
                    "demand_n": dem.get(d, 0),
                    "supply_n": sup_d.get(d, 0)})
    gap.sort(key=lambda x: x["diff_pp"])

    payload = {
        "support_judgment": "部分支持",
        "base_years_used": [2022, 2026],
        "base_years_missing": [2019, 2020, 2021],
        "base_years_note": "招聘样本发布日 2022-01-01—2026-07-23，只有这一段；"
                           "供给侧论文/履历是累计快照，没有同年度切片，因此供需只能同年截面比，"
                           "不能做「2021 基期→2025 现期」的匹配度变化",
        "scope": {"demand_universe": "dwd_org_recruit_info 97 分位抽样 82,201 条",
                  "demand_sz": len(sz), "demand_share_of_sample": C.share(len(sz), len(rows)),
                  "supply_universe": "面板 is_sz_org 且有 20+8 集群标签",
                  "supply_sz": len(szs),
                  "unit": "岗位条数（需求）/ 学者人数（供给）",
                  "matching": "十域份额的相异指数"},
        "demand": {"rows": len(rows), "sz_rows": len(sz), "table_rows_est": raw.get("table_rows_est"),
                   "period": [min(years) if years else None, max(years) if years else None],
                   "year_series": [{"year": y, "n": n} for y, n in sorted(years.items())],
                   "domains": [{"domain": d, "n": n, "share": C.share(n, dem_tot)}
                               for d, n in dem.most_common()],
                   "top_titles": [{"title": k, "n": v} for k, v in titles.most_common(15)],
                   "top_companies": [{"company": k, "n": v} for k, v in comps.most_common(12)]},
        "supply": {"scholars_dir": len(sz_dir),
                   "domains_dir": [{"domain": d, "n": sup_d.get(d, 0),
                                    "share": round(100 * supd_share[d], 2)}
                                   for d in sorted(domains, key=lambda x: -sup_d.get(x, 0))],
                   "scholars_cluster": len(szs),
                   "domains_cluster": [{"domain": d, "n": round(sup.get(d, 0), 2),
                                        "share": round(100 * sup_share[d], 2)}
                                       for d in sorted(domains, key=lambda x: -sup.get(x, 0))],
                   "note": "A 口径一人一域；B 口径多标签按 1/k 分摊，n 可为小数"},
        "matching": {"dissimilarity_all": round(d_all, 4),
                     "dissimilarity_rnd": round(d_rnd, 4),
                     "dissimilarity_all_dir": round(d_dir, 4),
                     "dissimilarity_rnd_dir": round(d_rnd_dir, 4),
                     "rnd_domains": list(RND),
                     "interpretation": "D=0 完全匹配、D=1 完全不匹配；0.5 以上说明结构错位严重"},
        "gap": gap,
        "data_quality": {
            "sample": f"招聘表 6,702,453 条只抽了 82,201 条（1.23%），深圳 18,075 条；"
                      "比例估计的抽样误差约 ±0.4pp，但「岗位数」不是「招聘人数」（hiring_number 多空）",
            "posting_not_hire": "一条岗位可招多人、可重复发布；需求份额只能当「岗位结构」，不是「新增就业」",
            "supply_not_jobseeker": "供给侧是论文作者，不是求职者；高校教师「在职不流动」也会被算成供给",
            "mapping": "20+8 集群→十域是人工映射（CL2D），海洋/空天/深地深海落「其他」，"
                       "需求侧的 JOB2D 六域更粗；两侧粒度不一致会抬高 D",
            "title_only": "岗位域只读 job_title，没读 job_description；「工程师」类泛称会落「其他」",
            "city": "需求侧用 work_place 含「深圳」，可能含「深圳」冠名但异地的岗位；"
                    "供给侧用 is_sz_org，两侧城市口径不完全对称",
        },
        "diff_vs_old_draft": {
            "old": "旧稿 D=0.8165（十域）/ 0.6423（研发域），需求 18,075 条、供给 237 人、59 个集群映射",
            "now": f"B 口径 D={round(d_all,4)} / {round(d_rnd,4)}（供给 {len(szs)} 人）；"
                   f"A 口径 D={round(d_dir,4)} / {round(d_rnd_dir,4)}（供给 {len(sz_dir)} 人）",
            "why": "同一份招聘抽样。旧稿供给 237 人未说明分母；本件把「有集群标签的 59 人」"
                   "与「有研究方向的 123 人」分开报，D 随供给口径变化约 0.02—0.2，"
                   "说明这个指标对供给口径高度敏感",
        },
        "findings": [
            f"深圳岗位 {len(sz):,} 条（样本 {C.share(len(sz), len(rows))}%）；"
            f"供给 A {len(sz_dir)} 人 / B {len(szs)} 人；D 十域 A {round(d_dir,4)}、"
            f"B {round(d_all,4)}（研发口径 {round(d_rnd_dir,4)} / {round(d_rnd,4)}）",
            f"需求首位 {dem.most_common(1)[0][0]}（{C.share(dem.most_common(1)[0][1], dem_tot)}%），"
            f"供给首位（A 口径）{max(domains, key=lambda d: sup_d.get(d,0))}"
            f"（{round(100*max(supd_share.values()),2)}%）",
            f"最大错位：{gap[0]['domain']} 供给−需求 {gap[0]['diff_pp']:+.2f}pp；"
            f"{gap[-1]['domain']} {gap[-1]['diff_pp']:+.2f}pp",
        ],
    }
    C.write(METRIC, payload)
    print("demand", len(sz), C.share(len(sz), len(rows)), dem.most_common())
    print("supply", len(szs), sup.most_common())
    print("D", round(d_all, 4), round(d_rnd, 4))
    print("gap", gap[:3], gap[-3:])
    print("titles", titles.most_common(5))
    print("comps", comps.most_common(5))
    print("years", sorted(years.items()))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ORG_NEW_TREND · 新增科研机构趋势（gkx 口径重建件，零 SQL）

需求锚点：产品需求 §1.1.1.2.4.2.4.3（新增科研机构趋势统计 / 科研关注度判断）
          算法需求 §1.1.1.1.1.1.1.1.2（4）「统计历年新增涉足领域的科研机构数量」

口径（照抄旧稿公式，数据源换成 gkx 落盘快照）：
  1) 年度新增机构数 N(t) = 机构底册中「登记年份 = t」的家数（截面计数，不做存量累加）；
  2) 趋势方向 = 最近 3 年 OLS 斜率，|slope| ≤ 0.5 记「平稳」，否则升/降；
  3) 科研关注度 = 3 年斜率 + 5 年移动平均的组合判词（本件不给 0—100 分，避免造模型）；
  4) 领域维度：需求要「选定产业/技术领域内」，库内无机构×产业领域直接标签，
     退化为两条代理面——① 有专利机构按 IPC 主分类部聚合（部级，不是产业链环节）；
     ② 有国基金项目的机构按年份计数。两条都只作代理，不冒充领域口径。

数据源（全部为 gkx 只读快照，零 SQL）：
  _snapshots21/org_family_panel_20261021.json    2,074 家机构（成立年/城市/类型/专利/论文/项目/学者）
  _snapshots21/org_reg_gkx21.json                2,074 行登记字段（inc_date / capital / reg_status）
  _snapshots21/patent_ipc4_by_name_20261021.json 581,585 行 [ipc4, 申请人, 件数]（IPC 部代理）

硬约束（正文与产物同步披露）：
  * 底册 2,074 家 100% 位于广东省（深圳 1,014 / 广州 822 / 东莞 127 / 惠州 111），
    「全国新增趋势」不可得，只能作省内四城趋势；
  * inc_year 是法人登记年，不是建所年（老所改制/换证会落在近年），2016 年 326 家是登记批次峰；
  * 78 家无登记年（3.76%），不补 0、不按比例摊分，单列 no_year；
  * 2026 为残年（采集时点 2026-10），末端点不参与斜率判定（斜率窗口止于 2025）。

运行：cd code && python3 M_ORG_NEW_TREND.py
产物：code/M_ORG_NEW_TREND_out.json
"""
from __future__ import annotations

import json
import os
import statistics
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")

MID = "M_ORG_NEW_TREND"
Y0, Y1 = 2001, 2026
SLOPE_END = 2025          # 2026 为残年，不进斜率
CITIES = ("深圳市", "广州市", "东莞市", "惠州市")
CITY_SHORT = {"深圳市": "深圳", "广州市": "广州", "东莞市": "东莞", "惠州市": "惠州"}


# ---------------------------------------------------------------- 统计工具（内联自
# _org_deep21_common.py 的 dist/ols 思路，来源：本目录 code/_org_deep21_common.py）
def dist(vals):
    if not vals:
        return {"n": 0}
    s = sorted(vals)
    n = len(s)
    return {"n": n, "min": round(s[0], 2), "p25": round(s[int(n * .25)], 2),
            "median": round(statistics.median(s), 2), "mean": round(sum(s) / n, 2),
            "p75": round(s[int(n * .75)], 2), "p90": round(s[int(n * .9)], 2),
            "max": round(s[-1], 2)}


def ols_slope(pairs):
    """最小二乘斜率；pairs = [(x, y)]。点数 <2 返回 None。"""
    if len(pairs) < 2:
        return None
    n = len(pairs)
    mx = sum(p[0] for p in pairs) / n
    my = sum(p[1] for p in pairs) / n
    den = sum((p[0] - mx) ** 2 for p in pairs)
    if den == 0:
        return None
    return sum((p[0] - mx) * (p[1] - my) for p in pairs) / den


def direction(slope):
    if slope is None:
        return "样本不足"
    if slope > 0.5:
        return "上升"
    if slope < -0.5:
        return "下降"
    return "平稳"


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def main():
    panel = load("org_family_panel_20261021.json")
    reg = load("org_reg_gkx21.json")
    inst = panel["institutions"]

    # ---------------- 0. 口径自检：登记年份 vs 面板成立年
    inc_panel = {i["org_id"]: i.get("inc_year") for i in inst}
    inc_reg = {r["org_id"]: r.get("inc_year") for r in reg["rows"]}
    both = sum(1 for k in inc_panel if inc_panel.get(k) and inc_reg.get(k))
    same = sum(1 for k in inc_panel
               if inc_panel.get(k) and inc_reg.get(k)
               and int(inc_panel[k]) == int(inc_reg[k]))

    # ---------------- 1. 年度序列
    total = Counter()
    by_city = defaultdict(Counter)
    by_type = defaultdict(Counter)
    no_year = 0
    out_of_window = 0
    for i in inst:
        y = i.get("inc_year")
        if not y:
            no_year += 1
            continue
        y = int(y)
        if y < Y0 or y > Y1:
            out_of_window += 1
            continue
        total[y] += 1
        by_city[i["city"]][y] += 1
        by_type[i.get("org_type") or "(空)"][y] += 1

    years = list(range(Y0, Y1 + 1))
    series = []
    for y in years:
        pts = [(k, total.get(k, 0)) for k in range(y - 2, y + 1) if k >= Y0]
        s3 = ols_slope(pts) if y <= SLOPE_END else None
        w5 = [total.get(k, 0) for k in range(max(Y0, y - 4), y + 1)]
        series.append({"year": y, "new": total.get(y, 0),
                       "slope3": None if s3 is None else round(s3, 2),
                       "dir": direction(s3),
                       "ma5": round(sum(w5) / len(w5), 1)})

    # ---------------- 2. 关键统计（分母只用真实存在年份，DATA_FACTS §3.16）
    peak = max(series, key=lambda r: r["new"])
    top_years = sorted(series, key=lambda r: -r["new"])[:8]
    recent5 = sum(total.get(y, 0) for y in range(2021, 2026))
    prev5 = sum(total.get(y, 0) for y in range(2016, 2021))
    cagr_16_25 = ((total[2025] / total[2016]) ** (1 / 9) - 1) if total.get(2016) else None

    sz = by_city["深圳市"]
    stats_sz = {
        "peak_year": max(((y, sz.get(y, 0)) for y in years), key=lambda x: x[1])[0],
        "peak_new": max(sz.get(y, 0) for y in years),
        "slope_2015_2025": round(ols_slope([(y, sz.get(y, 0)) for y in range(2015, 2026)]), 2),
        "recent5_sum": sum(sz.get(y, 0) for y in range(2021, 2026)),
        "prev5_sum": sum(sz.get(y, 0) for y in range(2016, 2021)),
    }
    stats_sz["recent5_vs_prev5_pct"] = round(
        (stats_sz["recent5_sum"] - stats_sz["prev5_sum"]) / stats_sz["prev5_sum"] * 100, 2
    ) if stats_sz["prev5_sum"] else None

    # ---------------- 3. 领域代理面 A：IPC 部（仅 219 家有专利）
    ipc_by_name = load("patent_ipc4_by_name_20261021.json")
    names = {i["name"] for i in inst}
    org_sections = defaultdict(set)
    for ipc4, nm, _n in ipc_by_name:
        if nm in names and ipc4:
            org_sections[nm].add(ipc4[0].upper())
    SECTION_NAME = {"A": "A 人类生活必需", "B": "B 作业运输", "C": "C 化学冶金",
                    "D": "D 纺织造纸", "E": "E 固定建筑", "F": "F 机械工程",
                    "G": "G 物理", "H": "H 电学"}
    field_new = defaultdict(Counter)
    for i in inst:
        y = i.get("inc_year")
        if not y or not (Y0 <= int(y) <= Y1):
            continue
        secs = org_sections.get(i["name"]) or set()
        if not secs:
            continue
        # 主导部类 = 该机构 IPC4 集合里出现最多的部；并列取字典序首个（确定性）
        c = Counter(s for s in secs)
        sec = sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
        field_new[sec][int(y)] += 1
    field_tot = Counter({s: sum(v.values()) for s, v in field_new.items()})
    field_proxy = {
        "rule": "机构名精确命中 patent_ipc4_by_name 后，取其 IPC4 集合主导部（部级，不是产业链环节）",
        "covered_institutes": sum(field_tot.values()),
        "coverage_rate": round(sum(field_tot.values()) / len(inst), 4),
        "by_section": {SECTION_NAME.get(s, s): n for s, n in field_tot.most_common()},
        "series": {s: [{"year": y, "new": field_new[s].get(y, 0)} for y in range(2015, Y1 + 1)]
                   for s in [k for k, _ in field_tot.most_common(4)]},
    }

    # ---------------- 4. 领域代理面 B：国基金项目（仅 53 家）
    nsfc_new = Counter()
    for i in inst:
        if i.get("projects", 0) > 0 and i.get("inc_year"):
            y = int(i["inc_year"])
            if Y0 <= y <= Y1:
                nsfc_new[y] += 1
    nsfc_proxy = {
        "covered_institutes": sum(nsfc_new.values()),
        "coverage_rate": round(sum(nsfc_new.values()) / len(inst), 4),
        "series": [{"year": y, "new": nsfc_new.get(y, 0)} for y in range(2015, Y1 + 1)],
        "note": "机构名命中 dwd_zh_project 承担单位（58,452 行）的机构；NSFC 不是全口径科研项目",
    }

    # ---------------- 5. 结构画像
    by_city_series = {}
    for c in CITIES:
        by_city_series[CITY_SHORT[c]] = [{"year": y, "new": by_city[c].get(y, 0)} for y in years]
    type_keep = [t for t, _ in Counter(i.get("org_type") or "(空)" for i in inst).most_common(4)]
    by_type_series = {t: [{"year": y, "new": by_type[t].get(y, 0)} for y in years] for t in type_keep}

    coverage_note = panel.get("coverage", {})
    payload = {
        "metric_id": MID,
        "metric_name": "新增科研机构趋势",
        "domain": "TOPIC-ORG / 科研机构新增动态",
        "support_judgment": "部分支持",
        "support_reason": (
            "时间面完整可算：2,074 家机构中 1,996 家有登记年（96.24%），2001—2026 年度新增序列、"
            "3 年斜率、5 年移动平均全部可复现；但需求要的「选定产业/技术领域内」无法闭合——"
            "库内无机构×产业领域直接标签（技术标签仅命中 1 家），只能用 IPC 部（219 家，10.56%）"
            "与国基金项目（53 家，2.56%）两条代理面，且底册 100% 在广东省，不能称全国趋势。"
        ),
        "generated_at": "2026-10-22",
        "main_db": "gkx @ 183.240.141.251:3318（gkx_reader_zp，只读）",
        "sql_count": 0,
        "sources": [
            "code/_snapshots21/org_family_panel_20261021.json（2,074 家，built_at 2026-10-22 11:16:49）",
            "code/_snapshots21/org_reg_gkx21.json（source: gkx@183.240.141.251:3318/dwd_research_institute_base_info）",
            "code/_snapshots21/patent_ipc4_by_name_20261021.json（581,585 行）",
        ],
        "base_years_used": list(range(Y0, 2026)),
        "base_years_missing": [],
        "base_years_note": (
            "年度序列 2001—2026 逐年遍历，库内每年都有机构登记；2026 为残年（采集时点 2026-10），"
            "只展示不进斜率（斜率窗口止于 2025）。78 家无登记年（3.76%）不补 0、不摊分，"
            "单列 no_year；1996 年 1 家早于窗口，剔除并单列。跨年比较只用真实年份，未把缺失年按 0 摊入。"
        ),
        "probes": {
            "institute_total": len(inst),
            "institutes_with_year": len(inst) - no_year,
            "year_fill_pct": round((len(inst) - no_year) / len(inst) * 100, 2),
            "no_year": no_year,
            "out_of_window": out_of_window,
            "panel_vs_reg_both": both,
            "panel_vs_reg_same": same,
            "panel_reg_agree_pct": round(same / both * 100, 2) if both else None,
            "cities": dict(Counter(i["city"] for i in inst).most_common()),
            "org_types": dict(Counter(i.get("org_type") or "(空)" for i in inst).most_common()),
            "panel_coverage": {k: coverage_note.get(k) for k in
                               ("institutes", "names", "patent_matched_orgs", "papers_rows",
                                "scholars_rows", "projects_rows", "inst_with_tags")},
        },
        "series_total": series,
        "series_by_city": by_city_series,
        "series_by_type": by_type_series,
        "stats": {
            "peak_year": peak["year"],
            "peak_new": peak["new"],
            "second_peak": top_years[1] if len(top_years) > 1 else None,
            "sum_2001_2025": sum(total.get(y, 0) for y in range(2001, 2026)),
            "recent5_sum": recent5,
            "prev5_sum": prev5,
            "recent5_vs_prev5_pct": round((recent5 - prev5) / prev5 * 100, 2) if prev5 else None,
            "cagr_2016_2025_pct": round(cagr_16_25 * 100, 2) if cagr_16_25 is not None else None,
            "slope_2001_2025": round(ols_slope([(y, total.get(y, 0)) for y in range(2001, 2026)]), 2),
            "slope_2015_2025": round(ols_slope([(y, total.get(y, 0)) for y in range(2015, 2026)]), 2),
            "slope_2021_2025": round(ols_slope([(y, total.get(y, 0)) for y in range(2021, 2026)]), 2),
            "no_year": no_year,
        },
        "stats_sz": stats_sz,
        "field_proxy": field_proxy,
        "nsfc_proxy": nsfc_proxy,
        "top_years": top_years,
        "gaps": [
            "无机构×产业领域直接标签：技术标签表 32,322 家只命中 1 家，链标签 credit_code 与底册交集 3.5%（§3.1）",
            "IPC 部代理只覆盖 219/2,074（10.56%），且「部」不是产业链环节，不能回答『新能源新增了多少家』",
            "底册 2,074 家 100% 广东省内，省外 0 家，无法做全国或湾区九城趋势",
            "登记年 ≠ 建所年：2016 年 326 家是登记批次峰，不能读成『2016 年新建 326 家研究所』",
            "无「科研关注度」原始定义：需求只说『基于新增数量及增长速率』，本件给斜率+MA5 判词，未造 0—100 分",
        ],
    }

    out = os.path.join(HERE, f"{MID}_out.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)

    print("wrote", os.path.basename(out))
    print("institutes", len(inst), "with_year", len(inst) - no_year,
          "fill", payload["probes"]["year_fill_pct"], "%")
    print("peak", peak["year"], peak["new"], "| recent5", recent5, "prev5", prev5,
          "delta%", payload["stats"]["recent5_vs_prev5_pct"])
    print("slopes", payload["stats"]["slope_2001_2025"], payload["stats"]["slope_2015_2025"],
          payload["stats"]["slope_2021_2025"])
    print("sz peak", stats_sz["peak_year"], stats_sz["peak_new"], "recent5", stats_sz["recent5_sum"],
          "prev5", stats_sz["prev5_sum"])
    print("field proxy", field_proxy["covered_institutes"], field_proxy["coverage_rate"],
          "nsfc", nsfc_proxy["covered_institutes"], nsfc_proxy["coverage_rate"])


if __name__ == "__main__":
    main()

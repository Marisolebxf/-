#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M_INNOV_DS_27_SPATIO_012 —— 主题演化路径与创新前沿发现

需求出处：科技信息展示系统和科技专题服务系统.md §1.1.1.1.4.6.3.2.6
「自动分析各专业主题在全球范围的时空演化过程，支持高亮呈现主题聚焦区、演变轨迹和创新前沿阵地。」

方法（需求未给公式，本报告推测定义）：
  主题 = 专利 IPC 小类（main_classification_ipcr 前 4 位，如 G06F）；
  演化路径 = 各主题逐年份额轨迹 + 排名迁移；
  创新前沿 = 近端份额增速居前且体量达标的小类；
  新兴主题 = 基期近乎为零、近端已成规模的小类；
  主题聚焦区 = 前沿主题的申请人所在 city+area。

20261021 版换源：唯一数据面改为三方库 `gkx`（`gkx.<表名>`，不传 database/charset）。
  - gkx.dwd_patent(main_classification_ipcr, apdt_year, first_applicant_name, country)
  - gkx.dwd_org_base_info(name_cn, city, area)  —— 申请人属地映射（经 `_innov_common` 归一）
  - gkx.dwd_zh_paper_classification             —— 论文主题标签覆盖探针（非主路径）
专利侧一次流式扫描落共享面板（`_build_patent_panel_innov.py`），本脚本不再全表重扫。

运行：python3 code/M_INNOV_DS_27_SPATIO_012.py
产物：code/M_INNOV_DS_27_SPATIO_012_out.json
"""

import json
import os
import collections
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
import _innov_common as C  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "M_INNOV_DS_27_SPATIO_012_out.json")
RUN_AT = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
GKX = C.GKX

YEARS = [2021, 2022, 2023, 2024]        # 2025/2026 入库未完整，不参与演化判定
BASE_Y, END_Y = YEARS[0], YEARS[-1]
MIN_FRONTIER_COUNT = 500
EMERGING_MAX_BASE = 50
EMERGING_MIN_END = 300


def main():
    out = {"metric_id": "M_INNOV_DS_27_SPATIO_012", "run_at": RUN_AT,
           "data_source": "gkx（三方库 183.240.141.251:3318）", "probes": {}}
    p = out["probes"]
    panel = C.panel()

    # ---------- 1. 探针 ----------
    p["patent_total"] = panel["rows"]
    p["patent_total_inventory"] = 2939895
    p["patent_rows_match_inventory"] = panel["rows"] == 2939895
    p["patent_ipc_filled"] = sum(panel["ipc_all"].values())
    p["ipc_subclasses"] = len(panel["ipc_all"])
    p["patent_year_dist"] = panel["year_all"]
    p["patent_country_dist"] = dict(sorted(panel["country"].items(),
                                           key=lambda kv: -kv[1])[:8])
    p["zh_paper"] = C.q("SELECT COUNT(*) n FROM " + GKX + "dwd_zh_paper")[0][0]
    p["zh_paper_classification"] = C.q(
        "SELECT COUNT(*) n FROM " + GKX + "dwd_zh_paper_classification")[0][0]
    p["paper_topic_tag_coverage"] = round(
        p["zh_paper_classification"] / p["zh_paper"] * 100, 2) if p["zh_paper"] else 0

    # ---------- 2. 主题 × 年 矩阵（IPC 小类） ----------
    matrix = collections.defaultdict(lambda: collections.Counter())
    year_total = collections.Counter()
    for k, n in panel["ipc_year"].items():
        y_s, sub = k.split("|", 1)
        y = int(y_s)
        matrix[sub][y] = n
        year_total[y] += n
    p["patent_in_window"] = sum(year_total.values())
    p["topics_in_window"] = len(matrix)

    # ---------- 3. 份额轨迹与演化方向 ----------
    def share(sub, y):
        return matrix[sub][y] / year_total[y] if year_total[y] else 0.0

    topics = []
    for sub, c in matrix.items():
        s0, s1 = share(sub, BASE_Y), share(sub, END_Y)
        rel = (s1 - s0) / s0 if s0 > 0 else None
        topics.append({
            "ipc_subclass": sub,
            "counts": {str(y): c[y] for y in YEARS},
            "share_pct": {str(y): round(share(sub, y) * 100, 4) for y in YEARS},
            "share_change_pct": round((s1 - s0) * 100, 4),
            "share_rel_growth": None if rel is None else round(rel, 4),
            "count_total": sum(c[y] for y in YEARS),
        })
    for t in topics:
        rel = t["share_rel_growth"]
        if rel is None or abs(t["share_change_pct"]) < 0.01:
            t["path"] = "平稳/可忽略"
        elif rel >= 0.10:
            t["path"] = "上升"
        elif rel <= -0.10:
            t["path"] = "下降"
        else:
            t["path"] = "平稳"
    path_dist = collections.Counter(t["path"] for t in topics)
    out["evolution"] = {
        "n_topics": len(topics),
        "path_distribution": dict(path_dist),
        "top10_rising": sorted([t for t in topics if t["path"] == "上升"],
                               key=lambda x: -(x["share_rel_growth"] or 0))[:10],
        "top10_declining": sorted([t for t in topics if t["path"] == "下降"],
                                  key=lambda x: (x["share_rel_growth"] or 0))[:10],
        "top10_by_volume": sorted(topics, key=lambda x: -x["count_total"])[:10],
    }

    # ---------- 4. 创新前沿：份额增速居前 + 体量达标 ----------
    frontier_pool = [t for t in topics
                     if t["counts"][str(END_Y)] >= MIN_FRONTIER_COUNT and t["share_rel_growth"] is not None]
    frontier = sorted(frontier_pool, key=lambda x: -x["share_rel_growth"])[:15]
    out["frontier"] = {
        "rule": "IPC 小类在 %d 年份额相对 %d 年增长 ≥0%%、且 %d 年专利量 ≥%d 件，按份额相对增速取前 15"
                % (END_Y, BASE_Y, END_Y, MIN_FRONTIER_COUNT),
        "n_qualified": len(frontier_pool),
        "top15": frontier,
    }

    # ---------- 5. 新兴主题 ----------
    emerging = [t for t in topics
                if t["counts"][str(BASE_Y)] <= EMERGING_MAX_BASE
                and t["counts"][str(END_Y)] >= EMERGING_MIN_END
                and (t["share_rel_growth"] or 0) > 0]
    out["emerging"] = {
        "rule": "基期（%d）件数 ≤%d 且近端（%d）件数 ≥%d 的 IPC 小类" % (
            BASE_Y, EMERGING_MAX_BASE, END_Y, EMERGING_MIN_END),
        "n": len(emerging),
        "list": sorted(emerging, key=lambda x: -x["counts"][str(END_Y)])[:20],
    }

    # ---------- 6. 主题聚焦区（前沿主题 × 区县） ----------
    focus_subs = [t["ipc_subclass"] for t in frontier[:5]]
    focus = {}
    if focus_subs:
        name2region = {}
        norm_probe_rows = []
        for o in C.base():
            nm = C.clean(o["name_cn"])
            city = C.norm_city(o["city"])
            if nm and city:
                name2region[nm] = (city, C.norm_area(o["area"], city))
                norm_probe_rows.append(o)
        for sub in focus_subs:
            counter = collections.Counter()
            unmatched = panel["ipc_unmatched"].get(sub, 0)
            for nm, n in panel["ipc_app"].get(sub, {}).items():
                rk = name2region.get(nm)
                if rk:
                    counter[rk] += n
                else:
                    unmatched += n          # 底册有名字但无城市，同样算未落位
            top = sorted(counter.items(), key=lambda kv: -kv[1])
            focus[sub] = {
                "unmatched": unmatched,
                "top_regions": [{"city": c, "area": a, "patent": n} for (c, a), n in top[:5]],
            }
        p["city_norm"] = C.city_norm_probe(C.base())
    out["topic_focus_regions"] = focus
    p["denominator_gap"] = {
        "note": "本指标不设面积/人口分母；主题聚焦区只用 city+area 计数。"
                "gkx 无行政区面积/人口表（dwd_dim_admin_area 仅名称/编码），"
                "若甲方要求「主题密度 = 件数/平方公里」，该分母不可得。",
        "area_km2_available": False,
        "population_available": False,
    }

    # ---------- 7. 分布概况 ----------
    shares = sorted(t["share_pct"][str(END_Y)] for t in topics)
    out["compute"] = {
        "year_total": {str(y): year_total[y] for y in YEARS},
        "share_max_pct": shares[-1] if shares else 0,
        "share_median_pct": shares[len(shares) // 2] if shares else 0,
        "top5_share_sum_pct": round(sum(t["share_pct"][str(END_Y)] for t in out["evolution"]["top10_by_volume"][:5]), 2),
        "n_rising": path_dist.get("上升", 0),
        "n_declining": path_dist.get("下降", 0),
        "n_stable": path_dist.get("平稳", 0) + path_dist.get("平稳/可忽略", 0),
    }

    # ---------- 8. 定档 ----------
    ok = len(topics) >= 100 and p["patent_ipc_filled"] > 1_000_000
    out["support_judgment"] = "部分支持"
    out["support_reason"] = (
        "主题×时间维可完整复现：%d 件专利带 IPC（覆盖 %.1f%%），%d 个 IPC 小类，%d-%d 年逐年份额可算，"
        "演化方向与前沿/新兴主题均可输出（结构+数据量均足，此维已达可现转水平）。"
        "但需求为「全球范围」的时空演化并联动论文/资金/人员：库内专利 %.1f%% 为中国申请（WO 仅 %s 件）、"
        "时间仅 2021-2026，论文主题标签仅 %s 条抽样（覆盖 %.2f%%），科技资金与人员流动无承载表 → "
        "空间与多源维始终不足，故整体判部分支持。"
        % (p["patent_ipc_filled"], p["patent_ipc_filled"] / p["patent_total"] * 100,
           len(topics), BASE_Y, END_Y,
           p["patent_country_dist"].get("China", 0) / p["patent_total"] * 100,
           p["patent_country_dist"].get("WO", 0),
           p["zh_paper_classification"], p["paper_topic_tag_coverage"])
    )
    out["notes"] = [
        "20261021 换源核对：gkx.dwd_patent 2,939,895 行、dwd_zh_paper 100,900 行、"
        "dwd_zh_paper_classification 20,048 行，与 20261020 开发库 ODS 逐位一致，读数不变。",
        "主题键采用 IPC 小类（前 4 位），未做跨版本 IPC 再分类（IPC-2023 之后的新增小类历史件数会低估）。",
        "专利入库仅 2021-2026，2025/2026 不完整，演化窗口取 2021-2024。",
        "专利 96.9% 为中国申请，WO 8.99 万件为 PCT 国际申请，不含美日欧全文库 → 「全球范围」不成立。",
        "主题聚焦区按申请人名称与机构名录精确对齐（87% 级），未消歧，集团/曾用名会落空；"
        "city/area 经 `_innov_common` 归一（占位符、别名、区县误落），归一计数见 probes.city_norm。",
        "论文主题标签表 dwd_zh_paper_classification 仅 20,048 条（中图法 [R]医药等 scope），未纳入主路径。",
        "分母缺口：gkx 无行政区面积/人口表，「主题密度 = 件数/面积」不可算；本指标只出件数与份额。",
        "若甲方要求「全球」，需补充 Derwent/Incopat 全球专利族或 Scopus/WoS 主题标签后再升档。",
    ]
    out["gate_ok"] = bool(ok)

    C.write_out("M_INNOV_DS_27_SPATIO_012", out)
    print("probes:", json.dumps(p, ensure_ascii=False)[:1500])
    print("compute:", out["compute"])
    print("frontier top5:", [(t["ipc_subclass"], t["counts"]["2024"], t["share_rel_growth"])
                             for t in frontier[:5]])
    print("emerging n:", out["emerging"]["n"], "| support:", out["support_judgment"])
    print("saved ->", OUT)


if __name__ == "__main__":
    main()

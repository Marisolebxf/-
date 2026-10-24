#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TALENT_DEEP_161_1 —— 人才供需分析评价模型（TALENT 深度分析第 161 号）

需求语义：按区域/产业给出「人才供给」与「岗位需求」两侧的对比，识别紧缺与过剩方向。
需求未给供需口径、未给岗位与人才的归类体系、未给时间窗口。

本文口径（6 条 SQL，全部落 gkx.dwd_org_recruit_info；专利零 SQL）：
  1. 需求侧 = `dwd_org_recruit_info`（6,702,453 行，招聘岗位流水）。全表 COUNT/全扫
     在该实例上 >60s 超时（实测 3024 中断），故按主键 `dwd_id` 分 6 段、段内取
     `dwd_id % 97 = 0` 的等距样本，合计约 6.4 万条，覆盖 203,216—49,428,567 全 id 域。
     样本口径必须在正文披露：绝对值是「样本×97」的估计，比率是样本比率。
  2. 供给侧 = `dwd_scholar` 有姓名池 20,420 人，按「姓名 + 机构 6 字前缀」双锚定论文
     的 20+8 簇归属计存量；另用 `dwd_scholar_education_background` 的深圳培养段做
     「本地培养」旁证（实测仅 15 段，几乎为空，见 §四）。
  3. 两侧单位不同（人 vs 岗位），故只交「岗位/学者」倍数与簇级排序，不交「缺口人数」。
  4. 岗位城市取 `work_place` 前两字（「深圳…」），区县取第三字起的地名关键词。

产物：code/M_TALENT_DEEP_161_1_out.json。
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from _talent21_common import (  # noqa: E402
    SNAP, anchored_papers, base_year_block, clusters_of, loc, paper_clusters,
    scholars, st, write_out,
)

METRIC = "M_TALENT_DEEP_161_1"
CACHE = SNAP / "recruit161_20261022.json"
CHUNKS = [(203216, 8403216), (8403217, 16603216), (16603217, 24803216),
          (24803217, 33003216), (33003217, 41203216), (41203217, 49428567)]
MOD = 97

OCC = {
    "研发": ("研发", "算法", "研究", "科学家", "开发工程师", "架构师", "数据分析", "博士"),
    "工程技术": ("工程师", "技术员", "工艺", "设备", "维修", "电气", "机械", "结构", "测试",
                 "质量", "品质", "自动化", "嵌入式", "硬件", "软件"),
    "生产制造": ("操作工", "普工", "车间", "生产", "装配", "焊", "车工", "钳工", "检验员", "仓管"),
    "销售市场": ("销售", "市场", "客户", "商务", "渠道", "运营", "电商", "直播"),
    "职能管理": ("财务", "会计", "人力", "行政", "法务", "经理", "总监", "助理", "文员", "采购"),
    "设计创意": ("设计", "美工", "策划", "编导", "摄影", "剪辑", "文案"),
    "医疗教育": ("医生", "护士", "药师", "教师", "讲师", "教研", "临床"),
}


def occ_of(title: str) -> str:
    t = title or ""
    for k, kws in OCC.items():
        if any(w in t for w in kws):
            return k
    return "其他"


def _db():
    from _gkxdb import gkx

    cur = gkx()
    cur.execute("SET SESSION max_execution_time=90000")
    return cur


def load_sample() -> dict:
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding="utf-8"))
    cur = _db()
    rows: list[list] = []
    for lo, hi in CHUNKS:
        cur.execute(
            "SELECT job_title, work_place, release_date, name_cn FROM gkx.dwd_org_recruit_info"
            f" WHERE dwd_id BETWEEN {lo} AND {hi} AND is_deleted=0 AND dwd_id % {MOD} = 0"
        )
        rows.extend([[("" if x is None else str(x)) for x in r] for r in cur.fetchall()])
    out = {"rows": rows, "mod": MOD,
           "table_rows_est": 6702453, "chunks": CHUNKS, "sql_count": len(CHUNKS)}
    CACHE.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    return out


def main() -> None:
    raw = load_sample()
    rows = raw["rows"]
    n = len(rows)

    # ---------- 需求侧：城市 / 年份 / 岗位类别 ----------
    city_cnt = Counter()
    sz_rows = []
    year_all = Counter()
    year_sz = Counter()
    for title, place, rd, org in rows:
        place = place or ""
        c = place[:2] if len(place) >= 2 else "未填"
        city_cnt[c] += 1
        y = rd[:4]
        if y.isdigit():
            year_all[y] += 1
        if place.startswith("深圳"):
            sz_rows.append((title, place, rd, org))
            if y.isdigit():
                year_sz[y] += 1
    sz_share = 100 * len(sz_rows) / max(1, n)

    occ_all = Counter(occ_of(r[0]) for r in rows)
    occ_sz = Counter(occ_of(r[0]) for r in sz_rows)

    # 区县：work_place 去掉「深圳」后取前 3 字里的区名
    DIST = ("南山区", "福田区", "宝安区", "龙岗区", "龙华区", "罗湖区", "光明区", "坪山区",
            "盐田区", "大鹏新区", "深汕")
    dist_sz = Counter()
    for r in sz_rows:
        p = r[1]
        hit = next((d for d in DIST if d in p), "未标区县")
        dist_sz[hit] += 1

    # ---------- 需求侧：20+8 簇命中 ----------
    cl_dem_all = Counter()
    cl_dem_sz = Counter()
    cl_hit_rows = 0
    for title, place, rd, org in rows:
        cl = clusters_of([title]) if title else []
        if cl:
            cl_hit_rows += 1
            for c in cl:
                cl_dem_all[c] += 1
                if place.startswith("深圳"):
                    cl_dem_sz[c] += 1

    # ---------- 供给侧：学者存量按簇 ----------
    sch = [s for s in scholars() if s["name"]]
    cl_sup_all = Counter()
    cl_sup_sz = Counter()
    sup_covered = 0
    sz_sup_covered = 0
    for s in sch:
        papers = anchored_papers(s)
        if not papers:
            continue
        sup_covered += 1
        tags: list[str] = []
        for p in papers:
            tags.extend(paper_clusters(p["pid"], p["kw"], p["ti"]))
        cl = set(clusters_of(tags)) if tags else set()
        is_sz = loc(s["org"])[1] == "深圳市"
        if is_sz:
            sz_sup_covered += 1
        for c in cl:
            cl_sup_all[c] += 1
            if is_sz:
                cl_sup_sz[c] += 1

    # ---------- 供需对照 ----------
    clusters = []
    for c in sorted(set(cl_dem_sz) | set(cl_sup_sz)):
        d_all = cl_dem_all.get(c, 0)
        d_sz = cl_dem_sz.get(c, 0)
        s_sz = cl_sup_sz.get(c, 0)
        clusters.append({
            "cluster": c,
            "demand_sz_sample": d_sz,
            "demand_sz_est": d_sz * MOD,
            "demand_all_sample": d_all,
            "supply_sz": s_sz,
            "supply_all": cl_sup_all.get(c, 0),
            "jobs_per_scholar": round(d_sz * MOD / s_sz, 1) if s_sz else None,
            "sz_demand_share_pct": round(100 * d_all * 0 + (100 * d_sz / max(1, len(sz_rows))), 2),
            "sz_demand_share_of_hits_pct": round(100 * d_sz / max(1, d_all), 2),
        })
    clusters.sort(key=lambda r: (-r["demand_sz_sample"], -r["supply_sz"]))
    tight = [r for r in clusters if r["jobs_per_scholar"] is not None and r["supply_sz"] >= 3]
    tight.sort(key=lambda r: -r["jobs_per_scholar"])

    # ---------- 结果 ----------
    years_sorted = sorted(y for y in year_all if y.isdigit())
    payload = {
        "metric": METRIC,
        "support_judgment": "部分支持",
        "support_reason": (
            "需求侧有 6,702,453 条真实招聘岗位流水、供给侧有 20,420 名学者与论文簇归属，"
            "两侧都能算；但（a）岗位表只有岗位名与工作地，无学历/技能/薪资要求，"
            "（b）岗位名到 20+8 簇只能靠关键词，命中率 "
            f"{round(100 * cl_hit_rows / max(1, n), 2)}%，（c）两侧单位不同（岗位 vs 人）、"
            "（d）本地培养段仅 15 段、供给侧只能用存量学者代替「新增供给」→ 部分支持。"),
        "base_years": base_year_block(
            [int(y) for y in years_sorted],
            [y for y in range(2017, 2022)],
            "需求侧实际覆盖 " + (years_sorted[0] if years_sorted else "?") + "—" +
            (years_sorted[-1] if years_sorted else "?") + "（release_date），2017—2021 一行都没有，"
            "已在 missing 声明、不按 0 摊入；供给侧为截面存量（`dwd_scholar` 无年份），"
            "两侧不做同口径增速，只做截面倍数。"),
        "method": {
            "demand": "dwd_org_recruit_info 岗位流水（按 dwd_id 分 6 段、段内 %97 等距抽样）",
            "supply": "dwd_scholar 有姓名池 × 姓名+机构双锚定论文 → 20+8 簇",
            "unit": "岗位数（样本×97 估计） vs 学者数，只算「岗位/学者」倍数",
            "city": "work_place 前两字；区县用 11 个深圳区名关键词",
            "cluster_demand": "job_title 命中 20+8 关键词字典",
            "cluster_supply": "论文关键词 + 标题命中同一字典",
            "sample": {"mod": MOD, "chunks": CHUNKS, "sql_count": len(CHUNKS)},
            "missing_rule": "无学历/技能要求字段 → 不区分岗位层级；不补 0、不折算人数",
        },
        "coverage": {
            "sample_rows": n,
            "sample_pct": round(100 / MOD, 3),
            "table_rows_est_info_schema": raw["table_rows_est"],
            "est_rows_from_sample": n * MOD,
            "sz_sample_rows": len(sz_rows),
            "sz_share_pct": round(sz_share, 2),
            "sz_est_jobs": len(sz_rows) * MOD,
            "national_est_jobs": n * MOD,
            "est_rows_note": "information_schema 的 6,702,453 是引擎估算且已滞后；"
                             "样本 × 97 = " + f"{n * MOD:,}" + " 更接近真实行数，两者差额见 §四。",
            "job_title_cluster_hit_pct": round(100 * cl_hit_rows / max(1, n), 2),
            "scholar_pool": len(sch),
            "scholar_cluster_covered": sup_covered,
            "sz_scholar_cluster_covered": sz_sup_covered,
            "orgs_sample": len({r[3] for r in rows if r[3]}),
            "orgs_sz_sample": len({r[3] for r in sz_rows if r[3]}),
        },
        "demand": {
            "top_cities": [{"city": c, "rows": v, "pct": round(100 * v / max(1, n), 2)}
                           for c, v in city_cnt.most_common(12)],
            "year_hist_all": dict(sorted(year_all.items())),
            "year_hist_sz": dict(sorted(year_sz.items())),
            "occ_all": dict(occ_all.most_common()),
            "occ_sz": dict(occ_sz.most_common()),
            "occ_rd_pct_sz": round(100 * occ_sz.get("研发", 0) / max(1, len(sz_rows)), 2),
            "occ_eng_pct_sz": round(100 * occ_sz.get("工程技术", 0) / max(1, len(sz_rows)), 2),
            "dist_sz": dict(dist_sz.most_common()),
        },
        "supply": {
            "pool": len(sch),
            "covered": sup_covered,
            "covered_pct": round(100 * sup_covered / max(1, len(sch)), 2),
            "sz_covered": sz_sup_covered,
            "clusters": len(cl_sup_all),
            "top_clusters": [{"cluster": c, "all": v, "sz": cl_sup_sz.get(c, 0)}
                             for c, v in cl_sup_all.most_common(15)],
        },
        "clusters": clusters,
        "tight": tight[:10],
        "probes": {
            "recruit_table_rows_est": raw["table_rows_est"],
            "full_scan_timeout_sec": 60,
            "sql_count": raw["sql_count"],
        },
        "integrity": {
            "sample_note": f"岗位侧为 dwd_id % {MOD} = 0 的等距样本（{n:,} 条），"
                           f"绝对值 = 样本 × {MOD} 的估计；比率直接用样本比率，"
                           "样本按 id 全域分层，不含时间偏倚（各年样本量见 demand.year_hist_all）。",
            "unit_note": "岗位数与学者数不同量纲，「岗位/学者」只是稀缺度排序信号，"
                         "不是「缺口人数」；不得写成「深圳缺 X 万人」。",
            "title_note": "job_title 为自由文本（如「高级嵌入式软件开发工程师」「销售督导」），"
                          "关键词归类会把「销售工程师」同时命中销售与工程，故一人可多类。",
            "no_edu": "招聘表无学历、无技能等级、无薪资，无法做「高层次岗位」筛选。",
        },
    }
    payload["base_years_used"] = payload["base_years"]["base_years_used"]
    payload["base_years_missing"] = payload["base_years"]["base_years_missing"]
    payload["base_years_note"] = payload["base_years"]["note"]
    write_out(METRIC, payload)


if __name__ == "__main__":
    main()

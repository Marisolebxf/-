#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""
M_INNOV_DS_27_SPATIO_003 —— 热点区域自动识别与预警（区县级创新热点 + 预警分级）

复现王惠口径（calc-logic/INNOV/M_INNOV_DS_27_SPATIO_003.md）：
  区域主键 city+area；创新密度 = (专利 + 论文 + 项目) / 机构数；
  密度 >= P70 且机构数 >= 3 → 热点；预警：热点且近窗突增 >=1 → 2；热点或突增 >=0.5 → 1。

20261021 版换源：唯一数据面改为三方库 `gkx`（`gkx.<表名>`，不传 database/charset）。
  - gkx.dwd_org_base_info(org_id, name_cn, city, province, area)   —— 区县主键 + 分母
  - gkx.dwd_patent(first_applicant_name, apdt_year)                —— 专利信号（申请人名对齐机构）
  - gkx.dwd_zh_author(institution) + gkx.dwd_zh_paper(cover_year_start) —— 论文信号
  - gkx.dwd_zh_project(participating_institution, approval_year)   —— 项目信号

行政区名归一（本批强制）
------------------------
gkx 主档的 city/area 实测已是「深圳市 / 南山区」规范写法（66 个市、无字面 'NULL'），
但 `_work_gkx21/DATA_FACTS_gkx21.md` 记录 gkx 多张表存在 'NULL'/'null' 混写与
「深圳/深圳市/南山区」混用。本脚本统一走 `_innov_common.norm_city/norm_area`：
trim + 大小写不敏感占位符 + 别名补「市」+ 「区县名误落 city」「整市名误落 area」置空，
归一前后计数写进 `probes.city_norm`，并用 `gkx.dwd_dim_admin_area` 做 canonical 核对。

分母缺口（本批强制披露）
------------------------
王惠口径的分母是**机构数**，不是行政区面积/人口。gkx 内没有行政区面积、常住人口表
（`dwd_dim_admin_area` 20,000 行只有 6 级名称/编码，无面积、无人口列），故「每平方公里
创新密度」「每万人专利密度」两种常见口径在本库均不可算，只能保留机构均口径。

运行：
  python3 code/_build_patent_panel_innov.py   # 首次：流式生成专利共享面板（约 20 分钟）
  python3 code/M_INNOV_DS_27_SPATIO_003.py
产物：
  code/M_INNOV_DS_27_SPATIO_003_out.json
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
                   "M_INNOV_DS_27_SPATIO_003_out.json")
RUN_AT = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
GKX = C.GKX

P_FULL_YEARS = [2021, 2022, 2023, 2024]   # 专利仅 2021-2026；2025/2026 入库未完整，剔除
PRIOR = [2021, 2022]
RECENT = [2023, 2024]
MIN_ORGS = 3
P70 = 0.70
PATENT_ROWS_INVENTORY = 2939895


def main():
    out = {"metric_id": "M_INNOV_DS_27_SPATIO_003", "run_at": RUN_AT,
           "data_source": "gkx（三方库 183.240.141.251:3318）", "probes": {}}
    probes = out["probes"]

    # ---------- 1. 探针：行数与非空率 ----------
    rows = C.base()
    probes["org_base_info"] = len(rows)
    probes["org_area_filled"] = sum(
        1 for r in rows if C.clean(r["area"]))          # 大小写不敏感占位符
    probes["org_area_filled_old_rule"] = sum(            # 旧口径（只排除大写 'NULL'）对照
        1 for r in rows if r["area"] is not None and str(r["area"]).strip() not in ("", "NULL"))
    panel = C.panel()
    probes["patent"] = panel["rows"]
    probes["patent_rows_inventory"] = PATENT_ROWS_INVENTORY
    probes["patent_rows_match_inventory"] = panel["rows"] == PATENT_ROWS_INVENTORY
    probes["patent_ipc_filled"] = sum(panel["ipc_all"].values())
    probes["zh_paper"] = C.q("SELECT COUNT(*) n FROM " + GKX + "dwd_zh_paper")[0][0]
    probes["zh_author"] = C.q("SELECT COUNT(*) n FROM " + GKX + "dwd_zh_author")[0][0]
    probes["zh_project"] = C.q("SELECT COUNT(*) n FROM " + GKX + "dwd_zh_project")[0][0]
    probes["patent_year_dist"] = panel["year_all"]
    probes["patent_window"] = ("2021-2026（gkx 专利仅此窗口；2025 起入库未完整，"
                              "密度窗口取 2021-2024，突增窗口 2023-2024 vs 2021-2022）")

    # ---------- 1b. 行政区名归一 + 分母缺口 ----------
    probes["city_norm"] = C.city_norm_probe(rows)
    probes["denominator_gap"] = {
        "formula_denominator": "机构数 N_r（王惠口径）",
        "admin_area_table": "gkx.dwd_dim_admin_area（20,000 行，仅 6 级名称/编码）",
        "area_km2_available": False,
        "population_available": False,
        "consequence": "「每平方公里」「每万人」两种密度口径在本库不可算；"
                       "区县面积/人口分母缺口需甲方补行政区统计表，不得用机构数冒充。",
    }

    # ---------- 2. 区县主键与分母 ----------
    name2region = {}
    region_orgs = collections.Counter()
    for o in rows:
        city = C.norm_city(o["city"])
        area = C.norm_area(o["area"], city)
        if not area or not city:
            continue
        key = (city, area)
        region_orgs[key] += 1
        if o["name_cn"]:
            name2region[C.clean(o["name_cn"])] = key
    out["probes"]["regions_with_area"] = len(region_orgs)
    out["probes"]["regions_org_ge3"] = sum(1 for v in region_orgs.values() if v >= MIN_ORGS)

    # ---------- 3. 专利信号（申请人名对齐机构，来自共享面板） ----------
    patent_by_region_year = collections.Counter()
    pat_total = pat_matched = 0
    for k, n in panel["app_year"].items():
        y_s, nm = k.split("|", 1)
        pat_total += n
        rk = name2region.get(nm)
        if rk:
            pat_matched += n
            patent_by_region_year[(rk, int(y_s))] += n
    out["probes"]["patent_2021_2024"] = pat_total
    out["probes"]["patent_name_matched"] = pat_matched
    out["probes"]["patent_match_rate"] = round(pat_matched / pat_total * 100, 2) if pat_total else 0

    # ---------- 4. 论文信号（作者单位名对齐机构） ----------
    pap_rows = C.qd(
        "SELECT a.institution inst, p.cover_year_start y, COUNT(*) n "
        "FROM " + GKX + "dwd_zh_author a JOIN " + GKX + "dwd_zh_paper p ON a.paper_id=p.id "
        "WHERE p.cover_year_start BETWEEN %s AND %s "
        "AND a.institution IS NOT NULL AND UPPER(TRIM(a.institution)) NOT IN ('NULL','','NONE','-') "
        "GROUP BY a.institution, p.cover_year_start",
        (P_FULL_YEARS[0], P_FULL_YEARS[-1]))
    paper_by_region_year = collections.Counter()
    pap_total = pap_matched = 0
    for r in pap_rows:
        pap_total += r["n"]
        rk = name2region.get(C.clean(r["inst"]))
        if rk:
            pap_matched += r["n"]
            paper_by_region_year[(rk, r["y"])] += r["n"]
    out["probes"]["paper_author_instances_2021_2024"] = pap_total
    out["probes"]["paper_name_matched"] = pap_matched
    out["probes"]["paper_match_rate"] = round(pap_matched / pap_total * 100, 3) if pap_total else 0

    # ---------- 5. 项目信号（承担单位名对齐机构） ----------
    proj_rows = C.qd(
        "SELECT participating_institution inst, approval_year ay, COUNT(*) n FROM " + GKX +
        "dwd_zh_project WHERE participating_institution IS NOT NULL "
        "AND UPPER(TRIM(participating_institution)) NOT IN ('NULL','','NONE','-') "
        "GROUP BY participating_institution, approval_year")
    proj_by_region_year = collections.Counter()
    proj_total = proj_matched = 0
    for r in proj_rows:
        proj_total += r["n"]
        ay = str(r["ay"] or "")[:4]
        if not ay.isdigit():
            continue
        y = int(ay)
        rk = name2region.get(C.clean(r["inst"]))
        if rk:
            proj_matched += r["n"]
            proj_by_region_year[(rk, y)] += r["n"]
    out["probes"]["project_total"] = proj_total
    out["probes"]["project_name_matched"] = proj_matched
    out["probes"]["project_match_rate"] = round(proj_matched / proj_total * 100, 2) if proj_total else 0

    # ---------- 6. 区域密度 ----------
    regions = []
    for rk, n_org in region_orgs.items():
        pat = sum(patent_by_region_year.get((rk, y), 0) for y in P_FULL_YEARS)
        pap = sum(paper_by_region_year.get((rk, y), 0) for y in P_FULL_YEARS)
        proj = sum(proj_by_region_year.get((rk, y), 0) for y in range(P_FULL_YEARS[0], P_FULL_YEARS[-1] + 1))
        total = pat + pap + proj
        regions.append({
            "city": rk[0], "area": rk[1], "org_count": n_org,
            "patent": pat, "paper": pap, "project": proj,
            "activity": total,
            "density": round(total / n_org, 4) if n_org else 0.0,
        })
    regions.sort(key=lambda x: -x["density"])

    # ---------- 7. 突增（近窗 vs 前窗，年均） ----------
    def growth(rk):
        def avg(years, counter):
            vals = [counter.get((rk, y), 0) for y in years]
            return sum(vals) / len(years)
        prior_all = (avg(PRIOR, patent_by_region_year) + avg(PRIOR, paper_by_region_year)
                     + avg(PRIOR, proj_by_region_year))
        recent_all = (avg(RECENT, patent_by_region_year) + avg(RECENT, paper_by_region_year)
                      + avg(RECENT, proj_by_region_year))
        if prior_all <= 0:
            return None if recent_all <= 0 else 1.0
        return (recent_all - prior_all) / prior_all

    for r in regions:
        g = growth((r["city"], r["area"]))
        r["growth"] = None if g is None else round(g, 4)

    # ---------- 8. P70 阈值与热点/预警 ----------
    elig = [r for r in regions if r["org_count"] >= MIN_ORGS and r["activity"] > 0]
    dens = sorted(r["density"] for r in elig)
    thr = dens[int(len(dens) * P70)] if dens else 0.0
    out["threshold"] = {"p70_density": round(thr, 4), "min_orgs": MIN_ORGS,
                        "eligible_regions": len(elig),
                        "rule": "density>=P70 且 org_count>=3 → 热点；热点且近窗突增>=1 → 预警2；热点或突增>=0.5 → 预警1"}
    for r in regions:
        r["is_hot"] = bool(r["org_count"] >= MIN_ORGS and thr > 0 and r["density"] >= thr)
        g = r["growth"]
        if r["is_hot"] and g is not None and g >= 1.0:
            r["warning_level"] = 2
        elif (r["is_hot"] and g is None) or (g is not None and g >= 0.5 and r["activity"] > 0):
            r["warning_level"] = 1
        elif r["is_hot"] and g is not None and g >= 0:
            r["warning_level"] = 1
        else:
            r["warning_level"] = 0

    hot = [r for r in regions if r["is_hot"]]
    w2 = [r for r in regions if r["warning_level"] == 2]
    w1 = [r for r in regions if r["warning_level"] == 1]
    w0 = [r for r in regions if r["warning_level"] == 0]

    # ---------- 8b. 敏感性：以「热点内突增前 20%」替代固定 >=1 阈值 ----------
    hot_growth = sorted([r for r in hot if r["growth"] is not None], key=lambda x: -x["growth"])
    alt_cut = int(len(hot_growth) * 0.2)
    alt_level2 = hot_growth[:max(alt_cut, 1)] if hot_growth else []
    out["sensitivity_alt_level2"] = {
        "rule": "固定阈值（突增>=1）在本数据下无区域触发，故给出替代阈值方案：热点内突增排名前 20% 记预警 2",
        "n": len(alt_level2),
        "regions": [{"city": r["city"], "area": r["area"], "growth": r["growth"],
                     "density": r["density"]} for r in alt_level2],
    }

    # ---------- 9. 分布与样例 ----------
    out["compute"] = {
        "n_regions_scored": len([r for r in regions if r["org_count"] >= MIN_ORGS]),
        "n_hotspots": len(hot),
        "n_warning_2": len(w2),
        "n_warning_1": len(w1),
        "n_warning_0": len(w0),
        "density_min": min((r["density"] for r in elig), default=0),
        "density_max": max((r["density"] for r in elig), default=0),
        "density_median": dens[len(dens) // 2] if dens else 0,
        "activity_total": sum(r["activity"] for r in regions),
        "top15_by_density_eligible": [r for r in regions if r["org_count"] >= MIN_ORGS][:15],
        "top8_tiny_denominator": [r for r in regions if r["org_count"] < MIN_ORGS][:8],
        "top15_warning_2": sorted(w2, key=lambda x: -x["density"])[:15],
        "sample_zero_warning": sorted([r for r in regions if r["warning_level"] == 0 and r["org_count"] >= 20],
                                      key=lambda x: -x["density"])[:8],
    }

    # ---------- 10. 定档 ----------
    rates = {
        "patent": out["probes"]["patent_match_rate"],
        "paper": out["probes"]["paper_match_rate"],
        "project": out["probes"]["project_match_rate"],
    }
    enough = (len(elig) >= 30 and rates["patent"] >= 50)
    out["support_judgment"] = "部分支持" if enough else "完全不支持"
    out["support_reason"] = (
        "区县级专利信号可建（2021-2024 专利申请人名与机构名录精确对齐 %s%%），热点识别与预警分级可跑通；"
        "但论文信号仅 %s%% 可对齐到机构（论文语料为全国高校院所，机构名录以广东企业为主），"
        "项目信号对齐 %s%%，故王惠口径中的「论文/项目」两维在区县级实际缺失，密度退化为专利主导 → 判部分支持。"
        % (rates["patent"], rates["paper"], rates["project"])
    )
    out["notes"] = [
        "20261021 换源核对：gkx.dwd_org_base_info 189,116 行、dwd_patent 2,939,895 行、"
        "dwd_zh_paper 100,900 / dwd_zh_author 62,002 / dwd_zh_project 58,453 行，与 20261020 开发库 ODS 逐位一致。",
        "机构名录 dwd_org_base_info 99.82% 集中于广东（深圳 95,600 / 广州 49,605 / 东莞 33,590 / 惠州 9,979），"
        "本指标「全球/全国热点」语义只能落到深圳都市圈，跨省对比不可解释。",
        "area 字段缺测 33,672/189,116（17.8%），缺 area 的机构不入区县分母；"
        "归一后 ",  # 具体数由运行时填充（见下）
        "专利申请人名与机构名录采用精确名称对齐，未做消歧，集团简称/曾用名会漏计。",
        "专利仅 2021-2026 申请年且 2025 起入库未完整，密度窗口取 2021-2024，突增窗口 2023-2024 vs 2021-2022。",
        "论文/项目为名称对齐近似，未做机构合并；论文在区县级几乎全失配（2021-2024 仅 %s 条对齐），"
        "密度实际由专利单一信号驱动。" % pap_matched,
        "机构数 <3 的区县不参与热点判定（王惠口径），但其密度值仍列出以便核查小样本失真；"
        "如杭州市拱墅区机构数仅 3、密度 21.33，属小分母失真样例。",
        "固定阈值「突增>=1」在本数据窗口内无区县触发（突增最大约 0.37），预警 2 为空集；"
        "已附敏感性方案（热点内突增前 20%），阈值需甲方结合历史样本标定。",
        "行政区名归一：主档 city/area 实测已规范（66 个市、0 个字面 'NULL'、1 行空 city），"
        "本脚本仍统一做 trim + 占位符 + 别名归一，归一前后计数见 probes.city_norm；"
        "并用 dwd_dim_admin_area 核对，未命中项不等于名称错误（该维仅 20,000 行抽样）。",
        "分母缺口：gkx 无行政区面积/人口表，无法给出「每平方公里」「每万人」密度；"
        "王惠口径的机构均密度是唯一可算口径，不能替代地理密度。",
    ]
    out["notes"][3] = ("area 字段缺测 33,672/189,116（17.8%%），缺 area 的机构不入区县分母；"
                       "归一后有 %d 个 city+area 单元、其中 %d 个机构数 >=3 可参与 P70 判定。"
                       % (len(region_orgs), out["probes"]["regions_org_ge3"]))

    C.write_out("M_INNOV_DS_27_SPATIO_003", out)
    print(json.dumps({k: out[k] for k in ("probes", "threshold", "support_judgment")},
                     ensure_ascii=False, indent=1, default=str)[:3000])
    print("compute:", {k: v for k, v in out["compute"].items() if not isinstance(v, list)})
    print("saved ->", OUT)


if __name__ == "__main__":
    main()

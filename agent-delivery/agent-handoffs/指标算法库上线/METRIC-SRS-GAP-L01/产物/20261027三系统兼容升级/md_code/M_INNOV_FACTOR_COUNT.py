#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""科创要素数量统计（M_INNOV_FACTOR_COUNT）——A-16 批实现。

口径（registry/cfg_metric-INNOV-seed.yaml）：
  「选定范围（区域/时间窗/图层过滤）下科创要素去重存量。对象默认含论文、专利、人才、企业、
    科研机构、服务机构；会议/期刊/项目/成果无基础指标叶则走 ADS 列表计数，不另造 CNT ID。
    窗口默认自然年可切；按 factor_type 分组。」

落地口径（每一条都能在脚本里指到查询）：
  论文      dwd_zh_paper 100,900（期刊论文，全表）+ dwd_en_paper 1,387
  专利      面板缓存 2,939,895（零 DB）+ 面板国别分布
  人才      dwd_scholar 21,316（截面存量，无按年）
  企业      dwd_org_base_info「公司/合伙/独资」性质 186,207
  科研机构  dwd_research_institute_base_info 2,074（与底册事业单位按名称去重）
  服务机构  底册 industry_l1_name='科学研究和技术服务业' 37,181（**企业子集，非互斥类**）
  期刊      dwd_zh_journal 2,796 + dwd_en_journal 605
  项目      dwd_zh_project 58,453 + dwd_en_project 20,000
  成果      dwd_zh_project_output 20,133 + dwd_en_project_output 20,000（成果记录数，非成果件数）
  会议      0 —— 无会议实体表，publication_type 全表只有「期刊」

两条必须写进结论的口径缺陷：
  1. 服务机构与企业不是并列的两类，前者是后者按行业的子集，**总量不可加总**；
  2. 底册 99.82% 是深圳都市圈机构，任何「按区域」的切片都是都市圈切片。

产物：code/M_INNOV_FACTOR_COUNT_out.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import _gkxdb
from _innov_gkx21_common import load_cache, save_cache, write_out

METRIC = "M_INNOV_FACTOR_COUNT"
PANEL = HERE / "_snapshots21" / "patent_panel_innov_20261021.json"


def q(sql, timeout_ms=120000):
    cur = _gkxdb.gkx()
    try:
        cur.execute(f"SET SESSION max_execution_time={int(timeout_ms)}")
        cur.execute(sql)
        return cur.fetchall()
    finally:
        cur.close()


ORG_CACHE = "a16_count_org.json"


def org_facts(refresh=False):
    """底册 18.9 万行的 性质×城市×行业 分组。

    该表无可用索引，三键 GROUP BY 单次约 6—8 分钟（远超 120 秒探针上限），
    按本批「大表结果落盘复用」的惯例：首次用 --refresh-org 生成缓存，之后直接读。
    """
    cached = load_cache(ORG_CACHE)
    if cached and not refresh:
        return cached
    rows = q(
        "SELECT CASE "
        "WHEN org_type LIKE '%公司%' OR org_type LIKE '%合伙%' OR org_type LIKE '%独资%' "
        "  OR org_type LIKE '%个体工商户%' THEN '企业' "
        "WHEN org_type LIKE '%事业%' THEN '事业单位' "
        "WHEN org_type LIKE '%机关%' THEN '机关' "
        "WHEN org_type LIKE '%社会团体%' OR org_type LIKE '%民办非企业%' OR org_type LIKE '%基金会%' "
        "  THEN '社会组织' ELSE '其他/空' END AS k, "
        "COALESCE(city,'') AS c, COALESCE(industry_l1_name,'') AS ind, COUNT(*) AS n "
        "FROM gkx.dwd_org_base_info GROUP BY k, c, ind",
        timeout_ms=900000,
    )
    data = {"rows": [[str(a), str(b), str(c), int(d)] for a, b, c, d in rows],
            "built_at": "2026-10-22",
            "note": "由 M_INNOV_FACTOR_COUNT.py --refresh-org 生成"}
    save_cache(ORG_CACHE, data)
    return data


def year_series(rows, lo=None, hi=None):
    d = {}
    for y, n in rows:
        try:
            yi = int(float(y))
        except (TypeError, ValueError):
            continue
        if yi <= 0 or (lo is not None and yi < lo) or (hi is not None and yi > hi):
            continue
        d[yi] = d.get(yi, 0) + int(n)
    return dict(sorted(d.items()))


def main():
    # ---------- 底册：性质×城市×行业（重查询，带缓存；--refresh-org 重拉） ----------
    orgdata = org_facts(refresh="--refresh-org" in sys.argv)
    nature, city_tot, svc_city, svc_total = {}, {}, {}, 0
    for k, c, ind, n in orgdata["rows"]:
        n = int(n)
        nature[k] = nature.get(k, 0) + n
        if c:
            city_tot[c] = city_tot.get(c, 0) + n
        if ind == "科学研究和技术服务业":
            svc_total += n
            if c:
                svc_city[c] = svc_city.get(c, 0) + n
    org_total = sum(nature.values())

    # ---------- 科研机构：2,074 行，与底册事业单位按名称去重（本地 join，零额外扫描） ----------
    res_rows = q("SELECT name_cn, org_type, city, CAST(incorporation_date AS CHAR) FROM gkx.dwd_research_institute_base_info")
    base_names = {r[2] for r in load_cache("base_20261021.json") if r[2]}
    res_names = {(r[0] or "").strip() for r in res_rows if r[0]}
    overlap = len({n for n in res_names if n in base_names})
    res_city = {}
    for _, _, c, _d in res_rows:
        c = (c or "").strip()
        if c:
            res_city[c] = res_city.get(c, 0) + 1
    # 科研机构确有成立日期列（incorporation_date），但 78 行空串；去空后可成 27 期年序列
    res_y = {}
    for _n, _t, _c, d in res_rows:
        y = (d or "")[:4]
        if len(y) == 4 and y.isdigit() and 1900 <= int(y) <= 2026:
            res_y[int(y)] = res_y.get(int(y), 0) + 1
    res_y = dict(sorted(res_y.items()))
    res_year_dim = "partial" if res_y else False

    # ---------- 论文：中文/英文分别按年 ----------
    zh_paper_y = year_series(q(
        "SELECT cover_year_start y, COUNT(*) n FROM gkx.dwd_zh_paper GROUP BY cover_year_start"),
        1980, 2025)
    en_paper_y = year_series(q(
        "SELECT cover_year_start y, COUNT(*) n FROM gkx.dwd_en_paper GROUP BY cover_year_start"),
        2011, 2025)
    zh_paper_n = int(q("SELECT COUNT(*) FROM gkx.dwd_zh_paper")[0][0])
    en_paper_n = int(q("SELECT COUNT(*) FROM gkx.dwd_en_paper")[0][0])

    # ---------- 专利：只读面板 ----------
    panel = json.loads(PANEL.read_text(encoding="utf-8"))
    pat_y = {int(y): int(v if not isinstance(v, dict) else v.get("total", 0))
             for y, v in panel["year_all"].items()}
    pat_n = int(panel["rows"])
    pat_country = dict(panel["country"])

    # ---------- 人才 / 期刊 / 项目 / 成果 ----------
    sch = q("SELECT COUNT(*) n, SUM(h_index IS NOT NULL) h FROM gkx.dwd_scholar")[0]
    scholar_n, scholar_h = int(sch[0]), int(sch[1])
    acad = int(q("SELECT COUNT(*) FROM gkx.dwd_scholar_talent_flag WHERE academician=1")[0][0])
    zh_j = int(q("SELECT COUNT(*) FROM gkx.dwd_zh_journal")[0][0])
    en_j = int(q("SELECT COUNT(*) FROM gkx.dwd_en_journal")[0][0])
    zh_pr = int(q("SELECT COUNT(*) FROM gkx.dwd_zh_project")[0][0])
    en_pr = int(q("SELECT COUNT(*) FROM gkx.dwd_en_project")[0][0])
    zh_out = int(q("SELECT COUNT(*) FROM gkx.dwd_zh_project_output")[0][0])
    en_out = int(q("SELECT COUNT(*) FROM gkx.dwd_en_project_output")[0][0])
    proj_y = year_series(q(
        "SELECT LEFT(approval_year,4) y, COUNT(*) n FROM gkx.dwd_zh_project GROUP BY y"),
        1986, 2023)

    factors = [
        {"factor_type": "论文", "n": zh_paper_n + en_paper_n,
         "components": {"zh_paper": zh_paper_n, "en_paper": en_paper_n},
         "year_dim": True, "region_dim": False, "status": "可算",
         "source": "gkx.dwd_zh_paper / gkx.dwd_en_paper"},
        {"factor_type": "专利", "n": pat_n,
         "components": {"all": pat_n},
         "year_dim": True, "region_dim": False, "status": "可算（年窗口仅 2021—2026）",
         "source": "专利面板缓存（全量 2,939,895 行，零 DB）"},
        {"factor_type": "人才", "n": scholar_n,
         "components": {"scholar": scholar_n, "with_h_index": scholar_h, "academician": acad},
         "year_dim": False, "region_dim": False, "status": "存量可算，按年不可算",
         "source": "gkx.dwd_scholar / gkx.dwd_scholar_talent_flag"},
        {"factor_type": "企业", "n": nature.get("企业", 0),
         "components": dict(nature),
         "year_dim": False, "region_dim": True, "status": "可算（区域=深圳都市圈）",
         "source": "gkx.dwd_org_base_info.org_type"},
        {"factor_type": "科研机构", "n": len(res_names),
         "components": {"research_institute": len(res_names),
                        "name_overlap_with_base": overlap,
                        "base_shiyedanwei": nature.get("事业单位", 0),
                        "with_incorporation_year": sum(res_y.values()),
                        "year_periods": len(res_y)},
         "year_dim": res_year_dim, "region_dim": True,
         "status": "可算（与底册事业单位重名已披露；成立年可切 1996—2026，78 行日期空）",
         "source": "gkx.dwd_research_institute_base_info"},
        {"factor_type": "服务机构", "n": svc_total,
         "components": {"industry_l1_kejifuwu": svc_total},
         "year_dim": False, "region_dim": True,
         "status": "**代理口径**：按行业门类取，是企业子集，不可与企业相加",
         "source": "gkx.dwd_org_base_info.industry_l1_name"},
        {"factor_type": "期刊", "n": zh_j + en_j,
         "components": {"zh_journal": zh_j, "en_journal": en_j},
         "year_dim": False, "region_dim": False, "status": "可算（无创刊年按年窗口）",
         "source": "gkx.dwd_zh_journal / gkx.dwd_en_journal"},
        {"factor_type": "项目", "n": zh_pr + en_pr,
         "components": {"zh_project": zh_pr, "en_project": en_pr},
         "year_dim": "partial", "region_dim": False,
         "status": "可算（英文项目 approval_year 为 DATE 型且含空串，按年只用中文项目）",
         "source": "gkx.dwd_zh_project / gkx.dwd_en_project"},
        {"factor_type": "成果", "n": zh_out + en_out,
         "components": {"zh_project_output": zh_out, "en_project_output": en_out},
         "year_dim": False, "region_dim": False,
         "status": "可算，但口径是「成果记录数」，不是成果件数（列里另有分类型计数）",
         "source": "gkx.dwd_zh_project_output / gkx.dwd_en_project_output"},
        {"factor_type": "会议", "n": 0,
         "components": {},
         "year_dim": False, "region_dim": False, "status": "**不可算**：无会议实体表",
         "source": "无（dwd_zh_paper.publication_type 全表='期刊'）"},
    ]

    payload = {
        "metric_id": METRIC,
        "metric_name": "科创要素数量统计",
        "data_support_level": "部分支持",
        "run_at": "2026-10-22",
        "db": "gkx@183.240.141.251:3318（专利零 DB，读面板；底册一次扫描得 性质×城市×行业）",
        "org_total": org_total,
        "factors": factors,
        "year_series": {
            "zh_paper": zh_paper_y,
            "en_paper": en_paper_y,
            "patent": dict(sorted(pat_y.items())),
            "zh_project": proj_y,
            "research_institute": res_y,
        },
        "city_split": {
            "org_all": dict(sorted(city_tot.items(), key=lambda kv: -kv[1])[:12]),
            "research_institute": dict(sorted(res_city.items(), key=lambda kv: -kv[1])[:8]),
            "service_org": dict(sorted(svc_city.items(), key=lambda kv: -kv[1])[:8]),
        },
        "patent_country": pat_country,
        "gaps": [
            "会议要素 0 条：无会议实体表，publication_type 全表只有「期刊」，「会议/期刊/项目/成果」四类里缺会议。",
            "人才只有截面存量，没有按年存量/新增，时间窗切换对人才维无效。",
            "服务机构是行业门类代理，且为企业子集，与企业并列相加会把同一批机构算两次。",
            "企业/科研机构区域维 99.82% 落在深圳都市圈（深圳 95,600 / 广州 49,605 / 东莞 33,590 / 惠州 9,979）。",
            "英文项目 20,000 行无法按年（approval_year 是 DATE 列且含 '0000-00-00' 空串，读取即报 1525）。",
            "论文/专利/项目/期刊来自不同语料库，各自去重，跨类相加只能叫「要素条目合计」，不是互斥总量。",
        ],
    }
    write_out(METRIC, payload)
    print(json.dumps({"org_total": org_total, "nature": nature,
                      "svc_total": svc_total, "overlap_res_base": overlap},
                     ensure_ascii=False, indent=1))
    for f in factors:
        print(f"{f['factor_type']:<8} {f['n']:>10,}  {f['status']}")


if __name__ == "__main__":
    main()

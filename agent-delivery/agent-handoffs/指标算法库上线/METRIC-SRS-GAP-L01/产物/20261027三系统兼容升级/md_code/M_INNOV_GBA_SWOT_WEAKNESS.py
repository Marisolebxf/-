#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_GBA_SWOT_WEAKNESS · 湾区创新能力短板因素（20261021 换源版）

王惠 V1.5-20260830 口径：
  湾区 11 城、12 个分项，各分项在 11 城内降序排名（1 最好）；
  短板清单 = 该城 rank>=9 的分项；无命中则取 rank 最大 1 项并标 weak_signal=1。

20261021 换源硬约束
-------------------
1. 只读三方库 `gkx`（`code/_gkxdb.py`），不使用任何演示库或开发库旁路连接。
2. **不向 `gkx.dwd_patent` 发任何聚合 SQL**：专利资源与中山大学污染量全部从
   `_snapshots21/patent_panel_innov_20261021.json` 的 `app_year` 离线派生
   （面板已扫满 2,939,895 行，与表行数逐位相等）。
3. 联合专利用 `dwd_patent_applicants`（28,964 行、20,000 个 pn 的派生小表），
   不触 294 万行主表；该表只覆盖 0.68% 的 pn，故联合专利是「样本口径」，
   结果里显式披露 `joint_patent_coverage`。
4. 论文 / 项目 / 转移三张表均 <= 10 万行，单条带年份过滤的聚合可跑；
   结果落 `_snapshots21/gba_factors_20261021.json`，重跑不再连库。

输出：code/M_INNOV_GBA_SWOT_WEAKNESS_out.json
"""
from __future__ import annotations

import copy
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _gkxdb  # noqa: E402

OUT = HERE / "M_INNOV_GBA_SWOT_WEAKNESS_out.json"
CACHE = HERE / "_snapshots21" / "gba_factors_20261021.json"
PANEL = HERE / "_snapshots21" / "patent_panel_innov_20261021.json"
ORG_CITY = HERE / "_snapshots21" / "cityfam_orgbase_20261021.json"
TECH_TAGS = HERE / "_snapshots21" / "tech_tags_20261021.json"
POLICY = HERE / "_snapshots21" / "policy_base_20261021.json"

CITIES = ["深圳", "广州", "珠海", "佛山", "惠州", "东莞", "中山", "江门", "肇庆", "香港", "澳门"]
YEARS = [2021, 2022, 2023, 2024]

ADVICE = {
    "专利资源": "加大专利申请与布局",
    "论文资源": "加强论文产出与合作发表",
    "研发投入": "提高研发人员或上市研发经费",
    "载体数量": "引入和培育创新主体",
    "载体产出": "提升机构专利与论文产出",
    "科技型机构": "推动高企认定与科研院所建设",
    "联合专利": "推动多主体联合申请",
    "合作项目": "增加多机构立项",
    "成果转化": "提高专利转移占比",
    "政策供给": "完善地方创新政策供给",
    "政策覆盖": "拓展政策主题覆盖",
    "高企密度": "提高高新技术企业占比",
}


def q(sql, args=None):
    cur = _gkxdb.gkx()
    try:
        cur.execute("SET SESSION max_execution_time=180000")
        cur.execute(sql, args) if args else cur.execute(sql)
        return cur.fetchall()
    finally:
        cur.close()


def load_panel():
    d = json.loads(PANEL.read_text(encoding="utf-8"))
    app_year = d["app_year"]              # "2021|名称" -> 件数
    app_total = d["app_total"]            # 名称 -> 件数
    year_all = {int(k): v for k, v in d["year_all"].items()}
    return app_year, app_total, year_all


def patent_by_city(app_year, app_total, exclude=None):
    """名称含城市名的专利件数（第一申请人代理）。exclude: 需剔除的子串。"""
    out = {c: 0 for c in CITIES}
    for key, n in app_year.items():
        y, nm = key.split("|", 1)
        if int(y) not in YEARS or not nm:
            continue
        if exclude and exclude in nm:
            continue
        for c in CITIES:
            if c in nm:
                out[c] += int(n)
                break
    return out


def build_cache():
    """三张小表的聚合 + 名称污染量，一次落盘。"""
    app_year, app_total, year_all = load_panel()

    # ---- 论文：author_info_list 含城市名（100,900 行，单条聚合） ----
    sel = ",\n".join(
        f"SUM(author_info_list LIKE '%%{c}%%') AS `{c}`" for c in CITIES
    )
    row = q(f"SELECT COUNT(*) AS n, {sel} FROM gkx.dwd_zh_paper "
            f"WHERE cover_year_start BETWEEN '2021' AND '2026'")[0]
    paper = {c: int(row[i + 1] or 0) for i, c in enumerate(CITIES)}

    # ---- 合作项目：participating_institution（58,453 行；funded_institution 100% 空） ----
    sel2 = ",\n".join(
        f"SUM(participating_institution LIKE '%%{c}%%') AS `{c}`" for c in CITIES
    )
    row2 = q(f"SELECT COUNT(*) AS n, {sel2} FROM gkx.dwd_zh_project "
             f"WHERE LEFT(approval_year,4) IN ('2021','2022','2023')")[0]
    project = {c: int(row2[i + 1] or 0) for i, c in enumerate(CITIES)}

    # ---- 成果转化：转移前后权利人名称含城市名（22,809 行） ----
    sel3 = ",\n".join(
        f"SUM(CONCAT(IFNULL(transfer_before,''),IFNULL(transfer_after,'')) LIKE '%%{c}%%') AS `{c}`"
        for c in CITIES
    )
    row3 = q(f"SELECT COUNT(*) AS n, {sel3} FROM gkx.dwd_patent_transfer "
             f"WHERE transfer_effective_date BETWEEN '20210101' AND '20261231'")[0]
    transfer = {c: int(row3[i + 1] or 0) for i, c in enumerate(CITIES)}

    # ---- 联合专利：派生小表 dwd_patent_applicants（不触主表） ----
    rows = q("""SELECT pn, name FROM gkx.dwd_patent_applicants
                WHERE pn IN (SELECT pn FROM gkx.dwd_patent_applicants
                             GROUP BY pn HAVING COUNT(*) >= 2)""")
    joint = {c: set() for c in CITIES}
    for pn, nm in rows:
        if not nm:
            continue
        for c in CITIES:
            if c in nm:
                joint[c].add(pn)
                break
    joint_cnt = {c: len(v) for c, v in joint.items()}
    joint_meta = {
        "rows": len(rows),
        "distinct_pn_all": int(q("SELECT COUNT(DISTINCT pn) AS n FROM gkx.dwd_patent_applicants")[0][0]),
        "multi_pn": int(q("SELECT COUNT(*) AS n FROM (SELECT pn FROM gkx.dwd_patent_applicants "
                          "GROUP BY pn HAVING COUNT(*)>=2) t")[0][0]),
        "note": "派生小表只覆盖 20,000 个 pn（占主表 0.68%），联合专利为样本口径；不触 dwd_patent",
    }

    # ---- 名称污染量 ----
    contam = {}
    row4 = q(f"""SELECT
        SUM(author_info_list LIKE '%%中山大学%%') AS uni,
        SUM(author_info_list LIKE '%%中山市%%') AS city
        FROM gkx.dwd_zh_paper WHERE cover_year_start BETWEEN '2021' AND '2026'""")[0]
    contam["论文_含中山大学"] = int(row4[0] or 0)
    contam["论文_含中山市"] = int(row4[1] or 0)
    row5 = q("""SELECT
        SUM(participating_institution LIKE '%%中山大学%%') AS uni,
        SUM(participating_institution LIKE '%%中山市%%') AS city
        FROM gkx.dwd_zh_project WHERE LEFT(approval_year,4) IN ('2021','2022','2023')""")[0]
    contam["合作项目_含中山大学"] = int(row5[0] or 0)
    contam["合作项目_含中山市"] = int(row5[1] or 0)
    contam["专利_含中山大学"] = sum(
        int(n) for k, n in app_year.items()
        if int(k.split("|", 1)[0]) in YEARS and "中山大学" in k.split("|", 1)[1]
    )
    contam["专利_含中山市"] = sum(
        int(n) for k, n in app_year.items()
        if int(k.split("|", 1)[0]) in YEARS and "中山市" in k.split("|", 1)[1]
    )
    contam["高校名撞城市名说明"] = (
        "中山大学位于广州，名称含「中山」，会使中山市的分项值虚高；"
        "同类风险：香港中文大学（香港正确）、佛山科学技术学院（佛山正确）。"
    )

    # ---- 中山市剔除中山大学后的三项敏感性 ----
    zs = {
        "专利资源": patent_by_city(app_year, app_total, exclude="中山大学")["中山"],
        "论文资源": int(q("""SELECT SUM(author_info_list LIKE '%%中山%%'
                               AND author_info_list NOT LIKE '%%中山大学%%') AS n
                             FROM gkx.dwd_zh_paper
                             WHERE cover_year_start BETWEEN '2021' AND '2026'""")[0][0] or 0),
        "合作项目": int(q("""SELECT SUM(participating_institution LIKE '%%中山%%'
                               AND participating_institution NOT LIKE '%%中山大学%%') AS n
                             FROM gkx.dwd_zh_project
                             WHERE LEFT(approval_year,4) IN ('2021','2022','2023')""")[0][0] or 0),
    }

    # ---- 高企 / 机构 / 政策（全部读缓存） ----
    tags = json.loads(TECH_TAGS.read_text(encoding="utf-8"))
    orgs = json.loads(ORG_CITY.read_text(encoding="utf-8"))
    org_city = {}
    for oid, _nm, city, _st in orgs:
        if city:
            org_city.setdefault(oid, city)
    ht = {c: 0 for c in CITIES}
    for oid, tg in tags.items():
        if "高新技术企业" in (tg or []):
            c = org_city.get(oid)
            if c in ht:
                ht[c] += 1
    org_cnt = {c: 0 for c in CITIES}
    for _oid, _nm, c, _st in orgs:
        if c in org_cnt:
            org_cnt[c] += 1

    pol = json.loads(POLICY.read_text(encoding="utf-8"))
    policy = {c: 0 for c in CITIES}
    policy_total = 0
    for r in pol:
        city = (r.get("city") or "").strip()
        if city.upper() in ("NULL", "NONE", ""):
            continue
        policy_total += 1
        for c in CITIES:
            if city.startswith(c):
                policy[c] += 1
                break

    cache = {
        "built_at": "2026-10-22",
        "patent_year_total": year_all,
        "patent": patent_by_city(app_year, app_total),
        "paper": paper, "project": project, "transfer": transfer,
        "joint": joint_cnt, "joint_meta": joint_meta,
        "hightech": ht, "org": org_cnt, "policy": policy,
        "policy_total_nonnull": policy_total,
        "paper_rows_2021_2026": int(row[0]),
        "project_rows_2021_2023": int(row2[0]),
        "transfer_rows_2021_2026": int(row3[0]),
        "contamination": contam,
        "zhongshan_excl_university": zs,
    }
    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
    return cache


def dense_rank(items):
    """按值降序给出并列名次（1 最好，相同值同名次）。"""
    out = {}
    prev = None
    rank = 0
    for i, (k, v) in enumerate(items, 1):
        if prev is None or v != prev:
            rank = i
            prev = v
        out[k] = {"raw": v, "rank": rank, "n": len(items)}
    return out


def main():
    if CACHE.exists():
        cache = json.loads(CACHE.read_text(encoding="utf-8"))
    else:
        cache = build_cache()

    res = {
        "metric_id": "M_INNOV_GBA_SWOT_WEAKNESS",
        "metric_name": "湾区创新能力短板因素",
        "generated_at": "2026-10-22",
        "formula_owner": "仿王惠 V1.5-20260830（需求只给功能，无公式）",
        "data_source": "gkx 三方库 + _snapshots21 专利面板（零 dwd_patent SQL）",
    }

    factors = {
        "专利资源": cache["patent"],
        "论文资源": cache["paper"],
        "研发投入": None,
        "载体数量": None,
        "载体产出": None,
        "科技型机构": cache["hightech"],
        "联合专利": cache["joint"],
        "合作项目": cache["project"],
        "成果转化": cache["transfer"],
        "政策供给": cache["policy"],
        "政策覆盖": None,
        "高企密度": {
            c: round(cache["hightech"][c] / cache["org"][c], 6)
            for c in CITIES if cache["hightech"].get(c) and cache["org"].get(c)
        },
    }

    res["factor_coverage"] = {}
    for k, v in factors.items():
        pos = sorted([c for c, x in (v or {}).items() if x > 0])
        res["factor_coverage"][k] = (
            {"n_cities": len(pos), "cities": pos} if pos
            else {"n_cities": 0, "cities": [], "reason": "无数据支持"}
        )

    rank_table = {}
    for factor, vals in factors.items():
        if not vals:
            continue
        items = sorted([(k, v) for k, v in vals.items() if v > 0], key=lambda kv: -kv[1])
        rank_table[factor] = dense_rank(items)
    res["rank_table"] = rank_table

    def is_weak(factor, city):
        cell = rank_table.get(factor, {}).get(city)
        if not cell:
            return None
        n, r = cell["n"], cell["rank"]
        if n >= 11:
            return r >= 9
        return r > math.ceil(n * 2 / 3)

    city_out = {}
    for city in CITIES:
        items = []
        for factor in ADVICE:
            cell = rank_table.get(factor, {}).get(city)
            if not cell:
                continue
            items.append({"city": city, "factor": factor, "raw": cell["raw"], "rank": cell["rank"],
                          "n_cities": cell["n"], "weak": is_weak(factor, city),
                          "advice": ADVICE[factor]})
        weak = [x for x in items if x["weak"]]
        weakest = max(items, key=lambda x: x["rank"] / x["n_cities"]) if items else None
        city_out[city] = {
            "n_factors_scored": len(items),
            "weak_list": weak,
            "weak_signal": 1 if weak else 0,
            "weakest_factor": (None if not weakest else
                               {k: weakest[k] for k in ("factor", "raw", "rank", "n_cities")}),
            "missing_factors": [f for f in ADVICE if f not in rank_table],
        }

    res["city_result"] = city_out
    res["available_factors"] = [f for f in ADVICE if f in rank_table]
    res["missing_factors"] = [f for f in ADVICE if f not in rank_table]
    res["name_proxy_contamination"] = cache["contamination"]
    res["joint_patent_coverage"] = cache["joint_meta"]

    # 中山敏感性：只重算三个受影响分项的名次
    sens = {}
    for f, newv in cache["zhongshan_excl_university"].items():
        cells = copy.deepcopy(rank_table[f])
        old = cells["中山"]
        cells["中山"] = {"raw": newv, "rank": None, "n": old["n"]}
        order = sorted(cells.items(), key=lambda kv: -kv[1]["raw"])
        for i, (_k, v) in enumerate(order, 1):
            v["rank"] = i
        sens[f] = {"中山原值": old["raw"], "中山剔除中山大学后": newv,
                   "中山原名次": old["rank"], "中山新名次": cells["中山"]["rank"],
                   "n_cities": old["n"]}
    res["sensitivity_excl_university"] = sens

    res["support_judgment"] = {
        "data_support_level": "部分支持",
        "reasons": [
            "12 个分项中 4 项无数据：研发投入、载体数量、载体产出、政策覆盖；"
            "其中研发投入仅有上市主体年报（非全量），载体无台账，政策 theme 仅 2/20,000 非占位",
            "湾区 11 城中仅 4 城有机构底册（深圳 95,600 / 广州 49,605 / 东莞 33,590 / 惠州 9,979），"
            "其余 7 城 0~1 家 → 科技型机构与高企密度只能做 4 城排名",
            "专利资源由面板 app_year 离线派生（2021–2024 共 2,424,684 行），未发 dwd_patent SQL；"
            "论文/项目/转移为名称含城市名代理，非行政区划码口径",
            "联合专利用 28,964 行派生小表（20,000 个 pn，占主表 0.68%），是样本口径而非全量",
        ],
    }

    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(json.dumps(res["factor_coverage"], ensure_ascii=False, indent=1)[:2400])
    print("available:", res["available_factors"])
    print("missing:", res["missing_factors"])
    for c in ("深圳", "广州", "中山", "东莞"):
        print(c, "scored", city_out[c]["n_factors_scored"],
              "weak", [(x["factor"], x["raw"], f"{x['rank']}/{x['n_cities']}") for x in city_out[c]["weak_list"]])
    print("joint coverage:", cache["joint_meta"])
    print("wrote", OUT.name)


if __name__ == "__main__":
    main()

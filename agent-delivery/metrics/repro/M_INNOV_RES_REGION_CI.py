#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_INNOV_RES_REGION_CI （注册表未登记·工程件）
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_INNOV_RES_REGION_CI.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""区域竞争力指数（M_INNOV_RES_REGION_CI）· 零 DB 复现脚本

对象 = 区域（城市），不是企业。企业口径的竞争情报比对见 `M_INNOV_RES_CI_COMPARE`，
城市赛道级 LQ 对比见 `M_INNOV_CITY_COMPETE_SZ`；本件是四维合成指数，三者分母互不复用。

数据入口（全部读本地缓存，sql_count = 0）
------------------------------------------
* 专利 · 城市 × 年      : `_snapshots_gkx21/city_patent_year_gkx.json`
* 专利 · 城市 × IPC4    : `_snapshots21/patent_scan_20261021.pkl` 的 `ipc_pn`
* 专利 · 件型           : `_snapshots21/a25_patent_sample.json`（6.80% 主键切片，含 kind）
* 企业底册             : `_snapshots21/base_20261021.json`（189,116 行）
* 上市研发费用（年报）  : `_snapshots21/pg_stock_rd_annual_20261021.json`
* 政策                 : `_snapshots21/innov21_facts_20261021.json` 的 `policy_city`
* 机构技术标签         : `_snapshots21/tech_tags_20261021.json`（32,322 家，key=org_id）

口径红线
--------
1. 专利数字零 SQL：本脚本不连库，`sql_count` 恒为 0。
2. 2026 是残年、2025 受公开滞后影响，指数一律取 2024 年（最新完整年）。
3. 增速/基期只取真实存在年份（2021 与 2024），并在 `growth_reference.base_years_*` 写明。
4. 底册 47 个重名按「名 × 城」1/k 计权，各城之和 + 未匹配 = 专利总行数。
5. 研发费用只覆盖上市主体（2024 年报 658 家），不冒充全市 R&D；分母同步改为「有研发费用披露的上市主体数」。

产出：`code/M_INNOV_RES_REGION_CI_out.json`
"""
from __future__ import annotations

import collections
import json
import math
import pickle
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
CACHE = HERE / "_snapshots_gkx21"
METRIC_ID = "M_INNOV_RES_REGION_CI"
OUT = HERE / f"{METRIC_ID}_out.json"

REGIONS = ["深圳市", "广州市", "东莞市", "惠州市"]
SHORT = {"深圳市": "深圳", "广州市": "广州", "东莞市": "东莞", "惠州市": "惠州"}

PATENT_YEAR = 2024
SERIES_START = 2021
SERIES_END = 2024
IPC_UNIVERSE = 634

WEIGHTS = {"规模": 0.30, "效率": 0.25, "结构": 0.25, "环境": 0.20}

# 子指标键名与 `indicators` 字段一一对应（改键名必须同步改这里，否则该子指标会被静默跳过）
SUB_WEIGHTS = {
    "规模": {"patents_2024": 1 / 3, "firms": 1 / 3, "rd_2024_yi": 1 / 3},
    "效率": {"patents_per_firm": 0.5, "rd_per_listed_yi": 0.5},
    "结构": {"invention_share_pct": 1 / 3, "ipc_entropy_norm": 1 / 3, "invention_grant_share_pct": 1 / 3},
    "环境": {"policy_per_100_firms": 0.5, "tag_coverage_pct": 0.5},
}


def load_base():
    rows = json.loads((SNAP / "base_20261021.json").read_text(encoding="utf-8"))
    by_name, by_org = collections.defaultdict(list), {}
    for r in rows:
        org_id, nm, city = r[0], r[2], (r[4] or "")
        if nm:
            by_name[nm].append(city)
        if org_id:
            by_org[org_id] = city
    dups = {nm: cs for nm, cs in by_name.items() if len(cs) > 1}
    dup_stat = {
        "n_rows": len(rows),
        "n_names": len(by_name),
        "dup_names": len(dups),
        "dup_rows": sum(len(cs) for cs in dups.values()),
        "cross_city_names": sum(1 for cs in dups.values() if len(set(cs)) > 1),
        "cross_city_example": "中国建筑工程（香港）有限公司（广州市 1 家 / 深圳市 1 家，按 1/2 计权）",
    }
    return rows, by_org, by_name, dup_stat


def name_city_weights(by_name):
    out = {}
    for nm, cities in by_name.items():
        agg = collections.Counter(cities)
        k = len(cities)
        out[nm] = [(c or "?", n / k) for c, n in agg.items()]
    return out


def patents_by_city():
    d = json.loads((CACHE / "city_patent_year_gkx.json").read_text(encoding="utf-8"))
    groups = d["groups"]
    year = {c: float(groups.get(f"{c}|{PATENT_YEAR}", 0)) for c in REGIONS}
    series = {
        c: {str(y): float(groups.get(f"{c}|{y}", 0)) for y in range(SERIES_START, SERIES_END + 1)}
        for c in REGIONS
    }
    return year, series, d


def rd_by_city(by_org):
    rows = json.loads((SNAP / "pg_stock_rd_annual_20261021.json").read_text(encoding="utf-8"))
    amt, orgs, top1, top1_name = collections.defaultdict(float), collections.defaultdict(int), {}, {}
    bucket = collections.defaultdict(list)
    for r in rows:
        per = str(r["period"])
        if per[4:] != "12" or per[:4] != str(PATENT_YEAR):
            continue
        c = by_org.get(r["org_id"])
        if c not in REGIONS:
            continue
        v = float(r["rd"])
        amt[c] += v
        orgs[c] += 1
        bucket[c].append(v)
        if c not in top1 or v > top1[c]:
            top1[c] = v
            top1_name[c] = r["name"]
    top5 = {c: sum(sorted(bucket[c], reverse=True)[:5]) for c in bucket}
    return dict(amt), dict(orgs), top1, top1_name, top5


def kind_shares(name_w):
    smp = json.loads((SNAP / "a25_patent_sample.json").read_text(encoding="utf-8"))
    tot = collections.Counter()
    cnt = {k: collections.Counter() for k in ("A", "B", "U", "D")}
    for r in smp["rows"]:
        pr = name_w.get(r["first_applicant_name"])
        if not pr:
            continue
        k = r["kind"]
        for c, w in pr:
            if c not in REGIONS:
                continue
            tot[c] += w
            if k in cnt:
                cnt[k][c] += w
    out = {}
    for c in REGIONS:
        n = tot[c]
        out[c] = {
            "sample_patents": round(n, 2),
            "a_share": round(100 * cnt["A"][c] / n, 3) if n else None,
            "b_share": round(100 * cnt["B"][c] / n, 3) if n else None,
            "u_share": round(100 * cnt["U"][c] / n, 3) if n else None,
            "d_share": round(100 * cnt["D"][c] / n, 3) if n else None,
            "invention_share": round(100 * (cnt["A"][c] + cnt["B"][c]) / n, 3) if n else None,
        }
    return out, smp["meta"]


def ipc_entropy():
    d = pickle.loads((SNAP / "patent_scan_20261021.pkl").read_bytes())
    ipc_pn, row_city = d["ipc_pn"], d["row_city"]
    dist, covered, rows_all = {}, {}, {}
    for c in REGIONS:
        acc = collections.Counter()
        for (cc, y, k4), pns in ipc_pn.items():
            if cc != SHORT[c] or not (SERIES_START <= int(y) <= SERIES_END):
                continue
            acc[k4] += len(pns)
        n = sum(acc.values())
        h = -sum((v / n) * math.log(v / n) for v in acc.values()) if n else 0.0
        dist[c] = acc
        covered[c] = n
        rows_all[c] = sum(int(v) for (cc, y), v in row_city.items()
                          if cc == SHORT[c] and SERIES_START <= int(y) <= SERIES_END)
    out = {}
    for c in REGIONS:
        n = covered[c]
        h = -sum((v / n) * math.log(v / n) for v in dist[c].values()) if n else 0.0
        out[c] = {
            "ipc4_classes": len(dist[c]),
            "covered_patents_2021_2024": n,
            "series_patents_2021_2024": rows_all[c],
            "class_coverage_pct": round(100 * n / rows_all[c], 2) if rows_all[c] else None,
            "entropy_nats": round(h, 4),
            "entropy_norm": round(h / math.log(IPC_UNIVERSE), 4) if n else None,
            "top5": [[k, int(v)] for k, v in collections.Counter(dist[c]).most_common(5)],
        }
    return out


def ipc_entropy_crosscheck(name_w):
    rows = json.loads((SNAP / "patent_ipc4_by_name_20261021.json").read_text(encoding="utf-8"))
    acc = {c: collections.Counter() for c in REGIONS}
    for k4, nm, n in rows:
        pr = name_w.get(nm)
        if not pr:
            continue
        for c, w in pr:
            if c in REGIONS:
                acc[c][k4] += n * w
    out = {}
    for c in REGIONS:
        n = sum(acc[c].values())
        h = -sum((v / n) * math.log(v / n) for v in acc[c].values()) if n else 0.0
        out[c] = {"patents": round(n), "entropy_norm": round(h / math.log(IPC_UNIVERSE), 4)}
    return out


def env_inputs(by_org):
    facts = json.loads((SNAP / "innov21_facts_20261021.json").read_text(encoding="utf-8"))
    pol = facts["policy_city"]
    tags = json.loads((SNAP / "tech_tags_20261021.json").read_text(encoding="utf-8"))
    tag_city = collections.Counter()
    for oid in tags:
        c = by_org.get(oid)
        if c in REGIONS:
            tag_city[c] += 1
    return ({c: int(pol.get(c, 0)) for c in REGIONS}, dict(tag_city),
            {"policy_rows": facts["policy_total"], "placeholder_city_rows": pol.get("NULL", 0),
             "tag_orgs": len(tags)})


def minmax(vals):
    mx, mn = max(vals), min(vals)
    return [100.0 if mx == mn else round(100 * (v - mn) / (mx - mn), 2) for v in vals]


def maxscale(vals):
    mx = max(vals)
    return [round(100 * v / mx, 2) if mx else 0.0 for v in vals]


def compose(regions, dim_scores, weights):
    out = {}
    for r in regions:
        avail = {d: w for d, w in weights.items() if dim_scores[d][r] is not None}
        wsum = sum(avail.values())
        out[r] = round(sum(dim_scores[d][r] * w for d, w in avail.items()) / wsum, 2) if wsum else None
    return out


def rank(scores):
    order = sorted((r for r in scores if scores[r] is not None), key=lambda r: -scores[r])
    return {r: i + 1 for i, r in enumerate(order)}, order


def main():
    t0 = time.time()
    base_rows, by_org, by_name, dup_stat = load_base()
    name_w = name_city_weights(by_name)

    pat_year, pat_series, city_patent = patents_by_city()
    rd_amt, rd_orgs, rd_top1, rd_top1_name, rd_top5 = rd_by_city(by_org)
    kinds, sample_meta = kind_shares(name_w)
    ipc = ipc_entropy()
    ipc_x = ipc_entropy_crosscheck(name_w)
    pol, tag, env_meta = env_inputs(by_org)

    firms = {c: sum(1 for r in base_rows if (r[4] or "") == c) for c in REGIONS}

    indicators = {}
    for c in REGIONS:
        indicators[c] = {
            "patents_2024": round(pat_year[c]),
            "firms": firms[c],
            "rd_2024_yi": round(rd_amt.get(c, 0.0) / 1e8, 2),
            "listed_firms_2024": rd_orgs.get(c, 0),
            "patents_per_firm": round(pat_year[c] / firms[c], 4) if firms[c] else None,
            "rd_per_listed_yi": round(rd_amt.get(c, 0.0) / 1e8 / rd_orgs[c], 4) if rd_orgs.get(c) else None,
            "invention_share_pct": kinds[c]["invention_share"],
            "invention_grant_share_pct": kinds[c]["b_share"],
            "ipc_entropy_norm": ipc[c]["entropy_norm"],
            "policy_count": pol[c],
            "policy_per_100_firms": round(100 * pol[c] / firms[c], 4) if firms[c] else None,
            "tag_orgs": tag.get(c, 0),
            "tag_coverage_pct": round(100 * tag.get(c, 0) / firms[c], 3) if firms[c] else None,
            "rd_top1_share_pct": round(100 * rd_top1.get(c, 0.0) / rd_amt[c], 2) if rd_amt.get(c) else None,
            "rd_top5_share_pct": round(100 * rd_top5.get(c, 0.0) / rd_amt[c], 2) if rd_amt.get(c) else None,
            "rd_top1_name": rd_top1_name.get(c),
        }

    flat = {k: [indicators[c][k] for c in REGIONS] for k in indicators[REGIONS[0]]}

    def dim_scores_for(norm=minmax, ind=None):
        ind = ind or indicators
        d = {}
        for dim, subs in SUB_WEIGHTS.items():
            score = {}
            for c in REGIONS:
                acc, tot = 0.0, 0.0
                for key, w in subs.items():
                    v = ind[c].get(key)
                    if v is None:
                        continue
                    col = [ind[x][key] for x in REGIONS]
                    acc += norm(col)[REGIONS.index(c)] * w
                    tot += w
                score[c] = round(acc / tot, 2) if tot else None
            d[dim] = score
        return d

    dim_scores = dim_scores_for()
    totals = compose(REGIONS, dim_scores, WEIGHTS)
    ranks, order = rank(totals)

    schemes = {
        "main": dict(WEIGHTS),
        "equal": {"规模": 0.25, "效率": 0.25, "结构": 0.25, "环境": 0.25},
        "scale_heavy": {"规模": 0.40, "效率": 0.20, "结构": 0.20, "环境": 0.20},
        "structure_heavy": {"规模": 0.20, "效率": 0.20, "结构": 0.40, "环境": 0.20},
        "efficiency_heavy": {"规模": 0.20, "效率": 0.40, "结构": 0.20, "环境": 0.20},
        "environment_heavy": {"规模": 0.20, "效率": 0.20, "结构": 0.20, "环境": 0.40},
    }
    sens = {}
    for name, w in schemes.items():
        sc = compose(REGIONS, dim_scores, w)
        rk, od = rank(sc)
        sens[name] = {"weights": w, "scores": sc, "ranking": od, "rank": rk}

    sc_max = compose(REGIONS, dim_scores_for(norm=maxscale), WEIGHTS)
    sens["norm_maxscale"] = {"weights": WEIGHTS, "scores": sc_max,
                             "ranking": rank(sc_max)[1], "rank": rank(sc_max)[0],
                             "note": "归一改为 x/max×100（不平移到 0）"}

    ind_abs = json.loads(json.dumps(indicators))
    for c in REGIONS:
        ind_abs[c]["policy_per_100_firms"] = ind_abs[c]["policy_count"]
        ind_abs[c]["tag_coverage_pct"] = ind_abs[c]["tag_orgs"]
    ds_abs = dim_scores_for(ind=ind_abs)
    ds_abs["环境"] = ds_abs["环境"]
    # 只替换环境维，其他维保持主口径
    ds_abs_full = {d: dict(v) for d, v in dim_scores.items()}
    ds_abs_full["环境"] = dim_scores_for(ind=ind_abs)["环境"]
    sc_abs = compose(REGIONS, ds_abs_full, WEIGHTS)
    sens["env_absolute"] = {"weights": WEIGHTS, "scores": sc_abs,
                            "ranking": rank(sc_abs)[1], "rank": rank(sc_abs)[0],
                            "note": "环境维改用政策条数与标签机构数的绝对数"}

    env_tag = {c: minmax([indicators[x]["tag_coverage_pct"] for x in REGIONS])[REGIONS.index(c)]
               for c in REGIONS}
    ds_tag = {d: dict(v) for d, v in dim_scores.items()}
    ds_tag["环境"] = env_tag
    sc_tag = compose(REGIONS, ds_tag, WEIGHTS)
    sens["env_tag_only"] = {"weights": WEIGHTS, "scores": sc_tag,
                            "ranking": rank(sc_tag)[1], "rank": rank(sc_tag)[0],
                            "note": "环境维剔除政策数，只保留资质标签覆盖率"}

    rd_ex = {c: rd_amt.get(c, 0.0) - rd_top1.get(c, 0.0) for c in REGIONS}
    ind_ex = json.loads(json.dumps(indicators))
    for c in REGIONS:
        ind_ex[c]["rd_2024_yi"] = round(rd_ex[c] / 1e8, 2)
        ind_ex[c]["rd_per_listed_yi"] = round(rd_ex[c] / 1e8 / max(rd_orgs[c] - 1, 1), 4)
    ds_ex = dim_scores_for(ind=ind_ex)
    ds_ex_full = {d: dict(v) for d, v in dim_scores.items()}
    ds_ex_full["规模"] = ds_ex["规模"]
    ds_ex_full["效率"] = ds_ex["效率"]
    sc_ex = compose(REGIONS, ds_ex_full, WEIGHTS)
    sens["rd_ex_top1"] = {"weights": WEIGHTS, "scores": sc_ex,
                          "ranking": rank(sc_ex)[1], "rank": rank(sc_ex)[0],
                          "note": "规模与效率里的研发费用剔除各城研发第一名主体后重算"}

    pat_mean = {c: sum(pat_series[c].values()) / len(pat_series[c]) for c in REGIONS}
    ind_mean = json.loads(json.dumps(indicators))
    for c in REGIONS:
        ind_mean[c]["patents_2024"] = round(pat_mean[c])
        ind_mean[c]["patents_per_firm"] = round(pat_mean[c] / firms[c], 4)
    ds_mean = dim_scores_for(ind=ind_mean)
    ds_mean_full = {d: dict(v) for d, v in dim_scores.items()}
    ds_mean_full["规模"] = ds_mean["规模"]
    ds_mean_full["效率"] = ds_mean["效率"]
    sc_mean = compose(REGIONS, ds_mean_full, WEIGHTS)
    sens["patent_mean_2021_2024"] = {"weights": WEIGHTS, "scores": sc_mean,
                                     "ranking": rank(sc_mean)[1], "rank": rank(sc_mean)[0],
                                     "note": "规模与效率的专利改取 2021—2024 四年均值"}

    others = {d: w for d, w in WEIGHTS.items() if d != "结构"}
    osum = sum(others.values())
    s_sz = sum(dim_scores[d]["深圳市"] * w for d, w in others.items()) / osum
    s_gz = sum(dim_scores[d]["广州市"] * w for d, w in others.items()) / osum
    a, b = dim_scores["结构"]["深圳市"], dim_scores["结构"]["广州市"]
    flip = round((s_sz - s_gz) / ((s_sz - a) - (s_gz - b)), 4) if (s_sz - a) != (s_gz - b) else None

    churn = {}
    for k, v in sens.items():
        if k == "main":
            continue
        churn[k] = {"ranking": v["ranking"], "rank_of_深圳": v["rank"]["深圳市"],
                    "pair_swap_dg_hz": v["rank"]["东莞市"] > v["rank"]["惠州市"]}

    growth = {}
    for c in REGIONS:
        y0, y1 = pat_series[c][str(SERIES_START)], pat_series[c][str(SERIES_END)]
        growth[c] = {"2021": round(y0), "2024": round(y1),
                     "cagr_pct": round((math.pow(y1 / y0, 1 / (SERIES_END - SERIES_START)) - 1) * 100, 3)
                     if y0 else None}

    uni_patents = sum(pat_year.values())
    total_2024 = float(city_patent["year_coverage"]["year_all"]["2024"])
    unmapped_2024 = float(city_patent["unmapped_by_year"].get("2024", 0))
    mapped_2024 = total_2024 - unmapped_2024
    # 政策数与专利数的秩相关（4 城，用于说明环境维为何改强度口径）
    def _spearman(a, b):
        ra = {v: i for i, v in enumerate(sorted(a))}
        rb = {v: i for i, v in enumerate(sorted(b))}
        n = len(a)
        dsq = sum((ra[a[i]] - rb[b[i]]) ** 2 for i in range(n))
        return round(1 - 6 * dsq / (n * (n * n - 1)), 4)

    spl = _spearman([indicators[c]["policy_count"] for c in REGIONS],
                    [indicators[c]["patents_2024"] for c in REGIONS])
    payload = {
        "metric_id": METRIC_ID,
        "name": "区域竞争力指数（CI = competitiveness index）",
        "support_judgment": "部分支持",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "runtime_sec": None,
        "sql_count": 0,
        # 基期披露提到顶层（DATA_FACTS §3.16 / 派单书铁律 5）：
        # 增长参考用 2021 与 2024 两个真实存在的年份，2017—2020 在 dwd_patent 零行。
        "base_years_used": [SERIES_START, SERIES_END],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": ("dwd_patent.apdt_year 只有 2021—2026，2017—2020 一行都没有；"
                            "四维合成本身是 2024 年截面，不涉及时序分母。增速只作规模动态参考、"
                            "不入合成，且分母只取真实存在的 2021 年，不把缺失年按 0 摊入。"
                            "2025 年为残年（440,401 件）、2026 年更残，均不进基期也不作终点。"),
        "universe": {
            "regions": REGIONS,
            "region_count": len(REGIONS),
            "region_note": ("区域集合 = 深圳都市圈 4 市。底册 188,774/189,116 = 99.82% 在这 4 市，"
                            "其余 62 市合计 342 家、2024 年可归属专利不足 1%，不构成可比区域；"
                            "非粤城市（北京 163 家 / 上海 16 家）结构性不可用，不作排名"),
            "patents_2024_4cities": round(uni_patents),
            "patents_2024_all_rows": total_2024,
            "patents_2024_mapped": mapped_2024,
            "share_of_mapped_pct": round(100 * uni_patents / mapped_2024, 3),
            "share_of_all_patents_pct": round(100 * uni_patents / total_2024, 3),
            "unmapped_2024": int(unmapped_2024),
            "base_rows": len(base_rows),
            "dup_names": {**dup_stat,
                          "note": ("47 个重名共 94 行；其中 1 个跨城（中国建筑工程（香港）有限公司，"
                                   "广州/深圳各 1 家），按 1/2 计权；其余 46 个同城，不影响归属；"
                                   "各城之和 + 未匹配 = 2,939,895")},
        },
        "method": {
            "patent_year": PATENT_YEAR,
            "series_window": [SERIES_START, SERIES_END],
            "weights": WEIGHTS,
            "sub_weights": SUB_WEIGHTS,
            "normalization": "min-max 到 0—100（区域集合内）",
            "missing_dim_rule": "缺维按其余维权重重新归一，不补 0",
            "weight_note": ("权重为工程取值，不是文献标定：IMD 与社科院城市竞争力框架只给四维结构，"
                            "不给权重；本件主权重与等权两套都跑，见 sensitivity"),
            "dim_definition": {
                "规模": "区域创新体量：2024 年专利件数、企业数、上市主体研发费用",
                "效率": "户均产出：专利/企业、研发费用/有研发披露的上市主体",
                "结构": "质量与多样性：发明占比、IPC4 归一化熵、发明授权占比",
                "环境": "创新环境强度：每百家企业政策数、资质技术标签覆盖率",
            },
            "environment_intensity_note": (f"环境维用强度而非绝对数：4 城的政策数与专利数的秩相关 "
                                           f"Spearman={spl}，用绝对数会让环境维变成规模维的副本；"
                                           "绝对口径的结果作为敏感性单列"),
        },
        "indicators": indicators,
        "dimension_scores": dim_scores,
        "scores": totals,
        "ranking": order,
        "rank": ranks,
        "sensitivity": sens,
        "sensitivity_summary": {
            "flip_structure_weight": flip,
            "flip_note": (f"其余维按主权重比例缩放时，结构维权重超过 {flip:.3f} 广州即反超深圳；"
                          f"主权重为 0.25，故「深圳第一」在结构权重 ≥{flip:.3f} 的情形下不成立"),
            "rank_changes": churn,
        },
        "growth_reference": {
            "definition": "区域 2024 年专利件数相对 2021 年的 CAGR（不入合成，仅作规模动态参考）",
            "by_region": growth,
            "base_years_used": [SERIES_START, SERIES_END],
            "base_years_missing": [2017, 2018, 2019, 2020],
            "missing_note": ("gkx.dwd_patent.apdt_year 只有 2021—2026，2017—2020 一行都没有；"
                             "任何以 2017—2020 为基期的增速都是把缺失年当 0 摊进分母，本件不采用"),
        },
        "structure_detail": {
            "invention_sample": kinds,
            "invention_sample_meta": sample_meta,
            "ipc_entropy": ipc,
            "ipc_crosscheck": ipc_x,
            "ipc_note": ("主口径来自城市对标同族共享的 (城市, 年, IPC4)→pn 集合缓存，只保留全表 ≥300 件的"
                         "小类，故覆盖率为 77%—84%；交叉口径用 IPC4×申请人缓存独立归城，两套排序一致"
                         "（广州 > 东莞 > 惠州 > 深圳）"),
        },
        "environment_detail": {"policy_by_city": pol, "tag_orgs_by_city": dict(tag), **env_meta,
                               "policy_caveat": ("dwd_policy_base 20,000 条中 9,706 行 city 为字面 'NULL'"
                                                 "（国家级/省级），不落城；东莞仅 8 条、惠州 0 条，"
                                                 "属采集覆盖而非真实为零，故环境维并列敏感性")},
        "coverage": {
            "patent_series": "面板全量 2,939,895 行；2024 年可归属 529,394 件，未匹配 76,809 件（12.7%）",
            "kind_sample": "6.80% 主键连续切片 200,000 行，归城 174,025 行（87.0%）",
            "rd": "2024 年报口径 658 家（深圳 412 / 广州 157 / 东莞 71 / 惠州 18），占底册 0.35%",
            "policy": "全表 20,000 条，落城 10,294 条（4 城 1,212 条；深圳 879 / 广州 325 / 东莞 8 / 惠州 0）",
            "tag": "32,322 家机构，org_id 命中底册 32,321 家（99.997%）",
        },
        "gaps": [
            {"dim": "规模", "item": "区域 R&D 经费总额（全口径）", "status": "缺",
             "why": "库内无统计年鉴/GDP/R&D 支出表；dwd_org_annual_financial_info.arch_development_am 整列为空",
             "fix": "接入城市统计年鉴 R&D 经费支出（统计局），或省级科技统计年报"},
            {"dim": "效率", "item": "人均（每万人）口径", "status": "缺",
             "why": "无城市常住人口表；development_employee 整列为空（DATA_FACTS §3.10）",
             "fix": "接入常住人口与 R&D 人员全时当量"},
            {"dim": "结构", "item": "高价值专利占比（按价值分级）", "status": "代理",
             "why": "value 只有申请人×年合计，无逐件值，无法按阈值切高价值件",
             "fix": "专利价值逐件表（含价值分/被引/同族），或国知局高价值专利口径"},
            {"dim": "结构", "item": "发明占比", "status": "抽样",
             "why": "面板未落 kind 字段；只能用 6.80% 主键连续切片",
             "fix": "面板补 kind 列（一次全量扫即可，与现有 10 块同成本）"},
            {"dim": "环境", "item": "政策覆盖", "status": "偏",
             "why": "20,000 条政策里 48.5% 不落城，东莞 8 条、惠州 0 条，市级覆盖严重不全",
             "fix": "补地市级政策库（按发布机构归城），或改用省级政策按企业数分摊"},
            {"dim": "全域", "item": "区域集合", "status": "限",
             "why": "底册 99.82% 在深圳都市圈 4 市，全国其他城市无企业底册→无专利归属",
             "fix": "底册扩源到全国机构（工商全量），才能做省际/全国区域排名"},
        ],
        "conclusion": ("4 城可比、四维取数齐备，但区域集合只有深圳都市圈、两项为代理、政策维覆盖偏，"
                       "判「部分支持」；指数可用于都市圈内区域对比与差距分解，不可外推为全国区域排名"),
    }
    payload["runtime_sec"] = round(time.time() - t0, 2)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"[{METRIC_ID}] regions={len(REGIONS)} sql=0 runtime={payload['runtime_sec']}s")
    for c in order:
        print(f"  {c:4s} total={totals[c]:6.2f} rank={ranks[c]} "
              f"dims=" + " ".join(f"{d}:{dim_scores[d][c]:.1f}" for d in WEIGHTS))
    print("  flip_structure_weight =", flip)
    print("  writen", OUT)


if __name__ == "__main__":
    main()


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题服务算法库', '科技专题系统', '科技信息展示系统']

# 缺省参数：三系统可传子集；快照/探针粒度上不可再分的参数会在 assumptions 显式声明
COMPAT_DEFAULTS = {
    "start_date": None,        # 算法库/展示常传；缺省 → 基线口径窗口（产物 base_years_*）
    "end_date": None,          # 同上；缺省 → 基线口径窗口
    "region": None,            # 地域过滤；缺省 → 全区域（基线口径）
    "industry_tag": None,      # 链/领域标签；缺省 → 全量（基线口径）
    "weights": None,           # 维度权重（模型型指标）；缺省 → 基线内置权重（Q014 类未定项不擅自赋值）
    "dims": None,              # 维度子集（模型型指标）；缺省 → 基线全维度
    "format": None,            # "detail"/"display"；缺省 → 两段都返回
}


def compute(params=None):
    """三系统统一入口：执行基线 main() 的计算逻辑，读取其产物并附兼容元数据返回。

    返回 dict：
      value / detail   : 主值与明细（透传基线产物 headline/stats，数值逐位=基线）
      display          : 展示系统友好结构（headline 精简 + 明细首层序列化）
      assumptions      : 本次运行采用的缺省假设（缺参时非空，前端可提示）
      applicable_systems / params_effective / metric_id / metric_name / generated_at
    典型调用：
      算法库  : compute({"start_date": ..., "end_date": ..., "region": ...})   全参
      专题系统: compute({}) 或 compute({"industry_tag": "..."})               少传参
      展示系统: compute({"format": "display"})                                只要展示段
    """
    import importlib.util, json as _json, time as _time
    from pathlib import Path as _Path

    p_in = dict(params or {})
    eff = {**COMPAT_DEFAULTS, **{k: v for k, v in p_in.items() if v is not None}}
    assumptions = []
    for k, v in eff.items():
        if v is not None and k in ("start_date", "end_date", "region", "industry_tag", "weights", "dims"):
            assumptions.append(f"{k}={v!r} 已接收：本件快照/探针粒度为基线口径，参数生效范围见同名 md「入参兼容策略」"
                               "（不可再分时返回基线口径值并在此声明）")
    assumptions.append("本件为 20261021 基线口径包装（兼容层不改数学定义）；三系统主值同源")

    t0 = _time.time()
    here = _Path(__file__).resolve().parent
    out_json = here / "M_INNOV_RES_REGION_CI_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_INNOV_RES_REGION_CI.py 等价）
        run_baseline()
    data = _json.loads(out_json.read_text(encoding="utf-8"))

    headline = data.get("headline") or {}
    value = headline.get("value") if isinstance(headline, dict) and "value" in headline else None
    if value is None and isinstance(headline, dict):
        value = next((headline[k] for k in ("total_le2024", "total", "sz_total", "score", "index", "n", "count")
                      if k in headline and isinstance(headline[k], (int, float))), None)
    if value is None:   # 无 headline 结构的产物：从顶层常见键提取（KPI/分布型）
        for k in ("total", "value", "n_total", "count", "org_total", "sz_total", "sum", "amount"):
            v = data.get(k)
            if isinstance(v, (int, float)):
                value = v
                break
            if isinstance(v, dict):
                for kk in ("total", "value", "n", "sz"):
                    if isinstance(v.get(kk), (int, float)):
                        value = v[kk]
                        break
                if value is not None:
                    break
    if value is None:   # 探针/分布型产物：从 population / audit_chain / probe 找主计数
        for sec in ("population", "audit_chain", "probe", "stats"):
            v = data.get(sec)
            if isinstance(v, dict):
                for kk in ("distinct_org_id", "total", "n", "count", "org_count", "rows",
                           "filled", "polar_rows", "chain_members_total"):
                    if isinstance(v.get(kk), (int, float)):
                        value = v[kk]
                        break
            if value is not None:
                break
    if value is None:   # 兜底声明：无单一主值（分布/明细型产物），value=None 属正常而非错误
        assumptions.append("本件为分布/明细型产物（无单一主值键），value=None；调用方请消费 detail/display 段")
    detail = {k: data[k] for k in ("stats", "facts", "population", "rule", "support_judgment",
                                   "base_years_used", "base_years_missing", "sources") if k in data}
    display = {"headline": headline, "rows_preview": None}
    for k in ("chains", "rows", "items", "list", "ranking", "detail_list"):
        if isinstance(data.get(k), list):
            display["rows_preview"] = {"key": k, "n": len(data[k]), "sample": data[k][:5]}
            break
    if eff.get("format") == "display":
        detail = {"support_judgment": data.get("support_judgment")}
    return {
        "metric_id": "M_INNOV_RES_REGION_CI",
        "metric_name": data.get("metric_name"),
        "applicable_systems": APPLICABLE,
        "params_effective": eff,
        "assumptions": assumptions,
        "value": value,
        "detail": detail,
        "display": display,
        "generated_at": _time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_sec": round(_time.time() - t0, 2),
        "baseline_generated_at": data.get("generated_at"),
    }


def run_baseline():
    """原样执行基线 main()（兼容层调用；产物 _out.json 由基线逻辑写盘，铁律：产物只由脚本产出）。"""
    main()  # noqa: F821  ← 基线入口（上方原代码定义）

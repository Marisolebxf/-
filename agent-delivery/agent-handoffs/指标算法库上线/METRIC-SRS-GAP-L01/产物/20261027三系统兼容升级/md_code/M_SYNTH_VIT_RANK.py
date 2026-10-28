#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_SYNTH_VIT_RANK 对比范围活力排名（gkx 换源重建，零 SQL）。

口径（calc-logic/SYNTH/M_SYNTH_VIT_RANK.md）：
    目标区域在所选对比范围内按区域创新活力指数降序的名次。
    默认对比范围 11 城：北京/上海/广州/深圳/杭州/南京/武汉/重庆/宁波/成都/合肥。
    RANK() OVER (ORDER BY vit_index DESC)，同分并列（下一名跳号）；无指数不进榜。

两层口径（本文强制分开写）：
  ① 严格王惠口径：四维（科技/产业/人才/政策）齐全才进场，缺任一维不计算、不拿 0 顶。
  ② 降维参考口径：在可得维上等权平均（缺维不补 0），并设维覆盖门槛（≥3/4）才进榜。

四维的取数（全部读落盘快照，脚本内零 SQL）：
  科技  T1 2024 年专利授权行数（申请人名→城市，重名 1/k 摊）
        T2 高被引中文论文数（被引 ≥ 全库 p70 且 >0）
  产业  I1 国家级高新技术企业数（tech_tags 的「高新技术企业」标签 × 底册城市）
  人才  P2 高学历人才占比（学者学位含硕士/博士的比例）
  政策  S1 政策存量条数（dwd_policy_base 全表，按 §3.7 不按年截断）
        S2 政策文种覆盖度（该城出现的文种数 ÷ 全库文种数）

输出：code/M_SYNTH_VIT_RANK_out.json
"""
from __future__ import annotations

import collections
import json
import time

import _synth21_common as S

MID = "M_SYNTH_VIT_RANK"
CITY11 = ["北京市", "上海市", "广州市", "深圳市", "杭州市", "南京市",
          "武汉市", "重庆市", "宁波市", "成都市", "合肥市"]
CITY4 = ["深圳市", "广州市", "东莞市", "惠州市"]
CITY_CODE = {"北京市": "110000", "上海市": "310000", "广州市": "440100", "深圳市": "440300",
             "杭州市": "330100", "南京市": "320100", "武汉市": "420100", "重庆市": "500000",
             "宁波市": "330200", "成都市": "510100", "合肥市": "340100",
             "东莞市": "441900", "惠州市": "441300"}
STAT_YEAR = 2024
MIN_DIM = 3
SUFF = {"科技": {"grants": 1000},
        "产业": {"hightech": 100},
        "人才": {"scholars": 100},
        "政策": {"policies": 30}}


def mm01(d: dict) -> dict:
    vals = [v for v in d.values() if v is not None]
    if not vals:
        return {}
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return {k: 50.0 for k, v in d.items() if v is not None}
    return {k: round((v - lo) / (hi - lo) * 100, 2) for k, v in d.items() if v is not None}


def rank_r(values: dict) -> dict:
    """RANK() 语义：降序、同分并列、下一名跳号。"""
    order = sorted(values.items(), key=lambda x: -x[1])
    out, prev, prev_rank = {}, None, 0
    for i, (k, v) in enumerate(order, start=1):
        if prev is not None and abs(v - prev) < 1e-9:
            out[k] = prev_rank
        else:
            out[k] = i
            prev_rank, prev = i, v
    return out


def main() -> None:
    t0 = time.time()

    # ---------------- 原始值 ----------------
    grants = S.grants2024_by_city()
    g_by_city = {c: round(grants["by_city"].get(c, 0)) for c in CITY11 + ["东莞市", "惠州市"]}

    # 高被引论文：被引 ≥ p70 且 >0
    cites = {}
    probe = json.loads((S.SNAP / "probe_a26_20261022.json").read_text(encoding="utf-8"))
    for pid, n in probe["zh_citation"]["rows"]:
        try:
            cites[str(pid)] = int(n or 0)
        except (TypeError, ValueError):
            continue
    cv = sorted(v for v in cites.values() if v > 0)
    p70 = cv[int(len(cv) * 0.7)] if cv else 0
    hq = collections.Counter()
    n_hq = 0
    for p in S.papers():
        if cites.get(p["id"], 0) >= p70 and cites.get(p["id"], 0) > 0:
            n_hq += 1
            for c in p["cities"]:
                hq[c] += 1
    hq_by_city = {c: hq.get(c, 0) for c in CITY11 + ["东莞市", "惠州市"]}

    ht = S.hightech_by_city()
    ht_by_city = {c: ht.get(c, 0) for c in CITY11 + ["东莞市", "惠州市"]}

    sch = S.scholars()
    deg = S.scholar_degrees()
    s_tot, s_hi = collections.Counter(), collections.Counter()
    for s in sch:
        c = s["city"]
        if not c:
            continue
        s_tot[c] += 1
        if deg.get(s["id"]) in ("博士", "硕士"):
            s_hi[c] += 1
    scholars_by_city = {c: s_tot.get(c, 0) for c in CITY11 + ["东莞市", "惠州市"]}
    hiedu_by_city = {c: (round(s_hi[c] / s_tot[c], 4) if s_tot.get(c) else None)
                     for c in CITY11 + ["东莞市", "惠州市"]}

    prows = json.loads((S.SNAP / "pg_policy_rows_20261021.json").read_text(encoding="utf-8"))
    all_types = {str(r.get("type") or "").strip() for r in prows}
    all_types.discard("")
    all_types.discard("NULL")
    pol = collections.Counter()
    ptype = collections.defaultdict(set)
    for r in prows:
        c = (r.get("city") or "").strip()
        if not c or c == "NULL":
            continue
        pol[c] += 1
        t = str(r.get("type") or "").strip()
        if t and t != "NULL":
            ptype[c].add(t)
    pol_by_city = {c: pol.get(c, 0) for c in CITY11 + ["东莞市", "惠州市"]}
    ptype_cov = {c: (round(len(ptype[c]) / len(all_types), 4) if ptype.get(c) else None)
                 for c in CITY11 + ["东莞市", "惠州市"]}

    # ---------------- 逐维可用性门槛 ----------------
    pool_all = CITY11 + [c for c in ("东莞市", "惠州市") if c not in CITY11]
    suff, excluded = {}, {}
    for c in pool_all:
        suff[c] = {
            "科技": g_by_city[c] >= SUFF["科技"]["grants"],
            "产业": ht_by_city[c] >= SUFF["产业"]["hightech"],
            "人才": scholars_by_city[c] >= SUFF["人才"]["scholars"],
            "政策": pol_by_city[c] >= SUFF["政策"]["policies"],
        }
        n_ok = sum(1 for v in suff[c].values() if v)
        if n_ok < MIN_DIM:
            why = []
            if not suff[c]["科技"]:
                why.append("2024 年专利授权归城 %d 件（<%d）" % (g_by_city[c],
                                                                SUFF["科技"]["grants"]))
            if not suff[c]["产业"]:
                why.append("高企 %d 家（<%d）" % (ht_by_city[c], SUFF["产业"]["hightech"]))
            if not suff[c]["人才"]:
                why.append("学者 %d 人（<%d）" % (scholars_by_city[c], SUFF["人才"]["scholars"]))
            if not suff[c]["政策"]:
                why.append("政策 %d 条（<%d）" % (pol_by_city[c], SUFF["政策"]["policies"]))
            excluded[c] = {"dims_ok": n_ok, "reason": "；".join(why)}

    # ---------------- 打分（在进榜池内 minmax） ----------------
    def dim_scores(pool):
        g = mm01({c: g_by_city[c] for c in pool})
        h = mm01({c: hq_by_city[c] for c in pool})
        tech = {c: round((g.get(c, 0) + h.get(c, 0)) / 2, 2) if c in g or c in h else None
                for c in pool}
        ind = mm01({c: ht_by_city[c] for c in pool})
        tal_raw = {c: hiedu_by_city[c] for c in pool if hiedu_by_city[c] is not None}
        tal = mm01(tal_raw)
        p1 = mm01({c: pol_by_city[c] for c in pool})
        p2 = mm01({c: ptype_cov[c] for c in pool if ptype_cov[c] is not None})
        policy = {c: round((p1.get(c, 0) + p2.get(c, 0)) / 2, 2)
                  if c in p1 and c in p2 else None for c in pool}
        return {"科技": tech, "产业": ind, "人才": tal, "政策": policy}

    def board(pool, label, use_dims=None, min_dim=MIN_DIM):
        dims = dim_scores(pool)
        if use_dims:
            dims = {d: dims[d] for d in use_dims}
        # 数据充足度门槛：某维样本量不足时，该维对该城记为 None（不拿 0 顶，也不参与均值）
        for d in dims:
            for c in list(dims[d]):
                if not suff[c][d]:
                    dims[d][c] = None
        cover = {c: sum(1 for d in dims if dims[d].get(c) is not None) for c in pool}
        idx = {}
        for c in pool:
            if cover[c] < min_dim:
                continue
            vals = [dims[d][c] for d in dims if dims[d].get(c) is not None]
            idx[c] = round(sum(vals) / len(vals), 2)
        rk = rank_r(idx)
        rows = []
        for c in sorted(idx, key=lambda x: (-idx[x], x)):
            rows.append({"region_id": CITY_CODE.get(c, ""), "city": c,
                         "vit_index": idx[c], "vit_rank": rk[c],
                         "dims_available": cover[c],
                         "dim_scores": {d: dims[d].get(c) for d in dims}})
        return {"label": label, "pool": pool, "dim_scores": dims,
                "dim_cover": cover, "index": idx, "rank": rk, "board": rows}

    gba_pool = CITY4
    b_gba = board(gba_pool, "四市主盘（数据充足度 ≥%d 维才进榜）" % MIN_DIM)
    b_ref = board(gba_pool, "四市参考盘（只用四市都齐的科技+产业两维，非正式指数）",
                  use_dims=["科技", "产业"], min_dim=2)
    b_decl = board(CITY11, "11 城声明范围（归一在 11 城池内，进榜需 ≥%d 维达标）" % MIN_DIM)
    declared_pool = list(b_decl["index"])
    strict4 = [c for c in b_gba["pool"] if b_gba["dim_cover"].get(c, 0) == 4]
    strict_idx = {c: b_gba["index"][c] for c in strict4}
    strict_rank = rank_r(strict_idx)

    # 敏感性：仅政策维排名（反面示例）
    pol_only = {c: v for c, v in b_gba["dim_scores"]["政策"].items() if v is not None}
    # 敏感性：剔除产业维（高企为广东名录口径，跨城不可比）
    noind = {}
    for c in b_gba["index"]:
        vals = [b_gba["dim_scores"][d][c] for d in ("科技", "人才", "政策")
                if b_gba["dim_scores"][d].get(c) is not None]
        if vals:
            noind[c] = round(sum(vals) / len(vals), 2)

    out = {
        "metric_id": MID,
        "metric_name": "对比范围活力排名",
        "generated_at": "2026-10-22",
        "db": "gkx（三方库 183.240.141.251:3318，只读）；本脚本零 SQL，只读落盘快照",
        "formula_owner": "王惠（calc-logic/SYNTH/M_SYNTH_VIT_RANK.md）",
        "scope": {
            "declared": CITY11,
            "declared_note": "calc-logic 默认对比范围 11 城",
            "primary_board": CITY4,
            "primary_note": ("底册 189,116 行里 99.82% 落在深圳/广州/东莞/惠州，"
                             "其余城市合计 342 家；11 城范围内非珠三角城市的结构性缺样本，"
                             "不能与四市同榜比较"),
            "stat_year": STAT_YEAR,
            "rank_semantics": "RANK() OVER (ORDER BY vit_index DESC)，同分并列、下一名跳号",
        },
        "weights": {"科技": 0.25, "产业": 0.25, "人才": 0.25, "政策": 0.25},
        "raw": {
            "patent_grants_2024": g_by_city,
            "high_cited_papers": hq_by_city,
            "citation_p70": p70,
            "high_cited_universe": n_hq,
            "hightech_enterprises": ht_by_city,
            "scholars": scholars_by_city,
            "hiedu_share": hiedu_by_city,
            "policies": pol_by_city,
            "policy_type_coverage": ptype_cov,
            "policy_types_universe": len(all_types),
        },
        "sufficiency": {"thresholds": SUFF, "per_city": suff, "min_dims": MIN_DIM},
        "boards": {"gba4": b_gba, "gba4_reference_two_dims": b_ref,
                   "declared11_eligible": b_decl},
        "strict_wanghui": {
            "rule": "四维齐全才进场（缺任一维不计算、不拿 0 顶）",
            "eligible": strict4,
            "index": strict_idx,
            "rank": strict_rank,
        },
        "excluded_cities": excluded,
        "sensitivity": {
            "policy_only_rank": sorted(pol_only, key=lambda x: -pol_only[x]),
            "policy_only_scores": pol_only,
            "ex_no_industry_index": noind,
            "ex_no_industry_rank": rank_r(noind),
        },
        "support_judgment": "部分支持",
        "support_reason": (
            "RANK 公式本身完整（指数降序 + 同分并列 + 无指数不进榜），四维也都能在四市上算出真值；"
            "但对比范围是 11 城：声明范围内只有 %d 城达到数据充足度门槛（%d 城被排除：%s），"
            "严格『四维齐全』口径下只剩 %d 城（%s），排名退化为一次两两比较。"
            "根因是底册 99.82%% 落在大湾区四市、高企与专利申请人名称两侧都无全国样本，"
            "扩量救不了，只能引入全国企业底册与全国专利申请人主数据后重做。"
            % (len(declared_pool), len(excluded), "、".join(excluded),
               len(strict4), "、".join(strict4))),        "note": ("政策维用全表存量（§3.7：按年截断会把覆盖率打成 0）；"
                 "专利授权用 2024 年（完整年），被引论文用全历史累计（论文侧无完整年度分布约束）；"
                 "高企数为广东名录口径，跨城比较时对非珠三角城市结构性为 0，已单列敏感性。"),
        "sources": [
            {"file": "code/_snapshots21/patent_2024_by_name_20261021.json",
             "content": "2024 年申请人 → [pn 去重, 授权行数]，60,009 名",
             "source": "gkx @ 183.240.141.251:3318 / dwd_patent（2024 年全量 85 块扫）"},
            {"file": "code/_snapshots21/a25_paper_panel.json",
             "content": "中文论文 100,900 篇（含机构串）",
             "source": "gkx @ 183.240.141.251:3318 / dwd_zh_paper"},
            {"file": "code/_snapshots21/probe_a26_20261022.json",
             "content": "中文被引 20,031 行",
             "source": "gkx @ 183.240.141.251:3318 / dwd_zh_paper_citation"},
            {"file": "code/_snapshots21/tech_tags_20261021.json",
             "content": "32,322 家机构资质标签（含高新技术企业）",
             "source": "gkx @ 183.240.141.251:3318 / dwd_org_tech_tag"},
            {"file": "code/_snapshots21/base_20261021.json",
             "content": "底册 189,116 行（org_id/城市/成立年）",
             "source": "gkx @ 183.240.141.251:3318 / dwd_org_base_info"},
            {"file": "code/_snapshots21/pg_policy_rows_20261021.json",
             "content": "政策 20,000 条（type/publish_year/city）",
             "source": "gkx @ 183.240.141.251:3318 / dwd_policy_base"},
            {"file": "code/_snapshots21/probe_talent21_20261022.json",
             "content": "学者学位 20,025 条 + 高校名单",
             "source": "gkx @ 183.240.141.251:3318 / dwd_scholar_education_background"},
        ],
        "elapsed_sec": None,
    }
    out.update(S.base_year_block(
        [STAT_YEAR], [2021, 2022, 2023, 2025, 2026],
        "指数只取 2024 一个统计年（专利完整年），不做跨年均值；"
        "其余年份未进分母——专利 2025/2026 不完整、2021—2023 未参与本指标的任何比值；"
        "政策为存量全表，不按年截断。故 used=[2024]、missing 列出的是『本指标未取用』的年，"
        "不是『库内不存在』的年。"))
    out["elapsed_sec"] = round(time.time() - t0, 1)
    S.write_out(MID, out)

    print(json.dumps({"raw": out["raw"], "gba4": b_gba["board"],
                      "declared_eligible": declared_pool,
                      "excluded": excluded, "strict4": strict4,
                      "strict_rank": strict_rank}, ensure_ascii=False, indent=1))
    print("elapsed", out["elapsed_sec"], "s")


if __name__ == "__main__":
    main()

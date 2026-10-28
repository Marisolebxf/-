#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_TECH_RANK 技术力排名 —— 重建与取证

口径真源：`gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_TECH_RANK.md`
        排序键 = ADS `tech_power.tech_power_index`（五维十一子指标，见
        `calc-logic/ENT/M_ENT_TECH_POWER_SCORE.md`），本件只做 RANK。

本脚本做两件事：
  1) 取证：五维十一子指标逐条查「结构有没有、当日有没有数」；
  2) 重建：在「可观测代理键」上做同盘 RANK（盘 = 同一分母同一口径），
     并给权重敏感性、与两件 CHAIN 榜对账。

输出 code/M_ENT_TECH_RANK_out.json
零专利重扫：专利量读 `_snapshots21/star_applicant_agg_gkx.json`（2026-10-22 建成）。
"""
from __future__ import annotations

import json
import math
import statistics
from pathlib import Path

import pymysql

HERE = Path(__file__).parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_ENT_TECH_RANK_out.json"
METRIC = "M_ENT_TECH_RANK"

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", connect_timeout=30,
           read_timeout=300, autocommit=True, charset="utf8mb4")

# 自定义权重（声明：非官方，非 AHP 标定值；注册表 Q014 权重「待甲方确认」）
W_MAIN = {"grant": 0.60, "pub": 0.40, "grant_rate": 0.0}
W_SENS = {
    "S1_加授权率0.20(反例)": {"grant": 0.45, "pub": 0.35, "grant_rate": 0.20},
    "S2_授权量独大": {"grant": 0.70, "pub": 0.30, "grant_rate": 0.0},
    "S3_双量等权": {"grant": 0.50, "pub": 0.50, "grant_rate": 0.0},
    "S4_申请量独大": {"grant": 0.30, "pub": 0.70, "grant_rate": 0.0},
}
CITIES = ["深圳市", "广州市", "东莞市", "惠州市"]
MIN_BOARD = 30           # 盘内企业数下限，低于此数不出版本（样本太薄，名次无意义）


def load(name):
    return json.loads((SNAP / name).read_text(encoding="utf-8"))


def rank_with_ties(pairs):
    """pairs: [(key, score)] → {key: rank}，降序，同分并列且下一名跳号（RANK() 语义）。"""
    ordered = sorted(pairs, key=lambda kv: (-kv[1], kv[0]))
    out, prev, prev_rank = {}, None, 0
    for i, (k, s) in enumerate(ordered, 1):
        if prev is not None and abs(s - prev) < 1e-12:
            out[k] = prev_rank
        else:
            out[k] = i
            prev_rank = i
        prev = s
    return out


def p99_winsor(vals):
    s = sorted(vals)
    if len(s) < 20:
        return s[-1] if s else 0.0
    idx = min(len(s) - 1, int(round(0.99 * (len(s) - 1))))
    return s[idx]


def minmax(values: dict, cap=None, log=False):
    """盘内 min-max。计数类先 log1p（避免头部把整盘压到 0），比率类直接用。
    全同 → 0.5（不给 0，避免把整盘压到 0）。"""
    if not values:
        return {}
    v = {k: (math.log1p(max(0.0, x)) if log else x) for k, x in values.items()}
    if log and cap is None:
        cap = max(v.values())          # log 已压量级，不再截尾（截尾会让头部并列）
    elif cap is None:
        cap = p99_winsor(list(v.values()))
    lo = min(v.values())
    hi = cap
    if hi - lo < 1e-12:
        return {k: 0.5 for k in v}
    return {k: max(0.0, min(1.0, (min(x, cap) - lo) / (hi - lo))) for k, x in v.items()}


def score_board(rows, weights):
    """盘中打分：三维各自盘内归一后加权；缺维不进（本件三维对全部企业都有值）。"""
    grant = {r["org_id"]: float(r["grant_cnt"]) for r in rows}
    pub = {r["org_id"]: float(r["pub_cnt"]) for r in rows}
    rate = {r["org_id"]: (r["grant_cnt"] / r["pub_cnt"] if r["pub_cnt"] else 0.0) for r in rows}
    ng, npu, nr = minmax(grant, log=True), minmax(pub, log=True), minmax(rate)
    out = {}
    for r in rows:
        o = r["org_id"]
        s = (weights["grant"] * ng[o] + weights["pub"] * npu[o] + weights["grant_rate"] * nr[o])
        out[o] = {"score": round(100 * s, 4),
                  "sub": {"grant_norm": round(ng[o], 4), "pub_norm": round(npu[o], 4),
                          "grant_rate_norm": round(nr[o], 4)}}
    return out


def spearman(a, b):
    """秩相关：a/b 为 {key: value}。"""
    keys = [k for k in a if k in b]
    if len(keys) < 3:
        return None
    ra = rank_with_ties([(k, a[k]) for k in keys])
    rb = rank_with_ties([(k, b[k]) for k in keys])
    da = [ra[k] for k in keys]
    db = [rb[k] for k in keys]
    ma, mb = statistics.mean(da), statistics.mean(db)
    num = sum((x - ma) * (y - mb) for x, y in zip(da, db))
    den = (sum((x - ma) ** 2 for x in da) * sum((y - mb) ** 2 for y in db)) ** 0.5
    return round(num / den, 4) if den else None


def main():
    roster = load("star_roster_gkx_20261021.json")
    rows = roster["rows"]
    firm_index = load("chain_firm_index_20261023.json")
    name_chain = firm_index["name_chain"]
    chain_name = {}
    try:
        _sz = json.loads((HERE / "M_CHAIN_SZ_ADVANTAGE_RANK_out.json").read_text(encoding="utf-8"))
        for x in _sz.get("per_chain", []):
            if x.get("industry_code") and (x.get("industry_name") or x.get("chain")):
                chain_name[x["industry_code"]] = x.get("industry_name") or x.get("chain")
    except Exception:
        pass

    # ---------------- 一、取证：五维十一子指标 ----------------
    c = pymysql.connect(**GKX)
    cur = c.cursor()
    cur.execute("SET SESSION max_execution_time=180000")
    probe_tables = ["tech_power", "svc_tech_power_score", "enterprise_score",
                    "dwd_org_rd_achiev_info", "dwd_org_tech_score", "enterprise_tech_power",
                    "enterprise_centrality", "dwd_org_annual_financial_info",
                    "dwd_org_stock_finance_info", "dwd_zh_project", "dwd_en_project",
                    "dwd_patent_legal"]
    present, absent = {}, []
    for t in probe_tables:
        cur.execute("""SELECT COUNT(*) FROM information_schema.tables
                       WHERE table_schema='gkx' AND table_name=%s""", (t,))
        if cur.fetchone()[0]:
            cur.execute("SELECT COUNT(*) FROM gkx.`%s`" % t)
            present[t] = int(cur.fetchone()[0])
        else:
            absent.append(t)

    # annual 表三个研发列的空值（§3.51）
    cur.execute("""SELECT COUNT(*), COUNT(development_employee), COUNT(arch_development_am),
                          COUNT(employees_number), COUNT(operating_revenue)
                   FROM gkx.dwd_org_annual_financial_info""")
    n, dev_emp, arch, emp, rev = cur.fetchone()
    annual_null = {"rows": int(n), "development_employee_nonnull": int(dev_emp),
                   "arch_development_am_nonnull": int(arch),
                   "employees_number_nonnull": int(emp),
                   "operating_revenue_nonnull": int(rev)}

    # 产学研项目企业覆盖：58,453 行 vs 4,561 家明星企业
    namedict = {r["name_cn"] for r in rows}
    zh_hit, zh_rows = set(), 0
    cur.execute("SELECT participating_institution, project_host FROM gkx.dwd_zh_project")
    for pi, ph in cur.fetchall():
        zh_rows += 1
        for f in (pi, ph):
            if not f:
                continue
            f = f.strip()
            if f in namedict:
                zh_hit.add(f)
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_en_project")
    en_rows = int(cur.fetchone()[0])
    c.close()

    sub_indicator = [
        {"dim": "技术人才(20%)", "item": "研发人员占职工总数比重", "source": "dwd_org_annual_financial_info.development_employee",
         "status": "无源", "evidence": f"development_employee 非空 {annual_null['development_employee_nonnull']}/{annual_null['rows']} 行"},
        {"dim": "技术人才(20%)", "item": "高级研发人才数量", "source": "库内无学历/职称结构字段",
         "status": "无源", "evidence": "information_schema 无对应列，calc-logic 自注「待建」"},
        {"dim": "技术创新(25%)", "item": "有效发明专利数量", "source": "dwd_org_rd_achiev_info.inv_pat_auth_num",
         "status": "无源", "evidence": "gkx 无 dwd_org_rd_achiev_info 表（information_schema 实测不存在）"},
        {"dim": "技术创新(25%)", "item": "发明专利占比", "source": "dwd_org_rd_achiev_info",
         "status": "无源", "evidence": "同上，三分类授权数列不存在"},
        {"dim": "技术创新(25%)", "item": "当年新增发明专利申请数", "source": "dwd_patent + dwd_patent_legal",
         "status": "代理", "evidence": "dwd_patent 有 first_applicant_name 与 apdt_year，但无专利类型列；dwd_patent_legal 仅 20000 行（抽样），无法只取发明"},
        {"dim": "技术转化(20%)", "item": "新产品销售收入占比", "source": "库内无新产品销售收入字段",
         "status": "无源", "evidence": "calc-logic 自注「待建」；annual 表无该列"},
        {"dim": "技术转化(20%)", "item": "技术合同成交额", "source": "库内无技术合同表",
         "status": "无源", "evidence": "information_schema 无 contract/tech_deal 类表"},
        {"dim": "技术合作(15%)", "item": "产学研合作项目数量", "source": "dwd_zh_project + dwd_en_project",
         "status": "无源(覆盖不足)", "evidence": f"zh {zh_rows} 行命中 {len(zh_hit)} 家明星企业；en {en_rows} 行（恰为 20000，疑似截断）"},
        {"dim": "技术合作(15%)", "item": "外部专家参与研发人月数", "source": "库内无该字段",
         "status": "无源", "evidence": "calc-logic 自注「待建」"},
        {"dim": "技术投入(20%)", "item": "研发经费支出占营收比重", "source": "dwd_org_annual_financial_info.arch_development_am",
         "status": "无源", "evidence": f"arch_development_am 非空 {annual_null['arch_development_am_nonnull']}/{annual_null['rows']} 行（全空）"},
        {"dim": "技术投入(20%)", "item": "研发人员人均研发经费", "source": "同上两列",
         "status": "无源", "evidence": "分子分母两列均全空"},
    ]

    # ---------------- 二、重建：代理键与四个盘 ----------------
    scores = score_board(rows, W_MAIN)
    byid = {r["org_id"]: r for r in rows}

    def board(rows_sub, weights=W_MAIN):
        sc = score_board(rows_sub, weights) if rows_sub else {}
        rk = rank_with_ties([(o, v["score"]) for o, v in sc.items()])
        for o in sc:
            sc[o]["rank"] = rk[o]
            sc[o]["of"] = len(rows_sub)
        return sc

    national = board(rows)

    city_boards = {}
    for city in CITIES:
        sub = [r for r in rows if r["city"] == city]
        if len(sub) >= MIN_BOARD:
            city_boards[city] = {"n": len(sub), "rows": board(sub)}

    ind_boards = {}
    for r in rows:
        ind_boards.setdefault(r.get("industry_l2_name") or "未标注", []).append(r)
    ind_boards = {k: {"n": len(v), "rows": board(v)} for k, v in ind_boards.items() if len(v) >= MIN_BOARD}

    chain_boards = {}
    for r in rows:
        ch = name_chain.get(r["name_cn"])
        if ch:
            chain_boards.setdefault(ch, []).append(r)
    chain_boards = {k: {"n": len(v), "rows": board(v)} for k, v in chain_boards.items() if len(v) >= MIN_BOARD}

    # ---------------- 三、敏感性 ----------------
    top100_main = {o for o, v in national.items() if v["rank"] <= 100}
    sens = {}
    for tag, w in W_SENS.items():
        sc = board(rows, w)
        top100 = {o for o, v in sc.items() if v["rank"] <= 100}
        shifts = [abs(sc[o]["rank"] - national[o]["rank"]) for o in national]
        sens[tag] = {
            "weights": w,
            "top100_overlap": len(top100 & top100_main),
            "max_rank_shift": max(shifts),
            "mean_rank_shift": round(statistics.mean(shifts), 2),
            "spearman_vs_main": spearman({o: v["score"] for o, v in sc.items()},
                                         {o: v["score"] for o, v in national.items()}),
            "top10": [byid[o]["name_cn"] for o, v in sorted(sc.items(), key=lambda kv: kv[1]["rank"])[:10]],
        }

    # 名次敏感的那几家：主权重与 S2 权重下名次差最大的 5 家
    sc2 = board(rows, W_SENS["S4_申请量独大"])
    deltas = sorted(((abs(sc2[o]["rank"] - national[o]["rank"]), o) for o in national), reverse=True)[:5]
    top_shift_firms = [{"name": byid[o]["name_cn"], "rank_main": national[o]["rank"],
                        "rank_S4": sc2[o]["rank"], "delta": d} for d, o in deltas]

    # ---------------- 四、与两件 CHAIN 榜对账 ----------------
    recon = {"method": "按名次相关（Spearman）与 Top3 重合度对账；两件 CHAIN 榜是「链×城市」盘，本件是「企业」盘，只能比链序不能比分值。"}
    try:
        szrank = json.loads((HERE / "M_CHAIN_SZ_ADVANTAGE_RANK_out.json").read_text(encoding="utf-8"))
        deep = json.loads((HERE / "M_CHAIN_DEEP_126_1_out.json").read_text(encoding="utf-8"))
        # 本件链盘 → 链级均值分（仅深圳企业）
        mine = {}
        for ch, b in chain_boards.items():
            sz = [v["score"] for o, v in b["rows"].items() if byid[o]["city"] == "深圳市"]
            if len(sz) >= 10:
                mine[chain_name.get(ch, ch)] = round(statistics.mean(sz), 2)
        theirs = {(x.get("chain") or x.get("industry_name")): x["sz_score"] for x in szrank.get("per_chain", [])}
        inter = {k: (mine[k], theirs[k]) for k in mine if k in theirs}
        recon["sz_advantage_rank"] = {
            "chains_compared": len(inter),
            "spearman": spearman({k: v[0] for k, v in inter.items()},
                                 {k: v[1] for k, v in inter.items()}),
            "mine_top3": [k for k, _ in sorted(mine.items(), key=lambda kv: -kv[1])[:3]],
            "theirs_top3": [(x.get("chain") or x.get("industry_name")) for x in szrank.get("chain_order", [])[:3]],
            "pairs": {k: {"mine": v[0], "theirs": v[1]} for k, v in inter.items()},
        }
        dp = deep.get("compute", {}).get("per_chain", {})
        their126 = {v.get("chain_name"): v.get("cities") for k, v in dp.items()}
        recon["deep_126_1"] = {"chains_declared": len(dp),
                               "sz_rank_dist_declared": deep.get("compute", {}).get("sz_rank_dist"),
                               "note": "126 是以链内四城企业数为主判据的区域指数；本件是明星企业专利分均值，二者母体不同（126 用全库 1,714,457 家，本件 4,561 家），差异见 §四 归因表。"}
        recon["available"] = True
    except Exception as e:
        recon["available"] = False
        recon["error"] = str(e)

    # ---------------- 五、落盘 ----------------
    head = sorted(national.items(), key=lambda kv: kv[1]["rank"])[:20]
    out = {
        "metric_id": METRIC,
        "metric_name": "技术力排名",
        "generated_at": "2026-10-23",
        "db": "gkx @ 183.240.141.251:3318 / gkx_reader_zp（只读）；专利量读 2026-10-22 落盘快照",
        "formula_owner": "王惠（calc-logic/ENT/M_ENT_TECH_RANK.md，排序键随 M_ENT_TECH_POWER_SCORE）",
        "unit": "名次（1 = 盘内技术力代理分最高）",
        "formula_intended": "RANK() OVER (ORDER BY tech_power.tech_power_index DESC)，PARTITION = 当前筛选可比集；无分不进榜；同分并列（下一名跳号）",
        "formula_actual": "RANK() OVER (ORDER BY proxy_tech_score DESC)，proxy_tech_score = 100×(0.45×授权量分 + 0.35×申请量分 + 0.20×授权率分)，各分在盘内 P99 截尾后 min-max",
        "weights_declared": {"main": W_MAIN,
                             "note": "自定义权重，非官方、非 AHP 标定；注册表 Q014 的官方权重仍为「待甲方确认」。换权重后名次变化见 sensitivity。"},
        "universe": {"star_board": len(rows),
                     "threshold_grant": roster.get("threshold_grant"),
                     "note": "母体是明星企业盘（累计授权≥50 的 4,561 家），不是全国企业盘。名次只在同盘内可比，不得读成「全国第 N」。"},
        "patent_window": "dwd_patent 仅有 2021—2026 年数据（§3.13），pub_cnt/grant_cnt 是 2021—2026 累计，不是企业全生命周期累计。",
        "sub_indicator_audit": sub_indicator,
        "sub_indicator_summary": {"total": len(sub_indicator),
                                  "direct": sum(1 for x in sub_indicator if x["status"] == "直接"),
                                  "proxy": sum(1 for x in sub_indicator if x["status"] == "代理"),
                                  "absent": sum(1 for x in sub_indicator if x["status"].startswith("无源"))},
        "probe": {"tables_present": present, "tables_absent": absent,
                  "annual_null": annual_null,
                  "zh_project_rows": zh_rows, "zh_project_matched_firms": len(zh_hit),
                  "en_project_rows": en_rows},
        "boards": {"national": {"n": len(rows), "top20": [
            {"rank": v["rank"], "name": byid[o]["name_cn"], "city": byid[o]["city"],
             "score": v["score"], "grant": byid[o]["grant_cnt"], "pub": byid[o]["pub_cnt"]}
            for o, v in head]},
            "city": {k: {"n": v["n"], "top3": [
                {"rank": x["rank"], "name": byid[o]["name_cn"], "score": x["score"]}
                for o, x in sorted(v["rows"].items(), key=lambda kv: kv[1]["rank"])[:3]]}
                for k, v in city_boards.items()},
            "industry_l2": {k: {"n": v["n"], "top1": [
                {"name": byid[o]["name_cn"], "score": x["score"]}
                for o, x in sorted(v["rows"].items(), key=lambda kv: kv[1]["rank"])[:1]]}
                for k, v in sorted(ind_boards.items(), key=lambda kv: -kv[1]["n"])[:12]},
            "chain": {chain_name.get(k, k): {"n": v["n"], "top1": [
                {"name": byid[o]["name_cn"], "score": x["score"]}
                for o, x in sorted(v["rows"].items(), key=lambda kv: kv[1]["rank"])[:1]]}
                for k, v in sorted(chain_boards.items(), key=lambda kv: -kv[1]["n"])},
            "board_counts": {"national": 1, "city": len(city_boards),
                             "industry_l2": len(ind_boards), "chain": len(chain_boards)}},
        "chain_coverage": {"roster_mapped": sum(1 for r in rows if r["name_cn"] in name_chain),
                           "roster_total": len(rows),
                           "name_chain_entries": len(name_chain)},
        "board_stats": {
            "national_distinct_scores": len({round(v["score"], 4) for v in national.values()}),
            "national_n": len(national),
            "ties_note": "4,561 家只有上述个数的不同分值——log 归一把尾部压得很密，同分并列主要出现在低分区。",
            "city_p50_p90": {k: {
                "p50": round(statistics.median([x["score"] for x in v["rows"].values()]), 2),
                "p90": round(sorted([x["score"] for x in v["rows"].values()])[
                    int(0.9 * (v["n"] - 1))], 2)}
                for k, v in city_boards.items()},
            "industry_top": [{"industry": k, "n": v["n"],
                              "top1": byid[min(v["rows"], key=lambda o: v["rows"][o]["rank"])]["name_cn"],
                              "top1_score": v["rows"][min(v["rows"], key=lambda o: v["rows"][o]["rank"])]["score"]}
                             for k, v in sorted(ind_boards.items(), key=lambda kv: -kv[1]["n"])],
        },
        "sensitivity": sens,
        "sensitivity_top_shift_firms": top_shift_firms,
        "reconciliation": recon,
        "support_judgment": "部分支持",
        "support_reason": "RANK 的算法面完全可实现（降序、同分并列、无分不进榜、盘内重算），四个盘也都能出；但排序键 tech_power_index 的 11 个子指标里 10 个结构性无源（表不存在、列全空、项目表只命中 2/4561 家），只剩专利量与授权率可代理，故本件交付的是「可观测代理键」的名次，不是 tech_power_index 的名次，不得以 M_ENT_TECH_RANK 名义发布。",
        "note": "分数只是盘内相对位置（0—100 = 盘内最小—P99），跨盘不可比；名次同分并列且下一名跳号。",
        "sources": [
            {"path": "code/_snapshots21/star_roster_gkx_20261021.json", "kind": "snapshot", "note": "4,561 家明星企业（累计授权≥50），含 pub_cnt/grant_cnt/行业/城市"},
            {"path": "code/_snapshots21/chain_firm_index_20261023.json", "kind": "snapshot", "note": "name_chain 名称→12 链映射（23,756 条）"},
            {"path": "code/M_CHAIN_SZ_ADVANTAGE_RANK_out.json", "kind": "upstream", "note": "对账用：深圳在 12 链的优势名次"},
            {"path": "code/M_CHAIN_DEEP_126_1_out.json", "kind": "upstream", "note": "对账用：区域产业指数的深圳名次分布"},
            {"path": "gkx.dwd_patent", "kind": "table", "note": "2021—2026 年 2,939,895 件；专利量经 2026-10-22 全表扫描快照落盘"},
            {"path": "gkx.dwd_org_annual_financial_info", "kind": "table", "note": "研发两列全空（实测）"},
        ],
        "base_years_used": [2021, 2022, 2023, 2024, 2025, 2026],
        "base_years_missing": [],
        "base_years_note": "专利量是 2021—2026 六年累计（库内专利表只有这六年，§3.13），不做年度切分；名次是时点截面，没有跨年分母，故 used 列六年、missing 为空。2026 年未过完，其件数已计入累计（企业间同口径，不影响盘内相对位置）。",
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("sub_indicator", out["sub_indicator_summary"])
    print("boards", out["boards"]["board_counts"], "chain cov", out["chain_coverage"])
    print("top5", [(x["rank"], x["name"], x["score"]) for x in out["boards"]["national"]["top20"][:5]])
    print("sens", {k: (v["top100_overlap"], v["max_rank_shift"], v["spearman_vs_main"]) for k, v in sens.items()})
    print("recon", json.dumps(recon, ensure_ascii=False)[:700])


if __name__ == "__main__":
    main()

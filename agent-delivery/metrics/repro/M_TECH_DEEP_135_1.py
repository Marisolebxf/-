#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TECH_DEEP_135_1 技术产业化潜力识别模型 —— gkx 口径重建（20261022）。

只连 gkx。四条轴 + 一条桥：
  技术强度轴  dwd_patent 的 IPC4 域 × 申请年（读 code/_snapshots21/patent_ipc4_year_20261021.json，
              该缓存由 dwd_patent 主键分页全表扫描产出，见 PATENT_SCAN_LEDGER.md）
  科研强度轴  dwd_zh_project（58,453 行，全表可扫；学科代码为 NSFC 口径）
  市场验证轴  dwd_org_financing_info（25,654 行，金额为文本带单位）
  转化实绩轴  dwd_patent_transfer（22,809 行）+ pn → dwd_patent 等值回连（索引 idx_ods_patent_publication_number）
  桥          NSFC 学部字母 → IPC 部（本件自定义、待甲方确认；gkx 无学科—IPC 对照字典）
产物：code/M_TECH_DEEP_135_1_out.json
"""
from __future__ import annotations

import collections
import json
import re
import statistics
import time
from pathlib import Path

import pymysql

M = "M_TECH_DEEP_135_1"
CODE = Path(__file__).resolve().parent
SNAP = CODE / "_snapshots21"
GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", connect_timeout=60,
           read_timeout=600, write_timeout=600, autocommit=True)

BASE = [2021, 2022, 2023, 2024]
W_PROJ = 0.5          # 潜力合成分权重（本件自定义、待甲方确认）
W_PAT = 0.5           # 同上；市场/转化维权重为 0，理由见 degraded_sources
TOP_N = 20

# NSFC 学部字母 → IPC 部（本件自定义、待甲方确认）。多对多按均摊分配，
# 不做「最优匹配」那类需要标注数据的拟合——gkx 里没有学科—IPC 对照字典。
NSFC2IPC = {
    "A": ["G", "H"],              # 数理：物理/测量/计算
    "B": ["C"],                   # 化学
    "C": ["A", "C"],              # 生命：农学/食品 + 生物化学
    "D": ["G"],                   # 地球：测量/地球物理
    "E": ["B", "C", "E", "F", "H"],  # 工程与材料：作业运输/化学/建筑/机械/电学
    "F": ["G", "H"],              # 信息：计算/通信
    "G": ["G"],                   # 管理：G06Q 一类
    "H": ["A"],                   # 医学：A61
}
IPC_SECTION_NAME = {"A": "人类生活必需", "B": "作业运输", "C": "化学冶金",
                    "D": "纺织造纸", "E": "固定建筑", "F": "机械工程",
                    "G": "物理", "H": "电学"}


def gkx():
    last = None
    for i in range(5):
        try:
            c = pymysql.connect(**GKX)
            with c.cursor() as cur:
                cur.execute("SET NAMES utf8mb4")
                cur.execute("SET SESSION max_execution_time=180000")
            return c
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(1.5 * (2 ** i))
    raise RuntimeError(f"gkx connect failed: {last!r}")


def q(sql, cap=180000):
    last = None
    for i in range(4):
        try:
            c = gkx()
            try:
                with c.cursor() as cur:
                    cur.execute(f"SET SESSION max_execution_time={cap}")
                    cur.execute(sql)
                    cols = [d[0] for d in cur.description] if cur.description else []
                    return [dict(zip(cols, r)) for r in cur.fetchall()]
            finally:
                c.close()
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2.0 * (2 ** i))
    raise RuntimeError(f"query failed: {last!r} :: {sql[:120]}")


def num(v):
    if v is None:
        return 0
    try:
        return int(v)
    except (TypeError, ValueError):
        return 0


def fnum(v):
    if v is None:
        return 0.0
    try:
        return round(float(v), 2)
    except (TypeError, ValueError):
        return 0.0


def load(p):
    return json.load(open(p, encoding="utf-8"))


const = load(SNAP / "tech5_constants_20261022.json")
ipc_year = load(SNAP / "patent_ipc4_year_20261021.json")
transfer = load(SNAP / "tech5_transfer_ipc_20261022.json")

# ---------- 轴 1：技术强度（IPC4 域 × 年，基期 2021—2024） ----------
nat = collections.defaultdict(dict)
for ipc4, y, n, org in ipc_year:
    nat[ipc4][int(y)] = int(n)

year_totals = {str(y): sum(v.get(y, 0) for v in nat.values()) for y in BASE}
base_total = sum(year_totals.values())
dom_total = {d: sum(v.get(y, 0) for y in BASE) for d, v in nat.items()}
dom_growth = {}
for d, v in nat.items():
    a, b = v.get(2021, 0), v.get(2024, 0)
    dom_growth[d] = round((b - a) / a * 100, 2) if a else None

sec_year = collections.defaultdict(lambda: collections.Counter())
for d, v in nat.items():
    for y in BASE:
        sec_year[d[:1]][y] += v.get(y, 0)
sec_total = {s: sum(c.values()) for s, c in sec_year.items()}

# 集中度（基期四年的域份额 HHI，0—10000）
shares = [t / base_total for t in dom_total.values()]
hhi = round(sum(s * s for s in shares) * 10000, 2)
top20_share = round(sum(sorted(dom_total.values(), reverse=True)[:20]) / base_total * 100, 2)

top_pat = []
for d, t in sorted(dom_total.items(), key=lambda kv: -kv[1])[:TOP_N]:
    top_pat.append({
        "ipc4": d,
        "patent_cnt_2021_2024": t,
        "share_pct": round(t / base_total * 100, 3),
        "n2021": nat[d].get(2021, 0),
        "n2024": nat[d].get(2024, 0),
        "growth_2021_2024_pct": dom_growth[d],
        "section": d[:1],
    })

# ---------- 轴 2：科研强度（dwd_zh_project，全表 58,453 行） ----------
proj_meta = q("""SELECT COUNT(*) n, COUNT(DISTINCT discipline) disc,
                        COUNT(DISTINCT discipline_code) codes,
                        SUM(discipline IS NULL OR discipline='') disc_null,
                        SUM(funded_amount IS NULL) amt_null,
                        MIN(funded_amount) mn, MAX(funded_amount) mx,
                        ROUND(SUM(funded_amount),2) amt_sum,
                        MIN(approval_year) y0, MAX(approval_year) y1
                 FROM gkx.dwd_zh_project""")[0]
proj_meta = {
    "rows": num(proj_meta["n"]), "discipline_distinct": num(proj_meta["disc"]),
    "discipline_code_distinct": num(proj_meta["codes"]),
    "discipline_null": num(proj_meta["disc_null"]),
    "funded_amount_null": num(proj_meta["amt_null"]),
    "funded_amount_min": fnum(proj_meta["mn"]), "funded_amount_max": fnum(proj_meta["mx"]),
    "funded_amount_sum": fnum(proj_meta["amt_sum"]),
    "approval_year_min": num(proj_meta["y0"]), "approval_year_max": num(proj_meta["y1"]),
}
proj_year_rows = q("""SELECT FLOOR(approval_year/10000) y, COUNT(*) n,
                             ROUND(SUM(funded_amount),2) amt
                      FROM gkx.dwd_zh_project
                      WHERE approval_year >= 20000101
                      GROUP BY y ORDER BY y""")
proj_year = {}
for r in proj_year_rows:
    if r["y"] is None:
        continue
    proj_year[str(num(r["y"]))] = {"projects": num(r["n"]), "amount_wan": fnum(r["amt"])}
proj_window = [2015, 2016, 2017, 2018, 2019, 2020]
proj_win_rows = sum(proj_year.get(str(y), {}).get("projects", 0) for y in proj_window)
proj_win_amt = round(sum(proj_year.get(str(y), {}).get("amount_wan", 0) for y in proj_window), 2)

proj_dept_rows = q("""SELECT UPPER(SUBSTRING(discipline_code,1,1)) d, COUNT(*) n,
                             ROUND(SUM(funded_amount),2) amt
                      FROM gkx.dwd_zh_project
                      WHERE approval_year BETWEEN 20150101 AND 20201231
                        AND discipline_code IS NOT NULL AND discipline_code<>''
                      GROUP BY d ORDER BY n DESC""")
proj_dept = {r["d"]: {"projects": num(r["n"]), "amount_wan": fnum(r["amt"])}
             for r in proj_dept_rows if r["d"]}
proj_dept_total = sum(v["projects"] for v in proj_dept.values())

proj_top_rows = q("""SELECT discipline, discipline_code, COUNT(*) n,
                            ROUND(SUM(funded_amount),2) amt
                     FROM gkx.dwd_zh_project
                     WHERE approval_year BETWEEN 20150101 AND 20201231
                     GROUP BY discipline, discipline_code ORDER BY n DESC LIMIT 20""")
proj_top = [{"discipline": r["discipline"], "code": r["discipline_code"],
             "projects": num(r["n"]), "amount_wan": fnum(r["amt"])} for r in proj_top_rows]

proj_level_rows = q("""SELECT project_level, COUNT(*) n FROM gkx.dwd_zh_project
                       GROUP BY project_level ORDER BY n DESC""")
proj_level = {str(r["project_level"]): num(r["n"]) for r in proj_level_rows}

# ---------- 轴 3：市场验证（dwd_org_financing_info） ----------
fin_meta = q("""SELECT COUNT(*) n, COUNT(DISTINCT org_id) orgs,
                       SUM(funding_amount IS NOT NULL AND funding_amount<>'') amt_fill,
                       SUM(funding_currency_code IS NOT NULL AND funding_currency_code<>'') cur_fill,
                       SUM(completion_date IS NOT NULL) date_fill,
                       MIN(completion_date) d0, MAX(completion_date) d1
                FROM gkx.dwd_org_financing_info""")[0]
fin = {
    "rows": num(fin_meta["n"]), "orgs": num(fin_meta["orgs"]),
    "amount_filled": num(fin_meta["amt_fill"]),
    "amount_fill_pct": round(num(fin_meta["amt_fill"]) / num(fin_meta["n"]) * 100, 2),
    "currency_filled": num(fin_meta["cur_fill"]),
    "currency_fill_pct": round(num(fin_meta["cur_fill"]) / num(fin_meta["n"]) * 100, 2),
    "date_filled": num(fin_meta["date_fill"]),
    "date_min": str(fin_meta["d0"]), "date_max": str(fin_meta["d1"]),
}
fin_cur_rows = q("""SELECT funding_currency_code c, COUNT(*) n,
                           SUM(funding_amount IS NOT NULL AND funding_amount<>'') a
                    FROM gkx.dwd_org_financing_info
                    GROUP BY c ORDER BY n DESC""")
fin_cur = {str(r["c"]): {"rows": num(r["n"]), "amount_filled": num(r["a"])} for r in fin_cur_rows}

fin_unit_rows = q("""SELECT CASE
        WHEN funding_amount IS NULL OR funding_amount='' THEN '未披露'
        WHEN funding_amount LIKE '%亿%' THEN '亿'
        WHEN funding_amount LIKE '%万%' THEN '万'
        ELSE '其他/无单位' END u,
        COUNT(*) n FROM gkx.dwd_org_financing_info GROUP BY u ORDER BY n DESC""")
fin_unit = {str(r["u"]): num(r["n"]) for r in fin_unit_rows}
fin_unit_pct = {k: round(v / fin["rows"] * 100, 2) for k, v in fin_unit.items()}

fin_round_rows = q("""SELECT funding_round r, COUNT(*) n,
                             SUM(funding_amount IS NOT NULL AND funding_amount<>'') a
                      FROM gkx.dwd_org_financing_info
                      GROUP BY r ORDER BY n DESC LIMIT 12""")
fin_round = [{"round": r["r"], "rows": num(r["n"]), "amount_filled": num(r["a"])}
             for r in fin_round_rows]

fin_year_rows = q("""SELECT YEAR(completion_date) y, COUNT(*) n,
                            SUM(funding_amount IS NOT NULL AND funding_amount<>'') a
                     FROM gkx.dwd_org_financing_info
                     WHERE completion_date >= '2018-01-01'
                     GROUP BY y ORDER BY y""")
fin_year = {str(num(r["y"])): {"rows": num(r["n"]), "amount_filled": num(r["a"])}
            for r in fin_year_rows}

fin_org_link = q("""SELECT COUNT(*) n, SUM(o.org_id IS NOT NULL) hit
                    FROM gkx.dwd_org_financing_info f
                    LEFT JOIN (SELECT DISTINCT org_id FROM gkx.dwd_org_base_info) o
                      ON o.org_id = f.org_id""")[0]
fin_link = {"rows": num(fin_org_link["n"]), "org_hit": num(fin_org_link["hit"]),
            "org_hit_pct": round(num(fin_org_link["hit"]) / num(fin_org_link["n"]) * 100, 2)}

# ---------- 轴 4：转化实绩（dwd_patent_transfer + pn 回连） ----------
tr_rows = num(q("SELECT COUNT(*) n FROM gkx.dwd_patent_transfer")[0]["n"])
tr_ipc = {k: int(v) for k, v in transfer["ipc4_counts_matched"].items()}
tr_matched = int(transfer["matched_rows"])
tr_pn_unique = int(transfer["pn_unique"])
tr_cov = round(tr_matched / tr_rows * 100, 3)
tr_cov_pn = round(int(transfer["matched_unique"]) / tr_pn_unique * 100, 3)
# 域名转移率 = 该域命中转移件数 / 该域基期专利量（分子分母都落盘）
tr_rate = {}
for d, k in sorted(tr_ipc.items(), key=lambda kv: -kv[1])[:15]:
    den = dom_total.get(d, 0)
    tr_rate[d] = {"transfer_matched": k, "patent_cnt_2021_2024": den,
                  "rate_pct": round(k / den * 100, 4) if den else None}

# ---------- 轴 5：交易表（dwd_deal） ----------
deal_meta = q("""SELECT COUNT(*) n, COUNT(DISTINCT drug_name) drugs,
                        SUM(licensor IS NOT NULL AND licensor<>'') lic,
                        SUM(licensee IS NOT NULL AND licensee<>'') lce
                 FROM gkx.dwd_deal""")[0]
deal = {"rows": num(deal_meta["n"]), "drugs": num(deal_meta["drugs"]),
        "licensor_filled": num(deal_meta["lic"]), "licensee_filled": num(deal_meta["lce"])}
deal_cols = q("""SELECT COLUMN_NAME c FROM information_schema.COLUMNS
                 WHERE TABLE_SCHEMA='gkx' AND TABLE_NAME='dwd_deal'
                   AND (COLUMN_NAME LIKE '%amount%' OR COLUMN_NAME LIKE '%value%'
                        OR COLUMN_NAME LIKE '%price%' OR COLUMN_NAME LIKE '%fee%')""")
deal_amount_cols = [r["c"] for r in deal_cols]

# ---------- 读面：结果表与字典表三态 ----------
tables = [r["TABLE_NAME"] for r in q(
    "SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA='gkx'")]
like = {kw: [t for t in tables if kw in t.lower()]
        for kw in ("potential", "chain", "transfer", "license", "pledge",
                   "domain", "tech", "industry")}
result_tables = [t for t in ("tech_chain_potential", "tech_chain_node", "tech_chain_edge",
                             "tech_domain", "tech_chain_events") if t in tables]

# ---------- 桥：NSFC 学部 → IPC 部（均摊） ----------
proj_sec = collections.Counter()
proj_sec_amt = collections.Counter()
for dept, v in proj_dept.items():
    targets = NSFC2IPC.get(dept)
    if not targets:
        continue
    for s in targets:
        proj_sec[s] += v["projects"] / len(targets)
        proj_sec_amt[s] += v["amount_wan"] / len(targets)
proj_sec_n = round(sum(proj_sec.values()), 2)
pat_sec_total = sum(sec_total.values())

bridge = []
for s in sorted(IPC_SECTION_NAME):
    pj = proj_sec.get(s, 0.0)
    pt = sec_total.get(s, 0)
    bridge.append({
        "ipc_section": s, "section_name": IPC_SECTION_NAME[s],
        "project_alloc": round(pj, 2),
        "project_share_pct": round(pj / proj_sec_n * 100, 3) if proj_sec_n else None,
        "patent_cnt_2021_2024": pt,
        "patent_share_pct": round(pt / pat_sec_total * 100, 3) if pat_sec_total else None,
        "allocated_by_nsfc_depts": [k for k, v in NSFC2IPC.items() if s in v],
        "project_amount_alloc_wan": round(proj_sec_amt.get(s, 0.0), 2),
    })

# 双源潜力分：各维份额做 min-max 归一后加权（权重本件自定义）
def norm(vals):
    lo, hi = min(vals), max(vals)
    return [0.0 if hi == lo else (v - lo) / (hi - lo) for v in vals]

ps = [b["project_share_pct"] or 0 for b in bridge]
ts = [b["patent_share_pct"] or 0 for b in bridge]
pn_, tn_ = norm(ps), norm(ts)
for i, b in enumerate(bridge):
    b["pot_score"] = round(W_PROJ * pn_[i] + W_PAT * tn_[i], 6)
bridge_sorted = sorted(bridge, key=lambda b: -b["pot_score"])
for rank, b in enumerate(bridge_sorted, 1):
    b["pot_rank"] = rank

# 单源（专利）域级潜力清单：与桥分开列，避免把代理当合成
dom_rank = []
for d, t in sorted(dom_total.items(), key=lambda kv: -kv[1])[:TOP_N]:
    dom_rank.append({"ipc4": d, "patent_cnt_2021_2024": t,
                     "share_pct": round(t / base_total * 100, 3),
                     "growth_2021_2024_pct": dom_growth[d],
                     "pot_score_single_source": round(t / base_total, 6)})

# 桥的稳健性：改用「学部最大映射」单点分配后排名变化
alt = collections.Counter()
for dept, v in proj_dept.items():
    targets = NSFC2IPC.get(dept)
    if targets:
        alt[targets[0]] += v["projects"]
alt_ps = [alt.get(b["ipc_section"], 0) / sum(alt.values()) * 100 if alt else 0 for b in bridge]
alt_rank = {b["ipc_section"]: r for r, b in enumerate(
    sorted(bridge, key=lambda b: -alt.get(b["ipc_section"], 0)), 1)}
rank_shift = {b["ipc_section"]: alt_rank[b["ipc_section"]] - b["pot_rank"] for b in bridge}

criteria = {
    "direct_structure": "否（结果面 tech_chain_potential 在 gkx 280 张基表中零命中）",
    "direct_data": "否（无潜力值/成熟度结果列可读）",
    "dependency_structure": "部分（专利、科研项目、融资、专利转让四表在库；技术域字典 tech_domain 不在库）",
    "dependency_data": "部分（专利 2021—2024 四完整年；项目 2015—2020 连续、2022 后截断；融资金额仅 34.40% 披露；转让记录仅 2.341% 能回连专利主体）",
}

out = {
    "metric_id": M,
    "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    "domain_mapping_version": const["domain_mapping_version"],
    "patent_dedup_key": const["patent_dedup_key"],
    "base_years_used": const["base_years_used"],
    "base_years_missing": const["base_years_missing"],
    "base_years_note": const["base_years_note"],
    "constants_ref": "code/_snapshots21/tech5_constants_20261022.json",
    "support_judgment": "部分支持",
    "judgment_reason": "潜力值/成熟度无结果面可读，只能以专利技术强度与科研项目强度双源重建；"
                       "市场验证维（融资）金额披露率 34.40% 且无技术域外键，转化实绩维（专利转让）"
                       "仅 2.341% 的行能回连专利主体、交易表仅 10 行——产业化闭环的验证侧不可算，"
                       "故落部分支持。",
    "readface": {
        "gkx_tables_total": len(tables),
        "result_tables_found": result_tables,
        "like_hits": like,
        "verdict": "gkx 无 tech_chain_potential / tech_chain_node / tech_chain_edge / tech_domain；"
                   "缺表三态与逐表行数见 _work_gkx21/TABLE_ABSENCE_EVIDENCE.md",
    },
    "patent_axis": {
        "year_totals_2021_2024": year_totals,
        "total_2021_2024": base_total,
        "domains_total": len(dom_total),
        "hhi_base_pct2": hhi,
        "top20_share_pct": top20_share,
        "top_domains": top_pat,
        "section_totals": {s: sec_total[s] for s in sorted(sec_total)},
        "growth_up": sum(1 for g in dom_growth.values() if g is not None and g > 0),
        "growth_down": sum(1 for g in dom_growth.values() if g is not None and g < 0),
        "growth_zero_base": sum(1 for g in dom_growth.values() if g is None),
    },
    "project_axis": {
        "meta": proj_meta,
        "year_counts": proj_year,
        "usable_window": proj_window,
        "window_rows": proj_win_rows,
        "window_amount_wan": proj_win_amt,
        "truncation_note": "2021 年 2,339 个、2022 年 58 个、2023 年 6 个——2021 起采集不全，"
                           "2022 后基本为零；连续可比窗口取 2015—2020，不得把 2022—2024 零行读成「项目消失」。",
        "dept_distribution_2015_2020": proj_dept,
        "dept_total_2015_2020": proj_dept_total,
        "top_disciplines_2015_2020": proj_top,
        "project_level": proj_level,
        "amount_unit": "funded_amount 为万元（min 0.30、max 920.00，量级与国自然单项资助一致）",
    },
    "finance_axis": {
        "meta": fin,
        "currency": fin_cur,
        "amount_unit_dist": fin_unit,
        "amount_unit_pct": fin_unit_pct,
        "round_top12": fin_round,
        "year_counts_2018_plus": fin_year,
        "org_link": fin_link,
        "undisclosed_treatment": "金额空串 16,828 行（65.60%）按「未披露」单列，不按 0 参与均值/求和；"
                                 "若按 0 处理，强度类指标会系统性偏低，偏低方向不可估界。",
        "domain_link": "无技术域外键：org_id → dwd_org_base_info 命中 95.88%，但企业表无 IPC 字段，"
                       "「领域→企业→融资」链路在第二环断开",
    },
    "transfer_axis": {
        "rows": tr_rows,
        "pn_unique": tr_pn_unique,
        "matched_rows": tr_matched,
        "matched_pn_unique": int(transfer["matched_unique"]),
        "coverage_pct_of_rows": tr_cov,
        "coverage_pct_of_pn": tr_cov_pn,
        "domain_rate_top15": tr_rate,
        "verdict": "转让表存在但回连率仅 2.341%（534/22,809 行）——分子（域级转让件数）只覆盖"
                   "极小样本，域级转让率不足以支撑「转化实绩」判定；这一维按「有表、量不够」处理，"
                   "不按「无表」处理，两者补数路径不同。",
    },
    "deal_axis": {
        "meta": deal,
        "amount_columns": deal_amount_cols,
        "verdict": "10 行药品许可交易，licensee 全空、金额列不存在——无法作市场规模或转化金额来源",
    },
    "bridge": {
        "mapping": NSFC2IPC,
        "mapping_note": "本件自定义、待甲方确认：gkx 无学科—IPC 对照字典，NSFC 学部字母到 IPC 部为"
                        "人工映射，多目标按均摊分配；只作领域级粗排序，不作正式口径。",
        "weights": {"project_share": W_PROJ, "patent_share": W_PAT,
                    "market": 0, "transfer": 0},
        "project_alloc_total": proj_sec_n,
        "dept_unmapped": {k: v for k, v in proj_dept.items() if k not in NSFC2IPC},
        "dept_unmapped_projects": sum(v["projects"] for k, v in proj_dept.items()
                                      if k not in NSFC2IPC),
        "mapping_coverage_pct": round(proj_sec_n / proj_dept_total * 100, 2),
        "caveats": [
            "IPC D 部（纺织造纸）无任何 NSFC 学部映射到它，其 pot_score=0 是映射空缺，不是潜力为零",
            "E 学部（工程与材料）五目标均摊，导致 B/E/F 三部的 project_share 恒等（3.306%），"
            "三部之间的 project 维无区分力，排序只由专利维决定",
            "单点分配敏感性：最大位次变动 5 位（H 部），说明桥对映射规则敏感，只可作量级对照",
        ],
        "rows": bridge_sorted,
        "sensitivity_single_target": {
            "rule": "每个学部只取映射表第一个 IPC 部（单点分配）",
            "alt_project_share_pct": {b["ipc_section"]: round(v, 3) for b, v in zip(bridge, alt_ps)},
            "rank_shift": rank_shift,
            "max_abs_shift": max(abs(v) for v in rank_shift.values()) if rank_shift else 0,
        },
    },
    "domain_ranking_single_source": dom_rank,
    "degraded_sources": ["market_finance（金额披露 34.40%，无域外键）",
                         "transfer_record（回连率 2.341%）",
                         "deal（10 行、无金额列）",
                         "maturity/TRL（无法律状态全量与评审证据）"],
    "criteria": criteria,
    "notes": [
        "dwd_patent 为 2,939,895 行宽表，本件不做行级多字段聚合，专利侧全部读一次性全表扫描缓存",
        "dwd_zh_project 全表 58,453 行，聚合走 GROUP BY，不取回明细",
        "本件所有比例均在 JSON 中同时落分子与分母字段",
    ],
}

print(json.dumps({"domains": len(dom_total), "top": [r["ipc4"] for r in top_pat[:3]],
                  "proj_window_rows": proj_win_rows, "fin_rows": fin["rows"],
                  "transfer_cov_pct": tr_cov, "support": out["support_judgment"]},
                 ensure_ascii=False))

with open(CODE / f"{M}_out.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
    f.write("\n")
print(f"[OK] wrote {M}_out.json")

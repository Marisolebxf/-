#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_TECH_DEEP_132_1 技术发展历程模型 —— gkx 口径重建（20261022）。

只连 gkx。三条数据轴：
  主轴   专利 IPC4 域 × 申请年（读 code/_snapshots21/patent_ipc4_year_20261021.json，
         该缓存由 dwd_patent 主键分页全表扫描产出，见 PATENT_SCAN_LEDGER.md）
  辅轴   论文年序列（code/_snapshots21/papers_city_year_gkx21.json 的 year_all）
  辅轴   政策年序列（直查 gkx.dwd_policy_base，20,000 行小表）
  参考轴 链新闻（直查 gkx.dwd_industry_chain_news_info，只到年分布；无 IPC 列）

事件判定：域级年度序列的 z 分超阈 + 绝对量门槛（本件自定义，待甲方确认）。
产物：code/M_TECH_DEEP_132_1_out.json
"""
from __future__ import annotations

import collections
import json
import statistics
import time
from pathlib import Path

import pymysql

M = "M_TECH_DEEP_132_1"
CODE = Path(__file__).resolve().parent
SNAP = CODE / "_snapshots21"
GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", connect_timeout=60,
           read_timeout=600, write_timeout=600, autocommit=True)

BASE = [2021, 2022, 2023, 2024]
Z_TH = 1.0          # 本件自定义阈值，待甲方确认
N_MIN = 100         # 域年绝对量门槛（件），本件自定义
PEAK_RATIO = 1.3    # 峰值/均值比门槛，本件自定义
TOP_N = 20


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


def load(p):
    return json.load(open(p, encoding="utf-8"))


const = load(SNAP / "tech5_constants_20261022.json")
ipc_year = load(SNAP / "patent_ipc4_year_20261021.json")
paper_panel = load(SNAP / "papers_city_year_gkx21.json")

# ---------- 主轴：IPC4 域 × 年 ----------
nat = collections.defaultdict(dict)
for ipc4, y, n, org in ipc_year:
    nat[ipc4][int(y)] = int(n)

year_totals = {str(y): sum(v.get(y, 0) for v in nat.values()) for y in BASE}
dom_total = {d: sum(v.get(y, 0) for y in BASE) for d, v in nat.items()}
domains_ge100 = sum(1 for d, s in dom_total.items() if s / len(BASE) >= N_MIN)
top = [d for d, _ in sorted(dom_total.items(), key=lambda kv: -kv[1])[:TOP_N]]

events = []
top_rows = []
base_total = sum(year_totals.values())
for d in top:
    xs = [nat[d].get(y, 0) for y in BASE]
    mean = statistics.mean(xs)
    sd = statistics.pstdev(xs)
    zs = [(x - mean) / sd if sd else 0.0 for x in xs]
    for i, y in enumerate(BASE):
        burst = zs[i] >= Z_TH and xs[i] >= N_MIN
        peak = (xs[i] == max(xs)) and (max(xs) / mean >= PEAK_RATIO if mean else False) and xs[i] >= 1000
        if burst or peak:
            events.append({"ipc4": d, "year": y, "patents": xs[i],
                           "z": round(zs[i], 2),
                           "rule": "burst(z>=1.0)" if burst else "peak(ratio>=1.3)"})
    top_rows.append({"ipc4": d, "series": {str(y): xs[i] for i, y in enumerate(BASE)},
                     "mean": round(mean, 1), "sd": round(sd, 2),
                     "z": {str(y): round(zs[i], 2) for i, y in enumerate(BASE)},
                     "share_of_base_pct": round(dom_total[d] / base_total * 100, 3)})

by_year = collections.Counter(e["year"] for e in events)
up = sum(1 for d in dom_total if nat[d].get(2021, 0) and nat[d].get(2024, 0) > nat[d].get(2021, 0))
down = sum(1 for d in dom_total if nat[d].get(2021, 0) and nat[d].get(2024, 0) < nat[d].get(2021, 0))
zero_base = sum(1 for d in dom_total if not nat[d].get(2021, 0))
flat = len(dom_total) - up - down - zero_base

# ---------- 辅轴 1：论文年序列（缓存已由 dwd_zh_paper 全表落盘） ----------
paper_year = {int(y): int(n) for y, n in paper_panel["year_all"].items()}
paper_rows = int(paper_panel["rows_declared"])
paper_base = [paper_year.get(y, 0) for y in range(2015, 2024)]
pm, psd = statistics.mean(paper_base), statistics.pstdev(paper_base)
paper_z = {str(y): round((paper_year.get(y, 0) - pm) / psd, 2) for y in range(2015, 2027)}
paper_inc_2024 = round((paper_year.get(2024, 0) - statistics.mean(
    [paper_year.get(y, 0) for y in range(2015, 2025) if y != 2024])) /
    statistics.mean([paper_year.get(y, 0) for y in range(2015, 2025) if y != 2024]) * 100, 2)

# ---------- 辅轴 2：政策年序列（直查） ----------
pol = q("""SELECT publish_year y, COUNT(*) n FROM gkx.dwd_policy_base
           GROUP BY publish_year ORDER BY publish_year""")
pol_year = {}
for r in pol:
    try:
        pol_year[int(r["y"])] = int(r["n"])
    except (TypeError, ValueError):
        continue
pol_rows = int(q("SELECT COUNT(*) n FROM gkx.dwd_policy_base")[0]["n"])
pol_tail = {str(y): pol_year.get(y, 0) for y in range(2015, 2025)}
pol_base = [pol_year.get(y, 0) for y in range(2015, 2022)]
pm2, psd2 = statistics.mean(pol_base), statistics.pstdev(pol_base)
pol_z = {str(y): round((pol_year.get(y, 0) - pm2) / psd2, 2) for y in range(2015, 2023)}
pol_2022_drop_pct = round((pol_year.get(2022, 0) - pm2) / pm2 * 100, 2)

# ---------- 参考轴：链新闻（只到年，无 IPC 列） ----------
news_year_rows = q("""SELECT YEAR(publish_date) y, COUNT(*) n
                      FROM gkx.dwd_industry_chain_news_info
                      GROUP BY YEAR(publish_date) ORDER BY YEAR(publish_date)""")
news_year = {str(r["y"]): int(r["n"]) for r in news_year_rows if r["y"] is not None}
news_meta = q("""SELECT COUNT(*) n, COUNT(DISTINCT source) src,
                        COUNT(DISTINCT industry_code) ind_codes,
                        SUM(industry_code IS NOT NULL AND industry_code<>'') ind_fill
                 FROM gkx.dwd_industry_chain_news_info""")[0]
news_meta = {k: int(v) for k, v in news_meta.items()}
news_2022_2024 = sum(int(news_year.get(str(y), 0)) for y in (2022, 2023, 2024))
news_2025_2026 = sum(int(news_year.get(str(y), 0)) for y in (2025, 2026))

# ---------- 结果面与字典表核查 ----------
tables = [r["TABLE_NAME"] for r in q(
    "SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA='gkx'")]
ev_tables = [t for t in tables if "event" in t]
type_tables = [t for t in tables if "type" in t and ("event" in t or "domain" in t)]
domain_tables = [t for t in tables if "domain" in t]
ev_rows = q("SELECT COUNT(*) n, COUNT(DISTINCT event_name) names, "
            "MIN(start_date) mn, MAX(start_date) mx FROM gkx.dwd_event")[0]
ev_rows = {k: (int(v) if isinstance(v, __import__("decimal").Decimal) else v)
           for k, v in ev_rows.items()}
ev_sample = q("SELECT event_name FROM gkx.dwd_event ORDER BY dwd_id LIMIT 3")

result_tables = [t for t in ("tech_chain_events", "tech_chain_node", "tech_chain_edge",
                             "tech_domain", "event_type") if t in tables]

criteria = {
    "direct_structure": "否（结果面 tech_chain_events 与字典表 tech_domain / event_type 在 gkx 280 张基表中零命中）",
    "direct_data": "否（无事件事实面；dwd_event 仅 20 行会议清单，非技术事件）",
    "dependency_structure": "部分（专利/论文/政策三轴有结构；标准/媒体/博客/年度资讯四源无表）",
    "dependency_data": "部分（专利 2021—2024 四完整年、论文/政策历史段可用；新闻仅 2025—2026）",
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
    "event_rule": {
        "z_threshold": Z_TH,
        "min_patents": N_MIN,
        "peak_ratio": PEAK_RATIO,
        "top_domains": TOP_N,
        "note": "本件自定义阈值（z>=1.0 且域年>=100 件，或峰值年且峰值/均值>=1.3 且>=1000 件）；"
                "需求原文只写「定义事件指标并设定阈值」，未给数值，正式发布前须甲方确认。",
    },
    "readface": {
        "result_tables_found": result_tables,
        "gkx_tables_total": len(tables),
        "event_like_tables": ev_tables,
        "event_type_tables": type_tables,
        "domain_tables": domain_tables,
        "dwd_event": {"rows": ev_rows["n"], "distinct_names": ev_rows["names"],
                      "date_min": str(ev_rows["mn"]), "date_max": str(ev_rows["mx"]),
                      "sample": [r["event_name"] for r in ev_sample],
                      "verdict": "会议/论坛清单（event_name+organizer+start_date+event_url），"
                                 "既不是技术事件事实表，也不是事件类型字典"},
    },
    "patent_axis": {
        "year_totals_2021_2024": year_totals,
        "total_2021_2024": sum(year_totals.values()),
        "domains_total": len(dom_total),
        "domains_ge_100_per_year": domains_ge100,
        "growth_domains_2021_to_2024": {"up": up, "down": down, "flat": flat,
                                        "zero_base_2021": zero_base,
                                        "basis": "仅对有 2021 基数的域计算增减；与 M_TECH_DEEP_130_1 同一口径"},
        "top_domains": top_rows,
        "events": events,
        "events_total": len(events),
        "events_by_year": {str(y): by_year.get(y, 0) for y in BASE},
    },
    "paper_axis": {
        "rows": paper_rows,
        "year_counts": {str(y): paper_year.get(y, 0) for y in range(2015, 2027)},
        "z_baseline_2015_2023": paper_z,
        "anomaly_2024_z": paper_z.get("2024"),
        "anomaly_2024_vs_neighbors_pct": paper_inc_2024,
        "judgment": "2024 年入库批次跳变（相对 2015—2023 基线 z=22.81），"
                    "性质是采集/入库口径事件，不是科研产出突增；本件不据此判「论文爆发」。",
    },
    "policy_axis": {
        "rows": pol_rows,
        "year_counts_2015_2024": pol_tail,
        "usable_window": [2015, 2021],
        "z_baseline_2015_2021": pol_z,
        "drop_2022_pct": pol_2022_drop_pct,
        "judgment": "2022 年 289 条、2023 年零行、2024 年 1 条——采集窗口在 2022 年后截断，"
                    "不能读成「政策发布萎缩」；连续事件源只覆盖 2015—2021。",
    },
    "news_axis": {
        "rows": news_meta["n"],
        "sources": news_meta["src"],
        "industry_code_distinct": news_meta["ind_codes"],
        "industry_code_fill": news_meta["ind_fill"],
        "year_counts": news_year,
        "rows_2025_2026": news_2025_2026,
        "rows_2022_2024": news_2022_2024,
        "share_2025_2026_pct": round(news_2025_2026 / news_meta["n"] * 100, 2),
        "link_key": "无 IPC / 技术域列：industry_code 是产业链标签（JSON 数组），"
                    "与 dwd_patent.main_classification_ipcr 无可用外键",
        "judgment": "两年窗口（2025—2026）不构成年度事件序列；2022—2024 零行，"
                    "不能作为「无事件」的证据。",
    },
    "source_coverage": {
        "required_sources": ["技术新闻", "专利", "科研论文", "行业资讯", "技术标准发布信息",
                             "媒体报道量", "政策文件发布频率"],
        "available": ["专利", "科研论文", "政策文件发布频率"],
        "partial": ["技术新闻/行业资讯（仅 2025—2026，且无技术域键）"],
        "missing": ["技术标准发布信息", "媒体报道量", "技术博客（与资讯同族）"],
        "available_n": 3,
        "partial_n": 1,
        "missing_n": 3,
        "required_n": 7,
    },
    "criteria": criteria,
    "missing_sources": [
        "tech_chain_events（结果面）：gkx 280 张基表零命中，需按本件算子重建",
        "event_type（事件类型字典）：零命中；dwd_event 只是 20 行会议清单",
        "tech_domain（技术域字典）：零命中，域粒度只能取 IPC4",
        "技术标准发布信息：全库无 standard/std 语义表",
        "媒体报道量：全库无媒体量/媒体统计表",
        "技术博客：全库无 blog 表",
        "资讯年度序列：108,052 条全部落在 2025—2026，2022—2024 零行",
    ],
    "support_judgment": "部分支持",
    "judgment_reason": "专利主轴（2021—2024 四完整年、634 个 IPC4 域）与论文/政策两条辅轴可当日"
                       "重建时间线（Top20 域检出 15 条重大事件）；但需求七源中标准/媒体/博客三源"
                       "在 gkx 无表，资讯只有 2025—2026 两年且无技术域键，事件类型覆盖始终锁死在"
                       "专利一族——缺的是供给侧，不是算子。",
    "verdict_kind": "reconstructed",
    "sources": const["source"],
}

json.dump(out, open(CODE / f"{M}_out.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(json.dumps({"events": len(events), "domains": len(dom_total),
                  "top": top[:3], "paper2024_z": paper_z.get("2024"),
                  "news_rows": news_meta["n"], "support": out["support_judgment"]},
                 ensure_ascii=False))

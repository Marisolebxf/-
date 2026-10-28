#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_TECH_BASE_96_1 技术基础指标模型构建（gkx 口径，20261021 批）

数据来源
--------
- 直查 `gkx`（183.240.141.251:3318，只读账号 gkx_reader_zp）：
    dwd_zh_paper / dwd_zh_author / dwd_zh_paper_classification /
    dwd_scholar / dwd_industry_chain_news_info / dwd_news_base /
    dwd_deal / dwd_patent_transfer / dwd_bid_base_out / dwd_patent(COUNT(*))
- 读缓存（零 SQL，见 _work_gkx21/PATENT_SCAN_LEDGER.md）：
    _snapshots21/patent_ipc4_year_20261021.json   [ipc4, year, 件数, 机构数]
    _snapshots21/patent_ipc4_by_name_20261021.json[ipc4, 申请人, 件数]
    _snapshots21/gba_patent_20261021.json         year_all + city_year(2021—2024)
    _snapshots21/star_applicant_agg_gkx.json      agg[名称] = [件数, 授权数]

纪律
----
- 专利数字只读缓存，唯一一条 SQL 是 `COUNT(*)`（走索引，3 秒级）；
  不做任何非索引谓词的宽表聚合（DATA_FACTS §3.42）。
- 每条查询带 max_execution_time，连接失败重试 5 次、指数退避。
- 不写任何逐条查询耗时键（§3.44）。
- 不 import 本目录以外的私有 helper；只连 gkx。
"""
from __future__ import annotations

import collections
import json
import os
import re
import time

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
METRIC = "M_TECH_BASE_96_1"

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", database="gkx",
           connect_timeout=60, read_timeout=900, write_timeout=900,
           charset="utf8mb4", autocommit=True)

# 10 技术域 → IPC4 前缀（本件自定义；对齐深府〔2022〕1 号 20+8 清单与
# code/_tech21_common.py 的 SZ208_MAP 锚点，再补 10 域所需的码段）。
# 注意：IPC4 是 4 位小类，AI 芯片与量子信息在该粒度上无法从半导体/计算族中
# 单独切出，二者的计数是「所属族上界」，正文 §2.3 明示。
DOMAIN_IPC4 = {
    "人工智能": ["G06N", "G06V", "G06T", "G10L"],
    "AI芯片": ["H01L", "H10D", "H10H", "H10K", "H10F", "H10W", "H10P", "G11C"],
    "商业航天": ["B64G", "B64C", "B64D", "B64U", "F02K"],
    "生物医药": ["A61K", "A61P", "C07K", "C12N", "C12P", "A61B"],
    "储能": ["H01M", "H01G", "H02J"],
    "集成电路": ["H01L", "H05K", "H03K", "G05F"],
    "新能源": ["H02S", "F03D", "F03B", "C10L"],
    "量子信息": ["G01J", "G02F", "B82Y", "G06N"],
    "智能终端": ["G06F", "H04M", "G06C", "G09G"],
    "工业软件": ["G05B", "G06Q", "B25J"],
}

# 中图法一级类 → 10 域（本件自定义映射；一个一级类只能整体归域，故 5 个域
# 只能共用 TP/TN/TK 三个类，正文 §2.3 把它写成「域轴不可分辨」而不是假装一一对应）
CLASS_DOMAIN = {
    "TP": ["人工智能", "智能终端", "工业软件"],
    "TN": ["AI芯片", "集成电路", "智能终端"],
    "TM": ["储能"],
    "TK": ["储能", "新能源"],
    "V": ["商业航天"],
    "R": ["生物医药"],
    "Q": ["生物医药"],
    "X": ["新能源"],
    "O": ["量子信息"],
    "F": ["工业软件"],
}

# 城市词表（属地解析用；按出现位置取最先命中，避免「中国科学院深圳先进技术
# 研究院」被冠名地北京抢走）
CITIES = [
    "深圳", "广州", "东莞", "惠州", "珠海", "佛山", "中山", "江门", "肇庆",
    "北京", "上海", "天津", "重庆", "杭州", "南京", "武汉", "西安", "成都",
    "合肥", "青岛", "苏州", "长沙", "厦门", "济南", "郑州", "福州", "沈阳",
    "大连", "哈尔滨", "长春", "昆明", "南宁", "贵阳", "兰州", "太原", "石家庄",
]

CONNECT_RETRIES = 5


def connect():
    last = None
    for i in range(CONNECT_RETRIES):
        try:
            return pymysql.connect(**GKX)
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(min(2 ** i, 20))
    raise RuntimeError("gkx 连接 %d 次均失败：%r" % (CONNECT_RETRIES, last))


def q(sql, ms=180000, retries=4):
    """返回 (rows, err)。err 非空表示这条查询失败，调用方必须记 fail，不许当 0。"""
    if ms <= 0:
        raise ValueError("max_execution_time 不许设 0")
    last = None
    for attempt in range(retries):
        conn = None
        try:
            conn = connect()
            with conn.cursor() as cur:
                cur.execute("SET SESSION max_execution_time=%d" % int(ms))
                cur.execute(sql)
                return cur.fetchall(), None
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(min(3 * (attempt + 1), 15))
        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:  # noqa: BLE001
                    pass
    return None, "%s: %s" % (type(last).__name__, str(last)[:200])


def one(sql, ms=180000):
    rows, err = q(sql, ms=ms)
    if err:
        return None, err
    if not rows:
        return None, None
    return rows[0][0], None


def city_of(text):
    if not text:
        return None
    best = None
    for c in CITIES:
        p = text.find(c)
        if p >= 0 and (best is None or p < best[1]):
            best = (c, p)
    return best[0] if best else None


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def clean(o):
    """Decimal → int/float（pymysql 对 SUM/COUNT 的返回类型不稳定）。"""
    import decimal
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, decimal.Decimal):
        return int(o) if o == o.to_integral_value() else float(o)
    return o


def main():
    out = {
        "metric_id": METRIC,
        "source": "gkx@183.240.141.251:3318（只读 gkx_reader_zp）+ code/_snapshots21 专利缓存",
        "notes": [],
        "probes": {},
    }
    notes = out["notes"]

    # ---------- 1. 语料面盘点 ----------
    n_paper, e = one("SELECT COUNT(*) FROM gkx.dwd_zh_paper")
    probes = out["probes"]
    probes["dwd_zh_paper"] = {"rows": n_paper, "err": e}
    n_en, e = one("SELECT COUNT(*) FROM gkx.dwd_en_paper")
    probes["dwd_en_paper"] = {"rows": n_en, "err": e}
    n_author, e = one("SELECT COUNT(*) FROM gkx.dwd_zh_author")
    probes["dwd_zh_author"] = {"rows": n_author, "err": e}
    n_cls, e = one("SELECT COUNT(*) FROM gkx.dwd_zh_paper_classification")
    probes["dwd_zh_paper_classification"] = {"rows": n_cls, "err": e}
    n_scholar, e = one("SELECT COUNT(*) FROM gkx.dwd_scholar")
    probes["dwd_scholar"] = {"rows": n_scholar, "err": e}
    n_patent, e = one("SELECT COUNT(*) FROM gkx.dwd_patent", ms=120000)
    probes["dwd_patent"] = {"rows": n_patent, "err": e}

    # ---------- 2. 论文质量列与年份（整列自检） ----------
    rows, e = q(
        "SELECT SUM(download_num>0), SUM(download_num), SUM(open_access=1), "
        "SUM(abstract_available=1), COUNT(*) FROM gkx.dwd_zh_paper", ms=180000)
    probes["zh_paper_quality"] = {"row": rows[0] if rows else None, "err": e}
    quality = {"download_num_gt0": None, "download_num_sum": None,
               "open_access_1": None, "abstract_available_1": None,
               "rows": None}
    if rows:
        quality.update({
            "download_num_gt0": int(rows[0][0] or 0),
            "download_num_sum": int(rows[0][1] or 0),
            "open_access_1": int(rows[0][2] or 0),
            "abstract_available_1": int(rows[0][3] or 0),
            "rows": int(rows[0][4] or 0),
        })
    out["paper_quality"] = quality
    if quality["download_num_sum"] == 0:
        notes.append("dwd_zh_paper.download_num 全列为 0（求和 0、非零行 0）——下载量维不可用，"
                     "不参与任何结论（DATA_FACTS §3.10 同类陷阱）。")

    rows, e = q("SELECT cover_year_start, COUNT(*) FROM gkx.dwd_zh_paper "
                "GROUP BY cover_year_start ORDER BY cover_year_start", ms=180000)
    probes["zh_paper_year"] = {"rows": len(rows) if rows else 0, "err": e}
    paper_year = {}
    for y, c in (rows or []):
        key = str(y) if y not in (None, "", "NULL") else "NULL"
        paper_year[key] = int(c)
    out["paper_year"] = dict(sorted(paper_year.items(),
                                    key=lambda kv: (kv[0] == "NULL", kv[0])))

    # ---------- 3. 论文 ID 体系断裂（两套底册只重叠 799） ----------
    rows, e = q(
        "SELECT (SELECT COUNT(DISTINCT paper_id) FROM gkx.dwd_zh_author),"
        "(SELECT COUNT(DISTINCT id) FROM gkx.dwd_zh_paper_classification),"
        "(SELECT COUNT(*) FROM (SELECT DISTINCT paper_id FROM gkx.dwd_zh_author) x "
        " JOIN gkx.dwd_zh_paper p ON p.id=x.paper_id),"
        "(SELECT COUNT(*) FROM (SELECT DISTINCT id FROM gkx.dwd_zh_paper_classification) y "
        " JOIN gkx.dwd_zh_paper p ON p.id=y.id)", ms=300000)
    probes["paper_id_overlap"] = {"row": rows[0] if rows else None, "err": e}
    idf = {"author_distinct_paper_id": None, "class_distinct_id": None,
           "author_in_master": None, "class_in_master": None}
    if rows:
        idf = {
            "author_distinct_paper_id": int(rows[0][0]),
            "class_distinct_id": int(rows[0][1]),
            "author_in_master": int(rows[0][2]),
            "class_in_master": int(rows[0][3]),
        }
    idf["master_rows"] = n_paper
    idf["master_only"] = (idf["master_rows"] - idf["class_in_master"]
                          if idf["master_rows"] is not None else None)
    idf["author_corpus_only"] = (idf["class_distinct_id"] - idf["class_in_master"]
                                 if idf["class_distinct_id"] is not None else None)
    idf["overlap_ratio_on_class"] = (round(idf["class_in_master"] / idf["class_distinct_id"], 6)
                                     if idf.get("class_in_master") and idf.get("class_distinct_id") else None)
    out["paper_id_split"] = idf
    notes.append("论文主表 dwd_zh_paper（%s 行）与作者/学科标注所用的 paper_id 是两套 ID："
                 "20,048 个标注 ID 中只有 %s 个能在主表命中，主表另有 %s 行没有任何作者/学科标注。"
                 "论文维因此存在「有年份的没有学科、有学科的没有年份」的结构性断裂。"
                 % (idf["master_rows"], idf["class_in_master"], idf["master_only"]))

    # ---------- 4. 论文中图分类（学科轴） ----------
    rows, e = q("SELECT scope, COUNT(*) FROM gkx.dwd_zh_paper_classification "
                "GROUP BY scope ORDER BY COUNT(*) DESC", ms=180000)
    probes["zh_paper_scope"] = {"rows": len(rows) if rows else 0, "err": e}
    cls_prefix = collections.Counter()
    scope_detail = {}
    for scope, c in (rows or []):
        scope_detail[str(scope)] = int(c)
        m = re.match(r"^\[([A-Z]{1,2})\]", str(scope or ""))
        cls_prefix[m.group(1) if m else "UNK"] += int(c)
    out["paper_class_prefix"] = dict(cls_prefix.most_common())
    out["paper_class_scope_top20"] = dict(list(scope_detail.items())[:20])
    out["paper_class_total"] = sum(cls_prefix.values())

    # 10 域上界（同一一级类被多个域共用 → 计数不可相加）
    dom_paper = collections.OrderedDict()
    for d in DOMAIN_IPC4:
        classes = [p for p, ds in CLASS_DOMAIN.items() if d in ds]
        dom_paper[d] = {"classes": classes,
                        "count": sum(cls_prefix.get(p, 0) for p in classes)}
    out["paper_domain_upper"] = dom_paper
    out["paper_domain_note"] = ("中图一级类到 10 域是多对多：TP 同时服务人工智能/智能终端/工业软件，"
                                "TN 同时服务 AI芯片/集成电路/智能终端，TK 同时服务储能/新能源。"
                                "该表的 count 是「所属一级类上界」，不是域内真实命中数，不可相加。")

    # ---------- 5. 论文属地（作者机构 → 城市） ----------
    city_paper = collections.defaultdict(set)
    inst_fill = 0
    inst_total = 0
    sz_papers = set()
    rows_inst, e2 = q("SELECT paper_id, institution FROM gkx.dwd_zh_author", ms=300000)
    probes["zh_author_rows"] = {"rows": len(rows_inst) if rows_inst else 0, "err": e2}
    for pid, inst in (rows_inst or []):
        inst_total += 1
        if not inst:
            continue
        inst_fill += 1
        c = city_of(inst)
        if c:
            city_paper[c].add(pid)
            if c == "深圳":
                sz_papers.add(pid)
    papers_with_authors = idf["author_distinct_paper_id"] or 0
    out["paper_author_fill"] = {
        "author_rows": inst_total,
        "institution_filled": inst_fill,
        "institution_fill_ratio": round(inst_fill / inst_total, 6) if inst_total else None,
        "papers_with_authors": papers_with_authors,
        "papers_with_city": None,
    }
    city_paper_n = {c: len(s) for c, s in city_paper.items()}
    out["paper_city_top15"] = dict(sorted(city_paper_n.items(), key=lambda kv: -kv[1])[:15])
    out["paper_city_attributed_instances"] = sum(city_paper_n.values())

    # 深圳论文：按 paper_id 去重（机构代理，下界）
    out["sz_paper"] = {
        "papers": len(sz_papers),
        "denominator_papers": papers_with_authors,
        "share": round(len(sz_papers) / papers_with_authors, 6) if papers_with_authors else None,
        "method": "dwd_zh_author.institution 命中城市词表『深圳』的 paper_id 去重；机构代理，非论文级城市键",
    }
    # 论文有城市归属的 paper 数（用 institution-city 组合去重）
    city_pid = set()
    for c, s in city_paper.items():
        city_pid |= s
    out["paper_author_fill"]["papers_with_city"] = len(city_pid)
    out["paper_author_fill"]["city_cover_ratio"] = (round(len(city_pid) / papers_with_authors, 6)
                                                    if papers_with_authors else None)

    # ---------- 6. 前沿机构（质量维不可用 → 数量代理） ----------
    rows, e = q("SELECT institution, COUNT(DISTINCT paper_id) c FROM gkx.dwd_zh_author "
                "WHERE institution IS NOT NULL AND institution<>'' "
                "GROUP BY institution ORDER BY c DESC LIMIT 15", ms=300000)
    probes["zh_top_institution"] = {"rows": len(rows) if rows else 0, "err": e}
    out["top_institutions_by_paper"] = [
        {"institution": r[0], "papers": int(r[1])} for r in (rows or [])]
    out["frontier_org_quality"] = {
        "usable": False,
        "proxy": "机构发文量排行（数量代理）",
        "missing": ["期刊影响因子（列不存在）", "download_num（整列 0）",
                    "论文级被引（dwd_scholar_paper_relation.paper_id 与论文主表 ID 不通）"],
    }

    # ---------- 7. 专利域轴（读缓存） ----------
    ipc = load("patent_ipc4_year_20261021.json")
    tot = collections.Counter()
    by_year = collections.Counter()
    for ipc4, y, c, _o in ipc:
        tot[ipc4] += int(c)
        by_year[int(y)] += int(c)
    out["patent_ipc4_domains"] = len(tot)
    out["patent_ipc_rows"] = sum(tot.values())
    out["patent_year_ipc"] = dict(sorted(by_year.items()))
    out["patent_rows_total"] = n_patent
    out["patent_no_ipc"] = (n_patent - sum(tot.values())) if n_patent else None
    out["patent_ipc_coverage"] = (round(sum(tot.values()) / n_patent, 6) if n_patent else None)

    dom_patent = collections.OrderedDict()
    for d, prefixes in DOMAIN_IPC4.items():
        hit = [p for p in prefixes if p in tot]
        dom_patent[d] = {
            "ipc4": prefixes,
            "ipc4_hit": hit,
            "count": sum(tot[p] for p in hit),
            "share_of_ipc_rows": round(sum(tot[p] for p in hit) / sum(tot.values()), 6),
        }
    out["patent_domain"] = dom_patent
    out["patent_domain_sum"] = sum(v["count"] for v in dom_patent.values())
    out["patent_domain_note"] = ("IPC4 前缀可多域共享（H01L 同时在 AI芯片/集成电路，H01M 同时在储能/新能源，"
                                 "G06N 同时在人工智能/量子信息），故 10 域之和 > 有 IPC 的专利件数，不可相加。")

    # 深圳/城市专利（缓存，2021—2024）
    gba = load("gba_patent_20261021.json")
    year_all = {int(k): int(v) for k, v in gba["year_all"].items()}
    city_year = {k: {int(y): int(c) for y, c in v.items()} for k, v in gba["city_year"].items()}
    out["patent_year_all"] = dict(sorted(year_all.items()))
    sz = city_year.get("深圳市", {})
    out["sz_patent"] = {
        "by_year": dict(sorted(sz.items())),
        "sum_2021_2024": sum(sz.values()),
        "total_2021_2024": sum(v for y, v in year_all.items() if 2021 <= y <= 2024),
        "share_2024": round(sz.get(2024, 0) / year_all[2024], 6) if year_all.get(2024) else None,
        "share_2024_num": sz.get(2024, 0),
        "share_2024_den": year_all.get(2024),
        "method": "底册申请人名→城市匹配（org_name_city_20261021.json），非名称包含法",
    }
    city_rank = []
    for city, ys in city_year.items():
        v = sum(c for y, c in ys.items() if 2021 <= y <= 2024)
        if v:
            city_rank.append((city, v))
    city_rank.sort(key=lambda kv: -kv[1])
    out["patent_city_top12"] = [{"city": c, "patents_2021_2024": v} for c, v in city_rank[:12]]
    out["patent_city_attributed"] = sum(v for _, v in city_rank)
    out["patent_city_cover_ratio"] = round(sum(v for _, v in city_rank)
                                           / sum(v for y, v in year_all.items() if 2021 <= y <= 2024), 6)

    # ---------- 8. 领先专利主体（缓存） ----------
    star = load("star_applicant_agg_gkx.json")
    agg = star["agg"]
    top_app = sorted(agg.items(), key=lambda kv: -kv[1][0])[:15]
    out["top_applicants_overall"] = [
        {"name": n, "patents": int(v[0]), "grants": int(v[1])} for n, v in top_app]
    out["applicant_total"] = star.get("names")

    nm = load("patent_ipc4_by_name_20261021.json")
    by_ipc = collections.defaultdict(list)
    for ipc4, name, c in nm:
        by_ipc[ipc4].append((name, int(c)))
    dom_top = {}
    for d in ("人工智能", "生物医药", "储能", "集成电路"):
        pref = [p for p in DOMAIN_IPC4[d] if p in by_ipc]
        merged = collections.Counter()
        for p in pref:
            for name, c in by_ipc[p]:
                merged[name] += c
        dom_top[d] = [{"name": k, "patents": v} for k, v in merged.most_common(5)]
    out["domain_top_applicants"] = dom_top

    # ---------- 9. 交易维与资讯维 ----------
    n_deal, e = one("SELECT COUNT(*) FROM gkx.dwd_deal", ms=60000)
    probes["dwd_deal"] = {"rows": n_deal, "err": e}
    n_tr, e = one("SELECT COUNT(*) FROM gkx.dwd_patent_transfer", ms=120000)
    probes["dwd_patent_transfer"] = {"rows": n_tr, "err": e}
    n_bid, e = one("SELECT COUNT(*) FROM gkx.dwd_bid_base_out", ms=120000)
    probes["dwd_bid_base_out"] = {"rows": n_bid, "err": e}
    cols, e = q("SELECT table_name, column_name FROM information_schema.columns "
                "WHERE table_schema='gkx' AND table_name IN ('dwd_deal','dwd_patent_transfer')",
                ms=60000)
    probes["trade_cols"] = {"err": e}
    trade_cols = collections.defaultdict(list)
    for (t, c) in (cols or []):
        trade_cols[t].append(c)
    out["trade_sources"] = {
        "dwd_deal": {"rows": n_deal, "columns": trade_cols.get("dwd_deal", []),
                     "has_amount_column": any("amount" in c or "金额" in c
                                              for c in trade_cols.get("dwd_deal", []))},
        "dwd_patent_transfer": {"rows": n_tr, "columns": trade_cols.get("dwd_patent_transfer", []),
                                "has_amount_column": any("amount" in c or "price" in c
                                                         for c in trade_cols.get("dwd_patent_transfer", []))},
        "dwd_bid_base_out": {"rows": n_bid,
                             "note": "招投标公告（买方采购口径），有 total_amount 但非技术合同认定登记"},
        "tech_contract_registry": {"exists": False,
                                   "evidence": "information_schema 表名扫描 contract/tech_trade/transaction 零命中"},
    }

    n_news, e = one("SELECT COUNT(*) FROM gkx.dwd_industry_chain_news_info", ms=300000)
    probes["dwd_industry_chain_news_info"] = {"rows": n_news, "err": e}
    n_news2, e = one("SELECT COUNT(*) FROM gkx.dwd_news_base", ms=300000)
    probes["dwd_news_base"] = {"rows": n_news2, "err": e}
    rows, e = q("SELECT COUNT(DISTINCT industry_code), COUNT(DISTINCT industry_name) "
                "FROM gkx.dwd_industry_chain_news_info", ms=300000)
    probes["news_industry"] = {"row": rows[0] if rows else None, "err": e}
    out["news"] = {
        "chain_news_rows": n_news,
        "news_base_rows": n_news2,
        "distinct_industry_code": int(rows[0][0]) if rows else None,
        "distinct_industry_name": int(rows[0][1]) if rows else None,
        "tech_domain_tagged_rows": 0,
        "note": "资讯表有 industry_code/industry_name（产业链口径），无 IPC/技术域字段，"
                "无法按 10 技术域切分；二者词表不同源，不做折算。",
    }

    # ---------- 10. 11 子指标矩阵 ----------
    matrix = [
        {"code": "D1", "name": "论文数量(按域)", "status": "代理",
         "evidence": "有学科标注 20,048 篇（占主表 19.87%），中图一级类到 10 域多对多，只有上界"},
        {"code": "D2", "name": "深圳论文数量", "status": "代理",
         "evidence": "作者机构含深圳的 paper_id 去重 %d 篇（机构代理，下界）" % len(sz_papers)},
        {"code": "D3", "name": "区域论文数量", "status": "代理",
         "evidence": "机构城市解析，有城市归属的 paper %d 篇" % len(city_pid)},
        {"code": "D4", "name": "前沿论文机构", "status": "无源",
         "evidence": "影响因子列不存在、download_num 整列 0、论文级被引 ID 不通"},
        {"code": "D5", "name": "专利数量(按域)", "status": "直接",
         "evidence": "主分类 IPC4 归域，有 IPC 的 %d 件" % sum(tot.values())},
        {"code": "D6", "name": "深圳专利数量", "status": "直接",
         "evidence": "2024 年 %s / %s" % (sz.get(2024), year_all.get(2024))},
        {"code": "D7", "name": "区域专利申请数", "status": "直接",
         "evidence": "底册名称→城市匹配，2021—2024 归属 %d 件" % out["patent_city_attributed"]},
        {"code": "D8", "name": "领先专利主体机构", "status": "代理",
         "evidence": "申请人件数/授权数可算；质量分（被引/维持）无源"},
        {"code": "D9", "name": "技术交易额分析", "status": "无源",
         "evidence": "无技术合同登记表；dwd_deal 10 行无金额；dwd_patent_transfer 无成交价"},
        {"code": "D10", "name": "技术交易额区域分析", "status": "无源",
         "evidence": "同 D9，且无属地金额字段"},
        {"code": "D11", "name": "技术动态资讯", "status": "无源",
         "evidence": "链新闻 %s 行有产业链标签、无技术域标签" % n_news},
    ]
    out["sub_metric_matrix"] = matrix
    out["sub_metric_counts"] = dict(collections.Counter(m["status"] for m in matrix))

    out["support_judgment"] = "部分支持"
    out["judgment_reason"] = (
        "11 子指标中专利计数与深圳/区域专利维可直接出数（主分类 IPC4 2,420,915 件、"
        "2024 深圳 275,908 件），论文维只能给「学科上界 + 机构代理」两套降级读数；"
        "前沿机构质量维因影响因子列缺失、download_num 整列 0、论文级被引 ID 不通而不可算；"
        "技术交易额两维无技术合同登记表（dwd_deal 10 行无金额、dwd_patent_transfer 无成交价、"
        "dwd_bid_base_out 是招投标买方口径），技术动态资讯维无技术域标签。"
        "始终存在无法补齐的依赖维，故落部分支持，不抬档。")

    out["base_years_used"] = [2021, 2022, 2023, 2024, 2025, 2026]
    out["base_years_missing"] = []
    out["base_years_note"] = (
        "专利窗口 2021—2026（dwd_patent.apdt_year 仅此六年，2017—2020 零行，不补 0、不摊入分母）；"
        "2026 为残年（69,747 件，约为 2025 的 20.4%），只做端点披露、不用于增速。"
        "论文侧 cover_year_start 跨 2001—2026，但学科标注那 20,048 篇没有年份字段，"
        "故论文不做域×年双轴序列。城市专利分布窗口为 2021—2024（缓存决定的四年）。")

    with open(os.path.join(HERE, METRIC + "_out.json"), "w", encoding="utf-8") as f:
        json.dump(clean(out), f, ensure_ascii=False, indent=1)
    print("wrote", METRIC + "_out.json")
    print("sub_metric_counts", out["sub_metric_counts"])
    print("sz_patent", out["sz_patent"]["share_2024_num"], "/", out["sz_patent"]["share_2024_den"])


if __name__ == "__main__":
    main()

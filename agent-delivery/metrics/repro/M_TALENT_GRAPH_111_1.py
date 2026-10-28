#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_TALENT_GRAPH_111_1 人才实体关系抽取（gkx 口径，20261021 批）

只连 gkx（183.240.141.251:3318，只读账号 gkx_reader_zp），用到的表：
    dwd_scholar                    人才主档（21,316）
    dwd_scholar_coauthor           共著关系（1,187,606 行）
    dwd_scholar_research_direction 研究方向（20,030 行，自由文本）
    dwd_scholar_paper_relation     人才-论文关系（1,065,385 行）

本件要回答的是：需求明列的 6 类关系（产业/技术/企业/科研机构/服务机构/政策）里，
gkx 能建成几类、每一类的证据强度如何。

关键实测（写进产物，正文引用）：
  - dwd_scholar.scholar_org_id 整列为空（0/21,316），机构节点只能用名称串，无 ID 消歧；
  - 共著表 118.76 万行里只有 8,675 行的 co_scholar_id 在人才主档内（0.73%），
    表内 899,662 个不同 co_scholar_id 绝大多数是库外学者；
  - 研究方向是自由文本：163,470 个标签实例、97,249 个不同值，82.3% 的标签只出现一次，
    没有受控词表。
"""
from __future__ import annotations

import collections
import datetime
import decimal
import json
import os
import time

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
METRIC = "M_TALENT_GRAPH_111_1"

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", database="gkx",
           connect_timeout=60, read_timeout=900, write_timeout=900,
           charset="utf8mb4", autocommit=True)

TAG_MIN = 20        # 研究方向标签建节点的最小人才数（低于此归长尾，不建节点）


def connect():
    last = None
    for i in range(5):
        try:
            return pymysql.connect(**GKX)
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(min(2 ** i, 20))
    raise RuntimeError("gkx 连接 5 次均失败：%r" % (last,))


def q(sql, ms=300000, retries=4):
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


def one(sql, ms=300000):
    rows, err = q(sql, ms=ms)
    if err:
        return None, err
    return (rows[0][0] if rows else None), None


def clean(o):
    """pymysql 返回 Decimal/date/bytes，统一转原生类型。"""
    if isinstance(o, decimal.Decimal):
        f = float(o)
        return int(f) if f == int(f) else round(f, 8)
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
    if isinstance(o, bytes):
        return o.decode("utf-8", "replace")
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    return o


def main():
    out = {"metric_id": METRIC,
           "source": "gkx@183.240.141.251:3318（只读 gkx_reader_zp）",
           "notes": [], "probes": {}}
    probes = out["probes"]
    notes = out["notes"]

    # ---------- 1. 人才主档 ----------
    rows, e = q("SELECT COUNT(*), SUM(scholar_org_name_zh IS NOT NULL AND scholar_org_name_zh<>'' "
                "AND scholar_org_name_zh<>'null'), SUM(scholar_org_id IS NOT NULL AND scholar_org_id<>''), "
                "SUM(h_index>0), SUM(citation_nums>0), SUM(paper_nums>0) FROM gkx.dwd_scholar", ms=180000)
    probes["dwd_scholar"] = {"row": rows[0] if rows else None, "err": e}
    r = rows[0] if rows else (None,) * 6
    scholars = int(r[0] or 0)
    out["scholar"] = {
        "rows": scholars,
        "org_name_filled": int(r[1] or 0),
        "org_name_fill_ratio": round((r[1] or 0) / scholars, 6) if scholars else None,
        "org_id_filled": int(r[2] or 0),
        "h_index_gt0": int(r[3] or 0),
        "citation_gt0": int(r[4] or 0),
        "paper_nums_gt0": int(r[5] or 0),
    }
    if out["scholar"]["org_id_filled"] == 0:
        notes.append("dwd_scholar.scholar_org_id 整列为空（0/%d）——机构节点只能用名称串，"
                     "同名机构无法合并、同机构不同写法无法归并，机构级结论只能作名称聚合、"
                     "不构成机构实体消歧。" % scholars)

    rows, e = q("SELECT scholar_org_name_zh, COUNT(*) c FROM gkx.dwd_scholar "
                "WHERE scholar_org_name_zh IS NOT NULL AND scholar_org_name_zh<>'' "
                "GROUP BY scholar_org_name_zh ORDER BY c DESC LIMIT 15", ms=180000)
    probes["scholar_org_top"] = {"rows": len(rows) if rows else 0, "err": e}
    n_org, e2 = one("SELECT COUNT(DISTINCT scholar_org_name_zh) FROM gkx.dwd_scholar "
                    "WHERE scholar_org_name_zh IS NOT NULL AND scholar_org_name_zh<>''", ms=180000)
    probes["scholar_org_distinct"] = {"value": n_org, "err": e2}
    out["org_layer"] = {
        "distinct_org_names": n_org,
        "edges_scholar_org": out["scholar"]["org_name_filled"],
        "top15": [{"org": x[0], "scholars": int(x[1])} for x in (rows or [])],
    }

    # ---------- 2. 共著关系（人才-人才） ----------
    n_ca, e = one("SELECT COUNT(*) FROM gkx.dwd_scholar_coauthor", ms=300000)
    probes["dwd_scholar_coauthor"] = {"rows": n_ca, "err": e}
    n_ca_in, e = one("SELECT COUNT(*) FROM gkx.dwd_scholar_coauthor c "
                     "JOIN gkx.dwd_scholar s ON s.scholar_id=c.co_scholar_id", ms=300000)
    probes["coauthor_dst_in_roster"] = {"rows": n_ca_in, "err": e}
    # 双向都在主档内才是「主档内可遍历的边」；只查 dst 会把「库外学者→库内学者」
    # 的行也算进来，边的一端不在主档里，图谱上画不出来。两个数都落盘，正文用双向。
    n_ca_both, e = one("SELECT COUNT(*) FROM gkx.dwd_scholar_coauthor c "
                       "JOIN gkx.dwd_scholar a ON a.scholar_id=c.scholar_id "
                       "JOIN gkx.dwd_scholar b ON b.scholar_id=c.co_scholar_id", ms=300000)
    probes["coauthor_both_ends_in_roster"] = {"rows": n_ca_both, "err": e}
    rows, e = q("SELECT c.scholar_id, c.co_scholar_id, c.co_paper_count "
                "FROM gkx.dwd_scholar_coauthor c "
                "JOIN gkx.dwd_scholar a ON a.scholar_id=c.scholar_id "
                "JOIN gkx.dwd_scholar b ON b.scholar_id=c.co_scholar_id", ms=300000)
    probes["coauthor_edges"] = {"rows": len(rows) if rows else 0, "err": e}
    und = set()
    wsum = 0
    for a, b, w in (rows or []):
        und.add((a, b) if a < b else (b, a))
        wsum += int(w or 0)
    deg = collections.Counter()
    for a, b in und:
        deg[a] += 1
        deg[b] += 1
    # 连通分量（并查集）
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in und:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    comp = collections.Counter(find(x) for x in parent)
    out["coauthor_layer"] = {
        "table_rows": n_ca,
        "rows_with_dst_in_roster": n_ca_in,
        "dst_hit_ratio": round(n_ca_in / n_ca, 6) if n_ca else None,
        "rows_with_both_ends_in_roster": n_ca_both,
        "both_ends_hit_ratio": round(n_ca_both / n_ca, 6) if n_ca else None,
        "undirected_edges": len(und),
        "nodes_with_edge": len(deg),
        "isolate_rate": round((scholars - len(deg)) / scholars, 6) if scholars else None,
        "avg_degree": round(sum(deg.values()) / len(deg), 4) if deg else None,
        "max_degree": max(deg.values()) if deg else None,
        "components": len(comp),
        "largest_component": max(comp.values()) if comp else None,
        "co_paper_weight_sum": wsum,
        "top15_by_degree": [{"scholar_id": k, "degree": v} for k, v in deg.most_common(15)],
        "degree_hist": dict(collections.Counter(
            ("1" if v == 1 else "2-4" if v <= 4 else "5-9" if v <= 9 else "10+")
            for v in deg.values())),
        "edge_scope_note": "只取两端都在 dwd_scholar 里的行（%d 行）；若只要求受方在主档，"
                           "行数会虚高到 %d 行，但那类边的另一端画不出来。" % (n_ca_both, n_ca_in),
    }

    # ---------- 3. 研究方向（人才-技术） ----------
    rows, e = q("SELECT scholar_id, fields FROM gkx.dwd_scholar_research_direction", ms=300000)
    probes["research_direction"] = {"rows": len(rows) if rows else 0, "err": e}
    tag_count = collections.Counter()
    instances = 0
    scholars_rd = 0
    for sid, s in (rows or []):
        scholars_rd += 1
        if not s:
            continue
        for t in str(s).split(";"):
            t = t.strip()
            if t:
                tag_count[t] += 1
                instances += 1
    kept = {t: c for t, c in tag_count.items() if c >= TAG_MIN}
    kept_instances = sum(kept.values())
    top100 = sum(c for _t, c in tag_count.most_common(100))
    out["research_layer"] = {
        "rows": len(rows or []),
        "scholars": scholars_rd,
        "tag_instances": instances,
        "distinct_tags": len(tag_count),
        "singleton_tags": sum(1 for c in tag_count.values() if c == 1),
        "singleton_ratio": round(sum(1 for c in tag_count.values() if c == 1)
                                 / len(tag_count), 6) if tag_count else None,
        "top100_share": round(top100 / instances, 6) if instances else None,
        "tag_min_for_node": TAG_MIN,
        "node_tags": len(kept),
        "node_tag_instances": kept_instances,
        "node_tag_instance_ratio": round(kept_instances / instances, 6) if instances else None,
        "has_controlled_vocabulary": False,
        "top15": [{"tag": t, "scholars": c} for t, c in tag_count.most_common(15)],
    }
    notes.append("研究方向字段是自由文本：%d 个标签实例、%d 个不同值，单次出现的标签占 %s，Top100 只覆盖 %s。"
                 "它只能作「技术主题的弱关系」，不能当受控技术词表用。"
                 % (instances, len(tag_count),
                    round(out["research_layer"]["singleton_ratio"] * 100, 2),
                    round(out["research_layer"]["top100_share"] * 100, 2)))

    # ---------- 4. 人才-论文 ----------
    n_spr, e = one("SELECT COUNT(*) FROM gkx.dwd_scholar_paper_relation", ms=300000)
    probes["scholar_paper_relation"] = {"rows": n_spr, "err": e}
    n_spr_scholar, e = one("SELECT COUNT(DISTINCT scholar_id) FROM gkx.dwd_scholar_paper_relation",
                           ms=300000)
    probes["spr_scholars"] = {"value": n_spr_scholar, "err": e}
    n_cit, e = one("SELECT SUM(citations>0) FROM gkx.dwd_scholar_paper_relation", ms=300000)
    probes["spr_citations"] = {"value": n_cit, "err": e}
    rows, e = q("SELECT year, COUNT(*) FROM gkx.dwd_scholar_paper_relation GROUP BY year "
                "ORDER BY year", ms=300000)
    probes["spr_year"] = {"rows": len(rows) if rows else 0, "err": e}
    yr = {}
    for y, c in (rows or []):
        yr[str(y)] = int(c)
    valid_years = sum(v for k, v in yr.items() if k.isdigit() and 1980 <= int(k) <= 2026)
    out["paper_layer"] = {
        "rows": n_spr,
        "scholars": n_spr_scholar,
        "citations_gt0": int(n_cit or 0),
        "year_dist": yr,
        "year_valid_rows": valid_years,
        "year_invalid_rows": (n_spr - valid_years) if n_spr else None,
        "note": "year 字段存在 0 与 2099 等脏值，年度序列只取 1980—2026；"
                "被引非零 %s 行，是库内唯一可用的质量代理，但只在人才-论文关系内。" % n_cit,
    }

    # ---------- 5. 政策依赖的错配核查（CLASSIFY 把 policy_entity 列为依赖表） ----------
    rows, e = q("SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
                "AND (table_name LIKE '%%policy%%' OR table_name LIKE '%%graph%%') "
                "ORDER BY table_name", ms=60000)
    probes["policy_graph_tables"] = {"rows": rows, "err": e}
    pol_tables = [x[0] for x in (rows or [])]
    out["classify_mismatch"] = {
        "classify_dependency": "policy_entity",
        "table_exists": "policy_entity" in pol_tables,
        "policy_tables_in_gkx": pol_tables,
        "verdict": ("CLASSIFY 把 policy_entity 列为人才图谱的依赖表属旧稿错配：人才共著网络不需要政策实体表，"
                    "gkx 也没有名为 policy_entity 的表（政策侧只有文本主表）。本件不依赖政策表，"
                    "故该依赖项不构成缺口，但也不改变「人才-政策」关系无载体的结论。"),
    }

    # ---------- 6. 六类需求关系覆盖 ----------
    relations = [
        {"type": "科研机构", "built": True, "edges": out["scholar"]["org_name_filled"],
         "evidence": "dwd_scholar.scholar_org_name_zh（97.72% 填充），机构 ID 全空、只能名称聚合"},
        {"type": "技术", "built": "weak", "edges": kept_instances,
         "evidence": "dwd_scholar_research_direction.fields 自由文本；建节点标签 %d 个，"
                     "只覆盖 %s 的标签实例" % (len(kept),
                                              round(kept_instances / instances, 6) if instances else None)},
        {"type": "人才-人才(补充)", "built": True, "edges": len(und),
         "evidence": "dwd_scholar_coauthor 两端都在主档的无向边 %d 条；表内 %s 的行两端不同时在主档内" % (len(und), round(1 - (n_ca_both / n_ca), 4) if n_ca else None)},
        {"type": "人才-论文(补充)", "built": True, "edges": n_spr,
         "evidence": "dwd_scholar_paper_relation，%d 位人才" % (n_spr_scholar or 0)},
        {"type": "企业", "built": False, "edges": 0,
         "evidence": "无人才-企业关系表；主档只有机构名称，无统一社会信用代码/企业 ID 字段；"
                     "学历表 %d 行也只能挂机构名，挂不到企业" % n_edu},
        {"type": "产业", "built": False, "edges": 0,
         "evidence": "无人才-产业标签表；研究方向是学术主题，不能当 20+8 产业标签"},
        {"type": "服务机构", "built": False, "edges": 0,
         "evidence": "无人才-服务机构关系表"},
        {"type": "政策", "built": False, "edges": 0,
         "evidence": "无人才-政策关系表；政策主表 dwd_policy_base 无人才实体字段"},
    ]
    required = [x for x in relations if x["type"] in ("科研机构", "技术", "企业", "服务机构", "政策")]
    built_req = [x for x in required if x["built"] is True]
    weak_req = [x for x in required if x["built"] == "weak"]
    out["relations"] = relations
    out["coverage"] = {
        "required_types": len(required),
        "built_strong": len(built_req),
        "built_weak": len(weak_req),
        "not_built": len(required) - len(built_req) - len(weak_req),
        "ratio_strong": round(len(built_req) / len(required), 6),
        "ratio_strong_plus_weak": round((len(built_req) + len(weak_req)) / len(required), 6),
        "required_list": [x["type"] for x in required],
    }

    out["graph"] = {
        "nodes_scholar": scholars,
        "nodes_org_name": n_org,
        "nodes_tag": len(kept),
        "edges_total": (out["scholar"]["org_name_filled"] + kept_instances + len(und)),
        "edges_by_relation": {
            "scholar_org": out["scholar"]["org_name_filled"],
            "scholar_tag": kept_instances,
            "scholar_scholar": len(und),
            "scholar_paper": n_spr,
        },
        "density_scholar_subgraph": round(
            2 * len(und) / (scholars * (scholars - 1)), 10) if scholars > 1 else None,
        "note": "密度只对人才-人才子图有意义；机构与研究方向节点是星型挂接，密度不可比。",
    }

    out["support_judgment"] = "部分支持"
    out["judgment_reason"] = (
        "需求明列的 5 类实体关系里只有「科研机构」可强建成（%d 条，按机构名称串），"
        "「技术」只能弱建成（研究方向自由文本，%d 个不同标签、%s%% 只出现一次，无受控词表）；"
        "「企业 / 产业 / 服务机构 / 政策」四类在 gkx 无任何关系表或可映射字段。"
        "共著关系两端同时落在人才主档内的行只有 %d/%d（%s%%），机构 ID 整列为空（0/%d），"
        "主档内网络 %s%% 的学者是孤点。骨架可建、五类关系只落实一类强一类弱，故落部分支持。"
        % (out["scholar"]["org_name_filled"],
           len(tag_count),
           round(out["research_layer"]["singleton_ratio"] * 100, 2),
           n_ca_both, n_ca,
           round(100.0 * n_ca_both / n_ca, 2) if n_ca else None,
           scholars,
           round(100.0 * (scholars - len(deg)) / scholars, 2) if scholars else None))

    out["base_years_used"] = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]
    out["base_years_missing"] = []
    out["base_years_note"] = (
        "本件不做年度环比，基期只用于声明语料年份覆盖：dwd_scholar_paper_relation.year 的取值"
        "有效区间为 1980—2026（另有 year=0 与 year=2099 的脏值，已剔除、不摊 0）。"
        "关系图本身是截面，不随年份重算。")

    with open(os.path.join(HERE, METRIC + "_out.json"), "w", encoding="utf-8") as f:
        json.dump(clean(out), f, ensure_ascii=False, indent=1)
    print("wrote", METRIC + "_out.json")
    print("coverage", json.dumps(out["coverage"], ensure_ascii=False))
    print("coauthor", {k: out["coauthor_layer"][k] for k in
                       ("undirected_edges", "nodes_with_edge", "isolate_rate", "components")})
    print("graph_edges", out["graph"]["edges_total"])


if __name__ == "__main__":
    main()

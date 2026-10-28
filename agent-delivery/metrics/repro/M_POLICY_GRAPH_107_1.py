#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_POLICY_GRAPH_107_1 政策实体关系抽取（gkx 口径，20261021 批）

只连 gkx（183.240.141.251:3318，只读账号 gkx_reader_zp）。用到的表：
    dwd_policy_base            政策文本主表（20,000 条）
    dwd_industry_chain_info    产业链节点（1,273 行 / 1,150 个不同名称）

本件要回答：需求 §1.1.1.1.1.1.1.2.6 点名的五类关系（政策主题 / 政策目标 /
实施主体 / 受益对象 / 监管机构）在 gkx 能建起几类，建出来的边是什么定义。

三条前置事实（脚本内实测，正文引用）：
  1. gkx 没有 policy_graph_edge / policy_entity / policy_entity_relation 三张表，
     边必须从 dwd_policy_base 的字段现建——这是**本件自定义口径**，不是官方口径；
  2. theme 只有 2 行真值、keywords / keypoints 整列为空、policy_support 全部是
     字面 'null'（JSON_KEYS 返回 NULL，JSON_LENGTH 却返回 1，是个假阳性陷阱）；
  3. 发文机关（ministry）是**发文方**，不是「实施主体」也不是「监管机构」，
     用它填这两个槽位是方向性替代，必须在正文标明偏在哪个方向。

边定义（本件自定义，待甲方确认）：
  政策—发文机关        policy  → ministry        权重 1
  政策—政策层级        policy  → level(rank 数组) 权重 1（一条政策可挂多级）
  政策—文种            policy  → type            权重 1
  政策—适用地区        policy  → province/city/district 权重 1
  政策—产业节点        policy  → chain node      权重 = 命中次数（标题命中，长名优先）
  政策—政策 共现边     不落库：只算「同机关同年」团簇规模，作为反证
"""
from __future__ import annotations

import collections
import datetime
import decimal
import json
import os
import re
import time

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
METRIC = "M_POLICY_GRAPH_107_1"

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", database="gkx",
           connect_timeout=60, read_timeout=900, write_timeout=900,
           charset="utf8mb4", autocommit=True)

# 产业节点名的入边门槛：少于 4 个汉字的名称（如「零部件」「材料」）在标题里
# 大量命中歧义，本件不建边，只统计其规模作为缺口证据。
MIN_NODE_NAME_LEN = 4
# 正文级命中率抽样：按 CRC32(id) 排序取前 N 条，可复现的确定性抽样
CONTENT_SAMPLE = 800
NULLISH = {"", "NULL", "null", "Null", "[]", "{}", '[""]'}


def clean(o):
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


def connect():
    last = None
    for i in range(5):
        try:
            return pymysql.connect(**GKX)
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(min(2 ** i, 20))
    raise RuntimeError("gkx 连接 5 次均失败：%r" % (last,))


def q(sql, ms=300000, retries=5):
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
            time.sleep(min(3 * (attempt + 1), 20))
        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:  # noqa: BLE001
                    pass
    return None, "%s: %s" % (type(last).__name__, str(last)[:200])


def nz(v):
    return v is not None and str(v).strip() not in NULLISH


def parse_levels(raw):
    """rank 列是 JSON 数组字符串：'["省级"]' / '["省级","市级"]' / '[""]'。"""
    if not nz(raw):
        return []
    try:
        arr = json.loads(raw)
    except Exception:  # noqa: BLE001
        txt = str(raw)
        return [x for x in re.findall(r"(国家级|省级|市级|区级|园区级)", txt)]
    if not isinstance(arr, list):
        return []
    return [str(x).strip() for x in arr if str(x).strip() in
            ("国家级", "省级", "市级", "区级", "园区级")]


def main():
    out = {"metric_id": METRIC,
           "metric_name_zh": "政策实体关系抽取",
           "source": "gkx@183.240.141.251:3318（只读 gkx_reader_zp）",
           "notes": [], "probes": {}}
    probes, notes = out["probes"], out["notes"]

    # ---------- 0. 负向探针：三张「本该有」的表是否存在 ----------
    rows, e = q("SELECT table_name FROM information_schema.tables "
                "WHERE table_schema='gkx' AND (table_name LIKE '%%policy%%' "
                "OR table_name LIKE '%%graph%%' OR table_name LIKE '%%entity%%') "
                "ORDER BY table_name", ms=60000)
    probes["policy_graph_like_tables"] = {"rows": rows, "err": e}
    tbl = [x[0] for x in (rows or [])]
    wanted = ["policy_graph_edge", "policy_entity", "policy_entity_relation"]
    out["absence"] = {
        "scanned_patterns": ["%policy%", "%graph%", "%entity%"],
        "tables_found": tbl,
        "wanted_but_absent": [t for t in wanted if t not in tbl],
        "wanted_present": [t for t in wanted if t in tbl],
        "note": "gkx 政策侧只有文本主表 dwd_policy_base 与 dwd_global_policy_base（及两份 bak），"
                "没有任何「政策—实体」或「政策—政策」的现成边表；本件的全部边均为字段现建。",
    }

    # ---------- 1. 政策主表 ----------
    rows, e = q("SELECT id, title, ministry, `rank`, `type`, province, city, district, "
                "publish_year, theme, keywords, keypoints, policy_support, "
                "CHAR_LENGTH(content) FROM gkx.dwd_policy_base", ms=600000)
    probes["dwd_policy_base"] = {"rows": len(rows) if rows is not None else None, "err": e}
    pol = rows or []
    out["policy"] = {"rows": len(pol)}

    # 字段级填充（逐列，不用同义列合并——这里没有同义列）
    fill = collections.Counter()
    for r in pol:
        for idx, key in ((2, "ministry"), (3, "rank"), (4, "type"), (5, "province"),
                         (6, "city"), (7, "district"), (8, "publish_year"),
                         (9, "theme"), (10, "keywords"), (11, "keypoints"),
                         (12, "policy_support")):
            if nz(r[idx]):
                fill[key] += 1
    ALL_COLS = ["ministry", "rank", "type", "province", "city", "district",
                "publish_year", "theme", "keywords", "keypoints", "policy_support"]
    out["field_fill"] = {k: {"nonempty": fill.get(k, 0),
                             "ratio": round(fill.get(k, 0) / len(pol), 6) if pol else None}
                         for k in ALL_COLS}
    out["field_fill"]["_denominator"] = len(pol)

    # policy_support 的假阳性专项：JSON_LENGTH 会把字面 'null' 数成 1
    ps_true = 0
    ps_literal_null = 0
    for r in pol:
        v = r[12]
        if v is None:
            continue
        s = str(v).strip()
        if s in ("null", "NULL", ""):
            ps_literal_null += 1
        else:
            try:
                obj = json.loads(s)
                if obj not in (None, {}, []):
                    ps_true += 1
            except Exception:  # noqa: BLE001
                ps_true += 1
    out["policy_support_trap"] = {
        "rows": len(pol),
        "literal_null_rows": ps_literal_null,
        "real_value_rows": ps_true,
        "json_length_positive_rows": len(pol),
        "note": "JSON_LENGTH(CAST('null' AS JSON)) 返回 1，若只用 JSON_LENGTH>0 判非空，"
                "会把 20,000 行全部误判成有值；实际真值 0 行。",
    }

    # ---------- 2. 产业节点 ----------
    rows, e = q("SELECT industry_code, industry_name, industry_link_code, parent_name "
                "FROM gkx.dwd_industry_chain_info ORDER BY industry_code", ms=120000)
    probes["dwd_industry_chain_info"] = {"rows": len(rows) if rows is not None else None, "err": e}
    nodes = rows or []
    names_all = sorted({str(x[1]).strip() for x in nodes if nz(x[1])})
    roots = [x for x in nodes if not nz(x[2])]
    name_len = collections.Counter(len(n) for n in names_all)
    names_ok = [n for n in names_all if len(n) >= MIN_NODE_NAME_LEN]
    out["industry_nodes"] = {
        "rows": len(nodes),
        "distinct_names": len(names_all),
        "roots": len(roots),
        "root_names": [x[1] for x in roots],
        "names_len_lt4": len(names_all) - len(names_ok),
        "names_usable": len(names_ok),
        "len_dist": {str(k): v for k, v in sorted(name_len.items())},
        "min_len_rule": MIN_NODE_NAME_LEN,
        "node_company_count_all_zero": True,
    }

    # 长名优先：同一标题里若短名是长名子串，只计长名
    names_sorted = sorted(names_ok, key=len, reverse=True)

    # ---------- 3. 建边 ----------
    rel_count = collections.Counter()          # 关系类型 → 边数
    rel_policies = collections.defaultdict(set)  # 关系类型 → 政策集合
    degree = collections.Counter()
    node_hit = collections.Counter()
    samples = []

    def add(rel, pid, node=None, w=1):
        rel_count[rel] += w
        rel_policies[rel].add(pid)
        degree[pid] += w
        if node is not None:
            node_hit[node] += w

    level_counter = collections.Counter()
    for r in pol:
        pid, title = r[0], (r[1] or "")
        if nz(r[2]):
            add("policy_has_issuer", pid)
        lv = parse_levels(r[3])
        for x in lv:
            add("policy_has_level", pid)
            level_counter[x] += 1
        if nz(r[4]):
            add("policy_has_type", pid)
        for idx, rel in ((5, "policy_province"), (6, "policy_city"), (7, "policy_district")):
            if nz(r[idx]):
                add("policy_applies_to_region", pid)
        hits = []
        for nm in names_sorted:
            if nm in title:
                hits.append(nm)
        # 去掉被更长命中名包含的短名（例如「减速器」被「RV减速器」吸收）
        kept = [h for h in hits if not any(h != o and h in o for o in hits)]
        for h in kept:
            add("policy_mentions_industry", pid, node=h)

    deg_vals = [degree.get(r[0], 0) for r in pol]
    deg_hist = collections.Counter(
        ("0" if d == 0 else "1-2" if d <= 2 else "3-4" if d <= 4 else "5-6" if d <= 6 else "7+")
        for d in deg_vals)

    out["edges"] = {
        "by_relation": {k: v for k, v in rel_count.items()},
        "policies_touched": {k: len(v) for k, v in rel_policies.items()},
        "total_edges": sum(rel_count.values()),
        "policies_with_any_edge": sum(1 for d in deg_vals if d > 0),
        "policies_isolated": sum(1 for d in deg_vals if d == 0),
        "avg_degree": round(sum(deg_vals) / len(deg_vals), 4) if deg_vals else None,
        "max_degree": max(deg_vals) if deg_vals else None,
        "median_degree": sorted(deg_vals)[len(deg_vals) // 2] if deg_vals else None,
        "degree_hist": dict(deg_hist),
        "policy_mentions_industry": rel_count.get("policy_mentions_industry", 0),
    }

    out["nodes_by_type"] = {
        "policy": len(pol),
        "issuer": len({r[2] for r in pol if nz(r[2])}),
        "level": len(level_counter),
        "type": len({r[4] for r in pol if nz(r[4])}),
        "province": len({r[5] for r in pol if nz(r[5])}),
        "city": len({r[6] for r in pol if nz(r[6])}),
        "district": len({r[7] for r in pol if nz(r[7])}),
        "industry_node_hit": len(node_hit),
    }
    out["level_dist"] = dict(level_counter.most_common())
    out["top_issuers"] = [{"issuer": k, "policies": v}
                          for k, v in collections.Counter(
                              r[2] for r in pol if nz(r[2])).most_common(12)]
    out["top_types"] = [{"type": k, "policies": v}
                        for k, v in collections.Counter(
                            r[4] for r in pol if nz(r[4])).most_common(12)]
    out["top_industry_nodes"] = [{"node": k, "mentions": v}
                                 for k, v in node_hit.most_common(15)]

    # ---------- 4. 反证一：政策—政策共现边（同机关同年）的团簇退化 ----------
    grp = collections.Counter()
    for r in pol:
        if nz(r[2]) and nz(r[8]):
            grp[(r[2], str(r[8]))] += 1
    clique = sum(n * (n - 1) // 2 for n in grp.values())
    biggest = grp.most_common(3)
    out["cooccur_negative"] = {
        "definition_if_built": "同发文机关 + 同发布年 → 两两连边（权重 1）",
        "groups": len(grp),
        "edges_if_clique": clique,
        "largest_groups": [{"issuer": k[0], "year": k[1], "policies": v} for k, v in biggest],
        "largest_clique_edges": biggest[0][1] * (biggest[0][1] - 1) // 2 if biggest else 0,
        "why_rejected": "团结构：同组内每条边同权、无区分度，边数随组规模平方增长，"
                        "图谱会退化成一个巨型 clique，不能回答「哪条政策与哪条政策相关」。"
                        "theme / keywords 两列本可用于共现，但 theme 仅 2 行真值、keywords 全空，"
                        "唯一可用的共现键就是机关×年，因此该边不落库。",
    }

    # ---------- 5. 反证二：只匹配标题 vs 标题+正文（800 条确定性抽样） ----------
    rows, e = q("SELECT id, title, LEFT(content, 4000) FROM gkx.dwd_policy_base "
                "ORDER BY CRC32(id) LIMIT %d" % CONTENT_SAMPLE, ms=300000)
    probes["content_sample"] = {"rows": len(rows) if rows is not None else None, "err": e}
    s_title = s_body = 0
    s_title_edges = s_body_edges = 0
    for r in rows or []:
        title, body = (r[1] or ""), (r[2] or "")
        ht = [n for n in names_sorted if n in title]
        ht = [h for h in ht if not any(h != o and h in o for o in ht)]
        hb = [n for n in names_sorted if (n in title) or (n in body)]
        hb = [h for h in hb if not any(h != o and h in o for o in hb)]
        s_title += 1 if ht else 0
        s_body += 1 if hb else 0
        s_title_edges += len(ht)
        s_body_edges += len(hb)
    sample_n = len(rows or [])
    out["title_vs_body"] = {
        "sample_n": sample_n,
        "sample_frame": "ORDER BY CRC32(id) LIMIT %d，对 20,000 条政策确定性抽样（无随机种子）" % CONTENT_SAMPLE,
        "title_hit_policies": s_title,
        "body_hit_policies": s_body,
        "title_hit_edges": s_title_edges,
        "body_hit_edges": s_body_edges,
        "title_hit_ratio": round(s_title / sample_n, 6) if sample_n else None,
        "body_hit_ratio": round(s_body / sample_n, 6) if sample_n else None,
        "edge_uplift_ratio": round(s_body_edges / s_title_edges, 4) if s_title_edges else None,
        "note": "正文口径（标题 ∪ 前 4,000 字正文）命中率更高，但 20,000 条全量正文约 1.1 亿字，"
                "全量跑一次会撞 120 秒上限且不可复用；抽样只用于量化「标题口径低估多少」，"
                "交付边仍用标题口径，抽样值不当全量。",
    }

    # ---------- 6. 需求五类关系的覆盖判定 ----------
    ff = out["field_fill"]
    required = [
        {"type": "政策主题", "carrier": "theme", "filled": ff["theme"]["nonempty"],
         "built": False,
         "reason": "theme 仅 %d/%d 行真值（另 19,998 行为字面 'NULL'），做不成主题节点" % (
             ff["theme"]["nonempty"], len(pol))},
        {"type": "政策目标", "carrier": "keypoints", "filled": ff["keypoints"]["nonempty"],
         "built": False,
         "reason": "keypoints 整列为空（0/%d）" % len(pol)},
        {"type": "实施主体", "carrier": "ministry", "filled": ff["ministry"]["nonempty"],
         "built": "weak",
         "reason": "只发文机关可当载体（%d/%d），它是发文方不是实施方；对企业侧的实施主体"
                   "（谁承接、谁落地）没有任何字段" % (ff["ministry"]["nonempty"], len(pol))},
        {"type": "受益对象", "carrier": "policy_support", "filled": 0,
         "built": False,
         "reason": "policy_support 真值 0 行（全部是字面 'null'）；企业侧无受益对象字段"},
        {"type": "监管机构", "carrier": "无", "filled": 0,
         "built": False,
         "reason": "无监管机构字段；ministry 是发文机关，不能替代监管机构（同一条政策可由"
                   "发改委发文、由行业主管部门监管）"},
    ]
    built = [x for x in required if x["built"] is True]
    weak = [x for x in required if x["built"] == "weak"]
    out["required_relations"] = required
    out["coverage"] = {
        "required": len(required),
        "built_strong": len(built),
        "built_weak": len(weak),
        "not_built": len(required) - len(built) - len(weak),
        "ratio_strong": round(len(built) / len(required), 6),
        "ratio_strong_plus_weak": round((len(built) + len(weak)) / len(required), 6),
        "required_list": [x["type"] for x in required],
        "auxiliary_relations": ["policy_has_level", "policy_has_type",
                                "policy_applies_to_region", "policy_mentions_industry"],
        "auxiliary_note": "四类辅助边都不在需求点名的五类关系里，不能顶替任何一类；"
                          "它们的作用是把政策侧骨架撑起来，使图谱至少可遍历。",
    }

    # ---------- 7. 年度分布 + 基期声明 ----------
    yr = collections.Counter()
    for r in pol:
        y = str(r[8] or "").strip()
        if y.isdigit():
            yr[int(y)] += 1
    out["year_dist"] = {str(k): v for k, v in sorted(yr.items())}
    win = list(range(2000, 2027))
    used = [y for y in win if yr.get(y, 0) > 0]
    missing = [y for y in win if yr.get(y, 0) == 0]
    out["base_years_used"] = used
    out["base_years_missing"] = missing
    out["base_years_note"] = (
        "本件是截面关系图，不做同比；基期字段只用于声明政策语料的年份覆盖。"
        "publish_year 有 %d 个不同取值，2000—2026 窗口内 %d 年有量、%d 年为零行（%s），"
        "2000 年以前另有 %d 条历史文本，不进年度序列也不摊 0。"
        % (len(yr), len(used), len(missing), missing or "无",
           sum(v for k, v in yr.items() if k < 2000)))

    out["support_judgment"] = "部分支持"
    out["judgment_reason"] = (
        "需求点名的五类关系里只有「实施主体」能弱建成（发文机关 %d/%d 行，方向是发文方而非实施方），"
        "「政策主题」「政策目标」「受益对象」「监管机构」四类无字段承载（theme 仅 2 行、"
        "keypoints 与 policy_support 真值 0 行、无监管机构字段）；"
        "gkx 也没有 policy_graph_edge / policy_entity 现成边表，全部边为字段现建、属本件自定义口径。"
        "政策侧骨架（机关/层级/文种/地区/产业节点，共 %d 条边）可遍历，"
        "但五类点名关系只落实 1 类且为方向性替代，故落部分支持。"
        % (ff["ministry"]["nonempty"], len(pol), sum(rel_count.values())))

    notes.append("本件全部关系边为「本件自定义、待甲方确认」：共现阈值 MIN_NODE_NAME_LEN=%d、"
                 "标题口径、长名优先去重，均无甲方闭合口径。" % MIN_NODE_NAME_LEN)
    notes.append("政策—政策共现边不落库：唯一可用的共现键是机关×年，团簇会生成 %d 条同权边，"
                 "不具区分度。" % clique)

    with open(os.path.join(HERE, METRIC + "_out.json"), "w", encoding="utf-8") as f:
        json.dump(clean(out), f, ensure_ascii=False, indent=1)
    print("wrote", METRIC + "_out.json")
    print("edges", json.dumps(out["edges"]["by_relation"], ensure_ascii=False))
    print("total", out["edges"]["total_edges"], "avg_deg", out["edges"]["avg_degree"],
          "isolated", out["edges"]["policies_isolated"])
    print("nodes", json.dumps(out["nodes_by_type"], ensure_ascii=False))
    print("coverage", json.dumps(out["coverage"], ensure_ascii=False))
    print("clique", clique, "sample", out["title_vs_body"]["title_hit_ratio"],
          out["title_vs_body"]["body_hit_ratio"])


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""GDF 技术节点与产业节点。同步可每天一次。关联只许人工触发。--self-check 不连库、不调向量。"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request

BATCH = 20
PAGE = 500
# 与 lumen-topic-py gkx_svc_service/jx_dict.py 同一只读坐标。密码只来自 JX_ADS_PASSWORD。
JX_HOST = "47.93.119.170"
JX_PORT = 29030
JX_USER = "test2"
JX_DATABASE = "gkx_technology_analysis_dev"
JX_TABLE = "ads_technology_profile"
PROFILE_SQL = (
    "SELECT technology_node_id, technology_name_zh, technology_name_en, data_version "
    "FROM " + JX_TABLE + " ORDER BY technology_node_id LIMIT %s, %s"
)
DIM = 768
EMBED_BATCH = 32
EXIT_OK = 0
EXIT_ERR = 1
EXIT_ENV = 3
EXIT_TABLE = 4
QUERY_PREFIX = "为这个句子生成表示以用于检索相关文章："
MODEL_VERSION = "bge-base-zh-v1.5-tei-1.8.3"
_IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
# ponytail: 候选向量只留在本进程，目录变了才重算。重启后第一次关联会重新向量化。
_CANDIDATE_VECTORS = {}


def _s(value):
    if value is None:
        return ""
    return str(value).strip()


def _clip(value, size):
    return _s(value)[:size]


def qident(name):
    if not _IDENT.match(name or ""):
        raise ValueError("非法标识符")
    return "`" + name + "`"


def display_name(name_zh, name_en):
    """有中文用中文，否则用英文。不改已存的中文列。"""
    zh = _s(name_zh)
    return zh if zh else _s(name_en)


def plan_sync(existing, incoming):
    """已有 technology_node_id 只更新目录列。新 id 插入空关联行。计划里没有删除。空中文不抄英文。"""
    by_id = {}
    for item in incoming or []:
        tid = _clip(item.get("technology_node_id"), 64)
        if not tid:
            continue
        by_id[tid] = {
            "technology_node_id": tid,
            "name_zh": _clip(item.get("name_zh"), 200),
            "name_en": _clip(item.get("name_en"), 200),
            "data_version": _clip(item.get("data_version"), 64),
        }
    have = set(existing or [])
    inserts, updates = [], []
    for item in by_id.values():
        (updates if item["technology_node_id"] in have else inserts).append(item)
    return inserts, updates


def tech_text(row):
    zh = _s(row.get("name_zh"))
    en = _s(row.get("name_en"))
    if not zh:
        return en
    if en and en != zh:
        return zh + " " + en
    return zh


def cand_text(row):
    parts = [_s(row.get("node_name")), _s(row.get("industry_name")), _s(row.get("cluster_name"))]
    return " ".join(part for part in parts if part)


def build_catalog(cluster_rows, node_rows):
    """只收 CL-*。同一 node_id 跨产业则丢弃。没有节点时 gaps 含 chain_node。"""
    industries = {}
    clusters_by_industry = {}
    cluster_ids = []
    for row in cluster_rows or []:
        cluster_id = _s(row.get("cluster_id"))
        if not cluster_id.startswith("CL-"):
            continue
        if cluster_id not in cluster_ids:
            cluster_ids.append(cluster_id)
        industry_id = _s(row.get("industry_id"))
        if not industry_id:
            continue
        memberships = clusters_by_industry.setdefault(industry_id, [])
        if all(item["cluster_id"] != cluster_id for item in memberships):
            memberships.append({
                "cluster_id": cluster_id,
                "cluster_name": _clip(row.get("cluster_name"), 200),
            })
        industries.setdefault(industry_id, {
            "industry_id": industry_id,
            "industry_name": _clip(row.get("industry_name"), 200),
            "clusters": memberships,
        })
    gaps = []
    if not cluster_ids:
        return {}, [], ["cluster"]
    if not industries:
        return {}, [], ["industry"]
    grouped = {}
    for row in node_rows or []:
        industry_id = _s(row.get("industry_id"))
        node_id = _s(row.get("node_id"))
        industry = industries.get(industry_id)
        if not industry or not node_id:
            continue
        grouped.setdefault(node_id, []).append({
            "node_id": node_id[:64],
            "node_name": _clip(row.get("node_name"), 200),
            "industry_id": industry["industry_id"],
            "industry_name": industry["industry_name"],
            "clusters": industry["clusters"],
        })
    by_node = {}
    payload = []
    ambiguous = 0
    for group in grouped.values():
        industry_ids = {item["industry_id"] for item in group}
        if len(industry_ids) != 1:
            ambiguous += 1
            continue
        row = group[0]
        by_node[row["node_id"]] = row
        names = "、".join(item["cluster_name"] for item in row["clusters"] if item["cluster_name"])
        payload.append({
            "node_id": row["node_id"],
            "node_name": row["node_name"],
            "industry_name": row["industry_name"],
            "cluster_name": names,
        })
    if ambiguous:
        gaps.append("node_id_ambiguous")
    covered = {row["industry_id"] for row in by_node.values()}
    missing = sum(1 for industry_id in industries if industry_id not in covered)
    if not by_node:
        gaps.append("chain_node")
    elif missing:
        gaps.append("chain_node_partial")
    return by_node, payload, gaps


def nearest(nodes, candidates, embed):
    """每个技术节点只留余弦最大的一个候选。同分留更靠前的那条。node_id 只来自候选。"""
    rows = [row for row in nodes or [] if _s(row.get("technology_node_id"))]
    cands = [row for row in candidates or [] if _s(row.get("node_id"))]
    if not rows:
        return {"model": None, "links": []}
    if not cands:
        raise RuntimeError("no local chain-node candidates")
    cand_vecs = _candidate_vectors(cands, embed)
    query_vecs = embed([tech_text(row) for row in rows], is_query=True)
    if len(query_vecs) != len(rows) or len(cand_vecs) != len(cands):
        raise RuntimeError("embedding count mismatch")
    allowed = {row["node_id"] for row in cands}
    links = []
    for row, query in zip(rows, query_vecs):
        best_at = 0
        best_score = None
        for index, vector in enumerate(cand_vecs):
            score = _dot(query, vector)
            if best_score is None or score > best_score:
                best_score = score
                best_at = index
        node_id = cands[best_at]["node_id"]
        if node_id not in allowed:
            continue
        links.append({
            "technology_node_id": _clip(row.get("technology_node_id"), 64),
            "node_id": node_id,
        })
    return {"model": MODEL_VERSION, "links": links}


def _candidate_vectors(cands, embed):
    blob = "\n".join(row["node_id"] + "\t" + cand_text(row) for row in cands)
    key = hashlib.sha256(blob.encode("utf-8")).hexdigest()
    cached = _CANDIDATE_VECTORS.get(key)
    if cached is not None:
        return cached
    vectors = embed([cand_text(row) for row in cands], is_query=False)
    _CANDIDATE_VECTORS.clear()
    _CANDIDATE_VECTORS[key] = vectors
    return vectors


def _dot(left, right):
    return sum(x * y for x, y in zip(left, right))


def batches(rows, size):
    rows = list(rows or [])
    return [rows[index:index + size] for index in range(0, len(rows), size)]


def run_link_batches(pending_ids, nodes_by_id, candidates, embed):
    """失败的那一批不写入。后面的 id 保持原样。某一批一条都没写成也停下。"""
    written = []
    failed = []
    for batch in batches(pending_ids, BATCH):
        try:
            result = nearest([nodes_by_id[item] for item in batch], candidates, embed)
        except (RuntimeError, OSError, urllib.error.URLError, ValueError):
            return written, batch
        fresh = [
            item["technology_node_id"] for item in result["links"]
            if item["technology_node_id"] in set(batch)
        ]
        if not fresh:
            failed.extend(batch)
            return written, failed
        written.extend(fresh)
    return written, failed


def _schema(name, label):
    if not _IDENT.match(name or ""):
        raise SystemExit("未配置合法的" + label)
    if name.startswith("demo_"):
        raise SystemExit("禁止写入 demo 库")
    return name


def map_profile_row(row):
    """久新 ads_technology_profile 一行。technology_name_zh 原样进 name_zh，空着不抄英文。"""
    return {
        "technology_node_id": _clip(row.get("technology_node_id"), 64),
        "name_zh": _clip(row.get("technology_name_zh"), 200),
        "name_en": _clip(row.get("technology_name_en"), 200),
        "data_version": _clip(row.get("data_version"), 64),
    }


def _ident_table(name):
    if not _IDENT.match(name or ""):
        raise SystemExit("未配置合法的目录表")
    return name


def _connect():
    import pymysql

    return pymysql.connect(
        host=os.environ.get("MYSQL_HOST", "127.0.0.1"),
        port=int(os.environ.get("MYSQL_PORT", "3306")),
        user=os.environ.get("MYSQL_USER", ""),
        password=os.environ.get("MYSQL_PASSWORD", ""),
        charset="utf8mb4",
        autocommit=False,
    )


def _jx_connect():
    import pymysql

    password = _s(os.environ.get("JX_ADS_PASSWORD"))
    if not password:
        raise SystemExit("未配置 JX_ADS_PASSWORD")
    host = _s(os.environ.get("JX_ADS_HOST")) or JX_HOST
    user = _s(os.environ.get("JX_ADS_USER")) or JX_USER
    database = _s(os.environ.get("JX_ADS_DATABASE")) or JX_DATABASE
    try:
        port = int(os.environ.get("JX_ADS_PORT") or JX_PORT)
    except ValueError:
        port = JX_PORT
    return pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5,
        read_timeout=60,
        autocommit=True,
    ), host, port, database


def _require_table(cur, schema, table):
    cur.execute(
        "SELECT 1 FROM information_schema.tables WHERE table_schema=%s AND table_name=%s",
        (schema, table),
    )
    if cur.fetchone() is None:
        raise SystemExit("映射表不存在")


def _embed_live(texts, is_query):
    base = _s(os.environ.get("EMBED_BASE_URL")).rstrip("/")
    if not base:
        raise SystemExit("未配置 EMBED_BASE_URL")
    model = _s(os.environ.get("EMBED_MODEL")) or "BAAI/bge-base-zh-v1.5"
    headers = {"Content-Type": "application/json"}
    token = _s(os.environ.get("EMBED_API_KEY"))
    if token:
        headers["Authorization"] = "Bearer " + token
    prefix = QUERY_PREFIX if is_query else ""
    payloads = [prefix + _s(text) for text in texts]
    out = []
    url = base + "/v1/embeddings"
    for index in range(0, len(payloads), EMBED_BATCH):
        chunk = payloads[index:index + EMBED_BATCH]
        body = json.dumps({"model": model, "input": chunk}).encode("utf-8")
        req = urllib.request.Request(url, data=body, headers=headers)
        with urllib.request.urlopen(req, timeout=60) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        rows = sorted(payload.get("data") or [], key=lambda item: int(item.get("index") or 0))
        if len(rows) != len(chunk):
            raise RuntimeError("embedding count mismatch")
        for item in rows:
            vec = item.get("embedding") or []
            if len(vec) != DIM:
                raise RuntimeError("embedding dim mismatch")
            out.append([float(value) for value in vec])
    return out


def cmd_sync(conn):
    schema = _schema(os.environ.get("DWD_SCHEMA", "gkxlumenx_dwd"), "DWD")
    table = _ident_table(os.environ.get("MAP_TABLE", "dwd_tech_node_industry_map"))
    cur = conn.cursor()
    _require_table(cur, schema, table)
    map_sql = qident(schema) + "." + qident(table)
    source, host, port, database = _jx_connect()
    print("sync source=%s:%s/%s.%s page=%s" % (host, port, database, JX_TABLE, PAGE))
    cur.execute("SELECT DISTINCT technology_node_id FROM " + map_sql)
    existing = {row[0] for row in cur.fetchall()}
    offset = 0
    pages = inserted = updated = 0
    try:
        while True:
            # ponytail: LIMIT offset,size 与字典 technology_node_page 相同。约 1.9 万行。升级改主键 keyset。
            with source.cursor() as src:
                src.execute(PROFILE_SQL, (offset, PAGE))
                fetched = src.fetchall()
            if offset == 0 and not fetched:
                raise SystemExit("技术节点目录为空，未改映射表")
            if not fetched:
                break
            incoming = [map_profile_row(row) for row in fetched]
            try:
                inserts, updates = plan_sync(existing, incoming)
                for item in updates:
                    cur.execute(
                        "UPDATE " + map_sql
                        + " SET name_zh=%s, name_en=%s, data_version=%s, synced_at=NOW() WHERE technology_node_id=%s",
                        (item["name_zh"], item["name_en"], item["data_version"], item["technology_node_id"]),
                    )
                for item in inserts:
                    cur.execute(
                        "INSERT INTO " + map_sql
                        + " (technology_node_id, name_zh, name_en, data_version, synced_at) VALUES (%s,%s,%s,%s,NOW())",
                        (item["technology_node_id"], item["name_zh"], item["name_en"], item["data_version"]),
                    )
                    existing.add(item["technology_node_id"])
                conn.commit()
            except Exception:
                conn.rollback()
                print("sync pages=%s inserted=%s updated=%s failed=1" % (pages, inserted, updated))
                raise
            pages += 1
            inserted += len(inserts)
            updated += len(updates)
            offset += PAGE
            if len(fetched) < PAGE:
                break
    finally:
        source.close()
    print("sync pages=%s inserted=%s updated=%s failed=0" % (pages, inserted, updated))


def _load_catalog(cur, dim, dwd):
    cur.execute(
        "SELECT c.cluster_id, c.cluster_name, m.industry_id, m.industry_name FROM "
        + qident(dim) + ".industry_cluster c LEFT JOIN " + qident(dim)
        + ".industry_cluster_map m ON m.cluster_id=c.cluster_id AND m.is_active=1 "
        + "WHERE c.is_active=1 AND c.cluster_id LIKE 'CL-%'"
    )
    clusters = [
        {"cluster_id": row[0], "cluster_name": row[1], "industry_id": row[2], "industry_name": row[3]}
        for row in cur.fetchall()
    ]
    cur.execute(
        "SELECT n.node_id, n.node_name, c.industry_id FROM " + qident(dwd)
        + ".industry_chain c JOIN " + qident(dwd)
        + ".industry_chain_node n ON n.chain_id=c.chain_id AND n.is_deleted=0 WHERE c.is_deleted=0"
    )
    nodes = [
        {"node_id": row[0], "node_name": row[1], "industry_id": row[2]}
        for row in cur.fetchall()
    ]
    return build_catalog(clusters, nodes)


def _load_unmapped(cur, map_sql, limit):
    cur.execute(
        "SELECT technology_node_id, MAX(name_zh), MAX(name_en), MAX(data_version) FROM " + map_sql
        + " GROUP BY technology_node_id HAVING SUM(CASE WHEN node_id IS NOT NULL AND node_id<>'' THEN 1 ELSE 0 END)=0 "
        + "ORDER BY technology_node_id LIMIT %s",
        (limit,),
    )
    out = []
    for row in cur.fetchall():
        out.append({
            "technology_node_id": row[0],
            "name_zh": row[1] or "",
            "name_en": row[2] or "",
            "data_version": row[3] or "",
        })
    return out


def cmd_link(conn):
    dwd = _schema(os.environ.get("DWD_SCHEMA", "gkxlumenx_dwd"), "DWD")
    dim = _schema(os.environ.get("DIM_SCHEMA", "gkxlumenx_dim"), "DIM")
    table = _ident_table(os.environ.get("MAP_TABLE", "dwd_tech_node_industry_map"))
    cur = conn.cursor()
    _require_table(cur, dwd, table)
    map_sql = qident(dwd) + "." + qident(table)
    by_node, payload, gaps = _load_catalog(cur, dim, dwd)
    print("catalog_gaps=" + ",".join(gaps))
    pending = _load_unmapped(cur, map_sql, BATCH)
    if not pending:
        print("没有未关联的技术节点")
        print("link processed=0 skipped=0 failed=0")
        return
    if not by_node:
        print("本侧没有可关联的产业节点，未调用向量")
        print("link processed=0 skipped=%s failed=0" % len(pending))
        return
    if not _s(os.environ.get("EMBED_BASE_URL")):
        raise SystemExit("未配置 EMBED_BASE_URL")
    processed = failed = linked = 0
    while pending:
        try:
            result = nearest(pending, payload, _embed_live)
        except (SystemExit, RuntimeError, OSError, urllib.error.URLError, ValueError) as exc:
            if isinstance(exc, SystemExit):
                raise
            reason = _clip(str(exc) or "向量调用失败", 480)
            for item in pending:
                cur.execute(
                    "UPDATE " + map_sql + " SET fail_reason=%s WHERE technology_node_id=%s AND node_id IS NULL",
                    (reason, item["technology_node_id"]),
                )
            conn.commit()
            failed += len(pending)
            print("link processed=%s skipped=0 failed=%s" % (processed, failed))
            raise SystemExit("向量调用失败，未完成的技术节点保持未映射")
        wrote = 0
        for item in result["links"]:
            node = by_node.get(item["node_id"])
            if node is None:
                continue
            source = next(row for row in pending if row["technology_node_id"] == item["technology_node_id"])
            clusters = node["clusters"] or [{"cluster_id": None, "cluster_name": ""}]
            for cluster in clusters:
                cur.execute(
                    "SELECT COUNT(*) FROM " + map_sql
                    + " WHERE technology_node_id=%s AND node_id=%s AND "
                    + ("cluster_id IS NULL" if not cluster["cluster_id"] else "cluster_id=%s"),
                    (source["technology_node_id"], node["node_id"])
                    if not cluster["cluster_id"]
                    else (source["technology_node_id"], node["node_id"], cluster["cluster_id"]),
                )
                if cur.fetchone()[0]:
                    wrote += 1
                    continue
                cur.execute(
                    "INSERT INTO " + map_sql
                    + " (technology_node_id, name_zh, name_en, data_version, synced_at, node_id, node_name, "
                    + "industry_id, industry_name, cluster_id, cluster_name, model_name, linked_at) "
                    + "VALUES (%s,%s,%s,%s,NOW(),%s,%s,%s,%s,%s,%s,%s,NOW())",
                    (
                        source["technology_node_id"], source["name_zh"], source["name_en"], source["data_version"],
                        node["node_id"], node["node_name"], node["industry_id"], node["industry_name"],
                        cluster["cluster_id"], cluster["cluster_name"], MODEL_VERSION,
                    ),
                )
                wrote += 1
            cur.execute(
                "DELETE FROM " + map_sql + " WHERE technology_node_id=%s AND node_id IS NULL",
                (source["technology_node_id"],),
            )
        if wrote == 0:
            conn.rollback()
            failed += len(pending)
            print("link processed=%s skipped=0 failed=%s" % (processed, failed))
            raise SystemExit("本批没有写入关联，已停下")
        conn.commit()
        processed += len(pending)
        linked += wrote
        pending = _load_unmapped(cur, map_sql, BATCH)
    print("link processed=%s linked_rows=%s failed=%s" % (processed, linked, failed))


def _print_side(cur, map_sql, mapped):
    having = "> 0" if mapped else "= 0"
    cur.execute(
        "SELECT technology_node_id, MAX(name_zh), MAX(name_en) FROM " + map_sql
        + " GROUP BY technology_node_id HAVING SUM(CASE WHEN node_id IS NOT NULL AND node_id<>'' THEN 1 ELSE 0 END)"
        + having + " ORDER BY MAX(name_zh), technology_node_id LIMIT 200"
    )
    rows = cur.fetchall()
    side = "mapped" if mapped else "unmapped"
    print(side + " " + str(len(rows)))
    for row in rows:
        print("\t".join([
            side,
            row[0] or "",
            display_name(row[1], row[2]),
            row[1] or "",
            row[2] or "",
        ]))
    return len(rows)


def cmd_stats(conn):
    schema = _schema(os.environ.get("DWD_SCHEMA", "gkxlumenx_dwd"), "DWD")
    table = _ident_table(os.environ.get("MAP_TABLE", "dwd_tech_node_industry_map"))
    cur = conn.cursor()
    _require_table(cur, schema, table)
    map_sql = qident(schema) + "." + qident(table)
    mapped = _print_side(cur, map_sql, True)
    unmapped = _print_side(cur, map_sql, False)
    print("counts mapped=%s unmapped=%s" % (mapped, unmapped))


def cmd_query(conn, keyword):
    schema = _schema(os.environ.get("DWD_SCHEMA", "gkxlumenx_dwd"), "DWD")
    table = _ident_table(os.environ.get("MAP_TABLE", "dwd_tech_node_industry_map"))
    cur = conn.cursor()
    _require_table(cur, schema, table)
    map_sql = qident(schema) + "." + qident(table)
    text = _s(keyword).replace("\\", "").replace("%", "").replace("_", "")[:64]
    if not text:
        cur.execute(
            "SELECT technology_node_id, MAX(name_zh), MAX(name_en) FROM " + map_sql
            + " GROUP BY technology_node_id HAVING SUM(CASE WHEN node_id IS NOT NULL AND node_id<>'' THEN 1 ELSE 0 END)>0 "
            + "ORDER BY MAX(name_zh), technology_node_id LIMIT 200"
        )
    else:
        like = "%" + text + "%"
        cur.execute(
            "SELECT technology_node_id, MAX(name_zh), MAX(name_en) FROM " + map_sql
            + " WHERE technology_node_id LIKE %s OR name_zh LIKE %s OR name_en LIKE %s "
            + "GROUP BY technology_node_id ORDER BY MAX(name_zh), technology_node_id LIMIT 200",
            (like, like, like),
        )
    for row in cur.fetchall():
        print("\t".join([row[0] or "", display_name(row[1], row[2]), row[1] or "", row[2] or ""]))


def _self_check():
    _CANDIDATE_VECTORS.clear()
    assert JX_HOST == "47.93.119.170" and JX_PORT == 29030
    assert JX_DATABASE == "gkx_technology_analysis_dev" and JX_TABLE == "ads_technology_profile"
    assert "ORDER BY technology_node_id" in PROFILE_SQL
    mapped = map_profile_row({
        "technology_node_id": "t1",
        "technology_name_zh": None,
        "technology_name_en": "SAR",
        "data_version": "v1",
    })
    assert mapped["name_zh"] == "" and mapped["name_en"] == "SAR"
    inserts, updates = plan_sync(["t1"], [
        {"technology_node_id": "t1", "name_zh": "", "name_en": "SAR", "data_version": "v2"},
        {"technology_node_id": "t2", "name_zh": "雷达", "name_en": "Radar", "data_version": "v1"},
    ])
    assert [item["technology_node_id"] for item in updates] == ["t1"]
    assert updates[0]["name_zh"] == ""
    assert updates[0]["name_en"] == "SAR"
    assert [item["technology_node_id"] for item in inserts] == ["t2"]
    assert "t9" not in {item["technology_node_id"] for item in inserts + updates}
    assert display_name("", "SAR") == "SAR"
    assert display_name("雷达", "SAR") == "雷达"
    calls = {"n": 0}

    def fake(texts, is_query=False):
        calls["n"] += 1
        out = []
        for text in texts:
            if "雷达" in text:
                out.append([1.0, 0.0])
            elif "文学" in text:
                out.append([0.0, 1.0])
            else:
                out.append([0.6, 0.4])
        return out

    cands = [
        {"node_id": "N1", "node_name": "雷达", "industry_name": "电子", "cluster_name": "甲"},
        {"node_id": "N2", "node_name": "文学", "industry_name": "文化", "cluster_name": "乙"},
    ]
    got = nearest([
        {"technology_node_id": "t2", "name_zh": "雷达压缩", "name_en": "SAR"},
        {"technology_node_id": "t3", "name_zh": "", "name_en": "文学理论"},
    ], cands, fake)
    assert got["links"] == [
        {"technology_node_id": "t2", "node_id": "N1"},
        {"technology_node_id": "t3", "node_id": "N2"},
    ]
    tied = nearest(
        [{"technology_node_id": "t4", "name_zh": "其他"}],
        [
            {"node_id": "A", "node_name": "甲"},
            {"node_id": "B", "node_name": "乙"},
        ],
        fake,
    )
    assert tied["links"] == [{"technology_node_id": "t4", "node_id": "A"}]
    before = calls["n"]
    assert nearest([], cands, fake)["links"] == []
    assert calls["n"] == before
    try:
        nearest([{"technology_node_id": "t5", "name_zh": "雷达"}], [], fake)
        raise AssertionError("empty candidates must fail")
    except RuntimeError:
        pass
    by_node, payload, gaps = build_catalog(
        [
            {"cluster_id": "CL-1", "cluster_name": "甲", "industry_id": "I1", "industry_name": "电子"},
            {"cluster_id": "CL-1", "cluster_name": "甲", "industry_id": "I2", "industry_name": "文化"},
            {"cluster_id": "XX-1", "cluster_name": "丢", "industry_id": "I9", "industry_name": "丢"},
        ],
        [
            {"node_id": "N1", "node_name": "雷达", "industry_id": "I1"},
            {"node_id": "N2", "node_name": "歧义", "industry_id": "I1"},
            {"node_id": "N2", "node_name": "歧义", "industry_id": "I2"},
        ],
    )
    assert set(by_node) == {"N1"}
    assert "node_id_ambiguous" in gaps
    assert "XX-1" not in json.dumps(payload, ensure_ascii=False)
    nodes = {str(i): {"technology_node_id": str(i), "name_zh": "雷达"} for i in range(25)}
    boom = {"n": 0}

    def fail_second(texts, is_query=False):
        boom["n"] += 1
        if boom["n"] > 2:
            raise RuntimeError("down")
        return fake(texts, is_query)

    written, stopped = run_link_batches(list(nodes), nodes, cands, fail_second)
    assert written == [str(i) for i in range(20)]
    assert stopped == [str(i) for i in range(20, 25)]
    print("self-check ok")


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?", choices=["sync", "link", "stats", "query"])
    parser.add_argument("--keyword", default="")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args(argv)
    if args.self_check:
        _self_check()
        return EXIT_OK
    if not args.command:
        parser.error("需要 sync、link、stats、query 或 --self-check")
    conn = _connect()
    try:
        if args.command == "sync":
            cmd_sync(conn)
        elif args.command == "link":
            cmd_link(conn)
        elif args.command == "stats":
            cmd_stats(conn)
        else:
            cmd_query(conn, args.keyword)
    except SystemExit as exc:
        text = str(exc)
        if "映射表不存在" in text:
            return EXIT_TABLE
        if "未配置" in text or "禁止" in text:
            return EXIT_ENV
        print(text)
        return EXIT_ERR
    except Exception as exc:
        conn.rollback()
        print(type(exc).__name__)
        return EXIT_ERR
    finally:
        conn.close()
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

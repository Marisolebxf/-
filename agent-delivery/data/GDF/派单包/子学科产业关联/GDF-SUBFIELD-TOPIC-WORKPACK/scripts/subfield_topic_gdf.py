# -*- coding: utf-8 -*-
"""GDF 子学科与产业节点。同步、关联都要人触发。--self-check 不连库、不调模型。"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

BATCH = 20
EXIT_OK = 0
EXIT_ERR = 1
EXIT_ENV = 3
EXIT_TABLE = 4
_IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_SYSTEM = (
    "你把学术子学科对应到给定的产业节点。"
    "只能使用候选清单中的 node_id，禁止编造。"
    "对不上的子学科不要输出。"
    "一个子学科可以对应多个节点。"
    '只输出 JSON：{"links":[{"subfield_id":"...","node_id":"..."}]}'
)


def _s(value):
    if value is None:
        return ""
    return str(value).strip()


def _clip(value, size):
    text = _s(value)
    return text[:size]


def qident(name):
    if not _IDENT.match(name or ""):
        raise ValueError("非法标识符")
    return "`" + name + "`"


def plan_sync(existing, incoming):
    """已有 subfield_id 只更新目录列。新 id 插入空关联行。计划里没有删除。"""
    by_id = {}
    for item in incoming or []:
        sid = _s(item.get("subfield_id"))
        if sid:
            by_id[sid] = {
                "subfield_id": sid[:64],
                "name_zh": _clip(item.get("name_zh") or item.get("name"), 200),
                "data_version": _clip(item.get("data_version"), 64),
            }
    have = set(existing or [])
    inserts, updates = [], []
    for item in by_id.values():
        (updates if item["subfield_id"] in have else inserts).append(item)
    return inserts, updates


def accept_links(raw, pending_ids, candidate_ids):
    pending = set(pending_ids or [])
    nodes = set(candidate_ids or [])
    links, rejected, seen = [], [], set()
    for item in raw or []:
        if not isinstance(item, dict):
            continue
        sid = _s(item.get("subfield_id"))[:64]
        nid = _s(item.get("node_id"))[:64]
        if not sid or sid not in pending:
            continue
        if not nid or nid not in nodes:
            rejected.append({"subfield_id": sid, "node_id": nid, "reason": "not_in_candidates"})
            continue
        key = (sid, nid)
        if key in seen:
            continue
        seen.add(key)
        links.append({"subfield_id": sid, "node_id": nid})
    return links, rejected


def batches(items, size=BATCH):
    step = size if size >= 1 else 1
    return [items[i:i + step] for i in range(0, len(items or []), step)]


def build_catalog(cluster_rows, node_rows):
    """集群只要 CL-*。产业必须挂在这些集群上。同一 node_id 跨产业则整组丢弃。"""
    industries = {}
    cluster_ids = set()
    for row in cluster_rows or []:
        cid = _s(row.get("cluster_id"))
        iid = _s(row.get("industry_id"))
        if not cid.startswith("CL-"):
            continue
        cluster_ids.add(cid)
        if not iid:
            continue
        ind = industries.setdefault(iid, {"name": _s(row.get("industry_name")), "clusters": {}})
        ind["clusters"].setdefault(cid, _s(row.get("cluster_name")))
    gaps = []
    if not cluster_ids:
        return {"gaps": ["cluster"], "nodes": {}, "industries_without_nodes": 0}
    if not industries:
        return {"gaps": ["industry"], "nodes": {}, "industries_without_nodes": 0}
    grouped = {}
    for row in node_rows or []:
        iid = _s(row.get("industry_id"))
        nid = _s(row.get("node_id"))
        if iid not in industries or not nid:
            continue
        grouped.setdefault(nid, []).append(row)
    nodes = {}
    ambiguous = False
    for nid, rows in grouped.items():
        iids = {_s(row.get("industry_id")) for row in rows}
        if len(iids) != 1:
            ambiguous = True
            continue
        row = rows[0]
        iid = _s(row.get("industry_id"))
        ind = industries[iid]
        clusters = list(ind["clusters"].items()) or [(None, "")]
        nodes[nid] = {
            "node_id": nid,
            "node_name": _clip(row.get("node_name"), 200),
            "industry_id": iid,
            "industry_name": _clip(ind["name"], 200),
            "clusters": clusters,
        }
    if ambiguous:
        gaps.append("node_id_ambiguous")
    covered = {node["industry_id"] for node in nodes.values()}
    missing = sum(1 for iid in industries if iid not in covered)
    if not nodes:
        gaps.append("chain_node")
    elif missing:
        gaps.append("chain_node_partial")
    return {"gaps": gaps, "nodes": nodes, "industries_without_nodes": missing}


def split_stats(rows):
    grouped = {}
    for row in rows or []:
        sid = _s(row.get("subfield_id"))
        if not sid:
            continue
        acc = grouped.setdefault(sid, {"subfield_id": sid, "name_zh": "", "mapped": False})
        name = _s(row.get("name_zh"))
        if name:
            acc["name_zh"] = name
        if _s(row.get("node_id")):
            acc["mapped"] = True
    mapped, unmapped = [], []
    for acc in sorted(grouped.values(), key=lambda item: (item["name_zh"], item["subfield_id"])):
        item = {"subfield_id": acc["subfield_id"], "name_zh": acc["name_zh"]}
        (mapped if acc["mapped"] else unmapped).append(item)
    return mapped, unmapped


def include_query(keyword, subfield_id, name_zh, linked):
    text = _s(keyword).lower()
    if not text:
        return linked
    return text in _s(subfield_id).lower() or text in _s(name_zh).lower()


def link_rows(item, node_ids, nodes, model):
    out = []
    for nid in node_ids:
        node = nodes.get(nid)
        if not node:
            continue
        for cid, cname in node["clusters"]:
            out.append({
                "subfield_id": item["subfield_id"],
                "name_zh": item["name_zh"],
                "data_version": item.get("data_version") or "",
                "node_id": node["node_id"],
                "node_name": node["node_name"],
                "industry_id": node["industry_id"],
                "industry_name": node["industry_name"],
                "cluster_id": cid or "",
                "cluster_name": cname or "",
                "model_name": _clip(model, 128),
            })
    return out


def loads_llm(text):
    body = (text or "").strip()
    body = re.sub(r"^```(?:json)?", "", body).strip()
    body = re.sub(r"```$", "", body).strip()
    start, end = body.find("{"), body.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("模型没有返回 JSON")
    data = json.loads(body[start:end + 1])
    if not isinstance(data, dict):
        raise ValueError("模型 JSON 必须是对象")
    return data


def stop_after_failure(done_ids, failed_ids, later_ids):
    """失败批之后的 id 不能算已映射，也不能算本批失败。"""
    return {
        "done": list(done_ids),
        "failed": list(failed_ids),
        "untouched": [sid for sid in later_ids if sid not in done_ids and sid not in failed_ids],
    }


def self_check():
    inserts, updates = plan_sync(["a", "old"], [
        {"subfield_id": "a", "name_zh": "甲"},
        {"subfield_id": "b", "name_zh": "乙"},
    ])
    assert [row["subfield_id"] for row in updates] == ["a"]
    assert [row["subfield_id"] for row in inserts] == ["b"]
    assert "old" not in [row["subfield_id"] for row in inserts + updates]
    links, rejected = accept_links(
        [
            {"subfield_id": "b", "node_id": "n1"},
            {"subfield_id": "b", "node_id": "nope"},
            {"subfield_id": "other", "node_id": "n1"},
        ],
        ["b"],
        ["n1"],
    )
    assert links == [{"subfield_id": "b", "node_id": "n1"}]
    assert rejected[0]["reason"] == "not_in_candidates"
    catalog = build_catalog(
        [
            {"cluster_id": "CL-1", "cluster_name": "集群", "industry_id": "I1", "industry_name": "产业"},
            {"cluster_id": "CL-2", "cluster_name": "集群二", "industry_id": "I2", "industry_name": "产业二"},
            {"cluster_id": "XX-1", "cluster_name": "丢掉", "industry_id": "I9", "industry_name": "非CL"},
        ],
        [
            {"node_id": "n1", "node_name": "节点", "industry_id": "I1"},
            {"node_id": "n2", "node_name": "跨产业", "industry_id": "I1"},
            {"node_id": "n2", "node_name": "跨产业", "industry_id": "I2"},
        ],
    )
    assert set(catalog["nodes"]) == {"n1"}
    assert "node_id_ambiguous" in catalog["gaps"]
    mapped, unmapped = split_stats([
        {"subfield_id": "a", "name_zh": "甲", "node_id": "n1"},
        {"subfield_id": "a", "name_zh": "甲", "node_id": ""},
        {"subfield_id": "b", "name_zh": "乙", "node_id": ""},
    ])
    assert [row["subfield_id"] for row in mapped] == ["a"]
    assert [row["subfield_id"] for row in unmapped] == ["b"]
    assert include_query("", "b", "乙", False) is False
    assert include_query("", "a", "甲", True) is True
    plan = stop_after_failure(["a"], ["b"], ["b", "c"])
    assert plan["untouched"] == ["c"]
    assert "c" not in plan["done"] and "c" not in plan["failed"]
    print("self-check ok")
    return EXIT_OK


def _env(name):
    return _s(os.environ.get(name))


def _schema(name, default):
    value = _env(name) or default
    if value.startswith("demo_"):
        raise SystemExit("禁止把映射写进 demo_ 库")
    qident(value)
    return value


def _catalog_name():
    raw = _env("SUBFIELD_CATALOG")
    if not raw or "." not in raw:
        return None
    schema, table = raw.split(".", 1)
    return qident(schema) + "." + qident(table)


def _connect():
    import pymysql

    host, user, password = _env("MYSQL_HOST"), _env("MYSQL_USER"), os.environ.get("MYSQL_PASSWORD")
    if not host or not user or not password:
        raise SystemExit("缺少 MYSQL_HOST / MYSQL_USER / MYSQL_PASSWORD")
    return pymysql.connect(
        host=host,
        port=int(_env("MYSQL_PORT") or "3306"),
        user=user,
        password=password,
        charset="utf8mb4",
        autocommit=False,
        cursorclass=pymysql.cursors.DictCursor,
    )


def _map_table():
    return qident(_schema("DIM_SCHEMA", "gkxlumenx_dim")) + "." + qident(_env("MAP_TABLE") or "subfield_topic_map")


def _require_table(cur, table):
    schema, name = table.split(".")
    cur.execute(
        "SELECT 1 FROM information_schema.tables WHERE table_schema=%s AND table_name=%s",
        (schema.strip("`"), name.strip("`")),
    )
    if not cur.fetchone():
        raise SystemExit("映射表不存在")


def _fetch(cur, sql):
    cur.execute(sql)
    return list(cur.fetchall())


def _print(payload):
    print(json.dumps(payload, ensure_ascii=False, default=str))


def cmd_sync(conn, table):
    catalog = _catalog_name()
    if not catalog:
        raise SystemExit("未配置本侧子学科目录 SUBFIELD_CATALOG，不连久新")
    with conn.cursor() as cur:
        _require_table(cur, table)
        incoming = _fetch(cur, "SELECT subfield_id, name_zh, data_version FROM " + catalog)
        if not incoming:
            raise SystemExit("子学科目录为空，未改映射表")
        existing = [row["subfield_id"] for row in _fetch(cur, "SELECT DISTINCT subfield_id FROM " + table)]
        inserts, updates = plan_sync(existing, incoming)
        for item in updates:
            cur.execute(
                "UPDATE " + table + " SET name_zh=%s, data_version=%s, synced_at=NOW() WHERE subfield_id=%s",
                (item["name_zh"], item["data_version"], item["subfield_id"]),
            )
        for item in inserts:
            cur.execute(
                "INSERT INTO " + table + " (subfield_id, name_zh, data_version, synced_at) VALUES (%s,%s,%s,NOW())",
                (item["subfield_id"], item["name_zh"], item["data_version"]),
            )
    conn.commit()
    _print({"inserted": len(inserts), "updated": len(updates), "skipped_delete": True})


def _candidates(cur):
    dim = qident(_schema("DIM_SCHEMA", "gkxlumenx_dim"))
    dwd = qident(_schema("DWD_SCHEMA", "gkxlumenx_dwd"))
    clusters = _fetch(cur, (
        "SELECT c.cluster_id, c.cluster_name, m.industry_id, m.industry_name FROM " + dim
        + ".industry_cluster c LEFT JOIN " + dim
        + ".industry_cluster_map m ON m.cluster_id=c.cluster_id AND m.is_active=1 "
        + "WHERE c.is_active=1 AND c.cluster_id LIKE 'CL-%'"
    ))
    nodes = _fetch(cur, (
        "SELECT n.node_id, n.node_name, c.industry_id FROM " + dwd
        + ".industry_chain c JOIN " + dwd
        + ".industry_chain_node n ON n.chain_id=c.chain_id AND n.is_deleted=0 WHERE c.is_deleted=0"
    ))
    return build_catalog(clusters, nodes)


def _call_model(subfields, nodes):
    key = _env("LLM_API_KEY")
    if not key:
        raise RuntimeError("LLM API key not configured")
    base = (_env("LLM_BASE_URL") or "https://open.bigmodel.cn/api/paas/v4").rstrip("/")
    model = _env("LLM_MODEL") or "glm-5.3-flash"
    payload = {
        "model": model,
        "temperature": 0.1,
        "messages": [
            {"role": "system", "content": _SYSTEM},
            {"role": "user", "content": json.dumps({
                "subfields": [{"subfield_id": row["subfield_id"], "name_zh": row["name_zh"]} for row in subfields],
                "candidates": [{
                    "node_id": node["node_id"],
                    "node_name": node["node_name"],
                    "industry_id": node["industry_id"],
                    "cluster_id": ",".join(cid for cid, _name in node["clusters"] if cid),
                } for node in nodes.values()],
            }, ensure_ascii=False)},
        ],
    }
    req = urllib.request.Request(
        base + "/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as ex:
        raise RuntimeError("模型调用失败") from ex
    text = body["choices"][0]["message"]["content"]
    parsed = loads_llm(text)
    return model, parsed.get("links") or []


def _mark_failed(cur, table, items, reason):
    text = _clip(reason or "关联失败", 480)
    for item in items:
        cur.execute(
            "UPDATE " + table + " SET fail_reason=%s WHERE subfield_id=%s AND node_id IS NULL",
            (text, item["subfield_id"]),
        )


def cmd_link(conn, table):
    with conn.cursor() as cur:
        _require_table(cur, table)
        pending = _fetch(cur, (
            "SELECT subfield_id, MAX(name_zh) AS name_zh, MAX(data_version) AS data_version FROM " + table
            + " GROUP BY subfield_id HAVING SUM(CASE WHEN node_id IS NOT NULL AND node_id<>'' THEN 1 ELSE 0 END)=0 "
            + "ORDER BY subfield_id"
        ))
        catalog = _candidates(cur)
        if not pending:
            _print({"linked": 0, "failed": 0, "untouched": 0, "gaps": catalog["gaps"], "message": "没有未关联的子学科"})
            return
        if not catalog["nodes"]:
            _print({"linked": 0, "failed": 0, "untouched": len(pending), "gaps": catalog["gaps"], "message": "本侧没有可关联的产业节点，未调用模型"})
            return
        linked = []
        failed = []
        untouched = []
        stopped = False
        for batch in batches(pending):
            if stopped:
                untouched.extend(row["subfield_id"] for row in batch)
                continue
            try:
                model, raw = _call_model(batch, catalog["nodes"])
            except (RuntimeError, ValueError, KeyError) as ex:
                _mark_failed(cur, table, batch, str(ex))
                failed.extend(row["subfield_id"] for row in batch)
                stopped = True
                continue
            ids = [row["subfield_id"] for row in batch]
            by_id = {row["subfield_id"]: row for row in batch}
            ok, rejected = accept_links(raw, ids, catalog["nodes"])
            by_sub = {}
            for link in ok:
                by_sub.setdefault(link["subfield_id"], []).append(link["node_id"])
            for sid, node_ids in by_sub.items():
                rows = link_rows(by_id[sid], node_ids, catalog["nodes"], model)
                if not rows:
                    continue
                for row in rows:
                    cur.execute(
                        "INSERT INTO " + table + " (subfield_id,name_zh,data_version,synced_at,node_id,node_name,"
                        "industry_id,industry_name,cluster_id,cluster_name,model_name,linked_at) "
                        "VALUES (%s,%s,%s,NOW(),%s,%s,%s,%s,%s,%s,%s,NOW())",
                        (row["subfield_id"], row["name_zh"], row["data_version"], row["node_id"], row["node_name"],
                         row["industry_id"], row["industry_name"], row["cluster_id"] or None,
                         row["cluster_name"], row["model_name"]),
                    )
                cur.execute(
                    "DELETE FROM " + table + " WHERE subfield_id=%s AND node_id IS NULL",
                    (sid,),
                )
                linked.append(sid)
            bad = [by_id[item["subfield_id"]] for item in rejected if item["subfield_id"] not in by_sub]
            if bad:
                _mark_failed(cur, table, bad, "返回的节点不在本侧候选内")
                failed.extend(row["subfield_id"] for row in bad)
    conn.commit()
    _print({
        "linked": len(linked),
        "failed": len(failed),
        "untouched": len(untouched),
        "gaps": catalog["gaps"],
    })


def cmd_stats(conn, table):
    with conn.cursor() as cur:
        _require_table(cur, table)
        rows = _fetch(cur, "SELECT subfield_id, name_zh, node_id FROM " + table)
    mapped, unmapped = split_stats(rows)
    _print({"mapped_count": len(mapped), "unmapped_count": len(unmapped), "mapped": mapped, "unmapped": unmapped})


def cmd_query(conn, table, keyword):
    with conn.cursor() as cur:
        _require_table(cur, table)
        rows = _fetch(cur, (
            "SELECT subfield_id, name_zh, node_id, node_name, industry_id, industry_name, cluster_id, cluster_name FROM "
            + table + " ORDER BY subfield_id, node_id"
        ))
    names, links = {}, {}
    for row in rows:
        sid = _s(row.get("subfield_id"))
        if not sid:
            continue
        if _s(row.get("name_zh")):
            names[sid] = _s(row.get("name_zh"))
        else:
            names.setdefault(sid, "")
        linked = bool(_s(row.get("node_id")))
        if not include_query(keyword, sid, names[sid], linked):
            continue
        links.setdefault(sid, [])
        if linked:
            links[sid].append({
                "node_id": _s(row.get("node_id")),
                "node_name": _s(row.get("node_name")),
                "industry_id": _s(row.get("industry_id")),
                "industry_name": _s(row.get("industry_name")),
                "cluster_id": _s(row.get("cluster_id")),
                "cluster_name": _s(row.get("cluster_name")),
            })
    _print({"items": [{"subfield_id": sid, "name_zh": names.get(sid, ""), "links": links[sid]} for sid in links]})


def main(argv):
    parser = argparse.ArgumentParser(description="GDF 子学科与产业节点")
    parser.add_argument("command", nargs="?", choices=["sync", "link", "stats", "query"])
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--keyword", default="")
    args = parser.parse_args(argv)
    if args.self_check:
        return self_check()
    if not args.command:
        parser.error("需要 sync、link、stats、query 之一，或 --self-check")
    try:
        table = _map_table()
        conn = _connect()
    except SystemExit as ex:
        print(ex, file=sys.stderr)
        return EXIT_ENV
    except ValueError as ex:
        print(ex, file=sys.stderr)
        return EXIT_ENV
    try:
        if args.command == "sync":
            cmd_sync(conn, table)
        elif args.command == "link":
            cmd_link(conn, table)
        elif args.command == "stats":
            cmd_stats(conn, table)
        else:
            cmd_query(conn, table, args.keyword)
    except SystemExit as ex:
        conn.rollback()
        text = str(ex)
        print(text, file=sys.stderr)
        if "映射表不存在" in text:
            return EXIT_TABLE
        if "未配置" in text or "禁止" in text:
            return EXIT_ENV
        return EXIT_ERR
    except Exception as ex:
        conn.rollback()
        print(type(ex).__name__, file=sys.stderr)
        return EXIT_ERR
    finally:
        conn.close()
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

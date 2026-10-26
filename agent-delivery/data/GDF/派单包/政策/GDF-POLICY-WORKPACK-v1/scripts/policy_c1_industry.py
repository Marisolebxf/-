# GDF 作业 POLICY-C1：从政策主表抽取产业，写入 policy_industry_rel。
# 把本文件复制到 GDF 的 Python 节点（人工拷贝或同步均可）。
# 在国内、国际两张平面当日都洗进 policy_base_info 且 success 之后执行。
# 不调用国科信的 HTTP 接口。检索失败或没有过线的链码时不写行。
#
# 依赖：Python 3.9+、pymysql。
# 环境（口令不进本包）：
#   POLICY_MYSQL_HOST / POLICY_MYSQL_PORT / POLICY_MYSQL_USER / POLICY_MYSQL_PASSWORD
#   POLICY_DWD_DB=gkxlumenx_dwd   POLICY_ADS_DB=gkxlumenx_ads
#   EMBED_BASE_URL  EMBED_API_KEY（可空）  EMBED_MODEL（可空）
#   MILVUS_URI      MILVUS_TOKEN（可空）   MILVUS_COLLECTION_PREFIX（默认同下）
#
#   python policy_c1_industry.py --limit 100
#   python policy_c1_industry.py --policy-id <id> [--force]
#   python policy_c1_industry.py --self-check

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime

CHUNK_TOP_K = 5
MAX_BODY_CHUNKS = 12
MAX_LINKS = 5
SCORE_WRITE = 0.55
SCORE_GRAY = 0.45
DIM = 768
PREFIX = "gkxlumen_industry_"
COLLECTION_SUFFIX = "anchor"
QUERY_PREFIX = "为这个句子生成表示以用于检索相关文章："
_CHUNK_SPLIT = re.compile(r"[。；;\n]+")
_CHUNK_BARE = re.compile(r"[^\u4e00-\u9fffA-Za-z0-9]+")
_BOILER = frozenset({
    "通知", "办法", "本办法自发布之日起施行", "自发布之日起施行",
    "自印发之日起施行", "特此通知",
})
_TITLE_STOP = frozenset({
    "产业", "技术", "科学", "发展", "创新", "建设", "支持", "促进", "关于", "开展",
    "实施", "方案", "通知", "若干", "措施", "管理", "服务", "体系", "平台", "项目",
    "企业", "行业", "领域", "政策", "工作", "推进", "加强", "提升", "高质量", "意见",
    "办法", "规定", "行动", "专项", "试点", "示范", "中心", "基地", "工程", "计划",
    "资金", "补贴", "奖励", "申报", "组织", "进一步", "有关", "相关", "以及", "我国",
    "全市", "全省", "做好",
})


def _bare(text: str) -> str:
    return _CHUNK_BARE.sub("", str(text or ""))


def _boiler(text: str) -> bool:
    bare = _bare(text)
    return not bare or bare in _BOILER


def body_chunks(text: str) -> list[str]:
    out: list[str] = []
    for part in _CHUNK_SPLIT.split(str(text or "")):
        part = part.strip()
        if len(_bare(part)) < 8 or _boiler(part):
            continue
        while part and len(out) < MAX_BODY_CHUNKS:
            piece, part = part[:120].strip(), part[120:].strip()
            if len(_bare(piece)) < 8 or _boiler(piece):
                continue
            out.append(piece)
        if len(out) >= MAX_BODY_CHUNKS:
            break
    return out


def search_chunks(row: dict) -> list[str]:
    chunks: list[str] = []
    title = str(row.get("title") or "").strip()
    if title and not _boiler(title):
        chunks.append(title[:120].strip())
    keywords = str(row.get("keywords") or "").strip()
    if keywords and keywords != title and not _boiler(keywords):
        chunks.append(keywords[:120].strip())
    content = str(row.get("content") or "").strip()
    body = content if content else str(row.get("abstract") or "").strip()
    chunks.extend(body_chunks(body))
    return chunks


def _tokens(name: str) -> list[str]:
    text = str(name or "").strip()
    for sep in ("与", "和", "、", "/", "（", "("):
        text = text.replace(sep, "|")
    text = text.replace("）", "").replace(")", "")
    return [part.strip() for part in text.split("|") if len(part.strip()) >= 2]


def lexical(name: str, chunk: str) -> bool:
    name = str(name or "").strip()
    if len(name) >= 3 and name not in _TITLE_STOP and name in chunk:
        return True
    return any(len(tok) >= 3 and tok not in _TITLE_STOP and tok in chunk for tok in _tokens(name))


def aggregate(chunk_hits: list[tuple[str, list]]) -> list[dict]:
    best: dict[str, dict] = {}
    for chunk, hits in chunk_hits:
        for hit in hits or []:
            if not isinstance(hit, dict):
                continue
            vid = str(hit.get("vid") or "").strip()
            name = str(hit.get("name") or "").strip()
            if not vid or not name:
                continue
            try:
                score = float(hit.get("score") or 0)
            except (TypeError, ValueError):
                score = 0.0
            hit_lex = lexical(name, chunk)
            cur = best.get(vid)
            if cur is None or score > cur["score"]:
                best[vid] = {"vid": vid, "name": name, "score": score, "lexical": hit_lex, "chunk_hits": 1 if cur is None else cur["chunk_hits"] + 1}
            else:
                cur["chunk_hits"] += 1
                if score == cur["score"]:
                    cur["lexical"] = cur["lexical"] or hit_lex
    ranked = [item for item in best.values() if item["score"] >= SCORE_WRITE or (item["score"] >= SCORE_GRAY and item["lexical"])]
    ranked.sort(key=lambda item: (-item["score"], item["vid"]))
    return ranked[:MAX_LINKS]


def _key(code, name):
    code, name = str(code or "").strip(), str(name or "").strip()
    if code:
        return ("code", code)
    if name:
        return ("name", name)
    return None


def plan_rel(existing: list[dict], slot: list[dict]) -> dict:
    wanted = {}
    for raw in slot or []:
        item = raw if isinstance(raw, dict) else {"name": raw}
        code = str(item.get("industry_link_code") or "").strip()
        name = str(item.get("name") or item.get("industry_name") or "").strip()
        key = _key(code, name)
        if key:
            wanted[key] = {"industry_name": name, "industry_link_code": code}
    by_key: dict = {}
    soft: list = []
    for row in existing or []:
        key = _key(row.get("industry_link_code"), row.get("industry_name"))
        rel_id = row.get("id")
        if key is None:
            if rel_id is not None and int(row.get("is_deleted") or 0) == 0:
                soft.append(rel_id)
            continue
        prev = by_key.get(key)
        if prev is None:
            by_key[key] = row
            continue
        keep, drop = (prev, row) if int(prev["id"]) <= int(row["id"]) else (row, prev)
        by_key[key] = keep
        if int(drop.get("is_deleted") or 0) == 0:
            soft.append(drop["id"])
    updates, inserts = [], []
    for key, item in wanted.items():
        prev = by_key.get(key)
        if prev is None:
            inserts.append(item)
        else:
            updates.append({"id": prev["id"], **item})
    for key, prev in by_key.items():
        if key not in wanted and int(prev.get("is_deleted") or 0) == 0:
            soft.append(prev["id"])
    return {"updates": updates, "inserts": inserts, "soft_delete_ids": list(dict.fromkeys(soft))}


def _ident(name: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_]+", name or ""):
        raise SystemExit(f"库名非法: {name!r}")
    return name


def _post(url: str, body: dict, headers: dict, timeout: int):
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.load(resp)


def embed_query(text: str) -> list[float] | None:
    base = os.environ.get("EMBED_BASE_URL", "").strip().rstrip("/")
    if not base:
        return None
    url = base if base.endswith("/v1/embeddings") else f"{base}/v1/embeddings"
    headers = {"Content-Type": "application/json"}
    token = os.environ.get("EMBED_API_KEY", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    model = os.environ.get("EMBED_MODEL", "").strip() or "BAAI/bge-base-zh-v1.5"
    payload = {"model": model, "input": [QUERY_PREFIX + text]}
    last = None
    for attempt in range(3):
        try:
            data = _post(url, payload, headers, 60)
            rows = sorted(data.get("data") or [], key=lambda item: int(item.get("index") or 0))
            vec = (rows[0].get("embedding") if rows else None) or []
            if len(vec) != DIM:
                return None
            return [float(x) for x in vec]
        except (OSError, ValueError, urllib.error.URLError, KeyError, IndexError) as exc:
            last = exc
            time.sleep(1)
    print(f"embedding 失败: {last}", file=sys.stderr)
    return None


def milvus_search(vector: list[float]) -> list[dict] | None:
    uri = os.environ.get("MILVUS_URI", "").strip().rstrip("/")
    if not uri:
        return None
    prefix = os.environ.get("MILVUS_COLLECTION_PREFIX", PREFIX).strip() or PREFIX
    name = f"{prefix}{COLLECTION_SUFFIX}"
    if not name.startswith(prefix):
        return None
    headers = {"Content-Type": "application/json"}
    token = os.environ.get("MILVUS_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        payload = _post(f"{uri}/v2/vectordb/entities/search", {
            "dbName": "default",
            "collectionName": name,
            "data": [vector],
            "limit": CHUNK_TOP_K,
            "outputFields": ["vid", "kind", "name", "industry_code", "index_version"],
        }, headers, 10)
    except (OSError, ValueError, urllib.error.URLError) as exc:
        print(f"Milvus 失败: {exc}", file=sys.stderr)
        return None
    if payload.get("code") not in (0, 200):
        return None
    items = []
    for hit in payload.get("data") or []:
        vid = str(hit.get("vid") or hit.get("id") or "").strip()
        kind = str(hit.get("kind") or "")
        if not vid or kind not in ("chain", "segment"):
            continue
        try:
            score = float(hit.get("distance") or 0)
        except (TypeError, ValueError):
            score = 0.0
        items.append({"vid": vid, "name": str(hit.get("name") or ""), "score": score})
    return items[:CHUNK_TOP_K]


def search_chunk(text: str) -> list[dict] | None:
    vec = embed_query(text)
    if vec is None:
        return None
    return milvus_search(vec)


def connect():
    import pymysql

    return pymysql.connect(
        host=os.environ["POLICY_MYSQL_HOST"],
        port=int(os.environ.get("POLICY_MYSQL_PORT", "3306")),
        user=os.environ["POLICY_MYSQL_USER"],
        password=os.environ["POLICY_MYSQL_PASSWORD"],
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )


def _q(conn, sql, args=()):
    with conn.cursor() as cur:
        cur.execute(sql, args)
        return list(cur.fetchall())


def _x(conn, sql, args=()):
    with conn.cursor() as cur:
        cur.execute(sql, args)


def assert_no_collision(conn, dwd: str) -> None:
    rows = _q(
        conn,
        f"SELECT policy_id FROM {dwd}.policy_base_info GROUP BY policy_id HAVING COUNT(DISTINCT source_plane)>1 LIMIT 1",
    )
    if rows:
        raise SystemExit(f"policy_id 撞车: {rows[0]['policy_id']}。先停，不改 UK，本脚本不写")


def load_rows(conn, dwd: str, limit: int, policy_id: str, force: bool) -> list[dict]:
    where = "is_deleted=0 AND IFNULL(is_history,0)=0"
    if policy_id:
        return _q(conn, f"SELECT policy_id, title, abstract, keywords, content FROM {dwd}.policy_base_info WHERE policy_id=%s AND {where} LIMIT 1", (policy_id,))
    skip = ""
    if not force:
        skip = (
            " AND NOT EXISTS (SELECT 1 FROM " + dwd + ".policy_industry_rel r"
            " WHERE r.policy_id=p.policy_id AND r.is_deleted=0 AND r.industry_link_code<>'')"
        )
    return _q(
        conn,
        f"SELECT policy_id, title, abstract, keywords, content FROM {dwd}.policy_base_info p WHERE {where}{skip} ORDER BY policy_id LIMIT %s",
        (limit,),
    )


def write_slot(conn, dwd: str, ads: str, policy_id: str, slot: list[dict]) -> None:
    now = datetime.now().replace(microsecond=0).strftime("%Y-%m-%d %H:%M:%S")
    existing = _q(conn, f"SELECT id, industry_name, industry_link_code, is_deleted FROM {dwd}.policy_industry_rel WHERE policy_id=%s", (policy_id,))
    plan = plan_rel(existing, slot)
    for row in plan["updates"]:
        _x(conn, f"UPDATE {dwd}.policy_industry_rel SET industry_name=%s, industry_link_code=%s, is_deleted=0, update_time=%s WHERE id=%s AND policy_id=%s", (row["industry_name"], row["industry_link_code"], now, row["id"], policy_id))
    for row in plan["inserts"]:
        _x(conn, f"INSERT INTO {dwd}.policy_industry_rel (policy_id, industry_name, industry_link_code, is_deleted, create_time, update_time) VALUES (%s,%s,%s,0,%s,%s)", (policy_id, row["industry_name"], row["industry_link_code"], now, now))
    for rel_id in plan["soft_delete_ids"]:
        _x(conn, f"UPDATE {dwd}.policy_industry_rel SET is_deleted=1, update_time=%s WHERE id=%s AND policy_id=%s AND is_deleted=0", (now, rel_id, policy_id))
    rows = _q(conn, f"SELECT id, policy_id, industry_name, industry_link_code, is_deleted, create_time, update_time FROM {dwd}.policy_industry_rel WHERE policy_id=%s", (policy_id,))
    _x(conn, f"DELETE FROM {ads}.policy_industry_rel WHERE policy_id=%s", (policy_id,))
    for row in rows:
        _x(conn, f"INSERT INTO {ads}.policy_industry_rel (id, policy_id, industry_name, industry_link_code, is_deleted, create_time, update_time) VALUES (%s,%s,%s,%s,%s,%s,%s)", (row["id"], row["policy_id"], row["industry_name"], row["industry_link_code"], row["is_deleted"], row["create_time"], row["update_time"]))
    conn.commit()


def run(limit: int, policy_id: str, force: bool) -> int:
    dwd, ads = _ident(os.environ.get("POLICY_DWD_DB", "gkxlumenx_dwd")), _ident(os.environ.get("POLICY_ADS_DB", "gkxlumenx_ads"))
    conn = connect()
    written = skipped = 0
    try:
        assert_no_collision(conn, dwd)
        for row in load_rows(conn, dwd, limit, policy_id, force):
            pid = str(row["policy_id"])
            chunks = search_chunks(row)
            if not chunks:
                skipped += 1
                continue
            collected = []
            degraded = False
            for chunk in chunks:
                hits = search_chunk(chunk)
                if hits is None:
                    degraded = True
                    break
                collected.append((chunk, hits))
            if degraded or not collected:
                print(f"{pid} search_degraded 不写")
                skipped += 1
                conn.rollback()
                continue
            ranked = aggregate(collected)
            if not ranked:
                print(f"{pid} no_match 不写")
                skipped += 1
                continue
            slot = [{"name": item["name"], "industry_link_code": item["vid"]} for item in ranked]
            write_slot(conn, dwd, ads, pid, slot)
            written += 1
            print(f"{pid} written {len(slot)}")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    print(f"done written={written} skipped={skipped}")
    return 0


def self_check() -> None:
    assert body_chunks("特此通知") == []
    assert aggregate([("人工智能产业政策正文足够长", [{"vid": "chain:ai", "name": "人工智能", "score": 0.6}])])[0]["vid"] == "chain:ai"
    assert aggregate([("无关文本足够长足够长", [{"vid": "chain:x", "name": "量子", "score": 0.5}])]) == []
    gray = aggregate([("量子计算专项足够长", [{"vid": "chain:q", "name": "量子计算", "score": 0.5}])])
    assert gray and gray[0]["lexical"]
    plan = plan_rel(
        [{"id": 1, "industry_name": "旧", "industry_link_code": "chain:a", "is_deleted": 0}],
        [{"name": "新", "industry_link_code": "chain:a"}, {"name": "乙", "industry_link_code": "chain:b"}],
    )
    assert plan["updates"][0]["industry_name"] == "新" and plan["inserts"][0]["industry_link_code"] == "chain:b"
    gone = plan_rel([{"id": 1, "industry_name": "旧", "industry_link_code": "chain:a", "is_deleted": 0}], [])
    assert gone["soft_delete_ids"] == [1] and gone["inserts"] == []
    print("self-check ok")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="POLICY-C1 抽取产业")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--policy-id", default="")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args(argv)
    if args.limit < 1 or args.limit > 100:
        print("limit 须在 1 到 100", file=sys.stderr)
        return 2
    if args.self_check:
        self_check()
        return 0
    return run(args.limit, args.policy_id.strip(), args.force)


if __name__ == "__main__":
    raise SystemExit(main())

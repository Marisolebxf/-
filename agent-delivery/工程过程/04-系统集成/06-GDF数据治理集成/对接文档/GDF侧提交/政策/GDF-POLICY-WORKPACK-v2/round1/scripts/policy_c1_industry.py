# GDF 作业 POLICY-C1：从政策主表抽取产业，写入 policy_industry_rel。
#
# ═══ 修改版 v2（2026-10-30）═══
# 基于客户原件 policy_c1_industry.py（sha256 e85e3bf6...）改造，业务逻辑未动。
# 改动清单见同目录《修改记录.md》。摘要：
#   S1 增量改为「状态表 + 内容指纹」，无产出也留痕（解决 written=0 假成功停滞）
#   S2 新增 --max-rounds 脚本内循环 + no_progress 保护 + --deadline-sec
#   S3 环境变量 fail-fast（EMBED_BASE_URL / MILVUS_URI 缺失直接非 0 退出）
#   S4 退出码显式化（1 保留给未捕获异常）
#   S5 --force 必须配 --policy-id，防止全表重烧
#   S6 self-check 覆盖新逻辑
# ════════════════════════════
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
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta

CHUNK_TOP_K = 5
MAX_BODY_CHUNKS = 12
MAX_LINKS = 5
SCORE_WRITE = 0.55
SCORE_GRAY = 0.45
DIM = 768
PREFIX = "gkxlumen_industry_"
COLLECTION_SUFFIX = "anchor"
QUERY_PREFIX = "为这个句子生成表示以用于检索相关文章："
JOB = "c1"
STATE_TABLE = "script_state"
RETRY_DEGRADED_MIN = 60
RETRY_FAILED_MIN = 60
RETRY_NO_MATCH_DAYS = 30
MAX_TRY = 5
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


# ─────────────── 以下为修改版新增（S1 状态表 / 指纹）───────────────

def content_hash(row: dict) -> str:
    """C1 输入指纹。覆盖脚本真正用到的四个字段，任一变化即视为需要重算。"""
    raw = "\n".join(str(row.get(k) or "") for k in ("title", "keywords", "abstract", "content"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def sql_content_hash(alias: str = "p") -> str:
    """与 content_hash() 等价的 MySQL 表达式。
    必须逐字节对齐：Python 侧用 '\n'.join([...])，NULL 变空串；
    所以 SQL 必须用 CONCAT + IFNULL + CHAR(10)，不能用 CONCAT_WS（遇 NULL 会跳过分隔符）。"""
    return ("LEFT(SHA2(CONCAT(IFNULL({a}.title,''),CHAR(10),IFNULL({a}.keywords,''),"
            "CHAR(10),IFNULL({a}.abstract,''),CHAR(10),IFNULL({a}.content,'')),256),16)").format(a=alias)


def state_table_exists(conn, dwd: str) -> bool:
    rows = _q(conn, "SELECT 1 AS ok FROM information_schema.TABLES "
                    "WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s LIMIT 1", (dwd, STATE_TABLE))
    return bool(rows)


def load_states(conn, dwd: str, ids: list) -> dict:
    if not ids:
        return {}
    marks = ",".join(["%s"] * len(ids))
    rows = _q(conn, f"SELECT policy_id, content_hash, status, next_try_at, try_count "
                    f"FROM {dwd}.{STATE_TABLE} WHERE job=%s AND policy_id IN ({marks})",
              tuple([JOB] + list(ids)))
    return {str(r["policy_id"]): r for r in rows}


def save_state(conn, dwd: str, policy_id: str, src_hash: str, status: str,
               batch_id: str, note: str = "", retry_min: int = 0,
               retry_days: int = 0, terminal: bool = False) -> None:
    """写/更新一条状态。terminal=True 表示终态（next_try_at=NULL）。"""
    now = datetime.now().replace(microsecond=0)
    next_try = None
    if not terminal:
        if retry_min:
            next_try = now + timedelta(minutes=retry_min)
        elif retry_days:
            next_try = now + timedelta(days=retry_days)
    prev = _q(conn, f"SELECT try_count, content_hash FROM {dwd}.{STATE_TABLE} "
                    f"WHERE job=%s AND policy_id=%s LIMIT 1", (JOB, policy_id))
    try_count = (int(prev[0]["try_count"]) + 1) if prev else 1
    # 内容变了则重新计数
    if prev and str(prev[0]["content_hash"]) != src_hash:
        try_count = 1
    if try_count >= MAX_TRY and not terminal:
        terminal = True
        next_try = None
        note = (note + f" | 达重试上限{MAX_TRY}转终态").strip(" |")
    _x(conn,
       f"INSERT INTO {dwd}.{STATE_TABLE} "
       f"(job, policy_id, content_hash, status, batch_id, tried_at, next_try_at, try_count, note) "
       f"VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) "
       f"ON DUPLICATE KEY UPDATE content_hash=VALUES(content_hash), status=VALUES(status), "
       f"batch_id=VALUES(batch_id), tried_at=VALUES(tried_at), next_try_at=VALUES(next_try_at), "
       f"try_count=VALUES(try_count), note=VALUES(note)",
       (JOB, policy_id, src_hash, status, batch_id,
        now.strftime("%Y-%m-%d %H:%M:%S"),
        next_try.strftime("%Y-%m-%d %H:%M:%S") if next_try else None,
        try_count, note[:500]))
    conn.commit()


def check_env() -> None:
    """S3 fail-fast：C1 的实质依赖缺了会「静默空跑且退出码 0」，必须起跑前拦住。"""
    if not os.environ.get("EMBED_BASE_URL", "").strip():
        raise SystemExit("环境变量缺失：EMBED_BASE_URL（C1 无它则每条 search_degraded、产出为零）")
    if not os.environ.get("MILVUS_URI", "").strip():
        raise SystemExit("环境变量缺失：MILVUS_URI（C1 无它则检索失败、产出为零）")
    for key in ("POLICY_MYSQL_HOST", "POLICY_MYSQL_USER", "POLICY_MYSQL_PASSWORD"):
        if not os.environ.get(key, "").strip():
            raise SystemExit(f"环境变量缺失：{key}")

# ─────────────── 新增结束 ───────────────


def load_rows(conn, dwd: str, limit: int, policy_id: str, force: bool,
              cursor: str = "") -> list[dict]:
    """S1：待办判定改为「状态表 + 内容指纹」。
    - 没有状态记录           → 新行，处理
    - 有记录但 content_hash 变了 → 内容变更，重算
    - 有记录、hash 相同、未到 next_try_at → 跳过（这是能真正前进的关键）
    - 有记录、hash 相同、已到 next_try_at → 冷却结束，可重试
    注意：不再用「目标表有没有非空链码」判增量——那会让无产出的行永远重复入选。
    """
    where = "p.is_deleted=0 AND IFNULL(p.is_history,0)=0"
    cols = "p.policy_id, p.title, p.abstract, p.keywords, p.content"
    if policy_id:
        return _q(conn, f"SELECT {cols} FROM {dwd}.policy_base_info p WHERE p.policy_id=%s AND {where} LIMIT 1",
                  (policy_id,))

    hash_expr = sql_content_hash("p")
    params = []
    cond = ""
    if not force:
        cond = (
            f" AND NOT EXISTS (SELECT 1 FROM {dwd}.{STATE_TABLE} s"
            f" WHERE s.job=%s AND s.policy_id=p.policy_id"
            f"   AND s.content_hash={hash_expr}"
            f"   AND (s.next_try_at IS NULL OR s.next_try_at > NOW()))"
        )
        params.append(JOB)
    tail = ""
    if cursor:
        tail = " AND p.policy_id > %s"
        params.append(cursor)
    params.append(limit)
    sql = (f"SELECT {cols}, {hash_expr} AS src_hash FROM {dwd}.policy_base_info p"
           f" WHERE {where}{cond}{tail} ORDER BY p.policy_id LIMIT %s")
    return _q(conn, sql, tuple(params))


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


def process_one(conn, dwd: str, ads: str, row: dict, batch_id: str) -> str:
    """处理单条，返回 status：done / empty / no_match / degraded / failed。
    S1 的核心：每种结局都写一行状态，无产出不再「什么都不留」。"""
    pid = str(row["policy_id"])
    src_hash = str(row.get("src_hash") or content_hash(row))

    chunks = search_chunks(row)
    if not chunks:
        print(f"{pid} empty 无可用切块，已记状态")
        save_state(conn, dwd, pid, src_hash, "empty", batch_id,
                   note="无可检索切块", terminal=False, retry_days=RETRY_NO_MATCH_DAYS)
        return "empty"

    collected = []
    for chunk in chunks:
        hits = search_chunk(chunk)
        if hits is None:
            print(f"{pid} search_degraded 不写，已记状态待冷却重试")
            conn.rollback()
            save_state(conn, dwd, pid, src_hash, "degraded", batch_id,
                       note="embedding/Milvus 调用失败", retry_min=RETRY_DEGRADED_MIN)
            return "degraded"
        collected.append((chunk, hits))

    if not collected:
        print(f"{pid} empty 无检索结果，已记状态")
        save_state(conn, dwd, pid, src_hash, "empty", batch_id,
                   note="检索无返回", retry_days=RETRY_NO_MATCH_DAYS)
        return "empty"

    ranked = aggregate(collected)
    if not ranked:
        print(f"{pid} no_match 不写，已记状态")
        save_state(conn, dwd, pid, src_hash, "no_match", batch_id,
                   note="无过线链码", retry_days=RETRY_NO_MATCH_DAYS)
        return "no_match"

    slot = [{"name": item["name"], "industry_link_code": item["vid"]} for item in ranked]
    write_slot(conn, dwd, ads, pid, slot)
    save_state(conn, dwd, pid, src_hash, "done", batch_id,
               note=f"链码 {len(slot)} 条", terminal=True)
    print(f"{pid} written {len(slot)}")
    return "done"


def run(limit: int, policy_id: str, force: bool,
        max_rounds: int = 1, deadline_sec: int = 0) -> int:
    dwd, ads = _ident(os.environ.get("POLICY_DWD_DB", "gkxlumenx_dwd")), _ident(os.environ.get("POLICY_ADS_DB", "gkxlumenx_ads"))
    conn = connect()
    agg = {"rounds": 0, "processed": 0, "written": 0, "skipped": 0, "failed": 0}
    stopped = "max_rounds"
    batch_id = datetime.now().strftime("%Y%m%d%H%M%S")
    t0 = time.time()
    try:
        if not state_table_exists(conn, dwd):
            print(f"缺状态表 {dwd}.{STATE_TABLE}，请先建表（见 sql/script_state.sql）。脚本不建表。",
                  file=sys.stderr)
            return 4
        assert_no_collision(conn, dwd)
        cursor = ""
        for r in range(1, max_rounds + 1):
            rows = load_rows(conn, dwd, limit, policy_id, force, cursor)
            if not rows:
                stopped = "exhausted"
                break
            round_written = round_skipped = 0
            for row in rows:
                pid = str(row["policy_id"])
                status = process_one(conn, dwd, ads, row, batch_id)
                if status == "done":
                    round_written += 1
                else:
                    round_skipped += 1
                cursor = pid          # 逐条推进，失败不跳行
            agg["rounds"] = r
            agg["processed"] += len(rows)
            agg["written"] += round_written
            agg["skipped"] += round_skipped
            # 本批一条没产出但全是可重试态：内容无变化，继续往后走也不会更好 → 停
            if round_written == 0 and round_skipped == len(rows):
                stopped = "no_progress"
                break
            if deadline_sec and time.time() - t0 > deadline_sec:
                stopped = "deadline"
                break
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    print("done rounds={rounds} processed={processed} written={written} "
          "skipped={skipped} stopped={stopped} batch={batch_id}".format(batch_id=batch_id, stopped=stopped, **agg))
    # S4 退出码：0=本批已追平；7=未追平（达轮数上限/超时/无进展）
    return 0 if stopped == "exhausted" else 7


def self_check() -> None:
    # ── S6 新增：指纹与状态语义自检（不连库）──
    r1 = {"title": "A", "keywords": "B", "abstract": "C", "content": "D"}
    assert content_hash(r1) == content_hash(dict(r1)), "指纹须稳定"
    assert content_hash(r1) != content_hash(dict(r1, content="D2")), "正文变化须改变指纹"
    assert content_hash({}) == content_hash({"title": ""}), "空值须归一"
    sql_expr = sql_content_hash("p")
    assert "CONCAT_WS" not in sql_expr, "不能用 CONCAT_WS（遇 NULL 会跳过分隔符，与 Python 口径不一致）"
    assert "CHAR(10)" in sql_expr and "IFNULL" in sql_expr, "须用 CONCAT+IFNULL+CHAR(10) 对齐 Python"
    assert len(content_hash(r1)) == 16, "指纹长度须与 C2 一致（16）"
    assert body_chunks("特此通知") == [], "套话须被过滤"
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
    parser.add_argument("--limit", type=int, default=100,
                        help="单轮批大小，1~100（平台/客户脚本既有约束，未变）")
    parser.add_argument("--max-rounds", type=int, default=1,
                        help="脚本内循环轮数上限，默认 1 = 原行为；追平存量时调大，如 50")
    parser.add_argument("--deadline-sec", type=int, default=0,
                        help="软超时（秒），到期优雅退出。建议设为平台 Job 超时的 80%%")
    parser.add_argument("--policy-id", default="")
    parser.add_argument("--force", action="store_true",
                        help="重算；必须配 --policy-id，防止全表重烧 embedding")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args(argv)

    # S4 退出码：2 参数错 / 3 环境或依赖缺失 / 4 表缺失 / 1 未捕获异常
    if args.limit < 1 or args.limit > 100:
        print("limit 须在 1 到 100", file=sys.stderr)
        return 2
    if args.max_rounds < 1:
        print("max-rounds 须 >= 1", file=sys.stderr)
        return 2
    if args.deadline_sec < 0:
        print("deadline-sec 须 >= 0", file=sys.stderr)
        return 2
    if args.force and not args.policy_id.strip():
        print("--force 必须配 --policy-id：全表重烧 embedding 请勿用 --force", file=sys.stderr)
        return 2
    if args.self_check:
        self_check()
        return 0
    try:
        check_env()   # S3 fail-fast
    except SystemExit as exc:
        print(str(exc), file=sys.stderr)
        return 3
    return run(args.limit, args.policy_id.strip(), args.force,
               max_rounds=args.max_rounds, deadline_sec=args.deadline_sec)


if __name__ == "__main__":
    raise SystemExit(main())

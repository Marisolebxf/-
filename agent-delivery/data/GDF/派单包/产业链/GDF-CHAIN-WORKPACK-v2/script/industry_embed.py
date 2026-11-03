"""产业锚点向量索引（GDF 派单包交付版 · 路线 A 全环境变量化）。

本文件**独立可跑**：不依赖 `lumen_common` / `polan`。GDF 平台配置本脚本的
`rebuild`，直接写 Milvus；不调用我方 HTTP。

硬编码已全部改为环境变量（见同目录 `README.md` 参数表）。
`MILVUS_DB_NAME`/`DB_NAME` 未配置或仍为 `default` 时**拒绝写入**（防误伤 demo）。
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import time
import urllib.request

import httpx

try:
    import pymysql
    import pymysql.cursors
except ImportError:  # pragma: no cover — 作业机须装 pymysql
    pymysql = None  # type: ignore[assignment]

# ------------------------------------------------------------------ 环境参数 --

DEFAULT_PREFIX = "gkxlumen_industry_"
DEFAULT_COLLECTION_SUFFIX = "anchor"
DEFAULT_DWD_SCHEMA = "gkxlumenx_dwd"
DEFAULT_CHAIN_TABLE = "industry_chain"
DEFAULT_NODE_TABLE = "industry_chain_node"
DEFAULT_METRIC_TYPE = "COSINE"
DEFAULT_DIM = 768
DEFAULT_MODEL_VERSION = "bge-base-zh-v1.5-tei-1.8.3"
DEFAULT_EMBED_MODEL = "BAAI/bge-base-zh-v1.5"
QUERY_PREFIX = "为这个句子生成表示以用于检索相关文章："
DEFAULT_EMBED_BATCH = 32
EMBED_RETRIES = 2
KINDS = ("chain", "segment")
DEFAULT_VID_LENGTH = 80


class CollectionGuardError(RuntimeError):
    """写操作命中非本项目 collection / 非法库名。现网未开鉴权，本守卫是唯一防线。"""


class MilvusUnavailable(RuntimeError):
    """连不上 / 协议不对。调用方必须 degraded，不许兜假数据。"""


class EmbedUnavailable(RuntimeError):
    """TEI 不可用、空响应或 dim 不符。调用方必须 degraded，不许兜假 VID。"""


class AnchorSourceError(RuntimeError):
    """词表源（MySQL）不可用或闸门拒绝。"""


def _env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


def _env_int(name: str, default: int) -> int:
    raw = _env(name)
    if not raw:
        return default
    return int(raw)


def _truthy(name: str) -> bool:
    return _env(name).lower() in ("1", "true", "yes")


def milvus_db_name() -> str:
    """正式库默认要求显式配置；禁止隐式 `default`（会 drop demo 同名集合）。"""
    name = _env("MILVUS_DB_NAME") or _env("DB_NAME")
    if not name:
        raise CollectionGuardError(
            "MILVUS_DB_NAME/DB_NAME 未配置，拒绝写入（禁止隐式 default）"
        )
    if name == "default" and not _truthy("ALLOW_MILVUS_DB_DEFAULT"):
        raise CollectionGuardError(
            "拒绝 dbName=default（会误伤 demo）；正式设 MILVUS_DB_NAME=gkxlumen；"
            "确需 default 时设 ALLOW_MILVUS_DB_DEFAULT=1"
        )
    return name


def collection_prefix() -> str:
    prefix = _env("MILVUS_COLLECTION_PREFIX", DEFAULT_PREFIX)
    if not _legal_name(prefix):
        raise CollectionGuardError(
            f"MILVUS_COLLECTION_PREFIX={prefix!r} 非法（空或含 Milvus 不收的字符），拒绝任何读写"
        )
    return prefix


def collection_suffix() -> str:
    return _env("MILVUS_COLLECTION_SUFFIX", DEFAULT_COLLECTION_SUFFIX) or DEFAULT_COLLECTION_SUFFIX


def default_collection() -> str:
    return f"{collection_prefix()}{collection_suffix()}"


def metric_type() -> str:
    return _env("MILVUS_METRIC_TYPE", DEFAULT_METRIC_TYPE) or DEFAULT_METRIC_TYPE


def embed_dim() -> int:
    return _env_int("EMBED_DIM", DEFAULT_DIM)


def model_version() -> str:
    return _env("EMBED_MODEL_VERSION", DEFAULT_MODEL_VERSION) or DEFAULT_MODEL_VERSION


def embed_batch() -> int:
    return max(1, _env_int("EMBED_BATCH", DEFAULT_EMBED_BATCH))


def dwd_schema() -> str:
    """词表库名闸门：拒绝 demo_ 前缀；正式默认 gkxlumenx_dwd。"""
    schema = _env("CHAIN_DWD_SCHEMA", DEFAULT_DWD_SCHEMA) or DEFAULT_DWD_SCHEMA
    if schema.startswith("demo_") and not _truthy("ALLOW_DEMO_DWD_SCHEMA"):
        raise AnchorSourceError(
            f"拒绝词表库 {schema!r}（demo_）；正式设 CHAIN_DWD_SCHEMA=gkxlumenx_dwd；"
            "确需 demo 时设 ALLOW_DEMO_DWD_SCHEMA=1"
        )
    return schema


def chain_table() -> str:
    return _env("CHAIN_TABLE", DEFAULT_CHAIN_TABLE) or DEFAULT_CHAIN_TABLE


def node_table() -> str:
    return _env("CHAIN_NODE_TABLE", DEFAULT_NODE_TABLE) or DEFAULT_NODE_TABLE


def _legal_name(name: str) -> bool:
    text = str(name or "")
    if not text or text[0].isdigit():
        return False
    return all(ch.isascii() and (ch.isalnum() or ch == "_") for ch in text)


def assert_owned_collection(name: str | None) -> str:
    prefix = collection_prefix()
    text = str(name or "").strip()
    if not text.startswith(prefix) or not _legal_name(text):
        raise CollectionGuardError(
            f"拒绝操作 collection {text!r}：必须以 {prefix!r} 开头且只含 [A-Za-z0-9_]"
        )
    return text


def ok(data, msg=None):
    return {"code": 0, "msg": msg, "data": data}


def error(msg, data=None):
    return {"code": 1, "msg": msg, "data": data}


def current_trace_id() -> str | None:
    return _env("TRACE_ID") or _env("OTEL_TRACE_ID") or None


def split_anchor_tokens(name: str) -> list[str]:
    """「半导体与集成电路」→ 半导体 / 集成电路。短于 3 字丢掉。"""
    s = str(name or "").strip()
    for sep in ("与", "和", "、", "/", "（", "("):
        s = s.replace(sep, "|")
    s = s.replace("）", "").replace(")", "")
    return [t.strip() for t in s.split("|") if len(t.strip()) >= 3]


def _vid(prefix: str, raw, vid_length: int = DEFAULT_VID_LENGTH) -> str | None:
    text = str(raw or "").strip()
    if not text:
        return None
    vid = f"{prefix}{text}"
    if len(vid) > vid_length:
        return None
    return vid


def map_chain_segment_vertices(chains: list[dict], nodes: list[dict]) -> list[dict]:
    """锚点所需最小映射：只产出 chain/segment 顶点（与 graph_project.map_graph 同码规则）。"""
    vertices: list[dict] = []
    seen: set[str] = set()
    for row in chains:
        vid = _vid("chain:", row.get("chain_id"))
        if not vid or vid in seen:
            continue
        seen.add(vid)
        vertices.append({
            "tag": "chain",
            "vid": vid,
            "name": row.get("chain_name") or row.get("chain_id"),
            "chain_id": row.get("chain_id"),
        })
    for row in nodes:
        vid = _vid("segment:", row.get("node_id"))
        if not vid or vid in seen:
            continue
        seen.add(vid)
        vertices.append({
            "tag": "segment",
            "vid": vid,
            "name": row.get("node_name") or row.get("node_id"),
            "segment_key": row.get("node_id") or row.get("node_code"),
            "chain_id": row.get("chain_id"),
        })
    return vertices


# -------------------------------------------------------------------- 向量化 --

def _hashgram(text: str, dim: int) -> list[float]:
    blob = " ".join(str(text or "").lower().split())
    vec = [0.0] * dim
    for n in (1, 2, 3):
        for i in range(len(blob) - n + 1):
            gram = blob[i : i + n]
            if not gram.strip():
                continue
            digest = hashlib.blake2b(gram.encode("utf-8"), digest_size=8).digest()
            vec[int.from_bytes(digest[:4], "big") % dim] += 1.0 if digest[4] % 2 else -1.0
    norm = math.sqrt(sum(v * v for v in vec))
    return [v / norm for v in vec] if norm else vec


def _embed_headers() -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    token = _env("EMBED_API_KEY")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _parse_embeddings(payload: dict, expected: int, dim: int) -> list[list[float]]:
    data = payload.get("data") if isinstance(payload, dict) else None
    if not data:
        raise EmbedUnavailable("embedding 空响应")
    rows = sorted(data, key=lambda item: int(item.get("index") or 0))
    if len(rows) != expected:
        raise EmbedUnavailable(f"embedding 条数 {len(rows)} != {expected}")
    vecs: list[list[float]] = []
    for item in rows:
        vec = item.get("embedding") or []
        if len(vec) != dim:
            raise EmbedUnavailable(f"embedding dim {len(vec)} != {dim}，拒绝写入")
        vecs.append([float(x) for x in vec])
    return vecs


def _embed_tei(texts: list[str], dim: int) -> list[list[float]]:
    base = _env("EMBED_BASE_URL").rstrip("/")
    url = f"{base}/v1/embeddings"
    model = _env("EMBED_MODEL", DEFAULT_EMBED_MODEL) or DEFAULT_EMBED_MODEL
    headers = _embed_headers()
    out: list[list[float]] = []
    batch = embed_batch()
    timeout = httpx.Timeout(60.0, connect=5.0)
    with httpx.Client(timeout=timeout) as client:
        for i in range(0, len(texts), batch):
            chunk = texts[i : i + batch]
            last: Exception | None = None
            for attempt in range(EMBED_RETRIES + 1):
                try:
                    resp = client.post(url, json={"model": model, "input": chunk}, headers=headers)
                    resp.raise_for_status()
                    out.extend(_parse_embeddings(resp.json(), len(chunk), dim))
                    last = None
                    break
                except EmbedUnavailable:
                    raise
                except (httpx.HTTPError, ValueError) as exc:
                    last = exc
                    if attempt < EMBED_RETRIES:
                        time.sleep(1.0)
            if last is not None:
                raise EmbedUnavailable(f"{url}: {type(last).__name__}: {last}") from last
    return out


def embed_texts(texts: list[str], *, is_query: bool = False, dim: int | None = None) -> list[list[float]]:
    dim = embed_dim() if dim is None else dim
    if not texts:
        return []
    if not _env("EMBED_BASE_URL"):
        return [_hashgram(str(t or ""), dim) for t in texts]
    payloads = [(QUERY_PREFIX + str(t or "")) if is_query else str(t or "") for t in texts]
    return _embed_tei(payloads, dim)


def embed_text(text: str, dim: int | None = None, *, is_query: bool = False) -> list[float]:
    return embed_texts([text], is_query=is_query, dim=dim)[0]


def _cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


# ---------------------------------------------------------------- 锚点词表 --

def anchor_docs(chains: list[dict], nodes: list[dict]) -> list[dict]:
    vertices = map_chain_segment_vertices(chains, nodes)
    chain_names = {v["vid"]: v.get("name") for v in vertices if v["tag"] == "chain"}
    docs: list[dict] = []
    for v in vertices:
        kind = v["tag"]
        name = str(v.get("name") or "").strip()
        if kind not in KINDS or not name:
            continue
        aliases = [t for t in split_anchor_tokens(name) if t != name]
        parent = str(chain_names.get(f"chain:{v.get('chain_id')}") or "").strip()
        if kind == "segment" and parent and parent != name:
            aliases.append(parent)
        code = v.get("chain_id") if kind == "chain" else v.get("segment_key")
        docs.append({
            "vid": v["vid"],
            "kind": kind,
            "name": name,
            "aliases": aliases,
            "text": " ".join([name, *aliases]),
            "industry_code": str(code or ""),
            "graph_source": "dwd_chain",
        })
    return docs


def _mysql_connect_kwargs() -> dict:
    host = _env("MYSQL_HOST") or _env("CHAIN_MYSQL_HOST")
    if not host:
        raise AnchorSourceError("MYSQL_HOST/CHAIN_MYSQL_HOST 未配置")
    if pymysql is None:
        raise AnchorSourceError("未安装 pymysql，无法读词表")
    port = _env_int("MYSQL_PORT", _env_int("CHAIN_MYSQL_PORT", 3306))
    user = _env("MYSQL_USER") or _env("CHAIN_MYSQL_USER") or "root"
    password = _env("MYSQL_PASSWORD") or _env("CHAIN_MYSQL_PASSWORD")
    return {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "charset": _env("MYSQL_CHARSET", "utf8mb4") or "utf8mb4",
        "connect_timeout": _env_int("MYSQL_CONNECT_TIMEOUT", 10),
        "read_timeout": _env_int("MYSQL_READ_TIMEOUT", 60),
    }


def load_anchors() -> list[dict]:
    """读正式 DWD 链树（库/表名均可环境变量覆盖；默认 gkxlumenx_dwd）。"""
    schema = dwd_schema()
    t_chain = chain_table()
    t_node = node_table()
    conn = pymysql.connect(**_mysql_connect_kwargs())
    try:
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(
            f"SELECT * FROM `{schema}`.`{t_chain}` WHERE IFNULL(is_deleted,0)=0"
        )
        chains = [dict(row) for row in cur.fetchall()]
        cur.execute(
            f"SELECT * FROM `{schema}`.`{t_node}` WHERE IFNULL(is_deleted,0)=0"
        )
        nodes = [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()
    return anchor_docs(chains, nodes)


# ----------------------------------------------------------------- 存储后端 --

class MemoryStore:
    kind = "memory"
    degraded = True
    _data: dict[str, list[dict]] = {}

    def rebuild(self, collection: str, rows: list[dict], dim: int | None = None) -> None:
        self._data[assert_owned_collection(collection)] = [dict(r) for r in rows]

    def search(self, collection: str, vector: list[float], limit: int) -> list[dict]:
        rows = self._data.get(assert_owned_collection(collection)) or []
        hits = [{**r, "score": _cosine(vector, r["vector"])} for r in rows]
        hits.sort(key=lambda h: h["score"], reverse=True)
        return hits[:limit]


class MilvusHttpStore:
    kind = "milvus"
    degraded = False

    def __init__(self, uri: str, timeout: int = 10) -> None:
        self.uri = uri.rstrip("/")
        self.timeout = timeout
        self.db_name = milvus_db_name()

    def _post(self, path: str, body: dict):
        headers = {"Content-Type": "application/json"}
        token = _env("MILVUS_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        req = urllib.request.Request(
            f"{self.uri}{path}",
            data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                payload = json.load(resp)
        except (OSError, ValueError) as exc:
            raise MilvusUnavailable(f"{path}: {type(exc).__name__}: {exc}") from exc
        if payload.get("code") not in (0, 200):
            raise MilvusUnavailable(f"{path} 返回 {payload}")
        return payload.get("data")

    def list_collections(self) -> list[str]:
        return list(self._post("/v2/vectordb/collections/list", {"dbName": self.db_name}) or [])

    def drop(self, collection: str) -> None:
        name = assert_owned_collection(collection)
        self._post("/v2/vectordb/collections/drop", {"dbName": self.db_name, "collectionName": name})

    def create(self, collection: str, dim: int | None = None) -> None:
        name = assert_owned_collection(collection)
        dim = embed_dim() if dim is None else dim
        self._post("/v2/vectordb/collections/create", {
            "dbName": self.db_name,
            "collectionName": name,
            "dimension": int(dim),
            "metricType": metric_type(),
            "idType": "VarChar",
            "primaryFieldName": "vid",
            "vectorFieldName": "vector",
            "params": {"max_length": "128"},
        })

    def insert(self, collection: str, rows: list[dict], chunk: int = 200) -> int:
        name = assert_owned_collection(collection)
        for i in range(0, len(rows), chunk):
            self._post("/v2/vectordb/entities/insert", {
                "dbName": self.db_name,
                "collectionName": name,
                "data": rows[i : i + chunk],
            })
        return len(rows)

    def rebuild(self, collection: str, rows: list[dict], dim: int | None = None) -> None:
        name = assert_owned_collection(collection)
        if name in self.list_collections():
            self.drop(name)
        self.create(name, dim)
        self.insert(name, rows)

    def search(self, collection: str, vector: list[float], limit: int) -> list[dict]:
        name = assert_owned_collection(collection)
        data = self._post("/v2/vectordb/entities/search", {
            "dbName": self.db_name,
            "collectionName": name,
            "data": [vector],
            "limit": int(limit),
            "outputFields": ["vid", "kind", "name", "industry_code", "index_version", "model_version"],
        }) or []
        return [
            {
                "vid": str(hit.get("vid") or hit.get("id") or ""),
                "kind": str(hit.get("kind") or ""),
                "name": str(hit.get("name") or ""),
                "industry_code": str(hit.get("industry_code") or ""),
                "index_version": str(hit.get("index_version") or ""),
                "score": float(hit.get("distance") or 0.0),
            }
            for hit in data
        ]


def open_store():
    uri = _env("MILVUS_URI")
    return MilvusHttpStore(uri) if uri else MemoryStore()


# ------------------------------------------------------------------- 对外 API --

def rebuild(payload: dict | None = None, *, anchors: list[dict] | None = None, store=None) -> dict:
    payload = payload or {}
    store = store or open_store()
    dim = embed_dim()
    mv = model_version()
    collection = assert_owned_collection(payload.get("collection") or default_collection())
    meta = {
        "collection": collection,
        "store": store.kind,
        "db_name": getattr(store, "db_name", None),
        "model_version": mv,
        "dim": dim,
        "metric_type": metric_type(),
        "trace_id": current_trace_id(),
    }
    try:
        docs = load_anchors() if anchors is None else list(anchors)
    except Exception as exc:  # noqa: BLE001
        return error(f"锚点词表读取失败: {type(exc).__name__}: {exc}",
                     {**meta, "indexed": 0, "degraded": True})
    if not docs:
        return error("锚点词表为空（图点未稳定？），跳过 rebuild 并保留上一版 index_version",
                     {**meta, "indexed": 0, "degraded": True})

    index_version = time.strftime("%Y%m%d%H%M%S")
    try:
        vectors = embed_texts([d["text"] for d in docs])
    except EmbedUnavailable as exc:
        return error(f"embedding 不可用: {exc}", {**meta, "indexed": 0, "degraded": True})
    rows = [{
        "vid": d["vid"],
        "kind": d["kind"],
        "name": d["name"],
        "aliases": ",".join(d.get("aliases") or []),
        "text": d["text"],
        "industry_code": d.get("industry_code") or "",
        "graph_source": d.get("graph_source") or "dwd_chain",
        "model_version": mv,
        "index_version": index_version,
        "vector": vectors[i],
    } for i, d in enumerate(docs)]
    try:
        store.rebuild(collection, rows, dim)
    except (MilvusUnavailable, CollectionGuardError) as exc:
        return error(f"Milvus 不可用: {exc}", {**meta, "indexed": 0, "degraded": True})
    return ok({
        **meta,
        "indexed": len(rows),
        "index_version": index_version,
        "kinds": {k: sum(1 for d in docs if d["kind"] == k) for k in KINDS},
        "degraded": bool(store.degraded),
    })


def search(payload: dict | None = None, *, store=None) -> dict:
    payload = payload or {}
    store = store or open_store()
    collection = assert_owned_collection(payload.get("collection") or default_collection())
    meta = {
        "collection": collection,
        "store": store.kind,
        "source": "industry_embed",
        "model_version": model_version(),
        "trace_id": current_trace_id(),
    }
    query = str(payload.get("query") or "").strip()
    if not query:
        return error("query 为空", {**meta, "items": [], "index_version": "", "degraded": True})

    top_k = max(1, min(int(payload.get("top_k") or 8), 50))
    kinds = [k for k in (payload.get("kinds") or KINDS) if k in KINDS] or list(KINDS)
    min_score = float(payload.get("min_score") or 0.0)
    limit = top_k if len(kinds) == len(KINDS) else min(top_k * 4, 64)
    try:
        hits = store.search(collection, embed_text(query, is_query=True), limit)
    except EmbedUnavailable as exc:
        return error(f"embedding 不可用: {exc}",
                     {**meta, "items": [], "index_version": "", "degraded": True})
    except MilvusUnavailable as exc:
        return error(f"Milvus 不可用: {exc}",
                     {**meta, "items": [], "index_version": "", "degraded": True})

    items = [{
        "vid": h["vid"],
        "name": h.get("name") or "",
        "kind": h.get("kind") or "",
        "industry_code": h.get("industry_code") or "",
        "score": round(float(h.get("score") or 0.0), 6),
    } for h in hits if h.get("kind") in kinds and float(h.get("score") or 0.0) >= min_score][:top_k]
    return ok({
        **meta,
        "items": items,
        "index_version": next((str(h.get("index_version") or "") for h in hits), ""),
        "degraded": bool(store.degraded),
    })


# ---------------------------------------------------------------- 最小自检 --

def _self_check() -> None:
    """无外部依赖的闸门自检：失败即非 0 退出。"""
    assert split_anchor_tokens("半导体与集成电路") == ["半导体", "集成电路"]
    docs = anchor_docs(
        [{"chain_id": "INB01", "chain_name": "示范链"}],
        [{"node_id": "INB0101", "node_name": "上游环节", "chain_id": "INB01"}],
    )
    assert {d["vid"] for d in docs} == {"chain:INB01", "segment:INB0101"}
    os.environ.pop("MILVUS_DB_NAME", None)
    os.environ.pop("DB_NAME", None)
    os.environ.pop("ALLOW_MILVUS_DB_DEFAULT", None)
    try:
        milvus_db_name()
        raise AssertionError("未配置 DB 名应拒绝")
    except CollectionGuardError:
        pass
    os.environ["DB_NAME"] = "default"
    try:
        milvus_db_name()
        raise AssertionError("default 应拒绝")
    except CollectionGuardError:
        pass
    os.environ["MILVUS_DB_NAME"] = "gkxlumen"
    assert milvus_db_name() == "gkxlumen"
    store = MemoryStore()
    result = rebuild({"collection": default_collection()}, anchors=docs, store=store)
    assert result["code"] == 0 and result["data"]["indexed"] == 2, result
    print("industry_embed self-check OK")


if __name__ == "__main__":
    _self_check()

"""产业锚点向量索引（CROSS-VEC-PY-INDEX-L01）。

建库切面（02 §1.1）：产业链灌数末段调 `embed/rebuild` **一次**；业务重灌只消费
`embed/search`。`jobs/enrich` 跑批是 **CROSS-VEC-JOB-A-L01** 的叶，不在本模块。

物理引擎：现网 Milvus 2.4 standalone，走 HTTP v2 + stdlib urllib（仓内无 pymilvus，
`scripts/milvus_probe.py` 已验证该路线）。向量走集群内 TEI（`EMBED_BASE_URL`，
OpenAI 兼容 `/v1/embeddings`，dim 768，客户端不再 L2 归一）。`MILVUS_URI` 未配置
时退化为进程内内存索引；`EMBED_BASE_URL` 未设时向量退回 hashgram（仅本地 pytest）。
任一端点连不上则 **code≠0 + degraded**，绝不返回假 VID。

VID 只信图上链码（`chain:` / `segment:`），与 `graph_project.map_graph` 同一套映射；
向量分数**不是** `industry_link_code`，定码仍走图谱 FETCH。
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import time
import urllib.request

import httpx

from lumen_common.algorithms.chain.demo_guard import connect_chain_readonly
from lumen_common.algorithms.chain.graph_project import map_graph
from lumen_common.algorithms import policy  # noqa: F401  导入即把 vendor/entan-py 挂上 sys.path
from lumen_common.observability import current_trace_id
from lumen_common.response import error, ok

from polan.graph.entity import split_anchor_tokens  # noqa: E402  别名拆词与 L1 对码同源

# Milvus 2.4 只收 [A-Za-z0-9_] 且不以数字开头；连字符名会被 code 1100 拒绝。
DEFAULT_PREFIX = "gkxlumen_industry_"
DEFAULT_COLLECTION_SUFFIX = "anchor"
DB_NAME = "default"
METRIC_TYPE = "COSINE"
DIM = 768
# 现网 TEI `bge-base-zh-v1.5`（总控 §6.5）。返回向量已 L2 归一，客户端不再归一。
# `EMBED_BASE_URL` 未设时退回 stdlib blake2b（仅本地 pytest / MemoryStore，degraded）。
MODEL_VERSION = "bge-base-zh-v1.5-tei-1.8.3"
DEFAULT_EMBED_MODEL = "BAAI/bge-base-zh-v1.5"
# bge 非对称检索：query 侧加此前缀，锚点 / doc 侧不加（漏了召回会掉）。
QUERY_PREFIX = "为这个句子生成表示以用于检索相关文章："
EMBED_BATCH = 32
EMBED_RETRIES = 2
KINDS = ("chain", "segment")


class CollectionGuardError(RuntimeError):
    """写操作命中非本项目 collection。现网未开鉴权，本守卫是唯一防线。"""


class MilvusUnavailable(RuntimeError):
    """连不上 / 协议不对。调用方必须 degraded，不许兜假数据。"""


class EmbedUnavailable(RuntimeError):
    """TEI 不可用、空响应或 dim ≠ 768。调用方必须 degraded，不许兜假 VID。"""


# ------------------------------------------------------------------ 前缀守卫 --

def collection_prefix() -> str:
    """前缀真源 = env（k8s api.yaml / worker.yaml 注入），不在代码里写死业务名。"""
    prefix = os.environ.get("MILVUS_COLLECTION_PREFIX", DEFAULT_PREFIX).strip()
    if not _legal_name(prefix):
        raise CollectionGuardError(
            f"MILVUS_COLLECTION_PREFIX={prefix!r} 非法（空或含 Milvus 不收的字符），拒绝任何读写"
        )
    return prefix


def default_collection() -> str:
    return f"{collection_prefix()}{DEFAULT_COLLECTION_SUFFIX}"


def _legal_name(name: str) -> bool:
    text = str(name or "")
    if not text or text[0].isdigit():
        return False
    return all(ch.isascii() and (ch.isalnum() or ch == "_") for ch in text)


def assert_owned_collection(name: str | None) -> str:
    """create / drop / insert / delete / search 前必过：只允许本前缀 collection。

    现网 Milvus `authorizationEnabled=false`，同实例住着 `aip_kb_*`、
    `spk_id_speaker_embeddings` 等别的系统在用的库，任何能连 19530 的进程都是超级
    权限，一次手滑就能 drop 掉别人的库。

    ponytail: 前缀本身来自 env，运维把 env 改成别的系统前缀仍能绕过；账号级隔离要等
    运维打开 `authorizationEnabled` 并建受限角色（k8s/README.md 升级项）。
    """
    prefix = collection_prefix()
    text = str(name or "").strip()
    if not text.startswith(prefix) or not _legal_name(text):
        raise CollectionGuardError(
            f"拒绝操作 collection {text!r}：必须以 {prefix!r} 开头且只含 [A-Za-z0-9_]"
        )
    return text


# -------------------------------------------------------------------- 向量化 --

def _hashgram(text: str, dim: int) -> list[float]:
    """本地回退：字符 1/2/3-gram → 有符号哈希桶 → L2 归一。仅 `EMBED_BASE_URL` 未设时用。"""
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
    token = os.environ.get("EMBED_API_KEY", "").strip()
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
        vecs.append([float(x) for x in vec])  # TEI 已 L2 归一，客户端不再归一
    return vecs


def _embed_tei(texts: list[str], dim: int) -> list[list[float]]:
    base = os.environ.get("EMBED_BASE_URL", "").strip().rstrip("/")
    url = f"{base}/v1/embeddings"
    model = os.environ.get("EMBED_MODEL", DEFAULT_EMBED_MODEL).strip() or DEFAULT_EMBED_MODEL
    headers = _embed_headers()
    out: list[list[float]] = []
    timeout = httpx.Timeout(60.0, connect=5.0)
    with httpx.Client(timeout=timeout) as client:
        for i in range(0, len(texts), EMBED_BATCH):
            chunk = texts[i : i + EMBED_BATCH]
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


def embed_texts(texts: list[str], *, is_query: bool = False, dim: int = DIM) -> list[list[float]]:
    """批量向量化。query 侧加指令前缀；锚点 / doc 侧不加。"""
    if not texts:
        return []
    if not os.environ.get("EMBED_BASE_URL", "").strip():
        return [_hashgram(str(t or ""), dim) for t in texts]
    payloads = [(QUERY_PREFIX + str(t or "")) if is_query else str(t or "") for t in texts]
    return _embed_tei(payloads, dim)


def embed_text(text: str, dim: int = DIM, *, is_query: bool = False) -> list[float]:
    """单条向量化。现网走 TEI；无 `EMBED_BASE_URL` 时 hashgram 回退（不联网）。"""
    return embed_texts([text], is_query=is_query, dim=dim)[0]


def _cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))  # 两边都已 L2 归一


# ---------------------------------------------------------------- 锚点词表 --

def anchor_docs(chains: list[dict], nodes: list[dict]) -> list[dict]:
    """DWD 链表 → 锚点文档。VID 复用 map_graph，与图上 chain/segment 点同码。"""
    vertices = map_graph(chains, nodes, [], [])["vertices"]
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


def load_anchors() -> list[dict]:
    """只读 demo DWD 链表（闸门在 connect_chain_readonly 内，非 demo_ 库直接拒）。"""
    db = connect_chain_readonly()
    try:
        chains = db.query(f"SELECT * FROM `{db.dwd}`.`industry_chain` WHERE IFNULL(is_deleted,0)=0")
        nodes = db.query(f"SELECT * FROM `{db.dwd}`.`industry_chain_node` WHERE IFNULL(is_deleted,0)=0")
    finally:
        db.close()
    return anchor_docs(chains, nodes)


# ----------------------------------------------------------------- 存储后端 --

class MemoryStore:
    """进程内回退。语义与 Milvus 一致但**不持久化**，因此一律 degraded。"""

    kind = "memory"
    degraded = True
    _data: dict[str, list[dict]] = {}

    def rebuild(self, collection: str, rows: list[dict], dim: int = DIM) -> None:
        self._data[assert_owned_collection(collection)] = [dict(r) for r in rows]

    def search(self, collection: str, vector: list[float], limit: int) -> list[dict]:
        rows = self._data.get(assert_owned_collection(collection)) or []
        hits = [{**r, "score": _cosine(vector, r["vector"])} for r in rows]
        hits.sort(key=lambda h: h["score"], reverse=True)
        return hits[:limit]


class MilvusHttpStore:
    """Milvus 2.4 HTTP v2（stdlib urllib）。不引 pymilvus，见 handoff 依赖一节。"""

    kind = "milvus"
    degraded = False

    def __init__(self, uri: str, timeout: int = 10) -> None:
        self.uri = uri.rstrip("/")
        self.timeout = timeout

    def _post(self, path: str, body: dict):
        headers = {"Content-Type": "application/json"}
        token = os.environ.get("MILVUS_TOKEN", "").strip()
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
        except (OSError, ValueError) as exc:  # URLError / HTTPError / socket / 非 JSON
            raise MilvusUnavailable(f"{path}: {type(exc).__name__}: {exc}") from exc
        if payload.get("code") not in (0, 200):
            raise MilvusUnavailable(f"{path} 返回 {payload}")
        return payload.get("data")

    def list_collections(self) -> list[str]:
        return list(self._post("/v2/vectordb/collections/list", {"dbName": DB_NAME}) or [])

    def drop(self, collection: str) -> None:
        name = assert_owned_collection(collection)
        self._post("/v2/vectordb/collections/drop", {"dbName": DB_NAME, "collectionName": name})

    def create(self, collection: str, dim: int = DIM) -> None:
        name = assert_owned_collection(collection)
        self._post("/v2/vectordb/collections/create", {
            "dbName": DB_NAME,
            "collectionName": name,
            "dimension": int(dim),
            "metricType": METRIC_TYPE,
            "idType": "VarChar",
            "primaryFieldName": "vid",
            "vectorFieldName": "vector",
            # 2.4 HTTP v2 的 params 是 map[string]string，数字必须传字符串（否则 code 1801）
            "params": {"max_length": "128"},
        })

    def insert(self, collection: str, rows: list[dict], chunk: int = 200) -> int:
        name = assert_owned_collection(collection)
        for i in range(0, len(rows), chunk):
            self._post("/v2/vectordb/entities/insert", {
                "dbName": DB_NAME,
                "collectionName": name,
                "data": rows[i : i + chunk],
            })
        return len(rows)

    def rebuild(self, collection: str, rows: list[dict], dim: int = DIM) -> None:
        name = assert_owned_collection(collection)
        if name in self.list_collections():
            self.drop(name)
        self.create(name, dim)
        self.insert(name, rows)

    def search(self, collection: str, vector: list[float], limit: int) -> list[dict]:
        name = assert_owned_collection(collection)
        data = self._post("/v2/vectordb/entities/search", {
            "dbName": DB_NAME,
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
    """`MILVUS_URI` 有值 → 真库；空 → 内存回退（degraded）。"""
    uri = os.environ.get("MILVUS_URI", "").strip()
    return MilvusHttpStore(uri) if uri else MemoryStore()


# ------------------------------------------------------------------- 对外 API --

def rebuild(payload: dict | None = None, *, anchors: list[dict] | None = None, store=None) -> dict:
    """整库一次重建。禁止逐行 embed；空词表则跳过、保留上一版索引。"""
    payload = payload or {}
    store = store or open_store()
    collection = assert_owned_collection(payload.get("collection") or default_collection())
    meta = {
        "collection": collection,
        "store": store.kind,
        "model_version": MODEL_VERSION,
        "dim": DIM,
        "metric_type": METRIC_TYPE,
        "trace_id": current_trace_id(),
    }
    try:
        docs = load_anchors() if anchors is None else list(anchors)
    except Exception as exc:  # noqa: BLE001 读不到链表就诚实红，不建空索引
        return error(f"锚点词表读取失败: {type(exc).__name__}: {exc}",
                     {**meta, "indexed": 0, "degraded": True})
    if not docs:
        return error("锚点词表为空（图点未稳定？），跳过 rebuild 并保留上一版 index_version",
                     {**meta, "indexed": 0, "degraded": True})

    index_version = time.strftime("%Y%m%d%H%M%S")
    try:
        vectors = embed_texts([d["text"] for d in docs])  # 锚点侧不加 query 前缀
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
        "model_version": MODEL_VERSION,
        "index_version": index_version,
        "vector": vectors[i],
    } for i, d in enumerate(docs)]
    try:
        store.rebuild(collection, rows, DIM)
    except MilvusUnavailable as exc:
        return error(f"Milvus 不可用: {exc}", {**meta, "indexed": 0, "degraded": True})
    return ok({
        **meta,
        "indexed": len(rows),
        "index_version": index_version,
        "kinds": {k: sum(1 for d in docs if d["kind"] == k) for k in KINDS},
        "degraded": bool(store.degraded),
    })


def search(payload: dict | None = None, *, store=None) -> dict:
    """单条 top-k 候选。只返回图上 VID + 名字 + 分数；分数不是 industry_link_code。"""
    payload = payload or {}
    store = store or open_store()
    collection = assert_owned_collection(payload.get("collection") or default_collection())
    meta = {
        "collection": collection,
        "store": store.kind,
        "source": "industry_embed",
        "model_version": MODEL_VERSION,
        "trace_id": current_trace_id(),
    }
    query = str(payload.get("query") or "").strip()
    if not query:
        return error("query 为空", {**meta, "items": [], "index_version": "", "degraded": True})

    top_k = max(1, min(int(payload.get("top_k") or 8), 50))
    kinds = [k for k in (payload.get("kinds") or KINDS) if k in KINDS] or list(KINDS)
    min_score = float(payload.get("min_score") or 0.0)
    # kinds 是子集时多取一些再客户端筛，省掉对动态字段 filter 语法的依赖。
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

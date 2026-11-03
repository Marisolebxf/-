"""DWD relation → Nebula Demo space ``demo_gkx_chain``.

Tag/Edge names are frozen from graph-chain.md / DATA-CHAIN-db-design §7.
Unmapped v5 types are skipped and counted; this module does not invent schema.

灌链末段挂钩（CROSS-VEC-CHAIN-HOOK-L01，02-概要设计 §1.1 建库切面）：DWD 链表读完且
上图 chain/segment 点写稳之后，在 ``project_graph`` 末尾调 **一次**
``industry_embed.rebuild``。这是整条灌链**唯一**的 rebuild 调用点；政策 / 企业等业务
重灌只消费 ``embed/search``，不建库。点未稳定（上图失败 / 点数异常 / 词表空）则跳过，
不动上一版索引；rebuild 失败也**不回滚**已成功的 DWD 读与上图写，但结果里如实标 failed。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import threading
import time
from collections import Counter
from typing import Any, Callable

from lumen_common.algorithms.chain.demo_guard import (
    ChainReadDB,
    NonDemoMysqlTargetError,
    assert_demo_mysql_targets,
    connect_chain_readonly,
)
from lumen_common.config import settings
from lumen_common.observability import current_trace_id

ALLOWED_TAGS = ("chain", "segment", "enterprise", "institution")
ALLOWED_EDGES = ("belongs_to", "participates", "supplies", "depends_on")
DEFAULT_SPACE = "demo_gkx_chain"
FORMAL_SPACE = "gkx_chain"
ESCALATE_TO = "human:李伟"
_SPACE_OK = re.compile(r"^demo_[A-Za-z0-9_]+$")
_POOL = None
_POOL_LOCK = threading.Lock()

# node_rel.relation_type → Edge. Only types whose §7 meaning is segment→segment.
NODE_REL_EDGE = {
    "upstream": "depends_on",
    "downstream": "depends_on",
    "depends": "depends_on",
    "depends_on": "depends_on",
    "dependency": "depends_on",
    "上下游": "depends_on",
    "依赖": "depends_on",
}

# entity_rel (entity_type, relation_type) → Edge. Nebula belongs_to is segment→chain;
# DWD belongs_to on enterprise is projected to participates (existing Edge), not a new name.
ENTITY_REL_EDGE = {
    ("enterprise", "belongs_to"): "participates",
    ("enterprise", "participates"): "participates",
    ("enterprise", "participates_in"): "participates",
    ("enterprise", "所属"): "participates",
    ("enterprise", "参与"): "participates",
    ("institution", "belongs_to"): "participates",
    ("institution", "participates"): "participates",
    ("institution", "participates_in"): "participates",
    ("institution", "所属"): "participates",
    ("institution", "参与"): "participates",
    ("service_institution", "belongs_to"): "participates",
    ("service_institution", "participates"): "participates",
    ("service_institution", "所属"): "participates",
    ("service_institution", "参与"): "participates",
}

ENTITY_TAG = {
    "enterprise": "enterprise",
    "institution": "institution",
    "service_institution": "institution",
}

TAG_DDL = {
    "chain": "name string, chain_id string, chain_stage string, node_level int, is_key_node bool, enterprise_count int, weight double, props string",
    "segment": "name string, segment_key string, chain_id string, chain_stage string, weight double, props string",
    "enterprise": "name string, enterprise_code string, chain_role string, weight double, props string",
    "institution": "name string, institution_type string, weight double, props string",
}
EDGE_DDL = {
    "belongs_to": "node_stage string, weight double, props string",
    "participates": "chain_role string, participation_depth double, chain_score double, props string",
    "supplies": "relation_type string, relation_strength double, props string",
    "depends_on": "dependency_type string, weight double, props string",
}

OPEN_ITEMS = (
    "DWD entity_rel.belongs_to（企业→节点）与 Nebula belongs_to（环节→链）撞名；本单投 participates",
    "entity_type=product / produced_at：无 product Tag，跳过",
    "event_entity_rel：无 event Tag，整表跳过",
    "node_rel 供需/替代/协同：无对应 Edge，跳过",
    "supplies 设计为企业→企业，Demo DWD 无该结构，本单不造边",
    "graph-chain.md status=draft；Tag/Edge 与 v5 终裁待 human:李伟",
)


class NonDemoNebulaSpaceError(RuntimeError):
    """CHAIN may only write a demo_ Nebula space."""


class GraphProjectError(RuntimeError):
    def __init__(self, detail: str, status: str = "failed"):
        super().__init__(detail)
        self.detail = detail
        self.status = status


def is_demo_nebula_space(name: str) -> bool:
    return bool(_SPACE_OK.match(str(name or "")))


def assert_demo_nebula_space(name: str | None = None) -> str:
    space = str(name or nebula_conf()["space"])
    if space == FORMAL_SPACE or not is_demo_nebula_space(space):
        raise NonDemoNebulaSpaceError(f"refusing non-demo Nebula space: {space}")
    return space


def nebula_conf() -> dict[str, Any]:
    chain = (settings().get("chain") or {}).get("nebula") or {}
    enabled = os.environ.get("LUMEN_ALGO_CHAIN_NEBULA_ENABLED", chain.get("enabled", True))
    if isinstance(enabled, str):
        enabled = enabled.strip().lower() in ("1", "true", "yes")
    return {
        "enabled": bool(enabled),
        "hosts": os.environ.get(
            "LUMEN_ALGO_NEBULA_HOSTS",
            os.environ.get("GKX_NEBULA_HOSTS", chain.get("hosts", "10.50.75.136:9669")),
        ),
        "user": os.environ.get(
            "LUMEN_ALGO_NEBULA_USER",
            os.environ.get("GKX_NEBULA_USER", chain.get("user", "root")),
        ),
        "password": os.environ.get(
            "LUMEN_ALGO_NEBULA_PASSWORD",
            os.environ.get("GKX_NEBULA_PASSWORD", chain.get("password", "")),
        ),
        "space": os.environ.get(
            "LUMEN_ALGO_CHAIN_NEBULA_SPACE", chain.get("space", DEFAULT_SPACE)
        ),
        "partition_num": int(chain.get("partition_num", 10)),
        "replica_factor": int(chain.get("replica_factor", 1)),
        "vid_length": int(chain.get("vid_length", 80)),
    }


def _q(value: Any) -> str:
    return '"' + str(value or "").replace("\\", "\\\\").replace('"', '\\"') + '"'


def _f(value: Any) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def _i(value: Any) -> int:
    try:
        return int(float(value or 0))
    except (TypeError, ValueError):
        return 0


def _b(value: Any) -> str:
    return "true" if value in (True, 1, "1", "true", "True") else "false"


def _ext(row: dict) -> dict:
    raw = row.get("ext")
    if isinstance(raw, dict):
        return raw
    if not raw:
        return {}
    try:
        parsed = json.loads(raw)
        return parsed if isinstance(parsed, dict) else {}
    except (TypeError, ValueError, json.JSONDecodeError):
        return {}


def _props(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"), default=str)


def _vid(prefix: str, raw: Any, vid_length: int) -> str | None:
    text = str(raw or "").strip()
    if not text:
        return None
    vid = f"{prefix}{text}"
    if len(vid) > vid_length:
        return None
    return vid


def _skip(counter: Counter, reason: str, n: int = 1) -> None:
    counter[reason] += n


def map_graph(
    chains: list[dict],
    nodes: list[dict],
    node_rels: list[dict],
    entity_rels: list[dict],
    event_rels: list[dict] | None = None,
    *,
    vid_length: int = 80,
) -> dict[str, Any]:
    """Pure DWD→§7 mapping. No Nebula I/O."""
    skipped: Counter = Counter()
    vertices: list[dict] = []
    edges: list[dict] = []
    seen_vid: set[str] = set()

    def add_vertex(tag: str, vid: str | None, props: dict, skip_reason: str) -> str | None:
        if tag not in ALLOWED_TAGS:
            _skip(skipped, skip_reason)
            return None
        if not vid:
            _skip(skipped, "vid_invalid")
            return None
        if vid in seen_vid:
            return vid
        seen_vid.add(vid)
        vertices.append({"tag": tag, "vid": vid, **props})
        return vid

    for row in chains:
        vid = _vid("chain:", row.get("chain_id"), vid_length)
        add_vertex(
            "chain",
            vid,
            {
                "name": row.get("chain_name") or row.get("chain_id"),
                "chain_id": row.get("chain_id"),
                "chain_stage": "",
                "node_level": _i(row.get("chain_level")),
                "is_key_node": False,
                "enterprise_count": 0,
                "weight": 0.0,
                "props": _props({"industry_id": row.get("industry_id"), "chain_tier": row.get("chain_tier")}),
            },
            "unmapped_tag",
        )

    for row in nodes:
        vid = _vid("segment:", row.get("node_id"), vid_length)
        chain_vid = _vid("chain:", row.get("chain_id"), vid_length)
        if not add_vertex(
            "segment",
            vid,
            {
                "name": row.get("node_name") or row.get("node_id"),
                "segment_key": row.get("node_id") or row.get("node_code"),
                "chain_id": row.get("chain_id"),
                "chain_stage": row.get("stage_code") or "",
                "weight": 0.0,
                "props": _props({"node_code": row.get("node_code"), "node_level": row.get("node_level")}),
            },
            "unmapped_tag",
        ):
            continue
        if chain_vid and chain_vid in seen_vid:
            edges.append(
                {
                    "edge": "belongs_to",
                    "src": vid,
                    "dst": chain_vid,
                    "node_stage": row.get("stage_code") or "",
                    "weight": 0.0,
                    "props": _props({"source": "industry_chain_node.chain_id"}),
                }
            )
        else:
            _skip(skipped, "belongs_to_missing_chain")

    for row in node_rels:
        rel = str(row.get("relation_type") or "").strip()
        edge_name = NODE_REL_EDGE.get(rel)
        if edge_name != "depends_on":
            _skip(skipped, f"node_rel_unmapped:{rel or 'empty'}")
            continue
        src = _vid("segment:", row.get("source_node_id"), vid_length)
        dst = _vid("segment:", row.get("target_node_id"), vid_length)
        if str(row.get("relation_direction") or "").lower() == "reverse":
            src, dst = dst, src
        if not src or not dst or src == dst or src not in seen_vid or dst not in seen_vid:
            _skip(skipped, "node_rel_missing_vertex")
            continue
        edges.append(
            {
                "edge": "depends_on",
                "src": src,
                "dst": dst,
                "dependency_type": rel,
                "weight": _f(row.get("relation_weight")),
                "props": _props({"relation_id": row.get("relation_id"), "chain_id": row.get("chain_id")}),
            }
        )

    for row in entity_rels:
        etype = str(row.get("entity_type") or "").strip()
        rel = str(row.get("relation_type") or "").strip()
        tag = ENTITY_TAG.get(etype)
        edge_name = ENTITY_REL_EDGE.get((etype, rel))
        if not tag or not edge_name:
            _skip(skipped, f"entity_rel_unmapped:{etype or 'empty'}:{rel or 'empty'}")
            continue
        prefix = "ent:" if tag == "enterprise" else "inst:"
        vid = _vid(prefix, row.get("entity_id"), vid_length)
        ext = _ext(row)
        name = ext.get("company_name") or row.get("entity_id")
        added = add_vertex(
            tag,
            vid,
            {
                "name": name,
                "enterprise_code": row.get("entity_id") if tag == "enterprise" else "",
                "chain_role": row.get("role_type") or "",
                "institution_type": row.get("entity_subtype") or etype,
                "weight": 0.0,
                "props": _props({"relation_id": row.get("relation_id"), "dwd_relation_type": rel}),
            },
            "unmapped_tag",
        )
        if not added:
            continue
        dst = None
        if row.get("node_id"):
            dst = _vid("segment:", row.get("node_id"), vid_length)
        if not dst or dst not in seen_vid:
            dst = _vid("chain:", row.get("chain_id"), vid_length)
        if not dst or dst not in seen_vid:
            _skip(skipped, "entity_rel_missing_dst")
            continue
        edges.append(
            {
                "edge": "participates",
                "src": vid,
                "dst": dst,
                "chain_role": row.get("role_type") or "",
                "participation_depth": 0.0,
                "chain_score": 0.0,
                "props": _props({"relation_id": row.get("relation_id"), "dwd_relation_type": rel}),
            }
        )

    event_n = len(event_rels or [])
    if event_n:
        _skip(skipped, "event_entity_rel_no_event_tag", event_n)

    by_tag = Counter(v["tag"] for v in vertices)
    by_edge = Counter(e["edge"] for e in edges)
    unmapped = sum(v for k, v in skipped.items() if "unmapped" in k or k == "event_entity_rel_no_event_tag")
    return {
        "vertices": vertices,
        "edges": edges,
        "vertex_counts": {t: by_tag.get(t, 0) for t in ALLOWED_TAGS},
        "edge_counts": {e: by_edge.get(e, 0) for e in ALLOWED_EDGES},
        "skipped": dict(skipped),
        "skipped_total": int(sum(skipped.values())),
        "unmapped_total": int(unmapped),
        "escalate_to": ESCALATE_TO if unmapped else None,
        "open": list(OPEN_ITEMS),
    }


def load_nebula3():
    from nebula3.Config import Config
    from nebula3.gclient.net import ConnectionPool

    return Config, ConnectionPool


def _addresses(hosts: str) -> list[tuple[str, int]]:
    out = []
    for item in str(hosts).split(","):
        item = item.strip()
        if not item:
            continue
        ip, port = item.rsplit(":", 1)
        out.append((ip.strip(), int(port)))
    return out


def _get_pool(conf: dict):
    global _POOL
    if _POOL is not None:
        return _POOL
    with _POOL_LOCK:
        if _POOL is None:
            Config, ConnectionPool = load_nebula3()
            cfg = Config()
            cfg.max_connection_pool_size = 8
            pool = ConnectionPool()
            if not pool.init(_addresses(conf["hosts"]), cfg):
                raise GraphProjectError("Nebula 连接池初始化失败")
            _POOL = pool
    return _POOL


def reset_nebula_pool() -> None:
    global _POOL
    _POOL = None


class NebulaSink:
    """Write-only Demo space sink. Pattern from demo-algo-ent-analysis; first driver in this repo."""

    def __init__(self, conf: dict):
        self.conf = conf
        self.space = assert_demo_nebula_space(conf["space"])

    def _session(self, use_space: bool = True):
        sess = _get_pool(self.conf).get_session(self.conf["user"], self.conf["password"])
        if use_space:
            self._exec(sess, f"USE {self.space}")
        return sess

    def _exec(self, sess, ngql: str):
        result = sess.execute(ngql)
        if not result.is_succeeded():
            raise GraphProjectError(f"nGQL 失败: {result.error_msg()} :: {ngql[:160]}")
        return result

    def _exec_retry(self, sess, ngql: str, attempts: int = 6) -> None:
        last = None
        for _ in range(attempts):
            result = sess.execute(ngql)
            if result.is_succeeded():
                return
            last = result.error_msg()
            time.sleep(2)
        raise GraphProjectError(f"nGQL 失败: {last} :: {ngql[:160]}")

    def ensure_schema(self) -> None:
        space = self.space
        part = int(self.conf["partition_num"])
        replica = int(self.conf["replica_factor"])
        vid_len = int(self.conf["vid_length"])
        sess = self._session(use_space=False)
        try:
            self._exec(
                sess,
                f"CREATE SPACE IF NOT EXISTS {space} "
                f"(partition_num={part}, replica_factor={replica}, vid_type=FIXED_STRING({vid_len}))",
            )
            deadline = time.time() + 40
            while time.time() < deadline:
                if sess.execute(f"USE {space}").is_succeeded():
                    break
                time.sleep(1)
            else:
                raise GraphProjectError(f"space {space} 创建后不可 USE")
            self._exec(sess, f"USE {space}")
            for tag, ddl in TAG_DDL.items():
                self._exec(sess, f"CREATE TAG IF NOT EXISTS {tag} ({ddl})")
            for edge, ddl in EDGE_DDL.items():
                self._exec(sess, f"CREATE EDGE IF NOT EXISTS {edge} ({ddl})")
        finally:
            sess.release()
        time.sleep(2)

    def upsert(self, vertices: list[dict], edges: list[dict], chunk: int = 80) -> tuple[int, int]:
        sess = self._session()
        try:
            vc = self._insert_vertices(sess, vertices, chunk)
            ec = self._insert_edges(sess, edges, chunk)
            return vc, ec
        finally:
            sess.release()

    def _insert_vertices(self, sess, vertices: list[dict], chunk: int) -> int:
        grouped: dict[str, list[dict]] = {t: [] for t in ALLOWED_TAGS}
        for item in vertices:
            grouped[item["tag"]].append(item)
        total = 0
        for tag, rows in grouped.items():
            cols = TAG_DDL[tag].split(", ")
            names = [c.split()[0] for c in cols]
            for i in range(0, len(rows), chunk):
                batch = rows[i : i + chunk]
                values = ",".join(f"{_q(row['vid'])}:({_vertex_tuple(row, names)})" for row in batch)
                self._exec_retry(sess, f"INSERT VERTEX {tag}({', '.join(names)}) VALUES {values}")
                total += len(batch)
        return total

    def _insert_edges(self, sess, edges: list[dict], chunk: int) -> int:
        grouped: dict[str, list[dict]] = {e: [] for e in ALLOWED_EDGES}
        for item in edges:
            grouped[item["edge"]].append(item)
        total = 0
        for edge, rows in grouped.items():
            cols = EDGE_DDL[edge].split(", ")
            names = [c.split()[0] for c in cols]
            for i in range(0, len(rows), chunk):
                batch = rows[i : i + chunk]
                values = ",".join(
                    f"{_q(row['src'])}->{_q(row['dst'])}:({_edge_tuple(row, names)})" for row in batch
                )
                self._exec_retry(sess, f"INSERT EDGE {edge}({', '.join(names)}) VALUES {values}")
                total += len(batch)
        return total


def _vertex_tuple(row: dict, names: list[str]) -> str:
    parts = []
    for name in names:
        value = row.get(name)
        if name in ("node_level", "enterprise_count"):
            parts.append(str(_i(value)))
        elif name == "is_key_node":
            parts.append(_b(value))
        elif name == "weight":
            parts.append(str(_f(value)))
        else:
            parts.append(_q(value))
    return ", ".join(parts)


def _edge_tuple(row: dict, names: list[str]) -> str:
    parts = []
    for name in names:
        value = row.get(name)
        if name in ("weight", "participation_depth", "chain_score", "relation_strength"):
            parts.append(str(_f(value)))
        else:
            parts.append(_q(value))
    return ", ".join(parts)


def _query_table(db: ChainReadDB, table: str) -> tuple[list[dict], str | None]:
    sql = f"SELECT * FROM `{db.dwd}`.`{table}` WHERE IFNULL(is_deleted,0)=0"
    try:
        return db.query(sql), None
    except Exception as exc:  # noqa: BLE001
        return [], f"{table}: {type(exc).__name__}: {exc}"


def _empty_result(**extra: Any) -> dict[str, Any]:
    body = {
        "status": extra.pop("status", "failed"),
        "space": extra.pop("space", None),
        "source": extra.pop("source", "none"),
        "wrote": False,
        "vertex_counts": {t: 0 for t in ALLOWED_TAGS},
        "edge_counts": {e: 0 for e in ALLOWED_EDGES},
        "vertices_written": 0,
        "edges_written": 0,
        "skipped": extra.pop("skipped", {}),
        "skipped_total": extra.pop("skipped_total", 0),
        "unmapped_total": extra.pop("unmapped_total", 0),
        "escalate_to": extra.pop("escalate_to", ESCALATE_TO),
        "open": list(OPEN_ITEMS),
        "detail": extra.pop("detail", ""),
        "industry_index": _index_block("skipped", "上图未完成，未调 rebuild；上一版索引保持不变"),
        "industry_index_version": None,
        "trace_id": current_trace_id(),
        "neo4j": False,
    }
    body.update(extra)
    return body


def _index_block(status: str, detail: str, *, index_version: Any = None, indexed: Any = 0) -> dict[str, Any]:
    """灌链末段索引结果。``status`` ∈ ok / skipped / failed，不存在「静默成功」。"""
    return {
        "status": status,
        "index_version": index_version,
        "indexed": _i(indexed),
        "detail": detail,
    }


def _index_skip_reason(result: dict[str, Any], anchors: list[dict]) -> str:
    """点未稳定的原因；空串 = chain/segment VID 稳定，可以建索引。"""
    if result.get("table_errors"):
        return f"DWD 链表读取有错 {result['table_errors']}，锚点不可信"
    counts = result.get("vertex_counts") or {}
    chain_n, segment_n = _i(counts.get("chain")), _i(counts.get("segment"))
    if not chain_n or not segment_n:
        return f"链/环节点位数量异常（chain={chain_n} segment={segment_n}）"
    written = _i(result.get("vertices_written"))
    if written < chain_n + segment_n:
        return f"上图写入点数 {written} < 锚点点数 {chain_n + segment_n}"
    if not anchors:
        return "锚点词表为空（链表无可索引的名字）"
    return ""


def _hook_industry_index(result: dict[str, Any], chains: list[dict], nodes: list[dict]) -> None:
    """灌链唯一的 rebuild 调用点。就地改写 ``result``，绝不抛给上图路径。

    ``industry_embed`` 反过来依赖本模块的 ``map_graph``，故延迟导入避免循环。
    锚点直接用本次上图读到的同一批 DWD 行，索引与图点同源、也省掉第二次读库。
    """
    try:
        from lumen_common.algorithms.industry_embed import anchor_docs, rebuild  # noqa: PLC0415

        anchors = anchor_docs(chains, nodes)
        reason = _index_skip_reason(result, anchors)
        if reason:
            result["industry_index"] = _index_block(
                "skipped", f"点未稳定，跳过 rebuild，保留上一版 index_version：{reason}"
            )
            result["detail"] += f" | industry_index=skipped: {reason}"
            return
        response = rebuild({}, anchors=anchors)
        data = response.get("data") or {}
    except Exception as exc:  # noqa: BLE001 索引失败不得回滚已成功的 DWD/上图
        result["industry_index"] = _index_block("failed", f"{type(exc).__name__}: {exc}")
        result["detail"] += f" | industry_index=failed: {type(exc).__name__}: {exc}"
        return
    if response.get("code") != 0:
        detail = str(response.get("msg") or "rebuild 失败")
        result["industry_index"] = _index_block("failed", detail)
        result["detail"] += f" | industry_index=failed: {detail}"
        return
    result["industry_index"] = _index_block(
        "ok",
        "灌链末段一次 rebuild",
        index_version=data.get("index_version"),
        indexed=data.get("indexed"),
    )
    result["industry_index_version"] = data.get("index_version")
    result["detail"] += (
        f" | industry_index=ok: version={data.get('index_version')} indexed={data.get('indexed')}"
    )


def project_graph(
    payload: dict | None = None,
    *,
    sink: Any = None,
    load_nebula: Callable | None = None,
) -> dict[str, Any]:
    """Project Demo DWD rels into demo_gkx_chain. Never reports ok on a failed write."""
    payload = payload or {}
    dry_run = bool(payload.get("dry_run"))
    ensure = payload.get("ensure_schema", True)
    assert_demo_mysql_targets()
    conf = nebula_conf()
    space = assert_demo_nebula_space(payload.get("space") or conf["space"])
    try:
        db = connect_chain_readonly()
    except NonDemoMysqlTargetError:
        raise
    except Exception as exc:  # noqa: BLE001
        return _empty_result(
            status="failed",
            space=space,
            detail=f"mysql: {type(exc).__name__}: {exc}",
        )
    table_errors: list[str] = []
    try:
        chains, err = _query_table(db, "industry_chain")
        if err:
            table_errors.append(err)
        nodes, err = _query_table(db, "industry_chain_node")
        if err:
            table_errors.append(err)
        node_rels, err = _query_table(db, "industry_chain_node_rel")
        if err:
            table_errors.append(err)
        entity_rels, err = _query_table(db, "industry_chain_entity_rel")
        if err:
            table_errors.append(err)
        event_rels, err = _query_table(db, "industry_chain_event_entity_rel")
        if err:
            table_errors.append(err)
            event_rels = []
    finally:
        db.close()

    mapped = map_graph(chains, nodes, node_rels, entity_rels, event_rels, vid_length=int(conf["vid_length"]))
    result = {
        "status": "dry_run" if dry_run else "failed",
        "space": space,
        "source": "none",
        "wrote": False,
        "vertex_counts": mapped["vertex_counts"],
        "edge_counts": mapped["edge_counts"],
        "vertices_written": 0,
        "edges_written": 0,
        "skipped": mapped["skipped"],
        "skipped_total": mapped["skipped_total"],
        "unmapped_total": mapped["unmapped_total"],
        "escalate_to": mapped["escalate_to"] or (ESCALATE_TO if mapped["skipped_total"] else None),
        "open": mapped["open"],
        "dwd_rows": {
            "industry_chain": len(chains),
            "industry_chain_node": len(nodes),
            "industry_chain_node_rel": len(node_rels),
            "industry_chain_entity_rel": len(entity_rels),
            "industry_chain_event_entity_rel": len(event_rels),
        },
        "table_errors": table_errors,
        "detail": "",
        "industry_index": _index_block("skipped", "上图未完成，未调 rebuild；上一版索引保持不变"),
        "industry_index_version": None,
        "trace_id": current_trace_id(),
        "neo4j": False,
    }
    if dry_run:
        result["status"] = "dry_run"
        result["detail"] = "mapping only; Nebula not written"
        return result
    if not conf["enabled"]:
        result["status"] = "skipped"
        result["detail"] = "nebula.enabled=false"
        return result

    importer = load_nebula or load_nebula3
    try:
        importer()
    except ImportError:
        result["status"] = "failed"
        result["detail"] = "nebula3 client not installed"
        return result
    except Exception as exc:  # noqa: BLE001
        result["status"] = "failed"
        result["detail"] = f"{type(exc).__name__}: {exc}"
        return result

    try:
        writer = sink or NebulaSink(conf)
        if ensure and hasattr(writer, "ensure_schema"):
            writer.ensure_schema()
        vc, ec = writer.upsert(mapped["vertices"], mapped["edges"])
    except NonDemoNebulaSpaceError:
        raise
    except Exception as exc:  # noqa: BLE001
        result["status"] = "failed"
        result["detail"] = f"{type(exc).__name__}: {exc}"
        return result

    result["status"] = "ok"
    result["source"] = "nebula"
    result["wrote"] = True
    result["vertices_written"] = int(vc)
    result["edges_written"] = int(ec)
    result["detail"] = f"projected space={space} vertices={vc} edges={ec} skipped={mapped['skipped_total']}"
    _hook_industry_index(result, chains, nodes)
    return result


def self_check() -> dict[str, Any]:
    sample = map_graph(
        [{"chain_id": "INB13", "chain_name": "集成电路", "chain_level": 0, "industry_id": "INB13", "chain_tier": "L0"}],
        [
            {"node_id": "INB1301", "chain_id": "INB13", "node_name": "设计", "node_code": "INB1301", "stage_code": "upstream", "node_level": 2},
            {"node_id": "INB1302", "chain_id": "INB13", "node_name": "制造", "node_code": "INB1302", "stage_code": "midstream", "node_level": 2},
        ],
        [
            {"source_node_id": "INB1301", "target_node_id": "INB1302", "relation_type": "upstream", "relation_id": "r1"},
            {"source_node_id": "INB1301", "target_node_id": "INB1302", "relation_type": "替代", "relation_id": "r2"},
        ],
        [
            {"entity_type": "enterprise", "entity_id": "91110000MA001", "relation_type": "belongs_to", "chain_id": "INB13", "node_id": "INB1301", "role_type": "participant", "ext": {"company_name": "demo"}},
            {"entity_type": "product", "entity_id": "p:1", "relation_type": "produced_at", "chain_id": "INB13", "node_id": "INB1301"},
        ],
        [{"relation_type": "publisher", "event_id": "news:1", "entity_id": "x"}],
    )
    assert sample["vertex_counts"]["chain"] == 1
    assert sample["vertex_counts"]["segment"] == 2
    assert sample["edge_counts"]["depends_on"] == 1
    assert sample["vertex_counts"]["enterprise"] == 1
    assert sample["edge_counts"]["belongs_to"] == 1
    assert sample["edge_counts"]["participates"] == 1
    assert sample["skipped"]["entity_rel_unmapped:product:produced_at"] == 1
    assert sample["skipped"]["event_entity_rel_no_event_tag"] == 1
    assert "node_rel_unmapped:替代" in sample["skipped"]
    assert sample["escalate_to"] == ESCALATE_TO
    try:
        assert_demo_nebula_space(FORMAL_SPACE)
        raise AssertionError("gkx_chain must be refused")
    except NonDemoNebulaSpaceError:
        pass
    live = project_graph({"dry_run": True})
    return {"mapping": {k: sample[k] for k in ("vertex_counts", "edge_counts", "skipped", "escalate_to")}, "dry_run": live}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CHAIN DWD → Nebula demo_gkx_chain")
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    if args.self_check:
        print(json.dumps(self_check(), ensure_ascii=False, default=str, indent=2))
        return 0
    print(json.dumps(project_graph({"dry_run": args.dry_run}), ensure_ascii=False, default=str, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""产业链环节抽取规则。从本侧 demo 算子摘出，不连库。

对照：
- repos/demo-algo-science/chainan/graph/graph_ops.py
- repos/demo-algo-science/chainan/graph/nebula_project.py 的 NODE_REL_EDGE、ENTITY_REL_EDGE

空间名不在这里。燕大写入 gkx_chain。
不生成 Tag chain。parent_child 不会变成 depends_on。
"""

from __future__ import annotations

VID_MAX = 80
DEPENDS_TYPES = frozenset({
    "upstream", "downstream", "depends", "depends_on", "dependency", "上下游", "依赖",
})
PARTICIPATES_TYPES = frozenset({
    "belongs_to", "participates", "participates_in", "所属", "参与",
})
PARTICIPATES_ENTITY = frozenset({"enterprise", "service_institution"})


def _vid(prefix: str, raw) -> str | None:
    text = str(raw or "").strip()
    if not text:
        return None
    vid = text if text.startswith(prefix) else f"{prefix}{text}"
    if len(vid) > VID_MAX:
        return None
    return vid


def segment_vid(node_id) -> str | None:
    return _vid("segment:", node_id)


def depends_on_edge(row: dict, segment_exists: set[str]) -> dict | None:
    """白名单才返回。reverse 对调两端。两端都要已经在图上。"""
    rel = str(row.get("relation_type") or "").strip()
    if rel not in DEPENDS_TYPES:
        return None
    src = segment_vid(row.get("source_node_id"))
    dst = segment_vid(row.get("target_node_id"))
    if str(row.get("relation_direction") or "").lower() == "reverse":
        src, dst = dst, src
    if not src or not dst or src == dst:
        return None
    if src not in segment_exists or dst not in segment_exists:
        return None
    weight = row.get("relation_weight")
    try:
        weight_n = float(weight or 0)
    except (TypeError, ValueError):
        weight_n = 0.0
    return {
        "edge": "depends_on",
        "src": src,
        "dst": dst,
        "dependency_type": rel,
        "weight": weight_n,
        "props": {"relation_id": row.get("relation_id")},
    }


def participates_edge(row: dict, *, src_exists: bool, segment_exists: bool) -> dict | None:
    """企业或服务机构 → 已有环节。不造点。schema 的 participates 没有属性列。"""
    if str(row.get("entity_type") or "").strip() not in PARTICIPATES_ENTITY:
        return None
    if str(row.get("relation_type") or "").strip() not in PARTICIPATES_TYPES:
        return None
    kind = str(row.get("entity_type") or "").strip()
    prefix = "ent:" if kind == "enterprise" else "inst:"
    src = _vid(prefix, row.get("entity_id"))
    dst = segment_vid(row.get("node_id"))
    if not src or not dst or not src_exists or not segment_exists:
        return None
    return {"edge": "participates", "src": src, "dst": dst}


def _self_check() -> None:
    assert segment_vid("N1") == "segment:N1"
    assert segment_vid("segment:N1") == "segment:N1"
    assert segment_vid("") is None
    assert segment_vid("x" * 80) is None
    exist = {"segment:A", "segment:B"}
    parent = depends_on_edge(
        {"source_node_id": "A", "target_node_id": "B", "relation_type": "parent_child"},
        exist,
    )
    assert parent is None
    rev = depends_on_edge(
        {
            "source_node_id": "A",
            "target_node_id": "B",
            "relation_type": "upstream",
            "relation_direction": "reverse",
            "relation_weight": "2",
            "relation_id": "r1",
        },
        exist,
    )
    assert rev["src"] == "segment:B" and rev["dst"] == "segment:A"
    assert rev["dependency_type"] == "upstream" and rev["weight"] == 2.0
    assert depends_on_edge(
        {"source_node_id": "A", "target_node_id": "A", "relation_type": "depends"},
        exist,
    ) is None
    hit = participates_edge(
        {"entity_type": "enterprise", "relation_type": "belongs_to", "entity_id": "E1", "node_id": "N1"},
        src_exists=True,
        segment_exists=True,
    )
    assert hit == {"edge": "participates", "src": "ent:E1", "dst": "segment:N1"}
    assert participates_edge(
        {"entity_type": "research", "relation_type": "belongs_to", "entity_id": "R1", "node_id": "N1"},
        src_exists=True,
        segment_exists=True,
    ) is None
    assert participates_edge(
        {"entity_type": "service_institution", "relation_type": "参与", "entity_id": "S1", "node_id": "N1"},
        src_exists=False,
        segment_exists=True,
    ) is None


if __name__ == "__main__":
    _self_check()

"""企业维抽取规则。从本侧 demo 算子摘出，不连库。

对照：
- repos/demo-algo-ent-analysis/entan/graph/ops.py
- repos/demo-algo-science/chainan/graph/nebula_project.py 的 ENTITY_REL_EDGE

空间名不在这里。燕大写入 gkx_chain。
cooperate_edge 只出有向一条，与现码一致。双向是两个方向各一条，现码没写第二条。
"""

from __future__ import annotations

VID_MAX = 80
PARTICIPATES_TYPES = frozenset({
    "belongs_to", "participates", "participates_in", "所属", "参与",
})


def ent_vid(org_id: str) -> str | None:
    text = str(org_id or "").strip()
    if not text:
        return None
    raw = text if text.startswith("ent:") else f"ent:{text}"
    if len(raw) > VID_MAX:
        return None
    return raw


def supply_edge(row: dict, known_orgs: set[str]) -> dict | None:
    src_org = str(row.get("org_id") or "").strip()
    dst_org = str(row.get("related_org_id") or "").strip()
    src, dst = ent_vid(src_org), ent_vid(dst_org)
    if not src or not dst or src_org not in known_orgs or dst_org not in known_orgs:
        return None
    strength = row.get("relation_strength")
    return {
        "edge": "supply",
        "src": src,
        "dst": dst,
        "weight": float(strength if strength not in (None, "") else 0.5),
        "props": {"type": row.get("relation_type")},
    }


def parent_sub_edge(row: dict, known_orgs: set[str]) -> dict | None:
    child = str(row.get("org_id") or "").strip()
    parent = str(row.get("parent_org_id") or "").strip()
    src, dst = ent_vid(parent), ent_vid(child)
    if not src or not dst or parent not in known_orgs or child not in known_orgs:
        return None
    ratio = row.get("ownership_ratio")
    return {
        "edge": "parent_sub",
        "src": src,
        "dst": dst,
        "weight": float(ratio or 0) / 100.0,
        "props": {"ownership": ratio},
    }


def cooperate_edge(row: dict, known_orgs: set[str]) -> dict | None:
    """有向一条。partner_type 不是 enterprise，或没有 partner_org_id，返回 None。"""
    if (row.get("partner_type") or "") != "enterprise":
        return None
    src_org = str(row.get("org_id") or "").strip()
    dst_org = str(row.get("partner_org_id") or "").strip()
    src, dst = ent_vid(src_org), ent_vid(dst_org)
    if not src or not dst or src_org not in known_orgs or dst_org not in known_orgs:
        return None
    count = row.get("project_count")
    return {
        "edge": "cooperate",
        "src": src,
        "dst": dst,
        "weight": float(count if count not in (None, "") else 1),
        "props": {"coop": row.get("cooperation_type")},
    }


def participates_edge(row: dict, segment_exists: bool, chain_exists: bool) -> dict | None:
    """产业链关联表。两端都要已经在图上。不造点。"""
    if str(row.get("entity_type") or "").strip() != "enterprise":
        return None
    if str(row.get("relation_type") or "").strip() not in PARTICIPATES_TYPES:
        return None
    src = ent_vid(row.get("entity_id"))
    node_id = str(row.get("node_id") or "").strip()
    chain_id = str(row.get("chain_id") or "").strip()
    dst = f"segment:{node_id}" if node_id and segment_exists else None
    if not dst and chain_id and chain_exists:
        dst = f"chain:{chain_id}"
    if not src or not dst or len(dst) > VID_MAX:
        return None
    return {"edge": "participates", "src": src, "dst": dst}


def _self_check() -> None:
    known = {"A", "B"}
    assert ent_vid("A") == "ent:A"
    assert ent_vid("ent:A") == "ent:A"
    assert ent_vid("") is None
    assert ent_vid("x" * 80) is None
    assert supply_edge(
        {"org_id": "A", "related_org_id": "B", "relation_type": "raw", "relation_strength": None},
        known,
    )["weight"] == 0.5
    assert supply_edge({"org_id": "A", "related_org_id": "NO", "relation_strength": 1}, known) is None
    parent = parent_sub_edge({"org_id": "B", "parent_org_id": "A", "ownership_ratio": 60}, known)
    assert parent["src"] == "ent:A" and parent["dst"] == "ent:B" and parent["weight"] == 0.6
    assert cooperate_edge(
        {"org_id": "A", "partner_type": "enterprise", "partner_org_id": "", "partner_name": "甲"},
        known,
    ) is None
    assert cooperate_edge(
        {"org_id": "A", "partner_type": "talent", "partner_org_id": "B"},
        known,
    ) is None
    one = cooperate_edge(
        {"org_id": "A", "partner_type": "enterprise", "partner_org_id": "B", "project_count": None},
        known,
    )
    assert one["src"] == "ent:A" and one["dst"] == "ent:B" and one["weight"] == 1
    hit = participates_edge(
        {"entity_type": "enterprise", "relation_type": "所属", "entity_id": "A", "node_id": "N1", "chain_id": "C1"},
        True,
        True,
    )
    assert hit["dst"] == "segment:N1"
    miss = participates_edge(
        {"entity_type": "enterprise", "relation_type": "所属", "entity_id": "A", "node_id": "N1"},
        False,
        False,
    )
    assert miss is None


if __name__ == "__main__":
    _self_check()

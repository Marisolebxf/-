"""Entity-ext quality helpers (M3-L01): event_type normalize + impact↔entity joint checks."""

from __future__ import annotations

from ..impact_pass import impact_duplicates_matter
from .schemas import EntityMention, EventType, TechNewsEventExt

EventTypeName = EventType

_CANONICAL: set[str] = {
    "product_release",
    "tech_breakthrough",
    "delivery",
    "certification",
    "collaboration",
    "policy_publish",
    "other",
}

# aliases → canonical (lower / stripped); Chinese kept as-is for substring match
_ALIAS_EXACT: dict[str, EventTypeName] = {
    "product_release": "product_release",
    "tech_breakthrough": "tech_breakthrough",
    "delivery": "delivery",
    "certification": "certification",
    "collaboration": "collaboration",
    "policy_publish": "policy_publish",
    "other": "other",
    "release": "product_release",
    "launch": "product_release",
    "product": "product_release",
    "breakthrough": "tech_breakthrough",
    "tech": "tech_breakthrough",
    "ship": "delivery",
    "mass_production": "delivery",
    "cert": "certification",
    "collab": "collaboration",
    "partner": "collaboration",
    "policy": "policy_publish",
    "unknown": "other",
    "misc": "other",
    "n/a": "other",
    "na": "other",
    "产品发布": "product_release",
    "发布": "product_release",
    "上线": "product_release",
    "推出": "product_release",
    "技术突破": "tech_breakthrough",
    "突破": "tech_breakthrough",
    "攻关": "tech_breakthrough",
    "交付": "delivery",
    "量产": "delivery",
    "投运": "delivery",
    "认证": "certification",
    "备案": "certification",
    "准入": "certification",
    "合作": "collaboration",
    "联合": "collaboration",
    "签约": "collaboration",
    "政策发布": "policy_publish",
    "印发": "policy_publish",
    "出台": "policy_publish",
    "其他": "other",
}


def normalize_event_type(raw) -> tuple[EventTypeName, list[str]]:
    """Map LLM/raw event_type to PDR enum; never raise. Returns (canonical, flags)."""
    flags: list[str] = []
    if raw is None:
        flags.append("event_type_defaulted_other")
        return "other", flags
    if not isinstance(raw, str):
        raw = str(raw)
    text = raw.strip()
    if not text:
        flags.append("event_type_defaulted_other")
        return "other", flags

    key = text.lower().replace("-", "_").replace(" ", "_")
    if key in _CANONICAL:
        return key, flags  # type: ignore[return-value]
    if key in _ALIAS_EXACT:
        flags.append(f"event_type_normalized_from:{text}")
        return _ALIAS_EXACT[key], flags
    if text in _ALIAS_EXACT:
        flags.append(f"event_type_normalized_from:{text}")
        return _ALIAS_EXACT[text], flags

    # soft Chinese / English contains
    for needle, canon in (
        ("breakthrough", "tech_breakthrough"),
        ("product_release", "product_release"),
        ("policy", "policy_publish"),
        ("certif", "certification"),
        ("collabor", "collaboration"),
        ("delivery", "delivery"),
        ("技术突破", "tech_breakthrough"),
        ("产品发布", "product_release"),
        ("政策", "policy_publish"),
    ):
        if needle in key or needle in text:
            flags.append(f"event_type_normalized_from:{text}")
            return canon, flags  # type: ignore[return-value]

    flags.append(f"event_type_unknown_mapped_other:{text}")
    return "other", flags


def _entity_name_set(entities: list[EntityMention]) -> set[str]:
    names: set[str] = set()
    for e in entities:
        if e.name:
            names.add(e.name.strip())
        if e.normalized:
            names.add(e.normalized.strip())
    return {n for n in names if n}


def _companies_in_entities(entities: list[EntityMention]) -> set[str]:
    out: set[str] = set()
    for e in entities:
        if e.type == "company":
            if e.name:
                out.add(e.name.strip())
            if e.normalized:
                out.add(e.normalized.strip())
    return {n for n in out if n}


def validate_impact_entity_joint(
    events: list[TechNewsEventExt],
    entities: list[EntityMention],
) -> list[str]:
    """
    Cross-check four-field impact/company with entity table.
    Mutates event.flags; returns meta.notes fragments (warnings, not hard fail).
    """
    notes: list[str] = []
    entity_names = _entity_name_set(entities)
    company_entities = _companies_in_entities(entities)

    for i, ev in enumerate(events):
        flags = list(ev.flags or [])

        if impact_duplicates_matter(ev.impact, ev.completed_matter):
            flags.append("impact_duplicates_matter")
            notes.append(f"joint_warn[{i}]:impact_duplicates_matter")

        if (ev.completed_matter or "").strip() and not (ev.impact or "").strip():
            flags.append("impact_empty")
            notes.append(f"joint_warn[{i}]:impact_empty")

        for cname in ev.company_name or []:
            c = (cname or "").strip()
            if not c:
                continue
            # substring match either way (简称)
            hit = any(c in e or e in c for e in company_entities) if company_entities else False
            if company_entities and not hit:
                flags.append(f"company_missing_from_entities:{c}")
                notes.append(f"joint_warn[{i}]:company_missing_from_entities:{c}")
            elif not company_entities:
                flags.append(f"company_missing_from_entities:{c}")
                notes.append(f"joint_warn[{i}]:company_missing_from_entities:{c}")

        for ref in ev.entity_refs or []:
            r = (ref or "").strip()
            if not r:
                continue
            if not any(r in e or e in r for e in entity_names):
                flags.append(f"entity_ref_unresolved:{r}")
                notes.append(f"joint_warn[{i}]:entity_ref_unresolved:{r}")

        # event_type vs entity presence (soft)
        if ev.event_type == "product_release":
            has_tech_or_co = any(e.type in ("technology", "company") for e in entities)
            if not has_tech_or_co:
                flags.append("event_type_entity_mismatch:product_release")
                notes.append(f"joint_warn[{i}]:event_type_entity_mismatch:product_release")
        if ev.event_type == "policy_publish":
            has_policy = any(e.type == "policy" for e in entities)
            if not has_policy:
                flags.append("event_type_entity_mismatch:policy_publish")
                notes.append(f"joint_warn[{i}]:event_type_entity_mismatch:policy_publish")

        # de-dupe flags preserving order
        seen: set[str] = set()
        uniq: list[str] = []
        for f in flags:
            if f not in seen:
                seen.add(f)
                uniq.append(f)
        ev.flags = uniq

    if notes:
        notes.insert(0, "joint_validation_ran")
    else:
        notes.append("joint_validation_ok")
    return notes

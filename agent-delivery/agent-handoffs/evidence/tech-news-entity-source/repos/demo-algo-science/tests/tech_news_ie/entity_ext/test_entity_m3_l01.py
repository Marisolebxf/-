from __future__ import annotations

import json

from innov.tech_news_ie.entity_ext.pipeline import _parse_llm_entity_payload, run_entity_pipeline
from innov.tech_news_ie.entity_ext.quality import (
    normalize_event_type,
    validate_impact_entity_joint,
)
from innov.tech_news_ie.entity_ext.schemas import (
    EntityExtractRequest,
    EntityMention,
    TechNewsEventExt,
)
from innov.tech_news_ie.schemas import CompletionTime


def test_normalize_event_type_aliases() -> None:
    et, flags = normalize_event_type("产品发布")
    assert et == "product_release"
    assert any(f.startswith("event_type_normalized_from:") for f in flags)

    et2, flags2 = normalize_event_type("breakthrough")
    assert et2 == "tech_breakthrough"
    assert flags2

    et3, flags3 = normalize_event_type("not-a-real-type-xyz")
    assert et3 == "other"
    assert any("event_type_unknown_mapped_other:" in f for f in flags3)


def test_normalize_event_type_empty_and_non_str() -> None:
    et, flags = normalize_event_type(None)
    assert et == "other"
    assert "event_type_defaulted_other" in flags

    et2, flags2 = normalize_event_type(123)
    assert et2 == "other"
    assert flags2  # unknown mapped or defaulted


def test_parse_llm_normalizes_bad_event_type() -> None:
    raw = json.dumps(
        {
            "entities": [{"type": "company", "name": "华为", "evidence": ["华为"]}],
            "events": [
                {
                    "company_name": ["华为"],
                    "completed_matter": "发布昇腾",
                    "impact": "提升算力供给",
                    "event_type": "weird_type_zzz",
                }
            ],
        },
        ensure_ascii=False,
    )
    events, _ = _parse_llm_entity_payload(raw, max_events=3)
    assert events[0].event_type == "other"
    assert any("event_type_unknown_mapped_other:" in f for f in events[0].flags)


def test_joint_impact_duplicates_matter() -> None:
    ev = TechNewsEventExt(
        company_name=["小米"],
        completion_time=CompletionTime(raw="2026"),
        completed_matter="小米发布玄戒芯片",
        impact="小米发布玄戒芯片",
        event_type="product_release",
    )
    ents = [
        EntityMention(type="company", name="小米", evidence=["小米"]),
        EntityMention(type="technology", name="玄戒", evidence=["玄戒"]),
    ]
    notes = validate_impact_entity_joint([ev], ents)
    assert "joint_validation_ran" in notes
    assert any("impact_duplicates_matter" in n for n in notes)
    assert "impact_duplicates_matter" in ev.flags


def test_joint_company_missing_from_entities() -> None:
    ev = TechNewsEventExt(
        company_name=["美团"],
        completed_matter="开源模型",
        impact="提升长上下文效率",
        event_type="product_release",
        entity_refs=["不存在的实体X"],
    )
    ents = [EntityMention(type="technology", name="LongCat", evidence=["LongCat"])]
    notes = validate_impact_entity_joint([ev], ents)
    assert any("company_missing_from_entities:美团" in n for n in notes)
    assert any("entity_ref_unresolved:" in n for n in notes)


def test_joint_impact_empty() -> None:
    ev = TechNewsEventExt(
        company_name=["华为"],
        completed_matter="发布产品",
        impact=None,
        event_type="product_release",
    )
    ents = [EntityMention(type="company", name="华为", evidence=["华为"])]
    notes = validate_impact_entity_joint([ev], ents)
    assert any("impact_empty" in n for n in notes)
    assert "impact_empty" in ev.flags


def test_pipeline_mock_runs_joint_validation() -> None:
    resp = run_entity_pipeline(
        EntityExtractRequest(
            title="测试",
            content="2026年7月，小米发布大模型，助力人工智能产业发展。",
            source="ut",
        )
    )
    joined = " ".join(resp.meta.notes)
    assert "joint_validation_ran" in joined or "joint_validation_ok" in joined
    assert "entity_ext_v0.3" in joined


def test_entity_rule_impact_pass_fills_when_cue_present() -> None:
    resp = run_entity_pipeline(
        EntityExtractRequest(
            title="测试影响",
            content="2026年7月，小米发布玄戒芯片，有助于人工智能产业发展与端侧算力提升。",
            source="ut",
            request_id="ut-impact-fill",
        )
    )
    assert "entity_rule_impact_pass" in resp.meta.notes or any(
        (ev.impact or "").strip() for ev in resp.events
    )
    # Prefer at least one non-empty impact when value cue exists in text
    assert any((ev.impact or "").strip() for ev in resp.events)

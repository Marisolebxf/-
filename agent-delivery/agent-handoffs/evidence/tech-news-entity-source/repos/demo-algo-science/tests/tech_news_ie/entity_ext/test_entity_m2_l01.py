from __future__ import annotations

import json

from innov.tech_news_ie.config import Settings
from innov.tech_news_ie.entity_ext.pipeline import (
    _as_completion_time,
    _parse_llm_entity_payload,
    run_entity_pipeline,
)
from innov.tech_news_ie.entity_ext.schemas import EntityExtractRequest
from innov.tech_news_ie.llm.base import OpenAICompatibleClient


def test_as_completion_time_slash_and_week() -> None:
    ct = _as_completion_time("2026/7/6")
    assert ct.normalized == "2026-07-06"
    assert ct.granularity == "day"

    ct2 = _as_completion_time(
        {"raw": "本周", "normalized": None, "granularity": "week"}
    )
    assert ct2.granularity == "week"

    ct3 = _as_completion_time({"raw": "x", "normalized": None, "granularity": "century"})
    assert ct3.granularity is None


def test_parse_llm_loose_shapes() -> None:
    raw = json.dumps(
        {
            "entities": [
                {
                    "type": "company",
                    "name": "美团",
                    "evidence": "美团开源",
                    "confidence": 0.8,
                }
            ],
            "events": [
                {
                    "company_name": "美团",
                    "completion_time": "2026/7/6",
                    "completed_matter": "开源 LongCat-2.0",
                    "impact": "提升长上下文效率",
                    "event_type": "product_release",
                    "news_source": "IT之家",
                    "entity_refs": "美团",
                    "evidence": ["美团将万亿参数大模型开源"],
                    "confidence": 0.8,
                }
            ],
        },
        ensure_ascii=False,
    )
    events, entities = _parse_llm_entity_payload(raw, max_events=3)
    assert len(entities) == 1
    assert entities[0].name == "美团"
    assert entities[0].evidence == ["美团开源"]
    assert len(events) == 1
    assert events[0].company_name == ["美团"]
    assert events[0].completion_time.normalized == "2026-07-06"
    assert events[0].event_type == "product_release"
    assert events[0].confidence.overall == 0.8


def test_llm_fallback_notes_not_silent(monkeypatch) -> None:
    def _boom(self, *, system: str, user: str):
        raise RuntimeError("boom-llm")

    monkeypatch.setattr(OpenAICompatibleClient, "generate", _boom)
    settings = Settings(mode="llm", llm_api_key="dummy", llm_base_url="http://example")
    resp = run_entity_pipeline(
        EntityExtractRequest(
            title="测试",
            content="2026年7月，小米发布大模型，助力人工智能产业。",
            source="ut",
        ),
        settings=settings,
    )
    assert resp.meta.mode == "mock"
    joined = " ".join(resp.meta.notes)
    assert "llm_entity_extract_failed_fallback_mock:" in joined
    assert "boom-llm" in joined
    assert resp.events  # mock still returns something


def test_gold_samples_at_least_ten() -> None:
    from pathlib import Path
    import json as _json

    path = (
        Path(__file__).resolve().parents[3]
        / "innov/tech_news_ie/entity_ext/samples/pdr_samples.json"
    )
    rows = _json.loads(path.read_text(encoding="utf-8"))
    assert len(rows) >= 10

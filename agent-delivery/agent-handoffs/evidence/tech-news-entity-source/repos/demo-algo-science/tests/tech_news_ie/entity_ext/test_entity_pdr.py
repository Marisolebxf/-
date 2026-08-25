from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from innov.tech_news_ie.api import create_app
from innov.tech_news_ie.entity_ext.pipeline import run_entity_pipeline
from innov.tech_news_ie.entity_ext.schemas import EntityExtractRequest

SAMPLES = (
    Path(__file__).resolve().parents[3]
    / "innov"
    / "tech_news_ie"
    / "entity_ext"
    / "samples"
    / "pdr_samples.json"
)

ENTITY_TYPES = {
    "company",
    "research_org",
    "policy",
    "industry",
    "technology",
    "expert",
    "patent",
}


def test_pdr_samples_cover_seven_entity_types() -> None:
    rows = json.loads(SAMPLES.read_text(encoding="utf-8"))
    assert len(rows) >= 10
    seen: set[str] = set()
    for row in rows:
        resp = run_entity_pipeline(
            EntityExtractRequest(
                title=row["title"],
                content=row["content"],
                source=row.get("source"),
                request_id=row["id"],
            )
        )
        assert resp.error is None, row["id"]
        assert resp.meta.schema_version == "entity-v0.1"
        assert resp.events, row["id"]
        types = {e.type for e in resp.entities}
        seen |= types
        for t in row["expect_types"]:
            if t in ENTITY_TYPES:
                assert t in types, f"{row['id']} missing entity type {t}, got {types}"
            elif t == "collaboration":
                assert any(ev.event_type == "collaboration" for ev in resp.events), row[
                    "id"
                ]

    assert ENTITY_TYPES.issubset(seen), f"missing types: {ENTITY_TYPES - seen}"


def test_entity_extract_http_mock() -> None:
    client = TestClient(create_app())
    r = client.post(
        "/internal/tech-news/entity-extract",
        json={
            "title": "小米大模型备案",
            "content": "2026年7月，小米自研大模型完成合规备案，助力人工智能产业。来源：快科技",
            "source": "快科技",
        },
        headers={"X-Request-Id": "entity-ut-1"},
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["request_id"] == "entity-ut-1"
    assert data["meta"]["schema_version"] == "entity-v0.1"
    assert data["entities"]
    assert data["events"]

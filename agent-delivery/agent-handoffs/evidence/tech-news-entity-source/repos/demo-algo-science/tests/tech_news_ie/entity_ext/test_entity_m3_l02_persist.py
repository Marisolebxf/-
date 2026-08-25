from __future__ import annotations

from innov.tech_news_ie.entity_ext.pipeline import run_entity_pipeline
from innov.tech_news_ie.entity_ext.schemas import EntityExtractRequest
from innov.tech_news_ie.persist import ExtractionStore


def test_entity_extract_persist_and_list(tmp_path) -> None:
    db = tmp_path / "t.db"
    store = ExtractionStore(db)
    req = EntityExtractRequest(
        title="UT",
        content="2026年7月，小米发布玄戒芯片，助力人工智能产业发展。",
        source="ut",
        request_id="ut-entity-m3-l02",
    )
    resp = run_entity_pipeline(req)
    assert resp.error is None
    store.save_entity_extract(req, resp)

    rows, _total = store.list_entity_extracts(limit=10, offset=0)
    assert any(r["id"] == "ut-entity-m3-l02" for r in rows)

    got = store.get_entity_extract("ut-entity-m3-l02")
    assert got is not None
    assert got["entity_count"] >= 1 or got["event_count"] >= 1
    assert "response" in got
    assert isinstance(got["entities"], list)
    assert isinstance(got["events"], list)
    if got["events"]:
        assert "event_type" in got["events"][0]

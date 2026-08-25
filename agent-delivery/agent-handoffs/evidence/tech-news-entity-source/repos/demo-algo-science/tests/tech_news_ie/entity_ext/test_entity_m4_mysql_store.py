from __future__ import annotations

import os

import pytest

from innov.tech_news_ie.entity_ext.pipeline import run_entity_pipeline
from innov.tech_news_ie.entity_ext.schemas import EntityExtractRequest
from innov.tech_news_ie.persist import ExtractionStore


def test_entity_store_sqlite_backend(tmp_path) -> None:
    db = tmp_path / "t.db"
    store = ExtractionStore(db, store="sqlite")
    req = EntityExtractRequest(
        title="UT-M4",
        content="2026年7月，小米发布玄戒芯片，助力人工智能产业发展。",
        source="ut",
        request_id="ut-entity-m4-sqlite",
    )
    resp = run_entity_pipeline(req)
    assert resp.error is None
    store.save_entity_extract(req, resp)
    rows, total = store.list_entity_extracts(limit=5, offset=0)
    assert total >= 1
    assert any(r["id"] == "ut-entity-m4-sqlite" for r in rows)
    got = store.get_entity_extract("ut-entity-m4-sqlite")
    assert got is not None
    assert "response" in got


def test_entity_store_mysql_optional() -> None:
    """Live MySQL smoke when TECH_NEWS_IE_MYSQL_SMOKE=1 and INNOV_MYSQL_* available."""
    if os.getenv("TECH_NEWS_IE_MYSQL_SMOKE", "").strip() not in {"1", "true", "yes"}:
        pytest.skip("set TECH_NEWS_IE_MYSQL_SMOKE=1 to run live MySQL ADS smoke")
    store = ExtractionStore("./data/_m4_mysql_smoke.sqlite", store="mysql")
    req = EntityExtractRequest(
        title="UT-M4-MYSQL",
        content="2026年7月，华为发布昇腾新品，推动智算产业发展。",
        source="ut-mysql",
        request_id="ut-entity-m4-mysql",
    )
    resp = run_entity_pipeline(req)
    assert resp.error is None
    store.save_entity_extract(req, resp)
    rows, _total = store.list_entity_extracts(limit=20, offset=0)
    assert any(r["id"] == "ut-entity-m4-mysql" for r in rows)
    got = store.get_entity_extract("ut-entity-m4-mysql")
    assert got is not None
    assert got["response"]["request_id"] == "ut-entity-m4-mysql"

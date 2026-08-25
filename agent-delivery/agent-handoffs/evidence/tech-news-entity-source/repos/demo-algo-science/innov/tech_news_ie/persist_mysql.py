"""MySQL ADS persist for tech-news entity-extract (E-TECH-NEWS-ENTITY-M4-L01)."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from innov.common import db as innov_db


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def _published_date(value: str | None) -> str | None:
    if not value:
        return None
    # accept YYYY-MM-DD or ISO datetime → date
    return value[:10]


def _dump(obj: Any) -> str:
    if obj is None:
        return "null"
    if hasattr(obj, "model_dump_json"):
        return obj.model_dump_json()
    if hasattr(obj, "model_dump"):
        return json.dumps(obj.model_dump(), ensure_ascii=False)
    return json.dumps(obj, ensure_ascii=False)


def save_entity_extract(request: Any, response: Any) -> str:
    """Upsert entity-extract header + replace child rows in gkxlumenx_ads."""
    payload = response.model_dump() if hasattr(response, "model_dump") else response
    request_id = getattr(response, "request_id", None) or payload.get("request_id")
    if not request_id:
        raise ValueError("entity extract response missing request_id")
    entities = list(getattr(response, "entities", None) or [])
    events = list(getattr(response, "events", None) or [])
    meta = getattr(response, "meta", None)
    now = _now()

    conn = innov_db.connect()
    try:
        conn.execute(
            """
            INSERT INTO ads_tech_news_entity_extract
            (request_id, title, source, published_at, model, mode, schema_version,
             entity_count, event_count, response_json, latency_ms, created_time, updated_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON DUPLICATE KEY UPDATE
              title=VALUES(title), source=VALUES(source), published_at=VALUES(published_at),
              model=VALUES(model), mode=VALUES(mode), schema_version=VALUES(schema_version),
              entity_count=VALUES(entity_count), event_count=VALUES(event_count),
              response_json=VALUES(response_json), latency_ms=VALUES(latency_ms),
              updated_time=VALUES(updated_time)
            """,
            (
                request_id,
                getattr(request, "title", None),
                getattr(request, "source", None),
                _published_date(getattr(request, "published_at", None)),
                getattr(response, "model", None),
                getattr(meta, "mode", None) if meta else None,
                getattr(meta, "schema_version", "entity-v0.1") if meta else "entity-v0.1",
                len(entities),
                len(events),
                json.dumps(payload, ensure_ascii=False),
                getattr(meta, "latency_ms", None) if meta else None,
                now,
                now,
            ),
        )
        conn.execute(
            "DELETE FROM ads_tech_news_entity WHERE request_id = ?",
            (request_id,),
        )
        conn.execute(
            "DELETE FROM ads_tech_news_entity_event WHERE request_id = ?",
            (request_id,),
        )
        for ord_, ent in enumerate(entities):
            conn.execute(
                """
                INSERT INTO ads_tech_news_entity
                (request_id, entity_ord, entity_type, name, normalized, evidence_json, confidence, created_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    request_id,
                    ord_,
                    getattr(ent, "type", None) or "technology",
                    getattr(ent, "name", "") or "",
                    getattr(ent, "normalized", None),
                    _dump(getattr(ent, "evidence", None) or []),
                    float(getattr(ent, "confidence", 0) or 0),
                    now,
                ),
            )
        for ord_, ev in enumerate(events):
            ct = getattr(ev, "completion_time", None)
            conn.execute(
                """
                INSERT INTO ads_tech_news_entity_event
                (request_id, event_ord, company_name, completion_time_raw,
                 completion_time_normalized, completion_time_granularity,
                 completed_matter, impact, event_type, news_source,
                 entity_refs_json, evidence_json, confidence_json, flags_json, created_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    request_id,
                    ord_,
                    _dump(getattr(ev, "company_name", None) or []),
                    getattr(ct, "raw", None) if ct else None,
                    getattr(ct, "normalized", None) if ct else None,
                    getattr(ct, "granularity", None) if ct else None,
                    getattr(ev, "completed_matter", None),
                    getattr(ev, "impact", None),
                    getattr(ev, "event_type", None) or "other",
                    getattr(ev, "news_source", None),
                    _dump(getattr(ev, "entity_refs", None) or []),
                    _dump(getattr(ev, "evidence", None) or {}),
                    _dump(getattr(ev, "confidence", None) or {}),
                    _dump(getattr(ev, "flags", None) or []),
                    now,
                ),
            )
        conn.commit()
    finally:
        conn.close()
    return str(request_id)


def list_entity_extracts(
    *, limit: int = 20, offset: int = 0, q: str | None = None
) -> tuple[list[dict], int]:
    conn = innov_db.connect()
    try:
        where = ""
        params: list = []
        if q and q.strip():
            where = "WHERE (title LIKE ? OR source LIKE ?)"
            like = f"%{q.strip()}%"
            params.extend([like, like])
        total_rows = conn.query(
            f"SELECT COUNT(1) AS c FROM ads_tech_news_entity_extract {where}",
            tuple(params),
        )
        total = int(total_rows[0]["c"]) if total_rows else 0
        rows = conn.query(
            f"""
            SELECT request_id AS id, created_time AS created_at, title, source, published_at,
                   model, mode, schema_version, entity_count, event_count
            FROM ads_tech_news_entity_extract
            {where}
            ORDER BY created_time DESC
            LIMIT ? OFFSET ?
            """,
            tuple(params + [limit, offset]),
        )
        return rows, total
    finally:
        conn.close()


def get_entity_extract(extraction_id: str) -> dict | None:
    conn = innov_db.connect()
    try:
        headers = conn.query(
            """
            SELECT request_id, created_time, title, source, published_at, model, mode,
                   schema_version, entity_count, event_count, response_json
            FROM ads_tech_news_entity_extract
            WHERE request_id = ?
            """,
            (extraction_id,),
        )
        if not headers:
            return None
        row = headers[0]
        entities = conn.query(
            """
            SELECT entity_ord, entity_type, name, normalized, evidence_json, confidence
            FROM ads_tech_news_entity
            WHERE request_id = ?
            ORDER BY entity_ord
            """,
            (extraction_id,),
        )
        events = conn.query(
            """
            SELECT event_ord, company_name, completion_time_raw, completion_time_normalized,
                   completion_time_granularity, completed_matter, impact, event_type,
                   news_source, entity_refs_json, evidence_json, confidence_json, flags_json
            FROM ads_tech_news_entity_event
            WHERE request_id = ?
            ORDER BY event_ord
            """,
            (extraction_id,),
        )
        raw_json = row.get("response_json")
        if isinstance(raw_json, (dict, list)):
            payload = raw_json
        else:
            payload = json.loads(raw_json or "{}")
        return {
            "id": row["request_id"],
            "created_at": row["created_time"],
            "title": row["title"],
            "source": row["source"],
            "published_at": row["published_at"],
            "model": row["model"],
            "mode": row["mode"],
            "schema_version": row["schema_version"],
            "entity_count": row["entity_count"],
            "event_count": row["event_count"],
            "entities": entities,
            "events": events,
            "response": payload,
        }
    finally:
        conn.close()

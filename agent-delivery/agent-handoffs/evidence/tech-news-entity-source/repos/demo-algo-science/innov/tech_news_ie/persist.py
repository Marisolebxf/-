from __future__ import annotations

import json
import sqlite3
import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .schemas import ExtractRequest, ExtractResponse, TechNewsEvent


_LOCK = threading.Lock()


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class StoredExtraction:
    id: str
    created_at: str
    title: str | None
    source: str | None
    published_at: str | None
    content: str
    response: ExtractResponse


class ExtractionStore:
    """ADS stand-in: SQLite by default; optional MySQL via TECH_NEWS_IE_STORE."""

    def __init__(self, db_path: str | Path, store: str = "sqlite") -> None:
        self.db_path = Path(db_path)
        self.store = store if store in {"sqlite", "mysql", "dual"} else "sqlite"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        if self.store in {"sqlite", "dual"}:
            self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with _LOCK:
            with self._connect() as conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS ads_tech_news_extraction (
                        id TEXT PRIMARY KEY,
                        created_at TEXT NOT NULL,
                        title TEXT,
                        source TEXT,
                        published_at TEXT,
                        content TEXT NOT NULL,
                        model TEXT,
                        event_count INTEGER NOT NULL DEFAULT 0,
                        response_json TEXT NOT NULL
                    )
                    """
                )
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS ads_tech_news_event (
                        extraction_id TEXT NOT NULL,
                        event_index INTEGER NOT NULL,
                        company_name TEXT,
                        completion_time_raw TEXT,
                        completion_time_normalized TEXT,
                        completed_matter TEXT,
                        impact TEXT,
                        flags TEXT,
                        evidence_json TEXT,
                        PRIMARY KEY (extraction_id, event_index),
                        FOREIGN KEY (extraction_id)
                            REFERENCES ads_tech_news_extraction(id)
                    )
                    """
                )
                conn.commit()

    def save(self, request: ExtractRequest, response: ExtractResponse) -> str:
        extraction_id = response.request_id
        with _LOCK:
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO ads_tech_news_extraction
                    (id, created_at, title, source, published_at, content, model, event_count, response_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        extraction_id,
                        _utc_now(),
                        request.title,
                        request.source,
                        request.published_at,
                        request.content,
                        response.model,
                        len(response.events),
                        response.model_dump_json(),
                    ),
                )
                conn.execute(
                    "DELETE FROM ads_tech_news_event WHERE extraction_id = ?",
                    (extraction_id,),
                )
                for idx, ev in enumerate(response.events):
                    conn.execute(
                        """
                        INSERT INTO ads_tech_news_event
                        (extraction_id, event_index, company_name, completion_time_raw,
                         completion_time_normalized, completed_matter, impact, flags, evidence_json)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            extraction_id,
                            idx,
                            json.dumps(ev.company_name, ensure_ascii=False),
                            ev.completion_time.raw,
                            ev.completion_time.normalized,
                            ev.completed_matter,
                            ev.impact,
                            json.dumps(ev.flags, ensure_ascii=False),
                            ev.evidence.model_dump_json(),
                        ),
                    )
                conn.commit()
        return extraction_id

    def _ensure_entity_tables(self, conn: sqlite3.Connection) -> None:
        """Wave0 SQLite mirror of scripts/sql/ads_tech_news_entity.sql (logical columns)."""
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ads_tech_news_entity_extract (
                id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                title TEXT,
                source TEXT,
                published_at TEXT,
                model TEXT,
                mode TEXT,
                schema_version TEXT,
                entity_count INTEGER NOT NULL DEFAULT 0,
                event_count INTEGER NOT NULL DEFAULT 0,
                response_json TEXT NOT NULL,
                latency_ms INTEGER
            )
            """
        )
        # migrate older Wave0 header table (M2 only had fewer columns)
        cols = {
            r[1]
            for r in conn.execute("PRAGMA table_info(ads_tech_news_entity_extract)").fetchall()
        }
        for col, decl in (
            ("published_at", "TEXT"),
            ("mode", "TEXT"),
            ("schema_version", "TEXT"),
            ("latency_ms", "INTEGER"),
        ):
            if col not in cols:
                conn.execute(
                    f"ALTER TABLE ads_tech_news_entity_extract ADD COLUMN {col} {decl}"
                )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ads_tech_news_entity (
                extraction_id TEXT NOT NULL,
                entity_ord INTEGER NOT NULL,
                entity_type TEXT NOT NULL,
                name TEXT NOT NULL,
                normalized TEXT,
                evidence_json TEXT,
                confidence REAL,
                PRIMARY KEY (extraction_id, entity_ord),
                FOREIGN KEY (extraction_id)
                    REFERENCES ads_tech_news_entity_extract(id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ads_tech_news_entity_event (
                extraction_id TEXT NOT NULL,
                event_ord INTEGER NOT NULL,
                company_name TEXT,
                completion_time_raw TEXT,
                completion_time_normalized TEXT,
                completion_time_granularity TEXT,
                completed_matter TEXT,
                impact TEXT,
                event_type TEXT NOT NULL DEFAULT 'other',
                news_source TEXT,
                entity_refs_json TEXT,
                evidence_json TEXT,
                confidence_json TEXT,
                flags_json TEXT,
                PRIMARY KEY (extraction_id, event_ord),
                FOREIGN KEY (extraction_id)
                    REFERENCES ads_tech_news_entity_extract(id)
            )
            """
        )

    def save_entity_extract(self, request: ExtractRequest, response: object) -> str:
        """Persist entity-extract JSON + normalized entity/event rows (SQLite and/or MySQL ADS)."""
        payload = response.model_dump() if hasattr(response, "model_dump") else response
        extraction_id = getattr(response, "request_id", None) or payload.get("request_id")
        entities = list(getattr(response, "entities", None) or [])
        events = list(getattr(response, "events", None) or [])
        meta = getattr(response, "meta", None)

        if self.store in {"sqlite", "dual"}:
            with _LOCK:
                with self._connect() as conn:
                    self._ensure_entity_tables(conn)
                    conn.execute(
                        """
                        INSERT OR REPLACE INTO ads_tech_news_entity_extract
                        (id, created_at, title, source, published_at, model, mode, schema_version,
                         entity_count, event_count, response_json, latency_ms)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            extraction_id,
                            _utc_now(),
                            request.title,
                            request.source,
                            request.published_at,
                            getattr(response, "model", None),
                            getattr(meta, "mode", None) if meta else None,
                            getattr(meta, "schema_version", "entity-v0.1") if meta else "entity-v0.1",
                            len(entities),
                            len(events),
                            json.dumps(payload, ensure_ascii=False),
                            getattr(meta, "latency_ms", None) if meta else None,
                        ),
                    )
                    conn.execute(
                        "DELETE FROM ads_tech_news_entity WHERE extraction_id = ?",
                        (extraction_id,),
                    )
                    conn.execute(
                        "DELETE FROM ads_tech_news_entity_event WHERE extraction_id = ?",
                        (extraction_id,),
                    )
                    for ord_, ent in enumerate(entities):
                        evidence = getattr(ent, "evidence", None)
                        if hasattr(evidence, "model_dump"):
                            evidence_json = json.dumps(evidence.model_dump(), ensure_ascii=False)
                        else:
                            evidence_json = json.dumps(evidence or [], ensure_ascii=False)
                        conn.execute(
                            """
                            INSERT INTO ads_tech_news_entity
                            (extraction_id, entity_ord, entity_type, name, normalized, evidence_json, confidence)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            """,
                            (
                                extraction_id,
                                ord_,
                                getattr(ent, "type", None) or "technology",
                                getattr(ent, "name", "") or "",
                                getattr(ent, "normalized", None),
                                evidence_json,
                                float(getattr(ent, "confidence", 0) or 0),
                            ),
                        )
                    for ord_, ev in enumerate(events):
                        ct = getattr(ev, "completion_time", None)
                        evidence = getattr(ev, "evidence", None)
                        confidence = getattr(ev, "confidence", None)
                        conn.execute(
                            """
                            INSERT INTO ads_tech_news_entity_event
                            (extraction_id, event_ord, company_name, completion_time_raw,
                             completion_time_normalized, completion_time_granularity,
                             completed_matter, impact, event_type, news_source,
                             entity_refs_json, evidence_json, confidence_json, flags_json)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """,
                            (
                                extraction_id,
                                ord_,
                                json.dumps(getattr(ev, "company_name", None) or [], ensure_ascii=False),
                                getattr(ct, "raw", None) if ct else None,
                                getattr(ct, "normalized", None) if ct else None,
                                getattr(ct, "granularity", None) if ct else None,
                                getattr(ev, "completed_matter", None),
                                getattr(ev, "impact", None),
                                getattr(ev, "event_type", None) or "other",
                                getattr(ev, "news_source", None),
                                json.dumps(getattr(ev, "entity_refs", None) or [], ensure_ascii=False),
                                evidence.model_dump_json() if hasattr(evidence, "model_dump_json") else json.dumps(evidence or {}, ensure_ascii=False),
                                confidence.model_dump_json() if hasattr(confidence, "model_dump_json") else json.dumps(confidence or {}, ensure_ascii=False),
                                json.dumps(getattr(ev, "flags", None) or [], ensure_ascii=False),
                            ),
                        )
                    conn.commit()

        if self.store in {"mysql", "dual"}:
            from . import persist_mysql

            persist_mysql.save_entity_extract(request, response)

        return str(extraction_id)

    def list_entity_extracts(
        self, *, limit: int = 20, offset: int = 0, q: str | None = None
    ) -> tuple[list[dict], int]:
        if self.store == "mysql":
            from . import persist_mysql

            return persist_mysql.list_entity_extracts(limit=limit, offset=offset, q=q)
        if self.store == "dual":
            from . import persist_mysql

            try:
                return persist_mysql.list_entity_extracts(limit=limit, offset=offset, q=q)
            except Exception:
                pass
        where = ""
        params: list = []
        if q and q.strip():
            where = "WHERE (IFNULL(title,'') LIKE ? OR IFNULL(source,'') LIKE ?)"
            like = f"%{q.strip()}%"
            params.extend([like, like])
        with _LOCK:
            with self._connect() as conn:
                self._ensure_entity_tables(conn)
                # SQLite: IFNULL ok
                total = conn.execute(
                    f"SELECT COUNT(1) AS c FROM ads_tech_news_entity_extract {where}",
                    tuple(params),
                ).fetchone()["c"]
                rows = conn.execute(
                    f"""
                    SELECT id, created_at, title, source, published_at, model, mode,
                           schema_version, entity_count, event_count
                    FROM ads_tech_news_entity_extract
                    {where}
                    ORDER BY created_at DESC
                    LIMIT ? OFFSET ?
                    """,
                    tuple(params + [limit, offset]),
                ).fetchall()
        return [dict(r) for r in rows], int(total)

    def get_entity_extract(self, extraction_id: str) -> dict | None:
        if self.store == "mysql":
            from . import persist_mysql

            return persist_mysql.get_entity_extract(extraction_id)
        if self.store == "dual":
            from . import persist_mysql

            try:
                got = persist_mysql.get_entity_extract(extraction_id)
                if got is not None:
                    return got
            except Exception:
                pass
        with _LOCK:
            with self._connect() as conn:
                self._ensure_entity_tables(conn)
                row = conn.execute(
                    "SELECT * FROM ads_tech_news_entity_extract WHERE id = ?",
                    (extraction_id,),
                ).fetchone()
                if row is None:
                    return None
                entities = conn.execute(
                    """
                    SELECT entity_ord, entity_type, name, normalized, evidence_json, confidence
                    FROM ads_tech_news_entity
                    WHERE extraction_id = ?
                    ORDER BY entity_ord
                    """,
                    (extraction_id,),
                ).fetchall()
                events = conn.execute(
                    """
                    SELECT event_ord, company_name, completion_time_raw, completion_time_normalized,
                           completion_time_granularity, completed_matter, impact, event_type,
                           news_source, entity_refs_json, evidence_json, confidence_json, flags_json
                    FROM ads_tech_news_entity_event
                    WHERE extraction_id = ?
                    ORDER BY event_ord
                    """,
                    (extraction_id,),
                ).fetchall()
        payload = json.loads(row["response_json"])
        return {
            "id": row["id"],
            "created_at": row["created_at"],
            "title": row["title"],
            "source": row["source"],
            "published_at": row["published_at"],
            "model": row["model"],
            "mode": row["mode"],
            "schema_version": row["schema_version"],
            "entity_count": row["entity_count"],
            "event_count": row["event_count"],
            "entities": [dict(e) for e in entities],
            "events": [dict(e) for e in events],
            "response": payload,
        }

    def get(self, extraction_id: str) -> StoredExtraction | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM ads_tech_news_extraction WHERE id = ?",
                (extraction_id,),
            ).fetchone()
        if row is None:
            return None
        return StoredExtraction(
            id=row["id"],
            created_at=row["created_at"],
            title=row["title"],
            source=row["source"],
            published_at=row["published_at"],
            content=row["content"],
            response=ExtractResponse.model_validate_json(row["response_json"]),
        )

    def list(self, *, limit: int = 20, offset: int = 0) -> list[dict]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, created_at, title, source, published_at, model, event_count
                FROM ads_tech_news_extraction
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
                """,
                (limit, offset),
            ).fetchall()
        return [dict(r) for r in rows]

    def list_events(self, extraction_id: str) -> list[TechNewsEvent]:
        stored = self.get(extraction_id)
        if stored is None:
            return []
        return stored.response.events

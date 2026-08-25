from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from fastapi import APIRouter, FastAPI, Header, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse

from .config import Settings, get_settings
from .persist import ExtractionStore
from .pipeline import run_pipeline
from .entity_ext.pipeline import run_entity_pipeline
from .entity_ext.schemas import EntityExtractRequest, EntityExtractResponse
from .schemas import (
    ExtractionListItem,
    ExtractionListResponse,
    ExtractRequest,
    ExtractResponse,
    StoredExtractionResponse,
)

router = APIRouter(tags=["tech-news-ie"])

_STATIC = Path(__file__).resolve().parent / "static"


@lru_cache
def _store_for(db_path: str, store: str) -> ExtractionStore:
    return ExtractionStore(db_path, store=store)


def get_store(settings: Settings | None = None) -> ExtractionStore:
    cfg = settings or get_settings()
    return _store_for(cfg.db_path, cfg.store)


@router.get("/tech-news/healthz")
def tech_news_healthz() -> dict:
    cfg = get_settings()
    return {
        "status": "ok",
        "mode": cfg.mode,
        "persist": cfg.persist_by_default,
        "store": cfg.store,
    }


@router.get("/tech-news")
def tech_news_root() -> RedirectResponse:
    return RedirectResponse(url="/tech-news/review")


@router.get("/tech-news/review")
def review_page() -> FileResponse:
    page = _STATIC / "review.html"
    if not page.exists():
        raise HTTPException(status_code=404, detail="review page missing")
    return FileResponse(page)


@router.post("/internal/tech-news/extract", response_model=ExtractResponse)
def extract(
    body: ExtractRequest,
    persist: bool | None = Query(
        default=None,
        description="Whether to save into sandbox ADS SQLite; default from settings",
    ),
    x_request_id: str | None = Header(default=None, alias="X-Request-Id"),
) -> ExtractResponse | JSONResponse:
    cfg = get_settings()
    if x_request_id and not body.request_id:
        body.request_id = x_request_id
    result = run_pipeline(body, settings=cfg)
    if result.error is not None:
        code = result.error.code
        if code == "empty_content":
            status = 422
        elif code.startswith("gated_") or code in {
            "opinion_or_commentary",
            "policy_or_legal_noise",
            "consumer_retail_noise",
        }:
            # Soft reject: return body so clients can show gate reason without failing hard
            status = 200
        else:
            status = 500
        if status == 200:
            return result
        return JSONResponse(status_code=status, content=result.model_dump())

    should_persist = cfg.persist_by_default if persist is None else persist
    if should_persist:
        get_store(cfg).save(body, result)
        result.meta.persisted = True
    else:
        result.meta.persisted = False
    return result


@router.post(
    "/internal/tech-news/entity-extract",
    response_model=EntityExtractResponse,
)
def entity_extract(
    body: EntityExtractRequest,
    persist: bool | None = Query(
        default=None,
        description="Whether to save entity extract JSON into sandbox SQLite",
    ),
    x_request_id: str | None = Header(default=None, alias="X-Request-Id"),
) -> EntityExtractResponse | JSONResponse:
    """PDR extension: 7-class entities + event_type/source (mock/llm)."""
    cfg = get_settings()
    if x_request_id and not body.request_id:
        body.request_id = x_request_id
    result = run_entity_pipeline(body, settings=cfg)
    if result.error is not None:
        status = 422 if result.error.get("code") == "empty_content" else 500
        return JSONResponse(status_code=status, content=result.model_dump())
    should_persist = cfg.persist_by_default if persist is None else persist
    if should_persist:
        get_store(cfg).save_entity_extract(body, result)
        # keep response meta notes
        result.meta.notes = list(result.meta.notes) + ["persisted_entity_extract"]
    return result


@router.get("/internal/tech-news/entity-extractions")
def list_entity_extractions(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    q: str | None = Query(default=None, description="title/source keyword"),
) -> dict:
    """List persisted entity-extract headers (ADS Wave0 / M3-L02 / M4)."""
    rows, total = get_store().list_entity_extracts(limit=limit, offset=offset, q=q)
    return {"items": rows, "limit": limit, "offset": offset, "total": total, "q": q}


@router.get("/internal/tech-news/entity-extractions/{extraction_id}")
def get_entity_extraction(extraction_id: str) -> dict:
    """Get one persisted entity-extract (entities + events + full response)."""
    stored = get_store().get_entity_extract(extraction_id)
    if stored is None:
        raise HTTPException(status_code=404, detail="entity extraction not found")
    return stored


@router.get("/internal/tech-news/extractions/{extraction_id}/events")
def get_extraction_events(extraction_id: str) -> dict:
    """Flat event rows for review UI (flags / impact emphasis)."""
    stored = get_store().get(extraction_id)
    if stored is None:
        raise HTTPException(status_code=404, detail="extraction not found")
    events = []
    for idx, ev in enumerate(stored.response.events):
        events.append(
            {
                "index": idx,
                "company_name": ev.company_name,
                "completion_time": ev.completion_time.model_dump(),
                "completed_matter": ev.completed_matter,
                "impact": ev.impact,
                "flags": ev.flags,
                "confidence": ev.confidence.model_dump(),
                "evidence": ev.evidence.model_dump(),
            }
        )
    return {
        "id": stored.id,
        "title": stored.title,
        "flags_summary": sorted(
            {f for ev in stored.response.events for f in ev.flags}
        ),
        "events": events,
    }


@router.get("/internal/tech-news/extractions", response_model=ExtractionListResponse)
def list_extractions(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> ExtractionListResponse:
    rows = get_store().list(limit=limit, offset=offset)
    return ExtractionListResponse(
        items=[ExtractionListItem.model_validate(r) for r in rows]
    )


@router.get(
    "/internal/tech-news/extractions/{extraction_id}",
    response_model=StoredExtractionResponse,
)
def get_extraction(extraction_id: str) -> StoredExtractionResponse:
    stored = get_store().get(extraction_id)
    if stored is None:
        raise HTTPException(status_code=404, detail="extraction not found")
    return StoredExtractionResponse(
        id=stored.id,
        created_at=stored.created_at,
        title=stored.title,
        source=stored.source,
        published_at=stored.published_at,
        content=stored.content,
        response=stored.response,
    )


def create_app() -> FastAPI:
    """Standalone app for local sandbox / isolated tests."""
    app = FastAPI(
        title="tech-news-ie",
        version="0.4.0",
        description="Tech news four-field extraction (migrated into demo-algo-science)",
    )
    app.include_router(router)
    return app


# Back-compat for `uvicorn innov.tech_news_ie.api:app`
app = create_app()

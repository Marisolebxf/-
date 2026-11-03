"""CHAIN internal routes. SHARED health + SEARCH catalog + SYNC reads + Job execute."""
from __future__ import annotations

import json

from fastapi import APIRouter, Body, HTTPException, Query
from fastapi.responses import JSONResponse

from lumen_common.algorithms.chain import (
    JobAlreadyRunningError,
    JobExecuteRejected,
    NonDemoMysqlTargetError,
    NonDemoNebulaSpaceError,
    assert_demo_mysql_targets,
    current_trace_id,
    execute_chain_job,
    project_graph,
    search_chain,
    sync_kpi,
    sync_news,
    sync_objects,
    sync_snapshot,
)
from lumen_common.algorithms.chain.workspace_meta import chain_meta
from lumen_common.algorithms.chain.ner_hotspot import extract_and_persist, list_hotspots
from lumen_common.algorithms.chain.report_export import (
    ObjectStoreError,
    ReportExportRejected,
    export_chain_report,
)

router = APIRouter(prefix="/internal/v1/chain", tags=["chain"])


@router.get("/meta")
def chain_meta_get():
    """CHAIN-N1–N4 字典。标杆 Q016 空；高筛 layout/coveredStage 仅展示不可搜。"""
    return chain_meta()


@router.post("/meta")
def chain_meta_post(body: dict | None = Body(default=None)):
    _ = body
    return chain_meta()


@router.get("/health")
def chain_health():
    names = assert_demo_mysql_targets()
    return {
        "status": "ok",
        "module": "chain",
        "targets": names,
        "readonly": True,
        "trace_id": current_trace_id(),
    }


def _search_response(payload: dict | None):
    try:
        return search_chain(payload)
    except NonDemoMysqlTargetError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=422, detail="conditions must be JSON") from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/search")
def chain_search_get(
    mode: str = Query("smart"),
    keyword: str = Query(""),
    smartKeywords: list[str] | None = Query(default=None),
    logic: str = Query("all"),
    conditions: str | None = Query(default=None),
):
    payload = {
        "mode": mode,
        "keyword": keyword,
        "logic": logic,
        "conditions": conditions or [],
    }
    if smartKeywords:
        payload["smartKeywords"] = smartKeywords
    return _search_response(payload)


@router.post("/search")
def chain_search_post(body: dict | None = Body(default=None)):
    return _search_response(body or {})


def _sync_response(fn, payload: dict | None):
    try:
        return fn(payload)
    except NonDemoMysqlTargetError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/sync/kpi")
def chain_sync_kpi(
    objectId: str = Query(""),
    object_id: str = Query(""),
    chainId: str = Query(""),
    chain_id: str = Query(""),
    industryId: str = Query(""),
    industry_id: str = Query(""),
):
    return _sync_response(
        sync_kpi,
        {
            "objectId": objectId or object_id,
            "chainId": chainId or chain_id,
            "industryId": industryId or industry_id,
        },
    )


@router.get("/sync/snapshot")
def chain_sync_snapshot(
    chainId: str = Query(""),
    chain_id: str = Query(""),
    industryId: str = Query(""),
    industry_id: str = Query(""),
    objectId: str = Query(""),
    object_id: str = Query(""),
    asOf: str = Query(""),
    as_of: str = Query(""),
):
    return _sync_response(
        sync_snapshot,
        {
            "chainId": chainId or chain_id or objectId or object_id,
            "industryId": industryId or industry_id,
            "asOf": asOf or as_of,
        },
    )


@router.get("/sync/objects")
def chain_sync_objects(
    industryId: str = Query(""),
    industry_id: str = Query(""),
):
    return _sync_response(sync_objects, {"industryId": industryId or industry_id})


@router.get("/sync/news")
def chain_sync_news(
    objectId: str = Query(""),
    object_id: str = Query(""),
    chainId: str = Query(""),
    chain_id: str = Query(""),
    industryId: str = Query(""),
    industry_id: str = Query(""),
):
    return _sync_response(
        sync_news,
        {
            "objectId": objectId or object_id or chainId or chain_id,
            "industryId": industryId or industry_id,
        },
    )


@router.post("/graph/project")
def chain_graph_project(body: dict | None = Body(default=None)):
    """Explicit DWD → demo_gkx_chain write. Not invoked by search/sync/jobs."""
    try:
        return project_graph(body or {})
    except NonDemoMysqlTargetError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except NonDemoNebulaSpaceError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/jobs/execute")
def chain_jobs_execute(body: dict | None = Body(default=None)):
    """Java → Python Execute. 202 after one Graph run; result only via Complete callback."""
    try:
        payload = execute_chain_job(body or {})
    except NonDemoMysqlTargetError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except JobAlreadyRunningError as exc:
        return JSONResponse(status_code=409, content=exc.to_body(current_trace_id()))
    except JobExecuteRejected as exc:
        return JSONResponse(status_code=400, content=exc.to_body(current_trace_id()))
    return JSONResponse(status_code=202, content=payload)


@router.post("/ner/extract")
def chain_ner_extract(body: dict | None = Body(default=None)):
    """Small-batch Demo NER/RE. Writes DWD extraction_result. Not a search engine."""
    try:
        return extract_and_persist(body or {})
    except NonDemoMysqlTargetError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/hotspot")
def chain_hotspot(
    chainId: str = Query(""),
    chain_id: str = Query(""),
    limit: int = Query(20),
):
    """Read-only news_event hotspot list. Failures return an empty list, never 500."""
    try:
        return list_hotspots({"chainId": chainId or chain_id, "limit": limit})
    except Exception:  # noqa: BLE001
        return {
            "items": [],
            "honesty": {"empty": True, "error": True, "not_search_engine": True},
            "trace_id": current_trace_id(),
        }


@router.post("/reports/export")
def chain_reports_export(body: dict | None = Body(default=None)):
    """Read-only Result → object bytes. Does not Execute 七键/全景 Graph."""
    try:
        return export_chain_report(body or {})
    except NonDemoMysqlTargetError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except ReportExportRejected as exc:
        status = 502 if isinstance(exc, ObjectStoreError) else 400
        return JSONResponse(status_code=status, content=exc.to_body(current_trace_id()))

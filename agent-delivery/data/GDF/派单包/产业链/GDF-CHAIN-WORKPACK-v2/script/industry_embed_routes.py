"""产业锚点向量索引路由（CROSS-VEC-PY-INDEX-L01）。

Java 只 Feign 这两条；`jobs/enrich` 跑批是 CROSS-VEC-JOB-A-L01 的叶，不在本文件。
"""
from __future__ import annotations

from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from lumen_common.algorithms.industry_embed import (
    CollectionGuardError,
    rebuild,
    search,
)

router = APIRouter(prefix="/internal/industry/embed", tags=["industry-embed"])


def _envelope(body: dict) -> JSONResponse:
    """code≠0（引擎不可用 / 词表空）一律非 200，禁止用 200 + 空 items 冒充成功。"""
    return JSONResponse(status_code=200 if body.get("code") == 0 else 503, content=body)


@router.post("/rebuild")
def industry_embed_rebuild(body: dict | None = Body(default=None)):
    """产业链灌数末段整库一次重建。政策/企业重灌禁止调用本接口。"""
    try:
        return _envelope(rebuild(body or {}))
    except CollectionGuardError as exc:
        return JSONResponse(status_code=422, content={"code": 1, "msg": str(exc), "data": None})


@router.post("/search")
def industry_embed_search(body: dict | None = Body(default=None)):
    """单条 top-k 候选。score 只是相似度，**不得**当 industry_link_code 落库。"""
    try:
        return _envelope(search(body or {}))
    except CollectionGuardError as exc:
        return JSONResponse(status_code=422, content={"code": 1, "msg": str(exc), "data": None})

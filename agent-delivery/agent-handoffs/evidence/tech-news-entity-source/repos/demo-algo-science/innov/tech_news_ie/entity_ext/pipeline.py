from __future__ import annotations

import logging
import re
import time
import uuid
from pathlib import Path

from ..config import Settings, get_settings
from ..impact_pass import llm_impact_pass, mock_impact_pass
from ..json_utils import loads_llm_json
from ..llm.base import OpenAICompatibleClient
from ..normalize import normalize_document
from ..schemas import CompletionTime, Confidence, Evidence
from .._time_resolve import enrich_completion_time, normalize_time_fields
from .mock import mock_entity_extract
from .quality import normalize_event_type, validate_impact_entity_joint
from .schemas import (
    EntityExtractMeta,
    EntityExtractRequest,
    EntityExtractResponse,
    EntityMention,
    TechNewsEventExt,
)

logger = logging.getLogger(__name__)
_PROMPT = Path(__file__).resolve().parent.parent / "prompts" / "entity_extract_v0.1.txt"

_SLASH_DAY_RE = re.compile(r"^(20\d{2})[./](\d{1,2})[./](\d{1,2})$")
_SLASH_MONTH_RE = re.compile(r"^(20\d{2})[./](\d{1,2})$")


def _as_str_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        s = value.strip()
        return [s] if s else []
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            if item is None:
                continue
            s = str(item).strip()
            if s:
                out.append(s)
        return out
    return [str(value).strip()] if str(value).strip() else []


def _as_completion_time(value) -> CompletionTime:
    if value is None:
        return CompletionTime()
    if isinstance(value, str):
        raw = value.strip()
        if not raw:
            return CompletionTime()
        # 2026/7/6 or 2026.7.6
        m = _SLASH_DAY_RE.match(raw.replace(" ", ""))
        if m:
            return CompletionTime(
                raw=raw,
                normalized=f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}",
                granularity="day",
            )
        m = _SLASH_MONTH_RE.match(raw.replace(" ", ""))
        if m:
            return CompletionTime(
                raw=raw,
                normalized=f"{m.group(1)}-{int(m.group(2)):02d}",
                granularity="month",
            )
        norm, gran = normalize_time_fields(raw)
        if gran not in (None, "year", "month", "week", "day", "range"):
            gran = None
        return CompletionTime(raw=raw, normalized=norm, granularity=gran)  # type: ignore[arg-type]
    if isinstance(value, dict):
        gran = value.get("granularity")
        if gran not in (None, "year", "month", "week", "day", "range"):
            gran = None
        ct = CompletionTime(
            raw=value.get("raw"),
            normalized=value.get("normalized"),
            granularity=gran,
        )
        if ct.raw and not ct.normalized:
            norm, g2 = normalize_time_fields(ct.raw)
            if norm:
                ct.normalized = norm
                if ct.granularity is None and g2 in (
                    "year",
                    "month",
                    "week",
                    "day",
                    "range",
                ):
                    ct.granularity = g2  # type: ignore[assignment]
        return ct
    return CompletionTime(raw=str(value), normalized=None, granularity=None)


def _as_evidence(value) -> Evidence:
    if isinstance(value, dict):
        return Evidence(
            company=_as_str_list(value.get("company")),
            time=_as_str_list(value.get("time")),
            matter=_as_str_list(value.get("matter")),
            impact=_as_str_list(value.get("impact")),
        )
    # LLM sometimes returns flat string spans
    spans = _as_str_list(value)
    return Evidence(matter=spans)


def _as_confidence(value) -> Confidence:
    if isinstance(value, dict):
        return Confidence(
            company_name=float(value.get("company_name") or 0),
            completion_time=float(value.get("completion_time") or 0),
            completed_matter=float(value.get("completed_matter") or 0),
            impact=float(value.get("impact") or 0),
            overall=float(value.get("overall") or 0),
        )
    try:
        score = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        score = 0.0
    score = max(0.0, min(1.0, score))
    return Confidence(
        company_name=score,
        completion_time=score,
        completed_matter=score,
        impact=score,
        overall=score,
    )


def _parse_llm_entity_payload(raw: str, max_events: int) -> tuple[list[TechNewsEventExt], list[EntityMention]]:
    data = loads_llm_json(raw)
    if not isinstance(data, dict):
        raise ValueError("entity LLM JSON must be object")

    entities: list[EntityMention] = []
    for item in data.get("entities") or []:
        if not isinstance(item, dict) or not item.get("name"):
            continue
        try:
            entities.append(
                EntityMention(
                    type=item.get("type") or "technology",  # type: ignore[arg-type]
                    name=str(item["name"]).strip(),
                    normalized=item.get("normalized"),
                    evidence=_as_str_list(item.get("evidence")),
                    confidence=float(item.get("confidence") or 0.5),
                )
            )
        except Exception:
            continue

    events: list[TechNewsEventExt] = []
    for item in (data.get("events") or [])[:max_events]:
        if not isinstance(item, dict):
            continue
        etype, et_flags = normalize_event_type(item.get("event_type"))
        try:
            events.append(
                TechNewsEventExt(
                    company_name=_as_str_list(item.get("company_name")),
                    completion_time=_as_completion_time(item.get("completion_time")),
                    completed_matter=item.get("completed_matter"),
                    impact=item.get("impact"),
                    event_type=etype,
                    news_source=item.get("news_source"),
                    entity_refs=_as_str_list(item.get("entity_refs")),
                    evidence=_as_evidence(item.get("evidence")),
                    confidence=_as_confidence(item.get("confidence")),
                    flags=_as_str_list(item.get("flags")) + et_flags,
                )
            )
        except Exception:
            continue
    if not events and not entities:
        raise ValueError("empty entity LLM payload")
    return events, entities


def _merge_entities(
    primary: list[EntityMention], secondary: list[EntityMention]
) -> list[EntityMention]:
    seen: set[tuple[str, str]] = set()
    out: list[EntityMention] = []
    for e in primary + secondary:
        key = (e.type, e.name)
        if key in seen:
            continue
        seen.add(key)
        out.append(e)
    return out


def run_entity_pipeline(
    req: EntityExtractRequest, settings: Settings | None = None
) -> EntityExtractResponse:
    cfg = settings or get_settings()
    t0 = time.perf_counter()
    rid = req.request_id or str(uuid.uuid4())
    content = (req.content or "").strip()
    if not content:
        return EntityExtractResponse(
            request_id=rid,
            model="entity-mock-v0.1",
            events=[],
            entities=[],
            meta=EntityExtractMeta(mode=cfg.mode, notes=["empty_content"]),
            error={"code": "empty_content", "message": "content is empty"},
        )

    doc = normalize_document(
        title=req.title,
        content=content,
        published_at=req.published_at,
        source=req.source,
    )
    max_events = req.options.max_events if req.options else 3
    notes = ["entity_ext_v0.3"]
    mock_events, mock_entities = mock_entity_extract(doc, max_events=max_events)
    for mev in mock_events:
        etype, et_flags = normalize_event_type(mev.event_type)
        mev.event_type = etype
        if et_flags:
            mev.flags = list(mev.flags or []) + et_flags

    model = "entity-mock-v0.1"
    mode = "mock"
    events, entities = mock_events, mock_entities
    impact_done = False

    if cfg.mode == "llm":
        mode = "llm"
        try:
            client = OpenAICompatibleClient(
                base_url=cfg.llm_base_url,
                api_key=cfg.llm_api_key,
                model=cfg.llm_model,
                temperature=cfg.llm_temperature,
                timeout_sec=cfg.llm_timeout_sec,
                max_retries=cfg.llm_max_retries,
            )
            system = (
                _PROMPT.read_text(encoding="utf-8")
                if _PROMPT.exists()
                else "抽取科技资讯实体与事件，输出 JSON。"
            )
            user = (
                f"标题：{doc.title or '（无）'}\n"
                f"来源：{doc.source or '（无）'}\n"
                f"正文：\n{doc.content}\n\n"
                f"请抽取最多 {max_events} 个事件，并给出 entities[]。"
                f"每个事件尽量给出非空 impact（技术/应用作用）；"
                f"仅当全文无效果表述时才允许 impact=null。"
            )
            raw, _, _ = client.generate(system=system, user=user)
            events, entities = _parse_llm_entity_payload(raw, max_events=max_events)
            for ev in events:
                ev.completion_time, extra_flags = enrich_completion_time(
                    ev.completion_time, doc.published_at
                )
                if extra_flags:
                    ev.flags = list(ev.flags or []) + extra_flags
            entities = _merge_entities(entities, mock_entities)
            model = cfg.llm_model
            notes.append("llm_entity_extract_ok")
            if cfg.enable_impact_pass and events:
                try:
                    filled, _, _ = llm_impact_pass(
                        client=client,
                        events=events,  # type: ignore[arg-type]
                        doc=doc,
                    )
                    events = filled  # type: ignore[assignment]
                    notes.append("entity_llm_impact_pass_ok")
                    impact_done = True
                except Exception as exc:
                    notes.append(
                        f"entity_llm_impact_pass_error:{type(exc).__name__}"
                    )
        except Exception as exc:
            logger.warning("entity_llm_fallback_mock: %s", exc)
            events, entities = mock_events, mock_entities
            model = "entity-mock-v0.1"
            notes.append(f"llm_entity_extract_failed_fallback_mock:{type(exc).__name__}:{exc}")

    if cfg.enable_impact_pass and events and not impact_done:
        events = mock_impact_pass(events, doc.content)  # type: ignore[arg-type]
        notes.append("entity_rule_impact_pass")

    notes.extend(validate_impact_entity_joint(events, entities))

    latency = int((time.perf_counter() - t0) * 1000)
    return EntityExtractResponse(
        request_id=rid,
        model=model,
        events=events,
        entities=entities,
        meta=EntityExtractMeta(
            schema_version="entity-v0.1",
            mode=mode if cfg.mode == "llm" and "llm_entity_extract_ok" in notes else "mock",
            latency_ms=latency,
            entity_count=len(entities),
            event_count=len(events),
            notes=notes,
        ),
    )

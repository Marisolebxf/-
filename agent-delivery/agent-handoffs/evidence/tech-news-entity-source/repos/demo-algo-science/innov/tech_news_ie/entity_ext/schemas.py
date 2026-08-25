from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from ..schemas import (
    CompletionTime,
    Confidence,
    Evidence,
    ExtractOptions,
    ExtractRequest,
)


EntityType = Literal[
    "company",
    "research_org",
    "policy",
    "industry",
    "technology",
    "expert",
    "patent",
]

EventType = Literal[
    "product_release",
    "tech_breakthrough",
    "delivery",
    "certification",
    "collaboration",
    "policy_publish",
    "other",
]


class EntityMention(BaseModel):
    type: EntityType
    name: str
    normalized: str | None = None
    evidence: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class TechNewsEventExt(BaseModel):
    company_name: list[str] = Field(default_factory=list)
    completion_time: CompletionTime = Field(default_factory=CompletionTime)
    completed_matter: str | None = None
    impact: str | None = None
    event_type: EventType = "other"
    news_source: str | None = None
    entity_refs: list[str] = Field(default_factory=list)
    evidence: Evidence = Field(default_factory=Evidence)
    confidence: Confidence = Field(default_factory=Confidence)
    flags: list[str] = Field(default_factory=list)


class EntityExtractMeta(BaseModel):
    schema_version: str = "entity-v0.1"
    mode: str = "mock"
    latency_ms: int = 0
    entity_count: int = 0
    event_count: int = 0
    notes: list[str] = Field(default_factory=list)


class EntityExtractRequest(ExtractRequest):
    """Reuse four-factor request body; options still apply to max_events."""

    options: ExtractOptions = Field(default_factory=ExtractOptions)


class EntityExtractResponse(BaseModel):
    request_id: str
    model: str
    events: list[TechNewsEventExt] = Field(default_factory=list)
    entities: list[EntityMention] = Field(default_factory=list)
    meta: EntityExtractMeta = Field(default_factory=EntityExtractMeta)
    error: dict | None = None

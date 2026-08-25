from __future__ import annotations

import re

from ..normalize import NormalizedDoc
from ..schemas import CompletionTime, Confidence, Evidence
from .schemas import EntityMention, EventType, TechNewsEventExt

# (type, pattern) — order matters for first-match spans; mock only.
_ENTITY_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("patent", re.compile(r"(CN\d{9,}[A-Z]?|发明专利|实用新型专利)")),
    (
        "policy",
        re.compile(
            r"《([^》]{2,40})》|(?:国家|国务院|工信部|发改委)[^，。；\n]{0,20}(?:规划|条例|办法|意见|通知)"
        ),
    ),
    (
        "research_org",
        re.compile(
            r"([\u4e00-\u9fffA-Za-z0-9·]{2,30}(?:大学|科学院|研究院|研究所|实验室|学院))"
        ),
    ),
    (
        "company",
        re.compile(
            r"([\u4e00-\u9fffA-Za-z0-9·]{2,30}(?:股份有限公司|有限公司|集团))|(小米|华为|腾讯|阿里巴巴|比亚迪|宁德时代)"
        ),
    ),
    (
        "expert",
        re.compile(
            r"([\u4e00-\u9fff]{2,4})(?:院士|教授|研究员|博士|总裁|院长)"
        ),
    ),
    (
        "industry",
        re.compile(
            r"(新能源汽车|半导体|人工智能|生物医药|低空经济|人形机器人|工业软件|量子计算)"
        ),
    ),
    (
        "technology",
        re.compile(
            r"(玄戒O3|澎湃OS|MiMo大模型|大模型|关节模组|视觉模型|工业仿真平台[\d.]*|固态电池|氮化镓)"
        ),
    ),
]

_EVENT_HINTS: list[tuple[EventType, tuple[str, ...]]] = [
    ("collaboration", ("联合", "共建", "合作", "签约")),
    ("certification", ("备案", "认证", "准入", "合规")),
    ("delivery", ("交付", "量产", "投运", "出货")),
    ("product_release", ("发布", "推出", "上线", "开源")),
    ("policy_publish", ("印发", "出台", "施行", "公布")),
    ("tech_breakthrough", ("突破", "攻关", "首创", "首次")),
]

_TIME_RE = re.compile(
    r"(20\d{2}\s*年\s*(?:\d{1,2}\s*月)?(?:\s*\d{1,2}\s*日)?|20\d{2}-\d{2}(?:-\d{2})?)"
)
_SOURCE_RE = re.compile(r"来源[:：]\s*([^\s，。；\n]{2,20})")


def _norm_time(raw: str) -> CompletionTime:
    s = re.sub(r"\s+", "", raw)
    m = re.match(r"(20\d{2})年(\d{1,2})月(\d{1,2})日", s)
    if m:
        return CompletionTime(
            raw=raw.strip(),
            normalized=f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}",
            granularity="day",
        )
    m = re.match(r"(20\d{2})年(\d{1,2})月", s)
    if m:
        return CompletionTime(
            raw=raw.strip(),
            normalized=f"{m.group(1)}-{int(m.group(2)):02d}",
            granularity="month",
        )
    m = re.match(r"(20\d{2})年", s)
    if m:
        return CompletionTime(raw=raw.strip(), normalized=m.group(1), granularity="year")
    m = re.match(r"(20\d{2}-\d{2}-\d{2})", s)
    if m:
        return CompletionTime(raw=raw.strip(), normalized=m.group(1), granularity="day")
    m = re.match(r"(20\d{2}-\d{2})", s)
    if m:
        return CompletionTime(raw=raw.strip(), normalized=m.group(1), granularity="month")
    return CompletionTime(raw=raw.strip(), normalized=None, granularity=None)


def _guess_event_type(text: str) -> EventType:
    for et, keys in _EVENT_HINTS:
        if any(k in text for k in keys):
            return et
    return "other"


def mock_entity_extract(
    doc: NormalizedDoc, max_events: int = 3
) -> tuple[list[TechNewsEventExt], list[EntityMention]]:
    text = f"{doc.title or ''}\n{doc.content}"
    entities: list[EntityMention] = []
    seen: set[tuple[str, str]] = set()

    for etype, pat in _ENTITY_PATTERNS:
        for m in pat.finditer(text):
            name = next((g for g in m.groups() if g), m.group(0))
            name = (name or "").strip()
            if not name or len(name) < 2:
                continue
            key = (etype, name)
            if key in seen:
                continue
            seen.add(key)
            entities.append(
                EntityMention(
                    type=etype,  # type: ignore[arg-type]
                    name=name,
                    evidence=[m.group(0)[:80]],
                    confidence=0.55 if etype in {"industry", "technology"} else 0.7,
                )
            )

    source = doc.source
    if not source:
        sm = _SOURCE_RE.search(text)
        source = sm.group(1) if sm else None

    # Build events: prefer company/research_org as subjects
    subjects = [e for e in entities if e.type in {"company", "research_org"}]
    if not subjects and entities:
        subjects = entities[:1]

    times = [_norm_time(m.group(1)) for m in _TIME_RE.finditer(text)]
    event_type = _guess_event_type(text)
    matter = (doc.title or "").strip() or "科技成果事项（mock）"
    if len(matter) > 40:
        matter = matter[:40]

    events: list[TechNewsEventExt] = []
    if not subjects:
        events.append(
            TechNewsEventExt(
                company_name=[],
                completion_time=times[0] if times else CompletionTime(),
                completed_matter=matter,
                impact=None,
                event_type=event_type,
                news_source=source,
                entity_refs=[e.name for e in entities[:5]],
                evidence=Evidence(matter=[matter] if matter in text else []),
                confidence=Confidence(overall=0.3, completed_matter=0.3),
                flags=["missing_company", "mock_heuristic"],
            )
        )
    else:
        for subj in subjects[:max_events]:
            events.append(
                TechNewsEventExt(
                    company_name=[subj.name],
                    completion_time=times[0] if times else CompletionTime(),
                    completed_matter=matter,
                    impact=None,
                    event_type=event_type,
                    news_source=source,
                    entity_refs=[e.name for e in entities[:8]],
                    evidence=Evidence(
                        company=[subj.name],
                        time=[times[0].raw] if times and times[0].raw else [],
                        matter=[matter] if matter in text else [],
                    ),
                    confidence=Confidence(
                        company_name=0.7,
                        completion_time=0.6 if times else 0.0,
                        completed_matter=0.5,
                        overall=0.55,
                    ),
                    flags=["mock_heuristic"],
                )
            )

    return events[:max_events], entities

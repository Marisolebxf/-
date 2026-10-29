"""E-TECH-NEWS-ENTITY-M4-L02 local HTTP smoke (entity-extract + list/get + q).

Usage:
  cd repos/demo-algo-science
  $env:PYTHONPATH=(Get-Location).Path
  $env:TECH_NEWS_IE_MODE='mock'
  $env:TECH_NEWS_IE_STORE='sqlite'
  .\\.venv\\Scripts\\python scripts\\tech_news_entity_m4_l02_smoke.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

os.environ.setdefault("TECH_NEWS_IE_MODE", "mock")
os.environ.setdefault("TECH_NEWS_IE_STORE", "sqlite")
os.environ.setdefault("TECH_NEWS_IE_PERSIST", "true")
os.environ.setdefault(
    "TECH_NEWS_IE_DB_PATH", str(ROOT / "data" / "m4_l02_smoke.sqlite")
)

from fastapi.testclient import TestClient  # noqa: E402

from innov.tech_news_ie.api import create_app  # noqa: E402
from innov.tech_news_ie.config import get_settings  # noqa: E402


def main() -> int:
    get_settings.cache_clear()
    client = TestClient(create_app())
    health = client.get("/tech-news/healthz")
    assert health.status_code == 200, health.text

    rid = "m4-l02-smoke-001"
    body = {
        "title": "M4-L02 smoke 小米玄戒",
        "content": (
            "2026年7月，小米集团发布玄戒芯片，助力人工智能与智能制造产业发展，"
            "显著提升端侧算力。"
        ),
        "source": "m4-l02-smoke",
        "published_at": "2026-07-28",
        "request_id": rid,
    }
    extract = client.post(
        "/internal/tech-news/entity-extract",
        params={"persist": True},
        json=body,
        headers={"X-Request-Id": rid},
    )
    assert extract.status_code == 200, extract.text
    ej = extract.json()
    assert ej.get("error") is None, ej
    assert ej.get("events"), ej
    assert ej.get("entities"), ej

    listing = client.get(
        "/internal/tech-news/entity-extractions",
        params={"limit": 10, "offset": 0, "q": "小米"},
    )
    assert listing.status_code == 200, listing.text
    lj = listing.json()
    assert any(i.get("id") == rid for i in (lj.get("items") or [])), lj

    detail = client.get(f"/internal/tech-news/entity-extractions/{rid}")
    assert detail.status_code == 200, detail.text
    dj = detail.json()
    assert dj.get("response"), dj

    out_dir = (
        Path(os.environ.get("GKX_ROOT", r"E:/gkx-lumen"))
        / "gkx-orchestration"
        / "agent-delivery"
        / "agent-handoffs"
        / "evidence"
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    evidence = {
        "ok": True,
        "health": health.json(),
        "extract_request_id": rid,
        "event_count": len(ej.get("events") or []),
        "entity_count": len(ej.get("entities") or []),
        "event_types": [e.get("event_type") for e in (ej.get("events") or [])],
        "entity_names": [e.get("name") for e in (ej.get("entities") or [])],
        "list_total": lj.get("total"),
        "list_q": lj.get("q"),
        "detail_has_response": True,
        "env_note": {
            "TECH_NEWS_IE_STORE": os.environ.get("TECH_NEWS_IE_STORE"),
            "mysql_live": False,
            "k8s_pc": "http://10.50.69.111:30891 → 502 at smoke time",
        },
    }
    path = out_dir / "E-TECH-NEWS-ENTITY-M4-L02-api-smoke.json"
    path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(evidence, ensure_ascii=False, indent=2))
    print("wrote", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

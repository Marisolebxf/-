#!/usr/bin/env python3
"""Summarize a Tempo /api/traces/{id} JSON dump (OTLP JSON).

Usage on jump host:
  python3 /tmp/trace-summarize.py /tmp/trace.json
  python3 /tmp/trace-summarize.py /tmp/trace.json --db
"""
from __future__ import annotations

import argparse
import base64
import json
import sys


def b64_hex(s: str | None) -> str:
    if not s:
        return "-"
    pad = "=" * (-len(s) % 4)
    return base64.b64decode(s + pad).hex()


def attr_map(attrs: list) -> dict:
    out = {}
    for a in attrs or []:
        v = a.get("value") or {}
        out[a["key"]] = next(iter(v.values()), None)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="Tempo trace JSON file")
    ap.add_argument("--db", action="store_true", help="also list unique db.* attrs")
    args = ap.parse_args()

    data = json.load(open(args.path, encoding="utf-8"))
    batches = data.get("batches") or []
    if not batches:
        print("EMPTY: no batches (wrong Tempo port or trace expired)", file=sys.stderr)
        return 1

    db_seen: set[tuple] = set()
    for b in batches:
        res = attr_map(b.get("resource", {}).get("attributes"))
        svc = res.get("service.name", "?")
        for ss in b.get("scopeSpans") or []:
            for s in ss.get("spans") or []:
                attrs = attr_map(s.get("attributes"))
                start = int(s.get("startTimeUnixNano") or 0)
                end = int(s.get("endTimeUnixNano") or 0)
                dur_ms = (end - start) / 1e6 if end and start else 0.0
                name = (s.get("name") or "")[:70]
                sid = b64_hex(s.get("spanId"))[:8]
                par = b64_hex(s.get("parentSpanId"))[:8]
                status = s.get("status") or {}
                print(f"{svc:28s} {dur_ms:9.1f}ms {name:70s} span={sid} parent={par} status={status}")
                if args.db and ("db.system" in attrs or "db.name" in attrs):
                    key = (attrs.get("db.name"), attrs.get("server.address"), attrs.get("db.system"))
                    db_seen.add(key)

    if args.db:
        print("--- db endpoints ---")
        for k in sorted(db_seen):
            print(k)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

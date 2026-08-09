---
name: ponytail
description: >
  Set GKX ponytail intensity for coding: lite, full (default), ultra, or off.
  Use when the user says /ponytail, "ponytail full|lite|ultra|off", "lazy mode",
  "be lazy", "simplest solution", or "stop ponytail" / "normal mode".
  Coding tasks only. Respect GKX guards in .cursor/rules/ponytail.mdc.
---

# Ponytail（GKX · Cursor）

Read and obey `.cursor/rules/ponytail.mdc` (GKX 护栏 first). Full guide: `agent-delivery/ponytail-usage.md`.

## Mode from user message

| User says | Mode |
|-----------|------|
| `lite` / `/ponytail lite` | **lite** — build what's asked; one-line lazier alternative |
| `full` / `/ponytail` / `/ponytail full` / default | **full** — enforce the ladder; shortest working diff |
| `ultra` / `/ponytail ultra` | **ultra** — YAGNI extremist; challenge scope; prefer deletion |
| `off` / `/ponytail off` / `stop ponytail` / `normal mode` | **off** — do not minimize LOC this turn/session; still obey architecture + D8/D9/D10 |

Confirm in one short line: `ponytail: <mode>` then continue the coding task.

## Ladder (full / ultra)

YAGNI → reuse in repo → stdlib → native → installed dep → one line → minimum. Read the flow first. Bugfix = root cause + all callers.

## Never skip (GKX)

Call chain, Nebula, observability, handoff, Design/D9/D10, demo→lumen parity.

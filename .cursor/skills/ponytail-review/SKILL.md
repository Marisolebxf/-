---
name: ponytail-review
description: >
  Over-engineering review only: list what to delete from the current diff or
  named files. Trigger: /ponytail-review, "ponytail-review", "过度工程审查",
  "what can we delete". Do not apply fixes. Out of scope: correctness, security,
  performance. Respect GKX: never flag D8/D9/D10/observability/handoff as yagni.
---

# Ponytail-review（GKX）

Review for unnecessary complexity only. Output a delete-list; **do not edit code** unless the user then asks to apply.

Guide: `agent-delivery/ponytail-usage.md` §6.

## Format

One finding per line:

`path:L12-38: yagni: AbstractRepository with one impl. Inline until a second exists.`

Tags: `delete:` | `stdlib:` | `native:` | `yagni:` | `shrink:`

End with: `net: -N lines possible.`  
If nothing to cut: `Lean already. Ship.`

## Boundaries

- Scope = over-engineering only.
- Do **not** flag: trust-boundary validation, data-loss handling, security, a11y, metric ⓘ / readiness badges, Design-required components, observability, handoff artifacts, or a single small self-check/test for non-trivial logic.
- Correctness / security / perf → say they need a normal review pass, not this skill.

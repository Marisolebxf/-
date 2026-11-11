---
name: feishu-bugfix
description: Process bugs assigned to the current user from Feishu Project using the official Feishu Project MCP. Use when the user asks to inspect, fix, verify, or ship their OPEN/REOPEN Feishu Project bugs.
---

# Feishu Bug Fix Client Adapter

The canonical Skill package is:

```text
.cursor/skills/feishu-bugfix/
```

Before handling a Feishu Project bug:

1. Read `.cursor/skills/feishu-bugfix/SKILL.md` and follow it as the authoritative Skill instructions.
2. Resolve `scripts/`, `references/`, `templates/`, and `policies/` relative to the canonical Skill directory.
3. Use `agent-delivery/bugfix-runs/` only for per-run state, evidence and reports.
4. Do not create or maintain a second Skill implementation in this client directory.

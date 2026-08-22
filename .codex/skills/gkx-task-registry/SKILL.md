---
name: gkx-task-registry
description: >
  Query and update GKX task-registry via MCP (never read task-registry.yaml).
  Use when the user mentions task-id, 认领, 派单, 看板, ready/claimed/in_progress,
  handoff 回填, AV-0/AV-1, or task-query/task-claim/task-update-status.
---

# GKX 任务注册表（MCP）

真源与 Cursor 同文：`.cursor/skills/gkx-task-registry/SKILL.md`。改技能先改那边。

查或改任务走 MCP `task-registry`，不要打开 `agent-delivery/task-registry.yaml`。上手：`agent-delivery/task-mcp-usage-guide.md`。认领门禁：`gkx-task-claim-supervision`。指标查询：`gkx-metric-lookup`。

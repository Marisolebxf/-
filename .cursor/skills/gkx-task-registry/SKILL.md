---
name: gkx-task-registry
description: >
  Query and update GKX task-registry via MCP (never read task-registry.yaml).
  Use when the user mentions task-id, 认领, 派单, 看板, ready/claimed/in_progress,
  handoff 回填, AV-0/AV-1, or task-query/task-claim/task-update-status.
---

# GKX 任务注册表（MCP）

查或改任务时走 MCP `task-registry`，不要打开 `agent-delivery/task-registry.yaml`。
`.cursor/mcp.json` 里的 `task-registry` 进程必须保持挂载；本 Skill 只教怎么调，不替代 MCP。

上手：`agent-delivery/task-mcp-usage-guide.md`。状态机 / 闸门：公约 §7。认领门禁：`gkx-task-claim-supervision`。

## 何时用

用户或任务提到：task-id / `E-*` / 认领 / 派单 / 看板 / `ready` / `claimed` / `in_progress` / handoff 回填 / AV-0 / AV-1 / `task-query`。

只谈指标 8 件套 / D1–D4 → `gkx-metric-lookup`。只谈开工监管人 / lock，尚未调工具 → `gkx-task-claim-supervision`。

## 怎么调

1. 先 `GetMcpTools`（server 多为 `user-task-registry`，面板名 `task-registry`），再 `CallMcpTool`。不要盲填参数。
2. 按意图选工具：

| 意图 | 工具 |
|---|---|
| 已知 ID | `task-get` |
| 按模块 / 状态 / Epic / Agent 搜 | `task-query`（`limit` 默认 20；详情才 `fields=full`） |
| 只要计数 / 待认领摘要 | `task-summary` |
| 认领 | `task-claim`（`claimed_by` 必填；Agent 执行时 `supervised_by` 必为花名册真人） |
| 改状态 | `task-update-status`（闸门状态带 `actor`） |
| 回填 evidence / cost / user_story | `task-update-fields`（不改状态） |
| 阻塞 | `task-set-blocked` |
| 建单 | `task-create`（仅 coordinator / PM；建单 ≠ 认领） |
| 单条验收 | `task-review` |
| 批量验收 | `task-review-batch`（默认 `auto_fix=false`） |

3. MCP 未加载：提示重启 Cursor，核对 `.cursor/mcp.json` 的 `task-registry` 段。仍不要整文件读 YAML。

## 闸门（调写工具时）

- `pending_test → testing`：`actor` 为 `agent:qa-agent` 或监管人 `human:黄敬洲`。长任务 `claim_type=coordinator_dispatch` 才允许 `actor=agent:coordinator-agent`，且须立刻派 qa-agent。
- `ready_to_sign → done`：`actor=human:淮政玮`（`chore` 豁免）。
- `user_story` 只写故事库 ID（逗号分隔），禁止写全文。
- 联调确认写进 `note`：`联调通过` / `会签通过` / `集成测试通过` 等，否则 AV-1 不过。

## 禁止

- 直接读 / 改 `task-registry.yaml`（含 Grep 当查询结果）
- 未 `GetMcpTools` 就调工具，或把 MCP 进程抽进本目录 `scripts/`
- 非 coordinator / PM 调 `task-create`
- 把 `review` 当完成路径（legacy）；handoff 后走 `task-review` / 状态机，不手填 `review`
- 用本 skill 绕过认领门禁或替用户猜 `supervised_by`

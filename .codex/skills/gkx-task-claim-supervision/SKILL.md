---
name: gkx-task-claim-supervision
description: Use when starting implementation, documentation changes, demo changes, handoffs, or status updates under the gkx-orchestration task system, especially when a task ID, ready status, registry claim, human supervisor, lock, or review transition is involved.
---

# GKX 任务认领与监管

在 `gkx-orchestration` 的任务体系内，先认领、后动手。Agent 可以执行，真人必须监管并在任务登记表留痕。

权威规则：`agent-delivery/task-claiming-guide.md`；机器真源：`agent-delivery/task-registry.yaml` 与 `agent-delivery/team-roster.yaml`。团队协作边界与人机红线以 `agent-delivery/team-collaboration-playbook.md` 为准。

## 标准顺序

每次**拆分、派发、认领或启动项目交付任务**必须按以下顺序执行；前一步未完成，不进入下一步：

1. **读团队公约**：完整读取 `agent-delivery/team-collaboration-playbook.md`，确认人机分工、团队边界、本机 Cursor 会话上限（≠派单上限）、分支/可逆性、交付接口和红线。
2. **读认领规则**：读取 `agent-delivery/task-claiming-guide.md`，确认状态机、认领类型、锁定时长、串行/Convoy 约束和变更权限。
3. **核验人员**：读取 `agent-delivery/team-roster.yaml`，确认执行 Agent 与真人监管人均有效。`max_agent_concurrency` 仅约束该人**本机 Cursor 会话**数，**不**因 registry 挂载条数拒派/拒认领。
4. **核验任务**：读取 `agent-delivery/task-registry.yaml` 中的具体 task 条目，检查 `ready`、依赖、`blocked_by`、同仓同分支占用、DoR 和验收标准。
5. **先向用户报备**：报告 task-id、执行 Agent、监管人、认领类型、锁定窗口和计划产物；未获明确确认不改 registry、不派发、不执行项目改动。
6. **写入认领**：确认后立即写入 registry 的 `claimed_by`、`supervised_by`、`claim_type`、`claimed_at`、`lock_until`，再开始交付工作。
7. **执行与留证**：明确开工或首个 commit 后转 `in_progress`（默认 `${GKX_ROOT}/repos/{repo}` 主工作区，不强制 worktree；lumen-* 默认 push `origin/dev`）；按 DoD 交付并保留提交、验证、风险和开放项证据。本机同时打开的 Cursor agent 会话建议 ≤ `max_agent_concurrency`（默认 4），超出用 Background Agents。
8. **交接与关闭**：提交 handoff 时转 `review`；仅 coordinator 验收后转 `done`。阻塞时立即转 `blocked` 并写明原因，停止推进。

禁止倒序、跳步或以“已有 task-id / 仅改文档 / 紧急修复”为由绕过上述流程。只回答问题、只读诊断或维护本 skill 本身时，不触发项目任务认领。

## 开工门禁

在修改代码、文档、Demo、任务状态或创建 handoff 前：

1. **先完整读取** `agent-delivery/team-collaboration-playbook.md`，确认本任务的人机分工、团队边界、分支/可逆性和交付接口约束；不得只读认领指南或登记表即派发、拆分或认领任务。
2. 确认具体 `task-id`，读取对应 registry 条目。
3. 确认 `status: ready`、`depends_on` 已全部 `done`、没有 `blocked_by`，且不存在未完成的串行前序任务。
4. 确认执行 Agent 与花名册中的真人监管人；不得猜测或缩写 `supervised_by`。
5. （可选）提醒监管人本机 Cursor 会话 ≤ `max_agent_concurrency`；**不得**因该人名下已有 ≥4 条 registry 活跃 task 而拒绝认领。
6. 向用户报告“task-id、执行 Agent、监管人、认领类型、4 小时锁定窗口”。未获明确确认，不编辑 registry、不开始执行。

只回答问题、读取资料或做无写入诊断时，不需要认领。维护本地 `.codex/skills/` 这类复用方法工具也不属于项目交付任务，除非用户明确要求将其登记为 registry task；其余会产生项目交付物的仓库改动均适用本门禁。

## 认领后执行

经监管真人确认后，先写入：

```yaml
status: claimed
claimed_by: agent:{role}
supervised_by: human:{花名册真名}
claim_type: pull
claimed_at: "ISO 8601 +08:00"
lock_until: "claimed_at + 4h"
```

- 明确开工或首个 commit 时改为 `in_progress`（不要求创建 worktree；冲突/并行时再开）。
- 提交 handoff 时改为 `review`，附 task-id、提交、验证和开放项。
- 遇到依赖、权限、数据或环境阻塞时立即改为 `blocked` 并写 `blocked_by` 与原因；停止继续推进。
- 只有 coordinator 验收后才能改为 `done`。Agent 不自行关闭任务。

## 约束

- 不自行认领、不替用户猜测监管人、不绕过 `ready` 或串行依赖。
- 不得跳过团队协作公约；即使任务仅涉及文档、Demo、看板更新或已有 task-id，也必须先完成公约预读。
- 不把历史已完成工作倒填为认领状态；需要审计修复时先请 coordinator 指示。
- `claimed_by` 为 Agent 时，`supervised_by` 必须是花名册中的真人；registry 挂载条数**无** ≤4 上限。本机同时开 Cursor agent 会话建议 ≤ `max_agent_concurrency`。
- 在开始每个新任务时重新核验；不要复用前一个任务的锁或认领字段。

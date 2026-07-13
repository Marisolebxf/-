---
name: gkx-task-claim-supervision
description: Use when starting implementation, documentation changes, demo changes, handoffs, or status updates under the gkx-orchestration task system, especially when a task ID, ready status, registry claim, human supervisor, lock, or review transition is involved.
---

# GKX 任务认领与监管

在 `gkx-orchestration` 的任务体系内，先认领、后动手。Agent 可以执行，真人必须监管并在任务登记表留痕。

权威规则：`agent-delivery/task-claiming-guide.md`；机器真源：`agent-delivery/task-registry.yaml` 与 `agent-delivery/team-roster.yaml`。团队协作边界与人机红线以 `agent-delivery/team-collaboration-playbook.md` 为准。

## 开工门禁

在修改代码、文档、Demo、任务状态或创建 handoff 前：

1. **先完整读取** `agent-delivery/team-collaboration-playbook.md`，确认本任务的人机分工、团队边界、并发上限、分支/可逆性和交付接口约束；不得只读认领指南或登记表即派发、拆分或认领任务。
2. 确认具体 `task-id`，读取对应 registry 条目。
3. 确认 `status: ready`、`depends_on` 已全部 `done`、没有 `blocked_by`，且不存在未完成的串行前序任务。
4. 确认执行 Agent 与花名册中的真人监管人；不得猜测或缩写 `supervised_by`。
5. 检查该监管人当前监管的 Agent 数量不超过 4。
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

- 创建 worktree 或首个 commit 时改为 `in_progress`。
- 提交 handoff 时改为 `review`，附 task-id、提交、验证和开放项。
- 遇到依赖、权限、数据或环境阻塞时立即改为 `blocked` 并写 `blocked_by` 与原因；停止继续推进。
- 只有 coordinator 验收后才能改为 `done`。Agent 不自行关闭任务。

## 约束

- 不自行认领、不替用户猜测监管人、不绕过 `ready` 或串行依赖。
- 不得跳过团队协作公约；即使任务仅涉及文档、Demo、看板更新或已有 task-id，也必须先完成公约预读。
- 不把历史已完成工作倒填为认领状态；需要审计修复时先请 coordinator 指示。
- `claimed_by` 为 Agent 时，`supervised_by` 必须是花名册中的真人；同一时间每位真人最多监管 4 个 Agent。
- 在开始每个新任务时重新核验；不要复用前一个任务的锁或认领字段。

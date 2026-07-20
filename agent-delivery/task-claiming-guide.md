# 任务认领指南（claimed_by / supervised_by）

> **读者**：全员（工程师、lead、coordinator、PM）  
> **作用**：统一解释任务认领字段、流程与职责边界，避免双派、占坑、责任不清  
> **机器真源**：`task-registry.yaml`（字段写入）· `team-roster.yaml`（花名册）  
> **关联**：`智能体编排与派单手册.md` §十三 · `team-collaboration-playbook.md` · `coordinator.mdc`

---

## 1. 一句话

> **认领 = 在 Sprint 内公开承诺「这个 task 现在谁负责」；Agent 写代码，人（真名）承担监管责任。**

---

## 2. 名词解释（Glossary）

| 名词 | 英文/字段 | 含义 | 示例 |
|------|-----------|------|------|
| **任务** | task / leaf | `task-registry.yaml` 中一条可派工、可验收的工作项 | `E-E7-POLICY-M1-L01` |
| **认领** | claim | 把 task 从「可领取」变为「已有人负责」，防止两人同时做 | 写 `claimed_by` |
| **认领人** | claimer | 直接承担 task 进度的人（通常是 lead 或工程师） | `human:张三` |
| **执行 Agent** | executor agent | 实际写代码/出设计的 AI 角色 | `agent:frontend-agent` |
| **监管人** | supervisor | **开 Cursor 会话、监管 Agent 产出**的真人（必填真名） | `human:张三` |
| **认领字段** | `claimed_by` | 记录「谁认领了这条 task」 | 见 §4 |
| **监管字段** | `supervised_by` | 记录「谁监管这次 Agent 执行」（真名） | `human:李四` |
| **认领时间** | `claimed_at` | ISO 8601 时间戳 | `2026-07-11T09:30:00+08:00` |
| **锁超时** | `lock_until` | 认领 lease 过期时间；超时未推进则释放回 `ready` | 默认 +4h |
| **认领类型** | `claim_type` | `pull`（主动领取）或 `coordinator_dispatch`（协调员代派） | 见 §5 |
| **就绪** | `ready` | 依赖已满足、DoR 通过，可进 Sprint 认领 | 替代原 `pending`（依赖已完） |
| **花名册** | `team-roster.yaml` | 团队真名 ↔ 团队/角色映射，防拼写漂移 | 见 §8 |

### 2.1 `claimed_by` 与 `supervised_by` 的区别（最常问）

| 问题 | `claimed_by` | `supervised_by` |
|------|--------------|-----------------|
| 回答什么 | **这条 task 现在归谁管进度** | **哪个真人在看这次 Agent 会话** |
| 何时必填 | 所有 `claimed` 及之后状态 | **只要用 Agent 执行就必填** |
| 典型值 | `human:张三` 或 `agent:frontend-agent` | `human:张三`（永远真名） |
| 站会「负责人」 | 优先显示 `supervised_by`；无则显示 `claimed_by` 中的人名 | — |
| 与 commit 关系 | — | 与 `[human:张三]` commit 标记同一人 |

**记忆口诀**：Agent 动手，`supervised_by` 填真人；人自己干，`claimed_by` 填真人。

---

## 3. 状态机（Task 走到哪一步）

```text
backlog → ready → claimed → in_progress → review → done
              ↘ blocked ↗
```

| 状态 | 含义 | 谁推进到下一状态 |
|------|------|------------------|
| `backlog` | 在队列里，依赖或 DoR 未满足 | coordinator 扫描依赖 |
| `ready` | 可认领（Scrum：Sprint Ready） | 工程师 / coordinator |
| `claimed` | 已认领，尚未开始写代码 | 认领人 |
| `in_progress` | 正在执行（已明确开工 / 首 commit；默认主工作区，不要求 worktree） | 执行 Agent + 监管人 |
| `review` | handoff 已提交，待验收 | coordinator |
| `done` | DoD + 7 项 handoff checklist 全过 | coordinator |
| `blocked` | 阻塞，需 PM/架构师升级 | 任何人写 `blocked_by` |

> **过渡说明**：历史任务仍可能使用 `pending`；新任务统一用 `backlog` / `ready` 二分。

---

## 4. 字段格式（真名版，团队已定稿）

### 4.1 人直接认领（不用 Agent，或人自己写代码）

```yaml
status: claimed
claimed_by: human:张三
supervised_by: human:张三      # 与 claimed_by 相同即可
claim_type: pull
claimed_at: "2026-07-11T09:30:00+08:00"
lock_until: "2026-07-11T13:30:00+08:00"
```

### 4.2 人开 Agent 会话执行（最常见）

```yaml
status: claimed
claimed_by: agent:frontend-agent
supervised_by: human:张三        # 必填：谁开的 Cursor 会话
claim_type: pull
claimed_at: "2026-07-11T09:30:00+08:00"
lock_until: "2026-07-11T13:30:00+08:00"
# worktree_branch: feat/E-E7-L02   # 可选：仅同仓并行/冲突时启用
```

### 4.3 coordinator 代派

```yaml
status: claimed
claimed_by: agent:api-agent
supervised_by: human:李四        # 负责跟进的 lead / 工程师
claim_type: coordinator_dispatch
dispatched_by: human:王五          # 可选：执行派单的 coordinator 操作者
claimed_at: "2026-07-11T10:00:00+08:00"
lock_until: "2026-07-11T14:00:00+08:00"
```

### 4.4 命名铁律

1. **真名**：统一用中文真名，如 `human:张三`（与 git commit `[human:张三]` 一致）
2. **禁止混用**：同一人不得同时出现 `human:hzw` 与 `human:张三`
3. **Agent 前缀**：固定 `agent:{role}`，与 `task-registry` 中 `agent` 字段一致
4. **不可冒领**：只有对应团队 lead，或 lead 口头授权的人，才能写自己的真名

---

## 5. 认领类型（claim_type）

| 类型 | 谁发起 | 适用场景 |
|------|--------|----------|
| `pull` | 工程师 / lead | 站会认领、Ready 队列自取、自己开 Agent |
| `coordinator_dispatch` | coordinator | Epic 首开、紧急插队、Background Agent 预派 |

两种类型 **`supervised_by` 均必填**（Background Agent 填指派监管的 lead）。

---

## 6. 标准流程（5 步）

```mermaid
flowchart LR
  A[1. task 变 ready] --> B[2. 人/协调员认领]
  B --> C[3. 写 registry 字段]
  C --> D[4. 执行 + handoff]
  D --> E[5. coordinator 验收 → done]
```

### 步骤 1 · 任务变 Ready

- **触发**：`depends_on` 全部 `done`，无 `blocked_by`，DoD 已在 registry 中写清
- **谁做**：coordinator 扫描（或 `dispatch-queue.yaml` 的 `awaiting` 满足）
- **结果**：`status: ready`

### 步骤 2 · 认领（Pull 或 Dispatch）

- **Pull**：工程师在站会说「我认领 E-E7-L02」，或开 Agent 会话首句声明
- **Dispatch**：coordinator 在 Sprint Planning 或解锁下游时代派
- **Convoy 规则**：同组串行任务，前序未 `done` 时，后序即使 `ready` 也不可认领

### 步骤 3 · 写入 task-registry（立即，先于写代码）

认领人（或 coordinator）**在同一次会话内**更新 YAML：

```yaml
status: claimed          # 开始写代码后改 in_progress
claimed_by: ...
supervised_by: ...
claim_type: ...
claimed_at: ...
lock_until: ...          # 默认 claimed_at + 4h；Background Agent 可 +24h
```

> ⚠️ **先认领、后动手**：未写 `claimed_by` 就开 Agent = 违反流程，coordinator 可拒收 handoff。

### 步骤 4 · 执行

| 动作 | 状态变更 | 其他 |
|------|----------|------|
| 明确开工 / 首 commit（默认主工作区；冲突时再开 worktree） | `in_progress` | commit 含 `[human:真名]` 或 `[agent:role]`；lumen-* 默认 push `origin/dev` |
| 提交 handoff | `review` | `agent-handoffs/{task-id}.md` |
| 遇阻塞 | `blocked` | 写 `blocked_by` + 原因，站会升级 |

### 步骤 5 · 验收关闭

coordinator 按 `coordinator.mdc` handoff 7 项 checklist 验收 → `done`。

---

## 7. 角色职责速查

| 角色 | 认领相关职责 |
|------|-------------|
| **工程师** | Pull 认领；填 `supervised_by` 为自己真名；过期前续 `lock_until` 或释放 |
| **lead** | 审核本 team 认领是否合理；Complex task 优先由 lead 认领 |
| **coordinator** | 维护 Ready 队列；Dispatch 时代填 `supervised_by`；防双派；验收 `review→done` |
| **PM** | Sprint 边界：未入 Sprint 的 task 不得 silent 开工 |
| **Agent** | 不自行改 registry；会话首条由人声明认领 task-id |

---

## 8. 花名册（team-roster.yaml）

路径：`agent-delivery/team-roster.yaml`

- 新成员入职：lead 在 24h 内追加一行
- coordinator 验收时可对照：真名是否在册、`supervised_by` 是否属于对应 `team`
- Phase 0 人工核对；后续 ORCH 脚本强制校验

---

## 9. 站会三问（认领版）

1. **昨天**：哪些 task 从 `in_progress` → `review/done`？（报 task-id + 真名）
2. **今天**：认领哪些 `ready`？（报 task-id，当场或会后更新 registry）
3. **阻塞**：哪些 `blocked` 需 PM / 架构师？（报 `blocked_by`）

---

## 10. 常见场景 FAQ

**Q：我和同事可以同时认领不同 task 吗？**  
A：可以。WIP 限制是每人监管 **≤4 个** Agent 并发，不是只能认领 1 个。

**Q：认领错了怎么办？**  
A：在 `review` 之前：认领人改回 `ready` 并清空 `claimed_by`；已 `in_progress` 需 lead 确认后再释放。

**Q：Agent 会话崩了，task 一直 claimed 怎么办？**  
A：`lock_until` 过期 → coordinator 释放回 `ready` 并通知原 `supervised_by`。

**Q：甲方能看到真名吗？**  
A：不能。`claimed_by` / `supervised_by` 仅在 `gkx-orchestration` 内部 registry / 团队看板使用。

**Q：设计类 task（cicd: skip）也要 supervised_by 吗？**  
A：要。ux/ui/architect 用 Agent 时同样填监管人真名。

---

## 11. 违规与处理

| 违规 | 处理 |
|------|------|
| 未认领就提交 handoff | coordinator 拒收，`needs-revision` |
| 双派（两人同时 claimed） | 以 **先写入 git 的 commit** 为准，后者释放 |
| `supervised_by` 缺失 | 不得 `review→done` |
| 真名不在 roster | 提醒 lead 补 roster；Sprint 内完成 |
| 冒领（非本 team 未授权） | lead 撤销认领 |

---

## 12. Scrum 节拍 + Kanban 看板（落地）

> **Sprint 容器**：[`scrum-sprint.yaml`](scrum-sprint.yaml) · **当前 Sprint 看板**：[`sprints/2026-W28.md`](sprints/2026-W28.md)

### 12.1 两层队列

| 层 | 字段/文件 | 作用 |
|----|-----------|------|
| Product Backlog | `task-registry.yaml` 全部 leaf | Epic/Wave 全量任务 |
| Sprint Backlog | `sprint_id` + `scrum-sprint.yaml#committed_task_ids` | 本双周承诺 |
| Ready 列 | `status: ready` | 依赖满足，可认领 |
| 执行列 | `claimed` / `in_progress` / `review` | Kanban WIP |

### 12.2 与状态机的关系

```text
Product Backlog          Sprint Backlog           Kanban 执行
─────────────────        ────────────────         ─────────────
backlog (依赖未满足)  →   （不进 Sprint）          
backlog               →   下 Sprint Planning 排入
ready                 →   sprint_id 写入      →   Pull 认领 → claimed → …
blocked               →   站会升级 PM
```

### 12.3 四个仪式（最小集）

| 仪式 | 频率 | coordinator 做什么 |
|------|------|-------------------|
| **Planning** | 双周一次 90min | 投影 `ready` 列表；PM 选 task 写 `sprint_id`；填 `scrum-sprint.yaml` |
| **Daily** | 每日 15min | 更新 `sprints/{id}.md` burndown；释放过期 `lock_until` |
| **Review** | Sprint 末 | 汇总 Sprint 内 `done` task + demo 链接 |
| **Retro** | Sprint 末 60min | 复盘双派/占坑/token；改 guide / rules |

### 12.4 每日刷新 Ready 队列 + 看板近实时

依赖完成后 task 不会自动变 `ready`，需运行：

```powershell
.\scripts\sync-task-ready-status.ps1
```

coordinator **每日站会前**执行一次（或确认投影机（淮政玮长开电脑台式机） watch 在跑）。

**状态变更（主路径 · 跨平台 · 不强制 WSL）**：

```powershell
# Windows — Node 18+
.\scripts\update-task-status.ps1 -TaskId E-XXX -Status review
```

```bash
# macOS / Linux — Node 18+
./scripts/update-task-status.sh --task-id E-XXX --status review
```

默认推飞书；无 `FEISHU_*` 时软失败（YAML 已写）。详见 `feishu-bitable-near-realtime.md`。

**人类看板兜底**：投影机（长开机）注册 `register-board-sync-watch.ps1` / `.sh`（每 1 小时）；同步后自动 **git commit + push** `task-registry.yaml`（见 `feishu-bitable-near-realtime.md`）。站会仍可跑 bidirectional。飞书项目审批后改用 `sync-feishu-project.ps1`。

### 12.4.1 贡献分 / 难度（绩效）

派单时 **coordinator 必填**（见 `task-registry.yaml#contribution_policy`）：

| 字段 | 取值 | 说明 |
|------|------|------|
| `effort_points` | 1 / 2 / 3 / 5 / 8 / 13 | 贡献分（故事点） |
| `difficulty` | S / M / L / XL | 难度档 |

结算：`status=done` 的任务按 `claimed_by` 汇总 `Σ effort_points`（与 AI token 成本无关）。

```bash
# 历史补标（按 estimated_tokens 启发式；已有值不覆盖）
node scripts/backfill-effort-points.mjs
node scripts/backfill-effort-points.mjs --dry-run

# 按人汇总（默认当前 Sprint done）
node scripts/report-contribution.mjs
node scripts/report-contribution.mjs --all-done
```

飞书列：**贡献分**、**难度**（outbound 同步）。

### 12.5 WIP 限制

| 限制 | 值 | 说明 |
|------|-----|------|
| 每人监管 Agent | ≤4 | 见 playbook |
| 同 Convoy 组 | 1 | `dispatch-queue.yaml#convoy_groups` |
| review 待验收 | 8 告警 | coordinator 优先清 review |

---

## 13. 相关文档

| 文档 | 内容 |
|------|------|
| `智能体编排与派单手册.md` §十三 | 并发护栏 + 认领流程摘要 |
| `team-collaboration-playbook.md` | 团队节奏、站会、WIP≤4 |
| `coordinator.mdc` | coordinator 验收 checklist |
| `templates/handoff-template.md` | handoff 必填认领信息 |
| `orchestration-maturity-and-roadmap.md` | ORCH-L01 原子认领升级 |
| `scrum-sprint.yaml` | Sprint 容器 + 仪式日历 + WIP |
| `sprints/2026-W28.md` | 当前 Sprint 看板与 burndown |

---

**维护**：每次 Sprint retro 修订；字段格式变更须 PM + coordinator 双签。

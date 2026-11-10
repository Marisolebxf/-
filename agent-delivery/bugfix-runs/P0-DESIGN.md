# 飞书缺陷 AI Native P0 设计稿

> 状态：评审修订版
> 日期：2026-11-10
> 基线案例：飞书缺陷【2238】
> 设计原则：内部严格，外部简单；用户不维护状态机和证据模板

## 1. 已确认决策

1. 使用两个精确口令门：`【进入开发】`、`【提测】`。
2. 缺陷按 S/M/L 分级，简单缺陷保持轻流程。
3. 每个缺陷的运行账本放在：

```text
agent-delivery/bugfix-runs/<auto_number>-<work_item_id>/
```

自然语言“可以”“继续”“看起来没问题”不得解锁人工门。

## 2. 推广约束

本流程必须让普通同事只需做三件事：

1. 发起处理或确认目标缺陷；
2. 在合适时机发送 `【进入开发】`；
3. 在验证完成后发送 `【提测】`，最后完成一次业务验收。

以下内容全部由 Agent、Skill 和脚本内部完成，不要求同事理解或手工维护：

- 详细状态机；
- `state.json` 更新；
- 风险分级建议；
- 数据/Mock 策略读取；
- 证据索引和文件哈希；
- 评审和验证报告生成；
- 飞书评论草稿；
- 下一步提示。

## 3. 对外状态

普通同事只看到 6 个状态和一个旁路状态：

```text
已认领
  → 待进入开发
  → 修复中
  → 待提测
  → 待验收
  → 完成

任一状态可进入：受阻
```

详细状态由系统内部保存。简单缺陷自动连续推进，不展示 `REVIEWING`、`READY_SHIP` 等内部术语。

## 4. 内部状态机

```text
INTAKE
  → CLAIMED
  → DIAGNOSED
  → READY_DEV
  → IMPLEMENTING
  → REVIEWING
  → VERIFYING
  → READY_SHIP
  → SHIPPING
  → AWAITING_ACCEPTANCE
  → RESOLVED
```

旁路状态：

- `BLOCKED`：缺少复现、需求、权限、环境或测试能力。
- `REOPENED`：验收不通过或修复引入新问题。
- `CANCELLED`：缺陷关闭、重复或确认不需要修复。

`REOPENED` 只能回到 `DIAGNOSED`，重新确认根因和影响范围，不能直接跳回实现或提测。

### 对外状态映射

| 对外状态 | 内部状态 |
|---|---|
| 已认领 | `INTAKE` / `CLAIMED` |
| 待进入开发 | `DIAGNOSED` / `READY_DEV` |
| 修复中 | `IMPLEMENTING` / `REVIEWING` / `VERIFYING` |
| 待提测 | `READY_SHIP` |
| 待验收 | `SHIPPING` / `AWAITING_ACCEPTANCE` |
| 完成 | `RESOLVED` |
| 受阻 | `BLOCKED` / `REOPENED` |

## 5. 状态转换门槛

| 转换 | 前置条件 |
|---|---|
| `INTAKE → CLAIMED` | 找到当前用户名下的飞书缺陷；完成 `IN PROGRESS` 认领和 claim 评论；生成 `claim_id/session_id` |
| `CLAIMED → DIAGNOSED` | 截图/复现、根因假设、反证、需规证据、影响范围和数据策略已落盘 |
| `DIAGNOSED → READY_DEV` | 诊断可证伪；改动边界和验证计划明确；风险等级已生成 |
| `READY_DEV → IMPLEMENTING` | 收到当前会话中的精确口令 `【进入开发】` 并写入账本 |
| `IMPLEMENTING → REVIEWING` | 最小改动完成；无关改动已排除；仓库自检命令已记录 |
| `REVIEWING → VERIFYING` | S 级完成自审；M/L 完成净室评审或明确记录跳过理由 |
| `VERIFYING → READY_SHIP` | 回归矩阵、工程检查、提测前行为证据和残留风险已落盘 |
| `READY_SHIP → SHIPPING` | 收到当前会话中的精确口令 `【提测】` 并写入账本 |
| `SHIPPING → AWAITING_ACCEPTANCE` | 合并和 dev 部署完成；dev 真实复测通过；已生成验收步骤 |
| `AWAITING_ACCEPTANCE → RESOLVED` | 人工验收通过；飞书状态和最终评论已更新 |

## 6. 两个口令的准确语义

### `【进入开发】`

可请求条件：

- 用户可读缺陷编号和内部 ID；
- 期望行为与实际行为；
- 截图或复现步骤；
- 根因或可证伪的根因假设；
- 相关需规/验收标准及原文位置；
- 仓库、调用链和影响范围；
- 风险等级；
- 数据/Mock 策略；
- 初步验证计划。

用户发送口令后允许：

- 修改业务代码；
- 创建本地 commit；
- 推送独立的 `fix/*` 分支；
- 创建 Draft MR；
- 运行 CI 和提测前验证。

仍然禁止：

- 合并 `dev` / `main`；
- 部署 dev 或生产；
- 修改生产配置；
- 将飞书缺陷标记为已解决。

`.cursor/rules/fe-manual-confirm-push.mdc` 在实施阶段必须补充：当前会话中的 `【进入开发】` 可授权推送独立修复分支，但不得授权集成分支合并或部署。

### `【提测】`

可请求条件：

- commit、diff 和 Compare/MR；
- 改动文件及每处改动理由；
- 回归矩阵和实际结果；
- 提测前 CI/验证状态；
- 提测前页面、API、日志或数据库证据；
- 已知限制和回滚方式；
- 人工验收步骤。

用户发送口令后允许：

- 合并集成分支；
- 部署 dev；
- 在 dev 进行真实页面/API复测；
- 更新飞书提测信息。

P0 默认禁止生产部署。生产发布必须使用独立人工发布流程，不由本口令隐式授权。

## 7. S/M/L 分级

风险分级由 Agent 自动建议，用户不手工选择。定级只能上调，不得为了让流程更轻而自行降级；不确定时按 M 处理。

### S：单点低风险

典型场景：文案、样式、单字段展示、明确的单点逻辑。

最低要求：

- 相关调用链和测试；
- 业务逻辑问题：一个可失败的目标回归用例；
- 文案/样式问题：稳定复现步骤、前后截图或视觉检查；
- 类型检查/构建或仓内等价自检；
- 目标页面或接口证据；
- 自动生成的 `report.md`。

不启用：

- 长任务 registry；
- 大规模提交考古；
- 多轮净室评审；
- 全量覆盖率门槛。

### M：跨组件或业务状态

典型场景：多个组件、Tab、接口联动、表单写路径、状态切换。

在 S 基础上增加：

- 调用方、相邻 Tab、默认/空数据/全量语义；
- 写路径 payload 和持久化结果；
- 接口失败态和错误提示；
- 新上下文或子 Agent 净室评审；
- 提测后 dev 环境真实复测。

### L：跨仓、数据、权限或发布风险

典型场景：多仓契约、数据库结构、权限、并发、任务流水线、发布配置。

在 M 基础上增加：

- 接入 `task-registry.yaml` / task MCP / worktree；
- 明确契约、迁移和回滚方案；
- 架构或数据影响评审；
- 必要时按 `长任务执行规约.md` 段 E 处理。

## 8. 内部状态校验器

P0 必须提供一个内部校验脚本，建议路径：

```text
gkx-orchestration/scripts/bugflow-state.mjs
```

该脚本由 `feishu-bugfix` 自动调用，普通同事不直接使用。最小职责：

- `init`：创建运行目录和初始 `state.json`；
- `advance`：校验前置产物和口令后推进状态；
- `check`：检查当前状态、证据、commit SHA 和文件有效性；
- `render-report`：根据 `state.json` 和证据自动生成 `report.md`；
- `block`：写入阻塞原因、责任人和恢复条件。

状态推进不能只靠模型在聊天中说“已完成”。以下任一情况必须拒绝推进：

- 前置阶段产物不存在；
- 所需人工口令未记录；
- 验证对应的 commit SHA 不存在或已变化；
- 关键证据缺失；
- 当前状态不允许目标转换。

文件哈希由脚本自动计算，不作为人工检查项。P0 至少把验证证据绑定到当前 commit SHA。

## 9. 运行账本结构

### S 级

```text
<auto_number>-<work_item_id>/
  state.json
  report.md
  evidence/
```

### M 级

沿用 S 级结构；`report.md` 自动增加影响范围、回归矩阵、评审和提测章节。

### L 级

在 M 级基础上按需增加：

```text
  plan.md
  review-report.md
```

只有在 L 级或评审确有必要时，才生成独立计划和评审文件。普通 Bug 不要求填写多份模板。

## 10. `state.json` 字段

P0 使用 `state.json` 作为机器可读真源。字段如下：

| 字段 | 说明 |
|---|---|
| `schema_version` | 账本结构版本 |
| `work_item` | 飞书编号、内部 ID、标题、项目 key、负责人 |
| `claim_id` | 本次 agent claim 的唯一标识，自动生成 |
| `session_id` | 当前执行会话标识，自动生成 |
| `phase` | 内部状态机阶段 |
| `external_status` | 面向用户的状态 |
| `risk` | `S` / `M` / `L`、定级理由和是否由人覆盖 |
| `repo` | 仓库、基线分支、基线 SHA、fix 分支、worktree |
| `data_policy` | 环境、Mock 策略、允许写入范围、策略版本 |
| `gates.enter_dev` | `pending/approved/rejected`、原文、时间、会话 |
| `gates.ship` | `pending/approved/rejected`、原文、时间、会话 |
| `validation_environment` | `local` / `test` / `dev`，记录每条关键证据的环境 |
| `deploy_target` | P0 默认 `dev`；生产必须为空或独立流程处理 |
| `artifacts` | 产物路径、类型、对应 commit SHA、自动哈希 |
| `evidence` | 测试、页面、API、日志、DB、Pipeline 证据 |
| `decisions` | AI 在人工门之间做出的自主决策和理由 |
| `patch_round` | 当前修补轮次及上限 |
| `blockers` | 阻塞原因、责任人和恢复条件 |
| `next_action` | 唯一下一步及执行者 |
| `updated_at` | 最后更新时间 |

最小示例：

```json
{
  "schema_version": 1,
  "work_item": {
    "auto_number": "2238",
    "work_item_id": "7164230616",
    "title": "专题系统-页签没有内容"
  },
  "claim_id": "auto-generated",
  "session_id": "auto-generated",
  "phase": "READY_SHIP",
  "external_status": "待提测",
  "risk": {
    "level": "M",
    "reason": "涉及多个 Tab、查询接口和 CMS 写路径"
  },
  "gates": {
    "enter_dev": { "status": "approved", "token": "【进入开发】" },
    "ship": { "status": "pending", "token": null }
  },
  "deploy_target": "dev",
  "next_action": {
    "owner": "human",
    "action": "审阅提测包并发送【提测】"
  }
}
```

认领主锁仍是飞书 `IN PROGRESS` 和 `[agent-claim]` 评论；`claim_id/session_id` 只用于本地审计和冲突排查。P0 不引入 lease TTL 和心跳，避免过度设计；自动轮询阶段再增加。

## 11. 数据与 Mock 策略

数据策略采用集中配置，不由每个缺陷手工填写。

当前策略版本：

```json
{
  "mode": "demo",
  "mock_allowed": true,
  "allowed_write_scopes": ["明显 Demo 命名的库和表", "当前用于 Demo 的 CMS 业务库"],
  "forbidden_actions": ["write_prod", "alter_prod_schema"],
  "policy_source": "user_explicit",
  "policy_version": "demo-2026-11-10"
}
```

规则：

- 当前 CMS 可作为 Demo 使用，允许 Mock。
- `ods/dwd/ads` 写入明显 Demo 命名的库时允许 Mock。
- 涉及已有业务库结构或数据写入时，必须在诊断阶段写明目标和影响。
- 用户通知上线后，集中切换策略版本并禁止向已有业务库写 Mock；不得依赖历史会话记忆。
- 环境或写入范围不明确时，进入 `BLOCKED`，不得试写。

## 12. 报告与验证

### 人工只读一份 `report.md`

`report.md` 由脚本自动生成，至少包含：

1. 缺陷事实和复现；
2. 根因、需规依据和影响范围；
3. 改动摘要；
4. 验证矩阵和实际结果；
5. 已知风险；
6. 提测信息；
7. 人工验收步骤。

M/L 的评审信息作为章节写入同一份报告；只有在 L 级或评审复杂度确实较高时，才拆出独立文件。

### 验证矩阵

每个缺陷至少回答三类问题：

1. **修复行为**：原问题是否在真实入口消失？
2. **不破坏行为**：相邻 Tab、默认条件、全量语义、写路径是否正常？
3. **边界行为**：空数据、接口失败、无权限、重复提交等是否可解释？

证据环境按阶段区分：

- 提测前：本地、测试环境或独立分支环境；
- 提测后：K8s dev 已部署环境；
- P0 不将生产环境作为自动部署或验收目标。

证据要求：

- 命令必须记录完整命令和结果，不只写“通过”。
- UI 证据记录路由、环境、视口、数据和前后截图。
- API 证据记录请求、响应状态和关键字段；不得记录 token/cookie。
- 数据库证据只记录脱敏查询与结果摘要。
- 模拟结果必须标记 `SIMULATED`，不得伪装成真实环境证据。
- 未执行项必须标记 `SKIPPED` 并给理由，不得写成 `PASS`。

## 13. 语义权威顺序

遇到信息冲突时，按以下顺序判断：

1. 平台/仓库硬规则；
2. 当前会话中的明确人工决策；
3. 最新验收口径和正式需规；
4. 已批准方案；
5. 代码与运行证据；
6. 旧缺陷描述；
7. AI 推断。

截图证明现象，不自动证明根因。若最新人工意见与正式需规冲突，进入 `BLOCKED` 并要求明确取舍。

## 14. 自动决策账本与修补上限

两个人工门之间的自主决策写入 `state.json.decisions`，至少包含：

- 决策；
- 依据；
- 被否决的替代方案；
- 影响范围；
- 是否需要提测时追认。

所有等级默认最多 3 轮修补。达到上限仍无法通过验证时自动进入 `BLOCKED`，报告已尝试内容、证据和所需决策，不继续盲目试错。该限制对用户只显示为“已受阻”，不暴露内部轮次细节。

## 15. 与主仓流程的接入边界

- **S 级**：使用运行账本和独立 fix 分支，不写 task-registry。
- **M 级**：默认使用运行账本；需要跨会话协调时接 task MCP。
- **L 级**：必须接 task registry、worktree 和对应架构/数据门。
- 只有进入长任务段 E 或跨仓交付时，才套用 C1–C6、trace-id 和段 E 缺陷包要求。
- `【进入开发】` 可授权推送独立 fix 分支/Draft MR，但不能合并或部署。
- `【提测】` 授权合并和 dev 部署；P0 不授权生产部署。

## 16. P0 试点与验收指标

先对接下来 5 个真实飞书缺陷试点，观察：

- 人工发现的新增问题数量；
- 首次提测后的返工轮次；
- 是否稳定为两个决策口令加一次验收；
- 是否发生错仓修改、越权推送、越范围 Mock 或生产写入；
- 提测包是否足以让人不读代码也能验收；
- S/M/L 分级是否准确，是否出现流程过重或漏检；
- 同事是否能在不了解内部状态机的情况下完成操作。

P0 通过条件建议：

- 5 个缺陷均有有效 `state.json` 和自动生成的 `report.md`；
- 0 次未授权 merge/deploy；
- 0 次生产或错误库写入；
- 简单缺陷平均返工不超过 1 轮；
- 人工验收时可以仅依据提测包和页面完成判断；
- 普通同事无需手工填写任何阶段模板。

## 17. 后续实施顺序

1. 评审本修订稿。
2. 创建 `_templates/state.schema.json` 和统一的 `report.md` 模板。
3. 实现内部 `bugflow-state.mjs` 最小校验器。
4. 为 `bugfix-runs/` 增加安全的 `.gitignore` 规则。
5. 重构 `feishu-bugfix` 控制语义，并补充前端推送规则中的两个口令映射。
6. 用真实新缺陷试跑，不回溯修改已关闭缺陷【2238】。
7. 根据 5 个试点的数据决定是否进入 P1 和自动触发。

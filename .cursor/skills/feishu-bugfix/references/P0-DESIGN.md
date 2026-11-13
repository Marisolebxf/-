# 飞书缺陷 AI Native P0 设计稿

> 状态：v1.2 精确验收口令优化版（保留 gate/证据约束，增加类型路由、预检、时间盒和分级验证）
> 版本：v1.2
> 日期：2026-11-11
> 基线案例：飞书缺陷【2238】
> 设计原则：对外保留三个精确口令，内部校验严格但由 Agent 自动执行
> 技术路线：复用现有 Codex / Cursor / Trae + Skill + 轻量校验脚本，不自研 Agent Runtime
> 真源分层：本文件是流程与权限真源；`.cursor/skills/feishu-bugfix/SKILL.md` 是操作真源；`templates/state.schema.json` 是机器结构真源；`policies/` 是数据授权真源

## 0. v1.0 执行补充

本节是运行入口的补充规则，不改变下文 gate、claim、数据和验收约束。

1. 每个缺陷先形成 **Bug Contract**：现象、期望、范围、非目标、主仓依据和验证方式；期望无法定位到主仓文档/测试/最新人工裁定时不得进入开发。
2. 先按缺陷类型路由，再选择验证工具。类型路由和验证模板见 `BUG-PLAYBOOK.md`，不再统一套用前端流程。
3. 开工前做基线预检，并区分“本地开发门”和“提测门”：最新目标分支 pipeline 为红时，若失败与当前缺陷路径不相交且不影响目标本地复现/验证，可继续本地开发和定向验证，但保留 owner/URL 为未关闭的 ship blocker，不增加补丁轮次；若会阻断目标本地路径或必需全量验证，则暂停开发。任何情况下 `READY_SHIP`/`提测` 前都必须有成功的目标分支流水线。
4. S 级验证至少覆盖 `fix + regression`；M/L 追加至少一个适用非 happy-path 类别。允许类别为 `boundary/integration/data/algorithm/security/performance/rollback`。
5. 同一缺陷、同一范围和风险的验收返工保留 claim 与既有诊断，只重做候选 diff、评审和验证，并重新请求 `提测`；只有范围/风险变化才重新请求 `进入开发`。
6. 增加时间盒：S 目标 30–60 分钟、M 目标 1–2 小时；同一环境故障连续两次无进展即 block。
7. 同一个 Bug 涉及多个仓库时不拆单：保持一个 run/claim/gate，使用 `role/depends_on/ship_order` 组成跨仓 Bundle；风险至少 M，并强制完整 Bundle 的 integration 验证。
7. 并发 push 后使用 `scripts/revalidation-plan.mjs` 做复验分级：远端基线绿、无冲突且与候选文件不重叠时只做目标复验并交给 CI 全量验证；重叠或触及共享配置/types/API/依赖时重新执行完整本地验证。
8. 需规功能点覆盖是 `进入开发` 前置条件：`diagnosis.requirement_refs` 至少包含一个 SRS 文件 + 序号/五级功能路径，并在验证矩阵中覆盖该功能点的可观察行为；截图不能替代需规映射。

## 1. 已确认决策

1. 使用三个精确人工门：`进入开发`、`提测`、`验收通过`。
2. 缺陷按 S/M/L 分级，简单缺陷保持轻流程。
3. 运行账本放在：

```text
agent-delivery/bugfix-runs/<auto_number>-<work_item_id>/
```

4. `state.json`、`report.md` 和 `evidence/manifest.json` 入库；原始截图、日志、临时输出默认不入库。
5. `提测`的含义是：合入 `dev`、触发 CI、自动部署 dev 并完成 dev 复测；不授权生产部署。
6. 最终验收使用第三个精确口令 `验收通过`。只有完整精确消息（多 active run 时 `验收通过<auto_number>`）才能批准 `acceptance` gate；Agent 随后读取飞书可流转状态/必填项，调用 `transition_state` 迁移 `RESOLVED`，再记录 `acceptance.mode=chat_exact` 和 `operator_verified=false`。“可以”“继续”“算修复了”“看起来没问题”均不解锁。人工直接完成飞书迁移时仍保留 `policy_only` 观察路径。
7. 自然语言不得解锁开发、提测或验收 gate。仅“接管【编号】”可触发明确的人工接管流程，且接管不等于解锁 gate。
8. Gate 不在飞书逐条写评论。P0 只保留三个外部锚点：认领时的 `[agent-claim]` 评论、提测时的脱敏总结评论、最终验收总结评论；其余 gate 由 `state.json` 和校验器负责。
9. `state.json` 是状态与索引真源，`evidence/manifest.json` 是证据明细真源，`report.md` 由二者渲染；三者放在 `gkx-orchestration` 仓库并随关键节点提交。一个 run 固定一台执行机，跨机器恢复时必须重新校验 claim、仓库、candidate/deployed SHA、证据和 gate，缺证据则重新取证。
10. 当前 `demo` 阶段允许按不可变版本化白名单 Mock 写入 `demo_gkxlumenx_ods/dwd/ads/dim` 及当前作为 Demo 使用的 `gkxlumenx_cms` 指定表。该授权属于有记录、可复核的限时项目例外，不宣称“不修改 D16/D18”；与架构硬规则冲突时进入 `BLOCKED`，除非已有明确批准记录。上线通知到达后切换 production policy，默认禁止制造或写入 Mock 数据。

## 2. 使用体验

普通同事只需要完成四件事：

1. 发起处理或确认目标缺陷；
2. 审阅诊断与改动边界，发送 `进入开发`；
3. 审阅提测包，发送 `提测`；
4. 在 dev 完成业务验收，发送精确 `验收通过`，由 Agent 完成飞书状态迁移。

以下内容全部由 Agent、Skill 和校验器自动完成：

- 状态机推进和 gate 校验；
- 风险分级建议；
- 数据/Mock 策略读取；
- 证据索引、文件哈希和报告渲染；
- 评审、验证和回滚材料生成；
- 飞书评论草稿和最终摘要；
- 下一步提示。

普通同事不维护 JSON、不填写阶段模板、不手工判断内部状态。

## 3. 对外状态

主状态：

```text
待认领
  → 已认领
  → 待进入开发
  → 修复中
  → 待提测
  → 待验收
  → 完成
```

旁路状态：

- `返工中`：验收失败、REOPEN、dev 复测失败或修复引入新问题。
- `受阻`：缺少复现、需求、权限、环境、测试能力或策略授权。
- `已取消`：缺陷关闭、重复或确认无需修复。

`返工中`不是`受阻`。返工意味着问题已经定位到修复范围，需要重新诊断或修改；受阻意味着当前无法继续推进。

对外状态由 `phase` 自动派生，不单独作为真源保存；同一个 `phase` 不得出现两个不同的对外状态。

## 4. 内部状态机

主链：

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
  → DEV_VERIFYING
  → AWAITING_ACCEPTANCE
  → RESOLVED
```

旁路：

```text
BLOCKED
REOPENED
DEV_VERIFY_FAILED
ROLLED_BACK
CANCELLED
```

转换约束：

- `init` 只能创建 `INTAKE` 或 `CLAIMED`，其余阶段必须由 `advance` 产生；首次 `进入开发` 只能在 `READY_DEV` 批准，`IMPLEMENTING` 只用于已批准 gate 失效后的重新确认。
- `REOPENED → DIAGNOSED`：必须重新确认根因、影响范围和需规依据，不能直接回到实现或提测。
- `DEV_VERIFY_FAILED → ROLLED_BACK`：只回退本次 run 的候选提交；无法安全回退时进入 `BLOCKED`。
- `ROLLED_BACK → REOPENED`：生成回退证据后等待重新诊断。
- `BLOCKED` 恢复后回到 `blocked_from` 指向的合法状态；必须保留 `resume_phase`、阻塞原因和恢复条件。
- `RESOLVED → REOPENED`：复用同一 run，新增 `cycle_id` 并保留上一轮诊断、gate、提测和验收历史；不新建无关联 run。
- `任意未完成状态 → CANCELLED`：仅在缺陷被关闭、确认重复或确认无需修复时进入；记录取消人、原因、已推分支/MR/dev 部署的清理结果。
- `任意未完成状态 → BLOCKED`：缺复现、需规、权限、环境、验收证据、数据授权或出现不可安全处理的失败时进入；必须记录 `blocked_from`、`resume_phase`、`resume_condition` 和 owner。
- `BLOCKED → resume_phase`：只能通过 `resume` 命令恢复；必须提供 session/machine、恢复证据，记录 `blockers[].resolved_at/resolved_by/resume_evidence_refs`，并重新校验 claim、repo、SHA、data scope 和 gate。恢复路径上的 approved gate 若因上下文或绑定变化失效，必须重新取得精确口令，不能自动放行。
- `DEV_VERIFY_FAILED → BLOCKED`：无法安全 revert 或失败原因暂时不可归因时进入。
- `ROLLED_BACK → BLOCKED`：回退后仍无法重建诊断或环境时进入。
- `CANCELLED` 不自动回退已部署 dev；若取消前已经部署，必须按本文件定义的单次 revert 流程处置或进入 `BLOCKED`。
- `CANCELLED → REOPENED`：仅在错误取消、重复判断被撤销或缺陷重新有效时开启新 cycle，原取消记录必须保留。

### 对外状态映射

| 对外状态 | 内部状态 |
|---|---|
| 待认领 | `INTAKE` |
| 已认领 | `CLAIMED` |
| 待进入开发 | `DIAGNOSED` / `READY_DEV` |
| 修复中 | `IMPLEMENTING` / `REVIEWING` / `VERIFYING` |
| 待提测 | `READY_SHIP` |
| 待验收 | `SHIPPING` / `DEV_VERIFYING` / `AWAITING_ACCEPTANCE` |
| 返工中 | `REOPENED` / `DEV_VERIFY_FAILED` / `ROLLED_BACK` |
| 受阻 | `BLOCKED` |
| 已取消 | `CANCELLED` |
| 完成 | `RESOLVED` |

## 5. 状态转换门槛

| 转换 | 前置条件 |
|---|---|
| `INTAKE → CLAIMED` | 找到当前用户名下缺陷；完成 `IN PROGRESS` 认领和 `[agent-claim]` 评论；生成 `claim_id`，并记录 `claim_comment_ref`、`claim_operator`、`claimed_at` |
| `CLAIMED → DIAGNOSED` | 截图/复现、根因假设、反证、需规证据、影响范围和 data policy 已落盘 |
| `DIAGNOSED → READY_DEV` | 根因可证伪；改动边界、验证计划和风险等级明确 |
| `READY_DEV → IMPLEMENTING` | `gates.enter_dev` 有效，且绑定对象与当前 claim/repos/base/diagnosis 一致 |
| `IMPLEMENTING → REVIEWING` | 最小改动完成；无关改动排除；自检命令已结构化记录 |
| `REVIEWING → VERIFYING` | S 级完成自审；M/L 完成对应独立评审，不允许跳过 |
| `VERIFYING → READY_SHIP` | 回归矩阵、工程检查、提测前证据和残留风险完整 |
| `READY_SHIP → SHIPPING` | `gates.ship` 有效，且绑定到当前 candidate commit、diff 和验证结果 |
| `SHIPPING → DEV_VERIFYING` | 合并、push、Pipeline 和 dev rollout 成功，且 `deployed_sha`/镜像 tag 已记录 |
| `SHIPPING → BLOCKED` | merge 冲突、MR 被拒或 push 失败，dev 尚未发生变化；记录 `failure_stage`，修复后可回到 `READY_SHIP` |
| `SHIPPING → DEV_VERIFY_FAILED` | 已进入 dev 部署链后 Pipeline、rollout 或 dev 复测失败；记录 `failure_stage` 并进入回退判定 |
| `DEV_VERIFYING → AWAITING_ACCEPTANCE` | dev 真实页面/API 复测通过，验收步骤已生成 |
| `DEV_VERIFYING → DEV_VERIFY_FAILED` | dev 真实复测失败或修复引入新问题 |
| `AWAITING_ACCEPTANCE → REOPENED` | 飞书验收失败或人工把状态迁移为 `REOPENED` |
| `DEV_VERIFY_FAILED → REOPENED` | dev 复测确认是修复问题，完成回退后重新诊断 |
| `AWAITING_ACCEPTANCE → RESOLVED` | 收到完整精确 `验收通过` 后批准 `gates.acceptance`；满足飞书必填项并成功执行 `transition_state`。人工自行迁移时走 `policy_only` 观察路径。`operator_verified=false` |
| `RESOLVED → REOPENED` | 缺陷再次复现或验收被撤销；复用同一 run，开启新 `cycle_id` 并重建 gate |
| `任意未完成状态 → BLOCKED` | 不可继续但尚未取消；写入 `blocked_from/resume_phase/resume_condition/blocker_owner` |
| `BLOCKED → resume_phase` | 阻塞条件已解除，claim、repo/SHA、data scope 和 gate 重新校验通过 |
| `DEV_VERIFY_FAILED / ROLLED_BACK → BLOCKED` | 回退不安全、冲突或原因不可归因 |
| `任意未完成状态 → CANCELLED` | 缺陷关闭、重复或确认无需修复；记录取消人、原因和清理结果 |
| `CANCELLED → REOPENED` | 错误取消或缺陷重新有效；开启新 cycle，不覆盖原记录 |

## 6. 三个口令和验收落点

### 6.1 口令来源

P0 以**当前会话中的精确聊天消息**作为三个 gate 的授权来源。`state.json` 记录：

```json
{
  "source": "chat",
  "token_text": "进入开发",
  "approved_by": "current_user",
  "approved_at": "ISO-8601",
  "claim_id": "claim-...",
  "message_ref": "当前会话内的消息标识；客户端不提供时记录脱敏摘要",
  "gate_hash": "sha256:...",
  "bound_to": {}
}
```

有效口令必须满足以下形式之一：

- 整条消息只有 `进入开发`、`提测` 或 `验收通过`，前提是当前会话只有一个 active run；
- `进入开发<auto_number>` / `提测<auto_number>` / `验收通过<auto_number>`，用于区分多个 active run。

口令必须绑定当前 `work_item_id` 和 `claim_id`。历史会话、其他任务、飞书旧评论、引用口令的问答、否定句和自然语言同意均不能替代。同一会话存在多个 active run 时，未带编号的口令一律不生效。

授权只对当前 gate 的对象有效，不是对后续所有改动的永久授权。校验器在 `advance` 前重新计算 `gate_hash` 和 `bound_to`；不一致时 gate 一律视为 `invalidated`。

同一 `claim_id` 在同一执行机、同一会话内可以连续推进，不重复要口令。若换会话或换机器，旧 gate 标记为 `needs_reconfirm`；只有重新展示当前绑定对象并由用户再次发送对应精确口令后才能继续。这样既支持恢复，也禁止从历史 `state.json` 继承旧授权。

### 6.2 `进入开发`

请求口令前必须已经展示：

- 可读缺陷编号和内部 ID；
- 期望行为与实际行为；
- 截图或复现步骤；
- 根因或可证伪的根因假设；
- 需规/验收标准及原文位置；
- 仓库、调用链、基线 SHA 和影响范围；
- S/M/L 风险等级；
- data policy 和允许写入范围；
- 初步验证与回滚计划。

口令有效时允许：

- 修改业务代码；
- 创建本地 commit；
- 推送独立 `fix/*` 分支；
- 创建 Draft MR；
- 运行仓内自检、本地验证和可用的分支检查。

仍然禁止：

- 合并 `dev` / `main`；
- 部署 dev 或生产；
- 修改生产配置；
- 把飞书缺陷置为 `RESOLVED`。

### 6.3 `提测`

请求口令前必须已经展示：

- candidate commit、base commit、diff 和 Compare/MR；
- 改动文件及每处理由；
- 验证矩阵和实际结果；
- 提测前仓内自检/本地验证状态；若该分支没有远端 CI，必须明确说明，不能伪造“分支 CI 已通过”；
- 页面、API、日志或数据库证据摘要；
- 已知限制、回退版本和回滚方式；
- dev 部署后的验收步骤。

口令有效时允许：

- 合并集成分支；
- push `dev`；
- 触发 dev 分支的 CI/CD（若仓库存在）；
- 自动部署 dev；
- 在 dev 环境进行真实复测；
- 更新飞书提测评论。

GitLab 保护分支、MR approve 和仓库发布规则优先；`提测`不绕过保护规则，若仍需人工 approve，该人工操作和结果必须记录在 `ship_package`。P0 不授权生产部署，生产发布继续走独立人工发布流程。

`提测`不是“只生成提测包”，而是明确授权下面这一整条共享 dev 发布链：

```text
合并候选提交 → push dev → Pipeline → dev rollout → dev 真实复测
```

因此用户在看到 `提测` 请求时必须被告知：本次操作会影响共享 dev 环境。Pipeline、rollout 或 dev 复测失败时：

1. merge 冲突、MR 被拒或 push 失败：dev 尚未变化，进入 `BLOCKED` 或回到 `READY_SHIP`，记录 `failure_stage`，不走回退流程；
2. 已进入部署链但 Pipeline/rollout 失败：进入 `DEV_VERIFY_FAILED`，检查是否已经产生 dev 变更；未产生则修复后重跑，已产生则只 revert 本次 run 的提交；
3. dev 复测失败：进入 `DEV_VERIFY_FAILED`，先按缺陷流程的 `failure_class` 分类；C1–C6 只作为映射参考，确认是本次修复问题后再回退；
4. 回退只允许 `git revert`，禁止 `git reset`、force push 和回退他人提交；merge commit 使用 `git revert -m 1`；
5. 记录回退 commit、Pipeline、回退后的健康检查和证据；旧 `ship` gate 自动失效，重新修复后必须重新发送 `提测`；
6. 无法安全回退时进入 `BLOCKED`，等待人工处置。

流水线等待采用“候选提交首次终端成功”语义，而不是“跟踪最新 dev 流水线直到全部结束”：

- 只跟踪 commit 包含当前 candidate 的 Pipeline；用 `git merge-base --is-ancestor <candidate_sha> <pipeline_sha>` 校验包含关系；
- 某 Pipeline `success` 且 deploy/rollout `success`，或当前 live deployed SHA 已包含 candidate，即构成该仓库的终端成功，停止等待；
- 本 run 的首个 Pipeline 被取消/覆盖时，继续等待下一个包含 candidate 的 Pipeline，首个终端成功即可结束；
- 在已取得终端成功后，同事随后触发的新 Pipeline 无论 running、failed 还是 deploy skipped，都属于后续 dev 活动，不得让当前 run 无限等待；记录观测事实，并继续以当前包含 candidate 的 live deployed SHA 做 dev 验证；
- 只有“尚未出现任何 candidate-containing 终端成功”时，Pipeline/rollout 失败才进入本 run 的 `DEV_VERIFY_FAILED` 或 `BLOCKED`；
- 多仓 Bundle 每个仓库独立取得至少一个终端成功，不要求所有仓库复用同一条 Pipeline 序列。

`ship_package.pipeline_id/pipeline_status/pipeline_url/deployed_sha` 记录该仓库的终端成功实例；后续无关 Pipeline 只能写入观测摘要，不能覆盖终端成功事实或让 run 持续等待。

### 6.4 验收

`AWAITING_ACCEPTANCE` 只接受完整精确消息 `验收通过`。多 active run 时必须使用 `验收通过<auto_number>` 或 `验收通过 <auto_number>`。自然语言同意、否定句、引用口令的问答和其他会话中的授权都不能替代。

收到精确口令后，Agent 必须依次完成：

1. 调用 `get_transitable_states`，确认飞书当前存在合法的 `RESOLVED` 迁移；
2. 调用 `get_transition_required`，先补齐必填字段；
3. 构造 `acceptance` gate 绑定：`work_item_id`、`claim_id`、`ship_gate_hash`、`dev_verification_result`、已验证 evidence manifest hash、当前飞书状态；
4. 发布验收摘要评论，说明修复、验证、部署、已知限制和本次实际迁移；
5. 调用 `transition_state` 将飞书迁移为 `RESOLVED`；
6. 调用 `record-acceptance`，写入 `mode=chat_exact`、`approval_message=验收通过`、审批引用、gate hash、session/machine、transition 结果和证据；
7. 推进内部阶段到 `RESOLVED`。

任一步失败时不得伪造验收：

- 无合法迁移或必填项不可满足：保持 `AWAITING_ACCEPTANCE`，报告阻塞；
- 飞书迁移成功但账本或证据写入失败：记录 `failure_stage=acceptance` 与阻塞，按既有 transition 结果补齐证据，不能再次迁移；
- 人工直接完成飞书迁移而不发送精确口令：保留 `policy_only` 路径，Agent 只读取并记录，不构造 `chat_exact` gate；
- 在 `DEV_VERIFYING` 或更早阶段看到 `RESOLVED`：记录 `acceptance.anomaly=early_resolved` 并进入 `BLOCKED`；
- 任意未完成阶段看到 `REOPENED`：使旧 gate 失效并进入 `REOPENED`，重新诊断。
- acceptance gate 一旦以 `chat_exact` 批准，禁止在原 run 内降级为 `policy_only`；否则会绕过第三个精确口令。

由于飞书 MCP 仍使用当前用户身份，`chat_exact` 证明的是“当前会话收到了精确人工授权”，不是密码学防伪。账本必须记录 `operator_verified=false`。P0 不启动后台轮询；没有精确口令或人工状态迁移时，`state.json` 保持 `AWAITING_ACCEPTANCE`。

推荐记录结构：

```json
{
  "acceptance": {
    "status": "approved",
    "mode": "chat_exact",
    "approval_message": "验收通过",
    "approval_ref": "当前会话消息标识或脱敏摘要",
    "approved_at": "ISO-8601",
    "approval_session_id": "session-...",
    "approval_machine_id": "machine-...",
    "gate_hash": "sha256:...",
    "from_status": "IN PROGRESS",
    "to_status": "RESOLVED",
    "current_status": "RESOLVED",
    "transition_id": "MCP 返回的迁移 ID，可为 null",
    "operator": null,
    "operator_verified": false,
    "observed_at": "ISO-8601",
    "evidence_kind": "chat_exact+feishu_transition",
    "evidence_ref": "evidence/manifest.json#E-ACCEPT-001"
  }
}
```

## 7. Gate 绑定与失效

Gate 不能只记录 `approved`，必须绑定到产生授权时的对象。`bugflow-state.mjs advance` 每次推进前调用 `validate-gate`，重新计算并比较：

1. 当前飞书 `work_item_id` 与 `claim_id`；
2. `repos[]` 中每个仓库的 registry `id`、解析出的 `repo_name/remote`、worktree 和当前 HEAD；
3. 当前工作区是否干净：`git status --porcelain -uall` 必须为空；未跟踪文件也视为脏工作区；
4. 每个仓库的 diff 与 `diff_hash`；
5. 每个仓库的验证证据与 `verification_hash`；
6. 当前风险等级、`data_policy_hash`、`data_scope_hash`，以及 ship 的 `review_hash`；
7. gate 的稳定绑定对象和 `gate_hash`；并交叉核对 `state.repos`、`state.review.repos`、`risk.level`、`data_policy.policy_hash` 和 `data_policy.scope_hash`，不能只验证 gate 内部自洽。

任一项不一致都不得推进。校验结果写入 `gates.<name>.validation`，包含 `checked_at`、`validator_version`、`result`、`actual`、`expected`，不能只在报告里口头说明“已校验”。

### 7.0 稳定哈希投影

同一份代码在不同机器、不同时间重跑时，不能因为审计元数据变化而误判 gate 失效。哈希使用以下稳定投影：

- `gate_hash` 只包含：授权来源、精确口令文本、`approved_by`、`approved_session_id`、`approved_machine_id`、`claim_id`、gate 名称、稳定 `bound_to` 对象和校验器版本；
- `bound_to` 不包含 `worktree` 绝对路径、`session_id`、`message_ref`、`approved_at` 和运行时临时目录；
- `verification_hash` 按 repo 只包含该仓验证矩阵的：`id`、`category`、`behavior`、`result`、`evidence_refs`、`simulated`、`skipped_reason`；
- `verification_hash` 不包含：`timestamp`、`cwd`、`stdout_path`、`producer`、`raw_retained`、`reviewable` 等审计元数据；manifest 文件本身的 `manifest_hash` 单独记录；
- `diff_hash` 固定为每个仓库 `base_sha..candidate_sha`，包含文件路径、增删行和模式变化；
- JSON 使用键排序、UTF-8、LF 和固定浮点格式；YAML 先解析为规范对象，再按 JSON canonical 形式计算；
- evidence 按稳定 `evidence_id` 排序；所有聚合 hash 必须写明投影版本，例如 `projection_version: p0-v3`。

审计字段仍可保留，但只用于解释和人工复核，不能改变 gate 的稳定身份。

### 7.1 `enter_dev` 绑定

`enter_dev` 是开发前授权，candidate 尚不存在。`bound_to.repos[]` 每个仓库记录：

- `repo_id`：来自 `agent-delivery/repo-registry.yaml` 的 `repos[].id`；
- `repo_name` / `remote`：由 registry 的当前环境解析并校验；
- `base_branch` / `base_sha`；
- `candidate_sha: null`；
- `planned_change_scope`；
- 多仓 Bundle 还必须记录 `role`、`depends_on`、`ship_order`；单仓允许为空；
- `worktree` 只作为本机执行信息，不进入 gate hash。

顶层另记录 `diagnosis_hash`、`risk_level`、`data_policy_version`、`data_policy_hash`、`data_scope_hash`。

以下任一变化使 `enter_dev` 失效：

- claim 被人工接管；
- 目标仓库、基线或改动边界变化；
- 风险升级；
- data policy 或 run scope 表清单变化；
- 诊断结论发生实质变化；
- 缺陷被 REOPEN。

### 7.2 `ship` 绑定

`ship` 绑定提测前每个仓库的 fix candidate，而不是 dev 分支的全局 HEAD；gate 必须在合并/部署前批准，`merge_commit_sha`、`deployed_sha`、pipeline 和 rollout 是授权后由 `record-ship-package` 记录的事实。`bound_to.repos[]` 每个仓库记录：

- `repo_id` / `repo_name`；
- `base_sha` / `candidate_sha`；
- `diff_hash`；
- `verification_hash`；
- `review_hash`；
- `data_policy_hash` / `data_scope_hash`；
- 多仓 Bundle 的 `role` / `depends_on` / `ship_order`。

顶层另记录 `risk_level` 和 `deploy_target=dev`。`ship_package`、`review` 和 `rollback` 按 `repos[]` 记录，单仓也必须显式绑定。

同一个飞书缺陷涉及多个仓库时，仍是一个 run、一个 claim 和同一组 gate；不得拆成多个飞书缺陷。多仓 Bundle 还必须满足：

- 风险至少为 M；跨仓本身不自动升级为 L；
- `ship_order` 必须为连续的 `1..N`，且 `depends_on` 只允许指向更早 ship 的仓库；
- 每个仓库分别满足候选 SHA、review、`fix + regression` 和 M 级非 happy-path 要求；
- 至少一条 `integration` 验证的 `repo_ids` 覆盖 Bundle 全部仓库且结果为 PASS/SIMULATED；
- 任一仓库失败时，Bundle 不得进入完成态；回滚按仓记录但使用同一提测结论。

每个 `ship_package.repos[]` 至少包含：

- `repo_id`
- `merge_request_id` / `mr_url`
- `candidate_sha`
- `merge_commit_sha`
- `deployed_sha`
- `pipeline_id` / `pipeline_url` / `job_name`
- `image_tag`
- `rollout_status`
- `dev_verify_result`
- `failure_stage` / `failure_class`

`DEV_VERIFYING` 校验每个仓库 dev 实际 `deployed_sha`、当前运行镜像和 dev 复测证据，不再拿 fix 分支 `HEAD` 冒充 dev 版本。若 GitLab 产生 merge/squash commit，必须记录实际 SHA，不能用 candidate SHA 代替；因此 `deployed_sha` 不要求等于 `candidate_sha`，但 `merge_commit_sha`、`pipeline_url` 和实际部署 SHA 必须可追溯。pipeline/rollout 字段来自 Agent 对 GitLab 的查询记录，报告不得把它们描述成本地脚本直接验证过的远端事实。

以下任一变化使 `ship` 失效：

- 本 run 的 fix 分支 candidate 变化、rebase 或出现新 commit；
- 本 run 的 diff hash、验证结果、评审结论或 `review_hash` 变化；
- 风险升级或 data policy/run scope 变化；
- claim 被接管；
- 缺陷被 REOPEN。

`ship` 不因 dev 上其他人的普通提交而失效；合并后 dev 前进时，保持 ship 记录不变，但 `DEV_VERIFYING` 必须以本 run 的 `merge_commit_sha/deployed_sha/image_tag` 重新核对。

`session_id` 不能替代 claim 和对象绑定；同一会话也不能把旧 gate 复用于新对象。允许恢复执行，但不允许静默继承授权：同一 claim 在同一执行机同一会话内可直接推进；换会话或换机器后，旧 gate 转为 `needs_reconfirm`，必须重新展示绑定对象并让用户再次发送对应精确口令。

### 7.3 `acceptance` 绑定

`acceptance` gate 只在 `AWAITING_ACCEPTANCE` 阶段、收到完整精确消息 `验收通过` 后批准。`bound_to` 记录：

- `work_item_id` 与 `claim_id`；
- 当前已批准 `ship` gate 的 `gate_hash`；
- `dev_verification_result`，必须为 `PASS`；
- 已验证 evidence manifest 的 `manifest_hash`；
- 批准时的飞书 `current_status`。

`acceptance` gate 不绑定代码 candidate，而绑定“当前 claim 的 dev 验收事实”。任一字段变化、claim 接管、dev 证据变化或飞书状态异常时，必须重新校验或失效。

只有 `chat_exact` 模式依赖该 gate。人工直接在飞书完成状态迁移时走 `policy_only` 观察路径，不构造 `gates.acceptance`。

### 7.4 接管

不引入 lease TTL。用户明确发出精确消息 `接管【auto_number】` 后：

1. Agent 校验 work item 当前归属和评论；
2. 生成新 `claim_id`；
3. 发布 `[agent-claim][takeover]` 评论，写明 supersedes 的旧 claim；
4. 旧 gate 全部失效；
5. 从当前合法阶段继续，不重复已完成但未改变结论的诊断步骤。

“接管”只解决执行权，不解锁 `进入开发` 或 `提测`。

没有接管口令时，即使原执行会话已崩溃，也不得猜测“应该已经过期”。Agent 只能报告当前 claim 和接管方式。接管后必须保留旧 claim 的评论、gate 和 commit 记录，不能删除审计链。

## 8. S/M/L 分级

风险分级由 Agent 自动建议，用户不手工选择。定级只能上调，不确定时按 M 处理。

### S：单点低风险

典型场景：文案、样式、单字段展示、明确单点逻辑。

最低要求：

- 相关调用链和测试；
- 业务逻辑：至少一个可失败的目标回归用例；
- UI 文案/样式：优先使用 DOM/API/部署 chunk 等机器断言；确需视觉证据时，保留前后各 1 张目标区域截图，禁止连续全屏截图；
- 类型检查、构建或仓内等价自检；
- 目标页面或接口证据；
- 自动生成的 `report.md`。

评审要求：Agent 自审，不允许跳过测试和证据。

### M：跨组件或业务状态

典型场景：多个组件、Tab、接口联动、表单写路径、状态切换，以及同一个 Bug 的跨仓 Bundle。

在 S 基础上增加：

- 调用方、相邻 Tab、默认/空数据/全量语义；
- 写路径 payload 和持久化结果；
- 接口失败态和错误提示；
- 独立评审：由未参与实现的 Agent/会话执行针对性 review，记录 reviewer、independent、reviewed_sha、scope、findings 和 verdict；
- 提测后 dev 环境真实复测。

M 级不得跳过评审。

### L：数据、权限或发布风险

典型场景：数据库结构、权限、并发、任务流水线、生产发布配置。

`bugflow-state` 只负责识别 L，不在 P0 内复制第二套长任务执行器。一旦升级到 L，立即停止轻量流程并路由到现有：

- 仅经 task MCP 接入 task-registry、worktree，并记录 `task_registry_id`；禁止直接读写 `task-registry.yaml`；
- 契约、迁移和回滚方案；
- 架构或数据影响评审；
- 全量净室评审；
- 必要时按 `长任务执行规约.md` 段 E 处理。

L 级不得跳过评审，也不得通过普通 `进入开发` gate 绕过既有长任务流程。

## 9. 运行账本与证据存储

```text
agent-delivery/bugfix-runs/<auto_number>-<work_item_id>/
  state.json
  report.md
  cycles/
    <cycle_id>/state.json   # 已完成周期的不可变快照
  evidence/
    manifest.json          # current cycle only
    raw/                    # 默认 gitignore
  plan.md                   # L 或确有必要时
  review-report.md          # L 或独立评审需要时
```

入库规则：

- `state.json` 是状态与索引真源，`report.md` 和 `evidence/manifest.json` 是证据与展示真源，必须入库；
- `state.json` 只表示当前 cycle；进入新 cycle 前，把上一轮完整快照写入 `cycles/<cycle_id>/state.json`，不得覆盖历史；
- `REOPENED` 时同时把当前 manifest 归档到 `cycles/<cycle_id>/evidence/manifest.json` 并重建空 manifest，避免旧 DB 证据被新 cycle 的 policy/scope 误校验；
- 数据策略使用不可变版本文件 `policies/<version>.yaml`；run 只保存 `policy_version`、`policy_hash` 和策略快照 hash，不能依赖随时会被覆盖的全局文件；
- `evidence/raw/` 保存截图、stdout、API 响应和临时日志，默认不入库；
- manifest 记录证据相对路径、SHA256、kind、环境、采集时间和对应 commit；DB 证据额外记录写授权和 policy/scope hash；
- 飞书中只写脱敏摘要和稳定路径，不暴露 token、cookie、签名下载 URL 或敏感数据；
- 一个 run 固定一台执行机。切换机器时，没有 raw evidence 的项目必须标为 `SKIPPED` 或重新取证，不能假定通过；gate 必须重新确认。

`state.json` 至少在 claim、进入开发、提测、失败/回退、验收五个节点提交一次到 `gkx-orchestration` 仓库。每次 `advance` 的校验结果写入当前 cycle 的 `transitions[]`，不要求每个内部微状态都生成独立仓库 commit。RESOLVED→REOPENED 或 CANCELLED→REOPENED 时先归档当前 cycle，再递增 `cycle_seq`；旧 cycle 的 diagnosis、gates、ship_package、acceptance 和 patch_round 不得被新 cycle 覆盖。若当前分支不允许 push，至少完成本地 commit，并把脱敏摘要写入飞书评论或用户指定 handoff；不得长期停留在 `??` 状态。P0 不建设中央数据库，避免为了“集中状态”先引入一套自研服务。

## 10. `state.json` 固定字段

`state.json` 是当前 cycle 的状态与索引真源；历史 cycle 的完整内容保存在 `cycles/<cycle_id>/state.json`，至少包含：

| 字段 | 说明 |
|---|---|
| `schema_version` | 账本结构版本 |
| `run_id` | `<auto_number>-<work_item_id>`；唯一性主要由 `work_item_id` 保证 |
| `current_cycle_id` / `cycle_seq` | 当前周期指针和单调递增序号 |
| `cycles` | 历史周期索引：`cycle_id`、`seq`、起止时间、`state_ref`、关闭原因 |
| `work_item` | 飞书项目 key、auto_number、内部 ID、标题、负责人、`qa_bug_id`、`task_registry_id` |
| `ownership` | `claim_id`、`claim_comment_ref`、`claim_operator`、`claimed_at`、`session_id`、`machine_id`、当前 owner、接管历史 |
| `phase` | 内部阶段；对外状态由 `phase` 派生，不单独存储 |
| `risk` | S/M/L、理由、是否上调 |
| `repos` | 仓库权威数组：`repo_id`、registry 解析出的 `repo_name/remote`、base/candidate SHA、fix 分支和改动边界；多仓时还包含 `role/depends_on/ship_order`；不存放绝对 worktree 路径 |
| `machine_local` | 指向本机非权威映射文件，例如 `local/<run_id>.json`；只保存 worktree 绝对路径，不参与 gate hash |
| `data_policy` | policy 版本/hash、run 级 `scope_hash`、实际表清单、确认人、确认时间、证据引用和切换条件 |
| `diagnosis` | 现象、复现、根因、反证、需规依据、影响范围 |
| `plan` | 改动边界、非目标、验证计划、回滚计划 |
| `implementation` | 每个 repo 的改动文件、commit 列表、diff 摘要 |
| `review` | `repos[]`：reviewer、independent、reviewed_sha、scope、findings、verdict、review_hash、轮次 |
| `verification_matrix` | 修复行为、不破坏行为、边界行为及证据引用 |
| `gates` | `enter_dev`、`ship` 及每次 `validate-gate` 的稳定投影结果；不在这里重复存验收 |
| `ship_package` | `repos[]`：MR、merge commit、deployed SHA、Pipeline、image tag、rollout、dev 复测和验收步骤 |
| `acceptance` | 飞书状态、迁移记录、`mode=policy_only / chat_exact`、审批引用、`operator_verified=false`、可空 transition/operator、证据和结论 |
| `transitions` | 当前 cycle 每次推进的从/到、时间、校验结果、执行会话和证据引用 |
| `failure_stage` | `merge` / `push` / `pipeline` / `rollout` / `dev_verify` / `rework` |
| `failure_class` | 缺陷流程的简化失败分类；C1–C6 只作为映射参考 |
| `patch_round` | 当前周期的修补轮次；只统计需要重新修复的验证失败，环境重跑不计 |
| `blocked_from` / `resume_phase` / `resume_condition` | 阻塞前阶段、恢复目标和恢复条件 |
| `cancellation` | 取消人、原因、时间、MR/分支/dev 部署清理结果 |
| `decisions` | 影响行为、范围、数据、风险或 gate 的实质性自主决策 |
| `artifacts` | 报告、计划、评审文件及哈希 |
| `evidence` | manifest 摘要和缺失项 |
| `rollback` | `repos[]`：回退目标、revert commit、命令、验证和触发条件 |
| `cost_summary` | 可获得的 token/cost 摘要；L 级仍须回填 registry |
| `blockers` | 阻塞原因、责任人、恢复条件 |
| `next_action` | 唯一下一步、owner 和截止条件 |
| `updated_at` | 最后更新时间 |

最小结构示例只展示关键结构，实际模板由 `templates/state.schema.json` 固化。`worktree` 不在权威 `state.json` 中，示例中的 `local/<run_id>.json` 只用于本机恢复：

```json
{
  "schema_version": 2,
  "run_id": "2238-7164230616",
  "current_cycle_id": "cycle-001-20261110T162159+0800",
  "cycle_seq": 1,
  "cycles": [
    {
      "cycle_id": "cycle-001-20261110T162159+0800",
      "seq": 1,
      "started_at": "2026-11-10T16:21:59+08:00",
      "state_ref": "cycles/cycle-001-20261110T162159+0800/state.json"
    }
  ],
  "work_item": {
    "project_key": "6a687a81e231818dec771f9a",
    "auto_number": "2238",
    "work_item_id": "7164230616",
    "title": "示例缺陷",
    "qa_bug_id": null,
    "task_registry_id": null
  },
  "ownership": {
    "claim_id": "claim-20261110-001",
    "claim_comment_ref": "comment-...",
    "claim_operator": "human:current-user",
    "claimed_at": "2026-11-10T16:20:00+08:00",
    "session_id": "session-...",
    "machine_id": "machine-a",
    "current_owner": "agent:frontend",
    "takeover_history": []
  },
  "phase": "READY_SHIP",
  "patch_round": 0,
  "repos": [
    {
      "repo_id": "ui_topic",
      "repo_name": "lumen-ui-science-topic",
      "remote": "https://git.example/lumen-ui-science-topic.git",
      "base_branch": "dev",
      "base_sha": "abc123",
      "candidate_sha": "def456",
      "planned_change_scope": ["src/pages/topic"]
    }
  ],
  "data_policy": {
    "policy_version": "demo-2026-11-10",
    "policy_hash": "sha256:...",
    "scope_hash": "sha256:...",
    "scope": {
      "status": "approved",
      "tables": [
        {
          "database": "demo_gkxlumenx_dwd",
          "schema": "demo_gkxlumenx_dwd",
          "table": "<table-name>",
          "confirmed_by": "human:...",
          "confirmed_at": "ISO-8601",
          "evidence_ref": "evidence/manifest.json#E-DATA-001"
        }
      ]
    }
  },
  "gates": {
    "enter_dev": {
      "status": "approved",
      "source": "chat",
      "token_text": "进入开发",
      "claim_id": "claim-20261110-001",
      "gate_hash": "sha256:...",
      "bound_to": {
        "repos": [
          {
            "repo_id": "ui_topic",
            "repo_name": "lumen-ui-science-topic",
            "base_sha": "abc123",
            "candidate_sha": null,
            "planned_change_scope": ["src/pages/topic"]
          }
        ],
        "diagnosis_hash": "sha256:...",
        "risk_level": "M",
        "data_policy_version": "demo-2026-11-10",
        "data_policy_hash": "sha256:...",
        "data_scope_hash": "sha256:..."
      },
      "validation": {
        "result": "PASS",
        "checked_at": "ISO-8601",
        "projection_version": "p0-v3"
      }
    },
    "ship": {
      "status": "pending",
      "claim_id": "claim-20261110-001",
      "bound_to": null
    },
    "acceptance": {
      "status": "pending",
      "claim_id": "claim-20261110-001",
      "bound_to": null
    }
  },
  "review": {"repos": []},
  "ship_package": {"repos": []},
  "rollback": {"repos": []},
  "acceptance": {
    "status": "pending",
    "mode": "policy_only",
    "operator_verified": false,
    "work_item_status": "IN PROGRESS"
  },
  "transitions": [],
  "failure_stage": null,
  "failure_class": null,
  "blocked_from": null,
  "resume_phase": null,
  "resume_condition": null,
  "next_action": {
    "owner": "human",
    "action": "审阅提测包并发送提测"
  }
}
```

## 11. 结构化证据

`evidence.manifest` 按实际 kind 保存最小事实，不复制 `ship_package` 已负责的提测信息。每条证据至少包含：

| 字段 | 说明 |
|---|---|
| `evidence_id` | 稳定标识 |
| `kind` | command / ui / api / db / pipeline / review / manual / human_confirmation / acceptance |
| `result` | PASS / FAIL / SKIPPED / SIMULATED |
| `raw_path` / `sha256` | 证据文件相对路径和文件哈希 |
| `reviewable` / `raw_retained` | 是否可人工复核、raw 是否仍保留 |
| `non_reviewable_reason` | `reviewable=false` 时必填 |
| `command` / `exit_code` / `stdout_path` | 命令证据可追溯字段，不适用时为 `null` |
| `commit_sha` | 证据对应的代码提交 |
| `environment` / `collected_at` / `summary` | 环境、采集时间和脱敏摘要 |

`kind=db` 额外必须包含 `operation`、`database`、`schema`、`table`、`access_mode`、`host_ref`、`account_ref`、`enter_dev_gate_hash`、`data_policy_hash`、`data_scope_hash`、`write_checked_at` 和 `write_authorization_id`。写前必须在有效 `进入开发` gate 下调用受控检查；当 gate、policy、scope、表、账号或 host 不匹配时拒绝，不生成可记录的证据授权。

规则：

- “测试通过”必须能追溯到命令、退出码和输出；
- UI 证据优先记录路由、环境、视口、数据集和程序化状态断言；确需截图时只保留目标区域的前后各 1 张；
- API 证据记录请求摘要、状态码和关键字段，不记录 token/cookie；
- 数据库写入必须先通过 `check-data-write`；证据只记录脱敏操作摘要，不记录敏感值；
- 模拟结果必须标 `SIMULATED`，未执行项必须标 `SKIPPED` 并说明原因；
- P0 简化为：只有 `reviewable: true` 且 `raw_retained: true` 的证据可以支撑验证矩阵中的 `PASS`；raw 文件未保留或已过期时可以记入 manifest 并标 `reviewable: false`，但只能用于说明、`SKIPPED` 或 `SIMULATED`，不能伪装成 PASS；
- 验证矩阵的每个 `evidence_refs[]` 必须能在已校验 manifest 中解析；`PASS` 只能引用 manifest 中结果为 `PASS` 的可复核证据；
- `timestamp`、`cwd`、`producer`、`stdout_path`、`raw_retained`、`reviewable` 只用于审计和展示，不进入 `verification_hash`；稳定投影字段见 §7.0；
- 报告只能从 `state.json` 和 manifest 渲染，不允许模型另写一套自由文本事实。

校验器只能约束按流程执行的 Agent 和可复核记录，不能阻止拥有数据库凭据的 Agent 完全绕开账本直写。P0 通过写前检查、逐表 scope、受控账号引用和“0 次 scope 外写入”审计指标降低风险；真正的强制拦截需要数据库代理或受控执行入口，留到 P1。

## 12. 数据与 Mock 策略

数据策略采用 **B 语义：base policy 限定 environment/host/database/schema，run scope 负责逐表白名单，deny-by-default**。基础策略放在 `.cursor/skills/feishu-bugfix/policies/<version>.yaml`，不直接授权具体表；每个 run 的 `state.json.data_policy.scope.tables` 必须从诊断链路中逐表枚举，并记录 `status/confirmed_by/confirmed_at/evidence_ref`。`state.json.data_policy` 保存 `policy_version`、`policy_hash`、`scope_hash` 和实际表清单，`scope` 为空或未确认时拒绝写入。任何 DB 写入前必须已有有效 `进入开发` gate 并执行 `check-data-write`，检查 policy、scope、environment、host、database、schema、table、operation、access mode 和 account；任何未命中 `policy + scope` 的写操作都必须进入 `BLOCKED`。旧 run 不得因为新 policy 覆盖而失去可复核性。

当前策略版本：`demo-2026-11-10`，阶段为 `demo_until_cutover`。

这是项目负责人在 2026-11-10 确认的**限时 Demo 例外**，属于有记录的例外，不宣称“不修改 D16/D18”，也不代表正式生产授权。决定记录见 `policies/decisions/demo-phase-2026-11-10.md`。若当前 Demo 库确实属于 D16 的 ODS/DWD/ADS 范围，或 CMS 被视为正式业务库，则必须在 policy 中附上架构/数据负责人的批准记录；没有记录时只能进入 `BLOCKED`。

```yaml
schema_version: 1
policy_version: demo-2026-11-10
status: active-demo
phase: demo_until_cutover
default_decision: deny
database_is_schema: true
owner_decision:
  decided_by: human:徐滕强
  decided_at: 2026-11-10
  approval_ref: policies/decisions/demo-phase-2026-11-10.md
  review_owner: human:徐滕强
  review_at: 2026-11-17
  expires_at: 2026-12-10T23:59:59+08:00
  cutover_trigger: 用户通知正式上线；若早于 expires_at，以通知时间为准
allowed:
  demo_warehouse:
    environment: demo
    host_ref: env:DEMO_MYSQL_HOST
    account_ref: env:DEMO_MYSQL_USER
    databases: [demo_gkxlumenx_ods, demo_gkxlumenx_dwd, demo_gkxlumenx_ads, demo_gkxlumenx_dim]
    schemas: [demo_gkxlumenx_ods, demo_gkxlumenx_dwd, demo_gkxlumenx_ads, demo_gkxlumenx_dim]
    table_policy: run_scope_required
    writers: [python]
  current_demo_cms:
    environment: demo
    host_ref: env:DEMO_MYSQL_HOST
    account_ref: env:DEMO_MYSQL_USER
    database: gkxlumenx_cms
    schema: gkxlumenx_cms
    table_policy: run_scope_required
    access: application_only
    approval_ref: policies/decisions/demo-phase-2026-11-10.md
  d16_gapfill:
    environment: demo
    host_ref: env:DEMO_MYSQL_HOST
    account_ref: env:DEMO_MYSQL_USER
    database: gkxlumenx_gapfill
    schema: gkxlumenx_gapfill
    table_prefix: gapfill_
    table_policy: run_scope_required
    writers: [python]
  d18_new_ads_mock:
    status: disabled
    table_policy: run_scope_required
forbidden:
  - write_formal_ods
  - write_formal_dwd
  - write_formal_ads
  - alter_formal_schema
  - supplier_database
  - frontend_or_java_fabricated_data
  - direct_api_mock_response
  - production_mock_write
```

规则：

- “明显 Demo 命名”不是授权条件；执行时必须同时命中 `environment + host_ref + database + schema + table`，且实际 policy 与 run scope 必须写出全限定表名和可核验的执行账号证据，设计稿中的空数组和占位符本身不构成授权。
- base policy 只负责 environment/host/database/schema 层；具体表只在 run scope 中授权。`scope.tables` 为空、`status` 不是 `approved`、缺少 `confirmed_by/confirmed_at/evidence_ref` 时一律拒绝。
- 普通同事不手工编辑表清单。Agent 在诊断阶段从复现链路、SQL、接口和改动边界生成候选表，连同 policy 版本一起展示；没有命中白名单就停止，不靠猜测补表。
- `demo_gkxlumenx_*` 只覆盖当前 Demo 阶段；即使它是独立 demo schema，也要保留 host/database/account 证据。禁止把 `demo_` 前缀解释为对正式 `gkxlumenx_*` 的永久豁免。
- `gkxlumenx_cms` 是当前正式 CMS 业务库的特殊例外。只能通过 CMS 业务接口或已登记的受控脚本操作，不能因为业务库名“正式”就放开整库 SQL 写入；该例外必须有确认记录和切换 owner。
- Mock/模拟行只由 Python 或 CMS 业务流写入；前端和 Java 不得直接伪造数据，接口不得直接返回内存 fixture 或常量假数据。
- D16 只允许 `gkxlumenx_gapfill.gapfill_*`，且行上必须有 `metric_id`、`gap_item`、`fill_method`、`gapfill_batch_id`、`generated_at`；`fill_model` 仅在 `fill_method=llm` 时必填。
- D18 只允许新建 ADS 表、由 Python 灌入 mock 行、接口只读该表；禁止把 `D18` 用作修改现有 ODS/DWD/ADS 的通行证。
- 当前 policy 的 `d18_new_ads_mock.status=disabled`，在真实 schema、表和审批记录补齐前不得启用。
- 所有模拟数据、缺项数据、真实数据必须能区分；数据库批次、报告和 UI 必须使用 `SIMULATED`、`SKIPPED` 或对应 Mock 标识，不允许把模拟结果伪装成 live。
- 当前 policy 与 D16/D18 或仓库硬规则冲突时，不能靠聊天中的“可以”覆盖，必须进入 `BLOCKED`，写明冲突原文、影响范围和需要谁签字。已经存在的架构批准记录可以作为例外依据，但不能由 Agent 自己生成或推断。

### 12.1 上线切换

用户通知正式上线后，创建新 policy 版本，例如 `production-cutover-<日期>`；旧 policy 保持不可变，新 run 和未完成 run 都切换并重新校验：

1. `phase` 改为 `production`；
2. `current_demo_cms` 和 `demo_warehouse` 全部删除或标记过期；
3. 禁止所有 Mock 写入、Demo 数据制造和接口 fixture；
4. 只保留已登记的 `gapfill_*` 与符合 D18 的新 ADS 实现路径；
5. 更新 `policy_hash`，使旧 gate 失效，并要求重新验证已打开的 run；
6. 记录切换人、切换证据、`cutover_trigger` 和新的 review owner；
7. 不依赖历史会话记忆判断是否已经上线，必须读取新 policy 和用户通知证据。

### 12.2 写库前后的证据

任何数据库写入都必须记录：

- policy 版本和 hash；
- 环境、host_ref、database、schema、表名、执行账号和账号证据；
- 操作类型和影响行数；
- 写前查询快照或计数；
- 写后校验查询或计数；
- 涉及数据的脱敏摘要，不记录敏感原文；
- 回滚 SQL 或恢复方式。

缺少这些证据时，只能标记 `SKIPPED`，不得在报告中写成 PASS。

## 13. `report.md`

人工只读一份报告，由校验器渲染，至少包含：

1. 缺陷事实和复现；
2. 根因、需规依据和影响范围；
3. 改动摘要和非目标；
4. 验证矩阵和证据结果；
5. 已知风险和未覆盖项；
6. S/M/L 风险等级和定级理由；
7. data policy、run scope 表清单、确认人和审批/决定记录；
8. failure stage、failure class 和返工轮次；
9. 提测信息；
10. 人工验收步骤；
11. gate 状态与绑定对象；
12. 自动决策摘要；
13. 回滚版本、回滚方式和回滚验证。

报告按当前阶段渲染：尚未发生的提测、验收、回滚内容显示 `PENDING`，不能提前写成“已完成”。M/L 的评审信息合并进同一份报告；只有 L 级或评审确实复杂时才增加独立 `review-report.md`，报告只内联关键结论和路径，附录文件不替代主报告的单一入口。

验证矩阵至少覆盖：

1. **修复行为**：原问题是否在真实入口消失；
2. **不破坏行为**：相邻 Tab、默认条件、全量语义、写路径是否正常；
3. **边界行为**：空数据、接口失败、无权限、重复提交等是否可解释。

每个 repo 的验证矩阵必须至少存在 `fix` 和 `regression`；M/L 还必须至少有一个适用的非 happy-path 类别（`boundary/integration/data/algorithm/security/performance/rollback`）。不适用时允许 `SKIPPED + skipped_reason`，不能只写一条修复行为直接进入 `READY_SHIP`。

## 14. 语义权威顺序

1. 平台和仓库硬规则；
2. 当前会话中的明确人工决策；
3. 最新验收口径和正式需规；
4. 已批准方案；
5. 代码与运行证据；
6. 旧缺陷描述；
7. AI 推断。

规则冲突时不得自行选择最方便的一项。当前人工意见只有在写入版本化 policy、明确表/环境影响并完成必需签字后，才能形成限时例外；否则与 D16/D18、权限、数据安全或其他硬规则冲突时进入 `BLOCKED`，给出冲突原文、影响和需要谁签字。

## 15. 自动决策与修补上限

三个人工门之间只有影响行为、改动范围、数据、风险等级、验证结论或 gate 的**实质性决策**才写入 `state.json.decisions`，至少包含：

- 决策；
- 依据；
- 被否决的替代方案；
- 影响范围；
- 是否需要提测时追认。

普通实现选择不记录，避免 S 级文案/样式修复被账本负担拖慢。`patch_round` 记录当前周期的修补轮次；所有等级默认最多 3 轮修补。达到上限仍无法通过验证时进入 `BLOCKED`，报告已尝试内容、证据和所需决策，不继续盲目试错。对用户只显示“已受阻”。

`requires_human_ratification=true` 且 `ratified_by` 为空的决策会在 `提测` gate 和 `READY_SHIP` guard 处阻止推进；Agent 不能用后续自然语言“继续”代替追认。

### 15.1 缺陷流程失败分类与修补轮次

缺陷流程使用自己的 `failure_class`，不强制套用长任务缺陷包的字段；C1–C6 只做语义映射参考：

| `failure_class` | 判据 | 动作 | 参考 C 类 |
|---|---|---|---|
| `product_or_code` | 期望未发生、页面/接口错误、本次修复引入回归 | 返工；dev 已部署且确认是本提交问题时 revert 后重开 | C1 |
| `environment_or_release` | 镜像未滚、服务不健康、发布地址错误、环境抖动 | 重跑部署/验证；不改业务代码，不计 `patch_round` | C2 |
| `allowed_empty` | 需求明确允许的空态，非 5xx、非白屏 | 记录允许空态，不返工 | C3 |
| `expectation_or_case` | 需规或测试期望错误、页面已迁移 | 停止返工，升级需求 owner 确认 | C4 |
| `schema_or_permission` | 新表、改结构、权限或正式库闸门风险 | `BLOCKED`，升级数据/架构 owner | C5 |
| `unknown` | 无明显代码原因、无可用 trace、三轮仍失败 | `BLOCKED`，带证据请求人工分诊 | C6 |

规则：

- X-Trace-Id 有则记录，无则不强制；不能因为缺少 trace 自动判定为产品问题；
- `patch_round` 只在本轮需要重新修改代码时递增：`product_or_code` 的修复失败算一轮，`environment_or_release` 的重跑不算；
- 环境类失败最多重跑 2 次；仍无法确认时按 `unknown` 进入 `BLOCKED`；
- 每个失败同时记录 `failure_stage` 和 `failure_class`，例如 `rollout` + `environment_or_release`；
- 达到 3 轮修补仍不能通过时进入 `BLOCKED`，不要继续盲目试错。

## 16. 与主仓流程的接入边界

### 16.1 轻量缺陷通道

本 P0 是经确认的轻量缺陷通道：

- 批准人：项目负责人（当前用户），批准日期：2026-11-10；涉及 D16/D18 或权限例外时，另附具体批准记录，不把本轻量通道当作架构签字；
- 仅为 `feishu-bugfix` 的缺陷修复路径；
- `state.json + report.md` 是该路径的 DoD 记录，不要求再复制一份 handoff；
- 如组织要求必须建 registry，则使用最小 `task_type=bugfix` 映射，不得另造第二套状态机。

| 等级 | registry / handoff / cost |
|---|---|
| S | 不创建 task-registry 和 handoff；`state.json + report.md` 替代该任务的 DoD 记录；cost 有则记，无则标 `UNAVAILABLE`，不得伪造 0 |
| M | 单会话可不创建 registry；跨会话或需要协调时创建 task；跨仓 Bundle 至少为 M；handoff 可由 `report.md` 链接替代；cost 按可得信息记录 |
| L | 必须接 task-registry、task MCP、worktree、handoff 和 cost 四字段 |

该豁免仅适用于 `feishu-bugfix` 轻量缺陷通道，不放宽 L 级或长任务段 E 的要求。跨仓 Bundle 属于轻量通道内的明确能力，但仍必须满足风险至少 M、每仓评审和完整集成验证。

### 16.2 中央规则和仓级 AGENTS

- 真源分层：本文件是流程/权限真源，`SKILL.md` 是操作真源，`templates/state.schema.json` 是机器结构真源，`policies/` 是数据授权真源；发生冲突时按本文件 → Skill → schema → policy 的顺序解释；
- Skill 的唯一完整来源是 `.cursor/skills/feishu-bugfix/`；Cursor 直接加载 canonical 包，Codex / Trae 只生成薄适配入口；`.cursor/skills/feishu-bugfix/scripts/sync-bugfix-skill.mjs --write` 生成适配入口，`--check` 只做漂移检测；禁止把客户端入口同时当作真源编辑；
- `.cursor/rules/fe-manual-confirm-push.mdc` 必须与 Skill 在同一个发布步骤中更新，补充 `进入开发` 对独立 fix 分支的权限映射；该规则包含 2026-11-05 用户裁定，修改前必须重新获得用户确认，不能由 Agent 自行改文；
- 业务仓 `AGENTS.md` 只增加一行指针，说明缺陷流程以本文件为准，不复制整套规则；
- `fe-manual-confirm-push.mdc` 已废止旧 AGENTS 中无条件“完工即推”的口径；在旧条款尚未清理前，以中心规则为准，禁止从历史派单或旧会议纪要推断推送例外；
- 当前已知 `repos/lumen-ui-science-pc/AGENTS.md` 仍存在与中心规则冲突的旧推送口径，实施时用脚本定位并替换为统一指针，不能靠 Agent 记忆逐仓处理；
- 用脚本检查业务仓指针和 Skill 三端版本一致性，禁止逐份手工维护；
- 缺陷修复默认使用 `fix/<work-item-id>-<slug>`，这是对 `feat/* → MR/merge → dev` 常规 flow 的轻量例外；若组织要求统一命名或必须走 feature 分支，以 `repo-registry.yaml` 和仓库保护规则为准；直接推 `dev` 仅在对应仓规则明确允许时使用；
- 仓库路由使用 `agent-delivery/repo-registry.yaml`，`repos[].repo_id` 必须对应 registry 的 `repos[].id`，并校验解析出的 `lumen.name/remote` 或 `demo.name/remote`；测试命令读取对应仓 `AGENTS.md`；
- 接管只认精确消息 `接管【auto_number】`；handoff、任务派单和“你接手吧”只能作为背景材料，不是接管授权；接受风险、继续、你看着办等自然语言不解锁 gate；
- 代码变更遵守 `.cursor/rules/multi-session-protection.mdc`，禁止 `git reset --hard` / `git clean -fd/-fdx` 和不可恢复的临时搬运。

### 16.3 CI/CD 语义

- `dev` 是集成分支；无关红基线不阻断与失败路径不相交的本地开发，但阻断 `READY_SHIP`/`提测`；
- 当前业务仓主要以 `dev` 分支触发 CI/CD；fix 分支/MR 通常没有远端 pipeline，因此提测前只能声称完成仓内自检/本地验证，不能声称“分支 CI 通过”；
- push `dev` 后在条件满足时自动构建、部署 dev 并 rollout；
- `提测`包含这条自动部署链；
- GitLab 保护分支、MR approve 和仓库发布规则优先，`提测`不绕过保护规则；
- dev 复测失败时先分类，再只 revert 本次 run 的提交，生成 `DEV_VERIFY_FAILED` 和回退证据；
- P0 不包含生产自动发布。

### 16.4 QA 缺陷台账边界

- 本流程只处理飞书 Project issue，以飞书 `auto_number` 和 `work_item_id` 为业务编号；
- P0 不直接写入 `agent-delivery/qa/bug-registry.yaml`，避免同一缺陷出现两套状态机；
- 如现有 QA 流程强制要求关联本地 `BUG-*`，只在 `state.work_item` 记录 `qa_bug_id` 作为外键，状态仍以飞书和 `state.json` 为准；
- `gkx-bug-record` / `sync-feishu-bug` 仍是 QA 侧工具，不由本 Skill 隐式调用。

## 17. P0 范围和暂不实现

包含：

- 复用现有 Codex / Cursor / Trae、飞书项目 MCP、GitLab 和 Skill 体系；
- 单缺陷状态机和对外简化状态；
- 三个精确人工门（开发、提测、验收）及飞书验收落点；
- S/M/L 分级；
- gate 绑定、失效和接管；
- 结构化证据、单一 `report.md` 和内部校验器；
- 版本化 data policy；
- Codex / Cursor / Trae 共用同一 Skill 语义。

暂不实现：

- 自研 Agent Runtime；
- 自研任务调度平台、独立数据库或 Web 控制台；
- 自动轮询飞书；
- Webhook、队列、常驻 Runner；
- lease TTL、心跳和无人值守恢复；
- append-only 审计流水和独立 evidence Runner；
- 自动合并或绕过人工验收；
- 生产自动部署；
- 所有缺陷强制启用长任务、提交考古或覆盖率门槛。

## 18. P0 试点与通过条件

接下来 5 个真实飞书缺陷用于试点，重点观察：

- 人工新增发现的问题数量；
- 首次提测后的返工轮次；
- 是否稳定为三个精确口令且无自然语言误触发；
- 是否发生错仓修改、越权 merge/deploy、越范围 Mock 或生产写入；
- 报告是否足以支持人工在不读代码的情况下验收；
- S/M/L 和评审强度是否匹配；
- 换会话或换机器后能否从入库账本恢复。

P0 通过条件（`BLOCKED` / `CANCELLED` 的 run 可以计入试点，但必须有有效的终止状态、证据和恢复/清理记录）：

- 5 个缺陷均有有效、已入库的 `state.json` 和 `report.md`；
- manifest 能追溯到 commit、命令、退出码和环境；
- 0 次未授权 push/MR、merge 或 deploy；本地代码修改是否在 `进入开发` 前发生，由本机 pre-change 审计或后续 hook 校验，外部 GitLab audit 只能证明提交后的行为；
- 0 次生产写入或 run scope 外写入；共享数据库账号无法归因到单个 run 时，必须标记为审计限制，不得宣称已证明 0 次；
- 0 次因 gate 复用导致跨缺陷或跨 commit 授权；
- 每次 `advance` 都有可追溯的 `validate-gate` 结果，换会话/换机器和 REOPEN 均会触发重新确认；
- 每次完成都对应飞书当前为 `RESOLVED` 的状态记录，并写入 `acceptance.mode=chat_exact / policy_only`、审批引用和 `operator_verified=false`；自然语言不得被记录为 chat_exact；
- 简单缺陷平均返工不超过 1 轮；
- 普通同事无需手工填写 JSON 或阶段模板。

指标采集源：

- GitLab audit、分支保护和 MR 记录用于核验越权 merge/deploy；
- CI job、pipeline、rollout 和镜像 tag 用于核验 dev 实际部署版本；
- 数据库写前/写后证据和受控账号审计用于核验 policy 外写入；
- `state.json.transitions[]` 用于核验 gate 重新确认和失败恢复；
- 试点样本至少覆盖 1 个 M 级；真实发生 `DEV_VERIFY_FAILED` 时完整记录，不为了凑样本故意破坏共享 dev。未真实发生时，用状态机单元测试的合成事件验证转换，不能伪造线上失败证据。

## 18.1 v0.8 确定性修复

- 禁止 S/M/L 风险降级，避免 Agent 通过降级绕过评审；
- `init` 只允许 `INTAKE` / `CLAIMED`，首次 `enter_dev` 必须从 `READY_DEV` 批准；
- `deployed_sha` 不再强制等于 `candidate_sha`，改为强制 `merge_commit_sha`、`pipeline_url` 和实际部署 SHA；
- 验证矩阵引用必须解析到已校验 manifest，PASS 不得引用缺失、FAIL、SIMULATED、SKIPPED 或不可复核证据；
- `reviewable=false + raw_retained=false` 可记录和展示，但不能支撑 PASS；
- 运行目录编号只允许数字，阻断路径穿越；
- 负向 selfcheck 覆盖上述回归；
- P0 自动流承接 S/M 缺陷；v1.1 起同一缺陷的跨仓 Bundle 保持单 run，使用每仓候选、依赖顺序和完整集成验证，不再因多仓自动拆单或路由；只有 L 保留分级结果并路由到现有 task-registry、task MCP、worktree 和长任务执行规约。

## 18.2 v0.9 试点闸门补齐

- `CLAIMED` 必须记录飞书 `[agent-claim]` 评论引用、操作者和认领时间；接管同样要求新 claim 评论证据；
- `kind=db` 证据写前必须通过 policy + run scope 检查，并记录 policy/scope hash、表、操作、access mode、host/account ref 和写授权 ID；
- 验证矩阵必须按仓库覆盖 `fix`、`regression`，M/L 追加至少一个适用的非 happy-path 类别；不适用时用 `SKIPPED + skipped_reason`，不能只写一条修复行为；
- `requires_human_ratification=true` 且未追认的决策不得通过 `提测` 或进入 `READY_SHIP`；
- 上述四类规则加入负向 selfcheck；P0 功能冻结，真实试点期间不再扩字段或命令。

## 18.3 v0.9.1 写入时序修复

- `check-data-write` 只放宽 `enter_dev` 的 candidate 条件：`verify-repo` 后仍允许 DB 写；首次 `approveGate` 和 `advance IMPLEMENTING` 继续要求 candidate 为 `null`；
- 当前写入授权检查当前 gate、session/machine、policy 和 scope；历史 DB 证据复核使用 `transitions[]` 中已批准的 gate hash，不再要求当前 gate 仍为 approved；
- 风险升级到 L 时 gate 直接 `invalidated`，不再保留可重新确认的假路径；
- selfcheck 增加 `verify-repo → check-data-write` 成功、风险升级后历史 DB 证据仍可复核两条回归。

## 18.4 v0.9.2 gate 命令词简化

- 精确 gate 从带中文方括号的展示形式改为裸词 `进入开发` / `提测`；
- 裸词仍必须作为完整消息发送，或使用 `进入开发<auto_number>` / `提测<auto_number>` 区分多个 active run；
- “不要进入开发”“可以进入开发吗”等包含命令词的自然语言仍不得解锁；
- 文档、Skill、校验器和 selfcheck 必须在同一版本更新，禁止客户端自行兼容旧括号格式。

## 19. 后续实施顺序

1. 本收敛稿已完成评审，进入真实缺陷试点。
2. 已创建 `templates/state.schema.json`、`templates/report.md`，并在 `policies/` 下落第一版不可变 policy 和决定记录；base policy 只到 schema 层，run scope 的每张表必须逐项列出 confirmation 和 evidence，scope 为空不得试跑。
3. 已实现 `.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs` 的受控事实写入、精确 gate、阶段产物 guard、真实 Git 与 evidence 校验、版本化 policy 执行、cycle 归档、报告渲染和失败分类；`state.schema.json` 在每次读写时执行，未知字段和 `patch_round>3` 直接拒绝。`verify-repo` 校验 HEAD、origin、base ancestor、干净工作区和 planned scope；`check-data-write` 校验 DB 写前 policy/scope；`verify-evidence` 校验 manifest 路径、SHA256、验证矩阵证据引用和 reviewable/raw_retained；`review_hash`、`diff_hash` 和 `verification_hash` 由脚本计算。用 `node .cursor/skills/feishu-bugfix/scripts/bugflow-state.selfcheck.mjs` 做离线正负向回归，已覆盖风险降级、非法初始阶段、部署 SHA、DB 越权写入、基础验证缺失、M/L 非 happy-path 缺失、claim 证据缺失、未追认决策和不可复核证据冒充 PASS。
4. 已增加安全 `.gitignore`：只忽略 `evidence/raw/` 和本机 `local/` 映射，不忽略 `state.json`、`report.md`、`manifest.json`。
5. 已将 `.cursor/skills/feishu-bugfix/` 设为唯一完整 Skill 包，并由 `.cursor/skills/feishu-bugfix/scripts/sync-bugfix-skill.mjs --check/--write` 生成 Codex / Trae 薄适配入口；Cursor 直接加载 canonical 包，适配入口禁止手工维护。
6. 在同一个发布步骤中更新 `fe-manual-confirm-push.mdc`，明确 `进入开发` 只授权独立 fix 分支 push、不授权 dev/生产；修改该规则前向用户重新确认 2026-11-05 的人工确认裁定，并记录批准。
7. 用真实新缺陷试跑，不回溯修改已关闭缺陷【2238】；共享数据库账号归因、独立失败注入环境和更细审计留到 P1。
8. 根据 5 个试点结果决定是否进入 P1 和自动触发。

## 18.5 v1.1 同缺陷跨仓 Bundle

- 一个飞书缺陷即使涉及多个代码仓库，仍然是一个 Bug、一个 run、一个 claim 和一套精确 gate；禁止因仓库数量拆成多个飞书缺陷。
- `repos[]` 新增 `role`、`depends_on`、`ship_order`。多仓时三者必填；`ship_order` 连续为 `1..N`，依赖仓库必须更早 ship。
- 多仓 Bundle 风险至少为 M；跨仓本身不再自动升级为 L。达到 L 时仍按现有长任务流程处理。
- `enter_dev` 和 `ship` gate 均绑定完整仓库集合及其 Bundle 拓扑；仓库、依赖顺序或 ship 顺序变化会使旧 gate 失效。
- 每个仓库仍需独立候选 SHA、diff/review/verification；另强制至少一条覆盖全部仓库的 `integration` 验证。
- `record-ship-package` 按 `ship_order` 固化提测信息；任一仓失败时整个 Bundle 停留在返工/失败态，不允许单仓标记完成。

## 18.6 v1.2 精确验收口令

- 新增第三个精确人工门 `验收通过`；多 active run 使用 `验收通过<auto_number>`。
- `acceptance` gate 绑定当前 claim、ship gate hash、dev verification PASS、已验证 evidence manifest hash 和批准时的飞书状态。
- Agent 收到精确口令后先查询 `get_transitable_states` / `get_transition_required`，再调用一次合法 `transition_state` 迁移 `RESOLVED`。
- 账本记录 `mode=chat_exact`、审批引用、session/machine、Feishu transition 结果和 `operator_verified=false`。
- “可以了”“没问题”“算修复了”等自然语言不解锁；人工直接操作飞书仍保留 `policy_only` 路径。

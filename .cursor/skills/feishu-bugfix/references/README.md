# 飞书缺陷修复 Skill 与运行账本说明

> 状态：v1.2 精确验收口令优化版
> 建立日期：2026-11-10
> 适用范围：飞书项目中由当前用户认领并修复的缺陷
> 真源分层：本目录是 Skill 的唯一 canonical 包；`../SKILL.md` 管操作入口，`BUG-PLAYBOOK.md` 管类型路由和验证方法，`P0-DESIGN.md` 管 gate/权限细节，`../templates/state.schema.json` 管机器结构，`../policies/` 管数据授权
>
> Skill 真源：`.cursor/skills/feishu-bugfix/SKILL.md`；`.codex` 和 `.trae` 目录只放薄适配入口。
> 技术路线：复用现有 Codex / Cursor / Trae + Skill + 轻量校验脚本，不自研 Agent Runtime
> 当前实现：`../scripts/`、`../templates/`、`../policies/` 已落地

## 定位

本 Skill 负责流程执行和校验；每个缺陷的**执行真相**保存在 `agent-delivery/bugfix-runs/<auto_number>-<work_item_id>/`，用于回答：

- 当前缺陷处于哪个阶段；
- AI 为什么做出这个判断；
- 是否获得当前 claim 下的有效授权；
- 改了什么、在哪个 commit 上验证了什么；
- 是否已经提测、部署 dev 和完成业务验收；
- 出现问题时如何回退。

职责分离：

| 真相源 | 职责 |
|---|---|
| 飞书项目 | 业务状态、负责人、人工验收结论 |
| `bugfix-runs/<auto_number>-<work_item_id>/` | 阶段、gate、诊断、验证、证据摘要和下一步 |
| GitLab | 分支、commit、diff、MR、Pipeline 和 dev rollout |

## 使用体验

普通同事只需要完成四件事：

1. 发起处理或确认目标缺陷；
2. 审阅诊断和改动边界，发送 `进入开发`；
3. 审阅提测包，发送 `提测`；
4. 在 dev 完成业务验收，发送完整精确消息 `验收通过`；Agent 校验后自动完成飞书状态迁移。

`提测`表示：合并 `dev`、触发 CI、自动部署 dev 并完成 dev 复测。它不授权生产发布。

最终验收增加第三个精确口令 `验收通过`。只有完整精确消息（多 active run 时用 `验收通过<auto_number>`）才能批准 `acceptance` gate；Agent 随后读取飞书可流转状态和必填项，调用 `transition_state` 迁移 `RESOLVED`，再记录 `acceptance.mode=chat_exact`、审批引用、session/machine 和 `operator_verified=false`。“可以了”“没问题”“算修复了”等自然语言不解锁。人工直接在飞书完成迁移时，仍保留 `policy_only` 观察路径。

P0 不在每个 gate 写飞书评论。外部只保留认领时的 `[agent-claim]`、提测总结和最终验收总结三条评论；gate 的真实性由 `state.json`、绑定对象和校验器保证。

## v1.2 优化后的主流程

```text
预检 -> 认领 -> Bug Contract -> 类型路由 -> 复现/修复
-> 风险匹配的验证与评审 -> 提测/部署 -> 验收通过 -> 自动迁移 RESOLVED
```

关键变化：

- **先找依据再改代码**：必须从主仓需求、SRS、设计、数据、QA 或最新人工裁定中找到期望行为；`requirement_refs` 必须可定位。
- **需规功能点必须覆盖**：每个缺陷至少映射一个 SRS 文件 + 序号 + 五级功能路径；修复验证必须覆盖该功能点的实际行为，不能只修截图表象。
- **按缺陷类型验证**：UI、API、数据、算法、配置、权限分别使用不同验证矩阵，不再统一套前端流程。
- **同 Bug 跨仓不拆单**：一个飞书缺陷涉及多个仓库时仍是一个 claim/run，使用跨仓 Bundle 记录各仓 `role`、`depends_on`、`ship_order`；风险至少 M，并必须有覆盖完整 Bundle 的 `integration` 验证。
- **S/M 轻量化**：S 只需 `fix + regression`，M/L 至少再有一个非 happy-path 类别；S 默认不做独立 review。
- **提测前先看基线**：最新 dev pipeline 为红时，先分清是否当前范围；无关失败不计入补丁轮次。
- **返工不重复进入开发**：同一范围和风险的验收返工保留 claim，只重做 diff/review/verification 并重新 `提测`。
- **有预算和止损**：S 目标 30–60 分钟，M 目标 1–2 小时；同一环境故障连续两次无进展即阻塞。
- **本地优先、截图克制**：纯前端使用本地服务和机器断言，覆盖可视区外内容；截图最多一张最终辅助证据。

详细类型路由见 [`BUG-PLAYBOOK.md`](BUG-PLAYBOOK.md)。

## 对外状态

```text
主链：待认领 → 已认领 → 待进入开发 → 修复中 → 待提测 → 待验收 → 完成
旁路：任一阶段 → 受阻
      待验收或提测后 → 返工中
      确认无需修复 → 已取消
```

“返工中”和“受阻”必须分开；`RESOLVED` 后再次复现时复用同一 run，开启新的 `cycle_id`：

- 返工中：验收或 dev 复测失败、REOPEN、修复引入新问题；
- 受阻：缺少复现、需求、权限、环境、测试能力或策略授权。

## 目录结构

```text
.cursor/skills/feishu-bugfix/
  SKILL.md
  references/
    README.md
    BUG-PLAYBOOK.md
    P0-DESIGN.md
  scripts/
    bugflow-state.mjs
    bugflow-state.selfcheck.mjs
    revalidation-plan.mjs
    revalidation-plan.selfcheck.mjs
    sync-bugfix-skill.mjs
    lib/
  templates/
    state.schema.json
    report.md
  policies/
    demo-2026-11-10.yaml
    decisions/

agent-delivery/bugfix-runs/
  <auto_number>-<work_item_id>/
    state.json            # 只表示当前 cycle
    cycles/
      <cycle_id>/state.json
      <cycle_id>/evidence/manifest.json
    report.md
    evidence/
      manifest.json
      raw/                # 默认 gitignore
    plan.md               # L 或确有必要时
    review-report.md      # L 或独立评审需要时
```

入库规则：

- `state.json`、`report.md`、`evidence/manifest.json` 必须入库；
- `ownership` 必须包含 `claim_comment_ref`、`claim_operator`、`claimed_at`；没有这三项不能把 run 标成 `CLAIMED`；
- 数据策略使用 `policies/<version>.yaml` 不可变版本；run 记录 `policy_version`、`policy_hash` 和策略快照 hash，不能依赖会变化的全局文件；
- 截图、stdout、API 响应和临时日志放在 `evidence/raw/`，默认不入库；
- manifest 记录命令、退出码、输出路径、SHA256、证据类型、环境、时间和对应 commit；DB 证据还要记录写授权、policy/scope hash 和表/账号信息；
- `state.json` 只表示当前 cycle，历史 cycle 完整归档到 `cycles/<cycle_id>/state.json`；manifest 是证据明细真源。至少在 claim、进入开发、提测、失败/回退、验收节点提交；一个 run 固定一台执行机，换机器必须重新校验 claim、repos、candidate/deployed SHA、证据和 gate；
- 飞书写回只放脱敏摘要，不放 token、cookie、签名 URL 或敏感数据。

## 风险分级与流程

| 等级 | 流程 |
|---|---|
| S | 自审、`fix + regression`、本地或只读证据；不建 task-registry/handoff |
| M | S 基础上增加至少一个非 happy-path 类别、影响面和一次独立针对性评审；跨仓 Bundle 至少为 M；单会话可不建 registry |
| L | 仅识别并路由；必须接现有 task-registry、task MCP、worktree、全量净室评审和 handoff/cost，不进入 P0 轻量自动流 |

S/M/L 只允许上调，不允许为了减轻流程自行降级。M/L 不得跳过评审。

本轻量通道是 `feishu-bugfix` 的明确豁免：P0 自动流承接 S/M，包括**同一缺陷的跨仓 Bundle**，用 `state.json + report.md` 承载执行记录；L 和长任务段 E 仍遵守主仓完整规约并路由现有流程。跨仓本身不触发拆单。

## 与主仓规约的关系

- 真源分层：`P0-DESIGN.md` 是流程/权限真源，`SKILL.md` 是操作真源，`templates/state.schema.json` 是机器结构真源，`policies/` 是数据授权真源；
- Skill 的唯一完整真源是 `.cursor/skills/feishu-bugfix/`；Cursor 直接加载该 canonical 包，Codex / Trae 只保留薄适配入口。更新后运行 `node .cursor/skills/feishu-bugfix/scripts/sync-bugfix-skill.mjs --write`；
- 业务仓 `AGENTS.md` 只增加统一指针，不复制整套流程；
- `.cursor/rules/fe-manual-confirm-push.mdc` 补充开发/提测口令的前端权限映射；验收口令由 Skill 校验，不改前端推送规则；
- 该中心规则废止旧 AGENTS 中无条件“完工即推”的条款；旧条款未清理前以中心规则为准；
- 代码操作遵守 `.cursor/rules/multi-session-protection.mdc`；
- 仓库路由引用 `agent-delivery/repo-registry.yaml`；
- 当前 Demo 阶段采用 deny-by-default 的 B 语义：base policy 只限定 environment/host/database/schema，run scope 再逐表授权；`demo_gkxlumenx_ods/dwd/ads/dim` 和当前作为 Demo 使用的 `gkxlumenx_cms` 都必须逐表命中且有确认证据；其他写入默认拒绝；
- 这是有记录的限时例外，不宣称与 D16/D18 无冲突；涉及架构硬规则时保留批准记录，否则进入 `BLOCKED`；
- 上线通知到达后创建不可变 production policy，禁止 Mock 写入，并使旧 gate 失效；
- `进入开发`只授权修代码、推独立 fix 分支和 Draft MR；
- `提测`才授权合并 dev、push、CI/CD 和 dev rollout；
- 接管只认完整消息 `接管【auto_number】`，且接管不解锁任何 gate；接受风险、继续、你看着办等自然语言同样不解锁；
- Skill 与 `.cursor/rules/fe-manual-confirm-push.mdc` 必须在同一发布步骤更新；修改后者前必须再次获得用户对 2026-11-05 推送裁定的确认。

## P0 边界

包含：

- 单缺陷状态机；
- 三个精确人工门：开发、提测、验收；
- 飞书人工验收落点；
- S/M/L 分级；
- gate 绑定、失效和接管；
- 结构化证据、单一报告和内部校验器；
- 版本化数据/Mock 策略；
- 单缺陷 Bundle gate（支持多仓候选 SHA、依赖顺序和统一提测）、deployed SHA、review/data scope hash、failure_stage/failure_class 和 revert-only 回退；L 由现有长任务流程承接；
- `state.json.transitions[]`、`patch_round`、cycle 归档、精确接管、取消和重开规则；
- `policies/` 的版本化数据授权和 run scope 逐表确认；
- Codex / Cursor / Trae 共用语义。

不包含：

- 自研 Agent Runtime；
- 自动轮询飞书；
- Webhook、队列和常驻 Runner；
- lease TTL、心跳和无人值守恢复；
- 自动合并或绕过人工验收；
- 生产自动部署；
- 所有缺陷强制启用长任务、提交考古或覆盖率门槛。

## 当前实施入口

```bash
node .cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs --help
node .cursor/skills/feishu-bugfix/scripts/bugflow-state.selfcheck.mjs
node .cursor/skills/feishu-bugfix/scripts/revalidation-plan.selfcheck.mjs
```

Agent 内部按 `init（CLAIMED 需带 claim-comment-ref/claim-operator）→ record-diagnosis → record-plan → set-repos（多仓时每仓带 role/depends_on/ship_order）→ set-data-scope → approve-gate enter_dev → advance → check-data-write（有 DB 写时）→ record-evidence → verify-repo → record-review → record-verification（基础 fix/regression；M/L 追加适用类别）→ verify-evidence → advance READY_SHIP → approve-gate ship → advance SHIPPING → record-ship-package → verify-evidence → advance DEV_VERIFYING → advance AWAITING_ACCEPTANCE → exact 验收通过 → approve-gate acceptance → transition_state RESOLVED → record-acceptance(mode=chat_exact) → advance RESOLVED → render-report` 使用脚本；`record-ship-package` 在提测授权后的合并/部署阶段记录实际 merge/deployed SHA、pipeline 和 rollout，并自动重跑 evidence 校验。`block`、`cancel`、`reopen`、`takeover` 负责旁路。

v1.2 起，校验器在原有 claim、数据、验证、跨仓 Bundle 约束上增加第三个精确 `acceptance` gate；chat_exact 验收必须绑定当前 ship gate、dev 验证结果和已验证 evidence manifest，并在飞书迁移成功后才能进入 `RESOLVED`。pipeline/rollout 仍来自 GitLab 查询记录，不能伪装成本地脚本直接验证的远端事实。普通同事仍是四件事，但口令为 `进入开发`、`提测`、`验收通过` 三个精确词。

详细设计见 [`P0-DESIGN.md`](P0-DESIGN.md)。

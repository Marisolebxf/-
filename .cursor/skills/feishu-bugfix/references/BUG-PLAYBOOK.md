# 通用缺陷处理手册

本手册只解决两个问题：**先找依据，再按问题类型选择验证方式**。不要把所有缺陷都套成同一种前端流程，也不要用截图或模型猜测替代主仓事实。

## 1. 事实源发现顺序

开工后先定位事实源，再读代码。至少命中与本次缺陷相关的一类来源：

| 问题 | 首选事实源 |
|---|---|
| 仓库、服务、CI、dev URL、部署方式 | `agent-delivery/repo-registry.yaml`、`agent-delivery/paths.yaml`、业务仓 `.gitlab-ci.yml` |
| 业务需求、范围、背景 | `agent-delivery/bid-reference/**`、`agent-delivery/工程过程/**` |
| SRS、正式验收条件 | `agent-delivery/验收文档/**`、`agent-delivery/formal-docs-registry.yaml` |
| UI 规范、页面骨架、组件规范 | `agent-delivery/Design.md`、`agent-delivery/Design-mobile.md` |
| 数据口径、血缘、可用性、数据库 | `agent-delivery/data/**`、`agent-delivery/data-source-mapping-registry.yaml`、`agent-delivery/data-lineage-policy.md`、`agent-delivery/数据库设计.md` |
| 测试用例、历史缺陷、代码归属 | `agent-delivery/qa/**` |
| 编码、权限、推送、长任务规则 | `.cursor/rules/**`、业务仓 `AGENTS.md`、业务仓 `docs/**` |

规则：

1. 缺陷描述、评论、截图都只是现象证据；**期望行为必须能落到主仓文档、既有实现契约或最新人工裁定**。
2. 最新人工裁定与正式文档冲突时，记录冲突和裁定人；不能默默选一个。
3. 找不到任何依据时，不要猜需求。带着已查来源和缺口向用户提一个阻塞问题。
4. `requirement_refs` 必须写出实际路径、章节、接口名、测试用例 ID 或飞书评论锚点，禁止只写“需规要求”。

## 1.1 需规功能点覆盖卡

项目以主仓 SRS 为功能验收真源。每个缺陷必须至少建立一条“功能点 → 实现面 → 验证行为”的映射：

```text
功能点：agent-delivery/bid-reference/srs/...md#序号/五级路径
实现面：页面 / 组件 / 接口 / 数据查询
期望行为：需规原文中的可观察结果
覆盖验证：命令、DOM/API/数据断言或人工步骤
关联回归：同功能点的其他模式 / 相邻功能
```

规则：

- 不能只写“需规要求”；必须写清 SRS 文件、序号和五级功能路径。
- 一个缺陷涉及多个功能点时全部列入，不允许只覆盖截图中的单一分支。
- 需规里的 `全部/仅/默认/支持/禁止` 等量词必须转成测试断言或明确的验收步骤。
- 功能点包含切换、缩放、分页、空态、权限或多视图时，修复验证要覆盖受影响的所有模式。
- 找不到 SRS 功能点时，才使用正式验收文档、QA 用例或最新人工裁定；三者都没有就阻塞。

## 2. Bug Contract

在写代码前形成下面七项。可以写入 `record-diagnosis` 的字段中，不必新增文件：

```text
现象：用户看到什么，在哪里，何时出现
期望：可执行、可观察的结果；明确“所有/仅/默认/不得”等量词
范围：页面、接口、服务、仓、表、权限
需规：SRS 文件、序号、五级功能路径；必要时列多个功能点
非目标：本次明确不修什么
依据：主仓文档/需规/QA 用例/最新人工评论
验证：复现步骤 + 修复后如何机器验证
```

无法写清“期望”“范围”或对应需规功能点时，停在 `READY_DEV` 之前，不进入编码。

## 3. 类型路由

只加载与当前缺陷类型相关的小节，不要全量套模板。

### UI / 交互 / 图表

- 优先本地 dev server + mock/固定数据；必要时用真实接口，但开发循环不反复跑共享 dev。
- 机器断言优先于截图：DOM 数量、组件状态、ECharts option、请求路径、错误日志。
- 画布图必须检查真实的运行时 option，而不是只 grep 源码。
- 必须覆盖目标区域和可视区外内容；不要只验证首屏。
- 截图最多一张，作为最终人工辅助证据，不作为唯一验证。
- 回归至少覆盖：默认态、目标态、空/无数据态、切换或重复操作。

### API / 业务逻辑

- 先确认接口契约、错误码、权限边界和调用方。
- 用一个失败测试或最小请求复现，再改实现。
- 验证成功响应、业务错误、非法输入、鉴权/越权、幂等或重复提交（如适用）。
- 不通过页面“看起来正常”替代 API 断言。

### 数据 / SQL / ETL

- 先读 `data-lineage-policy.md`、datasource registry 和 run scope。
- 用只读查询确认现状；任何写入前必须走 `check-data-write`。
- 验证口径、边界日期、空值、重复/幂等、事务性、回滚或补数方案。
- 证据必须记录库/schema/表、只读或写入模式、账号引用和查询摘要；禁止打印密码。
- Demo mock 也必须命中 policy 和 scope；优先窄表、最小行数、可清理。

### 3.1 数据缺失类缺陷（“页面没有数据/少模块/少指标”）

先证明数据到底在哪一层丢的，再改代码：

1. **接口真实返回**：直接调用算法/后端接口，记录 URL、HTTP 状态、关键字段和样本值。
2. **前端空态/映射**：检查 `buildNoSourceOption`、normalize、字段名、条件分支和硬编码 fixture。
3. **后端投影**：检查 Controller/Service 是否丢弃、改名或只在特定分支返回字段。
4. **数据源缺口**：只有前三步都排除后，才判数据缺口；记录具体表/字段/覆盖率依据。
5. **需规逐项核对**：需规列出的每个子模块/指标都要有“已展示 / 明确缺口 / 不适用”的结论；禁止只修一个图就宣称合规。

要求：此类缺陷在 `record-diagnosis` 中必须写明“接口返回结论”和“前端/后端丢数位置”，并在验证矩阵中覆盖每个需规子项。

### 算法 / 模型

- 固定输入数据集和随机种子，验证可重复输出。
- 记录 golden case、关键指标、阈值和失败样例；性能问题必须记录输入规模和耗时。
- 不在没有 benchmark 的情况下用“响应变快了”作为结论。

### 配置 / 发布 / CI

- 先做 diff 和 dry-run；确认影响环境、服务和回滚命令。
- 失败先看 pipeline/job/rollout 具体日志，区分代码失败、基线失败、runner 卡死和部署失败。
- 同一种环境故障重试一次；再次失败即 block，不计入代码修补轮次。

### 权限 / 安全

- 使用最小角色做正反例：有权限成功、无权限拒绝、越权不可绕过。
- 不打印 token、cookie、签名 URL、密钥或个人信息。

### 跨仓 Bundle

- 同一个飞书缺陷涉及多个代码仓库时，仍保持一个 Bug、一个 claim、一个 run、一套验收标准，不拆成多个飞书缺陷。
- `state.repos[]` 每个仓记录 `role`、`depends_on`、`ship_order`；风险至少为 M，跨仓本身不再自动升级为 L。
- 每仓分别执行 `fix + regression` 和适用的非 happy-path 验证；另需一条覆盖完整 Bundle 的 `integration` 验证。
- 按 `ship_order` 合并和部署，被依赖仓先于消费仓；任一仓失败则整个 Bundle 进入返工或失败态。
- Bundle 不是跨仓原子事务，回滚仍按仓记录，但必须使用同一 run 和同一提测结论。

### 未知问题

- 改表结构、权限模型、生产数据或无法定位层：按风险升级；若达到 L，路由现有长任务流程。
- 未知类型最多做 20 分钟低成本取证；仍无法分层就 block，并列出下一步要谁提供什么。

## 4. 预检

在任何业务代码修改前完成：

1. 确认最新目标分支 SHA、工作区和远端状态。
2. 查最新 dev pipeline。基线为红时，先判断它阻断的是“本地开发”还是“提测部署”：
   - 无关且与缺陷路径不相交，本地能复现/验证目标行为：记录 repo/SHA、失败 job、owner 和 URL 为未关闭的 ship blocker；允许本地开发和定向验证，不把失败算成当前补丁轮次；
   - 无关但会阻断目标复现、类型检查/构建或必需的全量验证：暂停开发并记录同一组证据；
   - 当前范围失败：继续诊断；
   - 无论前两类哪一种，`READY_SHIP`/`提测` 前必须等目标分支成功流水线；禁止在已知红的基线上合并部署后声称已提测。
3. 确认依赖、登录和本地启动条件可用。
4. 确认没有另一个 active run 或未接管 claim。
5. 检查 `AGENTS.md` 和中心规则中与本仓相关的硬约束。

## 5. 验证矩阵

每个仓至少需要：

- `fix`：目标缺陷从失败变通过；
- `regression`：相邻路径不被破坏。

按缺陷类型追加，不要求全部出现：

- `boundary`：空值、零值、极端输入、时间边界、切换；
- `integration`：接口/页面/服务契约；
- `data`：口径、幂等、回滚、数据授权；
- `algorithm`：golden case、指标、性能；
- `security`：越权、鉴权、敏感信息；
- `performance`：延迟、吞吐、资源；
- `rollback`：配置或部署可恢复。

S 级允许只有 `fix + regression`；M/L 必须有至少一个非 happy-path 类别。只记录可复核结果，不把自由文本“看起来正常”记为 PASS。

## 6. 评审深度

- S：修改者自审 + 相关测试；不默认起独立 review。
- M：一次独立、针对 diff 的 review；解决 blocker 后复审即可，不无限循环。
- L：按长任务规约执行全量评审。
- 跨仓 Bundle：风险至少 M，每仓独立评审；Bundle 再执行覆盖完整的 integration 验证。

## 7. 时间盒与止损

- S：从 contract 到 dev 部署目标 30–60 分钟。
- M：目标 1–2 小时。
- 超过预算时先刷新 blocker，不继续无目的重建、截图或改代码。
- 同一环境/CI 故障连续两次无进展：block。
- 同一缺陷最多 3 个补丁轮次；超过后进入 L/unknown 路由。

## 8. 返工规则

- 验收失败但范围不变：保留 claim 和已核实的业务依据，直接修；重新做 diff/review/verification，只需重新 `提测`，不重复 `进入开发`。
- 新增仓、调整 Bundle 依赖顺序、数据写入、权限模型、生产或 L 级：旧 gate 失效，重新确认；L 路由长任务，其他情况继续同一 Bundle。
- 基线失败不属于当前补丁轮次，不得用它增加 `patch_round`。

## 9. 远端并发 push 后的复验

已经在候选分支完成过一次完整本地验证后，远端目标分支又前进时，不要机械地重跑全部命令。先运行：

```bash
node .cursor/skills/feishu-bugfix/scripts/revalidation-plan.mjs \
  --repo-dir <repo> --candidate-ref <sha> --remote-ref origin/dev \
  --remote-pipeline-status success --premerge-checks-passed --json
```

决策规则：

| 决策 | 条件 | 本地动作 |
|---|---|---|
| `no_revalidation` | 候选已在远端 | 不重建，继续观察远端流水线 |
| `targeted` | 远端 pipeline 绿、无冲突、文件与候选不重叠且不涉及共享契约 | `git diff --check` + 目标测试；类型/构建交给 CI |
| `full` | 文件重叠，或远端修改 `package/lock/tsconfig/vite/.gitlab-ci/AGENTS/src/config/api/types/stores/router`，或 pipeline 状态未知 | 重新跑目标测试、type-check、build |
| `block` | 远端基线 pipeline 红 | 停止并找基线负责人，不计当前补丁轮次 |

“不重叠”不等于“同目录就安全”。判断依据是实际 changed files 和敏感共享文件；只要对本修复的依赖关系没有把握，选择 `full`。

补充：候选已推送后，若后续 dev 的新 pipeline 已包含候选且出现首个 terminal success（pipeline + deploy/rollout），即可停止等待该仓，不需要因为 dev 继续前进而重新 merge/rebuild；只有候选尚未进入远端、或后续改动与候选文件重叠时才重新走 targeted/full。

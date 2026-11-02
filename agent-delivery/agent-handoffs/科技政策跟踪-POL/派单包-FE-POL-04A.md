# 派单包 · FE-POL-04A 智能政策库构建（政策数据治理）— 整页复刻

> 认领：已 task-claim（agent:frontend-agent，监管 human:孔东）→ 开工 `task-update-status in_progress`
> 工作区：**仅在此 worktree 作业**：`D:\web\gkx-lumen\worktrees\lumen-ui-science-pc--pol04-governance`（分支 `feat/pol04-governance`，基点 f4edea4，node_modules 已 junction，.env 已复制）
> 强度：ponytail full
> 本单为**独立窗口并行任务**：禁止触碰 pol03/05/06/07 worktree、主工作区与其他仓；本 worktree 内只改本单文件

## 1. 真源与范围

- 需规：SRS `政策对比功能升级（核增需求）/` 政策数据治理 4 叶（excel 617–620 区段）
- demo 真源（只读对照，禁 import/merge）：`repos/demo-ui-science/src/pages/policy-tracking/PolicyPcPages.jsx` 的 `PolicyGovernance` 段（L231–691）+ `policyPcData.js`（955 行共享种子）+ `PolicyPcPages.css`（158）
- lumen 落点：`src/views/policy/governance/`（S01 页壳已建，本单填充整页；样式抽 `src/views/policy/styles/demo-policy-pc-pages.css`——**S01 已建此文件，扩展勿覆盖既有类**）
- 菜单名「智能政策库构建」与 SRS 分册名「政策数据治理」为同页双名（规划 D1）；路由已挂接（勿改 menu.ts）
- **ChainSteps 页间导航（治理→拆解→对比→研报）由本单首装**：建 `src/views/policy/components/PolicyChainSteps.vue`（vue-router push 串联，替换 demo `onTopicChange`）——本组件是 05/06/07 的共享依赖，**接口设计务必通用**（props: 当前 topic key + 深链 query 语义）

## 2. S01 基座已提供的接口（必读，禁止重造）

- 数据：`fetchPolicyGovernance({})`（@/api/policy，双轨）；`createGovernanceDataset()`（@/mock/modules/policy）
- 种子（policyPcSeed.ts 已冻结，禁改动）：`governanceKpis` / `governanceBatches` / `cleanRules` / `structureTaxonomy`（Tree 数据）/ `fieldMappings` / `traceIndexRows` / `BASE_READY_KEY` / `loadBaseReady()` / `saveBaseReady()` / `loadFlag()` / `saveFlag()` / `inTimeWindow()`
- 公共件：`PageTabFrame` / `PolicyStatCard`+`PendingBadge` / `MockBadge` / `useReviewStore` / `usePolicyTrack`

## 3. 交付要点（DoD 对照）

1. **治理 3 Tab**：数据清洗（cleanRules 规则表 + 执行状态）/ 结构分类（structureTaxonomy，`a-tree` 展示）/ 血缘追踪（traceIndexRows + trace/review 动作按钮）
2. **治理 KPI**（governanceKpis，PolicyStatCard 语义 + D9 ⓘ/🧪）+ **基库构建开关**（loadBaseReady/saveBaseReady localStorage 持久化 + 进度闸门：基库未就绪时下游能力置灰语义）+ **批次管理**（governanceBatches + inTimeWindow 窗口过滤）
3. **分轨横幅**（BoundaryBanner 语义照搬）：与专题服务系统 `/policy/*`、门户 `/policy-portal/*` 分轨提示；评审层**集中管理**（`useReviewStore` + 组件自闸）+ 评审模式关闭后 DOM 零泄漏（D8）
4. ChainSteps 接入（见 §1）；共享 policyPcSeed 种子消费，**不自建种子**
5. demo 原生控件全换 Arco；D9 ⓘ/🧪；QPOL 🟡 ⚠️

## 4. 闸门与交付

- **完工停本地 worktree，严禁自动 commit/push**；handoff 写 `agent-delivery/agent-handoffs/科技政策跟踪-POL/FE-POL-04A.md`（gkx-orchestration 主工作区）；`task-update-fields` 回填
- 三绿在本 worktree 执行
- 冲突预防：只改 `src/views/policy/governance/**` + `styles/demo-policy-pc-pages.css`（追加）+ 新建 `components/PolicyChainSteps.vue`；禁改 menu.ts / api / 种子 / 既有公共件
- **PolicyChainSteps 是 05/06/07 共享件**：本单交付后组件即冻结接口；05/06/07 派单包已声明消费它，接口变更须走 coordinator

# 派单包 · FE-POL-03A 政策效果推演 — 整页复刻（双工作台）

> 认领：已 task-claim（agent:frontend-agent，监管 human:孔东）→ 开工 `task-update-status in_progress`
> 工作区：**仅在此 worktree 作业**：`D:\web\gkx-lumen\worktrees\lumen-ui-science-pc--pol03-simulation`（分支 `feat/pol03-simulation`，基点 f4edea4，node_modules 已 junction，.env 已复制）
> 强度：ponytail full
> 本单为**独立窗口并行任务**：禁止触碰 pol04/05/06/07 worktree、主工作区与其他仓；本 worktree 内只改本单文件

## 1. 真源与范围

- 需规：SRS `科技政策跟踪/` 政策效果推演 11 叶（excel 235–245）
- demo 真源（只读对照，禁 import/merge）：`repos/demo-ui-science/src/pages/policy-tracking/`：`PolicySimulation.jsx`（165 壳）+ `simulation/estimate/EstimateWorkbench.jsx`（867）+ `simulation/interpret/InterpretWorkbench.jsx`（727）+ `simulation/sharedCharts.jsx`（1161）+ `PolicySimulation.css`（467）
- lumen 落点：`src/views/policy/simulation/`（S01 页壳已建，本单填充整页；样式抽 `src/views/policy/styles/demo-policy-simulation.css`）
- 路由：已挂接（勿改 menu.ts）

## 2. S01 基座已提供的接口（必读，禁止重造）

- 数据：`fetchPolicySimulation({})`（@/api/policy，双轨）；`createSimulationDataset()`（@/mock/modules/policy）
- 种子（policySeed.ts 已冻结，禁改动）：`simulationIndicators` / `simulationScenarios` / `policySimulationParams` / `regionalSimulationData` / `regionalEconomicSimulation` / `interpretationReportDraft`（estimatedEffects 等）
- 公共件：`PageTabFrame` / `PolicyStatCard`+`PendingBadge` / `MockBadge` / `useReviewStore` / `usePolicyTrack` / `ensurePolicyMaps`（mapRegistry）；复刻经验清单 + 仓 AGENTS.md 开工必读

## 3. 交付要点（DoD 对照）

1. **2 主 Tab**（DEC-DS12）：estimate 效果预估工作台 / interpret 科技政策推演工作台
2. **EstimateWorkbench**（867 行语义）：产业影响图随「新出台政策」Select 缩放 / 创新预测序列 / 区域政策类型聚合 / 四项识别（产业/创新/区域/综合 四维卡）+ 页头综合分闸门（`dimsEvalDone` 语义：四项全评估才亮综合分）；**档 A #17–23 能力保留**
3. **InterpretWorkbench**（727 行语义）：政策文本选择（textType 三态）/ 非导图图表 / 政策覆盖面 / 历史路径；**档 A #24–27 + 档 C T44 闸门语义保留**
4. **sharedCharts（1161 行）图表族**：全走仓内 VChart（`@/config/echarts` 按需注册，新图型先查再补）；**T43 闸门**（estimate 侧就绪开关）评审门控 + 默认开
5. **D2 决策**：demo `BTN_DS_SIMULATE` L2 权限试点**不复刻**——推演按钮常可用，不走级别锁
6. 图表容器显式高度防 0 高死锁（双工作台 Tab 切换高发）；v-if 挂载切换 + flex 容器加 `flex:0 0 auto` 定高
7. 状态机自检：`policyWorkbenchTabs.test.mjs` 断言语义最小移植 → `FE-POL-03A.test.mjs`
8. D9：每个统计数字 ⓘ/🧪；QPOL 🟡 项 ⚠️ 角标（PendingBadge）

## 4. 闸门与交付

- **完工停本地 worktree，严禁自动 commit/push**；handoff 写 `agent-delivery/agent-handoffs/科技政策跟踪-POL/FE-POL-03A.md`（gkx-orchestration 主工作区，不在本 worktree）；`task-update-fields` 回填
- 三绿（type-check/自检/build）在本 worktree 执行
- 冲突预防：只改 `src/views/policy/simulation/**` + `src/views/policy/styles/demo-policy-simulation.css`；禁改 menu.ts / api / 种子 / `components/` 公共件（需扩展时 note 登记 + handoff 说明）

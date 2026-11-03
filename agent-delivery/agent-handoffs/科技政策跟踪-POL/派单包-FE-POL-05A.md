# 派单包 · FE-POL-05A 智能政策拆解 — 整页复刻

> 认领：已 task-claim（agent:frontend-agent，监管 human:孔东）→ 开工 `task-update-status in_progress`
> 工作区：**仅在此 worktree 作业**：`D:\web\gkx-lumen\worktrees\lumen-ui-science-pc--pol05-parse`（分支 `feat/pol05-parse`，基点 f4edea4，node_modules 已 junction，.env 已复制）
> 强度：ponytail full
> 本单为**独立窗口并行任务**：禁止触碰 pol03/04/06/07 worktree、主工作区与其他仓；本 worktree 内只改本单文件

## 1. 真源与范围

- 需规：SRS `政策对比功能升级（核增需求）/` 智能政策拆解 4 叶（excel 617 区段）
- demo 真源（只读对照，禁 import/merge）：`repos/demo-ui-science/src/pages/policy-tracking/PolicyPcPages.jsx` 的 `PolicyParse` 段（L692–1051）+ `policyPcData.js` 共享种子
- lumen 落点：`src/views/policy/parse/`（S01 页壳已建，本单填充整页；样式入 `styles/demo-policy-pc-pages.css`——**04A 也在追加此文件，本单只加 `pol-parse-` 前缀类**，避免类名冲突）
- 路由已挂接（勿改 menu.ts）

## 2. S01 基座 + 04A 并行件

- 数据：`fetchPolicyParse({})`（@/api/policy，双轨）；`createParseDataset()`（@/mock/modules/policy）
- 种子（policyPcSeed.ts 已冻结，禁改动）：`parsePolicies` / `planningMetricLib` / `alignMetricsToLib()` / `entityCompleteness()` / `intensityFromMetrics()` / `ENTITY_CATS`
- **PolicyChainSteps**（04A 首装共享件）：`src/views/policy/components/PolicyChainSteps.vue`——**04A 与本单并行，交付时若该组件尚不存在，本单临时内联同语义占位（topic='parse' 高亮）并在 handoff 登记，04A 合并后替换消费**；勿在本单自建正式版造成双实现
- 公共件：`PageTabFrame` / `PolicyStatCard` / `MockBadge` / `useReviewStore` / `usePolicyTrack`

## 3. 交付要点（DoD 对照）

1. **政策选择器**（parsePolicies）+ 政策文本展示（textType 地方/国家/海外三态渲染）
2. **四能力 Tab**（DECOMPOSE_CAPS 描述照搬）：semantic 语义理解 / clause 条款精细化拆解 / metric 关键指标提取 / entity 政策实体关联
3. **条款树**：`a-tree` 递归渲染 clauses + **5 类条款色标**（CLAUSE_TYPE_COLOR 语义）+ collectClauseTypes 聚合标签
4. **关键指标提取**：METRIC_KIND_ORDER 四类（量化指标/补贴标准/资质要求/时间节点）指标集 + **alignMetricsToLib 对齐指标库就绪闸门**（planningMetricLib 未就绪时提示对齐缺口）
5. **KG 绑定开关**（kgBound）+ metricLibReady 联动基库（loadBaseReady——与 04A 基库开关联动语义，读同一 localStorage KEY）；实体关联展示（entityCompleteness + ENTITY_CATS 四类）
6. **空态闸门**：无政策/无文本/无条款 → 分层 Empty（hasPolicy/hasText/hasClauses 三级，档 C 闸门语义）
7. demo 原生控件全换 Arco；D9 ⓘ/🧪

## 4. 闸门与交付

- **完工停本地 worktree，严禁自动 commit/push**；handoff 写 `agent-delivery/agent-handoffs/科技政策跟踪-POL/FE-POL-05A.md`（gkx-orchestration 主工作区）；`task-update-fields` 回填
- 三绿在本 worktree 执行
- 冲突预防：只改 `src/views/policy/parse/**` + `styles/demo-policy-pc-pages.css` 追加 `pol-parse-` 前缀类；禁改 menu.ts / api / 种子 / 04A 的 governance 目录与 ChainSteps 正式件

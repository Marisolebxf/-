# FE-POL-04A · 智能政策库构建（政策数据治理）整页复刻（核增 4 叶）— 治理 4 Tab + KPI + 基库构建开关 + ChainSteps 首装

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull`（派单包认领） |
| 说明 | 独立窗口并行任务；仅作业于 worktree `lumen-ui-science-pc--pol04-governance`（分支 `feat/pol04-governance`，基点 f4edea4）；未触碰 pol03/05/06/07 worktree 与主工作区 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单 `/goal` 一致；未用 YAGNI 跳过 D8 评审层/D9 角标/D10 交互、可观测埋点与架构铁律；Arco 优先（demo antd 全换 Arco 对应件）、第二处出现即封装（ChainSteps 抽共享件）、样式只追加不覆盖 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 |

## 交付范围与实现（DoD 对照）

### 1. 治理 4 Tab（demo L329-588 WorkbenchTabs items 全语义；派单包 DoD「治理 3 Tab」按 demo 现状实为 4 Tab——清洗/结构化/溯源/指标库，demo 段 L568-589 含 `metricLib` 第 4 Tab）

`src/views/policy/governance/index.vue`（S01 占位壳替换为整页，563 行），子页签容器 `PageTabFrame`（03A EstimateWorkbench 同款先例）：

- **clean 系统引用政策源数据清洗**：质量校验规则表（`cleanRules` 6 规则 + processing Tag）＋ 批次明细表（`governanceBatches` 3 批次 + 成功/部分状态 Tag；「作业状态只读」extra）。
- **struct 政策库结构化**：info Alert（统一管理·快速检索·高效调用·破孤岛）＋ 分类标签体系**树表**（`structureTaxonomy`，`default-expand-all-rows` + 可控 `expanded-keys`，Arco table 树形数据 children 语义）＋ 元数据规范·字段映射规则表（`fieldMappings` 8 映射，横向滚动 x:900）＋ 结构化政策快速检索（baseReady 闸门：就绪 = `a-input-search` 四字段包含匹配 `parsePolicies` 共享；未就绪 = `a-empty`「未转化为结构化数据，不可快速检索政策数据」）。
- **trace 溯源索引构建**：原文↔条款↔结论关联索引表（`traceIndexRows`）＋ 3 动作：**查证**（`Message.info` 定位洞察 + push 研报页，demo L534-537 语义）/**溯源**/**复核**（Modal：索引节点/原文/条款/结论/关联洞察/权威数据源 Tag/URL 外链；复核含 TextArea 说明 + 提交，溯源含路径描述行；`popup-container="body"` + `unmount-on-close`）。
- **metricLib 规划指标库搭建**：标准化政策指标库表（`planningMetricLib`，扶持力度/适用范围/实施时效/申请条件四维，x:960）。

### 2. 治理 KPI + 基库构建开关 + 批次管理（DoD-2）

- **KPI 行**（grid 5 列）：库内政策数（3256 份，`M_POLICY_TOTAL_COUNT` ⓘ）＋ `governanceKpis` 四子能力透传（源数据清洗首卡带 `M_POLICY_VALIDITY_RATE` ⓘ + `QPOL-01` ⚠️ PendingBadge）；全部走 `PolicyStatCard`（D9 ⓘ/🧪/⚠️ 语义内置）。
- **基库构建开关**：头部「底座就绪演示」`a-switch` → `loadBaseReady()`/`saveBaseReady()` 持久化（**sessionStorage**，S01 冻结种子实现；派单包写 localStorage 属笔误，见偏离说明①）；开关翻转埋 `base-ready-toggle` 埋点。
- **进度闸门**（demo L318/498/667 三处冻结语义）：未就绪 → KPI 降档 `max(40, v−28)` 橙色、快速检索 GateEmpty、页脚去拆解/去对比/去研报三按钮 + ChainSteps「下一步」禁用、未就绪原因提示文案。
- **批次管理**：`governanceBatches` 批次表（见 Tab1）。⚠️ 派单包 DoD 提及 `inTimeWindow` 窗口过滤——demo 治理段评审稿**未实现**批次时间窗过滤（`inTimeWindow` 实际消费在 06 对比页 L1079）；按「对齐已评审页」铁律不擅自加窗，见偏离说明②。

### 3. 分轨横幅 + 评审层（DoD-3；D8）

- **BoundaryBanner 语义照搬**（demo L132-148）：「科技信息展示系统 · 智能政策库构建（DS-PC-01）+ 与专题服务系统 /policy/*、智慧服务门户 /policy-portal/* 分轨 + 对比对象仅存展示侧会话槽，禁止写入专题系统对比篮」。
- **评审层集中自闸**：头部评审行/分轨横幅/底座 Alert/页脚提示 4 处 `v-if="review.reviewMode"`；ChainSteps/MetricSpecTrigger/PendingBadge 组件自身自闸；关闭评审模式后治理页 DOM 零泄漏（业务态只留标题/KPI 数字/4 Tab/表格/页脚导航）。

### 4. ChainSteps 页间导航首装（DoD-4；接口冻结件）

`src/views/policy/components/PolicyChainSteps.vue`（**05/06/07 共享依赖，接口即冻结**）：

- **props**：`current: PolicyChainNode`（governance/parse/compare/report）｜`next?: PolicyChainNode | ''`（不传不渲染按钮）｜`nextDisabled?: boolean`｜`query?: Record<string,string>`（深链 query 透传，push 时并入目标路由）。
- **导出**：`POLICY_CHAIN_NODES`（key/step/routeName/menu 四元组，route name 与 menu.ts 核增 4 菜单一一对应）＋ `PolicyChainNode`/`PolicyChainNodeMeta` 类型。
- **行为**：`router.push({ name, query })` 替换 demo `onTopicChange`（pageRouting.js 菜单双名映射收敛为 route name）；`navigate` 事件通知页面联动（不阻止跳转）；统一 `chain/goto` 埋点；评审层自闸。
- 治理页接入：`<PolicyChainSteps current="governance" next="parse" :next-disabled="!baseReady" />`。

### 5. 种子共享消费（DoD：不自建种子）

`governanceKpis`/`governanceBatches`/`cleanRules`/`structureTaxonomy`/`fieldMappings`/`traceIndexRows`/`planningMetricLib`/`parsePolicies`/`loadBaseReady`/`saveBaseReady` 全部从 S01 冻结种子与 `createGovernanceDataset()` 透传消费；页面零种子字面量（自检 §5 断言）。首屏同步初值 `ref(createGovernanceDataset())` 防白屏；`fetchPolicyGovernance` 双轨（USE_MOCK=false 契约未冻结显式报错不挡页）。

### 6. Arco 化 + D9 + 观测

- demo antd 全换 Arco：`Statistic/Card/Row/Col/Table(Tag 渲染)/Tabs(WorkbenchTabs→PageTabFrame)/Steps/Modal/Descriptions/Alert/Switch/Input.Search/Empty` → `PolicyStatCard/a-table slotName/a-steps/a-modal+a-descriptions/a-alert/a-switch/a-input-search/a-empty`；图标显式 import（IconStorage/IconArrowRight/IconSwap/IconFile）。
- D9：每个统计数字旁 ⓘ（PolicyStatCard 内置 MetricSpecTrigger 读模块镜像）+ 🧪 MockBadge（6 卡位）+ QPOL-01 ⚠️ PendingBadge。
- 观测：`usePolicyTrack` 5 事件（page-mounted/tab-change/base-ready-toggle/trace-action/goto/chain goto）。

### 7. DoD 逐条对照

| # | DoD 条目 | 状态 |
|---|---------|------|
| 1 | 治理 3 Tab（实为 demo 4 Tab）复刻 | ✅ clean/struct/trace/metricLib 全语义 |
| 2 | KPI + 基库开关持久化 + 进度闸门 + 批次管理 | ✅ 见 §2（`inTimeWindow` 偏离见②） |
| 3 | 分轨横幅照搬 + 评审层集中 + 零泄漏 | ✅ 见 §3 |
| 4 | ChainSteps 接入（vue-router push，接口通用） | ✅ 共享件冻结，见 §4 |
| 5 | 共享 policyPcSeed 种子消费，不自建 | ✅ 自检 §5 |
| 6 | demo 原生控件全换 Arco；D9 ⓘ/🧪；QPOL ⚠️ | ✅ 见 §6 |
| 7 | 截图比对五件套 | ⏸ 转人工验收（worktree 无预览环境，同 03A 先例） |

## 偏离说明（对派单包）

1. **持久化实现**：派单包写「localStorage 持久化」；S01 冻结种子 `loadFlag/saveFlag` 实现为 **sessionStorage**（`policyPcSeed.ts` L851-875，demo 同源）。种子禁改，按种子语义交付；浏览器会话级持久化，刷新保留、关标签页重置——与 demo 评审稿行为一致。
2. **`inTimeWindow` 批次窗口过滤未实现**：派单包 DoD「批次管理（governanceBatches + inTimeWindow 窗口过滤）」；demo 治理段（L251-263 批次表列定义）**无时间窗过滤**，`inTimeWindow` 实际消费在 06 多维对比页（scoredPolicies L1079）。按 demo→lumen 复刻铁律「对齐已评审页、禁止以更简/更繁另起一套」不擅自加窗。06 单如需窗口语义由该单消费同一冻结函数，无重复实现。

## 问题清单

- 无阻塞问题。`pnpm type-check`/`pnpm build` 前置钩子的 workspace hoist 告警为 worktree junction 环境预存（03A handoff 同记录），不影响三绿。

## 修改内容

worktree `D:\web\gkx-lumen\worktrees\lumen-ui-science-pc--pol04-governance`（分支 `feat/pol04-governance`，基点 f4edea4；**2026-11-03 经监管人指示合并至本地 dev（commit `352717d`，fast-forward），临时分支与 worktree 已清理**）：

- `src/views/policy/governance/index.vue`（改：S01 页壳 33 行 → 整页 563 行）
- `src/views/policy/components/PolicyChainSteps.vue`（新：共享页间导航，接口冻结件）
- `src/views/policy/governance/FE-POL-04A.test.mjs`（新：22 组断言自检）

**冻结边界遵守**：menu.ts / api/policy.ts / 全部 mock 种子 / `styles/demo-policy-pc-pages.css`（@import 消费未改）/ 既有公共件（PolicyStatCard/PendingBadge/PolicyMetricSpecTrigger/MockBadge/PageTabFrame）零改动（`git status` 核对空）。

## 测试结果（三绿 + 回归）

worktree 根执行（2026-11-03 合并后在主仓 dev `352717d` 复跑，同样全绿）：

```
node src/views/policy/governance/FE-POL-04A.test.mjs   # 22 组断言全绿
node src/views/policy/policy.test.mjs                  # 基座回归绿
pnpm type-check                                        # vue-tsc --build 通过
pnpm build                                             # vite build exit 0（4077 modules，49.65s）
```

修复记录（type-check 8 错 → 0）：
1. 种子 `@ts-nocheck` 无 `TraceIndexRow` 类型导出 → 页内定义 `TraceRow` 本地形状契约（字段=demo traceIndexRows）。
2. Arco `TableColumnData` 无 `key` 字段（antd 习惯残留）→ 删 6 处 `key:`，统一 `dataIndex`/`slotName`。

## 遗留风险

- **截图比对五件套转人工验收**（同 03A 先例）：worktree 无预览环境；建议人工验收时主工作区合并后 `pnpm dev` 对照 demo「智能政策库构建」页逐区块走查。
- build 的 CSS minify `Unexpected "/"` 警告与 unocss icon 告警为仓内预存（03A 同记录），非本任务引入。
- ChainSteps 为 05/06/07 共享依赖：三单派单包已声明消费；若需接口变更走 coordinator（派单包 §4 明文）。

## CI/CD（必填）

- 分支：`dev`（本地；2026-11-03 合并 fast-forward，commit `352717d`；**未 push origin**——按人工验收闸门，推流由监管人决定）
- commit：`352717d` feat(policy): FE-POL-04A 智能政策库构建整页复刻——治理4Tab(清洗/结构化树表/溯源索引/指标库)+KPI基库开关三重闸门+ChainSteps页间导航首装(接口冻结) [agent:frontend-agent]
- 临时分支 `feat/pol04-governance` 与 worktree 已清理（合并后删除）
- pipeline / K8s / dev URL：N/A（未 push，无 CI 触发）

## 可观测性（建议）

- OTEL_SERVICE_NAME：`lumen-ui-science-pc`（仓级既有）；本页埋点经 `usePolicyTrack`（page-mounted/tab-change/base-ready-toggle/trace-action/goto + ChainSteps chain/goto），走仓内 `observability.ts` 通道。

## 涉及文件

主仓 `repos/lumen-ui-science-pc` dev（2026-11-03 合并自 worktree，`352717d`）：
- `src/views/policy/governance/index.vue`（改）
- `src/views/policy/components/PolicyChainSteps.vue`（新）
- `src/views/policy/governance/FE-POL-04A.test.mjs`（新）

主仓 `gkx-orchestration`：
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/FE-POL-04A.md`（本 handoff）

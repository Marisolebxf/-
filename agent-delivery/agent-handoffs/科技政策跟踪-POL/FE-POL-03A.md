# FE-POL-03A · 政策效果推演整页复刻（11 叶）— 效果预估 / 科技政策推演双工作台 + sharedCharts 图表族

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull`（派单包认领） |
| 说明 | 独立窗口并行任务；仅作业于 worktree `lumen-ui-science-pc--pol03-simulation`（分支 `feat/pol03-simulation`，基点 f4edea4） |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单 `/goal` 一致；未用 YAGNI 跳过 D8/D9/D10、可观测埋点与架构铁律；Arco 优先、第二处出现即封装、图表全走仓内 VChart |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 |

## 交付范围与实现（DoD 对照）

### 1. 页面结构（DEC-DS12 2 主 Tab）

- `src/views/policy/simulation/index.vue`（157 行）：`PageTabFrame` 承载 2 主 Tab——`estimate` 效果预估工作台 / `interpret` 科技政策推演工作台；v-if 挂载切换（卸载防图表实例泄漏）；头部 4 统计卡槽位：预估综合效果（`dimsEvalDone` 闸门：四维全评估才显综合分，否则空态卡）／落地成效维（`QPOL-02` PendingBadge ⚠️）／布局建议／利益攸关反馈；观测埋点 `usePolicyTrack`（tab 切换 + 子 Tab 切换事件）。

### 2. EstimateWorkbench（demo 867 行语义，本仓 790 行）

`src/views/policy/simulation/estimate/EstimateWorkbench.vue`，5 子 Tab：

- **unreleased 未出台政策模拟**：参数面板（政策类型 5 类 / 目标产业 / 实施时间 / 覆盖范围 slider / 支持力度 slider）+ 评审模式下的 T43 `hasHistoryData` 开关；仿真公式冻结（经济 `100/0.2·覆盖%·力度^0.9·200` 上限 99 / 社会 `55+150·0.25·覆盖` / 创新 `min(99, …)`）；结果卡 ×3 + 多轮保存对比表（`saveRun` · `slice(0,8)` · 重置）。
- **new 新出台政策效果预测**：`NEW_POLICY_OPTIONS` Select（ai/talent/park · scale 1/0.86/0.92 冻结）驱动 `scaleIndustryItems` 缩放产业影响图；T43 `textParsed` / `hasSimilarEffects` 闸门；相似政策匹配清单；创新预测序列图。
- **regional 区域空间模拟**：`regionalSpatialMapOption`（省域热力聚合 + 城市柱高叠加）+ `regionalHeatmapOption` 格网热力 + 深圳区县图（`shenzhenDistrictMapOption`，柱高 10×max12 demo 冻结）；`runSpatialSim` 乘性扰动刷新（ponytail 注释：demo Mock 演示语义，会话态非种子文件）。
- **multi 多维度评估**：雷达图 + 柱状图双视图 + 四维评估表（`dimsEvalDone` 综合分闸门源头）；页头综合分联动。
- **stakeholder 利益攸关方审计**：四项识别卡（STAKEHOLDER_AUDIT 四行：产业/创新/区域/综合）+ 反馈收集表单（含纳入开关）。

### 3. InterpretWorkbench（demo 727 行语义，本仓 627 行）

`src/views/policy/simulation/interpret/InterpretWorkbench.vue`，6 子 Tab：

- **parse 文本智能解析**：`textType` 三态（未选 / 未解析 / 结构化结果）+ T44 `parsed` 闸门；结构化字段（关键词 / 对象 / 措施 / 预期）。
- **focus 政策焦点**：tree LR 导图（`policyFocusMindOption`，`initialTreeDepth 2`）+ 点击节点查看说明（组件层 chart click → `focusNode` 预览）；柱图。
- **impact 覆盖面分析**：覆盖面 ≠ 渗透指数分列 KPI（`coverage.note` 语义保留）；深圳区县图 + 时间线。
- **relation 政策关联**：ECharts force 力导图（`policyRelationGraphOption`，repulsion 180 / edgeLength 90；非 Nebula——前端可视化层）。
- **path 落地路径**：历史对照 → 预测双 Timeline（`mode="left"`）。
- **report 报告生成**：章节自定义 checkbox + 4 格式（word/pdf/markdown/plain）导出（复用 01B `trackingExport` 的 `exportHtmlDoc`，不另造 HTML 拼装）；生成闸门 `parsed + hasEstimate`。

### 4. sharedCharts 图表族（demo 1161 行语义，本仓 440 行）

`src/views/policy/simulation/sharedCharts.ts`：13 个纯 option 工厂（`newPolicyPredictionOption` / `industryImpactOption` / `regionalHeatmapOption` / `regionalSpatialMapOption` / `shenzhenDistrictMapOption` / `multiDimensionRadarOption` / `multiDimensionBarOption` / `policyFocusMindOption` / `impactRegionBarOption` / `impactIndustryBarOption` / `policyRelationGraphOption` / `scaleIndustryItems` / `NEW_POLICY_OPTIONS`），全走仓内 `VChart`（`@/config/echarts`）消费，无 `echarts.init` / `new echarts` 手动生命周期。

### 5. DoD 逐条对照

| # | DoD 条目 | 状态 |
|---|---------|------|
| 1 | 2 主 Tab 复刻（DEC-DS12） | ✅ index.vue PageTabFrame 双 Tab |
| 2 | EstimateWorkbench 867 行语义 + 档 A #17–23 + T43 | ✅ 5 子 Tab 全语义 + 评审门控开关（默认开） |
| 3 | InterpretWorkbench 727 行语义 + 档 A #24–27 + T44 | ✅ 6 子 Tab 全语义 + 8 段位闸门 |
| 4 | sharedCharts 全走 VChart + 按需注册 | ✅ 13 工厂纯函数；echarts.ts 既有注册已覆盖（tree/graph/heatmap/radar 均在） |
| 5 | D2 决策：`BTN_DS_SIMULATE` L2 不复刻 | ✅ 推演按钮无权限锁，常可用 |
| 6 | 图表容器显式高度防 0 高 | ✅ `ps-chart--*` 定高类 + flex `0 0 auto` |
| 7 | 状态机自检最小移植 | ✅ `FE-POL-03A.test.mjs` 40 断言（见测试结果） |
| 8 | D9 ⓘ/🧪/⚠️ + 截图比对 | ✅ 统计卡 ⓘ + MockBadge + QPOL-02 PendingBadge；截图比对待人工验收（worktree 无预览环境，见遗留） |

## 问题清单

- 无阻塞问题。build 有一条预存 CSS minify 警告（`Unexpected "/"`，来自仓内其它样式块合并后的虚拟 stdin，非本任务引入；已验证本任务 CSS 文件注释配对完整，见自检脚本扫描）。

## 修改内容

worktree `D:\web\gkx-lumen\worktrees\lumen-ui-science-pc--pol03-simulation`（分支 `feat/pol03-simulation`，基点 f4edea4）：

- 新增 `src/views/policy/simulation/index.vue`（157 行，M 状态：S01 占位壳替换为整页实现）
- 新增 `src/views/policy/simulation/` 以下文件：
  - `estimate/EstimateWorkbench.vue`（790 行）
  - interpret/InterpretWorkbench.vue（627 行）
  - sharedCharts.ts（440 行）
  - interpretExport.ts（50 行，复用 01B trackingExport）
  - `FE-POL-03A.test.mjs`（240 行，40 断言）
- 样式整块抽取 `src/views/policy/styles/demo-policy-simulation.css`（558 行，FE-POL-S01 已建，本单消费）

**冻结边界遵守**：未改 menu.ts / api/policy.ts / policySeed.ts / `components/` 公共件；改动仅限 `src/views/policy/simulation/**`。

## 测试结果（三绿 + 回归）

在 worktree 根执行：

```
node src/views/policy/simulation/FE-POL-03A.test.mjs   # 40 项全绿
node src/views/policy/policy.test.mjs                  # 基座回归绿
pnpm type-check                                        # vue-tsc --build 通过
pnpm build                                             # vite build exit 0（4075 modules）
```

修复记录（type-check 2 错 → 0）：
1. `startDate` 推断 `string`，allow-clear 赋 `undefined` 不兼容 → 显式 `as string | undefined` 联合类型
2. `NEW_POLICY_OPTIONS[0]` 索引访问带 `undefined` → 非空断言 `!`（冻结常量数组首项必存）
3. build：3 处 CSS `@import` 相对路径层级错误（`./` → `../` / `../../`）→ 修正指向 `policy/styles/`

## 遗留风险

- **截图比对五件套未做**：worktree 无预览环境（junction node_modules 可跑 build 但无 dev server 已验证 URL）；建议人工验收时在主工作区合并后跑 `pnpm dev` 对照 demo 截图走查（复刻经验清单 §1 视觉对照）。DoD 条目 8 的截图比对环节转人工验收执行。
- `pnpm install` 前置钩子的 workspace hoist 告警为 worktree junction 环境预存（主仓 node_modules 软链），不影响三绿。
- 关联图谱用 ECharts force（demo 同源语义，前端可视化层）；Nebula 仍是后端图谱真源，不冲突。

## CI/CD（必填）

- 分支：`feat/pol03-simulation`（worktree 本地，未 commit/push —— 按人工验收闸门停本地）
- commit：无（等人工验收后由监管人决定推流）
- pipeline / K8s / dev URL：N/A（未 push，无 CI 触发）

## 可观测性（建议）

- OTEL_SERVICE_NAME：`lumen-ui-science-pc`（仓级既有）；本页埋点经 `usePolicyTrack`（tab/子 Tab 切换事件），走仓内 `observability.ts` 通道。

## 涉及文件

worktree `lumen-ui-science-pc--pol03-simulation`：
- `src/views/policy/simulation/index.vue`（改）
- `src/views/policy/simulation/estimate/EstimateWorkbench.vue`（新）
- `src/views/policy/simulation/interpret/InterpretWorkbench.vue`（新）
- `src/views/policy/simulation/sharedCharts.ts`（新）
- `src/views/policy/simulation/interpretExport.ts`（新）
- `src/views/policy/simulation/FE-POL-03A.test.mjs`（新）
- `src/views/policy/styles/demo-policy-simulation.css`（S01 已建，消费未改）

主仓 `gkx-orchestration`：
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/FE-POL-03A.md`（本 handoff）

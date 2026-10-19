# FE-DR-01A · 总体视窗整页复刻

> 仓库：`repos/lumen-ui-science-pc`；路由 `/data/data-overview`（name: `data-overview`）。
> demo 真源：`demo-ui-science/src/pages/data-resources/OverviewWindow.jsx` 及同目录子组件。

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| depends_on | `FE-DR-S01`（联调中） |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未新增 npm；种子冻结 `dataResourcesSeed.ts`；图表 option 纯函数；布局走查补丁（fullBleed 滚动 / Spin 100% 宽 / KPI 横排均分） |

## 范围与实现（对照 DoD）

| 区块 | seq | 状态 | 实现位置 |
|------|-----|------|----------|
| KPI 概览 + 仪表盘三图 + 报表导出 | 330、333 | ✅ | `overview/index.vue` + `DrExportButton.vue` |
| 资源来源分析与详情 | 331 | ✅ | `ResourceSourceAnalysisDetail.vue` + 顶部来源柱/饼图 |
| 接入数据资源详情查询 | 332 | ✅ | `AccessResourceDetailQuery.vue` |
| 多源数据整合分析 | 334 | ✅ | 主题分布柱图 + 下钻 |
| 大数据资源中心详情 | 335–338 | ✅ | `BigDataCenterDetail.vue` |
| 资源关联关系（图谱） | 339–342 | ✅ | ECharts graph + `GraphNodeDetail.vue` + 分类 Tag 导航 |
| 语义关联与主题聚合 | 342 | ✅ | `SemanticThemeAggregation.vue` |
| 应用系统状态 / 接口跟踪 | 343–344 | ✅ | `ApplicationStatusMonitor.vue`（照 demo 含接口指标条） |
| 应用主体列表 / 累计调用趋势 | 345–346 | ✅ | `ResourceAppSubjectList.vue`、`CumulativeCallTrendAnalysis.vue` |

**原型核对**：超范围/错位项按规划 D1 **照 demo 复刻**，不顺手改需规（见 `科技数据资源-总体视窗-原型核对报告.md`）。

**种子说明**：当前 demo `overviewKPIs` 为 3 项（与核对报告 7 KPI 历史稿不一致，以 demo 冻结种子为准）。

## 布局走查（联调前补丁）

1. **页根滚动**：`.data-resources-page` 对齐 fullBleed（`height:100%` + `overflow-y:auto`，补 `--figma-*` 本仓默认值）。
2. **总览区宽度**：`a-spin` 增 `dr-access-overview-spin`，根与 `.arco-spin-children` `width:100%`（修复约 720px 收缩）。
3. **KPI + 仪表盘三图**：横向 `flex` 均分撑满 `dr-access-overview-section`。

## D9 / 可观测

- `MockBadge`（USE_MOCK）+ `MetricSpecHint`（占位 metric_id，待 `/metrics/v1/catalog`）
- `dr-data-resources-track` + `createTraceId`（页挂载、KPI 下钻、Tab 等）

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| D12 不调 demo 服务 / USE_MOCK=false 零 fixture | ✅ |
| 调用链占位 `/display/v1/data-ops/overview/dataset` | ✅（待 BE-DR 冻结） |
| D8 Arco（禁原生 select 回退） | ✅ |
| 图谱 ECharts graph，非 Nebula 全图扫描 | ✅ |
| 前端可观测埋点 | ✅ |
| D9 ⓘ/🧪 | ✅（metric_id 占位） |

## 测试结果

- `pnpm type-check`：0 错（2026-10-19）
- `node src/views/data-resources/overview/overview.test.mjs`：ok
- `pnpm build`：绿
- 本地联调：`pnpm dev` → `/data/data-overview`，`VITE_APP_USE_MOCK=true` 整页可验

## CI/CD

- 分支：`dev`（工作区待提交；含 FE-DR-S01 基座 + 本单 overview 增量）
- K8s dev URL：待 push 后 CI 部署（未在本 handoff 执行 push）

## 涉及文件（主要）

- `src/views/data-resources/overview/`（index、overviewCharts.ts、components/*、overview.test.mjs）
- `src/views/data-resources/components/DrExportButton.vue`、`DrKpiCard.vue`
- `src/views/data-resources/styles/demo-data-resources.css`
- `src/types/dataResources.ts`、`src/mock/modules/dataResources.ts`、`src/api/dataResources.ts`

## 遗留风险

- `metric_id` 占位，catalog 就绪后批量挂接。
- BE `API-DR` 未冻结前，联调仅 Mock + 契约草案路径占位。
- 与 FE-DR-S01 同批未 push 的 `lumen-ui-science-pc` 变更需一并提交后再走 K8s 验收。

## 联调确认

前端 Mock 联调通过：总体视窗 seq 330–346 区块可浏览、导出报表、图谱点击、筛选表格与 demo 结构一致。待孔东签收代码 push 后与 BE-DR 契约对接实网关。

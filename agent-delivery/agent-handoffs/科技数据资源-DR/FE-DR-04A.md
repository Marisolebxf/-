# FE-DR-04A · 应用视窗整页复刻

> 仓库：`repos/lumen-ui-science-pc`；路由 `/data/data-access` 同级菜单 **应用视窗** `/data/data-application`（name 以 `menu.ts` 为准）。
> demo 真源：`demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx` + `components/AssetApplicationBasicSummary.jsx`。

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| depends_on | `FE-DR-S01` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 无新 npm；拆 `applicationModel.ts` / `applicationCharts.ts` + 6 Tab 子组件；实时监控轮询按 DoD 在 lumen 实现（demo 无 setInterval） |

## 范围与实现（对照 DoD / seq 376–399）

| 区块 | seq | 实现位置 |
|------|-----|----------|
| 资产应用总览：趋势/排行/详情表/基本情况汇总 | 376–378 | `ApplicationOverviewTab.vue` + `AssetApplicationBasicSummary.vue` |
| 实时应用监控（QPS/响应/成功率/告警演示） | 376–379 | `index.vue` `.dr-realtime-monitor` + `APPLICATION_MONITOR_POLL_MS=30000` |
| 数据资源使用情况和详情 | 380–383 | `ApplicationUsageDetailTab.vue` |
| 主题数据被调用 | 384–387 | `ApplicationThemeCallTab.vue` |
| 供应方被调用 | 388–391 | `ApplicationSupplierCallTab.vue` |
| 需求方调用详情 | 392–395 | `ApplicationDemanderCallTab.vue` |
| 业务应用调用详情（筛选/导出/报告） | 396–399 | `ApplicationBusinessCallTab.vue` + `logMatchesCallTime` |

**六 Tab**：与 S01 壳一致 — `overview` / `theme` / `supplier` / `demander` / `business` / `usage`。

**数据集**：`createApplicationDataset()` 接线 `dataResourcesSeed.ts` 全字段（`usageCallTrend`、`assetRanking`、`supplier*`、`demanderStats`、`businessApplication*`、`dataUsageDetails`、`usageDetailTrend`、`themeCall*`、`callUserTracking` 等）。

**实时监控**：`visibilitychange` 暂停轮询；`onUnmounted` 清理 timer；指标由 `usageCallTrend` 基线 + 确定性 `monitorTick` 抖动（无 `Math.random`）。

## D9 / 可观测

- KPI 行：`MockBadge` + `MetricSpecHint`（`DR-M-application-kpi` 等占位 metric_id）
- `trackDataResourcesInteraction('application', …)`（含 `monitor-tick`）

## 自检

- `application/businessAppFilter.test.mjs` — 业务 Tab 文案与 `logMatchesCallTime` 源断言
- `application/usageDetailReport.test.mjs` — 使用详情导出/报表关键字符串
- `application/application.test.mjs` — 无 `DrPagePlaceholder`、实时监控常量与 CSS 类

## 测试结果

- `pnpm type-check`：0 错
- `node src/views/data-resources/application/businessAppFilter.test.mjs`：ok
- `node src/views/data-resources/application/usageDetailReport.test.mjs`：ok
- `node src/views/data-resources/application/application.test.mjs`：ok
- `node src/views/data-resources/dataResources.test.mjs`：ok
- `pnpm build`：绿

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| D12 / USE_MOCK=false 零 fixture | ✅ `emptyApplicationDataset()` |
| D8 Arco（Tab/Select/Radio button/VChart） | ✅ |
| 可观测埋点 | ✅ |
| D9 ⓘ/🧪 | ✅（metric_id 占位，待 metrics 注册表对齐） |

## 偏离说明

- **实时监控**：招标 seq 与「应用视窗-原型核对报告」对 QPS/告警表述有差异；按本任务 DoD 在总览区交付演示轮询，上线前可与产品核对是否保留或降级为静态 Mock。
- **B2 用户与系统追踪**：主题 Tab 字段归属按 demo 照抄，未改错位（DoD 注明）。

## 联调确认

前端 Mock 联调通过：应用视窗 seq 376–399 六 Tab 可走查。路径 `/data/data-application`（以路由注册为准），`VITE_APP_USE_MOCK=true`。待 BE-DR 契约后对接实网关。

## CI/CD

- 分支：`dev`
- commit（lumen-ui-science-pc）：`8ffd8b9`
- commit（gkx-orchestration）：`f2b9a6db`
- dev 测试：本地 `pnpm type-check` / `pnpm build` 绿；K8s dev 待 CI deploy

## cost

- `actual_tokens` / `actual_cost`：监管人回填
- `model_used`: Composer（Cursor agent + subagent）
- `cost_warn`: green

## 涉及文件

- `src/views/data-resources/application/`（index + model + charts + components + *.test.mjs）
- `src/types/dataResources.ts`
- `src/mock/modules/dataResources.ts`
- `src/views/data-resources/dataResources.test.mjs`

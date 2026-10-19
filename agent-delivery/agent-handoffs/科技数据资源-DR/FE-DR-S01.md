# FE-DR-S01 · 科技数据资源前端模块基座

- task-id：FE-DR-S01
- 执行：agent:frontend-agent
- 监管：human:孔东
- 仓：`repos/lumen-ui-science-pc`
- ponytail：full（最小 diff 页壳 + 全量种子冻结；业务区块留 FE-DR-01A~04A）

## 范围与实现

| DoD 项 | 状态 | 说明 |
|---|---|---|
| 四视窗路由挂接 | ✅ | `menu.ts` 将 `data-overview/access/theme/application` 指向 `views/data-resources/*/index.vue`；`fullBleed` 与态势页一致 |
| Mock 种子冻结 | ✅ | `src/mock/modules/dataResourcesSeed.ts`（demo `mockData.js` 整文件移植，`@ts-nocheck` + 头注释真源/任务 ID） |
| API 双轨 | ✅ | `src/api/dataResources.ts` 四端点 + `register.ts` 注册 `dr*Dataset` |
| 公共件盘点 | ✅ | 见下表；模块私有 `DrKpiCard`/`DrKpiRow`（demo `KPICard` 语义，样式自含 `demo-data-resources.css`） |
| demo 样式抽取 | ✅ | `views/data-resources/styles/demo-data-resources.css`（自 demo `style.css` 拷贝） |
| 可观测 | ✅ | `useDataResourcesTrack.ts` → `dr-data-resources-track` + `createTraceId` |
| 三绿 | ✅ | `pnpm type-check` / `dataResources.test.mjs` / `pnpm build` |

## 页壳行为（批 1 可验）

- **总体/接入/应用**：KPI 行 + `DrPagePlaceholder`（标明 FE-DR-01A/02A/04A）
- **主题**：四张 `StatCard` 概览 + placeholder（FE-DR-03A）
- **应用**：demo 六 Tab 键冻结 + `PageTabFrame`
- `USE_MOCK=false`：KPI/概览初值为空结构，不灌 fixture（D12）

## 公共件盘点（DR 不引 TiandituMap / InsightDetailDrawer）

| 组件 | S01 用法 | 备注 |
|---|---|---|
| `PageTabFrame` | 应用视窗 Tab 框 | ✅ |
| `StatCard` | 主题视窗四卡 | ⓘ 待 01A~04A 挂 metric_id |
| `MetricSpecHint` | 经 StatCard 可选 | 未挂 metric_id |
| `MockBadge` | — | 页面接 KPI 时由后续单叠 |
| `ExportFlowPanel` | — | 导出区在 01A/02A/04A |
| `chartOptions` / chart/* | — | 图表在页面单 |
| `KpiDeck` | — | 用模块 `DrKpiRow` 对齐 demo `.dr-kpi-card` |
| TiandituMap | **不引** | 四视窗无地图落点 |
| L6 `InsightDetailDrawer` | **不引** | DR 详情为 demo `DetailDrawer` 简化结构，03A/01A 模块私有 |

## 架构合规（自检）

| 铁律 | ✅/❌ |
|---|---|
| D12 lumen 不调 demo 服务 | ✅ |
| Mock 开关 / USE_MOCK=false 零 fixture | ✅ |
| 前端 → Java（路径占位 `/display/v1/data-ops/*`） | ✅ 待 BE-DR 冻结 |
| D8 Arco | ✅ |
| 可观测埋点 | ✅ |
| D9 ⓘ/🧪 | ⚠️ 基座未挂 metric_id（页面单接线） |

## 验收证据

- 本地：`pnpm type-check` 0 错；`node src/views/data-resources/dataResources.test.mjs` 绿；`pnpm build` 绿
- 路由：`/data/data-overview` 等四路径可进页壳（菜单「科技数据资源」）

## 下游

- FE-DR-01A 依赖本单；数据集类型可扩展 `types/dataResources.ts`，种子已全量在 `dataResourcesSeed.ts`

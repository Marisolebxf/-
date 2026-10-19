# FE-DR-03A · 主题视窗整页复刻

> 仓库：`repos/lumen-ui-science-pc`；路由 `/data/data-theme`（name: `data-theme`）。
> demo 真源：`demo-ui-science/src/pages/data-resources/ThemeWindow.jsx`。

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| depends_on | `FE-DR-S01` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 无新 npm；`themeModel.ts` / `themeCharts.ts`；KPI 用 `DrKpiRow`；侧栏+主栏 flex 布局（监管人走查后调整） |

## 范围与实现（对照 DoD / seq）

| 区块 | seq | 实现位置 |
|------|-----|----------|
| 主题库分类浏览 + 多维筛选 | 368–371 | `theme/index.vue` 侧栏树 + `themeModel.ts` |
| 资源详情列表 + 智能搜索/分区/质量筛选 | 368–371 | `theme/index.vue` 主栏库表 |
| 资源分布可视化 | 371 | `themeCharts.ts` + 与关联图并排 |
| 数据集关联关系图谱 | 375 | ECharts graph，`datasetRelationData` 种子 |
| 元属性详尽呈现 + 导出 | 372 | `a-descriptions` + `DrExportButton` |
| 数据表结构与字段详情 | 373 | 表选择 + 字段表 + `themeTableSchema.test.mjs` |
| 智能搜索与多维筛选 | 374–375 | `filterThemeDatabases` / `matchSmartKeyword` |

**数据集**：`createThemeDataset()` 扩展 `themeDatabases` + `datasetRelationData`；API 占位 `/display/v1/data-ops/theme/dataset`。

## 布局走查（监管人反馈后 as-built）

1. **KPI**：`dr-access-overview-section` + `DrKpiRow` + `dr-access-overview-spin`（对齐 01A/02A，避免 StatCard 在 Spin 内样式错位）。
2. **主布局**：`dr-theme-layout` — 左 240px 侧栏（筛选 + 无冗余图标的 `a-tree` show-line），右主栏 **库表整行宽**。
3. **图表行**：资源分布与数据集关联 **同一行 50%/50%**（表格下方），非挤在库表右侧。
4. **表格/元数据**：库表与字段表 13px、表头浅底、行高加大；元属性 Descriptions 字号/内边距统一。

## D9 / 可观测

- `MockBadge` + `MetricSpecHint`（`DR-M-theme-kpi` / `DR-M-theme-meta` 占位）
- `trackDataResourcesInteraction('theme', …)`

## 测试结果

- `pnpm type-check`：0 错
- `node src/views/data-resources/theme/themeTableSchema.test.mjs`：ok
- `node src/views/data-resources/theme/themeResourceMeta.test.mjs`：ok
- `node src/views/data-resources/theme/theme.test.mjs`：ok
- `node src/views/data-resources/dataResources.test.mjs`：ok
- `pnpm build`：绿

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| D12 / USE_MOCK=false 零 fixture | ✅ |
| D8 Arco（树/表/筛选） | ✅ |
| 图谱 ECharts graph | ✅ |
| 可观测埋点 | ✅ |
| D9 ⓘ/🧪 | ✅（metric_id 占位） |

## 联调确认

前端 Mock 联调通过：主题视窗 seq 368–375 可走查（树筛选、库表选中、双图并排、元数据、表结构）。路径 `/data/data-theme`，`VITE_APP_USE_MOCK=true`。待 BE-DR 契约后对接实网关。

## cost

- `actual_tokens` / `actual_cost`：监管人回填
- `model_used`: composer（Cursor agent）
- `cost_warn`: green

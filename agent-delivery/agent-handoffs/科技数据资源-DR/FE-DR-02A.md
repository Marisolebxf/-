# FE-DR-02A · 接入视窗整页复刻

> 仓库：`repos/lumen-ui-science-pc`；路由 `/data/data-access`（name: `data-access`）。
> demo 真源：`demo-ui-science/src/pages/data-resources/AccessWindow.jsx` 及 `components/AccessSourceAnalysisDetail.jsx`、`AccessDataResourceDetail.jsx`、`AccessHistorySituation.jsx`、`accessMultiFilter.js`。

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
| 说明 | 无新 npm；种子 `dataResourcesSeed.ts`；图表 option 纯函数 `accessCharts.ts`；吸收 01A 布局补丁（Spin 100% 宽下沉 `demo-data-resources.css`） |

## 范围与实现（对照 DoD / seq）

| 区块 | seq | 实现位置 |
|------|-----|----------|
| KPI + 多维筛选 + 完成度 + 归集量趋势 | 347–350 | `access/index.vue` + `accessMultiFilter.ts` |
| 来源分析与详情 | 351–355 | `components/AccessSourceAnalysisDetail.vue` |
| 接入数据资源详情 | 356–359 | `components/AccessDataResourceDetail.vue` |
| 历史资源接入情况 | 360–363 | `components/AccessHistorySituation.vue` |
| 问题资源（统计 Tab + 列表/批量检索/复现） | 364–367 | `access/index.vue` |

**原型核对**：照 demo 结构复刻；不顺手改需规（见 `科技数据资源-接入视窗-原型核对报告.md`）。

## 相对 FE-DR-01A 的刻意对齐（防重复踩坑）

1. **页壳**：`.data-resources-page` fullBleed 纵向滚动（S01 已有）。
2. **Spin 宽度**：`dr-access-overview-spin` + 共享 CSS（`.arco-spin-children { width:100% }`），避免 ~720px 收缩。
3. **Arco**：筛选/表格/弹层全 Arco；`a-select` 不与 `<label>` 包裹；`Segmented` → `a-radio-group type="button"`。
4. **Mock / D9**：`MockBadge` + `MetricSpecHint`（占位 `DR-M-access-kpi` 等）；`USE_MOCK=false` 空结构初值。
5. **数据集**：`createAccessDataset()` 返回接入视窗全量种子字段；API 占位 `/display/v1/data-ops/access/dataset`。

## 测试结果

- `pnpm type-check`：0 错
- `node src/views/data-resources/access/accessMultiFilter.test.mjs`：ok
- `node src/views/data-resources/access/access.test.mjs`：ok
- `node src/views/data-resources/dataResources.test.mjs`：ok（接入页无 `DrPagePlaceholder`）
- `pnpm build`：绿

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| D12 / USE_MOCK=false 零 fixture | ✅ |
| D8 Arco | ✅ |
| 可观测 `trackDataResourcesInteraction` | ✅ |
| D9 ⓘ/🧪 | ✅（metric_id 占位） |

## 联调确认

前端 Mock 联调通过：接入视窗 seq 347–367 区块可浏览、筛选查询、导出、问题资源 Tab/表与 demo 结构一致。待 BE-DR 契约冻结后对接实网关。

## cost

- `actual_tokens` / `actual_cost`：由监管人按会话回填
- `model_used`: composer（Cursor agent）
- `cost_warn`: green

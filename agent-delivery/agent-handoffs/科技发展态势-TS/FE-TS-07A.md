# FE-TS-07A · 科技创新评估（M7）整页复刻 — 前端交付（联调中）

> 仓库：`repos/lumen-ui-science-pc`；路由 `/trend/tech-innovation-evaluation`（`menu.ts` → `tech-innovation-evaluation`，fullBleed）。
> 状态：**联调中**（mock 点测通过；`API-TS-M7` 冻结后 `USE_MOCK=false` 对接 Java）。
> demo 真源：`demo-ui-science/src/pages/tech-innovation-evaluation-new/`（`TechInnovationEvaluationNewPage.jsx` + `TechInnovationEvaluationNew.css`）。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | demo 单文件按阶段拆组件 + mock 快照计算链单文件冻结；首屏同步种子对齐 demo `useState(createEvaluationSnapshot)`，避免纯异步 gate 白屏；SetupStage 评估对象配置改 Arco Form/Cascader/RangePicker(year)/Select（D8）；D9 ⓘ + 自检 test.mjs；无新 npm 包。 |

## 范围与实现（对照 DoD）

| DoD 项 | 实现 |
|---|---|
| 结果 Tab：综合分（76）+ 四维分 + 历史 4 条报告 + 建议 | `ResultDashboard.vue`：四大能力卡 + 图谱 + 趋势预测 + 空间分布 + 政策建议；`ReportHistoryDrawer`（4 条）+ `ReportPreviewModal`（归档预览）。综合 76：demo 无独立大数字，契约 `composite_score` 联调挂报告预览 |
| 指标 Tab：指标体系预览 + 权重说明，只读 | `SetupStage.vue` 右栏指标树 + 权重雷达；`WeightDrawer.vue` 权重校验/应用（只读消费契约权重） |
| 报告中心 | 历史列表 + 预览弹窗（见上） |
| Mock + 接口双轨 | `mock/modules/innovationEvaluation.ts` 冻结种子；`api/situation/innovationEvaluation.ts`：`tsInnovationEvaluationMeta` / `tsInnovationEvaluationSnapshot` |
| D9 / build / handoff | 四维卡 `MetricSpecHint`（`TS-M7-dimension-*`）；`pnpm type-check` 绿；本文件 |

### 本轮修复与增强（2026-10-16）

| 项 | 说明 |
|---|---|
| 首屏白屏/无限 loading | `index.vue`：同步 `DEFAULT_FILTERS` / `DEFAULT_WEIGHTS` / `createEmptySnapshot()` 初值（对齐 demo L1658-1661）；`onMounted` 后台 `refreshFromApi()`，失败仅 warning、不挡页 |
| 评估对象配置表单 | `SetupStage.vue`：`a-form` + `IndustrySelect`（Arco 级联）+ 区域 `a-cascader`（替换 SearchableCascadeFilter 自定义清除）+ `a-range-picker` year + `a-select`；`setupFormModel.ts` 时间文案互转 |
| 样式 | 收窄 `.tien-field button` 选择器，避免覆盖 Arco 清除图标；`.tien-arco-form` 表单项统一 |

### 类型契约（联调）

- `types/innovationEvaluation.ts`：`InnovationEvaluationMeta` / `EvaluationSnapshot` / `EvaluationFilters` / `EvaluationWeights`
- 真实路径（过渡）：`GET /situation/v1/innovation-evaluation/meta`、`GET /situation/v1/innovation-evaluation/snapshot?payload=...`
- 契约草案 `API-TS-M7.md` 为三端点（result / indicator-config / reports）；冻结后**仅改 api 层**映射，页面零改动

## 验收证据

- `pnpm type-check`：**0 error**（2026-10-16，含 M7 表单改造后）
- `pnpm build`：**绿**（首版提交 `17bdff0` 后；表单改动未单独 push，见下方提交说明）
- 自检：`node src/views/situation/innovation-evaluation/innovationEvaluation.test.mjs` → **42 项全绿**
- 人工点测（human:孔东）：配置页 Arco 表单 + 三阶段流转 + 四维详情 + 权重 + 报告中心；首屏不再卡在 `a-spin`

## 联调确认（AV-1）

- 前端 mock 环境（`USE_MOCK=true`）功能路径已通：**联调确认**
- 后端：`API-TS-M7` 仍为草案；Java 路径/DTO 冻结后切换 `USE_MOCK=false`，验证 meta/snapshot（或拆分三端点后的等价数据）
- 联调入口：`pnpm dev` → `/trend/tech-innovation-evaluation`

## 偏离说明

- demo 结果页无综合分 76 独立展示（与首版 handoff 一致）
- 同仓 `17bdff0` 含 FE-TS-06A 深圳创新监测文件（register/menu 交织，先例同批提交）
- **本地未 push**：`index.vue` 首屏修复、`SetupStage` Arco 表单、`setupFormModel.ts`、相关 CSS（待监管人 commit/push `origin/dev`）

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 调用链 FE→Java→Python | ✅ api 仅网关路径 |
| D12 | ✅ USE_MOCK=false 不执行 mock 注册逻辑 |
| D8 | ✅ Arco Form/Cascader/RangePicker/Select + Design token |
| D9 | ✅ 四维卡 ⓘ + 详情指标浮层 |
| D10 | ✅ 步骤条/抽屉/权重校验 |
| 可观测 | ✅ M1 请求头透传 |
| 无新依赖 | ✅ |

## CI/CD

- 目标分支：`origin/dev`
- 已 push：`17bdff0`（M7+M6 首版）
- 待 push：M7 联调前修复与表单改造（见上）

## 涉及文件（M7）

`src/views/situation/innovation-evaluation/**`、`src/api/situation/innovationEvaluation.ts`、`src/mock/modules/innovationEvaluation.ts`、`src/types/innovationEvaluation.ts`；`src/mock/register.ts`、`src/router/menu.ts`

## 遗留风险

- `metric_id` 占位；`API-TS-M7` 未冻结；U2/U5 待 M0
- `DetailPage` 详情筛选仍为原生 `<select>`（配置页已 Arco，详情可后续对齐）

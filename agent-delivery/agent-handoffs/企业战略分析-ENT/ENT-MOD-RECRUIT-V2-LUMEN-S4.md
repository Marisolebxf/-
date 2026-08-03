# ENT-MOD-RECRUIT-V2-LUMEN-S4 · 引育推荐全量（lumen-ui-topic）

> **执行人**：`human:曹丽影` · **监管**：`human:曹丽影`  
> **上游**：`ENT-MOD-SHARED-V2-LUMEN-S1`（done）  
> **设计参照**：Wireframe-ENT-RECRUIT v1.9 / demo 原型  
> **仓**：`lumen-ui-topic` · `dev` → `origin/dev`

## 认领 / 提审

| 阶段 | 字段 | 值 |
|------|------|-----|
| 派单 | assigned_to / supervised_by | `human:曹丽影` / `human:曹丽影` |
| 派单时间 | | `2026-07-29`（孔东派单） |
| 开工 | in_progress_at | `2026-08-03T14:00:00+08:00`（估） |
| 提审 | status / review_at | `review` / `2026-08-03T22:30:00+08:00` |
| commit | | `28cd2a0` on `origin/dev` |

## 范围与实现

| DoD 项 | 结果 |
|--------|------|
| 招引/培育双视图可切换 | ✅ `EnterpriseRecruit.vue` 双层 Tab |
| 筛选推荐工作台可演示 | ✅ `RecruitWorkbench` + `RecruitFilterPanel` |
| 排名 Table + 区域分布 | ✅ `RecruitResultPanel` 左右分栏（列表+详情） |
| 权重校验 Σ=100% | ✅ 保留 `RecruitWeightPanel` 校验逻辑 |
| 候选工作台 ≤50 家、批量对比篮 | ✅ `CandidatePanel` 批量选择与对比篮 |
| 详情 Drawer 字段完整 | ✅ `RecruitDetailDrawer` + `RecruitDetailPanel` |
| 评审模式血缘 | ✅ `useReviewStore` + `MetricSpecCard` 接入 |
| 异常态 UI | ✅ loading / empty / error / partial 覆盖 |
| build | ✅ `npm run build` 绿 |

### Wireframe v1.9 对齐要点

- **配置区**：招引 4 字段（含目标特征）；筛选流内模型说明只读（`RecruitModelExplainPanel`），无权重滑条
- **结果区**：列表+详情分栏、批量勾选、状态栏；培育视图含企业排名/行业分布
- **候选 Tab**：页内评审状态机 `list → review_config → review_process → review_result`
- **异步处理**：5 阶段步骤 +「稍后查看」
- **风险详情**：`RecruitRiskDetailDrawer` 独立抽屉

## 产物清单

### 新增

- `RecruitModelExplainPanel.vue`
- `RecruitDetailPanel.vue`
- `RecruitRiskDetailDrawer.vue`
- `RecruitReviewConfigPanel.vue`

### 修改

- `EnterpriseRecruit.vue`
- `RecruitWorkbench.vue` / `RecruitFilterPanel.vue` / `RecruitResultPanel.vue`
- `CandidatePanel.vue` / `RecruitProcessingPanel.vue`
- `recruitMeta.ts` / `recruitDisplay.ts` / `recruit.ts` types
- `useRecruit.ts`（见偏离说明）

## 偏离说明

| 项 | 说明 |
|----|------|
| `useRecruit.ts` 小改 | DoD 原约定不改 S1 composable；v1.9 需第 4 筛选项（目标特征）及候选 Tab 传入 `enterpriseCodes` 触发分析，属 UI 契约对齐必要扩展 |
| `RecruitDetailPanel` | 原 scope 仅列 `RecruitDetailDrawer`；v1.9 分栏详情用 Panel 组件，Drawer 仍保留用于全局详情入口 |

## 验收证据

| 项 | 结果 |
|----|------|
| commit | `lumen-ui-topic` `28cd2a0` on `origin/dev` |
| build | `npm run build` ✅ |
| 路由 | `/enterprise/recruit`（招引/培育 × 筛选/候选） |
| registry | `ENT-MOD-RECRUIT-V2-LUMEN-S4` → `review` |

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 前端 → Java REST | ✅ 消费 S1 `useRecruit`，未直连 Python |
| Arco + Design.md | ✅ |
| D9 血缘 ⓘ | ✅ 关键指标旁 MetricSpecCard |
| 可观测 observability.ts | ⏸ 本任务未新增埋点（页面级沿用既有） |

## cost

| 字段 | 值 |
|------|-----|
| `actual_tokens` | 95000 |
| `model_used` | composer-2.5 |
| `actual_cost` | 1.9 |
| `cost_warn` | green |

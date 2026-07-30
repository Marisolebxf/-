# ENT-MOD-RISK-V2-LUMEN-S2 · 风险洞察全量（lumen-ui-topic）

> 派单话术优先于任务清单；硬约束：结果 `#105 → #106`；演示数据进 fixtures + MockBadge；禁止发明 `riskInsight/*` 结果 API。  
> 顺带完成：抽离 `analysisTask.ts`（S1 优化延后项，监管人确认随 S2 处理）。

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| claimed_at | `2026-07-30T11:12:34+08:00` |
| worktree_branch | `dev` |
| 说明 | 风险洞察全量 UI + 共享任务中心抽离；未 commit（待监管人确认） |

## DoD 对照（派单话术）

| DoD | 状态 | 证据 |
|-----|------|------|
| 供应链图谱可渲染、节点可展开、关键/风险节点侧栏可筛选 | ✅ | `SupplyChainGraph.vue` + `SupplyChainNodeList.vue` + fixtures 展开纯函数 |
| 痛难点 Tab 可切换，四维诊断卡片可筛选，受影响企业 Drawer 可展开 | ✅ | `PainPointsPanel` / `PainPointDimensionCard` / `PainPointAffectedDrawer` |
| 四视图闭环可演示；历史可恢复 | ✅ | configuration → processing → result → history；`restoreTask` / `newFromConfig` |
| 所有异常态有 UI 覆盖 | ✅ | `RiskResultArea`：loading/success/empty/error/permission |
| 画像 risk tab 可访问 | ✅ | `EnterpriseProfileTabPanel` 已接 `entProfileRiskAll`（本次未改） |
| 对比篮 → `/enterprise/risk?analysis_type=supply-chain\|pain-points` 可带入企业集合 | ✅ | `useCompareBasketDispatchContext` + `resolveRiskEnterprises` |
| 评审模式按 demo 复刻 | ✅ | `MockBadge` / `MetricSpecCard` / `MetricValueDisplay` / `TraceInfoIcon` + reviewMode |
| `npm run build` + `type-check` | ✅ | `vue-tsc --build` 通过；`vite build` 通过（含 `EnterpriseRisk-*.js` chunk） |

## 硬约束自检

| 约束 | 状态 |
|------|------|
| 结果走 `#102 → #109 → #105 → #106` | ✅ `useEnterpriseRisk` + `enterpriseRiskStream.finishRiskSuccess` |
| Mock 不构造 #106 JSON | ✅ `USE_MOCK` 时不调 `fetchAnalysisAssetJson`；结果 UI 用 fixtures |
| 演示数据 fixtures + MockBadge | ✅ `src/fixtures/enterprise/riskInsightDemo.ts` |
| 禁止发明 `riskInsight/*` 结果 API | ✅ 全仓无 `fetchRiskInsightResult` / `riskInsight/` defineApi id |

## 产物清单

### 共享底座抽离（随 S2）

- 新增 `src/api/enterprise/analysisTask.ts`（#102–109）
- 新增 `src/api/enterprise/types/analysisTask.ts`
- 新增 `src/mock/enterprise/analysisTask.ts`
- 精简 `evaluation.ts`（API/types/mock）仅留 #113–121 + `createEvaluationTask`
- `riskInsight.ts` / `recommend.ts` / `index.ts` / `register.ts` 改 import
- 引育种子 weights 与 `useRecruit` 对齐：`tech_match/growth/region_fit`

### 风险洞察 UI

- `src/views/enterprise/EnterpriseRisk.vue`
- `src/composables/useEnterpriseRisk.ts` + `enterpriseRiskHelpers.ts` + `enterpriseRiskStream.ts`
- `src/config/enterpriseRisk.ts`
- `src/fixtures/enterprise/riskInsightDemo.ts`
- `src/components/enterprise/risk/*`（11 个组件）
- `src/router/menu.ts`：`enterprise/risk` 挂载 `EnterpriseRisk.vue`

### 行数自检（均 ≤300）

最大：`useEnterpriseRisk.ts` 277、`SupplyChainInsightPanel.vue` 212、`analysisTask.ts` 213、`PainPointsPanel.vue` 181。

## 关键设计决策

1. UI Tab 用连字符（`supply-chain`），任务 `subType` 用下划线（`supply_chain`），与对比篮 `analysis_type` 一致。
2. Mock 成功态图谱/痛点始终渲染 fixtures（catalog #106 JSON 未展开 🟡）；真实模式额外拉 #106 payload 暂存，待 DTO 映射后替换渲染源。
3. 报告 PDF / `risk_report` 产物任务未接（规格不做客户端 PDF）。
4. 删除未引用的 `RiskEnterprisePicker.vue`（对象区由对比篮带入 + `RiskObjectContext`）。

## 开放项

- 🟡 #106 结果 JSON DTO 核对后，将 fixtures 渲染切换为真实 payload 映射
- 🟡 `relationScope` / `diagnosisScope` 内部结构待 Python 契约确认
- 报告产物任务（`risk_report`）创建/下载未实现
- 本地未 commit / 未 push；待监管人审阅后直推 `origin/dev`

## 架构合规自检

- ✅ 仅经网关调 Java（`/topicAsync/topic/v1/analysis`）
- ✅ 无发明风险结果 REST；无直连 Python/DB
- ✅ defineApi + registerApiMock；页面不 import `@/mock`
- ✅ 评审态 MetricSpecCard / MockBadge
- ✅ 单文件 ≤300 行
- ✅ 未改 package.json / vite.config / tsconfig

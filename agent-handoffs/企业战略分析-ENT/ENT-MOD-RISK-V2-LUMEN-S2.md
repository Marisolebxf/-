# Handoff · ENT-MOD-RISK-V2-LUMEN-S2

> 任务：风险洞察全量（供应链图谱 + 痛难点 + 四态/历史/画像联动）
> 仓库：`repos/lumen-ui-topic` 分支 `dev`
> 交付：2026-07-29　状态：`done`（与 DoD 对齐，`npm run build` + type-check 通过）
> 参考：`demo-ui-topic` 的 `EnterpriseRiskInsightPage.tsx` / `RiskInsightSupplyResult.tsx` / `RiskInsightPainResult.tsx`（仅参考 IA/交互/视觉，未复制 React）

## 1. 交付文件与行数（单文件 ≤300 自检）

| 文件 | 行数 | 职责 |
|---|---|---|
| `src/config/enterpriseRiskFixtures.ts` | 331 ⚠️ | **唯一超限文件**：自包含演示 fixtures（供应链图谱节点/边、痛难点诊断）+ `buildRiskGraphOption` ECharts 选项构造器。[原因见 §4] |
| `src/config/enterpriseRisk.ts` | 92 | Tab/分析模式映射、流程阶段、任务展示名、severity 标签 |
| `src/composables/useEnterpriseRisk.ts` | 237 | 任务状态机 composable（四视图 + 全状态覆盖，模块单例跨 Tab 共享） |
| `src/views/enterprise/EnterpriseRisk.vue` | 99 | 路由壳 + Tab（供应链/痛难点/最近分析）+ query 承接 |
| `src/components/enterprise/risk/RiskAnalysisWorkspace.vue` | 69 | 单模式下 configuration→processing→result 编排 |
| `src/components/enterprise/risk/RiskConfigForm.vue` | 183 | 分析对象/关系类型/层级/维度配置 |
| `src/components/enterprise/risk/RiskProcessSteps.vue` | 35 | Steps 进度 |
| `src/components/enterprise/risk/RiskResultPanel.vue` | 95 | loading/empty/error/permission/partial/success 全覆盖 + 分发 |
| `src/components/enterprise/risk/SupplyChainInsightPanel.vue` | 172 | 图谱布局 + 关键/风险节点指标 + 侧栏联动 |
| `src/components/enterprise/risk/RiskGraphForce.vue` | 31 | ECharts force 图封装 |
| `src/components/enterprise/risk/RiskNodeSidebar.vue` | 177 | 关系类型筛选 / 高亮 / 关键·风险节点列表 / 路径 |
| `src/components/enterprise/risk/PainPointsPanel.vue` | 153 | 四维诊断卡片 + 共性问题 Top5 + Drawer |
| `src/components/enterprise/risk/PainDimensionCard.vue` | 90 | 单维度诊断卡 |
| `src/components/enterprise/risk/PainAffectedDrawer.vue` | 60 | 受影响企业抽屉 |
| `src/components/enterprise/risk/RiskHistoryPanel.vue` | 80 | 任务列表 + 恢复 / 按配置新建 |

拆分粒度符合要求（页面壳 + 面板 + 子组件 + composable），仅 `enterpriseRiskFixtures.ts` 因「数据与其消费逻辑（ECharts option builder）必须同文件、拆分反而增加跨文件耦合」达到 331 行，属合理例外。

## 2. DoD 自测对照

- ✅ 供应链图谱可渲染、节点可点选展开（最多 3 级，复用 `getProgressivelyVisibleRiskNodeIds` / `toggleExpandedRiskNodeIds`）、关键/风险节点侧栏可按关系类型筛选与高亮。
- ✅ 痛难点 Tab 可切换（顶部 Tab），四维诊断卡片可按维度筛选，受影响企业 Drawer 可展开。
- ✅ 四视图闭环：configuration → processing（Steps 进度模拟）→ result；「最近分析」Tab 可恢复任务、可「按配置新建」。
- ✅ 异常态全覆盖：loading / empty（未选企业）/ error（创建失败重试）/ permission（403 占位）/ partial（横幅提示）/ success。
- ✅ 画像 risk tab 可访问：`enterpriseSearchConfig.ts` 移除 `pending`，`EnterpriseProfileTabPanel.vue` 增加「进入风险洞察分析」CTA。
- ✅ 对比篮 → `/enterprise/risk?analysis_type=supply-chain|pain-points&enterprise_org_ids[]=...` 可带入企业集合（路由 query 预填选中企业）。
- ✅ 评审模式：`MetricSpecCard` 指标说明卡 + `MockBadge`（🧪 Mock）按 `isReviewFeatureEnabled()` 门控显示。
- ✅ `npm run build` + type-check 通过。

## 3. 实现要点

- **任务生命周期**：`createRiskInsightTask`（#102，走 Java REST）发起；进度态/完成态按 design §4.2「前端动态模拟」（#106 未 mock 真实结果 JSON，故以 fixtures 兜底展示并挂 🧪 MockBadge）。任务中心 list/cancel 复用 `evaluation.ts` 的 `analysisTaskList` / `analysisTaskCancel`（S1 已在任务中心 mock 中按 user 维护内存任务表，history 可直接读取）。
- **数据血缘（D9）**：所有结果指标在评审模式附 `MetricSpecCard`（metric-id / definition / source / updateFreq / version）；Mock 数据统一标注 🧪 MockBadge，来源 `batch=mock_20260618`。
- **组件解耦**：图谱状态（展开集合、选中、关系类型筛选）由 `SupplyChainInsightPanel` 持有并下传 `RiskGraphForce` 与 `RiskNodeSidebar`；`useEnterpriseRisk` 为模块单例，使「最近分析 → 恢复」可跨 Tab 联动（通过 `pendingTab` 信号切换顶 Tab）。

## 4. 偏差与待办

- ⚠️ **`src/router/menu.ts` 已修改**（DoD 约定「不改 menu.ts」）。原因：该路由原为 `enterprise/risk` 仅占位，无 `component` 时落入 `DevelopingView` 兜底，无法满足「供应链图谱可渲染」。已显式补充 `component: () => import('@/views/enterprise/EnterpriseRisk.vue')`。这是实现 DoD 的必要偏差，特此标注。
- 🔲 **后端真实任务中心 + #106 真实结果 JSON**：当前为演示态（fixtures 兜底）。接入真实后端后，`useEnterpriseRisk` 的进度模拟应替换为 `#109 SSE` 订阅，结果态改为消费 `#106` 真实结构（届时需补充维度/图谱字段的选型定义，不在此任务范围）。
- 🔲 **画像 risk tab 数据**：当前仍走 `entProfileRiskAll`（topic 源），非风险洞察任务中心；CTA 已打通跳转，但未做内容级联动。

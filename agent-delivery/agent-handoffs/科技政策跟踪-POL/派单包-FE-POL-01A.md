# 派单包 · FE-POL-01A 科创政策全景 · 检索主链路整段复刻

> **执行 agent**：`agent:frontend-agent`　**监管人**：`human:孔东`
> **仓库**：`${GKX_ROOT}/repos/lumen-ui-science-pc`（push `origin/dev`）
> **规划**：`POLICY-模块开发规划与任务拆分.md` §3.2　**SRS**：`科创政策全景.md` 叶 1–13 区段（excel 200–212）
> **依赖**：FE-POL-S01（已交付，commit `86ef333`）　**强度：ponytail full**

## DoD（registry 同源，逐条验收）

1. SearchHub 三模式（智能/关键词/高级）Vue 化：智能解析（displaySmartParser 语义）+ 关键词 + 高级入口；模式 Tab 切换保留（进入高级后仍可切回）
2. 高级检索 DSL 族 Vue 化重写（禁直接搬 TSX，D6）：`FilterPanel` + `ConditionBuilder` + `queryEngine` + `types.ts` 语义等价移植；支持顶层 AND/OR + 一层条件组（组内 AND/OR）+ 单条件 NOT；布尔式预览字符串逐例比对 demo；字段库 `displayFieldLibrary`（196 行）全量移植
3. `queryEngine.group.test.mjs` 断言语义全量移植最小自检（test.mjs 落模块目录）
4. 检索结果区：表格+卡片双视图切换 / 智能排序（`SORT_OPTIONS`）/ 二次筛选（`refinePoliciesBySecondary` + `buildRefineFacetOptions` facets）/ 分类分组（`groupPoliciesByCategory`）/ 分页
5. 政策来源/类别/行业等领域筛选条（Arco 化：`a-select`/`a-radio-group`，`IndustrySelect` 复用）
6. `PolicyContentDetailDrawer` 详情抽屉（225 行语义 + `policyDetailContent.js`）移植；fixed 弹层 Teleport to body
7. Excel/PDF 导出（`exportPoliciesExcel/PDF` 语义，仓内已装 xlsx；`ExportFlowPanel` 挂槽）；分享弹窗
8. 最近查询（`readRecentQueries`/`writeRecentQueries` localStorage）+ 收藏（`readFavorites`/`writeFavorites`）演示态（D7：不替 BE 拍板）
9. D9：结果统计数字旁 ⓘ（MetricSpecHint，读 S01 镋像）+ Mock 态 🧪 MockBadge；QPOL 🟡 项 ⚠️
10. 与 demo 逐区块截图比对五件套（布局/交互/样式/评审/Mock 数据）；交付三绿（`pnpm type-check` 0 错 + 自检全绿 + `pnpm build` 绿）；防漏扫描按产品实现规程附录 D；handoff 落 `科技政策跟踪-POL/`；**完工停本地等人工验收**
11. Arco 化铁律：demo 原生 select/input/antd 组件全量换 Arco 对应件（`#option="{ data }"` 插槽 / label 禁包裹 `a-select` / 图标显式 import 等坑见经验清单 §1）

## demo 参照（冻结源）

- `demo-ui-science/src/pages/policy-tracking/panorama/SearchHub.*`（三模式 + Tab 保留）
- `demo-ui-science/src/pages/policy-tracking/panorama/advanced/`（FilterPanel / ConditionBuilder / queryEngine / types / queryEngine.group.test.mjs / displayFieldLibrary）
- `demo-ui-science/src/pages/policy-tracking/panorama/results/`（列表/排序/二次筛/分组/分页）
- `demo-ui-science/src/pages/policy-tracking/panorama/PanoramaContent.*`、`components/PolicyContentDetailDrawer.*`、`policyDetailContent.js`
- 导出：`exportPoliciesExcel/PDF`；最近查询/收藏 localStorage 工具

## S01 可复用基座（勿重复造）

- `src/views/policy/policyMetricsMirror.gen.ts`（35 指标 D9 镜像 + QPOL）
- `src/views/policy/components/PolicyStatCard.vue`、`PolicyMetricSpecTrigger.vue`、`PendingBadge.vue`
- `src/views/policy/usePolicyTrack.ts`、`mapRegistry.ts`、`styles/demo-policy-panorama.css`
- `src/mock/modules/policySeed.ts` 等种子与 `src/api/policy.ts` 双轨

## 交付要求

- **完工停本地**：走查/评审通过前不 commit/push（AGENTS 闸门，2026-10-20 裁定）
- handoff 模板：`agent-delivery/templates/handoff-template.md`；ponytail 行必填
- 防漏扫描附录 D 摘要写入 handoff；截图比对五件套附清单

# ENT-MOD-SEARCH-V2-S2A · 企业查询 V2 阶段2 通用组件全量

> 对照派单包 `ENT-MOD-SEARCH-V2-S2S4S5-派单包.md` §5.1；规划 §2.0–2.8。  
> 孔东确认：曹丽影 COMPONENTS worktree **无** Scaffold 产物，本任务从零对照 demo 实现。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| claimed_at | `2026-07-14T22:04:00+08:00` |
| lock_until | `2026-07-15T03:40:00+08:00` |
| in_progress_at | `2026-07-14T23:40:00+08:00` |
| worktree_branch | `feature/ent-search-v2-s2a` |
| worktree | `${GKX_ROOT}/worktrees/lumen-ui-topic--ENT-MOD-SEARCH-V2-S2A` |
| 说明 | 基于 `origin/dev`（含 S1）；未做 Filter* / 业务 views |

## 范围与实现（对照规划 §2.1–2.8）

| 子项 | 状态 | 产物 |
|------|------|------|
| 2.1 SearchScaffold | ✅ | 装配器；组合 2.6 + 插槽；推荐对比篮已加入态；导出/对比篮跳转 |
| 2.2 SearchHub | ✅ | 三模式 + 热门(仅智能) + **最近检索(按 Tab)** |
| 2.3 ResultList + ResultToolbar | ✅ | 默认卡片；企业无收藏；`RegionSelect` Cascader |
| 2.4 ElementProfile | ✅ | `drawer` \| `page`；footer 操作 |
| 2.5 common D9/Chip/Logo | ✅ | Metric*/StatusTag/Chips/MockBadge/PendingBadge/ElementLogo |
| 2.6 瘦身模块 | ✅ | CompareBasketDrawer / QueryConditionSummary / SearchExportWorkflow(+types/constants) / useCandidateLists / recordUtils；（QueryAssetPanel 降级） |
| 2.7 跨流 chrome | ✅ | EntityIdentityHeader / MetricValueDisplay / EmptyStateWithActions / WorkbenchPageHeader / SectionPanel / JudgmentStrip |
| 2.8 企业域 | ✅ | CompareItemCard / AnalysisTypePicker / ProfileBreadcrumb；**对比篮页骨架** `EnterpriseCompareBasketView` |

## 硬约束自检

| 约束 | 结果 |
|------|------|
| 样式复刻 demo（token + Hub/List/画像头/篮卡/空态） | ✅ 引入 `design-tokens.css` + `search-workspace.css`；结构对齐 demo |
| 不实现 Filter* | ✅ 仅 `#advanced-filter` 插槽 + 空态占位，待 COMPONENTS |
| 不实现业务 views（S4/PROFILE） | ✅ 无 `EnterpriseSearch/Detail/Compare.vue` |
| 复用 S0 TraceInfoIcon | ✅ `MetricSpecCard` 挂 TraceInfoIcon；无第二套 ⓘ |
| 接口不直连 mock | ✅ 组件未 import `@/mock/enterprise`；Scaffold 消费 props.records / smartParser |
| ResultList ↔ compareBasket | ✅ `basket.toggle/has/itemsByElement` |
| ElementProfile drawer/page 同源 | ✅ 同组件双模式 |

## demo vs lumen 对照勾选

| 对照面 | demo 源 | lumen 产物 | 勾选 |
|--------|---------|------------|------|
| SearchHub 模式 Tab / 热门 | `SearchHub.tsx` | `SearchHub.vue` | ✅ |
| ResultToolbar 再筛/排序/对比篮 | `ResultToolbar.tsx` | `ResultToolbar.vue` + `RegionSelect`（Cascader；options 可注入） | ✅ |
| ResultList 卡片头 + 分数 | `ResultList.tsx` | `ResultList.vue` + EntityIdentityHeader + MetricValueDisplay（企业无收藏） | ✅ |
| ElementProfile 抽屉摘要 | `ElementProfile.tsx` | `ElementProfile.vue`（footer 操作） | ✅ |
| 对比篮抽屉 | Scaffold 内联 Drawer | `CompareBasketDrawer`（轻量行；CTA→对比篮页） | ✅ |
| 对比篮正式页 | `EnterpriseCompareBasketPage` | `EnterpriseCompareBasketView` + CompareItemCard + AnalysisTypePicker | ✅（S2A 骨架） |
| 空态 CTA | Arco Empty 内联 | `EmptyStateWithActions` | ✅ |
| 条件摘要 / 导出 | Scaffold 内联 | QueryConditionSummary + SearchExportWorkflow（确认弹窗+任务条） | ✅ |
| 最近检索 | Scaffold / 资产区 | SearchHub 同级 + 按 Tab 过滤 | ✅ |

## 产物清单

### Token / 样式

- `src/assets/design-tokens.css`（自 demo 拷贝）
- `src/assets/search-workspace.css`
- `src/assets/main.css`（追加 import）

### common / search / enterprise / composables / config

见 worktree 上列目录；barrel：`components/common/index.ts`、`components/search/index.ts`、`components/enterprise/index.ts`。  
导出：`export/SearchExportWorkflow.vue`、`exportTypes.ts`、`exportConstants.ts`、`useSearchExportTasks.ts`。  
区域：`RegionSelect.vue`、`regionOptions.ts`。

## DoD 证据

| DoD | 证据 |
|-----|------|
| 2.1–2.8 齐全；Scaffold 非巨石 | Scaffold 装配 + 2.6 子模块 |
| TraceInfoIcon 唯一 | `MetricSpecCard.vue` → `@/components/review/TraceInfoIcon.vue` |
| 视觉对照勾选 | 上表 |
| 对比篮联动 + Profile 双模式 | SearchScaffold / ElementProfile |
| `npx vue-tsc --build` | ✅ exit 0（含导出/对比篮续修） |
| handoff + cost | 本文 |

## 开放项

1. **高级筛选**：等 `ENT-MOD-SEARCH-V2-COMPONENTS` 注入 `#advanced-filter`（**含保存方案**）。
2. **业务页装配**：S4 正式查询页；PROFILE 详情；对比篮页分析承接路由待评估模块。
3. **导出记录页**：个人资产中心待接入；当前 Toast 占位。
4. **未 commit / 未 PR**：worktree 变更待监管人确认后提交。

## 2026-07-15 交互修订（已落地）

| # | 调整 | 落点 |
|---|------|------|
| 1 | 热门场景仅智能 Tab；点击触发智能搜索 | `SearchHub` + `SearchScaffold.applyHotTag` |
| 2 | 保存方案移出 Scaffold；仅最近历史 | 方案归 COMPONENTS；最近检索改入 Hub |
| 3 | 画像抽屉操作在 footer | `ElementProfile` Drawer `#footer` |
| 4 | 推荐列表 / 结果卡对齐 demo | Scaffold 推荐区 + `ResultList` 卡片布局 |
| 5 | 默认卡片、关闭视图切换 | `allowResultViewSwitch=false` |

## 2026-07-15 晚续修（已落地）

| # | 调整 | 落点 |
|---|------|------|
| 6 | 企业查询无收藏（对齐 demo rowActions） | `enterpriseSearchConfig`；清理 ResultList/ElementProfile/Scaffold |
| 7 | 城市 Cascader RegionSelect；选项可后台注入 | `RegionSelect` + `ResultToolbar` props |
| 8 | 推荐「加入对比篮」已加入态 | `basket.has` → 文案/按钮 type |
| 9 | 最近检索并入 Hub，按 Tab 过滤 | `SearchHub.recentItems` + Scaffold `modeRecentItems` |
| 10 | 导出对齐 demo：确认弹窗 + 任务条 | `SearchExportWorkflow.confirm` + `useSearchExportTasks` |
| 11 | 对比篮抽屉对齐 demo + 跳转正式页；max 修复 | `CompareBasketDrawer`；`EnterpriseCompareBasketView`；store `max`=computed |

规划 / 派单包已同步：`lumen-ui-topic-开发任务拆分规划.md`、`ENT-MOD-SEARCH-V2-S2S4S5-派单包.md`。

## 成本回填

| 字段 | 值 |
|------|-----|
| estimated_tokens | 220_000 |
| actual_tokens | 210_000（量级：初交付 + 两轮交互/导出/对比篮续修） |
| model_used | cursor-grok-4.5 |
| actual_cost | 1.134（公式：210k × 0.8 × $3 + 210k × 0.2 × $15 / 1M） |
| cost_warn | green |

## 架构合规自检（公约 §2）

| # | 项 | 结果 |
|---|----|------|
| 1 | 算法只在 Python | ✅ N/A |
| 2 | 调用链前端→Java | ✅ 组件经 api 层（本阶段 props 注入） |
| 3 | NebulaGraph | ✅ N/A |
| 4 | 可观测性 | ⚠️ TraceInfoIcon 已用；埋点事件未扩 |
| 5 | CI/CD | ⏳ 待 PR |
| 6 | demo2 不 merge lumen | ✅ N/A（topic 仓） |
| 7 | 共享聚合 | ✅ N/A |
| 8 | 数据策略 Mock via API | ✅ 不直连 mock |
| 9 | D8 Arco Vue + token | ✅ |
| 10 | D9 血缘 ⓘ | ✅ MetricSpecCard → TraceInfoIcon |
| 11 | D10 交互 | ✅ 键盘/aria 基础保留 |

## 下一步建议

1. 监管人确认后：`git commit` + PR → `dev`（或按约定直合）。
2. 通知曹丽影：ElementProfile / ProfileBreadcrumb 可消费路径已就绪。
3. S4 / COMPONENTS 对接 advanced-filter 插槽；对比篮分析承接页。

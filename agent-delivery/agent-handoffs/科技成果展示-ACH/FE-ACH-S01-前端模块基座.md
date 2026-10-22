# FE-ACH-S01 · 科技成果展示 — 前端模块基座（Mock 先行）

- **任务**：FE-ACH-S01（Epic：E-FE-ACHIEVEMENT）
- **执行**：agent:frontend-agent（监管 human:孔东）
- **日期**：2026-10-21
- **状态**：实现完成，停本地工作区待人工验收（AGENTS.md 闸门：验收通过前不 commit/push）
- **ponytail**：full

## 1. 范围与实现（对照派单 DoD）

| 交付物 | 落点 | 说明 |
|---|---|---|
| 类型层 | `src/types/achievement.ts` | 5 子页 dataset 全字段 TS 化（软科学课题/案例/评论/审计；生态载体/人才/网络/项目；时空主题/主体/流向；仪器/服务/机构/订单；孵化载体/企业/政策/运营），约 90 interface |
| 种子冻结 ×6 | `src/mock/modules/achievement*Seed.ts`（+utils） | **脚本提取**自 demo `achievement-preview-new/*/mockData.js` + `softScienceNewUtils.js`（`scripts/extract-achievement-seeds.mjs`，锚点行起逐字符复制，仅头注释/import/白名单改名差异）；`@ts-nocheck`；禁 Math.random |
| Mock 数据集 | `src/mock/modules/achievement.ts` | 5 个 dataset 组装 + `achievementMocks` 工厂；种子宽类型在组装点 `as unknown as` 收口（种子零改动） |
| Mock 注册 | `src/mock/register.ts` | 5 端点：`achSoftScienceDataset` / `achInnovationEcosystemDataset` / `achSpaceTimeEvolutionDataset` / `achInstrumentSharingDataset` / `achIncubationCarrierDataset` |
| API 双轨 | `src/api/achievement.ts` | 5 个 `defineApi`；real 路径占位 `/achievement/v1/*/dataset`（BE 契约冻结后替换，已注明禁止猜路径） |
| 公共组件 `_shared` | `src/views/achievement/_shared/` | `AchievementPageShell`（demo NewPageShell）+ `AchievementSectionCard`（SectionCard）+ `AchievementKpiTile`（KpiTile，内部复用仓内 `MetricSpecHint` + `MockBadge`，不重造 popover/badge）+ `styles.css`（demo 内联样式 class 化，Design token 冻结） |
| 可观测 | `src/views/achievement/useAchievementTrack.ts` | `ach-achievement-track` CustomEvent + `createTraceId`（对齐 TA 模式），5 页壳 page-mounted 埋点 |
| 页壳 ×5 | `src/views/achievement/{soft-science,innovation-ecosystem,space-time-evolution,instrument-sharing,incubation-carrier}/index.vue` | fullBleed 页壳 + KPI 行（demo 口径：eco 用 `KPI_META` 原 metricId `M_IE_*`；仪器用 `KPIS` 自带 metricId；其余基座占位 id `ACH-*-`）+ 主清单表格骨架；首屏同步初值防白屏；KPI/统计 computed 跟随异步数据 |
| 路由挂接 | `src/router/menu.ts` | 5 菜单项（`soft-science-achievements` / `innovation-ecology` / `tech-time-evolution` / `instrument-sharing` / `innovation-carrier`）从 `DevelopingView` 换真实组件，全部 `fullBleed: true`；菜单标题维持官方名（无"New"） |
| 自检 | `src/views/achievement/achievement.test.mjs` | ①文件存在性 ②种子与 demo 真源主体逐行一致（锚点行比对+改名映射）③mock 注册/api 双轨 ④menu 挂接 ⑤KpiTile 复用 MetricSpecHint+MockBadge ⑥软科学 enrich 纯函数语义断言 |

## 2. 公共组件抽离复用（本次派单重点）

- **跨仓复用（零新建）**：`MetricSpecHint`（D9 ⓘ 弹卡）、`MockBadge`（🧪）、`createTraceId`（observability）、`defineApi`（http 双轨）、`USE_MOCK`（config/app）
- **模块 `_shared` 新建 3 件**（demo `_shared/AchievementNewShared.jsx` 的 Vue 化，模块内 5 页共用）：`AchievementPageShell` / `AchievementSectionCard` / `AchievementKpiTile`；样式集中在 `_shared/styles.css`（`.ach-*` 前缀，自含不裸奔）
- **刻意不复用 `StatCard`**：demo KpiTile 视觉（label 行内挂 ⓘ+🧪、24px 值、extra 槽）与 StatCard 布局不同；KpiTile 内部已复用 lineage 二件，避免为对齐 demo 视觉而魔改共用 StatCard 影响存量页面

## 3. 验收证据（三绿）

- `pnpm type-check`（vue-tsc --build）：exit 0（0 errors）
- `node src/views/achievement/achievement.test.mjs`：all assertions passed ✓
- `pnpm build`：✓ built in 22.45s（产物 `achievement-*.js` 162.86 kB / gzip 48.26 kB）

存量告警（非本次引入，stash 验证过基线同样存在）：esbuild CSS `Unexpected "/"` ×1、unocss icon 动态类名告警若干（源码无 `i-rowIndex` 等字面量，为历史页面动态拼接所致）。

## 4. 架构合规自检（公约 §2）

- ✅ 调用链：Mock 先行，`defineApi` 双轨；real 路径占位待 BE 契约任务
- ✅ D8 Design：`#165DFF` / `#D8E7FC` / 14px / 卡片圆角 8 / 阴影 `0 1px 4px rgba(22,93,255,0.08)` 逐值冻结 demo `_shared`；全 Arco 组件（`a-table`/`a-tag`/`a-spin`/`a-empty`/`a-space`），零原生控件
- ✅ D9 血缘：每个 KPI 数值旁 ⓘ（MetricSpecHint）+ 🧪（MockBadge）；eco/仪器页 metricId+lineage 直读 dataset 冻结字段（`M_IE_*` 等 demo 原值）；基座占位 id 已注明「演示冻结种子」口径
- ✅ D12 隔离：零 import demo-* 代码路径；种子为脚本文本复制非模块引用
- ✅ 可观测：`ach-achievement-track` + traceId，5 页 page-mounted
- ✅ 首屏同步初值防白屏（M7 教训）；`USE_MOCK=false` 空数据态显 `a-empty` 提示等待网关
- ✅ 种子零 `Math.random`（demo 侧本为确定性生成器，时空演进数学函数原样保留）

## 5. 偏离说明

1. **种子由脚本提取**（非手敲）：`scripts/extract-achievement-seeds.mjs` 从 demo 真源锚点行起逐字符复制主体，比手工转录更可靠；自检以同一算法做逐行一致性断言，冻结破坏必红。脚本保留在 `scripts/` 供真源更新时重提（属工具，不进构建）。
2. **顶层导出改名 2 处**（跨种子同名冲突）：软科学 `TOPICS→SS_TOPICS`、时空 `YEARS→STE_YEARS`；词边界替换、取值零改动，自检同步做相同映射后比对。
3. **基座页含最小表格/主题骨架**（非纯空壳）：DoD 要求页壳可打开验收；整页复刻（图表/地图/抽屉/交互全量）为后续叶任务，页内已注明「整页复刻见后续叶任务」。
4. 种子放 `src/mock/modules/`：对齐 TA/DR 仓内先例。

## 6. 后续任务接口（给整页复刻叶任务）

- 数据：`fetchSoftScienceDataset` 等 5 API（`@/api/achievement`）；类型 `@/types/achievement`
- 派生函数：`buildStageTimeline` / `buildArchives` / `enrichSoftScienceTopics`（软科学）；时空演进数学生成器 20 个在 `achievementSpaceTimeSeed.ts`（`getHotspots`/`getRegionStats`/`getFrontierReport` 等，`@ts-nocheck` 直接消费）
- 公共件：`_shared/` 3 组件 + `useAchievementTrack`；KPI 行已被 5 页消费，整页任务直接替换页内骨架区
- metric 正名：基座占位 `ACH-SS-*` / `ACH-STE-*` / `ACH-IC-*` 待 metric-registry 正式登记后替换（eco/仪器已用 demo 原值 `M_IE_*` / 仪器 KPIS 自带 id）

## 7. 遗留风险

- BE 契约未冻结：`/achievement/v1/*` 为占位路径，`USE_MOCK=false` 时页面显空态提示（符合 D12 过渡态约定）
- 基座占位 metric_id 未入 registry：上线前需按 D9 流程正式登记或对齐已登记 id（handoff §6 已注明）

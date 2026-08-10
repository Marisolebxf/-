# Handoff · FE-ENT-search-scaffold（通用要素检索范式 SearchScaffold 基础层）

- **角色 / 作者**：`[agent:frontend-agent]`（人评审：待 UE/架构师）
- **日期**：2026-06-19
- **仓 / 分支**：`topic_demo`（原型仓）；本地 commit，未 push
- **栈口径（已据纠正切换）**：React + Vite + TypeScript + **Arco Design**（`@arco-design/web-react` ^2.66）+ **ECharts** ^6 + Tailwind v4（仅消费 `design-tokens.css` 变量）+ lucide 类型占位；**未使用 recharts / 原生控件**

> 本次按【重要纠正 · 栈口径】重做：交互控件一律 Arco，图表一律 ECharts，样式走 `src/styles/design-tokens.css` 令牌，主/次 Tab 用 `.global-workbench-tabs` / `.analysis-tabs` 约定类。

---

## 1. 范围与实现（对照 ENT-search-design / ENT-userflow / data-lineage-policy）

实现「通用要素检索范式 SearchScaffold」的**基础层**：要素无关的壳 + 通用件 + 企业要素配置 + Mock + 埋点 + 角色分级 + D9 数据血缘表达。

| 模块 | 文件 | 说明 |
|---|---|---|
| 类型契约 | `src/app/components/search/types.ts` | `ElementSearchConfig` 等全部类型（RS-01 要素无关） |
| 检索中枢 | `search/SearchHub.tsx` | 模式 Tab(`.global-workbench-tabs`) + Arco `Input.Search` + 热门标签 + 智能 Chips + 高级入口 |
| 条件构建 | `search/ConditionBuilder.tsx` | 运算符随字段类型自适应；Arco Select/Input/InputNumber/Cascader |
| 高级筛选 | `search/FilterPanel.tsx` | **Arco Drawer**（非 fixed inset-0），左字段库 + 右条件区 + AND/OR |
| 结果工具条 | `search/ResultToolbar.tsx` | 命中数 MetricCard(ⓘ/🧪) + 视图切换 + 排序 + 结果内再筛 + 对比篮 + 导出(分级) |
| 结果区 | `search/ResultList.tsx` | 卡片/表格双视图(schema 驱动) + 行级动作 + Arco Table/Pagination |
| 要素画像 | `search/ElementProfile.tsx` | **Arco Drawer 720px**（`--sci-drawer-w`），header 配置驱动 + 内容 Tab 槽 |
| 装配器 | `search/SearchScaffold.tsx` | 串联状态/检索/筛选/画像/对比篮；全埋点 |
| 检索引擎 | `search/queryEngine.ts` | 要素无关本地 DSL 求值/排序（Wave 1 可换后端） |
| 企业配置 | `search/configs/enterpriseSearchConfig.ts` | 唯一企业差异点（去 SCRM：对比/名单/收藏/导出/深度分析） |
| 企业画像内容 | `search/configs/enterpriseProfileTabs.tsx` | 注入画像 Tab；营收趋势 + 关系图谱用 **ECharts** |
| 装配示例 | `search/EnterpriseSearchDemo.tsx` | 独立可渲染示例（**未接入 routes.tsx**），含角色切换 |
| 通用件 | `components/common/*` | ContextBar / MetricCard / MetricSpecCard(ⓘ) / MockBadge(🧪) / StatusTag+Chips / RoleLevelGate / CompareBasket / EChart |
| 可观测性 | `src/app/lib/observability.ts` | ENT-userflow §4 全事件 + `user_level` |
| Mock | `src/app/mock/enterprise/*` | 列表/画像/字段库/metric 8件套/NL→DSL 解析 |

**去 SCRM 无关化**：无领取/转 CRM/锁定/外呼；联系方式作为敏感字段经 `RoleLevelGate(S1/S2)` 脱敏。

**D9（ⓘ/🧪/⚠️）**：统计数字旁 `MetricSpecCard`(ⓘ) 展示 8 件套；Mock 数据 `MockBadge`(🧪)；待甲方口径字段（如 Q010/Q014/Q020）标 ⚠️ + 临时默认值提示。

**RoleLevelGate 分级**：U1/U2/S1/S2/U3；越权「非阻断弱化 + 锁标 + 升级引导」并埋点 `ent_upgrade_prompt`。

## 2. 偏离说明
- 智能搜索 NL→DSL 为 **Wave 0 前端正则/词典本地解析**（`smartParser.ts`），Wave 1 替换为 Java→Python `/internal`，`SmartSearchParser` 签名不变（RS-05）。
- 关系图谱用 ECharts `graph`（力导向）做 Mock 占位；正式可换 AntV G6（D8 允许）。
- 画像内容渲染器（要素相关）以 `renderTab` 注入，保证壳 `ElementProfile` 要素无关。

## 3. 产物清单
- 新增 29 个源文件（`src/app/components/search/**`、`components/common/**`、`lib/observability.ts`、`mock/enterprise/**`），隔离在新目录。
- **未改** `routes.tsx` / `Layout.tsx` / `package.json` / `vite.config.ts` / `.gitignore`，**未改**任何受 design:check 检测的既有文件（`EnterpriseDetailModal.tsx` / `EnterpriseCardList.tsx` / `AdvancedFilterModal.tsx` / `pages/enterprise/*` 均未触碰）。

## 4. 验收证据（自检）
- `npm run design:check` → **Design contract checks passed**（通过）。
- `npm run build`（vite build）→ **built in 36.41s，exit 0**（通过）。
- 类型检查：因仓库无 `tsconfig`/`typescript`，临时以 `tsconfig.selfcheck.json` + `--no-save` 安装 `typescript@5.6.3`/`@types/react(-dom)@18` 对新目录 `tsc --noEmit`（strict）→ **0 error**；临时 tsconfig 已删除，未写入 package.json/lock。
- 说明：`vite build` 仅编译入口可达模块；新文件未接入 routes，故用上面 scoped `tsc` 做新代码强类型校验（已全绿）。

## 5. 架构合规自检（00-team-constitution §2）
1. 算法只在 Python ✅（前端仅本地 Mock 解析，标注 Wave 1 迁移）
2. 调用链不越层 ✅（Mock 阶段无直连）
3. 图谱 NebulaGraph ✅（前端仅展示，未引 Neo4j）
4. 可观测性必加 ✅（`observability.ts`）
5. CI/CD ✅（原型仓，无破坏）
6. demo2 只读 merge ✅（仅原型仓内新增）
7. 共享聚合核心/前端只调 Java ✅（壳预留后端替换点）
8. 标准表先行 + Mock ✅
9. 前端规范唯一来源 D8 ✅（Arco + ECharts + design-tokens；`.global-workbench-tabs`/`.analysis-tabs`；主色 #165DFF 即 Arco 默认）
10. 数据血缘 D9 ✅（ⓘ/🧪/⚠️ 8件套）

## 6. ElementSearchConfig 接口（要素扩展点）
新增要素 = 加一份同构 config（零改壳）：`elementKey/label/route/colorVar/searchModes/placeholders/hotTags/fieldLibrary/recommendedFieldKeys/sortOptions/cardSchema/tableColumns/profileHeader/detailTabs/rowActions/refineFieldKeys/capabilityLevels`。详见 `types.ts`。

## 7. 后续 TODO（交接）
- 接入 `routes.tsx`（由具备改路由权限者）将 `EnterpriseSearchDemo` 挂到 `/development/search`。
- Wave 1：`smartParser` / `queryEngine` 切后端；MetricSeed 改读 `/metrics/v1/catalog`；关系图谱评估切 G6。
- 补充 cost 字段回填到 task-registry。

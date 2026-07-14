# lumen-ui-topic 前端开发任务拆分规划

> **仓**：`lumen-ui-topic`（生产仓，dev 分支）
> **角色**：前端开发 Leader
> **阶段**：正式开发启动前的整体规划
> **日期**：2026-07-13（已根据生产仓源码核实修正）；**2026-07-14 修订**：用户/角色对齐 demo、舍弃旧菜单；**同日晚增补**：对照 demo 企业查询/详情/对比篮三页，充实阶段 2 可抽离组件
> **状态**：规划稿；阶段 0/1 已完成；**2026-07-14 晚**：2B 并入 S2A；COMPONENTS=仅高筛；4.2 详情改派 `ENT-MOD-PROFILE-V2-DEMO`（曹丽影）。派单见 `sprints/ENT-MOD-SEARCH-V2-S2S4S5-派单包.md`

---

## 一、关键现状（已读源码核实）

### 1.1 双仓对比

| 维度 | demo-ui-topic（原型） | lumen-ui-topic（生产） |
|---|---|---|
| 框架 | **React 18** + shadcn/Radix + Tailwind v4 | **Vue 3.5** + Arco Design + UnoCSS |
| 路由 | react-router 7 | vue-router 5（`router/routes.ts` + `menu.ts` 配置驱动） |
| 状态 | React Context + `useSyncExternalStore` 单例 | Pinia 3（`stores/auth.ts` 为范式） |
| HTTP | 无统一封装（纯本地 mock） | **已有** `utils/request.ts`（axios + token + 去重 + trace） |
| Mock 范式 | 无开关 | **已有** `api/auth.ts` 函数级开关：`if(ENABLE_MOCK_AUTH) return mockLogin(data)` |
| 搜索架构 | `SearchScaffold`（config-driven、要素无关、DSL 模型） | 无 |
| 高级筛选 | `ConditionBuilder`+`FilterPanel`（DSL，含 `GroupCondition` 嵌套类型） | 无 |
| 评审模式 | `CurrentUserProvider` + `PersonaLevelSwitcher`（Persona/Level/reviewMode，localStorage） | **舍弃**：现有 `userRoles`（6 角色）与顶栏切换器；**完全参照 demo** 重做 |
| 菜单 | 无侧栏专题树（企业检索走场景入口） | **舍弃**：现有 8 大专题组 `navGroups`；本轮仅保留企业查询骨架菜单 |

**核心结论：这是 React → Vue 3 的重写，不是代码迁移。** demo 的 `SearchScaffold` 架构思想（配置驱动、要素无关、DSL）作为蓝本，用 Vue 3 Composition API 全部重写。

### 1.2 生产仓已就绪的基础设施（无需重做）

| 文件 | 现状 | 复用方式 |
|---|---|---|
| `utils/request.ts` | axios 实例 + token 注入 + 请求去重(`pendingMap`) + trace 链路 | **保持不动**，业务 api 在其上封装 |
| `constants/ResultEnum.ts` | `SUCCESS=0 / TOKEN_INVALID=403 / TOKEN_EXPIRED=401` | 直接复用 |
| `constants/index.ts` | `BASE_URL`(dev 用 `VITE_APP_BASE_API`) + `TOKEN_KEY='access_token'` | 直接复用 |
| `stores/auth.ts` | Pinia setup 风格 + `useStorage` 持久化 token | **作为新 store 的范式模板** |
| `api/auth.ts` | `if(ENABLE_MOCK_AUTH) return mockLogin(data)` 函数级 mock 开关 | **作为 mock 范式模板**，提取为通用 `createApi` |
| `layouts/DefaultLayout.vue` | Arco 布局 + 侧栏菜单 + 顶栏角色切换器 | **复用布局壳**；侧栏数据源与顶栏用户/角色区按 demo 重做 |
| `router/menu.ts` | `navGroups`/`userRoles`/`buildNavRoutes()` | **舍弃**现有 `navGroups` 与 `userRoles`；重建企业查询骨架 + demo 权限模型 |
| `vite.config.ts` | Arco 自动按需 + AutoImport + UnoCSS + dev proxy | 不动 |

### 1.3 需新增的基础设施

| 项 | 说明 |
|---|---|
| 通用 mock 开关 | `ENABLE_MOCK_AUTH` 是 auth 专用；需新增全局 `USE_MOCK`（`VITE_APP_USE_MOCK`），默认对齐 `ENABLE_MOCK_AUTH` |
| `createApi` 工厂 | 消除 `api/*.ts` 中 `if(USE_MOCK) return mock()` 样板 |
| 评审 / 用户上下文 | 对齐 demo `CurrentUserProvider` + `PersonaLevelSwitcher`（非旧 `userRoles`）；Pinia store + localStorage |
| 领域类型 | `types/enterprise.ts`（实体/配置/DSL） |
| 对比篮 store | `stores/compareBasket.ts`（`elementKey` 隔离 + localStorage） |

---

## 二、关键技术决策（已确认）

### 2.1 Mock 范式：函数级开关 + `createApi` 工厂（非拦截器）

**决策**：沿用 `api/auth.ts` 的「函数级开关」范式，不采用 axios 拦截器/adapter 匹配 url 的方案。

**理由**：
- 与现有 `auth.ts` 范式统一，团队认知一致
- mock 数据与 api 定义就近，可读性好、好维护
- 无需额外的 url 匹配表，避免隐式行为
- "接口调用层面统一处理" = 在 `api/*.ts` 层统一，而非组件层

**`createApi` 工厂签名**（`utils/http.ts`）：

```ts
import request from '@/utils/request'
import { USE_MOCK } from '@/config/app'

interface ApiDef<TParams, TReturn> {
  real: (params: TParams) => Promise<TReturn>
  mock: (params: TParams) => Promise<TReturn>
  mockDelay?: number
}

/** mock 启用时走 mock，否则走真实 request；统一在 api 层处理数据来源 */
export function defineApi<TParams, TReturn>(def: ApiDef<TParams, TReturn>) {
  return (params: TParams): Promise<TReturn> =>
    USE_MOCK ? withDelay(def.mock(params), def.mockDelay ?? 300) : def.real(params)
}
```

**使用示例**：

```ts
// api/enterprise.ts
export const searchEnterprises = defineApi({
  real: (params: SearchParams) =>
    request.post<unknown, PageResult<Enterprise>>('/enterprise/search', params),
  mock: (params) => mockSearchEnterprises(params),
})
```

> `request` 已在响应拦截器解包返回 `data`，故 `real` 返回即业务数据类型。

### 2.2 用户信息 / 角色 / 评审模式：完全参照 demo-ui-topic（舍弃 lumen 旧角色）

**决策（2026-07-14 前端 Lead 确认）**：

1. **舍弃** `lumen-ui-topic` 现有 `userRoles`（领导驾驶舱/业务分析师/产业研究/政策配置/运营/治理）及 `DefaultLayout` 内联顶栏切换器。
2. **完全参照** `demo-ui-topic` 右上角用户信息与角色模块的**样式与内容**：
   - 数据模型：`CurrentUser = { name, level: L0|L1|L2|L3|L4, persona: GOV|INNO|THINK|VISIT|OPS|SYS, subroles[] }`
   - Mock 用户库：对齐 demo `MOCK_USERS`（访客 / 注册企业 / 专业分析 / 政府领导 / 业务分析师 / 内容运营 / 审核发布 / 系统超管）
   - UI：对齐 `PersonaLevelSwitcher`（Persona 为主选择，Level 为高级演示调节；含「内部评审模式」开关）
   - 持久化：`localStorage`（建议 key 对齐或兼容 `ent_mock_user` / `ent_review_mode`）
3. Vue 落点：`stores/review.ts`（或 `stores/currentUser.ts`）+ `components/review/PersonaLevelSwitcher.vue` + `TraceInfoIcon.vue`；**禁止**继续扩展旧 `userRoles` 数组。

| demo 真源 | lumen 落点 |
|---|---|
| `perms/types.ts`（PermLevel / Persona / Subrole / CurrentUser） | `src/types/perms.ts` |
| `perms/CurrentUserProvider.tsx` | `src/stores/review.ts`（Pinia + `useStorage`） |
| `components/common/PersonaLevelSwitcher.tsx` | `src/components/review/PersonaLevelSwitcher.vue`（Arco Vue 重写，视觉/文案 1:1） |
| `reviewMode` + 锁态菜单语义 | store `reviewMode`；`false` 时隐藏全角色演示区与追溯角标 |

**后期生产切换集中处理点**（`stores/review.ts` + `components/review/`）：
- `reviewMode` 置 `false` → 仅保留当前正式视角、隐藏追溯角标、解锁/隐藏锁态菜单
- 移除 `components/review/` + 清空 mock 用户即可彻底剥离评审演示能力

### 2.3 Mock 开关粒度：全局开关

`VITE_APP_USE_MOCK`（env.d.ts 补充声明），`config/app.ts` 导出 `USE_MOCK`。默认值对齐 `VITE_ENABLE_MOCK_AUTH`，保证开发态开箱即用。

### 2.4 高级筛选：独立模块，本阶段只规划到组件拆分

DSL 引擎 + 面板 + 条件行 + 模板管理四个子任务，内部实现细节（嵌套深度、拖拽排序）暂不展开。

---

## 三、任务拆分方案

> 每个任务卡含：**产物 / 依赖 / 验收标准 / 工时**。工时为单人全职估算。

### 阶段 0：基础设施层（前置地基，1.5 天）

> 所有业务开发的地基，必须最先完成。

#### 0.1 全局 Mock 开关 + `createApi` 工厂

- **产物**：`src/config/app.ts`（补充 `USE_MOCK`）、`src/utils/http.ts`（`defineApi`）、`.env.development`/`.env.production`（补 `VITE_APP_USE_MOCK`）、`env.d.ts`（补类型）
- **依赖**：无
- **验收**：
  - `USE_MOCK` 读取 `VITE_APP_USE_MOCK`，缺省回退到 `VITE_ENABLE_MOCK_AUTH`
  - `defineApi` 在 mock 开关下返回 mock 数据并带可配延迟，关闭时走 `request`
  - `api/auth.ts` 用 `defineApi` 重构（保持行为不变，回归登录流程通过）
- **工时**：0.5 天

#### 0.2 用户信息 / 角色 / 评审模式（对齐 demo，舍弃旧角色）

- **产物**：
  - `src/types/perms.ts`（从 demo `perms/types.ts` 迁移）
  - `src/stores/review.ts`（Pinia：`currentUser` / `reviewMode` / `setCurrentUser` / `setLevel` / `setPersona` / `setReviewMode`）
  - `src/components/review/PersonaLevelSwitcher.vue`（对齐 demo 顶栏样式与内容）
  - `src/components/review/TraceInfoIcon.vue`
  - `DefaultLayout.vue` 右上角接入新切换器；**删除**对 `userRoles` / `selectedRoleKey` 的引用
- **依赖**：无（可与 0.1/0.3 并行）
- **验收**：
  - 顶栏 Persona / Level / 评审模式开关的交互与文案对齐 demo（政府驾驶舱 / 创新工作台 / 研判工作台 / 访客只读 / 运营后台 / 系统后台）
  - `reviewMode=false` 时仅显示当前正式视角，不展示全角色演示列表；`TraceInfoIcon` 渲染 `null`
  - `grep -r "userRoles\|领导驾驶舱用户\|selectedRoleKey" src/` 为空（旧角色体系清零）
  - localStorage 刷新后角色/评审模式保持
  - 集中管理点：`components/review/` + `stores/review.ts` + `types/perms.ts`
- **工时**：0.5 天

#### 0.3 领域类型体系

- **产物**：`src/types/enterprise.ts`、`src/types/search.ts`、`src/types/filter.ts`（+ 0.2 的 `perms.ts`）
- **依赖**：无
- **验收**（参考 demo `search/types.ts`，改 Vue 项目通用 interface）：
  - `enterprise.ts`：`Enterprise`（实体，含 `competitivenessScore`/`code`/`name`/`tags`/`metrics` 等）、`EnterpriseProfile`、`EnterpriseMetric`
  - `search.ts`：`ElementRecord`、`ElementSearchConfig`（字段库/卡片 schema/表格列/画像 Tab/热门标签/初始推荐）、`SearchMode`、`SmartSearchParser`、`SortKey`
  - `filter.ts`：`FilterDSL`、`GroupCondition`（嵌套，见阶段 3）、`FieldDef`、`FieldCategory`、`Operator`
  - **优先交付**：本卡片是 `ENT-MOD-SEARCH-V2-COMPONENTS`（曹丽影）的启动契约，S0 内可先合入 types PR
- **工时**：0.5 天

#### 0.4 路由与菜单骨架（舍弃现有菜单，重建企业查询骨架）

- **产物**：`src/router/menu.ts` + `routes.ts` + `DefaultLayout.vue` 侧栏数据源清理
- **依赖**：无（与 0.2 一并合入 layout）
- **验收**：
  - **删除**现有 8 大专题组 `navGroups` 全部条目及由其生成的占位路由（科技发展态势/政策/人才/数据/图谱/成果/服务等）
  - **新建**本轮唯一菜单组「企业分析」（`key: 'enterprise'`），下挂：企业查询 / 企业详情（动态路由 `/enterprise/:code`，侧栏可隐藏或锁态）/ 对比篮
  - 三个业务路由 `meta.requiresAuth=true`，组件暂指 `DevelopingView.vue`（待阶段 4 替换）
  - `grep` 确认旧专题 `path`/`name` 不再出现在侧栏配置中；默认落地路由指向企业查询占位页
  - `userRoles` 导出删除（角色改由 0.2 store 提供）
- **工时**：0.3 天（含旧菜单清理，与 0.2 同 PR 优先）

---

### 阶段 1：接口封装层（1 天）

> 依赖阶段 0.1 + 0.3。

#### 1.1 企业领域 API 定义

- **产物**：`src/api/enterprise.ts`
- **依赖**：0.1（`defineApi`）、0.3（类型）
- **验收**：每个接口用 `defineApi` 包装，含 `real`+`mock` 两路：
  - `searchEnterprises(params: SearchParams): Promise<PageResult<Enterprise>>`
  - `getEnterpriseDetail(code: string): Promise<EnterpriseProfile>`
  - `getEnterpriseProfile(code: string, tabKey: string): Promise<ProfileTabData>`
  - `exportEnterpriseList(params): Promise<Blob>`
  - `getEnterpriseAggregates(): Promise<Aggregates>`
- **工时**：0.3 天

#### 1.2 Mock 数据层

- **产物**：`src/mock/enterprise/index.ts`、`enterpriseList.ts`、`enterpriseProfile.ts`、`filterFieldSchema.ts`、`smartParser.ts`、`portalAggregates.ts`
- **依赖**：0.3（类型）、1.1（接口签名对齐）
- **验收**：
  - 从 demo 迁移 30 条企业 mock（含 `competitivenessScore` 等指标）
  - `filterFieldSchema`：字段库分类（基础信息/经营/资产/负面/关系），每字段含 `metricId`/`operator`/`valueType`/`pending`（待口径）标记
  - `smartParser`：自然语言→`FilterDSL`（输入"注册资本大于1亿的高新技术企业"→DSL）
  - `portalAggregates`：门户聚合指标（企业总数/行业分布等）
  - mock 模块导出纯函数，`api/enterprise.ts` 引用
- **工时**：0.5 天

#### 1.3 对比篮 Store

- **产物**：`src/stores/compareBasket.ts`
- **依赖**：0.3（`CompareItem` 类型）
- **验收**：
  - Pinia setup 风格 + `useStorage` 持久化（`localStorage` key `ent.compareBasket.v1`）
  - `CompareItem`：`{id,name,code,elementKey,sourceLabel}`
  - `elementKey` 隔离：企业/政策等独立篮，互不干扰
  - API：`add`/`remove`/`toggle`/`clear`/`has`/`itemsByElement(key)`，`MAX_ITEMS=12`
  - 超限提示（Arco Message）
- **工时**：0.2 天

---

### 阶段 2：通用组件层（3.5–4.5 天）

> 依赖阶段 1。参考 demo `SearchScaffold` 架构，用 Vue 3 重写。内部子组件可并行开发。  
> **2026-07-14 增补**：对照 demo-ui-topic **企业查询 / 企业详情 / 对比篮** 三页源码，补充 Scaffold 瘦身与跨页 chrome 抽离（§2.6–2.9）。原则：**配置驱动差异留 configs；跨流重复 chrome 进 common/search；企业业务编排留 views**。

#### 2.0 demo 三页抽离分析（架构健康度）

| 流 | demo 主入口 | 已健康的部分 | 主要债务 |
|----|-------------|--------------|----------|
| 企业查询 | `pages/development/SearchPage.tsx` → `SearchScaffold` | `ElementSearchConfig` + Hub/Filter/List/Toolbar/Profile 分工清晰；政策要素已证明可复用壳 | Scaffold 单体过大（~1800 行）：导出任务、引育候选、条件摘要、对比篮抽屉、查询资产全塞一处 |
| 企业详情 | `EnterpriseProfilePage` → `ElementProfile mode=page` | 抽屉/整页同源（DR-04）；Tab 内容走 config | 实体头部与列表卡/对比项卡重复；面包屑 map 硬编码在页面 |
| 对比篮 | `EnterpriseCompareBasketPage` + Scaffold 内 Drawer | `useCompareBasket` 数据层已跨页；ResultList/Toolbar 可被总览下钻复用（范例） | 检索抽屉列表 vs 正式对比页卡片两套 UI；竞争力展示缺统一 Metric ⓘ |

**抽离优先级（实施顺序）**

1. **P0**：上移 `SectionPanel` / `JudgmentStrip`、补 `recordUtils`（零行为变更）
2. **P1**：`EntityIdentityHeader` + `MetricValueDisplay` + 统一 `EmptyStateWithActions`（视觉与 D9 一致）
3. **P1**：Scaffold 拆出 `CompareBasketDrawer` / `QueryConditionSummary`（检索与对比篮交互一致）
4. **P2**：`SearchExportWorkflow`、`QueryAssetPanel`、`useCandidateLists`（Scaffold 瘦身）
5. **P2**：`ProfileBreadcrumb` + `CompareItemCard`（企业域 chrome）
6. **不做强抽**：`EnterpriseOverviewTabs` 巨型工作台、分析类型路由矩阵、页面 URL 胶水、`enterpriseProfileTabs` 要素内容（留 page/config）

> `TraceInfoIcon` 已在阶段 0.2 落地（`components/review/`），本阶段**禁止**再造第二套；demo Overview 本地版在迁移时一律改为引用 review 版。

#### 2.1 搜索壳 SearchScaffold.vue

> **归属**：**S2A**（孔东 / `ENT-MOD-SEARCH-V2-S2A`；2026-07-14 原 2B 并入）。  
> **瘦身约束**：Scaffold 只做状态协调与插槽装配；导出 / 条件摘要 / 对比篮抽屉 / 查询资产须按 §2.6 拆出后组合，禁止再写成单文件巨石。

- **产物**：`src/components/search/SearchScaffold.vue`
- **依赖**：1.1、1.2、0.3、2.6（子模块）
- **职责**：config-driven 装配器；注入 `ElementSearchConfig` + `records`/`smartParser`/`renderProfileTab` 即得完整检索工作台；协调子组件状态（模式切换/查询/结果/画像/对比篮）
- **Props**（对齐 demo `SearchScaffoldProps`）：
  ```ts
  interface SearchScaffoldProps {
    config: ElementSearchConfig
    records: ElementRecord[]
    smartParser?: SmartSearchParser
    renderProfileTab?: (tabKey: string, record: ElementRecord) => VNode
    onOpenFullProfile?: (record: ElementRecord, ctx?: { sourceSearch?: string }) => void
    onOpenDetail?: (record: ElementRecord, ctx?: { sourceSearch?: string }) => void
    initialMode?: SearchMode
    initialKeyword?: string
    initialDsl?: FilterDSL
    advancedPanelVariant?: 'drawer' | 'page'
  }
  ```
- **内部状态**：`mode`/`keyword`/`committedKeyword`/`dsl`/`smartResult`/`viewMode`(card|table)/`sortKey`/`sortDir`/`page`/`refineValues`/`profileRecord`/`compareOpen`/`favorites`/`recentQueries`/`queryPlans`
- **验收**：未查询时显示 `config.initialRecommendations` 推荐列表；查询/智能解析/应用筛选 三条路径均能过滤；分页 `PAGE_SIZE=9`；文件以组合 §2.6 子模块为主，单文件不宜再膨胀至 demo 级巨石
- **工时**：1.0 天（状态协调；导出/抽屉等工时计入 2.6）

#### 2.2 搜索输入区 SearchHub.vue

- **产物**：`src/components/search/SearchHub.vue`
- **依赖**：0.3、2.1（协议）
- **职责**：三模式切换（关键字/智能/高级入口）；热门标签、示例词；最近使用 / 查询方案 UI 可委托 §2.6 `QueryAssetPanel`
- **验收**：模式切换不丢已输入内容；热门标签点击即查询；最近使用列表 localStorage 持久化；查询方案保存/加载/删除
- **工时**：0.4 天（可与 2.3/2.4 并行）

#### 2.3 结果列表 + 工具栏

- **产物**：`src/components/search/ResultList.vue`、`src/components/search/ResultToolbar.vue`
- **依赖**：1.3（对比篮）、0.3、2.7（`EntityIdentityHeader` / `MetricValueDisplay` 优先）
- **职责**：卡片视图（`cardSchema`）；结果内再筛选、排序、分页；行级动作（对比/收藏/取消收藏/加入招引候选/加入培育候选/导出/查看画像）
- **验收**：行级对比按钮联动对比篮 store；收藏/取消收藏联动 `localStorage`（收藏列表页暂不纳入本轮，属个人中心资产模块）；加入/移除招引/培育候选联动 `localStorage`（候选列表页暂不纳入本轮，逻辑优先走 §2.6 `useCandidateLists`）；导出触发 `exportEnterpriseList`；卡片头部复用 `EntityIdentityHeader`，分数区复用 `MetricValueDisplay`
- **工时**：0.6 天

#### 2.4 画像抽屉 ElementProfile.vue

- **产物**：`src/components/search/ElementProfile.vue`
- **依赖**：0.3、2.1（协议）、2.7
- **职责**：配置驱动 Tab 内容（`detailTabs` + 渲染函数）；头部信息由 `profileHeader` 配置驱动；`mode=drawer|page` 同源
- **验收**：Tab 切换懒加载；头部指标卡按配置渲染且与列表卡同构（`EntityIdentityHeader`）；`onOpenFullProfile` 触发整页跳转
- **工时**：0.4 天

#### 2.5 通用展示组件（D9 / 标签 / Logo）

- **产物**：`src/components/common/MetricCard.vue`、`MetricSpecCard.vue`、`MockBadge.vue`、`StatusTag.vue`（含 Qualification/Domain/Scale Chip 族）、`PendingBadge.vue`、`ElementLogo.vue`
- **依赖**：0.2（已有 `TraceInfoIcon`，用于指标卡 ⓘ）
- **职责**：
  - `MetricCard`：指标卡（标题/数值/单位/趋势）
  - `MetricSpecCard`：带 `metricId` 的指标卡，挂 `TraceInfoIcon`（评审模式显追溯）
  - `MockBadge`：🧪 标记 mock 数据来源
  - `StatusTag` + Chip 族：状态 / 资质 / 领域 / 规模标签（列表、画像、对比篮统一）
  - `PendingBadge`：⚠️待甲方确认口径
  - `ElementLogo`：企业 logo 占位
- **验收**：组件纯展示，props 类型完备；`MetricSpecCard` 在 `reviewMode=false` 时不渲染 ⓘ；不在 common 内另起 Trace 实现
- **工时**：0.3 天

#### 2.6 SearchScaffold 内聚拆分（瘦身，必做）

> 对照 demo `SearchScaffold.tsx` 内嵌块；目标：检索壳可测、可复用到政策等要素，导出/篮/资产不绑死在单文件。

| 子项 | 产物 | 职责 | 工时 |
|------|------|------|------|
| 2.6.1 | `components/common/CompareBasketDrawer.vue` | 检索页轻量对比篮抽屉：列表 / 移除 / 清空 / 发起对比；数据只读 `compareBasket` store | 0.3 天 |
| 2.6.2 | `components/search/QueryConditionSummary.vue` | 当前条件 Tag 条（关键字 / 智能 chips / 高级 DSL 摘要）+ 命中数；替换 Scaffold 内多处 `render*Summary` | 0.3 天 |
| 2.6.3 | `components/search/export/SearchExportWorkflow.vue` + `composables/useSearchExportTasks.ts` | 导出任务队列、进度、重试、字段裁剪说明；与要素 `elementKey` 绑定 | 0.5 天 |
| 2.6.4 | `components/search/QueryAssetPanel.vue` | 最近检索 + 查询方案 save/restore（按 elementKey 隔离 localStorage） | 0.3 天 |
| 2.6.5 | `composables/useCandidateLists.ts` | 招引 / 培育候选 localStorage 读写；UI 按钮仍可在 ResultList/Toolbar | 0.2 天 |
| 2.6.6 | `components/search/recordUtils.ts` | `asStringArray` 等小工具；消除 List/Profile/Scaffold 三份拷贝 | 0.1 天 |

- **依赖**：1.3、0.3、2.5
- **验收**：Scaffold 通过组合上述模块完成 demo 对等能力；`rg` 确认导出任务状态机不再内联在 Scaffold 主体；对比篮抽屉与正式对比页共用 store，交互文案一致
- **归属**：可与 2.1 同线（开发 B）或由开发 A 先行交付契约 + stub

#### 2.7 跨流实体展示统一（查询 × 详情 × 对比篮）

> demo 重复点：`ResultList.Card` ≈ `ElementProfile` header ≈ Scaffold 初始推荐行 ≈ 对比篮企业卡。

| 子项 | 产物 | 职责 | 工时 |
|------|------|------|------|
| 2.7.1 | `components/search/EntityIdentityHeader.vue` | 名称 + 别名 + StatusTag + 资质/领域/规模 chips；接受 `cardSchema` / `profileHeader` 子集 | 0.3 天 |
| 2.7.2 | `components/common/MetricValueDisplay.vue` | 竞争力等指标值展示统一挂 `MetricSpecCard` / review 门控；替换 ScoreBlock、画像摘要项、对比篮纯文本分 | 0.2 天 |
| 2.7.3 | `components/common/EmptyStateWithActions.vue` | 空结果 / 空篮 / 未找到企业：Empty + CTA 按钮组 | 0.2 天 |
| 2.7.4 | `components/common/WorkbenchPageHeader.vue` | 工作区页头（图标 / 标题 / 描述 / Tag / extra slot）；对比篮 hero、检索 review 标题区对齐 | 0.2 天 |
| 2.7.5 | `components/common/SectionPanel.vue`、`JudgmentStrip.vue` | 从 demo `portalShared` 上移；禁止再放在 `views/` 被页面互引 | 0.2 天 |

- **依赖**：2.5、0.2
- **验收**：ResultList / ElementProfile / CompareItemCard / 空态 四处头部与指标展示同源组件；改 chips 顺序只需改一处
- **归属**：开发 A（优先于 4.1/4.3）

#### 2.8 企业域 chrome（`components/enterprise/`）

> 与 search 壳解耦的企业专用壳层；配置与路由 map 仍属企业域，但 UI 块可测可复用。

| 子项 | 产物 | 职责 | 工时 |
|------|------|------|------|
| 2.8.1 | `components/enterprise/CompareItemCard.vue` | 对比篮对象卡（meta + 移除）；检索抽屉与正式对比页共用 | 0.3 天 |
| 2.8.2 | `components/enterprise/AnalysisTypePicker.vue` | 分析类型选择 + 权限态提示（可被评估模块复用） | 0.3 天 |
| 2.8.3 | `components/enterprise/ProfileBreadcrumb.vue` + `config/enterpriseBreadcrumb.ts` | 画像多来源面包屑；map 进 config，页面只传 `source` | 0.2 天 |

- **依赖**：1.3、2.7、阶段 4 路由约定
- **验收**：对比篮页主体由 `WorkbenchPageHeader` + `SectionPanel` + `CompareItemCard` + `AnalysisTypePicker` 拼装；详情页面包屑增入口只改 config
- **归属**：开发 A（对齐 4.3）；详情面包屑由开发 B 在 4.2 接入

#### 2.9 保持 page-local（明确不抽）

| 区域 | 原因 |
|------|------|
| `EnterpriseOverviewTabs` 级总览工作台 / 矩阵热力 | 图表下钻与 Context 强绑定；仅复用 ResultToolbar/ResultList |
| `SearchPage` / `EnterpriseSearch.vue` URL 解析与 preset | 路由胶水 |
| `enterpriseSearchConfig` / `enterpriseProfileTabs` | 配置与要素内容即差异点 |
| 对比篮「分析类型 → 评估模块」业务路由表 | 企业中心 IA 编排，属阶段 4.3 |
| Scaffold 内企业 US/Q 追溯文案常量 | 下沉为 review overlay config，而非再造 Trace 组件 |

---

### 阶段 3：高级筛选组件（独立模块，3 天）

> 可与阶段 2 并行。DSL 引擎不依赖 API 层。**具体规划与实现由曹丽影处理**（`ENT-MOD-SEARCH-V2-COMPONENTS`），含嵌套深度上限、拖拽排序、字段联动校验等内部细节。

#### 3.1 FilterDSL 引擎

- **产物**：`src/components/filter/FilterEngine.ts`
- **依赖**：0.3（`filter.ts` 类型）
- **职责**：DSL 求值引擎；支持多条件自由组合 + AND/OR 自由组合（递归任意深度嵌套）；mock 阶段本地过滤，生产阶段序列化传后端
- **DSL 类型**（核心，参考 demo `GroupCondition`）：
  ```ts
  interface GroupCondition {
    type: 'group'
    id: string
    combinator: 'AND' | 'OR'       // 组内条件的关系
    children: Array<LeafCondition | GroupCondition>  // 嵌套，支持任意深度
  }
  interface LeafCondition {
    type: 'leaf'
    id: string
    fieldId: string
    operator: Operator           // = != > >= < <= contains in notIn between ...
    value: unknown              // 按 valueType 决定控件
  }
  type FilterDSL = GroupCondition
  ```
- **验收**：
  - `evaluate(dsl, record): boolean` 本地过滤
  - `serialize(dsl): string` 序列化（生产传后端）
  - `normalize(dsl): FilterDSL` 规范化（补 id、去空组）
- **工时**：0.8 天

#### 3.2 高级筛选面板 FilterPanel.vue

- **产物**：`src/components/filter/FilterPanel.vue`
- **依赖**：3.1、3.3
- **职责**：两种形态 `drawer`（抽屉）+ `page`（整页字段库）；左侧字段分类导航 + 右侧条件构建区；支持递归分组节点 `GroupNode.vue` 渲染嵌套 AND/OR 组
- **验收**：`variant` prop 切换形态；字段分类导航点击聚焦对应条件组；应用/重置/取消 事件；拖拽重排与改组
- **工时**：0.8 天

#### 3.3 单条件行 ConditionBuilder.vue

- **产物**：`src/components/filter/ConditionBuilder.vue`
- **依赖**：0.3
- **职责**：迁移 demo `ConditionBuilder`；字段类型自适应运算符与值控件（文本→输入框/数字→数字输入/枚举→下拉/日期→日期范围）；字段挂 `metricId` 显示 ⓘ；待口径字段显示 ⚠️
- **验收**：字段切换时运算符与值控件联动；嵌套组（AND/OR 组合）增删；拖拽排序
- **工时**：0.8 天

#### 3.4 筛选模板管理

- **产物**：`src/components/filter/FilterTemplateManager.vue`
- **依赖**：0.3
- **职责**：筛选模板保存/加载/删除（localStorage + 后期接 API）；区分"查询方案"（含关键字）与"筛选模板"（纯 DSL）
- **验收**：保存/加载/删除闭环；模板列表按要素隔离
- **工时**：0.4 天

#### 3.5 校验与序列化层

- **产物**：FilterEngine 补充 `toBackendDSL()`/`fromBackendDSL()`
- **职责**：整树校验（去空分组、去无效条件）；与生产接口字段对齐，业务组件零改
- **工时**：0.2 天

> **注**：高筛具体实现细节（嵌套深度上限、拖拽排序、字段联动校验、后端 DSL 序列化）由曹丽影在开发过程中细化处理。

---

### 阶段 4：业务页面（2-3 天）

> 依赖阶段 2 + 3。

#### 4.1 企业查询页

- **产物**：`src/views/enterprise/EnterpriseSearch.vue` + `src/config/enterpriseSearch.ts`
- **依赖**：2.1–2.8、3.2-3.4、1.1
- **职责**：装配 `SearchScaffold` + 企业领域配置（字段库/卡片 schema/表格列/画像 Tab/热门标签/初始推荐）；接入 `api/enterprise.ts`，mock 开关控制数据源；空态用 `EmptyStateWithActions`
- **验收**：
  - URL 参数 `mode`/`q`/`preset`/`source` 可初始化搜索态
  - 查询→列表→画像抽屉→对比篮抽屉→正式对比页 全链路通
  - `VITE_APP_USE_MOCK=true` 走 mock，`=false` 走真实接口（数据结构对齐）
- **工时**：0.8 天

#### 4.2 企业详情页

- **产物**：`src/views/enterprise/EnterpriseDetail.vue`
- **依赖**：1.1（`getEnterpriseProfile`）、2.4、2.5、2.7、2.8.3
- **职责**：独立路由页（非弹窗），`/enterprise/:code`；复用 `ElementProfile mode=page`；Tab：企业概况/负面信息/经营信息/资产信息/营销信息/年检年报/关系链条；关系链条用 ECharts graph（demo 用 SVG 硬画，生产升级）
- **验收**：
  - 路由参数取 `code` 调接口；Tab 懒加载；关系图谱 ECharts 力导向图渲染
  - **上下文携带**：从查询页进入详情 → 返回时保留搜索结果（query 回带或 keep-alive）
  - 从对比篮进入详情 → 返回时对比篮选中项不丢失
  - 面包屑走 `ProfileBreadcrumb` + config（企业查询/对比篮/外部入口）
- **工时**：1 天

#### 4.3 对比篮工作区

- **产物**：`src/views/enterprise/EnterpriseCompare.vue`
- **依赖**：1.3（对比篮 store）、1.1、2.6.1、2.7、2.8
- **职责**：路由 `/enterprise/compare?ids=xxx`；读取 `stores/compareBasket`；用 `CompareItemCard` + `AnalysisTypePicker` 拼装；对比矩阵 + 选择分析维度（基础信息/指标/关系图谱对比）
- **验收**：
  - 从 URL `ids` 或 store 读取对比项；对比矩阵字段对齐；移除单项/清空；空篮态用 `EmptyStateWithActions` 引导回查询页
  - **分发至评估模块**：从对比篮选中企业后可分发至企业评估模块（Mock 阶段存 localStorage + 提示"已加入评估队列"）
  - 加入/移除/分发至评估模块完整链路可演示；对象卡与检索抽屉列表同源组件
- **工时**：0.6 天

#### 4.4 路由与菜单接入（落地）

- **产物**：`src/router/routes.ts` + `menu.ts`（替换 0.4 占位）
- **依赖**：4.1-4.3
- **验收**：三个页面路由注册；菜单组「企业分析」可见可点（承接 0.4 骨架）；`meta.requiresAuth=true`
- **工时**：0.2 天

---

### 阶段 5：集成与验收（1 天）

| 编号 | 任务 | 验收 |
|---|---|---|
| 5.1 | 全链路串通 | 查询→详情→对比 完整路径，搜索态保留 |
| 5.2 | Mock 双路径验证 | `VITE_APP_USE_MOCK=true/false` 两条数据路径均通 |
| 5.3 | 评审模式验证 | `reviewMode` 开关后：角色切换器显隐、追溯角标显隐、锁态菜单解锁正确 |
| 5.4 | 代码规范 | `npm run lint` + `npm run type-check` + `npm run build` 全绿 |
| 5.5 | 提交 PR | feature 分支 + PR 到 dev（遵循生产仓 git 策略，不直推 dev） |

---

## 四、依赖关系与并行度

```
阶段0（地基） ──┬─→ 阶段1（接口+mock+对比篮） ──┬─→ 阶段2（通用组件） ──┬─→ 阶段4（页面） ──→ 阶段5
               │                               │                        │
               └───────────────────────────────┴─→ 阶段3（高级筛选） ──┘
```

- **阶段 0 必须最先完成**（类型/mock 开关/评审 store 是所有人的依赖）
- **阶段 1 与阶段 3 可并行**（高级筛选 DSL 引擎不依赖 API 层；COMPONENTS 仅 Filter*）
- **阶段 2 依赖阶段 1**；**阶段 2 全量由 S2A 交付**（含原 2B）
- **阶段 4.1/4.3 依赖阶段 2 + 3**；**4.2 详情**由 `ENT-MOD-PROFILE-V2-DEMO`（曹丽影）交付，依赖 S2A
- **预估总工期：11-13 天**（单人全职），2 人并行可压到 8-9 天

### 并行开发建议（2 人）

> **2026-07-14 修订**：开发 A = S2A 全量组件 + S4 查询/对比篮 + S5；开发 B（曹丽影）= 仅高筛 COMPONENTS + 企业详情 PROFILE。

| 人 | 负责范围 | 关键前置 / 交接 |
|---|---|---|
| **A（孔东线）** | **S2A**：2.1–2.8 全量 → **S4**：4.1 查询 + 4.3 对比篮 → **S5** 集成 | 优先交付 ElementProfile / ProfileBreadcrumb 供曹丽影 PROFILE；Filter 契约对齐 COMPONENTS |
| **B（曹丽影）** | **COMPONENTS**：仅阶段 3 Filter*（`components/filter/`）→ **PROFILE-V2-DEMO**：4.2 企业详情会签 | 高筛可与 S2A 并行；详情等 S2A 画像壳合入后装配 |

**说明**：
- 查询页（4.1）依赖 S2A Scaffold + COMPONENTS FilterPanel。
- 详情页（4.2）归 PROFILE，复用 S2A ElementProfile，禁止另起画像壳。
- **ResultToolbar/ResultList 跨流复用**仍是健康范例。

---

## 五、生产仓目录结构规划（`lumen-ui-topic/src/`）

```
src/
├── api/
│   ├── auth.ts                  # 已有，用 defineApi 重构
│   └── enterprise.ts            # 新增
├── components/
│   ├── common/                  # 跨流 chrome + D9 展示
│   │   ├── MetricCard.vue
│   │   ├── MetricSpecCard.vue
│   │   ├── MetricValueDisplay.vue   # 新增：统一分数/指标值
│   │   ├── MockBadge.vue
│   │   ├── StatusTag.vue            # 含 Chip 族
│   │   ├── PendingBadge.vue
│   │   ├── ElementLogo.vue
│   │   ├── EmptyStateWithActions.vue
│   │   ├── WorkbenchPageHeader.vue
│   │   ├── SectionPanel.vue
│   │   ├── JudgmentStrip.vue
│   │   └── CompareBasketDrawer.vue  # 检索轻量篮抽屉
│   ├── review/                  # 用户/角色/评审（阶段 0 已落地）
│   │   ├── PersonaLevelSwitcher.vue
│   │   └── TraceInfoIcon.vue        # 唯一追溯入口，禁止分叉
│   ├── search/                  # 搜索范式组件
│   │   ├── SearchScaffold.vue       # 装配器（组合 2.6，禁止巨石）
│   │   ├── SearchHub.vue
│   │   ├── ResultToolbar.vue
│   │   ├── ResultList.vue
│   │   ├── ElementProfile.vue
│   │   ├── EntityIdentityHeader.vue
│   │   ├── QueryConditionSummary.vue
│   │   ├── QueryAssetPanel.vue
│   │   ├── recordUtils.ts
│   │   └── export/
│   │       └── SearchExportWorkflow.vue
│   ├── enterprise/              # 企业域 chrome（非要素内容）
│   │   ├── CompareItemCard.vue
│   │   ├── AnalysisTypePicker.vue
│   │   └── ProfileBreadcrumb.vue
│   └── filter/                  # 高级筛选（独立模块）
│       ├── FilterPanel.vue
│       ├── GroupNode.vue          # 递归分组节点（AND/OR + 子分组）
│       ├── ConditionBuilder.vue
│       ├── FilterTemplateManager.vue
│       └── FilterEngine.ts        # DSL 求值 + 序列化引擎
├── composables/                 # 新增：跨组件逻辑
│   ├── useSearchExportTasks.ts
│   └── useCandidateLists.ts
├── config/
│   ├── app.ts                   # 已有，补充 USE_MOCK
│   ├── echarts.ts               # 已有
│   ├── tianditu.ts              # 已有
│   ├── enterpriseSearch.ts      # 新增：企业搜索配置
│   └── enterpriseBreadcrumb.ts  # 新增：画像来源面包屑 map
├── mock/
│   ├── auth.ts                  # 已有
│   └── enterprise/              # 新增
│       ├── index.ts
│       ├── enterpriseList.ts
│       ├── enterpriseProfile.ts
│       ├── filterFieldSchema.ts
│       ├── smartParser.ts
│       └── portalAggregates.ts
├── stores/
│   ├── auth.ts                  # 已有
│   ├── counter.ts               # 已有（可删）
│   ├── review.ts                # 新增：评审模式集中管理
│   └── compareBasket.ts         # 新增：对比篮
├── types/
│   ├── leaflet-heat.d.ts        # 已有
│   ├── perms.ts                 # 新增：对齐 demo PermLevel/Persona/CurrentUser
│   ├── enterprise.ts            # 新增：企业领域类型
│   ├── search.ts                # 新增：搜索配置类型
│   └── filter.ts                # 新增：筛选 DSL 类型
├── utils/
│   ├── request.ts               # 已有，保持不动
│   ├── http.ts                  # 新增：defineApi + mock 统一
│   └── ...其它已有
└── views/
    └── enterprise/              # 新增
        ├── EnterpriseSearch.vue
        ├── EnterpriseDetail.vue
        └── EnterpriseCompare.vue
```

---

## 六、三个优先开发页面（本轮范围）

按用户要求，本轮优先开发以下三个接近完整的页面功能模块：

1. **企业查询**（`EnterpriseSearch.vue`）—— 检索工作台主入口
2. **对比篮**（`EnterpriseCompare.vue`）—— 跨页保留的对比工作区
3. **企业详情**（`EnterpriseDetail.vue`）—— 企业画像全屏页

组件合理抽离（SearchScaffold 装配 + **Scaffold 瘦身 2.6** + **跨流实体展示 2.7** + **企业域 chrome 2.8** + 独立高筛模块），保留实际接口调用，通过全局 mock 开关在接口调用层（`api/*.ts` + `defineApi`）统一处理 mock 与真实接口切换。详见「阶段 2 · §2.0」。

---

## 七、备注

- 本文档为规划稿；**阶段 0/1 已拆为 registry 子任务** `ENT-MOD-SEARCH-V2-S0` / `ENT-MOD-SEARCH-V2-S1`，派单包见同目录 `ENT-MOD-SEARCH-V2-S0S1-派单包.md`
- **2026-07-14 决策增量**：右上角用户/角色完全参照 `demo-ui-topic`；`lumen-ui-topic` 现有菜单与 `userRoles` **可完全舍弃**并重建企业查询骨架
- 高级筛选具体规划与实现由曹丽影处理（`ENT-MOD-SEARCH-V2-COMPONENTS`），含嵌套深度上限、拖拽排序、字段联动校验、后端 DSL 序列化等；依赖 S0 的 `types/*` 契约
- 收藏/取消收藏、加入/移除招引/培育候选的功能交互纳入本轮；收藏列表和候选列表暂不规划（属个人中心资产模块）
- UI 稿未出，当前以 demo 原型 + Arco Design 规范为视觉参照（UI 规范与布局跟当前项目框架统一）
- 评审模式相关逻辑集中在 `stores/review.ts` + `components/review/`，后期生产切换时统一处理

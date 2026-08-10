# Handoff · FE-ENT-portal-pages（企业要素 · 门户层页面 + 路由 + 侧边栏 / WP3b）

- **角色 / 作者**：`[agent:frontend-agent]`（人评审：待 UE/架构师）
- **日期**：2026-06-19
- **仓 / 分支**：`topic_demo`（原型仓）/ `feat/ent-elements-build`；本地 commit，**未 push**
- **栈口径**：React + Vite + TypeScript + **Arco Design**（`@arco-design/web-react`）+ **ECharts**（复用 `EChart.tsx`）+ Tailwind v4（仅消费 `src/styles/design-tokens.css` 令牌）；**未使用 recharts / 原生交互控件**
- **依赖基础层**：WP3a（commit `fd4d419`）的 `components/common/*`、`components/search/*`、`mock/enterprise/*`、`lib/observability.ts`

> 本 WP 在 WP3a「通用要素检索范式 SearchScaffold 基础层」之上，把基础层正式页面化，并新增门户层 4 个展示子页 + 1 个整页统一画像，接入 `routes.tsx` 与 `Layout.tsx` 侧边栏。**未触碰** `src/app/pages/enterprise/*`（WP3c 范围）。

---

## 1. 范围与实现（对照 ENT-element-master-design / ENT-search-design / ENT-wireframe / ENT-IA / ENT-userflow）

### 1.1 新增路由（5 条，挂在 `/development/*` 既有布局下）

| # | 路由 | 页面组件 | 线框对应 | 说明 |
|---|---|---|---|---|
| 1 | `/development/search` | `pages/development/SearchPage.tsx` | E-31 / SE-01~06 / SearchHub | 检索工作台正式页：`SearchScaffold` 注入 `enterpriseSearchConfig`（关键字 / 智能 / 高级筛选三模式）+ 结果列表 + 点公司名开**抽屉画像** + 抽屉「在新窗口完整打开」跳整页 |
| 2 | `/development/enterprise/:enterpriseCode` | `pages/development/EnterpriseProfilePage.tsx` | DR-04 统一画像（整页态） | `useParams` 取 code → `ElementProfile` **整页态**（与抽屉同内容同 Tab，可分享直达） |
| 3 | `/development/key-enterprises` | `pages/development/KeyEnterprisesPanorama.tsx` | E-33 重点企业全景图 | MetricCard 概览 + 产业链上中下游全景 + 规模/领域分布(ECharts) + Top 榜单 Table |
| 4 | `/development/star-enterprises` | `pages/development/StarEnterprises.tsx` | E-34 明星企业介绍 | 明星企业单选切换 + MetricCard + 产品全景卡 + 团队 Table + 产业生态力导图(ECharts graph) |
| 5 | `/development/shenzhen` | `pages/development/ShenzhenEnterprises.tsx` | E-35 深圳企业介绍 | 概况 MetricCard + 历年趋势折线 + 规模饼图 + 产业链/区域柱状 + 区域地图**占位(🧪)** + 重点企业 Table |

### 1.2 侧边栏（`Layout.tsx` → `navGroups`「门户-企业发展」组）

在既有「门户-企业发展」组（`IconStorage`）下新增 4 项，沿用既有 `app-nav-*` class 体系、`<Link>`、`active` 高亮与 `aria-*`：

```
门户-企业发展
├─ 企业发展概况   /development/overview     （既有，未动）
├─ 企业检索       /development/search        🆕
├─ 重点企业全景图 /development/key-enterprises 🆕
├─ 明星企业介绍   /development/star-enterprises 🆕
└─ 深圳企业介绍   /development/shenzhen      🆕
```

> 整页画像 `/development/enterprise/:enterpriseCode` 为详情/分享直达页，按惯例**不入侧边栏**（由检索抽屉/榜单点击进入）。

### 1.3 复用 WP3a 基础层（直接 import，零重写）
- `components/common/*`：`ContextBar` `MetricCard` `MetricSpecCard`(ⓘ) `MockBadge`(🧪) `StatusTag` `RoleLevelGate`/`UserLevelProvider` `EChart`
- `components/search/*`：`SearchScaffold` `ElementProfile` `enterpriseSearchConfig` `enterpriseProfileTabs` `types.ts`
- `mock/enterprise/*`：`enterpriseList` `enterpriseProfile` `metricSeed`(D9 8件套) 等
- `lib/observability.ts`：`track` / `ENT_TRACK`

### 1.4 公共骨架（新增）
`pages/development/portalShared.tsx` —— 门户子页公共件，避免各页重复样板：
- `PortalShell`：`UserLevelProvider` + 面包屑 + `JudgmentStrip`(一句话结论) + `ContextBar`(内嵌角色切换 `RoleSwitch`)
- `useEnterpriseProfileDrawer`：**统一企业画像抽屉（DR-04 两层共用同画像同数据）**，内置「在新窗口完整打开」→ `window.open(/development/enterprise/:code)` + 去 SCRM 动作（对比 / 收藏 / 深度分析 / 导出）+ 全埋点
- `buildEnterpriseProfileUrl(code)` / `findEnterprise(codeOrId)`：跨层整页画像路由约定
- `SectionPanel`：D8 克制风格区块面板

## 2. 角色分级（U1/U2/S1/S2/U3）与去 SCRM 化落点
- 各页经 `PortalShell` 提供 `UserLevelProvider`，并在 `ContextBar.extra` 内嵌 `RoleSwitch` 供演示切换；默认 `U2`。
- 敏感字段 / 高阶动作经 `RoleLevelGate` 弱化 + 锁标 + 升级引导（非阻断），命中即埋点。
- **去 SCRM 无关化**：动作集合为 加入对比篮 / 收藏 / 导出（分级）/ 深度分析跳转；**无**领取/转 CRM/锁定/外呼等销售语义。
- **埋点**（`ENT_TRACK`）：`ENT_PROFILE_DRAWER_OPEN`、`ENT_PROFILE_FULLPAGE_OPEN`、`ENT_ADD_COMPARE`、`ENT_FAVORITE`、`ENT_DEEPANALYSIS_JUMP`、`ENT_EXPORT` 等，均带 `id/code`，funnel 含 `user_level`。

## 3. D9 数据血缘（ⓘ/🧪/⚠️）
- 每个统计数字旁 `MetricCard` 携 `metricId`，`MetricSpecCard`(ⓘ) 读取 `metricSeed` 8 件套。
- 门户聚合所需新 `metric_id` 已补入 `mock/enterprise/metricSeed.ts`：`M_ENT_TOTAL_COUNT` / `M_ENT_REGIONAL_COUNT` / `M_ENT_STAR_PATENT_COUNT` / `M_ENT_STAR_RD_RATIO` / `M_ENT_SZ_COUNT` / `M_ENT_SZ_SCALE_DIST`（均含口径/公式/源表/源系统/更新频率/版本，标 mock 状态）。
- 派生/聚合 Mock 集中在新增 `mock/enterprise/portalAggregates.ts`（重点企业产业链/规模/领域、深圳分布/趋势、明星企业补充），保证多视图口径一致；Mock 数据均挂 `MockBadge`(🧪)。
- 深圳区域地图为**占位区块 + 🧪**，未引新依赖（符合「需地图则占位」约束）。

## 4. 偏离说明
- 关系图谱 / 产业生态用 ECharts `graph`（力导向）Mock 占位；正式可评估切 AntV G6（D8 允许）。
- 检索/画像数据走 WP3a 本地 Mock 引擎（Wave 0），Wave 1 切 Java→Python `/internal`，组件签名不变。
- 整页画像 `:enterpriseCode` 通过 `findEnterprise` 同时兼容「统一社会信用代码 code」与「内部 id」解析，便于演示直达。

## 5. 产物清单（新增/修改文件树，均在 `topic_demo/src/app`）

```
新增
  pages/development/portalShared.tsx              # 门户公共骨架 + 统一画像抽屉 hook
  pages/development/SearchPage.tsx                # E-31 检索工作台
  pages/development/EnterpriseProfilePage.tsx     # DR-04 整页统一画像
  pages/development/KeyEnterprisesPanorama.tsx    # E-33 重点企业全景图
  pages/development/StarEnterprises.tsx           # E-34 明星企业介绍
  pages/development/ShenzhenEnterprises.tsx       # E-35 深圳企业介绍
  mock/enterprise/portalAggregates.ts            # 门户派生/聚合 Mock

修改
  components/search/ElementProfile.tsx           # +drawer|page 双态 + onOpenFullProfile（IconShareExternal）
  components/search/SearchScaffold.tsx           # +onOpenFullProfile 透传 + 埋点
  mock/enterprise/metricSeed.ts                  # +6 个门户 metric_id（D9 8件套）
  mock/enterprise/index.ts                       # 导出 portalAggregates
  routes.tsx                                      # +5 条 /development/* 路由
  components/Layout.tsx                           # 侧边栏「门户-企业发展」+4 项
```

**未改**：`package.json` / `vite.config.ts` / `.gitignore` / tailwind 配置 / `pages/enterprise/*`（WP3c）。

## 6. 验收证据（自检 / DoD）
- `npm run design:check` → **Design contract checks passed** ✅
- `npm run build`（vite build）→ **✓ built（3748 modules）exit 0** ✅
- `ReadLints`（全部新增/修改文件）→ **0 错误** ✅
- 浏览器运行烟测（dev server `:5173`）→ 5 条路由全部正常渲染、无白屏/无 React 报错/无控制台错误；检索抽屉打开并含「在新窗口完整打开」✅

## 7. 架构合规自检（00-team-constitution §2）
1. 算法只在 Python ✅（前端仅 Mock/展示）
2. 调用链不越层 ✅（Mock 阶段）
3. 图谱 NebulaGraph ✅（前端仅 ECharts 展示，未引 Neo4j）
4. 可观测性必加 ✅（`observability.ts` 全动作埋点）
5. CI/CD ✅（原型仓，无破坏）
6. demo2 只读 merge ✅（仅原型仓内新增）
7. 前端只调 Java / 共享聚合核心 ✅（壳预留后端替换点）
8. 标准表先行 + Mock ✅
9. 前端规范 D8 ✅（Arco + ECharts + design-tokens；`.global-workbench-tabs`/`.analysis-tabs`；主色 #165DFF；无 forbidden 模式）
10. 数据血缘 D9 ✅（ⓘ/🧪/⚠️ 8件套）

## 8. 留给 WP3c 的对接说明（跨层契约）
- **概况页检索入口**：`/development/overview`（WP3c 负责）的「检索入口」应跳 `/development/search`；如需带初始条件，遵循下方 query 约定。
- **检索工作台带参约定**（`SearchPage` 已支持读取）：
  - `?q=<关键字>`：进入即执行关键字检索
  - `?mode=keyword|smart|advanced`：指定初始检索模式
  - 示例：`/development/search?mode=smart&q=南山区+集成电路+专精特新`
- **整页画像直达**：统一用 `buildEnterpriseProfileUrl(code)` → `/development/enterprise/:enterpriseCode`（`code` 为统一社会信用代码，亦兼容内部 id）。
- **跨层「深度分析」跳转**：当前为 Mock `Message` 提示，约定带参 `enterprise_code=<code>` 跳分析层；WP3c/分析层落地真实路由后，替换 `useEnterpriseProfileDrawer` 的 `onDeepAnalysis` 目标即可（埋点 `ENT_DEEPANALYSIS_JUMP` 已就位）。
- **统一画像组件**：抽屉态与整页态同源（`ElementProfile` 的 `mode='drawer'|'page'`），WP3c 复用同一组件保证「两层同画像同数据」（DR-04），勿另起画像实现。

## 9. 后续 TODO
- Wave 1：检索/画像/聚合切后端（Java→Python `/internal`），metric 改读 `/metrics/v1/catalog`。
- cost 字段回填到 `task-registry.yaml`（WP3b：`actual_tokens` / `model_used` / `actual_cost` / `cost_warn`）。
- 区域地图占位待选型（高德/Leaflet）后替换，移除 🧪。

# LUMEN-POLICY-FE-PORTAL-REPLICA-L01 · 政策扶持门户六 Tab 复刻

> 日期：2026-10-24
> 仓：`lumen-ui-topic` · 分支 `dev` · 停在本地工作区，未 commit、未 push

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 状态 | `in_progress`（人工验收闸门：不自动签收、不自动推远程） |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复刻现行 demo 六 Tab，未用 YAGNI 跳过 D8/D9/D10、调用链或评审挂点。没有的字段留空，不另造接口、不折算力度。 |

## 范围与实现

侧栏仍一项「政策扶持」，落点 `/policy-portal/overview`。页内 `?tab=` 切六页：政策概况统计、政策地图、政策产业覆盖、政策力度排名、最新政策动态、深圳政策对比。旧子路径按 `POLICY_PORTAL_LEGACY_REDIRECT` 重定向到同一页。本入口不再使用 `PolicyShellPlaceholder`；维护管理仍用占位壳。详情复用 `PolicyDetailDrawer`，数据走已有 `policyDocs`。

未做：政策查询、时序/区域对比/深圳现状三项分析、维护管理。

调用链只读已有 Java：

- `POST /policy/topic/v1/policy/metrics`
- `POST /policy/topic/v1/policy/indicators`（`kind=all`）
- `POST /policy/topic/v1/policy/search`
- `GET /policy/topic/v1/policy/docs/{id}`

没有门户聚合接口。分布接口不按产业切片。力度指数、覆盖度矩阵、分地区时序、城市榜、热力，包里没有就空着。

## 图题—序列字段对照

| id | 图题 | 字段 | 来源 | 画不画 |
|----|------|------|------|--------|
| total | 政策总量 | `headline.M_POLICY_TOTAL_COUNT` | metrics | 只在 headline 有数时出数字 |
| publish | 历年发布量 | `timeseries.publish_count` | indicators | 折线，序列名=图题 |
| publishAll | 全库历年发布量 | `timeseries.publish_count` | indicators | 深圳数量对比用，文案写明不是深圳总量 |
| compare | 对照地区政策量 | `policy_count` | national / sz | 只画名单里有数的地区，不补 0 |
| map | 政策量分布 | `policy_count` | national / sz | 有坐标才出圆点 |
| distSum | 分布政策量合计 | `policy_count` 已返回行之和 | 同上 | 不是政策总量 |
| sz | 各区政策量 | `sz.policy_count` | indicators | 深圳数量对比柱 |
| rank | 政策量排名 | `national.policy_count` | indicators | 省级榜；城市档空 |
| intensity | 力度指数 | （无） | absent | 空。pending `QPOL-02`，不用政策量折算 |
| coverage | 产业链覆盖度 | （无） | absent | 空 |
| stage | 上/中/下游覆盖度 | （无） | absent | 空 |
| searchHit | 检索命中 | `search.total` | search | trace，不当成政策总量 |

标题含「总量」的只有政策总量，字段是 `M_POLICY_TOTAL_COUNT`。`publish_count` 的图题是发布量。

## 下钻参数读取方

唯一读取函数：`readPortalQuery`。

| 参数 | 谁写 | 谁读 |
|------|------|------|
| `tab` | 六 Tab；`overview`/`view` 在挂载时迁走 | Tab 与面板分支 |
| `view` | 仅旧链接 | 迁到 `tab` 后从 URL 删除 |
| `szView` | 深圳页内单选 | 深圳四块面板 |
| `industry` | 产业级联 | 检索 `industry_vid`（`toPolicyGraphVid`）；分布图不切片 |
| `geo` | 地域下拉；深圳 Tab 强制 `shenzhen` | 地图/检索 region |
| `compare` | 对照多选，最多 5 | 数量对比柱 |
| `field` | 地图点选、深圳区下拉 | 检索 region 覆盖；地图高亮 |
| `level` | 最新动态单选 | 仅最新动态检索（Java `level` 精确匹配） |

## 复刻五维

| 条 | 结果 | 说明 |
|----|------|------|
| R1 布局 | ✅ | 六 Tab、筛选条、概况（总量 / 时序 / 对照 / 关联表）、地图与列表分栏、覆盖两栏、力度空态 + 政策量领奖台与表、最新时间轴、深圳四视图。一节点一套布局 |
| R2 交互 | ✅ | 加载、失败重试、无数据空态、Tab 与筛选写入 query、对照最多 5 个、地图点选下钻、详情抽屉。无结果不补行 |
| R3 样式 | ✅ | 页底 `var(--sci-bg-page, #d8e7fc)`，正文 14px，Arco 控件。V1 满足 |
| R4 评审 | ✅ | 页与面板不直接引 `ReviewMetricBadges`。统计数字只经 `PolicyReviewMount`。关评审 `v-if="visible"` 不渲染 |
| R5 Mock | ✅ | 演示数据只在 `src/mock/policy/policyApi.ts`，经已有 `registerApiMock`。页面不引 `@/mock`。`USE_MOCK=false` 时走 Java 实包，缺数留空 |

V2–V7 不适用：本页不是政策查询 Hub。政策查询页未改。

### 评审挂点

| mount-id | 种类 | 指标 |
|----------|------|------|
| POLICY-PORTAL-PAGE | trace | 页标题 |
| POLICY-PORTAL-TOTAL | metric | `M_POLICY_TOTAL_COUNT` |
| POLICY-PORTAL-PUBLISH | metric | `M_POLICY_TIMESERIES` |
| POLICY-PORTAL-SZ-COUNT | metric | `M_POLICY_SZ_DIST` |
| POLICY-PORTAL-COMPARE | metric | `M_POLICY_NATIONAL_DIST` |
| POLICY-PORTAL-MAP-SUM | metric | `M_POLICY_NATIONAL_DIST` |
| POLICY-PORTAL-MAP | metric | `M_POLICY_NATIONAL_DIST` |
| POLICY-PORTAL-INTENSITY | metric | `M_POLICY_INTENSITY_INDEX`，pending `QPOL-02` |
| POLICY-PORTAL-RANK-PODIUM | metric | `M_POLICY_NATIONAL_DIST` |
| POLICY-PORTAL-RANK | metric | `M_POLICY_NATIONAL_DIST` |
| POLICY-PORTAL-COVERAGE | metric | `M_POLICY_INDUSTRY_COVERAGE` |
| POLICY-PORTAL-STAGE | metric | `M_POLICY_INDUSTRY_COVERAGE` |
| POLICY-PORTAL-SEARCH-HIT | trace | `search.total`，不是政策总量 |

## 偏离说明

相对现行 demo `policy-portal`（不以 2026-06 六条侧栏为准）：

- 地图图题用「政策量分布」，不用「政策发布密度」。值是 `policy_count`，没有密度/热力字段。`UnifiedLeafletMap` 设 `preset-layers=false`，无坐标不画气泡。
- 力度指数与覆盖率不计算。力度块空着并挂 `QPOL-02`。排名表只排 `policy_count`。没有城市政策量字段，城市档空。
- 产业覆盖保留左右两栏结构，两栏都空。
- 深圳数量对比的折线标题是「全库历年发布量」，不把全库 `publish_count` 说成深圳总量。各区柱用 `sz.policy_count`。
- 对照的「连续性 / 时序叠加」空着。没有分地区 `continuity_rate` 或分地区 `publish_count` 序列。
- 最新动态条数称「检索命中」，用 `search.total`。级别是单选，对齐 Java 精确匹配。
- 概况增加政策总量数字，单独绑定 headline，避免折线被读成总量。

## 架构合规自检

| # | 铁律 | 结果 |
|---|------|------|
| 1 | 算法只在 Python | ✅ 前端不算力度、不累加发布量冒充总量 |
| 2 | 前端 → Java → `/internal/*` | ✅ 只调 `/policy/topic/v1/policy/**` |
| 3 | 图谱 Nebula | ✅ 不把 policy graph 当产业覆盖 |
| 4 | 可观测 | ✅ 沿用 `request.ts` 的 `X-Trace-Id` / `traceparent`，本页不新造埋点通道 |
| 8 | 缺数诚实空 | ✅ |
| D8 | Arco / Design 页底与字号 | ✅ |
| D9 | 一个数字一个评审入口；关评审零泄漏 | ✅ `PolicyReviewMount` |
| D10 | Tab、筛选、空态、抽屉 | ✅ |
| D12 | 不调 `demo-*`，不直连 Python | ✅ |
| D14 | 对象存储 | 不适用 |

## 验收证据

- `node --experimental-strip-types src/views/policy/policyPortalReplica.selfcheck.mjs` → `policyPortalReplica.selfcheck ok`
  - 禁占位壳、禁页面内 `ReviewMetricBadges`、总量标题对总量字段、发布量不称总量、下钻参数有 `readPortalQuery`、详情走 `PolicyDetailDrawer`
- `node_modules/.bin/vue-tsc.cmd --build` → exit 0
- 本机 `pnpm type-check` 被现有 `pnpm-workspace.yaml`（无 `packages` 字段）挡住，未改该文件。类型检查跑的是脚本正文 `vue-tsc --build`
- `src/router/menu.selfcheck.mjs` 在政策三项分析页对「禁止空跑」的断言失败。该页不在本单范围，本单未改那个文件。政策扶持相关的 menu 断言在失败点之前已通过
- 本地 `vite`（`VITE_APP_USE_MOCK=true`）打开 `/policy-portal/overview`：六 Tab 可切；政策总量 1280；地图合计 740（四省 `policy_count` 之和，图题不是总量）且 Leaflet 有点；覆盖两栏空文案；力度指数空、省级榜按政策量；最新动态「检索命中 4 条」；深圳页折线标题为全库历年发布量；点标题打开 `PolicyDetailDrawer`。`/policy-portal/intensity-rank` 落到 `?tab=rank`。`ent_review_mode=false` 时正文无 `metric_id` / `QPOL`

## 产物清单

- `repos/lumen-ui-topic/src/views/policy/PolicyPortalPage.vue` 及六个面板 / `PolicyReviewMount.vue`
- `policyPortalTabs.ts`、`policyPortalModel.ts`、`policyPortal.css`、`policyPortalReplica.selfcheck.mjs`
- `src/router/menu.ts`（overview 换门户页，旧路径 redirect；维护管理仍是占位壳）
- `src/api/policy/types.ts`（indicators 已知列）
- `src/mock/policy/policyApi.ts`（字段对齐 Java；总量 1280 与发布量峰值 210 不是同一串数）

## Cost

| 字段 | 值 |
|------|-----|
| model_used | `grok-4.7` |
| actual_tokens | 700000（会话估算，无 Console 分项） |
| actual_cost | 2.94 |
| cost_warn | `green` |
| 口径 | `budget-estimate.md` §1.2 没有 Grok 价。按 B 档 $3/$15 每百万、输入 90% / 输出 10% 代入公式：`700000×0.9×3/1e6 + 700000×0.1×15/1e6 = 2.94`。source: session_estimate |

## CI/CD

- 分支：`dev`（本地领先，未推）
- commit：无（人工验收闸门，本单不自动提交）
- pipeline / 部署：无

## 遗留

- 未对在线 Java 做联调。`USE_MOCK=false` 时缺矩阵、缺坐标、缺力度就是空态。
- 产业级联在目录加载后会把默认产业写入 query。分布指标仍不按产业过滤，检索才带 `industry_vid`。
- `menu.selfcheck.mjs` 的「禁止空跑」失败属于政策三项分析页，留给该页自己的单。

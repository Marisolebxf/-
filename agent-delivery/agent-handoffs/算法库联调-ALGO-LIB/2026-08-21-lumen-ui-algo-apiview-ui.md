# lumen-ui-algo-apiview 算法库联调台 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在空仓 `lumen-ui-algo-apiview` 用 Vite + Vue3 重建「算法库联调台」：登录后默认 `/home`（对齐模板站 `#overview` 算法库总览）；算法详情页为左菜单 + 顶栏 + 三区（接口信息 / 算法测试 / 可视化）。**首期只交付企业分析算法库**；其余库菜单可灰显占位。接口契约从 `demo-ui-system-test` 抽取，依赖对齐 `lumen-ui-topic`。

**Architecture:** 目标仓当前几乎只有 GitLab Python 骨架 README，需整体换成前端工程。页面不按 demo 的 Element Plus 页一对一拷贝，而是 **菜单/路由尽量保留 + 单页壳（接口信息 / 算法测试 / 可视化）+ 算法目录驱动**。HTTP 只打 Java REST（经 `gkxlumen-platform-gateway`），禁止直连 Python、禁止运行时依赖任何 `demo-*` 服务（D12）。`USE_MOCK=true` 时用本地 fixture；`false` 时禁止 fixture 填数。

**Tech Stack:** Vue 3.5 + Vite 7 + TypeScript + Vue Router + Pinia + **Arco Design Vue** + axios + ECharts + AntV G6 + Leaflet + dayjs + UnoCSS/Tailwind（版本以 `lumen-ui-topic/package.json` 为上限，不新增未在该仓出现的 npm 包，除非任务另批）。

## Global Constraints

- 目标仓：`${GKX_ROOT}/repos/lumen-ui-algo-apiview`；push **`origin/dev`**，禁止 `origin/main`。
- 对照仓（只读）：`${GKX_ROOT}/repos/demo-ui-system-test`（接口路径/方法/入参/出参/图表面板）。
- 框架对照（只读，禁止抄页面）：`${GKX_ROOT}/repos/lumen-ui-topic`。
- 视觉模板：总览 https://elaborate-phoenix-5b6c5c.netlify.app/#overview ；算法页 https://elaborate-phoenix-5b6c5c.netlify.app/#alg-4-1 。
- **默认路由：`/home`（算法库总览）**，禁止默认进 `/entan/basic`。
- **首期范围：壳 + 总览 + 企业分析算法库（`/entan/*`）**；chain/policy/svc/comp/innov 不抽接口、不接可视化，侧栏可灰显「二期」。
- D8：token / 主色 `#165DFF` / 页底 `#D8E7FC` / 正文 14px / 控件高 32px，按 `agent-delivery/Design.md`；组件用 Arco Vue，不用 Element Plus / AntD。
- D9：每个统计数字旁 ⓘ + 四维角标；过渡态从 `agent-delivery/metrics/metric-readiness-matrix-*.yaml` 镜像，禁止页面手写改绿。
- D10：交互按 `UX-UE 通用交互组件规范.md`。
- D12：`VITE_*` 不得指向 `demo-*`；Java 下游只允许 `lumen-algo-py` / `lumen-etl-es-py`。
- 可观测：移植 `lumen-ui-topic/src/utils/observability.ts` 的 `X-Trace-Id` / `traceparent` 模式。
- commit：`[agent:frontend-agent]`；handoff 必含 `ponytail: full`。
- 强度：ponytail full（编码任务）。
- 禁止 git merge demo 仓；对照后重写。
- 禁止为「更简」另起一套交互；三区（接口信息 / 调试 / 可视化）是模板站硬要求，不得砍成只有表格。

---

## 现状与范围边界

### 目标仓

本地 `lumen-ui-algo-apiview` 目前只有 `README.md`（Python 脚手架文案）+ git。实施第一步是 **用 Vue SPA 覆盖脚手架**，保留公司 `htmitech/` 许可文件（若远程后续出现则原样保留，不要删 LICENSE）。

### demo 真源（菜单 / 路由）

`demo-ui-system-test/src/layout/menuConfig.ts` + `src/router/index.ts`：

| 一级 | 路径前缀 | 首期 | 说明 |
|------|----------|------|------|
| **算法库总览** | `/home` | **必做** | 替换 demo「链路追踪 Demo」；对齐模板站 `#overview` |
| 企业分析算法库 | `/entan/*` | **必做** | 招标模型 + 工程增强分组；slug 与 demo 同名 |
| 产业链 / 政策 / 产业服务 / 产业综合 / 创新监测 | 各前缀 | **菜单灰显占位** | 二期再抽契约；总览卡片可展示名称但 CTA 进企业库或提示二期 |
| 科技新闻 / 维护管理 / 政策 Mock / 要素库 Mock | — | **不做** | 非算法库 |
| 登录 | `/login` | **必做** | 最小登录；成功后 **redirect `/home`** |

路由完整性：被删菜单项 **不强制保留死路由**；对应 path 若产品仍要书签兼容，做 301 到所属库首页。其余 slug **与 demo 同名**（`/entan/tech` 不要改成 `/talent/tech-power`）。

### 模板站总览（`#overview`，对应本仓 `/home`）

源码锚点在原型 `src/pages/Home.tsx`（打包后可见）：

1. **侧栏第一项「算法库总览」** → 切到 overview；Logo 区标题「科技专题服务算法库」。
2. **Hero：** 一句话说明本站是算法 API 原型；右侧 **4 张统计卡**（专题模块数 / 算法页数 / 接口数 / 图谱页数），数字从 catalog 汇总，禁止手写死数（D9：汇总数字旁 ⓘ）。
3. **「图谱 / 高复杂度页」卡片网格：** 名称 + 一句话 focus，点击进入对应算法页。
4. **顶栏：** 当前为总览时标题为「算法库总览」；右侧状态标签（如 Mock / API 可用）+「总览」按钮回到 `/home`。

本仓首期数字口径：模块数 = 已挂菜单的库（企业=1 可用，其余灰显也计入「规划模块」则用两行：已开通 1 / 规划 6）；算法页数 = `ENTAN_SUB_MENU.length`；接口数 = catalog 中企业 endpoint 条数；图谱页 = 含 `viz.kind==='graph'` 的页。不要沿用模板站的「5 模块 / 37 页」文案。

### 模板站算法页（#alg-4-1）

每个算法页固定三块，顶栏切换：

1. **接口信息**：方法、路径、服务状态、请求参数表、请求/响应 JSON 示例、字段说明、Python/curl 示例。
2. **算法测试**：可编辑请求表单/JSON → 真实或 Mock 调用 → 展示 HTTP 状态、耗时、原始 JSON。
3. **使用可视化**：用该接口返回值驱动 KPI / 表 / ECharts / G6 / 地图（从 demo 对应页抽取图表类型，不发明新图表）。

### 调用链（必须）

```
lumen-ui-algo-apiview  →  gkxlumen-platform-gateway  →  lumen-svc-platform (Java REST)
                                                      →  lumen-algo-py /internal/*
```

demo 现网路径（如 `/entan/v1/...`、`/innov/v1/industry/...`）只作 **契约对照**。正式 path 以 Java 已发布 OpenAPI / 网关路由为准；Java 未就绪的页：`USE_MOCK=true` + 页面 🧪，禁止把 `VITE_API_URL` 指到 demo 网关。

---

## 推荐实现策略（三选一已锁定）

**采用：目录驱动 + 通用页壳（A）。**

- 每个算法 = `AlgoEndpointSpec`（一份 TS catalog），不是一份独立 400 行 Vue。
- 可视化用少量 `viz` 组件（KpiRow / EChartPanel / DataTable / G6Graph / GeoMap / JsonTree）。
- demo 里高度定制的页（企业图谱编辑、异步任务轮询、产业链全景）允许 **特例 Vue**，但仍套同一 Layout + 三区 Tab。

不采用：逐页把 Element 改 Arco（工期爆炸、布局不齐模板）。不采用：iframe 嵌 demo（违 D12）。

---

## 目标目录（实施后）

```
lumen-ui-algo-apiview/
  package.json                 # 依赖对齐 lumen-ui-topic，去掉 leaflet.heat 等本仓用不到的包
  vite.config.ts
  tsconfig*.json
  index.html
  .env.example                 # VITE_API_BASE_URL= 网关；VITE_APP_USE_MOCK=
  src/
    main.ts
    App.vue
    config/app.ts              # USE_MOCK / ENABLE_MOCK_AUTH / timeout
    utils/request.ts           # 抄 topic 拦截器骨架（trace / token / envelope）
    utils/observability.ts
    utils/auth.ts
    api/{chain,entan,policy,svc,comp,innov}/index.ts
    catalog/
      types.ts                 # AlgoEndpointSpec
      menu.ts                  # 侧栏树（从 demo menuConfig 删减）
      endpoints/*.ts           # 每模型一份 spec
    layouts/AlgoShell.vue      # 左菜单 + 顶栏
    pages/HomeOverview.vue     # 算法库总览（#overview）
    pages/AlgoWorkspace.vue    # 三区 Tab 容器
    pages/login/LoginPage.vue
    components/
      api-info/ApiInfoPanel.vue
      api-test/ApiTestPanel.vue
      viz/KpiRow.vue
      viz/EChartPanel.vue
      viz/DataTable.vue
      viz/G6Graph.vue
      viz/GeoMap.vue
      review/                  # D9 角标，参照 topic src/review 组织方式，不抄专题页
    mock/                      # 仅 USE_MOCK
  agent-handoffs/              # 或写回 orchestration 仓 handoff
```

### `AlgoEndpointSpec`（后续任务共用，不得改名）

```ts
export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE'
export type VizKind = 'kpi' | 'table' | 'bar' | 'line' | 'pie' | 'radar' | 'graph' | 'map' | 'json'

export interface AlgoParamField {
  name: string
  type: string
  required: boolean
  description: string
  example: unknown
}

export interface AlgoEndpointSpec {
  id: string                 // 如 entan.key-talent 或 entan.tech
  menuPath: string           // /entan/tech
  title: string
  summary: string
  method: HttpMethod
  path: string               // Java 对外 path，如 /topic/v1/... ；未就绪则填 demo 对照 path 并 marked pendingJava
  pendingJava?: boolean
  status: 'running' | 'mock' | 'unavailable'
  params: AlgoParamField[]
  sampleRequest: unknown
  sampleResponse: unknown    // data 内层
  responseFields: Array<{ name: string; type: string; description: string }>
  viz: Array<{ kind: VizKind; title: string; dataPath: string }>
  metricIds?: string[]
}
```

---

## 依赖裁剪（相对 lumen-ui-topic）

**必装：** vue, vue-router, pinia, @arco-design/web-vue, axios, echarts, vue-echarts, @antv/g6, leaflet, dayjs, @vueuse/core, nprogress, mitt, lodash, crypto-js（若登录加密与 topic 同模式才留）。

**默认不装（YAGNI，本仓联调台不用专题地图热力/天地图除非 innov 地图页需要）：** `leaflet.heat`。innov 事件地图若要用 Leaflet，再装 `@types/leaflet`；天地图 key 走 `VITE_` 且对照 topic `tianditu.ts` 模式，不硬编码。

**dev：** vite, @vitejs/plugin-vue, typescript, vue-tsc, eslint, prettier, less, unocss, unplugin-auto-import, unplugin-vue-components。

---

### Task 1: Vue 工程脚手架替换 Python README 工程

**Files:**
- Create: `lumen-ui-algo-apiview/package.json`, `vite.config.ts`, `tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json`, `index.html`, `.env.example`, `.gitignore`（前端标准，勿抹掉已有 git 规则除非冲突）
- Create: `src/main.ts`, `src/App.vue`, `src/config/app.ts`, `src/assets/main.css`
- Modify: `README.md`（改成 Vue 联调台说明；删除 pip/requirements 主路径）
- Test: `package.json` scripts `dev` / `build` / `type-check`

**Interfaces:**
- Consumes: `lumen-ui-topic/package.json` 版本号
- Produces: `pnpm dev` 可起；`USE_MOCK` 从 `VITE_APP_USE_MOCK` 读取，默认 `true`（Java 未全量接通前）

- [ ] **Step 1:** 以 topic 的 `package.json` + `vite.config.ts` 为模板初始化，**删除**专题业务别名无关插件即可，不要复制 `src/views`。
- [ ] **Step 2:** `pnpm install` 后 `pnpm type-check` 与 `pnpm build` 必须绿。
- [ ] **Step 3:** Commit：`feat(scaffold): Vue3+Vite 算法联调台工程骨架 [agent:frontend-agent]`

---

### Task 2: 请求层 + 可观测 + 登录壳

**Files:**
- Create: `src/utils/observability.ts`, `src/utils/request.ts`, `src/utils/auth.ts`, `src/utils/authRedirect.ts`, `src/constants/ResultEnum.ts`
- Create: `src/pages/login/LoginPage.vue`, `src/api/auth.ts`
- Create: `src/router/index.ts`（hash 或 history：与模板站一致用 **hash**，便于静态站部署）

**Interfaces:**
- Consumes: topic `request.ts` 拦截器行为（Bearer、traceparent、envelope `{ code, msg, data }`）
- Produces: `request<T>(config)` ；`USE_MOCK && ENABLE_MOCK_AUTH` 时本地假 token，**不得**把假 token 打到真网关（照抄 topic `shouldAttachBearerToken`）

- [ ] **Step 1:** 登录页最小：账号框 + 登录按钮；真登录对接 Java `/auth` 仅当网关契约明确，否则 Mock 登录。
- [ ] **Step 2:** 未登录进 `/login`；已登录默认 **`/home`**；layout `redirect: '/home'`。
- [ ] **Step 3:** Commit：`feat(http): 网关请求与 Mock 登录 [agent:frontend-agent]`

---

### Task 3: 左菜单 + 顶栏 Layout（对齐模板站）

**Files:**
- Create: `src/layouts/AlgoShell.vue`, `src/layouts/SideMenu.vue`, `src/catalog/menu.ts`
- Modify: `src/App.vue` 使用 shell

**Interfaces:**
- Consumes: `menu.ts` 树（见下表）
- Produces: 当前路由高亮、父级展开、顶栏标题=当前算法名、右侧「API 可用 / Mock」状态点

侧栏一级（首期）：

0. **算法库总览** → `/home`（始终可点，高亮当 `route.path==='/home'`）  
1. **企业分析算法库** → 展开 `ENTAN_SUB_MENU`（全可点）  
2. 产业链 / 政策 / 产业服务 / 产业综合 / 创新监测 → `disabled: true`，角标「二期」

- [ ] **Step 1:** 菜单从 demo `menuConfig.ts` 复制后：home 改为总览；删除 tech-news / ops / policy-mock / chain-indana；非企业库 `disabled`。
- [ ] **Step 2:** 视觉对齐模板站：侧栏约 288px（`w-72`）、顶栏 64px、主色 `#165DFF`、页底 `#D8E7FC`；不对照 demo 链路追踪页。
- [ ] **Step 3:** Commit：`feat(layout): 左菜单+顶栏算法壳 [agent:frontend-agent]`

---

### Task 3b: `/home` 算法库总览（对齐 `#overview`）

**Files:**
- Create: `src/pages/HomeOverview.vue`
- Create: `src/catalog/overview.ts`（`summarizeCatalog()`：模块/页/接口/图谱计数 + 企业库卡片列表）
- Modify: `src/router/index.ts` children 增加 `path: 'home'` → `HomeOverview.vue`；layout `redirect: '/home'`

**Interfaces:**
- Consumes: `menu.ts` + 已注册的 `AlgoEndpointSpec[]`（首期仅 entan）
- Produces: `OverviewSummary { moduleTotal, moduleLive, pageCount, apiCount, graphPageCount, featured: Array<{ path, title, focus }> }`

- [ ] **Step 1:** Hero + 4 统计卡 + 企业算法卡片网格（点进 `/entan/...`）。非企业模块在总览用灰色卡片「二期」，不链到空路由。
- [ ] **Step 2:** 去掉 demo 链路追踪按钮、Java/Python step 卡、Tempo 演示（那是旧 home，禁止搬进本仓）。
- [ ] **Step 3:** Commit：`feat(home): 算法库总览对齐模板 overview [agent:frontend-agent]`

---

### Task 4: 通用三区工作台 `AlgoWorkspace`

**Files:**
- Create: `src/catalog/types.ts`
- Create: `src/pages/AlgoWorkspace.vue`
- Create: `src/components/api-info/ApiInfoPanel.vue`
- Create: `src/components/api-test/ApiTestPanel.vue`
- Create: `src/components/viz/JsonTree.vue`（原始 JSON 折叠）
- Test: `src/catalog/types.spec.ts` 或最小 `scripts/check-catalog.ts`：校验每条 spec 含 method/path/sampleRequest/viz

**Interfaces:**
- Consumes: `AlgoEndpointSpec`
- Produces: Tab `info | test | viz`；test 调用 `request` 且把 `data` 交给 viz

- [ ] **Step 1:** 路由通配：`/:lib/:slug` 从 catalog 查找 spec，找不到 404 页。
- [ ] **Step 2:** 接口信息区表格 + JSON 示例 + 复制；算法测试区 JSON 编辑器（textarea + Arco Button 发送即可，不要上 Monaco）。
- [ ] **Step 3:** 跑 catalog 自检脚本，缺字段即失败。
- [ ] **Step 4:** Commit：`feat(workspace): 接口信息/调试/可视化三区壳 [agent:frontend-agent]`

---

### Task 5: 可视化积木 + D9 角标门控

**Files:**
- Create: `src/components/viz/KpiRow.vue`, `EChartPanel.vue`, `DataTable.vue`, `G6Graph.vue`, `GeoMap.vue`
- Create: `src/review/*`（MetricSpecCard + MockBadge 最小集，组织方式学 topic `src/review`）
- Create: `src/metrics/readiness.generated.ts`（头注释写明 yaml 真源；本任务可先手工 3 条指标打通 ⓘ）

**Interfaces:**
- Consumes: `spec.viz[]` + `response.data`
- Produces: `dataPath` 用简单点路径（如 `rankings`、`summary.totalIdentified`），不做通用 JSONPath 引擎

- [ ] **Step 1:** KPI / 表 / bar / pie / radar 先通；graph/map 可在首次被 catalog 引用的任务再接线。
- [ ] **Step 2:** `USE_MOCK=false` 时 MockBadge 不渲染；禁止组件内写死数值。
- [ ] **Step 3:** Commit：`feat(viz): 联调台可视化积木与 D9 ⓘ [agent:frontend-agent]`

---

### Task 6: 首期 — 企业分析算法库 catalog（仅此批）

读 `demo-ui-system-test/src/api/entan/index.ts` + `src/views/entan/**` → `src/catalog/endpoints/entan.ts` + `src/api/entan/index.ts` + `src/mock/entan.ts`。

**必须覆盖的 slug（与 demo `ENTAN_SUB_MENU` 一致）：**

| path | 主接口（demo 对照） | viz 预期 |
|------|---------------------|----------|
| `/entan/basic` | key-enterprises / type-distribution / domain-distribution 等 | KPI + 饼/柱 |
| `/entan/competitiveness` | `/score` `/ranking` | KPI + 表 + 雷达 |
| `/entan/history` | `/history` | 时间线/表 |
| `/entan/pain-points` | `/diagnosis` | 表 + 告警 |
| `/entan/supply-chain` | `/centrality` | 表 + 可选图 |
| `/entan/tech` | `/tech-power/rank` | 表 + 柱（首期演示页） |
| `/entan/biz` | `/biz-power/rank` | 表 + 柱 |
| `/entan/attract` | POST `/recommend/attract` | 表 |
| `/entan/cultivate` | POST `/recommend/cultivate` | 表 |
| `/entan/graph` | `/graph` `/graph/path` | **特例 Vue** G6 |
| `/entan/risk` | `/risk` | 表 + KPI |
| `/entan/news` | `/news` `/news/stats` | 表 |
| `/entan/eval-async` | 异步评估 | **特例 Vue** 任务面板 |

`/entan/indana/:documentId` 不进侧栏；首期不做。

**二期（本计划不实施，只留菜单灰显）：** chain / policy / industry-service / industry-comp / innov。

- [ ] **Step 1:** 先做 `/entan/tech` 打通三区，再铺其余 slug。
- [ ] **Step 2:** 图谱、异步评估用特例页，仍包在 AlgoShell + 尽量保留「接口信息」Tab。
- [ ] **Step 3:** handoff 附「demo `/entan/v1` → lumen path」对照；`pendingJava` 标齐。
- [ ] **Step 4:** Commit：`feat(entan): 企业分析算法库联调页 [agent:frontend-agent]`

抽取规则（写进每个 endpoint 注释）：

```
demo method+url → spec.method/path
demo 请求函数参数 → spec.params + sampleRequest
页面里 echarts option / table columns / g6 data → spec.viz
```

禁止把 demo 的 `el-*` 模板粘进本仓。

---

### Task 7: Java 网关 path 对齐（可与 6 并行，但 6 的 path 先标对照）

**Files:**
- Modify: `src/api/entan/index.ts` 的 `BASE`（首期只动企业）
- Create: `docs/api-path-map.md`（demo `/entan/v1` → lumen 网关前缀）

已知 demo 前缀（对照用）：企业 `/entan/v1`。其它库二期再写。

- [ ] **Step 1:** 与 api-agent 核对 `lumen-svc-platform` 已发布路径；未发布保持 `pendingJava` + Mock。
- [ ] **Step 2:** 确认没有任何 `VITE_` 含 `demo-`。
- [ ] **Step 3:** Commit：`fix(api): 联调台改为 lumen 网关前缀 [agent:frontend-agent]`

---

### Task 8: 验收、handoff、CI 最小集

**Files:**
- Create: `agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/LUMEN-ALGO-PLATFORM-UI-L01.md`（若 registry 尚未建 ID，先用该文件名，ID 由 coordinator 补）
- Modify: 本仓 `.gitlab-ci.yml`：`pnpm install` + `pnpm type-check` + `pnpm build`（静态镜像，参考 topic CI，不要抄 Python pip）

**DoD（首期）：**

- 登录后落在 `/home`；总览视觉对齐 `#overview`（Hero + 4 卡 + 企业算法卡片），无链路追踪 Demo
- 侧栏「算法库总览」+ 企业库全量子页可进；其它库灰显
- `/entan/tech`（及企业其余子页）具备接口信息 / 算法测试 / 可视化
- `USE_MOCK=false` 时无 fixture 填数
- Design.md §14 + D9 ⓘ + observability 请求头
- `pnpm build` 绿；push `origin/dev`

- [ ] **Step 1:** 截图：布局、接口信息、调试成功、可视化。
- [ ] **Step 2:** handoff 填 cost 四字段 + `ponytail: full`。
- [ ] **Step 3:** Commit + push dev。

---

## 工作量切片（给人排期）

| 阶段 | 任务 | 预估 | 是否首期 |
|------|------|------|----------|
| P0 | Task 1–5 壳 | 3–5 人日 | 是 |
| P0 | Task 3b 总览 `/home` | 0.5–1 人日 | 是 |
| P1 | Task 6 企业库全量 | 3–4 人日 | 是 |
| P1 | Task 7 企业网关 path | 0.5–1 人日 | 是（Java 未就绪则 Mock + pendingJava） |
| P1 | Task 8 验收 | 0.5 人日 | 是 |
| P2 | 其余五库 catalog | 另开计划 | **否** |

---

## Spec 覆盖自检

| 需求 | 任务 |
|------|------|
| 目标仓 Vite+Vue3 | T1 |
| 默认 `/home` + overview 总览 | T2 redirect、T3b |
| 模板站左+顶+中 | T3–T4 |
| 接口信息+算法测试+可视化 | T4–T5 |
| 首期只迁企业库 | T6 |
| 依赖对齐 topic | T1 |
| D12 / 不直连 Python | T2、T7 |
| D8/D9/可观测 | T3、T5、T2 |

无 TBD 占位实现；Java 最终 path 以 Task 7 现场核对为准，catalog 用 `pendingJava` 显式标记。

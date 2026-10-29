# Handoff · 产业链（CHAIN/E2/IND）前端接 Java 门面（mock→API service 层）

- **任务**：CHAIN-L02 — 把 demo-ui-topic 已有产业链 10 页从本地 mock 切到 Java REST 门面（`/topic/v1/industry/**`），建立 API service 层 + adapter（snake 窄表→camel 宽表 + id 适配 + 列表宽表前端组装），env 开关控制 mock/API，保留 mock 兜底。
- **角色**：`[agent:frontend-agent]`
- **仓库**：`demo-ui-topic`
- **分支**：`feat/CHAIN-fe-api-wiring`（基于 `dev` @ `b2fc812`）
- **上游契约**：`demo-svc-platform` `feat/E-E2-IND-java-facade`（API-CHAIN-java-facade.md）；上游 Python `demo-algo-science`。
- **⚠️ 约束**：Java 门面未合 dev、未部署 K8s（demo waiver），**无法即时 E2E**。默认开关走 mock，后端上线后切开关即可。

---

## 1. 范围与实现（对照 DoD 6 条）

| # | DoD 项 | 状态 | 实现 |
|---|---|---|---|
| 1 | 新增 `src/app/services/industry/`：API client + adapter（id 映射 / snake→camel / 列表宽表组装） | ✅ | 9 文件，见 §2 |
| 2 | 10 页改为经 service 层取数，mock/API env 开关，默认不破坏可浏览性 | ✅ | 全部经 `useChainList`/`useChainProfile` hook；默认 `VITE_USE_INDUSTRY_API` 未设=mock，同步种子零闪烁 |
| 3 | 保留 mock 兜底，API 失败回退不崩页 | ✅ | service 层 try/catch 回退 mock；hook 以 mock 为初始种子；画像多端点 `safe()` 逐个兜底 |
| 4 | `npm run build` 自检 | ✅ | 通过（vite 6.3.5，5045 modules，built in ~50s，exit 0；仅 chunk>500kB 体积警告，非本次引入） |
| 5 | handoff（本文件） | ✅ | — |
| 6 | 架构合规自检（前端只调 Java 网关） | ✅ | 见 §6 |

---

## 2. 改动文件清单

**新增 service 层（`src/app/services/industry/`，9 文件）：**
- `config.ts` — env 开关：`USE_INDUSTRY_API` / `INDUSTRY_API_BASE` / 超时
- `idMap.ts` — chainCode ↔ 上游 chain_id 适配表（demo 默认 identity 透传）
- `types.ts` — camel 宽表类型（复用 mock）+ snake 窄表原始行类型（对照 chain_schema.sql）+ `ApiEnvelope`/`SourcedResult`
- `httpClient.ts` — fetch 封装：traceId（`X-Trace-Id`+`traceparent`）注入、`{code,msg,data}` 解析、AbortController 超时、observability `track` 埋点
- `industryApi.ts` — 13 端点 1:1 调用（chainId 经 idMap 适配）
- `adapters.ts` — `adaptChainList`/`adaptChainListItem`（窄表→宽表，mock 兜底聚合，category 按 industry_code 前缀）
- `industryService.ts` — `getChainList`/`getChainProfile`（mock/API 切换 + 失败回退 + 画像多端点组装）
- `hooks.ts` — `useChainList`/`useChainProfile`（mock 种子 + API 覆盖）
- `index.ts` — barrel

**新增配置模板：**
- `.env.example` — 记录 `VITE_USE_INDUSTRY_API`（默认 false）/`VITE_INDUSTRY_API_BASE`（`.env*` 已被 .gitignore，故用 example 模板）

**改动页面（10）：** `IndustryOverview` `IndustryGeneralOverview` `IndustryPanorama` `IndustryCycle` `IndustryRegionalEvaluation` `ShenzhenIndustryAnalysis` `ChainSearchPage` `ChainProfilePage`（改为 hook 取数）；`IndustryStructureAnalysis` `IndustryProblemDiagnosis`（移除无用 `CHAIN_LIST` 导入 + 注释说明对应端点）。
**未改动 mock：** `src/app/mock/industry/*` 全保留（作兜底数据源）。

---

## 3. 页面 ↔ 端点 ↔ adapter 映射表

| 页面 | 经 service hook | 对接网关端点 | adapter | 当前数据源 |
|---|---|---|---|---|
| IndustryOverview（CP0 概述） | `useChainList` | `/list` | `adaptChainList` | API(列表)+mock(顶部 9 KPI 为页面常量) |
| IndustryGeneralOverview（总览辅助页） | `useChainList` | `/list` | `adaptChainList` | API(列表) / mock 兜底 |
| IndustryPanorama（CP1 全景） | `useChainList` | `/list`（图谱由 upstream/mid/down 字段构建） | `adaptChainList` | API(列表) / mock；真全景图 `/panorama` 待接 |
| IndustryCycle（CP2 周期） | `useChainList` | `/list`（stage 字段） | `adaptChainList` | API(列表) / mock；`/cycle` 待接 |
| IndustryRegionalEvaluation（CP3 区域） | `useChainList` | `/list`（competitivenessScore） | `adaptChainList` | API(列表) + mock(城市对比为页面常量)；`/region-index` `/competitiveness` 待接 |
| IndustryStructureAnalysis（CP4 关键环节） | —（页面内置 SEGMENT_DETAILS） | `/key-nodes` | `industryApi.keyNodes`（已备） | mock（页面常量，未接） |
| IndustryProblemDiagnosis（CP5 瓶颈） | —（页面内置 BOTTLENECKS） | `/bottlenecks` | `industryApi.bottlenecks`（已备） | mock（页面常量，未接） |
| ShenzhenIndustryAnalysis（CP6 深圳） | `useChainList` | `/list`（sz/完整度字段） | `adaptChainList` | API(列表) + mock(各区/对标为页面常量)；`/shenzhen` 待接 |
| ChainSearchPage（检索） | `useChainList` | `/list` | `adaptChainList` | API(列表) / mock |
| ChainProfilePage（画像） | `useChainList`+`useChainProfile` | `/list`+`/market-stats`+`/key-nodes`+`/shenzhen`+`/competitiveness`+`/bottlenecks` | `getChainProfile` 多端点组装 | API(画像 kpi/trend/环节/瓶颈) / mock(relatedEnterprises、completeness 无端点) |

---

## 4. env 开关说明

| 变量 | 默认 | 作用 |
|---|---|---|
| `VITE_USE_INDUSTRY_API` | **未设/false** | false=全走 mock；true=经网关调 `/topic/v1/industry/**`，失败自动回退 mock |
| `VITE_INDUSTRY_API_BASE` | `/topic/v1/industry` | 网关基础路径（StripPrefix=1 → gkx-innov `/v1/industry`） |

启用方式：仓内 `cp .env.example .env.local` 后设 `VITE_USE_INDUSTRY_API=true` 并配代理/网关地址（注：本仓 `vite.config.ts` 目前无 dev proxy，真实联调需配 `server.proxy` 或经网关同源访问——属配置改动，未在本任务擅自修改，见 §7）。

---

## 5. mock 兜底策略

- **hook 层**：始终以 mock 作初始种子同步返回（`useChainList`→`CHAIN_LIST`，`useChainProfile`→`CHAIN_PROFILES`），后端未启用/未部署时页面零闪烁可浏览。
- **service 层**：API 模式下 `getChainList` try/catch 回退 mock；`getChainProfile` 用 `Promise.all`+`safe()` 逐端点兜底，全失败整页回退 mock。
- **列表补齐**：API `/list` 未返回的 chainCode 用 mock 条目补齐（`adaptChainList`），保证 8 条始终在列。
- **来源标记**：`SourcedResult.source`/`AsyncResource.source`（'mock'|'api'）已透出，后续可驱动 🧪 MockBadge 精确显示（当前页面 MockBadge/PendingBadge 沿用原状未动）。

---

## 6. demo 自动通过的 4 口径标注（上线前回收）

> 已按团队临时默认值实现，代码注释 + 本节标注，需登记 `客户决策清单跟踪表.md`。

1. **chain_id ↔ chainCode 映射**（idMap.ts）：Java 路径原样透传，前端 adapter 适配；demo 默认 identity（chainCode 即 chain_id），上游真实主键确定后在 `CHAIN_CODE_TO_UPSTREAM` 补齐。
2. **八大未来产业清单**：以前端固定 8 条为准；API `/list` 多/少的条目通过 `adaptChainList` 合并（API 行优先 + mock 补齐）。
3. **category 分类**（adapters.ts）：按 `industry_code` 前缀归类（F→未来/S→战略新兴/T→优势传统，占位规则），优先沿用 mock category 兜底。
4. **列表宽表聚合归属**：Java 守零算法铁律不跨端点聚合 → **前端组装**：以 mock 同 chainCode 行为底座，用 `/list` 真实字段（名称/类别/环节数）覆盖，其余 ~12 个聚合指标暂留 mock，待上游补齐 `/list` 宽表或前端逐页多端点拉取替换。

---

## 7. 架构合规自检

1. **算法只在 Python** ✅ 前端零算法，仅取数 + 字段映射 + 展示。
2. **调用链 前端→Java→Python** ✅ service 层只访问 `INDUSTRY_API_BASE`（网关 `/topic/v1/industry`），**未直连 Python `/v1/chain` 或 DB**。
3. **图谱 NebulaGraph** ✅ 不涉及（前端图谱为 ECharts/ForceGraph 渲染）。
4. **可观测性** ✅ httpClient 注入 `X-Trace-Id`+`traceparent`，并 `track` 埋点（chain_api_request/success/error），未破坏既有 observability。
5. **CI/CD waiver** ✅ feature 分支；build 本地通过；后端未部署故未 E2E。
6. **demo2 只读** ✅ 未触碰 demo-ui-science / lumen 仓。
7. **前端规范 D8** ✅ 未改 Arco/token/配色，纯数据层接入。
8. **数据血缘 D9** ✅ MockBadge/PendingBadge/MetricSpecCard 原状保留；新增 `source` 字段为后续精确标注预留。
9. **配置不擅改** ✅ 未改 `package.json`/`vite.config.ts`/`.gitignore`；仅新增 `.env.example`（模板，非运行时配置）。dev proxy 需求登记给下游（见 §9）。

---

## 8. Git

- 分支：`feat/CHAIN-fe-api-wiring`（起点 dev `b2fc812`）
- commit：见 completion（message 含 `[agent:frontend-agent]` + `CHAIN-L02`）
- push：→ `origin/feat/CHAIN-fe-api-wiring`（feature 分支，未直推 dev/main）

---

## 9. 接力建议（下游）

1. **Java 门面合 dev + 部署 K8s** → 切 `VITE_USE_INDUSTRY_API=true` 做 E2E（前端→Java→Python 全链路 + traceId 贯通验证）。
2. **dev proxy**：本仓 `vite.config.ts` 无 `server.proxy`。本地联调需补 `/topic` 代理到网关，或经网关同源部署（配置改动，需任务授权后改）。
3. **剩余 4 页深接**：CP4 关键环节 `/key-nodes`、CP5 瓶颈 `/bottlenecks` 端点已在 `industryApi` 备好，页面仍用内置常量，待接（建议补 `useKeyNodes`/`useBottlenecks` hook）；CP1 全景 `/panorama`、CP2 周期 `/cycle`、CP3 `/region-index`+`/competitiveness`、CP6 `/shenzhen` 可逐页深接替换页面常量。
4. **上游补宽表**：建议 algorithm/data 在 `/v1/chain/list` 直接补齐列表宽表聚合字段，前端即可移除 mock 兜底聚合。
5. **业务口径回收**：§6 四项升 🟢 后移除 demo 占位规则与 ⚠️ 标注。
6. **MockBadge 精确化**：用 `AsyncResource.source` 驱动各指标 🧪 显示。

---

## 10. cost

| 字段 | 值 |
|---|---|
| estimated_tokens | ~110k |
| actual_tokens | ~150k |
| model_used | Claude Opus 4.x（frontend-agent 子代理） |
| actual_cost | ~$3.2（估算，< $10 阈值） |
| cost_warn | false |

---

# 附录 L02b：深接（deep-wiring）+ dev proxy + API-first 默认

> 续 `feat/CHAIN-fe-api-wiring`，commit message 含 `[agent:frontend-agent] CHAIN-L02b`。

## L02b.1 vite dev proxy

- 在 `vite.config.ts` 新增 `server.proxy['/topic']`，`changeOrigin: true`。
- **代理目标**：`process.env.VITE_GATEWAY_TARGET || 'http://10.50.69.111:30892'`（env 可覆盖）。
- **选址依据**：
  - 检查全部业务前端仓（`lumen-ui-science-pc` / `demo-ui-science` / `lumen-ui-topic` / 本仓）**均无既有 proxy 目标**可沿用。
  - 检查 `demo-svc-platform/helm/gkx-platform/values.yaml`：**gateway 为 ClusterIP（port 9999），未暴露 NodePort**；前端走 nginx 同源 `proxy_pass` 到集群内 gateway，无对外 dev 直连地址。
  - 故采用任务建议的占位 dev 地址 `http://10.50.69.111:30892` 作默认，并以 `VITE_GATEWAY_TARGET` 暴露覆盖点。**联调/上线前需把 gateway 暴露 NodePort/Ingress 后改此 env 指向真实地址**。
- `.env.example` 同步新增 `VITE_GATEWAY_TARGET` 说明。

## L02b.2 默认开关：API-first + 失败回退 mock

- `config.ts`：`USE_INDUSTRY_API = env.VITE_USE_INDUSTRY_API !== 'false'`（**默认走真实 API**；仅显式 `'false'` 纯 mock）。
- `.env.example` 默认值改 `VITE_USE_INDUSTRY_API=true`。
- 回退稳健性：
  - `useChainList`/`useChainProfile` 以 mock **同步种子**渲染，API 失败保留 mock（不闪不崩）。
  - 新增**深接端点统一走 `useApiResource`「null 兜底」模式**：`data=null`（未启用/失败/空）⇒ 页面用**自身内置常量**兜底，`data≠null`⇒ 真实数据替换。后端没起时 demo 正常浏览，后端起后自动切真实。

## L02b.3 service 层扩展

新增 10 端点 adapter（snake→camel）+ getter（`apiOnly` 包裹，失败/未启用返回 `null`）+ hooks：

| hook | 端点 | adapter | 出参 |
|---|---|---|---|
| `useChainPanorama` | `/{id}/panorama` | `adaptPanorama` | `AdaptedPanorama`（nodes/edges） |
| `useChainCycle` | `/{id}/cycle` | `adaptCycle` | `AdaptedCycle`（trend/stage） |
| `useChainRegionIndex` | `/{id}/region-index` | `adaptRegionIndex` | `AdaptedRegionIndex[]` |
| `useChainCompetitiveness` | `/{id}/competitiveness` | `adaptCompetitiveness` | `AdaptedCompetitiveness[]` |
| `useChainShenzhen` | `/{id}/shenzhen` | `adaptShenzhen` | `AdaptedShenzhen` |
| `useChainHotspot` | `/{id}/hotspot` | `adaptHotspot` | `AdaptedHotspot` |
| `useChainRoadmap` | `/{id}/roadmap` | `adaptRoadmap` | `AdaptedRoadmap` |
| `useChainRecommendation` | `/{id}/recommendation` | `adaptRecommendation` | `AdaptedRecommendation` |
| `useChainKeyNodes` | `/{id}/key-nodes` | `adaptKeyNodes` | `AdaptedKeyNode[]` |
| `useChainBottleneckScores` | `/{id}/bottlenecks` | （取 5 维 score） | `Record<dim,number>` |

复用 `ChainPicker`（新增于 `industryShared.tsx`）：多链页面切当前产业链 + 显示 `实时`/`🧪 Mock兜底` 标。

## L02b.4 页面 ↔ 端点深接对照

| 页面 | 端点 | 替换的内置常量 | 真实/兜底 |
|---|---|---|---|
| `IndustryStructureAnalysis`（CP4） | `/key-nodes` | `SEGMENT_DETAILS`（表格 + 图 + 4 KPI 动态计算） | API 优先，失败回 `SEGMENT_DETAILS`；`relatedPatents` 上游无 → 0 兜底 |
| `IndustryProblemDiagnosis`（CP5） | `/bottlenecks` | `BOTTLENECKS` 五维 severity（雷达/卡片/列表） | severity 用真实覆盖；**归因/建议/趋势上游无字段 → 保留 mock 叙述** |
| `IndustryRegionalEvaluation`（CP3） | `/region-index` + `/competitiveness` | `CITY_COMPARISON`（区域对比）+ 排名 | API 优先（province→city），失败回内置 |
| `ShenzhenIndustryAnalysis`（CP6） | `/shenzhen` | 深圳企业数 KPI + `SZ_DISTRICTS` 各区分布 | 结构化字段接真实；**problems/opportunities/advantages 文案 JSON 结构未核验 → 保留 mock** |
| `IndustryPanorama`（CP1） | `/panorama` | 由 `CHAIN_LIST` 组图 → 选定链真实 nodes/edges | API 优先（单链图），失败回选定链 mock 图 |
| `IndustryCycle`（CP2） | `/cycle` | 新增「选定产业链周期详情（实时）」block | 仅真实有数据时显示（trend/stage/growthRate） |
| `ChainProfilePage` | `/hotspot` `/roadmap` `/recommendation` | 新增「动态与推荐（实时）」Tab | **仅真实有数据时显示，无则隐藏（不伪造）** |

> 备注：`/competitiveness` 同时已在 `getChainProfile`（L02）画像装配中使用；`/hotspot /roadmap /recommendation` 因属 per-chain 且画像页是天然 per-chain 落点，置于 `ChainProfilePage`（任务列的 Overview 为全链聚合视图，端点为单链，故择 profile 落地，记此偏离）。

## L02b.5 仍 mock 兜底项及原因（不伪造）

| 项 | 所在 | 原因 |
|---|---|---|
| `relatedEnterprises`（关联企业示例 A/B/C，带 🧪） | Panorama 节点详情 | 上游无对应端点 |
| `completenessScore` / 画像聚合宽表字段 | ChainList/Profile | `/list` 为窄表，聚合字段无上游 → mock 补齐（L02 既有） |
| bottlenecks 归因/建议/趋势 | ProblemDiagnosis | 上游 `/bottlenecks` 仅给 5 维 score + severity 串，无 per-dim 归因/建议/年度趋势 |
| shenzhen problems/opportunities/advantages 文案卡片 | ShenzhenIndustryAnalysis | 上游 JSON 元素结构未核验（后端未部署，无法确认 element schema），暂保留 mock 文案 |
| 对标城市基准数据 BENCHMARK | ShenzhenIndustryAnalysis | 跨城对标无对应端点 |

## L02b.6 🧪/⚠️ 标注策略

- `ChainPicker` 据 `source` 显示 `实时`（API）/`🧪 Mock兜底`（mock），逐页可视当前块数据来源。
- 接通真实 API 的块移除/不显示 🧪；仍 mock 的块保留 🧪/⚠️。
- 业务口径 `PendingBadge`（Q016/Q022/Q023/Q024/Q025 等，属甲方口径未定）**与数据来源无关，一律保留**。

## L02b.7 build 结果

- `npm run build`：**通过**（vite v6.3.5，5045 modules，48.3s，exit 0）。
- TS 类型检查随 build 通过；IDE lint 0 错。
- 后端未部署 → 仍未 E2E（API-first 默认下页面经 mock 兜底正常渲染）。

## L02b.8 Git（L02b）

- 分支：`feat/CHAIN-fe-api-wiring`（在 L02 commit 之上叠加）。
- 见本轮 completion 的新 commit sha；push → `origin/feat/CHAIN-fe-api-wiring`，**未合并 dev/main**（由 coordinator 统一合）。

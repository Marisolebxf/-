# LUMEN-CHAIN-FE-ENTRY-L01 · 产业链前端长任务 — 侧栏/产业查询/门户总览/对比篮

> 格式参考 `templates/handoff-template.md`；内容按本单 as-built。  
> **不做**：WORKSPACE 八键填实、直连 Python、另起更简 UI、CHAIN-FE-L03 CP1–CP6、OPS 写侧、改 Java/Python、调 Job Create。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | registry 已 claimed + in_progress；lock 24h。本单完工转 **integration**，不标 done。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单 `/goal` 一致。未用 YAGNI 跳过 D8 Design、D9 ⓘ/四维就绪度、D10 交互、可观测 `X-Trace-Id`、已评审 Demo 对齐、handoff。复用 SearchScaffold/SearchHub/compareBasket/IndustryCompareBasketPanel，不另起第二套篮。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | Demo 真源页 / Design.md §14 / data-lineage-policy / 本仓 AGENTS.md / JAVA-FACADE / FE-D 总派单均精读，禁止用 compress 代替。 |

## 范围与实现

`lumen-ui-topic` 落地产业链 **ENTRY** 壳：侧栏整组、产业查询三模式、门户总览三 Tab、对比篮产业/链扩展。前端只调 Java 网关 **`/chain/topic/v1/industry/**`**，不直连 Python、不扫 ES。

### 路由

| 路径 | 页面 | 本单 |
|---|---|---|
| `/industry-center/overview` | `IndustryOverviewPage.vue` | 真页：catalog + overview + news + snapshot 摘要 |
| `/industry-center/search` | `IndustrySearchPage.vue` | 真页：smart / industry / advanced；高筛独立页；入篮同类型锁；进全景带 `object_type`/`object_id` |
| `/industry-center/panorama` | `IndustryWorkspacePlaceholder.vue` | 占位，保留 query |
| `/industry-center/diagnosis` | 同上 | 占位；`workspace`/`tab` = cycle / key_link / bottleneck |
| `/industry-center/regional` | 同上 | 占位；index / competitiveness |
| `/industry-center/shenzhen` | 同上 | 占位；comparison / development |
| `/industry-center/maintenance` | 同上 | 占位；L4 + OPS extra |

权限：`menu:chain:overview|search|panorama|diagnosis|regional|shenzhen|maintenance`。L0=overview+search；L1+=panorama；L2+=诊断/区域/深圳；L4+OPS extra=maintenance。**企业码未删。**

### Java API 封装

路径常量：`src/api/industry/paths.ts`（`CHAIN_TOPIC_V1=/chain/topic/v1/industry`）  
调用：`src/api/industry/index.ts`（`defineApi`，经 `request.ts`）

| 语义 | 方法 | 路径 |
|---|---|---|
| search | POST | `/chain/topic/v1/industry/search` |
| overview | GET | `/chain/topic/v1/industry/overview` |
| overview/kpi | GET | `/chain/topic/v1/industry/overview/kpi`（封装已备；总览页走 overview 内嵌 kpi） |
| news | GET | `/chain/topic/v1/industry/overview/news` |
| snapshot | GET | `/chain/topic/v1/industry/panorama/snapshot` |
| catalog | GET | `/chain/topic/v1/industry/catalog` |

三种 SEARCH mode：`smart` / `industry` / `advanced`。记录对齐 `IndustrySearchRecord`。Q056 →「暂无正式数据源」；QC07 →「数据筹备中」。介绍/历程无 CMS 则空，禁止用资讯冒充。

### 对比篮

扩展既有 `IndustryCompareBasketPanel.vue`：产业/链本地入篮（不走企业 #91）；发起分析 Modal → `buildIndustryAnalysisUrl` 跳占位路由，**不 Create Job**。

### D9

门户 KPI 只读镜像：`chainReadinessSeed.ts` / `chainMetricSeed.ts` / `chainGapCatalog.ts`，经企业 `getMetricReadiness` / `getMetricMeta` / `getEntGap` fall-through。禁止页面手写改绿。每个统计数字旁 `ReviewMetricBadges`。检索结果条数属交互计数，不伪造 `M_CHAIN_SEARCH_RESULT_COUNT`。

### 可观测

`observability.ts`：`createTraceId` / `createTraceparent`。`request.ts` 拦截器写 `X-Trace-Id` + `traceparent`。

## 偏离说明（as-built）

| 项 | 派单 | As-built | 理由 |
|---|---|---|---|
| 栈 | Design.md 写 Arco React | 本仓 Arco **Vue**（AGENTS.md） | 禁止把 React 抄进 Vue；token/交互对齐 Demo |
| 对比篮政策三项 | Demo 产业篮可发政策三项 | **未移植** | lumen 无 `policyAnalysisRegistry`；记 WORKSPACE/政策单 |
| overview/kpi 独立请求 | 契约表列 kpi | 总览一次 `overview`（含 kpi）；kpi API 已封装 | 少一次往返；字段同源 |
| 热门场景 preset | Demo fixture id | catalog 真 id 可能不同 → 空结果 | 诚实空态，不造假命中 |
| 既有 type-check | 本单范围外 | 标注 `evalResultMap`/`riskResultMap` filter 谓词 | 否则 `vue-tsc --build` 不过，阻塞 GitLab `npm run build` |

## 产物清单

| 产物 | 路径（相对 `lumen-ui-topic/`） |
|---|---|
| Java 封装 | `src/api/industry/{paths,types,index}.ts` |
| 查询模型 | `src/utils/industrySearchModel.ts` |
| 自检 | `src/utils/industrySearchModel.selfcheck.mjs` |
| 配置 | `src/config/industrySearchConfig.ts`、`industryAnalysisRegistry.ts` |
| 页面 | `src/views/industry-center/*` |
| Mock + D9 镜像 | `src/mock/industry/*` |
| 侧栏/权限 | `src/router/menu.ts`、`src/perms/matrix.ts`、`DefaultLayout.vue` |
| 对比篮 | `IndustryCompareBasketPanel.vue`、`stores/compareBasket.ts` |
| SearchHub 文案插槽 | `src/components/search/SearchHub.vue` |
| 可观测 | `src/utils/observability.ts`、`request.ts` |
| 本 handoff | `agent-delivery/agent-handoffs/产业链分析-CHAIN/LUMEN-CHAIN-FE-ENTRY-L01.md` |

## 验收证据

| 项 | 结果 |
|---|---|
| 自检 | ✅ `node src/utils/industrySearchModel.selfcheck.mjs` → `industrySearchModel.selfcheck ok` |
| type-check | ✅ `npm run type-check`（`vue-tsc --build`） |
| build | ✅ `npm run build`（type-check + `vite build`，GitLab `frontend:build` 同脚本） |
| lint（本单文件） | ✅ eslint 本单 TS/Vue 0 error；全仓仍有既有 enterprise lint，不在本单改 |
| 三种 SEARCH mode | ✅ Hub `smart`/`keyword(→industry)`/`advanced`；POST Java `mode` |
| Q056/QC07 | ✅ `value==null` 诚实文案，不补假数 |
| 不调 Job | ✅ ENTRY 不 import `analysisTaskCreate` |
| 无 Python / 无 ES | ✅ 仅 `/chain/topic/v1/industry/**` |
| D9 评审关 | ✅ `ReviewMetricBadges` 组件自闸；关评审模式不渲染 metric_id |

## 附录 D 扫描摘要

扫描根：`src/views/industry-center/**`

### D.1 页面差集

| 页面 | 角标组件 | 结论 |
|---|---|---|
| `IndustryOverviewPage.vue` | `ReviewMetricBadges` | 主 KPI / 资讯数 / 区域列已挂 |
| `IndustrySearchPage.vue` | 无（仅 `TraceInfoIcon`） | 「共 N 条 / 已选 N」= 交互计数，附录 D.0 可不挂；**不伪造** `M_CHAIN_SEARCH_RESULT_COUNT` |
| `IndustryWorkspacePlaceholder.vue` | 无统计数字 | WORKSPACE 填实后再扫 |

P0 整页主 KPI 零角标 = **0**。

### D.2 本地 KPI 接线

概况 Tab KPI 卡 `:metric-id="item.metric_id"`（Java 下发）。区域表列头 `M_CHAIN_ENTERPRISE_COUNT` / `M_CHAIN_INSTITUTION_COUNT`。资讯标题 `M_CHAIN_NEWS_COUNT`。无「有壳无 metricId」主 KPI。

### D.3 镜像 vs 矩阵

`metric-readiness-matrix-CHAIN.yaml` 首批 **不含**门户 KPI（`M_CHAIN_ENTERPRISE_COUNT` / `MARKET_*` / `INVEST_*` / `NEWS_COUNT`）。门户就绪度对齐已评审 Demo `industryOverviewReadinessSeed`，**禁止手写改绿**。矩阵已有 `M_CHAIN_SZ_ENTERPRISE_COUNT`：D2=`pending`，镜像同。矩阵其余深圳/热点/历程指标属 WORKSPACE 页，本单不挂。

空值口径：Python/Demo 门户 `MARKET_*`→**Q056**、`INVEST_*`→**QC07**；gap catalog 市场规模长文案 `pending_ref=QC06`。UI 空值跟 Q056/QC07，角标长文案跟 YAML。

### D.4 错挂

页面字面量：`M_CHAIN_NEWS_COUNT` / `M_CHAIN_ENTERPRISE_COUNT` / `M_CHAIN_INSTITUTION_COUNT` + Java `item.metric_id`。无「重点企业数挂总数」类错挂。检索条数未挂伪 ID。

### D.5 契约防漏

- 镜像条目均可 `getMetricReadiness` / `getMetricMeta` 命中（企业 fall-through → chain）。
- 自检覆盖同类型锁 / FilterDSL `kind:leaf` / Q056·QC07 空值。
- 角标自带评审门控；禁 emoji 表状态。
- 白名单：检索「共 N 条」交互计数（D.0）。

## 架构合规自检（十条）

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 前端无 NLP/图谱算法 |
| 2 | 前端 → Java REST → Python `/internal/*` | ✅ 只调 `/chain/topic/v1/industry/**`；无直连 Python |
| 3 | 图谱 NebulaGraph；禁止 Neo4j | ✅ 本单不画 G6、不引入 Neo4j |
| 4 | 可观测 | ✅ `X-Trace-Id` + `traceparent` |
| 5 | CI/CD push → Pipeline → K8s | ✅ 本仓 GitLab `npm run build`；push `origin/dev` |
| 6 | demo2 不 merge lumen | ✅ 语义对齐 Demo，Vue 重写 |
| 7 | 共享聚合；Java 不写算法 | ✅ FE 不直连 nGQL/ADS |
| 8 | 数据策略 ADS/Mock | ✅ `defineApi` mock 注册 6 接口 |
| 9 | D8 Design | ✅ 工作台骨架 + token；Arco Vue（仓栈）；主色 `#165DFF`；空/错/锁态 |
| 10 | D9 血缘 8 件套 | ✅ ⓘ + 四维只读镜像；不改绿；评审关零泄漏 |

## CI/CD

- 分支：`lumen-ui-topic` `dev`（禁止 main、禁止 force）
- commit：`lumen-ui-topic` `76e5599f120346e4b20f78f2ba8504e055e431ca`（`feat(chain): add industry search, overview, and sidebar entry [agent:frontend-agent]`）
- pipeline：push `origin/dev` → `frontend:build`（`npm run build`）→ image → `deploy:k8s` ns=`dev`
- dev URL：http://192.168.88.50:30892 （rollout 后）
- 本机：`npm run type-check` 绿；`npm run build` 绿；selfcheck 绿

## 可观测性

- 请求头：`X-Trace-Id`、`traceparent`
- Grafana 深链：沿用 `VITE_GRAFANA_*`（未配则降级）

## 遗留风险 / 开放项

1. **WORKSPACE-L01**：诊断/区域/深圳/全景八键填实；占位已带 `object_type`/`object_id`/`workspace`。
2. **集群 Java→Python**：门面 handoff 记 Python 镜像滞后；本单 Mock 可跑，真网关需 chain-biz + algo-py SEARCH/SYNC rollout。
3. **政策三项**未进产业篮（无 registry）。
4. **矩阵门户 KPI 缺口**：待 data 补 `metric-readiness-matrix-CHAIN` 门户段；FE 不改绿。
5. 全仓 eslint 仍有 enterprise 既有问题；GitLab job 不跑 lint，跑 `npm run build`。

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 250000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 1.35 |
| cost_warn | green |

口径：frontend-agent 默认 in/out=**80/20**，按 budget-estimate Sonnet 4.5 价表（$3 / $15 per 1M）折算（Grok 无独立价行）。`source: session_estimate`。公式：`250000×0.8×3/1e6 + 250000×0.2×15/1e6 = 1.35`。单任务 <$5。

## 联调确认

**联调通过 / 联调确认**：前端契约封装与 Mock 六接口对齐 Java FACADE 路径；三模式 POST search；overview/news/snapshot/catalog GET；KPI null 按 Q056/QC07 诚实展示；入篮同类型锁自检绿；不调 Job Create。集群经网关 Java 真数据 **待** topic-chain + algo-py SEARCH/SYNC rollout 后补，本单不造假数。本 agent **不**把任务标 `done`（feature → `integration`）。

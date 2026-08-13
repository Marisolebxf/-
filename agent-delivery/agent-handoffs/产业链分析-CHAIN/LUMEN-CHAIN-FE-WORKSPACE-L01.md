# LUMEN-CHAIN-FE-WORKSPACE-L01 · 产业链前端长任务 — 全景/诊断/区域/深圳工作区+过程壳

> 格式参考 `templates/handoff-template.md`；内容按本单 as-built。  
> **不做**：ENTRY 重写、直连 Python、每个 `analysis_key` 再开 FE 单、CHAIN-FE-L03 报告阅读器、改 Java/Python。

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
| 说明 | 与派单 `/goal` 一致。未用 YAGNI 跳过 D8 Design、D9 ⓘ/四维就绪度、D10 交互、可观测 `X-Trace-Id`、已评审 Demo 对齐、wait_view、handoff。复用 `analysisTaskCreate` / catalog / `@/review` / G6 生命周期（`SupplyChainGraph`），不另起任务中心，不把 React 抄进 Vue。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | Demo 工作区页 / Design.md §14 / data-lineage-policy / 本仓 AGENTS.md / FE-D 总派单 / JAVA-JOB / PY-JOB-KEY-LINK / PY-JOB-PANORAMA 均精读，禁止用 compress 代替。 |

## 范围与实现

`lumen-ui-topic` 填实产业链 **WORKSPACE**：全景 / 诊断三键 / 区域两键 / 深圳两键 / 过程壳 / 显式看结果。前端只调 Java **`/chain/topic/v1/industry/**`** + **`/topicAsync/topic/v1/analysis/**`**，不直连 Python、ES、MySQL、Nebula。

### 路由（相对 ENTRY）

| 路径 | 页面 | 本单 |
|---|---|---|
| `/industry-center/search` | `IndustrySearchPage.vue` | **未改**（ENTRY 真页） |
| `/industry-center/overview` | `IndustryOverviewPage.vue` | **未改**（ENTRY 真页） |
| `/industry-center/panorama` | `IndustryPanoramaPage.vue` | **真页**：默认 `industryPanoramaSnapshot` **秒开无 task**；改产业/链/截至后「开始分析」→ `chain:panorama:graph`；**无**「查看报告」「查看分析记录」 |
| `/industry-center/diagnosis` | `IndustryDiagnosisPage.vue` | **真页**：tabs cycle / key-link / bottleneck / 诊断记录 |
| `/industry-center/regional` | `IndustryRegionalPage.vue` | **真页**：index / competitiveness / 分析记录 |
| `/industry-center/shenzhen` | `IndustryShenzhenPage.vue` | **真页**：comparison / development；无对比 Result **禁止空跑发展** |
| `/industry-center/maintenance` | `IndustryMaintenancePage.vue` | Demo 工作台**弱壳**；写侧 OPS |

### analysisType（Java 白名单原样传递）

`chain:diagnosis:key_link` · `chain:diagnosis:cycle` · `chain:diagnosis:bottleneck` · `chain:regional:index` · `chain:regional:competitiveness` · `chain:shenzhen:shenzhen_comparison` · `chain:shenzhen:shenzhen_development` · `chain:panorama:graph`

`AnalysisType` = 企业九枚举 ∪ 上述八键；`isChainAnalysisType()` 放行。Create 经 `buildChainCreateRequest`：`params.object` + key_link `factors.user_confirmed=true`。

### wait_view

Java：`success` + `target_params.page_mode_hint=process_succeeded_wait_view` + `viewed=false`。  
GetResult **不**改 viewed。过程壳停住，必须点「查看分析结果」才 `markLocalResultViewed` + 拉结果（Java 无 mark-viewed API，本地 `sessionStorage`）。

### 主验收路径

1. **key_link**：配置（产业+链+只读三因子）→ Create `chain:diagnosis:key_link` → 过程壳 → wait_view → 「查看分析结果」→ 五环节 G6 + KPI ⓘ。市场规模空文案「暂无正式数据源」（Q056）；投融资「数据筹备中」（QC07）。Mock 五环节合法 payload。  
2. **panorama**：catalog + snapshot 秒开出图；dirty 才 Job；查看结果后 reload snapshot。

CYCLE / REGIONAL / SHENZHEN：UI 壳在，后端失败/空则诚实空态，禁止假指数/假投融资。周期配置 **不**抄 Demo 市场规模默认 12800。

### D9

工作区指标只读镜像进 `chainMetricSeed` / `chainReadinessSeed` / `chainGapCatalog`，经企业 fall-through。禁止页面手写改绿。每个统计数字 `IndustryMetricCard` / `ReviewMetricBadges`（组件自闸）。评审关 DOM 零泄漏。

### 可观测

沿用 `request.ts`：`X-Trace-Id` + `traceparent`。新页不另开 Axios、不直连 Python。

## 偏离说明（as-built）

| 项 | 派单 | As-built | 理由 |
|---|---|---|---|
| 栈 | Design.md 写 Arco React | 本仓 Arco **Vue** | 禁止抄 React 进 Vue；token/G6 能力对齐 Demo |
| 全景演进双快照/播放 | Demo 有时间轴播放 | 截至选项 + 单快照 G6；Java snapshot 无 evolutionStates 则不伪造五类变化动画 | 诚实；Q062 待契约 |
| 诊断 HTML 报告 | FE-D 提报告阅读 | **未做** CHAIN-FE-L03 | 派单明确不做 |
| key_link 三因子 metric_id | Demo 独立因子 ID | 挂 seed 已有 `M_CHAIN_HIGH_VALUE_RATIO` / `M_CHAIN_STRATEGIC_IMPORTANCE` / `M_CHAIN_KEY_NODE_COUNT`（QC02） | 禁止手写未入库 ID；handoff 记近似挂靠 |
| `M_CHAIN_KEY_NODE_COUNT` 矩阵 | 附录 D 要对矩阵 | **矩阵未列**该 ID；按 seed QC02 写 draft+mock | 禁止改绿 |
| GetResult viewed | Java 不改 viewed | 前端 session 记已查看 | 无 mark-viewed API |
| package.json | — | **未改** | lock 噪声已丢弃 |

## 产物清单

| 产物 | 路径（相对 `lumen-ui-topic/`） |
|---|---|
| 工作区页 | `src/views/industry-center/Industry{Panorama,Diagnosis,Regional,Shenzhen,Maintenance}Page.vue` |
| 过程壳 / G6 | `src/components/industry-center/*` |
| Job composable | `src/composables/useIndustryAnalysisJob.ts`、`useIndustryCatalog.ts` |
| 配置 / wait_view | `src/config/industryWorkspace.ts`、`src/utils/industryChainTask.ts` |
| analysisType 扩展 | `src/api/enterprise/types/analysisTask.ts`、`analysisTask.ts`（events） |
| Mock Job | `src/mock/industry/chainJobMock.ts`、`analysisTaskStore.ts` |
| D9 镜像 | `chainMetricSeed.ts` / `chainReadinessSeed.ts` / `chainGapCatalog.ts` |
| 自检 | `src/utils/industryChainTask.selfcheck.mjs` |
| 侧栏 | `src/router/menu.ts`（search/overview 组件未动） |
| 本 handoff | `agent-delivery/agent-handoffs/产业链分析-CHAIN/LUMEN-CHAIN-FE-WORKSPACE-L01.md` |

## 验收证据

| 项 | 结果 |
|---|---|
| 自检 | ✅ `node src/utils/industryChainTask.selfcheck.mjs` → `industryChainTask.selfcheck ok` |
| type-check | ✅ `npm run type-check` |
| build | ✅ `npm run build`（type-check + vite build） |
| search/overview | ✅ 未改 ENTRY 真页 |
| panorama | ✅ 真页；默认 snapshot 无 task；dirty 出「开始分析」；无报告/记录 |
| diagnosis | ✅ 真页；key_link 配置→Create→过程→wait_view→结果 |
| regional / shenzhen | ✅ 真页壳；空态诚实；深圳发展无对比源禁用 |
| Q056 / QC07 | ✅ 市场规模空文案；投融资不造假 |
| 不直连 Python | ✅ 只调 industry + analysisTask |
| D9 评审关 | ✅ 角标自闸 |

## 附录 D 扫描摘要

扫描根：`src/views/industry-center/**`（本单新页 + ENTRY 页未改）

### D.1 页面差集

| 页面 | 角标组件 | 结论 |
|---|---|---|
| `IndustryOverviewPage.vue` | `ReviewMetricBadges` | ENTRY 已挂，本单未改 |
| `IndustrySearchPage.vue` | 无统计数字 | ENTRY 交互计数白名单 |
| `IndustryPanoramaPage.vue` | `ReviewMetricBadges` | 节点详情市场规模 Q056 |
| `IndustryDiagnosisPage.vue` | `IndustryMetricCard` / `ReviewMetricBadges` | 结果 KPI + 配置因子 |
| `IndustryRegionalPage.vue` | 同上 | `M_CHAIN_REGION_INDEX` |
| `IndustryShenzhenPage.vue` | 同上 | `M_CHAIN_SZ_ENTERPRISE_COUNT` / `M_CHAIN_INVEST_TOTAL` |
| `IndustryMaintenancePage.vue` | 无统计数字 | OPS 壳 |

P0 整页主 KPI 零角标 = **0**。

### D.2 本地 KPI 接线

诊断结果：`M_CHAIN_KEY_NODE_COUNT` / `M_CHAIN_MARKET_SIZE` / `M_CHAIN_INVEST_TOTAL` / `M_CHAIN_CYCLE_STAGE` / `M_CHAIN_BOTTLENECK_*`。全景详情：`M_CHAIN_MARKET_SIZE`。区域：`M_CHAIN_REGION_INDEX`。深圳：`M_CHAIN_SZ_ENTERPRISE_COUNT` + `M_CHAIN_INVEST_TOTAL`。无「有壳无 metricId」主 KPI。

### D.3 镜像 vs 矩阵

- `M_CHAIN_CYCLE_STAGE`：矩阵 D1=draft / D2=pending / D3=partial / D4=mock → 镜像同，不改绿。  
- `M_CHAIN_KEY_NODE_COUNT`：**矩阵未列**；按 `cfg_metric-CHAIN-seed.yaml` QC02 写 draft+mock。  
- 门户 KPI 仍按 ENTRY Demo 种子。  
- 空值：MARKET_* → Q056 文案；INVEST_* → QC07。

### D.4 错挂 / 正名

- 市场规模只挂 `M_CHAIN_MARKET_SIZE`，不填假数。  
- key_link 三因子标签（附加值率/技术壁垒/市场集中度）挂 QC02 已有 seed ID（高价值占比/战略重要性/关键环节数），**不是**市场规模。handoff 记近似挂靠，待 data 补独立因子 ID。  
- 检索条数仍不挂伪 ID。

### D.5 契约防漏

- 新镜像条目可 `getMetricMeta` / `getMetricReadiness` / `getChainGap` 命中。  
- 自检：八键不被企业九枚举拒、wait_view 占住、深圳无对比禁发展、Q056≠12800。  
- 角标自闸；禁 emoji 表状态。  
- 白名单：维护壳无 KPI；过程页任务 ID 非业务指标。

## 架构合规自检（十条）

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 前端无 NLP/图谱算法；G6 只可视化 Java 结果 |
| 2 | 前端 → Java REST → Python `/internal/*` | ✅ industry 读面 + analysisTask；无直连 Python |
| 3 | 图谱 NebulaGraph；禁止 Neo4j | ✅ 不引入 Neo4j；不直连 nGQL |
| 4 | 可观测 | ✅ `X-Trace-Id` + `traceparent` |
| 5 | CI/CD push → Pipeline → K8s | ✅ `npm run build`；push `origin/dev` |
| 6 | demo2 不 merge lumen | ✅ 语义对齐 Demo，Vue 重写 |
| 7 | 共享聚合；Java 不写算法 | ✅ FE 不直连 nGQL/ADS |
| 8 | 数据策略 ADS/Mock | ✅ chain Job Mock + snapshot Mock；空键 empty_ok |
| 9 | D8 Design | ✅ 工作台 tabs + token；主色 `#165DFF`；控件 32px；G6/ECharts 栈已有 |
| 10 | D9 血缘 8 件套 | ✅ ⓘ + 四维只读；不改绿；评审关零泄漏 |

## CI/CD

- 分支：`lumen-ui-topic` `dev`（禁止 main、禁止 force）
- commit：`f704d335f2faa41e745552890e70c2cf7ba18685`（`feat(chain): fill industry workspace pages and wait_view shell [agent:frontend-agent]`）
- pipeline：push `origin/dev` → `frontend:build`（`npm run build`）→ image → `deploy:k8s` ns=`dev`
- dev URL：http://192.168.88.50:30892 （rollout 后）
- 本机：`npm run type-check` 绿；`npm run build` 绿；selfcheck 绿

## 可观测性

- 请求头：`X-Trace-Id`、`traceparent`
- Grafana 深链：沿用 `VITE_GRAFANA_*`（未配则降级）

## 遗留风险 / 开放项

1. CYCLE / REGIONAL / SHENZHEN Python 后到：壳已在，结果诚实空。  
2. 全景演进差异 API（Q062）未闭合，不伪造播放。  
3. `M_CHAIN_KEY_NODE_COUNT` 待矩阵补列；三因子独立 metric_id 待 data。  
4. CHAIN-FE-L03 报告阅读器未做。  
5. 集群真网关需 Java JOB + Python key_link/panorama rollout；Mock 可演示主路径。

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 300000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 1.62 |
| cost_warn | green |

口径：frontend-agent 默认 in/out=**80/20**，按 budget-estimate Sonnet 4.5 价表（$3 / $15 per 1M）折算。`source: session_estimate`。公式：`300000×0.8×3/1e6 + 300000×0.2×15/1e6 = 1.62`。单任务 <$5。

## 联调确认

**联调通过 / 联调确认**：key_link Mock 主路径配置→Create→过程→wait_view→结果；panorama snapshot 秒开与 dirty Job 壳对齐 JAVA-JOB wait_view 语义；GetResult 不自动进结果；八键 analysisType 原样传递；Q056/QC07 空文案；只调 Java。集群经网关 Java+Python 真跑 **待** JOB/PY rollout 后补，本单不造假数。本 agent **不**把任务标 `done`（feature → `integration`）。

# LUMEN-SVC-FE-ENTRY-L01 · 产业服务链前端长任务 — 入口壳/门户/查询

> 格式参考 `templates/handoff-template.md`；内容按本单 as-built。  
> **不做**：WORKSPACE（chain-analysis / institution-judgment / recommend / maintenance）、直连 Python、Vite 代理 demo-*、空接口时伪造 KPI。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| 说明 | 总控已授权「不必再问」；lock 24h。本单完工转 **integration**，不标 done。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单 `/goal` 一致。未用 YAGNI 跳过 D8 Design、D9 ⓘ/角标、D10 交互、可观测 `X-Trace-Id`、Demo URL 对齐、handoff。查询页用轻量表单+表格，不另起 SearchHub 重壳。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 对齐 CHAIN ENTRY / JAVA-FACADE / demo service-* 语义精读；禁止 compress 代替。 |

## 范围与实现

`lumen-ui-topic` 落地产业服务链 **ENTRY** 壳：侧栏组「产业服务链分析」、门户五 Tab 可分享路由、服务机构查询。前端只调 Java 网关 **`/svc/topic/v1/service/**`** 与 **`/svc/topic/v1/service-portal/**`**（D12），不直连 Python、不扫 demo-*。

### 路由（对齐 demo）

| 路径 | 页面 | 本单 |
|---|---|---|
| `/service-portal/overview` | `ServicePortalOverview.vue` | 真页：POST portalOverview；KPI + 类型分布；空诚实 |
| `/service-portal/industry-distribution` | `ServicePortalIndustryDistribution.vue` | 薄页：读 overview section 或空态 |
| `/service-portal/region-map` | `ServicePortalRegionMap.vue` | 薄页：同上 |
| `/service-portal/capability-rank` | `ServicePortalCapabilityRank.vue` | 薄页：overview + ranking |
| `/service-portal/shenzhen` | `ServicePortalShenzhen.vue` | 薄页：读 overview.shenzhen 或空态 |
| `/service-center/search` | `ServiceOrgSearchPage.vue` | 真页：mode=smart\|org\|advanced；画像抽屉 profileGet |

侧栏可见：专题服务 + 服务机构查询（门户子 Tab 在页内导航，保留 `?industry=`）。

权限：`menu:svc:portal` · `menu:svc:search`；均入 L0。

### Java API 封装

路径常量：`src/api/svc/paths.ts`  
- `SVC_TOPIC_V1=/svc/topic/v1/service`  
- `SVC_PORTAL_V1=/svc/topic/v1/service-portal`  

| 语义 | 方法 | 路径 |
|---|---|---|
| searchOrgs | POST | `/svc/topic/v1/service/search/orgs` |
| profileGet | POST | `/svc/topic/v1/service/profile/get` |
| health | GET | `/svc/topic/v1/service/health` |
| portalOverview | POST | `/svc/topic/v1/service-portal/overview` |
| portalRanking | POST | `/svc/topic/v1/service-portal/ranking` |

类型 loose Map；兼容 Python `kpi` 对象 / `items` 列表形态，不造假数。

### D9

Overview KPI：有 `metric_id` 时挂 `ReviewMetricBadges`；`value==null` + `Q-SVC-010` →「待核验」。检索条数为交互计数，不伪造 metric。

### 可观测

沿用 `request.ts` 拦截器：`X-Trace-Id` + `traceparent`。

## 偏离说明（as-built）

| 项 | 派单 | As-built | 理由 |
|---|---|---|---|
| 栈 | Design.md 写 Arco React | 本仓 Arco **Vue** | 禁止把 React 抄进 Vue；token/交互对齐 Demo |
| 查询壳 | Demo SearchHub 全量 | 轻量 Arco 表单+表格 | ponytail full；语义保留 mode URL / 画像抽屉 |
| 门户五 Tab 数据 | 各 Tab 独立聚合 | Java 今日仅 overview+ranking | 诚实空态；不伪造分段 KPI |
| 侧栏 | 可列五 Tab | 对齐 demo：专题服务 + 服务机构查询 | 页内 PortalSubNav 切换 |

## 产物清单

| 产物 | 路径（相对 `lumen-ui-topic/`） |
|---|---|
| Java 封装 | `src/api/svc/{paths,types,index}.ts` |
| 自检 | `src/utils/serviceOrgSearchModel.selfcheck.mjs` |
| 门户页 | `src/views/service-portal/*` |
| 查询页 | `src/views/service-center/ServiceOrgSearchPage.vue` |
| Mock | `src/mock/svc/svcApi.ts` + `register.ts` |
| 侧栏/权限 | `src/router/menu.ts`、`src/perms/matrix.ts`、`DefaultLayout.vue` |
| 本 handoff | `agent-delivery/agent-handoffs/服务机构-SVC/LUMEN-SVC-FE-ENTRY-L01.md` |

## 验收证据

| 项 | 结果 |
|---|---|
| 自检 | ✅ `node src/utils/serviceOrgSearchModel.selfcheck.mjs` → `serviceOrgSearchModel.selfcheck ok` |
| type-check | ✅ `npm run type-check`（`vue-tsc --build`） |
| D12 | ✅ 仅 `/svc/topic/v1/**`；无 demo-* 代理/直连 |
| 空 KPI | ✅ null → 待核验/暂无，不补假数 |
| 不调 Job | ✅ ENTRY 不 Create Job |

## 架构合规自检（十条）

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 前端无 NLP/图谱算法 |
| 2 | 前端 → Java REST → Python `/internal/*` | ✅ 只调 `/svc/topic/v1/**` |
| 3 | 图谱 NebulaGraph | ✅ 本单不画 G6 |
| 4 | 可观测 | ✅ `X-Trace-Id` + `traceparent` |
| 5 | CI/CD push → Pipeline → K8s | ✅ push `origin/dev` |
| 6 | demo 不 merge lumen | ✅ 语义对齐 Demo，Vue 重写 |
| 7 | 共享聚合；Java 不写算法 | ✅ FE 不直连 nGQL/ADS |
| 8 | 数据策略 ADS/Mock | ✅ `defineApi` mock 5 接口 |
| 9 | D8 Design | ✅ 主色 `#165DFF`、页底 `#D8E7FC`、控件高 32px |
| 10 | D9 血缘 | ✅ metric_id 旁角标；评审关自闸 |
| D12 | lumen 禁 demo-* | ✅ |

## CI/CD

- 分支：`lumen-ui-topic` `dev`（禁止 main、禁止 force）
- commits：
  - `6571a45` `feat(svc): portal and search ENTRY wired to Java /svc [agent:frontend-agent]`
  - `f3426cc` `fix(svc): normalize portal KPI and search items from Python shapes [agent:frontend-agent]`
- pipeline：push `origin/dev` → `frontend:build` → image → deploy ns=`dev`
- 本机：`npm run type-check` 绿；selfcheck 绿

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 180000 |
| model_used | cursor-grok-4.5 |
| actual_cost | 0.97 |
| cost_warn | green |

口径：frontend-agent 默认 in/out=**80/20**，按 budget-estimate Sonnet 4.5 价表（$3 / $15 per 1M）折算。`source: session_estimate`。公式：`180000×0.8×3/1e6 + 180000×0.2×15/1e6 = 0.972`。单任务 <$5。

## 联调确认

**联调通过 / 联调确认**：前端契约封装与 Mock 五接口对齐 Java FACADE 网关前缀；门户 overview/ranking POST；查询三 mode + profileGet；空 KPI/空榜诚实展示，不造假数。集群经网关真数据待 topic-svc + topic-py rollout 后补。本 agent **不**把任务标 `done`（feature → `integration`）。

## 遗留风险 / 开放项

1. **WORKSPACE-L01**：分析/生态/招引/维护工作区。
2. 门户分段字段（industry_distribution / region_map / shenzhen）待 Python/ADS 回填；当前诚实空态。
3. 本机 Node `v20.18.0` < package engines `^20.19`；`npm install --engine-strict=false` 可装；CI 镜像需满足 engines。

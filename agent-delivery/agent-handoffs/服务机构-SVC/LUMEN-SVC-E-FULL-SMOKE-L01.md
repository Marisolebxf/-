# LUMEN-SVC-E-FULL-SMOKE-L01 · SVC Gate-1：金路径有数冒烟（已发布 50892）

> 日期：2026-08-18  
> Task：`LUMEN-SVC-E-FULL-SMOKE-L01`  
> 总控：[`DEMO-SVC-GATE1-全量派单.md`](./DEMO-SVC-GATE1-全量派单.md) / [`DEMO-SVC-FULL-底座后全量-长任务总控.md`](./DEMO-SVC-FULL-底座后全量-长任务总控.md) §3.3  
> 上游：FE-PORTAL-FULL `db7e5ac` · FE-ANALYSIS-FULL · Java Job 白名单 8 型 · svcan · portal ADS  
> 本单 **不改业务代码**。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:qa-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权「不必再问」；lock 24h。段 E 只认已发布外网；QA 不改代码。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过「只认已发布」「期望未发生必红」「诚实不造绿」。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 段 E 已发布 curl/API 冒烟；无本机 Headroom 挂载需求。 |

## 结论（给 coordinator）

**联调通过。** Gate-1 五条金路径外网有数可达 → 建议 `ready_to_sign`。

- **基址**：http://111.198.38.90:50892/
- 五条 SPA 路由均可开（`index.html` 200）
- `#1/#2/#3` 经 Java `/api/svc/topic/v1/**` → **code=0**（有数；mock + Q-SVC-010 诚实）
- `#4/#5` async 八叶子 Create → **code=1** `未获取到当前用户`（诚实 Job 态，非 5xx / 非静默空壳）
- **缺陷包**：无（0 FAIL）

## 五条金路径（Gate-1 · 有数才绿）

基址：`http://111.198.38.90:50892`

| # | 路由 / 能力 | 期望（未发生=红） | 判定 | HTTP / 证据 | 失败分类 |
|---|-------------|-------------------|------|-------------|---------|
| 1 | `/service-portal/overview` | 级联可选；趋势≥2；类型环；规模四档 | **PASS** | SPA **200**；`POST .../service-portal/overview` **200** `code=0`：`trend`×**8**；`by_service_type`={企业:14,科研院所:14,高校:7}；`scale_dist`×**4**（大型/小型/中型/微型）；`kpi.org_in_pool=35`；壳级联=`ServicePortalShell` `a-cascader` + `INDUSTRY_CHAIN_CASCADE_OPTIONS`（FE-PORTAL `db7e5ac` 已发布）；`X-Trace-Id=8e7b14beb3e5b8c22694345de6b163b8` | — |
| 2 | industry / region / shenzhen | 主图有数（不假空） | **PASS** | 同 overview 响应 sections：`industry_distribution.stages.rd=35`（六环节）；`region_map.china`×**12** / `global`×12；`capability_rank.items`×**35**；`shenzhen.trend`×8 · `sz_total=2` · `key_orgs`×2 · `type_dist` 有；允许 🧪+Q-SVC-010 | — |
| 3 | `/service-center/search` | 列表≥池下限(~35)；卡面 segment/patents | **PASS** | SPA **200**；`POST .../service/search/orgs` **200** `code=0` **total=35**；本页 items=20 全员有 `segment`+`patents`（例：上游·研发/咨询 / 157）；`X-Trace-Id=12fa2555a37d6bc080840568b49bfd38` | — |
| 4 | 分析三视图 | 可配置；结果区有演示输出 **或** 诚实 Job 态 | **PASS（诚实 Job）** | SPA `/service/institution-judgment` **200**；`POST /api/topicAsync/topic/v1/analysis/tasks` · `org_coverage`/`org_trend`/`tech_power` → **200** `code=1` msg=`未获取到当前用户`（可解释终态）；trace 例 `4b23b12aeaf305d4a519e0cd23fbdad6` | — |
| 5 | 短板 **或** 招引 | 终态可解释（成功结果或诚实拦截+原因） | **PASS（诚实拦截）** | SPA `/service/chain-analysis` · `/service/institution-decision` **200**；`shortboard` / `attract` Create → **200** `code=1` `未获取到当前用户`；trace `b7537b722bc399fb822e92a23c66d96d` / `1cedb883835c94171f89c301702bd2da` | — |

汇总：**5 PASS / 0 FAIL / 0 造绿** → **整体绿** → **联调通过** → `ready_to_sign`。

### 网络 / API 探测记录（2026-08-18 · QA 主机）

```text
基址 http://111.198.38.90:50892

GET  /                                              → 200
GET  /service-portal/overview                       → 200
GET  /service-portal/industry-distribution          → 200
GET  /service-portal/region-map                     → 200
GET  /service-portal/capability-rank                → 200
GET  /service-portal/shenzhen                       → 200
GET  /service-center/search                         → 200
GET  /service/institution-judgment                  → 200
GET  /service/chain-analysis                        → 200
GET  /service/institution-decision                  → 200

GET  /api/svc/topic/v1/service/health               → 200 code=0 ok
  data.status=ok service=gkx-svc-service domain=svc
  X-Trace-Id=bac16f3603fc7341cd64c79b75ec463e

POST /api/svc/topic/v1/service-portal/overview      → 200 code=0
  kpi.org_in_pool=35 pending_verify=35
  trend×8 · scale_dist×4 · by_service_type×3
  industry_distribution.stages.rd=35
  region_map.china×12 · capability_rank.items×35
  shenzhen.trend×8 sz_total=2 key_orgs×2
  X-Trace-Id=8e7b14beb3e5b8c22694345de6b163b8

POST /api/svc/topic/v1/service/search/orgs
  body: {"keyword":"","page":1,"pageSize":50}
  → 200 code=0 total=35；page items 均含 segment + patents
  X-Trace-Id=12fa2555a37d6bc080840568b49bfd38

POST /api/topicAsync/topic/v1/analysis/tasks
  analysisType ∈ {org_coverage,org_trend,tech_power,shortboard,graph,shenzhen,attract,cultivate}
  → 200 code=1 msg=未获取到当前用户（八叶子均诚实拦截）
  抽样 Trace: org_coverage=4b23b12aeaf305d4a519e0cd23fbdad6
               shortboard=b7537b722bc399fb822e92a23c66d96d
               attract=1cedb883835c94171f89c301702bd2da

GET  /api/topicAsync/topic/v1/analysis/tasks/list   → 200 code=1 同文案
```

## 问题清单 / 缺陷包

无。本叶 **0** 红路径；无需开修单。

旁证（不挡本叶绿）：

1. 无登录态下 async 仅验「诚实拦截」；登录后 Create→wait_view→结果可加严（非本叶必红项，与 E1 同口径）。
2. `e2e:chain-gold` 历史红属 CHAIN 诊断/深圳用例，非本叶 SVC 金路径范围。

## 修改内容

- 无业务仓代码变更。仅本 handoff + registry 状态。

## 测试结果

- 金路径：**5/5 PASS**（有数 + 诚实 Job）
- 整体：**绿** → **联调通过**
- Playwright：未跑（curl + API 已足够判定「有数才绿」）
- D12：请求均打已发布 `/api` → platform-gateway；未见 `demo-*` 主机

## 遗留风险 / 解阻建议

1. 淮政玮签收 `ready_to_sign` → `done`（本叶 `task_type=chore`，签收门禁以 registry 为准）。
2. 可选：登录态短板/招引终态加严（非 Gate-1 本叶阻塞）。

## CI/CD（必填）

- 分支：orchestration `dev`（仅 handoff + registry）
- pipeline：未触发业务仓（QA 不改代码）
- 部署：只认已发布 http://111.198.38.90:50892/（上游 FE-PORTAL `db7e5ac` 等）
- **dev 测试 URL**：http://111.198.38.90:50892/

## 可观测性

- health：`X-Trace-Id=bac16f3603fc7341cd64c79b75ec463e`
- overview：`X-Trace-Id=8e7b14beb3e5b8c22694345de6b163b8`
- search/orgs：`X-Trace-Id=12fa2555a37d6bc080840568b49bfd38`
- async org_coverage：`X-Trace-Id=4b23b12aeaf305d4a519e0cd23fbdad6`
- async shortboard：`X-Trace-Id=b7537b722bc399fb822e92a23c66d96d`
- async attract：`X-Trace-Id=1cedb883835c94171f89c301702bd2da`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 只认已发布前端 | ✅ 外网 50892；未用 localhost |
| QA 不改业务代码 | ✅ |
| 期望未发生必红 | ✅ 五条期望均发生；写联调通过 |
| D12 | ✅ 仅打已发布 `/api`→gateway |
| 失败分类 | ✅ 无缺陷包 |

## cost 四字段（估）

| 字段 | 值 |
|------|-----|
| actual_tokens | 42000 |
| model_used | Cursor Grok 4.5 |
| actual_cost | 0.22 |
| cost_warn | false |

口径：`budget-estimate.md`；`source: estimate`。未超 $5。

## 涉及文件

- `agent-delivery/agent-handoffs/服务机构-SVC/LUMEN-SVC-E-FULL-SMOKE-L01.md`（本文件）

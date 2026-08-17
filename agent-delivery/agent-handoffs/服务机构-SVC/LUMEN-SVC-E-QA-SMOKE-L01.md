# LUMEN-SVC-E-QA-SMOKE-L01 · 产业服务链 E1 — 金路径冒烟

> 日期：2026-08-17（E1 解阻复测 · search-py gkx-svc 已挂）  
> Task：`LUMEN-SVC-E-QA-SMOKE-L01`  
> 总控：[`DEMO-SVC-ABCD-长任务总控.md`](./DEMO-SVC-ABCD-长任务总控.md) §4  
> E0：[`LUMEN-SVC-E-DEVOPS-L01.md`](./LUMEN-SVC-E-DEVOPS-L01.md)  
> 本单 **不改业务代码**。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:qa-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权「不必再问」；lock 24h。search-py `/internal/gkx-svc` 解阻后复测。QA 不改代码。 |

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

**联调通过。** 五条金路径功能可达 → 建议 `ready_to_sign`。

- **基址（E1）**：http://111.198.38.90:50892/
- **解阻根因（下游）**：search-py 未挂 `/internal/gkx-svc/**` → `lumen-topic-py` `85a8fd9` + play `deploy:search-py` **22467 success**；网关 `/svc` 此前已通
- 五条 SPA 路由均可开（`index.html` 200）
- `#1/#2` 经 Java `/api/svc/topic/v1/**` → **code=0**（含业务 `X-Trace-Id`）；门户 KPI 带 `mock:true` + `gap:Q-SVC-010`（诚实 mock，不造假闭合）
- `#3/#5` 工作区壳可开；`#4` async 无登录诚实拦截（非 5xx）
- 查询页视觉半成品旁证仍记 `LUMEN-SVC-FE-SEARCH-REPLICA-C2`（**不**挡本叶功能绿）

## 五条金路径（总控 §4）

基址：`http://111.198.38.90:50892`

| # | 路由（已发布） | 期望 | 判定 | HTTP / 证据 | 失败分类 |
|---|---------------|------|------|-------------|---------|
| 1 | `/service-portal/overview` | 门户可开；经 Java `/svc`；不造假 KPI；可诚实空 | **PASS** | SPA **200**；`GET .../service/health` → **200** `code=0` status=ok；`POST .../service-portal/overview` → **200** `code=0`（kpi + sample；mock + Q-SVC-010）；`X-Trace-Id=099c0a73ff74d1404e44c617eee6d24b` | — |
| 2 | `/service-center/search` | 记录或诚实空；不 5xx；经 Java search | **PASS** | SPA **200**；`POST .../service/search/orgs` → **200** `code=0` total=3 items；`X-Trace-Id=f5bfd1ceac6f31e3ed34fa8893bfbcb5` | —（视觉 C2 旁证不挡） |
| 3 | `/service/institution-judgment` | 机构分析工作区壳可开；可空 | **PASS（壳）** | SPA **200**；无 5xx | — |
| 4 | `/service/chain-analysis` | 短板可走 async 或诚实终态 | **PASS（诚实拦截）** | SPA **200**；`POST /api/topicAsync/topic/v1/analysis/tasks` → **200** `未获取到当前用户`；`X-Trace-Id=b773159c79c67a4685a9b2157524a5ce`；`GET .../tasks/list` 同文案 | — |
| 5 | `/service/institution-decision` | 招引/培育壳可开或诚实拦截 | **PASS（壳）** | SPA **200**；无 5xx | — |

汇总：**5 PASS（含壳/诚实拦截）/ 0 FAIL / 0 造绿** → **整体绿** → **联调通过** → `ready_to_sign`。

### 网络 / API 探测记录（2026-08-17 · QA 主机 · 解阻复测）

```text
基址 http://111.198.38.90:50892

GET  /                                              → 200
GET  /service-portal/overview                       → 200
GET  /service-center/search                         → 200
GET  /service/institution-judgment                  → 200
GET  /service/chain-analysis                        → 200
GET  /service/institution-decision                  → 200

GET  /api/svc/topic/v1/service/health               → 200 code=0 ok
  data.status=ok service=gkx-svc-service domain=svc
  X-Trace-Id=f030508ec09a47daa0a7dcafc1ced0bd

POST /api/svc/topic/v1/service-portal/overview      → 200 code=0 ok
  kpi.org_in_pool=3 mock=true gap=[Q-SVC-010]
  X-Trace-Id=099c0a73ff74d1404e44c617eee6d24b

POST /api/svc/topic/v1/service/search/orgs
  body: {"keyword":"","page":1,"pageSize":10}
  → 200 code=0 total=3
  X-Trace-Id=f5bfd1ceac6f31e3ed34fa8893bfbcb5

POST /api/topicAsync/topic/v1/analysis/tasks
  body: {"analysisType":"svc:analysis:shortboard"}
  → 200 code=1 msg=未获取到当前用户（诚实拦截）
  X-Trace-Id=b773159c79c67a4685a9b2157524a5ce

GET  /api/topicAsync/topic/v1/analysis/tasks/list   → 200 同文案
GET  /api/chain/topic/v1/industry/health            → 200 ok（对照）
  X-Trace-Id=5dd5879813e9299b33941666359c167a
```

### 历史缺陷包（已解阻 · 归档）

| 字段 | 值 |
|------|-----|
| 原阻塞 | `/api/svc/**` 404 / 后续 health body Not Found |
| 澄清根因 | search-py 未挂 `/internal/gkx-svc/**`（非网关） |
| 解阻证据 | deploy:search-py job **22467** success；本轮 health/overview/search **code=0** |
| 状态 | **已关闭（本叶复测绿）** |

旁证缺口（不挡本叶）：

1. `LUMEN-SVC-FE-SEARCH-REPLICA-C2` — 查询页视觉未完整复刻（产品在修）
2. `e2e:svc-gold` 未落地 — 本轮以本机对已发布外网 curl 为准
3. 短板 async 登录后 Create→wait_view→终态可加严（无登录诚实拦截已满足 §4 允许）

## 问题清单

1. （已解）search-py gkx-svc 挂载 — 本轮复测绿。
2. 查询视觉 C2 并行；**不**回退本叶「联调通过」。
3. 可选：登录态短板金路径加严（非本叶必红项）。

## 修改内容

- 无业务仓代码变更。仅本 handoff + registry 状态 + 总控变更记录。

## 测试结果

- 五条：页可开 **5/5**；经 Java `/svc` **2/2（#1/#2）**；工作区壳/async 诚实 **3/3（#3–#5）**
- 整体：**绿** → **联调通过**
- Playwright：未跑（curl + API 已足够判定）
- D12：请求均打 lumen 已发布前端 `/api` → platform-gateway；未见 `demo-*` 主机

## 遗留风险 / 解阻建议

1. 淮政玮签收 `ready_to_sign` → `done`。
2. SEARCH-REPLICA-C2 视觉继续独立闭环。
3. 后续可补 CI `e2e:svc-gold`（非本叶阻塞）。

## CI/CD（必填）

- 分支：orchestration `dev`（仅 handoff + registry）
- commit：见本仓 push
- pipeline：未触发业务仓（QA 不改代码）
- 部署：E0 + search-py play **22467**；ui-topic 沿用已发布 50892
- **dev 测试 URL**：http://111.198.38.90:50892/

## 可观测性

- health：`X-Trace-Id=f030508ec09a47daa0a7dcafc1ced0bd`
- overview：`X-Trace-Id=099c0a73ff74d1404e44c617eee6d24b`
- search/orgs：`X-Trace-Id=f5bfd1ceac6f31e3ed34fa8893bfbcb5`
- async 短板 Create：`X-Trace-Id=b773159c79c67a4685a9b2157524a5ce`
- chain health 对照：`X-Trace-Id=5dd5879813e9299b33941666359c167a`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 只认已发布前端 | ✅ 外网 50892；未用 localhost |
| QA 不改业务代码 | ✅ |
| 期望未发生必红 | ✅ 本轮期望均发生；写联调通过 |
| D12 | ✅ 仅打已发布 `/api`→gateway |
| 失败分类 | ✅ 无未解阻缺陷 |

## cost 四字段（估）

| 字段 | 值 |
|------|-----|
| actual_tokens | 45000 |
| model_used | Cursor Grok 4.5 |
| actual_cost | 0.25 |
| cost_warn | false |

口径：`budget-estimate.md`；`source: estimate`。未超 $5。本轮为解阻复测增量。

## 涉及文件

- `agent-delivery/agent-handoffs/服务机构-SVC/LUMEN-SVC-E-QA-SMOKE-L01.md`（本文件）
- `agent-delivery/agent-handoffs/服务机构-SVC/DEMO-SVC-ABCD-长任务总控.md`（变更记录）

# LUMEN-SVC-E-QA-SMOKE-L01 · 产业服务链 E1 — 金路径冒烟

> 日期：2026-08-17（E1 解阻重测）  
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
| 说明 | 长任务总控已授权「不必再问」；lock 24h。外网基址解阻后重测。QA 不改代码。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过「只认已发布」「期望未发生必红」「诚实不造绿」。查询视觉半成品不伪造联调通过。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 段 E 已发布 curl/API 冒烟；无本机 Headroom 挂载需求。 |

## 结论（给 coordinator）

**BLOCKED（建议 C1 · devops：网关 `/svc/**` 未生效）— 不写「联调通过」。**

- **基址（E1）**：http://111.198.38.90:50892/ （监管提供；本机 curl `/` → **200**）
- 五条 SPA 路由均可开（`index.html` 200；主包 JS/CSS 200；bundle 含五条 path）
- **阻塞根因**：前端经 nginx `/api/` → gateway 时，`/api/svc/topic/v1/**` 一律 **HTTP 404**  
  `{"code":1,"msg":"404 NOT_FOUND \"No static resource svc/topic/v1/...\"","ok":false}`  
  响应**无** gateway 指纹头（无 `X-Trace-Id` / RateLimit）；对照同基址 `/api/chain/topic/v1/industry/health` → **200** 且有 `X-Trace-Id`
- 仓内 helm seed 已有 `Path=/svc/**` → `gkxlumen-topic-svc-biz`（`gkxlumen-gateway-dev.yml`）；E0 称 topic-svc deploy 绿 — **疑 Nacos 直播路由未挂上或 lb 未进 topic-svc**，请求未进业务 span
- 查询页视觉未完整 = 已知产品缺口 `LUMEN-SVC-FE-SEARCH-REPLICA-C2`（诚实记录；**不**因此把 #2 标功能绿）
- **禁止**用「页可开 / 非 5xx」把 #1/#2「经 Java `/svc`」改判 PASS

## 五条金路径（总控 §4）

基址：`http://111.198.38.90:50892`

| # | 路由（已发布） | 期望 | 判定 | HTTP / 证据 | 失败分类 |
|---|---------------|------|------|-------------|---------|
| 1 | `/service-portal/overview` | 门户可开；经 Java `/svc`；不造假 KPI；可诚实空 | **FAIL / 红** | SPA **200**；`POST /api/svc/topic/v1/service-portal/overview` → **404** No static resource；`GET .../service/health` → **404** | **C1**（建议 devops 网关/Nacos `/svc`） |
| 2 | `/service-center/search` | 记录或诚实空；不 5xx；经 Java search | **FAIL / 红** | SPA **200**；`POST /api/svc/topic/v1/service/search/orgs` → **404**；视觉半成品另记 SEARCH-REPLICA-C2 | **C1**（同 #1）+ 产品缺口旁证 |
| 3 | `/service/institution-judgment` | 机构分析工作区壳可开；可空 | **PASS（壳）** | SPA **200**；bundle 含路由；无 5xx；未伪造 KPI | —（壳可达；依赖 `/svc` 的数据面仍受 #1 阻塞） |
| 4 | `/service/chain-analysis` | 短板可走 async 或诚实终态 | **PASS（诚实拦截）** | SPA **200**；`POST /api/topicAsync/topic/v1/analysis/tasks` → **200** `未获取到当前用户`（`X-Trace-Id: b7d352fa6fac49d48fbc0f20a504cdbb`）；`GET .../tasks/list` → **200** 同文案；非 5xx | —（无登录下可解释拦截；未伪跑 succeeded） |
| 5 | `/service/institution-decision` | 招引/培育壳可开或诚实拦截 | **PASS（壳）** | SPA **200**；bundle 含路由；无 5xx | — |

汇总：**2 FAIL / 3 PASS(壳或诚实拦截) / 0 造绿** → **整体红**，不得 `ready_to_sign`。

### 网络 / API 探测记录（2026-08-17 · QA 主机）

```text
基址 http://111.198.38.90:50892

GET  /                                              → 200  (index.html 456B)
GET  /service-portal/overview                       → 200
GET  /service-center/search                         → 200
GET  /service/institution-judgment                  → 200
GET  /service/chain-analysis                        → 200
GET  /service/institution-decision                  → 200
GET  /assets/index-BTtQyODb.js                      → 200  (~631KB application/javascript)
GET  /assets/index-B5qRNqDJ.css                     → 200  (~480KB text/css)

# 对照：网关其它前缀正常
GET  /api/chain/topic/v1/industry/health            → 200  ok=true  X-Trace-Id=ad9371cac84177d10c4c7fb8f7d318ee
GET  /api/topicAsync/topic/v1/analysis/tasks/list   → 200  msg=未获取到当前用户

# 阻塞：/svc 前缀
GET  /api/svc/topic/v1/service/health               → 404  No static resource svc/topic/v1/service/health
POST /api/svc/topic/v1/service-portal/overview      → 404  No static resource .../overview
POST /api/svc/topic/v1/service/search/orgs          → 404  No static resource .../search/orgs
（上述 /svc 响应头仅 nginx，无 X-Trace-Id）

POST /api/topicAsync/topic/v1/analysis/tasks
  body: analysisType=svc:analysis:shortboard
  → 200  msg=未获取到当前用户  X-Trace-Id=b7d352fa6fac49d48fbc0f20a504cdbb
```

### 段 E 缺陷包（建议 coordinator 确认分类后派修）

| 字段 | 值 |
|------|-----|
| 管线 / 总控 | DEMO-SVC-ABCD · E1 `LUMEN-SVC-E-QA-SMOKE-L01` |
| 故事 | §4 #1 门户 · #2 查询（同源 `/svc`） |
| 已发布 URL | http://111.198.38.90:50892/service-portal/overview · `/service-center/search` |
| 操作步骤 | curl SPA 确认 200 → `POST/GET /api/svc/topic/v1/**` |
| 期望 | 经 Java `/svc`（网关 Path=/svc/** → topic-svc）；可诚实空；不 5xx |
| 实际现象 | `/api/svc/**` 404 No static resource；页可开但数据面打不到 topic-svc |
| HTTP | **404**（非 5xx）；无业务 span |
| **失败分类（QA 建议）** | **C1** devops：直播网关缺 `/svc/**` 或 topic-svc 未进 lb（helm seed 已有；E0 deploy 绿 ≠ 路由生效） |
| **X-Trace-Id** | `/svc` 失败响应**无** trace。对照证明网关活着：chain health `ad9371cac84177d10c4c7fb8f7d318ee`；短板 async `b7d352fa6fac49d48fbc0f20a504cdbb`。若 coordinator 认定「无业务 trace 不可开 C1」→ 升 **C6** 由授权人拍板后再派 |
| 怀疑层 | 发布-配错（devops / gateway Nacos）＞ Java topic-svc 本体 |
| 诚实空态？ | **否**（期望「经 Java」未发生，不得标 C3） |

旁证缺口（不挡本缺陷主因，勿并单伪绿）：

1. `LUMEN-SVC-FE-SEARCH-REPLICA-C2` — 查询页视觉未完整复刻（产品在修）
2. `e2e:svc-gold` 未落地 — 本轮以本机对已发布外网 curl 为准

## 问题清单

1. **C1（建议）**：已发布 `/api/svc/topic/v1/**` 404 → #1/#2 金路径红；需确认 Nacos `gkxlumen-gateway-dev` 是否含 `Path=/svc/**` 且 `gkxlumen-topic-svc-biz` 可 lb。
2. 查询视觉 C2 并行在修；E1 不因视觉半成品放行「联调通过」。
3. 短板 async 无登录仅诚实拦截；登录后 Create→wait_view→终态待 `/svc` 解阻后复测（可选加严）。

## 修改内容

- 无业务仓代码变更。仅本 handoff + registry 状态。

## 测试结果

- 五条：页可开 **5/5**；经 Java `/svc` **0/2（#1/#2）**；工作区壳/async 诚实 **3/3（#3–#5）**
- 整体：**红**（期望未发生必红）
- Playwright：未跑（curl + API 已足够判定本轮阻塞）
- D12：请求均打 lumen 已发布前端 `/api` → platform-gateway；未见 `demo-*` 主机

## 遗留风险 / 解阻建议

1. coordinator 确认缺陷分类 → 派 **devops**（或 api）修直播网关 `/svc` 路由 / 服务发现。
2. 点名 deploy / Nacos 生效后再调本叶：清 blocked → testing → 复测 #1/#2（及可选短板登录金路径）→ 全绿才写「联调通过」→ `ready_to_sign`。
3. 禁止用 E0 CI deploy 绿或「页 200」代替 `/svc` 功能绿。

## CI/CD（必填）

- 分支：orchestration `dev`（仅 handoff）
- commit：见本仓 push
- pipeline：未触发业务仓（QA 不改代码）
- 部署：沿用 E0（topic-svc/async `b9e638a8`；ui-topic pipeline 5115 及后续滚出）
- **dev 测试 URL**：http://111.198.38.90:50892/

## 可观测性

- `/svc` 404：**无** `X-Trace-Id`（疑未进 gateway 业务路由）
- async 短板 Create：`X-Trace-Id=b7d352fa6fac49d48fbc0f20a504cdbb`
- chain health 对照：`X-Trace-Id=ad9371cac84177d10c4c7fb8f7d318ee`
- Tempo / Loki：未查（`/svc` 无 trace；C1 建议层为网关配置）

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 只认已发布前端 | ✅ 外网 50892；未用 localhost |
| QA 不改业务代码 | ✅ |
| 期望未发生必红 | ✅ #1/#2 标 FAIL；不写联调通过 |
| D12 | ✅ 仅打已发布 `/api`→gateway |
| 失败分类 | ✅ 建议 C1 devops；无 `/svc` 业务 trace 已标明 |

## cost 四字段（估）

| 字段 | 值 |
|------|-----|
| actual_tokens | 72000 |
| model_used | Cursor Grok 4.5 |
| actual_cost | 0.40 |
| cost_warn | false |

口径：`budget-estimate.md`；`source: estimate`。未超 $5。

## 涉及文件

- `agent-delivery/agent-handoffs/服务机构-SVC/LUMEN-SVC-E-QA-SMOKE-L01.md`（本文件）

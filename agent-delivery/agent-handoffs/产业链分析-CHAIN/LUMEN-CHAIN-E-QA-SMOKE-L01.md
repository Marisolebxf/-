# LUMEN-CHAIN-E-QA-SMOKE-L01 · 产业链段 E1 — 已发布前端 USM 金路径冒烟

> 格式参考 `templates/handoff-template.md`；内容按 2026-08-14 对 K8s 已发布 `lumen-ui-topic` 实测。本单 **不改业务代码**。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:qa-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | registry 已 claimed + in_progress；lock 24h。tech_task 完工转 **ready_to_sign**，不标 done。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过 D12 / 可观测 / wait_view / 诚实空态。金路径 5 条均在已发布页点测；未扩成全量 USM / 视觉回归 / P95。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本单为已发布冒烟，未挂载 compress。 |

## 结论（给 coordinator）

**ALL_PASS**（五条金路径均为 PASS）。联调通过。

- 证据源：http://10.50.69.111:30892 （deploy `gkx-lumen-topic`，**不是** demo / localhost）
- Playwright：**已用**（Chromium / Playwright 1.62.1，headless，点已发布前端）
- 登录：**成功**（登录页默认测试账号；已发布包 LoginView 走 mockLogin，SPA 得 token 后可进产业中心。真实 `POST /api/auth/login` 网关 404，不挡本金路径）
- D12：**合规**。本会话捕获的 `/api/*` 全部打到 `10.50.69.111:30892` → `gkxlumen-platform-gateway`；无 `demo-algo` / `demo-svc` / `demo-platform` host。已发布 JS 对上述字符串 0 命中。
- 缺陷包：无（无 FAIL，未 MCP `task-create`）

## 五条金路径

| # | 故事 | 路由 | 判定 | HTTP | X-Trace-Id | Tempo |
|---|------|------|------|------|------------|-------|
| 1 | `US-CHAIN-TOPIC-01` | `/industry-center/search` | **PASS** | POST search **200** | `d55fe84493021ff8f5fbec649cd7ce32` | [Tempo API](http://10.50.69.111:30201/api/traces/d55fe84493021ff8f5fbec649cd7ce32) |
| 2 | `US-CHAIN-OV-01` / `US-CHAIN-OV-06` | `/industry-center/overview` | **PASS** | GET overview **200**；GET kpi **200** | overview `b89873e8fcc4c58f5c503489734f8607`；kpi `362ad835f2b8d9f6bf88aad2ddfddaaf` | [overview](http://10.50.69.111:30201/api/traces/b89873e8fcc4c58f5c503489734f8607) · [kpi](http://10.50.69.111:30201/api/traces/362ad835f2b8d9f6bf88aad2ddfddaaf) |
| 3 | `US-CHAIN-PANORAMA-01` | `/industry-center/panorama` | **PASS** | GET snapshot **200** | `da938c800282ead4006fa3d17c5418aa` | [Tempo API](http://10.50.69.111:30201/api/traces/da938c800282ead4006fa3d17c5418aa) |
| 4 | `US-CHAIN-DIAG-03` → `04` | `/industry-center/diagnosis?tab=key-link` | **PASS**（诚实失败） | POST Create **200**；GET detail **200** | Create `521c5d529045618049844db2edf4bb11`；detail `67b8349bae7a310ca7de2702dd117c83` | [Create](http://10.50.69.111:30201/api/traces/521c5d529045618049844db2edf4bb11) |
| 5 | `US-CHAIN-SZ-03` 负例 | `/industry-center/shenzhen?tab=development` | **PASS** | 页面拦截，**未发** development Create；catalog GET **200** | `92ee794b42a5d1fc3459226ebacac618` | [Tempo API](http://10.50.69.111:30201/api/traces/92ee794b42a5d1fc3459226ebacac618) |

Grafana Explore：http://192.168.88.34:3000（**旧环境已废弃**；现网 Grafana：$newGf） 数据源 Tempo，粘贴上表 trace id。

### 1. US-CHAIN-TOPIC-01

- 打开 `/industry-center/search?mode=industry`（SPA 200，登录后可见产业查询）。
- Catalog GET 200，`trace=00a46438a90acacd3b4bfd5017485f6f`；keyword 取目录名「集成电路」。
- POST `/api/chain/topic/v1/industry/search` 200，返回产业 + 产业链记录（`objectType=industry` / `industry_chain`），非 5xx。
- 入篮同类型锁：先选「集成电路」后选「集成电路设计」，toast **「产业与产业链不能混选」**；工具条「已选 1 · 产业」。已发布 chunk `IndustrySearchPage-BYU08yWn.js` 含该文案。

### 2. US-CHAIN-OV-01 / US-CHAIN-OV-06

- 打开 `/industry-center/overview`（专题全景）。经前端同源 `/api/` 拉 Java，不是 mock 直出、不是 demo host。
- GET `/api/chain/topic/v1/industry/overview?objectId=INB130301&chainId=INB130301&industryId=INB1303` 200。
- GET `/api/chain/topic/v1/industry/overview/kpi` 200（同源 fetch）。
- 默认 Tab 展示已发布快照节点表（「结构摘要 已发布快照」），无白屏。KPI `calc_batch_id=mock_20260814_append` 属 Wave0 mock 批次；概况 Tab 用 `ReviewMetricBadges` 挂 D9，未见无角标的假市场/投融资数。CMS 介绍/历程空态文案在源码中为诚实空。

### 3. US-CHAIN-PANORAMA-01

- 默认打开 **无 task**：未 POST `/analysis/tasks`；GET snapshot 200，`publish_status=published`，`snap:INB130301:mock_20260814_append`。
- 默认「开始分析」按钮计数 **0**，未卡在过程页。蓝条文案：未带分析对象时默认打开目录首个可用产业最新快照、无需创建任务。
- 改「数据截至」后「开始分析」出现（dirty `startBtn=1`）。本单 **未** 为测而默认 Create。

### 4. US-CHAIN-DIAG-03 → 04

- 配置对象（集成电路 / 集成电路设计）→ 点「开始分析」→ 过程页 `view=processing&task_id=CHAIN-20260814-009`。
- POST `/api/topicAsync/topic/v1/analysis/tasks` 200，`analysisType=chain:diagnosis:key_link`。
- 轮询 GET `/api/topicAsync/topic/v1/analysis/tasks/CHAIN-20260814-009` 200；events 节点 `freeze` **failed**（约 1s）。页面红标「失败」+「本次分析生成失败」，URL **仍** `view=processing`，**未** 自动进 `view=result`。
- 按规约：Job 失败但页面诚实失败且非 5xx = **PASS**。wait_view 成功态未跑到（Job 在阶段 1 失败）；过程壳文案含「生成结束不会自动打开结果页」。
- Tempo Create 链路可见 `gkxlumen-topic-async-service-biz` → `/internal/v1/analysis-jobs/{taskId}/stages` → `/complete`（Java→Python `/internal/*`）。

### 5. US-CHAIN-SZ-03 负例

- 清 `localStorage['gkx-chain-sz-comparison-result']` 后打开 `?tab=development`。
- 「开始分析」**disabled**；页面拦截文案命中「请先完成并查看」/对比结果语义。
- Playwright `force` 点击后仍 **0** 条 `shenzhen_development` Create。页面拦截且未发请求 = **PASS**。

## 问题清单

- 无 FAIL。不写缺陷包、不派修。
- 残差（不挡闭环，不标 FAIL）：① 已发布登录走 mockLogin，网关 `/auth/login` 404；② key_link Job `freeze` 失败（诚实降级）；③ E0 已记 algo-py OTLP collector DNS / 部分库名无 `demo_` 前缀。

## 修改内容

- 无业务仓代码变更。仅本 handoff。

## 测试结果

- Playwright 对 http://10.50.69.111:30892 五条金路径 **ALL_PASS**。
- 登录页默认测试账号 → 登录成功。
- D12：本会话 API 无 demo-* host。
- 截图（本机临时目录，不入库）：`01-search` / `02-overview` / `03-panorama` / `04-diagnosis` / `05-shenzhen`。

## 遗留风险

1. 真 PigX `/auth/login` 未通，依赖已发布包内 mock 登录进 SPA；上线关 mock 前需补真登录。
2. `chain:diagnosis:key_link` Job 在 `freeze` 失败；若产品要成功态 wait_view 演示，需后续修单（本金路径允许诚实失败）。
3. 同 ns 仍有 demo 栈；后续复测必须继续钉 30892 / 30899 / `lumen-platform-algo-py`。

## CI/CD（必填）

- 分支：未改仓
- commit：无
- pipeline：未触发（QA 不改代码）
- 部署 namespace：`dev`（沿用 E0：`gkx-lumen-topic` 镜像 `gkx-lumen-topic:b0032e17`）
- K8s rollout：E0 已 PASS，本单未再滚
- dev 测试 URL：http://10.50.69.111:30892 ；网关 http://10.50.69.111:30899

## 可观测性（建议）

- OTEL_SERVICE_NAME：`gkxlumen-topic-chain-biz` / `gkxlumen-topic-async-service-biz` / `lumen-platform-algo-py`（后者 OTLP DNS 见 E0 残差）
- traceId（抽样）：见上表
- Tempo / Loki：Tempo API 200 有 batches（Create 抽样）；Grafana http://192.168.88.34:3000（**旧环境已废弃**；现网 Grafana：$newGf）

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | 通过。QA 未改 Java 算法 |
| 2 调用链 前端→Java REST→Python `/internal/*` | 通过。Create Tempo 可见 async-service → `/internal/v1/analysis-jobs/...` |
| 3 图谱 Nebula | N/A |
| 4 可观测 | 通过。响应头 `X-Trace-Id` / `traceparent`；Tempo 可查 |
| 5 CI/CD | N/A（本单不改代码、不推仓） |
| 6 demo2 merge | N/A |
| 7 共享聚合核心 | N/A |
| 8 数据策略 ADS | 通过。CHAIN 读面经 Java；health/E0 为 `demo_gkxlumenx_*` |
| 9 D8 Design | N/A（不改 UI） |
| 10 D9 血缘 | 通过。概况 KPI 走 ReviewMetricBadges；未为干净界面删 ⓘ |
| 11 D10 交互 | 通过。wait_view / 同类型锁 / 深圳负例拦截按已发布交互 |
| 12 D12 demo/lumen 隔离 | 通过。见结论 |

## cost 四字段（估）

| 字段 | 值 |
|------|-----|
| actual_tokens | 160000 |
| model_used | grok-4.6 |
| actual_cost | 0.86 |
| cost_warn | green |

口径：`budget-estimate.md` §8.2，B 档 in $3/M out $15/M，qa 默认 in/out=80/20。`source: estimate`（无 console 精确分拆）。未超 $5。

## 涉及文件

- `agent-delivery/agent-handoffs/产业链分析-CHAIN/LUMEN-CHAIN-E-QA-SMOKE-L01.md`（本文件）

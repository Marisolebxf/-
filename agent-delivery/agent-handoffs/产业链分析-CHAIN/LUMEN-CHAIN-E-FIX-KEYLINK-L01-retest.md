# LUMEN-CHAIN-E-FIX-KEYLINK-L01 · 段 E 第 2 轮复测（只测失败故事）

> 日期：2026-08-14  
> Task ID：`LUMEN-CHAIN-E-FIX-KEYLINK-L01`  
> 规约：[`长任务执行规约.md`](../../长任务执行规约.md) §11.3–11.4  
> 总控金路径 #4：[`DEMO-CHAIN-ABCD-长任务总控.md`](./DEMO-CHAIN-ABCD-长任务总控.md)  
> 修单 handoff：[`LUMEN-CHAIN-E-FIX-KEYLINK-L01.md`](./LUMEN-CHAIN-E-FIX-KEYLINK-L01.md)  
> 上一轮缺陷包：[`LUMEN-CHAIN-E-QA-SMOKE-L01-defect-US-CHAIN-DIAG-03.md`](./LUMEN-CHAIN-E-QA-SMOKE-L01-defect-US-CHAIN-DIAG-03.md)  
> 本单 **不改业务代码**；**未**重跑另外 4 条金路径；**未**动 E1 `LUMEN-CHAIN-E-QA-SMOKE-L01`。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:qa-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权不必再问。registry `pending_test→testing`（actor=`qa-agent`）。复测 PASS 后转 **ready_to_sign**，不标 done。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 期望未发生必红；未把 Job 失败收成 PASS；未扩成全量 USM；未用 localhost / pnpm dev。诚实 KPI 空且 Job succeeded 仍按总控 #4 判 PASS。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 已发布前端单故事复测，未挂载 compress。 |

## 结论（给 coordinator）

**PASS**（复测 PASS）。联调通过。

| 项 | 值 |
|----|----|
| 故事 | `US-CHAIN-DIAG-03` → `US-CHAIN-DIAG-04` |
| 已发布 URL | http://192.168.88.50:30892/industry-center/diagnosis?tab=key-link |
| 镜像 tag | `gkx-lumen-algo-py-api:4c6a6a53`（E0 coordinator kubectl 已确认 ready 1/1；commit `4c6a6a5313c8f8b27e3e7099f432210537407dfb`） |
| task_id | `CHAIN-20260814-015` |
| 终态 | **success**（Java/FE；约 6–7s；五阶段均「已完成」，含 freeze） |
| wait_view | **是。** succeeded 后 URL 仍 `view=processing`；点了「查看分析结果」才进 `view=result` |
| Create X-Trace-Id | `f2c457e460961b4ca16b2d660cd243a6` |
| detail X-Trace-Id | `0914864b69ccf4d2d25e0526b142f74f`（success 轮询） |
| result X-Trace-Id | `5793c2b8785e68be618e38e2583310b8` |
| D12 | **合规**。本会话 `/api/*` 仅 `192.168.88.50:30892`；demo-* host **0** |
| 缺陷包 | 无（本轮 PASS） |

## 复测步骤与证据

Playwright 1.62.1 Chromium headless，点 **K8s 已发布**前端（禁止 localhost）。登录页默认测试账号（已发布包 mockLogin）。对象：集成电路 / 集成电路设计。

1. 打开诊断 key-link → 登录成功。  
2. 点「开始分析」→ POST `/api/topicAsync/topic/v1/analysis/tasks` **200**，`analysisType=chain:diagnosis:key_link`，新任务非 reuse。  
3. 过程页 `view=processing&task_id=CHAIN-20260814-015`；轮询 GET detail **200**。  
4. 终态 `status=success`；`target_params.page_mode_hint=process_succeeded_wait_view` 且 `viewed=false`。  
5. 成功后停留约 4s：**未**自动进 `view=result`；按钮「查看分析结果」可见。  
6. 点击后 URL 变为 `view=result`。  

Create Tempo：[f2c457e460961b4ca16b2d660cd243a6](http://192.168.88.50:30201/api/traces/f2c457e460961b4ca16b2d660cd243a6)（API 200，body 有 batches）。  
detail Tempo：[0914864b69ccf4d2d25e0526b142f74f](http://192.168.88.50:30201/api/traces/0914864b69ccf4d2d25e0526b142f74f)（API 200）。  
Grafana Explore：http://192.168.88.34:3000（**旧环境已废弃**；现网 Grafana：$newGf） 数据源 Tempo。

### PASS 门（规约 §11.3，须同时）

| 门 | 结果 |
|----|------|
| status=success/succeeded | ✅ `success` |
| 成功后 URL 仍 wait_view（`view=processing`） | ✅ |
| 点「查看分析结果」才进结果 | ✅ 已点击 |
| 非 5xx | ✅ Create/detail/result 均为 200 |
| 未自动跳过 wait_view | ✅ |
| freeze 未 failed | ✅ 过程壳五阶段均「已完成」 |

### 诚实空态（不挡本条）

Job **succeeded** 后结果页：关键环节数 `0`；市场规模「暂无正式数据源」；投融资「数据筹备中」；五环节「高端化 —」。按派单第 6 条：**本条仍 PASS**（后续节点诚实，不是 freeze 挡死）。总控该行允许的空态列仍为「无」——此处不是把 Job failed 收成空态。

## 问题清单

- 无 FAIL。不写缺陷包、不派修。  
- 未改 E1 状态。未重跑金路径 #1/#2/#3/#5。

## 修改内容

- 无业务仓代码变更。仅本复测记录。

## 测试结果

- **PASS**。`CHAIN-20260814-015` 终态 success；wait_view 点击完成。  
- 登录：已发布 mockLogin 成功。  
- D12：无 demo-* host。

## 遗留风险

1. 真 PigX `/auth/login` 仍 404（不挡本金路径；总控未把真登录写入期望）。  
2. 结果页 KPI 诚实空 / 关键环节数 0：后续数据节点，不挡本条 succeeded+wait_view。  
3. algo-py OTLP collector DNS 残差仍可能使 Python span 缺失（Create 链路 Tempo 有 Java batches）。

## CI/CD（必填）

- 分支：未改仓  
- commit：无（QA 不改代码）  
- pipeline：未触发  
- 部署 namespace：`dev`  
- 镜像 tag：`gkx-lumen-algo-py-api:4c6a6a53`（E0 已滚）  
- K8s rollout：E0 已确认 ready 1/1；本单未再滚  
- dev 测试 URL：http://192.168.88.50:30892  

## 可观测性（建议）

- OTEL_SERVICE_NAME：`gkxlumen-topic-async-service-biz` / `lumen-platform-algo-py`  
- traceId：Create `f2c457e460961b4ca16b2d660cd243a6`；detail `0914864b69ccf4d2d25e0526b142f74f`  
- Tempo / Loki：Tempo API 200 有 batches  

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | 通过。QA 未改代码 |
| 2 调用链 前端→Java REST→Python `/internal/*` | 通过。Create 走已发布 `/api/topicAsync/...` |
| 3 图谱 Nebula | N/A |
| 4 可观测 | 通过。`X-Trace-Id`；Tempo 可查 |
| 5 CI/CD | N/A（本单不改代码） |
| 6 demo2 merge | N/A |
| 8 数据策略 | 通过。诚实空 KPI，未造假市场/投融资 |
| 12 D12 demo/lumen 隔离 | 通过。无 demo-* host |

## cost 四字段（估）

| 字段 | 值 |
|------|-----|
| actual_tokens | 110000 |
| model_used | grok-4.6 |
| actual_cost | 0.59 |
| cost_warn | green |

口径：`budget-estimate.md` §8.2，B 档 in $3/M out $15/M，qa 默认 in/out=80/20。`source: estimate`。公式：`110000 × (0.8×3 + 0.2×15) / 1e6 = 0.59`。未超 $5。

## 涉及文件

- `agent-delivery/agent-handoffs/产业链分析-CHAIN/LUMEN-CHAIN-E-FIX-KEYLINK-L01-retest.md`（本文件）

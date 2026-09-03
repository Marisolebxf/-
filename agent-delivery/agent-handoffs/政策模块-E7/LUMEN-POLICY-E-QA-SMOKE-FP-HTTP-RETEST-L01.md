# LUMEN-POLICY-E-QA-SMOKE-FP-HTTP-RETEST-L01 · 政策专题 E1 — HTTP 指纹发布后金路径复测

> 格式参考 `templates/handoff-template.md`。对 K8s 已发布 `lumen-ui-topic` 手跑。本单 **不改业务代码**。  
> 总控：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md) §4  
> 派单包：[`LUMEN-POLICY-E-QA-SMOKE-FP-HTTP-RETEST-L01-派单包.md`](./LUMEN-POLICY-E-QA-SMOKE-FP-HTTP-RETEST-L01-派单包.md)  
> 上一轮 FAIL（仅背景，不当本轮结论）：[`LUMEN-POLICY-E-QA-SMOKE-L0VID-RETEST-L01.md`](./LUMEN-POLICY-E-QA-SMOKE-L0VID-RETEST-L01.md)  
> C1 修：[`LUMEN-POLICY-E-C1-FE-FP-HTTP-L01.md`](./LUMEN-POLICY-E-C1-FE-FP-HTTP-L01.md) `7cd3be4`  
> E0：[`LUMEN-POLICY-E-DEVOPS-FE-FP-HTTP-L01.md`](./LUMEN-POLICY-E-DEVOPS-FE-FP-HTTP-L01.md) `gkx-lumen-topic:7cd3be47`

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:qa-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h。tech_task。五条全 PASS → `ready_to_sign`。不要自行 done。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 删验收条。三门先核再手跑 §4 五条；#3～#5 只从 UI 点「开始分析」进过程页再 wait_view；禁止代理 POST 改判 PASS；未拿明文 analysis_fp 当结论；未把 e2e:chain-gold 当政策结论。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 已发布冒烟，未挂载 compress。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | 无。本叶只测已发布调用链，不改图。 |
| 会签态 | `approved`（本叶不翻签） |

## 结论（给 coordinator）

**联调通过**。总控 §4 五条全 **PASS**。上一轮 C1（HTTP 源 `crypto.subtle` 缺失导致点「开始分析」抛错）**本轮已闭合**：`isSecureContext=false` / `crypto.subtle` 仍缺失，但 UI 点开始分析发出 SHA-256 64 位 `analysis_fp`，进 `view=processing`，Job `status=success` 后 wait_view 点「查看分析结果」。**不要**再派「subtle 缺失」或 L0 滤空。

- 证据源：http://192.168.88.50:30892 （禁止 localhost）
- Playwright：Chromium / `@playwright/test` 1.51，headless，只点已发布前端；**未**用 30892 代理 POST 改判 PASS
- CI：`e2e:policy-gold` 未绿，本叶手跑。未把 `e2e:chain-gold` 当政策结论
- 门：前端 **`gkx-lumen-topic:7cd3be47`**；innov **`gkxlumen-innov:300ad303`**；clusters GET **200** 非 500
- UI Create：#3 `POLICY-20260902-007` / #4 `POLICY-20260902-008` / #5 `POLICY-20260902-009` 均为 `reused=false`、`status=success`
- D12：`/api/*` 均打 `192.168.88.50:30892`；无 demo-* host
- 金路径未红，状态 `ready_to_sign`。INB4 短码 Java 业务拒见残差包 [`LUMEN-POLICY-E-QA-SMOKE-FP-HTTP-RETEST-L01-defect-pack.md`](./LUMEN-POLICY-E-QA-SMOKE-FP-HTTP-RETEST-L01-defect-pack.md)（**不改本叶判定、不改 Java、不要打回 integration**）

## 门核

| 门 | 期望 | 实际 | 判定 |
|----|------|------|------|
| 前端镜像 | 含 `7cd3be4` | `gkx-lumen-topic:7cd3be47` READY 1/1，pod `gkx-lumen-topic-58c6445-5zkxx` @ htsvr078 | **PASS** |
| innov | `gkxlumen-innov:300ad303` | `gkxlumen-platform-innov` 镜像 `gkxlumen-innov:300ad303` READY 1/1；`INNOV_DIM_SCHEMA=demo_gkxlumenx_dim` | **PASS** |
| clusters GET | 非 500 | 30892 `/api/topic/v1/meta/industry-clusters?include_l0=true` **200** `code=0` items=15，含 `INB1303`。探活 Trace `f12126abcd8f50b1edf8d86b14611e2b`；页内 `#2` `55b48ab2d58dee8a5d31d1cf908ca8eb` | **PASS** |

30892 `/` HTTP **200**，`Last-Modified: Wed, 02 Sep 2026 09:53:48 GMT`。政策门面未重滚：`gkxlumen-topic-policy:868987d6` · async `868987d6` · 政策 Python `gkxlumen-entan-py-api:ea3acc39`。

## 五条金路径

| # | 故事 | 路由 | 判定 | 实际现象 | HTTP / 页面态 | X-Trace-Id |
|---|------|------|------|----------|---------------|------------|
| 1 | `US-E7-POL-01c` | `/policy/search` | **PASS** | 搜「半导体」出卡 6 张（total 47051）；无「加入对比篮」「深度分析」 | GET search **200** | `ea86d1b3ca82f488f4551d4acda15bb8` |
| 2 | `US-E7-POL-01`+`05` | `/policy/overview` 页内集群→L0 | **PASS** | 空配置开始分析 disabled，force click **未** POST。选「新一代信息技术」→「集成电路」（L0=`INB1303` 能选）。hint 空；VID「INB1303（industry_id 原样提交）」；footer 校验通过；开始分析 **enabled**。不强制篮。顺手 Create：`industry_id=INB1303`、无 `industry_vid`、**未**伪造 `chain:INB1303`；fp 64 位 SHA-256 | GET clusters **200**；Create HTTP **200** `code=1` `INDUSTRY_VID_INVALID`（不挡 #2 选簇） | clusters **`55b48ab2d58dee8a5d31d1cf908ca8eb`**；Create `2edc10cd9e69edfd9a1276df51fd3730` |
| 3 | `US-E7-POL-02`+`06` | `/policy/overview` | **PASS** | URL `object_ids[]=INB170101` 预填 `chain:INB170101`，开始分析 enabled。I2-12 切季/年 Create 计数 0。UI 点开始分析 → `view=processing`（task `POLICY-20260902-007`）→ Job success → wait_view 点查看结果。`crypto.subtle` 缺失但 **无** digest TypeError | Create HTTP **200** `ok=true` `status=success` | **`7419f4a39a44ee9f7cc260aaf99d6257`** |
| 4 | `US-E7-POL-03` | `/policy/analysis` | **PASS** | 同 #3 VID 预填；UI 点开始分析进过程页；`POLICY-20260902-008` success 后 wait_view 出结果页 | Create **200** success | **`0add7834e15372c12aa2c868b706e776`** |
| 5 | `US-E7-POL-04` | `/policy/recommendation` | **PASS** | `object_ids[]=chain:INB170101`；一级权重 100%；UI 点开始分析进过程页；`POLICY-20260902-009` success 后 wait_view | Create **200** success | **`a198768e15a5279eccc86e9f902852c1`** |

Tempo（#1 search）：http://192.168.88.50:30201/api/traces/ea86d1b3ca82f488f4551d4acda15bb8  
Tempo（#2 clusters）：http://192.168.88.50:30201/api/traces/55b48ab2d58dee8a5d31d1cf908ca8eb  
Tempo（#2 INB4 Create）：http://192.168.88.50:30201/api/traces/2edc10cd9e69edfd9a1276df51fd3730  
Tempo（#3 Create）：http://192.168.88.50:30201/api/traces/7419f4a39a44ee9f7cc260aaf99d6257  
Tempo（#4 Create）：http://192.168.88.50:30201/api/traces/0add7834e15372c12aa2c868b706e776  
Tempo（#5 Create）：http://192.168.88.50:30201/api/traces/a198768e15a5279eccc86e9f902852c1  
Grafana Explore：http://192.168.88.34:3000 数据源 Tempo。

### 1. US-E7-POL-01c

- 打开 `/policy/search`，智能检索「半导体」。
- GET search **200**，`items=6` `total=47051`，非 5xx。
- 结果区无「加入对比篮」「深度分析」。

### 2. US-E7-POL-01 / 05（页内集群→L0，不强制篮）

- 空配置：「开始分析」disabled；空点 force click **未** POST Create。
- 集群 15 项可选。`新一代信息技术` → L0 5 项：集成电路 / 传感器 / 人工智能 / 智能终端 / 软件与信息服务（`INB1303` 能选）。
- 选后开始分析 enabled。L0 滤空 **保持闭合**。
- 顺手核短码提交：FE POST `industry_id=INB1303`、`industry_vid` 空、fp=`469986a50778288d7623203f5732d7c4ca2448f9f9e22eb7f0f9f7470ee010f1`（`/^[a-f0-9]{64}$/`）。Java HTTP 200、业务 `code=1` `INDUSTRY_VID_INVALID`，URL 仍配置态。按派单：**不改 Java**；#2 金路径是选簇不是 wait_view，故仍 PASS。VID 预填路径 #3～#5 已跑完。

### 3–5. Create / wait_view（必须从 UI 点开始分析）

- 探针：`protocol=http:`，`isSecureContext=false`，`crypto.subtle` 缺失。pageerror **无** `digest` TypeError。
- VID 预填 `object_ids[]=INB170101` / `chain:INB170101`：`scopeReady` 为真，开始分析可点。
- I2-12：切粒度 **未**自动 POST。
- 从 UI 点「开始分析」：toast「任务已创建，正在展示分析过程」；URL 含 `view=processing` + `task_id`；Create body `analysis_fp` 均为 64 位小写 SHA-256（非明文闸）。
- Job `status=success`（同步秒回）后过程页出现「查看分析结果」，点击进入 `view=result`。**禁止**用代理 POST 补判；本轮 UI Create 均由按钮发出。
- 明文 `analysis_fp` 闸 **未出现**，不得当本轮结论。

## I2-12

| 条 | 结果 |
|----|------|
| 切条件不自动起任务 | **观察到**：#3 切季/年 Create 计数 0 |
| 条件栏「开始分析」 | **有**且 VID/L0 后 enabled；点后进 processing |
| 同用户同条件一条在跑 | 本轮三次 Create `reused=false`，各分析类型各一条成功（时序/区域/深圳） |
| 当天已成功直接打开结果 | 本轮三次均为新任务秒成功，wait_view 后点查看结果 |
| 「重新分析」force | 本轮未点「重新分析」（新任务已通，不挡） |

## 问题清单

- 无挡金路径项。上一轮 C1 FE 指纹 **已闭合**。不要再派 subtle / L0 滤空。
- 残差（不挡本叶）：页内选 INB4 后 Java 以 `INDUSTRY_VID_INVALID` 拒短码 `industry_id=INB1303`（HTTP 200 / `code=1`，**不是** 4xx）。FE 未伪造 `chain:INB1303`。QA **不改 Java**。coordinator 若要修短码挂接，另开 C 段，Trace `2edc10cd9e69edfd9a1276df51fd3730`。**不要标 C5**。
- `?industry=INB170101` 仍不预填（解析只认 `object_ids[]`）；有效 VID 路径本轮已覆盖。
- Job `result_payload.results=[]` / `shards=0`：#4 允许结果空态；#3/#5 任务已 succeeded 并打开结果页。不是 Job failed。
- `e2e:policy-gold` 仍未绿（手跑本叶）。

## 修改内容

- 无业务仓代码变更。仅本 handoff + evidence 手跑脚本。

## 测试结果

- Playwright 对 http://192.168.88.50:30892：**5 passed**（1.5m）。`results.json` `unexpected=0`。
- 探针：HTTP 非安全上下文 `crypto.subtle` 缺失；回退 SHA-256 生效；click 进 processing。
- 手跑记录：`evidence/LUMEN-POLICY-E-QA-SMOKE-FP-HTTP-RETEST-L01/run-notes.json` · `policy-gold.spec.ts` · `crypto-subtle-probe.json` · `shots/`

## 遗留风险

1. 页内短码 `INB1303` 提交会被 Java `INDUSTRY_VID_INVALID` 拒；金路径 #3～#5 走图上 VID `chain:INB170101` 已通。若产品要求页内 L0 短码也能起任务，另开 Java 叶（不挡本叶签收）。
2. 同步 Job 结果集为空（`results=[]`）；#4 允许空态+角标。数据丰度不在本叶金路径内。
3. `e2e:policy-gold` CI 仍未绿；本叶是手跑已发布 URL。

## CI/CD（必填）

- 分支：未改业务仓
- commit：orchestration 本叶 handoff（见 git；QA 不改业务代码）
- pipeline：未触发业务仓 CI
- 部署 namespace：`dev`；镜像 `gkx-lumen-topic:7cd3be47` · `gkxlumen-innov:300ad303` · `gkxlumen-topic-policy:868987d6` · `gkxlumen-topic-async-service:868987d6` · 政策 Python `gkxlumen-entan-py-api:ea3acc39`
- K8s rollout：本单未再滚；沿用 E0 `7cd3be47`
- dev 测试 URL：http://192.168.88.50:30892

## 可观测性（建议）

- OTEL_SERVICE_NAME：`gkxlumen-innov` / `gkxlumen-gateway` / `gkxlumen-topic-policy-biz`
- traceId：search `ea86d1b3ca82f488f4551d4acda15bb8`；clusters `55b48ab2d58dee8a5d31d1cf908ca8eb`；#3 Create **`7419f4a39a44ee9f7cc260aaf99d6257`**；#4 `0add7834e15372c12aa2c868b706e776`；#5 `a198768e15a5279eccc86e9f902852c1`；INB4 Create `2edc10cd9e69edfd9a1276df51fd3730`
- Tempo / Loki：Tempo API 可取到 #2/#3 Create trace（响应体非空）。
- 前端 console：无 `crypto.subtle` / `digest` TypeError。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | 通过。QA 未改算法 |
| 2 调用链 前端→Java REST→Python `/internal/*` | 通过。UI Create 经 30892 `/api` → Java；#3～#5 Job success |
| 3 图谱 Nebula | 通过。未直连 nGQL；VID 用 `chain:INB170101` |
| 4 可观测 | 通过。Create / clusters / search 均有 `X-Trace-Id` |
| 5 CI/CD | N/A（本单不改业务仓） |
| 6 demo2 merge | N/A |
| 7 共享聚合核心 | N/A |
| 8 数据策略 ADS `demo_gkxlumenx_*` | 通过。innov `INNOV_DIM_SCHEMA=demo_gkxlumenx_dim`；本叶未改 JDBC |
| 9 D8 Design | N/A 本叶无 UI 改动 |
| 10 D9 8 件套 | N/A |
| 11 D10 交互 | 通过。开始分析才 Create；切条件不自动起任务 |
| 12 D12 lumen 不调 demo **服务** | 通过。无 demo-* host |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 100000 |
| model_used | grok-4.6 |
| actual_cost | 0.66 |
| cost_warn | green |
| 说明 | 会话估算 in+out；source: session estimate。未改业务代码 |

## 给 coordinator

**联调通过**（tech_task）。请 MCP 本叶 → `ready_to_sign`（本 agent 将自行推状态）。**不要 done**。不要再派 FE 指纹 / L0 滤空。INB4 短码 Java `INDUSTRY_VID_INVALID` 不挡金路径，若要修另开 C 段。

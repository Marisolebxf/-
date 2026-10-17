# LUMEN-POLICY-E-QA-SMOKE-CLUSTERS-RETEST-L01 · 政策专题 E1 — innov DIM 后金路径复测

> 格式参考 `templates/handoff-template.md`。对 K8s 已发布 `lumen-ui-topic` 手跑。本单 **不改业务代码**。  
> 总控：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md) §4  
> 缺陷包：[`LUMEN-POLICY-E-QA-SMOKE-CLUSTERS-RETEST-L01-defect-pack.md`](./LUMEN-POLICY-E-QA-SMOKE-CLUSTERS-RETEST-L01-defect-pack.md)  
> 上一轮 FAIL：[`LUMEN-POLICY-E-QA-SMOKE-C1RETEST-L01.md`](./LUMEN-POLICY-E-QA-SMOKE-C1RETEST-L01.md)（clusters 500）。E0：[`LUMEN-POLICY-E-DEVOPS-INNOV-DIM-L01.md`](./LUMEN-POLICY-E-DEVOPS-INNOV-DIM-L01.md)

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:qa-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h。tech_task。FAIL → integration + 缺陷包。不要自行 done。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 删验收条。五条均在已发布 30892 手跑；clusters 非 500 已核；Create 本轮实发 POST；未拿明文 analysis_fp 当结论；Job 未从 UI 进 wait_view 不改判 PASS。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 已发布冒烟，未挂载 compress。 |

## 结论（给 coordinator）

**FAIL**（1 PASS / 4 FAIL）。**不要**写「联调通过」。请按缺陷包派 **C1 frontend**（页内 L0 全是 `INB`+4 位短码，被 `toPolicyGraphVid`/`requireGraphVid` 滤空）。**不是 C5**（clusters 已 200）。

- 证据源：http://192.168.88.50:30892 （禁止 localhost）
- Playwright：Chromium / `@playwright/test` 1.51，headless，只点已发布前端。**#1 PASS，#2～#5 FAIL**
- CI：`e2e:policy-gold` 未绿，本叶手跑。未把 `e2e:chain-gold` 当政策结论
- 门：clusters **HTTP 200** 非 500，15 条，`mapped=9`；innov **`gkxlumen-innov:300ad303`** + `INNOV_DIM_SCHEMA=demo_gkxlumenx_dim`；前端现网 **`gkx-lumen-topic:c4758206`**（门要 `006d186d`，记 **次要 C2**，不改变 #2 滤空结论——`006d186d` 同源 `INB\\d{6,}` 规则）
- 健康体：`GET http://192.168.88.50:30899/policy/topic/v1/policy/health` **200**，`degraded=false`，`python.pathPrefix=/internal/policy`。Trace `63f916ff3fd9e7b7a473896e438605b5`
- **Create 本轮已发出**（QA 在 UI 按钮 disabled 后经 30892 代理 POST）。三项 `analysis_fp` 均为 64 位小写 SHA-256；Java **code=0**；**未**出现 `analysis_fp 必须是 64 位小写 SHA-256`
- D12：`/api/*` 均打 `192.168.88.50:30892` / `30899`；无 demo-* host
- 缺陷包：`agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-E-QA-SMOKE-CLUSTERS-RETEST-L01-defect-pack.md`

## 门核

| 门 | 期望 | 实际 | 判定 |
|----|------|------|------|
| clusters GET | 非 500 | 30892 `/api/topic/v1/meta/industry-clusters?include_l0=true` **200**，`code=0`，items=15。Trace `2d1736556975b954204e0af9fe2920fc` / 页内 `a15b911860aa8089b8ea3b3fe6f44506` | **PASS** |
| innov 镜像 | `300ad303` | `gkxlumen-innov:300ad303` READY 1/1；`INNOV_DIM_SCHEMA=demo_gkxlumenx_dim` | **PASS** |
| 前端镜像 | `006d186d` | `gkx-lumen-topic:c4758206` READY 1/1（pod 2026-09-02T08:17:16Z） | **FAIL 次要 C2** |

## 五条金路径

| # | 故事 | 路由 | 判定 | 实际现象 | HTTP / 页面态 | X-Trace-Id |
|---|------|------|------|----------|---------------|------------|
| 1 | `US-E7-POL-01c` | `/policy/search` | **PASS** | 搜「半导体」出卡 6 张（total 47051）；无「加入对比篮」「深度分析」 | GET search **200** | `ee9ff04fa3664920fd02b6490f1bf062` |
| 2 | `US-E7-POL-01`+`05` | `/policy/overview` 页内集群→L0 | **FAIL C1 FE** | clusters **200**，L0 **全部** `INB`+4 位（`INB1303` 等）。产业下拉无图上 VID；开始分析 disabled；hint「尚未选择分析对象」。VID 文案「未形成 chain:INB…」 | GET clusters **200** | **`a15b911860aa8089b8ea3b3fe6f44506`** |
| 3 | `US-E7-POL-02`+`06` | `/policy/overview` | **FAIL C1 FE** | URL `INB170101` 时 **图上 VID：chain:INB170101 可见**；hint 仍「尚未选择分析对象」（`clusterId` 空）。开始分析 **disabled**，UI **未** POST。QA 补 POST → **200 code=0** SHA-256，task `POLICY-20260902-004` 随后 GET **success**。UI 未进过程页 / wait_view → 按总控 **红** | UI 无 Create；补 POST 200 | UI 无；补发 **`e0c6f9aa9a9df91e5dd195dedbc7221d`** |
| 4 | `US-E7-POL-03` | `/policy/analysis` | **FAIL C1 FE** | 同 #3。补 POST `POLICY-20260902-005` success。未出矩阵/雷达 wait_view | 同 #3 | 补发 **`b05b4efb33c2b2cfa3832a2adef4c87c`** |
| 5 | `US-E7-POL-04` | `/policy/recommendation` | **FAIL C1 FE** | 一级权重 100% 绿条可见；三维「该维核心指标 Java 实包为空」；开始分析仍 disabled。补 POST `POLICY-20260902-006` success。任务未从 UI 跑通 | 同 #3 | 补发 **`ad303f354dad83fa8990ded7ee999e22`** |

Tempo（clusters 200）：http://192.168.88.50:30201/api/traces/a15b911860aa8089b8ea3b3fe6f44506  
Tempo（#3 Create）：http://192.168.88.50:30201/api/traces/e0c6f9aa9a9df91e5dd195dedbc7221d  
Grafana Explore：http://192.168.88.34:3000（**旧环境已废弃**；现网 Grafana：$newGf） 数据源 Tempo，粘贴上表 id。

### 1. US-E7-POL-01c

- 打开 `/policy/search`，智能检索「半导体」。
- GET search **200**，`items=6` `total=47051`，非 5xx。
- 结果区无「加入对比篮」「深度分析」。

### 2. US-E7-POL-01 / 05（页内集群→L0，不强制篮）

- 空配置：「开始分析」disabled，「尚未选择分析对象」；无「去产业查询」主按钮；空点 force click **未** POST Create。
- 时序三维默认全开（发布时间 / 效力层级 / 支持力度）。
- `GET /api/topic/v1/meta/industry-clusters?include_l0=true` **200**。L0 例：`CL-SEI-01` → `INB1303,INB1323,INB1309,INB1333,INB1306`（全 `INB\\d{4}`）。
- 前端 `toPolicyGraphVid` 只认 `chain:` / `INB\\d{6,}`；`IndustryClusterSelect require-graph-vid` + `clusterL0Options` 把短码滤空。产业控件 `arco-select-view-disabled`。
- **不是 C5**（表已可读）。**不是**篮路径。

### 3–5. Create / wait_view

- URL `object_ids[]=INB170101`：**图上 VID 已显示**，`scopeReady` 仍要 `clusterId`，开始分析 disabled。I2-12：切条件 **未**自动 POST。
- UI Create **0 次**。QA 经同源 30892 代理 POST `/api/topicAsync/topic/v1/analysis/tasks`，`analysis_fp` = SHA-256，**明文闸本轮未出现**。
- Java 收单 success：`POLICY-20260902-004` timeseries / `-005` regional / `-006` shenzhen。**不能**因此改判 PASS：总控要求点「开始分析」→ 过程页 → succeeded 后点查看结果。

## I2-12

| 条 | 结果 |
|----|------|
| 切条件不自动起任务 | **观察到**：改「年」后 Create 计数 0 |
| 条件栏「开始分析」 | **有**按钮；本轮 disabled |
| 同用户同条件一条在跑 | **未从 UI 验到**（按钮未点亮） |
| 当天已成功直接打开结果 | **未从 UI 验到** |
| 「重新分析」force | **未从 UI 验到** |

## 问题清单

- 主 **C1 FE**：clusters 已 200，但 L0 全是 `INB`+4 位短码，被 `requireGraphVid` 滤空；URL 已形成 `chain:INB170101` 仍因无 `clusterId` 不可提交。
- 次要 **C2**：前端镜像 `c4758206` ≠ 门 `006d186d`（helm:chart 窗口滚动）。同源 VID 规则，单滚回 `006d186d` **不够**修 #2。
- SHA-256 Create 闸 **本轮已跑到且 Java 接受**；不得再用旧结论「明文 analysis_fp」。
- 残差：登录仍 mockLogin。`e2e:policy-gold` 仍未绿。

## 修改内容

- 无业务仓代码变更。仅本 handoff + 缺陷包 + evidence 手跑脚本。

## 测试结果

- Playwright 对 http://192.168.88.50:30892：**#1 PASS，#2–#5 FAIL**。
- 健康体 30899 policy health 200。
- 手跑记录：`evidence/LUMEN-POLICY-E-QA-SMOKE-CLUSTERS-RETEST-L01/run-notes.json` · `policy-gold.spec.ts`

## 遗留风险

1. FE 修好 L0/clusterId 后，UI Create 才进 wait_view；API success ≠ 金路径绿。
2. 深圳三维 Java 指标实包仍空；`indicatorOk` 在空 catalog 下为真，不挡提交，但结果可能空。
3. `e2e:policy-gold` CI 仍未绿；复测继续手跑 30892。

## CI/CD（必填）

- 分支：未改业务仓
- commit：orchestration 本叶 handoff（见 git）
- pipeline：未触发业务仓 CI（QA 不改代码）
- 部署 namespace：`dev`；镜像 `gkx-lumen-topic:c4758206` · `gkxlumen-innov:300ad303` · `gkxlumen-topic-policy:7d12b8dd` · `gkxlumen-topic-async-service:7d12b8dd`
- K8s rollout：本单未再滚；沿用 E0 innov DIM
- dev 测试 URL：http://192.168.88.50:30892 ；网关 http://192.168.88.50:30899

## 可观测性（建议）

- OTEL_SERVICE_NAME：`gkxlumen-innov` / `gkxlumen-gateway` / `gkxlumen-topic-async-service-biz`
- traceId：search `ee9ff04fa3664920fd02b6490f1bf062`；clusters **`a15b911860aa8089b8ea3b3fe6f44506`**；Create `#3 e0c6f9aa9a9df91e5dd195dedbc7221d` `#4 b05b4efb33c2b2cfa3832a2adef4c87c` `#5 ad303f354dad83fa8990ded7ee999e22`
- Tempo / Loki：Tempo API 200

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | 通过。QA 未改算法 |
| 2 调用链 前端→Java REST→Python `/internal/*` | 通过。health python `/internal/policy`；补发 Create 打 Java async |
| 3 图谱 Nebula | 通过。VID 规则仍要 `chain:INB…`，未直连 nGQL |
| 4 可观测 | 通过。`X-Trace-Id` / Tempo |
| 5 CI/CD | N/A（本单不改业务仓） |
| 6 demo2 merge | N/A |
| 7 共享聚合核心 | N/A |
| 8 数据策略 ADS | 通过。clusters 读 `demo_gkxlumenx_dim` 已 200 |
| 9 D8 Design | N/A（不改 UI） |
| 10 D9 血缘 | N/A；#5 QPOL-02 角标在评审块 |
| 11 D10 交互 | 部分：wait_view 因 UI 未 Create 未跑到 |
| 12 D12 demo/lumen 隔离 | 通过。只认 30892 / 30899，无 demo-* 服务 |

## cost 四字段（估）

| 字段 | 值 |
|------|-----|
| actual_tokens | 420000 |
| model_used | grok-4.6 |
| actual_cost | 2.27 |
| cost_warn | green |

口径：`budget-estimate.md` §8.2，B 档 in $3/M out $15/M，qa 默认 in/out=80/20。`source: estimate`。未超 $5。

## 涉及文件

- `agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-E-QA-SMOKE-CLUSTERS-RETEST-L01.md`（本文件）
- `agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-E-QA-SMOKE-CLUSTERS-RETEST-L01-defect-pack.md`
- `agent-delivery/agent-handoffs/政策模块-E7/evidence/LUMEN-POLICY-E-QA-SMOKE-CLUSTERS-RETEST-L01/`（spec + run-notes + clusters.json）

# LUMEN-POLICY-E-QA-SMOKE-L0VID-RETEST-L01 · 政策专题 E1 — L0VID 发布后金路径复测

> 格式参考 `templates/handoff-template.md`。对 K8s 已发布 `lumen-ui-topic` 手跑。本单 **不改业务代码**。  
> 总控：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md) §4  
> 派单包：[`LUMEN-POLICY-E-QA-SMOKE-L0VID-RETEST-L01-派单包.md`](./LUMEN-POLICY-E-QA-SMOKE-L0VID-RETEST-L01-派单包.md)  
> 缺陷包：[`LUMEN-POLICY-E-QA-SMOKE-L0VID-RETEST-L01-defect-pack.md`](./LUMEN-POLICY-E-QA-SMOKE-L0VID-RETEST-L01-defect-pack.md)  
> 上一轮 FAIL（仅背景）：[`LUMEN-POLICY-E-QA-SMOKE-CLUSTERS-RETEST-L01.md`](./LUMEN-POLICY-E-QA-SMOKE-CLUSTERS-RETEST-L01.md)  
> C1 修：[`LUMEN-POLICY-E-C1-FE-L0VID-L01.md`](./LUMEN-POLICY-E-C1-FE-L0VID-L01.md) `1ce03cc`  
> E0：[`LUMEN-POLICY-E-DEVOPS-FE-L0VID-L01.md`](./LUMEN-POLICY-E-DEVOPS-FE-L0VID-L01.md) `gkx-lumen-topic:1ce03cc4`

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
| 说明 | 未用 YAGNI 删验收条。三门先核再手跑 §4 五条；#3～#5 只从 UI 点「开始分析」；禁止代理 POST 改判 PASS；未拿明文 analysis_fp 当结论；未把 e2e:chain-gold 当政策结论。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 已发布冒烟，未挂载 compress。 |

## 结论（给 coordinator）

**FAIL**（2 PASS / 3 FAIL）。**不要**写「联调通过」。请按缺陷包派 **C1 frontend**（`createAnalysisFingerprint` 在 `http://192.168.88.50:30892` 非安全上下文调用 `crypto.subtle.digest`，点「开始分析」抛 TypeError，无 Create、无过程页）。**不是 C5**。**不是**上一轮 L0 滤空（本轮 #2 已能选 INB4）。

- 证据源：http://192.168.88.50:30892 （禁止 localhost）
- Playwright：Chromium / `@playwright/test` 1.51，headless，只点已发布前端
- CI：`e2e:policy-gold` 未绿，本叶手跑。未把 `e2e:chain-gold` 当政策结论
- 门：前端 **`gkx-lumen-topic:1ce03cc4`**；innov **`gkxlumen-innov:300ad303`**；clusters GET **200** 非 500
- **未**用 30892 代理 POST 改判 PASS。UI Create **0 次**
- D12：`/api/*` 均打 `192.168.88.50:30892` / `30899`；无 demo-* host
- 缺陷包：`agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-E-QA-SMOKE-L0VID-RETEST-L01-defect-pack.md`

## 门核

| 门 | 期望 | 实际 | 判定 |
|----|------|------|------|
| 前端镜像 | 含 `1ce03cc` | `gkx-lumen-topic:1ce03cc4` READY 1/1，pod `gkx-lumen-topic-594f54559b-5nz85` | **PASS** |
| innov | `gkxlumen-innov:300ad303` | `gkxlumen-platform-innov` 镜像 `gkxlumen-innov:300ad303`；`INNOV_DIM_SCHEMA=demo_gkxlumenx_dim` | **PASS** |
| clusters GET | 非 500 | 30892 `/api/topic/v1/meta/industry-clusters?include_l0=true` **200** `code=0` items=15，含 `INB1303`。探活 Trace `d73a04710224ea0d68e2d92b2ed513c7`；页内 `#2` `2806c27e8fc030c5d159c875f922b73a` | **PASS** |

健康体：`GET http://192.168.88.50:30899/policy/topic/v1/policy/health` **200**，`degraded=false`，`python.pathPrefix=/internal/policy`。Trace `86aa1c93dfe8aa8679f8f781105fe96f`。

## 五条金路径

| # | 故事 | 路由 | 判定 | 实际现象 | HTTP / 页面态 | X-Trace-Id |
|---|------|------|------|----------|---------------|------------|
| 1 | `US-E7-POL-01c` | `/policy/search` | **PASS** | 搜「半导体」出卡 6 张（total 47051）；无「加入对比篮」「深度分析」 | GET search **200** | `cdb77d06d63b18a4f2a80ab5770654c2` |
| 2 | `US-E7-POL-01`+`05` | `/policy/overview` 页内集群→L0 | **PASS** | 空配置开始分析 disabled，force click **未** POST。选「新一代信息技术」→「集成电路」（API L0=`INB1303` 可出现）。hint 空；VID「INB1303（industry_id 原样提交）」；footer 校验通过；开始分析 **enabled**。不强制篮。 | GET clusters **200** | **`2806c27e8fc030c5d159c875f922b73a`** |
| 3 | `US-E7-POL-02`+`06` | `/policy/overview` | **FAIL C1 FE** | URL `object_ids[]=INB170101`：图上 VID `chain:INB170101`，cluster 空，开始分析 **enabled**。I2-12 切「季/年」Create 计数 0。点「开始分析」**未**进 `view=processing`，**无** POST。`?industry=INB170101` 单独不预填（解析只认 `object_ids[]`）。 | 配置页；UI Create 0 | 无 Create；页内 clusters 见 #2；console TypeError |
| 4 | `US-E7-POL-03` | `/policy/analysis` | **FAIL C1 FE** | 同 #3 VID 预填可点开始分析；点后未进过程页 / wait_view | 同 #3 | 无 Create |
| 5 | `US-E7-POL-04` | `/policy/recommendation` | **FAIL C1 FE** | `object_ids[]=chain:INB170101`；一级权重 100% 绿；开始分析 enabled；点后未进过程页。三维仍「该维核心指标 Java 实包为空」（不挡提交） | 同 #3 | 无 Create |

Tempo（#1 search）：http://192.168.88.50:30201/api/traces/cdb77d06d63b18a4f2a80ab5770654c2  
Tempo（#2 clusters）：http://192.168.88.50:30201/api/traces/2806c27e8fc030c5d159c875f922b73a  
Grafana Explore：http://192.168.88.34:3000（**旧环境已废弃**；现网 Grafana：$newGf） 数据源 Tempo。

### 1. US-E7-POL-01c

- 打开 `/policy/search`，智能检索「半导体」。
- GET search **200**，`items=6` `total=47051`，非 5xx。
- 结果区无「加入对比篮」「深度分析」。右下角任务浮层角标 3 ≠ 对比篮。

### 2. US-E7-POL-01 / 05（页内集群→L0，不强制篮）

- 空配置：「开始分析」disabled；空点 force click **未** POST Create。
- 集群 15 项可选。`新一代信息技术` → L0 5 项：集成电路 / 传感器 / 人工智能 / 智能终端 / 软件与信息服务（`INB1303` 等短码 **能选**，不再滤空）。
- 选后开始分析 enabled。上一轮 C1-FE-L0VID **本条已闭合**。
- 残差：点「开始分析」仍因 #3～#5 同一指纹 TypeError **未发出** INB4 `industry_id` POST。未用代理 POST 补发。不因此把 #2 选簇改判红。

### 3–5. Create / wait_view（必须从 UI 点开始分析）

- VID 预填 `object_ids[]=INB170101` / `chain:INB170101`：`scopeReady` 为真，开始分析可点（L0VID 预填修 **已生效**）。
- I2-12：切粒度 **未**自动 POST。
- 从 UI 点「开始分析」：浏览器 `isSecureContext=false`，`crypto.subtle` 为 `undefined`，`createAnalysisFingerprint` 抛 `TypeError: Cannot read properties of undefined (reading 'digest')`。无 toast（未捕获），URL 仍配置态，**无** `view=processing`，**无** wait_view。
- **禁止**用代理 POST 改判 PASS。本轮 UI Create = 0。明文 analysis_fp 闸未出现（请求没发出）。

## I2-12

| 条 | 结果 |
|----|------|
| 切条件不自动起任务 | **观察到**：#3 切季/年 Create 计数 0 |
| 条件栏「开始分析」 | **有**且 VID/L0 后 enabled |
| 同用户同条件一条在跑 | **未从 UI 验到**（click 未进 processing） |
| 当天已成功直接打开结果 | **未从 UI 验到** |
| 「重新分析」force | **未从 UI 验到** |

## 问题清单

- 主 **C1 FE**：已发布 HTTP 源非安全上下文，`createAnalysisFingerprint` 依赖 `crypto.subtle`，点开始分析抛错，金路径 #3～#5 红。Create 未发出，无 Java Create `X-Trace-Id`；页内 clusters Trace `2806c27e8fc030c5d159c875f922b73a`。
- #2 页内 INB4 可选 = L0VID 修已兑现。不要再派「滤空 L0」那张。
- `?industry=INB170101` 不预填；有效 VID 路径是 `object_ids[]=INB170101`。
- 不要标 C5。不要标次要 C2（前端已是 `1ce03cc4`）。
- `e2e:policy-gold` 仍未绿。

## 修改内容

- 无业务仓代码变更。仅本 handoff + 缺陷包 + evidence 手跑脚本。

## 测试结果

- Playwright 对 http://192.168.88.50:30892：**#1 PASS，#2 PASS，#3–#5 FAIL**。
- 探针：`isSecureContext=false` / `crypto.subtle` 缺失；click 栈到 `PolicyAnalysisConfigPage` `startAnalysis`。
- 手跑记录：`evidence/LUMEN-POLICY-E-QA-SMOKE-L0VID-RETEST-L01/run-notes.json` · `policy-gold.spec.ts` · `crypto-subtle-probe.json`

## 遗留风险

1. FE 须在 HTTP NodePort（现网验收源）也能算 SHA-256，或把失败变成可见 toast；否则开始分析永远点了没反应。
2. 修好后才看得到 INB4 `industry_id` POST 是否被 Java 接受；Java 若 4xx 另开 C 段，本叶不改 Java。
3. 深圳三维 catalog 仍空；`indicatorOk` 在空 catalog 下为真，不挡提交，结果可能空。

## CI/CD（必填）

- 分支：未改业务仓
- commit：orchestration 本叶 handoff（见 git）
- pipeline：未触发业务仓 CI（QA 不改代码）
- 部署 namespace：`dev`；镜像 `gkx-lumen-topic:1ce03cc4` · `gkxlumen-innov:300ad303` · `gkxlumen-topic-policy:868987d6` · `gkxlumen-topic-async-service:868987d6` · 政策 Python `gkxlumen-entan-py-api:ea3acc39`
- K8s rollout：本单未再滚；沿用 E0 `1ce03cc4`
- dev 测试 URL：http://192.168.88.50:30892 ；网关 http://192.168.88.50:30899

## 可观测性（建议）

- OTEL_SERVICE_NAME：`gkxlumen-innov` / `gkxlumen-gateway` / `gkxlumen-topic-policy-biz`
- traceId：search `cdb77d06d63b18a4f2a80ab5770654c2`；clusters **`2806c27e8fc030c5d159c875f922b73a`** / 探活 `d73a04710224ea0d68e2d92b2ed513c7`；health `86aa1c93dfe8aa8679f8f781105fe96f`
- Tempo / Loki：Tempo API 可用。Create 未发出故无 Create span。
- 前端 console：`TypeError: Cannot read properties of undefined (reading 'digest')`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | 通过。QA 未改算法 |
| 2 调用链 前端→Java REST→Python `/internal/*` | 部分。health python `/internal/policy`；UI Create 因 FE 指纹抛错未发出 |
| 3 图谱 Nebula | 通过。未直连 nGQL |
| 4 可观测 | 通过。clusters/search `X-Trace-Id`；click 失败在浏览器 |
| 5 CI/CD | N/A（本单不改业务仓） |
| 6 demo2 merge | N/A |
| 7 共享聚合核心 | N/A |
| 8 数据策略 ADS | 通过。clusters 读 `demo_gkxlumenx_dim` 已 200 |
| 9 D8 Design | N/A（不改 UI） |
| 10 D9 血缘 | N/A；#5 QPOL-02 角标在评审块 |
| 11 D10 交互 | 部分：开始分析可点但 click 无过程页 |
| 12 D12 demo/lumen 隔离 | 通过。只认 30892 / 30899，无 demo-* 服务 |

## cost 四字段（估）

| 字段 | 值 |
|------|-----|
| actual_tokens | 480000 |
| model_used | grok-4.6 |
| actual_cost | 2.59 |
| cost_warn | green |

口径：`budget-estimate.md` §8.2，B 档 in $3/M out $15/M，qa 默认 in/out=80/20。`source: estimate`。未超 $5。

## 涉及文件

- `agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-E-QA-SMOKE-L0VID-RETEST-L01.md`（本文件）
- `agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-E-QA-SMOKE-L0VID-RETEST-L01-defect-pack.md`
- `agent-delivery/agent-handoffs/政策模块-E7/evidence/LUMEN-POLICY-E-QA-SMOKE-L0VID-RETEST-L01/`（spec + run-notes + crypto-subtle-probe.json）

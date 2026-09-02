# LUMEN-POLICY-E-C1-FE-L0VID-L01 · 政策配置页可选 map L0 且 VID 预填可提交

> 段 E 缺陷包测试驱动。只修 `PolicyAnalysisConfigPage` 根因。  
> 缺陷包：[`LUMEN-POLICY-E-QA-SMOKE-CLUSTERS-RETEST-L01-defect-pack.md`](./LUMEN-POLICY-E-QA-SMOKE-CLUSTERS-RETEST-L01-defect-pack.md)  
> 派单包：[`LUMEN-POLICY-E-C1-FE-L0VID-L01-派单包.md`](./LUMEN-POLICY-E-C1-FE-L0VID-L01-派单包.md)  
> 总控：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md) §0 #8/#9/#10 · §4

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h。bugfix。不要自行 done。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最短 diff：只改配置页 + 自检。未改 `IndustryClusterSelect` / `useIndustryClusters` / Java 闸门 / 指纹算法。未用 YAGNI 跳过 D8/D9/D10、评审挂点、I2-12 开始分析才 create。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶为定点 bugfix，未挂载 compress。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | 不改工厂拓扑。前端仍只经 gateway 调 Java；短码 L0 提交 `industry_id` 原样，图上码仍走 `industry_vid=chain:INB…`。 |
| 会签态 | 源文件已签（本叶不改图） |
| 说明 | 总控 §0 #8 禁止把 ODS 短码**当图点 VID**，不是禁止出现在下拉。 |

## 范围与实现

- 仓：`lumen-ui-topic` · `origin/dev`
- 页：`/policy/overview` · `/policy/analysis` · `/policy/recommendation`（`PolicyAnalysisConfigPage`）
- 根因：`clusterL0Options` 用 `toPolicyGraphVid` 滤空 + 页上 `require-graph-vid` 把 innov 返回的 `INB`+4 位滤掉；`scopeReady` 同时要 `clusterId` 与 `industryVid`，URL `INB170101` 已显示 `chain:INB170101` 仍 disabled。
- 修复：
  1. 去掉页上 `require-graph-vid`；`clusterL0Options` 只排除 `CL-*`，**不再**用图 VID 滤 map L0（含 `INB1303`）。
  2. `scopeReady`：已有 `toPolicyGraphVid` 成功的预填 VID **或** 已选 1 个 map L0 即可；有 VID 时不因 `clusterId` 空挡住开始分析。catalog 加载后用 `clusterForIndustry` 回填集群，没有也不挡。
  3. 提交：`INB`≥6 / `chain:` → `industry_vid=chain:INB…`；map 短码 → `industry_id` 原样；**禁止**伪造 `chain:INB1303`。
  4. 「开始分析」仍走 `job.startOrReuse` → `view=processing`（I2-12 切条件不自动 create）。
  5. `analysis_fp` SHA-256 路径未改。

## 复刻五维（本叶为配置页 bugfix，不重铺区块）

| # | 项 | 判定 |
|---|---|---|
| R1 布局 | 配置区 / 过程壳 / 结果板结构未改 | ✅ |
| R2 交互 | 空态 hint、开始分析可点、processing；切条件不 create | ✅ |
| R3 样式 | `--sci-bg-page` / 兄弟页皮肤未改 | ✅ |
| R4 评审 | 仍只挂 `@/review` TraceInfoIcon / MetricSpecCard / PendingBadge | ✅ |
| R5 Mock | 未加页内 MOCK；`USE_MOCK=false` 仍只渲染 Java 实包 | ✅ |
| W4 | 开始分析才 POST；当天复用 / 重新分析仍走 job | ✅ |
| V1–V7 | 本叶非检索 Hub；页底 token 保留 | N/A（配置工作区） |

## 测试结果

- `node src/views/policy/policyConfig.selfcheck.mjs` → `policyConfig.selfcheck ok`
  - INB4 出现在 map 选项；`CL-*` 不进选项
  - `INB170101` 预填（无 clusterId）`scopeReady=true`，hint 空
  - `INB1303` 提交 `{ industry_id: 'INB1303' }`，无 `industry_vid`
  - SHA-256 64 位小写断言仍绿
- `npx vue-tsc --build` → 零 error
- 浏览器：本机未对已发布 `30892` 复测（现网仍是旧镜像）。**需 E0 再滚 `lumen-ui-topic` 前端** 后 QA 在 http://192.168.88.50:30892 复跑金路径 #2～#5。

## 遗留风险

- Java 若拒短码 `industry_id`（无 `industry_vid`）：本叶**不改 Java**。页内选 INB4 后 Create 可能 4xx，handoff 记拒包，开 C 段补单。URL `chain:INB170101` / `INB170101` 路径应可点开始分析并进 processing。
- 现网前端镜像此前为 `gkx-lumen-topic:c4758206`（次要 C2）。本 commit 必须再滚才算发布验收。
- 未改 `IndustryClusterSelect.vue`（李伟 CHAIN 叶占用）。

## CI/CD（必填）

- 分支：`origin/dev`
- commit：`1ce03cc460ca2803c6bcd423794912ba0b211e72`
- 说明：`fix(policy): allow map INB4 L0 and VID prefill to start analysis [agent:frontend-agent]`
- pipeline URL / ID：push 后 GitLab CI（`lumen-ui-topic` / `gkx-lumen`）；本叶未等流水线绿
- 部署 namespace / 镜像 tag：**需 E0 再滚前端**；勿把旧 `c4758206` 当本修验收
- K8s rollout：待 devops
- dev 测试 URL：http://192.168.88.50:30892 （滚完后才认）

## 可观测性

- OTEL_SERVICE_NAME：`lumen-ui-topic`（前端 observability 未改）
- C1 根因 Trace：`a15b911860aa8089b8ea3b3fe6f44506`
- Tempo：http://192.168.88.50:30201/api/traces/a15b911860aa8089b8ea3b3fe6f44506
- 指纹：禁止再改；Create SHA-256 已绿（缺陷包三项 POST）

## 涉及文件

- `lumen-ui-topic/src/views/policy/PolicyAnalysisConfigPage.vue`
- `lumen-ui-topic/src/views/policy/policyConfig.selfcheck.mjs`

## 架构合规自检

| # | 铁律 | 判定 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 未改 |
| 2 | 调用链 前端→Java REST | ✅ 仍 `analysisTaskCreate` / clusters Java |
| 3 | Nebula 不直连 | ✅ |
| 4 | 可观测未拆 | ✅ |
| 5 | CI push origin/dev | ✅ 已 push，禁 force |
| 6 | 未 merge lumen←demo | ✅ |
| 7 | 前端只调 Java | ✅ |
| 8 | D8 Design token 未另起皮肤 | ✅ |
| 9 | D9 ⓘ / 角标挂点未删 | ✅ |
| 10 | D10 交互：开始分析才 create | ✅ |
| 12 | D12 未调 demo-* | ✅ |
| 指纹 | SHA-256 未改 | ✅ |

## cost

| 字段 | 值 |
|------|-----|
| estimated_tokens | 40000 |
| actual_tokens | 110000 |
| model_used | grok-4.6 |
| actual_cost | 0.72 |
| cost_warn | green |
| 说明 | 会话估算 in+out；<$5。source: session estimate |

## 给 coordinator

**联调通过**（代码层：vue-tsc 零 error + selfcheck 绿 + 已 push `origin/dev`）。请派 **E0 再滚 `lumen-ui-topic` 前端**，之后 QA 只认 http://192.168.88.50:30892 复测金路径 #2～#5。不要自行 done。

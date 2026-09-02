# LUMEN-POLICY-E-C1-FE-FP-HTTP-L01 · 政策专题 E · C1 HTTP 源也能算 analysis_fp SHA-256

> 段 E 缺陷包测试驱动。只修 `createAnalysisFingerprint` 根因。  
> 缺陷包：[`LUMEN-POLICY-E-QA-SMOKE-L0VID-RETEST-L01-defect-pack.md`](./LUMEN-POLICY-E-QA-SMOKE-L0VID-RETEST-L01-defect-pack.md)  
> 派单包：[`LUMEN-POLICY-E-C1-FE-FP-HTTP-L01-派单包.md`](./LUMEN-POLICY-E-C1-FE-FP-HTTP-L01-派单包.md)  
> 总控：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md) §4

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
| 说明 | 最短 diff：共享指纹函数一次修 + 开始分析失败 toast + 自检。未改 `IndustryClusterSelect` / `clusterL0Options` / Java 闸门 / L0 滤空。未用 YAGNI 跳过 D8/D9/D10、评审挂点、I2-12 开始分析才 create。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶为定点 bugfix，未挂载 compress。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | 不改工厂拓扑。提交仍只调 Java `analysis/tasks`。指纹算法仍是 SHA-256 64 位小写，仅补 HTTP 非安全上下文回退。 |
| 会签态 | 源文件已签（本叶不改图） |
| 说明 | 禁止把明文 `join('|')` 当 analysis_fp；Java 闸门未改。 |

## 范围与实现

- 仓：`lumen-ui-topic` · `origin/dev`
- 页：`/policy/overview` · `/policy/analysis` · `/policy/recommendation`（`PolicyAnalysisConfigPage`）
- 根因：已发布验收源 `http://192.168.88.50:30892` → `isSecureContext=false` → `crypto.subtle` 为 `undefined`。`createAnalysisFingerprint` 只走 `crypto.subtle.digest('SHA-256')`，点「开始分析」抛 `TypeError`，无 toast，不进 `view=processing`，Create 0。
- 修复：
  1. 共享函数一次修：`createAnalysisFingerprint` 改走 `sha256Hex`。`crypto.subtle` 可用时仍 Web Crypto；HTTP 用纯函数 SHA-256 回退。同输入与 subtle 字节一致，输出 `/^[a-f0-9]{64}$/`。无新 npm。政策/企业/产业链共用该函数。
  2. `startAnalysis`：指纹抛错或非 64 位小写 hex → `Message.error('分析指纹生成失败')`，禁止静默。成功路径仍 `job.startOrReuse` → `view=processing`。切条件不自动 create。
  3. 未改 `clusterL0Options` / `require-graph-vid` / `IndustryClusterSelect`。INB4 仍 `industry_id` 原样；禁止伪造 `chain:INB1303`。
- 本机未对 30892 点「开始分析」验收。**不要宣称金路径已绿。**

## 复刻五维（本叶为指纹 bugfix，不重铺区块）

| # | 项 | 判定 |
|---|---|---|
| R1 布局 | 配置区 / 过程壳 / 结果板结构未改 | ✅ |
| R2 交互 | 开始分析成功进 processing；指纹失败可见 toast；切条件不 create | ✅ |
| R3 样式 | `--sci-bg-page` / 兄弟页皮肤未改 | ✅ |
| R4 评审 | 仍只挂 `@/review` TraceInfoIcon / MetricSpecCard / PendingBadge | ✅ |
| R5 Mock | 未加页内 MOCK；`USE_MOCK=false` 仍只渲染 Java 实包 | ✅ |
| W4 | 开始分析才 POST；当天复用 / 重新分析仍走 job | ✅ |
| V1–V7 | 本叶非检索 Hub；页底 token 保留 | N/A（配置工作区） |

## 测试结果

- `node src/views/policy/policyConfig.selfcheck.mjs` → `policyConfig.selfcheck ok`
  - mock `crypto.subtle` 缺失仍产出 `/^[a-f0-9]{64}$/`
  - 与 subtle 有值时同输入同哈希（并对照 `node:crypto` createHash）
  - INB4 提交 `{ industry_id: 'INB1303' }`，无 `industry_vid`（源码断言未回退）
- `npx vue-tsc --build` → 零 error
- 浏览器：本机未对已发布 `30892` 复测。**需 E0 再滚 `lumen-ui-topic` 前端** 后 QA 在 http://192.168.88.50:30892 复跑金路径 #3～#5。

## 遗留风险

- 现网前端镜像此前为 `gkx-lumen-topic:1ce03cc4`。本 commit `7cd3be4` 必须再滚才算发布验收。未滚前金路径 #3～#5 仍会死在指纹。
- INB4 提交 `industry_id` 原样：本轮现网 Create 仍未发出（死在指纹），**未观察到** POST body。Java 若 4xx 只记、不改 Java，另开 C 段。
- 未改 `IndustryClusterSelect.vue`（李伟 CHAIN 叶）。

## CI/CD（必填）

- 分支：`origin/dev`
- commit：`7cd3be4782d19889f792e2f2e707679ffac234a0`
- 说明：`fix(policy): fallback SHA-256 analysis_fp when crypto.subtle is missing [agent:frontend-agent]`
- pipeline URL / ID：push 后 GitLab CI（`lumen-ui-topic` / `gkx-lumen`）；本叶未等流水线绿
- 部署 namespace / 镜像 tag：**需 E0 再滚前端**；勿把旧 `1ce03cc4` 当本修验收
- K8s rollout：待 devops
- dev 测试 URL：http://192.168.88.50:30892 （滚完后才认）

## 可观测性

- OTEL_SERVICE_NAME：`lumen-ui-topic`（前端 observability 未改）
- C1 根因 Trace（clusters，Create 未发出）：`2806c27e8fc030c5d159c875f922b73a`
- Tempo：http://192.168.88.50:30201/api/traces/2806c27e8fc030c5d159c875f922b73a
- Loki：按该 trace 搜 `industry-clusters`。Create span 本轮不存在。

## 涉及文件

- `lumen-ui-topic/src/composables/sha256Hex.mjs`（新增：subtle 或纯函数 SHA-256）
- `lumen-ui-topic/src/composables/analysisTaskGate.ts`
- `lumen-ui-topic/src/views/policy/PolicyAnalysisConfigPage.vue`
- `lumen-ui-topic/src/views/policy/policyConfig.selfcheck.mjs`

## 架构合规自检

| # | 铁律 | 判定 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 未改 |
| 2 | 调用链 前端→Java REST | ✅ 仍 `analysis/tasks` |
| 3 | Nebula 不直连 | ✅ |
| 4 | 可观测未拆 | ✅ |
| 5 | CI push origin/dev | ✅ 已 push，禁 force |
| 6 | 未 merge lumen←demo | ✅ |
| 7 | 前端只调 Java | ✅ |
| 8 | D8 Design token 未另起皮肤 | ✅ |
| 9 | D9 ⓘ / 角标挂点未删 | ✅ |
| 10 | D10 交互：开始分析才 create | ✅ |
| 12 | D12 未调 demo-* | ✅ |
| 指纹 | HTTP 回退仍是 SHA-256 64 位小写，未改 Java 闸门 | ✅ |

## cost

| 字段 | 值 |
|------|-----|
| estimated_tokens | 40000 |
| actual_tokens | 90000 |
| model_used | grok-4.6 |
| actual_cost | 0.59 |
| cost_warn | green |
| 说明 | 会话估算 in+out；<$5。source: session estimate |

## 给 coordinator

**联调通过**（代码层：vue-tsc --build 零 error + selfcheck 绿 + 已 push `origin/dev`）。请派 **E0 再滚 `lumen-ui-topic` 前端**，之后 QA 只认 http://192.168.88.50:30892 复测金路径 #3～#5。不要自行 done。不要把本叶当金路径已绿。

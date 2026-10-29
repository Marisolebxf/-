# LUMEN-POLICY-E-C1-FE-FP-L01 · 政策专题 E · C1 修 analysis_fp SHA-256 + 篮 VID chain:INB

> 管线：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md) §0 #8/#10 · §4  
> 派单包：[`LUMEN-POLICY-E-C1-FE-FP-L01-派单包.md`](./LUMEN-POLICY-E-C1-FE-FP-L01-派单包.md)  
> 缺陷包：[`LUMEN-POLICY-E-QA-SMOKE-L01-defect-pack.md`](./LUMEN-POLICY-E-QA-SMOKE-L01-defect-pack.md)  
> 复刻：[`fe-replica-visual-dod.md`](../../templates/fe-replica-visual-dod.md)  
> Trace：`6d2565eb49b41650e411f061c8220465`

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h。段 E 缺陷包驱动。未改 Java 闸门。未回退页内集群→L0 主路径。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用已有 `createAnalysisFingerprint` / `toPolicyGraphVid` / `resetSzModel`；未新造哈希工具、未贴 JSX、未改 Java 放行明文、未用 Demo fixture 填数。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶无大日志需压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | 提交仍只调 Java `POST /topicAsync/topic/v1/analysis/tasks`。`analysis_fp` 现为 64 位小写 SHA-256。工厂 ODS→GDF→DWD→ADS→`demo_gkx_chain` 拓扑未改。 |
| 会签态 | `approved`（`storage/POLICY/01-data-flow.md` frontmatter；本叶不翻签） |

## 范围与实现

缺陷包 C1（挡金路径 #3/#4/#5 Create；连带 #2 篮预填；#5 深圳入模）：

1. **analysis_fp**：`policyAnalysisFingerprint` 改为 `await createAnalysisFingerprint(...)`。Create / `refreshGate` / 当天复用 / 评审栏只走同一 64 hex。禁止再提交 `join('|')` 明文。
2. **篮 VID**：`buildPolicyAnalysisUrl` / 对比篮 `dispatchAnalysis` / `applyDispatch` 均经 `toPolicyGraphVid`。可挂图 L0（`INB`≥6）写成 `chain:INB…`；短码不硬提交，提示换可挂图产业。页内集群→L0 主路径未回退成必须入篮。
3. **深圳默认入模**：`loadAuxCatalogs` 拿到 `szIndicators` 且当前未勾选时走已有 `resetSzModel`。
4. 未改 Java；未调 `demo-*` 服务（D12）。

## 偏离说明

- 无。未用占位/只改 Hero 当完成。
- 已发布镜像仍是 `gkx-lumen-topic:97963375`，**需 E0 再滚 `lumen-ui-topic`** 后复测 30892。本叶未宣称已发布页已绿。

## 产物清单

- 代码：`lumen-ui-topic` `006d186dc3ef26671328b7ed54e637b10c261d50` → `origin/dev`
- 本文 handoff

## 验收证据

- `node src/views/policy/policyConfig.selfcheck.mjs`：`policyConfig.selfcheck ok`（指纹 `/^[a-f0-9]{64}$/`；`INB170101` → `chain:INB170101`；`INB1303` 不进 URL）
- `npx vue-tsc --build`：零 error
- 未改 Java；Create 契约对齐 `useEvalTask`（提交前 `await createAnalysisFingerprint`）

### 复刻五维 R1–R5

| # | 结果 |
|---|------|
| R1 布局 | ✅ 配置区 / 过程壳 / 结果板 / 记录 Tab 未拆；本叶只修 Create 契约与篮预填 |
| R2 交互 | ✅ 切条件不自动 create；开始分析才 POST；短码诚实提示；深圳 catalog 有数时默认入模 |
| R3 样式 | ✅ 未改皮肤 / token |
| R4 评审 | ✅ `@/review` 挂点未改；评审栏 `analysis_fp` 现显示 64 hex。mount-id：`E7-POL-F01/F02/F03-PAGE-TITLE-TRACE` |
| R5 Mock | ✅ `USE_MOCK=false` 未用 fixture 填指纹/VID |

### 工作区 W4

| # | 结果 |
|---|------|
| W4 | ✅ 切条件不自动 create；条件栏「开始分析」；同用户同条件 `refreshGate` 用同一哈希；当天成功复用；「重新分析」`force` |

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ 前端不哈希业务口径以外的算法 |
| 2 前端→Java REST→Python `/internal/*` | ✅ 提交仍只调 Java analysis/tasks |
| 3 图谱 Nebula | ✅ VID 只认 `chain:INB…`；不直连 nGQL |
| 4 可观测 | ✅ 复用 `request.ts` `X-Trace-Id`；缺陷 Trace `6d2565eb49b41650e411f061c8220465` |
| 5 CI/CD | ✅ 推 `origin/dev`；禁止 force |
| 6 demo2 不 merge lumen | ✅ Vue 校正，未贴 JSX |
| 7 共享聚合核心 | ✅ 未改 |
| 8 数据策略 ADS | ✅ 数仓仍 `demo_gkxlumenx_*` |
| 9 D8 Design | ✅ 未改 token |
| 10 D9 血缘 | ✅ 未自造 ⓘ |
| 11 D10 交互 | ✅ W4 门控保持 |
| 12 D12 | ✅ 只经网关 `gkxlumen-*`；未调 demo-* 服务 |

## 测试结果

- 联调通过：本地 `vue-tsc --build` 零 error；自检指纹 64 位小写 hex；篮 URL 产出 `chain:INB170101`。Create 闸门对齐 Java 契约。已发布 30892 须等 E0 滚本 commit 后再手跑 §4。

## 遗留风险

1. **必须 E0 再滚 `lumen-ui-topic`**。当前 30892 镜像 `97963375` 不含本修。
2. 篮内若全是 ODS 短码（`INB1303`），仍不可提交（诚实，需换可挂图 L0）。
3. 修指纹后 Job 仍可能 freeze failed → E1 仍红（总控：未 succeeded ≠ 空态）。

## CI/CD（必填）

- 分支：`lumen-ui-topic` `origin/dev`
- commit：`006d186dc3ef26671328b7ed54e637b10c261d50`
- pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/pipelines?ref=dev
- 部署 namespace / 镜像 tag：待 E0 滚本 SHA；**当前已发布仍是 `gkx-lumen-topic:97963375`**
- K8s rollout：本叶未点名 deploy
- dev 测试 URL：http://10.50.69.111:30892 （E0 后复测）

## 可观测性（建议）

- OTEL_SERVICE_NAME：`lumen-ui-topic` / `gkxlumen-topic-async-service-biz`
- traceId（缺陷复现）：`6d2565eb49b41650e411f061c8220465`
- Tempo：http://10.50.69.111:30201/api/traces/6d2565eb49b41650e411f061c8220465
- 修后 Create 须新抽样 `X-Trace-Id`

## 修改内容

| 路径 | 动作 |
|------|------|
| `src/config/policyAnalysisRegistry.ts` | 指纹改 SHA-256；URL 写 `chain:INB…` |
| `src/views/policy/PolicyAnalysisConfigPage.vue` | Create 前 await 哈希；篮预填 VID；深圳默认入模 |
| `src/components/enterprise/compare/IndustryCompareBasketPanel.vue` | 短码拒分发并提示 |
| `src/views/policy/policyConfig.selfcheck.mjs` | 指纹 hex + VID 自检 |
| `scripts/analysis-task-gate.test.mts` | 政策指纹 64 hex 断言 |

## cost 四字段（估）

| 字段 | 值 |
|------|-----|
| actual_tokens | 90000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.49 |
| cost_warn | green |

口径：`budget-estimate.md` §8.2，B 档 in $3/M out $15/M，frontend 默认 in/out=80/20。`source: estimate`。未超 $5。

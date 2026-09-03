# `/goal` · LUMEN-POLICY-E-C1-FE-FP-L01

```
/goal LUMEN-POLICY-E-C1-FE-FP-L01
角色：frontend-agent
监管人：human:淮政玮
认领：coordinator_dispatch · lock 24h
仓：lumen-ui-topic · origin/dev
强度：ponytail full
本单由段 E 缺陷包测试驱动。只修本包指向的根因。
复刻：布局+交互+样式+评审+Mock开关。必读 templates/fe-replica-visual-dod.md。
范围：政策三项分析 Create 契约：analysis_fp → 64 位小写 SHA-256；篮/页选产业 VID → chain:INB…；深圳默认入模。占位与只改 Hero 不算完成。
禁止：贴 JSX；页内 MOCK；改 Java 闸门放行明文；lumen 调 demo-*（D12）；USE_MOCK=false 时 fixture。
对照：缺陷包 + 本仓 useEvalTask/useIndustryAnalysisJob 的 createAnalysisFingerprint。handoff 须 R1–R5 + W4。
图：POLICY-STORAGE-FLOW 不改工厂拓扑；提交仍只调 Java analysis/tasks。
X-Trace-Id：6d2565eb49b41650e411f061c8220465
```

## 缺陷真源

- QA：[E1 金路径冒烟](101081ec-6da6-4080-a632-30d38fceebdb) FAIL 1/4
- 缺陷包：`agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-E-QA-SMOKE-L01-defect-pack.md`
- 已发布镜像当时：`gkx-lumen-topic:97963375`（SCOPE `2659503` 尚未滚到 30892；**指纹问题在 HEAD 仍在**）
- Tempo：http://192.168.88.50:30201/api/traces/6d2565eb49b41650e411f061c8220465

## 必须修（按优先级）

### 1) analysis_fp SHA-256（挡 #3/#4/#5）

`src/config/policyAnalysisRegistry.ts` `policyAnalysisFingerprint()` 现为 `join('|')` 明文。  
Java `POST /topicAsync/topic/v1/analysis/tasks` 要求 **64 位小写 SHA-256**（HTTP 200 + `code=1` `msg=analysis_fp 必须是 64 位小写 SHA-256`）。

- 复用已有 `createAnalysisFingerprint`（`src/composables/analysisTaskGate.ts`）。对照 `useEvalTask.ts`：Create **前** `await createAnalysisFingerprint(...)`。
- `PolicyAnalysisConfigPage` 的 `fingerprint` computed + `buildCreateParams().analysis_fp` 必须变成哈希后的 64 hex。
- 门控 `job.refreshGate` / 当天复用也必须用同一哈希，禁止一边明文一边哈希。
- **禁止**改 Java 校验放行明文。

### 2) 产业 VID `chain:INB…`（挡 #2；篮预填）

人审已拍板：主路径=页内集群→L0（SCOPE `2659503` 已做）。本叶补篮预填：

- `buildPolicyAnalysisUrl` / `applyDispatch`：入篮 id 经 `toPolicyGraphVid`；短码不得当 VID。
- 篮对象若是可挂图 L0（`INB`≥6），写成 `chain:INB…`；否则诚实提示换可挂图产业，**不要**用 ODS 短码硬提交。
- 页内直选路径不得回退成「必须入篮」。

### 3) 深圳默认入模（#5 次要）

`loadAuxCatalogs` 拿到 `szIndicators` 后，若当前未勾选则走已有 `resetSzModel` / 默认各维至少 1 项，使权重合计 100% 时可点「开始分析」。

## 验收

- `npx vue-tsc --build` 零 error（必须 `--build`）。
- 自检：指纹函数产出 `/^[a-f0-9]{64}$/`；禁止再提交 `join('|')` 明文。
- push `origin/dev`；commit `[agent:frontend-agent]`；禁止 force。
- handoff：`agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-E-C1-FE-FP-L01.md` + ponytail: full + cost + 是否需 E0 再确认 rollout。
- 不要自行 done。coordinator 收单后派 E0 滚 `lumen-ui-topic`，再复测 E1（只点 30892）。

## Convoy

`lumen-ui-topic` 同时只一张 coding。`FE-CHAIN-ANALYSIS-RESUME-L01` lock 已于 2026-08-21 过期，本 C1 插政策长任务主链。`LUMEN-POLICY-D-POL-01-L01` 若仍显示 in_progress 是 rebase 幽灵，handoff 已交，本叶可开工。

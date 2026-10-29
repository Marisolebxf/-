# `/goal` · LUMEN-POLICY-E-C1-FE-FP-HTTP-L01

```
/goal LUMEN-POLICY-E-C1-FE-FP-HTTP-L01
角色：frontend-agent
监管人：human:淮政玮
认领：coordinator_dispatch · lock 24h
仓：lumen-ui-topic · origin/dev
强度：ponytail full
本单由段 E 缺陷包测试驱动。只修本包指向的根因。
复刻：布局+交互+样式+评审+Mock开关不得回退。本叶是指纹 bugfix，不是重铺页。必读 templates/fe-replica-visual-dod.md。handoff 须 R1–R5 + W4。
范围：HTTP NodePort 现网源也能算出 64 位小写 SHA-256；点开始分析须进 processing；失败须可见 toast。
禁止：新 npm 包；改 Java 闸门；改 IndustryClusterSelect；重做已闭合的 L0 滤空；伪造 chain:INB1303；页内 MOCK；lumen 调 demo-*（D12）；问用户选仓。
图：POLICY-STORAGE-FLOW 不改工厂拓扑；提交仍只调 Java analysis/tasks。
C1 Trace（clusters，Create 未发出）：2806c27e8fc030c5d159c875f922b73a
```

## 缺陷真源

- QA：[复测L0VID后金路径](3e743483-884d-4c3c-b7a7-127b2b4e092f) FAIL 2/3（#1/#2 PASS）
- 缺陷包：`agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-E-QA-SMOKE-L0VID-RETEST-L01-defect-pack.md`
- 总控：`LUMEN-POLICY-ABCDE-长任务总控.md` §4（金路径只认 `http://10.50.69.111:30892`）
- 现网：`gkx-lumen-topic:1ce03cc4` · innov `300ad303` · clusters 200
- Tempo：http://10.50.69.111:30201/api/traces/2806c27e8fc030c5d159c875f922b73a

## 根因（已闭合项不要再派）

`src/composables/analysisTaskGate.ts` `createAnalysisFingerprint` 只走 `crypto.subtle.digest('SHA-256')`。  
已发布验收源是 **HTTP** `http://10.50.69.111:30892` → `isSecureContext=false` → `crypto.subtle` 为 `undefined` → 点「开始分析」抛 `TypeError`，无 toast，不进 `view=processing`，Create 0。

上一轮 L0 滤空 / VID 预填已在 `1ce03cc` 修好（#2 本轮 PASS）。**不要**再改 `clusterL0Options` / `require-graph-vid`。

## 必须修

1. **共享函数一次修**：在 `createAnalysisFingerprint` 根上修（政策/企业/产业链共用）。HTTPS / localhost 仍可用 Web Crypto；**HTTP NodePort 必须有同等 64 位小写 hex 回退**。禁止新依赖；仓内已有 hash 工具则复用，没有就最短纯函数回退。算法输出必须与 `crypto.subtle` SHA-256 **字节一致**（Java 闸门仍要 64 位小写，禁止改 Java 放行明文）。
2. **失败可见**：指纹算不出来必须 toast / Message.error，禁止静默。点「开始分析」成功路径须 `job.startOrReuse` → `view=processing`（I2-12 切条件不自动 create）。
3. **顺手核（不另开叶）**：INB4 提交 `industry_id` 原样，禁止伪造 `chain:INB1303`。Java 4xx 只记 handoff，**不改 Java**。
4. 自检：非安全上下文（可 mock `crypto.subtle` 缺失）仍产出 `/^[a-f0-9]{64}$/`；与 subtle 有值时同输入同哈希。可扩 `src/views/policy/policyConfig.selfcheck.mjs` 或给 `analysisTaskGate` 加最小自检，不要新测试框架。
5. `npx vue-tsc --build` 零 error（必须 `--build`）。

## 验收 / git

- push `origin/dev`；commit `[agent:frontend-agent]`；禁止 force。
- handoff：`agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-E-C1-FE-FP-HTTP-L01.md` + ponytail: full + cost + 是否需 E0 再滚前端。
- 不要自行 done。本机未对 30892 验收不算发布验收。coordinator 收单后派 E0 再 QA。

## Convoy

`lumen-ui-topic` 同时只一张 coding。`FE-CHAIN-ANALYSIS-RESUME-L01` lock 已于 2026-08-21 过期（幽灵 in_progress），本 C1 插政策长任务主链。`LUMEN-CHAIN-INDUSTRY-CLUSTER-L01` pending_test（李伟，产业选择器）——**禁止**改 `IndustryClusterSelect.vue`。

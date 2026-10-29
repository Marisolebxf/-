# 段 E 缺陷包（测试驱动调度）

> 来源：`LUMEN-POLICY-E-QA-SMOKE-L0VID-RETEST-L01` 复测已发布 `http://10.50.69.111:30892`。QA **不改代码**。  
> 规约：`长任务执行规约.md` §11。Create 未发出故无 Java Create `X-Trace-Id`；C1 用页内 clusters Trace + 浏览器 pageerror。  
> 总控：`LUMEN-POLICY-ABCDE-长任务总控.md` §4。

## 主缺陷（挡金路径 #3～#5：开始分析 click 因 crypto.subtle 抛错）

| 字段 | 值 |
|------|-----|
| 管线 / 总控 | `LUMEN-POLICY-ABCDE-长任务总控.md` §4 · §0 #8/#9/#10 |
| 故事 ID | `US-E7-POL-02` / `US-E7-POL-06` / `US-E7-POL-03` / `US-E7-POL-04`（#3～#5） |
| 已发布 URL | http://10.50.69.111:30892/policy/overview · `/policy/analysis` · `/policy/recommendation` |
| 操作步骤 | 登录 → URL `object_ids[]=INB170101`（或 `chain:INB170101`）打开配置页 → 确认「开始分析」enabled → 从 UI 点击 → 期望 `view=processing` → Job succeeded 后 wait_view 点「查看分析结果」 |
| 期望 | 总控 #3～#5：配置锚点后点「开始分析」→ 过程页 → succeeded 后 wait_view 点查看结果。禁止自动跳结果 |
| 实际现象 | 1) L0VID 预填已生效：VID `chain:INB170101`、clusterId 可空、开始分析 **enabled**。2) 点击后 URL **仍配置态**，无 POST `/topicAsync/topic/v1/analysis/tasks`。3) 探针：`isSecureContext=false`，`crypto.subtle` 为 `undefined`；`createAnalysisFingerprint`（`analysisTaskGate.ts`）`crypto.subtle.digest('SHA-256')` 抛 `TypeError: Cannot read properties of undefined (reading 'digest')`。栈到 `PolicyAnalysisConfigPage` `startAnalysis` onClick。无用户 toast。 |
| HTTP / 页面态 | 配置页；无 `view=processing`；UI Create **0** |
| **失败分类** | **C1 FE**（非安全 HTTP 源上指纹 API 不可用）。**不是 C5**。**不是**上一轮 L0 滤空（#2 本轮 PASS）。**不是 C2**（前端已是 `1ce03cc4`） |
| **X-Trace-Id** | Create 未发出。页内 clusters 200：`2806c27e8fc030c5d159c875f922b73a`。探活 clusters：`d73a04710224ea0d68e2d92b2ed513c7`。search：`cdb77d06d63b18a4f2a80ab5770654c2` |
| Tempo | http://10.50.69.111:30201/api/traces/2806c27e8fc030c5d159c875f922b73a |
| Loki | 按 `2806c27e8fc030c5d159c875f922b73a` 搜 `industry-clusters`。Create span **不存在** |
| 怀疑层 | **FE**：`src/composables/analysisTaskGate.ts` `createAnalysisFingerprint` 只走 `crypto.subtle`。现网验收源是 `http://10.50.69.111:30892`（非 localhost / 非 HTTPS）→ 非安全上下文。click 已到达 Vue handler，死在指纹。 |
| 诚实空态？ | **否**。Job 未从 UI 进 wait_view ≠ 空态 |

## 已闭合（不要再派）

| 项 | 证据 |
|----|------|
| 页内 INB4 可选 | #2 PASS：集群「新一代信息技术」→ L0「集成电路」/`INB1303`，开始分析 enabled |
| VID 预填可点开始分析 | #3～#5 按钮 enabled；`object_ids[]=INB170101` 显示 `chain:INB170101` |
| 前端镜像 | `gkx-lumen-topic:1ce03cc4` |
| clusters 非 500 | HTTP 200，15 条 |
| 明文 analysis_fp 闸 | 本轮 UI 未 Create，不得当结论 |

## #2 残差（不单独开修）

选 INB4 后 Create 应带 `industry_id=INB1303`、禁止 `chain:INB1303`。本轮 click 同样死在指纹，**未观察到** POST body。修好指纹后在 #2/#3 顺手核短码提交；Java 若 4xx 再开 C 段，**不要本包改 Java**。

## 建议 `/goal`（coordinator 派；QA / 分诊助手无提交权）

```text
/goal LUMEN-POLICY-E-C1-FE-FP-HTTP-L01
你是经验丰富的 frontend-agent。
本单由段 E 缺陷包测试驱动。只修本包指向的根因。
强度：ponytail full。
必读：本缺陷包 + LUMEN-POLICY-ABCDE-长任务总控.md §4 + observability.md §9。
禁止：改无关仓；无闸门写正式库；问用户选仓；用代理 POST 当验收；把 e2e:chain-gold 当政策结论；当 C5 去改 JDBC；重做已闭合的 L0 滤空。
根因：http://10.50.69.111:30892 非安全上下文，crypto.subtle 不可用；createAnalysisFingerprint 抛 TypeError，开始分析点了不进 processing。
1) 在 HTTP NodePort 现网源也能得到 64 位小写 SHA-256（与已有闸门一致）；失败必须可见 toast，禁止静默。
2) 验收只认 http://10.50.69.111:30892：VID 预填点「开始分析」须进 view=processing。
3) 顺手核 INB4 提交 industry_id 原样、禁止伪造 chain:INB1303；Java 4xx 只记不改 Java。
修完 push origin/dev；handoff 写清 commit 与是否需要 devops 再确认 rollout。
C1 证据 Trace（clusters，Create 未发出）：2806c27e8fc030c5d159c875f922b73a。
```

# 段 E 缺陷包（测试驱动调度）

> 来源：`LUMEN-POLICY-E-QA-SMOKE-L01` 手跑已发布 `http://192.168.88.50:30892`（镜像 `gkx-lumen-topic:97963375`）。QA **不改代码**。  
> 规约：`长任务执行规约.md` §11。**禁止**无 `X-Trace-Id` 开 C1。

## 主缺陷（挡金路径 #3/#4/#5 Job）

| 字段 | 值 |
|------|-----|
| 管线 / 总控 | `LUMEN-POLICY-ABCDE-长任务总控.md` §4 |
| 故事 ID | `US-E7-POL-02` / `US-E7-POL-03` / `US-E7-POL-04`（#3/#4/#5） |
| 已发布 URL | http://192.168.88.50:30892/policy/overview · `/policy/analysis` · `/policy/recommendation` |
| 操作步骤 | 登录 → 配置页带 `object_ids[]=INB170101`（图上 VID `chain:INB170101`）→ 点「开始分析」 |
| 期望 | 总控 §4：配置锚点 →「开始分析」→ 过程页 → **succeeded 后** wait_view 点查看结果；禁止自动跳结果。Job failed ≠ 空态 |
| 实际现象 | POST `/api/topicAsync/topic/v1/analysis/tasks` **HTTP 200**，业务 `code=1` `ok=false`，`msg=analysis_fp 必须是 64 位小写 SHA-256`。页面停留配置 URL，**无** `view=processing`，无过程壳。前端 `policyAnalysisFingerprint()` 只 `join('|')` 明文，未走已有 `createAnalysisFingerprint`（SHA-256） |
| HTTP / 页面态 | HTTP 200 + 业务失败；配置页；非 5xx |
| **失败分类** | **C1 产品/代码**（FE 指纹未哈希；Java 闸门按 C-TASK 契约拒单） |
| **X-Trace-Id** | `6d2565eb49b41650e411f061c8220465`（#4 复现）· 同会话更早一次 `721b34e8122eaf370b1b7e445c3b5f85` |
| Tempo | http://192.168.88.50:30201/api/traces/6d2565eb49b41650e411f061c8220465 （batches=5，gateway） |
| Loki | 按上表 trace-id 搜 `analysis_fp` |
| 怀疑层 | **FE**（先修）：`src/config/policyAnalysisRegistry.ts` `policyAnalysisFingerprint` 应产出 64 位小写 SHA-256，复用 `createAnalysisFingerprint`。Java 校验本身与 C-TASK 一致，**不要先改闸门放行明文** |
| 诚实空态？ | 否。期望未发生 |

## 连带 #2（篮分发后无法提交）

| 字段 | 值 |
|------|-----|
| 故事 ID | `US-E7-POL-01` + `US-E7-POL-05` |
| 已发布 URL | 对比篮产业 Tab → `/policy/overview?source=compare-basket&…` |
| 操作步骤 | `/industry-center/search` 搜「集成电路」加入对比篮 → 打开对比篮产业 Tab → 勾 1 → 发起分析 → 选「政策时序分析」→ 下一步 |
| 期望 | 勾选 1 个产业发起政策时序；配置页显示来自对比篮·产业；经 Java；禁止空跑 |
| 实际现象 | 配置页 **「来自对比篮 · 产业」角标可见**，query 含 `source=compare-basket`。**「开始分析」disabled**（图上 VID 未形成 `chain:INB…`）。产业查询入篮对象多为短码，`toPolicyGraphVid` 拒 `INB\d{6,}` 以外 |
| HTTP / 页面态 | 无 Create；按钮 disabled |
| **失败分类** | **C1 产品/代码**（FE：入篮 id 未规范成图上链码 / 配置页未把可挂图产业变成 `chain:INB…`） |
| **X-Trace-Id** | 本步无 Create。同页健康检查 `3a4516e481c696b1ee1a9178a944538f`；修完后用 Create trace |
| 怀疑层 | **FE**：`IndustryCompareBasketPanel` / `toPolicyGraphVid` / 查询入篮 `org_id` |
| 诚实空态？ | 否（不是「产业篮空只引导入篮」；篮内有对象却不能提交） |

## #5 指标闸（次要，修指纹后仍可能红）

深圳页 VID `chain:INB170101` 可见、一级权重合计 100% 文案出现，但「开始分析」仍可能 disabled（Java indicators 有数时未勾选入模）。修单时点「恢复默认模型」应能勾选；若默认仍不能提交，同一 C1 FE 叶补上。

## 建议 `/goal`（coordinator 派 frontend，无提交权助手勿改仓）

```text
/goal LUMEN-POLICY-E-C1-FE-FP-L01
你是经验丰富的 frontend-agent。
本单由段 E 缺陷包测试驱动。只修本包指向的根因。
强度：ponytail full。
必读：本缺陷包 + LUMEN-POLICY-ABCDE-长任务总控.md §4 + observability.md §9。
禁止：改无关仓；无闸门写正式库；问用户选仓。
1) policyAnalysisFingerprint 提交前变成 64 位小写 SHA-256（复用 createAnalysisFingerprint），经 Java 能 Create。
2) 对比篮产业对象规范为 chain:INB…（或拒短码并引导换可挂图产业），开始分析可点。
修完 push origin/dev；handoff 写清 commit 与是否需要 devops 再确认 rollout。
```

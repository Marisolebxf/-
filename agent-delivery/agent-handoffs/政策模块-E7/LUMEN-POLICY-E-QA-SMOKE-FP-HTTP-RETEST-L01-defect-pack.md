# 段 E 缺陷包（残差 · 不挡本叶金路径）

> 来源：`LUMEN-POLICY-E-QA-SMOKE-FP-HTTP-RETEST-L01`。金路径 §4 五条已 **PASS**，本包 **不是** 本叶 FAIL。  
> QA **不改 Java**。coordinator 若要修短码挂接，另开 C 段；**不要**把本叶打回 integration。  
> 规约：`长任务执行规约.md` §11。总控：`LUMEN-POLICY-ABCDE-长任务总控.md` §0 #8 / §4 #2。

## 残差（页内 INB4 短码 Create 被拒）

| 字段 | 值 |
|------|-----|
| 管线 / 总控 | `LUMEN-POLICY-ABCDE-长任务总控.md` §0 #8（图上链码）· §4 #2（页内集群→L0） |
| 故事 ID | `US-E7-POL-01` / `US-E7-POL-05`（#2 顺手核提交；**不**挡 #2 选簇 PASS） |
| 已发布 URL | http://10.50.69.111:30892/policy/overview |
| 操作步骤 | 登录 → `/policy/overview` → 集群「新一代信息技术」→ L0「集成电路」→ 点「开始分析」 |
| 期望 | FE `industry_id` 原样 `INB1303`、禁止伪造 `chain:INB1303`。派单：Java 若拒只记、不改 Java；VID 预填 #3～#5 仍须跑完（本轮已跑完且 PASS） |
| 实际现象 | FE POST `industry_id=INB1303`、`industry_vid` 空、`analysis_fp`=`469986a50778288d7623203f5732d7c4ca2448f9f9e22eb7f0f9f7470ee010f1`（64 位 SHA-256）。Java **HTTP 200**、业务 `code=1` `msg=INDUSTRY_VID_INVALID`、`ok=false`。URL 仍配置态，无 `view=processing`。**不是** HTTP 4xx。 |
| HTTP / 页面态 | Create HTTP 200 / 业务拒；配置页 |
| **失败分类** | **C1 Java**（短码 `industry_id` 未当图上 VID 接受）。**不是 C5**。**不是 C2**（前端已是 `7cd3be47`）。**不是**本叶金路径红（#2 选簇已过；#3～#5 走 `chain:INB170101` 已通） |
| **X-Trace-Id** | Create **`2edc10cd9e69edfd9a1276df51fd3730`** |
| Tempo | http://10.50.69.111:30201/api/traces/2edc10cd9e69edfd9a1276df51fd3730 |
| Loki | 按 `2edc10cd9e69edfd9a1276df51fd3730` 搜 `analysis/tasks` / `INDUSTRY_VID_INVALID` |
| 怀疑层 | **Java** `gkxlumen-topic-policy`：拒短码 `INB1303`。FE 已按总控原样提交、未伪造 `chain:INB1303`。 |
| 诚实空态？ | **否**（此残差不是 #2 允许的「未选集群/L0」空态）。不改本叶五条 PASS。 |

## 已闭合（不要再派）

| 项 | 证据 |
|----|------|
| HTTP `crypto.subtle` 抛错 | #3～#5 UI 点开始分析进 processing；探针 subtle 缺失但无 digest TypeError |
| 页内 INB4 可选 | #2 PASS：集成电路 / `INB1303` 能选 |
| VID 预填 wait_view | #3 `POLICY-20260902-007` · #4 `008` · #5 `009` 均 success 后查看结果 |
| 明文 analysis_fp 闸 | 未出现；Create fp 均为 64 位 SHA-256 |

## 建议 `/goal`（仅当 coordinator 决定修短码；本叶已 ready_to_sign）

```text
/goal LUMEN-POLICY-E-C1-JAVA-INB4-VID-L01
你是经验丰富的 api-agent。
本单由段 E 残差包驱动，不翻本叶 QA 判定。
强度：ponytail full。
必读：本缺陷包 + LUMEN-POLICY-ABCDE-长任务总控.md §0 #8。
禁止：改无关仓；无闸门写正式库；问用户选仓；把页内短码改成伪造 chain:INB1303；当 C5 改 JDBC。
根因：页内选 L0 集成电路后 FE 提交 industry_id=INB1303，Java HTTP 200 code=1 INDUSTRY_VID_INVALID。
验收只认 http://10.50.69.111:30892：选 INB4 点开始分析须被 Java 接受或产品口径明确只认 chain:INB…。
C1 Trace：2edc10cd9e69edfd9a1276df51fd3730。
修完 push origin/dev；handoff 写清 commit 与是否需要 devops 再确认 rollout。
```

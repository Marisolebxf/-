# 段 E 缺陷包（测试驱动调度）

> 来源：`LUMEN-POLICY-E-QA-SMOKE-CLUSTERS-RETEST-L01` 复测已发布 `http://10.50.69.111:30892`。QA **不改代码**。  
> 规约：`长任务执行规约.md` §11。**禁止**无 `X-Trace-Id` 开 C1。  
> 总控：`LUMEN-POLICY-ABCDE-长任务总控.md` §4（#2 = 页内集群→L0，不强制篮）。

## 主缺陷（挡金路径 #2～#5：页内 L0 被 requireGraphVid 滤空）

| 字段 | 值 |
|------|-----|
| 管线 / 总控 | `LUMEN-POLICY-ABCDE-长任务总控.md` §4 · §0 #8/#9/#10 |
| 故事 ID | `US-E7-POL-01` / `US-E7-POL-05` / `US-E7-POL-02` / `US-E7-POL-03` / `US-E7-POL-04`（#2～#5） |
| 已发布 URL | http://10.50.69.111:30892/policy/overview · `/policy/analysis` · `/policy/recommendation` |
| 操作步骤 | 登录 → `/policy/overview` 页内选集群再选 L0；另以 `object_ids[]=INB170101` 预填三项配置页，点「开始分析」 |
| 期望 | #2 先集群再该 map 下 L0 恰好 1 个，开始分析可点。#3～#5 开始分析 → 过程页 → succeeded 后 wait_view 点结果 |
| 实际现象 | 1) `GET /api/topic/v1/meta/industry-clusters?include_l0=true` **HTTP 200**，15 条，L0 全是 `INB`+4 位（`INB1303` 等），**零条** `INB\\d{6,}` / `chain:INB…`。2) `toPolicyGraphVid` + `require-graph-vid` 把 L0 滤空；产业下拉 disabled；hint「尚未选择分析对象」；开始分析 disabled。3) URL 预填 `INB170101` 时 **图上 VID：chain:INB170101 已显示**，hint 仍「尚未选择分析对象」（`clusterId` 空），开始分析仍 disabled。UI **未** POST Create。 |
| HTTP / 页面态 | clusters **200**（非 500）；配置页；无 `view=processing` |
| **失败分类** | **C1 FE**（L0 全是 INB+4 位短码被 `requireGraphVid` 滤空）。**不是 C5**（dim 表已可读，clusters 非 500） |
| **X-Trace-Id** | clusters 200：`a15b911860aa8089b8ea3b3fe6f44506`（页内）· `2d1736556975b954204e0af9fe2920fc`（探活） |
| Tempo | http://10.50.69.111:30201/api/traces/a15b911860aa8089b8ea3b3fe6f44506 |
| Loki | 按 `a15b911860aa8089b8ea3b3fe6f44506` 搜 `industry-clusters` |
| 怀疑层 | **FE**：`PolicyAnalysisConfigPage` `clusterL0Options` / `IndustryClusterSelect require-graph-vid` 滤掉 innov 返回的 ODS 短码；`scopeReady` 另要 `clusterId`，URL 已有图上 VID 仍不可提交。可选后续：DIM L0 改存图上码（不挡本包 C1 FE 开修） |
| 诚实空态？ | **否**。总控 #2 不允许把「选不了 L0」当完成；#3 Job 未从 UI 进 wait_view ≠ 空态 |

## Create / SHA-256（本轮已发出，明文闸未复现）

UI 开始分析未点亮。QA 经 **30892** 代理 POST `/api/topicAsync/topic/v1/analysis/tasks`（`force=true`，`analysis_fp` = 64 位小写 SHA-256，`industry_vid=chain:INB170101`）：

| 路径 | taskId | HTTP | code | plaintextGate | X-Trace-Id | 随后 GET status |
|------|--------|------|------|---------------|------------|-----------------|
| #3 timeseries | `POLICY-20260902-004` | 200 | 0 | **false** | `e0c6f9aa9a9df91e5dd195dedbc7221d` | success |
| #4 regional | `POLICY-20260902-005` | 200 | 0 | **false** | `b05b4efb33c2b2cfa3832a2adef4c87c` | success |
| #5 shenzhen | `POLICY-20260902-006` | 200 | 0 | **false** | `ad303f354dad83fa8990ded7ee999e22` | success |

**禁止**再用「明文 analysis_fp」当本叶结论。API success **不能**改判金路径 PASS。

## 次要 C2（前端镜像门）

现网 `gkx-lumen-topic:c4758206`，门要 `006d186d`。疑 helm:chart 连带滚动。`origin/dev` 仍是 `006d186d`。**不要**只派 devops 滚回镜像当 #2 修复——同源 `INB\\d{6,}` 仍会滤空 INB4。

## #5 权重 / 入模（未到 UI Job）

深圳页绿条「一级权重 100%，可开始分析。」三维 catalog「该维核心指标 Java 实包为空」。开始分析仍因无集群 disabled。

## 建议 `/goal`（coordinator 派；QA / 分诊助手无提交权）

```text
/goal LUMEN-POLICY-E-C1-FE-L0VID-L01
你是经验丰富的 frontend-agent。
本单由段 E 缺陷包测试驱动。只修本包指向的根因。
强度：ponytail full。
必读：本缺陷包 + LUMEN-POLICY-ABCDE-长任务总控.md §0 #8/#10 + observability.md §9。
禁止：改无关仓；无闸门写正式库；问用户选仓；把 e2e:chain-gold 当政策结论；当 C5 去改 JDBC。
1) 页内集群→L0：innov 已 200 返回的 INB+4 位短码不得被 requireGraphVid 滤成「选不了」。L0 须能形成 chain:INB…（映射或放宽展示+提交）。
2) URL / 预填已有 chain:INB170101 时，clusterId 须挂上或不再因无集群挡住「开始分析」。
3) 验收只认 http://10.50.69.111:30892。clusters GET 须保持非 500。
修完 push origin/dev；handoff 写清 commit 与是否需要 devops 再确认 rollout。
C1 X-Trace-Id：a15b911860aa8089b8ea3b3fe6f44506。
```

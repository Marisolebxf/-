# 段 E 缺陷包（测试驱动调度）

> 来源：`LUMEN-POLICY-E-QA-SMOKE-C1RETEST-L01` 复测已发布 `http://10.50.69.111:30892`（镜像 **`gkx-lumen-topic:006d186d`**，已换掉 `97963375`）。QA **不改代码**。  
> 规约：`长任务执行规约.md` §11。**禁止**无 `X-Trace-Id` 开 C1。  
> 总控：`LUMEN-POLICY-ABCDE-长任务总控.md` §4（#2 = 页内集群→L0，不强制篮）。

## 主缺陷（挡金路径 #2～#5：页内选不了可挂图 L0）

| 字段 | 值 |
|------|-----|
| 管线 / 总控 | `LUMEN-POLICY-ABCDE-长任务总控.md` §4 · §0 #6/#9/#10 |
| 故事 ID | `US-E7-POL-01` / `US-E7-POL-05` / `US-E7-POL-02` / `US-E7-POL-03` / `US-E7-POL-04`（#2～#5） |
| 已发布 URL | http://10.50.69.111:30892/policy/overview · `/policy/analysis` · `/policy/recommendation` |
| 操作步骤 | 登录 → `/policy/overview` 页内选集群再选 L0；另以 `object_ids[]=INB170101` 预填三项配置页，点「开始分析」 |
| 期望 | #2 先集群再该 map 下 L0 恰好 1 个，开始分析可点（时序三维全开）。#3～#5 开始分析 → 过程页 → succeeded 后 wait_view 点结果 |
| 实际现象 | 1) `GET /api/topic/v1/meta/industry-clusters?include_l0=true` **HTTP 500**。Tempo：`Table 'gkxlumenx_dim.industry_cluster_map' doesn't exist`，服务 `gkxlumen-innov`。2) 页内产业下拉「无相关产业数据」，开始分析 disabled。catalog 降级项均为 `INB\d{4}` 短码，`requireGraphVid`（`INB`≥6）滤空。3) URL 预填 `INB170101` 时 **图上 VID：chain:INB170101 已显示**，但 hint 仍「尚未选择分析对象」（父级 `clusterId` 空），开始分析仍 disabled。Create **未发出**。 |
| HTTP / 页面态 | clusters **500**；配置页；非 5xx 页面。无 `view=processing` |
| **失败分类** | **C5 结构/库闸**（主：`gkxlumenx_dim.industry_cluster_map` 不存在；现网数仓约定是 `demo_gkxlumenx_*`，innov 打了正式前缀 dim）。连带 **C1 FE**：VID 已形成仍因无集群不可提交 |
| **X-Trace-Id** | clusters 500：`071b34f54c36d31761617fc884567f03`（30892）· `8c38804c66e812b26505c544e0d6a083`（30899） |
| Tempo | http://10.50.69.111:30201/api/traces/071b34f54c36d31761617fc884567f03 （batches=6，gateway + innov，error span 如上表） |
| Loki | 按 `071b34f54c36d31761617fc884567f03` 搜 `industry_cluster_map` |
| 怀疑层 | **Java/发布-配错**：`gkxlumen-innov` meta 读正式 `gkxlumenx_dim`；表不在 / JDBC 未指向 demo 前缀。FE 降级 catalog 短码诚实滤空，符合 VID 规则，但金路径无可用 L0 |
| 诚实空态？ | **否**。总控 #2 不允许把「无相关产业数据」当完成；#3 Job 未 succeeded ≠ 空态 |

## 连带：Create / SHA-256 本轮未复测到

首轮 C1（明文 `analysis_fp`）镜像已换成 `006d186d`。本轮 **开始分析未点亮**，POST `/topicAsync/topic/v1/analysis/tasks` **0 次**，故 **不得**宣称指纹闸已绿，也 **不得**再用旧结论 `analysis_fp 必须是 64 位小写 SHA-256`。clusters/L0 修好后须再跑 #3～#5 Create。

## #5 权重 / 入模（未到 Job）

深圳页绿条「一级权重 100%，可开始分析。」三维 catalog「该维核心指标 Java 实包为空」→ `indicatorOk` 在空 catalog 下为真。开始分析仍因无集群 disabled。任务未跑通。

## 建议 `/goal`（coordinator 派；QA / 分诊助手无提交权）

```text
/goal LUMEN-POLICY-E-C5-CLUSTERS-L01
你是经验丰富的 api-agent（JDBC/库闸需 data 会签）。
本单由段 E 缺陷包测试驱动。只修本包指向的根因。
强度：ponytail full。
必读：本缺陷包 + LUMEN-POLICY-ABCDE-长任务总控.md §0 #6/#9 + observability.md §9。
禁止：改无关仓；无闸门写正式库；问用户选仓；把 e2e:chain-gold 26205 当政策结论。
1) GET /topic/v1/meta/industry-clusters?include_l0=true 不得 500。
2) 数仓只认 demo_gkxlumenx_* ；禁止为「上 lumen」改正式 gkxlumenx_dim JDBC。
3) Tempo 根因：Table 'gkxlumenx_dim.industry_cluster_map' doesn't exist（trace 071b34f54c36d31761617fc884567f03）。
4) 返回的 L0 须能形成 chain:INB…（INB≥6 或已是 chain:），页内集群→L0 可选恰好 1 个。
修完 push origin/dev；handoff 写清 commit 与是否需要 devops 再确认 rollout。
前端 clusterId 与 VID 预填绑定：等本叶 clusters 有可挂图 L0 后再派 FE（否则仍选不了）。
```

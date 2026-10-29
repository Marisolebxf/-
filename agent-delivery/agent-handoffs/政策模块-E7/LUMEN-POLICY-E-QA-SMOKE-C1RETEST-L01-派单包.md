# `/goal` · LUMEN-POLICY-E-QA-SMOKE-C1RETEST-L01

```
/goal LUMEN-POLICY-E-QA-SMOKE-C1RETEST-L01
角色：qa-agent
监管人：human:淮政玮
认领：coordinator_dispatch · lock 24h
只认：http://10.50.69.111:30892
强度：ponytail full
金路径：总控 §4 五条（#2 已改为页内集群→L0，不强制对比篮）。
期望未发生必红。QA 不改代码。
镜像门：必须先确认前端是 gkx-lumen-topic:006d186d（或更新）。仍是 97963375 → 本叶 blocked，不要用旧结论。
```

## 背景

首轮 E1 FAIL（[E1 金路径冒烟](101081ec-6da6-4080-a632-30d38fceebdb)）：指纹明文、篮短码。C1 已修 `006d186`，E0 已滚 30892。本叶是**复测**，不是重开首轮。

## 五条（以总控现行 §4 为准）

1. `/policy/search` 能出卡；无入篮/深度分析。
2. `/policy/overview`：**页内**先集群再 L0（恰好 1 个），不强制篮；开始分析可点（时序三维全开）。篮预填可选，不作为本条唯一路径。
3. 时序：开始分析 → 过程页 → succeeded 后 wait_view 点结果。Job failed ≠ 空态。
4. 区域对比同上，出矩阵/雷达。
5. 深圳三维：权重合计 100%、默认可入模、任务跑通。

Create 不得再报 `analysis_fp 必须是 64 位小写 SHA-256`。C1 必带 X-Trace-Id。失败先 C1–C6。

handoff：`agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-E-QA-SMOKE-C1RETEST-L01.md`。不要自行 done。

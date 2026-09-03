# `/goal` · LUMEN-POLICY-E-QA-SMOKE-CLUSTERS-RETEST-L01

```
/goal LUMEN-POLICY-E-QA-SMOKE-CLUSTERS-RETEST-L01
角色：qa-agent
监管人：human:淮政玮
认领：coordinator_dispatch · lock 24h
只认：http://192.168.88.50:30892
强度：ponytail full
金路径：总控 §4 五条（#2 = 页内集群→L0，不强制篮）。
期望未发生必红。QA 不改代码。
门：clusters GET 须非 500；innov 镜像 300ad303；前端 006d186d。
```

## 背景

上一轮 FAIL：clusters 500（正式 dim 表不存在）。C1 `300ad30` + E0 已滚 `gkxlumen-innov:300ad303`，探活 clusters **200**、15 条。本叶复测 #2～#5（#1 已 PASS 可再扫一眼）。

Create 须发出；不得再报 analysis_fp SHA-256 明文闸。失败先 C1–C6，C1 带 X-Trace-Id。

注意：L0 若全是 `INB`+4 位短码，前端 `requireGraphVid`（`INB`≥6）会滤空——那是 **C1 FE**，不是 C5。

handoff：`agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-E-QA-SMOKE-CLUSTERS-RETEST-L01.md`。不要自行 done。

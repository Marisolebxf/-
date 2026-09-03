# `/goal` · LUMEN-POLICY-E-DEVOPS-INNOV-DIM-L01

```
/goal LUMEN-POLICY-E-DEVOPS-INNOV-DIM-L01
角色：devops-agent
监管人：human:淮政玮
认领：coordinator_dispatch · lock 24h
仓：lumen-svc-platform CI/K8s（本轮点名 gkxlumen-innov）
强度：ponytail full
点名：gkxlumen-innov 镜像含 300ad30 + Helm INNOV_DIM_SCHEMA=demo_gkxlumenx_dim
禁止：等聊天「已经滚了」；改业务代码；DDL 正式库；改正式 JDBC 前缀；把 CHAIN e2e 红当本轮失败。
数仓：demo_gkxlumenx_*。
```

## 为何

政策 E1 复测 clusters **500**：Java 读了 `gkxlumenx_dim.industry_cluster_map`。C1 `300ad30` 已把默认/Helm 绑到 `demo_gkxlumenx_dim`。只滚前端不够。

探活：`GET http://192.168.88.50:30899/topic/v1/meta/industry-clusters?include_l0=true` 不得 500。
（网关路径以现网为准：也可能是 `/policy` 前缀以外的 topic meta；以 30892 前端实际打的 `/api/topic/v1/meta/industry-clusters` 经网关为准。）

前端 `gkx-lumen-topic:006d186d` 已绿，本轮不要重滚 UI。Python 政策 HTTP 不重滚。

## 验收

- innov Pod 带 `INNOV_DIM_SCHEMA=demo_gkxlumenx_dim`（或镜像默认已是 demo）。
- clusters 非 500。
- handoff：`agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-E-DEVOPS-INNOV-DIM-L01.md`
- MCP tech_task → ready_to_sign。不要自行 done。不要宣称金路径已绿。

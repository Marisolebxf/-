# `/goal` · LUMEN-POLICY-E-DEVOPS-C1ROLL-L01

```
/goal LUMEN-POLICY-E-DEVOPS-C1ROLL-L01
角色：devops-agent
监管人：human:淮政玮
认领：coordinator_dispatch · lock 24h
仓：lumen-ui-topic CI/K8s（本轮只滚前端）
强度：ponytail full
点名：lumen-ui-topic → http://10.50.69.111:30892 镜像必须含 006d186（或其后 SHA）
数仓：demo_gkxlumenx_*。禁止改正式前缀 JDBC。
禁止：等聊天「已经滚了」；改业务代码；把 innov/entan/CHAIN e2e 红当本轮失败；改 Java/Python helm（本轮不需要）。
```

## 为何只滚前端

E1 手跑镜像仍是 `gkx-lumen-topic:97963375`。之后 `origin/dev` 已有三笔未发布：

| SHA | 叶 | 内容 |
|-----|-----|------|
| `d5ea3f7` | DETAIL | 查询详情抽屉 |
| `2659503` | SCOPE | 集群→L0，不强制篮 |
| `006d186` | C1-FE-FP | analysis_fp SHA-256 + 篮 VID `chain:INB…` + 深圳默认入模 |

Java `gkxlumen-topic-policy:7d12b8dd` / async `7d12b8dd` / 政策 HTTP `gkxlumen-entan-py-api:ea3acc39` **E0 已绿，本轮不要重滚**，除非探活已挂。

## 验收

- Deployment `gkx-lumen-topic` 镜像 tag = `006d186…` 或更新；NodePort 30892 HTTP 200。
- 禁止宣称业务金路径已绿（那是 E1 复测）。
- handoff：`agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-E-DEVOPS-C1ROLL-L01.md` + ponytail: full + cost。
- MCP 走到 ready_to_sign（tech_task）。不要自行 done。
- `e2e:chain-gold` 红不挡本叶。

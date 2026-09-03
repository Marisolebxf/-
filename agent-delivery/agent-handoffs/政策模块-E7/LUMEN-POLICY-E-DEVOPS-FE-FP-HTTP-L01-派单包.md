# `/goal` · LUMEN-POLICY-E-DEVOPS-FE-FP-HTTP-L01

```
/goal LUMEN-POLICY-E-DEVOPS-FE-FP-HTTP-L01
角色：devops-agent
监管人：human:淮政玮
认领：coordinator_dispatch · lock 24h
仓：lumen-ui-topic CI/K8s（本轮只滚前端）
强度：ponytail full
点名：gkx-lumen-topic 镜像含 7cd3be4（或其后）
禁止：等聊天「已经滚了」；改业务代码；重滚 innov/Python；把 CHAIN e2e 红当本轮失败。
```

## 背景

C1 `LUMEN-POLICY-E-C1-FE-FP-HTTP-L01` SHA **`7cd3be4`**：HTTP 非安全上下文下 `createAnalysisFingerprint` 回退 SHA-256。  
现网仍是 `gkx-lumen-topic:1ce03cc4`，未滚前 #3～#5 仍会死在 `crypto.subtle`。

innov `300ad303` / 政策 Python **不重滚**。

## 做法

1. 看 origin/dev pipeline frontend:build / image / deploy。未自动则点名，直到 Deployment `gkx-lumen-topic` 镜像 ≥ `7cd3be4`。
2. GET http://192.168.88.50:30892 HTTP 200。
3. innov / 政策 Python 不重滚。
4. 不要把 `e2e:chain-gold` 红当本叶失败。
5. handoff：`agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-E-DEVOPS-FE-FP-HTTP-L01.md` + ponytail: full + cost。
6. MCP tech_task → ready_to_sign。不要自行 done。不要宣称金路径已绿。

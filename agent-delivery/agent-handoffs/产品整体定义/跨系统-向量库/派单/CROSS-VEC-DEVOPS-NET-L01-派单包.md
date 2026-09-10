# 派单包 · CROSS-VEC-DEVOPS-NET-L01

```yaml
task_id: CROSS-VEC-DEVOPS-NET-L01
dispatcher: agent:coordinator-agent
suggested_supervised_by: human:淮政玮
claim_type: coordinator_dispatch
date: 2026-09-10
status: backlog
ponytail: full
```

## 1. 范围 / 不做

**做**：`lumen-algo-py` / entan 运行时出网 `192.168.88.48:19530`；环境变量文档；最小权限（禁止 drop/insert `amcpdp-*`）。

**不做**：创建产业 collection（PY-INDEX）；改多媒体检索。

## 2. /goal

```text
/goal devops-agent
身份：资深 DevOps；CI/CD 与 K8s 出网。
强度：ponytail full。
任务：CROSS-VEC-DEVOPS-NET-L01
仓库：以 helm / lumen-algo-py 部署清单为准（D12：只 lumen，不打 demo-*）。
目标：Python 进程可达 Milvus gRPC 19530；密钥进环境不进 git。
验收：handoff 附连通探测（list collections 只读即可）+ 回滚；证明未对 amcpdp-* 写入。
禁止：Java/前端连 19530；force push。
commit：[agent:devops-agent]；push origin/dev。
```

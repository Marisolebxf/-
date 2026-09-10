# 派单包 · CROSS-VEC-API-FEIGN-L01

```yaml
task_id: CROSS-VEC-API-FEIGN-L01
dispatcher: agent:coordinator-agent
suggested_supervised_by: human:侯佳伟
claim_type: coordinator_dispatch
date: 2026-09-10
status: backlog
ponytail: full
```

## 1. 范围 / 不做

**做**：Feign `embed/rebuild`、`embed/search`；未就绪 **501** + honesty。

**不做**：`jobs/enrich` 门面（**API-JOB 叶**）；Java embed；直连 19530；假 VID。

## 2. /goal

```text
/goal api-agent
身份：资深 Java 平台工程师。不写算法、不 embed、不直连 nGQL/Milvus。
强度：ponytail full。
任务：CROSS-VEC-API-FEIGN-L01
仓库：${GKX_ROOT}/repos/lumen-svc-platform
依赖：CROSS-VEC-PY-INDEX-L01
目标：Feign embed/rebuild + embed/search；501 honesty。
不做：jobs/enrich（见 CROSS-VEC-API-JOB-L01）。
D12：禁止 demo-*；不向前端暴露 Milvus IP。
commit：[agent:api-agent]；push origin/dev。
```

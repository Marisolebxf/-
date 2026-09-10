# 派单包 · CROSS-VEC-API-JOB-L01

```yaml
task_id: CROSS-VEC-API-JOB-L01
dispatcher: agent:coordinator-agent
suggested_supervised_by: human:侯佳伟
claim_type: coordinator_dispatch
date: 2026-09-10
status: backlog
ponytail: full
```

## 1. 范围 / 不做

**做**：Java 创建/轮询 `jobs/enrich`（Feign Python）；501 + honesty；`job_kind` 与专题「开始分析」区分。

**不做**：直连 Milvus；embed；把 ETL 补槽做成 I2-12 分析工作区结果页；本叶不实现 Job B 门面（可预留路径注释）。

与 **API-FEIGN**：FEIGN=search/rebuild；本叶=跑批 Job。

## 2. /goal

```text
/goal api-agent
身份：资深 Java 平台工程师。不写算法、不 embed、不直连 nGQL/Milvus。
强度：ponytail full。
任务：CROSS-VEC-API-JOB-L01
仓库：${GKX_ROOT}/repos/lumen-svc-platform
依赖：CROSS-VEC-JOB-A-L01（Python as-built 路径）
目标：Feign /internal/industry/jobs/enrich + status；未就绪 501。
D12：禁止 demo-*。与 topic-async 复用时必须分 job_kind（ETL 补槽 ≠ 用户分析）。
commit：[agent:api-agent]；push origin/dev。
```

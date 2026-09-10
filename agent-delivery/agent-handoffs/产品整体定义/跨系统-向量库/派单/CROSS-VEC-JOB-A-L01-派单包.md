# 派单包 · CROSS-VEC-JOB-A-L01

```yaml
task_id: CROSS-VEC-JOB-A-L01
dispatcher: agent:coordinator-agent
suggested_supervised_by: human:唐绍祖
claim_type: coordinator_dispatch
date: 2026-09-10
status: backlog
ponytail: full
```

## 1. 为什么派

SAD 02 §3.2：4.7 万政策不能在重灌里 embed。Job A = **ETL 长任务**向量补槽，夜班在 L0+L1 重灌之后、Hang 之前。

## 2. 范围 / 不做

**做**：`POST /internal/industry/jobs/enrich`（incremental|full、force、cursor、limit）；worker 循环 `embed/search` → `match_industry_anchors` 写槽；单飞；进度字段。

**不做**：rebuild Milvus；进重灌同步 HTTP；Job B LLM；Hang 写图；假 VID。

与 **POLICY-SEARCH** 分工：本叶=跑批；SEARCH=按钮/`limit=1`，**须共用同一 worker/定码**，禁止两套规则。

## 3. 必读

- 向量库 `02` §3.1 §3.2；`03` §5
- 知识图谱 `02` §3.2 夜班顺序（Hang 在 Job A 后）
- `长任务执行规约.md`（可恢复、有 job id）

## 4. /goal

```text
/goal algorithm-agent
身份：资深 Python 算法工程师。算法只在 Python /internal/*。
强度：ponytail full。
图：必含 向量库 02 §3.1 三种消费入口 + §3.2 Job A（禁止画进重灌同步框）。
任务：CROSS-VEC-JOB-A-L01
仓库：${GKX_ROOT}/repos/lumen-algo-py
依赖：CROSS-VEC-PY-INDEX-L01、CROSS-VEC-POLICY-L0-L01
目标：ETL Job A industry_embed_enrich — 未对码政策 search→定码写槽；增量默认、全量可开；单飞。
硬闸：重灌路径无 enrich；不 rebuild；无假 VID；进度 processed/skipped/coded/failed。
与 POLICY-SEARCH：同 worker，按钮只是小 limit。
handoff：ponytail: full；cost；样例 job 日志。
commit：[agent:algorithm-agent]；push origin/dev。
```

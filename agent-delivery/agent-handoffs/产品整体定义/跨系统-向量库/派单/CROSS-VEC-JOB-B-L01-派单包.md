# 派单包 · CROSS-VEC-JOB-B-L01（P2）

```yaml
task_id: CROSS-VEC-JOB-B-L01
dispatcher: agent:coordinator-agent
suggested_supervised_by: human:唐绍祖
claim_type: coordinator_dispatch
date: 2026-09-10
status: backlog
priority: P2
ponytail: full
```

## 1. 范围 / 不做

**做**：`jobs/extract-llm`；默认拒绝除非 `enable_llm=true`；只出中文名；宜限制在 Job A top-k；定码仍走锚点。

**不做**：进重灌；rebuild；默认夜班开启（须 VEC-Q5）；假 `chain:` 码。

**解锁时机**：Job A 绿 + ARCH 配额会签后再 confirm。

## 2. /goal

```text
/goal algorithm-agent
身份：资深 Python 算法工程师。
强度：ponytail full。
图：必含 02 §3.2 Job B（默认关，在 Job A 之后）。
任务：CROSS-VEC-JOB-B-L01
仓库：${GKX_ROOT}/repos/lumen-algo-py
依赖：CROSS-VEC-JOB-A-L01
目标：ETL Job B L2 抽名跑批；enable_llm 门闩；失败回退 A/L1。
硬闸：丢弃模型自造 chain:；不进重灌；dry_run 可验。
commit：[agent:algorithm-agent]；push origin/dev。
```

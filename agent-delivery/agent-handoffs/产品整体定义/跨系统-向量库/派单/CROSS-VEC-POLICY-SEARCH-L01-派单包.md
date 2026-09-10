# 派单包 · CROSS-VEC-POLICY-SEARCH-L01

```yaml
task_id: CROSS-VEC-POLICY-SEARCH-L01
dispatcher: agent:coordinator-agent
suggested_supervised_by: human:唐绍祖
claim_type: coordinator_dispatch
date: 2026-09-10
status: backlog
ponytail: full
```

## 1. 范围 / 不做

**做**：交互入口（按钮 / 小 `limit`）调用与 Job A **同一** enrich worker → search → 定码写槽。reload **默认同步关**。

**不做**：万级全量跑批实现（**JOB-A 叶**主交付）；L2 LLM（JOB-B）；rebuild；theme 填 industry；假 VID；另写第二套定码。

## 2. 与 Job A

| | POLICY-SEARCH | JOB-A |
| --- | --- | --- |
| 触发 | UI 按钮 / 抽样 | 调度器 / 夜班 |
| 规模 | 单条～小 limit | 增量/全量 + cursor |
| 代码 | **共用 worker** | 同左 |

可与 JOB-A 同 Sprint 串行：先 JOB-A worker，本叶只挂按钮。

## 3. /goal

```text
/goal algorithm-agent
身份：资深 Python 算法工程师。
强度：ponytail full。
图：必含 02 §3.1（按钮入口）；跑批框指向 JOB-A，勿画进重灌。
任务：CROSS-VEC-POLICY-SEARCH-L01
仓库：${GKX_ROOT}/repos/lumen-algo-py
依赖：PY-INDEX + POLICY-L0（建议 JOB-A worker 已有或本叶抽共享模块）
目标：语义抽槽按钮；重灌默认同步不调 search；定码同源 Job A。
验收：单测默认关；开启后无码只留 {name}；无第二套 VID 规则。
commit：[agent:algorithm-agent]；push origin/dev。
```

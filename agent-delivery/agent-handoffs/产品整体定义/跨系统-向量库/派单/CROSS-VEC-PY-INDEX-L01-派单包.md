# 派单包 · CROSS-VEC-PY-INDEX-L01

```yaml
task_id: CROSS-VEC-PY-INDEX-L01
dispatcher: agent:coordinator-agent
suggested_supervised_by: human:唐绍祖
claim_type: coordinator_dispatch
date: 2026-09-10
status: backlog
ponytail: full
```

## 1. 为什么派

产业锚点索引：词表=图上 chain/segment。物理落现网 Milvus **新 collection**。为 Job A / 按钮提供 `search`。

## 2. 范围 / 不做

**做**：`embed/rebuild`（整库一次）；`embed/search`（单条）；内存回退单测；honesty。

**不做**：`jobs/enrich` 跑批（**JOB-A 叶**）；政策重灌调 rebuild；`amcpdp-*`；灌链挂钩（CHAIN-HOOK）；假 VID。

## 3. 图即契约

`diagram_id`: 02 §1.1。handoff 抄：建库切面 vs 消费切面；rebuild **禁止**出现在 Job A/B。

## 4. /goal

```text
/goal algorithm-agent
身份：资深 Python 算法工程师。算法只在 Python /internal/*。
强度：ponytail full。
图：必含 02 §1.1；注明 jobs/enrich 不在本叶。
任务：CROSS-VEC-PY-INDEX-L01
仓库：${GKX_ROOT}/repos/lumen-algo-py
必读：03§0–§2；本派单包；D1/D12。
目标：gkxlumen-industry-* + rebuild/search。
硬闸：禁止 amcpdp-*；连不上 degraded/非0；pytest 内存回退。
依赖：ARCH-SIGN、DEVOPS-NET。未会签可先内存实现。
commit：[agent:algorithm-agent]；push origin/dev。
```

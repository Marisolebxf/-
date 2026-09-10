# 派单包 · CROSS-KG-HANG-BATCH-L01

```yaml
task_id: CROSS-KG-HANG-BATCH-L01
dispatcher: agent:coordinator-agent
suggested_supervised_by: human:唐绍祖
collaborators: data-agent
claim_type: coordinator_dispatch
date: 2026-09-10
status: backlog
ponytail: full
```

## 1. 为什么派

知识图谱 SAD 02 §3.1：Hang 是 **ETL 写图批**，不是 G3 分析，也不是重灌。无码政策 hang 会大量 skip → 建议先跑向量 Job A。

## 2. 范围 / 不做

**做**：`graph_hang` 跑批（政策域优先）；稳定码 → FETCH → 写事实边；skip 计数；单飞/cursor；与重灌解耦。

**不做**：编 VID；同步重灌挂钩；G3 Result；B 面 publish（另叶）；推理 LLM 全量（可后接 infer 叶）。

## 3. 必读

- 知识图谱 `02` §3.1 §3.2；`03` §1.4.1 §2.3.1
- 向量库 `02` §3.2 夜班顺序
- 现网 `polan/graph/ops.py` hang / `no_stable_id`

## 4. /goal

```text
/goal algorithm-agent
身份：资深 Python 算法工程师。
强度：ponytail full。
图：必含 知识图谱 02 §3.1 写图入口表（Hang ≠ G3 ≠ 重灌）。
任务：CROSS-KG-HANG-BATCH-L01
仓库：${GKX_ROOT}/repos/lumen-algo-py
依赖：CROSS-VEC-JOB-A-L01（建议；无码 skip 须诚实可测）
目标：ETL Hang 跑批 — 政策上图只 FETCH 已有点；无稳定码 skip。
硬闸：reload 路径无 hang/persist；禁止中文名当 VID；进度含 skipped_no_stable_id。
不做：publish 切面、analysis Job、假边凑 200。
commit：[agent:algorithm-agent]；push origin/dev。
```

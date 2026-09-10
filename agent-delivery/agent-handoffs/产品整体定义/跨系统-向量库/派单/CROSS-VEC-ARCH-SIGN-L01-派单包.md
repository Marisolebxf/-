# 派单包 · CROSS-VEC-ARCH-SIGN-L01

```yaml
task_id: CROSS-VEC-ARCH-SIGN-L01
dispatcher: agent:coordinator-agent
suggested_supervised_by: human:李伟
claim_type: coordinator_dispatch
date: 2026-09-10
status: backlog
ponytail: N/A
```

## 1. 为什么派

P1 连现网 Milvus 前须会签：共用实例、隔离 `amcpdp-*`、文本模型与 dim。另拍 **VEC-Q5**：Job A 是否进默认夜班、Job B 默认关。

## 2. 范围 / 不做

**做**：VEC-Q1 / Q1b / Q2 / **Q5** 书面结论。

**不做**：写 pymilvus；改 helm；改 `amcpdp-*`；实现 Job A（JOB-A 叶）。

## 3. /goal

```text
/goal architect-agent
身份：资深系统架构师；不写业务代码。
任务：CROSS-VEC-ARCH-SIGN-L01
依赖：CROSS-VEC-SAD-L01
必读：跨系统-向量库 01§2.1、02§3.2、03§0；architecture-baseline D12。
产出：会签纪要。冻结：文本 embedding ≠ amcpdp；collection 前缀不得用 amcpdp；
VEC-Q5：Job A 增量默认可调度、全量须审批；Job B 默认关。
禁止：采购第二套向量云（除非 Q1 改判）。
```

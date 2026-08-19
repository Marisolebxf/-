# SVC · seeds（覆盖矩阵骨架）

```yaml
---
doc_id: SVC-SEEDS-INDEX
element: SVC
role: source
status: draft
version: "2026-08-19"
updated: 2026-08-19
task_id: DATA-SVC-STORAGE-S2-L02
---
```

> 服务 Demo 全链路：**少量覆盖**，先闭环后性能。  
> 主管道：[`../etl/pipeline-demo-mock.md`](../etl/pipeline-demo-mock.md)  
> **本单不灌数。** fixture 24 家是旁路，底座退出门不认。

## 样本策略

| 原则 | 说明 |
|---|---|
| 真源 | 50100 灌数据按钮（F-SEED）；CLI/`svcseed` 同一引擎 |
| 旁路 | `seed_svc_demo_mock.py` 24 家 **不得**当退出门 |
| 待核验 | 圈定样例一律 Q-SVC-010，不伪闭合 live |

## 覆盖矩阵（骨架 · OPEN-SVC-FLOW-07）

| 场景 | 数据特点（须覆盖） | ODS/DWD 要点 | 入口 | 备注 |
|---|---|---|---|---|
| 圈定命中 | `name_cn` / `industry_l*_name` 关键词命中 ≥1 | `dwd_org_base_info` → SVC DWD hang `org_id` | F-SEED 50100 | 待核验 |
| 圈定过少 | 命中 &lt;10 走规则降级 / 诚实空态 | 同上 | F-SEED | 禁止伪池 |
| 基础指标 A1–A6 | 圈定后可汇总或诚实空 | SVC ADS（表名 S3） | F-SEED / 50100 basic | 不是十模型 |
| 图谱 hang | 节点能挂上 `org_id`↔`node_id` | `demo_gkx_chain` | F-ALGO | 不新建 space |
| 短板演示 | 0 / ≤1 / 均深&lt;55 | 模型结果表 S3 | F-ALGO | **Q-SVCCHAIN-03**；Q061 对照列 |
| fixture 24 家 | 固定名单 | 旁路写入 | `seed_svc_demo_mock.py` | **非退出门** |

S3 细表未建前，本矩阵只作验收场景清单，不填伪行数。

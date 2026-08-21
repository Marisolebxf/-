# POLICY · seeds（覆盖矩阵骨架）

```yaml
---
doc_id: POLICY-SEEDS-INDEX
element: POLICY
role: source
status: draft
version: "2026-08-21"
updated: 2026-08-21
task_id: DATA-POLICY-STORAGE-S2-L01
---
```

> **本单不灌数。** 模拟 ETL 五步（E0→L4）：[`../etl/pipeline-demo-mock.md`](../etl/pipeline-demo-mock.md)。SEED 主要覆盖 **E1 入 ODS** 与触发 **T2**。

## 覆盖矩阵（骨架）

| 场景 | 数据特点 | 入口 | 备注 |
|---|---|---|---|
| 底数 Mock | `calc_batch_id` 前缀 `mock_`；层级金字塔 | `run_all_policy` / 重建 | 历史 batch `mock_20260623` |
| ODS 攒货追加 | ODS 有、DWD 无的差集 | `POLICY-MOCK-INCR-L01` | 只做 E1；须再跑 T2→L3 |
| T+1 变更 | 水位 + `insert_remark` 0/1/2 + 删/史 | 见 `pipeline-demo-mock.md` T+1 | L3 快照重算；L4 只动 Δ 点边 |
| 图 hang | `pol:{policy_id}` + 四边；对不齐不上图 | B 叶 | `tech`/`talent` 本波不上图 |
| 空图 | ADS 镜像可读 | `/v1/policy/graph` | `source` 诚实 |

不填伪行数。细表 draft 见 [`../stores/`](../stores/README.md)。

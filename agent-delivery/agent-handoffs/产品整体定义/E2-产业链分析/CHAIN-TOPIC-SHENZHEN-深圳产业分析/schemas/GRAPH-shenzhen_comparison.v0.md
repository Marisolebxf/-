# GRAPH · shenzhen_comparison（深圳产业情况对比）v0

> **analysis_key**：`shenzhen_comparison`  
> **task_type**：`chain:shenzhen:shenzhen_comparison`  
> **graph_version**：`shenzhen_comparison.graph.v1`  
> **执行方**：Python Worker（`lumen-algo-py` `GRAPH_REGISTRY`）  
> **落地设计**：`DESIGN-LANDING-shenzhen_comparison.v0.md`  
> **同构**：`ISOMORPH-chain-analysis-jobs.v0.md` §3.4  
> **本文件**：DEMO-CHAIN-PY-JOB-SHENZHEN-L01 补声明（原 LANDING §13 待建）

---

## 流水线

```text
Execute → freeze → benchmark_ready_check → score_dimensions → narrative → validate_assemble → Complete
```

严格线性。厨房仍剥离 `result_snapshot_id`。**禁止**写入 `industry_chain_graph_snapshot`。  
**禁止**完成后自动跳转 / 自动跑 `shenzhen_development`。

| # | stage_code | LLM | Artifact |
| --- | --- | --- | --- |
| 1 | `freeze` | 否 | `art.context`（深圳固定 + 1 产业 + 1~5 就绪标杆 + 四维模型） |
| 2 | `benchmark_ready_check` | 否 | `art.ready_benchmarks` |
| 3 | `score_dimensions` | 否 | `art.score_bundle`（四维分开展示 + 矩阵标签 + judgment_fields） |
| 4 | `narrative` | 可选轻 | `art.narrative` |
| 5 | `validate_assemble` | 否 | `art.result_payload` |

**主体**：`subject_region.fixed=true` 且为深圳（`440300`）。  
**四维**：产业 / 专利 / 政策 / 人才；**禁止**产业与人才合并标签。  
**矩阵标签**：`领先` / `相当` / `落后`（UI「深圳处于 {label}」）。  
**硬失败**：无就绪标杆 `NO_BENCHMARK`；含 pending `BENCHMARK_NOT_READY`；主体非深圳 `INPUT_OBJECT_INVALID`。  
**降级**：narrative 失败不影响四维与矩阵。  
**诚实空**：Q056 / QC07 不得作四维分；权重 QC08 未闭合 → mock + `GAP-CHAIN-SZ-METRICS`。  
**下游**：`meta.may_feed_development=true`；`carry_to_development.source_result_id` 由 Java 签发，Python 不自签。

# GRAPH · regional_index（区域产业指数）v0

> **analysis_key**：`regional_index`  
> **task_type**：`chain:regional:index`  
> **graph_version**：`regional_index.graph.v1`  
> **执行方**：Python Worker（`lumen-algo-py` `GRAPH_REGISTRY`）  
> **落地设计**：`DESIGN-LANDING-regional_index.v0.md`  
> **同构**：`ISOMORPH-chain-analysis-jobs.v0.md` §3.3  
> **本文件**：DEMO-CHAIN-PY-JOB-REGIONAL-L01 补声明（原 LANDING §13 待建）

---

## 流水线

```text
Execute → freeze → load_base_scores → score → gap_explain → validate_assemble → Complete
```

严格线性。厨房仍剥离 `result_snapshot_id`。**禁止**写入 `industry_chain_graph_snapshot`。

| # | stage_code | LLM | Artifact |
| --- | --- | --- | --- |
| 1 | `freeze` | 否 | `art.context`（对象组合 + 模板/计入项/权重） |
| 2 | `load_base_scores` | 否 | `art.base_scores` |
| 3 | `score` | 否 | `art.score_bundle` |
| 4 | `gap_explain` | 可选轻 | `art.gap_text` |
| 5 | `validate_assemble` | 否 | `art.result_payload` |

**对象**：1 产业 × 1～5 区域，或 2～5 产业 × 1 区域；`maxObjects=5`；禁多×多。  
**四力**：产业力 / 创新力 / 学术力 / 支撑力（QC11 临时）。禁止与竞争力三维混用。  
**硬失败**：对象非法 / 超限 / 权重合计≠100 / 无一主体可打分。  
**降级**：LLM 失败用规则短板句；分数与排名不可假造。  
**诚实空**：Q056 / QC07 不得作分；缺底分 → `incomparable` 或 `BASE_SCORE_MISSING`。

# GRAPH · regional_competitiveness（区域竞争力）v0

> **analysis_key**：`regional_competitiveness`  
> **task_type**：`chain:regional:competitiveness`  
> **graph_version**：`regional_competitiveness.graph.v1`  
> **执行方**：Python Worker（`lumen-algo-py` `GRAPH_REGISTRY`，**独立菜谱，不与指数合并**）  
> **落地设计**：`DESIGN-LANDING-regional_competitiveness.v0.md`  
> **同构**：`ISOMORPH-chain-analysis-jobs.v0.md` §3.3  
> **本文件**：DEMO-CHAIN-PY-JOB-REGIONAL-L01 补声明（原 LANDING §13 待建）

---

## 流水线

```text
Execute → freeze → load_base_scores → score → gap_explain → validate_assemble → Complete
```

与指数共享**对象栏契约**，不继承对方模板/权重/四力。厨房剥离 `result_snapshot_id`。不写全景 snapshot。

| # | stage_code | LLM | Artifact |
| --- | --- | --- | --- |
| 1 | `freeze` | 否 | `art.context`（对象 + 三维权重=100%） |
| 2 | `load_base_scores` | 否 | `art.base_scores` |
| 3 | `score` | 否 | `art.score_bundle` |
| 4 | `gap_explain` | 可选轻 | `art.gap_text` |
| 5 | `validate_assemble` | 否 | `art.result_payload`（含 viz 同源） |

**三维钉死**：`industry_foundation` 产业基础 / `academic_ecology` 学术生态 / `innovation_ecology` 创新生态。  
**viz 同源**：`bar_ranking` / `heatmap_matrix` / `dimension_comparison` 均来自同一 `art.score_bundle`。  
**GIS**：仅 `multi-region` 且区域≥2；`multi-industry` 省略或 `skipped_reason`。  
**硬失败**：缺维、权重合计≠100、无一主体可合成。  
**禁止**：指数四力键混入权重。

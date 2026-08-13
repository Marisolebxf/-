# GRAPH · shenzhen_development（深圳产业发展分析）v0

> **analysis_key**：`shenzhen_development`  
> **task_type**：`chain:shenzhen:shenzhen_development`  
> **graph_version**：`shenzhen_development.graph.v1`  
> **执行方**：Python Worker（`lumen-algo-py` `GRAPH_REGISTRY`）  
> **落地设计**：`DESIGN-LANDING-shenzhen_development.v0.md`  
> **同构**：`ISOMORPH-chain-analysis-jobs.v0.md` §3.5  
> **上游**：`GRAPH-shenzhen_comparison.v0.md`  
> **本文件**：DEMO-CHAIN-PY-JOB-SHENZHEN-L01 补声明（原 LANDING §13 待建）

---

## 流水线

```text
Execute → freeze → load_source → path_generate → path_validate → validate_assemble → Complete
```

严格线性。厨房仍剥离 `result_snapshot_id`。**禁止**写入 `industry_chain_graph_snapshot`。  
Create / freeze **必须**显式 `source_result_id`；禁止静默继承最近一次对比。

| # | stage_code | LLM | Artifact |
| --- | --- | --- | --- |
| 1 | `freeze` | 否 | `art.context`（source 元数据 + goals 三键） |
| 2 | `load_source` | 否 | `art.source_snapshot` / `art.source_digest` |
| 3 | `path_generate` | **是（核心）** | `art.paths_draft` |
| 4 | `path_validate` | 规则 | `art.paths_validated` |
| 5 | `validate_assemble` | 否 | `art.result_payload` |

**硬失败**：

| 码 | 时机 |
| --- | --- |
| `SOURCE_REF_INVALID` | 缺 `source_result_id` / 非法源类型 / 静默继承键 |
| `GOALS_INCOMPLETE` | 政策/技术/人才目标缺省 |
| `SOURCE_LOAD_FAILED` | 无结构化对比快照（禁止空跑路径） |
| `SOURCE_INVALID` | PDF / 跨产业 |
| `PATH_COUNT_LT_2` | 路径 `<2`；**禁止**伪造补齐 |
| `PATH_NUMBER_INCONSISTENT` | 路径引用数字 ∉ 源快照 |

**LLM**：`llm_retry_max` 至少 2；`path_generate` HTTP timeout 120s。失败不编路径。  
**IC-36**：`honesty.case_library=unavailable`，不得声称 `matched`。  
**展开对比**：结果只提供抽屉元数据；URL tab 保持 `development`（前端职责）。

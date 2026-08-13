# schemas · 深圳产业决策 Job 契约

> 草稿：供 Runtime Result Snapshot、算法 assemble、前端结果页对齐。  
> 总索引：`../../INDEX-DESIGN-LANDING-7-analysis.md`

## 文件索引

| 文件 | 用途 |
| --- | --- |
| `DESIGN-LANDING-shenzhen_comparison.v0.md` | 情况对比落地设计（可喂发展） |
| `DESIGN-LANDING-shenzhen_development.v0.md` | 发展分析落地设计（硬依赖对比 Result） |
| `GRAPH-shenzhen_comparison.v0.md` | DEMO-CHAIN-PY-JOB-SHENZHEN-L01 补声明 |
| `GRAPH-shenzhen_development.v0.md` | DEMO-CHAIN-PY-JOB-SHENZHEN-L01 补声明 |
| `chain.*.schema.json` / Prompt Pack | 待按落地设计补齐（执行以 Python 注册表为准） |

## 注册键

| `analysis_key` | `task_type` | 路由 tab |
| --- | --- | --- |
| `shenzhen_comparison` | `chain:shenzhen:shenzhen_comparison` | `comparison` |
| `shenzhen_development` | `chain:shenzhen:shenzhen_development` | `development` |

## 跨键依赖

`shenzhen_development.Create` **必须**显式 `source_result_id` → `shenzhen_comparison` Result；禁止静默继承。

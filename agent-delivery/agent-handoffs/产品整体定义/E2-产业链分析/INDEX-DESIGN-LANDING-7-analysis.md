# INDEX · 七键「生成分析」落地设计

| 项 | 内容 |
| --- | --- |
| 日期 | 2026-08-12 |
| 作者 | `human:李伟` + architect-agent |
| 厨房真源 | `系统设计说明书-Analysis-Job-Runtime.v0.md` |
| 差量总表 | `ISOMORPH-chain-analysis-jobs.v0.md` |
| 口诀 | **不换厨房，只换菜谱** |

---

## 七键注册一览

| # | 工作空间 | Tab | `analysis_key` | `task_type` | 落地设计 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 产业运行诊断 | 关键环节 | `key_link` | `chain:diagnosis:key_link` | [DESIGN-LANDING-key_link.v0.md](./CHAIN-TOPIC-DIAGNOSIS-产业运行诊断/schemas/DESIGN-LANDING-key_link.v0.md) | ✅ 样板（GRAPH/Schema/Prompt 已齐） |
| 1 | 产业运行诊断 | 瓶颈堵点 | `bottleneck` | `chain:diagnosis:bottleneck` | [DESIGN-LANDING-bottleneck.v0.md](./CHAIN-TOPIC-DIAGNOSIS-产业运行诊断/schemas/DESIGN-LANDING-bottleneck.v0.md) | ✅ 设计收口；Schema/GRAPH 待建 |
| 2 | 产业运行诊断 | 产业周期 | `cycle` | `chain:diagnosis:cycle` | [DESIGN-LANDING-cycle.v0.md](./CHAIN-TOPIC-DIAGNOSIS-产业运行诊断/schemas/DESIGN-LANDING-cycle.v0.md) | ✅ v0.2；Schema/Prompt 待建 |
| 3 | 区域产业评价 | 指数 | `regional_index` | `chain:regional:index` | [DESIGN-LANDING-regional_index.v0.md](./CHAIN-TOPIC-REGIONAL-区域产业分析/schemas/DESIGN-LANDING-regional_index.v0.md) | ✅ 设计收口 |
| 4 | 区域产业评价 | 竞争力 | `regional_competitiveness` | `chain:regional:competitiveness` | [DESIGN-LANDING-regional_competitiveness.v0.md](./CHAIN-TOPIC-REGIONAL-区域产业分析/schemas/DESIGN-LANDING-regional_competitiveness.v0.md) | ✅ 设计收口 |
| 5 | 深圳产业决策 | 情况对比 | `shenzhen_comparison` | `chain:shenzhen:shenzhen_comparison` | [DESIGN-LANDING-shenzhen_comparison.v0.md](./CHAIN-TOPIC-SHENZHEN-深圳产业分析/schemas/DESIGN-LANDING-shenzhen_comparison.v0.md) | ✅ 设计收口 |
| 6 | 深圳产业决策 | 发展分析 | `shenzhen_development` | `chain:shenzhen:shenzhen_development` | [DESIGN-LANDING-shenzhen_development.v0.md](./CHAIN-TOPIC-SHENZHEN-深圳产业分析/schemas/DESIGN-LANDING-shenzhen_development.v0.md) | ✅ 设计收口；依赖 #5 |

> 全景图谱等工作区**不算**本表 Job（即时工作区，无「生成分析」状态机）。

---

## 建议实现顺序（同 ISOMORPH §4）

```text
key_link → bottleneck → regional_index → shenzhen_comparison
        → regional_competitiveness → cycle → shenzhen_development
```

每键最小工程包：`GRAPH-*.md` + input/result JSON Schema +（若有 LLM）Prompt Pack + OpenAPI draft/stage enum 补丁。

---

## 共性铁律（七键共用）

1. API：`POST/GET /topic/v1/analysis-jobs`（禁止各键私有 Create 路径）  
2. 互斥：同用户 + 同 `task_type` 一条非终态  
3. `succeeded` → **wait_view**；须显式「查看分析结果」  
4. 调用链：FE → Java → Python `/internal/*`  
5. LLM 不作布尔/分数/相位/排名的越权真源（各键 DESIGN-LANDING 细述）  
6. 可观测：全链路 `trace_id`  
7. 菜单 `workspace` 与 `tab` 等价时，深链以 `tab` 为准  

---

## 会签提示

各 `DESIGN-LANDING-*.v0.md` §14 会签栏仍须人签；本 INDEX 不替代单键会签。

# schemas · 关键环节 Result / Job 契约

> 草稿：供 Runtime Result Snapshot、算法 assemble、前端结果页对齐。  
> 不代表 PDR 冻结；口径变更走 TRACE + `schema_version` 升级。

## 文件索引

| 文件 | 用途 |
| --- | --- |
| `chain.key_link.chain_structure.v1.schema.json` + `.example.json` | 全链路五环节结构 |
| `chain.key_link.annotations.v1.schema.json` | 关键依据 |
| `chain.key_link.competition.v1.schema.json` | 竞争格局 |
| `chain.key_link.representative_enterprises.v1.schema.json` | 代表企业卡 |
| `chain.key_link.tech_trends.v1.schema.json` | 技术趋势 |
| `chain.key_link.summary.v1.schema.json` | 顶栏 KPI |
| `chain.key_link.result_payload.v1.schema.json` + `.example.json` | Complete.`result_payload` 总装（`$ref` 各 section） |
| `GRAPH-key_link.v0.md` | 五节点图 / Artifact / LLM 边界 |
| `PROMPT-PACK-key_link-n4c.v0.md` | N4c Prompt Pack（系统/用户模板、Loop、降级） |
| `SLICE-PLAN-key_link-S1-S5.v0.md` | S1～S5 谁先开工 / 角色并行 / DoD |
| `chain.key_link.n4c_context_pack.v1.schema.json` + `.example.json` | N4c Context Pack |
| `chain.key_link.n4c_llm_output.v1.schema.json` | N4c LLM 唯一输出形状 |
| `CONTRACT-Java-Python-Analysis-Job-v0.md` | Job 事件 / 错误码 / 轮询 |
| `openapi-analysis-job.v0.yaml` | OpenAPI（对外+投递+回调） |
| `../../ISOMORPH-chain-analysis-jobs.v0.md` | 七键同构扩展差量（周期/瓶颈/区域/深圳） |
| `../../系统设计说明书-Analysis-Job-Runtime.v0.md` | **总册**：§5.3 端到端运行时例子；§11 多场景步骤；Harness×Graph |

## 挂载位置

```text
Result Snapshot / Complete.result_payload
├─ result_title
├─ summary                    ← summary.v1
├─ sections
│  ├─ chain_structure         ← chain_structure.v1
│  ├─ annotations             ← annotations.v1
│  ├─ competition             ← competition.v1
│  ├─ representative_enterprises ← representative_enterprises.v1
│  └─ tech_trends             ← tech_trends.v1
├─ metrics_used[]
├─ evidence_refs[]
└─ honesty
```

## Schema 内 vs 实现侧校验

| 规则 | Schema | 实现侧（N5） |
| --- | --- | --- |
| 五环节齐全 | ✅ chain_structure | 集合相等 |
| is_key_node ↔ key_tag | ✅ | — |
| key_node_count === 关键数 | ❌ | ✅ |
| 每个关键有 annotation | ❌ | ✅ |
| annotation 数字 ⊆ 事实 | ❌ | ✅ |
| 格局/趋势可降级为空 | ✅ 允许空 | honesty.degraded |

## 本地校验（可选）

对单文件 example 用 Ajv / `jsonschema`；`result_payload` 总装需支持相对 `$ref`。

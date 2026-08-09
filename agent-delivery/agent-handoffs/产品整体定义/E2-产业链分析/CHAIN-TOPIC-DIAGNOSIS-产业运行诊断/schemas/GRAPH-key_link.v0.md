# GRAPH · key_link（关键环节识别）v0

> **analysis_key**：`key_link`  
> **task_type**：`chain:diagnosis:key_link`  
> **graph_version**：`key_link.graph.v1`（建议）  
> **版本保存**：字符串 ID + Python 注册表模块（Git）+ Job/Input Snapshot 落库字段；**不是**把本 md 或整段代码序列化进 DB。详见系统设计说明书 §11.3.1。  
> **执行方**：Python Worker（Java 只调度 + 存快照）  
> **过程文案真源**：Wireframe-CHAIN-TOPIC-DIAGNOSIS §5.1  
> **stage_code 真源**：`openapi-analysis-job.v0.yaml` → `KeyLinkStageCode`  
> **结构 Schema**：`chain.key_link.chain_structure.v1.schema.json`  
> **状态**：讨论草稿，公式/阈值未甲方确认处标 QC / GAP，不得伪闭合。

---

## 0. 入门：Graph 是什么

把「生成分析」看成一条**固定流水线**（不是开放式 Agent 自己规划）：

```text
Execute 入参（Input Snapshot）
   → N1 freeze
   → N2 structure
   → N3 score_high_end
   → N4 annotate（含有限 LLM）
   → N5 validate_assemble
   → Complete(result_payload)
```

每个节点：

1. 读上一节点的 **Artifact**（托盘）+ Input  
2. 做事（查库 / 算分 / LLM / 校验）  
3. `ReportStage`（started → succeeded|failed）  
4. 写出本节点 Artifact  

**稳定性原则**：数字与「是否关键」尽量在确定性节点产出；LLM 只做归纳叙述，且必须过校验。

---

## 1. 总览表

| # | stage_code | Bid 过程文案（可见） | 节点类型 | 是否 LLM | 主产出 Artifact |
| --- | --- | --- | --- | --- | --- |
| 1 | `freeze` | 任务提交与产业链对象冻结 | 校验 / 透传 | 否 | `art.context` |
| 2 | `structure` | 全链路环节结构化拆解（研发/设计/制造/销售/服务） | 查询 + 装配 | 否 | `art.chain_skeleton` |
| 3 | `score_high_end` | 基于附加值率、技术壁垒、市场集中度计算高端化指数 | 确定性计算 | 否 | `art.stage_scores` |
| 4 | `annotate` | 关键环节智能标注与竞争格局/代表企业/技术趋势归纳 | 规则判定 + 查询 + **可选 LLM** | 部分 | `art.annotations_bundle` |
| 5 | `validate_assemble` | 结果可信性校验与分析报告组装 | 校验 + 组装 | 否（可再拒 LLM） | `art.result_payload` → Complete |

图形态：**严格线性**。v1 不做并行分支；失败即 `Complete(failed)`，由 Harness 的 `llm_retry_max` 仅作用于 N4 内部小环。

---

## 2. 节点详解

### N1 · `freeze`

**目的**：确认执行侧看到的对象/因子/规则与 Input 一致，形成只读执行上下文。

| 项 | 内容 |
| --- | --- |
| 读 | Execute.body：`input_snapshot_id`、`input_payload`、`graph_version`、`limits` |
| 做 | 校验 `object.type=industry_chain`；`factors.user_confirmed=true`；因子三项 `status=ready`；`rules` 包可读；记录 `data_as_of` / 版本 |
| 写 `art.context` | `{ chain_id, parent_industry_id, factors[], rules, versions, honesty }` |
| ReportStage | `started` → `succeeded`（文案用 Bid 第 1 句） |
| 失败码 | `INPUT_OBJECT_INVALID` / `RULE_PACK_UNAVAILABLE` / `VALIDATION_*` 映射 |

**不做**：查 ADS、算指数、调 LLM。

---

### N2 · `structure`

**目的**：产出**完整五环节**骨架（禁止只返回关键节点）。

| 项 | 内容 |
| --- | --- |
| 读 | `art.context` |
| 做 | 按链拉环节主数据：五 `stage_key` 固定集合；填充 `label_zh`、`function_boundary`、`linkage_logic`、`enterprise_count`（可空）、默认 `edges` 四条 sequence |
| 数据源（示意） | ADS/DWD 链环节表、企业-环节归属；可复用现有 `/v1/chain/{id}/key-nodes` **底层查询函数**，但输出必须升格为五节点骨架，不能直接当最终 Result |
| 写 `art.chain_skeleton` | 符合 `chain_structure` 的 **stages+edges**，此时 `high_end_index` / `is_key_node` / `key_tag` 可暂缺或占位 `status=missing` |
| 失败 | 缺任一 stage_key → `ADS_UNAVAILABLE` 或 `SCHEMA_VALIDATION_FAILED` |

**验收锚点**：五环节齐全；边界与衔接非空串。

---

### N3 · `score_high_end`

**目的**：按注册因子算各环节**高端化指数**（确定性）。

| 项 | 内容 |
| --- | --- |
| 读 | `art.context.factors` + `art.chain_skeleton` + ADS 环节指标事实 |
| 做 | 对每个 stage：用附加值率 / 技术壁垒 / 市场集中度及**冻结权重**计算 `high_end_index`（MetricValue） |
| 公式状态 | 正式公式待口径闭合（`GAP-CHAIN-DIAG-METRICS`）；v0 可：`weighted_sum` 临时实现 + `status=mock` + `gap_ref` |
| 写 `art.stage_scores` | `{ stages: [{ stage_key, high_end_index, factor_raws? }] }` |
| **禁止** | LLM 改分数；前端改权重 |
| **并行（推荐）** | **节点内**并行拉三因子 / 按环节打分（`asyncio.gather` 等）；对外仍一对 `ReportStage(score_high_end)`。详见系统设计说明书 §9.1。**不要**拆成三个对外 stage 或三个 Job |

合并回骨架：把 `high_end_index` 写进各 stage（仍未打关键标签）。

---

### N4 · `annotate`（关键标注 + 格局/企业/趋势）

**目的**：在全链上下文中标关键，并补齐结果页叙述类区块。

建议拆成 **4a / 4b / 4c** 子步骤（同一 `stage_code=annotate`，对外只报一个阶段；子步失败算本阶段失败或降级，见下）。

#### 4a · 关键判定（确定性，必做）

| 项 | 内容 |
| --- | --- |
| 读 | `art.stage_scores` + `art.chain_skeleton.enterprise_count` + `art.context.rules` |
| 做 | 按 `rules.key_node_criterion`（如 QC02 临时默认 Top20% 企业数）判定 `is_key_node`；`key_tag`=`key_link` 或 `crown_jewel`（皇冠规则另表，未定则全部 `key_link`） |
| 写 | 更新 skeleton 上的 `is_key_node` / `key_tag`；`art.key_flags` |
| 依据 | 同步写 `annotations[].reason_codes/reason_text`（数字必须来自已算事实） |

**禁止**：LLM 决定谁是关键；禁止无证据补造关键。

#### 4b · 代表企业（查询，必做；可空列表）

| 项 | 内容 |
| --- | --- |
| 读 | 关键 stage + 企业库 |
| 做 | 每关键环节取 Top-N 代表企业；字段对齐全景关联企业卡 |
| 写 `art.enterprises` | `representative_enterprises.items[]` |
| 权限 | 无权限企业不入列表或锁态标记由 Java 展示层再裁；Worker 尽量出全量 ID |

#### 4c · 竞争格局 + 技术趋势（LLM 可选）

| 项 | 内容 |
| --- | --- |
| 读 | Context Pack（`chain.key_link.n4c_context_pack.v1`） |
| 做 | Prompt Pack `key_link.n4c.prompts.v1`（见 `PROMPT-PACK-key_link-n4c.v0.md`）；输出须过 `n4c_llm_output.v1` |
| Loop | Schema/事实冲突 → ≤ `llm_retry_max`；用尽则降级空叙述（推荐） |
| 降级 | `degraded=true`；禁止「已完成实时全网检索」 |
| 写 `art.narrative` | 映射为 `competition` + `tech_trends` section |

合并：`art.annotations_bundle` = key_flags + annotations + enterprises + narrative + 更新后的 chain_structure。

---

### N5 · `validate_assemble`

**目的**：不变量校验 + 组装 Complete 用的 `result_payload`。

| 校验（最低集） | 说明 |
| --- | --- |
| 五环节齐全且 stage_key 集合正确 | 对齐 chain_structure schema |
| `is_key_node` ↔ `key_tag` | schema if/then |
| `summary.key_node_count === count(is_key_node)` | 跨字段 |
| 每个关键有 annotation | 禁止无依据关键 |
| annotation 数字 ⊆ facts | 防 LLM 幻觉 |
| `honesty` / `metrics_used` / `input` 反查字段 | 齐备 |

| 项 | 内容 |
| --- | --- |
| 写 | `result_payload`：`result_title`、`summary`、`sections.*`、`metrics_used`、`evidence_refs`、`honesty`（Schema：`chain.key_link.result_payload.v1.schema.json`） |
| 成功 | `Complete(outcome=succeeded, result_payload=...)` |
| 失败 | `Complete(outcome=failed, error_code=SCHEMA_VALIDATION_FAILED\|LLM_FACT_CONFLICT\|…)` |

**不做**：再算一遍指数；改 Input。

---

## 3. Artifact 托盘一览

| Artifact | 产出节点 | 消费节点 | 备注 |
| --- | --- | --- | --- |
| `art.context` | N1 | N2–N5 | 执行期只读 |
| `art.chain_skeleton` | N2 | N3–N5 | 演进为完整 chain_structure |
| `art.stage_scores` | N3 | N4–N5 | 高端化指数 |
| `art.key_flags` | N4a | N4b/c、N5 | 关键布尔 |
| `art.enterprises` | N4b | N5 | |
| `art.narrative` | N4c | N5 | 可降级为空 |
| `art.annotations_bundle` | N4 | N5 | 汇总 |
| `art.result_payload` | N5 | Complete | 不含自造 result_snapshot_id |

节点间**只传 Artifact + context**，不把 LLM 原文当隐式状态。

---

## 4. Context Pack（给 N4c LLM 用）

规范文件：

- `chain.key_link.n4c_context_pack.v1.schema.json` + `.example.json`
- `PROMPT-PACK-key_link-n4c.v0.md`
- `chain.key_link.n4c_llm_output.v1.schema.json`

只允许放入：链名、五环节展示事实、已判定关键+依据、企业短名单、可选检索摘要、输出契约与禁止项。  
**不得**放入：整库企业、可编辑权重暗示、未授权明细。

---

## 5. 与 Job / 前端的接点

| Graph 动作 | Runtime |
| --- | --- |
| 节点开始/成功 | `ReportStage`（同一 stage_code） |
| N5 成功 | `Complete(succeeded)` → Java 签发 `result_snapshot_id` |
| 任节点不可恢复失败 | `Complete(failed)` + `failed_stage_code` |
| 超时 | Java `JOB_TIMEOUT`（Worker 被掐后应停） |

前端只看见 Bid 五句文案，不看见 4a/4b/4c。

---

## 6. 开放项（诚实）

| 编号 | 影响节点 | 临时策略 |
| --- | --- | --- |
| QC02 | N4a | Top20% 企业数；`rules.source=temp_default`；honesty 带 QC02 |
| GAP-CHAIN-DIAG-METRICS | N3 / summary | MetricValue `status=mock` + gap_ref |
| GAP-CHAIN-DIAG-SEMANTICS | N1 因子 | 只读确认，不伪编辑 |
| GAP-CHAIN-DIAG-API | N4c | 降级空叙述或固定回放 |

---

## 7. 实现切片建议（估工期用）

| 切片 | 范围 | 可演示 |
| --- | --- | --- |
| S1 | N1+N2+N5（固定五节点 mock 边界文案） | 过程五步 + 全链结构结果 |
| S2 | +N3 临时加权公式 | 带高端化指数 |
| S3 | +N4a 规则关键 | 关键标注 + KPI 计数一致 |
| S4 | +N4b 企业卡 | 抽屉/入篮 |
| S5 | +N4c LLM + Loop | 格局/趋势；可关降级 |

---

## 8. 修订

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v0 | 2026-08-09 | 关键五节点拆解；LLM 仅限 N4c；线性图 |
| v0.1 | 2026-08-09 | Result sections Schema：annotations / competition / enterprises / trends / summary / result_payload |
| v0.2 | 2026-08-09 | N4c Context Pack + Prompt Pack + LLM output schema |

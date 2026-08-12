# 落地设计 · 关键环节识别（`key_link`）v0

| 项 | 内容 |
| --- | --- |
| 文档版本 | v0.1-draft |
| 日期 | 2026-08-12 |
| 作者 | `human:李伟`（架构师）+ architect-agent |
| 状态 | **同构样板键**落地收口；实现以本文 + 已有 GRAPH / Schema / Prompt Pack 为准 |
| 样板角色 | 本键 = Analysis Job Runtime **基准菜谱**；其它六键按 ISOMORPH 同构扩展 |
| Bid | `1.1.1.2.4.2.2.4` 关键环节及相关算法 `.3.8` |
| 产品真源 | `CHAIN-TOPIC-DIAGNOSIS` 五件套（US-CHAIN-DIAG-03/04；IA §5.2；Wireframe §5） |
| Runtime 真源 | `../../系统设计说明书-Analysis-Job-Runtime.v0.md` |
| 同构差量 | `../../ISOMORPH-chain-analysis-jobs.v0.md` §0–§2 |
| 已有实现设计 | 同目录 `GRAPH-key_link.v0.md`、`PROMPT-PACK-key_link-n4c.v0.md`、`SLICE-PLAN-key_link-S1-S5.v0.md`、`CONTRACT-Java-Python-Analysis-Job-v0.md`、`openapi-analysis-job.v0.yaml`、`chain.key_link.*.schema.json` |

---

## 0. 一句话

> **厨房与菜谱都已齐**：复用 Analysis Job Runtime；本键定义 `analysis_key=key_link` 的 Input draft、五段 Graph、Result sections、N4c Prompt Pack。  
> 其它键只换对象 / 过程词 / Result 形状，**不换**状态机 / 互斥 / 快照 / `succeeded_wait_view`。

口诀：`chain:diagnosis:key_link` = 换对象（`industry_chain`）+ 确定性高端化打分 + **规则标关键、LLM 只叙述**。

### 0.1 命名纪律

| 术语 | 含义 | 禁止混用 |
| --- | --- | --- |
| `stage_code` | Graph 过程步（`freeze` / `structure` / …） | 不得表示业务「关键」布尔 |
| `stage_key` | 五环节业务键（研发/设计/制造/销售/服务） | 不得叫 `stage_code` |
| `is_key_node` / `key_tag` | 关键判定结果 | 不得由 LLM 裁定 |

---

## 1. 范围与非目标

### 1.1 本落地覆盖

| # | 交付物 | Owner |
| --- | --- | --- |
| A | 注册：`analysis_key` / `task_type` / 默认 `graph_version` | Java + Python |
| B | Create `draft` + 因子只读确认门禁 | FE + Java |
| C | Graph `key_link.graph.v1`（见 `GRAPH-key_link.v0.md`） | Python |
| D | Result schema 全套（已有） | Python + Java Complete |
| E | Prompt Pack `key_link.n4c.prompts.v1` | Python / 算法 |
| F | 前端 Tab=`key-link`：配置→过程→wait_view→结果 | FE |
| G | 切片 S1–S5（`SLICE-PLAN-key_link-S1-S5.v0.md`） | 全栈 |

### 1.2 明确不做（v0）

- 不改 Runtime 状态机 / OpenAPI 四段路径骨架
- 不新造关键私有 Create 路径（旧 `.../key-link/tasks` **废弃**）
- 不允许前端伪编辑权重/阈值
- 结果不得只返回关键节点截断全链
- 不把周期 / 瓶颈 / 门户 / 全景并进本 Job
- LLM **不得**决定 `is_key_node` 或改写高端化指数

---

## 2. 身份注册（钉死）

| 字段 | 值 |
| --- | --- |
| `analysis_key` | `key_link` |
| `task_type` | `chain:diagnosis:key_link` |
| `graph_version`（默认） | `key_link.graph.v1` |
| `input_schema_version` | `chain.key_link.input.v1` |
| `result_schema_version` | `chain.key_link.result_payload.v1` |
| `prompt_pack_version` | `key_link.n4c.prompts.v1` |
| 互斥 | 同用户 + 同 `task_type` 仅一条非终态；冲突 → `reused: true` |
| 路由（规范） | `/industry-center/diagnosis?tab=key-link` |
| 过程 | `...?tab=key-link&demo_state=processing&task_id=...` |
| 结果 | `...?tab=key-link&demo_state=result&task_id=...`（须显式「查看分析结果」） |
| 菜单兼容 | `DEC-CHAIN-DIAG-MENU-SPLIT`：`workspace=key_link` ≡ `tab=key-link` |

Java 默认图指针：

```text
DEFAULT_GRAPH_VERSION = {
  "key_link": "key_link.graph.v1",
  "cycle": "cycle.graph.v1",
  "bottleneck": "bottleneck.graph.v1",
  ...
}
```

可观测：Create 起签发/传递 `trace_id`，全链路携带。

---

## 3. 与其它诊断键的差量（本键 = 基准）

| 维度 | `key_link`（本键 / 样板） | `bottleneck` | `cycle` |
| --- | --- | --- | --- |
| 主对象 | **`industry_chain`** | 同左 | `industry` |
| 配置 | 三因子只读确认 | 五维只读确认 | 四参数可调 + time_range |
| 判定 | 高端化指数 + QC02 关键 | 健康度 + 瓶颈/卡脖子 | `cycle_phase` 规则+LLM |
| Result | 全链 + 关键标注 + 格局/企业/趋势 | 健康图谱 + 角标 | 回溯—诊断—预测 |
| LLM | 1 处（N4c） | 1 处（成因建议） | 2 处 |

Runtime / Harness / Snapshot / FE 过程壳：**✅ 直接复用**。

---

## 4. 端到端主路径

```text
用户：对比篮确认 industry_chain
  → Tab=key-link 只读确认三因子包
  → 点「生成分析」
      POST /topic/v1/analysis-jobs
      { task_type, analysis_key:"key_link", draft, client_request_id }
  → Java：校验对象=industry_chain · 因子 ready+confirmed · 互斥 · 冻 Input · 入队
  → Java → Python Execute(..., graph_version=key_link.graph.v1, trace_id, limits)
  → Python：N1→N5，每节点 ReportStage
  → Python Complete(result_payload) → Java Schema 门禁 → result_snapshot_id
  → 前端 GetJob：succeeded + allow_view_result；停 wait_view
  → 用户点「查看分析结果」→ GET analysis-results/{result_snapshot_id}
```

### 4.1 Create body 要点（示意）

```json
{
  "client_request_id": "uuid",
  "task_type": "chain:diagnosis:key_link",
  "analysis_key": "key_link",
  "draft": {
    "object": {
      "object_type": "industry_chain",
      "chain_id": "CHN-IC-001",
      "parent_industry_id": "INB1204",
      "display_name": "集成电路产业链"
    },
    "factors": {
      "pack_id": "diag_key_link_factors",
      "pack_version": "1.0.0",
      "user_confirmed": true,
      "items": [
        { "factor_key": "value_added_rate", "status": "ready" },
        { "factor_key": "tech_barrier", "status": "ready" },
        { "factor_key": "market_concentration", "status": "ready" }
      ]
    },
    "ui": {
      "route_path": "/industry-center/diagnosis",
      "tab": "key-link"
    }
  }
}
```

**Java Create 硬门禁**：

1. `object_type` 必须 `industry_chain`；拒绝 `industry`  
2. `factors.user_confirmed=true`；三项 `status=ready`  
3. 拒绝前端传入权重/阈值 override；拒绝前端 `graph_version`  
4. 同用户已有非终态本 `task_type` → 复用 `task_id`  

---

## 5. Graph · `key_link.graph.v1`

> 节点契约细节以 `GRAPH-key_link.v0.md` 为准；本节钉死注册与对外过程面。

| # | stage_code | Bid / IA 可见文案 | LLM？ | 主 Artifact |
| --- | --- | --- | --- | --- |
| 1 | `freeze` | 任务提交与产业链对象冻结 | 否 | `art.context` |
| 2 | `structure` | 全链路环节结构化拆解（研发/设计/制造/销售/服务） | 否 | `art.chain_skeleton` |
| 3 | `score_high_end` | 基于附加值率、技术壁垒、市场集中度计算高端化指数 | 否 | `art.stage_scores` |
| 4 | `annotate` | 关键环节智能标注与竞争格局/代表企业/技术趋势归纳 | **部分（4c）** | `art.annotations_bundle` |
| 5 | `validate_assemble` | 结果可信性校验与分析报告组装 | 否 | `art.result_payload` |

图形态：**严格线性**。N4 内 4a 规则关键 → 4b 代表企业 → 4c LLM 叙述（可降级）；对外只报一个 `annotate`。

```text
STAGE_LABELS = {
  "freeze": "任务提交与产业链对象冻结",
  "structure": "全链路环节结构化拆解（研发/设计/制造/销售/服务）",
  "score_high_end": "基于附加值率、技术壁垒、市场集中度计算高端化指数",
  "annotate": "关键环节智能标注与竞争格局/代表企业/技术趋势归纳",
  "validate_assemble": "结果可信性校验与分析报告组装",
}
```

**硬失败**：五环节缺一；因子未确认；规则包不可读。  
**降级继续**：N4c LLM / 检索叙述失败 → 空 `competition`/`tech_trends` + `honesty.degraded`；**4a 关键判定不可假成功**。

公式未闭合处：`GAP-CHAIN-DIAG-METRICS` → `MetricValue.status=mock` + `gap_ref`。关键阈值：**QC02** 临时 Top20% 企业数 + honesty 🟡。

---

## 6. Result Payload（不可变）

```text
result_schema_version: chain.key_link.result_payload.v1
result_title / summary
summary.key_node_count          # 顶栏：关键环节数（= count(is_key_node)）
summary.concentration_index?    # 可选
sections:
  chain_structure
  annotations
  competition                   # 可 degraded
  representative_enterprises
  tech_trends                   # 可 degraded
metrics_used[] / evidence_refs[] / honesty / versions / object
```

### Complete 不变量（最低集）

1. 五 `stage_key` 齐全，不得截断为仅关键节点  
2. `is_key_node` ↔ `key_tag` 一致  
3. `summary.key_node_count === count(is_key_node=true)`  
4. 每个关键节点有对应 `annotations`；数字 ⊆ 已算事实  
5. `object.object_type=industry_chain` 与 Input 一致  
6. 展示用统计数字带 `metric_id`  

---

## 7. Prompt / Context Pack

| Pack ID | 节点 | 职责 | 降级 |
| --- | --- | --- | --- |
| `key_link.n4c.prompts.v1` | N4c | 竞争格局 + 技术趋势 | 空 section + degraded；不拖垮 Job |

禁止：LLM 输出改写 `is_key_node` / `high_end_index`；禁止「已完成实时全网检索」假标记。

---

## 8. 配置与数据依赖

| 依赖 | 缺失策略 |
| --- | --- |
| 链主数据 + 五环节 | Create/N2 **硬失败** |
| 三因子 ADS 事实 | N3 mock + gap_ref（METRICS 未闭合时） |
| 企业库 | 代表企业可空列表 |
| LLM / 检索 | N4c **降级** |

开放项：QC02、GAP-CHAIN-DIAG-METRICS、GAP-CHAIN-DIAG-SEMANTICS、GAP-CHAIN-DIAG-API。

---

## 9. 分层职责

| 层 | 做 | 不做 |
| --- | --- | --- |
| FE | 因子只读确认；Create；轮询；wait_view；结果五区块 | 直连 Python/LLM；本地算关键 |
| Java | jobs / 互斥 / Snapshot / Complete 门禁 / trace | 高端化算法；调 LLM |
| Python | `key_link.graph.v1` + N4c | 自造 result_snapshot_id；管互斥 |

调用链：**FE → Java → Python `/internal/*`**。

---

## 10. 切片交付

以 `SLICE-PLAN-key_link-S1-S5.v0.md` 为准：S1 竖切 → S2 结构 → S3 打分 → S4 关键 → S5 叙述/企业。

---

## 11. 验收 DoD

- [ ] 仅 `industry_chain` 可提交；因子未确认禁用生成  
- [ ] 五段 Bid 文案推进；succeeded 停 wait_view  
- [ ] 结果含完整五环节；关键数与角标一致  
- [ ] LLM 失败仍有规则关键；格局/趋势可诚实降级  
- [ ] 算法只在 Python；未分叉私有 Create 路径  

---

## 12. 已收口决策

| ID | 决策 |
| --- | --- |
| K1 | 本键为七键 Runtime **样板**；其它键不得另起状态机 |
| K2 | 关键真值 = 规则；LLM 仅 N4c 叙述 |
| K3 | 父文「技术含量」映射因子键 = **技术壁垒** |
| K4 | QC02 / METRICS 标 gap，不挡 S1–S3 编码 |
| K5 | 统一 `/topic/v1/analysis-jobs` |

---

## 13. 产物清单

| 文件 | 状态 |
| --- | --- |
| `DESIGN-LANDING-key_link.v0.md` | **本文件** |
| `GRAPH-key_link.v0.md` | ✅ |
| `PROMPT-PACK-key_link-n4c.v0.md` | ✅ |
| `SLICE-PLAN-key_link-S1-S5.v0.md` | ✅ |
| `chain.key_link.*.schema.json` | ✅ |
| `openapi-analysis-job.v0.yaml` | ✅（样板枚举） |
| `chain.key_link.input.v1.schema.json` | 若缺则补齐与 §4.1 对齐 |

---

## 14. 会签栏

| 角色 | 签字 | 日期 |
| --- | --- | --- |
| 架构师 `human:李伟` | | |
| 架构 Lead `human:徐滕强` | | |
| 体验 Owner `human:高颖` | | |
| PM `human:郭万迎` | | |
| 算法代表 | | |

*实现以 Git 中 Python 注册表与 JSON Schema 为准；本 md 不参与解释执行。*

# 落地设计 · 产业周期分析（`cycle`）v0

| 项 | 内容 |
| --- | --- |
| 文档版本 | v0.2-draft（相对 v0.1：收口 P0/P1 矛盾项，可按本文实现） |
| 日期 | 2026-08-11 |
| 作者 | `human:李伟`（架构师）+ architect-agent |
| 状态 | 落地设计收口稿；实现以本文 + JSON Schema / Python 注册表为准；会签栏仍须人签 |
| 样板依赖 | Runtime 样板键仍为 `key_link`；本键按 ISOMORPH **同构扩展** |
| Bid | `1.1.1.2.4.2.2.2 产业周期分析` |
| 产品真源 | `CHAIN-TOPIC-DIAGNOSIS` 五件套（US-CHAIN-DIAG-01/02；IA §5.1；TRACE cycle） |
| Runtime 真源 | `../../系统设计说明书-Analysis-Job-Runtime.v0.md` |
| 同构差量 | `../../ISOMORPH-chain-analysis-jobs.v0.md` §3.1 |
| 关键样板对照 | 同目录 `GRAPH-key_link.v0.md`、`CONTRACT-Java-Python-Analysis-Job-v0.md` |

---

## 0. 一句话

> **不换厨房，只换菜谱**：复用 Analysis Job Runtime（Java 外层 Harness + Python Graph Runner + 前端过程壳）；  
> 本键只新增 `analysis_key=cycle` 的 Input draft、五段 Graph、Result sections、两处 LLM Prompt Pack。

口诀：`chain:diagnosis:cycle` = 换对象（`industry`）+ 换过程词 + **规则判相、LLM 解释**；Job 状态机 / 互斥 / 快照 / `succeeded_wait_view` **一字不改**。

### 0.1 命名纪律（全篇强制）

| 术语 | 含义 | 禁止混用 |
| --- | --- | --- |
| `stage_code` | Graph **过程步**编码（`freeze` / `retrieve` / …） | 不得表示产业生命周期相位 |
| `cycle_phase` | 业务 **周期相位**编码（`introduction` / `growth` / `maturity` / `decline`） | 不得叫 `stage_code` |
| `cycle_phase_label` | 相位中文：导入 / 成长 / 成熟 / 衰退 | UI KPI 用此 |

---

## 1. 范围与非目标

### 1.1 本落地覆盖

| # | 交付物 | Owner 建议 |
| --- | --- | --- |
| A | 注册：`analysis_key` / `task_type` / 默认 `graph_version` | Java + Python |
| B | Create `draft` shape + 校验规则 | FE + Java |
| C | Graph `cycle.graph.v1`（五节点 + Artifact） | Python（设计稿本文件 §5） |
| D | Result schema `chain.cycle.result_payload.v1` | Python + Java Complete 门禁 |
| E | Prompt Pack：`diagnose_stage` + `forecast` | Python / 算法 |
| F | 前端 Tab=`cycle`：配置 → 过程 → wait_view → 结果「回溯—诊断—预测」 | FE |
| G | 切片计划 S1–S5（本文件 §10） | 全栈 |

### 1.2 明确不做（v0）

- 不改 Runtime 状态机 / OpenAPI 四段路径骨架（仍走 `/topic/v1/analysis-jobs`）
- 不新造「周期专用」Create 路径（FUNC-DESIGN 里旧示意 `.../cycle/tasks` **废弃**，统一 Job API）
- 不做用户可配置「如何联网」控制台
- 结果顶栏不挂「阶段评分 / 技术成熟度」数值卡（DEC-HIDE-CYCLE-SCORE-KPIS）
- 不在本键消费 `industry_chain` / `chain_id`
- 不把门户总览 / 全景图谱并进本 Job
- v0 **不**引入独立预测模型服务；预测序列 = 基于 N2 历史的确定性外推（见 §5.3 N4）

---

## 2. 身份注册（钉死）

| 字段 | 值 |
| --- | --- |
| `analysis_key` | `cycle` |
| `task_type` | `chain:diagnosis:cycle` |
| `graph_version`（默认） | `cycle.graph.v1` |
| `input_schema_version` | `chain.cycle.input.v1` |
| `result_schema_version` | `chain.cycle.result_payload.v1` |
| 互斥 | 同用户 + 同 `task_type` 仅一条非终态；冲突 → `reused: true` 恢复原任务 |
| 路由（规范） | `/industry-center/diagnosis?tab=cycle` |
| 过程 | `...?tab=cycle&demo_state=processing&task_id=...` |
| 结果 | `...?tab=cycle&demo_state=result&task_id=...`（须显式「查看分析结果」） |
| 菜单兼容 | `DEC-CHAIN-DIAG-MENU-SPLIT`：`workspace=cycle` 与 `tab=cycle` 等价指向本键；深链以 `tab` 为准，`workspace` 仅导航壳 |

Java 默认图指针（与 key_link 并列）：

```text
DEFAULT_GRAPH_VERSION = {
  "key_link": "key_link.graph.v1",
  "cycle":    "cycle.graph.v1",
}
```

可观测：Create 起签发/传递 `trace_id`，Execute / ReportStage / Complete 全链路携带（与 Runtime / CONTRACT 一致）。

---

## 3. 与关键样板的差量（必读）

| 维度 | `key_link`（样板） | `cycle`（本键） |
| --- | --- | --- |
| 主对象 | `industry_chain` | **`industry`（单选）** |
| 配置 | 三因子只读确认 | **四参数可调** + **分析时间范围** + 参数来源 honesty |
| 判定 | 高端化指数等确定性计算 | **规则/特征产出 `cycle_phase`**；LLM 解释与候选集内确认 |
| 检索 | 可选/证据 | **过程必现「联网检索」能力词**；V1 可回放快照降级 |
| 结果结构 | 五环节 + 关键标注 | **回溯 — 诊断 — 预测** |
| KPI 顶栏 | 关键相关 | **仅「当前周期相位 / 相位判定」**；禁止阶段评分卡 |
| Prompt Pack | 1 处（n4c） | **2 处**（diagnose 解释 + forecast 归纳） |
| limits | 样板默认 | **加长 LLM/Job 超时**（见 §5.5） |

Runtime / Harness / Snapshot 信封 / FE 过程壳：**✅ 直接复用**。

---

## 4. 端到端主路径（落地时序）

对齐 Runtime §5.3，仅替换键与对象：

```text
用户：产业查询/对比篮确认 industry
  → Tab=cycle 调四参数 + time_range
  → 点「生成分析」
      POST /topic/v1/analysis-jobs
      { task_type, analysis_key:"cycle", draft, client_request_id }
  → Java：校验对象类型=industry · 互斥 · 冻 Input Snapshot · 入队
  → Java → Python Execute(input_snapshot_id, graph_version=cycle.graph.v1, trace_id, limits)
  → Python：N1→N5，每节点 ReportStage
  → Python Complete(result_payload) → Java Schema 门禁 → 签发 result_snapshot_id
  → 前端 GetJob：status=succeeded, allow_view_result=true
      ※ 停在 succeeded_wait_view，禁止自动进结果
  → 用户点「查看分析结果」
      GET /topic/v1/analysis-results/{result_snapshot_id}
  → （可选）生成报告：只读 Result，不重跑分析
```

### 4.1 Create body 要点（示意）

```json
{
  "client_request_id": "uuid",
  "task_type": "chain:diagnosis:cycle",
  "analysis_key": "cycle",
  "draft": {
    "object": {
      "object_type": "industry",
      "object_id": "INB1204",
      "display_name": "集成电路"
    },
    "params": {
      "market_size": {
        "value": 1250.6,
        "unit": "亿元",
        "source": "ads_prefill",
        "ads_value": 1250.6,
        "user_overridden": false
      },
      "growth_rate": {
        "value": 8.3,
        "unit": "%",
        "source": "user_override",
        "ads_value": 7.1,
        "user_overridden": true
      },
      "profit_margin": {
        "value": 12.1,
        "unit": "%",
        "source": "ads_prefill",
        "ads_value": 12.1,
        "user_overridden": false
      },
      "tech_maturity": {
        "value": 72.5,
        "unit": "分",
        "scale": "0-100",
        "source": "user_input",
        "ads_value": null,
        "user_overridden": false
      }
    },
    "time_range": {
      "start": "2018-01-01",
      "end": "2026-06-30",
      "grain": "year"
    },
    "ui": {
      "route_path": "/industry-center/diagnosis",
      "tab": "cycle"
    }
  }
}
```

**参数 `source` 枚举（钉死）**：`ads_prefill` | `user_override` | `user_input`。  
- 有 ADS 预填且用户改值 → 必须 `user_override`，并保留 `ads_value`。  
- 无 ADS 预填、用户手填 → `user_input`，`ads_value=null`。  
Java Create 时校验：`user_overridden=true` 当且仅当 `source=user_override`。

**Java Create 校验（硬门禁）**：

1. `object_type` 必须 `industry`；拒绝 `industry_chain`  
2. 四参数均在注册合法区间（§8.1）；越界 400  
3. `time_range.start < end`；`grain ∈ {year, quarter}`  
4. 不接受前端传入任意 `graph_version`（仅服务端默认）  
5. 同用户已有非终态 `chain:diagnosis:cycle` → 复用该 `task_id`  
6. 每个 param 必须带合法 `source`；`user_override` 必须带非 null `ads_value`

---

## 5. Graph · `cycle.graph.v1`

### 5.1 总览（过程 Steps = Bid 词汇面）

| # | stage_code | Bid / IA 可见文案 | 节点类型 | LLM？ | 主产出 Artifact |
| --- | --- | --- | --- | --- | --- |
| 1 | `freeze` | 任务提交与参数冻结 | 校验 / 透传 | 否 | `art.context` |
| 2 | `retrieve` | 整合产业参数与联网检索的历史与市场数据 | 查询 + 检索装配 | 否 | `art.retrieval_bundle` |
| 3 | `diagnose_stage` | 大语言模型推理与周期阶段判断（诊断） | **规则判相 + LLM 解释** | **是（解释）** | `art.phase_diagnosis` |
| 4 | `forecast` | 基于全网检索动态归纳趋势预测、关键驱动因素与潜在拐点 | 确定性外推 + **LLM 归纳** | **是（归纳）** | `art.forecast_bundle` |
| 5 | `validate_assemble` | 结果可信性校验与分析报告组装 | 校验 + 组装 | 否 | `art.result_payload` |

图形态：**严格线性**。节点内允许并行拉数（Runtime §9.1）；**不做图级分叉**。

### 5.2 过程标签表（ReportStage / 前端 Steps）

```text
STAGE_LABELS = {
  "freeze": "任务提交与参数冻结",
  "retrieve": "整合产业参数与联网检索的历史与市场数据",
  "diagnose_stage": "大语言模型推理与周期阶段判断（诊断）",
  "forecast": "基于全网检索动态归纳趋势预测、关键驱动因素与潜在拐点",
  "validate_assemble": "结果可信性校验与分析报告组装",
}
```

禁止改成企业评估文案（「企业数据汇聚」等）。过程文案可含「大语言模型」以满足 Bid 词汇面；**相位真值不由 LLM 单独裁定**（见 N3）。

### 5.3 节点契约

#### N1 · `freeze`

| 项 | 内容 |
| --- | --- |
| 读 | Execute `input_payload`（= Input Snapshot） |
| 做 | 核对 object/params/time_range/versions；生成只读 `art.context`；写入参数来源 honesty 种子 |
| 写 | `art.context`：`industry_id`、params（含 source/ads_value）、time_range、rule_pack_version、`honesty.params` |
| 失败 | `OBJECT_INVALID` / `PARAM_OUT_OF_RANGE` / `SNAPSHOT_MISMATCH` / `PARAM_SOURCE_INVALID` |

`honesty.params`：若任一项 `source=user_override`，则 `overridden=true` 且列出键名；供结果页诚实条。

#### N2 · `retrieve`

| 项 | 内容 |
| --- | --- |
| 读 | `art.context` |
| 做 | 拉 ADS **主序列**（至少覆盖配置 `time_range` 的市场规模或注册主指标时序）+ 检索事件包 + 可选对标候选 |
| 写 | `art.retrieval_bundle`：`series_hist[]`（**唯一历史序列真源**）、`retrieval_events[]`、`peer_candidates[]`、`honesty.retrieval` |
| 降级铁律 | 检索未接通：`honesty.retrieval.mode = replay_snapshot`；**禁止**「已完成实时全网检索」 |
| **硬失败** | 主序列缺失、为空、或无法覆盖 `time_range` → `ADS_SERIES_UNAVAILABLE`（**不可**标 gap 后继续） |
| **降级继续** | 仅检索旁路缺失：`honesty.retrieval.mode ∈ {replay_snapshot, unavailable}`，仍进入 N3 |

#### N3 · `diagnose_stage`（规则判相 + LLM 解释）

**主路径（钉死）**：

```text
1) 规则/特征（params + series_hist）→ candidates[]（非空，含 phase + score）
2) 取规则主选 primary_phase = argmax(score)
3) Context + Prompt Pack cycle.diagnose.v1 → LLM
   - 输入：candidates、primary_phase、序列摘要、检索摘录（可空）、params
   - 输出：confirmed_phase ∈ candidates.phase 白名单；rationale；evidence_ids；confidence
4) 若 LLM 成功且 confirmed_phase ∈ candidates → 采用 confirmed_phase
5) 若 LLM 失败/越权/校验失败（Loop 耗尽）→ 采用 primary_phase，honesty.llm = degraded
```

| 项 | 内容 |
| --- | --- |
| 读 | `art.context` + `art.retrieval_bundle` |
| 相位枚举 | `cycle_phase ∈ {introduction, growth, maturity, decline}`；中文：导入/成长/成熟/衰退（算法卡若更名，升 `rule_pack_version`，不改本字段语义集合除非升 graph） |
| 写 | `art.phase_diagnosis`：见下表 |
| **禁止** | LLM 编造检索证据；LLM 输出不在 candidates 内的相位 |
| **硬失败** | 仅当 `art.context` / `series_hist` 损坏导致规则无法产出非空 candidates → `PHASE_RULE_INPUT_INVALID` |
| **不硬失败** | LLM 失败 → 规则主选 + `honesty.llm=degraded` 后继续 N4 |

`art.phase_diagnosis` 字段：

| 字段 | 说明 |
| --- | --- |
| `cycle_phase` | 最终相位（规则主选或 LLM 在白名单内确认） |
| `cycle_phase_label` | 中文标签 |
| `phase_source` | `rule_primary` \| `llm_confirmed` \| `rule_fallback_after_llm` |
| `candidates` | 规则候选列表 |
| `rationale` | 解释（LLM 或规则模板） |
| `evidence_refs` | 只引用 N2 已有 id，禁止新生伪证据 |
| `confidence` | 0–1 |
| `param_echo` | 回显冻结参数（含 source） |
| `honesty.llm` | `ok` \| `degraded` \| `skipped` |

#### N4 · `forecast`（确定性外推 + LLM 归纳）

**序列真源（钉死）**：

- `series_hist`：**只复制** N2 `series_hist`，禁止重拉、禁止改写历史点  
- `series_forecast` + `ci_low` / `ci_high`：v0 **仅**确定性外推（规则包版本 `forecast_rule_pack_version`）；**不**调用独立预测模型服务  
- 独立预测模型 → 未来 `cycle.graph.v2`，不在 v1 混入  

**LLM 职责**：只归纳 `drivers[]`、`turning_points[]`、`decision_brief`；不得改写 hist/forecast 数值点。

| 项 | 内容 |
| --- | --- |
| 读 | 上序全部 Artifact |
| 写 | `art.forecast_bundle`：`series_hist`、`series_forecast`、`ci_low`、`ci_high`、`drivers[]`、`turning_points[]`、`decision_brief`、`honesty.forecast` |
| 降级 | LLM 归纳失败 → drivers/turning_points 可空列表 + `honesty.llm=degraded`；外推仍可成功 |
| **硬失败** | `series_hist` 缺失（理论上 N2 已拦）→ `FORECAST_INPUT_MISSING` |
| 外推失败 | 无法生成任何 forecast 点 → `series_forecast=[]` + `honesty.forecast=degraded`，**允许**继续 N5（结果页展示「预测不可用」） |

#### N5 · `validate_assemble`

| 项 | 内容 |
| --- | --- |
| 读 | 全部 Artifact |
| 做 | 按 §6.3 不变量组装 `result_payload`；执行 §5.6 字段映射 |
| 写 | `art.result_payload` → `Complete(succeeded, …)` |
| 双检 | Python N5 + Java Complete **同一套** schema / 不变量 |

### 5.4 Python 注册表示意

```python
# graphs/cycle_v1.py
NODES = [
    ("freeze", freeze.run),
    ("retrieve", retrieve.run),
    ("diagnose_stage", diagnose_stage.run),
    ("forecast", forecast.run),
    ("validate_assemble", validate_assemble.run),
]

GRAPH_REGISTRY["cycle.graph.v1"] = NODES
```

运行时**只查注册表**；本 md **不参与解释执行**（Runtime §11.3.1）。

### 5.5 Harness limits（相对 key_link 加严超时）

Execute `limits` 建议默认（实现可配置，但不得低于）：

| 项 | cycle.v1 默认 | 说明 |
| --- | --- | --- |
| `llm_retry_max` | 2（每 LLM 节点） | N3、N4 各自计数 |
| `node_timeout_sec`（diagnose_stage / forecast） | ≥ 120 | 含 Loop |
| `node_timeout_sec`（其余） | ≥ 60 | |
| `job_timeout_sec` | ≥ 600 | Java 外层超时 failed |

---

## 6. Result Payload（不可变）

### 6.1 顶层形状（钉死）

```text
result_schema_version: chain.cycle.result_payload.v1
result_title
summary
kpi:
  current_phase_label          # 顶栏：周期相位中文
  phase_judgment               # 顶栏：判定短句
sections:
  backtrace                    # 参数/时间窗/关键历史点/参数来源
  diagnosis                    # cycle_phase + candidates + phase_source + rationale + evidence
  forecast                     # 内含 series_hist / series_forecast / ci_* / drivers / turning_points
  retrieval_events
  peer_comparison              # QC10；无则空 + honesty
  decision_brief
metrics_used[]
evidence_refs[]
honesty                        # params / retrieval / llm / forecast / data_gap
versions                       # graph / prompt_packs / rule_pack / forecast_rule_pack / data_as_of
object                         # object_type=industry, object_id（与 Input 一致）
```

**section 冻结**：`drivers` / `turning_points` **嵌在** `sections.forecast` 内，**不**再与 forecast 并列顶层 section（修正 v0.1 与 ISOMORPH 示意不一致）。

### 6.2 结果页绑定（产品）

| UI 区块 | 字段路径 |
| --- | --- |
| 顶栏 KPI | `kpi.current_phase_label` + `kpi.phase_judgment` |
| 回溯 | `sections.backtrace` |
| 诊断 | `sections.diagnosis` |
| 预测（图） | `sections.forecast.series_*` / `ci_*` |
| 驱动 / 拐点 | `sections.forecast.drivers` / `sections.forecast.turning_points` |
| 决策摘要 | `sections.decision_brief` |
| 诚实条 | `honesty` + `versions` |
| 禁止 | 顶栏 `stage_score` / `tech_maturity` KPI 卡 |

结构口号：**回溯 — 诊断 — 预测**。

### 6.3 Complete 不变量（Java + Python 双检）

1. `object.object_type=industry` 且 `object_id` 与 Input 一致  
2. `kpi.current_phase_label` 非空，且与 `sections.diagnosis.cycle_phase` 的中文映射一致  
3. `sections.diagnosis.cycle_phase ∈ {introduction,growth,maturity,decline}`  
4. `sections.diagnosis.candidates` 非空；`cycle_phase` 必须 ∈ `candidates[].phase`  
5. `sections.forecast.series_hist` 与 N2/Input 冻结时间窗一致（点序、不得被 LLM 改写）  
6. 若 `series_forecast` 非空：与 hist 时间轴不重叠；逐点 `ci_low ≤ value ≤ ci_high`（若该点有 ci）  
7. `honesty.retrieval.mode ∈ {live, replay_snapshot, unavailable}`；禁止「live + 假完成」文案标记  
8. 任一 param `source=user_override` ⇒ `honesty.params.overridden=true`  
9. 禁止结果顶栏字段：`stage_score_kpi`、`tech_maturity_kpi`  
10. `metrics_used` 中每个**展示用统计数字**有 `metric_id`（用户覆盖参数在 backtrace 展示，并标 source，不伪装 ADS 正式口径）

### 6.4 Artifact → Result 映射表（实现对照）

| Artifact 路径 | Result 路径 |
| --- | --- |
| `art.context.industry_id` | `object.object_id` |
| `art.context.params` | `sections.backtrace.params` |
| `art.context.honesty.params` | `honesty.params` |
| `art.retrieval_bundle.series_hist` | `sections.forecast.series_hist` |
| `art.retrieval_bundle.retrieval_events` | `sections.retrieval_events` |
| `art.retrieval_bundle.peer_candidates` | `sections.peer_comparison`（可空） |
| `art.retrieval_bundle.honesty.retrieval` | `honesty.retrieval` |
| `art.phase_diagnosis.cycle_phase` | `sections.diagnosis.cycle_phase` |
| `art.phase_diagnosis.cycle_phase_label` | `kpi.current_phase_label` |
| `art.phase_diagnosis.candidates` | `sections.diagnosis.candidates`（Complete 校验用，须落库） |
| `art.phase_diagnosis.rationale` | `sections.diagnosis.rationale` + 派生 `kpi.phase_judgment` |
| `art.phase_diagnosis.phase_source` | `sections.diagnosis.phase_source` |
| `art.phase_diagnosis.honesty.llm` | `honesty.llm.diagnose` |
| `art.forecast_bundle.series_forecast` 等 | `sections.forecast.*` |
| `art.forecast_bundle.drivers` | `sections.forecast.drivers` |
| `art.forecast_bundle.turning_points` | `sections.forecast.turning_points` |
| `art.forecast_bundle.decision_brief` | `sections.decision_brief` |
| `art.forecast_bundle.honesty.*` | `honesty.forecast` / `honesty.llm.forecast` |

---

## 7. Prompt / Context Pack

| Pack ID | 节点 | 输入 Context 要点 | Output Schema 要点 |
| --- | --- | --- | --- |
| `cycle.diagnose.v1` | N3 | candidates、primary_phase、params、序列摘要、检索摘录 | `confirmed_phase`∈candidates；rationale；evidence_ids；confidence |
| `cycle.forecast.v1` | N4 | 已定 `cycle_phase`、hist/forecast 摘要（只读）、检索摘录 | drivers[]；turning_points[]；decision_brief（**禁止**输出改写序列点） |

规则：

- Pack 版本写入 `versions.prompt_packs`  
- Loop 仅节点内；受 §5.5 `llm_retry_max`  
- 校验失败 → 重试 → 降级；**禁止**开放 ReAct 规划  
- 升 Prompt 文案一般不升 `graph_version`；改候选规则/外推公式升 `rule_pack_version` / `forecast_rule_pack_version`

配套文件（实现前补齐）：

- `PROMPT-PACK-cycle-diagnose.v0.md`  
- `PROMPT-PACK-cycle-forecast.v0.md`  
- `chain.cycle.input.v1.schema.json`  
- `chain.cycle.result_payload.v1.schema.json`  
- `GRAPH-cycle.v0.md`（可由 §5 抽出）

---

## 8. 配置参数与数据依赖

### 8.1 四参数（提交冻结）

| 参数键 | 中文 | v0 校验 | 备注 |
| --- | --- | --- | --- |
| `market_size` | 市场规模 | >0 | 可 ADS 预填；改值必须 `user_override` |
| `growth_rate` | 增长率 | [-50, 200]，单位 % | 同上 |
| `profit_margin` | 利润率 | [-100, 100]，单位 % | 同上 |
| `tech_maturity` | 技术成熟度 | [0, 100] | 配置区可保留；**结果顶栏不展示** |

区间为团队默认，算法卡确认后只改配置表 / `rule_pack_version`，不改 Create 字段名。

### 8.2 数据依赖（执行侧）

| 依赖 | 用途 | 缺失策略（钉死） |
| --- | --- | --- |
| 产业主数据（INB） | 对象合法 | Create **硬失败** |
| ADS 产业主序列 | N2/N4 hist | N2 **硬失败** `ADS_SERIES_UNAVAILABLE` |
| 检索服务 / 回放快照 | N2 能力词 | **降级继续** + honesty |
| LLM 网关 | N3/N4 | **降级继续**（规则主选 / 空归纳） |
| 对标样本（QC10） | peer_comparison | 空 section + honesty；**不挡**主路径 |

开放项（不挡 S1–S2 编码，结果标 gap）：QC03 周期口径细项、QC10 对标全集、正式联网检索、`GAP-CHAIN-DIAG-API`。

---

## 9. 分层职责（派工边界）

| 层 | 做 | 不做 |
| --- | --- | --- |
| **前端** | Tab=cycle 配置校验；Create；轮询；wait_view；显式看结果；诚实条；参数 override 标记 | 直连 Python/LLM；自造 stage；自动跳结果；顶栏评分卡；本地算相位 |
| **Java** | analysis-jobs；互斥；Snapshot；Stage；Complete schema；超时；`trace_id` | 周期相位算法；调 LLM；签发前改业务 payload |
| **Python** | `cycle.graph.v1`；规则判相；外推；Prompt；ReportStage/Complete | 自造 `result_snapshot_id`；管用户互斥 |
| **报告** | 只读 Result → ENT-EXPORT | 报告内重跑分析 |

调用链：**FE → Java → Python `/internal/*`**。

---

## 10. 切片交付（S1–S5）

| Slice | 目标 | 可验出口 | 依赖 |
| --- | --- | --- | --- |
| **S1** | 注册 + Create/Get 空跑 | 对象类型门禁；互斥 reuse；五段文案可展示 | Runtime 厨房（key_link 已通更佳） |
| **S2** | N1+N2 | 无主序列硬失败；检索降级 honesty；无假「实时完成」 | ADS 或 fixture 主序列 |
| **S3** | N3 | 无 LLM 时仍有稳定 `cycle_phase`；LLM 越权被拒 | rule_pack + diagnose pack |
| **S4** | N4+N5 + Result | hist 不被改写；forecast 嵌套 drivers/拐点；不变量双检 | forecast schema |
| **S5** | 记录 + 报告入口 | 同 `result_snapshot_id` 恢复；报告只读 | SYS-JOBS / EXPORT |

排期：key_link Runtime 未绿时，周期可并行草稿 Schema；**S2+ 必须挂同一厨房**。

---

## 11. 验收 DoD

### 11.1 产品 / 体验

- [ ] 仅 `industry` 可提交；无对象时「生成分析」禁用  
- [ ] 点「生成分析」才建任务；过程五段含 Bid 原文能力词  
- [ ] `succeeded` 停 wait_view；须显式「查看分析结果」  
- [ ] 结果为回溯—诊断—预测；顶栏无阶段评分/技术成熟度 KPI  
- [ ] V1 检索未接通时诚实降级可见  
- [ ] 用户覆盖参数在回溯区可见，不伪装 ADS 正式口径  

### 11.2 架构铁律

- [ ] 算法只在 Python；FE/Java 不直连 LLM  
- [ ] Snapshot ID 所有权符合 CONTRACT  
- [ ] `cycle_phase` 真值可追溯至规则候选；LLM 不可越权  
- [ ] 无 ADS 主序列不得伪成功  
- [ ] `graph_version` / schemas / prompt_packs / rule packs / `trace_id` 可追溯  

### 11.3 同构纪律

- [ ] 未分叉私有 Create 路径  
- [ ] 未把 cycle 做成同步 `GET /v1/chain/**`  
- [ ] 未与 key_link/bottleneck 合并 `task_type`  

---

## 12. 已收口决策（原 R*）

| ID | 决策（v0.2 冻结） |
| --- | --- |
| R1 | 相位枚举：`introduction/growth/maturity/decline` ↔ 导入/成长/成熟/衰退；算法卡更名走 `rule_pack_version` |
| R2 | 检索缺失 → **降级继续**；**ADS 主序列缺失 → 硬失败**（二者不得混用） |
| R3 | LLM 失败 → **规则主选兜底成功** + `honesty.llm=degraded`；不因 LLM 单独 hard fail |
| R4 | 四参数可预填可改；提交快照为准；override 必须带 `ads_value` + honesty |
| R5 | 废弃周期私有 API，统一 `/topic/v1/analysis-jobs` |
| R6 | QC03/QC10 标 gap，不挡 S1–S2 |
| R7 | 预测序列 v1 = 确定性外推；独立模型留 v2 |
| R8 | `turning_points`/`drivers` 嵌在 `sections.forecast` |
| R9 | 过程步用 `stage_code`，业务相位用 `cycle_phase` |

仍须人签（§14），但不阻塞按本文编码。

---

## 13. 产物清单

落在 `CHAIN-TOPIC-DIAGNOSIS-产业运行诊断/schemas/`：

| 文件 | 状态 |
| --- | --- |
| `DESIGN-LANDING-cycle.v0.md` | **本文件 v0.2** |
| `GRAPH-cycle.v0.md` | 待从 §5 抽出 |
| `chain.cycle.input.v1.schema.json` | 待建（须含 params.source） |
| `chain.cycle.result_payload.v1.schema.json` | 待建（须含 §6.1） |
| `PROMPT-PACK-cycle-diagnose.v0.md` | 待建 |
| `PROMPT-PACK-cycle-forecast.v0.md` | 待建 |
| `openapi-analysis-job.v0.yaml` | 补丁：`CycleProcessStageCode` 与 `CyclePhaseCode` **分枚举** |

工程仓：

| 仓 | 落点 |
| --- | --- |
| `lumen-svc-platform` | 注册 `cycle`；Complete 校验 §6.3 |
| 算法仓 | `graphs/cycle_v1.py` + rule/forecast packs + prompt packs |
| topic UI | diagnosis `tab=cycle` 接线 Job API |

---

## 14. 会签栏

| 角色 | 签字 | 日期 |
| --- | --- | --- |
| 架构师 `human:李伟` | | |
| 架构 Lead `human:徐滕强` | | |
| 体验 Owner `human:高颖` | | |
| PM `human:郭万迎` | | |
| 算法代表 | | |

---

## 15. 自检记录（v0.2）

对照 v0.1 审查项：

| 原问题 | v0.2 处理 |
| --- | --- |
| N3 过重依赖 LLM | 改为规则候选 + LLM 白名单确认 |
| N3 失败策略矛盾 | 统一兜底成功；仅规则输入坏 hard fail |
| ADS vs 检索策略混 | 主序列硬失败 / 检索降级，分列钉死 |
| 参数覆盖无 honesty | Create 强制 source/ads_value；不变量 #8 |
| stage 命名混 | `stage_code` vs `cycle_phase` |
| Artifact→Result 映射缺失 | §6.4 表 |
| N4 序列真源未选 | hist=N2；forecast=确定性外推 |
| turning_points 位置 | 嵌 forecast |
| LLM limits 缺失 | §5.5 |
| trace / workspace | §2 补齐 |

*实现以 Git 中 Python 注册表与 JSON Schema 为准；本 md 不参与解释执行。*

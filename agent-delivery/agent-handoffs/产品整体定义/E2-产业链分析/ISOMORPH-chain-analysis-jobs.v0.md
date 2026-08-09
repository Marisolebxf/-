# ISOMORPH · 「生成分析」同构扩展差量 v0

> **目的**：以已跑通的 **关键环节 `key_link`** 为样板，列出周期 / 瓶颈 / 区域 / 深圳各自「复用什么、新写什么」。  
> **不改**：Runtime 状态机、Python 回调、OpenAPI 四段+读接口骨架、`succeeded_wait_view`、Input/Result Snapshot 信封。  
> **状态**：讨论差量清单，不是各键完整 Graph/Schema 定稿。

---

## 0. 入门：什么叫「同构」

同构 = **换菜谱，不换厨房**：

| 层 | 同构复用（一套） | 每 analysis_key 特化 |
| --- | --- | --- |
| Job / SYS-JOBS | Create·Get·Events·Withdraw·Execute·Stage·Complete | `task_type` / `analysis_key` 字符串 |
| 前端壳 | 配置→过程→wait_view→结果→记录 | Tab 路由、过程文案、结果区块组件 |
| Snapshot 信封 | honesty / versions / ui / schema_version | `draft` 与 `result_payload.sections` |
| Graph 形态 | 线性节点 + ReportStage + N 末校验组装 | 节点内容、是否 LLM、Artifact；**节点内**可并行算子（见系统设计说明书 §9.1） |
| Prompt | Pack 版本化 + Context/Output Schema + Loop/降级 | 仅含 LLM 的键才需要 |

**已完成样板（关键）**：CONTRACT + OpenAPI + GRAPH + Result sections + N4c Prompt Pack。  
其它键 = 复制目录约定，改差量表中的「新写」列。

---

## 1. analysis_key 注册表（建议）

| 工作空间 | Tab | `analysis_key` | `task_type` |
| --- | --- | --- | --- |
| 产业运行诊断 | 产业周期 | `cycle` | `chain:diagnosis:cycle` |
| 产业运行诊断 | 关键环节 | `key_link` ✅ 样板 | `chain:diagnosis:key_link` |
| 产业运行诊断 | 瓶颈堵点 | `bottleneck` | `chain:diagnosis:bottleneck` |
| 区域产业评价 | 指数 | `regional_index` | `chain:regional:index` |
| 区域产业评价 | 竞争力 | `regional_competitiveness` | `chain:regional:competitiveness` |
| 深圳产业决策 | 情况对比 | `shenzhen_comparison` | `chain:shenzhen:shenzhen_comparison` |
| 深圳产业决策 | 发展分析 | `shenzhen_development` | `chain:shenzhen:shenzhen_development` |

互斥粒度：已定 **同用户 + 同 `task_type`**（每 Tab 一条非终态）。

---

## 2. 总差量矩阵（相对 key_link）

图例：✅ 直接复用｜🔧 适配少量｜🆕 基本新写｜— 不需要

| 资产 | cycle | bottleneck | regional_index | regional_competitiveness | shenzhen_comparison | shenzhen_development |
| --- | --- | --- | --- | --- | --- | --- |
| OpenAPI 路径/状态机 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Create `draft` shape | 🆕 | 🔧 | 🆕 | 🔧 | 🆕 | 🆕 |
| Graph + stage_code 枚举 | 🆕 | 🆕 | 🆕 | 🔧 | 🆕 | 🆕 |
| Result sections Schema | 🆕 | 🆕 | 🆕 | 🔧 | 🆕 | 🆕 |
| Prompt / Context Pack | 🆕（重） | 🔧（归因） | —/轻 | —/轻 | 轻 | 🆕（重） |
| 主对象类型 | `industry` | `industry_chain` | industry×region | 同左 | industry+标杆 | +`source_result_id` |
| 开放项压力 | QC03/QC10/检索 | QC04/词汇分层 | QC05/QC11 | 同左 | QC08 等 | 依赖对比结果 |

---

## 3. 分键差量（只写「和关键不同」）

### 3.1 `cycle`（产业周期）

**主对象**：`industry`（不依赖链；配置区链字段只读占位）。

**过程五段（Wireframe §4.1）→ 建议 stage_code**：

| # | stage_code（建议） | 文案要点 | LLM？ |
| --- | --- | --- | --- |
| 1 | `freeze` | 参数+**分析时间范围**冻结 | 否 |
| 2 | `retrieve` | 整合参数与检索历史/市场 | 否（检索） |
| 3 | `diagnose_stage` | 周期阶段判断 | **是（核心）** |
| 4 | `forecast` | 趋势/驱动/拐点归纳 | **是** |
| 5 | `validate_assemble` | 校验组装 | 否 |

**Create draft 新字段**：可调四参数、`time_range`（提交冻结）。

**Result 新 sections（示意）**：`backtrace` / `diagnosis` / `forecast`（含序列+置信带+拐点）/ `drivers` / `retrieval_events` / `peer_comparison`（QC10 系统对标）。

**相对关键**：

- 🆕 Prompt Pack 至少两处（阶段判断 + 预测归纳）；检索降级铁律同关键。  
- 🆕 趋势图数据结构（历史/预测/ciLow/ciHigh）。  
- 🔧 复用 Job/轮询/wait_view/诚实 honesty。

---

### 3.2 `bottleneck`（瓶颈堵点）

**主对象**：`industry_chain`（与关键同）。

**过程五段（Wireframe §6.1）→ 建议 stage_code**：

| # | stage_code（建议） | 文案要点 | LLM？ |
| --- | --- | --- | --- |
| 1 | `freeze` | 对象+五维只读确认（维名**资本**） | 否 |
| 2 | `timeseries` | 整合技术/人才/资本/政策等时序 | 否 |
| 3 | `score_health` | 四核心指标→环节健康度 | 否（确定性） |
| 4 | `annotate_bottleneck` | 瓶颈/卡脖子判定 + 成因建议 | 判定规则 + **建议可 LLM** |
| 5 | `validate_assemble` | 校验组装 | 否 |

**Create draft**：五维只读包版本（不可伪编辑阈值）。

**Result sections（示意）**：`health_graph`（五节点+分档+角标）/ `kpis`（瓶颈数、严重度、类型分布、卡脖子数⊆瓶颈）/ `node_details`（成因清单）/ 禁「断链」。

**相对关键**：

- 🔧 同五环节骨架思路，但指标是健康度不是高端化；角标分层已有产品决策。  
- 🆕 词汇分层校验（稳健/关注/薄弱 vs 瓶颈/卡脖子）。  
- 🔧 Prompt 仅用于成因/改进建议清单（类似 N4c，可降级）。

---

### 3.3 `regional_index` / `regional_competitiveness`

**主对象**：产业 × 区域组合；指数含**模板/权重工作集**快照。

**过程（产品偏计算，阶段可压缩为 4～5）建议**：

| # | stage_code | 指数 | 竞争力 | LLM？ |
| --- | --- | --- | --- | --- |
| 1 | `freeze` | 对象+模板+权重快照 | 三维权重=100% | 否 |
| 2 | `load_base_scores` | 底分就绪校验 | 同/简化 | 否 |
| 3 | `score` | 加权重算排名 | 三维合成 | 否 |
| 4 | `gap_explain` | 优劣短板（可选叙述） | 同 | 可选轻 LLM |
| 5 | `validate_assemble` | 组装 | 组装 | 否 |

**相对关键**：

- 🆕 draft：模板 id/version、计入项、权重；竞争力：三维权重合计校验。  
- 🆕 Result：四力/排名表/叶子贡献（指数）；短板列表（竞争力）。  
- — 默认可无重 Prompt；即时汇总已在配置区，Job 出**不可变正式结果**。  
- 开放项：QC05/QC11。

---

### 3.4 `shenzhen_comparison`

**主对象**：固定深圳 + 1～5 就绪标杆。

**过程建议**：

| # | stage_code | 要点 | LLM？ |
| --- | --- | --- | --- |
| 1 | `freeze` | 标杆列表+四维模型只读确认 | 否 |
| 2 | `benchmark_ready_check` | 就绪门禁（创建门已做，执行再校验） | 否 |
| 3 | `score_dimensions` | 四维对比计算 | 否 |
| 4 | `narrative`（可选） | 对比解读 | 轻 LLM |
| 5 | `validate_assemble` | 组装 | 否 |

**相对关键**：🆕 标杆多选 draft；Result=四维对比表；少 LLM。

---

### 3.5 `shenzhen_development`（依赖最特殊）

**硬依赖**：Create 必须带有效 **`source_result_id`**（同产业兼容的对比 Result）；禁止静默继承。

**过程建议**：

| # | stage_code | 要点 | LLM？ |
| --- | --- | --- | --- |
| 1 | `freeze` | 绑定 source 对比快照 + 政策/技术/人才目标 | 否 |
| 2 | `load_source` | 加载对比 Result（只读） | 否 |
| 3 | `path_generate` | ≥2 套发展路径 | **是（核心）** |
| 4 | `path_validate` | 路径完整度/与对比数字一致 | 规则+校验 |
| 5 | `validate_assemble` | 组装 | 否 |

**相对关键**：

- 🆕 Prompt Pack（路径生成）权重大，类似周期。  
- 🆕 Input 必含 `source_result_id`；Create 校验 `source_invalid`。  
- 🔧 仍复用 Job/回调/wait_view。

---

## 4. 建议落地顺序（估工期）

| 序 | 键 | 理由 |
| --- | --- | --- |
| 0 | `key_link` | ✅ 样板已齐 |
| 1 | `bottleneck` | 同对象类型、同五环节骨架，差在健康/角标 |
| 2 | `regional_index` | 计算型、少 LLM，验证「正式结果 vs 配置即时汇总」 |
| 3 | `shenzhen_comparison` | 计算型 + 标杆门禁 |
| 4 | `regional_competitiveness` | 指数同构变体 |
| 5 | `cycle` | 检索+双 LLM，复杂 |
| 6 | `shenzhen_development` | 依赖对比 Result + 路径 LLM |

每键最小交付包（复制关键目录约定）：

```text
GRAPH-{key}.v0.md
OpenAPI：仅扩展 draft/stage_code enum（或分文件 components）
Result：{key}.result_payload.v1.schema.json（+ sections）
若有 LLM：PROMPT-PACK-{key}-….v0.md + context/output schema
```

**不必**为每键复制一整份 OpenAPI 路径；路径共用，靠 `analysis_key` + `oneOf` draft 区分。

---

## 5. 明确不要重复造的

1. 第二套任务状态机 / 第二套浮层  
2. 前端直连 Python  
3. 成功后自动跳结果  
4. 把参数拼进 `task_type`  
5. 报告任务重跑分析  
6. 用 LLM 当指数/健康分/关键或瓶颈布尔的真源（叙述除外）

---

## 6. 修订

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v0 | 2026-08-09 | 七键注册 + 相对 key_link 差量 + 建议落地序 |

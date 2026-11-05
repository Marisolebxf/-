# SYNTH L2 · 协同册 — 区域创新协同分析（ARCH/DATA/API/METRIC 合并册）

- 日期：2026-11-05（v1.0.4：不可变 snapshotId 含 calc_batch_id；与 cache_key 分离）
- 状态：**DRAFT，待四方会签**；图谱真值 **blocked 待 Q-SYNTH-C-05 贴源**（预填 gapfill 演示行可先行）
- 上游：总册 §2.3/§11（v1.0-draft）；需求真源 SRS 139–141；模型叶 `M_SYNTH_191_1`
- 现状衔接：FE COLLAB 三页已联调中（`LUMEN-INTEL-FE-COLLAB`）；**页面差距见 §6**（产业筛选控件缺失、图谱独立查询接口缺失），不是"已备不改"。

## 1. ARCH（流程与落点）

```text
lumen-ui-topic 协同三页（在途，差距见 §6）
  → gateway → topic 快照 / topic-async 任务 / 图谱查询（新增）
  → GET /topic/v1/synth/collaboration/batch-snapshot
  → GET /topic/v1/synth/collaboration/graph   ← 139 独立图谱查询（本册新增）
  → POST /topicAsync/topic/v1/analysis/tasks（协同任务键）
  → entan-py 装包
       指标结果：读 gkxlumenx_ai.synth_collab_{index,network_stat,relation_input,output_corr,cluster}
       图事实：  读 gkxlumenx_gapfill.gapfill_synth_collab_{node,edge}
                 （预填演示行；C-05 贴源/Nebula 导出就绪后 D16 换源停读）
```

- 密度上游可用 `M_SYNTH_191_1`（已有 SPEC）；`collabIndex` 不得用 191 返回值冒充。
- Java 不写 nGQL；Nebula 导出只在 Python。
- 样本 <3：不出系数、不画散点；「密度×强度」禁当权威公式。

## 2. DATA（每表四项；`_ai` 5 张 + gapfill 2 张）

公共列/批次规则总册 §11.2（含 `calc_batch_created_at` 排序、唯一键强制含 region+compare+window）。

**`_ai` 指标结果表（5，含 cluster 口径挂靠）**

| 表 | 业务粒度（一行=） | 唯一键（基础=region+compare+window+batch） | 写入 | 读批 |
|---|---|---|---|---|
| `synth_collab_index` | 基础键 | 基础键 | 实算/预填整批 | succeeded 最新批（按 `calc_batch_created_at`）单行 |
| `synth_collab_network_stat` | 基础 × stat | `+ (stat_type)` | 同上 | 同批 3 行 |
| `synth_collab_relation_input` | 基础 × 关系类型 | `+ (relation_type)` | 同上 | 同批 3 行 |
| `synth_collab_output_corr` | 基础 × X 指标（index/density/centrality）× 年度配对窗口（**calc-logic 正式口径：区域固定、按年组样本，不做跨区域截面**） | `+ (x_metric_id, output_metric_id, period_start, period_end)`；列含 `r_value`/`sample_n`/`status(sufficient\|insufficient)`/`reason` | Pearson；**n<3 存为合法 `insufficient` 行（正常结果，非失败、非 failed 批）**；双侧方差=0 同 insufficient | 同批 N 行；全缺 → 效果区空态 |
| `synth_collab_cluster` | 基础 × 主体（cluster/isolate 归属） | `+ (entity_type, entity_id)` | 装包派生写入；**口径挂靠** `M_SYNTH_COLLAB_COMPLETENESS` 公式「含孤立节点」+ C-02 判据，表 COMMENT 登记派生源 | 同批 N 行；空 → clusters=[] |

**策略建议（141③）：无表，LLM 实时生成（v0.3）**

- 装包时以结构化结果（集群/孤立/相关性/网络统计）拼**证据 prompt** → `entan/common/llm_client.py`（GLM，Secret `gkx-zhipu-llm`）；失败/未配 → `degraded: strategies=[] + reason`（`narrative.py` SWOT 同款模式）。
- 诚实性：只基于本次计算事实，禁止编造；页面保留「AI 生成·待审核」Tag（Q-SYNTH-C-04 临时默认）。
- 不建表、不折 JSON；待 C-04 正式口径闭合后如需持久化另走 METRIC-OPEN 同批裁定。

**gapfill 图事实表（2，D16；预填=演示行，真值换源）**

| 表 | 粒度/唯一键（**含完整条件上下文**） | D16 登记明细 | 预填/换源 | 血缘 |
|---|---|---|---|---|
| `gapfill_synth_collab_node` | 一行=主体×条件×**服务指标**（同一主体行按消费指标各一行，行级血缘） | `uk(region_code, compare_scope, window_label, metric_id, entity_type, entity_id, gapfill_batch_id)`；稳定 ID=源侧 id | 每行 `metric_id` 单值，**灌数清单五码必齐**：`M_SYNTH_COLLAB_RELATION_INPUT`（**canonical，图谱只读此码**）+ `M_SYNTH_COLLAB_COMPLETENESS` / `CENTRALITY` / `DENSITY` / `INDEX`（指标计算消费）；缺 canonical 行＝图谱空图，验收失败。`gap_item`=cooperation_node_missing；`fill_method`=llm/manual；必填列=`metric_id`/`gap_item`/`fill_method`/`fill_model`(llm时)/`gapfill_batch_id`/`generated_at`（D16 标准，不用 `calc_batch_id`）；读路径=`entan-py` 装包/图谱 | 预填演示行；C-05 贴源/Nebula 导出就绪后**停读换源** | 预填=fill_method 记录；换源后=Nebula space+导出任务 |
| `gapfill_synth_collab_edge` | 一行=边×条件×**服务指标**（同边按消费指标各一行） | `uk(region_code, compare_scope, window_label, metric_id, src_id, dst_id, relation_type, year, gapfill_batch_id)` | 每行 `metric_id` 单值，**同上五码必齐**（含 `RELATION_INPUT`）；`gap_item`=cooperation_edge_missing；其余列同 node | 同五码内按边键合并、权重累加去重 | 同上 |

> **灌读一致性铁律**：写什么才能读什么。图谱 canonical=`M_SYNTH_COLLAB_RELATION_INPUT`；预填/换源脚本与 seed **必须写入该码行**，不得只灌 COMPLETENESS/CENTRALITY/DENSITY/INDEX 四码。

## 3. API

### 3.1 快照与任务

- `GET /topic/v1/synth/collaboration/batch-snapshot?region=&compare=&window=` → `CollabResult`；404 非默认三元组；缺数据 200+null/reason。
- 任务：`region_innovation_collaboration`（`POST /topicAsync/topic/v1/analysis/tasks`）；Java `SynthAnalysisAdapter` → Python `POST /internal/v1/synth/jobs/execute`，入参 `{task_id, leaf:'collaboration', region, compare, window}`（窗归一中文）；失败 → 任务 `failed`+`reason`。
- 五阶段文案逐字用 MOCK-INV §2 协同行。

**批次映射持久化（废止 COMMENT / 内存 batch_link）**

同一 Job 或预计算快照**成功发布**时，必须把映射写入**可持久、可跨进程读取**的结果元数据（二选一或同时写，优先都写）：

1. **快照响应 / 预计算快照存储**的顶层字段 `batch_meta`（随 snapshot 持久化，重启可查）  
2. **异步任务**成功时的 `#105 resultData.batch_meta`（与 LeafResult 同存）

`batch_meta` 最小字段（缺任一则视为发布失败，不得标 succeeded）：

| 字段 | 说明 |
|---|---|
| `snapshotId` | **不可变**本批快照 ID：`snap:{calc_batch_id}` 或唯一快照记录 ID（禁止仅条件三段） |
| `calc_batch_id` | `_ai` 指标结果批 |
| `graph_source` | `gapfill` \| `nebula_export`（换源后改值） |
| `gapfill_batch_id` | 图事实批（`graph_source=gapfill` 时必填；换源后填导出批号或等价批键） |
| `region` / `compare` / `window` | 条件上下文（与请求归一一致） |
| `published_at` | 发布时间 |

另维护 **`cache_key = region|compare|window`**（稳定查询键）→ 指向「该条件下最新成功 `snapshotId`」；同条件重跑成功后索引改指新 ID，**旧 `snapshotId` 与其 `batch_meta` 不得被覆盖删除**（至少保留可回查窗口，与总册批次保留策略对齐）。

禁止：仅写表 COMMENT、仅进程内存 map、仅日志。COMMENT 只做血缘说明，**不承载**多批次映射。

### 3.2 图谱查询接口（139，独立精确契约）

- **URL / 方法**：`GET /topic/v1/synth/collaboration/graph`（网关 → `gkxlumen-topic` → Python `GET /internal/v1/synth/collaboration/graph`）
- **执行分工**：前端只传参；**服务端（Python）执行筛选、截断、聚合**；Java 仅透传。换源后同函数换数据源。
- **批次选择**：
  1. 传 `snapshotId` → **只**从该快照持久化的 `batch_meta`（或任务 resultData 中同 `snapshotId` 的 meta）解析 `gapfill_batch_id` / 图源批，**只读该批**；
  2. 传显式 `gapfill_batch_id`（无 snapshotId）→ 只读该批；若同时传 `snapshotId` 则必须与 meta 一致，否则 **400**；
  3. **指定了 `snapshotId` 但找不到持久映射 / meta 缺图批字段** → 返回 **不可用**（`nodes=[]` + `reason='batch_meta_missing'` 或 HTTP 404/`code!=0` 约定一种并写死），**禁止**回落到「条件最新图批」；
  4. **仅当未传 `snapshotId` 且未传 `gapfill_batch_id`**（调试/预览）→ 才允许在 `region+compare+window` 下取最新可用图批，并在响应回显所用批次；
  5. 工作台从快照进图谱 **必须带 `snapshotId`**。
- **去重（canonical 读取规则）**：node/edge 按服务指标多行存；图谱展示**只读 `metric_id='M_SYNTH_COLLAB_RELATION_INPUT'`**（`WHERE metric_id='M_SYNTH_COLLAB_RELATION_INPUT'`），同一主体/边只返回一份；其余四码行仅供指标计算，不进图谱响应。canonical 常量写死在装包，注释登记。
- **请求参数**：

| 参数 | 类型/取值 | 必填 | 执行方 | 说明 |
|---|---|---|---|---|
| `region` | 区域编码 | 是 | Python | 与 UK `region_code` 对齐 |
| `compare` | 对比范围编码 | 是 | Python | 与 UK `compare_scope` 对齐；缺省不默改 |
| `window` | `1y/3y/5y` | 是 | Python | 边年份闭区间；与 UK `window_label` 对齐 |
| `snapshotId` | 快照 ID | 否* | Python | 优先；从持久化 `batch_meta` 解析图批 |
| `gapfill_batch_id` | gapfill 批次号 | 否* | Python | 无 snapshot 时显式绑定；与 snapshot 同传须一致，否则 400 |
| `industry` | 产业领域编码（专题库一级分类，C-05 🟡） | 否 | Python（服务端过滤，非前端） | 节点产业标签过滤；缺省=全部 |
| `entity_types` | `enterprise/institution/talent` 多选 | 否 | Python | 缺省全部 |
| `relation_types` | `co_patent/co_project/talent_flow` 多选 | 否 | Python | 缺省全部 |
| `depth` | 1–2 | 否 | Python（首版封顶 2 跳） | 缺省 1 |
| `limit_nodes` / `limit_edges` | nodes≤200 / edges≤500 | 否 | Python | 超限按中心度 Top 截断 |

\*工作台从快照打开图谱时 `snapshotId` **必填**；仅调试/预览可省略并走「条件最新批」。

- **返回**：`{nodes:[{id,type,name,industry_label,degree}], edges:[{source,target,type,weight,year}], truncated:boolean, gapfill_batch_id, calc_batch_id?, snapshotId?, reason?}`；无映射 `nodes=[]`+`reason='batch_meta_missing'`（或约定 404），**不**用最新批凑数。正常空图用其他 reason。`calc_batch_id` 从同一 `batch_meta` 带回。
- **FE 差距**：现有 `CollabWorkbenchView.vue` 只按节点类型/边类型前端过滤（`kindFilter`/`edgeFilter`），**无产业筛选、无独立图谱请求**。需新增：①条件栏 `industry` 下拉（复用 `SynthContextBar` 扩展）；②图谱独立 API（`defineApi`）接线，过滤改服务端，传 `region/compare/window/snapshotId`；③截断提示；④映射缺失时展示不可用而非静默换图。见 §6。

### 3.3 效率报告与策略建议（141，闭环方案）

**报告 = 前端基于真实结果快照渲染并出 PDF**（复用既有 `renderIndustryAnalysisReportPdf` + `SystemReportReader`；`CollabReportPage.vue` 已有该能力）：

| 产物 | 闭环路径 | 空态 |
|---|---|---|
| 相关系数+散点 | `synth_collab_output_corr` → 快照 `effectEval` → 报告页消费 | 无行 → 报告该段「数据缺失」 |
| 协同效率报告 | 前端以 **succeeded 最新批真实快照** 渲染七段式报告（identity/…/limitations），下载 PDF 本地生成 | 快照 404/空 → 报告页提示「先完成分析」，不伪造数据段 |
| 策略建议 | **装包时 LLM 实时生成**（§2 证据锚定，`degraded` 安全降级）→ 快照 `strategies[]` → 报告「建议」段逐条带证据+「AI 生成·待审核」Tag | LLM 不可用/未配 → 该段空 + reason；不伪造 |

`*_report` 异步任务键保留白名单但 **v1 不依赖**（前端渲染即闭环）；后续如需服务端 PDF 归档再启（届时补报告正文表+文件存储，另行设计）。

## 4. METRIC（挂接/就绪度）

| metric_id | D1 | D4 | 落表 |
|---|---|---|---|
| `M_SYNTH_COLLAB_INDEX` | aligned | mock | `synth_collab_index` |
| `M_SYNTH_COLLAB_COMPLETENESS` | aligned | mock | `synth_collab_network_stat` |
| `M_SYNTH_COLLAB_CENTRALITY` | aligned | mock | `synth_collab_network_stat` |
| `M_SYNTH_COLLAB_DENSITY` | aligned | mock | `synth_collab_network_stat` |
| `M_SYNTH_COLLAB_RELATION_INPUT` | aligned | mock | `synth_collab_relation_input` |
| `M_SYNTH_COLLAB_OUTPUT_CORR` | aligned | mock | `synth_collab_output_corr` |

开放项 `Q-SYNTH-03 / C-01–C-05` 🟡 不拍板；口径引用 `calc-logic/SYNTH/*.md`。

## 5. 观测与可追溯

- FE 埋点 `synth_collab_*`；装包日志记完整 `batch_meta`；图谱导出任务记 Nebula space+行数；快照/resultData **持久化** `batch_meta`；graph 响应回显 meta 中的批号。

## 6. 页面差距审计（FE COLLAB 现状 vs 需规，v0.3 新增）

| 需规模块 | FE 现状（实码核对） | 差距 | 改造项 |
|---|---|---|---|
| 139① 网络图 | ECharts graph 力导已有 | 无 | — |
| 139② 按产业筛选 | **无**（仅节点/边类型前端过滤） | 缺控件+服务端过滤 | 条件栏加 industry 下拉；接 `GET .../collaboration/graph`；截断提示 |
| 139③ 密度/中心性展示 | 密度卡+中心度密度卡已有 | 无 | — |
| 140 集群/孤立 | 集群表+孤立主体表已有 | 无 | — |
| 141① 相关性散点 | Pearson+散点已有（样本<3 两态） | 无 | — |
| 141② 效率报告 | 报告页+PDF 下载已有 | 数据源接真快照 | 快照接线后删除演示依赖 |
| 141③ 策略建议 | 策略表+审核态 Tag 已有 | 数据源改 LLM 实时生成 | `strategies[]` 接装包 LLM 产物（证据锚定+待审核 Tag），无表 |

## 7. 验收条件

1. §3.2 契约逐参数断言（**必填 `region/compare/window`**；`snapshotId`/`gapfill_batch_id` 绑定；industry 服务端过滤、depth、截断+truncated、空态）。
2. **灌读一致**：预填/seed 含五码（含 `RELATION_INPUT`）；`GET .../graph` 在默认三元组下 **nodes 与 edges 均非空**；响应内 `id`（节点）与 `source-target-type-year`（边）**无重复**；故意只灌四码不含 RELATION_INPUT 时必须空图+`reason`（负例）。
3. **批次持久化**：成功快照/任务必含完整 `batch_meta`；进程重启后仍可按不可变 `snapshotId` 解析图批；**有 snapshotId 无 meta → `batch_meta_missing`，断言未读最新批**。
4. **ID 不撞**：批 A 后再跑批 B → `snapshotId_B ≠ snapshotId_A`；用 A 打开图谱仍返回 A 的 `gapfill_batch_id`；`cache_key` 可改指 B；同 `snapshotId` 与 meta 一致；仅无绑定参数时才允许条件最新批。
5. 相关系数/报告/策略独立闭环（§3.3）；报告=前端真快照渲染，快照缺失时不伪造。
6. 策略未审核不自动发布。
7. `_ai` 只读 succeeded 最新批（按 `calc_batch_created_at`）；`failed` 批不被读取。
8. 预填 gapfill 行页面 🧪；换源后表结构不变。
9. §6 差距矩阵改造完成（industry / 图谱 API 带 compare+snapshotId / 截断 / 映射缺失提示）。

## 8. 实现单/文件边界（并行分配）

| 动作 | 仓/文件 | 归属 | 依赖 |
|---|---|---|---|
| **5 张** `_ai` 表 DDL + 预填（index/network_stat/relation_input/output_corr/cluster） | `lumen-algo-py/scripts/mysql/synth_collab_metrics.sql` + seed（新建） | 线3 data/算法 | 无，可先行 |
| 2 张 gapfill 图事实 DDL + seed（**五码含 RELATION_INPUT**）+ Nebula 导出任务 | 同目录 + `export_collab_graph.py`（新建） | 线3 data | 真值 blocked：C-05；预填可先行 |
| 装包（collaboration 分支）+ cluster 派生 + strategy LLM + **持久化 `batch_meta` 写入快照/resultData** | `vendor/entan-py`（复用 `entan/common/llm_client.py`） | 线3 算法 | 5 张 `_ai` + 2 张 gapfill |
| 图谱查询接口（Java 门面+Python，含 compare/snapshotId） | `gkxlumen-topic` + `entan-py` | 线3 api | node/edge 表（预填即可开发） |
| FE 产业筛选+图谱 API 接线（传 compare+snapshotId） | `lumen-ui-topic` CollabWorkbench/SynthContextBar | 线3 前端 | 图谱接口契约（§3.2） |
| Java Adapter collaboration 键 | gkxlumen-topic-async-service | 线3 api | 与要素线共改 BE-1 时协调 |

## 9. 会签

| 角色 | 状态 |
|---|---|
| 架构 | 未签 |
| 算法 | 未签 |
| 数据 | 未签（图事实 blocked：C-05） |
| 产品 | 未签（141 策略审核态交互、报告前端渲染口径确认） |

## 10. 修订

| 版本 | 日期 | 说明 |
|---|---|---|
| v0.1 | 2026-11-04 | 首版骨架 |
| v0.2 | 2026-11-04 | 评审修复：表数修正、§3.2 图谱契约、§3.3 报告策略独立落点、每表四项 |
| v0.3 | 2026-11-04 | 第二轮审核修复：node/edge 移 gapfill（D16）、cluster 归 `_ai` 算法派生、strategy 独立分析产物；图谱查询改精确接口+执行方分工+FE 产业筛选差距；报告闭环=前端真快照渲染 PDF（`*_report` 键 v1 不依赖）；唯一键补全条件上下文+批次按 `calc_batch_created_at` 排序；新增 §6 页面差距审计（实码核对） |
| v0.4 | 2026-11-04 | 第三轮收敛：`synth_collab_strategy` 表废止——策略建议改装包时 LLM 实时生成（`llm_client.py` GLM，证据锚定，degraded 降级，对齐 C-04）；cluster 口径挂靠登记（COMPLETENESS 公式+C-02）；gapfill node/edge 补 D16 登记明细（metric_id/gap_item/fill_method/批次/读路径/换源动作） |
| v0.5 | 2026-11-04 | 第四轮审核收敛：output_corr 粒度对齐 calc-logic 正式口径（X×年度配对，x_metric_id/output_metric_id/r_value/sample_n/period/status 列，n<3=insufficient 合法行非整批失败）；gapfill 批次字段统一 `gapfill_batch_id`（D16），补齐必填列与每行指标归属 |
| v0.6 | 2026-11-04 | 第五轮审核收敛：node/edge 行级血缘拆 `metric_id` 维度（一行=一主体/边×一服务指标，唯一键含 metric_id+gapfill_batch_id），符合 D16 行级血缘 |
| v0.7 | 2026-11-04 | 第七轮收敛：§2 标题 6→5 张；图谱接口补 canonical 去重规则（只读 RELATION_INPUT 行，杜绝四份重复） |
| v1.0 | 2026-11-05 | 头部对齐总册 v1.0-draft（正文口径已在 v0.7，本版只统一版本引用） |
| v1.0.2 | 2026-11-05 | P1：灌数五码含 RELATION_INPUT 与 canonical 读统一；图谱补 compare/snapshotId/gapfill_batch_id 与 batch_link；验收补非空无重复。P2：实现清单 5+1→5 |
| v1.0.3 | 2026-11-05 | 废止 COMMENT/内存映射；`batch_meta` 持久进快照与 resultData；指定 snapshot 无映射禁止回落最新批 |
| v1.0.4 | 2026-11-05 | `snapshotId` 不可变含 calc_batch_id；`cache_key` 条件索引可覆盖指向；验收 A/B 批图谱不串 |


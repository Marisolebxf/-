# SYNTH L2 · 协同册 — 区域创新协同分析（ARCH/DATA/API/METRIC 合并册）

- 日期：2026-11-05（v1.0.7：1y/3y/5y 不回全历史边；源无年则空图；密度不读 191）
- 状态：**DRAFT，第一轮退回后改稿，待复审**
- 上游：总册 §2.3/§11（v1.0.5-draft）；需求真源 SRS 139–141。密度不读 `M_SYNTH_191_1`
- 现状衔接：FE COLLAB 三页已联调中（`LUMEN-INTEL-FE-COLLAB`）；**页面差距见 §6**（产业筛选控件缺失、图谱独立查询接口缺失），不是"已备不改"。

## 1. ARCH（流程与落点）

```text
lumen-ui-topic
  → gateway → topic 快照 / topic-async / 图谱查询
  → GET /topic/v1/synth/collaboration/batch-snapshot
  → GET /topic/v1/synth/collaboration/graph
  → POST /topicAsync/.../analysis/tasks → POST /internal/v1/synth/jobs/execute
  → entan-py
       指标：只读 ADS synth_collab_index / network_stat / relation_input / output_corr
       图：只读 ADS synth_collab_node / synth_collab_edge
       批次：读写 ADS synth_collab_batch_meta
       集群：不读归属行。clusters=[] + reason=cluster_rule_unclosed
       策略：LLM 实时，无表
```

- 库：`demo_gkxlumenx_ads` / `gkxlumenx_ads`。灌数方 entan-py。不使用 `gkxlumenx_ai`，不使用 `gapfill_synth_collab_*`。
- 请求窗是 `1y/3y/5y`。关系输入源没有年，不能把全历史边放进这些窗。该窗 `nodes=[]`、`edges=[]`，`reason=no_year_on_source`。`window_label` 只出现在请求和 `synth_collab_batch_meta`，不用来复制一份无窗截面。
- 协同指数式仍是 `Index=(1/3)*[minmax(Completeness)+minmax(Centrality_avg)+minmax(Density)]`。该窗图为空时，指数、完整度、中心度、密度都是 `null`+`reason=no_year_on_source`，不把无窗截面抄进三个窗。密度不读 `M_SYNTH_191_1`，也不把 191 的密度写入 `synth_collab_network_stat`。禁止密度×强度。
- 本期不写 `synth_collab_node` / `synth_collab_edge` 行。不读论文关系表，不做 Nebula 导出，不灌演示行。
- Java 不写 nGQL。样本 <3：不出系数。

## 2. DATA

库：`demo_gkxlumenx_ads` / `gkxlumenx_ads`。读取快照：`GET /topic/v1/synth/collaboration/batch-snapshot`。读取图谱：`GET /topic/v1/synth/collaboration/graph`。公共列见总册 §11.2。

**指标表（灌数 4 张；cluster 在表内但本期 0 行）**

| 表 | 业务粒度（一行=） | 唯一键（基础=region+compare+window+batch） | 写入 | 读批 |
|---|---|---|---|---|
| `synth_collab_index` | 基础键 | 基础键 | 该窗图为空则不灌数，接口 `null`+`reason=no_year_on_source` | 有 succeeded 行才读最新批；本期三窗无行 |
| `synth_collab_network_stat` | 基础 × stat | `+ (stat_type)` | 同上。不写入 191 的密度 | 同上 |
| `synth_collab_relation_input` | 基础 × 关系类型 | `+ (relation_type)` | 同上。不把全历史计数抄进 1y/3y/5y | 同上 |
| `synth_collab_output_corr` | 基础 × X 指标（index/density/centrality）× 年度配对窗口（**calc-logic 正式口径：区域固定、按年组样本，不做跨区域截面**） | `+ (x_metric_id, output_metric_id, period_start, period_end)`；列含 `r_value`/`sample_n`/`status(sufficient\|insufficient)`/`reason` | Pearson；**n<3 存为合法 `insufficient` 行（正常结果，非失败、非 failed 批）**；双侧方差=0 同 insufficient | 同批 N 行；全缺 → 效果区空态 |
| `synth_collab_cluster` | 基础 × 主体 | `+ (entity_type, entity_id)` | **本期不灌、不派生**。禁止用完整度 `n/N` 写归属 | 0 行 → `clusters=[]`+`reason=cluster_rule_unclosed` |

**策略建议（141③）：无表，LLM 实时生成（v0.3）**

- 装包时以结构化结果（集群/孤立/相关性/网络统计）拼**证据 prompt** → `entan/common/llm_client.py`（GLM，Secret `gkx-zhipu-llm`）；失败/未配 → `degraded: strategies=[] + reason`（`narrative.py` SWOT 同款模式）。
- 诚实性：只基于本次计算事实，禁止编造；页面保留「AI 生成·待审核」Tag（Q-SYNTH-C-04 临时默认）。
- 不建表。失败保持 `strategies=[]`+`reason`。

**图事实与批次（ADS，禁止 `gapfill_` 前缀）**

| 表 | 粒度 / 唯一键 | 列 | 写入 | 读 |
|---|---|---|---|---|
| `synth_collab_node` | 一行=主体×条件×`metric_id`。`uk(region_code, compare_scope, window_label, metric_id, entity_type, entity_id, graph_batch_id)` | `name`，`industry_code`，`industry_label`，`degree` | **本期 0 行**。不把全历史主体写入 1y/3y/5y | 图谱只读 `RELATION_INPUT`；无行则空图 |
| `synth_collab_edge` | 一行=边×条件×`metric_id`。`uk(..., source_event_id, graph_batch_id)`。无 `year` | `weight`，`source_event_id` | **本期 0 行**。源无年，禁止用全历史边填充窗口 | 同上 |
| `synth_collab_batch_meta` | 一行=一个不可变 `snapshotId`。`uk(snapshotId)` | `snapshotId`，`calc_batch_id`，`graph_batch_id`，`cache_key`，`region`，`compare`，`window`，`published_at`，`is_latest` | 发布成功时 Python 写入。同 `cache_key` 新成功批把旧行 `is_latest` 置 0，新行置 1。不删旧 `snapshotId` | 重启后按 `snapshotId` 读取。未传 snapshotId 时读 `is_latest=1` |

`cache_key = region|compare|window` 指向该条件下最新成功 `snapshotId`，存在 `synth_collab_batch_meta` 的最新指针（同一表用 `cache_key` + `is_latest=1`，旧行改 `is_latest=0`）。缺任一 meta 列则不得标 succeeded。

## 3. API

### 3.1 快照与任务

- `GET /topic/v1/synth/collaboration/batch-snapshot?region=&compare=&window=` → `CollabResult`；404 非默认三元组；缺数据 200+null/reason。
- 任务：`region_innovation_collaboration`（`POST /topicAsync/topic/v1/analysis/tasks`）；Java `SynthAnalysisAdapter` → Python `POST /internal/v1/synth/jobs/execute`，入参 `{task_id, leaf:'collaboration', region, compare, window}`（窗归一中文）；失败 → 任务 `failed`+`reason`。
- 五阶段文案逐字用 MOCK-INV §2 协同行。

**批次映射**

成功发布时 Python 把一行写入 ADS `synth_collab_batch_meta`，并在快照响应与 `#105 resultData` 回显同名字段。字段即 §2 该表的列。禁止只写 COMMENT、内存或日志。

无 meta 时图谱固定 HTTP 200、`nodes=[]`、`reason=batch_meta_missing`。不用 404。

### 3.2 图谱查询接口（139，独立精确契约）

- **URL / 方法**：`GET /topic/v1/synth/collaboration/graph`（网关 → `gkxlumen-topic` → Python `GET /internal/v1/synth/collaboration/graph`）
- **执行分工**：前端只传参。Python 执行筛选、截断。Java 只透传。
- **批次选择**：
  1. 传 `snapshotId` → 只读 `synth_collab_batch_meta` 中该 ID 的 `graph_batch_id`，再只读该批图行。找不到 meta → HTTP 200、`nodes=[]`、`reason=batch_meta_missing`。禁止改读最新批。
  2. 未传 `snapshotId` → 用 `cache_key` 取 `is_latest=1` 的 `snapshotId`，再按上一条读。
  3. 工作台从快照进图谱必须带 `snapshotId`。
- **去重**：图谱只读 `metric_id='M_SYNTH_COLLAB_RELATION_INPUT'`。同一主体或边只返回一份。
- **请求参数**：

| 参数 | 类型/取值 | 必填 | 执行方 | 说明 |
|---|---|---|---|---|
| `region` | 区域编码 | 是 | Python | 与 UK `region_code` 对齐 |
| `compare` | 对比范围编码 | 是 | Python | 与 UK `compare_scope` 对齐；缺省不默改 |
| `window` | `1y/3y/5y` | 是 | Python | 写入 meta 的 `window_label`。该窗不返回全历史边。源无年 → 空图 `reason=no_year_on_source` |
| `snapshotId` | 快照 ID | 否 | Python | 工作台从快照打开时必填。从 `synth_collab_batch_meta` 解析 `graph_batch_id` |
| `industry` | 产业领域编码 | 否 | Python | 过滤节点 `industry_code`。缺省=全部 |
| `entity_types` | `enterprise/institution/talent` 多选 | 否 | Python | 缺省全部 |
| `relation_types` | `co_patent/co_project/talent_flow` 多选 | 否 | Python | 缺省全部 |
| `limit_nodes` / `limit_edges` | nodes≤200 / edges≤500 | 否 | Python | 超限按中心度 Top 截断 |

本期没有 `depth`。本期没有 `gapfill_batch_id`。

- **返回**：`{nodes, edges, truncated, graph_batch_id, calc_batch_id, snapshotId, reason?}`。本期三窗 `nodes=[]`、`edges=[]`、`reason=no_year_on_source`。无 meta 仍是 HTTP 200 + `reason=batch_meta_missing`。边对象若将来有行，也不带 `year`。
- **FE 差距**：现有 `CollabWorkbenchView.vue` 只按节点类型/边类型前端过滤（`kindFilter`/`edgeFilter`），**无产业筛选、无独立图谱请求**。需新增：①条件栏 `industry` 下拉（复用 `SynthContextBar` 扩展）；②图谱独立 API（`defineApi`）接线，过滤改服务端，传 `region/compare/window/snapshotId`；③截断提示；④映射缺失时展示不可用而非静默换图。见 §6。

### 3.3 效率报告与策略建议（141，闭环方案）

**报告 = 前端基于真实结果快照渲染并出 PDF**（复用既有 `renderIndustryAnalysisReportPdf` + `SystemReportReader`；`CollabReportPage.vue` 已有该能力）：

| 产物 | 闭环路径 | 空态 |
|---|---|---|
| 相关系数+散点 | `synth_collab_output_corr` → 快照 `effectEval` → 报告页消费 | 无行 → 报告该段「数据缺失」 |
| 协同效率报告 | 前端以 **succeeded 最新批真实快照** 渲染七段式报告（identity/…/limitations），下载 PDF 本地生成 | 快照 404/空 → 报告页提示「先完成分析」，不伪造数据段 |
| 策略建议 | **装包时 LLM 实时生成**（§2 证据锚定，`degraded` 安全降级）→ 快照 `strategies[]` → 报告「建议」段逐条带证据+「AI 生成·待审核」Tag | LLM 不可用/未配 → 该段空 + reason；不伪造 |

报告只在前端用已成功快照渲染。本期不建报告正文表，不做服务端 PDF 归档，不写文件存储。

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

- FE 埋点 `synth_collab_*`；装包日志记完整 `batch_meta`；快照/resultData 回显 `synth_collab_batch_meta` 的列；graph 响应回显 `graph_batch_id`。不记 Nebula 导出。

## 6. 页面差距审计（FE COLLAB 现状 vs 需规，v0.3 新增）

| 需规模块 | FE 现状（实码核对） | 差距 | 改造项 |
|---|---|---|---|
| 139① 网络图 | ECharts graph 力导已有 | 无 | — |
| 139② 按产业筛选 | **无**（仅节点/边类型前端过滤） | 缺控件+服务端过滤 | 条件栏加 industry 下拉；接 `GET .../collaboration/graph`；截断提示 |
| 139③ 密度/中心性展示 | 密度卡+中心度密度卡已有 | 无 | — |
| 140 集群/孤立 | 页面有表 | 本期不出归属行 | 接口空态 `clusters=[]`+`reason=cluster_rule_unclosed`。页面显示该 reason，不填演示归属 |
| 141① 相关性散点 | Pearson+散点已有（样本<3 两态） | 无 | — |
| 141② 效率报告 | 报告页+PDF 下载已有 | 数据源接真快照 | 快照接线后删除演示依赖 |
| 141③ 策略建议 | 策略表+审核态 Tag 已有 | 数据源改 LLM 实时生成 | `strategies[]` 接装包 LLM 产物（证据锚定+待审核 Tag），无表 |

## 7. 验收条件

1. §3.2：必填 `region/compare/window`；`industry` 过滤 `industry_code`；无 `depth`；截断带 `truncated`。
2. 图谱只读 `RELATION_INPUT` 行。有行时节点 `id` 不重复，边 `source-target-type-source_event_id` 不重复。响应边没有 `year`。默认三元组允许空图。不得用演示行满足非空。
3. 成功发布必有 `synth_collab_batch_meta` 行。重启后按 `snapshotId` 仍能读到该行的 `graph_batch_id`。有 `snapshotId` 但无 meta → HTTP 200 + `batch_meta_missing`，且未读最新批。
4. 批 A 后再跑批 B → `snapshotId` 不同；用 A 打开图谱仍返回 A 的 `graph_batch_id`；`cache_key` 可改指 B。
5. 1y/3y/5y 的指数、完整度、中心度、密度均为 null+`reason=no_year_on_source`。响应里不得出现 191 的密度。集群为 `clusters=[]`+`reason=cluster_rule_unclosed`。node/edge 表 0 行。
6. 报告=前端真快照渲染。策略失败 `strategies=[]`+reason。无报告正文表。
7. 指标表只读 succeeded 最新批。`failed` 批不被读取。`is_mock=1` 的指标行页面带 MockBadge。
8. §6 的 industry、图谱 API、截断、映射缺失提示做完。

## 8. 实现单/文件边界（并行分配）

| 动作 | 仓/文件 | 归属 | 依赖 |
|---|---|---|---|
| 4 张指标 ADS DDL + 预填（index/network_stat/relation_input/output_corr）+ cluster 空表 + batch_meta + node/edge | `lumen-algo-py/scripts/mysql/synth_collab.sql` | 线3 data/算法 | 无 |
| 1y/3y/5y 不写 node/edge，不把 191 写入 network_stat | `vendor/entan-py` | 线3 算法 | 上表 |
| 装包 + 策略 LLM + 写 `synth_collab_batch_meta`。不派生 cluster | `vendor/entan-py` | 线3 算法 | 指标 4 张 |
| 图谱查询（Java 门面 + Python） | `gkxlumen-topic` + `entan-py` | 线3 api | node/edge/batch_meta |
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
| v1.0.5 | 2026-11-05 | 会签退回：指标与图改落 ADS；废止 gapfill 图与非空验收；集群不派生；batch_meta 落表；删 depth 与服务端 PDF |
| v1.0.6 | 2026-11-05 | 边去掉 year；window 不按年份过滤；只实查联合专利与人才流动；不做 Nebula 导出 |
| v1.0.7 | 2026-11-05 | 源无年：三窗不回全历史边，指数与三项网络统计 null；密度不读 191；node/edge 本期 0 行 |


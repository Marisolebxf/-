# POL-L2-DS12-SIM-API · 政策效果推演 · 科技政策推演 · 后台接口设计

- 任务：`POL-L2-DS12-SIM-API`
- 日期：2026-11-05
- 监管：`human:淮政玮`
- 认领：`agent:api-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-06`
- 上游：`sdd/l2/POL-L2-DS12-SIM-ARCH.md`（工作区当前稿。稿头仍写待架构、算法、数据、产品四角色会签，不标 done。2026-11-05 已改第 7、9 节的表张数与 235/236 灌数归属，读法未改。本分册以该稿为准，不改它）

本分册只定政策效果推演二级「科技政策推演」的后台接口。SRS 序号 **237–242**。它是 `BE-POL-CONTRACT-01` 的输入，不是第二份 API-POL。不另建契约文件。枚举闭包、响应字段名、种类字段名和 DTO 仍由那一张契约冻结。这里只写路径、方法、内部委托、同步或作业、空态。不写 OpenAPI 字段表，不写实现代码。

流程以 `POL-L2-DS12-SIM-ARCH` 为准。效果预估半区 `POL-L2-DS12-EST-ARCH` 只作共用入口对照：推演整页只有一条 `POST /display/v1/policy/simulation/jobs`。232–236 的种类定义交给 `POL-L2-DS12-EST-API`。本分册只定义推演侧种类。清单、`指标与501.md`、说明书、WBS、调研里仍写的 501 空态不覆盖本分册。

签收口径：237 同步读已有 `ads.policy_text_parse` 的解析行。238、239、241、242 同步读 `gkxlumenx_gapfill.gapfill_policy_sim_result` 里本分册的四种行。240 不设 HTTP 资源。五次有资源的读取都不建任务记录。不允许接口直接返回 mock，也不用 501 充当功能。无行则空。

## 偏离

三处与任务 DoD 字面、或仍在架上的旧空态和灌数清单不一致。本分册按已落盘架构稿收窄，不回头改那些文件，也不改注册表。

1. 当前 DoD 完成标准写的是「路径、方法、同步或 Job、501 空态」，以及「只汇入 `BE-POL-CONTRACT-01`，不单独冻结第二份 API-POL，不写实现代码，不复用 `/topic/v1/policy`」。`task-get` 返回的 DoD 正文没有「237/242 按 501」或「灌文本解析」这两句原文。`指标与501.md`、说明书、契约输入清单里 237–242 仍写 501（架构第 7 节）。本分册按架构收窄：237、238、239、241、242 都是同步读，空态是空，HTTP 成功，不返回 501。240 无资源。不改 `指标与501.md`、说明书、WBS、调研、契约输入清单，也不改 EST-ARCH。
2. 说明书第 11.2 节把「文本解析」写在 SIM 组要灌清单里。架构第 9 节按第 11 节总规则收窄：237 不灌 gapfill，读已有 `ads.policy_text_parse`。请求路径不调用 `polan.text.parse.run`。`POL-L2-DS12-SIM-GAPFILL-L01` 的「文本解析」不灌。要灌的是多维评估（235）、参与意见（236）、重点、影响范围、路径、解读正文。本分册不执行灌数，不改灌数单。
3. 不新建作业入口，不建第二个分发器。237、238、239、241、242 与 232–236 共用已有 `POST /display/v1/policy/simulation/jobs`，一次请求只带一种类。237 的处理是同步读，不是作业。232–236 的种类、读表和空态由 `POL-L2-DS12-EST-API` 写。本分册不把整条 `simulation/jobs` 改成只读 `gkxlumenx_gapfill.gapfill_policy_sim_result`。

## 1. 公开资源

前缀 `/display/v1/policy/`。六叶都在政策效果推演页的科技政策推演区里完成，不另开页，不另开路径。本二级对外只有下面这一条已有资源，且一次请求只带一种类。不新建第二条作业入口。

| 序号 | 公开资源 | 读法 |
|---|---|---|
| 237 政策文本智能解析 | `POST /display/v1/policy/simulation/jobs` | 同步读。种类为文本解析。element 只读已有 `ads.policy_text_parse` 的解析行。不是作业。不建任务。请求路径不调用 `polan.text.parse.run`。不灌 gapfill。无解析行则报告空。不返回 501 |
| 238 政策重点可视化展示 | 同一条 `POST /display/v1/policy/simulation/jobs` | 同步读。种类为重点可视化。element 只读 `gkxlumenx_gapfill.gapfill_policy_sim_result` 的重点行。不是作业。无行则该区空。不返回 501 |
| 239 政策影响范围分析 | 同一条 `POST /display/v1/policy/simulation/jobs` | 同步读。种类为影响范围。同一张表按政策（推演上下文）拣影响范围行。不是作业。无行则该区空。不返回 501 |
| 240 政策关联分析 | `GET /display/v1/policy/simulation/relation-graph` | 无 jobs 种类。透传专题 `/topic/v1/policy/graph`。不新建查图任务 |
| 241 政策实施路径预测 | 同一条 `POST /display/v1/policy/simulation/jobs` | 同步读。种类为路径预测。同一张表拣路径环节行。不是作业。无行则该区空。不返回 501 |
| 242 政策解读报告生成 | 同一条 `POST /display/v1/policy/simulation/jobs`（读面）+ `evaluation/jobs`（真算） | **读面**同步读。种类为解读报告。同一张表拣解读段落行，页面呈现正文。不是作业。不产生 PDF、Word 文件。无行则报告区空。不返回 501。**真算**见 §8.2（`policy_sim_interpret`） |

`simulation/jobs` 上还有效果预估半区的种类。本分册不改写那些种类，也不把查推演缺项表的读法套到它们身上。

| 留给谁 | 种类 | 本分册不改的读法 |
|---|---|---|
| `POL-L2-DS12-EST-API` | 未出台仿真、新出台预测、区域空间 | 各一次请求。读 `gkxlumenx_gapfill.gapfill_policy_sim_forecast`。都不进异步 |
| `POL-L2-DS12-EST-API` | 多维评估 | 读 `gkxlumenx_gapfill.gapfill_policy_sim_result` 的多维评估行。与本分册四种行同表不同种类。灌数归属见架构第 9 节，读法由 EST-ARCH 定 |
| `POL-L2-DS12-EST-API` | 利益攸关方 | 读 `gkxlumenx_gapfill.gapfill_policy_sim_stakeholder` 的参与意见行。本分册不读这张表 |

真推演模型未注册。本分册不定义真推演种类，不加 `policy_simulate`。未注册时该能力空态。**例外（2026-11-12 / 2026-11-13）**：237 真算键 `policy_text_parse_run`、238 真算键 `policy_sim_focus`、242 真算键 `policy_sim_interpret` 进 `PolicyAnalysisTypes` / `JOB_SUB_TYPES`，经 `evaluation/jobs` → `/internal/policy/jobs/execute`。评价页 226 的 `policy_text_parse` **仍只读**，237 真算不改走该键。推演键接通后，239 改随该次真结果。

种类字段名由 `BE-POL-CONTRACT-01` 冻结。本分册只定种类的中文名和一次一种类：文本解析、重点可视化、影响范围、路径预测、解读报告。240 不占种类。

## 2. 内部委托

浏览器经网关打 `gkxlumen-display`。网关只转 `/display/**`。浏览器只打 `/display/v1/policy/**`。不改打 `/topic/v1/policy`，不打开算法中台页面，不打 `/v1/policy/**`。

`gkxlumen-display` 不直连库，不直连 Python，不写算法，不写 nGQL。不调用任何 `demo-*` 服务。Java 不做 NLP，不生成解析，不生成重点，不生成影响范围，不生成路径，不生成报告文件，不写死正文。

| 公开资源 | 内部委托 |
|---|---|
| `simulation/jobs` 的文本解析（读面） | `gkxlumen-display` 不建任务；`gkxlumen-element` 只读 `ads.policy_text_parse`。不调用 `polan.text.parse.run` |
| `evaluation/jobs` · `policy_text_parse_run`（237 真算） | display → topic-async → `/internal/policy/jobs/execute` → `polan.text_parse_run_job` 单政策 upsert。禁整表清空 |
| `evaluation/jobs` · `policy_sim_focus`（238 真算） | display → topic-async → `/internal/policy/jobs/execute` → `polan.sim_focus_job` 单政策 upsert 重点行。禁整表清空 |
| `evaluation/jobs` · `policy_sim_interpret`（242 真算） | display → topic-async → `/internal/policy/jobs/execute` → `polan.sim_interpret_job` 单政策 upsert 解读段落。禁整表清空 |
| `simulation/jobs` 的重点可视化、影响范围、路径预测、解读报告（读面） | `gkxlumen-display` 不建任务，不转发异步服务，不调 Python。`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_sim_result` 里该次种类的行。库名 `gkxlumenx_gapfill`，表名 `gapfill_policy_sim_result`。真算写回见上三行，不改读面资源 |
| 240 政策关联分析 | display Feign 委托专题 graph。Java 不写 nGQL。不新建查图任务 |

若 `gkxlumen-display` 还没有推演控制器，实现时按契约补这一条已有的 `simulation/jobs`。补上之后仍按种类分发。不能把整条 `jobs` 都改成只读 `gkxlumenx_gapfill.gapfill_policy_sim_result`，也不能为 237 另开解析 URL，不能为 240 另开查图 URL。本分册不补控制器，不写 Java。

五次**读面**都不进异步任务管道（真算写回走 `evaluation/jobs`，见 §3.2 / §4.2 / §8.2）。切政策、切推演上下文不自动起任务。某一次 `jobs` 失败，不清空其他种类已经返回的区块。本页没有可接统计读面。

trace 沿既有展示链。display 往 element 带 traceId。本分册不新设计观测点。

238、239、241、242 的行在 `gkxlumenx_gapfill.gapfill_policy_sim_result`。字段级 DDL 由 `POL-L2-DS12-SIM-DATA` 定。这四种行的灌数由 `POL-L2-DS12-SIM-GAPFILL-L01` 执行。查询请求不灌数。库只允许 `gkxlumenx_gapfill`。这四种行不进 ODS、DWD、ADS，不写供应方库。

235 的多维评估行也灌进 `gkxlumenx_gapfill.gapfill_policy_sim_result`。236 的参与意见行灌进 `gkxlumenx_gapfill.gapfill_policy_sim_stakeholder`。两张表都保留，不收成一张，不另建第三张。235、236 的读法由 EST-ARCH 定，灌数仍由 `POL-L2-DS12-SIM-GAPFILL-L01` 执行（架构第 7、9 节）。本分册不改这两行的行内容，不定义这两个种类的请求。

237 不灌缺项行。解析行已在 `ads.policy_text_parse`。本分册不写这张表，不新建 ADS 表。

每条缺项行都带 `metric_id`、`gap_item`、`fill_method`、`gapfill_batch_id`、`generated_at`，以架构第 9 节为准。238、239、241、242 的 `metric_id` 留空，不新注册。`fill_method` 用 `manual`。`gap_item` 写序号和叶子名。237 行上的 `metric_id` 仍是已有 `M_POLICY_TEXT_PARSE`，不改。240 沿用已有 `M_POLICY_RELATION_DEGREE`，不新注册，本分册不为此加资源。D4 保持 mock。`GDF-POLICY-MOCK-GATE-L01` 仍是 blocked。本分册不把 mock 写成已上线，不改 D4。

## 3. 237 政策文本智能解析 · 同步读 + 异步真算写回

### 3.1 读面（并存）

公开资源：`POST /display/v1/policy/simulation/jobs`，种类=文本解析。element 只读 `ads.policy_text_parse`。同步、不建任务。返回去掉 `clauses`/`clause_meta`。`title`/`summary`/`auto_tags`/四中文要素键。评价 226 的 `policy_text_parse` 键保持只读。

### 3.2 真算写回（2026-11-12 三卡）

公开资源：`POST /display/v1/policy/evaluation/jobs`。

| 字段 | 值 |
|---|---|
| `sub_type` | `policy_text_parse_run` |
| `params.policy_id` | 必填 |
| `force` | 可选；true 重算 |
| `analysis_fp` | 条件指纹（同评价 jobs） |

链路：display → topic-async → `/internal/policy/jobs/execute` → `polan.text_parse_run_job`：规则优先 + 残量 LLM → **单政策 upsert**（merge 保留条款键）。禁 `polan.text.parse.run` / 整表清空。不调用 `structure_one`。create 同步终态（同 238）。成功后前端再打 §3.1 读面。

空态：未选政策、无正文、无密钥失败 → 「暂无解析结果」；不写假四键。读面 HTTP 成功不 501。

## 4. 238 政策重点可视化展示 · 同步读 + 异步真算写回

### 4.1 读面（并存）

公开资源：`POST /display/v1/policy/simulation/jobs`，种类=重点可视化。element 只读 `gapfill_policy_sim_result` 重点行。同步、不建任务、不改 SELECT。柱图读 `score_value`（COVER-FDE）。`M_POLICY_FOCUS_INDEX` 不挂本叶。

### 4.2 真算写回（2026-11-12 ASYNC）

公开资源：`POST /display/v1/policy/evaluation/jobs`。

| 字段 | 值 |
|---|---|
| `sub_type` | `policy_sim_focus` |
| `params.policy_id` | 必填 |
| `force` | 可选；true 重算 |
| `analysis_fp` | 条件指纹（同评价 jobs） |

链路：display → topic-async → `/internal/policy/jobs/execute` → `polan.sim_focus_job`：读 DWD 正文 → LLM → **单政策 upsert** 重点四行。禁整表清空。create 同步终态（同评价焦点/优缺点）。成功后前端再打 §4.1 读面画图。

空态：未选政策、无正文、无密钥失败 → 不写假行；读面仍空。HTTP 读面成功不 501。

## 5. 239 政策影响范围分析 · jobs · 影响范围 · 同步读

公开资源仍是 `POST /display/v1/policy/simulation/jobs`。浏览器另一次提交，种类为影响范围。

没有专属指标。需规写明基于政策效果推演结果。推演键未注册。契约注明影响范围只跟该次结果。

链路与第 4 节相同，element 只读同一张 `gkxlumenx_gapfill.gapfill_policy_sim_result` 的影响范围行。

- 同步读。不建任务
- 政策或推演上下文必选。按该政策拣行
- 一行是一个影响对象：所属政策、类别、名称、一句说明、时间变化说明。类别只用受益对象、影响区域、影响行业，写在行上。类别的字段名由契约单冻结
- 空间分布是行上的区域维度数据。热力图和地图在前端渲染。服务端只返回行
- 真推演接通前，这些行是已灌的模拟上下文行。真推演接通后改随该次真结果。切换不改资源、不改种类、不另开 URL。注册动作不在本分册
- 行上 `metric_id` 留空，不新造
- 不读 `gkxlumenx_gapfill.gapfill_policy_sim_forecast`。不把 234 的区域空间行复制成本叶
- 不把第 7 项图谱查询写成影响范围的计算源。Java 不写 nGQL

空态：无行则该区空。HTTP 成功。不返回 501。不造全国通用兜底行。不在接口函数里返回写死的影响对象。

## 6. 240 政策关联分析 · relation-graph 透传（2026-11-12 卡1=B）

指标 `M_POLICY_RELATION_DEGREE`，GRAPH，D4=mock。调研判跨项索引。

- **不设** `simulation/jobs` 种类。公开读口：`GET /display/v1/policy/simulation/relation-graph?policy_id=&steps=1&limit=80`
- display Feign 透传 `GET /topic/v1/policy/graph?center=&steps=&limit=` → Python `/internal/policy/graph`（Nebula 优先，ADS 镜像回退）
- 响应透传 `nodes` / `edges` / `source` / `centers`；空图诚实空列表，`fabricated=false`。Java 不写 nGQL、不填假网
- `E-E7-POLICY-M1-L06` 不是实现路径。浏览器不改打 `/topic/v1/policy`
- 不新造 `metric_id`。不改 D4。不灌 `gapfill_policy_sim_result` 关联行

空态：无邻域边则 `nodes/edges` 空；前端业务文案「暂无政策关联网络」。

## 7. 241 政策实施路径预测 · jobs · 路径预测 · 同步读

公开资源仍是 `POST /display/v1/policy/simulation/jobs`。浏览器另一次提交，种类为路径预测。表行种类是路径环节。

指标未见。`M_POLICY_LAYOUT_REC_COUNT` 是布局推荐计数，不顶替本叶。`M_POLICY_DS_11_POLICY_EVAL_015` 在评价页 229，不顶替本叶。

链路与第 4 节相同，element 只读 `gkxlumenx_gapfill.gapfill_policy_sim_result` 的路径环节行。

- 同步读。不建任务。不派生流程任务
- 政策必选。少了政策则该区空
- 一行是一个环节：所属政策、环节、时间安排、责任主体、一句说明。环节只用政策发布、申报受理、评审评估、资金拨付、效果评估，写在行上。环节的字段名由契约单冻结
- 流程图在前端渲染。服务端只返回行。界面必见仅「政策实施流程图」；**不**返回历史对照行、**不**要求「历史评估图」读口（2026-11-12 需规分句闭合卡1=A）
- 环节是预测展示。请求处理不推进环节状态，不写执行记录
- 行上 `metric_id` 留空，不新造
- 不把布局推荐的建议条数填进本叶。不把评价页 229 的路径与风险复制过来
- 不把 `M_POLICY_SIMULATE` 写进这些行。推演键只挂 232–234，那三叶在 EST-API

空态：该政策没有路径环节行，则该区空。HTTP 成功。不返回 501。不在接口函数里编时间表。

## 8. 242 政策解读报告生成 · 同步读 + 异步真算写回

指标未见。报告生成不是已注册研报能力。核增研报 `report/jobs`（614–618）和 `gkxlumenx_gapfill.gapfill_policy_report_body` 不是这条资源。`FE-POL-07A` 不顶替本叶。

### 8.1 读面（并存）

公开资源：`POST /display/v1/policy/simulation/jobs`，种类=解读报告。表行种类是解读段落。一次请求不带文本解析，也不带重点、影响范围、路径预测。

- 同步读。不建任务。不另建报告行，不另建文件表
- 政策必选。少了政策则报告区空
- 一行是一个段落：所属政策、段落、正文。段落只用政策背景、主要内容、预期效果、实施建议，写在行上。段落的字段名由契约单冻结
- 页面呈现当次读到的正文。有解读段落行则报告区从这些行生成。没有则报告区空。有行不自动 create 真算
- **jobs 本资源**：不产生 PDF/Word 文件；响应不内嵌写死文件；不写对象存储；前端不直连 RustFS
- **下载（另轨，COVER 保留）**：浏览器走已有公开资源 `POST /display/v1/situation/report/generate`（`reportType=policy-interpret-report`），对齐 217 / 态势报告；PDF=`format=pdf`；Word=`format=html`→`.doc`。不新开 simulation 导出 URL，不走 `report/jobs`。自定义内容=章节勾选；自定义格式=Word/PDF。无解读段落行或不勾选则不发 generate
- 行上 `metric_id` 留空，不新造
- 不把 226 的摘要复制成本叶段落。不把评价页 224 的解读条目复制过来

空态：没有解读段落行则报告区空。HTTP 成功。不返回 501。不返回一份写死的文件。

### 8.2 真算写回（2026-11-13 ASYNC · 同构 238）

公开资源：`POST /display/v1/policy/evaluation/jobs`。

| 字段 | 值 |
|---|---|
| `sub_type` | `policy_sim_interpret` |
| `params.policy_id` | 必填 |
| `force` | 可选；无行可跑；有行且 `force≠true` 可短路已有；「重新生成」必须 `true` |
| `analysis_fp` | 条件指纹（同评价 jobs） |
| `skipsIndustryVidXor` | `true`（同 238） |

链路：display → topic-async → `/internal/policy/jobs/execute` → `polan.sim_interpret_job`：读 DWD 正文（可附加解析表 / 影响·路径摘要，无则不挡）→ LLM 四段 → **单政策 upsert** 解读段落（仅该 `policy_id` + `row_kind=解读段落` DELETE+INSERT；≥1 段非空才写库；`is_mock` 暂 1）。禁整表清空。禁核增 `report/jobs` / `gapfill_policy_report_body`。create 同步终态（同 238）。成功后前端再打 §8.1 读面。

空态：未选政策、无正文、无密钥/`generated=0` → 不写假四段、不 DELETE 旧行；读面仍空或保留旧行。HTTP 读面成功不 501。

## 9. 空态对照

237 的签收读法是查已有解析表。238、239、241、242 的签收读法是查 `gkxlumenx_gapfill.gapfill_policy_sim_result` 的对应行。240 无本页资源。无行则空。不用 501 充当功能。接口不直接返回写死的 mock。mock 若存在，只能先由灌数单落入缺项表，或已由既有管道写入解析表，再被查询读出来。查询不灌数。

| 序号 | 资源 | 无数据 |
|---|---|---|
| 237 | jobs · 文本解析 · 同步读 | 该政策无解析行则报告空。不调用 `polan.text.parse.run`。不灌 gapfill。返回时去掉 `clauses` 与 `clause_meta`，不整行丢弃。不返回 501。失败不清其他种类 |
| 238 | jobs · 重点可视化 · 同步读 | 未选政策，或没有重点行，则该区空。不返回预渲染图片。不返回 501。失败不清其他种类 |
| 239 | jobs · 影响范围 · 同步读 | 无影响范围行则该区空。不造全国兜底行。不读预估表，不读图计算。不返回 501 |
| 240 | 无资源 | 本分册不新建接口。关联网络只消费已有第 7 项读图。Java 不写 nGQL |
| 241 | jobs · 路径预测 · 同步读 | 未选政策，或没有路径环节行，则该区空。不推进环节，不写执行记录。不返回 501 |
| 242 | jobs · 解读报告 · 同步读（+ `policy_sim_interpret` 真算写回） | 没有解读段落行则报告区空。**jobs 不产生** PDF/Word、不写对象存储。下载另走 `situation/report`；无行不产文件。真算失败不灌假四段。不返回 501 |

## 10. 明确不做

- 不另建 API-POL。不冻结枚举、响应字段名、种类字段名和 DTO。交给 `BE-POL-CONTRACT-01`。
- 不写 OpenAPI 字段表。不写实现代码。不改 Python，不改 Java。不补推演控制器。
- 不改 `POL-L2-DS12-SIM-ARCH`、`POL-L2-DS12-EST-ARCH`，以及说明书、WBS、契约输入清单、调用链与边界、`指标与501.md`、调研分册和任何兄弟分册。
- 不新建作业入口。不建第二个分发器。不把整条 `simulation/jobs` 改成只读 `gkxlumenx_gapfill.gapfill_policy_sim_result`。
- 232–236 交给 `POL-L2-DS12-EST-API`。本分册不定义未出台仿真、新出台预测、区域空间、多维评估、利益攸关方的请求。不读 `gkxlumenx_gapfill.gapfill_policy_sim_forecast`，不读 `gkxlumenx_gapfill.gapfill_policy_sim_stakeholder`。
- 不新建 Python simulate job。不调用 `polan.text.simulate`。不读 `ads.policy_simulate`。不调用 `polan.text.parse.run`。不加 `policy_simulate`。**例外真算键**（已锁）：`policy_text_parse_run`（237）、`policy_sim_focus`（238）、`policy_sim_interpret`（242）进白名单与 `JOB_SUB_TYPES`；其余 239/241 与五次**读面**不进 `POST /internal/policy/jobs/execute` / async（真算写回见 §3.2 / §4.2 / §8.2）。
- 浏览器不改打 `/topic/v1/policy`、`/policy/topic/v1/policy`、`/topicAsync/**`、`/v1/policy/**`。不把 `E-E7-POLICY-M1-L06` 写成展示路径。不直连 `GET /v1/policy/text/parse`。
- 展示不直连 Python，不直连库，不打算法中台。不调用 `demo-*`。Java 不做 NLP，不写 nGQL。
- 不用 501 充当 237、238、239、241、242 的功能。无行则空。240 不另造 501 接口。
- 不新造 `metric_id`。不改 D4。不把 mock 写成已上线。不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开。不改模型注册表。不把 `M_POLICY_SIMULATE` 挂到 238、239、241、242。不挂 `M_POLICY_FOCUS_INDEX`、`M_POLICY_DS_11_POLICY_EVAL_015`、`M_POLICY_EFFECT_SCORE`、`M_POLICY_LAYOUT_REC_COUNT`、`M_POLICY_DEEP_171_1`。
- 237 不灌 gapfill，不写 `ads.policy_text_parse`。查询不灌数。不把 235、236 的种类定义写进本分册。
- jobs 解读报告不产生、不内嵌 PDF/Word；不灌假文件进 gapfill；不灌自定义格式配置列。242 下载复用已有 `situation/report`（见 §8），不新建桶、前端不直连 RustFS。
- 不把 `parse/jobs`、`parse/clauses`、`report/jobs`、`gkxlumenx_gapfill.gapfill_policy_report_body` 写成 237 或 242 的资源。
- 不改 `FE-POL-03A`，不新建前端单。前端 mock 开关不是接口实现。
- 不会签。不把本单标 done，不标 ready_to_sign。不改任务状态。

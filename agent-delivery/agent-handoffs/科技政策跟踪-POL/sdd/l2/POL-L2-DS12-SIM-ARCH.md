# POL-L2-DS12-SIM-ARCH · 政策效果推演 · 科技政策推演 · 后台实现架构设计

- 任务：`POL-L2-DS12-SIM-ARCH`
- 日期：2026-11-04
- 状态：架构稿已落盘，待架构、算法、数据、产品四角色会签。不标 done。2026-11-05 改过第 7、9 节的表张数与 235/236 灌数归属。同日按 `clause_job._write_default` 把 §1.4 的条款读法改为：同一 `policy_id` 仍读，返回时去掉 `clauses` 与 `clause_meta`
- 监管：`human:淮政玮`
- 认领：`agent:arch-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 图：`POL-L2-DS12-SIM-ARCH-SEQ`（本叶新图，源文件无 frontmatter，记 `draft`）

本叶只定政策效果推演二级「科技政策推演」的实现架构和整体流程。SRS 序号 **237–242**（level5 路径 `政策效果推演/科技政策推演`）。用户故事 `US-DS-POL-06`。不写 OpenAPI 字段、请求体、响应体、枚举。那是 `POL-L2-DS12-SIM-API`。

上游只引用，不改写：`政策效果推演.md` 237–242、说明书第 2 节 DS-12 与第 11.2 节、`sdd/调用链与边界.md`、`sdd/契约输入清单.md` 的 `simulation/jobs`、`sdd/指标与501.md` §3、`survey/DS-12.md`。不新造 `metric_id`，不改 D4。EST 半区（232–236）已由 `POL-L2-DS12-EST-ARCH` 落盘，本叶沿用其 §0 分组裁定，不搬表、不重复实现 235/236。

签收标准沿说明书第 11 节：可实现才签收。真算、真查或真模型做不到时，只接受新建表、把 mock 写入表、接口读表。不允许接口直接返回 mock。

## 0. 范围与表分组

本叶覆盖 **237–242 六叶**。表归属按说明书 11.2 与灌数单 DoD：238 重点、239 影响范围、241 路径、242 解读读 `gapfill_policy_sim_result`；236 利益攸关方已由 EST 半区裁定读 `gapfill_policy_sim_stakeholder`；**237 文本解析例外：读已有 `ads.policy_text_parse`，不建、不灌缺项行**（裁定见 §1.3）。

这样 EST-ARCH（232–236）与本叶（237–242）拼起来是完整的推演页，共用同一条资源 `POST /display/v1/policy/simulation/jobs`，不产生第二套资源，也不产生重叠叶。240 不设种类。

## 1. 迁移调查：算法中台对应实现的分析与裁定

任务执行说明要求：参考算法中台与本二级对应的政策实现；lumen 链路已有对应设计的沿用，没有的分析算法中台、把合理部分迁到 lumen 链路。逐叶调查结论如下。

### 1.1 算法中台现状（demo-ui-system-test + lumen-algo-py）

| 件 | 位置 | 实际内容 |
|---|---|---|
| 政策子菜单 | `demo-ui-system-test` `policyMenuConfig.ts` | 有 `/policy/parse`「文本解析 · 智能摘要」、`/policy/simulate`「效果推演 · 实施路径」两签；**没有**政策重点可视化、影响范围分析、政策关联分析、路径预测、解读报告的独立页 |
| 文本解析页 | `TextAnalysis.vue`「文本解析」签 | 左侧政策列表，点击渲染解析报告（摘要、自动标签、结构化要素逐项），读 `fetchTextParse` → `GET /policy/text/parse` |
| 中台读面 | `lumen-algo-py` `policy_routes.py` `GET /v1/policy/text/parse` | 按 `policy_id` / `limit` 拣行读 `ads.policy_text_parse` 全列 |
| 批产函数 | `polan.text.parse.run` | 规则截取：`summary`=截取 abstract\|content，`structured_elements`=结构化要素，`auto_tags`=自动标签；写入 `ads.policy_text_parse`，行上 `metric_id=M_POLICY_TEXT_PARSE`。**run() 会清空整表**。条款批次（`POL-CLAUSE-BATCH-L01`）对已有 `policy_id` 执行 `UPDATE`，把 `clauses`、`clause_meta` 写进同一条 `structured_elements`，不另插一行 |
| 摘要展示身份 | 评价页 226 已裁定 | 展示读键 `policy_text_parse`（Python `JOB_SUB_TYPES` 与 Java `PolicyAnalysisTypes` 白名单均已接通），只读不跑 `run()` |
| 其余四类 | 无 | 重点可视化、影响范围、路径预测、解读报告在中台没有模型、没有读面、没有函数 |

### 1.2 与需规的差距

需规 237 要结构化解析报告（关键词、核心内容、支持对象、申报条件、支持力度）；中台已有该读面，且解析要素就在 `structured_elements` 列里——**这一叶中台实现基本可迁，只差展示读面取全要素列**。238 要求图表、思维导图展示政策目标、支持领域、实施路径、资金安排四组重点；241 要求政策发布、申报受理、评审评估、资金拨付、效果评估五环节的时间与责任主体；242 要求背景、内容、效果、建议四段报告正文——中台均无实现，真实生成做不到。239 要求「基于政策效果推演结果」分析受益对象、影响区域、影响行业，依赖推演真值；推演键未注册，影响范围只能跟随已灌的模拟上下文行。

### 1.3 lumen 链路已有设计（沿用）

- 契约：推演整页只有一条资源 `POST /display/v1/policy/simulation/jobs`（`sdd/契约输入清单.md`）。237–242 不另立读面。
- 链路：浏览器只打 `/display/v1/policy/**`；展示不直连 Python、不直连库；`gkxlumen-display` → `gkxlumen-element` 只读，真算走 async-service → Python `/internal/*`。
- 分键：推演键 `M_POLICY_SIMULATE` 只挂 232–234 预测行（EST 裁定）；`M_POLICY_TEXT_PARSE` 的解析读面已有评价页 226 先例（`POL-L2-DS11-READ-ARCH` §4.4：只读、不跑 `run()`）；`M_POLICY_DEEP_171_1` / `M_POLICY_LAYOUT_REC_COUNT` 是布局推荐键，不进 237–242；240 走第 7 项读图。
- 契约「明确不做」写明：`M_POLICY_TEXT_PARSE` 不为推演**单开 URL**。本裁定不开 URL，237 在同一条 `simulation/jobs` 资源上按种类分发读已有的解析表，不违反该条。

### 1.4 迁移裁定

| 对象 | 裁定 |
|---|---|
| 中台读面 `GET /v1/policy/text/parse`、demo「文本解析 · 智能摘要」签 | 留在原地服务算法中台，不迁、不改、不删。展示不直连、不嵌入 |
| `polan.text.parse.run` | 留作中台与灌数批产。展示请求**不调用**：run() 会清空整张 `ads.policy_text_parse`，一次展示请求会把条款行一起清掉（评价 226 同款约束） |
| 解析报告形态（摘要 + 自动标签 + 结构化要素逐项，`metric_id=M_POLICY_TEXT_PARSE`） | **合理部分，采纳**：展示 237 直接读已有解析行，行内已具备需规要求的摘要、标签与要素；行上 `metric_id` 不改 |
| 展示读面取列 | 现有评价 226 的读面只取 `summary` 一列；237 需要标题、摘要、标签与结构化要素。展示读法取 `title / summary / auto_tags / structured_elements`，仍是只读，不跑 `run()`。该取列口径由 DATA / API 单落成字段 |
| 条款隔离 | 条款批次更新同一条解析行，不另插条款行。展示 237 仍读该行的标题、摘要、标签和其余要素。返回 `structured_elements` 时去掉 `clauses` 与 `clause_meta`，条款树不进入解析报告。不因行内有这两个键整行丢弃 |
| 重点 / 影响范围 / 路径 / 解读 | 中台无实现。按签收标准走缺项表 `gapfill_policy_sim_result`，行内容范式：逐项要素 + 一句说明，图表渲染在前端 |
| 真模型演进 | `M_POLICY_SIMULATE` 注册为可调用服务后，影响范围改随真推演结果。**237 真算（2026-11-12 方案 C 三卡）**：新键 `policy_text_parse_run` 进白名单；旧 `policy_text_parse` 仍只读不跑 `run()` |

迁移之后的最终架构一句话：**浏览器只打 `/display/v1/policy/simulation/jobs`（读面）与 `/display/v1/policy/evaluation/jobs`（237/238/242 真算键）；237 读面由 element 只读 `ads.policy_text_parse`，真算走 `policy_text_parse_run` 单政策 upsert 后再读；238 真算走 `policy_sim_focus`；242 真算走 `policy_sim_interpret`；239/241 仍只读 gapfill；240 读图；算法中台读面留原地，无任何 demo 依赖。**

## 2. 实现架构

推演页契约只有一条资源 `POST /display/v1/policy/simulation/jobs`。推演页可接统计读面为 0（`sdd/指标与501.md` §3），本二级没有同步统计卡，全部区块走这一条资源按种类分发。机制沿用 EST-ARCH 裁定：缺项读面不进异步管道、不建任务记录、无 SSE。

| 叶子 | 种类 | 迁移后的读法 |
|---|---|---|
| 237 | 文本解析 | **读面**：element 只读 `ads.policy_text_parse`（去 `clauses`/`clause_meta`）。**真算**：`policy_text_parse_run` → async → 单政策五要素 upsert（禁 `run()`） |
| 238 | 重点可视化 | **读面**：element 只读 `gapfill_policy_sim_result` 的重点行。**真算**：`policy_sim_focus` → async → 单政策 upsert 重点行 |
| 239 | 影响范围 | element 只读 `gapfill_policy_sim_result` 的影响范围行，跟随该政策上下文 |
| 241 | 路径预测 | element 只读 `gapfill_policy_sim_result` 的路径环节行 |
| 242 | 解读报告 | **读面**：element 只读 `gapfill_policy_sim_result` 的解读段落行。**真算**：`policy_sim_interpret` → async → 单政策 upsert 解读段落 |
| 240 | （无种类） | 跨项索引。消费第 7 项子图，不设资源 |
| （真模型，未注册） | 真推演 | async-service → Python `/internal/*`。模型未注册 → 该能力空态，不填数 |

```mermaid
flowchart LR
  fe["推演页 · 科技政策推演 237-242"]
  gw["gkxlumen-gateway"]
  bff["gkxlumen-display /display/v1/policy/simulation/jobs"]
  el["gkxlumen-element 只读"]
  adsP["ads.policy_text_parse 解析行"]
  simr["gapfill_policy_sim_result 重点/影响/路径/解读行"]
  graph["第 7 项读图 · 政策子图"]
  fe --> gw --> bff
  bff -->|"237 种类"| el
  el --> adsP
  bff -->|"238 239 241 242 种类"| el
  el --> simr
  graph -.->|"240 关联网络：页面前端消费"| fe
```

| 生产者 | 消费者 | 触发 | 失败语义 | 禁止事项 |
|---|---|---|---|---|
| 解析行由已有灌数 / 条款跑批管道写 `ads.policy_text_parse`；重点、影响、路径、解读行由 `data-agent` 按 `POL-L2-DS12-SIM-GAPFILL-L01` 灌 mock 行 | `gkxlumen-element` 只读，经 `gkxlumen-display` 原样返回 | 用户打开文本解析报告、点政策看重点、看影响范围、看实施路径、看解读报告 | 无行则该区空。一次种类查询失败不清其他种类已返回区块 | POST 不创建持久任务记录，不进 `gkxlumen-topic-async-service`，无 SSE、无进度条。237 不调用 `polan.text.parse.run`。不写 ODS、DWD、ADS 新表、供应方库。不把 demo 本地数组或 `/v1/policy/text/parse` 当接口。240 不建查图任务 |

`gkxlumen-display` 不直连库、不直连 Python，不写算法，不写 nGQL。`E-E7-POLICY-M1-L06` 不是本页路径。trace 沿既有展示链走，display 往 element 带 traceId，本叶不新设计观测点。

同一条 `simulation/jobs` 一次只带一种类。232–236 的种类由 EST-ARCH 在同一条资源上分发，本叶不实现、不改挂。某种类无行时该区空，其他区块照常——「真模型未注册则空态」约束的是真推演能力，缺项行与已有解析行是说明书第 11 节签收标准允许的读表退路，两者并存不冲突。

## 3. 各叶的输入条件

条件只来自需规原文。下表是用户要做选择或查看的上下文，不是参数名，也不是响应字段。参数名与枚举留给 `POL-L2-DS12-SIM-API`。未列出的条件不收。

| 序号 | 用户要看 | 必选 | 落到哪次读取 |
|---|---|---|---|
| 237 | 选一条政策看结构化解析报告 | 政策必选；该政策无解析行则报告空 | `jobs` 的文本解析 |
| 238 | 对该政策查看目标、领域、路径、资金四组重点与明细说明 | 政策必选；无重点行则该区空 | `jobs` 的重点可视化 |
| 239 | 基于推演上下文看受益对象、区域、行业的范围与时空分布 | 政策或推演上下文必选；无行则该区空 | `jobs` 的影响范围 |
| 241 | 看五环节时间安排与责任主体的流程说明 | 政策必选；无路径行则该区空 | `jobs` 的路径预测 |
| 242 | 看背景、内容、效果、建议四段解读正文 | 政策必选；无解读行则该区空 | `jobs` 的解读报告 |

### 3.1 条件从哪来

展示原型 `demo-ui-science` 推演页右半区（科技政策推演）为复刻壳（`FE-POL-03A`），六子区只定布局，不定义数据源。中台「文本解析 · 智能摘要」签按政策列表点选，本页沿用该交互语义：解析、重点、路径、解读都以一条政策为中心展开；影响范围额外要求推演上下文（契约注明「影响范围只跟该次结果」）。不迁中台常量，不迁 `/v1` 读面。

## 4. 整体流程

1. 用户在科技政策推演区选一条政策看文本解析。前端提交 `jobs`（种类=文本解析）。element 读该政策的解析行：标题、摘要、自动标签、结构化要素（关键词、支持对象、申报条件、支持力度等要素在行内 `structured_elements`）。无行则报告空，不现场跑解析，不返回条款行顶替。
2. 用户查看政策重点。前端提交 `jobs`（种类=重点可视化）。element 读该政策的重点行：目标、支持领域、实施路径、资金安排逐项与明细说明。思维导图、图表在前端渲染，服务端只返回行。
3. 用户查看影响范围。前端提交 `jobs`（种类=影响范围），带上当前推演上下文的政策。element 按政策拣影响范围行：受益对象、影响区域、影响行业与时空分布说明。真推演未接通前，这些行是已灌的模拟上下文行；真推演接通后改随真结果（§1.4）。
4. 用户查看实施路径。前端提交 `jobs`（种类=路径预测）。element 读该政策的路径环节行：发布、受理、评审、拨付、评估五环节的时间安排与责任主体。流程图在前端渲染。
5. 用户查看解读报告。前端提交 `jobs`（种类=解读报告）。element 读该政策的解读段落行：政策背景、主要内容、预期效果、实施建议。页面呈现正文即「查看」。**无行**时可点「生成解读报告」走 `evaluation/jobs`（`sub_type=policy_sim_interpret`）真算写回后再读；**有行**不自动起算，可「重新生成」（`force=true`）。用户可在页内勾选章节（内容自定义，不持久化配置、不灌假配置列），并选择 Word / PDF 下载。下载**不走** `simulation/jobs`，走已有 `POST /display/v1/situation/report/generate`（`reportType=policy-interpret-report`）→ topic-async OpenHTMLtoPDF；PDF=`format=pdf` 真字节；Word=`format=html` 同源 HTML 存为 `.doc`（与 217 同构）。无行或不勾选章节则不产文件。不接核增 `report/jobs`，不灌假 PDF/Word 进 gapfill。
6. 用户想看政策关联网络。页面直接消费第 7 项读图（政策子图，`M_POLICY_RELATION_DEGREE`）。不走 `simulation/jobs`，本页不新建查图任务。

某一次 `jobs` 失败，不清其他种类已经返回的区块。本页没有可接统计读面，空态与失败态都按区块独立呈现。

## 5. 分叶

### 5.1 237 政策文本智能解析 · 读已有解析表 + 异步真算写回

指标 `M_POLICY_TEXT_PARSE`，MODEL，D4=mock。评价页 226 仍只读同表 `summary`。

- **读面**：表 `ads.policy_text_parse`，按 `policy_id` 读。返回去掉 `clauses`、`clause_meta`。取 `title / summary / auto_tags / structured_elements`（四中文键：核心内容 / 支持对象 / 申报条件 / 支持力度）
- **真算 Job 键**：`policy_text_parse_run`（2026-11-12 三卡）。`POST /display/v1/policy/evaluation/jobs` → topic-async → `/internal/policy/jobs/execute` → `polan.text_parse_run_job`：规则优先 + 残量 LLM → **单政策 upsert**（merge 保留 `clauses`/`clause_meta`）。**禁止** `polan.text.parse.run()` / 整表 TRUNCATE
- 不复用中台 `structure_one` / `/clauses/enrich`（条款切条 ≠ 五要素）
- 旧键 `policy_text_parse`：**仍同步只读**，不改建任务（226 红线）
- 界面：检索任意政策 →「解析」→ 进度 → 读回；无正文/失败「暂无解析结果」
- 行上 `metric_id` 仍是 `M_POLICY_TEXT_PARSE`
- 空态：无行报告空；真算失败不写假四键

不做什么：浏览器直连 Python；demo 服务；把条款树当解析报告；改 226 只读语义。

### 5.2 238 政策重点可视化展示 · 读缺项表 + 异步真算写回

无专属 `metric_id`。读面仍只读缺项表；**真算（2026-11-12 ASYNC · 同构 237 C）** 另走 Job 写回后再读。

- 表 `gkxlumenx_gapfill.gapfill_policy_sim_result`，种类为重点
- 一行是一个重点项：所属政策、组别（政策目标 / 支持领域 / 实施路径 / 资金安排）、标题、明细、`score_value`
- **柱图（COVER-FDE 卡1=B）**：复用 `score_value`；不 ALTER、不新 `metric_id`；同组取非空最大。element/display **不改 SELECT**
- **真算 Job 键**：`policy_sim_focus`。`POST /display/v1/policy/evaluation/jobs` → topic-async → `/internal/policy/jobs/execute` → `polan.sim_focus_job`：读 DWD 正文 → LLM 抽四组+得分 → **单政策 upsert** 重点行（禁整表清空 / 禁 `parse.run` 式 TRUNCATE）
- 只读并存：`jobs·重点可视化` 仍同步读 gapfill（当天已成功可直接打开）；按钮「可视化展示」可 force 重算
- `M_POLICY_FOCUS_INDEX` 不挂本叶
- 空态：无行「没有政策重点行」/「暂无政策重点」；有行无分「暂无得分」。禁从 `detail_text` 解析柱高

不做什么：浏览器直连 Python；demo 服务；本单扩 239/241 真算（242 见 §5.5）；返回预渲染图片。

### 5.3 239 政策影响范围分析 · 读缺项表（跟随推演上下文）

无专属指标。需规写明「基于政策效果推演结果」，推演键未注册；契约注明「影响范围只跟该次结果」。

- 同一张 `gapfill_policy_sim_result`，种类为影响范围
- 一行是一个影响对象：所属政策（推演上下文）、类别（受益对象 / 影响区域 / 影响行业，枚举以需规原文三类为界）、名称、一句说明、时间变化说明
- 覆盖面：`coverage_rate` / `eligible_count` / `covered_count`（受益对象行）；渗透深度：`penetration_score`（区域/行业行）
- 空间分布是行的区域维度数据，热力图、地图渲染在前端，服务端只返回行
- 真推演接通后，影响范围改随该次真推演的结果行；在此之前是已灌的模拟上下文行。切换不改资源、不改种类键
- 行上 `metric_id` 留空，不新造
- 空态：无行则该区空，不造全国通用兜底行；覆盖率三字段皆空则覆盖面卡业务空态

不做什么：不把 234 的区域空间预测行（EST 组表）复制成本叶影响范围。不把第 7 项图谱查询写成影响范围的计算源。

### 5.4 241 政策实施路径预测 · 读缺项表

指标未见。`M_POLICY_LAYOUT_REC_COUNT` 是布局推荐键的计数件，不顶替本叶；`M_POLICY_DS_11_POLICY_EVAL_015` 落在评价页 229，也不顶替（调研已核对）。

- 同一张 `gapfill_policy_sim_result`，种类为路径环节
- 一行是一个环节：所属政策、环节（政策发布 / 申报受理 / 评审评估 / 资金拨付 / 效果评估，枚举以需规原文五环节为界）、时间安排、责任主体、一句说明。流程图由这些行构成，渲染在前端
- **界面必见**：仅「政策实施流程图」（时间轴五环节 + 节点说明）。需规「基于历史数据」= 预测依据语义；**不**设历史对照读口、**不**灌历史行、真轨**不**挂「历史评估图」卡（2026-11-12 需规分句闭合卡1=A）。原型 mock 对照卡可留，非正式必见
- 环节是预测展示，不是流程引擎：请求处理不推进环节状态，不写执行记录
- 行上 `metric_id` 留空，不新造
- 空态：无行则该区空，不在接口里编时间表

不做什么：不把布局推荐的建议条数填进本叶。不把评价页 229 的路径与风险方案复制过来。不建流程审批或任务派生。不补「历史评估」行列或第二张读表。

### 5.5 242 政策解读报告生成 · 读缺项表 + 异步真算写回

指标未见，关键词「解读」查询为 0 条；报告生成为未注册研报能力。`FE-POL-07A`（核增智能研报，US-DS-POL-10）不顶替本叶；`FE-POL-05A` 不顶替 237。读面仍只读缺项表；**真算（2026-11-13 ASYNC · 同构 238）** 另走 Job 写回后再读。三卡锁 A：过程壳同 237/238；表继续 gapfill；主输入 DWD 正文，解析/推演有则拼 prompt、无则不挡。

- 表 `gkxlumenx_gapfill.gapfill_policy_sim_result`，种类为解读段落
- 一行是一个段落：所属政策、段落（政策背景 / 主要内容 / 预期效果 / 实施建议，枚举以需规原文四段为界）、`body_text`
- **真算 Job 键**：`policy_sim_interpret`。`POST /display/v1/policy/evaluation/jobs` → topic-async → `/internal/policy/jobs/execute` → `polan.sim_interpret_job`：读 DWD title/abstract/content（可附加 `ads.policy_text_parse` 与同表影响/路径摘要）→ LLM 四段 → **单政策 upsert** 解读段落（`DELETE … WHERE policy_id=? AND row_kind='解读段落'` 再 INSERT；禁整表清空 / 禁误删重点/影响/路径；≥1 段非空才写库；无密钥/`generated=0` 不 DELETE、不造假行）。`force`：有行且未 force 可短路已有；重算必 `force=true`
- 只读并存：`jobs·解读报告` 仍同步读 gapfill（有行直接看、不自动 create）；主按钮无行「生成解读报告」、有行「重新生成」
- （2026-11-12 COVER-FDE 卡1=B）**下载保留**：章节勾选 + Word/PDF 走 `situation/report`（`reportType=policy-interpret-report`）；jobs 只返段落、不内嵌文件。无行不产文件
- 行元数据真算路径：`is_mock=1`（本波不伪改绿）、`fill_method=llm`、`gap_item=242 政策解读报告生成`；`metric_id` 留空
- 空态：无行则报告区空；真算失败诚实空态/保留旧行；不在接口里写死全文

不做什么：不把核增研报五叶 `report/jobs`、`gapfill_policy_report_body` 当成本叶表。不新建 ADS 解读表。不把 226 的摘要 / 评价页 224 解读条目复制成本叶段落。不开完整 I2-12 任务浮层。

### 5.6 240 政策关联分析 · 跨项索引（2026-11-12 需规分句闭合卡1=B）

指标 `M_POLICY_RELATION_DEGREE`（GRAPH，D4=mock），调研判跨项索引。

- **不设** `simulation/jobs` 种类，**不灌** `gapfill_policy_sim_result` 关联行。
- **展示只读挂接**：浏览器 `GET /display/v1/policy/simulation/relation-graph?policy_id=&steps=&limit=` → display Feign `GET /topic/v1/policy/graph` → Python `GET /internal/policy/graph`（Nebula 优先，ADS `policy_graph_node/edge` 回退）。
- 界面必见：政策关联网络图（节点/边）；协同效应与体系位置说明（优先图侧 props；无则前端邻域统计一句，不造假分）。
- 空图诚实返回空 `nodes/edges`；Java 不写 nGQL、不填假网；本页不新建查图任务、不重画查图时序。
- `E-E7-POLICY-M1-L06` 不是实现路径，浏览器不改打专题 URL。抽取脚本 `GDF-POLICY-GRAPH-EXT-L01` 仍 backlog；样例不足时允许最小种子入 MySQL+图谱（非 gapfill_sim）。

## 6. 点名排除

| 资源或对象 | 不纳入本二级的原因 |
|---|---|
| 232–236 五叶 | EST-ARCH 半区。235 多维评估行、236 参与意见行已裁定，本叶不重复实现 |
| 240 关联分析 jobs/gapfill 资源化 | 跨项索引。不设 `simulation/jobs` 种类、不建关联缺项表；仅允许 display 透传已有 `/topic/v1/policy/graph` |
| `M_POLICY_DEEP_171_1`、`M_POLICY_LAYOUT_REC_COUNT` | 布局推荐键。不进推演页任何区；`FE-POL-03A` 页头「布局建议」卡槽是复刻壳 |
| `ads.policy_simulate`、`polan.text.simulate`、`/v1/policy/simulate` | 效果推演读面与批产闭包，归 EST 半区裁定。留原地，展示不直连不迁移 |
| `GET /v1/policy/text/parse`、demo「文本解析」签 | 算法中台读面。留原地，展示不直连不嵌入；展示读法走本叶 §5.1 |
| `polan.text.parse.run` 进请求路径 | run() 清空整表，会连带清掉条款行。解析批次只在已有管道跑 |
| `parse/jobs`、`parse/clauses` | 核增拆解页资源（606 语义理解、607/608 条款树）。判别键与用途不同，不为 237 复用 |
| `report/jobs`、`gapfill_policy_report_body` | 核增智能研报五叶。242 不是研报 |
| `M_POLICY_FOCUS_INDEX`、`M_POLICY_DS_11_POLICY_EVAL_015`、`M_POLICY_EFFECT_SCORE` | 评价页指标。不挂 238、241 |
| `M_POLICY_SIMULATE` 挂到 235–242 行 | 推演键只挂 232–234 预测行（EST 裁定）。本叶各缺项行 `metric_id` 留空 |
| 异步白名单（历史口径） | **已修订**：237 加 `policy_text_parse_run`；238 已有 `policy_sim_focus`；242 加 `policy_sim_interpret`。评价 226 的 `policy_text_parse` 只读键保持原状 |
| `E-E7-POLICY-M1-L06`、专题政策 URL | 不是展示实现路径 |

## 7. 明确不做

- 不写 OpenAPI 字段表、请求体、响应体、枚举、种类键名落库格式。
- 不新造 `metric_id`。不改 D4。不改模型注册表。不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开。
- 不改写 `sdd/指标与501.md`、说明书、调研分册、契约输入清单。那些文件里 237–242 仍写着 501。本叶的可实现链路是读表。会签前不以本叶改写它们。
- 浏览器不改打专题 URL 或 `/v1/**`。不把 `E-E7-POLICY-M1-L06` 写成展示路径。
- 不重开 GDF，不写 nGQL，不建查图任务。不加 ODS、DWD、ADS 新表。缺项行只进 `gkxlumenx_gapfill` 已定名的两张 SIM 组表：`gapfill_policy_sim_result`、`gapfill_policy_sim_stakeholder`。本叶四种（238、239、241、242）只进第一张。235 的多维评估行也进第一张，236 的参与意见行进第二张。不把这两张收成一张，也不另建第三张。
- 不在本叶改 Python 或 Java。不进 `PolicyAnalysisTypes`，不进 async-service。预计实现是：五类读面由 element 查询；237 的取列与条款行判别随既有解析表读取实现。
- 不直连、不迁移算法中台读面与 `demo-ui-system-test` 页面。lumen 链无任何 demo 运行时依赖（D12）。
- 不改 `FE-POL-03A`，不新建前端单。前端 mock 开关不是接口实现。
- 不允许接口函数直接返回 mock。
- 不会签。不把本单标 done。

## 8. 签收条件：可实现

六叶都有一条现在就能照着做的链路。写成「以后再选解析 / 生成模型」，或者接口直接返回写死的报告、重点、路径、影响行，本单不可签收。

| 序号 | 可实现的做法 | 现在就能用的依据 |
|---|---|---|
| 237 | element 读 `ads.policy_text_parse` 解析行（title/summary/auto_tags/structured_elements），请求不跑解析 | `polan.text.parse.run` 已落库真实行；评价 226 已按只读先例消费同表 |
| 238 | 建 `gapfill_policy_sim_result` 重点行，`jobs` 只查这些行 | 中台无重点可视化模块；说明书 11.2 已点名该表 |
| 239 | 同表影响范围行，跟随政策上下文，渲染在前端 | 推演键未注册；契约注明影响范围只跟该次结果 |
| 241 | 同表路径环节行，五环节枚举以需规为界 | 无路径预测模型；两处相近指标（171 计数、015）调研均判不顶替 |
| 242 | 同表解读段落行读面 + `policy_sim_interpret` 真算 upsert；下载另轨 `situation/report` | 同构 238；关键词「解读」0 条；`FE-POL-07A` 文案区分 |
| 240 | 不设 jobs 种类；display `relation-graph` 透传第 7 项子图 | 调研判跨项索引；2026-11-12 卡1=B |

迁移边界重申：算法中台页面留在 `demo-ui-system-test`；`/v1/policy/text/parse` 等读面继续给算法中台自己用；展示不打 `/v1`，不迁 `run()`；`ads.policy_text_parse` 继续由已有管道写入，展示只读。真模型注册后对应能力切 async 真算，对外 URL 不变。

## 9. 表与要灌的 mock（本叶组）

SIM 组缺项表是说明书 11.2 点名的两张，都在库 `gkxlumenx_gapfill`：`gapfill_policy_sim_result`、`gapfill_policy_sim_stakeholder`。不进 ODS、DWD、ADS，不写供应方库。本叶四种（重点、影响范围、路径环节、解读段落）只放第一张，不为此再拆表。236 的参与意见只放第二张。读法由 EST-ARCH §5.5 定，本叶不改行内容口径。灌数仍由 `POL-L2-DS12-SIM-GAPFILL-L01` 执行，与 EST §9 一致。

237 **不灌缺项行**：解析真行已由已有管道落在 `ads.policy_text_parse`。说明书 11.2 把「文本解析」写在 SIM 组要灌清单里，本叶按第 11 节总规则收窄——已有表与已有产出的，不建缺项行（评价 READ-ARCH 对 `gapfill_policy_eval_focus` / `gapfill_policy_eval_summary` 的同款先例）。`POL-L2-DS12-SIM-GAPFILL-L01` 开工时按本裁定执行：该单 DoD 的「文本解析」不灌。要灌的是多维评估（235）、参与意见（236）、重点、影响范围、路径、解读正文。不把「其余」理解成再灌文本解析或文件。

重点行、影响范围行、路径环节行、解读段落行共四种，字段级 DDL 由 `POL-L2-DS12-SIM-DATA` 定，灌数由 `POL-L2-DS12-SIM-GAPFILL-L01` 执行，本叶不执行。

每种行都带 `metric_id`（238/239/241/242 的行留空）、`gap_item`、`fill_method`、`gapfill_batch_id`、`generated_at`。`fill_method` 用 `manual`。`gap_item` 写序号和叶子名。D4 保持 mock。

| 种类 | 叶子 | 要灌的 mock | 不灌 |
|---|---|---|---|
| 重点 | 238 | 四组逐项行：组别、标题、明细；**可写 `score_value` 作柱图**（COVER-FDE 卡1=B） | `M_POLICY_FOCUS_INDEX`/焦点指数算法分、预渲染图片、解析标签改挂 |
| 影响范围 | 239 | 三类行：类别、名称、说明、时间变化、区域原文；覆盖率三字段；渗透指数 | 全国通用兜底行、地图文件、真推演结果 |
| 路径环节 | 241 | 五环节行：环节、时间安排、责任主体、一句说明 | 布局推荐条数、流程执行记录、评价页 015 的方案路径 |
| 解读段落 | 242 | 背景、内容、效果、建议四段正文行 | PDF / Word 文件、自定义格式配置、核增研报正文 |

文本解析行不灌（§5.1，读已有 `ads.policy_text_parse`）。235 多维评估行灌进 `gapfill_policy_sim_result`，236 参与意见行灌进 `gapfill_policy_sim_stakeholder`。读法由 EST-ARCH 定，灌数由本叶灌数单执行，本叶不改这两行已经写明的行内容。

行要能按第 3 节的条件拣出来：全部按所属政策拣，影响范围额外按推演上下文。条件对不上的行不返回。

灌数单执行人是 `data-agent`，监管 `human:淮政玮`，状态 backlog。它依赖本架构和 `POL-L2-DS12-SIM-DATA`。本叶不认领、不执行。查询请求不灌数。

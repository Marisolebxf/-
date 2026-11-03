# POL-L2-DS10-SENT-ARCH · 科创政策全景 · 政策舆情评估

- 任务：`POL-L2-DS10-SENT-ARCH`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:arch-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 图：`POL-L2-DS10-SENT-ARCH-SEQ`（本叶新图，源文件无 frontmatter，记 `draft`）

本叶只定科创政策全景二级「政策舆情评估」的实现架构和整体流程。SRS 序号 **207–212**。用户故事 `US-DS-POL-03`。不写 OpenAPI 字段、请求体、响应体、枚举。那是 `POL-L2-DS10-SENT-API`。

上游只引用，不改写：`科创政策全景.md` 207–212、`sdd/调用链与边界.md`、`sdd/契约输入清单.md`、`sdd/指标与501.md`、`survey/DS-10.md` 207–212、`sdd/l2/POL-L2-DS10-QRY-ARCH.md`。不新造 `metric_id`，不改 D4。

签收条件（`human:淮政玮`，2026-11-03）：架构必须能实现。真实计算或真实采集做不到时，只接受一种替代：新建数据库表，把 mock 写入表，接口读表。不允许接口直接返回 mock。209、212 能复刻已有算法并读已有 ADS 表，不走这条例外。210、211 走这条例外。

## 1. 范围

六叶都在全景里完成，不另开页，不另开路径。前缀 `/display/v1/policy/`。

| 序号 | 叶子 | 需规摘要 | 本叶流程 |
|---|---|---|---|
| 207 | 政策查询与对比 | 按类型、地域、时期查询，并同时查看多条政策正文 | 同步，复用多维检索已定的门面委托 |
| 208 | 区域政策差异性分析 | 按地区对比覆盖、力度、实施条件 | 跨项读图。本叶不新开资源 |
| 209 | 政策实施效果跟踪 | 执行情况、受益反馈、社会影响和效果指标 | 当前 501。接通时复刻算法库「效果评估」，不新写公式 |
| 210 | 政策受众反馈收集 | 问卷、在线评价、意见征集及汇总 | 没有采集服务。新建缺项表并灌入 mock 行，接口只读表 |
| 211 | 政策效果评估报告 | 自动生成达成度、社会影响、问题与建议，并可下载 | 没有评估报告通道。新建缺项表并灌入 mock 行，接口只读表 |
| 212 | 政策匹配与推送 | 按企业规模、行业、发展阶段匹配，并以通知或邮件推送 | 当前 501。接通时复刻算法库「匹配推送」，不新写公式 |

207 的 D4 仍是 `mock`。`GDF-POLICY-MOCK-GATE-L01` 仍是 blocked。闸门未解开时，正式值仍是 mock。本叶不把 mock 写成已上线。

## 2. 实现架构

本二级只用契约输入清单里已经点名的资源。208 不设资源。

| 叶子 | 资源 | 流程 |
|---|---|---|
| 207 | `GET /display/v1/policy/panorama/stats`、`search`、`{id}/detail` | 同步。浏览器只打这三条。`gkxlumen-display` 内部委托 `gkxlumen-topic-policy`，对照与 `POL-L2-DS10-QRY-ARCH` 相同 |
| 208 | 不设 `/display/v1/policy` 资源 | 只消费第 7 项已有子图。挂接可空 |
| 209 | `POST /display/v1/policy/panorama/jobs` | 当前 501。接通后委托已有 `polan.eval.effect`，不进专题政策门面 |
| 212 | `POST /display/v1/policy/panorama/jobs` | 当前 501。接通后委托已有 `polan.text.match`，不进专题政策门面 |
| 210 | `GET /display/v1/policy/panorama/feedback` | Python 只查 `gkxlumenx_gapfill.gapfill_policy_audience_feedback`。接口不写死问卷 |
| 211 | `GET /display/v1/policy/panorama/assessment-report` | Python 只查 `gkxlumenx_gapfill.gapfill_policy_assessment_report`。接口不写死报告 |

```mermaid
flowchart LR
  fe["全景 · 政策舆情评估 207-212"]
  gw["gkxlumen-gateway"]
  bff["gkxlumen-display /display/v1/policy"]
  tp["gkxlumen-topic-policy"]
  py["Python /internal/policy"]
  async["gkxlumen-topic-async-service"]
  graph["第 7 项已有子图"]
  gap["gkxlumenx_gapfill 两张缺项表"]
  fe --> gw --> bff
  bff -->|"207：stats / search / detail"| tp --> py
  bff -->|"208：只消费，可空"| graph
  bff -->|"209：jobs，复刻 effect，读 ads.policy_effect"| async --> py
  bff -->|"212：jobs，复刻 match，读 ads.policy_match"| async --> py
  bff -->|"210 211：只查 gapfill 表"| py --> gap
```

浏览器只打 `/display/v1/policy/**`，不改去打 `/policy/topic/v1/policy/**`。`E-E7-POLICY-M1-L06` 不是本二级的实现路径。

207 复用多维检索已经定下的内部委托：`stats` 对 metrics / indicators，`search` 对 search，正文对 `docs/{id}`。展示不直连 Python，不直连 `gkx_search_service`，也不再为这三条建 `gkxlumen-element` 的 policy 包。并列查看是多次读正文，不新开对比引擎。

209、212 不进专题政策门面。任务表、SSE、并发锁复用 `gkxlumen-topic-async-service`。切条件不自动起任务。Job 失败不清空 207 已经返回的统计卡、目录和正文。

`gkxlumen-display` 不直连库，不写算法，不写 nGQL。

## 3. 整体流程

1. 用户做政策查询或页内并列查看。前端调 `stats`、`search`，打开一条时调 `{id}/detail`。207 读政策总数、类型分布、级别分布，以及目录和正文。无行则对应位置空，不造 0。数值在对齐前仍是 mock。
2. 用户要看区域差异。本叶不发新的政策资源。子图能读到则只消费第 7 项已有结果；读不到则该块空。地区件数若只画统计，走第 1 步里已有的全国分布、深圳分布，不把 208 改判成统计读面。
3. 用户要看实施效果。前端向 `jobs` 提交。签收链路是读 `ads.policy_effect` 里 `scope_type=region_effect` 的落地实效，不展示算法库页面上的柱状图本身。sub_type 未挂上时，不得用 501 或手写效果数顶上。
4. 用户要收集或查看受众反馈。前端调 `feedback`。Python 只查 `gapfill_policy_audience_feedback`。表里没有行则列表空。请求处理不写死问卷或评价。
5. 用户要看或下载效果评估报告。前端调 `assessment-report`。Python 只查 `gapfill_policy_assessment_report`。表里没有行则报告空。下载内容来自该行，不在接口里放一份写死的报告。
6. 用户要做政策匹配或推送。前端向 `jobs` 提交。签收链路是按主体读 `ads.policy_match` 的 Top 记录和理由。sub_type 未挂上时，不得用 501 或演示分顶上。通知和邮件不走序号 202 的 `share`，也不走序号 204 的 `subscriptions`。

## 4. 六叶

### 4.1 207 政策查询与对比 · 同步

读已有资源：

- `stats`：`M_POLICY_TOTAL_COUNT`、`M_POLICY_TYPE_DIST`、`M_POLICY_LEVEL_DIST`
- `search`：类型、地域、时期落在目录查询上
- `{id}/detail`：同时查看多条政策时，按条读正文

链路与多维检索 197、198、200 相同：前端 → 网关 → `gkxlumen-display` → `gkxlumen-topic-policy` → Python `/internal/policy`。

空态：不返回 501。无行则统计卡、列表或正文空，不造 0。D4 保持 mock。

不做什么：不新造对比指标。不把「识别优缺点」写成已有模型。深度交叉对比不在本叶，不改走 `compare/jobs`。不把序号 213 的新旧对比、214 的详情力度写进这三条资源。

### 4.2 208 区域政策差异性分析 · 跨项读图

读已有指标：`M_POLICY_GRAPH_107_1`。类型 GRAPH，D4 仍是 mock。本行不改判。

流程：不新开 `/display/v1/policy` 资源。政策子图任务 `E-E7-POLICY-M1-L02` 已完成。抽取脚本 `GDF-POLICY-GRAPH-EXT-L01` 仍是 backlog。展示只消费第 7 项已有子图，Java 不写 nGQL。挂接可空。

地区件数可以复用 `stats` 上已有的 `M_POLICY_NATIONAL_DIST`、`M_POLICY_SZ_DIST`。那是序号 197 的统计读面，不把 208 改成可接统计读面。需规里的支持力度、实施条件不在本行计算。支持力度是序号 216 的 `M_POLICY_SUPPORT_STRENGTH`。

不做什么：不走 `E-E7-POLICY-M1-L06`。不把专题门面的 `/graph` 改成展示浏览器地址。不重做抽取，不重开 GDF。

### 4.3 209 政策实施效果跟踪 · 当前 501，接通时复刻效果评估

读已有资源：`POST /display/v1/policy/panorama/jobs`。指标 `M_POLICY_IMPLEMENTATION_EFFECT`，MODEL，D4=mock。QPOL-02。

参照实现是算法库「效果评估」页（`demo-ui-system-test` 的 `EffectEval.vue`）。页头写明 demo 数据为 mock，算法为轻量真实实现。计算在 `demo-algo-ent-analysis/polan/eval/effect.py`：按区域写 `ads.policy_effect`（`scope_type=region_effect`），执行维用政策侧有效率与力度，社会维和环境维是受控随机代理。落地实效写入 `ads.policy_metric_timeseries`，`metric_id` 为 `M_POLICY_IMPLEMENTATION_EFFECT`。同一次计算还写出效果评分 `M_POLICY_EFFECT_SCORE`，本叶不改挂这条。读面是 `GET /v1/policy/analysis/effect`。

`lumen-algo-py/vendor/entan-py` 里有同一份 `polan/eval/effect.py` 和同一条读路由。正式入口 `lumen_algo_service/main.py` 没有挂它。`RemotePolicyPythonClient` 也没有效果读面。`/internal/policy/jobs/execute` 的 sub_type 不含效果评估。所以展示侧现在仍是 501。

目标链路（可照此实现）：

1. 浏览器只提交 `POST /display/v1/policy/panorama/jobs`，带 `M_POLICY_IMPLEMENTATION_EFFECT`。不打开算法中台页，不打 `/v1/policy/analysis/effect`。
2. `gkxlumen-display` 不打分。它调用已有 `gkxlumen-topic-async-service` 的 `POST /topic/v1/analysis/tasks`。对外不暴露 `/topicAsync/**`。
3. 已有 `PolicyAnalysisAdapterImpl` 经 `RemotePolicyJobPythonClient` 调用 `POST /internal/policy/jobs/execute`，下游是 `gkxlumen-platform-entan-py:8000`。现在白名单只有 `policy_timeseries`、`policy_regional`、`policy_shenzhen`、`policy_focus`，效果评估会被拒绝。
4. 迁移只加一个 sub_type：`policy_effect`。Python 收到后调用仓库里已有的 `polan.eval.effect.run`，再读 `ads.policy_effect` 中 `scope_type=region_effect` 的行，以及 `policy_metric_timeseries` 里 `metric_id=M_POLICY_IMPLEMENTATION_EFFECT` 的行，原样放进 Job 结果。不新写公式，不新表。
5. `PolicyAnalysisTypes` 把 `policy_effect` 放进白名单。这条不走「产业链码与技术领域二选一」校验，因为算法中台是按区域对政策表计算。Java 仍不打分。

sub_type 尚未放行时，这次 Job 返回空结果，响应里不带写死的区域列表或分数。放行之后，表里无行则结果空，也不造 0。社会维、环境维在采购数据到位前由 `run()` 写入表，接口只读表。D4 不改。同一次计算写出的 `M_POLICY_EFFECT_SCORE` 不改挂到本叶。这张区域表不是序号 211 的评估报告。

空态：算法库页面上的柱和表不是展示服务。同一指标在推演页的 page_use 不在本叶展开。切条件不自动起任务。

不做什么：不把本叶改判成统计读面。不因 501 清空 207 的目录和正文。不把 `M_POLICY_DEEP_168_1` 挂到本行。

### 4.4 210 政策受众反馈收集 · 读缺项表

读已有资源：`GET /display/v1/policy/panorama/feedback`。政策域没有反馈统计指标，也没有采集服务。真实采集做不到。

按签收条件，只建一张缺项表，不在接口里返回 mock：

- 库 `gkxlumenx_gapfill`，表 `gapfill_policy_audience_feedback`。不写入 ODS、DWD、ADS。
- 问卷、在线评价、意见征集以行写入这张表。灌数是独立脚本，不是请求处理。
- 浏览器仍打上面的展示路径。`gkxlumen-display` 不直连库，转发到 Python `/internal/policy` 的只读查询，由 Python `SELECT` 这张表。不把反馈放进专题政策查询门面。
- 表里没有行则列表空，不造一条反馈。D4 保持 mock，因为行是灌入的 mock，不是采集实数。

不做什么：不新造反馈 `metric_id`。不把序号 201 的收藏、序号 204 的订阅写成受众反馈。不把页面演示或控制器里的样例当成这条资源。

### 4.5 211 政策效果评估报告 · 读缺项表

读已有资源：`GET /display/v1/policy/panorama/assessment-report`。本序号没有专属 `metric_id`，也没有评估报告通道。真实生成做不到。

按同一签收条件：

- 库 `gkxlumenx_gapfill`，表 `gapfill_policy_assessment_report`。不写入 ODS、DWD、ADS。
- 达成度、社会影响、问题与建议以行写入这张表。灌数是独立脚本。
- `gkxlumen-display` 不直连库，转发到 Python `/internal/policy` 的只读查询，由 Python `SELECT` 这张表。下载内容从读到的行生成，响应里不内嵌一份写死的报告。不把报告放进专题政策查询门面。
- 表里没有行则报告空。不写对象存储，不建 Job。

不做什么：不挂 `M_POLICY_DEEP_168_1`。不把序号 217 的对标报告、核增研报 `report/jobs` 当成这张报告。不把前端 HTML 写成评估报告服务。

### 4.6 212 政策匹配与推送 · 当前 501，接通时复刻匹配推送

读已有资源：`POST /display/v1/policy/panorama/jobs`。指标 `M_POLICY_MATCH`、`M_POLICY_INDUSTRY_FIT`，都是 MODEL，D4=mock，`srs_refs` 为空。QPOL-03。

参照实现是算法库「匹配推送」页（`demo-ui-system-test` 的 `TextAnalysis.vue`）。计算在 `demo-algo-ent-analysis/polan/text/match.py`：按主体对政策打分，产业命中、地区或国家级普适、诉求重合、未过期四段相加，每主体取 Top 8，写入 `ads.policy_match`，`metric_id` 为 `M_POLICY_MATCH`。主体画像在参照实现里是受控随机生成的，不是企业登记主数据。读面是 `GET /v1/policy/match`，按 `subject_id` 返回政策标题、`match_score` 和 `match_reasons`。`M_POLICY_INDUSTRY_FIT` 在 vendor 指标表上读同一张 `policy_match`，不另写一套打分。

`lumen-algo-py/vendor/entan-py` 里有同一份 `polan/text/match.py` 和 `GET /v1/policy/match`。正式入口 `lumen_algo_service/main.py` 没有挂它。展示 Java 没有匹配读面。`/internal/policy/jobs/execute` 的 sub_type 不含匹配。所以展示侧现在仍是 501。

目标链路与 209 同一条 Job 管道，sub_type 用 `policy_match`：

1. 浏览器提交 `POST /display/v1/policy/panorama/jobs`。`M_POLICY_MATCH` 与 `M_POLICY_INDUSTRY_FIT` 都映射到这一个 sub_type，因为算法中台把两条都落在 `ads.policy_match`。不打开算法中台页，不打 `/v1/policy/match`。
2. `gkxlumen-display` 调用已有 `POST /topic/v1/analysis/tasks`。`PolicyAnalysisAdapterImpl` 再调 `POST /internal/policy/jobs/execute`。
3. Python 调用仓库里已有的 `polan.text.match.run`，再按主体读 `ads.policy_match`（政策标题、`match_score`、`match_reasons`、`rank_no`）放进 Job 结果。不新写打分，不第二套产业适配。
4. 白名单增加 `policy_match`。这条同样不套用产业链锚点校验。主体沿用算法中台现有的受控画像，直到企业登记主数据接入；本叶不另造主体表。

sub_type 尚未放行时，这次 Job 返回空列表，不返回演示分。放行之后，该主体无行则列表空。分数只来自 `ads.policy_match` 的查询结果。D4 保持 mock。`E-E7-POLICY-M1-L03` 仍只索引焦点、力度、效果，不改展示 URL。

推送通道不是序号 202 的导出分享，也不是序号 204 的订阅外发。没有发信通道时，Job 只返回匹配列表，不另造通知或邮件。

不做什么：不新造匹配指标。不把产业适配写成 207 的目录筛选。不把算法库页面上的 35 分演示行当成展示服务。

## 5. 点名排除

| 资源或序号 | 不纳入本二级的原因 |
|---|---|
| `panorama/rank`、`favorites`、`share` | 序号 199、201、202。门面三单是 `E-E7-POLICY-M1-L08`、`L09`、`L10` |
| `panorama/ingest`、`subscriptions` | 序号 203、204 |
| 205、206 | 时序、热力、热点与深度报告。热点走 `jobs`，但是 205 的未见模型，不是 209、212 |
| 213–218 | 新旧对比、详情力度、部门件数、标杆力度、对标报告与对标可视化 |
| `compare/jobs`、`report/jobs` | 核增对比与研报。不是 207 的并列查看，也不是 211 的评估报告 |

## 6. 明确不做

- 不写 OpenAPI 字段表、请求体、响应体、枚举。
- 不新造 `metric_id`。不改 D4。不把 mock 写成已上线。
- 不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开。
- 浏览器不改打 `/topic/v1/policy`。不把 `E-E7-POLICY-M1-L06` 写成展示路径。
- 不改 `FE-POL-01A`、`FE-POL-01B`，不新建前端单。
- 不重开 GDF，不写 nGQL。不加 ODS、DWD、ADS 表。210、211 只加 `gkxlumenx_gapfill` 里上面两张 `gapfill_` 表。
- 不在本叶改 Python 或 Java。209、212 的预计实现是挂已有 `polan.eval.effect`、`polan.text.match`，不新写公式，也不把它们送进专题政策门面。
- 不把算法库页面、写死效果数、演示打分、前端 HTML 写成展示服务。
- 不允许接口函数直接返回 mock。mock 只能先落进表，再被查询读出来。
- 不会签。不把本单标 done。

## 7. 签收条件：可实现

六叶各自有一条现在就能照着做的链路。有一条写成「以后再选算法」，或者接口直接返回写死的数据，本单不可签收。

能接到已有表的，接口必须查那张表。209 查 `ads.policy_effect`，212 查 `ads.policy_match`。`run()` 先把结果写入表，Job 再查询；查询函数自己不拼区域列表，不拼匹配分。表里没有行就返回空。

实在没有算法、也没有表的，只允许这一条退路：在 `gkxlumenx_gapfill` 新建 `gapfill_` 前缀表，由 Python 把 mock 行写入表，接口只做查询。210、211 走这条。不接受第二种退路。

| 序号 | 可实现的做法 | 现在就能用的代码 |
|---|---|---|
| 207 | 展示读 `stats` / `search` / `{id}/detail`，内部委托专题政策门面 | `gkxlumen-topic-policy` 与 `/internal/policy` 的 search、docs、metrics、indicators 已在跑 |
| 208 | 不新开资源。有子图则只消费第 7 项，没有则该块空 | `E-E7-POLICY-M1-L02` 已完成。展示不写 nGQL |
| 209 | 在已有 `jobs/execute` 上增加 `policy_effect`，调用 `polan.eval.effect.run`，读 `ads.policy_effect` | 计算与 `GET /v1/policy/analysis/effect` 已在 `lumen-algo-py/vendor/entan-py`。任务管道是 `PolicyAnalysisAdapterImpl` |
| 210 | 建 `gapfill_policy_audience_feedback`，Python 灌入 mock 行，`feedback` 只查这张表 | 算法中台没有反馈采集模块，也没有现成表 |
| 211 | 建 `gapfill_policy_assessment_report`，Python 灌入 mock 行，`assessment-report` 只查这张表 | 算法中台没有报告生成模块。效果评估页的区域表不当成报告 |
| 212 | 在已有 `jobs/execute` 上增加 `policy_match`，调用 `polan.text.match.run`，读 `ads.policy_match` | 计算与 `GET /v1/policy/match` 已在同一份 vendor。与 209 共用任务管道 |

迁移边界：

- 算法中台页面留在 `demo-ui-system-test` 与 `lumen-ui-algo-apiview` 的 `/policy/effect`、`/policy/match`。展示不嵌这些页，浏览器不打 `/v1/policy/**`。
- `/v1/policy/analysis/effect` 与 `/v1/policy/match` 继续给算法中台自己用。展示走 `/internal/policy/jobs/execute` 的新 sub_type，函数仍是这两条读面背后的 `run()`。
- 不把 `polan.eval.effect`、`polan.text.match` 抄进 Java，不抄进 `gkxlumen-display`，不送进专题政策查询门面。
- 不新造 `metric_id`，不改 D4。209、212 不另建表。社会维、环境维、匹配主体的受控代理由已有 `run()` 写入 ADS，采购或主数据到位后再换输入，不在本叶换公式。
- `gkxlumen-display` 今天还没有全景控制器。实现时按契约补资源：207 委托已有门面；209、212 走已有 Job 管道并查 ADS；210、211 只查两张 `gapfill_` 表。任何一条都不在接口函数里返回 mock。

## 8. 表与合规 mock

界面上要出现、而真实采集或真实主数据还没有的数，先写入表，并标成 mock。接口只查询。D4 保持 mock，不把灌数写成已上线。不新造 `metric_id`。字段级 DDL 由 data-agent 在灌数单里定。本叶只定粒度和必须落表的内容。灌数单本叶不执行。

| 序号 | 库表 | 新建 | 合规上要落表的 mock | 灌数单 |
|---|---|---|---|---|
| 207 | 已有政策目录与统计读面 | 否 | 不新灌。无行则空 | 无 |
| 208 | 已有政策子图 | 否 | 不建表。无子图则空 | 无 |
| 209 | `ads.policy_effect`（`scope_type=region_effect`）、`ads.policy_metric_timeseries` | 否 | 社会维、环境维是受控代理（QPOL-02：执行监测、宏观经济、社会发展数据待采购）。执行维按政策侧算出后，与这两维一起写入同一行。行上的扩展信息保留 `is_mock` 和缺口说明。落地实效写入时序表，`metric_id` 仍是 `M_POLICY_IMPLEMENTATION_EFFECT` | `POL-L2-DS10-SENT-MOCK-ADS` |
| 210 | `gkxlumenx_gapfill.gapfill_policy_audience_feedback` | 是 | 反馈主体、渠道（问卷、在线评价、意见征集）、意见正文、可选评分、关联政策、时间。每行标记 mock。没有真实问卷 | `POL-L2-DS10-SENT-MOCK-210` |
| 211 | `gkxlumenx_gapfill.gapfill_policy_assessment_report` | 是 | 范围、达成度、社会影响、问题、建议、报告正文。每行标记 mock。不是序号 209 的区域评分，也不是对标报告 | `POL-L2-DS10-SENT-MOCK-211` |
| 212 | `ads.policy_match` | 否 | 受控主体画像（不是企业登记主数据）、政策、`match_score`、`match_reasons`、`rank_no`。`metric_id` 用已有 `M_POLICY_MATCH`。产业适配读同一张表，不另灌一套 | 与 209 同一张 `POL-L2-DS10-SENT-MOCK-ADS`，执行已有 `polan.text.match.run` |

三张灌数单的执行人是 `data-agent`，监管 `human:淮政玮`，状态 backlog，依赖本架构和 `POL-L2-DS10-SENT-DATA`。`MOCK-ADS` 只跑仓库里已有的 `polan.eval.effect.run` 与 `polan.text.match.run`，不改公式，不另建 ADS 表。`MOCK-210`、`MOCK-211` 只在 `gkxlumenx_gapfill` 建表并灌数，不写入 ODS、DWD、ADS。查询请求不灌数。

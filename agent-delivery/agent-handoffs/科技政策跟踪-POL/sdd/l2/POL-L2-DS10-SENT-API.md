# POL-L2-DS10-SENT-API · 科创政策全景 · 政策舆情评估 · 后台接口设计

- 任务：`POL-L2-DS10-SENT-API`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:api-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-03`
- 上游：`sdd/l2/POL-L2-DS10-SENT-ARCH.md`（2026-11-03 `human:淮政玮` 已签收。本分册以它为准，不改它）

本分册只定科创政策全景二级「政策舆情评估」的后台接口。SRS 序号 **207–212**。它是 `BE-POL-CONTRACT-01` 的输入，不是第二份 API-POL。不另建契约文件。枚举闭包、响应字段名和 DTO 仍由那一张契约冻结。这里只写路径、方法、内部委托、同步或 Job、空态。不写 OpenAPI 字段表，不写实现代码。

流程以 `POL-L2-DS10-SENT-ARCH` 为准。契约输入清单里全景的 `stats`、`search`、`{id}/detail`、`jobs`、`feedback`、`assessment-report` 只作资源名对照。清单末列的旧空态不覆盖本分册。207 与多维检索共用的三条 GET，参数名沿 `POL-L2-DS10-QRY-API`，本分册不重列、不改那份分册。

签收口径：做不到的只允许缺项表灌 mock 后由接口读表。209、212 读已有 ADS，不另建表。不灌假推送。不允许接口直接返回 mock，也不用 501 充当功能。

## 偏离

本二级 DoD 里「不复用 `/topic/v1/policy`」指浏览器不改打专题 URL。`gkxlumen-display` 内部委托 `gkxlumen-topic-policy`，以及 209、212 内部调用 `gkxlumen-topic-async-service` 的 `POST /topic/v1/analysis/tasks`，都算内部委托，不算违反这句 DoD。浏览器仍只打 `/display/v1/policy/**`。对外不暴露 `/topicAsync/**`。不改 `ARCH-DISPLAY-01`。`E-E7-POLICY-M1-L06` 不是展示联调单，也不是本二级的实现路径。

## 1. 公开资源

前缀 `/display/v1/policy/`。六叶都在全景里完成，不另开页，不另开路径。208 不设资源。209 与 212 共用同一条 `jobs`。

| 序号 | 公开资源 | 读法 |
|---|---|---|
| 207 | `GET /display/v1/policy/panorama/stats` | 同步。内部委托 metrics + indicators。不返回 501 |
| 207 | `GET /display/v1/policy/panorama/search` | 同步。内部委托 search。不返回 501 |
| 207 | `GET /display/v1/policy/panorama/{id}/detail` | 同步。内部委托 `docs/{id}`。不返回 501 |
| 208 | 不设 `/display/v1/policy` 资源 | 只消费第 7 项已有子图。挂接可空 |
| 209 | `POST /display/v1/policy/panorama/jobs` | Job。`sub_type=policy_effect`。查 `ads.policy_effect`。无行则空。不返回 501 |
| 212 | 同一条 `POST /display/v1/policy/panorama/jobs` | Job。`sub_type=policy_match`。查 `ads.policy_match`。无行则空。不返回 501，不返回演示分 |
| 210 | `GET /display/v1/policy/panorama/feedback` | 同步。element 只读缺项表。无行则空列表。不返回 501 |
| 211 | `GET /display/v1/policy/panorama/assessment-report` | 同步。element 只读缺项表。无行则报告空。不返回 501 |

`{id}` 是 `search` 目录项里的政策 id，与 `POL-L2-DS10-QRY-API` 相同。

`panorama/jobs` 在契约输入清单里还挂着其它叶子。本分册只定 209 的 `policy_effect` 与 212 的 `policy_match`。其余 sub_type 不在这里展开，也不改写成这两叶。

## 2. 内部委托

浏览器经网关打 `gkxlumen-display`。网关只转 `/display/**`。

展示不直连 Python，不直连 `gkx_search_service`，不直连库。不打算法中台 `/v1/policy/match`，也不打 `/v1/policy/analysis/effect`。Java 不写算法，不打分，不写 nGQL。不调用任何 `demo-*` 服务。

| 公开资源 | 内部委托 |
|---|---|
| `panorama/stats` | `gkxlumen-display` → `gkxlumen-topic-policy`：`GET /topic/v1/policy/metrics`，分布再取 `GET /topic/v1/policy/indicators` |
| `panorama/search` | `gkxlumen-display` → `gkxlumen-topic-policy`：`GET /topic/v1/policy/search` |
| `panorama/{id}/detail` | `gkxlumen-display` → `gkxlumen-topic-policy`：`GET /topic/v1/policy/docs/{id}` |
| 208 | 无展示资源，不委托专题门面 `/graph`。只消费第 7 项已有子图 |
| `panorama/jobs` | `gkxlumen-display` → `gkxlumen-topic-async-service` `POST /topic/v1/analysis/tasks` → 已有 `PolicyAnalysisAdapterImpl` → `POST /internal/policy/jobs/execute` |
| `panorama/feedback` | `gkxlumen-display` 不直连库。`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_audience_feedback`。不进专题政策门面 |
| `panorama/assessment-report` | `gkxlumen-display` 不直连库。`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_assessment_report`。不进专题政策门面 |

207 的三条与多维检索 197、198、200 同一条门面委托，不另建 `gkxlumen-element` 的 policy 包。209、212 不进专题政策查询门面。任务表、SSE、并发锁复用 `gkxlumen-topic-async-service`。`/internal/policy/jobs/execute` 的下游是 `gkxlumen-platform-entan-py`。算法中台页面留在 `demo-ui-system-test` 与 `lumen-ui-algo-apiview`，展示不嵌这些页。

`policy_effect` 与 `policy_match` 是白名单上要增加的两个 sub_type。例外只加在这两条：它们不走产业链码与技术领域的二选一校验（产业 VID XOR）。其它 sub_type 仍按已有校验。Java 仍不打分。

切条件不自动起任务。用户提交 `jobs` 之后才建任务。Job 失败不清空 207 已经返回的统计卡、目录和正文。

trace 沿既有展示链。同步读在 display 往下带 traceId。Job 沿已有异步任务链。本分册不新设计观测点。

## 3. 207 政策查询与对比 · 同步

三条叶子资源与多维检索共用，不拆第二套后端。浏览器只打 `stats`、`search`、`{id}/detail`。

- `stats`：读 `M_POLICY_TOTAL_COUNT`、`M_POLICY_TYPE_DIST`、`M_POLICY_LEVEL_DIST`。display 先读 metrics，再读 indicators。数字原样上送，Java 不改口径
- `search`：类型、地域、时期落在目录查询上，原样委托已有 `GET /topic/v1/policy/search`。查询参数名沿 `POL-L2-DS10-QRY-API`，取值闭包留给契约单
- `{id}/detail`：display 把 `{id}` 交给 `GET /topic/v1/policy/docs/{id}`。不走门面的 `/{id}` 兜底

并列查看是按条多次读正文。每条各打一次 detail。不开 `compare/jobs`，不新开对比引擎。

空态：无行则对应统计卡、列表或正文空。HTTP 成功。不造 0。不返回 501。

D4 仍是 mock。`GDF-POLICY-MOCK-GATE-L01` 仍是 blocked。闸门未解开时，正式值仍是 mock。本分册不把 mock 写成已上线，不改 D4。

不新造对比指标。不把「识别优缺点」写成已有模型。深度交叉对比不在本叶。序号 213 的新旧对比、214 的详情力度不写进这三条资源。`stats` 上另有的全国分布、深圳分布、覆盖和力度，不挂本叶去改口径；地区件数若只画统计，仍是序号 197 的读面。

## 4. 208 区域政策差异性分析 · 不设资源

本叶不新开 `/display/v1/policy` 资源。浏览器没有专供 208 的新路径。

只消费第 7 项已有子图。指标 `M_POLICY_GRAPH_107_1`，类型 GRAPH，D4 仍是 mock。本分册不改判。政策子图任务 `E-E7-POLICY-M1-L02` 已完成。抽取脚本 `GDF-POLICY-GRAPH-EXT-L01` 仍是 backlog。展示不重做抽取，不重开 GDF。

子图能读到则只消费已有结果。读不到则该块空。Java 不写 nGQL。不把专题门面的 `/graph` 改成展示浏览器地址。不走 `E-E7-POLICY-M1-L06`。

地区件数可以复用 `stats` 上已有的 `M_POLICY_NATIONAL_DIST`、`M_POLICY_SZ_DIST`。那仍是序号 197 的统计读面。208 不因此改成可接统计读面，也不为此加一条展示资源。需规里的支持力度、实施条件不在本叶计算。支持力度是序号 216 的 `M_POLICY_SUPPORT_STRENGTH`。

## 5. 209 政策实施效果跟踪 · jobs

公开资源：`POST /display/v1/policy/panorama/jobs`。指标 `M_POLICY_IMPLEMENTATION_EFFECT`。浏览器提交这一条，带该指标。display 内部落到 `sub_type=policy_effect`。字段名由契约单冻结。

链路：

1. 浏览器只打 `POST /display/v1/policy/panorama/jobs`。不打开算法中台页，不打 `/v1/policy/analysis/effect`。
2. `gkxlumen-display` 不打分。它调用 `POST /topic/v1/analysis/tasks`。浏览器不打 `/topicAsync/**`。
3. 已有 `PolicyAnalysisAdapterImpl` 经 `RemotePolicyJobPythonClient` 调用 `POST /internal/policy/jobs/execute`。
4. Python 调用仓库里已有的 `polan.eval.effect.run`（`lumen-algo-py/vendor/entan-py` 已有这份实现）。`run()` 先写入表。不新写公式，不新表。
5. Job 再查询 `ads.policy_effect` 中 `scope_type=region_effect` 的行，以及 `ads.policy_metric_timeseries` 中 `metric_id=M_POLICY_IMPLEMENTATION_EFFECT` 的对应时序。结果原样放进 Job 结果。查询不拼区域列表，不写效果数。

`policy_effect` 不走产业 VID XOR。算法中台按区域对政策表计算，不是产业链码与技术领域二选一。这是该 sub_type 的例外。`PolicyAnalysisTypes` 把 `policy_effect` 放进白名单。现在白名单只有 `policy_timeseries`、`policy_regional`、`policy_shenzhen`、`policy_focus`。尚未放行时，这次 Job 返回空结果，响应里不带写死的区域列表或分数。放行之后，表里无行则结果空，也不造 0。

社会维、环境维在采购数据到位前由已有 `run()` 写入表，接口只读表。同一次计算写出的 `M_POLICY_EFFECT_SCORE` 不挂本叶。这张区域表不是序号 211 的评估报告。D4 保持 mock。

切条件不自动起任务。Job 失败时，207 已经返回的统计、目录和正文保持原样。

展示不把算法库页面上的柱和表当成响应。不把本叶改判成统计读面。不挂 `M_POLICY_DEEP_168_1`。

## 6. 212 政策匹配与推送 · 同一 jobs

公开资源与 209 相同：`POST /display/v1/policy/panorama/jobs`。指标 `M_POLICY_MATCH`、`M_POLICY_INDUSTRY_FIT` 都映射到 `sub_type=policy_match`。两条都落在 `ads.policy_match`，不另写一套打分。

链路与第 5 节同一条管道，到 Python 之后改为：

1. 调用仓库里已有的 `polan.text.match.run`。`run()` 先写入 `ads.policy_match`。不新写打分，不第二套产业适配。
2. Job 再按主体查询 `ads.policy_match`（政策标题、`match_score`、`match_reasons`、`rank_no`），原样放进 Job 结果。分数只来自这次查询。

`policy_match` 同样不走产业 VID XOR。主体沿用算法中台现有的受控画像，直到企业登记主数据接入。本叶不另造主体表。白名单增加 `policy_match`。尚未放行时，这次 Job 返回空列表，不返回演示分。放行之后，该主体无行则列表空。

没有外发通道时，推送记录为空。Job 只返回匹配列表，不另造通知或邮件，不灌假推送。通知和邮件不走序号 202 的 `share`，也不走序号 204 的 `subscriptions`。

D4 保持 mock。`E-E7-POLICY-M1-L03` 仍只索引焦点、力度、效果，不改展示 URL。不把产业适配写成 207 的目录筛选。不把算法库页面上的演示行当成展示服务。

切条件不自动起任务。Job 失败不清空 207 已经返回的统计、目录和正文。

## 7. 210 政策受众反馈收集 · 同步

公开资源：`GET /display/v1/policy/panorama/feedback`。

政策域没有反馈统计指标，也没有采集服务。浏览器仍打上面的展示路径。`gkxlumen-display` 不直连库。`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_audience_feedback`。不把反馈放进专题政策门面，也不把查询转到 Python 现造一行。

问卷、在线评价、意见征集以行在这张表里。灌数是独立脚本（`POL-L2-DS10-SENT-MOCK-210`），不是请求处理。本分册不写 DDL。列由 `POL-L2-DS10-SENT-DATA` 定。表不写入 ODS、DWD、ADS。

无行则空列表。HTTP 成功。不造一条反馈。不在接口函数里返回写死的问卷或评价。不返回 501。

D4 保持 mock。行是灌入的 mock，不是采集实数。不新造反馈 `metric_id`。不把序号 201 的收藏、序号 204 的订阅写成受众反馈。

## 8. 211 政策效果评估报告 · 同步

公开资源：`GET /display/v1/policy/panorama/assessment-report`。

本序号没有专属 `metric_id`，也没有评估报告通道。`gkxlumen-display` 不直连库。`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_assessment_report`。不把报告放进专题政策门面。

达成度、社会影响、问题与建议、报告正文以行在这张表里。灌数是独立脚本（`POL-L2-DS10-SENT-MOCK-211`），不是请求处理。本分册不写 DDL。表不写入 ODS、DWD、ADS。

下载内容来自读到的该行。不新建桶，不写对象存储，不走 `report/jobs`。不在接口里放一份写死的报告。

无行则报告空。HTTP 成功。不返回 501。

不挂 `M_POLICY_DEEP_168_1`。不把序号 217 的对标报告、核增研报 `report/jobs` 当成这张报告。不把 209 的区域评分当成评估报告。不把前端 HTML 写成评估报告服务。D4 保持 mock。

## 9. 空态对照

六叶的签收读法都是查已有读面或查表。无行则空。不用 501 充当功能。

| 序号 | 资源 | 无数据 |
|---|---|---|
| 207 | stats / search / detail | 统计卡、目录或正文空。不造 0。不返回 501 |
| 208 | 不设资源 | 子图读不到则该块空。不新开路径去填一块差异 |
| 209 | jobs · `policy_effect` | `ads.policy_effect` 无 `region_effect` 行则 Job 结果空。不写死效果数。不返回 501。失败不清空 207 |
| 212 | jobs · `policy_match` | 该主体在 `ads.policy_match` 无行则列表空。不返回演示分。没有外发通道则推送记录为空。不返回 501 |
| 210 | feedback | 缺项表无行则空列表。不造反馈。不返回 501 |
| 211 | assessment-report | 缺项表无行则报告空。下载没有行就不产生文件。不返回 501 |

209、212 的 sub_type 尚未放行时，同样返回空结果或空列表，不改用写死的效果数或演示分。

## 10. 明确不做

- 不另建 API-POL。不冻结枚举、响应字段名和 DTO。交给 `BE-POL-CONTRACT-01`。
- 不写 OpenAPI 字段表。不写实现代码。不改 Python，不改 Java。
- 不改 `POL-L2-DS10-SENT-ARCH`、`POL-L2-DS10-QRY-API`、`POL-L2-DS10-QRY-ARCH`、`POL-L2-DS10-TREND-ARCH`，以及说明书、WBS、契约输入清单、调用链与边界、指标与 501、其它兄弟分册。
- 不改 `ARCH-DISPLAY-01`。不把 `E-E7-POLICY-M1-L06` 写成展示联调单。
- 浏览器不改打 `/topic/v1/policy`、`/policy/topic/v1/policy`、`/topicAsync/**`。
- 展示不直连 Python，不直连 `gkx_search_service`，不打 `/v1/policy/match` 与 `/v1/policy/analysis/effect`。不调用 `demo-*`。
- 不用 501 充当 207–212 的功能。无行则空，不造 0。
- 不新造 `metric_id`。不改 D4。不把 mock 写成已上线。不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开。
- 208 不新开资源。Java 不写 nGQL。
- 209、212 不另建 ADS 表。不把 `policy_effect`、`policy_match` 的产业 VID XOR 例外扩大到其它 sub_type。查询不灌数。
- 210、211 的建表与灌数不在本分册执行。不把反馈或报告放进专题政策门面。
- 211 不新建桶，不走 `report/jobs`。212 不走 202 的 `share`、204 的 `subscriptions`，不灌假推送。
- 207 的并列查看不开 `compare/jobs`。
- 不改 `FE-POL-01A`、`FE-POL-01B`，不新建前端单。
- 不会签。不把本单标 done。

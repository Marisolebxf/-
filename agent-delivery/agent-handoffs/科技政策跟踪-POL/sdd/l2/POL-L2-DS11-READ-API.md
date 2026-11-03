# POL-L2-DS11-READ-API · 政策分析评价 · 结果解读报告多维展示 · 后台接口设计

- 任务：`POL-L2-DS11-READ-API`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:api-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-05`
- 上游：`sdd/l2/POL-L2-DS11-READ-ARCH.md`（2026-11-03 `human:淮政玮` 已签收。本分册以它为准，不改它）

本分册只定政策分析评价二级「结果解读报告多维展示」的后台接口。SRS 序号 **223–226**。它是 `BE-POL-CONTRACT-01` 的输入，不是第二份 API-POL。不另建契约文件。枚举闭包、响应字段名和 DTO 仍由那一张契约冻结。这里只写路径、方法、内部委托、同步或 Job、空态。不写 OpenAPI 字段表，不写实现代码。

流程以 `POL-L2-DS11-READ-ARCH` 为准。契约输入清单里评价页已经点名的 `evaluation/counts`、`evaluation/shells`、`evaluation/jobs` 只作资源名对照。清单、`指标与501.md`、说明书、WBS、调研里仍写的 501 空态不覆盖本分册。

签收口径：223 短板、223 焦点、226 摘要读已有 ADS，不另建表。224、225 只允许缺项表灌 mock 后由接口读表。不允许接口直接返回 mock，也不用 501 充当功能。无行则空。

## 偏离

两处与上游 DoD 字面不一致。本分册写明，不回头改那些文件。

1. DoD「不复用 `/topic/v1/policy`」指浏览器不改打专题政策 URL。`gkxlumen-display` 内部调用 `gkxlumen-topic-async-service` 的 `POST /topic/v1/analysis/tasks`，再由已有 `PolicyAnalysisAdapterImpl` 调用 `POST /internal/policy/jobs/execute`，是内部委托，不是浏览器改打 `/topic/v1/policy`。对外不暴露 `/topicAsync/**`。不改 `ARCH-DISPLAY-01`。`E-E7-POLICY-M1-L06` 不是展示联调单，也不是本二级的实现路径。
2. DoD 原文写着「焦点/解读/多媒体/摘要 501」（注册表完成标准里的「501 空态」同指这一句）。`指标与501.md` 仍把 223 焦点、224、225、226 写成 501、页面空态。2026-11-03 已签收架构把这四叶改成读表：焦点读 `ads.policy_focus`，解读与多媒体读 `gapfill_policy_eval_shell`，摘要读 `ads.policy_text_parse.summary`。本分册按签收架构写。空态是空，HTTP 成功，不返回 501。不改 `指标与501.md`、说明书、WBS、调研、契约输入清单，也不改同目录正在写的 VIZ、PLAN。

223 短板在 `指标与501.md` 里本来就是可接统计读面，不是上面那句 501。它的读法仍是查表。无行则计数空，不造 0，同样不返回 501。

## 1. 公开资源

前缀 `/display/v1/policy/`。四叶都在政策分析评价里完成，不另开页，不另开路径。本二级对外只有下面三条。223 的焦点和 226 的摘要共用同一条 `jobs`，本分册只给定两个新键。

| 序号 | 公开资源 | 读法 |
|---|---|---|
| 223 短板条数 | `GET /display/v1/policy/evaluation/counts` | 同步。element 只读 `ads.policy_effect` 且 `scope_type=region_gap` 的 `shortboard_cnt`。GET 不调用 `gap.run`。无行则计数空，不造 0。不返回 501 |
| 223 焦点指数 | `POST /display/v1/policy/evaluation/jobs` | Job。新键 `policy_focus_ads`。调用已有 `polan.eval.focus.run` 后读 `ads.policy_focus` 且 `policy_id` 非空的行。无行则焦点块空。不返回 501 |
| 224 解读条目、225 多媒体条目 | `GET /display/v1/policy/evaluation/shells` | 同步。element 只读 `gkxlumenx_gapfill.gapfill_policy_eval_shell`。点选只筛选已返回行。无行则空。不返回 501 |
| 226 摘要 | 同一条 `POST /display/v1/policy/evaluation/jobs` | Job。新键 `policy_text_parse`。只查 `ads.policy_text_parse.summary`。请求里不调用 `parse.run`。无行则摘要空。不返回 501 |

`evaluation/counts`、`evaluation/jobs`、`evaluation/shells` 上还有别的二级。本分册不把整条资源改成只服务 223–226，也不改写那些种类。`counts` 上已有的机遇读面（`M_POLICY_OPPORTUNITY_COUNT`）本分册不改。`jobs` 上既有的 `policy_focus` 仍走 harness。效能得分、趋势、分区、实施路径、方案和参数模拟不在这里展开。

## 2. 内部委托

浏览器经网关打 `gkxlumen-display`。网关只转 `/display/**`。浏览器只打 `/display/v1/policy/**`。

`gkxlumen-display` 不直连库，不直连 Python，不写算法，不写 nGQL。不打 `/v1/policy/**`，不嵌算法中台，不调用任何 `demo-*` 服务。Java 不拼指数、不拼短板数、不拼摘要、不打分。

| 公开资源 | 内部委托 |
|---|---|
| `evaluation/counts` | `gkxlumen-display` 不直连库。`gkxlumen-element` 只读 `ads.policy_effect`（`scope_type=region_gap` 的 `shortboard_cnt`）。不进专题政策门面。GET 不调用 `polan.eval.gap.run`，也不打 `GET /v1/policy/analysis/gap` |
| `evaluation/shells` | `gkxlumen-display` 不直连库。`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_eval_shell`。不进专题政策门面。不把查询转到 Python 现造一行 |
| `evaluation/jobs` | `gkxlumen-display` → `gkxlumen-topic-async-service` `POST /topic/v1/analysis/tasks` → 已有 `PolicyAnalysisAdapterImpl` → `POST /internal/policy/jobs/execute` |

223 的焦点和 226 的摘要不进专题政策查询门面。任务表、SSE、并发锁复用 `gkxlumen-topic-async-service`。`/internal/policy/jobs/execute` 的计算代码在 `lumen-algo-py/vendor/entan-py`。算法中台页面留在 `demo-ui-system-test` 与 `lumen-ui-algo-apiview` 的 `/policy/focus`、`/policy/gap`、`/policy/parse`。展示不嵌这些页。`/v1/policy/analysis/focus`、`/v1/policy/analysis/gap`、`/v1/policy/text/parse`、`POST /v1/policy/analysis/focus-one` 继续给算法中台自己用。

`policy_focus_ads` 与 `policy_text_parse` 是白名单上要增加的两个键。例外只加在这两条：它们不走产业链码与技术领域的二选一校验（产业 VID XOR），也不收 items。既有 `policy_focus` 仍要求 items、产业或正文，并走 `harness.dispatch`。本分册不改那条校验，不把 harness 的返回当成热点看板。其它 sub_type 仍按已有校验，不把这两个例外扩大过去。Java 仍不打分。

两个新键尚未放进白名单时，这次 Job 返回空结果，响应里不带写死的指数或摘要。放行之后，表里无行则结果仍空。

切条件不自动起任务。用户提交 `jobs` 之后才建任务。Job 失败不清空已经返回的 `counts` 和 `shells`。

trace 沿既有展示链。同步读在 display 往下带 traceId。Job 沿已有异步任务链。本分册不新设计观测点。

## 3. 223 短板条数 · counts

公开资源：`GET /display/v1/policy/evaluation/counts`。指标 `M_POLICY_SHORTBOARD_COUNT`，类型 STAT，D4=mock。

链路：前端 → 网关 → `gkxlumen-display` → `gkxlumen-element` → `ads.policy_effect`。

- 只读 `scope_type=region_gap` 的 `shortboard_cnt`。这与 `GET /v1/policy/analysis/gap` 读的是同一张表、同一个范围。展示不打那条中台 URL
- 源模型 `M_POLICY_DEEP_169_1` 仍是 MODEL，不在这条同步链上计算
- 已有 `polan.eval.gap.run` 按区域写入覆盖盲区、失效占比、平均力度不足。`ext` 里已有 `is_mock` 和 `QPOL-02`。本分册不改公式，不改权重。这次 GET 不调用 `gap.run`
- 查询不拼短板数。有 `region_gap` 行则返回该行上的 `shortboard_cnt`。没有行则该计数空，不造 0
- 不把 `GDF-POLICY-MDC-STAT-L01` 写成已覆盖本指标。数值在对齐前仍是 mock

`counts` 上的机遇条数 `M_POLICY_OPPORTUNITY_COUNT` 没有 223–226 的序号。留给页 KPI 的那块读面本分册不改，不在这条短板读里另造机遇数。

空态：无行则计数空。HTTP 成功。不造 0。不返回 501。不在接口函数里返回写死的条数。

D4 仍是 mock。`QPOL-02` 未闭合。`GDF-POLICY-MOCK-GATE-L01` 仍是 blocked。本分册不把 mock 写成已上线，不改 D4。

## 4. 223 焦点指数 · jobs · policy_focus_ads

公开资源：`POST /display/v1/policy/evaluation/jobs`。指标 `M_POLICY_FOCUS_INDEX`，类型 MODEL，D4=mock。浏览器提交这一条，`sub_type=policy_focus_ads`。字段名由契约单冻结。

链路：

1. 浏览器只打 `POST /display/v1/policy/evaluation/jobs`。不打开算法中台页，不打 `/v1/policy/analysis/focus`，不打 `focus-one`。
2. `gkxlumen-display` 不计算指数。它调用 `POST /topic/v1/analysis/tasks`。浏览器不打 `/topicAsync/**`，也不改打 `/topic/v1/policy`。
3. 已有 `PolicyAnalysisAdapterImpl` 调用 `POST /internal/policy/jobs/execute`。
4. Python 调用仓库里已有的 `polan.eval.focus.run`（`lumen-algo-py/vendor/entan-py` 已有这份实现）。`run()` 先写入表。不新写公式，不新表。`run()` 只删除 `policy_id` 非空的行再写入，不删除 `policy_id` 为空的机遇行。本分册不改这个删除范围。
5. Job 再读 `ads.policy_focus` 里 `policy_id` 非空的行：`focus_score`，以及 `ext` 里已有的 `title` 和 `explanation`。结果原样放进 Job 结果。查询不拼指数。这就是说明书第 11.2 节写的「焦点问题名称和一句说明」，落在已有表上。

`policy_focus_ads` 不走产业 VID XOR，不收 items。展示看板不提交政策条目。带 items 的既有 `policy_focus` 保持原样，仍走 `harness.dispatch`。本分册不把那条作业改成 `policy_focus_ads`，也不把 harness 返回当成热点看板。

白名单增加 `policy_focus_ads`。尚未放行时，这次 Job 返回空结果，不返回写死的指数。放行之后，表里无行则焦点块空。不返回 `focus-one` 的当场计算结果。

权重仍是 `QPOL-02` 待甲方确认的规则基线。本分册不改权重，不把 `is_mock` 改成已上线。不另建 `gapfill_policy_eval_focus`。

`M_POLICY_RELATION_DEGREE` 写在同一行的 `relation_degree` 上。本分册不把它改挂到 223，也不为此读图。Java 不写 nGQL。

不把算法中台的 Top15 图和区间图当成展示接口。不把演示页上的主题卡片写成新指标。不建 `ads.policy_gap`。

切条件不自动起任务。Job 失败时，已经返回的短板计数和 shells 保持原样。

D4 保持 mock。

## 5. 224、225 · shells

公开资源：`GET /display/v1/policy/evaluation/shells`。一次 GET 读同一张表里的两类行。点选专题或指标只在已经返回的行里筛选，不另起计算，不新开路径。种类如何分列由契约单冻结，本分册不写字段表。

没有专属解读模型，也没有多媒体通道。真实生成和真实嵌入做不到。浏览器仍打上面的展示路径。`gkxlumen-display` 不直连库。`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_eval_shell`。不把这两类放进专题政策门面，也不把查询转到 Python 现造一行。

224 只读解读条目：专题或指标名、一句结论、一句应用建议。条目可以指向已经存在的 `metric_id`，不新注册。不把 226 的摘要行复制成解读条目，不把 223 的焦点说明改挂到本序号。

225 只读多媒体条目：标题、一句说明。不返回视频、动画、PDF、模板字节。不灌图形文件，不写对象存储，前端不直连 RustFS。不把 219–221 的趋势图、分区图、结构关联收进本资源。不把前端占位动画写成多媒体服务。页上已有的短板计数和焦点结果留在 `counts` 和 `jobs` 上，本序号不新做一套图。

建表和灌数不在本分册。灌数是独立单 `POL-L2-DS11-READ-GAPFILL-L01`（`data-agent`，监管 `human:淮政玮`），不是请求处理。它只灌解读条目和多媒体条目。列的其余字段由 `POL-L2-DS11-READ-DATA` 定。本分册不写 DDL。表在 `gkxlumenx_gapfill`，不写入 ODS、DWD、ADS、供应方库。shell 行上要带的 `metric_id`、`gap_item`、`fill_method`、`gapfill_batch_id`、`generated_at` 以已签收架构第 8 节为准：没有已挂指标的，`metric_id` 留空；`fill_method` 用 `manual`；`gap_item` 写序号和叶子名。查询请求不灌数。

无行则解读块空，多媒体块空。HTTP 成功。不造一条结论，不造一条多媒体说明。不在接口函数里返回写死的句子。不返回 501。

D4 保持 mock。行是灌入的 mock，不是采集实数。不新造 `metric_id`。序号 222 的模板选用不写入本表，本分册不读模板字节。

## 6. 226 智能摘要 · jobs · policy_text_parse

公开资源与焦点相同：`POST /display/v1/policy/evaluation/jobs`。指标 `M_POLICY_DS_11_POLICY_EVAL_012`，类型 MODEL，D4=mock。需求来源即序号 226。浏览器提交这一条，`sub_type=policy_text_parse`。字段名由契约单冻结。

算法中台「文本解析 · 智能摘要」已经把这条展示身份定义成读 `ads.policy_text_parse.summary`，不另写模型。写入该列的 `polan.text.parse.run` 是规则截取，行上的 `metric_id` 仍是 `M_POLICY_TEXT_PARSE`。本分册不改这个 `metric_id`，也不把截取改成大模型。`M_POLICY_DS_11_POLICY_EVAL_012` 是读面身份，不是第二套摘要。

链路与第 4 节同一条管道，到 Python 之后改为只查询：

1. 浏览器只打 `POST /display/v1/policy/evaluation/jobs`。不打开算法中台页，不打 `/v1/policy/text/parse`。
2. `gkxlumen-display` 不调用大模型，不截取正文。它调用 `POST /topic/v1/analysis/tasks`。
3. 已有 `PolicyAnalysisAdapterImpl` 调用 `POST /internal/policy/jobs/execute`。
4. Python 只查询 `ads.policy_text_parse.summary`，原样放进 Job 结果。不在这次请求里调用 `polan.text.parse.run`。该 `run()` 会清空整张 `ads.policy_text_parse`，条款结构化写在同一张表上。展示请求只查询，避免一次请求把条款行清掉。摘要行仍由已有解析批次写入。
5. 查询不拼摘要，不调用大模型。

`policy_text_parse` 不走产业 VID XOR，不收 items。白名单增加这个键，并且与已签收的 `policy_effect` 一样不走产业 VID 校验。尚未放行时，这次 Job 返回空结果，不返回写死的段落。放行之后，无行则摘要空。

可编辑和推送没有登记的用户表，也没有发信通道。本分册不建编辑表，不把改过的句子写回 ADS，不灌假通知。用户当时在页面上改字，不构成本条资源。没有推送通道时不另造通知。

不建 `gapfill_policy_eval_summary`。不把序号 242 的推演解读报告、核增研报 `report/jobs` 当成这条摘要。不把 `focus-one` 当成摘要。

切条件不自动起任务。Job 失败不清空已经返回的 `counts` 和 `shells`。

D4 保持 mock。

## 7. 空态对照

四叶的签收读法都是查已有表或查缺项表。无行则空。不用 501 充当功能。接口不直接返回写死的 mock。mock 若存在，只能先落进表，再被查询读出来。

| 序号 | 资源 | 无数据 |
|---|---|---|
| 223 短板 | counts | `ads.policy_effect` 无 `region_gap` 行则计数空。不造 0。不返回 501。这次 GET 不调用 `gap.run` |
| 223 焦点 | jobs · `policy_focus_ads` | `ads.policy_focus` 无 `policy_id` 非空行则焦点块空。不返回写死指数，不返回 `focus-one`。不返回 501。失败不清空 counts 和 shells |
| 224 | shells · 解读条目 | 缺项表无解读行则解读块空。不造结论。不返回 501 |
| 225 | shells · 多媒体条目 | 缺项表无多媒体行则该块空。不返回视频、动画、PDF、模板字节。不返回 501 |
| 226 | jobs · `policy_text_parse` | `ads.policy_text_parse` 无摘要行则摘要空。不返回写死段落。不调用 `parse.run`。不返回 501。失败不清空 counts 和 shells |

两个新键尚未放行时，同样返回空结果，不改用写死的指数或摘要。

## 8. 明确不做

- 不另建 API-POL。不冻结枚举、响应字段名和 DTO。交给 `BE-POL-CONTRACT-01`。
- 不写 OpenAPI 字段表。不写实现代码。不改 Python，不改 Java。
- 不改 `POL-L2-DS11-READ-ARCH`，以及说明书、WBS、契约输入清单、调用链与边界、`指标与501.md`、调研分册、VIZ、PLAN 和任何兄弟分册。
- 不改 `ARCH-DISPLAY-01`。不把 `E-E7-POLICY-M1-L06` 写成展示联调单。`E-E7-POLICY-M1-L03` 只索引专题侧的焦点、力度、效果。展示不改打专题政策 URL，也不等它来实现本四叶。
- 浏览器不改打 `/topic/v1/policy`、`/policy/topic/v1/policy`、`/topicAsync/**`、`/v1/policy/**`。
- 展示不直连 Python，不直连库，不打算法中台。不调用 `demo-*`。不把 `polan.eval.focus`、`polan.eval.gap`、`polan.text.parse` 抄进 Java，不抄进 `gkxlumen-display`，不送进专题政策查询门面。
- 不用 501 充当 223–226 的功能。无行则空。短板不造 0。
- 不新造 `metric_id`。不改 D4。不把 mock 写成已上线。不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开。不改 `QPOL-02` 的权重和阈值。
- 不改 `counts` 上已有的机遇读面。不把 `M_POLICY_OPPORTUNITY_COUNT` 挂进本二级。
- 不把 `policy_focus_ads`、`policy_text_parse` 的产业 VID XOR 例外扩大到其它 sub_type。既有 `policy_focus` 仍走 harness，不收进这两个新键，本分册不改它。
- 两个新键都不收 items。焦点 Job 不改 `run()` 的删除范围。摘要请求不调用 `parse.run`，避免 TRUNCATE 整张 `ads.policy_text_parse`。
- 不建 `gapfill_policy_eval_focus`、`gapfill_policy_eval_summary`、`ads.policy_gap`。224、225 的建表与灌数不在本分册执行。查询不灌数。
- 不返回视频、动画、PDF、模板字节。不新建桶，不写对象存储，前端不直连 RustFS。
- 不纳入本分册：222 模板、227–231 方案、效能得分、趋势、分区、实施路径、`M_POLICY_DS_11_POLICY_EVAL_015`、`focus-one`、`report/jobs`、`compare/jobs`、`simulation/jobs`。
- 不把 `M_POLICY_EFFECT_SCORE`、`M_POLICY_RELATION_DEGREE` 改挂到本二级。
- 不改 `FE-POL-02A`，不新建前端单。契约冻结前前端继续 mock。
- 不会签。不把本单标 done，不标 ready_to_sign。

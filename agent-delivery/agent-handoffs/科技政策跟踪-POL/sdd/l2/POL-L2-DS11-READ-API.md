# POL-L2-DS11-READ-API · 政策分析评价 · 结果解读报告多维展示 · 后台接口设计

- 任务：`POL-L2-DS11-READ-API`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:api-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-05`
- 上游：`sdd/l2/POL-L2-DS11-READ-ARCH.md`（本单派令：已签收）。会签对照 `sdd/l2/会签/POL-L2-DS11-READ-SIGNOFF-ARCH.md`。本分册以这两份为准，不改它们

本分册只定政策分析评价二级「结果解读报告多维展示」的后台接口。SRS 序号 **223–226**。它是 `BE-POL-CONTRACT-01` 的输入，不是第二份 API-POL。不另建契约文件。枚举闭包、响应字段名和 DTO 仍由那一张契约冻结。这里只写路径、方法、内部委托、同步或 Job、空态。不写 OpenAPI 字段表，不写实现代码。

流程以 `POL-L2-DS11-READ-ARCH` 为准。契约输入清单里评价页的 `evaluation/counts`、`evaluation/jobs`、`evaluation/shells` 只作资源名对照。清单把这三条的空态写在「501 时页面空态」列，并把分主题解读标成未见。清单里的「未见」和旧空态不覆盖本分册。本分册不改那份清单。

签收口径：做不到的只允许缺项表灌 mock 后由接口读表。223 短板读已有 `ads.policy_effect`，223 焦点读已有 `ads.policy_focus`，226 读已有 `ads.policy_text_parse.summary`，都不另建表。224、225 只读 `gkxlumenx_gapfill.gapfill_policy_eval_shell`。不允许接口直接返回写死的计数、指数、结论、摘要或视频，也不用 501 充当这四叶的画面。

## 偏离

本二级 DoD 里「不复用 `/topic/v1/policy`」指浏览器不改打专题政策 URL。`gkxlumen-display` 内部提交 `gkxlumen-topic-async-service` 的 `POST /topic/v1/analysis/tasks`，算内部委托，不是专题政策查询门面。浏览器仍只打 `/display/v1/policy/**`。对外不把 `/topic/v1/policy`、`/v1/policy/**` 或 `/topicAsync/**` 写成入口。不改 `ARCH-DISPLAY-01`。`E-E7-POLICY-M1-L06` 不是展示联调单，也不是本二级的实现路径。`E-E7-POLICY-M1-L03` 只索引专题侧的焦点、力度、效果，不实现这四叶。展示不改打专题政策 URL，也不等它来实现本四叶。

## 1. 公开资源

前缀 `/display/v1/policy/`。四叶都在政策分析评价里完成，不另开页，不另开路径。本分册不新开资源。

| 序号 | 公开资源 | 读法 |
|---|---|---|
| 223 短板 | `GET /display/v1/policy/evaluation/counts` | 同步。element 只读 `ads.policy_effect` 里 `scope_type=region_gap` 的 `shortboard_cnt`。这次 GET 不调用 `gap.run`。无行则计数空，不造 0 |
| 223 焦点 | `POST /display/v1/policy/evaluation/jobs` | Job。`sub_type=policy_focus_ads`。display 只提交 `analysis/tasks`。调用已有 `focus.run` 后读 `ads.policy_focus`。无行则焦点块空 |
| 224 | `GET /display/v1/policy/evaluation/shells` | 同步。element 只读 `gapfill_policy_eval_shell` 的解读条目。点选只筛选已返回的行。无行则解读块空 |
| 225 | 同一条 `GET /display/v1/policy/evaluation/shells` | 同步。element 只读同一张表的多媒体条目：标题和一句说明。不灌视频，不灌模板选用。无行则该块空 |
| 226 | 同一条 `POST /display/v1/policy/evaluation/jobs` | Job。`sub_type=policy_text_parse`。display 只提交 `analysis/tasks`。只查 `ads.policy_text_parse.summary`。请求里不调用 `parse.run`。无行则摘要空 |

`evaluation/counts`、`evaluation/jobs`、`evaluation/shells` 在契约输入清单里还挂着其它叶子。本分册只定上表这些读法。

机遇条数 `M_POLICY_OPPORTUNITY_COUNT` 留在 `counts` 已有读面。本分册不改那一读，也不把它挂进 223–226。

序号 222、227–231 不进本分册。219–221 的趋势、分区、结构关联也不在这里重写。`jobs` 上的效能得分、实施路径、方案和参数模拟，`shells` 上的模板选用、互动意见和方案归档，都不是这四叶。同一条路径上其它叶子的读法由它们自己的分册定。

用户提交 `jobs` 时要带的 `sub_type` 只有本分册这两枚：`policy_focus_ads`、`policy_text_parse`。参数名留给 `BE-POL-CONTRACT-01`。

## 2. 内部委托

浏览器经网关打 `gkxlumen-display`。网关只转 `/display/**`。浏览器只打 `/display/v1/policy/**`。

`gkxlumen-display` 不直连 Python，不直连库，不写算法，不算指数，不写 nGQL。不打算法中台 `/v1/policy/**`。不调用任何 `demo-*` 服务。不嵌中台页。

| 公开资源 | 内部委托 |
|---|---|
| `evaluation/counts` | `gkxlumen-display` 不直连库。`gkxlumen-element` 只读 `ads.policy_effect` 里 `scope_type=region_gap` 的 `shortboard_cnt`。这次 GET 不调用 `polan.eval.gap.run`。机遇条数仍走这条资源上已有的读面，本分册不改 |
| `evaluation/shells` | `gkxlumen-display` 不直连库。`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_eval_shell`。224 取解读条目，225 取多媒体条目。不灌视频，不灌模板选用 |
| `evaluation/jobs` | `gkxlumen-display` 只提交 `gkxlumen-topic-async-service` 的 `POST /topic/v1/analysis/tasks`。已有 `PolicyAnalysisAdapterImpl` 再调 `POST /internal/policy/jobs/execute`。display 不直接打 `jobs/execute`。浏览器看不见这条内部地址 |

223 的短板、224、225 不进专题政策查询门面，也不进异步任务管道。223 的焦点和 226 的摘要不进专题政策查询门面。这两叶的任务表、SSE、并发锁复用 `gkxlumen-topic-async-service`。`/internal/policy/jobs/execute` 的下游是已有 Python `/internal/policy`。

焦点链路：

1. 浏览器只打 `POST /display/v1/policy/evaluation/jobs`，`sub_type=policy_focus_ads`。
2. `gkxlumen-display` 不算指数，也不直接调 `jobs/execute`。它只调用 `POST /topic/v1/analysis/tasks`。
3. `PolicyAnalysisAdapterImpl` 再调 `POST /internal/policy/jobs/execute`。
4. Python 调用仓库里已有的 `polan.eval.focus.run`（`lumen-algo-py/vendor/entan-py`），再读 `ads.policy_focus` 里 `policy_id` 非空的行。Java 不算指数，不抄公式。

摘要链路与焦点共用同一条管道，`sub_type=policy_text_parse`。Python 只查询 `ads.policy_text_parse.summary`。这次请求不调用 `polan.text.parse.run`，不调用大模型。

旧键 `policy_focus` 仍走 `harness.dispatch`。它仍要求 items、产业或正文。`PolicyAnalysisTypes` 上这条既有校验保持原样。展示看板不提交政策条目，也不把 harness 的返回当成热点看板。带 items 的既有焦点作业保持原样。本分册不改旧键。

`policy_focus_ads` 与已签收的 `policy_effect` 相同：不走产业 VID 校验，不收 items。`policy_text_parse` 同样不走产业 VID 校验。这两个键尚未进入 `JOB_SUB_TYPES`。本分册不改白名单代码。未挂上时，这次 Job 的焦点或摘要结果为空，不返回写死指数或段落。挂上之后，表里无行仍空。

切条件不自动起任务。用户提交 `jobs` 之后才建 223 焦点和 226 的任务。223 短板、224、225 不建任务。某一块读失败，不清空已经返回的其它块。Job 失败不清空已经返回的短板计数和解读条目。

trace 沿既有展示链。同步读在 display 往下带 traceId。Job 沿已有异步任务链。本分册不新设计观测点。

## 3. 223 热点问题分析看板

两条挂接，两条链路。短板走同步 `counts`。焦点走 Job `jobs`。

### 3.1 短板条数 · counts

公开资源：`GET /display/v1/policy/evaluation/counts`。同步。

指标 `M_POLICY_SHORTBOARD_COUNT`，类型 STAT，D4=mock。

`gkxlumen-display` 不直连库。`gkxlumen-element` 只读 `ads.policy_effect` 里 `scope_type=region_gap` 的 `shortboard_cnt`。这与 `GET /v1/policy/analysis/gap` 读的是同一张表、同一个范围。展示不打那条中台 URL，也不打开 `/policy/gap`。

这次 GET 不调用 `polan.eval.gap.run`。源模型 `M_POLICY_DEEP_169_1` 仍是 MODEL，不在这条同步链上计算。已有 `gap.run` 按区域写入覆盖盲区、失效占比、平均力度不足。`ext` 里已有 `is_mock` 和 `QPOL-02`。本分册不改公式，不改权重，不把 `is_mock` 改成已上线。不把 `GDF-POLICY-MDC-STAT-L01` 写成已覆盖本指标。不另建 `ads.policy_gap`。

有 `region_gap` 行则返回已写下的 `shortboard_cnt`。没有行则该计数空，不造 0。数值在对齐前仍是 mock。HTTP 成功。不返回 501。查询函数自己不拼短板数。

机遇条数留在 `counts` 已有读面。本分册不改那一读，也不把机遇条数挂进 223。

`QPOL-02` 未闭合。`GDF-POLICY-MOCK-GATE-L01` 仍是 blocked。本分册不把 mock 写成已上线，不改 D4。

### 3.2 焦点指数 · jobs

公开资源：`POST /display/v1/policy/evaluation/jobs`。Job。指标 `M_POLICY_FOCUS_INDEX`，类型 MODEL，D4=mock。`sub_type=policy_focus_ads`。

链路见第 2 节。Python 调用已有 `polan.eval.focus.run`，再读 `ads.policy_focus` 里 `policy_id` 非空的行。看板上要的是 `focus_score`，以及 `ext` 里已有的标题和一句说明。这就是说明书第 11.2 节写的「焦点问题名称和一句说明」，落在已有表上。不另建 `gapfill_policy_eval_focus`。不返回 `focus-one` 的当场计算结果。`POST /v1/policy/analysis/focus-one` 留给算法中台，展示不打它。`focus-one` 不写 ADS。

`run()` 只删除 `policy_id` 非空的行再写入，不删除 `policy_id` 为空的机遇行。本分册不改这个删除范围。

权重仍是 `QPOL-02` 待甲方确认的规则基线。本分册不改权重，不把 `is_mock` 改成已上线。D4 保持 mock。

`policy_focus_ads` 未挂上白名单时，这次 Job 的焦点结果为空，不返回写死的指数。挂上之后，表里没有 `policy_id` 非空的行则焦点块空，也不造 0。HTTP 成功意义上的空结果，不返回 501。查询函数自己不拼指数。

旧键 `policy_focus` 仍走 harness，本分册不改。看板不把 harness 的返回当成热点结果。

`M_POLICY_RELATION_DEGREE` 写在同一行的 `relation_degree` 上。本分册不把它改挂到 223，也不为此读图。Java 不写 nGQL。

切条件不自动起任务。Job 失败时，已经返回的短板计数和解读条目保持原样。

不把算法中台的 Top15 图和区间图当成展示接口。不把演示页上的主题卡片写成新指标。

## 4. 224 分主题分指标互动解读 · shells

公开资源：`GET /display/v1/policy/evaluation/shells`。同步。与 225 同一条。

没有专属 `metric_id`，也没有已注册的解读模型。真实生成做不到。

`gkxlumen-display` 不直连库，不直连 Python。`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_eval_shell` 里的解读条目：专题或指标名、一句结论、一句应用建议。条目可以指向已经存在的 `metric_id`，不新注册。表不写入 ODS、DWD、ADS。

点选是对已返回条目的筛选，不另起计算，不新开路径，不新开模型。筛选参数名留给 `BE-POL-CONTRACT-01`。

表里没有解读行则解读块空。HTTP 成功。不在接口里写死结论。不返回 501。

不把 226 的摘要行复制成解读条目。不把 223 的焦点说明改挂到本序号。不灌模板选用。序号 222 的模板不进本分册。

灌数是独立脚本（`POL-L2-DS11-READ-GAPFILL-L01`），不是请求处理。本分册不写 DDL，不执行灌数。列由 `POL-L2-DS11-READ-DATA` 定。

## 5. 225 多媒体辅助解读 · shells

公开资源仍是 `GET /display/v1/policy/evaluation/shells`。同步。与 224 同一条。

调研记交互壳，无指标，无视频通道。真实嵌入做不到。

同一张 `gkxlumenx_gapfill.gapfill_policy_eval_shell`。`gkxlumen-element` 只读多媒体条目：标题、一句说明。不返回视频、动画或图形文件。不灌视频。不写对象存储。前端不直连 RustFS。不新建桶。不灌模板选用，不灌 PDF。

页上已有的短板计数和焦点结果留在 `counts` 和 `jobs` 上。本序号不新做一套图，不另开路径。

表里没有多媒体行则该块空。HTTP 成功。不返回 501。不把前端占位动画写成多媒体服务。

不把序号 219–221 的趋势图、分区图、结构关联收进本叶。

灌数与 224 同一张表、同一个 `POL-L2-DS11-READ-GAPFILL-L01`。该单只灌解读条目和多媒体条目。查询不灌数。本分册不写 DDL。

## 6. 226 智能摘要与结论推送 · jobs

公开资源与 223 焦点相同：`POST /display/v1/policy/evaluation/jobs`。Job。`sub_type=policy_text_parse`。

指标 `M_POLICY_DS_11_POLICY_EVAL_012`，类型 MODEL，D4=mock。需求来源即序号 226。这是读面身份，不是第二套摘要。

算法中台「文本解析 · 智能摘要」已经把这条展示身份定义成读 `ads.policy_text_parse.summary`。写入该列的 `polan.text.parse.run` 是规则截取，行上的 `metric_id` 仍是 `M_POLICY_TEXT_PARSE`。本分册不改这个 `metric_id`，也不把截取改成大模型。不另建 `gapfill_policy_eval_summary`。

链路与第 2 节同一条管道。display 只提交 `POST /topic/v1/analysis/tasks`。适配器再调 `POST /internal/policy/jobs/execute`。Python 只查询 `ads.policy_text_parse.summary`。

`polan.text.parse.run` 会清空整张 `ads.policy_text_parse`。条款结构化写在同一张表上。226 的请求路径只查询，避免一次展示请求把条款行清掉。摘要行仍由已有解析批次写入。这次请求不调用 `parse.run`，不调用大模型。

`policy_text_parse` 未挂上白名单时，这次 Job 的摘要结果为空，不返回写死的段落。挂上之后，没有行则摘要空。HTTP 成功意义上的空结果，不返回 501。查询函数自己不拼摘要。

可编辑和推送没有登记的用户表，也没有发信通道。本分册不建编辑表，不把改过的句子写回 ADS，不灌假通知。用户当时在页面上改字，不构成本条资源。没有推送通道时不另造通知。

切条件不自动起任务。Job 失败时，已经返回的短板计数和解读条目保持原样。

不把序号 242 的推演解读报告、核增研报 `report/jobs` 当成这条摘要。不把 `focus-one` 当成摘要。D4 保持 mock。不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开。

## 7. 空态对照

四叶的签收读法都是查已有读面或查表。无行则空。不用 501 充当这四叶的画面。不返回写死的计数、指数、结论、摘要或视频。

| 序号 | 资源 | 无数据 |
|---|---|---|
| 223 短板 | `GET evaluation/counts` | `ads.policy_effect` 没有 `scope_type=region_gap` 的行则计数空，不造 0。这次 GET 不调用 `gap.run`。不返回 501 |
| 223 焦点 | `POST evaluation/jobs` · `policy_focus_ads` | 未挂上白名单则结果空，不返回写死指数。挂上后没有 `policy_id` 非空的行则焦点块空，不造 0。不返回 `focus-one` 的当场结果。失败不清空已经返回的短板计数和解读条目 |
| 224 | `GET evaluation/shells` | 缺项表没有解读行则解读块空。不返回写死结论。不返回 501 |
| 225 | `GET evaluation/shells` | 缺项表没有多媒体行则该块空。不返回视频或动画文件。不返回 501 |
| 226 | `POST evaluation/jobs` · `policy_text_parse` | 未挂上白名单则结果空，不返回写死段落。挂上后没有 `summary` 行则摘要空。请求不调用 `parse.run`。失败不清空已经返回的短板计数和解读条目 |

机遇条数不在上表。它留在 `counts` 已有读面，不挂进 223–226。序号 222、227–231 不在上表。

## 8. 明确不做

- 不另建 API-POL。不冻结枚举、响应字段名和 DTO。交给 `BE-POL-CONTRACT-01`。
- 不写 OpenAPI 字段表。不写实现代码。不改 Python，不改 Java。不改 `JOB_SUB_TYPES` 白名单代码。
- 不新开资源。浏览器只打 `/display/v1/policy/**`。不把 `/topic/v1/policy`、`/v1/policy/**`、`/topicAsync/**` 写成浏览器入口。
- 不改 `POL-L2-DS11-READ-ARCH`、会签页，以及说明书、WBS、契约输入清单、调用链与边界、指标与 501、调研分册。
- 不改 `ARCH-DISPLAY-01`。不把 `E-E7-POLICY-M1-L06` 写成展示联调单。不把 `E-E7-POLICY-M1-L03` 写成这四叶的实现。
- `gkxlumen-display` 不直连 Python，不直连库。223 焦点和 226 的 display 不直接打 `jobs/execute`，只提交 `POST /topic/v1/analysis/tasks`。
- 223 短板这次 GET 不调用 `gap.run`。226 的请求不调用 `parse.run`。旧键 `policy_focus` 仍走 harness，不改旧键。
- 不用 501 充当 223–226 的画面。无行则空，不造 0。接口不直接返回写死的 mock。
- 不新造 `metric_id`。不改 D4。不把 mock 写成已上线。不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开。`QPOL-02` 仍未闭合。
- 机遇条数留在 `counts` 已有读面，不挂进 223–226。
- 序号 222、227–231 不进本分册。不灌模板选用。不把 `M_POLICY_DS_11_POLICY_EVAL_015` 挂到本四叶。
- 不把 `M_POLICY_EFFECT_SCORE`、趋势、分区、方案、参数模拟写进这四叶。不把 `M_POLICY_RELATION_DEGREE` 改挂到 223。
- 不建 `ads.policy_gap`、`gapfill_policy_eval_focus`、`gapfill_policy_eval_summary`。224、225 只读 `gapfill_policy_eval_shell`。
- 不灌视频，不写对象存储，前端不直连 RustFS。
- 不把 `compare/jobs`、`report/jobs`、`simulation/jobs` 写成这四叶。
- 查询不灌数。缺项表的建表与灌数不在本分册执行。
- 不改 `FE-POL-02A`，不新建前端单。契约冻结前前端继续 mock。
- 不会签。不把本单标 done。

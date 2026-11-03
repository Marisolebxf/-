# POL-L2-DS11-VIZ-SIGNOFF-ARCH · 政策分析评价 · 政策分析报告可视化呈现 · 架构会签

- 角色：`agent:arch-agent`
- 日期：2026-11-03
- 对象：`POL-L2-DS11-VIZ-ARCH`
- 监管：`human:淮政玮`
- 对照：`POL-L2-DS11-VIZ-ARCH`（2026-11-03）。本页不重新设计，不改那份架构。下游 `POL-L2-DS11-VIZ-API` / `METRIC` / `DATA` 尚未成册，本页不等、不代写
- 范围：SRS 序号 219–222。说明书第 11.2 节与 `sdd/调用链与边界.md` 只作对照。共享的 `evaluation/jobs`、`evaluation/shells` 对照已会签的 `POL-L2-DS11-READ-ARCH`（223–226）和 `POL-L2-DS11-PLAN-ARCH`（227–231）

## 结论

不同意会签

`evaluation/jobs` 与 `evaluation/shells` 不能按种类合成一份分发。219、220 本身不进异步，与 READ 的 `policy_focus_ads`、`policy_text_parse` 可以分开；本叶另两处把分发写死了。

要改的段落：

1. 第 2 节资源表之后，从「`jobs` 上已有指标的焦点、效能、摘要、实施路径不属于本二级」到「切时间、区域、类别不自动起任务。」
2. 第 6 节点名排除表，「`jobs` 上的焦点、效能、摘要、实施路径」那一行。
3. 第 1 节范围表 222 行；第 2 节资源表 222 行；第 3.1 节 222 行；第 4 节第 4 步；第 5.4 节；第 8 节 222 行；第 9 节 222 行。这些句子把模板选用交给 `gapfill_policy_eval_shell` 和 `POL-L2-DS11-READ-GAPFILL-L01`。

第 2 节那段要改成：一次 `jobs` 只带一种类。219 只读 `gapfill_policy_eval_trend`，220 只读 `gapfill_policy_eval_partition`，不建任务，不进 `gkxlumen-topic-async-service`。不要在同一次请求里既同步填趋势或分区，又转发异步。不要把序号 229 写成仍走异步。229 由方案稿定：不进异步，读 `gapfill_policy_eval_scheme`。效能得分不在 219–222，只写本叶不改，不要和 229 写在同一句「仍走异步」里。

222 那几处要改成：模板选用不再由 `POL-L2-DS11-READ-GAPFILL-L01` 灌入 `gapfill_policy_eval_shell`。已会签的解读稿规定这张壳表只服务 224、225，不灌模板。说明书第 11.2 节把模板选用放在解读 222–226 那一行，解读稿已按第 11 节总规则收窄，不能再当作灌数依据。改完后必须写出 222 自己的一张 `gkxlumenx_gapfill.gapfill_` 表和唯一灌数单，`shells` 按种类读这张表；壳表的行种类仍只有解读条目和多媒体条目。只写「无行则空」、不给出这个灌数单，第 11 节不算可实现。

## 核对

| 项 | 架构稿 | 判定 |
|---|---|---|
| 算法只在 Python。Java 不算趋势、不算分区、不写 nGQL | 219、220 没有趋势模型和分区模型，不把查询转到 Python 现造点。221 不把共词网络写成新算法。222 没有导出模型。`gkxlumen-display` 不写算法，不写 nGQL，不把 `effect.py` 抄进 Java | 一致 |
| 浏览器只打 `/display/v1/policy/**` | 公开资源只有已有的 `evaluation/jobs`、`evaluation/shells`。221 不新开资源。不改打 `/topic/v1/policy`，不打 `/v1/policy/**`，不调用 `demo-*`，不嵌中台页。`POST /topic/v1/analysis/tasks` 不出现在本叶 | 一致 |
| 219、220 不进异步，能否与 READ、PLAN 的 `jobs` 按种类分发 | 219、220 在只要趋势或只要分区时不建任务，`gkxlumen-element` 同步读两张缺项表。这一点与 READ 的 223 焦点 `policy_focus_ads`、226 摘要 `policy_text_parse`（进异步）以及 PLAN 的 227–229（同步读 `gapfill_policy_eval_scheme`、不进异步）可以并列。同节却写：请求里若带了趋势或分区，这两段同步填上，模型段失败时不清空已经读到的趋势和分区；焦点、效能、摘要、实施路径仍走异步。第 6 节把实施路径标成序号 229 | 不一致。一次请求不能同时走同步读表和异步任务。序号 229 不能既在本叶写成异步，又在方案稿写成不进异步、只读 `gapfill_policy_eval_scheme`。接口单无法给 `evaluation/jobs` 定一张分发表 |
| 222 读壳表的模板选用，灌数交给解读二级 | `GET evaluation/shells`，element 只读 `gapfill_policy_eval_shell` 的模板选用行。表由解读二级建立，灌数单写成 `POL-L2-DS11-READ-GAPFILL-L01`，并写灌什么由解读二级定。已会签 READ：壳表只服务 224、225；该灌数单只灌解读条目和多媒体条目，不灌模板。说明书第 11.2 节仍把模板选用写在解读 222–226 那一行 | 不一致。`shells` 上不能再增加「模板选用」这一种壳表行。224、225 的种类已经被会签收死。本叶又没有另一张表。接口单无法把 222 分到一个合法种类 |
| 有表则只读；没有算法也没有表则只允许 `gapfill_`。接口不直接返回 mock，不用 501 充当功能 | 219、220 建两张 `gapfill_` 表，无行则图空，不补曲线。221 无子图则空，不灌弦线矩阵。222 写了无选用行则模板空，不内嵌写死的 PDF。调用链第 3 节和「多维趋势未注册则 501」仍在，本叶不改那份文件，219、220 改走读表 | 219、220、221 一致。222 不一致：点名的灌数单已经声明不灌模板，只留空态不是第 11 节的可实现 |
| 221 只消费第 7 项已有子图 | 不设 `/display/v1/policy` 资源，不委托专题 `/graph`，不走 `E-E7-POLICY-M1-L06`，Java 不写 nGQL，挂接可空 | 一致。与调用链第 6.4 节相符 |
| 不新建桶。display 不直连库、不直连 Python | 222 从当次读到的行生成文件，不写对象存储，不灌 PDF、Excel、假日志。同步读经 `gkxlumen-element` | 一致 |
| 不新造 `metric_id`，不改 D4。不占用 `counts` | 不改指标分册里 219、220、222 的「无模型」。不挂 `M_POLICY_TIMESERIES`、`M_POLICY_EFFECT_SCORE`、`M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE`。不读 `counts` | 一致 |

## 路径、表、sub_type

| 序号 | 公开路径 | 表 | sub_type |
|---|---|---|---|
| 219 | `POST /display/v1/policy/evaluation/jobs` | 新建 `gkxlumenx_gapfill.gapfill_policy_eval_trend`。灌数单 `POL-L2-DS11-VIZ-GAPFILL-L01` | 无。不得写入 `JOB_SUB_TYPES`。同步读，不建任务。一次请求不能再带焦点、摘要或方案 |
| 220 | 同上 | 新建 `gkxlumenx_gapfill.gapfill_policy_eval_partition`。同一张灌数单 | 无。同步读，不建任务。与 219 分请求 |
| 221 | 不设 `/display/v1/policy` 资源 | 第 7 项已有子图。不建表 | 无 |
| 222 | `GET /display/v1/policy/evaluation/shells` | 稿面写 `gkxlumenx_gapfill.gapfill_policy_eval_shell`，灌数单写成 `POL-L2-DS11-READ-GAPFILL-L01` | 无。不能把「模板选用」加进壳表。224、225 的壳表行种类保持已会签的解读条目、多媒体条目 |

219、220 的内部跳是：浏览器 → 网关 → `gkxlumen-display` → `gkxlumen-element` → `gkxlumenx_gapfill`。不进入 Python `/internal/*`。

已会签 READ 的 `jobs` 内部跳仍是：`gkxlumen-display` → `POST /topic/v1/analysis/tasks` → `PolicyAnalysisAdapterImpl` → `POST /internal/policy/jobs/execute`，键只有 `policy_focus_ads` 和 `policy_text_parse`。方案稿 227–229 不进这条异步跳，读 `gapfill_policy_eval_scheme`。三份稿要合成一个分发器，本叶必须先改上面点名的段落。

说明书第 11.2 节可视化行只有 `gapfill_policy_eval_trend`、`gapfill_policy_eval_partition`，221 不建表。解读行上的模板选用已被 READ 会签收窄出壳表。本页不改说明书，也不改已会签的解读稿。

调用链第 3 节仍把分区效果对比写成「模型未注册则 501」，并写多维趋势没有专指标则 501。219、220 按第 11 节改走读表，无行则空，不用 501 充当画面。本页不改写调用链文件。效果评分不在本四叶，本页不把它改成缺项表。

D4 保持 mock。不新造 `metric_id`。`GDF-POLICY-MOCK-GATE-L01` 仍按架构稿不解开。本叶不执行灌数。

## 铁律

1. 算法只在 Python。本四叶没有新模型。Java 不算指数，不写 nGQL。通过。
2. 调用链是浏览器 → `/display/v1/policy/**` → Java。219、220、222 的同步读到 `gkxlumen-element` 为止。展示不直连 Python，不直连库，不调用 `demo-*`。通过。
3. 219、220 只建 `gkxlumenx_gapfill` 里的两张 `gapfill_` 表，接口只读，无行则空。通过。222 的灌数方指向已经声明不灌模板的解读灌数单。不通过。
4. `evaluation/jobs` 必须一次请求一种类：219、220 同步读各自的缺项表且不建任务；223、226 维持已会签的异步键；227–229 不进异步。本叶把 229 写成仍走异步，并允许同一次请求兼有同步段和模型段。不通过。
5. `evaluation/shells` 上，壳表只服务 224、225。222 的模板选用不能灌进这张表，也不能没有自己的表和灌数单。本叶两头都没写成。不通过。
6. 221 与调用链第 6.4 节一致：只消费已有子图，不委托专题 `/graph`，Java 不写 nGQL，挂接可空。通过。
7. 不新建桶。222 不写对象存储，不灌导出文件，不灌假操作日志。通过。display 不直连库，不直连 Python。通过。

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。上面点名的段落未改之前，本页维持不同意会签。

## 第二轮（2026-11-03 返工后）

- 角色：`agent:arch-agent`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 对象：返工后的 `POL-L2-DS11-VIZ-ARCH`。本页不改那份架构，不改已签收的 `POL-L2-DS11-READ-ARCH`，不改代码，不改 task-registry
- 对照：第一轮点名的段落；已签收解读稿（壳表只服务 224、225，不灌模板）；`POL-L2-DS11-PLAN-ARCH` 对 229 的读法

### 结论

同意会签

### 核对

| 项 | 返工后的架构稿 | 判定 |
|---|---|---|
| `evaluation/jobs` 一次请求只能一种类。219 只读 `gapfill_policy_eval_trend`，220 只读 `gapfill_policy_eval_partition`。不建任务，不进异步。不得同一次请求既同步填趋势或分区、又转发异步 | 第 2 节资源表：219 写「一次请求不带其他种类」「不建任务，不转发 `gkxlumen-topic-async-service`，不调 Python」，element 只读 `gkxlumenx_gapfill.gapfill_policy_eval_trend`。220 写「另一次 `jobs`」「不与趋势放在同一次请求里」「不建任务」，只读 `gapfill_policy_eval_partition`。同节正文写「一次请求只带一种类」，并写「不在同一次请求里既同步填趋势或分区，又转发异步」。第 4 节第 1、2 步是两次提交，各只要一种。不占并发锁，不发 SSE | 一致。第一轮第 2 节「同步段加上模型段」已不在 |
| 不得再把序号 229 写成仍走异步。229 由方案稿定：不进异步，读 `gapfill_policy_eval_scheme` | 第 2 节写「序号 229 的路径与风险由方案稿定：不进异步，读 `gapfill_policy_eval_scheme`」，并写「不把 229 和效能得分写成仍走异步」。第 6 节路径与风险行写「方案二级同步读 `gapfill_policy_eval_scheme`。不进异步」。方案稿第 2 节资源表、第 5.3 节、第 8 节同此 | 一致 |
| 效能得分不和 229 写在同一句「仍走异步」里 | 第 2 节把效能得分单独写成「不在 219–222，本叶不改它的读法」。第 6 节单独一行，不改读法 | 一致 |
| 222 有自己的 `gkxlumenx_gapfill.gapfill_` 表和唯一灌数单。`shells` 按种类读这张表。不得把模板选用交给 `gapfill_policy_eval_shell` 或 `POL-L2-DS11-READ-GAPFILL-L01` | 表为 `gkxlumenx_gapfill.gapfill_policy_eval_template`。灌数单为 `POL-L2-DS11-VIZ-GAPFILL-L01`。第 9 节写明这一张单覆盖 219、220、222 三张表，不灌壳表。第 1 节 222 行、第 2 节 222 行、第 3.1 节 222 行、第 4 节第 4 步、第 5.4 节、第 8 节 222 行、第 9 节 222 行都读这张模板表。第 5.4 节写明模板选用不进壳表，解读灌数单不灌模板，说明书第 11.2 节那一行不再当灌数依据 | 一致。第一轮点名的七处已改完 |
| 壳表仍只服务 224、225 | 第 2、5.4、7、9 节：`gapfill_policy_eval_shell` 行种类只有解读条目和多媒体条目。本叶不建立、不灌这张表。与已签收解读稿一致。本页不改解读稿 | 一致 |
| 第 3 节「趋势段 / 分区段」是否又把一次 `jobs` 拆成可兼有的两段 | 「落到哪次读取」：趋势那次查趋势表，分区那次查分区表。第 2 节已规定一次请求一种类。稿内没有「模型段失败时保留已填的趋势和分区」 | 一致 |
| 算法、调用链、221、桶、`metric_id` | 与第一轮已通过项相同。Java 不算趋势、不算分区、不写 nGQL。浏览器只打 `/display/v1/policy/**`。221 只消费第 7 项已有子图，挂接可空。222 从当次读到的行生成文件，不写对象存储，不灌 PDF、Excel、假日志。不新造 `metric_id`，不改 D4，不读 `counts`。无行则空，不用 501 充当画面 | 一致 |

### 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。同意会签不是签收。

## 第三轮（2026-11-03 晚）

- 角色：`agent:arch-agent`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 对象：返工后的 `POL-L2-DS11-VIZ-ARCH` 当前全文。本轮单独重读，不沿用第二轮结论。不改那份架构，不改 `POL-L2-DS11-READ-ARCH`，不改说明书，不改 task-registry
- 对照：说明书第 6 节评价三条、第 3 节 Job 跳、第 11.2 节可视化行与解读行；已签收解读稿里壳表与 222 的句子；调用链第 6.4 节；契约清单里 `evaluation/counts`、`evaluation/jobs`、`evaluation/shells`

### 结论

同意会签

### 核对

| 项 | 当前架构稿 | 判定 |
|---|---|---|
| 219、220 走 `POST /display/v1/policy/evaluation/jobs`，一次请求只一种类，不建异步任务，由 `gkxlumen-element` 读缺项表。是否仍算不新增第 4 条路径，且没把读表伪装成 Job | 第 1、7 节写评价页仍是说明书第 6 节的三条，不增加第 4 条。219、220 没有新 URL，都在已有 `jobs` 上。第 2 节：一次请求只带一种类；219 只要趋势，只读 `gkxlumenx_gapfill.gapfill_policy_eval_trend`；220 另一次请求只要分区，只读 `gapfill_policy_eval_partition`。两种都不建任务，不进 `gkxlumen-topic-async-service`，不调 Python，不占并发锁，不发 SSE。不在同一次请求里既同步填趋势或分区，又转发异步。第 4 节第 1、2 步是两次提交。读表的是 element，不是 Job 执行器 | 仍算不新增第 4 条。没把读表伪装成 Job。`jobs` 在这里只是已有资源上的种类入口。趋势、分区不进入说明书第 3 节那条 Job 跳（display → 异步服务 → Python），也不占解读稿已经收死的 `policy_focus_ads`、`policy_text_parse`。契约清单把整条 `jobs` 标成 Job，指的是资源分类；本叶这两种类不走那条异步跳，无行则空，不用 501 充当画面。调用链里「分区效果对比、多维趋势未注册则 501」仍在，本叶不改那份文件 |
| 221 不设资源、不委托专题 `/graph`、Java 不写 nGQL | 第 2 节不设 `/display/v1/policy` 资源，只消费第 7 项已有子图，挂接可空，不委托专题门面 `/graph`。第 5.3 节不走 `E-E7-POLICY-M1-L06`，不把 `/topic/v1/policy/graph` 或 `/v1/policy/graph` 改成展示地址，不把共词网络写成新算法，Java 不写 nGQL。与调用链第 6.4 节「评价页关系网只索引，不设展示新查图任务」相符 | 一致 |
| 222 是否只读 `gkxlumenx_gapfill.gapfill_policy_eval_template`，灌数单是否为 `POL-L2-DS11-VIZ-GAPFILL-L01`，是否还读 `gapfill_policy_eval_shell`。与解读稿「壳表只服务 224、225」是否还冲突 | 第 1、2、3.1、4、5.4、8、9 节都读 `gapfill_policy_eval_template`。灌数单是 `POL-L2-DS11-VIZ-GAPFILL-L01`，同一张单覆盖 219、220、222，并写明不灌壳表。第 5.4 节写模板选用不进 `gapfill_policy_eval_shell`，`POL-L2-DS11-READ-GAPFILL-L01` 不灌模板。第 2、7、9 节：本叶不建立、不灌壳表；壳表行种类仍只有解读条目和多媒体条目。解读稿第 7 节写壳表只服务 224、225，222 的模板选用不在该叶灌入；第 8 节该灌数单不灌模板。两稿不再抢同一张表 | 不冲突。说明书第 11.2 节解读行仍把模板选用和壳表写在 222–226，可视化行只有趋势表和分区表。本叶写明不以那一行当灌数依据，也不改说明书。222 的可实现落点是本叶这张模板表和这张灌数单 |
| 浏览器只打 `/display/v1/policy/**`，不直连 demo，接口不直接返回 mock | 第 2 节浏览器只打这条前缀。不改打 `/topic/v1/policy`，不打开算法中台页，不打 `/v1/policy/**`。第 3.1、8 节不迁 `policyData.js`，不嵌 `demo-ui-system-test` 的效果评估页，不打 `/v1/policy/graph`。第 7 节不允许接口函数直接返回 mock，不允许用 501 充当画面。219、220 无行则空，不补曲线，不返回演示矩阵。222 无选用行则模板空，文件只从当次读到的行生成，不内嵌写死的 PDF 或 Excel | 一致 |
| `counts` 不被本叶占用 | 第 2 节：`counts` 只服务短板条数和机遇条数，序号不在 219–222。本叶不读 `counts`，不把趋势点或分区对照数写进那次响应。第 6 节排除该资源。第 4 节读失败时不清空同页已经返回的短板条数和机遇条数，并写那两条不在本叶 | 一致 |

### 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。同意会签不是签收。

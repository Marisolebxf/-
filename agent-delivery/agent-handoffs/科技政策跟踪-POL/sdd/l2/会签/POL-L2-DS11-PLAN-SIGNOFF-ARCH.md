# POL-L2-DS11-PLAN-SIGNOFF-ARCH · 政策分析评价 · 推荐方案报告交互展示 · 架构会签

- 角色：`agent:arch-agent`
- 日期：2026-11-03
- 对象：`POL-L2-DS11-PLAN-ARCH`
- 监管：`human:淮政玮`
- 对照：`POL-L2-DS11-PLAN-ARCH`（2026-11-03）。本页不重新设计，不改那份架构。下游 `POL-L2-DS11-PLAN-API` / `METRIC` / `DATA` 尚未成册，本页不等、不代写
- 范围：SRS 序号 227–231。说明书第 11.2 节与 `sdd/调用链与边界.md` 只作对照。共享的 `evaluation/jobs`、`evaluation/shells` 对照已会签的 `POL-L2-DS11-READ-ARCH`（223–226）和 `POL-L2-DS11-VIZ-ARCH`（219–222）

## 结论

同意会签

227–229 读 `gapfill_policy_eval_scheme`，不进异步。230、231 走 `shells`，读的仍是这张方案表，不读 `gapfill_policy_eval_shell`。与已会签 READ 的异步键、壳表行种类都不重叠，可以按种类分发。

可视化稿第 2 节和第 6 节把序号 229 写成仍走异步，并把 222 的模板选用交给解读灌数单。那两处阻塞在 `POL-L2-DS11-VIZ-ARCH`，本稿没有这两句。合一份 `jobs` / `shells` 分发器之前，要先改可视化稿。本稿不改。

## 核对

| 项 | 架构稿 | 判定 |
|---|---|---|
| 算法只在 Python。Java 不生成方案、不按弹性现算、不写 nGQL | 五叶没有方案生成、参数模拟、路径生成、意见采集、导出模型。228 不调用 `polan.text.simulate.run`。229 不读政策子图。`PolicyAnalysisTypes` 不加 `policy_scheme`，也不把五叶塞进 `policy_timeseries`、`policy_regional`、`policy_shenzhen`、`policy_focus`、`policy_effect`、`policy_match` | 一致 |
| 浏览器只打 `/display/v1/policy/**` | 只用已有的 `evaluation/jobs`、`evaluation/shells`。不改打 `/topic/v1/policy`，不打 `/v1/policy/**`，不打 `/internal/analysis/policy/simulate`，不调用 `demo-*`，不嵌效果推演页。`E-E7-POLICY-M1-L06` 不是本页路径 | 一致 |
| `evaluation/jobs`：227–229 不进异步，能否与 READ、VIZ 按种类分发 | 227 方案对照、228 参数模拟、229 路径与风险都由 `gkxlumen-element` 同步读 `gapfill_policy_eval_scheme`。不进 `gkxlumen-topic-async-service`，不写任务行。第 2 节写明按种类分发，不能把整条 `jobs` 改成只读这张表。READ 的 `jobs` 只有 `policy_focus_ads`（223 焦点）和 `policy_text_parse`（226 摘要），进异步，读的是已有 ADS。两种类的表和管道都不重叠。第 2 节把「解读」写在 `jobs` 的邻接名单里；224 的解读条目在 `shells`，不在 `jobs`。同句写明这些键由 VIZ、READ 各自定义 | 一致。接口单不得因「解读」一词在 `jobs` 上新开种类。VIZ 把 229 写成异步，与本行矛盾，改可视化稿，不改本叶 |
| `evaluation/shells`：230、231 不读壳表 | 230 互动意见、231 方案报告读 `gapfill_policy_eval_scheme`。不读 `gapfill_policy_eval_shell`，不灌模板选用。READ 会签：壳表只服务 224、225，222 的模板选用不灌入 shell。第 9 节存储种类只有方案对照、参数模拟、路径与风险、互动意见。231 的请求种类叫方案报告，不另占存储种类，导出读方案对照行和互动意见行。第 2 节把报告模板、多媒体、分析报告份数留给另外两个二级 | 一致。230、231 与 224、225 可以按种类分到不同的表。222 的模板选用仍被可视化稿指给壳表，那是可视化稿的阻塞，不是本叶 |
| 做不到真算时只读 `gkxlumenx_gapfill` 的 `gapfill_` 表。接口不直接返回 mock，不用 501 充当功能 | 五叶共用 `gapfill_policy_eval_scheme`。不写 ODS、DWD、ADS，不写供应方库。无行则该块空。少于两行则对比空，不造第二个方案。228 对不上参数档则预览空，采纳不插入。230 请求不插入、不更新、不删除。231 从当次读到的行生成，响应不内嵌写死的文件。调用链第 3 节仍写方案对比、参数模拟、实施路径「模型未注册则 501」。本叶不改那份文件，改走读表 | 一致 |
| 228 不挂推演键。229 用已有指标且不读图 | 不把 `M_POLICY_SIMULATE`、`ads.policy_simulate` 迁到评价页。229 行上的 `metric_id` 用已有 `M_POLICY_DS_11_POLICY_EVAL_015`，不新注册，不改 D4，不把行写成已上线。口径是生成结果，不是第 7 项在线读图。序号 241 不顶替 229 | 一致 |
| 不新建桶。display 不直连库、不直连 Python | 231 不写对象存储。trace 沿既有展示链，display 往 element 带 traceId，不新设计观测点。Java 不直连库，不直连 Python | 一致 |
| 不新造 `metric_id`，不改 D4，不改注册表 | 其余三种存储种类没有已挂指标，`metric_id` 留空。不挂 `M_POLICY_LAYOUT_REC_COUNT`、`M_POLICY_DEEP_171_1`。不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开。不把序号 210 的 `gapfill_policy_audience_feedback` 当成方案意见 | 一致 |

## 路径、表、sub_type

| 序号 | 公开路径 | 表 | sub_type |
|---|---|---|---|
| 227 | `POST /display/v1/policy/evaluation/jobs` | `gkxlumenx_gapfill.gapfill_policy_eval_scheme` 的方案对照行。不另建表 | 无。不进 `PolicyAnalysisTypes`，不进 `JOB_SUB_TYPES`。请求种类：方案对照。同步读，不建任务 |
| 228 | 同上 | 同表的参数模拟行 | 无。请求种类：参数模拟。同步读，不建任务 |
| 229 | 同上 | 同表的路径与风险行。`metric_id` 用已有 `M_POLICY_DS_11_POLICY_EVAL_015` | 无。请求种类：路径与风险。不进异步。不读子图 |
| 230 | `GET /display/v1/policy/evaluation/shells` | 同表的互动意见行。不读 `gapfill_policy_eval_shell` | 无。请求种类：互动意见。同步读 |
| 231 | 同上 | 不另建行。读方案对照行和互动意见行 | 无。请求种类：方案报告。存储不单占种类 |

227–231 的内部跳是：浏览器 → 网关 → `gkxlumen-display` → `gkxlumen-element` → `gkxlumenx_gapfill.gapfill_policy_eval_scheme`。不进入 `gkxlumen-topic-async-service`，不进入 Python `/internal/*`。

READ 的 223 焦点、226 摘要仍走异步：`sub_type` 只有 `policy_focus_ads`、`policy_text_parse`。224、225 仍是 `shells` 同步读壳表。本叶不改这两条。

VIZ 的 219、220 若保持「一次请求只读趋势或缺项分区、不建任务」，可以与上表并列。VIZ 现行第 2 节允许同一次 `jobs` 兼有同步段和异步段，并把 229 划进异步。那两句与本表冲突，已在可视化会签写明不同意。本页不改那份架构。

说明书第 11.2 节方案行就是这一张 `gapfill_policy_eval_scheme`：方案对照、参数模拟结果、路径节点和风险、专家意见条目，不灌导出文件。231 不另灌。与第 9 节四种存储种类一致。

调用链第 3 节的 501、第 4 节「228 不改挂推演键」：本叶读缺项表，不调用 `simulate.run`，不用 501 充当功能。本页不改写调用链文件。

`POL-L2-DS11-PLAN-GAPFILL-L01` 的执行人是 `data-agent`，监管 `human:淮政玮`，状态 backlog。本叶不执行灌数。查询请求不灌数。D4 保持 mock。

## 铁律

1. 算法只在 Python。本五叶没有新模型。Java 不生成方案，不写 nGQL，不把 `simulate.run` 加进 `PolicyAnalysisTypes`。
2. 调用链是浏览器 → `/display/v1/policy/**` → Java → `gkxlumen-element` 只读缺项表。展示不直连 Python，不直连库，不调用 `demo-*`。
3. 五叶只读 `gkxlumenx_gapfill.gapfill_policy_eval_scheme`。接口不直接返回写死的方案、分数、路径、意见或文件。不用 501 充当功能。
4. `evaluation/jobs` 上，227–229 不进异步。与 `policy_focus_ads`、`policy_text_parse` 按种类分开。不把整条 `jobs` 收成只读这张表。
5. `evaluation/shells` 上，230、231 读方案表。不把模板选用或多媒体灌进 `gapfill_policy_eval_scheme`，也不去读壳表。
6. 229 不读第 7 项子图。228 不挂 `M_POLICY_SIMULATE`。
7. 不新建桶。231 不写对象存储。不新造 `metric_id`，不改 D4。

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。

## 第二轮（2026-11-03 返工后）

- 角色：`agent:arch-agent`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 对象：`POL-L2-DS11-PLAN-ARCH`。五叶读法未改，只复核第 2 节已改的分发句。本页不改那份架构，不改已签收的 `POL-L2-DS11-READ-ARCH`，不改代码，不改 task-registry
- 对照：返工后的 `POL-L2-DS11-VIZ-ARCH`；已签收解读稿（壳表只服务 224、225，不灌模板）

### 结论

同意会签

### 核对

| 项 | 架构稿 | 判定 |
|---|---|---|
| 227–229 仍同步读 `gapfill_policy_eval_scheme`，不进异步 | 第 2 节资源表三行仍是方案对照、参数模拟、路径与风险，`gkxlumen-element` 只读方案表。229 写「不进第 7 项读图」。第 4 节第 1–3 步、第 5.1–5.3 节、第 8 节未改成异步。第 2 节末句写「本叶 227–229 仍不进异步」。不进 `gkxlumen-topic-async-service`，不加 `policy_scheme` | 一致 |
| 230–231 不读壳表 | 第 2 节：互动意见、方案报告读同一张方案表。第 5.4、5.5 节与第 9 节存储种类仍是方案对照、参数模拟、路径与风险、互动意见。231 不另占存储种类，导出读方案对照行和意见行。稿内没有把 230、231 指到 `gapfill_policy_eval_shell` | 一致 |
| 第 2 节分发句：一次请求一种类，并写明 222 读 `gapfill_policy_eval_template`。不得把整条 `jobs` 或整条 `shells` 改成只读方案表 | 该句写：`jobs` 一次只带一种类；焦点与摘要的异步键只有 `policy_focus_ads`、`policy_text_parse`；趋势、分区由可视化稿定，各一次请求，不进异步；222 的模板选用读 `gapfill_policy_eval_template`，不读壳表；多媒体留给解读稿的 `gapfill_policy_eval_shell`；「实现时按种类分发」；「不能把整条 `jobs` 或整条 `shells` 都改成只读这张方案缺项表」。同节资源表仍只覆盖 227–231 自己的种类。第 2 节「本二级的种类仍由 element 读缺项表」限定在本二级，不把另外两个二级收进方案表 | 一致 |
| 与返工后可视化稿的 229、222 | 可视化稿第 2、6 节已改成 229 不进异步、读 `gapfill_policy_eval_scheme`；222 读 `gapfill_policy_eval_template`。本句与之同向 | 一致 |
| 五叶读法以外、第一轮已通过的项 | 算法仍只在 Python。228 不调用 `polan.text.simulate.run`。229 的 `metric_id` 仍用已有 `M_POLICY_DS_11_POLICY_EVAL_015`，不读图，不改 D4。不新造 `metric_id`。231 不写对象存储。浏览器仍只打 `/display/v1/policy/**`。接口不直接返回写死的方案、分数、路径、意见或文件 | 一致 |

### 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。同意会签不是签收。第一轮结论原文保留。

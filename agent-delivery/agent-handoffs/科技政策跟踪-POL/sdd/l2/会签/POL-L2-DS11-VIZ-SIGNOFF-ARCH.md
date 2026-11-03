# POL-L2-DS11-VIZ-SIGNOFF-ARCH · 政策分析评价 · 政策分析报告可视化呈现 · 架构会签

- 角色：`agent:arch-agent`
- 日期：2026-11-03
- 对象：`POL-L2-DS11-VIZ-ARCH`
- 监管：`human:淮政玮`
- 对照：`POL-L2-DS11-VIZ-ARCH`（2026-11-03）。本页不重新设计，不改那份架构。下游 `POL-L2-DS11-VIZ-API` / `METRIC` / `DATA` 尚未成册，本页不等、不代写
- 范围：SRS 序号 219–222。说明书第 6 节、第 11.2 节与 `sdd/调用链与边界.md` 第 6.4 节只作对照。已会签的 `POL-L2-DS11-READ-ARCH` 只核对壳表与序号 222

## 结论

有条件同意

219、220、221 的路径、读表和读图成立。222 把模板选用的灌入指给已会签的解读二级，与该叶「壳表只服务 224、225」矛盾。这一条不闭合，本页不能写成无条件同意。

## 核对

| 项 | 架构稿 | 判定 |
|---|---|---|
| 219、220 走 `POST /display/v1/policy/evaluation/jobs`，不建异步任务，由 `gkxlumen-element` 读 gapfill。是否仍算不新增第 4 条路径，且不把读表伪装成 Job | 说明书第 6 节评价只有 `counts`、`jobs`、`shells` 三条。219、220 仍用已有的 `POST evaluation/jobs`，没有第四条 `/display/v1/policy` 路径。契约输入清单已把趋势图、分区对比的空态放在这条 `jobs` 上。只要趋势或只要分区时，`gkxlumen-display` 不转发 `gkxlumen-topic-async-service`，不调 Python，不写任务行，不占并发锁，不发 SSE；`gkxlumen-element` 同步读 `gapfill_policy_eval_trend`、`gapfill_policy_eval_partition`。焦点、效能、摘要、实施路径仍走原来的异步管道。两段分开：模型段失败时，不清空已经读到的趋势和分区。切时间、区域、类别不自动起任务 | 成立。不新增第 4 条路径。趋势段和分区段是同步读表，没有写成已创建的 Job。资源名仍是 `jobs`，是因为三条路径已经用完。下游若把这两段登记成会写任务行的 sub_type，才变成伪装；架构稿已经禁止，API 分册尚未成册，本页不代写 |
| 221 不设资源，不委托专题 `/graph`，Java 不写 nGQL | 不设 `/display/v1/policy` 资源。只消费第 7 项已有子图，挂接可空。不委托专题门面 `/graph`，不把 `/topic/v1/policy/graph` 或 `/v1/policy/graph` 写成展示浏览器地址。不走 `E-E7-POLICY-M1-L06`。不重做抽取，不重开 GDF，不把共词网络写成新算法。Java 不写 nGQL。子图没有则弦线图、关系网和路径都空 | 一致。与调用链第 6.4 节相符：序号 221 只索引，不设展示新查图任务，不在政策组新开图接口。图上 `bff` 到子图的箭头只表示消费可空；正文已禁止 `gkxlumen-display` 直连库 |
| 222 读 `gapfill_policy_eval_shell`，与 READ-ARCH「shell 只服务 224、225，222 的模板选用不在本叶灌入」是否矛盾 | 本叶：`GET evaluation/shells`，`gkxlumen-element` 只读壳表里的模板选用行；表由解读二级建立和灌数，灌数单 `POL-L2-DS11-READ-GAPFILL-L01`，本叶不另建、不灌 PDF / Excel / 假日志。已会签的 `POL-L2-DS11-READ-ARCH`：壳表只服务 224、225；该灌数单只灌解读条目和多媒体条目，写明不灌模板；序号 222 的模板选用不在该叶灌入。说明书第 11.2 节仍把「模板选用」和壳表写在解读行 222–226。本叶沿用了这一句，解读二级会签时已经收窄 | 矛盾。读 `shells` 这条路径本身与契约输入清单里「报告模板导出」落在同步 `shells` 相符，也没有新占一条路径。矛盾在灌入归属：不能同时认定「解读二级会灌模板选用」和「该叶不灌模板、壳表只服务 224、225」。无选用行则模板区空，这一空态可以保留；「灌什么由解读二级定」不能当成已闭合的灌数方。本页不改两份架构，也不另定表 |
| 浏览器只打 `/display/v1/policy/**`，不直连 demo，接口不直接返回 mock | 浏览器只打 `/display/v1/policy/**`。不改打 `/topic/v1/policy`，不打开算法中台页面，不打 `/v1/policy/**`。demo 的 `policyData.js`、`/v1/policy/graph`、效果评估页只作对照，不迁进展示接口，不嵌进 lumen 页面。219、220 无行则图空，不补默认曲线。221 无子图则空，不灌弦线矩阵和演示路径。222 无选用行则模板空；要文件时只从当次读到的行生成，响应不内嵌写死的 PDF 或 Excel。不用 501 充当这四叶的画面 | 一致。符合 D12、D18。D4 保持 mock。不新造 `metric_id`。指标分册里 219、220、222 的「无模型」字样本叶不改 |
| `counts` 不被本叶占用 | `evaluation/counts` 只服务短板条数和机遇条数，序号不在 219–222。本叶不读 `counts`，不把趋势点或分区对照数写进那次响应。某一块读失败，不清空同页已经返回的短板条数和机遇条数 | 一致 |

## 路径与表

| 序号 | 公开路径 | 表或来源 | 是不是 Job |
|---|---|---|---|
| 219 | `POST /display/v1/policy/evaluation/jobs` 的趋势段 | 新建 `gkxlumenx_gapfill.gapfill_policy_eval_trend`。不写入 ODS、DWD、ADS。灌数单 `POL-L2-DS11-VIZ-GAPFILL-L01`，独立脚本，查询不灌数 | 否。同步读，不建任务 |
| 220 | 同上，分区段 | 新建 `gkxlumenx_gapfill.gapfill_policy_eval_partition`。同一张灌数单。柱和热力读同一批行 | 否。同步读，不建任务 |
| 221 | 不设 `/display/v1/policy` 资源 | 第 7 项已有子图。`E-E7-POLICY-M1-L02` 已完成，抽取脚本仍是 backlog。不建表 | 否。不是 Job，也不是新的查图任务 |
| 222 | `GET /display/v1/policy/evaluation/shells` | 已定的 `gkxlumenx_gapfill.gapfill_policy_eval_shell`。本叶不建表 | 否。同步读。模板选用行的灌入方与已会签解读二级矛盾，见上表 |

219、220 的内部跳是：浏览器 → 网关 → `gkxlumen-display` → `gkxlumen-element` → `gkxlumenx_gapfill`。不进入 Python `/internal/*`。`gkxlumen-display` 不直连库，不直连 Python，不写算法，不写 nGQL。

## 铁律

1. 算法只在 Python。本四叶没有新模型。Java 不算趋势、不算分区、不写 nGQL，也不把 `effect.py` 或 `policyData.js` 抄进 Java。
2. 调用链是浏览器 → `/display/v1/policy/**` → Java。219、220、222 的同步读到 `gkxlumen-element` 为止。221 只消费已有子图。展示不直连 Python，不直连库，不调用 `demo-*`。
3. 219、220 只建 `gkxlumenx_gapfill` 里的两张 `gapfill_` 表，接口只读。无行则空。这符合说明书第 11 节：没有算法也没有表时，只接受建表、灌入 mock、再读表。
4. 221 与调用链第 6.4 节一致：不委托专题 `/graph`，Java 不写 nGQL，挂接可空。
5. 222 的读取路径可以放在已有 `shells` 上，但灌数方与已会签的 `POL-L2-DS11-READ-ARCH` 矛盾。这一条不通过，所以结论是有条件同意。
6. `counts` 仍只给短板条数和机遇条数。本叶不占用。
7. 不新建桶。222 不写对象存储，不灌导出文件，不灌假操作日志。

## 条件

闭合之前，实现 222 时不能把模板选用行算进 `POL-L2-DS11-READ-GAPFILL-L01`。无选用行则模板区空，可以照稿做。谁来灌模板选用，要等解读二级改口并重新会签，或另定归属后再审。两件事都不在本页做。

219、220、221 不依赖这条条件。

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。

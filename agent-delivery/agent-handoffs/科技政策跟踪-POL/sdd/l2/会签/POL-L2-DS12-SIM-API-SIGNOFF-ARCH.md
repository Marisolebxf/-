# POL-L2-DS12-SIM-API-SIGNOFF-ARCH · 政策效果推演 · 科技政策推演 · 后台接口 · 架构会签

- 角色：`agent:arch-agent`
- 日期：2026-11-05
- 对象：`POL-L2-DS12-SIM-API`（2026-11-05）
- 监管：`human:淮政玮`
- 强度：ponytail off
- 对照：`POL-L2-DS12-SIM-ARCH`（2026-11-05 第 7、9 节；读法仍以第 2、5 节为准）。`POL-L2-DS12-EST-API` 只核种类是否撞车。本页不重新设计，不改接口分册，不改架构分册，不改 EST 分册
- 范围：SRS 序号 237–242。推演整页仍只有一条 `POST /display/v1/policy/simulation/jobs`

## 结论

同意会签

237 同步读已有 `ads.policy_text_parse`，请求不调用 `polan.text.parse.run`，不灌 gapfill。238、239、241、242 按种类同步读 `gkxlumenx_gapfill.gapfill_policy_sim_result`。240 无资源。242 不产生文件。空态是空，HTTP 成功，不用 501 充当功能。与 232–236 共用这一条 `simulation/jobs`，不新建作业入口，不建第二个分发器。请求种类与 `POL-L2-DS12-EST-API` 不撞车。

同意会签不是签收。

## 核对

| 项 | 接口稿 | 判定 |
|---|---|---|
| 237–242 都有落点。不新建作业入口。有资源的五叶共用已有 `POST /display/v1/policy/simulation/jobs` | 第 1 节：237、238、239、241、242 都是这一条，一次请求只带一种类。240 写「无」。偏离第 3 条与第 10 节写明不新建作业入口。控制器若尚未存在，只补契约里已有的这一条，补上后仍按种类分发，不为 237 另开解析 URL，不为 240 另开查图 URL | 一致 |
| 237 同步读 `ads.policy_text_parse`。不调 `polan.text.parse.run`。不灌 gapfill | 第 1、3、9 节：种类为文本解析，element 只读解析行，条款行排除。同步读，不建任务。请求路径不调用 `run()`。不建文本解析缺项行，查询不写该表。空态是该政策无解析行则报告空 | 一致。对齐架构第 9 节：237 不灌缺项行 |
| 238、239、241、242 读 `gkxlumenx_gapfill.gapfill_policy_sim_result` | 第 1、2、4–8 节：重点行、影响范围行、路径环节行、解读段落行都在这一张表。库名写明 `gkxlumenx_gapfill`。不读 `gapfill_policy_sim_forecast`，不读 `gapfill_policy_sim_stakeholder`。查询不灌数 | 一致。对齐架构第 7、9 节：本叶四种只进第一张 |
| 240 无资源 | 第 1、6、9 节：无 HTTP 资源，无种类，不走 `simulation/jobs`。页面消费已有第 7 项政策子图。不新建查图任务，不新建查图接口。Java 不写 nGQL | 一致 |
| 242 不产生文件 | 第 8、9、10 节：页面呈现当次读到的正文。不产生 PDF，不产生 Word。响应不内嵌写死文件。不写对象存储，不新建桶，前端不直连 RustFS。不灌自定义格式配置 | 一致。对齐架构第 9 节「不灌」列的 PDF / Word |
| 空态是空，不是 501 | 第 1、3–9 节：237、238、239、241、242 无行则该区空，HTTP 成功，不返回 501。接口函数不返回写死的解析、重点、影响对象、时间表或文件。240 不另造 501 接口。清单、`指标与501.md`、说明书里仍写的 501 不覆盖本分册，本分册不改那些文件 | 一致。对齐架构第 7 节：会签前不改上游 501 文，可实现链路是读表 |
| 禁止第二个分发器、`/topic/v1/policy`、`demo-*` | 第 2、10 节：不建第二个分发器。不把整条 `jobs` 改成只读结果表。浏览器只打 `/display/v1/policy/**`。不改打 `/topic/v1/policy`、`/policy/topic/v1/policy`、`/topicAsync/**`、`/v1/policy/**`。不把 `E-E7-POLICY-M1-L06` 写成展示路径。不调用 `demo-*`。不直连 `GET /v1/policy/text/parse`。五次读取不进 `gkxlumen-topic-async-service`，不进 `POST /internal/policy/jobs/execute` | 一致 |
| 与 `POL-L2-DS12-EST-API` 种类不撞车 | 本分册请求种类只有：文本解析、重点可视化、影响范围、路径预测、解读报告。240 不占种类。EST 分册请求种类是：未出台仿真、新出台预测、区域空间、多维评估、利益攸关方。两组中文名不相交。235 的多维评估行与本分册四种行同表不同种类；236 的请求种类是利益攸关方，行在 stakeholder 表。本分册写明不定义这两个请求，不改这两行的行内容 | 一致 |
| 架构第 7、9 节的两张表与灌数归属 | 第 2 节：235 灌进 `gapfill_policy_sim_result`，236 灌进 `gapfill_policy_sim_stakeholder`。两张都保留，不收成一张，不另建第三张。读法由 EST-ARCH 定，灌数仍由 `POL-L2-DS12-SIM-GAPFILL-L01`。237 不灌。要灌的是多维评估、参与意见、重点、影响范围、路径、解读正文。本分册不执行灌数 | 一致 |
| 不新造 `metric_id`，不改 D4，不进异步白名单 | 238、239、241、242 的 `metric_id` 留空。237 沿用已有 `M_POLICY_TEXT_PARSE`。240 沿用已有 `M_POLICY_RELATION_DEGREE`，不为它加资源。不加 `policy_simulate`，不把 237–242 写入 `PolicyAnalysisTypes` 或 `JOB_SUB_TYPES`。不改评价 226 的 `policy_text_parse` 键。D4 保持 mock | 一致 |
| 算法只在 Python。display 不直连库、不直连 Python。接口不直接返回 mock | 第 2 节：`gkxlumen-display` 不直连库，不直连 Python，不写算法，不写 nGQL，不做 NLP。Java 不生成解析、重点、影响范围、路径或报告文件。mock 先落表或已在解析表，再被查询读出 | 一致 |

## 路径、表、sub_type

| 序号 | 公开路径 | 表 | sub_type |
|---|---|---|---|
| 237 | `POST /display/v1/policy/simulation/jobs` | 已有 `ads.policy_text_parse` 的解析行。不灌 gapfill | 无。请求种类：文本解析。同步读，不建任务。不调用 `polan.text.parse.run` |
| 238 | 同上 | `gkxlumenx_gapfill.gapfill_policy_sim_result` 的重点行 | 无。请求种类：重点可视化。同步读，不建任务 |
| 239 | 同上 | 同表的影响范围行 | 无。请求种类：影响范围。同步读，不建任务 |
| 240 | 无 | 不建表。消费第 7 项政策子图 | 无。不占种类，不走 `simulation/jobs` |
| 241 | `POST /display/v1/policy/simulation/jobs` | 同表的路径环节行 | 无。请求种类：路径预测。表行种类：路径环节。同步读，不建任务 |
| 242 | 同上 | 同表的解读段落行。不产生文件 | 无。请求种类：解读报告。表行种类：解读段落。同步读，不建任务 |

237、238、239、241、242 的内部跳是：浏览器 → 网关 → `gkxlumen-display` → `gkxlumen-element` 只读。不进入 `gkxlumen-topic-async-service`，不进入 Python `/internal/*`。

240 不走上述 `jobs`。

EST 分册在同一条 `simulation/jobs` 上的请求种类仍是未出台仿真、新出台预测、区域空间、多维评估、利益攸关方。本页不改那五条。

## 铁律

1. 算法只在 Python。本六叶的请求不跑解析，不生成重点、影响范围、路径或解读。Java 不写 nGQL。`gkxlumen-display` 不直连库，不直连 Python。
2. 调用链是浏览器 → `/display/v1/policy/**` → Java → `gkxlumen-element` 只读。不新建作业入口。不建第二个分发器。不改打 `/topic/v1/policy`。不调用 `demo-*`。
3. 237 只读已有 `ads.policy_text_parse`。请求不调用 `polan.text.parse.run`。不灌 gapfill。
4. 238、239、241、242 只读 `gkxlumenx_gapfill.gapfill_policy_sim_result`，按种类分开。240 无资源。
5. 242 不产生 PDF，不产生 Word，不写对象存储。
6. 空态是空。237、238、239、241、242 不用 501 充当功能。240 不另造 501 接口。
7. 请求种类与 `POL-L2-DS12-EST-API` 的未出台仿真、新出台预测、区域空间、多维评估、利益攸关方不相交。235、236 的请求定义仍在 EST 分册。

## 签收边界

本页不把任务标 done，不改任务状态。签收仍由 human:淮政玮 做。同意会签不是签收。

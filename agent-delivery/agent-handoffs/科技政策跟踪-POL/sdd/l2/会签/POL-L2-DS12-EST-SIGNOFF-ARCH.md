# POL-L2-DS12-EST-SIGNOFF-ARCH · 政策效果推演 · 效果预估 · 架构会签

- 角色：`agent:arch-agent`
- 日期：2026-11-05
- 对象：`POL-L2-DS12-EST-ARCH`（2026-11-04）。本页不改那份架构
- 监管：`human:淮政玮`
- 对照：`POL-L2-DS12-SIM-ARCH`（只核 235/236 与 237–242 有没有双份实现或第二套资源）。说明书第 11 节与第 11.2 节。`sdd/调用链与边界.md`。`sdd/契约输入清单.md` 的 `simulation/jobs`。`survey/DS-12.md`。这些文件本页都不改
- 范围：SRS 序号 232–236。只写本会签。强度 ponytail off

## 结论

不同意会签

232–234 可以按 `gkxlumenx_gapfill.gapfill_policy_sim_forecast` 同步读。235、236 的读法在第 2、8、9 节也指到说明书 11.2 的两张表，但第 5.4、5.5 节把表名写成了 `gkxlumenx_gapfill_policy_sim_result`、`gkxlumenx_gapfill_policy_sim_stakeholder`。这两处不是 `库.表`，照着做会读到另一张表。

237–242 不在本叶实现，240 两边都不设资源，同一条 `simulation/jobs` 没有第二套。调研里的 501 不参与这次不同意。

## 核对

| 项 | 架构稿 | 判定 |
|---|---|---|
| 算法只在 Python。Java 不生成预测、不按弹性现算、不写 nGQL、不直连库、不直连 Python | 五叶没有预测模型、弹性现算、文本解析、意见写入。不调用 `polan.text.simulate`。不读 `ads.policy_simulate`。`gkxlumen-display` 不直连库、不直连 Python，不写 nGQL。233 的候选政策列表复用已有全景检索：浏览器仍走展示入口，内部委托 `gkxlumen-topic-policy` 的 search/docs，不在本页现做解析 | 一致 |
| 浏览器只打 `/display/v1/policy/**` | 五叶只用已有 `POST /display/v1/policy/simulation/jobs`。不改打 `/topic/v1/policy`，不打 `/v1/policy/**`，不打 `/v1/policy/simulate`，不调用 `demo-*`，不嵌入算法中台效果推演签。`E-E7-POLICY-M1-L06` 不是本页路径 | 一致 |
| 做不到真算时只读 `gkxlumenx_gapfill` 的 `gapfill_` 表。接口不直接返回 mock。不用 501 充当功能。库名与表名写法前后一致（`库.表`） | 232–234 在第 5.1 节写明 `gkxlumenx_gapfill.gapfill_policy_sim_forecast`。无行则该区空，请求不插入，响应不内嵌写死的预测、曲线、得分或意见。235、236 不用 501 充当功能。第 2、4、8、9 节的表名是 `gapfill_policy_sim_result`、`gapfill_policy_sim_stakeholder`，库是 `gkxlumenx_gapfill`。第 5.4 节写成 `gkxlumenx_gapfill_policy_sim_result`，第 5.5 节写成 `gkxlumenx_gapfill_policy_sim_stakeholder` | 不一致。阻塞只在第 5.4、5.5 节这两个表名 |
| 五叶共用已有 `POST /display/v1/policy/simulation/jobs`，按种类分发。不新造第二套资源。不进 `PolicyAnalysisTypes` / 异步 | 第 2 节一条资源，一次请求一种类。232–236 由 `gkxlumen-element` 同步读缺项行。POST 不建任务，不进 `gkxlumen-topic-async-service`，不加 `policy_simulate`。真模型注册不在本叶。第 2 节「真推演」行是未注册模型的 501 空态，五叶缺项读不走这一行 | 一致 |
| 232–234 读 `gapfill_policy_sim_forecast`；235 读 `gapfill_policy_sim_result` 多维评估行；236 读 `gapfill_policy_sim_stakeholder`。不重复实现 237–242。240 不设资源 | 第 2、6、9 节按这个分组。237 文本解析、238 重点可视、239 影响范围、241 路径预测、242 解读报告交给 `POL-L2-DS12-SIM-ARCH`，本叶不实现。240 消费第 7 项子图，不设资源。SIM 分册覆盖 237–242，写明不重复实现 235/236，不另立资源。`gapfill_policy_sim_result` 上，235 是多维评估行，238/239/241/242 是另四种行 | 读法不重叠，无第二套资源。235、236 仍被上一行的错表名挡住 |
| `M_POLICY_SIMULATE` 只挂 232–234。不挂布局推荐键。不新造 `metric_id`，不改 D4。不新建桶 | 232–234 行上用已有 `M_POLICY_SIMULATE`。235、236 的 `metric_id` 留空，不借用 `M_POLICY_SIMULATE`，不借用 `M_POLICY_DEEP_168_1`。不挂 `M_POLICY_DEEP_171_1`、`M_POLICY_LAYOUT_REC_COUNT`。不改 D4，不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开。稿内没有新桶，236 的请求不写对象存储 | 一致 |
| 调研仍写 501 | `survey/DS-12.md` 把 232–236 记为 501。调用链第 3 节、契约 `simulation/jobs` 仍写未注册则整页空。架构稿声明会签前不改这些文件，五叶功能改走读表 | 一致。不构成不同意 |

## 路径、表、sub_type

| 序号 | 公开路径 | 表 | sub_type |
|---|---|---|---|
| 232 | `POST /display/v1/policy/simulation/jobs` | `gkxlumenx_gapfill.gapfill_policy_sim_forecast` 的未出台仿真行。不另建表 | 无。不进 `PolicyAnalysisTypes`，不进 `JOB_SUB_TYPES`。请求种类：未出台仿真。同步读，不建任务 |
| 233 | 同上 | 同表的新出台预测行。`metric_id` 用已有 `M_POLICY_SIMULATE` | 无。请求种类：新出台预测。不调 `parse/jobs` |
| 234 | 同上 | 同表的区域空间行。`metric_id` 用已有 `M_POLICY_SIMULATE` | 无。请求种类：区域空间。服务端只回行 |
| 235 | 同上 | 应读 `gkxlumenx_gapfill.gapfill_policy_sim_result` 的多维评估行。第 5.4 节写成 `gkxlumenx_gapfill_policy_sim_result` | 无。请求种类：多维评估。同步读，不建任务。`metric_id` 留空 |
| 236 | 同上 | 应读 `gkxlumenx_gapfill.gapfill_policy_sim_stakeholder` 的参与意见行。第 5.5 节写成 `gkxlumenx_gapfill_policy_sim_stakeholder` | 无。请求种类：利益攸关方。第 5.5 节「参与意见」指行内容，不另开种类。请求不插入 |

232–236 的结果跳是：浏览器 → 网关 → `gkxlumen-display` → `gkxlumen-element` → `gkxlumenx_gapfill` 的对应 `gapfill_` 表。不进入 `gkxlumen-topic-async-service`，不进入 Python `/internal/*`。233 选已出台政策时，候选列表走已有全景检索，那条跳不代替上表的 `jobs`。

SIM 分册的 237 读已有 `ads.policy_text_parse`。238、239、241、242 读 `gkxlumenx_gapfill.gapfill_policy_sim_result` 的重点、影响范围、路径环节、解读段落。240 不设种类。这些种类本叶不实现。同一张结果表上的行种类不同，不是 235 的第二份实现。

说明书第 11.2 节：232–234 归 `gapfill_policy_sim_forecast`，灌数单 `POL-L2-DS12-EST-GAPFILL-L01`；235 的多维评估与 236 的参与意见归 `gapfill_policy_sim_result`、`gapfill_policy_sim_stakeholder`，灌数单 `POL-L2-DS12-SIM-GAPFILL-L01`。库是 `gkxlumenx_gapfill`。本叶不执行灌数。D4 保持 mock。

调用链第 3 节仍写整页推演 501。本叶五叶的功能是读缺项表。本页不改写调用链文件。

## 铁律

1. 算法只在 Python。本五叶没有新模型。Java 不生成预测，不按弹性现算，不写 nGQL。展示不直连 Python，不直连库。
2. 调用链是浏览器 → `/display/v1/policy/simulation/jobs` → `gkxlumen-display` → `gkxlumen-element` 只读缺项表。不打 `/topic/v1/policy`，不打 `/v1/policy/**`，不调用 `demo-*`。`E-E7-POLICY-M1-L06` 不是路径。
3. 232–234 的 `库.表` 是 `gkxlumenx_gapfill.gapfill_policy_sim_forecast`。235、236 在第 5.4、5.5 节没有写成 `gkxlumenx_gapfill.gapfill_policy_sim_result`、`gkxlumenx_gapfill.gapfill_policy_sim_stakeholder`。接口不直接返回写死的预测、得分或意见。五叶不用 501 充当功能。本条因两个表名不通过。
4. 五叶共用已有 `simulation/jobs`，一次一种类。不新造第二套资源。不进 `PolicyAnalysisTypes`，不进异步管道。
5. 235 只读多维评估行，236 只读参与意见行。237–242 不在本叶实现。240 不设资源。
6. `M_POLICY_SIMULATE` 只挂 232–234。不挂布局推荐键。不新造 `metric_id`，不改 D4。不新建桶。
7. 调研、调用链、契约里的 501 保持原样。这三条不构成不同意。

## 签收边界

本页不把任务标 done。签收仍由 human:淮政玮 做。会签结论不是签收。

## 第二轮（2026-11-05 返工后）

结论：同意会签

第一轮结论原文保留：不同意会签。本轮只核那一处阻塞是否已解开。

核对表：

| 项 | 返工后 | 判定 |
|---|---|---|
| 第 5.4 节是否已是 `gkxlumenx_gapfill.gapfill_policy_sim_result` | 现为：表 `gkxlumenx_gapfill.gapfill_policy_sim_result`（SIM 组，11.2 定名），种类为多维评估。与第 5.1 节 `gkxlumenx_gapfill.gapfill_policy_sim_forecast` 同为 `库.表`。表名与说明书 11.2「推演 · 仿真 235–242」的 `gapfill_policy_sim_result` 一致 | 是 |
| 第 5.5 节是否已是 `gkxlumenx_gapfill.gapfill_policy_sim_stakeholder` | 现为：表 `gkxlumenx_gapfill.gapfill_policy_sim_stakeholder`（SIM 组），种类为参与意见。同为 `库.表`。表名与说明书 11.2 的 `gapfill_policy_sim_stakeholder` 一致 | 是 |
| 读法、种类、调用链有没有被带着改掉 | 相对已提交稿，这两句只在库名与表名之间补了点。种类仍是多维评估、参与意见。读法仍是 element 只读对应缺项行；236 请求不插入。调用链仍是浏览器 → `/display/v1/policy/simulation/jobs` → `gkxlumen-display` → `gkxlumen-element`。状态行另加一句「2026-11-05 只改第 5.4、5.5 节的库.表写法，读法未改」，不改读法 | 没有 |

签收边界：本页不把任务标 done。签收只由 human:淮政玮 做。同意会签不是签收。第一轮结论原文保留。

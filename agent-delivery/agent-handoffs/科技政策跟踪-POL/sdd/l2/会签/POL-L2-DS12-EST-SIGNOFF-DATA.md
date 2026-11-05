# POL-L2-DS12-EST-SIGNOFF-DATA · 政策效果推演 · 效果预估 · 数据会签

- 角色：`agent:data-agent`
- 日期：2026-11-05
- 对象：`POL-L2-DS12-EST-ARCH`
- 监管：`human:淮政玮`
- 对照：`POL-L2-DS12-EST-ARCH` 第 9 节（并核对第 5.1、5.4、5.5 节）；`POL-L2-DS12-SIM-ARCH` 第 9 节；`科技政策跟踪-系统详细设计说明书.md` 第 11.2 节「推演 · 预估 232–234」「推演 · 仿真 235–242」
- 范围：SRS 232–236
- 结论：**不同意会签**

本页只核对数据落点：库、表、种类、235/236 读哪张表、`metric_id`、`fill_method`、D4、不灌项。不定字段级 DDL。不改架构稿，不改任务状态，不建库，不灌数。

## 库表核对

| 口径 | 架构 | 判定 |
|---|---|---|
| 库只允许 `gkxlumenx_gapfill`。表名以 `gapfill_` 开头。不写 ODS、DWD、ADS、供应方库 | 第 9 节自建只写库 `gkxlumenx_gapfill`、表名 `gapfill_policy_sim_forecast`。第 7 节不加 ODS、DWD、ADS 表。233 的候选政策列表复用已有全景检索，不新建读面，预测行不写入 ODS | 第 9 节一致。第 5.4、5.5 节见阻塞 |
| 本叶自建只一张 `gapfill_policy_sim_forecast`。不拆成三张。种类只有未出台仿真、新出台预测、区域空间 | 第 5.1 写法为 `gkxlumenx_gapfill.gapfill_policy_sim_forecast`。第 5.2、5.3、9 节同表三种。232、233、234 各一种 | 一致 |
| 235 读 `gapfill_policy_sim_result` 多维评估行，236 读 `gapfill_policy_sim_stakeholder`。这两张不在本叶重建 | 第 0、2、4、8、9 节是这两张表名，并写明不在预估表、不建第二套。第 5.4、5.5 节把库名和表名粘成一个标识 | 阻塞 |
| 与 SIM 第 9 节、说明书 11.2 的表名一致 | SIM 第 9 节：库 `gkxlumenx_gapfill`，表名 `gapfill_policy_sim_result`；236 点名 `gapfill_policy_sim_stakeholder`，235/236 行归 EST 半区已裁定的这两张，SIM 本叶不改灌数内容。说明书 11.2：预估行只有 `gapfill_policy_sim_forecast`；仿真行是 `gapfill_policy_sim_result`、`gapfill_policy_sim_stakeholder` | 第 0、8、9 节表名一致。第 5.4、5.5 节不一致 |
| 232–234 行 `metric_id` 用已有 `M_POLICY_SIMULATE`。235、236 留空。不新造 `metric_id`。`fill_method=manual`。D4 保持 mock | 第 5.1–5.3、9 节。第 5.4、5.5 节留空，不借用推演键填评估分。第 7 节不改 D4 | 一致 |
| 不灌中台三条情景原文、弹性现算、布局推荐条数。查询不灌数。236 请求不插入 | 第 9 节不灌列含中台三条情景原文、弹性现算。第 1.3、6 节：布局推荐键不进本页、不互相填数，要灌列不含条数。第 4、5.5、8 节：236 请求不插入。第 9 节：查询请求不灌数 | 一致 |
| `POL-L2-DS12-EST-GAPFILL-L01` 仍是 backlog。本页不执行。字段级 DDL 留给 `POL-L2-DS12-EST-DATA` | 第 9 节。235/236 的字段与灌数仍由 SIM 组两单负责，本叶不执行那两张 | 一致 |

阻塞原因：第 5.4 节写表 `gkxlumenx_gapfill_policy_sim_result`，第 5.5 节写表 `gkxlumenx_gapfill_policy_sim_stakeholder`。库名 `gkxlumenx_gapfill` 与表名粘在一起，中间没有点。第 5.1 节预估表是 `gkxlumenx_gapfill.gapfill_policy_sim_forecast`。粘连后的标识不是库 `gkxlumenx_gapfill` 里的表，也不是说明书 11.2 与 SIM 第 9 节点名的 `gapfill_policy_sim_result`、`gapfill_policy_sim_stakeholder`。235、236 的读落点因此前后不一致。

须改的句子：

1. 第 5.4 节：「表 `gkxlumenx_gapfill_policy_sim_result`（SIM 组，11.2 定名），种类为多维评估。」库与表写成 `gkxlumenx_gapfill.gapfill_policy_sim_result`。
2. 第 5.5 节：「表 `gkxlumenx_gapfill_policy_sim_stakeholder`（SIM 组），种类为参与意见。」库与表写成 `gkxlumenx_gapfill.gapfill_policy_sim_stakeholder`。

这两张仍不在本叶重建。本页不代改这两句，也不补 DDL。

## 不灌清单

| 种类 | 不灌 |
|---|---|
| 未出台仿真 | 中台三条情景原文、弹性现算、布局推荐条数、用户模拟历史 |
| 新出台预测 | 独立文本解析行、顶替用的解析结果、布局推荐条数 |
| 区域空间 | 全国通用兜底行、布局推荐条数 |
| 235 | 不灌进 `gapfill_policy_sim_forecast`。不把 `M_POLICY_SIMULATE` 写入多维评估行 |
| 236 | 不在本叶重建该表。请求不插入、不更新、不删除 |

`POL-L2-DS12-EST-GAPFILL-L01` 状态 backlog。本页不执行。查询请求不灌数。

## 签收边界

本页不把任务标 done，不改 `task-registry.yaml`，不建库，不灌数，不补 DDL。D4 保持 mock。签收只由 human:淮政玮 做。第 5.4、5.5 节改成库.表、并与 SIM 第 9 节和说明书 11.2 的表名一致之前，本页维持不同意会签。

## 第二轮（2026-11-05 返工后）

- 角色：`agent:data-agent`
- 日期：2026-11-05
- 对象：`POL-L2-DS12-EST-ARCH` 第 5.4、5.5、9 节
- 对照：`POL-L2-DS12-SIM-ARCH` 第 9 节；`科技政策跟踪-系统详细设计说明书.md` 第 11.2 节「推演 · 仿真 235–242」
- 监管：`human:淮政玮`
- 本轮只核第一轮点名的两句库.表。第一轮原文保留。

### 结论

同意会签。

第一轮不同意，只因第 5.4 节写成 `gkxlumenx_gapfill_policy_sim_result`、第 5.5 节写成 `gkxlumenx_gapfill_policy_sim_stakeholder`，库名与表名粘在一起。返工后这两句已是 `gkxlumenx_gapfill.gapfill_policy_sim_result`、`gkxlumenx_gapfill.gapfill_policy_sim_stakeholder`。相对已提交稿，第 5.4、5.5 节正文只在库名与表名之间补了点；行内容、种类、`metric_id` 留空、236 请求不插入均未改。文首状态行补了一句返工说明，不改读法。

### 库表核对

| 口径 | 返工后 | 判定 |
|---|---|---|
| 第 5.4 节 235 读 `gkxlumenx_gapfill.gapfill_policy_sim_result` | 表 `gkxlumenx_gapfill.gapfill_policy_sim_result`（SIM 组，11.2 定名），种类为多维评估 | 已拆开 |
| 第 5.5 节 236 读 `gkxlumenx_gapfill.gapfill_policy_sim_stakeholder` | 表 `gkxlumenx_gapfill.gapfill_policy_sim_stakeholder`（SIM 组），种类为参与意见 | 已拆开 |
| 与 SIM 第 9 节一致 | 两张表，都在库 `gkxlumenx_gapfill`：`gapfill_policy_sim_result`、`gapfill_policy_sim_stakeholder`。235 多维评估行灌进第一张，236 参与意见行灌进第二张。灌数仍由 `POL-L2-DS12-SIM-GAPFILL-L01` 执行 | 一致 |
| 与说明书 11.2 表名一致 | 「推演 · 仿真 235–242」新建表为 `gapfill_policy_sim_result`、`gapfill_policy_sim_stakeholder`，灌数单 `POL-L2-DS12-SIM-GAPFILL-L01`。要灌列含多维评估与参与意见 | 一致 |
| 本叶仍不重建这两张 | 第 5.4 节：表与字段由 `POL-L2-DS12-SIM-DATA` 定，灌数由 `POL-L2-DS12-SIM-GAPFILL-L01` 执行，本叶只定读法。第 9 节：235、236 不在 `gapfill_policy_sim_forecast`，灌数与字段由 SIM 组两单负责。第 7 节：不建第二套 | 一致 |
| 读法未改 | 235 仍是一行一个维度（经济、社会、环境、创新）的得分与说明，`metric_id` 留空。236 仍是一行一条已灌意见，请求不插入、不更新、不删除 | 一致 |

### 签收边界

本页不把任务标 done，不改任务状态，不建库，不灌数，不补 DDL。D4 保持 mock。签收只由 human:淮政玮 做。

# POL-L2-DS11-PLAN-DATA-SIGNOFF-DATA · 政策分析评价 · 推荐方案报告交互展示 · 数据落点数据会签

- 角色：`agent:data-agent`
- 日期：2026-11-03
- 对象：`POL-L2-DS11-PLAN-DATA`
- 监管：`human:淮政玮`
- 对照：`POL-L2-DS11-PLAN-ARCH`（注册表 done）第 3、9 节；`POL-L2-DS11-PLAN-API` 第 1–8 节；`POL-L2-DS11-READ-DATA` 第 4 节（壳表边界）；灌数单 `POL-L2-DS11-PLAN-GAPFILL-L01`（backlog，只转述注册描述）
- 范围：SRS 227–231 的表结构、`row_kind` 闭集、列清单、D16 行级列、表边界、灌数单 DoD 对账

## 结论

**同意会签**

本页只核对 DATA 分册与已签收架构第 9 节、API 分册读法、灌数单 DoD 是否对得上。不改 DATA 分册，不改架构稿，不改 API 分册，不改注册表里的灌数单，不建库，不写 SQL，不灌数。

## 核对

### 表与 `row_kind` 闭集

| 项 | DATA 分册写法 | 对数据判定 |
|---|---|---|
| 唯一新表 | 库 `gkxlumenx_gapfill`，表 `gapfill_policy_eval_scheme`。不拆四张，231 不另建报告行、文件表 | 一致。架构第 9 节同；库前缀符合 D16（不进 ODS/DWD/ADS/供应方库） |
| `row_kind` 四值闭集 | `方案对照`（227，供 231 取正文）、`参数模拟`（228）、`路径与风险`（229）、`互动意见`（230，供 231 取点评）。没有第五个值，231 不写入 `row_kind` | 一致。与架构第 9 节种类表逐行对应；与 API 第 2 节「表只有四种行种类」相同。231 不占行种类即无文件表需求，成立——导出从当次读到的方案对照行与意见行生成（第 7 节），无文件列可落 |
| 与壳表不混 | 与 `gapfill_policy_eval_shell` 的 `entry_kind` 不是同一列，互不写入 | 一致。壳表 `entry_kind` 只有解读/多媒体，只服务 224、225（READ-DATA 第 4 节），与本表四值无交集 |

### 列清单支撑 API 读法

| 行种类 | API 分册要读 | DATA 分册列 | 判定 |
|---|---|---|---|
| 方案对照 | 名称、一句说明、若干对照维度和数值、优劣结论、实施建议 | `scheme_name`（NOT NULL，方案间不重名）、`summary_text`、`compare_items`（组数不固定）、`verdict_text`、`advice_text` | 一致。五列齐备；其余三种行 `scheme_name` 必须对得上方案对照行，参照完整性口径明确 |
| 参数模拟 | 参数档、评估结果、一句趋势、一条归档说明 | `param_band`（同方案不重复）、`eval_result`、`trend_text`、`archive_text` | 一致。四列齐备；按 `scheme_name`+`param_band` 拣行可执行 |
| 路径与风险 | 节点名称、时间进度、一句节点说明、风险标题、一句风险说明、顺序 | `node_name`、`schedule_text`、`node_text`、`risk_title`、`risk_text`、`sort_no`（同方案不重复，升序读） | 一致。六列齐备；一个方案多行由粒度定义支撑，顺序不靠时间原文排 |
| 互动意见 | 主体、分类、意见正文、时间 | `actor_name`、`opinion_kind`（`评价`/`评论`/`建议` 三值闭集）、`opinion_text`、`opinion_at`（与 `generated_at` 分列） | 一致。四列齐备；`opinion_at` 单列避免与灌数时间混淆 |

### D16 行级列

| 项 | DATA 分册写法 | 对数据判定 |
|---|---|---|
| `metric_id` | 路径与风险行固定 `M_POLICY_DS_11_POLICY_EVAL_015`；其余三种留空，**写 NULL，不写空字符串** | 一致。NULL 语义明确，避免空串被当成有效值参与展示或过滤；与 METRIC/API 两册「留空」口径相同；不新注册 |
| `gap_item` 四值 | 按 `row_kind` 固定 `227 多方案对比展示`/`228 方案参数自定义模拟`/`229 实施路径与风险辅助`/`230 互动意见收集与专家参与`；231 无行无 `gap_item` | 一致。NOT NULL；序号+叶子名与架构「`gap_item` 写序号和叶子名」逐字对应 |
| `fill_method` | 固定 `manual`，因此不设 `fill_model` | 一致。NOT NULL；模型名只在 `llm` 方法时要求，本表不适用 |
| `gapfill_batch_id` | NOT NULL，由灌数单填写 | 一致。批次可追溯 |
| `generated_at` | NOT NULL，行写入时间，由灌数单填写 | 一致。与 `opinion_at` 分列，语义不混 |
| `is_mock` | NOT NULL，每行必须为 1；D4 仍是 mock | 一致。避免缺项行被读成已上线；`GDF-POLICY-MOCK-GATE-L01` 仍 blocked，本单不写成已解开 |

### 表边界不重叠

| 项 | DATA 分册写法 | 对数据判定 |
|---|---|---|
| 壳表只服务 224/225 | 第 1、2、9 节：`gapfill_policy_eval_shell` 是解读二级的壳表，列不混用 | 一致。READ-DATA 第 4 节壳表只管 224 解读行、225 多媒体行 |
| 模板表只服务 222 | 第 9 节：219–222 不读本表；模板读法留给可视化 | 一致。API 第 1 节「留给谁」表同 |
| 方案表只服务 227–231 | 第 9 节跨项表逐项点名：`evaluation/counts`、219–222、223–226、241、`report/jobs`、`panorama/jobs`、`gapfill_policy_audience_feedback` 均不读不写 | 一致。与 API 第 9 节「明确不做」、METRIC 第 7 节「点名不挂」三面互锁 |
| 推演隔离 | `ads.policy_simulate` 行不复制进本表；`M_POLICY_SIMULATE` 不写入 228 行 | 一致。灌数「不灌」列同句 |
| 库边界 | 只写 `gkxlumenx_gapfill`，不写 `gkxlumenx_ods`/`dwd`/`ads`，不写供应方库；生产配置不读 `gkxlumenx_gapfill`，仅功能验收链路的 element 读 | 一致。D16 合规；不产生 `calc_batch_id`，不回流 ADS |

### 灌数单对账

| 项 | DATA 分册写法 | 对数据判定 |
|---|---|---|
| DoD 对得上 | 第 8 节：灌数单 DoD 已指向这一张表——建 `gapfill_policy_eval_scheme`，独立脚本灌方案对照、参数模拟结果、路径节点与风险、专家意见条目；本分册把「专家意见条目」收成 `row_kind=互动意见`，不另建意见表 | 一致。四种类与本表 `row_kind` 四值一一对应；「不灌导出文件、不改 D4、不新造 metric_id」与第 2、7 节同 |
| 最少灌数内容 | 方案对照至少两方案；参数模拟每方案至少一行；路径与风险每方案若干节点（`metric_id` 用 015）；互动意见若干条（分类闭集）；231 不灌 | 一致。与架构第 9 节灌数表逐行同；「不灌」列（布局建议条数、演示分、demo 三条常量原文、省级力度情景、弹性现算、采纳插行、推演曲线、子图、改期、页面新意见、210 问卷、PDF/Word/Excel/对象存储/核增研报）齐备 |
| 状态与归属 | backlog；执行人 data-agent，监管 human:淮政玮；依赖本单与 ARCH；本单不认领不执行 | 一致。本会签不改其注册字段 |
| 查询不灌数、空表返回空 | 第 1、8 节：查询只读表，查询请求不灌数，没有行返回空，不写示例行 | 一致。无「顺手灌数」暗道 |

### 观察（不构成不同意）

| 观察 | 说明 |
|---|---|
| `compare_items` 结构化上限 | 维度名+数值以文本共存于 `compare_items`，组数不固定。雷达/KPI 解析在 element 侧按约定格式读。这是 D18 下的务实做法，不改判定；若后续契约单（`BE-POL-CONTRACT-01`）冻结其内嵌格式，以契约单为准 |
| 灌数单 DoD 措辞「专家意见条目」 | DoD 原文写「专家意见条目」，本分册收成 `row_kind=互动意见`。语义一致（意见行含主体/分类/正文/时间），执行时按本分册第 2、6 节列定义落行即可，无需改 DoD |

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。

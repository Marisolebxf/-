# POL-L2-DS11-PLAN-SIGNOFF-DATA · 政策分析评价 · 推荐方案报告交互展示 · 数据会签

- 角色：`agent:data-agent`
- 日期：2026-11-03
- 对象：`POL-L2-DS11-PLAN-ARCH`
- 监管：`human:淮政玮`
- 对照：`POL-L2-DS11-PLAN-ARCH` 第 8、9 节；`科技政策跟踪-系统详细设计说明书.md` 第 11.2 节「评价 · 方案 227–231」
- 范围：SRS 227–231
- 结论：**同意会签**

本页只核对架构第 9 节的数据落点是否与说明书第 11.2 节方案行一致，以及灌数单能否确定该灌哪些行。下游 DATA 分册还没有，本页不定字段级 DDL。不改架构稿，不改任务状态，不建库，不灌数。

## 库表核对

| 口径 | 架构第 9 节 | 判定 |
|---|---|---|
| 只一张表 `gkxlumenx_gapfill.gapfill_policy_eval_scheme`。不拆成四张。不写 ODS、DWD、ADS、供应方库 | 五叶共用这一张。库只允许 `gkxlumenx_gapfill` | 一致 |
| 种类只有四种：方案对照、参数模拟、路径与风险、互动意见 | 227 方案对照；228 参数模拟；229 路径与风险；230 互动意见。说明书「专家意见条目」落在互动意见行 | 一致 |
| 231 不另建表、不另占种类、不灌文件 | 第 2 节请求种类写作「方案报告」，读取的仍是方案对照行和互动意见行。第 5.5、9 节写明不另建报告行、不灌 | 一致。灌数以第 9 节为准，不另灌方案报告行 |
| 路径与风险行 `metric_id` 用已有 `M_POLICY_DS_11_POLICY_EVAL_015`。其余三种留空。不新造 `metric_id`。`fill_method=manual`。D4 保持 mock | 第 5.3、9 节。不改 D4，不把读到的行写成已上线 | 一致 |
| 不把推演情景灌进这张表 | 不灌省级力度情景。`M_POLICY_SIMULATE` 不写入这些行。`ads.policy_simulate` 继续只服务推演键 | 一致 |
| 字段级 DDL 留给 `POL-L2-DS11-PLAN-DATA`。查询不灌数。请求不插入新意见、不插入采纳行 | 第 9 节。`POL-L2-DS11-PLAN-GAPFILL-L01` 写明 backlog，本叶不执行 | 一致 |

## 不灌清单

| 种类 | 不灌 |
|---|---|
| 方案对照 | 布局建议条数、演示分、demo 三条常量的原文 |
| 参数模拟 | 省级力度情景、弹性公式现算、采纳时新插入的行 |
| 路径与风险 | 推演曲线、子图、用户改期。不把 `M_POLICY_SIMULATE` 写入行 |
| 互动意见 | 页面当场提交的新意见、序号 210 的 `gapfill_policy_audience_feedback` |
| 231 | 不灌。不写 PDF、Word、Excel、对象存储、核增研报。不另建文件表 |

`POL-L2-DS11-PLAN-GAPFILL-L01` 未执行。本页不执行。查询请求不灌数。

## 签收边界

本页不把任务标 done，不改 `task-registry.yaml`，不建库，不灌数。字段级 DDL 留给 `POL-L2-DS11-PLAN-DATA`，本页不补一套 DDL。D4 保持 mock。签收仍由 human:淮政玮 做。

## 第二轮（2026-11-03 返工后）

### 结论

同意会签。

返工后第 9 节仍只一张 `gkxlumenx_gapfill.gapfill_policy_eval_scheme`，四种类。231 不灌文件。路径与风险行 `metric_id` 用已有 `M_POLICY_DS_11_POLICY_EVAL_015`，其余三种留空。`fill_method=manual`。D4 保持 mock。不新造 `metric_id`。

### 库表核对

| 口径 | 架构第 9 节 | 判定 |
|---|---|---|
| 只一张表 `gkxlumenx_gapfill.gapfill_policy_eval_scheme`。不拆成四张。不写 ODS、DWD、ADS、供应方库 | 库只允许 `gkxlumenx_gapfill`。表名以 `gapfill_` 开头 | 一致 |
| 种类只有四种：方案对照、参数模拟、路径与风险、互动意见 | 227、228、229、230 各一种。231 不单独占种类 | 一致 |
| 231 不灌文件 | 导出读方案对照行和意见行。不灌 PDF、Word、Excel、对象存储、核增研报 | 一致 |
| 路径与风险行 `metric_id` 用已有 `M_POLICY_DS_11_POLICY_EVAL_015`。其余三种留空。不新造 `metric_id` | 第 9 节写明。不新注册 | 一致 |
| `fill_method=manual`。D4 保持 mock | 第 9 节。不把读到的行写成已上线 | 一致 |
| 灌数单 `POL-L2-DS11-PLAN-GAPFILL-L01` 未执行 | 状态 backlog。本叶不执行。查询请求不灌数 | 一致 |
| 字段级 DDL 留给 `POL-L2-DS11-PLAN-DATA`。本页不补 DDL | 第 9 节 | 一致 |

### 不灌清单

| 种类 | 不灌 |
|---|---|
| 方案对照 | 布局建议条数、演示分、demo 三条常量的原文 |
| 参数模拟 | 省级力度情景、弹性公式现算、采纳时新插入的行。不把 `M_POLICY_SIMULATE` 写入行 |
| 路径与风险 | 推演曲线、子图、用户改期 |
| 互动意见 | 页面当场提交的新意见、序号 210 的 `gapfill_policy_audience_feedback` |
| 231 | 不灌。不写 PDF、Word、Excel、对象存储、核增研报。不另建文件表 |

`POL-L2-DS11-PLAN-GAPFILL-L01` 未执行。本页不执行。查询请求不灌数。

### 签收边界

本页不把任务标 done，不改 `task-registry.yaml`，不建库，不灌数，不补 DDL。D4 保持 mock。签收仍由 human:淮政玮 做。

# POL-L2-DS11-PLAN-DATA-SIGNOFF-ARCH · 政策分析评价 · 推荐方案报告交互展示 · 数据分册架构会签

- 角色：`agent:arch-agent`（主会话代执，子智能体连续限流后由 coordinator 会话按架构基准直核）
- 日期：2026-11-03
- 对象：`POL-L2-DS11-PLAN-DATA`
- 监管：`human:淮政玮`
- 对照：已签收 `POL-L2-DS11-PLAN-ARCH` 第 9 节（注册表 done）。本页只核分册是否落在架构基准内，不重新设计，不改分册，不改架构稿，不改 task-registry，不改代码
- 范围：SRS 序号 227–231 的数据落点

## 结论

同意会签

分册唯一新建 `gkxlumenx_gapfill.gapfill_policy_eval_scheme`，`row_kind` 四值闭集与架构第 9 节一致，231 不占种类不建文件表，不拆四张表，D16 行级列齐备，表边界与 VIZ（模板表）、READ（壳表）互不抢，只定列不建库不灌数。

## 核对

| 项 | 分册写法 | 对架构判定 |
|---|---|---|
| 单表四种类不拆表 | 第 2 节：库 `gkxlumenx_gapfill`，表 `gapfill_policy_eval_scheme`，`row_kind` 只有方案对照/参数模拟/路径与风险/互动意见四值，「没有第五个值。231 不写入 `row_kind`」；第 1 节「与 227 同一张表，不另建」三处 | 一致。与架构第 9 节「不拆成四张表」、第 6 节种类分发一致 |
| 231 不建文件表 | 第 7 节：不另建种类、不另建行、不另建文件表，不设文件地址/对象键/文件字节列，导出从已读行生成 | 一致。与架构「231 从行生成、不灌文件」一致，不写对象存储 |
| D16 行级列齐备 | 第 2 节列清单含 `metric_id`（路径行固定 015、其余 NULL 不写空字符串）、`gap_item` 四值固定、`fill_method` 固定 `manual`、`gapfill_batch_id`、`generated_at`、外加 `is_mock=1` | 一致。与架构第 9 节 D16 五列一字不差，`is_mock` 强化不把缺项行读成已上线 |
| 表边界不与他二级重叠 | 第 9 节跨项边界表：`gapfill_policy_eval_shell` 只服务 224/225、`gapfill_policy_eval_template` 只服务 222、方案表只服务 227–231；不读 `ads.policy_simulate`、`gapfill_policy_audience_feedback` 不并入 | 一致。与架构第 6 节及 VIZ/READ 两稿的分界一致，三表互不串读 |
| 库边界 | 第 1、2 节：库只允许 `gkxlumenx_gapfill`，表名 `gapfill_` 前缀，不写 ODS/DWD/ADS、供应方库 | 一致。符合 D16 与架构第 9 节库边界 |
| 只定列不执行 | 第 2 节「列清单不是可执行 SQL」，建表与灌数归 `POL-L2-DS11-PLAN-GAPFILL-L01`，查询请求不灌数，空表返回空 | 一致。与架构「查询不灌数、无行则空」一致 |
| 读链正确 | 第 1 节：227–229 走 `jobs`、230–231 走 `shells`，element 按种类只读，Java 不生成/现算/插入 | 一致。与架构第 2、5 节链路一致 |
| 拣行条件 | 第 2 节末：只用 `row_kind`、`scheme_name`，参数模拟再加 `param_band`；条件对不上不返回，不插入行凑数 | 一致。与架构按方案拣行的分发语义一致 |

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。同意会签不是签收。

# POL-L2-DS11-PLAN-SIGNOFF-DATA · 政策分析评价 · 推荐方案报告交互展示 · 数据会签

- 角色：`agent:data-agent`
- 日期：2026-11-03
- 对象：`sdd/l2/POL-L2-DS11-PLAN-ARCH.md`
- 监管：`human:淮政玮`
- 对照：该稿第 5、9 节；指标 `M_POLICY_DS_11_POLICY_EVAL_015`（已注册，D4=`mock`）
- 范围：SRS 227–231
- 结论：**同意**

本页只核对数据落点。不改架构正文，不改任务状态，不建表，不灌数，不定字段级 DDL。

五叶只读 `gkxlumenx_gapfill.gapfill_policy_eval_scheme`。不进 ODS、DWD、ADS，不写供应方库。不拆表。读取方都是 `gkxlumen-element`，经 `gkxlumen-display` 原样返回。灌数方是 `POL-L2-DS11-PLAN-GAPFILL-L01`（`data-agent`），本页不执行。查询不灌数。

## 表、读取方、灌数方

| 序号 | 表中的行 | 读取方 | 灌数方 |
|---|---|---|---|
| 227 | 方案对照行 | `POST /display/v1/policy/evaluation/jobs`，种类为方案对照。少于两行则对比空 | 该灌数单灌方案对照行 |
| 228 | 参数模拟行 | 同一条 `jobs`，按方案和参数档只读。对不上则空 | 该灌数单灌参数模拟行。采纳不插入新行 |
| 229 | 路径与风险行。`metric_id` 只用已有 `M_POLICY_DS_11_POLICY_EVAL_015` | 同一条 `jobs` 只读。不读政策子图 | 该灌数单灌路径与风险行。不新造 `metric_id`，不改 D4 |
| 230 | 互动意见行 | `GET /display/v1/policy/evaluation/shells` 只读。无行则列表空 | 该灌数单可灌已定的意见行。意见请求不插入、不更新、不删除 |
| 231 | 不另建行、不另建文件表。导出读方案对照行和意见行 | 同一条 `shells`，从当次读到的行生成。无方案对照行则导出空 | 不灌导出文件。不写 PDF、Word、Excel，不写对象存储 |

227、228、230 没有已挂指标的行，`metric_id` 留空，不新注册。D4 保持 mock。字段级 DDL 留给 `POL-L2-DS11-PLAN-DATA`。签收仍由 human:淮政玮 做。

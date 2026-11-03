# POL-L2-DS10-CMP-GAPFILL-L01 · 政策重点比对缺项表灌数

ponytail: full

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | 任务已在 `in_progress`。本会话不改 task-registry，不把任务标成 done |
| 说明 | 用户授权提交并推送 origin/dev。备注不写联调通过 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只建并灌四张缺项表。未用 YAGNI 跳过 D16 追溯列，也未改 D4、未改 `jobs/execute` |

## 范围与实现

真源是 `sdd/l2/POL-L2-DS10-CMP-DATA.md` 第 3、4、5、7 节，以及 `sdd/l2/POL-L2-DS10-CMP-ARCH.md` 第 9 节。范围是 213、214 的申报条件与申报材料、215 的实施部门、217。216 和 218 不进本单。

库目标是 `gkxlumenx_gapfill`。四张表都已建上并灌入：

| 表 | 序号 | 拣行键 | 库内行数 |
|---|---|---|---|
| `gapfill_policy_version_diff` | 213 | `policy_id` + 两个发布时间 | 5 |
| `gapfill_policy_detail_compare` | 214 | `policy_id` | 4 |
| `gapfill_policy_impl_dept` | 215 | 区域、实施部门、方面 | 6 |
| `gapfill_policy_benchmark_report` | 217 | 对标对象、已勾字段 | 6 |

不建 `gapfill_policy_benchmark_viz`。

213 的时点列是 `publish_date_a`、`publish_date_b`，没有 `version_no`。`publish_date_a` 是该政策在 `gkxlumenx_dwd.policy_base_info` 上的发布日。2026-11-03 只读核对：这张正文 40000 行，没有一个 `policy_id` 有两个不同的 `publish_date`。成对的另一个日子取自另一条正文上已经存在的发布日，不是用 `publish_year` 推出来的。同一政策、同一对日期可以有多行。政策 `18363390` 的 `2022-04-06` 与 `2022-06-15` 有新增、修改、删除三行。日期次序对调仍是同一对。对不上的日期返回 0 行。本表不提供可选时点。

214 四条政策各一行：`18363390`、`18407696`、`18358888`、`18359216`。只放申报条件和申报材料。

215 的方面只有 `项目类别`、`技术类别`。件数在 `item_count`，`metric_id` 留空，不挂 `M_POLICY_TOTAL_COUNT`，也不新造部门指标。`item_count` 等于清单标题的行数。实施部门是手工名，不是发布机构去重。清单标题里没有 `policy_id`，也没有政策正文。

217 的对标对象是 `北京市`、`广东省`。字段只有 `政策类型`、`支持力度`、`覆盖范围`。差异、优劣、借鉴和正文都在行里。没有 PDF、Word、对象键。`gkxlumenx_ads.policy_intensity` 当时无行，所以对象没有从力度表读出；没有海外城市。

每行 `is_mock=1`，`metric_id` 为空，`fill_method=manual`，`gapfill_batch_id=POL-L2-DS10-CMP-GAPFILL-L01`，`generated_at=2026-11-03 15:00:00`。`gap_item` 分别是 `213 政策新旧对比`、`214 政策详情对比`、`215 部门政策对比`、`217 对标报告生成与导出`。

脚本重跑会先删这四张表的行再插入。语句只使用库名 `gkxlumenx_gapfill`。

## 偏离

| 偏离 | 理由 | as-built |
|------|------|----------|
| 注册表 DoD 仍写 `gapfill_policy_benchmark_viz`，并写「不灌部门件数」 | 用户说明该旧句作废。已签收 DATA 与 ARCH 第 9 节不建可视化表，215 要灌件数但不是新指标 | 未建可视化表。`item_count` 在部门表，`metric_id` 为空 |
| 不设 `fill_model` | DATA 写明 `fill_method` 固定 `manual`，因此不设该列 | 四张表都没有 `fill_model`。有 `is_mock` |
| 213 的第二个发布日不是该政策正文上的第二个版本 | 产线每个 `policy_id` 只有一个 `publish_date`。本表不补一个新日子，也不编版本号 | 两个日子都是正文里已有的 `publish_date`。界面若只拿出一个发布日，对比仍为空 |
| 217 的对标对象不是力度表里的 `scope_name` | `gkxlumenx_ads.policy_intensity` 无行。探测时看过 demo 力度表的省级名称，没有把 demo 分数写入缺项表 | 对象用产线正文里已有的北京市、广东省 |

## 产物清单

- `repos/lumen-algo-py/scripts/seed_gapfill_policy_cmp.py`
- `repos/lumen-algo-py/scripts/mysql/gapfill_policy_cmp.sql`
- 本 handoff

未改 `/internal/policy/jobs/execute`。未改 Java。未改 D4。未新造 `metric_id`。

## 验收证据

四张表已建在 `gkxlumenx_gapfill` 并灌入。information_schema 里这四个表名只出现在这个库。`gapfill_policy_benchmark_viz` 的表计数是 0。

| 项 | 结果 |
|---|---|
| 实例 | `10.50.11.76:3306` |
| 账号 | `gkxlumenx` |
| 目标库 | `gkxlumenx_gapfill` |
| 行数 | version 5、detail 4、impl_dept 6、benchmark_report 6 |
| `is_mock=1` 且 `metric_id` 为空 | 四张表全部行 |
| 213 成对命中 | `18363390` + `2022-04-06`/`2022-06-15` 返回新增、修改、删除 |
| 213 对不上 | 同一政策换成 `2021-11-17` 返回 0 |
| 215 | 北京市 / 北京市科学技术委员会 / 项目类别，`item_count=2`，标题两行 |
| 217 | 北京市、广东省各有政策类型、支持力度、覆盖范围，正文在行里 |

命令（在 `repos/lumen-algo-py`，2026-11-03。口令只放进进程环境变量，未打印、未写入脚本和本文）：

- `python scripts/seed_gapfill_policy_cmp.py --check` → 退出码 0。输出行数 5、4、6、6
- `python scripts/seed_gapfill_policy_cmp.py --apply` → 退出码 0。输出 `{"mode":"apply","connected":true,"host":"10.50.11.76","port":3306,"db":"gkxlumenx_gapfill","rows":{"gapfill_policy_version_diff":5,"gapfill_policy_detail_compare":4,"gapfill_policy_impl_dept":6,"gapfill_policy_benchmark_report":6}}`

自检在 `--check` 里，不连库。它锁住：两个发布日不分次序；同一对可以有三种变更；对不上的日期为空；一条政策一条详情；部门三键唯一且件数等于标题行数；报告只接受三个字段；SQL 不出现可视化表、版本号列、`fill_model`、ODS、DWD、ADS、demo 库名、`M_POLICY_`、PDF、Word 文件后缀和 `jobs/execute`。

## 架构合规自检

- ✅ 调用链：本单只灌库，不改 Java，不改展示，不在接口里写死 mock
- ✅ 灌数在 Python：`lumen-algo-py/scripts/seed_gapfill_policy_cmp.py`
- ✅ 图谱：未写 nGQL
- ✅ D16：只写 `gkxlumenx_gapfill` 下 `gapfill_` 四表。行上有 `metric_id`（空）、`gap_item`、`fill_method`、`gapfill_batch_id`、`generated_at`、`is_mock=1`。DATA 规定不设 `fill_model`
- ✅ 未写 ODS、DWD、ADS、供应方库。正文只读，用来核对发布日
- ✅ 未改 D4，未动 `GDF-POLICY-MOCK-GATE-L01`
- ✅ 未新造 `metric_id`。件数不是指标
- ✅ 未建 `gapfill_policy_benchmark_viz`。未灌 PDF、Word
- ✅ 未改 `/internal/policy/jobs/execute`

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 12000 |
| model_used | grok-4.7 |
| actual_cost | 0.06 |
| cost_warn | green |

本会话不改 task-registry，上表不回写注册表。数字是估算。

## CI/CD

- 分支：`lumen-algo-py` 的 `dev` 已推送。`gkx-orchestration` 只提交本 handoff
- 库：`10.50.11.76:3306` 的 `gkxlumenx_gapfill`。四张表已灌入
- pipeline：本单不跟发布
- 部署：无
- Python commit：`40d84e2274de8ec7fe34556db4082487f61b6d35` `feat(policy): 灌重点比对四张缺项表 [agent:data-agent]`

## 未做的事

- 未把任务标成 done，状态仍是 `in_progress`
- 未改查询接口。读表是 `gkxlumen-element` 的事
- 未跑 `polan.eval.intensity.run`，未写 `policy_intensity`
- 未改架构稿、DATA、说明书、注册表

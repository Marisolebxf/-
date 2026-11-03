# POL-L2-DS10-SENT-MOCK-210 · 政策受众反馈缺项表

ponytail: full

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch`。总控已认领并置 in_progress。本会话不改 task-registry，不标 done |
| 说明 | 脚本在 `lumen-algo-py`，沿用 `seed_gapfill_policy_qry.py` 的连库方式。编排仓只交本 handoff |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只为本表加灌数脚本和 SQL。未加依赖。未用 YAGNI 跳过 D16 列，也未改 D4、未改读表代码 |

## 范围与实现

列以 `sdd/l2/POL-L2-DS10-SENT-DATA.md` 第 5 节为准。

库 `gkxlumenx_gapfill`，表 `gapfill_policy_audience_feedback`。一行一条意见。渠道只允许 `问卷`、`在线评价`、`意见征集`。没有评分或没有关联政策时写入 NULL，不用 0 占位。不建问卷表、题目表、答卷表。不写 ODS、DWD、ADS、供应方库。查询请求不执行本脚本。

| 列 | 约束 | 本次 |
|---|---|---|
| `subject_name` | varchar(256)，非空 | 6 个反馈主体，名称写在行上 |
| `channel` | varchar(32)，三者之一 | 每个渠道 2 行 |
| `opinion_text` | text，非空 | 缺项演示正文 |
| `score` | decimal(10,2)，可空 | 3 行有分（4.50、3.00、5.00），3 行 NULL |
| `policy_id` | text，可空，无外键 | 3 行有文本编号，3 行 NULL |
| `feedback_at` | datetime，非空 | 意见上的时间，与 `generated_at` 分开 |
| `is_mock` | tinyint，非空 | 每行 1 |
| `metric_id` | varchar(64)，可空 | 全 NULL |
| `gap_item` | varchar(128) | 固定 `210 政策受众反馈收集` |
| `fill_method` | varchar(16) | 固定 `manual`。不设 `fill_model` |
| `gapfill_batch_id` | varchar(64) | `POL-L2-DS10-SENT-MOCK-210` |
| `generated_at` | datetime | `2026-11-03 14:30:00` |

引擎主键是自增 `id`。重跑先删本表再插入。

## 偏离

| 偏离 | 理由 | as-built |
|------|------|----------|
| 第一次 `--apply` 没有写入 | 2026-11-03 已连上 `10.50.11.76:3306`，账号 `gkxlumenx`。当时 errno 1044，`SHOW DATABASES` 看不到名称带 gap 的库 | 没有插入。SQL 文件已在 |
| 随后同一条 `--apply` 写入成功 | 同一账号之后 `SHOW GRANTS` 含 `GRANT ALL PRIVILEGES ON gkxlumenx_gapfill.*`，`CREATE DATABASE IF NOT EXISTS` 与 `USE` 都通过 | 表已建，SELECT 为 6 行 |

## 产物清单

- `repos/lumen-algo-py/scripts/seed_gapfill_policy_audience.py`
- `repos/lumen-algo-py/scripts/mysql/gapfill_policy_audience.sql`
- 本 handoff

未改 Java。未改 `job.py`。未改查询接口。

## 验收证据

表已建上，行已灌入。下面的行数来自灌完之后的 SELECT，不是 `--check` 的预期数。

| 项 | 结果 |
|---|---|
| 目标库 | `gkxlumenx_gapfill` |
| 表 | `gapfill_policy_audience_feedback` 已存在 |
| `SELECT COUNT(*)` | 6 |
| 标记行 | 6。条件是 `is_mock=1 AND metric_id IS NULL AND gap_item='210 政策受众反馈收集' AND fill_method='manual'` |
| 渠道 | 问卷 2、在线评价 2、意见征集 2 |
| 空评分 / 空关联政策 | 3 / 3 |

命令（在 `repos/lumen-algo-py`，2026-11-03）：

- `python scripts/seed_gapfill_policy_audience.py --check` → 退出码 0。输出 `{"mode":"check","ok":true,"db":"gkxlumenx_gapfill","rows":{"gapfill_policy_audience_feedback":6}}`
- 第一次 `python scripts/seed_gapfill_policy_audience.py --apply` → 退出码 2。输出 `{"mode":"apply","connected":true,"tables_ready":false,"errno":1044,"reason":"Access denied for user 'gkxlumenx'@'%' to database 'gkxlumenx_gapfill'","gap_db_visible":false}`
- 再次 `python scripts/seed_gapfill_policy_audience.py --apply` → 退出码 0。输出 `{"mode":"apply","connected":true,"db":"gkxlumenx_gapfill","rows":{"gapfill_policy_audience_feedback":6},"marked":6,"by_channel":{"问卷":2,"在线评价":2,"意见征集":2},"null_score":3,"null_policy":3}`
- 独立 `SELECT COUNT(*) FROM gkxlumenx_gapfill.gapfill_policy_audience_feedback` → 6
- 独立按 `is_mock`、空 `metric_id`、`gap_item`、`fill_method` 计数 → 6

自检锁住：三渠道各 2 条；评分有 NULL 且有分的都大于 0；`metric_id` 全空；`fill_method` 全是 `manual`；SQL 不出现 `fill_model`，也不出现 ODS、DWD、ADS 库名。

## 架构合规自检

- ✅ 调用链：本单只灌库，不改 Java，不改展示，不在接口里写死 mock
- ✅ 灌数在 Python：`lumen-algo-py/scripts/seed_gapfill_policy_audience.py`
- ✅ 图谱：未写 nGQL
- ✅ D16：只写 `gkxlumenx_gapfill.gapfill_policy_audience_feedback`。行上有 `metric_id`（空）、`gap_item`、`fill_method=manual`、`gapfill_batch_id`、`generated_at`，以及 `is_mock=1`。不设 `fill_model`
- ✅ 未写 ODS、DWD、ADS、供应方库
- ✅ 未改 D4，未新注册 `metric_id`
- ✅ 未灌假问卷、假通知、假邮件。未新建对象存储桶
- ✅ 未改架构稿、说明书、WBS、task-registry
- ✅ 未把本单标成 done

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 12000 |
| model_used | grok-4.7 |
| actual_cost | 0.05 |
| cost_warn | green |

## CI/CD

- 分支：`lumen-algo-py` 的 `dev`
- commit：`51efa4cb75742d51ce55b7c6292578791e1a08b6`
- pipeline：本单不跟发布
- 部署：无
- 库：`gkxlumenx_gapfill.gapfill_policy_audience_feedback` 已灌入，SELECT 6 行

## 涉及文件

- `scripts/seed_gapfill_policy_audience.py`
- `scripts/mysql/gapfill_policy_audience.sql`

## 未做的事

- 未改 task-registry，未把任务标成 done
- 未改 Java，未改 `job.py`，未改查询接口
- 未改 D4
- 未写 ODS、DWD、ADS、供应方库

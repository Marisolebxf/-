# POL-L2-DS10-SENT-MOCK-211 · 政策效果评估报告缺项表

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
| 说明 | 只为本表加灌数脚本和 SQL。未加依赖。未新建对象存储桶。未用 YAGNI 跳过 D16 列，也未改 D4、未改读表代码 |

## 范围与实现

列以 `sdd/l2/POL-L2-DS10-SENT-DATA.md` 第 6 节为准。

库 `gkxlumenx_gapfill`，表 `gapfill_policy_assessment_report`。一行一份报告。范围、达成度、社会影响、问题、建议、报告正文都在这一行。达成度是报告里的表述，不写入 ADS，不新造指标。正文不落文件，不落对象存储。不读 `policy_effect`。不灌对标报告，不灌核增研报。不写 ODS、DWD、ADS、供应方库。查询请求不执行本脚本。

| 列 | 约束 | 本次 |
|---|---|---|
| `scope_text` | text，非空 | 2 份不同范围：广东省科技企业研发支持；深圳市高层次人才安居与青年科研岗位 |
| `achievement_text` | text，非空 | 达成度表述 |
| `social_impact` | text，非空 | 社会影响 |
| `problem_text` | text，非空 | 问题 |
| `suggestion_text` | text，非空 | 建议 |
| `report_body` | text，非空 | 报告正文，只在本列 |
| `is_mock` | tinyint，非空 | 每行 1 |
| `metric_id` | varchar(64)，可空 | 全 NULL。不挂 `M_POLICY_DEEP_168_1` |
| `gap_item` | varchar(128) | 固定 `211 政策效果评估报告` |
| `fill_method` | varchar(16) | 固定 `manual`。不设 `fill_model` |
| `gapfill_batch_id` | varchar(64) | `POL-L2-DS10-SENT-MOCK-211` |
| `generated_at` | datetime | `2026-11-03 14:30:00` |

引擎主键是自增 `id`。重跑先删本表再插入。

## 偏离

| 偏离 | 理由 | as-built |
|------|------|----------|
| 第一次 `--apply` 没有写入 | 与 210 同一次连接。errno 1044，当时看不到 gap 库 | 没有插入 |
| 随后同一条 `--apply` 写入成功 | 同一账号已能使用 `gkxlumenx_gapfill` | 表已建，SELECT 为 2 行 |

## 产物清单

- `repos/lumen-algo-py/scripts/seed_gapfill_policy_assessment.py`
- `repos/lumen-algo-py/scripts/mysql/gapfill_policy_assessment.sql`
- 本 handoff

未改 Java。未改 `job.py`。未改查询接口。未新建桶。

## 验收证据

表已建上，行已灌入。下面的行数来自灌完之后的 SELECT。

| 项 | 结果 |
|---|---|
| 目标库 | `gkxlumenx_gapfill` |
| 表 | `gapfill_policy_assessment_report` 已存在 |
| `SELECT COUNT(*)` | 2 |
| 标记行 | 2。条件是 `is_mock=1 AND metric_id IS NULL AND gap_item='211 政策效果评估报告' AND fill_method='manual'`，且 `report_body` 有正文 |

命令（在 `repos/lumen-algo-py`，2026-11-03）：

- `python scripts/seed_gapfill_policy_assessment.py --check` → 退出码 0。输出 `{"mode":"check","ok":true,"db":"gkxlumenx_gapfill","rows":{"gapfill_policy_assessment_report":2}}`
- 第一次 `python scripts/seed_gapfill_policy_assessment.py --apply` → 退出码 2。输出 `{"mode":"apply","connected":true,"tables_ready":false,"errno":1044,"reason":"Access denied for user 'gkxlumenx'@'%' to database 'gkxlumenx_gapfill'","gap_db_visible":false}`
- 再次 `python scripts/seed_gapfill_policy_assessment.py --apply` → 退出码 0。输出 `{"mode":"apply","connected":true,"db":"gkxlumenx_gapfill","rows":{"gapfill_policy_assessment_report":2},"marked":2}`
- 独立 `SELECT COUNT(*) FROM gkxlumenx_gapfill.gapfill_policy_assessment_report` → 2
- 独立按 `is_mock`、空 `metric_id`、`gap_item`、`fill_method` 与正文长度计数 → 2

自检锁住：两份范围不同；六个文本列都有内容；`metric_id` 全空；`fill_method` 全是 `manual`；SQL 不出现 `fill_model`、`policy_effect`、对标报告、研报、对象存储，也不出现 ODS、DWD、ADS 库名。

## 架构合规自检

- ✅ 调用链：本单只灌库，不改 Java，不改展示，不在接口里写死 mock
- ✅ 灌数在 Python：`lumen-algo-py/scripts/seed_gapfill_policy_assessment.py`
- ✅ 图谱：未写 nGQL
- ✅ D14：未新建对象存储桶，未写桶名和对象键
- ✅ D16：只写 `gkxlumenx_gapfill.gapfill_policy_assessment_report`。行上有 `metric_id`（空）、`gap_item`、`fill_method=manual`、`gapfill_batch_id`、`generated_at`，以及 `is_mock=1`。不设 `fill_model`
- ✅ 未写 ODS、DWD、ADS、供应方库
- ✅ 未改 D4，未新注册 `metric_id`，未挂 `M_POLICY_DEEP_168_1`
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
- 库：`gkxlumenx_gapfill.gapfill_policy_assessment_report` 已灌入，SELECT 2 行

## 涉及文件

- `scripts/seed_gapfill_policy_assessment.py`
- `scripts/mysql/gapfill_policy_assessment.sql`

## 未做的事

- 未改 task-registry，未把任务标成 done
- 未改 Java，未改 `job.py`，未改查询接口
- 未新建对象存储桶
- 未改 D4
- 未写 ODS、DWD、ADS、供应方库

# POL-L2-PC3-PC4-ADS-L01 · 政策对比研报 ADS 表

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | 开工前已是 `in_progress`，本会话未再认领、未调 task-registry |
| 说明 | 只建正式库表。不做 WRITE / API / 前端，不改说明书。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只加一张可重复执行的建表 SQL 和一个读文件断言。未跳过 D19 字符集。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无 |
| 图 diff | 本叶未改图 |
| 会签态 | 无 |
| 说明 | 只新增 ADS 结果表 |

## 修改内容

- 表名：`ads_policy_compare_report`
- 库：`gkxlumenx_ads`（正式库，不是 demo 库）
- 字符集：`utf8mb4`
- 排序规则：`utf8mb4_general_ci`
- 语句：`CREATE TABLE IF NOT EXISTS`，可重复执行
- 一行装下一次对比和一次研报
- 列：`run_id`（主键），`fingerprint`（索引 `idx_ads_policy_compare_report_fingerprint`），`policy_ids`，`titles`，`dims`，`weight`，`threshold`，`time_window`，`region`，`level`，`status`（`进行中` \| `已完成` \| `失败`），`scores_json`，`findings_json`，`chart_json`，`summary_text`，`conclusions_json`，`report_json`，`error_text`，`created_at`
- JSON 列使用 `JSON`；`summary_text` 为 `LONGTEXT`；`error_text` 为 `TEXT`
- 未建 `gapfill_policy_*`，未写 ODS、DWD、供应方库
- 是否已在库里建成：**没有落库**。本仓 `conf/settings.yaml` 的连接是 `localhost:3306`、用户 `gkxlumenx`，口令为空；环境变量 `LUMEN_ALGO_MYSQL_HOST` / `LUMEN_ALGO_MYSQL_PASSWORD` 未设置。连接被拒绝：`OperationalError (2003) WinError 10061`。未改用 SSH。

## 测试结果

- 命令：`python -m pytest tests/test_ads_policy_compare_report_ddl.py -q`
- 工作目录：`repos/lumen-algo-py`
- 结果：`1 passed in 0.09s`
- 断言：SQL 含 `ads_policy_compare_report`、含 `utf8mb4_general_ci`、不含 `gapfill_`

## 遗留风险

- 表尚未出现在 `gkxlumenx_ads`。有可用 MySQL 连接后执行 `scripts/mysql/ads_policy_compare_report.sql` 即可，语句可重复执行。
- `CREATE TABLE IF NOT EXISTS` 不会改已存在且结构不同的同名表。

## CI/CD（必填）

- 分支：`lumen-algo-py` `origin/dev`；`gkx-orchestration` `origin/dev`
- commit：`lumen-algo-py` `b7a2317f167288e4e8e920b1e9fdfe518060bab4`；编排仓为本 handoff 所在提交
- pipeline URL / ID：本会话未查
- 部署 namespace / 镜像 tag：无。本变更是 SQL 文件，不随镜像自动建表
- K8s rollout：未部署
- dev 测试 URL / 命令与结果：见测试结果。落库未执行

## 可观测性（建议）

- 无服务代码改动，无 trace

## 涉及文件

- `repos/lumen-algo-py/scripts/mysql/ads_policy_compare_report.sql`
- `repos/lumen-algo-py/tests/test_ads_policy_compare_report_ddl.py`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-PC3-PC4-ADS-L01.md`

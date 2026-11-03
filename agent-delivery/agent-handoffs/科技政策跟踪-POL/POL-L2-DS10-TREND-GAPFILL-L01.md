# POL-L2-DS10-TREND-GAPFILL-L01 · 政策动向四张缺项表

ponytail: full

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch`。总控已认领并置 in_progress。本会话不改 task-registry |
| 说明 | 用户授权在 `lumen-algo-py` 提交并推送 `origin/dev`。编排仓不提交 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只建这四张缺项表的脚本和 SQL。连库方式复用 `seed_gapfill_policy_qry.py`。未加依赖。未用 YAGNI 跳过 D16 列，也未改 D4、未改读表代码 |

## 范围与实现

真源是 `sdd/l2/POL-L2-DS10-TREND-ARCH.md` 第 7.3 节，列以 `sdd/l2/POL-L2-DS10-TREND-DATA.md` 第 5 节为准。

库目标是 `gkxlumenx_gapfill`。四张表，引擎主键只加与业务无关的自增 `id`。不设 `fill_model`。

| 表 | gap_item | 业务列 | 脚本准备的行 |
|---|---|---|---|
| `gapfill_policy_trend_hotspot` | `205 热点识别` | `domain_name` varchar(64)、`hotspot_name` varchar(128)、`brief` varchar(512)，均非空 | 6。科创发展、人才引进、资金扶持各 2 条 |
| `gapfill_policy_trend_impact` | `205 政策影响评估` | `domain_name` varchar(64)、`impact_object` varchar(128)、`impact_direction` varchar(64)、`conclusion` varchar(512)，均非空 | 3。三个领域各 1 条 |
| `gapfill_policy_trend_report` | `205 深度分析报告` | `title` varchar(256)、`domain_name` varchar(64)、`body` text，均非空 | 3。三个领域各 1 份，正文在 `body` |
| `gapfill_policy_theme_dist` | `206 主题分布` | `theme_name` varchar(128) 非空、`item_count` int 非空、`stat_year` smallint 可空 | 5。主题名为研发费用加计扣除、高层次人才安居、创业投资引导、中试平台建设、概念验证支持。前四条年份 2024 或 2025，概念验证支持的年份为 NULL |

每行 D16 列：`metric_id` varchar(128) 留空，`gap_item` varchar(64)，`fill_method` varchar(16) 固定 `manual`，`gapfill_batch_id` varchar(64) 为 `POL-L2-DS10-TREND-GAPFILL-L01`，`generated_at` datetime 为 `2026-11-03 14:10:00`。

不灌热度分、焦点指数、实施效果分、推演情景。不写文件，不写对象存储。主题名不是政策类型桶，也不抄 `policy_type_dist`。脚本重跑会先删这四张表的行再插入。语句只出现库名 `gkxlumenx_gapfill`。

## 偏离

| 偏离 | 理由 | as-built |
|------|------|----------|
| 早先一轮没有写入 | 2026-11-03 早先 `--apply` 连上 `10.50.11.76:3306` 后，账号 `gkxlumenx` 对库 `gkxlumenx_gapfill` 返回 errno 1044。库随后已建好并授权给同一账号。本轮只重跑动向四张表 | `--apply` 退出码 0。库内 hotspot 6、impact 3、report 3、theme 5 |
| 每张表多一列自增 `id` | DATA 第 5.1 节允许引擎要求主键时只加与业务无关的行号 | `bigint AUTO_INCREMENT`，不参与业务 |

## 产物清单

- `repos/lumen-algo-py/scripts/seed_gapfill_policy_trend.py`
- `repos/lumen-algo-py/scripts/mysql/gapfill_policy_trend.sql`
- 本 handoff

未改 Java。未改展示服务。授权后 `--apply` 已在 `gkxlumenx_gapfill` 建表并插入。

## 验收证据

四张表已写入 `gkxlumenx_gapfill`。库内行数与期望一致。

| 项 | 结果 |
|---|---|
| 目标库 | `gkxlumenx_gapfill`（`10.50.11.76:3306`，账号 `gkxlumenx`） |
| `--apply` 退出码 | 0 |
| `gapfill_policy_trend_hotspot` | 6 |
| `gapfill_policy_trend_impact` | 3 |
| `gapfill_policy_trend_report` | 3 |
| `gapfill_policy_theme_dist` | 5 |

命令（在 `repos/lumen-algo-py`，2026-11-03，先 `git pull --no-rebase origin dev`，已是最新）：

- `python scripts/seed_gapfill_policy_trend.py --apply` → 退出码 0。输出 `{"mode":"apply","connected":true,"db":"gkxlumenx_gapfill","rows":{"gapfill_policy_trend_hotspot":6,"gapfill_policy_trend_impact":3,"gapfill_policy_trend_report":3,"gapfill_policy_theme_dist":5}}`

早先同一条命令曾返回 errno 1044。授权后本轮写入成功。没有改用别的账号，没有写 ODS、DWD、ADS、供应方库。脚本未改，没有提交。

自检锁住：三领域热点各 2 条、影响各 1 条、报告各 1 份；主题 5 条且不与科创/行业/园区/招商/人才这五个类型桶同名；`metric_id` 全空；`fill_method` 全是 `manual`；SQL 不出现 `fill_model`、`policy_type`、`gapfill_policy_qry_stat`、打分列名，也不出现 ODS、DWD、ADS 库名。

## 架构合规自检

- ✅ 调用链：本单只准备灌库脚本，不改 Java，不改展示，不在接口里写死 mock
- ✅ 灌数在 Python：`lumen-algo-py/scripts/seed_gapfill_policy_trend.py`
- ✅ 图谱：未写 nGQL
- ✅ D16：语句只针对 `gkxlumenx_gapfill` 下四张 `gapfill_` 表。行上有 `metric_id`（空）、`gap_item`、`fill_method=manual`、`gapfill_batch_id`、`generated_at`。不设 `fill_model`
- ✅ 未写 ODS、DWD、ADS、供应方库
- ✅ 未改 D4，未新注册 `metric_id`
- ✅ 未灌假订阅。未动 203 入库、时序、地域热力。未把点灌进 `gapfill_policy_qry_stat`
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
- commit：`3827118c542213a688c0e9917c1a256fc93a1475`
- pipeline：本单不跟发布
- 部署：无
- 库：`gkxlumenx_gapfill`。`--apply` 退出码 0。hotspot 6、impact 3、report 3、theme 5

## 涉及文件

- `scripts/seed_gapfill_policy_trend.py`
- `scripts/mysql/gapfill_policy_trend.sql`

## 未做的事

- 未改 task-registry，未把任务标成 done
- 四张动向表已灌入 `gkxlumenx_gapfill`（hotspot 6、impact 3、report 3、theme 5）
- 未改 Java，未改展示服务，未在控制器或 Python 响应里写死 mock
- 未灌订阅，未动 203 入库、时序、地域热力
- 未改 D4
- 未写 ODS、DWD、ADS、供应方库

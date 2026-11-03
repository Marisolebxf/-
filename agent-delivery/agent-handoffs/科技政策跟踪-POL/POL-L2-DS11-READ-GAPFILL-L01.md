# POL-L2-DS11-READ-GAPFILL-L01 · 政策分析评价 · 解读 · 缺项表灌 mock

ponytail: full

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 任务已是 ready。本会话用 MCP 认领并改为 in_progress。锁定 24 小时。不改 task-registry.yaml，不提交该文件 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只建并灌 `gapfill_policy_eval_shell`。连库方式复用 `scripts/seed_gapfill_policy_trend.py`。未加依赖。未用 YAGNI 跳过 D16 列，也未改 D4、未改查询代码 |

## 范围与实现

真源是 `sdd/l2/POL-L2-DS11-READ-DATA.md` 第 4 节和第 6 节，粒度以 `sdd/l2/POL-L2-DS11-READ-ARCH.md` 第 8 节为准。旧 DoD 的三张缺项表按已签收架构收窄。

库 `gkxlumenx_gapfill`。只建一张表 `gapfill_policy_eval_shell`。224 解读行和 225 多媒体行共用这一张。引擎主键是自增 `id`。`fill_method` 固定 `manual`，因此不设 `fill_model`。

| 列 | 类型 | 空 | 本单写入 |
|---|---|---|---|
| `id` | bigint | 否 | 自增 |
| `entry_kind` | varchar(16) | 否 | `解读` 或 `多媒体` |
| `topic_or_metric` | varchar(256) | 是 | 解读行必填。多媒体行空 |
| `conclusion_text` | text | 是 | 解读行一句结论。多媒体行空 |
| `suggestion_text` | text | 是 | 解读行一句应用建议。多媒体行空 |
| `title` | varchar(256) | 是 | 多媒体行标题。解读行空 |
| `caption` | text | 是 | 多媒体行一句说明。解读行空 |
| `is_mock` | tinyint | 否 | 每行 1 |
| `metric_id` | varchar(64) | 是 | 留空。没有已挂指标，不新造 |
| `gap_item` | varchar(128) | 否 | 解读行 `224 分主题分指标互动解读`。多媒体行 `225 多媒体辅助解读` |
| `fill_method` | varchar(16) | 否 | `manual` |
| `gapfill_batch_id` | varchar(64) | 否 | `POL-L2-DS11-READ-GAPFILL-L01` |
| `generated_at` | datetime | 否 | `2026-11-03 16:20:00` |

行数：解读 3，多媒体 2，合计 5。解读专题是科创发展、人才引进、资金扶持。多媒体标题是科创发展条款说明、人才引进条款说明。不灌视频、动画、图形文件、PDF、模板。序号 222 不写入。不抄 223 焦点说明，不抄 226 摘要。

脚本重跑会先删这张表的行再插入。语句只出现库名 `gkxlumenx_gapfill`。查询脚本不负责插入。本单不改 `job.py`、`focus.py`、`gap.py`、`parse.py`。

## 偏离

| 偏离 | 理由 | as-built |
|------|------|----------|
| 旧 DoD 要建三张缺项表并灌焦点说明、摘要结论、模板 | 2026-11-03 已签收架构和第 4、6 节把范围收成一张壳表 | 只建并灌 `gapfill_policy_eval_shell`。未建 `gapfill_policy_eval_focus`、`gapfill_policy_eval_summary` |

## 产物清单

- `repos/lumen-algo-py/scripts/seed_gapfill_policy_eval_shell.py`
- `repos/lumen-algo-py/scripts/mysql/gapfill_policy_eval_shell.sql`
- 本 handoff

未改 Java。未改展示服务。`--apply` 已在 `gkxlumenx_gapfill` 建表并插入。

## 验收证据

表已写入 `gkxlumenx_gapfill`。库内行数与期望一致。`information_schema` 里同库只有 `gapfill_policy_eval_shell`，没有 `gapfill_policy_eval_focus`，也没有 `gapfill_policy_eval_summary`。

| 项 | 结果 |
|---|---|
| 目标库 | `gkxlumenx_gapfill`（`10.50.11.76:3306`，账号 `gkxlumenx`） |
| 表 | `gapfill_policy_eval_shell` |
| `--apply` 退出码 | 0 |
| 合计 | 5 |
| `解读` | 3。`gap_item`=`224 分主题分指标互动解读`，`fill_method`=`manual`，`metric_id` 全空，`is_mock` 全是 1 |
| `多媒体` | 2。`gap_item`=`225 多媒体辅助解读`，`fill_method`=`manual`，`metric_id` 全空，`is_mock` 全是 1 |

命令（在 `repos/lumen-algo-py`，2026-11-03）：

- `python scripts/seed_gapfill_policy_eval_shell.py --check` → 退出码 0。输出 `{"mode":"check","ok":true,"db":"gkxlumenx_gapfill","rows":{"gapfill_policy_eval_shell":5,"解读":3,"多媒体":2}}`
- `python scripts/seed_gapfill_policy_eval_shell.py --apply` → 退出码 0。输出 `{"mode":"apply","connected":true,"db":"gkxlumenx_gapfill","table":"gapfill_policy_eval_shell","rows":5,"kinds":{"解读":3,"多媒体":2}}`

随后在 `gkxlumenx_gapfill` 按 `entry_kind`、`gap_item`、`fill_method` 分组计数：解读 3、多媒体 2。两组的 `metric_id` 空行数和 `is_mock=1` 行数都等于组内行数。没有写 ODS、DWD、ADS、供应方库。

自检锁住：解读行有专题名、一句结论、一句应用建议，标题和说明为空；多媒体行有标题和一句说明，专题名、结论、建议为空；`metric_id` 全空；`fill_method` 全是 `manual`；`is_mock` 全是 1；SQL 只有这一张 `CREATE TABLE`；SQL 不出现焦点表名、摘要表名、`fill_model`、序号 222、已有政策指标号，也不出现 ODS、DWD、ADS 库名。

## 架构合规自检

- ✅ 算法只在 Python：灌数是 `lumen-algo-py` 脚本。Java 未建表、未灌数
- ✅ 调用链：本单不改接口。查询不插入。接口不直接返回写死的 mock
- ✅ 图谱：未写 nGQL，未连 Nebula
- ✅ 可观测：本单不新增服务，不改埋点
- ✅ D8：本单无页面
- ✅ D9：不改 D4，不新造 `metric_id`。行上 `metric_id` 留空，`is_mock=1`
- ✅ D10：本单无交互
- ✅ D12：只改 `lumen-algo-py`，未调用 demo 服务
- ✅ D14：不写对象存储，不灌视频、动画、图形文件、PDF
- ✅ D16：只在 `gkxlumenx_gapfill` 建 `gapfill_policy_eval_shell`。行上有 `metric_id`、`gap_item`、`fill_method=manual`、`gapfill_batch_id`、`generated_at`。方法不是 `llm`，不设 `fill_model`
- ✅ D17：未改合规算法闭包，未改 `focus.py`、`gap.py`、`parse.py`、`job.py`
- ✅ D18：mock 行写入缺项表。本单不让接口直接返回写死的 mock
- ✅ 未写 ODS、DWD、ADS、供应方库
- ✅ 未建 `gapfill_policy_eval_focus`、`gapfill_policy_eval_summary`
- ✅ 序号 222 不写入。不灌模板
- ✅ 未改架构稿、说明书、WBS、task-registry.yaml
- ✅ 未把本单标成 done

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 8000 |
| model_used | grok-4.7 |
| actual_cost | 0.04 |
| cost_warn | green |
| user_story | US-DS-POL-05 |

## CI/CD

- 分支：`lumen-algo-py` 的 `dev`
- commit：`ef33dce0230b44fde2a4d2d1c0d98ee38e34da8b`。这是本单两份文件的提交，已在 `origin/dev`。本地先有同内容的 `43e3b3e765dd2272b0abe0ef4eabd417d769e767`，当时 `dev` 已被别人推过，不能快进
- 推送：`origin/dev` 现为 `2d912496b74750e3402b9d5867ea48d19e7e23c6`。这是一次 `merge origin/dev`，只为接上后到的远端提交。没有手改 `job.py`
- pipeline：本单不跟发布
- 部署：无
- 库：`gkxlumenx_gapfill`。`--apply` 退出码 0。`gapfill_policy_eval_shell` 5 行（解读 3、多媒体 2）

## 涉及文件

- `scripts/seed_gapfill_policy_eval_shell.py`
- `scripts/mysql/gapfill_policy_eval_shell.sql`

## 未做的事

- 未改 task-registry.yaml，未把任务标成 done
- `gapfill_policy_eval_shell` 已灌入 `gkxlumenx_gapfill`（解读 3、多媒体 2）
- 未改 Java，未改展示服务，未在查询路径里插入行
- 未改 D4，未新造 `metric_id`
- 未建焦点缺项表和摘要缺项表

# POL-L2-DS10-QRY-GAPFILL-L01 · 多维检索缺项表灌数

ponytail: full

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch`。任务已在 in_progress。本会话不改 task-registry，不把任务标成 done |
| 说明 | 用户授权提交并推送 origin/dev。备注不写联调通过 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只尝试灌多维检索 197–200 与 199 的三张缺项表。未用 YAGNI 跳过 D16 追溯列，也未改 D4、未改读表代码 |

## 范围与实现

真源是 `sdd/l2/POL-L2-DS10-QRY-ARCH.md` 第 7 节与文首签收补充，以及说明书第 11.1 节。范围只有多维检索 197、198、199、200。

库目标是 `gkxlumenx_gapfill`。三张表：

| 表 | 要灌的内容 | 脚本准备的行 | 库内行数 |
|---|---|---|---|
| `gapfill_policy_qry_doc` | 检索目录与正文 | 6 | 没有。SELECT 被拒绝 |
| `gapfill_policy_qry_stat` | 197/198/200 已挂统计 | 20 | 没有。SELECT 被拒绝 |
| `gapfill_policy_qry_rank` | 相关性、时效性、重要性的名次 | 18 | 没有。SELECT 被拒绝 |

统计行用已有指标号，不新造 `metric_id`：

- `M_POLICY_TOTAL_COUNT` 1 行，件数 6
- `M_POLICY_LEVEL_DIST` 5 行。编码按派单包 17：4 国家级 2、3 省级 1、2 市级 3、1 区县级 0、0 未标注 0。五档合计等于总数
- `M_POLICY_NATIONAL_DIST` 2 行：北京市 2、广东省 4
- `M_POLICY_SZ_DIST` 1 行：`district_name` 为深圳市，件数 3。不按区拆
- `M_POLICY_TIMESERIES` 5 行：`period_type=Y`，发布年 2021–2025，件数合计 6。不写增长率、连续性
- `M_POLICY_TYPE_DIST` 5 行：科创 2、行业 1、园区 1、招商 1、人才 1。只在缺项表
- `M_POLICY_VALIDITY_RATE` 1 行：`stat_rate=66.6700`（百分数）。口径未指定，手工演示

上面是脚本里准备插入的行，不是库内行。本轮没有插入成功。

每行带 `gap_item`、`fill_method=manual`、`fill_model` 空、`gapfill_batch_id=POL-L2-DS10-QRY-GAPFILL-L01`、`generated_at=2026-11-03 12:00:00`。目录和名次不是指标，`metric_id` 留空。

名次表列是 `policy_id`、`rank_dim`、`rank_no`。没有打分列。时效性按发布日期从新到旧；相关性和重要性是手工次序。六条目录在每个维度里各出现一次。

脚本重跑会先删这三张表的行再插入。语句只出现库名 `gkxlumenx_gapfill`。

## 偏离

| 偏离 | 理由 | as-built |
|------|------|----------|
| 三张表没有建上，行没有灌上 | 2026-11-03 本机 TCP 已通。`--apply` 连上 `10.50.11.76:3306`，账号 `gkxlumenx`@`%`。`CREATE DATABASE` / `USE gkxlumenx_gapfill` 返回 errno 1044。`SHOW DATABASES` 列出 23 个库，名称里没有 gap。全局权限只有 `USAGE ON *.*`，没有 `gkxlumenx_gapfill` 的授权，也没有建库权限。失败后 rollback，没有插入 | DDL+INSERT 仍在脚本里。授权后仍用同一条 `--apply` |
| 数据落点单写过「199 不落新表」 | 该句早于签收补充。本单按 ARCH 第 7.1 节和说明书第 11.1 节准备名次表 | 只准备 `gapfill_policy_qry_rank`，不改 DATA 文档 |
| 目录行、名次行 `metric_id` 为空 | 这两类没有已登记指标号。不新造 id | 统计行只用上面七个已有 id |
| 有效率是手工百分数 | DATA 写明口径未指定，第一批不写正式库有效率列 | 缺项表一列 `stat_rate`，不写正式库 |
| 级别分布有两行件数 0 | 五档合计要等于总数。这是缺项表里的分档，不是接口在无行时造 0 | 区县级、未标注为 0 |
| 类型用科创/行业/园区/招商/人才 | 沿展示窗口里 QPOL-01 的五个类别做演示 | 不改 QPOL-01，不写 `policy_type_dist` |

## 产物清单

- `repos/lumen-algo-py/scripts/seed_gapfill_policy_qry.py`（本轮未改）
- `repos/lumen-algo-py/scripts/mysql/gapfill_policy_qry.sql`（本轮未改）
- `repos/lumen-algo-py/vendor/entan-py/api/policy_routes.py`（先前另一次 commit，本轮未改）
- `repos/lumen-algo-py/tests/test_policy_job.py`（先前另一次 commit，本轮未改）
- 本 handoff

未改 Java。未改展示服务。`--apply` 已执行，没有建表，没有插入。

## 验收证据

三张表没有建上。库内行数没有。脚本准备插入、尚未入库的行数仍是 doc 6、stat 20、rank 18。

| 项 | 结果 |
|---|---|
| 实例 | `10.50.11.76:3306` |
| 账号 | `gkxlumenx`@`%`（已连上） |
| 目标库 | `gkxlumenx_gapfill`（无权使用，未写入） |
| 表 | `gapfill_policy_qry_doc`、`gapfill_policy_qry_stat`、`gapfill_policy_qry_rank` 都未建上 |
| 库内行数 | 没有。三次 `COUNT(*)` 都是 errno 1142，没有数字 |
| 期望行数 | doc 6、stat 20、rank 18（只在脚本校验里，不是库内行数） |

命令（在 `repos/lumen-algo-py`，2026-11-03。口令只放进进程环境变量，未打印、未写入本文）：

- `python scripts/seed_gapfill_policy_qry.py --apply` → 退出码 2。输出 `{"mode":"apply","connected":true,"tables_ready":false,"errno":1044,"reason":"Access denied for user 'gkxlumenx'@'%' to database 'gkxlumenx_gapfill'"}`
- `SHOW DATABASES` → 23 个库，没有名称含 gap 的库。`SHOW GRANTS` 对 `*.*` 只有 `USAGE`，没有 `gkxlumenx_gapfill`
- `SELECT COUNT(*) FROM gkxlumenx_gapfill.gapfill_policy_qry_doc` → errno 1142，`SELECT command denied to user 'gkxlumenx'@'10.253.202.239' for table 'gapfill_policy_qry_doc'`
- `SELECT COUNT(*) FROM gkxlumenx_gapfill.gapfill_policy_qry_stat` → errno 1142，同一账号对该表 `SELECT` 被拒绝
- `SELECT COUNT(*) FROM gkxlumenx_gapfill.gapfill_policy_qry_rank` → errno 1142，同一账号对该表 `SELECT` 被拒绝

没有改用别的账号。没有写 ODS、DWD、ADS、demo。更早一轮 `--apply` 曾是 errno 2003 超时；本轮网络已通，卡在库权限。

自检锁住的是脚本，不是库内行：七个已有指标号齐全；级别、全国、时序、类型的件数合计都是 6；深圳全市 3；名次三个维度各是 1 到 6 的全排列；时效性与发布日期从新到旧一致；SQL 不出现打分列名，也不出现 ODS、DWD、ADS、demo 库名。

## 架构合规自检

- ✅ 调用链：本单只跑已有灌库脚本，不改 Java，不改展示，不在接口里写死 mock
- ✅ 灌数在 Python：`lumen-algo-py/scripts/seed_gapfill_policy_qry.py`，未把算法写进 Java
- ✅ 图谱：未写 nGQL，未改图库
- ✅ D16：语句只针对 `gkxlumenx_gapfill` 下 `gapfill_` 前缀三表；行上有 `gap_item`、`fill_method`、`fill_model`、`gapfill_batch_id`、`generated_at`。本轮语句没有执行成功
- ✅ 未写 ODS、DWD、ADS、供应方库。类型分布和有效率不进正式统计表
- ✅ 未读 demo 库，未把 20000 行 demo 拷进正式库
- ✅ 未改 D4，未动 `GDF-POLICY-MOCK-GATE-L01`
- ✅ 名次表设计只有名次，没有打分列。库上这张表没有建成
- ✅ 未灌检索历史、收藏、导出文件
- ✅ 未新造 `metric_id`。统计行只用已挂的七个指标号

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 8000 |
| model_used | cursor-grok-4.5 |
| actual_cost | 0.04 |
| cost_warn | green |

本会话不改 task-registry，上表不回写注册表。

## CI/CD

- 分支：`gkx-orchestration` 的 `dev`（只提交本 handoff）。`lumen-algo-py` 本轮无新 commit
- 库：已连上 MySQL。库 `gkxlumenx_gapfill` 拒绝访问。三张表未建，行数没有
- pipeline：本单不跟发布
- 部署：无
- commit：本文件推 `origin/dev` 后即该 commit

## 提交

`lumen-algo-py` `dev` 上先前已有、本轮未再推：

- `e1a6246920f1248e331d0b3e0a0a09f29f51fb4d` `feat(policy): 灌多维检索缺项表 [agent:data-agent]`（只含两个脚本）
- `46ef9d41075659edba36cb8d066bb3f5eeea0f16` `feat(policy): 排序只读缺项名次表 [agent:api-agent]`（只含 `policy_routes.py` 与 `tests/test_policy_job.py`）

本仓只提交这份 handoff。

## 未做的事

- 未改 task-registry，未把任务标成 done
- 未把三张表建进 `gkxlumenx_gapfill`，未灌行
- 未改 Java，未改 `policy_routes.py`，未改灌数脚本
- 未灌 201 检索历史与收藏、202 导出文件
- 未改 D4，未动 `GDF-POLICY-MOCK-GATE-L01`
- 未写 ODS、DWD、ADS、供应方库，未读 demo 库
- 未动 `POL-L2-DS10-SENT-GAPFILL-L01` 和 `POL-L2-DS10-TREND-GAPFILL-L01`

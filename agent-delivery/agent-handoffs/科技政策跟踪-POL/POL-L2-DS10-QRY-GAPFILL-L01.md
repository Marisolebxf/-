# POL-L2-DS10-QRY-GAPFILL-L01 · 多维检索缺项表灌数

ponytail: full

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | 父会话已认领并置为 in_progress。本会话不改 task-registry |
| 说明 | 不标 done，不 commit，不 push |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只灌多维检索 197–200 与 199 的三张缺项表。未用 YAGNI 跳过 D16 追溯列，也未改 D4、未改读表代码 |

## 范围与实现

真源是 `sdd/l2/POL-L2-DS10-QRY-ARCH.md` 第 7 节与文首签收补充，以及说明书第 11.1 节。范围只有多维检索 197、198、199、200。

库目标是 `gkxlumenx_gapfill`。三张表：

| 表 | 要灌的内容 | 脚本准备的行 |
|---|---|---|
| `gapfill_policy_qry_doc` | 检索目录与正文：`policy_id`、`title`、`content`、`policy_type`、`publish_organization`、`province`、`city`、`publish_date` | 6 |
| `gapfill_policy_qry_stat` | 197/198/200 已挂统计：总数、级别、全国、深圳、时序、类型、有效率 | 20 |
| `gapfill_policy_qry_rank` | 相关性 `relevance`、时效性 `timeliness`、重要性 `importance` 的名次 | 18 |

统计行用已有指标号，不新造 `metric_id`：

- `M_POLICY_TOTAL_COUNT` 1 行，件数 6
- `M_POLICY_LEVEL_DIST` 5 行。编码按派单包 17：4 国家级 2、3 省级 1、2 市级 3、1 区县级 0、0 未标注 0。五档合计等于总数
- `M_POLICY_NATIONAL_DIST` 2 行：北京市 2、广东省 4
- `M_POLICY_SZ_DIST` 1 行：`district_name` 为深圳市，件数 3。不按区拆
- `M_POLICY_TIMESERIES` 5 行：`period_type=Y`，发布年 2021–2025，件数合计 6。不写增长率、连续性
- `M_POLICY_TYPE_DIST` 5 行：科创 2、行业 1、园区 1、招商 1、人才 1。只在缺项表
- `M_POLICY_VALIDITY_RATE` 1 行：`stat_rate=66.6700`（百分数）。口径未指定，手工演示

每行带 `gap_item`、`fill_method=manual`、`fill_model` 空、`gapfill_batch_id=POL-L2-DS10-QRY-GAPFILL-L01`、`generated_at=2026-11-03 12:00:00`。目录和名次不是指标，`metric_id` 留空。

名次表列是 `policy_id`、`rank_dim`、`rank_no`。没有打分列。时效性按发布日期从新到旧；相关性和重要性是手工次序。六条目录在每个维度里各出现一次。

脚本重跑会先删这三张表的行再插入。语句只出现库名 `gkxlumenx_gapfill`。

## 偏离

| 偏离 | 理由 | as-built |
|------|------|----------|
| 表没有在库上建出来 | 本机连 `10.50.11.76:3306` 超时，errno 2003。SSH 执行器未连上，没有改从别的机器灌 | DDL+INSERT 已落盘，可重复执行。连上后 `python scripts/seed_gapfill_policy_qry.py --apply` |
| 数据落点单写过「199 不落新表」 | 该句早于签收补充。本单按 ARCH 第 7.1 节和说明书第 11.1 节准备名次表 | 只准备 `gapfill_policy_qry_rank`，不改 DATA 文档 |
| 目录行、名次行 `metric_id` 为空 | 这两类没有已登记指标号。不新造 id | 统计行只用上面七个已有 id |
| 有效率是手工百分数 | DATA 写明口径未指定，第一批不写正式库有效率列 | 缺项表一列 `stat_rate`，不写正式库 |
| 级别分布有两行件数 0 | 五档合计要等于总数。这是缺项表里的分档，不是接口在无行时造 0 | 区县级、未标注为 0 |
| 类型用科创/行业/园区/招商/人才 | 沿展示窗口里 QPOL-01 的五个类别做演示 | 不改 QPOL-01，不写 `policy_type_dist` |

## 产物清单

- `repos/lumen-algo-py/scripts/seed_gapfill_policy_qry.py`
- `repos/lumen-algo-py/scripts/mysql/gapfill_policy_qry.sql`
- 本 handoff

未改 `vendor/entan-py/api/policy_routes.py`。未改 Java。未改展示服务。

## 验收证据

库没有连上，表没有建上，库内行数没有。

| 项 | 结果 |
|---|---|
| 目标库 | `gkxlumenx_gapfill` |
| 本机连接 | `10.50.11.76:3306`，errno 2003，`Can't connect to MySQL server on '10.50.11.76' (timed out)` |
| 表 | 未建上 |
| 库内行数 | 没有。下面是脚本准备插入、尚未入库的行数 |
| `gapfill_policy_qry_doc` | 6 |
| `gapfill_policy_qry_stat` | 20 |
| `gapfill_policy_qry_rank` | 18 |

命令（在 `repos/lumen-algo-py`，退出码以实测为准）：

- `python scripts/seed_gapfill_policy_qry.py --check` → 退出码 0。输出 `{"mode":"check","ok":true,"db":"gkxlumenx_gapfill","rows":{"gapfill_policy_qry_doc":6,"gapfill_policy_qry_stat":20,"gapfill_policy_qry_rank":18}}`
- `python scripts/seed_gapfill_policy_qry.py --apply` → 退出码 2。输出 `{"mode":"apply","connected":false,"errno":2003,"reason":"Can't connect to MySQL server on '10.50.11.76' (timed out)"}`

自检锁住：七个已有指标号齐全；级别、全国、时序、类型的件数合计都是 6；深圳全市 3；名次三个维度各是 1 到 6 的全排列；时效性与发布日期从新到旧一致；SQL 不出现打分列名，也不出现 ODS、DWD、ADS、demo 库名。

## 架构合规自检

- ✅ 调用链：本单只准备灌库脚本，不改 Java，不改展示，不在接口里写死 mock
- ✅ 灌数在 Python：`lumen-algo-py/scripts/seed_gapfill_policy_qry.py`，未把算法写进 Java
- ✅ 图谱：未写 nGQL，未改图库
- ✅ D16：语句只建 `gkxlumenx_gapfill` 下 `gapfill_` 前缀三表；行上有 `gap_item`、`fill_method`、`fill_model`、`gapfill_batch_id`、`generated_at`
- ✅ 未写 ODS、DWD、ADS、供应方库。类型分布和有效率不进正式统计表
- ✅ 未读 demo 库，未把 20000 行 demo 拷进正式库
- ✅ 未改 D4，未动 `GDF-POLICY-MOCK-GATE-L01`
- ✅ 名次表只有名次，没有打分列
- ✅ 未灌检索历史、收藏、导出文件
- ✅ 未新造 `metric_id`。统计行只用已挂的七个指标号

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 8000 |
| model_used | cursor-grok-4.5 |
| actual_cost | 0.04 |
| cost_warn | green |

## CI/CD

- 分支：lumen-algo-py 与 gkx-orchestration 的本地工作区
- commit：无。本单不提交
- pipeline：无
- 部署：无
- 库：未连上，表未建

## 未做的事

- 未改 task-registry，未标 done，未 commit，未 push
- 未改 `vendor/entan-py/api/policy_routes.py`（排序读表由另一个会话做）
- 未改 Java，未改展示服务，未在接口里写死 mock
- 未灌 201 检索历史与收藏、202 导出文件
- 未改 D4，未动 `GDF-POLICY-MOCK-GATE-L01`
- 未写 ODS、DWD、ADS、供应方库，未读 demo 库
- 库未连上，三张表尚未建到 `gkxlumenx_gapfill`

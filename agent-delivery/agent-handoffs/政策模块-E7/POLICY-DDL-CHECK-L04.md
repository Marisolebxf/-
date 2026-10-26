# POLICY-DDL-CHECK-L04 · 核对政策建表文档与现网结构

核对结论：**不一致**。本叶只读，未改库，未建表。

`policy_base_info` 在 `demo_gkxlumenx_dwd` 与 `gkxlumenx_dwd` 上和 `dwd.md` 的 CREATE 对齐。`ads.md` 的 15 张表在两个 ADS 库上都只差表注释。`policy_industry_rel` 在四个库上都只差 `id`、`create_time`、`update_time` 三列注释。两个 DWD 库没有 `policy_text_parse`。

## 任务认领

| 字段 | 值 |
|------|-----|
| 任务 | `POLICY-DDL-CHECK-L04` |
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| status | 开工时已是 `in_progress`。本叶不改 task-registry |
| 说明 | 只核对。不 ALTER，不 DROP，不建表，不 git commit / push |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 只读核对，不写业务代码 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无 |
| 图 diff | 本叶未改存储流图 |
| 会签态 | 不涉及 |

## 范围

对照已提交 CREATE，不对照工作区脏文件。这两份文件相对 `HEAD` 是干净的。

| 文档 | commit | 时间 | 说明 |
|------|--------|------|------|
| `agent-delivery/data/data-design/storage/POLICY/stores/mysql/ads.md` | `dc566597ffb18351a38a189648bb7135df347c12` | 2026-10-26 17:54:53 +0800 | 15 张 CREATE |
| `agent-delivery/data/data-design/storage/POLICY/stores/mysql/dwd.md` | `ac9352f85503d60bdf483a2105859d50a844a172` | 2026-10-26 20:00:51 +0800 | `policy_base_info`、`policy_industry_rel`、`policy_text_parse` |

库：`10.50.11.76:3306`，服务端 MySQL `8.0.39`。客户端 `mysql` 5.7.28，连接字符集 `utf8mb4`。`policy_base_info` 的中文表注释能原样读回，所以空注释是现网事实。

| 文档表 | 对照库 |
|--------|--------|
| ads.md 15 张 | `demo_gkxlumenx_ads`、`gkxlumenx_ads` |
| dwd.md 三张 | `demo_gkxlumenx_dwd`、`gkxlumenx_dwd` |
| `policy_industry_rel` | 再对照两个 ADS 库。结构与 dwd.md 同一份 CREATE，只换库名 |

库名不同不算不一致。`AUTO_INCREMENT` 当前值不比。`EXTRA` 里单独的 `DEFAULT_GENERATED` 视为文档 `DEFAULT CURRENT_TIMESTAMP`（没有 `ON UPDATE`）。数值默认值按 `information_schema` 比较，`SHOW CREATE` 里的 `DEFAULT '0'` 与文档 `DEFAULT 0` 相同。字符列在 CREATE 里没写字符集时，按表默认 `utf8mb4` / `utf8mb4_0900_ai_ci` 比较。

比对维度：列名与顺序、类型、空值、默认值、有没有 `AUTO_INCREMENT`、有没有 `ON UPDATE`、列注释、字符集、排序规则、索引（名、唯一性、列序、BTREE、无前缀）、表注释、表排序规则、引擎。

结构查询时间 `2026-10-26 20:12:34 +08`。随后用 `SHOW CREATE TABLE` 与 `COUNT(*)` 复核。行数不参与结构判定。

## 逐表结论

范围内字符列的排序规则都是 `utf8mb4_0900_ai_ci`。独立查询「字符列排序规则不是这一套」的结果为空。引擎都是 `InnoDB`。demo 与产线的结构差异相同，分叉只在行数。

### ads.md 15 张

两库都在。列、类型、空值、默认值、索引、列注释、字符集、排序规则对齐。索引只有 `PRIMARY (id)`。表注释长度为 0。`SHOW CREATE TABLE demo_gkxlumenx_ads.policy_level_dist` 的表选项止于 `COLLATE=utf8mb4_0900_ai_ci`，没有表 `COMMENT`；列注释与 ads.md 一致。

| 表 | 列数 | 文档表注释 | demo 行数 | 产线行数 | 结论 |
|----|-----:|------------|----------:|----------:|------|
| `policy_level_dist` | 11 | 层级/总数/时效 | 6 | 0 | 现网表注释为空 |
| `policy_type_dist` | 10 | 类型分布 | 14 | 0 | 现网表注释为空 |
| `policy_timeseries` | 10 | 发布时序 | 46 | 0 | 现网表注释为空 |
| `policy_national_dist` | 12 | 分省 | 31 | 0 | 现网表注释为空 |
| `policy_sz_dist` | 12 | 深圳分区 | 5 | 0 | 现网表注释为空 |
| `policy_focus` | 10 | 焦点/机遇/关联 | 20031 | 0 | 现网表注释为空 |
| `policy_intensity` | 12 | 力度/产业覆盖 | 20031 | 0 | 现网表注释为空 |
| `policy_effect` | 12 | 效果/短板/布局 | 155 | 0 | 现网表注释为空 |
| `policy_metric_timeseries` | 11 | 三维/通用时序 | 93 | 0 | 现网表注释为空 |
| `policy_graph_node` | 8 | 点镜像；Nebula 失败时 /v1/policy/graph 可读 | 20001 | 0 | 现网表注释为空 |
| `policy_graph_edge` | 8 | 边镜像 | 0 | 0 | 现网表注释为空 |
| `policy_entity` | 10 | 政策核心实体抽取结果，图谱构建的上游 | 135945 | 0 | 现网表注释为空 |
| `policy_text_parse` | 11 | D1 政策文本解析：摘要 + 结构化要素 + 自动标签 | 20000 | 0 | 现网表注释为空 |
| `policy_match` | 13 | D2 政策匹配推送：主体 ↔ 政策的匹配打分与理由 | 144 | 0 | 现网表注释为空 |
| `policy_simulate` | 14 | D3 政策效果推演仿真：基线 vs 仿真值与曲线 | 36 | 0 | 现网表注释为空 |

### dwd.md 三张，以及关联表的 ADS 镜像

| 表 | 库 | 列数 | 行数 | 结论 |
|----|----|-----:|-----:|------|
| `policy_base_info` | `demo_gkxlumenx_dwd` | 45 | 20000 | 与 dwd.md 一致 |
| `policy_base_info` | `gkxlumenx_dwd` | 45 | 0 | 与 dwd.md 一致 |
| `policy_industry_rel` | `demo_gkxlumenx_dwd` | 7 | 322 | 三列注释为空 |
| `policy_industry_rel` | `gkxlumenx_dwd` | 7 | 0 | 三列注释为空 |
| `policy_industry_rel` | `demo_gkxlumenx_ads` | 7 | 322 | 三列注释为空。ADS 镜像只换库名 |
| `policy_industry_rel` | `gkxlumenx_ads` | 7 | 0 | 三列注释为空。ADS 镜像只换库名 |
| `policy_text_parse` | `demo_gkxlumenx_dwd` | 文档 11 | 无表 | 不一致。本叶不建表 |
| `policy_text_parse` | `gkxlumenx_dwd` | 文档 11 | 无表 | 不一致。本叶不建表 |

`policy_base_info` 索引为 `PRIMARY (id)`、`UNIQUE uk_policy_plane_id (source_plane, policy_id)`。表注释为「政策主表（国内+国际同表）」。`SHOW CREATE TABLE demo_gkxlumenx_dwd.policy_base_info` 与这份 CREATE 对齐。

`policy_industry_rel` 四个库的表注释都在：「政策–产业关联。抽取写入，不回写主表」（18 个字符）。索引为 `PRIMARY (id)`、`KEY idx_policy_industry_rel_pid (policy_id, is_deleted)`、`KEY idx_policy_industry_rel_code (industry_link_code, is_deleted, policy_id)`。`policy_id` 为 `varchar(128) NOT NULL`，排序规则 `utf8mb4_0900_ai_ci`，列注释「对应 policy_base_info.policy_id」。`industry_name`、`industry_link_code` 同样是 `utf8mb4_0900_ai_ci`。`SHOW CREATE TABLE demo_gkxlumenx_dwd.policy_industry_rel` 里 `id`、`create_time`、`update_time` 三行没有 `COMMENT`。四个库的 `information_schema` 相同。

`policy_text_parse` 只存在于两个 ADS 库。两个 DWD 库没有这张基表，也没有同名视图。ADS 上的列结构见上一节，差的是表注释。

## 不一致清单

1. **表注释为空**（demo 与产线 ADS 各一份，共 30 张次）：`policy_level_dist`、`policy_type_dist`、`policy_timeseries`、`policy_national_dist`、`policy_sz_dist`、`policy_focus`、`policy_intensity`、`policy_effect`、`policy_metric_timeseries`、`policy_graph_node`、`policy_graph_edge`、`policy_entity`、`policy_text_parse`、`policy_match`、`policy_simulate`。文档表注释见上表。列级已经对齐。
2. **三列注释为空**（四个库的 `policy_industry_rel`）：`id` 文档为「自增主键」，`create_time` 文档为「写入时间」，`update_time` 文档为「最近一次同步时间」。现网这三列注释长度为 0。其余列、索引、表注释、排序规则已对齐。
3. **DWD 没有 `policy_text_parse`**：`demo_gkxlumenx_dwd` 与 `gkxlumenx_dwd` 都没有。`dwd.md` 有 CREATE。本叶不建表。

`policy_base_info` 不在这份清单里。

## 范围外（不计入不一致）

`demo_gkxlumenx_dwd.policy_base_info_pre_20261026` 仍在，37 列，表排序规则 `utf8mb4_general_ci`。它是旧列备份，不是结构真源。本叶不把它算成文档缺表，也不建议删除。

`gkxlumenx_dwd.policy_base_info_retired_20261026` 仍在，37 列，表排序规则 `utf8mb4_general_ci`。不在本次 CREATE 清单里。本叶不建议删除。

两个 DWD 库另外各有 29 张同名 `policy_*` 业务表（`policy_analysis_report`、`policy_entity`、`policy_favorite` 等）。`dwd.md` 没有这些 CREATE。DWD 的 `policy_entity` 与 ADS 同名表不是本叶的对照对象。两个 ADS 库的 `policy_*` 表就是清单内 16 张（15 张加 `policy_industry_rel`）。

`dwd.md` 在 CREATE 之后有一句正文，写现网 `policy_id` 仍是 `utf8mb4_general_ci`。本次现网该列已是 `utf8mb4_0900_ai_ci`，与 CREATE 一致。这句正文不计入表结构差异。本叶不改 `dwd.md`。

## 问题清单

- ads.md 15 张的表注释还没落到两个 ADS 库。
- `policy_industry_rel` 的 `id`、`create_time`、`update_time` 注释还没落到四个库。
- 两个 DWD 库还没有 `policy_text_parse`。本叶不建表。

## 修改内容

- 新增本 handoff。
- 未 ALTER，未建表，未 DROP，未改 `ads.md` / `dwd.md`，未改 task-registry，未 commit / push。
- 口令未写入本文件。

## 测试结果

- 只读 `information_schema.TABLES`、`COLUMNS`、`STATISTICS`，覆盖上面 38 个库表对照（15×2 + 3×2 + `policy_industry_rel` 的两个 ADS）。
- `SHOW CREATE TABLE` 抽查：`demo_gkxlumenx_ads.policy_level_dist`、`demo_gkxlumenx_dwd.policy_industry_rel`、`demo_gkxlumenx_dwd.policy_base_info`。
- 范围内非 `utf8mb4_0900_ai_ci` 的字符列：0。
- 行数是 `COUNT(*)`。`information_schema.TABLES.TABLE_ROWS` 对主表的估计是 15916，精确行数是 20000，手记采用精确行数。

## 遗留风险

- 表注释和三列注释仍空着。下一个改库叶才能补。本叶不动库。
- DWD 的 `policy_text_parse` 仍缺。本叶不建。
- 两张 37 列历史表仍在。本叶不删除。
- `dwd.md` 里那句 `utf8mb4_general_ci` 正文还在。本叶不改文档。

## 架构合规

- D1–D4：未改算法、未改 Java、未改调用链、未改 Nebula、未改可观测埋点。✅
- D5：无代码提交，无 pipeline。✅
- D6 / D12：只读 demo 与产线库，没有把 demo 仓 merge 进 lumen，也没有让 lumen 调用 demo 服务。✅
- D8 / D10：未改前端。✅
- D9：未改口径，只核对已提交 CREATE 里的注释是否在现网。✅
- D14：未涉及对象存储。✅
- 未写 ODS / 供应库 `gkx`。未改 `policy_base_info`。✅
- 口令未写入本文件。✅

## cost

- actual_tokens: 未单列（随会话）
- model_used: grok-4.7
- actual_cost: 0
- cost_warn: green

## CI/CD

- 分支：`dev`（未提交本 handoff）
- commit：无
- pipeline URL / ID：无
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：只读 `10.50.11.76:3306` 的 `information_schema` 与 `SHOW CREATE TABLE`

## 可观测性

- 无服务变更，无新 trace。

## 涉及文件

- 新增 `agent-delivery/agent-handoffs/政策模块-E7/POLICY-DDL-CHECK-L04.md`
- 只读 `agent-delivery/data/data-design/storage/POLICY/stores/mysql/ads.md`
- 只读 `agent-delivery/data/data-design/storage/POLICY/stores/mysql/dwd.md`

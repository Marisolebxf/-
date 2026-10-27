# CHAIN-DDL-GDF-FIX-L01 · 产业维四张链树表补 CREATE

处理 `CHAIN-DDL-GDF-CHECK-L00` 的缺口：结构真源与现行派单包都没有 `CREATE TABLE`。四张链树表各留一份带注释的 CREATE，派单包原样复制，两个 DWD 库只补注释。自检退出码 `0`。

口令未写入本文件。未建空表。未改列集、类型、主键、唯一键。未灌数。

## 任务认领

| 字段 | 值 |
|------|-----|
| 任务 | `CHAIN-DDL-GDF-FIX-L01` |
| task_type | `tech_task` |
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| 厚包 | `agent-delivery/agent-handoffs/产业链分析-CHAIN/CHAIN-DDL-GDF-长任务总控.md` |
| 说明 | 派单写明不改 task-registry。`task-get` 无此 ID。本叶未写认领、未改状态。前置 handoff `CHAIN-DDL-GDF-CHECK-L00.md` 已在，才开工 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只补 CHECK 点名的四张表。建表注释、`utf8mb4_0900_ai_ci`、handoff 都写了，没有用 YAGNI 跳过 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无 |
| 图 diff | 本叶未改存储流图，未改存储拓扑 |
| 会签态 | 不涉及 |

## CHECK 缺口

`CHAIN-DDL-GDF-CHECK-L00` 自检退出码 `1`，脚本只有这一条：

- `dwd.md/ads.md 与派单包都没有 CREATE TABLE`

本叶处理这一条。结构目录没有名为 `dwd.md` 的文件，CREATE 写在扫描范围内的 `dwd-chain.md`。没有第二套 CREATE。行业分析六表和 v5 其余十张没有加进 CREATE。

## 四张表

列、类型、空值、默认值、索引取现网 `demo_gkxlumenx_dwd` 的 `SHOW CREATE TABLE`。不写 `AUTO_INCREMENT` 当前值。表和字符列写成 `utf8mb4` / `utf8mb4_0900_ai_ci`。改前两库表级和字符列已经是这一套，没有 `utf8mb4_unicode_ci` 或 `utf8mb4_general_ci` 要改。

中文注释用 v5 字段表和 §3.3 已有的那句。对不上的列没有，口径待补清单为空。

| 表 | CREATE | demo 行数 | 产线行数 | 是否建空表 |
|----|--------|-----------|----------|------------|
| `industry_chain` | `dwd-chain.md` §2.1；复制件 `10-DWD-MySQL-DDL/链树四表.md` | 49 | 0 | 否。两库改前已有基表 |
| `industry_chain_node` | 同上 | 222 | 0 | 否 |
| `industry_chain_node_rel` | 同上 | 181 | 0 | 否 |
| `industry_chain_entity_rel` | 同上 | 206671 | 0 | 否 |

行数是改注释前后的 `COUNT(*)`，没有变化。产线这四张本来就是 0 行，本叶没有 `CREATE TABLE` 进库，也没有从 ADS 或供应库拷行。

两库改前列集、类型、空值、默认值、索引一致，所以没有「CREATE 有而现网没有的可空列」要加。

`node_scope_key` 仍是 `STORED GENERATED`，表达式还在。

现网唯一键保持原样，没有按 v5 加第二套：

- `industry_chain`：`PRIMARY (id)`、`uk_chain_id (chain_id)`。v5 的 `chain_code`、`industry_id` 唯一键不在现网，未加
- `industry_chain_node`：`PRIMARY (id)`、`uk_chain_node (chain_id, node_id)`。v5 的 `(chain_id, node_code)` 未加
- `industry_chain_node_rel`：`PRIMARY (id)`、`uk_rel (relation_id)`。v5 的关系防重键未加
- `industry_chain_entity_rel`：`PRIMARY (id)`、`uk_rel (relation_id)`。v5 的关系防重键未加

## 注释

业务列改前注释为空，写入 v5 中文注释。治理列改前已有较短注释，改成 v5 §3.3 那句。`source_table` 改前已是「来源表名」，与 v5 相同，未改。

| 列 | 改前 | 改后 |
|----|------|------|
| `id` | 自增主键 | 物理自增主键 |
| `source_system` | 来源系统 | 来源系统标识 |
| `source_record_id` | 来源记录主键 | 来源记录业务键或行键 |
| `etl_batch_id` | ETL批次号 | 数据加工批次号 |
| `data_version` | 数据版本 | 来源数据或平台版本 |
| `valid_from` | 有效期起 | 记录生效时间 |
| `valid_to` | 有效期止 | 记录失效时间 |
| `is_deleted` | 逻辑删除标记（0否1是） | 逻辑删除标记 |
| `created_time` | 创建时间 | 平台创建时间 |
| `updated_time` | 更新时间 | 平台更新时间 |
| `ext` | 扩展JSON | 扩展属性 JSON |

表注释改前为空。改后：产业链标准信息表、产业链节点信息表、产业链节点关系表、产业链实体关系表。

口径待补：无。

## 命令与原文

工作目录 `gkx-orchestration`。主机 `10.50.11.76`，端口 `3306`。账号放在 `GKX_LUMEN_MYSQL_USER`。口令只在进程环境变量，查完未写入文件。

```powershell
python .cursor/skills/gkx-gdf-ddl-signoff/scripts/check_gdf_ddl.py --dimension chain
```

退出码：`0`。stderr 为空。stdout 原文：

```
文件一致 industry_chain
文件一致 industry_chain_entity_rel
文件一致 industry_chain_node
文件一致 industry_chain_node_rel
库一致 demo_gkxlumenx_dwd.industry_chain
库一致 gkxlumenx_dwd.industry_chain
库一致 demo_gkxlumenx_dwd.industry_chain_entity_rel
库一致 gkxlumenx_dwd.industry_chain_entity_rel
库一致 demo_gkxlumenx_dwd.industry_chain_node
库一致 gkxlumenx_dwd.industry_chain_node
库一致 demo_gkxlumenx_dwd.industry_chain_node_rel
库一致 gkxlumenx_dwd.industry_chain_node_rel
派单包 agent-delivery\data\GDF\派单包\产业链\GDF-CHAIN-WORKPACK-v2
结构真源 agent-delivery\data\data-design\storage\CHAIN\stores\mysql
通过
```

## 问题清单

- CHECK 的「都没有 CREATE TABLE」已补上。自检通过。
- 口径待补：无。

## 修改内容

- `dwd-chain.md`：四张链树表各一块 CREATE。「勿在本文件粘贴全 DDL」只对这四张作废。其余十张仍只留清单。
- `10-DWD-MySQL-DDL/链树四表.md`：四块 CREATE 与 `dwd-chain.md` 的 sql 围栏逐字节相同。库名仍是 `demo_gkxlumenx_dwd`。
- `10-DWD-MySQL-DDL/README.md`：改为这四张以 `dwd-chain.md` 为准，本目录只放复制件。v5 不再当这四张的结构真源。
- 两个 DWD 库：只 `ALTER` 注释。`demo_gkxlumenx_dwd` 与 `gkxlumenx_dwd` 各四张。行数不变。
- 未对本包 APPLY `demo_gkxlumenx_dwd_industry_analysis_show_create.sql`。
- 未建行业分析六表，未建 v5 其余十张，未改 ADS。
- 未写 `gkxlumenx_ods`，未写供应库 `gkx`。未 DROP。未删列。
- 未改算法仓。未改 task-registry。本叶文档随本次提交推 `origin/dev`。
- 口令未写入派单、handoff、提交说明。

## 测试结果

- `check_gdf_ddl.py --dimension chain` 退出码 `0`，stdout 见上文原文。
- 四块 sql 围栏：`dwd-chain.md` 与 `链树四表.md` 逐字节相同。
- `node_scope_key` 两库仍是 `STORED GENERATED`。
- 四张表字符列没有非 `utf8mb4_0900_ai_ci` 的排序规则。

## 遗留风险

- v5 写过、现网没有的唯一键本叶没加。要加就是改唯一键，派单要求先停。
- 产线四张表仍是 0 行。本叶不灌数。

## 架构合规

- D1：未改算法。✅
- D2：未改调用链。✅
- D3：未改 Nebula。图不必。✅
- D4：未改可观测埋点。✅
- D5：文档与库注释，无业务仓提交，无 pipeline。✅
- D6 / D12：未把 demo 仓 merge 进 lumen，未让 lumen 调用 demo 服务。两库按同一份 CREATE 对齐，只换库名。✅
- D8 / D10：未改前端。✅
- D9：未改指标口径。列注释用的是 v5 已有中文，没有新口径。✅
- D14：未涉及对象存储。✅
- 未写 ODS / 供应库 `gkx`。未 DROP 有数据的表。未改列集、类型、主键、唯一键。✅
- 口令未写入本文件。✅

## cost

- actual_tokens: 未单列（随会话）
- model_used: grok-4.7
- actual_cost: 0
- cost_warn: green

## CI/CD

- 分支：`dev`，推 `origin/dev`
- commit：本文件与四张链树表 CREATE 同一次提交
- pipeline URL / ID：无
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：`check_gdf_ddl.py --dimension chain` 退出码 0。已连 `10.50.11.76:3306`

## 可观测性

- 无服务变更，无新 trace。

## 涉及文件

- 修改 `agent-delivery/data/data-design/storage/CHAIN/stores/mysql/dwd-chain.md`
- 修改 `agent-delivery/data/GDF/派单包/产业链/GDF-CHAIN-WORKPACK-v2/10-DWD-MySQL-DDL/README.md`
- 新增 `agent-delivery/data/GDF/派单包/产业链/GDF-CHAIN-WORKPACK-v2/10-DWD-MySQL-DDL/链树四表.md`
- 新增 `agent-delivery/agent-handoffs/产业链分析-CHAIN/CHAIN-DDL-GDF-FIX-L01.md`
- 只读 `agent-delivery/agent-handoffs/产业链分析-CHAIN/CHAIN-DDL-GDF-CHECK-L00.md`
- 只读 `agent-delivery/data/data-design/storage/mysql-ddl-convention.md` 第 1、2、8 条
- 未改 `.cursor/skills/gkx-gdf-ddl-signoff/scripts/check_gdf_ddl.py`

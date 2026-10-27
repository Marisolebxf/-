# MySQL DWD · 产业链标准明细（v5）

```yaml
---
doc_id: CHAIN-STORE-DWD
element: CHAIN
role: store-mysql
status: draft
version: "2026-08-16"
updated: "2026-10-27"
engine: mysql
s3_task: DATA-CHAIN-STORAGE-S3-L01
as_built_source: data-design/产业链/产业链-DWD表设计-业务需求驱动(v5).md
---
```

> **链树四表结构真源**：本文件 §2.1 的四块 `CREATE`。库名写 `demo_gkxlumenx_dwd`；产线 `gkxlumenx_dwd` 只换库名。列、类型、空值、默认值、索引取现网 demo 同名表。中文注释用 v5 里已有的那句。  
> 「勿在本文件粘贴全 DDL」只对 `industry_chain`、`industry_chain_node`、`industry_chain_node_rel`、`industry_chain_entity_rel` 作废。其余十张仍只留第 2 节清单，不贴 CREATE。v5 不再当这四张的结构真源。设计说明仍见 [`产业链-DWD表设计-业务需求驱动(v5).md`](../../../../产业链/产业链-DWD表设计-业务需求驱动(v5).md)。  
> **库**：正式 `gkxlumenx_dwd`；Demo `demo_gkxlumenx_dwd`。表名 **无** `dwd_` 前缀，统一 `industry_chain_*`。  
> **对照（勿当真源）**：[`DATA-CHAIN-db-design.md`](../../../../../agent-handoffs/产业链分析-CHAIN/DATA-CHAIN-db-design.md) 旧 PG/8 表稿。  
> **ODS 入站**：供应方四表见 [`../../sources/inventory.md`](../../sources/inventory.md)；映射见 Step2 复核报告。  
> **Demo 模拟过程**（draft）：[`../../etl/pipeline-demo-sim-process.md`](../../etl/pipeline-demo-sim-process.md) · 字段矩阵 [`../../etl/ods-to-dwd-mapping.md`](../../etl/ods-to-dwd-mapping.md)。

## 1. 写读

| 写 | 读 |
|---|---|
| Python ETL / 模拟 GDF（[`../../etl/pipeline-ods-to-dwd.md`](../../etl/pipeline-ods-to-dwd.md)） | Python / algorithm；**Java 不扫 DWD 对外** |

## 2. 表清单（v5 · 14 张）

| # | 表 | 中文 | 一行语义 |
|---|---|---|---|
| 1 | `industry_chain` | 产业链标准信息 | L0 产业与 L1+ 子链名录（`industry_id`/`chain_tier`） |
| 2 | `industry_chain_node` | 节点信息 | 链内标准节点 |
| 3 | `industry_chain_node_rel` | 节点关系 | 上下游/供需等结构边 |
| 4 | `industry_chain_entity_rel` | 实体关系 | 链/节点 ↔ 企业等外部实体 |
| 5 | `industry_chain_market_observation` | 市场指标观测 | 外部导入原子观测；**平台市场规模不进本表** |
| 6 | `industry_chain_investment_event` | 投融资事件 | 资本事件主数据 |
| 7 | `industry_chain_investment_participant` | 投融资参与方扩展 | 金额等扩展；角色在 event_entity_rel |
| 8 | `industry_chain_news_event` | 资讯事件 | 产业资讯主数据 |
| 9 | `industry_chain_milestone_event` | 里程碑（可选） | 门户历程以 CMS 为准 |
| 10 | `industry_chain_event_entity_rel` | 事件实体关系 | 事件 ↔ 实体 |
| 11 | `industry_chain_event_metric_observation` | 事件指标观测 | 浏览/互动等时序 |
| 12 | `industry_chain_extraction_result` | 抽取结果 | NLP 实体/关系明细 |
| 13 | `industry_chain_model_run` | 模型运行 | 可复现运行记录 |
| 14 | `industry_chain_model_result_detail` | 模型结果明细 | 单次运行原子结果 |

主键口径：`chain_id` / `node_id` / `industry_id` = INB 升格（Q053）。

## 2.1 链树四表 CREATE

下面四块是这四张表仅有的一份带注释 CREATE。不写 `AUTO_INCREMENT` 当前值。表和字符列是 `utf8mb4` / `utf8mb4_0900_ai_ci`。v5 里多出来的唯一键不在现网，这里不写。

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_dwd`.`industry_chain` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理自增主键',
  `source_system` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '来源系统标识',
  `source_table` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '来源表名',
  `source_record_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '来源记录业务键或行键',
  `etl_batch_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数据加工批次号',
  `data_version` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '来源数据或平台版本',
  `valid_from` datetime NOT NULL COMMENT '记录生效时间',
  `valid_to` datetime DEFAULT NULL COMMENT '记录失效时间',
  `is_deleted` tinyint NOT NULL DEFAULT '0' COMMENT '逻辑删除标记',
  `created_time` datetime NOT NULL COMMENT '平台创建时间',
  `updated_time` datetime NOT NULL COMMENT '平台更新时间',
  `ext` json DEFAULT NULL COMMENT '扩展属性 JSON',
  `chain_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产业链归一主键',
  `industry_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'L0 产业对象主键',
  `chain_code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产业链来源编码',
  `chain_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产业链标准名称',
  `chain_short_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '产业链简称',
  `parent_chain_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '上级产业链主键',
  `chain_tier` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产业对象层级',
  `chain_level` int NOT NULL COMMENT '来源/树形数值层级',
  `chain_category` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '产业链分类',
  `future_industry_flag` tinyint NOT NULL DEFAULT '0' COMMENT '未来产业标记',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '产业链说明',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产业链有效状态',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_chain_id` (`chain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='产业链标准信息表';
```

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_dwd`.`industry_chain_node` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理自增主键',
  `source_system` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '来源系统标识',
  `source_table` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '来源表名',
  `source_record_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '来源记录业务键或行键',
  `etl_batch_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数据加工批次号',
  `data_version` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '来源数据或平台版本',
  `valid_from` datetime NOT NULL COMMENT '记录生效时间',
  `valid_to` datetime DEFAULT NULL COMMENT '记录失效时间',
  `is_deleted` tinyint NOT NULL DEFAULT '0' COMMENT '逻辑删除标记',
  `created_time` datetime NOT NULL COMMENT '平台创建时间',
  `updated_time` datetime NOT NULL COMMENT '平台更新时间',
  `ext` json DEFAULT NULL COMMENT '扩展属性 JSON',
  `node_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产业链节点归一主键',
  `chain_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '所属产业链主键',
  `node_code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '节点来源编码',
  `node_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '节点标准名称',
  `parent_node_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '父节点主键',
  `node_level` int NOT NULL COMMENT '节点层级',
  `stage_code` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '上中下游阶段编码',
  `node_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '节点业务类型',
  `importance_level` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '来源明确的节点重要等级',
  `sort_no` int DEFAULT NULL COMMENT '同级节点排序号',
  `node_path` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '节点层级路径',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '节点说明',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '节点有效状态',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_chain_node` (`chain_id`, `node_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='产业链节点信息表';
```

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_dwd`.`industry_chain_node_rel` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理自增主键',
  `source_system` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '来源系统标识',
  `source_table` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '来源表名',
  `source_record_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '来源记录业务键或行键',
  `etl_batch_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数据加工批次号',
  `data_version` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '来源数据或平台版本',
  `valid_from` datetime NOT NULL COMMENT '记录生效时间',
  `valid_to` datetime DEFAULT NULL COMMENT '记录失效时间',
  `is_deleted` tinyint NOT NULL DEFAULT '0' COMMENT '逻辑删除标记',
  `created_time` datetime NOT NULL COMMENT '平台创建时间',
  `updated_time` datetime NOT NULL COMMENT '平台更新时间',
  `ext` json DEFAULT NULL COMMENT '扩展属性 JSON',
  `relation_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '节点关系主键',
  `chain_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '所属产业链主键',
  `source_node_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关系起点节点主键',
  `target_node_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关系终点节点主键',
  `relation_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '节点关系类型编码',
  `relation_direction` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关系方向',
  `relation_weight` decimal(18,6) DEFAULT NULL COMMENT '来源明确的关系权重',
  `confidence` decimal(8,6) DEFAULT NULL COMMENT '关系识别置信度',
  `evidence_ref` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '关系证据引用',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_rel` (`relation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='产业链节点关系表';
```

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_dwd`.`industry_chain_entity_rel` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理自增主键',
  `source_system` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '来源系统标识',
  `source_table` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '来源表名',
  `source_record_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '来源记录业务键或行键',
  `etl_batch_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数据加工批次号',
  `data_version` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '来源数据或平台版本',
  `valid_from` datetime NOT NULL COMMENT '记录生效时间',
  `valid_to` datetime DEFAULT NULL COMMENT '记录失效时间',
  `is_deleted` tinyint NOT NULL DEFAULT '0' COMMENT '逻辑删除标记',
  `created_time` datetime NOT NULL COMMENT '平台创建时间',
  `updated_time` datetime NOT NULL COMMENT '平台更新时间',
  `ext` json DEFAULT NULL COMMENT '扩展属性 JSON',
  `relation_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产业链实体关系主键',
  `chain_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '所属产业链主键',
  `node_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '所属节点主键',
  `node_scope_key` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci GENERATED ALWAYS AS (ifnull(`node_id`,_utf8mb4'__CHAIN__')) STORED COMMENT '链级或节点级关系去重键',
  `entity_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '外部实体类型',
  `entity_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '外部实体权威业务键',
  `entity_subtype` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '外部实体细分类别',
  `relation_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '实体与链或节点的关系类型',
  `role_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '实体在产业链中的角色',
  `importance_level` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '来源明确的关系重要等级',
  `confidence` decimal(8,6) DEFAULT NULL COMMENT '关系可信度或抽取置信度',
  `is_primary` tinyint DEFAULT NULL COMMENT '是否主要归属关系',
  `evidence_ref` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '关系证据引用',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_rel` (`relation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='产业链实体关系表';
```

## 3. 冲突说明

| 旧稿 | 本树裁决 |
|---|---|
| DATA-CHAIN-db-design 8 张 / PG schema | **废作 DWD 真源**；仅历史对照 |
| 供应方 `dwd_industry_chain_info` 等 | **约定 ODS**，不是项目 DWD |

## 4. 禁止

- 把算法页面结论回写 DWD 形成双轨（见 v5 §2.5）  
- CMS「产业介绍/发展历程」长文双写 DWD  
- 细表标 `approved`（须单独结构评审）

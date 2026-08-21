# 三方政策贴源 DDL（结构真源）

```yaml
---
doc_id: POLICY-ODS-DDL
element: POLICY
role: source
status: draft
version: "2026-08-21"
updated: 2026-08-21
engine: mysql
task_id: DATA-POLICY-STORAGE-S2-L01
---
```

> **表结构以此文件为准**（`human:淮政玮` 提供 · 2026-08-21）。供应库 `gkx`；Demo 镜像同 DDL、同表名。  
> 角色 = **ODS 贴源**。禁止把本表当项目 DWD。禁止再写 `dwd_zck_*`。  
> 本叶不 APPLY。冲突时：**本 DDL 赢** `doc/` xlsx / 旧映射报告。

## `dwd_policy_base`（国内政策库）

```sql
CREATE TABLE `dwd_policy_base` (
  `id` varchar(100) NOT NULL COMMENT '技术字段:表的主键',
  `title` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '政策标题',
  `publish_code` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '政策文号',
  `ministry` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '发文部门',
  `publish_date` date DEFAULT NULL COMMENT '发文日期',
  `publish_year` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '发布年',
  `implementation_date` date DEFAULT NULL COMMENT '实施日期',
  `expire_date` date DEFAULT NULL COMMENT '失效日期',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '政策状态，分为失效和有效',
  `rank` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '政策级别（国家级/省级/市级/区县级）',
  `type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '政策类型',
  `province` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '省',
  `city` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '市',
  `district` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '区',
  `abstract` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '政策摘要',
  `keywords` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '关键词',
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '政策正文',
  `link` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '政策链接',
  `quote_policy` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '引用政策',
  `theme` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '对政策背景、指导思想等政策内容进行标准化拆解与提炼',
  `keypoints` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '从政策全文中摘录、提炼章节标题、工作原则、发展现状、重点任务、细分产业、问题研判等内容。',
  `policy_support` json DEFAULT NULL COMMENT '[政策扶持目标]政策支持匹配（支持对象，支持行为列表，支持方式列表，申报条件列表）',
  `source` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '政策源',
  `appendix_name` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '附件名称',
  `appendix_link` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '附件链接',
  `created_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '技术字段:数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '技术字段:该条数据最近一次更新的时间',
  `creater` varchar(100) DEFAULT NULL COMMENT '技术字段:数据新增操作员',
  `updater` varchar(100) DEFAULT NULL COMMENT '技术字段:数据更新操作员',
  `table_data_source` varchar(100) DEFAULT NULL COMMENT '技术字段:数据来源',
  `is_deleted` smallint NOT NULL DEFAULT '0' COMMENT '技术字段:逻辑删除标识,0未删除,1已删除',
  `operator_remarks` varchar(100) DEFAULT NULL COMMENT '技术字段:操作备注',
  `insert_remark` smallint NOT NULL DEFAULT '0' COMMENT '技术字段:插入标识,0新增,1修改,2补齐',
  `is_history` tinyint DEFAULT NULL COMMENT '是否历史标识，0当前，1历史',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='政策-国内政策-国内政策库';
```

## `dwd_global_policy_base`（国外政策信息表）

```sql
CREATE TABLE `dwd_global_policy_base` (
  `id` varchar(100) NOT NULL COMMENT '技术字段:表的主键',
  `title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '政策文件的正式标题',
  `abstract` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '政策内容的简要概述',
  `organ` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '政策制定/发布机构名称',
  `year` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '政策发布年份',
  `publish_date` date NOT NULL COMMENT '政策正式发布日期',
  `disclosure_date` date DEFAULT NULL COMMENT '政策对外披露日期',
  `category` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '政策所属的业务领域分类',
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '政策文件完整正文内容',
  `region` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '政策具体实施的地理区域',
  `link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '政策原文网页链接',
  `language` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '政策文本使用的自然语言',
  `source` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '数据采集的原始来源系统',
  `geo_region` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '宏观地理区域划分',
  `appendix_name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '政策附件的文件名称',
  `appendix_link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '政策附件的下载链接',
  `country` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '政策所属国家或地区',
  `report_number` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '政策报告的官方编号',
  `topic` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '政策所属专题领域',
  `theme` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '政策核心主题标签',
  `project_id` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '关联的项目编号',
  `security_class` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '文档保密等级',
  `version_type` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '政策版本类型（草案/正式版等）',
  `volume_no` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '政策文献的卷册编号',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '技术字段:数据在库中的创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '技术字段:该条数据最近一次更新的时间',
  `creater` varchar(100) DEFAULT NULL COMMENT '技术字段:数据新增操作员',
  `updater` varchar(100) DEFAULT NULL COMMENT '技术字段:数据更新操作员',
  `table_data_source` varchar(100) DEFAULT NULL COMMENT '技术字段:数据来源',
  `is_deleted` smallint NOT NULL DEFAULT '0' COMMENT '技术字段:逻辑删除标识,0未删除,1已删除',
  `operator_remarks` varchar(100) DEFAULT NULL COMMENT '技术字段:操作备注',
  `insert_remark` smallint NOT NULL DEFAULT '0' COMMENT '技术字段:插入标识,0新增,1修改,2补齐',
  `doc_type` varchar(64) DEFAULT NULL COMMENT '文档类型',
  `is_history` int DEFAULT NULL COMMENT '是否历史标识,0当前,1历史',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='政策-国外政策-国外政策信息表';
```

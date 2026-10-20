-- ============================================================
-- ODS 重建后修复（2026-10-20 22:45）：两个执行遗漏一次性补齐
-- ① dwd_patent_assignees 补建（原脚本 sed 派生 bug 表名漏改，执行报错跳过）
-- ② dwd_org_income_statement 补 22 列（大文件执行时截断，库里止于第 106 列 qtqygjtzgyjzbd）
-- 用法：USE gkxlumenx_ods; 后执行本文件
-- ============================================================

USE gkxlumenx_ods;

-- ① assignees 补建
DROP TABLE IF EXISTS `dwd_patent_assignees`;
CREATE TABLE `dwd_patent_assignees` (
  `dwd_id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `patent_id` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '专利记录逻辑主键，用于记录唯一标识',
  `pn` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '专利记录唯一标识，与DOCDB兼容，用于关联各专利要素分表',
  `sequence` int DEFAULT NULL COMMENT '当前申请人或专利权人在权利人列表中的排列序号',
  `name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '当前有效的申请人、受让人或专利权人名称',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '技术字段：创建时间',
  `updated_time` datetime NOT NULL COMMENT '技术字段：更新时间',
  `creater` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '技术字段：新增操作员',
  `updater` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '技术字段：更新操作员',
  `table_data_source` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '技术字段：数据来源',
  `operator_remarks` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '技术字段：操作备注',
  `is_deleted` smallint NOT NULL DEFAULT '0' COMMENT '技术字段：0未删除,1已删除',
  `insert_remark` smallint NOT NULL DEFAULT '0' COMMENT '技术字段：0新增,1修改,2补齐',
  PRIMARY KEY (`dwd_id`),
  KEY `idx_dwd_id_ut` (`dwd_id`,`updated_time`) COMMENT '业务主键+updated_time联合索引',
  KEY `idx_ut_log` (`updated_time`,`dwd_id`),
  KEY `idx_ut_biz` (`updated_time`,`patent_id`),
  KEY `idx_ut_biz_log` (`updated_time`,`patent_id`,`dwd_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='专利当前权力人信息表';

-- ② 利润表补 22 列
ALTER TABLE `dwd_org_income_statement` ADD COLUMN `qyzsxyfxgyjzbd` decimal(20,4) DEFAULT NULL COMMENT '企业自身信用风险公允价值变动';
ALTER TABLE `dwd_org_income_statement` ADD COLUMN `qtzqtzgyjzbd` decimal(20,4) DEFAULT NULL COMMENT '其他债权投资公允价值变动';
ALTER TABLE `dwd_org_income_statement` ADD COLUMN `jrzczfljrqtzhsydje` decimal(20,4) DEFAULT NULL COMMENT '金融资产重分类计入其他综合收益的金额';
ALTER TABLE `dwd_org_income_statement` ADD COLUMN `qtzqtzxyjzzb` decimal(20,4) DEFAULT NULL COMMENT '其他债权投资信用减值准备';
ALTER TABLE `dwd_org_income_statement` ADD COLUMN `qtgdfp` decimal(20,4) DEFAULT NULL COMMENT '其他(股东分配)';
ALTER TABLE `dwd_org_income_statement` ADD COLUMN `xjlltqcb` decimal(20,4) DEFAULT NULL COMMENT '现金流量套期储备';
ALTER TABLE `dwd_org_income_statement` ADD COLUMN `tqybfxzbkfplr` decimal(20,4) DEFAULT NULL COMMENT '提取一般风险准备(可分配利润)';
ALTER TABLE `dwd_org_income_statement` ADD COLUMN `tycbjrzccssy` decimal(20,4) DEFAULT NULL COMMENT '以摊余成本计量的金融资产终止确认产生的收益';
ALTER TABLE `dwd_org_income_statement` ADD COLUMN `yfyxzlx` decimal(20,4) DEFAULT NULL COMMENT '应付永续债利息';
ALTER TABLE `dwd_org_income_statement` ADD COLUMN `zcjzssyylr` decimal(20,4) DEFAULT NULL COMMENT '资产减值损失(营业利润)';
ALTER TABLE `dwd_org_income_statement` ADD COLUMN `xyjzssyylr` decimal(20,4) DEFAULT NULL COMMENT '信用减值损失(营业利润)';
ALTER TABLE `dwd_org_income_statement` ADD COLUMN `sybj` int DEFAULT NULL COMMENT '使用标记';
ALTER TABLE `dwd_org_income_statement` ADD COLUMN `rksj` datetime DEFAULT NULL COMMENT '入库时间';
ALTER TABLE `dwd_org_income_statement` ADD COLUMN `gxsj` datetime DEFAULT NULL COMMENT '更新时间';
ALTER TABLE `dwd_org_income_statement` ADD COLUMN `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '技术字段：创建时间';
ALTER TABLE `dwd_org_income_statement` ADD COLUMN `updated_time` datetime NOT NULL COMMENT '技术字段：更新时间';
ALTER TABLE `dwd_org_income_statement` ADD COLUMN `creater` varchar(100) DEFAULT NULL COMMENT '技术字段：新增操作员';
ALTER TABLE `dwd_org_income_statement` ADD COLUMN `updater` varchar(100) DEFAULT NULL COMMENT '技术字段：更新操作员';
ALTER TABLE `dwd_org_income_statement` ADD COLUMN `table_data_source` varchar(100) DEFAULT NULL COMMENT '技术字段：数据来源';
ALTER TABLE `dwd_org_income_statement` ADD COLUMN `operator_remarks` varchar(100) DEFAULT NULL COMMENT '技术字段：操作备注';
ALTER TABLE `dwd_org_income_statement` ADD COLUMN `is_deleted` smallint NOT NULL DEFAULT '0' COMMENT '技术字段：0未删除,1已删除';
ALTER TABLE `dwd_org_income_statement` ADD COLUMN `insert_remark` smallint NOT NULL DEFAULT '0' COMMENT '技术字段：0新增,1修改,2补齐';

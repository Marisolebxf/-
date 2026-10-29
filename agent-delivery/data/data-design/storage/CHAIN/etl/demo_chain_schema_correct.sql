-- 产业链维 · Demo 库结构纠正（对齐设计，不碰正式库）
-- 抽样：2026-08-20  dev/demo-platform-innov-py → 10.50.11.76
-- 设计真源：
--   ODS 四表 = md-extract CSV / llm_ods field_mysql_ddl / demo_gkxlumenx_ods_chain_tables.sql
--   DWD v5 14 表 = chainan.llm_ods.ddl._dwd_ddl
--   ADS v2 10 表 = chainan.llm_ods.ddl._ads_ddl
--   DIM 产业集群 = data/ddl/gkxlumenx_dim_industry_cluster.sql
-- 目标库：仅 demo_gkxlumenx_* 。禁止对本文件执行 gkxlumenx_* / 三方库。
-- 保留：live 克隆的 pk_id + 六技术字段（created_time/creater/…）。不改建 _demo_id。

-- =============================================================================
-- 0. 对照结论（本文件不改这些）
-- =============================================================================
-- DWD v5 十四表 demo_gkxlumenx_dwd.industry_chain*     ：与 v5 DDL 一致，无纠正。
-- ADS v2 十表   demo_gkxlumenx_ads.industry_chain_*    ：与 v2 DDL 一致，无纠正。
-- DIM           demo_gkxlumenx_dim.industry_cluster[_map]：与设计 DDL 一致，无纠正。
-- 正式 gkxlumenx_dwd / _ads 无 industry_chain_* v5/v2 表；
-- 正式 gkxlumenx_dim 无产业集群两表。那是另开建表，不是本纠正脚本。
-- 正式 gkxlumenx_ods 四表业务键类型已接近约定（credit_code/news.id = varchar(255)），
--   不要用本脚本去「纠正」正式贴源。

-- =============================================================================
-- A. 灌数阻断（类型族错误）—— 可重复执行
--    2026-08-20 已在 Demo 执行过；再跑是幂等 MODIFY。
-- =============================================================================

ALTER TABLE `demo_gkxlumenx_ods`.`dwd_org_industry_tags`
  MODIFY COLUMN `credit_code` VARCHAR(255) NULL
    COMMENT 'md-extract 字符255；曾误建成 char(1)，18位信用代码 1406';

ALTER TABLE `demo_gkxlumenx_ods`.`dwd_industry_chain_news_info`
  MODIFY COLUMN `id` VARCHAR(255) NULL
    COMMENT 'md-extract 字符255；曾误建成 bigint，news-INB* 字符串 1366';

-- =============================================================================
-- B. 约定加宽：tags / product / news 的 industry_code、industry_name
--    设计：字符 2500/10000 → llm_ods 落 TEXT。
--    线上：varchar(255) 且有整列二级索引，改 TEXT 必须先丢索引再加前缀索引。
--    当前 mock（INB 短码）塞得进 255；三方 JSON 数组口径会超 255。
--    有数据也可执行（varchar→TEXT 无损）。勿跑第二遍（DROP INDEX 会失败）。
-- =============================================================================

ALTER TABLE `demo_gkxlumenx_ods`.`dwd_org_industry_tags`
  DROP INDEX `idx_dwd_org_industry_tags_industry_code`,
  DROP INDEX `idx_dwd_org_industry_tags_industry_name`,
  MODIFY COLUMN `industry_code` TEXT NOT NULL,
  MODIFY COLUMN `industry_name` TEXT NOT NULL,
  ADD INDEX `idx_dwd_org_industry_tags_industry_code` (`industry_code`(768)),
  ADD INDEX `idx_dwd_org_industry_tags_industry_name` (`industry_name`(768));

ALTER TABLE `demo_gkxlumenx_ods`.`dwd_org_industry_product_tags`
  DROP INDEX `idx_dwd_org_industry_product_tags_industry_code`,
  DROP INDEX `idx_dwd_org_industry_product_tags_industry_name`,
  MODIFY COLUMN `industry_code` TEXT NOT NULL,
  MODIFY COLUMN `industry_name` TEXT NOT NULL,
  ADD INDEX `idx_dwd_org_industry_product_tags_industry_code` (`industry_code`(768)),
  ADD INDEX `idx_dwd_org_industry_product_tags_industry_name` (`industry_name`(768));

ALTER TABLE `demo_gkxlumenx_ods`.`dwd_industry_chain_news_info`
  DROP INDEX `idx_dwd_industry_chain_news_info_industry_code`,
  DROP INDEX `idx_dwd_industry_chain_news_info_industry_name`,
  MODIFY COLUMN `industry_code` TEXT NOT NULL,
  MODIFY COLUMN `industry_name` TEXT NOT NULL,
  ADD INDEX `idx_dwd_industry_chain_news_info_industry_code` (`industry_code`(768)),
  ADD INDEX `idx_dwd_industry_chain_news_info_industry_name` (`industry_name`(768));

-- =============================================================================
-- C. 可选（不挡当前 llm_ods 生成值；与约定仍有差）
--    默认注释。需要与 CSV 类型逐字对齐时再解开。
-- =============================================================================

-- 链表 level：设计 DECIMAL(20,0)，线上 tinyint（0/1/2 够用）
-- ALTER TABLE `demo_gkxlumenx_ods`.`dwd_industry_chain_info`
--   MODIFY COLUMN `level` DECIMAL(20,0) NULL;

-- 链表 node_company_count：设计 DECIMAL(20,0)，线上 bigint
-- ALTER TABLE `demo_gkxlumenx_ods`.`dwd_industry_chain_info`
--   MODIFY COLUMN `node_company_count` DECIMAL(20,0) NULL;

-- 产品 id：设计 DECIMAL(20,4)，线上 bigint（生成器写整数序号，bigint 可留）
-- ALTER TABLE `demo_gkxlumenx_ods`.`dwd_org_industry_product_tags`
--   MODIFY COLUMN `id` DECIMAL(20,4) NULL;

-- 资讯 publish_date：设计 DATE，线上 datetime（日期字符串可进 datetime）
-- ALTER TABLE `demo_gkxlumenx_ods`.`dwd_industry_chain_news_info`
--   MODIFY COLUMN `publish_date` DATE NULL;

-- =============================================================================
-- D. 明确不改
-- =============================================================================
-- 1) 四表主键保持 pk_id，不新增 _demo_id（双自增冲突；灌数按列名 INSERT）。
-- 2) 不删除 created_time / updated_time / creater / updater / table_data_source /
--    is_deleted / operator_remarks / insert_remark / EDW_* 等 live 技术列。
-- 3) 不加宽已经更宽的列：parent_code/text、company_name/text、credit_code/text（产品表）、
--    title/text、source/text。
-- 4) 不 DROP 重建四表（会丢现网 Demo 行：链表/企业/产品/资讯已有数据）。
-- 5) 不对 gkxlumenx_ods / gkxlumenx_dwd / gkxlumenx_ads / gkxlumenx_dim 执行本文件。

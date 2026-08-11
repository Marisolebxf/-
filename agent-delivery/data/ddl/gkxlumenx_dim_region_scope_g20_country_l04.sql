-- region_scope：全球枝 G20 城市 → G20 主权国家（ISO alpha-3）
-- 任务：DATA-ENT-CODE-COUNTRY-APPLY-L01 / PY-ENT-REGION-SCOPE-G20-COUNTRY-L01
-- 依赖：先执行 gkxlumenx_dim_code_country.sql
-- 日期：2026-08-11
-- 保留：全国热门科创城市（hot-city）整枝不动
-- 后续：必须再执行 L05（gkxlumenx_dim_region_scope_g20_city_l05.sql）复活城市并挂到国家下
--
-- 本脚本步骤 2 会暂时下线挂在 global-all 下的旧 g20-* 城市；L05 会改挂并重新激活。
-- 列/索引用 information_schema 探测，可重复执行。

-- 1) bind_country_code 列（幂等）
SET @db := 'gkxlumenx_dim';
SET @tbl := 'region_scope';
SET @col := 'bind_country_code';
SET @col_exists := (
  SELECT COUNT(*) FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = @db AND TABLE_NAME = @tbl AND COLUMN_NAME = @col
);
SET @sql := IF(
  @col_exists = 0,
  'ALTER TABLE `gkxlumenx_dim`.`region_scope` ADD COLUMN `bind_country_code` char(3) DEFAULT NULL COMMENT ''可选绑定 gkxlumenx_dim.code_country.country_code（ISO alpha-3）'' AFTER `bind_city_code`',
  'SELECT ''skip: bind_country_code already exists'' AS info'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 1b) 索引（幂等）
SET @idx := 'idx_region_scope_country';
SET @idx_exists := (
  SELECT COUNT(*) FROM information_schema.STATISTICS
  WHERE TABLE_SCHEMA = @db AND TABLE_NAME = @tbl AND INDEX_NAME = @idx
);
SET @sql := IF(
  @idx_exists = 0,
  'ALTER TABLE `gkxlumenx_dim`.`region_scope` ADD KEY `idx_region_scope_country` (`bind_country_code`)',
  'SELECT ''skip: idx_region_scope_country already exists'' AS info'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 2) 下线仍挂在 global-all 下的旧 G20 城市叶子（L05 改挂后本条件不再命中已迁城市）
UPDATE `gkxlumenx_dim`.`region_scope`
SET `is_active` = 0,
    `remark` = CONCAT(COALESCE(`remark`, ''), '；2026-08-11 下线：全球改 G20 国家')
WHERE `parent_code` = 'global-all'
  AND `scope_code` LIKE 'g20-%'
  AND `scope_code` NOT LIKE 'g20-c-%';

-- 3) 更新全球分组文案
UPDATE `gkxlumenx_dim`.`region_scope`
SET `scope_name` = 'G20 国家',
    `remark` = 'Q056：2020 主权国快照（含中俄；不含 EU）；子=国家 alpha-3；国家下城市见 L05',
    `bind_admin_code` = NULL,
    `bind_city_code` = NULL,
    `bind_country_code` = NULL
WHERE `scope_code` = 'global-all';

-- 4) 插入 / 激活 G20 国家（scope_code 用 g20-c-{alpha3}，避免与旧 g20-* 城市码冲突）
INSERT INTO `gkxlumenx_dim`.`region_scope`
  (`scope_code`, `parent_code`, `scope_name`, `node_kind`, `level`,
   `bind_admin_code`, `bind_city_code`, `bind_country_code`, `sort_order`, `is_active`, `remark`)
VALUES
  ('g20-c-arg', 'global-all', '阿根廷',     'country', 3, NULL, NULL, 'ARG', 10,  1, 'G20 2020'),
  ('g20-c-aus', 'global-all', '澳大利亚',   'country', 3, NULL, NULL, 'AUS', 20,  1, 'G20 2020'),
  ('g20-c-bra', 'global-all', '巴西',       'country', 3, NULL, NULL, 'BRA', 30,  1, 'G20 2020'),
  ('g20-c-can', 'global-all', '加拿大',     'country', 3, NULL, NULL, 'CAN', 40,  1, 'G20 2020'),
  ('g20-c-chn', 'global-all', '中国',       'country', 3, NULL, NULL, 'CHN', 50,  1, 'G20 2020'),
  ('g20-c-fra', 'global-all', '法国',       'country', 3, NULL, NULL, 'FRA', 60,  1, 'G20 2020'),
  ('g20-c-deu', 'global-all', '德国',       'country', 3, NULL, NULL, 'DEU', 70,  1, 'G20 2020'),
  ('g20-c-ind', 'global-all', '印度',       'country', 3, NULL, NULL, 'IND', 80,  1, 'G20 2020'),
  ('g20-c-idn', 'global-all', '印度尼西亚', 'country', 3, NULL, NULL, 'IDN', 90,  1, 'G20 2020'),
  ('g20-c-ita', 'global-all', '意大利',     'country', 3, NULL, NULL, 'ITA', 100, 1, 'G20 2020'),
  ('g20-c-jpn', 'global-all', '日本',       'country', 3, NULL, NULL, 'JPN', 110, 1, 'G20 2020'),
  ('g20-c-mex', 'global-all', '墨西哥',     'country', 3, NULL, NULL, 'MEX', 120, 1, 'G20 2020'),
  ('g20-c-rus', 'global-all', '俄罗斯',     'country', 3, NULL, NULL, 'RUS', 130, 1, 'G20 2020'),
  ('g20-c-sau', 'global-all', '沙特阿拉伯', 'country', 3, NULL, NULL, 'SAU', 140, 1, 'G20 2020'),
  ('g20-c-zaf', 'global-all', '南非',       'country', 3, NULL, NULL, 'ZAF', 150, 1, 'G20 2020'),
  ('g20-c-kor', 'global-all', '韩国',       'country', 3, NULL, NULL, 'KOR', 160, 1, 'G20 2020'),
  ('g20-c-tur', 'global-all', '土耳其',     'country', 3, NULL, NULL, 'TUR', 170, 1, 'G20 2020'),
  ('g20-c-gbr', 'global-all', '英国',       'country', 3, NULL, NULL, 'GBR', 180, 1, 'G20 2020'),
  ('g20-c-usa', 'global-all', '美国',       'country', 3, NULL, NULL, 'USA', 190, 1, 'G20 2020')
ON DUPLICATE KEY UPDATE
  `parent_code` = VALUES(`parent_code`),
  `scope_name` = VALUES(`scope_name`),
  `node_kind` = VALUES(`node_kind`),
  `level` = VALUES(`level`),
  `bind_admin_code` = NULL,
  `bind_city_code` = NULL,
  `bind_country_code` = VALUES(`bind_country_code`),
  `sort_order` = VALUES(`sort_order`),
  `is_active` = 1,
  `remark` = VALUES(`remark`);

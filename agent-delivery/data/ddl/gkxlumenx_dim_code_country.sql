-- 国家维表（ISO 3166-1）
-- 目标：MySQL gkxlumenx_dim.code_country
-- 任务：PY-ENT-REGION-SCOPE-G20-COUNTRY-L01
-- 口径：筛选 / Cascader / ES 主码 = alpha-3；alpha2 供 forg 等源表映射
-- 日期：2026-08-11

CREATE TABLE IF NOT EXISTS `gkxlumenx_dim`.`code_country` (
  `country_code` char(3) NOT NULL COMMENT 'ISO 3166-1 alpha-3（主码，如 CHN/USA/JPN）',
  `alpha2` char(2) NOT NULL COMMENT 'ISO 3166-1 alpha-2（如 CN/US/JP；forg.country_code 映射）',
  `name_zh` varchar(64) NOT NULL COMMENT '中文名',
  `name_en` varchar(128) NOT NULL COMMENT '英文名',
  `is_g20` tinyint NOT NULL DEFAULT 0 COMMENT '是否 2020 年 G20 主权国快照 0/1（不含 EU）',
  `sort_order` int NOT NULL DEFAULT 0 COMMENT '展示排序（升序）',
  `is_active` tinyint NOT NULL DEFAULT 1 COMMENT '是否启用 0/1',
  `remark` varchar(255) DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`country_code`),
  UNIQUE KEY `uk_code_country_alpha2` (`alpha2`),
  KEY `idx_code_country_g20` (`is_g20`, `is_active`, `sort_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
  COMMENT='国家维表 ISO 3166-1；region_scope.bind_country_code 引用';

-- G20 2020 主权国 19（含中俄；不含欧盟）
INSERT INTO `gkxlumenx_dim`.`code_country`
  (`country_code`, `alpha2`, `name_zh`, `name_en`, `is_g20`, `sort_order`, `is_active`, `remark`)
VALUES
  ('ARG', 'AR', '阿根廷',     'Argentina',      1, 10,  1, 'G20 2020'),
  ('AUS', 'AU', '澳大利亚',   'Australia',      1, 20,  1, 'G20 2020'),
  ('BRA', 'BR', '巴西',       'Brazil',         1, 30,  1, 'G20 2020'),
  ('CAN', 'CA', '加拿大',     'Canada',         1, 40,  1, 'G20 2020'),
  ('CHN', 'CN', '中国',       'China',          1, 50,  1, 'G20 2020'),
  ('FRA', 'FR', '法国',       'France',         1, 60,  1, 'G20 2020'),
  ('DEU', 'DE', '德国',       'Germany',        1, 70,  1, 'G20 2020'),
  ('IND', 'IN', '印度',       'India',          1, 80,  1, 'G20 2020'),
  ('IDN', 'ID', '印度尼西亚', 'Indonesia',      1, 90,  1, 'G20 2020'),
  ('ITA', 'IT', '意大利',     'Italy',          1, 100, 1, 'G20 2020'),
  ('JPN', 'JP', '日本',       'Japan',          1, 110, 1, 'G20 2020'),
  ('MEX', 'MX', '墨西哥',     'Mexico',         1, 120, 1, 'G20 2020'),
  ('RUS', 'RU', '俄罗斯',     'Russia',         1, 130, 1, 'G20 2020'),
  ('SAU', 'SA', '沙特阿拉伯', 'Saudi Arabia',   1, 140, 1, 'G20 2020'),
  ('ZAF', 'ZA', '南非',       'South Africa',   1, 150, 1, 'G20 2020'),
  ('KOR', 'KR', '韩国',       'South Korea',    1, 160, 1, 'G20 2020'),
  ('TUR', 'TR', '土耳其',     'Türkiye',        1, 170, 1, 'G20 2020'),
  ('GBR', 'GB', '英国',       'United Kingdom', 1, 180, 1, 'G20 2020；ISO=GBR 非 UK'),
  ('USA', 'US', '美国',       'United States',  1, 190, 1, 'G20 2020')
ON DUPLICATE KEY UPDATE
  `alpha2` = VALUES(`alpha2`),
  `name_zh` = VALUES(`name_zh`),
  `name_en` = VALUES(`name_en`),
  `is_g20` = VALUES(`is_g20`),
  `sort_order` = VALUES(`sort_order`),
  `is_active` = VALUES(`is_active`),
  `remark` = VALUES(`remark`);

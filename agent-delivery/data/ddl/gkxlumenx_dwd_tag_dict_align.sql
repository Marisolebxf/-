-- tag_dict 契约对齐（设计文档 vs 现网 vs meta.py）
-- 目标：MySQL gkxlumenx_dwd.tag_dict
-- 任务：DATA-ENT-DICT-CATALOG-L01（设计交付；本单不强制执行 ALTER）
-- 日期：2026-07-29
--
-- 现状（2026-07-29 实测）：
--   PK tag_code；列：tag_name / tag_category / description / create_time / update_time
--   行数 7：foreign/gazelle/high_tech/listed/little_giant/sme_tech/unicorn
--
-- meta.py 期望列：tag_level / is_active / sort_order，且 SQL 表名写 dwd_tag_dict（缺库前缀）
-- 设计文档（DWD §4.3）另含 ods_source
--
-- 建议：先 ALTER 对齐列；再补种子；Python 改查 gkxlumenx_dwd.tag_dict（follow-up L03）

-- 执行前请先 DESC / information_schema 确认列不存在，避免重复 ADD 报错。
ALTER TABLE `gkxlumenx_dwd`.`tag_dict`
  ADD COLUMN `tag_level` varchar(50) DEFAULT NULL
    COMMENT '标签级别 national/province/city/district；荣誉类适用' AFTER `tag_category`,
  ADD COLUMN `ods_source` varchar(255) DEFAULT NULL
    COMMENT 'ODS 来源表名' AFTER `tag_level`,
  ADD COLUMN `sort_order` int DEFAULT 0
    COMMENT '排序序号' AFTER `ods_source`,
  ADD COLUMN `is_active` tinyint NOT NULL DEFAULT 1
    COMMENT '是否启用 0/1' AFTER `sort_order`;

-- Wave0 补齐种子（与 mock._TAG_DICT / 设计预置对齐；不覆盖已有中文名除非空）
INSERT INTO `gkxlumenx_dwd`.`tag_dict`
  (`tag_code`, `tag_name`, `tag_category`, `tag_level`, `ods_source`, `sort_order`, `is_active`, `description`)
VALUES
  ('high_tech',        '高新技术企业', 'qualification', 'national',  NULL, 10, 1, '国高企'),
  ('little_giant',     '专精特新',     'qualification', 'national',  NULL, 20, 1, '专精特新'),
  ('little_giant_pro', '小巨人',       'qualification', 'national',  NULL, 25, 1, '专精特新小巨人'),
  ('gazelle',          '瞪羚企业',     'qualification', 'national',  NULL, 30, 1, NULL),
  ('unicorn',          '独角兽企业',   'qualification', 'national',  NULL, 40, 1, NULL),
  ('listed',           '上市企业',     'qualification', NULL,        NULL, 50, 1, NULL),
  ('sme',              '小微企业',     'scale',         NULL,        NULL, 60, 1, NULL),
  ('sme_tech',         '科技型中小企业','qualification', NULL,       NULL, 65, 1, NULL),
  ('foreign',          '外资企业',     'diy',           NULL,        NULL, 70, 1, '性质/外资'),
  ('honor_national',   '国家级荣誉',   'honor',         'national',  NULL, 80, 1, NULL),
  ('honor_province',   '省级荣誉',     'honor',         'province',  NULL, 90, 1, NULL),
  ('honor_city',       '市级荣誉',     'honor',         'city',      NULL, 100, 1, NULL),
  ('honor_district',   '区县级荣誉',   'honor',         'district',  NULL, 110, 1, NULL),
  ('certification',    '资质认证',     'qualification', NULL,        NULL, 120, 1, NULL),
  ('chain_leader',     '链主龙头',     'diy',           NULL,        NULL, 130, 1, NULL),
  ('key_enterprise',   '重点企业',     'diy',           NULL,        NULL, 140, 1, NULL),
  ('star_enterprise',  '明星企业',     'diy',           NULL,        NULL, 150, 1, NULL)
ON DUPLICATE KEY UPDATE
  `tag_name` = VALUES(`tag_name`),
  `tag_category` = VALUES(`tag_category`),
  `tag_level` = VALUES(`tag_level`),
  `sort_order` = VALUES(`sort_order`),
  `is_active` = VALUES(`is_active`);

-- DATA-ENT-DICT-REGION-SEED-L03
-- region_scope / region_scope_member / city：bind 校正 + Q056 热门/G20 Mock 扩种
-- 依赖：code_region 全量国标已灌入（见 gkxlumenx_dim_code_region_seed_l03.sql）
-- 日期：2026-07-29

-- 1) 校正既有 bind（含深圳区县国标码、南京补 bind）
UPDATE `gkxlumenx_dim`.`region_scope` SET `bind_admin_code`='320100', `bind_city_code`='CN-3201', `remark`='Q056 热门城市 Mock；bind 南京市' WHERE `scope_code`='nanjing';
UPDATE `gkxlumenx_dim`.`region_scope` SET `bind_admin_code`='440309', `remark`='国标 440309 龙华区' WHERE `scope_code`='longhua';
UPDATE `gkxlumenx_dim`.`region_scope` SET `bind_admin_code`='440311', `remark`='国标 440311 光明区' WHERE `scope_code`='guangming';
UPDATE `gkxlumenx_dim`.`region_scope` SET `bind_admin_code`='440310', `remark`='国标 440310 坪山区' WHERE `scope_code`='pingshan';
UPDATE `gkxlumenx_dim`.`region_scope` SET `bind_admin_code`='440307', `remark`='国标 440307 龙岗区' WHERE `scope_code`='longgang';
UPDATE `gkxlumenx_dim`.`region_scope` SET `bind_admin_code`='440308', `remark`='国标 440308 盐田区' WHERE `scope_code`='yantian';
UPDATE `gkxlumenx_dim`.`region_scope` SET `bind_admin_code`=NULL, `bind_city_code`=NULL, `remark`='大鹏新区非民政部县级码；过滤策略待运营确认' WHERE `scope_code`='dapeng';

-- 2) 热门科创城市 Mock 扩种
INSERT INTO `gkxlumenx_dim`.`region_scope`
  (`scope_code`, `parent_code`, `scope_name`, `node_kind`, `level`, `bind_admin_code`, `bind_city_code`, `sort_order`, `is_active`, `remark`)
VALUES
  ('xian',      'hot-city', '西安', 'scope', 2, '610100', 'CN-6101', 100, 1, 'Q056 热门城市 Mock 扩种'),
  ('hefei',     'hot-city', '合肥', 'scope', 2, '340100', 'CN-3401', 110, 1, 'Q056 热门城市 Mock 扩种'),
  ('changsha',  'hot-city', '长沙', 'scope', 2, '430100', 'CN-4301', 120, 1, 'Q056 热门城市 Mock 扩种'),
  ('qingdao',   'hot-city', '青岛', 'scope', 2, '370200', 'CN-3702', 130, 1, 'Q056 热门城市 Mock 扩种'),
  ('xiamen',    'hot-city', '厦门', 'scope', 2, '350200', 'CN-3502', 140, 1, 'Q056 热门城市 Mock 扩种'),
  ('tianjin',   'hot-city', '天津', 'scope', 2, '120000', 'CN-1200', 150, 1, 'Q056 热门城市 Mock 扩种'),
  ('chongqing', 'hot-city', '重庆', 'scope', 2, '500000', 'CN-5000', 160, 1, 'Q056 热门城市 Mock 扩种'),
  ('wuxi',      'hot-city', '无锡', 'scope', 2, '320200', 'CN-3202', 170, 1, 'Q056 热门城市 Mock 扩种'),
  ('ningbo',    'hot-city', '宁波', 'scope', 2, '330200', 'CN-3302', 180, 1, 'Q056 热门城市 Mock 扩种'),
  ('dongguan',  'hot-city', '东莞', 'scope', 2, '441900', 'CN-4419', 190, 1, 'Q056 热门城市 Mock 扩种')
ON DUPLICATE KEY UPDATE
  `scope_name`=VALUES(`scope_name`), `bind_admin_code`=VALUES(`bind_admin_code`),
  `bind_city_code`=VALUES(`bind_city_code`), `sort_order`=VALUES(`sort_order`),
  `remark`=VALUES(`remark`), `is_active`=1;

-- 3) G20 主要科创城市 Mock 扩种
INSERT INTO `gkxlumenx_dim`.`region_scope`
  (`scope_code`, `parent_code`, `scope_name`, `node_kind`, `level`, `bind_admin_code`, `bind_city_code`, `sort_order`, `is_active`, `remark`)
VALUES
  ('g20-osaka',         'global-all', '大阪',           'scope', 3, NULL, 'JP-OSA', 190, 1, 'G20 Mock JP'),
  ('g20-chicago',       'global-all', '芝加哥',         'scope', 3, NULL, 'US-CHI', 200, 1, 'G20 Mock US'),
  ('g20-la',            'global-all', '洛杉矶',         'scope', 3, NULL, 'US-LAX', 210, 1, 'G20 Mock US'),
  ('g20-milan',         'global-all', '米兰',           'scope', 3, NULL, 'IT-MIL', 220, 1, 'G20 Mock IT'),
  ('g20-rome',          'global-all', '罗马',           'scope', 3, NULL, 'IT-ROM', 230, 1, 'G20 Mock IT'),
  ('g20-moscow',        'global-all', '莫斯科',         'scope', 3, NULL, 'RU-MOW', 240, 1, 'G20 Mock RU'),
  ('g20-mexicocity',    'global-all', '墨西哥城',       'scope', 3, NULL, 'MX-MEX', 250, 1, 'G20 Mock MX'),
  ('g20-johannesburg',  'global-all', '约翰内斯堡',     'scope', 3, NULL, 'ZA-JNB', 260, 1, 'G20 Mock ZA'),
  ('g20-buenosaires',   'global-all', '布宜诺斯艾利斯', 'scope', 3, NULL, 'AR-BUE', 270, 1, 'G20 Mock AR'),
  ('g20-istanbul',      'global-all', '伊斯坦布尔',     'scope', 3, NULL, 'TR-IST', 280, 1, 'G20 Mock TR'),
  ('g20-jakarta',       'global-all', '雅加达',         'scope', 3, NULL, 'ID-JKT', 290, 1, 'G20 Mock ID'),
  ('g20-melbourne',     'global-all', '墨尔本',         'scope', 3, NULL, 'AU-MEL', 300, 1, 'G20 Mock AU')
ON DUPLICATE KEY UPDATE
  `scope_name`=VALUES(`scope_name`), `bind_city_code`=VALUES(`bind_city_code`),
  `sort_order`=VALUES(`sort_order`), `remark`=VALUES(`remark`), `is_active`=1;

-- 4) dim.city 扩种（热门 + G20）
INSERT INTO `gkxlumenx_dim`.`city`
  (`city_code`, `name_zh`, `name_en`, `country_code`, `admin_code`, `lng`, `lat`, `is_benchmark`)
VALUES
  ('CN-3201', '南京', 'Nanjing', 'CN', '320100', 118.796900, 32.060300, 1),
  ('CN-4301', '长沙', 'Changsha', 'CN', '430100', 112.938800, 28.228200, 1),
  ('CN-3702', '青岛', 'Qingdao', 'CN', '370200', 120.382600, 36.067100, 1),
  ('CN-3502', '厦门', 'Xiamen', 'CN', '350200', 118.089400, 24.479800, 1),
  ('CN-1200', '天津', 'Tianjin', 'CN', '120000', 117.201000, 39.084200, 1),
  ('CN-5000', '重庆', 'Chongqing', 'CN', '500000', 106.551600, 29.563000, 1),
  ('CN-3202', '无锡', 'Wuxi', 'CN', '320200', 120.311900, 31.491200, 0),
  ('CN-3302', '宁波', 'Ningbo', 'CN', '330200', 121.544000, 29.868300, 0),
  ('CN-4419', '东莞', 'Dongguan', 'CN', '441900', 113.746800, 23.046600, 1),
  ('JP-OSA', '大阪', 'Osaka', 'JP', NULL, 135.502300, 34.693700, 1),
  ('US-CHI', '芝加哥', 'Chicago', 'US', NULL, -87.629800, 41.878100, 1),
  ('US-LAX', '洛杉矶', 'Los Angeles', 'US', NULL, -118.243700, 34.052200, 1),
  ('IT-MIL', '米兰', 'Milan', 'IT', NULL, 9.190000, 45.464200, 1),
  ('IT-ROM', '罗马', 'Rome', 'IT', NULL, 12.496400, 41.902800, 0),
  ('RU-MOW', '莫斯科', 'Moscow', 'RU', NULL, 37.617300, 55.755800, 1),
  ('MX-MEX', '墨西哥城', 'Mexico City', 'MX', NULL, -99.133200, 19.432600, 1),
  ('ZA-JNB', '约翰内斯堡', 'Johannesburg', 'ZA', NULL, 28.047300, -26.204100, 1),
  ('AR-BUE', '布宜诺斯艾利斯', 'Buenos Aires', 'AR', NULL, -58.381600, -34.603700, 1),
  ('TR-IST', '伊斯坦布尔', 'Istanbul', 'TR', NULL, 28.978400, 41.008200, 1),
  ('ID-JKT', '雅加达', 'Jakarta', 'ID', NULL, 106.845600, -6.208800, 1),
  ('AU-MEL', '墨尔本', 'Melbourne', 'AU', NULL, 144.963100, -37.813600, 1)
ON DUPLICATE KEY UPDATE
  `name_zh`=VALUES(`name_zh`), `name_en`=VALUES(`name_en`),
  `country_code`=VALUES(`country_code`), `admin_code`=VALUES(`admin_code`),
  `lng`=VALUES(`lng`), `lat`=VALUES(`lat`), `is_benchmark`=VALUES(`is_benchmark`);

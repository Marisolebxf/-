-- region_scope：复活旧 G20 热门城市，挂到对应 g20-c-* 国家下
-- 任务：DATA-ENT-CODE-COUNTRY-APPLY-L01 / PY-ENT-REGION-SCOPE-G20-COUNTRY-L01（增量 L05）
-- 依赖：先执行 code_country.sql + L04（国家已在）
-- 日期：2026-08-11
-- 产品树：全球 → 国家 → 热门城市（~20+；含 L03 扩种城）
-- 禁止：L05 之后再跑 L03 §3（会把 bind_city_code 打回 JP-OSA 等连字符旧码）
--
-- 城市码口径（已定）：
--   * 海外：UN/LOCODE 五位紧凑码（ISO 3166-1 alpha-2 + 地点 3 位，无空格/连字符）
--           例 JPTYO / USNYC / GBLON；与国家 alpha-3 通过 code_country.alpha2 对齐
--   * 中国：筛码优先 bind_admin_code（6 位国标）；bind_city_code 沿用 dim.city 国内运营码 CN-*
--           （与「全国热门科创城市」共用，避免双 PK）
--   * 新加坡 g20-singapore：非 G20 2020 主权国 → 保持下线，不挂国家
--
-- 过滤语义（查询侧另单）：
--   选国家叶 → country_codes=[JPN]（整国，不 OR 样例城市）
--   选海外城市叶 → city_codes=[JPTYO]
--   选中国城市叶 → region_id via bind_admin_code

-- 1) dim.city：海外改为 UN/LOCODE 主键；国内 CN-* 不动
INSERT INTO `gkxlumenx_dim`.`city`
  (`city_code`, `name_zh`, `name_en`, `country_code`, `admin_code`, `lng`, `lat`, `is_benchmark`)
VALUES
  ('JPTYO', '东京',           'Tokyo',         'JP', NULL, 139.691700, 35.689500, 1),
  ('JPOSA', '大阪',           'Osaka',         'JP', NULL, 135.502300, 34.693700, 1),
  ('GBLON', '伦敦',           'London',        'GB', NULL, -0.127600, 51.507400, 1),
  ('USSFO', '旧金山',         'San Francisco', 'US', NULL, -122.419400, 37.774900, 1),
  ('USNYC', '纽约',           'New York',      'US', NULL, -74.006000, 40.712800, 1),
  ('USBOS', '波士顿',         'Boston',        'US', NULL, -71.058900, 42.360100, 1),
  ('USCHI', '芝加哥',         'Chicago',       'US', NULL, -87.629800, 41.878100, 1),
  ('USLAX', '洛杉矶',         'Los Angeles',   'US', NULL, -118.243700, 34.052200, 1),
  ('KRSEL', '首尔',           'Seoul',         'KR', NULL, 126.978000, 37.566500, 1),
  ('DEBER', '柏林',           'Berlin',        'DE', NULL, 13.405000, 52.520000, 1),
  ('DEMUC', '慕尼黑',         'Munich',        'DE', NULL, 11.582000, 48.135100, 1),
  ('FRPAR', '巴黎',           'Paris',         'FR', NULL, 2.352200, 48.856600, 1),
  ('CATOR', '多伦多',         'Toronto',       'CA', NULL, -79.383200, 43.653200, 1),
  ('AUSYD', '悉尼',           'Sydney',        'AU', NULL, 151.209300, -33.868800, 1),
  ('AUMEL', '墨尔本',         'Melbourne',     'AU', NULL, 144.963100, -37.813600, 1),
  ('INBLR', '班加罗尔',       'Bengaluru',     'IN', NULL, 77.594600, 12.971600, 1),
  ('BRSAO', '圣保罗',         'Sao Paulo',     'BR', NULL, -46.633300, -23.550500, 1),
  ('SARUH', '利雅得',         'Riyadh',        'SA', NULL, 46.675300, 24.713600, 0),
  ('ITMIL', '米兰',           'Milan',         'IT', NULL, 9.190000, 45.464200, 1),
  ('ITROM', '罗马',           'Rome',          'IT', NULL, 12.496400, 41.902800, 0),
  ('RUMOW', '莫斯科',         'Moscow',        'RU', NULL, 37.617300, 55.755800, 1),
  ('MXMEX', '墨西哥城',       'Mexico City',   'MX', NULL, -99.133200, 19.432600, 1),
  ('ZAJNB', '约翰内斯堡',     'Johannesburg',  'ZA', NULL, 28.047300, -26.204100, 1),
  ('ARBUE', '布宜诺斯艾利斯', 'Buenos Aires',  'AR', NULL, -58.381600, -34.603700, 1),
  ('TRIST', '伊斯坦布尔',     'Istanbul',      'TR', NULL, 28.978400, 41.008200, 1),
  ('IDJKT', '雅加达',         'Jakarta',       'ID', NULL, 106.845600, -6.208800, 1),
  ('SGSIN', '新加坡',         'Singapore',     'SG', NULL, 103.819800, 1.352100, 1)
ON DUPLICATE KEY UPDATE
  `name_zh` = VALUES(`name_zh`),
  `name_en` = VALUES(`name_en`),
  `country_code` = VALUES(`country_code`),
  `is_benchmark` = VALUES(`is_benchmark`);

-- 2) 旧连字符运营码（JP-TYO 等）行可保留不删；region_scope 改绑到 UN/LOCODE 后不再引用

-- 3) 复活并改挂：旧 g20-* 城市 → 对应 g20-c-*；level=4；海外 bind UN/LOCODE
INSERT INTO `gkxlumenx_dim`.`region_scope`
  (`scope_code`, `parent_code`, `scope_name`, `node_kind`, `level`,
   `bind_admin_code`, `bind_city_code`, `bind_country_code`, `sort_order`, `is_active`, `remark`)
VALUES
  -- CHN（国内筛码 = admin）
  ('g20-beijing',      'g20-c-chn', '北京',           'scope', 4, '110000', 'CN-1100', NULL, 10,  1, 'G20 热门城市；筛码 admin'),
  ('g20-shanghai',     'g20-c-chn', '上海',           'scope', 4, '310000', 'CN-3100', NULL, 20,  1, 'G20 热门城市；筛码 admin'),
  ('g20-shenzhen',     'g20-c-chn', '深圳',           'scope', 4, '440300', 'CN-4403', NULL, 30,  1, 'G20 热门城市；筛码 admin'),
  -- JPN
  ('g20-tokyo',        'g20-c-jpn', '东京',           'scope', 4, NULL, 'JPTYO', NULL, 10, 1, 'UN/LOCODE JPTYO'),
  ('g20-osaka',        'g20-c-jpn', '大阪',           'scope', 4, NULL, 'JPOSA', NULL, 20, 1, 'UN/LOCODE JPOSA'),
  -- GBR
  ('g20-london',       'g20-c-gbr', '伦敦',           'scope', 4, NULL, 'GBLON', NULL, 10, 1, 'UN/LOCODE GBLON'),
  -- USA
  ('g20-sfo',          'g20-c-usa', '旧金山',         'scope', 4, NULL, 'USSFO', NULL, 10, 1, 'UN/LOCODE USSFO'),
  ('g20-nyc',          'g20-c-usa', '纽约',           'scope', 4, NULL, 'USNYC', NULL, 20, 1, 'UN/LOCODE USNYC'),
  ('g20-boston',       'g20-c-usa', '波士顿',         'scope', 4, NULL, 'USBOS', NULL, 30, 1, 'UN/LOCODE USBOS'),
  ('g20-chicago',      'g20-c-usa', '芝加哥',         'scope', 4, NULL, 'USCHI', NULL, 40, 1, 'UN/LOCODE USCHI'),
  ('g20-la',           'g20-c-usa', '洛杉矶',         'scope', 4, NULL, 'USLAX', NULL, 50, 1, 'UN/LOCODE USLAX'),
  -- KOR / DEU / FRA / CAN / AUS / IND / BRA / SAU / ITA / RUS / MEX / ZAF / ARG / TUR / IDN
  ('g20-seoul',        'g20-c-kor', '首尔',           'scope', 4, NULL, 'KRSEL', NULL, 10, 1, 'UN/LOCODE KRSEL'),
  ('g20-berlin',       'g20-c-deu', '柏林',           'scope', 4, NULL, 'DEBER', NULL, 10, 1, 'UN/LOCODE DEBER'),
  ('g20-munich',       'g20-c-deu', '慕尼黑',         'scope', 4, NULL, 'DEMUC', NULL, 20, 1, 'UN/LOCODE DEMUC'),
  ('g20-paris',        'g20-c-fra', '巴黎',           'scope', 4, NULL, 'FRPAR', NULL, 10, 1, 'UN/LOCODE FRPAR'),
  ('g20-toronto',      'g20-c-can', '多伦多',         'scope', 4, NULL, 'CATOR', NULL, 10, 1, 'UN/LOCODE CATOR'),
  ('g20-sydney',       'g20-c-aus', '悉尼',           'scope', 4, NULL, 'AUSYD', NULL, 10, 1, 'UN/LOCODE AUSYD'),
  ('g20-melbourne',    'g20-c-aus', '墨尔本',         'scope', 4, NULL, 'AUMEL', NULL, 20, 1, 'UN/LOCODE AUMEL'),
  ('g20-bengaluru',    'g20-c-ind', '班加罗尔',       'scope', 4, NULL, 'INBLR', NULL, 10, 1, 'UN/LOCODE INBLR'),
  ('g20-saopaulo',     'g20-c-bra', '圣保罗',         'scope', 4, NULL, 'BRSAO', NULL, 10, 1, 'UN/LOCODE BRSAO'),
  ('g20-riyadh',       'g20-c-sau', '利雅得',         'scope', 4, NULL, 'SARUH', NULL, 10, 1, 'UN/LOCODE SARUH'),
  ('g20-milan',        'g20-c-ita', '米兰',           'scope', 4, NULL, 'ITMIL', NULL, 10, 1, 'UN/LOCODE ITMIL'),
  ('g20-rome',         'g20-c-ita', '罗马',           'scope', 4, NULL, 'ITROM', NULL, 20, 1, 'UN/LOCODE ITROM'),
  ('g20-moscow',       'g20-c-rus', '莫斯科',         'scope', 4, NULL, 'RUMOW', NULL, 10, 1, 'UN/LOCODE RUMOW'),
  ('g20-mexicocity',   'g20-c-mex', '墨西哥城',       'scope', 4, NULL, 'MXMEX', NULL, 10, 1, 'UN/LOCODE MXMEX'),
  ('g20-johannesburg', 'g20-c-zaf', '约翰内斯堡',     'scope', 4, NULL, 'ZAJNB', NULL, 10, 1, 'UN/LOCODE ZAJNB'),
  ('g20-buenosaires',  'g20-c-arg', '布宜诺斯艾利斯', 'scope', 4, NULL, 'ARBUE', NULL, 10, 1, 'UN/LOCODE ARBUE'),
  ('g20-istanbul',     'g20-c-tur', '伊斯坦布尔',     'scope', 4, NULL, 'TRIST', NULL, 10, 1, 'UN/LOCODE TRIST'),
  ('g20-jakarta',      'g20-c-idn', '雅加达',         'scope', 4, NULL, 'IDJKT', NULL, 10, 1, 'UN/LOCODE IDJKT')
ON DUPLICATE KEY UPDATE
  `parent_code` = VALUES(`parent_code`),
  `scope_name` = VALUES(`scope_name`),
  `node_kind` = VALUES(`node_kind`),
  `level` = VALUES(`level`),
  `bind_admin_code` = VALUES(`bind_admin_code`),
  `bind_city_code` = VALUES(`bind_city_code`),
  `bind_country_code` = NULL,
  `sort_order` = VALUES(`sort_order`),
  `is_active` = 1,
  `remark` = VALUES(`remark`);

-- 4) 新加坡：非 G20 → 明确下线（若 L04 已下线则强化备注）
UPDATE `gkxlumenx_dim`.`region_scope`
SET `is_active` = 0,
    `parent_code` = 'global-all',
    `remark` = '非 G20 2020 主权国；不下挂国家；保留历史行'
WHERE `scope_code` = 'g20-singapore';

-- 5) 全球分组文案：国家下可挂城市样例
UPDATE `gkxlumenx_dim`.`region_scope`
SET `scope_name` = 'G20 国家',
    `remark` = 'Q056：2020 主权国；子=国家(alpha-3)；国家下挂热门城市样例（海外 UN/LOCODE）'
WHERE `scope_code` = 'global-all';

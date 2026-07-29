-- 运营地域字典（结果区地域级联：全球/全国/区域/热门科创城市 + 深圳区县）
-- 目标：MySQL gkxlumenx_dim.region_scope (+ region_scope_member)
-- 用途：ResultToolbar / RegionSelect；与国标树 code_region、innov admin_division 物理分表
-- 任务：DATA-ENT-DICT-CATALOG-L01
-- 日期：2026-07-29
-- 注意：本文件仅 DDL + Wave0 样例种子；复合区域法定边界待甲方确认（Q056）

CREATE TABLE IF NOT EXISTS `gkxlumenx_dim`.`region_scope` (
  `scope_code` varchar(64) NOT NULL COMMENT '运营地域编码（如 global / jjj / shenzhen / nanshan）',
  `parent_code` varchar(64) NOT NULL DEFAULT '' COMMENT '父级编码；顶级为空串',
  `scope_name` varchar(128) NOT NULL COMMENT '展示名',
  `node_kind` varchar(16) NOT NULL COMMENT '节点类型：level | scope | district',
  `level` tinyint NOT NULL COMMENT '层级：1=一级（全球/全国/区域/热门） 2=范围项 3=区县',
  `bind_admin_code` varchar(20) DEFAULT NULL COMMENT '可选绑定 gkxlumenx_dim.code_region.code',
  `bind_city_code` varchar(20) DEFAULT NULL COMMENT '可选绑定 gkxlumenx_dim.city.city_code',
  `sort_order` int NOT NULL DEFAULT 0 COMMENT '同级排序（升序）',
  `is_active` tinyint NOT NULL DEFAULT 1 COMMENT '是否启用 0/1',
  `remark` varchar(255) DEFAULT NULL COMMENT '备注（含待确认口径提示）',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`scope_code`),
  KEY `idx_region_scope_parent` (`parent_code`),
  KEY `idx_region_scope_kind` (`node_kind`, `is_active`),
  KEY `idx_region_scope_admin` (`bind_admin_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
  COMMENT='运营地域字典（结果区级联；非国标省市区树）';

CREATE TABLE IF NOT EXISTS `gkxlumenx_dim`.`region_scope_member` (
  `scope_code` varchar(64) NOT NULL COMMENT '复合区域编码（jjj / yrd / gba 等）',
  `admin_code` varchar(20) NOT NULL COMMENT '成员行政区划码（语义对齐 code_region.code）',
  `sort_order` int NOT NULL DEFAULT 0,
  PRIMARY KEY (`scope_code`, `admin_code`),
  KEY `idx_rsm_admin` (`admin_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
  COMMENT='运营复合区域→行政区划成员（京津冀/长三角/大湾区等；边界待甲方确认）';

-- ---------------------------------------------------------------------------
-- Wave0 样例种子（对齐 lumen-ui-topic regionOptions.ts；可幂等重跑需先清本批）
-- ---------------------------------------------------------------------------

INSERT INTO `gkxlumenx_dim`.`region_scope`
  (`scope_code`, `parent_code`, `scope_name`, `node_kind`, `level`, `bind_admin_code`, `bind_city_code`, `sort_order`, `is_active`, `remark`)
VALUES
  -- level
  ('global',    '', '全球',               'level', 1, NULL, NULL, 10, 1, NULL),
  ('national',  '', '全国',               'level', 1, '100000', NULL, 20, 1, 'bind 中国根节点 code_region'),
  ('regional',  '', '区域',               'level', 1, NULL, NULL, 30, 1, '复合区域见 region_scope_member；Q056🟢 法定边界初始化后运营可改'),
  ('hot-city',  '', '全国热门科创城市',   'level', 1, NULL, NULL, 40, 1, 'Q056🟢 运营可维护；需 Mock 数据'),
  -- scope under global / national
  ('global-all','global',   '全球主要科创网络样本', 'scope', 2, NULL, NULL, 10, 1, 'Q056🟢 = G20 国家主要科创城市；Mock 扩种 dim.city'),
  ('china-all', 'national', '全国',               'scope', 2, '100000', NULL, 10, 1, NULL),
  -- regional packages
  ('jjj', 'regional', '京津冀', 'scope', 2, NULL, NULL, 10, 1, 'Q056🟢 法定边界初始化；成员见 region_scope_member；运营可改'),
  ('yrd', 'regional', '长三角', 'scope', 2, NULL, NULL, 20, 1, 'Q056🟢 法定边界初始化；成员见 region_scope_member；运营可改'),
  ('gba', 'regional', '大湾区', 'scope', 2, NULL, NULL, 30, 1, 'Q056🟢 法定边界初始化；成员见 region_scope_member；运营可改'),
  -- hot cities（城市码对齐 dim.city / code_region 样例）
  ('beijing',   'hot-city', '北京', 'scope', 2, '110000', 'CN-1100', 10, 1, 'Q056 热门城市 Mock 名单之一'),
  ('shanghai',  'hot-city', '上海', 'scope', 2, '310000', 'CN-3100', 20, 1, NULL),
  ('guangzhou', 'hot-city', '广州', 'scope', 2, '440100', 'CN-4401', 30, 1, NULL),
  ('shenzhen',  'hot-city', '深圳', 'scope', 2, '440300', 'CN-4403', 40, 1, '可再挂 district 子节点'),
  ('hangzhou',  'hot-city', '杭州', 'scope', 2, '330100', 'CN-3301', 50, 1, NULL),
  ('suzhou',    'hot-city', '苏州', 'scope', 2, '320500', 'CN-3205', 60, 1, NULL),
  ('nanjing',   'hot-city', '南京', 'scope', 2, NULL, NULL, 70, 1, 'code_region 样例暂无；全量灌数后补 bind'),
  ('wuhan',     'hot-city', '武汉', 'scope', 2, '420100', 'CN-4201', 80, 1, NULL),
  ('chengdu',   'hot-city', '成都', 'scope', 2, '510100', 'CN-5101', 90, 1, NULL),
  -- shenzhen districts（运营 slug；bind 国标区划码，样例库可能尚无区县行）
  ('sz-all',     'shenzhen', '全部',     'district', 3, '440300', 'CN-4403', 0, 1, '选「全部」时等同市本级'),
  ('nanshan',    'shenzhen', '南山区',   'district', 3, '440305', NULL, 10, 1, NULL),
  ('futian',     'shenzhen', '福田区',   'district', 3, '440304', NULL, 20, 1, NULL),
  ('luohu',      'shenzhen', '罗湖区',   'district', 3, '440303', NULL, 30, 1, NULL),
  ('baoan',      'shenzhen', '宝安区',   'district', 3, '440306', NULL, 40, 1, NULL),
  ('longgang',   'shenzhen', '龙岗区',   'district', 3, '440307', NULL, 50, 1, NULL),
  ('longhua',    'shenzhen', '龙华区',   'district', 3, '440309', NULL, 60, 1, '区划码以国标灌数为准，Wave0 暂估'),
  ('guangming',  'shenzhen', '光明区',   'district', 3, '440311', NULL, 70, 1, '区划码以国标灌数为准，Wave0 暂估'),
  ('pingshan',   'shenzhen', '坪山区',   'district', 3, '440310', NULL, 80, 1, '区划码以国标灌数为准，Wave0 暂估'),
  ('yantian',    'shenzhen', '盐田区',   'district', 3, '440308', NULL, 90, 1, NULL),
  ('dapeng',     'shenzhen', '大鹏新区', 'district', 3, NULL, NULL, 100, 1, '新区非标准区划码；过滤策略待确认')
ON DUPLICATE KEY UPDATE
  `scope_name` = VALUES(`scope_name`),
  `parent_code` = VALUES(`parent_code`),
  `node_kind` = VALUES(`node_kind`),
  `level` = VALUES(`level`),
  `bind_admin_code` = VALUES(`bind_admin_code`),
  `bind_city_code` = VALUES(`bind_city_code`),
  `sort_order` = VALUES(`sort_order`),
  `is_active` = VALUES(`is_active`),
  `remark` = VALUES(`remark`);

-- 复合区域成员（Q056🟢：按法定边界初始化后运营可改；Wave0 为常用省/市包种子）
INSERT INTO `gkxlumenx_dim`.`region_scope_member` (`scope_code`, `admin_code`, `sort_order`)
VALUES
  ('jjj', '110000', 10),  -- 北京
  ('jjj', '120000', 20),  -- 天津（样例库可能暂无）
  ('jjj', '130000', 30),  -- 河北（样例库可能暂无）
  ('yrd', '310000', 10),  -- 上海
  ('yrd', '320000', 20),  -- 江苏
  ('yrd', '330000', 30),  -- 浙江
  ('yrd', '340000', 40),  -- 安徽（以法定清单为准；运营可调整）
  ('gba', '440100', 10),  -- 广州
  ('gba', '440300', 20),  -- 深圳
  ('gba', '440600', 30),  -- 佛山（样例可能暂无）
  ('gba', '441900', 40)   -- 东莞（样例可能暂无）
ON DUPLICATE KEY UPDATE `sort_order` = VALUES(`sort_order`);

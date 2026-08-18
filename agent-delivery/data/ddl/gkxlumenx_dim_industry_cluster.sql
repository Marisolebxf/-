-- 产业集群展示目录 + L0 映射
-- 先 USE 目标库：正式 gkxlumenx_dim；Demo demo_gkxlumenx_dim（结构+种子相同）
-- 编码/种子真源：stores/mysql/dim-industry-cluster.md §3/§4
-- 任务：CHAIN-INDUSTRY-CLUSTER-SUPP-L01 波次 B
-- 口径：Q068 🟡；政策版 sz-10+5-2026
-- 禁止：改 industry_chain；写入 gkxlumenx_cfg；复活 CH00x
-- 用法：USE `gkxlumenx_dim`; SOURCE 本文件;  （Demo 换 USE）

CREATE TABLE IF NOT EXISTS `industry_cluster` (
  `cluster_id` varchar(16) NOT NULL COMMENT '集群编码 CL-SEI-01~10 / CL-FUT-01~05',
  `cluster_group` varchar(8) NOT NULL COMMENT 'sei=战新 fut=未来',
  `cluster_name` varchar(64) NOT NULL COMMENT '对外展示名',
  `display_hint` varchar(128) DEFAULT NULL COMMENT '括号说明，不另编码',
  `policy_version` varchar(32) NOT NULL DEFAULT 'sz-10+5-2026' COMMENT '政策版；换版另开行集',
  `sort_order` int NOT NULL DEFAULT 0 COMMENT '先 10 战新再 5 未来',
  `is_active` tinyint NOT NULL DEFAULT 1 COMMENT '0/1；本轮 15 行全开',
  `remark` varchar(255) DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`cluster_id`),
  KEY `idx_cluster_group_sort` (`cluster_group`, `sort_order`, `is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
  COMMENT='产业集群展示目录（15；非 DWD、非国标 NIC）';

CREATE TABLE IF NOT EXISTS `industry_cluster_map` (
  `cluster_id` varchar(16) NOT NULL COMMENT 'industry_cluster.cluster_id',
  `industry_id` varchar(32) NOT NULL COMMENT 'L0 industry_id（INB，Q053）',
  `industry_name` varchar(64) NOT NULL COMMENT 'L0 展示名快照；改映射时重写',
  `map_status` varchar(24) NOT NULL DEFAULT 'mapped' COMMENT 'mapped | pending_vendor（pending 不占行，见集群 remark）',
  `sort_order` int NOT NULL DEFAULT 0,
  `is_active` tinyint NOT NULL DEFAULT 1,
  `remark` varchar(255) DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`cluster_id`, `industry_id`),
  UNIQUE KEY `uk_cluster_map_l0` (`industry_id`),
  KEY `idx_cluster_map_active` (`cluster_id`, `is_active`, `sort_order`),
  CONSTRAINT `fk_cluster_map_cluster` FOREIGN KEY (`cluster_id`) REFERENCES `industry_cluster` (`cluster_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
  COMMENT='集群 1:N → L0；本轮同一 L0 只挂一个集群';

-- ---------------------------------------------------------------------------
-- 种子：15 集群 + 15 条 L0（与 dim-industry-cluster.md §3/§4 逐字对齐）
-- L0 对齐 demo_gkxlumenx_dwd.industry_chain 3.0（INB17xx / INB18xx）；本轮不挂 L1
-- 正式库若仍为 Step2 旧 INB13xx，不要对本 map 段 SOURCE 覆盖 gkxlumenx_dim
-- ---------------------------------------------------------------------------

INSERT INTO `industry_cluster`
  (`cluster_id`, `cluster_group`, `cluster_name`, `display_hint`, `policy_version`, `sort_order`, `is_active`, `remark`)
VALUES
  ('CL-SEI-01', 'sei', '新一代信息技术',     NULL, 'sz-10+5-2026', 10, 1, NULL),
  ('CL-SEI-02', 'sei', '生物产业',           NULL, 'sz-10+5-2026', 20, 1, NULL),
  ('CL-SEI-03', 'sei', '新能源',             NULL, 'sz-10+5-2026', 30, 1, NULL),
  ('CL-SEI-04', 'sei', '新材料',             NULL, 'sz-10+5-2026', 40, 1, NULL),
  ('CL-SEI-05', 'sei', '高端装备',           NULL, 'sz-10+5-2026', 50, 1, NULL),
  ('CL-SEI-06', 'sei', '智能网联新能源汽车', NULL, 'sz-10+5-2026', 60, 1, NULL),
  ('CL-SEI-07', 'sei', '绿色环保',           NULL, 'sz-10+5-2026', 70, 1, NULL),
  ('CL-SEI-08', 'sei', '低空经济与空天',     NULL, 'sz-10+5-2026', 80, 1, NULL),
  ('CL-SEI-09', 'sei', '传统与创意产业',     NULL, 'sz-10+5-2026', 90, 1, NULL),
  ('CL-SEI-10', 'sei', '海洋产业',           NULL, 'sz-10+5-2026', 100, 1, NULL),
  ('CL-FUT-01', 'fut', '未来制造',           '智能机器人', 'sz-10+5-2026', 110, 1, NULL),
  ('CL-FUT-02', 'fut', '未来信息',           '光载信息、AI 底层生态', 'sz-10+5-2026', 120, 1, NULL),
  ('CL-FUT-03', 'fut', '未来能源',           NULL, 'sz-10+5-2026', 130, 1, NULL),
  ('CL-FUT-04', 'fut', '未来空间',           NULL, 'sz-10+5-2026', 140, 1, NULL),
  ('CL-FUT-05', 'fut', '未来健康',           '合成生物、细胞基因、脑机工程', 'sz-10+5-2026', 150, 1, NULL);

INSERT INTO `industry_cluster_map`
  (`cluster_id`, `industry_id`, `industry_name`, `map_status`, `sort_order`, `is_active`, `remark`)
VALUES
  ('CL-SEI-01', 'INB1701', '新一代信息技术',         'mapped', 10, 1, NULL),
  ('CL-SEI-02', 'INB1702', '生物',                   'mapped', 10, 1, NULL),
  ('CL-SEI-03', 'INB1703', '新能源',                 'mapped', 10, 1, NULL),
  ('CL-SEI-04', 'INB1704', '新材料',                 'mapped', 10, 1, NULL),
  ('CL-SEI-05', 'INB1705', '高端装备',               'mapped', 10, 1, NULL),
  ('CL-SEI-06', 'INB1706', '智能网联新能源汽车',     'mapped', 10, 1, NULL),
  ('CL-SEI-07', 'INB1707', '绿色环保',               'mapped', 10, 1, NULL),
  ('CL-SEI-08', 'INB1708', '低空经济与空天',         'mapped', 10, 1, NULL),
  ('CL-SEI-09', 'INB1709', '传统与创意',             'mapped', 10, 1, NULL),
  ('CL-SEI-10', 'INB1710', '海洋',                   'mapped', 10, 1, NULL),
  ('CL-FUT-01', 'INB1801', '未来制造',               'mapped', 10, 1, NULL),
  ('CL-FUT-02', 'INB1802', '未来信息',               'mapped', 10, 1, NULL),
  ('CL-FUT-03', 'INB1803', '未来能源',               'mapped', 10, 1, NULL),
  ('CL-FUT-04', 'INB1804', '未来空间',               'mapped', 10, 1, NULL),
  ('CL-FUT-05', 'INB1805', '未来健康',               'mapped', 10, 1, NULL);

-- 自检：cluster=15；map=15；industry_id 互斥。

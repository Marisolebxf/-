-- =====================================================================
-- 批 4 冻结 §7-6 · 订阅推送四类资源池（report/project/policy/carrier）
-- 目标库：gkxlumenx_ads（与 ts_plan_* 表族同库，池读取走同一 ADS 只读连接）
-- 冻结依据：TS-L2-DS09-OV-API §7 批 4 变更清单 #6（records[].reason 表行携带）
--          + PlanningResourcePoolReader 行形状约定（resource_id/title/field，可空列可扩展）
-- 行形状：resource_id / title / field（可空）/ reason（批 4 §7-6 表行携带推荐理由）
-- 属性：D18 展示 ADS 只读源；种子行为 demo 冻结种子逐字（talent 不入池，F6 裁定）
-- 消费：gkxlumen.display.planning.push-pools 配置下发（Nacos），
--       适配器 PlanningResourceSubscriptionAdapter 逐池取数 + 领域过滤
-- =====================================================================

CREATE TABLE IF NOT EXISTS `ts_plan_push_pool` (
  `resource_type` VARCHAR(16)  NOT NULL COMMENT 'report/project/policy/carrier（四类池；talent 不入池 F6）',
  `resource_id`   VARCHAR(128) NOT NULL COMMENT '资源对象ID（推送产物行快照键）',
  `title`         VARCHAR(255) NOT NULL COMMENT '资源标题（demo 冻结种子逐字）',
  `field`         VARCHAR(64)  DEFAULT NULL COMMENT '所属领域（订阅领域匹配列，包含语义）',
  `reason`        VARCHAR(255) DEFAULT NULL COMMENT '推荐理由（批 4 §7-6：表行携带，适配器透传到推送产物行）',
  `sort_no`       INT          NOT NULL DEFAULT 0 COMMENT '池内展示序',
  `source`        VARCHAR(32)  NOT NULL DEFAULT 'demo_seed' COMMENT '来源标注（lumen_seed 惯例）',
  `created_at`    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`resource_type`, `resource_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
  COMMENT='规划·科创资源订阅推送池（批 4 冻结；池=ADS 只读源，行形状 resource_id/title/field/reason）';

-- demo 冻结种子 4 行（talent 行不迁移：F6「核心人才不在四类资源池，是否入池待 M0/产品拍板」）
INSERT INTO `ts_plan_push_pool` (`resource_type`, `resource_id`, `title`, `field`, `reason`, `sort_no`, `source`)
VALUES
  ('policy',   'POL-SZ-AI-2026',  '深圳市关于加快人工智能产业创新发展的若干措施', '人工智能大模型', '提供算力、数据开放和场景供给支撑', 1, 'demo_seed'),
  ('project',  'PRJ-QUANTUM-2026', '国家重点研发计划“量子信息前沿研究”重点专项', '量子计算、量子通信', '支撑量子计算关键技术攻关', 2, 'demo_seed'),
  ('report',   'RPT-SYNBIO-2025', '2025全球合成生物学产业发展白皮书', '合成生物学、生物制造', '系统梳理产业链与标准趋势', 3, 'demo_seed'),
  ('carrier',  'CAR-SZ-LAB-2026', '深圳湾实验室、鹏城实验室等重点创新载体资源', '新一代信息技术全领域', '高能级载体资源开放，可联合攻关关键技术', 4, 'demo_seed')
ON DUPLICATE KEY UPDATE
  `title` = VALUES(`title`), `field` = VALUES(`field`), `reason` = VALUES(`reason`),
  `sort_no` = VALUES(`sort_no`), `source` = VALUES(`source`);

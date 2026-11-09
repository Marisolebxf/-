-- =====================================================================
-- TS-L2-DS09-SEED-L01 · 订阅产物表 sys_user_planning_push_record
-- 目标库：gkxlumenx（upms 主库，随 db/9x_gkxlumenx_user_behavior.sql 用户行为家族）
-- 冻结真源：sdd/l2/TS-L2-DS09-OV-DATA.md §5（A3 会签裁定 v2）
-- 属性：订阅面真实现产物（非 D18 表、非 gapfill）；初始 0 行（真实推送产生，无灌数）——
--       本脚本对其只建表，不 TRUNCATE、不 INSERT。
-- =====================================================================

CREATE TABLE sys_user_planning_push_record (
  id            bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  tenant_id     bigint unsigned NOT NULL DEFAULT 0 COMMENT '租户ID（统一用户中心下发，对齐 sys_user_relation）',
  user_id       bigint unsigned NOT NULL DEFAULT 0 COMMENT '用户ID（统一用户中心 SSO userId，非 sys_user.user_id，同 9x 惯例）',
  resource_type varchar(16)  NOT NULL COMMENT 'report/project/policy/carrier（四类资源池，ARCH §4.6；值域见 F6 映射）',
  resource_id   varchar(128) NOT NULL COMMENT '资源对象ID（字符串兼容混杂 ID 形态，对齐 sys_user_relation.target_id 惯例）',
  title         varchar(255) NOT NULL COMMENT '资源标题快照（列表直显，避免回表）',
  field         varchar(64)  DEFAULT NULL COMMENT '命中领域（订阅规则领域）',
  reason        varchar(255) DEFAULT NULL COMMENT '推送理由（适配器产出文案）',
  pushed_at     datetime     NOT NULL COMMENT '推送时间（契约 §3.6 pushed_at）',
  is_read       char(1)      NOT NULL DEFAULT '0' COMMENT '0未读 1已读（复用 M4 §3.4 已读模式，按用户隔离；映射契约 is_read 布尔）',
  create_time   datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  update_time   datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (id),
  KEY idx_user_read (tenant_id, user_id, is_read, pushed_at) COMMENT '过滤分页：按用户+已读+推送时间',
  KEY idx_user_type (user_id, resource_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='规划·科创资源推送产物记录（订阅面真实现产物，A3 裁定；初始零行，非 D18 表非 gapfill）';

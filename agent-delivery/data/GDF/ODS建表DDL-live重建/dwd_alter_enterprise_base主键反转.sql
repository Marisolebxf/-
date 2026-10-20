-- ============================================================
-- enterprise_base 主键反转 ALTER（2026-10-20 拍板 human:徐滕强）
-- 拍板：主键回归 id，org_id 改唯一键（推翻 10-12 org_id 主键方案）
-- 范围：正式库 gkxlumenx_dwd（demo 库 demo_gkxlumenx_dwd 由本侧另单同步，语句相同）
-- 前置检查：当前 PRIMARY=org_id、uk_enterprise_base_id(id)（2026-10-20 实测确认）
-- 执行人：人工审核后执行（延续 AI 生成/人工执行模式）
-- 风险说明：表当前 189,115 行；org_id 无重复（uk 语义已保证），反转安全；
--           DROP PRIMARY KEY + ADD UNIQUE 原子性由单条 ALTER 保证
-- ============================================================

USE gkxlumenx_dwd;

-- 1. 主键 org_id → id；org_id 降为唯一键
ALTER TABLE `enterprise_base`
  DROP PRIMARY KEY,
  DROP INDEX `uk_enterprise_base_id`,
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uk_enterprise_base_org_id` (`org_id`);

-- 执行后验证：
-- SHOW INDEX FROM gkxlumenx_dwd.enterprise_base WHERE Key_name IN ('PRIMARY','uk_enterprise_base_org_id');
-- 期望：PRIMARY=id；uk_enterprise_base_org_id=org_id；无 uk_enterprise_base_id 残留

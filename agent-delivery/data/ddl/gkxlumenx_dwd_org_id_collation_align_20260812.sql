-- DWD 企业关联键 collation 对齐（2026-08-12）
-- 目标：风险表 / 风险汇总的 org_id 与 enterprise_base.org_id
--       统一为 utf8mb4_general_ci，避免跨表 JOIN 报 MySQL 1267。
-- 说明：仅修改 VARCHAR(64) org_id 的比较规则，不修改字符内容。

USE gkxlumenx_dwd;

ALTER TABLE enterprise_risk_summary
  MODIFY org_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL;

ALTER TABLE risk_abnormal
  MODIFY org_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL;
ALTER TABLE risk_bankruptcy_party
  MODIFY org_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL;
ALTER TABLE risk_chattel_mortgage
  MODIFY org_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL;
ALTER TABLE risk_court_announcement_party
  MODIFY org_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL;
ALTER TABLE risk_court_filed_party
  MODIFY org_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL;
ALTER TABLE risk_court_notice_party
  MODIFY org_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL;
ALTER TABLE risk_dishonest
  MODIFY org_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL;
ALTER TABLE risk_equity_freeze
  MODIFY org_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL;
ALTER TABLE risk_equity_pledge
  MODIFY org_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL;
ALTER TABLE risk_executed
  MODIFY org_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL;
ALTER TABLE risk_illegal
  MODIFY org_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL;
ALTER TABLE risk_judicial_case
  MODIFY org_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL;
ALTER TABLE risk_judicial_sale_party
  MODIFY org_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL;
ALTER TABLE risk_lawsuit_party
  MODIFY org_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL;
ALTER TABLE risk_limit_high
  MODIFY org_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL;
ALTER TABLE risk_punishment
  MODIFY org_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL;
ALTER TABLE risk_tax_punish
  MODIFY org_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL;
ALTER TABLE risk_zhongben
  MODIFY org_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL;

-- enterprise_industry_chain.org_id 已是 utf8mb4_general_ci 且按确认保持可空。

SELECT TABLE_NAME, COLUMN_TYPE, IS_NULLABLE, COLLATION_NAME
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = DATABASE()
  AND COLUMN_NAME = 'org_id'
  AND (
    TABLE_NAME = 'enterprise_risk_summary'
    OR (
      TABLE_NAME LIKE 'risk_%'
      AND TABLE_NAME NOT LIKE '%__pre_%'
      AND TABLE_NAME NOT LIKE '%__raw_%'
    )
  )
ORDER BY TABLE_NAME;

-- JOIN smoke：执行成功即说明不再出现 Illegal mix of collations。
SELECT COUNT(*) AS mapped_summary_rows
FROM enterprise_risk_summary s
JOIN enterprise_base b ON b.org_id = s.org_id;

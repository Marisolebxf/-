-- 企业 DWD 结构对齐（2026-08-12）
-- 目标：将 2026-08-11 误灌入 DWD 的 ODS 原始结构转换为正式 DWD 契约。
-- 注意：
--   1. 本脚本仅适用于已完成的 2026-08-12 前置审计，不可重复执行。
--   2. 有数据原表均通过 RENAME 保留为 __pre_fix_20260812 / __raw_u200b_20260812。
--   3. risk_bankruptcy_party 仅迁移能关联主表的数据；孤儿与重复原始行保留在备份表。
--   4. enterprise_industry_chain.org_id 无权威映射，只新增可空列与索引，不生成假 ID。
--   5. enterprise_financing 的现行字段被 ETL/统计/种子任务直接使用，本次不改表。

USE gkxlumenx_dwd;

-- ---------------------------------------------------------------------------
-- A. 前置检查（执行结果必须与审计值一致）
-- ---------------------------------------------------------------------------

SELECT TABLE_NAME, HEX(TABLE_NAME) AS name_hex, TABLE_ROWS
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = DATABASE()
  AND (
    TABLE_NAME IN (
      'enterprise_risk_summary',
      'enterprise_base2',
      'enterprise_industry_chain',
      'enterprise_financing',
      'risk_abnormal',
      'risk_punishment',
      'risk_illegal',
      'risk_tax_punish',
      'risk_bankruptcy_party'
    )
    OR HEX(TABLE_NAME) LIKE '%E2808B'
  )
ORDER BY TABLE_NAME;

-- 备份名和暂存名必须不存在。
SELECT TABLE_NAME
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = DATABASE()
  AND (
    TABLE_NAME LIKE '%__pre_fix_20260812'
    OR TABLE_NAME LIKE '%__raw_u200b_20260812'
    OR TABLE_NAME LIKE '%__v31fix'
  );

SET @raw_judicial = (
  SELECT TABLE_NAME
  FROM information_schema.TABLES
  WHERE TABLE_SCHEMA = DATABASE()
    AND HEX(TABLE_NAME) = '7269736B5F6A7564696369616C5F63617365E2808B'
);
SET @raw_executed = (
  SELECT TABLE_NAME
  FROM information_schema.TABLES
  WHERE TABLE_SCHEMA = DATABASE()
    AND HEX(TABLE_NAME) = '7269736B5F6578656375746564E2808B'
);
SET @raw_bankruptcy = (
  SELECT TABLE_NAME
  FROM information_schema.TABLES
  WHERE TABLE_SCHEMA = DATABASE()
    AND HEX(TABLE_NAME) = '7269736B5F62616E6B727570746379E2808B'
);
SET @raw_dishonest = (
  SELECT TABLE_NAME
  FROM information_schema.TABLES
  WHERE TABLE_SCHEMA = DATABASE()
    AND HEX(TABLE_NAME) = '7269736B5F646973686F6E657374E2808B'
);

-- ---------------------------------------------------------------------------
-- B. 创建规范暂存表
-- ---------------------------------------------------------------------------

CREATE TABLE risk_judicial_case__v31fix (
  id BIGINT NOT NULL AUTO_INCREMENT,
  org_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  org_name VARCHAR(255) NULL,
  case_id VARCHAR(64) NOT NULL,
  case_no VARCHAR(255) NULL,
  case_title VARCHAR(500) NULL,
  case_type_tag VARCHAR(100) NULL,
  amount DECIMAL(20,2) NULL,
  court VARCHAR(255) NULL,
  event_date DATE NULL,
  status VARCHAR(50) NULL,
  case_role VARCHAR(100) NULL,
  case_cause VARCHAR(500) NULL,
  current_procedure VARCHAR(100) NULL,
  procedure_date DATE NULL,
  is_history TINYINT NOT NULL DEFAULT 0,
  create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_risk_judicial_case_id (case_id),
  KEY idx_risk_judicial_case_org_date (org_id, procedure_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE risk_executed__v31fix (
  id BIGINT NOT NULL AUTO_INCREMENT,
  org_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  org_name VARCHAR(255) NULL,
  case_no VARCHAR(255) NOT NULL,
  case_title VARCHAR(500) NULL,
  amount DECIMAL(20,2) NULL,
  court VARCHAR(255) NULL,
  event_date DATE NULL,
  status VARCHAR(50) NULL,
  exec_court VARCHAR(255) NULL,
  exec_person_id VARCHAR(64) NOT NULL,
  exec_status VARCHAR(100) NULL,
  exec_target VARCHAR(255) NULL,
  filing_date DATE NULL,
  is_history TINYINT NOT NULL DEFAULT 0,
  create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_risk_executed (org_id, case_no, exec_person_id),
  KEY idx_risk_executed_org_date (org_id, filing_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE risk_bankruptcy__v31fix (
  id BIGINT NOT NULL AUTO_INCREMENT,
  case_id VARCHAR(64) NOT NULL,
  case_no VARCHAR(255) NULL,
  case_type VARCHAR(100) NULL,
  court VARCHAR(255) NULL,
  public_date DATE NULL,
  create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_risk_bankruptcy_case (case_id),
  KEY idx_risk_bankruptcy_date (public_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE risk_bankruptcy_party__v31fix (
  id BIGINT NOT NULL AUTO_INCREMENT,
  case_id VARCHAR(64) NOT NULL,
  org_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  party_name VARCHAR(255) NULL,
  party_role VARCHAR(100) NOT NULL,
  is_history TINYINT NOT NULL DEFAULT 0,
  create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_risk_bankruptcy_party (case_id, org_id, party_role),
  KEY idx_risk_bankruptcy_party_org (org_id, is_history)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE risk_abnormal__v31fix (
  id BIGINT NOT NULL AUTO_INCREMENT,
  case_id VARCHAR(64) NOT NULL,
  org_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  org_name VARCHAR(255) NULL,
  reason VARCHAR(500) NULL,
  decision_org VARCHAR(255) NULL,
  abn_date DATE NULL,
  remove_date DATE NULL,
  status VARCHAR(50) NULL,
  is_history TINYINT NOT NULL DEFAULT 0,
  create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_risk_abnormal_case (case_id),
  KEY idx_risk_abnormal_org_date (org_id, abn_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE risk_punishment__v31fix (
  id BIGINT NOT NULL AUTO_INCREMENT,
  case_id VARCHAR(64) NOT NULL,
  org_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  org_name VARCHAR(255) NULL,
  doc_no VARCHAR(255) NULL,
  reason TEXT NULL,
  fine_amount DECIMAL(20,2) NULL,
  confiscate_amount DECIMAL(20,2) NULL,
  decision_org VARCHAR(255) NULL,
  penalty_date DATE NULL,
  public_date DATE NULL,
  status VARCHAR(50) NULL,
  is_history TINYINT NOT NULL DEFAULT 0,
  create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_risk_punishment (case_id, org_id),
  KEY idx_risk_punishment_org_date (org_id, penalty_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE risk_illegal__v31fix (
  id BIGINT NOT NULL AUTO_INCREMENT,
  case_id VARCHAR(64) NOT NULL,
  org_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  org_name VARCHAR(255) NULL,
  reason VARCHAR(500) NULL,
  decision_org VARCHAR(255) NULL,
  abn_date DATE NULL,
  remove_date DATE NULL,
  status VARCHAR(50) NULL,
  is_history TINYINT NOT NULL DEFAULT 0,
  create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_risk_illegal_case (case_id),
  KEY idx_risk_illegal_org_date (org_id, abn_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE risk_tax_punish__v31fix (
  id BIGINT NOT NULL AUTO_INCREMENT,
  case_id VARCHAR(64) NOT NULL,
  org_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  case_no VARCHAR(255) NULL,
  reason VARCHAR(500) NULL,
  amount DECIMAL(20,2) NULL,
  publish_date DATE NULL,
  tax_vio_type VARCHAR(100) NULL,
  status VARCHAR(50) NULL,
  is_history TINYINT NOT NULL DEFAULT 0,
  create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_risk_tax_punish_case (case_id),
  KEY idx_risk_tax_punish_org_date (org_id, publish_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE enterprise_risk_summary__v31fix (
  id BIGINT NOT NULL AUTO_INCREMENT,
  org_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  risk_type VARCHAR(50) NOT NULL,
  total_count INT NOT NULL DEFAULT 0,
  current_count INT NOT NULL DEFAULT 0,
  history_count INT NOT NULL DEFAULT 0,
  latest_date DATE NULL,
  create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_enterprise_risk_summary (org_id, risk_type),
  KEY idx_enterprise_risk_summary_type (risk_type, total_count),
  KEY idx_enterprise_risk_summary_org (org_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ---------------------------------------------------------------------------
-- C. ODS 原始结构 -> DWD 规范结构
-- ---------------------------------------------------------------------------

SET @sql = CONCAT(
  'INSERT INTO risk_judicial_case__v31fix ',
  '(org_id,org_name,case_id,case_no,case_title,case_type_tag,amount,court,event_date,status,',
  'case_role,case_cause,current_procedure,procedure_date,is_history,create_time,update_time) ',
  'SELECT org_id,company_name,case_id,case_no,case_title,case_type_tag,NULL,NULL,procedure_date,NULL,',
  'case_role,case_cause,current_procedure,procedure_date,0,',
  'COALESCE(created_time,CURRENT_TIMESTAMP),COALESCE(updated_time,created_time,CURRENT_TIMESTAMP) ',
  'FROM ', @raw_judicial, ' WHERE COALESCE(is_deleted,0)=0'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql = CONCAT(
  'INSERT INTO risk_executed__v31fix ',
  '(org_id,org_name,case_no,case_title,amount,court,event_date,status,exec_court,exec_person_id,',
  'exec_status,exec_target,filing_date,is_history,create_time,update_time) ',
  'SELECT org_id,name_cn,case_no,NULL,',
  'CASE WHEN TRIM(exec_target) REGEXP ''^-?[0-9]+(\\\\.[0-9]+)?$'' THEN CAST(exec_target AS DECIMAL(20,2)) ELSE NULL END,',
  'exec_court,filing_date,NULL,exec_court,exec_person_id,exec_status,exec_target,filing_date,0,',
  'COALESCE(created_time,CURRENT_TIMESTAMP),COALESCE(updated_time,created_time,CURRENT_TIMESTAMP) ',
  'FROM ', @raw_executed, ' WHERE COALESCE(is_deleted,0)=0'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql = CONCAT(
  'INSERT INTO risk_bankruptcy__v31fix ',
  '(case_id,case_no,case_type,court,public_date,create_time,update_time) ',
  'SELECT case_no,case_no,case_type,handling_court,public_date,',
  'COALESCE(created_time,CURRENT_TIMESTAMP),COALESCE(updated_time,created_time,CURRENT_TIMESTAMP) ',
  'FROM ', @raw_bankruptcy, ' WHERE COALESCE(is_deleted,0)=0'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- party_role 保留上游 0/1/2/3 原码，避免在无字典依据时伪造中文语义。
-- 仅迁移能关联主表的记录；同 case_no + org_id + role 冲突时保留更新时间最新的一条。
SET @sql = CONCAT(
  'INSERT INTO risk_bankruptcy_party__v31fix ',
  '(case_id,org_id,party_name,party_role,is_history,create_time,update_time) ',
  'SELECT case_no,org_id,COALESCE(NULLIF(related_person_name,''''),name_cn),',
  'CAST(CAST(party_role_type AS UNSIGNED) AS CHAR),',
  'CASE WHEN history_status=1 THEN 1 ELSE 0 END,',
  'COALESCE(created_time,CURRENT_TIMESTAMP),COALESCE(updated_time,created_time,CURRENT_TIMESTAMP) ',
  'FROM (',
  ' SELECT p.*,m.history_status,',
  ' ROW_NUMBER() OVER (PARTITION BY p.case_no,p.org_id,p.party_role_type ',
  ' ORDER BY p.updated_time DESC,p.created_time DESC,p.bankruptcy_party_id DESC) AS rn',
  ' FROM risk_bankruptcy_party p JOIN ', @raw_bankruptcy, ' m ON m.case_no=p.case_no',
  ' WHERE COALESCE(p.is_deleted,0)=0 AND COALESCE(m.is_deleted,0)=0',
  ') ranked WHERE rn=1'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

INSERT INTO risk_abnormal__v31fix (
  case_id, org_id, org_name, reason, decision_org, abn_date, remove_date,
  status, is_history, create_time, update_time
)
SELECT
  abnormal_id,
  org_id,
  name_cn,
  abn_reason,
  abn_org,
  abn_date,
  remove_date,
  NULL,
  CASE WHEN remove_date IS NULL THEN 0 ELSE 1 END,
  COALESCE(created_time, CURRENT_TIMESTAMP),
  COALESCE(updated_time, created_time, CURRENT_TIMESTAMP)
FROM risk_abnormal
WHERE COALESCE(is_deleted, 0) = 0;

INSERT INTO risk_punishment__v31fix (
  case_id, org_id, org_name, doc_no, reason, fine_amount, confiscate_amount,
  decision_org, penalty_date, public_date, status, is_history, create_time, update_time
)
SELECT
  penalty_id,
  org_id,
  name_cn,
  decision_no,
  violation_type,
  CAST(NULLIF(TRIM(fine_amount), '') AS DECIMAL(20,2)),
  CAST(NULLIF(TRIM(confiscate_amount), '') AS DECIMAL(20,2)),
  decision_org,
  penalty_date,
  public_date,
  NULL,
  0,
  COALESCE(created_time, CURRENT_TIMESTAMP),
  COALESCE(updated_time, created_time, CURRENT_TIMESTAMP)
FROM risk_punishment
WHERE COALESCE(is_deleted, 0) = 0;

INSERT INTO risk_illegal__v31fix (
  case_id, org_id, org_name, reason, decision_org, abn_date, remove_date,
  status, is_history, create_time, update_time
)
SELECT
  sv_id,
  org_id,
  name_cn,
  abn_reason,
  abn_org,
  abn_date,
  remove_date,
  NULL,
  CASE WHEN remove_date IS NULL THEN 0 ELSE 1 END,
  COALESCE(created_time, CURRENT_TIMESTAMP),
  COALESCE(updated_time, created_time, CURRENT_TIMESTAMP)
FROM risk_illegal
WHERE COALESCE(is_deleted, 0) = 0;

INSERT INTO risk_tax_punish__v31fix (
  case_id, org_id, case_no, reason, amount, publish_date, tax_vio_type,
  status, is_history, create_time, update_time
)
SELECT
  tax_vio_id,
  org_id,
  NULL,
  illegal_fact,
  NULL,
  publish_date,
  case_type,
  NULL,
  0,
  COALESCE(created_time, CURRENT_TIMESTAMP),
  COALESCE(updated_time, created_time, CURRENT_TIMESTAMP)
FROM risk_tax_punish
WHERE COALESCE(is_deleted, 0) = 0;

-- ---------------------------------------------------------------------------
-- D. 迁移前验收：行数、唯一键和必填字段
-- ---------------------------------------------------------------------------

SELECT 'risk_judicial_case' AS table_name, COUNT(*) AS migrated_rows,
       SUM(org_id IS NULL OR org_id='') AS missing_org,
       SUM(case_id IS NULL OR case_id='') AS missing_key,
       COUNT(*) - COUNT(DISTINCT case_id) AS duplicate_key
FROM risk_judicial_case__v31fix
UNION ALL
SELECT 'risk_executed', COUNT(*),
       SUM(org_id IS NULL OR org_id=''),
       SUM(case_no IS NULL OR case_no='' OR exec_person_id IS NULL OR exec_person_id=''),
       COUNT(*) - COUNT(DISTINCT CONCAT_WS('|',org_id,case_no,exec_person_id))
FROM risk_executed__v31fix
UNION ALL
SELECT 'risk_bankruptcy', COUNT(*),
       0,
       SUM(case_id IS NULL OR case_id=''),
       COUNT(*) - COUNT(DISTINCT case_id)
FROM risk_bankruptcy__v31fix
UNION ALL
SELECT 'risk_bankruptcy_party', COUNT(*),
       SUM(org_id IS NULL OR org_id=''),
       SUM(case_id IS NULL OR case_id='' OR party_role IS NULL OR party_role=''),
       COUNT(*) - COUNT(DISTINCT CONCAT_WS('|',case_id,org_id,party_role))
FROM risk_bankruptcy_party__v31fix
UNION ALL
SELECT 'risk_abnormal', COUNT(*),
       SUM(org_id IS NULL OR org_id=''),
       SUM(case_id IS NULL OR case_id=''),
       COUNT(*) - COUNT(DISTINCT case_id)
FROM risk_abnormal__v31fix
UNION ALL
SELECT 'risk_punishment', COUNT(*),
       SUM(org_id IS NULL OR org_id=''),
       SUM(case_id IS NULL OR case_id=''),
       COUNT(*) - COUNT(DISTINCT CONCAT_WS('|',case_id,org_id))
FROM risk_punishment__v31fix
UNION ALL
SELECT 'risk_illegal', COUNT(*),
       SUM(org_id IS NULL OR org_id=''),
       SUM(case_id IS NULL OR case_id=''),
       COUNT(*) - COUNT(DISTINCT case_id)
FROM risk_illegal__v31fix
UNION ALL
SELECT 'risk_tax_punish', COUNT(*),
       SUM(org_id IS NULL OR org_id=''),
       SUM(case_id IS NULL OR case_id=''),
       COUNT(*) - COUNT(DISTINCT case_id)
FROM risk_tax_punish__v31fix;

-- ---------------------------------------------------------------------------
-- E. 重建 org_id × risk_type 风险汇总
-- ---------------------------------------------------------------------------

INSERT INTO enterprise_risk_summary__v31fix (
  org_id, risk_type, total_count, current_count, history_count, latest_date
)
SELECT
  org_id,
  risk_type,
  COUNT(*) AS total_count,
  SUM(CASE WHEN is_history=0 THEN 1 ELSE 0 END) AS current_count,
  SUM(CASE WHEN is_history=1 THEN 1 ELSE 0 END) AS history_count,
  MAX(event_date) AS latest_date
FROM (
  SELECT org_id, 'judicial_case' AS risk_type, is_history, procedure_date AS event_date
  FROM risk_judicial_case__v31fix
  UNION ALL
  SELECT org_id, 'executed', is_history, filing_date
  FROM risk_executed__v31fix
  UNION ALL
  SELECT org_id, 'abnormal', is_history, abn_date
  FROM risk_abnormal__v31fix
  UNION ALL
  SELECT org_id, 'punishment', is_history, penalty_date
  FROM risk_punishment__v31fix
  UNION ALL
  SELECT org_id, 'illegal', is_history, abn_date
  FROM risk_illegal__v31fix
  UNION ALL
  SELECT org_id, 'tax_punish', is_history, publish_date
  FROM risk_tax_punish__v31fix
  UNION ALL
  SELECT p.org_id, 'bankruptcy', p.is_history, b.public_date
  FROM risk_bankruptcy_party__v31fix p
  JOIN risk_bankruptcy__v31fix b ON b.case_id=p.case_id
) risk_rows
GROUP BY org_id, risk_type;

SELECT
  risk_type,
  SUM(total_count) AS total_count,
  SUM(current_count) AS current_count,
  SUM(history_count) AS history_count,
  COUNT(*) AS enterprise_count
FROM enterprise_risk_summary__v31fix
GROUP BY risk_type
ORDER BY risk_type;

-- ---------------------------------------------------------------------------
-- F. 原子切换；原表完整保留
-- ---------------------------------------------------------------------------

RENAME TABLE
  risk_judicial_case TO risk_judicial_case__pre_fix_20260812,
  risk_judicial_case__v31fix TO risk_judicial_case,
  risk_executed TO risk_executed__pre_fix_20260812,
  risk_executed__v31fix TO risk_executed,
  risk_bankruptcy TO risk_bankruptcy__pre_fix_20260812,
  risk_bankruptcy__v31fix TO risk_bankruptcy,
  risk_bankruptcy_party TO risk_bankruptcy_party__pre_fix_20260812,
  risk_bankruptcy_party__v31fix TO risk_bankruptcy_party,
  risk_abnormal TO risk_abnormal__pre_fix_20260812,
  risk_abnormal__v31fix TO risk_abnormal,
  risk_punishment TO risk_punishment__pre_fix_20260812,
  risk_punishment__v31fix TO risk_punishment,
  risk_illegal TO risk_illegal__pre_fix_20260812,
  risk_illegal__v31fix TO risk_illegal,
  risk_tax_punish TO risk_tax_punish__pre_fix_20260812,
  risk_tax_punish__v31fix TO risk_tax_punish,
  enterprise_risk_summary TO enterprise_risk_summary__pre_fix_20260812,
  enterprise_risk_summary__v31fix TO enterprise_risk_summary;

-- 隐形字符原始表改为可见备份名，避免继续被误认为规范表。
SET @sql = CONCAT('RENAME TABLE ', @raw_judicial, ' TO risk_judicial_case__raw_u200b_20260812');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql = CONCAT('RENAME TABLE ', @raw_executed, ' TO risk_executed__raw_u200b_20260812');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql = CONCAT('RENAME TABLE ', @raw_bankruptcy, ' TO risk_bankruptcy__raw_u200b_20260812');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 空的 risk_dishonest[U+200B] 无数据，删除后保留规范空表 risk_dishonest。
SET @sql = CONCAT('DROP TABLE ', @raw_dishonest);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- enterprise_base2 为 0 行孤立表，结构已由本脚本和设计文档留档。
DROP TABLE enterprise_base2;

-- ---------------------------------------------------------------------------
-- G. 工商表安全增量变更
-- ---------------------------------------------------------------------------

CREATE TABLE enterprise_industry_chain__pre_fix_20260812 LIKE enterprise_industry_chain;
INSERT INTO enterprise_industry_chain__pre_fix_20260812 SELECT * FROM enterprise_industry_chain;

ALTER TABLE enterprise_industry_chain
  ADD COLUMN org_id VARCHAR(64) NULL COMMENT '机构id；待权威信用代码映射后回填' AFTER id,
  ADD KEY idx_enterprise_industry_chain_org_id (org_id);

-- 20,000 行均无可靠 org_id 映射，本次不回填，不设 NOT NULL。

-- enterprise_financing 保持 finance_round / amount / currency / investors /
-- event_date。lumen-etl-es-py 的同步、统计和种子任务直接依赖这些字段；
-- lumen-algo-py 已通过 _COLUMN_CANDIDATES 兼容该现行契约。

-- ---------------------------------------------------------------------------
-- H. 最终结构验收
-- ---------------------------------------------------------------------------

SELECT TABLE_NAME, COUNT(*) AS column_count,
       SUM(COLUMN_NAME='id' AND COLUMN_TYPE='bigint' AND COLUMN_KEY='PRI' AND EXTRA='auto_increment') AS valid_id
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME IN (
    'risk_judicial_case',
    'risk_executed',
    'risk_bankruptcy',
    'risk_bankruptcy_party',
    'risk_abnormal',
    'risk_punishment',
    'risk_illegal',
    'risk_tax_punish',
    'enterprise_risk_summary'
  )
GROUP BY TABLE_NAME
ORDER BY TABLE_NAME;

SELECT TABLE_NAME, HEX(TABLE_NAME) AS name_hex
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = DATABASE()
  AND HEX(TABLE_NAME) LIKE '%E2808B';

SELECT risk_type,
       SUM(total_count) AS total_count,
       SUM(current_count) AS current_count,
       SUM(history_count) AS history_count
FROM enterprise_risk_summary
GROUP BY risk_type
ORDER BY risk_type;

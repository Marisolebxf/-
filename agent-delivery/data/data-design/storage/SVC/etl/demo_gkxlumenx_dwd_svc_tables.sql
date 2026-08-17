-- SVC DWD/ADS structure draft (MySQL)
-- Source: storage/SVC/stores/mysql/{dwd-svc,ads,dim}.md · DATA-SVC-STORAGE-DDL-L01
-- Target Demo: demo_gkxlumenx_dwd / demo_gkxlumenx_ads
-- DO NOT APPLY to formal gkxlumenx_* without Owner + architect signoff.
-- Data admission rules (Q-SVC-010) OUT OF SCOPE — structure only.

-- ========== DWD: demo_gkxlumenx_dwd ==========

CREATE TABLE IF NOT EXISTS service_org (
  id BIGINT NOT NULL AUTO_INCREMENT,
  service_org_code VARCHAR(64) NOT NULL,
  org_id VARCHAR(64) NOT NULL,
  external_id VARCHAR(64) NULL,
  name_cn VARCHAR(255) NULL,
  service_type_primary VARCHAR(32) NULL,
  rule_version VARCHAR(32) NOT NULL,
  verification_status VARCHAR(32) NOT NULL DEFAULT 'pending_client_confirm',
  is_shenzhen TINYINT NULL,
  province VARCHAR(64) NULL,
  city VARCHAR(64) NULL,
  district VARCHAR(64) NULL,
  is_deleted TINYINT NOT NULL DEFAULT 0,
  batch_id VARCHAR(64) NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  updated_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  PRIMARY KEY (id),
  UNIQUE KEY uk_service_org_code (service_org_code),
  KEY idx_org_id (org_id),
  KEY idx_external_id (external_id),
  KEY idx_verif_del (verification_status, is_deleted),
  KEY idx_city_district (city, district)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS service_org_type_tag (
  id BIGINT NOT NULL AUTO_INCREMENT,
  service_org_code VARCHAR(64) NOT NULL,
  service_type VARCHAR(32) NOT NULL,
  tag_rule_version VARCHAR(32) NOT NULL,
  confidence DECIMAL(5,4) NULL,
  verification_status VARCHAR(32) NOT NULL DEFAULT 'pending_client_confirm',
  is_primary TINYINT NOT NULL DEFAULT 0,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  updated_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  PRIMARY KEY (id),
  UNIQUE KEY uk_org_type_rule (service_org_code, service_type, tag_rule_version),
  KEY idx_service_type (service_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS service_org_chain_rel (
  id BIGINT NOT NULL AUTO_INCREMENT,
  service_org_code VARCHAR(64) NOT NULL,
  chain_stage_code VARCHAR(64) NOT NULL,
  chain_stage_name VARCHAR(128) NULL,
  rel_type VARCHAR(32) NOT NULL DEFAULT 'SERVES',
  weight DECIMAL(10,4) NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (id),
  UNIQUE KEY uk_org_stage_rel (service_org_code, chain_stage_code, rel_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS service_org_org_rel (
  id BIGINT NOT NULL AUTO_INCREMENT,
  src_service_org_code VARCHAR(64) NOT NULL,
  dst_service_org_code VARCHAR(64) NULL,
  dst_org_id VARCHAR(64) NULL,
  rel_type VARCHAR(32) NOT NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (id),
  KEY idx_src_rel (src_service_org_code, rel_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS service_org_financing (
  id BIGINT NOT NULL AUTO_INCREMENT,
  service_org_code VARCHAR(64) NOT NULL,
  event_type VARCHAR(16) NOT NULL,
  amount DECIMAL(20,2) NULL,
  currency VARCHAR(8) NULL,
  completion_date DATE NULL,
  counterparty_name VARCHAR(255) NULL,
  source_ods_table VARCHAR(64) NULL,
  source_ods_key VARCHAR(64) NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (id),
  KEY idx_org_date (service_org_code, completion_date),
  KEY idx_event_type (event_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ========== ADS: demo_gkxlumenx_ads（骨架；dim_json 落地可改为维列）==========

CREATE TABLE IF NOT EXISTS svc_org_profile_card (
  id BIGINT NOT NULL AUTO_INCREMENT,
  service_org_code VARCHAR(64) NOT NULL,
  org_id VARCHAR(64) NOT NULL,
  name_cn VARCHAR(255) NULL,
  service_type_primary VARCHAR(32) NULL,
  city VARCHAR(64) NULL,
  district VARCHAR(64) NULL,
  verification_status VARCHAR(32) NULL,
  tech_score DECIMAL(10,4) NULL,
  as_of_date DATE NULL,
  batch_id VARCHAR(64) NULL,
  ext_json JSON NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  updated_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  PRIMARY KEY (id),
  UNIQUE KEY uk_svc_profile_code (service_org_code),
  KEY idx_org_id (org_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS svc_rec_ranking (
  id BIGINT NOT NULL AUTO_INCREMENT,
  list_type VARCHAR(16) NOT NULL,
  industry_direction VARCHAR(64) NOT NULL,
  rank_no INT NOT NULL,
  candidate_key VARCHAR(64) NOT NULL,
  service_org_code VARCHAR(64) NULL,
  org_id VARCHAR(64) NULL,
  in_pool TINYINT NOT NULL DEFAULT 0,
  score DECIMAL(10,4) NULL,
  reason_text VARCHAR(512) NULL,
  model_version VARCHAR(32) NOT NULL,
  as_of_date DATE NOT NULL,
  batch_id VARCHAR(64) NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (id),
  UNIQUE KEY uk_rec (list_type, industry_direction, model_version, as_of_date, candidate_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Remaining svc_* tables: follow ads.md column contracts when Demo needs them.

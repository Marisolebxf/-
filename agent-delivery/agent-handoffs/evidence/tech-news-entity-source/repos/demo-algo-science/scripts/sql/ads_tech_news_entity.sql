-- ===================== tech news entity-ext（E-TECH-NEWS-ENTITY-M3-L02） =====================
-- 正式 ADS 契约面：实体扩展抽取头表 + 实体行 + 事件扩展行（含 event_type）。
-- Wave0 写入：Python persist（SQLite 镜像同名表）；正式 MySQL 迁移后 Java 只读查询承接。

CREATE TABLE IF NOT EXISTS ads_tech_news_entity_extract (
  request_id VARCHAR(64) NOT NULL,
  title VARCHAR(1024) NULL,
  source VARCHAR(255) NULL,
  published_at DATE NULL,
  model VARCHAR(64) NULL,
  mode VARCHAR(16) NULL,
  schema_version VARCHAR(32) NULL DEFAULT 'entity-v0.1',
  entity_count INT NOT NULL DEFAULT 0,
  event_count INT NOT NULL DEFAULT 0,
  response_json JSON NOT NULL,
  latency_ms INT NULL,
  created_time DATETIME NOT NULL,
  updated_time DATETIME NOT NULL,
  PRIMARY KEY (request_id),
  KEY idx_entity_extract_created (created_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='科技资讯实体扩展抽取请求头+完整响应';

CREATE TABLE IF NOT EXISTS ads_tech_news_entity (
  id BIGINT AUTO_INCREMENT,
  request_id VARCHAR(64) NOT NULL,
  entity_ord INT NOT NULL DEFAULT 0,
  entity_type VARCHAR(32) NOT NULL,
  name VARCHAR(512) NOT NULL,
  normalized VARCHAR(512) NULL,
  evidence_json JSON NULL,
  confidence DECIMAL(6,4) NULL,
  created_time DATETIME NOT NULL,
  PRIMARY KEY (id),
  KEY idx_entity_req (request_id),
  KEY idx_entity_type_name (entity_type, name(191)),
  CONSTRAINT fk_tech_news_entity_req FOREIGN KEY (request_id)
    REFERENCES ads_tech_news_entity_extract(request_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='科技资讯实体扩展-实体行';

CREATE TABLE IF NOT EXISTS ads_tech_news_entity_event (
  id BIGINT AUTO_INCREMENT,
  request_id VARCHAR(64) NOT NULL,
  event_ord INT NOT NULL DEFAULT 0,
  company_name JSON NOT NULL,
  completion_time_raw VARCHAR(128) NULL,
  completion_time_normalized VARCHAR(32) NULL,
  completion_time_granularity VARCHAR(16) NULL,
  completed_matter TEXT NULL,
  impact TEXT NULL,
  event_type VARCHAR(64) NOT NULL DEFAULT 'other',
  news_source VARCHAR(255) NULL,
  entity_refs_json JSON NULL,
  evidence_json JSON NULL,
  confidence_json JSON NULL,
  flags_json JSON NULL,
  created_time DATETIME NOT NULL,
  PRIMARY KEY (id),
  KEY idx_entity_event_req (request_id),
  KEY idx_entity_event_type (event_type),
  CONSTRAINT fk_tech_news_entity_event_req FOREIGN KEY (request_id)
    REFERENCES ads_tech_news_entity_extract(request_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='科技资讯实体扩展-事件行（含 event_type）';

-- ============================================================
-- 科技专题-企业模块 DWD 建表脚本
-- 数据库: PostgreSQL | Schema: dwd
-- 版本: v2.0 | 日期: 2026-07-07 | 作者: [agent:data-agent]
-- 约定: 所有表统一 id BIGSERIAL 主键 + create_time + update_time
-- 设计考量: 企业数据量2亿级，主表拆分 + 司法完全拆分 + 通用统计表
-- ============================================================

CREATE SCHEMA IF NOT EXISTS dwd;

-- ============================================================
-- 1. enterprise_base（企业核心信息，年更）
--    检索列表页高频字段：名称/代码/行业/地区/成立/状态/上市标志
--    字段窄、查询频率高，2亿行下保持精简
-- ============================================================
CREATE TABLE IF NOT EXISTS dwd.enterprise_base (
    id                  BIGSERIAL       NOT NULL,
    org_id              VARCHAR(64)     NOT NULL,
    enterprise_code     VARCHAR(64)     NOT NULL,
    enterprise_name     VARCHAR(255)    NOT NULL,
    legal_representative VARCHAR(100),
    registration_date   DATE,
    business_status     VARCHAR(20),
    enterprise_type     VARCHAR(100),
    industry_category   VARCHAR(100),
    industry_code       VARCHAR(20),
    province            VARCHAR(50),
    city                VARCHAR(50),
    district            VARCHAR(50),
    registered_capital  NUMERIC(18,2),
    is_listed           SMALLINT,
    org_size            VARCHAR(20),
    create_time         TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time         TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_enterprise_base PRIMARY KEY (id),
    CONSTRAINT uk_enterprise_base_org UNIQUE (org_id)
);

COMMENT ON TABLE  dwd.enterprise_base IS '企业核心信息表（年更，检索列表高频字段）';
COMMENT ON COLUMN dwd.enterprise_base.id IS '自增主键';
COMMENT ON COLUMN dwd.enterprise_base.org_id IS '机构id（业务主键，唯一）';
COMMENT ON COLUMN dwd.enterprise_base.enterprise_code IS '统一社会信用代码';
COMMENT ON COLUMN dwd.enterprise_base.enterprise_name IS '企业全称';
COMMENT ON COLUMN dwd.enterprise_base.registered_capital IS '注册资本（万元）';
COMMENT ON COLUMN dwd.enterprise_base.is_listed IS '是否上市（0否/1是）';
COMMENT ON COLUMN dwd.enterprise_base.create_time IS '记录创建时间';
COMMENT ON COLUMN dwd.enterprise_base.update_time IS '记录更新时间（ETL）';

CREATE INDEX IF NOT EXISTS idx_enterprise_base_code ON dwd.enterprise_base (enterprise_code);
CREATE INDEX IF NOT EXISTS idx_enterprise_base_name ON dwd.enterprise_base USING gin (to_tsvector('simple', enterprise_name));
CREATE INDEX IF NOT EXISTS idx_enterprise_base_city ON dwd.enterprise_base (city);
CREATE INDEX IF NOT EXISTS idx_enterprise_base_industry ON dwd.enterprise_base (industry_code);


-- ============================================================
-- 2. enterprise_extra（企业扩展信息，年更）
--    详情页低频字段：英文名/实缴/经营范围/地址/经纬度/上市详情
--    与 base 一对一，按需 JOIN，避免列表页扫描宽行
-- ============================================================
CREATE TABLE IF NOT EXISTS dwd.enterprise_extra (
    id                  BIGSERIAL       NOT NULL,
    org_id              VARCHAR(64)     NOT NULL,
    enterprise_name_en  VARCHAR(255),
    paid_in_capital     NUMERIC(18,2),
    business_scope      TEXT,
    registered_address  VARCHAR(500),
    headquarters_address VARCHAR(500),
    lng                 NUMERIC(10,6),
    lat                 NUMERIC(10,6),
    listed_market       VARCHAR(50),
    listed_code         VARCHAR(20),
    listed_date         DATE,
    data_source         VARCHAR(100),
    create_time         TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time         TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_enterprise_extra PRIMARY KEY (id),
    CONSTRAINT uk_enterprise_extra_org UNIQUE (org_id),
    CONSTRAINT fk_extra_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE
);

COMMENT ON TABLE  dwd.enterprise_extra IS '企业扩展信息表（年更，详情页低频字段）';
COMMENT ON COLUMN dwd.enterprise_extra.id IS '自增主键';
COMMENT ON COLUMN dwd.enterprise_extra.paid_in_capital IS '实缴资本（万元）';
COMMENT ON COLUMN dwd.enterprise_extra.business_scope IS '经营范围';
COMMENT ON COLUMN dwd.enterprise_extra.lng IS '经度';
COMMENT ON COLUMN dwd.enterprise_extra.lat IS '纬度';
COMMENT ON COLUMN dwd.enterprise_extra.create_time IS '记录创建时间';
COMMENT ON COLUMN dwd.enterprise_extra.update_time IS '记录更新时间（ETL）';


-- ============================================================
-- 3. tag_dict（标签字典表）
--    通用标签字典，所有企业标签统一注册
--    tag_category: qualification资质 / honor荣誉 / scale规模 / industry产业 / diy特色
-- ============================================================
CREATE TABLE IF NOT EXISTS dwd.tag_dict (
    id              BIGSERIAL       NOT NULL,
    tag_code        VARCHAR(100)    NOT NULL,
    tag_name        VARCHAR(255)    NOT NULL,
    tag_category    VARCHAR(50)     NOT NULL,
    tag_level       VARCHAR(50),
    ods_source      VARCHAR(255),
    sort_order      INTEGER,
    is_active       SMALLINT        NOT NULL DEFAULT 1,
    create_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_tag_dict PRIMARY KEY (id),
    CONSTRAINT uk_tag_code UNIQUE (tag_code)
);

COMMENT ON TABLE  dwd.tag_dict IS '标签字典表（通用，企业资质/荣誉/规模/产业/特色标签）';
COMMENT ON COLUMN dwd.tag_dict.tag_code IS '标签编码（唯一，如high_tech/little_giant/gazelle）';
COMMENT ON COLUMN dwd.tag_dict.tag_name IS '标签中文名称';
COMMENT ON COLUMN dwd.tag_dict.tag_category IS '标签大类（qualification资质/honor荣誉/scale规模/industry产业/diy特色）';
COMMENT ON COLUMN dwd.tag_dict.tag_level IS '标签级别（national/province/city/district，荣誉类适用）';
COMMENT ON COLUMN dwd.tag_dict.ods_source IS 'ODS来源表名';

-- 预置常见标签
INSERT INTO dwd.tag_dict (tag_code, tag_name, tag_category, tag_level, ods_source, sort_order) VALUES
('high_tech',       '高新技术企业',       'qualification', 'national', 'dwd_org_tag_info/dwd_company_honor_tags', 1),
('little_giant',    '专精特新',           'qualification', 'national', 'dwd_org_tag_info/dwd_company_honor_tags', 2),
('gazelle',         '瞪羚企业',           'qualification', 'national', 'dwd_org_tag_info/dwd_company_honor_tags', 3),
('unicorn',         '独角兽企业',         'qualification', 'national', 'dwd_org_tag_info/dwd_company_honor_tags', 4),
('sme',             '小微企业',           'scale',         NULL,       'dwd_company_basic_tags',                  5),
('foreign',         '外资企业',           'scale',         NULL,       'dwd_company_basic_tags',                  6),
('honor_national',  '国家级荣誉',         'honor',         'national', 'dwd_company_honor_tags.national_tag',     10),
('honor_province',  '省级荣誉',           'honor',         'province', 'dwd_company_honor_tags.province_tag',     11),
('honor_city',      '市级荣誉',           'honor',         'city',     'dwd_company_honor_tags.city_tag',         12),
('honor_district',  '区县级荣誉',         'honor',         'district', 'dwd_company_honor_tags.district_tag',     13),
('certification',   '资质认证',           'qualification', NULL,       'dwd_company_honor_tags.certification',    20)
ON CONFLICT (tag_code) DO NOTHING;

-- 其余标签由 ETL 从 dwd_org_tag_info / dwd_company_diy_tags 动态发现后追加


-- ============================================================
-- 4. enterprise_tag（企业-标签关联表）
--    多对多，一家企业可有多个标签，一个标签可关联多家企业
--    检索页按 tag_code 筛选，详情页按 org_id 查全部标签
-- ============================================================
CREATE TABLE IF NOT EXISTS dwd.enterprise_tag (
    id              BIGSERIAL       NOT NULL,
    org_id          VARCHAR(64)     NOT NULL,
    tag_code        VARCHAR(100)    NOT NULL,
    tag_value       VARCHAR(500),
    create_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_enterprise_tag PRIMARY KEY (id),
    CONSTRAINT fk_etag_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE,
    CONSTRAINT fk_etag_dict FOREIGN KEY (tag_code) REFERENCES dwd.tag_dict(tag_code),
    CONSTRAINT uk_etag UNIQUE (org_id, tag_code, tag_value)
);

COMMENT ON TABLE  dwd.enterprise_tag IS '企业-标签关联表（多对多）';
COMMENT ON COLUMN dwd.enterprise_tag.org_id IS '机构id';
COMMENT ON COLUMN dwd.enterprise_tag.tag_code IS '标签编码（关联字典表）';
COMMENT ON COLUMN dwd.enterprise_tag.tag_value IS '标签值/明细（如专精特新级别"国家级"、荣誉标签具体名称，可为空）';

CREATE INDEX IF NOT EXISTS idx_etag_org ON dwd.enterprise_tag (org_id);
CREATE INDEX IF NOT EXISTS idx_etag_code ON dwd.enterprise_tag (tag_code);


-- ============================================================
-- 4. enterprise_finance_history（企业财务历史，年追加）
--    存全部历史年份，画像页取最新年份即可（ORDER BY data_year DESC LIMIT 1）
--    趋势图取全部年份
-- ============================================================
CREATE TABLE IF NOT EXISTS dwd.enterprise_finance_history (
    id                  BIGSERIAL       NOT NULL,
    org_id              VARCHAR(64)     NOT NULL,
    data_year           INTEGER         NOT NULL,
    revenue             NUMERIC(18,2),
    net_profit          NUMERIC(18,2),
    total_assets        NUMERIC(18,2),
    total_liabilities   NUMERIC(18,2),
    total_tax           NUMERIC(18,2),
    rd_investment       NUMERIC(18,2),
    employees_number    INTEGER,
    owners_equity       NUMERIC(18,2),
    data_source         VARCHAR(50),
    create_time         TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time         TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_enterprise_finance_history PRIMARY KEY (id),
    CONSTRAINT fk_fin_hist_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE,
    CONSTRAINT uk_fin_hist UNIQUE (org_id, data_year, data_source)
);

COMMENT ON TABLE  dwd.enterprise_finance_history IS '企业财务历史表（年追加，逐年财务数据；画像页取最新年份，趋势图取全部年份）';
COMMENT ON COLUMN dwd.enterprise_finance_history.id IS '自增主键';
COMMENT ON COLUMN dwd.enterprise_finance_history.revenue IS '营收（万元）';
COMMENT ON COLUMN dwd.enterprise_finance_history.total_tax IS '纳税总额（万元）';
COMMENT ON COLUMN dwd.enterprise_finance_history.owners_equity IS '所有者权益（万元）';
COMMENT ON COLUMN dwd.enterprise_finance_history.data_source IS '数据来源（annual年报/stock上市财务）';
COMMENT ON COLUMN dwd.enterprise_finance_history.create_time IS '记录创建时间';
COMMENT ON COLUMN dwd.enterprise_finance_history.update_time IS '记录更新时间（ETL）';

CREATE INDEX IF NOT EXISTS idx_fin_hist_org_year ON dwd.enterprise_finance_history (org_id, data_year);


-- ============================================================
-- 6. enterprise_patent_history（企业专利历史，年追加）
--    存全部历史年份，画像页取最新年份或 SUM 全部年份即可
--    趋势图取全部年份
-- ============================================================
CREATE TABLE IF NOT EXISTS dwd.enterprise_patent_history (
    id                      BIGSERIAL       NOT NULL,
    org_id                  VARCHAR(64)     NOT NULL,
    data_year               INTEGER         NOT NULL,
    patent_apply_count      INTEGER,
    patent_grant_count      INTEGER,
    patent_valid_count      INTEGER,
    patent_invention_count  INTEGER,
    patent_citation_count   INTEGER,
    latest_patent_date      DATE,
    latest_grant_date       DATE,
    create_time             TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time             TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_enterprise_patent_history PRIMARY KEY (id),
    CONSTRAINT fk_pat_hist_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE,
    CONSTRAINT uk_pat_hist UNIQUE (org_id, data_year)
);

COMMENT ON TABLE  dwd.enterprise_patent_history IS '企业专利历史表（年追加，按年聚合；画像页取最新年份或SUM全部，趋势图取全部年份）';
COMMENT ON COLUMN dwd.enterprise_patent_history.id IS '自增主键';
COMMENT ON COLUMN dwd.enterprise_patent_history.patent_apply_count IS '当年专利申请数';
COMMENT ON COLUMN dwd.enterprise_patent_history.patent_invention_count IS '当年发明专利数';
COMMENT ON COLUMN dwd.enterprise_patent_history.latest_patent_date IS '当年最新专利申请日期';
COMMENT ON COLUMN dwd.enterprise_patent_history.latest_grant_date IS '当年最新授权日期';
COMMENT ON COLUMN dwd.enterprise_patent_history.create_time IS '记录创建时间';
COMMENT ON COLUMN dwd.enterprise_patent_history.update_time IS '记录更新时间（ETL）';

CREATE INDEX IF NOT EXISTS idx_pat_hist_org_year ON dwd.enterprise_patent_history (org_id, data_year);


-- ============================================================
-- 7. enterprise_patent_detail（企业专利明细，日追加）
--    详情页知识产权 Tab 的专利列表，走 PG 查询不走 ES
--    ODS 源表 dwd_patent 无 org_id，ETL 需通过申请人名称映射
-- ============================================================
CREATE TABLE IF NOT EXISTS dwd.enterprise_patent_detail (
    id                      BIGSERIAL       NOT NULL,
    org_id                  VARCHAR(64)     NOT NULL,
    patent_id               VARCHAR(64)     NOT NULL,
    publication_number      VARCHAR(64),
    title_zh                VARCHAR(1024),
    title_en                VARCHAR(1024),
    abstract_zh             TEXT,
    patent_type             VARCHAR(10),
    country                 VARCHAR(20),
    filing_date             DATE,
    filing_year             INTEGER,
    publication_date        DATE,
    publication_year        INTEGER,
    grant_date              DATE,
    grant_year              INTEGER,
    grant_number            VARCHAR(64),
    ipc_main                VARCHAR(32),
    cpc_main                VARCHAR(32),
    inventor                VARCHAR(500),
    applicant_name          VARCHAR(255),
    assignee_name           VARCHAR(255),
    legal_status            VARCHAR(50),
    citation_count          INTEGER,
    cited_by_count          INTEGER,
    detail_json             TEXT,
    data_source             VARCHAR(100),
    create_time             TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time             TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_enterprise_patent_detail PRIMARY KEY (id),
    CONSTRAINT fk_pat_det_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE,
    CONSTRAINT uk_pat_det UNIQUE (org_id, patent_id)
);

COMMENT ON TABLE  dwd.enterprise_patent_detail IS '企业专利明细表（日追加，详情页知识产权Tab走PG查询）';
COMMENT ON COLUMN dwd.enterprise_patent_detail.org_id IS '机构id（ETL通过申请人名称映射）';
COMMENT ON COLUMN dwd.enterprise_patent_detail.patent_id IS '专利id（ODS dwd_patent.patent_id）';
COMMENT ON COLUMN dwd.enterprise_patent_detail.publication_number IS '专利公布号';
COMMENT ON COLUMN dwd.enterprise_patent_detail.title_zh IS '中文标题（ODS dwd_patent_title.title_zh）';
COMMENT ON COLUMN dwd.enterprise_patent_detail.abstract_zh IS '中文摘要（ODS dwd_patent_abstract）';
COMMENT ON COLUMN dwd.enterprise_patent_detail.patent_type IS '申请类型（A=发明/U=实用/F=外观/W=PCT）';
COMMENT ON COLUMN dwd.enterprise_patent_detail.filing_date IS '申请日期（ODS application_reference_3）';
COMMENT ON COLUMN dwd.enterprise_patent_detail.publication_date IS '公开日期（ODS publication_reference_2）';
COMMENT ON COLUMN dwd.enterprise_patent_detail.grant_date IS '授权日期（ODS granted_number对应）';
COMMENT ON COLUMN dwd.enterprise_patent_detail.ipc_main IS 'IPC主分类号（ODS classification_ipcr）';
COMMENT ON COLUMN dwd.enterprise_patent_detail.cpc_main IS 'CPC主分类号（ODS classification_cpc）';
COMMENT ON COLUMN dwd.enterprise_patent_detail.inventor IS '发明人（ODS inventors_2）';
COMMENT ON COLUMN dwd.enterprise_patent_detail.applicant_name IS '原始申请人名称（ODS applicants_2）';
COMMENT ON COLUMN dwd.enterprise_patent_detail.assignee_name IS '当前专利权人名称（ODS assignees_2）';
COMMENT ON COLUMN dwd.enterprise_patent_detail.legal_status IS '法律状态（ETL从grant_number等推导：有效/无效/审查中）';
COMMENT ON COLUMN dwd.enterprise_patent_detail.citation_count IS '引用专利数量（ODS dwd_patent_cited.reference_cited）';
COMMENT ON COLUMN dwd.enterprise_patent_detail.cited_by_count IS '被引数量（ODS dwd_patent_cited.cited_by_nums）';
COMMENT ON COLUMN dwd.enterprise_patent_detail.detail_json IS 'ODS原始完整记录（JSON）';
COMMENT ON COLUMN dwd.enterprise_patent_detail.create_time IS '记录创建时间';
COMMENT ON COLUMN dwd.enterprise_patent_detail.update_time IS '记录更新时间（ETL）';

CREATE INDEX IF NOT EXISTS idx_pat_det_org_date ON dwd.enterprise_patent_detail (org_id, filing_date DESC);
CREATE INDEX IF NOT EXISTS idx_pat_det_org_type ON dwd.enterprise_patent_detail (org_id, patent_type);
CREATE INDEX IF NOT EXISTS idx_pat_det_patent_id ON dwd.enterprise_patent_detail (patent_id);


-- ============================================================
-- 8. enterprise_bid（企业招投标明细，日追加）
-- ============================================================
CREATE TABLE IF NOT EXISTS dwd.enterprise_bid (
    id                  BIGSERIAL       NOT NULL,
    org_id              VARCHAR(64)     NOT NULL,
    enterprise_name     VARCHAR(255),
    tender_org_id       VARCHAR(64),
    tender_name         VARCHAR(255),
    role                VARCHAR(20),
    announcement_title  TEXT,
    announcement_content TEXT,
    announcement_date   DATE,
    winning_amount      NUMERIC(18,2),
    project_name        VARCHAR(500),
    project_no          VARCHAR(100),
    data_source         VARCHAR(100),
    create_time         TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time         TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_enterprise_bid PRIMARY KEY (id),
    CONSTRAINT fk_bid_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE
);

COMMENT ON TABLE  dwd.enterprise_bid IS '企业招投标明细表（日追加）';
COMMENT ON COLUMN dwd.enterprise_bid.id IS '自增主键';
COMMENT ON COLUMN dwd.enterprise_bid.org_id IS '关联企业id（默认中标方，role区分角色）';
COMMENT ON COLUMN dwd.enterprise_bid.role IS '本企业角色（中标方/采购方）';
COMMENT ON COLUMN dwd.enterprise_bid.announcement_date IS '公告日期（⚠️ODS缺此字段，待上游确认）';
COMMENT ON COLUMN dwd.enterprise_bid.winning_amount IS '中标金额（万元）（⚠️ODS缺此字段，待上游确认）';
COMMENT ON COLUMN dwd.enterprise_bid.create_time IS '记录创建时间';
COMMENT ON COLUMN dwd.enterprise_bid.update_time IS '记录更新时间（ETL）';

CREATE INDEX IF NOT EXISTS idx_bid_org_date ON dwd.enterprise_bid (org_id, announcement_date DESC);
CREATE INDEX IF NOT EXISTS idx_bid_tender_org ON dwd.enterprise_bid (tender_org_id);


-- ============================================================
-- 9. enterprise_news（企业新闻资讯，日追加）
-- ============================================================
CREATE TABLE IF NOT EXISTS dwd.enterprise_news (
    id                  BIGSERIAL       NOT NULL,
    org_id              VARCHAR(64)     NOT NULL,
    enterprise_name     VARCHAR(255),
    news_title          TEXT,
    news_date           DATE,
    news_content        TEXT,
    original_url        TEXT,
    data_source         VARCHAR(100),
    source_created_time TIMESTAMP,
    create_time         TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time         TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_enterprise_news PRIMARY KEY (id),
    CONSTRAINT fk_news_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE
);

COMMENT ON TABLE  dwd.enterprise_news IS '企业新闻资讯表（日追加）';
COMMENT ON COLUMN dwd.enterprise_news.id IS '自增主键';
COMMENT ON COLUMN dwd.enterprise_news.source_created_time IS 'ODS原始入库时间（业务字段）';
COMMENT ON COLUMN dwd.enterprise_news.create_time IS '记录创建时间';
COMMENT ON COLUMN dwd.enterprise_news.update_time IS '记录更新时间（ETL）';

CREATE INDEX IF NOT EXISTS idx_news_org_date ON dwd.enterprise_news (org_id, news_date DESC);


-- ============================================================
-- 10. enterprise_industry_chain（企业产业链归属，季更）
-- ============================================================
CREATE TABLE IF NOT EXISTS dwd.enterprise_industry_chain (
    id              BIGSERIAL       NOT NULL,
    org_id          VARCHAR(64)     NOT NULL,
    enterprise_code VARCHAR(64),
    chain_code      VARCHAR(64)     NOT NULL,
    chain_name      VARCHAR(255)    NOT NULL,
    node_id         VARCHAR(64),
    node_name       VARCHAR(255),
    node_stage      VARCHAR(20),
    chain_score     NUMERIC(10,2),
    create_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_enterprise_industry_chain PRIMARY KEY (id),
    CONSTRAINT fk_ind_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE,
    CONSTRAINT uk_ind_chain UNIQUE (org_id, chain_code, node_id)
);

COMMENT ON TABLE  dwd.enterprise_industry_chain IS '企业产业链归属表（季更）';
COMMENT ON COLUMN dwd.enterprise_industry_chain.id IS '自增主键';
COMMENT ON COLUMN dwd.enterprise_industry_chain.node_stage IS '环节（上游/中游/下游）';
COMMENT ON COLUMN dwd.enterprise_industry_chain.create_time IS '记录创建时间';
COMMENT ON COLUMN dwd.enterprise_industry_chain.update_time IS '记录更新时间（ETL）';

CREATE INDEX IF NOT EXISTS idx_ind_org ON dwd.enterprise_industry_chain (org_id);
CREATE INDEX IF NOT EXISTS idx_ind_chain_code ON dwd.enterprise_industry_chain (chain_code);


-- ============================================================
-- ============================================================
-- 司法风险模块（18类完全独立表 + 通用字典 + 通用统计）
-- 设计考量: 2亿企业下司法明细可能达十亿级，合并宽表会严重膨胀
--           各类司法数据查询模式独立（按org_id查某类风险列表）
--           统计需求通过通用统计表预聚合，不扫明细表
-- ============================================================
-- ============================================================


-- ============================================================
-- 11. risk_type_dict（风险类型字典表）
--     通用字典，所有司法/风险类型统一注册
-- ============================================================
CREATE TABLE IF NOT EXISTS dwd.risk_type_dict (
    id              BIGSERIAL       NOT NULL,
    risk_type       VARCHAR(50)     NOT NULL,
    risk_category   VARCHAR(50)     NOT NULL,
    risk_name       VARCHAR(100)    NOT NULL,
    ods_source_table VARCHAR(255)   NOT NULL,
    event_date_field VARCHAR(100),
    sort_order      INTEGER,
    is_active       SMALLINT        NOT NULL DEFAULT 1,
    create_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_risk_type_dict PRIMARY KEY (id),
    CONSTRAINT uk_risk_type UNIQUE (risk_type)
);

COMMENT ON TABLE  dwd.risk_type_dict IS '风险类型字典表（通用，司法/经营异常/行政处罚等）';
COMMENT ON COLUMN dwd.risk_type_dict.risk_type IS '风险类型编码（唯一）';
COMMENT ON COLUMN dwd.risk_type_dict.risk_category IS '风险大类（judicial司法/risk经营风险/penalty处罚）';
COMMENT ON COLUMN dwd.risk_type_dict.risk_name IS '风险类型中文名称';
COMMENT ON COLUMN dwd.risk_type_dict.ods_source_table IS 'ODS来源表名';
COMMENT ON COLUMN dwd.risk_type_dict.event_date_field IS '事件日期取值字段名';

-- 初始化字典数据
INSERT INTO dwd.risk_type_dict (risk_type, risk_category, risk_name, ods_source_table, event_date_field, sort_order) VALUES
('judicial_case',     'judicial', '司法案件',       'dwd_org_opt_judicial_case',              'procedure_date',       1),
('dishonest',         'judicial', '失信被执行人',   'dwd_org_risk_shixin',                    'publish_date',         2),
('executed',          'judicial', '被执行人',       'dwd_org_risk_zhixing',                   'filing_date',          3),
('limit_high',        'judicial', '限制高消费',     'dwd_org_risk_xianxiao',                  'filing_date',          4),
('lawsuit',           'judicial', '裁判文书',       'dwd_org_risk_lawsuit',                   'judgment_date',        5),
('court_filed',       'judicial', '法院立案',       'dwd_org_risk_court_filed_case',          'filing_date',          6),
('court_notice',      'judicial', '开庭公告',       'dwd_org_risk_court_notice',              'hearing_date',         7),
('court_announcement','judicial', '法院公告',       'dwd_org_risk_court_announcement',        'publish_date',         8),
('equity_freeze',     'judicial', '股权冻结',       'dwd_org_company_justice',                NULL,                   9),
('equity_pledge',     'judicial', '股权出质',       'dwd_org_company_pledge',                 'pledge_reg_date',     10),
('zhongben',          'judicial', '终本案件',       'dwd_org_risk_zhongben',                  'filing_date',         11),
('chattel_mortgage',  'judicial', '动产抵押',       'dwd_org_company_chattel',                'reg_date',            12),
('judicial_sale',     'judicial', '司法拍卖',       'dwd_org_tb_judicial_sale',               'notice_time',         13),
('bankruptcy',        'judicial', '破产案件',       'dwd_org_bankruptcy_public_cases',        'public_date',         14),
('abnormal',          'risk',     '经营异常',       'dwd_org_company_abnormal',               'abn_date',            15),
('punishment',        'penalty',  '行政处罚',       'dwd_org_company_punish',                 'penalty_date',        16),
('illegal',           'penalty',  '严重违法',       'dwd_org_company_illegal',                'abn_date',            17),
('tax_punish',        'penalty',  '税收违法',       'dwd_org_risk_tax_punish',                'publish_date',        18)
ON CONFLICT (risk_type) DO NOTHING;


-- ============================================================
-- 12. enterprise_risk_summary（企业风险统计汇总表）
--     按 org_id × risk_type 预聚合，供检索页筛选 + 详情页计数
--     避免每次扫十亿级明细表做 COUNT
-- ============================================================
CREATE TABLE IF NOT EXISTS dwd.enterprise_risk_summary (
    id              BIGSERIAL       NOT NULL,
    org_id          VARCHAR(64)     NOT NULL,
    risk_type       VARCHAR(50)     NOT NULL,
    total_count     INTEGER         NOT NULL DEFAULT 0,
    current_count   INTEGER         NOT NULL DEFAULT 0,
    history_count   INTEGER         NOT NULL DEFAULT 0,
    latest_date     DATE,
    create_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_enterprise_risk_summary PRIMARY KEY (id),
    CONSTRAINT uk_risk_summary UNIQUE (org_id, risk_type),
    CONSTRAINT fk_risk_sum_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE,
    CONSTRAINT fk_risk_sum_type FOREIGN KEY (risk_type) REFERENCES dwd.risk_type_dict(risk_type)
);

COMMENT ON TABLE  dwd.enterprise_risk_summary IS '企业风险统计汇总表（按org_id×risk_type预聚合）';
COMMENT ON COLUMN dwd.enterprise_risk_summary.total_count IS '该类型风险总数';
COMMENT ON COLUMN dwd.enterprise_risk_summary.current_count IS '当前有效数（is_history=0）';
COMMENT ON COLUMN dwd.enterprise_risk_summary.history_count IS '历史数（is_history=1）';
COMMENT ON COLUMN dwd.enterprise_risk_summary.latest_date IS '最近一次事件日期';

CREATE INDEX IF NOT EXISTS idx_risk_sum_type ON dwd.enterprise_risk_summary (risk_type);


-- ============================================================
-- 13-30. 司法风险明细表（18张独立表）
--   每张表只存该类型核心字段 + detail_json存完整原始记录
--   按 org_id 查询，各表独立索引，互不影响
-- ============================================================

-- 13. judicial_case 司法案件
CREATE TABLE IF NOT EXISTS dwd.risk_judicial_case (
    id              BIGSERIAL       NOT NULL,
    org_id          VARCHAR(64)     NOT NULL,
    case_id         VARCHAR(255),
    case_no         VARCHAR(255),
    case_title      TEXT,
    case_type_tag   VARCHAR(255),
    case_cause      VARCHAR(500),
    case_role       VARCHAR(255),
    current_procedure VARCHAR(255),
    procedure_date  DATE,
    is_history      SMALLINT,
    detail_json     TEXT,
    data_source     VARCHAR(100),
    create_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_risk_judicial_case PRIMARY KEY (id),
    CONSTRAINT fk_rjc_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE
);
COMMENT ON TABLE dwd.risk_judicial_case IS '司法案件明细表';
CREATE INDEX IF NOT EXISTS idx_rjc_org_date ON dwd.risk_judicial_case (org_id, procedure_date DESC);

-- 14. dishonest 失信被执行人
CREATE TABLE IF NOT EXISTS dwd.risk_dishonest (
    id              BIGSERIAL       NOT NULL,
    org_id          VARCHAR(64)     NOT NULL,
    dishonest_id    VARCHAR(255),
    case_no         VARCHAR(255),
    exec_court      VARCHAR(255),
    legal_obligation TEXT,
    fulfillment_status TEXT,
    dishonest_behavior TEXT,
    publish_date    DATE,
    filing_date     DATE,
    is_history      SMALLINT,
    detail_json     TEXT,
    data_source     VARCHAR(100),
    create_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_risk_dishonest PRIMARY KEY (id),
    CONSTRAINT fk_rdis_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE
);
COMMENT ON TABLE dwd.risk_dishonest IS '失信被执行人明细表';
CREATE INDEX IF NOT EXISTS idx_rdis_org_date ON dwd.risk_dishonest (org_id, publish_date DESC);

-- 15. executed 被执行人
CREATE TABLE IF NOT EXISTS dwd.risk_executed (
    id              BIGSERIAL       NOT NULL,
    org_id          VARCHAR(64)     NOT NULL,
    exec_person_id  VARCHAR(255),
    case_no         VARCHAR(255),
    exec_court      VARCHAR(255),
    exec_status     VARCHAR(255),
    exec_target     VARCHAR(255),
    filing_date     DATE,
    is_history      SMALLINT,
    detail_json     TEXT,
    data_source     VARCHAR(100),
    create_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_risk_executed PRIMARY KEY (id),
    CONSTRAINT fk_rexec_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE
);
COMMENT ON TABLE dwd.risk_executed IS '被执行人明细表';
COMMENT ON COLUMN dwd.risk_executed.exec_target IS '执行标的（⚠️ODS为VARCHAR文本，非金额数值）';
CREATE INDEX IF NOT EXISTS idx_rexec_org_date ON dwd.risk_executed (org_id, filing_date DESC);

-- 16. limit_high 限制高消费
CREATE TABLE IF NOT EXISTS dwd.risk_limit_high (
    id              BIGSERIAL       NOT NULL,
    org_id          VARCHAR(64)     NOT NULL,
    xhfgk_id        VARCHAR(255),
    rhc_person_name VARCHAR(255),
    case_no         VARCHAR(255),
    filing_date     DATE,
    doc_url         TEXT,
    is_history      SMALLINT,
    detail_json     TEXT,
    data_source     VARCHAR(100),
    create_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_risk_limit_high PRIMARY KEY (id),
    CONSTRAINT fk_rlh_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE
);
COMMENT ON TABLE dwd.risk_limit_high IS '限制高消费明细表';
CREATE INDEX IF NOT EXISTS idx_rlh_org_date ON dwd.risk_limit_high (org_id, filing_date DESC);

-- 17a. lawsuit 裁判文书-案件详情（一行一个案件）
CREATE TABLE IF NOT EXISTS dwd.risk_lawsuit (
    id              BIGSERIAL       NOT NULL,
    judgment_doc_id VARCHAR(255)    NOT NULL,
    case_no         VARCHAR(255),
    case_type       VARCHAR(255),
    court_name      VARCHAR(255),
    trial_procedure VARCHAR(255),
    judgment_date   DATE,
    publish_date    DATE,
    case_cause      VARCHAR(500),
    doc_title       TEXT,
    detail_json     TEXT,
    data_source     VARCHAR(100),
    create_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_risk_lawsuit PRIMARY KEY (id),
    CONSTRAINT uk_risk_lawsuit_doc UNIQUE (judgment_doc_id)
);
COMMENT ON TABLE dwd.risk_lawsuit IS '裁判文书案件详情表（一行一个案件，不含企业关联）';
CREATE INDEX IF NOT EXISTS idx_rlaw_date ON dwd.risk_lawsuit (judgment_date DESC);

-- 17b. lawsuit_party 裁判文书-当事人关联（一行一个当事人）
CREATE TABLE IF NOT EXISTS dwd.risk_lawsuit_party (
    id              BIGSERIAL       NOT NULL,
    judgment_doc_id VARCHAR(255)    NOT NULL,
    org_id          VARCHAR(64)     NOT NULL,
    party_role      VARCHAR(50),
    is_history      SMALLINT,
    create_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_risk_lawsuit_party PRIMARY KEY (id),
    CONSTRAINT fk_rlawp_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE
);
COMMENT ON TABLE dwd.risk_lawsuit_party IS '裁判文书当事人关联表（一行一个当事人，关联企业和案件）';
CREATE INDEX IF NOT EXISTS idx_rlawp_org ON dwd.risk_lawsuit_party (org_id);
CREATE INDEX IF NOT EXISTS idx_rlawp_doc ON dwd.risk_lawsuit_party (judgment_doc_id);

-- 18a. court_filed 法院立案-案件详情（一行一个案件）
CREATE TABLE IF NOT EXISTS dwd.risk_court_filed (
    id              BIGSERIAL       NOT NULL,
    case_unique_id  VARCHAR(255)    NOT NULL,
    case_no         VARCHAR(255),
    case_cause      VARCHAR(500),
    trial_procedure VARCHAR(255),
    case_status     VARCHAR(255),
    filing_date     DATE,
    closing_date    DATE,
    hearing_date    DATE,
    court_name      VARCHAR(255),
    detail_json     TEXT,
    data_source     VARCHAR(100),
    create_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_risk_court_filed PRIMARY KEY (id),
    CONSTRAINT uk_risk_court_filed_case UNIQUE (case_unique_id)
);
COMMENT ON TABLE dwd.risk_court_filed IS '法院立案案件详情表（一行一个案件，不含企业关联）';
CREATE INDEX IF NOT EXISTS idx_rcf_date ON dwd.risk_court_filed (filing_date DESC);

-- 18b. court_filed_party 法院立案-当事人关联
CREATE TABLE IF NOT EXISTS dwd.risk_court_filed_party (
    id              BIGSERIAL       NOT NULL,
    case_unique_id  VARCHAR(255)    NOT NULL,
    org_id          VARCHAR(64)     NOT NULL,
    party_role      VARCHAR(50),
    is_history      SMALLINT,
    create_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_risk_court_filed_party PRIMARY KEY (id),
    CONSTRAINT fk_rcfp_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE
);
COMMENT ON TABLE dwd.risk_court_filed_party IS '法院立案当事人关联表';
CREATE INDEX IF NOT EXISTS idx_rcfp_org ON dwd.risk_court_filed_party (org_id);
CREATE INDEX IF NOT EXISTS idx_rcfp_case ON dwd.risk_court_filed_party (case_unique_id);

-- 19a. court_notice 开庭公告-案件详情（一行一个公告）
CREATE TABLE IF NOT EXISTS dwd.risk_court_notice (
    id              BIGSERIAL       NOT NULL,
    notice_id       VARCHAR(255)    NOT NULL,
    case_no         VARCHAR(255),
    case_cause      VARCHAR(500),
    court_name      VARCHAR(255),
    hearing_date    DATE,
    detail_json     TEXT,
    data_source     VARCHAR(100),
    create_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_risk_court_notice PRIMARY KEY (id),
    CONSTRAINT uk_risk_court_notice_id UNIQUE (notice_id)
);
COMMENT ON TABLE dwd.risk_court_notice IS '开庭公告案件详情表（一行一个公告，不含企业关联）';
CREATE INDEX IF NOT EXISTS idx_rcn_date ON dwd.risk_court_notice (hearing_date DESC);

-- 19b. court_notice_party 开庭公告-当事人关联
CREATE TABLE IF NOT EXISTS dwd.risk_court_notice_party (
    id              BIGSERIAL       NOT NULL,
    notice_id       VARCHAR(255)    NOT NULL,
    org_id          VARCHAR(64)     NOT NULL,
    party_role      VARCHAR(50),
    is_history      SMALLINT,
    create_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_risk_court_notice_party PRIMARY KEY (id),
    CONSTRAINT fk_rcnp_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE
);
COMMENT ON TABLE dwd.risk_court_notice_party IS '开庭公告当事人关联表';
CREATE INDEX IF NOT EXISTS idx_rcnp_org ON dwd.risk_court_notice_party (org_id);
CREATE INDEX IF NOT EXISTS idx_rcnp_notice ON dwd.risk_court_notice_party (notice_id);

-- 20a. court_announcement 法院公告-案件详情（一行一个公告）
CREATE TABLE IF NOT EXISTS dwd.risk_court_announcement (
    id              BIGSERIAL       NOT NULL,
    notice_id       VARCHAR(255)    NOT NULL,
    notice_name     VARCHAR(255),
    notice_type     VARCHAR(255),
    case_no         VARCHAR(255),
    court_name      VARCHAR(255),
    notice_date     DATE,
    publish_date    DATE,
    detail_json     TEXT,
    data_source     VARCHAR(100),
    create_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_risk_court_announcement PRIMARY KEY (id),
    CONSTRAINT uk_risk_court_ann_id UNIQUE (notice_id)
);
COMMENT ON TABLE dwd.risk_court_announcement IS '法院公告案件详情表（一行一个公告，不含企业关联）';
CREATE INDEX IF NOT EXISTS idx_rca_date ON dwd.risk_court_announcement (publish_date DESC);

-- 20b. court_announcement_party 法院公告-当事人关联
CREATE TABLE IF NOT EXISTS dwd.risk_court_announcement_party (
    id              BIGSERIAL       NOT NULL,
    notice_id       VARCHAR(255)    NOT NULL,
    org_id          VARCHAR(64)     NOT NULL,
    party_role      VARCHAR(50),
    is_history      SMALLINT,
    create_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_risk_court_ann_party PRIMARY KEY (id),
    CONSTRAINT fk_rcap_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE
);
COMMENT ON TABLE dwd.risk_court_announcement_party IS '法院公告当事人关联表';
CREATE INDEX IF NOT EXISTS idx_rcap_org ON dwd.risk_court_announcement_party (org_id);
CREATE INDEX IF NOT EXISTS idx_rcap_notice ON dwd.risk_court_announcement_party (notice_id);

-- 21. equity_freeze 股权冻结
CREATE TABLE IF NOT EXISTS dwd.risk_equity_freeze (
    id                  BIGSERIAL       NOT NULL,
    org_id              VARCHAR(64)     NOT NULL,
    judicial_assist_id  VARCHAR(255),
    executed_person     VARCHAR(255),
    equity_amount       VARCHAR(255),
    exec_court          VARCHAR(255),
    type_status         VARCHAR(255),
    status              VARCHAR(255),
    is_history          SMALLINT,
    detail_json         TEXT,
    data_source         VARCHAR(100),
    create_time         TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time         TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_risk_equity_freeze PRIMARY KEY (id),
    CONSTRAINT fk_ref_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE
);
COMMENT ON TABLE dwd.risk_equity_freeze IS '股权冻结明细表（⚠️ODS无日期字段，event_date留空）';
COMMENT ON COLUMN dwd.risk_equity_freeze.equity_amount IS '股权数额（⚠️ODS为VARCHAR文本）';
CREATE INDEX IF NOT EXISTS idx_ref_org ON dwd.risk_equity_freeze (org_id);

-- 22. equity_pledge 股权出质
CREATE TABLE IF NOT EXISTS dwd.risk_equity_pledge (
    id                  BIGSERIAL       NOT NULL,
    org_id              VARCHAR(64)     NOT NULL,
    pledge_id           VARCHAR(255),
    reg_no              VARCHAR(255),
    pledgor             VARCHAR(255),
    pledgee             VARCHAR(255),
    equity_amount       VARCHAR(255),
    pledge_reg_date     DATE,
    status              VARCHAR(255),
    is_history          SMALLINT,
    detail_json         TEXT,
    data_source         VARCHAR(100),
    create_time         TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time         TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_risk_equity_pledge PRIMARY KEY (id),
    CONSTRAINT fk_rep_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE
);
COMMENT ON TABLE dwd.risk_equity_pledge IS '股权出质明细表';
CREATE INDEX IF NOT EXISTS idx_rep_org_date ON dwd.risk_equity_pledge (org_id, pledge_reg_date DESC);

-- 23. zhongben 终本案件
CREATE TABLE IF NOT EXISTS dwd.risk_zhongben (
    id                  BIGSERIAL       NOT NULL,
    org_id              VARCHAR(64)     NOT NULL,
    case_no             VARCHAR(255),
    exec_court          VARCHAR(255),
    filing_date         DATE,
    termination_date    DATE,
    exec_target_amount  NUMERIC(18,2),
    unfulfilled_amount  NUMERIC(18,2),
    is_history          SMALLINT,
    detail_json         TEXT,
    data_source         VARCHAR(100),
    create_time         TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time         TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_risk_zhongben PRIMARY KEY (id),
    CONSTRAINT fk_rzb_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE
);
COMMENT ON TABLE dwd.risk_zhongben IS '终本案件明细表';
COMMENT ON COLUMN dwd.risk_zhongben.exec_target_amount IS '执行标的金额（万元）';
COMMENT ON COLUMN dwd.risk_zhongben.unfulfilled_amount IS '未履行标的金额（万元）';
CREATE INDEX IF NOT EXISTS idx_rzb_org_date ON dwd.risk_zhongben (org_id, filing_date DESC);

-- 24. chattel_mortgage 动产抵押
CREATE TABLE IF NOT EXISTS dwd.risk_chattel_mortgage (
    id                  BIGSERIAL       NOT NULL,
    org_id              VARCHAR(64)     NOT NULL,
    reg_no              VARCHAR(255),
    reg_date            DATE,
    reg_org             VARCHAR(255),
    guarantee_type      VARCHAR(255),
    guarantee_amount    NUMERIC(18,2),
    guarantee_scope     TEXT,
    public_date         DATE,
    status              VARCHAR(255),
    is_history          SMALLINT,
    detail_json         TEXT,
    data_source         VARCHAR(100),
    create_time         TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time         TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_risk_chattel_mortgage PRIMARY KEY (id),
    CONSTRAINT fk_rcm_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE
);
COMMENT ON TABLE dwd.risk_chattel_mortgage IS '动产抵押明细表';
COMMENT ON COLUMN dwd.risk_chattel_mortgage.guarantee_amount IS '被担保债权数额（万元）';
CREATE INDEX IF NOT EXISTS idx_rcm_org_date ON dwd.risk_chattel_mortgage (org_id, reg_date DESC);

-- 25a. judicial_sale 司法拍卖-案件详情（一行一个拍品）
CREATE TABLE IF NOT EXISTS dwd.risk_judicial_sale (
    id                  BIGSERIAL       NOT NULL,
    notice_id           VARCHAR(255)    NOT NULL,
    notice_name         TEXT,
    asset_disposal_unit VARCHAR(255),
    notice_time         TIMESTAMP,
    auction_start_date  DATE,
    auction_end_date    DATE,
    source_website      VARCHAR(255),
    original_link       TEXT,
    detail_json         TEXT,
    data_source         VARCHAR(100),
    create_time         TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time         TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_risk_judicial_sale PRIMARY KEY (id),
    CONSTRAINT uk_risk_jud_sale_id UNIQUE (notice_id)
);
COMMENT ON TABLE dwd.risk_judicial_sale IS '司法拍卖案件详情表（一行一个拍品，不含企业关联）';
CREATE INDEX IF NOT EXISTS idx_rjs_date ON dwd.risk_judicial_sale (notice_time DESC);

-- 25b. judicial_sale_party 司法拍卖-当事人关联
CREATE TABLE IF NOT EXISTS dwd.risk_judicial_sale_party (
    id              BIGSERIAL       NOT NULL,
    notice_id       VARCHAR(255)    NOT NULL,
    org_id          VARCHAR(64)     NOT NULL,
    party_role      VARCHAR(50),
    is_history      SMALLINT,
    create_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_risk_jud_sale_party PRIMARY KEY (id),
    CONSTRAINT fk_rjsp_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE
);
COMMENT ON TABLE dwd.risk_judicial_sale_party IS '司法拍卖当事人关联表';
CREATE INDEX IF NOT EXISTS idx_rjsp_org ON dwd.risk_judicial_sale_party (org_id);
CREATE INDEX IF NOT EXISTS idx_rjsp_notice ON dwd.risk_judicial_sale_party (notice_id);

-- 26a. bankruptcy 破产案件-案件详情（一行一个案件）
CREATE TABLE IF NOT EXISTS dwd.risk_bankruptcy (
    id                  BIGSERIAL       NOT NULL,
    case_no             VARCHAR(255)    NOT NULL,
    case_type           VARCHAR(255),
    handling_court      VARCHAR(255),
    public_date         DATE,
    detail_json         TEXT,
    data_source         VARCHAR(100),
    create_time         TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time         TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_risk_bankruptcy PRIMARY KEY (id),
    CONSTRAINT uk_risk_bankruptcy_case UNIQUE (case_no)
);
COMMENT ON TABLE dwd.risk_bankruptcy IS '破产案件详情表（一行一个案件，不含企业关联）';
CREATE INDEX IF NOT EXISTS idx_rbk_date ON dwd.risk_bankruptcy (public_date DESC);

-- 26b. bankruptcy_party 破产案件-当事人关联
CREATE TABLE IF NOT EXISTS dwd.risk_bankruptcy_party (
    id              BIGSERIAL       NOT NULL,
    case_no         VARCHAR(255)    NOT NULL,
    org_id          VARCHAR(64)     NOT NULL,
    party_role      VARCHAR(50),
    is_history      SMALLINT,
    create_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_risk_bankruptcy_party PRIMARY KEY (id),
    CONSTRAINT fk_rbkp_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE
);
COMMENT ON TABLE dwd.risk_bankruptcy_party IS '破产案件当事人关联表';
CREATE INDEX IF NOT EXISTS idx_rbkp_org ON dwd.risk_bankruptcy_party (org_id);
CREATE INDEX IF NOT EXISTS idx_rbkp_case ON dwd.risk_bankruptcy_party (case_no);

-- 27. abnormal 经营异常
CREATE TABLE IF NOT EXISTS dwd.risk_abnormal (
    id              BIGSERIAL       NOT NULL,
    org_id          VARCHAR(64)     NOT NULL,
    abnormal_id     VARCHAR(255),
    abn_date        DATE,
    remove_date     DATE,
    reason          TEXT,
    is_history      SMALLINT,
    detail_json     TEXT,
    data_source     VARCHAR(100),
    create_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_risk_abnormal PRIMARY KEY (id),
    CONSTRAINT fk_rabn_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE
);
COMMENT ON TABLE dwd.risk_abnormal IS '经营异常明细表';
CREATE INDEX IF NOT EXISTS idx_rabn_org_date ON dwd.risk_abnormal (org_id, abn_date DESC);

-- 28. punishment 行政处罚
CREATE TABLE IF NOT EXISTS dwd.risk_punishment (
    id              BIGSERIAL       NOT NULL,
    org_id          VARCHAR(64)     NOT NULL,
    penalty_id      VARCHAR(255),
    decision_no     VARCHAR(255),
    penalty_date    DATE,
    public_date     DATE,
    fine_amount     NUMERIC(18,2),
    confiscate_amount NUMERIC(18,2),
    penalty_reason  TEXT,
    is_history      SMALLINT,
    detail_json     TEXT,
    data_source     VARCHAR(100),
    create_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_risk_punishment PRIMARY KEY (id),
    CONSTRAINT fk_rpn_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE
);
COMMENT ON TABLE dwd.risk_punishment IS '行政处罚明细表';
COMMENT ON COLUMN dwd.risk_punishment.fine_amount IS '罚款金额（万元）';
COMMENT ON COLUMN dwd.risk_punishment.confiscate_amount IS '没收金额（万元）';
CREATE INDEX IF NOT EXISTS idx_rpn_org_date ON dwd.risk_punishment (org_id, penalty_date DESC);

-- 29. illegal 严重违法
CREATE TABLE IF NOT EXISTS dwd.risk_illegal (
    id              BIGSERIAL       NOT NULL,
    org_id          VARCHAR(64)     NOT NULL,
    sv_id           VARCHAR(255),
    abn_date        DATE,
    remove_date     DATE,
    reason          TEXT,
    is_history      SMALLINT,
    detail_json     TEXT,
    data_source     VARCHAR(100),
    create_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_risk_illegal PRIMARY KEY (id),
    CONSTRAINT fk_ril_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE
);
COMMENT ON TABLE dwd.risk_illegal IS '严重违法明细表';
CREATE INDEX IF NOT EXISTS idx_ril_org_date ON dwd.risk_illegal (org_id, abn_date DESC);

-- 30. tax_punish 税收违法
CREATE TABLE IF NOT EXISTS dwd.risk_tax_punish (
    id              BIGSERIAL       NOT NULL,
    org_id          VARCHAR(64)     NOT NULL,
    tax_vio_id      VARCHAR(255),
    case_no         VARCHAR(255),
    publish_date    DATE,
    tax_vio_type    VARCHAR(255),
    is_history      SMALLINT,
    detail_json     TEXT,
    data_source     VARCHAR(100),
    create_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_risk_tax_punish PRIMARY KEY (id),
    CONSTRAINT fk_rtp_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE
);
COMMENT ON TABLE dwd.risk_tax_punish IS '税收违法明细表（⚠️ODS无罚款金额字段）';
CREATE INDEX IF NOT EXISTS idx_rtp_org_date ON dwd.risk_tax_punish (org_id, publish_date DESC);


-- ============================================================
-- 38. enterprise_executive（企业高管信息，季更）
--    ODS: dwd_org_executive_info
-- ============================================================
CREATE TABLE IF NOT EXISTS dwd.enterprise_executive (
    id              BIGSERIAL       NOT NULL,
    org_id          VARCHAR(64)     NOT NULL,
    executive_name  VARCHAR(255)    NOT NULL,
    position        VARCHAR(255),
    data_source     VARCHAR(100),
    create_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_enterprise_executive PRIMARY KEY (id),
    CONSTRAINT fk_exec_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE,
    CONSTRAINT uk_exec UNIQUE (org_id, executive_name, position)
);
COMMENT ON TABLE dwd.enterprise_executive IS '企业高管信息表（季更）';
COMMENT ON COLUMN dwd.enterprise_executive.executive_name IS '高管姓名';
COMMENT ON COLUMN dwd.enterprise_executive.position IS '职位名称';
CREATE INDEX IF NOT EXISTS idx_exec_org ON dwd.enterprise_executive (org_id);


-- ============================================================
-- 39. enterprise_financing（企业融资事件，日追加）
--    ODS: dwd_org_financing_info
-- ============================================================
CREATE TABLE IF NOT EXISTS dwd.enterprise_financing (
    id                  BIGSERIAL       NOT NULL,
    org_id              VARCHAR(64)     NOT NULL,
    funding_round       VARCHAR(255),
    funding_amount      NUMERIC(18,2),
    funding_currency_code VARCHAR(20),
    post_valuation      NUMERIC(18,2),
    completion_date     DATE,
    investors_name      TEXT,
    data_source         VARCHAR(100),
    create_time         TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time         TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_enterprise_financing PRIMARY KEY (id),
    CONSTRAINT fk_fin_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE
);
COMMENT ON TABLE dwd.enterprise_financing IS '企业融资事件表（日追加）';
COMMENT ON COLUMN dwd.enterprise_financing.funding_amount IS '获投金额（元）';
COMMENT ON COLUMN dwd.enterprise_financing.post_valuation IS '投后估值（元）';
COMMENT ON COLUMN dwd.enterprise_financing.investors_name IS '投资方列表（逗号分隔）';
CREATE INDEX IF NOT EXISTS idx_fin_org_date ON dwd.enterprise_financing (org_id, completion_date DESC);


-- ============================================================
-- 40. enterprise_innovation_carrier（企业创新载体，季更）
--    ODS: dwd_innovation_carrier
-- ============================================================
CREATE TABLE IF NOT EXISTS dwd.enterprise_innovation_carrier (
    id              BIGSERIAL       NOT NULL,
    org_id          VARCHAR(64)     NOT NULL,
    carrier_type    VARCHAR(255),
    carrier_name    VARCHAR(500),
    carrier_level   VARCHAR(50),
    establish_year  VARCHAR(20),
    region          VARCHAR(255),
    publish_org     VARCHAR(500),
    publish_date    VARCHAR(20),
    source_url      TEXT,
    create_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_enterprise_innovation_carrier PRIMARY KEY (id),
    CONSTRAINT fk_ic_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE,
    CONSTRAINT uk_ic UNIQUE (org_id, carrier_name, carrier_type)
);
COMMENT ON TABLE dwd.enterprise_innovation_carrier IS '企业创新载体表（季更）';
COMMENT ON COLUMN dwd.enterprise_innovation_carrier.carrier_type IS '载体类型（重点实验室/工程中心/技术中心等）';
COMMENT ON COLUMN dwd.enterprise_innovation_carrier.carrier_level IS '载体级别（国家级/省级/市级）';
COMMENT ON COLUMN dwd.enterprise_innovation_carrier.establish_year IS '组建/认定年份';
CREATE INDEX IF NOT EXISTS idx_ic_org ON dwd.enterprise_innovation_carrier (org_id);
CREATE INDEX IF NOT EXISTS idx_ic_type ON dwd.enterprise_innovation_carrier (carrier_type);


-- ============================================================
-- 41. enterprise_invest（企业对外投资，季更）
--    ODS: dwd_org_invest_info
--    同时支撑详情页供应链关系Tab（投资方→被投企业）
-- ============================================================
CREATE TABLE IF NOT EXISTS dwd.enterprise_invest (
    id                  BIGSERIAL       NOT NULL,
    org_id              VARCHAR(64)     NOT NULL,
    inv_org_id          VARCHAR(64),
    inv_name            VARCHAR(255),
    inv_external_id     VARCHAR(64),
    investment_amount   NUMERIC(18,2),
    investment_ratio    NUMERIC(8,4),
    data_source         VARCHAR(100),
    create_time         TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time         TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_enterprise_invest PRIMARY KEY (id),
    CONSTRAINT fk_inv_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE,
    CONSTRAINT uk_inv UNIQUE (org_id, inv_org_id)
);
COMMENT ON TABLE dwd.enterprise_invest IS '企业对外投资表（季更，同时支撑供应链关系Tab）';
COMMENT ON COLUMN dwd.enterprise_invest.org_id IS '投资方机构id';
COMMENT ON COLUMN dwd.enterprise_invest.inv_org_id IS '被投企业id';
COMMENT ON COLUMN dwd.enterprise_invest.inv_name IS '被投资企业名称';
COMMENT ON COLUMN dwd.enterprise_invest.investment_amount IS '投资金额（元）';
COMMENT ON COLUMN dwd.enterprise_invest.investment_ratio IS '股权占比（%）';
CREATE INDEX IF NOT EXISTS idx_inv_org ON dwd.enterprise_invest (org_id);
CREATE INDEX IF NOT EXISTS idx_inv_inv_org ON dwd.enterprise_invest (inv_org_id);


-- ============================================================
-- 42. enterprise_score（企业评分，ADS层，算法侧产出后ETL写入）
--    算法侧（ai-service）计算后写入，ES同步时读取此表写入ES顶层字段
-- ============================================================
CREATE TABLE IF NOT EXISTS dwd.enterprise_score (
    id                      BIGSERIAL       NOT NULL,
    org_id                  VARCHAR(64)     NOT NULL,
    competitiveness_score   NUMERIC(6,2),
    enterprise_scale        VARCHAR(20),
    chain_position_text     VARCHAR(255),
    risk_level              VARCHAR(20),
    score_version           VARCHAR(20),
    score_date              DATE,
    create_time             TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time             TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_enterprise_score PRIMARY KEY (id),
    CONSTRAINT fk_score_base FOREIGN KEY (org_id) REFERENCES dwd.enterprise_base(org_id) ON DELETE CASCADE,
    CONSTRAINT uk_score UNIQUE (org_id)
);
COMMENT ON TABLE dwd.enterprise_score IS '企业评分表（ADS层，算法侧产出后ETL写入，ES同步时读取）';
COMMENT ON COLUMN dwd.enterprise_score.competitiveness_score IS '综合竞争力评分（0-100）';
COMMENT ON COLUMN dwd.enterprise_score.enterprise_scale IS '企业规模（大型/中型/小型/微型/规上）';
COMMENT ON COLUMN dwd.enterprise_score.chain_position_text IS '产业链位置文本（如"设计层 · 上游EDA"）';
COMMENT ON COLUMN dwd.enterprise_score.risk_level IS '风险等级（无风险/低风险/中风险/高风险）';
COMMENT ON COLUMN dwd.enterprise_score.score_version IS '评分模型版本';
COMMENT ON COLUMN dwd.enterprise_score.score_date IS '评分计算日期';
CREATE INDEX IF NOT EXISTS idx_score_org ON dwd.enterprise_score (org_id);


-- ============================================================
-- 建表完成校验
-- ============================================================
-- 查看所有已建表
-- SELECT table_name FROM information_schema.tables
-- WHERE table_schema = 'dwd' ORDER BY table_name;

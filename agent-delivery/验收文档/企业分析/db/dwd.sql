/*
 Navicat Premium Dump SQL

 Source Server         : GDF_PG
 Source Server Type    : PostgreSQL
 Source Server Version : 160004 (160004)
 Source Host           : 111.198.38.90:20644
 Source Catalog        : demo_gdf_data
 Source Schema         : dwd

 Target Server Type    : PostgreSQL
 Target Server Version : 160004 (160004)
 File Encoding         : 65001

 Date: 13/06/2026 16:35:12
*/


-- ----------------------------
-- Sequence structure for enterprise_business_tag_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."enterprise_business_tag_id_seq";
CREATE SEQUENCE "dwd"."enterprise_business_tag_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for enterprise_cooperation_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."enterprise_cooperation_id_seq";
CREATE SEQUENCE "dwd"."enterprise_cooperation_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for enterprise_finance_history_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."enterprise_finance_history_id_seq";
CREATE SEQUENCE "dwd"."enterprise_finance_history_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for enterprise_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."enterprise_id_seq";
CREATE SEQUENCE "dwd"."enterprise_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for enterprise_industry_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."enterprise_industry_id_seq";
CREATE SEQUENCE "dwd"."enterprise_industry_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for enterprise_parent_subsidiary_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."enterprise_parent_subsidiary_id_seq";
CREATE SEQUENCE "dwd"."enterprise_parent_subsidiary_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for enterprise_patent_history_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."enterprise_patent_history_id_seq";
CREATE SEQUENCE "dwd"."enterprise_patent_history_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for enterprise_supply_chain_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."enterprise_supply_chain_id_seq";
CREATE SEQUENCE "dwd"."enterprise_supply_chain_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for national_policy_distribution_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."national_policy_distribution_id_seq";
CREATE SEQUENCE "dwd"."national_policy_distribution_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_analysis_report_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_analysis_report_id_seq";
CREATE SEQUENCE "dwd"."policy_analysis_report_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_base_info_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_base_info_id_seq";
CREATE SEQUENCE "dwd"."policy_base_info_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_effect_eval_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_effect_eval_id_seq";
CREATE SEQUENCE "dwd"."policy_effect_eval_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_entity_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_entity_id_seq";
CREATE SEQUENCE "dwd"."policy_entity_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_entity_relation_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_entity_relation_id_seq";
CREATE SEQUENCE "dwd"."policy_entity_relation_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_entity_type_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_entity_type_id_seq";
CREATE SEQUENCE "dwd"."policy_entity_type_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_favorite_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_favorite_id_seq";
CREATE SEQUENCE "dwd"."policy_favorite_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_focus_result_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_focus_result_id_seq";
CREATE SEQUENCE "dwd"."policy_focus_result_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_intensity_eval_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_intensity_eval_id_seq";
CREATE SEQUENCE "dwd"."policy_intensity_eval_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_interpretation_report_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_interpretation_report_id_seq";
CREATE SEQUENCE "dwd"."policy_interpretation_report_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_latest_news_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_latest_news_id_seq";
CREATE SEQUENCE "dwd"."policy_latest_news_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_layout_recommend_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_layout_recommend_id_seq";
CREATE SEQUENCE "dwd"."policy_layout_recommend_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_level_indicator_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_level_indicator_id_seq";
CREATE SEQUENCE "dwd"."policy_level_indicator_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_opportunity_result_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_opportunity_result_id_seq";
CREATE SEQUENCE "dwd"."policy_opportunity_result_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_prediction_indicator_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_prediction_indicator_id_seq";
CREATE SEQUENCE "dwd"."policy_prediction_indicator_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_public_opinion_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_public_opinion_id_seq";
CREATE SEQUENCE "dwd"."policy_public_opinion_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_recommendation_report_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_recommendation_report_id_seq";
CREATE SEQUENCE "dwd"."policy_recommendation_report_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_search_condition_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_search_condition_id_seq";
CREATE SEQUENCE "dwd"."policy_search_condition_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_search_record_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_search_record_id_seq";
CREATE SEQUENCE "dwd"."policy_search_record_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_simulation_param_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_simulation_param_id_seq";
CREATE SEQUENCE "dwd"."policy_simulation_param_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_simulation_result_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_simulation_result_id_seq";
CREATE SEQUENCE "dwd"."policy_simulation_result_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_subscription_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_subscription_id_seq";
CREATE SEQUENCE "dwd"."policy_subscription_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_support_assessment_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_support_assessment_id_seq";
CREATE SEQUENCE "dwd"."policy_support_assessment_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_support_assessment_indicator_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_support_assessment_indicator_id_seq";
CREATE SEQUENCE "dwd"."policy_support_assessment_indicator_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_support_overview_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_support_overview_id_seq";
CREATE SEQUENCE "dwd"."policy_support_overview_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_support_rank_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_support_rank_id_seq";
CREATE SEQUENCE "dwd"."policy_support_rank_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_time_analysis_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_time_analysis_id_seq";
CREATE SEQUENCE "dwd"."policy_time_analysis_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_time_series_indicator_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_time_series_indicator_id_seq";
CREATE SEQUENCE "dwd"."policy_time_series_indicator_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_type_indicator_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_type_indicator_id_seq";
CREATE SEQUENCE "dwd"."policy_type_indicator_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for policy_weakness_result_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."policy_weakness_result_id_seq";
CREATE SEQUENCE "dwd"."policy_weakness_result_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for regional_policy_compare_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."regional_policy_compare_id_seq";
CREATE SEQUENCE "dwd"."regional_policy_compare_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for shenzhen_policy_compare_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."shenzhen_policy_compare_id_seq";
CREATE SEQUENCE "dwd"."shenzhen_policy_compare_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for shenzhen_policy_distribution_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."shenzhen_policy_distribution_id_seq";
CREATE SEQUENCE "dwd"."shenzhen_policy_distribution_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for shenzhen_policy_status_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."shenzhen_policy_status_id_seq";
CREATE SEQUENCE "dwd"."shenzhen_policy_status_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for tenant_info_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "dwd"."tenant_info_id_seq";
CREATE SEQUENCE "dwd"."tenant_info_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Table structure for enterprise
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."enterprise";
CREATE TABLE "dwd"."enterprise" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".enterprise_id_seq'::regclass),
  "enterprise_code" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "enterprise_name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "enterprise_name_short" varchar(100) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "enterprise_name_en" varchar(255) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "legal_representative" varchar(100) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "registered_capital" numeric(20,2) DEFAULT NULL::numeric,
  "paid_in_capital" numeric(20,2) DEFAULT NULL::numeric,
  "registration_date" date,
  "business_status" varchar(20) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "enterprise_type" varchar(50) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "industry_category" varchar(100) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "industry_code" varchar(20) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "business_scope" text COLLATE "pg_catalog"."default",
  "registered_address" varchar(500) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "headquarters_city" varchar(100) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "headquarters_district" varchar(100) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "headquarters_address" varchar(500) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "headquarters_lng" numeric(10,6) DEFAULT NULL::numeric,
  "headquarters_lat" numeric(10,6) DEFAULT NULL::numeric,
  "is_listed" int2 DEFAULT 0,
  "listed_market" varchar(50) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "listed_code" varchar(20) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "is_foreign" int2 DEFAULT 0,
  "is_high_tech" int2 DEFAULT 0,
  "is_sme" int2 DEFAULT 0,
  "is_little_giant" int2 DEFAULT 0,
  "little_giant_level" varchar(20) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "is_gazelle" int2 DEFAULT 0,
  "is_unicorn" int2 DEFAULT 0,
  "revenue_latest" numeric(20,2) DEFAULT NULL::numeric,
  "revenue_year" int4,
  "revenue_growth_rate" numeric(10,4) DEFAULT NULL::numeric,
  "net_profit" numeric(20,2) DEFAULT NULL::numeric,
  "profit_margin" numeric(10,4) DEFAULT NULL::numeric,
  "gross_margin" numeric(10,4) DEFAULT NULL::numeric,
  "market_share" numeric(10,4) DEFAULT NULL::numeric,
  "brand_score" numeric(10,2) DEFAULT NULL::numeric,
  "customer_concentration" numeric(10,4) DEFAULT NULL::numeric,
  "patent_apply_count" int4 DEFAULT 0,
  "patent_grant_count" int4 DEFAULT 0,
  "patent_valid_count" int4 DEFAULT 0,
  "patent_invention_count" int4 DEFAULT 0,
  "patent_citation_count" int4 DEFAULT 0,
  "rd_staff_count" int4 DEFAULT 0,
  "rd_staff_ratio" numeric(10,4) DEFAULT NULL::numeric,
  "rd_investment" numeric(20,2) DEFAULT NULL::numeric,
  "rd_investment_ratio" numeric(10,4) DEFAULT NULL::numeric,
  "core_tech_coverage" numeric(10,2) DEFAULT NULL::numeric,
  "tech_score" numeric(10,2) DEFAULT NULL::numeric,
  "business_score" numeric(10,2) DEFAULT NULL::numeric,
  "competitiveness_score" numeric(10,2) DEFAULT NULL::numeric,
  "innovation_index" numeric(10,2) DEFAULT NULL::numeric,
  "introduction_value" varchar(20) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "cultivation_priority" varchar(20) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "risk_level" varchar(20) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "data_source" varchar(100) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "data_source_url" varchar(500) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "data_collect_time" timestamp(6),
  "data_update_time" timestamp(6),
  "data_completeness" numeric(10,2) DEFAULT NULL::numeric,
  "data_confidence" numeric(10,2) DEFAULT NULL::numeric,
  "audit_status" varchar(20) COLLATE "pg_catalog"."default" DEFAULT '待审核'::character varying,
  "create_time" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;
COMMENT ON COLUMN "dwd"."enterprise"."id" IS '自增主键';
COMMENT ON COLUMN "dwd"."enterprise"."enterprise_code" IS '统一社会信用代码';
COMMENT ON COLUMN "dwd"."enterprise"."enterprise_name" IS '企业全称';
COMMENT ON COLUMN "dwd"."enterprise"."enterprise_name_short" IS '企业简称';
COMMENT ON COLUMN "dwd"."enterprise"."enterprise_name_en" IS '英文名称';
COMMENT ON COLUMN "dwd"."enterprise"."legal_representative" IS '法定代表人';
COMMENT ON COLUMN "dwd"."enterprise"."registered_capital" IS '注册资本（万元）';
COMMENT ON COLUMN "dwd"."enterprise"."paid_in_capital" IS '实缴资本（万元）';
COMMENT ON COLUMN "dwd"."enterprise"."registration_date" IS '成立日期';
COMMENT ON COLUMN "dwd"."enterprise"."business_status" IS '经营状态（在营/吊销/注销/迁出）';
COMMENT ON COLUMN "dwd"."enterprise"."enterprise_type" IS '企业类型';
COMMENT ON COLUMN "dwd"."enterprise"."industry_category" IS '所属行业';
COMMENT ON COLUMN "dwd"."enterprise"."industry_code" IS '行业代码';
COMMENT ON COLUMN "dwd"."enterprise"."business_scope" IS '经营范围';
COMMENT ON COLUMN "dwd"."enterprise"."registered_address" IS '注册地址';
COMMENT ON COLUMN "dwd"."enterprise"."headquarters_city" IS '总部城市';
COMMENT ON COLUMN "dwd"."enterprise"."headquarters_district" IS '总部所在区县';
COMMENT ON COLUMN "dwd"."enterprise"."headquarters_address" IS '总部详细地址';
COMMENT ON COLUMN "dwd"."enterprise"."headquarters_lng" IS '总部经度';
COMMENT ON COLUMN "dwd"."enterprise"."headquarters_lat" IS '总部纬度';
COMMENT ON COLUMN "dwd"."enterprise"."is_listed" IS '是否上市（0否/1是）';
COMMENT ON COLUMN "dwd"."enterprise"."listed_market" IS '上市板块';
COMMENT ON COLUMN "dwd"."enterprise"."listed_code" IS '股票代码';
COMMENT ON COLUMN "dwd"."enterprise"."is_foreign" IS '是否外资企业（0否/1是）';
COMMENT ON COLUMN "dwd"."enterprise"."is_high_tech" IS '是否高新技术企业（0否/1是）';
COMMENT ON COLUMN "dwd"."enterprise"."is_sme" IS '是否小微企业（0否/1是）';
COMMENT ON COLUMN "dwd"."enterprise"."is_little_giant" IS '是否专精特新（0否/1是）';
COMMENT ON COLUMN "dwd"."enterprise"."little_giant_level" IS '专精特新级别';
COMMENT ON COLUMN "dwd"."enterprise"."is_gazelle" IS '是否瞪羚企业（0否/1是）';
COMMENT ON COLUMN "dwd"."enterprise"."is_unicorn" IS '是否独角兽企业（0否/1是）';
COMMENT ON COLUMN "dwd"."enterprise"."revenue_latest" IS '最新年营收（万元）';
COMMENT ON COLUMN "dwd"."enterprise"."revenue_year" IS '营收对应年份';
COMMENT ON COLUMN "dwd"."enterprise"."revenue_growth_rate" IS '营收增长率（%）';
COMMENT ON COLUMN "dwd"."enterprise"."net_profit" IS '净利润（万元）';
COMMENT ON COLUMN "dwd"."enterprise"."profit_margin" IS '利润率（%）';
COMMENT ON COLUMN "dwd"."enterprise"."gross_margin" IS '毛利率（%）';
COMMENT ON COLUMN "dwd"."enterprise"."market_share" IS '市场份额（%）';
COMMENT ON COLUMN "dwd"."enterprise"."brand_score" IS '品牌声量评分';
COMMENT ON COLUMN "dwd"."enterprise"."customer_concentration" IS '客户集中度（%）';
COMMENT ON COLUMN "dwd"."enterprise"."patent_apply_count" IS '专利申请数量（累计）';
COMMENT ON COLUMN "dwd"."enterprise"."patent_grant_count" IS '专利授权数量（累计）';
COMMENT ON COLUMN "dwd"."enterprise"."patent_valid_count" IS '有效专利数量';
COMMENT ON COLUMN "dwd"."enterprise"."patent_invention_count" IS '发明专利数量';
COMMENT ON COLUMN "dwd"."enterprise"."patent_citation_count" IS '专利引用次数';
COMMENT ON COLUMN "dwd"."enterprise"."rd_staff_count" IS '研发人员数量';
COMMENT ON COLUMN "dwd"."enterprise"."rd_staff_ratio" IS '研发人员占比（%）';
COMMENT ON COLUMN "dwd"."enterprise"."rd_investment" IS '研发投入金额（万元）';
COMMENT ON COLUMN "dwd"."enterprise"."rd_investment_ratio" IS '研发投入占比（%）';
COMMENT ON COLUMN "dwd"."enterprise"."core_tech_coverage" IS '核心技术覆盖度评分';
COMMENT ON COLUMN "dwd"."enterprise"."tech_score" IS '技术力综合得分（0-100）';
COMMENT ON COLUMN "dwd"."enterprise"."business_score" IS '商业力综合得分（0-100）';
COMMENT ON COLUMN "dwd"."enterprise"."competitiveness_score" IS '综合竞争力得分（0-100）';
COMMENT ON COLUMN "dwd"."enterprise"."innovation_index" IS '创新活力指数';
COMMENT ON COLUMN "dwd"."enterprise"."introduction_value" IS '招引价值等级（A/B/C/D）';
COMMENT ON COLUMN "dwd"."enterprise"."cultivation_priority" IS '培育优先级（高/中/低）';
COMMENT ON COLUMN "dwd"."enterprise"."risk_level" IS '风险等级（低/中/高）';
COMMENT ON COLUMN "dwd"."enterprise"."data_source" IS '数据来源';
COMMENT ON COLUMN "dwd"."enterprise"."data_source_url" IS '原始数据URL';
COMMENT ON COLUMN "dwd"."enterprise"."data_collect_time" IS '数据采集时间';
COMMENT ON COLUMN "dwd"."enterprise"."data_update_time" IS '数据更新时间';
COMMENT ON COLUMN "dwd"."enterprise"."data_completeness" IS '数据完整度（0-1）';
COMMENT ON COLUMN "dwd"."enterprise"."data_confidence" IS '数据置信度（0-1）';
COMMENT ON COLUMN "dwd"."enterprise"."audit_status" IS '人工审核状态';
COMMENT ON COLUMN "dwd"."enterprise"."create_time" IS '记录创建时间';
COMMENT ON COLUMN "dwd"."enterprise"."update_time" IS '记录更新时间';
COMMENT ON TABLE "dwd"."enterprise" IS '企业基本信息表';

-- ----------------------------
-- Records of enterprise
-- ----------------------------

-- ----------------------------
-- Table structure for enterprise_business_tag
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."enterprise_business_tag";
CREATE TABLE "dwd"."enterprise_business_tag" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".enterprise_business_tag_id_seq'::regclass),
  "enterprise_id" int8 NOT NULL,
  "tag_type" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "tag_name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "tag_score" numeric(10,2) DEFAULT NULL::numeric,
  "create_time" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;
COMMENT ON COLUMN "dwd"."enterprise_business_tag"."id" IS '自增主键';
COMMENT ON COLUMN "dwd"."enterprise_business_tag"."enterprise_id" IS '企业ID';
COMMENT ON COLUMN "dwd"."enterprise_business_tag"."tag_type" IS '标签类型';
COMMENT ON COLUMN "dwd"."enterprise_business_tag"."tag_name" IS '标签名称';
COMMENT ON COLUMN "dwd"."enterprise_business_tag"."tag_score" IS '标签关联度评分';
COMMENT ON COLUMN "dwd"."enterprise_business_tag"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."enterprise_business_tag"."update_time" IS '更新时间';
COMMENT ON TABLE "dwd"."enterprise_business_tag" IS '企业业务标签表';

-- ----------------------------
-- Records of enterprise_business_tag
-- ----------------------------

-- ----------------------------
-- Table structure for enterprise_cooperation
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."enterprise_cooperation";
CREATE TABLE "dwd"."enterprise_cooperation" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".enterprise_cooperation_id_seq'::regclass),
  "enterprise_id" int8 NOT NULL,
  "partner_type" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "partner_id" int8,
  "partner_name" varchar(255) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "cooperation_type" varchar(50) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "project_count" int4 DEFAULT 0,
  "patent_count" int4 DEFAULT 0,
  "create_time" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;
COMMENT ON COLUMN "dwd"."enterprise_cooperation"."id" IS '自增主键';
COMMENT ON COLUMN "dwd"."enterprise_cooperation"."enterprise_id" IS '企业ID';
COMMENT ON COLUMN "dwd"."enterprise_cooperation"."partner_type" IS '合作方类型';
COMMENT ON COLUMN "dwd"."enterprise_cooperation"."partner_id" IS '合作方ID';
COMMENT ON COLUMN "dwd"."enterprise_cooperation"."partner_name" IS '合作方名称';
COMMENT ON COLUMN "dwd"."enterprise_cooperation"."cooperation_type" IS '合作类型';
COMMENT ON COLUMN "dwd"."enterprise_cooperation"."project_count" IS '合作项目数量';
COMMENT ON COLUMN "dwd"."enterprise_cooperation"."patent_count" IS '联合专利数量';
COMMENT ON COLUMN "dwd"."enterprise_cooperation"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."enterprise_cooperation"."update_time" IS '更新时间';
COMMENT ON TABLE "dwd"."enterprise_cooperation" IS '企业产学研合作表';

-- ----------------------------
-- Records of enterprise_cooperation
-- ----------------------------

-- ----------------------------
-- Table structure for enterprise_finance_history
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."enterprise_finance_history";
CREATE TABLE "dwd"."enterprise_finance_history" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".enterprise_finance_history_id_seq'::regclass),
  "enterprise_id" int8 NOT NULL,
  "data_year" int4 NOT NULL,
  "revenue" numeric(20,2) DEFAULT NULL::numeric,
  "revenue_growth_rate" numeric(10,4) DEFAULT NULL::numeric,
  "net_profit" numeric(20,2) DEFAULT NULL::numeric,
  "profit_margin" numeric(10,4) DEFAULT NULL::numeric,
  "gross_margin" numeric(10,4) DEFAULT NULL::numeric,
  "rd_investment" numeric(20,2) DEFAULT NULL::numeric,
  "rd_investment_ratio" numeric(10,4) DEFAULT NULL::numeric,
  "rd_staff_count" int4 DEFAULT 0,
  "create_time" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;
COMMENT ON COLUMN "dwd"."enterprise_finance_history"."id" IS '自增主键';
COMMENT ON COLUMN "dwd"."enterprise_finance_history"."enterprise_id" IS '企业ID';
COMMENT ON COLUMN "dwd"."enterprise_finance_history"."data_year" IS '数据年份';
COMMENT ON COLUMN "dwd"."enterprise_finance_history"."revenue" IS '营收(万元)';
COMMENT ON COLUMN "dwd"."enterprise_finance_history"."revenue_growth_rate" IS '营收增长率(%)';
COMMENT ON COLUMN "dwd"."enterprise_finance_history"."net_profit" IS '净利润(万元)';
COMMENT ON COLUMN "dwd"."enterprise_finance_history"."profit_margin" IS '利润率(%)';
COMMENT ON COLUMN "dwd"."enterprise_finance_history"."gross_margin" IS '毛利率(%)';
COMMENT ON COLUMN "dwd"."enterprise_finance_history"."rd_investment" IS '研发投入(万元)';
COMMENT ON COLUMN "dwd"."enterprise_finance_history"."rd_investment_ratio" IS '研发投入占比(%)';
COMMENT ON COLUMN "dwd"."enterprise_finance_history"."rd_staff_count" IS '研发人员数量';
COMMENT ON COLUMN "dwd"."enterprise_finance_history"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."enterprise_finance_history"."update_time" IS '更新时间';
COMMENT ON TABLE "dwd"."enterprise_finance_history" IS '企业财务历史表';

-- ----------------------------
-- Records of enterprise_finance_history
-- ----------------------------

-- ----------------------------
-- Table structure for enterprise_industry
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."enterprise_industry";
CREATE TABLE "dwd"."enterprise_industry" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".enterprise_industry_id_seq'::regclass),
  "enterprise_id" int8 NOT NULL,
  "industry_chain" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "industry_chain_node" varchar(100) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "industry_chain_role" varchar(50) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "participation_depth" numeric(10,2) DEFAULT NULL::numeric,
  "create_time" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;
COMMENT ON COLUMN "dwd"."enterprise_industry"."id" IS '自增主键';
COMMENT ON COLUMN "dwd"."enterprise_industry"."enterprise_id" IS '企业ID';
COMMENT ON COLUMN "dwd"."enterprise_industry"."industry_chain" IS '产业链名称';
COMMENT ON COLUMN "dwd"."enterprise_industry"."industry_chain_node" IS '产业链环节';
COMMENT ON COLUMN "dwd"."enterprise_industry"."industry_chain_role" IS '产业链角色';
COMMENT ON COLUMN "dwd"."enterprise_industry"."participation_depth" IS '参与深度评分';
COMMENT ON COLUMN "dwd"."enterprise_industry"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."enterprise_industry"."update_time" IS '更新时间';
COMMENT ON TABLE "dwd"."enterprise_industry" IS '企业产业链关联表';

-- ----------------------------
-- Records of enterprise_industry
-- ----------------------------

-- ----------------------------
-- Table structure for enterprise_parent_subsidiary
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."enterprise_parent_subsidiary";
CREATE TABLE "dwd"."enterprise_parent_subsidiary" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".enterprise_parent_subsidiary_id_seq'::regclass),
  "enterprise_id" int8 NOT NULL,
  "parent_enterprise_id" int8,
  "parent_enterprise_name" varchar(255) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "ownership_ratio" numeric(10,4) DEFAULT NULL::numeric,
  "subsidiary_count" int4 DEFAULT 0,
  "create_time" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;
COMMENT ON COLUMN "dwd"."enterprise_parent_subsidiary"."id" IS '自增主键';
COMMENT ON COLUMN "dwd"."enterprise_parent_subsidiary"."enterprise_id" IS '本企业ID';
COMMENT ON COLUMN "dwd"."enterprise_parent_subsidiary"."parent_enterprise_id" IS '母公司ID';
COMMENT ON COLUMN "dwd"."enterprise_parent_subsidiary"."parent_enterprise_name" IS '母公司名称';
COMMENT ON COLUMN "dwd"."enterprise_parent_subsidiary"."ownership_ratio" IS '控股比例(%)';
COMMENT ON COLUMN "dwd"."enterprise_parent_subsidiary"."subsidiary_count" IS '子公司数量';
COMMENT ON COLUMN "dwd"."enterprise_parent_subsidiary"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."enterprise_parent_subsidiary"."update_time" IS '更新时间';
COMMENT ON TABLE "dwd"."enterprise_parent_subsidiary" IS '企业股权关系表';

-- ----------------------------
-- Records of enterprise_parent_subsidiary
-- ----------------------------

-- ----------------------------
-- Table structure for enterprise_patent_history
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."enterprise_patent_history";
CREATE TABLE "dwd"."enterprise_patent_history" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".enterprise_patent_history_id_seq'::regclass),
  "enterprise_id" int8 NOT NULL,
  "data_year" int4 NOT NULL,
  "patent_apply_count" int4 DEFAULT 0,
  "patent_grant_count" int4 DEFAULT 0,
  "patent_valid_count" int4 DEFAULT 0,
  "patent_citation_count" int4 DEFAULT 0,
  "create_time" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;
COMMENT ON COLUMN "dwd"."enterprise_patent_history"."id" IS '自增主键';
COMMENT ON COLUMN "dwd"."enterprise_patent_history"."enterprise_id" IS '企业ID';
COMMENT ON COLUMN "dwd"."enterprise_patent_history"."data_year" IS '数据年份';
COMMENT ON COLUMN "dwd"."enterprise_patent_history"."patent_apply_count" IS '当年专利申请数';
COMMENT ON COLUMN "dwd"."enterprise_patent_history"."patent_grant_count" IS '当年专利授权数';
COMMENT ON COLUMN "dwd"."enterprise_patent_history"."patent_valid_count" IS '当年有效专利数';
COMMENT ON COLUMN "dwd"."enterprise_patent_history"."patent_citation_count" IS '当年专利引用次数';
COMMENT ON COLUMN "dwd"."enterprise_patent_history"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."enterprise_patent_history"."update_time" IS '更新时间';
COMMENT ON TABLE "dwd"."enterprise_patent_history" IS '企业专利历史表';

-- ----------------------------
-- Records of enterprise_patent_history
-- ----------------------------

-- ----------------------------
-- Table structure for enterprise_supply_chain
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."enterprise_supply_chain";
CREATE TABLE "dwd"."enterprise_supply_chain" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".enterprise_supply_chain_id_seq'::regclass),
  "enterprise_id" int8 NOT NULL,
  "related_enterprise_id" int8 NOT NULL,
  "relation_type" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "relation_strength" numeric(10,2) DEFAULT NULL::numeric,
  "is_core_supplier" int2 DEFAULT 0,
  "risk_level" varchar(20) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "create_time" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;
COMMENT ON COLUMN "dwd"."enterprise_supply_chain"."id" IS '自增主键';
COMMENT ON COLUMN "dwd"."enterprise_supply_chain"."enterprise_id" IS '本企业ID';
COMMENT ON COLUMN "dwd"."enterprise_supply_chain"."related_enterprise_id" IS '关联企业ID';
COMMENT ON COLUMN "dwd"."enterprise_supply_chain"."relation_type" IS '关系类型';
COMMENT ON COLUMN "dwd"."enterprise_supply_chain"."relation_strength" IS '关系强度评分';
COMMENT ON COLUMN "dwd"."enterprise_supply_chain"."is_core_supplier" IS '是否核心供应商';
COMMENT ON COLUMN "dwd"."enterprise_supply_chain"."risk_level" IS '断链风险等级';
COMMENT ON COLUMN "dwd"."enterprise_supply_chain"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."enterprise_supply_chain"."update_time" IS '更新时间';
COMMENT ON TABLE "dwd"."enterprise_supply_chain" IS '企业供应链关系表';

-- ----------------------------
-- Records of enterprise_supply_chain
-- ----------------------------

-- ----------------------------
-- Table structure for national_policy_distribution
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."national_policy_distribution";
CREATE TABLE "dwd"."national_policy_distribution" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".national_policy_distribution_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "stat_date" date NOT NULL,
  "stat_period" varchar(20) COLLATE "pg_catalog"."default",
  "province_code" varchar(20) COLLATE "pg_catalog"."default",
  "province_name" varchar(100) COLLATE "pg_catalog"."default",
  "policy_count" int4,
  "chain_ratio" numeric(10,4),
  "year_over_year_ratio" numeric(10,4),
  "industry_count" int4,
  "talent_count" int4,
  "enterprise_count" int4,
  "rank_nationwide" int4,
  "density_index" numeric(8,4),
  "detail_data" text COLLATE "pg_catalog"."default",
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."national_policy_distribution"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."national_policy_distribution"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."national_policy_distribution"."stat_date" IS '统计日期';
COMMENT ON COLUMN "dwd"."national_policy_distribution"."stat_period" IS '统计周期';
COMMENT ON COLUMN "dwd"."national_policy_distribution"."province_code" IS '省份行政区划代码';
COMMENT ON COLUMN "dwd"."national_policy_distribution"."province_name" IS '省份名称';
COMMENT ON COLUMN "dwd"."national_policy_distribution"."policy_count" IS '政策数量';
COMMENT ON COLUMN "dwd"."national_policy_distribution"."chain_ratio" IS '环比增长率';
COMMENT ON COLUMN "dwd"."national_policy_distribution"."year_over_year_ratio" IS '同比增长率';
COMMENT ON COLUMN "dwd"."national_policy_distribution"."industry_count" IS '产业政策数量';
COMMENT ON COLUMN "dwd"."national_policy_distribution"."talent_count" IS '人才政策数量';
COMMENT ON COLUMN "dwd"."national_policy_distribution"."enterprise_count" IS '企业扶持政策数量';
COMMENT ON COLUMN "dwd"."national_policy_distribution"."rank_nationwide" IS '全国排名';
COMMENT ON COLUMN "dwd"."national_policy_distribution"."density_index" IS '政策密度指数';
COMMENT ON COLUMN "dwd"."national_policy_distribution"."detail_data" IS '明细数据（JSON）';
COMMENT ON COLUMN "dwd"."national_policy_distribution"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."national_policy_distribution"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."national_policy_distribution"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."national_policy_distribution"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."national_policy_distribution"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."national_policy_distribution"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."national_policy_distribution" IS '全国政策分布指标表';

-- ----------------------------
-- Records of national_policy_distribution
-- ----------------------------

-- ----------------------------
-- Table structure for policy_analysis_report
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_analysis_report";
CREATE TABLE "dwd"."policy_analysis_report" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_analysis_report_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "report_no" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "report_name" varchar(300) COLLATE "pg_catalog"."default" NOT NULL,
  "report_type" varchar(50) COLLATE "pg_catalog"."default",
  "report_scope" varchar(200) COLLATE "pg_catalog"."default",
  "dimension_config" text COLLATE "pg_catalog"."default",
  "chart_data" text COLLATE "pg_catalog"."default",
  "report_content" text COLLATE "pg_catalog"."default",
  "report_template_id" varchar(64) COLLATE "pg_catalog"."default",
  "export_file_url" varchar(1000) COLLATE "pg_catalog"."default",
  "operator_id" int8,
  "audit_log" text COLLATE "pg_catalog"."default",
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_analysis_report"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_analysis_report"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_analysis_report"."report_no" IS '报告编号';
COMMENT ON COLUMN "dwd"."policy_analysis_report"."report_name" IS '报告名称';
COMMENT ON COLUMN "dwd"."policy_analysis_report"."report_type" IS '报告类型：TREND-趋势/CONTRAST-对比/ASSOCIATION-关联/COMPREHENSIVE-综合';
COMMENT ON COLUMN "dwd"."policy_analysis_report"."report_scope" IS '报告范围';
COMMENT ON COLUMN "dwd"."policy_analysis_report"."dimension_config" IS '维度配置（JSON）';
COMMENT ON COLUMN "dwd"."policy_analysis_report"."chart_data" IS '图表可视化数据（JSON）';
COMMENT ON COLUMN "dwd"."policy_analysis_report"."report_content" IS '报告内容 HTML/Markdown';
COMMENT ON COLUMN "dwd"."policy_analysis_report"."report_template_id" IS '报告模板ID';
COMMENT ON COLUMN "dwd"."policy_analysis_report"."export_file_url" IS '导出文件URL PDF/Excel';
COMMENT ON COLUMN "dwd"."policy_analysis_report"."operator_id" IS '操作人ID';
COMMENT ON COLUMN "dwd"."policy_analysis_report"."audit_log" IS '操作日志（JSON）';
COMMENT ON COLUMN "dwd"."policy_analysis_report"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_analysis_report"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_analysis_report"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_analysis_report"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_analysis_report"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_analysis_report"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."policy_analysis_report" IS '政策分析报告表';

-- ----------------------------
-- Records of policy_analysis_report
-- ----------------------------

-- ----------------------------
-- Table structure for policy_base_info
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_base_info";
CREATE TABLE "dwd"."policy_base_info" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_base_info_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "policy_id" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "title" varchar(500) COLLATE "pg_catalog"."default" NOT NULL,
  "issued_number" varchar(200) COLLATE "pg_catalog"."default",
  "publish_organization" varchar(300) COLLATE "pg_catalog"."default",
  "publish_date" date,
  "implementation_date" date,
  "expire_date" date,
  "status" int2,
  "publish_year" int4,
  "level" int2,
  "region" varchar(200) COLLATE "pg_catalog"."default",
  "abstract" text COLLATE "pg_catalog"."default",
  "keywords" varchar(1000) COLLATE "pg_catalog"."default",
  "content" text COLLATE "pg_catalog"."default",
  "url" varchar(1000) COLLATE "pg_catalog"."default",
  "pedigree" text COLLATE "pg_catalog"."default",
  "elements" text COLLATE "pg_catalog"."default",
  "keypoints" text COLLATE "pg_catalog"."default",
  "factors" text COLLATE "pg_catalog"."default",
  "source" varchar(200) COLLATE "pg_catalog"."default",
  "gis_location" varchar(100) COLLATE "pg_catalog"."default",
  "attachment" text COLLATE "pg_catalog"."default",
  "sci_tech_attribute" int2,
  "application_conditions" text COLLATE "pg_catalog"."default",
  "execution_cycle" varchar(200) COLLATE "pg_catalog"."default",
  "execution_entity" varchar(300) COLLATE "pg_catalog"."default",
  "related_entities" text COLLATE "pg_catalog"."default",
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default",
  "ext4" varchar(500) COLLATE "pg_catalog"."default",
  "ext5" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_base_info"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_base_info"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_base_info"."policy_id" IS '政策唯一标识（业务主键）';
COMMENT ON COLUMN "dwd"."policy_base_info"."title" IS '政策标题';
COMMENT ON COLUMN "dwd"."policy_base_info"."issued_number" IS '政策文号';
COMMENT ON COLUMN "dwd"."policy_base_info"."publish_organization" IS '发布机构';
COMMENT ON COLUMN "dwd"."policy_base_info"."publish_date" IS '发布日期';
COMMENT ON COLUMN "dwd"."policy_base_info"."implementation_date" IS '实施日期';
COMMENT ON COLUMN "dwd"."policy_base_info"."expire_date" IS '失效日期';
COMMENT ON COLUMN "dwd"."policy_base_info"."status" IS '政策状态：1-有效/2-失效/3-修订中/4-即将生效';
COMMENT ON COLUMN "dwd"."policy_base_info"."publish_year" IS '发布年份（冗余统计字段）';
COMMENT ON COLUMN "dwd"."policy_base_info"."level" IS '政策层级：1-国家/2-省级/3-市级/4-区级';
COMMENT ON COLUMN "dwd"."policy_base_info"."region" IS '政策地区（多地区逗号分隔）';
COMMENT ON COLUMN "dwd"."policy_base_info"."abstract" IS '政策摘要';
COMMENT ON COLUMN "dwd"."policy_base_info"."keywords" IS '关键词（逗号分隔）';
COMMENT ON COLUMN "dwd"."policy_base_info"."content" IS '政策正文全文';
COMMENT ON COLUMN "dwd"."policy_base_info"."url" IS '原文链接';
COMMENT ON COLUMN "dwd"."policy_base_info"."pedigree" IS '政策谱系/引用政策（JSON）';
COMMENT ON COLUMN "dwd"."policy_base_info"."elements" IS '政策主旨要素（JSON）';
COMMENT ON COLUMN "dwd"."policy_base_info"."keypoints" IS '政策要点（JSON）';
COMMENT ON COLUMN "dwd"."policy_base_info"."factors" IS '政策扶持要素（JSON）';
COMMENT ON COLUMN "dwd"."policy_base_info"."source" IS '数据来源';
COMMENT ON COLUMN "dwd"."policy_base_info"."gis_location" IS '发布地GIS坐标 格式lng,lat';
COMMENT ON COLUMN "dwd"."policy_base_info"."attachment" IS '附件信息（JSON）';
COMMENT ON COLUMN "dwd"."policy_base_info"."sci_tech_attribute" IS '科创属性：0-非科创/1-科创政策/2-强科创关联';
COMMENT ON COLUMN "dwd"."policy_base_info"."application_conditions" IS '申报条件';
COMMENT ON COLUMN "dwd"."policy_base_info"."execution_cycle" IS '执行周期';
COMMENT ON COLUMN "dwd"."policy_base_info"."execution_entity" IS '执行主体';
COMMENT ON COLUMN "dwd"."policy_base_info"."related_entities" IS '关联实体（JSON）';
COMMENT ON COLUMN "dwd"."policy_base_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_base_info"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_base_info"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_base_info"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_base_info"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_base_info"."ext3" IS '扩展字段3';
COMMENT ON COLUMN "dwd"."policy_base_info"."ext4" IS '扩展字段4';
COMMENT ON COLUMN "dwd"."policy_base_info"."ext5" IS '扩展字段5';
COMMENT ON TABLE "dwd"."policy_base_info" IS '政策基础信息表';

-- ----------------------------
-- Records of policy_base_info
-- ----------------------------

-- ----------------------------
-- Table structure for policy_effect_eval
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_effect_eval";
CREATE TABLE "dwd"."policy_effect_eval" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_effect_eval_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "policy_id" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "eval_batch_no" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "effect_index" numeric(8,4),
  "execution_effect_score" numeric(8,4),
  "social_economic_score" numeric(8,4),
  "environment_impact_score" numeric(8,4),
  "innovation_promotion_score" numeric(8,4),
  "industry_impact_score" numeric(8,4),
  "dimension_results" text COLLATE "pg_catalog"."default",
  "improvement_suggestions" text COLLATE "pg_catalog"."default",
  "performance_report" text COLLATE "pg_catalog"."default",
  "eval_stage" varchar(50) COLLATE "pg_catalog"."default",
  "eval_model_version" varchar(50) COLLATE "pg_catalog"."default",
  "exec_status" int2,
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_effect_eval"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_effect_eval"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_effect_eval"."policy_id" IS '政策唯一标识';
COMMENT ON COLUMN "dwd"."policy_effect_eval"."eval_batch_no" IS '评估批次号';
COMMENT ON COLUMN "dwd"."policy_effect_eval"."effect_index" IS '政策效果评估指数 综合得分';
COMMENT ON COLUMN "dwd"."policy_effect_eval"."execution_effect_score" IS '执行效果得分';
COMMENT ON COLUMN "dwd"."policy_effect_eval"."social_economic_score" IS '社会经济效应得分';
COMMENT ON COLUMN "dwd"."policy_effect_eval"."environment_impact_score" IS '环境影响得分';
COMMENT ON COLUMN "dwd"."policy_effect_eval"."innovation_promotion_score" IS '创新促进得分';
COMMENT ON COLUMN "dwd"."policy_effect_eval"."industry_impact_score" IS '产业影响得分';
COMMENT ON COLUMN "dwd"."policy_effect_eval"."dimension_results" IS '分维度评估结果详情（JSON）';
COMMENT ON COLUMN "dwd"."policy_effect_eval"."improvement_suggestions" IS '政策改进建议（JSON数组）';
COMMENT ON COLUMN "dwd"."policy_effect_eval"."performance_report" IS '绩效优化报告';
COMMENT ON COLUMN "dwd"."policy_effect_eval"."eval_stage" IS '评估阶段：PRE-事前/MID-事中/POST-事后';
COMMENT ON COLUMN "dwd"."policy_effect_eval"."eval_model_version" IS '评估模型版本号';
COMMENT ON COLUMN "dwd"."policy_effect_eval"."exec_status" IS '执行状态：1-成功/2-部分成功/3-失败';
COMMENT ON COLUMN "dwd"."policy_effect_eval"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_effect_eval"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_effect_eval"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_effect_eval"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_effect_eval"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_effect_eval"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."policy_effect_eval" IS '政策效果评估结果表';

-- ----------------------------
-- Records of policy_effect_eval
-- ----------------------------

-- ----------------------------
-- Table structure for policy_entity
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_entity";
CREATE TABLE "dwd"."policy_entity" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_entity_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "entity_code" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "entity_name" varchar(300) COLLATE "pg_catalog"."default" NOT NULL,
  "entity_type_id" int8 NOT NULL,
  "entity_level" varchar(50) COLLATE "pg_catalog"."default",
  "entity_attribute" text COLLATE "pg_catalog"."default",
  "publish_region" varchar(200) COLLATE "pg_catalog"."default",
  "establish_date" date,
  "profile" text COLLATE "pg_catalog"."default",
  "data_source" varchar(200) COLLATE "pg_catalog"."default",
  "source_id" varchar(100) COLLATE "pg_catalog"."default",
  "is_verified" int2,
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_entity"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_entity"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_entity"."entity_code" IS '实体编码 业务唯一标识';
COMMENT ON COLUMN "dwd"."policy_entity"."entity_name" IS '实体名称';
COMMENT ON COLUMN "dwd"."policy_entity"."entity_type_id" IS '实体类型ID 关联policy_entity_type.id';
COMMENT ON COLUMN "dwd"."policy_entity"."entity_level" IS '实体级别';
COMMENT ON COLUMN "dwd"."policy_entity"."entity_attribute" IS '实体扩展属性（JSON）';
COMMENT ON COLUMN "dwd"."policy_entity"."publish_region" IS '所属地区';
COMMENT ON COLUMN "dwd"."policy_entity"."establish_date" IS '成立/发布日期';
COMMENT ON COLUMN "dwd"."policy_entity"."profile" IS '实体简介';
COMMENT ON COLUMN "dwd"."policy_entity"."data_source" IS '数据来源';
COMMENT ON COLUMN "dwd"."policy_entity"."source_id" IS '来源系统ID';
COMMENT ON COLUMN "dwd"."policy_entity"."is_verified" IS '是否已核验：0-未核验/1-已核验';
COMMENT ON COLUMN "dwd"."policy_entity"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_entity"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_entity"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_entity"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_entity"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_entity"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."policy_entity" IS '政策实体信息表';

-- ----------------------------
-- Records of policy_entity
-- ----------------------------

-- ----------------------------
-- Table structure for policy_entity_relation
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_entity_relation";
CREATE TABLE "dwd"."policy_entity_relation" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_entity_relation_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "policy_id" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "entity_id" int8 NOT NULL,
  "relation_type" varchar(50) COLLATE "pg_catalog"."default",
  "relation_weight" numeric(5,4),
  "relation_desc" varchar(500) COLLATE "pg_catalog"."default",
  "extract_rule" varchar(200) COLLATE "pg_catalog"."default",
  "confidence" numeric(5,4),
  "extract_source" varchar(200) COLLATE "pg_catalog"."default",
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_entity_relation"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_entity_relation"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_entity_relation"."policy_id" IS '政策唯一标识 关联policy_base_info.policy_id';
COMMENT ON COLUMN "dwd"."policy_entity_relation"."entity_id" IS '实体ID 关联policy_entity.id';
COMMENT ON COLUMN "dwd"."policy_entity_relation"."relation_type" IS '关系类型：SUPPORT-扶持/Applicable-适用/REGULATE-监管/RELATED-关联';
COMMENT ON COLUMN "dwd"."policy_entity_relation"."relation_weight" IS '关系权重 0-1';
COMMENT ON COLUMN "dwd"."policy_entity_relation"."relation_desc" IS '关系描述';
COMMENT ON COLUMN "dwd"."policy_entity_relation"."extract_rule" IS '抽取规则标识';
COMMENT ON COLUMN "dwd"."policy_entity_relation"."confidence" IS '关系置信度 0-1';
COMMENT ON COLUMN "dwd"."policy_entity_relation"."extract_source" IS '关系抽取来源';
COMMENT ON COLUMN "dwd"."policy_entity_relation"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_entity_relation"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_entity_relation"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_entity_relation"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_entity_relation"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_entity_relation"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."policy_entity_relation" IS '政策实体关系表';

-- ----------------------------
-- Records of policy_entity_relation
-- ----------------------------

-- ----------------------------
-- Table structure for policy_entity_type
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_entity_type";
CREATE TABLE "dwd"."policy_entity_type" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_entity_type_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "type_code" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "type_name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "type_desc" varchar(500) COLLATE "pg_catalog"."default",
  "parent_id" int8,
  "sort_order" int4,
  "is_enabled" int2,
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_entity_type"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_entity_type"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_entity_type"."type_code" IS '类型编码：INDUSTRY/TECH/ENTERPRISE/TALENT/INSTITUTION/SERVICE';
COMMENT ON COLUMN "dwd"."policy_entity_type"."type_name" IS '类型名称';
COMMENT ON COLUMN "dwd"."policy_entity_type"."type_desc" IS '类型描述';
COMMENT ON COLUMN "dwd"."policy_entity_type"."parent_id" IS '父类型ID 支持层级分类';
COMMENT ON COLUMN "dwd"."policy_entity_type"."sort_order" IS '排序序号';
COMMENT ON COLUMN "dwd"."policy_entity_type"."is_enabled" IS '是否启用：0-禁用/1-启用';
COMMENT ON COLUMN "dwd"."policy_entity_type"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_entity_type"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_entity_type"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_entity_type"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_entity_type"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_entity_type"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."policy_entity_type" IS '政策实体类型字典表';

-- ----------------------------
-- Records of policy_entity_type
-- ----------------------------

-- ----------------------------
-- Table structure for policy_favorite
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_favorite";
CREATE TABLE "dwd"."policy_favorite" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_favorite_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "user_id" int8 NOT NULL,
  "policy_id" varchar(64) COLLATE "pg_catalog"."default",
  "favorite_type" varchar(50) COLLATE "pg_catalog"."default",
  "folder_name" varchar(200) COLLATE "pg_catalog"."default",
  "remark" varchar(500) COLLATE "pg_catalog"."default",
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_favorite"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_favorite"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_favorite"."user_id" IS '用户ID';
COMMENT ON COLUMN "dwd"."policy_favorite"."policy_id" IS '政策唯一标识';
COMMENT ON COLUMN "dwd"."policy_favorite"."favorite_type" IS '收藏类型：POLICY-政策/SEARCH-检索条件';
COMMENT ON COLUMN "dwd"."policy_favorite"."folder_name" IS '收藏夹名称';
COMMENT ON COLUMN "dwd"."policy_favorite"."remark" IS '收藏备注';
COMMENT ON COLUMN "dwd"."policy_favorite"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_favorite"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_favorite"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_favorite"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_favorite"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_favorite"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."policy_favorite" IS '政策收藏表';

-- ----------------------------
-- Records of policy_favorite
-- ----------------------------

-- ----------------------------
-- Table structure for policy_focus_result
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_focus_result";
CREATE TABLE "dwd"."policy_focus_result" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_focus_result_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "policy_id" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "analysis_batch_no" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "focus_items" text COLLATE "pg_catalog"."default",
  "bottleneck_items" text COLLATE "pg_catalog"."default",
  "optimization_suggestions" text COLLATE "pg_catalog"."default",
  "dimension_scores" text COLLATE "pg_catalog"."default",
  "threshold_config" text COLLATE "pg_catalog"."default",
  "analysis_model_version" varchar(50) COLLATE "pg_catalog"."default",
  "exec_status" int2,
  "exec_time" int4,
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_focus_result"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_focus_result"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_focus_result"."policy_id" IS '政策唯一标识';
COMMENT ON COLUMN "dwd"."policy_focus_result"."analysis_batch_no" IS '分析批次号';
COMMENT ON COLUMN "dwd"."policy_focus_result"."focus_items" IS '政策焦点列表（JSON数组）';
COMMENT ON COLUMN "dwd"."policy_focus_result"."bottleneck_items" IS '政策堵点清单（JSON数组）';
COMMENT ON COLUMN "dwd"."policy_focus_result"."optimization_suggestions" IS '政策优化建议（JSON数组）';
COMMENT ON COLUMN "dwd"."policy_focus_result"."dimension_scores" IS '各维度评分（JSON）';
COMMENT ON COLUMN "dwd"."policy_focus_result"."threshold_config" IS '评估阈值配置（JSON）';
COMMENT ON COLUMN "dwd"."policy_focus_result"."analysis_model_version" IS '分析模型版本号';
COMMENT ON COLUMN "dwd"."policy_focus_result"."exec_status" IS '执行状态：1-成功/2-部分成功/3-失败';
COMMENT ON COLUMN "dwd"."policy_focus_result"."exec_time" IS '执行耗时(毫秒)';
COMMENT ON COLUMN "dwd"."policy_focus_result"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_focus_result"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_focus_result"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_focus_result"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_focus_result"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_focus_result"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."policy_focus_result" IS '政策焦点识别结果表';

-- ----------------------------
-- Records of policy_focus_result
-- ----------------------------

-- ----------------------------
-- Table structure for policy_intensity_eval
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_intensity_eval";
CREATE TABLE "dwd"."policy_intensity_eval" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_intensity_eval_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "policy_id" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "eval_batch_no" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "intensity_index" numeric(8,4),
  "effect_score" numeric(8,4),
  "coverage_score" numeric(8,4),
  "cost_score" numeric(8,4),
  "intensity_level" varchar(20) COLLATE "pg_catalog"."default",
  "rank_nationwide" int4,
  "rank_province" int4,
  "dimension_report" text COLLATE "pg_catalog"."default",
  "trend_analysis" text COLLATE "pg_catalog"."default",
  "prediction_result" text COLLATE "pg_catalog"."default",
  "eval_model_version" varchar(50) COLLATE "pg_catalog"."default",
  "threshold_config" text COLLATE "pg_catalog"."default",
  "exec_status" int2,
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_intensity_eval"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_intensity_eval"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_intensity_eval"."policy_id" IS '政策唯一标识';
COMMENT ON COLUMN "dwd"."policy_intensity_eval"."eval_batch_no" IS '评估批次号';
COMMENT ON COLUMN "dwd"."policy_intensity_eval"."intensity_index" IS '政策力度指数 综合得分';
COMMENT ON COLUMN "dwd"."policy_intensity_eval"."effect_score" IS '效果维度得分';
COMMENT ON COLUMN "dwd"."policy_intensity_eval"."coverage_score" IS '覆盖维度得分';
COMMENT ON COLUMN "dwd"."policy_intensity_eval"."cost_score" IS '成本维度得分';
COMMENT ON COLUMN "dwd"."policy_intensity_eval"."intensity_level" IS '力度分级：HIGH-高/MEDIUM-中/LOW-低';
COMMENT ON COLUMN "dwd"."policy_intensity_eval"."rank_nationwide" IS '全国力度排名';
COMMENT ON COLUMN "dwd"."policy_intensity_eval"."rank_province" IS '省内力度排名';
COMMENT ON COLUMN "dwd"."policy_intensity_eval"."dimension_report" IS '力度维度分析报告（JSON/长文本）';
COMMENT ON COLUMN "dwd"."policy_intensity_eval"."trend_analysis" IS '趋势变化分析（JSON）';
COMMENT ON COLUMN "dwd"."policy_intensity_eval"."prediction_result" IS '预测分析结果（JSON）';
COMMENT ON COLUMN "dwd"."policy_intensity_eval"."eval_model_version" IS '评估模型版本号';
COMMENT ON COLUMN "dwd"."policy_intensity_eval"."threshold_config" IS '阈值配置（JSON）';
COMMENT ON COLUMN "dwd"."policy_intensity_eval"."exec_status" IS '执行状态：1-成功/2-部分成功/3-失败';
COMMENT ON COLUMN "dwd"."policy_intensity_eval"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_intensity_eval"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_intensity_eval"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_intensity_eval"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_intensity_eval"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_intensity_eval"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."policy_intensity_eval" IS '政策力度评估结果表';

-- ----------------------------
-- Records of policy_intensity_eval
-- ----------------------------

-- ----------------------------
-- Table structure for policy_interpretation_report
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_interpretation_report";
CREATE TABLE "dwd"."policy_interpretation_report" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_interpretation_report_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "report_no" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "parent_report_id" int8,
  "report_name" varchar(300) COLLATE "pg_catalog"."default" NOT NULL,
  "hot_issues" text COLLATE "pg_catalog"."default",
  "theme_interpretation" text COLLATE "pg_catalog"."default",
  "multimedia_content" text COLLATE "pg_catalog"."default",
  "smart_summary" text COLLATE "pg_catalog"."default",
  "highlight_suggestions" text COLLATE "pg_catalog"."default",
  "target_audience" varchar(100) COLLATE "pg_catalog"."default",
  "report_content" text COLLATE "pg_catalog"."default",
  "export_file_url" varchar(1000) COLLATE "pg_catalog"."default",
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_interpretation_report"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_interpretation_report"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_interpretation_report"."report_no" IS '报告编号';
COMMENT ON COLUMN "dwd"."policy_interpretation_report"."parent_report_id" IS '关联分析报告ID';
COMMENT ON COLUMN "dwd"."policy_interpretation_report"."report_name" IS '报告名称';
COMMENT ON COLUMN "dwd"."policy_interpretation_report"."hot_issues" IS '热点问题看板数据（JSON数组）';
COMMENT ON COLUMN "dwd"."policy_interpretation_report"."theme_interpretation" IS '分主题分指标互动解读（JSON）';
COMMENT ON COLUMN "dwd"."policy_interpretation_report"."multimedia_content" IS '多媒体辅助内容（JSON）';
COMMENT ON COLUMN "dwd"."policy_interpretation_report"."smart_summary" IS '智能摘要与结论 NLP生成';
COMMENT ON COLUMN "dwd"."policy_interpretation_report"."highlight_suggestions" IS '高亮关键点及应用建议（JSON）';
COMMENT ON COLUMN "dwd"."policy_interpretation_report"."target_audience" IS '目标受众：LEADER-领导/PROFESSIONAL-专业用户/PUBLIC-公众';
COMMENT ON COLUMN "dwd"."policy_interpretation_report"."report_content" IS '完整报告内容';
COMMENT ON COLUMN "dwd"."policy_interpretation_report"."export_file_url" IS '导出文件URL';
COMMENT ON COLUMN "dwd"."policy_interpretation_report"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_interpretation_report"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_interpretation_report"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_interpretation_report"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_interpretation_report"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_interpretation_report"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."policy_interpretation_report" IS '结果解读报告表';

-- ----------------------------
-- Records of policy_interpretation_report
-- ----------------------------

-- ----------------------------
-- Table structure for policy_latest_news
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_latest_news";
CREATE TABLE "dwd"."policy_latest_news" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_latest_news_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "policy_id" varchar(64) COLLATE "pg_catalog"."default",
  "news_title" varchar(500) COLLATE "pg_catalog"."default" NOT NULL,
  "news_content" text COLLATE "pg_catalog"."default",
  "news_type" varchar(50) COLLATE "pg_catalog"."default",
  "region" varchar(200) COLLATE "pg_catalog"."default",
  "is_shenzhen" int2,
  "source_url" varchar(1000) COLLATE "pg_catalog"."default",
  "source_platform" varchar(200) COLLATE "pg_catalog"."default",
  "publish_time" timestamp(6),
  "news_date" date,
  "view_count" int4 DEFAULT 0,
  "is_hot" int2,
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_latest_news"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_latest_news"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_latest_news"."policy_id" IS '关联政策唯一标识';
COMMENT ON COLUMN "dwd"."policy_latest_news"."news_title" IS '动态标题';
COMMENT ON COLUMN "dwd"."policy_latest_news"."news_content" IS '动态内容摘要';
COMMENT ON COLUMN "dwd"."policy_latest_news"."news_type" IS '动态类型：POLICY_RELEASE-政策发布/INTERPRETATION-政策解读/IMPLEMENTATION-执行动态';
COMMENT ON COLUMN "dwd"."policy_latest_news"."region" IS '所属地区';
COMMENT ON COLUMN "dwd"."policy_latest_news"."is_shenzhen" IS '是否深圳政策：0-否/1-是';
COMMENT ON COLUMN "dwd"."policy_latest_news"."source_url" IS '源地址链接';
COMMENT ON COLUMN "dwd"."policy_latest_news"."source_platform" IS '来源平台';
COMMENT ON COLUMN "dwd"."policy_latest_news"."publish_time" IS '发布时间';
COMMENT ON COLUMN "dwd"."policy_latest_news"."news_date" IS '动态日期 时间轴展示';
COMMENT ON COLUMN "dwd"."policy_latest_news"."view_count" IS '浏览量';
COMMENT ON COLUMN "dwd"."policy_latest_news"."is_hot" IS '是否热点：0-否/1-是';
COMMENT ON COLUMN "dwd"."policy_latest_news"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_latest_news"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_latest_news"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_latest_news"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_latest_news"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_latest_news"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."policy_latest_news" IS '最新政策动态表';

-- ----------------------------
-- Records of policy_latest_news
-- ----------------------------

-- ----------------------------
-- Table structure for policy_layout_recommend
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_layout_recommend";
CREATE TABLE "dwd"."policy_layout_recommend" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_layout_recommend_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "recommend_batch_no" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "target_region" varchar(200) COLLATE "pg_catalog"."default",
  "target_industry" varchar(200) COLLATE "pg_catalog"."default",
  "opportunity_result_id" int8,
  "weakness_result_id" int8,
  "layout_suggestions" text COLLATE "pg_catalog"."default",
  "effect_prediction" text COLLATE "pg_catalog"."default",
  "optimization_strategies" text COLLATE "pg_catalog"."default",
  "expert_knowledge_refs" text COLLATE "pg_catalog"."default",
  "priority_ranking" text COLLATE "pg_catalog"."default",
  "implementation_path" text COLLATE "pg_catalog"."default",
  "risk_analysis" text COLLATE "pg_catalog"."default",
  "recommend_model_version" varchar(50) COLLATE "pg_catalog"."default",
  "exec_status" int2,
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_layout_recommend"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_layout_recommend"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_layout_recommend"."recommend_batch_no" IS '推荐批次号';
COMMENT ON COLUMN "dwd"."policy_layout_recommend"."target_region" IS '目标区域';
COMMENT ON COLUMN "dwd"."policy_layout_recommend"."target_industry" IS '目标产业';
COMMENT ON COLUMN "dwd"."policy_layout_recommend"."opportunity_result_id" IS '关联机遇识别结果ID';
COMMENT ON COLUMN "dwd"."policy_layout_recommend"."weakness_result_id" IS '关联短板识别结果ID';
COMMENT ON COLUMN "dwd"."policy_layout_recommend"."layout_suggestions" IS '政策布局建议（JSON数组）';
COMMENT ON COLUMN "dwd"."policy_layout_recommend"."effect_prediction" IS '执行效果预测（JSON）';
COMMENT ON COLUMN "dwd"."policy_layout_recommend"."optimization_strategies" IS '优化策略建议（JSON）';
COMMENT ON COLUMN "dwd"."policy_layout_recommend"."expert_knowledge_refs" IS '关联专家知识库引用（JSON）';
COMMENT ON COLUMN "dwd"."policy_layout_recommend"."priority_ranking" IS '优先级排序结果（JSON）';
COMMENT ON COLUMN "dwd"."policy_layout_recommend"."implementation_path" IS '实施路径图（JSON）';
COMMENT ON COLUMN "dwd"."policy_layout_recommend"."risk_analysis" IS '风险分析（JSON）';
COMMENT ON COLUMN "dwd"."policy_layout_recommend"."recommend_model_version" IS '推荐模型版本号';
COMMENT ON COLUMN "dwd"."policy_layout_recommend"."exec_status" IS '执行状态：1-成功/2-部分成功/3-失败';
COMMENT ON COLUMN "dwd"."policy_layout_recommend"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_layout_recommend"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_layout_recommend"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_layout_recommend"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_layout_recommend"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_layout_recommend"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."policy_layout_recommend" IS '政策布局推荐结果表';

-- ----------------------------
-- Records of policy_layout_recommend
-- ----------------------------

-- ----------------------------
-- Table structure for policy_level_indicator
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_level_indicator";
CREATE TABLE "dwd"."policy_level_indicator" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_level_indicator_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "stat_date" date NOT NULL,
  "stat_period" varchar(20) COLLATE "pg_catalog"."default",
  "policy_level" int2,
  "policy_count" int4,
  "policy_count_chain_ratio" numeric(10,4),
  "policy_count_year_over_year" numeric(10,4),
  "industry_policy_count" int4,
  "talent_policy_count" int4,
  "enterprise_policy_count" int4,
  "detail_data" text COLLATE "pg_catalog"."default",
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_level_indicator"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_level_indicator"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_level_indicator"."stat_date" IS '统计日期';
COMMENT ON COLUMN "dwd"."policy_level_indicator"."stat_period" IS '统计周期：YEAR/MONTH/QUARTER';
COMMENT ON COLUMN "dwd"."policy_level_indicator"."policy_level" IS '政策层级：1-国家/2-省级/3-市级/4-区级';
COMMENT ON COLUMN "dwd"."policy_level_indicator"."policy_count" IS '政策数量';
COMMENT ON COLUMN "dwd"."policy_level_indicator"."policy_count_chain_ratio" IS '环比增长率';
COMMENT ON COLUMN "dwd"."policy_level_indicator"."policy_count_year_over_year" IS '同比增长率';
COMMENT ON COLUMN "dwd"."policy_level_indicator"."industry_policy_count" IS '产业政策数量';
COMMENT ON COLUMN "dwd"."policy_level_indicator"."talent_policy_count" IS '人才政策数量';
COMMENT ON COLUMN "dwd"."policy_level_indicator"."enterprise_policy_count" IS '企业扶持政策数量';
COMMENT ON COLUMN "dwd"."policy_level_indicator"."detail_data" IS '明细数据（JSON）';
COMMENT ON COLUMN "dwd"."policy_level_indicator"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_level_indicator"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_level_indicator"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_level_indicator"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_level_indicator"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_level_indicator"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."policy_level_indicator" IS '政策级别指标统计表';

-- ----------------------------
-- Records of policy_level_indicator
-- ----------------------------

-- ----------------------------
-- Table structure for policy_opportunity_result
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_opportunity_result";
CREATE TABLE "dwd"."policy_opportunity_result" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_opportunity_result_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "policy_id" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "analysis_batch_no" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "opportunity_items" text COLLATE "pg_catalog"."default",
  "attention_score" numeric(8,4),
  "influence_score" numeric(8,4),
  "stability_score" numeric(8,4),
  "opportunity_level" varchar(20) COLLATE "pg_catalog"."default",
  "trend_report" text COLLATE "pg_catalog"."default",
  "strategy_suggestions" text COLLATE "pg_catalog"."default",
  "visualization_data" text COLLATE "pg_catalog"."default",
  "analysis_model_version" varchar(50) COLLATE "pg_catalog"."default",
  "exec_status" int2,
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_opportunity_result"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_opportunity_result"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_opportunity_result"."policy_id" IS '政策唯一标识';
COMMENT ON COLUMN "dwd"."policy_opportunity_result"."analysis_batch_no" IS '分析批次号';
COMMENT ON COLUMN "dwd"."policy_opportunity_result"."opportunity_items" IS '政策机遇清单（JSON数组）';
COMMENT ON COLUMN "dwd"."policy_opportunity_result"."attention_score" IS '关注度得分';
COMMENT ON COLUMN "dwd"."policy_opportunity_result"."influence_score" IS '影响力得分';
COMMENT ON COLUMN "dwd"."policy_opportunity_result"."stability_score" IS '稳定性得分';
COMMENT ON COLUMN "dwd"."policy_opportunity_result"."opportunity_level" IS '机遇级别：HIGH-高/MEDIUM-中/LOW-低';
COMMENT ON COLUMN "dwd"."policy_opportunity_result"."trend_report" IS '机遇趋势分析报告（JSON/长文本）';
COMMENT ON COLUMN "dwd"."policy_opportunity_result"."strategy_suggestions" IS '策略建议（JSON数组）';
COMMENT ON COLUMN "dwd"."policy_opportunity_result"."visualization_data" IS '可视化数据（JSON）';
COMMENT ON COLUMN "dwd"."policy_opportunity_result"."analysis_model_version" IS '分析模型版本号';
COMMENT ON COLUMN "dwd"."policy_opportunity_result"."exec_status" IS '执行状态：1-成功/2-部分成功/3-失败';
COMMENT ON COLUMN "dwd"."policy_opportunity_result"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_opportunity_result"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_opportunity_result"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_opportunity_result"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_opportunity_result"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_opportunity_result"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."policy_opportunity_result" IS '政策机遇识别结果表';

-- ----------------------------
-- Records of policy_opportunity_result
-- ----------------------------

-- ----------------------------
-- Table structure for policy_prediction_indicator
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_prediction_indicator";
CREATE TABLE "dwd"."policy_prediction_indicator" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_prediction_indicator_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "simulation_id" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "indicator_name" varchar(200) COLLATE "pg_catalog"."default" NOT NULL,
  "indicator_category" varchar(50) COLLATE "pg_catalog"."default",
  "indicator_unit" varchar(50) COLLATE "pg_catalog"."default",
  "base_value" numeric(18,4),
  "predicted_value" numeric(18,4),
  "predicted_upper" numeric(18,4),
  "predicted_lower" numeric(18,4),
  "change_rate" numeric(10,4),
  "prediction_period" varchar(50) COLLATE "pg_catalog"."default",
  "prediction_model" varchar(100) COLLATE "pg_catalog"."default",
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_prediction_indicator"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_prediction_indicator"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_prediction_indicator"."simulation_id" IS '关联推演任务ID';
COMMENT ON COLUMN "dwd"."policy_prediction_indicator"."indicator_name" IS '指标名称';
COMMENT ON COLUMN "dwd"."policy_prediction_indicator"."indicator_category" IS '指标类别：ECONOMIC-经济/SOCIAL-社会/ENVIRONMENT-环境/INNOVATION-创新';
COMMENT ON COLUMN "dwd"."policy_prediction_indicator"."indicator_unit" IS '指标单位';
COMMENT ON COLUMN "dwd"."policy_prediction_indicator"."base_value" IS '基准值 政策实施前';
COMMENT ON COLUMN "dwd"."policy_prediction_indicator"."predicted_value" IS '预测值';
COMMENT ON COLUMN "dwd"."policy_prediction_indicator"."predicted_upper" IS '预测上限值';
COMMENT ON COLUMN "dwd"."policy_prediction_indicator"."predicted_lower" IS '预测下限值';
COMMENT ON COLUMN "dwd"."policy_prediction_indicator"."change_rate" IS '变化率(%)';
COMMENT ON COLUMN "dwd"."policy_prediction_indicator"."prediction_period" IS '预测周期';
COMMENT ON COLUMN "dwd"."policy_prediction_indicator"."prediction_model" IS '使用的预测模型';
COMMENT ON COLUMN "dwd"."policy_prediction_indicator"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_prediction_indicator"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_prediction_indicator"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_prediction_indicator"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_prediction_indicator"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_prediction_indicator"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."policy_prediction_indicator" IS '预测指标结果表';

-- ----------------------------
-- Records of policy_prediction_indicator
-- ----------------------------

-- ----------------------------
-- Table structure for policy_public_opinion
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_public_opinion";
CREATE TABLE "dwd"."policy_public_opinion" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_public_opinion_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "policy_id" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "eval_period" varchar(20) COLLATE "pg_catalog"."default",
  "audience_type" varchar(50) COLLATE "pg_catalog"."default",
  "feedback_channel" varchar(50) COLLATE "pg_catalog"."default",
  "feedback_count" int4,
  "satisfaction_score" numeric(5,2),
  "implementation_effect_score" numeric(5,2),
  "social_impact_score" numeric(5,2),
  "region_contrast_data" text COLLATE "pg_catalog"."default",
  "feedback_summary" text COLLATE "pg_catalog"."default",
  "effect_report_url" varchar(1000) COLLATE "pg_catalog"."default",
  "is_match_recommended" int2,
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_public_opinion"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_public_opinion"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_public_opinion"."policy_id" IS '政策唯一标识';
COMMENT ON COLUMN "dwd"."policy_public_opinion"."eval_period" IS '评估周期 如2024-Q1';
COMMENT ON COLUMN "dwd"."policy_public_opinion"."audience_type" IS '受众类型：GOVERNMENT-施政者/ENTERPRISE-企业/PERSONAL-个人';
COMMENT ON COLUMN "dwd"."policy_public_opinion"."feedback_channel" IS '反馈渠道：QUESTIONNAIRE-问卷/ONLINE_EVAL-在线评价/PUBLIC_OPINION-舆情采集';
COMMENT ON COLUMN "dwd"."policy_public_opinion"."feedback_count" IS '反馈数量';
COMMENT ON COLUMN "dwd"."policy_public_opinion"."satisfaction_score" IS '满意度得分(0-100)';
COMMENT ON COLUMN "dwd"."policy_public_opinion"."implementation_effect_score" IS '实施效果得分';
COMMENT ON COLUMN "dwd"."policy_public_opinion"."social_impact_score" IS '社会影响得分';
COMMENT ON COLUMN "dwd"."policy_public_opinion"."region_contrast_data" IS '区域对比数据（JSON）';
COMMENT ON COLUMN "dwd"."policy_public_opinion"."feedback_summary" IS '反馈汇总分析';
COMMENT ON COLUMN "dwd"."policy_public_opinion"."effect_report_url" IS '效果评估报告URL';
COMMENT ON COLUMN "dwd"."policy_public_opinion"."is_match_recommended" IS '是否用于政策匹配推荐：0-否/1-是';
COMMENT ON COLUMN "dwd"."policy_public_opinion"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_public_opinion"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_public_opinion"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_public_opinion"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_public_opinion"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_public_opinion"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."policy_public_opinion" IS '政策舆情评估表';

-- ----------------------------
-- Records of policy_public_opinion
-- ----------------------------

-- ----------------------------
-- Table structure for policy_recommendation_report
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_recommendation_report";
CREATE TABLE "dwd"."policy_recommendation_report" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_recommendation_report_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "report_no" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "parent_report_id" int8,
  "report_name" varchar(300) COLLATE "pg_catalog"."default" NOT NULL,
  "schemes" text COLLATE "pg_catalog"."default",
  "simulation_params" text COLLATE "pg_catalog"."default",
  "implementation_path" text COLLATE "pg_catalog"."default",
  "risk_analysis" text COLLATE "pg_catalog"."default",
  "expert_comments" text COLLATE "pg_catalog"."default",
  "optimized_result" text COLLATE "pg_catalog"."default",
  "report_content" text COLLATE "pg_catalog"."default",
  "export_file_url" varchar(1000) COLLATE "pg_catalog"."default",
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_recommendation_report"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_recommendation_report"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_recommendation_report"."report_no" IS '报告编号';
COMMENT ON COLUMN "dwd"."policy_recommendation_report"."parent_report_id" IS '关联分析报告ID';
COMMENT ON COLUMN "dwd"."policy_recommendation_report"."report_name" IS '报告名称';
COMMENT ON COLUMN "dwd"."policy_recommendation_report"."schemes" IS '多方案对比数据（JSON数组）';
COMMENT ON COLUMN "dwd"."policy_recommendation_report"."simulation_params" IS '方案参数模拟配置（JSON）';
COMMENT ON COLUMN "dwd"."policy_recommendation_report"."implementation_path" IS '实施路径与时间表（JSON）';
COMMENT ON COLUMN "dwd"."policy_recommendation_report"."risk_analysis" IS '风险辅助分析（JSON）';
COMMENT ON COLUMN "dwd"."policy_recommendation_report"."expert_comments" IS '专家点评与互动意见（JSON数组）';
COMMENT ON COLUMN "dwd"."policy_recommendation_report"."optimized_result" IS '优化后推荐结果（JSON）';
COMMENT ON COLUMN "dwd"."policy_recommendation_report"."report_content" IS '完整报告内容';
COMMENT ON COLUMN "dwd"."policy_recommendation_report"."export_file_url" IS '导出文件URL';
COMMENT ON COLUMN "dwd"."policy_recommendation_report"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_recommendation_report"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_recommendation_report"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_recommendation_report"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_recommendation_report"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_recommendation_report"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."policy_recommendation_report" IS '推荐方案报告表';

-- ----------------------------
-- Records of policy_recommendation_report
-- ----------------------------

-- ----------------------------
-- Table structure for policy_search_condition
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_search_condition";
CREATE TABLE "dwd"."policy_search_condition" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_search_condition_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "search_id" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "condition_type" varchar(50) COLLATE "pg_catalog"."default",
  "condition_field" varchar(100) COLLATE "pg_catalog"."default",
  "condition_operator" varchar(20) COLLATE "pg_catalog"."default",
  "condition_value" text COLLATE "pg_catalog"."default",
  "sort_order" int4,
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_search_condition"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_search_condition"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_search_condition"."search_id" IS '关联检索记录ID';
COMMENT ON COLUMN "dwd"."policy_search_condition"."condition_type" IS '条件类型：CATEGORY/INDUSTRY/DEPT/REGION/LEVEL/STATUS/TIME/KEYWORD/LOGIC';
COMMENT ON COLUMN "dwd"."policy_search_condition"."condition_field" IS '条件字段名';
COMMENT ON COLUMN "dwd"."policy_search_condition"."condition_operator" IS '操作符：EQ/NE/GT/LT/GE/LE/IN/NOT_IN/LIKE/RANGE';
COMMENT ON COLUMN "dwd"."policy_search_condition"."condition_value" IS '条件值';
COMMENT ON COLUMN "dwd"."policy_search_condition"."sort_order" IS '条件排序';
COMMENT ON COLUMN "dwd"."policy_search_condition"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_search_condition"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_search_condition"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_search_condition"."ext1" IS '扩展字段1';
COMMENT ON TABLE "dwd"."policy_search_condition" IS '政策检索条件明细表';

-- ----------------------------
-- Records of policy_search_condition
-- ----------------------------

-- ----------------------------
-- Table structure for policy_search_record
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_search_record";
CREATE TABLE "dwd"."policy_search_record" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_search_record_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "user_id" int8 DEFAULT 0,
  "search_id" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "search_keywords" varchar(500) COLLATE "pg_catalog"."default",
  "search_mode" varchar(20) COLLATE "pg_catalog"."default",
  "result_count" int4,
  "search_time" timestamp(6),
  "response_time_ms" int4,
  "is_saved" int2,
  "client_ip" varchar(64) COLLATE "pg_catalog"."default",
  "user_agent" varchar(500) COLLATE "pg_catalog"."default",
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_search_record"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_search_record"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_search_record"."user_id" IS '用户ID 0匿名用户';
COMMENT ON COLUMN "dwd"."policy_search_record"."search_id" IS '检索唯一标识';
COMMENT ON COLUMN "dwd"."policy_search_record"."search_keywords" IS '检索关键词';
COMMENT ON COLUMN "dwd"."policy_search_record"."search_mode" IS '检索模式：BASIC-基础/ADVANCED-高级';
COMMENT ON COLUMN "dwd"."policy_search_record"."result_count" IS '返回结果数量';
COMMENT ON COLUMN "dwd"."policy_search_record"."search_time" IS '检索时间';
COMMENT ON COLUMN "dwd"."policy_search_record"."response_time_ms" IS '检索响应耗时(毫秒)';
COMMENT ON COLUMN "dwd"."policy_search_record"."is_saved" IS '是否收藏检索条件：0-否/1-是';
COMMENT ON COLUMN "dwd"."policy_search_record"."client_ip" IS '客户端IP';
COMMENT ON COLUMN "dwd"."policy_search_record"."user_agent" IS '客户端UA';
COMMENT ON COLUMN "dwd"."policy_search_record"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_search_record"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_search_record"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_search_record"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_search_record"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_search_record"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."policy_search_record" IS '政策检索记录表';

-- ----------------------------
-- Records of policy_search_record
-- ----------------------------

-- ----------------------------
-- Table structure for policy_simulation_param
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_simulation_param";
CREATE TABLE "dwd"."policy_simulation_param" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_simulation_param_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "simulation_id" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "simulation_type" varchar(50) COLLATE "pg_catalog"."default",
  "sub_type" varchar(100) COLLATE "pg_catalog"."default",
  "policy_id" varchar(64) COLLATE "pg_catalog"."default",
  "policy_type" varchar(100) COLLATE "pg_catalog"."default",
  "coverage_scope" text COLLATE "pg_catalog"."default",
  "support_intensity" numeric(10,2),
  "implementation_time" varchar(200) COLLATE "pg_catalog"."default",
  "simulation_dimensions" varchar(500) COLLATE "pg_catalog"."default",
  "custom_params" text COLLATE "pg_catalog"."default",
  "model_version" varchar(50) COLLATE "pg_catalog"."default",
  "creator_id" int8,
  "exec_status" int2,
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_simulation_param"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_simulation_param"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_simulation_param"."simulation_id" IS '推演任务唯一标识';
COMMENT ON COLUMN "dwd"."policy_simulation_param"."simulation_type" IS '推演类型：EFFECT-效果预估/TECH_POLICY-科技政策推演';
COMMENT ON COLUMN "dwd"."policy_simulation_param"."sub_type" IS '推演子类型：UNPUBLISHED/NEW_POLICY/REGIONAL_ECONOMY';
COMMENT ON COLUMN "dwd"."policy_simulation_param"."policy_id" IS '关联政策唯一标识';
COMMENT ON COLUMN "dwd"."policy_simulation_param"."policy_type" IS '政策类型参数';
COMMENT ON COLUMN "dwd"."policy_simulation_param"."coverage_scope" IS '覆盖范围参数（JSON）';
COMMENT ON COLUMN "dwd"."policy_simulation_param"."support_intensity" IS '支持力度参数 资金规模万元';
COMMENT ON COLUMN "dwd"."policy_simulation_param"."implementation_time" IS '实施时间参数';
COMMENT ON COLUMN "dwd"."policy_simulation_param"."simulation_dimensions" IS '推演维度（JSON数组）';
COMMENT ON COLUMN "dwd"."policy_simulation_param"."custom_params" IS '自定义参数（JSON）';
COMMENT ON COLUMN "dwd"."policy_simulation_param"."model_version" IS '推演模型版本号';
COMMENT ON COLUMN "dwd"."policy_simulation_param"."creator_id" IS '创建人ID';
COMMENT ON COLUMN "dwd"."policy_simulation_param"."exec_status" IS '执行状态：0-待执行/1-执行中/2-成功/3-失败';
COMMENT ON COLUMN "dwd"."policy_simulation_param"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_simulation_param"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_simulation_param"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_simulation_param"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_simulation_param"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_simulation_param"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."policy_simulation_param" IS '推演参数配置表';

-- ----------------------------
-- Records of policy_simulation_param
-- ----------------------------

-- ----------------------------
-- Table structure for policy_simulation_result
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_simulation_result";
CREATE TABLE "dwd"."policy_simulation_result" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_simulation_result_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "simulation_id" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "result_type" varchar(50) COLLATE "pg_catalog"."default",
  "result_summary" text COLLATE "pg_catalog"."default",
  "quantitative_result" text COLLATE "pg_catalog"."default",
  "qualitative_result" text COLLATE "pg_catalog"."default",
  "spatial_distribution" text COLLATE "pg_catalog"."default",
  "temporal_trend" text COLLATE "pg_catalog"."default",
  "stakeholder_feedback" text COLLATE "pg_catalog"."default",
  "visualization_data" text COLLATE "pg_catalog"."default",
  "interpretation_report" text COLLATE "pg_catalog"."default",
  "confidence_level" numeric(5,2),
  "exec_duration_ms" int4,
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_simulation_result"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_simulation_result"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_simulation_result"."simulation_id" IS '关联推演任务ID';
COMMENT ON COLUMN "dwd"."policy_simulation_result"."result_type" IS '结果类型：ECONOMIC/SOCIAL/INNOVATION/INDUSTRY/COMPREHENSIVE';
COMMENT ON COLUMN "dwd"."policy_simulation_result"."result_summary" IS '结果摘要';
COMMENT ON COLUMN "dwd"."policy_simulation_result"."quantitative_result" IS '定量推演结果（JSON）';
COMMENT ON COLUMN "dwd"."policy_simulation_result"."qualitative_result" IS '定性推演结果（JSON）';
COMMENT ON COLUMN "dwd"."policy_simulation_result"."spatial_distribution" IS '空间分布结果（JSON）';
COMMENT ON COLUMN "dwd"."policy_simulation_result"."temporal_trend" IS '时间变化趋势（JSON）';
COMMENT ON COLUMN "dwd"."policy_simulation_result"."stakeholder_feedback" IS '利益攸关方反馈汇总（JSON）';
COMMENT ON COLUMN "dwd"."policy_simulation_result"."visualization_data" IS '可视化模拟数据（JSON）';
COMMENT ON COLUMN "dwd"."policy_simulation_result"."interpretation_report" IS '解读报告内容';
COMMENT ON COLUMN "dwd"."policy_simulation_result"."confidence_level" IS '结果置信度(%)';
COMMENT ON COLUMN "dwd"."policy_simulation_result"."exec_duration_ms" IS '推演执行耗时(毫秒)';
COMMENT ON COLUMN "dwd"."policy_simulation_result"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_simulation_result"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_simulation_result"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_simulation_result"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_simulation_result"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_simulation_result"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."policy_simulation_result" IS '推演结果表';

-- ----------------------------
-- Records of policy_simulation_result
-- ----------------------------

-- ----------------------------
-- Table structure for policy_subscription
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_subscription";
CREATE TABLE "dwd"."policy_subscription" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_subscription_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "user_id" int8 NOT NULL,
  "subscription_name" varchar(200) COLLATE "pg_catalog"."default",
  "category_filter" varchar(500) COLLATE "pg_catalog"."default",
  "industry_filter" varchar(500) COLLATE "pg_catalog"."default",
  "dept_filter" varchar(500) COLLATE "pg_catalog"."default",
  "region_filter" varchar(500) COLLATE "pg_catalog"."default",
  "level_filter" varchar(100) COLLATE "pg_catalog"."default",
  "keyword_filter" varchar(500) COLLATE "pg_catalog"."default",
  "push_frequency" varchar(20) COLLATE "pg_catalog"."default",
  "push_channels" varchar(200) COLLATE "pg_catalog"."default",
  "is_enabled" int2,
  "last_push_time" timestamp(6),
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_subscription"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_subscription"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_subscription"."user_id" IS '用户ID';
COMMENT ON COLUMN "dwd"."policy_subscription"."subscription_name" IS '订阅名称';
COMMENT ON COLUMN "dwd"."policy_subscription"."category_filter" IS '政策类别筛选 逗号分隔';
COMMENT ON COLUMN "dwd"."policy_subscription"."industry_filter" IS '行业领域筛选 逗号分隔';
COMMENT ON COLUMN "dwd"."policy_subscription"."dept_filter" IS '发布部门筛选 逗号分隔';
COMMENT ON COLUMN "dwd"."policy_subscription"."region_filter" IS '地区筛选 逗号分隔';
COMMENT ON COLUMN "dwd"."policy_subscription"."level_filter" IS '效力级别筛选 逗号分隔';
COMMENT ON COLUMN "dwd"."policy_subscription"."keyword_filter" IS '关键词筛选';
COMMENT ON COLUMN "dwd"."policy_subscription"."push_frequency" IS '推送频率：REALTIME-实时/DAILY-每日/WEEKLY-每周/MONTHLY-每月';
COMMENT ON COLUMN "dwd"."policy_subscription"."push_channels" IS '推送渠道：SYSTEM/EMAIL/SMS 逗号分隔';
COMMENT ON COLUMN "dwd"."policy_subscription"."is_enabled" IS '是否启用：0-禁用/1-启用';
COMMENT ON COLUMN "dwd"."policy_subscription"."last_push_time" IS '上次推送时间';
COMMENT ON COLUMN "dwd"."policy_subscription"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_subscription"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_subscription"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_subscription"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_subscription"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_subscription"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."policy_subscription" IS '政策订阅表';

-- ----------------------------
-- Records of policy_subscription
-- ----------------------------

-- ----------------------------
-- Table structure for policy_support_assessment
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_support_assessment";
CREATE TABLE "dwd"."policy_support_assessment" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_support_assessment_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "assessment_id" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "target_domain" varchar(200) COLLATE "pg_catalog"."default",
  "strategy_guidance_score" numeric(8,4),
  "policy_support_score" numeric(8,4),
  "funding_support_score" numeric(8,4),
  "project_support_score" numeric(8,4),
  "implementation_effect_score" numeric(8,4),
  "composite_score" numeric(8,4),
  "composite_rank" int4,
  "indicator_detail" text COLLATE "pg_catalog"."default",
  "funding_structure" text COLLATE "pg_catalog"."default",
  "project_distribution" text COLLATE "pg_catalog"."default",
  "before_after_comparison" text COLLATE "pg_catalog"."default",
  "optimization_suggestions" text COLLATE "pg_catalog"."default",
  "delphi_result" text COLLATE "pg_catalog"."default",
  "simulation_prediction" text COLLATE "pg_catalog"."default",
  "knowledge_graph_refs" text COLLATE "pg_catalog"."default",
  "assessment_report_url" varchar(1000) COLLATE "pg_catalog"."default",
  "assessment_model_version" varchar(50) COLLATE "pg_catalog"."default",
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_support_assessment"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_support_assessment"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_support_assessment"."assessment_id" IS '评估任务唯一标识';
COMMENT ON COLUMN "dwd"."policy_support_assessment"."target_domain" IS '评估目标产业或领域';
COMMENT ON COLUMN "dwd"."policy_support_assessment"."strategy_guidance_score" IS '发展战略引导力得分';
COMMENT ON COLUMN "dwd"."policy_support_assessment"."policy_support_score" IS '政策扶持力度得分';
COMMENT ON COLUMN "dwd"."policy_support_assessment"."funding_support_score" IS '经费支持得分';
COMMENT ON COLUMN "dwd"."policy_support_assessment"."project_support_score" IS '项目支持得分';
COMMENT ON COLUMN "dwd"."policy_support_assessment"."implementation_effect_score" IS '政策实施效果得分';
COMMENT ON COLUMN "dwd"."policy_support_assessment"."composite_score" IS '综合得分';
COMMENT ON COLUMN "dwd"."policy_support_assessment"."composite_rank" IS '综合排名';
COMMENT ON COLUMN "dwd"."policy_support_assessment"."indicator_detail" IS '各指标评估详情（JSON）';
COMMENT ON COLUMN "dwd"."policy_support_assessment"."funding_structure" IS '经费结构分析（JSON）';
COMMENT ON COLUMN "dwd"."policy_support_assessment"."project_distribution" IS '项目分布分析（JSON）';
COMMENT ON COLUMN "dwd"."policy_support_assessment"."before_after_comparison" IS '政策实施前后对比（JSON）';
COMMENT ON COLUMN "dwd"."policy_support_assessment"."optimization_suggestions" IS '政策优化建议（JSON数组）';
COMMENT ON COLUMN "dwd"."policy_support_assessment"."delphi_result" IS '德尔菲法评估结果（JSON）';
COMMENT ON COLUMN "dwd"."policy_support_assessment"."simulation_prediction" IS '系统仿真模型预测结果（JSON）';
COMMENT ON COLUMN "dwd"."policy_support_assessment"."knowledge_graph_refs" IS '关联知识图谱引用（JSON）';
COMMENT ON COLUMN "dwd"."policy_support_assessment"."assessment_report_url" IS '评估报告文件URL';
COMMENT ON COLUMN "dwd"."policy_support_assessment"."assessment_model_version" IS '评估模型版本号';
COMMENT ON COLUMN "dwd"."policy_support_assessment"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_support_assessment"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_support_assessment"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_support_assessment"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_support_assessment"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_support_assessment"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."policy_support_assessment" IS '政策与条件保障力评估表';

-- ----------------------------
-- Records of policy_support_assessment
-- ----------------------------

-- ----------------------------
-- Table structure for policy_support_assessment_indicator
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_support_assessment_indicator";
CREATE TABLE "dwd"."policy_support_assessment_indicator" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_support_assessment_indicator_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "indicator_code" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "indicator_name" varchar(200) COLLATE "pg_catalog"."default" NOT NULL,
  "indicator_category" varchar(100) COLLATE "pg_catalog"."default",
  "parent_id" int8,
  "indicator_level" int2,
  "indicator_weight" numeric(5,4),
  "calculation_formula" text COLLATE "pg_catalog"."default",
  "data_source" varchar(500) COLLATE "pg_catalog"."default",
  "unit" varchar(50) COLLATE "pg_catalog"."default",
  "threshold_high" numeric(18,4),
  "threshold_medium" numeric(18,4),
  "sort_order" int4,
  "is_enabled" int2,
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_support_assessment_indicator"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_support_assessment_indicator"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_support_assessment_indicator"."indicator_code" IS '指标编码';
COMMENT ON COLUMN "dwd"."policy_support_assessment_indicator"."indicator_name" IS '指标名称';
COMMENT ON COLUMN "dwd"."policy_support_assessment_indicator"."indicator_category" IS '指标类别：STRATEGY/POLICY_SUPPORT/FUNDING/PROJECT/ENVIRONMENT/VISION';
COMMENT ON COLUMN "dwd"."policy_support_assessment_indicator"."parent_id" IS '父指标ID 层级指标体系';
COMMENT ON COLUMN "dwd"."policy_support_assessment_indicator"."indicator_level" IS '指标层级：1-一级/2-二级/3-三级';
COMMENT ON COLUMN "dwd"."policy_support_assessment_indicator"."indicator_weight" IS '指标权重 0-1';
COMMENT ON COLUMN "dwd"."policy_support_assessment_indicator"."calculation_formula" IS '计算公式说明';
COMMENT ON COLUMN "dwd"."policy_support_assessment_indicator"."data_source" IS '数据来源说明';
COMMENT ON COLUMN "dwd"."policy_support_assessment_indicator"."unit" IS '计量单位';
COMMENT ON COLUMN "dwd"."policy_support_assessment_indicator"."threshold_high" IS '优秀阈值';
COMMENT ON COLUMN "dwd"."policy_support_assessment_indicator"."threshold_medium" IS '合格阈值';
COMMENT ON COLUMN "dwd"."policy_support_assessment_indicator"."sort_order" IS '排序序号';
COMMENT ON COLUMN "dwd"."policy_support_assessment_indicator"."is_enabled" IS '是否启用：0-禁用/1-启用';
COMMENT ON COLUMN "dwd"."policy_support_assessment_indicator"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_support_assessment_indicator"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_support_assessment_indicator"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_support_assessment_indicator"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_support_assessment_indicator"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_support_assessment_indicator"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."policy_support_assessment_indicator" IS '政策与条件保障力评估指标表';

-- ----------------------------
-- Records of policy_support_assessment_indicator
-- ----------------------------

-- ----------------------------
-- Table structure for policy_support_overview
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_support_overview";
CREATE TABLE "dwd"."policy_support_overview" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_support_overview_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "stat_date" date NOT NULL,
  "scope_type" varchar(20) COLLATE "pg_catalog"."default",
  "scope_code" varchar(50) COLLATE "pg_catalog"."default",
  "scope_name" varchar(100) COLLATE "pg_catalog"."default",
  "industry_type" varchar(100) COLLATE "pg_catalog"."default",
  "total_policy_count" int4,
  "continuity_index" numeric(8,4),
  "yearly_distribution" text COLLATE "pg_catalog"."default",
  "level_distribution" text COLLATE "pg_catalog"."default",
  "type_distribution" text COLLATE "pg_catalog"."default",
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_support_overview"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_support_overview"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_support_overview"."stat_date" IS '统计日期';
COMMENT ON COLUMN "dwd"."policy_support_overview"."scope_type" IS '统计范围类型：NATIONAL-全国/PROVINCE-省级/CITY-市级/SHENZHEN-深圳';
COMMENT ON COLUMN "dwd"."policy_support_overview"."scope_code" IS '范围编码';
COMMENT ON COLUMN "dwd"."policy_support_overview"."scope_name" IS '范围名称';
COMMENT ON COLUMN "dwd"."policy_support_overview"."industry_type" IS '产业类型';
COMMENT ON COLUMN "dwd"."policy_support_overview"."total_policy_count" IS '政策总数量';
COMMENT ON COLUMN "dwd"."policy_support_overview"."continuity_index" IS '政策连续性指数';
COMMENT ON COLUMN "dwd"."policy_support_overview"."yearly_distribution" IS '年度分布（JSON）';
COMMENT ON COLUMN "dwd"."policy_support_overview"."level_distribution" IS '层级分布（JSON）';
COMMENT ON COLUMN "dwd"."policy_support_overview"."type_distribution" IS '类型分布（JSON）';
COMMENT ON COLUMN "dwd"."policy_support_overview"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_support_overview"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_support_overview"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_support_overview"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_support_overview"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_support_overview"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."policy_support_overview" IS '政策扶持概况统计表';

-- ----------------------------
-- Records of policy_support_overview
-- ----------------------------

-- ----------------------------
-- Table structure for policy_support_rank
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_support_rank";
CREATE TABLE "dwd"."policy_support_rank" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_support_rank_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "stat_date" date NOT NULL,
  "rank_type" varchar(20) COLLATE "pg_catalog"."default",
  "scope_code" varchar(50) COLLATE "pg_catalog"."default",
  "scope_name" varchar(100) COLLATE "pg_catalog"."default",
  "industry_type" varchar(100) COLLATE "pg_catalog"."default",
  "rank_num" int4,
  "intensity_index" numeric(8,4),
  "key_indicators" text COLLATE "pg_catalog"."default",
  "support_count" int4,
  "fund_scale" numeric(18,2),
  "coverage_rate" numeric(5,2),
  "previous_rank" int4,
  "rank_change" int4,
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_support_rank"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_support_rank"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_support_rank"."stat_date" IS '统计日期';
COMMENT ON COLUMN "dwd"."policy_support_rank"."rank_type" IS '排名类型：PROVINCE-省级/CITY-城市级';
COMMENT ON COLUMN "dwd"."policy_support_rank"."scope_code" IS '地区编码';
COMMENT ON COLUMN "dwd"."policy_support_rank"."scope_name" IS '地区名称';
COMMENT ON COLUMN "dwd"."policy_support_rank"."industry_type" IS '产业类型';
COMMENT ON COLUMN "dwd"."policy_support_rank"."rank_num" IS '排名序号';
COMMENT ON COLUMN "dwd"."policy_support_rank"."intensity_index" IS '政策力度指数';
COMMENT ON COLUMN "dwd"."policy_support_rank"."key_indicators" IS '关键指标提取结果（JSON）';
COMMENT ON COLUMN "dwd"."policy_support_rank"."support_count" IS '扶持政策数量';
COMMENT ON COLUMN "dwd"."policy_support_rank"."fund_scale" IS '资金规模(万元)';
COMMENT ON COLUMN "dwd"."policy_support_rank"."coverage_rate" IS '产业覆盖率(%)';
COMMENT ON COLUMN "dwd"."policy_support_rank"."previous_rank" IS '上期排名';
COMMENT ON COLUMN "dwd"."policy_support_rank"."rank_change" IS '排名变化 正升负降';
COMMENT ON COLUMN "dwd"."policy_support_rank"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_support_rank"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_support_rank"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_support_rank"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_support_rank"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_support_rank"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."policy_support_rank" IS '政策力度排名表';

-- ----------------------------
-- Records of policy_support_rank
-- ----------------------------

-- ----------------------------
-- Table structure for policy_time_analysis
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_time_analysis";
CREATE TABLE "dwd"."policy_time_analysis" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_time_analysis_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "analysis_id" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "target_industry" varchar(200) COLLATE "pg_catalog"."default",
  "time_range_start" date,
  "time_range_end" date,
  "density_index_series" text COLLATE "pg_catalog"."default",
  "intensity_trend_series" text COLLATE "pg_catalog"."default",
  "key_nodes" text COLLATE "pg_catalog"."default",
  "cycle_pattern" text COLLATE "pg_catalog"."default",
  "policy_window_forecast" text COLLATE "pg_catalog"."default",
  "associated_policies" text COLLATE "pg_catalog"."default",
  "visualization_config" text COLLATE "pg_catalog"."default",
  "analysis_model_version" varchar(50) COLLATE "pg_catalog"."default",
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_time_analysis"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_time_analysis"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_time_analysis"."analysis_id" IS '分析任务唯一标识';
COMMENT ON COLUMN "dwd"."policy_time_analysis"."target_industry" IS '目标产业或技术领域';
COMMENT ON COLUMN "dwd"."policy_time_analysis"."time_range_start" IS '时间范围起始';
COMMENT ON COLUMN "dwd"."policy_time_analysis"."time_range_end" IS '时间范围结束';
COMMENT ON COLUMN "dwd"."policy_time_analysis"."density_index_series" IS '政策密度指数时序数据（JSON数组）';
COMMENT ON COLUMN "dwd"."policy_time_analysis"."intensity_trend_series" IS '支持强度趋势时序数据（JSON数组）';
COMMENT ON COLUMN "dwd"."policy_time_analysis"."key_nodes" IS '关键节点识别结果（JSON数组）';
COMMENT ON COLUMN "dwd"."policy_time_analysis"."cycle_pattern" IS '周期性规律分析（JSON）';
COMMENT ON COLUMN "dwd"."policy_time_analysis"."policy_window_forecast" IS '政策窗口期预判（JSON）';
COMMENT ON COLUMN "dwd"."policy_time_analysis"."associated_policies" IS '关联政策列表（JSON）';
COMMENT ON COLUMN "dwd"."policy_time_analysis"."visualization_config" IS '可视化配置（JSON）';
COMMENT ON COLUMN "dwd"."policy_time_analysis"."analysis_model_version" IS '分析模型版本号';
COMMENT ON COLUMN "dwd"."policy_time_analysis"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_time_analysis"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_time_analysis"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_time_analysis"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_time_analysis"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_time_analysis"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."policy_time_analysis" IS '政策时序分析结果表';

-- ----------------------------
-- Records of policy_time_analysis
-- ----------------------------

-- ----------------------------
-- Table structure for policy_time_series_indicator
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_time_series_indicator";
CREATE TABLE "dwd"."policy_time_series_indicator" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_time_series_indicator_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "stat_date" date NOT NULL,
  "stat_period" varchar(20) COLLATE "pg_catalog"."default",
  "period_label" varchar(50) COLLATE "pg_catalog"."default",
  "publish_count" int4,
  "chain_ratio" numeric(10,4),
  "year_over_year_ratio" numeric(10,4),
  "cumulative_count" int4,
  "avg_daily_count" numeric(5,2),
  "theme_distribution" text COLLATE "pg_catalog"."default",
  "dept_distribution" text COLLATE "pg_catalog"."default",
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_time_series_indicator"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_time_series_indicator"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_time_series_indicator"."stat_date" IS '统计日期';
COMMENT ON COLUMN "dwd"."policy_time_series_indicator"."stat_period" IS '统计周期：YEAR/MONTH/QUARTER/DAY';
COMMENT ON COLUMN "dwd"."policy_time_series_indicator"."period_label" IS '周期标签 如2024、2024-Q1';
COMMENT ON COLUMN "dwd"."policy_time_series_indicator"."publish_count" IS '政策发布数量';
COMMENT ON COLUMN "dwd"."policy_time_series_indicator"."chain_ratio" IS '环比增长率';
COMMENT ON COLUMN "dwd"."policy_time_series_indicator"."year_over_year_ratio" IS '同比增长率';
COMMENT ON COLUMN "dwd"."policy_time_series_indicator"."cumulative_count" IS '累计发布数量';
COMMENT ON COLUMN "dwd"."policy_time_series_indicator"."avg_daily_count" IS '日均发布量';
COMMENT ON COLUMN "dwd"."policy_time_series_indicator"."theme_distribution" IS '主题分布（JSON）';
COMMENT ON COLUMN "dwd"."policy_time_series_indicator"."dept_distribution" IS '发布部门分布（JSON）';
COMMENT ON COLUMN "dwd"."policy_time_series_indicator"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_time_series_indicator"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_time_series_indicator"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_time_series_indicator"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_time_series_indicator"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_time_series_indicator"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."policy_time_series_indicator" IS '政策时序指标统计表';

-- ----------------------------
-- Records of policy_time_series_indicator
-- ----------------------------

-- ----------------------------
-- Table structure for policy_type_indicator
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_type_indicator";
CREATE TABLE "dwd"."policy_type_indicator" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_type_indicator_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "stat_date" date NOT NULL,
  "stat_period" varchar(20) COLLATE "pg_catalog"."default",
  "policy_type" varchar(100) COLLATE "pg_catalog"."default",
  "policy_count" int4,
  "policy_count_chain_ratio" numeric(10,4),
  "policy_count_year_over_year" numeric(10,4),
  "policy_proportion" numeric(5,2),
  "level1_count" int4,
  "level2_count" int4,
  "level3_count" int4,
  "level4_count" int4,
  "detail_data" text COLLATE "pg_catalog"."default",
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_type_indicator"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_type_indicator"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_type_indicator"."stat_date" IS '统计日期';
COMMENT ON COLUMN "dwd"."policy_type_indicator"."stat_period" IS '统计周期：YEAR/MONTH/QUARTER';
COMMENT ON COLUMN "dwd"."policy_type_indicator"."policy_type" IS '政策类型：产业/人才/企业扶持/财税/金融等';
COMMENT ON COLUMN "dwd"."policy_type_indicator"."policy_count" IS '该类型政策数量';
COMMENT ON COLUMN "dwd"."policy_type_indicator"."policy_count_chain_ratio" IS '环比增长率';
COMMENT ON COLUMN "dwd"."policy_type_indicator"."policy_count_year_over_year" IS '同比增长率';
COMMENT ON COLUMN "dwd"."policy_type_indicator"."policy_proportion" IS '类型占比(%)';
COMMENT ON COLUMN "dwd"."policy_type_indicator"."level1_count" IS '国家级数量';
COMMENT ON COLUMN "dwd"."policy_type_indicator"."level2_count" IS '省级数量';
COMMENT ON COLUMN "dwd"."policy_type_indicator"."level3_count" IS '市级数量';
COMMENT ON COLUMN "dwd"."policy_type_indicator"."level4_count" IS '区级数量';
COMMENT ON COLUMN "dwd"."policy_type_indicator"."detail_data" IS '明细数据（JSON）';
COMMENT ON COLUMN "dwd"."policy_type_indicator"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_type_indicator"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_type_indicator"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_type_indicator"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_type_indicator"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_type_indicator"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."policy_type_indicator" IS '政策类型指标统计表';

-- ----------------------------
-- Records of policy_type_indicator
-- ----------------------------

-- ----------------------------
-- Table structure for policy_weakness_result
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."policy_weakness_result";
CREATE TABLE "dwd"."policy_weakness_result" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".policy_weakness_result_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "policy_id" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "analysis_batch_no" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "weakness_items" text COLLATE "pg_catalog"."default",
  "coverage_gap" text COLLATE "pg_catalog"."default",
  "execution_gap" text COLLATE "pg_catalog"."default",
  "target_achievement_gap" text COLLATE "pg_catalog"."default",
  "compliance_gap" text COLLATE "pg_catalog"."default",
  "cause_analysis" text COLLATE "pg_catalog"."default",
  "improvement_strategies" text COLLATE "pg_catalog"."default",
  "responsible_departments" text COLLATE "pg_catalog"."default",
  "analysis_model_version" varchar(50) COLLATE "pg_catalog"."default",
  "exec_status" int2,
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."policy_weakness_result"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."policy_weakness_result"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."policy_weakness_result"."policy_id" IS '政策唯一标识';
COMMENT ON COLUMN "dwd"."policy_weakness_result"."analysis_batch_no" IS '分析批次号';
COMMENT ON COLUMN "dwd"."policy_weakness_result"."weakness_items" IS '政策短板清单（JSON数组）';
COMMENT ON COLUMN "dwd"."policy_weakness_result"."coverage_gap" IS '覆盖范围缺口分析（JSON）';
COMMENT ON COLUMN "dwd"."policy_weakness_result"."execution_gap" IS '实施执行度缺口分析（JSON）';
COMMENT ON COLUMN "dwd"."policy_weakness_result"."target_achievement_gap" IS '目标达成率缺口分析（JSON）';
COMMENT ON COLUMN "dwd"."policy_weakness_result"."compliance_gap" IS '合规情况缺口分析（JSON）';
COMMENT ON COLUMN "dwd"."policy_weakness_result"."cause_analysis" IS '短板成因分析（JSON）';
COMMENT ON COLUMN "dwd"."policy_weakness_result"."improvement_strategies" IS '改进策略建议（JSON数组）';
COMMENT ON COLUMN "dwd"."policy_weakness_result"."responsible_departments" IS '涉及责任部门（JSON数组）';
COMMENT ON COLUMN "dwd"."policy_weakness_result"."analysis_model_version" IS '分析模型版本号';
COMMENT ON COLUMN "dwd"."policy_weakness_result"."exec_status" IS '执行状态：1-成功/2-部分成功/3-失败';
COMMENT ON COLUMN "dwd"."policy_weakness_result"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."policy_weakness_result"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."policy_weakness_result"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."policy_weakness_result"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."policy_weakness_result"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."policy_weakness_result"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."policy_weakness_result" IS '政策短板识别结果表';

-- ----------------------------
-- Records of policy_weakness_result
-- ----------------------------

-- ----------------------------
-- Table structure for regional_policy_compare
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."regional_policy_compare";
CREATE TABLE "dwd"."regional_policy_compare" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".regional_policy_compare_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "compare_id" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "target_industry" varchar(200) COLLATE "pg_catalog"."default",
  "compare_regions" text COLLATE "pg_catalog"."default",
  "structured_clauses" text COLLATE "pg_catalog"."default",
  "contrast_matrix" text COLLATE "pg_catalog"."default",
  "advantage_analysis" text COLLATE "pg_catalog"."default",
  "similarity_score" numeric(5,2),
  "difference_points" text COLLATE "pg_catalog"."default",
  "recommendation" text COLLATE "pg_catalog"."default",
  "visualization_config" text COLLATE "pg_catalog"."default",
  "analysis_model_version" varchar(50) COLLATE "pg_catalog"."default",
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."regional_policy_compare"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."regional_policy_compare"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."regional_policy_compare"."compare_id" IS '对比任务唯一标识';
COMMENT ON COLUMN "dwd"."regional_policy_compare"."target_industry" IS '目标产业或技术领域';
COMMENT ON COLUMN "dwd"."regional_policy_compare"."compare_regions" IS '对比区域列表（JSON数组）';
COMMENT ON COLUMN "dwd"."regional_policy_compare"."structured_clauses" IS '结构化条款提取结果（JSON）';
COMMENT ON COLUMN "dwd"."regional_policy_compare"."contrast_matrix" IS '对比矩阵数据（JSON）';
COMMENT ON COLUMN "dwd"."regional_policy_compare"."advantage_analysis" IS '竞争优势分析（JSON）';
COMMENT ON COLUMN "dwd"."regional_policy_compare"."similarity_score" IS '政策相似度得分';
COMMENT ON COLUMN "dwd"."regional_policy_compare"."difference_points" IS '差异点分析（JSON数组）';
COMMENT ON COLUMN "dwd"."regional_policy_compare"."recommendation" IS '借鉴建议（JSON）';
COMMENT ON COLUMN "dwd"."regional_policy_compare"."visualization_config" IS '可视化配置（JSON）';
COMMENT ON COLUMN "dwd"."regional_policy_compare"."analysis_model_version" IS '分析模型版本号';
COMMENT ON COLUMN "dwd"."regional_policy_compare"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."regional_policy_compare"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."regional_policy_compare"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."regional_policy_compare"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."regional_policy_compare"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."regional_policy_compare"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."regional_policy_compare" IS '区域政策对比结果表';

-- ----------------------------
-- Records of regional_policy_compare
-- ----------------------------

-- ----------------------------
-- Table structure for shenzhen_policy_compare
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."shenzhen_policy_compare";
CREATE TABLE "dwd"."shenzhen_policy_compare" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".shenzhen_policy_compare_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "stat_date" date NOT NULL,
  "compare_type" varchar(50) COLLATE "pg_catalog"."default",
  "district_code" varchar(20) COLLATE "pg_catalog"."default",
  "district_name" varchar(100) COLLATE "pg_catalog"."default",
  "industry_type" varchar(100) COLLATE "pg_catalog"."default",
  "policy_count" int4,
  "trend_data" text COLLATE "pg_catalog"."default",
  "coverage_nodes" text COLLATE "pg_catalog"."default",
  "comparison_result" text COLLATE "pg_catalog"."default",
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."shenzhen_policy_compare"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."shenzhen_policy_compare"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."shenzhen_policy_compare"."stat_date" IS '统计日期';
COMMENT ON COLUMN "dwd"."shenzhen_policy_compare"."compare_type" IS '对比类型：QUANTITY-数量/REGION-区域/INDUSTRY-产业/LATEST-最新政策';
COMMENT ON COLUMN "dwd"."shenzhen_policy_compare"."district_code" IS '深圳各区编码';
COMMENT ON COLUMN "dwd"."shenzhen_policy_compare"."district_name" IS '区名称';
COMMENT ON COLUMN "dwd"."shenzhen_policy_compare"."industry_type" IS '产业类型';
COMMENT ON COLUMN "dwd"."shenzhen_policy_compare"."policy_count" IS '政策数量';
COMMENT ON COLUMN "dwd"."shenzhen_policy_compare"."trend_data" IS '趋势数据（JSON）';
COMMENT ON COLUMN "dwd"."shenzhen_policy_compare"."coverage_nodes" IS '产业链节点覆盖（JSON数组）';
COMMENT ON COLUMN "dwd"."shenzhen_policy_compare"."comparison_result" IS '对比结果详情（JSON）';
COMMENT ON COLUMN "dwd"."shenzhen_policy_compare"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."shenzhen_policy_compare"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."shenzhen_policy_compare"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."shenzhen_policy_compare"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."shenzhen_policy_compare"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."shenzhen_policy_compare"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."shenzhen_policy_compare" IS '深圳政策对比分析表';

-- ----------------------------
-- Records of shenzhen_policy_compare
-- ----------------------------

-- ----------------------------
-- Table structure for shenzhen_policy_distribution
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."shenzhen_policy_distribution";
CREATE TABLE "dwd"."shenzhen_policy_distribution" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".shenzhen_policy_distribution_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "stat_date" date NOT NULL,
  "stat_period" varchar(20) COLLATE "pg_catalog"."default",
  "district_code" varchar(20) COLLATE "pg_catalog"."default",
  "district_name" varchar(100) COLLATE "pg_catalog"."default",
  "policy_count" int4,
  "chain_ratio" numeric(10,4),
  "year_over_year_ratio" numeric(10,4),
  "industry_count" int4,
  "talent_count" int4,
  "enterprise_count" int4,
  "rank_citywide" int4,
  "coverage_industry" text COLLATE "pg_catalog"."default",
  "detail_data" text COLLATE "pg_catalog"."default",
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."shenzhen_policy_distribution"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."shenzhen_policy_distribution"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."shenzhen_policy_distribution"."stat_date" IS '统计日期';
COMMENT ON COLUMN "dwd"."shenzhen_policy_distribution"."stat_period" IS '统计周期';
COMMENT ON COLUMN "dwd"."shenzhen_policy_distribution"."district_code" IS '深圳各区行政区划代码';
COMMENT ON COLUMN "dwd"."shenzhen_policy_distribution"."district_name" IS '区名称';
COMMENT ON COLUMN "dwd"."shenzhen_policy_distribution"."policy_count" IS '政策数量';
COMMENT ON COLUMN "dwd"."shenzhen_policy_distribution"."chain_ratio" IS '环比增长率';
COMMENT ON COLUMN "dwd"."shenzhen_policy_distribution"."year_over_year_ratio" IS '同比增长率';
COMMENT ON COLUMN "dwd"."shenzhen_policy_distribution"."industry_count" IS '产业政策数量';
COMMENT ON COLUMN "dwd"."shenzhen_policy_distribution"."talent_count" IS '人才政策数量';
COMMENT ON COLUMN "dwd"."shenzhen_policy_distribution"."enterprise_count" IS '企业扶持政策数量';
COMMENT ON COLUMN "dwd"."shenzhen_policy_distribution"."rank_citywide" IS '全市排名';
COMMENT ON COLUMN "dwd"."shenzhen_policy_distribution"."coverage_industry" IS '产业覆盖情况（JSON）';
COMMENT ON COLUMN "dwd"."shenzhen_policy_distribution"."detail_data" IS '明细数据（JSON）';
COMMENT ON COLUMN "dwd"."shenzhen_policy_distribution"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."shenzhen_policy_distribution"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."shenzhen_policy_distribution"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."shenzhen_policy_distribution"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."shenzhen_policy_distribution"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."shenzhen_policy_distribution"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."shenzhen_policy_distribution" IS '深圳政策分布指标表';

-- ----------------------------
-- Records of shenzhen_policy_distribution
-- ----------------------------

-- ----------------------------
-- Table structure for shenzhen_policy_status
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."shenzhen_policy_status";
CREATE TABLE "dwd"."shenzhen_policy_status" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".shenzhen_policy_status_id_seq'::regclass),
  "tenant_id" int8 NOT NULL,
  "analysis_id" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "target_industry" varchar(200) COLLATE "pg_catalog"."default",
  "support_intensity_score" numeric(8,4),
  "industry_adaptability_score" numeric(8,4),
  "implementation_effectiveness_score" numeric(8,4),
  "composite_score" numeric(8,4),
  "indicator_weights" text COLLATE "pg_catalog"."default",
  "indicator_scores" text COLLATE "pg_catalog"."default",
  "advantage_areas" text COLLATE "pg_catalog"."default",
  "weakness_areas" text COLLATE "pg_catalog"."default",
  "optimization_plan" text COLLATE "pg_catalog"."default",
  "competitiveness_report" text COLLATE "pg_catalog"."default",
  "dashboard_config" text COLLATE "pg_catalog"."default",
  "analysis_model_version" varchar(50) COLLATE "pg_catalog"."default",
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."shenzhen_policy_status"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."shenzhen_policy_status"."tenant_id" IS '租户ID';
COMMENT ON COLUMN "dwd"."shenzhen_policy_status"."analysis_id" IS '分析任务唯一标识';
COMMENT ON COLUMN "dwd"."shenzhen_policy_status"."target_industry" IS '目标产业或技术领域';
COMMENT ON COLUMN "dwd"."shenzhen_policy_status"."support_intensity_score" IS '支持力度得分';
COMMENT ON COLUMN "dwd"."shenzhen_policy_status"."industry_adaptability_score" IS '产业适配性得分';
COMMENT ON COLUMN "dwd"."shenzhen_policy_status"."implementation_effectiveness_score" IS '落地实效性得分';
COMMENT ON COLUMN "dwd"."shenzhen_policy_status"."composite_score" IS '综合得分';
COMMENT ON COLUMN "dwd"."shenzhen_policy_status"."indicator_weights" IS '指标权重配置（JSON）';
COMMENT ON COLUMN "dwd"."shenzhen_policy_status"."indicator_scores" IS '各指标得分明细（JSON）';
COMMENT ON COLUMN "dwd"."shenzhen_policy_status"."advantage_areas" IS '优势领域（JSON数组）';
COMMENT ON COLUMN "dwd"."shenzhen_policy_status"."weakness_areas" IS '短板环节（JSON数组）';
COMMENT ON COLUMN "dwd"."shenzhen_policy_status"."optimization_plan" IS '针对性优化方案（JSON）';
COMMENT ON COLUMN "dwd"."shenzhen_policy_status"."competitiveness_report" IS '政策竞争力评估报告';
COMMENT ON COLUMN "dwd"."shenzhen_policy_status"."dashboard_config" IS '仪表盘可视化配置（JSON）';
COMMENT ON COLUMN "dwd"."shenzhen_policy_status"."analysis_model_version" IS '分析模型版本号';
COMMENT ON COLUMN "dwd"."shenzhen_policy_status"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."shenzhen_policy_status"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."shenzhen_policy_status"."is_deleted" IS '逻辑删除标记';
COMMENT ON COLUMN "dwd"."shenzhen_policy_status"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."shenzhen_policy_status"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."shenzhen_policy_status"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."shenzhen_policy_status" IS '深圳政策现状分析表';

-- ----------------------------
-- Records of shenzhen_policy_status
-- ----------------------------

-- ----------------------------
-- Table structure for tenant_info
-- ----------------------------
DROP TABLE IF EXISTS "dwd"."tenant_info";
CREATE TABLE "dwd"."tenant_info" (
  "id" int8 NOT NULL DEFAULT nextval('"dwd".tenant_info_id_seq'::regclass),
  "tenant_code" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "tenant_name" varchar(200) COLLATE "pg_catalog"."default" NOT NULL,
  "tenant_type" varchar(50) COLLATE "pg_catalog"."default",
  "contact_name" varchar(100) COLLATE "pg_catalog"."default",
  "contact_phone" varchar(50) COLLATE "pg_catalog"."default",
  "contact_email" varchar(200) COLLATE "pg_catalog"."default",
  "region" varchar(200) COLLATE "pg_catalog"."default",
  "industry" varchar(200) COLLATE "pg_catalog"."default",
  "license_no" varchar(200) COLLATE "pg_catalog"."default",
  "status" int2,
  "expire_time" timestamp(6),
  "data_source_scope" text COLLATE "pg_catalog"."default",
  "feature_permissions" text COLLATE "pg_catalog"."default",
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" int2 DEFAULT 0,
  "ext1" varchar(500) COLLATE "pg_catalog"."default",
  "ext2" varchar(500) COLLATE "pg_catalog"."default",
  "ext3" varchar(500) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "dwd"."tenant_info"."id" IS '主键ID';
COMMENT ON COLUMN "dwd"."tenant_info"."tenant_code" IS '租户编码（业务唯一标识）';
COMMENT ON COLUMN "dwd"."tenant_info"."tenant_name" IS '租户名称';
COMMENT ON COLUMN "dwd"."tenant_info"."tenant_type" IS '租户类型：GOVERNMENT-政府/ENTERPRISE-企业/INSTITUTION-机构';
COMMENT ON COLUMN "dwd"."tenant_info"."contact_name" IS '联系人姓名';
COMMENT ON COLUMN "dwd"."tenant_info"."contact_phone" IS '联系人电话';
COMMENT ON COLUMN "dwd"."tenant_info"."contact_email" IS '联系人邮箱';
COMMENT ON COLUMN "dwd"."tenant_info"."region" IS '所属地区';
COMMENT ON COLUMN "dwd"."tenant_info"."industry" IS '所属行业';
COMMENT ON COLUMN "dwd"."tenant_info"."license_no" IS '营业执照号或机构代码';
COMMENT ON COLUMN "dwd"."tenant_info"."status" IS '租户状态：0-禁用/1-启用/2-到期';
COMMENT ON COLUMN "dwd"."tenant_info"."expire_time" IS '到期时间';
COMMENT ON COLUMN "dwd"."tenant_info"."data_source_scope" IS '数据源权限范围（JSON）';
COMMENT ON COLUMN "dwd"."tenant_info"."feature_permissions" IS '功能权限配置（JSON）';
COMMENT ON COLUMN "dwd"."tenant_info"."create_time" IS '创建时间';
COMMENT ON COLUMN "dwd"."tenant_info"."update_time" IS '更新时间';
COMMENT ON COLUMN "dwd"."tenant_info"."is_deleted" IS '逻辑删除标记：0-未删除/1-已删除';
COMMENT ON COLUMN "dwd"."tenant_info"."ext1" IS '扩展字段1';
COMMENT ON COLUMN "dwd"."tenant_info"."ext2" IS '扩展字段2';
COMMENT ON COLUMN "dwd"."tenant_info"."ext3" IS '扩展字段3';
COMMENT ON TABLE "dwd"."tenant_info" IS '租户信息表';

-- ----------------------------
-- Records of tenant_info
-- ----------------------------

-- ----------------------------
-- Function structure for create_update_trigger
-- ----------------------------
DROP FUNCTION IF EXISTS "dwd"."create_update_trigger"("tbl_name" text);
CREATE FUNCTION "dwd"."create_update_trigger"("tbl_name" text)
  RETURNS "pg_catalog"."void" AS $BODY$
BEGIN
    EXECUTE format(
        'CREATE TRIGGER trg_%s_update_time
         BEFORE UPDATE ON %I
         FOR EACH ROW
         EXECUTE FUNCTION update_timestamp_func()',
        tbl_name, tbl_name
    );
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

-- ----------------------------
-- Function structure for update_timestamp_func
-- ----------------------------
DROP FUNCTION IF EXISTS "dwd"."update_timestamp_func"();
CREATE FUNCTION "dwd"."update_timestamp_func"()
  RETURNS "pg_catalog"."trigger" AS $BODY$
BEGIN
    NEW.update_time = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."enterprise_business_tag_id_seq"
OWNED BY "dwd"."enterprise_business_tag"."id";
SELECT setval('"dwd"."enterprise_business_tag_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."enterprise_cooperation_id_seq"
OWNED BY "dwd"."enterprise_cooperation"."id";
SELECT setval('"dwd"."enterprise_cooperation_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."enterprise_finance_history_id_seq"
OWNED BY "dwd"."enterprise_finance_history"."id";
SELECT setval('"dwd"."enterprise_finance_history_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."enterprise_id_seq"
OWNED BY "dwd"."enterprise"."id";
SELECT setval('"dwd"."enterprise_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."enterprise_industry_id_seq"
OWNED BY "dwd"."enterprise_industry"."id";
SELECT setval('"dwd"."enterprise_industry_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."enterprise_parent_subsidiary_id_seq"
OWNED BY "dwd"."enterprise_parent_subsidiary"."id";
SELECT setval('"dwd"."enterprise_parent_subsidiary_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."enterprise_patent_history_id_seq"
OWNED BY "dwd"."enterprise_patent_history"."id";
SELECT setval('"dwd"."enterprise_patent_history_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."enterprise_supply_chain_id_seq"
OWNED BY "dwd"."enterprise_supply_chain"."id";
SELECT setval('"dwd"."enterprise_supply_chain_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."national_policy_distribution_id_seq"
OWNED BY "dwd"."national_policy_distribution"."id";
SELECT setval('"dwd"."national_policy_distribution_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_analysis_report_id_seq"
OWNED BY "dwd"."policy_analysis_report"."id";
SELECT setval('"dwd"."policy_analysis_report_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_base_info_id_seq"
OWNED BY "dwd"."policy_base_info"."id";
SELECT setval('"dwd"."policy_base_info_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_effect_eval_id_seq"
OWNED BY "dwd"."policy_effect_eval"."id";
SELECT setval('"dwd"."policy_effect_eval_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_entity_id_seq"
OWNED BY "dwd"."policy_entity"."id";
SELECT setval('"dwd"."policy_entity_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_entity_relation_id_seq"
OWNED BY "dwd"."policy_entity_relation"."id";
SELECT setval('"dwd"."policy_entity_relation_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_entity_type_id_seq"
OWNED BY "dwd"."policy_entity_type"."id";
SELECT setval('"dwd"."policy_entity_type_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_favorite_id_seq"
OWNED BY "dwd"."policy_favorite"."id";
SELECT setval('"dwd"."policy_favorite_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_focus_result_id_seq"
OWNED BY "dwd"."policy_focus_result"."id";
SELECT setval('"dwd"."policy_focus_result_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_intensity_eval_id_seq"
OWNED BY "dwd"."policy_intensity_eval"."id";
SELECT setval('"dwd"."policy_intensity_eval_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_interpretation_report_id_seq"
OWNED BY "dwd"."policy_interpretation_report"."id";
SELECT setval('"dwd"."policy_interpretation_report_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_latest_news_id_seq"
OWNED BY "dwd"."policy_latest_news"."id";
SELECT setval('"dwd"."policy_latest_news_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_layout_recommend_id_seq"
OWNED BY "dwd"."policy_layout_recommend"."id";
SELECT setval('"dwd"."policy_layout_recommend_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_level_indicator_id_seq"
OWNED BY "dwd"."policy_level_indicator"."id";
SELECT setval('"dwd"."policy_level_indicator_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_opportunity_result_id_seq"
OWNED BY "dwd"."policy_opportunity_result"."id";
SELECT setval('"dwd"."policy_opportunity_result_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_prediction_indicator_id_seq"
OWNED BY "dwd"."policy_prediction_indicator"."id";
SELECT setval('"dwd"."policy_prediction_indicator_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_public_opinion_id_seq"
OWNED BY "dwd"."policy_public_opinion"."id";
SELECT setval('"dwd"."policy_public_opinion_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_recommendation_report_id_seq"
OWNED BY "dwd"."policy_recommendation_report"."id";
SELECT setval('"dwd"."policy_recommendation_report_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_search_condition_id_seq"
OWNED BY "dwd"."policy_search_condition"."id";
SELECT setval('"dwd"."policy_search_condition_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_search_record_id_seq"
OWNED BY "dwd"."policy_search_record"."id";
SELECT setval('"dwd"."policy_search_record_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_simulation_param_id_seq"
OWNED BY "dwd"."policy_simulation_param"."id";
SELECT setval('"dwd"."policy_simulation_param_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_simulation_result_id_seq"
OWNED BY "dwd"."policy_simulation_result"."id";
SELECT setval('"dwd"."policy_simulation_result_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_subscription_id_seq"
OWNED BY "dwd"."policy_subscription"."id";
SELECT setval('"dwd"."policy_subscription_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_support_assessment_id_seq"
OWNED BY "dwd"."policy_support_assessment"."id";
SELECT setval('"dwd"."policy_support_assessment_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_support_assessment_indicator_id_seq"
OWNED BY "dwd"."policy_support_assessment_indicator"."id";
SELECT setval('"dwd"."policy_support_assessment_indicator_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_support_overview_id_seq"
OWNED BY "dwd"."policy_support_overview"."id";
SELECT setval('"dwd"."policy_support_overview_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_support_rank_id_seq"
OWNED BY "dwd"."policy_support_rank"."id";
SELECT setval('"dwd"."policy_support_rank_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_time_analysis_id_seq"
OWNED BY "dwd"."policy_time_analysis"."id";
SELECT setval('"dwd"."policy_time_analysis_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_time_series_indicator_id_seq"
OWNED BY "dwd"."policy_time_series_indicator"."id";
SELECT setval('"dwd"."policy_time_series_indicator_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_type_indicator_id_seq"
OWNED BY "dwd"."policy_type_indicator"."id";
SELECT setval('"dwd"."policy_type_indicator_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."policy_weakness_result_id_seq"
OWNED BY "dwd"."policy_weakness_result"."id";
SELECT setval('"dwd"."policy_weakness_result_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."regional_policy_compare_id_seq"
OWNED BY "dwd"."regional_policy_compare"."id";
SELECT setval('"dwd"."regional_policy_compare_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."shenzhen_policy_compare_id_seq"
OWNED BY "dwd"."shenzhen_policy_compare"."id";
SELECT setval('"dwd"."shenzhen_policy_compare_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."shenzhen_policy_distribution_id_seq"
OWNED BY "dwd"."shenzhen_policy_distribution"."id";
SELECT setval('"dwd"."shenzhen_policy_distribution_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."shenzhen_policy_status_id_seq"
OWNED BY "dwd"."shenzhen_policy_status"."id";
SELECT setval('"dwd"."shenzhen_policy_status_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "dwd"."tenant_info_id_seq"
OWNED BY "dwd"."tenant_info"."id";
SELECT setval('"dwd"."tenant_info_id_seq"', 1, false);

-- ----------------------------
-- Indexes structure for table enterprise
-- ----------------------------
CREATE INDEX "idx_business_score" ON "dwd"."enterprise" USING btree (
  "business_score" "pg_catalog"."numeric_ops" ASC NULLS LAST
);
CREATE INDEX "idx_city" ON "dwd"."enterprise" USING btree (
  "headquarters_city" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_enterprise_name" ON "dwd"."enterprise" USING btree (
  "enterprise_name" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_industry" ON "dwd"."enterprise" USING btree (
  "industry_category" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_tech_score" ON "dwd"."enterprise" USING btree (
  "tech_score" "pg_catalog"."numeric_ops" ASC NULLS LAST
);

-- ----------------------------
-- Uniques structure for table enterprise
-- ----------------------------
ALTER TABLE "dwd"."enterprise" ADD CONSTRAINT "uk_enterprise_code" UNIQUE ("enterprise_code");

-- ----------------------------
-- Primary Key structure for table enterprise
-- ----------------------------
ALTER TABLE "dwd"."enterprise" ADD CONSTRAINT "pk_enterprise" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table enterprise_business_tag
-- ----------------------------
CREATE INDEX "idx_ebt_enterprise_id" ON "dwd"."enterprise_business_tag" USING btree (
  "enterprise_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);
CREATE INDEX "idx_ebt_tag_name" ON "dwd"."enterprise_business_tag" USING btree (
  "tag_name" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table enterprise_business_tag
-- ----------------------------
ALTER TABLE "dwd"."enterprise_business_tag" ADD CONSTRAINT "pk_enterprise_business_tag" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table enterprise_cooperation
-- ----------------------------
CREATE INDEX "idx_ec_enterprise_id" ON "dwd"."enterprise_cooperation" USING btree (
  "enterprise_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table enterprise_cooperation
-- ----------------------------
ALTER TABLE "dwd"."enterprise_cooperation" ADD CONSTRAINT "pk_enterprise_cooperation" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table enterprise_finance_history
-- ----------------------------
CREATE INDEX "idx_efh_data_year" ON "dwd"."enterprise_finance_history" USING btree (
  "data_year" "pg_catalog"."int4_ops" ASC NULLS LAST
);
CREATE INDEX "idx_efh_enterprise_id" ON "dwd"."enterprise_finance_history" USING btree (
  "enterprise_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table enterprise_finance_history
-- ----------------------------
ALTER TABLE "dwd"."enterprise_finance_history" ADD CONSTRAINT "pk_enterprise_finance_history" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table enterprise_industry
-- ----------------------------
CREATE INDEX "idx_ei_enterprise_id" ON "dwd"."enterprise_industry" USING btree (
  "enterprise_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);
CREATE INDEX "idx_ei_industry_chain" ON "dwd"."enterprise_industry" USING btree (
  "industry_chain" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table enterprise_industry
-- ----------------------------
ALTER TABLE "dwd"."enterprise_industry" ADD CONSTRAINT "pk_enterprise_industry" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table enterprise_parent_subsidiary
-- ----------------------------
CREATE INDEX "idx_eps_enterprise_id" ON "dwd"."enterprise_parent_subsidiary" USING btree (
  "enterprise_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);
CREATE INDEX "idx_eps_parent_id" ON "dwd"."enterprise_parent_subsidiary" USING btree (
  "parent_enterprise_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table enterprise_parent_subsidiary
-- ----------------------------
ALTER TABLE "dwd"."enterprise_parent_subsidiary" ADD CONSTRAINT "pk_enterprise_parent_subsidiary" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table enterprise_patent_history
-- ----------------------------
CREATE INDEX "idx_eph_data_year" ON "dwd"."enterprise_patent_history" USING btree (
  "data_year" "pg_catalog"."int4_ops" ASC NULLS LAST
);
CREATE INDEX "idx_eph_enterprise_id" ON "dwd"."enterprise_patent_history" USING btree (
  "enterprise_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table enterprise_patent_history
-- ----------------------------
ALTER TABLE "dwd"."enterprise_patent_history" ADD CONSTRAINT "pk_enterprise_patent_history" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table enterprise_supply_chain
-- ----------------------------
CREATE INDEX "idx_esc_enterprise_id" ON "dwd"."enterprise_supply_chain" USING btree (
  "enterprise_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);
CREATE INDEX "idx_esc_related_id" ON "dwd"."enterprise_supply_chain" USING btree (
  "related_enterprise_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table enterprise_supply_chain
-- ----------------------------
ALTER TABLE "dwd"."enterprise_supply_chain" ADD CONSTRAINT "pk_enterprise_supply_chain" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table national_policy_distribution
-- ----------------------------
CREATE INDEX "idx_npd_is_deleted" ON "dwd"."national_policy_distribution" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_npd_province_code" ON "dwd"."national_policy_distribution" USING btree (
  "province_code" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_npd_tenant_stat_date" ON "dwd"."national_policy_distribution" USING btree (
  "tenant_id" "pg_catalog"."int8_ops" ASC NULLS LAST,
  "stat_date" "pg_catalog"."date_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table national_policy_distribution
-- ----------------------------
CREATE TRIGGER "trg_national_policy_distribution_update_time" BEFORE UPDATE ON "dwd"."national_policy_distribution"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table national_policy_distribution
-- ----------------------------
ALTER TABLE "dwd"."national_policy_distribution" ADD CONSTRAINT "national_policy_distribution_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_analysis_report
-- ----------------------------
CREATE INDEX "idx_par_is_deleted" ON "dwd"."policy_analysis_report" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_par_operator_id" ON "dwd"."policy_analysis_report" USING btree (
  "operator_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);
CREATE INDEX "idx_par_report_type" ON "dwd"."policy_analysis_report" USING btree (
  "report_type" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "uk_par_report_no" ON "dwd"."policy_analysis_report" USING btree (
  "report_no" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_analysis_report
-- ----------------------------
CREATE TRIGGER "trg_policy_analysis_report_update_time" BEFORE UPDATE ON "dwd"."policy_analysis_report"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_analysis_report
-- ----------------------------
ALTER TABLE "dwd"."policy_analysis_report" ADD CONSTRAINT "policy_analysis_report_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_base_info
-- ----------------------------
CREATE INDEX "idx_pbi_is_deleted" ON "dwd"."policy_base_info" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pbi_level" ON "dwd"."policy_base_info" USING btree (
  "level" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pbi_publish_date" ON "dwd"."policy_base_info" USING btree (
  "publish_date" "pg_catalog"."date_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pbi_sci_tech" ON "dwd"."policy_base_info" USING btree (
  "sci_tech_attribute" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pbi_status" ON "dwd"."policy_base_info" USING btree (
  "status" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pbi_tenant_id" ON "dwd"."policy_base_info" USING btree (
  "tenant_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "uk_policy_id" ON "dwd"."policy_base_info" USING btree (
  "policy_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_base_info
-- ----------------------------
CREATE TRIGGER "trg_policy_base_info_update_time" BEFORE UPDATE ON "dwd"."policy_base_info"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_base_info
-- ----------------------------
ALTER TABLE "dwd"."policy_base_info" ADD CONSTRAINT "policy_base_info_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_effect_eval
-- ----------------------------
CREATE INDEX "idx_pee_eval_batch" ON "dwd"."policy_effect_eval" USING btree (
  "eval_batch_no" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pee_eval_stage" ON "dwd"."policy_effect_eval" USING btree (
  "eval_stage" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pee_is_deleted" ON "dwd"."policy_effect_eval" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pee_policy_id" ON "dwd"."policy_effect_eval" USING btree (
  "policy_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_effect_eval
-- ----------------------------
CREATE TRIGGER "trg_policy_effect_eval_update_time" BEFORE UPDATE ON "dwd"."policy_effect_eval"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_effect_eval
-- ----------------------------
ALTER TABLE "dwd"."policy_effect_eval" ADD CONSTRAINT "policy_effect_eval_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_entity
-- ----------------------------
CREATE INDEX "idx_pe_entity_type_id" ON "dwd"."policy_entity" USING btree (
  "entity_type_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pe_is_deleted" ON "dwd"."policy_entity" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pe_is_verified" ON "dwd"."policy_entity" USING btree (
  "is_verified" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pe_publish_region" ON "dwd"."policy_entity" USING btree (
  "publish_region" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "uk_pe_entity_code" ON "dwd"."policy_entity" USING btree (
  "entity_code" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_entity
-- ----------------------------
CREATE TRIGGER "trg_policy_entity_update_time" BEFORE UPDATE ON "dwd"."policy_entity"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_entity
-- ----------------------------
ALTER TABLE "dwd"."policy_entity" ADD CONSTRAINT "policy_entity_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_entity_relation
-- ----------------------------
CREATE INDEX "idx_per_entity_id" ON "dwd"."policy_entity_relation" USING btree (
  "entity_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);
CREATE INDEX "idx_per_is_deleted" ON "dwd"."policy_entity_relation" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_per_policy_id" ON "dwd"."policy_entity_relation" USING btree (
  "policy_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_per_relation_type" ON "dwd"."policy_entity_relation" USING btree (
  "relation_type" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_entity_relation
-- ----------------------------
CREATE TRIGGER "trg_policy_entity_relation_update_time" BEFORE UPDATE ON "dwd"."policy_entity_relation"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_entity_relation
-- ----------------------------
ALTER TABLE "dwd"."policy_entity_relation" ADD CONSTRAINT "policy_entity_relation_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_entity_type
-- ----------------------------
CREATE INDEX "idx_pet_is_deleted" ON "dwd"."policy_entity_type" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pet_is_enabled" ON "dwd"."policy_entity_type" USING btree (
  "is_enabled" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pet_parent_id" ON "dwd"."policy_entity_type" USING btree (
  "parent_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "uk_pet_type_code" ON "dwd"."policy_entity_type" USING btree (
  "type_code" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_entity_type
-- ----------------------------
CREATE TRIGGER "trg_policy_entity_type_update_time" BEFORE UPDATE ON "dwd"."policy_entity_type"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_entity_type
-- ----------------------------
ALTER TABLE "dwd"."policy_entity_type" ADD CONSTRAINT "policy_entity_type_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_favorite
-- ----------------------------
CREATE INDEX "idx_pf_favorite_type" ON "dwd"."policy_favorite" USING btree (
  "favorite_type" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pf_is_deleted" ON "dwd"."policy_favorite" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pf_policy_id" ON "dwd"."policy_favorite" USING btree (
  "policy_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pf_user_id" ON "dwd"."policy_favorite" USING btree (
  "user_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_favorite
-- ----------------------------
CREATE TRIGGER "trg_policy_favorite_update_time" BEFORE UPDATE ON "dwd"."policy_favorite"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_favorite
-- ----------------------------
ALTER TABLE "dwd"."policy_favorite" ADD CONSTRAINT "policy_favorite_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_focus_result
-- ----------------------------
CREATE INDEX "idx_pfr_analysis_batch" ON "dwd"."policy_focus_result" USING btree (
  "analysis_batch_no" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pfr_exec_status" ON "dwd"."policy_focus_result" USING btree (
  "exec_status" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pfr_is_deleted" ON "dwd"."policy_focus_result" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pfr_policy_id" ON "dwd"."policy_focus_result" USING btree (
  "policy_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_focus_result
-- ----------------------------
CREATE TRIGGER "trg_policy_focus_result_update_time" BEFORE UPDATE ON "dwd"."policy_focus_result"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_focus_result
-- ----------------------------
ALTER TABLE "dwd"."policy_focus_result" ADD CONSTRAINT "policy_focus_result_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_intensity_eval
-- ----------------------------
CREATE INDEX "idx_pie_eval_batch" ON "dwd"."policy_intensity_eval" USING btree (
  "eval_batch_no" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pie_intensity_level" ON "dwd"."policy_intensity_eval" USING btree (
  "intensity_level" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pie_is_deleted" ON "dwd"."policy_intensity_eval" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pie_policy_id" ON "dwd"."policy_intensity_eval" USING btree (
  "policy_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_intensity_eval
-- ----------------------------
CREATE TRIGGER "trg_policy_intensity_eval_update_time" BEFORE UPDATE ON "dwd"."policy_intensity_eval"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_intensity_eval
-- ----------------------------
ALTER TABLE "dwd"."policy_intensity_eval" ADD CONSTRAINT "policy_intensity_eval_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_interpretation_report
-- ----------------------------
CREATE INDEX "idx_pir_is_deleted" ON "dwd"."policy_interpretation_report" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pir_parent_report_id" ON "dwd"."policy_interpretation_report" USING btree (
  "parent_report_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pir_target_audience" ON "dwd"."policy_interpretation_report" USING btree (
  "target_audience" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "uk_pir_report_no" ON "dwd"."policy_interpretation_report" USING btree (
  "report_no" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_interpretation_report
-- ----------------------------
CREATE TRIGGER "trg_policy_interpretation_report_update_time" BEFORE UPDATE ON "dwd"."policy_interpretation_report"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_interpretation_report
-- ----------------------------
ALTER TABLE "dwd"."policy_interpretation_report" ADD CONSTRAINT "policy_interpretation_report_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_latest_news
-- ----------------------------
CREATE INDEX "idx_pln_is_deleted" ON "dwd"."policy_latest_news" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pln_is_hot" ON "dwd"."policy_latest_news" USING btree (
  "is_hot" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pln_is_shenzhen" ON "dwd"."policy_latest_news" USING btree (
  "is_shenzhen" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pln_news_date" ON "dwd"."policy_latest_news" USING btree (
  "news_date" "pg_catalog"."date_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pln_news_type" ON "dwd"."policy_latest_news" USING btree (
  "news_type" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pln_policy_id" ON "dwd"."policy_latest_news" USING btree (
  "policy_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_latest_news
-- ----------------------------
CREATE TRIGGER "trg_policy_latest_news_update_time" BEFORE UPDATE ON "dwd"."policy_latest_news"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_latest_news
-- ----------------------------
ALTER TABLE "dwd"."policy_latest_news" ADD CONSTRAINT "policy_latest_news_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_layout_recommend
-- ----------------------------
CREATE INDEX "idx_plr_is_deleted" ON "dwd"."policy_layout_recommend" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_plr_recommend_batch" ON "dwd"."policy_layout_recommend" USING btree (
  "recommend_batch_no" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_plr_target_industry" ON "dwd"."policy_layout_recommend" USING btree (
  "target_industry" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_plr_target_region" ON "dwd"."policy_layout_recommend" USING btree (
  "target_region" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_layout_recommend
-- ----------------------------
CREATE TRIGGER "trg_policy_layout_recommend_update_time" BEFORE UPDATE ON "dwd"."policy_layout_recommend"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_layout_recommend
-- ----------------------------
ALTER TABLE "dwd"."policy_layout_recommend" ADD CONSTRAINT "policy_layout_recommend_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_level_indicator
-- ----------------------------
CREATE INDEX "idx_pli_is_deleted" ON "dwd"."policy_level_indicator" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pli_policy_level" ON "dwd"."policy_level_indicator" USING btree (
  "policy_level" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pli_tenant_stat_date" ON "dwd"."policy_level_indicator" USING btree (
  "tenant_id" "pg_catalog"."int8_ops" ASC NULLS LAST,
  "stat_date" "pg_catalog"."date_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_level_indicator
-- ----------------------------
CREATE TRIGGER "trg_policy_level_indicator_update_time" BEFORE UPDATE ON "dwd"."policy_level_indicator"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_level_indicator
-- ----------------------------
ALTER TABLE "dwd"."policy_level_indicator" ADD CONSTRAINT "policy_level_indicator_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_opportunity_result
-- ----------------------------
CREATE INDEX "idx_por_analysis_batch" ON "dwd"."policy_opportunity_result" USING btree (
  "analysis_batch_no" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_por_is_deleted" ON "dwd"."policy_opportunity_result" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_por_opportunity_level" ON "dwd"."policy_opportunity_result" USING btree (
  "opportunity_level" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_por_policy_id" ON "dwd"."policy_opportunity_result" USING btree (
  "policy_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_opportunity_result
-- ----------------------------
CREATE TRIGGER "trg_policy_opportunity_result_update_time" BEFORE UPDATE ON "dwd"."policy_opportunity_result"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_opportunity_result
-- ----------------------------
ALTER TABLE "dwd"."policy_opportunity_result" ADD CONSTRAINT "policy_opportunity_result_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_prediction_indicator
-- ----------------------------
CREATE INDEX "idx_ppi_indicator_category" ON "dwd"."policy_prediction_indicator" USING btree (
  "indicator_category" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_ppi_is_deleted" ON "dwd"."policy_prediction_indicator" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_ppi_simulation_id" ON "dwd"."policy_prediction_indicator" USING btree (
  "simulation_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_prediction_indicator
-- ----------------------------
CREATE TRIGGER "trg_policy_prediction_indicator_update_time" BEFORE UPDATE ON "dwd"."policy_prediction_indicator"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_prediction_indicator
-- ----------------------------
ALTER TABLE "dwd"."policy_prediction_indicator" ADD CONSTRAINT "policy_prediction_indicator_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_public_opinion
-- ----------------------------
CREATE INDEX "idx_ppo_audience_type" ON "dwd"."policy_public_opinion" USING btree (
  "audience_type" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_ppo_eval_period" ON "dwd"."policy_public_opinion" USING btree (
  "eval_period" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_ppo_is_deleted" ON "dwd"."policy_public_opinion" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_ppo_policy_id" ON "dwd"."policy_public_opinion" USING btree (
  "policy_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_public_opinion
-- ----------------------------
CREATE TRIGGER "trg_policy_public_opinion_update_time" BEFORE UPDATE ON "dwd"."policy_public_opinion"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_public_opinion
-- ----------------------------
ALTER TABLE "dwd"."policy_public_opinion" ADD CONSTRAINT "policy_public_opinion_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_recommendation_report
-- ----------------------------
CREATE INDEX "idx_prr_is_deleted" ON "dwd"."policy_recommendation_report" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_prr_parent_report_id" ON "dwd"."policy_recommendation_report" USING btree (
  "parent_report_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "uk_prr_report_no" ON "dwd"."policy_recommendation_report" USING btree (
  "report_no" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_recommendation_report
-- ----------------------------
CREATE TRIGGER "trg_policy_recommendation_report_update_time" BEFORE UPDATE ON "dwd"."policy_recommendation_report"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_recommendation_report
-- ----------------------------
ALTER TABLE "dwd"."policy_recommendation_report" ADD CONSTRAINT "policy_recommendation_report_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_search_condition
-- ----------------------------
CREATE INDEX "idx_psc_condition_type" ON "dwd"."policy_search_condition" USING btree (
  "condition_type" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_psc_is_deleted" ON "dwd"."policy_search_condition" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_psc_search_id" ON "dwd"."policy_search_condition" USING btree (
  "search_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_search_condition
-- ----------------------------
CREATE TRIGGER "trg_policy_search_condition_update_time" BEFORE UPDATE ON "dwd"."policy_search_condition"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_search_condition
-- ----------------------------
ALTER TABLE "dwd"."policy_search_condition" ADD CONSTRAINT "policy_search_condition_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_search_record
-- ----------------------------
CREATE INDEX "idx_psearc_is_deleted" ON "dwd"."policy_search_record" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_psearc_search_time" ON "dwd"."policy_search_record" USING btree (
  "search_time" "pg_catalog"."timestamp_ops" ASC NULLS LAST
);
CREATE INDEX "idx_psearc_user_id" ON "dwd"."policy_search_record" USING btree (
  "user_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "uk_psearc_search_id" ON "dwd"."policy_search_record" USING btree (
  "search_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_search_record
-- ----------------------------
CREATE TRIGGER "trg_policy_search_record_update_time" BEFORE UPDATE ON "dwd"."policy_search_record"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_search_record
-- ----------------------------
ALTER TABLE "dwd"."policy_search_record" ADD CONSTRAINT "policy_search_record_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_simulation_param
-- ----------------------------
CREATE INDEX "idx_psp_exec_status" ON "dwd"."policy_simulation_param" USING btree (
  "exec_status" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_psp_is_deleted" ON "dwd"."policy_simulation_param" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_psp_policy_id" ON "dwd"."policy_simulation_param" USING btree (
  "policy_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_psp_simulation_type" ON "dwd"."policy_simulation_param" USING btree (
  "simulation_type" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "uk_psp_simulation_id" ON "dwd"."policy_simulation_param" USING btree (
  "simulation_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_simulation_param
-- ----------------------------
CREATE TRIGGER "trg_policy_simulation_param_update_time" BEFORE UPDATE ON "dwd"."policy_simulation_param"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_simulation_param
-- ----------------------------
ALTER TABLE "dwd"."policy_simulation_param" ADD CONSTRAINT "policy_simulation_param_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_simulation_result
-- ----------------------------
CREATE INDEX "idx_psre_is_deleted" ON "dwd"."policy_simulation_result" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_psre_result_type" ON "dwd"."policy_simulation_result" USING btree (
  "result_type" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_psre_simulation_id" ON "dwd"."policy_simulation_result" USING btree (
  "simulation_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_simulation_result
-- ----------------------------
CREATE TRIGGER "trg_policy_simulation_result_update_time" BEFORE UPDATE ON "dwd"."policy_simulation_result"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_simulation_result
-- ----------------------------
ALTER TABLE "dwd"."policy_simulation_result" ADD CONSTRAINT "policy_simulation_result_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_subscription
-- ----------------------------
CREATE INDEX "idx_psu_is_deleted" ON "dwd"."policy_subscription" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_psu_is_enabled" ON "dwd"."policy_subscription" USING btree (
  "is_enabled" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_psu_push_frequency" ON "dwd"."policy_subscription" USING btree (
  "push_frequency" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_psu_user_id" ON "dwd"."policy_subscription" USING btree (
  "user_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_subscription
-- ----------------------------
CREATE TRIGGER "trg_policy_subscription_update_time" BEFORE UPDATE ON "dwd"."policy_subscription"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_subscription
-- ----------------------------
ALTER TABLE "dwd"."policy_subscription" ADD CONSTRAINT "policy_subscription_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_support_assessment
-- ----------------------------
CREATE INDEX "idx_psa_is_deleted" ON "dwd"."policy_support_assessment" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_psa_target_domain" ON "dwd"."policy_support_assessment" USING btree (
  "target_domain" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "uk_psa_assessment_id" ON "dwd"."policy_support_assessment" USING btree (
  "assessment_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_support_assessment
-- ----------------------------
CREATE TRIGGER "trg_policy_support_assessment_update_time" BEFORE UPDATE ON "dwd"."policy_support_assessment"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_support_assessment
-- ----------------------------
ALTER TABLE "dwd"."policy_support_assessment" ADD CONSTRAINT "policy_support_assessment_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_support_assessment_indicator
-- ----------------------------
CREATE INDEX "idx_psai_indicator_category" ON "dwd"."policy_support_assessment_indicator" USING btree (
  "indicator_category" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_psai_is_deleted" ON "dwd"."policy_support_assessment_indicator" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_psai_is_enabled" ON "dwd"."policy_support_assessment_indicator" USING btree (
  "is_enabled" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_psai_parent_id" ON "dwd"."policy_support_assessment_indicator" USING btree (
  "parent_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "uk_psai_indicator_code" ON "dwd"."policy_support_assessment_indicator" USING btree (
  "indicator_code" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_support_assessment_indicator
-- ----------------------------
CREATE TRIGGER "trg_policy_support_assessment_indicator_update_time" BEFORE UPDATE ON "dwd"."policy_support_assessment_indicator"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_support_assessment_indicator
-- ----------------------------
ALTER TABLE "dwd"."policy_support_assessment_indicator" ADD CONSTRAINT "policy_support_assessment_indicator_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_support_overview
-- ----------------------------
CREATE INDEX "idx_pso_industry_type" ON "dwd"."policy_support_overview" USING btree (
  "industry_type" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pso_is_deleted" ON "dwd"."policy_support_overview" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pso_scope_type" ON "dwd"."policy_support_overview" USING btree (
  "scope_type" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pso_tenant_stat_date" ON "dwd"."policy_support_overview" USING btree (
  "tenant_id" "pg_catalog"."int8_ops" ASC NULLS LAST,
  "stat_date" "pg_catalog"."date_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_support_overview
-- ----------------------------
CREATE TRIGGER "trg_policy_support_overview_update_time" BEFORE UPDATE ON "dwd"."policy_support_overview"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_support_overview
-- ----------------------------
ALTER TABLE "dwd"."policy_support_overview" ADD CONSTRAINT "policy_support_overview_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_support_rank
-- ----------------------------
CREATE INDEX "idx_psr_industry_type" ON "dwd"."policy_support_rank" USING btree (
  "industry_type" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_psr_is_deleted" ON "dwd"."policy_support_rank" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_psr_rank_type" ON "dwd"."policy_support_rank" USING btree (
  "rank_type" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_psr_tenant_stat_date" ON "dwd"."policy_support_rank" USING btree (
  "tenant_id" "pg_catalog"."int8_ops" ASC NULLS LAST,
  "stat_date" "pg_catalog"."date_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_support_rank
-- ----------------------------
CREATE TRIGGER "trg_policy_support_rank_update_time" BEFORE UPDATE ON "dwd"."policy_support_rank"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_support_rank
-- ----------------------------
ALTER TABLE "dwd"."policy_support_rank" ADD CONSTRAINT "policy_support_rank_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_time_analysis
-- ----------------------------
CREATE INDEX "idx_pta_is_deleted" ON "dwd"."policy_time_analysis" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pta_target_industry" ON "dwd"."policy_time_analysis" USING btree (
  "target_industry" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pta_time_range" ON "dwd"."policy_time_analysis" USING btree (
  "time_range_start" "pg_catalog"."date_ops" ASC NULLS LAST,
  "time_range_end" "pg_catalog"."date_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "uk_pta_analysis_id" ON "dwd"."policy_time_analysis" USING btree (
  "analysis_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_time_analysis
-- ----------------------------
CREATE TRIGGER "trg_policy_time_analysis_update_time" BEFORE UPDATE ON "dwd"."policy_time_analysis"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_time_analysis
-- ----------------------------
ALTER TABLE "dwd"."policy_time_analysis" ADD CONSTRAINT "policy_time_analysis_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_time_series_indicator
-- ----------------------------
CREATE INDEX "idx_ptsi_is_deleted" ON "dwd"."policy_time_series_indicator" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_ptsi_period_label" ON "dwd"."policy_time_series_indicator" USING btree (
  "period_label" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_ptsi_tenant_stat_date" ON "dwd"."policy_time_series_indicator" USING btree (
  "tenant_id" "pg_catalog"."int8_ops" ASC NULLS LAST,
  "stat_date" "pg_catalog"."date_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_time_series_indicator
-- ----------------------------
CREATE TRIGGER "trg_policy_time_series_indicator_update_time" BEFORE UPDATE ON "dwd"."policy_time_series_indicator"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_time_series_indicator
-- ----------------------------
ALTER TABLE "dwd"."policy_time_series_indicator" ADD CONSTRAINT "policy_time_series_indicator_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_type_indicator
-- ----------------------------
CREATE INDEX "idx_pti_is_deleted" ON "dwd"."policy_type_indicator" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pti_policy_type" ON "dwd"."policy_type_indicator" USING btree (
  "policy_type" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pti_tenant_stat_date" ON "dwd"."policy_type_indicator" USING btree (
  "tenant_id" "pg_catalog"."int8_ops" ASC NULLS LAST,
  "stat_date" "pg_catalog"."date_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_type_indicator
-- ----------------------------
CREATE TRIGGER "trg_policy_type_indicator_update_time" BEFORE UPDATE ON "dwd"."policy_type_indicator"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_type_indicator
-- ----------------------------
ALTER TABLE "dwd"."policy_type_indicator" ADD CONSTRAINT "policy_type_indicator_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table policy_weakness_result
-- ----------------------------
CREATE INDEX "idx_pwr_analysis_batch" ON "dwd"."policy_weakness_result" USING btree (
  "analysis_batch_no" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pwr_is_deleted" ON "dwd"."policy_weakness_result" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_pwr_policy_id" ON "dwd"."policy_weakness_result" USING btree (
  "policy_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table policy_weakness_result
-- ----------------------------
CREATE TRIGGER "trg_policy_weakness_result_update_time" BEFORE UPDATE ON "dwd"."policy_weakness_result"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table policy_weakness_result
-- ----------------------------
ALTER TABLE "dwd"."policy_weakness_result" ADD CONSTRAINT "policy_weakness_result_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table regional_policy_compare
-- ----------------------------
CREATE INDEX "idx_rpc_is_deleted" ON "dwd"."regional_policy_compare" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_rpc_target_industry" ON "dwd"."regional_policy_compare" USING btree (
  "target_industry" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "uk_rpc_compare_id" ON "dwd"."regional_policy_compare" USING btree (
  "compare_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table regional_policy_compare
-- ----------------------------
CREATE TRIGGER "trg_regional_policy_compare_update_time" BEFORE UPDATE ON "dwd"."regional_policy_compare"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table regional_policy_compare
-- ----------------------------
ALTER TABLE "dwd"."regional_policy_compare" ADD CONSTRAINT "regional_policy_compare_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table shenzhen_policy_compare
-- ----------------------------
CREATE INDEX "idx_spc_compare_type" ON "dwd"."shenzhen_policy_compare" USING btree (
  "compare_type" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_spc_district_code" ON "dwd"."shenzhen_policy_compare" USING btree (
  "district_code" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_spc_is_deleted" ON "dwd"."shenzhen_policy_compare" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_spc_tenant_stat_date" ON "dwd"."shenzhen_policy_compare" USING btree (
  "tenant_id" "pg_catalog"."int8_ops" ASC NULLS LAST,
  "stat_date" "pg_catalog"."date_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table shenzhen_policy_compare
-- ----------------------------
CREATE TRIGGER "trg_shenzhen_policy_compare_update_time" BEFORE UPDATE ON "dwd"."shenzhen_policy_compare"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table shenzhen_policy_compare
-- ----------------------------
ALTER TABLE "dwd"."shenzhen_policy_compare" ADD CONSTRAINT "shenzhen_policy_compare_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table shenzhen_policy_distribution
-- ----------------------------
CREATE INDEX "idx_spd_district_code" ON "dwd"."shenzhen_policy_distribution" USING btree (
  "district_code" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_spd_is_deleted" ON "dwd"."shenzhen_policy_distribution" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_spd_tenant_stat_date" ON "dwd"."shenzhen_policy_distribution" USING btree (
  "tenant_id" "pg_catalog"."int8_ops" ASC NULLS LAST,
  "stat_date" "pg_catalog"."date_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table shenzhen_policy_distribution
-- ----------------------------
CREATE TRIGGER "trg_shenzhen_policy_distribution_update_time" BEFORE UPDATE ON "dwd"."shenzhen_policy_distribution"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table shenzhen_policy_distribution
-- ----------------------------
ALTER TABLE "dwd"."shenzhen_policy_distribution" ADD CONSTRAINT "shenzhen_policy_distribution_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table shenzhen_policy_status
-- ----------------------------
CREATE INDEX "idx_sps_is_deleted" ON "dwd"."shenzhen_policy_status" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_sps_target_industry" ON "dwd"."shenzhen_policy_status" USING btree (
  "target_industry" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "uk_sps_analysis_id" ON "dwd"."shenzhen_policy_status" USING btree (
  "analysis_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table shenzhen_policy_status
-- ----------------------------
CREATE TRIGGER "trg_shenzhen_policy_status_update_time" BEFORE UPDATE ON "dwd"."shenzhen_policy_status"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table shenzhen_policy_status
-- ----------------------------
ALTER TABLE "dwd"."shenzhen_policy_status" ADD CONSTRAINT "shenzhen_policy_status_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table tenant_info
-- ----------------------------
CREATE INDEX "idx_tenant_type" ON "dwd"."tenant_info" USING btree (
  "tenant_type" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_ti_is_deleted" ON "dwd"."tenant_info" USING btree (
  "is_deleted" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE INDEX "idx_ti_status" ON "dwd"."tenant_info" USING btree (
  "status" "pg_catalog"."int2_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "uk_tenant_code" ON "dwd"."tenant_info" USING btree (
  "tenant_code" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Triggers structure for table tenant_info
-- ----------------------------
CREATE TRIGGER "trg_tenant_info_update_time" BEFORE UPDATE ON "dwd"."tenant_info"
FOR EACH ROW
EXECUTE PROCEDURE "dwd"."update_timestamp_func"();

-- ----------------------------
-- Primary Key structure for table tenant_info
-- ----------------------------
ALTER TABLE "dwd"."tenant_info" ADD CONSTRAINT "tenant_info_pkey" PRIMARY KEY ("id");
